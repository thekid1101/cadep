"""Generative friction mechanism — context-specific verification questions (PRD Section 8.4)."""

from __future__ import annotations

from cadep import config
from cadep.agents.base import BaseAgent
from cadep.models import (
    DevilsAdvocateOutput,
    PanelResult,
    RetrievalConfidence,
    SpecialistOutput,
    SynthesizerOutput,
)
from cadep.prompts import FRICTION_GENERATOR


class FrictionGenerator:
    """Generates context-specific verification questions after full-audit panels."""

    def __init__(self):
        self._agent = BaseAgent(
            model=config.MODEL_FRICTION,
            max_output_tokens=config.FRICTION_MAX_OUTPUT_TOKENS,
            agent_name="friction",
        )

    async def generate(self, panel_result: PanelResult) -> tuple[str, dict]:
        """Generate a friction question. Returns (question, usage)."""
        summary = self._build_panel_summary(panel_result)
        prompt = FRICTION_GENERATOR.format(panel_summary=summary)

        result = await self._agent.call(
            "You generate verification questions that force genuine engagement.",
            prompt,
        )

        usage = {
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "model": result.usage.model,
            "cost": result.usage.estimated_cost,
        }

        if result.success:
            return result.text.strip(), usage
        return self._fallback_question(panel_result), usage

    def _build_panel_summary(self, pr: PanelResult) -> str:
        parts = []

        if pr.specialist_output:
            spec = pr.specialist_output
            if spec.critical_issues:
                issues = "; ".join(i.description[:100] for i in spec.critical_issues[:3])
                parts.append(f"Specialist critical issues: {issues}")
            if spec.validated:
                parts.append(f"Specialist validated: {'; '.join(spec.validated[:2])}")

        if pr.da_output:
            da = pr.da_output
            attacks = da.assumption_attacks + da.transfer_risks + da.practical_failure_modes
            if attacks:
                attack_strs = [f"[{a.dimension}] {a.description[:80]}" for a in attacks[:3]]
                parts.append(f"Devil's Advocate attacks: {'; '.join(attack_strs)}")

        if pr.synthesizer_output:
            syn = pr.synthesizer_output
            parts.append(f"Synthesizer failure point: {syn.likely_failure_point[:150]}")
            if syn.strongest_uncertainty:
                parts.append(f"Strongest uncertainty: {syn.strongest_uncertainty[:100]}")
            if syn.ungrounded_challenges:
                parts.append(f"Ungrounded challenges: {'; '.join(syn.ungrounded_challenges[:2])}")

        parts.append(f"Retrieval confidence: {pr.retrieval_confidence.value}")

        return "\n".join(parts)

    def _fallback_question(self, pr: PanelResult) -> str:
        """Generate a basic friction question without LLM if the call fails."""
        if pr.synthesizer_output and pr.synthesizer_output.verification_steps:
            step = pr.synthesizer_output.verification_steps[0]
            return (
                f"The panel recommended this verification step: \"{step}\". "
                f"Describe specifically how you will perform this check "
                f"and what result would change your decision."
            )
        return (
            "Describe the specific verification you will perform before "
            "acting on this panel output, and what finding would change your decision."
        )

    @staticmethod
    def validate_answer(answer: str) -> bool:
        """Check friction answer meets minimum engagement threshold."""
        word_count = len(answer.split())
        return word_count >= config.FRICTION_MIN_ANSWER_WORDS
