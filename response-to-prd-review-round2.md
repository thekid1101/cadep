Every point here makes the Phase 0 design more rigorous. Let me address each one with specific commitments.

**Point 1 — DA anchoring, not just DA difference.**

You're right that "different" is the wrong metric. The DA could produce textually different objections that are still anchored to the specialist's frame — attacking adjacent angles rather than genuinely independent ones. The test I proposed would pass a DA that reads the specialist's output, thinks "they covered eigenvalue distortion, so I'll attack stationarity instead," and calls that independent. It's not. It's derivative framing with different vocabulary.

Revised test design: for each of the 8 proposals, a blind rater evaluates the DA output on two dimensions — (a) does the DA attack assumptions the specialist didn't touch, and (b) does the DA's framing feel independent or derivative of the specialist's framing? I'll also add a structural check: count how many DA objections share key terms or concepts with the specialist output. If the prompt-separated DA's objection vocabulary overlaps with the specialist by more than the structurally-separated DA's does, anchoring is present regardless of whether the literal objections are "different."

Pass criteria: the prompt-separated DA must score within 1 standard deviation of the structurally-separated DA on both independence dimensions across the 8 proposals. If it doesn't, prompt separation is insufficient for this role.

**Point 2 — Citation clustering needs a predeclared threshold.**

Agreed. Setting it now:

≥75% of citations in each panel output must come from papers in the query's primary concept domain (as defined by the concept_index.json routing). If a copula query produces 6 citations and 2 are from portfolio optimization papers with no clear relevance to the copula question, that's a fail even though the total citation count looks healthy.

On the test set coverage: you're right that if none of the 8 proposals touch portfolio optimization, those papers get a free ride. I'll ensure at least one of the 8 proposals is portfolio-adjacent (e.g., "building a minimum-variance portfolio with 200 assets and 2 years of data") so the portfolio papers are either correctly activated or exposed as vault bloat.

For papers that aren't triggered by any of the 8 proposals, I'll flag them as "untested, provisionally included" rather than treating silence as validation.

**Point 3 — 155-paper graph: confirmed, build timeline removed entirely.**

Not disclaimed. Removed. The architecture document becomes a reference for what the knowledge graph looks like when fully populated. No phases, no timelines, no sprint estimates. It gets a build timeline when Phase 0 results justify scaling.

**Point 4 — Predeclared thresholds, written before test runs.**

Setting them now, in writing, before seeing any data:

- Drift rate: recommendation language in ≤10% of outputs. Above 10%, the constrained-critic contract is not holding.
- Vault citation compliance: ≥90% of citations reference actual vault papers. Below 90%, the grounding claim is false.
- Format compliance: fast-path outputs contain exactly 3 fields in ≥90% of runs. Below 90%, the output contract is broken.

These go into the Phase 0 criteria document today. If I see the data first and then set thresholds, I'll set them to pass. That's exactly the kind of motivated reasoning CADEP is supposed to prevent.

**Point 5 — Provenance threshold tightened to ≤10%.**

You're right that 20% is too lenient for the thing the PRD calls "the most dangerous form of epistemic leakage." Revised:

- Fast path: ≤10% of outputs may contain unsourced numeric claims.
- Full audit: 0% tolerance. Any unsourced numeric claim in a full-audit output is a critical failure. Full audit is the high-trust mode. If the system produces crisp unsourced numbers in the mode designed to look most authoritative, the trust model is inverted.

**Point 6 — Friction independence needs an operational test.**

Defining it now: for each of the 8 full audits, after receiving the friction question, I answer this meta-question: "Does this question challenge my acceptance of the output, or does it merely ask me to restate what the output already concluded?"

Pass criteria: ≥50% of friction questions must challenge acceptance rather than restate conclusions. Below 50%, friction independence has failed in the Cowork implementation and the mechanism is providing false comfort rather than genuine challenge.

I'll also track whether friction questions ever reference DA concerns that the synthesizer downweighted or omitted. If friction consistently reinforces the synthesizer's ranking rather than surfacing things the synthesizer chose not to emphasize, the same-context-window problem is leaking into friction generation.

**The pre-commitment question: what happens if Cowork passes Phase 0?**

This is the most important point in the entire review and I'm glad you raised it before results arrive. Writing it down now:

If the Cowork skill passes Phase 0 on all behavioral criteria, we still build the following enforcement mechanisms in the API version:

1. **Structural agent separation** — because passing Phase 0 on 8 proposals doesn't prove prompt separation holds at scale. The first time the model gets a long, complex proposal with dense specialist output, the DA anchoring risk goes up. Structural separation is insurance against the tail cases we haven't tested.

2. **Code-enforced drift scanner and output parser** — because prompt-based compliance at 90%+ on 8 runs doesn't mean 90%+ on 200 runs. Deterministic enforcement doesn't degrade with scale. Prompt compliance might.

3. **Provenance tagging parser** — because the full-audit zero-tolerance threshold for unsourced numerics cannot be reliably maintained by prompt instruction alone over time.

What we accept as sufficient in the Cowork version if Phase 0 passes:

- The behavioral patterns (specialist → DA → synthesizer pipeline, adversarial routing, friction questions) are validated as producing decision-relevant critique.
- The vault structure and concept routing work well enough that the right papers get cited.
- The Cowork skill is a legitimate tool for personal use where the operator (me) provides the enforcement layer that the code doesn't.

What we do NOT accept: that the Cowork skill is deployable to other users without code-enforced mechanisms. If it ever serves anyone besides me, the API version's enforcement is mandatory because other users won't know which outputs to distrust.

This is written down before Phase 0 runs. It stays written down after.
