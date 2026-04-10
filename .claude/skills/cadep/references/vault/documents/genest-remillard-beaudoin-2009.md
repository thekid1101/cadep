---
doc_id: genest-remillard-beaudoin-2009
title: "Goodness-of-Fit Tests for Copulas: A Review and a Power Study"
authors: ["Christian Genest", "Bruno Rémillard", "David Beaudoin"]
year: 2009
citation_count: 1795
source_url: https://doi.org/10.1016/j.insmatheco.2007.10.005
concept_tags: [copula, goodness-of-fit, model-selection]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Most comprehensive review and power comparison of goodness-of-fit tests for
  copula models. Required reference for any proposal involving copula model
  selection or validation.
---

## Core Methodology
Comprehensive review and Monte Carlo power study of goodness-of-fit (GoF) tests for parametric copula models. Focuses on "blanket tests" that assess the global fit of a parametric copula C_θ against the nonparametric empirical copula. Tests are based on the empirical copula process C_n(u) - C_{θ̂}(u), using Cramér-von Mises (S_n = ∫[C_n(u) - C_{θ̂}(u)]² dC_n(u)) and Kolmogorov-Smirnov (T_n = sup|C_n(u) - C_{θ̂}(u)|) statistics. Because the null distribution depends on the unknown parameter θ, p-values are obtained via parametric bootstrap: (1) estimate θ̂ from data, (2) simulate B samples from C_{θ̂}, (3) re-estimate and re-compute the test statistic for each sample.

## Key Results
- Cramér-von Mises statistic (S_n) consistently outperforms Kolmogorov-Smirnov (T_n) in statistical power across all scenarios tested
- Parametric bootstrap produces valid (asymptotically correct) p-values for composite null hypotheses
- Tests have good power to distinguish between Gaussian, Clayton, Frank, and Gumbel copula families with n ≥ 200
- Power increases with sample size and with the magnitude of the true departure from the null model
- Pseudo-observations (rank-based) should be used instead of known marginals — using parametric marginals introduces additional error
- Rosenblatt transform-based tests provide a complementary approach with different power profiles

## Stated Limitations
- Parametric bootstrap is computationally intensive: B bootstrap samples × parameter re-estimation per sample (B = 1000 recommended)
- Power decreases rapidly in dimensions d > 2 — the tests are primarily practical for bivariate and trivariate copulas
- Tests are designed for i.i.d. data — serial dependence in time series data requires modification (block bootstrap or pre-filtering via GARCH)
- Asymptotic theory for the test statistics under the null is complex and not easily extended to new copula families
- The tests assess global fit — they may miss localized departures (e.g., poor tail fit with good bulk fit)

## Applicability Conditions
- Appropriate when: validating a copula model choice before using it for simulation or risk measurement, comparing competing copula families
- Works best when: data is bivariate or trivariate, sample size is n ≥ 200, data is i.i.d. or pre-filtered for serial dependence
- Degrades when: dimension exceeds 3-4 (power drops significantly), sample size is small (n < 100), data has strong serial dependence without pre-filtering
- Not appropriate for: high-dimensional copula validation (use vine copula information criteria instead), real-time model selection (bootstrap is too slow), time series data without GARCH pre-filtering
