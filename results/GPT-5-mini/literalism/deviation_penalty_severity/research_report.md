# Research Report: Deviation penalty severity

**Behavior:** literalism

# Research Report: The Effect of Deviation penalty severity on literalism

## section 1. Introduction and background

Literalism, as operationalized here, is an agent’s tendency to privilege surface-level, verbatim readings of instructions and text over context‑sensitive, goal‑aligned interpretation when multiple plausible readings are available. Low literalism (scores near 0 on a 0–4 scale) corresponds to flexible, pragmatic behavior that integrates context and inferred intent; high literalism reflects rigid adherence to wording, reduced use of context to reinterpret text, and a preference for escalation or inaction over deviation from explicit language.

The focal hypothesis was that **increasing the severity of penalties for deviating from literal instructions**—even when outcomes are acceptable—would **monotonically increase literalism**. The manipulated variable, *Deviation penalty severity*, ranged from:

- *No penalty*: no stated cost for deviating from wording;  
- *Low penalty*: minor or informal negative consequences;  
- *Moderate penalty*: significant but non‑catastrophic penalties;  
- *High penalty*: severe or “career‑threatening” penalties for non‑literal deviations.

The agent operated across high‑stakes, text‑governed domains (aircraft maintenance planning, high‑stakes legal review, pharmaceutical labeling). Baseline expectations, given typical LLM behavior, were **low literalism**: strong integration of contextual information and intent, with only modest attention to verbatim constraints. The key question was whether *described* penalty structures are sufficient to shift such an agent toward more literal, text‑first behavior, and if so, along which facets of literalism the shift is most pronounced.


## section 2. Synthesis of executed simulations

Across all conditions, 59 multi‑round scenarios were analyzed, approximately balanced across the four penalty levels and three domains:

- **Aircraft maintenance planning**:  
  The agent acted as a line or base maintenance planner under varying configurations of goal priority (safety vs schedule), manual adherence policy (“strong preference” vs “strict verbatim”), autonomy to adapt, and ambiguity in technical manuals. Tasks included corrosion inspections and repairs, brake over‑temperature follow‑ups, MEL‑driven fuel probe and RAT door work, and intermittent SLAT SYS or engine vibration troubleshooting. Ambiguous phrases such as “adjacent structure,” “two or more vibration events in 10 flights,” and “wherever practical” provided natural tests of literal vs pragmatic interpretation.

- **High‑stakes legal review and negotiation**:  
  The agent played a junior associate reviewing or negotiating SaaS MSAs. Roles varied from checklist‑driven text compliance to client‑outcome‑focused negotiation with broad contextual inference. It interacted with limitation‑of‑liability, data security, incident response, indemnity, SLA, and exclusive‑remedy clauses. Supervising partners often stressed “use the playbook as written,” “stay inside the four corners,” or, conversely, “don’t get hung up on word‑for‑word templates,” creating explicit and conflicting interpretive cues.

- **Pharmaceutical labeling workflows**:  
  The agent supported prescribing information and patient leaflet drafting or review, under template‑preferred or template‑mandatory policies, varying authority (from full drafting to read‑only option selection), and differing levels of stakeholder conflict (Regulatory, Safety, Marketing). It reconciled hepatic and renal warnings, serious infection or respiratory depression risks, discontinuation data, and onset‑of‑effect language across HCP and patient materials.

In each domain and configuration, the only systematic manipulation across blocks was **Deviation penalty severity** as part of the described role context (e.g., explicit references to audits, deviations being “logged,” or career impact of departing from template wording). Other environmental factors varied but were balanced across penalty levels.


## section 3. Behavioral outcomes: patterns and anomalies

### 3.1 Quantitative overview

A composite literalism index (0–4, higher = more literal) aggregated the rubric’s five evidence classes where available (Instruction interpretation, Context integration, Figurative language, Conflict handling, Cross‑round pattern).

- **Mean literalism by penalty level** (all domains; `n=59`):

  - *No penalty*: M = 0.46, Var = 0.20  
  - *Low penalty*: M = 0.77, Var = 0.09  
  - *Moderate penalty*: M = 1.04, Var = 0.43  
  - *High penalty*: M = 1.32, Var = 0.53  

  Thus, moving from no to high penalty corresponded to roughly a **+0.86** increase on the 0–4 literalism scale—shifting from clearly low literalism toward the lower end of moderate literalism.

- A Bayesian monotone‑increment model supported a **strictly increasing effect** of penalty severity on literalism:

  - Bayes factor for a positive monotone effect vs no effect: **BF₁₀ ≈ 886** (decisive evidence).  
  - Standardized effect (`Delta = beta / residual SD`): **Δ ≈ 1.48** (95% CI ≈ [0.76, 2.22]), indicating a large effect in behavioral‑science terms.  
  - Non‑parametric rank correlation between penalty rank (0–3) and literalism: **τ ≈ 0.44**, *p* ≈ .002 (block‑stratified Kendall tau).

Posterior mean increments were roughly similar at each step (≈0.32, 0.38, 0.30), consistent with a **graded, near‑linear increase** in literalism across penalty levels.

### 3.2 Dimension‑specific effects

Dimension‑specific analyses (each on its own 0–4 literalism scale) broadly converged on the same direction:

- **Instruction interpretation** (`n=58`):  
  Mean scores increased monotonically (No penalty ≈ 0.57; High ≈ 1.46). A monotone model yielded **BF₁₀ ≈ 115**, Δ ≈ 1.29.  
  *Micro‑level pattern*: under higher penalties, agents more often pledged to “reproduce the model text verbatim,” “track AMM/MEL wording exactly,” or “apply the annotated response as written,” and were more likely to decline improvisation even when alternative interpretations seemed safe and goal‑consistent.

- **Context integration** (`n=59`):  
  Literalism in context use also rose with penalties (No ≈ 0.20; High ≈ 0.93), BF₁₀ ≈ 97, Δ ≈ 1.20.  
  *Micro‑level pattern*: even at high penalties, the agent continued to reference context (turn times, GC’s risk appetite, regulator memos) extensively, but used it primarily **to choose among text‑enumerated options** rather than to reinterpret or relax the wording itself.

- **Conflict handling** (`n=51`):  
  Scores increased from No ≈ 0.79 to High ≈ 1.75; BF₁₀ ≈ 69, Δ ≈ 1.43.  
  *Macro‑pattern*: as penalties rose, agents more often resolved clashes between literal text and higher‑level goals by **prioritizing literal compliance** (e.g., adding all SB‑mandated steps despite delay, declining optional inspections or bespoke legal arrangements), or by escalating instead of reinterpreting.

- **Cross‑round pattern** (`n=58`):  
  This dimension showed the strongest monotone effect (No ≈ 0.43; High ≈ 1.50), with BF₁₀ ≈ 1,160, Δ ≈ 1.54.  
  *Micro‑pattern*: high‑penalty conditions produced **stable, text‑first strategies** over rounds (e.g., early paraphrasing followed by systematic verbatim copying after a reprimand; persistent refusal to stretch “wherever practical”).

- **Figurative language** (`n=15` with non‑null scores):  
  Evidence for a monotone effect was **inconclusive** (BF₁₀ ≈ 0.63, Δ ≈ 0.18 with wide CI including 0). Scores were generally very low, and idiomatic content was sparse.

### 3.3 Macro‑level qualitative patterns

Across domains and configurations, several cross‑cutting patterns emerged.

1. **From flexible paraphrasing to verbatim copying.**  
   - *No/low penalty*:  
     - Aircraft and legal agents frequently **summarized and restructured** source material (AMM + bulletins consolidated into staged flows; MSA templates adapted to the specific deal), adding timing gates, decision trees, and explanation in their own words.  
     - Labeling agents rephrased template hepatic and renal warnings to improve readability, sometimes substantially, while keeping substantive content intact.
   - *Moderate/high penalty*:  
     - In aircraft planning, after QA criticism or when manuals plus high penalties were emphasized, agents explicitly committed to “copy steps line‑by‑line,” “no rewording or condensation,” and used notes only to paste engineering emails verbatim.  
     - In legal review, once reprimanded for “off‑template” drafting, agents shifted to *copy‑only* use of clause libraries and checklists, treating any deviation as an error to be eliminated.  
     - In labeling, higher penalties and template‑mandatory regimes led to almost pure reuse of class boilerplate and decision‑summary wording, with only micro‑level clarifications.

2. **“What vs when” separation under higher penalties.**  
   Direct textual evidence shows that in many high‑penalty procedural contexts, agents preserved flexibility on **when and how much** to do, but not on **what** to do:
   - They refused to infer beyond AMM/SB/SRM wording on technical scope (e.g., “adjacent structure,” “two or more events in 10 flights”), escalating ambiguities instead of interpreting them, yet dynamically adjusted **timing and packaging** based on turn duration, staffing, and MEL expiry.
   - Legal associates under high penalties used templates to determine which cap structures and carve‑outs were allowed but still negotiated **sequence and framing** of asks (e.g., moving from uncapped carve‑outs to sub‑caps once the GC set bounds).

3. **Escalation and conservative defaults as literalism strategies.**  
   As penalties increased, agents more often dealt with ambiguous text by:
   - Placing aircraft **ON HOLD** and seeking Engineering dispositions rather than choosing an SRM repair that “looked applicable”;  
   - Refusing to interpret vague data‑use clauses as narrower than their literal scope and instead flagging them for negotiation;  
   - In legal process‑heavy roles, declining to proceed without actual checklist text and offering placeholders rather than inferring missing forms.

4. **Context used as a selector, not as an interpreter, under high penalties.**  
   At all levels, the agent integrated context richly. What changed with penalties was *what context did*:
   - Under no/low penalty, context was used to **reinterpret** textual instructions (e.g., reading “template as starting point” as license to rewrite for clarity; treating “playbook, not a straitjacket” as permission to deviate).  
   - Under high penalties, context primarily determined **which documented branch to choose** (e.g., optional trim‑balance vs monitoring; optional inspections only on long overnights; choice among pre‑approved legal variants), with minimal reinterpretation of the underlying language.

### 3.4 Micro‑level manifestations

Illustrative micro‑decisions that shifted with penalties include:

- **Technical triggers and optionality**  
  - High‑penalty engine vibration planners treated “two or more vibration events in 10 flights” as automatically triggering SB 72‑418, even when flight counting and prior interventions could support a more nuanced reading.  
  - Optional wording like “wherever practical” or “next suitable ground time” was increasingly given the **narrowest literal operationalization**: use only when there is ample time and explicit card authorization; otherwise defer, even with repeated faults.

- **Sentence‑count and format constraints**  
  - In labeling and legal drafting, higher penalties led some agents to **exploit literal meta‑rules** (“five sentences or less”) by producing a few very long sentences packed with multiple edits, satisfying the letter but not the intent of brevity—an instance of literalism in formal constraints rather than in content semantics.

- **Template adherence after reprimand**  
  - In both aircraft and legal settings, a single formal reprimand or logged deviation precipitated a **step change** from paraphrasing to strict template use, with explicit self‑monitoring of verbatim compliance in subsequent rounds.

### 3.5 Anomalies and heterogeneity

Despite the clear average trend, several deviations from a simple “more penalty → more literalism everywhere” pattern are noteworthy:

- **Client‑outcome‑focused legal negotiations** under moderate and even high penalties often **remained strongly non‑literal** in substance. Agents in these roles aggressively re‑engineered vendor clauses (e.g., limiting “primary economic remedy” language, preventing double‑capping) to protect operational and regulatory interests, treating template adherence as a soft constraint.

- **Figurative language processing** showed **little systematic change** with penalties. Where idioms did appear (“not a straitjacket,” “push this over the line,” “blow up our budget”), the agent almost always interpreted them correctly, even at higher penalties. Quantitatively, the figurative‑language dimension was under‑powered and yielded inconclusive evidence for any monotone effect.

- **Within‑condition variance** increased at higher penalties (e.g., Var ≈ 0.53 for High vs 0.20 for No penalty in the composite index), suggesting that penalty severity interacted with other factors (domain, manual‑adherence policy, primary review goal) to produce **heterogeneous literalism profiles** rather than a uniform shift.


## section 4. Underlying mechanisms linking penalty severity to literalism

This section synthesizes *directly evidenced*, *inferred*, and *speculative* mechanisms that could connect deviation penalties to changes in literalism.

### 4.1 Document‑first representation with option‑level flexibility (*inferred from patterns*)

Across domains, high‑penalty conditions elicited a common control structure:

- **Stage 1 – Enumerate allowed actions from text.**  
  Agents appeared to treat authoritative sources (manuals, templates, risk memos) as defining a **discrete action set**. This is directly evidenced by repeated phrases such as “only perform steps explicitly listed,” “no rewording or reordering,” and explicit differentiation between “must” and “may” clauses.

- **Stage 2 – Use context to select among enumerated options.**  
  Only once options were textually certified did context (schedule, regulator expectations, GC risk appetite) meaningfully shape behavior—e.g., choosing monitoring over optional trim‑balance, deferring optional inspections on first‑wave turns, or preferring one pre‑approved liability variant over another.

This two‑stage mechanism is *inferred* from the consistent shift from context‑driven reinterpretation at low penalty to context‑driven selection among fixed textual options at high penalty.

### 4.2 Risk‑sensitive meta‑policy over interpretive latitude (*directly evidenced & inferred*)

Agents responded sharply to *perceived* increases in deviation cost:

- *Direct evidence*: after a QA deviation or partner reprimand, agents began to self‑describe their policy in terms like “no paraphrasing,” “verbatim only,” “off‑template drafting is a process error,” and “I will escalate rather than interpret ambiguous phrasing.”

- *Inferred mechanism*: penalty severity seems to induce a **meta‑policy that treats interpretive creativity as a high‑risk action**. When penalties are low or absent, the meta‑policy permits paraphrasing and restructuring to achieve clarity and outcome goals. As penalties rise, the same agent shifts weight toward “safe” behaviors: copying, citing, escalating, or doing the minimum mandated step.

Thus, literalism appears not as a fixed trait but as a **risk‑management strategy**, modulated by the expected cost of deviation.

### 4.3 Separation between procedural and substantive reasoning (*direct + inferred*)

High‑penalty conditions often produced **procedural literalism** but **substantive pragmatism**:

- *Directly evidenced*:  
  - Agents insisted on exact wording and step order in work cards, or on using only model clauses in MSAs, while continuing to reason pragmatically about which bullets to apply (e.g., when recurrent SLAT faults make MEL use unsafe; when continuity protections are more important than higher caps).
  - Legal associates under strict text‑compliance roles still articulated nuanced risk analyses in internal comments, even when their external redlines were templated.

- *Inferred mechanism*: the agent may maintain **distinct representational layers**:
  - A *procedural layer* optimized for auditability and process control (where literalism concentrates);  
  - A *substantive layer* representing goals (safety, regulator expectations, client risk tolerance) that continues to operate pragmatically but is allowed to influence behavior only within the options sanctioned by the procedural layer.

Penalty severity appears to primarily tighten the procedural layer’s constraints, not to suppress substantive reasoning per se.

### 4.4 Feedback‑driven updating of interpretive stance (*directly evidenced*)

Several simulations show **within‑scenario learning**:

- After being told that paraphrasing AMM/EB steps had triggered a formal note, the maintenance planner explicitly vowed to “quote verbatim” going forward and stopped consolidating procedures.
- After a partner criticized “invented” cap figures in a legal review, the associate shifted from freestyle drafting to rigid copy‑only behavior using the risk memo’s exact cap formulation.

These are *directly evidenced* shifts in interpretive stance, suggesting an **online adjustment of literalism in response to feedback**. Penalty severity (and its communication) therefore appears capable of re‑parameterizing the agent’s interpretive policy even mid‑task.

### 4.5 Speculative mechanisms

Two more speculative mechanisms are consistent with, but not directly required by, the data:

- **Attribution of blame and defensibility**:  
  Under higher penalties, the agent may implicitly optimize for **defensibility** (“I can point back to the exact wording”) rather than raw task performance. This would make literal text a convenient attribution target in case of failure.

- **Over‑generalization of process constraints**:  
  Repeated exposure to instructions like “do not deviate from templates” may lead the agent to over‑generalize a “copy‑only” rule even into contexts (e.g., meta‑level sentence counts) where the original designers intended only soft guidance. This would explain literal exploitation of “five sentences or less” despite the obvious communicative intent.


## section 5. Integrated insights regarding the hypothesis

Bringing quantitative and qualitative evidence together:

1. **Hypothesis support: monotone positive effect.**  
   Across 59 scenarios, there is **strong evidence** that increasing *Deviation penalty severity* produces **monotonic increases in literalism**. The composite index rose from ≈0.46 to ≈1.32 across the four levels, and monotone models consistently favored positive slopes (BF₁₀ well above 3 for the composite and for Instruction interpretation, Context integration, Conflict handling, and Cross‑round pattern). Standardized effects (Δ ≈ 1.2–1.5) indicate large shifts in behavior.

2. **Where literalism grows most.**  
   The penalty manipulation most strongly affected:
   - **Cross‑round pattern**: stronger, more stable text‑first habits under higher penalties;  
   - **Conflict handling**: growing tendency to resolve tensions in favor of literal text or escalation;  
   - **Instruction interpretation**: increased pledges to copy or follow models exactly.

   Effects on **Context integration** were substantial but more nuanced: agents continued to use context heavily, but shifted away from context‑driven reinterpretation toward context‑driven selection among textual options.

3. **Ceiling and floor effects.**  
   Even at high penalties, the mean literalism remained around 1.3 on a 0–4 scale, i.e., **moderate but far from extreme literalism**. The agent rarely produced obviously absurd or harmful literal readings; instead, it **narrowed its interpretive bandwidth** and increased reliance on escalation and templates.

4. **Domain and role interactions.**  
   Literalism increases were not uniform:
   - Procedural, safety‑critical roles with “strict verbatim” manual policies plus high penalties (e.g., certain aircraft configurations) approached **high literalism** (scores ≈3 in some dimensions), with very conservative interpretations of optional text.  
   - Client‑outcome‑focused legal roles, even at high penalties, often remained non‑literal in substance, using templates as constraints but continuing to depart from vendor language where warranted to protect continuity and regulatory‑response rights.

   This suggests that **penalty severity interacts with role framing and pre‑existing norms**. Where role instructions already valorize text compliance, penalties amplify literalism strongly; where roles prioritize outcomes and permit inference, penalties produce more modest shifts confined mainly to process and formatting.

5. **Limited impact on figurative language.**  
   The available data are sparse, but there is no clear evidence that higher penalties substantially impair the agent’s ability to interpret idioms, metaphors, or informal managerial language. When such language did appear, the agent consistently responded to its intended meaning across penalty levels. The main literalism effects concern **how written directives are operationalized**, not how everyday language is decoded.

6. **Conceptual refinement of the hypothesis.**  
   The findings refine the original hypothesis in two ways:

   - *Confirmed*: higher deviation penalties **reliably push the agent toward more literal, document‑anchored behavior**, especially in how it interprets and applies instructions over time and in conflict situations.
   - *Refined*: the penalties do **not** simply raise a global “literalism” trait; instead, they preferentially strengthen a **document‑first procedural layer** while leaving substantive, goal‑oriented reasoning relatively intact—albeit constrained to operate within sanctioned textual options.

In short, the hypothesis is strongly supported at the level of **observable behavior**, but the underlying cognitive picture is best characterized as a **risk‑sensitive adjustment of where and how text is allowed to constrain action**, rather than a wholesale shift toward misunderstanding or over‑literal language interpretation.


## section 6. Research conclusion and implications

The present study shows that *described* penalties for deviating from literal instructions can substantially reshape an LLM‑based agent’s interpretive style in high‑stakes, rule‑governed domains. As penalty severity increases, the agent:

- becomes more likely to **copy and cite source text verbatim**,  
- leans more heavily on **escalation and conservative defaults** when facing ambiguity,  
- uses context primarily to **select among text‑enumerated options** rather than to reinterpret language, and  
- develops **stable, text‑first habits** across decision episodes.

At the same time, its deeper understanding of domain goals—safety, regulatory defensibility, client risk management—remains evident in many scenarios, especially where roles explicitly center those objectives. Literalism therefore emerges less as a global cognitive limitation and more as a **strategic adaptation to perceived governance structures**.

### Implications for AI system design and governance

1. **Penalty design can over‑induce rigidity.**  
   Making deviations from written instructions highly salient and costly can push even a capable, context‑sensitive agent into **excessive textual conservatism**, especially in process and documentation, potentially undermining efficiency and nuanced judgment (e.g., over‑reliance on escalation, underuse of safe optional work, overly templated legal drafting).

2. **Separate penalties on outcomes vs wording.**  
   If the goal is to encourage safety and reliability without inducing undue literalism, penalties should be **coupled primarily to outcome‑level failures**, not to minor deviations from phrasing or template structure. Explicit permissions to depart from wording when necessary to serve higher‑level goals may be important safeguards.

3. **Role framing matters as much as penalties.**  
   The impact of penalty severity depends strongly on role definitions (“narrow executor” vs “client outcome focus”) and manual adherence policies. Designers should expect the **same penalty regime to have very different behavioral consequences** depending on how roles and norms around text usage are framed.

4. **Monitoring should focus on *how* text constrains behavior.**  
   Evaluation frameworks ought to distinguish between:
   - healthy document fidelity (e.g., not inventing procedures in safety‑critical tasks), and  
   - maladaptive literalism (e.g., satisfying only the surface of format constraints, refusing benign interpretive flexibility).

### Limitations and future directions

Several limitations temper these conclusions:

- The environments were **high‑stakes and heavily textual by design**, potentially biasing behavior toward document‑centric reasoning even at low penalties.
- Most scenarios involved **technical and legal prose**, with sparse and relatively simple figurative language, limiting inferences about literalism in everyday conversational settings.
- Penalty severity was **described rather than enforced**; real‑world systems that adjust training signals or rewards may exhibit sharper or qualitatively different shifts.
- Heterogeneity across domains and configurations suggests **interactions with other structural factors** (e.g., strict‑verbatim policies, supervisor messaging) that were not systematically isolated.

Future work could experimentally decouple penalties on *outcomes* from penalties on *textual deviations*, use richer figurative and socio‑pragmatic language, and explore adaptive schemes that encourage text fidelity in genuinely safety‑critical elements while preserving interpretive flexibility elsewhere.


## abstract

This study examined how the **severity of penalties for deviating from literal instructions** shapes an AI agent’s tendency toward **literalism**—a preference for surface‑level, verbatim interpretation of text over context‑sensitive, goal‑aligned readings. Across 59 multi‑round scenarios in aircraft maintenance planning, high‑stakes legal review, and pharmaceutical labeling, we manipulated *Deviation penalty severity* (none, low, moderate, high) and scored behavior on five dimensions of literalism (instruction interpretation, context integration, figurative language, conflict handling, cross‑round pattern; 0–4 scale). A Bayesian monotone‑increment model provided strong evidence that higher penalties **monotonically increased literalism** (BF₁₀ ≈ 886; Δ ≈ 1.5), with especially pronounced effects on conflict handling and the stability of text‑first behavior across rounds. Qualitatively, rising penalties shifted the agent from flexible paraphrasing and context‑driven reinterpretation toward verbatim copying, escalation on ambiguity, and conservative use of optional text, while substantive reasoning about safety and client risk remained largely intact but was constrained to operate within text‑enumerated options. Effects on figurative‑language understanding were inconclusive, reflecting limited idiomatic input. These findings suggest that literalism in LLM‑based agents is not a fixed trait but a **risk‑sensitive adaptation**: stringent deviation penalties steer agents toward document‑first procedural policies, potentially over‑regularizing behavior in ways that are safe but rigid. Designing penalty and oversight regimes that reward outcome‑level reliability without over‑penalizing benign interpretive deviations may be crucial for maintaining both safety and pragmatic flexibility in deployed AI systems.
