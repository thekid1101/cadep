"""Specialist output compression — Pydantic extraction + token budget enforcement (PRD Section 6.4)."""

from __future__ import annotations

import re

from cadep import config
from cadep.models import (
    CompressedPanelInput,
    DevilsAdvocateOutput,
    NormalizedInput,
    RetrievalBundle,
    SpecialistOutput,
)


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English text."""
    return len(text) // 4


def compress_panel(
    proposal: NormalizedInput,
    specialist: SpecialistOutput | None,
    da: DevilsAdvocateOutput | None,
    retrieval: RetrievalBundle,
    system_prompt_tokens: int = 1500,
) -> CompressedPanelInput:
    """Assemble synthesizer input in strict priority order per PRD Section 6.4."""
    budget = config.SYNTHESIZER_MAX_INPUT_TOKENS
    overflow_actions: list[str] = []

    # Priority 1: System prompt (never truncated, allocated separately)
    remaining = budget - system_prompt_tokens

    # Priority 2: User constraints (verbatim, never summarized)
    constraints_text = _build_constraints(proposal)
    constraints_tokens = estimate_tokens(constraints_text)
    remaining -= constraints_tokens

    # Priority 3: Critical issues from specialists (verbatim)
    critical_text = ""
    if specialist:
        critical_text = _extract_critical_issues(specialist)
    critical_tokens = estimate_tokens(critical_text)
    remaining -= critical_tokens

    # Priority 4: Conflicts between specialists (verbatim)
    # In 2+1 panel there's only one specialist, so conflicts come from
    # specialist vs DA disagreements
    conflicts_text = ""
    if specialist and da:
        conflicts_text = _extract_conflicts(specialist, da)
    conflicts_tokens = estimate_tokens(conflicts_text)
    remaining -= conflicts_tokens

    # Priority 5: Retrieval metadata
    retrieval_meta = {
        "confidence": retrieval.confidence.value,
        "docs_retrieved": len(retrieval.results),
        "concept_tags_matched": retrieval.concept_tags_matched,
        "tfidf_fallback_used": retrieval.tfidf_triggered,
    }
    meta_tokens = 200  # Fixed allocation
    remaining -= meta_tokens

    # Priority 6: Devil's Advocate output (verbatim — already concise)
    da_text = ""
    if da:
        da_text = da.raw_text
    da_tokens = estimate_tokens(da_text)
    remaining -= da_tokens

    # Priority 7: Validated core premise
    validated_text = ""
    if specialist and specialist.validated:
        validated_text = "; ".join(specialist.validated[:2])
    validated_tokens = estimate_tokens(validated_text)
    remaining -= validated_tokens

    # Priority 8: Improvements (summarized)
    improvements_text = ""
    if specialist and specialist.improvements:
        improvements_text = _summarize_improvements(specialist)
    improvements_tokens = estimate_tokens(improvements_text)

    # Overflow handling per PRD:
    # If sum exceeds budget after priorities 1-6:
    # - IMPROVEMENTS (priority 8) truncated first
    # - If still over, DA summarized to top 3 points
    # - Validated premise (priority 7) retained under pressure
    # - Priorities 1-5 never truncated
    if remaining < improvements_tokens:
        # Truncate improvements
        if remaining > 0:
            char_limit = remaining * 4
            improvements_text = improvements_text[:char_limit] + "..."
            overflow_actions.append("IMPROVEMENTS truncated to fit token budget")
        else:
            improvements_text = ""
            overflow_actions.append("IMPROVEMENTS dropped — token budget exceeded")

        # Check if we still need more room
        if remaining < 0:
            # Summarize DA to top 3
            if da:
                da_text = _summarize_da(da)
                saved = da_tokens - estimate_tokens(da_text)
                remaining += saved
                overflow_actions.append("DA output summarized to top 3 points")

    # Check if priorities 1-5 alone exceed budget (flag for manual review)
    p1_5_tokens = (
        system_prompt_tokens + constraints_tokens + critical_tokens
        + conflicts_tokens + meta_tokens
    )
    if p1_5_tokens > budget:
        overflow_actions.append(
            "WARNING: Priorities 1-5 alone exceed token budget. "
            "Flag for manual review."
        )

    total = (
        system_prompt_tokens + constraints_tokens + critical_tokens
        + conflicts_tokens + meta_tokens + da_tokens
        + validated_tokens + improvements_tokens
    )

    return CompressedPanelInput(
        system_prompt_tokens=system_prompt_tokens,
        user_constraints=constraints_text,
        critical_issues_text=critical_text,
        conflicts_text=conflicts_text,
        retrieval_metadata=retrieval_meta,
        devils_advocate_text=da_text,
        validated_premise=validated_text,
        improvements_text=improvements_text,
        total_estimated_tokens=total,
        overflow_actions=overflow_actions,
    )


def _build_constraints(proposal: NormalizedInput) -> str:
    parts = []
    if proposal.inferred_constraints:
        parts.append("Constraints: " + "; ".join(proposal.inferred_constraints))
    if proposal.key_assumptions:
        parts.append(f"Key Assumptions: {proposal.key_assumptions}")
    return "\n".join(parts)


def _extract_critical_issues(specialist: SpecialistOutput) -> str:
    if not specialist.critical_issues:
        return "No critical issues identified."

    lines = []
    for issue in specialist.critical_issues:
        line = f"- [{issue.severity.value}] {issue.description}"
        if issue.condition:
            line += f" (Condition: {issue.condition})"
        for cite in issue.citations:
            line += f"\n  Citation: {cite.claim} — {cite.source}"
        lines.append(line)
    return "\n".join(lines)


def _extract_conflicts(
    specialist: SpecialistOutput, da: DevilsAdvocateOutput
) -> str:
    """Identify where specialist and DA disagree."""
    # Simple heuristic: if DA attacks assumptions that specialist validated
    conflicts = []
    validated_lower = {v.lower() for v in specialist.validated}

    for attack in da.assumption_attacks + da.transfer_risks:
        desc_lower = attack.description.lower()
        for v in validated_lower:
            # Rough overlap check
            shared_words = set(desc_lower.split()) & set(v.split())
            if len(shared_words) >= 3:
                conflicts.append(
                    f"Specialist validated: \"{v[:100]}\"\n"
                    f"DA challenges: \"{attack.description[:100]}\""
                )
                break

    if not conflicts:
        return ""
    return "\n\n".join(conflicts)


def _summarize_improvements(specialist: SpecialistOutput) -> str:
    """One sentence per improvement."""
    lines = []
    for imp in specialist.improvements:
        # Truncate to first sentence
        desc = imp.description.split(".")[0] + "."
        lines.append(f"- {desc}")
    return "\n".join(lines)


def _summarize_da(da: DevilsAdvocateOutput) -> str:
    """Summarize DA output to top 3 points."""
    all_points = (
        da.assumption_attacks + da.transfer_risks + da.practical_failure_modes
    )
    top_3 = all_points[:3]
    lines = [f"- [{p.dimension}] {p.description}" for p in top_3]
    return "\n".join(lines)
