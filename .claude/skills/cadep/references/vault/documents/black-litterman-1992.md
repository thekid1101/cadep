---
doc_id: black-litterman-1992
title: "Global Portfolio Optimization"
authors: ["Fischer Black", "Robert Litterman"]
year: 1992
citation_count: 1471
source_url: https://doi.org/10.2469/faj.v48.n5.28
concept_tags: [portfolio-optimization, estimation-error, bayesian-estimation]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Foundational Bayesian approach to portfolio optimization that uses equilibrium
  returns as a prior, addressing estimation error in expected returns. Widely
  adopted in institutional portfolio management.
---

## Core Methodology
Combines Capital Asset Pricing Model (CAPM) equilibrium returns as a Bayesian prior with investor views expressed as linear constraints on expected returns. The equilibrium prior is π = δ·Σ·w_mkt, where δ is the risk aversion parameter, Σ is the covariance matrix, and w_mkt is the market capitalization weight vector. Investor views are expressed as P·μ = q + ε where P is a pick matrix, q is the view vector, and ε ~ N(0, Ω) represents view uncertainty. The posterior expected return is a precision-weighted combination: μ_BL = [(τΣ)⁻¹ + P'Ω⁻¹P]⁻¹[(τΣ)⁻¹π + P'Ω⁻¹q].

## Key Results
- Posterior expected returns blend equilibrium priors with investor views, weighted by their respective precisions
- Without investor views, the model defaults to equilibrium-implied returns — producing the market portfolio (a sensible neutral position)
- Avoids the extreme and unintuitive positions common in unconstrained Markowitz optimization
- The parameter τ controls relative confidence in the equilibrium prior vs. investor views — smaller τ means more confidence in equilibrium
- Portfolio weights change smoothly as views are added or modified — unlike Markowitz which can produce discontinuous jumps
- Equivalent to a mixed estimation (Theil) regression model combining prior information with sample evidence

## Stated Limitations
- Treats the covariance matrix Σ as known — estimation error in Σ is completely ignored in the standard formulation
- The choice of τ is ad hoc and significantly affects results; no consensus on the correct value (common choices: 0.025 to 1.0)
- Requires specifying both views and their confidence levels (Ω) — garbage in, garbage out; overconfident views produce extreme portfolios
- The equilibrium prior assumes CAPM holds — if the market is not in equilibrium or CAPM is misspecified, the prior is wrong
- View specification is subjective — the framework does not help generate views, only incorporate them
- Does NOT solve the covariance estimation problem — it must be paired with a good covariance estimator

## Applicability Conditions
- Appropriate when: institutional constraints require stable, intuitive portfolio weights; the analyst has specific return views to incorporate with quantified confidence
- Works best when: a small number of well-considered views are combined with the equilibrium prior, the covariance matrix is estimated separately with a good method (Ledoit-Wolf, DCC)
- Degrades when: many poorly calibrated views are specified (Ω is wrong), τ is chosen poorly, the covariance estimate is poor (GIGO)
- Not appropriate for: solving the covariance estimation problem (orthogonal concern), situations where CAPM equilibrium is a poor prior, purely systematic/quantitative strategies with no analyst views
