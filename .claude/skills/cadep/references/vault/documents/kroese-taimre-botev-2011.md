---
doc_id: kroese-taimre-botev-2011
title: "Handbook of Monte Carlo Methods"
authors: ["Dirk P. Kroese", "Thomas Taimre", "Zdravko I. Botev"]
year: 2011
citation_count: 976
source_url: https://doi.org/10.1002/9781118014967
concept_tags: [monte-carlo, variance-reduction, simulation, rare-event-simulation]
superseded_by: null
coverage_quality: full
math_syntax_status: unverified
cadep_citation_count: 0
last_verified: "2026-04-10"
slot_justification: |
  Modern handbook covering Monte Carlo methods with emphasis on rare-event
  simulation and cross-entropy methods. Fills the gap between Glasserman's
  finance focus and Robert-Casella's Bayesian focus with algorithmic coverage.
---

## Core Methodology
Practical handbook covering the full spectrum of Monte Carlo methods with emphasis on algorithmic implementation. Covers random variable generation, permutation and combinatorial sampling, Markov chain Monte Carlo, the cross-entropy (CE) method for importance sampling optimization, splitting methods for rare-event probability estimation, kernel density estimation in Monte Carlo contexts, and randomized optimization. The cross-entropy method iteratively updates the importance sampling distribution by minimizing the KL divergence to the optimal zero-variance importance distribution, using samples from the current proposal.

## Key Results
- Cross-entropy method provides a systematic algorithm for finding near-optimal importance sampling distributions by iteratively minimizing KL divergence
- Splitting method for rare-event estimation: decompose a rare event into nested less-rare events and estimate conditional probabilities sequentially
- Variance minimization framework for choosing among variance reduction techniques based on problem structure
- Adaptive importance sampling convergence guarantees under regularity conditions (consistency of the CE estimator)
- Kernel density estimation provides nonparametric estimates of the sampling distribution that can improve subsequent MC steps
- Practical algorithms for combinatorial optimization via randomized search (simulated annealing, CE optimization)

## Stated Limitations
- Cross-entropy method can converge to suboptimal importance sampling distributions in multimodal problems
- Splitting requires careful threshold selection; poor thresholds lead to inefficient estimation or high variance
- Adaptive methods may not converge in highly irregular problems where the landscape of the objective changes rapidly
- Most variance reduction guarantees are asymptotic — finite-sample performance requires empirical validation
- The CE method's convergence theory assumes the parametric family contains a good approximation to the optimal proposal
- Rare-event simulation remains inherently challenging when the rare event has no natural decomposition into nested events

## Applicability Conditions
- Appropriate when: estimating rare-event probabilities (extreme portfolio losses, tail risk), optimizing under uncertainty, designing efficient simulation studies
- Works best when: the rare event can be decomposed into nested events (splitting), the parametric family for CE includes a good proposal, problem dimension is moderate
- Degrades when: the rare event has no natural decomposition, the parametric CE family is too restrictive, problem dimension is very high without exploitable structure
- Not appropriate for: routine Monte Carlo estimation where standard techniques suffice, problems where importance sampling is unnecessary (well-behaved, moderate-probability events)
