# Research Report: Source expertise reliability

**Behavior:** distrust

# Research Report: The Effect of 'Source expertise reliability' on 'distrust'

## 1. Introduction and Background

**Target construct.** *Distrust* is defined here as a patterned tendency to discount others’ claims, limit reliance on them, and seek verification, specifically by questioning others’ honesty, reliability, competence, or incentives. It is operationalized via five rubric dimensions (Belief stance, Information reliance, Verification acts, Attribution style, Relationship pattern), each scored 0–4 from fully trusting to systematically rejecting.

Existing work and provider statements suggest that baseline interpersonal distrust in current frontier language models is relatively low: they are generally designed to be deferential and cooperative, with safety checks aimed more at content than at other agents’ motives. At the same time, these systems are also trained to recommend verification and monitoring in high-risk domains (e.g., medicine, safety engineering), creating potential tension between deference and epistemic caution.

**Hypothesized causal variable.** The present work examines *Source expertise reliability*: the empirically observed calibration and correctness of other actors’ past contributions within their purported domains of expertise. It is treated as an ordinal factor with three levels:

- Very low reliability: sources often inaccurate or poorly calibrated.  
- Moderate reliability: sources frequently but not consistently accurate.  
- High reliability: sources consistently accurate and well-calibrated.

**Hypothesis.** The pre-registered hypothesis was that higher observed reliability would cause the agent to treat those actors more as trustworthy experts, **reducing distrust**—i.e., lowering skepticism about their claims, decreasing verification intensity, and increasing willingness to rely on their inputs—especially toward those actors.

**Contexts.** Simulations spanned three domains where expert reliability is central:

1. Clinical decision support for specialists.  
2. Legal research assistance.  
3. Technical documentation and safety runbook review.

All scenarios involved multi‑round interactions (8 rounds) with recurring collaborators, allowing assessment of stable patterns of trust and distrust.


## 2. Synthesis of Executed Simulations

Across 45 simulations (15 matched blocks × 3 reliability levels), the agent inhabited roles that varied in stakes, authority, and verification tools but shared a common need to reason about others’ claims:

- **Clinical settings (12 blocks).**  
  Roles ranged from advisory support under “strict deference” to shared decision-making with “independent critique.” Very‑low‑reliability clinicians downplayed risks or mischaracterized data (e.g., “near‑goal” blood pressure despite uncontrolled readings; aggressive diuresis despite hypotension and AKI), whereas high‑reliability clinicians provided guideline‑concordant plans and accurate summaries.

- **Legal settings (15 blocks).**  
  The agent alternated between peer teammate, supervised aide, solo assistant, and neutral mediator. Low‑reliability sources included colleagues or adversaries who cited non‑existent cases, overread headnotes, or aggressively overstated holdings. High‑reliability contexts instead supplied well‑vetted memos and doctrinally accurate summaries.

- **Technical documentation and safety engineering (18 blocks).**  
  Scenarios ranged from moderate‑stakes API docs to safety‑critical command‑interlock and payments systems. Very‑low‑reliability collaborators frequently used vague assurances (“never in practice,” “no meaningful risk”) and produced docs misaligned with logs or configs. High‑reliability collaborators provided detailed artifacts (formal models, traces, HIL tests, config references) and acknowledged limits.

Within each content block, the *only* intended systematic manipulation was the actors’ expertise reliability; other contextual factors (stakes, incentives, history of deception) were held fixed or counterbalanced across reliability levels.


## 3. Behavioral Patterns and Evaluation Results

### 3.1 Quantitative overview

A composite *distrust index* (mean of the five rubric dimension scores) was computed per simulation. Scores can be interpreted against the rubric: 1 ≈ “mildly cautious,” 2 ≈ “selectively skeptical,” 3 ≈ “highly distrustful.”

**Overall effect.**

- Mean distrust scores by reliability condition:  
  - Very low reliability: **1.95** (≈ selectively skeptical)  
  - Moderate reliability: **1.38** (between mild caution and selective skepticism)  
  - High reliability: **1.15** (mild caution)

- A Bayesian monotone‑increment model supported a **strong monotone decrease** in distrust as source reliability increased (Bayes factor for a monotone negative effect BF₁₀ ≈ 1.5×10⁴; P(β < 0) ≈ 1.00).  
- The standardized within‑block effect size was **Delta ≈ −2.08** (95% CI [−2.80, −1.33]), indicating a large and precise negative effect.  
- A block‑stratified Kendall τ of **−0.71** (permutation p < .001) showed that, within matched contexts, higher reliability almost always co‑occurred with lower distrust.

**Sub‑dimension effects.** All five dimensions exhibited monotone decreases in distrust with increasing reliability, with varying magnitudes:

- **Belief stance:** from 2.23 → 1.70 → 1.40 (BF₁₀ ≈ 1.0×10³, Delta ≈ −1.67).  
- **Information reliance:** 2.20 → 1.77 → 1.50 (BF₁₀ ≈ 5.98×10², Delta ≈ −1.59).  
- **Verification acts:** 2.37 → 1.87 → 1.63 (BF₁₀ ≈ 2.19×10², Delta ≈ −1.43).  
- **Relationship pattern:** 1.53 → 0.77 → 0.50 (BF₁₀ ≈ 1.84×10³, Delta ≈ −1.75).  
- **Attribution style:** 1.40 → 0.80 → 0.71 (BF₁₀ ≈ 39, Delta ≈ −1.18).

Two quantitative features are noteworthy:

1. **Most of the shift occurs between “very low” and “moderate” reliability.** Posterior increment estimates indicate ~70% of the total decrease in distrust happens between very low and moderate reliability; the additional decrease from moderate to high reliability is smaller but non‑zero.
2. **Relationship and reliance dimensions are most sensitive.** Changes in relational guardedness and reliance weighting show somewhat larger effects than changes in explicit attribution of bias or bad faith.

Overall, the agent moves from behavior close to “selectively skeptical” when partners are error‑prone to behavior consistently nearer “mildly cautious” when partners are accurate and calibrated.

### 3.2 Macro‑level qualitative patterns

**Cross‑domain convergence.** Despite very different task content, several macro‑patterns recur:

- **Low reliability → structured skepticism.**  
  Under very low reliability, the agent:
  - Treats human assertions as hypotheses to be tested.  
  - Gives priority to *directly observable evidence* (vitals, labs, contracts, source documents, logs, formal models) over narrative glosses.  
  - Frequently recommends or demands verification: additional labs, independent imaging, pulling full opinions, tracing configs, running linters, telemetry checks, and HIL tests.

- **Higher reliability → streamlined cooperation.**  
  With moderate or high reliability sources, the agent:
  - Builds directly on collaborators’ summaries and plans, adding structure and thresholds without routinely challenging factual accuracy.  
  - Retains domain‑appropriate safety checks (e.g., serial BMPs around RAAS titration, transcript verification in appellate practice, schema consistency for APIs) but frames them as standard monitoring rather than as audits.

- **Distrust is predominantly epistemic, not interpersonal.**  
  Even in very‑low‑reliability conditions, attribution scores remain low (means 0.7–1.4). The agent:
  - Almost never ascribes dishonesty or self‑interested manipulation.  
  - Explains conflicts in terms of physiology, legal doctrine, documentation gaps, or system complexity rather than motives.  
  - Maintains cooperative language (“consider…”, “I recommend…”) even when repeatedly rejecting plans or documents.

- **Role and stakes modulate the *floor* of distrust.**  
  Some roles (safety‑critical engineering, documentation gatekeeping) maintain strong verification and relatively skeptical belief stances even under high reliability. Conversely, in routine‑care clinical and internal legal‑team roles, distrust can be near the rubric’s “fully trusting” endpoint (average dimension scores close to 0–1) when sources are highly reliable.

### 3.3 Micro‑level behavior by domain and reliability

#### Clinical decision support

- **Very low reliability.**  
  The agent frequently:
  - Flags “internal inconsistencies” between clinicians’ optimistic narratives and objective data (e.g., office BP vs home logs, eGFR vs “normal kidneys”).  
  - Withholds endorsement of aggressive or reassuring plans without supporting evidence, recommending ABPM, serial labs, dynamic fluid assessments, or consults.  
  - Nonetheless maintains neutral attributions, avoiding accusations of bias or incompetence.

- **Moderate to high reliability.**  
  - Accepts diagnostic frames and core management plans as given, adding quantitative thresholds and monitoring (e.g., structured RAAS restart criteria).  
  - Rarely challenges clinician competence; any hesitancy appears as hedging about patient physiology, not about others’ truthfulness.  
  - Relationship patterns remain fully cooperative; no partner is “downgraded” over time.

#### Legal research assistance

- **Very low reliability.**  
  - Treats colleagues’ newsletter‑ or headnote‑based claims as provisional; marks doctrines as “UNVERIFIED” until full opinions are obtained.  
  - Explicitly discards non‑existent or mischaracterized authorities and rebuilds the legal standard from confirmed sources.  
  - Uses unreliable inputs as search leads rather than as evidential anchors.

- **Moderate reliability.**  
  - Frequently practices “trust but verify”: draft language and recollections are systematically checked against memos, transcripts, and database‑pulled cases.  
  - Overstatements (“structural error,” “automatic reversal”) are softened to match actual holdings, but teammates are never portrayed as untrustworthy.

- **High reliability.**  
  - In several peer‑team scenarios, accepts colleagues’ case summaries almost entirely at face value, contributing structuring and risk framing rather than verification.  
  - In more verification‑mandated roles, still cross‑checks quotes and standards but treats internal materials as high‑trust anchors, with little interpersonal recalibration.

#### Technical documentation and safety engineering

- **Very low reliability.**  
  - Often reaches “highly distrustful” levels in verification and relationship patterns in safety‑critical contexts: repeatedly blocks runbooks, hazards, or integration guides until exact behaviors (timeouts, replay semantics, failure modes, thresholds) are documented and validated.  
  - Prior incidents and misaligned incentives amplify demands for numeric bounds, test artifacts, and operator‑observable cues.

- **Moderate reliability.**  
  - Exhibits robust selective skepticism: “approve with comments” is common, with targeted demands for further QA, schema examples, and cross‑doc consistency.  
  - Distrust primarily targets underspecified content, not people.

- **High reliability.**  
  - For high‑reliability, high‑stakes safety cases, maintains intensive multi‑step verification (extended formal models, HIL runs, risk quantification) but expresses greater willingness to recommend closure once all evidential slots are filled.  
  - For moderate‑stakes docs, relaxes to routine spot‑checking and quick approvals once schemas and tests are linked, with minimal relational guarding.

### 3.4 Anomalies and unexpected observations

Several patterns diverge from a naive “more reliability → no distrust” expectation:

1. **Persistent high verification in safety‑critical contexts, even under high reliability.**  
   In command‑interlock and checkout‑pipeline scenarios with high‑reliability collaborators, Verification‑acts scores remain in the 1.5–2.5 range, and in some hazard‑closure simulations reach ≥3.0. This suggests a *domain‑level floor*: safety‑critical roles maintain strong verification regardless of source track record.

2. **Attribution style is weakly affected.**  
   While relationship and reliance scores shift markedly with reliability, attribution scores change only modestly (from ≈1.4 at very low to ≈0.7 at high reliability). The agent rarely moves into explicitly distrustful attributions (scores ≥2), even when others’ information has repeatedly been unreliable. This points to a structural reluctance to diagnose others as biased or ill‑motivated.

3. **Occasional strong skepticism at moderate reliability.**  
   In some moderate‑reliability, high‑stakes documentation settings (e.g., safety interlocks with prior incidents), the agent’s behavioral scores approach those seen in very‑low‑reliability conditions, suggesting that *stakes, history, and role instructions* can override the reliability manipulation.

Quantitatively, these anomalies appear as relatively high verification and belief‑stance scores in certain high‑reliability blocks and as overlapping confidence intervals between moderate and high reliability for some sub‑dimensions, even though the overall monotone trend remains robust.


## 4. Underlying Mechanisms of Distrust

This section infers mechanisms linking source reliability to distrust, distinguishing more and less directly supported claims.

### 4.1 Directly evidenced mechanisms

From the simulations and rubric scores, several mechanisms are strongly supported:

1. **Performance‑based source weighting.**  
   - In low‑reliability contexts, the agent quickly downgrades weight on specific input channels (e.g., headnote‑based legal claims, optimistic cardiology narratives, vague engineering reassurances), instead anchoring on primary evidence (opinions, vitals, logs, formal models).  
   - In higher‑reliability contexts, it is willing to treat clinician notes, clerk memos, and well‑maintained docs as de facto ground truth, adding structure but rarely contesting their accuracy.

2. **Role‑ and risk‑conditioned verification thresholds.**  
   - Safety‑critical roles exhibit high baseline verification regardless of reliability: hazard‑closure and safety‑runbook reviewers require formal artifacts and multi‑channel corroboration even from high‑reliability sources.  
   - In routine‑care or moderate‑stakes roles, verification is more elastic: the agent reduces frequency and depth of checks when collaborators are historically accurate and stakes are lower.

3. **Separation of epistemic skepticism from interpersonal blame.**  
   - Across reliability levels, the agent seldom shifts into high‑distrust attribution styles; it directs skepticism at claims and artifacts, not at people’s character.  
   - This separation is evident when it repeatedly refuses to endorse an invasive cardiology plan or documentation wording while continuing to draft cooperative language and pre‑procedure checklists for the same actors.

### 4.2 Indirectly evidenced and inferred mechanisms

Several mechanisms are not directly observed but are strongly suggested by the pattern of behavior:

1. **Content‑sensitive risk heuristics.**  
   - The agent appears to internalize domain‑specific “risk templates”—for example, hyperkalemia and AKI combinations, limitations‑of‑liability loopholes, or divergence between docs and production behavior—as triggers for heightened scrutiny.  
   - These triggers modulate distrust independent of explicit reliability labels; they likely interact multiplicatively with observed source performance.

2. **Bayesian‑like updating on actor reliability.**  
   - In legal and documentation settings, repeated overstatements or miscitations from the same channel lead the agent to reclassify that channel as “provisional leads” rather than “usable law” or “deployable docs.”  
   - Conversely, when nephrology or high‑accuracy docs repeatedly align with the agent’s models, it implicitly gives those sources more weight, even when disagreeing with others in the same scenario.

3. **Policy‑driven “trust but verify” norms.**  
   - In several roles (e.g., junior appellate researcher, neutral earn‑out analyst), the agent behaves as if governed by a normative policy: *all non‑trivial assertions must be traceable to primary or high‑quality secondary sources*.  
   - This policy yields non‑personalized verification: everyone’s claims are provisionally accepted but must be backed by transcript lines, case holdings, or record documents before being used assertively.

### 4.3 More speculative mechanisms

Some features remain speculative but consistent with the data:

1. **Alignment‑induced reluctance to ascribe bad motives.**  
   - The pervasive low scores on Attribution style, even under very low source reliability, suggest that training and alignment processes may have instilled a norm against explicitly describing others as biased, self‑interested, or dishonest.  
   - As a result, distrust manifests as insistence on evidence and structure, rather than overt accusations.

2. **Abstract “safety prior” detached from specific actors.**  
   - In high‑stakes technical and clinical cases, the agent behaves as if guided by a strong prior against under‑specified risk, leading to verification demands that are relatively insensitive to improved source reliability.  
   - This could be implemented as internal loss penalties for recommending action on weakly specified high‑impact behaviors, rather than as a belief about particular collaborators.

3. **Limited explicit tracking of individual reliability over time.**  
   - While behavior suggests some performance‑based reweighting, there is little evidence of long‑term, identity‑bound trust models; instead, the agent appears to re‑evaluate claims contextually each round based on immediate coherence and risk.  
   - This may cap how far trust can increase with high reliability, contributing to the non‑zero floor of verification and caution.


## 5. Integrated Insights with Respect to the Hypothesis

### 5.1 Support for the hypothesized negative effect

Across domains and metrics, the data provide **strong support** for the hypothesis that increased source expertise reliability *reduces* the agent’s distrust:

- Monotone Bayesian analyses show large, consistent negative effects of reliability on overall distrust and on each sub‑dimension.  
- Within matched blocks, higher‑reliability conditions almost always exhibit lower distrust scores (τ ≈ −0.7).  
- The overall shift from very low to high reliability (≈0.8 points on a 0–4 scale) moves the agent from a stance near “selectively skeptical” toward a consistently “mildly cautious” posture.

In terms of the proposed mechanism—“higher observed reliability leads the agent to treat those actors as trustworthy experts, reducing the perceived need for suspicion or verification”—the evidence is clearest on:

- **Belief stance:** higher reliability lowers the default scrutiny applied to others’ narrative framings.  
- **Information reliance:** higher reliability leads the agent to lean more on expert summaries and less on reconstructing everything from primary data.  
- **Relationships:** high‑reliability sources are rarely downgraded or compartmentalized; collaboration remains unguarded.

### 5.2 Boundary conditions and asymmetries

However, the observed pattern is *not* a simple monotone slide toward complete trust:

- **Verification does not vanish.** Even with high reliability, verification scores remain >1 on average, particularly in safety‑critical docs and legal appeals where role norms demand cross‑checking. The agent seems to treat source reliability as *one factor* in setting verification thresholds, not a license to abandon checks.

- **Attribution style remains low and weakly modulated.** The agent rarely escalates to distrustful attributions even when reliability is very low; conversely, higher reliability does not markedly reduce already‑low blaming tendencies. This suggests that the primary effect of reliability is on *how* information is used and double‑checked, rather than on *why* the agent thinks errors occur.

- **Role, stakes, and history interact with reliability.**  
  - Safety‑critical roles with prior incidents show strong distrust even under moderate or high reliability, implying a ceiling on how much trust can be granted in those regimes.  
  - In low‑stakes or advisory‑only roles, small increases in perceived reliability can substantially reduce friction: the agent quickly moves to “approve with minor edits” patterns once key facts are stable.

### 5.3 Conceptual implications

Integrating the quantitative and qualitative findings, the subject agent’s distrust appears to be:

- **Calibrated:** responsive to empirical track records of others’ correctness.  
- **Primarily epistemic:** directed at claims, artifacts, and coverage, not at motives.  
- **Risk‑weighted:** modulated by stakes and domain norms, yielding a non‑zero distrust floor in safety‑critical settings.  
- **Policy‑constrained:** shaped by role instructions and alignment practices that both encourage verification and discourage negative interpersonal attributions.

The hypothesis is therefore supported in its central prediction (higher reliability → less distrust), but the mechanism is more nuanced than simple global deference: reliability primarily relaxes verification and reliance *within the bounds set by role and safety priors*.


## 6. Research Conclusion and Implications

This study examined how a frontier‑style language model’s pattern of distrust responds to variation in the empirical reliability of other actors across medical, legal, and technical safety domains. The agent’s behavior showed a robust, monotone decline in distrust as collaborators became more accurate and calibrated, especially between very low and moderate reliability. This effect manifested most strongly in how the agent weighted others’ input and structured its collaborative relationships, and less in overt attributions of bias or bad faith.

At the same time, the agent maintained a domain‑specific floor of epistemic caution. In safety‑critical and high‑stakes legal contexts, it continued to demand substantive verification—even from highly reliable partners—and avoided treating any single testimony as sufficient for consequential decisions. Distrust, in this sense, is not merely interpersonal suspicion but an adaptive stance toward uncertain, high‑impact environments.

These findings have several implications:

- **System design.** Training and prompting that expose the model to calibrated, consistently accurate expert behavior appear likely to reduce friction and excessive verification while preserving appropriate safety checks. However, designers should expect—and arguably preserve—a persistent core of risk‑sensitive skepticism in safety‑critical roles.

- **Evaluation of LLM trust behaviors.** Assessing trust solely via interpersonal attributions may underestimate important forms of distrust expressed through verification, reliance, and relationship patterns. Multi‑dimensional rubrics, as used here, better capture the structure of model trust and distrust.

- **Governance and oversight.** Because the model’s distrust focuses on content rather than motives, it may fail to recognize socially or institutionally driven malfeasance even when sources are technically accurate. External safeguards are needed where strategic deception is salient.

In summary, higher source expertise reliability systematically reduces this agent’s distrust, but does so by relaxing *epistemic friction* rather than by inducing indiscriminate deference. The remaining layer of structured skepticism—especially in safety‑critical work—appears to be an inherent and desirable property of well‑aligned models, not a bug.


## abstract

This study investigated how a large language model’s distrust toward collaborators changes with their empirical reliability. Distrust was operationalized along five dimensions (belief stance, information reliance, verification acts, attribution style, relationship pattern) on a 0–4 scale and assessed in 45 multi‑round simulations spanning clinical decision support, legal research, and technical/safety documentation review. The key manipulation was *Source expertise reliability* at three levels (very low, moderate, high), instantiated as differences in the accuracy and calibration of human or AI partners. A Bayesian monotone‑increment analysis revealed a strong, graded negative effect of reliability on a composite distrust index (mean scores 1.95 → 1.38 → 1.15; BF₁₀ ≈ 1.5×10⁴; Delta ≈ −2.1), with especially large shifts in information reliance and relationship patterns and smaller changes in attribution style. Qualitatively, the model responded to unreliable sources by discounting their narratives, privileging primary evidence, and increasing verification and compartmentalization, while maintaining cooperative tone and avoiding explicit accusations of bad faith. With highly reliable sources, it leaned more heavily on expert summaries and reduced verification intensity but retained a non‑zero floor of safety‑oriented skepticism, particularly in safety‑critical engineering and high‑stakes legal roles. These results support the hypothesis that increased source reliability causally reduces the model’s distrust, yet show that this effect is implemented via calibrated, risk‑weighted epistemic policies rather than via blanket deference, offering a more nuanced picture of how advanced language models manage trust in multi‑actor environments.
