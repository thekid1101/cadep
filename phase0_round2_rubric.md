# Phase 0 Round 2 — Pre-Declared Rubric

**Frozen**: April 10, 2026
**Written before any Round 2 test runs**
**Purpose**: Test whether a single prompted baseline with CADEP's output constraints matches CADEP's discipline while retaining broader coverage

---

## Rubric (4 dimensions, max 10 per proposal, max 80 across 8)

### (a) Decision-Changing Flaw Identified — Binary, 3 points
Did the output identify the predeclared answer key weakness? Yes = 3, No = 0. No partial credit.

### (b) Flaw Grounded in Verifiable Vault Citation — Binary, 2 points
Is the decision-changing flaw backed by a citation to a paper that exists in the vault, and does the paper actually support the claim? Yes = 2, No = 0.

### (c) Actionability — Scale, 1-3 points
- 3: Output contains a concrete, immediately executable verification step
- 2: Verification step present but vague or requires interpretation
- 1: Mentions "further investigation" without specifics

### (d) No Unbackable Claims — Binary, 2 points
Did the output avoid unsourced numeric claims, out-of-vault citations, and recommendation language ("use X instead", "switch to", "the correct approach is")? Yes = 2, No = 0. Any single violation = 0.

---

## Test Design

Same 8 proposals from Round 1. Same predeclared answer keys (already frozen).

**Condition A**: CADEP Cowork skill outputs (already collected in Round 1 — reuse, do not re-run)

**Condition B**: "Prompted baseline" — single Claude conversation receiving:
- The same vault documents as CADEP
- The CADEP fast-path/full-audit output format constraints
- The "no recommendation language" rule
- The "cite only vault papers" rule
- NO multi-agent pipeline, no specialist/DA/synthesizer separation

The prompted baseline prompt:
"Review this proposal. Identify the single most decision-relevant flaw, cite a specific paper from the provided vault documents, provide one concrete verification step. Do not recommend alternative methods. Do not cite papers outside the provided documents. Do not produce unsourced numeric claims. Use this exact output format: LIKELY FAILURE POINT, UNTESTED ASSUMPTION, CHECK NEXT."

**What this tests**: If the prompted baseline matches CADEP on all 4 dimensions, the multi-agent pipeline does not earn its complexity — the value is in the prompt template and vault curation. If the prompted baseline drifts (recommends solutions, cites outside vault, inflates output), the pipeline has a case for behavioral enforcement.
