---
doc_id: chen-fan-2006
title: "Estimation of Copula-Based Semiparametric Time Series Models"
authors: ["Xiaohong Chen", "Yanqin Fan"]
year: 2006
citation_count: 1180
source_url: https://doi.org/10.1016/j.jeconom.2005.09.010
concept_tags: [copula, dependence-modeling]
superseded_by: null
coverage_quality: partial
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-07"
slot_justification: |
  Key reference for semiparametric copula estimation — avoids full parametric
  specification of marginals. Important when marginal distributions are unknown
  or misspecification risk is high.
---

## Core Methodology
Semiparametric estimation of copula models where marginal distributions are estimated nonparametrically (via empirical CDFs or kernel methods) while the copula is modeled parametrically. The pseudo-maximum-likelihood (PML) approach: (1) estimate marginal CDFs nonparametrically; (2) transform observations to pseudo-uniform using estimated marginals; (3) estimate copula parameters via maximum likelihood on the pseudo-observations.

## Key Results
- PML estimator is consistent and asymptotically normal under mild regularity conditions
- Avoids marginal misspecification bias — parametric marginals that are wrong propagate errors into copula estimation
- Efficiency loss relative to full MLE is small when marginals are correctly specified, but PML is robust when they are not
- The rank-based PML is particularly robust — uses only ranks, eliminating marginal estimation entirely
- Standard errors must account for the two-stage estimation — naive standard errors from the copula step are too small

## Stated Limitations
- Loses efficiency compared to correctly specified full MLE — the price of robustness
- Pseudo-observations create estimation noise that propagates to copula parameter estimates
- Asymptotic results require both sample size and smoothness conditions — finite-sample performance can differ from asymptotics
- Standard error correction is non-trivial — bootstrap is the practical solution
- Does not address copula model selection — only estimation within a chosen copula family

## Applicability Conditions
- Appropriate when: marginal distributions are unknown, complex, or likely misspecified
- Works best when: sample size is moderate to large (n > 200) for reliable nonparametric marginal estimation
- Degrades when: sample size is very small — nonparametric marginal estimates become noisy
- Key advantage: separates marginal estimation error from dependence estimation error
