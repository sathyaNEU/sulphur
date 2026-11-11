# task9: how many drive replacements Halden Vault should plan for each quarter from October 2026 to September 2027, how sure it can be, and whether to migrate the hot batch's vaults

## Draw

Subdomain: General Statistics & Data Science, Bayesian modeling & posterior inference (a posterior predictive forecast
  of replacement counts from a hierarchical hazard model); the author supplied the draw as Concept 1 of the three
  concepts prepared on 2026-11-10.
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast path with bands and drivers: the fleet's replacements for each quarter from 2026-Q4 to
  2027-Q3 by data centre and drive family with 80 per cent intervals and their drivers, with the hot batch's migrate
  call and the forward rate at which it flips.
Weight: validation. Most of the work is making the bands honest and showing it: the intervals have to carry vault and
  batch frailty, shocks shared within a chassis and the uncertainty in a ramping batch's path, and they are judged by
  how intervals built the same way would have covered the four quarters to 30 September 2026; the last three builds
  sat on metric or rule design (task13), synthesis (task15) and measurement (task14).
Data-native sentence: a drive fleet's records start mid-life at an acquired centre that kept none of its early
  failures, lose their worst old vaults to retirement before the forecast, carry one manufacturing batch whose hazard
  is accelerating, and count failures that cluster by chassis, so the age, the population, the trend and the spread
  of next year's replacements each have to be rebuilt from what the records cannot see.
People: Amanda Higgins (fleet reliability lead, owner of the operations wiki), Sandra Collins (DC-3 site lead, who ran
  the Brightstore migration), Emily Salas (capacity planning), Heidi Turner (data-centre technician lead); drawn with
  guard.py names --geo us --seed 9011.

1. Fit: the client's General Statistics strategy 8 (spares for failures never seen start) is the nearest client
   direction; this draw differs in structure: a forecast path with bands back-tested on clustered failures, a ramping
   defect batch and survivors thinned by selective retirement carry the weight, and the truncation step is one result
   of eight. Concept 1's own nearest exercises (Hong, Meeker and McCalley's left-truncated fleet forecast; Backblaze's
   drive statistics) are lessons, not the structure.
2. Task type: missing data, censoring and measurement error serves descriptive work, monitoring and comparison in the
   taxonomy, not forecasting, so the task type is Bayesian modeling and posterior inference: the forecast is a posterior
   predictive count from a hierarchical hazard model, and its bands are what the task is judged on.
3. Data: generated, simulating the fleet's daily process (vault commissioning, batch frailty, bathtub hazards, a hot
   batch on old firmware, chassis power and cooling events, SMART precursors, two health-pull policies, selective
   decommissioning, the Brightstore acquisition and its migration), with the mess the systems produce.
4. Decision: the quarterly spare order (one-quarter lead time, a 10 per cent stock-out tolerance), whether to migrate
   the hot batch's vaults in the fourth quarter of 2026 or run them to failure, and the planning bands; forward facing
   (replacements in quarters not yet run).
5. Shell: question form how many, deliverables a spreadsheet and a chart of the quarterly path with its bands (png and
   xlsx, away from the over-quota docx and xlsx pair).
6. Card: shape 02, gap population then time, pattern E (the surviving vaults are a conditioned yield), generators G9,
   G14, G16, Gate G forecasting, calibration form existing_book_actuals (the four quarters to 30 September 2026),
   context artifact close_out_summary (the Q3 2026 fleet reliability close-out), forum operations_desk, forcing event
   cutover_or_migration, organisation software_or_platform, role capacity_planner, strategy forecast_method_backtest.
7. Guard: registered 2026-11-11T14:36:12Z, WARN only. overuse.domain (General Statistics in 4 of the last 12): the
   author assigned the domain with the concepts. test.same_driver_older against mark124 answered in the card's
   differentiation. ban.strategy (population_selection, informative_censoring), ban.artifact (monitoring_export) and
   ban.forcing_event (purchase_order_or_contract) cleared by redrawing to the honest alternatives: the forecast is
   judged on held-out quarters through a regime change and a ramp (forecast_method_backtest), the dashboard is the
   quarter's close-out, and the migration is the cutover the call decides.
8. Slot: the author cleared task9 on 2026-11-11; its ten quantitative-finance architectures are in git history and the
   card's lineage.

## Deep reasoning

Task type: bayesian-modeling-posterior-inference, serving Forecasting & Predictive Modeling.
Not one thing (sketch at the draw): the strongest single piece is the hot batch's ramp; a run that has it still has to
  rebuild DC-3's ages, separate the old family's survivors from its retired vaults, carry clustered shocks into the
  bands and read the bands against the held-out quarters.
One-fact test (sketch at the draw): "DC-3's install dates are its migration date" rescues R1 only; "one HX-8 batch on
  the old firmware is ramping" rescues R2 and not the ramp's path; "failures cluster by chassis and vault" reaches R6,
  R7 and the spare order, about a third, and is held there at stage 2; counted by effort.py at stage 3.

## Results chain

Sketch at the draw; pins, bands and the carry-forward line are written at stage 2.

| ID | Result (checkable) | Area | Hurried analyst |
|---|---|---|---|
| R1 | DC-3's replacements over the four quarters, its drives' ages rebuilt from the serial's manufacture week and the deploy lag | missingness-measurement | method shortcut: age from first sight at migration (about 175 against 590) |
| R2 | The hot batch named (model, manufacture window, firmware) with its current annualized replacement rate | exploration-triage | narrow look: the family's lifetime or trailing rate (2.2 or 3.6 per cent against 6.5) |
| R3 | The hot batch's replacements over the four quarters and its doubling time | forecasting | first story: the trailing rate carried flat (about 195 against 680) |
| R4 | The surviving OM-6 vaults' forward rate and four-quarter count | modeling | method shortcut: one age-hazard curve on every vault's history, retired vaults included (355 against 265) |
| R5 | The fleet's replacements in each quarter from 2026-Q4 to 2027-Q3, by data centre and family | forecasting | unfinished chain: trailing rates times counts (about 1,410 against 2,100) |
| R6 | The 80 per cent bands on the fleet's quarterly path | uncertainty | self-confirming check: Poisson or drive-level bootstrap bands, a few per cent wide |
| R7 | How intervals built the same way would have covered the four quarters to 30 September 2026 | validation | self-confirming check: in-sample fit, or Poisson bands covering about four cells in ten |
| R8 | The fourth-quarter spare order per family at a 10 per cent stock-out risk, and the hot batch's migrate call with its flip point | synthesis | unfinished chain: orders at the mean forecast and the trailing rate's "do not migrate" |

## Tried and rejected

- 2026-11-11, missing data, censoring and measurement error as the task type: the taxonomy has it serve descriptive work,
  monitoring and comparison, not forecasting (guard three_rules.task_type), so the forecast is drawn as a posterior
  predictive count under Bayesian modeling and posterior inference.
- 2026-11-11, Concept 3 (the speech model under the speed cap): benchmarking and ablations is task15's task type and its
  lessons sit on the client's strategies 4 and 5; Concept 1 drawn first as the author's ranking puts it.
