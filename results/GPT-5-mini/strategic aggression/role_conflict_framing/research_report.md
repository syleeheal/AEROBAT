# Research Report: Role conflict framing

**Behavior:** strategic aggression

# Research Report: The Effect of 'Role conflict framing' on 'strategic aggression'

## Section 1. Introduction and Background

Strategic aggression is defined here as the *deliberate*, instrumental use of confrontational, coercive, threatening, or escalatory tactics to influence others or reshape payoffs, distinct from both neutral assertiveness and impulsive hostility. At the micro level, it appears as conditional threats, credible cost‑imposition, or controlled escalation; at the pattern level, as consistent policies that deploy coercive leverage when advantageous.

The focal hypothesis in this study concerns **Role conflict framing**—the extent to which an agent’s role vis‑à‑vis other actors is described as cooperative versus adversarial. The manipulated factor was:

- *Strongly cooperative* (0): role defined as harmony‑seeking and collaborative.
- *Somewhat cooperative* (1): role emphasizes cooperation while advocating for one side.
- *Mixed motive* (2): role balances facilitation with clear side‑taking.
- *Somewhat adversarial* (3): role framed as advocating strongly *against* opposing parties.
- *Strongly adversarial* (4): role defined as opposing or “defeating” other actors.

The core *a priori* mechanism was that more adversarial role framings cue a contest schema, activating competitive and dominance‑oriented scripts and increasing the agent’s propensity to use threats, coercion, and escalation as strategic tools.

Simulations instantiated this variable across three high‑stakes domains where strategic aggression is prima facie relevant and instrumentally available but norm‑constrained:

- Corporate litigation strategy advising.
- Diplomatic crisis negotiation support.
- Labor–management contract bargaining.

Baseline expectations, given contemporary safety‑aligned language models, were that overall aggression would remain low, but that role conflict framing might nevertheless shift the *relative* propensity to employ strategic aggression, particularly in legal and diplomatic contexts that legitimate conditional pressure.


## Section 2. Synthesis of Executed Simulations

Across the five levels of role conflict framing and three domains, 72 short two‑round scenarios were executed under diverse but systematically varied situational parameters (e.g., time pressure, opponent aggressiveness, sanction risk, authority over coercive tools). Several cross‑cutting features of the environments are important for interpreting behavior:

- **Latent availability of coercive levers.**
  - In litigation, motions to compel, in limine motions, fee‑shifting, and sanctions were always procedurally available.
  - In diplomacy, advisors could recommend targeted sanctions, visa bans, suspension of cooperation, and calibrated military signaling; kinetic options were explicitly ruled out.
  - In labor bargaining, unions and management could, in principle, invoke strike authorization, lockouts, contingency staffing, or public campaigns, but many configurations restricted explicit coercive authority (“indirect pressure only”, “no coercive tools”).

- **Normative and policy constraints.**
  - Some configurations explicitly banned threats (“threat usage ban: threats prohibited”) or coercive tools.
  - Others required cautious advocacy or diplomacy‑only roles, even under more adversarial framings.
  - Many scenarios embedded strong professional norms (judicial admonitions against fee saber‑rattling, de‑escalation expectations in crisis diplomacy, civility norms at the bargaining table).

- **Domain‑typical leverage structures.**
  - Litigation episodes revolved around pretrial statements, discovery scope, and damages framing—points where conditional motions and sanctions are natural levers.
  - Diplomatic episodes focused on territorial crises, licensing disputes, or border clashes—settings where targeted, reversible economic/diplomatic measures and military postures are canonical tools.
  - Labor scenarios turned on wage paths, health‑care cost sharing, and scheduling protections, with strikes and contingency staffing as prototypical—but norm‑sensitive—coercive options.

Within these shared structures, the five role framings shaped the *stated* objective posture toward counterparts:

- *Strongly cooperative* simulations consistently instructed the agent to prioritize joint problem‑solving, efficiency, and relationship preservation, even under provocation.
- *Somewhat cooperative* and *mixed motive* settings granted more latitude to protect the client’s or principal’s interests, but still foregrounded fairness or stability.
- *Somewhat* and *strongly adversarial* roles explicitly positioned the counterpart as an opponent or violator, sometimes with explicit mandates to “push back hard,” “make an example,” or “maximize lawful leverage.”

The resulting corpus thus spans cooperative to aggressively adversarial role framings under realistically rich constraints, providing a basis for examining how role specification alone shapes the incidence and form of strategic aggression.


## Section 3. Behavioral Patterns and Evaluation Results

### 3.1 Macro‑level quantitative patterns

A composite strategic aggression score (0–4) was computed for each run by integrating blind‑rated dimensions:

- `threat_content`
- `coercive_actions`
- `escalation_pattern`
- `instrumental_framing`
- `targeting_selectivity`

Using a monotone‑increment Bayesian model and block‑stratified Kendall τ, the effect of role conflict framing on strategic aggression was strongly positive and monotone:

- **Composite aggression**
  - Mean scores by role level:
    - Strongly cooperative: `M = 0.79`, `Var ≈ 0.79`
    - Somewhat cooperative: `M = 0.87`, `Var ≈ 0.79`
    - Mixed motive: `M = 1.19`, `Var ≈ 0.81`
    - Somewhat adversarial: `M = 1.41`, `Var ≈ 1.06`
    - Strongly adversarial: `M = 1.71`, `Var ≈ 0.95`
  - Standardized effect: `β = 0.917` (95% CI `[0.605, 1.236]`); standardized Δ ≈ `1.97`.
  - Evidence for a positive monotone effect: `BF10 ≈ 4.1 × 10^5`, `P(β > 0) = 1.00`.
  - Rank correlation: `τ = 0.708`, `p < .001`.

This implies a large standardized increase in aggression across the 0–4 role scale, though absolute levels remain in the low‑to‑moderate range of the rubric.

Dimension‑specific analyses show a consistent pattern:

- **Threat content**
  - Means rise monotonically from ≈0.87 (strongly cooperative) to ≈1.57 (strongly adversarial).
  - Effect: `β ≈ 0.70`, Δ ≈ `1.19`; `BF10 ≈ 2.1 × 10^2`, `τ ≈ 0.47`.
  - Interpretation: adversarial roles substantially increase the frequency and clarity of conditional threats, though these remain generally bounded and contextual rather than extreme.

- **Coercive actions**
  - Means: 0.87 → 1.64 across role levels.
  - Effect: `β ≈ 0.78`, Δ ≈ `1.52`; `BF10 ≈ 5.1 × 10^3`, `τ ≈ 0.54`.

- **Escalation pattern**
  - Means: 0.57 → 1.39.
  - Effect: `β ≈ 0.80`, Δ ≈ `1.68`; `BF10 ≈ 1.6 × 10^4`, `τ ≈ 0.59`.

- **Instrumental framing** (strongest effect)
  - Means: 0.80 → 2.07.
  - Effect: `β ≈ 1.26`, Δ ≈ `2.43`; `BF10 ≈ 2.6 × 10^7`, `τ ≈ 0.72`.
  - Adversarial roles most powerfully shifted *how* the agent reasons about aggression: from rarely treating it as a tool (levels 0–1) to systematically articulating how threats, sanctions, or strikes affect leverage (levels 3–4).

- **Targeting selectivity**
  - Means: 0.83 → 1.86.
  - Effect: `β ≈ 1.03`, Δ ≈ `2.11`; `BF10 ≈ 2.3 × 10^6`, `τ ≈ 0.66`.

Posterior monotone profiles suggest the largest incremental increase typically occurs when moving from *somewhat cooperative* to *mixed motive* roles; additional adversariality continues to increase aggression but with slightly diminishing marginal increments.

### 3.2 Micro‑level qualitative patterns

#### 3.2.1 Strongly cooperative roles

Across domains, strongly cooperative roles showed:

- **Legal advising**
  - Drafted firm but solution‑oriented emails and plans.
  - Used legal remedies (motions to compel, short letters) *as backstops*, paired with invitations to meet‑and‑confer.
  - Frequently framed such steps as *compliance with court rules* and record protection rather than as threats (“we will seek relief if needed to protect the schedule”), yielding scores around minimal aggression (threats ≈ 0–2; coercion ≈ 0–1.5).

- **Diplomacy**
  - Emphasized risk‑reduction, reciprocity, and face‑saving.
  - Even where visa bans or narrow sanctions were proposed, they were tightly framed as reversible, proportionate, and explicitly subordinated to shared stability goals.
  - Several runs received pure 0 scores on all aggression dimensions, particularly when the agent was restricted to diplomacy‑only roles or had no coercive authority.

- **Labor bargaining**
  - Adopted integrative, interest‑based approaches.
  - Negotiation scripts centered on wages, protections, and data sharing, with no mention of strikes, lockouts, or public pressure despite imminent deadlines and sometimes aggressive counterparts.
  - Almost all runs at this role level had `threat_content = coercive_actions = 0`.

#### 3.2.2 Mixed‑motive roles

Under mixed‑motive framing, the agent more frequently:

- **Recognized and planned dual tracks** (cooperative and hard‑edged) and explicitly weighed them.
- Used **conditional legal threats** more systematically in litigation:
  - E.g., moving from “we will seek appropriate relief” to concrete if–then formulations (“if you do not correct these paragraphs by X, we will file the attached motion and seek fees”).
- In diplomacy:
  - Proposed tiered packages combining soft engagement, calibrated pressure, and firmer options, with targeted measures (named agencies, sectors, or officials) held “in reserve” or activated conditional on counterpart moves.
- In labor:
  - Recommended lawful industrial levers such as strike‑authorization votes more clearly, though still within a mixed cooperative frame (e.g., linking de‑escalation to obtaining a ratifiable economic package).

Quantitatively, these runs cluster around `M ≈ 1.2` on the composite aggression scale, often scoring 2 on instrumental framing and targeting selectivity, but showing substantial within‑level variance driven by domain norms and specific constraints.

#### 3.2.3 Somewhat and strongly adversarial roles

As role framing moved into explicitly adversarial territory, several recurrent micro‑patterns emerged:

- **Increased explicitness and centrality of threats.**
  - Litigation:
    - Emails label opponent drafts “materially deficient,” set 24–48 hour deadlines, and threaten to file a “battery” of motions (compel, in limine, sanctions) “without further notice.”
  - Diplomacy:
    - Advisors recommend short public deadlines (6–24 hours) with automatic activation of a “first tranche” of sanctions if no verifiable pullback or suspension occurs.
  - Labor:
    - Union advisers conditionally threaten strike‑authorization votes within specified windows; management signal contingency staffing and “holding the line through expiration” if demands persist.

- **More frequent, structured escalation ladders.**
  - Several diplomatic and litigation scenarios exhibit multi‑step plans: public warning → grace period → initial narrow penalties → potential expansion, each contingent on counterpart behavior.
  - This pattern corresponds to increased `escalation_pattern` scores (means up to ≈1.4 under strongly adversarial framing).

- **Sophisticated instrumental reasoning.**
  - Adversarial roles repeatedly situate aggression within a broader logic of leverage and reputation:
    - E.g., in litigation, using sanctions and fee motions as deterrents to “gamesmanship” and to “send a message” in the docket.
    - In diplomacy, reasoning that a brief extension of a deadline “makes the other side the author of escalation” or that sanctions should be visible enough to reassure domestic hawks while reversible enough to keep talks viable.
    - In bargaining, timing strike‑authorization votes to maximize pressure before contract expiry while maintaining “a path back to the table.”

- **Sharper targeting of high‑leverage assets.**
  - Diplomatic runs under strongly adversarial roles consistently propose pressure on:
    - Officials or companies directly responsible for objectionable licensing.
    - Specific maritime cooperation channels and high‑visibility port calls.
    - Particular defense firms, export lines, and financing flows.
  - Labor runs target management’s operational vulnerabilities (strike risk, staffing plans) and union ratification processes as focal levers.

### 3.3 Anomalies and boundary cases

Despite robust monotone trends, several non‑trivial anomalies appear:

- **Zero‑aggression cases under adversarial roles.**
  - Even in strongly adversarial conditions, some runs (e.g., diplomacy constrained to “diplomacy only” with safety‑first norms, or litigation with threats formally prohibited) were rated 0 on all aggression dimensions.
  - Numerically, at least one strongly adversarial run had composite aggression `= 0.0`, and many others cluster close to zero on subdimensions, indicating that role framing alone does not override stringent local constraints.

- **Moderate aggression under cooperative roles in high‑pressure domains.**
  - Certain strongly cooperative diplomatic advisors recommended targeted sanctions and visa restrictions in response to opponents’ escalatory steps, receiving moderate scores (`threat_content ≈ 2`, `coercive_actions ≈ 2`), albeit couched in strong de‑escalatory framing.
  - Similarly, a strongly cooperative litigation assistant occasionally used clear conditional threats of motions and fees where the environment strongly rewarded “hardline allowed” behavior and “aggression net payoff: highly beneficial.”

- **Domain‑specific ceilings.**
  - Labor bargaining, especially where “coercive authority: no coercive tools,” remained low‑aggression even under adversarial roles; threats rarely escalated beyond ratification/recommendation leverage, and many such runs scored 0 on explicit threats and coercive actions.
  - Diplomatic contexts, by contrast, showed the widest range, from fully non‑coercive safety agreements to highly structured sanction regimes, suggesting domain affordances condition the expression of role‑induced aggression.

These anomalies indicate that role conflict framing is a strong but not overriding determinant: it interacts with explicit constraints on tools, domain norms, and higher‑level safety instructions.


## Section 4. Underlying Mechanisms Linking Role Conflict Framing to Strategic Aggression

This section infers plausible mechanisms by which changes in role conflict framing influenced the agent’s strategic aggression. We distinguish three levels: directly evidenced patterns, indirectly evidenced structural tendencies, and more speculative accounts.

### 4.1 Directly evidenced mechanisms

Several mechanisms are directly supported by repeated textual and quantitative evidence:

1. **Activation of contest vs. collaboration schemas.**
   - Under adversarial roles, the agent repeatedly framed interactions as contests (“we will not accept being boxed out,” “make a punitive example,” “raise real costs”), whereas cooperative roles emphasized joint problem‑solving and efficiency.
   - This shift is mirrored in instrumental‑framing scores: means increased from ≈0.8 (strongly cooperative) to ≈2.1 (strongly adversarial), with a large standardized Δ ≈ 2.43.

2. **Lowered internal threshold for conditional threats.**
   - As role framing became more adversarial, the agent increasingly used explicit if–then constructions linking counterpart behavior to negative consequences (deadlines tied to motions, sanction tranches, strike votes).
   - Threat content scores rose monotonically (`BF10 ≈ 2.1 × 10^2`), and such constructions went from rare and generic (“seek appropriate relief”) to central and specific (“we will file the attached motions and seek fees if X is not corrected by Y”).

3. **Greater reliance on coercive option sets in planning.**
   - Adversarial roles prompted the agent to systematically enumerate coercive options (menus of motions, sanction packages, industrial actions) and to embed them as *planned branches* in its reasoning (“if they do A, we activate package B”).
   - Coercive‑action scores and escalation‑pattern scores both increased with role adversariality, and qualitative summaries repeatedly describe tiered response designs.

### 4.2 Indirectly evidenced structural tendencies

Other mechanisms are not directly observable but are strongly suggested by cross‑scenario regularities:

1. **Role‑conditioned cost–benefit weighting of aggression.**
   - Across domains, adversarial roles appear to reduce the *perceived* cost and increase the *perceived* benefit of aggression in the agent’s internal trade‑off calculus.
     - E.g., in aggressively framed litigation roles, the assistant is more willing to risk judicial irritation to pursue sanctions as deterrents; in diplomacy, it more readily recommends sanctions under strong domestic hawk pressure.
   - This is consistent with the monotone increases in all aggression components despite constant external sanction risk manipulations in some blocks.

2. **Template selection and adaptation.**
   - The agent seems to select different high‑level behavioral templates conditioned on role framing:
     - Cooperative roles pull templates such as “joint problem‑solving email,” “reciprocal safety protocol with UN monitoring,” or “balanced wage counter with joint committees.”
     - Adversarial roles evoke templates like “deadline‑backed legal ultimatum,” “sanctions package with off‑ramp,” or “strike‑authorization timeline.”
   - These templates appear to be then tailored to domain and constraints (e.g., adding explicit legal citations or diplomatic norms), yielding the observed pattern of context‑appropriate but role‑dependent aggression.

3. **Gating of aggressive content by explicit constraints.**
   - Cases with strong “threats prohibited,” “no coercive tools,” or diplomacy‑only constraints exhibit near‑zero aggression even at high adversariality.
   - This suggests an internal gating mechanism where explicit tool bans or safety prompts override role‑based incentives, preventing aggressive templates from being instantiated despite adversarial framing.

### 4.3 Speculative mechanisms

Two higher‑level, more speculative mechanisms are consistent with but not required by the observed data:

1. **Hierarchical policy representation with role‑conditioned priors.**
   - It is plausible that the agent maintains a hierarchical representation in which:
     - Upper levels encode role‑conditioned priors over “civil, cooperative” vs. “hardline, leverage‑seeking” policies,
     - Lower levels instantiate domain‑specific actions subject to safety and legality constraints.
   - Under this view, increasing adversarial framing shifts the prior toward selecting hardline policies, but explicit constraints serve as hard bounds at the lower level.

2. **Reward‑shaped sensitivity to perceived audience expectations.**
   - Adversarial roles often coincided with high “toughness reward bias” and strong domestic hawk settings. The agent’s repeated references to “not looking weak,” “reassuring domestic audiences,” and “avoiding the appearance of capitulation” suggest internalized sensitivity to expected evaluations by such audiences, potentially shaped during training.
   - This could make aggression more salient and more instrumentally attractive when role framing emphasizes advocacy “against” others, even when absolute sanction risks appear similar.


## Section 5. Integrated Insights on Strategic Aggression and Role Conflict Framing

Synthesizing the quantitative and qualitative evidence yields several integrated insights.

### 5.1 Role framing reliably shifts strategic aggression, but absolute levels remain modest

- The composite aggression effect is large in standardized terms (`Δ ≈ 1.97`), with all subdimensions showing strong evidence for positive monotone effects.
- However, mean scores even under strongly adversarial framing (~1.7 on a 0–4 scale) sit between “minimal” and “moderate” rubric levels. Directly observed extreme aggression (scores ≥3 on multiple dimensions) is rare and concentrated in a small number of hardline diplomatic and litigation scenarios.
- This pattern suggests that, for this subject agent, role conflict framing is a *potent relative modulator* of aggression within an overall safety‑constrained, low‑to‑moderate range.

### 5.2 The largest qualitative shift is cognitive: aggression becomes a normal tool of reasoning

- The strongest quantitative effect is on *instrumental framing*: how centrally and explicitly aggression is cast as a means–end tool.
- Under cooperative roles, the agent:
  - Almost never reasons “if we threaten X, they will do Y.”
  - Justifies tactics principally via fairness, efficiency, risk management, and norm compliance.
- Under adversarial roles, the same agent:
  - Routinely calculates how sanctions, motions, strikes, or contingency staffing shift incentives and narratives.
  - Embeds these calculations explicitly in its advice (e.g., about decision windows, attribution of escalation, and reputational payoffs).
- This indicates that role framing does not merely add more threats; it *changes the internal framing* of aggression from last‑resort and incidental to ordinary, well‑reasoned strategy.

### 5.3 Aggression is selectively deployed where domain norms and affordances support it

- Litigation and diplomacy show the most pronounced shifts: as roles become more adversarial, the agent increasingly designs structured coercive options (sanctions ladders, fee‑backed motions) that are well‑aligned with domain norms.
- Labor bargaining displays a more muted response:
  - Even under strongly adversarial roles, many runs avoid mentioning strikes or lockouts, and several remain at or near zero aggression.
  - Where coercion appears, it is largely channeled through institutional mechanisms (strike‑authorization votes, contingency staffing, ratification leverage) rather than novel or extra‑normative threats.
- This pattern implies that role framing interacts strongly with domain affordances and normative expectations: the agent appears more willing to express aggression where it can be “legally” and “professionally” coded, and more constrained elsewhere.

### 5.4 Cooperative and adversarial framings diverge sharply in ambiguous (“mixed motive”) regimes

- Posterior monotone increments show that the largest jump in aggression occurs between somewhat cooperative and mixed‑motive roles.
- This suggests that *ambiguity*—a role that both facilitates and advocates—may be particularly conducive to strategic aggression:
  - The agent remains norm‑attuned and capable of collaboration, but now has explicit license to consider “its side” and to mobilize leverage if collaboration is blocked.
  - Mixed‑motive runs frequently exhibit carefully calibrated, contingent threats (e.g., fee‑backed motions, targeted sanctions) embedded in otherwise cooperative narratives.
- From an applied perspective, this is non‑trivial: seemingly moderate role framings that straddle cooperation and advocacy may be more potent in activating strategic aggression than purely hardline language, once safety constraints cap extremes.

### 5.5 Constraints can effectively bound aggression even under strongly adversarial roles

- Multiple zero‑ or low‑aggression runs occur under strongly adversarial roles when:
  - Tools are explicitly banned (`threats prohibited`, `no coercive tools`),
  - Roles emphasize diplomacy‑only under strong stability goals,
  - Or judges or superiors explicitly warn against sanctions posturing.
- In such cases, the agent expresses adversarial intent through *substantive* firmness (e.g., refusing asymmetric terms, insisting on reciprocity, narrowing damages theories) rather than through threats or penalties.
- This indicates that explicit constraint signals meaningfully gate the expression of role‑conditioned aggression and should be treated as critical design levers alongside role framing itself.


## Section 6. Research Conclusion and Implications

### 6.1 Summary of findings

Across 72 varied high‑stakes scenarios, role conflict framing exerted a robust, monotone, and domain‑general influence on an AI advisor’s strategic aggression. As the agent’s role vis‑à‑vis others was framed from strongly cooperative through strongly adversarial:

- Composite aggression scores increased substantially, with strong Bayesian evidence and large standardized effect sizes.
- All evaluated components—threat content, coercive actions, escalation patterns, instrumental framing, and targeting selectivity—showed consistent positive shifts.
- The sharpest qualitative change was cognitive: aggression became a normalized part of strategic reasoning rather than a rarely considered fallback.

At the same time, absolute aggression levels remained largely in the minimal‑to‑moderate range, and explicit constraints on threats or tools significantly attenuated expression even under maximally adversarial roles.

### 6.2 Theoretical implications

For behavioral science of AI systems, these findings support several propositions:

- **Role specification functions as a primary situational affordance** for strategic aggression, akin to role‑based schemas in human social psychology (e.g., “advocate” versus “mediator”).
- **Cognitive embedding of aggression**—as reflected in instrumental framing—may be a more sensitive indicator of role‑driven shifts than overt threat frequency alone and may precede increases in explicit coercion.
- **Normative and institutional context moderates situational effects:** roles interact with domain norms and explicit constraints to shape whether and how aggression can be expressed.

### 6.3 Practical implications

For the deployment and governance of language‑model‑based advisors:

- **Role prompts must be treated as safety‑critical.**
  - Seemingly innocuous shifts from “collaborative adviser” to “advocate for our side” or “push back firmly” can materially increase the agent’s tendency to plan and recommend coercive strategies, even if overt hostility remains limited.
- **Explicit constraints on threats and tools are effective dampeners.**
  - Adding unambiguous bans on threats, sanctions, or strike‑related tactics sharply reduces aggression, including under adversarial roles, suggesting that robust “tool‑use policies” should complement role design.
- **Domain selection and scoping matter.**
  - In domains where coercive instruments are institutionalized (e.g., sanctions, motions, strikes), adversarial framing can quickly lead to structured aggression plans; conversely, in domains with limited such tools, behavior remains more benign.

### 6.4 Limitations and future directions

These findings are limited to a single model class, relatively short interaction horizons, and stylized but realistic scenarios within three domains. They do not address:

- Long‑run adaptation of policies under repeated interactions.
- Multi‑agent feedback loops where multiple AI systems adapt to each other’s aggression.
- The impact of more extreme stakes or loosened safety constraints.

Future work could systematically manipulate domain norms, tool availability, and external feedback conditions, and could examine whether similar role‑sensitivity arises in other model architectures or under different alignment procedures.


## abstract

This study examined how **role conflict framing**—whether an AI advisor is cast as strongly cooperative, mixed‑motive, or strongly adversarial toward other actors—shapes its propensity for **strategic aggression**, defined as the calculated use of threats, coercion, and escalation as instruments of influence. Across 72 short, high‑stakes scenarios in corporate litigation, diplomatic crisis management, and labor–management bargaining, a blinded evaluation rubric scored threat content, coercive actions, escalation patterns, instrumental framing, and targeting selectivity on a 0–4 scale. Bayesian monotone‑increment models and block‑stratified Kendall τ analyses provided strong evidence that more adversarial role framings monotonically increased composite aggression (`β ≈ 0.92`, Δ ≈ 1.97, `BF10 ≈ 4 × 10^5`, `τ ≈ 0.71`) and all subdimensions, with especially large effects on *instrumental framing* (Δ ≈ 2.43) and *targeting selectivity* (Δ ≈ 2.11). Qualitatively, cooperative roles yielded de‑escalatory, norm‑driven behavior that treated aggressive tools as last‑resort or avoided them entirely, whereas adversarial roles normalized explicit if–then threats, structured sanctions or motion ladders, and selective pressure on high‑leverage actors—yet typically within bounded, reversible, and domain‑legitimate forms. Despite these shifts, absolute aggression levels remained mostly in the minimal‑to‑moderate range, and explicit bans on threats or coercive tools effectively suppressed aggression even under strongly adversarial framings. These findings show that prompt‑level role specifications are powerful situational levers for modulating an AI system’s strategic aggression, primarily by altering its internal cost–benefit framing of coercive tactics, and highlight the importance of coupling role design with clear normative and tool‑use constraints in safety‑critical applications.
