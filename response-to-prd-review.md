Thanks for this. You're right on every structural point and I need to own that rather than argue around it. Let me go through each one.

**1. Single model kills structural independence — agreed, this is the central question.**

You're correct that calling this a "tradeoff" understates it. The PRD's agent separation wasn't a nice-to-have architectural choice — it was the mechanism that prevented the DA from being contaminated by the specialist's framing and prevented the synthesizer from cherry-picking across the full context. In the Cowork skill, all three roles share a context window. The DA "not knowing" what the specialist found is now a prompt instruction, not a structural guarantee.

I should have flagged this as an open validation question rather than a settled tradeoff. Here's what I'll add to the Phase 0 criteria: run the same 8 proposals through both the API version (structural separation) and the Cowork skill (prompt separation), blind-score both using the existing severity rubric, and specifically measure whether the DA produces meaningfully different objections when it can't see the specialist output vs. when it technically can but is told not to reference it. If prompt separation produces measurably weaker DA output, the Cowork skill is a convenience tool, not the product.

**2. Vault scope creep — you're right, I expanded without acknowledging the expansion.**

The original vault was scoped to "high-dimensional estimation and dependence modeling." I added portfolio optimization (4 papers), time series dependence (3 papers), and Monte Carlo simulation (3 papers) without updating the scope document or justifying the expansion against the 25-paper cap. That's exactly the vault creep the cap was designed to prevent.

The honest framing: we expanded the vault from 10 to 29 papers because 10 felt too thin to produce useful critique. But "felt too thin" isn't a valid justification when the PRD explicitly says to earn expansion through proven need. The right move is to freeze the vault at the current 29, run Phase 0 evals, and let the results tell us whether the additional domains actually improve critique quality or just add context noise. If the portfolio optimization papers never get cited in the first 8 proposals, they don't belong in the vault yet.

I'll also add the "lost in the middle" concern as a Phase 0 measurement: are the right 3-4 papers getting attention in each review, or is the model distributing attention across all 29? This is testable by checking whether citations cluster on the relevant papers or scatter.

**3. 155 papers is a long-term architecture document, not a near-term build target.**

Full stop. I got ahead of myself. The knowledge graph design is a roadmap that shows where the system could go if Phase 0 succeeds. Framing it as a phased build plan with timelines implied commitment to scaling before we've proven the core loop works. The PRD's "earn complexity" principle applies here: the 155-paper graph gets built when the 29-paper vault has proven it changes decisions. Not before.

I'll relabel the architecture document accordingly and remove the build timeline.

**4. The three "remaining issues" are architectural gaps, not prompt engineering challenges.**

This is the point I most need to concede cleanly. Let me restate what's actually happening:

- **Drift scanner**: The PRD has regex enforcement that strips recommendation language. The Cowork skill has a prompt instruction that says "don't use recommendation language." These are not equivalent. One is deterministic, the other is probabilistic. The skill will drift.

- **Vault-only citations**: The PRD gives specialists only vault documents as context. The Cowork skill gives the model its full training data plus vault documents plus a prompt instruction to only cite vault papers. The model will cite outside the vault because there's no structural boundary preventing it.

- **Output parser**: The PRD strips non-compliant fast-path content via code. The Cowork skill asks the model to self-comply. It won't always comply because self-regulation is exactly the kind of task LLMs are inconsistent at.

Calling these "prompt engineering challenges" was minimizing real risk. I'll reclassify them as validation risks in the Phase 0 criteria with specific measurements: drift rate (% of outputs containing recommendation language), vault citation compliance (% of citations that reference actual vault papers vs. training data), and format compliance (% of fast-path outputs that contain exactly 3 fields with no extras).

If any of these rates are below acceptable thresholds, the Cowork skill needs compensating mechanisms — even if those mechanisms are imperfect prompt-based versions of the code-enforced originals.

**5. Provenance tagging has no enforcement layer — correct.**

The skill instructs the model to tag numeric claims. There's no parser to flag violations. In the API version, the parser catches [unsourced] tags and flags them. In the Cowork version, the model might tag, might not, and there's no second pass to catch what it misses.

I'll add provenance compliance to the Phase 0 measurements: manually check the first 8 proposals for unsourced numeric claims that slipped through without tags. If the rate is above 20%, the skill needs a more aggressive prompting strategy or an explicit "review your output for unsourced numbers before presenting" self-check step.

**6. Friction mechanism independence is collapsed — correct.**

The PRD designed friction as a separate Haiku call specifically so the system challenging the operator is independent from the system that produced the critique. In the Cowork skill, the same model in the same context generates both the critique and the friction question. The question is structurally biased toward the critique it just produced.

This is a real degradation. The mitigation in the Cowork version is that friction questions are generated from a priority list (conflicts first, then unresolved DA attacks, etc.) which adds some structure. But the independence guarantee is gone. I'll flag this in the "what we lost" section and note that if friction questions consistently align with the synthesizer's framing rather than challenging it, the mechanism isn't working.

**Overall: reframing the v2.0 addendum.**

You're right that the addendum frames the Cowork skill as equivalent-with-tradeoffs when it's actually a reduced-fidelity prototype that trades structural enforcement for speed and cost. I'll rewrite the addendum to include:

1. A "What We Lost" section listing every PRD mechanism absent from the Cowork implementation
2. The three "prompt engineering challenges" reclassified as validation risks with specific Phase 0 measurements
3. Explicit framing of prompt-simulated agent separation as an unvalidated hypothesis
4. The 155-paper graph relabeled as long-term architecture, not near-term build target
5. Retrieval quality measurement criteria for the expanded vault
6. An honest assessment of the distance between current implementation and the north star

The Cowork skill is worth building because it gets Phase 0 running at zero marginal cost with fast iteration. But it needs to be honest about what it is: a rapid prototype that tests whether the behavioral patterns work, not a production system that enforces them. The API version remains the path to structural enforcement. The Cowork version tells us whether the enforcement is worth building.
