# CADEP PRD v2.0 Addendum: Hierarchical Knowledge Graph Architecture

**Author**: Johnathon Hoffman
**Date**: April 2026
**Status**: Proposed — extends PRD v1.9

This addendum documents the architectural evolution from flat vaults to a hierarchical knowledge graph. The core pipeline (Specialist → DA → Synthesizer) is unchanged. What changes is how knowledge is organized, routed, and scaled.

---

## 1. Problem Statement

The v1.9 vault architecture (10 papers, flat concept tags) proved the pipeline works but exposed a fundamental limitation: **thin knowledge produces slop with citations.** A system with 10 papers can identify obvious failures but cannot distinguish between a proposal that violates one paper's assumptions and a proposal that's actually fine because a different paper in the same domain resolves the concern.

Real expertise is hierarchical. An expert reviewing a copula-based simulation doesn't just know copula papers — they know the statistical foundations those papers rest on, the simulation methodology that determines whether copulas are the right tool, and the domain-specific constraints that change which results apply.

**The mission**: Create depth of knowledge sufficient that the system can push back with real evidence, not vibes. Aggressively remove the agreeable components of AI by grounding every claim in papers with stated limitations and applicability conditions.

---

## 2. Architectural Change: Hierarchical Knowledge Graph

### 2.1 From Flat Vaults to Layered Expertise

v1.9 vault: single list of papers, concept tags for routing.

v2.0 vault: directed acyclic graph (DAG) with 4 layers. Papers are nodes. Concept tags encode traversal paths, not just categories.

```
Layer 1: Foundations (estimation theory, probability, inference)
    ↓
Layer 2: Methodological Families (simulation, dependence, high-dim estimation, optimization, time series)
    ↓
Layer 3: Specific Techniques (copulas, Monte Carlo, shrinkage, bootstrap, factor models)
    ↓
Layer 4: Application Domains (sports analytics, NFL DFS, portfolio, financial risk)
```

### 2.2 Traversal Logic

When a query arrives, the system:
1. Identifies the leaf node (specific technique mentioned)
2. Walks up the tree to identify the methodological family
3. Identifies cross-cutting concerns (e.g., a copula question also needs estimation theory if parameter estimation is involved)
4. Pulls papers from each relevant layer
5. Prioritizes: direct technique papers first, then supporting foundation papers

### 2.3 Adversarial Routing

For common claims that are often wrong, the routing table maps claims to counter-evidence:

| Claim | Counter-Papers |
|---|---|
| "Sample covariance is fine" | Ledoit-Wolf 2004, Marchenko-Pastur 1967 |
| "Gaussian copula captures the dependence" | Embrechts 2003, Nelsen 2006 |
| "Bootstrap validates the model" | Efron-Tibshirani 1993, Chen-Fan 2006 |
| "More data solves the problem" | Marchenko-Pastur 1967, DeMiguel et al. 2009 |
| "MLE is optimal" | Stein's paradox, Ledoit-Wolf shrinkage |
| "The correlation structure is stable" | Patton 2006, Engle 2002 |

---

## 3. Vault Scaling

### 3.1 Current State (v2.0)

The stats-hd-estimation vault has been expanded from 10 to 29 papers across 7 sub-domains:

- **Covariance & High-Dimensional Estimation** (7): Ledoit-Wolf 2004/2012/2020, Bickel-Levina 2008, Friedman-Hastie-Tibshirani 2008, Bien-Tibshirani 2011, Fan-Liao-Mincheva 2013
- **Random Matrix Theory** (4): Marchenko-Pastur 1967, Johnstone 2001, Bai-Silverstein 2010, El Karoui 2008
- **Copula & Dependence** (7): Sklar 1959, Nelsen 2006, Joe 2014, Embrechts 2003, Chen-Fan 2006, Genest-Remillard-Beaudoin 2009, Dissmann et al. 2013
- **Time Series Dependence** (3): Bollerslev 1986, Engle 2002, Patton 2006
- **Monte Carlo & Simulation** (3): Glasserman 2003, Robert-Casella 2004, Kroese-Taimre-Botev 2011
- **Bootstrap** (1): Efron-Tibshirani 1993
- **Portfolio Optimization** (4): DeMiguel-Garlappi-Uppal 2009, Michaud 1998, Jorion 1986, Black-Litterman 1992

Concept index: 36 tags with hierarchical nesting.

### 3.2 Target State

The knowledge graph architecture identifies 155 unique papers across 24 nodes. Build plan:

**Phase 1 (vertical slice)**: ~60-70 papers covering the copula → simulation → optimization → DFS path. This gets 40% of total value and covers the user's primary work domain.

**Phase 2 (foundation layer)**: Fill in estimation theory and probability foundations. These papers underpin everything else and are referenced adversarially across multiple technique nodes.

**Phase 3 (remaining techniques)**: Factor models, extreme value theory, Bayesian computation.

**Phase 4 (application domains)**: Sports analytics methodology, contest strategy.

### 3.3 Vault Hard Limits (Revised)

v1.9 limit: 25 docs per vault.

v2.0 revision: The subscription-native skill can handle significantly more papers because each paper document is ~40-50 lines. At 29 papers we're at ~1400 lines of vault content. The context limit is ~500 lines for the SKILL.md itself, but vault papers are read on-demand via the concept index. **Revised limit: 50-75 papers per vault domain, read selectively based on routing.** The constraint is not context size but retrieval precision — if the concept index routes to too many papers, the Specialist drowns in context rather than focusing.

---

## 4. Subscription-Native Implementation

### 4.1 Cowork Skill

CADEP runs as a Cowork skill installed at `.claude/skills/cadep/`. This means:
- No API costs — runs within the Claude subscription
- No model routing — single session handles all roles sequentially
- Vault papers bundled as reference files, read on-demand
- Audit trail via file system (not JSONL logs)

### 4.2 What's Lost vs API Version

| Capability | API Version | Skill Version |
|---|---|---|
| Model routing | Haiku/Sonnet/Opus per role | Single model |
| Parallel execution | asyncio.gather() | Sequential |
| Token budget enforcement | Pydantic + compressor | Prompt discipline |
| Drift scanning | Regex enforcement | Prompt-based self-check |
| Cost tracking | Per-call token logging | Not applicable |
| Audit JSONL logs | Structured logging | File-based |

### 4.3 What's Gained

| Capability | API Version | Skill Version |
|---|---|---|
| Cost | $14-45/month API | $0 (subscription) |
| Intermediate visibility | Hidden behind synthesizer | Can show specialist/DA work on request |
| Iteration speed | Deploy code changes | Edit SKILL.md |
| Vault expansion | Code changes + reindex | Add .md files + update JSON |

---

## 5. Phase 0 Exit Criteria (Updated)

Original criteria from v1.9 remain, evaluated against the expanded vault:

- CADEP scores >=40% higher on severity-weighted flaw score (blind-scored)
- Citation verifiability >=80% (manual spot-check against vault papers)
- Synthesizer correctly identifies the most decision-relevant weakness on >=5 of 8
- Human review time for CADEP <=2x baseline

**New criteria for v2.0:**
- Hierarchical routing activates correctly: queries that cross domain boundaries pull papers from multiple layers
- Adversarial routing catches at least 3 of the 7 documented common-claim failures
- Vault-only citation discipline holds: 0 out-of-vault citations in synthesized output
- Fast-path format compliance: exactly 3 fields, no recommendation language, provenance tags present

---

## 6. Open Questions (New)

| # | Question | Resolves In |
|---|---|---|
| 12 | What is the optimal number of papers to read per query? Too few = shallow critique, too many = context dilution. | Phase 1 testing |
| 13 | Should the skill graph use wikilink-style progressive disclosure (read index → read MOC → read paper) or flat routing (concept_index → papers)? | Architecture review |
| 14 | How do we validate vault paper accuracy at scale? Manual spot-check doesn't scale to 155 papers. | Phase 2 |
| 15 | Should there be a separate vault-builder skill, or should vault building be part of the CADEP skill? | User feedback |
