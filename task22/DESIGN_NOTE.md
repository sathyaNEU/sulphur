# task22: which of Brandvold Public Utilities' fourteen gas districts enter the 2027-2029 main replacement program, and where the 2027 meter changeouts go

Architecture 2, re-rooted 2026-11-12 (filed 2026-11-13 UTC) after architecture 1 (Delmont Power and Light's feeder
energy balance) was landed by both platform runs (`runs/arch1_triage.md`). New world, dataset and shell; the deciding
lessons are drawn from what those runs named and waved through, never from what they computed.

## Draw

Subdomain: Energy Systems & Utilities (gas distribution losses and the district gas balance; house task type
  distribution-losses-energy-balance; the client's nearest task types are load forecasting and grid reliability)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a reconciled table plus findings: each pressure district's monthly gas balance from October 2023 to
  September 2026, conformed from the systems that each see part of it (the regulator stations' correctors, the cycle
  reads, the meter register, the accounts, the damage reports, the utility's own use), with the findings on top: the
  districts whose leak loss crosses the main replacement program's line and the districts whose non-compensating
  meters the 2027 changeout replaces
Weight: measurement: the largest term of every district's balance (what its customers took at base conditions) is
  recorded by meters that register gas at its own temperature, over read periods that cut across the months, and for
  a few accounts not at all; the last two builds put their weight on attribution (task4 v13) and investigation
  (task9 v3)
Data-native sentence: nothing meters a district's leaks, so each district's leak loss is what is left after what its
  customers took, and that term is recorded by meters that register the gas at the temperature it has in the buried
  service, read on cycles that cut across the months, with a few accounts taking gas no meter records; the regulator
  stations see each district's gas day by day, the commercial correctors and the county soil station see the
  temperature the gas in the ground actually has, while the 2024-25 logger study and the 2019 consultant both tied
  that temperature to the airport's air in winters when air and soil moved together.
People: drawn with `guard.py names --geo us --seed 2208`: Marc Gilbert (the gas utility's engineering manager, who
  asks; not named in the prompt), Jocelyn Murray (the consultant who wrote the 2019 lost and unaccounted-for gas study).
Decision: before the Brandvold Utilities Commission adopts the 2027 capital budget in December 2026, the engineering
  manager files which of the fourteen pressure districts enter the 2027-2029 main replacement program (the program
  rules: a district enters when its leak loss in the twelve months ending September 30, 2026 exceeded 1.0 per cent of
  the gas delivered into it) and in which districts the 2027 changeout replaces the meters that do not correct for gas
  temperature (funded where they under-registered by more than 4.0 per cent of what they registered over the same
  twelve months), with what the changeouts already scheduled for 2027 will have replaced before the 2027-28 heating
  season; forward-facing (the programs and the season are 2027's).

Card: `.claude/skills/fingerprint/cards/task22.json`, architecture v2, checked at WARN against every card on file
(skeleton severity none against everything, the slot's lineage included). The WARNs, answered: the strategy risk
(grain_or_unit) is analysis, not a field read: every field read correctly still leaves the gas temperature to
estimate, the read periods to re-cut and the diversion to tell from absence; the chain-near WARN against task8 v19
(the same answer shape and weight) shares no lesson, mechanism or file role; the question form "which" is the
decision's own (which districts); record_algorithm_inversion on two live builds (task16 v3, task20 v3) is a supporting
lesson here (the cycle inverted on each district's daily sendout), not the one the call turns on; set_over_threshold
on four live builds is the honest form for a filed per-district line. Redrawn at filing: the organisation family (an
investor-owned gas company repeats task20 v3's utility in the window, so the utility is the city's own, as most
Minnesota gas towns' are), the forum (a committee repeats task9 and task20; the city's Utilities Commission is a
board), the stakeholder family and the memo (a Word memo repeats task9 and task20's set; the Commission gets a short
deck).

## Stump screen

Written at the draw, before the card was registered and before any code. Six candidates through the nine tests (1 off
the closed page, 2 not a reflex, 3 nothing filed, 4 clean data, 5 two records, 6 the waved-through assumption with
its precedent, 7 a plausible shallower story, 8 across the data, 9 worth the call). Magnitudes from the scratch
prototype (a Fargo-to-Alexandria climate, soil at 24 inches insulated by snow, residential use of 0.055 Mcf a day
plus 0.0105 per degree day below 60 F): the outdoor non-compensating meters under-registered 5.3 per cent of what
they registered in the twelve months to September 2026 on the soil, against 7.5 per cent on the airport's monthly
air temperature (in the snowless 2023-24 winter the two differ by 0.6); spreading each read evenly over its days
moved 0.3 to 0.8 per cent of a district's twelve-month use across the window's ends, degree-day weighting 0.0 to 0.2.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Non-compensating meters register gas at the temperature of the buried service, which follows the soil; in the deep-snow winter of 2025-26 the soil held near freezing while the air fell as far as in 2024-25, so the logger study's tie of gas temperature to the airport's air (validated on its own winter) and the 2019 consultant's monthly-mean method overstate the 2025-26 under-registration by about 2 points of the outdoor non-compensating volume, and indoor meters sit at basement temperature | gas temperature carried on the air as the study and the incumbent did (N04 a model's transfer named and left untested; L37 a check that cannot see the condition; L22 the incumbent's formula whose generating assumption the data contradict) | the commercial correctors' daily average gas temperatures through 2025-26 and the county soil station's 20 and 40 inch temperatures, daily, against the monthly reads | none | kept |
| Each read period's gas carried to calendar months on the district's own regulator-station daily sendout: spread evenly it moves gas across the September and October ends (heating starts in October) and across the winter months (student rentals empty over the break) | consumption between actual reads spread evenly by day (N20, both architecture 1 runs) | the regulator stations' daily corrector volumes against the cycle reads | 2 is partial in gas: degree-day weighting lands near the golden outside the college district | kept |
| The 2027 changeouts finish at the pace access allows (indoor meters need an appointment), about two thirds by the heating season in 2024 and 2025, not on the plan's October 31 date | planned works taken to happen in full on their dates (N22, architecture 1 run 1; N03) | the 2024-26 changeout work orders (planned and completed dates, by meter location) against the 2027 plan | none | kept |
| Accounts whose winter use collapsed are new snowbirds (absent November to April, normal summers) or bypassed meters (low in every month from the bypass on, the summer base load included) | every collapse read as diversion, or every one as absence (L26 a plausible shallower explanation that passes its own checks) | the summer months' reads and the same accounts' earlier winters, and the 2023-26 revenue protection cases | 5 is partial: the summer evidence is the same reads file at another season | kept as a fourth, supporting result |
| The regulator stations' corrector gaps and fixed-factor days rebuilt from the gate balance | R39 (both architecture 1 runs rebuilt a sub-meter's gaps from the upstream balance) | the city gate corrector | 2 | dropped as a trap; kept as an assembly result priced Right |
| Leak loss read from leak counts times the incumbent's emission factor per mile of main | none: the runs take the balance's residual by reflex (R40's kind) | the regulator stations against the reads | 2, 4 | dropped |

The three strongest are independent: no one sentence rescues two of them (the gas temperature, the daily shape and
the past pace each name their own record), and the fourth is graded on its own evidence.

## Deep reasoning

Task type: distribution-losses-energy-balance (Energy Systems & Utilities, the house task type serving ETL; the client's
  nearest task types are load forecasting and grid reliability): a gas utility's district balance conformed from the
  systems that each see part of it, whose residual is each district's leak loss.
Domain test: every result is a quantity a gas distribution utility's measurement engineers compute: each pressure
  district's sendout at its regulator stations with the faulty corrector days rebuilt from the city gate, the billed
  volume of cycle-read meters carried to calendar months, the under-registration of meters that register gas at its
  own temperature, the gas taken through bypasses and furnace taps, the leak loss left, and the changeout schedule's
  pace.
Swap: "which electric feeders enter the reconductoring program on their losses" keeps the balance's frame, but an
  electric meter registers energy, not a volume at the temperature of the gas, there is no base condition to convert
  to and no soil holding the medium's temperature under the snow, so the deciding judgment (the gas temperature the
  non-compensating meters saw, tied to the soil rather than the air the incumbent used) has no counterpart.
Where the weight sits: R3, measurement: the largest term every district's leak loss is read against is the gas its
  customers took at base conditions, and for most meters that is a volume registered at the gas's own temperature;
  the temperature has to be rebuilt day by day from what sees it (the loggers in one winter, the soil station, the
  commercial correctors every day), and the incumbent's tie to the airport's air held only while air and soil moved
  together.
Layer 1: the regulator station correctors' communication gaps (random days on every station; Riverside's January 12 to 25,
  2026), Lakeview's failed pressure transducer (the corrector substituted its configured 25 psig for 35 from December 4
  to 21, 2025) and Westgate's stuck temperature transmitter (February 3 to 11, 2026); the AMR reads on twenty business-day
  cycles with estimated reads trued up by the next actual, four-dial rollovers, commercial multipliers, final and
  initial reads at the 2024 and 2025 exchanges and special reads at account changes; the June 2025 extract re-run that
  repeats a month of rows; blank compensation flags on 0.6 per cent of the register (the model code tells); the
  correctors' fixed-factor days; the airport's and the soil station's missing days; the gas day named by the date it
  begins at 9:00 a.m. None decides a result on its own: R2 of the bar asserts each, and R1 grades the station rebuild.
Not one thing: three judgments each move the district designations and none is enough alone: the gas temperature (the
  logger study's air line alone designates Downtown and Old Town only), the calendarization (reads spread evenly alone
  adds Halvorsen), the diversion against absence (every collapse booked alone drops Lakeview, no diversion alone adds
  Elm Grove and East Industrial); the careful but hurried route, which takes the air line, spreads evenly and books
  every collapse, designates Downtown and Old Town, and each one correction on it still files a wrong set; the
  changeout set and the 2027 pace need judgments of their own (R3's temperature, R8's past pace).
One-fact test: the most useful single sentence is "gas in a buried service runs near the soil's temperature, and the
  2025-26 snow kept the soil warm; the commercial correctors log what the gas actually was"; on the careful pass it
  rescues R3 and R7 (2 of 8) and no designation, because the reads are still spread evenly and every collapse is still
  booked; the calendarization, diversion and pace sentences rescue one result each (effort.json hints, computed).
Not semantics: every field, code and clause read correctly (the read types, the model codes, the pressure factor, the
  rules' definitions of leak loss, base conditions, under-registration and gas taken without authorization) still
  leaves the gas temperature to estimate, the read periods to re-cut and each collapse to read as diversion or
  absence, each filing a different wrong set.
Not rule application: the program rules file what leak loss is, the base conditions, the two lines, the 100 meters and
  the window; no filed procedure says what temperature the gas at a meter had, how a read period's gas falls across
  its days, which collapses in use are diversion, or how fast a changeout schedule is worked.
Estimand: the program rules, Resolution 2026-11 (leak loss and its terms; base conditions 14.73 psia and 60 F;
  Rule 1, a district enters the 2027-2029 main replacement program when its leak loss in the twelve months ending
  September 30, 2026 exceeded 1.0 per cent of the gas delivered into it; Rule 2, the 2027 changeout goes where the
  non-compensating meters under-registered by more than 3.5 per cent of their billed volume over the same months, with
  at least 100 such meters; Rule 3, the 2027 plan's Old Town and Downtown changeouts proceed); the gas rate schedules
  (the billing volume as registered volume times the pressure factor 0.9663, estimated bills corrected by the next
  actual reading, the gas day); the 2027 plan (the heating season begins November 1); the
  prompt (the monthly balance's columns and window, each district's leak loss as a share of its gas in, the accounts
  that took gas without authorization, the scheduled 2027 changeouts done before the 2027-28 heating season).
No decoy: nothing is written to carry a wrong answer: the 2025 logger study memo reports its own fit of its own data,
  which reproduces exactly (R4 of the bar asserts it) and held for its winter; the 2019 consultant's monthly-mean method
  is the incumbent's honest computation for 2019; the utility's annual LAUF report states its billed basis truthfully;
  no document ranks districts.
No replay: no result re-derives a published figure; the annual LAUF report's billed-basis percentages are the
  incumbent figure the runs reproduce and the chain supersedes.
Pinned: every rival a careful analyst could defend is run on the cut pack and lands inside each graded band with the
  golden sets (checks.py R7): each read spread on a base-and-degree-day fit of the district's sendout instead of the
  sendout itself, the gas temperature tied to the commercial correctors' instead of the soil, and both together; the
  sets hold under the air coefficient 20 per cent either way, the indoor temperature 2 F either way, and the damage,
  own use and diversion volumes 20 per cent either way. Every district sits 12 per cent or more from the 1.0 line
  (nearest Lakeview 1.21 and Halvorsen 0.83) and every eligible district 12 per cent or more from the 3.5 line
  (nearest Airport 2.99 and College Hill 3.05).
Run forecast: a strong run loses R3 by a method shortcut (the logger study's straight line on the airport's air, or the
  2019 monthly mean), R2 by dismissed own evidence (each read spread evenly by day, named as an assumption and kept),
  R4 by stopping at the first story (every collapse in use booked as diversion, new snowbirds with it), R5, R6 and R7
  by a method shortcut (the residual and the rules on those terms), and R8 by dismissed own evidence (every scheduled
  changeout taken as done on its date); R1 is earned by reflex.
Strategy label: OWN (no client strategy carries a gas balance; the client's emissions-table ETL strategy is the nearest
  by type and shares no step).
Depth level: 5 on the client's scale: four independent judgments each move a graded figure (the gas temperature, the
  calendarization, diversion against absence, the changeout pace), the designation needs the first three together,
  and seven shortcut routes land on five different wrong sets (none, two, four, six and seven districts).
Lesson: a correction carried on a proxy is only as good as the proxy's tie to the true driver in the period it is
  applied to: the gas a non-compensating meter registers is at the temperature of the soil around the service, which
  moved with the air in the winters the incumbent and the logger study were checked on and came apart from it under the
  2025-26 snow, so the in-sample checks pass and the target year's correction is overstated; the balance also needs the
  cycle reads re-cut on each district's own daily sendout and each collapse in use read for diversion or absence by the
  season only one of them touches. No build on file corrects a recorded volume for a physical state that a second
  instrument sees.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each district's gas in at its regulator stations, faulty days rebuilt from the city gate: Riverside 22,715.3 Mcf in January 2026, Lakeview 13,568.6 in December 2025, the fourteen districts 1,844,373 in the twelve months to September 2026 | assembly-reconciliation | the correctors' daily records and alarms, the city gate corrector, the stations sheet; the rules' gas delivered into the district | January and December within 1.5 per cent, the twelve months within 0.3 per cent | dismissed own evidence: the faulty days kept as recorded or as zero (Riverside's January 12,943.3); the careful pass rebuilds them by reflex (R39) | - | Ask 1 |
| R2 | the billed volume of each district's cycle-read meters carried to calendar months on the district's own daily sendout: College Hill 16,638.8 Mcf in January 2026, North End 14,000.3 in March 2026, Old Town 8,105.3 in October 2025, Halvorsen 3,293.3 in October 2025 | missingness-measurement | the reads' read types and indexes, the stations' daily volumes; the prompt's calendar month | each within 2 per cent | dismissed own evidence: each read spread evenly over its days, named as an assumption and kept (College Hill January 15,647.2, North End March 12,788.1) | - | Component 4 |
| R3 | the under-registration of the meters that do not compensate for gas temperature in the twelve months to September 2026: Riverside 3,645 Mcf, Lakeview 2,406; College Hill 3.05, Airport 2.99, Halvorsen 4.61 per cent of their billed volume | missingness-measurement | the register's flags and model codes, the loggers, the soil station, the commercial correctors' gas temperatures; the rules' base conditions and under-registration | Mcf within 6 per cent; shares within 0.20 points | method shortcut: the 2024-25 logger study's straight line on the airport's air (Riverside 4,452 Mcf, Halvorsen 5.67 per cent), or the 2019 consultant's monthly mean air | - | Component 1 |
| R4 | the accounts that took gas without authorization in the twelve months: 15, with 568 Mcf in Elm Grove, 1,310 in East Industrial and 267 in Sundquist | exploration-triage | each account's monthly use against its own weather response the year before, the accounts' open and closed dates, the exchanges; the rules' bypass or interference | count within 1; volumes within 25 per cent | stopped at the first story: every collapse in use booked as diversion, new snowbirds with it (61 accounts) | - | Component 3 |
| R5 | each district's leak loss in the twelve months to September 2026 as a share of its gas in: Riverside 1.25, Lakeview 1.21, Sundquist 1.35, Halvorsen 0.83, Elm Grove 0.69, East Industrial 0.59, College Hill 0.78 | decomposition-attribution | the rules' leak loss; R1 to R4, own use, the damage reports | each within 0.10 points | method shortcut: the residual on the air line, the even spread and every collapse booked (Riverside 0.59, Lakeview -0.03, Sundquist 0.83, Halvorsen 0.20) | R1, R2, R3, R4 | Component 2 |
| R6 | the districts that enter the 2027-2029 main replacement program: Downtown, Lakeview, Old Town, Riverside and Sundquist | synthesis | Rule 1 | exact set | method shortcut: Downtown and Old Town only | R5 | Recommendation |
| R7 | the districts where the 2027 meter changeout goes: Elm Grove, Halvorsen, Lakeview, North End, Prairie Rose, Riverside and Sundquist | synthesis | Rule 2 | exact set | method shortcut: the air line puts Airport, College Hill and East Industrial over the 3.5 line too | R3 | Ask 2 |
| R8 | the changeouts the 2027 plan schedules in Old Town and Downtown that are done before the 2027-28 heating season: 668 of 976 | forecasting | the 2024-25 work orders' planned and completed dates by meter location, the 2027 plan, its November 1 season start | within 4 per cent | dismissed own evidence: every scheduled changeout done on its date (976) | - | Ask 3 |

Carry-forward: R1, R2, R3, R4 and R8 stand on inputs of their own (the stations and the gate; the reads and the
stations' daily volumes; the loggers, the soil and the correctors; each account's own reads; the work orders and the
plan); R5 falls with any of R1 to R4, R6 with R5, R7 with R3. A run that slips on the gas temperature keeps R1, R2, R4
and R8; one that spreads evenly keeps R1, R3, R4, R7 and R8; one that books every collapse keeps R1, R2, R3, R7 and R8.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| the deep snow of 2025-26 holding the soil, and the gas in every buried service, near freezing while the air fell as far as in 2024-25 | constructed (the simulated weather and soil) | no: every outdoor non-compensating meter in all fourteen districts, in the soil station's record every day; it moves three designations and adds three changeout districts, and moves nothing in Old Town and Downtown, whose meters are mostly inside | modelling: the gas temperature fitted on the driver it follows (the soil) and checked on the correctors' 2025-26 gas temperatures | modelling | keep |
| new snowbirds, away from mid-November to mid-April for the first time in 2025-26 | constructed (the simulated households) | no: in eleven districts (3 per cent of Lakeview, under 1 per cent elsewhere); it decides Lakeview only when every collapse is booked | modelling: each collapsed account's winter heating response and its summer | modelling | keep |
| bypasses and furnace taps from the autumn of 2025 | constructed (the estimand's own term) | no: six districts, two of them deciding (Elm Grove and East Industrial with no diversion subtracted) | modelling: each account against its own weather response | modelling | keep |
| student rentals emptied over the winter break and the summer | constructed (the simulated households) | no: College Hill, Old Town and Downtown; it decides no set and shows in R2's College Hill January | a targeted query: the station's daily volume against degree days | routine | keep, R2 only |
| the early October 2025 cold spell | constructed (the simulated weather) | no: every district's read periods across October 1, at sizes set by each district's cycles; it decides Halvorsen only under an even spread | modelling: the read periods re-cut on the station's daily volume | modelling | keep |
| the stations' faults | constructed (the simulated correctors) | no: random communication gaps on every station, three named faults; graded in R1 | a targeted query: the stations against the gate | routine | keep, R1 only |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each district's gas in at its regulator stations, faulty days rebuilt from the gate | Missed | Right | Right |
| R2 the volume billed for each district's meters, carried to calendar months | Missed | Partly | Right |
| R3 the under-registration of the meters that do not compensate for gas temperature | Missed | Missed | Right |
| R4 the accounts that took gas without authorization, and their volume | Missed | Partly | Right |
| R5 each district's leak loss in the twelve months to September 2026, per cent of its gas in | Missed | Missed | Right |
| R6 the districts that enter the 2027-2029 main replacement program | Missed | Missed | Right |
| R7 the districts where the 2027 meter changeout goes | Missed | Partly | Right |
| R8 the scheduled 2027 changeouts done before the 2027-28 heating season | Missed | Missed | Right |
| Roughly | 0 of 8 | 2.5 of 8 | 8 of 8 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the passes are the generator's own routes on
  the cut pack: the quick pass bills taken in the month read, the stations as recorded, no temperature correction and
  no diversion; the careful pass every file conformed and the stations rebuilt, the logger study's air line, reads
  spread evenly, every collapse booked as diversion and the plan's dates; the golden)
Largest single hint: "Gas in a buried service runs near the soil's temperature, and the 2025-26 snow kept the soil
  warm; the commercial correctors log what the gas actually was."; rescues 2 of 8 results
Pair estimate: 40.5 (the careful pass earns R1, part of R2, R4 and R7 and the instruction-following share; every lost
  cell cites a precedent of its own class)

## Data provenance

Source: generated by task22/generator from a simulated municipal gas distribution system (seed 22062): daily weather
  for three winters (the snowless 2023-24, the thin cover of 2024-25 and the deep snow of 2025-26) and the soil under
  it at five depths, fourteen pressure districts fed through sixteen regulator stations from one city gate, about
  10,300 premises with their meters (compensating or not, inside or out, exchanged in the 2024 and 2025 programs), daily
  use by premise driven by the weather with base load, students, snowbirds, vacancies and furnace rebates, what each
  meter registered at its gas's temperature, AMR cycle reads with the billing system's estimates, 58 corrector
  customers, bypasses and furnace taps, leaks, third-party damage, station heaters, the 2024-25 loggers and the
  changeout work orders.
Behaves like the real thing: gas at an outdoor meter set follows the soil at service depth, pulled a fifth of the way
  toward the air and warmed by the house wall in the cold, and indoor meters sit near basement temperature, as
  temperature-logging studies of residential meters report; snow cover insulates the soil and holds it near freezing;
  a non-compensating meter under-registers by the ratio of 519.67 to the gas's temperature in Rankine, about 5 per cent
  of an outdoor meter's winter volume; leak loss runs 0.2 to 1.6 per cent of a district's gas in, highest where cast
  iron remains, as gas utilities report; inside meters take an appointment to change.
Genuine patterns: (1) heating-driven use with a base load and a thermal carry-over from the day before (2) three
  different winters and their soils (3) student rentals emptied over the break and the summer, snowbirds every
  winter, account turnover with vacant spells (4) furnace replacements lowering a household's heating slope (5) the
  2024 and 2025 changeout programs, faster outside than inside (6) leaks growing as the mains age and with frost in
  cast iron districts (7) third-party damage concentrated in the growing districts
Problems by process: correctors' communication failures, a failed pressure transducer and a stuck temperature
  transmitter; AMR modules going quiet and the billing system estimating; rollovers, multipliers and exchanges; the
  June 2025 extract re-run; register flags left blank; the correctors' fixed-factor days; the weather stations' missing
  days.
Breadth: 22 files (three large CSVs of 18,577 to 421,786 rows, a daily weather and a daily soil record of 1,192 rows
  each, seven workbooks, four PDFs, three distractors: the appliance rebates, the CNG station's sales and the supply
  invoices), fourteen districts, sixteen stations, 10,282 premises and 58 corrector customers, so deciding which
  records close each district's balance is work.

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, missingness-measurement, exploration-triage,
  decomposition-attribution, synthesis, synthesis, forecasting
Question form: which (which districts enter the program, which get the changeout)
Nearest build: task8 v19 (the same answer shape and weight: a reconciled table, measurement) equates test scores across
  instruments through a common measure; this build corrects recorded gas volumes for a physical state a second
  instrument sees and decides a filed per-district line; architecture 1 of this slot closed an electric balance whose
  technical term was a network computation. Abstraction sentence: none writable against either; the guard's
  skeleton read is severity none against everything on file.

## Frontier check

Precedents: R2 N20 (consumption between reads spread evenly by day, both architecture 1 runs); R3 L22 (the published
  formula whose generating assumption the data contradict), L37 (a check that cannot see the condition), N04 (a
  model's transfer named and left untested); R4 L26 (a plausible shallower explanation that passes its own checks); R5
  and R6 L22, L26, N20; R7 L22, L37, N04; R8 N22 (planned additions taken to start in full on their dates, architecture
  1 run 1), N03 (scheduled works assumed to happen as planned).
Shallow path checks: R3: the logger study's air line fits its own winter (R-squared 0.76) and a hold-out of its own
  logger-days passes, and the corrected system loss looks plausible; only the soil station or the correctors'
  2025-26 gas temperatures (another instrument, the target winter) show the gas warmer than the line says. R2: the
  even spread reconciles every twelve months to the billed totals; only the stations' daily volumes (another grain)
  show the October 2025 cold spell and College Hill's empty break. R4: booking every collapse reconciles to the drop
  in billed volume and finds the known bypasses; only each account's summer and its winter heating response (another
  season) tell the snowbirds apart. R8: the plan's dates are filed; only the 2024-25 work orders (another program) show
  the pace inside meters were changed at.
Assumption made false: that the gas at a meter without compensation is at the air's temperature, or at a line on the
  air fitted in an earlier winter (N04): false here because the gas follows the soil around the service and the
  2025-26 snow held the soil near freezing while the air fell as far as in 2024-25; tested through the soil station
  and the correctors' gas temperatures. And that a read period's gas falls evenly over its days (N20): false because
  heating began in a cold first week of October 2025 and College Hill's rentals emptied over the break; tested by the
  stations' daily volumes.
Forcing: the line is each district's leak loss against 1.0 per cent of its gas in (Rule 1) and each eligible
  district's under-registration against 3.5 per cent (Rule 2); the golden family's four variants agree within 0.06
  points and file both golden sets; the nearest districts to Rule 1's line are Lakeview 1.21 and Halvorsen 0.83 (family
  0.83 to 0.85, perturbations 0.76 to 0.90), to Rule 2's College Hill 3.05 and Airport 2.99; the shortcuts land on the
  other side (the air line Lakeview 0.44 and Riverside 0.52; the even spread Halvorsen 1.16; every collapse booked
  Lakeview 0.26; no diversion Elm Grove 1.29, East Industrial 1.27; the air line College Hill 3.71, Airport 3.71); the
  air coefficient, the indoor temperature, damage, own use and diversion moved by their defensible spreads all hold.
Noun swap: the nearest skeletons on file (skeleton.py check: task4 arch 12, task4 arch 10, task4 v13, task22 v1) share
  at most one supporting lesson and no decision form, answer pattern, mechanism or detection; swapped into task22 v1
  (feeders, theft, technical losses) the deciding move (a recorded volume converted at the temperature its medium had,
  carried on the soil rather than the air) has no place, and v1's lessons (a nonlinear loss at the loads' positions, a
  switching log replayed) none here; severity none.
Closed strategies: the call turns on exposure_basis_decoupled (a correction carried on a proxy that moved with its true
  driver only in the periods it was checked on), off the client's closed page; the nearest card, "The pooled effect
  does not transfer to a target with a different mix", differs in mechanism and fix: no effect is estimated on one
  population and reweighted to another's mix; the gas temperature is a physical state rebuilt from the instrument that
  follows its driver and checked on a second instrument in the target winter. The supporting lessons (the cycle
  inverted on each district's sendout, diversion told from absence, the changeout pace) are open too; the chain keeps
  no closed lesson as a step (skeleton.py closed task22: none).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | leak loss in a district | gas in less customers, own use, damage and diversion; gas in less billed volume | the rules' definition | the program rules, section 2 |
| SF2 | the twelve months | October 1, 2025 to September 30, 2026 by the days gas flowed; bills read in the window | the days gas flowed | the rules' "in the twelve months ending September 30, 2026" and the prompt's calendar months |
| SF3 | base conditions | 14.73 psia and 60 F; the meter's own conditions | 14.73 psia and 60 F | the rules |
| SF4 | the gas day | named by the date it begins at 9:00 a.m.; the calendar day | its start date | the gas rate schedules, section 4; same call: a nine-hour shift is inside every band |
| SF5 | the billed volume | registered ccf times the pressure factor; times a temperature factor too | the pressure factor | the gas rate schedules, section 2 |
| SF6 | a meter's under-registration | the gas it delivered at base conditions less its billed volume; none for compensating meters | the rules' definition, compensating meters zero | the rules, section 2 |
| SF7 | Rule 2's ratio and eligibility | under-registration over the non-compensating meters' billed volume, 100 or more such meters in service; over all meters | the rules' ratio | the rules' Rule 2 |
| SF8 | a meter whose compensation flag is blank | its model code's compensation; non-compensating | the model code | the register's meter models sheet (and the R2 assertion: either reading holds every set) |
| SF9 | gas taken without authorization | through a bypass or interference; any fall in use | bypass or interference | the rules, section 2 |
| SF10 | a corrector's fixed-factor day | its uncorrected volume at the account's own correction; as recorded | the account's own correction | same call: inside every band |
| SF11 | own use in a district | the station heaters; with the gate line heater | the station heaters | the rules (the gate heater sits in no district) |
| SF12 | damage losses | the reports' estimates; recomputed | the reports' estimates | the rules' "as reported"; 20 per cent either way holds |
| SF13 | the 2027-28 heating season | from November 1, 2027; from October 1 | November 1 | the 2027 plan's note |
| SF14 | done before the season | the expected count at the past pace; every meter whose planned date falls before it | the expected count | the prompt's "will be done"; the work orders |
| SF15 | a premise's district | the register's pressure district | the register | the register |
| SF16 | a corrector customer's district | the corrector sheet's pressure district | the corrector sheet | the register |
| SF17 | an account whose use collapsed | a run of three or more months under its own weather response of the year before, reaching into the heating season; any such run, summer included; cuts from 0.30 to 0.50 of the response | a run reaching a heating month at 0.40 | same call inside 0.30 to 0.45; at 0.50 without the heating month the extras are College Hill rentals whose summer of 2025 dipped as far (their own reads; checks.py) |
| SF18 | a furnace tap against an absence | winter heating response lost with the base kept; reduced by two-thirds or more | lost (heat kept under 0.10 to 0.25: same call) | at 0.35 the extras are first-year snowbirds back at their weather response in May 2026, while every tap is under 0.65 in May's heating (checks.py) |
| SF19 | the leak loss share's window | the program's twelve months (Rule 1's); the three years of the balance; each month | the program's twelve months | the prompt's "for the program's twelve months" and Rule 1 |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the fourteen pressure districts; every premise and corrector customer the register places in each |
| 2 | Unit of account: the district, by the gas day for gas in and by the day for customers' use |
| 3 | Attribution window: a premise's gas counts in the district the register places it in, every day |
| 4 | As-of dating: the extracts of November 2 to 5, 2026; the twelve months end September 30, 2026 |
| 5 | Version basis: one extract per system; the June 2025 re-run's repeated rows kept once |
| 6 | Denominator: leak loss over gas in (SF1); under-registration over the non-compensating meters' billed volume (SF7) |
| 7 | Weighting: none; volumes summed |
| 8 | Window length: twelve calendar months (SF2); the monthly balance thirty-six |
| 9 | Boundary inclusivity: a month runs from the first gas day to the last; a read covers the days before it |
| 10 | Rounding path: daily volumes summed at full precision, Mcf shown to 0.1 or 1, shares to 0.01 |
| 11 | Tie-break: none needed; every district is 12 per cent or more from each line |
| 12 | Maturity and censoring: every read covering September 2026 is in the extract (the last cycles read in October) |
| 13 | Order of operations: rebuild the stations, build the read periods, spread them, correct for temperature, find diversion, subtract |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: the re-run's rows are exact copies, kept once |
| 16 | Identity normalisation: premises to districts by the register; meters to compensation by flag or model code |
| 17 | Netting against gross: a true-up after an estimate nets inside the actual-to-actual period |
| 18 | Dimensional units: Mcf at base conditions; per cent of gas in; per cent of billed volume |
| 19 | Code and status semantics: read types, alarms and corrector status as each system writes them; estimated bills as the rate schedules describe them |
| 20 | Integerisation: accounts and meters whole; the 2027 count the expected number, rounded |
| 21 | Clause scope: Rules 1 and 2 apply to every district alike; Rule 3 to the plan's two districts |
| 22 | Forward window contents: the 2027 plan's changeouts in Old Town and Downtown, nothing else |

## Literal reader

Executing the rules word for word: each district's leak loss is its regulator stations' gas, less what its customers
took at 14.73 psia and 60 F, the station heaters, the damage reports and the gas taken through bypasses or
interference, over the twelve months ending September 30, 2026; districts over 1.0 per cent enter the program; the
changeout goes where the non-compensating meters' under-registration exceeded 3.5 per cent of their billed volume with
100 or more such meters. A reader who converts with the logger study's line, spreads each read evenly and books every
collapse designates Downtown and Old Town; none of those is another reading of a filed term, each is an easier method
on the same filed estimand.

## Prompt contract

A voice rewrite keeps: the question (which of the fourteen districts enter the 2027-2029 main replacement program and
which get the 2027 meter changeout); the monthly balance from October 2023 to September 2026 with its columns (gas in,
the billed volume of the gas its meters took that month, what the meters without temperature compensation under-registered, the corrector
customers, own use, damage, gas taken without authorization, the leak loss left); for the program's twelve months, each
district's leak loss as a share of its gas in and the accounts that took gas without authorization; how many of the
changeouts already scheduled for 2027 will be done before the 2027-28 heating season; a spreadsheet and a short deck for the Utilities Commission. It never
adds a rounding instruction, a method (no soil, logger, air, temperature model, snow, degree day, daily shape, even
spread, snowbird, bypass, summer, work order or pace), a warning, an attached file's name, a role, or a count the data
hold.

## Pre-ship check

- Bar re-read on the built pack: eight results across six areas (assembly and reconciliation, missingness and
  measurement, exploration and triage, decomposition and attribution, synthesis, forecasting), each pinned by a filed
  sentence (Resolution 2026-11's definitions and Rules 1 to 3, the gas rate schedules' billing volume and gas day, the
  2027 plan's November 1 season start) and the data, with the bands the answer blocks state; precut 0 FAIL; checks.py
  117 of 117; verify.py 17 of 17 on its own path; two rebuilds byte-identical.
- Hidden factor record against the cut data: the 2025-26 snow holds the soil at 20 inches about 8 F warmer than in
  2024-25 at the same air, in every district's record; new snowbirds in eleven districts (3 per cent of Lakeview);
  bypasses and furnace taps in six districts (15 accounts found, 16 in the simulation: the Old Town tap from December
  20 enters only at a half cut); student rentals in three districts; the early October
  2025 cold spell across every district's read periods; station faults on every station.
- Effort test against effort.py: quick 7.0, careful 40.5 (2.5 of 8), thorough 100; the largest hint rescues 2 of 8;
  seven shortcuts land on five distinct wrong sets.
- Forcing: Rule 1's nearest districts Lakeview 1.21 and Halvorsen 0.83, Rule 2's College Hill 3.05 and Airport 2.99;
  the golden family's four variants and ten perturbations file both golden sets; the scheduled 2027 count's rivals
  668 to 689 inside 4 per cent of 668; the accounts count 14 to 16 under every defensible detection (SF17, SF18).
- Stage 4: the determinism judge DETERMINISTIC and APPROVE on the fresh cut and again on the final prompt
  (`determinism_check_report.md`; its first pass had read a stale target.zip). The isolated leak reader on the fresh
  cut: no ranking file, no helping file, no answer figure, every REVIEW line harmless; its points ruled in one pass:
  the gas rate schedules' meter-access clause (an inside meter takes an appointment, the mechanism R8's pace turns on)
  removed; the prompt pins the accounts to "the program's twelve months" and the billed volume to "the gas its meters
  took that month", and after the reader's re-read the leak loss share to the same twelve months (it had no window of
  its own), and a third read of that prompt alone found every ask determinate and nothing named; the re-read's other points (the rules and the plan's note file what is decided; "took gas ... in" is not
  "found in"; the zip entries carry the sender's Central clock, read an hour off on an Eastern machine) are harmless; the plan's note that the heating season begins November 1 stays, since it files R8's window and
  the hurried count (every scheduled changeout done) is the shortcut, not the reading. The accounts result, which the
  judge re-derived only on a coarse binning, was then forced in checks.py (SF17, SF18), with the golden's collapse
  rule now requiring a run that reaches the heating season; no figure, pack file or golden file moved.
- Gate WARNs answered: precut's two routine factors (student rentals, station faults: Hidden factor record, neither
  decides a set) and nearest chains (Template check); the deliverable quota (a spreadsheet and a deck on 24 per cent of
  21 prompts, against the last two builds' spreadsheet and memo, which heart refuses to repeat: Tried and rejected);
  heart's strategy risk, chain near and question form, and the house lessons and shell (Draw).
- Containers: audit_containers exit 0 on the pack, the golden and both zips.

## Tried and rejected

- 2026-11-12, at filing: a rural electric cooperative as the organisation (Ketchum Prairie Electric Cooperative):
  both its honest organisation families repeat the last three builds (task7 v10 a cooperative, task13 v4 a utility),
  so the same balance moved to a city-owned utility, where theft, far-end grows and deemed lights are as common.
- 2026-11-12, stage 3: the window to October 2026 with the extracts pulled on December 2: the pack's files ran past
  the day it ships (breaker data to November 30, the GIS export dated November 25), a dated tell; the world moved back a
  month to the twelve months to September 2026 with the extracts of November 2 to 5, the simulation and the hourly
  files from September 2023 and the reads from August 2023, so every bill in the first window carries simulated use
  (a cut with the reads starting in September had written late cycles' first bills as register-only reads, dropping a
  month of their sales from the first window and turning the rise into a fall), the weather on a stream of its own,
  and NTH-3's theft target lowered from 566 to 480 MWh to hold the fourth-to-fifth margin (197.6).
- 2026-11-12, stage 4: the leak reader found the three feeders without AMI (APT-4, CHL-2 and CHL-3) were three of the
  golden four, with the CWP naming the same three for AMI's third phase: one group-by and one PDF line gave a prior on
  three names. The rollout moved CHL-3 into the May 2026 phase with NTH-4 and APT-3 and left IND-3 for the third, so
  the meters left on AMR are APT-4 and CHL-2 (in every route's four) and IND-3 (seventh), and the pattern says nothing
  about the contested places; the AMI dates draw from a stream of their own, CHL-3's theft target rose from 577 to
  610 MWh to hold the margin (196.2), and the large load applications are numbered in each year's order received
  (the approved 2026 three had read LL-2026-01 to 03 against three-digit numbers everywhere else).
- 2026-11-12, runs: architecture 1 (the feeder energy balance and the four-feeder sweep) landed on both platform runs:
  both replayed the switching log with pole-tag matching, rebuilt the breaker gaps from the delivery point, computed
  hourly I2R on the GIS at current loads, measured the new loads on interval analogs and recomputed the lights from the
  inventory, every one a judgment the effort test had priced lost (paper 20.8 against about the thorough column); each
  move's data were complete, labelled and the field's textbook input. Architecture spent with its world; re-rooted to
  architecture 2 on what both runs named and waved through (`runs/arch1_triage.md`).
- 2026-11-12, stage 4: the determinism judge's first pass read target.zip before stage 5 had re-cut it, so it judged architecture 1's electric pack against architecture 2's gas prompt and blocks (NOT_DETERMINISTIC on input_files); both zips were cut from the current build and the judge re-run on the fresh cut.
- 2026-11-12, stage 4: a Word memo for the Commission in place of the deck, to clear voice-check's deliverable quota
  (a spreadsheet and a deck on 24 per cent of 21 prompts): it repeats task20's and task9's set, the last two builds
  (heart's repeat.deliverables), the reason the deck was drawn at filing, so the deck stays and the quota WARN is
  answered in the Pre-ship check.
