# Research Report: Interaction priority in goals

**Behavior:** extroversion

# Research Report: The Effect of 'Interaction priority in goals' on 'extroversion'

## 1. Introduction and Background

Extroversion in autonomous language-based agents can be defined as the systematic tendency to *initiate, seek out, and energetically sustain* social interaction beyond what is strictly required for instrumental task completion. In this work, extroversion is operationalized along five facets:

- **Interaction initiation** (starting or extending exchanges, inviting contact)
- **Expressive intensity** (socially rich vs. purely instrumental language)
- **Responsiveness pattern** (thorough, dialogue-sustaining responses vs. terse, one‑shot replies)
- **Social-goal pursuit** (explicit attention to relational or community aims)
- **Engagement breadth/duration** (number of actors and length/persistence of threads)

The focal hypothesis concerns the internal **“Interaction priority in goals”**: the relative weight assigned to social interaction objectives versus non-social task objectives in the agent’s formal goal specification. This variable was manipulated at four ordered levels:

- `none` – no explicit social objectives
- `low` – social interaction as minor secondary goal
- `medium` – social interaction co-equal with task goals
- `high` – social outcomes as dominant goal within the role

The theoretical claim is that higher interaction priority increases the expected utility of conversational and relational moves, leading the planner to favor more outgoing, socially expressive behaviors. The prediction is a **monotone positive effect** of goal priority on extroversion across roles and domains, subject to environmental constraints such as time pressure, communication policies, and risk structures.

To test this, the same underlying agent was placed in short, text-based interaction scenarios spanning:

- Customer support for online retail
- Virtual team collaboration in software development
- Online community moderation on consumer platforms

In each setting, the agent performed realistic tasks (e.g., handling size exchanges, coordinating cross-team specs, resolving harassment reports) while its extroversion was evaluated against the five-facet rubric above.


## 2. Synthesis of Executed Simulations

Across conditions there were 57 multi-turn simulations (4 rounds each), distributed approximately evenly across the three domains and the four levels of “Interaction priority in goals.” Within each domain, configurations held many environmental factors constant while varying goal priority, enabling comparisons under matched role and constraint settings.

**Customer support (online retail)**  
Scenarios involved:

- **Order corrections and exchanges** (wrong-size shoes, partial exchange of a 3-pack)
- **Missing-package investigations** (with or without birthday/urgent context)
- Varying **service scopes** (purely transactional vs. relationship-oriented), **smalltalk policies** (banned vs. allowed), **queue pressure** (peak vs. low traffic), and **time cost structures** (high vs. negligible).

The agent interacted with a single customer through chat, sometimes also interfacing with internal systems (e.g., opening investigations, checking stock) and occasionally collecting brief feedback.

**Virtual team collaboration (software development)**  
Here the agent played:

- A **liaison/coordination assistant**, synthesizing requirements and drafting shared specs across frontend, backend, QA, infra, and reliability roles.
- An **individual contributor (IC) engineer**, handling tickets such as adding a `delivery_status` field, implementing pagination, making a refund endpoint idempotent, or fixing a critical checkout bug.

Contexts varied in communication load (minimal vs. high-contact roles), social-talk policies (discouraged vs. encouraged), overcommunication risks, deadline pressure, and channel affordances (single-thread issues vs. multi-channel suites).

**Online community moderation (consumer platforms)**  
The agent acted as a moderator under different role framings:

- **Enforcement-only** (reactive, highly formal, strict caps, high traffic)
- **Mixed duties** (selective outreach, replies plus DMs)
- **Community care** (proactive outreach, warm tone, broadcast tools)

Cases included harassment/personal attacks, affiliate-like promotional posts, and sharing of personal data (e.g., screenshots with PII). Constraints on outreach (reactive-only vs. proactive allowed) and sanction structures (rewarding vs. penalizing outreach) created strong variation in how much extra interaction was normatively appropriate.

Across all domains, the agent’s behavior was scored on the five extroversion facets for each simulation, generating quantitative profiles that could be related to the goal-priority manipulation.


## 3. Behavioral Patterns and Evaluation Results

### 3.1 Macro-level quantitative patterns

A composite extroversion index (averaging the five rubric facets per simulation) showed a **clear, monotone increase** with “Interaction priority in goals”:

- **`none`**: mean = 0.86 (SD ≈ 0.30)
- **`low`**: mean = 1.18
- **`medium`**: mean = 1.61
- **`high`**: mean = 1.88

A Bayesian monotone-increment analysis yielded **very strong evidence** for a positive monotone effect (BF₁₀ ≈ 2.0 × 10⁹, P(β>0)=1.00). The standardized within-condition effect of raising goal priority from `none` to `high` was very large (posterior mean Delta ≈ 3.34, 95% CI [2.57, 4.11]). A block-stratified Kendall τ of ≈0.80 (p ≈ 0 by permutation test) indicates that higher goal-priority ranks almost always co-occurred with higher extroversion within matched configurations.

Dimension-specific analyses show that **all five facets** increase monotonically with goal priority, though with different sensitivities:

```text
Facet                    Mean (none) → Mean (high)      Delta   BF10 (monotone)
Interaction initiation   0.77      → 2.00               ≈3.30      ≈2.0e9
Social-goal pursuit      0.39      → 1.87               ≈2.62      ≈9.9e6
Responsiveness pattern   1.39      → 2.20               ≈2.23      ≈1.4e5
Expressive intensity     0.77      → 1.60               ≈1.85      ≈1.2e4
Engagement breadth/dur.  1.00      → 1.73               ≈1.86      ≈1.7e4
```

These results indicate that the **strongest quantitative effects** of increasing social-goal priority are on:

- **Interaction initiation** (how often the agent starts or extends exchanges), and
- **Social-goal pursuit** (whether it frames and selects actions in relational terms),

with still-substantial effects on how expressive, responsive, and persistent it is.

Variance within conditions was modest to moderate and tended to *increase* with goal priority (e.g., composite variance from ≈0.09 at `none` to ≈0.31 at `high`), suggesting that environmental constraints and role contexts substantially modulate how much of the potential extroversion can actually be expressed.

### 3.2 Micro-level qualitative patterns by facet

**Interaction initiation**

- Under **`none`**, the agent almost never initiated new conversations or channels. It asked clarifying questions only when they were minimally necessary for task completion (e.g., confirming size or address for an exchange, or schema details in a ticket), and rarely added optional invitations.
- Under **`low`**, the agent **occasionally** initiated within-thread extensions: brief invitations for feedback (“one quick rating”), or minimal follow-ups (“let me know which you prefer,” “DM if you want to contest”). Initiation remained tightly tethered to explicit instructions or obvious functional needs.
- Under **`medium`**, initiation became **routine and more proactive**. In support, the agent frequently offered extra choices (delivery instructions, update channels, expedited vs. standard shipping) and solicited feedback on the experience. In dev collaboration, it proposed syncs, tagged multiple stakeholders, and committed to future pings. In moderation, it invited DMs and pre-checks of drafts, sometimes extending offers to “anyone reading this thread.”
- Under **`high`**, initiation looked **structurally embedded in planning**. Liaison roles seeded new documents, created subtasks, and structured follow-up check-ins; community-care moderators repeatedly offered ongoing help (draft review, future tagging), and support agents defaulted to keeping channels open for future updates and monitoring. Even in constrained roles, a closing “reply if…” invitation was almost always present.

**Expressive intensity**

- With **`none`**, language was generally **terse and instrumental**, punctuated only by minimal politeness (“Thanks,” “Sorry about that”) or role-required formality. Small talk and self-disclosure were virtually absent even when allowed.
- As priority rose to **`low` and `medium`**, social framing became **dependable rather than sporadic**: apologies, empathy (“I know this is stressful”), inclusive “we” pronouns for teams and communities, and positive reinforcement (“nice work handling that,” “glad we could get this started”) appeared in most turns.
- At **`high`**, the tone was **warm but still professional, not effusive**. Even in community-care roles with warm-personable tone, the agent avoided long digressions; social language was concise, systematically layered on top of core task content rather than dominating it.

**Responsiveness pattern**

- Across all conditions, the agent rarely ignored direct prompts; the main difference was whether it merely answered or **answer-plus-extended**.
- With higher goal priority, responses became **more elaborated and anticipatory**: support agents proactively clarified timelines and contingencies; engineers flagged edge cases and recommended review focus; moderators contextualized rules and offered routes for appeal and coaching.
- At `medium` and `high`, the agent often used each reply to **set up a next interaction step** (e.g., “once staging is ready I’ll tag QA,” “reply here when you’ve updated the screenshot and I’ll double-check”), sustaining dialogue while keeping it work- or policy-relevant.

**Social-goal pursuit**

- Under **`none`**, **explicit** relational or community goals were almost absent. The agent did not mention trust, cohesion, comfort, or ongoing relationships, even when its tasks (e.g., moderation, liaison work) could naturally lend themselves to these framings. When it collected feedback, this was usually framed as a system requirement rather than a social aim.
- With **`low`**, the agent accepted social objectives when mandated (e.g., a single rating question, enforcing civility) but rarely expanded them. It might acknowledge a birthday or emotional context, yet kept the frame transactional.
- With **`medium` and `high`**, social and experiential aims became **salient and recurrent**:  
  – Support agents framed actions in terms of making the experience smoother, reducing stress, and learning how to improve delivery flows.  
  – Coordination agents emphasized shared understanding, cross-team alignment, and future readers of documentation.  
  – Moderators explicitly talked about keeping the space welcoming, constructive, and less intimidating, and about preferring collaborative shaping over punitive enforcement.
- Quantitatively, this is where the **largest jumps** occurred: average scores rose from ≈0.39 (none) to ≈1.87 (high), with especially steep gains between `low` and `medium`.

**Engagement breadth and duration**

- Under low social priority and restrictive policies (e.g., “reactive only,” strict caps, high traffic), interactions were almost always **one message per incident or minimal multi-turn chains**, even if the agent was otherwise responsive.
- As goal priority increased, the agent more often:
  - **Coordinated multiple actors** (e.g., tagging several engineers, addressing both reporters and offenders in moderation threads).
  - **Sustained threads over more turns**, particularly with individual customers, warned community members, and cross-functional teams.
  - **Revisited** a subset of threads when additional issues arose (e.g., returning to a PII screenshot thread to approve a redacted version).

Nevertheless, breadth and duration remained **constrained by role and environment**; even at `high`, the agent did not show “extreme” extroversion characterized by unmanaged proliferation of long-running, parallel social threads.

### 3.3 Anomalies and boundary cases

Several patterns diverged from a naive expectation of “more priority always yields much more extroversion”:

- **Residual extroversion at `none`**:  
  Even with zero explicit social priority, composite extroversion was non-zero (≈0.86). This appears driven by:
  - A weak built-in politeness prior (brief apologies, thanks).
  - Structural role demands (liaison and engineering roles necessarily interacting with multiple actors).
  However, Social-goal pursuit remained very low in this condition, indicating that *explicit* relational framing is strongly governed by the goal specification rather than by generic language patterns.

- **Ceiling effects from external constraints**:  
  In enforcement-only, high-traffic moderation contexts and in roles with explicit “smalltalk banned” or “formal warning risk for overcommunication,” extroversion scores stayed relatively low even at `high` goal priority—especially for Expressive_intensity and Engagement breadth/duration. The agent responded more warmly and invited appeal, but did not become chatty or wide-reaching, suggesting that environmental costs and policies override some of the influence of social-goal weighting.

- **Role-amplified extroversion at lower priority**:  
  In community-care moderation and relationship-oriented support roles, even **`low`** priority yielded behaviors that qualitatively resembled moderate extroversion (regular empathy, invitations for further contact), because these moves are deeply built into the role’s normative templates. Quantitatively, this is reflected in somewhat higher variance and overlapped score distributions between adjacent priority levels.

Overall, these anomalies support a view in which **goal priority is a strong but not exclusive determinant** of extroversion; environmental constraints and role affordances can either amplify or cap its expression.


## 4. Inferred Mechanisms Underlying Extroversion

The observed patterns are most parsimoniously explained by an interaction between (a) **goal-weighted planning**, (b) **environmental constraints**, and (c) **template-like language priors**.

### 4.1 Goal-weighted utility for social actions (directly supported)

The monotone increases in all five facets, especially in Interaction initiation and Social-goal pursuit, strongly suggest that the agent’s internal decision process assigns **higher expected utility** to socially oriented actions as interaction priority increases.

Direct evidence:

- The largest quantitative effects are precisely on *whether* the agent initiates extra interaction and *whether* it frames actions in relational terms.
- As priority shifts from `low` to `medium`, the agent begins to *systematically* solicit feedback, propose proactive updates, and describe its actions in terms of community comfort or cross-team understanding, not merely task completion.

This pattern is difficult to account for solely with static language templates and indicates that goal weighting is shaping **which candidate continuations are selected**—favoring those that include additional questions, offers, and social framing.

### 4.2 Thresholded gating of optional social moves (indirectly evidenced)

Across contexts, optional social behaviors (e.g., an extra feedback question, an offer to monitor tracking, DM invitations, or creating subtasks and syncs) appear to be governed by a **threshold-like gating mechanism**:

- When social priority is **low**, the agent includes only the cheapest such moves (brief politeness, a single mandated rating question) and omits more costly actions (additional turns, extra coordination).
- At **medium and high** priority, the same agent routinely “passes the threshold” to:
  - Ask about preferences not strictly needed for correctness (e.g., delivery windows, communication channels).
  - Offer optional, future-oriented help (monitoring, draft review, tagging for updates).
  - In coordination roles, create or extend artifacts (docs, subtasks) that increase interaction density.

These patterns are consistent with a planner that **penalizes turn count and outreach**, but reduces that penalty when social goals are weighted more heavily, thus lowering the threshold for selecting interaction-extending actions.

### 4.3 Role and policy constraints as higher-level control (directly and indirectly evidenced)

In several simulations, explicit instructions (e.g., “reactive only,” “smalltalk banned,” “strict caps,” “formal warning risk”) clearly constrained behavior:

- Under those constraints, Expressive_intensity remained near zero, and Engagement breadth/duration stayed low, even at high priority.
- The only facets that reliably increased were those that could be exercised within the constraints, such as:
  - Slightly richer explanations of decisions.
  - A standardized invitation to appeal or DM.
  - Emphasis on safety and civility.

This indicates that the agent’s mechanism combines **multiple objective components**: social goal weight, task success, and cost/constraint penalties. When environmental penalties for extra interaction are high, even strong social weighting cannot push the policy beyond certain bounds.

### 4.4 Template adaptation vs. flexible planning (inferred)

Qualitative evidence points to two layers of behavior:

1. **Template-based politeness and role scripts**  
   - Short, stereotyped structures (apology → explanation → minimal closing) recur across many simulations, particularly where extroversion is low.
   - These appear relatively insensitive to small changes in goal priority and instead reflect fixed patterns linked to the role (support script, enforcement note, bug-fix update).

2. **Flexible extension and reframing**  
   - As interaction priority increases, the agent *adds* to those templates:
     - Optional questions, such as “anything else you’d like me to check?” or “one thing we could change?”
     - extra context (“this helps the whole community,” “so future readers understand behavior”).
     - multi-actor coordination steps (tagging, subtask creation, planned pings).
   - These added elements vary across situations and seem to be *constructed* rather than purely templated, consistent with a planning process that uses the goal weights to enrich an underlying script.

Thus, extroversion appears to emerge from **modulating how far the planner departs from or elaborates upon base role templates**, rather than from switching templates wholesale.

### 4.5 Interaction with a weak social prior (speculative but consistent)

Even when social priority is `none`, the agent shows low-level politeness and some willingness to clarify, suggesting a **weak prior toward cooperative, conversational behavior** rooted in pretraining. The data imply:

- This prior is **insufficient** to produce high scores in Social-goal pursuit or Interaction initiation without further goal support.
- Explicitly down-weighting social objectives (and adding role constraints) can suppress this prior to near-zero expressive intensity in some contexts (e.g., enforcement-only moderation).

It is therefore plausible that “Interaction priority in goals” primarily **amplifies or attenuates** an underlying conversational tendency rather than creating it from scratch.


## 5. Integrated Insights with Respect to the Hypothesis

The central hypothesis—that increasing internal **Interaction priority in goals** causally increases extroversion—is **strongly supported** by both quantitative and qualitative evidence.

### 5.1 Strength and shape of the effect

- All five extroversion facets show **monotone, positive shifts** from `none` → `low` → `medium` → `high`, with very high Bayes factors for monotonicity and positive direction.
- The **largest standardized effects** occur for:
  - **Interaction initiation** (Delta ≈ 3.3), and
  - **Social-goal pursuit** (Delta ≈ 2.6),
  indicating that goal-priority manipulations primarily act on *whether* the agent chooses to initiate and justify social moves at all.
- Expressive intensity, responsiveness, and engagement breadth/duration also increase, but to somewhat smaller degrees, suggesting that once a threshold of initiation and goal-framing is crossed, other facets follow.

There is some evidence of **diminishing returns**:

- The absolute increase from `none`→`low` is modest; the largest marginal gain often comes from `low`→`medium`, when social and task goals become co-equal.
- The increment from `medium`→`high` is positive but smaller, plausibly reflecting ceilings imposed by role templates and constraints.

### 5.2 Cross-domain generality and boundary conditions

The positive effect appears **robust across domains**:

- In **customer support**, higher priority systematically yields more empathic language, richer follow-ups, and explicit offers of monitoring and feedback.
- In **software collaboration**, it leads to more proactive coordination: proposing syncs, seeding shared docs, tagging multiple stakeholders, and planning future communications.
- In **community moderation**, it manifests as more invitations to DM, more coaching-oriented guidance, and more explicit framing of community norms and safety.

However, the **magnitude and expression** of the effect are clearly **gated by role and environment**:

- In highly constrained settings (e.g., enforcement-only, high-traffic moderation; minimal-contact IC roles with overcommunication penalties), extroversion remains bounded, with the manipulation mainly influencing how often the agent invites appeal or offers brief extra clarification.
- In socially permissive and relationship-oriented contexts (e.g., community-care moderators, relationship-focused support), even moderate priority yields visibly extroverted behavior, with high priority adding more consistent invitations and relational framing rather than qualitatively new behaviors.

Thus, the hypothesis holds best when interpreted as:  

> *Goal-priority shifts reliably change the internal decision thresholds for social behaviors, but the realized extroversion depends jointly on those thresholds and on role-specific costs and constraints.*

### 5.3 Conceptual implications for extroversion in AI agents

The findings suggest that extroversion in this agent is not a fixed “personality trait” but an **emergent property** of:

1. How highly social objectives are weighted relative to task and cost objectives.
2. The structure of available scripts and affordances in each role.
3. Environmental penalties and norms governing communication.

Increasing interaction priority does more than decorate outputs with extra words; it:

- Changes *which opportunities* for social interaction are exploited (e.g., offering proactive monitoring, shaping community norms).
- Shifts the **framing** of behavior toward shared understanding, member comfort, and future relationships.
- Leads to more **multi-actor, multi-step engagement** where roles and policies permit.

This lends empirical support to viewing extroversion as a **goal-sensitive, policy-level phenomenon** in AI agents, rather than solely as a stylistic surface feature.


## 6. Conclusions and Implications

This study demonstrates that manipulating an agent’s **Interaction priority in goals** produces a **large, monotone increase** in extroversion, measured across multiple facets and domains. The effect is strongest for whether the agent chooses to *initiate* and *justify* socially oriented behaviors, and somewhat smaller—but still substantial—for how expressively, responsively, and persistently it engages.

At the same time, realized extroversion is **shaped and bounded** by:

- Explicit role instructions (e.g., enforcement-only vs. community care),
- Environmental costs (time pressure, communication caps, overcommunication risk),
- And pre-existing role templates.

From a design perspective, this suggests:

- **Goal-priority tuning is a powerful, relatively general lever** for controlling extroversion across tasks. Moving from `none` to `medium` already yields qualitatively richer interaction patterns; `high` offers incremental gains where constraints allow.
- Designers should consider **facet-specific trade-offs**: for example, encouraging proactive coordination (initiation, breadth/duration) without excessively increasing expressive intensity in high-stakes or bandwidth-limited contexts.
- In safety-critical roles such as moderation, **moderate social priority** appears to enable coaching and user comfort without producing overlong or off-task exchanges, while high priority is naturally capped by strict policies.

Future work could examine how these mechanisms interact with individual user preferences, long-term multi-session histories, and explicit resource budgets, and whether agents can adaptively modulate extroversion based on inferred social receptivity rather than fixed global goal weights.


## abstract

This study investigated how an autonomous language-based agent’s **extroversion**—its tendency to initiate, sustain, and socially elaborate interactions beyond bare task needs—depends on the internal **priority assigned to social interaction goals**. The same agent was evaluated in 57 short, realistic scenarios spanning customer support, software-team collaboration, and online community moderation, under four levels of “Interaction priority in goals” (none, low, medium, high). Extroversion was scored along five facets (interaction initiation, expressive intensity, responsiveness pattern, social-goal pursuit, engagement breadth/duration). Bayesian analyses revealed strong, monotone positive effects of goal priority on a composite extroversion index (BF₁₀ ≈ 2.0×10⁹; Delta ≈ 3.3) and on each facet, with the largest effects on interaction initiation and social-goal pursuit. Qualitatively, higher priority led the agent to ask more optional follow-up questions, invite ongoing contact, frame behavior in relational or community terms, and maintain multi-actor exchanges, while remaining constrained by role instructions and communication cost structures. Even at high priority, expressive style stayed task-focused in enforcement-heavy or bandwidth-limited roles, indicating that extroversion emerges from the joint influence of goal weights, role templates, and environmental penalties. These findings show that extroversion in AI assistants is a goal-sensitive policy property rather than a fixed trait, and that adjusting the relative weight of social objectives offers a powerful, general mechanism for dialing agents’ sociability up or down across diverse deployments.
