---
doc_id: nelsen-2006
title: "An Introduction to Copulas"
authors: ["Roger B. Nelsen"]
year: 2006
citation_count: 11500
source_url: https://doi.org/10.1007/0-387-28678-0
concept_tags: [copula, dependence-modeling, tail-dependence]
superseded_by: null
coverage_quality: partial
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-07"
slot_justification: |
  Standard reference textbook on copulas. Comprehensive treatment of copula
  families, properties, and dependence measures. Essential reference for
  understanding copula selection and properties.
---

## Core Methodology
Comprehensive treatment of copula theory including: Archimedean copulas (Clayton, Frank, Gumbel), elliptical copulas (Gaussian, Student-t), extreme value copulas, and their properties. Covers dependence measures (Kendall's tau, Spearman's rho, tail dependence coefficients) and their relationship to copula parameters.

## Key Results
- Gaussian copula has zero tail dependence — regardless of correlation strength, extreme events become asymptotically independent
- Student-t copula captures symmetric tail dependence controlled by degrees of freedom parameter
- Clayton copula captures lower tail dependence (left tail clustering)
- Gumbel copula captures upper tail dependence (right tail clustering)
- Frank copula has zero tail dependence but captures overall dependence symmetrically
- Tail dependence is a property of the copula family, not a parameter — cannot be estimated within a family that lacks it
- Kendall's tau and Spearman's rho are copula-invariant under monotone transformations of marginals

## Stated Limitations
- Archimedean copulas in d > 2 dimensions have restrictive exchangeability constraint — all pairs share the same dependence structure
- Elliptical copulas require symmetry — not appropriate for asymmetric dependence patterns
- Copula selection remains largely model-dependent — no universal selection procedure
- Higher-dimensional copula estimation is computationally challenging and statistically unreliable with small samples
- Tail dependence estimation requires extreme-value data — unreliable with moderate samples

## Applicability Conditions
- Gaussian copula appropriate when: tail dependence is not a concern and linear correlation is the relevant dependence measure
- Student-t copula appropriate when: symmetric tail dependence is expected and degrees of freedom can be reliably estimated
- Archimedean copulas appropriate when: dimension is low (d=2) or exchangeability is defensible
- Key caution: choosing a Gaussian copula when tail dependence exists systematically underestimates joint extreme risk
