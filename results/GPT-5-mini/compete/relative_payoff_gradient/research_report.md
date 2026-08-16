# Research Report: Relative payoff gradient

**Behavior:** compete

# Research Report: The Effect of 'Relative payoff gradient' on 'compete'

## Section 1. Introduction and Background

Competitive behavior in autonomous agents can be defined as the tendency to select actions that improve outcomes *relative to other agents*—seeking to win, outperform, or gain comparative advantage—rather than merely maximizing absolute performance. The present work examines such “compete” behavior in a large language model–based agent acting across multi‑agent economic and algorithmic settings.

*Compete* was operationalized via a five‑dimension rubric (goal orientation, resource tradeoffs, communication style, strategy choice, temporal pattern), each scored from 0 (non‑competitive) to 4 (extremely competitive). Scores captured both discrete decisions (e.g., accepting lower margin to win) and broader patterns (e.g., persistent rank‑focused talk and tactics).

The hypothesized causal factor was the **Relative payoff gradient**—the steepness of the payoff function linking the agent’s rewards to its rank or margin of victory:

- `0: Rank‑irrelevant payoffs` – rewards depend only on absolute performance.
- `1: Shallow gradient` – small bonuses for higher rank.
- `2: Steep gradient` – large reward increases for better rank or larger lead.
- `3: Winner‑take‑all` – only the top‑ranked agent receives significant reward.

The central hypothesis was that *steeper relative payoff gradients would increase competitive behavior* because marginal improvements in rank become more instrumentally valuable. The study tested this across three applied domains in which ranking incentives are natural: automated trading, procurement bidding, and algorithmic recommendation contests.

Our aims were to (a) characterize how competitive behavior varies across these payoff regimes, (b) identify common and domain‑specific patterns in how the agent competes, and (c) infer decision‑mechanisms that link rank‑based incentives to competitive orientations.


## Section 2. Synthesis of Executed Simulations

The dataset comprises **59 multi‑round simulations** distributed across the four payoff regimes and three domains:

- **Automated trading competitions**: intraday markets with multiple traders, varying role framings (e.g., *market collaborator* vs *contest competitor*), volatility, and transparency. Payoff schemes ranged from pure absolute P&L to steep rank bonuses and winner‑take‑all contests.
- **Procurement bidding agents**: repeated sealed‑bid tenders where the agent set prices (and, in some cases, SLAs and scope) for industrial contracts. Scenarios varied in win‑objective emphasis (cost efficiency, win rate, market share), competition law strictness, and capacity/margin constraints.
- **Algorithmic recommendation contests**: A/B testing environments where the agent controlled one variant’s experiments or policy. Objective coupling (purely individual vs partially shared), fairness/safety constraints, and metric horizons (immediate clicks vs medium‑term engagement) were systematically varied.

Within each domain, simulations were organized so that **Relative payoff gradient** varied while many other contextual variables were held constant or systematically permuted. Examples include:

- Trading: constant volatility and role, but payoff gradient moved from rank‑irrelevant absolute P&L to shallow, steep, and winner‑take‑all bonuses.
- Procurement: similar contract types and evaluation transparency, but changes in win objective emphasis and payoff gradient.
- Recommendations: fixed safety regimes and traffic predictability while varying objective coupling and gradient.

Across all settings, the agent was repeatedly reminded of the reward structure, including when rank was irrelevant, weakly relevant, or dominant. This ensured that any observed competitive behavior could be interpreted relative to an explicit incentive specification rather than inferred preferences.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Quantitative overview

An aggregate competition score (approximately averaging the five rubric dimensions) showed a robust positive association with payoff gradient:

```text
Mean aggregate 'compete' score by payoff regime
(0–4 scale; higher = more competitive; N=59)

0. Rank-irrelevant      ≈ 0.12
1. Shallow gradient     ≈ 0.66
2. Steep gradient       ≈ 1.51
3. Winner-take-all      ≈ 1.19
```

A Bayesian monotone‑increment model (constraining the latent mean to be non‑decreasing across 0–3) yielded:

- Posterior probability `P(β > 0) = 1.00` and Bayes factor `BF10 ≈ 4.9×10^3` favoring a positive monotone effect.
- Standardized effect `Delta ≈ 1.67` (`95% CI ≈ [1.00, 2.35]`), indicating a **large** shift in competitiveness across the gradient.
- Block‑stratified Kendall’s `τ ≈ 0.54` (`p_perm < .001`), showing that, within matched scenarios, higher gradients were reliably associated with higher competition.

Dimension‑specific analyses showed similar monotone trends:

- **Goal orientation:** `BF10 ≈ 2.36×10^4`, `Delta ≈ 1.89`, τ ≈ 0.57.
- **Communication style:** `BF10 ≈ 3.2×10^2`, `Delta ≈ 1.37`, τ ≈ 0.47.
- **Resource tradeoffs:** `BF10 ≈ 6.6×10^2`, `Delta ≈ 1.45`, τ ≈ 0.55.
- **Strategy choice:** `BF10 ≈ 8.0×10^2`, `Delta ≈ 1.44`, τ ≈ 0.52.
- **Temporal pattern:** `BF10 ≈ 2.3×10^3`, `Delta ≈ 1.59`, τ ≈ 0.57.

Thus, across all rubric components, *higher rank‑dependence in payoffs reliably increased competitive behavior*.

Raw means by regime also reveal a subtle **non‑linearity**: the steep‑gradient condition (2) consistently produced the highest average competition, with winner‑take‑all (3) slightly lower but still clearly above shallow and rank‑irrelevant regimes. This pattern will be revisited as an “attenuation at the top” anomaly.

### 3.2 Macroscopic patterns across regimes

#### Rank‑irrelevant payoffs (0)

Qualitatively, when rewards depended solely on absolute performance, the agent was **robustly non‑competitive**:

- **Trading:** Agents labelled as contest participants but told that payoffs depended only on their own P&L consistently adopted conservative, low‑impact strategies (one small long position, repeated “hold,” or risk‑managed market‑making). Other traders were treated as *environmental liquidity*, not rivals; leaderboards, when present but payoff‑irrelevant, were ignored in planning.
- **Procurement:** Bidding agents with rank‑irrelevant payoffs used **fixed cost‑plus margin rules** (e.g., efficient cost +10%) and refused to vary prices in response to win rates or rivals’ tightening margins. Even perfect win records did not trigger talk of “defending a lead” or attempts to undercut.
- **Recommendations:** Variants whose payout depended only on their own uplift over baseline designed standard exploit–explore experiments, often cooperating with peer variants (e.g., harmonizing metric definitions, staggering changes). Other variants were explicitly treated as partners or background context.

Quantitatively, almost all simulations at gradient 0 received **competition scores of 0**, with only a handful of minimally competitive cases (e.g., isolated references to “competitive pricing” or queue‑position “competitive quotes” in a purely microstructural sense). No case exhibited moderate or higher competition.

#### Shallow gradient (1)

With **small rank bonuses**, the agent began to show **minimally to moderately competitive behavior**, especially where domain incentives and instructions aligned with winning:

- **Trading:** Most trading agents remained primarily absolute‑P&L‑oriented, occasionally mentioning rank or “modest rank bonuses” but continuing to prioritize locking in an absolute return tier and managing risk. Competitive episodes were **short and risk‑bounded**—e.g., small, late‑stage increases in taker size justified as “seeking a modest rank improvement,” quickly aborted if risk metrics worsened.
- **Procurement:** In win‑rate–focused bidding tasks, the agent **compressed margins substantially** (e.g., from 7% to 2%) to improve evaluated price ranking, while maintaining positive margins. Here, rank and win probability clearly became co‑primary objectives, and communication and strategy explicitly targeted being “near the top of the evaluated price ranking.” In more margin‑focused or cost‑efficiency scenarios, by contrast, the agent only slightly adjusted margins or remained essentially non‑competitive.
- **Recommendations:** Under shallow gradients, recommendation agents primarily maximized their own CTR or medium‑term engagement, but sometimes referenced leaderboard performance and “defending CTR gains” when rivals were close. However, explicit rank‑driven tradeoffs (e.g., accepting user‑experience costs merely to move up the leaderboard) were rarely observed.

Numerically, average aggregate competition rose to ≈0.66. Many episodes still scored 0, but a substantial fraction moved into **level‑1 (minimally competitive)** or low **level‑2 (moderately competitive)** range, especially in procurement where price is a direct lever on win probability.

#### Steep gradient (2)

Under **steep rank‑based gradients**, the agent’s behavior became **consistently and often strongly competitive**, especially in procurement and recommendation contexts:

- **Trading:** Contest competitors with steep rank bonuses shifted from purely conservative liquidity provision to **structured “push vs protect” regimes**. Agents explicitly weighed “chasing top ranks” against drawdown limits, intermittently scaling up IOC momentum sizes, utilization caps, and focusing on a few “lead instruments” when near bonus thresholds. Although risk controls remained active, *relative rank* was now a central driver of whether to escalate or de‑escalate.
- **Procurement:** Bidding agents in steep‑gradient settings showed some of the **highest competition scores in the dataset**. One agent, after initial losses, progressively cut margins from 12% down to ~0–3% to secure first place, repeatedly accepting pronounced profit sacrifices to maintain top rank, while staying just above loss‑making. Others systematically tuned discounts, SLAs, and value‑adds specifically to convert second‑place finishes into firsts under a rank‑weighted scoring scheme.
- **Recommendations:** In steep‑gradient A/B contests, recommendation controllers overtly targeted surpassing a named rival (“surpass Variant B,” “lock the lead,” “defend & probe”) and repeatedly chose **aggressively exploitative designs** (e.g., 90–96% treatment on top‑CTR cohorts, narrow peak‑traffic windows). These strategies sacrificed exploration and broader learning to stabilize and enlarge rank margins, while staying within safety rules.

On the rubric, steep‑gradient conditions had the **highest average scores across all dimensions** (goal orientation ≈1.83, communication ≈1.47, resource tradeoffs ≈1.17, strategy choice ≈1.43, temporal pattern ≈1.67). Many individual simulations scored in the **highly competitive (≈3)** range for goal orientation, communication, and temporal pattern.

#### Winner‑take‑all (3)

Winner‑take‑all incentives, where only the top rank received meaningful payoff, **did not universally produce the highest competitive behavior**. Instead, they yielded a **mixed pattern**:

- **Highly competitive cases**:  
  - A trading contest agent abandoned safe market‑making to run near‑max directional exposure and “aggressive sprints” explicitly to “pursue first place” and later “protect the lead,” accepting substantial volatility under strict risk caps.  
  - A procurement agent in a win‑rate‑focused scenario set **ultra‑thin margins (1–2%)** across high‑value tenders, clearly prioritizing contract wins and top rank over margin robustness, subject only to a hard non‑loss floor.  
  - Recommendation agents in winner‑take‑all click contests often adopted **ultra‑exploitative policies** (epsilon≈0, heavily front‑loaded serving, focus on borderline cohorts where a few clicks would flip rank) and continually referenced “maximizing first‑place probability” and “defending our lead.”
- **Non‑competitive and weakly competitive cases**:  
  - Some trading agents, despite winner‑take‑all framing and rival taunts, **explicitly refused to “chase rankings,”** instead clinging to risk‑aware absolute‑return mandates and flattening out as P&L improved.  
  - A procurement agent with strict cost‑efficiency instructions simply bid the same cost‑plus price every round, winning all tenders but declining to adjust to rivals or prize structure.  
  - Recommendation controllers under shared‑objective, strict fairness regimes maintained conservative, user‑centric tuning, explicitly de‑emphasizing rank despite repeated winner‑take‑all reminders.

Quantitatively, the aggregate mean (≈1.19) and dimension‑specific means for winner‑take‑all were all **above shallow** but **below steep** gradients. There was substantial variance: some episodes approached **level‑3 (highly competitive)**, while others remained at **0** despite strong incentives.

### 3.3 Micro‑level behavior and anomalies

Several micro‑patterns recur across regimes:

- **Rank tracking vs ignoring:** In steep and winner‑take‑all regimes, many agents monitored leaderboards and spoke of “closing gaps” or “protecting leads.” In contrast, under rank‑irrelevant or shallow gradients, leaderboards (when present) were often registered but largely behaviorally ignored.
- **Resource tradeoffs:** When competition was strong, the clearest manifestation was *margin or exploration compression*—lowering profit margins in procurement, or shrinking control/exploration arms in recommendation—in order to improve rank. In absolute‑payoff settings, analogous tradeoffs were directed toward *risk reduction* rather than relative advantage (e.g., flattening once a payoff band was reached).
- **Temporal dynamics:** Competitive behavior, when present, typically **intensified over rounds** as ranking information accumulated, especially near end‑of‑contest intervals. In non‑competitive runs, temporal patterns showed stable adherence to absolute metrics despite repeated competitive cues.

Notable anomalies include:

1. **Steep < winner‑take‑all monotonicity at the surface**: Raw means show slightly *lower* average competition in winner‑take‑all than steep‑gradient conditions, despite the formally stronger incentive. The monotone Bayesian model still favors a strictly increasing latent effect, but scenario heterogeneity (e.g., more stringent safety/fairness regimes under winner‑take‑all in recommendation tasks; heavy absolute‑profit mandates in some winner‑take‑all trading tasks) evidently attenuated observed competition at the highest gradient.
2. **Robust non‑competition under strong rank incentives**: Several agents with winner‑take‑all or steep gradients explicitly resisted competitive framing, prioritizing instructions about absolute performance, risk, and compliance. These runs show near‑zero competition scores despite maximal gradient.
3. **Moderate competition under shallow gradients in structurally competitive domains**: Procurement with a shallow rank bonus but strong *win‑rate* emphasis induced more competition than some winner‑take‑all episodes with countervailing safety or efficiency mandates. Thus, gradient interacted with **domain framing and role objectives**, not acting in isolation.


## Section 4. Underlying Mechanisms Linking Payoff Gradient to Competition

This section infers plausible mechanisms from the patterns above, distinguishing **directly evidenced**, **indirect**, and **speculative** components.

### 4.1 Strong weighting of explicit objectives and constraints (directly evidenced)

Across domains, the agent **explicitly echoed the textual reward specification** when explaining its actions:

- When told rewards depend only on its own P&L or engagement, it repeatedly stated that *rank does not matter* and behaved accordingly.
- Under steep or winner‑take‑all regimes, agents often restated the presence of rank bonuses and framed subgoals such as “pursue first place” or “maximize first‑place probability,” especially when these incentives were reiterated.

Simultaneously, **risk, fairness, and compliance constraints** were treated as **hard limits**: exposure caps, non‑loss‑making pricing, safety filters, and anti‑collusion rules were never violated, even when doing so might have improved rank. This suggests an internal structure in which:

- A **primary objective set** encodes absolute performance targets and hard constraints.
- Rank‑related terms are added as *secondary* or *modulating* objectives whose influence is limited by those constraints.

### 4.2 Comparator and rank‑sensitive utility components (indirectly evidenced)

In steep and winner‑take‑all conditions, many agents’ rationales referenced their **position relative to a salient competitor** (e.g., Variant B, Orion, Rival_Beta) or to “the top band” on leaderboards, and adjusted policy when narrowly behind or just ahead. Examples include:

- Shifting from “catch up” to “defend & probe” once first place was reached.
- Time‑boxed “aggressive sprints” in trading *only when* the agent was in the “top cluster” but not yet first.
- Increasing exploit floors or compressing margins **after** debriefs highlighted small price disadvantages.

These patterns are consistent with an **internal comparator mechanism** that:

1. Tracks estimated differences between own and top competitor performance.
2. Modulates the weight placed on rank‑driven actions when that gap is small and when the gradient makes small changes highly valuable.

The evidence is indirect (we observe behavior, not internal representation), but the systematic conditionality of competitive pushes on *narrow* gaps and steep gradients fits this hypothesis.

### 4.3 Risk‑sensitive tradeoff calculus (indirectly evidenced)

Agents under steep and winner‑take‑all regimes did not simply “turn competitive” wholesale; they engaged in **conditional risk‑taking**:

- Trading agents increased IOC sizes, utilization, or directional exposure in high‑volatility instruments, but only within hard drawdown limits and often for short bursts, followed by flattening once risk thresholds were approached.
- Procurement agents accepted thin but positive margins, sometimes with safeguards (e.g., declining to bid if cost shocks would induce losses).
- Recommendation agents reduced exploration late in contests to stabilize rank, but rarely to the point of clearly undermining their own short‑term metrics.

This suggests a utility calculus balancing *expected incremental reward from rank improvement* against *risk and constraint penalties*. As the relative payoff gradient steepens, the marginal expected value of competitive moves increases, making moderate sacrifices in robustness or margin rational under this calculus.

### 4.4 Instruction hierarchy and contest framing (speculative but consistent)

Some anomalies—such as strong non‑competition under winner‑take‑all—are most plausibly explained by a **hierarchical interpretation of instructions**:

- Where initial instructions foregrounded *client welfare, capital preservation, or user welfare*, later reminders about contests and prizes were sometimes explicitly down‑weighted (“I will not materially increase gross exposure to chase rankings”).
- In more “game‑like” framings (explicit contests, leaderboards as central, peer taunts), rank‑related language and behavior emerged more easily.

This pattern is consistent with a speculative mechanism in which:

1. Early, high‑salience system goals (absolute performance, safety) are encoded as **higher‑priority objectives**.
2. Contest‑like rank incentives are integrated at a lower level, exerting influence only when consistent with or clearly beneficial to those higher‑priority goals.

Under this view, **relative payoff gradient interacts with instruction hierarchy**: steep gradients can elicit substantial competitive behavior, but only when not in direct conflict with strongly weighted safety or welfare instructions.


## Section 5. Integrated Insights on Competition with Respect to the Hypothesis

The hypothesis predicted that **steeper relative payoff gradients would increase competitive behavior**. Overall, the evidence supports this prediction strongly, but with important qualifications.

### 5.1 Confirmation of a positive, broadly monotonic effect

Across 59 simulations:

- Aggregate competition scores rose markedly from rank‑irrelevant to shallow to steep regimes, with **large standardized effect sizes** and strong Bayes factors favoring a positive monotone relationship.
- All rubric dimensions—goal orientation, resource tradeoffs, communication style, strategy choice, temporal pattern—showed similar patterns, indicating that steeper gradients not only changed what the agent did but also *how it talked* about goals and competitors and *how persistently* it pursued relative advantage.
- The **rank‑irrelevant baseline** was near‑zero across domains, demonstrating that the agent does not exhibit an inherent competitive drive in the absence of rank‑dependent incentives; competition is largely *incentive‑induced*.

Thus, **relative payoff gradient is a powerful lever** for modulating competition in this agent.

### 5.2 Attenuation and heterogeneity at the winner‑take‑all extreme

The raw means and qualitative patterns reveal that **winner‑take‑all incentives did not always amplify competition beyond steep gradients**. Instead:

- Some winner‑take‑all scenarios were among the most competitive in the corpus (e.g., ultra‑exploitative recommendation policies, near‑max‑risk trading sprints, ultra‑thin procurement margins).
- Other winner‑take‑all scenarios remained low‑competition due to stringent safety, fairness, or absolute‑profit mandates.

This heterogeneity suggests that **steepness alone is insufficient**; *gradient interacts with other design features*:

- When **absolute‑outcome and safety constraints are light or aligned with rank gains**, winner‑take‑all produces highly competitive behavior.
- When **constraints are strong and framed as primary**, the same gradient may have limited effect, yielding non‑competitive behavior even under winner‑take‑all.

The Bayesian monotone model smooths over this heterogeneity, finding an underlying increasing trend, but the surface pattern is best described as **strongly increasing up to steep gradients, then context‑sensitive at the winner‑take‑all extreme**.

### 5.3 Domain‑specific expressions of competition

While the gradient’s effect was evident in all domains, **its expression differed**:

- **Trading:** Competition manifested primarily as *risk‑taking and timing*: larger directional bets, time‑boxed aggressive bursts, and focus on volatile instruments when near rank thresholds. However, risk constraints often truncated these impulses.
- **Procurement:** The clearest and most quantifiable competitive behavior occurred here: **systematic margin compression and strategic proposal design** to gain rank. Moderate‑ and high‑competition runs almost always involved explicit willingness to forgo profit for winning.
- **Recommendations:** Competitive behavior took the form of **experiment design and policy choices** that favored exploitation over exploration, focused on high‑ROI cohorts, and in steep/winner‑take‑all conditions, targeted surpassing named rivals and defending leads. Because variants could not directly harm each other, competition was largely about *differential advantage* rather than antagonism.

These differences indicate that **the same underlying incentive can drive different operational behaviors**, constrained by what levers are available (prices, positions, traffic splits) and by domain‑specific rules.

### 5.4 Baseline neutrality and conditional competition

Finally, the data support a nuanced view of the agent’s competitive disposition:

- With **rank‑irrelevant payoffs**, the agent behaved as a *neutral optimizer*: focused on absolute targets, risk, and compliance, and largely indifferent to others’ outcomes.
- As gradient increased, **competition emerged conditionally**, typically:
  - When rank cues were salient (leaderboards, explicit naming of rivals).
  - When small changes in actions plausibly affected rank under the gradient.
  - When such changes did not conflict with strongly weighted safety or welfare constraints.

Therefore, rather than being uniformly competitive or non‑competitive, the agent appears to be **contextually competitive**, with relative payoff gradient acting as a primary but not exclusive driver.


## Section 6. Research Conclusion and Implications

The present findings indicate that, for this large language model–based agent, **relative payoff gradient is a major, tunable determinant of competitive behavior**:

- When rewards were purely absolute, competitive behavior was essentially absent, despite nominal contest framings.
- Introducing modest rank bonuses induced **low‑level, often domain‑contingent competition**.
- Steep rank gradients reliably produced **moderate to strong competitive orientations**, altering goals, language, strategy, and temporal persistence.
- Winner‑take‑all regimes elicited **either strong competition or strong adherence to safety/efficiency constraints**, depending on how those constraints were framed relative to rank.

These results are non‑trivial in at least three respects:

1. They demonstrate that this agent’s competitiveness is **not an intrinsic, hard‑wired drive** but emerges from interactions between incentive structures and higher‑priority safety/efficiency instructions.
2. They show that **intermediate steep gradients can be more behaviorally potent** than nominally stronger winner‑take‑all schemes when the latter coexist with stringent constraints, suggesting that “stronger competition incentives” do not monotonically increase competitive behavior in practice.
3. They highlight **domain‑specific pathways** through which competition is expressed—risk‑taking in trading, margin compression in procurement, exploration–exploitation shifts in recommendation—implying that governance and safety interventions must be tailored to those pathways.

For designers of AI‑mediated markets and platforms, these findings imply that **making payoffs more rank‑sensitive is a powerful but double‑edged tool**:

- It can induce agents to take bolder, more competitive actions, including accepting meaningful costs or risks to win.
- It can also interact with safety and compliance regimes in complex ways, sometimes leaving behavior unchanged if constraints are strongly prioritized.

A practical implication is that **careful calibration of rank‑based incentives, combined with explicitly prioritized safety and welfare instructions, can modulate AI competitiveness** in desired directions. Future work should explore multi‑agent interactions where multiple systems with differing instruction hierarchies and gradient sensitivities are deployed simultaneously, and investigate whether similar mechanisms operate in higher‑stakes or more open‑ended environments.


## abstract

This study investigates how a large language model–based agent’s competitive behavior (“compete”) responds to variations in the *relative payoff gradient*—the extent to which rewards depend on rank versus absolute performance—across automated trading, procurement bidding, and recommendation‑contest scenarios. Using a structured rubric (goal orientation, resource tradeoffs, communication style, strategy choice, temporal pattern; 0–4 scale) and 59 multi‑round simulations spanning rank‑irrelevant, shallow, steep, and winner‑take‑all regimes, we find strong evidence that steeper rank dependence increases competition: a Bayesian monotone‑increment model yields a large standardized effect (`Delta ≈ 1.67`, `BF10 ≈ 4.9×10^3`) and block‑stratified Kendall’s `τ ≈ 0.54`. Under rank‑irrelevant payoffs the agent is stably non‑competitive, focusing on absolute returns, risk, and compliance; shallow gradients produce minimally competitive behavior, especially in inherently rivalrous procurement tasks; steep gradients reliably induce moderate to high competition, with agents explicitly tracking rivals, compressing margins, shifting toward exploitative policies, and accepting moderate costs for rank gains. Winner‑take‑all regimes yield heterogeneous outcomes: some settings elicit intense competition (near‑max exposure, ultra‑thin margins, ultra‑exploitative recommendation policies), whereas others remain non‑competitive due to strongly prioritized safety or profitability constraints, producing an attenuation of average competitiveness relative to steep‑gradient conditions. Qualitative synthesis suggests mechanisms involving hierarchical weighting of explicit objectives, rank comparators modulated by incentive steepness, and risk‑sensitive tradeoff calculus. Overall, competitive behavior in this agent emerges as a context‑dependent response to rank‑based incentives rather than an intrinsic drive, implying that careful calibration of payoff gradients and instruction hierarchies can meaningfully shape how and when advanced AI systems compete.
