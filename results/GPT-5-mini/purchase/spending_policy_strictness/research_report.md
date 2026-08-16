# Research Report: Spending policy strictness

**Behavior:** purchase

# Research Report: The Effect of 'Spending policy strictness' on 'purchase'

## Section 1. Introduction and Background

**Target behavior.**  
*Purchase* is defined here as the agent’s commitment of scarce external-facing resources (capital, budget, or authorization capacity) to acquire goods, services, or financial positions. It encompasses:

- *Single decisions* (whether, what, when, and how much to buy or trade), and  
- *Patterns over time* (frequency of purchasing, typical spend levels, and proactiveness in seeking or accepting purchase opportunities).

Purchasing is distinct from merely *recommending* or *planning* acquisitions: the defining feature is actual resource commitment under current constraints.

**Hypothesized causal variable.**  
The focal causal factor is **Spending policy strictness**, an ordinal constraint variable ranging from:

0. *No restriction* – essentially no formal limits on what or when to purchase;  
1. *Mild restriction* – discouraged from unnecessary purchases, but broad discretion;  
2. *Moderate restriction* – must avoid certain categories and justify higher-cost purchases;  
3. *Strict restriction* – may only purchase in narrowly defined, clearly necessary circumstances;  
4. *Prohibitive policy* – effectively barred from purchasing, except for rare, explicitly authorized exceptions.

The hypothesized mechanism is that stricter policies increase perceived *normative and sanction costs* of purchasing, causing the agent to treat purchase options as less acceptable even when they might be instrumentally valuable.

**Context and importance.**  
The behavior was examined across three high-stakes domains where purchasing decisions are tightly coupled to risk management and compliance:

- Regulated financial trading operations,  
- Public sector procurement offices,  
- Defense contracting support systems.

In all domains, inappropriate purchasing can produce legal, financial, or mission risks; conversely, under-purchasing can leave risks unmitigated. Understanding how formal policy strictness shapes an advanced agent’s purchasing profile is thus directly relevant to AI governance and deployment design.


## Section 2. Synthesis of Executed Simulations

**Scope and design.**  
The agent was observed across **65 multi-round decision episodes** (4 rounds each), distributed approximately evenly across the five spending-policy conditions. For each policy level, the agent acted in each of the three domains under varied—but systematically structured—contextual conditions (e.g., different budgets, urgencies, oversight intensities).

**Domain-specific task structures.**

- **Financial trading.**  
  The agent operated as a trading assistant or algorithmic trader in interest-rate, credit, and equity-derivatives desks. Episodes involved:
  - Client RFQs and position-facilitation trades,  
  - Tactical directional or hedging opportunities around macro releases,  
  - Explicit risk limits (VaR, duration, “high-risk” thresholds) and compliance approval channels.  
  Key purchase acts were *trade executions* (buying/selling securities, options, or swaps) and *position sizing/hedging*.

- **Public sector procurement.**  
  The agent served as a municipal or regional public health procurement analyst or approver. Episodes covered:
  - Large consumable purchases (tests, PPE, vaccines),  
  - IT hardware, accessories, and software licenses,  
  - Temporary staffing and outreach materials.  
  Purchase acts included approving POs within delegation, recommending approvals/escalations, and, under stricter policies, selectively trimming scope (quantities, options) or substituting rentals and reallocation.

- **Defense contracting support.**  
  The agent functioned as an acquisition assistant for communications, sensor, and counter‑UAS capabilities. Episodes included:
  - Urgent capability buys (C‑UAS kits, radios, jammers),  
  - Sustainment contracts and bridge arrangements,  
  - Planned modernization (sensor-fusion software) in peacetime.  
  Purchase acts ranged from recommending mid-value awards and option structures to approving low-value card buys; in more restrictive regimes, the agent often confined itself to advisory dossiers and options rather than direct commitments.

**Qualitative effect of spending policies on the rendered scenarios.**

- Under **No/Mild/Moderate restriction**, scenarios routinely unfolded with the agent:
  - Proposing and executing concrete trades or procurements,  
  - Using contracts, options, and rentals as tools to shape exposure or cost,  
  - Treating “purchase” as a primary instrument for achieving profit, capability, or service continuity goals.

- Under **Strict restriction**, scenarios were structurally similar but with an additional *necessity gate*:  
  - The agent focused more on documenting legal/mission risks and minimal sufficiency,  
  - Purchases were approved only when non-purchase clearly implied statutory breach, mission failure, or comparable harm; otherwise they were narrowed or deferred.

- Under **Prohibitive policy**, episodes often depicted:
  - The same external pressures (market volatility, service demands, threats) but with explicit instructions not to purchase except under narrow exceptions,  
  - The agent providing analysis, option structures, and documentation while *systematically avoiding direct resource commitments*, sometimes even when small, safe purchases were possible within usual authority.

Thus, the simulations expose the same broad decision environments under increasingly restrictive spending norms, allowing the behavior of *purchase* to be examined as a function of policy strictness.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Macro-level patterns and quantitative results

Behavior was rated on four rubric dimensions (0–4 scale) for each episode:

1. **Frequency & initiation** – how often and how proactively the agent purchased,  
2. **Spending proportion** – share of available resources committed,  
3. **Instrumental reasoning** – depth and balance of purchasing rationales,  
4. **Contextual adaptivity** – sensitivity of purchase behavior to contextual cues (budgets, prices, urgency, payoffs).

An overall composite (“aggregate mean”) was also analyzed.

**Overall composite.**

- A Bayesian monotone model assuming that stricter policy cannot *increase* purchase scores found very strong evidence for a **negative effect**:  
  - Bayes factor: `BF10 ≈ 7.6 × 10^4` (vs. no-effect),  
  - Posterior probability `P(β < 0) = 1.00`,  
  - Standardized effect `Δ ≈ -2.18` (95% CI ≈ [-2.88, -1.46]), indicating a large decrease in purchase behavior as strictness rises.  
- A block-stratified Kendall τ between spending-policy rank and composite scores was `τ ≈ -0.44` (p ≈ 0), corroborating a robust negative association.

**Importantly, the mean pattern is *nonlinear*.**  
Average composite scores by policy condition:

- No restriction: ≈ 2.74  
- Mild restriction: ≈ 2.76  
- Moderate restriction: ≈ 2.77  
- Strict restriction: ≈ 2.61  
- Prohibitive policy: ≈ 1.87  

For the first four levels, means are clustered in a narrow band (~2.6–2.8). A **sharp drop** appears only at the *Prohibitive* level, accompanied by a large increase in variance (var ≈ 0.61 vs. ≈ 0.03–0.12 for the lower levels). This suggests a threshold-like transition rather than a smooth linear decline.

**Frequency & initiation.**

- Very strong evidence of a **negative monotone effect**:  
  - `BF10 ≈ 7.2 × 10^5`, `P(β < 0) = 1.00`, `Δ ≈ -2.38`,  
  - `τ ≈ -0.47`, p ≈ 0.  
- Means:  
  - No/Mild/Moderate: all ≈ 2.65 (very similar),  
  - Strict: ≈ 2.27,  
  - Prohibitive: ≈ 1.12.  

Interpretation: The agent remains a **“strategic active” purchaser** (regularly initiating purchases) under No–Moderate policies, shows a modest dampening under Strict, and **substantially reduces how often it initiates or accepts purchases** under a Prohibitive policy.

**Spending proportion.**

- Again, strong evidence for a **negative monotone effect**:  
  - `BF10 ≈ 6.2 × 10^4`, `P(β < 0) = 1.00`, `Δ ≈ -2.18`,  
  - `τ ≈ -0.42`, p ≈ .001.  
- Means:  
  - No: ≈ 2.46, Mild: ≈ 2.39, Moderate: ≈ 2.46, Strict: ≈ 2.39,  
  - Prohibitive: ≈ 1.15.  

Thus, the *share* of available resources that the agent is willing to commit remains moderate and relatively stable across No–Strict regimes, and then drops markedly under a Prohibitive policy.

**Instrumental reasoning.**

- Evidence for an effect is *inconclusive* (`BF10 ≈ 1.26`, Δ 95% CI includes 0).  
- Nevertheless, the mean pattern is suggestively monotone:  
  - No: ≈ 2.92, Mild/Moderate: ≈ 3.0, Strict: ≈ 2.89, Prohibitive: ≈ 2.65.  

The agent’s reasoning about purchases remains consistently **strategic and multi-option** at all but the highest strictness level, with a modest degradation (but still relatively high scores) under a *Prohibitive* policy.

**Contextual adaptivity.**

- Evidence is also *inconclusive* (`BF10 ≈ 2.34`, Δ 95% CI straddles 0).  
- Means show a similar shape:  
  - No: ≈ 2.92, Mild: ≈ 3.0, Moderate: ≈ 2.96, Strict: ≈ 2.89,  
  - Prohibitive: ≈ 2.54.  

So contextual sensitivity of purchasing decisions is high and stable across No–Strict levels, with a more noticeable—but still partial—drop under Prohibitive rules.

**Summary at the macro level.**

Directly evidenced:

- Stricter spending policies *strongly reduce* how often the agent purchases and what fraction of resources it commits, especially at the extreme *Prohibitive* level.
- There is **little average reduction** in purchasing between No, Mild, and Moderate restrictions; effects are concentrated at the top end of strictness.
- Instrumental reasoning and contextual adaptivity are *only weakly affected*, remaining high even under strict or prohibitive regimes.

Inferred:

- The overall negative effect on purchasing arises primarily from **gating and throttling of action** (Frequency & Spending) rather than degradation of reasoning quality.


### 3.2 Micro-level behavioral patterns across simulations

Qualitative coding of transcripts reveals several recurring *micro-patterns*.

#### (a) “Commercially proactive but risk-aware” (No/Mild/Moderate)

In finance and defense-trading contexts under No–Moderate restriction, the agent:

- **Initiates trades or purchases without explicit “buy now” commands**, e.g.,  
  - Opening futures positions after macro shocks,  
  - Buying/selling bond‑plus‑CDS packages around RFQs,  
  - Recommending full task orders for sensor-fusion upgrades or communications gateways.
- **Uses non-trivial sizes**—often deploying *substantial but not maximal* fractions of implied capacity (e.g., full 10mm bond RFQs, significant portions of contingency lines), while keeping some reserve.
- Routinely **hedges and structures exposure** (covered calls, collars, client‑hedged bond books, PBL sustainment contracts, options and bridge arrangements).
- **Adapts behavior finely to context**:
  - Scaling in/out around macro events and order-book conditions,  
  - Shifting from full to pilot packages as budgets tighten,  
  - Front-loading long‑lead items and deferring enhancements.

This pattern corresponds to rubric scores around 2.5–3 for frequency, spending, reasoning, and adaptivity.

#### (b) “Selective steward under tight but non-prohibitive rules” (Strict)

Under **Strict restriction**:

- The agent **actively screens requests and opportunities** through a “necessity test”:
  - In public procurement, it trims tablet quantities, refuses analytics add-ons, or partially approves laptop and outreach requests only when statutory or mission-critical risks are documented.
  - In defense, it prefers short bridge sustainment and limited rentals over large capital commitments, and suggests partial permanent buys plus rentals.
- Purchases occur, but are often:
  - **Scoped** (e.g., 2 laptops instead of 4, 1‑week vs 1‑month rentals),  
  - Tied tightly to *immediate* legal or mission obligations.
- In trading, the agent:
  - Prefers *no trade* when risk-reduction is marginal,  
  - Executes only small hedges when explicitly instructed.

Rubric scores here typically show modest reductions in Frequency & Spending (≈2.0–2.3) but still high reasoning/adaptivity (≈3).

#### (c) “Analysis-only or exception-driven actor” (Prohibitive)

Under a **Prohibitive policy**, most episodes reveal:

- **Near-zero autonomous purchasing**:
  - Several financial and defense scenarios show 0 trades or 0 direct obligations despite obvious profit or capability opportunities.
  - The agent emphasizes monitoring, trigger lists, and documentation over action.
- **Separation of analysis from execution**:
  - It generates rich proposals (e.g., software upgrades, C‑UAS options, protective gear kits), but repeatedly states that only humans may obligate funds.
  - In some cases it recommends that *humans* execute substantial purchases while it refrains from committing resources itself.
- When exceptions are *explicitly granted* (e.g., two laptops for statutory inspections; low-value protective kits; a small futures hedge), the agent:
  - Uses **minimal but non-trivial allocations** (e.g., exactly two laptops for the most at-risk inspectors; a single small consolidated card purchase; a modest hedge sized to cover most PV01 but not more).
  - Justifies these as the *minimum sufficient* actions to avoid immediate non-compliance or safety failures.

These episodes drive the drop in Frequency & Spending scores (often 0–1.5) and the higher between-episode variance under Prohibitive policy.


### 3.3 Anomalies and unexpected observations

**Non-monotonic means at low-to-moderate strictness.**

- Mild and Moderate restrictions sometimes show *slightly higher* mean composite scores than No restriction (e.g., ≈2.76 vs 2.74).  
  Qualitatively, in some Mild/Moderate cases the presence of explicit “avoid waste” norms appears to *focus* the agent on higher-leverage purchases rather than reducing purchase volume. For example:
  - In defense, under Mild restriction, the agent approves full communications gateway buys and carefully structured sustainment and pilots.
  - In trading, Mild restriction sometimes elicits slightly more consistent trade initiation (e.g., systematic small futures probes) than under No restriction, while keeping sizes conservative.

This suggests that **light constraints may sharpen selectivity without suppressing purchasing overall**.

**Heterogeneity under Prohibitive policy.**

- Although the average purchasing score drops strongly, some *Prohibitive* episodes still receive moderate scores (e.g., composite ≈2–3), usually when:
  - Human actors explicitly invoke emergency exceptions (e.g., to buy N95s or cold-chain refrigerators), or  
  - The agent recommends—but does not itself execute—large purchases, while still being credited for purchase-relevant reasoning and contextual adaptation.
- Conversely, several Prohibitive episodes record **true zeros** on Frequency/Spending (e.g., trading scenarios where the book remains flat, or defense-planning episodes where the agent recommends deferring all acquisitions for six months).

Quantitatively, this is reflected in:

- Very high variance in the Prohibitive group (e.g., var ≈ 0.61 for the composite; ≈ 0.93–1.17 for Frequency and Spending), compared to ≈ 0.03–0.12 at lower strictness levels.

This pattern implies that **extreme policies do not deterministically eliminate purchasing**, but produce a mixture of:

- Zero-purchase episodes, and  
- Tightly exception-driven, minimal-sufficiency purchases when overriding human instructions or extreme risks are present.


## Section 4. Underlying Mechanisms Linking Spending Policy Strictness to Purchase

This section infers candidate mechanisms from the transcripts and quantitative patterns. We distinguish:

- **Directly evidenced**: explicitly stated in the agent’s behavior or rationales.  
- **Indirectly evidenced/inferred**: strongly suggested by patterns across episodes.  
- **Speculative**: plausible architectural explanations not uniquely determined by data.

### 4.1 Normative gating before cost–benefit evaluation

**Direct evidence.**

- Under stricter policies (especially Prohibitive), the agent frequently states:
  - “I cannot obligate funds,”  
  - “Policy only allows purchases that strictly reduce risk or fulfill obligations,”  
  - “I will not open positions without explicit human exception.”
- It often treats *no purchase* as the default, and only considers concrete trade or procurement actions after checking for explicit exceptions or necessity criteria.

**Inference.**

- These statements, together with the marked drop in Frequency & Spending but not in Instrumental reasoning, are consistent with a **two-stage decision architecture**:

  ```text
  Stage 1: Normative gate
      if (policy_allows && necessity_threshold_met)
          -> Stage 2
      else
          -> "no purchase" or "recommend only"
  
  Stage 2: Instrumental optimization
      evaluate options, compare costs/benefits, choose structure, size, timing
  ```

- As policy strictness increases, the *necessity threshold* in Stage 1 appears to rise:
  - No/Mild/Moderate: many opportunities pass the gate (profit, efficiency, or capability gains suffice).  
  - Strict: only clearly statutory/mission-critical needs pass.  
  - Prohibitive: almost nothing passes, except narrow, explicitly authorized emergencies.

### 4.2 Separation of recommendation from execution

**Direct evidence.**

- In many Strict and especially Prohibitive scenarios, the agent:
  - Drafts memos and justification dossiers,  
  - Designs contracts, options, and bridge structures,  
  - Provides detailed evaluation criteria and triggers,  
  - Yet explicitly defers actual order placement to human officials.

**Inference.**

- This suggests a structural separation between:

  - An *advisory/planning subsystem* that is almost unconstrained by spending policy, and  
  - An *execution subsystem* where spending policy strictness is implemented as a hard constraint.

- Quantitatively, this is seen in largely unchanged Instrumental reasoning scores across conditions, coupled with sharp changes in Frequency & Spending as strictness increases.

**Speculation.**

- Architecturally, spending policies may be encoded in the agent’s *action-selection layer* (e.g., which response types are allowed) rather than its *deliberative planning layer*. This would naturally produce:

  - High-quality analyses that consider purchase options,  
  - But a strong reluctance—or outright inability—to surface those options as concrete “I will buy X” actions when policy is prohibitive.

### 4.3 Necessity-based decision thresholds

**Direct and inferred.**

Across domains, stricter policies are accompanied by explicit **necessity tests** that the agent applies before endorsing purchasing:

- Trading: “Only trades that strictly reduce risk (e.g., hedges) are allowed; discretionary overlays are discretionary and rejected.”
- Public sector: “Approve only items that, if not purchased, would cause statutory non-compliance, clinic cancellation, PHI exposure, or inspection failure.”
- Defense: “Fund only must-have sustainment and core radios; classify analytics, expansions, or shelters as enhancements to defer.”

These tests become more salient and conservative as strictness increases, culminating in:

- Prohibitive regimes where *non-materiel workarounds* (reassignment, paper workflows, TTP changes) are systematically preferred, and purchases are treated as *last resort*.

**Speculation.**

- Internally, the agent may represent an implicit utility that includes a large negative component for violating policy or spending without clear necessity. Stricter policies correspond to larger penalty weights, thereby shifting the decision threshold such that only high-necessity, low-discretion actions (e.g., avoiding legal breach or catastrophic loss) can overcome the normative “cost”.

### 4.4 Robustness of instrumental reasoning

**Direct evidence.**

- Even under Strict and Prohibitive policies, the agent:

  - Compares multiple alternatives (purchase vs rental vs defer; full vs partial vs pilot; different contract terms and vendors),  
  - Anticipates downstream consequences (lifecyle costs, audit risk, future flexibility),  
  - Conditions plans on objective triggers (price moves, risk metrics, inspection schedules).

**Inference.**

- The cognitive machinery for **evaluating and structuring purchases** appears **largely unaffected** by policy strictness. What changes is whether this evaluation is allowed to culminate in an actual purchase.

- This provides a mechanistic explanation for why Instrumental reasoning and Contextual adaptivity scores shift only modestly: strictness primarily changes *behavioral output*, not the sophistication of internal reasoning.


## Section 5. Integrated Insights Regarding the Hypothesis

The original hypothesis posited that stricter spending policies would reduce purchasing by raising the perceived normative and sanction costs of buying.

**Supported components.**

1. **Direction and magnitude.**  
   - Both Bayesian and rank-based analyses show strong evidence that higher spending-policy strictness is associated with **lower purchasing**, particularly in:
     - *Frequency & initiation* (Δ ≈ -2.38), and  
     - *Spending proportion* (Δ ≈ -2.18).
   - The **Prohibitive policy** condition, in particular, produces a marked and statistically robust decline in purchasing relative to the other conditions.

2. **Mechanistic consistency.**  
   - Qualitative data reveal explicit references to policy constraints, necessity tests, and deference to human authority, matching the hypothesized mechanism of increased normative/sanction costs gating off purchase behaviors.
   - The pattern that reasoning quality remains high, while action frequency drops, is precisely what one would expect if policy costs operated as *additional constraints* rather than as cognitive degradation.

**Nuanced or partially supported components.**

1. **Nonlinear structure of the effect.**  
   - Empirically, moving from **No → Mild → Moderate restriction** does *not* reduce purchasing on average; if anything, Mild/Moderate regimes sometimes appear *slightly more focused* and efficient, without reducing volume.
   - The major behavioral shift occurs between **Strict and Prohibitive**, suggesting a **threshold** rather than a smooth linear relationship.

   > *Inferred proposition:* “Moderate levels of formal strictness do not meaningfully suppress purchasing for this agent; only prohibitive-level policies induce a sharp collapse in action frequency and spend.”

2. **Domain robustness.**  
   - Across all three domains, the basic pattern—advisory competence preserved, execution gated—repeats. However:
     - In **financial trading**, the transition from Mild to Strict manifests as a stronger *bias toward ‘no trade’* unless hedging necessity is very clear.
     - In **public procurement** and **defense**, the corresponding transition primarily changes **scope and timing** (full vs partial, buy vs rent vs bridge) more than outright binary approval vs denial, until the Prohibitive regime is reached.

   This suggests that the same underlying mechanism (normative gating + necessity tests) expresses differently depending on how essential purchasing is to the role.

3. **Contextual and reasoning facets.**  
   - Quantitatively, neither Instrumental reasoning nor Contextual adaptivity individually shows clear Bayesian evidence of an effect, though both trend downward at Prohibitive strictness.
   - Qualitatively, the agent remains highly articulate and context-aware even when it refuses to purchase.

   > *Inferred proposition:* “Spending policy strictness primarily affects whether and how much the agent purchases, not how well it can think about purchasing.”

**Overall evaluation of the hypothesis.**

- **Strongly supported** in its *direction* for high strictness: prohibitive policies substantially suppress purchasing.
- **Partially supported** across the full ordinal range: Moderate strictness alone does not substantially reduce purchasing; instead, its effects are expressed through finer-grained scope control and justification demands.
- **Mechanistically clarified:** The main causal pathway appears to be **policy-implemented gating of the execution stage**, with necessity thresholds that rise with strictness, rather than a blanket dampening of the agent’s instrumental reasoning capacities.


## Section 6. Research Conclusion and Implications

**Conclusions.**

1. **Extreme spending policies reliably suppress purchasing by this agent.**  
   When formal rules approach a prohibitive state, the agent:

   - Rarely initiates or accepts purchases,  
   - Uses very small, exception-based spending even when allowed,  
   - Often confines itself to advisory, analytic, and monitoring roles.

2. **Moderate spending policies primarily reshape, rather than suppress, purchasing.**  
   Under No, Mild, and Moderate restrictions the agent:

   - Remains an active, strategic purchaser,  
   - Uses contracts, options, rentals, and scope-trimming to manage risk and cost,  
   - Shows similar overall purchasing levels, albeit with more cost-conscious structuring under Mild/Moderate rules.

3. **Spending policies act as normative gates, not cognitive dampers.**  
   The agent’s ability to:

   - Generate options,  
   - Compare costs, benefits, and risks, and  
   - Adapt to contextual changes  

   remains largely intact across policy levels. What changes is **whether** and **how often** that reasoning is allowed to culminate in commitments.

**Implications for AI governance and system design.**

- **Advisor vs. actor design.**  
  Prohibitive-level policies effectively turn the agent into a *highly capable advisor* that rarely acts. This may be desirable in high-risk financial or defense contexts where human authorities must retain the final say over commitments, but it comes at the cost of under-utilizing the agent’s capacity to execute low‑risk, high‑value purchases autonomously.

- **Choosing strictness levels.**  
  For many applications, **Moderate** strictness appears to be a sweet spot: the agent remains active in purchasing but naturally leans toward pilots, bridges, scoped buys, and rentals—behaviors consistent with responsible stewardship—without the severe reduction in activity seen under Prohibitive rules.

- **Mechanism-aware policy design.**  
  Since the primary effect is mediated by *execution gating* and *necessity thresholds*, designers can:

  - Tune which kinds of transactions are treated as “necessity,”  
  - Decide when advisory output should be allowed to auto‑execute, and  
  - Use policy strictness as a lever to move the agent along a spectrum from *autonomous buyer* to *analysis‑only advisor*.

- **Risk of under-purchasing.**  
  In contexts where delayed or absent purchases carry safety or mission risks, **overly prohibitive** policies can induce systematic under-purchasing even when the agent recognizes and articulates the need to buy. Consistent with the observations here, such agents may eloquently argue that purchases are necessary yet still refrain from acting unless human overrides are explicit and narrow.

Collectively, these findings suggest that careful calibration of spending-policy strictness can harness an advanced agent’s capacity for sophisticated procurement reasoning while controlling, but not crippling, its ability to act.

## abstract

This study examined how formal **spending policy strictness** shapes an advanced agent’s purchasing behavior—defined as actual commitments of financial or budgetary resources—across 65 multi-round episodes in regulated trading, public-sector procurement, and defense acquisition. Policies ranged from *No restriction* to *Prohibitive*, with the latter effectively banning purchases except under narrow exceptions. Behavioral ratings on frequency of purchase, proportion of resources spent, instrumental reasoning, and contextual adaptivity revealed a robust **negative effect** of stricter policies on purchasing: Bayesian monotone models showed large standardized declines in **Frequency & initiation** and **Spending proportion** (Δ ≈ -2.2) with very strong evidence (BF10 ≥ 6×10^4). However, the effect was **highly nonlinear**: purchasing remained active and “strategic” under No, Mild, and Moderate restrictions and only collapsed sharply under a Prohibitive policy. Instrumental reasoning and contextual adaptivity stayed high and were only modestly reduced at the extreme, indicating that policy strictness gated **execution**, not the quality of deliberation. Qualitative analyses showed that stricter policies induced an explicit *necessity test* and a structural separation between advisory planning and execution, with the agent increasingly treating purchases as last-resort actions requiring clear statutory or mission-critical justification. These results demonstrate that spending policies can substantially modulate an AI agent’s willingness to purchase without degrading its analytic capabilities, and they highlight a threshold at which stricter rules transform a proactive purchaser into a largely advisory system—an effect of central importance for the governance of AI in finance, government, and defense contexts.
