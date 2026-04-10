# CADEP Phase 0 Evaluation Contract

**Frozen**: April 10, 2026
**Status**: Binding — all thresholds predeclared before any test runs
**Author**: Johnathon Hoffman
**Reviewed by**: Project Manager (PRD v1.9 author), 2 review rounds

This document consolidates every predeclared threshold, pass criterion, and pre-commitment governing Phase 0 evaluation. It was written before any Phase 0 test data was collected. Thresholds may not be revised after seeing results. If a threshold is wrong, the correct response is to flag it as a design error and re-run with a corrected threshold — not to retroactively adjust the bar.

---

## 1. Test Set Design

### 1.1 Proposals

8 real proposals, stratified:
- 2 low-stakes
- 2 medium-stakes
- 2 high-stakes
- 2 boundary-case (at edge of vault scope)

At least 1 proposal must be portfolio-adjacent to activate portfolio optimization papers. At least 1 must be copula-specific. At least 1 must involve simulation methodology.

### 1.2 Baseline Protocol

Each proposal runs through:
- **CADEP Cowork skill** (prompt-simulated agent separation)
- **CADEP API version** (structural agent separation) — if available; otherwise deferred to Phase 0b
- **Single well-prompted Claude conversation** (baseline) receiving the same normalized proposal and the same vault documents

Baseline prompt: "Review this proposal. Identify flaws, cite specific papers from the provided documents, and recommend verification steps." One shot, no multi-turn refinement.

### 1.3 Blind Scoring Protocol

Outputs are scored blind where possible. Strip identifiers, randomize presentation order, score against the prewritten severity rubric. True blinding will be fragile (outputs are stylistically different). The real protection is the predeclared rubric and thresholds, not pseudo-blindness.

---

## 2. Severity Rubric

Predeclared before scoring. From PRD v1.9, unchanged.

| Tier | Definition | Points |
|------|-----------|--------|
| Tier 1: Decision-Changing | Flaw that should change whether to proceed | 3 |
| Tier 2: Implementation-Relevant | Changes how to proceed, not whether | 1 |
| Tier 3: Contextual Caveat | Technically correct, doesn't affect decision | 0 |

Severity-weighted score = (Tier 1 count × 3) + (Tier 2 count × 1)

---

## 3. Pass Criteria — Original (from PRD v1.9)

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| Severity-weighted flaw score | CADEP scores ≥40% higher than baseline | Blind-scored per severity rubric |
| Directional winner | CADEP outperforms on ≥6 of 8 proposals | Blind-scored |
| Citation verifiability | ≥80% of citations supported by vault paper text | Manual spot-check, top 2 citations per proposal (16 checks total) |
| Vulnerability identification | Synthesizer identifies most decision-relevant weakness on ≥5 of 8 | Scored against predeclared answer key (written before running panels) |
| Human review time | CADEP review time ≤2× baseline review time | Timed per proposal |

---

## 4. Pass Criteria — Cowork-Specific (new, predeclared)

These criteria measure whether the Cowork skill's prompt-based mechanisms hold without code enforcement.

### 4.1 Behavioral Compliance

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| Drift rate | Recommendation language in ≤10% of outputs | Count outputs containing "use X instead", "the correct approach is", "you should use/switch/adopt", "recommend using", "better approach/method is", "switch to", "replace with" |
| Vault citation compliance | ≥90% of citations reference actual vault papers | Count citations, verify each doc_id exists in vault/documents/ |
| Format compliance (fast path) | Exactly 3 fields in ≥90% of fast-path outputs | Check for LIKELY FAILURE POINT, UNTESTED ASSUMPTION, CHECK NEXT only — no extra sections |
| Provenance compliance (fast path) | ≤10% of fast-path outputs contain unsourced numeric claims | Check all numeric claims for [user-input] or [vault: doc_id] tags |
| Provenance compliance (full audit) | 0% tolerance | ANY unsourced numeric claim in a full-audit output is a critical failure |

### 4.2 Retrieval Quality

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| Citation clustering | ≥75% of citations per output come from papers in the query's primary concept domain | Map each citation to concept_index.json domains, count primary vs. non-primary |
| Untested papers | Papers not triggered by any of the 8 proposals flagged as "untested, provisionally included" | Track which vault papers are cited at least once across all 8 proposals |

### 4.3 Agent Separation (Prompt vs. Structural)

**Note**: This test requires running both the Cowork skill and the API version on the same proposals. If the API version is not yet operational, this test is deferred to Phase 0b but remains a binding requirement before the Cowork skill is considered validated.

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| DA independence — assumption coverage | Prompt-separated DA attacks assumptions the specialist didn't touch at a rate within 1 SD of structurally-separated DA | Blind rater scores each DA output on "does DA attack assumptions specialist didn't touch?" (1-5 scale) |
| DA independence — framing independence | Prompt-separated DA framing rated as independent (not derivative) at a rate within 1 SD of structurally-separated DA | Blind rater scores "does DA framing feel independent or derivative of specialist?" (1-5 scale) |
| DA anchoring check | Prompt-separated DA's objection vocabulary overlap with specialist output does not exceed structural DA's overlap by more than 15% | Count shared key terms between specialist and DA outputs |

**If prompt separation fails**: the Cowork skill is a convenience tool for personal use, not the product. The API version with structural separation is required for any use beyond the operator who understands the limitation.

### 4.4 Friction Independence

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| Friction challenges acceptance | ≥50% of friction questions challenge acceptance of the output rather than restating conclusions | For each full audit, meta-question: "Does this question challenge my acceptance, or ask me to restate what the output concluded?" |
| Friction surfaces downweighted concerns | At least 2 of 8 friction questions reference DA concerns that the synthesizer downweighted or omitted | Track whether friction questions cite DA-originated concerns not emphasized in synthesis |

---

## 5. Kill Criteria

If ANY of the following occur, the architecture has not earned further buildout:

- CADEP fails to outscore baseline on severity-weighted flaw score by ≥40%
- CADEP fails to outperform directionally on ≥6 of 8 proposals
- Citation verifiability drops below 80%
- Drift rate exceeds 10% (constrained-critic contract broken)
- Vault citation compliance drops below 90% (grounding claim false)
- Any unsourced numeric claim appears in a full-audit output (critical failure)

---

## 6. Pre-Commitment: What Happens After Phase 0

### If the Cowork skill passes Phase 0:

**We still build the following enforcement mechanisms in the API version:**

1. **Structural agent separation** — passing Phase 0 on 8 proposals doesn't prove prompt separation holds at scale. Structural separation is insurance against tail cases.
2. **Code-enforced drift scanner and output parser** — prompt-based compliance at 90%+ on 8 runs doesn't guarantee 90%+ on 200 runs. Deterministic enforcement doesn't degrade with scale.
3. **Provenance tagging parser** — full-audit zero-tolerance for unsourced numerics cannot be reliably maintained by prompt instruction alone over time.

**We accept as sufficient in the Cowork version:**

- The behavioral patterns (specialist → DA → synthesizer pipeline, adversarial routing, friction questions) are validated as producing decision-relevant critique.
- The vault structure and concept routing work well enough that the right papers get cited.
- The Cowork skill is a legitimate tool for **personal use** where the operator provides the enforcement layer that the code doesn't.

**We do NOT accept:**

- That the Cowork skill is deployable to other users without code-enforced mechanisms. If it ever serves anyone besides the original operator, the API version's enforcement is mandatory because other users won't know which outputs to distrust.

### If the Cowork skill fails Phase 0:

- Diagnose whether failures are behavioral (the pipeline doesn't produce good critique) or enforcement (the critique is good but compliance mechanisms leak).
- If behavioral: the pipeline design needs revision regardless of implementation.
- If enforcement: the API version with structural mechanisms may pass where prompt-based mechanisms failed. Build and re-test.

---

## 7. Predeclared Answer Keys

For each of the 8 proposals, write a brief answer key BEFORE running any panels:

"The most decision-relevant weakness of this proposal is ___."

If ambiguous, write the top 2 candidates and accept either. Score the synthesizer against the predeclared key. If the synthesizer selects a weakness not in the key, require a written explanation of why it was more decision-relevant.

**Answer keys must be written and timestamped before the first panel run.**

---

## 8. 155-Paper Knowledge Graph

The knowledge graph architecture document (24 nodes, 155 papers) is a **long-term reference document**, not a near-term build target. It contains no build timeline. It receives a build timeline only when Phase 0 results justify scaling beyond the current 29-paper vault.

---

## 9. Document Integrity

This document is frozen as of the date above. It may not be revised after Phase 0 test data is collected. If a threshold is discovered to be poorly calibrated, the correct response is:

1. Flag it as a design error in the Phase 0 results document
2. Propose a revised threshold with justification
3. Re-run affected tests against the revised threshold
4. Document both the original result (against original threshold) and the revised result

Retroactive threshold adjustment without re-running is not permitted.
