# Sulfur strategies: the client's atlas, indexed, and what Mark measured dead

The client's per-domain strategies (`guidelines/client/learning-modules/stumping-strategies.md`, exported
2026-11-09) are the starting point for every draw. Each strategy there names its analysis type and answer shape,
where the weight of the work sits, the investigation (the chain of hard results), where the difficulty already lives
in public data, a scenario with real breadth, where a hurried analyst goes wrong, what the solver delivers and how
each result is kept deterministic; each domain group ends with "Shallow versions of these ideas", the one-thing twins
of its own strategies with the client's verdicts. This file indexes them so a draw reads the right entries in one
pass, and keeps Mark's measured record of what the models execute.

## How to use the atlas

1. Find the assigned domain group below and read every entry whose analysis type matches the assignment, plus the
   group's shallow versions (the line numbers point into the export).
2. Take the **lesson**: which work is genuinely long in this field, where a hurried analyst goes wrong, how a result
   is pinned without naming the method. Never take the shape: "Copy the lesson, not the shape." The client's own
   strategies are on its reviewers' desks, so a build that walks one entry's investigation in its order with its
   deliverables is a reskin.
3. Write the chain from this world's own process (`../SKILL.md` 1.1), with the weight somewhere the last builds have
   not leaned (`guard.py check` blocks a repeat).
4. Check every hidden factor the chain needs against the shallow versions: the client sends back a factor the author
   built, placed only in the deciding units, found by one cross-tab and fixed by one routine step, and approves a
   hard method step on real behaviour (adding "would give careful work more to earn" when it stands alone).

## The index (77 strategies)

The analysis type and the weight are the export's own words; the line is where the entry starts.

**Product Analytics**

| # | Strategy | Analysis type | Weight | Line |
|---|---|---|---|---|
| 1 | A traffic decline with several causes at once | Root-Cause | Investigation-heavy | 70 |
| 2 | A purchase funnel that leaked in a few of many segments | Comparative & Explanation | Triage-heavy | 99 |
| 3 | Newer cohorts that come back less | Root-Cause | Synthesis-heavy | 124 |
| 4 | A tracker that changed under the series | Data Quality, Monitoring & Alerting | Measurement-heavy | 149 |
| 5 | Usage jumps against a baseline that swings by itself | Anomaly Detection & Diagnostics | Rule design | 177 |
| 6 | A paying base whose history started late | Forecasting & Predictive | Validation-heavy | 202 |
| 7 | Many experiments, read one at a time | Experiment & Causal | Modeling-heavy | 230 |
| 8 | Ratings from people who chose to rate | Descriptive & Distribution | Estimating a hard-to-measure quantity | 258 |
| 9 | Who to contact when the send budget is fixed | Opportunity Sizing & Decision Support | Allocation under a constraint | 286 |
| 10 | Two eras of categories in one table | Data Extraction & Conformation | Assembly-heavy | 311 |
| 11 | A category sales change with price, promotion and assortment all moving | Comparative & Explanation | Attribution-heavy | 339 |

**Quantitative Finance and Trading**

| # | Strategy | Analysis type | Weight | Line |
|---|---|---|---|---|
| 1 | Why a desk's P&L stopped explaining | Root-Cause | Investigation-heavy | 444 |
| 2 | A monitoring rule for a risk model, and what its alarms meant | Data Quality, Monitoring & Alerting | Rule design | 473 |
| 3 | A bridge from paper factor to real funds | Comparative & Explanation | Attribution-heavy | 498 |
| 4 | Slow-moving predictors, proven in real time | Forecasting & Predictive | Validation-heavy | 529 |
| 5 | Bond trade reports conformed into one record per trade | Data Extraction & Conformation | Assembly-heavy, then estimation of a quantity the public data hide | 559 |
| 6 | Effects from a real randomized market pilot | Experiment & Causal | Modeling-heavy | 589 |
| 7 | Pricing a seasoned loan pool | Opportunity Sizing & Decision Support | Estimation under censoring, feeding an optimization | 621 |
| 8 | Explaining a margin squeeze | Root-Cause | Synthesis-heavy | 646 |
| 9 | Where to cut the loss distribution for a securitization | Descriptive & Distribution | Estimation of a hard-to-measure quantity: how strongly defaults move together | 675 |
| 10 | A payment forecast with honest bands | Forecasting & Predictive | Uncertainty-heavy | 703 |
| 11 | Dating when excess claims ended | Anomaly Detection & Diagnostics | Measurement-heavy | 728 |

**Machine Learning Research**

| # | Strategy | Analysis type | Weight | Line |
|---|---|---|---|---|
| 1 | Which runs went wrong, and what went wrong first | Anomaly Detection & Diagnostics | Investigation | 842 |
| 2 | Splitting an eval regression across changes that shipped together | Root-Cause | Attribution | 873 |
| 3 | Where a run will land, read from its early curve | Forecasting & Predictive | Validation | 903 |
| 4 | Ranking runs fairly across seeds, test items and hardware | Comparative & Explanation | Measurement | 934 |
| 5 | Label errors in the yardstick | Data Quality, Monitoring & Alerting | Estimating a quantity nobody observes directly | 966 |
| 6 | Traffic spikes that are not people | Anomaly Detection & Diagnostics | Triage at breadth | 995 |
| 7 | A drift alarm that would ring every day | Data Quality, Monitoring & Alerting | Designing the rule itself | 1023 |
| 8 | Spares for failures you never saw start | Opportunity Sizing & Decision Support | Modeling, then allocation under constraints | 1054 |
| 9 | The effect of a shock that hit every unit | Experiment & Causal | Building the counterfactual | 1083 |
| 10 | Percentile cuts from a weighted, top-coded survey | Descriptive & Distribution | Recovering what the file hides | 1111 |
| 11 | One station series across a schema change | Data Extraction & Conformation | Assembly | 1139 |

**Biomedical and Health Sciences**

| # | Strategy | Analysis type | Weight | Line |
|---|---|---|---|---|
| 1 | Forecasting transplants from a waitlist where death and delisting compete | Forecasting & Predictive | Validation-heavy | 1239 |
| 2 | A starting-dose table from thousands of sparse, mistimed drug levels | Forecasting & Predictive | Modeling-heavy | 1270 |
| 3 | A screening threshold when only the positives were worked up | Opportunity Sizing & Decision Support | Measurement-heavy | 1295 |
| 4 | Ranking explanations for an inflated genome-wide signal | Root-Cause | Investigation-heavy | 1320 |
| 5 | Bridging a trend across a staggered change of instrument | Comparative & Explanation | Attribution-heavy | 1348 |
| 6 | An alert rule for 60 wastewater sites with a fixed false-alarm budget | Data Quality, Monitoring & Alerting | Design of the rule itself | 1373 |
| 7 | An allocation by expected burden from suppressed, small and lagged counts | Opportunity Sizing & Decision Support | Allocation under constraints, driven by a quantity no table reports: next year's expected deaths in counties where this year's are suppressed, noisy or not yet in | 1398 |
| 8 | A blood pressure distribution across two devices and a complex sample design | Descriptive & Distribution | Measurement and design | 1423 |
| 9 | Conforming two decades of spontaneous reports into one case-level table | Data Extraction & Conformation | Assembly-heavy | 1458 |
| 10 | A survival effect when control patients switched to the new drug | Experiment & Causal | Synthesis-heavy | 1490 |
| 11 | Finding what drove a drug spending overrun across thousands of products | Root-Cause | Triage-heavy | 1518 |
| 12 | Choosing facilities for inspection from noisy, risk-adjusted outcome ratios | Anomaly Detection & Diagnostics | Estimation of a hard-to-measure quantity: each facility's true, persistent performance, which chance and drift hide in every year's ratio | 1547 |

**Economics and Quantitative Social Science**

| # | Strategy | Analysis type | Weight | Line |
|---|---|---|---|---|
| 1 | A forecast built on the numbers you will actually have | Forecasting & Predictive Modeling | Validation | 1652 |
| 2 | A revenue shortfall bridged to its causes | Root-Cause Analysis | Attribution | 1683 |
| 3 | A regional panel built from withheld cells and moving industry codes | Data Extraction & Conformation (ETL / Pipeline Build) | Assembly | 1708 |
| 4 | Why participation moved differently across 51 states | Comparative & Explanation | Measurement | 1739 |
| 5 | An alert rule for voter roll removals | Data Quality, Monitoring & Alerting | Rule design | 1767 |
| 6 | A mail plan when the message spreads through the household | Experiment & Causal Analysis | Allocation under a budget | 1797 |
| 7 | Spell lengths from a panel with seams and edges | Descriptive & Distribution Analysis | Estimating a quantity no file records | 1825 |
| 8 | Sizing a multi-site study when sites genuinely differ | Opportunity Sizing & Decision Support | Modeling | 1861 |
| 9 | Finding the cause of every break in agency crime counts | Anomaly Detection & Diagnostics | Investigation | 1895 |
| 10 | Returns to prison when one way back is closed | Forecasting & Predictive Modeling | Synthesis | 1925 |

**Engineering and Physical Sciences**

| # | Strategy | Analysis type | Weight | Line |
|---|---|---|---|---|
| 1 | Debugging a low-cost air sensor network | Data Quality, Monitoring & Alerting | Design of a monitoring rule | 2026 |
| 2 | Finding the breaks in a station network before trusting its trend | Anomaly Detection & Diagnostics | Triage at breadth | 2055 |
| 3 | A design flood from a short record, several neighbors and a reservoir upstream | Forecasting & Predictive Modeling | Estimation of a hard-to-measure quantity | 2084 |
| 4 | Bridging expected to actual energy at a wind farm | Root-Cause Analysis | Attribution | 2117 |
| 5 | Diagnosing underperformance across a solar fleet | Anomaly Detection & Diagnostics | Investigation | 2146 |
| 6 | A ten-year peak load forecast whose bands hold up | Forecasting & Predictive Modeling | Validation | 2175 |
| 7 | One emissions table from agencies that count different things | Data Extraction & Conformation (ETL / Pipeline Build) | Assembly | 2205 |
| 8 | Grading plant efficiency after accounting for how each plant was run | Comparative & Explanation | Modeling | 2234 |
| 9 | Sizing a battery when the month's peak is not known in advance | Opportunity Sizing & Decision Support | Optimization under constraints and uncertainty | 2263 |
| 10 | Injury risk per hour worked across a shift | Descriptive & Distribution Analysis | Measurement | 2296 |
| 11 | The safety effect of a signal display change at sites picked after bad years | Experiment & Causal Analysis | Synthesis | 2325 |

**Other**

| # | Strategy | Analysis type | Weight | Line |
|---|---|---|---|---|
| 1 | A state scorecard from overlapping survey years | Comparative & Explanation | Measurement | 2435 |
| 2 | Interviewers whose fieldwork needs re-checking | Anomaly Detection & Diagnostics | Triage at breadth | 2466 |
| 3 | Splitting a fixed fund from small-area estimates | Opportunity Sizing & Decision Support | Estimation of a hard-to-measure quantity, then allocation under constraints | 2498 |
| 4 | An alert rule for a seasonal claims series | Data Quality, Monitoring & Alerting | Designing the rule itself, then proving it out of sample | 2523 |
| 5 | Neighborhood data conformed across boundary changes | Data Extraction & Conformation (ETL / Pipeline Build) | Assembly | 2557 |
| 6 | Why city service got slower, from the request log | Root-Cause Analysis | Investigation | 2582 |
| 7 | A ridership forecast after a regime break | Forecasting & Predictive Modeling | Validation | 2613 |
| 8 | Net effect of enforcement cameras with nearby spillover | Experiment & Causal Analysis | Modeling | 2644 |
| 9 | Achievement gaps recovered from proficiency bands | Descriptive & Distribution Analysis | Estimating a quantity the files never publish | 2678 |
| 10 | An early-warning cutoff set to advisor capacity | Forecasting & Predictive Modeling | Framing and calibration | 2703 |
| 11 | Splitting a score drop among its explanations | Root-Cause Analysis | Attribution and synthesis | 2734 |

## Generated data under the atlas

The atlas points at public data for each strategy, and public data used as is remains welcome. Generated data is the
house route and is fine when it behaves like the real thing throughout (the author's ruling, 2026-11-09): the
generator simulates the process the entry describes (the funnel's sessions and users, the fleet's sensors and work
orders, the cohort's maturity), so the files carry the same patterns, noise and problems the entry says the public
data carry, across every unit, and no effect is placed only where it decides a result. The export's own line for
assembled or extended data: "it has to behave like the real thing throughout, with many genuine patterns and noise,
never one effect added for the solver to find."

## The client's deep judgments, as results

Each judgment below is now one result in a chain, never the whole task: the client calls a task priced by one
legitimate method step "thinner" and asks for the results around it. The Mark record still says which forms the runs
execute by reflex; a judgment in its dead form scores Right in the careful column (`../SKILL.md` Part 3).

| Judgment (client) | Mark's record | Label | The live form |
|---|---|---|---|
| **A comparison that is actually clean** | F9 causal design: no measured hold; died 107 v2 (a filed effect formula), 118 and 124 (the contamination readable), 230 twice (stratification a reflex), 193 v1 and v2 (the comparison population and its value filed in the estimand: no third position). Shipped 131 (a household's cards share baskets). Client: Examples 2 (0.46), 4 (0.24), 6 (0.57), 8 (0.40), 13 (0.44) accepted | WORKS IN FORM | The contamination is visible only through a relation in the data (the same app build carrying a push outage; areas started worst-first; leader-follower price pairs; waiting states that received the freed staff time; cities diverging before the rule), never a column, a schema or a filed sentence; the comparison is never filed in the estimand; and after the clean comparison is chosen the chain carries further results (weighting to the decision's mix, the effect's uncertainty, the decision quantity) |
| **Heterogeneity that pooling hides** | F5 composition held (68, 83; pattern E approved on 30). Grouping as the step is dead (1.1c: per-class against pooled shows in the fit, likelihood ratio 511.1 on 668 df, and a blind reader fitted per class unasked). Client: Examples 1 (0.26), 5 (0.45), 6, 7 (0.55) | WORKS IN FORM | The groups respond differently AND the decision weights them to a population whose mix differs from the sample (next year's traffic, the system that will adopt, the treated population), with the group property rebuilt from a history (a per-customer use count), never read off a column. Dead form: the result's whole move is "estimate it by segment instead of pooled" |
| **Uncertainty that matches the design** | G17 statistical rigor: supporting only; 6 of 12 textbook routes landed in-house, clustered errors a house reflex (`evidence.md` 1.1j); a filed confidence level is a filed method once only a variance remains (readability test 1). Client: Example 14 (0.59, "closer to a single-insight task"), Example 12 | DOES NOT WORK as a result's only difficulty | Only as one result in a longer chain whose other results need their own judgments (the estimate the interval wraps needed its own judgment first). "Cluster by school" alone is a one-fact stump |
| **Variance beyond sampling noise** | A level at a selected unit is a shrinkage target and shrinkage is the opponent's reflex (James-Stein 40 of 40); a shrinkage choice moves about 8 per cent at most (G16). Approved 253 (a floor count is a sum of probabilities, not shrunken predictions). Client: Example 15 (0.50) | WORKS IN FORM | Standard shrinkage is the hurried route and the result's hard move is the variance component the standard model omits (a cohort-to-cohort term, a year-to-year persistence term), or a decision quantity that is a sum of probabilities. Dead form: shrinkage itself as the golden |
| **Separating two explanations for one pattern** | F8 attribution: held after repair 72, shipped 182 (each bore's own driver-only path fitted before the effect); died 36 (an argmax under a stated rule), 119 and 122 (a filed sentence), 228 twice (a reflex). A dated cause whose effect steps the series dies to an event study (36). Client: Examples 1, 3 (0.45) | WORKS IN FORM | Only a like-for-like comparison rebuilt from history separates the two (composition against behavior at a fixed use count; demand that drives spend); no explanation arrives as a dated cutover whose step an event study finds, and no filed sentence names the split |
| **Outcomes that have not finished happening** | F4 maturity: portal held 181 (each route's own reporting delay; the pooled-delay nowcast picks the wrong area). Died 134 loop 0 (Kaplan-Meier censored at the cut was the golden), 190 ("nowcast or count" settled by the WHAT). Client: Example 1 (open returns projected), Example 10 (0.43) | WORKS IN FORM | Completion speed differs by a unit no pooled factor captures (a route, a lab whose delay changed, a vintage, a channel), so the pooled or textbook completion factor files a named wrong answer. Dead form: the field's standard censoring or development method (Kaplan-Meier, one pooled chain ladder) is itself the golden |
| **A forecast that has to earn its place** | F6 method selection: held 46 (a rate law stationary in cumulative service exposure rebuilt from a movement log), approved 33, shipped 446 v2; died 38 (an enumerable model class behind a shipped back-test is an answer key, eleven rounds), 89 v5 and v6, 130 v3 (the analog default), 125. Law L6: pin by identity or exhaustion, never by fit. Client: Example 5 (0.45) | WORKS IN FORM | The invariant the right model rests on is constructed from a log, the back-test the solver runs is its own, and no shipped test enumerates the winner; the forecast must beat the naive baseline out of sample and the committed level carry its uncertainty |

## Mark's families, as results

These join the union. A Mark driver that was approved is now in the client's hands and possibly in training data, so
the family is reusable and the driver never is (`guard.py heart` blocks it).

| Mark family | Record | Label | The live form under Sulfur |
|---|---|---|---|
| F1 Time: a clock the closed window never exercised | Portal held 102 and 107 v4, both validated decoys, now blocked; legal form shipped 134 v2 (a conversion hazard by time since entry) | WORKS IN FORM | A clock process estimated from every unit that went through it; never a validated decoy, never a dated cutover |
| F2 Grain: what one unit of the decided thing is | Portal held 103 v3 (the call held, the asks gave way); died 44 (an order id bridged the grains), 48, 67, 103 v1 and v2 | WORKS IN FORM | The unit constituted from a history, a place or a household, with no key bridging the grains; pair it with a statistical judgment, since the client requires one in the chain |
| F3 Binding constraint: a shared limit | Portal held 106 run 3; died on an argmax over a filed capacity vector (87) | WORKS IN FORM, as a supporting result only | Sulfur bans "if the top option breaks the cap, take the next" as rule application, and a constraint is not a statistical judgment, so it is one result in a chain whose priced results are estimates |
| F7 Population: who is in the denominator | Approved 25, 28; shipped 229, 132 (a replacement restarts the wear curve); died 100 v1 (a clause handed it over), 269 v4 (a population the estimand must name cannot be the step) | WORKS | The selection mechanism (on outcome, schedule, symptom, survival, replacement) built from histories, never a status word or clause |
| F10 Identity resolution | No hold; died 120, 121 twice, 81 v3, 90 | DOES NOT WORK as a result's only difficulty | Layer 1 or a supporting result; the client's shape 15 allows it only upstream of an estimate whose uncertainty depends on match quality |
| F11 Stated rule, hard construction | No hold; died 133 v1 (a portal model at 100), 107 v3, 67, 37 | DOES NOT WORK | Rule application, banned by Sulfur |
| F12 Uncertainty and hold | Never drawn | UNTESTED | A hold is legal only when reaching it takes work (`../SKILL.md` Part 3, G17); several client examples offer HOLD as an answer |
| F13 The withheld rule | Retired; the official-decoy form blocked | DOES NOT WORK | A planted rule, banned by Sulfur |
| The validated decoy | 27 of 30 builds from 99 to 130; blocked | DOES NOT WORK | Banned (a decoy) |

## Never build these (Mark's measured deaths, every one still binding)

From `strategies.md` Part 6 and `../SKILL.md` Part 9, in one place. Each is a form the models solved or a gate killed; as a result in a chain it is earned by the runs, and as the whole task it is the one thing the client returns.

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

## Measured in Sulfur (the run record to 2026-11-11)

Two `sulfur-record.md` rows move a label; the forms below were landed by both runs in two rounds or more, so each is a
reflex in the careful column whatever its label above (`precedents.json` R01 to R20 carry the runs' own words):

| Form | Sulfur rows | Now |
|---|---|---|
| A forecast form chosen by a hold-out the run builds itself (two calibrations by leave-one-out, a family by a chronological winter, a breakpoint on held-out configurations) | task16 arch 1, task10 arch 6, task4 arch 9 | DOES NOT WORK as a result's difficulty; it lives only where the record's hold-out cannot see the condition the forecast window has (`validation_cannot_see_condition`) |
| A mechanism one plot or one group-by of one file shows | task2 arch 3, task3 arch 2 and 3, task5 arch 2, task7 arch 4 round 2, task8 arch 17 | DOES NOT WORK |
| A capped availability ceiling, the rebound after a window, a predictive tail, commissioning by competing risks | task10 arch 6, task10 arch 7 | DOES NOT WORK (R05 to R07) |
| A trial's effect carried to the target along a modifier one join or one second file away | task7 arch 7, task16 arch 2 (the judge's first pass) | DOES NOT WORK alone; `transport_effect_modifiers` is on five of our live builds and one accepted client task (`skeleton.py check` warns on it) |
| One more correction inside a scaffold the runs already landed | task4 arch 6 to 10, task10 arch 4 to 7 | DOES NOT WORK; the skeleton guard blocks it on the slot's lineage |

**Live, from the client's level 4 and 5 tasks** (where frontier runs lost; `../SKILL.md` Part 1b): the split carried
to the decision (L09 to L12), the assumption a run names and waves through made false (N01 to N07, L06, L07), units
selected by the outcome's own history (L13, L14), a measured response and the marginal unit (L15, L17), the system's
net against the unit's own (L16), a shallow path that passes its own checks (L26 to L31). Each is a kind of
judgment: the client's tasks themselves are in `../../fingerprint/corpus/client_skeletons.json` and may not be
reskinned. The first Sulfur build on each moves its label with its rows.

## Keeping this file current

The index is regenerated from the export whenever the client re-exports it. A Sulfur run or review that lands a
judgment in a given form moves its label down one step with the `sulfur-record.md` row cited; two rows move a label,
one row is noted beside it. The move is a `SKILLS:` commit.
