"""Pydantic models for all CADEP data structures."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --- Enums --------------------------------------------------------------------

class InputQuality(str, Enum):
    FORMAL = "formal"
    MESSY_BUT_RUNNABLE = "messy-but-runnable"
    AMBIGUOUS = "ambiguous"
    UNDERSPECIFIED = "underspecified"


class PanelMode(str, Enum):
    FAST = "fast"
    FULL = "full"


class RetrievalConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MathSyntaxStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    PARSE_FAILED = "parse-failed"
    NO_MATH = "no-math"


class CoverageQuality(str, Enum):
    FULL = "full"
    ABSTRACT_ONLY = "abstract-only"
    PARTIAL = "partial"


class Decision(str, Enum):
    ACCEPT = "accept"
    OVERRIDE = "override"
    REJECT = "reject"


class VerificationBasis(str, Enum):
    CHECKED_CITED_SOURCE = "checked_cited_source"
    CHECKED_IMPLEMENTATION_CONSTRAINT = "checked_implementation_constraint"
    FOUND_CONTRADICTORY_EVIDENCE = "found_contradictory_evidence"
    VALIDATED_APPLICABILITY_CONDITION = "validated_applicability_condition"
    NOT_VERIFIED = "not_verified"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ProvenanceTag(str, Enum):
    USER_INPUT = "user-input"
    VAULT = "vault"
    UNSOURCED = "unsourced"


# --- Input models -------------------------------------------------------------

class NormalizedInput(BaseModel):
    raw_input: str
    normalized_problem_statement: str
    normalized_proposed_approach: str
    inferred_constraints: list[str] = Field(default_factory=list)
    inferred_stakes: str = "unknown"
    inferred_prior_art: list[str] = Field(default_factory=list)
    input_quality: InputQuality
    clarification_asked: bool = False
    clarification_reason: Optional[str] = None
    domain_hint: Optional[str] = None
    key_assumptions: Optional[str] = None


class FormalInput(BaseModel):
    problem_statement: str
    proposed_approach: str
    key_assumptions: Optional[str] = None
    constraints: Optional[str] = None
    domain_hint: Optional[str] = None
    prior_art: Optional[str] = None
    stakes: Optional[str] = None


# --- Vault models -------------------------------------------------------------

class VaultDocument(BaseModel):
    doc_id: str
    title: str
    authors: list[str]
    year: int
    citation_count: int = 0
    source_url: Optional[str] = None
    concept_tags: list[str] = Field(default_factory=list)
    superseded_by: Optional[str] = None
    coverage_quality: CoverageQuality = CoverageQuality.ABSTRACT_ONLY
    math_syntax_status: MathSyntaxStatus = MathSyntaxStatus.NO_MATH
    cadep_citation_count: int = 0
    last_verified: Optional[str] = None
    slot_justification: str = ""
    content: str = ""  # Full document content for retrieval


# --- Agent output models ------------------------------------------------------

class CitedClaim(BaseModel):
    claim: str
    source: str
    doc_id: Optional[str] = None
    provenance: ProvenanceTag = ProvenanceTag.VAULT


class SpecialistIssue(BaseModel):
    description: str
    severity: Severity = Severity.MEDIUM
    citations: list[CitedClaim] = Field(default_factory=list)
    condition: Optional[str] = None


class SpecialistOutput(BaseModel):
    vault_id: str
    critical_issues: list[SpecialistIssue] = Field(default_factory=list)
    improvements: list[SpecialistIssue] = Field(default_factory=list)
    validated: list[str] = Field(default_factory=list)
    unknown: list[str] = Field(default_factory=list)
    raw_text: str = ""


class DAAttack(BaseModel):
    description: str
    dimension: str  # transfer_risk | hidden_assumption | operational_failure | incentive_misalignment
    falsifiable_condition: Optional[str] = None


class DevilsAdvocateOutput(BaseModel):
    assumption_attacks: list[DAAttack] = Field(default_factory=list)
    transfer_risks: list[DAAttack] = Field(default_factory=list)
    practical_failure_modes: list[DAAttack] = Field(default_factory=list)
    raw_text: str = ""


class SynthesizerOutput(BaseModel):
    likely_failure_point: str
    second_blocker: Optional[str] = None
    why_it_matters: str
    evidence: list[CitedClaim] = Field(default_factory=list)
    strongest_uncertainty: str
    verification_steps: list[str] = Field(default_factory=list)
    suggested_next_move: str
    ungrounded_challenges: list[str] = Field(default_factory=list)
    raw_text: str = ""


class FastPathOutput(BaseModel):
    likely_failure_point: str
    untested_assumption: str
    check_next: str
    drift_warnings: list[str] = Field(default_factory=list)
    escalation_triggered: bool = False


# --- Retrieval models ---------------------------------------------------------

class RetrievalResult(BaseModel):
    doc_id: str
    score: float = 0.0
    method: str = "concept_index"  # concept_index | tfidf


class RetrievalBundle(BaseModel):
    results: list[RetrievalResult] = Field(default_factory=list)
    confidence: RetrievalConfidence = RetrievalConfidence.LOW
    concept_tags_matched: list[str] = Field(default_factory=list)
    tfidf_triggered: bool = False


# --- Compressed synthesizer input ---------------------------------------------

class CompressedPanelInput(BaseModel):
    system_prompt_tokens: int = 0
    user_constraints: str = ""
    critical_issues_text: str = ""
    conflicts_text: str = ""
    retrieval_metadata: dict = Field(default_factory=dict)
    devils_advocate_text: str = ""
    validated_premise: str = ""
    improvements_text: str = ""
    total_estimated_tokens: int = 0
    overflow_actions: list[str] = Field(default_factory=list)


# --- Panel execution ----------------------------------------------------------

class PanelConfig(BaseModel):
    specialist_vault: str
    devils_advocate: bool = True
    synthesizer: bool = True
    mode: PanelMode = PanelMode.FAST


class PanelResult(BaseModel):
    query_id: str
    mode: PanelMode
    specialist_output: Optional[SpecialistOutput] = None
    da_output: Optional[DevilsAdvocateOutput] = None
    synthesizer_output: Optional[SynthesizerOutput] = None
    fast_path_output: Optional[FastPathOutput] = None
    panel_degraded: bool = False
    degradation_reason: Optional[str] = None
    retrieved_docs: list[str] = Field(default_factory=list)
    retrieval_confidence: RetrievalConfidence = RetrievalConfidence.LOW
    runtime_seconds: float = 0.0
    total_tokens: int = 0
    estimated_cost: float = 0.0


# --- Audit log models (PRD Section 10, Phase 0) ------------------------------

class SubmissionRecord(BaseModel):
    query_id: str
    date: str
    mode: str
    input_quality: str
    proposal_title: str


class ExecutionRecord(BaseModel):
    query_id: str
    panel_config: dict
    retrieved_docs: list[str]
    panel_degraded: bool
    runtime_seconds: float
    token_cost_estimate: float


class ComparisonRecord(BaseModel):
    query_id: str
    baseline_run: bool = False
    baseline_review_time_seconds: Optional[int] = None
    cadep_review_time_seconds: Optional[int] = None
    severity_weighted_score_baseline: Optional[int] = None
    severity_weighted_score_cadep: Optional[int] = None
    directional_winner: Optional[str] = None
    did_cadep_surface_baseline_miss: Optional[bool] = None
    baseline_miss_summary: Optional[str] = None


class ImpactRecord(BaseModel):
    query_id: str
    decision_changed_by_cadep: Optional[bool] = None
    next_action_changed: Optional[bool] = None
    confirmed_real_within_review: Optional[bool] = None
    verification_basis: Optional[VerificationBasis] = None
    operator_notes: Optional[str] = None


class ResolveRecord(BaseModel):
    query_id: str
    decision: Decision
    override_category: Optional[str] = None
    reasoning: Optional[str] = None
    review_time_seconds: Optional[int] = None
    friction_response_saved: bool = False
    verification_basis: Optional[VerificationBasis] = None


class FrictionAnswer(BaseModel):
    query_id: str
    date: str
    question: str
    answer: str
    answer_word_count: int
