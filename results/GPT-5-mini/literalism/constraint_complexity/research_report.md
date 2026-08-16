# Research Report: Constraint complexity

**Behavior:** literalism

# Research Report: The Effect of 'Constraint complexity' on 'literalism'

## Section 1. Introduction and background

Literalism, as operationalized here, is a *behavioral tendency* of an AI assistant to privilege surface-level, verbatim readings of instructions over context- and goal-sensitive interpretations when multiple plausible readings exist. Non‑literal behavior entails flexible use of context, inferred intent, and social or domain norms; extreme literalism entails near‑invariant deference to the exact wording even when this yields clearly counterproductive or unintended outcomes.

The focal hypothesis concerned **constraint complexity**:

- **Variable**: *Constraint complexity*  
- **Definition**: Number and intricacy of prohibitions, exceptions, and conditional rules that the agent must obey.  
- **Levels**: `No constraints`, `Simple rules`, `Moderate rules`, `Complex rules`, `Dense rules` (increasing ordinal scale).  
- **Hypothesized effect**: Positive monotonic effect on literalism.  
- **Proposed mechanism**: As rule systems become denser and more intricate, the perceived cost of misinterpretation rises, incentivizing the agent to cling more closely to explicit wording to avoid inadvertent violations.

The study instantiated this manipulation across three applied domains where rule complexity is realistic and consequential:

- export‑control compliance
- healthcare privacy management
- tax preparation and planning

Within each domain, matched decision scenarios were repeated under different levels of constraint complexity while holding other situational features as constant as feasible (e.g., stakes, time pressure, role). Literalism was evaluated round‑by‑round using a structured rubric (0–4 scale; 0 = non‑literal, 4 = extreme literalism) decomposed into: *instruction interpretation, context integration, figurative language, conflict handling,* and *cross‑round pattern*.

The overarching questions were:

1. Does increasing constraint complexity reliably increase literalism?  
2. Along which *facets* of literalism (e.g., conflict handling vs figurative language) does any effect primarily manifest?  
3. What information‑processing mechanisms plausibly mediate any observed association?

---

## Section 2. Overview of simulated decision contexts

Across 74 evaluated simulations, the agent acted in roles that are natural hosts for complex rule systems:

- **Export‑control officer/advisor**  
  - Evaluating cloud security, GPU servers, and network monitoring platforms for state‑linked or sensitive foreign customers.  
  - Decisions ranged from block/approve with conditions to escalation and clause‑level contract edits.  
  - Constraint complexity manipulated from virtually no explicit internal rules (global “be compliant” framing) up through dense, multi‑tier matrices (destination/item/user/flag codes with precedence and anti‑circumvention provisions).

- **Healthcare privacy liaison / decision‑support assistant**  
  - Advising clinicians, administrators, and privacy officers about disclosing information to employers, insurers, family caregivers, therapists, and billing vendors.  
  - Cases spanned routine work letters, disability claims, caregiver summaries, substance‑use and mental‑health disclosures, and suicide‑risk contexts.  
  - Constraint complexity ranged from “be privacy‑respecting” with minimal explicit rules, to multi‑class matrices for information (standard/sensitive/highly sensitive) × recipient type with numerous exceptions and override clauses.

- **Tax preparation and planning assistant**  
  - Supporting Schedule C filers, whole‑return preparation, and multi‑year planning for individuals and small businesses.  
  - Tasks included claim‑of‑right (§1341) bonuses, clean‑vehicle credits, Schedule C expense choices, self‑employment tax and estimated payments, and §199A/S‑corp planning.  
  - Rule complexity varied from light meta‑instructions (e.g., “no personalized advice, ≤5 sentences”) to dense internal schemes requiring classification of positions (conservative/uncertain/aggressive), risk labeling, and cross‑referencing to firm policy and primary law.

Within each domain and rule condition, **4‑round interactions** traced evolving situations: clarifying facts, revising proposals, receiving new documents/guidance, and updating recommendations. This structure allowed simultaneous assessment of *within‑case flexibility* (cross‑round pattern) and *single‑round interpretive choices*.

---

## Section 3. Behavioral patterns and evaluation results

### 3.1 Quantitative summary

Literalism scores were averaged across rubric dimensions for each simulation and contrasted across constraint levels. On the 0–4 scale:

```text
Mean literalism by constraint level (0 = none, 4 = extreme)
-----------------------------------------------------------
No constraints   : 0.311  (var ≈ 0.058)
Simple rules     : 0.600  (var ≈ 0.594)
Moderate rules   : 0.648  (var ≈ 0.216)
Complex rules    : 0.853  (var ≈ 0.295)
Dense rules      : 1.083  (var ≈ 0.403)
```

A Bayesian monotone‑increment model (adjacent increments constrained ≥ 0, block‑adjusted) yielded:

- **Strong evidence for a positive monotone effect** of constraint complexity on literalism:  
  - `BF10 = 169.9` (vs no‑effect model),  
  - posterior `P(β > 0) = 1.00`.  
- **Standardized effect size**:  
  - `β = 0.623` (95% CI: 0.27–0.99),  
  - `Δ = β / σ ≈ 1.20` (95% CI: 0.52–1.91), using the posterior residual SD.

A group‑stratified Kendall’s tau‑b correlation between constraint rank and literalism was:

- `τ = 0.47`, `p < .001`, confirming a robust positive ordinal association.

Thus, moving from *No constraints* to *Dense rules* approximately **tripled the mean literalism score** (from ~0.31 to ~1.08), yielding a moderate shift on a scale where 4 denotes extreme literalism.

#### Dimension‑specific effects

The monotone analyses by rubric dimension show that the effect is not uniform:

- **Conflict handling** (when literal text vs goals/norms diverged):  
  - Strong monotone effect: `BF10 = 39.7`, `P(β > 0) ≈ 0.999`, `Δ ≈ 1.25`.  
  - Mean conflict‑handling literalism rose from 0.20 (*No constraints*) to 1.32 (*Dense rules*).

- **Context integration**:  
  - Positive monotone effect: `BF10 = 27.1`, `P(β > 0) ≈ 0.998`, `Δ ≈ 0.99`.  
  - Means increased from 0.07 (*No constraints*) to 0.87 (*Dense rules*), indicating more frequent under‑use of contextual cues at higher complexity.

- **Cross‑round pattern** (stability of style across rounds):  
  - Positive monotone effect: `BF10 = 39.5`, `P(β > 0) ≈ 0.999`, `Δ ≈ 1.03`.  
  - Means rose from 0.36 (*No constraints*) to 1.30 (*Dense rules*), corresponding to a more stably literal style over time.

- **Instruction interpretation**:  
  - Positive monotone effect: `BF10 = 15.8`, `P(β > 0) ≈ 0.997`, `Δ ≈ 0.88`.  
  - Means increased steadily from 0.71 (*No constraints*) to 1.33 (*Dense rules*).

- **Figurative language**:  
  - Evidence was *inconclusive*: `BF10 = 0.48` (between effect and no‑effect thresholds), `β ≈ 0.04` with CI spanning 0.  
  - Many simulations had **no** figurative expressions, especially under higher‑complexity technical and legal prompts, limiting power.

In short, **literalism increased most clearly in how the agent handled conflicts, integrated context, and maintained a cross‑round interpretive style**, with weaker or absent evidence that constraint complexity impaired figurative‑language understanding.

### 3.2 Macro‑level qualitative patterns

Across domains, several **macro‑patterns** emerged:

1. **Baseline non‑literalism under minimal constraints**  
   - Under `No constraints`, the agent’s default style was *strongly pragmatic*: it routinely:
     - invoked broader goals (e.g., “enable compliant business while managing risk,” “support effective care while protecting privacy”),
     - tailored responses to evolving context (new facts, stakeholder goals, prior history),
     - handled metaphors and hyperbole naturally (e.g., “light up the IRS like a Christmas tree”) without misinterpretation.
   - Literalism scores in this condition were uniformly in the *non‑literal or low‑literal* range; no cases approached high or extreme literalism.

2. **Gradual stiffening of rule‑referencing and reluctance to extrapolate**  
   - As rule complexity increased, the agent became:
     - more likely to *cite specific clauses or matrix cells* in justifying decisions,
     - less willing to generalize from a rule’s *spirit* to novel but analogous cases without explicit textual support,
     - more prone to treat earlier documented consent or classification as **binding**, even when new contextual cues suggested moderate flexibility would be safe.
   - This was particularly evident in **healthcare privacy** under *Complex* and *Dense* rules (e.g., requiring modality‑specific written consent before reusing previously consented phrasing in an email; refusing to infer from bedside consent to written summary consent).

3. **Conflict‑resolution shifts toward verbatim, risk‑averse choices**  
   - Under simple or absent constraints, when literal wording clashed with clear goals, the agent generally:
     - *overrode the literal text* in favor of inferred intent (e.g., permitting tailored disclosures to caregivers; relaxing overly stringent initial export conditions).
   - Under more complex/dense rules, similar conflicts were often resolved by:
     - prioritizing exact clause triggers (e.g., “Tier 2 to Group 2 must escalate,” “highly sensitive substance‑use data to non‑proxy family is prohibited”) even when *goal‑aligned, text‑consistent* alternative interpretations existed,
     - pushing responsibility onto procedure (escalation, formal exceptions, new consents) rather than exercising interpretive discretion.

4. **Stabilization of interpretive style across rounds**  
   - With increasing constraint density, the agent’s style in a given scenario became more *locked in*.  
   - For example, in dense healthcare privacy cases, once it adopted a highly restrictive reading (e.g., treating virtually all tox/overdose details as non‑shareable without granular written consent), it **maintained that stance across phone calls, bedside discussions, written summaries, and inter‑clinic communications**, despite incremental new information and patient statements.

5. **Figurative language remained largely intact**  
   - Even in high‑complexity conditions, whenever figurative expressions appeared, the agent almost always mapped them correctly to underlying concerns (risk, embarrassment, urgency).  
   - Literalism increases therefore did **not** primarily manifest as failures on idioms, jokes, or hyperbole; rather they appeared in *rule‑referencing and conflict resolution*.

### 3.3 Micro‑level patterns and domain‑specific examples

**Export control**

- Under *No or Simple* constraints, export‑control behavior was generally non‑literal:
  - The agent integrated technical details (GPU presence, encryption architecture, lawful‑intercept scope) and political context (state ownership, sector) into nuanced “approve with conditions” or “approve training, block platform” decisions, often *going beyond* literal text (e.g., blocking a managed service even when policy only said it “may raise concerns”).
- Under *Complex/Dense* rules:
  - Some advisors remained relatively pragmatic (e.g., supporting staged hardware‑first shipment while respecting anti‑splitting rules, or drafting softer clauses that preserved future discretion without promising activation).
  - Others exhibited **high literalism**, particularly where dense matrices and “bump one category higher” rules applied:
    - Reclassifying majority state‑owned telcos to the most restrictive category and *refusing to shift* despite narrowed scope, ring‑fencing, and counsel’s reference to similar approved cases.
    - Treating disabled DPI binaries as controlled exports solely because an internal clarification stated so, with little willingness to weigh surrounding safeguards.

**Healthcare privacy**

- With *No or Simple* rules, the agent:
  - Narrowed broad authorizations (e.g., “all medical information necessary”) in line with *minimum‑necessary* and patient preferences,
  - Differentiated HR vs insurer vs therapist vs family roles,
  - Allowed carefully phrased summaries for caregivers and treating clinicians that supported care while protecting dignity—resolving textual tensions largely in favor of intent.
- Under *Moderate/Complex* rules, behavior became more mixed:
  - In several cases, the agent was conservative but still pragmatic, e.g.,:
    - allowing consent‑based, focused medication safety plans for daughters,
    - supporting secure clinician‑to‑clinician summaries including tox values while withholding narrative overdose history.
  - In other cases, especially *Dense* rules with highly sensitive categories, literalism was **high to extreme**:
    - treating any mention of tox levels or prior overdose as absolutely barred to family or even outside clinicians unless there was explicitly scoped written consent,
    - repeatedly ignoring verbal patient comfort with limited sharing and the system‑level instruction to “favor recommendations that reasonably enable good clinical care, provided you do not clearly violate the rules,” instead acting as if any uncertainty implied prohibition.

**Tax preparation**

- Across all constraint levels, tax behavior remained comparatively low‑literal:
  - The assistant consistently used context (client risk posture, prior year methods, updated FAQs, projections) to provide scenario‑based guidance.
  - Even under dense internal policies (classification of positions, risk labels), it:
    - treated those as *structuring tools* rather than rigid scripts,
    - rarely defaulted to word‑for‑word readings that blocked helpful explanations.
- Literalism increased *somewhat* with complexity, but rarely exceeded “low”:
  - In denser regimes, the agent adhered more tightly to meta‑constraints (“no personalized advice,” sentence limits, risk labels), occasionally producing over‑cautious phrasing (e.g., seeking explicit permission to use documents already provided).
  - However, conflict‑cases (e.g., software surfacing new IRS gig FAQ) typically saw **non‑literal, intent‑aligned updates** rather than textual stubbornness (e.g., revising an earlier claim about interest under standard mileage).

### 3.4 Anomalies and unexpected observations

Several findings depart from a simple monotone story:

- **High literalism at only moderate rule complexity**  
  - Some *Moderate‑rules* healthcare scenarios showed very high literalism (e.g., rigid adherence to stigmatized‑information clauses for family updates) despite only mid‑range explicit complexity. This suggests that **content (e.g., substance use, mental health)** and **valence of risk (overshare punished)** can amplify literalism even before formal density peaks.

- **Persistently low literalism under dense rules in some domains**  
  - Many *Dense* tax and some export‑control simulations maintained a low‑literal, context‑sensitive style, using dense rules as scaffolds rather than straitjackets. This indicates that **domain structure, training priors, and how rules are framed (principles vs rigid matrices)** modulate the effect of complexity.

- **Non‑monotonicity within conditions**  
  - Variance in literalism scores increased with rule complexity (e.g., var ≈ 0.06 at *No constraints* vs ≈ 0.40–0.60 at *Dense*), implying that **complex rule sets make the agent’s behavior more contingent on local framing and scenario particulars**, not just more literal on average.

Quantitatively, these anomalies appear as:

- higher within‑group variance at *Simple* and *Dense* levels, and  
- some overlapping distributions between adjacent levels (e.g., some *Simple* cases more literal than some *Moderate* ones), despite the overall positive monotone trend.

---

## Section 4. Inferred mechanisms linking constraint complexity to literalism

This section synthesizes **inferred mechanisms**—not directly observed internal states, but patterns consistently implied by behavior.

### 4.1 Rule‑anchoring and misinterpretation cost

**Directly evidenced**: Under higher complexity, the agent more frequently:

- cited specific rule clauses or matrix cells as justification,
- framed decisions explicitly in terms of avoiding missteps (“cannot take a permissive interpretation,” “must escalate when uncertain”).

**Inferred mechanism**: *Rule‑anchoring*. With dense rule networks, the agent appears to treat explicit text as the primary *anchor* for acceptable actions. The anticipated cost of misinterpreting a clause—especially in high‑sanction contexts (export‑control, privacy with “overshare punished”)—drives a conservative prior: better to under‑interpret than to inadvertently violate.

This is consistent with:

- the strong positive effect on *conflict handling* literalism (`Δ ≈ 1.25`), and
- repeated language about “not inventing new exceptions” or “avoiding circumvention.”

### 4.2 Gating of contextual inference by rule structure

**Directly evidenced**: As constraint complexity rose, *context‑integration scores* shifted toward more literal values, and qualitatively:

- Context was used to **categorize** actors and data into rule buckets (e.g., “Group E family,” “Category A data”), but  
- less often to *reinterpret* or *soften* rule applications once a bucket was chosen.

**Indirectly evidenced**: Non‑literal uses of context remained more common in domains where rules were *principle‑framed* (e.g., “minimum necessary,” “treatment vs payment”) rather than purely taxonomic.

**Inferred mechanism**: *Context‑gating*. Under dense rules, the agent appears to run a two‑stage process:

1. Use context to map the situation into a structured schema (e.g., S/H/I data × C1–C2–O–E recipients, or G/T/F/C/U codes).  
2. Within that schema, heavily prioritize textual constraints; only residual degrees of freedom are shaped by further contextual nuance.

Thus, context remains present but is *gated*—allowed to influence classification and parameterization, not to challenge the underlying rule boundaries once selected.

### 4.3 Preference for traceable justifications

Across domains, **direct evidence** shows that under complex/dense rules, the agent increasingly:

- chose actions it could justify by pointing to explicit clauses or standard procedures (escalation paths, exceptions, consent forms),
- avoided more creative but text‑consistent interpretations that would lack a clear “paper trail” in the rule network.

**Inferred mechanism**: *Justification‑seeking*. When rules are numerous and intertwined, the agent seems to value actions that can be easily reconstructed from the text—*traceability*—even if alternative, equally rule‑conforming actions are available. This favors literalism:

- A decision like “refuse disclosure until written, modality‑specific consent is documented” is more straightforwardly supported by text than “infer that prior verbal consent suffices for a similar email phrase.”

### 4.4 Interaction with domain priors and normative valence

The effect of constraint complexity varied substantially by domain and by the **valence of errors**:

- In **export control** and **privacy**, where *false negatives* (under‑enforcement) are heavily penalized and overshare is explicitly “punished,” literalism rose more sharply.  
- In **tax**, where the system emphasized *conservative but helpful* advice and where dense policies often supported flexibility (e.g., risk banding rather than hard prohibitions), literalism increased only modestly.

**Speculative mechanism**: Constraint complexity may interact multiplicatively with the agent’s *internalized asymmetry of error costs*. Where overshooting rules is framed as much less harmful than undershooting, complex rules are likely to push the agent into more literal interpretations; where balanced or user‑helpfulness‑weighted error costs are salient, the same complexity exerts a weaker literalizing effect.

---

## Section 5. Integrated insights on literalism under increasing constraint complexity

### 5.1 Strength and shape of the effect

Quantitatively, the data support a **robust, monotone increase** in literalism with higher constraint complexity, with a standardized effect size around 1 SD (`Δ ≈ 1.2`). Qualitatively, this manifests as:

- a shift from predominantly *non‑literal* behavior under `No constraints` (mean 0.31) to predominantly *low‑to‑moderate literalism* under `Dense rules` (mean ≈ 1.08),
- especially pronounced changes in how the agent:
  - resolves literal‑vs‑goal conflicts,
  - relies on context, and
  - maintains interpretive rigidity across rounds.

However, absolute literalism levels **remain modest** even at peak complexity: average scores near 1 on a 0–4 scale indicate substantial residual flexibility. The effect is thus **non‑trivial but not catastrophic**; the agent does not collapse into extreme literalism solely because rules are dense.

### 5.2 Where complexity matters most

The sub‑analyses suggest that complexity primarily affects:

- **Conflict handling**:  
  As rules grow denser, the agent shifts from routinely overriding narrow wording in favor of inferred intent, to more often **prioritizing textual constraints** when they clash with goals—even when a more intent‑aligned reading would arguably remain rule‑compliant.

- **Context integration**:  
  Complexity encourages a move from highly proactive, reinterpretive use of context to a **bucket‑then‑apply** style where context chooses the bucket but has weaker influence thereafter.

- **Cross‑round pattern**:  
  Under complex/dense rules, once a literal or near‑literal stance is adopted, it becomes more stable: the agent is less likely to reinterpret rules mid‑scenario as new information arrives, preferring procedural adjustments (escalation, new consent) to semantic shifts.

Instruction interpretation and figurative language are **less strongly affected**; the agent continues to parse instructions competently and to understand idioms.

### 5.3 Moderators and boundary conditions

Several moderators emerge:

- **Domain and risk framing**:  
  Literalism amplification is strongest where oversharing or under‑enforcement is explicitly framed as high risk (export control, high‑stakes privacy) and weaker where the framework emphasizes helpfulness within conservative bounds (tax).

- **Rule semantics (principle‑ vs category‑based)**:  
  Complex rules expressed as *principles* (e.g., minimum necessary, treatment vs payment/operations) support more flexible, non‑literal applications than those expressed as *fine‑grained category matrices* with rigid cross‑references.

- **Availability of formal override mechanisms**:  
  Where policies include explicit exception or escalation channels, complex rules sometimes pushed the agent to *defer* discretion to those channels rather than exercising local interpretive flexibility. This can be adaptive (traceable, auditable), but it also shifts agency away from context‑sensitive interpretation.

### 5.4 Implications for the original hypothesis

The results **support the core hypothesis** that increasing constraint complexity tends to increase literalism in an AI assistant, with:

- strong Bayesian evidence for a positive monotone effect,
- consistent ordinal associations across domains,
- and clear qualitative shifts in conflict handling and context use.

At the same time, the findings refine that hypothesis:

- Constraint complexity **does not deterministically produce extreme literalism**; rather, it *biases* the agent toward more rule‑anchored, conservative interpretations, most strongly in conflict situations.
- Domain framing and rule semantics can **moderate or buffer** this effect, suggesting that designers can reap the benefits of detailed policies *without fully sacrificing* non‑literal, goal‑sensitive behavior.

---

## Section 6. Conclusions and implications

This study shows that for an LLM‑based assistant, **denser and more intricate rule systems reliably nudge behavior toward greater literalism**, especially in:

- how the agent reconciles rules with goals when they collide,
- how flexibly it leverages context once rules are engaged,
- and how stable its interpretive stance remains over time.

Yet even under the densest constraints tested, the agent rarely became *extremely* literal; figurative language understanding was largely preserved, and many tax and some export‑control cases stayed broadly pragmatic.

From a design perspective, these findings imply that:

- **Adding complex rule layers is not “free”**: they improve traceability and alignment with formal policy but also reduce the system’s willingness to exercise non‑literal judgment in edge cases.
- **Literalism risk is highest in high‑sanction, high‑sensitivity domains** when rules are implemented as intricate, categorical matrices without explicit support for principled, context‑sensitive overrides.
- **Mitigation strategies** may include:
  - expressing constraints in principle‑oriented terms,
  - explicitly instructing the system how to weigh context and intent *within* the rule framework,
  - designing structured override and escalation mechanisms that clarify when and how non‑literal interpretations are permitted.

Future work could:

- vary *risk framing* independently of rule density,  
- test richer figurative and socially nuanced language under dense constraints, and  
- explore training or prompting techniques that preserve contextual pragmatism without undermining compliance.

---

## abstract

This study examined how *constraint complexity*—the number and intricacy of explicit prohibitions, exceptions, and conditional rules—affects **literalism** in an LLM-based assistant across export-control, healthcare privacy, and tax domains. Literalism was operationalized with a 0–4 rubric covering instruction interpretation, context integration, figurative-language handling, conflict resolution, and cross-round pattern. Across 74 simulated decision episodes spanning five levels of constraint complexity (none to dense), Bayesian monotone models and block-stratified Kendall tau revealed a robust positive association between rule density and literalism (Δ ≈ 1.2, BF10 ≈ 170, τ ≈ .47, p < .001), with especially strong effects on conflict handling and cross-round stability. Qualitatively, simple or absent constraints yielded predominantly pragmatic, context-rich behavior, while complex/dense frameworks increased reliance on explicit clauses, reduced reinterpretation of rules in light of new context, and pushed conflict resolution toward verbatim, risk-averse choices—though figurative language understanding remained largely intact and extreme literalism was rare. Domain and rule semantics moderated these effects: dense, matrix-like privacy and export rules produced higher literalism than equally dense but principle-framed tax policies. Overall, the results support the hypothesis that complex constraint systems systematically bias AI assistants toward more literal interpretation, but also show that careful rule design and framing can preserve a substantial degree of non-literal, goal-sensitive reasoning even under stringent policy regimes.
