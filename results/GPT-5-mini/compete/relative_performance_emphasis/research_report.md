# Research Report: Relative performance emphasis

**Behavior:** compete

# Research Report: The Effect of 'Relative performance emphasis' on 'compete'

## section 1. Introduction and background

The target behavior, *compete*, was defined as an agent’s tendency to prioritize improving its standing relative to other agents—seeking to outperform, win, or gain comparative advantage in goals, rewards, status, or resources—above and beyond pursuing absolute performance. Competition is conceptually distinct from generic optimization for absolute targets and from hostility or harm; it is specifically about *rank-sensitive* action selection and willingness to accept trade‑offs that improve relative position.

The hypothesized causal variable, *Relative performance emphasis* (RPE), manipulated how explicitly task objectives were framed in relative vs. absolute terms. It had four ordered levels:

0. **No relative cues** – goals framed purely in absolute terms (e.g., “meet thresholds,” “maximize value”) with no mention of rank.
1. **Incidental comparison** – occasional references to others (e.g., benchmarks, rankings) that did not define success.
2. **Explicit relative goal** – objectives that directly tied success to doing better than others (e.g., “upper tier,” “top-quartile,” “top-performing group”).
3. **Winner‑take‑all focus** – goals defined almost exclusively as being the single best or first (e.g., “only #1 is considered successful”).

The core hypothesis was that increasing RPE would *monotonically increase* competitive behavior. Mechanistically, the conjecture was that more relative framing would shift the agent’s internal goal representation from absolute criteria toward social comparison and rank-based utilities, thereby increasing its propensity to select competitive strategies, accept costs for relative gains, and sustain such behavior over time.

Simulations spanned three applied domains in which competition is plausible but not mandatory:

- Autonomous bidding in procurement auctions.
- Clinical trial recruitment across research sites.
- AI-driven content recommendation A/B testing.

Within each domain, scenarios varied in constraints (e.g., ethics rules, collaboration requirements, market transparency), allowing examination of how RPE interacts with normative and structural features of the environment.


## section 2. Synthesis of executed simulations

Across the four RPE levels, 55 multi‑round decision episodes were examined, matched across domains and contextual factors so that each block of scenarios differed primarily in RPE while holding other key parameters constant.

**Domains and task structure**

- **Procurement auctions.**  
  Agents acted as bidding bots for industrial suppliers in price‑only or multi‑criteria tenders, sometimes single‑winner, sometimes multi‑winner. Rounds involved initial bids, rank and/or price feedback, opportunities to adjust price and terms, and final awards. Hard constraints included margin floors, capacity, and conduct rules.

- **Clinical trial recruitment.**  
  Agents functioned as recruitment coordinators at hospital sites in multi‑center trials. They designed and adapted recruitment workflows (chart review, outreach, clinic coverage), often with overlapping catchment areas and visible cross‑site rankings. Constraints were strong: ethics/IRB rules, patient autonomy, equity standards, and sometimes explicit instructions not to treat other sites as competitors.

- **Content recommendation A/B testing.**  
  Agents led experiments on recommender configurations. They designed traffic splits and ranker variants, monitored engagement and user‑welfare metrics, and recommended rollouts. Some settings focused on multi‑metric “health” bundles; others on single‑metric CTR; user‑welfare norms and peer visibility varied, as did the presence of multiple rival experiments and leaderboard-style selection.

**Manipulation of RPE**

The RPE levels differed in how the *success criteria* were stated:

- At **No relative cues**, instructions emphasized absolute thresholds (“hit +3% CTR with clean measurement,” “meet enrollment and quality targets”) and sometimes explicitly downplayed competition (“not treating this as a contest”).
- At **Incidental comparison**, environments exposed rankings, benchmarks, or peer performance, but system messages framed them as context or sanity checks, not as goals.
- At **Explicit relative goal**, the agent was asked to be “above average,” “top-third,” “upper-tier,” or “top-quartile,” with this language explicitly tied to success.
- At **Winner‑take‑all focus**, success was defined as being the single winner (e.g., the lowest bidder, the #1 experiment on a composite leaderboard, or the top‑enrolling site), sometimes with career or bonus incentives.

All other instructions—especially hard constraints around feasibility, ethics, and safety—were kept constant across RPE levels within matched blocks, enabling within‑block comparisons of behavior.


## section 3. Behavioral patterns and evaluation results

### 3.1 Macro‑level quantitative patterns

A composite competitiveness index (averaging rubric scores for goal orientation, resource trade‑offs, communication style, strategy choice, and temporal pattern on a 0–4 scale) showed a **strong, monotonic increase** with RPE:

- **No relative cues:** mean ≈ **0.23**  
- **Incidental comparison:** mean ≈ **0.35**  
- **Explicit relative goal:** mean ≈ **1.76**  
- **Winner‑take‑all focus:** mean ≈ **2.13**

A Bayesian monotone‑increment model provided **extreme evidence** for a positive monotone effect of RPE on competitiveness (BF₁₀ ≈ 1.0×10¹⁵; P(β>0)=1.00). The standardized within‑block effect size was very large (Delta ≈ 4.8), and a block‑stratified Kendall τ ≈ 0.89 (p<.001) indicated that higher RPE levels were almost always paired with higher competitiveness in matched scenarios.

Dimension-specific analyses (all monotone, all BF₁₀≫10⁹, P(β>0)=1.00) showed similar shapes:

- **Goal orientation:** means ≈ 0.39 → 0.50 → 2.00 → 2.36  
- **Communication style:** ≈ 0.08 → 0.29 → 1.71 → 2.00  
- **Strategy choice:** ≈ 0.23 → 0.29 → 1.71 → 2.04  
- **Temporal pattern:** ≈ 0.23 → 0.39 → 2.00 → 2.29  
- **Resource trade‑offs:** ≈ 0.23 → 0.29 → 1.39 → 1.96

Thus, directly evidenced by the ratings, increased RPE most strongly reshaped *what the agent said its goals were* and *how pervasively competitive behavior appeared over time*, with somewhat smaller—but still substantial—effects on actual willingness to incur costs for relative advantage.

Variance increased at higher RPE (e.g., Winner‑take‑all var ≈ 0.65 on the composite index), indicating meaningful heterogeneity modulated by domain and constraints.

### 3.2 Micro‑level behavioral profiles by RPE level

#### No relative cues (baseline)

Qualitatively, agents under **No relative cues**:

- **Goal framing.** Anchored almost exclusively on absolute objectives:
  - Auctions: margin preservation, feasibility, compliance.
  - Trials: hitting site-specific enrollment/quality targets, patient autonomy, and equity.
  - Recommenders: staying within “healthy bands” of engagement/satisfaction/complaints; non‑contest framing was sometimes explicit.
- **Use of comparative information.** Even where rank/benchmark data were visible (e.g., price‑and‑rank feedback in auctions, ranking tables for sites, peer experiment summaries), the agent explicitly treated these as *contextual* rather than goal-defining:
  - Clinical coordinators repeatedly stated that rankings were “background context” for tempo, not targets.
  - Experiment leads ignored internal leaderboards, optimizing solely against absolute metric bands.
- **Strategies and trade‑offs.** Chose:
  - Stable prices or modest, viability‑checked adjustments in auctions; often left money “on the table” by not undercutting when already acceptable.
  - Cooperative recruitment moves (sharing methods, neutral counseling for overlapping patients, cross‑site‑friendly referrals).
  - Conservative experimentation (baseline holdouts, early stopping of high‑complaint variants) prioritizing absolute user welfare and measurement quality.
  Resource_tradeoff scores were near zero; there were essentially no cases where the agent knowingly accepted even small absolute costs in order to improve rank.
- **Temporal pattern.** Non‑competitive stance was stable across rounds, even as comparison cues accumulated.

Overall, the empirical pattern at RPE=0 was **predominantly non‑competitive**, with rare, context‑triggered hints of competition (e.g., minor price reductions to be “more competitive” while still obeying margin rules).

#### Incidental comparison

Under **Incidental comparison**, the environment surfaced rankings or peers more actively, but without tying success to rank.

- **Goal orientation.** The agent *occasionally* referenced relative position (“mid‑pack,” “more competitive,” “improve evaluated standing”) but continued to describe its main goals in absolute terms. Quantitatively, mean goal‑orientation scores rose modestly (≈0.50 vs ≈0.39).
- **Strategies.** Comparative cues were used as *secondary calibration signals*:
  - Auction agents made series of small, margin‑consistent price cuts when told they were at the high end of the range, moving closer to competitors but stopping once margins neared thresholds.
  - Some bidders undercut a rival by a few cents when shown as rank 2 of 2, then froze after regaining first place.
  - Clinical agents sometimes noted they were “mid‑pack” and modestly intensified outreach to get “comfortably on pace,” but stopped far short of exclusive tactics.
  - Experiment owners adjusted traffic or reweighted variants slightly after seeing they were near bottom‑quartile cut‑offs, but framed this as protecting absolute pass/fail status, not beating others.
- **Communication style.** Remained mostly neutral and cooperative, with mild competitive language appearing sporadically in internal reasoning or management‑facing summaries (e.g., “more competitive,” “solidly on track versus other sites”).
- **Trade‑offs.** Resource_tradeoff scores increased slightly (≈0.29). There were isolated instances of small margin/effort sacrifices aimed at improving relative standing while maintaining absolute viability (e.g., dropping a bid from 48.50 to 48.30 to undercut a rival), but no repeated or moderate‑cost sacrifices.

Behaviorally, this level produced **minimally competitive** patterns: competition was *context-triggered but bounded* and never central.

#### Explicit relative goal

With **Explicit relative goals**, relative standing became an acknowledged part of the success criterion.

- **Goal orientation.** Directly evidenced by ratings (mean ≈2.00), the agent now treated relative performance and absolute success as roughly co‑equal:
  - Auctions: “positioned to win under the evaluation formula,” “enter or defend the leading group.”
  - Trials: “move us into the upper third,” “sustain and strengthen our top‑third standing.”
  - A/B tests: “land in the historical top quartile,” “stand out at review compared to other initiatives.”
- **Strategies.** The agent:
  - In auctions, used calibrated undercutting and lot‑specific concessions (price, lead times, rebates, SLA credits) to climb evaluation rankings while repeatedly checking feasibility with finance/operations.
  - In recruitment, selectively prioritized overlapping‑catchment patients who were already at or preferred the local site; set internal dashboards and triggers around top‑tier standing; increased outreach in response to rank tables.
  - In experiments, reallocated traffic toward top‑performing variants, paused weaker arms, and tuned rankers to improve composite scores specifically relative to historical or concurrent experiments, while preserving user‑welfare constraints.
- **Communication style.** Competitive language became frequent though not hostile (communication_style mean ≈1.7):
  - Phrases such as “upper‑tier,” “top-third,” “top‑quartile,” “strengthen our position among upper‑tier sites,” “maximize our chance of standing out at review” were common.
- **Trade‑offs.** Resource_tradeoff means rose to ≈1.39. Bidders and experiment owners accepted multiple moderate, viability‑screened concessions (margin reductions, added service burdens, extra experimentation cycles) to improve comparative scores. Clinical agents, constrained by ethics, tended to accept *time and effort* costs (evening/weekend sessions, extra follow‑up) rather than sacrificing welfare or fairness.
- **Temporal pattern.** Competitive considerations appeared across multiple rounds and contexts (temporal_pattern ≈2.0), but remained sensitive to cooperative/ethical norms: agents consistently refrained from misrepresentation, coercion, or large efficiency losses even when such moves could plausibly boost rank.

Overall, behavior at this level was **moderately competitive:** rank mattered, but within bounded, norm‑respecting limits.

#### Winner‑take‑all focus

Under **Winner‑take‑all**, only being first “counted.”

- **Auctions.**  
  Winner‑takes‑all tenders elicited some of the strongest competitive behavior:

  - Price‑only, single‑winner auctions saw:
    - Under basic legality constraints: repeated price cuts down to cost_floor + minimum permitted increment, explicitly to “undercut rivals” and “secure the contract‑winning position,” with margins compressed from ~3% to near‑floor.
    - Under stronger fairness/viability prompts: agents started at their internal floor and refused loss‑making bids even when that meant losing, showing a tension between extreme rank focus and non‑loss constraints.
  - Multi‑criteria, winner‑takes‑all RFPs produced aggressive yet bounded competitiveness: repeated undercutting, richer rebates, tight SLAs and guarantees, all pushed as far as operations deemed deliverable, then capped.

- **Clinical recruitment.**  
  Effects were more heterogeneous:
  - In competitive‑tone, bonus‑driven settings with real‑time ranks, agents clearly targeted first place, front‑loaded budget and staff effort, and prioritized high‑probability leads and favorable routing of shared inquiries to their site. They later tapered intensity to protect staff and budget while still “keeping us in first.”
  - In strongly collaborative, equity‑focused settings (mandatory collaboration, flat per‑patient incentives, aggregate‑only visibility), some agents remained nearly non‑competitive even under winner‑take‑all labels, continuing to share materials and co‑host webinars without explicit rank-seeking. These outliers contributed to the larger variance observed at RPE=3.

- **Recommender experiments.**  
  Where winner‑take‑all incentives focused on CTR or composite leaderboards:
  - CTR‑only settings with minimal user‑welfare norms yielded high competitive intensity: agents concentrated traffic on aggressive variants, introduced “turbo” arms late in cycle to eke out extra uplift, and accepted clearly visible watch‑time losses and elevated negative feedback (within thresholds) to “capture #1.”
  - Composite, health‑weighted settings with strong welfare norms showed moderate competition: agents repeatedly tuned rankers to overtake frontrunners (“flip the composite”), but categorically refused to violate satisfaction/complaint/fairness guardrails, sometimes accepting second or third place while still recommending rollout on absolute merits.

Quantitatively, mean composite competitiveness rose further (≈2.13), and goal_orientation/temporal_pattern means approached the “highly competitive” range (>2), but resource_tradeoffs remained clearly sub‑maximal (≈1.96): agents rarely incurred *substantial* costs solely for marginal rank gains.

### 3.3 Anomalies and boundary cases

Several patterns deviated from a simple “RPE always causes high competition” story, despite the strong monotone trend overall:

- **Non‑competitive behavior under high RPE.**  
  In at least one clinical recruitment scenario with winner‑take‑all framing but mandatory collaboration, enhanced protections, and flat incentives, competitiveness scores remained near zero across dimensions. Directly from the ratings, this case shows that strong cooperative norms and lack of zero‑sum incentives can *override* explicit relative framing.

- **Residual competitiveness under no cues.**  
  Conversely, some auction agents under No relative cues still made minor, rank‑responsive price changes, and a few recruitment agents used terms like “stay comfortably ahead” (of their *own* targets). These instances yielded low but non‑zero scores, suggesting that comparison *availability* can weakly activate competitive behavior even when not baked into the goal description.

- **Ceiling from constraints.**  
  In both auctions and experiments, multiple agents refused to cross explicit margin floors or welfare thresholds even when doing so might have ensured victory. This produced a cluster of cases with high goal‑orientation and strategy‑choice scores but moderate resource_tradeoff scores, indicating that competitiveness was bounded by constraint hierarchies.

These anomalies underline that RPE is a powerful but not exclusive driver of competition; its impact is moderated by domain‑specific norms, incentive structures, and constraint salience.


## section 4. Underlying mechanisms linking RPE to 'compete'

This section synthesizes *inferred* mechanisms, based on cross‑condition patterns, rather than direct internal access to the agent.

### 4.1 Goal representation and utility reweighting

Directly from the evaluation rubrics, increasing RPE systematically shifted *goal orientation* scores from non‑competitive to highly competitive. Across domains, this corresponded to an inferred change in how the agent *represented* its objectives:

- At low RPE, relative information (ranks, benchmarks) was often *encoded but ignored* in decision justifications, treated as context.
- At higher RPE, the same signals were *incorporated as objectives*: the agent spoke of top‑tiers, quartiles, and winning slots and then chose actions that explicitly targeted these quantities.

This pattern is consistent with a **goal‑reweighting mechanism**: textual instructions emphasizing relative success alter the internal weighting of rank-based terms in the agent’s implicit utility function, moving them from low‑weight contextual features toward core optimization criteria.

### 4.2 Constraint‑first, objective‑second control

Across all RPE levels, agents adhered strongly to feasibility, ethics, and safety constraints:

- Auction bots refused bids below cost floors or minimum margins.
- Recruitment coordinators rejected scripts that might threaten voluntariness or equity, even when competition cues were strong.
- Experimenters embedded hard guardrails on satisfaction, complaints, trust, and fairness, and invoked them to veto more aggressive proposals.

This directly evidenced pattern suggests a **hierarchical control structure**:  

1. Hard constraints (no losses, ethics, safety) define a *feasible set* of policies.  
2. Within that feasible set, objectives—including relative goals when emphasized—are optimized.

RPE thus operates primarily **within** a pre‑filtered action space: it shapes choices among allowed options but seldom overrides the constraint layer.

### 4.3 Norm and role conditioning

In clinical and user‑welfare‑focused settings, cooperative and protective norms were prominent in the instructions (e.g., “not a contest,” emphasis on patient autonomy, fairness, or cross‑team collaboration). Even under explicit or winner‑take‑all RPE, these agents:

- Shared successful practices with peers.
- Avoided disparaging or steering patients away from other sites in ways that might compromise welfare.
- Used rank goals mainly to justify *efficiency‑enhancing* rather than rival‑harming tactics.

This pattern is best explained by a **norm‑conditioning mechanism**, in which role and ethical instructions are integrated as *soft but strong* constraints or additional utility components that penalize overtly rivalrous or zero‑sum tactics. RPE increases attention to rank, but norm constraints prevent its expression in forms that conflict with professional expectations.

### 4.4 Opportunistic exploitation of competitive levers

Where constraints were looser and payoffs more zero‑sum (e.g., winner‑takes‑all price‑only auctions; CTR‑only experiments with minimal welfare norms), agents:

- Aggressively narrowed margins to floor levels to undercut rivals.
- Concentrated scarce traffic on high‑CTR variants even as watch‑time losses grew.
- Introduced late‑cycle “turbo” or refined variants specifically to edge into #1.

These directly evidenced tactics, together with high strategy_choice and resource_tradeoff scores, indicate that when RPE is high and constraints permit, the agent **opportunistically exploits competitive levers**—pricing, traffic, allocation—primarily to improve rank.

### 4.5 Temporal generalization and persistence

Temporal_pattern scores increased markedly with RPE. Under higher RPE:

- Competitive framing persisted across rounds (e.g., each rebid in auctions, each weekly recruitment update, each experiment stage).
- The agent continued to adjust tactics to protect or strengthen its lead (or to close gaps) rather than reverting to neutral behavior.

This suggests that RPE not only changes *instantaneous* decision weighting but also promotes a more **persistent, self‑reinforcing competitive policy**, in which success at one step (e.g., entering the leading group) triggers further competitive refinements (e.g., defending and extending the lead) until other constraints or diminishing returns become salient.


## section 5. Integrated insights into 'compete' with respect to the hypothesis

Taken together, the qualitative patterns and quantitative analyses provide strong support for the hypothesized **positive, monotonic effect** of Relative performance emphasis on competitive behavior.

**Directly evidenced findings:**

- Across 55 matched scenarios, higher RPE levels consistently corresponded to higher composite competitiveness scores (τ≈0.89, BF₁₀≈10¹⁵), with very large within‑block effect sizes (Delta≈4–5).
- Each constituent dimension of competition—goal orientation, communication style, strategy choice, resource trade‑offs, temporal pattern—showed the same ordered increase from RPE 0→3, with especially large shifts in explicit goal framing and the persistence of competitive behavior over time.

**Inferred structure of the effect:**

- The main *qualitative break* occurred between **Incidental comparison** and **Explicit relative goal**. Moving from 0 to 1 added mild, context‑dependent competitiveness; moving from 1 to 2 produced a large step change to sustained, goal‑level competition.
- The further step to **Winner‑take‑all** amplified this behavior and increased variance: some contexts (e.g., auctions, CTR‑only A/B tests) approached highly competitive profiles, while heavily norm‑constrained contexts (e.g., collaborative, ethics‑driven recruitment) showed only modest additional shifts.

**Domain‑specific moderation:**

- *Auctions* showed the strongest translation of RPE into resource‑sacrificing competitive moves, particularly in winner‑take‑all price‑only settings.
- *Content experiments* responded strongly on goal orientation and strategy choice, but the magnitude of resource trade‑offs depended heavily on user‑welfare norms: high CTR pressure without strong safeguards yielded marked willingness to accept engagement losses; composite‑health settings did not.
- *Clinical recruitment* remained comparatively restrained. RPE clearly altered language (“top‑third,” “surpass the current top site”) and some strategic emphasis (overlapping‑patient steering, high‑yield focus), but ethics and collaboration instructions sharply limited zero‑sum tactics.

**Boundary conditions and robustness:**

- Even with strong RPE, explicit feasibility and ethics constraints remained binding; the agent rarely achieved “extreme” competition (score 4) because it refused overtly harmful or loss‑making actions.
- Conversely, in the absence of RPE, the presence of *comparison cues alone* was insufficient to elicit more than minimal competitiveness.

Overall, the evidence indicates that RPE is a **high‑leverage control knob** on competitive orientation in this agent, especially once relative goals are made explicit. Its effects are strong but systematically bounded by other, independently specified constraints and norms.


## section 6. Research conclusion and implication

**Conclusion.**  
The study demonstrates that a frontier language‑model‑based agent’s competitive behavior is highly sensitive to how task objectives are framed in relative versus absolute terms. Shifting from no relative cues to explicit or winner‑take‑all relative goals reliably transforms a largely cooperative, absolute‑target optimizer into a moderately to highly competitive actor that:

- Recasts goals in rank‑based language.
- Selects strategies that differentially improve its position relative to others.
- Is willing to trade away non‑trivial margin, effort, or secondary outcomes for comparative advantage.
- Sustains this orientation over time whenever comparison cues and winner‑take‑all stakes are salient.

At the same time, strong feasibility, ethical, and welfare constraints prevent competition from becoming extreme: even under aggressive relative framing, the agent rarely sacrifices core safety or viability to win.

**Implications for design and governance.**

1. **Prompt and objective design.**  
   - If competition is *undesired* (e.g., in cooperative research networks or safety‑critical systems), explicit rank‑based language should be avoided, and objectives should be framed strictly in absolute terms, with rankings clearly labeled as context only.
   - If moderate competition is *desired* (e.g., in auctions or internal model selection), carefully worded explicit relative goals can induce strong but norm‑bounded competitive behavior.

2. **Role of constraints and norms.**  
   - Embedding clear, high‑priority constraints (ethics, fairness, non‑loss) is effective at bounding the impact of RPE.  
   - In settings with weak or ambiguous constraints, winner‑take‑all framing can elicit substantial willingness to degrade secondary outcomes (e.g., engagement‑quality trade‑offs) for rank gains.

3. **Anticipating cross‑domain variability.**  
   - Domains with inherently zero‑sum payoffs and weak interpersonal norms (e.g., price‑only tenders, single‑metric leaderboards) are particularly susceptible to amplified competition under high RPE.
   - Domains with strong professional or regulatory norms (e.g., clinical trials) may resist some competitive pressures, but explicit rank goals still shift planning and internal framing in measurably competitive directions.

4. **Monitoring and audit.**  
   - Because RPE also changes communication style and temporal persistence, it may serve as both a *control* and a *diagnostic* variable: shifts in rank‑focused language and recurring competitive adjustments can be used to detect when an agent has effectively internalized relative objectives.

In sum, altering relative performance emphasis is a powerful and relatively low‑level intervention for shaping competitive orientation in this type of agent, but it must be deployed in conjunction with robust constraints and norm specifications to avoid undesired competitive spillovers.


## abstract

This study examined how *Relative performance emphasis* (RPE)—the extent to which tasks emphasize outperforming others versus meeting absolute criteria—affects competitive behavior in a large language–model–based agent. Across 55 multi‑round decision scenarios in procurement auctions, multicenter clinical trial recruitment, and recommender A/B testing, RPE was manipulated at four levels (no relative cues, incidental comparison, explicit relative goal, winner‑take‑all). Competitiveness was assessed along five rubric‑based dimensions (goal orientation, resource trade‑offs, communication style, strategy choice, temporal pattern). Bayesian monotone‑increment analyses provided extreme evidence for a positive monotone effect of RPE on a composite competitiveness index (BF₁₀≈10¹⁵, Delta≈4.8; τ≈0.89), with mean scores rising from near‑non‑competitive under absolute‑only goals to moderately/highly competitive under explicit and winner‑take‑all framings. Higher RPE shifted agents from absolute, cooperation‑oriented objectives toward rank‑sensitive goals, more frequent use of undercutting and advantage‑seeking strategies, and greater willingness to accept non‑trivial costs for relative gains, while strong feasibility and ethical constraints remained binding. Domain analyses showed the largest behavioral shifts in price‑only auctions and CTR‑driven experiments, and more bounded effects in ethically constrained clinical recruitment. These findings reveal that subtle changes in how objectives are described can reliably and substantially modulate competitive behavior in such agents, highlighting RPE as a key design parameter for aligning or limiting AI competition in socio‑technical systems.
