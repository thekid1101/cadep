---
doc_id: johnstone-2001
title: "On the Distribution of the Largest Eigenvalue in Principal Components Analysis"
authors: ["Iain M. Johnstone"]
year: 2001
citation_count: 1850
source_url: https://doi.org/10.1214/aos/1009210544
concept_tags: [random-matrix-theory, eigenvalue-distribution, principal-components]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Established Tracy-Widom distribution as the limiting distribution for the largest
  eigenvalue of Wishart matrices. Essential for PCA significance testing in high
  dimensions and for determining the number of signal components.
---

## Core Methodology
Shows that the largest eigenvalue of a Wishart matrix W_p(I_p, n) (sample covariance from p-dimensional Gaussian data with n observations), when centered by μ_np = (√(n-1) + √p)² and scaled by σ_np = (√(n-1) + √p)(1/√(n-1) + 1/√p)^(1/3), converges in distribution to the Tracy-Widom law of order 1 (TW₁). This provides a precise null distribution for the largest principal component variance under the hypothesis that the population covariance is proportional to the identity.

## Key Results
- The largest sample eigenvalue, properly centered and scaled, converges to the Tracy-Widom distribution TW₁
- The centering constant μ_np = (√(n-1) + √p)² and scaling constant σ_np are explicit functions of p and n
- Provides a test for the number of significant principal components: reject if scaled largest eigenvalue exceeds TW₁ critical value
- Finite-sample corrections improve accuracy for moderate p and n (the basic centering/scaling can be inaccurate for p,n < 50)
- The result extends to testing whether the k-th largest eigenvalue exceeds the null — enables sequential testing for the number of factors
- Under alternatives (spiked covariance model), the largest eigenvalue exhibits a phase transition: eigenvalues above a critical threshold separate from the bulk

## Stated Limitations
- Assumes Gaussian data; extensions to non-Gaussian distributions exist (Soshnikov 2002) but under stronger moment conditions
- Requires both p and n to be large for the TW approximation to be accurate; unreliable when either is small (< 20)
- Sensitive to outliers — a single outlier can inflate the largest eigenvalue beyond the TW threshold
- The phase transition result assumes the spike is above the BBP (Baik-Ben Arous-Péché) threshold; below-threshold signals are undetectable
- Does not directly address the covariance estimation problem — only tests whether signal exists

## Applicability Conditions
- Appropriate when: testing significance of principal components, determining how many eigenvalues represent signal vs. noise
- Works best when: data is approximately Gaussian, both p and n exceed 50, no extreme outliers
- Degrades when: data is heavy-tailed, sample size is small relative to dimension, outliers are present
- Not appropriate for: estimating the covariance matrix (only tests structure), non-Gaussian heavy-tailed data without robust modifications
