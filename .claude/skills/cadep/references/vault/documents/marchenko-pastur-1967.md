---
doc_id: marchenko-pastur-1967
title: "Distribution of Eigenvalues for Some Sets of Random Matrices"
authors: ["Vladimir A. Marchenko", "Leonid A. Pastur"]
year: 1967
citation_count: 4200
source_url: https://doi.org/10.1070/SM1967v001n04ABEH001994
concept_tags: [random-matrix-theory, eigenvalue-distribution, covariance-estimation.high-dimensional]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Foundational theorem in random matrix theory establishing the limiting spectral
  distribution of sample covariance matrices. Required reference for understanding
  eigenvalue behavior when p/n → γ > 0.
---

## Core Methodology
Proves that the empirical spectral distribution of a sample covariance matrix (1/n)X'X, where X is p×n with i.i.d. entries, converges almost surely to a deterministic distribution (the Marchenko-Pastur law) as p,n → ∞ with p/n → γ. The proof uses analytic properties of the Stieltjes transform and moment methods, establishing that the limiting spectral measure is universal — independent of the specific entry distribution under regularity conditions (matching first two moments).

## Key Results
- The empirical spectral distribution converges almost surely to the Marchenko-Pastur distribution with parameter γ = p/n
- When the true covariance is identity, the support of the limit distribution is [(1-√γ)², (1+√γ)²]
- The limiting density has a characteristic form: ρ(x) = (1/2πγx)·√((b-x)(x-a)) for x ∈ [a,b], where a = (1-√γ)² and b = (1+√γ)²
- When γ > 1, there is an additional point mass of (1-1/γ) at zero (more variables than observations)
- The result holds for general entry distributions with finite second moment — universality
- Sample eigenvalues spread far beyond their population values; the spreading increases with γ

## Stated Limitations
- Assumes i.i.d. entries with finite second moment; dependent or heavy-tailed entries require separate analysis
- Base result assumes the true population covariance is identity; extensions to general Σ require the generalized Marchenko-Pastur equation
- Requires p/n → γ for a constant γ ∈ (0,∞); the result does not apply when p is fixed and n → ∞
- Convergence is almost sure but rates of convergence are not characterized — finite-sample approximation quality is unknown
- Describes the bulk of the spectrum only; edge eigenvalue behavior follows Tracy-Widom (see johnstone-2001)

## Applicability Conditions
- Appropriate when: assessing whether sample covariance eigenvalues exhibit distortion expected from high-dimensional sampling noise
- Works best when: the ratio p/n is held approximately constant, data entries are approximately i.i.d. with light tails
- Degrades when: p/n varies significantly, both p and n are small (< 50), entries are heavy-tailed or strongly dependent
- Not appropriate for: understanding individual extreme eigenvalues (use Tracy-Widom), structured population covariance without the generalized equation, correlated or sparse data
