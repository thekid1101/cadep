"""Specialist agent — grounded critique from curated literature."""

from __future__ import annotations

from cadep import config
from cadep.agents.base import AgentResult, BaseAgent
from cadep.models import NormalizedInput, PanelMode, VaultDocument
from cadep.prompts import SPECIALIST_FAST, SPECIALIST_FULL


class SpecialistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            model=config.MODEL_SPECIALIST,
            max_output_tokens=config.SPECIALIST_MAX_OUTPUT_TOKENS,
            agent_name="specialist",
        )

    async def run(
        self,
        proposal: NormalizedInput,
        documents: list[VaultDocument],
        vault_id: str,
        mode: PanelMode = PanelMode.FAST,
    ) -> AgentResult:
        domain_name = vault_id.replace("-", " ").title()
        template = SPECIALIST_FULL if mode == PanelMode.FULL else SPECIALIST_FAST

        system_prompt = template.format(
            domain_name=domain_name,
            domain=domain_name,
        )

        docs_context = self._format_documents(documents)

        user_message = (
            f"## Proposal\n\n"
            f"**Problem**: {proposal.normalized_problem_statement}\n\n"
            f"**Proposed Approach**: {proposal.normalized_proposed_approach}\n\n"
        )
        if proposal.key_assumptions:
            user_message += f"**Key Assumptions**: {proposal.key_assumptions}\n\n"
        if proposal.inferred_constraints:
            user_message += f"**Constraints**: {'; '.join(proposal.inferred_constraints)}\n\n"

        user_message += f"## Available Documents\n\n{docs_context}"

        return await self.call(system_prompt, user_message)

    def _format_documents(self, documents: list[VaultDocument]) -> str:
        parts = []
        for doc in documents:
            header = f"### {doc.doc_id}: {doc.title}\n"
            header += f"**Authors**: {', '.join(doc.authors)} ({doc.year})\n"
            header += f"**Citations**: {doc.citation_count}\n"
            header += f"**Coverage**: {doc.coverage_quality.value}\n"
            header += f"**Math status**: {doc.math_syntax_status.value}\n"
            header += f"**Tags**: {', '.join(doc.concept_tags)}\n\n"
            if doc.content:
                header += doc.content + "\n"
            parts.append(header)
        return "\n---\n".join(parts)
