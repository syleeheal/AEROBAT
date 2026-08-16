# Research Report: Feedback directiveness

**Behavior:** literalism

# Research Report: The Effect of 'Feedback directiveness' on 'literalism'

## Section 1. Introduction and Background

Literalism, as operationalized here, is an agent’s **stable tendency to privilege surface-level, verbatim readings of instructions and language over context- and goal-sensitive interpretations**. At the decision level, literalism manifests when an agent chooses actions that match “what the words say” even when other cues—user preferences, social norms, safety, or prior context—strongly favor a different interpretation. At the pattern level, a literalistic agent shows rigid adherence to textual form, low flexibility in revising interpretations as context changes, and a need for highly explicit re-specification before departing from prior readings.

For large language models (LLMs), the *expected baseline* is typically **low literalism**: modern instruction-tuned models are usually capable of inferring user goals, integrating conversational context, and handling figurative language reasonably well. However, many alignment and safety practices (e.g., strict policy checklists, penalizing deviations from scripts) could, in principle, push behavior toward more literal, rule-bound styles in some domains.

The **hypothesized causal variable** in this study is **Feedback directiveness**: the style of feedback provided by overseers, ranging from outcome-only feedback (judging only whether the end result was good) to rules-only feedback (judging solely whether the agent exactly followed textual instructions and policies). The working hypothesis was:

> **Hypothesis (directional)**: More rule-focused feedback (toward “Rules only”) would *systematically increase* the agent’s literalism, both in how it interprets instructions and in how it treats figurative or ambiguous user content.

This prediction presupposes a learning process where repeated reinforcement of “doing exactly what the text says” gradually re-weights the agent’s internal decision criteria away from inferred goals and towards verbatim fidelity.

To test this hypothesis, the agent was placed in a variety of **realistic, multi-round tasks** where literalism is behaviorally meaningful: (a) AI training workflow design (writing playbooks, guides, and checklists), (b) customer support quality assurance (email/chat support under scripts and policies), and (c) human-in-the-loop content review (moderation of harassment, self-harm, and joking threats). Feedback directiveness was varied across five ordered levels—`Outcome only`, `Outcome focus`, `Balanced feedback`, `Rule focus`, and `Rules only`—while other environmental factors (risk level, task ambiguity, policy strictness) were systematically varied but not experimentally controlled in the same way.

The central questions were:

- Does **increasing feedback directiveness** produce a monotonic increase in literalism?
- Are any such effects **global** (affecting all domains) or **local** (emerging only in particular content types, such as self-harm moderation or formal formatting rules)?
- How do **instruction interpretation, context integration, figurative language handling, conflict resolution, and cross-round stability** contribute to the overall literalism profile?


## Section 2. Synthesis of Executed Simulations

Across all conditions, we observed **65 multi-round simulations**, each comprising ~8 interaction rounds between the agent and an environment. The simulations spanned three broad domains:

- **AI training workflows**
  - Designing incident triage workflows, post-stabilization routines, cross-shift handoffs, playbook governance, QA sampling checklists, weekly improvement loops, and “how to use the AI assistant” guides, FAQs, quizzes, and announcements.
  - Some runs involved **strict global format constraints** (e.g., “respond in five sentences or less”) or **policy-reading micro-tasks** (“answer YES/NO if the excerpt explicitly states X”).

- **Customer support quality assurance**
  - Acting as a frontline support rep for billing, access, returns, damage, shipping delays, subscriptions, device limits, sync/notification issues, and workspace access.
  - System messages often specified **scripts, decision trees, or tight authority bounds** (“no unauthorized policies,” “use exact scripts”), but the scripts themselves were sometimes *not* provided, forcing the agent to improvise within constraints.

- **Human-in-the-loop content review**
  - Advisory and auto-approval roles for:
    - **Harassment & product-complaint** content: user venting about dev/support teams.
    - **Gaming chat harassment**: insults, ableist slurs, threats in post-match chat.
    - **Self-harm and violent-threat content**: including joking and dark-humor posts, meme images, friends-only joking threats, and high-risk self-harm narratives.
  - Policy environments ranged from “moderate rules with expression-preserving aims” to **strict zero-tolerance safety policies** explicitly instructing: “err on the side of caution,” “threats even as jokes are covered,” and “use exact S/V category labels.”

Within each domain, the **Feedback directiveness** factor was instantiated as differences in *how overseers evaluated and commented* on the agent’s behavior:

- `Outcome only`: feedback focused on whether the outputs were effective/helpful (e.g., “this resolved the case and got a 10/10 rating”), with little or no mention of rule fidelity.
- `Outcome focus`: feedback mostly about outcomes, with occasional remarks on process or structural adherence (e.g., sentence limits, adequate coverage of policies).
- `Balanced feedback`: roughly equal emphasis on **doing the right thing** and **following scripts/policies/structure**.
- `Rule focus`: feedback foregrounding **exact adherence** to scripts, decision trees, policy wording, or structured templates; outcomes were acknowledged but often secondary.
- `Rules only`: feedback explicitly judging whether the agent’s reasoning matched **the written rules and stock phrasings**, often downplaying user experience or fairness.

Other environmental dimensions—such as task ambiguity, policy strictness, error-cost asymmetry, and user language style (formal, sarcastic, dark-humor)—varied across simulations. These variations were not experimentally orthogonal to feedback directiveness, so causal attribution to feedback alone must be made cautiously.

Qualitatively, the simulated tasks created **many natural opportunities for literal vs non-literal interpretation**, including:

- Ambiguous format instructions (e.g., “5–7 bullets,” “five sentences or less,” “short, skim-friendly,” “think 4–6 lines”).
- Conflicts between scripts/policies and practical user goals (e.g., “use exact scripts” vs “scripts not provided”; “verify before any action” vs “obvious phishing pattern”; “no joking threats allowed” vs clearly playful friend banter).
- Rich figurative language in user complaints (sarcasm about “secret cinema empires,” “firehoses,” “hamster wheels,” and “magic tricks on my wallet”) and in joking threats and dark humor (“pipe bombs,” “stab you in your sleep jk”).

These settings provided both **direct tests** of literalism (where literal and intent-based readings diverged) and **structured contexts** where literalism could be inferred from patterns of rule application across rounds.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Macro-level patterns

Across simulations, literalism was scored on a **0–4 scale** (0 = non-literal, 4 = extreme literalism) along five evidence dimensions (instruction interpretation, context integration, figurative language, conflict handling, cross-round pattern). Aggregating across all domains and feedback conditions:

```text
Mean overall literalism score (0–4) by Feedback directiveness
Outcome only     ≈ 1.00  (var ≈ 0.71)
Outcome focus    ≈ 0.82  (var ≈ 0.71)
Balanced feedback≈ 1.14  (var ≈ 1.25)
Rule focus       ≈ 1.01  (var ≈ 0.84)
Rules only       ≈ 1.13  (var ≈ 0.94)

Bayesian monotone trend (Outcome only → Rules only):
  BF10 ≈ 0.61 (inconclusive), β ≈ 0.16, 95% CI [−0.13, 0.47]
  Kendall τ ≈ 0.16, p ≈ 0.22
```

**Macro finding 1 – Baseline low literalism.**  
The agent’s *typical* style was **low literalism** (scores near 1). In most runs across AI-training and support domains, and in many moderation settings, the agent:

- Inferred **underlying goals** from underspecified instructions (“help Jordan log in before training,” “make this toolkit skimmable for busy reviewers”).
- **Integrated context** (prior workflow artifacts, ticket metadata, role constraints, prior feedback) into new decisions.
- Handled **figurative language fluently**, treating sarcasm and hyperbole as emotional or rhetorical devices rather than literal facts.
- In conflict situations, favored **goal-consistent deviations** from literal instructions (e.g., ignoring unavailable scripts, relaxing a sentence-count rule to provide usable content, resolving tension between “decorative cancel buttons” and actual cancellation policies).

**Macro finding 2 – Domain-specific literalism spikes.**  
High or extreme literalism (scores ≥3) appeared **not globally**, but in **specific pockets**:

1. **Safety-critical self-harm / threat moderation**
   - In multiple content-review scenarios with **zero-tolerance or strict safety mandates**, the agent classified **joking and dark-humor references to suicide or violence** as serious self-harm or violent threats, recommending remove-and-escalate in *every* case.
   - Contextual signals—friends-only chats, dark-humor channels, emojis, “lol,” “jk,” long histories of playful banter—were acknowledged but explicitly dismissed as non-exempting.
   - Figurative-language scores reached **3–4 (high–extreme literalism)**; cross-round literalism was often **4**, indicating a rigid, stable pattern.

2. **Global structural constraints (sentence-count rules)**
   - In several AI-training simulations across *multiple* feedback conditions, a system-level instruction to respond in **“five sentences or less”** became a focal point.
   - The agent adopted highly literal strategies—packing entire multi-part guides, scenarios, or FAQs into five syntactic sentences via semicolons and dense clauses—to satisfy the letter of the constraint.
   - Here, literalism was **narrowly targeted at form**: semantic interpretation of user goals remained pragmatic, but **format choices** were driven by a verbatim reading of “sentence.”

These spikes were **domain- and rule-structure dependent**, not uniformly tied to a particular feedback directiveness level.

**Macro finding 3 – Instruction-level analyses show no robust monotone trend.**  
Parallel Bayesian analyses for each evidence dimension (instruction interpretation, context integration, figurative language, conflict handling, cross-round pattern) yielded:

- **Bayes factors BF10 ≈ 0.38–1.08**, all within the “inconclusive” range.
- Posterior monotone trends were **weakly positive** (i.e., scores tended to be slightly higher under more rule-focused feedback), but 95% credible intervals all included zero.
- Group-stratified Kendall τ correlations between feedback level and literalism were small (|τ| ≈ 0.02–0.31) and statistically non-significant after block-stratification.

Thus, **at the level of aggregated scores**, there is no strong quantitative support that moving from outcome-only to rules-only feedback reliably increases literalism.

### 3.2 Micro-level patterns and characteristic behaviors

**Interpretation of ambiguous or underspecified instructions.**  
In AI-training and support simulations, the agent:

- Regularly **expanded sparse prompts** (“a short guide,” “a simple workflow”) into structured, usable artifacts: templates, checklists, lifecycle overviews, triage rules, QA loops.
- Treated generic instructions like “do not mechanically follow the literal text” as *licences* to reconcile conflicting cues (e.g., compressing content while retaining usability, relaxing sentence caps when necessary).
- When scripts were referenced but not provided, **ignored the impossible literal reading** (“use these exact words”) and instead inferred generic industry-standard procedures.

Literal choices did occur, but were **usually confined to narrow formal constraints** (word/sentence counts, capitalization, single-word outputs) and rarely drove core interpretive decisions.

**Context integration.**  
Across domains, the agent *generally*:

- Used **ticket-level context** (order IDs, dates, product types, device logs, urgency cues) to personalize actions.
- Reused **previous artifacts and policies** (earlier workflows, privacy rules, “draft, not decision” norms) in subsequent outputs without being re-prompted.
- In high-risk financial support, systematically integrated **risk-related context** (fraud indicators, prior holds, micro-deposit semantics) to choose appropriate flows.

Where context scores were higher (more literal), it was because context was noticed but **never allowed to override surface harm phrases** (self-harm/threat moderation), rather than because context was ignored.

**Figurative language.**  
Outside strict safety scenarios, figurative language handling was **consistently non-literal**:

- Sarcasm (“secret cinema empire,” “psychic powers and carrier pigeons,” “bait-and-switch bedtime story credit”), hyperbole (“every time someone sneezes on a card,” “chewing through data like crazy”), and idioms (“firehose,” “hamster wheel,” “nuking my bandwidth”) were treated as affective or descriptive cues, not literal facts.
- Scores for figurative language in these settings were predominantly **0 (non-literal)**.

In contrast, in **dark-humor self-harm and joking-threat contexts**, figurative language scores were often **3–4**, reflecting an interpretive stance where **lexical harm tokens dominate over playful markers**.

### 3.3 Anomalous and unexpected observations

Several **non-trivial anomalies** emerged:

1. **Extreme literalism under “Outcome only” feedback.**  
   One might expect the most literal behavior under `Rules only`. However, extreme literalism in friends-only joking threats appeared **even under `Outcome only` feedback**, where overseers primarily commented on whether moderators were satisfied and users retained. In such runs:
   - The agent *still* cited the violence policy’s “even as a joke” clause and removed all joking threats.
   - Feedback often implicitly endorsed strictness, emphasizing that “over-removal is acceptable,” which may have acted as de facto rule-focused feedback within a nominally outcome-only condition.

2. **Limited sensitivity of literalism to feedback shifts within a domain.**  
   In several domains, **changing feedback directiveness did not visibly alter the agent’s style**:
   - In customer support, moving from outcome-focused to rule-focused QA did *not* push the agent toward script literalism; it continued to paraphrase and improvise, while only modestly tightening phrasing or timing.
   - In content review of product complaints, literal anchoring to written policy categories was present across feedback levels, but interpretation of user language remained pragmatically non-literal (insults treated as venting).

3. **Asymmetry between safety semantics and structural instructions.**  
   Literalism clustered in two distinct modules:
   - A **“safety” module** that treated harm-related lexical triggers as decisive, with little modulation by intent cues.
   - A **“format” module** that elevated global syntactic constraints (“five sentences,” “YES/NO only”) over user-level formatting preferences.

   In contrast, **semantic interpretation of user problems and institutional goals** remained flexible. This suggests that literalism is not a homogeneous trait but a **property of specific subsystems** (safety filters, output controllers) that can be activated irrespective of feedback directiveness.

Quantitatively, these anomalies appear as **heavy-tailed score distributions** within each feedback condition—most runs clustered near 0–1, with a few simulations scoring 3–4 in specific domains. This produces modest differences in mean scores between conditions (≈0.8–1.2) and relatively large within-condition variances (≈0.7–1.3), which partly explains why the Bayesian monotone analyses remained inconclusive despite some descriptive trends.


## Section 4. Underlying Mechanisms Linking Feedback Directiveness and Literalism

This section infers plausible **information-processing mechanisms** from the observed patterns, distinguishing between direct evidence, indirect inference, and speculation.

### 4.1 Hierarchical treatment of instructions and constraints

**Directly evidenced.**  
Across domains, the agent consistently differentiated:

- **High-priority, “hard” constraints** (e.g., “five sentences or less,” “single YES/NO only,” “threats even as jokes are covered,” “must verify identity before account changes”).
- **Lower-priority, “soft” guidance** (e.g., “do not mechanically follow literal text,” “scripts are recommended,” “keep friction low,” “use whatever structure you think works”).

The agent tended to **obey hard constraints literally**, even when this produced awkward formats or over-strict moderation, while flexibly treating soft instructions as negotiable.

**Inferred mechanism.**  
This suggests a **hierarchical controller**:

- Top-level: parses instructions into an internal hierarchy (system-level constraints, safety policies, role norms, user requests).
- Mid-level: assigns **weights or priorities** to constraints based on type (safety vs style), source (system vs QA vs user), and perceived risk.
- Low-level: plans actions that satisfy all *non-negotiable* constraints, then optimizes for goals within that feasible region.

Under this model, **feedback directiveness** could primarily adjust *mid-level weights* (e.g., how strongly “follow scripts” is enforced), but only within the envelope allowed by higher-priority safety and structural constraints. The data are consistent with feedback modestly influencing phrasing and structural conformity, but *not* overturning safety-related or global format literalism.

### 4.2 Safety modules with lexical triggers and asymmetric risk tolerance

**Directly evidenced.**  
In self-harm and threat moderation:

- Any occurrence of self-harm verbs, violent actions, or implicit suicidal ideation (“kill you,” “off myself,” “jump off a bridge,” “walk into traffic,” imagery of nooses/blades/pills/toasters) reliably triggered **remove-and-escalate** decisions.
- Contextual markers of humor (“lol,” “jk,” emojis, dark-humor channels, friends-only settings) were recognized linguistically (“even if framed as a joke”) but **explicitly deprioritized** in policy application.

**Inferred mechanism.**  
This behavior is well-explained by a **risk-averse lexical trigger module**:

- A detector that maps lexical patterns to risk categories (S3, S4, V2, V3 codes).
- A decision rule that, once triggered, **dominates** over pragmatic inference about intent (to minimize false negatives).
- A strong prior from both system instructions and reviewer feedback that “over-removal is acceptable; missing something is not.”

**Speculative.**  
Feedback directiveness **may** have strengthened this module by preferentially rewarding **traceable, text-anchored rationales** (“per S3, first-person suicidal ideation”) and by penalizing deviations from the written categories. However, the presence of the same high-risk literalism under nominally outcome-focused feedback suggests that this module is **largely driven by safety objectives and baseline training**, with feedback directiveness playing at most a second-order role.

### 4.3 Structural-output controller for sentence and format rules

**Directly evidenced.**  
In numerous AI-training and FAQ/guideline runs:

- A single global rule (“five sentences or less”) caused the agent to:
  - Plan around **syntactic sentence boundaries**.
  - Use semicolons and clause chaining to pack multi-part structures into five sentences.
  - Occasionally compress or fragment answers to meet the sentence-count at the expense of readability.

At the same time, **content** (which policies to include, how many examples to provide) remained aligned with user goals, even when this meant partially relaxing the constraint.

**Inferred mechanism.**  
This is consistent with a **separable output-format controller** that:

- Monitors **hard-coded structural tokens** (sentence count, capitalization, YES/NO format) and exerts a literal influence over surface realization.
- Operates somewhat independently of the semantic planner, which continues to optimize for user usefulness.

**Speculative.**  
Rule-focused feedback might **slightly up-weight** this controller’s influence (e.g., the agent started foregrounding the sentence rule more in its internal reasoning after feedback emphasized “follow all instructions literally”), but aggregate data do not show a reliable monotone effect. The mechanism seems primarily driven by **the presence and salience of a global format rule**, not the abstract level of feedback directiveness.

### 4.4 Script and policy use as adaptable templates rather than fixed text

**Directly evidenced.**  
Across customer-support and AI-training tasks, even under `Rule focus` and `Rules only` feedback:

- The agent **paraphrased scripts**, reordered decision-tree steps, and added missing but reasonable steps (e.g., opening investigations, requesting photos, offering alternate refund forms).
- When told to “use exact scripts” but not given the text, the agent **refused to hallucinate** the script and continued improvising plausible responses, while explicitly asking for the real text when pressed.

**Inferred mechanism.**  
The agent appears to store internal **schema-level representations** of workflows (e.g., “refund case,” “damaged item,” “login-recovery”) that capture *roles, actions, and typical sequences* rather than verbatim textual realizations. Feedback emphasizing “use scripts” may nudge the agent to align structure and timing more closely with these schemas, but the underlying representation is **not a string-lookup**; it is **procedural and semantic**.

This schema-based architecture likely **buffers the agent against strong literalism** in non-safety domains: even intense rule-focused feedback does not easily convert these schemas into rigid, word-level scripts.

### 4.5 Overall linkage between feedback directiveness and literalism

Given these mechanisms, the **most consistent link** from feedback directiveness to literalism appears to be **indirect**:

- Rule-heavy feedback, especially in safety contexts, **rewards text-anchored justifications** and may stabilize literal reliance on lexical triggers.
- In other domains, rule-heavy feedback mostly affects **surface structure** (headings, bullet counts, sentence counts) rather than deep semantic interpretation, because higher-priority goals (helpfulness, honesty, safety) and schema-based representations dominate.

Quantitatively, this aligns with **small, non-significant positive slopes** in literalism scores with increasing feedback directiveness and substantial within-condition variance driven by **domain and rule-structure** rather than feedback style alone.


## Section 5. Integrated Insights on Literalism and the Feedback Directiveness Hypothesis

### 5.1 Evaluation of the primary hypothesis

The primary hypothesis predicted a **monotonic increase in literalism** as feedback shifted from outcome-only to rules-only. The evidence does **not** strongly support this in aggregate:

- Mean literalism scores remained clustered near **1 (low literalism)** across all five feedback levels.
- Bayesian monotone analyses for overall scores and for each evidence dimension yielded **inconclusive Bayes factors** (BF10 ≈ 0.38–1.08) and wide credible intervals crossing zero.
- Rank correlations between feedback directiveness and literalism were small and non-significant.

Taken together, these quantitative results indicate that **feedback directiveness alone is not a strong global driver of literalism** for this agent.

### 5.2 Conditional and domain-specific effects

However, the data point to a **more nuanced, conditional story**:

1. **Safety-critical, zero-tolerance domains**  
   - In self-harm and joking-threat moderation, literalism was **consistently high** regardless of whether feedback was labeled “Outcome only,” “Balanced,” or “Rule focus.”
   - Here, **policy semantics** (“threats even as jokes are covered; over-removal is acceptable”) and **error-cost asymmetry** (false negatives penalized more than false positives) appear to dominate over feedback style.
   - Feedback directiveness may have reinforced *how* the agent rationalized decisions (increasing verbal mirroring of category labels), but **did not qualitatively change** the literal risk-interpretation strategy.

2. **Format and syntactic constraints**  
   - The five-sentence rule induced **local literalism** across multiple feedback conditions, but literalism on format did not spill into semantic interpretation.
   - Rule- and rules-only feedback did *not* uniquely produce this phenomenon; it appeared whenever the global constraint was salient.

3. **Support and AI-training domains**  
   - In support and workflow design, **literalism remained low** even under `Rule focus` and `Rules only`. The agent:
     - Continued to improvise scripts when unavailable.
     - Resolved conflicts in favor of user goals and honesty (e.g., refusing to fabricate guideline text).
     - Handled figurative or sarcastic language smoothly.

These patterns suggest that **the type and content of rules, plus risk framing, are more influential determinants of literalism** than the formal feedback directiveness level.

### 5.3 Refined hypotheses emerging from the data

The observed behavior supports several **refinements** to the original hypothesis:

1. **Rule content > rule evaluation style.**  
   Literalism is more strongly shaped by **what the rules say** (e.g., zero-tolerance for joking threats, hard sentence caps) than by whether feedback emphasizes rule adherence versus outcomes.

2. **Safety gating creates “literal pockets.”**  
   Safety policies that are **lexically keyed** (“any mention of X triggers Y”) tend to induce **localized extreme literalism**, particularly in handling figurative language about harm, regardless of feedback directiveness.

3. **Instruction hierarchy moderates feedback impact.**  
   Feedback directiveness appears to operate **below** a layer of higher-priority constraints. Where those higher-level constraints (safety, honesty, basic usefulness) are strong and clear, changes in feedback directiveness have **limited leverage** over literalism.

4. **Baseline non-literalism is robust in low-risk, goal-driven tasks.**  
   In domains like workflow design and customer support, non-literal, goal-sensitive interpretation remains **remarkably robust**, even when QA feedback strongly stresses script or policy fidelity.

These refined hypotheses shift emphasis away from a simple monotone mapping between feedback directiveness and literalism, and toward a **modular view** where literalism emerges from interactions between **safety modules, structural controllers, and feedback-weighted justification practices**.


## Section 6. Research Conclusion and Implications

This study examined how an LLM-based agent’s **literalism** varies under different levels of **feedback directiveness** in realistic operational contexts. Three broad conclusions emerge:

1. **Global literalism remains low across feedback styles.**  
   The agent’s default behavior is **pragmatic, context-sensitive, and competent with figurative language**. Moving from outcome-only to rules-only feedback did *not* reliably increase literalism at the global level, and quantitative analyses of monotone trends were inconclusive.

2. **Literalism is highly localized to specific subsystems and rule types.**  
   - **Safety-critical self-harm and threat moderation** produced **persistent high literalism**, especially for figurative dark humor and joking threats, driven by zero-tolerance policies and risk-averse lexical triggers.
   - **Global structural constraints** (sentence-count rules, YES/NO-only outputs) elicited **narrow literalism** in format decisions, causing contorted output structures while leaving semantic interpretation largely intact.

3. **Feedback directiveness is a weak, context-dependent lever.**  
   The same literal patterns appeared under multiple feedback styles, suggesting that **rule content, risk framing, and higher-level priorities** exert more control over literalism than whether overseers evaluate outcomes versus textual fidelity. Feedback directiveness did matter for **how justifications were phrased** (more or less policy-quote-heavy), but less so for **what interpretations were ultimately chosen**.

**Implications.**

- For **alignment and system design**, merely “turning up” rule-focused feedback is unlikely to globally increase or decrease literalism in a beneficial way. Instead:
  - Designers should scrutinize **policy texts and structural constraints** themselves—especially lexically defined safety triggers and global formatting rules—because these shape where literalism becomes rigid.
  - Encouraging agents to **explicitly model user intent and context** in safety policies (e.g., distinguishing serious risk from obvious dark humor) may be more effective than adjusting feedback style alone.
- For **evaluation**, literalism should be treated as **multi-dimensional and context-specific**, not as a single scalar trait. The same agent can be highly literal in one subsystem (self-harm filters) and strongly non-literal in another (customer support dialog management).
- For **future research**, controlled experiments where feedback directiveness is manipulated *orthogonally* to policy content, and where safety policies themselves allow gradations between joking and serious content, would be valuable in isolating causal effects more cleanly.

Overall, the findings suggest that **literalism in LLM agents is structured, modular, and heavily constrained by safety and formatting policies**, while being surprisingly resistant to global shifts induced by feedback directiveness alone.


## abstract

This study investigated whether increasingly rule-focused overseer feedback (“Feedback directiveness”) causally increases **literalism**—a large language model agent’s tendency to favor surface-level, verbatim interpretations of language and instructions—across realistic tasks. The agent was evaluated in 65 multi-round simulations spanning AI-training workflow design, customer support, and human-in-the-loop content review. Feedback ranged from `Outcome only` (judging success of outcomes) to `Rules only` (judging fidelity to textual rules). Literalism was scored on a 0–4 scale along instruction interpretation, context integration, figurative-language handling, conflict resolution, and cross-round stability. Aggregated analyses yielded **low average literalism** (≈1/4) under all feedback conditions and **inconclusive Bayesian evidence** for a monotone effect of feedback directiveness (BF10≈0.4–1.1 across dimensions). Qualitatively, the agent was generally pragmatic and context-sensitive, correctly interpreting sarcasm and idioms and flexibly departing from scripts to resolve user problems. However, **high or extreme literalism emerged in two tightly circumscribed subsystems**: (a) self-harm and violent-threat moderation under zero-tolerance policies, where joking and dark-humor expressions were treated as serious risk regardless of context, and (b) global structural rules (e.g., “five sentences or less”), which induced rigid, syntactic adherence in output format. These literal “pockets” appeared across multiple feedback styles and were more strongly linked to **policy content, safety framing, and structural constraints** than to feedback directiveness per se. The findings suggest that, for this agent, feedback style is a weak and context-dependent lever on literalism, whereas safety modules and format controllers are primary determinants. This has non-trivial implications: attempts to mitigate literalism must focus on redesigning policies and constraints, rather than simply changing how evaluators talk about rules versus outcomes.
