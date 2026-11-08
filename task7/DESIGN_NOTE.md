# task7 design note (architecture 5)

Architectures 1 to 4 left only the Tried and rejected record at the end of this note; their files were removed at the
author's word on 2026-11-08.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task7.json`, architecture v5, lineage v1 to v4 (v4 moved in with its fate
  and shell), registered 2026-11-08 at WARN only and re-checked on the registered card as the last act of stage 1. A
  first draft with the gap `population` first BLOCKed `test.same_puzzle` against task3's lineage v1 (population, G14,
  quantity figure); the decisive gap is `objective`, the honester reading, because the property register's rolled-forward
  value is a correct market figure and the loss is scored on what the property fetches when its borrower fails.
- **WARNs answered:** `overuse.strategy` (population_selection in three of twelve): the security behind the loans that
  fail is selected by the failure, which is this build's mechanism, and the other carriers select by busy-hour sampling
  (task6) and by examination on signs (mark124), not by the outcome being priced. `overuse.forum` (executive_team): an
  Irish bank's plan lines are set by its executive committee, and the shell carries the forum only as the deck's
  audience. `overuse.objective` (forecasting six in twelve): banking x forecasting has never been built and is the
  client's most welcome objective. `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, against task2 v4):
  the stump is carried by what the loss model's input means at its fit against at its use, a modelling judgment; task2's
  is a change of support in a resource model.
- **Pairing:** Banking, Credit & Financial Risk, task type `expected-credit-loss-provisioning`, which serves
  forecasting: the expected credit loss of the loans on the book at 31 December 2026 over 2027.
- **Shape:** 07, a grid of cells: the 2027 plan figure, its two lending-book cells and the five facilities expected
  to cost most, with the facility-level file (2,260 rows) behind them; every cell moves with the deep step (the default
  path files nil, €0.25 million and nil on the three figures and one of the five).
- **Strategy:** `population_selection` (failure selects the security that falls behind its market), Gate G
  `method_or_model_selection`, generators G14 (the security's yield conditioned on the failure), G6 (the book is staler
  than the record's failures were) and G3 (the register's carried value against what a sale realises).
- **Strategy label (`sulfur-strategies.md`):** WORKS IN FORM, heterogeneity that pooling hides: the shortfall differs by
  the years since the last inspection, and the decision weights it to a book far staler than the record's defaults, the
  staleness rebuilt from the valuation history and never read off a column.
- **Data-native sentence:** Ardcarn stopped inspecting its performing commercial property security after its 2012 to 2019
  cycle and has carried it since as quarterly index roll-forwards, while its loss model was fitted on the inspection it
  orders when a borrower defaults; a property that falls behind its market is the kind whose borrower defaults, so the
  roll-forward overstates the security of exactly the loans that will make the losses, by more the longer since the
  last inspection, and since 2022 the workout unit has re-inspected large facilities months before they default, so
  the record's recent defaults rest on fresh inspections while the year-end book does not.
- **Abstraction sentence:** a recovery input that the record measures fresh at failure is carried forward from an old
  measurement for the units being priced, and the failing units' input has drifted adversely from the carry-forward by
  more the older the measurement. Written against the nearest approved and in-flight builds, it is none of theirs:
  mark179 prices an excess hazard after an outside event, mark132 a clock a replacement restarts, mark124 a rate
  measured on units examined for signs of the outcome, task2 a change of support, task8 arch 18 two features cancelling.
- **World:** Ardcarn Bank plc, a fictional licensed lender headquartered in Galway, lending to small and medium
  businesses on commercial property across the Republic (let retail, offices and industrial units; owner-occupied
  hotels, pubs and restaurants, nursing homes and shops). People drawn with `guard.py names --geo Ireland --seed 7`:
  Colm Hourican (chief financial officer, who sets the 2027 plan's credit-loss line) and Geraldine Harkins (chief risk
  officer). Currency EUR.
- **Sources (all constructed for this task, seeded and deterministic; nothing real is described):** the month-end
  facility fact of the warehouse (facility x month, January 2022 to December 2026, 133,156 rows, the large messy CSV);
  the property valuation history, a type 2 dimension whose quarterly index roll-forward rows sit beside the inspections
  (121,249 rows, the long CSV); the property dimension with inferred members; the facility register with the 2021 core
  banking re-keying and its crosswalk; the security bridge sharing properties between facilities; the default register
  (2012 to 2026); the receivers' sales and the recovery postings; the commercial property index by sector and region
  with its release vintages; the credit policy's master scale and ECL standard and the loss given default model
  documentation (PDF); the chief financial officer's 2027 plan request; and distractors a planner would weigh (the 2027
  property market outlook, the rent roll, the buildings insurance register, the September 2026 concentration report).

## Default path

The field's own method for the deciding quantity, executed as the files state it:

1. plan_2027_credit_loss_request.pdf and the policy fix the line: each facility performing at 31 December 2026 takes
   the master-scale chance of default for its year-end grade, its year-end balance, and CRE-LGD-3.
2. The 20261231 rows of the month-end fact with default flag N give 2,260 facilities and €1.84 billion; the bridge rows
   in force at the year end give the security, a shared property split by exposure (policy 4.4).
3. The valuation history is cleaned (exact repeats, same-day corrections, legacy FULL and IDX codes) and the row in
   force on 31 December 2026 gives each property's value: the register's carried value.
4. CRE-LGD-3, max(0, EAD - 0.78 x V) / EAD, on that value; the model documentation's back-test passes in every year,
   so the route validates.
5. PD x LGD x EAD summed over the book.

- **Ends on:** €0.2 million (€221,294), which rounds to nil at the nearest €500,000.
- **Golden:** €2.0 million (€2,022,102).

## Stump sentence

The default path files €0.2 million (nil at the nearest €500,000) because it feeds CRE-LGD-3 the register's carried
values, index roll-forwards of inspections up to twenty years old, while the model's V is the inspection the bank orders
at default and the bank's own defaults came in below the carried value by more the longer since the inspection behind
it; the year-end book is far staler than the record, so neither the record's average shortfall (€1.2 million, so
€1.0 million) nor its latest years (€0.8 to €1.4 million) price it, and only the shortfall modelled on the years since
inspection and carried to each facility files €2.0 million.

## Deep reasoning

- **Task type:** expected-credit-loss-provisioning (Banking, Credit & Financial Risk), which serves forecasting: the 2027
  expected credit loss of the book performing at the year end.
- **Domain test:** the deciding quantity is the expected value of each facility's security at a 2027 default, the V of
  the bank's commercial property LGD model; the field's estimator is CRE-LGD-3 applied to the security value with the
  master-scale PD and the year-end exposure.
- **Swap:** "plan the 2027 readmission cost of the patients discharged at the year end, where the cost model was fitted
  on the cost assessed at readmission" stops making sense: there is no collateral carried between inspections by a
  market index, no inspection that a failure triggers, and no failure that selects the collateral which has fallen
  behind its market.
- **Layer 1:** the warehouse's own texture, each from the system that makes it: type 2 valuation rows with exact
  repeats and same-day corrections (the load process), legacy FULL and IDX basis codes before the 2021 conversion,
  facility numbers re-issued on 5 June 2021 with the register's crosswalk, inferred property members (properties loaded
  before their dimension row), a June 2024 month-end batch loaded twice and a February 2023 batch never loaded,
  second default triggers on the same facility, recovery postings into 2027, index release vintages; none sits on a
  graded path (SF3, SF15, SF16, SF14).
- **Layer 2:** heterogeneity that pooling hides (population selection): the shortfall of the security at default
  against the carried value grows with the years since the inspection the carried value rests on, and the decision
  weights that relation to a year-end book far staler than the record's defaults.
- **Decisive step:** model the bank's inspection at default as a share of the value carried on the default date as a
  function of the years since the inspection that value rests on, from the bank's own defaults, and price each
  performing facility's security at its own years since inspection and lending book.
- **Not semantics:** every field read right (V is the inspection at default, the register's value is an index
  roll-forward, FULL and IDX are the old codes, the book is on the facility) still leaves the default path on the
  carried values, which are the register's correct market figures for a performing property and not what a failing
  borrower's property is inspected at.
- **Not rule application:** no filed rule says how to estimate V before a default happens: the memo asks for "the
  expected value of the security at that date", the model defines V as the inspection at default, and nothing says the
  carried value is biased or what the bias depends on. The enumerated family spreads from €0.22 million (carried) to
  €4.18 million (a blanket 25 per cent haircut) over seven plan cells; the standing family (log, normal, linear,
  banded and median fits, split or pooled, index-adjusted, exposure-weighted, three sub-periods, three other forms,
  sale proceeds, the fork readings) spreads €1.92 to €2.12 million, all €2.0 million; the ruling-out is loud: the
  slope on staleness is 23 standard errors from nought, and the record's average, its latest years and the cycle's
  drift miss the plan cell by €375,000 or more.
- **Analyst test:** CRE-LGD-3 on the register's carried values with the master-scale PD and the year-end balance, the
  model's own validated route, files €0.2 million, nil at the nearest €500,000.
- **Estimand:** plan_2027_credit_loss_request.pdf: the expected credit loss on the commercial property facilities
  performing at 31 December 2026 that default during 2027, the master-scale PD for the year-end grade, the year-end
  balance, and CRE-LGD-3 applied to the value the bank would expect its inspection to put on the security if the
  facility defaulted, each default as if on 1 January 2027 and prices held at the latest published level; defaulted
  facilities and 2027 lending outside the line.
- **No decoy:** nothing is planted: the carried values are the register's correct roll-forwards, the back-test is the
  model's genuine validation, the referral inspections are the workout unit's ordinary practice, and no memo, draft or
  stakeholder figure argues for any plan figure.
- **No certified replay:** the method is not recovered by reproducing a published figure; no file prints the plan
  line, an ECL total or a shortfall ratio.
- **Chain:** (1) V in CRE-LGD-3 is the inspection the bank orders at default, while the year-end register carries
  index roll-forwards, so the input has to be predicted before any default happens; (2) the bank's defaults since
  2012, joined through the legacy facility numbers, the bridge on each default date and the cleaned type 2 history,
  give the inspection at default against the value carried then: 844 defaults averaging 87.1 per cent; (3) that ratio
  falls with the years since the inspection the carried value rests on, about 2.9 per cent a year, 23 standard errors
  from nought, while the cycle's inspections of performing properties fall by less (no failure selected them), so the
  shortfall is selection and ageing, not a constant; (4) the year-end book is staler than the record (26 per cent of
  exposure on inspections seven or more years old against 9 per cent of defaults, and 10 per cent of the defaults since
  2022, which the workout unit re-inspected months before default), so the relation, not any average, prices it;
  (5) each facility's expected value at its own years and lending book through CRE-LGD-3 and the master scale gives
  €2.0 million, €1.25 million on investment lending and €0.75 million on owner-occupied.
- **Judgment:** the statistical judgment is that the shortfall is a function of staleness to be estimated on a selected
  record and transferred to a population with another staleness mix: a regression of the log ratio on the years since
  inspection with a retransformation to the mean, justified by the slope's precision, by the cycle inspections that
  show the unselected drift, and by the referral defaults that sit at the fresh end of the same line.
- **Hidden by:** the register's current row reads as fresh (a valuation date at the last quarter end, basis index
  roll-forward), the model's back-test passes in every year because it feeds the inspection at default, and the record's
  latest years are no worse than its earlier ones because the large recent defaults were re-inspected at referral.
- **After the notice:** once the solver sees inspections at default coming in below the carried values, it still owes
  (1) that the shortfall is not a constant: the record's average applied flat files €1.2 million, so €1.0 million;
  (2) that the latest years are not the book: their average applied flat files €0.8 to €1.4 million, because a third
  of them rest on inspections made months before default; (3) the book's staleness rebuilt per property from the type 2
  history past the roll-forward rows; (4) that owner-occupied security falls further at the same staleness: pooling
  lands the plan figure but files €1.5 million and €0.5 million on the split.
- **One-fact test:** the likeliest rescuing sentence, "the carried values are roll-forwards of old inspections", is
  already policy 4.5's own description of a roll-forward and still leaves the record to be built across three re-keyed
  files, the shortfall to be modelled on staleness, the referral inspections to be read as freshness rather than better
  recoveries, and the relation to be transferred per facility; a sentence naming the relation would be the method.
- **No replay:** the call re-derives no published figure and no stated number is wrong; the concentration report and
  the outlook are exposures and market views.
- **Pinned:** every rival run on the cut pack, asserted in checks.py: log, normal, linear, banded and median fits split
  by book (€1.92 to €2.10 million, all three cells), pooled (€1.93 to €2.11 million, the plan cell, other split cells),
  exposure-weighted (€2.05 million), defaults 2012 to 2019, 2017 to 2026 and 2020 to 2026 (€2.00 to €2.04 million), quadratic,
  square-root and log-of-one-plus forms (€2.05 to €2.07 million), one slope with a level per book (€2.03 million), the
  receivers' net proceeds against the carried value with no haircut (€2.12 million), and the fork readings SF6, SF8,
  SF10, SF17 to SF22, every one on the golden's three cells and five facilities.
- **Run forecast:** a run that applies CRE-LGD-3 to the carried values is a method shortcut at rung 0 (nil); a run that
  builds the record and applies its average or its latest years' is an unfinished chain at rung 2 (€1.0 to €1.5
  million); a run that fits the staleness relation but pools the books lands the plan figure and is dismissed own
  evidence on the owner-occupied gap (€1.5 million and €0.5 million).
- **Strategy label:** WORKS IN FORM, heterogeneity that pooling hides, in its live form: the shortfall by staleness
  weighted to the population the decision serves (a book staler than the record), the staleness rebuilt from the type 2
  history and never read off a column.
- **Lesson:** a loss model's input measured fresh at failure cannot be fed a carried-forward value, and a selected
  record's average transfers only through the variable that selects it; no build on file teaches this (mark179 prices
  a post-event hazard, mark124 a rate measured on examined units, task2 a change of support).

## Survivor anatomy

- **Actor:** the years since the inspection behind a carried value has no column: the register's rows carry a valuation
  date (the quarter end for a roll-forward) and a basis, and the age of the inspection is a relation between rows of
  the type 2 history, read past every roll-forward row.
- **Link:** the record joins the default register to the valuation history through re-keyed facility numbers (the
  register's crosswalk) and the bridge as at each default date, a join no key offers, and compares the inspection at
  default with the value carried before it, a comparison CRE-LGD-3 never asks for (it takes V at default as given).
- **Reflex:** the field's method, CRE-LGD-3 on the register's security values with the master scale and the year-end
  balance, files €0.2 million, nil at the nearest €500,000 (the default path).
- **Back-test:** the model documentation's back-test passes in every default year because it feeds the inspection at
  default; the easy route validates.
- **Second use:** every file the step reads is in the pack for the plan anyway: the valuation history (the carried
  values), the default register and facility register (the record and the books), the bridge (the security), the
  index (the roll-forwards), the model documentation; delete the step and none drops out.
- **Shock:** the recovered movement reads as ordinary: the five facilities expected to cost most rank 1, 10, 101, 130
  and 511 on exposure, 1, 6, 12, 25 and 27 on PD times exposure, 3, 453, 731, 792 and 799 on the carried-value loss and
  433 to 854 on staleness; the answer set is an interval of no shipped statistic.
- **Pins:** the WHAT sits in the chief financial officer's memo and policy 4.1 to 4.4 (population, PD, exposure, the
  LGD model, the date, prices held); no filed sentence names staleness, the record, a regression, the referral practice
  or a split of the shortfall by book.

## Readability screen

| Rung | What the rows in view show | Verdict |
|---|---|---|
| 0 the model on the carried values | the register's row in force per property, CRE-LGD-3, the master scale | readable |
| 1 a reflex haircut (blanket, or 10 per cent past three years) | the model's 22 per cent, any haircut a reviewer adds | readable |
| 2 the record's shortfall applied flat (all years or the latest) | inspections at default against carried values, averaged | readable |
| 3 the shortfall by years since inspection, carried to each facility (decisive) | no column: the years rebuilt per property past the roll-forward rows, the record joined through re-keyed numbers and the bridge as at each default | silent |
| 4 the lending books apart (ask) | no column: owner-occupied security below investment at the same years, read only in the fitted record | silent |

Test 8 (framing): neither the prompt nor any governing document states that the year-end book is staler than the
record, that recent defaults were re-inspected at referral, that the shortfall depends on anything, or that the books
differ; the memo frames the line on its own terms (performing at the year end, defaulting in 2027).

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "credit loss" for 2027 | expected credit loss on 2027 defaults of the year-end performing book | 2027 write-offs on facilities already in default | another line | memo: "expected credit loss on the commercial property facilities that are performing at 31 December 2026 and default during 2027" (SF1) |
| SF2 | the population | default flag N at 20261231, 2,260 facilities | with the year-end defaulted facilities | another figure | memo: "already in default at 31 December 2026 are provided for separately and are not in this line" (SF2) |
| SF3 | the year-end snapshot | one 20261231 row per facility | the June 2024 batch loaded twice | same call | the reload reaches no year-end row (SF3) |
| SF4 | chance of default | the master scale at the year-end grade | a rate recalibrated on the record | another figure | memo and policy 4.1 (SF4) |
| SF5 | exposure | the 31 December 2026 balance | a balance amortised to a 2027 default, or the limit | another figure | memo: "its exposure is its balance at that date" (SF5) |
| SF6 | "expected value" of the security | the mean (Duan retransformation) | the median of the fitted ratio | €2.10 million, the same cells | same call (SF6) |
| SF7 | when the default falls | as if on 1 January 2027 | spread through 2027 (half a year staler) | €2.26 million, so €2.5 million | memo: "as if it fell on 1 January 2027" (SF7) |
| SF8 | prices | held at the latest published level | the outlook's 2027 capital growth applied | €2.00 million, the same cells | same call (SF8) |
| SF9 | a shared property | split in proportion to exposure | the whole property to each facility | another figure | policy 4.4 (SF9) |
| SF10 | the carried value | the register's row in force on 31 December 2026 | the last inspection re-rolled on the latest release | €2.02 million, the same cells | same call (SF10) |
| SF11 | lending book | the facility's own (fact and register agree) | the property's type | same call | they agree on all 2,260 (SF11) |
| SF12 | "cost the bank the most" | expected 2027 loss | exposure, or LGD | another list | the ask's words (SF12) |
| SF13 | a loan | a facility | a customer | same five | five customers (SF13) |
| SF14 | inferred property members | the book read from the facility | the facility dropped for a missing type | same call | 41 facilities keep their book (SF14) |
| SF15 | repeats and same-day rows | dropped | kept | same call | none sits in force after cleaning (SF15) |
| SF16 | FULL and IDX | inspection and index roll-forward | other bases | another record | policy 4.6 (SF16) |
| SF17 | the inspection at default | within 92 days after the default | within 60 or 180 days | €2.03 and €2.02 million, the same cells | same call (SF17) |
| SF18 | the record's carried value | in force on the default date | in force the day before the inspection | €2.05 million, the same cells | same call (SF18) |
| SF19 | years since inspection, to | 1 January 2027 | 31 December 2026 | the same cells | same call (SF19) |
| SF20 | a default's years since inspection | from the inspection its carried value rests on | from the last inspection dated before the default | €2.03 million, the same cells | same call (SF20) |
| SF21 | the market's move in a ratio | the ratio against the value carried on the default date | index-adjusted to the inspection's quarter | €2.09 million, the same cells | same call (SF21) |
| SF22 | which inspection is at default | the one ordered on or after the default | the nearest either side | €2.02 million, the same cells | same call (SF22) |
| SF23 | the loss on the security | CRE-LGD-3 applied to the expected value of the inspection at default | the loss averaged over the spread of values an inspection might return | €2.48 million, so €2.5 million | memo: "CRE-LGD-3 applied to the value we would expect our inspection to put on the security if the facility defaulted" (SF23) |

## Ladder

| Rung | Route | 2027 line | Plan figure | Investment / owner-occupied |
|---|---|---|---|---|
| 0 | CRE-LGD-3 on the carried values (default path) | €221,294 | nil | €0.25m / nil |
| 1a | 10 per cent off values inspected over three years ago | €571,909 | €0.5m | €0.5m / €0.25m |
| 1b | blanket haircut of 10, 15, 20 or 25 per cent | €0.82m to €4.18m | €1.0, 1.5, 2.5, 4.0m | |
| 2a | the record's average shortfall (87.1 per cent) flat | €1,210,923 | €1.0m | €0.75m / €0.25m |
| 2b | the cycle's inspections of performing properties by years | €1,241,140 | €1.0m | €1.0m / €0.25m |
| 2c | the latest years' shortfall flat (66 windows and variants) | €0.80m to €1.37m | €1.0m to €1.5m | |
| 3 (decisive) | the shortfall by years since inspection, pooled | €2,023,524 | €2.0m | €1.5m / €0.5m |
| 3 + ask | by lending book (golden) | €2,022,102 | €2.0m | €1.25m / €0.75m |
| family | every standing rival (Pinned) | €1.92m to €2.12m | €2.0m | €1.25m / €0.75m |
| ruled out | defaults spread through 2027 (SF7) | €2,257,522 | €2.5m | |

The record's routes sit €375,000 or more outside the plan cell (asserted), the nearest blanket haircut (15 per cent)
€181,000; the family's nearest edge is €127,000 inside
it (€2.12 million against €2.25 million), the books' €48,000 and €50,000 inside theirs. The five facilities are the same
under every split member: AB322222580 (€110,067), AB316705961 (€57,448), AB321158994 (€37,941), AB325355079 (€36,941),
AB322344238 (€32,225); the sixth is €29,207. Pricing: the residue the filed WHAT leaves is the estimator of V, a method;
the move is €1.8 million on a call the record's average misses by €0.8 million; one standard error on the slope
(0.00125 on 0.0292) moves the plan figure by about €100,000, so the cell holds the golden 2.3 standard errors either
way.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | facilities performing at 31 December 2026 that default in 2027 | filed: memo (SF2) |
| 2 Unit of account | the facility; euro | filed: prompt and memo (SF13) |
| 3 Attribution window | 2027 defaults; the record 2012 to 2026 | filed: memo; C1 over record windows (SF17) |
| 4 As-of dating | the 31 December 2026 snapshot, defaults as if on 1 January 2027 | filed: memo (SF7, SF19) |
| 5 Version basis | the register's row in force against a re-roll on the latest release | C1 (SF10) |
| 6 Denominator | the value carried on the default date | C1 (SF18, SF21) |
| 7 Weighting | each default once in the fit | C1: exposure-weighted the same cells |
| 8 Window length | every default since 2012 | C1: 2012 to 2019, 2017 to 2026, 2020 to 2026 the same cells |
| 9 Boundary inclusivity | 92 days after default; seven years is descriptive only | C1 (SF17); nothing graded on an edge |
| 10 Rounding path | each figure rounded once from the unrounded sum | filed: prompt |
| 11 Tie-break | none: the fifth and sixth facilities €3,018 apart, every member the same five | C1 |
| 12 Maturity and censoring | 2027 defaults unobserved; the line is an expectation | filed: memo |
| 13 Order of operations | the expected value of the security, then the LGD | filed: memo ("the expected value of the security") |
| 14 Row order | no estimator depends on file order | C1: a property shared by two defaulted facilities defaults with both, one ratio |
| 15 Duplicate resolution | exact repeats and same-day rows dropped; the first default per facility | C1 (SF15) |
| 16 Identity normalisation | legacy facility numbers through the register's crosswalk | the bank's own crosswalk (policy 4.6) |
| 17 Netting against gross | none | not applicable: no quantity offsets another |
| 18 Dimensional units | euro throughout | units in the data |
| 19 Code and status semantics | FULL and IDX; INV and OWN; default flag Y and N | policy 4.6; the fact's own codes (SF11, SF16) |
| 20 Integerisation | each loan to the euro; the CSV total is its rows' sum | filed: prompt |
| 21 Clause scope | CRE-LGD-3 for every facility secured on commercial property | filed: model documentation 1, policy 4.4 |
| 22 Forward window contents | prices held, no 2027 lending, master-scale PD | filed: memo (SF8) |

## Literal reader

Executed word for word, the memo, policy 4.1 to 4.6 and the model documentation fix the population, the PD, the
exposure, the LGD formula and its V (the value the bank would expect its inspection to put on the security if the
facility defaulted, as of 1 January 2027 at the latest published prices), the date and the prices; the literal reader
that feeds the register's carried values to the model files nil, an easy method on the same literal estimand (the
carried value taken as the expected inspection), never another reading of it. Every term's alternatives are in the fork table and land on the golden's cells or are ruled out by a
quoted sentence; the estimator of V stays open and the data force it: the record rejects a constant shortfall (the
slope at 23 standard errors), the latest years' average (it misses by €375,000 or more), the cycle's unselected drift,
and pooling on the split (the owner-occupied level 4 points lower).

## Oracles

None ships. The model's back-test ties under every route because it uses the inspection at default (true and silent on
the carried value); the concentration report states exposures and limits, the outlook market views; no file totals,
ranks or splits a 2027 credit loss.

## Ask sheet

- **Ask A, the split by lending book (2 cells, rides the deep step and carries its own judgment):** owner-occupied
  security comes in 4 points lower at default at the same years since inspection, so the shortfall is fitted per book;
  golden €1.25 million and €0.75 million, pooled €1.5 million and €0.5 million, the default path €0.25 million and nil.
- **Ask B, the five facilities expected to cost most (5 names):** every split member names the same five; the pooled run
  keeps them, the default path keeps one, the record's average two.
- **Ask C, the facility-level CSV (2,260 rows):** its rows, columns and order by expected loss, its total equal to the
  plan figure before rounding, its first row AB322222580; the per-loan euros move a few per cent with the fit's
  conventions (the judge's rebuild), so no euro-exact cell is graded, and every owner-occupied row moves under pooling.
- **Pair ceiling:** 42.3 (landed run with the books pooled 69.0, default path 15.6; with the strongest off-call route,
  the latest years by book, 51.4; a landed run that also splits the books 57.8).
- **Shallow keep:** 15.6 per cent of the ask weight.
- **Measured by:** task7/generator/ceiling.py on the cut pack.

| Ask figure | Golden | Landed run (staleness, books pooled) | Shallow run (carried values) | Cracker verdict on the landed run |
|---|---|---|---|---|
| plan figure | €2.0 million | €2.0 million | nil | keeps |
| investment | €1.25 million | €1.5 million | €0.25 million | misses |
| owner-occupied | €0.75 million | €0.5 million | nil | misses |
| the five facilities | AB322222580, AB316705961, AB321158994, AB325355079, AB322344238 | the same five | one of five | keeps |
| CSV rows and columns | 2,260 rows, 10 columns | the same | the same | keeps |
| CSV first row | AB322222580 | AB322222580 | another facility | keeps |

## Prompt contract

A voice rewrite may not drop or change: the question (how much credit loss Ardcarn Bank's 2027 plan should carry for
the commercial property loans it held at the end of 2026); the population (the loans performing at the year end that go
into default during 2027); exco_cre_credit_loss_2027.pptx as the deck for the plan, giving the figure, its split between
investment lending and owner-occupied lending, and the five loans expected to cost the bank the most;
cre_expected_loss_2027_by_loan.csv with every one of those performing loans and its expected 2027 loss; the plan figure
to the nearest €500,000, the split to the nearest €250,000 and each loan's loss to the nearest euro. It may never add
inspections, valuations, staleness, the register, roll-forwards, the index, the record, past defaults, recoveries,
haircuts, the LGD model by name, the workout unit, the master scale by name, a count of loans, or any hint that the
books differ or that the carried values are out of date.

## Leak sweep rulings

`leak.py --asof 2027-01-15` returns REVIEW; each line ruled in the main thread:

- Sweep 2, "the model" in cre_lgd_model_documentation_2025.pdf: a model document's own subject; harmless.
- Sweep 3, golden-looking figures in the policy (0.75 and 1.25, the master scale's 0.75 and 1.25 per cent for grades
  3 and 4) and the model document (0.2, a back-test difference of -0.2 points): coincidences of a scale and a table
  with the graded euro figures; harmless.
- Sweep 4, the policy's inspection, roll-forward, record and register terms: policy 4.5 and 4.6 describe the register's
  fields and versions in the bank's voice and say nothing of staleness, selection or the record's shortfall; the memo's
  security, facility and latest-published wording files the WHAT; harmless.
- Sweep 8, internal_grade and default_flag in the month-end fact: ordinary warehouse names; harmless.
- Sweep 9, dates after 15 January 2027: maturity dates in the fact and register, lease ends in the rent roll, renewal
  dates in the insurance register; forward-dated fields, not events; harmless.

## Tried and rejected

- The note's decisive rung, per feeder the smaller of expected buyers and hosting slots: a stated connection standard, a per-feeder hosting map and a neighbourhood-to-feeder join whose keys line up hand it to any solver who reads them, its driver sits nearest task106's, and as labelled it BLOCKs on ban.pattern C (task119), ban.calibration pilot_log (task122) and test.same_driver_older (a signature spent in nine builds); kept as rung 2.
- Resistance-to-heat-pump netting (each resistance conversion frees feeder headroom for oil or propane conversions): the connection standard either states a per-heat-pump assessment, which contradicts the netting and is a counter-pin, or states a net-change rule, which hands it over; a corpus of past approvals would refute the stop rung, which L1 forbids.
- Heat pumps per home (large ducted homes taking two outdoor units, so two feeder draws per slot): visible at heat-pump grain in any connection or rebate record, and found by any solver who counts rebates per buyer; moves only the saturated feeders, too little to change a leader.
- Survey staleness (homes converted since fieldwork leave the pool): a dated register keyed on neighbourhood is a schema-visible pool deduction a careful solver makes unprompted.
- Competing claims on feeder headroom (the utility's deferred queue, committed loads, a state income-qualified programme): each needs a first-come-first-served clause the solver executes, and the effect sits only on saturated feeders.
- Seasonal against winter hosting capacity on summer-peaking feeders: needs a filed "winter" assessment that sends the solver straight to the feeder load history.
- A feeder map naming each neighbourhood's primary feeder while boundary streets sit on the next one: reads as a coarse instrument (sole_data_defect yes under the instrument repair), and a solver who reads "primary" looks for the street-level join.
- The expected minimum against the minimum of the expectation at feeders where buyers and slots balance: under 10 per cent on any feeder and inside the nearest ten on co-op totals.
- The year-end lapse on Year 1's lag alone (late autumn purchases missing 31 December): a stated deadline the solver replays at the finest grain on offer; kept as the check that passes at rung 2.
- A utility service-upgrade queue for old 100 A homes as the decisive rung: the upgrade requirement has to be stated for determinism, which sends the solver to upgrade lead times, and old homes sit mostly on saturated feeders, where the feeder cap already binds.
- Relabelling the note's pilot log as realised_outcome_roster to clear ban.calibration: a relabel that does not name the decisive move, so the organ itself was redrawn as Year 1's install book.
- A Nova Scotia setting with a fictional utility (oil and electric heat): the province's distribution is one large utility, so a co-op that sets its own heat-pump rate meters reads as invented; moved to Minnesota co-op territory.
- A field operations voice saying the 2025 meter-exchange backlog is behind us: true, but it names the backlog and sends a reader to the weeks the crews ran at their ceiling; dropped.
- A filed field-procedure line on the order of work (standing orders first, then orders in date order): read beside the programme's volume it gives a solver a reason to ask whether the crews keep up; the order is to be pinned by the 2025 record instead, and the line stays out unless the determinism check needs it.
- Keeping one co-op as the requester at registration, relabelled cooperative_or_member_body to clear ban.org_family: the key is honest for a member-owned co-op, but two United States power-company allocation builds would then sit side by side with task124, the calibration and artifact bans would still need redrawing, and the business-operations-analytics x opportunity-sizing-decision pairing would still block task128; the requester moved to the fund instead.
- The draw's per-co-op ask figures (meters still unset on 31 December, qualifying buyers the feeders turn away) and its chart parts (the stacked series, the year-end queue annotated): each names rung 3 or rung 4 in the prompt, which outranks every file, so a solver is told the queue and the feeder cap exist before opening anything; replaced by two device-carried pilot audits and a 2027-against-2026 chart.
- Spare capacity of about six sets a week at Lakes: the autumn queue bites harder, but each crew's annual spare (about 300) then falls below Lakes' 420 placeable meters, so a crude annual check hands Riverbend the lead without the queue; spare set back to about ten (annual about 500).
- Lakes and Uplands crews on a Monday-to-Friday week: the 2027 Friday holidays (Christmas observed 24 December, New Year observed 31 December) and Thanksgiving Friday open a holiday-handling fork worth up to a full ten on Lakes' slots; moved both crews to four ten-hour days, Monday to Thursday, with the 2026 record showing they worked the Thursdays before Friday holidays.
- Grading the year's rebated installs as the unrounded co-op sets rounded once to the nearest ten: the two binding co-ops' convention spreads (about 5 and 3.5 sets) add across a ten on the total; the graded total is the sum of the co-ops' slots, with the unallocated figure its complement.
- A spring queue left to run continuously into the autumn at the binding crews: year-end sets then depend on the spring start week and every holiday from Memorial Day on, a spread of more than ten; spring volumes sized so both crews clear by August.
- Pilot spring shares that differ by neighbourhood: per-co-op and pooled readings of the forward calendar then differ by 4.2 sets a point at Lakes; set to exactly 25 per cent in every pilot neighbourhood.
- A 2027 slot-release rule (a quarter of each co-op's slots in the spring window): it makes arrivals depend on the allocation itself and its fixed point (Lakes about 183) disagrees with the one-pass queue (about 240), a fork created by a filed sentence; no release rule, so both readings give 240.
- A per-co-op ask on the pilot's days from claim to payment: a staffing decision that the split never reads, so it fails H18; re-cut to the rebate dollars paid in 2026 and the installs they cover, the audit trail of the pilot the rates are built on.
- A pilot close-out stating the total rebates paid: an oracle that verifies ask B's handling for free; the pack states no paid, cost or cleared total.
- Field-order volumes at the draw's 70,000 rows: six crews' standing work over 104 weeks is about 31,000 orders at realistic crew sizes, and padding the file to 70,000 would need order types nothing reads; 31,000 clears the gate.
- Ask B's clock device on the 31 December 2026 evening payment run: the pack's as-of date is 11 December and the trustees meet on 17 December, so no December run exists to cross the year; the cutoff moved to the fund's November month end (the 30 November run clears on 1 December UTC) and the prompt asks for rebate dollars paid through the end of November.
- Anthony Bentley as the outreach director: the name is not in the seed-127 draw (`guard.py names --geo "United States, Minnesota" --seed 127 --n 200`); Anne Garcia from the draw then took BLOCK people.first against task125; Sara Duncan from the same draw is clear.
- The outreach director's belief that Uplands has more propane and electric homes than any other co-op: Table H1 puts Valley first on propane and electricity, so the belief would be a stakeholder read the pack refutes; reworded to more qualifying homes, which the survey's joint counts make true (rung 1's leader).
- The rung 3 twins with each neighbourhood's buyers split across two feeders: the map puts each neighbourhood on exactly one feeder, so Elm Park and Birch Hollow are identical on the survey and sit on a full and a roomy feeder respectively.
- A Lakes ceiling cycle averaging 10.45 a day over twenty days: the plateau's 50 days start mid-cycle and recover 10.57, which moves Lakes across a ten; the ceiling is a four-day 11, 10, 11, 10 pattern (42 a week) and standing work a twenty-day block averaging 8.05, so spare is 2.44 a day in any window.
- Pilot install rates with neighbourhood-level noise: rates by system and income band, or each co-op's own pilot rates, would each give a different forward figure (H14); every pilot neighbourhood is built from unit blocks (38 ducted-propane households to 3 installs, 32 electric to 1, 95 hydronic to 1), so every finer grain returns the system rates exactly.
- Pilot purchase dates spread evenly with a random installer lead time: autumn installs clustered to six orders a week at Uplands (0.86 of its spare); installs are spread evenly over each season's install span instead, peak four a week at Lakes and three at Uplands.
- The rebate amount as a pilot-log column: it would let a per-rebate reconciliation of the ledger find every returned payment for free; the amounts live in Schedule B of the participation terms instead (still a reconciliation route, recorded as HZ2's leakage).
- The rules file named `clean_heat_programme_rules_2027.pdf` after the fund: leak.py's file-name sweep reads `clean_` as the author's cleaned-data noun (LEAK); renamed `heat_pump_programme_rules_2027.pdf` in the generator.
- A "Decision sought" closing section and totals for expected installs, feeder room and meter sets in the note's line-by-line table: the section restated the split on an orphaned page, and a meter-set total of 1,174 beside 1,170 placed is a second statement of the year's installs by another rounding path (H3); both cut.
- 2026-10-10: the crew meter-set queue as decisive rung under a hosting-slot cap; the determinism judge returned SEND_BACK and the build was retired, not submitted.
- 2026-10-12, re-root (architecture 2): the author re-queued the number in wave 1 as "re-root, Opportunity Sizing". Candidates weighed at the draw and rejected: a charged-off card portfolio's sale against keeping it (the warehouse's payers are a visible attribute every solver conditions on, and the composition-mix strategy is banned against task501); a diabetic eye screening van placed by first-round against repeat-round yield (the prevalence-round effect is textbook to a strong solver); acoustic leak-detection crews placed by main material (material is a GIS column the reflex stratifies on, and a conditioned yield transferred across mixes is composition mix); a health plan's navigations split by procedure group where members follow their surgeon (the payment-claims task type serves ETL and Anomaly Detection, not Opportunity Sizing); an overdraft fee cap's revenue at risk sequenced after the banks' own changes (lending sits outside Economics in the client taxonomy, and no banking task type serving Opportunity Sizing fits a rule's revenue impact).
- 2026-10-12, architecture 2 at stage 2: a brokerage "package available from" date beside the start date (care ready before the patient left): it shows the care wait apart from the delay for every patient held by equipment, so a solver reconciling the two sees a third of Ashby Vale's patients leaving days after their care was ready and goes looking; the brokerage records care starting on the day the patient went home, and the restart patients carry the counterfactual instead.
- Restart patients needing discharge equipment at the same rate as new-package patients: subtracting their average nights (the control reflex) filed the golden split exactly; restart patients mostly have their equipment at home already (0.15 of the rate), and the control now files Ashby Vale first.
- Wendlebury's equipment need at 0.27 of covered patients: counting equipment patients at nought (R2) then filed the golden split; at 0.62, with the North depot's quick deliveries, R2 fills Cleeve Park and leaves Wendlebury short while the golden barely moves.
- The national weekly return by site: its nights per discharge rank the hospitals on the delay, an artifact on rung 0; it ships by trust, a distractor.
- A boundary change moving two wards from Ashby to Marchford district in April 2026 as an Ask B device: the ask's "district" would read two ways (as then or as now); the districts are stable and the county-line postcode district carries the district hazard.
- The winter's delayed bed-days total in the chart's title: within-trust moves leave the five-hospital total unchanged, so the cracker banks it; the title states what the chart shows, and the ask adds each hospital's delayed patients.
- Re-brokered and re-sent referrals as Ask B devices: whether a re-sent referral is a second referral the brokerage took reads two ways; cut.
- The part-filled hospital's bed-days at 967.45: rounding the value to two places first gives 968; the clearance brings one Cleeve Park delivery forward a day, so 968.23 rounds to 968 on every path.
- 2026-10-14, second-layer attempt after shipping (built to stage 4, not shipped): the patients the wait for home care itself sent to a rehabilitation bed or a care home (re-assessed while waiting, so the warehouse records them on pathway 2 or 3 and the default cohort conditions on the wait's own outcome), found from the brokerage's withdrawn hospital referrals, with the note's section 3 moved to "medically optimised for discharge home on pathway 1". Every free gate was green (27,838 checks, the verifier, a byte-identical rebuild, precut, leak.py), but the judge returned NOT_DETERMINISTIC and SEND_BACK on that pack (determinism_check_report_loop1.md, which covers the rejected prototype and not the shipped pack): no shipped sentence says a withdrawn hospital referral marks a patient optimised for home, and that reading alone moves Ashby Vale from 10 packages to none. Filing the population as "whatever pathway they left on" would hand over the post-treatment insight and leave only a record linkage a solver executes once told, so the call would turn on a filed rule; the leak reader also opened a fork on the package's "up to four weeks" (the re-assessed patients waited 23 to 26 nights on average). Reverted to the shipped pack, which the generator rebuilds byte-identical (27,095 checks); the shipped build's longest saving is 14 nights, so the four-week fork does not reach it.
- 2026-10-14, architecture 3 (a full refresh at the author's request, built to stage 4, not shipped): actuarial reserving for a motor bodily injury book (Ninebark Mutual, year end 2026, Forecasting), the paid history restated at the latest diagonal's closed shares of claimant features (Berquist-Sherman) after a claims platform slowed settlement, $400 million carried against the paid chain ladder's $325 million. Stage 3 green, the leak reader clean and the adjudicated clone check on Sonnet CLEAN, but the judge returned NOT_DETERMINISTIC, SEND_BACK: the reserving basis leaves the method to the actuary, and frequency-severity on paid per closed feature carries $350 million with nothing shipped selecting between them, while filing the method would make the decisive step rule application. The author restored this architecture; architecture 3's note, generator and judge report are in git at 6edd337.
- 2026-10-16, loop 1: filing the dependency as a discharge rule ("the ward discharges the patient once the delivery is made") in the equipment notes: it states the timing that a package's counterfactual turns on, so the decisive step would read as executing a filed rule; the route's definition files only what the equipment is for. The judge's optional pin (required_by is the discharge ready date) stays out for the same reason.
- 2026-10-16, loop 1: practices closed by merger on covered patients' spells (67, carried by the patient for every later admission): dropping the closed codes moved four hospitals' caps, a field reading that could decide figures on the main call; the registration is now taken at admission, so the closed codes sit only on spells admitted before each merger.
- 2026-10-16, loop 1: waits drawn flat between two bounds (home care 4 to 10 nights in Marchford, 6 to 14 in Ashby; South deliveries 5 to 13): the stage 4 reader read the covered patients' nights after the ready date, 3 to 14 with a hard floor, as too clean for delay data; every wait is now right-skewed by its quantile at the same uniform draw, so no other draw in the stream moved.
- 2026-10-16, loop 1: a weekend event moved to the Monday (and sometimes the Tuesday) by a fixed chance: every Saturday and Sunday the services turned down piled onto Monday, so Monday carried 1.8 times a midweek day's discharges and 2.3 times its deliveries, a new tell; a turned-down weekend day now redraws the wait from the service's own spread, which spreads the weekend's load across the working week.
- 2026-10-31, reship under the learning loop's rules: the acute, equipment and council extract notes and the data
  request log withdrawn (shipped files may not describe the data, and the log narrated a device); the two reporting
  conventions the notes carried that a figure turns on (delayed nights dated to their evening, a patient delayed in a
  month with one such night; the brokerage's wait in calendar days from receipt to start) moved into the fund note's
  monitoring section, and every other field reads from its own column. The prompt dropped its counts of hospitals,
  districts and months and opens on where the packages go.
- 2026-11-07, portal FAILED_TO_STUMP on architecture 2: both responses filed the golden split exactly (Royal Marchford 508, Wendlebury 350, Holmford 120, Cleeve Park 222, Ashby Vale none, 6,816 bed-days). The equipment wait running alongside the care wait is an overlap a careful response finds by joining the depot's deliveries to the covered patients, so the stump was a hidden overlap rather than a method the field's full practice gets wrong; the discharge world is spent and the slot re-roots in another domain.
- 2026-11-07, architecture 4 draw, candidates screened on paper before this card: the marginal travel a visit
  adds to a crew's day (a shared cost a removal does not save is architecture 2's logic, and routing reads the same
  for any field); a pooled fleet assessed by round rather than by vehicle (task153's fleet duty-cycle world, and the
  estimand has to name the rounds); arrivals seeing busier units than the time-average busy fraction (the optimization
  card's MEXCLP is the careful route and a replay of the calls lands the golden); failures per running hour or start
  (task170 and task176 screens); vacancy chains (task174, task137); turbine wakes (task187); demand-response snapback
  (task118); a lower screening threshold read from interval cancers in excess of the undetectable band (excess over a
  reference band is epidemiology's attributable-risk reflex, and the follow-up contradicts any extrapolation, so a
  back-test picks the golden); a written-off portfolio's hold value by payment arrangement (architecture 2's draw
  rejected the card portfolio sale, and a paying segment is a visible attribute); a setting active only above a
  threshold (task162), threshold counts from point predictions (task253, task151), staggered adoption (task136,
  task137), immortal time (task122), a post-treatment control (the careful textbook's own remedy). Chosen: the
  write-off a support package keeps off borrowers that depend on the supported firm's payments.
- Contagion defaults on the first payees of each payer (stage 3, 2026-11-08): the record's payee default rate then rose
  with receipt share (bands at 0.30, 0.43 and 0.57), so a logistic fit on share or three share bands moved Matai's
  figure and the total a NZ$50,000 bin. Reassigned within each payer so the rate is flat in share, every count and date
  kept; a two-band cut at 0.65 still moves a bin (SF11), as no assignment of 31 outcomes holds every cut.
- Matai Valley Foods in Manufacturing (stage 3, 2026-11-08): a rate by the defaulting payer's division (3 of 8 in
  Manufacturing) put Matai at NZ$1,650,000. Moved to Agriculture as a grower-packer supplying supermarkets, a division
  in which no payer defaulted.
- Fernmark Bank and Harcourt Packhouse (stage 3, 2026-11-08, H21): FernMark is New Zealand's national brand mark and
  Harcourts a national real-estate brand one letter away. Renamed Ruahine Bank and Marlowe Packhouse.
- The wholesale borrower's 2025 re-default (stage 3, 2026-11-08): put wholesale's share at exactly 6.25 per cent, a
  rounding tie. Dropping it changed the number of defaults and shifted every later draw (asks A and C moved); the third
  re-default moved to retail instead, same draws.
- Round watch-list PDs and balances, and a validation table marked Pass on every grade (stage 4 leak reader,
  2026-11-08): two-digit PDs, term loans drawn exactly to their limits and balances in whole thousands read as built,
  and an honest one-sided test fails grades 5 to 7. PDs now carry four decimals, balances cents, term loans amortise,
  and the table carries the bank's traffic light, amber in grades 5 to 7 and monitored.
- 2026-11-08, platform round 1 (run 1 98 on the call; run 2 58 off it, Kinloch and Ridgeway, after computing the eight dependants and the record's 13 of 31 and declining to price them): both runs filed every security value, total commitment and 2025 sector share exactly. The case-file asks were rule application (terms 4.1 and 4.2 file the indexation and the guarantee basis; the validation report files the default definition), and the hygiene battery (migration dates, discharges, former names, releases, loan-keyed register rows) was run by reflex, as Mark measured; dropped as asks, their files ship as context.
- The ranked list of the eight package values as an ask: six of the eight have no dependants, so the default path files six of eight cells; kept in the golden workbook as the table behind the choice, not asked.
- The write-off each package keeps off other borrowers, a list of the dependants with their own figures, or the intake's write-off split by sector as asks: each names or hints at the dependence in the prompt (the deep step handed over), and the sector split also sits NZ$6,300 under a bin edge at Transport.
- Envelopes of NZ$4.0, 7.0 and 8.0 million: the standing family spreads each across two NZ$50,000 bins; the grid runs from NZ$4.5 to NZ$6.5 million.
- The less dependent payees' count (6 of 61) as a graded figure: one of the six defaulted exactly 365 days after its payer, so a follow-up convention moves it to 5 of 61; it stays out of every answer block and the note.
- A second judgment the clean landed run would miss, to bring the paper pair under 50: none survives the freeze. An interval on the rise forks across methods, a timing split of 2027 against 2028 write-off reopens the call, and every leak-free handle on the dependence is a function of the package values the clean landed run computes; the pair stays at 56.0.
- Critical component 1 as a count ("8 from Matai Valley Foods"): the off-call run counted the eight and denied the protection, and kept the criterion; reworded, numbers frozen, so the component states that the package keeps them out of default.
- figures.json keys `commitment.Northgate Print` (1,750,000) and `sector_counts.I.1` (5) left with the case-file and sector asks; freeze.py read them as main-call figures only because their values coincide with Matai's NZ$1,750,000 and the 5 of 211 control count, which stay in figures.json under their own keys (`--allow` on both).
- 2026-11-08, platform round 2 on architecture 4 (the re-sited asks: fall-back intakes and the envelope curve): both runs landed Kinloch Engineering and Matai Valley Foods (the author's word; texts not pasted). The payer dependence was a mechanism the transactions and the default register visibly carried, and both runs priced it once they had measured it. Architecture 4 is spent, and its world (Ruahine Bank, its borrowers, its payments) with it.
- 2026-11-08, cleanup at the author's word: every file of architectures 1 to 4 (generators, packs, goldens, reports, runs) removed from the folder; this record, the run record and the card's lineage keep what each died of.
- 2026-11-08, architecture 5 draw, on paper: the excess default risk of a borrower in the year after a downgrade (rating momentum), with 2027 following a 2026 downgrade wave and the grade-only transition matrix validating on the pooled history. Stripped of nouns it is mark179's driver (a chance that rises for a period after an event, the forecast year following a surge of such events), and a path property the state omits is the same abstraction as task1's provider tenure; dropped before a card was written.
- 2026-11-08, architecture 5 draw, on paper: two effects offsetting inside the observed window (mix against rate under a flat total) as the deep step; task3 arch 3 and task8 arch 18 both carry it, so a third would read as a template.
- 2026-11-08, architecture 5 at stage 2, the recent-experience route (seed 129): the record's latest years averaged flat,
  pooled or by book, landed the plan cell and both book cells, because the record's recent defaults were as stale as the
  year-end book a year later; the world now has the workout unit re-inspect facilities of €1 million or more at
  referral from 2022, so a third of the recent defaults rest on fresh inspections and recent experience files €0.8 to
  €1.4 million.
- Watch-list re-inspections at a downgrade to grade 7 or 8 from 2023 (stage 2): they reached 21 of 354 recent defaults
  and moved nothing; re-inspecting every stage 2 facility at its annual review from 2022 freshened the riskiest part of
  the year-end book, pulled the golden to €2.36 million beside the record's average (€2.24 million), and was reverted.
- No go-live roll-forward (stage 2): defaults from January to April 2012 were set against un-indexed 2004 to 2007
  inspections (ratios 0.2 to 0.35), which bent every functional form apart; the warehouse's go-live now rolls every
  value forward to 2011 Q3 on 3 January 2012.
- The 2013 to 2019 recovery at full strength (stage 2): the index rose 3 to 5 per cent between the carried quarter and
  the inspection at default, so the raw and index-adjusted ratios split the plan figure by 7 per cent; every index move
  after the 2012 trough is halved and SF21 asserts the two land together.
- A year-end book facility with no valuation row in force (stage 2): a December 2026 origination whose inspection loaded
  on 10 January 2027; inspections dated in the year now load by 31 December, and the register writes no roll-forward
  over a newer inspection already on file.
- Seeds 129 to 152 scanned with the master scale as the one free scale (stage 2): seed 141 at 0.82 of the earlier
  published scale is the only world where every standing rival files the three graded cells with €48,000 or more inside
  the book cells and €127,000 inside the plan cell, the five facilities hold under every split member, the pooled run
  misses both book cells and every shallow route misses the plan cell by €375,000 or more.
- The memo's "the expected value of the security at that date" (stage 4, leak reader 1): read literally as the register's
  latest value with prices held, which is the default path, and it left room for the unconditional market value and for
  the loss averaged over the values an inspection might return (€2.48 million, so €2.5 million); the memo now files V as
  the value the bank would expect its inspection to put on the security if the facility defaulted, and the loss as
  CRE-LGD-3 applied to it (SF23), naming no record, staleness or shortfall.
- Customer names drawn by lending book alone and floor areas drawn flat in a range (stage 4, leak reader 1): a
  "Hospitality Ltd" carried a nursing-care code and a 4,459 m2 medical centre sat on a small value; names now follow
  the property's business and areas the first inspection's value at a regional rate per square metre, both on streams
  of their own so no graded draw moved.
- Customer, legacy facility and property numbers in steps of 13, 37 and 11 (stage 4, leak reader 2): sorted, each ran
  as an arithmetic progression; the numbers now carry irregular gaps from a stream of their own, increasing in the same
  order, so no sort and no graded figure moved.
- Secondary figures stated at a precision no other construction reproduces (stage 4, determinism judge, FIX_NOW): the
  record's 844 (a count of properties, written as defaults; the judge counted 833 to 883 by its own rules), the cohort
  since 2022 as 112 of 319 and 10 per cent (122 of 322 and 8.7), the band means 75 and 9 per cent (73.7 and 8.5), the
  CSV's euro total and the unrounded plan figure (the judge's base €2.06 million), "€0.2 million" beside a €500,000
  grid, and the order of the third and fourth facilities. The blocks now state the graded cells at the prompt's
  rounding, the fitted ratios (reproduced to the whole per cent), the model figure as €0.22 million, the working counts
  in words with each bound asserted in checks.py, and the five as a set with the clear leader named.
- The Step-by-Step's "more than 20 standard errors" and a column list read as required (stage 4, re-judge, optional
  notes): 20 held for the pooled slope (23) and not for each book's (15 and 19), now "more than 10 in each lending
  book", asserted per book; the prompt names no CSV columns, so the answer now requires each facility's number and
  its expected loss and calls the golden file's other columns a choice of layout.
- 2026-11-08, platform round 1 on architecture 5: not stumped; the model filed the €2.0 million plan figure (the author's word; run
  texts not pasted). The stage 4 re-judge had named the risk: filing V as the value the bank would expect its
  inspection to put on the security if the facility defaulted sends a solver to the record of inspections at default,
  and once that record is built the shortfall's slope on years since inspection is the visible covariate a strong
  model fits; architecture 5 is spent.
