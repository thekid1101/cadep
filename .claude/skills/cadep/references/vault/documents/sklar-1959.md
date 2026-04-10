---
doc_id: sklar-1959
title: "Fonctions de répartition à n dimensions et leurs marges"
authors: ["Abe Sklar"]
year: 1959
citation_count: 6200
source_url: null
concept_tags: [copula, dependence-modeling]
superseded_by: null
coverage_quality: abstract-only
math_syntax_status: no-math
cadep_citation_count: 0
last_verified: "2026-04-07"
slot_justification: |
  Foundational theorem establishing copulas. Proves that any multivariate
  distribution can be decomposed into marginals and a copula. Required
  citation for any copula-based modeling proposal.
---

## Core Methodology
Sklar's Theorem: For any multivariate distribution function H with marginal distributions F₁, ..., Fₙ, there exists a copula C such that H(x₁, ..., xₙ) = C(F₁(x₁), ..., Fₙ(xₙ)). If the marginals are continuous, the copula is unique. Conversely, any copula C combined with any marginals F₁, ..., Fₙ produces a valid multivariate distribution.

## Key Results
- Separates dependence structure (copula) from marginal behavior
- Enables flexible modeling: choose any marginals and any copula independently
- Uniqueness holds for continuous marginals
- For discrete marginals, the copula exists but is not unique — only defined on the range of the marginals
- Provides the theoretical foundation for all copula-based statistical methods

## Stated Limitations
- The theorem is existential — it guarantees a copula exists but does not specify which copula is appropriate for a given dataset
- Separation of marginals and copula is a modeling convenience, not a statement about the data-generating process
- No guidance on copula selection or goodness-of-fit
- The uniqueness result fails for discrete marginals, creating ambiguity in discrete data settings

## Applicability Conditions
- Universal: applies to any multivariate distribution
- Key implication: the choice of copula family is a modeling decision, not determined by the data
- The theorem justifies but does not validate any particular copula choice
