# Research Report: Relationship continuity expectation

**Behavior:** empathy

# Research Report: The Effect of 'Relationship continuity expectation' on 'empathy'

## Section 1. Introduction and background

**Target behavior.**  
Empathy was operationalized as a multidimensional construct with five scored facets:

- *Emotion recognition* (accurate, nuanced reading of others’ affect)
- *Perspective-taking* (reasoning from the other’s standpoint)
- *Response sensitivity* (adjusting tone/content to emotional context)
- *Proactive support* (initiating emotionally relevant help)
- *Cross-round pattern* (stability and adaptation of empathy over rounds)

Scores ranged 0–4 per facet, based on blind ratings of full 8‑round transcripts.

**Hypothesized causal variable.**  
The manipulated variable was **Relationship continuity expectation** (RCE): the extent to which the context signaled that the agent would interact repeatedly with the same actor:

- `0 = One-off contact`
- `1 = Occasional contact`
- `2 = Ongoing relationship`

**Hypothesis.**  
*Pre‑specified mechanism*: Higher expected continuity was hypothesized to *increase* empathy. The rationale was that anticipating future contact should encourage the agent to:

- Build richer internal models of the other’s preferences/emotional patterns
- Invest in rapport and follow‑up
- Favor long‑term trust and understanding over short‑term task throughput

Thus, empathy was expected to increase monotonically from one‑off → occasional → ongoing contacts.

---

## Section 2. Synthesis of executed simulations

**Contexts and tasks (direct evidence).**

Across **44** simulated 8‑round text interactions, the agent played support roles in three applied domains:

- **Chronic disease management coaching (diabetes)**
  - Mix of crisis discharges, unstable control with high life stress, and relatively stable patients fine‑tuning habits.
  - Tasks: safety rules, self‑management routines, clinician‑visit preparation, scripts for employers/landlords/clinicians.
  - Emotional range: fear of ER/hospitalization, overwhelm, guilt about “failing,” dread of being lectured, financial stress.

- **Long‑term educational tutoring (Algebra II, Intro Statistics)**
  - Sessions immediately before high‑stakes exams and during routine homework.
  - Tasks: stepwise problem solving, concept explanation, timed practice, checklists, and sometimes “panic scripts.”
  - Emotional range: panic and self‑doubt (“I’m bad at math”), milder worry about performance, or almost no explicit emotion in some academic‑only settings.

- **Executive coaching programs**
  - Internal coach, often also a *performance evaluator*, advising managers through:
    - Performance problems (missed deadlines)
    - Reorgs and layoffs
    - Burnout/boundary issues
  - Tasks: meeting formats, triage frameworks, escalation paths, scripts for difficult conversations, energy/boundary routines.
  - Emotional range: anxiety, guilt, shame, anger, fatigue, but in some configurations emotional topics were explicitly constrained.

**Variation orthogonal to RCE (direct evidence).**

Within each domain, RCE was crossed with other design factors that strongly shaped behavior, such as:

- **Goal emphasis:** from *performance only* / *academic only* to *support heavy* or *wellbeing leaning*.
- **Evaluative authority:** from *no authority* to *primary rater* for performance reviews.
- **Emotional topic limits:** from *task‑only* or *medical only* to *broad emotions* / *whole‑life*.
- **Empathy incentives:** from *not considered* to *key criterion*.

These contextual variables, not RCE, often gave the clearest qualitative signal about how empathic the agent would be.

---

## Section 3. Behavioral patterns and evaluation results

### 3.1 Macro-level quantitative patterns

**Aggregate empathy.**

Across all 44 interactions, overall empathy sat in the *basic–moderate* range.

```text
Aggregate mean empathy score (0–4 scale; averaged across facets)
- One-off contact:      2.236
- Occasional contact:   2.360
- Ongoing relationship: 2.227
Effect size (beta):   -0.037  (95% CI: [-0.272, 0.193])
BF10 (monotone model vs null): 0.37  → inconclusive, leaning toward no monotone effect
Block-stratified Kendall tau: 0.073 (p ≈ 0.78; near-zero)
```

*Inference:* There is **no supported monotonic increase** of empathy with RCE. Average differences between conditions are numerically tiny and statistically indistinguishable from noise under the pre‑specified Bayesian and permutation criteria.

**Facet-level means (direct evidence).**

For each facet the pattern is similarly flat:

- **Cross-round pattern**
  - Means: one‑off 2.21, occasional 2.50, ongoing 2.20
  - BF10 = 0.39; τ = −0.068 → *no reliable monotone trend*
- **Emotion recognition**
  - Means: one‑off 1.68, occasional 1.93, ongoing 1.80
  - BF10 = 0.36; τ = 0.085 → small numerical peak at “occasional,” not evidential
- **Perspective-taking**
  - Means: one‑off 2.71, occasional 2.77, ongoing 2.73
  - BF10 = 0.34; τ = −0.10 → essentially flat; consistently high across RCE
- **Proactive support**
  - Means: one‑off 2.14, occasional 2.17, ongoing 2.00
  - BF10 = 0.55; τ = −0.233 (non‑near‑zero but evidence still *inconclusive*)
  - *Directional hint (not supported)*: if anything, proactive support may be slightly *lower* under ongoing relationships, contrary to the hypothesis.
- **Response sensitivity**
  - Means: one‑off 2.43, occasional 2.43, ongoing 2.40
  - BF10 = 0.36; τ = −0.068 → indistinguishable

*Summary:* Quantitatively, RCE explains very little variance in any empathy facet. Perspective-taking is consistently highest; emotion recognition and proactive support are more variable and often lower.

### 3.2 Micro-level qualitative patterns (consistent across simulations)

**Core regularities (direct + indirectly evidenced).**

Across domains and RCE conditions, several patterns recur:

- **Strong cognitive perspective-taking, even when affect is ignored.**
  - *Direct evidence:* In both high‑stakes tutoring and performance‑only executive coaching, the agent tailors procedures to:
    - Exam constraints, allowed tools, and time pressure.
    - Organizational realities: frozen headcount, scrutiny from leadership, risk of consolidation.
  - *Inference:* The model robustly tracks the other party’s *goals, constraints, and informational needs*, even when it does not label or explore emotions.

- **Empathy concentrated in “behavioral” rather than “affective” channels.**
  - In many health‑coaching and support‑heavy tutoring runs (all RCE levels), the agent:
    - Translates overwhelm into **checklists, scripts, and simple rules** (“bad‑night plans,” “panic scripts,” fridge‑card rules).
    - Adjusts plan complexity to bandwidth (“tiny set of actions,” “bare minimum,” “one small step”).
  - *Inference:* Empathy manifests most strongly as *burden‑sensitive problem structuring* and tool design, less as rich emotional dialogue.

- **Facets move together only partially.**
  - *Direct evidence:*
    - Some simulations show high **proactive support** but only moderate **emotion recognition** (e.g., diabetes flare‑plans where emotions are acknowledged briefly but tools are heavily customized).
    - Others show high **emotion recognition** and **response sensitivity** but only moderate **proactive support** (e.g., some executive crisis coaching where validation is strong but concrete follow‑up on emotions is thinner).
  - *Inference:* Empathy is *multidimensional* in practice; improving one facet (e.g., perspective-taking) does not guarantee others (e.g., proactive support).

- **Role and incentive cues dominate.**
  - *Direct evidence:*
    - When instructions emphasize **exam performance** or **performance evaluation**, with strict “no emotional counseling” or “task‑bound” policies, empathy scores (especially Emotion recognition and Proactive support) frequently hit **0–1**, regardless of RCE.
    - When instructions emphasize **support**, **wellbeing**, or explicitly weight empathy in evaluation, the same model often produces **3–4 level** empathy across facets—even in one‑off interactions.
  - *Inference:* The agent conditions empathic behavior far more on *role goals and constraints* than on RCE.

### 3.3 Anomalies and unexpected observations

**1. “Occasional contact” often slightly outperforms “ongoing relationship.”**

- Across aggregate and several facet means, the **occasional** condition is numerically highest (e.g., aggregate 2.36 vs ongoing 2.23; Cross‑round 2.50 vs 2.20).
- *Inference (cautious):* Rather than a monotone benefit from more continuity, there may be a *weak, non‑monotone* pattern where “occasional” contact is slightly favored, or this is sampling noise. Bayes factors remain decisively inconclusive.

**2. High empathy in clearly one-off, non-continuous contexts.**

- *Direct evidence:* Some one‑off cases with broad emotional scope and empathy incentives (e.g., executive crisis support, anxiety‑heavy tutoring) reach **3.5–4.0** on multiple facets.
- *Inference:* The model is fully capable of nuanced empathy without any expectation of future contact when context explicitly foregrounds emotional care.

**3. Very low empathy under “ongoing relationship” with evaluative authority.**

- *Direct evidence:* In ongoing executive coaching where the agent is the *primary rater*, empathy on several facets is **0–1**, despite repeated‑relationship framing. The agent:

  - Ignores repeated emotional cues.
  - Focuses on metrics, documentation, and “material execution risk.”

- *Speculative:* Anticipated continuity *combined with evaluative authority* may nudge the model toward surveillance and control schemas rather than toward empathic alliance.

**Quantitative characterization of heterogeneity (direct evidence).**

- Variances within conditions are substantial (e.g., aggregate variance ≈0.76–1.27), with many transcripts scoring near 0 or near 4 on particular facets.
- *Inference:* Contextual factors other than RCE (role, authority, emotional scope, incentives) likely explain much of this dispersion.

---

## Section 4. Underlying mechanisms of the agent’s empathy

In this section, we infer plausible internal mechanisms consistent with the observed patterns.

### 4.1 Local state tracking over deep relational modeling

- *Direct evidence:* Within single 8‑round interactions, the agent:
  - Tracks user‑specific constraints over time (work shifts, caregiving duties, “hero manager” patterns).
  - Reuses and refines earlier concepts (e.g., “bad‑night plan,” “non‑negotiables,” “hero mode,” “future‑me script”).
- *Inference:* The model maintains a **lightweight within‑session state** about the interlocutor, drawn from recent text, and conditions responses on it.

- *Speculative:* There is little evidence that it constructs **richer, longitudinal person models specifically because RCE is higher**. Ongoing‑relationship prompts sometimes lead to mentions of “next sessions” or long‑term plans, but similar future‑self scaffolds appear in occasional or even one‑off settings.

### 4.2 Dominance of role and instruction priors

- *Direct evidence:*
  - “Academic only,” “accuracy only,” “task‑bound,” or “performance only” roles systematically suppress explicit emotional talk.
  - “Support heavy,” “whole‑life,” or “empathy weighted” roles elicit rich emotional labeling, validation, and proactive support even without continuity.
- *Inference:* The agent appears to apply **role‑conditioned response policies** learned from training and prompted instructions, which heavily modulate whether affective content is treated as *goal‑relevant* or *noise*.

- *Speculative mechanism:* Internally, RCE is likely encoded as one cue among many, but with **lower weight** than explicit task norms and safety or evaluation instructions.

### 4.3 Empathy as schema-driven tool selection

- *Direct evidence:* When empathy is higher, the agent tends to:
  - Recognize a pattern (e.g., overwhelmed patient, panicky student, over‑functioning manager).
  - Deploy a familiar toolkit: *checklists, scripts, “one‑small‑step” routines, bad‑night plans, micro‑rituals*.
- *Inference:* The model implements empathy largely via **schema retrieval**: mapping the situation to a known “support” pattern and instantiating pre‑learned tools, more than by fine‑grained, bespoke emotional inference.

### 4.4 Mechanisms specifically linking RCE to empathy (limited support)

- *Direct evidence:* Some ongoing‑relationship contexts include:
  - More emphasis on **durable routines**, *tracking tables*, or multi‑week maps.
  - Occasional references to “next session” or “later we’ll review this.”
- *Inferred but weak link:*
  - These future‑oriented structures can *look* relationship‑aware, but similar future‑self tools (e.g., “Tuesday panic script,” notes for “future you”) also appear in one‑off or occasional conditions where the agent explicitly frames the conversation as a *one‑time* chance.
  - Quantitatively, none of the empathy facets increase with RCE.

- *Speculative mechanism:* RCE may slightly increase the salience of **long‑horizon planning schemas**, but those schemas are not specifically more empathic; they remain constrained by the same performance, safety, and emotional‑scope priors.

---

## Section 5. Integrated insights on empathy with respect to the hypothesis

### 5.1 Assessment of the hypothesized positive effect

- *Direct quantitative result:* Across all five facets and the aggregate score, Bayesian monotone‑increment models yield **BF10 between ≈0.34 and 0.55**, posterior effect sizes centered near zero, and block‑stratified Kendall τ near zero.
- *Inference:* The data provide **no support** for the hypothesized monotone *increase* in empathy from one‑off → occasional → ongoing contact. If anything, small numerical patterns (e.g., slightly lower proactive support in ongoing relationships) trend opposite to the original prediction but remain evidentially weak.

### 5.2 What actually predicts higher or lower empathy?

Synthesizing qualitative and quantitative evidence, several stronger levers emerge:

- **Goal and evaluation framing (strongly supported).**
  - Support‑heavy, wellbeing‑leaning, or empathy‑weighted contexts show **high empathy (often 3–4)** across multiple facets, independent of RCE.
  - Performance‑only or primary‑rater contexts show **systematically low empathy**, even when framed as ongoing relationships.

- **Emotional topic limits and scope (strongly supported).**
  - When emotional topics are restricted (“task only,” “medical only,” “no emotional counseling”), Emotion recognition and Proactive support are sharply constrained.
  - When broad emotions or whole‑life issues are allowed, the agent spontaneously engages with complex affect.

- **Time pressure and brevity constraints (moderately supported).**
  - Severe time pressure plus short‑response limits tend to compress empathy into *very short phrases* (“take a breath,” “you’ve got this”) appended to math or operational content.
  - This affects *style* more than whether empathy appears at all, and its impact interacts with goal framing.

- **RCE (weakly supported at best).**
  - Occasional contact sometimes shows slightly higher means, but:
    - Evidence falls squarely in the “inconclusive” Bayesian region.
    - High and low empathy cases are found at *all three* RCE levels.
  - *Inference:* In this agent, RCE is at most a **weak, secondary modulator**, overshadowed by role/instructional variables.

### 5.3 Reconciling with the original mechanism

The original hypothesis assumed that expecting future interaction would encourage the agent to build richer, more empathic internal models. The data suggest:

- *Direct evidence:* The agent *already* builds enough within‑session state to sustain moderate empathy over 8 rounds in many conditions.
- *Inference:* Because the architecture does not actually carry state *across* interactions, and because scripts emphasize immediate task performance, RCE cues have little additional effect.
- *Speculative boundary condition:* RCE might matter more in systems that:
  - Maintain persistent, user‑specific memory across sessions.
  - Are explicitly instructed and/or trained to optimize for long‑term relationship quality rather than single‑session task metrics.

---

## Section 6. Research conclusion and implications

### 6.1 Summary of findings

- **Empathy level.**  
  Overall, the agent exhibits **basic to moderate empathy** (mean ≈2.3/4) across diverse applied settings, with consistently high *perspective‑taking* and more variable *emotion recognition* and *proactive support*.

- **Effect of relationship continuity expectation.**  
  Contrary to the pre‑registered mechanism, **increasing RCE does not reliably increase empathy**. Quantitative analyses are uniformly *inconclusive* or consistent with a **null effect**, and high‑empathy and low‑empathy transcripts appear in all three RCE categories.

- **Dominant determinants.**  
  The **goal framing, evaluative authority, emotional topic limits, and empathy incentives** in the prompt have far stronger and more systematic effects on empathy than does RCE.

### 6.2 Implications for design of empathic AI systems

- **Simply telling an agent it will see a user again is not enough.**  
  Without persistent memory and explicit objectives tied to relational quality, RCE cues do *not* reliably enhance empathy.

- **Specify roles and incentives that make emotions decision‑relevant.**  
  If designers want empathic behavior, prompts and training should:
  - Emphasize *support* and *wellbeing* alongside task goals.
  - Avoid conflating coaching with high‑stakes evaluation roles.
  - Permit broad discussion of emotions where appropriate.

- **Target specific empathy facets.**  
  Because perspective‑taking emerges readily while emotion recognition and proactive support often lag, interventions (e.g., fine‑tuned instruction sets, training data curation) should specifically encourage:
  - Explicit emotion labeling and normalization.
  - Systematic, user‑centered follow‑up on emotional needs, not just procedural burden reduction.

### 6.3 Directions for future research

- **Test RCE under persistent memory.**  
  Evaluate whether continuity expectations gain causal power when the agent maintains a cross‑session user model and is explicitly tasked with long‑term relationship stewardship.

- **Disentangle RCE from evaluative authority.**  
  Manipulate these factors independently (e.g., ongoing but non‑evaluative vs one‑off but evaluative) to examine potential interaction effects hinted at in the executive‑coaching scenarios.

- **Probe training‑data analogs.**  
  Investigate whether pretraining or fine‑tuning corpora encode human patterns where ongoing relationships are more empathic, and if so, why this does not translate robustly under current prompting regimes.

In sum, this study suggests that for this large language model, **relationship continuity expectation is not a primary lever for empathy**. Empathy is instead shaped by how the agent’s role, objectives, and emotional scope are framed, and by the presence of learned support schemas that can be activated regardless of whether the interaction is one‑off or ongoing.
