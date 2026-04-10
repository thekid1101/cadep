"""Synthesizer agent — constrained meta-critic (most consequential agent)."""

from __future__ import annotations

from cadep import config
from cadep.agents.base import AgentResult, BaseAgent
from cadep.models import CompressedPanelInput, PanelMode
from cadep.prompts import SYNTHESIZER_FAST, SYNTHESIZER_FULL


class SynthesizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            model=config.MODEL_SYNTHESIZER,
            max_output_tokens=config.SYNTHESIZER_MAX_OUTPUT_TOKENS,
            agent_name="synthesizer",
        )

    async def run(
        self,
        compressed_input: CompressedPanelInput,
        mode: PanelMode = PanelMode.FAST,
    ) -> AgentResult:
        system_prompt = SYNTHESIZER_FULL if mode == PanelMode.FULL else SYNTHESIZER_FAST

        user_message = self._build_user_message(compressed_input)
        return await self.call(system_prompt, user_message)

    def _build_user_message(self, ci: CompressedPanelInput) -> str:
        parts = []

        if ci.user_constraints:
            parts.append(
                f"## User Constraints & Key Assumptions\n"
                f"(Passed verbatim — never summarized)\n\n"
                f"{ci.user_constraints}"
            )

        if ci.critical_issues_text:
            parts.append(
                f"## Critical Issues from Specialists\n\n"
                f"{ci.critical_issues_text}"
            )

        if ci.conflicts_text:
            parts.append(
                f"## Conflicts Between Panel Members\n\n"
                f"{ci.conflicts_text}"
            )

        if ci.retrieval_metadata:
            meta_lines = [f"- {k}: {v}" for k, v in ci.retrieval_metadata.items()]
            parts.append(
                f"## Retrieval Metadata\n\n" + "\n".join(meta_lines)
            )

        if ci.devils_advocate_text:
            parts.append(
                f"## Devil's Advocate Output\n\n"
                f"{ci.devils_advocate_text}"
            )

        if ci.validated_premise:
            parts.append(
                f"## Validated Core Premise\n"
                f"(What is sound about the proposal — needed to contextualize objections)\n\n"
                f"{ci.validated_premise}"
            )

        if ci.improvements_text:
            parts.append(
                f"## Improvements (summarized)\n\n"
                f"{ci.improvements_text}"
            )

        if ci.overflow_actions:
            parts.append(
                f"## Token Budget Notes\n\n"
                + "\n".join(f"- {a}" for a in ci.overflow_actions)
            )

        return "\n\n---\n\n".join(parts)
