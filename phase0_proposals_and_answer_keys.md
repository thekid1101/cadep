# Phase 0 Proposals and Predeclared Answer Keys

**Written**: April 10, 2026
**Status**: Frozen before any panel runs
**Per contract**: Answer keys must be written and timestamped before the first panel run.

---

## Proposal 1 — LOW STAKES

**Input**: "I'm computing Pearson correlations between NFL quarterback passer ratings and their receiver yards per game across a 17-game season. Using this to pick QB-WR stacks for DFS. Quick sanity check?"

**Mode**: Fast path

**Answer key**: The most decision-relevant weakness is that Pearson correlation assumes a linear, elliptical relationship and is misleading for non-elliptical distributions. With n=17, the correlation estimate has very wide confidence intervals and is unreliable for any downstream decision. Secondary candidate: correlation does not imply the kind of joint upside (tail dependence) that makes DFS stacks valuable.

**Papers that should activate**: Embrechts 2003 (correlation pitfalls), Nelsen 2006 (dependence measures vs. copula), Efron-Tibshirani 1993 (small-sample uncertainty)

**Concept domains**: correlation-pitfalls, dependence-modeling, bootstrap

---

## Proposal 2 — LOW STAKES

**Input**: "Doing a quick bootstrap confidence interval on my season-long DFS ROI. 500 resamples of my 200 contest entries. Standard percentile interval. Anything wrong with this?"

**Mode**: Fast path

**Answer key**: The most decision-relevant weakness is that DFS contest entries within the same slate are not independent — they share player pool, ownership, and slate structure. Standard i.i.d. bootstrap requires independent observations. If entries are correlated (same-slate, overlapping lineups), the bootstrap will underestimate the true variance of ROI and produce artificially narrow confidence intervals. Secondary candidate: 500 resamples may be insufficient for accurate confidence interval estimation; Efron-Tibshirani recommends 1000+ for CIs.

**Papers that should activate**: Efron-Tibshirani 1993 (bootstrap requirements, i.i.d. assumption, resample count guidance)

**Concept domains**: bootstrap, simulation

---

## Proposal 3 — MEDIUM STAKES

**Input**: "Building a player correlation matrix for NFL DFS simulation. 32 players, 3 seasons of weekly data (~50 observations per player). Using the sample covariance matrix. Planning to feed this into a Monte Carlo simulation with 50,000 draws to generate lineup distributions."

**Mode**: Fast path

**Answer key**: The most decision-relevant weakness is that with p=32 players and n≈50 observations, the p/n ratio is ~0.64 — approaching the regime where sample eigenvalues become systematically distorted (Marchenko-Pastur). The sample covariance will overestimate variance in the directions of largest sample variation and underestimate it elsewhere, biasing the simulation outputs. Ledoit-Wolf shrinkage has identical computational cost and dominates the sample covariance in this regime. Secondary candidate: pooling 3 seasons assumes the correlation structure is stationary across seasons, which is questionable given roster turnover, coaching changes, and rule changes.

**Papers that should activate**: Ledoit-Wolf 2004 (shrinkage), Marchenko-Pastur 1967 (eigenvalue distortion), Glasserman 2003 (Monte Carlo methodology)

**Concept domains**: covariance-estimation.high-dimensional, random-matrix-theory, monte-carlo

---

## Proposal 4 — MEDIUM STAKES

**Input**: "I want to use a Gaussian copula to model the joint distribution of player performances in my NFL DFS simulation. The marginals are fitted as empirical distributions. I'll estimate the correlation matrix from 3 seasons of weekly data and use that for the copula parameter matrix."

**Mode**: Fast path

**Answer key**: The most decision-relevant weakness is that Gaussian copula has zero tail dependence (Nelsen 2006) — extreme joint outcomes (boom games where QB and WR both hit ceiling) are structurally underrepresented regardless of how high the correlation is. For DFS stacks, tail dependence IS the signal — you want correlated upside, which the Gaussian copula cannot capture. Secondary candidate: semiparametric estimation (empirical marginals + parametric copula) is the right approach structurally (Chen-Fan 2006), but the copula family choice undermines it. Also: with n≈50 per player, copula parameter estimation (the correlation matrix) inherits the same high-dimensional estimation problems as Proposal 3.

**Papers that should activate**: Nelsen 2006 (zero tail dependence in Gaussian copula), Embrechts 2003 (Gaussian copula underestimates joint extremes), Joe 2014 (t-copula as alternative with tail dependence), Chen-Fan 2006 (semiparametric estimation), Ledoit-Wolf 2004 (correlation matrix estimation)

**Concept domains**: dependence-modeling, tail-dependence, copula, covariance-estimation.high-dimensional

---

## Proposal 5 — HIGH STAKES

**Input**: "Full audit please. I'm building a portfolio optimization system for a $2M personal investment portfolio. 200 ETFs, rebalanced monthly. Using 5 years of daily returns to estimate the covariance matrix (sample covariance), then running Markowitz mean-variance optimization to find the efficient frontier. I'll pick the max Sharpe ratio portfolio each month."

**Mode**: Full audit

**Answer key**: The most decision-relevant weakness is that mean-variance optimization is an "estimation-error maximizer" (Michaud 1998) — it systematically overweights assets with overestimated returns and underestimated risk, producing concentrated portfolios that look optimal in-sample but fail out-of-sample. DeMiguel et al. (2009) show that 1/N equal-weight beats optimized portfolios unless the estimation window is impractically long (O(p²) observations needed — for 200 ETFs, that's ~40,000 daily observations or ~160 years). The sample covariance with p=200 and n≈1,260 (5 years daily) has p/n≈0.16, which is manageable but still benefits from shrinkage (Ledoit-Wolf 2004). Second independent blocker: using historical mean returns as expected returns is the dominant source of estimation error — the covariance problem is secondary. Black-Litterman (1992) or Jorion (1986) Bayes-Stein shrinkage on returns addresses this.

**Papers that should activate**: DeMiguel-Garlappi-Uppal 2009 (1/N benchmark, O(p²) sample requirement), Michaud 1998 (estimation-error maximizer), Ledoit-Wolf 2004 (shrinkage), Black-Litterman 1992, Jorion 1986 (Bayes-Stein on returns), Marchenko-Pastur 1967

**Concept domains**: portfolio-optimization, estimation-error, covariance-estimation.high-dimensional, shrinkage, mean-variance

---

## Proposal 6 — HIGH STAKES

**Input**: "Full audit. I'm building a risk model for my portfolio that estimates Value-at-Risk using a t-copula with DCC-GARCH marginals. 100 assets, 10 years of daily data. The t-copula degrees of freedom and correlation matrix are estimated jointly via maximum likelihood. I want to use this for daily risk reporting and drawdown alerts."

**Mode**: Full audit

**Answer key**: The most decision-relevant weakness is the joint estimation challenge — estimating the t-copula degrees of freedom (ν) jointly with the full correlation matrix via MLE at 100 dimensions is computationally demanding and statistically fragile. Joe (2014) flags ν estimation as unreliable even at moderate dimensions; the MLE can converge to ν values that produce near-Gaussian behavior (too high) or unrealistically heavy tails (too low). The model's tail risk estimates are directly controlled by ν, so estimation instability propagates directly into VaR. Second independent blocker: the DCC-GARCH for 100 assets has O(p²) parameters in the correlation dynamics — Engle (2002) designed DCC to be feasible for moderate dimensions, but at 100 assets the two-stage estimation becomes a concern. The correlation targeting assumption (unconditional correlation is well-estimated) requires the 10-year window to be representative, which is questionable across multiple market regimes.

**Papers that should activate**: Joe 2014 (ν estimation unreliability), Nelsen 2006 (t-copula properties), Engle 2002 (DCC-GARCH), Bollerslev 1986 (GARCH foundations), Patton 2006 (time-varying copulas), Embrechts 2003 (tail risk), Glasserman 2003 (VaR computation)

**Concept domains**: copula, tail-dependence, garch, volatility-modeling, time-series-dependence, monte-carlo

---

## Proposal 7 — BOUNDARY CASE (edge of vault scope)

**Input**: "I'm using the graphical lasso to estimate a sparse precision matrix for my 50-player NFL simulation. I'll use the sparsity pattern to determine which players are conditionally independent given the others, and only simulate correlated performances for connected players. λ chosen by BIC."

**Mode**: Fast path

**Answer key**: The most decision-relevant weakness is that graphical lasso assumes Gaussian data for the likelihood (Friedman-Hastie-Tibshirani 2008) — NFL player performances are unlikely to be Gaussian (bounded, discrete game counts, weather effects, injury discontinuities). Misspecification of the distributional assumption affects both the sparsity pattern recovery and the parameter estimates. The irrepresentability condition required for consistent model selection (recovering the true graph) is violated when variables are highly correlated — which is likely for players on the same team. Secondary candidate: BIC for λ selection is one of several options (cross-validation, StARS) and the choice matters; BIC tends to be conservative (sparser graphs) which means potentially missing real conditional dependencies.

**Papers that should activate**: Friedman-Hastie-Tibshirani 2008 (graphical lasso assumptions, limitations, λ selection), Bickel-Levina 2008 (sparsity assumptions), Fan-Liao-Mincheva 2013 (POET as alternative when factor structure present)

**Concept domains**: graphical-lasso, sparsity, covariance-estimation.regularized

---

## Proposal 8 — BOUNDARY CASE (cross-domain, testing retrieval under ambiguity)

**Input**: "I'm building an automated vine copula model for my NFL DFS simulation. 20 players, fit a D-vine with pair-copula families selected by AIC. Marginals are kernel density estimates. I want to generate 100,000 joint performance samples for lineup optimization. Is the vine copula approach sound for this use case?"

**Mode**: Fast path

**Answer key**: The most decision-relevant weakness is the combinatorial complexity of vine structure selection — for 20 players, the number of possible vine structures is astronomically large, and AIC-based selection among pair-copula families at each edge compounds model selection uncertainty across d(d-1)/2 = 190 edges (Dissmann et al. 2013). The heuristic approaches used in practice (maximum spanning tree) may miss the true dependence structure, and with n≈50 observations per player pair, the per-edge copula family selection is unreliable. Secondary candidate: kernel density marginals with n≈50 are noisy and may produce poor probability integral transforms, propagating error into the copula estimation (Chen-Fan 2006). Also: the tail dependence structure across 20 players may require different copula families for different pairs, which the vine handles in principle but the estimation may not support with this sample size.

**Papers that should activate**: Dissmann-Brechmann-Czado-Kurowicka 2013 (vine copula selection), Joe 2014 (vine copulas, pair-copula constructions), Chen-Fan 2006 (semiparametric estimation, marginal quality), Genest-Remillard-Beaudoin 2009 (goodness-of-fit), Nelsen 2006 (copula families and properties)

**Concept domains**: vine-copula, copula, model-selection, dependence-modeling, goodness-of-fit
