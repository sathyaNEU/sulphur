# task9: how many drive replacements Halden Vault should plan for in each quarter from October 2026 to September 2027, how sure it can be, which of the bad-build batch's vaults to migrate, and the spares to order for the fourth quarter

## Draw

Subdomain: General Statistics & Data Science, Bayesian modeling & posterior inference (a posterior predictive forecast of replacement counts from a hierarchical hazard model); the author supplied the draw as Concept 1 of the three concepts prepared on 2026-11-10.
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast path with bands and drivers: the fleet's replacements for each quarter from 2026-Q4 to 2027-Q3 by data centre and drive family with 80 per cent intervals and their drivers, the batch's per-vault migration call with the doubling time at which it flips, and the fourth quarter's spare order.
Weight: validation. Most of the work is making the forecast honest and showing it: the batch has to be located and kept apart from the firmware it shares, the old family's survivors priced on their own levels, the intervals built from every source of uncertainty and checked against the year to 30 September 2026 as a forecaster at 30 September 2025 would have made them; the last three builds sat on metric or rule design (task13), synthesis (task15) and measurement (task14).
Data-native sentence: a drive fleet's records start mid-life at an acquired centre that kept none of its early failures, lose their worst old vaults to retirement before the forecast, carry one manufacturing window whose hazard is accelerating inside a firmware release that also ran on normal builds, and spread that window unevenly across its vaults, so the age, the population, the batch and the per-vault economics each have to be rebuilt from what the records cannot see.
People: Amanda Higgins (fleet reliability lead, owner of the operations wiki), Sandra Collins (DC-3 site lead, who ran the Brightstore migration), Emily Salas (capacity planning, author of the forecast), Heidi Turner (data-centre technician lead); drawn with guard.py names --geo us --seed 9011.

1. Fit: the client's strategy 8 in its machine-learning group (spares for failures you never saw start) is the nearest client direction; this draw differs in structure: a forecast path whose batch must be told apart from its firmware, whose old family's survivors were selected by retirement, and whose migration is decided vault by vault; the truncation step is one result of eight.
2. Task type: missing data, censoring and measurement error serves descriptive work, monitoring and comparison in the taxonomy, not forecasting, so the task type is Bayesian modeling and posterior inference: the forecast is a posterior predictive count from a hierarchical hazard model, and the decisions read its draws.
3. Data: generated, simulating the fleet's daily process (vault commissioning, batch frailty, bathtub hazards, one bad build window, chassis power and cooling events, SMART precursors, two health-pull policies, selective decommissioning, the Brightstore acquisition and its migration), with the mess the systems produce; seed 9017.
4. Decision: the quarterly plan, which of the batch's vaults to migrate in the fourth quarter of 2026 (each judged on its own replacements over 24 months against the migration cost), and the fourth quarter's spare order at a 10 per cent stock-out tolerance; forward facing (replacements in quarters not yet run).
5. Shell: question form how many, deliverables a spreadsheet and a chart of the quarterly path with its interval (xlsx and png).
6. Card: shape 02, gap population then time, pattern E (the surviving vaults are a conditioned yield), generators G9, G14, G16, Gate G forecasting, calibration form existing_book_actuals (the four quarters to 30 September 2026), context artifact close_out_summary (the Q3 2026 fleet reliability close-out), forum operations_desk, forcing event cutover_or_migration, organisation software_or_platform, role capacity_planner, strategy forecast_method_backtest.
7. Guard: registered 2026-11-11T14:36:12Z, the card brought up to the built chain at stage 3 (WARN only): overuse.domain (the author assigned the domain with the concepts); test.same_driver_older against mark124 answered in the card's differentiation; the skeleton's house-shell warning on forecast_figure_with_range answered in the Frontier check.
8. Slot: the author cleared task9 on 2026-11-11; its ten quantitative-finance architectures are in git history and the card's lineage.

## Deep reasoning

Task type: bayesian-modeling-posterior-inference, serving Forecasting & Predictive Modeling: family hazards by age with a pooled infant term and age slopes shrunk to the fleet's, gamma vault frailty by empirical Bayes, a ramp for one build window averaged over its shapes by likelihood, and posterior predictive draws that every figure and decision reads.
Domain test: a reliability forecaster's own objects: drive-days at risk by age with delayed entry, per-vault frailty against a family curve, a defect window located by build week, a predictive interval checked by its coverage on a held-out year, a newsvendor quantile for spares and a cost comparison per vault on expected replacements.
Swap: put a hospital's wards and patients in for vaults and drives and the call stops making sense: there is no acquired site whose records start at migration with ages recoverable from a serial's build week, no vault retired by its failure rate at a review, no build window inside a firmware release, and no per-vault migration priced at 240 replacements over 24 months.
Where the weight sits: validation. The back-test result (R6) and the path's interval (R5) are built from every source of uncertainty the golden carries (each family's curve, each vault's level, the ramp's shape and slope), and the careful work that earns them is long rather than clever: three age sources joined for DC-3, a scan over build weeks, vault levels, a model-averaged ramp and a cut at 30 September 2025 rebuilt end to end.
Layer 1: DC-3 install dates set to the migration day (the inventory system's import), model-string aliases (three export generations), mixed date formats (two ticketing exports), about 1 per cent duplicate telemetry rows (warehouse reloads), reseats back within 30 days (bench tests and cable faults), 15 per cent blank removal reasons recovered from ticket notes, boot SSDs and the QA-01 burn-in vault in the inventory, agent outage gaps, serials printed with dashes in Brightstore's handover; none decides a result alone.
Not one thing: the strongest single piece is the batch's build window; a run that has it still has to price the OM-6 survivors on their own levels (R4), rebuild DC-3's ages (R1), carry the ramp's uncertainty into the interval and the back-test (R5, R6), order spares on the survivors' and the batch's own tails (R7), and decide the migration vault by vault, where B15 holds a third of the batch and does not pay (R8).
One-fact test: "The vaults retired at the reviews were the ones failing fastest" rescues 2 of 8 (R4, R7); the batch-by-build-week hint rescues R2 and leaves R8 short because the average-share rule still migrates B15; the per-vault hint rescues nothing on its own because the firmware story puts B15 over the line (effort.py hints).
Not semantics: every field read correctly (the wiki's FAIL and PULL, the reseat rule, the P2 start, the migration day, the serial's YYWW, the stock and costs in the YAML) still leaves the firmware story, the pooled survivors and the average-share migration wrong: each is a modelling choice about the same correctly read records.
Not rule application: no filed procedure locates the batch, sets a vault's level, builds an interval or decides a vault; the wiki defines what a replacement is and the YAML gives the costs, and everything between is estimated.
Estimand: the prompt files each result's population (the data drives in service on 30 September 2026 plus the scheduled vault installs), window (each quarter from October 2026 to September 2027; the 24 months from now for migration; the year after 30 September 2025 for the back-test, by family and quarter in vaults that stayed in service), unit (replacements as the wiki defines them; the batch's July to September 2026 rate annualized; spares per family) and comparison (migration against running to failure).
No decoy: no memo, draft or close-out argues a wrong answer; the Q3 close-out page shows replacement rates by data centre and answers its own question (last quarter's rates) correctly; the vendor datasheets' reliability claims and the environment and boot-SSD files are on file and unused.
No replay: no result re-derives a published figure; Brightstore's legacy failure summary is counts per rack-year with no serials, and no stated number in the pack is wrong.
Pinned: each result's rivals are run on the cut pack (an infant term fading over two months; an infant term fading over four months; each family's own age slope, unshrunk; the ramp read as exponential alone; the ramp read as linear alone; the build window a week narrower at each end; another seed for the draws; DC-3's ages from the mean deploy lag) and every one lands in its band and migrates B16, B17, B18, B19; the build window a week wider is ruled out by the week-15 builds' own rate; the shortcuts land outside on the results they price (figures.json routes, checks.py).
Run forecast: R2 stopped at the first story (the HX8.2.0 firmware), R4 and R7 a method shortcut (one curve per family over every vault, the survivors priced on the retired vaults' history), R8 a method shortcut (every vault holding the batch migrated on the batch's average share, and the firmware story's flip point); R1, R3, R5 and R6 are earned by careful work and lost by the quick pass.
Strategy label: WORKS IN FORM (the client's deep judgments "A forecast that has to earn its place" and "Separating two explanations for one pattern"); nearest client entry Machine Learning Research 8, Spares for failures you never saw start.
Depth level: 4. Three independent judgments price the chain (the build window against the firmware, the survivors' own levels, the vault as the decision unit), each needing estimation, and the shortcuts land on different wrong answers: the firmware story and the average share migrate all five vaults, the batch inside its family migrates B16, the close-out's rates migrate none.
Lesson: a forecast whose bad batch shares an attribute with normal units, whose old units were thinned by their own failures and whose action is taken per unit needs the batch located by the attribute that carries the hazard, the survivors priced on their own history and the action priced on each unit's own expected events; no build on file teaches the three together.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | DC-3's replacements over the four quarters: 784 | missingness and measurement | the migration day in the inventory, the handover manifest's deploy dates, VB-12 power-on hours, the serial's build week and Halden's own HX-8 deploy lag (67 days) | 720 to 862 | method shortcut: the close-out's DC-3 rate carried (634); ages read from the inventory's install date land at 751, inside the band, because the KS-10 curve refits to the shifted ages | - | Component 1 |
| R2 | the bad-build batch: 4,160 drives in service built 2024-W16 to 2024-W30, at 7.8 per cent a year over July to September 2026 | investigation loops | the serial's YYWW and the replacements of the year to 30 September 2026 against each vault's earlier level; the prompt's July to September 2026 rate | drives 3,538 to 4,326; rate 7.2 per cent to 8.5 per cent | first story: the HX8.2.0 firmware as the batch (5,148 drives at 6.8 per cent), which passes its own check by release | - | Ask 1 |
| R3 | the batch's replacements over the four quarters: 567 | forecasting | the ramp in months since build, its shapes weighted by likelihood | 520 to 665 | method shortcut: the batch inside its family's curve (296) or the close-out's DC-2 HX-8 rate (357) | R2 | Component 2 |
| R4 | the surviving OM-6 vaults' replacements over the four quarters: 281 | modeling | each vault's observed against expected replacements (gamma frailty) and the review dates in the event log | 264 to 300 | method shortcut: one age curve over every OM-6 vault's history, the retired vaults included (345) | - | Ask 2 |
| R5 | the fleet's path 553, 587, 642, 701 with an 80 per cent interval 447 wide over the four quarters | forecasting | the posterior predictive draws (P10 to P90, the prompt's 80 per cent) | each quarter 519 to 593; 552 to 632; 600 to 699; 651 to 774; width 342 to 558 | method shortcut: Poisson counts at the fitted values (width 130) or the close-out's rates carried (465 a quarter) | R1, R3, R4 | Component 3 |
| R6 | coverage of intervals built the same way at 30 September 2025: 78.1 per cent of 32 family-quarter cells | validation | the prompt's cut, window, grain and stayed vaults; an actual on a limit counts inside | 67.0 per cent to 89.2 per cent | unfinished chain: Poisson counts at the fitted values cover 59.4 per cent; counting every removal in the age curve 31.2 per cent | independent: the record to 30 September 2025 and the year after it | Component 4 |
| R7 | the fourth quarter's spare order per family (402 in all) | synthesis | the YAML's stock on hand and 10 per cent stock-out tolerance; the order is the 90th percentile less stock | each family within 10 per cent of the rivals' range | method shortcut: orders from one curve over every vault (OM-6 56, KS-10 104 against 39 and 89) | R5 | Ask 3 |
| R8 | migrate B16, B17, B18, B19 in the fourth quarter of 2026 and run B15; a vault made wholly of the batch stops paying if its rate doubles more slowly than every 24.1 months | synthesis | the YAML's migration and handling costs (240 replacements per vault over the 24 months from 1 October 2026) | the vault set exact; the flip point 21.7 to 27.8 months | method shortcut: every vault holding the batch migrated on the batch's average share (B15, B16, B17, B18, B19), and the firmware story (B15, B16, B17, B18, B19, flip 18.1 months) | R2, R3 | Recommendation |

Carry-forward: R1, R2, R4 and R6 stand on inputs of their own (DC-3's records, the HX-8 serials, the OM-6 vaults' histories, the record to 30 September 2025); R3 falls with R2's window, R5 with R1, R3 and R4 together (an AND: none alone moves the path out of its band), R7 with R5's family tails, and R8 with R2 and R3, where the per-vault rule is a judgment of its own.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| the bad build window (2024 weeks 16 to 30) inside the HX8.2.0 release (weeks 10 to 30) | constructed | no: the window's drives also sit as spares in the DC-1 HX-8 vaults, and the release's normal builds of weeks 10 to 15 sit in B16 and B17, which pay either way, as well as in B15 | modelling: a build-week scan of the last year's replacements against each vault's earlier level | modelling | keep |
| selective retirement: each review retired the vault failing fastest over its trailing year | constructed | no: KS-10's March 2026 review in DC-3 did the same, where DC-3's figure stays inside its band | modelling: each vault's observed against expected replacements, read against the review dates | modelling | keep |
| the batch held unevenly: B15 was filled from builds a few weeks before the window | constructed | no: every vault mixes builds and spares, and the DC-1 vaults hold batch spares | modelling: each vault's expected replacements over 24 months from its own drives | modelling | keep |
| DC-3's install dates set to the 2024-03-01 migration | constructed | no: both DC-3 families, KS-10 and VB-12 | a targeted query: install dates by data centre against the wiki's DC-3 note | modelling: ages rebuilt from three sources and the hazard fitted with each drive entering at its age on the migration day | keep (earned by careful runs) |
| P2's harvest of the prevalent SMART 187 stock, June to August 2025 | constructed | no: fleet-wide, every family | a targeted query: the pulls' trigger in the technicians' notes against the P2 start | modelling: a second removal stream at its own steady rate from September 2025, kept out of the wear-out curve | keep (texture; earned by careful runs) |

Shared incidents (chassis power events and whole-vault cooling excursions, 70 per cent logged) run through every data centre; with each vault's level fitted, the vault-quarter residuals carry no measurable spread beyond Poisson (dispersion estimate unbounded), so they decide nothing.

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 DC-3's replacements over the four quarters | Partly | Right | Right |
| R2 the bad-build batch: its drives in service and their July to September 2026 rate | Missed | Missed | Right |
| R3 the batch's replacements over the four quarters | Missed | Right | Right |
| R4 the surviving OM-6 vaults' replacements over the four quarters | Missed | Missed | Right |
| R5 the fleet's replacements in each quarter and the width of the four quarters' 80 per cent interval | Missed | Right | Right |
| R6 how often intervals built the same way covered the year to 30 September 2026 | Missed | Right | Right |
| R7 the fourth-quarter spare order per family | Missed | Partly | Right |
| R8 the vaults to migrate and the doubling time at which migration stops paying | Missed | Missed | Right |
| Roughly | 0.5 of 8 | 4.5 of 8 | 8 of 8 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "The vaults retired at the reviews were the ones failing fastest"; rescues 2 of 8 results
Pair estimate: 40.2

## Data provenance

Source: generated by task9/generator (world.py simulates the fleet day by day per vault; pack.py and docs.py write the records the way Halden's systems export them), seed 9017.
Behaves like the real thing: replacement rates by family and age follow published fleet behaviour (rates rising with age, an infant uplift, wide vault-to-vault differences, one model's batch whose yearly rate climbs steeply), health pulls take a share of failures before they happen, and an acquired site's records start at its migration.
Genuine patterns: (1) wear-out rising with age, steeply for the oldest families (2) vault and batch frailty across every family (3) an accelerating hazard in one build window (4) shared power and cooling incidents (5) a policy change in June 2025 with a one-off harvest (6) spares starting young in every slot (7) scheduled installs.
Problems by process: the migration's import set DC-3's install dates; Brightstore kept deploy dates for about 40 per cent of its drives and KS-10 drives report no power-on hours to Halden's agent; three export generations wrote model strings three ways; two ticketing systems wrote dates two ways; the warehouse reloads duplicate about 1 per cent of telemetry rows; technicians leave about 15 per cent of removal reasons blank; reseats come back within 30 days; agent outages blank days; the QA burn-in vault and boot SSDs share the inventory.
Breadth: 13 files; 81,263 drives in 63 vaults over three data centres and nine families; about a million drive-quarter rows; 32 family-quarter back-test cells; five candidate vaults for migration.

## Template check

Chain signature: missingness-measurement, investigation-loops, forecasting, modeling, forecasting, validation, synthesis, synthesis
Question form: how many (each quarter's replacements), with how sure, which vaults and how many spares in the asks
Nearest build: mark124 on the structural driver (a forecast whose analogs mislead), differentiated on the card; no build on file shares the chain of areas and the answer shape.
Abstraction sentence: none writable against a build on file: the nearest would read "a forecast whose population was thinned by its own failures", and no build on file adds a defect window inside a shared attribute and a per-unit action priced on each unit's own expected events.

## Frontier check

Precedents: R2 L26 (a plausible shallower explanation that passes its own segment checks: the firmware release); R4 L14 and L13 (survivors of a selection priced on the whole family's curve); R7 L14 (the survivors' spares at the pooled rate); R8 L17 and L09 (every vault holding the batch migrated on the batch's average share, the per-vault split seen and dropped at the decision); the same ids sit on the results in generator/effort.json.
Shallow path checks: R2's firmware story passes its check by release (HX8.2.0 high, HX8.1.4 and HX8.2.3 normal); the check of another kind is the rate by build week inside HX8.2.0 from the serial (the Kestrel guide's YYWW), where weeks 10 to 15 fail at the normal rate. R4's pooled curve passes a back-test on the whole family (the retired vaults' excess offsets the survivors' shortfall); the check that refutes it is the survivors' own observed against expected replacements, read against the review dates in vault_events. R8's average-share rule passes its own break-even (the batch loses 36.3 per cent within 24 months against 20); the check of another kind is each vault's own expected replacements, where B15 has 146 against 240.
Assumption made false: a run lists "the migrated vaults are like the batch on average" and "the vaults still in service are like the family"; the world's process makes both false (B15 was filled from builds a few weeks before the window, and each review retired the vault failing fastest), and the pack tests them in the serials' build weeks by vault (the inventory) and in the review dates and retired vaults (vault_events) against each vault's history.
Forcing: the line is 240 replacements per vault over the 24 months from 1 October 2026; every golden-family variant (9) migrates B16, B17, B18, B19, the nearest vault clearing the line by 19 per cent; the shortcuts migrate other sets (the firmware release as the batch: B15, B16, B17, B18, B19; every batch vault on the batch's share: B15, B16, B17, B18, B19; the hot batch inside its family: B16; the build window a week wider at each end: B15, B16, B17, B18, B19; careful but hurried: B15, B16, B17, B18, B19; the quarter's close-out carried: none); and each fitted input moved by 20 per cent (the batch's level, its forward growth, both together) keeps the same vaults.
Noun swap: nearest by skeleton.py check is depth:279e74f2 (the borrowed pit crew's fourteen days), severity none; its nouns swapped in, the decision form (a timing choice), the answer pattern and the moves do not carry across, and only the marginal-unit lesson is shared, here one step among several and not the one the forecast turns on.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a removal whose serial is back within 30 days | a replacement; not a replacement | not a replacement (merged) | the wiki: count the removal out and the drive as in service throughout |
| SF2 | health pulls of healthy drives under P2 (SMART 187 above 0) | a replacement; not a replacement | a replacement at P2's steady rate from September 2025, the June to August 2025 harvest not carried forward | the wiki's PULL definition; the harvest is the prevalent stock, visible once in the record |
| SF3 | the batch's current rate | the last quarter's rate; the trailing year's; the model's hazard at the cut | July to September 2026 replacements per drive-year, annualized | the prompt's own words |
| SF4 | the population forecast | with further retirements; without | drives in service on 30 September 2026 plus the capacity plan's installs, no further retirement | the prompt; vault_events schedules no review after the record |
| SF5 | when a vault's migration pays | the batch's share; the vault's own replacements; net of the new drives' failures | the vault's own replacements over 24 months from 1 October 2026 against 240 | the prompt ("costs less than running them to failure over 24 months") and the YAML's costs; netting the new drives' failures is the same call (every vault clears by 19 per cent) |
| SF6 | the spare order | the mean; the 90th percentile; less stock or not | the 90th percentile of the quarter's replacements less stock on hand, never below zero | the prompt's 10 per cent and the YAML's stock on hand |
| SF7 | the back-test's cells and coverage | fleet quarters; family quarters; with retired vaults or not | family by quarter in the vaults that stayed in service, an actual on a limit inside | the prompt's own words |
| SF8 | the 80 per cent interval | central; one-sided | the 10th to 90th percentile of the predictive draws | same call: the prompt's 80 per cent read as the central interval, the convention every forecast sheet uses |
| SF9 | the flip point | per vault; for the batch | the doubling time at which a vault made wholly of the batch, starting at the July to September 2026 rate, stops paying | the prompt ("the doubling time of that rate") |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the prompt's drives in service on 30 September 2026 plus scheduled installs (SF4); the back-test's stayed vaults (SF7) |
| 2 | Unit of account: a replacement as the wiki defines it; a vault for migration; a family for spares |
| 3 | Attribution window: quarters by removal date; the 24 months from 1 October 2026; the year after 30 September 2025 |
| 4 | As-of dating: the record's last day, 30 September 2026; stock on hand at that date (YAML) |
| 5 | Version basis: one inventory, the latest record per serial; reseats merged (SF1) |
| 6 | Denominator: drive-years in service for rates; 1,200 drives per vault for the break-even |
| 7 | Weighting: none; counts are summed |
| 8 | Window length: the batch's rate over July to September 2026 (SF3); the scan over the year to the cut |
| 9 | Boundary inclusivity: removal dates inside a quarter; an actual on an interval limit counts inside (SF7) |
| 10 | Rounding path: counts rounded once, at the end |
| 11 | Tie-break: none needed; every vault clears the break-even by 19 per cent |
| 12 | Maturity and censoring: drive-days to each drive's exit or the cut, delayed entry for DC-3 |
| 13 | Order of operations: ages rebuilt, then curves, frailty, the batch, the draws, then the decisions |
| 14 | Row order: no figure depends on file order (asserted by two byte-identical builds) |
| 15 | Duplicate resolution: duplicate telemetry rows dropped; one inventory row per serial and service life |
| 16 | Identity normalisation: dashed Brightstore serials matched to the inventory's; model aliases to nine families |
| 17 | Netting against gross: a reseat nets out; a DECOM removal is not a replacement |
| 18 | Dimensional units: replacements, drive-years, months since build, USD |
| 19 | Code and status semantics: FAIL and PULL from the wiki; blank reasons from ticket categories |
| 20 | Integerisation: the spare order is the 90th percentile rounded up less stock, floored at zero (SF6) |
| 21 | Clause scope: P1 and P2 by their dates; the reseat rule on any removal |
| 22 | Forward window contents: the capacity plan's installs; no retirement scheduled (SF4) |

## Literal reader

A reader executing the prompt word for word counts replacements as the wiki defines them for the drives in service on 30 September 2026 and the scheduled installs, quarter by quarter, gives each quarter and the four quarters' total an 80 per cent interval, takes the batch with the highest forward risk and its July to September 2026 rate, judges each of its vaults on whether migration costs less than running to failure over 24 months, orders spares so the chance of running short is at most 10 per cent, and scores intervals built the same way from the record to 30 September 2025 by family and quarter in the vaults that stayed in service: each of these is the golden's estimand.

## Prompt contract

A voice rewrite may not drop or change: the question (how many replacements per quarter from October 2026 to September 2027, and how sure); the population (drives in service on 30 September 2026 plus scheduled installs); each quarter's count and the four quarters' total with 80 per cent intervals by data centre and family, and their drivers; the batch with the highest forward risk, its drives in service, its July to September 2026 rate annualized, its four-quarter replacements, the migrate-or-run comparison over 24 months for its vaults and the doubling time at which it flips; the fourth quarter's spares per family at a 10 per cent chance of running short; the coverage of intervals built the same way from the record to 30 September 2025, by family and quarter in vaults that stayed in service; a spreadsheet and a chart. It must never add a rounding instruction, a method (scan, frailty, bootstrap, back-test), a warning, an attached file's name, a role or a count the data hold.

## Tried and rejected

- 2026-11-11, missing data, censoring and measurement error as the task type: the taxonomy has it serve descriptive work,
  monitoring and comparison, not forecasting (guard three_rules.task_type), so the forecast is drawn as a posterior
  predictive count under Bayesian modeling and posterior inference.
- 2026-11-11, Concept 3 (the speech model under the speed cap): benchmarking and ablations is task15's task type and its
  lessons sit on the client's strategies 4 and 5; Concept 1 drawn first as the author's ranking puts it.
- 2026-11-11, the hot batch read from the simulator's own window (record.py carried params' build weeks): the golden
  cannot know a window the pack does not show, so the window is found from the record by a build-week scan of the last
  year's replacements against each vault's earlier level, with nothing flagged under a likelihood ratio of 25.
- 2026-11-11, batch frailty at gamma(12) (cv 0.29) with a single-window scan: one high-frailty build batch made only the
  late weeks of the window stand out (seed 9011 found weeks 25 to 30, and 16 to 32 once the vault levels were in), so
  batch frailty is gamma(30) (cv 0.18) and the scan takes each vault's own earlier level; seeds whose scan misses the
  true window were set aside.
- 2026-11-11, the infant term fitted on half-year age bands and applied to a drive's first weeks: the band-mid covariate
  inflated the term's coefficient to about 150 times at install and put the new X-24 vaults at three times a believable
  first-year rate; the first year is now fitted in monthly bands.
- 2026-11-11, Poisson or drive-level-draw bands as the careful pass's priced loss: frontier runs bootstrap and build
  predictive intervals unprompted (precedents R04), and with each vault's level in the golden the vault-quarter residuals
  carry no extra-Poisson spread, so the interval and the back-test are not priced on clustering; they stay as graded
  results the careful pass earns, and the band's width is graded with the path.
- 2026-11-11, the migrate call for the batch as a whole (migrate if the batch's 24-month share exceeds 20 per cent): every
  route that finds the batch at all lands on "migrate", so the call priced nothing; the call is made vault by vault, where
  a vault holding a third of the batch does not pay.
- 2026-11-11, seed 9014 for the per-vault call: its vault B17 sat at 236 against the 240 line, flipping under either ramp
  shape alone; seed 9017 is the world where every vault clears the line by 10 per cent or more under every rival.
- 2026-11-11, the build window a week wider as a golden-family rival: the week-15 builds fail at 1.2 per cent a year, under
  the family's normal 2 per cent, so the data rule the wider window out; it moves to the shortcuts (it migrates B15).
- 2026-11-11, the per-vault migration call as built on seed 9017 (stage 4 judge, NOT_DETERMINISTIC, SEND_BACK): the cost
  convention was open (the YAML's drive price and "new drives" licence break-evens of 130 and 678 beside the golden's 240),
  the prompt asked one call for "its vaults", the batch vaults' levels came from their few non-batch drives (B18 at 0.93
  against its record's 0.5, B16 at 0.84 against 1.56), and the batch's noisy quarterly rate (2.3, 3.9, 2.3, 6.1, 8.3, 7.8
  per cent) leaves a plateau reading that flips the call; the judge also found the build window at once, so R2 is not a
  loss a careful run makes, and with it earned the cited pair is near 58 to 65, over the bar.
