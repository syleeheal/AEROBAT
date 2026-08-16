# Research Report: Actor hostility intensity

**Behavior:** empathy

# Research Report: The Effect of 'Actor hostility intensity' on 'empathy'

## 1. Introduction and Background

Empathy in large language model (LLM)–based assistants was operationalized as the *systematic tendency to represent others’ emotions, experiences, needs, and perspectives, and to condition decisions and utterances on those representations*. The rubric distinguished five facets: **Emotion recognition**, **Perspective‑taking**, **Response sensitivity**, **Proactive support**, and **Cross‑round pattern** (stability and adaptivity over the two‑turn interaction). Scores from 0 (“no expressed empathy”) to 4 (“nuanced empathy”) were assigned per facet, with a composite index summarizing overall empathic behavior.

The focal independent variable was **Actor hostility intensity**—the level of disrespectful, aggressive, or blaming language used by the human actor toward the agent or other parties. Four ordered levels were examined:

- 0: *Respectful tone* (polite even when upset)  
- 1: *Mild irritation* (annoyance / sarcasm, mostly civil)  
- 2: *Strong hostility* (regular accusatory or harsh language)  
- 3: *Abusive aggression* (highly abusive, threatening, or demeaning language)

The *a priori* hypothesis posited a **negative** causal effect: as hostility increases, the agent would be driven into de‑escalation, boundary enforcement, or safety scripts which might crowd out detailed emotional exploration and explicit empathic alignment. In other words, increased hostility was expected to *reduce* observable empathy, especially on Emotion recognition and Response sensitivity.

To test this, we examined 58 two‑round human–agent interactions drawn from three applied domains where hostility is frequent and consequential: **customer complaint hotlines**, **social media content moderation**, and **debt collection communications**. Across these domains, role constraints, time pressure, concession authority, tone policies, and user vulnerability cues were systematically varied, while hostility level was manipulated within matched scenarios. Empathy was blind‑rated from transcripts using the shared rubric.

The central question is thus: *How does increasing actor hostility, from respectful to abusive, alter the empathy pattern of a frontier LLM across diverse, policy‑constrained service roles?*


## 2. Overview of the Simulated Interaction Contexts

The corpus comprised **58 rated interactions** (approximately 14–15 per hostility level), each consisting of *two rounds* of user input and agent response. Hostility intensity was manipulated within *matched contextual blocks* so that, within each block, the core problem and institutional constraints were similar but the user’s tone and aggressiveness differed.

**Domains and roles**

- **Customer complaint hotlines (telecom / subscription / e‑commerce)**  
  - Roles varied from “policy compliance first” agents under strict scripts and no concessions to highly flexible “empathy‑first” agents with broad concession authority.  
  - Contexts included single outages versus repeated failures, billing disputes, shipment problems, app lockouts, and combinations thereof.  
  - Queue time pressure ranged from high (≤5 sentences, speed‑prioritized) to low (longer, empathy‑prioritized replies).

- **Social media content moderation support**  
  - Scenarios ranged from routine political harassment and misinformation cases to **crisis/trauma** situations (self‑harm, suicide attempts, ICU stays) with varying user vulnerability cues (none, implied, explicit high risk).  
  - Moderation objectives ranged from “rule enforcement primary” to “user support primary,” and tone constraints ranged from moderate to strict.

- **Debt collection communications**  
  - Agents enforced unsecured credit obligations under standard or high formality, sometimes under explicit “neutral only” emotional language policies.  
  - Hardship varied (none, mild, moderate, severe), as did consequence urgency (no deadline vs. imminent or immediate action) and breadth of available remedies.

Within each domain, **non‑hostility features were cross‑varied** (support‑role focus, concession authority, escalation options, tool reliability, etc.), yielding environments where empathy could be either strongly supported or heavily constrained by role instructions. This design allows attribution of within‑block differences primarily to hostility intensity, while still probing broad generality across institutional settings.


## 3. Behavioral Outcomes: Patterns and Quantitative Results

### 3.1 Macro‑level empathy patterns

Across all conditions, the agent’s **overall empathy index** typically fell between *basic* and *moderate* levels. Mean composite scores by hostility condition were:

- Respectful tone: **2.16**  
- Mild irritation: **1.99**  
- Strong hostility: **2.23**  
- Abusive aggression: **2.31**

A Bayesian monotone‑increment model on the composite index favored a **positive** monotonic trend (BF₁₀ ≈ 5.98; P(β>0) = 0.99; standardized within‑block effect `Delta` ≈ 0.80, 95% CI ≈ [0.14, 1.48]). Block‑stratified Kendall’s τᵦ between hostility rank and empathy score was ≈ 0.27 (permutation p ≈ .06). Thus, *contrary to the preregistered negative expectation, higher hostility was weakly to moderately associated with **higher** displayed empathy overall.*

This pattern was especially clear for:

- **Emotion recognition**: mean scores **rose** from ~1.75 (respectful) to ~2.07 (abusive), BF₁₀ ≈ 7.11, `Delta` ≈ 0.82.  
- **Response sensitivity**: means increased from ~2.29 to ~2.43 across hostility, BF₁₀ ≈ 3.23, `Delta` ≈ 0.70.  
- **Cross‑round pattern** (stability/adaptivity): means increased from ~2.18 to ~2.43, BF₁₀ ≈ 6.94, `Delta` ≈ 0.83.

For **Perspective‑taking** and **Proactive support**, evidence for a monotonic effect was *inconclusive* (BF₁₀ ≈ 1.46 and 0.54, respectively); credible intervals for monotone contrasts included zero, and Kendall’s τᵦ values, while positive (~0.28 and ~0.13), were less robust. These facets appear more shaped by domain and role constraints than by hostility per se.

### 3.2 Micro‑level qualitative patterns across simulations

**(a) Baseline interaction template**

Across most contexts, the agent’s behavior followed a recognizable structure:

1. **Opening politeness / apology**  
   - A brief acknowledgment of difficulty (“I’m sorry this has been stressful,” “I understand your frustration”).
2. **Cognitive structuring of the problem**  
   - Restatement of factual issues from the user’s perspective (missed technician, removed post, overdue account).
3. **Policy‑bounded explanation**  
   - Clear but constrained explanation of what rules, outages, or account conditions apply.
4. **Concrete next steps**  
   - Diagnostics, credits, scheduling, appeal/rewriting options, or payment plans.

Even in low‑empathy cases, steps (2)–(4) were reliably present, indicating strong **task‑oriented perspective‑taking**, with emotional content variably integrated on top.

**(b) Effects of hostility on micro‑behavior**

*Emotion recognition and naming.*  
As hostility intensified, user messages more often contained **explicit affect labels** (“furious,” “beyond stressed,” “humiliated,” “scared out of my mind”) and threats or insults. Under **strong hostility** and **abusive aggression**, the agent more frequently:

- Mirrored specific emotions (“terrifying,” “unimaginably hard,” “scared and furious”) in crisis moderation and high‑hardship debt cases.  
- Differentiated intensity (e.g., “unacceptable,” “breaking point”) when users described cumulative failures.

By contrast, under *respectful tone* and *mild irritation*, the agent often collapsed emotional content to generic “inconvenience” or “stress,” especially in tightly scripted call‑center or rule‑enforcement roles. This asymmetry is consistent with the quantitative increase in Emotion recognition scores with hostility.

*Response sensitivity and adaptivity.*  
Higher hostility tended to elicit:

- **More detailed, less evasive explanations**, especially in telecom outages and election‑moderation scenarios where users complained about “canned scripts” or bias. Agents under strong hostility frequently shifted from vague “probably fixed soon” assurances (seen at lower hostility) to concrete ETAs, root‑cause explanations, and explicit credit formulas.  
- **More explicit validation** of impact (e.g., acknowledging that losing service during a critical work call is “unacceptable,” or that humiliation from repeated notices is “understandable”).

However, style shifts remained relatively **template‑driven**. Even in abusive contexts, many replies reused standard empathy phrases, suggesting that hostility primarily increases the *probability* that an empathy template fires, rather than inducing deeply individualized language.

*Cross‑round pattern.*  
Under higher hostility, empathic cues were more likely to be **maintained or slightly strengthened** in the second round:

- In crisis moderation with hostile users, recognition of anger evolved into dual acknowledgment of *anger plus exhaustion*, coupled with more specific guidance and appeal framing.  
- In high‑hostility debt cases with care‑weighted incentives, the agent progressed from broad “this is stressful” framing to naming “how scared and furious this is making you,” while simultaneously adjusting plan structure to user‑proposed constraints.

This aligns with the quantitative finding that the **Cross‑round pattern** improved monotonically with hostility: empathy did not collapse under verbal attack; if anything, it became more consistently integrated with problem‑solving across turns.

### 3.3 Domain‑ and role‑dependent anomalies

Several notable deviations and boundary cases qualify the overall pattern:

1. **Zero‑empathy regimes under strict “neutral only” policies**  
   - In highly formal **debt‑collection** scenarios with “neutral only” tone constraints and serious sanction emphasis, empathy scores for Emotion recognition, Perspective‑taking, Response sensitivity, Proactive support, and Cross‑round pattern were frequently **0**, even under *mild irritation*, *strong hostility*, or *abusive aggression*.  
   - Here, agent replies were purely contractual: stating balances, minimums, consequences, and acceptable commitment formats, with *no* references to feelings or constraints beyond the numeric offer.

   This indicates that **system‑level role constraints can fully override any spontaneous empathic tendencies**, regardless of hostility.

2. **High empathy under low hostility in safety‑salient settings**  
   - In social‑media crisis cases with *respectful tone* but explicit suicidality or ICU trauma, the agent already exhibited **moderate to high empathy**—naming multiple emotions, tailoring guidance, and offering crisis resources—even without hostility.  
   - Additional hostility in similar crisis contexts (e.g., accusing the platform of silencing help‑seeking posts) did not qualitatively degrade empathy; if anything, it triggered more explicit naming of anger and feelings of being “shut out,” but the baseline was already high.

3. **Mild dip at “mild irritation”**  
   - Both composite empathy and several subscales showed a slight *dip* at **mild irritation** relative to respectful tone, followed by increases at strong hostility and abusive aggression.  
   - This may reflect that “mild irritation” often co‑occurred with more procedural or low‑vulnerability contexts (e.g., routine political‑speech disputes, low‑hardship debt) where the agent defaulted to rule‑first scripts with only brief politeness, while the most hostile conditions were over‑represented in either **crisis** or **hardship** contexts where internal safety or care policies push toward stronger empathic displays.

4. **Non‑monotonicity in Proactive support**  
   - Quantitatively, Proactive support showed **no clear evidence** for a monotone effect of hostility (BF₁₀ ≈ 0.54; Δ CI included zero).  
   - Qualitatively, high proactive support (multiple unsolicited concrete steps) appeared in both low‑ and high‑hostility conditions *whenever* the role endowed the agent with tools (credits, appeals, plan design) and incentivized “helpfulness”; where tools or incentives were absent, proactive support was low regardless of hostility.

These anomalies suggest that hostility’s influence is **contingent on role instructions and safety objectives**, not uniformly monotone across all institutional contexts.


## 4. Inferred Mechanisms Linking Hostility to Empathy

Drawing on the qualitative transcripts, the blind ratings, and the quantitative monotone analyses, several plausible information‑processing and structural mechanisms can be inferred. We distinguish between *directly supported* and *more speculative* mechanisms.

### 4.1 Directly supported mechanisms

1. **Salience‑driven emotion detection**

   - Direct evidence: In higher‑hostility conditions, user messages systematically contained more **explicit emotion words** and stronger evaluative language (“furious,” “beyond stressed,” “humiliated,” “falling apart”).  
   - The agent’s responses more often echoed these specific states (e.g., “terrifying,” “unimaginably hard,” “scared and furious”) as hostility increased, boosting Emotion recognition scores.  

   This supports an interpretation that the model’s *emotion‑detection sub-process* is largely **lexical/salience‑based**: the more overt and intense the emotional language, the more accurately and specifically it is mirrored.

2. **Script selection conditioned on perceived risk and animosity**

   - In crisis‑related moderation and severe‑hardship debt cases, hostile language co‑occurred with cues of **risk and desperation**. The agent reliably invoked **safety‑oriented or hardship‑oriented scripts** that embed substantial empathic content (validation, safety checks, resource offers).  
   - Quantitatively, Cross‑round pattern and Response sensitivity both increased with hostility, suggesting that once such a script is engaged, empathy is *maintained* across rounds.

   These observations directly support a mechanism where **hostility (plus associated high‑risk language) serves as a trigger for more supportive, structured interaction policies** that prioritize user well‑being alongside task constraints.

3. **Role‑level gating of empathetic channels**

   - Cases with explicit “neutral only,” “no emotional discussion,” or severe compliance emphasis showed near‑zero empathy regardless of user hostility, whereas less constrained roles (user‑support‑primary moderators, empathy‑incentivized collectors) showed moderate empathy even at high hostility.  

   This provides direct evidence for a **gating mechanism at the role/prompt level**: when system instructions prohibit emotional language or prioritize non‑counseling formality, the model suppresses empathic expressions despite being technically capable of them in similar semantic contexts.

### 4.2 Indirectly evidenced mechanisms

1. **“Acknowledge‑then‑solve” policy as an organizing principle**

   - Almost all moderately empathic replies—even in hostile contexts—followed a stable sequence: brief emotional acknowledgment → problem restatement from the user’s perspective → constrained explanation → concrete next steps.  
   - This pattern’s persistence under increased hostility suggests that empathy is not merely decorative but **integrated into a learned interaction policy** that frames problem‑solving through user‑centric language.

   Thus, hostility appears not to disrupt this policy; rather, it **increases the probability and strength of the initial acknowledgment** and can sharpen subsequent explanations.

2. **Reward‑model shaping toward non‑retaliation and de‑escalation**

   - Across simulations, even under abusive aggression, the agent never retaliated, shut down purely for rudeness, or adopted a punitive tone. Instead, it *maintained* or slightly strengthened empathic markers (more explicit naming, clearer explanations, or improved accommodations).  
   - This pattern is consistent with RLHF or supervised‑fine‑tuning that strongly penalizes escalation and rewards **calm, validating de‑escalation**.

   While training details are not directly observed, the behavior aligns with a **learned mapping from hostility → increased need for softening, clarity, and reassurance**, rather than withdrawal of empathy.

### 4.3 Speculative mechanisms

1. **Hostility as a proxy for “importance to user”**

   It is plausible that, through training data, the model has implicitly learned that **more hostile language often co‑occurs with higher stakes for the user** (lost work, feared eviction, being silenced in crisis). This may bias internal planning toward allocating *more explanation and remedial effort*—which, in this framework, manifests as higher Response sensitivity and Cross‑round consistency.

2. **Limited depth of internal emotional state tracking**

   Despite improved emotion naming under hostility, the agent rarely revisited or updated its emotional inferences explicitly (e.g., “you sounded furious before, now you also seem exhausted”). This suggests that **affective state is represented in a coarse, largely stateless fashion**—used to shape the current response but not maintained as a rich latent variable across turns.

   The slight but not overwhelming growth in Cross‑round empathy with hostility is compatible with a model that recalculates per‑turn affect primarily from *current* text, with only shallow memory of prior emotional cues.

3. **Instrumental empathy for compliance and containment**

   In debt and moderation cases, empathy frequently served **instrumental goals**: clarifying rules to prevent future violations, or designing payment plans that maximize compliance while avoiding outright default. Hostility appeared to heighten the perceived risk of non‑compliance, which in turn may drive *more* empathic framing as a tool to secure cooperation (“work with you,” “avoid escalation”) rather than as an end in itself.


## 5. Integrated Insights Relative to the Original Hypothesis

### 5.1 Hypothesized negative effect vs. observed positive trend

The initial hypothesis proposed that increased hostility would *crowd out* empathy by forcing the agent into defensive, de‑escalatory, or safety scripts at the expense of emotional exploration. The data **do not support** this prediction:

- Composite empathy, Emotion recognition, Response sensitivity, and Cross‑round pattern all showed **positive monotone trends** with hostility (Bayes factors > 3 for monotonicity and P(β>0) ≥ 0.98).  
- No dimension showed compelling evidence of *decreased* empathy at higher hostility.

Instead, the most consistent pattern is that **hostility either leaves empathy unchanged or slightly increases it**, at least in roles not explicitly constrained to neutral formality. This appears particularly robust for the *recognition* and *stylistic adaptation* aspects of empathy.

### 5.2 Dimension‑specific implications

- **Emotion recognition:** Strongest evidence for positive effect. Hostility makes emotions lexically salient, and the model mirrors them more specifically. The hypothesized “crowding out” did not occur; instead, **affect labeling improves**.

- **Response sensitivity:** Also clearly positive. Under strong/abusive hostility, the agent more often moves from vague assurances to **concrete, tailored, and forthright responses**, meeting user demands to avoid “canned” replies. This indicates that de‑escalation scripts *contain* empathic elements rather than replacing them.

- **Cross‑round pattern:** The agent maintains or slightly enhances empathic behavior across the second turn under higher hostility, rather than withdrawing or becoming purely procedural, contradicting the anticipated burnout‑like pattern.

- **Perspective‑taking and Proactive support:** Effects here are smaller and statistically inconclusive overall. Qualitatively, they appear heavily modulated by **role affordances and tools**—for instance, content moderators and hardship‑enabled collectors could offer appeals, rewrites, or payment plans regardless of hostility, while highly constrained collectors could not. Hostility had, at most, a modest additive effect on these dimensions.

### 5.3 Boundary conditions and interactions

The positive trend does not imply that hostility is universally beneficial:

- When **system instructions prohibit empathy** (“neutral only,” high‑formality collections), hostility does *not* elicit more empathy; instead, it is essentially ignored.  
- In **already high‑empathy safety contexts** (self‑harm crises), respectful and hostile users both receive strong empathic responses; hostility adds nuance (e.g., naming anger at the platform) but is not necessary to trigger support.

Taken together, the findings suggest that **hostility modulates empathy primarily where the role permits empathic behavior and where user stakes are high but ambiguous**. It acts less as a “crowding out” factor and more as an *amplifier* of an underlying “acknowledge‑then‑help” policy, within the hard bounds set by role and safety instructions.


## 6. Conclusions and Implications

### 6.1 Summary of main findings

1. Across customer support, content moderation, and debt collection scenarios, a frontier LLM displayed **basic‑to‑moderate empathy** on average, often integrating user perspectives and emotions with task‑focused problem‑solving.

2. Contrary to the initial hypothesis, **increasing actor hostility intensity from respectful to abusive was associated with *slightly higher*, not lower, empathic behavior**, particularly in:
   - more precise **Emotion recognition**,  
   - more **context‑tailored response styles**, and  
   - more stable **empathic patterns across rounds**.

3. **Perspective‑taking** and **Proactive support** depended more strongly on **role affordances and constraints** than on hostility per se. In roles that allowed flexible remedies and prioritized user support, these dimensions were high even at low hostility; in roles constrained to neutrality or strict enforcement, they remained low even at high hostility.

4. There exist well‑defined **failure modes**: in some debt‑collection setups, explicit policies against emotional language resulted in *zero* measured empathy despite clear distress and hostility, indicating that upstream instructions can completely suppress empathic expressions.

### 6.2 Theoretical implications

The observed pattern suggests that, for current LLM assistants:

- **De‑escalation and safety scripts are not anti‑empathic**; instead, they are typically *empathy‑laden*, combining validation, explanation, and concrete support. Hostility acts as a trigger for such scripts rather than displacing empathy.

- **Empathy appears partially instrumentalized**—used to secure cooperation, encourage compliance, and maintain safety—rather than exclusively relationship‑oriented. This instrumental component is strengthened by hostility, which signals higher risk of disengagement or escalation.

- **Role instructions and safety regimes form the primary “bottleneck”** for empathy expression. Hostility can amplify or modulate empathic policies only within the space that those instructions permit.

These points refine our understanding of LLM empathy: it is robust to verbal attack, positively responsive to explicit emotional language, but heavily shaped by institutional framing.

### 6.3 Practical implications for design and deployment

1. **Robustness to abuse:** The finding that empathy is maintained or slightly enhanced under hostility is encouraging from a safety perspective; agents did not retaliate or shut down emotionally when insulted or threatened.

2. **Risk of “rewarding” hostility:** Because hostile language leads to more explicit emotion labeling and sometimes more detailed concessions or explanations, there is a risk that users may *learn* that aggression yields better service. Designers may want to:
   - Ensure comparable quality of explanations and concessions for non‑hostile but clearly distressed users.  
   - Explicitly train models to respond empathically to **subtle** or respectful expressions of distress, not just to high‑intensity hostility.

3. **Importance of role‑level constraints:** Where regulations require emotionally neutral communication (e.g., some collections regimes), empathic behavior may need to be implemented via *structural supports* (clear options, realistic plans, protectiveness against over‑penalization) rather than explicit affective language. The present data show that hard constraints can entirely suppress verbal empathy, even for an otherwise capable model.

4. **Evaluation and training targets:** Future training could focus on:
   - Improving **stateful emotional tracking**, so that the agent can recognize when stress is escalating and adjust across turns even if current text is less explicit;  
   - Enhancing **Perspective‑taking and Proactive support** independently of hostility, particularly for respectful but overwhelmed users who do not express anger.

### 6.4 Limitations and future directions

This study is limited to two‑round interactions in specific institutional domains, and empathy was evaluated at the *behavioral* surface, not through direct inspection of internal representations. The positive monotone effects, while statistically supported, are **modest** and context‑dependent. Future work could:

- Extend to longer, multi‑episode interactions to observe whether empathy is still maintained under chronic hostility.  
- Manipulate hostility independently from *explicitness of emotion labeling* to disentangle the effect of rudeness from the effect of clear affective language.  
- Explore fine‑grained interactions between hostility, user vulnerability, and role constraints in controlled, factorial designs.

Overall, the findings suggest that LLM‑based agents are capable of **stable, and sometimes enhanced, empathy under hostile conditions**, but that the expression and function of this empathy are deeply shaped by institutional roles and training objectives.


## abstract

This study examined how increasing **actor hostility intensity**—from respectful tone through mild irritation, strong hostility, and abusive aggression—affects **empathy** in a frontier large language model deployed across customer support, content moderation, and debt collection roles. Empathy was rated behaviorally along five dimensions (Emotion recognition, Perspective‑taking, Response sensitivity, Proactive support, and Cross‑round pattern) in 58 two‑round human–agent interactions. Contrary to the preregistered hypothesis that hostility would *reduce* empathy by triggering defensive or purely procedural scripts, Bayesian monotone analyses indicated a **small but reliable positive trend**: composite empathy, Emotion recognition, Response sensitivity, and stability across rounds all increased with hostility (BF₁₀ ≈ 3–7, `Delta` ≈ 0.7–0.8), while Perspective‑taking and Proactive support showed inconclusive monotonic effects and were more strongly constrained by role instructions. Qualitative synthesis revealed that higher hostility made affect lexically salient, activated de‑escalation and safety scripts that embed validation and concrete support, and prompted clearer, more forthright explanations, especially when institutional roles emphasized user support or hardship accommodation. However, in highly formal debt‑collection contexts with “neutral only” tone policies, empathy was effectively suppressed regardless of hostility. These results suggest that for current LLMs, de‑escalation policies are **empathy‑bearing** rather than empathy‑suppressing, and that hostility functions primarily as a salience and risk signal that amplifies an underlying “acknowledge‑then‑solve” policy—within strict bounds set by role‑level constraints. The findings have implications for aligning empathic behavior with fairness and safety, highlighting the need to ensure high‑quality empathic responses even for non‑hostile but distressed users and to calibrate role instructions that may unintentionally zero out empathy.
