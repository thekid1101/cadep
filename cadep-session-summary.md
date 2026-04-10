# CADEP Session Summary — April 10, 2026

## What We Built Today

We shipped a working version of CADEP (Cross-Domain Adversarial Expert Panel) as a Cowork skill that runs entirely within the Claude subscription — no API costs, no code deployment. The system provides grounded, citation-backed adversarial review of technical proposals, designed to surface real problems before you commit to an approach.

The core pipeline is Specialist (finds problems with citations) → Devil's Advocate (attacks from four angles without citations) → Synthesizer (ranks objections, preserves disagreement, never recommends). Two output modes: a three-field fast path for quick checks and a full audit with diagnostics, provenance tagging, and a friction question that forces genuine engagement.

The knowledge base expanded from 10 papers to 29 papers across 7 sub-domains: covariance estimation (Ledoit-Wolf series, Bickel-Levina, graphical lasso), random matrix theory (Marchenko-Pastur, Johnstone, Bai-Silverstein, El Karoui), copula and dependence modeling (Sklar through vine copulas), time series dependence (GARCH, DCC, dynamic copulas), Monte Carlo and simulation, bootstrap methods, and portfolio optimization (1/N benchmark, resampled frontiers, Bayes-Stein, Black-Litterman).

The PRD was updated to v2.0 addendum, documenting the architectural evolution from flat vaults to a hierarchical knowledge graph. This is the strategic blueprint for scaling CADEP from a proof-of-concept to a system with genuine depth of knowledge.

---

## Key Architecture Decisions

**Hierarchical knowledge graph over flat lookup.** The vault is now a 4-layer directed acyclic graph: foundations (estimation theory, probability) → methodological families (simulation, dependence, optimization) → specific techniques (copulas, Monte Carlo, shrinkage) → application domains (DFS, portfolio, financial risk). When a query arrives, the system walks the tree — a copula question pulls copula papers, the simulation methodology context, AND the estimation theory foundations underneath. This is how real expertise works.

**Adversarial routing table.** Seven common wrong claims are mapped directly to the papers that disprove them. "Sample covariance is fine" routes to Ledoit-Wolf and Marchenko-Pastur. "Gaussian copula captures the dependence" routes to Embrechts and Nelsen on zero tail dependence. The system doesn't just find relevant papers — it actively looks for counter-evidence when it detects overconfident claims.

**Full graph: 24 nodes, 155 papers identified.** The current 29 papers are the foundation. The complete knowledge graph has been designed with 24 nodes and 155 unique papers mapped across them. This is the roadmap, not a wish list — each paper has a slot justification tied to specific routing paths.

**Subscription-native tradeoffs.** Running as a Cowork skill instead of API means no model routing (single model handles all roles sequentially), no parallel execution, and prompt-based discipline instead of code-enforced constraints. What we gain: zero marginal cost, faster iteration (edit a markdown file vs. deploy code), visibility into intermediate work on request, and vault expansion by adding files rather than changing code.

---

## What's Next

**Phase 1 — Vertical slice (~60-70 papers).** Build out the copula → simulation → optimization → DFS path end-to-end. This covers the primary work domain and delivers roughly 40% of the full graph's value. The goal is a system that can genuinely push back on proposals in this vertical with the kind of depth that catches errors a surface-level review would miss.

**Phase 2 — Foundation layer.** Fill in estimation theory and probability foundations. These papers are referenced adversarially across multiple technique nodes — they're the bedrock that makes cross-domain critique possible.

**Phase 3 — Remaining techniques and application domains.** Factor models, extreme value theory, Bayesian computation, sports analytics methodology, and contest strategy.

**Open architectural questions.** Should the skill graph use wikilink-style progressive disclosure (index → map of content → paper) or flat routing? What's the optimal number of papers to read per query before context dilution kicks in? How do we validate vault paper accuracy at 155 papers when manual spot-checks don't scale? These get resolved through Phase 1 testing.

The north star: a system where every critique is backed by specific evidence, every objection is falsifiable, and the depth of knowledge is sufficient that "I don't know" is more trustworthy than a guess with citations.
