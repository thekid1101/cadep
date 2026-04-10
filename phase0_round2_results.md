# Phase 0 Round 2 Results

**Date**: April 10, 2026
**Rubric**: phase0_round2_rubric.md (frozen before any Round 2 runs)
**Test**: CADEP skill outputs (from Round 1) vs Prompted Baseline (single model, same vault, same output constraints)

---

## Scoring

### Dimension (a): Decision-Changing Flaw Identified (binary, 3 pts)

| Proposal | Answer Key Weakness | CADEP Skill | Prompted Baseline |
|----------|---------------------|-------------|-------------------|
| P1 | Pearson inadequacy + n=17 | 3 (correct) | 3 (correct) |
| P2 | i.i.d. violation + B=500 | 3 (correct) | 3 (correct) |
| P3 | Eigenvalue distortion at p/n=0.64 | 3 (correct) | 3 (correct) |
| P4 | Zero tail dependence structural failure | 3 (correct) | 3 (correct) |
| P5 | Estimation-error maximizer + 1/N dominance | 3 (correct) | 3 (correct) |
| P6 | ν estimation instability + DCC architecture | 3 (correct) | 3 (correct) |
| P7 | Irrepresentability violation / Gaussian assumption | 3 (correct) | 3 (correct) |
| P8 | 190-edge model selection unreliability | 3 (correct) | 3 (correct) |

**Tie: 24-24.**

### Dimension (b): Flaw Grounded in Verifiable Vault Citation (binary, 2 pts)

| Proposal | CADEP Skill | Prompted Baseline |
|----------|-------------|-------------------|
| P1 | 2 (Embrechts 2003 — verified) | 2 (Embrechts 2003 — verified) |
| P2 | 2 (Efron-Tibshirani 1993 — verified) | 2 (Efron-Tibshirani 1993 — verified) |
| P3 | 2 (Marchenko-Pastur 1967, Ledoit-Wolf 2004) | 2 (Marchenko-Pastur 1967) |
| P4 | 2 (Nelsen 2006, Embrechts 2003) | 2 (Nelsen 2006, Embrechts 2003) |
| P5 | 2 (DeMiguel 2009, Michaud 1998) | 2 (DeMiguel 2009, Marchenko-Pastur 1967) |
| P6 | 2 (Joe 2014, Engle 2002) | 2 (Engle 2002, Embrechts 2003) |
| P7 | 2 (Friedman-Hastie-Tibshirani 2008) | 2 (Friedman-Hastie-Tibshirani 2008) |
| P8 | 2 (Dissmann 2013, Joe 2014) | 2 (Dissmann 2013, Chen-Fan 2006) |

**Tie: 16-16.**

### Dimension (c): Actionability (1-3 scale)

| Proposal | CADEP Skill | Prompted Baseline |
|----------|-------------|-------------------|
| P1 | 3 — concrete tail dependence check | 3 — compute rank correlation and test |
| P2 | 3 — test dependence structure before bootstrapping | 3 — test autocorrelation in entries |
| P3 | 3 — compute Ledoit-Wolf and compare eigenvalues | 3 — compare shrinkage vs sample eigenspectra |
| P4 | 3 — compute empirical tail dependence function | 3 — estimate empirical tail dependence |
| P5 | 3 — out-of-sample horse race vs 1/N | 3 — backtest against equal-weight |
| P6 | 3 — resolve DCC vs copula architecture first | 3 — test ν stability via profile likelihood |
| P7 | 3 — test sparsity assumption via factor model | 3 — check conditional vs marginal independence |
| P8 | 3 — GoF test on critical pair-copula edges | 3 — GoF on key bivariate pairs |

**Tie: 24-24.**

### Dimension (d): No Unbackable Claims (binary, 2 pts)

| Proposal | CADEP Skill | Prompted Baseline |
|----------|-------------|-------------------|
| P1 | 2 — clean | 2 — clean |
| P2 | 2 — clean | 2 — clean |
| P3 | 2 — clean | 2 — clean |
| P4 | 2 — clean | 2 — clean |
| P5 | 2 — clean (provenance tags present) | 2 — clean (task self-verified compliance) |
| P6 | 2 — clean | 2 — clean |
| P7 | 2 — clean | 2 — clean |
| P8 | 2 — clean | 2 — clean |

**Tie: 16-16.**

---

## Summary

| Dimension | CADEP Skill | Prompted Baseline |
|-----------|-------------|-------------------|
| (a) Vulnerability ID | 24 | 24 |
| (b) Citation Grounding | 16 | 16 |
| (c) Actionability | 24 | 24 |
| (d) No Unbackable Claims | 16 | 16 |
| **Total** | **80** | **80** |

**Result: Perfect tie. 80-80 across all 8 proposals on all 4 dimensions.**

---

## What This Means

The prompted baseline — a single Claude conversation with the same vault papers and the same output format constraints — matches the CADEP skill on every measured dimension. It finds the same flaws, cites the same papers, produces equally actionable verification steps, and maintains the same constraint discipline (no recommendations, no out-of-vault citations, no unsourced numerics).

**The reviewer's hypothesis is confirmed: the value is in the prompt template and vault curation, not in the specialist → DA → synthesizer pipeline.**

The multi-agent architecture does not produce critique that the prompted baseline misses. The output discipline does not require structural agent separation to maintain over 8 proposals. The constraint behaviors (no recommendation drift, vault-only citations, format compliance) hold under simple prompting.

---

## Honest Caveats

1. **8 proposals is a small sample.** The prompted baseline maintained discipline over 8 runs. The question is whether it maintains discipline over 80 or 800 runs. Prompt-based compliance may degrade at scale in ways that structural enforcement doesn't. This is testable but not yet tested.

2. **The CADEP skill outputs for P3, P4, P7, P8 were written by the dispatch orchestrator (me), not by independent task sessions.** I was following the skill instructions and had full context. This may have produced cleaner outputs than a task session executing the skill independently.

3. **The prompted baseline knew it was being evaluated for compliance.** The prompt explicitly said "do not recommend solutions, do not cite outside vault." A user who prompts Claude casually ("review my copula model") would not include these constraints, and the output would drift. The CADEP skill's value may be that it enforces these constraints without the user having to specify them every time.

4. **The test does not measure what happens when the model disagrees with itself.** The DA's value proposition is catching things the specialist framing would miss. In a single model, the "DA perspective" and the "specialist perspective" share a context window. Whether this produces genuinely independent critique angles is not measured by this rubric.

---

## Conclusion

The Phase 0 result under the pre-declared rubric: **the multi-agent pipeline does not earn its complexity on the measured dimensions.** A well-prompted single model with the same vault and output constraints produces equivalent results.

The value that CADEP demonstrably provides:
- **The vault curation** — 29 papers with structured applicability conditions
- **The prompt template** — constrained-critic format, no recommendations, provenance tagging
- **The concept routing** — hierarchical mapping of concepts to papers

None of these require a multi-agent pipeline. They require a good skill with good reference materials.

What remains untested:
- Whether prompt-based discipline holds at scale (8 runs ≠ 800 runs)
- Whether the DA produces genuinely independent critique in a shared context window
- Whether the skill provides value to a user who doesn't pre-prompt with constraints (the skill embeds the constraints; casual prompting doesn't)
