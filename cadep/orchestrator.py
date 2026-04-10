"""Main orchestrator — async flow tying all components together (PRD Section 4.1)."""

from __future__ import annotations

import asyncio
import json
import re
import time
from datetime import datetime, timezone

from cadep import config
from cadep.agents.devils_advocate import DevilsAdvocateAgent
from cadep.agents.specialist import SpecialistAgent
from cadep.agents.synthesizer import SynthesizerAgent
from cadep.audit_logger import AuditLogger
from cadep.domain_classifier import DomainClassifier
from cadep.drift_scanner import parse_fast_path_fields, scan_fast_path
from cadep.escalation_checker import check_escalation
from cadep.friction_generator import FrictionGenerator
from cadep.input_normalizer import InputNormalizer
from cadep.models import (
    CitedClaim,
    DAAttack,
    DevilsAdvocateOutput,
    ExecutionRecord,
    FastPathOutput,
    InputQuality,
    NormalizedInput,
    PanelMode,
    PanelResult,
    RetrievalConfidence,
    SpecialistIssue,
    SpecialistOutput,
    SubmissionRecord,
    SynthesizerOutput,
)
from cadep.output_formatter import format_fast_path, format_full_audit
from cadep.retrieval import VaultRetriever
from cadep.specialist_compressor import compress_panel
from cadep.token_logger import TokenLogger


class Orchestrator:
    """Runs the CADEP panel flow end-to-end."""

    def __init__(self):
        self.normalizer = InputNormalizer()
        self.classifier = DomainClassifier()
        self.friction_gen = FrictionGenerator()
        self.token_logger = TokenLogger()
        self.audit_logger = AuditLogger()

    async def submit(
        self,
        raw_input: str,
        mode: PanelMode = PanelMode.FAST,
        proposal_file: str | None = None,
    ) -> dict:
        """Run a full panel submission. Returns result dict for CLI display."""
        if not config.ANTHROPIC_API_KEY:
            return {
                "success": False,
                "error": "ANTHROPIC_API_KEY not set. Create a .env file in the project root:\n"
                         "  ANTHROPIC_API_KEY=your-key-here\n"
                         "Or set the environment variable directly.",
                "query_id": "",
            }

        start_time = time.monotonic()
        query_id = self._generate_query_id()

        # Load from file if provided
        if proposal_file:
            from pathlib import Path
            p = Path(proposal_file)
            if p.exists():
                raw_input = p.read_text(encoding="utf-8")

        # Check backlog before full audit
        if mode == PanelMode.FULL:
            unresolved = self.audit_logger.get_unresolved_audits()
            if len(unresolved) >= config.MAX_UNRESOLVED_AUDITS:
                return {
                    "success": False,
                    "error": f"Unresolved audit backlog ({len(unresolved)}) exceeds limit ({config.MAX_UNRESOLVED_AUDITS}). "
                             f"Resolve pending audits first. Fast-path remains available.",
                    "query_id": query_id,
                }

        # Step 1: Normalize input
        proposal, norm_usage = await self.normalizer.normalize(raw_input)
        if norm_usage:
            from cadep.agents.base import TokenUsage
            self.token_logger.log(
                TokenUsage(**{k: v for k, v in norm_usage.items() if k != "cost"}),
                "normalizer", query_id,
            )

        # Handle underspecified input
        if proposal.input_quality == InputQuality.UNDERSPECIFIED:
            return {
                "success": False,
                "error": "underspecified",
                "clarification": proposal.clarification_reason,
                "query_id": query_id,
            }

        # Handle ambiguous input (Tier B)
        if proposal.input_quality == InputQuality.AMBIGUOUS and proposal.clarification_asked:
            return {
                "success": False,
                "error": "ambiguous",
                "clarification": proposal.clarification_reason,
                "query_id": query_id,
                "proposal": proposal.model_dump(),
            }

        # Step 2: Domain classification
        vault_id, class_confidence, class_usage = await self.classifier.classify(proposal)
        if class_usage:
            from cadep.agents.base import TokenUsage
            self.token_logger.log(
                TokenUsage(**{k: v for k, v in class_usage.items() if k != "cost"}),
                "classifier", query_id,
            )

        if not vault_id:
            return {
                "success": False,
                "error": "No vault available. Create a vault first.",
                "query_id": query_id,
            }

        # Step 3: Retrieval
        retriever = VaultRetriever(vault_id)
        concept_tags = self._extract_concept_tags(proposal)
        query_text = f"{proposal.normalized_problem_statement} {proposal.normalized_proposed_approach}"
        retrieval = retriever.retrieve(concept_tags, query_text)
        doc_ids = [r.doc_id for r in retrieval.results]
        documents = retriever.get_documents(doc_ids)

        # Step 4: Parallel specialist + DA dispatch
        specialist_agent = SpecialistAgent()
        da_agent = DevilsAdvocateAgent()

        specialist_task = specialist_agent.run(proposal, documents, vault_id, mode)
        da_task = da_agent.run(proposal)
        spec_result, da_result = await asyncio.gather(specialist_task, da_task)

        # Log token usage
        if spec_result.success:
            self.token_logger.log(spec_result.usage, "specialist", query_id)
        if da_result.success:
            self.token_logger.log(da_result.usage, "devils_advocate", query_id)

        # Parse specialist output
        specialist_output = self._parse_specialist(spec_result.text, vault_id) if spec_result.success else None
        da_output = self._parse_da(da_result.text) if da_result.success else None

        # Check for panel degradation
        panel_degraded = not spec_result.success or not da_result.success
        degradation_reason = None
        if panel_degraded:
            failed = []
            if not spec_result.success:
                failed.append(f"Specialist: {spec_result.error}")
            if not da_result.success:
                failed.append(f"DA: {da_result.error}")
            degradation_reason = "; ".join(failed)

        # Step 5: Compress specialist output for synthesizer
        compressed = compress_panel(proposal, specialist_output, da_output, retrieval)

        # Step 6: Synthesizer
        synth_agent = SynthesizerAgent()
        synth_result = await synth_agent.run(compressed, mode)

        if synth_result.success:
            self.token_logger.log(synth_result.usage, "synthesizer", query_id)

        runtime = time.monotonic() - start_time

        # Build panel result
        panel_result = PanelResult(
            query_id=query_id,
            mode=mode,
            specialist_output=specialist_output,
            da_output=da_output,
            panel_degraded=panel_degraded,
            degradation_reason=degradation_reason,
            retrieved_docs=doc_ids,
            retrieval_confidence=retrieval.confidence,
            runtime_seconds=round(runtime, 1),
            total_tokens=self.token_logger.session_tokens,
            estimated_cost=round(self.token_logger.session_cost, 4),
        )

        # Route based on mode
        if mode == PanelMode.FAST:
            return await self._handle_fast_path(
                panel_result, proposal, synth_result.text, query_id
            )
        else:
            return await self._handle_full_audit(
                panel_result, proposal, synth_result.text, query_id
            )

    async def _handle_fast_path(
        self,
        panel: PanelResult,
        proposal: NormalizedInput,
        raw_synth: str,
        query_id: str,
    ) -> dict:
        """Process fast-path output with drift scanning and escalation check."""
        # Step 7: Parse into exactly 3 fields
        fields = parse_fast_path_fields(raw_synth)

        # Drift scan
        warnings = scan_fast_path(raw_synth)

        # Escalation check
        escalation = check_escalation(raw_synth)

        fast_output = FastPathOutput(
            likely_failure_point=fields["likely_failure_point"],
            untested_assumption=fields["untested_assumption"],
            check_next=fields["check_next"],
            drift_warnings=warnings,
            escalation_triggered=escalation,
        )

        panel.fast_path_output = fast_output

        # Log submission + execution
        self._log_submission_and_execution(panel, proposal)

        # Format display
        display = format_fast_path(fast_output, proposal, query_id)

        return {
            "success": True,
            "mode": "fast",
            "query_id": query_id,
            "display": display,
            "runtime_seconds": panel.runtime_seconds,
            "tokens": panel.total_tokens,
            "cost": panel.estimated_cost,
        }

    async def _handle_full_audit(
        self,
        panel: PanelResult,
        proposal: NormalizedInput,
        raw_synth: str,
        query_id: str,
    ) -> dict:
        """Process full-audit output with friction question generation."""
        # Parse synthesizer output into structured form
        synth_output = self._parse_synthesizer(raw_synth)
        panel.synthesizer_output = synth_output

        # Generate friction question
        friction_q, friction_usage = await self.friction_gen.generate(panel)
        if friction_usage:
            from cadep.agents.base import TokenUsage
            self.token_logger.log(
                TokenUsage(**{k: v for k, v in friction_usage.items() if k != "cost"}),
                "friction", query_id,
            )

        # Format and save markdown
        markdown = format_full_audit(panel, proposal)
        output_path = self.audit_logger.save_panel_output(query_id, markdown)

        # Persist friction question alongside panel output
        self.audit_logger.save_friction_question(query_id, friction_q)

        # Log submission + execution
        self._log_submission_and_execution(panel, proposal)

        return {
            "success": True,
            "mode": "full",
            "query_id": query_id,
            "output_path": str(output_path),
            "friction_question": friction_q,
            "runtime_seconds": panel.runtime_seconds,
            "tokens": panel.total_tokens,
            "cost": panel.estimated_cost,
        }

    def _log_submission_and_execution(
        self, panel: PanelResult, proposal: NormalizedInput
    ) -> None:
        self.audit_logger.log_submission(SubmissionRecord(
            query_id=panel.query_id,
            date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            mode=panel.mode.value,
            input_quality=proposal.input_quality.value,
            proposal_title=proposal.normalized_problem_statement[:80],
        ))
        self.audit_logger.log_execution(ExecutionRecord(
            query_id=panel.query_id,
            panel_config={
                "specialist": panel.specialist_output.vault_id if panel.specialist_output else "none",
                "devils_advocate": panel.da_output is not None,
                "synthesizer": True,
            },
            retrieved_docs=panel.retrieved_docs,
            panel_degraded=panel.panel_degraded,
            runtime_seconds=panel.runtime_seconds,
            token_cost_estimate=panel.estimated_cost,
        ))

    def _generate_query_id(self) -> str:
        now = datetime.now(timezone.utc)
        date_part = now.strftime("%Y-%m-%d")
        # Count existing submissions for today
        existing = self.audit_logger.get_submissions()
        today_count = sum(1 for s in existing if s.get("date") == date_part)
        return f"{date_part}-{today_count + 1:03d}"

    def _extract_concept_tags(self, proposal: NormalizedInput) -> list[str]:
        """Extract likely concept tags from proposal text for retrieval."""
        text = f"{proposal.normalized_problem_statement} {proposal.normalized_proposed_approach}".lower()
        # Map common terms to concept tags
        tag_keywords = {
            "covariance": ["covariance-estimation"],
            "shrinkage": ["shrinkage", "covariance-estimation.high-dimensional"],
            "copula": ["copula", "dependence-modeling"],
            "t-copula": ["copula", "dependence-modeling", "tail-dependence"],
            "gaussian copula": ["copula", "dependence-modeling"],
            "correlation": ["dependence-modeling", "covariance-estimation"],
            "bootstrap": ["bootstrap", "simulation"],
            "high-dimensional": ["covariance-estimation.high-dimensional"],
            "dimensionality": ["covariance-estimation.high-dimensional"],
            "graphical lasso": ["graphical-lasso", "covariance-estimation"],
            "regularization": ["regularization"],
            "monte carlo": ["simulation"],
            "tail dependence": ["tail-dependence", "copula"],
            "sample size": ["covariance-estimation.high-dimensional"],
        }

        tags = set()
        for keyword, tag_list in tag_keywords.items():
            if keyword in text:
                tags.update(tag_list)

        return list(tags) if tags else ["general"]

    def _parse_specialist(self, text: str, vault_id: str) -> SpecialistOutput:
        """Parse raw specialist text into structured output with citations."""
        output = SpecialistOutput(vault_id=vault_id, raw_text=text)

        sections = self._split_sections(text)

        # Group multi-line items into blocks (Issue/Condition/Citation/Severity = one block)
        for block in self._group_into_blocks(sections.get("CRITICAL ISSUES", []), ["Issue"]):
            issue = self._parse_specialist_issue(block, default_severity="CRITICAL")
            output.critical_issues.append(issue)

        for block in self._group_into_blocks(sections.get("IMPROVEMENTS", []), ["Issue", "Suggestion"]):
            issue = self._parse_specialist_issue(block, default_severity="MEDIUM")
            output.improvements.append(issue)

        output.validated = sections.get("VALIDATED", [])
        output.unknown = sections.get("UNKNOWN", [])

        return output

    def _group_into_blocks(self, items: list[str], primary_labels: list[str]) -> list[str]:
        """Group consecutive items into blocks starting at primary field labels.

        E.g. Issue + Condition + Citation + Severity = one block.
        """
        if not items:
            return []

        # Build regex for primary labels that start a new block
        primary_pattern = "|".join(re.escape(f"**{label}**") for label in primary_labels)
        # Also treat lines without ** prefix as primary if no labels match at all
        has_any_primary = any(
            re.search(primary_pattern, item) for item in items
        )

        if not has_any_primary:
            # No structured labels found — each item is its own block
            return items

        blocks: list[str] = []
        current_lines: list[str] = []

        for item in items:
            if re.search(primary_pattern, item) and current_lines:
                blocks.append("\n".join(current_lines))
                current_lines = []
            current_lines.append(item)

        if current_lines:
            blocks.append("\n".join(current_lines))

        return blocks

    def _parse_specialist_issue(self, text: str, default_severity: str = "HIGH") -> SpecialistIssue:
        """Extract structured fields from a specialist issue block."""
        description = text
        severity = default_severity
        condition = None
        citations: list[CitedClaim] = []

        # Extract severity if tagged: **Severity**: CRITICAL
        sev_match = re.search(r"\*\*Severity\*\*:\s*(CRITICAL|HIGH|MEDIUM|LOW)", text, re.IGNORECASE)
        if sev_match:
            severity = sev_match.group(1).upper()
            description = text[:sev_match.start()].strip()

        # Extract condition: **Condition**: ...
        cond_match = re.search(r"\*\*Condition\*\*:\s*(.+?)(?=\*\*|$)", text, re.DOTALL)
        if cond_match:
            condition = cond_match.group(1).strip()

        # Extract citations: **Citation**: Author(s) (Year) — finding
        # Also handles inline: "Author (Year) — finding" patterns
        cite_patterns = [
            r"\*\*Citation\*\*:\s*(.+?)(?=\*\*|$)",  # Bold-labeled
            r"(?:^|\n)\s*[-*]\s*Citation:\s*(.+)",     # List-item labeled
        ]
        for pattern in cite_patterns:
            for match in re.finditer(pattern, text, re.MULTILINE):
                cite_text = match.group(1).strip()
                if "—" in cite_text:
                    source, claim = cite_text.split("—", 1)
                    citations.append(CitedClaim(claim=claim.strip(), source=source.strip()))
                else:
                    citations.append(CitedClaim(claim=cite_text, source="unspecified"))

        # Fallback: detect inline Author (Year) patterns as citations
        if not citations:
            inline_cites = re.findall(
                r"([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)*(?:\s+et\s+al\.?)?\s*\(\d{4}\)[^.]*\.?)",
                text,
            )
            for cite in inline_cites[:3]:
                if "—" in cite:
                    source, claim = cite.split("—", 1)
                    citations.append(CitedClaim(claim=claim.strip(), source=source.strip()))
                else:
                    citations.append(CitedClaim(claim=cite.strip(), source=cite.strip()))

        # Clean description: remove extracted subfields
        for pattern in [r"\*\*Severity\*\*:[^\n]*", r"\*\*Condition\*\*:[^\n]*", r"\*\*Citation\*\*:[^\n]*"]:
            description = re.sub(pattern, "", description).strip()

        # Extract the core issue description (first field)
        issue_match = re.search(r"\*\*Issue\*\*:\s*(.+?)(?=\*\*|$)", description, re.DOTALL)
        if issue_match:
            description = issue_match.group(1).strip()

        # Infer severity from keywords if not explicitly tagged
        if not sev_match:
            text_lower = text.lower()
            if any(w in text_lower for w in ["critical", "fundamentally", "cannot work", "fails entirely"]):
                severity = "CRITICAL"
            elif any(w in text_lower for w in ["significant", "substantial", "important"]):
                severity = "HIGH"

        return SpecialistIssue(
            description=description or text[:200],
            severity=severity,
            citations=citations,
            condition=condition,
        )

    def _parse_da(self, text: str) -> DevilsAdvocateOutput:
        """Parse raw DA text into structured output with falsifiable conditions."""
        output = DevilsAdvocateOutput(raw_text=text)

        sections = self._split_sections(text)

        for block in self._group_into_blocks(sections.get("ASSUMPTION ATTACKS", []), ["Assumption"]):
            output.assumption_attacks.append(self._parse_da_attack(block, "hidden_assumption"))

        for block in self._group_into_blocks(sections.get("TRANSFER RISKS", []), ["Risk"]):
            output.transfer_risks.append(self._parse_da_attack(block, "transfer_risk"))

        for block in self._group_into_blocks(sections.get("PRACTICAL FAILURE MODES", []), ["Mode"]):
            output.practical_failure_modes.append(self._parse_da_attack(block, "operational_failure"))

        return output

    def _parse_da_attack(self, text: str, dimension: str) -> DAAttack:
        """Extract structured fields from a DA attack block."""
        description = text
        falsifiable_condition = None

        # Extract labeled fields
        # **Assumption**: ... / **Risk**: ... / **Mode**: ...
        for label in ["Assumption", "Risk", "Mode"]:
            match = re.search(rf"\*\*{label}\*\*:\s*(.+?)(?=\*\*|$)", text, re.DOTALL)
            if match:
                description = match.group(1).strip()

        # **If false**: ... / **Falsifiable test**: ... / **Trigger**: ...
        for label in ["If false", "Falsifiable test", "Trigger"]:
            match = re.search(rf"\*\*{label}\*\*:\s*(.+?)(?=\*\*|$)", text, re.DOTALL)
            if match:
                falsifiable_condition = match.group(1).strip()

        return DAAttack(
            description=description or text[:200],
            dimension=dimension,
            falsifiable_condition=falsifiable_condition,
        )

    def _parse_synthesizer(self, text: str) -> SynthesizerOutput:
        """Parse raw synthesizer text into structured output."""
        sections = self._split_sections(text)

        failure = self._join_section(sections.get("MOST LIKELY FAILURE POINT", []))
        second = self._join_section(sections.get("SECOND INDEPENDENT BLOCKER", []))
        why = self._join_section(sections.get("WHY THIS MATTERS", []))
        uncertainty = self._join_section(sections.get("STRONGEST UNRESOLVED UNCERTAINTY", []))
        next_move = self._join_section(sections.get("SUGGESTED NEXT MOVE", []))

        evidence = []
        for item in sections.get("EVIDENCE", []):
            if "—" in item:
                claim, source = item.rsplit("—", 1)
                evidence.append(CitedClaim(claim=claim.strip(), source=source.strip()))
            else:
                evidence.append(CitedClaim(claim=item, source="unspecified"))

        verification = sections.get("WHAT YOU MUST VERIFY PERSONALLY", [])
        ungrounded = sections.get("UNGROUNDED CHALLENGES", [])

        return SynthesizerOutput(
            likely_failure_point=failure or text[:500],
            second_blocker=second or None,
            why_it_matters=why or "",
            evidence=evidence,
            strongest_uncertainty=uncertainty or "",
            verification_steps=verification,
            suggested_next_move=next_move or "",
            ungrounded_challenges=ungrounded,
            raw_text=text,
        )

    def _split_sections(self, text: str) -> dict[str, list[str]]:
        """Split markdown-style output into sections."""
        sections: dict[str, list[str]] = {}
        current_section = None
        current_items: list[str] = []

        for line in text.splitlines():
            line = line.strip()
            # Check for section headers (### or ##)
            header_match = re.match(r"^#{1,3}\s+(.+)$", line)
            if header_match:
                if current_section is not None:
                    sections[current_section] = current_items
                current_section = header_match.group(1).strip().upper()
                current_items = []
                continue

            # Check for bold section headers like **CRITICAL ISSUES**
            bold_match = re.match(r"^\*\*(.+?)\*\*\s*$", line)
            if bold_match:
                if current_section is not None:
                    sections[current_section] = current_items
                current_section = bold_match.group(1).strip().upper()
                current_items = []
                continue

            # Collect items
            if current_section is not None and line:
                # Remove leading bullet/number markers
                item = re.sub(r"^[-*•]\s*", "", line)
                item = re.sub(r"^\d+[\.\)]\s*", "", item)
                if item:
                    current_items.append(item)

        if current_section is not None:
            sections[current_section] = current_items

        return sections

    def _join_section(self, items: list[str]) -> str:
        return " ".join(items) if items else ""
