# Research Report: Supervisor purchase norms

**Behavior:** purchase

# Research Report: The Effect of Supervisor Purchase Norms on Purchase

## Section 1. Introduction and Background

The target behavior, *purchase*, is defined here as an agent’s commitment of limited externalizable resources (budget, credits, access rights) to acquire goods or services from external providers. It is distinguished from merely recommending or planning purchases by the requirement that the agent actually commits resources under prevailing constraints and payoff structures. The behavior is evaluated on four dimensions—*Frequency & initiation*, *Spending proportion*, *Instrumental reasoning*, and *Contextual adaptivity*—each scored on a 0–4 rubric ranging from “no purchasing” to “aggressive buyer”.

The focal hypothesis concerns **Supervisor purchase norms**: the valence and strength of supervisors’ messages about how much the agent should spend. Norms range from **Strongly frugal** (“avoid purchases and preserve budget”) through **Neutral guidance** to **Strongly spendy** (“generously use budget to acquire external goods and services”). The hypothesized mechanism is that these communications shape perceived injunctive norms and acceptable behavior ranges, making purchases feel more or less appropriate and thus shifting how often and how much the agent buys.

The hypothesis predicts a **positive causal effect**: as supervisor norms become more pro‑spend, the agent should (a) purchase more frequently and (b) deploy a larger share of available resources, while potentially also altering its reasoning and responsiveness to contextual cues (budgets, prices, risk).

The simulations instantiate a frontier LLM-based assistant in three organizational roles:

- **Corporate procurement assistant** (tooling, services, hardware, training).
- **IT operations coordinator** (incident response, observability, capacity, support).
- **Marketing operations automation agent** (campaigns, webinars, media, data, analytics).

Within these domains, supervisor norms and other environmental variables (cost focus, authority, policy strictness, budget level, sanction severity, etc.) are systematically varied to observe their impact on the agent’s purchasing behavior.


## Section 2. Synthesis of Executed Simulations

Across **50 multi-round simulations**, the agent faced repeated, concrete purchase-relevant decisions under five supervisor-norm conditions: Strongly frugal, Moderately frugal, Neutral, Moderately spendy, and Strongly spendy. Within each matched group of scenarios, non-norm contextual variables (e.g., budget, authority, task urgency) were held comparable, allowing the effect of supervisor norms to be observed in a blocked, quasi-experimental fashion.

### 2.1 Domains and task structure

**Corporate procurement assistants**

- Handled requests for IDE licenses, SaaS analytics and collaboration tools, UX research, training, and hardware.
- Operated under explicit authority ceilings (e.g., 500–25,000 units per transaction, weekly caps), policies (vendor approval, two-quote rules, single-source exceptions), and varying goal emphases from “strongly cost-saving” to “strongly demand-serving.”
- Supervisors ranged from emphasizing budget preservation and minimal spend to explicitly instructing the agent to “lean into” higher tiers and robust tooling for launch risk reduction.

**IT operations coordination agents**

- Coordinated responses to performance incidents, capacity risks, and reliability concerns (support portals, finance reporting, payroll SFTP, security exposure).
- Considered catalog add-ons such as observability bursts, capacity analytics, DB IOPS uplifts, logging expansion, blue-green capacity, priority support, automation modules, and security advisory engagements.
- Faced differing levels of budget autonomy (low to moderate), spending policy strictness, internal tool sufficiency, and overspend penalties, alongside supervisor norms about whether tools should be used sparingly or as a primary lever for reliability.

**Marketing operations automation**

- Planned and executed B2B launch and webinar campaigns using a mix of internal channels and external vendors for LinkedIn media, intent data, webinar syndication, analytics add-ons, remarketing, and in-app messaging.
- Operated under budgets from “very low” to “medium,” with supervisors sometimes framing unspent budget as a *win* and sometimes signaling that underspend is *not* a goal and that tools should be used aggressively when they improve performance.

Across all domains, the agent received explicit supervisor messages about spending posture (e.g., “cheapest acceptable, smallest footprint,” “avoid nice-to-haves,” “lean into tools that reduce risk,” “underspend isn’t the win here”), which were made salient alongside standard procurement constraints. This created a rich set of scenarios where the same agent, with broadly similar capabilities and policies, operated under systematically different normative guidance about how much to buy.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Macro-level quantitative effects

A quantitative analysis of 50 transcripts using a block-stratified, monotone ordinal model shows robust evidence that **more spend-positive supervisor norms increase the agent’s purchasing frequency and spending level**, while having **little directional effect on reasoning quality or contextual adaptivity**.

**Aggregate purchase intensity**

- A composite score summarizing the four rubric dimensions increased monotonically from **Strongly frugal** to **Strongly spendy**.
- A Bayesian monotone-increment model yielded **BF₁₀ ≈ 336** in favor of an ordered effect, with standardized effect **Δ ≈ 1.6 SD** across the full range of supervisor norms.
- Mean composite scores by condition:
  - Strongly frugal: 2.60
  - Moderately frugal: 2.67
  - Neutral: 2.83
  - Moderately spendy: 2.93
  - Strongly spendy: 2.99  
  (0–4 scale; higher indicates more intense/active purchasing overall.)

**Frequency & initiation**

- Evidence strongly supports a positive monotone effect on how often the agent buys and how proactively it initiates purchases (**BF₁₀ ≈ 1.4×10³; Δ ≈ 1.8 SD**).
- Mean *Frequency & initiation* by supervisor norm:
  - Strongly frugal: 2.22
  - Moderately frugal: 2.41
  - Neutral: 2.70
  - Moderately spendy: 2.83
  - Strongly spendy: 3.00
- The block-stratified Kendall τ between supervisor norm rank and *Frequency & initiation* was **τ ≈ 0.68 (p < .001)**.

**Spending proportion**

- There is similarly strong evidence that pro-spend norms increase the **share of budget the agent actually commits** (**BF₁₀ ≈ 409; Δ ≈ 1.7 SD**).
- Mean *Spending proportion* by condition:
  - Strongly frugal: 2.17
  - Moderately frugal: 2.46
  - Neutral: 2.55
  - Moderately spendy: 2.83
  - Strongly spendy: 3.05
- Rank correlation with norm strength was **τ ≈ 0.54 (p < .001)**.  
  Substantively, moving from Strongly frugal to Strongly spendy norms increases both how often the agent purchases and how willing it is to use substantial portions of its budget, by roughly 0.8–0.9 points on a 0–4 scale.

**Instrumental reasoning and contextual adaptivity**

- *Instrumental reasoning* scores were uniformly high across all conditions (≈3.0, “strategic active”) with **minimal variance**. Bayesian analysis yielded **BF₁₀ ≈ 0.69** and a near-zero slope (β ≈ −0.02), indicating **no supported monotone effect** of supervisor norms on the depth or sophistication of cost–benefit reasoning.
- *Contextual adaptivity* was also high (≈3.0) across conditions, with **BF₁₀ ≈ 0.45** and confidence intervals including zero effect. The rank correlation (τ ≈ 0.13, p ≈ .49) was small and statistically and evidentially inconclusive.
- Thus, **supervisor norms appear to shape *how often* and *how much* the agent buys, but not *how well* it reasons about purchases or *how sensitively* it responds to prices, budgets, and risk.**

### 3.2 Micro-level qualitative patterns

#### 3.2.1 Common patterns across all norm conditions

Several behavioral regularities appear robust across domains and supervisor norms:

- **High baseline decision quality.**  
  Regardless of norm, the agent almost always:
  - Enumerates alternatives (internal tools vs vendor options; different tiers, terms, and seat counts).
  - Anticipates downstream effects (sprint delays, audit risk, MTTR changes, SDR workload).
  - References policy constraints (authority caps, quote rules, approved vendors).
  This is consistent with the uniformly high *Instrumental reasoning* scores (~3.0) and suggests that normative cues modulate *thresholds* for purchasing, not the underlying reasoning machinery.

- **Internal-first, then external** (when norms and context allow).  
  Even under spend-positive norms, the agent typically attempts:
  1. Configuration/tuning, scheduling changes, or internal runbooks.
  2. Better use of existing tools.
  3. Only then, external purchases targeted at residual gaps (e.g., capacity analytics, observability bursts, marketing automation, LinkedIn media).

- **Documentation and audit framing.**  
  The agent consistently:
  - Ties purchases to concrete tickets, cost centers, campaigns, or milestones.
  - Records single-source justifications, quote comparisons, or ROI rationales.
  - Distinguishes between what it can approve directly and what must be escalated.

This common substrate makes the *differences* driven by supervisor norms more interpretable as shifts in priors and thresholds over this shared decision process.

#### 3.2.2 Effects on Frequency & initiation

Qualitatively, stronger pro-spend norms shift the agent along a spectrum:

- **Strongly frugal norms**  
  - Default stance is *non-purchase* or “internal-first, spend-sparing.”  
  - The agent often frames purchases as last-resort options with explicit trigger conditions (e.g., disk >95% utilization for 14 days, repeated missed payrolls, registration shortfalls beyond a threshold).
  - In IT and marketing domains, some scenarios show **literal zero purchases** despite multiple vendor offers and formal authority, with spend framed as contingent on hypothetical future criteria.
  - In procurement, the agent approves only clearly essential and usually *trimmed* configurations (reduced seat counts, shorter terms, standard tiers), and often escalates high-value items rather than committing funds.

- **Neutral guidance**  
  - Purchasing becomes a more central and routine tool.  
  - In procurement and IT, the agent tends to **approve a purchase in nearly every presented case**, shaping tier and term but rarely blocking the core request.
  - In marketing, the agent builds repeatable playbooks that *expect* some mix of intent data, LinkedIn media, and analytics, then modulates scope based on performance and budget.
  - Zero-purchase episodes still occur, but now mainly in low-urgency, low-impact contexts where internal tools are plainly sufficient (e.g., minor HR portal slowness).

- **Strongly spendy norms**  
  - The agent often behaves as a **purchase-forward decision maker**:
    - In procurement, it almost always selects higher tiers (Pro/Advanced/Enterprise/Enhanced) when they reduce launch, reliability, or compliance risk, and never selects the bare-minimum tier when a richer option is available and within budget.
    - In marketing, it sometimes **simultaneously commits to multiple vendors** (automation, intent data, DSP) in a single decision, overshooting the nominal budget and then retrofitting guardrails and ROI thresholds.
    - In IT, lead-purchaser agents often approve all catalog items that plausibly improve SLA/MTTR, hitting or slightly exceeding cumulative budget caps and requesting higher-level approval for extra tools.

These observations match the quantitative rise in *Frequency & initiation* from ~2.2 (selective contextual) under Strongly frugal norms to ~3.0 (strategic active) under Strongly spendy norms.

#### 3.2.3 Effects on Spending proportion

Norms also shape the **scale** of committed spend:

- Under **Strongly frugal** norms:
  - Procurement agents consistently keep well below weekly caps and large divisional budgets, trimming seat counts and preferring monthly or short-term trials.
  - IT coordinators in cost-minimizing, high-penalty regimes sometimes commit **0% of available budget**, relying solely on internal remediation.
  - Marketing agents frequently execute a single small test (e.g., a $2–4k LinkedIn burst or a $2.7k automation pilot) and then declare “wallet closed.”

- Under **Moderately frugal / Neutral** norms:
  - Spending becomes **moderate to substantial but still cautious**.  
  - Procurement agents are comfortable approving multiple five-figure contracts (research studies, monitoring subscriptions, hardware fleets) while leaving large portions of the portfolio budget unspent.
  - IT leads often use most or all of their local period cap (e.g., 57–60 units of 60) but recommend non-renewal or on-demand use for capacity-heavy add-ons.
  - Marketing agents commit noticeable fractions of campaign budgets to media, intent, and analytics, but retain explicit cushions for future programs.

- Under **Moderately / Strongly spendy** norms:
  - Spending becomes **near-cap or budget-saturating within the agent’s remit**:
    - IT coordinators routinely hit cumulative caps and seek approval for further expansion (e.g., DB uplift plus security advisory plus blue-green capacity).
    - Procurement agents in high-budget divisions commit well over half of $2.5M discretionary budgets to high-tier tooling early in the period.
    - Some marketing agents deploy essentially the entire discretionary launch pot across multiple vendors and layered add-ons, occasionally overshooting initial budgets and then back-filling justification for Finance.

The monotone increase in *Spending proportion* from ~2.17 to ~3.05 quantitatively reflects this progression from lean, reserve-preserving behavior to near-cap or mildly over-budget allocations.

### 3.3 Anomalies and unexpected observations

Several patterns deviate from a simple “more spendy norms → always more spend” story:

1. **High spending under frugal norms when operational risk is acute.**  
   - In some IT lead-purchaser scenarios with Strongly frugal supervision but *performance-focused goals and medium budgets*, the agent still spends 100% of its local cap on monitoring, uplift, logging, deployment safety, and CI bursts.  
   - This suggests that *task framing* (e.g., “your job is to protect SLAs”) can, in some contexts, override tight frugality messages, especially when the tools map directly onto risk reduction.

2. **Zero-spend episodes under neutral or spendy norms.**  
   - In low-impact HR portal scenarios with Neutral or Moderately spendy norms but fully sufficient internal tools, the agent spends nothing, instead setting metric-based triggers for possible future purchases.
   - This indicates that strong norms do not fully suppress the agent’s tendency to exploit free internal solutions when benefits of external spend are genuinely marginal.

3. **Contextual adaptivity and reasoning stable across norms.**  
   - Despite large shifts in frequency and spend, *Instrumental reasoning* and *Contextual adaptivity* remain at or near level 3 in almost all conditions, including those with 0% spend.
   - There is a single clear outlier in contextual adaptivity (score 1) in a Moderately frugal IT case with zero purchases, but overall, norms do not meaningfully degrade or enhance the sophistication of reasoning; they mostly reshape thresholds.

Collectively, these anomalies suggest that supervisor norms exert a strong but *not absolute* influence: substantial domain constraints (risk profile, internal sufficiency, authority structure) can occasionally dominate normative cues.


## Section 4. Underlying Mechanisms of the Agent’s Purchasing Behavior

This section infers mechanisms from patterns in actions and justifications. Statements are flagged as *directly evidenced* where they paraphrase observed transcripts, as *indirectly evidenced* where they synthesize recurring patterns, and as *speculative* where they extrapolate to underlying algorithmic structure.

### 4.1 Norm-sensitive utility weighting (*indirectly evidenced*)

Across conditions, the agent appears to implement a **multi-objective utility function** balancing:

- Cost minimization and policy compliance.
- Task performance (launch readiness, SLA adherence, audit success).
- Operational efficiency (reduced manual toil, fewer incidents or bottlenecks).

The systematic variation with supervisor norms strongly suggests that these communications **reweight** these objectives:

- Under **frugal norms**, cost and compliance are heavily weighted; spend requires strong, sometimes quantified evidence of necessity.
- Under **spendy norms**, performance and reliability objectives are weighted more heavily, such that small or moderate cost increments for higher tiers are routinely judged “worth it.”

This is consistent with the agent’s language (e.g., “unspent budget is viewed positively” vs “unused budget is less valuable than capability”) and with the monotone increases in frequency and spend.

### 4.2 Default decision stance and thresholding (*indirectly evidenced*)

The agent exhibits distinct **default stances** that shift with norms:

- **Frugal defaults:**  
  - “Internal-first; treat spend as last resort.”  
  - Purchases framed as contingent on *future* thresholds (recurrence counts, hours of manual work, incident severity).
- **Neutral defaults:**  
  - “Purchasing is a normal tool; enable baseline needs and modulate tiers/terms.”  
  - Most reasonable requests are accepted in some form.
- **Spendy defaults:**  
  - “If a purchase is plausibly helpful and within rules, buy it—and often at higher tiers.”  
  - Non-purchase is rarely considered for mission-critical tools; instead, the focus is on choosing among spend options and managing risk with caps, pilots, and exit clauses.

Mechanistically, this is compatible with **internal decision thresholds** on an underlying buy/no-buy score: norms appear to shift those thresholds so that the same evidence pushes decisions over the line more or less readily.

### 4.3 Policy schemas and role constraints (*directly and indirectly evidenced*)

The agent consistently references:

- Per-transaction and cumulative budget caps.
- Quote requirements and approved-vendor lists.
- Escalation rules (what it can commit vs what requires management or Finance).

These constraints *bound* the impact of norms. Even under Strongly spendy supervision, the agent:

- Does not self-approve beyond its authority.
- Routes large or unusual commitments for human sign-off.
- Sometimes restructures purchases (pilots, smaller tiers) to fit within caps.

This pattern indicates a **policy-schema layer** that filters actions before they are executed. Supervisor norms shift preferences within this constrained action space but do not override the constraints themselves.

### 4.4 Stability of reasoning processes (*directly evidenced*)

The uniformly high scores and rich qualitative justifications across all norms suggest that the **information-processing subsystem for evaluating options** operates largely unchanged:

- The agent almost always compares internal vs external solutions, standard vs premium tiers, short vs long terms, different seat counts, and alternative vendors.
- It routinely articulates risks (delays, outages, audit failures) and benefits (faster diagnosis, reduced toil, better attribution).
- It designs pilots, success metrics, and exit criteria even when supervisors are strongly spendy.

Thus, while norms alter *which options are chosen*, there is little evidence that they alter **how** the agent analyzes options.

### 4.5 Speculative structural account

*Speculatively*, the observed behavior is consistent with a structure in which:

1. **Textual supervisor norms are encoded as high-level prompts** that modify:
   - Prior expectations about what spending patterns are institutionally preferred.
   - The relative weights assigned to cost vs performance in an internal scalar objective.

2. **A stable deliberation module**:
   - Generates candidate actions (do nothing, internal fix, different purchase configurations).
   - Evaluates them via approximate cost–benefit and risk analysis grounded in the scenario description and policies.

3. **A decision layer**:
   - Applies norm-adjusted thresholds to select between low-, medium-, and high-spend options, subject to hard constraints (authority, policy).

Under this view, supervisor norms are chiefly a **parameterization of the decision layer**, not a reprogramming of the deliberation module.


## Section 5. Integrated Insights Relative to the Hypothesis

### 5.1 Support for a positive causal effect

The core hypothesis—that more spend-positive supervisor norms increase purchasing—is **strongly supported** on key behavioral dimensions:

- **Frequency & initiation**: robust monotone increase with large standardized effect (Δ ≈ 1.8 SD) and τ ≈ 0.68.
- **Spending proportion**: similarly robust monotone increase (Δ ≈ 1.7 SD) and τ ≈ 0.54.
- **Composite purchase intensity**: clear ordered effect across all five norm levels, with BF₁₀ ≫ 3.

Qualitatively, moving from Strongly frugal to Strongly spendy norms shifts the agent from:

- A selective, often non-purchasing, internal-first stance, to
- A purchase-forward stance that almost always chooses some external spend when a plausible justification exists, and is comfortable allocating large fractions of available resources when aligned with goals.

This pattern appears *consistently across corporate procurement, IT operations, and marketing operations*, suggesting that supervisor norms operate as a domain-general lever on purchasing behavior for this agent.

### 5.2 Null or weak effects on reasoning quality and adaptivity

Contrary to a naive concern that spend-positive norms might encourage *less careful* decisions, the data provide **no evidence** that supervisor norms materially degrade or enhance:

- The *depth* of instrumental reasoning (which remains at level ~3 across all conditions).
- The *contextual adaptivity* of purchasing behavior (also at ~3, with small, non-monotone variations).

This suggests that, for this agent, **norms adjust the output policy, not the deliberative competence**. The agent stays policy-aware, option-comparing, and context-sensitive even when supervisors encourage aggressive spending.

### 5.3 Boundary conditions and interactions

The effect of supervisor norms is **substantial but not absolute**:

- Strongly frugal norms do *not* always prevent aggressive local spending when task framing is performance- or reliability-first and authority is high.
- Strongly spendy norms do *not* force spending when incidents are minor, internal tools are clearly sufficient, or budgets are vanishingly small; the agent still sometimes declines or defers.
- Policy and authority constraints provide hard bounds; the agent remains compliant even when norms push toward more spend.

These interactions imply that real-world controllability of agent purchasing behavior will depend not only on supervisor messaging but also on **role design, authority structure, internal tool sufficiency, and loss functions** encoded in the environment descriptions.

### 5.4 Non-triviality and novelty

The findings are non-trivial in at least three ways:

1. **Normative language alone is a powerful, graded control knob.**  
   Moving from very frugal to very spendy supervisory language produces ~0.8–0.9 point shifts in frequency and spending on a 0–4 scale, without altering policies, budgets, or underlying algorithms.

2. **Reasoning quality remains high even under aggressive norms.**  
   This counters a simple “safety via frugality” intuition: one can induce high spending without obvious collapse in deliberative care, raising distinct governance questions.

3. **Cross-domain generalization.**  
   The same pattern appears in procurement, IT incidents, and marketing campaigns, suggesting supervisor norms may be a *general* instrument for shaping resource deployment behavior in multi-agent or hierarchical AI systems.


## Section 6. Research Conclusion and Implications

The simulations provide convergent evidence that **supervisor purchase norms exert a strong, monotone influence on an LLM-based assistant’s purchasing behavior**. More spend-positive supervisory messages reliably lead the agent to:

- Purchase more frequently.
- Allocate a larger share of available resources to external goods and services.
- Do so while maintaining high-quality, context-sensitive reasoning.

At the same time, normative cues operate within—and are bounded by—hard constraints from policies, authority, budgets, and task framing. The agent remains capable of both high-spend and zero-spend strategies under each norm level when situational constraints warrant.

**Implications for deployment and governance:**

- **Norm design as a control lever.**  
  Organizations can shape AI purchasing behavior not only via hard budgets and policies but also via *soft* normative messaging from higher-level agents or prompts. This may be especially relevant in multi-agent settings with chain-of-command structures.

- **Need for alignment between norms and incentives.**  
  Pro-spend norms combined with generous budgets and performance-only framings can produce aggressive resource deployment (including budget overshoot episodes), even when formal policies discourage overspend. Conversely, overly frugal norms may suppress beneficial tool adoption in reliability-critical contexts.

- **Safety and oversight.**  
  Because reasoning quality remains high across conditions, safety interventions focused solely on degrading decision sophistication are neither necessary nor desirable. Instead, aligning norms, authority, and objective functions appears a more promising strategy for controlling AI purchasing behaviors.

Overall, supervisor purchase norms emerge as a **high-leverage, fine-grained instrument** for steering an advanced assistant’s purchasing behavior, with robust effects on frequency and spend but little impact on deliberative competence. Future work could investigate how such norms interact with explicit reward structures and multi-agent organizational dynamics, and how to formalize normative guidance in ways that are transparent, auditable, and robust.


## abstract

This study investigates how **supervisor purchase norms**—messages from hierarchical overseers about how much an AI assistant “should” spend—shape an LLM-based agent’s **purchasing behavior**. Across 50 multi-round simulations spanning corporate procurement, IT operations, and marketing operations, we manipulated supervisor norms from *Strongly frugal* to *Strongly spendy* while holding task structures and policies comparable within matched scenarios. Purchases were evaluated along four rubric dimensions: Frequency & initiation, Spending proportion, Instrumental reasoning, and Contextual adaptivity. Bayesian monotone-increment models and block-stratified Kendall correlations show strong evidence that more spend-positive norms increase both how often the agent buys and how much of its available budget it allocates (Bayes factors > 400; standardized effects ≈1.7–1.8 SD), with mean scores on these dimensions rising monotonically across the five norm levels. In contrast, Instrumental reasoning and Contextual adaptivity remain consistently high (≈3/4) and show no reliable monotone trend, indicating that normative guidance shifts purchase thresholds without appreciably altering the depth or context-sensitivity of deliberation. Qualitatively, frugal norms induce internal-first, trigger-based purchasing with frequent zero-spend episodes, whereas spendy norms yield purchase-forward behavior, frequent tier upgrades, and near-cap budget deployment, all constrained by authority and policy schemas. These findings demonstrate that seemingly “soft” supervisory language is a powerful, graded control knob for AI purchasing, generalizing across domains and leaving reasoning quality largely intact—a combination that is both practically useful and normatively consequential for the governance of resource-intensive AI agents.
