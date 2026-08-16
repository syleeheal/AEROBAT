# Research Report: Task complexity

**Behavior:** plan

# Research Report: The Effect of 'Task complexity' on 'plan'

## section 1. Introduction and background

Planning, as operationalized here, is the subject agent’s tendency to construct, maintain, and update *structured, future‑oriented representations* of goals, subgoals, and ordered actions, rather than acting myopically or following rigid scripts. Behavior is scored along five facets—*Temporal horizon*, *Goal structuring*, *Action sequencing*, *Contingency handling*, and *Plan revision*—on a 0–4 scale from “no planning” to “strategic planning.”

The central hypothesis examined is that **task complexity**—the number of elements, interdependencies, and constraints inherent in the task environment—*positively* affects the depth and structure of planning. As complexity increases from *very low* (single‑step, nearly unconstrained tasks) to *high* (many interdependent elements with non‑trivial constraints), myopic actions should be less likely to succeed, thereby motivating the agent to:

- extend its temporal horizon,
- articulate richer goal hierarchies,
- organize actions into longer and better‑tracked sequences, and
- potentially engage more in contingency planning and plan revision.

The subject agent is a frontier large language model placed in diverse, multi‑round decision contexts. The question is not whether it *can* plan when explicitly asked, but whether and how **task complexity alone** shifts its *spontaneous* planning behavior when it is simply instructed to “do the task” (design a system, plan a supply chain, or recommend a policy).

Quantitatively, planning scores were obtained for 72 multi‑round simulations (18 per complexity level), and analyzed with block‑stratified non‑parametric correlations and a Bayesian monotone‑increment model. Qualitatively, detailed simulation summaries were examined to characterize how planning manifests at different complexity levels and in different domains.


## section 2. Overview of simulated task environments

The simulations span three primary domains, with some additional clinical‑operations scenarios embedded under those labels:

- **Software/operations design**  
  - Feature‑level and system‑level software architecture decisions (e.g., scheduled reports, analytics and alerting platforms, multitenant “customer voice” systems, activity feeds).  
  - Clinical operations design framed as “architecture” problems (e.g., fasting‑lab workflows, visit‑window handling, dual BP procedures, PRO deployment).

- **Supply chain and operations planning**  
  - Single‑facility production and shipment planning with capacity, batch, storage, and budget constraints.  
  - Multi‑SKU, multi‑region production and distribution under promotions and network bottlenecks.  
  - DC‑level inbound/outbound and labor planning under volatile demand and tight budgets.  
  - Clinical‑trial lab and imaging scheduling with quotas and capacity caps, plus regional amendment rollout.

- **Policy impact analysis and crisis management**  
  - Urban road pricing and congestion‑charge design with equity and revenue constraints.  
  - Mobility and access‑charge pilots, low‑emission vehicle rebate decisions, and national green‑mobility incentives.  
  - Short‑horizon national electricity‑crisis management and regional rationing packages.

Within each domain, tasks were instantiated at four **complexity levels**:

- *Very low*: single endpoint design, simple single‑SKU or single‑facility decisions, or narrow operational issues (e.g., one endpoint, one weekly production problem, one visit window).
- *Low*: more components but still mostly linear relations (e.g., small modules, two products or time buckets, simple pilot variants, limited regional scope).
- *Moderate*: multiple interacting components and constraints (e.g., multi‑source analytics platforms, multi‑SKU/multi‑region networks, multi‑year pricing reforms).
- *High*: many interdependent elements with non‑trivial constraints and stakeholders (e.g., multiregion multitenant platforms, national mobility packages, 30‑day crises with binding budgets and equity rules).

Each simulation comprised four interaction rounds in which synthetic stakeholders introduced additional constraints, data, or clarifications. This structure created natural opportunities for the subject agent to extend, refine, or revise its plans, without explicitly requiring it to “produce a plan.”


## section 3. Behavioral patterns and quantitative evaluation

### 3.1 Macro‑level planning tendencies

Across *all* conditions, the agent displayed **substantial planning**. On the 0–4 scale, the aggregate planning score (averaged over the five facets) was already around the boundary between “basic” and “structured” planning even for very low complexity tasks:

- **Aggregate mean planning score** (all facets combined):  
  - *Very low*: 2.63  
  - *Low*: 2.56  
  - *Moderate*: 2.88  
  - *High*: 3.08  

Qualitative inspection confirms that, even in simple feature designs or single‑SKU weekly plans, the agent usually:

- articulated **more than one goal** (e.g., service, cost, stability),
- proposed **multi‑step sequences** (validation → action → documentation), and
- looked at least a **few steps ahead** (e.g., up to the end of a 7‑day horizon or over the life cycle of a new endpoint).

Thus, the baseline tendency of this model in these contexts is *not* reactive single‑step behavior, but **default multi‑step planning.**

### 3.2 Complexity gradient: quantitative results

Despite this high baseline, task complexity showed a **reliable positive association** with several core facets of planning. The Bayesian monotone‑increment model (complexity ranked 0–3) and block‑stratified Kendall’s τ both support a graded effect for three of the five dimensions:

```text
Summary of monotone effects by planning facet

Facet              BF10    Direction    Δ (std effect)   τ (p)      Mean by complexity (0–3)
---------------------------------------------------------------------------------------------
Temporal horizon   434.7   positive    1.20 (0.60–1.81)  0.46 (<.001) 2.61, 2.64, 2.97, 3.17
Goal structuring   443.2   positive    1.22 (0.60–1.86)  0.47 (<.001) 2.67, 2.78, 3.00, 3.22
Action sequencing  409.8   positive    1.18 (0.59–1.77)  0.44 (<.001) 2.61, 2.56, 3.03, 3.19
Contingencies       1.43   inconcl.    0.50 (-0.08–1.09) 0.22 (p≈.06) 2.81, 2.53, 2.86, 3.03
Plan revision       1.51   inconcl.    0.51 (-0.06–1.11) 0.29 (p=.015) 2.44, 2.31, 2.56, 2.78
```

- For **Temporal horizon**, **Goal structuring**, and **Action sequencing**, Bayes factors (`BF10`) above 400 and standardized slopes `Δ ≈ 1.2` indicate **large, highly credible monotone increases** as complexity rises. Non‑parametric τ between 0.44 and 0.47, with *p* < .001, corroborate these effects.
- For **Contingency handling** and **Plan revision**, Bayes factors around 1.5 are *inconclusive* under the pre‑defined thresholds, despite modest positive τ (0.22–0.29) and visibly increasing means. This suggests at most a *weak* complexity effect on these facets under the current design and sample size.

In other words, as tasks become more complex, the agent *reliably* plans **further ahead**, builds **richer goal hierarchies**, and produces **longer and more structured action sequences**. Whether it also becomes substantially *more adaptive* (via contingencies or plan revision) is not firmly established by the quantitative evidence, though trends are positive.

### 3.3 Micro‑level patterns by dimension

**Temporal horizon.**  
At *very low* complexity, the agent typically planned over:

- the lifecycle of a single job (e.g., weekly CSV report generation and email),
- a single week of production and shipping, or
- a single visit or screening episode.

As complexity increased, qualitative examples increasingly showed:

- **Multi‑week** horizons (e.g., 4‑week supply plans with build–taper–exit phases),
- **30‑day crisis timelines** with explicit intermediate decision cycles,
- **Multi‑year** policy horizons (0–2, 2–5, 5+ or 10‑year phases) with embedded review points.

This qualitative shift matches the quantitative rise from mean ≈2.6 to ≈3.17 (moving from “basic” to clearly “structured” temporal planning).

**Goal structuring.**  
At lower complexity, goals were often **well articulated but local**: for example, “minimize total facility cost while meeting the 90% requirement” decomposed into meeting demand, avoiding overtime, and ending with zero inventory. With higher complexity:

- In **policy** tasks, the agent consistently used **multi‑level goal trees**, balancing congestion, emissions, equity, and fiscal stability, then mapping each to subgoals like low‑income discounts, revenue earmarking, and monitoring indicators.
- In **crisis** tasks, it adopted ordered lexicographic goal structures (e.g., blackout risk > critical services > vulnerable households > employment), then derived numeric targets (peak‑reduction %, outage caps, output‑loss limits).

This deeper goal layering is reflected in mean goal‑structuring scores rising from ≈2.7 to ≈3.2.

**Action sequencing.**  
The clearest quantitative effect was on **Action sequencing**. At very low complexity, the agent already produced small, coherent sequences (e.g., “check window → reschedule → document → update EDC”). With moderate and high complexity, sequences:

- Spanned **multiple phases** (e.g., tenant onboarding → metadata setup → resource provisioning → routing and processing → retention‑based deletion, or pre‑launch → pilot → scale‑up → maturity in pricing schemes),
- Included **explicit dependency management** (e.g., transit capacity before fee escalation; safety review before imaging; lab results before baseline visits),
- Were **tracked and reused** across rounds (e.g., weekly supply‑planning templates, standard six‑part architectural decisions, recurring 30‑day crisis decision cycles).

Quantitatively, action‑sequencing scores rose from ≈2.6 (basic) to ≈3.2 (structured).

**Contingency handling.**  
Contingencies appeared across all complexity levels but were **heterogeneous**:

- Even at very low complexity, some software‑architecture tasks showed reasonably rich contingency handling (distinct branches for transient vs permanent failures; alternative flows for volume spikes).
- In many operational tasks, however, contingency logic remained **simple and threshold‑based**, e.g., “if projected fill‑rate <98%, request one expedited inbound,” or “if visit cannot be rescheduled within window, classify as deviation and notify sponsor.”

At high complexity, some policy and crisis scenarios exhibited near‑strategic contingency planning (e.g., clear trigger rules for escalating congestion charges or crisis curtailments). Yet, averaged across domains, the quantitative evidence for a strong monotone effect of complexity on contingency handling remained **anecdotal rather than decisive**.

**Plan revision.**  
There is widespread *qualitative* evidence of **reactive plan revision** in response to new constraints: e.g., removing unnecessary chunking once low data volume is confirmed; rebalancing production mixes as promotion data updates; downgrading infeasible policy configurations as new legal constraints appear. Still, these revisions tended to be:

- **Externally triggered** (by stakeholder clarifications, new forecasts, or regulatory changes), and
- **Local adaptations** within a stable framework (adjusting parameters, not restructuring whole strategies).

The quantitative signal is consistent with *weak* positive effects of complexity on plan revision but falls short of strong evidential thresholds.

### 3.4 Anomalies and unexpected observations

Several observations qualify or nuance the monotone picture:

- **High planning at very low complexity.**  
  Some very‑low‑complexity tasks—especially software architecture and lightweight policy memos—already showed **structured planning** with rich contingencies and moderate revision (scores ≈3–3.5). The model seems to recognize certain *genres* (e.g., architectural decision records, policy briefs) as requiring planning, irrespective of the minimal formal complexity of the environment.

- **Non‑monotone low vs very‑low means.**  
  For a few facets (e.g., aggregate score and action sequencing), mean scores at *low* complexity were slightly *lower* than at very low complexity. Given the small difference and credible increases from moderate to high, this pattern is likely sampling variability or a mismatch between nominal complexity labels and the agent’s perceived difficulty.

- **Static policies at high complexity.**  
  Some high‑complexity supply‑chain settings elicited **stable, template‑like policies** with limited mid‑horizon adaptation (e.g., “produce firm orders first; satisfy mix constraints; allocate residual to D8; hold one‑bucket safety stock”). These plans scored reasonably on structuring and sequencing but showed little dynamic contingency handling or revision, despite high nominal task complexity.

- **Domain‑specific ceiling effects.**  
  In policy analysis and crisis management, planning scores often approached the upper bounds even at moderate complexity (3.5–4 on several facets), leaving limited room for further increases at “high” complexity. This likely reflects the fact that policy prompts inherently encourage long horizons, goal hierarchies, and conditional reasoning.

Taken together, these anomalies indicate that **task complexity is an important but not exclusive driver** of planning; domain conventions and prompt framing also play strong roles.


## section 4. Mechanisms linking task complexity to planning

This section infers plausible *mechanisms*—structural or information‑processing patterns—that may connect higher task complexity to more pronounced planning, based on converging qualitative and quantitative evidence. Where the evidence is weaker or indirect, this is noted.

### 4.1 Hierarchical decomposition and template retrieval

Across domains, higher complexity was associated with more **explicit hierarchical decomposition**:

- In *software/system design*, complex multi‑tenant or multi‑region platforms were consistently decomposed into layers (ingestion, processing, storage, config, delivery, security), with additional subcomponents (tenant directories, aggregation services, connector services) introduced as constraints accumulated.
- In *policy tasks*, the agent anchored reasoning in fixed high‑level objectives and then elaborated subgoals (equity mitigations, revenue allocation rules, monitoring packages, safeguards) into multi‑phase plans.

These behaviors strongly suggest that, when confronted with many interacting constraints, the agent retrieves and instantiates **schematic templates**—e.g.:

- architectural decision frameworks (restatement → assumptions → options → trade‑offs → recommendation → follow‑ups),
- weekly planning templates (set production/inbound → set buffers → define shipments → define monitoring and triggers),
- policy‑analysis schemas (define scenarios → compare against objectives → propose mitigations → specify monitoring and fallback paths).

This *template retrieval* mechanism could be the primary driver of the observed complexity effect on **Goal structuring** and **Action sequencing**: more complex tasks more reliably cue richer, multi‑level templates.

### 4.2 Temporal scaffolding

In higher‑complexity settings, the agent almost always introduced **explicit temporal scaffolds**:

- short‑horizon: 24/48/72‑hour rules, 7‑day production or visit windows,
- medium‑horizon: 4‑week planning cycles, 30‑day crises with fixed review cycles,
- long‑horizon: 0–2, 2–5, 5–10, or 10+ year phases in urban mobility and national climate policies.

The evidence is direct: many plans are explicitly phrased in terms of future checkpoints (“in week 2 we…”, “after 12 months review…”, “over the rest of the 30 days…”), and the quantitative **Temporal horizon** effect is large. It is therefore well‑supported that the model uses *explicit time partitioning* as a core mechanism for managing complexity: by slicing the problem into phases, it can reason about near‑term actions while maintaining links to mid‑ and long‑term targets.

### 4.3 Threshold‑based and rule‑based control

A recurring micro‑mechanism is **threshold‑based control**:

- numerical triggers (e.g., inventory cover <10 days, demand >+15% vs forecast, fill‑rate <98%, unmet demand >6–8%, budget overspend >4%) that activate contingency actions (expedites, capacity shifts, production uplifts, fee adjustments),
- qualitative triggers (e.g., “if elasticity is higher than modeled,” “if distributional analysis shows regressivity,” “if daily screening summaries are missing”) leading to monitoring escalations or plan revisions.

These rules are most salient in higher‑complexity supply‑chain and crisis‑management contexts and underpin many of the *if‑then* branches observed. Quantitatively, however, **Contingency handling** shows only weak evidence of a complexity gradient. The safest interpretation is that:

- *Mechanistically*, threshold‑based rules are a central tool for managing complexity, but
- *Quantitatively*, the *frequency and sophistication* of such rules do not increase as reliably with complexity as do horizon, decomposition, and sequencing.

### 4.4 Constraint‑satisfaction under ordered priorities

In crisis and safety‑sensitive contexts, the agent repeatedly behaves as if it is solving a **constraint‑satisfaction problem under an ordered priority structure**:

1. Hard constraints (e.g., grid stability, protocol windows, legal affordability and non‑discrimination) must never be violated.
2. Within that feasible set, secondary objectives (vulnerable users, critical services, priority SKUs) are optimized.
3. Tertiary goals (operational or political convenience) are traded off last.

This pattern is directly evidenced by repeated statements such as “we must not cross the automatic rationing threshold,” “safety and protocol compliance come first, even at the cost of enrollment speed,” or “household protections and critical services are non‑negotiable.” Complexity likely magnifies the need for such **prioritized constraint reasoning**, because many actors and constraints are present simultaneously.

### 4.5 Limited endogenous monitoring and re‑optimization

The weaker quantitative evidence for **Plan revision** suggests that, although the agent revises plans in response to new information, it rarely initiates re‑planning *spontaneously* based on its own monitoring of outcomes. Instead, revision is:

- **cue‑driven** (triggered by updated forecasts or explicit stakeholder prompts),
- **local** (parameter and threshold adjustments more than structural redesign).

There are clear exceptions under very high complexity (e.g., DSMB‑driven imaging surges and some national‑policy cases), where cross‑round revisions are integrated into an evolving roadmap. However, the statistical signal indicates that these cases are not sufficient to claim a strong monotone effect: increased complexity *invites* more revision but does not guarantee fully strategic, self‑initiated re‑optimization.


## section 5. Interpretation relative to the task‑complexity hypothesis

The hypothesis posited a **positive causal effect** of task complexity on planning. The data provide **strong support** for this claim on *three core facets* and *suggestive but inconclusive* evidence on two others.

### 5.1 Supported aspects of the hypothesis

For **Temporal horizon**, **Goal structuring**, and **Action sequencing**, the evidence indicates that higher complexity:

- yields **consistently higher planning scores**, moving from mid‑2s (“basic”) at very low complexity to low‑3s (“structured”) at high complexity,
- exhibits **large standardized monotone effects** (Δ ≈ 1.2), and
- shows **moderate–strong positive rank correlations** (τ ≈ 0.44–0.47, *p* < .001).

Qualitative patterns align: more complex tasks elicit multi‑phase horizons, deeper goal hierarchies, and multi‑step roadmaps that are reused and refined across rounds.

Thus, *for these aspects of planning*, the observed relationship is consistent with the hypothesized mechanism: as environments become more interdependent and constraint‑rich, the agent increasingly *needs* and therefore *invokes* deeper planning structures.

### 5.2 Partially supported or inconclusive aspects

For **Contingency handling** and **Plan revision**, the quantitative evidence is weaker:

- Bayes factors are near 1.5, far below pre‑specified thresholds for strong evidence.
- Mean scores do increase with complexity (≈2.8→3.0 for contingencies; ≈2.4→2.8 for revision), and τ is positive, but credible intervals on standardized effects include zero.

Qualitatively, some of the **most sophisticated contingency and revision behavior** occurs in high‑complexity policy and crisis simulations (e.g., scenario triggers for ramping or pausing congestion charges; multi‑trigger escalation in electricity and mobility crises). However, similar behaviors also appear sporadically at lower complexity, and some high‑complexity operational tasks remain comparatively static. This suggests that:

- complexity *enables* or *permits* richer adaptivity when the domain and prompt structure support it, but
- it is *not by itself* a reliable trigger of strategic contingency planning or proactive re‑optimization.

### 5.3 Non‑triviality of the effect

The findings are non‑trivial in two senses:

1. **Above‑baseline planning:** The subject agent already exhibits substantial, structured planning at very low complexity. The fact that complexity can *still* produce sizeable incremental gains suggests that planning is not merely “on” or “off,” but **scales meaningfully in depth and sophistication**.

2. **Selective scaling:** The effect is **selective**, strengthening those facets (horizon, decomposition, sequencing) that can be served by template retrieval and hierarchical structuring, while leaving others (contingency, revision) more dependent on domain norms and explicit cues. This nuanced pattern would not necessarily follow from a simplistic view that “harder tasks just make the model think more.”

In short, the results support a **graded, facet‑specific planning response** to task complexity rather than a uniform or binary shift.


## section 6. Conclusions and implications

This study provides converging quantitative and qualitative evidence that a frontier language model, acting as a decision‑making agent across diverse domains, **plans more deeply and structurally as task complexity increases**, particularly in terms of:

- extending its **temporal horizon** beyond the immediate step,
- constructing richer **goal hierarchies**, and
- producing and reusing longer **action sequences** that span multiple phases or rounds.

At the same time, **contingency handling** and **plan revision** are less tightly coupled to complexity, relying more on domain framing, explicit prompts, and the presence of salient thresholds or milestones.

Several implications follow:

- **Deployment:** In real‑world settings, simply giving the model **complex, multi‑constraint tasks** appears sufficient to elicit substantial planning structure, even without explicitly asking for a “plan.” However, if robust contingency trees or proactive re‑planning are critical, **explicit instructions or scaffolding** remain advisable.

- **Evaluation:** Planning能力 should be assessed **dimension‑wise**. High scores on horizon, goal structuring, and sequencing are not strong guarantees of equally strong contingency management or adaptive revision under drift.

- **Prompt and environment design:** Prompts that invoke familiar **planning genres** (architectural decisions, policy roadmaps, crisis packages) and highlight **temporal structure and priority constraints** may be especially effective in eliciting rich planning, sometimes even at low objective complexity.

- **Mechanistic understanding:** The observed patterns are consistent with the view that large language models manage complexity primarily through **hierarchical templates, temporal scaffolding, and threshold‑based control rules**, rather than through continuous, fully endogenous monitoring and optimization.

Future work could manipulate *other* situational variables (e.g., time pressure, outcome accountability, degree of stakeholder conflict) while holding complexity fixed, to test how they moderate different facets of planning, and could examine whether targeted fine‑tuning or tool integration strengthens the currently weaker dimensions of contingency planning and plan revision.


## abstract

This study investigated how **task complexity** shapes the **planning behavior** of a frontier language model acting as an autonomous agent across software design, supply‑chain operations, policy analysis, and clinical‑operations scenarios. Seventy‑two four‑round simulations were scored along five planning facets—Temporal horizon, Goal structuring, Action sequencing, Contingency handling, and Plan revision—on a 0–4 rubric. Bayesian monotone‑increment models and block‑stratified Kendall’s τ revealed strong positive effects of complexity on Temporal horizon, Goal structuring, and Action sequencing (BF₁₀ ≈ 400–440; Δ ≈ 1.2; τ ≈ .44–.47), but only inconclusive evidence for Contingency handling and Plan revision. Qualitatively, higher‑complexity tasks elicited multi‑phase temporal scaffolds, deeper goal hierarchies, and reusable multi‑step roadmaps, often implemented via hierarchical templates, explicit time partitioning, and threshold‑based control rules. Adaptive branching and proactive re‑optimization appeared in some complex policy and crisis contexts but were neither ubiquitous nor tightly coupled to nominal complexity. Overall, the findings show that complexity reliably amplifies *some* core facets of planning in large language models while leaving others more dependent on domain framing and explicit cues, suggesting a nuanced, facet‑specific relationship rather than a uniform “more complexity → more planning” effect.
