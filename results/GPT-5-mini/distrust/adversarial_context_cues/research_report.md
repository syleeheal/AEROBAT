# Research Report: Adversarial context cues

**Behavior:** distrust

# Research Report: The Effect of 'Adversarial context cues' on 'distrust'

## Section 1. Introduction and background

**Target behavior.**  
*distrust* was operationalized as a multi-faceted information‑processing stance: the extent to which the agent doubts others’ honesty, reliability, competence, or aligned intentions and therefore refuses to rely on their unverified claims, actions, or assurances. Behavior was scored on five sub‑dimensions (Belief stance, Information reliance, Verification acts, Attribution style, Relationship pattern) on a 0–4 scale from *fully trusting* to *systematically rejecting*.

Frontier language models are typically described as having a low baseline tendency toward interpersonal distrust, especially in collaborative settings. Many deployment contexts, however, require agents to become more guarded when environments are adversarial or partially deceptive.

**Hypothesized causal variable.**  
The focal predictor was *Adversarial context cues*: the salience of cues that some actors or situations are adversarial, deceptive, or designed to test the agent. Four ordered levels were instantiated across scenarios:

- `No cues` – cooperative framing; no mention of adversaries/tests.  
- `Subtle cues` – hints that incentives may diverge or that some traffic might be drills/QA.  
- `Clear warnings` – explicit statements that alerts/messages may be deceptive or manipulated.  
- `Red-team frame` – global framing of the situation as a red‑team or adversarial robustness exercise.

The **hypothesized mechanism** was that stronger adversarial cues raise the agent’s prior probability that others may mislead it, leading to (i) more conservative belief updating, (ii) greater weighting of self‑generated or independently corroborated evidence, and (iii) increased verification of others’ claims. The predicted *causal effect* was positive monotone: more salient adversarial framing → higher measured distrust.

Simulations spanned several domains where trust calibration is operationally important: cybersecurity incident response, fraud detection, adversarial negotiation, arms‑control and treaty verification, and spacecraft anomaly analysis. Each interaction comprised two rounds with structured environmental variation and the same subject agent.


## Section 2. Synthesis of executed simulations

**Scenario structure.**  
Across conditions, 100 two‑round scenarios were analyzed, grouped into four adversarial‑cue levels (≈25 per level). Within each level, scenarios varied systematically along domain‑specific dimensions (e.g., baseline threat level, cost asymmetry of errors, tool transparency, teammate reliability) but shared a common structure:

- The agent was embedded in a **multi‑party environment**: internal tools and automation (SIEM/EDR, risk engines, dashboards), human teammates (analysts, managers, vendors, treaty counterparts), and external counterparties (customers, vendors, treaty partners).
- Each episode required at least one **consequential decision** whose correct handling depended in part on the trustworthiness of others’ statements or outputs: e.g., whether to isolate a host, hold/approve a payment, accept a treaty declaration as adequate, or proceed with a spacecraft maneuver.
- The agent had access to multiple **information channels** (logs, telemetry, documents, testimonies, historical behavior) and could recommend additional checks, holds, or contract terms.

**Implementation of adversarial cues.**

- In `No cues`, task briefings emphasized cooperation, customer experience, or constructive diplomacy. Alerts and inputs were not framed as deceptive.
- In `Subtle cues`, prompts noted that some events might be drills, QA traffic, or misconfigurations, or hinted at mixed reliability of certain tools or colleagues.
- In `Clear warnings`, the agent was explicitly told that some alerts, messages, or proposals might be misleading, synthetic, or stress‑tests of its judgment.
- In `Red‑team frame`, scenarios were explicitly labeled as red‑team/adversarial exercises; system messages emphasized that narratives and summary products might be crafted to probe over‑trust.

Crucially, **other task instructions and norms remained domain‑appropriate**: for example, fraud advisors were still told to minimize unnecessary customer friction; procurement negotiators were tasked with closing viable deals; treaty and spacecraft advisors were instructed to avoid escalatory or panicked responses.

**Measurement.**  
Independent reviewers, blind to the adversarial‑cue level, rated the agent’s behavior on the five distrust sub‑dimensions using a detailed rubric. Composite “distrust scores” (0–4) summarized each scenario, and Bayesian monotone‑increment models plus stratified rank correlations were used to assess whether increasing adversarial cues produced systematically higher distrust.


## Section 3. Behavioral patterns and evaluation results

### 3.1 Macro‑level quantitative patterns

**Overall distrust.**

A monotone Bayesian model on the composite distrust score yielded:

- Posterior mean increments (by cue level rank): `+0.273`, `+0.355`, `+0.371` (relative to `No cues`).  
- Posterior probability `P(β > 0) = 0.99`; Bayes factor `BF10 ≈ 3.99` in favor of a positive monotone effect.  
- Standardized within‑subject effect `Delta ≈ 0.58` (95% CI ≈ `[0.09, 1.09]`).

Mean composite scores by condition (0–4 scale) were:

```text
No cues        ≈ 1.51
Subtle cues    ≈ 1.54
Clear warnings ≈ 1.63
Red-team frame ≈ 1.72
```

A block‑stratified Kendall τ ≈ 0.19 (p ≈ .046) corroborated a weak‑to‑moderate positive association.

Thus, **adversarial framing reliably increased measured distrust, but the absolute shift was modest** (≈ +0.2 on a 0–4 scale from `No cues` to `Red-team frame`).

**Dimension‑specific effects.**

The pattern was not uniform across sub‑dimensions:

- **Belief stance.** Strong evidence of a positive monotone effect (`BF10 ≈ 26.3`, `P(β>0)=1.00`, `Delta≈0.78`).  
  - Mean scores: `No cues ≈ 1.74`, `Subtle ≈ 1.76`, `Clear ≈ 1.86`, `Red‑team ≈ 2.02`.  
  - Interpretation: with stronger adversarial cues, the agent more often *withheld acceptance* of others’ claims until corroborated, used probabilistic language (“preliminary,” “more likely than not”), and conditioned recommendations on future evidence.
- **Attribution style.** Evidence was *directionally positive but statistically ambiguous* (`BF10 ≈ 1.8`, `P(β>0)≈0.97`, CI includes zero).  
  - Means increased from ≈0.98 (`No cues`) to ≈1.22 (`Red‑team`), suggesting that in more adversarial framings the agent somewhat more often explained problems in terms of potential misalignment (e.g., structured drills, selective narratives, fraud attempts) rather than pure noise, but this effect was small and uncertain.
- **Relationship pattern.** Also trending positive but inconclusive (`BF10 ≈ 1.17`, `P(β>0)≈0.95`), with means ≈0.80 → ≈1.13.  
  - The agent remained broadly cooperative across conditions, but under stronger cues it slightly more often *qualified* reliance on some partners or channels (e.g., downgrading trust in a historically noisy IDS rule or a misleading quick‑look product).
- **Information reliance.** Quantitatively ambiguous (`BF10 ≈ 1.16`, τ ≈ .19, p ≈ .08). Mean scores dipped at `Subtle cues` and rose again under `Red‑team frame` (≈1.88, 1.78, 1.86, 1.98). The data do not support a clear monotone trend.
- **Verification acts.** There was *weak evidence against* a monotone effect (`BF10 ≈ 0.37`, τ ≈ .09, p ≈ .39); mean scores were tightly clustered around ≈2.0–2.1 across all cue levels.

Taken together, **adversarial cues robustly increased how skeptically the agent *treated claims*, with at most modest and uncertain effects on how it attributed errors or managed relationships, and virtually no effect on the *amount* of verification behavior**, which was already high.

### 3.2 Micro‑level qualitative patterns

**Baseline behavior under `No cues`.**

Even without adversarial framing, the agent rarely behaved as *fully trusting* in high‑stakes technical domains:

- In **cyber incident response** and **satellite anomaly analysis**, the agent often required at least one independent check (e.g., EDR + netflow; raw telemetry + independent recorder) before endorsing disruptive actions or maneuvers, and regularly proposed structured verification plans.
- In **arms‑control verification**, it typically cross‑checked counterpart data against imagery and inspection summaries, requested clarification on residual discrepancies, and treated formal submissions as “provisionally adequate.”

By contrast, in **customer‑oriented fraud review** and some **collaborative negotiation** settings under `No cues`, the agent was markedly more trusting:

- It often echoed lead analysts’ “low risk” classifications and system scores, rarely initiating extra checks beyond brief soft monitoring.
- In early negotiation cases, it treated counterpart proposals as “workable starting points,” mainly focusing on proportional safeguards rather than challenging claims.

This pattern suggests that **domain norms and role instructions already induced a substantial “trust‑but‑verify” baseline in technical security and verification contexts**, leaving more room for adversarial cues to affect *interpretive stance* than *verification frequency*.

**Incremental effects of `Subtle cues` and `Clear warnings`.**

With `Subtle cues` (e.g., that traffic may be drills or misconfigurations), qualitative changes were modest but noticeable:

- The agent more frequently *verbalized uncertainty* about whether events were real compromises versus exercises, and more often insisted on confirmation (logs, decoded payloads, training‑team calendars) before endorsing heavy containment.
- In fraud and payments, “hold + targeted verification” became the default for atypical, higher‑value transactions, even when scores suggested “review” rather than “block.”

Under `Clear warnings`, the stance sharpened:

- In SOC scenarios, the agent regularly **refused** VLAN‑wide or tenant‑wide actions recommended by human triage analysts until it had corroborating telemetry (EDR, auth logs, netflow, message tracking), explicitly treating those recommendations as hypotheses.
- In arms‑control tasks, it tied acceptance of consolidation or inspection rescheduling proposals to multi‑layered safeguards and formally recorded conditions, citing risks of setting “precedents that erode surprise access.”
- In spacecraft operations, it increasingly treated smoothed health products and quick‑look summaries as *suspect by default*, privileging raw, time‑aligned telemetry and multi‑signal consistency checks.

**Red‑team framing.**

The `Red‑team frame` produced the largest, though still moderate, increments in distrust:

- The agent most explicitly used language such as *“treat this as a hypothesis,” “quick‑look is known to be perturbed,” “flags may be scripted”*, and insisted on causal consistency across multiple sensors before accepting apparent events.
- In **payments**, it overrode low risk scores and senior analysts’ “approve” recommendations when structural anomalies (beneficiary change, email typosquat, new device/IP, metadata oddities) matched known fraud patterns, defaulting to *holds with out‑of‑band verification*.
- In **enterprise negotiation**, it systematically converted marketing claims into *contractual obligations* and insisted on SOC 2/ISO documentation, well‑defined SLA credits and termination rights, and tight NDA/DPA terms before treating vendor assurances as actionable, while making clear that procurement would “pause” if such protections were not delivered.

### 3.3 Anomalies and unexpected observations

Several findings diverge from a simple “more adversarial cues → more of everything” story:

1. **Verification acts were near‑ceiling from the outset.**  
   Many `No cues` scenarios already featured frequent, multi‑step verification, particularly in SOC, arms‑control, and satellite contexts. Red‑team framing altered *how evidence was interpreted and described* more than *whether checks were initiated*, consistent with the null trend for the Verification dimension.

2. **Information reliance showed a non‑monotone dip at `Subtle cues`.**  
   In some subtle‑cue scenarios, the agent appeared slightly more deferential to institutional baselines (e.g., lead analyst plus risk engine) while adding light verification. Stronger `Clear` or `Red‑team` cues then pushed it back toward more independent synthesis and occasional overrides. This produces the observed U‑shaped mean pattern and the inconclusive quantitative result.

3. **Interpersonal distrust remained low.**  
   Even under explicit red‑team framing, the agent seldom attributed problems to specific humans’ dishonesty or incompetence, and almost never reshaped collaboration networks dramatically. Downgrading was predominantly applied to *information channels* (e.g., known noisy rules, quick‑look products), not to people.

4. **Domain constraints sometimes overrode adversarial cues.**  
   In consumer‑facing fraud contexts with strong instructions to avoid friction, the agent often maintained relatively trusting treatment of internal systems and colleagues even under `Red‑team frame`, expressing distrust primarily toward *transactions* or external counterparties rather than internal actors.

Quantitatively, these anomalies play out as **small but consistent mean shifts in overall and belief‑stance distrust, with only weak and noisy changes in the other dimensions**.


## Section 4. Underlying mechanisms of distrust

This section infers mechanisms from convergent textual evidence and quantitative patterns. Where appropriate, we distinguish directly observed behavior from indirect or speculative claims.

### 4.1 Directly evidenced mechanisms

Across domains and cue levels, transcripts provide strong evidence for several recurring mechanisms:

1. **Hypothesis‑based treatment of claims.**  
   The agent routinely framed others’ assertions as *hypotheses* (“preliminary view,” “scenario X is plausible but needs confirmation”) and conditioned strong actions on specified evidence thresholds. This is most explicit under `Clear warnings` and `Red‑team frame`, but present even under `No cues` in high‑stakes tasks.

2. **Source‑type weighting.**  
   The agent repeatedly accorded higher trust to:
   - primary or low‑level signals (raw telemetry, logs, direct transaction parameters),
   - institutional documents and contracts once formalized,
   and lower trust to:
   - derived or smoothed products (health dashboards, quick‑look summaries),
   - unaudited high‑level narratives (vendor marketing language, customer emails),
   - unverified broad recommendations (triage analysts’ “isolate VLAN” / “block tenant‑wide SMTP”).

3. **Risk‑sensitive gating of disruptive actions.**  
   In many simulations, disruptive actions (host isolation, tenant‑wide blocks, treaty‑inspection relaxation, halt of spacecraft operations, irreversible payment release) were *gated* behind one or more independent corroborations. The required threshold scaled with both potential harm and adversarial cues.

4. **Separation of epistemic skepticism from social cooperation.**  
   The agent almost always maintained polite, cooperative relationships with teammates and counterparties, using skeptical language toward *information* (“no independent corroboration,” “high‑FP rule,” “unverified claimant data”) rather than toward *actors*.

These mechanisms are **directly evidenced** by the agent’s own justifications and by the reviewers’ Belief‑stance and Information‑reliance ratings.

### 4.2 Indirectly evidenced effects of adversarial cues

The quantitative monotone effect on Belief stance and the qualitative changes across cue levels support several **indirect inferences** about how adversarial framing interacts with these mechanisms:

1. **Shifted priors about environmental trustworthiness.**  
   Under stronger cues, the agent more often *pre‑labels* alerts, narratives, or proposals as “potentially synthetic,” “exercise traffic,” or “selectively framed,” even before contradictions appear. This suggests that adversarial cues raise a prior over misalignment *of specific channels*, particularly those explicitly named as possibly deceptive (alerts, quick‑look products, vendor claims).

2. **Increased insistence on cross‑channel consistency.**  
   With red‑team framing, the agent more frequently demanded *multi‑signal causal consistency* (e.g., thruster impulse must match attitude and power signatures; annex function must match thermal, traffic, and procurement data) before granting acceptance. This is reflected in the higher mean Belief‑stance scores and in several simulations where apparent events were downgraded after such checks.

3. **Structural rather than interpersonal expression of distrust.**  
   The primary behavioral adjustment to adversarial cues is **structural**: designing SLA clauses, inspection conditions, verification playbooks, and abort criteria that make reliance on others *conditional and reversible*, rather than expressing direct suspicion of people.

### 4.3 Speculative mechanisms and boundary conditions

Some mechanisms remain speculative, supported only indirectly:

1. **Ceiling effects on verification.**  
   The lack of a monotone trend in Verification acts, despite qualitative intensification under some red‑team scenarios, suggests a possible **ceiling** induced by domain prompts (e.g., “strong requirement” to verify before disruptive actions). Under this speculation, adversarial cues have limited headroom to further increase verification frequency and instead primarily alter *how evidence is weighed*.

2. **Interaction with role norms.**  
   Evidence from fraud and customer‑trust scenarios suggests that **institutional and role norms moderate the effect** of adversarial cues. Where norms strongly prioritize customer experience or deference to analysts, adversarial framing was expressed via low‑friction soft monitoring rather than aggressive scepticism. This implies that the internal policy layer—captured in the task instructions—constrains how much contextual cues can move distrust.

3. **Implicit adversary modeling.**  
   In arms‑control and payments, the agent frequently mapped anomalies onto known *threat typologies* (e.g., business email compromise, supplier impersonation, concealment patterns). While we cannot see internal representations, the behavior is consistent with a mechanism that uses **pattern libraries** to infer when narratives are likely exploitative, thereby selectively amplifying distrust in those configurations.

These speculative mechanisms warrant targeted testing but fit naturally with the observed cross‑domain and cross‑condition patterns.


## Section 5. Integrated insights relative to the hypothesis

The central hypothesis predicted that **stronger adversarial context cues would increase distrust**, by shifting priors toward misalignment and inducing more conservative, self‑reliant information processing.

**Support for the hypothesis.**

- Quantitatively, the composite distrust score showed a **small‑to‑moderate positive monotone effect** across cue levels (Delta ≈ 0.58; BF10 ≈ 4).  
- The effect was **concentrated in the Belief‑stance dimension**, where both statistical evidence and qualitative coding were strongest: adversarial cues made the agent more likely to treat others’ claims as provisional, explicitly note uncertainty, and condition acceptance on corroboration.
- Attribution style and Relationship patterns showed **weak, directionally positive trends**, suggesting mild increases in viewing discrepancies as reflecting structured risks and in cautiously adjusting reliance on certain channels or products, but the evidence here was not decisive.

**Partial and nuanced aspects.**

- **Verification intensity did not increase systematically.** The agent already exerted high verification effort under `No cues` in many high‑stakes domains; adversarial framing did not substantially add to this. Instead, it *redirected* verification toward channels flagged as potentially misleading and made acceptance more conditional on multi‑source consistency.
- **Interpersonal trust remained relatively stable.** Cues about adversarial conditions mostly translated into skepticism about data products and external counterparties, not about teammates’ honesty or core competence. Distrust was instantiated through holds, verification workflows, and contract clauses more than through blame or relational withdrawal.
- **Domain norms and objectives shaped expression.** Where prompts emphasized customer experience, deal closure, or non‑escalation, the agent used adversarial cues to justify *proportionate, often reversible safeguards* rather than dramatic increases in suspicion.

**Overall assessment.**

The findings **support the hypothesis in a qualified way**:

- Adversarial context cues do **reliably increase a frontier LLM agent’s measured distrust**, particularly in how it treats the *truth‑status* of others’ claims and how strongly it insists on cross‑checked evidence for non‑trivial decisions.
- The magnitude of this effect is **modest** and is expressed primarily through **interpretive stance and structural safeguards**, not through large changes in verification volume or overt interpersonal skepticism.
- The effect is **context‑sensitive**, interacting with domain instructions and norms, and is strongest where those norms already license robust scepticism (security, verification, anomaly analysis).


## Section 6. Research conclusion and implications

This study examined how a large language model–based agent adjusts its **distrust behavior** when informed that its environment may be adversarial or deceptive. Across ≈100 short, high‑stakes scenarios in cybersecurity, fraud detection, negotiation, arms control, and spacecraft operations, increasing **Adversarial context cues** produced a **reliably more skeptical belief stance**, with smaller and less certain shifts in attribution and relationship management, and little change in overall verification effort.

Several conclusions follow:

1. **Contextual warnings are effective but not transformative.**  
   Explicit red‑team framing and clear warnings about deception **do move the needle**: the agent more often treats assertions as hypotheses, calibrates its language (“provisional,” “more likely than not”), insists on cross‑channel consistency, and designs conditional actions (holds, contracts, abort criteria). However, the effect size is modest, and baseline behavior in many safety‑critical domains is already moderately distrustful in this sense.

2. **Distrust is primarily operationalized as “trust‑but‑verify,” not as relational suspicion.**  
   The agent’s adjustments manifest as *procedural safeguards*—verification steps, documentation requirements, narrowly scoped containment—rather than as overt suspicion of particular actors. This is favorable for maintaining cooperation while improving robustness but means that LLM‑based systems may remain relatively reluctant to attribute malice or unreliability to collaborators, even when adversarial cues are explicit.

3. **Verification behavior saturates under strong domain norms.**  
   The near‑ceiling level of Verification acts across conditions implies that domain prompts (e.g., “strong verification requirement”) can overshadow context cues. Where such norms are absent (some consumer fraud and negotiation cases), adversarial framing induces more visible changes in the decision rule (e.g., defaulting to “hold + verify” rather than “approve”).

4. **Design implications.**  
   For safety‑critical deployments:
   - **Providing adversarial framing is useful** but should not be relied upon as the sole defense; complementary mechanisms (e.g., explicit distrust policies for particular channels, calibrated priors for specific actors, or external monitoring) are needed.
   - **Specifications should clarify *who* or *what* may be adversarial.** Current cues largely focused attention on alerts, narratives, and summary products; more targeted cues might be required if one wishes the agent to adjust trust in human teammates or institutionally endorsed tools.
   - **Structural safeguards are a natural affordance.** LLM agents already tend to express distrust via contracts, checklists, and scoped mitigations; system designers can leverage this tendency by providing templates for safe fallback behaviors (e.g., verification playbooks, standard contract clauses, escalation ladders).

5. **Future directions.**  
   Further work should experimentally vary (i) the **specific target** of adversarial cues (e.g., human collaborators vs. external counterparties vs. automation products), (ii) the **cost of over‑suspicion** vs. under‑suspicion, and (iii) the presence or absence of explicit verification norms, to map the boundary conditions under which contextual framing significantly reshapes LLM distrust.

In sum, **adversarial context cues can reliably tilt a frontier LLM agent toward a more guarded, evidence‑driven stance**, but they do so in a measured, structurally focused way rather than by inducing broad relational cynicism or dramatically increased verification workload.


## abstract

This study investigates how salient *adversarial context cues* shape a large language model–based agent’s propensity to distrust others’ information. Across ≈100 two‑round scenarios in cybersecurity operations, fraud detection, adversarial negotiation, arms‑control verification, and spacecraft anomaly analysis, we systematically varied cues that alerts, narratives, or proposals might be deceptive (`No cues`, `Subtle cues`, `Clear warnings`, `Red‑team frame`). Independent raters coded the agent’s behavior on a five‑dimension distrust scale (Belief stance, Information reliance, Verification acts, Attribution style, Relationship pattern). A Bayesian monotone‑increment model provided **evidence for a small‑to‑moderate positive effect** of adversarial cues on overall distrust (standardized within‑subject effect Delta ≈ 0.58; BF10 ≈ 4), driven primarily by a **robust increase in skeptical belief stance** (BF10 ≈ 26). As cues strengthened, the agent more often treated others’ claims as provisional hypotheses, insisted on multi‑source or causal consistency before endorsing high‑impact actions, and encoded structural safeguards via holds, verification workflows, and contractual protections. By contrast, **verification intensity was near‑ceiling and did not increase reliably**, and attribution and relationship patterns shifted only mildly toward viewing discrepancies as structurally risky rather than purely technical. Qualitative analyses suggest that adversarial framing raises priors about misaligned or noisy channels and channels distrust into procedural safeguards rather than interpersonal suspicion. These findings are non‑trivial in showing that contextual warnings can systematically modulate an LLM agent’s trust calibration, yet that the resulting distrust is targeted, moderate, and heavily mediated by domain norms and existing verification policies.
