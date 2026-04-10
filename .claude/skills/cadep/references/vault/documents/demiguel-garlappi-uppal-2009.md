---
doc_id: demiguel-garlappi-uppal-2009
title: "Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?"
authors: ["Victor DeMiguel", "Lorenzo Garlappi", "Raman Uppal"]
year: 2009
citation_count: 5200
source_url: https://doi.org/10.1093/rfs/hhm075
concept_tags: [portfolio-optimization, estimation-error, diversification]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Landmark paper demonstrating that estimation error makes optimized portfolios
  underperform naive 1/N diversification out of sample. Essential reference for
  understanding why covariance estimation quality matters for downstream decisions.
---

## Core Methodology
Compares 14 different portfolio optimization models against the naive equally-weighted 1/N strategy across 7 empirical datasets spanning different asset classes and time periods. Tests whether the theoretical gains from optimal diversification survive estimation error in practice. Derives closed-form expressions for the minimum estimation window (sample size) required for a mean-variance optimized portfolio to outperform 1/N, showing this grows as O(p²) where p is the number of assets. Models tested include unconstrained mean-variance, Bayesian approaches (Jorion, Pastor), shrinkage methods, minimum-variance, and constraint-based strategies.

## Key Results
- None of the 14 optimized strategies consistently beats the 1/N portfolio on out-of-sample Sharpe ratio, certainty equivalent return, or turnover across datasets
- The required sample size for mean-variance optimization to outperform 1/N grows as O(p²) — prohibitively large for portfolios with p > 25 assets
- Estimation error in the covariance matrix is the primary driver of poor out-of-sample performance, not just error in the mean vector
- Bayesian, shrinkage, and constraint-based methods improve over unconstrained optimization but still struggle to beat 1/N
- The minimum-variance portfolio (ignoring expected returns entirely) is among the best-performing strategies — confirming that mean estimation is the weakest link
- 1/N achieves competitive certainty equivalent values even with sample sizes T > 500

## Stated Limitations
- Results depend on the evaluation metric (Sharpe ratio, certainty equivalent, turnover); different metrics can favor different strategies
- Analysis is limited to equity portfolios; results may not generalize to other asset classes or international settings
- Out-of-sample evaluation does not explicitly account for transaction costs in all comparisons
- Focuses on unconditional (buy-and-hold/rebalance) strategies; does not evaluate conditional or dynamic approaches
- The 1/N portfolio is only truly optimal when all assets have equal expected returns and equal risk — the comparison inherently favors 1/N when true parameters are uncertain

## Applicability Conditions
- Appropriate when: evaluating whether a covariance estimator improves portfolio performance in practice — this paper provides the key benchmark
- Works best when: the number of assets is moderate to large (p ≥ 10) and sample size is not extremely large relative to dimensionality
- Degrades when: the analyst has strong prior information about expected returns (reducing estimation error), the investment universe is very small (p < 5)
- Not appropriate for: comparison against strategies with explicit constraints, multi-period optimization, or trading cost models not included in the 14 models tested
