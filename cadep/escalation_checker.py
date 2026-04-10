"""Critical signal detection for fast-path escalation (PRD Section 7.2)."""

from __future__ import annotations

import re

# Critical-severity language patterns
CRITICAL_PATTERNS = [
    r"\bcritical\b",
    r"\bfundamentally\s+(?:flawed|broken|wrong|invalid)\b",
    r"\bcannot\s+(?:work|succeed|be\s+valid)\b",
    r"\bfails?\s+(?:catastrophically|entirely|completely)\b",
    r"\birrecoverable\b",
    r"\bdata\s+loss\b",
    r"\bsafety\s+(?:risk|hazard|violation)\b",
    r"\bsevere\s+(?:bias|error|flaw)\b",
    r"\bmathematically\s+(?:invalid|impossible|undefined)\b",
    r"\bviolates?\s+(?:assumption|condition|requirement)\b",
]


def check_escalation(text: str) -> bool:
    """Check if fast-path output contains critical-severity signals.

    Returns True if escalation to full audit should be suggested.
    """
    for pattern in CRITICAL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
