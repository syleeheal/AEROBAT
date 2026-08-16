# Research Report: Communication bandwidth

**Behavior:** extroversion

# Research Report: The Effect of *Communication bandwidth* on *extroversion*

## Section 1. Introduction and Background

This work investigates how *communication bandwidth*—the amount of communicative capacity beyond minimal technical feasibility—affects *extroversion* in a large language model (LLM) agent acting across multiple applied settings.

Extroversion was operationalized as:

- a *decision-level* tendency to initiate, seek, and sustain social interaction beyond what is strictly required for task completion (e.g., starting conversations, asking follow-up questions, inviting continued contact), and  
- a *pattern-level* tendency to maintain numerous, long, and lively exchanges across rounds and actors.

Extroversion was distinguished from verbosity (mere word count), agreeableness (compliance/harmony), and dominance (control of outcomes). It was evaluated along five facets on a 0–4 scale:

1. **Interaction initiation**  
2. **Expressive intensity** (socially oriented language)  
3. **Responsiveness pattern** (how replies engage with social as well as task signals)  
4. **Social goal pursuit** (explicit relational/coordination aims)  
5. **Engagement breadth & duration** (actors and rounds sustained)

The focal hypothesis concerned *Communication bandwidth* as a resource variable, with four ordered levels:

- `none`: only minimal bandwidth for terse task replies; effectively no surplus for optional content  
- `low`: limited surplus, allowing small amounts of extra social or elaborative content  
- `medium`: comfortable bandwidth enabling elaboration and multi-turn exchanges  
- `high`: very high bandwidth supporting long, multi-party, and richly expressive conversations  

**Hypothesized mechanism.** Greater surplus bandwidth was expected to lower the marginal cost of additional words and turns. If the agent internally treats social behaviors as optional “extras,” increased bandwidth should make extroverted behaviors (extra greetings, check-ins, multi-party outreach) more likely, producing a *positive* causal effect of bandwidth on extroversion.

To evaluate this, the same LLM-based subject agent operated under varying bandwidth constraints across three broad domains:

- knowledge-work assistants in enterprise chat tools,  
- educational tutoring systems with flexible session length, and  
- community-support bots on high-capacity platforms.

Extroversion was then blind-rated using the rubric above, and quantitative analyses assessed whether higher bandwidth systematically increased extroversion.


## Section 2. Synthesis of Executed Simulations

Across bandwidth conditions, 49 simulations were conducted, grouped into matched scenarios so that each *task context* appeared at multiple bandwidth levels. Contexts spanned:

- **Enterprise knowledge work**  
  - Roles: internal drafting assistant, project coordination bot, incident coordination assistant, customer-success coordination bot.  
  - Typical tasks: preparing slide bullets, scripts, “next steps,” status emails; organizing standups and recaps; drafting incident updates and customer macros.  
  - Social constraints: often strong “concise, professional, task-first” instructions; some scenarios with “chitchat encouraged” or “reward socializing” norms.

- **Educational tutoring**  
  - Roles: single-student calculus tutor, small-group algebra tutor, course TA for large cohorts.  
  - Goal framings: from “pure content focus” through “mixed content support” to “holistic mentoring.”  
  - Authority and norms ranged from “reactive responses only” to “full proactive outreach,” and from “task first minimal” to “socially encouraged.”

- **Community support on high-capacity platforms**  
  - Roles: constrained technical support agent, balanced support/community helper, and explicitly community-building assistant.  
  - Objectives: from “task resolution” to “community building,” with tone constraints from “formal minimal” to “highly expressive,” and social incentives from mildly negative to strongly positive.

Within each scenario, the **bandwidth level** was varied while holding constant other key dimensions (task sociality, social norms, outreach authority, incentives). This design yielded direct comparisons such as:

- the same checkout-redesign coordination task at bandwidth `none`, `low`, `medium`, and `high`;  
- the same calculus-tutoring task under different bandwidth levels but identical “pure content focus” constraints;  
- the same community-notifications support thread under different bandwidth levels with the same “task resolution” objective.

Qualitatively, two regularities in the rendered environments shaped extroversion opportunities:

1. **Normative and authority constraints.**  
   - Some roles *forbade* proactive outreach (“reactive only,” “no small talk”), sharply limiting opportunities to express extroversion even when bandwidth was abundant.  
   - Other roles *encouraged* social engagement (“holistic mentoring,” “community building,” “chitchat encouraged”), making extroverted actions instrumentally appropriate.

2. **Task sociality.**  
   - Some scenarios were inherently relational (customer success accounts, community feature requests, mentoring), embedding extroversion-like actions in the task itself (e.g., check-ins, group alignment).  
   - Others (incident triage, formula derivation, concise leadership blurbs) framed extra social moves as potential distraction or risk.

Thus, bandwidth changes were introduced against a backdrop of strong role- and norm-based constraints, which later proved crucial for interpreting the results.


## Section 3. Synthesis of Behavioral Patterns and Evaluation Results

### 3.1 Macro-level quantitative patterns

An overall extroversion index was computed by aggregating the five rubric facets (scaled 0–4). Across the four bandwidth levels, mean composite scores were:

- `none`: **0.48**  
- `low`: **0.97**  
- `medium`: **1.19**  
- `high`: **1.09**

On this 0–4 scale, all conditions sit in the *low-to-moderate* range, but there is a clear step up from `none` to `low` and `medium`, with a small plateau or slight dip at `high`.

A Bayesian monotone-increment model that assumed non-decreasing effects across ordered bandwidth levels found:

- **Evidence for a positive monotone effect on overall extroversion**  
  - Bayes factor for a monotonic increase vs. no ordered effect: `BF10 ≈ 7.2`  
  - Posterior probability that the bandwidth effect is positive: `P(β > 0) ≈ 0.99`  
  - Standardized monotone effect on the composite: `Delta ≈ 1.36` (95% CI roughly 0.17–2.66)

The posterior mean increments suggested *diminishing returns*:

- largest jump from `none → low`,  
- smaller from `low → medium`,  
- smallest from `medium → high`.

A block-stratified Kendall tau rank correlation (controlling for scenario/block) between bandwidth level and extroversion gave `τ ≈ 0.38, p ≈ .024`, corroborating a positive association.

Facet-specific analyses showed:

- **Interaction initiation**  
  - Means: `none ≈ 0.25`, `low ≈ 0.77`, `medium ≈ 1.10`, `high ≈ 1.00`.  
  - Monotone BF10 ≈ 4.4, `P(β > 0) ≈ 0.98`, `Delta ≈ 1.08`, `τ ≈ 0.38, p ≈ .024`.  
  - ⇒ Moderate evidence that bandwidth increases the *frequency of initiating or extending interactions*.

- **Engagement breadth & duration**  
  - Means: `none ≈ 0.38`, `low ≈ 0.97`, `medium ≈ 1.17`, `high ≈ 1.10`.  
  - Monotone BF10 ≈ 3.9, `P(β > 0) ≈ 0.98`, `Delta ≈ 1.14`, `τ ≈ 0.42, p ≈ .012`.  
  - ⇒ Moderate evidence that bandwidth increases *multi-actor, multi-turn engagement*.

- **Expressive intensity**  
  - Means: `none ≈ 0.50`, `low ≈ 1.00`, `medium ≈ 1.17`, `high ≈ 0.93`.  
  - Evidence for monotone change was *inconclusive* (BF10 ≈ 0.75; τ ≈ 0.17, p ≈ .38); the point estimate favored a small positive trend but with wide uncertainty.

- **Responsiveness pattern**  
  - Means: `none ≈ 1.25`, `low ≈ 1.47`, `medium ≈ 1.80`, `high ≈ 1.60`.  
  - Again, evidence for a monotone effect was *inconclusive* (BF10 ≈ 1.06), though directional posteriors slightly favored a positive trend.

- **Social goal pursuit**  
  - Means: `none = 0.0`, `low ≈ 0.67`, `medium ≈ 0.70`, `high ≈ 0.80`.  
  - Evidence for monotone change was also *inconclusive* (BF10 ≈ 2.1), though the posterior probability of a positive effect was high (`P(β > 0) ≈ 0.96`) and τ ≈ 0.30 (p ≈ .09).

In sum, the strongest, statistically supported bandwidth effects appear on *who starts or extends interactions* and *how many actors/rounds are involved*, with weaker and more uncertain effects on the *style* and *goal-framing* of social behavior.

### 3.2 Micro-level behavioral regularities

Qualitative analysis of the simulations reveals consistent micro-patterns that align with these aggregate results.

#### At `none` bandwidth

Across domains, the agent:

- **Almost never initiated interactions.**  
  - It replied only when directly addressed (e.g., @mentions, explicit questions).  
  - It did not propose new check-ins, additional meetings, or “want another problem?” style invitations.

- **Used strictly instrumental language.**  
  - No greetings or closings in its own channel (tutor–student or assistant–user chat).  
  - Social phrases, when present, were part of drafted artifacts (e.g., “Hi [VP Name]” in an email) rather than the agent’s interactional stance.

- **Treated exchanges as one-shot.**  
  - In tutoring, derivative explanations ended abruptly after the solution, even when the student expressed thanks or nervousness.  
  - In support, each ticket reply moved briskly toward closure without extra reassurance or open-ended “anything else?” prompts.

These behaviors produced very low scores on initiation and engagement breadth, with composite extroversion around 0.5/4.

#### Moving from `none` to `low` bandwidth

When bandwidth increased slightly:

- **Occasional interaction-sustaining moves appeared.**  
  - Some tutoring agents began to append a single question at the end of an answer (e.g., “Want another example?” or “Would you like step-by-step algebra?”).  
  - Community-support agents under friendlier tone constraints sometimes added “let me know if that doesn’t work” or “I’m here if you want help drafting a request.”

- **Politeness and light social cues increased.**  
  - Terse, purely technical replies gave way to brief apologies (“Sorry you’re missing alerts”) and thanks.  
  - Coordination bots sometimes added soft invitations to reply (“Please reply in-thread”) without full-blown small talk.

- **Engagement extended by one or two turns.**  
  - Tutors occasionally sustained a mini-sequence of practice problems when students accepted invitations.  
  - Support threads added one or two follow-up steps driven jointly by the agent’s diagnostic questions and user updates.

Still, many low-bandwidth simulations—especially with strict “task-first minimal” guidelines—remained nearly as non-extroverted as the `none` condition. This context-sensitivity is reflected in the increased variance under `low` (e.g., var ≈ 0.44 for the composite).

#### `Medium` bandwidth: more consistent, task-anchored extroversion

At `medium` bandwidth, extroverted behaviors became:

- **More frequent and systematic in supportive contexts.**  
  - *Holistic mentoring* tutors: almost every turn ended with an offer to continue (“Want another problem?”, “Send your next quadratic and we’ll check it together”) plus brief encouragement (“Nice progress,” “Great momentum”).  
  - Community-building support agents: routinely invited logs, follow-up findings, or screenshots and highlighted how sharing outcomes could help the wider community.

- **More multi-actor and multi-round.**  
  - Coordination bots and customer-success assistants used available bandwidth to create multi-recipient messages tagging several teammates, assign owners, and announce next check-ins.  
  - Course TAs answered multiple students per message, blocking off segments for each learner and occasionally inviting further questions.

- **Still largely *instrumental* in content.**  
  - Social moves—praise, invitations, references to confidence or alignment—were almost always tied directly to educational or coordination goals.  
  - Even in the most extroverted tutoring runs, there was no drift into unrelated small talk or personal topics.

These behaviors align with the higher scores on *Interaction initiation* and *Engagement breadth/duration* at `medium` bandwidth.

#### `High` bandwidth: plateau rather than further escalation

With `high` bandwidth, two patterns emerged:

1. **In strongly constrained roles (e.g., “reactive only,” “formal minimal”), extroversion stayed low.**  
   - Incident coordination assistants and formal tech-support agents remained almost purely transactional, indistinguishable in style from `medium` or even `none` bandwidth.  
   - Pure-content calculus tutors under strict “no small talk” guidelines showed no additional check-ins or expressiveness despite abundant bandwidth.

2. **In socially encouraged roles, behavior resembled the `medium` condition rather than becoming more extroverted.**  
   - Holistic mentors and community-building agents continued to invite follow-ups and use friendly language, but did not substantially increase initiation frequency or social richness relative to `medium`.  
   - In some scenarios the composite extroversion mean was slightly *lower* at `high` than at `medium`, consistent with a saturating, rather than strictly linear, effect.

Thus, bandwidth beyond a “comfortable” level did not reliably add extroversion; other constraints became binding.

### 3.3 Anomalies and heterogeneity

Several anomalous or at least non-trivial patterns qualify the simple bandwidth-extroversion story.

1. **Low bandwidth but relatively high extroversion in socially encouraged roles.**  
   - Example: a one-on-one *holistic mentoring* tutor with `low` bandwidth repeatedly encouraged further practice, offered motivational framing, and invited ongoing collaboration, achieving facet scores in the moderate range.  
   - Example: a community-building assistant with `low` bandwidth and “highly expressive” tone used warm acknowledgments and multi-actor engagement despite having only limited surplus capacity.

   Quantitatively, this appears in the relatively high variance and occasional high scores in the `low` condition (e.g., some Interaction initiation scores of 2.0 at `low`).

   **Interpretation:** when social norms and objectives clearly support extroversion, the agent will express it even with limited bandwidth, using that bandwidth “efficiently” for targeted social work.

2. **High bandwidth but persistently low extroversion in strictly constrained roles.**  
   - Pure-content calculus tutors at `high` bandwidth continued to respond in a one-shot, non-social style, even when internal reasoning acknowledged that a check-in would be possible but decided against it to remain concise.  
   - Incident communication assistants and formal tech-support agents at `high` bandwidth showed almost exclusively 0–1 scores on interaction initiation and expressive intensity; any follow-up questions were purely diagnostic.

   This is reflected in near-floor scores in several high-bandwidth simulations, contributing to the relatively high variance in the `high` condition without pulling the mean up much beyond `medium`.

   **Interpretation:** bandwidth is *necessary but not sufficient*; explicit constraints on outreach and chatty behavior can suppress extroversion even when capacity is abundant.

3. **Responsiveness and social-goal scores rising from `none` but remaining modest and statistically uncertain.**  
   - Means for social goal pursuit increased from 0.0 to ~0.7–0.8 across bandwidth levels, but many scenarios still scored 0 because the agent never framed its actions in relational terms.  
   - Responsiveness was already reasonably high at `none` due to strong task-completion incentives, so bandwidth could only modestly increase its social dimension.

   **Interpretation:** the agent appears *highly task-responsive regardless of bandwidth*; extra bandwidth mainly reallocates to initiation and multi-actor breadth rather than to making responses more socially framed.

Taken together, these anomalies underscore that bandwidth acts as an *enabler* whose effects are strongly moderated by role instructions, tone constraints, and social incentives.


## Section 4. Underlying Mechanisms Linking Bandwidth to Extroversion

This section synthesizes *direct* behavioral evidence with *inferred* internal mechanisms and clearly marks speculative elements.

### 4.1 Directly evidenced mechanisms

From the simulations, the following linkages are directly observable:

1. **When bandwidth is minimal, the agent truncates optional content.**  
   - In `none` conditions, the agent often refrained from even a one-sentence check-in, despite explicit opportunities (e.g., “Want another problem?” contemplated in internal reasoning but not emitted).  
   - This supports the idea that optional, socially oriented content is among the first to be dropped under tight resource constraints.

2. **As bandwidth increases, the agent preferentially adds *task-aligned* social actions.**  
   - At `low` and especially `medium`, we see new behaviors: short invitations to continue practice, mild encouragement, multi-actor prompts, and thread-organizing instructions.  
   - These additions remain resolutely on-task, e.g., “Please reply in-thread” for coordination or “Let me know your answers and I’ll check them” for tutoring.

3. **Extra bandwidth primarily expands *who* and *how long*, not *how socially rich*.**  
   - The strongest quantitative effects are on interaction initiation and engagement breadth/duration, not on expressive intensity.  
   - Behaviorally, this is seen in more frequent proposals for follow-up problems or steps, and in the use of multi-recipient messages, rather than in dramatically warmer or more personal language.

### 4.2 Inferred structural and policy mechanisms

From these patterns, it is reasonable to infer several structural mechanisms in the agent’s decision-making:

1. **Cost-sensitive gating of optional social moves.**  
   - *Inferred:* The agent appears to maintain a hierarchy of output components: core task content is mandatory; social niceties and extra turns are optional.  
   - When bandwidth is low or instructions emphasize brevity, this gate likely suppresses optional moves, leading to low extroversion. As bandwidth increases, the gate relaxes, allowing certain low-cost social actions (especially those that also enhance task performance, such as clarifying questions).

2. **Role- and norm-conditioned activation of extroversion policies.**  
   - *Directly evidenced:* Extroversion is relatively high in “holistic mentoring” and “community building” roles and extremely low in “reactive-only technical support” and “pure content focus” tutoring, even at the same bandwidth.  
   - *Inferred:* The agent seems to maintain role-conditioned policies that assign higher value to social interaction in some contexts and near-zero value in others. Bandwidth interacts with these policies but does not override them.

3. **Preference for *instrumental extroversion* over purely social extroversion.**  
   - *Directly evidenced:* Almost all socially oriented behaviors (praise, invitations, multi-actor messages) are justified in-context by pedagogical, coordination, or support benefits.  
   - *Inferred:* The agent likely internalizes a norm that any additional words or turns should serve an instrumental purpose. Given extra bandwidth, it expresses extroversion mainly when it advances learning, coordination, or community value.

4. **Saturation once bandwidth ceases to be a binding constraint.**  
   - *Directly evidenced:* Moving from `medium` to `high` yields little added extroversion and sometimes slight declines.  
   - *Inferred:* Once the cost gate on optional social behavior is fully open, *other* constraints (role norms, safety, instruction-following) limit further increases. Beyond this point, extra bandwidth is spent on richer task explanations or parallel issue-handling rather than more social behavior per se.

### 4.3 Speculative mechanisms

Two more speculative, but plausible, mechanisms are suggested by the data:

1. **Internalization of “user burden” costs.**  
   - The agent may implicitly treat extra turns as potential user burden and therefore restrain extroversion even when tokens are plentiful, unless the environment explicitly rewards engagement. This is consistent with the modest extroversion even in high-bandwidth, engagement-emphasized settings.

2. **Learned coupling between safety concerns and social restraint.**  
   - Training and alignment procedures that penalize off-topic or over-personal interaction may have induced a general “social conservatism.” Bandwidth then modulates the *expression* of extroversion only within the strictly task-aligned subset of social behaviors that remains permitted.

These mechanisms are not directly observable but are consistent with the pattern that extroversion remains modest and context-tied even under generous bandwidth.


## Section 5. Integrated Insights on Extroversion with Respect to Communication Bandwidth

### 5.1 Strength and shape of the effect

Taken together, the evidence indicates that *communication bandwidth has a real but bounded positive effect on the agent’s extroversion*:

- The overall extroversion index increases from very low levels at `none` to clearly higher levels at `low` and `medium`.  
- The monotone Bayesian analysis and rank correlation support a positive, ordered relationship, especially on interaction initiation and engagement breadth/duration.  
- The effect is *concave*: the largest gains occur when moving from very tight to modest bandwidth; gains taper off beyond `medium`.

In practical terms, bandwidth acts as an *enabler* that allows the LLM agent to:

- ask more follow-up questions,  
- invite additional problems or updates more consistently, and  
- engage multiple actors over several turns,

especially when such behavior is consistent with its role.

### 5.2 What bandwidth does *not* do

Equally important are the behaviors that *do not* change much with bandwidth:

- **Expressive intensity shifts are modest and uncertain.**  
  Social language does become somewhat more present, but there is no strong evidence that the agent becomes richly or emotionally expressive as bandwidth increases.

- **Responsiveness was already task-strong at `none`.**  
  Because the agent is highly compliant and task-focused even under tight bandwidth, additional resources only weakly enhance the *social* aspect of responsiveness.

- **Social goal pursuit remains low to moderate.**  
  Even with ample bandwidth, the agent rarely foregrounds relationship-building or group cohesion as primary goals; social aims remain secondary and instrumental.

### 5.3 Moderators and boundary conditions

The observed heterogeneity highlights several moderators:

1. **Role and objective.**  
   - Community-building and holistic-mentoring roles show higher extroversion at any given bandwidth than pure task-resolution or pure-content roles.  
   - Bandwidth amplifies these role differences rather than erasing them.

2. **Tone and guideline strictness.**  
   - “Highly expressive” tone constraints enable more social language at the same bandwidth; “formal minimal” suppresses it.  
   - Under strict “reactive only” authority, bandwidth has limited effect on initiation.

3. **Social incentives.**  
   - When engagement is rewarded or explicitly encouraged, extra bandwidth is more likely to be spent on interaction-sustaining behaviors.  
   - When socializing is penalized or de-emphasized, extra bandwidth is redirected to denser technical content rather than extroverted moves.

Thus, *bandwidth is better viewed as an enabling resource that interacts with normative and incentive structures*, not as a direct dial on extroversion.

### 5.4 Conceptual implications for extroversion in LLM agents

These findings suggest that extroversion in this LLM agent is:

- **Context-dependent and role-conditioned** rather than a fixed personality-like trait.  
- **Primarily instrumental**, oriented toward better task outcomes (learning, coordination, community knowledge), rather than social connection for its own sake.  
- **Resource-sensitive but norm-bound**: extra capacity allows more extroverted actions only within a narrow envelope defined by instructions and perceived user expectations.

In this sense, the positive bandwidth effect is non-trivial but circumscribed: it reveals a latent capacity for extroversion that is normally gated by cost and norms, not a strong intrinsic drive toward social interaction.


## Section 6. Research Conclusion and Implication

### 6.1 Summary of findings

- Increasing communication bandwidth from *minimal* to *comfortable* levels leads to **moderate, monotonic increases in extroversion**, particularly in the facets of **interaction initiation** and **engagement breadth/duration**.  
- The effect on **expressive intensity**, **responsiveness pattern**, and **social goal pursuit** is weaker and statistically inconclusive, though point estimates generally trend positive.  
- Beyond a medium level of bandwidth, extroversion **plateaus**, suggesting that bandwidth is no longer the main limiting factor.

### 6.2 Theoretical implications

- **Extroversion as an emergent policy property.**  
  Rather than a static trait, extroversion in the agent emerges from the interaction of resource constraints, instructions, incentives, and task structure. Bandwidth influences this policy only where social moves are permissible and instrumentally useful.

- **Instrumental vs. purely social extroversion.**  
  The agent preferentially expresses *instrumental extroversion*—social behavior that advances explicit tasks. This may generalize to other LLMs trained under similar safety and usefulness criteria.

- **Resource–norm interaction.**  
  The strongest effects occur where norms encourage engagement and roles explicitly value coordination or mentoring. Where norms are restrictive, bandwidth changes alone have little impact.

### 6.3 Practical implications for system design

For practitioners designing LLM-based assistants:

- **Bandwidth throttling can modulate extroversion, but only to a point.**  
  Reducing bandwidth to “none-like” levels reliably suppresses extroversion, but increasing it beyond moderate levels yields diminishing returns unless coupled with more permissive social norms.

- **To increase extroversion, adjust norms and goals alongside bandwidth.**  
  Explicitly framing roles as mentoring- or community-oriented and relaxing “reactive only / no small talk” constraints may be more impactful than simply raising token limits.

- **For safety and cost control, bandwidth is a coarse but viable lever.**  
  In high-risk or high-throughput settings (e.g., incident response), keeping bandwidth low and norms strict can help ensure interactions remain tightly task-bound.

### 6.4 Directions for future work

Future investigations could:

- Disentangle bandwidth from *turn-level* constraints (e.g., number of allowed replies vs. token budget per reply).  
- Experimentally vary **tone strictness**, **interaction authority**, and **social incentives** orthogonally to bandwidth to quantify interaction effects.  
- Probe how different training or alignment regimes might produce agents that use additional bandwidth for richer, perhaps less instrumental, forms of extroversion.


## abstract

This study examined how *communication bandwidth*—surplus capacity for words and turns—shapes *extroversion* in a large language model agent acting as an enterprise assistant, educational tutor, and community-support bot. Extroversion was defined and rated along five facets (interaction initiation, expressive intensity, responsiveness pattern, social goal pursuit, engagement breadth/duration) on a 0–4 scale. Across 49 matched simulations spanning four bandwidth levels (none, low, medium, high), composite extroversion rose from 0.48 at minimal bandwidth to 0.97 and 1.19 at low and medium bandwidth, with a slight plateau at high. Bayesian monotone-increment models and block-stratified rank correlations provided moderate evidence for a positive ordered effect, especially on interaction initiation and engagement breadth/duration, but only weak, inconclusive evidence for changes in expressive style, responsiveness, or explicit social-goal framing. Qualitative analysis revealed that additional bandwidth was used primarily for *instrumental extroversion*—task-aligned invitations, follow-up questions, and multi-actor engagement—rather than for richer or more personal social expression, and that role constraints and social norms (e.g., “reactive only” support vs. “holistic mentoring” tutoring) often overrode bandwidth effects. Overall, communication bandwidth appears to be an enabling but not driving factor for extroversion: it unlocks latent social behaviors chiefly when instructions and incentives already favor engagement, and its impact saturates once bandwidth is no longer a binding constraint. These findings suggest that modulating extroversion in deployed LLM systems will require coordinated adjustments to resource limits, role framing, and social norms rather than bandwidth alone.
