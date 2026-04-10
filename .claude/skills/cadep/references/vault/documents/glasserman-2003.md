---
doc_id: glasserman-2003
title: "Monte Carlo Methods in Financial Engineering"
authors: ["Paul Glasserman"]
year: 2003
citation_count: 3674
source_url: https://doi.org/10.1007/978-0-387-21617-1
concept_tags: [monte-carlo, variance-reduction, simulation, importance-sampling]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Definitive reference for Monte Carlo simulation in quantitative finance.
  Covers variance reduction, importance sampling, stratification, and convergence —
  all essential for simulation-based estimation and validation in CADEP.
---

## Core Methodology
Comprehensive treatment of Monte Carlo simulation for financial derivatives pricing and risk measurement. Covers the full pipeline: random number generation (uniform and non-uniform), simulation of stochastic processes (geometric Brownian motion, jump-diffusion, stochastic volatility), variance reduction techniques (antithetic variates, control variates, importance sampling, stratified sampling), quasi-Monte Carlo methods using low-discrepancy sequences, and efficiency analysis. Establishes the theoretical framework for analyzing convergence rates and quantifying efficiency gains from variance reduction.

## Key Results
- Standard Monte Carlo convergence rate is O(1/√n) regardless of dimension — the curse of dimensionality does not apply to the convergence rate
- Control variates reduce variance by exploiting correlation with a known-expectation quantity; optimal coefficient has a closed form
- Importance sampling optimal tilt minimizes variance by sampling proportionally to |f(x)·p(x)|; in practice, exponential tilting is used
- Stratified sampling always reduces variance compared to crude Monte Carlo (guaranteed improvement)
- Quasi-Monte Carlo (QMC) can achieve O(1/n) convergence for smooth integrands via low-discrepancy sequences (Sobol, Halton)
- Bridge sampling enables efficient simulation of path-dependent quantities by first sampling key time points

## Stated Limitations
- Variance reduction techniques are problem-specific — no single method is universally best; the wrong choice can increase variance
- Importance sampling can catastrophically increase variance if the tilt distribution is poorly chosen (weight degeneracy)
- QMC effectiveness degrades in very high dimensions (> 100) unless the integrand has low effective dimension
- Convergence rate analysis assumes finite variance; heavy-tailed distributions may have infinite variance, requiring truncation or alternative methods
- The O(1/√n) rate is a CLT result — pre-asymptotic behavior may be poor for small n or multimodal targets

## Applicability Conditions
- Appropriate when: simulating portfolio returns, estimating risk measures (VaR, CVaR, expected shortfall), validating estimation procedures, pricing derivatives
- Works best when: the payoff/quantity of interest is a smooth function, variance reduction techniques can be tailored to the problem structure
- Degrades when: the quantity of interest is an extreme quantile or rare event (standard MC is inefficient), the integrand is discontinuous or has infinite variance
- Not appropriate for: problems where analytical solutions exist (unnecessary computational cost), estimation problems where resampling (bootstrap) is more natural
