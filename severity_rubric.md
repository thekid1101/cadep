# CADEP Phase 0 Severity Rubric

Pre-written before scoring. Used for blind-scored evaluation of both CADEP panel outputs and baseline outputs.

## Scoring Tiers

### Tier 1: Decision-Changing (3 points)
A flaw that, if true, should change the operator's decision about whether to proceed with the proposed approach.

**Examples:**
- Method assumes independence that provably does not hold in the stated context
- Cited paper's applicability conditions are violated by the proposal's parameters (e.g., p >> n when method requires p < n)
- Alternative method demonstrably outperforms on the stated objective with equivalent constraints
- Implementation would produce biased results in a direction that invalidates the use case

### Tier 2: Implementation-Relevant (1 point)
A flaw that does not change the decision to proceed but changes HOW to proceed.

**Examples:**
- Hyperparameter tuning guidance that affects convergence or accuracy
- Sample size consideration that affects confidence but not viability
- Computational cost issue that affects feasibility but has known workarounds
- Edge case that requires explicit handling but does not invalidate the approach

### Tier 3: Contextual Caveat (0 points)
Background information that is technically correct but does not affect the specific decision.

**Examples:**
- General limitations of the method class that are well-known to practitioners
- Theoretical concerns that do not apply given the stated constraints
- Historical context about the method's development
- Recommendations for further reading

## Scoring Protocol

1. For each proposal, score CADEP output and baseline output independently
2. Count flaws in each tier
3. Severity-weighted score = (Tier 1 count x 3) + (Tier 2 count x 1) + (Tier 3 count x 0)
4. Record directional winner (higher score = better)
5. Note any flaws surfaced by one but not the other

## Phase 0 Exit Criteria (Reference)

- CADEP scores >=40% higher on severity-weighted flaw score
- CADEP outperforms on >=6 of 8 proposals directionally
- Citation verifiability >=80% (manual spot-check)
- Synthesizer correctly identifies most decision-relevant weakness on >=5 of 8
- Human review time for CADEP <=2x baseline
