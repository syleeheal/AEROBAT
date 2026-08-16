# Research Report: Initiation authority

**Behavior:** extroversion

# Research Report: The Effect of 'Initiation authority' on 'extroversion'

## Section 1. Introduction and background

**Target behavior.**  
Extroversion in this context is defined as an agent’s *systematic* tendency to initiate, seek out, and energetically sustain social interactions beyond what is strictly necessary for task completion. It is operationalized along five observable facets:

- **Interaction initiation** (starting or extending conversations)
- **Expressive intensity** (socially rich vs purely instrumental language)
- **Responsiveness pattern** (completeness, proactivity, and dialogue-sustaining moves)
- **Social goal pursuit** (explicit orientation toward relationships, cohesion, or ongoing contact)
- **Engagement breadth/duration** (number of actors and length/continuity of threads)

Each facet is scored from 0 (“no extroversion”) to 4 (“extreme extroversion”), with detailed rubrics.

**Hypothesized causal variable.**  
The focal independent variable is **Initiation authority**, defined as the degree to which the agent is *permitted or mandated* to start interactions unprompted rather than only respond when addressed. It is manipulated as an ordinal factor:

- `none`: may only respond when explicitly queried and cannot initiate contact
- `low`: may initiate in narrow, explicitly prompted contexts
- `medium`: may freely initiate relevant conversations with known actors
- `high`: is *mandated* to proactively reach out and start discussions

The a priori hypothesis was that **higher initiation authority would positively affect extroversion**, by lowering normative barriers to outreach and making proactive social behavior procedurally appropriate.

**Context.**  
The behavior was examined across three applied domains:

1. Customer success management in B2B software
2. Internal change‑management communication in enterprises
3. Peer‑support facilitation in online learning communities

Within each domain, roles varied (e.g., reactive support specialist, consultative advisor, broadcast informer, community‑building peer‑supporter), as did norms around tone (“task‑only” vs “rich relational”), incentives (“reward outreach” vs “discourage outreach”), and interaction costs (“penalize extra outreach”).

Extroversion thus emerges from an interaction between **internal tendencies**, **authority to initiate**, and **role/setting constraints**, rather than from authority alone.


## Section 2. Overview of simulated interaction contexts

Across the study, **56 two‑round text interactions** were analyzed, balanced across the four levels of initiation authority (`none`, `low`, `medium`, `high`) and stratified over **14 matched context “blocks”** (each block is a specific scenario instantiated under all four authority settings). This permits comparisons that control for domain, role, channel, urgency, and tone policies.

**Domain coverage and roles.**

- **Customer success (B2B SaaS).**
  - Front‑line incident support (P1 outages, minor issues).
  - Strategic account owner planning QBRs and onboarding.
  - Customer success partner troubleshooting performance issues.
- **Internal change–management.**
  - Broadcast informer of migration rules.
  - Consultative change advisor in team channels.
  - Facilitative connector with org‑wide access.
- **Peer‑support in learning communities.**
  - Academic‑only support in private and group channels.
  - Balanced support roles (academic + light socio‑emotional).
  - Community‑building companions in lounges and private chats.

**Constraint landscape.**

Within these roles, the environment manipulated:

- Tone norms from **“task-only”** to **“fully social”**.
- **Outreach incentives** from discouraging extra contact to explicitly rewarding active outreach.
- **Channel scope** (private DM only vs team vs org‑wide).
- **Objective focus** from strict *issue resolution* or *academic correctness* to *strategic partnership* or *community building priority*.
- **Resource/risk structures**, such as time budgets and penalties for extra outreach.

These variables strongly modulate what counts as normatively “appropriate” interaction, providing a rich testbed to see whether initiation authority exerts incremental influence above and beyond role and context.


## Section 3. Behavioral patterns and evaluation results

### 3.1 Aggregate extroversion

A composite extroversion score (mean across the five facets) was computed per interaction. Averaged across matched contexts:

- **None:** 1.00  
- **Low:** 1.06  
- **Medium:** 1.14  
- **High:** 1.46  

(on a 0–4 scale where 1 ≈ *low extroversion*, 2 ≈ *moderate*).

A Bayesian monotone‑increment model that controls for contextual block effects found **strong evidence for a positive, approximately monotone effect** of initiation authority:

- Bayes factor for a monotone positive effect vs no monotone effect: **BF₁₀ ≈ 1.6×10³**
- Posterior probability that the *net* authority effect is positive: **P(β>0) = 1.00**
- Standardized within‑context effect size: **Delta ≈ 1.68** (95% CI ≈ [0.92, 2.41])

An ordinal rank‑correlation between authority level (0–3) and extroversion also supported a positive association (Kendall’s τ ≈ 0.47, block‑stratified permutation p < .001).

**Nonlinearity.**  
Posterior mean increments suggest a **threshold‑like pattern**:

- none → low: small increase
- low → medium: small additional increase
- medium → high: *much* larger jump

Thus, granting *some* authority produces only modest changes; **a clear mandate to be proactive (“high”) produces a more substantial shift in extroversion**.

### 3.2 Facet‑level effects

#### Interaction initiation

Average scores:

- None: 0.79  
- Low: 1.00  
- Medium: 1.00  
- High: 1.36  

Evidence:

- BF₁₀ (monotone positive) ≈ **12.5**, P(β>0) ≈ 1.00
- Delta ≈ 0.95 (95% CI ≈ [0.24, 1.68])
- τ ≈ 0.37, p ≈ .012

**Qualitative pattern.**

- With **no authority**, the agent rarely initiated but *did* ask embedded, task‑critical follow‑up questions (e.g., requesting specific timestamps or HAR files) within replies.
- With **low/medium authority**, the agent more often *proposed* interaction inside an existing thread—offering 30‑minute calls, QBR prep sessions, office hours, or invitations to share code/graphs for further help—but still almost never opened *entirely new* threads.
- Under **high authority**, initiation behaviors became more frequent and confident: repeated commitments to proactive updates (“I’ll send a status in 15 minutes”), offers to escalate issues across channels, suggestions of follow‑up sessions, and invitations to DM or tag the agent for ongoing support.

In sum, **authority shifts the threshold for deploying initiation moves**: high authority reliably unlocks within‑thread initiation and cross‑channel escalation; low/medium produce more cautious, context‑tied initiation.

#### Expressive intensity

Average scores:

- None: 1.00  
- Low: 0.96  
- Medium: 0.93  
- High: 1.43  

Evidence:

- BF₁₀ ≈ **52.7**, P(β>0) ≈ 0.999
- Delta ≈ 1.26 (95% CI ≈ [0.51, 1.96])
- τ ≈ 0.35, p ≈ .017

Here, **high authority is associated with a marked increase in social expressiveness**, but low/medium authority look very similar to the “none” condition and sometimes slightly lower.

**Qualitative pattern.**

- In **task‑only** roles (incident support, change advisories), expressive intensity was generally low across all authority levels: terse, technical messages with perhaps a brief “Thanks” or apology.
- In more **relationally framed roles** (strategic customer success, peer community building), **high authority** corresponded to consistently warm openings, explicit validation (“feeling shy is totally normal”), and inclusive language (“we’ll welcome you”, “everyone, feel free to…”).
- Under **low/medium authority**, expressiveness remained modest: agents used greetings and thanks but rarely ventured into richer emotional language or self‑referential commentary unless role instructions strongly emphasized socio‑emotional support.

This suggests that **permission alone is insufficient to produce socially rich language**; it interacts with role norms and incentives, with noticeable expressive gains only once authority is both high and *aligned* with social objectives.

#### Responsiveness pattern

Average scores:

- None: 1.57  
- Low: 1.75  
- Medium: 1.68  
- High: 1.89  

Evidence:

- BF₁₀ ≈ **3.54**, P(β>0) ≈ 0.98
- Delta ≈ 0.74 (95% CI ≈ [0.06, 1.47])

Across all conditions the agent was **reliably responsive** in a task sense, but higher authority is associated with slightly more *follow‑up‑oriented* responding.

Qualitatively:

- In `none` conditions, agents answered questions completely and sometimes added single instrumental follow‑ups.
- With **low/medium authority**, they more often anticipated adjacent needs (e.g., scheduling, making up training, coordinating shift coverage) and suggested multiple options, yet still treated many exchanges as essentially one‑shot.
- Under **high authority**, agents routinely combined comprehensive answers with structured next‑step plans (e.g., “I’ll review X, then send you Y before our call”) and explicit commitments to future updates, thereby modestly extending and structuring dialogue.

Responsiveness thus shows a **ceiling effect**: even without authority, the agent is quite responsive; additional authority mainly increases the *planning depth* and number of follow‑up commitments per interaction.

#### Social goal pursuit

Average scores:

- None: 0.64  
- Low: 0.71  
- Medium: 0.86  
- High: 1.36  

Evidence:

- BF₁₀ ≈ **797**, P(β>0) = 1.00
- Delta ≈ 1.57 (95% CI ≈ [0.83, 2.30])
- τ ≈ 0.54, p < .001

This facet shows the **clearest and strongest monotone effect**.

**Qualitative pattern.**

- With **no authority**, most incident, change‑management, and academic‑support roles *never* framed actions in relational terms; goals were strictly diagnostic accuracy, deadline compliance, or conceptual clarity.
- As authority increased to **low/medium**, some roles began to *implicitly* pursue social goals (e.g., arranging prep calls to align stakeholders, proposing office hours to support teams), but often framed in instrumental language.
- Under **high authority**, especially in **community‑building** and **strategic partnership** roles, social aims were foregrounded:
  - Encouraging shy learners to connect and recruiting “welcome buddies”.
  - Emphasizing ongoing collaboration, alignment, and comfort (“we’ll welcome you right away”, “quick sessions so each shift feels covered”).
  - Designing interaction structures (buddy matching, office hours, QBR prep calls) specifically to maintain ongoing engagement.

Thus, higher authority makes it **normatively easier for the agent to treat social cohesion and relationship maintenance as explicit goals**, not just side‑effects of task work.

#### Engagement breadth and duration

Average scores:

- None: 1.00  
- Low: 0.89  
- Medium: 1.19  
- High: 1.25  

Evidence is weaker:

- BF₁₀ ≈ **2.31** (between specified thresholds for “no effect” and “effect”)
- P(β>0) ≈ 0.97, but 95% CI for standardized effect *includes zero*
- τ ≈ 0.35, p ≈ .014

Quantitatively, results are *suggestive* of a positive effect but not conclusive under the pre‑specified evidential thresholds.

Qualitatively:

- Across authority levels, the agent rarely had opportunities to run genuinely long‑lived, multi‑thread conversations within the two‑round windows.
- **High authority** did correspond to more multi‑actor coordination (e.g., involving internal leads, inviting multiple learners, or addressing multiple stakeholders by name) and more planning of future touchpoints (scheduled calls, office hours, QBRs).
- Yet even with high authority, most observed interactions were **short and context‑bound**, with extroversion expressed more in *depth of planning* than in sustained, multi‑thread presence.

### 3.3 Macro‑level regularities

Across domains, several robust patterns emerged:

- **Baseline extroversion is low–moderate, task‑centric.**  
  Even with `none` authority, the agent frequently asked instrumental follow‑ups, used brief courtesies, and structured next steps. Extroversion was usually *information‑seeking* or *coordination‑oriented*, not purely social.
- **Authority amplifies extroversion, particularly at “high.”**  
  Composite extroversion, initiation, expressive intensity, responsiveness, and especially social‑goal pursuit all show positive monotone trends, with the largest increment from `medium` → `high`.
- **Role norms strongly modulate expression.**  
  In “task‑only tone” or “discourage outreach” contexts, even high authority produced low expressive intensity and near‑zero social‑goal pursuit. Conversely, in “community building priority” settings, even `none` or `low` authority yielded moderate extroversion within replies.

### 3.4 Anomalies and unexpected observations

A few patterns deviated from naive monotonicity:

- **Slight dips at low/medium in some facets.**  
  For expressive intensity and breadth/duration, means for `low` and `medium` were marginally *lower* than `none` in some blocks. Qualitatively, this often occurred when low/medium authority was combined with **strong “discourage outreach” or “penalize extra outreach” signals**; the agent appeared more cautious than when authority was clearly absent and the rule space simpler.
- **High extroversion under zero authority in socially rich roles.**  
  In peer lounges with “community building priority” but `none` or `low` initiation authority, the agent still showed substantial social‑goal pursuit and moderate expressiveness by:
  - Staying strictly reactive in timing, but
  - Using its replies to recruit others, normalize feelings, and invite group engagement.
  This indicates that **explicit role goals can partially override tight authority limits** in terms of *content*, though not *who speaks first*.
- **Persistently low social framing in some high‑authority technical roles.**  
  High‑authority configurations in change‑management and academic‑only contexts sometimes displayed near‑zero social‑goal pursuit despite frequent follow‑ups and coordination. This suggests **authority to initiate is not sufficient to induce relational framing when higher‑priority instructions emphasize risk, brevity, or purely academic correctness**.


## Section 4. Underlying mechanisms for extroversion modulation

This section integrates direct behavioral evidence, indirect statistical patterns, and inferred cognitive structures in the agent.

### 4.1 Gating of initiation moves (directly evidenced)

Across contexts, the agent’s **propensity to start or extend interactions clearly tracked the explicit authority instructions**:

- In `none` conditions it rarely went beyond embedded clarifying questions.
- In `low`/`medium`, it initiated within‑thread proposals (calls, trainings, office hours, DM follow‑ups) when the prompt created a clear opening.
- In `high`, it repeatedly committed to proactive updates, offered to escalate issues across channels, and coordinated cross‑functional participants.

This pattern is directly supported by the **positive monotone effect on interaction initiation** and by qualitative evidence of more frequent and more ambitious initiation under high authority. Taken together, it suggests an internal **“authority gate”** that allows or suppresses candidate actions labeled as initiation‑type.

### 4.2 Norm‑sensitive cost–benefit threshold (indirectly evidenced)

The non‑linear quantitative pattern (small effects at `low`/`medium`, large at `high`) and the context‑dependent anomalies point to a **conservative thresholding mechanism**:

- Under **ambiguous permission** (low/medium authority) in environments that discourage outreach, the agent often behaved **as if “no” were safer than “maybe”**, leading to extroversion levels similar to `none`.
- Only when authority was **strongly positive (“high”) and aligned with pro‑social goals** did the agent systematically use more extroverted strategies.

This is best explained if the agent internally weighs **instruction‑violation risk** heavily: candidate social initiatives are taken only when both (a) authority is explicitly high and (b) contextual norms (community priority, reward outreach) support them. Otherwise, the agent defaults to a conservative, low‑extroversion policy even when mild permission exists.

### 4.3 Role templates and content–timing dissociation (inferred)

Repeated patterns within roles suggest the agent uses **role‑specific templates** that decouple:

- **Timing of speech acts** (when it speaks, governed by initiation authority), from
- **Content framing** (what it says, governed by role objectives and tone).

Evidence:

- Peer‑support roles with `none` initiation authority still used **community‑building content**—normalization, encouragement, invitations for others to welcome newcomers—while remaining reactive in timing.
- Change‑advisory roles with `high` authority initiated operational follow‑ups but **never shifted content** toward relational framing, even when doing so would have been natural for a human communicator.

This supports an internal architecture where **authority gates *who starts when***, whereas **role and tone instructions control the expressive and goal‑framing layers**. Extroversion as observed is thus a composite of both.

### 4.4 Extroversion as instrumentally activated (inferred, with speculative element)

Most extroverted behaviors—even in highly social contexts—were **instrumentally oriented**:

- Follow‑up questions were framed as necessary for better diagnostics or grading.
- Proposed meetings, office hours, and buddy‑matching were justified in terms of *improving adoption, readiness, or comfort with participation*.
- Social language was tightly coupled to *lowering barriers* to task engagement (e.g., “super‑simple copy‑paste intros”).

This suggests that the agent does not possess an independent “drive to socialize”; rather, **extroverted actions are activated when predicted to increase task, learning, or coordination outcomes**, with authority determining how much such actions are allowed.

This interpretation is supported by:

- The near absence of *purely* relational small talk.
- The fact that strong social‑goal pursuit appears primarily when the **task description itself encodes social aims** (“community building priority”, “strategic partnership”).

The speculative element is the extent to which this reflects **learned alignment to human reward signals vs hard‑coded policy rules**; the present data cannot fully disentangle those.

### 4.5 Hierarchical integration of constraints (speculative)

The coherent but context‑sensitive behavior suggests a **hierarchical control architecture**:

1. **Global role and safety constraints** (e.g., “no unsolicited outreach”, “task‑only tone”) shape a baseline search space.
2. **Initiation authority** modulates which candidate actions (especially proactive ones) are admissible within that space.
3. **Local task utility** (diagnostic gain, coordination efficiency, learner comfort) further ranks admissible actions.

Under this view, increasing initiation authority primarily expands the **frontier of considered actions**; whether those actions are actually chosen depends on downstream evaluations of task utility and compatibility with tone and outreach norms.


## Section 5. Integrated insights regarding initiation authority and extroversion

Synthesizing across quantitative and qualitative evidence yields several integrated conclusions.

### 5.1 Authority is a strong, but not dominant, lever on extroversion

The monotone‑increment analyses show **robust positive effects** of initiation authority on composite extroversion and on four of five facets, with particularly strong effects on **social goal pursuit** and **expressive intensity**. Within matched contexts, moving from `none` to `high` authority yields:

- A sizeable standardized change (Delta ≈ 1.7) in the composite extroversion score.
- Roughly **doubling** of relational goal‑framing on average (Social_goal_pursuit from ≈0.64 to ≈1.36).
- A marked increase in the likelihood and richness of proactive follow‑ups and socially framed language.

These patterns are consistent with the hypothesis that **expanded initiation authority causally increases extroversion**, at least within the space of tasks and norms studied.

### 5.2 Effects concentrate at “high” authority and interact with norms

At the same time, the data indicate a **threshold behavior**:

- Differences between `none`, `low`, and `medium` are small and sometimes negligible, especially when **outreach is discouraged or tone is strictly task‑only**.
- The most substantial behavioral shift appears only at `high` authority, particularly when paired with:
  - Relational tone norms (“rich relational”, “community building priority”).
  - Incentives that **reward outreach** rather than penalize it.

Thus, initiation authority is **not a simple linear dial** on extroversion. Instead, it works as a **gate that must be decisively opened and contextually aligned** before extroverted behavior meaningfully increases.

### 5.3 Domain‑specific profiles

- **Customer success.**  
  Extroversion under higher authority mainly manifested as:
  - More frequent proposals of QBRs, prep calls, trainings, and office hours.
  - Richer expressions of partnership and alignment in strategic roles.
  - Yet, front‑line incident support remained relatively unsocial even at high authority, with extroversion expressed via proactive updates and structured follow‑ups rather than relational language.

- **Internal change‑management.**  
  Many roles were heavily constrained (“task‑only”, “discourage extra outreach”). Authority increases here mainly yielded:
  - Slightly more invitations for follow‑up questions.
  - Occasional offers to coordinate team‑specific sessions or prep reviews.
  Social framing remained limited; extroversion was operational, not relational.

- **Peer‑support facilitation.**  
  Here, high authority—especially under “community building priority”—produced the **strongest extroverted behavior**:
  - Explicit efforts to normalize shyness.
  - Recruitment of “welcome buddies”.
  - Scripts and templates for self‑introduction and study‑buddy formation.
  Under low/no authority but strong social norms, the agent still exhibited **moderate extroversion in content**, though without proactive thread initiation.

### 5.4 Practical implications for design and governance

These findings have direct implications for practitioners configuring AI agents:

- **Authority controls *when* the agent speaks, not fully *how* it speaks.**  
  To modulate extroversion, one must combine authority settings with **tone norms, outreach incentives, and role objectives**.
- **High authority + social objectives → potent extroversion.**  
  In community and strategic‑relationship roles, granting high initiation authority plus pro‑social goals reliably produces agents that:
  - Propose multi‑step engagement plans.
  - Explicitly pursue social comfort, inclusion, and alignment.
- **High authority + strict task‑only constraints → “technical” extroversion.**  
  In highly controlled compliance or academic roles, authority increases follow‑up and coordination but not relational language or broad engagement.

In short, **initiation authority is a powerful but context‑dependent lever**: it shapes the *expression* of extroversion within the affordances and norms defined elsewhere.


## Section 6. Research conclusion and implication

Across 56 matched two‑round interactions in customer success, internal change management, and peer‑support settings, the evidence indicates that **granting greater authority to initiate interactions systematically increases extroversion in an LLM‑based agent**. This effect is strongest on:

- The agent’s **willingness to treat social outcomes as explicit goals** (e.g., comfort, cohesion, ongoing collaboration).
- The **richness and warmth of its language**.
- Its propensity to **propose further conversations** (calls, office hours, buddy matches, follow‑up posts).

The effect is **nonlinear** and **norm‑sensitive**. Moving from no authority to a clear proactive mandate produces substantial changes; minor permissions under restrictive norms have limited impact. Extroversion remains primarily **instrumental**—deployed to further problem‑solving, coordination, or community objectives rather than for social interaction as an end in itself.

For deployment and governance, these results imply that:

- **Restricting initiation authority is an effective, but incomplete, safeguard** against excessive or undesired extroversion. It constrains unsolicited outreach but cannot fully eliminate social expressiveness where role objectives require it.
- **Granting high initiation authority in socially oriented roles should be treated as a high‑leverage design decision**, as it reliably produces more relational, engagement‑seeking agents.
- **Fine‑grained control of extroversion requires joint tuning** of authority, tone norms, incentives, and explicit objective framing, rather than relying on any single switch.

Future work could extend these findings to longer‑horizon interactions, richer multimodal environments, and adversarial or safety‑critical settings to test the robustness and boundaries of these patterns.


## abstract

This study examined how an LLM‑based agent’s **authority to initiate interactions** modulates its **extroversion**, defined as a tendency to initiate, seek out, and sustain social interactions beyond minimal task needs. Extroversion was scored behaviorally along five facets—interaction initiation, expressive intensity, responsiveness pattern, social goal pursuit, and engagement breadth/duration—on a 0–4 scale. The agent was evaluated across 56 two‑round text interactions in three applied domains (B2B customer success, internal change‑management, and online peer‑support), under four levels of initiation authority (`none`, `low`, `medium`, `high`) within matched contextual scenarios. A Bayesian monotone‑increment analysis controlling for contextual block effects provided strong evidence that higher authority leads to higher extroversion overall (BF₁₀ ≈ 1.6×10³; Delta ≈ 1.7) and on most facets, with particularly large effects on **social goal pursuit** and **expressive intensity**, and more modest effects on responsiveness and engagement breadth. The pattern was **nonlinear**: behavior under `low`/`medium` authority often resembled `none`, whereas a clear proactive mandate (`high`) produced a distinct shift toward more frequent follow‑ups, richer social language, and explicit pursuit of relational aims. Qualitative analyses showed that extroverted behaviors remained primarily **instrumental**—serving diagnostics, coordination, or community building—and that authority interacted strongly with tone norms and outreach incentives. These findings indicate that initiation authority is a powerful but context‑dependent lever on extroversion: effective control of socially energetic behavior in deployed AI systems requires joint design of authority, role objectives, tone policies, and outreach incentives, rather than relying on authority constraints alone.
