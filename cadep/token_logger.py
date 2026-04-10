"""Token and cost tracking — logs every SDK call from day one (PRD Section 4.2)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from cadep import config
from cadep.agents.base import TokenUsage


class TokenLogger:
    """Append-only JSONL log tracking every SDK call's token usage and cost."""

    def __init__(self):
        self.log_path = config.AUDIT_LOGS_DIR / "token_usage.jsonl"
        self._session_tokens = 0
        self._session_cost = 0.0
        self._call_count = 0

    def log(self, usage: TokenUsage, agent_name: str, query_id: str = "") -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_id": query_id,
            "agent": agent_name,
            "model": usage.model,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "total_tokens": usage.input_tokens + usage.output_tokens,
            "estimated_cost_usd": round(usage.estimated_cost, 6),
            "duration_seconds": round(usage.duration_seconds, 2),
        }

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        self._session_tokens += usage.input_tokens + usage.output_tokens
        self._session_cost += usage.estimated_cost
        self._call_count += 1

    @property
    def session_tokens(self) -> int:
        return self._session_tokens

    @property
    def session_cost(self) -> float:
        return self._session_cost

    @property
    def call_count(self) -> int:
        return self._call_count

    def get_totals(self) -> dict:
        """Read the full log and compute lifetime totals."""
        if not self.log_path.exists():
            return {"total_tokens": 0, "total_cost_usd": 0.0, "total_calls": 0}

        total_tokens = 0
        total_cost = 0.0
        total_calls = 0

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                total_tokens += record.get("total_tokens", 0)
                total_cost += record.get("estimated_cost_usd", 0)
                total_calls += 1

        return {
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "total_calls": total_calls,
        }
