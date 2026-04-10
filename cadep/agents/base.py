"""Base agent with Anthropic SDK call and retry logic."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field

import anthropic

from cadep import config


@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    duration_seconds: float = 0.0

    @property
    def estimated_cost(self) -> float:
        input_cost = (self.input_tokens / 1000) * config.COST_PER_1K_INPUT.get(self.model, 0)
        output_cost = (self.output_tokens / 1000) * config.COST_PER_1K_OUTPUT.get(self.model, 0)
        return input_cost + output_cost


@dataclass
class AgentResult:
    text: str = ""
    usage: TokenUsage = field(default_factory=TokenUsage)
    success: bool = True
    error: str | None = None


class BaseAgent:
    """Base class for all CADEP agents. Handles SDK calls with retry."""

    def __init__(self, model: str, max_output_tokens: int, agent_name: str = "agent"):
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.agent_name = agent_name
        self._client: anthropic.AsyncAnthropic | None = None

    @property
    def client(self) -> anthropic.AsyncAnthropic:
        if self._client is None:
            self._client = anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
        return self._client

    async def call(self, system: str, user: str) -> AgentResult:
        """Make an SDK call with exponential backoff retry."""
        last_error = None
        for attempt in range(config.SDK_MAX_RETRIES):
            try:
                start = time.monotonic()
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_output_tokens,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                duration = time.monotonic() - start

                text = ""
                for block in response.content:
                    if block.type == "text":
                        text += block.text

                usage = TokenUsage(
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                    model=self.model,
                    duration_seconds=duration,
                )
                return AgentResult(text=text, usage=usage)

            except anthropic.APIStatusError as e:
                last_error = str(e)
                if e.status_code < 500:
                    # 4xx — don't retry
                    return AgentResult(success=False, error=f"{self.agent_name}: {e.status_code} {last_error}")
                # 5xx — retry with backoff
                if attempt < config.SDK_MAX_RETRIES - 1:
                    delay = config.SDK_RETRY_BASE_DELAY * (2 ** attempt)
                    await asyncio.sleep(delay)

            except (anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                last_error = str(e)
                if attempt < config.SDK_MAX_RETRIES - 1:
                    delay = config.SDK_RETRY_BASE_DELAY * (2 ** attempt)
                    await asyncio.sleep(delay)

        return AgentResult(success=False, error=f"{self.agent_name}: failed after {config.SDK_MAX_RETRIES} retries — {last_error}")
