---
doc_id: dissmann-brechmann-czado-kurowicka-2013
title: "Selecting and Estimating Regular Vine Copulae and Application to Financial Returns"
authors: ["Jeffrey F. Dißmann", "Eike C. Brechmann", "Claudia Czado", "Dorota Kurowicka"]
year: 2013
citation_count: 850
source_url: https://doi.org/10.1016/j.csda.2012.08.010
concept_tags: [copula, vine-copula, model-selection, dependence-modeling]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Standard reference for automated vine copula model selection and estimation.
  Essential for any high-dimensional copula modeling where pair-copula
  constructions are used.
---

## Core Methodology
Proposes a sequential top-down algorithm for selecting and estimating regular vine (R-vine) copulae. The algorithm proceeds tree by tree: (1) for each tree level, select the tree structure by maximizing the sum of absolute empirical Kendall's τ values across edges (strongest pairwise dependencies captured first); (2) for each edge (pair-copula), select the best-fitting bivariate copula family from a candidate set using AIC; (3) estimate parameters via maximum likelihood; (4) compute pseudo-observations for the next tree level via the h-function (conditional distribution function of the copula). This makes vine copula modeling practical for moderate dimensions (d ≤ 50).

## Key Results
- Sequential algorithm is computationally feasible for dimensions up to d ≈ 50, requiring d(d-1)/2 bivariate copula fits
- Kendall's τ-based structure selection captures the strongest dependencies in the first trees, where they matter most
- AIC-based pair-copula family selection is effective in simulation studies — correctly identifies the true family with high probability when n ≥ 500
- Applied to financial returns, reveals heterogeneous pairwise dependence structures that exchangeable or elliptical copulas miss entirely
- Available in the R package VineCopula (and later rvinecopulib) with a complete implementation
- The independence copula in higher-order trees provides automatic parsimony — weak residual dependencies are pruned

## Stated Limitations
- Sequential estimation is not globally optimal — errors in the first tree (structure or family selection) propagate to subsequent trees
- The set of candidate pair-copula families affects model selection quality; too few candidates may miss the truth, too many increase computation
- Computational cost grows as O(d²) in the number of pair-copulas to estimate; infeasible for d > 100 without truncation
- AIC can overfit when sample size per pair is small — each pair-copula only sees n observations regardless of d
- The independence copula as a default in higher trees may mask residual dependence that accumulates
- The algorithm requires complete data — missing values must be imputed before vine copula estimation

## Applicability Conditions
- Appropriate when: modeling dependence among 5-50 variables with heterogeneous pairwise structures, when different pairs require different copula families
- Works best when: sufficient data per pair (n > 200 recommended for reliable family selection), the true dependence structure has strong associations concentrated in a few pairs
- Degrades when: d > 50 (truncation needed), sample size is small relative to the number of pairs, all dependencies are roughly equal (structure selection has little power)
- Not appropriate for: very high dimensions without truncation (use factor copulas instead), settings where all pairs have the same dependence structure (elliptical copula is simpler and sufficient)
