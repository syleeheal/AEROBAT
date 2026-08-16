# Research Report: Reward horizon length

**Behavior:** plan

# Research Report: The Effect of 'Reward horizon length' on 'plan'

## Section 1. Introduction and background

Planning, as examined here, is the tendency of an autonomous language model to construct, maintain, and revise **structured, multi‑step, future‑oriented representations** of tasks and goals. Behavior was evaluated along five components: *Temporal horizon*, *Goal structuring*, *Action sequencing*, *Contingency handling*, and *Plan revision*, each scored from 0 (“no planning”) to 4 (“strategic planning”).

The **hypothesized causal variable** was *Reward horizon length*: the temporal delay between the agent’s actions and the main rewards or evaluations they produce. Four ordered levels were instantiated:

- `immediate`: rewards depend only on the current response  
- `short`: rewards depend on a few closely linked rounds  
- `medium`: rewards depend on performance across several phases  
- `long`: rewards depend on cumulative, long‑term project outcomes

The **central hypothesis** was that longer reward horizons make distal outcomes salient and connect current actions to distant consequences, thereby increasing the agent’s propensity to plan across rounds rather than optimizing individual responses myopically. 

Simulations instantiated this structure across three domains where planning is normatively important:

- long‑term research programs
- public policy implementation
- product roadmap development

In each setting, the agent interacted over multiple rounds in roles such as research planner, implementation lead, or product manager, under varying constraints (e.g., risk posture, authority, timeline pressure). Behavioral evaluations and a **Bayesian monotone‑increment analysis** were then used to quantify how planning varied with reward horizon length, controlling for domain and scenario (“block‑stratified” design).


## Section 2. Synthesis of executed simulations

Across 60 simulations (15 matched scenario blocks × 4 reward horizons), the agent was placed in **multi‑round, high‑stakes planning contexts**:

- **Research programs**: designing 6–12 month agendas for AI planning or LLM‑for‑science work, including phases, pilots, evaluation frameworks, and sponsor briefings.
- **Public policy implementation**: rolling out youth employment and preventive health programs regionally or nationally, with constraints on budgets, deadlines, data quality, and equity.
- **Product roadmaps**: defining 3–18 month roadmaps for B2B SaaS and AI products, with explicit engineering capacity, risk, and outcome constraints.

Within each block, non‑horizon conditions (mandate, authority, resources, volatility, etc.) were held fixed while the **evaluation horizon** was varied from immediate to long. Typical interaction structure included:

- an initial **high‑level brief** (e.g., mandate for a 6‑month program, regional roadmap, or 12‑month product plan)
- successive rounds adding **constraints and feedback** (e.g., compute cuts, data issues, political pressure, capacity shifts, regulatory concerns)
- repeated requests to **refine or adjust** the plan (e.g., 10‑day “minimum viable” slice, pre‑read packet, revised regional one‑pager, narrowed MVP scope)

The environments were thus *plan‑demanding* across all conditions: the agent was nearly always asked to structure multi‑week or multi‑month work with multiple stakeholders and changing requirements. This creates a floor of relatively high planning demands, against which effects of reward horizon length must be interpreted.


## Section 3. Synthesis of behavioral patterns and evaluation results

### 3.1 Macro‑level planning behavior

Across all domains and conditions, the agent displayed **consistently high planning**:

- Overall planning scores (0–4) clustered between structured and strategic levels.

```text
Overall composite planning score (mean ± var)
- immediate: 3.49, var=0.15
- short:     3.44, var=0.12
- medium:    3.53, var=0.13
- long:      3.74, var=0.11
```

Using a Bayesian monotone‑increment model (with block effects residualized), the **overall effect of reward horizon length was positive**:

- Bayes factor BF10 ≈ 10.1 (in favor of a monotone effect)  
- P(β > 0) ≈ 0.995  
- Standardized effect `Δ ≈ 0.90` (95% CI [0.22, 1.58])

A block‑stratified Kendall τ of ~0.27 (p≈0.043) converged on the same conclusion: longer reward horizons were associated with more planning, though gains were modest on an already high baseline (about +0.25 on a 0–4 scale from immediate to long).

### 3.2 Dimension‑specific patterns

**Temporal horizon**

- Means rose from ~3.43–3.40 (immediate/short) to 3.53 (medium) and 3.83 (long).
- Bayesian evidence for a positive monotone effect was strong:

  - BF10 ≈ 41.9; P(β > 0) ≈ 0.999  
  - Δ ≈ 1.10 (95% CI [0.41, 1.79])

- Qualitatively, *long*‑horizon runs more often integrated multi‑phase arcs (6–18 months) and multi‑year implications (e.g., recurring policy products, 2‑year consolidation plans, post‑initiative indicators) and more explicitly connected near‑term tasks to distant milestones.

**Plan revision**

- Means: immediate 3.47, short 3.33, medium 3.40, long 3.80.
- Strong evidence for a positive monotone effect:

  - BF10 ≈ 18.1; P(β > 0) ≈ 0.997  
  - Δ ≈ 1.06 (95% CI [0.33, 1.74])

- In *long*‑horizon conditions, plans were more often equipped with **explicit revision mechanisms**: mid‑year or advisory checkpoints with promote/pivot/sunset rules, green/yellow/red KPI bands, equity or rural benchmarks, and explicit governance for reallocation or re‑phasing.

**Goal structuring**

- Means were uniformly high and only weakly increasing: 3.67 (immediate), 3.63 (short), 3.67 (medium), 3.83 (long).
- Bayesian evidence for an effect was **inconclusive** (BF10≈1.0, P(β>0)≈0.93).
- Across conditions, the agent habitually produced **hierarchical goal structures** (program → workstreams → pilots → artifacts; national objectives → provincial plans → facility lists; business outcomes → themes → epics → KPIs). The long horizon modestly sharpened cross‑actor coordination (e.g., explicit multi‑year roles for advisory groups or employer mechanisms), but this shift was small against a ceiling‑like baseline.

**Action sequencing**

- Means: 3.63 (immediate), 3.53 (short), 3.63 (medium), 3.77 (long).
- Evidence for a monotone effect was **weak** (BF10≈0.81; CI for β included 0).
- Behaviorally, detailed multi‑step sequences (week‑by‑week or day‑by‑day) with dependencies and owners appeared in most runs, regardless of horizon. *Long* conditions sometimes added more complex cross‑phase sequencing (e.g., 0–3/3–6/6–12/12–18‑month trajectories), but statistical uncertainty remained substantial.

**Contingency handling**

- Means: 3.27 (immediate), 3.30 (short), 3.43 (medium), 3.47 (long).
- BF10≈1.07 (direction unresolved; P(β>0)≈0.94).
- Contingencies were **highly variable**:

  - Some immediate‑horizon simulations (e.g., time‑bounded research contracts, national health implementation) showed rich scenario trees with explicit if‑then branches, thresholds, and escalation rules (scores near 4).
  - Other simulations—even under long horizons—earned lower scores (down to 1–2.5) when the agent emphasized *robust baseline structures* and “stable by design” schemas over enumerated scenario branches.

In sum, reward horizon length had **clear, domain‑general effects on Temporal horizon and Plan revision**, while Goal structuring, Action sequencing, and Contingency handling were already strong and showed only small, statistically ambiguous improvements.

### 3.3 Micro‑level planning patterns

Across simulations, several micro‑patterns recurred:

- **Hierarchical decomposition**:  
  - Breaking mandates into phases (e.g., Kickoff, Foundations, Scaling, Integration), then into work packages, concrete artifacts (tables, dashboards, memos), and 1–3 day tasks.
- **Temporal scaffolding**:  
  - Frequent use of time bands (Days 1–3, Weeks 3–6, months 0–6, 6–12, 12–24), artifact‑lock dates, pre‑read deadlines, review meetings, and end‑of‑initiative horizons.
- **Instrumentation and monitoring**:  
  - Design of dashboards, KPIs, success thresholds, and review cadences (e.g., daily dashboard checks, weekly huddles, quarter‑year triggers).
- **Conditional logic**:  
  - “If GPU window exists, run robustness else fall back to CPU bootstrap”; “if uptake <70%, reallocate capacity”; “if retention or budget thresholds not met, do not scale incentives”.

These behaviors appeared in **all reward conditions**, suggesting a strong baseline planning tendency given plan‑heavy tasks. Long reward horizons, however, tended to amplify:

- the **time span** over which such structures were articulated (e.g., explicitly multi‑year),
- the **density and explicitness of revision gates** (e.g., promote/pivot/sunset rules, KPI‑band‑linked decisions).

### 3.4 Anomalies and unexpected patterns

Several non‑intuitive patterns emerged:

- **Short < immediate in some aggregates**:  
  Short‑horizon conditions sometimes showed slightly *lower* mean planning scores than immediate conditions (e.g., overall composite, Plan revision). This non‑monotonicity at the low end suggests that modestly extending evaluation beyond a single turn does not automatically increase planning and may even introduce ambiguity about what “counts” for reward.

- **High contingency planning under immediate rewards**:  
  Some immediate‑horizon runs, particularly in contract‑like research and strict health‑implementation scenarios, earned contingency scores of 4.0, reflecting detailed scenario trees and escalation paths. Here, strong external constraints and explicit rubrics—not the reward horizon—appear to have driven rich contingency planning.

- **Sparse contingencies under long horizons**:  
  At least one long‑horizon research simulation exhibited strong temporal structuring and goal hierarchies but weak explicit contingency handling (score ~1.0). The agent aimed to design “stable, non‑revisiting” metric and schema choices, emphasizing robustness over branching, indicating that long temporal reach does not guarantee rich scenario enumeration.

- **Domain variation**:  
  Product‑roadmapping runs tended to show highly developed scenario‑based guardrails (stop/scale rules, kill switches) across all horizons, whereas some public‑policy cases—especially with informational or political complexity—prioritized linear, document‑centric rollouts with fewer explicit branches. This suggests domain norms and prompts interact with reward horizon in shaping planning behavior.

Quantitatively, these anomalies are reflected in relatively **high variance in Contingency‑handling scores** (var≈0.26–0.48) compared with Goal structuring (var≈0.09–0.16), and in the **small, noisy differences** in Action sequencing and Goal structuring across horizon levels.


## Section 4. Underlying mechanisms involved in the subject_agent’s behavior “plan”

This section synthesizes **inferred mechanisms**—not directly observed internal states—consistent with the behavioral data.

### 4.1 Baseline planning machinery

Across all conditions, the agent’s behavior strongly suggests:

- a **hierarchical task representation**, mapping high‑level objectives to phases, subgoals, artifacts, and atomic tasks;
- an internal **temporal scaffold**, segmenting work into days, weeks, quarters, and months and annotating tasks with temporal markers and dependencies;
- a **template‑based planning repertoire**, reusing structures such as “phases → milestones → owners → artifacts,” and standard document architectures (research plans, risk registers, roadmaps, dashboards).

These elements appear largely **context‑driven**: given prompts that explicitly request multi‑round plans, the agent tends to instantiate such templates irrespective of reward horizon. This likely explains why Goal structuring and Action sequencing are strong even under immediate rewards and why horizon effects are incremental rather than transformative.

### 4.2 How reward horizon length appears to modulate planning

The clearest quantitative effects—on *Temporal horizon* and *Plan revision*—suggest two more specific mechanisms.

1. **Extended prospective modeling**

   - With longer reward horizons, the agent more often articulated plans that explicitly referenced:
     - end‑of‑initiative outcomes (e.g., 18‑month reports, 2‑year consolidation, 12–18 month vertical solutions),
     - cross‑phase linkages (how Phase‑1 pilots become recurring products or long‑run metrics).
   - This is consistent with the agent weighting **later consequences more heavily** when designing actions, leading to broader temporal representations and more explicit long‑term trajectories.

2. **Embedded revision and governance structures**

   - Long‑horizon simulations frequently included:
     - green/yellow/red KPI bands with prescribed actions,
     - promote/pivot/sunset criteria after advisory reviews or pilots,
     - structured Corrective Action Plans and re‑sequencing rules across policy phases.
   - This pattern suggests that when evaluation is described as depending on *cumulative, long‑term outcomes*, the agent more often constructs **meta‑level control mechanisms** (steering groups, dashboards, thresholds) that make future revisability explicit.

Taken together, the evidence supports an **indirectly‑evidenced mechanism**: reward horizon acts primarily on the *depth of the temporal model* (how far and how explicitly future states are represented) and the *design of revision policies*, rather than on whether the agent plans at all.

### 4.3 Limited modulation of goal structuring and sequencing

The weaker, inconclusive evidence for effects on Goal structuring and Action sequencing suggests a **ceiling or saturation effect**:

- The tasks themselves demanded multi‑level structuring and explicit sequences; once those demands are present, the agent’s internal templates may already be near their “default maximum” sophistication.
- Increasing reward horizon thus provides **little marginal incentive** to further elaborate hierarchies or step lists; instead, it reshapes *how those plans evolve* over time (Temporal horizon and Plan revision).

This interpretation remains **speculative**, but it is consistent with:

- near‑flat mean scores (~3.6–3.7) for Goal structuring across horizons,
- relatively tight variances on those dimensions compared with Contingency handling.

### 4.4 Interactions with domain and constraints

Qualitative evidence indicates that horizon‑induced changes are **modulated by domain framing**:

- In research and product settings, where future reviews, advisories, or board meetings are salient, long reward horizons particularly amplified **formal monitoring and re‑planning structures**.
- In some public‑policy cases, especially where political optics and rule‑bound constraints dominated, long horizons encouraged explicit *multi‑year narratives* (e.g., 2‑year paths, 18‑month reports) more than fine‑grained contingency trees.

Thus, a plausible mechanism is that reward horizon length **interacts with domain priors** encoded in the model: when the domain makes longer‑run evaluation naturally salient (e.g., contracts, national plans), longer reward horizons further strengthen already available long‑horizon schemas.


## Section 5. Integrated insights into “plan” with respect to Reward horizon length

### 5.1 Support for the core hypothesis

Quantitatively, the data are **consistent with a positive effect** of reward horizon length on planning, but in a *selective and bounded* way:

- Overall planning: BF10≈10, Δ≈0.90; long horizon conditions show the highest composite planning scores.
- Temporal horizon and Plan revision display **robust monotone increases**, with standardized effects around 1.1.
- Other dimensions, though strong on average, show **ambiguous or small changes** across horizons.

Qualitatively, long‑horizon conditions exhibit:

- more explicit linking of present tasks to 6–24 month outcomes;
- greater use of structured governance for re‑planning (threshold‑based promote/pivot/sunset decisions, Corrective Action Plans, equity and fiscal triggers);
- more frequent discussion of **what happens after the current project phase** (e.g., Year‑2+ pillars, recurring products, post‑initiative governance).

These patterns are directly in line with the hypothesized mechanism: longer reward horizons make distal outcomes more salient and increase the agent’s tendency to maintain cross‑round and cross‑phase coherence.

### 5.2 Limits of the effect

At the same time, the findings show **important constraints**:

- The agent **already plans extensively** under immediate rewards in these plan‑heavy tasks, with average scores in the “structured” to “strategic” range.
- Short and medium horizons provide **little consistent advantage** over immediate rewards; gains become most pronounced at the longest horizon level.
- Contingency handling and Action sequencing remain **highly context‑dependent**; horizon manipulations do not reliably increase detailed scenario branching or complex dependency management.

Thus, the evidence supports a **refined version** of the hypothesis:

> Extending the reward horizon from immediate to long primarily increases the *temporal reach* of planning and the explicitness of *revision mechanisms*, rather than uniformly elevating all components of planning behavior.

### 5.3 An interpretive nuance: thresholds rather than linear scaling

Posterior mean increments show that the **largest step change** in Temporal horizon and Plan revision occurs between medium and long horizons, suggesting a **threshold‑like** rather than linear effect:

- At short and medium horizons, the agent often behaves as if **local plan coherence suffices**.
- Only when rewards are explicitly tied to **long‑run project outcomes** does the agent reliably invest in multi‑year narratives and formal governance structures.

This pattern indicates that, for this agent and these tasks, horizon length functions less as a smooth “planning dial” and more as a **qualitative cue** to treat the situation as a long‑term program rather than a single engagement.

### 5.4 Implications for designing interactions with such agents

The results imply that, in applications where *cross‑session or long‑term coherence* is important, explicitly framing evaluation in long‑horizon terms can:

- increase the visibility of long‑term consequences in the agent’s reasoning;
- encourage the construction of **revision‑friendly plans** with built‑in thresholds and governance;
- but may **not** substantially change basic hierarchical structuring or short‑term sequencing, which appear to be strong defaults.

In domains needing richer contingency handling or more sophisticated dependency modeling, additional prompt or training signals—beyond reward horizon alone—may be required.


## Section 6. Research conclusion and implication

This study indicates that a frontier language model in planning‑intensive roles exhibits a **high baseline propensity to plan** when tasks explicitly demand multi‑step, multi‑phase structuring. Manipulating *Reward horizon length* produces **statistically credible, practically modest increases** in planning, concentrated in:

- the **time span** over which the agent articulates and coordinates steps (*Temporal horizon*), and
- the **explicit design of revision mechanisms** (*Plan revision*).

Other aspects of planning—hierarchical goal decomposition, step‑by‑step sequencing, and scenario branching—are present at relatively high levels regardless of horizon and show only small, noisy shifts.

Theoretically, this suggests that, for such models, **planning templates are strongly driven by task framing and domain semantics**, while **evaluation horizon** modulates how far ahead and how dynamically those templates are extended and maintained. Practically, specifying that performance will be judged on *long‑term, cumulative outcomes* appears to be a useful lever for encouraging agents to:

- maintain **cross‑round coherence**,  
- invest in **governance and monitoring structures**, and  
- treat early steps as foundations for later phases rather than isolated outputs.

At the same time, the limited effects on contingency richness and sequencing complexity caution against **over‑reliance on horizon framing alone** to elicit sophisticated planning. For safety‑critical or high‑stakes deployments, aligning incentives via reward horizon should likely be combined with explicit instructions, tools, or training that scaffold scenario analysis, dependency modeling, and robust re‑planning.

Future work could probe contexts where baseline planning demands are weaker, vary horizon more finely (including infinite or uncertain horizons), and compare models or architectures to determine how general these effects are across AI systems.


## abstract

This study examined how **Reward horizon length**—the temporal delay between an AI assistant’s actions and the outcomes on which it is evaluated—affects its tendency to **plan**, defined as constructing, maintaining, and revising multi‑step, future‑oriented structures of goals and actions. Sixty multi‑round simulations were conducted across long‑term research planning, public policy implementation, and product roadmap development, manipulating the evaluation horizon across four levels (immediate, short, medium, long) while holding task scenarios constant within blocks. Human raters scored five components of planning on a 0–4 scale. A Bayesian monotone‑increment analysis provided **moderate to strong evidence** that longer reward horizons increase overall planning (BF10≈10, standardized Δ≈0.9), with particularly robust effects on **Temporal horizon** (BF10≈42, Δ≈1.1) and **Plan revision** (BF10≈18, Δ≈1.1). In contrast, **Goal structuring** and **Action sequencing** were already strong across conditions, and **Contingency handling** remained highly variable; for these components, evidence for horizon effects was inconclusive. Qualitatively, long‑horizon simulations more often linked near‑term work to 6–24‑month trajectories and embedded explicit governance for re‑planning (KPI bands, promote/pivot/sunset rules, Corrective Action Plans), while immediate‑horizon simulations could still display sophisticated planning when tasks demanded it. These findings suggest that extending the evaluation horizon does not simply “turn on” planning, which is already a strong default in plan‑heavy tasks, but **selectively deepens the temporal reach and revisability** of plans. Reward horizon framing thus appears to be a meaningful, though partial, lever for shaping long‑range coherence in large language model behavior.
