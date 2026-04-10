---
doc_id: patton-2006
title: "Modelling Asymmetric Exchange Rate Dependence"
authors: ["Andrew J. Patton"]
year: 2006
citation_count: 1200
source_url: https://doi.org/10.1111/j.1468-2354.2006.00387.x
concept_tags: [copula, time-series-dependence, dynamic-copula]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Pioneered time-varying copula models by allowing copula parameters to evolve
  over time via ARMA-like dynamics. Bridges copula theory and time series
  dependence modeling.
---

## Core Methodology
Extends static copula models to allow parameters to vary over time via an evolution equation driven by lagged dependence measures. For the time-varying normal copula: ρ_t = Λ(ω + β·ρ_{t-1} + α·(1/k)·Σ_{j=1}^{k} Φ⁻¹(u_{t-j})·Φ⁻¹(v_{t-j})) where Λ is a modified logistic transformation ensuring ρ_t ∈ (-1,1). Analogous evolution equations are defined for Clayton and Student-t copula parameters, allowing tail dependence to vary over time. Estimation is by maximum likelihood conditional on estimated marginals (inference functions for margins — IFM approach).

## Key Results
- Time-varying copulas capture changing dependence regimes (e.g., increased correlation during crises, contagion effects)
- Asymmetric dependence detected in exchange rates: stronger dependence during joint depreciations than joint appreciations
- The Student-t copula with time-varying parameters outperforms static alternatives and time-varying Gaussian copula (captures dynamic tail dependence)
- IFM estimation is consistent and asymptotically normal under correct marginal specification
- Model comparison via AIC/BIC and Vuong likelihood ratio test for non-nested copula models
- The forcing variable approach (lagged cross-products of transformed residuals) provides a natural measure of recent dependence

## Stated Limitations
- Parametric specification of dynamics may be misspecified — the evolution equation is ad hoc, not derived from economic theory
- IFM estimation inherits errors from the marginal estimation stage; two-stage standard errors understate true uncertainty
- The framework is inherently bivariate — multivariate extension to d > 2 via time-varying vine copulas is non-trivial and computationally expensive
- Parameter instability can lead to poor out-of-sample performance if the driving dynamics change
- The number of lags k in the forcing variable is typically set to 10 without formal selection

## Applicability Conditions
- Appropriate when: dependence structure changes over time (regime shifts, crises, contagion), modeling asymmetric tail dependence dynamics
- Works best when: applied to bivariate or low-dimensional problems, the marginals are well-specified, sufficient data exists to estimate dynamic parameters (n > 500)
- Degrades when: the dependence dynamics are stable over time (static copula is sufficient), the marginal specification is poor (contaminates copula estimation), applied to high dimensions without vine copula extension
- Not appropriate for: high-dimensional dependence modeling without vine copulas (see dissmann-brechmann-czado-kurowicka-2013), settings where marginal distributions are highly uncertain
