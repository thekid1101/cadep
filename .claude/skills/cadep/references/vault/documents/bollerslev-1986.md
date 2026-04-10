---
doc_id: bollerslev-1986
title: "Generalized Autoregressive Conditional Heteroskedasticity"
authors: ["Tim Bollerslev"]
year: 1986
citation_count: 28500
source_url: https://doi.org/10.1016/0304-4076(86)90063-1
concept_tags: [garch, volatility-modeling, time-series-dependence]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Introduced the GARCH model, the foundation for all conditional volatility
  modeling. Required for any proposal involving time-varying covariance
  estimation or volatility clustering.
---

## Core Methodology
Generalizes Engle's (1982) ARCH model by allowing the conditional variance to depend on its own past values as well as past squared innovations. The GARCH(p,q) model specifies: σ²_t = ω + Σ_{i=1}^{q} α_i·ε²_{t-i} + Σ_{j=1}^{p} β_j·σ²_{t-j}. The workhorse GARCH(1,1) specification is σ²_t = ω + α·ε²_{t-1} + β·σ²_{t-1}, capturing volatility clustering — large (small) changes tend to be followed by large (small) changes. Estimation is by maximum likelihood, assuming Gaussian or Student-t conditional innovations.

## Key Results
- GARCH(1,1) captures the key stylized facts of financial return volatility: clustering, mean-reversion, and excess kurtosis (leptokurtosis)
- Stationarity of the variance process requires α + β < 1; the unconditional variance is ω/(1 - α - β)
- GARCH is equivalent to an ARMA model for squared returns: ε²_t follows ARMA(max(p,q), p)
- Maximum likelihood estimation is straightforward under Gaussian or Student-t innovations; quasi-MLE is consistent even under misspecified innovation distribution
- GARCH(1,1) is almost always sufficient in practice — higher-order specifications rarely improve fit for financial data
- The persistence parameter (α + β) determines how quickly volatility shocks decay; values near 1 indicate near-integrated volatility (IGARCH)

## Stated Limitations
- Symmetric: treats positive and negative shocks identically — does not capture the leverage effect (negative returns increase volatility more than positive returns of equal magnitude)
- Does not capture long memory in volatility (slow hyperbolic decay of autocorrelations); FIGARCH or HAR models address this
- Gaussian GARCH underestimates tail risk; Student-t or GED innovations partially address this but may still be insufficient
- Multivariate extensions (BEKK, CCC, DCC) suffer from parameter explosion: O(p²) or O(p⁴) parameters
- Estimation with heavy-tailed innovations requires quasi-MLE or robust methods; standard MLE standard errors are invalid

## Applicability Conditions
- Appropriate when: modeling conditional variance for portfolio risk, filtering returns before copula estimation, volatility forecasting
- Works best when: the return series exhibits volatility clustering, the leverage effect is not the primary concern, univariate or low-dimensional setting
- Degrades when: the leverage effect is important (use EGARCH or GJR-GARCH), long memory is present, the series is multivariate with many assets
- Not appropriate for: static covariance estimation (GARCH is inherently dynamic), high-dimensional problems without DCC or factor structure, data without volatility clustering
