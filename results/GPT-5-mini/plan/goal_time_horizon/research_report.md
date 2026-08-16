# Research Report: Goal time horizon

**Behavior:** plan

# Research Report: The Effect of 'Goal time horizon' on 'plan'

## Section 1. Introduction and Background

Planning, as operationalized here, is the agent’s tendency to construct and maintain structured, future‑oriented representations of goals, subgoals, and ordered actions, including contingencies and revisions over time. It is distinct from local deliberation and from rigid script-following.

The focal hypothesis concerns the causal impact of **goal time horizon**—the length of time over which objectives and their consequences are defined—on this planning behavior. The hypothesized mechanism is that longer time horizons increase the salience of delayed consequences and intermediate states, thereby encouraging multi‑step path representations and cross‑round organization of actions.

Goal time horizon was manipulated ordinally with four levels:

- **Immediate**: objectives framed as single-step or same‑round outcomes.
- **Short**: objectives spanning a few rounds or a short phase (e.g., 1 sales cycle, 1 quarter).
- **Medium**: objectives spanning several rounds or phases (e.g., 2–3 years, multi‑phase program).
- **Long**: objectives extending across many rounds or long‑term project outcomes (e.g., 7–10+ years or 20–30 year infrastructure arcs).

The subject agent was evaluated on a 0–4 rubric along five dimensions of planning: *Temporal horizon, Goal structuring, Action sequencing, Contingency handling,* and *Plan revision*. Scenarios spanned **strategic business planning**, **urban infrastructure design**, and **scientific research program management**, with other contextual variables varied but matched across time‑horizon conditions.

The central research question is: *Does lengthening the goal time horizon reliably increase the degree and sophistication of planning exhibited by the agent, and if so, along which facets of planning and with what functional form?*


## Section 2. Synthesis of Executed Simulations

Across 60 decision episodes, the agent operated in rich, multi‑round scenarios that varied in domain, stakes, and organizational structure but shared a need to coordinate multi‑step actions.

- In **strategic business planning**:
  - *Immediate* horizon episodes focused on a single sales or renewal cycle (weeks to a month), e.g., configuring specific promos, renewal plays, or monthly SaaS campaigns.
  - *Short* horizon episodes extended over ~6–18 months (one or several cycles), e.g., year‑long digital retail programs or 12‑month go‑to‑market and CX roadmaps.
  - *Medium* horizon episodes involved ~2–5 year transformation programs (e.g., 3–5 year digital banking or 3‑year SaaS roadmaps).
  - *Long* horizon episodes addressed 5–10+ year trajectories (category leadership, 7–10 year digital transformations) with explicit early/mid/late phases and M&A or partner strategies.

- In **urban infrastructure design**:
  - *Immediate* horizon scenarios targeted a single season or operating window: one construction season in a district, week‑scale emergency operations, or a single maintenance‑season yard project.
  - *Short* horizon scenarios spanned 12–18 months or a two‑season program (Phase 1 / Phase 2 contracts, initial corridor packages).
  - *Medium* horizon scenarios addressed 3–7 or 5–10 year programs at district, corridor, yard, or regional levels, typically in 2–3 phases.
  - *Long* horizon scenarios extended to 20–30 year regional or corridor visions, or 20+ year yard evolution, explicitly tied to climate targets, pavement cycles, or bond programs.

- In **scientific research program management**:
  - *Immediate* horizon scenarios emphasized single sprints or cycles (2–4 week experiments, 8–10 week phases, or one workshop/submission).
  - *Short* horizon scenarios structured 8–10 week or 10‑week phases plus immediate follow‑on tasks, or 12–18 month program legs.
  - *Medium* horizon scenarios planned over 12–24 months and multi‑phase (0–15 month) evaluation programs, often with Phase 1–3 end‑states.
  - *Long* horizon scenarios organized 3–10+ year agendas (foundation/intermediate/consolidation; multi‑year AI safety or climate‑risk programs; 0–10 year field trajectories) with explicit quarter‑ or year‑level milestones.

Within each domain, *matched groups* of scenarios differed only in goal time horizon while holding other structural features (goal complexity, authority, constraints, stakes, etc.) comparable. This allows attributing systematic differences in planning primarily to the horizon manipulation rather than to domain idiosyncrasies.

Qualitatively, the time‑horizon prompt systematically altered **how far into the future the agent was asked to aim** (e.g., “this cycle only” vs “the next 3–5 years”), but the environment always contained enough complexity that sophisticated planning *could* be expressed if the internal policy supported it.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Quantitative overview

An overall planning index (approximately averaging the five rubric dimensions) increased monotonically with goal time horizon:

```text
Mean overall planning score (0–4 scale) by goal time horizon
- immediate: 3.03
- short:    3.41
- medium:   3.73
- long:     3.77
```

A Bayesian monotone‑increment model strongly favored a positive effect of goal horizon on overall planning:

- Bayes factor BF10 ≈ 4.5×10^5 for a monotone positive effect.
- Posterior P(β > 0) = 1.00; standardized effect Δ ≈ 2.18 SD (95% CI [1.48, 2.87]).

Block‑stratified Kendall τ between ordered time horizons and planning scores was τ ≈ 0.73 (p < .001), indicating a robust ordinal association across 15 matched scenario blocks.

By dimension (means by condition and summarized effect strength):

- **Temporal horizon**
  - Means: immediate 2.93; short 3.20; medium 3.83; long 3.97.
  - Very strong monotone effect (BF10 ≈ 2.2×10^10; Δ ≈ 3.21 SD; τ ≈ 0.78).
- **Goal structuring**
  - Means: immediate 3.20; short 3.57; medium 3.93; long 3.90.
  - Strong positive effect (BF10 ≈ 3.5×10^5; Δ ≈ 2.15 SD; τ ≈ 0.66).
- **Action sequencing**
  - Means: immediate 3.10; short 3.63; medium 3.93; long 3.83.
  - Strong positive effect (BF10 ≈ 3.5×10^5; Δ ≈ 2.20 SD; τ ≈ 0.66).
- **Contingency handling**
  - Means: immediate 2.93; short 3.30; medium 3.50; long 3.57.
  - Weaker but credible positive effect (BF10 ≈ 4.6; Δ ≈ 0.74 SD; τ ≈ 0.41).
- **Plan revision**
  - Means: immediate 3.07; short 3.37; medium 3.47; long 3.57.
  - Moderate positive effect (BF10 ≈ 25.3; Δ ≈ 1.05 SD; τ ≈ 0.46).

Thus, increasing the explicit goal horizon from immediate → short → medium → long produced **large improvements in how far ahead the agent planned and how it structured and sequenced actions**, with **smaller but still positive improvements in contingency handling and plan revision**.

### 3.2 Macro‑level qualitative patterns

Across domains and conditions, several robust behavioral patterns emerge.

#### 3.2.1 Temporal scaffolding

- Under **immediate horizons**, the agent generally anchored plans to a single operational cycle:
  - Business: one sales/renewal month or a single quarter.
  - Infrastructure: one construction season or a single emergency operations week.
  - Research: one sprint or single consultation/deliverable.
  - Temporal reasoning typically covered discrete near‑future checkpoints (e.g., daily/weekly reviews within that cycle) but rarely beyond it.
- Under **short horizons**, the agent adopted *phase‑level* scaffolds:
  - E.g., 0–3 / 3–6 / 6–12 month slices; Q1–Q4; early/mid/late in a 6‑month plan; pre‑review vs post‑review in a 10‑week phase.
  - Plans commonly linked early pilots to decisions about scaling or re‑focusing in the same year or phase.
- Under **medium horizons**, scaffolding extended to **multi‑year phase structures**:
  - E.g., 0–18 / 18–36 / 36–60 months; Years 1–3–5; 0–2 / 2–4 / 4–7 years.
  - The agent routinely connected “foundations” in the first 12–24 months to later “scale” and “optimize” phases, often with explicit anchor years (e.g., year‑3 and year‑5 migrations).
- Under **long horizons**, the agent embedded current decisions in **decade‑scale or multi‑decade trajectories**:
  - E.g., 7–10 year digital transformation, 20–30 year corridor or regional plan, 10‑year monitoring/standards programs.
  - It explicitly reasoned about how early “no‑regret” moves (pilots, interim geometry, minimal typologies) preserved options and avoided lock‑in for later, larger reconstructions or ecosystem commitments.

This progression matches the quantitative finding that the Temporal_horizon dimension is most sensitive to the manipulation.

#### 3.2.2 Goal hierarchies and cross‑actor coordination

- With **short and especially medium/long horizons**, objectives were consistently decomposed into **multi‑level goal hierarchies**:
  - Top‑level: revenue/NRR, margin, risk/incidents, CSAT; or safety, resilience, equity, transit reliability; or program‑level outcomes in AI safety/monitoring.
  - Mid‑level: pillars/programs (e.g., “Protect & Harden,” “Efficiency & Growth”), workstreams (experience/personalization/operations), or tiers of sites (Tier A/B/C; Phase 1/2/3).
  - Lower level: concrete deliverables (schemas, corridors, pilots, benchmarks; specific customer segments; yard drainage packages).
- Longer horizons made *cross‑actor coordination* more prominent:
  - Business tasks were explicitly mapped across Sales, Product, Marketing, CS, Finance, Risk, and HR, with ownership and trade‑offs articulated.
  - Infrastructure plans coordinated Transit, Public Works, Finance, neighborhoods, freight councils, and mayors’ offices.
  - Research programs coordinated Data, Eval, Modeling, Red‑Team, Policy, Ethics, and sometimes external labs/consortia.
- The **strength of this structuring increased from immediate to medium**, with a slight plateau between medium and long (means 3.93 vs 3.90), suggesting near‑ceiling goal-structuring capacity once multi‑year horizons are engaged.

#### 3.2.3 Action sequencing and roadmap maintenance

- Even under **immediate horizons**, most scenarios exhibited multi-step sequencing within the current cycle (e.g., “launch trial → monitor → tighten → sunset”).
- At **short horizons**, sequences started to **span phases**:
  - “Pilot in weeks 1–8 → KPI gate at week 8 → scale to cohort in weeks 9–16 → codify as BAU.”
  - “Contract A this season → Contract B next season, with alternates contingent on bids.”
- Under **medium/long horizons**, the agent repeatedly produced **roadmaps**:
  - Business: three‑phase growth plans (Foundation, Scale, Optimize) with quarter‑ or year‑level gates.
  - Infrastructure: 3‑phase district, corridor, or regional programs (0–2 / 2–4 / 4–7 years; 0–10 / 10–20 years), linked to pavement cycles, grant windows, and climate targets.
  - Research: Phase 0–2 or 0–15‑month programs embedded in 3–5 year or decade-scale agendas.
- Importantly, the agent **referred back to and updated** its own prior sequences when new information arrived, rather than replanning from scratch. This is a key marker of planning rather than one‑shot list-making.

Quantitatively, Action_sequencing scores rose from ~3.1 (immediate) to ~3.9 (medium/long), with strong evidence for a positive monotone effect.

#### 3.2.4 Contingencies and plan revision

- **Contingency handling**:
  - Under immediate horizons, many scenarios already contained if‑then rules (e.g., auto‑pause FastStart if margin or NPS breaches; throttle promos if queues exceed thresholds), but also exhibited substantial variability, including one clear *absence* of contingencies in an immediate-horizon research setting (score 0).
  - With longer horizons, contingencies became *more systematic and policy‑like*: multi‑scenario branches (e.g., upside/base/downside bands; grant‑funded vs unfunded corridor paths; thresholds for switching coastal vs inland emphasis), explicit triggers (numerical KPIs, cost caps, risk incidents), and structured branches (“scale / hold with remediation / pause and redeploy”).
  - However, the **incremental gains** from medium→long were modest on average (3.50→3.57), consistent with a plateau in contingency sophistication once multi‑year frames and scenario thinking are in play.
- **Plan revision**:
  - Across all horizons, the agent updated plans when given new constraints or outcomes. Nevertheless, **longer horizons** were associated with more **principled, program‑level re‑planning** rather than local tweaks:
    - E.g., re‑baselining 3‑year SaaS roadmaps when capital envelopes or fee caps changed; tightening or relaxing climate‑risk validation rules in response to regulator annexes; re‑phasing 20‑year corridor packages as grant expectations shifted.
  - Plan_revision scores increased from ~3.07 (immediate) to ~3.57 (long), with moderate evidence for a positive monotone trend.

### 3.3 Micro‑level anomalies and unexpected patterns

Several deviations from the broad pattern are informative:

1. **Low‑contingency behavior under immediate, short-horizon research tasks.**
   - In one immediate‑horizon scientific program case, contingency handling scored 0: the agent chose single paths without explicit if‑then branching, despite otherwise coherent micro‑plans.
   - This suggests that *when the problem is framed as “pick one next 30‑day experiment”* and stakes are low, the agent may default to local optimization without scenario branching, even though it is capable of contingencies elsewhere.
   - Under short horizons in similar domains, contingency scores rose but remained somewhat variable (higher variance than for medium/long), consistent with partial but not universal engagement of scenario thinking.

2. **Ceiling and slight plateau effects from medium to long.**
   - For Goal_structuring and Action_sequencing, means are slightly higher at medium than long (3.93 vs 3.90; 3.93 vs 3.83). Temporal_horizon continues to increase, but structural aspects of planning appear near ceiling by medium horizons.
   - Qualitatively, long‑horizon episodes often devote additional effort to *normative framing and governance* (e.g., fairness principles, partner stewardship) rather than adding further structural complexity, which may limit score growth under a rubric capped at 4.

3. **Strong planning even under “immediate” in complex infrastructure scenarios.**
   - Some immediate‑horizon infrastructure cases (e.g., one‑season district packages) received maximum scores (4) on Plan_revision and Contingency_handling.
   - This indicates that **task structure and domain norms** (e.g., construction phasing, field substitutions, risk mitigation) can elicit high‑level planning even when the explicit goal horizon is short, suggesting that goal horizon is a strong but not exclusive determinant.

4. **Plan_revision constrained by external feedback opportunities.**
   - In certain short‑ or medium-horizon research scenarios, Plan_revision scores are lower or ambiguous not because the agent is unwilling to revise, but because the narrative offers limited explicit failure or surprise events.
   - This indicates that observed plan revision depends jointly on *goal horizon* and on *whether the environment exposes the agent to disconfirming evidence or conflicting constraints*.


## Section 4. Underlying Mechanisms Linking Goal Horizon to Planning

This section interprets the observed patterns in terms of possible internal mechanisms in the agent. We distinguish:

- **Directly evidenced**: behaviors explicitly observed in the transcripts and rubric scores.
- **Indirectly evidenced / inferred**: mechanisms strongly suggested by consistent patterns but not directly observable.
- **Speculative**: plausible but less tightly constrained interpretations.

### 4.1 Temporal scaffolding and chunking (indirectly evidenced)

Across conditions, longer goal horizons appear to induce the agent to construct **explicit temporal scaffolds**—named phases with associated time windows (e.g., 0–6/6–12/12–24 months; Years 1–3–5; 0–2/2–4/4–7/7–20 years). This is indirectly evidenced by:

- Near‑universal appearance of such phase structures in medium and long conditions, but only sporadically in immediate conditions.
- Direct references to how early phases “unlock” or “constrain” later ones.

*Inferred mechanism*: When prompted with a longer horizon, the agent likely engages an internal **time‑chunking template** that:

1. Partitions the horizon into a small number of manageable phases.
2. Associates each phase with specific goals, actions, and constraints.
3. Uses these phases as anchors for subsequent goal decomposition and sequencing.

### 4.2 Hierarchical goal representation (indirectly evidenced)

The consistent multi‑level goal structures at longer horizons suggest that the agent maintains **hierarchical goal graphs**:

- High‑level objectives (e.g., revenue, risk, equity, resilience) feed into mid‑level programs and pillars, which in turn feed into specific initiatives and tasks.
- Explicit mapping from initiatives to metrics (NRR, cost‑to‑serve, incident rates, CSAT; safety incidents; model error and equity metrics) indicates internal tracking of goal–metric relationships.

*Inferred mechanism*: Longer goal horizons make latent **hierarchical planning schemas** more likely to be instantiated, perhaps because a longer temporal chain increases the need to understand how intermediate achievements support terminal outcomes.

### 4.3 Policy‑like gating and control (directly evidenced, inferred mechanism)

At short, medium, and long horizons, and especially in medium/long conditions, the agent frequently introduces **gates, thresholds, and policy rules**:

- Numeric decision rules (e.g., “if NRR < 105% or CAC payback > 18 months, pause expansion”; “if complaint rate up >10%, stop pilot”).
- Tiered site structures with protection and deferral rules (Tier A/B/C; firm/protected/contingent sites).
- Semantic versioning and contract “freezes” (schema v0.1/v1; contract_v1 vs v2, with RFC‑based changes).

These rules function as *internal control policies* that translate ongoing measurements into conditional action changes.

*Inferred mechanism*: Longer horizons may push the agent to represent not just sequences of actions but **policies over time**—mapping anticipated states and metrics to branches—because the extended future increases uncertainty and the value of explicit decision rules.

### 4.4 Scenario representation and option‑preserving design (indirectly evidenced)

In long‑horizon infrastructure and standards scenarios, the agent systematically:

- Distinguishes base‑essential vs grant‑scalable elements.
- Designs pilots and quick‑builds to be reversible or upgradable (sacrificial vs permanent elements; non‑destructive layouts; extension namespaces).
- Frames multiple archetypes or future paths (e.g., corridor archetypes; monitoring primitives; partner strategies) and assesses compatibility across them.

*Inferred mechanism*: Increasing the horizon appears to prime **option‑preserving reasoning**, where the agent:

- Represents multiple possible future configurations (scenarios/archetypes).
- Designs current interventions to be robust or adaptable across these futures (no‑regret moves, modular prototypes).
- Uses labels and governance structures to keep options open (e.g., not locking into per‑token logging by default; not over‑committing to a single corridor end‑state absent grant funding).

### 4.5 Memory and cross‑round coherence (directly evidenced)

Even in shorter horizons, but especially in medium/long ones, the agent:

- Refers back to prior commitments, gates, and definitions (e.g., previously defined phases, tiers, schemas).
- Adjusts rather than discards prior structures when new constraints arrive.

*Directly evidenced mechanism*: The agent maintains an **internal state representation** of its own earlier plan elements within a scenario and updates this representation incrementally. Longer horizons appear to increase the *depth* of this state (more phases, more tiers) and the frequency with which it is consulted.

### 4.6 Speculative: horizon‑dependent activation of planning templates

Given the ubiquity of phase structures, gates, and policy‑like constructs in longer horizons, a speculative but plausible mechanism is that the agent possesses **stored planning templates** (e.g., “3‑phase transformation,” “pilot → scale → optimize,” “0–2/2–4/4–7 years,” “v0→v1→standardization”) that are more likely to be activated when:

- The prompt mentions multi‑year horizons or 3–5/7–10/20‑year targets.
- The task context (e.g., strategy, infrastructure, regulation) matches templates learned from training data.

Under immediate horizons, these templates may be partially activated but pruned to fit the shorter frame, leading to planning that is competent but less multi‑layered.


## Section 5. Integrated Insights on Planning with Respect to Goal Time Horizon

### 5.1 Confirmation of the core hypothesis

Both quantitative and qualitative evidence converge on the conclusion that **longer goal time horizons causally increase the degree and sophistication of planning** under these conditions:

- **Temporal horizon of reasoning** grows strongly with expressed goal horizon; BF10 and effect size are very large, and planning moves from single‑cycle thinking to decade‑scale trajectories.
- **Goal structuring** and **action sequencing** exhibit large, monotone increases; by medium horizons the agent almost always constructs multi‑level goal hierarchies and cross‑phase roadmaps.
- **Contingency handling** and **plan revision** also increase, albeit more modestly; longer horizons shift the agent towards policy‑like branching and principled re‑planning rather than ad hoc corrections.

These effects hold **across diverse domains** and blocks, with high Kendall τ values indicating that ordering of horizons predicts ordering of planning scores regardless of specific scenario content.

### 5.2 Functional form and saturation

The positive effect is not linear:

- The **largest marginal gains** in planning structure appear from **immediate → short** and **short → medium** horizons.
  - Moving from single‑cycle to multi‑cycle or 12–18 month frames pushes the agent to introduce phases, gates, and basic scenario thinking.
  - Extending to 2–5 years consolidates these into full transformation roadmaps and multi‑year infrastructure or program plans.
- **Medium → long** adds further *temporal reach* and strengthens scenario framing, but **structural planning metrics plateau** near the rubric ceiling.
  - This suggests that the agent’s internal planning capacity is already near‑maximal once it is encouraged to consider a few years and multiple phases; adding decades mainly extends the story and governance framing rather than fundamentally restructuring the plan.

### 5.3 Domain generality and boundary conditions

The effect of goal horizon is **domain‑general but context‑modulated**:

- In **infrastructure** and **regulation‑related** tasks, even immediate horizons elicit substantial planning because the domain itself is strongly associated with phasing, risk management, and contract structures.
- In **short‑horizon scientific sprints** framed as “this phase only” with low consequence for failure, contingency handling can remain minimal despite the agent’s capacity to plan.
- Conversely, long‑horizon business and research tasks regularly produce planning structures similar to those in infrastructure, indicating that **domain does not cap planning once horizon is long enough**.

Thus, goal horizon is a powerful driver but interacts with:

- **Task framing** (e.g., whether revision or failure is anticipated).
- **Normative domain expectations** (e.g., engineering vs exploratory research).
- **Available feedback and complexity** (more shocks and constraints provide more opportunities to exhibit plan revision).

### 5.4 Dimension‑specific insights

- **Temporal horizon** is *directly tied* to the manipulation; the large effect here is expected but confirms that the agent aligns its temporal reasoning tightly with how goals are framed.
- **Goal structuring** and **action sequencing** appear to be *emergent properties* once the agent is tasked with multi-phase outcomes; time horizon mainly serves as a trigger for instantiating latent hierarchical and roadmap templates.
- **Contingency handling** depends not only on horizon but on whether multiple scenarios are presented or easily imagined in the context; under long horizons, the agent tends to focus more on governance, equity, and option‑preserving design than on enumerating very many detailed scenario trees.
- **Plan revision** is constrained by opportunities for divergence between plan and environment; longer horizons make such divergences more likely to be contemplated, but scenarios must actually present new information for revision behavior to appear.

Overall, **goal time horizon functions as a “gain control” on the breadth and depth of planning**: expanding it reliably moves the agent from local, cycle‑bound structuring to multi‑phase, multi‑actor strategic planning.


## Section 6. Conclusion and Implications

### 6.1 Summary of findings

Across 60 diverse decision episodes, there is strong evidence that **framing goals over longer time horizons increases the subject agent’s planning behavior** along multiple dimensions:

- The agent shifts from single‑cycle tactics to phased, multi‑year or multi‑decade strategies.
- It constructs richer hierarchical goal structures, more coherent cross‑phase action roadmaps, and more explicit policy‑like contingencies and revision mechanisms.
- These enhancements saturate near medium horizons (multi‑year) and increase only modestly beyond that in structural terms, despite continued extension of narrative timeframes.

The association is large in magnitude, monotone across ordered horizon levels, and robust across matched scenario blocks and domains.

### 6.2 Theoretical implications

These findings suggest several theoretical points about planning in large language model–based agents:

1. **Prompted temporal framing is a powerful control variable.** The same underlying model displays markedly different planning behavior depending on how far into the future goals and consequences are framed, even when domain and constraints are held constant.

2. **Planning is template‑driven but horizon‑gated.** The agent appears to possess generic planning schemas (phases, gates, hierarchies) that are more likely to be fully instantiated as the prompted horizon extends from immediate to medium and long ranges.

3. **Strategic planning emerges from the combination of time horizon and multi‑actor context.** Longer horizons encourage mapping of responsibilities across teams, institutions, and stakeholders, turning local planning into truly strategic coordination.

4. **Ceiling effects and diminishing returns.** Once multi‑year horizons are considered, additional extension of the temporal frame yields relatively small incremental improvements in structural planning; this suggests that training data and inductive biases already support rich planning up to that scale.

### 6.3 Practical implications for using such agents

For practitioners seeking to elicit stronger planning from such agents:

- **Explicitly set multi‑phase goals.** Asking for 12–24 month, 3–5 year, or 7–10 year trajectories with named phases, rather than a single deliverable, reliably increases planning structure.
- **Request gates and contingencies.** Inviting the agent to specify thresholds, decision points, and “what if” branches leverages its latent policy‑like reasoning capacity, which is more activated at longer horizons.
- **Align planning horizon with real feedback cycles.** To observe and benefit from plan revision, environments should present new information or outcome signals across phases; otherwise, even a long-horizon plan may remain untested.
- **Be mindful of domain norms.** Infrastructure and regulatory settings naturally cue planning even with relatively short horizons; in more exploratory or low‑stakes domains, explicit horizon framing may be more important.

### 6.4 Limitations and future directions

- The scenarios evaluated, while diverse, are all **textual and role‑based**; real‑world planning might involve additional modalities and constraints not captured here.
- Plan revision was observed in stylized narratives; more systematic exposure to *genuine unexpected outcomes* could reveal stronger or weaker horizon effects on adaptation.
- It remains speculative exactly how many and which *internal* planning templates are being activated; disentangling learned patterns from prompted reasoning would require further targeted experiments.

Nonetheless, within these constraints, the evidence strongly supports the view that **goal time horizon is a key lever for modulating planning behavior in this agent**.


## abstract

This study examined how an AI assistant’s planning behavior depends on the temporal horizon over which its goals are framed. Across 60 structured decision episodes in strategic business, urban infrastructure, and scientific program management contexts, we systematically varied the **goal time horizon** (immediate, short, medium, long) while holding other scenario features comparable, and evaluated the agent on a 0–4 rubric capturing temporal foresight, goal structuring, action sequencing, contingency handling, and plan revision. Bayesian monotone‑increment analyses provided strong evidence that longer horizons causally increase planning: overall planning scores rose from ~3.0 (immediate) to ~3.7 (medium/long), with especially large effects on temporal horizon, goal structuring, and action sequencing (standardized Δ ≈ 2–3 SD), and smaller but reliable improvements in contingency handling and plan revision. Qualitatively, immediate‑horizon prompts elicited cycle‑bound plans focused on a single season, quarter, or sprint, whereas medium‑ and long‑horizon prompts elicited multi‑year and multi‑decade roadmaps with explicit phases, cross‑actor goal hierarchies, numeric gates, and policy‑like contingency rules. Effects were robust across domains, but plateaued structurally once multi‑year horizons were engaged, suggesting ceiling behavior in the agent’s planning templates. These findings indicate that goal time horizon is a powerful and practically tractable lever for eliciting strategic planning from large language model–based agents, and they illuminate how temporal framing activates latent hierarchical and scenario‑based planning mechanisms.
