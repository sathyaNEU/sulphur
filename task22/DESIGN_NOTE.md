# task22: which of Brandvold Public Utilities' fourteen gas districts enter the 2027-2029 main replacement program, and where the 2027 meter changeouts go

Architecture 2, redesign loop 1 (2026-11-13), in the same world after the platform review of the same day
(`runs/arch2_review_2026-11-13.md`): both runs (49 and 46, average 47.5; the reviewer's own reward 71.0, stumped type
match failed) filed Downtown, Old Town, Riverside and Sundquist and lost only the unauthorized-use screen, so one
classification call carried the main replacement set. The judgment the runs lost stays and is split into two
independent ones; a third sits in another term of the balance; every judgment both runs made unprompted (the soil
temperature, the degree-day calendarization, the station repairs, the changeout pace: R71 to R74) is now a reflex
priced Right, and the 2027 changeout count is no longer asked. Architecture 1 (Delmont Power and Light's feeder
balance) was landed by both runs (`runs/arch1_triage.md`).

## Draw

Subdomain: Energy Systems & Utilities (gas distribution losses and the district gas balance; house task type
  distribution-losses-energy-balance; the client's nearest task types are load forecasting and grid reliability)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a reconciled table plus findings: each pressure district's monthly gas balance from October 2023 to
  September 2026, conformed on one real-gas basis from the systems that each see part of it (the regulator station
  correctors, the customer correctors, the cycle reads, the meter register, the accounts, the damage reports, the
  utility's own use), with the findings on top: the districts whose leak loss crosses the main replacement program's
  line, the premises where gas was taken without authorization, and the districts whose non-compensating meters the
  2027 changeout replaces
Weight: triage: 112 falls in use across 10,282 premises read one by one for their cause (a bypass or a furnace tap, a
  household away for the winter, a dual-fuel heat pump, a change of hands), beside every balance term put on one
  real-gas basis; the last two live builds put their weight on modeling (task25) and measurement (task20 v5)
Data-native sentence: nothing meters a district's leaks, so each district's leak loss is what is left after every
  other term, and here those terms come from correctors on two recording algorithms (the EVC-II station units carry the
  gas's supercompressibility, the four EVC-I station units and every customer corrector correct for pressure and
  temperature only) and from premise reads whose falls in use have three causes the reads alone do not name (a bypass
  or a furnace tap, a household away for the winter, a dual-fuel heat pump added to the furnace).
People: drawn with `guard.py names --geo us --seed 2208`: Marc Gilbert (the gas utility's engineering manager, who
  asks; not named in the prompt), Jocelyn Murray (the consultant who wrote the 2019 lost and unaccounted-for gas study).
Decision: before the Brandvold Utilities Commission adopts the 2027 capital budget in December 2026, the engineering
  manager files which of the fourteen pressure districts enter the 2027-2029 main replacement program (Rule 1: leak loss
  in the twelve months ending September 30, 2026 over 1.0 per cent of the gas delivered into the district) and where the
  2027 changeout replaces the meters that do not correct for gas temperature (Rule 2: under-registration over 3.5 per
  cent of their billed volume, 100 or more such meters); forward-facing (the programs are 2027's).

Card: `.claude/skills/fingerprint/cards/task22.json`, architecture v2 (the returned first cut kept in its lineage as
v2a), re-registered 2026-11-13 at WARN; skeleton severity none against everything on file, the lineage included. The
WARNs, answered: stated_rule_hard_construction (strategy risk) is analysis here, not a field read or a filed
procedure: every field and rule read correctly still leaves the supercompressibility to estimate and carry, and each
fall in use to read; the chain-near WARN against task8
v19 (the same answer shape) shares no lesson, mechanism or file role; driver near (0.20) is this slot's own returned
cut, whose deciding lessons all changed; set_over_threshold on five live builds is the honest form for a filed
per-district line; the repeats of task1 v5 (decision type, a spreadsheet and a deck, "which") are the decision's own
and the deck stays (a Word memo repeats task9 and task20). context_artifact redrawn from filed_standard (task1 v5 in
the window) to register: the meter register's stations and corrector accounts sheets are the stakeholder's file the
deciding work reads. Re-registering moved the window to task25, task20 v5 and task1 v5, so three more axes were
redrawn to the honester label that clears them: the weight to triage (above), the calibration form to
gold_standard_subsample (the dual-fuel controls rebates and the revenue protection cases are the verified subsamples
the classification is checked on; parallel_run_overlap repeats task25), the stump strategy to
stated_rule_hard_construction (the rules file leak loss and base conditions in full; the difficulty is building each
term on one basis; grain_or_unit repeats task24) and the forcing event to statutory_or_regulatory_filing (the
December 1 filing with the Commission; budget_or_appropriation repeats task25).

## Stump screen

Written at the redesign, before any code changed (`references/stump-screen.md`). Six candidates through the eleven
tests (1 off the closed page, 2 not a reflex, 3 nothing filed, 4 clean data, 5 two records, 6 the waved-through
assumption with its precedent, 7 a plausible shallower story, 8 across the data, 9 worth the call against the variant
battery, 10 the run's alternative ruled out by named data, 11 the golden can measure it). Magnitudes from the
prototype on the world's arrays: supercompressibility at 25 to 58 psig is 0.43 to 1.0 per cent of a volume (Dranchuk
and Abou-Kassem on the gate's gravity 0.59), so an EVC-I station understates its district's gas in by 0.4 to 0.6 per
cent and a process customer at 55 psig is billed 0.9 per cent short; a dual-fuel home whose furnace runs only below a
switchover near 0 F takes 15 to 30 per cent of its past heating, and booked as a tap it is about 60 Mcf of theft that
was never taken.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Four EVC-I station correctors and every customer corrector correct for pressure and temperature only; the twelve EVC-II stations carry the gas's supercompressibility, so Riverside's gas in is short 0.6 per cent and East Industrial's process customers at 52 to 55 psig are billed 0.9 per cent short | each corrector's recorded volume taken as the volume at base conditions, its factor checked against its own pressure and temperature, a check that cannot see the missing term (L28) | the EVC-II stations' recorded factors against their pressure and temperature, the gate's daily gravity, the gate balance | none | kept |
| Dual-fuel heat pumps added in 2025 leave the furnace only the coldest days: the winter use falls to the base on most days and comes back at the household's whole past heating slope below a switchover near 0 F | a fall in heating with the base kept booked as a furnace tap; fuel switching named and left untested (N36, both architecture 2 runs) | the read periods against the airport's degree days on the cold days only; a quarter of the conversions carry a dual-fuel controls rebate | none | kept |
| New snowbirds away from mid-November to mid-April: winter use falls with a setback heating response, the base goes, and May is back at the household's own weather response | every fall in use booked as gas taken without authorization (L47, N36, both architecture 2 runs) | May 2026's reads against the household's own response of the year before; the accounts file for a spring change of hands | 7 is partial: the May evidence is the same reads file at another season | kept |
| The 2027 scheduled changeouts at the crews' capacity rather than each job's own past delay (N38) | crews' shared capacity left out | the 2024-25 work orders by crew and week | 2 (dated works at the organisation's own record is measured dead: R73, R65) and 9 (the count is no part of the call) | dropped, and the count is no longer asked |
| The gas temperature model carried past the winter it was fitted on (N37) | the transfer named and left untested | the commercial correctors' gas temperatures all year | 9 (summer volumes are small: no district crosses either line) | dropped |
| Riverside's January gap filled at the station's interpolated share of the gate (run 1's own method, Riverside 1.85 on architecture 2) | a single-day hold-out certifying the fill | the gate less the other stations on the gap days | 2 (run 2 rebuilt the gap by conservation, R74, R39) | dropped as a trap; a recorded shortcut |

The three kept are independent: no one sentence rescues two of them (the supercompressibility sentence names the
correctors; the May sentence names the household's return; the cold-day sentence names the furnace's switchover),
and each moves the main set on its own (Stump factorial).

## Deep reasoning

Task type: distribution-losses-energy-balance (Energy Systems & Utilities, the house task type serving ETL; the client's
  nearest task types are load forecasting and grid reliability): a gas utility's district balance conformed from the
  systems that each see part of it, whose residual is each district's leak loss.
Domain test: every result is a quantity a gas distribution utility's measurement engineers compute: each district's
  sendout and each process customer's gas at base conditions on one real-gas basis, the gas taken through bypasses and
  furnace taps told from absence and from a dual-fuel heat pump's cold-day furnace load, and the leak loss left.
Swap: "which electric feeders enter the reconductoring program on their losses" keeps the balance's frame, but an
  electric meter records energy, there is no supercompressibility for a corrector to leave out, no base conditions
  and no furnace that takes the load below a heat pump's switchover, so none of the three deciding judgments has a
  counterpart.
Where the weight sits: R1 and R2, measurement: the corrector customers are a third of the system's gas and East
  Industrial's process customers most of its gas in, so their basis decides East Industrial; Riverside's single station
  is an EVC-I unit; and 112 premises' falls in use have to be read one by one for which of four causes each is.
Layer 1: the regulator station correctors' communication gaps (Riverside's January 12 to 25, 2026), Lakeview's failed
  pressure transducer (the corrector substituted 25 psig for 35 from December 4 to 21, 2025) and Westgate's stuck
  temperature transmitter (February 3 to 11, 2026); the AMR reads on twenty business-day cycles with estimated reads
  trued up by the next actual, four-dial rollovers, multipliers, final and initial reads at the 2024 and 2025 exchanges
  and special reads at account changes; the June 2025 extract re-run that repeats a month of rows; blank compensation
  flags (the model code tells); the customer correctors' fixed-factor days; the airport's and the soil station's
  missing days. None decides a result: the station repairs are graded inside R1 and made by reflex (R74).
Not one thing: three judgments each move the main set on their own and none is enough alone: every corrector as
  recorded drops Riverside and adds East Industrial; every fall booked as theft drops Lakeview; the dual-fuel homes
  booked as taps drop Riverside and Sundquist; the route both runs took (all three hurried, every reflex right) files
  Downtown, East Industrial and Old Town, and each one fixed alone on it still files a wrong set.
One-fact test: the most useful single sentence is "four of the station correctors and every customer corrector correct
  for pressure and temperature only; at 25 to 58 psig the gas is not an ideal gas"; on the careful pass it rescues R1
  (1 of 6) and no set; the May sentence and the cold-day sentence rescue none alone (effort.json hints, computed).
Not semantics: every field, code and clause read correctly (the corrector models, the delivery pressures, the read
  types, the pressure factor, the rules' base conditions, leak loss and gas taken without authorization) still leaves
  the supercompressibility to estimate and carry to each corrector's pressure and temperature day by day, and each fall
  in use to read on May's response and on the cold days' response.
Not rule application: the program rules file what leak loss is, the base conditions, the two lines and the 100 meters;
  no filed procedure says that a corrector leaves a term out, what supercompressibility the gas had, or whether a fall
  in use was a theft, an absence or a heat pump.
Estimand: the program rules, Resolution 2026-11 (leak loss: gas delivered into the district less the gas its customers
  took through their meters, own use, third-party damage and gas taken without authorization, every quantity at base
  conditions 14.73 psia and 60 F; a meter's under-registration the gas it delivered at base conditions less its billed
  volume; Rule 1; Rule 2; Rule 3); the gas rate schedules (the billing volume, Schedule G-3 billed on the corrector's
  volume corrected for the pressure and temperature it measures); the prompt (the monthly balance's columns and window,
  each district's leak loss share for the program's twelve months, the premises where gas was taken without
  authorization with how much each took).
No decoy: nothing is written to carry a wrong answer: the 2025 logger study memo reports its own fit of its own data,
  which reproduces exactly (checks.py R4); the 2019 consultant's monthly-mean method is the incumbent's honest
  computation for 2019; the tariff describes Schedule G-3's billing truthfully; no document ranks districts; the
  rebates file records equipment, never a finding.
No replay: no result re-derives a published figure; the annual LAUF report's billed-basis percentages are the
  incumbent figure the chain supersedes.
Pinned: every rival a careful analyst could defend is run on the cut pack and lands inside each graded band with the
  golden sets (checks.py R7): supercompressibility from Hall and Yarborough or fitted on the EVC-II stations' own
  records, each read spread on a base-and-degree-day fit of its district's sendout, the outdoor gas temperature tied to
  the commercial correctors', and the three together; the 12-variant battery and the 13 conventions of the screen file
  one main set, one changeout set and 16 premises; the sets hold under the air coefficient and the damage, own use and
  unauthorized volumes 20 per cent either way, the indoor temperature 2 F either way and the gas's gravity 0.01 either
  way. Every district sits 12 per cent or more from the 1.0 line (nearest Riverside 1.17 and Halvorsen 0.83) and every
  eligible district 12 per cent or more from the 3.5 line (nearest Airport 3.02).
Run forecast: a strong run loses R1 by a self-confirming check (each corrector's factor checked against its own pressure
  and temperature, which reproduces the recorded volume), R2 and R5 by dismissed own evidence (the falls split by
  signature, then every one booked: L47; fuel switching named and left untested: N36), R3 and R4 with them, and earns
  R6 by reflex (R71).
Strategy label: OWN (no client strategy carries a gas balance; the client's emissions-table ETL strategy is the nearest
  by type and shares no step).
Depth level: 5 on the client's scale: three independent judgments each move the main set (Stump factorial), and eight
  shortcut routes land on six different wrong sets.
Lesson: a balance's residual is only as good as the basis its terms share: two corrector algorithms on one system put
  part of the gas off the base-conditions basis, and the shortfall grows with each instrument's own pressure, so the
  residual moves district by district until every term is on the real-gas basis the better instruments already carry;
  and a fall in use has lawful causes with their own signatures (a household home again in May, a furnace that
  answers only the coldest days) that the falls' size alone cannot tell from theft.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each district's gas in and its corrector customers on one real-gas basis: Riverside 128,796 Mcf and College Hill 305,841 in the twelve months to September 2026, East Industrial's corrector customers 397,372, Lakeview 13,536.7 in December 2025 | assembly-reconciliation | the station and customer correctors' uncorrected volume, pressure and temperature, the EVC-II stations' own factors, the gate's gravity; the rules' base conditions | twelve months within 0.3 per cent, December within 1.5 per cent | self-confirming check: each corrector's factor checked against its own pressure and temperature reproduces the recorded volume, so Riverside 128,005 and East Industrial's customers 395,152 | - | Ask 1 |
| R2 | the premises where gas was taken without authorization in the twelve months: 16, with 18 accounts | exploration-triage | each premise's reads against its own weather response the year before, May 2026, the cold days' read periods, the accounts file; the rules' bypass or interference | each within 1 | dismissed own evidence: the falls split by signature, then every one booked, absences and dual-fuel homes with them (101 premises) | - | Component 1 |
| R3 | each district's leak loss in the twelve months as a share of its gas in: Riverside 1.17, Lakeview 1.21, Sundquist 1.35, East Industrial 0.67, Halvorsen 0.83, Elm Grove 0.67, College Hill 0.78, Downtown 1.35 | decomposition-attribution | the rules' leak loss; R1, R2, own use, the damage reports | each within 0.10 points | dismissed own evidence: the residual on the correctors as recorded and every fall booked (Riverside 0.18, Lakeview 0.19, Sundquist 0.64, East Industrial 1.14) | R1, R2 | Component 2 |
| R4 | the districts that enter the 2027-2029 main replacement program: Downtown, Lakeview, Old Town, Riverside and Sundquist | synthesis | Rule 1 | exact set | dismissed own evidence: Downtown, East Industrial and Old Town | R3 | Recommendation |
| R5 | the gas taken without authorization, by district: Elm Grove 464 Mcf, East Industrial 1,330, Sundquist 266, Old Town 157 | exploration-triage | each premise's reads against its own weather response the year before | each within 25 per cent | dismissed own evidence: every fall booked (Elm Grove 709, Sundquist 730, Old Town 459) | - | Ask 2 |
| R6 | the districts where the 2027 meter changeout goes: Elm Grove, Halvorsen, Lakeview, North End, Prairie Rose, Riverside and Sundquist | synthesis | Rule 2; the loggers, the soil station, the register | exact set | method shortcut: the logger study's air line puts Airport, College Hill and East Industrial over 3.5 (the careful pass earns the set by reflex, R71) | - | Recommendation 2 |

Carry-forward: R1, R2, R5 and R6 stand on inputs of their own (the correctors and the gate; each premise's reads; the
loggers and the register); R3 falls with R1 or R2, R4 with R3. A run that misses the real-gas basis keeps R2, R5 and
R6; one that books every fall keeps R1 and R6; one that books the dual-fuel homes as taps keeps R1 and R6.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| four EVC-I station correctors and every customer corrector correcting for pressure and temperature only | constructed (the simulated correctors, the utility's 2021 metering program) | no: four stations in four districts and all 65 customer correctors in fourteen; it decides Riverside and East Industrial and moves Old Town, Downtown, College Hill and Airport without deciding them | a targeted query (each station's recorded factor against its pressure and temperature) read with the gas's physics, checked by the gate balance | estimation: the supercompressibility fitted on the EVC-II stations or taken from a correlation on the gate's gravity, carried day by day to each corrector's own pressure and temperature | keep (one of three stumps; alone a single-fact stump) |
| dual-fuel heat pumps added to gas-heated homes in 2024 and 2025 | constructed (the simulated households) | no: 52 homes in thirteen districts, 44 of them converted in 2025 (2.6 per cent of Sundquist's homes, under 1 per cent elsewhere); it decides Sundquist and Riverside together | modelling: each fall's read periods against the degree days of the cold days only | modelling | keep |
| new snowbirds, away from mid-November to mid-April for the first time in 2025-26 | constructed (the simulated households) | no: in ten districts (Lakeview 17 of 58); it decides Lakeview only | modelling: each fall's May 2026 against the household's own weather response | modelling | keep |
| bypasses and furnace taps from the autumn of 2025 | constructed (the estimand's own term) | no: six districts; it decides Elm Grove only when nothing is subtracted | modelling: each premise against its own weather response | modelling | keep |
| the 2025-26 deep snow and the January 2026 cold week | constructed (the simulated weather) | no: every outdoor meter and every station; it moves no set on the golden family (R71 is a reflex) | modelling: the loggers on the soil | modelling | keep |
| the stations' faults | constructed (the simulated correctors) | no: random communication gaps on every station, three named faults; graded in R1 | a targeted query: the stations against the gate | routine | keep, R1 only |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each district's gas in and its corrector customers on one real-gas basis | Missed | Missed | Right |
| R2 the premises where gas was taken without authorization, and their accounts | Missed | Missed | Right |
| R3 each district's leak loss in the twelve months to September 2026, per cent of its gas in | Missed | Missed | Right |
| R4 the districts that enter the 2027-2029 main replacement program | Missed | Missed | Right |
| R5 the gas taken without authorization, by district | Missed | Missed | Right |
| R6 the districts where the 2027 meter changeout goes | Missed | Right | Right |
| Roughly | 0 of 6 | 1 of 6 | 6 of 6 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the passes are the generator's own routes on
  the cut pack: the quick pass bills taken in the month read, the stations as recorded, no temperature correction and
  nothing subtracted; the careful pass is the route both architecture 2 runs took, every reflex right and the three
  stumps hurried; the golden)
Largest single hint: "Four of the station correctors and every customer corrector correct for pressure and temperature
  only; at 25 to 58 psig the gas is not an ideal gas."; rescues 1 of 6 results
Pair estimate: 14.0 (the careful pass earns R6 and the instruction-following share; every lost cell cites a precedent
  of its own class: L28, L47, N36)

## Stump factorial

Reflex route: the route both architecture 2 runs took (`runs/arch2_run1.md`, `arch2_run2.md`): every reflex right
  (the soil-aware gas temperature R71, degree-day calendarization R72, the station repairs R74, the rebated homes set
  aside by the rebates file) and every stump hurried (every corrector as recorded, every fall booked as theft, no
  cold-day test); it files Downtown, East Industrial and Old Town, which misses the call.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| J1 a household away for the winter told from a tap by its heating response in May | stump | every fall booked as gas taken without authorization | L47, N36 | Downtown, Old Town, Riverside and Sundquist (Lakeview out) | Downtown, East Industrial, Lakeview and Old Town; no result rescued | no |
| J2 a dual-fuel heat pump told from a furnace tap by its cold-day response | stump | every lost heating response booked as a furnace tap | N36 | Downtown, Lakeview and Old Town (Riverside and Sundquist out) | Downtown, East Industrial, Old Town and Sundquist; no result rescued | no |
| J3 every corrector put on the real-gas basis | stump | every corrector's volume taken as recorded | L28 | Downtown, East Industrial, Lakeview, Old Town and Sundquist (Riverside out, East Industrial in) | Downtown and Old Town; R1 rescued | yes |
| J4 the gas temperature in the buried services on the soil | reflex | the logger study's air line | R71 | Downtown and Old Town | - | - |
| J5 the cycle reads carried to months on a weather shape | reflex | each read spread evenly | R72 | Downtown, Halvorsen, Lakeview, Old Town, Riverside and Sundquist | - | - |
| J6 the stations' faulty days rebuilt from the gate | reflex | the faulty days as recorded | R74, R39 | Downtown and Sundquist | - | - |

Level: 5: three necessary stumps, none sufficient, the single drops on three distinct wrong sets (effort.py, measured).

## Data provenance

Source: generated by task22/generator from a simulated municipal gas distribution system (seed 22062): daily weather
  for three winters (the snowless 2023-24, the thin cover of 2024-25 and the deep snow of 2025-26 with a cold week in
  late January) and the soil under it, the gate analyser's daily gravity, fourteen pressure districts fed through
  sixteen regulator stations from one city gate (twelve EVC-II correctors carrying the gas's supercompressibility, four
  EVC-I units correcting for pressure and temperature only), about 10,300 premises with their meters, daily use by
  premise driven by the weather with base load, students, snowbirds, vacancies, furnace rebates and dual-fuel heat
  pumps, what each meter registered at its gas's temperature, AMR cycle reads with the billing system's estimates, 65
  corrector customers (seven process plants at 40 to 55 psig) on EVC-I units, bypasses and furnace taps, leaks,
  third-party damage, station heaters, the 2024-25 loggers and the changeout work orders.
Behaves like the real thing: natural gas at 25 to 58 psig and 30 to 60 F has a compressibility of 0.987 to 0.994 at
  gravity 0.59, so its volume at base conditions exceeds the ideal-gas correction by 0.4 to 1.0 per cent (Dranchuk and
  Abou-Kassem on Sutton's pseudo-critical properties, as AGA practice gives); small utilities' electronic volume
  correctors are commonly configured for pressure and temperature only; a dual-fuel heat pump with a gas furnace backup
  burns gas only below its switchover; first-year snowbirds leave in November and are back by late April; gas at an
  outdoor meter set follows the soil at service depth, and snow cover holds the soil near freezing.
Genuine patterns: (1) heating-driven use with a base load and a thermal carry-over from the day before (2) three
  different winters and their soils (3) student rentals emptied over the break and the summer, snowbirds every winter,
  account turnover with vacant spells (4) furnace replacements lowering a household's heating slope; dual-fuel
  conversions removing most of it (5) the 2024 and 2025 changeout programs, faster outside than inside (6) leaks
  growing as the mains age and with frost in cast iron districts (7) third-party damage concentrated in the growing
  districts (8) the gas's supercompressibility rising with each instrument's pressure and falling with its temperature
Problems by process: correctors' communication failures, a failed pressure transducer and a stuck temperature
  transmitter; AMR modules going quiet and the billing system estimating; rollovers, multipliers and exchanges; the
  June 2025 extract re-run; register flags left blank; the customer correctors' fixed-factor days; the weather stations'
  missing days; the correctors' recorded pressures rounded to a tenth.
Breadth: 22 files (three large CSVs of 18,577 to 421,786 rows, a daily weather and a daily soil record, seven
  workbooks, four PDFs, three distractors: the CNG station's sales, the supply invoices and the 2024-25 work orders),
  fourteen districts, sixteen stations, 10,282 premises and 65 corrector customers, so deciding which records close
  each district's balance, and on which basis, is work.

## Template check

Chain signature: assembly-reconciliation, exploration-triage, decomposition-attribution, synthesis, exploration-triage,
  synthesis
Question form: which (which districts enter the program, which get the changeout)
Nearest build: task8 v19 (the same answer shape: a reconciled table) equates test scores across instruments through a
  common measure; this build puts a gas balance's terms on one real-gas basis and reads falls in use for their causes
  before a filed per-district line; architecture 1 of this slot closed an electric balance whose technical term was a
  network computation; the returned cut v2a turned on the gas temperature at the meters (now a reflex). Abstraction
  sentence: none writable against any of them; the guard's skeleton read is severity none against everything on file.

## Frontier check

Precedents: R1 L28 (a check that cannot see the problem certified the estimate); R2 L47 (the falls split by signature,
  then every one booked, both architecture 2 runs), N36 (fuel switching, absence and changed occupants named as
  explanations and left untested, both runs); R3 L47, N36, L28; R4 L47, N36, L28; R5 L47, N36.
Shallow path checks: R1: each corrector's corrected-to-uncorrected ratio matches its own pressure-and-temperature factor
  exactly, so a run that checks the correctors (both runs did, on the fixed-factor days) certifies the recorded
  volumes; only the EVC-II stations' factors (another instrument at the same pressures) and the gas's physics show the
  term the EVC-I units leave out. R2 and R5: booking every fall reconciles to the drop in billed volume and finds every
  real bypass and tap; only May 2026 (another season, when the household is home) and the cold days' read periods
  (another grain) tell the absences and the dual-fuel homes apart. R3 and R4: the careful residual is positive in
  twelve districts and passes the published LAUF bridge; only the two terms above move it.
Assumption made false: that a corrector's corrected volume is the gas's volume at base conditions (the tariff bills it
  so): false here because four station correctors and every customer corrector leave the gas's supercompressibility
  out, which the EVC-II stations' records show at 0.43 to 0.97 per cent by pressure; tested through the stations' own
  factors and the gate balance. And that a fall in heating with the base kept is a furnace tap (N36 named it): false
  for 43 of the falls, homes that added dual-fuel heat pumps, whose furnace takes the whole past load on the coldest
  days (31 found by the cold days' read periods, 12 also on the rebates file); tested on the read periods against the
  cold days' degree days and on the rebates file.
Forcing: the line is each district's leak loss against 1.0 per cent of its gas in (Rule 1) and each eligible district's
  under-registration against 3.5 per cent (Rule 2); the golden family (four rivals and their combination) and the
  12-variant battery file both golden sets, the nearest districts to Rule 1's line Riverside 1.17 (battery 1.17 to
  1.25, perturbations 1.11 to 1.24) and Halvorsen 0.83 (battery to 0.86, perturbations to 0.91), to Rule 2's Airport
  3.02; the shortcuts land on the other side (every corrector as recorded: Riverside 0.57, East Industrial 1.14; every
  fall booked: Lakeview 0.26; the dual-fuel homes as taps: Riverside 0.93, Sundquist 0.61; the careful route: Riverside
  0.18, Lakeview 0.19, Sundquist 0.64, East Industrial 1.14); the air coefficient, the indoor temperature, damage, own
  use, the unauthorized volumes and the gas's gravity moved by their defensible spreads all hold.
Noun swap: the nearest skeletons on file (skeleton.py check: task4 arch 12, task4 v13, task9 v3, this slot's v2a and
  v1) share at most one supporting lesson and no decision form, answer pattern, mechanism or detection; swapped into
  task4 v13 (kegs, a fleet balance) the deciding moves (a corrector's missing supercompressibility, a furnace's
  switchover, a household home in May) have no place; severity none.
Closed strategies: the call turns on conservation_residual_attribution (every term of a balance on one basis before the
  residual is read), behavioural_response_measured (the cold-day threshold of a dual-fuel furnace) and the reading of
  each fall for its cause, all off the client's closed page; the nearest card is "The instrument changed (drift or step
  change)", and the mechanism and fix differ: nothing changed over the record (every EVC-I unit has corrected for
  pressure and temperature only since 2021, beside EVC-II units that never did), no break is found against an unaffected
  series, and the fix is the gas's physics carried day by day to each instrument's own pressure and temperature. The
  chain keeps no closed lesson as a step (skeleton.py closed task22: 0 of 5 lessons closed).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | leak loss in a district | gas in less customers, own use, damage and gas taken without authorization; gas in less billed volume | the rules' definition | the program rules, section 2 |
| SF2 | the twelve months | October 1, 2025 to September 30, 2026 by the days gas flowed; bills read in the window | the days gas flowed | the rules' "in the twelve months ending September 30, 2026" and the prompt's calendar months |
| SF3 | base conditions | 14.73 psia and 60 F; the meter's own conditions | 14.73 psia and 60 F | the rules |
| SF4 | the gas day | named by the date it begins at 9:00 a.m.; the calendar day | its start date | the gas rate schedules, section 4; same call: a nine-hour shift is inside every band |
| SF5 | the billed volume | registered ccf times the pressure factor; times a temperature factor too | the pressure factor | the gas rate schedules, section 2 |
| SF6 | a meter's under-registration | the gas it delivered at base conditions less its billed volume | the rules' definition | the rules, section 2 |
| SF7 | Rule 2's ratio and eligibility | under-registration over the non-compensating meters' billed volume, 100 or more such meters; over all meters | the rules' ratio | the rules' Rule 2 |
| SF8 | a meter whose compensation flag is blank | its model code's compensation; non-compensating | the model code | the register's meter models sheet (and checks.py R2: either reading holds every set) |
| SF9 | gas taken without authorization | through a bypass or interference; any fall in use | bypass or interference | the rules, section 2 |
| SF10 | a corrector's fixed-factor day | its uncorrected volume at the account's own ratio; as recorded | the account's own ratio | same call: inside every band (checks.py R2) |
| SF11 | own use in a district | the station heaters; with the gate line heater | the station heaters | the rules (the gate heater sits in no district) |
| SF12 | damage losses | the reports' estimates; recomputed | the reports' estimates | the rules' "as reported"; 20 per cent either way holds |
| SF15 | a premise's district | the register's pressure district | the register | the register |
| SF16 | a corrector customer's district | the corrector sheet's pressure district | the corrector sheet | the register |
| SF17 | a fall in use | a run of three or more months under 0.40 of the premise's own weather response, reaching the heating season, outside vacancies and exchanges; cuts 0.35 to 0.45, runs of 3 or 4 | the golden's | same call (checks.py SF17 to SF23: 16 premises, both sets) |
| SF19 | the leak loss share's window | the program's twelve months; the three years; each month | the program's twelve months | the prompt's "for the program's twelve months" and Rule 1 |
| SF20 | a corrector customer's gas at base conditions | the corrector's billed volume (pressure and temperature); the real-gas volume at 14.73 psia and 60 F | the real-gas volume | the rules (every quantity at base conditions; under-registration is delivered less billed); the EVC-II stations and the gate carry the gas on that basis |
| SF21 | supercompressibility | Dranchuk and Abou-Kassem; Hall and Yarborough; fitted on the EVC-II stations; Papay's short form | the first | same call for the first three (checks.py R7); Papay ruled out: it misses the EVC-II stations' own recorded factor by more than twice the others (checks.py SF21), and still files the golden sets |
| SF22 | a household away for the winter | May 2026 at 0.7 or more of its own weather response; 0.6 to 0.8 | 0.7 | same call; every booked tap is under 0.6 in May, every household away over 0.8 (checks.py SF22) |
| SF23 | a dual-fuel heat pump | a fall whose read periods answer the cold days' degree days at 0.3 or more of the household's own past slope with the best switchover at or below 10 F; 0.2 to 0.4, 5 to 15 F | the golden's | same call; every booked tap's cold-day slope is under 0.1, every dual-fuel home's 0.4 or more (checks.py SF23) |
| SF24 | the unit of the count | premises; accounts | premises, each with its accounts | the prompt's "any premises where gas was taken without authorization" |
| SF25 | a premise with a dual-fuel controls rebate | no theft; screened like any other | no theft | the rebates file's dated equipment record (checks.py SF25) |
| SF26 | the 2027 scheduled changeouts | not asked | not asked | the prompt; Rule 3 files the scheduled districts |
| SF27 | a station's faulty days | the gate less the other stations; the station's interpolated share of the gate | the gate less the other stations | named data: on Riverside's gap days every other station is metered, so the gate balance pins Riverside; the share fill moves Riverside's twelve months 0.4 per cent (a recorded shortcut, run 1's method) |

## Pinning list

Every constant the golden's estimator uses that the world also holds (determinism-check §1).

| Constant | Golden value | Home |
|---|---|---|
| base conditions | 14.73 psia and 60 F | lauf_reduction_program_rules_2026.pdf, section 2 |
| atmospheric pressure at Brandvold | 13.98 psia | solved from the customer correctors' own ratios in commercial_correctors_daily_2023-09_2026-10.csv (the median gas day), and implied by the pressure factor in gas_rate_schedules_2026.pdf |
| the pressure factor | 0.9663 | gas_rate_schedules_2026.pdf, section 2 |
| the gas's specific gravity | 0.585 to 0.599 day by day | city_gate_station_daily_2023-09_2026-10.csv |
| supercompressibility | Dranchuk and Abou-Kassem on Sutton's pseudo-criticals | the estimator family's measured spread (Hall and Yarborough and the EVC-II stations' own fit within 0.0004 of it on the stations in regulator_station_correctors_daily_2023-09_2026-10.csv) |
| which correctors leave it out | RS-1, OT-2, DT-2, CH-1 and every customer corrector | measured: each corrector's recorded factor against its pressure and temperature in regulator_station_correctors_daily_2023-09_2026-10.csv and commercial_correctors_daily_2023-09_2026-10.csv; the models in premise_meter_register_2026-11-02.xlsx |
| the outdoor gas temperature | soil at 20 inches + 0.181 x (air - soil) + 1.75 F below 45 F | fitted on gas_temperature_study_loggers_2024-11_2025-04.csv; the measured spread of the soil and corrector-tied rivals |
| the indoor gas temperature | the indoor loggers on the soil at 40 inches | fitted on gas_temperature_study_loggers_2024-11_2025-04.csv |
| the dual-fuel switchover | estimated per premise, best of -10 to 15 F | the read periods in amr_meter_reads_2023-08_2026-10.csv against brandvold_regional_airport_daily_2023-08_2026-10.csv; the measured spread of the 5 to 15 F caps |
| the absence's return | home by May 2026 | the reads in amr_meter_reads_2023-08_2026-10.csv; the measured spread of the 0.6 to 0.8 cuts |
| the collapse screen | 0.40 of the premise's own response, three months into the heating season | the measured spread of the 0.35 to 0.45 cuts and runs of 3 or 4 |

Variant battery: 12 variants of the modelled transports (supercompressibility from Dranchuk and Abou-Kassem, Hall and
  Yarborough or the EVC-II stations' own fit, each read spread on the sendout or a degree-day fit, the outdoor gas
  temperature tied to the soil or to the commercial correctors: the full cross) file one answer, the golden main set and
  the golden changeout set; 13 conventions of the screen book the same 16 premises and file the same sets.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the fourteen pressure districts; every premise and corrector customer the register places in each |
| 2 | Unit of account: the district, by the gas day for gas in and by the day for customers' use; the premise for gas taken without authorization |
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
| 13 | Order of operations: rebuild the stations, put every corrector on the real-gas basis, build the read periods, spread them, correct for temperature, read the falls, subtract |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: the re-run's rows are exact copies, kept once |
| 16 | Identity normalisation: premises to districts by the register; meters to compensation by flag or model code; stations to corrector models by the stations sheet |
| 17 | Netting against gross: a true-up after an estimate nets inside the actual-to-actual period |
| 18 | Dimensional units: Mcf at base conditions on the real-gas basis; per cent of gas in; per cent of billed volume |
| 19 | Code and status semantics: read types, alarms and corrector status as each system writes them |
| 20 | Integerisation: premises, accounts and meters whole |
| 21 | Clause scope: Rules 1 and 2 apply to every district alike; Rule 3 to the plan's two districts |
| 22 | Forward window contents: the 2027-2029 program and the 2027 changeout, nothing else |

## Literal reader

Executing the rules word for word: each district's leak loss is its regulator stations' gas at base conditions, less what
its customers took through their meters at base conditions, the station heaters, the damage reports and the gas taken
through bypasses or interference, over the twelve months ending September 30, 2026; districts over 1.0 per cent enter
the program; the changeout goes where the non-compensating meters' under-registration exceeded 3.5 per cent of their
billed volume with 100 or more such meters. A reader who takes every corrector's volume as recorded and books every
fall in use designates Downtown, East Industrial and Old Town; neither is another reading of a filed term (the rules
file base conditions and theft as bypass or interference), each is an easier method on the same filed estimand.

## Prompt contract

A voice rewrite keeps: the question (which districts enter the 2027-2029 main replacement program and which get the
2027 meter changeout); the monthly balance from October 2023 to September 2026 with its columns (gas in, the billed
volume of the gas its meters took that month, what the meters without temperature compensation under-registered, the
corrector customers, own use, damage, gas taken without authorization, the leak loss left); for the program's twelve
months, each district's leak loss as a share of its gas in and any premises where gas was taken without
authorization, with how much each took; a spreadsheet and a short deck for the Utilities Commission. It never adds a rounding
instruction, a method (no supercompressibility, compressibility, real gas, corrector model, heat pump, dual fuel,
switchover, snowbird, May, cold day, soil, logger, air, degree day, bypass or tap), a warning, an attached file's name,
a role, or a count the data hold, and it asks for no count of the 2027 scheduled changeouts.

## Pre-ship check

- Bar re-read on the built pack: six results across four areas (assembly and reconciliation, exploration and triage,
  decomposition and attribution, synthesis), each pinned by a filed sentence (Resolution 2026-11's definitions and
  Rules 1 to 3, the rate schedules' billing volume) and the data, with the bands the answer blocks state; checks.py 162
  of 162; verify.py 21 of 21 on its own path (its own real-gas fit on the EVC-II stations).
- Truth replay: the golden's 16 premises are exactly the simulation's bypasses and furnace taps; every fall read as a
  dual-fuel home is one; every graded R1 and R5 cell is inside its band around the simulation's; every district's leak
  share within 0.15 points of the simulation's, which designates the same five districts.
- Effort test against effort.py: quick 7.0, careful 14.0 (1 of 6), thorough 100; the largest hint rescues 1 of 6; eight
  shortcuts land on six distinct wrong sets; the factorial at level 5.
- Forcing: Rule 1's nearest districts Riverside 1.17 and Halvorsen 0.83, Rule 2's Airport 3.02; the golden family, the
  battery and ten perturbations file both golden sets.
- Stage 4: the determinism judge DETERMINISTIC and APPROVE on the first cut (station factors, Riverside's and Lakeview's
  gas in and East Industrial's corrector customers recomputed within their bands; the two Riverside gap days with a
  second station down and the Lakeview transducer days closed by the alarms the pack files), re-judged once on the final
  cut after the prompt's "any premises" and the rebates' numbering in date order (determinism_check_report.md). The
  isolated leak reader quoted no sentence that hands over a priced step; its LEAK was the rules' thresholds and Rule 3's
  carve-out, the decision lines the governing document must file, ruled harmless (leak_check_report.md, Solver's-eye
  read). It took Schedule G-3's corrected volume as already at base conditions: the hurried reading R1 prices.
- leak.py REVIEW lines, each harmless: the rules' 1.0 is Rule 1's filed line; the stump-vocabulary hits in the rate
  schedules, the memo, the rules and the 2019 report are the field's own nouns (station, pressure, corrector, factor,
  conditions, district names), none naming the move; the memo, the register, the damage reports and the own-use sheet
  name districts beside raw figures and rank none on the decision question (the reader agreed); the 2027 plan's dates
  are a forward plan's; the prompt's shell quota (a question in "which", a spreadsheet and a deck) is the decision's
  own form, answered in the Draw.
- The reviewer's three fixes: premise 3135379 (Old Town, a furnace tap from December 20, 2025) is among the 16 (the
  base test that called it an absence is gone; the May test reads it); the step-by-step's counts are the screen's own
  on the golden path (112 falls: 9 bypasses, 7 taps, 52 households away, 43 dual-fuel homes, 1 change of hands); the
  prompt counts premises and the golden lists each premise's accounts (16 premises, 18 accounts).

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
- 2026-11-13, review: architecture 2's first cut (the gas temperature on the soil, the reads on each district's
  sendout, diversion told from new snowbirds, the changeout pace) returned: both runs made the temperature, the
  calendarization, the station repairs and the pace unprompted and lost only the unauthorized-use screen, so one
  classification call carried the main set (reward 71.0, stumped type match failed; runs/arch2_review_2026-11-13.md).
  Redesigned in the same world: the screen split into two independent judgments beside a third in another term.
- 2026-11-13, redesign: telling a dual-fuel home from a tap on the winter months' linear heating fit: the convex
  cold-day response reads as a reduced heating response with the base gone, so the homes classed as absences and the
  judgment moved no set; the screen reads absence on May's return and the dual-fuel homes on the cold days' read periods.
- 2026-11-13, redesign: the absence test on May and October 2026 together: October 2026 is only partly read by the
  extract, so households home in October read low; May alone separates them.
- 2026-11-13, redesign: the 2027 scheduled changeouts at the crews' capacity (run 2 named shared crews as untested):
  dated works carried at the organisation's own record of past works is measured dead (R73, R65) and the count is no
  part of the call; the count is no longer asked.
- 2026-11-13, redesign: the station gap filled at the station's interpolated share of the gate as a golden-family
  rival: on Riverside's gap days every other station is metered, so the gate balance pins Riverside and the share fill
  moves its twelve months 0.4 per cent; it stays a recorded shortcut (run 1's method on architecture 2).
