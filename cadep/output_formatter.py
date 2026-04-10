"""Output formatting — fast-path inline + full-audit markdown (PRD Section 7)."""

from __future__ import annotations

from datetime import datetime, timezone

from cadep.models import (
    FastPathOutput,
    NormalizedInput,
    PanelResult,
    SynthesizerOutput,
)
from cadep.prompts import (
    BELOW_SCHEMA_NOTE,
    CRITICAL_ESCALATION,
    FAST_PATH_HEADER,
)


def format_fast_path(
    fast_path: FastPathOutput,
    proposal: NormalizedInput,
    query_id: str,
) -> str:
    """Format fast-path output for inline display (PRD Section 7.2)."""
    lines = []

    # Below-schema warning if applicable
    if proposal.input_quality.value in ("messy-but-runnable", "ambiguous"):
        lines.append(BELOW_SCHEMA_NOTE)
        lines.append("")

    lines.append(f"⚡ {FAST_PATH_HEADER}")
    lines.append("")

    lines.append(
        f"1. LIKELY FAILURE POINT: {fast_path.likely_failure_point}"
    )
    lines.append("")
    lines.append(
        f"2. UNTESTED ASSUMPTION: {fast_path.untested_assumption}"
    )
    lines.append("")
    lines.append(
        f"3. CHECK NEXT: {fast_path.check_next}"
    )

    # Drift warnings
    for warning in fast_path.drift_warnings:
        lines.append("")
        lines.append(f"⚠️  {warning}")

    # Escalation
    if fast_path.escalation_triggered:
        lines.append("")
        lines.append(f"⚠️  {CRITICAL_ESCALATION}")

    return "\n".join(lines)


def format_full_audit(
    panel: PanelResult,
    proposal: NormalizedInput,
) -> str:
    """Format full-audit output as markdown (PRD Section 7.1)."""
    syn = panel.synthesizer_output
    if not syn:
        return "# CADEP Full Audit\n\nError: Synthesizer produced no output."

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    parts = []
    parts.append(f"# CADEP Full Audit")
    parts.append(f"Query ID: {panel.query_id}")
    parts.append(f"Date: {date}")
    parts.append(f"Proposal: {proposal.normalized_problem_statement[:80]}")
    parts.append("")

    # Proposal Snapshot
    parts.append("## Proposal Snapshot")
    parts.append(f"**Problem**")
    parts.append(proposal.normalized_problem_statement)
    parts.append("")
    parts.append(f"**Proposed Approach**")
    parts.append(proposal.normalized_proposed_approach)
    parts.append("")
    if proposal.inferred_constraints:
        parts.append(f"**Explicit Constraints**")
        parts.append("; ".join(proposal.inferred_constraints))
        parts.append("")

    parts.append("---")
    parts.append("")

    # 1) Most Likely Failure Point
    parts.append("## 1) Most Likely Failure Point")
    parts.append(syn.likely_failure_point)
    parts.append("")

    if syn.second_blocker:
        parts.append("## 1b) Second Independent Blocker")
        parts.append(syn.second_blocker)
        parts.append("")

    # 2) Why This Matters
    parts.append("## 2) Why This Matters")
    parts.append(syn.why_it_matters)
    parts.append("")

    # 3) Evidence
    parts.append("## 3) Evidence")
    for claim in syn.evidence:
        parts.append(f"- {claim.claim} — {claim.source}")
    parts.append("")

    # 4) Strongest Unresolved Uncertainty
    parts.append("## 4) Strongest Unresolved Uncertainty")
    parts.append(syn.strongest_uncertainty or "No major unresolved uncertainty beyond normal implementation risk.")
    parts.append("")

    # 5) What You Must Verify Personally
    parts.append("## 5) What You Must Verify Personally")
    for i, step in enumerate(syn.verification_steps, 1):
        parts.append(f"{i}. {step}")
    parts.append("")

    parts.append("---")
    parts.append("")

    # Suggested Next Move
    parts.append("## Suggested Next Move")
    parts.append(syn.suggested_next_move)
    parts.append("")

    parts.append("---")
    parts.append("")

    # Diagnostics (collapsed)
    parts.append("<details>")
    parts.append("<summary>Diagnostics</summary>")
    parts.append("")

    # Panel Composition
    parts.append("### Panel Composition")
    if panel.specialist_output:
        parts.append(f"- Specialist: {panel.specialist_output.vault_id}")
    parts.append(f"- Devil's Advocate: {'present' if panel.da_output else 'absent'}")
    parts.append(f"- Synthesizer: Opus")
    parts.append("")

    # Source Notes
    parts.append("### Source Notes")
    parts.append(f"- Retrieved docs: {len(panel.retrieved_docs)}")
    parts.append(f"- Retrieval quality: {panel.retrieval_confidence.value}")
    parts.append("")

    # Disagreement Structure
    parts.append("### Disagreement Structure")
    if syn.ungrounded_challenges:
        for challenge in syn.ungrounded_challenges:
            parts.append(f"- Ungrounded DA challenge: {challenge}")
    else:
        parts.append("- No substantive disagreement.")
    parts.append("")

    # Citation Notes
    parts.append("### Citation Notes")
    for claim in syn.evidence:
        parts.append(f"- {claim.source} — {claim.claim[:80]}")
    parts.append("")

    # Panel Degradation
    parts.append("### Panel Degradation")
    if panel.panel_degraded:
        parts.append(f"- {panel.degradation_reason}")
    else:
        parts.append("- No panel degradation.")
    parts.append("")

    parts.append("</details>")

    return "\n".join(parts)


def format_status(
    unresolved: list[dict],
    staleness: list[dict],
    totals: dict,
) -> str:
    """Format the cadep status display."""
    lines = []
    lines.append("CADEP Status")
    lines.append("=" * 40)

    # Unresolved audits
    if unresolved:
        lines.append(f"\nUnresolved audits: {len(unresolved)}")
        for audit in unresolved:
            lines.append(f"  - {audit['query_id']}: {audit.get('proposal_title', 'untitled')}")
    else:
        lines.append("\nNo unresolved audits.")

    # Staleness warnings
    if staleness:
        lines.append("\nStaleness warnings:")
        for w in staleness:
            lines.append(f"  ⚠️  {w['query_id']}: {w['staleness']} ({w['hours_old']}h)")

    # Token totals
    lines.append(f"\nLifetime usage:")
    lines.append(f"  Tokens: {totals.get('total_tokens', 0):,}")
    lines.append(f"  Cost: ${totals.get('total_cost_usd', 0):.4f}")
    lines.append(f"  API calls: {totals.get('total_calls', 0)}")

    return "\n".join(lines)
