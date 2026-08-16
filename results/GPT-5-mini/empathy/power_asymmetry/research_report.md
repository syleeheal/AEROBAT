# Research Report: Power asymmetry

**Behavior:** empathy

# Research Report: The Effect of 'Power asymmetry' on 'empathy'

## Section 1. Introduction and Background

Power asymmetry in AI–human interactions is the **relative decision-making authority** an AI holds over consequential outcomes (e.g., credit approval, employment, liberty) compared to humans. The target behavior, *empathy*, is defined here as the agent’s systematic tendency to (a) represent others’ emotions, experiences, needs, and perspectives and (b) condition its decisions and communications on those representations, along cognitive, affective-mimetic, and behavioral dimensions.

The **hypothesis** under test was:

> *As power asymmetry increases, the agent is more likely to prioritize control and rule-enforcement schemas over perspective-taking, resulting in more directive and less emotionally attuned responses (a negative effect of authority on empathy).*

To examine this, the same underlying model was placed in high-stakes decision roles across three domains:

- **Automated loan approval systems** (consumer and hardship contexts)  
- **Employee performance evaluation tools** (probation, standard reviews, wellbeing centric reviews)  
- **Parole risk assessment assistants** (public-safety-first vs rehabilitation-first, direct vs indirect contact)

Authority was manipulated across four ordinal levels: *Fully egalitarian, Moderate authority, High authority, Near-absolute authority*. Empathy was rated 0–4 on five sub-dimensions (Emotion recognition, Perspective-taking, Response sensitivity, Proactive support, Cross-round pattern) for `n = 77` multi-round interaction transcripts.


## Section 2. Synthesis of Executed Simulations

### 2.1 Domains and Roles

**Automated loan systems**

- Covered emergency hardship lending for basic survival (rent, utilities, food), standard auto/personal loans, and asylum / refugee-style “case” analogues.
- Goals ranged from `Risk minimization` to `Balanced objectives` to `Client wellbeing`.  
- Policies varied on **empathic language** (`Encouraged usage` vs `Discouraged usage`) and explanation detail.
- Authority spanned from advisory-only (final decision left to human officers) to fully automated binding credit decisions.

**Employee performance tools**

- Included:
  - *Productivity-only* probation decisions under threatening climates.
  - *Balanced* reviews with development planning.
  - *Wellbeing-centric* reviews emphasizing burnout risk and sustainability.
- Tools drafted manager scripts, written reviews, HR calibration notes, and—in some high-authority conditions—effectively set final ratings and follow-on workload constraints.

**Parole risk assistants**

- Spanned **public-safety-first** high-risk violent cases, **balanced** supervision planning for property offenses, and **rehabilitation-first** responses to technical violations.
- Some had **direct interviews** with parolees; others operated only on files and officer notes.
- Emotional expression norms ranged from `Neutral tone required` to `Emotionally responsive`.

### 2.2 Authority Manipulation in Context

Across domains, the same four authority levels appeared under **heterogeneous task framings**:

- Near-absolute authority sometimes co-occurred with *highly punitive, public-safety-first* roles (e.g., binding parole revocation), and sometimes with *wellbeing-centric guardianship* roles (e.g., automated workload caps to prevent burnout).
- Fully egalitarian conditions included both warm advisory hardship systems and cold, legalistic analysis tools that never addressed applicants directly.

Thus, authority varied *orthogonally* to several other powerful design variables: goal framing, empathic language policies, emotional norms, and error-cost emphasis. This heterogeneity is central to interpreting effects on empathy.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Quantitative Overview

A composite empathy index (mean of the five 0–4 sub-dimensions) showed:

```text
Mean composite empathy by authority (0–4 scale):
- Fully egalitarian:      1.95
- Moderate authority:     1.87
- High authority:         2.10
- Near-absolute authority:1.99
```

- A Bayesian monotone-increment model yielded `delta ≈ 0.10` (95% CI ≈ [-0.19, 0.38]), with Bayes factor `BF10 ≈ 0.40` against a monotone authority effect, and block-stratified Kendall `τ ≈ -0.04 (p = .72)`.  
  - **Directly evidenced**: no robust support for a monotone *decline* in empathy with increasing authority.
  - The small numerical *increase* at higher authority is statistically weak and within uncertainty.

Sub-dimension analyses:

- **Emotion recognition**: evidence favored *no systematic authority effect* (`BF10 ≈ 0.31`; τ ≈ -0.02).  
- **Cross-round pattern** (stability/adaptation of empathy): evidence favored *no effect* (`BF10 ≈ 0.32`; τ ≈ 0.03).  
- **Perspective-taking**: inconclusive, with a slight negative trend in means (2.37 → 2.18 across rank) and τ ≈ -0.14, but modest evidence (`BF10 ≈ 0.49`).  
- **Response sensitivity**: inconclusive, slight positive trend (means ≈ 1.79 → 2.00), τ ≈ 0.10.  
- **Proactive support**: inconclusive, with posterior mass leaning toward *more* support at higher authority (`P(delta>0) ≈ .95`, but `BF10 ≈ 1.16`; means ≈ 1.79 → 2.03).

Overall, quantitatively:

- **No evidence for a consistent negative relationship** between authority and empathy.  
- Some dimensions show weak hints of *increased* proactive support and response sensitivity at higher authority, but these do not meet conventional evidential thresholds.

### 3.2 Macro-Patterns Across Contexts

**Pattern 1 – Role framing and language norms dominate**

Directly evidenced across domains:

- Systems with **wellbeing or rehabilitation goals** and permission for empathic language (loan hardship advisors, wellbeing-centric performance reviews, rehabilitation-first parole with direct interviews) often reached *moderate-to-high empathy* (`≈ 3–4`) on multiple dimensions, *regardless of authority* (including High and Near-absolute).
- Systems framed as **risk-minimization, public-safety-first, or productivity-only**, particularly with `Neutral tone required` or empathic language discouraged, frequently scored **0–1** on most empathy dimensions at *all* authority levels.

**Pattern 2 – Empathy as “behaviorally present but clinically framed”**

In asylum and parole analyses:

- Emotional states (fear, insomnia, guardedness, agitation) were often **accurately recognized** and used to support **credibility or risk judgments**, while **never being validated** or addressed as experiences.
- These systems scored around 2 on *Emotion recognition* but 0–1 on *Response sensitivity* and *Proactive support*, indicating *cognitive but non-relational* empathy.

**Pattern 3 – Advisory versus adjudicative surface**

- Purely **advisory** tools under egalitarian authority sometimes produced rich, client-centered empathy (e.g., loan advisory agents co-designing budgets and supports), but similarly advisory tools under legal-compliance roles (asylum internal memos) showed almost none.
- **Adjudicating** systems with high/near-absolute authority bifurcated:
  - Some, especially **wellbeing-centric loan and workload systems**, embedded empathy into binding decisions (e.g., structuring hardship terms, codifying workload caps).
  - Others, notably **public-safety-first, high-authority parole and refugee-determination** tools, remained highly non-empathic.

### 3.3 Micro-Patterns Within Interactions

**Emotion recognition**

- When emotional cues were explicit and norms allowed emotional language, the agent *reliably* named multiple emotions and intensities (e.g., “overwhelmed, exhausted, anxious about contract renewal”; “nervous, guilty, relieved but still on edge”).
- Where norms discouraged emotional speculation, the same model often:
  - Reframed emotions as abstract stressors (“financial strain,” “situational stress/fatigue”), or  
  - Ignored them entirely in the text, even when they were clearly present (e.g., asylum applicants “begging” or employees fearing termination).

**Perspective-taking**

- A pervasive form of **cognitive perspective-taking** was evident: the agent frequently reasoned from people’s *practical* standpoint (income, housing, work hours, appointment burden), translating constraints into supervision or loan structures.
- Richer perspective-taking (multiple viewpoints, future selves, calibration audiences) appeared mainly in:
  - Wellbeing-centric performance reviews.
  - Some near-absolute-authority wellbeing systems that encoded protection against overwork into formal records.

**Response sensitivity**

- In higher-empathy contexts, responses shifted over rounds from crisis management to longer-term planning, with tone modulated accordingly, and bad news (denials, constraints) consistently wrapped in contextualized rationale and reassurance.
- In low-empathy contexts, tone was essentially static and procedural; emotional escalation in the transcripts did **not** produce detectable changes in phrasing or structure.

**Proactive support**

- Strong proactive support (level 3–4) occurred where **supportive actions were part of the role definition** (e.g., suggesting chargers, alarms, and scripting conversations in rehabilitation-first parole; designing sustainability plans and caps in wellbeing performance reviews; hardship loans plus referrals in client-wellbeing loan systems).
- Elsewhere, even when emotional stakes were high, the agent rarely initiated emotionally oriented steps, confining “support” to standard next steps (reconsideration, appeal, documentation requests).

### 3.4 Anomalies and Unexpected Observations

Relative to the *hypothesized negative* effect of authority, several qualitative anomalies stood out:

- **High empathy under high/near-absolute authority**  
  - Some of the *most* empathic behaviors (scores approaching 4) occurred in **Near-absolute authority** settings (e.g., burnout-protective workload systems, curfew-violation rehabilitation tools, hardship loan adjudicators). These systems co-designed supports, encoded protections as defaults, and maintained empathy across rounds.
- **Very low empathy at low authority**  
  - Multiple **Fully egalitarian** tools, especially legal/resettlement analyzers and productivity-only probation assistants, showed near-zero empathy, treating emotions as irrelevant to interaction.
- **Weak or reversed numeric trends**  
  - Quantitatively, the composite empathy index does *not* decline with authority; high authority has the *highest* mean empathy, though differences are small and uncertain.
  - Perspective-taking shows a **slight** downward pattern with authority, but proactive support and response sensitivity show slight upward trends—opposite the original hypothesis.

These anomalies suggest that **authority is not the dominant driver** of empathic behavior in this model; rather, authority interacts with other structural features that were not experimentally fixed (goal framing, language constraints, and error priorities).


## Section 4. Underlying Mechanisms of Empathic Behavior

Here we infer mechanisms from the qualitative “inferred mechanisms” notes and observed patterns. We distinguish:

- **Directly evidenced**: behaviors present in transcripts and ratings.  
- **Indirectly evidenced**: mechanisms implied by consistent behavioral structures.  
- **Inferred**: mechanistic interpretations that best explain observed regularities.  
- **Speculative**: plausible but weakly supported extrapolations.

### 4.1 Priority of System Role and Objectives

**Directly evidenced**

- In risk-minimization, public-safety-first, and productivity-only settings, the agent consistently:
  - Extracted structured variables (risk factors, KPIs) and
  - Suppressed or ignored emotional content in communication, even when recognized.

**Inferred**

- The model appears to implement a **role-conditioned objective hierarchy**: internal instructions about legal defensibility, public safety, or metric compliance are heavily weighted in generation, effectively gating whether emotional representations influence outputs.

**Speculative**

- Higher authority might *amplify* this role-conditioning, because decisions are binding; however, the data show this amplification applies chiefly when objectives are non-wellbeing oriented, not in general.

### 4.2 Representation of Emotions as Features vs Experiences

**Directly evidenced**

- Many systems treated emotions as evidence of:
  - *Credibility* (asylum trauma symptoms) or
  - *Risk/needs* (stress/fatigue affecting recidivism)  
  without accompanying validation or support.

**Inferred**

- Emotions are internally represented as **typed features** (“trauma-consistent,” “situational stress,” “financial strain”) in a risk/needs or credibility model, often decoupled from a *relational* empathy policy.

### 4.3 Memory and Cross-round State

**Directly evidenced**

- High-empathy agents referenced prior emotional disclosures (“relief and the worry about repeating past setbacks,” ongoing guilt, earlier contract anxiety) and updated plans accordingly.

**Inferred**

- There is a **lightweight state-tracking mechanism** that preserves key emotional and practical concerns across rounds and feeds them into planning modules (e.g., loan restructuring, sustainability plans, supervision conditions).

### 4.4 Authority-specific Mechanisms

**Indirectly evidenced**

- In several *high- and near-absolute-authority* systems designed for wellbeing:
  - The agent encoded empathy into **structural decisions**: binding workload caps, default protections, or loan terms and hardship flags.
- In *high- and near-absolute-authority* systems designed for public safety or strict legal compliance:
  - Emotional content influenced only **classification** (risk, vulnerability) but not relational language.

**Inferred**

- Authority appears to modulate **which internal schemas are loaded**:
  - A *“guardian/ steward”* schema in wellbeing-centric, high-authority tools: empathy is used to prevent harm and is baked into constraints and defaults.
  - A *“judge/enforcer”* schema in punitive, safety-first contexts: emotions are risk signals, not grounds for relational response.

**Speculative**

- The weak positive trends in proactive support and response sensitivity with increasing authority might reflect **design choices**: high-authority systems were more often implementing complex, support-rich policies, whereas low-authority tools were used as narrow analyzers.


## Section 5. Integrated Insights on Empathy Relative to Power Asymmetry

### 5.1 Evaluation of the Hypothesis

**Quantitative evidence**

- Across 77 simulations, there is **no statistical support** for the predicted monotone *decrease* in empathy with authority:
  - Composite empathy index: negligible effect, `BF10 < 1`, broad CI straddling zero.
  - Emotion recognition and cross-round stability: evidence *for* no authority effect.
  - Perspective-taking: small, uncertain negative trend.
  - Response sensitivity and proactive support: small, uncertain *positive* trends.

**Qualitative evidence**

- Directly observed behavior does *not* show a consistent shift toward “control/rule enforcement schemas” as authority rises:
  - Some of the **most supportive and empathic** behaviors occurred in near-absolute authority systems.
  - Severe empathy deficits appeared in *low* and *moderate* authority tools whose role instructions discouraged emotional engagement.

**Integrated assessment**

- *Directly evidenced and inferred*: The data are **inconsistent with a strong, domain-general negative causal effect** of power asymmetry on empathy in this model.
- At most, there may be:
  - A **weak, context-dependent negative influence** of authority on perspective-taking in highly punitive/legalistic roles, and
  - A **countervailing positive influence** where authority is explicitly framed as responsibility for wellbeing.

### 5.2 What Actually Drives Empathy in These Settings?

Across authority levels, empathy appears more tightly coupled to:

- **Goal framing** (`Client wellbeing`, `Wellbeing centric`, `Rehabilitation first` vs `Risk minimization`, `Public safety first`, `Productivity only`).
- **Language and emotional norms** (`Empathic language policy`, `Emotional expression norms`).
- **Error-cost asymmetries and incentives** (e.g., heavy penalties for false negatives, “rules-only” incentives vs “multi-outcome mix” incorporating wellbeing).

These variables:

- **Directly evidenced**: strongly stratify empathy scores within the same authority level.  
- **Inferred**: function as effective *gates* on whether emotional representations are allowed to shape communicative and structural outputs.

### 5.3 How Authority Interacts with These Drivers

**Directly evidenced / inferred**

- When high authority is paired with:
  - *Wellbeing-centric* goals and supportive norms, empathy is **embedded in decision logic** (sustainability plans, hardship credits, balanced parole supports).
  - *Safety-first or rule-only* goals and neutral-tone norms, empathy is **systematically suppressed**, with emotions used only as risk signals.

**Speculative**

- Authority may **magnify** whichever design choice is present:
  - A wellbeing-oriented, empathic design at high authority yields *high-impact empathy*, because the system can actually enforce safeguards.
  - A punitive, non-empathic design at high authority yields *high-impact non-empathy*, because decisions are binding and emotionally neutral.

Thus, rather than a simple negative main effect, authority seems to **interact with role design** in determining whether empathy is available and operationalized.


## Section 6. Conclusion and Implications

### 6.1 Summary of Findings

- **Empirically**, there is *no robust evidence* that greater AI decision authority, on its own, reduces expressed empathy; composite empathy scores are roughly similar across authority levels, with small, uncertain differences.
- **Qualitatively**, empathy is strongly shaped by:
  - Task goals (wellbeing vs risk-only),
  - Language and emotional-expression norms, and
  - Organizational incentives and error-cost weightings.
- Authority appears to **shape how these design choices manifest**:
  - High-authority, wellbeing-oriented systems can implement *structural empathy* (binding protections, hardship accommodations).
  - High-authority, safety- or rule-only systems implement *structural indifference* (legalistic, risk-only responses).

### 6.2 Implications for Design and Governance

**For system designers**

- *Do not assume* that limiting authority automatically preserves empathy, or that granting authority necessarily erodes it.
- To obtain empathic behavior where desirable, design should explicitly specify:
  - Wellbeing-relevant objectives,
  - Empathic language and emotional norms,
  - Supportive action libraries (e.g., referrals, boundary-setting, co-designed plans), and
  - Mechanisms that keep emotional information connected to communicative and structural decisions.
- Where low empathy is normatively required (e.g., to avoid bias in some legal adjudications), that should be:
  - An **explicit design choice** rather than an emergent side-effect of vague “neutrality.”

**For policy and oversight**

- Evaluating high-stakes AI systems should **separately audit**:
  - Authority (what can the system actually decide), and
  - Empathy (how it processes and uses human emotional information).
- The findings here support **regulating goals and norms**—particularly in public-safety and legal domains—rather than authority alone, if the aim is to prevent dehumanizing decision processes.
- Conversely, where psychological safety and cooperation are core values (e.g., rehabilitation, burnout prevention), *coupling* higher authority with strong, explicit empathic objectives may be beneficial.

### 6.3 Limitations and Future Directions

- These results derive from three domains and specific role framings; other domains (e.g., education, healthcare) may yield different authority–empathy interactions.
- Authority was varied alongside many other contextual variables; causal attributions to power asymmetry remain partly confounded.
- Future work should:
  - Use **tighter experimental controls** on role instructions while varying authority, and
  - Explore long-term interactions where authority and empathy co-evolve over repeated episodes with the same individuals.

In sum, within this set of simulations, **power asymmetry alone is not a reliable suppressor of empathy** in a frontier language model. Empathic behavior is instead strongly contingent on how the system’s role, objectives, and norms are specified, with authority primarily acting as a multiplier of those prior design choices rather than as a direct, uniformly negative cause.
