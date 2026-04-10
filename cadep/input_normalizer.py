"""Three-tier input intake — PRD Section 3."""

from __future__ import annotations

import json

import yaml

from cadep import config
from cadep.agents.base import BaseAgent
from cadep.models import FormalInput, InputQuality, NormalizedInput
from cadep.prompts import INPUT_NORMALIZER


class InputNormalizer:
    """Normalizes raw user input into a structured proposal."""

    def __init__(self):
        self._agent = BaseAgent(
            model=config.MODEL_NORMALIZER,
            max_output_tokens=config.NORMALIZER_MAX_OUTPUT_TOKENS,
            agent_name="normalizer",
        )

    async def normalize(self, raw_input: str) -> tuple[NormalizedInput, dict]:
        """Normalize input. Returns (normalized_input, token_usage_dict).

        Tries formal YAML parse first, then falls back to LLM normalization.
        """
        # Try formal schema first
        formal = self._try_formal_parse(raw_input)
        if formal is not None:
            normalized = NormalizedInput(
                raw_input=raw_input,
                normalized_problem_statement=formal.problem_statement,
                normalized_proposed_approach=formal.proposed_approach,
                inferred_constraints=[formal.constraints] if formal.constraints else [],
                inferred_stakes=formal.stakes or "unknown",
                inferred_prior_art=[formal.prior_art] if formal.prior_art else [],
                input_quality=InputQuality.FORMAL,
                domain_hint=formal.domain_hint,
                key_assumptions=formal.key_assumptions,
            )
            return normalized, {}

        # LLM normalization for messy input
        return await self._llm_normalize(raw_input)

    def _try_formal_parse(self, raw_input: str) -> FormalInput | None:
        """Attempt to parse input as YAML formal schema."""
        try:
            data = yaml.safe_load(raw_input)
            if isinstance(data, dict) and "problem_statement" in data and "proposed_approach" in data:
                return FormalInput(**data)
        except (yaml.YAMLError, TypeError, ValueError):
            pass
        return None

    async def _llm_normalize(self, raw_input: str) -> tuple[NormalizedInput, dict]:
        """Use Haiku to normalize messy input."""
        prompt = INPUT_NORMALIZER.format(raw_input=raw_input)
        result = await self._agent.call("You are an input parser.", prompt)

        usage = {
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "model": result.usage.model,
            "cost": result.usage.estimated_cost,
        }

        if not result.success:
            # Fallback: treat as underspecified
            return NormalizedInput(
                raw_input=raw_input,
                normalized_problem_statement="",
                normalized_proposed_approach="",
                input_quality=InputQuality.UNDERSPECIFIED,
                clarification_asked=True,
                clarification_reason="Normalization failed. Please provide more detail.",
            ), usage

        parsed = self._parse_normalizer_response(result.text, raw_input)
        return parsed, usage

    def _parse_normalizer_response(self, text: str, raw_input: str) -> NormalizedInput:
        """Parse the JSON response from the normalizer LLM."""
        try:
            # Extract JSON from response (may have surrounding text)
            start = text.index("{")
            end = text.rindex("}") + 1
            data = json.loads(text[start:end])
        except (ValueError, json.JSONDecodeError):
            return NormalizedInput(
                raw_input=raw_input,
                normalized_problem_statement="",
                normalized_proposed_approach="",
                input_quality=InputQuality.UNDERSPECIFIED,
                clarification_asked=True,
                clarification_reason="Could not parse input. Please rephrase.",
            )

        quality = data.get("input_quality", "messy-but-runnable")
        try:
            input_quality = InputQuality(quality)
        except ValueError:
            input_quality = InputQuality.MESSY_BUT_RUNNABLE

        clarification_needed = data.get("clarification_needed", False)

        return NormalizedInput(
            raw_input=raw_input,
            normalized_problem_statement=data.get("normalized_problem_statement", ""),
            normalized_proposed_approach=data.get("normalized_proposed_approach", ""),
            inferred_constraints=data.get("inferred_constraints", []),
            inferred_stakes=data.get("inferred_stakes", "unknown"),
            inferred_prior_art=data.get("inferred_prior_art", []),
            input_quality=input_quality,
            clarification_asked=clarification_needed,
            clarification_reason=data.get("clarification_question"),
        )
