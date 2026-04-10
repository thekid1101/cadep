"""Domain classification — Haiku-based vault routing."""

from __future__ import annotations

from pathlib import Path

from cadep import config
from cadep.agents.base import BaseAgent
from cadep.models import NormalizedInput, RetrievalConfidence
from cadep.prompts import DOMAIN_CLASSIFIER


class DomainClassifier:
    """Classifies proposals into vault domains using Haiku."""

    def __init__(self):
        self._agent = BaseAgent(
            model=config.MODEL_CLASSIFIER,
            max_output_tokens=config.CLASSIFIER_MAX_OUTPUT_TOKENS,
            agent_name="classifier",
        )

    def get_available_vaults(self) -> list[dict]:
        """Discover available vaults from the vault directory."""
        vaults = []
        vault_dir = config.VAULT_DIR
        if not vault_dir.exists():
            return vaults
        for vault_path in vault_dir.iterdir():
            if vault_path.is_dir():
                scope_file = vault_path / "vault_scope.md"
                scope = ""
                if scope_file.exists():
                    scope = scope_file.read_text(encoding="utf-8")[:500]
                vaults.append({
                    "vault_id": vault_path.name,
                    "scope": scope,
                })
        return vaults

    async def classify(self, proposal: NormalizedInput) -> tuple[str, RetrievalConfidence, dict]:
        """Classify proposal into a vault. Returns (vault_id, confidence, usage)."""
        # If domain hint provided, use it directly
        if proposal.domain_hint:
            vaults = self.get_available_vaults()
            vault_ids = [v["vault_id"] for v in vaults]
            if proposal.domain_hint in vault_ids:
                return proposal.domain_hint, RetrievalConfidence.HIGH, {}

        vaults = self.get_available_vaults()
        if not vaults:
            return "", RetrievalConfidence.LOW, {}

        if len(vaults) == 1:
            # Only one vault — skip LLM call
            return vaults[0]["vault_id"], RetrievalConfidence.HIGH, {}

        vault_list = "\n".join(
            f"- {v['vault_id']}: {v['scope'][:200]}" for v in vaults
        )
        proposal_text = (
            f"{proposal.normalized_problem_statement}\n"
            f"{proposal.normalized_proposed_approach}"
        )
        prompt = DOMAIN_CLASSIFIER.format(
            vault_list=vault_list,
            proposal=proposal_text,
        )

        result = await self._agent.call(
            "You are a domain classifier. Return only the vault ID and confidence.",
            prompt,
        )

        usage = {
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "model": result.usage.model,
            "cost": result.usage.estimated_cost,
        }

        if not result.success:
            return vaults[0]["vault_id"], RetrievalConfidence.LOW, usage

        vault_id, confidence = self._parse_classification(result.text, vaults)
        return vault_id, confidence, usage

    def _parse_classification(
        self, text: str, vaults: list[dict]
    ) -> tuple[str, RetrievalConfidence]:
        vault_ids = [v["vault_id"] for v in vaults]
        lines = text.strip().splitlines()

        vault_id = vaults[0]["vault_id"]  # default
        confidence = RetrievalConfidence.LOW

        for line in lines:
            line_upper = line.strip().upper()
            if line_upper.startswith("VAULT:"):
                parsed_id = line.split(":", 1)[1].strip()
                if parsed_id in vault_ids:
                    vault_id = parsed_id
            elif line_upper.startswith("CONFIDENCE:"):
                conf_str = line.split(":", 1)[1].strip().upper()
                if conf_str in ("HIGH", "MEDIUM", "LOW"):
                    confidence = RetrievalConfidence(conf_str)

        return vault_id, confidence
