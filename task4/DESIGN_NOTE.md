# task4: which of Havørn Regional's rotables will be short of spares in 2027 and which over-stocked once the Helgeland routes start, and how many spares each part number should hold

## Draw

Subdomain: Regression, classification & model diagnostics (General Statistics & Data Science; house domain Supply Chain & Logistics, inventory and demand planning: a regional airline's rotable spares pool)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A flagged set with the evidence (each rotable part number's 2027 spares line diagnosed as short, over-stocked or right against what the pool holds, with its expected 2027 unscheduled removals and 80 per cent range, the spares it needs for the 95 per cent fill rate and what moves it; the watch-list serials worth scrapping and the 2027 removals scrapping the whole list would save)
Weight: triage: the work is deciding, part number by part number, which of several processes the October projection gets wrong for it (the exposure its removals follow, the aircraft-side faults behind the watch list's counts, a bulletin embodied through its own shop visits, the shared shop's turnaround) and carrying each into its spares, where the last three live builds weighed measurement (task8), validation (task20) and attribution (task9)
Data-native sentence: the maintenance system records each removal against a part's serial and an aircraft on a date, and the reliability report reads it per flight hour, while what sets next year's need sits in other records at other grains: the legs each aircraft flew (hours and landings, which moved together on every base's network and part company on the Helgeland short sectors), the shop's findings and dates per serial (which removals found nothing, which embodied the bulletin, how long each waited for the shop) and the weather each base had on each day.
People: Britt Berge (technical director, signs the 2027 rotable spares plan, its purchase orders and the watch-list scrapping), Sigurd Fredriksen (reliability engineer, author of the October reliability report and its watch list), Ruth Johannessen (rotables and stores controller, owner of the pool records), Sondre Edvardsen (Bodø component shop supervisor), Siri Johansen (planning analyst, whose workbook and slides the golden are) (`guard.py names --geo Norway --seed 1204`). None appears in the prompt.

Architecture 12, 2026-11-11, a new world after architecture 11 (Saarnela's peak plan) was landed on the platform (`runs/arch11/run1.md`): the run took the aisle congestion, the acquired brand's full mix and the 53-week re-key unprompted and lost only the forecaster's growth-conditioned overstatement, the one judgment that was a relation between two quantities no standard check probes. Architecture 12 builds every priced judgment in that form, where reading every file correctly still leaves the analysis wrong: an exposure the record's hours and landings never separated in aggregate; serials flagged by their own removal counts, which mostly measure the aircraft they flew on and chance (the same structure as a rollout count read as misconduct when it measures repair loops); a fix embodied through the population's own shop visits; one shop queue that every in-house line shares, which the summer holiday weeks narrow. The winter's cold snaps and each station's troubleshooting are carried in the golden too, but each sits inside every band as a golden-family member, so neither is priced. New decision form (each line of the spares plan diagnosed), new dataset, new shell (how-many | which | pptx+xlsx).
Guard (2026-11-11, registered card): WARN only. The decisive pattern was redrawn at the draw from G6 (composition shift, task20's) to G2 (grain mismatch: the rate's exposure unit), the honest label for a removal rate carried per flight hour where the part wears per landing or start. WARNs answered: overuse.forum (the 2027 rotable spares are capital spend the technical director signs at the management team's December budget meeting; no rarer forum is true), repeat.gate_g (forecasting against task20: a card-panel revenue figure there, removals by exposure through a shop queue here), and the house lessons inherited_attribute_from_other_unit and queue_or_capacity_replay (each one judgment beside two lessons no build on file teaches, exposure_basis_decoupled first). At the build the card's lessons dropped serial_or_common_shock_dependence and heterogeneity_carried_to_decision, which the golden carries but no band prices. At READY (2026-11-12) the post-pull heart run blocked the card's stump strategy and forum against task21 (registered before this card) once later re-registrations left the three-build window: both axes redrawn to what the build is, the strategy forecast_method_backtest (the 2027 regime makes the per-flight-hour fit and the 2026 turnaround wrong out of sample, the base mix's composition effect sitting inside every band; grain_or_unit and population_selection repeat task8 and task19) and the forum line_manager_or_team (the shipped standard has the technical director approve the plan in the department's own line, 6.1, and no meeting is in the pack); heart WARN only.

## Deep reasoning

Task type: Forecasting & Predictive Modeling on a model-diagnostic spine (Regression, classification & model diagnostics): event-rate regressions with an exposure offset chosen by likelihood, a two-group mixture on serial counts, a calibrated queue replay and a Monte Carlo pool replay, each checked against the record it was fitted on.
Domain test: every result is a regression or model-diagnostic object the field's analyst builds: a removal rate's exposure basis, which the record's collinear hours and landings hide in aggregate and the bases' sector lengths separate (2 dlogL 23.8, 17.5 and 18.2 for the starter-generator, brake and bleed valve); a count-selected watch list whose counts mostly measure the aircraft and chance, read through a mixture on each serial's own exposure; a queue whose service rate is calibrated to its own turnarounds before it carries a heavier year; the fill rate read off a replay rather than Palm's stationary formula.
Swap: put a hospital's nouns in (wards for bases, admissions for landings, nurses for technicians, readmitted patients for watch-list serials) and the call stops making sense: no hospital forecasts a ward's admissions per bed-hour against a programme that adds short stays, sends readmissions through a single repair shop with a holiday roster, or withdraws a patient for repeat visits; the exposure, the shop and the serial are the airline's own objects.
Where the weight sits: the triage of sixteen part numbers, each needing its own reading of which process the October report's per-flight-hour reading gets wrong for it (landings, the aircraft's faults, the bulletin, the shop), and the long build behind the in-house lines, where the right removals still miss unless they go through a shop replay calibrated on the shop's own work orders and roster.
Layer 1: the maintenance system re-sends a corrected change as a new row with -R1 and keeps the original; the reason codes changed from U/S/C to UNSCH/SCHED/CONV with the May 2024 upgrade; 2024's scanners prefixed serials with S/N; robbed units appear as a CONV removal and a later install-only fit; the flight-data feed re-sends whole days and loses the off and on times on some legs; the shop's finding code starts in March 2024 (text only before); the part numbers carry their dashes or not by source; each removes its own cleaning step and none decides a result.
Not one thing: the strongest single piece is the exposure (landings, not hours), and a run that nails it still loses the in-house spares (Palm on the 2026 turnaround with the landing-driven removals gives 6, 5 and 5 where the shop's 2027 queue needs 9, 9 and 7), the watch list (the counts at face value save 64, the confirmed failures alone 14, the golden 35), the recommendation's buys on the batteries and brakes, and the ranges.
One-fact test: the most useful sentence is "the starter-generators, brakes and bleed valves wear by landings and engine starts, which the 2027 programme raises while flight hours fall"; run on the careful pass it takes R2 most of the way (56, 50 and 47 against 59, 51 and 40) and rescues no other result: the in-house spares stay at 0 of 5 lines in band and the plan's lines at 9 of 15.
Not semantics: every field, unit and clause read correctly still leaves the hurried results wrong: the October report's MTBUR is defined per flight hour (standard 3.2) and computes correctly, the watch list is three removals in twelve months (3.3) and is the report's own, the turnaround is removal to serviceable stock (2.4) and the 2026 average is a true average; the errors are in carrying those true figures to 2027.
Not rule application: no filed procedure forecasts a removal, sizes a pool or reads a serial; the standard files the WHAT (the fill rate over the year's removals at the expected rate, the 80 per cent range with the rate's own uncertainty, the withdrawal test against a new unit, the saving counted for the position over the year) and leaves every method open.
Estimand: standard 4.1 to 4.4 fix the year (calendar 2027), the population (the units in service at 30 November 2026 under the issued programme), the fill rate (the share of the year's unscheduled removals with a serviceable unit in Bodø stores or a station kit), the outcome (unscheduled removals as 2.1 defines them, whatever the finding) and the range (10th to 90th percentile with the rate's uncertainty); 5.1 and 5.2 fix the withdrawal test and the saving's count; the prompt names the deliverables and asks each result in its unit.
No decoy: the October report gives each part's twelve-month MTBUR and the watch list, both computed exactly as the standard defines them (3.2 and 3.3), and no 2027 forecast (its 2027 outlook section was taken out at stage 4); the budget line replacing every listed serial is the incumbent's plan, and ask 5 prices it on the golden's footing (the whole list saves about 35 removals); nothing ships to carry a wrong answer.
No replay: no result re-derives a published figure; the report's twelve-month counts and MTBURs are inputs, and every graded figure is a 2027 quantity no file states.
Pinned: each result's rivals are run on the cut pack: the removals against the both-exposures fit, the no-frost fit, the stations pooled, the 2024 to 2026 window and the last twelve months on each part's own exposure; the spares against a second stream of replays, the no-fault-found months without their spread, every winter at its average frost, the shop calibrated on 2025 to 2026, the both-exposures and twelve-month removals and Palm's theorem on the repairers' lines; the saving against the raw serial rates; the ranges against a negative binomial; every band is their span (a unit either side on counts), and every hurried figure sits outside it (checks.py R3, SF12 to SF16).
Run forecast: R2 (dismissed own evidence: the per-flight-hour transfer named and left untested; the stage 4 judge's blind derivation found the landings driver by comparing the bases' rates, so R2 may fall to a careful run and is graded Partly in the careful column), R6 and R8 (method shortcut, then an unfinished chain: Palm on the 2026 average turnaround), R3 and R3b (dismissed own evidence and method shortcut: the no-fault-found removals set aside, the listed serials priced on population averages), R7 (method shortcut: monthly counts bootstrapped around the wrong centre) and R9 (unfinished chain).
Strategy label: own (exposure decoupling with a shared repair queue and a count-selected list), not a family on file in references/sulfur-strategies.md.
Depth level: 5, three independent judgments that each move a block of graded figures (the exposure for the landing-driven removals, the shop's queue for the in-house spares, the aircraft-driven and chance removals for the watch list) and a fourth on the bulletin, with four shortcuts landing on four different wrong plans (none, the careful pass's eleven lines, the landings-only route's fifteen, the average-turnaround route's thirteen).
Lesson: a rate is carried on the exposure its own record says drives it, a shared service's turnaround is replayed at next year's load before it sizes anything, and a list selected by its members' own counts measures their hosts and chance before it measures them; no build on file teaches the first.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R2 | the starter-generator, brake and bleed valve 2027 unscheduled removals: 59, 51, 40 | modeling | the aircraft-month panel from the legs and the register: landings beat hours and days (2 dlogL 23.8, 17.5, 18.2); the issued 2027 programme (4.1) | 55 to 66, 49 to 55, 38 to 48 | dismissed own evidence: carries the October per-flight-hour rate to 2027 (41, 36, 34) though the programme's own landings rise 19 per cent while hours fall 13, the transfer named and left untested | - | Component 1 |
| R3 | the watch-list serials worth withdrawing: 8 of 23 (ADC9270, C3880, FD7205, RT4534, SG6792, V210070, V2715, WH1688) | investigation | standard 5.1; the changes at the aircraft-position grain (runs of serviceable removals by two or more serials); each serial's own installed exposure | exact (the mixture and the raw rates file the same 8) | dismissed own evidence: sets the no-fault-found removals aside as noise and withdraws on confirmed failures alone (4 serials, one of them a short run its own record does not repeat, the five intermittent rogues kept) | - | Component 3 |
| R3b | the removals withdrawing the whole list saves in 2027: about 35 | decomposition and attribution | standard 5.2 (counted for the position over the year); the serials' own rates with the aircraft-driven removals set aside | 33 to 47 | method shortcut: prices the listed serials on the part's population average, the counts' excess at face value (64) or the confirmed failures alone (14) | independent: the changes and the findings | Ask 3 |
| R4 | the propeller control's 2027 removals and spares: 19 and 5 | forecasting | the repairers' SB 61-0042 returns, the snapshot's bulletin column, each serial's installed spells | 17 to 21 removals; 5 spares | method shortcut (the quick pass): pools the modified and unmodified cohorts at the twelve months' rate (14); the careful pass splits them and is right | - | Component 4 |
| R5 | every part number's expected 2027 unscheduled removals, sixteen lines | forecasting | each part's driver by likelihood; the programme; each station's no-fault-found rate | the rivals' span per line, a removal either side | method shortcut: one exposure for every part, the twelve months per flight hour, right on the flight-hour parts and wrong on every landing-driven one | - | Ask 1 |
| R6 | the in-house lines' spares through the Bodø shop's 2027 queue: 9, 9, 7, 4, 5 | modeling | the roster and the work orders; the replay calibrated to the shop's own 2024 to 2026 turnarounds; standard 4.3 | 9 to 11, 9 to 10, 7 to 8, 4, 5 to 6 | method shortcut: Palm's formula on the 2026 average turnaround, each line priced alone where the shop nets it against the other lines' load in the holiday weeks (5, 4, 4, 2, 3) | R2 | Component 2 |
| R7 | the 80 per cent ranges, sixteen lines | uncertainty | standard 4.4 (both the year's chance and the rate's own uncertainty) | the golden family's and the negative binomial's span, a removal either side | method shortcut: the twelve months' counts bootstrapped month by month around the per-flight-hour outlook, independent months where the cold snaps and the aircraft's faults share shocks | R5 | Ask 1 |
| R8 | the spares each line needs for the 95 per cent fill rate, sixteen lines | synthesis | standard 4.2 and 4.3, the replay's fill curve per line | the golden family's span per line | unfinished chain: right on the flight-hour repairers' lines, then Palm on the average turnaround carried to every in-house line | R5, R6 | Ask 2 |
| R9 | the lines to buy and to cut with how many: buy 16 on 6 lines, cut 18 on 9 | synthesis | the lines every golden-family method moves the same way | the family's span per line | unfinished chain: cuts the avionics right and holds or cuts the landing-driven and in-house pools | R8 | Recommendation |

Carry-forward: R2, R3, R3b, R4 and R5 are graded on the shipped files alone; R7 is graded against the golden's centre, so a run with the wrong removals loses its ranges too; R6 and R8 need both the removals and the shop, and a run with the right removals that skips the queue still loses the in-house lines; R9 falls with R8; R3b is graded on the whole list whatever a run decides in R3.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| landing- and start-driven wear | constructed (the world's physics, per landing or start) | no: six part numbers wear by landings or starts, three priced, and every base flies it | modelling: a panel fit of each part's confirmed failures on landings, hours and days across bases with different sector lengths | modelling (a driver chosen by likelihood, carried on the programme's landings) | keep |
| aircraft-side intermittent faults and station swaps | constructed (the stations' troubleshooting process) | no: 54 faults on 25 aircraft across seven part numbers, in the removal counts of every listed and unlisted serial | investigation: runs of serviceable removals from one aircraft position by two or more serials | modelling (the runs and their windows set aside before each serial's own rate) | keep |
| rogue serials, confirmed and intermittent | constructed (a share of each pooled part number) | no: eight listed and six unlisted across seven part numbers | modelling: a two-group mixture on each serial's own removals and exposure | modelling | keep |
| SB 61-0042 embodied at shop visits | constructed (the repairer's process) | no: every propeller control removed since October 2024, in the repairers' orders and the snapshot | a targeted query on the repairers' returns, then each serial's spells | modelling (the conversion rolled through 2027) | keep |
| the Bodø shop's queue and staggered summer holidays | constructed (the shop's roster and work) | no: all five in-house lines, every month of the record | modelling: a day-by-day replay calibrated to the shop's own turnarounds | modelling | keep |
| cold snaps and each station's swap practice | constructed (the weather and the stations) | no: every base and every cold-sensitive or intermittent part | a targeted query (frost terms, station rates) | modelling inside the golden, and inside every band as golden-family members | keep, unpriced |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R2 the landing-driven parts' 2027 unscheduled removals | Missed | Partly | Right |
| R3 the watch-list serials worth withdrawing | Missed | Missed | Right |
| R3b the removals withdrawing the whole watch list saves | Missed | Missed | Right |
| R4 the propeller control's 2027 removals and spares | Missed | Right | Right |
| R5 every part number's expected 2027 unscheduled removals | Partly | Partly | Right |
| R6 the in-house lines' spares through the Bodø shop's 2027 queue | Missed | Missed | Right |
| R7 the 80 per cent ranges | Partly | Partly | Right |
| R8 the spares each line needs | Missed | Partly | Right |
| R9 the lines to buy and to cut, with how many | Missed | Partly | Right |
| Roughly | 1 of 9 | 3.5 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (each pass computed end to end in generator/analysis.py and generator/effort_passes.py on the cut pack)
Largest single hint: the starter-generators, brakes and bleed valves wear by landings and engine starts, which the 2027 programme raises while flight hours fall; rescues 1 of 9 results (R2), and on the careful pass leaves the in-house spares at 0 of 5 lines in band
Pair estimate: 43.6 (quick 20.8, thorough 100; R2 hand-graded Partly in the careful column after the stage 4 judge found the landings driver blind)

## Data provenance

Source: generated by the seeded generator in task4/generator, which simulates the airline day by day from January 2023 to the snapshot and then 2027 itself: the fleet's rotations on each base's network, the weather at each base, each installed unit's wear on its own exposure, the aircraft's own intermittent faults and the stations' troubleshooting, the Bodø shop's queue on its roster, the repairers' turnarounds and the pool.
Behaves like the real thing: removals follow each part's physics (Weibull wear on landings, starts, hours or calendar time, faster in the cold), outstations swap units to troubleshoot what Bodø finds, rogue units cycle between wing and shop, a service bulletin reaches the fleet one shop visit at a time, a three-technician shop with third-party work queues in the holiday weeks, and the reliability report computes MTBUR and the watch list exactly as the standard defines them; the clean truth replayed for 2027 puts the starter-generator's removals within 6 per cent of the golden's and a third above the per-flight-hour outlook (checks.py T5 and T6).
Genuine patterns: (1) the flying's seasonality, weekday pattern and winter block-time stretch; (2) each base's network and sector length, from Trondheim's 63 minutes a landing to Bodø's 17; (3) cold snaps that reach the northern bases together; (4) overdispersed no-fault-found removals from faults that persist until a station finds them; (5) a shop queue that builds in the staggered summer holidays and at Christmas; (6) a bulletin's conversion through the population's own removals; (7) the heavy checks' downtime and robbery between aircraft.
Problems by process: the corrected changes re-sent with -R1 beside their originals (the maintenance system's correction workflow); U/S/C codes before the May 2024 upgrade and UNSCH/SCHED/CONV after; the S/N prefix from 2024's handheld scanners; the flight-data feed's re-sent days and lost off/on times; the shop's finding code added in March 2024; part numbers with and without dashes by source system; install-only rows where a robbed or awaited unit was fitted later.
Breadth: thirteen files (two distractors), 239,844 legs on 30 aircraft over four bases, 1,600-odd component changes on sixteen part numbers and 950 pooled serials, three shops and repairers, four winters of daily weather; each part number needs its own driver, findings mix and turnaround, so choosing what to look at is the triage.

## Template check

Chain signature: modeling, investigation, decomposition and attribution, forecasting, forecasting, modeling, uncertainty, synthesis, synthesis
Question form: which and how many (which part numbers will be short, which over-stocked, how many spares each should hold), with the watch list's saving and its withdrawals asked beside the plan
Nearest build: task20 architecture 1 (spent; a per-unit diagnosis of a card portfolio's revenue under a composition shift), severity none on skeleton.py: another decision field, another dataset, other lessons; task21 (a pricing dial) shares only selection on noisy means

## Frontier check

Precedents: R2 N04 and N01 (a model's transfer to a new range named and left untested; an enlarged programme assumed to scale in proportion), R3 L03 and L13 (a second log at another grain set aside; population rates applied to a subset selected by its own counts), R3b L14 (selected survivors priced on population tables), R5 L12 and L36 (pooled cohorts whose rates drift; a transfer fitted on one range carried to faster duties), R6 L15 and L16 (a response assumed instead of measured; the unit priced alone where the system nets it), R7 L35 (an independence count where units share shocks), R8 and R9 L11 (the split built for the first step and dropped for the next); the same ids sit on each result in generator/effort.json, and R4 is Right in the careful column
Shallow path checks: the per-flight-hour outlook passes its own back-test (each year's count from the year before's MTBUR lands within noise, because hours and landings moved together on every base's network in the record) and reproduces the October report exactly; the check of another kind that refutes it is the aircraft-month panel across bases from flight_legs_2023-01_2026-11.csv and fleet_register.xlsx, where landings beat hours by 2 dlogL 23.8 to 18.2. Palm on the 2026 average turnaround passes 2026's own fill; the replay at 2027's load from bodo_shop_roster_2023-2026.csv and bodo_shop_work_orders_2023-2026.csv refutes it (about 29 days in July and August against 13). The confirmed-failure watch list passes the check that its serials carry the most confirmed failures; the runs of serviceable removals on one aircraft position in component_changes_2023-01_2026-11.csv refute it.
Assumption made false: that removals scale with flight hours (the report's own outlook) and that the shop's turnaround stays at 2026's: the world's 2027 programme puts eight aircraft on quarter-hour Helgeland sectors, so landings rise 19 per cent while hours fall 13, and the extra landing-driven removals reach a three-technician shop in the weeks its roster runs on two; the legs file by base and the shop's roster test both. And that a serial's removal count measures the serial: the outstations swap units to find an aircraft's intermittent fault, and the changes at the aircraft-position grain test it.
Forcing: the call is a set of 6 buys and 9 cuts; all seven golden-family members (a second stream of replays, the no-fault-found months without their spread, every winter at its average frost, the shop calibrated on 2025 to 2026 alone, the both-exposures removals, the last twelve months' removals, Palm's theorem on the repairers' lines) file the same lines; the four shortcuts file four other sets (none; the careful pass's eleven lines with a brake cut and no starter-generator, bleed valve or battery buy; the landings-only route's fifteen with a flap actuator buy and no brake buy; the average-turnaround route's thirteen without the brake and battery buys); each fitted input moved by its spread (the three priced rates 20 per cent down, the shop's capacity 5 per cent either way, the propeller control's rate, the frost terms and every no-fault-found rate 20 per cent up) holds the call, the nearest lines being the one-unit changes, which every member moves the same way
Noun swap: the nearest on file by skeleton.py check is task20 architecture 1 (spent, severity none): with its nouns swapped in, only the decision form (each unit diagnosed) carries across; the lessons (an exposure decoupled by the forward plan, a count that measures its host, a shared queue), the detection, the moves and the file roles do not; against the client's library the nearest is also severity none

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | unscheduled removal | every UNSCH (U) removal whatever the finding / confirmed failures only | every UNSCH removal | standard 2.1 (whatever the shop or repairer later finds); checks.py SF1 |
| SF2 | in 2027 | calendar 2027 / the twelve months from the snapshot | calendar 2027 | standard 4.1 (the coming calendar year); checks.py SF2 |
| SF3 | the 95 per cent fill rate | share of the year's removals with a unit held / the chance a unit is held on a random day | the share of removals | standard 4.2 and 4.3; the replay reads it over the year's removals; checks.py SF3 |
| SF4 | the pool and its spares | every unit beyond those installed / serviceable units only | every unit beyond those installed | standard 2.3 (serviceable, unserviceable and on order); checks.py SF4 |
| SF5 | the 80 per cent range | chance and the rate's uncertainty / chance only | both | standard 4.4; checks.py SF5 |
| SF6 | the units the plan is for | the units in service at 30 November 2026 / net of the recommended withdrawals | the units in service | standard 4.1; checks.py SF6 |
| SF7 | the 2027 flying | the issued 2027 programme / 2026's flying | the issued programme | standard 4.1; checks.py SF7 |
| SF8 | a new unit's removals | the healthy serials' rate / the part's average serial | the healthy serials' rate | standard 5.1 compares with a new unit; the mixture's healthy group sits below every listed part's pooled rate; checks.py SF8 |
| SF9 | the removals a withdrawal saves | for the position over the year / per installed year | for the position over the year | standard 5.2; checks.py SF9 |
| SF10 | the October watch list | the report's 23 serials / a list recomputed another way | the report's | the report section 4 and standard 3.3; checks.py SF10 |
| SF11 | the change against the pool | spares needed less the pool / less serviceable stock | less the pool | standard 2.3; checks.py SF11 |
| SF12 | short of spares, over-stocked | every defensible method moves the line the same way / the golden's arithmetic alone | the robust lines | same call: every golden-family member files the same lines; checks.py SF12 |
| SF13 | the exposure a rate is carried on (HOW) | landings / flight hours / calendar days | each part's best by likelihood | the record: 2 dlogL 23.8, 17.5, 18.2; checks.py SF13 |
| SF14 | the window the rates are fitted on (HOW) | 2023 to 2026 / 2024 to 2026 / the last twelve months | 2023 to 2026 | same call: all three inside every band; checks.py SF14 |
| SF15 | taxi time at the Helgeland fields the record has not flown | the quieter fields' times / 3 to 8 minutes | the 25th percentile of the record's fields | same call: 2027's flight hours move under 1.5 per cent; checks.py SF15 |
| SF16 | the shop's 2027 staffing and capacity (HOW) | the roster's holidays a year earlier with the calibrated capacity / capacity 5 per cent either side | the roster and the calibration | same call; checks.py SF16 |
| SF17 | flight hours | air time, off to on / block time, out to in | air time, the programme's block minutes less each field's usual taxi | the October report's 28,810 flight hours reproduce on air time and not on block time (about 43,700); checks.py SF17 |
| SF18 | a serial's expected rate (HOW) | two groups of serials by mixture / its own raw rate / one gamma shrinkage toward the part's rate | two groups | the serials' own counts reject the one-gamma model on every listed part with a second group (2 dlogL 9.3 to 34.3, about 160 pooled); the raw rates file the same eight; checks.py SF18 |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the sixteen pooled part numbers and every unit in service at 30 November 2026 (4.1), the listed serials kept in service for the plan |
| 2 | Unit of account: the part number's line for the spares; the serial for the watch list; the position for the saving (5.2) |
| 3 | Attribution window: a removal belongs to its change date; a fill to the removal's date (4.2) |
| 4 | As-of dating: the exports of 1 December 2026, the snapshot of 30 November 2026, the report to 31 October 2026 |
| 5 | Version basis: a corrected change (-R1) replaces its original; one export of each file |
| 6 | Denominator: removals over each part's own driving exposure, per position; the fill rate over the year's removals (4.2) |
| 7 | Weighting: the fill rate counts every removal once; the forecast sums station-months |
| 8 | Window length: the fitting record January 2023 to October 2026; the plan year 2027 |
| 9 | Boundary inclusivity: the report's twelve months 1 November 2025 to 31 October 2026 inclusive; 2027 from 1 January to 31 December |
| 10 | Rounding path: removals at full precision, rounded once to whole removals; spares whole units from the fill curve; per cent to whole points |
| 11 | Tie-break: a removal matched to the first shop or repairer order for its serial within ten days |
| 12 | Maturity and censoring: units still in the shop at the snapshot start the replay in the pipeline; the last month's removals with no finding yet are counted as removals |
| 13 | Order of operations: clean, match findings, fit, carry to 2027, replay the shop, replay the pools, then set against the pool |
| 14 | Row order: no step depends on file order; every event dated |
| 15 | Duplicate resolution: the feed's re-sent legs are exact copies, kept once |
| 16 | Identity normalisation: serials upper-cased with the S/N prefix stripped; part numbers matched with or without their dashes |
| 17 | Netting against gross: buys and cuts are separate lines; nothing nets across part numbers |
| 18 | Dimensional units: removals a year; spares in units; turnarounds in days; exposures in landings, flight hours or days per position |
| 19 | Code and status semantics: U and UNSCH, S and SCHED, C and CONV one each (2.1); the shop's CONF, NFF and BER codes or the text before March 2024 |
| 20 | Integerisation: counts and spares whole |
| 21 | Clause scope: 4.2 to 4.4 apply to every part number alike; 5.1 and 5.2 to every listed serial |
| 22 | Forward window contents: the issued programme, the snapshot and the record to 30 November 2026 drive 2027; nothing else is needed |

## Literal reader

Executed word for word: the prompt asks every part number's expected 2027 unscheduled removals with an 80 per cent range, the spares for the 95 per cent fill rate and the change against the pool, the parts to buy and to cut with what moves each, the 2027 removals scrapping every October watch-list serial would save and which of them to scrap; standard 2.1 fixes the removals counted, 2.3 the pool, 4.1 the year, the units and the programme, 4.2 and 4.3 the fill rate at the expected rate, 4.4 the range, 5.1 the withdrawal test against a new unit and 5.2 the saving's count; read literally they give the golden's estimands, and every method stays open (SF1 to SF16).

## Prompt contract

A voice rewrite keeps: the question (which part numbers will be short of spares in 2027, which over-stocked, how many spares each should hold); the reason the plan rests on estimates (the Helgeland routes from April, so 2027's flying is not this year's); every part number's expected unscheduled removals in 2027 with an 80 per cent range; the spares for the 95 per cent fill rate and the change against what the pool holds today; the parts to buy and to cut with what moves each; the 2027 removals scrapping every serial on the October watch list would save; which of those serials to scrap; a spreadsheet and a few slides. It never adds a rounding instruction, a method (per landing, Palm, a queue, a mixture, shrinkage), a warning, an attached file's name, a role or a count the data hold.

## Leak rulings

Ruled in the main thread on `leak.py --asof 2026-11-30` (verdict REVIEW, no LEAK), 2026-11-12, on the stage 3 cut (target.zip 183ee655a14c4f36):
- answer figures: every figure the sweep took from the answer blocks was a part number's digit group or the bulletin's number (23085, 3214552, 61-0042 and the rest), identifiers every file carries; declared under `stated_inputs` in `metadata.json`. Harmless.
- author vocabulary, the report and the pool offer: "generator" inside "Starter-generator", the part's own name, declared under `field_terms`. Harmless.
- design-note vocabulary, the standard (9 terms), the report (5) and the pool offer (3): ordinary words of a reliability programme (removal, aircraft, station, standard, record). The standard files the WHAT (what a removal is, the pool, the fill rate, the range, the withdrawal test) and the report its own MTBUR and watch list; neither names an exposure, a queue, a fault run or a serial's own rate. Harmless.
- dates after the setting: the fleet register's planned heavy checks and the 2027 flying programme, both plans a planning department holds for the coming year and the plan's own inputs. Harmless.
- the stage 4 reader's question 2 and 4: the October report's section 3, "2027 removals at October's MTBUR", read as a ready-made forecast of an asked figure. Fixed: the section is out of the report (the difficulty survives the deletion, since every careful run computes the same projection from section 2's MTBUR); the budget line in the watch-list section stays as the incumbent's plan that ask 5 prices.

## Tried and rejected

- 2026-11-11, architecture 11 stage 4, the site manager's staffing sheet with its rate checked on 30 random days of 2025: the off-peak days' paid hours carry the packing moves and the check read as a defect rather than as the sheet's own check; it now checks the 2025 rate on the 2025 peak's own days, the check its author would run.
- 2026-11-11, architecture 11 stage 4, the overstatement (ask 4) measured against the lines picked in the peak weeks, as the prompt's "the lines we went on to pick" read: the judge found two readings, and the measured spread was wide (14.8 against the lines picked, 11.2 on the orders released by the standard's rule, 10.0 on the orders placed, because the dense peaks' backlog spills into week 51); the ask now reads "the order lines it placed in those weeks", the budget's own quantity, and the calibration moved to the same basis (leave-one-out 0.026 against 0.056 for a constant).
- 2026-11-11, architecture 11 stage 4 preparation, a mixed calendar alignment (November's days moved by weekday, December's by date) as a profile rival: it leaves 29 and 30 November 2027 without any source day, so week 48 loses Cyber Monday's orders (26 per cent of its hours); it is no profile and is ruled out in the note's Pinned line, while the same-weekday move's two-day offset of the Christmas bell moves weeks 49 and 50 by under 5 per cent.
- 2026-11-11, architecture 11 stage 3, the client's 2027 plan for Kotikaari small parts at +33 per cent (the marketplace launch): the calibrated overstatement then took out more lines than the pooled share, against the congestion and the full Huippu mix, so the careful route landed near the golden's evening weeks and the calendar alone recovered them; the 2027 plan is +7 per cent, the lowest on record, so the pooled share over-corrects and every correction moves the hours the same way.
- 2026-11-11, architecture 11 stage 3, the peak as ISO weeks 46 to 51: week 51 of 2027 (20 to 26 December) holds the Christmas closures, and moving 2025's days onto 2027's by weekday put 2025's closed 24 to 26 December onto 2027's open 22 and 23 December, so every profile construction disagreed on that week by tens of per cent; the standard's peak is weeks 46 to 50.
- 2026-11-11, architecture 11 stage 3, the web orders released partly the same day (before noon) and partly the next: the profile then depended on a split no file states; the standard's release is the next working day (2.4), visible in the picks.
- 2026-11-11, architecture 11 stage 3, the 2022 to 2025 budgets planned +16, +8, +27 and +12 per cent for small parts: the eight budget-years' overstatements did not rise with the plan clearly enough (leave-one-out 0.042 against 0.039 for each group's mean), so the calibration was not pinned; the plans spread to +25, +4, +30 and +10 with less noise in realised growth, leave-one-out 0.033 against 0.054.
- 2026-11-11, architecture 11 stage 3, P2 at 10 aisles and a limit of 20: P2's ratios ran eight per cent above P1's in every week, so no single volume level kept both zones' week 46 and week 47 clear of the line; P2 has 11 aisles and a limit of 22.
- 2026-11-11, architecture 10 (the Niittylä order, landed by both platform runs, `runs/arch10/`): every graded figure inside its band on both runs (order 17 exact); the diesel bridge was the obvious join once the prompt asked each block's diesel figure beside its energy, the heater-out days were read as the record of all-electric heating, and the charging split was one regression on the sessions. The world and its scaffold (a count of vehicles for duties under an energy limit and a night supply, architectures 5 to 10) are left together.

- 2026-11-10, architecture 10 stage 4, the first judge pass (FIX_NOW): a rank list in component 1 that depended on
  which blocks count as short (out of the blocks; the component states the means and the gap); the 19th block's kWh
  shortfall, whose magnitude depended on the plug-in margins assumed (out of the blocks; the windows are now the
  standard's words, each block's return to its departure inside the night period, the supply rescanned for
  balanced margins under them); M111 within the 10 kWh grading tolerance of the limit (every block now 26 kWh clear in
  the truth and 18 in the golden). The reader's figure 20 (outlets, the quotation's range) moved apart (26 outlets, four to thirty buses).
- 2026-11-10, architecture 10 stage 4, the second judge pass (DETERMINISTIC, one item owed): the heaters' band edges
  propagated to the cut, now asserted (SF27, both bands' edges land the same 18 and the same verdicts, the band half a
  kW either side of the golden); the re-read's realism line (a session starting under zero state of charge): the
  pilot's blocks, stand-ins and weekend blocks now pass the planner's own range check (the pilot buses' 480 kWh as the
  quoted model's), the boosters on a heater-out day capped at 12 kW, no electric day ends under 15 per cent; the
  stand-ins are the next three on the planner's list, so the pilot's record reaches no hard block; the heater fit
  leaves the heater-out days' hours out of its intervals.
- 2026-11-10, architecture 10 stage 3, the night's energy for the recommended buses as ask 5: every route capped by the
  night lands near the capacity's energy (the careful pass's 21 lighter buses sum to the golden's 18), so the figure
  graded nothing; replaced by the night demand of every qualifying block (8.7 MWh against 13.0 on the careful pass).
- 2026-11-10, architecture 10 stage 3, the telematics days uploaded twice in March 2026 (cold days): kept, they halve
  the heater fit's slope through the degree-days without litres and move every energy 7 to 11 kWh; the portal's outage
  moved to May, where the duplicates touch nothing (SF6 asserted within 8 kWh).
- 2026-11-10, architecture 10 stage 3, electric stand-ins on any short weekday block: 37 stand-in days spread over 30
  blocks gave almost every qualifying block its own electric days and the hurried fit nothing to miss; the dispatcher
  now keeps three approved stand-in blocks, so the bridge reaches the hard blocks through them and the weekend blocks
  while the pilot's covariate fit stays light on the 39 blocks it never ran.
- 2026-11-10, architecture 10 stage 3, the pilot's energy model with a per-hour auxiliary term beside block effects:
  kilometres and hours are collinear within a block, the term was unidentified (15.7 kW against 2.2) and every block
  effect biased; the per-km rate by block now carries the auxiliaries, and the diesel rate carries the idle draw the
  same way, so the bridge is one line.
- 2026-11-10, architecture 10 stage 3, charging allowed from the bus's return: the night's windows summed to 17 hours
  and no realistic supply bound the order; the connection agreement's night period (21:00 to 07:00, the load-control
  relay) is the operating arrangement, and the supply scanned at 5 kW steps for balanced margins (700 kW under the exact windows: the 18 hold
  3 per cent up, the 19th fits only 2 per cent down, 10 or 20 minute plug-in margins cut at the same 18, and the heaters'
  band edges leave the 18).
- 2026-11-10, architecture 10 stage 3, the pilot blocks as the thriftiest of all 48: the planner also needs the range,
  so the pick was from the blocks of 225 km or less, and the pilot sits at ranks 11 to 23 of the 48; the component
  states the gap and the ranks among the short blocks as computed.
- 2026-11-10, architecture 10 stage 2, the cold-day selection (the planner keeping the electric buses in on the
  coldest days) as the heating judgment: with fuel heaters the pilot has no range problem on cold days, and a handful
  of cold days the forecast missed would be outliers one residual plot shows; replaced by the heaters' share, which
  sits on every winter day and in a file the runs dismiss.
- 2026-11-10, architecture 10 stage 2, a 2027 timetable that re-cuts the blocks (line-level difficulty decomposed from
  the 2026 blocks): a second attribution the task did not need and a re-keying a solver would read as a trap; the 2027
  blocks are the 2026 autumn timetable's.
- 2026-11-10, architecture 9 (the calibration's transfer to the pilot's part loads, the early-life loss, the winter
  speed, in the Fryele world): both platform runs landed the golden exactly (`runs/arch9/`): run 1 by per-shipper
  calibration carried to each duty's own declarations, a square-root age form and a separate winter driving-time
  model; run 2 by the same with a declaration regime split found from the error itself. Each estimate the design
  priced as a step the runs had named and not taken was a mechanism one file's plot or one join carried. The world is
  left after five architectures; the lesson (what beats these runs is evidence in a file they dismiss, a structure
  across files nothing names, a count over many units, and selection into the training record) is this
  architecture's design.

- 2026-11-10, stage 4 re-judge, a stronger early-life loss so the straight-line loss flips a duty on its own (early
  loss 4.0 to 5.0 per cent over 0.18 to 0.30 years): the limit gap reached only 11.7 to 12.5 kWh against margins of
  10 or more, the curved forms spread 4.2 to 7.0 per cent, and the change would move graded figures after the one
  re-judge; not built. The -5 C speed ratio left the graded components instead (the re-judge thread put it within a
  careful run's reach), every figure unmoved.

- 2026-11-10, stage 4, the combination's tare and the drops as a graded component (R4 at first): the judge flagged it
  as earned by reflex and its isolated thread put a careful pass at 50 to 62 per cent on a grid that counted it
  twice; cut from the graded chain (kept in the model and the workbook), the verdicts' partial credit raised to
  three quarters of the duties; the careful pass 26.8 to 20.8, its design-day-speed variant 46.5 to 42.5.

- 2026-11-10, architecture 8 (three register joins beside the winter speed: the combination's tare by trailer, a
  multi-drop load taken off at its stops, ePTO fridge units drawing by the hour): both platform runs landed the golden
  exactly (order 7; payload 2.24 and 2.23, loss 3.78 and 3.79, every energy within about 3 kWh; `runs/arch8/`). Each
  join was to a register the runs already read, the new export, sheet and quotation line announced the steps, and the
  hourly fridge term made both runs time the design day, which is the winter speed. The judge's warning that the
  careful pass would earn 4 to 5 of 8 was recorded as a caveat instead of a blocker. Re-rooted as architecture 9: the
  fridge draw removed, the work moved into what the runs named and did not test.
- 2026-11-10, stage 2, the declaration practice differing by depot for the same shipper, read from an axle-load or
  gross-weight column in the daily summary: the summary carries no such column, and adding one would be a column that
  exists for the step; replaced by the pilot's part loads, which the pack already shows through each duty's own notes.
- 2026-11-10, stage 2, a battery-management or SOC-window update partway through, tractor by tractor: a timing break
  one residual plot per tractor shows and one indicator fixes (the client's shallow hidden factor, and this note's own
  earlier rejection of a drive-software update); replaced by the early-life loss, a form chosen by fit across every
  tractor.
- 2026-11-10, stage 2, the trailer body's air drag as the between-duty confounder of the payload slope (dense loads on
  low bodies): the tipper and the inloader have no pilot twin, so their drag would be a fork, and a flatbed's drag
  against a box is not physically one-signed; dropped.
- 2026-11-10, stage 2 pricing, the pilot duties at 80 to 93 per cent of the terminal's loads with drag 0.060: the
  careful pass's light-duty flips cleared its own limit by under 2 kWh; at 74 to 90 per cent, drag 0.066 and the
  winter fall 0.0125 a degree they clear it by 5 kWh or more.

- 2026-11-09, architecture 7 (the speed transfer as the deciding step beside the three reflex steps): both platform runs
  (`runs/arch7/run1.md`, `run2.md`, summaries) earned the payload term (1.98, 1.97), the loss (3.75), the cold curve and
  12 of 14 energies, fitted squared routing-tool speed (the year's ratio absorbed) and ordered 5, V14 out at 444.4 and
  443.0 kWh against the 442 kWh limit (golden 435.4). One duty, one judgment, 1 to 3 kWh: a thin level 3, and the
  graded 10 kWh band held both verdicts on V14; run 2 offered the golden's answer as a defensible alternative. Re-rooted
  as architecture 8: three more covariates the pilot's own rows do not show (the combination's tare by trailer, the
  tonne-km of a multi-drop load, the ePTO fridge units), each flipping two duties of its own, and no duty within 13 kWh.
- 2026-11-09, stage 2 pricing, the trailer pools one kind per pilot duty: the tare term (1.6) and the payload term (2.4)
  were confounded between duties and one shared coefficient gave 2.0, a 0.4 spread on R1; mixed pools (a mega on a box
  duty, a forklift on half the building-materials flatbeds) identify the tare within duty and bring the spread to 0.2.
- 2026-11-09, stage 2 pricing, the fridge unit at 3.4 kW: "every reefer draws" moved V33 13 kWh, no flip at a 13 kWh
  margin; at 4.4 kW it flips V30 and V33 clear of the limit.
- 2026-11-09, stage 2 pricing, V11 with two drops (0.56 at 44 per cent of the run): carried to the last drop it moved only
  9 kWh; three drops with a first stop at a fifth of the run move it 18.
- 2026-11-09, stage 2 pricing, the winter ratio at 0.0100 a degree and drag 0.046: the year's ratio moved every energy
  11 to 13 kWh and flipped nothing at a 13 kWh margin; at 0.0120 and 0.054 it moves 12 to 20 and flips V03, V11, V33.
- 2026-11-09, stage 2, a payload elevation term (the loaded leg's net descent): within-duty payload spread times a fixed
  elevation is under 1 kWh against 7 kWh of trip noise, so the term is set by physics constants (an efficiency and a
  regeneration share) the pack cannot pin: a fork, dropped.
- 2026-11-09, stage 2, a 2027 annual electricity figure over a normal year (the convexity of the cold curve): the gap
  between the year's energy at the mean temperature and over the ten-year distribution is about 2.5 per cent, inside the
  honest family's spread; dropped.

- 2026-11-09, architecture 6 (three estimates each moving the order: the payload term under declaration error, the
  sub-zero cold curve, the first-year battery loss net of the cold): the platform's run 1 landed the call and every
  graded figure (13 of 14 energies in their bin, 2.0 and 3.8 exact). It corrected the declarations by their measured
  error variance, kept a temperature quadratic on its fit, and regressed energy per full charge on age, temperature
  and tractor: each step a reflex for a frontier run once the asks named the quantity. Its own assumptions list named
  the gap it left untested: "Energy scales linearly with route distance ... the new round trips are 266-355 km,
  compared with 202-241 km for the pilot routes, so this remains a transfer assumption." Architecture 7 keeps the
  three steps in the chain and puts the deciding work in that transfer.
- 2026-11-09, stage 2, a second scenario (the order on a -10 C or -8 C day) as a further graded result: duties sit
  within 1 kWh of the limit across the honest rivals at both temperatures; dropped.
- 2026-11-09, stage 2, the drag coefficient at 0.032: leaving speed out moved every energy only 6 to 15 kWh, so half
  stayed within the graded 10 kWh and the careful pass priced at 58.5; at 0.046 (air drag about a sixth of the draw
  at 70 km/h) the shift is 9 to 21 kWh.
- 2026-11-09, stage 2, a drive-software update logged in the workshop file as the second judgment (the pilot's
  efficiency stepping down at each tractor's own update date): a timing break built into the data, found by one
  residual plot and fixed by one indicator, the client's shallow hidden factor; not built.

- 2026-11-09, stage 4, the dairy and the pallet maker writing one standard full-load weight on every note (13,500 kg
  on all 389 of the dairy's pilot notes): the determinism judge read a column with no spread at all as an authored
  device; both now declare the load plan's pallets at a standard weight each (540 and 360 kg), the pallet count on
  the note agreeing, and the per-shipper calibration carries them like any other.
- 2026-11-09, architecture 5 (one deep step: the declared payloads' dilution, with the cold form and every other step
  never moving a duty): returned by the portal, version 13, reward 68.5, not stumped. The review: the decision rests on
  one recognition, Tabergs Trävaror's exact declarations confirm the corrected term for free (2.19 against 2.20), and
  under calibration V03, V07 and V11 stay over the limit under every cold form. Rebuilt in the same world on the
  client's instruction as a results chain in which three estimates each move the order.
- 2026-11-09, stage 2 pricing, the drinks maker's scale from November 2025 or June 2026: its scale-weight pilot days
  alone (340 or 128) pinned the payload term at 2.03 with a standard error of 0.33, a second free check; from 17
  August 2026 they are about 60 and give 2.2 with a standard error of 0.52, a band from 1.2 to 3.2 that does not tell 2.0 from the declared fit's 1.2.
- 2026-11-09, stage 2 pricing, Forsheda Gummi in place of Tabergs: the pilot shippers' mean loads spanned only 10.8 to
  13.6 t, so the payload term was confounded with the duties' own route effects (2.5 to 2.7 on the true payloads
  against 2.15); the glassworks at 21 t widens the span and the route effect is halved.
- 2026-11-09, stage 2 pricing, the sub-zero curve at 0.0175 kWh per km per degree: one cold rate shifted every energy
  about 8.5 kWh, leaving no room between the one-rate route's margin and the golden's on V03; at 0.024 the shift is
  about 12.5 kWh.
- 2026-11-09, stage 2, a cold figure of its own (the design day's extra energy per 100 km over a mild day): one rate
  and the curved forms agree on it within the honest family's spread, because the one-rate fit lowers its base
  instead; the cold form is graded through the fourteen energies.
- 2026-11-09, stage 3, the pilot's 468 kWh usable battery: on cold days late in the pilot the logged state of charge
  went below zero (the architecture 5 pack had days ending at -13 per cent); the pilot battery is now 520 kWh usable
  and the longest duties are shorter, so no day ends below 5 per cent.
- 2026-11-09, stage 3, the quotation's warranty at 70 per cent after 8 years (3.75 per cent a year): inside the loss
  band, so the manufacturer's floor would have given the graded loss; at 75 per cent it gives 3.1, outside the band,
  and still orders the six.

- 2026-11-08, stage 5, the forum and context artifact as drawn (board_of_directors, register): `guard.py heart` on
  the final pull BLOCKed both (`ban.forum`, `ban.artifact`) against task2 v4, registered after this card; redrawn to
  executive_team (the management group approves the order) and operations_log (the weighbridge and telematics logs
  carry the evidence), the prompt, FES-2 1 and 4.4 and the memo reworded; no figure moved.

- 2026-11-08, stage 4, narrowing the pilot shippers' mean loads (11.7 to 12.9 t) so the pilot-shippers' pooled line
  (rung 2a) falls clear of the limit: the golden lost the between-shipper spread its estimate leans on (slope 1.95, the
  within-duty fit and the shipper-mean route left the golden's bins and the latter its six); reverted, the rung is
  ruled out by the per-shipper slopes and recorded as straddling the limit.

- 2026-11-08, architecture 4 (the Irish retailer's outlying districts handed to a courier, each set priced on the
  fitted van run): spent on the platform; the author reports not stumped, run texts not supplied to the repo. The van
  that drives through a district to reach the next one is a mechanism the stop sequences visibly carry (the run-days
  that skipped a district show it), modelled on sight like every earlier Sulfur landing. The world is left; the next
  deep step must sit in a property the rows in view cannot show, with its evidence in another file.
- 2026-11-08, stage 2 pricing, the pilot's telematics at trip grain (each leg's energy): the empty legs carry a payload
  of exactly zero, an error-free contrast with the loaded leg, so the declared fit's payload term came out at 2.0
  against 2.2 and the dilution vanished; the fleet portal's daily summary is the pilot's record.
- 2026-11-08, stage 2 pricing, clerks' error at 21 to 24 per cent: the declared slope fell to 0.6 kWh per tonne per
  100 km, below what rolling resistance alone costs, a figure a solver sanity-checks against physics; at 17 per cent
  it is 1.0, low but not absurd.
- 2026-11-08, stage 2, an ask on each going duty's spare load to the nearest tonne: the standing family spread it over
  a tonne on four of six duties (a fork on the asks); dropped.
- 2026-11-08, stage 2, the shortlist on mid-weight loads: duties near the pilot's mean load (12 t) give the same energy
  on any slope, so the shallow run kept 6 of 14 energies; the shortlist's shippers now sit far from the mean.

- 2026-10-31, architecture 2 (the agro-climatic network's 2028 drift-alert setting, the drifts cut short by the 3.0
  alerts' repairs): spent at the batch 1 repair; the determinism judge returned NOT_DETERMINISTIC, SEND_BACK: the 4.0
  call counted every repaired drift the re-run never reached as exactly one later alert, which no shipped file
  forces; a rate model built from the sensor history (onset at the previous clean check) puts slow drifts hundreds of
  days from the wider limits and gives 14 to 16 a year at 4.0, not 18; and the new contractor's visit day rested on
  an inference. Filing the counting rule would make the decisive step rule application, so the world is left after
  two architectures.
- 2026-10-31, the draw's first card (gap population, G3 decisive): `test.same_puzzle` and `test.same_driver` BLOCK
  against task270 v8, task464 and four older builds; the decisive gap is time (the route of record is standing and the
  routing changed night by night), the honest reading, which clears both.
- 2026-10-31, a bypass mechanism (depot-to-depot direct trailers skipping every hub): on the route of record each
  direct-loaded parcel is a miss at its plan's hub, a loud rate a solver investigates, and the lane-night correction
  that follows lands that hub's verdict; dropped before any data, the overflow alone carries the step.
- 2026-10-31, overflow nights on which Pruszkow's own scanning is unaffected: the overflow nights' excess of unscanned
  parcels at the Warsaw depots over Pruszkow's usual rate is then Strykow's unscanned overflow, a one-subtraction route
  to the call; Pruszkow's own misses now rise with its sorter's load on the same nights, so the excess route charges
  Strykow with Pruszkow's own misses and clears Pruszkow.
- 2026-10-31, a linehaul trip log in the pack: it is a second, timed route to each trailer and nothing else reads it,
  so its presence would announce the step (readability test 7); the unload bursts carry the trailer on their own.
- 2026-10-31, the first ask A (each hub's sort events its interface sent twice): a re-sent batch of sort events is the
  battery's near-exact duplicate and sits on the call's own file; the ask moved to the courier events per depot.
- 2026-10-31, one handheld model per depot (TC51 at the contract depots only): the battery's near-exact duplicate then
  lands every TC52 depot's re-sends exactly; every depot now runs both models.
- 2026-10-31, ask B matched against every courier event: with trailer collections as the only absence, any courier
  event is evidence of collection and that shortcut lands all 13 depots; couriers now record a failed pickup against the
  pre-advised number, which is no collection.
- 2026-10-31, marketplace order numbers drawn per seller for every marketplace: two sellers on one marketplace then
  share an order number and a pickup is counted against the wrong order; the marketplaces that number orders globally
  now do so.
- 2026-10-31, Strykow's own sorter at 0.61 per cent: the morning's sorted split left Strykow at 0.87, 1.148x from the
  line; at 0.56 per cent it sits at 0.77.
- 2026-10-31, the card as drawn at the heart screen (G3 decisive, the head of tracking data quality asking, a PDF note
  beside the workbook): `guard.py heart` BLOCKed ban.pattern and ban.role against task5's later re-draw, and warned
  the shell (whether, each, pdf and xlsx) repeated task245; the measured ladder puts the decisive step past the
  missing-at-random split (rung 1), so the decisive generator is G17 and G3 is the default path's; the requester is
  redrawn to the director of network operations and the chart goes to the board on a slide.
- 2026-10-31, the claims file opened claims up to five days after the extract (`leak.py`, dates after the setting): a
  claim not yet opened on 6 November is not in a 6 November extract, and a claim opened in its last five days is open.

Architecture 2 and earlier, carried from the agro-climatic note:


- The seed's own pitfall (a per-station two-sigma rule against a network budget): the multiplicity reflex; it is the
  default path, not a stump.
- Limits estimated from short baselines (the parameter-estimation effect on false alarms): an honest replay of the
  filed limit-setting over the record lands it, and executing the filed limit rule is close to rule application.
- A burn-in of new sensors in a 2028 replacement programme: a composition shift (composition_mix banned against
  task473) announced by the replacement plan.
- Closures clustered in one province: the continuing stations keep their near neighbours on their own side and the
  alerts barely move (prototype, 0 of 97 continuing stations' spread up by 5 per cent); the programme's stations are
  interspersed, as gap-filling stations are.
- validated_decoy true on the first card (the replay reproduces the alert log and only the closures break it):
  guard BLOCK; the April 2026 additions put the refutation inside the record.
- Seed 252: the per-setting figures at 3.0 and 3.5 sat 0.17 from their rounding edges (65.67, 26.67 a year) and a
  literal reading of the record's first fortnight moved 3.0; a scan of 1,000 seeds found one (1141) with all four
  three-year counts divisible by three and unchanged under the start, limit-rounding and strict-limit readings.
- A statistic defined on every day with 10 residuals: the export carries read days only, and a reader of the export
  moved 4.0 from 11 to 10; the statistic and its alerts are now on read days (section 5).
- The hold read per calendar year: lifting it each January moved 3.0 and 3.5 by a whole alert; section 8 now says a
  new year's configuration does not lift it.
- One out-of-sample year: a single fresh year on the 2028 network raised exactly 18 at 3.5; three fresh years are the
  section 7 horizon (24.7 at 3.5, 10.3 at 4.0).
- The asks with one campaign device drawn at random: the readings-first path kept 10 of 24 and the order-first path
  12; the campaign visits, the cancellations after the visit and the remote resets are now aimed at every district,
  and the standard's absence reaches the winter visits no campaign touches.
- Architecture 1 (the record re-run with the 34 closing programme stations out of the neighbour pool, as the decisive
  step on its own): spent 10-20 at stage 4. Reader 1 re-ran the quality control with the 2028 network and filed 4.0 at
  9 a year, every setting within one of the golden (63, 26, 9 and 3 against 61, 25, 9 and 3); reader 2 replayed the
  record and filed 3.5 at 9; judge DETERMINISTIC APPROVE. A stated change with an obvious mechanism is landed by a
  careful reader: the network re-run is now the first rung, and the decisive step is the drifts the record's own 3.0
  alerts cut short.
- One key, the censoring alone (no closures): a single unprompted insight decides it, and a reader who thinks of the
  repairs lands the call; two keys, each alone leaving 3.5 inside the visits, are needed.
- Drifts anywhere in the network: a drift left to grow carries a close neighbour's statistic over that neighbour's
  limit before its own alert (prototype, 5 to 12 stations per seed whose counterfactual count departed from the
  re-run plus the cut-short drifts); drifts now sit only where the weight a neighbour gives them times their spread
  stays under 0.7 of the neighbour's own, at stations that keep their usual neighbours.
- Censored drifts the spring round would have found first: a drift cut short in January or February at a setting of
  3.0 would at 4.5 have met the station's spring round before its alert (prototype, 1 to 2 a year); a drift whose
  station's next round falls before it could have crossed 4.5 is redrawn.
- An autumn calibration round in 2027 and 2028: 2028's rounds would then differ from 2025's and 2026's, and the
  record's drifts of June to August would have been found by a round rather than an alert, a forecasting fork on
  the window; every year now has the spring round only.
- The six stations added in April 2026: their 21 months against the record's three years opened an annualisation
  fork on each setting's count; the six infill stations now report from 2025.
- Old sensors with standing offsets up to 0.4 degrees: a false alert's visit at such a station adjusts a sensor
  that never drifted, and the history's drift-alert adjustments stop meaning drifts; standing offsets are now under
  0.12 degrees and no check without a drift passes the 0.2 adjustment threshold.
- The visit asks on orders and readings alone (round 2): drift orders cancelled after the visit with the readings under
  the cancelled order, orders the handover export lost, and a closed order with nothing under it counted a visit when
  the station had a reading under another order while it was open. The pass 3 judge sent it back (52 cancelled orders
  with readings against the dictionary's Visita, the lost orders' window unrecoverable; Gate C on asks 3 and 4), and
  with the visit filed reader D built the visits from the readings station by station and took 24 of 24. Filing a
  visit closes the fork and hands the ask to every reader; the devices that held were all readings a careful reader
  joins. The cancellations after a visit and the lost orders are gone; the device is now readings no visit made (a
  spare checked at the workshop under the station's order), found only against the range the station's logger
  recorded that day.
- The growth of a drift left to the reader (rounds 1 to 3): the pass 4 judge read section 7 literally as the record
  re-run and found nothing filed that a drift the 3.0 alert's check set right would have gone on growing; the as-found
  errors at repair (0.6 to 0.9 of the 4.0 limit) then read as the drifts' full size, and 3.5 stood as at least as
  defensible (SEND_BACK, Gates A to C on the main call). Section 9 now files the property of sensors the counterfactual
  rests on (a drift does not stop on its own and grows at the sensor's own rate until a check sets it right); the
  censoring remains the analyst's, and the cut-short drifts alone, without the network re-run, still file 3.5.
- An open interval on the rate (2026-11-07, the portal's Domains Fit return): a bootstrap over the month's mornings or
  unloadings puts Pruszkow's lower bound at 1.01 (90 per cent) and 0.97 (95), so its side of the tolerance moves with
  the method and the seed; the request files the interval's model (each parcel an independent chance of a miss), under
  which every standard binomial interval keeps each hub on one side, and grades only that side.
- 2026-11-08, architecture 3 (the Polish carrier's October missed sort scans by hub, the unscanned overflow parcels
  charged to the hub whose trailer they came off): spent on the platform; both runs reached the golden's call and every
  graded figure, so the platform returned not stumped before any rubric. Each read the overflow off the observed hub
  within each delivery-depot, door and night cohort by a plan-against-observed cross-check, a contradiction a cross-tab
  exposes and so a work order, and executed every texture device and the interval the request named. The world is left
  (one architecture per world); the next deep step has to move both runs' Final Recommendation, since a landed call
  never reaches the asks.
- 2026-11-08, stage 2 pricing, Killala as a through-road district: its approach from Ballina is too short for time in
  district to clear 1.15 of the line once removal keeps it (1.47 against 1.24); it left the offer and stays on the
  Ballina run.
- 2026-11-08, stage 2 pricing, the first set-by-set pricing: handing over a run's far end makes every through-road
  district before it the new end, so a corridor whose end goes takes its through-roads with it and the default and the
  golden agreed on them; the deep step bites only where the far end stays (Clifden, whose hotels and shops take
  several parcels a stop) or where removal is priced one district at a time (Mulranny, Bangor Erris).
- 2026-11-08, stage 2, the draft prompt's "the van-hours our runs would no longer drive" and "the van-hours each of our
  runs would shed": counterfactual words pointing at removal (the review's condition 1); cut to "the van-hours it
  saves" and "before and after the hand-over".
- 2026-11-08, stage 3, the golden's run hours without the driver's break: NPS-3 2.3 counts depot out to depot in, so
  the before and after figures were short by the break; the model now carries the break (never saved), found by the
  ceiling script against the run log.
- Stage 4 fix pass (2026-11-08): the judge's independent fit put Leenane and Letterfrack at 118 to 124 van-hours against the golden's 110 and R04's saved hours 30 above the golden on a 2026-only fit, and read the offer's "in any combination" beside NPS-3 4.1 as a search order. Dropped the combination wording (NPS-3 4.3 now names the selection as an outcome), moved saved hours to 100-hour bins with the Achill road slowed (R04 to about 710 saved, 1,610 before) and Owenduff's price raised to EUR 13.40 to hold the net saving mid-bin; component 1 is now 'about 110 van-hours' against the hours Owenduff's charge would pay for. The call, the stump, the ladder and the default path did not move.
- 2026-11-10, architecture 10 stage 4, pass 7 on target.zip 67186f2dd19abb65 (the 690 kW world): judge DETERMINISTIC APPROVE (17 needs a charging efficiency under 0.894, never observed; 19 needs 0.948 or more, one outlier session in 3,291; the heater band, 10 to 20 minute margins and both schedules land 18; careful but hurried about 2.5 of 8, ordering about 21; the diesel ask does not hand over the bridge). Its two findings: the six pilot buses after delivery, closed as SF30 (one bus a block assigned, the night on the assigned blocks); and the Step-by-Step's earliest-departure clause, which its thread could not reproduce because it took every block as in the depot the whole night (3 of the 18 are; the generator's least-slack schedule recharges the 18 and earliest-departure-first leaves 98 kWh short), so the clause is cut to the exact flow and the least-slack schedule. The fourth leak reader quoted no process sentence, found no helper file and no one thing, and noticed the fuel heaters on a read, so R3's notice is a careful-pass move and its price rests on the figure from the HVO fills. No graded figure and neither zip moved.
- 2026-11-10, architecture 10 loop 1, the platform's holistic audit (0 of 1 items addressed): the order count was not
  forced (the agreement's "except for the workshop's two outlets at 22 kW" beside DES-1 3.2's "in the periods the
  agreement gives it" and the quotation's 22 kW AC inlet put M124 in, 19 for 18), and "a yes or no on going electric"
  (23 or 18), "every block that passes" (8.7 or 6.7 MWh) and "deliver" (8.0 or 8.7 MWh) each read two ways. Closed by
  WHAT pins (DES-1 3.2: the charging lane's chargers, the workshop's outlets for buses under repair, the draw as the
  chargers take it; the agreement and the plan on the outlets; the prompt's "qualifies under the standard" and "the bus
  of every qualifying block on charge" at the connection point). With the heaters already read by a careful run (the
  leak reader noticed them), the heater fix alone landed the old count (18), so the chain was one judgment short: the
  charging sessions now carry what a bus on charge draws beside its recharge (the battery held at charging temperature
  on a cold night), a third independent judgment graded as component 3, which moves the order to 17; the six pilot
  buses move to Kauppala in the plan, closing SF30 by the data.
- 2026-11-10, architecture 10 loop 1, the least night-period capacity at which every qualifying block can be
  recharged, as a sixth ask (the reinforcement's size): the exact flow needs 921 kW against 913 kW for the night's draw
  over its ten hours, because almost every qualifying bus is in the depot from 21:00 and leaves after 05:00, so the
  averaging shortcut lands inside any honest band and the ask would grade nothing; not built.
- 2026-11-10, architecture 10 loop 1, a cabin preconditioning load before departure from the charger (the quotation's
  earlier row): the relay holds the chargers off from 07:00, so the blocks departing after 07:00 (and the afternoon
  blocks departing after 11:00) could not precondition from the charger and the draw's timing forked; replaced by the
  battery's thermal management over the released hours, which the relay bounds on every block.
- 2026-11-10, architecture 10 loop 1, the clean re-judge (FIX_NOW, order kept): the loss band of 3.8 to 5.0 excluded a
  straight line in age (2.96 on that pack, 2.80 on the judge's refit) with nothing shipped ruling it out; the loss moves no
  verdict and no bus, so the band is widened to 2.7 to 5.0 rather than a document naming the age form (a HOW pin). The
  same pass recomputed the 17 and M145 by its own max-flow and least-slack schedules across its own readings of the
  charging split and the workshop outlets, the night at 9.23 MWh and the conditioning at 2.98 to 3.46 kW, all inside
  their bands; its simplified diesel refit (19 blocks, no swipe merge) did not reproduce ask 1, which `verify.py`
  reproduces on all 48 within 0.7 on its own code path, so Step 2 now says the fit is joint over every block the
  intervals touch. The answer blocks dropped the context figures an earlier audit read as rival answers (the energy
  into the batteries, the draw for the assigned blocks, the fit's unbanded efficiency and parameters from component 3).
- 2026-11-10, architecture 10 loop 1, the main thread's check on the FIX_NOW re-judge (APPROVE, order kept), whose own
  conditioning fit came out at 2.23 kW: the battery's gain on charge read on the fitted fade curve without the
  reversible cold capacity put the draw at 2.27 kW, the efficiency at 0.958 and the order at 18 (M124 refused), and fitted
  the sessions better than the day's own record, a fork on the call. The reversible cold capacity was 0.16 per cent a
  degree below 10 C (4 per cent at -15 C), riding in the gain on exactly the cold nights the conditioning is read from;
  at 0.04 per cent a degree (1 per cent at -15 C, a pack its thermal management keeps warm) every capacity basis but the
  bare quoted 480 kWh lands 17 with M145 refused (SF42), and the loss, the verdicts, the energies and the order do not
  move (the limit 390.5 to 390.3 kWh). The APPROVE was scoped to the earlier pack, so the judge runs once more.
- 2026-11-10, architecture 10 loop 1, the platform's Domains Fit return on the READY prompt (979f04f): it read every ask as
  a lookup or a certified figure applied to a stated rule ("look up diesel use per 100 km, compare a quoted kWh figure
  against a design-day threshold, count qualifying blocks, and sum connection-point energy ... nothing needs to be
  estimated, modelled, forecast or validated"), the "quoted 2027 model" taken for a quoted energy. The prompt now leads
  with the forecast's population (most of the blocks never run by an electric bus) and names each result as what it is
  (an estimate of the diesel use, a forecast from the company's own operating records of the design-day energy, an
  estimate of the loss, a forecast of the night's draw), as this slot's architecture 5 did when the same review read it
  as route arithmetic; the answer blocks say the same. A 90 per cent interval on the loss, the review's own example, was
  measured and not built: the iid, by-bus clustered and per-bus intervals all read 4.2 to 4.5 on this pack, so it would
  grade nothing, and its bounds would inherit the age-form fork the band was widened for. No graded figure and neither
  zip moved.
- 2026-11-11, architecture 11 (Saarnela fulfilment centre's 2027 peak plan, a schedule under capacity on ten results) landed on the platform: the pasted run opened the evening shift in weeks 47 to 50 in both small-parts zones exactly as the golden, fitted the aisle congestion on a logged density term, re-keyed the 53-week calendar and read Huippu Sport at its own mix (+0.129 against 0.13); it lost only the overstatement conditioned on the budget's planned growth (the pooled 9.97 per cent, certified by its own held-out WAPE) and the agency hours (7,744 against 8,390). Three of the four judgments were one recognition and a routine fit, and the one that held was a relation between a forecast's error and its own claim that no standard check probes, so architecture 12 leaves the world, the scaffold and the shell and builds every judgment as that kind of relation (runs/arch11/run1.md).
- 2026-11-12, architecture 12 stage 3, world seed 41207 with the first cold sensitivities: the record's twelve months for the starter-generator ran about 30 per cent above their expectation and the fitted frost terms came out negative on every landing-driven part, so the per-flight-hour outlook sat near the clean truth and the cold-snap replay ran backwards; the cold sensitivities rose to what the parts show in service and the world was drawn from a screen of 80 seeds (the record near its expectation on the priced parts, the frost terms positive, the drivers separated, the bulletin measurable, a watch list mostly of victims).
- 2026-11-12, architecture 12 stage 3, the Bodø shop at 56 to 58 per cent other work: the 2027 load took it past saturation, the golden's queue climbing to 40 days by December while its calibrated capacity ran 7 per cent low, so every in-house need rode the calibration's error; the shop now takes 52 per cent other work and each technician takes three summer weeks, staggered, so the queue builds in the holiday weeks and clears by the autumn in both the replay and the clean truth.
- 2026-11-12, architecture 12 stage 3, the shop replay at a constant capacity a technician-day with a July rule written in: the calibration came out low (the day-to-day other work, the beyond-repair assessments and the backlog at the window's start were missing) and the holiday rule was the generator's own; the replay now takes each day's other work as the shop booked it, starts five months early, carries the assessments, and staffs each day from the roster's own record, a later day from the roster's holidays a year before.
- 2026-11-12, architecture 12 stage 3, the forcing block's perturbations: the replay read only the propeller control's forecast, so moving the starter-generator's rate moved nothing, and each perturbation ran on another stream; the replay now carries each forecast's confirmed and no-fault-found totals and every part draws from its own stream, so a perturbation's effect is its own.
- 2026-11-12, architecture 12 stage 3, the 80 per cent range as a Poisson draw on top of the replay's count: it doubled the chance variance; the range now moves the replay's own count by the rate's error.
- 2026-11-12, architecture 12 stage 3, the avionics pools sized at 2027's need: the quick pass's pool as it stands then matched 9 of 16 lines and the careful pass's Palm 6, so more care earned less; the flight-hour repairers' pools are sized on the heavier 2026 flying, which a real pool carries into a year of fewer hours.
- 2026-11-12, architecture 12 stage 3, a world whose watch list was mostly rogues (14 of 25): the counts at face value saved 73 removals against the golden's 66, inside its band; the drawn world's list is 8 rogues, 14 victims of their aircraft's faults and one serial of chance.
- 2026-11-12, architecture 12 stage 3, the last twelve months left out of the removal bands: the report's own window on each part's driver is a defensible estimate, so it is a rival in every removal band and a member of the spares family; it moves no line of the plan.
- 2026-11-12, architecture 12 stage 4, the October report's 2027 outlook (section 3, every part at October's MTBUR on the programme's planned hours): the leak reader read it as the closest thing to a ready-made answer for the asked removals; it is out of the report, which keeps the twelve months' MTBUR and the watch list.
