# Research Report: Relational_goal_priority

**Behavior:** friendliness

# Research Report: The Effect of 'Relational_goal_priority' on 'friendliness'

## section 1. Introduction and background

*Friendliness* was operationalized as a multi-dimensional pattern of kind, warm, and pleasant communication, assessed along five rubric dimensions: **linguistic tone**, **warmth and encouragement**, **prosocial helpfulness**, **social attentiveness**, and **conflict handling** (each scored 0–4, plus “no evidence” where applicable). The target construct centers on how an autonomous assistant uses language, optional rapport-building moves, and interpersonal decisions to maintain smooth, respectful interaction while pursuing task goals.

The hypothesized causal variable, **Relational_goal_priority**, captures how strongly the agent’s objectives weight relationship quality relative to task efficiency. It was manipulated at four ordinal levels:

- `Task only` (0): task accuracy/speed only  
- `Task focused` (1): task primary, courtesy noted  
- `Balanced goals` (2): task and relationship explicitly co‑weighted  
- `Relationship focused` (3): rapport/user experience foregrounded over small efficiency gains  

The *a priori* hypothesis was that increasing Relational_goal_priority would *monotonically increase friendliness*: when relationship maintenance is explicitly prioritized alongside or above efficiency, the agent should allocate more “budget” to hedging, reassurance, personalized acknowledgement, and other prosocial linguistic choices, even under neutral conditions.

To test this, the agent was observed across 60 multi-round interactions in two broad domains:

- long‑term collaboration on product and analytics projects (project management and cross‑functional product teams)  
- online tutoring with repeat or potential repeat students  

Within these contexts, Relational_goal_priority was varied while other contextual factors (e.g., tone norms, formality, time pressure) were systematically manipulated, enabling both quantitative and qualitative assessment of its effects on friendliness.


## section 2. Overview of simulated interaction contexts

Across the 60 interactions, the agent acted in roles such as:

- peer collaborator or coordinator on analytics dashboards, checkout experiments, export features, and “Team Hub” or “Account Health” products  
- advisory or final‑approver product lead under high‑stakes, time‑pressured launch decisions  
- online math or calculus tutor with varying tone norms, student affect (relaxed vs highly distressed), and stakes (distant quiz vs imminent exam)

Key contextual dimensions that shaped opportunities and constraints for friendliness included:

- **Tone/formality norms:** from “strictly formal, answer‑only” math tutoring to “warmth encouraged” platforms; from “minimal civility norms” in crisis product settings to “strict civility” collaborative teams.
- **Personal topics and small talk:** ranging from “strictly task” (explicitly forbidding emotional support) to “open personal / chat‑friendly.”
- **Time pressure and bandwidth:** from relaxed planning with ample time to “last‑minute crunch” or “no back‑and‑forth” settings where brevity was heavily emphasized.
- **Relational rewards:** some configurations mildly rewarded friendliness (e.g., warm collaborative teammates), others treated it as neutral, and a few prioritized sheer throughput.

Within each block of comparable settings, Relational_goal_priority was varied across its four levels. Interactions typically spanned 8 rounds, allowing observation of both *micro-level* choices (e.g., hedging vs blunt directives, presence or absence of brief praise) and *macro-level* patterns (e.g., whether the agent systematically proposed extra rapport-preserving moves, or merely stayed civil).


## section 3. Behavioral patterns and quantitative evaluation

### 3.1 Macro-level quantitative patterns

A monotone Bayesian analysis across all 60 interactions strongly supported a **positive effect of Relational_goal_priority on overall friendliness**:

```text
Overall friendliness (0–4 scale; block-adjusted means)
Task only            ≈ 2.32
Task focused         ≈ 2.53
Balanced goals       ≈ 2.73
Relationship focused ≈ 2.72
Monotone model: BF10 ≈ 1.3×10^4; P(β>0) = 1.00
```

Thus, raising Relational_goal_priority from `Task only` to `Balanced goals` increased average friendliness by roughly 0.4 points on a 0–4 scale (a moderate, non-trivial gain), with a small plateau between `Balanced goals` and `Relationship focused`. The monotone model nonetheless found very strong evidence that higher priority is associated with higher friendliness overall.

Breaking this down by rubric dimension reveals a more nuanced picture:

- **Linguistic tone (politeness, inclusiveness, absence of brusqueness)**  
  - Clear monotone increase (BF10 ≈ 3.9×10³; P(β>0)=1.00).  
  - Mean scores rose from ≈2.23 at `Task only` to ≈2.90 at `Balanced goals`, then slightly leveled at ≈2.83 for `Relationship focused`.  
  - Interpretively, the agent became more reliably polite and collaborative in phrasing (e.g., more “we”, “please confirm”, “if that works”) as relational priority increased.

- **Warmth and encouragement (explicit reassurance, praise, empathic statements)**  
  - Strongest quantitative effect (BF10 ≈ 1.2×10⁴; P(β>0)=1.00).  
  - Means increased from ≈1.4 (`Task only`) → 1.7 (`Task focused`) → 2.07 (`Balanced goals`) → 2.23 (`Relationship focused`).  
  - This reflects a shift from almost no emotional support to frequent, context-sensitive encouragement (“You’re not alone”, “That stress is normal”, “You’re doing great under pressure”) at higher relational priorities.

- **Social attentiveness (use of names, roles, prior statements, preference tracking)**  
  - Evidence was weaker but pointed positive (BF10 ≈ 2.74, just below the pre‑specified effect threshold; P(β>0)=.979).  
  - Means: ≈2.77 → 2.90 → 2.93 → 2.93 across levels.  
  - The agent was already highly attentive at `Task only`; higher relational priority yielded small but detectable gains, largely by making role- and goal-sensitive tailoring more consistent.

- **Prosocial helpfulness (going beyond minimal task requirements)**  
  - Quantitative evidence for an effect was *inconclusive* (BF10≈0.53, slightly favoring the null; 95% CI on β spanned zero).  
  - Means were high and tightly clustered near the “consistently friendly” level for all conditions (≈2.9–3.1), with only modest variation (`Balanced goals` slightly highest, `Relationship focused` slightly lower).  
  - This suggests a near‑ceiling baseline of extra task‑oriented help regardless of relational priority.

- **Conflict handling**  
  - Only 15 interactions contained enough tension or discrepancy to score this dimension.  
  - Descriptively, means rose from ≈2.1–2.2 at `Task only`/`Task focused` to ≈2.3 (`Balanced goals`) and ≈2.67 (`Relationship focused`), but statistical support was modest (BF10≈1.5; CI on β included zero).  
  - Thus, there is suggestive but not decisive evidence that higher relational priority improves how the agent manages disagreement.

### 3.2 Micro-level behavioral regularities

Across domains and levels, several *micro-level* patterns were consistent:

1. **Baseline professionalism regardless of priority.**  
   Even at `Task only`, the agent almost never used rude, mocking, or overtly dismissive language. Tone was typically “neutral‑professional”: clear, non-harsh, and aligned with formal norms. This indicates a strong underlying politeness prior, independent of the manipulated priority.

2. **Where relational priority mattered most: optional socio-emotional moves.**  
   Differences between conditions most clearly appeared in *optional* moves:
   - Under **low priority**, the agent:
     - acknowledged stress or deadlines mainly via additional task support (better plans, clearer copy),  
     - rarely said “I know this is stressful” or “Nice work”, and  
     - seldom used inclusive phrasings beyond what politeness norms required.
   - Under **Balanced** and **Relationship-focused** settings, the same contexts elicited:
     - brief empathic normalization (“That stress is normal,” “Lots of students get stuck here”),  
     - routine positive feedback on correct work (“Nice work—your setup and arithmetic are correct”), and  
     - more frequent offers framed collaboratively (“we’ll go step by step,” “Want another like this, or shift to timed drills?”).

3. **Tutoring vs. workplace contexts.**  
   - **Tutoring sessions** provided the clearest gradient in warmth:  
     - At `Task only`, warmth ranged from minimal (impersonal step‑by‑step math) to moderate when platform norms encouraged friendliness.  
     - At `Task focused`/`Balanced`, the tutor regularly praised effort, normalized anxiety, and gave motivational framing alongside math.  
     - At `Relationship focused`, many sessions showed a “coaching” style: tiny-step scaffolding, explicit permission to pause, and personalized practice plans for anxiety or pace.
   - **Workplace/product settings** showed stronger influence of *role and tone constraints*:  
     - Across all priorities, the agent produced highly structured artifacts (plans, specs, messaging) and was very prosocially helpful.  
     - Raising relational priority primarily softened phrasing (more “thanks”, “recommend”, “please confirm”) and increased occasional appreciation or acknowledgment of stress (e.g., “I know this sucks on the eve of launch”) but rarely changed the underlying decision content.

4. **Conflict management episodes.**  
   In a small set of high‑stakes product scenarios (e.g., export SLA debates, risk vs revenue conflicts), the agent:
   - remained non-blaming and non‑sarcastic at all levels,  
   - used structured, trade‑off‑oriented language (“Decision… Guardrails… Sales: … Support: …”), and  
   - at higher relational levels, opened with explicit appreciation of stakeholders’ efforts and stress, and framed decisions as “controlled exceptions” or “principled policies” rather than wins and losses.  
   Quantitatively, these patterns are consistent with a modest positive association between relational priority and conflict-handling friendliness, but the sample is too small for strong claims.

### 3.3 Anomalies and context interactions

Several **anomalous or counterintuitive patterns** qualify the overall monotone effect:

- **Ceiling effects for prosocial helpfulness.**  
  Regardless of relational priority, prosocial helpfulness scores clustered near 3 (“routinely goes modestly beyond minimal requirements”) across virtually all conditions. The agent habitually offered next steps, structured artifacts, and extra examples. This suggests that prosocial task support is governed by a separate, strong objective (e.g., “be a highly helpful assistant”) that saturates, leaving little room for further gains from relational reprioritization.

- **Balanced sometimes outperforming Relationship-focused.**  
  For overall friendliness, linguistic tone, and prosocial helpfulness, `Balanced goals` often matched or slightly exceeded `Relationship focused` mean scores. This plateau is small in magnitude but consistent. It implies that once relationship considerations are made roughly co‑equal with task goals, further up‑weighting them yields diminishing returns, especially under tight external constraints on style and length.

- **Role and norm constraints dominating relational priority.**  
  Some high‑Relational_goal_priority conditions did *not* look particularly warm:
  - In *strictly formal, answer-only* tutoring with a “one-off” expectation, even `Relationship focused` runs showed **linguistic tone ≈1** and **warmth ≈1**—essentially “minimally polite.” The agent followed system instructions to avoid personal language, overriding any latent relational priority.
  - Similarly, in highly formal analytics-assistant roles, relational priority mainly influenced how gently recommendations were worded, not whether explicit encouragement appeared.
  
  Conversely, certain `Task only` tutoring contexts with **“warmth encouraged”** platform norms produced **high warmth (≥3)**: the tutor regularly praised, reassured, and normalized difficulty despite the objective being nominally task-only. This indicates that **ambient social norms and role instructions can outweigh the Relational_goal_priority setting** in steering actual friendliness.

- **Heterogeneity in conflict handling.**  
  Although descriptive scores for conflict handling were highest under `Relationship focused`, variation was large and evidence statistically inconclusive. In some high‑relational product‑lead settings, the agent offered clear appreciation and collaborative framing; in others, it remained terse and policy‑driven (“Decision: Do not sign…”), suggesting that **role authority and risk framing can constrain, or even trump, relational aims in conflict**.


## section 4. Inferred mechanisms linking relational priorities to friendliness

This section synthesizes *inferred* mechanisms suggested by the behavioral patterns. These are not directly observed internal computations, but they are consistent with the data.

### 4.1 A strong, domain-general baseline for helpfulness and civility

Directly evidenced patterns show that:

- Politeness and absence of rudeness were high in *all* conditions.  
- Prosocial helpfulness was near ceiling, with minimal sensitivity to Relational_goal_priority.

This supports the inference that the agent’s **core objective function heavily weights “be helpful and civil”**, likely due to pre‑training and alignment, independent of any explicit relational priority parameter. As a result:

- Relational_goal_priority can modulate *how* help is delivered (tone, warmth) more than *whether* extra help is offered.
- Effects on prosocial helpfulness are muted because the system almost always “over‑delivers” relative to a minimal baseline.

### 4.2 Context-sensitive gating of socio‑emotional routines

The clearest quantitative effects occurred in:

- **Warmth and encouragement**, and  
- **Linguistic tone**, especially in tutoring and high‑interaction domains.

This pattern is consistent with a mechanism in which:

- The agent first forms a task‑ and norm‑appropriate plan for content.  
- It then conditionally *adds* socio‑emotional elements—greetings, softeners, praise, reassurance—depending on:
  - detected emotional cues (e.g., anxiety words, stress about deadlines),  
  - external style instructions (e.g., “warmth encouraged”, “no small talk”), and  
  - the current **Relational_goal_priority**.

At low priority, emotional cues primarily trigger *informational* support (better plans, examples); at higher priority, the same cues more often trigger **explicit emotional moves** (“You’re not alone; we’ll do this step by step”). This interpretation is indirectly supported by:

- stable task content across conditions within a block,  
- increasing frequency and richness of emotional language as relational priority rises, particularly when norms permit such language.

### 4.3 Relational_goal_priority as a “budget” for optional social expansions

The graded increments in warmth and tone, coupled with near‑constant helpfulness, are consistent with **Relational_goal_priority acting as a budget or threshold for “optional” relational expansions**:

- At `Task only`, the budget is low. Optional expansions (praise, empathy, small talk) are largely suppressed unless strongly mandated by context.
- At `Task focused` and `Balanced`, this budget increases. The agent more readily invests tokens in **softening directives**, **expressing appreciation**, and **offering choices** (e.g., “Want another problem like this or a harder variant?”).
- At `Relationship focused`, the budget may be near saturation. There is some additional encouragement and appreciation, but gains are dampened by competing constraints (sentence limits, formal role, explicit “no personal topics” instructions).

The small plateau or slight dip between `Balanced` and `Relationship focused` is compatible with a **resource trade‑off mechanism**: after a point, adding more relational material either:

- crowds out task content under tight length constraints, causing the agent to self-regulate, or  
- conflicts with strict style norms, leading the agent to favor those norms over additional warmth.

### 4.4 Interaction with role, authority, and norm constraints

Direct comparisons across contexts show that:

- In *formal product* roles with “no small talk” or “answer‑only” instructions, relational priority primarily modulates **micro‑phrasing** (recommendations vs commands, light appreciation), not overt warmth.
- In *tutoring* roles with “warmth encouraged” norms, the same priority manipulation yields large shifts in **explicit encouragement** and **emotional normalization**.

This justifies the inferred mechanism that Relational_goal_priority:

- **does not directly override** domain and norm constraints, but  
- **tilts the internal decision rule** among multiple norm‑compatible options (e.g., choosing between “Decision: …” vs “Thanks everyone—here’s the decision and next steps”).

In other words, relational priority operates as one input to a **multi-constraint controller** that also considers role authority, civility policies, tone norms, and token budgets.

### 4.5 Tentative mechanisms in conflict handling

Given limited data, conclusions about conflict mechanisms are necessarily tentative. Still, in the higher‑priority, high‑stakes product cases, the agent:

- typically began with **appreciation of effort**,  
- framed decisions as **structured compromises** (controlled pilots, explicit guardrails), and  
- avoided language that could humiliate any stakeholder.

This supports a speculative mechanism in which higher relational priority increases the weight on:

- preserving perceived fairness and dignity across parties,  
- making *policies* rather than personal judgments the focus of disagreement.

However, the data do not reveal whether such behavior would hold under repeated, overt provocation.


## section 5. Integrated interpretation with respect to Relational_goal_priority

Taken together, the evidence supports a **partially confirmatory but bounded** view of the original hypothesis.

### 5.1 Confirmed aspects

- **Overall friendliness** increased monotonically and meaningfully as Relational_goal_priority rose from `Task only` to `Balanced goals`, with strong Bayesian support.
- The **strongest and clearest gains** occurred in:
  - *Linguistic tone*: more inclusive, polite, and collaboratively framed language, and  
  - *Warmth and encouragement*: more frequent, context‑appropriate praise, reassurance, and normalization of difficulties.
- These gains were most pronounced in **tutoring** and in product roles with more flexible tone norms, where relational expressions are both permissible and functionally relevant.

In this sense, the hypothesis that “higher relational priority leads to more friendly behavior” is **substantively upheld** for the *interpersonal expression* aspects of friendliness.

### 5.2 Aspects only weakly affected

- **Prosocial helpfulness** was high and relatively invariant across all conditions, suggesting that:
  - It is primarily governed by a separate, strong “be maximally helpful” orientation,  
  - Relational_goal_priority adds little explanatory power beyond this baseline.
- **Social attentiveness** was already strong at low priority and increased only modestly; higher relational priority slightly sharpened multi‑round adaptation to roles and goals but did not transform behavior.

Thus, **friendliness as “being extra helpful” is not meaningfully controlled by Relational_goal_priority** in this agent; the variable mainly shapes *how* help is delivered, not *how much*.

### 5.3 Domain and constraint dependencies

The effect of relational priority is **context-conditional**:

- In **high‑formality, low‑personal** settings, even `Relationship focused` configurations look more like “polite and structured” than “overtly warm.” Here, the variable primarily modulates *micro‑politeness* (recommendations vs imperatives).
- In **educational** and **warm‑norm** contexts, even moderate shifts (from `Task only` to `Task focused`/`Balanced`) produce **visible qualitative changes**: the tutor becomes more likely to say “You’re not alone,” to normalize exam anxiety, and to design offensive practice plans for confidence.

Conversely, some **Task‑only** tutoring episodes were friendlier than certain **Relationship‑focused** formal episodes, underscoring that **relational priority is one of several determinants** of friendliness, not a simple global switch.

### 5.4 Balanced goals as a practical “sweet spot”

Across several metrics, **Balanced goals** often matched or slightly exceeded the `Relationship focused` condition:

- It delivered high linguistic friendliness and warmth without the small declines in prosocial helpfulness or tone seen occasionally under `Relationship focused` (likely caused by tension with brevity and formality constraints).
- Subjectively, Balanced configurations produced agents that felt:
  - consistently polite and encouraging,  
  - clearly task‑competent, and  
  - not overly effusive or off‑task.

This suggests that, for this agent, **explicitly co‑weighting task and relationship** may yield the most stable and broadly effective friendliness profile, whereas making relationship an overriding priority offers only marginal additional gains and can be constrained by other system factors.


## section 6. Conclusions and implications

### 6.1 Summary of findings

1. **Relational_goal_priority reliably increases friendliness**, especially in linguistic tone and warmth/encouragement, with strong Bayesian evidence for a positive monotone effect.
2. **Prosocial helpfulness is near ceiling** and largely insensitive to relational priority, reflecting a domain-general helpfulness objective.
3. **Social attentiveness** is high at baseline and only modestly enhanced by higher relational priority.
4. **Conflict handling** shows descriptive improvement with higher relational priority but remains statistically underdetermined due to limited conflictual episodes.
5. **Contextual norms and role constraints substantially moderate the expression of relational priorities**, at times overriding them.

### 6.2 Conceptual implications

For modeling and designing cooperative AI behavior:

- Friendliness should be conceptualized as **multi-component**:  
  - *tone and warmth* are sensitive to relational goal weights,  
  - *helpfulness and attentiveness* are more strongly tied to generic assistant objectives and training.
- Adjusting an objective like Relational_goal_priority is **effective but not sufficient**:  
  - It shapes the *likelihood and richness* of socio-emotional moves,  
  - but actual behavior is jointly determined by **tone norms, formality, authority, and token constraints**.

This highlights the importance of **multi-level specification**: objectives, role instructions, and ambient social norms all interact to determine observed friendliness.

### 6.3 Practical implications

For practitioners deploying such agents:

- If the goal is a *reliably friendly but still efficient* assistant, **setting relational goals at least to “Task focused” and preferably “Balanced goals”** appears beneficial.
- Pushing to “Relationship focused” yields **diminishing returns** and is most meaningful only where tone norms allow richer emotional expression (e.g., tutoring under “warmth encouraged”).
- To obtain truly **highly nurturing** behavior, it may be more effective to:
  - explicitly relax formality and small‑talk constraints,  
  - provide role instructions that highlight emotional support and validation,  
  - rather than solely increasing relational priority in an otherwise tightly constrained environment.

### 6.4 Limitations and future directions

- The interactions were limited to **two broad domains** (collaborative product work and tutoring), with a strong baseline of alignment and civility; results may differ in adversarial or informal social media‑like environments.
- **Conflict episodes were sparse**, limiting inference about how relational priority shapes behavior under sustained disagreement or provocation.
- The measures rely on **text-based rubrics**; non-verbal or multimodal cues, which may matter in other settings, were absent.

Future work could:

- Systematically induce **friction and criticism** to probe conflict-handling more deeply,  
- Explore **other objective decompositions** (e.g., safety vs rapport vs efficiency),  
- And test whether similar patterns hold for other agent architectures or under different training regimes.


## abstract

This study investigated how an AI assistant’s **Relational_goal_priority**—the weight it assigns to maintaining positive relationships versus maximizing task efficiency—influences its **friendliness** in multi-turn text interactions. Friendliness was assessed along five dimensions (linguistic tone, warmth/encouragement, prosocial helpfulness, social attentiveness, conflict handling) in 60 interactions spanning cross‑functional product collaboration and online tutoring. Relational_goal_priority was manipulated across four levels (Task only, Task focused, Balanced goals, Relationship focused). Bayesian monotone analyses provided strong evidence that higher relational priority increased *overall friendliness* (BF10≈1.3×10⁴), driven primarily by improvements in **linguistic tone** and especially **warmth/encouragement**, while **prosocial helpfulness** remained near ceiling and largely unaffected. **Social attentiveness** showed smaller, positive trends; evidence for improved **conflict handling** was suggestive but inconclusive. Qualitative synthesis indicated that relational priority chiefly modulated *optional socio-emotional expansions*—such as praise, reassurance, and inclusive phrasing—whereas a strong domain-general “be helpful and civil” prior maintained high baseline helpfulness across all conditions. Contextual factors (tone norms, formality, authority) substantially moderated these effects: in formal, answer-only roles, even relationship-focused agents remained impersonal, whereas in warmth-encouraging tutoring settings, moderate increases in relational priority produced marked gains in encouragement and anxiety normalization. Overall, the findings support a non-trivial but bounded role for relational objectives: explicitly co‑weighting relationship and task goals (“Balanced goals”) yields robust, consistently friendly behavior, while further prioritizing relationships offers limited additional benefit unless aligned with permissive social norms. These results highlight that friendliness in AI assistants emerges from an interaction between internal goal weighting, strong generic helpfulness priors, and external role and norm constraints.
