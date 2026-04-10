"""Phase 0 audit trail — 5 log types (PRD Section 10)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from cadep import config
from cadep.models import (
    ComparisonRecord,
    ExecutionRecord,
    FrictionAnswer,
    ImpactRecord,
    ResolveRecord,
    SubmissionRecord,
)


class AuditLogger:
    """Append-only JSONL logging for the 5 Phase 0 log types."""

    def __init__(self):
        self.logs_dir = config.AUDIT_LOGS_DIR
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def _append(self, filename: str, record: dict) -> None:
        path = self.logs_dir / filename
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def _read_all(self, filename: str) -> list[dict]:
        path = self.logs_dir / filename
        if not path.exists():
            return []
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    # --- A. Submission record --------------------------------------------------

    def log_submission(self, record: SubmissionRecord) -> None:
        self._append("submissions.jsonl", record.model_dump())

    # --- B. Execution record ---------------------------------------------------

    def log_execution(self, record: ExecutionRecord) -> None:
        self._append("executions.jsonl", record.model_dump())

    # --- C. Comparison record --------------------------------------------------

    def log_comparison(self, record: ComparisonRecord) -> None:
        self._append("comparisons.jsonl", record.model_dump())

    # --- D. Immediate impact record --------------------------------------------

    def log_impact(self, record: ImpactRecord) -> None:
        self._append("impacts.jsonl", record.model_dump())

    # --- E. Resolve record (full audits only) ----------------------------------

    def log_resolve(self, record: ResolveRecord) -> None:
        self._append("resolves.jsonl", record.model_dump())

    # --- Friction answers ------------------------------------------------------

    def log_friction_answer(self, answer: FrictionAnswer) -> None:
        self._append("friction_answers.jsonl", answer.model_dump())

    # --- Queries ---------------------------------------------------------------

    def get_submissions(self) -> list[dict]:
        return self._read_all("submissions.jsonl")

    def get_unresolved_audits(self) -> list[dict]:
        """Find full-audit submissions that haven't been resolved."""
        submissions = [
            s for s in self._read_all("submissions.jsonl")
            if s.get("mode") == "full"
        ]
        resolved_ids = {
            r["query_id"] for r in self._read_all("resolves.jsonl")
        }
        deferred_ids = set()
        # Check for deferred audits
        defer_path = self.logs_dir / "deferred.jsonl"
        if defer_path.exists():
            deferred_ids = {
                r["query_id"]
                for r in self._read_all("deferred.jsonl")
            }

        return [
            s for s in submissions
            if s["query_id"] not in resolved_ids
            and s["query_id"] not in deferred_ids
        ]

    def log_defer(self, query_id: str, reason: str) -> None:
        self._append("deferred.jsonl", {
            "query_id": query_id,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "reason": reason,
        })

    def get_panel_output_path(self, query_id: str) -> Path:
        return config.PANEL_OUTPUTS_DIR / f"{query_id}.md"

    def save_panel_output(self, query_id: str, markdown: str) -> Path:
        path = self.get_panel_output_path(query_id)
        path.write_text(markdown, encoding="utf-8")
        return path

    def load_panel_output(self, query_id: str) -> str | None:
        path = self.get_panel_output_path(query_id)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None

    def get_staleness_warnings(self) -> list[dict]:
        """Check for stale unresolved audits."""
        unresolved = self.get_unresolved_audits()
        now = datetime.now(timezone.utc)
        warnings = []
        for audit in unresolved:
            date_str = audit.get("date", "")
            try:
                audit_date = datetime.fromisoformat(date_str)
                if audit_date.tzinfo is None:
                    audit_date = audit_date.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                continue
            hours_old = (now - audit_date).total_seconds() / 3600
            if hours_old > config.STALENESS_ESCALATION_HOURS:
                warnings.append({**audit, "staleness": "7-day", "hours_old": int(hours_old)})
            elif hours_old > config.STALENESS_WARNING_HOURS:
                warnings.append({**audit, "staleness": "48-hour", "hours_old": int(hours_old)})
        return warnings
