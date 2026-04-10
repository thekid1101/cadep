---
doc_id: efron-tibshirani-1993
title: "An Introduction to the Bootstrap"
authors: ["Bradley Efron", "Robert J. Tibshirani"]
year: 1993
citation_count: 42500
source_url: https://doi.org/10.1007/978-1-4899-4541-9
concept_tags: [bootstrap, simulation]
superseded_by: null
coverage_quality: partial
math_syntax_status: no-math
cadep_citation_count: 0
last_verified: "2026-04-07"
slot_justification: |
  Foundational text on bootstrap methods. Required reference for any proposal
  involving resampling-based validation of estimators. Most-cited statistics
  book of the modern era.
---

## Core Methodology
The bootstrap estimates the sampling distribution of a statistic by resampling with replacement from the observed data. For a statistic θ̂ computed from data X₁,...,Xₙ: (1) draw B bootstrap samples X₁*,...,Xₙ* by sampling with replacement; (2) compute θ̂* for each bootstrap sample; (3) use the distribution of θ̂* values to estimate standard errors, confidence intervals, and bias of θ̂.

## Key Results
- Bootstrap provides consistent estimates of standard errors and confidence intervals without distributional assumptions
- Bias-corrected and accelerated (BCa) intervals have better coverage than basic percentile intervals
- Parametric bootstrap (resample from fitted model) is more efficient when model is correct
- Bootstrap fails for statistics that are not smooth functions of the empirical distribution (e.g., extreme order statistics)
- Block bootstrap and other variants handle dependent data (time series, spatial)
- B = 200 typically sufficient for standard error estimation; B = 1000+ needed for confidence intervals

## Stated Limitations
- Bootstrap is inconsistent for extreme quantiles and maximum/minimum statistics
- Standard (i.i.d.) bootstrap fails for dependent data — block bootstrap or model-based bootstrap required
- Computational cost of B resamples × cost of computing θ̂ can be prohibitive for complex estimators
- Bootstrap confidence intervals can have poor coverage for skewed or bounded statistics without BCa correction
- The bootstrap estimates the sampling distribution centered at the observed statistic, not at the true parameter — this distinction matters for bias

## Applicability Conditions
- Appropriate when: the statistic is a smooth function of the data and observations are i.i.d. (or dependence is handled via block/model bootstrap)
- Works best when: sample size is moderate (n ≥ 30) and the statistic is well-behaved
- Degrades when: sample size is very small, statistic is non-smooth, or data has complex dependence
- Not appropriate for: extreme quantile estimation, statistics at boundary of parameter space
- For copula validation: bootstrap can validate copula parameter estimates but requires pseudo-observation bootstrap (not naive resampling)
