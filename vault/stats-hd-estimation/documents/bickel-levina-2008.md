---
doc_id: bickel-levina-2008
title: "Regularized Estimation of Large Covariance Matrices"
authors: ["Peter J. Bickel", "Elizaveta Levina"]
year: 2008
citation_count: 2103
source_url: https://doi.org/10.1214/009053607000000758
concept_tags: [covariance-estimation.high-dimensional, regularization]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-07"
slot_justification: |
  Establishes theoretical framework for banding and thresholding covariance estimators.
  Proves convergence rates under sparsity assumptions. Key reference for understanding
  when and why regularized covariance estimation works.
---

## Core Methodology
Two regularization approaches: (1) Banding — set entries of sample covariance to zero beyond a bandwidth k from the diagonal; (2) Thresholding — set entries below a threshold to zero. Both exploit assumed sparsity structure in the true covariance matrix. Convergence rates established under operator norm and Frobenius norm.

## Key Results
- Banding estimator achieves optimal rate under bandable covariance assumption (entries decay away from diagonal)
- Thresholding achieves minimax-optimal rate over the class of sparse covariance matrices
- Rate of convergence is (k/n + k^(-2α)) for banding, where α controls decay rate
- Both methods preserve positive semi-definiteness with appropriate modifications
- Bandwidth/threshold selection via cross-validation shown to be consistent

## Stated Limitations
- Banding requires a natural ordering of variables — not applicable when ordering is arbitrary
- Thresholding can produce non-positive-definite matrices without modification
- Sparsity assumptions on covariance (not precision) matrix — different structural assumption from graphical lasso
- Convergence rates assume sub-Gaussian data — heavy tails require different analysis
- Neither method is rotation-equivariant — results depend on coordinate system

## Applicability Conditions
- Requires: variables have a meaningful ordering (for banding) or covariance matrix is approximately sparse
- Works best when: covariance matrix has off-diagonal decay or sparse structure
- Degrades when: true covariance is dense or has long-range correlations
- Not appropriate when: variable ordering is arbitrary and covariance is not sparse (use shrinkage instead)
