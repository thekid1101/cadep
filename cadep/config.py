"""CADEP configuration — paths, model names, token budgets, retry settings."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --- Paths -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VAULT_DIR = PROJECT_ROOT / "vault"
AUDIT_DIR = PROJECT_ROOT / "audit"
AUDIT_LOGS_DIR = AUDIT_DIR / "logs"
PANEL_OUTPUTS_DIR = AUDIT_DIR / "panel_outputs"

# Ensure runtime dirs exist
AUDIT_LOGS_DIR.mkdir(parents=True, exist_ok=True)
PANEL_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Anthropic SDK ------------------------------------------------------------

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Model routing per PRD Section 4.1
MODEL_HAIKU = "claude-haiku-4-5-20251001"
MODEL_SONNET = "claude-sonnet-4-6-20250514"
MODEL_OPUS = "claude-opus-4-6-20250514"

MODEL_CLASSIFIER = MODEL_HAIKU
MODEL_NORMALIZER = MODEL_HAIKU
MODEL_FRICTION = MODEL_HAIKU
MODEL_SPECIALIST = MODEL_SONNET
MODEL_DEVILS_ADVOCATE = MODEL_SONNET
MODEL_SYNTHESIZER = MODEL_OPUS
MODEL_CURATOR = MODEL_SONNET

# --- Token budgets (PRD Section 6.4) -----------------------------------------

SYNTHESIZER_MAX_INPUT_TOKENS = 8_000
SYNTHESIZER_BUDGET = {
    "system_prompt": 1_500,
    "user_constraints": 500,
    "critical_issues": 2_000,
    "conflicts": 2_000,
    "retrieval_metadata": 200,
    "devils_advocate": 1_000,
    "validated_premise": 100,
    "improvements": 800,
}

SPECIALIST_MAX_OUTPUT_TOKENS = 2_000
DA_MAX_OUTPUT_TOKENS = 1_500
SYNTHESIZER_MAX_OUTPUT_TOKENS = 2_000
CLASSIFIER_MAX_OUTPUT_TOKENS = 200
NORMALIZER_MAX_OUTPUT_TOKENS = 500
FRICTION_MAX_OUTPUT_TOKENS = 300

# --- Retry settings (PRD Section 5.1) ----------------------------------------

SDK_MAX_RETRIES = 3
SDK_RETRY_BASE_DELAY = 2.0  # seconds, exponential backoff

API_MAX_RETRIES = 3
API_RETRY_BASE_DELAY = 2.0
API_TIMEOUT = 10  # seconds

# --- Cost estimates (PRD Section 4.2) ----------------------------------------

COST_PER_1K_INPUT = {
    MODEL_HAIKU: 0.001,
    MODEL_SONNET: 0.003,
    MODEL_OPUS: 0.015,
}
COST_PER_1K_OUTPUT = {
    MODEL_HAIKU: 0.005,
    MODEL_SONNET: 0.015,
    MODEL_OPUS: 0.075,
}

# --- Vault settings -----------------------------------------------------------

VAULT_MAX_DOCS = 25
CURATOR_MAX_PAPERS_PER_MONTH = 2

# --- Audit settings (PRD Section 8.5) ----------------------------------------

STALENESS_WARNING_HOURS = 48
STALENESS_ESCALATION_HOURS = 168  # 7 days
MAX_UNRESOLVED_AUDITS = 3  # Backlog >3 pauses new full-audit submissions

# --- Friction settings (PRD Section 8.4) -------------------------------------

FRICTION_MIN_ANSWER_WORDS = 15

# --- Retrieval settings (PRD Section 9.3) ------------------------------------

TFIDF_TOP_K = 5
TFIDF_MIN_SIMILARITY = 0.3
