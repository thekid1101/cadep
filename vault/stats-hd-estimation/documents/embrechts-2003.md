---
doc_id: embrechts-2003
title: "Modelling Dependence with Copulas and Applications to Risk Management"
authors: ["Paul Embrechts", "Filip Lindskog", "Alexander McNeil"]
year: 2003
citation_count: 3150
source_url: null
concept_tags: [copula, dependence-modeling, tail-dependence]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-07"
slot_justification: |
  Seminal paper on pitfalls of correlation-based dependence measures and
  copula applications in risk management. Critical reference for understanding
  why linear correlation fails and when copulas add value.
---

## Core Methodology
Demonstrates the inadequacy of linear correlation as a dependence measure and shows how copulas provide a more complete characterization. Presents three fundamental pitfalls of correlation: (1) correlation is not a measure of concordance for non-elliptical distributions; (2) zero correlation does not imply independence; (3) marginal distributions and correlations do not determine the joint distribution. Shows how copula-based risk measures address these shortcomings.

## Key Results
- Linear correlation can be misleading for non-elliptical distributions — same marginals and same correlation can produce vastly different joint tail behavior
- For a given pair of marginals, the attainable correlation range may be a strict subset of [-1, 1] — correlation bounds depend on the marginals
- VaR and Expected Shortfall depend on the full joint distribution, not just correlations — copula choice matters for risk quantification
- Gaussian copula systematically underestimates joint extreme losses in financial data
- Student-t copula with low degrees of freedom captures the empirically observed clustering of extreme events
- The distinction between tail dependence and correlation is decision-critical for risk management

## Stated Limitations
- Does not provide a copula selection procedure — illustrates pitfalls rather than prescribing solutions
- Examples are primarily bivariate — high-dimensional implications are not fully explored
- Risk management applications assume stationary dependence structure — time-varying dependence requires dynamic copulas
- Tail dependence is a limiting property — finite-sample tail behavior may not match the asymptotic coefficient

## Applicability Conditions
- Essential reading when: a proposal uses correlation as the primary dependence measure, especially for non-Gaussian data
- Directly applicable when: evaluating whether a Gaussian copula is adequate for risk quantification
- Key finding: if joint tail risk matters for the decision, using correlation alone or a Gaussian copula is structurally inadequate
- Caution: the paper demonstrates problems but does not solve the model selection problem
