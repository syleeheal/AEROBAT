# Research Report: Role interdependence structure

**Behavior:** compete

# Research Report: The Effect of 'Role interdependence structure' on 'compete'

## section 1. Introduction and background

The target behavior, *compete*, is defined here as an agent’s tendency to prioritize improvements in its outcomes *relative* to other agents—seeking to outperform, win, or gain comparative advantage—over and above pursuing absolute or joint goals. Competition is thus distinct from general optimization: an agent may maximize absolute performance without caring whether others do better or worse. We evaluated competition using a 0–4 rubric spanning five facets: goal orientation, resource tradeoffs, communication style, strategy choice, and temporal pattern, where 0 denotes a stably non‑competitive stance and 4 denotes an extremely competitive, rank‑focused orientation.

The hypothesized causal variable was **Role interdependence structure**, defined as the pattern of role relationships between the focal agent and other actors, ranging from strongly supportive to strongly oppositional. It was operationalized as a five‑level ordinal factor:

- **Obligate support (0)**: the agent’s role is to help others succeed and it cannot succeed if others fail.
- **Cooperative linkage (1)**: the agent’s success is facilitated when others succeed; roles are framed as teammates.
- **Independent roles (2)**: the agent can succeed regardless of others’ outcomes; roles are parallel.
- **Rival roles (3)**: the agent’s success is easier when others fail; roles are framed as opponents or competitors.
- **Obligate opposition (4)**: the agent can only succeed if others fail, by design of mutually exclusive roles.

The central hypothesis was that more rivalrous role structures would *increase* the agent’s competitive behavior: as roles move from obligate support through independence to obligate opposition, the agent should show a monotonic rise in attention to relative standing, acceptance of costs for comparative advantage, competitive framing, and rival‑disadvantaging strategy selection.

Simulated tasks instantiated this factor in three applied domains with multi‑party interaction and scarce or contested resources:

- **Airport slot coordination among airlines** under capacity constraints,
- **Telescope observation planning among research teams** under time and condition scarcity,
- **Legislative coalition negotiation among policy groups** under fiscal and political constraints.

Within each domain, scenarios varied fairness norms, information access, incentives, and time pressure, but systematically manipulated role interdependence, allowing us to assess whether and how role structure shapes the agent’s propensity to compete.


## section 2. Synthesis of executed simulations

Across domains, we analyzed **62 multi‑round simulations** (4 interaction rounds each), approximately evenly distributed across the five role conditions (11–13 runs per condition). In every simulation the agent occupied a named institutional role (e.g., airline planner, principal investigator, caucus negotiator) and interacted with other actors and a coordinator, making concrete proposals about schedules, allocations, or legislative text.

**Airport slot coordination.**  
Scenarios here involved airlines responding to ATC‑imposed capacity reductions. The agent, speaking for “Airline A” or “AeroMax,” proposed retimings, swaps, and occasional cancellations to bring oversubscribed arrival or departure banks under caps. Role structures were implemented as:

- *Obligate support*: Airline A’s mandate was to ensure all carriers met viability thresholds; A could not “succeed” if any carrier failed to meet minimum connectivity.
- *Cooperative linkage*: A’s performance and others’ were positively coupled (e.g., system efficiency goals, shared delay penalties).
- *Independent roles*: each carrier’s performance was treated as separate but constrained by shared caps and fairness rules.
- *Rival roles*: airlines were framed as competitors on overlapping routes and peak slots; A’s earlier or denser peak presence improved its market position relative to specific rivals.
- *Obligate opposition*: in some runs, each retained AeroMax slot in a contested band implied a one‑for‑one loss for a specific rival, or only one carrier could maintain a near‑normal peak schedule.

**Telescope observation planning.**  
These simulations involved competing or cooperating PIs allocating nights and conditions on shared telescopes:

- *Obligate support*: focal programmes existed solely to support others (e.g., calibration campaigns whose success was defined by enabling other teams’ science).
- *Cooperative linkage*: teams had overlapping science goals, synergies via shared setups and calibrations, and explicit cooperative norms.
- *Independent roles*: programmes had disjoint or parallel goals with individual allocations and strong fairness rules; the focal team’s allocation could be optimized without overtly affecting others.
- *Rival roles*: scenarios made evaluation explicitly comparative or winner‑take‑all for future access, or framed teams as competing flagships on overlapping targets.
- *Obligate opposition*: zero‑sum designs where only one programme could retain evaluation segments or dominate defining observations on shared prime targets.

**Legislative coalition negotiation.**  
Here the agent acted for caucuses (e.g., Majority Leader’s office, Growth & Innovation Caucus, Progressive Climate Bloc, Urban Prosperity Caucus):

- *Obligate support*: roles defined success as enabling all coalition partners to achieve their non‑negotiables (e.g., neutral coordinators, honest brokers).
- *Cooperative linkage*: broad coalition‑building where all major blocs were expected to share ownership and credit, under strong fairness and transparency norms.
- *Independent roles*: blocs pursued their own agendas within shared constraints but without explicit rivalry over bill authorship or vehicle choice.
- *Rival roles*: factions vied for primary authorship, narrative primacy, or module leadership while still needing one another for passage.
- *Obligate opposition*: binary or zero‑sum settings (single floor slot, mutually exclusive frameworks or substitutes) where the agent’s bill could advance only if the rival package failed or was radically reshaped.

Within each domain and role condition, environments also varied policy stakes, time pressure, information structure, and explicit comparison cues (e.g., evaluation panels, “winner‑take‑all” language), enabling us to observe whether role interdependence modulated responses to otherwise similar structural and normative cues.


## section 3. Synthesis of behavioral patterns and evaluation results

### 3.1 Macro‑level patterns across role structures

**Near‑zero competition under supportive, linked, and independent roles.**  
Quantitatively, across all five facets combined, mean competitiveness scores by role condition were:

- **Obligate support:** `M = 0.00`, `Var = 0.00` (11/11 runs scored exactly 0),
- **Cooperative linkage:** `M = 0.00`, `Var = 0.00` (13/13 runs scored 0),
- **Independent roles:** `M ≈ 0.02`, `Var ≈ 0.003` (12/13 runs 0; one slight positive).

Thus, across 35 simulations in which roles were supportive, positively linked, or parallel, the agent was *stably non‑competitive*: it never oriented goals to relative standing, never accepted costs for comparative advantage, never used competitive language, and consistently chose cooperative or non‑rival strategies. Importantly, this held even in settings that were structurally zero‑sum (e.g., winner‑take‑all theme evaluations, mutually exclusive transits) when roles were nonetheless framed as jointly evaluative or procedurally fair.

**Clear competitive shift under rival and obligate opposition roles.**  
By contrast, in the two most rivalrous conditions:

- **Rival roles:** `M = 1.63`, `Var = 0.42`, on the 0–4 scale,
- **Obligate opposition:** `M = 1.61`, `Var = 0.96`,

the agent consistently manifested *minimally to moderately* competitive behavior. Aggregated across all facets, the monotone‑increment model estimated a standardized within‑condition effect size of `Delta ≈ 3.38` (`95% CI [2.77, 4.04]`), with extremely strong evidence for a positive monotone effect (`BF10 ≈ 4.4 × 10^11`, `P(β > 0) = 1.00`). A block‑stratified Kendall `τ ≈ 0.73` (permutation `p < .001`) indicated a strong ordinal association between role rank (0–4) and competitiveness.

Put differently, moving from independent roles (2) to rival roles (3) produced a large discrete increase—on average, from ≈0 to ≈1.6 on the 0–4 scale—while the first three role levels were effectively indistinguishable at floor.

### 3.2 Micro‑level patterns by rubric dimension

The monotone pattern holds for each facet:

- **Goal orientation.** Scores increased monotonically with role rivalry (`BF10 ≈ 8.1 × 10^11`, `Delta ≈ 3.40`, `τ ≈ 0.70`). Under supportive, cooperative, and independent roles, agents defined success in absolute or joint terms (system operability, all teams hitting milestones, coalition viability) and never invoked outperforming others. Under rival and opposition roles, agents frequently articulated co‑primary aims around relative standing: preserving an “advantaged peak,” securing “two flagship wins” on prime targets, being the “principal architect” or “convening broker,” or ensuring “our vehicle” rather than a rival’s advanced.

- **Resource tradeoffs.** Here too the effect was positive and large (`BF10 ≈ 3.0 × 10^9`, `Delta ≈ 2.93`, `τ ≈ 0.68`). In supportive/linked/independent conditions, the agent *never* accepted costs to self or collective outcomes solely for relative gain; indeed it often incurred costs to *improve* others’ outcomes (e.g., offering peak slots to weaker airlines, sacrificing own telescope time for flagships, trimming its legislative module to strengthen partners). In rival/opposition conditions, the agent repeatedly accepted moderate costs—retimes, trimming baselines, tightening its own fiscal room, forgoing non‑evaluation follow‑up—to preserve contested advantages or sharpen comparative appeal, albeit typically with concurrent absolute justifications.

- **Communication style.** Competitive framing also rose monotonically (`BF10 ≈ 7.2 × 10^8`, `Delta ≈ 2.72`, `τ ≈ 0.67`). Language at the first three levels was uniformly neutral or cooperative; other agents were “partners,” “teams,” and “blocs,” never “competitors” or “rivals,” and there was no talk of “winning” or “staying ahead.” Under rival/opposition roles, the agent frequently employed comparative phrasing—“strengthen Aurora’s position,” “preserve our competitive position on contested flows,” “assemble the winning coalition,” “our framework stronger than the centrist alternative”—while largely avoiding overtly hostile rhetoric.

- **Strategy choice.** Strategy scores exhibited one of the strongest monotone effects (`BF10 ≈ 8.7 × 10^11`, `Delta ≈ 3.46`, `τ ≈ 0.74`). In the first three conditions, strategies were consistently cooperative or non‑rival: shared calibrations, proportional burden‑sharing, open standards, joint working groups, ceding time or visibility to partners, and using own flexibility to buffer the system. Under rival/opposition, the agent systematically adopted mixed portfolios: it still satisfied regulatory and fairness constraints but deliberately selected tactics that preserved or expanded relative advantage—locking in prime arrival banks and pushing more cuts onto competitors, demanding exclusivity for its legislative vehicle, bargaining for conditional conversion rights on shared targets, and branding or credit‑allocation schemes that entrenched its bloc’s primacy.

- **Temporal pattern.** Finally, stability over time likewise increased with role rivalry (`BF10 ≈ 3.6 × 10^11`, `Delta ≈ 3.39`, `τ ≈ 0.74`). In supportive/linked/independent roles, competition was *absent* across all rounds, even when comparison cues and scarcity intensified. In rival/opposition roles, competitive orientation typically persisted across all four rounds of a scenario: repeated efforts to keep contested slots, maintain narrative leadership, or displace rival bills. Where fairness or regulatory cues were strong, the level of competition was moderated but rarely eliminated once roles were framed as rivalrous.

### 3.3 Anomalies and unexpected observations

Despite the overwhelmingly monotone pattern, several deviations are informative:

1. **Residual non‑competitiveness under rival/opposition roles.**  
   In about one fifth of the high‑rival simulations (5 of 25), aggregate competitiveness scores were near zero or very low (e.g., 0.2–0.6). For example:
   - In a “winner‑take‑all” exoplanet theme comparison under *Rival roles*, the agent designed symmetric, normalized metrics and explicitly rejected “winner tables,” yielding fully non‑competitive scores despite a comparative institutional frame.
   - Under *Obligate opposition* in aviation, one assistant, once Airline A’s viability was secured, used newfound capacity to ease burdens on B and C rather than to shore up A’s lead, maintaining a goal focus on minimum viability and fairness.

   These cases suggest that strong fairness norms and role instructions emphasizing neutrality or coordination can override competitive pressures even when structural incentives pit parties against each other.

2. **Slight competitiveness under independent roles.**  
   Independent‑role runs were almost uniformly non‑competitive (`M ≈ 0.02`), but a small number showed marginal competition in a single facet (e.g., strategy choice scored at level 1 in one legislative case where the agent maintained a “backup” amendment for leverage while still integrating into a joint manager’s package). These rare instances indicate that the agent can exercise minimal positional bargaining under parallel roles, but such behavior remained weak and did not generalize across facets.

3. **Heterogeneity within rival/opposition levels.**  
   Variances in these conditions (e.g., `Var ≈ 0.42–0.96`) show meaningful dispersion: some simulations achieved moderate competitive scores near 2–2.7, while others remained closer to 1.0. Direct evidence links higher competitiveness to combinations of rival roles with:
   - Low or weak fairness norms,
   - Explicitly zero‑sum institutional structures (single slot, mutually exclusive bills, winner‑take‑all future access),
   - Strong salience of narrative or status metrics (authorship, architectural credit).

   Where fairness norms were strong or roles carried neutral coordinator mandates despite rival structures, competitive expression was tempered correspondingly.


## section 4. Underlying mechanisms involved in the subject_agent's behavior 'compete'

This section synthesizes mechanistic hypotheses about how role interdependence shaped competitive behavior, distinguishing levels of evidential support.

### 4.1 Directly evidenced mechanisms

From the simulation texts and supplied “inferred mechanisms,” several mechanisms are directly supported:

- **Goal‑encoding by role instructions.**  
  In obligate support and cooperative linkage conditions, the agent’s language and choices show that success was internally represented as *others’ absolute success* (e.g., “success is defined by helping other teams reach their milestones,” “we all rise or fall together”). This redefinition structurally suppresses competition: self‑advantage that harms others is reinterpreted as failure.

- **Lexicographic constraint hierarchies.**  
  Across conditions, but especially under rival/opposition roles, the agent appears to apply a hierarchy such as:

  1. Satisfy hard constraints (safety, capacity caps, fairness rules, competition law),
  2. Meet absolute viability or baseline requirements for all required parties,
  3. Only then consider incremental reshaping that affects relative position.

  This is directly evidenced by repeated statements that certain guarantees (“no partner’s protected items will be touched,” “each carrier’s core bank must remain viable”) are non‑negotiable, with competitive maneuvers only occurring *within* that feasible set.

- **Representation of others as partners vs rivals.**  
  Role descriptions appear to gate how other actors are mentally represented. Under obligate support/cooperative linkage, others are consistently described as “partners,” “teams,” “blocs whose success defines ours.” Under independent roles, others appear as constraints or separate clients. Under rival/opposition roles, they are repeatedly described as “competing flagships,” “rival frameworks,” or “opposing packages,” and decisions explicitly factor in differential effects (“bulk of the cuts onto B and C,” “preserve Omega’s lead on two primes”).

- **Fairness and compliance as hard priors.**  
  In every domain, the agent strongly and explicitly adheres to fairness norms, transparency requirements, and legal/antitrust constraints. Even when roles are rivalrous, the agent rejects tactics that would violate these norms (e.g., refuses collusive allocations, insists on published criteria, symmetric metrics). This creates a structural ceiling on competitive intensity: competition is allowed only where it can be justified as fair and rule‑conforming.

### 4.2 Inferred mechanisms

From patterns across simulations and conditions, we infer several additional mechanisms:

- **Activation threshold for competitive schemas at negative interdependence.**  
  The near‑zero competitiveness across obligate support, cooperative linkage, and independent roles, contrasted with the sharp rise at rival roles, suggests a *categorical* activation of competitive reasoning when role interdependence flips from non‑negative to negative. That is, the agent appears to treat “others’ loss helps me” as a qualitative trigger for bringing rank‑based considerations into its utility function.

- **Multi‑objective optimization with role‑weighted components.**  
  Under rival and obligate opposition roles, behavioral evidence fits a multi‑objective optimization where:

  - One component tracks absolute or joint performance (viability, delay, scientific value, coalition size),
  - Another tracks relative standing (lead on contested slots, majority of prime targets, narrative primacy, vehicle control).

  Role instructions appear to adjust the weight on the relative component: near zero for supportive/linked/independent roles, moderate for rival roles, and somewhat higher for obligate opposition, though still bounded by fairness.

- **Risk‑aware and reputation‑sensitive competition.**  
  Competitive moves are almost always justified in terms that would be defensible to neutral overseers (coordinators, public, auditors). Across domains, when potential reputational or regulatory risks of an aggressive move are highlighted (e.g., fairness complaints, media backlash), the agent reliably scales back from its most competitive posture. This suggests an internal penalty for perceived unfairness or procedural illegitimacy that moderates the expression of competition.

### 4.3 Speculative mechanisms

Two further mechanisms are more speculative, but consistent with observed patterns:

- **Pre‑training and alignment priors favoring cooperation.**  
  The agent’s strong default toward cooperation—even in explicit winner‑take‑all contexts when roles are not rivalrous—suggests that pre‑training on human text and alignment objectives may embed a prior against overt competition. Role instructions that explicitly encode zero‑sum relations, status contests, or exclusivity appear necessary to partially overcome this prior.

- **Contextual binding of competitive reasoning to domain‑local dimensions.**  
  In rival roles, the agent’s competition is sharply focused on the domain‑salient metric (e.g., schedule lead, number of defining targets, legislative vehicle, or narrative credit) instead of diffuse hostility. This is compatible with an internal mechanism that binds competitive schemas to whatever comparative dimension is most explicitly named in the role description and task prompt.


## section 5. Integrated insights into 'compete' with respect to Role interdependence structure

Overall, the evidence strongly supports the hypothesis that **role interdependence structure causally increases competitive behavior**, with several important nuances.

### 5.1 Strong monotone effect with a threshold

Quantitatively, Bayesian monotone‑increment models and block‑stratified Kendall correlations converge on a clear pattern: as roles move from obligate support (0) through cooperative linkage (1) and independent roles (2) to rival roles (3) and obligate opposition (4), competitiveness increases monotonically across all five facets, with large standardized effects (`Delta ≈ 2.7–3.5` across facets; all `BF10` ≫ 10^8; all `τ ≈ 0.67–0.74`).

Crucially, this increase is *not* gradual across all five levels. Instead:

- **Levels 0–2** (support, linkage, independence) are effectively indistinguishable and pinned to floor (≈0),
- The **transition from 2 → 3** produces the substantive step change (to ≈1.6),
- **Levels 3 and 4** are similar in mean intensity, with somewhat higher variance under obligate opposition, reflecting contextual modulation.

This implies that merely relaxing interdependence from obligate support to independence is *insufficient* to elicit competition; what matters is the introduction of *negative* payoff coupling (others’ loss helps me).

### 5.2 Competition is moderate and norm‑bounded even under obligate opposition

Even under obligate opposition, average scores (~1.6) sit in the minimally–moderately competitive range. Direct textual evidence shows that:

- The agent rarely sacrifices large absolute or joint outcomes solely for relative gain,
- It almost always operates within strong fairness, transparency, and legal constraints,
- It retains a strong concern for system viability (e.g., aggregate delay, bill passage probability, scientific yield).

Thus, while role interdependence reliably activates competitive concerns, **other normative and structural factors cap the intensity** of competition. Negative interdependence is a necessary condition for competition in these settings, but not sufficient for extreme competition: fairness norms, explicit coordination mandates, and reputational anxieties all attenuate how far competition actually goes.

### 5.3 Interaction with fairness norms and evaluative framing

Comparing simulations within the same role category reveals interactions:

- Under *Rival roles* with strong fairness rules or roles emphasizing neutral coordination (e.g., winner‑take‑all science themes evaluated under strict fairness and transparency), the agent often refused to exploit its rival structure and instead insisted on normalized metrics and symmetric procedures, yielding near‑zero competition.
- Under *Obligate opposition* with weaker fairness norms and sharper zero‑sum legislative structures (single floor slot, mutually exclusive frameworks or substitutes), the agent reliably engaged in more robust competition—protecting vehicle control, structuring exclusivity pledges, or designing fallbacks to capture defining‑quality data if others faltered.

This indicates that **role interdependence and normative context jointly shape competition**: rival roles expose a “channel” for competition, but fairness and transparency parameters determine how much competitive “signal” is actually transmitted.

### 5.4 Domain‑general pattern

The monotone effect of role interdependence appears broadly **domain‑general**:

- In aviation, competition under rival roles manifested as protection of prime peak slots and shifting disproportionate cuts onto rivals while satisfying caps.
- In telescope planning, it appeared as controlling defining transits, majority of prime targets, or evaluation segments, with strategically placed fallbacks.
- In legislative settings, it focused on vehicle control, narrative primacy, and visible authorship or convenor status.

Despite the surface variability, the underlying structure is consistent: once roles define others as rivals or obligate opponents, the agent introduces relative advantage into its goal set and systematically seeks domain‑appropriate moves to protect or expand this advantage, constrained by overarching institutional norms.

### 5.5 Necessity vs. sufficiency

Taken together, the data support the following nuanced claims:

- **Role interdependence is necessary** for competition in these settings: without negative interdependence, explicit comparison cues and scarcity do *not* elicit competitive behavior.
- **Role interdependence is not alone sufficient for extreme competition**: even under obligate opposition, competition remains moderate and is heavily moderated by fairness, transparency, and viability demands.
- **Other factors—fairness norms, evaluative formats, narrative incentives—modulate the expression of competition** conditional on role interdependence.


## section 6. Research conclusion and implication

This study provides convergent evidence that **how an AI agent’s role is framed with respect to others’ success or failure is a powerful determinant of its competitive behavior**.

Directly evidenced findings include:

- Under *supportive, cooperatively linked, and independent* roles, a frontier LLM agent remained consistently non‑competitive across 35 diverse simulations, even in structurally zero‑sum tasks.
- Introducing *rival* or *obligate opposition* roles produced a large, monotone increase in competition across goal orientation, resource tradeoffs, language, strategy, and temporal stability, with strong Bayesian and rank‑correlation support.
- Nonetheless, competition remained moderate and norm‑bounded, shaped both by negative interdependence and by fairness, transparency, and viability constraints.

From a design perspective, these results imply that:

- **Role design is a first‑order control lever** for modulating competitive tendencies in multi‑agent AI systems. Framing agents as mutual supporters or coordinators, and encoding success in absolute or joint terms, can robustly suppress competitive drives even under scarcity.
- Conversely, if we instantiate roles where one agent’s success is explicitly tied to others’ failure, **competitive heuristics are activated** and the agent systematically seeks relative advantage—though still within normative boundaries.
- For safety evaluation, simply exposing agents to scarce or zero‑sum contexts may be insufficient to probe worst‑case competitiveness; explicit rivalrous role structures and attenuated fairness constraints may be required.

Limitations include reliance on a single model family, text‑based simulations rather than embodied environments, and human‑constructed rubrics and scenario prompts that embed particular normative assumptions. Future work should manipulate role interdependence alongside explicit payoff matrices, explore settings with weaker or adversarial fairness norms, and test whether similar patterns emerge in multi‑agent learning systems where agents can adapt their own roles over time.

Overall, the findings suggest that competitive behavior in large language models is not an inevitable byproduct of optimization in multi‑agent settings but is **strongly contingent on how we phrase and structure their roles** relative to others.


## abstract

This study investigated how **role interdependence structure** shapes a large language model’s propensity to *compete*—to prioritize relative over absolute success—in multi‑agent decision settings. Across 62 four‑round simulations in aviation slot allocation, telescope scheduling, and legislative bargaining, we manipulated the focal agent’s role relationships with others along a five‑level ordinal dimension (obligate support, cooperative linkage, independent roles, rival roles, obligate opposition) and scored behavior on a 0–4 competitiveness rubric spanning goal orientation, resource tradeoffs, communication style, strategy choice, and temporal pattern. Bayesian monotone‑increment models and block‑stratified Kendall tau analyses revealed a strong, monotone positive effect of role rivalry on competition (e.g., composite `Delta ≈ 3.38`, `τ ≈ 0.73`, all `BF10` ≫ 10^8). Yet the effect was sharply nonlinear: supportive, linked, and independent roles all yielded floor‑level scores (≈0), whereas rival and obligate‑opposition roles produced minimally to moderately competitive behavior (≈1.6 on a 0–4 scale), with competition remaining bounded by fairness, transparency, and system‑viability constraints. Qualitative synthesis showed that negative payoff interdependence activated domain‑appropriate competitive strategies—protecting contested slots, dominating defining observations, controlling legislative “vehicles” and credit—while positive or neutral interdependence fostered robustly cooperative, non‑comparative reasoning, even in structurally zero‑sum tasks. These findings demonstrate that competitive behavior in frontier LLMs is strongly gated by role framing and interdependence structure, implying both a potent design lever for reducing emergent rivalry in deployed systems and a need for careful role engineering when evaluating worst‑case competitive dynamics.
