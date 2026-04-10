"""Devil's Advocate agent — constrained first-principles attack."""

from __future__ import annotations

from cadep import config
from cadep.agents.base import AgentResult, BaseAgent
from cadep.models import NormalizedInput
from cadep.prompts import DEVILS_ADVOCATE


class DevilsAdvocateAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            model=config.MODEL_DEVILS_ADVOCATE,
            max_output_tokens=config.DA_MAX_OUTPUT_TOKENS,
            agent_name="devils_advocate",
        )

    async def run(self, proposal: NormalizedInput) -> AgentResult:
        user_message = (
            f"## Proposal Under Review\n\n"
            f"**Problem**: {proposal.normalized_problem_statement}\n\n"
            f"**Proposed Approach**: {proposal.normalized_proposed_approach}\n\n"
        )
        if proposal.key_assumptions:
            user_message += f"**Key Assumptions**: {proposal.key_assumptions}\n\n"
        if proposal.inferred_constraints:
            user_message += f"**Constraints**: {'; '.join(proposal.inferred_constraints)}\n\n"
        if proposal.inferred_stakes != "unknown":
            user_message += f"**Stakes**: {proposal.inferred_stakes}\n\n"

        return await self.call(DEVILS_ADVOCATE, user_message)
