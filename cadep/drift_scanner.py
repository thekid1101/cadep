"""Fast-path drift scanner — regex enforcement of output contract (PRD Section 7.2)."""

from __future__ import annotations

import re

from cadep.prompts import DRIFT_WARNING, NUMERIC_UNSOURCED_WARNING

# Recommendation language patterns — the fast path must NOT recommend methods
RECOMMENDATION_PATTERNS = [
    r"\buse\s+\w+\s+instead\b",
    r"\bthe\s+correct\s+approach\s+is\b",
    r"\byou\s+should\s+(?:use|switch|adopt|implement)\b",
    r"\brecommend\s+(?:using|switching|adopting)\b",
    r"\bbetter\s+(?:approach|method|technique|alternative)\s+(?:is|would be)\b",
    r"\bswitch\s+to\b",
    r"\badopt\b.*\binstead\b",
    r"\breplace\s+(?:with|by)\b",
]

# Provenance tag patterns for numeric claims
UNSOURCED_NUMERIC = re.compile(r"\[unsourced\]")
SOURCED_NUMERIC = re.compile(r"\[(user-input|vault:\s*\S+)\]")
# Bare numbers that might be unsourced claims (not years, not simple counts)
BARE_NUMERIC = re.compile(
    r"(?<!\d)(?:~?\d+(?:\.\d+)?%|~?\d+(?:\.\d+)?x|~?[\d,]+(?:\.\d+)?)\b"
    r"(?!\s*(?:papers?|docs?|documents?|items?|steps?|bullets?|sections?))"
)


def scan_fast_path(text: str) -> list[str]:
    """Scan fast-path output for drift violations. Returns list of warnings."""
    warnings = []

    # Check for recommendation language
    for pattern in RECOMMENDATION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            warnings.append(DRIFT_WARNING)
            break

    # Check for unsourced numeric claims via provenance tags
    if UNSOURCED_NUMERIC.search(text):
        warnings.append(NUMERIC_UNSOURCED_WARNING)

    return warnings


def parse_fast_path_fields(raw_text: str) -> dict[str, str]:
    """Parse synthesizer fast-path output into exactly three fields.

    Returns dict with keys: likely_failure_point, untested_assumption, check_next.
    Any content not mapping to these fields is stripped (PRD Section 7.2).
    """
    fields = {
        "likely_failure_point": "",
        "untested_assumption": "",
        "check_next": "",
    }

    # Try structured parsing first (FIELD_NAME: content)
    patterns = {
        "likely_failure_point": r"LIKELY_FAILURE_POINT:\s*(.*?)(?=UNTESTED_ASSUMPTION:|CHECK_NEXT:|$)",
        "untested_assumption": r"UNTESTED_ASSUMPTION:\s*(.*?)(?=CHECK_NEXT:|$)",
        "check_next": r"CHECK_NEXT:\s*(.*?)$",
    }

    for field_name, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.DOTALL | re.IGNORECASE)
        if match:
            fields[field_name] = match.group(1).strip()

    # Fallback: try numbered section parsing (1. 2. 3.)
    if not any(fields.values()):
        sections = re.split(r"\n\s*(?:\d+[\.\)]\s*)", raw_text)
        section_keys = ["likely_failure_point", "untested_assumption", "check_next"]
        for i, key in enumerate(section_keys):
            if i + 1 < len(sections):
                fields[key] = sections[i + 1].strip()

    # Strip provenance tags from display (but warnings already captured)
    for key in fields:
        fields[key] = re.sub(r"\s*\[(user-input|vault:\s*\S+|unsourced)\]", "", fields[key])

    return fields


def strip_recommendation_language(text: str) -> str:
    """Remove recommendation sentences from fast-path output."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    filtered = []
    for sentence in sentences:
        is_recommendation = False
        for pattern in RECOMMENDATION_PATTERNS:
            if re.search(pattern, sentence, re.IGNORECASE):
                is_recommendation = True
                break
        if not is_recommendation:
            filtered.append(sentence)
    return " ".join(filtered)
