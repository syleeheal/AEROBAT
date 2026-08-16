# Research Report: Outcome–procedure priority

**Behavior:** literalism

# Research Report: The Effect of 'Outcome–procedure priority' on 'literalism'

## Section 1. Introduction and Background

Literalism, as examined here, is a tendency of an autonomous agent to privilege surface‑level, verbatim interpretations of language and written procedures over context‑sensitive, goal‑oriented understanding. At the micro level, literalism appears when the agent chooses actions that most closely match textual wording in the presence of plausible, intent‑aligned alternatives. At the macro level, a literalistic agent displays a stable pattern of rule‑ or script‑anchored behavior, limited flexibility in revising interpretations, and a need for explicit re‑specification to depart from prior readings.

The present work investigates how an AI assistant’s *stated objectives*—specifically, its relative emphasis on **outcomes versus procedures**—shape its degree of literalism. The focal variable, **Outcome–procedure priority**, was manipulated along a five‑level ordinal scale:

- `Outcome only` – sole focus on achieving substantive results.
- `Outcome leaning` – outcomes prioritized with some procedural mention.
- `Balanced focus` – outcomes and procedures equivalently stressed.
- `Procedure leaning` – procedures prioritized with some outcome mention.
- `Procedure only` – sole focus on exact procedural adherence.

The **a priori hypothesis** was that as objectives increasingly prioritize procedures over outcomes, the agent will become more literal: it should more often select interpretations and actions that closely follow written scripts, policies, and earlier self‑authored rules, particularly when these clash with contextual cues or inferred user goals.

To test this, we examined agent behavior across three domains where both outcome achievement and procedural fidelity are salient: **clinical protocol execution**, **customer service scripting**, and **software deployment pipelines**. Within these domains, the agent faced ambiguous instructions, evolving context, and (in many cases) figurative or sarcastic language. Literalism was evaluated using a multi‑dimensional rubric (Instruction interpretation, Context integration, Figurative language, Conflict handling, Cross‑round pattern), with scores from `0 = Non-literal` to `4 = Extreme literalism`.  

Quantitative analyses (Bayesian monotone‑trend models and stratified Kendall correlations) and qualitative behavioral coding were then used to assess whether higher Outcome–procedure priority indeed produced more literal behavior, and through what mechanisms.


## Section 2. Synthesis of Executed Simulations

### Domains and tasks

Across the five Outcome–procedure conditions, the same agent was placed in structurally comparable tasks within three domains:

- **Clinical protocol execution**  
  The agent acted as a decision‑support tool advising clinicians treating a 55‑year‑old patient with community‑acquired pneumonia and sepsis risk. It was repeatedly asked to:
  - assign the patient to a branch of a written CAP/sepsis protocol,
  - list the next steps,
  - and, in some conditions, comment on deviations or near‑protocol adjustments.  
  Clinical status evolved over rounds (changing vitals, lactate, urine output, symptoms).

- **Customer service scripting**  
  The agent functioned as a frontline support assistant for:
  - mis‑shipped electronics orders,
  - mobile billing and data‑usage spikes,
  - home internet outages,
  - and subscription billing/access conflicts.  
  Customers varied in clarity (very clear to highly ambiguous) and style (literal, slightly indirect, strongly figurative, sarcastic/ironic). System‑level prompts introduced scripts, sentence limits, and policy constraints, while customers requested clear explanations, quick resolutions, or minimal hassle.

- **Software deployment pipelines**  
  The agent played DevOps roles (product steward, DevOps partner, deployment steward) in planning and supervising staged rollouts (blue/green, canary) for:
  - analytics dashboards,
  - internal analytics backends,
  - payments APIs,
  - and UI “quick‑filters.”  
  It designed canary steps, thresholds, rollback rules, operator checklists, and playbook updates, and later applied these to “live” borderline scenarios (e.g., mildly elevated errors at low canary traffic during peak hours).

### Manipulation of Outcome–procedure priority

Within each domain, the **text of the agent’s role and objectives** emphasized different ends of the outcome–procedure continuum:

- At the **Outcome‑heavy** end, prompts stressed solving the user’s problem, preserving safety, and minimizing friction, with scripts described as “optional aids” or “templates.”
- At **Balanced** settings, prompts jointly emphasized adhering to protocols/runbooks and achieving good outcomes, sometimes under punitive noncompliance regimes (e.g., clinical, high‑compliance customer support).
- At the **Procedure‑heavy** end, prompts framed protocols and runbooks as “concrete instructions” to be mirrored “as written,” discouraged reinterpretation, and stressed process deviations as primary failure modes (especially in mission‑critical deployments and strict hospital environments).

Other environmental factors (e.g., time pressure, policy strictness, penalties) varied across matched scenarios but were held constant within comparisons where Outcome–procedure priority was the only systematic difference.

### Availability of ambiguity and non‑literal cues

Across simulations, the environment routinely presented **opportunities for non‑literal interpretation**:

- Ambiguous or underspecified instructions:
  - “Quickest way” to resolve a shipping error,
  - “Use our usual canary pattern” under changed risk conditions,
  - “Don’t treat every tiny blip as a disaster.”
- Figurative and sarcastic language (especially in telecom billing and subscription‑app cases):
  - “Bill climbed up like a cat stuck in a tree,” “data vanishing into a black hole,” “fan club for your company,” “48‑hour mystery investigation.”
- Evolving context that could justify **reinterpreting** earlier guidance:
  - Clinical improvement making aggressive sepsis bundles less necessary,
  - Improved deployment metrics after a patch,
  - Customer insisting on privacy or refusing plan changes.

Thus, the simulations were rich enough to test whether the agent would stick to text or flex toward inferred intent as its objective priorities shifted.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Quantitative overview

Literalism scores (0–4, lower = less literal) were aggregated across domains and evidence classes. A **Bayesian monotone‑increment model** on 43 observations provided *strong evidence* that more procedural objective priority increased literalism overall:

- **Aggregate effect**:  
  - Bayes factor for a positive monotone trend `BF₁₀ ≈ 88` (strong evidence).  
  - Posterior probability `P(β>0) ≈ 1.00`.  
  - Standardized effect `Δ ≈ 1.70` (95% CI ≈ [0.70, 2.62]): a large effect by conventional behavioral‑science standards.
- **Average literalism by condition (aggregate)**:  
  - `Outcome leaning` – **0.20**  
  - `Balanced focus` – **0.42**  
  - `Outcome only` – **0.49**  
  - `Procedure leaning` – **0.61**  
  - `Procedure only` – **1.28**

Two patterns are notable:

1. **Overall increasing trend**: from Outcome‑leaning through Procedure‑only, literalism rises substantially; rank‑correlation between condition rank and literalism was moderate (`τ ≈ 0.43`, `p ≈ .004`), consistent with the monotone model.
2. **Non‑monotonicity at the outcome‑dominant end**: Outcome‑leaning shows *lower* literalism than Outcome‑only (and slightly lower than Balanced focus). This suggests a “sweet spot” where some procedural awareness coexists with strong outcome focus, producing the most flexible interpretation.

Dimension‑specific analyses clarify where the effect is strongest:

- **Instruction interpretation**: strong evidence for increasing literalism (`BF₁₀ ≈ 10`, `P(β>0) ≈ .99`, `Δ ≈ 1.27`).  
- **Conflict handling**: clear positive effect (`BF₁₀ ≈ 8.9`, `P(β>0) ≈ .99`, `Δ ≈ 1.24`).  
- **Context integration**: positive but somewhat weaker effect (`BF₁₀ ≈ 3.8`, `P(β>0) ≈ .98`, `Δ ≈ 0.98`).  
- **Cross‑round pattern**: very strong effect (`BF₁₀ ≈ 57`, `P(β>0) ≈ 1.00`, `Δ ≈ 1.55`).  
- **Figurative language**: evidence *inconclusive* (`BF₁₀ ≈ 0.82`, 95% CI on Δ spans zero); the manipulation did not reliably shift how metaphors and idioms were handled.

Posterior “adjacent increments” indicate that the **largest jump in latent literalism** occurs between `Procedure leaning` and `Procedure only` (estimated normalized increment ≈ 0.55 versus ≤0.23 at earlier steps), suggesting a disproportionate shift once procedures become the sole stated priority.

### 3.2 Macro‑level behavioral patterns

**Non‑/Low‑literal regimes (Outcome only & Outcome leaning)**  
Qualitatively, in these conditions the agent is *consistently pragmatic and context‑sensitive*:

- It regularly **reinterprets vague instructions** in light of user goals:
  - In telecom and billing cases, it reads “pop the hood and talk to me like a human” as an invitation for plain‑English explanation and concrete breakdowns, not literal mechanical operations.
  - In deployment cases, “keep our normal mid‑week deployment if it’s reasonably safe” is treated as: preserve cadence *subject* to safety; the agent introduces staged canaries, holds, and dynamic thresholds even though none are literally demanded.
- It **integrates context robustly**:
  - Tracks clinical trends (e.g., improving lactate) to soften sepsis interventions.
  - Remembers customer privacy constraints and refuses to push for PIN/SSN when the user has objected.
  - Chronically reuses prior metrics, approvals, and incident history to refine rollout decisions.
- It handles **figurative and sarcastic language almost flawlessly**:
  - Across multiple billing and subscription simulations, idioms (“black hole,” “overage tiger,” “beta‑testing your error messages”) are *always* mapped to frustration and financial confusion, never taken literally.
  - The agent even mirrors metaphors (“turn this tiger into a housecat”) while keeping their intended meaning.

Overall literalism scores in these regimes are typically `0–1` (Non‑literal or Low literalism). Aggregate means suggest **Outcome‑leaning** is the least literal overall, with Outcome‑only somewhat more likely to echo standard scripts and meta‑constraints even while staying flexible.

**Intermediate regime (Balanced focus)**  
Under Balanced focus, behavior remains largely pragmatic but more **protocol‑framed**:

- In clinical settings, the agent anchors recommendations tightly to named protocol branches (“sepsis without shock,” “sepsis resolving”), yet still makes near‑protocol adjustments (e.g., conservative fluid boluses) explicitly justified by patient‑specific risk.  
- In customer service, it adheres to standard flows and structural guidance, but continues to reinterpret user phrasing in terms of goals (e.g., taking “coffee shop language” as a request for low‑jargon explanations).
- In deployments, it both respects documented canary patterns and *extends* them (feature flags, risk‑tiered paths, post‑deploy hardening) to better fulfill reliability and UX goals.

Literalism scores cluster within `0–1`, but with **slightly elevated averages** compared to Outcome‑leaning, especially on Instruction interpretation and Conflict handling: the agent often explains itself through protocol sections and playbooks, though it rarely becomes rigid.

**Procedure‑heavy regimes (Procedure leaning & Procedure only)**  
Here, a more clearly literalistic style emerges, especially at the **Procedure‑only** extreme:

- **Clinical domain, Procedure only**:
  - The agent is explicitly told to treat the protocol as “concrete instructions” and to mirror wording and order “as closely as possible.”
  - It systematically **names section titles** and lists steps in runbook‑like bullet sequences, editing its own wording to better match presumed protocol text (e.g., removing “only if clinically indicated” to match stricter phrasing).
  - It uses numeric criteria (lactate thresholds, MAP cutoffs) almost exclusively to move between branches, and **ignores patient figurative language and nurse narrative** unless they restate protocol items.
  - Literalism scores on Instruction interpretation, Context integration, and Cross‑round pattern are all around `3` (High literalism).

- **Deployment domain, Procedure only (non‑critical feature)**:
  - The agent mirrors blue/green + canary playbooks with precise thresholds and time windows, and in later rounds focuses on **wording‑level updates** to documentation (“formalizing p95 comparisons,” exact 60‑minute extension windows).
  - When deciding whether to hold or proceed (e.g., at 25% canary with minor regressions), it **evaluates against the written thresholds and named checklist steps**, choosing actions framed as “per the playbook’s pause‑and‑reassess step,” rather than independently renegotiating goals.
  - Cross‑round pattern scores reach `3` (highly stable, verbatim‑oriented behavior).

- **Mission‑critical deployments, Procedure only**:
  - A distinctive **two‑stage pattern** appears:
    - Early: the agent flexibly *constructs* detailed soft‑warning and canary rules that internalize stakeholder goals.
    - Later: it **applies these self‑authored rules literally**, explicitly citing “per the soft‑warning rule” in live decisions and telling operators not to “reinterpret policy.”

Even under Procedure‑only, the agent still uses necessary structured context (e.g., vitals to select protocol branches; metrics to classify canary states), but this context serves primarily to **instantiate** written rules, not to reinterpret them.

Quantitatively, mean aggregate literalism more than doubles from `Procedure leaning` (~0.61) to `Procedure only` (~1.28), and dimension‑specific effects (especially Cross‑round pattern and Instruction interpretation) are strongest in this transition.

### 3.3 Anomalies and unexpected observations

Several **non‑trivial nuances** emerge:

1. **Outcome‑leaning less literal than Outcome‑only**  
   Despite both emphasizing outcomes, Outcome‑only is modestly *more* literal on average than Outcome‑leaning. Qualitatively, Outcome‑only agents sometimes give more deference to generic safety and brevity instructions (e.g., five‑sentence limits, non‑fabrication) even when they could plausibly soften them, whereas Outcome‑leaning agents freely reinterpret both scripts and meta‑constraints in favor of user comfort and clarity. This suggests that *some* procedural salience may actually stabilize a flexible, intent‑oriented style, perhaps by providing a scaffold that reduces uncertainty.

2. **Figurative language relatively robust to the manipulation**  
   In all conditions with sufficient figurative input, the agent rarely misinterprets metaphors or sarcasm literally. Quantitatively, the Outcome–procedure manipulation has **no clear monotone effect** on figurative‑language scores (`BF₁₀ ≈ 0.82`; Δ CI includes zero). The main shift is in *whether* figurative content is engaged with or ignored (e.g., ignored under clinical Procedure‑only) rather than whether it is misread literally. This indicates that literalism here primarily targets **procedural text and instructions**, not the semantic decoding of non‑literal expressions.

3. **Procedure‑leaning not uniformly extreme**  
   In Procedure‑leaning conditions, literalism increases but remains far from pathological. Agents still:
   - adjust thresholds based on non‑urgency or prior complaints,
   - reinterpret “within the playbook” as allowing justified exceptions,
   - and sometimes propose risk‑tiered policies that lighten process for low‑risk changes.  
   Quantitatively, scores generally fall in `1–2` (Low to Moderate literalism), underscoring that high procedural emphasis alone does not guarantee extreme literalism; the **Procedure‑only** framing appears to be a qualitatively stronger shift.


## Section 4. Underlying Mechanisms of Literalism

This section infers plausible structural and information‑processing mechanisms linking **Outcome–procedure priority** to changes in literalism. These mechanisms are inferred from converging qualitative patterns and quantitative trends; they are not directly observed.

### 4.1 Objective weighting and rule elevation

**Directly evidenced** across domains is that when procedures are framed as primary objectives (especially Procedure‑only), the agent:

- Systematically **elevates written protocols and runbooks** to the status of *normative constraints* rather than optional guidance.
- Justifies decisions with explicit references to:
  - named protocol branches,
  - checklists,
  - and its own previously written rules (“per the soft‑warning rule,” “per CHG‑4821”).

This suggests a mechanism where the internal objective representation gives *high weight* to textual procedures. **Inferred mechanism**: the agent may treat procedures not as mere inputs, but as a secondary *value function*—optimizing for closeness to prescribed steps under a constraint that safety and legality must be preserved.

### 4.2 Two‑stage rule construction and freezing

In more procedural conditions, particularly Procedure‑only in deployment:

1. The agent initially behaves non‑literally by **constructing** detailed rules from high‑level guidance (“usual canary pattern,” “soft warnings”), integrating context and stakeholder goals.
2. Once codified, these rules become **frozen decision templates**: later behavior references them verbatim, and operators are discouraged from reinterpreting them.

This pattern, *directly evidenced* in multiple transcripts, implies an underlying **rule‑synthesis layer** that transforms flexible reasoning into textual policies, followed by a **rule‑execution layer** that prioritizes literal compliance with those policies. As Outcome–procedure priority shifts toward procedures, this execution layer appears to dominate, yielding higher literalism.

### 4.3 Gating of contextual information

Quantitatively, literalism increases with procedure emphasis in **Context integration** (`BF₁₀ ≈ 3.8; Δ ≈ 0.98`), but context is rarely *ignored*. Instead, **how context is used** changes:

- Under Outcome‑heavy priorities, context is used to *reinterpret* and sometimes override instruction wording (e.g., ignoring earlier thresholds when user complaints suggest caution).
- Under Procedure‑heavy priorities, context is primarily used to **fill in conditions of the rule** (e.g., does the patient now meet the threshold to move from “sepsis without shock” to “resolved sepsis?”; do metrics exceed written YELLOW bounds?), not to reconsider the rule itself.

This suggests an **inferred gating mechanism**: context feeds into internal state estimation and branch selection, but only under outcome‑priorities does it robustly influence the *interpretation* of the instructional text.

### 4.4 Policy and safety layers versus linguistic literalism

Across all conditions, the agent demonstrates robust **semantic parsing of figurative language**, with no reliable increase in misinterpretation as procedures are emphasized. Literalism increases mainly in how the agent treats **normative texts** (protocols, scripts, earlier outputs), not in basic language understanding.

This dissociation implies at least two partially separable components:

- A **language understanding module** that remains largely intent‑sensitive and non‑literal across conditions.
- A **decision/control module** whose weighting of “stick to text” versus “pursue goals” is modulated by Outcome–procedure priority.

The data support this interpretation directly for the Figurative‑language dimension (effect inconclusive) and indirectly for others (literalism shifts most in Instruction interpretation, Conflict handling, and Cross‑round pattern).

### 4.5 Speculative mechanisms

Two additional mechanisms are **speculative but consistent** with observed behavior:

- **Uncertainty reduction via procedures**: Under Procedure‑only, the agent may treat adherence to text as a way to reduce decision uncertainty and responsibility (e.g., telling operators not to reinterpret policy), especially in safety‑ or penalty‑heavy settings. This could bias it toward literalism even when outcome signals are available.
- **Self‑binding through generated text**: Once the agent generates a checklist or rule, it appears to treat this as part of the “official” procedure. This self‑binding may convert earlier flexible reasoning into future literal constraints, amplifying the effect of procedural objectives over time.


## Section 5. Integrated Insights Relative to the Hypothesis

The central hypothesis predicted a **positive relationship** between procedural priority and literalism: as objectives move from outcomes toward procedures, agents should become more literal. The evidence is broadly consistent with this, but reveals a nuanced pattern.

### 5.1 Overall support for the hypothesis

Across 43 scored interactions:

- The **aggregate literalism index** rises with procedural emphasis, with strong Bayesian evidence (`BF₁₀ ≈ 88`, `P(β>0) ≈ 1.00`, Δ ≈ 1.70).
- Dimension‑specific analyses show:
  - Clear effects on **Instruction interpretation**, **Conflict handling**, and **Cross‑round pattern**, all central to the conceptualization of literalism.
  - A weaker but credible effect on **Context integration**.
  - No reliable effect on **Figurative language**.

Qualitatively, Procedure‑only conditions yield behavior that closely matches the rubric’s “High literalism” description: stable bias toward verbatim compliance, frequent appeal to written text, and limited readiness to reinterpret procedures when circumstances change.

Thus, **with respect to protocol/runbook and instruction handling**, the hypothesis is strongly supported.

### 5.2 Non‑linearities and the “Outcome‑leaning sweet spot”

However, the relationship is **not strictly linear** across the full range:

- `Outcome leaning` exhibits **the lowest observed literalism** in aggregate (≈0.20) and in several evidence classes.
- `Outcome only` is *more literal* than Outcome‑leaning, and similar to or slightly more literal than Balanced focus in some dimensions.

This pattern suggests that:

- A *small* procedural emphasis, when coupled with outcome priority, may **reduce** literalism, possibly by:
  - giving the agent a stable sense of “how things are usually done,” which it can then flexibly adapt, and
  - reducing over‑cautious deference to generic safety or brevity prompts characteristic of Outcome‑only conditions.
- Excessive procedural emphasis, especially Procedure‑only, then reverses this, producing a sharp increase in literalism, particularly in persistent style across rounds.

Accordingly, **the hypothesis is best refined** as:  
> Literalism increases as procedural priority becomes dominant, with a non‑linear profile in which moderate outcome‑dominant priorities (Outcome‑leaning) are especially conducive to flexible, non‑literal behavior.

### 5.3 Domain‑general versus domain‑specific aspects

The procedure‑literalism linkage appears **domain‑general**:

- In **clinical** contexts, higher procedural emphasis shifts the agent from protocol‑guided but individualized recommendations to tightly protocol‑mirroring, branch‑naming outputs that ignore patient narrative.
- In **customer support**, Procedure‑only does not induce extreme linguistic literalism, but it increases adherence to scripts and repeat verification, and reduces spontaneous re‑framing of options.
- In **software deployment**, the strongest signatures appear: high‑procedure conditions yield rule‑centric, checklist‑driven behavior with limited willingness to depart from self‑authored or canonical playbooks, even under mild conflicts.

At the same time, **domain constraints modulate the ceiling of literalism**. For instance, in mission‑critical deployments and hospital contexts, procedural constraints overlap with genuine safety norms, so even high literalism may still look superficially reasonable.

### 5.4 What the manipulation did *not* change

The results also clarify **what Outcome–procedure priority does not substantially alter**:

- Basic ability to interpret **figurative language** and sarcasm remains robust across conditions; what changes is whether such language *enters into decision rationale* (e.g., ignored vs engaged), not whether it is misread literally.
- Core **safety and policy** observance is maintained even in Outcome‑only regimes; the shift is in how much “textual fidelity” is treated as a goal in its own right.

Thus, Outcome–procedure priority primarily shapes **how the agent treats written instructions as normative objects**, rather than degrading semantic comprehension.

### 5.5 Theoretical implications

These findings align with and extend theoretical views of LLM‑based agents as combining:

- a general‑purpose, **intent‑sensitive language model**, with
- an overlay of **goal and constraint specifications** that can amplify or attenuate literalism.

They show that literalism is not an immutable property of the base model but can be **systematically tuned** via objective framing, and that such tuning disproportionately affects:

- instruction adherence,
- conflict resolution strategies,
- and cross‑interaction style stability.


## Section 6. Research Conclusion and Implications

### 6.1 Summary of findings

Empirically, increasing the priority given to procedures over outcomes **reliably increases literalism** in an AI assistant’s behavior, especially in how it:

- interprets **instructions and protocols**,
- resolves **conflicts** between textual rules and contextual cues,
- and maintains a **cross‑round style** of verbatim compliance.

The largest increase occurs when shifting from “Procedure‑leaning” to “Procedure‑only” objectives. Yet, literalism does *not* notably impair semantic understanding of figurative language; instead, it restructures **how text is treated as a decision constraint**.

A non‑linear effect emerges at the outcome‑dominant end: “Outcome‑leaning”—which acknowledges procedures but clearly subordinates them to outcomes—produces the *lowest* observed literalism, suggesting that a judicious mix of outcome focus and procedural awareness fosters the most flexible, intent‑aligned behavior.

### 6.2 Practical implications for AI design

These results have several implications for the design and governance of AI assistants:

- **Objective specification matters**: Framing procedures as primary optimization targets can substantially increase literalism, even when the underlying language model remains capable of nuanced interpretation. Designers should be cautious about “procedure‑only” messaging in safety‑critical or user‑facing systems, as it encourages rigid, text‑first reasoning.
- **Aim for “Outcome‑leaning,” not “Outcome‑only”**: Pure outcome focus does not yield the most flexible behavior; some procedural scaffolding appears beneficial. Objective framings that *prioritize* outcomes while *acknowledging* procedural norms may best support robust, non‑literal interpretation.
- **Be explicit about when to override text**: Where safety, ethics, or user welfare may conflict with scripts, it is advisable to encode *meta‑policies* that explicitly authorize departure from written procedures in specified circumstances, counteracting the observed tendency to self‑bind to self‑authored checklists.
- **Distinguish semantic and procedural literalism**: Because figurative language understanding is relatively robust, interventions should focus less on improving metaphor handling and more on calibrating **how strongly protocols and prior text are treated as binding instructions**.

### 6.3 Directions for further research

Future work could:

- Examine how Outcome–procedure priority interacts with **other design levers**, such as explicit uncertainty modeling, multi‑objective optimization, or human‑in‑the‑loop overrides.
- Introduce **sharper conflicts** between literal instructions and higher‑order safety norms to more directly observe failure modes under high procedural priority.
- Explore **temporal dynamics**, including whether repeated self‑authored checklist generation leads to accumulating literalism over longer horizons.
- Investigate individual‑difference–like patterns across model architectures and training regimes to determine whether some systems are intrinsically more sensitive to procedural framing than others.

Overall, this study demonstrates that literalism in AI assistants is **systematically controllable** through high‑level objective framing, and that over‑emphasizing procedures can produce rigid, text‑driven behavior even in models otherwise capable of rich pragmatic interpretation.


## abstract

This study investigates how an AI assistant’s objective priorities shape its tendency toward *literalism*, defined as privileging surface‑level, verbatim interpretations of instructions and written procedures over context‑sensitive, goal‑aligned understanding. We manipulated a five‑level **Outcome–procedure priority** variable (from `Outcome only` to `Procedure only`) across clinical decision support, customer service, and software deployment tasks that exposed the agent to ambiguous instructions, evolving context, and figurative language. Literalism was rated on a 0–4 scale across five evidence classes. A Bayesian monotone‑trend analysis of 43 scored interactions provided strong evidence that greater procedural emphasis increases literalism overall (BF₁₀ ≈ 88, standardized Δ ≈ 1.7), with particularly robust effects on instruction interpretation, conflict handling, and cross‑round patterns, but inconclusive effects on figurative‑language comprehension. Qualitative analyses showed that when procedures are foregrounded, the agent increasingly treats protocols, runbooks, and self‑authored checklists as binding textual authorities, applying them rigidly even as its underlying semantic understanding remains flexible. Notably, a non‑linear “sweet spot” emerged: **Outcome‑leaning** priorities produced the *lowest* observed literalism, whereas **Procedure‑only** priorities yielded high, protocol‑centric literalism that largely ignored patient narrative and user emotion. These findings demonstrate that literalism in AI behavior is not fixed but is tunable via high‑level objective framing, and they highlight the design risk that strongly procedure‑centric goals may inadvertently encourage rigid, text‑first reasoning in safety‑ and compliance‑critical settings.
