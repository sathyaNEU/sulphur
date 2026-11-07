# Sulfur strategies: the union, minus what did not work

The author's rule for this file: classify which strategies worked in Mark and which will not; the ones that did not
work are marked so they are never built, because the models may have learned them; then take the union of Sulfur's
strategies and Mark's, minus the ones that do not work. Sources: the client's per-domain strategies
(`guidelines/client/learning-modules/stumping-strategied.txt`), the client's 15 accepted examples
(`guidelines/client/examples/`), and Mark's measured record (`strategies.md`, `evidence.md`, `shipped-ledger.md`,
`../SKILL.md` Parts 1 and 9).

## How to read the labels

| Label | Meaning | Build it? |
|---|---|---|
| **WORKS** | Mark's portal held it, or a client example stumped both runs with it and Mark records no death of that form | yes, with a new driver (the fingerprint guard blocks a repeat) |
| **WORKS IN FORM** | the strategy is sound, but Mark measured one form of it dying; the dead form is named and banned, the live form is stated | only in the live form |
| **DOES NOT WORK** | Mark measured it landing, or the client's own example notes call it single-insight; the models execute it | never as the deep step; it may sit at rung 0 or 1 of the ladder, as the shallow path the deep step overturns |
| **UNTESTED** | neither record measures it | yes, as fresh ground, with the screens run harder |

**Why a client-recommended strategy can still be DOES NOT WORK.** Mark's portal graded the top responses of many
runs; a step that one model in four takes by reflex was landed there. Sulfur grades two runs, so the same step can
pass on one platform round and fail the next, and once an approved task carries it, the models may learn it. Where
Mark measured a named method being executed by reflex, it is filed DOES NOT WORK here even when a client example
used it, and the client's own notes agree on the clearest cases (Example 14, clustering on the randomized unit,
"closer to a single-insight task", 0.59; Example 12, Lee bounds, a chain the client calls short, 0.45).

**What any DOES NOT WORK strategy is still good for.** Mark's law 1.1b: the field's named method belongs at rung 0 or 1,
written into `## Default path`, and the deep step is the recognition that this dataset violates that method's
precondition. A run that applies the method correctly and lands wrong is the intended failure (a method shortcut or
an unfinished chain, both of which the client counts as deep).

## Part A. The client's seven deep judgments, classified

| Judgment (client) | Mark's record | Label | The live form |
|---|---|---|---|
| **A comparison that is actually clean** | F9 causal design: no measured hold; died 107 v2 (a filed effect formula), 118 and 124 (the contamination readable), 230 twice (stratification a reflex), 193 v1 and v2 (the comparison population and its value filed in the estimand: no third position). Shipped 131 (a household's cards share baskets). Client: Examples 2 (0.46), 4 (0.24), 6 (0.57), 8 (0.40), 13 (0.44) accepted | WORKS IN FORM | The contamination is visible only through a relation in the data (the same app build carrying a push outage; areas started worst-first; leader-follower price pairs; waiting states that received the freed staff time; cities diverging before the rule), never a column, a schema or a filed sentence; the comparison is never filed in the estimand; and after the clean comparison is chosen the chain carries two more inferences (weighting to the decision's mix, the effect's uncertainty, the decision quantity) |
| **Heterogeneity that pooling hides** | F5 composition held (68, 83; pattern E approved on 30). Grouping as the step is dead (1.1c: per-class against pooled shows in the fit, likelihood ratio 511.1 on 668 df, and a blind reader fitted per class unasked). Client: Examples 1 (0.26), 5 (0.45), 6, 7 (0.55) | WORKS IN FORM | The groups respond differently AND the decision weights them to a population whose mix differs from the sample (next year's traffic, the system that will adopt, the treated population), with the group property rebuilt from a history (a per-customer use count), never read off a column. Dead form: the deep step is "estimate it by segment instead of pooled" |
| **Uncertainty that matches the design** | G17 statistical rigor: supporting only; 6 of 12 textbook routes landed in-house, clustered errors a house reflex (`evidence.md` 1.1j); a filed confidence level is a filed method once only a variance remains (readability test 1). Client: Example 14 (0.59, "closer to a single-insight task"), Example 12 | DOES NOT WORK as the deep step | Only as one link of a longer chain whose deciding step is another judgment (the estimate the interval wraps needed its own judgment first). "Cluster by school" alone is a one-fact stump |
| **Variance beyond sampling noise** | A level at a selected unit is a shrinkage target and shrinkage is the opponent's reflex (James-Stein 40 of 40); a shrinkage choice moves about 8 per cent at most (G16). Approved 253 (a floor count is a sum of probabilities, not shrunken predictions). Client: Example 15 (0.50) | WORKS IN FORM | Standard shrinkage is the shallow path (rung 0 or 1) and the deep step is the variance component the standard model omits (a cohort-to-cohort term, a year-to-year persistence term), or a decision quantity that is a sum of probabilities. Dead form: shrinkage itself as the golden |
| **Separating two explanations for one pattern** | F8 attribution: held after repair 72, shipped 182 (each bore's own driver-only path fitted before the effect); died 36 (an argmax under a stated rule), 119 and 122 (a filed sentence), 228 twice (a reflex). A dated cause whose effect steps the series dies to an event study (36). Client: Examples 1, 3 (0.45) | WORKS IN FORM | Only a like-for-like comparison rebuilt from history separates the two (composition against behavior at a fixed use count; demand that drives spend); no explanation arrives as a dated cutover whose step an event study finds, and no filed sentence names the split |
| **Outcomes that have not finished happening** | F4 maturity: portal held 181 (each route's own reporting delay; the pooled-delay nowcast picks the wrong area). Died 134 loop 0 (Kaplan-Meier censored at the cut was the golden), 190 ("nowcast or count" settled by the WHAT). Client: Example 1 (open returns projected), Example 10 (0.43) | WORKS IN FORM | Completion speed differs by a unit no pooled factor captures (a route, a lab whose delay changed, a vintage, a channel), so the pooled or textbook completion factor files a named wrong answer. Dead form: the field's standard censoring or development method (Kaplan-Meier, one pooled chain ladder) is itself the golden |
| **A forecast that has to earn its place** | F6 method selection: held 46 (a rate law stationary in cumulative service exposure rebuilt from a movement log), approved 33, shipped 446 v2; died 38 (an enumerable model class behind a shipped back-test is an answer key, eleven rounds), 89 v5 and v6, 130 v3 (the analog default), 125. Law L6: pin by identity or exhaustion, never by fit. Client: Example 5 (0.45) | WORKS IN FORM | The invariant the right model rests on is constructed from a log, the back-test the solver runs is its own, and no shipped test enumerates the winner; the forecast must beat the naive baseline out of sample and the committed level carry its uncertainty |

## Part B. The client's per-domain strategies, classified

Numbering follows the client file. "Banned" items are the client's own look-alikes and are always DOES NOT WORK.

| Domain | Strategy (client) | Label | Why, and the live form where there is one |
|---|---|---|---|
| Product Analytics | 01 Novelty that keeps getting topped up | WORKS IN FORM | F1's legal form: a clock process (time since each user's exposure) estimated from every unit that went through it; never a dated cutover |
| Product Analytics | 02 A flat average over segments moving in opposite directions | WORKS IN FORM | Part A heterogeneity: decides through reweighting to the future mix; partial pooling is not the golden |
| Product Analytics | 03 Clustered randomization with a few giant clusters | DOES NOT WORK | Part A design uncertainty as the deep step |
| Marketing | 05 Targeting the persuadable instead of the likely | WORKS IN FORM | The uplift or Qini method sits at rung 0 or 1; the deep step is what this holdout violates (contamination, an exposure the randomization did not cover) |
| Marketing | 06 Platform-credited conversions against a market test with few markets | WORKS IN FORM | Synthetic control as the golden is a named method (1.1b); the deep step is a donor-pool or pre-period condition the data show broken |
| Marketing | 07 Stated intent calibrated against your own launches | UNTESTED | A calibration corpus is an organ; a corpus with one surviving fit over a scannable set is an answer key (Mark Part 6), so the forward population must differ from every settled launch on a property the history shows |
| Quantitative Finance | 01 Validation the strategy could not have tuned to | WORKS IN FORM | F6 and F7: point-in-time universes, delistings and the search discount are live; a shipped back-test over an enumerable variant set is an answer key |
| Quantitative Finance | 02 Risk that moves with the regime | UNTESTED | Decay tested out of sample (F6 constraints) |
| Quantitative Finance | 03 Inference that matches how the sample was drawn | DOES NOT WORK alone | Overlap correction alone is a one-fact stump (the client says so: pair it with the persistent-regressor bias "so the one-fact test fails"); live only as the client's compound |
| Banking | 05 Seasoning, vintage and calendar in default curves | WORKS IN FORM | F4: immature vintages projected with speeds that differ by vintage; a pooled seasoning curve files the named wrong answer |
| Banking | 06 Selection in who you can observe | WORKS | F7 population selection (approved 25, 28; shipped 229, 132): the selection built from histories (a random-approval cell against selected overrides) |
| Banking | 07 Correlated defaults, not independent ones | UNTESTED | Excess variance beyond independence carried into the tail; pin so every reasonable dependence estimate clears the allocation |
| Actuarial | 09 Immature development and the tail | WORKS IN FORM | Chain ladder at rung 0 (Mark lists triangle development among the reflex families); the deep step is the precondition broken (a case-reserve adequacy shift visible in the data) and the tail fitted after it |
| Actuarial | 10 Exposure mix and credibility in an indication | WORKS IN FORM | F5: restating to the current mix decides; credibility weighting is a rung, never the golden |
| Actuarial | 11 Trend versus development | WORKS IN FORM | A calendar effect on every diagonal is a chronic trend, not a dated step; counting it once decides |
| General Statistics | 01 Validation that leaks through time or through groups | WORKS IN FORM | F6: grouped forward validation at the operating capacity, with no shipped test naming the winner |
| General Statistics | 02 A held-out set that does not look like deployment | WORKS IN FORM | F7 and F6: the deployment population rebuilt from history |
| General Statistics | 03 Calibration and discrimination when the decision uses a threshold | UNTESTED | Fresh ground |
| General Statistics | 04 Variance components and shrinkage when ranking many small units | WORKS IN FORM | Part A variance: shrinkage is the shallow path; the deep step is the variance component beyond it. Shrinkage as the golden DOES NOT WORK |
| General Statistics | 05 Dependence that breaks independent standard errors | DOES NOT WORK | Part A design uncertainty as the deep step |
| Biomedical | 01 Transporting a trial effect to the population that will be treated | WORKS IN FORM | Part A heterogeneity: the modifier's distribution differs in the treated population |
| Biomedical | 02 Competing risks in older or sicker cohorts | WORKS IN FORM | Kaplan-Meier is rung 0 (134 loop 0 died with it as the golden); the deep step is the competing-exit structure plus case mix, not a named estimator alone |
| Biomedical | 03 Cluster randomization with few, unequal clusters | DOES NOT WORK | Part A design uncertainty as the deep step |
| Epidemiology | 05 Nowcasting through a reporting delay that has changed | WORKS | F4's portal hold (181): each route's or lab's own delay |
| Epidemiology | 06 Excess mortality that has to be justified out of sample | WORKS IN FORM | F6: the baseline chosen by the solver's own out-of-sample check; no shipped test enumerates it |
| Epidemiology | 07 Vaccine effectiveness when vaccination and incidence both move through the season | WORKS IN FORM | F9: the calendar confounding visible in the data; a stratification that is the field's reflex died twice (230) |
| Pharmacology | 09 Immortal time from exposure defined after cohort entry | WORKS IN FORM | The immortal-time fix is a named correction (a reflex, 1.1b) at rung 1; the client's chain needs the residual confounding after the landmark to decide |
| Pharmacology | 10 Confounding by indication and the active-comparator new-user design | WORKS IN FORM | The design is a named method; it decides only where the data show a precondition broken (frailty imbalance the design does not remove) |
| Pharmacology | 11 Stimulated reporting and masking in spontaneous report data | WORKS IN FORM | Disproportionality is rung 0; the deep step is the reporting rate that changed after an alert, read from the reports' own timing |
| Healthcare Delivery | 13 Regression to the mean in programs started after a bad spell | WORKS IN FORM | Survives the WHAT screen (it files a true or future level, `evidence.md` 1.2); a correction sized by the selection's extremity measured worse than nothing (`../SKILL.md` Part 3), so the live form is concurrent units matched on the selection (Example 6) |
| Healthcare Delivery | 14 Case-mix adjustment with shrinkage for provider profiling | WORKS IN FORM | Shrinkage as the golden DOES NOT WORK; live only where shrinkage is the shallow path and case mix plus a variance component decide |
| Healthcare Delivery | 15 Selection into a pilot, then scaling to the whole system | WORKS IN FORM | F7 and F5: the pilots' own trends and the system's mix |
| Economics | 01 Staggered adoption with effects that grow | WORKS | Survives the WHAT screen (`evidence.md` 1.2); Example 4 (0.24) |
| Economics | 02 Comparison units contaminated by the treatment | WORKS IN FORM | Part A clean comparison: the spillover visible only through a relation in the data (Example 8) |
| Economics | 03 Average effect for the wrong population | WORKS IN FORM | F5 and F7: reweighted to the target population |
| Political Science | 05 Ecological inference that respects heterogeneity | UNTESTED | Heterogeneity decides; the named EI estimator alone is a rung |
| Political Science | 06 Nonresponse that weighting on demographics does not fix | UNTESTED | Mark's survey ground is its most crowded (29 cards): duplicate risk is high, read `guard.py mechanisms` first |
| Political Science | 07 Anticipation that contaminates the pre-period | WORKS IN FORM | Never a dated step an event study finds; the anticipation is a drift the pre-period shows |
| Sociology | 09 Age, period and cohort that point in different directions | WORKS IN FORM | APC is unidentified without a constraint: pinned by observed cohort paths the data carry, or it is an unpinned ambiguity |
| Sociology | 10 Composition change dressed as behavior change | WORKS | F5 held (68, 83); Example 1 |
| Sociology | 11 Duration that is censored and length-biased | WORKS IN FORM | Kaplan-Meier at rung 0; the length bias from the sampling design the data show |
| Psychology | 13 Attrition that depends on the outcome | DOES NOT WORK as specified | Lee or trimming bounds as the golden is a named method; the client calls Example 12's chain short. Live only with the bounds at rung 1 and another judgment deciding |
| Psychology | 14 Demand effects that only the unobtrusive measure exposes | UNTESTED | Separating two explanations; fresh ground |
| Psychology | 15 Between-site variation beyond sampling noise | WORKS IN FORM | Part A variance: the component beyond the standard model decides |
| Criminology | 17 Regression to the mean in where the program goes | WORKS IN FORM | As Healthcare 13 |
| Criminology | 18 Displacement against diffusion of benefits | WORKS IN FORM | Part A clean comparison: nearby areas contaminated, read from the data |
| Criminology | 19 Immature follow-up and a shifting release population | WORKS IN FORM | F4 with F5 |
| Physical & Environmental | 01 Censoring at shifting detection limits | DOES NOT WORK as specified | The client's build makes a censored estimator against substitution the deciding step: a named method as the golden (134 loop 0, 1.1b). Live only with the censored estimator at rung 1 and the shifting limits interacting with another judgment |
| Physical & Environmental | 02 Serial dependence and change points in sensor series | WORKS IN FORM | The upstream reference construction must be the judgment; the dependence-aware interval is a link (G17 supporting only); a dated change an event study finds is dead |
| Physical & Environmental | 03 Spatial dependence and preferential sampling | DOES NOT WORK as specified | Declustering against the raw mean is a named method as the golden; live only where declustering is rung 1 |
| Energy | 05 Weather normalization and the wrong baseline in savings verification | WORKS IN FORM | Regression to the mean (Healthcare 13 form) plus building-specific balance points (heterogeneity) |
| Energy | 06 Peak coincidence and load diversity in capacity planning | WORKS IN FORM | Mark's grid-reliability cell is its most spent anomaly ground (four cards); the coincidence estimated empirically from interval data, a new driver required |
| Energy | 07 Extreme tails versus normal assumptions | DOES NOT WORK as specified | A GEV or peaks-over-threshold fit against a normal fit is a named method as the golden (Mark's extreme-value family is a reflex) |
| Human Factors | 09 Learning and order effects in usability trials | WORKS IN FORM | The period and order effects visible in the data; a named crossover model alone is a rung |
| Human Factors | 10 Repeated measures analyzed as independent | DOES NOT WORK | Part A design uncertainty as the deep step |
| Human Factors | 11 Speed-accuracy tradeoffs that flip which design is better | UNTESTED | The curves interpolated at the operating pace; fresh ground |
| Survey | 01 Combine multiple imputation with the survey design | WORKS IN FORM | Two named methods compounding; one alone is a reflex. Crowded Mark ground |
| Survey | 02 Small-area estimates that borrow strength honestly | DOES NOT WORK as specified | Fay-Herriot shrinkage as the golden (James-Stein 40 of 40) |
| Survey | 03 Nonresponse bias that weighting does not remove | UNTESTED | Calibration on a linked auxiliary; crowded Mark ground |
| Urban | 01 Spillover and displacement around place-based investments | WORKS IN FORM | Part A clean comparison |
| Urban | 02 The modifiable areal unit problem when the question is about people | WORKS IN FORM | F2 grain: the decision's unit built from finer records with no key bridging the grains |
| Urban | 03 Net, not gross, regional economic impact | WORKS IN FORM | Separating explanations: the displaced activity estimated, never filed |
| Education | 01 Reliability-adjusted school effects with cohort-to-cohort variation | WORKS | Example 15 (0.50), the same shape as Mark's approved 253 |
| Education | 02 Measurement error in value-added | WORKS IN FORM | Example 11 (0.28) stumped both runs; the reliability must be estimated from the pack's own data (a filed reliability coefficient is one fact) |
| Education | 03 Regression to the mean when schools are picked for low scores | WORKS IN FORM | As Healthcare 13 |

## Part C. Mark's families that Sulfur does not list, classified

These join the union. A Mark driver that was approved is now in the client's hands and possibly in training data, so
the family is reusable and the driver never is (`guard.py heart` blocks it).

| Mark family | Record | Label | The live form under Sulfur |
|---|---|---|---|
| F1 Time: a clock the closed window never exercised | Portal held 102 and 107 v4, both validated decoys, now blocked; legal form shipped 134 v2 (a conversion hazard by time since entry) | WORKS IN FORM | A clock process estimated from every unit that went through it; never a validated decoy, never a dated cutover |
| F2 Grain: what one unit of the decided thing is | Portal held 103 v3 (the call held, the asks gave way); died 44 (an order id bridged the grains), 48, 67, 103 v1 and v2 | WORKS IN FORM | The unit constituted from a history, a place or a household, with no key bridging the grains; pair it with a statistical judgment, since the client requires one in the chain |
| F3 Binding constraint: a shared limit | Portal held 106 run 3; died on an argmax over a filed capacity vector (87) | WORKS IN FORM, lower rung only | Sulfur bans "if the top option breaks the cap, take the next" as rule application, and a constraint is not a statistical judgment, so it is one link of a chain whose deciding step is an estimate |
| F7 Population: who is in the denominator | Approved 25, 28; shipped 229, 132 (a replacement restarts the wear curve); died 100 v1 (a clause handed it over), 269 v4 (a population the estimand must name cannot be the step) | WORKS | The selection mechanism (on outcome, schedule, symptom, survival, replacement) built from histories, never a status word or clause |
| F10 Identity resolution | No hold; died 120, 121 twice, 81 v3, 90 | DOES NOT WORK as the deep step | Layer 1 or a lower rung; the client's shape 15 allows it only upstream of an estimate whose uncertainty depends on match quality |
| F11 Stated rule, hard construction | No hold; died 133 v1 (a portal model at 100), 107 v3, 67, 37 | DOES NOT WORK | Rule application, banned by Sulfur |
| F12 Uncertainty and hold | Never drawn | UNTESTED | A hold is legal only when reaching it takes work (`../SKILL.md` Part 3, G17); several client examples offer HOLD as an answer |
| F13 The withheld rule | Retired; the official-decoy form blocked | DOES NOT WORK | A planted rule, banned by Sulfur |
| The validated decoy | 27 of 30 builds from 99 to 130; blocked | DOES NOT WORK | Banned (a decoy) |

## Part D. Never build these (Mark's measured deaths, every one still binding)

From `strategies.md` Part 6 and `../SKILL.md` Part 9, in one place. Each is a form the models solved or a gate killed.

- **The field's named method as the golden**: landed every time Mark shipped it (139, 166 v1 and v2, 156, 137, 133,
  255, 273 v2 and v4, 464 v2, and 45 more in-house). The library test: a stump sentence reading "use X on Y" with X a
  named correction is a reflex.
- **The default construction as the golden** (134 loop 0, 130 v3, 62, 87 v6b, 100 v1): write the default path first.
- **A reading of a term** (133 v1, a portal model at 100): data semantics.
- **A quantity named by a filed sentence**, twelve landings, or by a helper document or the schema (six landings): the
  readable step.
- **A column one join away** (117, 119, 120 v1, 124 loop 0); relabelling the column was landed again.
- **A reflex correction**, ten landings; **the last link of the obvious chain**.
- **A control that nominates or refutes, or an oracle that ties only under the golden** (seven landings).
- **A filed rule over filed candidates** (37, 36): rule application.
- **A dated cause whose effect steps the series**: an event study finds it (36).
- **A grouping as the step** (1.1c) and **a level at a selected unit** (shrinkage is the reflex).
- **An estimator family with nothing in the data to close it**: an unpinned ambiguity.
- **The value of a counterfactual the estimand files** (193 v2): price the cheapest member first.
- **A pin naming the clock, window, test or population the stump rides on**: landed on the next round (141 SF33, 179
  v3, 181 v2, 118 v2).
- **A rung stacked above a solved step**, and **hardening the asks alone after a landed call**: never held.
- **Resisted over-correction (the reported figure is wrong)**: died every time (38 v2, 40, 62, 87 v6b); Sulfur bans
  it as replay or flip-the-wrong-number.
- **A planted defect deciding**: a copied block, test rows, a shifted clock, a hidden extract. Sulfur's examples 1,
  4, 13 and 14 carry planted-looking defects that decided nothing, which is the only legal use.

## Keeping this file current

A Sulfur run that lands a WORKS or WORKS IN FORM strategy moves it down one label here, with the run's row in
`sulfur-record.md` cited; a run that misses on an UNTESTED strategy for a deep reason moves it up. The move is a
`SKILLS:` commit. Two rows are needed to move a label; one row is noted beside the strategy.
