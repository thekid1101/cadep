# Vault: stats-hd-estimation

## Covers
- Covariance matrix estimation (shrinkage, graphical lasso, sparse covariance, POET/factor-based, random matrix theory)
- Copula modeling (parametric, semiparametric, tail dependence, vine copulas, time-varying copulas, goodness-of-fit)
- Bootstrap and simulation methods (bootstrap, Monte Carlo, variance reduction, importance sampling, MCMC, rare-event simulation)
- Dimensionality constraints (p >> n, small-sample estimation, eigenvalue behavior)
- Random matrix theory (Marchenko-Pastur, Tracy-Widom, spectral analysis, nonlinear shrinkage)
- Portfolio optimization under estimation error (1/N benchmarks, resampled frontiers, Bayes-Stein, Black-Litterman)
- Time series dependence (GARCH, DCC, dynamic copulas)
- Model selection for copulas (goodness-of-fit tests, vine copula structure selection)

## Does Not Cover
- Bayesian estimation beyond Black-Litterman (future vault if project work demands)
- Robust estimation / M-estimators (future vault)
- General machine learning (future vault)
- Time series forecasting (out of scope)
- Options pricing / derivatives (out of scope)

## Boundary Cases
- Regularization: covered when applied to estimation; not covered as general optimization
- Simulation: covered both for validating estimators and as standalone Monte Carlo methodology
- Portfolio optimization: covered as motivation for estimation quality; not covered as standalone asset management
- GARCH/DCC: covered as inputs to covariance estimation; not covered as standalone forecasting tools
- Bayesian methods: covered when directly applied to portfolio estimation (Jorion, Black-Litterman); not covered as general inference framework
