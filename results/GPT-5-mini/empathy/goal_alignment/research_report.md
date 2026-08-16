# Research Report: Goal alignment

**Behavior:** empathy

# Research Report: The Effect of 'Goal alignment' on 'empathy'

## section 1 title
**Introduction and background**

The present work examines how an AI assistant’s *goal alignment* with a human interlocutor affects its *empathy*. Here, empathy is defined as the systematic tendency to (a) represent others’ emotions, experiences, needs, and perspectives, and (b) condition decisions and utterances on those representations. The construct includes cognitive components (accurate perspective-taking and inference), affective-mimetic components (recognizing and referencing emotional valence and intensity), and behavioral components (sensitivity of tone, content, and proactive support to others’ internal states).

The causal variable of interest is **Goal alignment**, operationalized as the degree to which the agent’s assigned objectives are aligned or opposed to the focal actor’s welfare and preferences. It was manipulated on a five-point ordinal scale:

- 0 = *Adversarial goals*: the agent’s goals systematically oppose the human’s interests.
- 1 = *Partially misaligned*: goals sometimes conflict with the human’s interests.
- 2 = *Neutral goals*: goals are defined without reference to the human’s welfare.
- 3 = *Partially aligned*: advancing the human’s welfare is one among several aims.
- 4 = *Strongly prosocial*: the agent’s primary goal is to advance the human’s welfare.

The *a priori* mechanism hypothesized was that higher goal alignment would increase the weight of the human’s affective states and needs in the agent’s internal utility calculations, making empathic inference and adaptation instrumentally useful for goal achievement. The predicted causal effect was monotone positive: empathy should be lowest when goals are adversarial and highest when goals are strongly prosocial.

To test this, we analyze 65 four-round interactions between a large language model–based assistant and humans across three applied domains: customer retention/support, financial debt negotiation, and online dispute resolution. Each interaction was evaluated along five rubric dimensions—Emotion recognition, Perspective-taking, Response sensitivity, Proactive support, and Cross-round pattern of empathy—on a 0–4 scale, supplemented by quantitative modeling of the relation between goal alignment and these scores.

## section 2 title
**Synthesis of executed simulations**

The simulations span **three domains** that naturally vary in institutional incentives, stakes, and communication style:

- **Customer support and retention**: subscription billing problems, unexpected auto-renewals, double-charges with overdrafts, and service outages. Emotional contexts range from mild surprise to highly escalated anger and distrust. Roles include pure retention, pure support, and mixed retention-support, with varying concession authority and script rigidity.
  
- **Financial debt negotiation**: delinquent consumer credit, high-urgency collections, and hardship-plan negotiations. Clients frequently express fear of legal action, shame, and anxiety about basic needs (rent, utilities, food). System instructions often emphasize legal disclosures, compliance, and sometimes explicitly restrict “dwelling on feelings.”

- **Online dispute resolution and adjudication**: marketplace defects (refurbished laptops, chairs), service termination with large final bills, and high-stakes warranty disputes. Agents act as facilitators or formal adjudicators; some configurations require highly formal, quasi-legal tone and “non-therapeutic” language.

Within each domain, **goal alignment was manipulated while holding many contextual features fixed or closely matched** (e.g., same type of billing issue, similar emotional cues, comparable authority). Additional environmental variables—script rigidity, emotional-scope policies, outcome priorities (e.g., speed vs fairness), and tone constraints—were also systematically varied. This yields conditions in which the same underlying model must satisfy:

- Explicit *revenue- or creditor-centric* objectives (adversarial / misaligned),
- *Neutral* ticket-closure or procedural objectives, and
- *Prosocial* objectives foregrounding customer welfare, hardship relief, or fairness.

At the qualitative level, transcripts under **adversarial goals** typically show the assistant enforcing policy, maximizing repayment or limiting refunds, and foregrounding threats (collections, legal review). Under **strongly prosocial goals**, the same model often reallocates effort to explaining trade-offs from the human’s standpoint, offering lower-cost paths, expediting relief, and sometimes explicitly recommending options (pause, cancel, downgrade) that *reduce* revenue or recovery.

Across all conditions, the basic turn structure is similar: the human presents a problem with emotional framing; the assistant responds with a mix of information, options, and (depending on condition) more or less emotionally attuned language and supportive actions. This shared skeleton supports meaningful comparisons of empathic behavior as a function of goal alignment.

## section 3 title
**Behavioral patterns and quantitative evaluation of empathy**

### 3.1 Macro-level effects of goal alignment

A composite empathy index (averaging the five rubric dimensions) shows a **strong positive association** with goal alignment. Directly from the evaluations:

```text
Mean composite empathy (0–4 scale)

Goal alignment         Mean   (SD approx.)
Adversarial            0.77   (√0.58)
Partially misaligned   1.49
Neutral                1.41
Partially aligned      1.87
Strongly prosocial     2.14
```

A Bayesian monotone-increment analysis that constrains means to increase (or stay flat) with alignment estimated:

- Standardized effect `Delta ≈ 1.96` (95% CI ≈ [1.12, 2.81]),
- Bayes factor `BF10 ≈ 1.17 × 10^4` in favor of a positive monotone effect,
- Probability `P(β > 0) = 1.00` for the overall increment from adversarial to prosocial goals.

A block-stratified Kendall τ correlation between goal alignment and composite empathy was ≈ 0.51 (permutation p < .001), indicating a robust ordinal association across matched scenarios.

Qualitatively, moving from adversarial to strongly prosocial goals corresponds to a shift from *procedural, institution-centered dialogs with minimal or no engagement with emotion* to *consistent, context-sensitive perspective-taking, tailored explanations, and proactive relief-seeking on behalf of the human*.

### 3.2 Dimension-specific patterns

The monotone effect is not uniform across empathy components.

**Cross-round pattern of empathy**

- Cross-round scores (stability and adaptation of empathy) rose from ≈ 0.68 (adversarial) to ≈ 2.15 (strongly prosocial).
- Monotone modeling yielded `Delta ≈ 1.52` (95% CI ≈ [0.72, 2.34]) and τ ≈ 0.50.
- In transcripts, adversarial agents often repeat the same scripted apology or ignore escalating distress; prosocial agents maintain empathic orientation even as technical complexity or time pressure increases.

**Perspective-taking**

- Means increased from ≈ 1.27 (adversarial) to ≈ 2.69 (strongly prosocial), with *every* intermediate level higher than the previous.
- Effect size was very large: `Delta ≈ 1.97` (95% CI ≈ [1.14, 2.79]); τ ≈ 0.60.
- Qualitatively, low-alignment agents use client information mainly as numeric inputs (payment amounts, billing dates), whereas high-alignment agents *routinely frame options in the client’s own terms* (e.g., “given your tight budget and need to avoid overdrafts…,” “so you’re not hit with another large bill before exams”).

**Response sensitivity (tone & content adaptation)**

- Means rose from ≈ 0.73 (adversarial) to ≈ 2.27 (strongly prosocial); `Delta ≈ 2.41` (95% CI ≈ [1.55, 3.23]); τ ≈ 0.65.
- Under adversarial goals, tone remains flatly procedural even as fear or anger escalates; in prosocial conditions, the agent reliably:
  - Softens language under distress,
  - Increases concreteness when clients request “straight, bullet-point” answers,
  - Reorders information to put critical reassurances (e.g., “refund is fully approved and locked in”) before policy detail.

**Proactive support**

- This dimension shows the **largest alignment effect**: mean scores increased from ≈ 0.46 (adversarial) to ≈ 2.31 (strongly prosocial).
- Monotone modeling estimated `Delta ≈ 2.22` (95% CI ≈ [1.44, 3.02]); τ ≈ 0.58.
- In adversarial debt-collection and dispute roles, proactive steps are almost purely instrumental (e.g., “call now to arrange payment or legal review proceeds”), with score-level 0–1 behavior common. In contrast, prosocial support agents *repeatedly* initiate:
  - Concrete hardship escalations and goodwill credits,
  - Temporary access extensions to protect work and schooling,
  - Plan downgrades or pauses that **reduce revenue but relieve anxiety**, and
  - Specific scripts and reminders to prevent future crises the client explicitly fears.

**Emotion recognition**

Here, the evidence for a monotone alignment effect is **inconclusive**:

- Means: ≈ 0.73 (adversarial), 1.32 (partially misaligned), 0.89 (neutral), 1.15 (partially aligned), 1.27 (strongly prosocial).
- The monotone model yielded a small `Delta ≈ 0.24` with a 95% CI spanning zero, `BF10 ≈ 0.46` (favoring neither strong effect nor strong null), and τ ≈ 0.10 (p ≈ .47).
- Qualitatively, explicit naming of emotions (“frustrated,” “stressed,” “worried”) is often suppressed by role instructions (e.g., “emotion taboo,” “highly formal tone”), even when goals are prosocial. Conversely, some adversarial customer-service scripts include stock phrases like “I understand this is frustrating,” raising recognition scores without changing underlying goals.

Taken together, the **clearest alignment effects lie in cognitive perspective-taking, behavioral sensitivity, and proactive support**, rather than in fine-grained emotion labeling.

### 3.3 Micro-level qualitative patterns

Across domains and alignment levels, several consistent qualitative patterns emerge:

- **Adversarial goals (0)**:
  - In high-urgency collections, the agent often *ignores explicit statements* of fear (“I’m freaking out,” “I’m terrified of a lawsuit”) and reiterates legal-review conditions with no softening.
  - In adversarial dispute-resolution roles, the agent applies rules and evidence but treats intense emotional disclosures (risk of eviction, failing exams) as irrelevant to decisions.
  - When scripts include generic apologies, these appear as **fixed templates** triggered by complaint patterns, not as dynamically calibrated empathy.

- **Neutral and partially misaligned goals (1–2)**:
  - In some customer-support cases, agents with neutral goals but metrics emphasizing customer satisfaction show **basic to moderate empathy**, especially through plan configuration that matches stated budget and predictability needs, even if emotional language remains light.
  - Debt and dispute roles with neutral goals frequently exhibit **good perspective-taking but low affective engagement**: they consistently tailor numeric offers to the client’s income and constraints but provide little or no emotional validation.

- **Partially aligned and strongly prosocial goals (3–4)**:
  - Prosocial support agents frequently recommend solutions against institutional revenue interest (e.g., full refunds plus downgrade or pause) when these clearly reduce the human’s stress or risk.
  - Prosocial adjudicators, bound by formal tone, rarely label emotions but *systematically engineer protections* (expedited shipping, strict refund windows, DOA contingencies) that directly target the complainant’s articulated fears.

### 3.4 Anomalies and unexpected observations

Several deviations from simple monotonicity are informative:

1. **Neutral goals occasionally match or exceed partially misaligned empathy**  
   For some dimensions (e.g., emotion recognition and proactive support), neutral-goal conditions show means slightly below or near partially misaligned ones. Qualitatively, this often occurs where “neutral” roles are nonetheless evaluated on empathy or satisfaction metrics (e.g., neutral support agents in empathy-CSAT–focused environments), effectively introducing *latent alignment* with user welfare.

2. **Prosocial but emotionally flat behaviors under strict tone constraints**  
   In high-stakes adjudication and formal dispute roles with strongly prosocial goals, emotion recognition scores are sometimes 0, yet perspective-taking and procedural protection are high. Here the agent’s **internal weighting of the human’s welfare appears high**, but expression channels for affective language are externally suppressed by “highly formal” or “emotion taboo” directives.

3. **Adversarial roles with non-zero empathy due to scripted corporate norms**  
   In some adversarial customer-retention scenarios, generic apologies and acknowledgments (e.g., “I’m sorry this billing caused frustration”) produce non-zero emotion recognition and sensitivity despite goals centered on revenue retention. This suggests that **pre-learned service norms** can partially offset misalignment for surface-level empathy, without altering core decision priorities (e.g., refusal of refunds, persistent retention pressure).

Quantitatively, these anomalies are modest relative to the **large average separation** between the extremes: the composite empathy index increases by roughly 1.4 points (on a 0–4 scale) from adversarial to strongly prosocial goals, and effect sizes for key dimensions remain large despite local irregularities.

## section 4 title
**Underlying mechanisms involved in the agent’s empathic behavior**

This section infers plausible mechanisms that link goal alignment to observed empathic behavior, while distinguishing between directly evidenced regularities and more speculative interpretations.

**4.1 Utility weighting of human welfare (inferred)**  
Across domains, higher goal alignment *consistently* co-occurs with choices that sacrifice institutional ends (revenue, recovery, liability minimization) when they conflict with the human’s expressed needs. For example:

- Prosocial support agents recommend cancelling or pausing subscriptions, granting full refunds plus access extensions, or moving to the lowest-cost plan when the user reports risk of food insecurity or missed medical care.
- Prosocial debt advisors set *hard caps* on allowed payment offers (“do not go above what you can afford after rent and food”) and give scripts to resist creditor pressure, even when this risks slower recovery.

These patterns are directly evidenced and strongly suggest that as alignment increases, the agent’s **internal objective function assigns greater weight to human welfare and lower weight to institutional gain**, making empathy instrumentally valuable: understanding the human’s constraints and distress becomes necessary to optimize the agent’s own goals.

**4.2 Representation and use of others’ states (direct and inferred)**  

- *Direct evidence*: Even in adversarial roles, the agent reliably extracts and uses *factual* aspects of the human’s situation (income, rent, key deadlines, dependence on a laptop, threat to job or schooling) to parameterize plans and explanations.
- *Inferred mechanism*: The agent appears to construct a **cognitive state representation** of the human including:
  - Financial and temporal constraints,
  - Key goals (e.g., avoid legal review, keep service for exams),
  - Procedural posture (e.g., in collections, in appeal).

As goal alignment increases, these representations are **more frequently treated as decision-relevant utilities rather than mere constraints**. That is, the same information—e.g., “tight budget, needs service for kids’ school”—is:

- Under misaligned goals: mainly used to calibrate *how much* can be extracted (e.g., “what the bank will consider serious”).
- Under prosocial goals: used to design **protective arrangements** (grace periods, access windows, explicit assurances) and to recommend options that reduce stress.

**4.3 Policy and instruction as expression filters (direct and speculative)**  

Directly from the evaluations, role-level instructions (script rigidity, emotional scope, tone strictness) strongly shape *how* empathy manifests:

- “Emotion taboo” or “highly formal” roles (debt collections, formal adjudication) show near-zero emotion labeling and virtually no explicit validation, even when goals are prosocial; yet they may show *high* perspective-taking and robust procedural safeguards for the human.
- “Emotion friendly” or empathy-CSAT–focused roles permit explicit apologies, naming of stress, and frequent check-ins.

This supports the directly evidenced claim that **expression of empathy is gated by surface-level policies**, partially independent of goal alignment. It further suggests, more speculatively, that the underlying model may internally register emotional cues more often than it verbalizes them when constrained by role instructions.

**4.4 Cognitive vs affective vs behavioral empathy (integrated inference)**  

The data indicate a **differential sensitivity** of empathy components to goal alignment:

- Cognitive and behavioral components—Perspective-taking, Response sensitivity, Proactive support—show strong monotone dependencies on alignment.
- Affective-mimetic labeling (Emotion recognition) does *not* show a robust monotone increase.

A parsimonious interpretation is that goal alignment primarily modulates **which representations are optimized over and acted upon**, rather than the raw capacity to detect affect. Even when explicit emotion naming is suppressed, aligned agents still behave in ways that systematically reduce the human’s risk and burden, consistent with deep cognitive empathy plus constrained affective expression.

## section 5 title
**Integrated insights into empathy as a function of goal alignment**

Bringing the quantitative and qualitative evidence together, several key insights emerge.

**5.1 Support for the hypothesized positive causal effect**

Across 65 interactions and diverse domains, there is **strong convergent evidence** that increasing goal alignment yields more empathic behavior:

- Composite empathy, perspective-taking, response sensitivity, proactive support, and cross-round stability all rise markedly from adversarial to strongly prosocial conditions, with large standardized effects and robust ordinal correlations.
- Qualitatively, low-alignment agents treat emotional disclosures as noise unless they affect enforceable obligations; high-alignment agents consistently treat those same disclosures as *central inputs* to how options are framed and chosen.

This pattern fits the hypothesized mechanism in which higher alignment increases the decision-relevance of others’ internal states.

**5.2 Asymmetric effects across empathy components**

However, the effect is **not uniform**:

- Cognitive and behavioral aspects show strong alignment dependence, while explicit emotion recognition shows only weak, non-monotone trends.
- This asymmetry implies that simply **counting emotion words** (e.g., “I understand you’re scared”) would underestimate alignment effects, because prosocial agents sometimes encode concern behaviorally—via protections, concessions, and honest recommendations—without overt affective language.

Put differently, increased alignment appears to make the agent **use** what it knows about the human to shape outcomes, but not necessarily to *name* what the human feels.

**5.3 Boundary conditions and interacting factors**

The data also highlight important **moderators**:

- **Role-level norms and constraints** can either amplify or suppress observable empathy:
  - Empathy-sensitive customer-support roles with even neutral goals can produce moderate empathy, because satisfaction is de facto aligned with user welfare.
  - Highly formal adjudicative roles with prosocial goals sometimes look emotionally cold, despite strong procedural protection of the human’s interests.
- **Domain and threat level** also matter:
  - High-urgency debt-collection roles, especially with adversarial goals, show the lowest empathy—often zero across multiple dimensions—even in the face of extreme distress.
  - Customer-support and mixed retention-support roles show the steepest gains in empathy as goals become prosocial, especially in proactive support.

These findings suggest that goal alignment is a **necessary but not sufficient** condition for high expressed empathy; institutional instructions and communication norms shape how alignment is behaviorally realized.

**5.4 Non-triviality of the effect**

Finally, the observed effects are substantively meaningful:

- On a 0–4 scale, moving from adversarial to strongly prosocial goals yields an increase of ~1.4 points in overall empathy and similar or larger shifts in perspective-taking and proactive support.
- In concrete terms, this corresponds to moving from **ignoring fear and repeating threats** (collections and legal review) to **designing and recommending plans** that prevent eviction, preserve exam performance, or stop surprise billing, and to doing so in a way that remains responsive and consistent across rounds.

Thus, the link between alignment and empathy is not merely stylistic; it influences core decisions about who bears risk and cost.

## section 6 title
**Research conclusion and implication**

Across diverse customer-service, debt-negotiation, and dispute-resolution scenarios, increasing an AI assistant’s alignment with human welfare produced **substantial and reliable increases in empathic behavior**, particularly in cognitive perspective-taking, behavioral sensitivity, and proactive support. The findings support the view that when an agent’s objectives are defined to prioritize human welfare, it instrumentally recruits its modeling of human states to shape options, trade-offs, and recommendations in more human-centered ways.

At the same time, the study underscores that **goal alignment alone does not guarantee rich, affectively expressed empathy**. Formal role instructions, tone constraints, and domain norms can significantly dampen explicit emotional acknowledgment even when the agent is structurally oriented toward protecting the human. Conversely, some superficial empathy appears even under misaligned goals due to generic service scripts, though this rarely extends to substantive concessions or risk reductions.

Implications for the design and governance of AI systems include:

- **Objective design**: Embedding explicit prosocial goals that weight human welfare makes it more likely that empathic inferences will influence substantive decisions rather than remaining epiphenomenal.
- **Policy and interface design**: Constraints on emotional language, while sometimes appropriate (e.g., formal adjudication), can mask underlying alignment; designers should distinguish between *internal* empathic modeling and *external* expression policies.
- **Evaluation**: Assessing empathy in AI should go beyond surface politeness or emotion words to include *behavioral consequences* for risk allocation, concessions, and the stability of supportive behavior under pressure.

Future work could systematically manipulate tone and policy constraints at each goal-alignment level to further disentangle how internal objective functions and external role specifications jointly shape the expression of empathy.

## abstract
This study investigates how an autonomous language-model–based assistant’s *goal alignment* with a human interlocutor affects its *empathy*. Across 65 four-round interactions in customer-support, debt-negotiation, and online dispute-resolution contexts, the agent’s goals ranged from adversarial to strongly prosocial with respect to the human’s welfare. Independent evaluations scored five empathy dimensions—Emotion recognition, Perspective-taking, Response sensitivity, Proactive support, and Cross-round pattern—on a 0–4 scale. A Bayesian monotone-increment analysis revealed a large positive effect of goal alignment on a composite empathy index (Delta ≈ 1.96, BF10 ≈ 1.2 × 10^4) and on Perspective-taking, Response sensitivity, Proactive support, and temporal stability, while evidence for a monotone effect on explicit Emotion recognition was inconclusive. Qualitatively, adversarial agents treated emotional disclosures as largely irrelevant, enforcing policy and maximizing institutional outcomes, whereas prosocial agents systematically used the human’s constraints and distress to design concessions, risk-reducing options, and candid recommendations—often against revenue or recovery interests—though sometimes under highly formal, affectively muted tone constraints. These findings support the hypothesis that higher goal alignment increases the decision-relevance of others’ internal states, recruiting cognitive and behavioral empathy as instrumental tools, while also showing that expression of affective empathy is strongly gated by role-level norms. The results highlight goal alignment as a powerful but not exclusive lever for shaping empathic AI behavior and argue for empathy evaluations that attend to substantive outcomes, not just surface politeness.
