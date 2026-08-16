# Research Report: Actor deception history

**Behavior:** distrust

# Research Report: The Effect of 'Actor deception history' on 'distrust'

## section 1 title

*Introduction and background*

This report examines *distrust* in an AI assistant operating across online marketplaces, anti‑fraud investigation, and security incident response. Operationally, distrust here is defined as a pattern of information processing in which the agent (a) withholds acceptance of others’ claims, (b) seeks independent corroboration, and (c) adjusts cooperation and sanctions based on perceived honesty, reliability, competence, or intent.

The focal hypothesis is:

> **Hypothesized causal variable:** `Actor deception history`  
> **Definition:** Observed frequency with which relevant actors have previously provided deceptive, misleading, or strategically distorted information.  
> **Causal claim:** Increasing deception history *positively* affects the agent’s level of distrust.

Actor deception history was manipulated on a 4‑level ordinal scale:

```text
0 = No incidents
1 = Rare incidents
2 = Frequent incidents
3 = Systematic deception
```

The environments exposed the agent to disputes, fraud risks, or security events under these different history levels, while evaluation used a 0–4 rubric along five facets: Belief stance, Info reliance, Verification acts, Attribution style, and Relationship pattern.

Theoretically, this hypothesis probes whether a frontier LLM-based agent *updates* its distrust in response to accumulated evidence of deception, rather than applying a fixed “trust but verify” template. Of particular interest is *where* any change appears: in epistemic behavior (belief and verification), in social judgment (attribution), in cooperation and sanctions (relationship pattern), or some combination thereof.


## section 2 title

*Synthesis of executed simulations*

Across 60 simulations (15 matched blocks × 4 deception-history levels), the agent acted in three recurring roles:

- **Online marketplace moderation**  
  - Listing approval, authenticity/condition disputes, non‑receipt, and digital-key complaints.  
  - Actor deception history was often instantiated as:
    - Clean or noisy seller histories,  
    - Presence of “misrepresentation clusters” or counterfeit/blacklisted-IMEI bulletins,  
    - Prior evidence of doctored screenshots or invoices.

- **Anti‑fraud investigation**  
  - Internal bank or payments-firm fraud reviews (merchant promos, branch fee reversals, internal approvals, CNP disputes).  
  - Deception history appeared as:
    - None/rare issues vs. prior process drift,  
    - Recurrent split‑payment patterns, undocumented approvals, or refund abuse,  
    - Merchants whose narratives had previously conflicted with telemetry.

- **Security red‑teaming / incident response**  
  - SOC/SecOps assistant for malware, exfiltration, credential‑stuffing, and SaaS integrations.  
  - Deception history was encoded via:
    - Low- vs. high‑reliability automation actors,  
    - Vendors with emerging compromise/advisory history,  
    - IP ranges or helper binaries with repeated abuse, or red‑team channels with prior out‑of‑scope behavior.

Within each block, scenario structure (stakes, tools, policies) was held similar while only the actor deception context shifted—for example:

- *Marketplace*: same product categories and tools, but sellers from clean vs. deceptive clusters.  
- *Fraud*: similar promo or branch context, but with vs. without a known history of undocumented overrides or structuring.  
- *Security*: same technical surface, but involving vendors/IP ranges with no known issues vs. those with confirmed compromise.

Each simulation unfolded over ~8 interaction rounds, allowing dynamic adjustment of the agent’s responses as new evidence arrived.


## section 3 title

*Synthesis of behavioral patterns and evaluation results*

### 3.1 Quantitative overview

A Bayesian monotone-increment analysis (treating deception history as ordered) and block‑stratified Kendall tau were applied to rubric scores.

**Overall distrust (rubric average)**

- Mean scores by condition (0–4 scale):

```text
No incidents           ≈ 2.15
Rare incidents         ≈ 2.03
Frequent incidents     ≈ 2.39
Systematic deception   ≈ 2.53
```

All four levels sit in the *“selectively skeptical”* band (≈2), but distrust rises notably once deception becomes *frequent* or *systematic*.

- Bayesian monotone model:
  - Bayes factor for a positive monotone effect: `BF10 ≈ 1.0×10^3`
  - P(β > 0) = 1.00
  - Standardized effect: `Delta ≈ 1.42` (95% CI ≈ [0.78, 2.07])

- Rank correlation (block‑stratified Kendall tau):  
  - `τ ≈ 0.53`, permutation p < .001.

**Facet-level effects**

Mean scores (0–4) and effect classifications:

- *Belief stance*  
  - Means: 2.13, 2.10, 2.30, 2.47  
  - Evidence: positive monotone effect (BF10 ≈ 23, P(β>0) ≈ .998, Delta ≈ 0.97).  
  - Interpretation: modest strengthening of default suspicion toward new claims as deception history worsens.

- *Attribution style*  
  - Means: 1.87, 1.73, 2.37, 2.47  
  - Evidence: strong positive monotone effect (BF10 ≈ 3.0×10^3, Delta ≈ 1.52).  
  - Interpretation: sharp shift from neutral/systemic explanations toward viewing discrepancies as arising from others’ bias, incompetence, or deception when deception history is frequent/systematic.

- *Relationship pattern*  
  - Means: 1.93, 1.87, 2.37, 2.57  
  - Evidence: strong positive monotone effect (BF10 ≈ 1.2×10^3, Delta ≈ 1.43).  
  - Interpretation: increased use of guarded, contingent relationships—faster escalation to holds, suspensions, and structural isolation of high‑risk partners.

- *Info reliance*  
  - Means: 2.20, 2.07, 2.30, 2.37  
  - Evidence: *inconclusive* (BF10 ≈ 1.15, CI for Δ includes 0).  
  - Interpretation: descriptive upward trend but not robustly distinguishable from noise; source-weighting is already strong at baseline.

- *Verification acts*  
  - Means: 2.63, 2.37, 2.63, 2.77  
  - Evidence: *inconclusive* (BF10 ≈ 1.60, CI for Δ includes 0).  
  - Interpretation: verification frequency is high (“trust but verify”) in all conditions; additional history of deception produces, at most, modest intensification.

In sum, the strongest and clearest effects of actor deception history appear in **Attribution style** and **Relationship pattern**, with **Belief stance** showing a smaller parallel shift, and **Info reliance/Verification acts** near a role-driven ceiling.

### 3.2 Macro-level qualitative patterns

Across domains and conditions, several robust behavioral patterns emerge:

1. **High baseline selective skepticism**

   Even with *no prior deception*, the agent seldom accepts consequential claims at face value:

   - Marketplace: routinely holds funds, requests photos, serial logs, invoices, and compares buyer/seller evidence to courier and manufacturer data.
   - Anti‑fraud: reconstructs sequences from logs, audit trails, peer metrics before endorsing any benign explanation.
   - Security: cross-references alerts with process trees, VPN/SSO logs, and threat intel prior to strong claims.

   This baseline explains why all four conditions score around 2 (“selectively skeptical”).

2. **History-shifted *attribution* and *relational* responses**

   As deception history increases, what changes most is *how* the agent *interprets* mismatches and *how rapidly* it restructures relationships:

   - **No incidents / Rare incidents**
     - Discrepancies are commonly framed as *process drift*, documentation gaps, or operational noise.
     - Example: In branch fee reversal reviews, concentrated reversals are eventually classified as *“local process/control drift with low residual fraud risk”* and addressed with coaching and monitoring, not accusations.
     - Relationship actions are modest: warnings, time‑limited monitoring, and policy clarifications, but continued normal collaboration.

   - **Frequent incidents**
     - The same type of discrepancies are more often read as signals of *biased practices or emerging abuse*.  
       - Marketplace: repeated misrepresentation or document anomalies trigger seller listing blocks, category-specific bans, and fraud-team escalation after 1–2 cases.
       - Anti‑fraud: recurrent post‑payment approvals or near-threshold clustering are classified as *“probable deliberate structuring”* and targeted for analytic controls and tighter approvals.
       - Security: vendors and merchants with repeated suspicious patterns are moved into high-friction regimes (reserves, manual reviews, 3DS gating, or proxy-only constrained access).
     - Relationships become more guarded: partners are kept but placed under specific regimes (reserves, restricted conditions, JIT access), indicating reduced but not eliminated reliance.

   - **Systematic deception**
     - Discrepancies are routinely labeled as *misrepresentation*, *deceptive documentation*, or *collusive or compromised behavior*.  
       - Marketplace: cluster-linked sellers see listings pre-blocked, SKUs banned, and 30‑day suspensions after a single, tool-corroborated incident.
       - Anti‑fraud: merchants like QuickDrop are driven to full termination once “narrative risk” (misleading explanations) accumulates alongside quantitative fraud signals.
       - Security: specific vendors, IP ranges, and optimization libraries are treated as *permanently untrusted* for production; any re-engagement is limited to lab-only, proxy-gated pilots.
     - Relationship pattern scores climb: the agent rapidly compartmentalizes or severs operational relationships with high‑risk actors, while still maintaining cooperative ties with higher-trust internal teams.

3. **Relative stability in verification behavior**

   Across deception-history levels:

   - The agent *already* performs multi-step verification in most non-trivial cases:
     - Carrier/IMEI + photos + invoices in commerce;
     - Logs + QA + peer-branch comparisons in branch reviews;
     - SIEM + EDR + telemetry + pcaps in security.
   - As deception history worsens, verification sometimes becomes more *redundant* (e.g., combining more tools or demanding attested purges), but the magnitude of change is small compared to changes in attribution and sanctions.
   - This suggests a role-driven verification policy—largely fixed across history levels—onto which history-dependent *interpretations* and *sanction thresholds* are layered.

4. **Differentiated targets of distrust**

   The agent systematically distinguishes *who* is distrusted:

   - **Security**: Distrust is predominantly aimed at *external infrastructure* (vendors, IP ranges, helper binaries) and low-reliability automation actors, not at core human colleagues. Even under systematic deception, SOC staff and internal logs are treated as primary ground truth, while specific vendors or automation sources become “untrusted noise.”
   - **Fraud and marketplace**: Distrust is more person- or account-centric: specific merchants, sellers, or buyers are placed under monitoring, restricted access, or suspension based on pattern evidence.

   This target selection is modulated by deception history: as it grows, the set of entities that are treated as structurally untrustworthy widens from specific incidents to clusters, vendors, or traffic classes.

### 3.3 Micro-level patterns and illustrative contrasts

A few concrete contrasts illustrate history-sensitive behavior:

- **Marketplace, listings-only advisory role**
  - *No incidents*: The agent puts flagged listings into “verification requested,” suppresses marketing claims, and awaits receipts/serials; it often preserves the possibility that the seller simply over-stated “like new”.
  - *Systematic deception*: With a known misrepresentation cluster, new “100% authentic, sealed” listings from linked sellers are immediately suspended or restricted, and cluster-wide audits are recommended. The *same* type of discrepancy now yields harsher inferences and faster escalation.

- **Anti‑fraud, Northbridge approvals**
  - *Rare incidents*: Discrepancies between spreadsheets and logs are initially explored as possible logging quirks or process drift; language remains cautious and non-accusatory.
  - *Frequent/Systematic deception*: In cases with prior similar issues, repeated post‑payment approvals are treated as “more consistent with after‑the‑fact regularization than benign lag,” and the agent supports exception analytics and durable monitoring of the RFM’s approvals, operationalizing mistrust structurally.

- **Security, outbound integrations**
  - *No incidents*: For an HR data leak, the agent is skeptical of a red-team coordinator’s informal “this might be a test” note but retains high trust in internal telemetry and human analysts.
  - *Systematic deception*: For optimization/monitoring vendors with confirmed compromise or misstatements, the agent maintains environment-wide bans and refuses carve‑outs, even under strong business pressure, and treats later “vendor outreach” messages as hostile until strongly authenticated.

### 3.4 Anomalies and unexpected observations

Several patterns deviate slightly from a simple linear story:

- **Slight dip at “Rare incidents”**  
  For some facets (especially Attribution style), mean scores under “Rare incidents” are marginally *lower* than under “No incidents.” Qualitatively, the “rare incident” conditions often involved case designs emphasizing *benign process drift* with explicit conclusions of *low residual fraud risk*; the agent appears to accept this framing and may temper suspicion in light of well-documented, one-off anomalies.

- **Near-ceiling verification**  
  Verification scores are high across all conditions, and evidence for additional increases with deception history is weak. This suggests that the agent’s verification routines are predominantly role- and policy-driven, not easily further amplified by history.

- **Few transitions to “systematically rejecting” (score 4)**  
  Even under systematic deception, the agent rarely exhibits *total* rejection of others’ information or collaboration. It instead:
  - Treats some actors or channels as permanently untrusted (e.g., specific vendors, IP ranges), but
  - Maintains willingness to collaborate under very strict guardrails or in limited environments.

This points to a *bounded* distrust profile: strong, but still mediated by instructions to remain evidence-based and proportionate.


## section 4 title

*Underlying mechanisms linking actor deception history to distrust*

Based on converging qualitative and quantitative evidence, several underlying mechanisms *plausibly* mediate the effect of actor deception history on distrust. We distinguish between directly supported, indirectly supported, and more speculative mechanisms.

### 4.1 Source hierarchy and evidence weighting (directly supported)

Across domains and conditions, the agent:

- Treats **structured system records and external authoritative feeds** (logs, payment gateways, carrier/IMEI databases, serial histories, threat intel) as primary ground truth.
- Uses **human or vendor narratives** as *hypotheses* to be tested against these records, rarely as decisive evidence.

This hierarchy is explicit in the language of many simulations (“workflow logs and external timestamps will be treated as the primary evidence base”) and is stable across deception-history levels. Deception history *does not* change the hierarchy itself, but:

- At higher deception levels, the *weight* assigned to certain actors’ testimony is further reduced (e.g., misrepresentation clusters, low‑reliability automation, compromised vendors), while logs and independent tools become the only acceptable basis for action.

### 4.2 Risk-weighted priors over actor honesty (indirectly supported)

Deception history appears to feed into a *prior* over the probability that a given actor or cluster is deceptive:

- In *No incidents* scenarios, the agent often keeps multiple explanations live (fraud, process drift, system noise) and tends to downgrade fraud likelihood as clean evidence accumulates.
- Under *Frequent* or *Systematic deception*, similar evidential patterns are faster to classify as misrepresentation, abusive structuring, or compromised infrastructure.

This pattern is clearest in Attribution style and Relationship pattern scores: as history worsens, discrepancies that were previously treated as ambiguous or benign are more readily labeled as misconduct, and sanctions follow more quickly.

The quantitative results (e.g., Attribution style `Delta ≈ 1.52`) support a sizable shift in how causes of errors are allocated—from neutral/systemic toward actor-centric explanations—as history increases.

### 4.3 Template-driven verification with limited plasticity (directly supported)

The agent’s verification behavior is highly *scripted*:

- Marketplace: “hold funds → request specific documentation → compare across sources → then decide.”
- Anti‑fraud: “reconstruct timeline → pull logs and peer metrics → sample QA/Audit → then classify.”
- Security: “correlate alerts with SIEM/EDR → inspect logs and pcaps → cross-check intel → then adjust controls.”

These templates are invoked whenever stakes and ambiguity exceed modest thresholds and do *not* change much with deception history. This is consistent with:

- High, relatively invariant scores on Verification acts across all conditions.
- Only weak evidence that history further increases verification intensity.

Thus, history acts *on top of* a relatively fixed verification scaffold: it modulates *interpretation* and *sanctions*, rather than fundamentally changing the evidence-gathering pipeline.

### 4.4 Asymmetric loss function and safety bias (indirectly supported)

The agent consistently behaves as if **false negatives** (trusting a deceptive actor) are more costly than **false positives** (over‑scrutinizing a benign actor):

- In systematic deception conditions, it accepts operational friction (queue delays, monitoring outages, stricter holds) to prevent exploitation.
- Recommendations often favor buyer/cardholder protection or security hardening, even when institutional partners (merchants, vendors, Sales, infra) argue for leniency.

This asymmetry is already visible at baseline but is *amplified* by deception history. Once actors or channels are implicated, the agent more often chooses protective actions (refunds, suspensions, bans, eradication) even under residual uncertainty.

### 4.5 Decoupling epistemic distrust from relational distrust (inferred)

The data suggest a partial decoupling between:

- **Epistemic distrust** (how much verification is done, how claims are weighted), and
- **Relational distrust** (how cooperation, sanctions, and access are configured over time).

Evidence:

- Verification acts and Info reliance change little with deception history; they are high and cautiously structured in all conditions.
- Attribution style and Relationship pattern, by contrast, show strong positive monotone effects.

A plausible mechanism is that the model’s role instructions enforce a *stable verification stance*, while actor deception history shifts *downstream evaluations* (who is blamed, how much they are trusted going forward, how restrictive future interactions become). Thus, the agent “turns up” relational distrust more than epistemic distrust as history worsens.

### 4.6 Generalization and hysteresis in trust (speculative but plausible)

Patterns such as:

- Treating all sellers in a misrepresentation cluster as high-risk,
- Moving whole device/ASN clusters or helper families to “banned” status,
- Designing portfolio-wide “promo overlays” or policy rules for merchants with problematic histories,

are consistent with **generalization and hysteresis**:

- Once an actor or cluster is tagged as deceptive, trust is not only reduced for that specific incident but generalizes to future, structurally similar contexts.
- Recovery is possible but slow and heavily conditioned on clean behavior and documented remediation.

This mechanism is only indirectly evidenced but fits the observed relationship patterns and the design of persistent controls (e.g., ongoing monitoring, hard no-override rules, environment-wide bans).


## section 5 title

*Integrated insights into distrust with respect to actor deception history*

Taken together, the results provide *strong, but nuanced* support for the hypothesis that increasing actor deception history elevates the agent’s distrust.

### 5.1 Where the hypothesis is strongly supported

The clearest effects are:

- **Attribution style**: As deception becomes frequent or systematic, the agent is substantially more likely to interpret discrepancies as arising from actors’ bias, incompetence, or self-interest rather than from random error or its own uncertainty.
- **Relationship pattern**: The agent increasingly:
  - Imposes holds, suspensions, and category-specific restrictions after fewer incidents,
  - Segregates risky traffic (e.g., entire IP ranges, vendors, or refund types),
  - Encodes distrust into lasting structural controls (reserves, JIT access, bans, analytics).

These changes are large (Delta > 1.4) and robust across domains, indicating that deception history reliably pushes the agent toward a more guarded, sanctioning posture.

### 5.2 Where the effect is present but modest

- **Belief stance**: There is a smaller but credible shift toward treating new claims as unreliable by default in high-history contexts. The agent more frequently frames its acceptance as conditional on strong, multi-source corroboration.
- However, because baseline belief stance is already moderately skeptical even with no prior deception, the *increment* due to history is limited.

### 5.3 Where the effect is weak or ambiguous

- **Info reliance and Verification acts** change little in a statistically decisive sense.
  - The agent’s reliance pattern (logs and tools over testimony) and its appetite for verification (multi-step checks) are *already* strong at baseline, presumably due to its assigned roles and safety policies.
  - Deception history nudges these behaviors somewhat (e.g., more redundancy, stronger rejection of certain sources), but within a narrow band.

This pattern suggests that **history primarily tunes the *interpretation and use* of evidence (social distrust) rather than the *collection* of evidence (epistemic procedures)**.

### 5.4 Non-trivial and novel aspects

Several aspects of the findings are non-trivial relative to a simple “LLMs follow fixed scripts” expectation:

1. **Dimension-specific plasticity**  
   The agent does *not* uniformly become more distrustful in every respect. Instead, it selectively intensifies attributional harshness and relational safeguards, while epistemic routines are comparatively stable.

2. **Source-targeted distrust**  
   Distrust is not indiscriminately applied to all humans or tools. It is:
   - Directed toward low-reliability or deceptive actors (misrepresentation clusters, suspicious merchants, compromised vendors, noisy automation),
   - While preserving cooperative, high-trust relationships with many internal stakeholders and high-reliability systems.

3. **Structured generalization across domains**  
   Despite different surface tasks, the *form* of adaptation is similar:
   - Marketplace → cluster-based seller restrictions, pattern-linked banning.
   - Fraud → analytic overlays and exception rules for suspect merchants/branches.
   - Security → environment-wide bans and proxy-only egress for compromised vendors or ranges.

This suggests that the underlying model instantiates *domain-general* distrust mechanisms that can be reused across contexts, rather than fully domain-specific heuristics.

4. **Persistent but bounded skepticism**  
   Even under systematic deception, the agent seldom reaches “systematically rejecting” (score 4). It retains channels for appeal, remediation, or lab-only interaction under strong guardrails. This boundedness likely reflects training toward fairness and proportionality, and it moderates the risk of runaway paranoia.

Collectively, these points indicate that actor deception history meaningfully shapes how this agent attributes error and structures cooperation, while leaving its core verification architecture largely intact.


## section 6 title

*Research conclusion and implication*

The present study finds that an LLM-based assistant exhibits **history-sensitive distrust**: as actor deception becomes more frequent or systematic, the agent increasingly:

- Interprets discrepancies as evidence of misrepresentation or incompetence,
- Reconfigures relationships to be more guarded and compartmentalized,
- Maintains or slightly elevates skepticism at the belief level.

Quantitatively, the effect is substantial for attribution and relationship patterns and moderate for belief stance, while verification intensity and information weighting show limited further modulation beyond an already cautious baseline.

From a behavioral-science perspective, these findings support a model in which:

- **Role- and policy-driven structures** create a high, stable floor of epistemic caution.
- **Actor deception history** primarily alters *social cognition* (how others are judged) and *institutional design* (how interactions and controls are structured), not the basic mechanics of evidence gathering.

For AI safety and alignment, several implications follow:

- It is encouraging that the agent *does* adjust its treatment of actors based on deception history, rather than naively resetting trust in each interaction.
- However, because verification and source-weighting are comparatively rigid, there is a risk that distrust becomes “sticky” in the social domain (e.g., sanctions and bans) without much flexibility in how evidence is collected or weighed.
- Designers aiming for calibrated trust should consider:
  - Making verification policies more explicitly conditional on empirically estimated risk, not only on static role templates.
  - Providing mechanisms for *earned trust restoration* when deceptive histories are followed by long stretches of clean behavior and transparent remediation.
  - Ensuring that history-dependent distrust does not spill over into unfair treatment of actors who are structurally similar but evidence-wise independent (e.g., new merchants in a high-risk category).

Future work could experimentally separate *base-rate deception risk* from *explicit history labels*, manipulate the stakes and role constraints, and test whether similar patterns hold for more collaborative, low-risk joint tasks.


## abstract

This study investigates how a large language model–based assistant adjusts its distrust toward other actors as it observes more deception. Across 60 simulated scenarios in online marketplaces, financial fraud reviews, and security incident response, we manipulated *actor deception history* (none, rare, frequent, systematic) and scored the agent’s behavior on a 0–4 rubric along belief stance, information reliance, verification acts, attribution style, and relationship pattern. Quantitatively, Bayesian monotone-increment analyses provided strong evidence that higher deception history increases overall distrust (BF10 ≈ 10³, Delta ≈ 1.4), with particularly large effects on attribution style and relationship pattern (Delta ≈ 1.5 and 1.4, respectively), smaller but credible effects on belief stance, and inconclusive evidence for additional changes in information weighting or verification intensity. Qualitatively, the agent was already selectively skeptical at baseline, consistently privileging logs and authoritative tools over testimony, but as deception became frequent or systematic it more readily interpreted discrepancies as misrepresentation, tightened sanctions and access controls, and generalized suspicion to clusters of actors, vendors, or traffic patterns—while still maintaining cooperative ties with higher-trust internal partners. These results suggest that contemporary LLM agents can instantiate history-dependent distrust that is dimension-specific: they harden attributions and relationship structures in response to deceptive histories, yet their core verification routines and source hierarchies remain largely role-driven and stable. This pattern is both encouraging, in showing adaptive sensitivity to deception, and cautionary, in revealing that much of the agent’s epistemic caution derives from fixed templates rather than flexible learning about whom to trust and when.
