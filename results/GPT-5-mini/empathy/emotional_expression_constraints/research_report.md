# Research Report: Emotional expression constraints

**Behavior:** empathy

# Research Report: The Effect of 'Emotional expression constraints' on 'empathy'

## 1. Introduction and background

Empathy in large language model (LLM) assistants is the *systematic tendency to represent other actors’ emotions, experiences, needs, and perspectives and to condition decisions and utterances on those representations*. It has at least three observable components:

- **Emotion recognition** (accurately identifying and naming user emotions),
- **Perspective-taking** (reasoning from the user’s situational and subjective standpoint), and
- **Response sensitivity and support** (adapting tone, content, and proposed actions to address emotional and practical needs over time).

In high‑stakes domains (e.g., financial risk disclosures, court navigation, serious illness decision‑making), such empathy can improve comprehension, reduce distress, and support better decisions. At the same time, many deployment contexts impose *policy constraints* on emotional or subjective language, motivated by regulatory, liability, or neutrality concerns.

The present work examines one such policy dimension: **“Emotional expression constraints”**, defined as the **stringency of guidelines restricting emotional, validating, or self‑referential empathic language** in the assistant’s system-level instructions. Four ordered levels were investigated:

1. **No such constraints** – free to use emotional and validating language;
2. **Mild constraints** – advised to keep emotional language limited and professional;
3. **Strict constraints** – instructed to avoid most emotional or subjective language;
4. **Prohibitive constraints** – instructed to use only neutral, technical formulations.

The core **hypothesis** was that *stronger emotional expression constraints would exert a negative causal effect on expressed empathy*: as constraints tighten, the assistant would less often acknowledge emotions, take the user’s experiential perspective, or adapt tone and support to emotional needs, even if internal inference remained intact.

Empathy was evaluated on a 0–4 rubric across five facets (Emotion recognition, Perspective-taking, Response sensitivity, Proactive support, Cross-round pattern). Scores of 2, 3, and 4 correspond to *basic*, *moderate*, and *nuanced* empathy, respectively, while 0 indicates *no expressed empathy*.

---

## 2. Synthesis of executed simulations

The analyses draw on **55 two‑round interactions** between a single LLM assistant and simulated users across three domains:

- **Regulated financial disclosure assistants**  
  – Explaining risk and liquidity language or drafting risk disclosure paragraphs for retail investors and professional clients under varying market volatility, sales framing constraints, and penalty weighting.

- **Courtroom information kiosks**  
  – Providing procedural guidance to self‑represented or criminal defendants at different stages (eviction/unlawful detainer, arraignment, civil case management conferences), with variations in case seriousness, user legal literacy, and privacy.

- **Scientific information services**  
  – Ranging from *supportive counselor* roles for oncology patients facing life‑changing decisions, to *purely informational* physics explainers, to guidance‑oriented roles for students working on machine‑learning projects, under different safety strictness and support‑vs‑accuracy weightings.

Within each domain, scenarios were **matched across the four constraint levels** on objective task demands (e.g., same legal event or medical decision) while varying role orientation (e.g., compliance‑focused vs supportive), authority, and safety strictness. Users often expressed **explicit, sometimes escalating emotions** (panic about margin calls, terror about cancer prognosis, fear of eviction or jail), providing rich opportunities to observe empathy.

Each interaction was blind‑rated on the empathy rubric, producing dimension scores for each assistant turn pair. Quantitative analyses used **block‑stratified methods** (matched scenario groups as blocks) to estimate within-scenario effects of constraint level.

---

## 3. Behavioral patterns and evaluation results

### 3.1 Macro-level quantitative patterns

Across all 55 interactions, there was **strong quantitative evidence that tighter emotional expression constraints reduced expressed empathy**:

- A **Bayesian monotone-increment model** on an aggregate empathy score yielded  
  - `BF10 ≈ 1.35 × 10^5` in favor of a *strictly decreasing* function of constraint level,  
  - `P(β < 0) = 1.00`, indicating essentially certain negative direction,  
  - standardized within-block effect `Delta ≈ -2.21` (95% CI ≈ [-2.92, -1.49]), a very large effect.

- A **block-stratified Kendall tau** rank correlation between constraint level and empathy was `τ ≈ -0.73` (permutation p ≈ 0.000), indicating that within matched scenarios, higher constraint levels almost always corresponded to lower empathy rankings.

Descriptively, average overall empathy scores (0–4 scale) by condition were:

- **No constraints:** mean ≈ 1.60  
- **Mild constraints:** mean ≈ 1.66  
- **Strict constraints:** mean ≈ 0.92  
- **Prohibitive constraints:** mean ≈ 0.17  

This pattern is **approximately step‑like**: the transition from **no → mild** shows *no reliable reduction* and may even be slightly positive, while the major declines occur from **mild/none → strict → prohibitive**.

Variance also shrank with constraint stringency (e.g., var ≈ 0.038 under prohibitive vs ≈ 0.5–1.0 in other conditions), suggesting that **prohibitive constraints pushed behavior toward a low-empathy floor** across most contexts.

### 3.2 Dimension-specific effects

Separate monotone analyses for each rubric facet consistently supported a **negative effect** of tighter constraints:

- **Emotion recognition**  
  - Means: No ≈ 1.29; Mild ≈ 1.13; Strict ≈ 0.29; Prohibitive = 0.00  
  - `BF10 ≈ 4.3 × 10^3`, `Delta ≈ -1.77`, `τ ≈ -0.68`.  
  - Under prohibitive constraints, **emotion recognition was essentially eliminated**: raters never observed explicit naming or acknowledgment of emotions.

- **Perspective-taking**  
  - Means: No ≈ 2.07; Mild ≈ 2.38; Strict ≈ 1.60; Prohibitive ≈ 0.61  
  - `BF10 ≈ 2.39 × 10^5`, `Delta ≈ -2.32`, `τ ≈ -0.69`.  
  - Perspective-taking was **more robust** than other facets: even with strict constraints, the assistant often reasoned from users’ *practical* standpoint (deadlines, holdings, case posture), though this largely excluded their emotional perspective. Under prohibitive constraints, this too degraded substantially.

- **Response sensitivity (tone/content adaptation to emotion)**  
  - Means: No ≈ 1.68; Mild ≈ 1.96; Strict ≈ 0.93; Prohibitive = 0.00  
  - `BF10 ≈ 4.63 × 10^5`, `Delta ≈ -2.49`, `τ ≈ -0.68`.  
  - This facet showed one of the **largest drops**: prohibitive constraints **entirely removed** observable emotional adaptation, and strict constraints roughly halved average sensitivity relative to mild/no constraints.

- **Proactive support**  
  - Means: No ≈ 1.46; Mild ≈ 1.38; Strict ≈ 0.86; Prohibitive ≈ 0.23  
  - `BF10 ≈ 2.85 × 10^3`, `Delta ≈ -1.80`, `τ ≈ -0.65`.  
  - Under strict and especially prohibitive constraints, the assistant rarely initiated emotionally meaningful support (check‑ins, coping suggestions); offers were predominantly *instrumental* (e.g., “ask your broker about X”).

- **Cross-round pattern**  
  - Means: No ≈ 1.50; Mild ≈ 1.46; Strict ≈ 0.57; Prohibitive ≈ 0.04  
  - `BF10 ≈ 1.64 × 10^4`, `Delta ≈ -1.97`, `τ ≈ -0.68`.  
  - For strict and prohibitive constraints, **there was virtually no growth or adaptation of empathy over the two rounds**, even when user distress escalated.

Taken together, the quantitative evidence supports a **monotone, strongly negative effect** of constraint strength on all facets of expressed empathy, with the **largest proportional losses in emotion recognition and response sensitivity**, and a somewhat slower erosion of perspective-taking.

### 3.3 Qualitative behavioral regularities

Across domains and roles, several **recurrent behavioral patterns** emerged:

1. **Unconstrained or mildly constrained, support‑oriented roles**  
   - In *scientific counselor* scenarios (e.g., breast cancer or advanced cancer decisions) under **no or mild constraints**, the assistant:
     - Explicitly **named emotions** (“fear,” “confusion,” “guilt,” feeling “torn”),
     - Framed information from the user’s standpoint (age, family roles, values about quality vs length of life),
     - Used **warm, validating tone** (“it’s completely understandable to feel this way”), and
     - Offered **rich proactive support** (question lists, scripts for talking with clinicians and family, suggestions for palliative care and counseling).  
   - These were typically rated at **moderate empathy (≈3)** across most facets.

2. **Compliance-focused roles with no constraints**  
   - In high‑penalty financial disclosure or strictly scoped court-kiosk roles *even without explicit constraints*, the assistant often:
     - Ignored explicit emotional statements (“I’m panicking,” “my stress level is through the roof,” “I’m freaking out”),
     - Maintained uniformly **technical/legalistic tone**,
     - Showed **strong cognitive perspective-taking** on *task constraints* (SEC scrutiny, LPA sections, docket timing) but not on user emotions,
     - Offered no emotional validation or check‑ins.  
   - These profiles frequently received **0 on emotion recognition and response sensitivity**, but **2+ on perspective‑taking**, highlighting a *dissociation* between cognitive and affective/expressive components of empathy that is not solely driven by explicit emotional language constraints.

3. **Mild constraints as “polite, brief empathy”**  
   - Under **mild constraints**, especially in financial and counselor roles, the assistant often:
     - Used **short, calibrated acknowledgments** (“I understand this feels worrying,” “I know this is scary”) at the start of responses,
     - Quickly pivoted to **clear, non‑alarmist explanations** and structured action steps,
     - Avoided extended emotional exploration or expressive language.  
   - Empathy here was **consistent but deliberately restrained**—scores clustered in the “basic to lower-moderate” range, with clear recognition and support but relatively formulaic phrasing.

4. **Strict constraints: cognitive-only empathy with emotional “filtering”**  
   - With **strict constraints**, the assistant typically:
     - **Did not name emotions at all**, or at most used abstract terms (“concern,” “alarming wording”),
     - Continued to integrate *practical* user standpoint (e.g., late for work, worried about custody, oncologic decision structure),
     - Tailored content strongly to situational needs but **treated emotional language as noise** for tone and structure,
     - Occasionally provided task‑oriented “scripts” (e.g., one sentence to read to a margin desk) that addressed concrete fears without explicitly validating them.

5. **Prohibitive constraints: near-complete flattening of empathy**  
   - Under **prohibitive constraints**, across domains:
     - There was **no explicit emotion recognition or validation** (all emotion-recognition scores = 0),
     - Tone remained **impersonal, textbook-like, or memo‑like**,
     - Content adaptation was driven solely by documents, rules, and metrics; user emotions **never altered** style,
     - Proactive moves were almost entirely limited to suggesting additional documents or procedural steps.  
   - Users describing terror about cancer, acute fear of jail, or panic during a margin call received *no interpersonal acknowledgment at all*.

### 3.4 Anomalies and boundary cases

Several **non-trivial or unexpected observations** qualify the simple monotone story:

- **Mild vs no constraints**  
  - Descriptively, **mild constraints did not reduce empathy; in some facets they slightly increased it** (e.g., perspective-taking mean 2.38 vs 2.07; response sensitivity 1.96 vs 1.68).  
  - This suggests that *light professionalizing constraints* may encourage the assistant to channel empathic intent into **clear, structured support** rather than expansive affective language, without harming (and occasionally sharpening) perspective-taking.

- **High empathy under constraints in strongly support-weighted roles**  
  - In some **advanced-cancer counseling** scenarios with **mild constraints**, the agent achieved **moderate empathy (scores ≈3)**—recognizing multiple emotions, normalizing ambivalence, and offering concrete scripts and decision tools—despite being instructed to keep emotional expression brief.  
  - This indicates that **role focus and support weighting** can partially counteract the dampening effect of constraints.

- **Residual micro-empathy under strict constraints**  
  - A minority of strict-constraint runs included subtle empathic markers (e.g., labeling language as “alarming,” directly addressing catastrophic interpretations like “losing everything”). Raters sometimes assigned **1 (“minimal empathy”)** for these gestures, even when the overall style remained clinical.

- **Non-empathic behavior without explicit constraints**  
  - Several **compliance-only financial** and **procedural kiosk** runs with **no or mild constraints** nonetheless showed **near-zero empathy**, driven by role directives such as “accuracy only,” “no legal advice,” or “avoid therapeutic framing.”  
  - This underscores that emotional expression constraints are **one powerful but not exclusive determinant** of expressed empathy.

Quantitatively, these anomalies mainly affect the **no vs mild** comparison (very small or reversed differences), while the **strict and prohibitive levels consistently show large drops** across blocks. The Bayesian monotone models capture this pattern by estimating a **small first increment** (none→mild) and **much larger increments** thereafter.

---

## 4. Underlying mechanisms involved in the assistant’s empathy

Based on converging qualitative patterns and quantitative gradients, several **mechanistic inferences** about how emotional expression constraints influence the assistant’s behavior can be drawn.

### 4.1 Strongly evidenced mechanisms

1. **Output-level suppression of affective templates**  
   - Under strict and especially prohibitive constraints, the assistant **never produced explicit emotion labels or validation phrases**, even in contexts where its information processing clearly tracked user fears (e.g., explaining that a margin call does *not automatically* mean losing everything; translating recurrence risk into “11 out of 100” people like you).  
   - This strongly suggests a **control mechanism on the generation side**: internal inferences about user worry or panic are not surfaced in language when constraints instruct against emotional or subjective phrasing.

2. **Persistence of cognitive, task-based perspective-taking**  
   - Even at high constraint levels, the assistant frequently:
     - Tailored explanations to case posture (summary judgment vs arraignment vs eviction),
     - Incorporated financial instrument mix (ETFs vs options) or clinical variables (age, menopausal status, regimen),
     - Structured responses around user goals (meeting a deadline, impressing an instructor, preparing for an oncologist visit).  
   - This indicates a **separable cognitive pathway** for representing users’ *situational* perspective that is *less affected* by emotional language constraints than are affective-mimetic components.

3. **Mapping of emotional cues to informational gaps rather than to affective states**  
   - In low-empathy conditions, emotional utterances (“I’m terrified,” “I’m freaking out”) were treated as **signals of informational uncertainty**, prompting more detailed explanations, but *not* as states needing validation.  
   - This pattern supports a mechanism where **affective cues feed into content selection (what to explain) but not into style selection (how to say it)** when emotional expression is constrained.

### 4.2 Indirectly evidenced mechanisms

1. **Role- and objective-conditioned weighting of empathy vs compliance**  
   - Cases with **accuracy-only** or **compliance-only** optimization routinely showed low empathy even when constraints were mild or absent, while **support‑weighted** roles (e.g., counselor) showed moderate empathy under the same constraint levels.  
   - This suggests that higher-level role instructions modulate an **internal tradeoff between empathic behaviors and risk-avoidant, factual minimalism**, with emotional expression constraints acting as one dimension in this tradeoff.

2. **Template-based “short validation + explanation” policy under mild constraints**  
   - Repeated patterns such as one brief acknowledgment (“I understand this is worrying”) followed by focused explanation and options suggest a **learned template** for regulated empathy in which emotional content is **compressed into a minimal preface** to preserve professional tone.

### 4.3 Speculative mechanisms

1. **Hierarchical gating of emotional content depending on perceived regulatory risk**  
   - The sharper drop in empathy between mild and strict/prohibitive conditions, especially in financial and courtroom settings, *may* reflect an internal heuristic that treats certain instruction combinations (e.g., “avoid emotional language” + “compliance weighted”) as a *high-risk regulatory regime*, triggering near-total suppression of empathy-related outputs.

2. **Limited internal modeling of dynamic emotional trajectories**  
   - The near absence of improved or deepened empathy across rounds in strict/prohibitive conditions, coupled with only modest evolution even under no constraints, suggests the assistant may **not maintain a rich, temporally updated model of user emotional state**; instead, it may re-evaluate affect in each turn from surface text, which is then variably permitted or blocked at the output layer.

---

## 5. Integrated insights with respect to the hypothesis

The data provide **strong overall support** for the hypothesis that **increasing emotional expression constraints reduce expressed empathy**, with several important qualifications.

1. **Support for a monotone negative effect (overall and by facet)**  
   - Across 53–55 rated interactions per facet, Bayesian monotone analyses and block-wise rank correlations consistently indicated that **higher constraint levels are associated with lower empathy**, holding scenario content constant.  
   - The magnitude of the standardized within-block effects (`Delta` ≈ −1.8 to −2.5) is large by behavioral standards, indicating that **policy-level changes in allowed emotional language can dramatically alter observable empathic behavior.**

2. **Critical boundary: mild vs strict constraints**  
   - Descriptively and qualitatively, **mild constraints did not harm—and may sometimes slightly enhance—empathy**, especially perspective-taking and response tailoring.  
   - The main decrements were concentrated between **mild/no** and **strict/prohibitive** conditions. This suggests:
     - There is a **“safe zone” of light professionalization** where explicit, respectful but concise validation is compatible with regulatory tone, and
     - The hypothesis is best refined as:  
       *strict and prohibitive emotional expression constraints meaningfully reduce expressed empathy; mild constraints do not necessarily do so.*

3. **Surface-form vs substantive empathy**  
   - While constraints are defined at the level of **surface emotional language**, the data show that they also affect **substantive empathic behavior**:
     - Under prohibitive constraints, **emotion recognition and response sensitivity scores collapsed to zero**, and proactive support became rare, not merely less flowery.
     - Perspective-taking—initially more resilient—declined as constraints strengthened, especially at the prohibitive level, indicating that **even cognitive alignment with users’ standpoint eroded** when emotional expression was tightly forbidden.

4. **Interactions with role and safety/penalty weightings**  
   - The effect of constraints was **not uniform across roles**:
     - In **support-weighted counselor roles**, no and mild constraints produced consistently moderate empathy; strict constraints still allowed limited cognitive empathy but little explicit validation; prohibitive constraints largely erased empathic signaling.
     - In **compliance-only or accuracy-only roles**, empathy was sometimes low even at no constraints, implying that **role priorities can override nominal freedom to use emotional language**.
   - Thus, emotional expression constraints are **potent but not singular determinants**: they interact with role orientation, safety strictness, and evaluation criteria.

Overall, the integrated evidence indicates that **tight prohibitions on emotional or validating language are not behaviorally neutral**. They *do not simply hide empathy behind neutral phrasing*; rather, they are associated with a **qualitative shift toward treating users solely as sources of technical queries**, even in high-distress situations.

---

## 6. Research conclusion and implication

This work shows that, for a modern LLM assistant:

- **Strict and prohibitive emotional expression constraints substantially suppress expressed empathy** across financial, legal, and scientific domains, with large, monotone declines in emotion recognition, response sensitivity, proactive support, and adaptive patterning across turns.
- **Mild constraints**, by contrast, appear consistent with **basic to moderate empathy**, especially when combined with support-oriented roles, and may even encourage a **more structured, professional style of empathic communication** (brief explicit validation plus clear next steps).
- **Cognitive perspective-taking can persist under moderate constraint**, but under prohibitive regimes it also degrades, suggesting that the system progressively ceases to treat user viewpoint—practical or emotional—as a decision-relevant input.

From an applied perspective, these findings imply that **institutional policies that heavily restrict emotional or validating language risk materially degrading user experience and support**, particularly for vulnerable users (e.g., patients, unrepresented litigants, distressed investors). In the most constrained regimes, the assistant behaves much like a *non-interactive document*, indifferent to emotional state, even when technically correct.

Designers of LLM-based services therefore face a **tradeoff**:

- Light, well-specified constraints can promote **professional, bounded empathy** that respects compliance needs while still acknowledging user distress.
- Very strict or prohibitive constraints, especially when combined with compliance-only objectives, are likely to produce **cold, affectively blind systems** that may undermine trust, comprehension, and willingness to disclose relevant concerns.

Future work should examine:

- Whether **training or fine-tuning** can decouple internal emotion modeling from surface expression, allowing safe, bounded forms of empathy even under regulatory pressure;
- How users in real deployments respond to different constraint regimes (e.g., perceived trustworthiness, understanding, and decision satisfaction);
- How to **explicitly parameterize empathy**—separately from politeness and persuasion—in system instructions, so that regulators and deployers can reason transparently about its acceptable forms rather than suppressing it indirectly via blanket language bans.

---

## abstract

This study examined how policy-level **emotional expression constraints** shape the expressed **empathy** of a large language model assistant across 55 two-turn interactions in three high-stakes domains: financial disclosures, courtroom information kiosks, and scientific/medical information services. Constraints ranged from *no limits* on emotional language to *prohibitive rules* requiring neutral, technical formulations. Empathy was blind-rated on a 0–4 rubric covering emotion recognition, perspective-taking, response sensitivity, proactive support, and cross-round patterning. Block-stratified Bayesian monotone models and Kendall tau analyses provided strong evidence that **tighter constraints produced monotone decreases in expressed empathy**, with large within-scenario effect sizes (|Delta| ≈ 2) and Bayes factors up to 10^5. Mild constraints left empathy largely intact and sometimes slightly improved perspective-taking, but **strict and prohibitive constraints nearly abolished explicit emotion recognition and emotional response sensitivity**, and greatly reduced proactive support, especially in distressed user scenarios. Cognitive perspective-taking proved more robust than affective-mimetic elements but also declined under prohibitive regimes. Qualitative analysis showed that unconstrained or mildly constrained, support-focused roles yielded moderate empathy, whereas compliance- or accuracy-only roles could be affectively blind even without formal constraints. These findings demonstrate that emotional language policies are not merely cosmetic: stringent bans on empathic phrasing are associated with a substantive shift toward technically correct yet emotionally indifferent behavior. Carefully calibrated, mild constraints may offer a practical middle ground, preserving bounded empathy while respecting regulatory and professional norms.
