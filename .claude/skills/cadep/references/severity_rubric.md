---
doc_id: severity-rubric
title: "CADEP Phase 0 Severity Rubric"
purpose: Blind scoring of panel outputs for quality evaluation
---

## Scoring Tiers

### Tier 1: Decision-Changing (3 points)
A flaw that, if true, should change the operator's decision about whether to proceed.

Examples:
- Method assumes independence that provably does not hold
- Cited paper's applicability conditions are violated by the proposal's parameters
- Alternative method demonstrably outperforms on the stated objective
- Implementation would produce biased results that invalidate the use case

### Tier 2: Implementation-Relevant (1 point)
A flaw that changes HOW to proceed but not WHETHER to proceed.

Examples:
- Hyperparameter tuning guidance affecting convergence
- Sample size consideration affecting confidence but not viability
- Computational cost issue with known workarounds
- Edge case requiring explicit handling

### Tier 3: Contextual Caveat (0 points)
Background info that doesn't affect the specific decision.

Examples:
- General method limitations well-known to practitioners
- Theoretical concerns not applicable given stated constraints
- Historical context
- Further reading recommendations

## Scoring Protocol
1. Count flaws per tier
2. Severity-weighted score = (Tier 1 x 3) + (Tier 2 x 1)
3. Higher score = more decision-relevant issues surfaced
