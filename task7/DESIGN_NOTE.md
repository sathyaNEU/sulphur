# task7: which of Platte Ridge PPD's 24 feeders receive voltage optimisation in the 2027 capital programme

## Draw

Subdomain: Energy efficiency & demand response evaluation (energy-systems-utilities, efficiency-savings-verification)
Analysis type: Experiment & Causal
Answer shape: a flagged set with the evidence (the feeders funded, each feeder's yearly saving at the substation with its band, and the trial's measured response behind it)
Weight: modeling: each feeder's yearly saving at the substation is built from three models fitted on the pack (its load's makeup against the weather and the survey, its far end hour by hour, its losses against current squared) and the trial's measured response; no record holds it (the trial ran on eight feeders in spring and autumn); the last two builds sat in assembly (task22) and investigation (task9), and hard-to-measure was redrawn because task20 holds it
Data-native sentence: the randomised trial measured the energy response to a voltage cut on eight feeders on the days its regulators actually ran, the tap changers move every feeder's voltage a few thousand times a year but only for a half-hour read that thermostats undo, the customer meters miss the line losses and the far-end meters set how far each feeder can go, so each part of the yearly saving has to be assigned to the record that sees it
Guard (registered card, 2026-11-13): gap redrawn from population to objective (population with G13 and a designated set repeats task8's lineage), forum board_of_directors (the District's board approves the capital programme; executive_team and line_manager_or_team repeat task9 and task13); WARN repeat.deliverables docx+xlsx (task9): a planner's workbook and memo is what this reader uses; WARN house_lesson position_on_network_effect (task9, task13): a supporting step here (the far end caps the volts), the call turns first on instrument_noncompliance; WARN house_shell set_over_threshold: the decision is a funded set against each feeder's own cost under VO-1 2.1, no other form is honest
People: Joseph Harmon (manager of distribution engineering, owner of VO-1), Mary Wilson (system planning, whose workbook and memo the golden are), Bruce Hart (finance), Anthony Harris (GIS and register) (`guard.py names --geo US --seed 1113`). None appears in the prompt.

Architecture 12, 2026-11-13, a new world on the author's word after architecture 11 (Hollins Creek's EV charging default) was landed by the platform run on every graded result (task7/runs/arch11/run1.md: the night-by-night Stagger replay a reflex under EV-4 4.3, the Sequence rule written in the proposal). Built to the stump factorial from the draw: five methods the data force, each prototyped on paper and then on the generator's own estimators before the pack was cut.

## Stump screen

Written at the draw on 2026-11-13, each candidate prototyped in a scratch simulation against the world's truth before any generator code (task7/runs/arch11/run1.md supplies the waved-through assumptions).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| the trial read on the volts its regulators took off, not on the day's assignment | the response taken at the scheduled 4 per cent (N24, L04) | the pilot regulator log against the bus SCADA, quarter-hour | none | kept (J1) |
| an untested feeder's response from its own makeup, not the trial feeders' average | each feeder like the trial feeders (N25, L15) | each feeder's load against the weather, the appliance survey | none | kept (J2) |
| the response carried hour by hour through the year, thermostatic load giving its energy back | a spring and autumn figure carried flat (N12, L15) | the year's load against the weather, the survey's resistive heat and water heaters | 1 (near the closed seasons card: answered in Closed strategies) | kept (J3) |
| the volts each feeder can give from its far-end meters | the trial's 4.8 V scaled to every feeder (N01, L17) | the bellwether meters' hourly minimum voltages | none | kept (J4) |
| the losses from current squared, not the annual report's rate added in proportion | an unmeasured component spread in proportion (N21, L22) | the substation revenue meters against the customer sums, the register's ohms | none | kept (J5) |
| Stagger-style persistence or random-start correlation, a GIS mis-mapping of coordinated groups, offline fallback nights | tried in architecture 11's world | - | 3 (filed text contradicted, a literal replay catches it, too weak) | dropped (Tried and rejected) |

## Deep reasoning

Task type: efficiency-savings-verification (Energy efficiency & demand response evaluation), which serves Experiment & Causal
Domain test: every result is a conservation-voltage-reduction measurement and verification quantity: a randomised on/off trial's energy response per volt, each feeder's achievable voltage reduction against the service minimum, the change in its line losses, and its yearly energy saving at the substation against the equipment's cost; the distribution planner's own M&V work
Swap: "fund voltage optimisation where the far end has room, the load is not thermostatic and the losses do not undo the saving" read with servers for feeders loses its meaning: there is no service voltage floor, no thermostat, no line loss growing with the square of current
Where the weight sits: R5, each feeder's yearly saving at the substation, built from the trial (R2), each feeder's makeup through the year, its far end (R3) and its losses (R4); long because every feeder-quarter is rebuilt from records at four grains (quarter-hour meter sums, hourly far-end minima, the trial's daily records, the register), not clever
Layer 1: the MDM export's re-sent October block and its estimated intervals (meters not reporting), the bus SCADA's lost scans, the regulator log's mixed-case modes, the weather station's missing reports, the bellwether meters three to a feeder (the lowest each hour counts); each made by the system that exports the file, none deciding a feeder on its own
Not one thing: the strongest single piece is the dose (J1): told it alone, the careful route still files ASH-219, ASH-222, CDB-116, CDB-219 wrong; each of the other four alone leaves two to five feeders wrong; one sentence rescues one result of six at most
One-fact test: "read the trial on the volts its regulators actually took off" rescues R2 only (1 of 6); "the volts come from the far-end meters" rescues R3 only; the other three rescue none (effort.json hints)
Not semantics: every field read right (the modes, the SCADA voltages, the bellwether minima, the survey codes, the register's ohms) still leaves the careful route funding 14 feeders, ASH-222, CDB-219, HOL-219 wrong, because each of the five is an estimate a reading cannot make
Not rule application: VO-1 files what is compared (energy at the breaker over a year like 2026 against normal running, 115 V hour by hour, the 4.8 V cap, USD 48 and 9.4); no filed procedure measures the response, carries it to a feeder or an hour, sets a feeder's volts or prices its losses
Estimand: VO-1 2.1 to 2.4 and 3.1 to 3.2; the trial protocol's design; the capital plan's costs; the prompt's per-feeder quantities
No decoy: the annual report's 6.1 per cent is a correct system statistic (energy delivered less retail sales over energy delivered) and answers a different quantity; no document argues a feeder
No replay: no result re-derives a published figure
Pinned: the heating and water-heating draws by the annual report's load research; every rival in the golden family (a resistive home at 2.5 or 3.2 times a heat pump home's heating draw, the trial's weather terms without squares, the trial's control from every untested feeder) files the same 13 feeders, nearest 6.1 per cent from the line; the trial scale moved by twice its sampling error (4.6 per cent), the loss coefficient by 20 per cent and the far-end readings by 0.2 V each hold the call; the world's own 2027 funds the same feeders, every feeder 6.2 per cent or more from the line, the golden's savings within 4.5 per cent of the world's on average
Run forecast: R2 lost to dismissed own evidence (the local-mode ON days seen and the assignment read anyway), R3 and R4 to a method shortcut (the trial's volts and the report's loss rate carried), R5 and R6 to the stack of shortcuts (each feeder like the trial average, spring carried flat); R1 earned
Strategy label: OWN (a randomised voltage trial carried through instruments with different blind spots to feeders and hours it never covered)
Depth level: 5 by the stump factorial: five necessary methods (dose, makeup, seasons with the give-back, headroom, losses), none sufficient, the single drops on four distinct wrong sets; the reflex route funds 14 feeders
Lesson: a voltage response measured on a few feeders on their best-behaved days is a structure, not a number: thermostats give it back, the far end caps it, the lines take part of it, and each feeder carries it in its own proportions; no build on file teaches the set

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each feeder's 2026 energy at the customer meters (MWh) | assembly and reconciliation | VO-1 3.1; the MDM export | within 2 MWh | method shortcut: the export summed with its re-sent block | - | Ask 1 |
| R2 | the trial's change in energy per 1 per cent of voltage removed, averaged over the trial feeders | causal reasoning | VO-1 3.1 (feeder-head voltage); the trial protocol | the golden family, 0.64 to 0.69 | dismissed own evidence: the regulator log's local-mode ON days seen and the trial read on its assignment | independent: the trial records | Component 2 |
| R3 | the average reduction in volts each feeder could be held at over the year | missingness and measurement | VO-1 2.3 | the golden family | method shortcut: the trial's 4.8 V carried to every feeder | independent: the far-end meters | Ask 3 |
| R4 | the change in each feeder's own line losses (MWh a year) | decomposition and attribution | VO-1 2.2 (energy at the breaker) | the golden family, 10 per cent or 3 MWh | method shortcut: the annual report's 6.1 per cent added in proportion | R3 | Ask 4 |
| R5 | each feeder's yearly energy saving at the substation (MWh) | forecasting | VO-1 2.2 to 2.4 | the golden family, 3 per cent or 8 MWh | method shortcut: the trial feeders' average carried flat at 4.8 V | R2, R3, R4 | Component 1 |
| R6 | the feeders that receive VO in 2027 | synthesis | VO-1 2.1 | exact | method shortcut: the careful route funds 14 | R5 | Recommendation |

Carry-forward: R1, R2 and R3 stand on their own records; R4 uses R3's volts; R5 falls with R2, R3 and R4; R6 with R5; a run with one feeder's figures wrong still earns the others' cells.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| some ON days never ran (communications) and each ramped down over its first hour | constructed (every trial feeder, both windows, a share set by each regulator's link) | no: all eight trial feeders, 10 to 38 per cent of ON days | a targeted query (regulator mode and output against the bus) | modelling (the response on the achieved dose) | keep |
| thermostatic load gives its energy back over a day | constructed (water heaters and resistive heat on every residential and rural feeder, all year) | no: every feeder with electric water heating or resistive heat | modelling (the load's makeup against the weather and the survey) | modelling | keep |
| the far end caps the reduction, hour by hour | constructed (every feeder's voltage drop with its length, conductor and load) | no: every feeder; it binds on the long and heavy ones | a targeted query (the bellwether minima) | modelling (hour by hour against 115 V) | keep |
| losses rise as constant-power loads draw more current at a lower voltage | constructed (current squared on every feeder) | no: every feeder, most on long rural lines | modelling (head meters against customer sums and the register) | modelling | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each feeder's 2026 energy at the customer meters (MWh) | Right | Right | Right |
| R2 the trial's change in energy per 1 per cent of voltage removed, averaged over the trial feeders | Missed | Missed | Right |
| R3 the average reduction in volts each feeder could be held at over the year | Missed | Missed | Right |
| R4 the change in each feeder's own line losses (MWh a year) | Missed | Missed | Right |
| R5 each feeder's yearly energy saving at the substation (MWh) | Missed | Missed | Right |
| R6 the feeders that receive voltage optimisation in 2027 | Missed | Partly | Right |
| Roughly | 1 of 6 | 1.5 of 6 | 6 of 6 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: the trial read on the volts its regulators actually took off, not on the day's assignment; rescues 1 of 6 results
Pair estimate: 32.3 (measured by effort.py on generator/effort.json; the careful pass is the reflex route)

## Stump factorial

Reflex route: every move a run makes unprompted or the files spell out set right (the export cleaned, the trial regressed with weather and day-type terms against comparable feeders, energy at the breaker, 115 V and 4.8 V, USD 48 and 9.4), every stump hurried: the trial on its assignment, the trial feeders' average for the untested feeders, flat through the year, the trial's 4.8 V everywhere, the report's 6.1 per cent added; it funds 14 feeders (ASH-222, CDB-219, HOL-219 wrong).

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| J1 the trial read on the volts its regulators actually took off | stump | the day's assignment | N24, L04 | moves ASH-113, GBR-219, GBR-222, HOL-219 | leaves ASH-219, ASH-222, CDB-116, CDB-219 wrong; R2 rescued (1 of 6) | yes |
| J2 each untested feeder's response from its own makeup | stump | the trial feeders' average | N25, L15 | moves CDB-219 | leaves ASH-222, HOL-219 wrong; none rescued | no |
| J3 the response through the year, thermostatic load giving its energy back | stump | the spring and autumn figure flat | N12, L15 | moves ASH-222 | leaves ASH-222, CDB-219, HOL-219 wrong; none rescued | no |
| J4 the volts from the far-end meters, hour by hour | stump | the trial's 4.8 V | N01, L17 | moves ASH-222 | leaves ASH-222, CDB-219, HOL-219 wrong; R3 rescued (1 of 6) | yes |
| J5 the losses from current squared | stump | the report's 6.1 per cent in proportion | N21, L22 | moves ASH-222, CDB-219 | leaves ASH-222, CDB-219, ELC-116, GBR-219, HOL-219 wrong; none rescued | no |
| J6 the export cleaned and the far-end lowest reading taken | reflex | - | R04, R05 | same call | - | - |
| J7 energy at the breaker, 115 V, 4.8 V, USD 48 and 9.4 | reflex | - | VO-1 (filed) | same call | - | - |

Level: 5 (five necessary stumps, none sufficient, the single drops on four distinct wrong answers)

## Data provenance

Source: generated by the seeded generator in task7/generator from a simulated public power district: weather at the quarter-hour; each feeder's load built from its customers' appliance holdings (base load, electric water heating, resistive heat, heat pumps, air conditioning) driven by the weather and the calendar; each substation bus under its load tap changer, stepping 5/8 per cent when the transmission voltage drifts out of its band; the trial's pilot regulators with their communication failures and settling; every load answering the voltage at its own exponent, thermostatic load recovering with its thermostat; line losses with current squared; far-end voltages from each feeder's drop
Behaves like the real thing: conservation voltage reduction factors of 0.5 to 0.9 per feeder, the give-back of resistive water heating and space heat, ANSI Range A binding at the far end of long rural lines, losses rising under CVR where constant-power load dominates, LTC operation a few times a day
Genuine patterns: (1) winter and summer peaks with the weather, (2) commercial weekday shapes against residential evening peaks, (3) LTC taps clustering with the transmission voltage's daily swing, (4) far-end voltage falling with load and line length, (5) loss shares of 1 to 13 per cent, highest on the long rural lines
Problems by process: the MDM's re-sent block and estimated intervals; the SCADA historian's lost scans; the weather station's missing reports; the regulator log's case drift; three bellwethers a feeder
License: not applicable (generated data)
Used as is: not applicable (generated data)
Breadth: 16 files, 24 feeders on six substations, 841,632 meter intervals, 630,720 bellwether hours, 10,595 tap operations, 2,297 survey households, 84 MB

## Template check

Chain signature: assembly-reconciliation, causal-reasoning, missingness-measurement, decomposition-attribution, forecasting, synthesis
Question form: which (which feeders receive VO); answered by a funded set with each feeder's figures
Nearest build: task13 (grid reliability, Kotuku) shares the energy domain and position on the network as a supporting lesson; its decision is an outage remedy, its records relays and outage logs; task22 shares the utility setting and nothing in the chain
Abstraction sentence: none writable against a build on file.

## Frontier check

Precedents: R2 (N24 the response read at the trigger only; L04 the caveat flagged and the recorded outcome kept), R3 (N01 proportional scaling; L17 the average unit), R4 (N21 an unmeasured component spread in proportion; L22 the published formula), R5 (N25 each unit off its own or the pooled event; N12 a season's rate carried; L15 an assumed response), R6 (N25, L15)
Shallow path checks: R2: the assignment reading passes a randomisation balance check and reproduces the ON-minus-OFF difference; only the regulator log against the bus SCADA (another record, quarter-hourly) shows the ON days that never ran; R3: the trial's 4.8 V is what the trial achieved on its feeders; only the far-end meters (hourly, another record) show where 115 V binds; R4: the report's 6.1 per cent reproduces the system's losses exactly; only the head meters against the customer sums (quarter-hourly) show losses rising under a lower voltage; R5: the trial average reproduces the trial feeders' mean; only each feeder's load against the weather and the survey shows its own makeup
Assumption made false: "the response is a first-bill pulse at the scheduled dose" (N24), false because some ON days never ran, tested by the regulator log; "the same response everywhere and all year" (N25, N12), false because thermostatic load gives its energy back and its share moves by feeder and season, tested by the load and the survey; "losses scale with load" (N21), false because constant-power loads draw more current at a lower voltage, tested by the head meters
Forcing: the line is each feeder's present value over its installed cost at 1.0; the golden family's nearest is 6.1 per cent from it; the drops land 3 to 25 per cent across; the trial scale moved by 4.6 per cent (twice its bootstrap error of 2.3 per cent), the loss coefficient by 20 per cent and the far-end readings by 0.2 V each leave the call; the world's own 2027 funds the same feeders
Noun swap: nearest by skeleton.py check is read at register; the decision form (a funded set over a value-to-cost line) and the five lessons differ from every card on file
Closed strategies: the call turns on latent_structure_estimation and instrument_noncompliance, neither on the closed page; the seasons step sits next to the closed seasons card (seasonal_shift_calibration): its fix is not a factor calibrated on a target season's record but a makeup estimated from the year's load and the survey, with thermostatic load giving its energy back; no closed lesson decides a feeder

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a feeder's yearly saving | at the customer meters / at the substation breaker | at the breaker | VO-1 2.2 |
| SF2 | the comparison | 2026 as operated / 2026 as the feeder normally runs | normal running, the trial's ON days restored | VO-1 2.2 |
| SF3 | the voltage floor | 114 V / 115 V | 115 V, hour by hour | VO-1 2.3 |
| SF4 | the cap | 4 per cent of the feeder's own voltage / 4.8 V on the 120 V base | 4.8 V on the 120 V base | VO-1 2.3 |
| SF5 | the value | one year / the equipment's life | USD 48 a MWh times 9.4 | VO-1 2.4 |
| SF6 | voltage removed in the trial | the scheduled 4 per cent / the feeder-head reduction recorded | the recorded reduction | VO-1 3.1 (feeder-head voltage is the bus or the pilot regulator's output) |
| SF7 | far-end voltage | one bellwether / the lowest of the feeder's bellwethers | the lowest each hour | VO-1 3.1 |
| SF8 | heating split | by households / by heating draw | by draw, the load research's 12,100 and 4,350 kWh | the annual report's load research; the ratio at 2.5 or 3.2 is same call |
| SF9 | trial weather terms | linear / with squares | with squares | same call (the average 0.65 against 0.67, inside the band) |
| SF10 | re-sent rows | summed / dropped | dropped | the repeated rows are exact copies of the same feeder and interval |
| SF11 | a water heater's draw | an engineering figure / the load research | the load research's 3,200 kWh a year | the annual report's load research |
| SF12 | the trial's control | same-class untested feeders / every untested feeder | same class | same call |

## Closure table

| Axis | Closure |
|---|---|
| 1 | population: the district's 24 feeders in the register |
| 2 | unit of account: the feeder; MWh a year; volts on the 120 V base |
| 3 | attribution window: a year like 2026 (VO-1 2.2) |
| 4 | as-of: records to 13 November 2026 (exports 2 to 16 November) |
| 5 | version basis: VO-1 revision 2; the 2027 capital plan |
| 6 | denominator: per 1 per cent of feeder-head voltage removed |
| 7 | weighting: none across feeders; each decided on its own |
| 8 | window length: the trial's two windows; the year for the saving |
| 9 | boundary inclusivity: equals or exceeds (VO-1 2.1) |
| 10 | rounding path: none filed; precision in the answer blocks |
| 11 | tie-break: none needed (nearest 6.1 per cent from the line) |
| 12 | maturity: the trial closed on 13 November |
| 13 | order of operations: response, makeup, volts, losses, value |
| 14 | row order: the register's |
| 15 | duplicate resolution: re-sent rows dropped |
| 16 | identity normalisation: feeder ids as the register |
| 17 | netting: losses netted at the breaker |
| 18 | dimensional units: kWh by quarter, MWh a year, volts on 120 V |
| 19 | code semantics: regulator modes VO and LOCAL (any case) |
| 20 | integerisation: none |
| 21 | clause scope: VO-1 applies to the 2027 programme |
| 22 | forward window contents: a year like 2026, the 2027 capital plan |

## Literal reader

VO-1 2.1 to 2.4 executed word for word on the read-back pack, with the trial read on its recorded feeder-head reduction (3.1), gives the 13 feeders and each feeder's figures in the answer blocks.

## Prompt contract

A voice rewrite may not drop or change: the question (which feeders get VO in the 2027 capital programme); the workbook and the short memo; the decision and the yearly saving at the substation in MWh for each feeder; each feeder's 2026 energy at the customer meters, average achievable reduction in volts over the year and change in its own line losses in MWh a year; the trial's change in energy per 1 per cent of voltage removed, averaged over its feeders. It must never add: a method, the trial's failures, thermostats, a file name, a role, a count of feeders, rounding.

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
- 2026-11-08, re-root to architecture 6: architecture 5's files removed from the folder (in git at c404109); its run
  kept as `runs/arch5/run1.md`.
- 2026-11-08, architecture 6's first mechanism (take-up of a once-only grant offer driven by the rise in use into the
  notice season; the counterfactual conditioned on the seasons before the notice): priced on the clean truth at design,
  before any pack. Selection on a rise brackets the truth, a twelve-month baseline over (heating optimisation 8.3 against
  6.2) and a long one under (4.5); the eligible comparison on a panel landed within a point and a half, a two-season
  baseline within one, and the golden family's own spread (5.0 to 6.3 per cent across pools, baselines and the ratio of
  totals, with the never-in-the-programme pool at 7.5) crossed every decision bar the long-baseline routes could be
  separated by; a comparison bracketing the truth always has a lucky baseline. Redrawn the same day as the lottery
  comparison that a second programme treated (one-sided: every route that keeps a treated comparison building files
  low).
- 2026-11-08, the offer-once rule across seven rounds (2019 to 2025): later offers went only to buildings newly flagged,
  which had risen into the top fifth, so later rounds were rise-selected even with take-up at random and the long
  baselines understated again; the pilot became one round drawn by lot.
- 2026-11-08, a tuning campaign spread evenly over seven winters: the first season after the works carried little
  contamination, so the first season alone landed every figure; the campaign front-loaded (twelve districts in its
  first autumn); the first season alone now misses every rate and lands only the funded set.
- 2026-11-08, the comparison read as drawn, with no baseline (the post-period means of drawn and passed-over buildings):
  in kWh it carries the buildings' size spread (several points of standard error), so it is noise, not a member of the
  golden family; every licensed route takes a baseline.
- 2026-11-08, the ask layer measured at a pair of 53.3 on the cut pack (the saving to April 2026 the only second
  judgment, and its shortcut within 4 per cent of the golden at the nearest 5,000 tonnes): the asks re-sited onto two
  judgments of their own, the funded round once the offer closes (the 2019 responses' timing by measure) and the pilot's
  2025/26 saving at the council's rates; the saving to April 2026 dropped, because "without the works" could also be
  read as with the service visits those buildings would then have had, which a single season at the council's rates
  makes converge.
- 2026-11-08, the application rows: every application with its verdict let the lottery keep the heating controls and
  insulation rows; the sheet now lists the funded applications, the office's own grant list.
- 2026-11-08, the first autumn's visits in twelve districts from September: the first season alone still funded
  heating optimisation (at 0.96 of the limit); sixteen districts from August put it at 1.15 times the limit.
- 2026-11-08, the draw as first realised: the heating optimisation works buildings ran 3 per cent under their
  passed-over owners on the 2018/19 season by chance, and the lottery read as drawn, with no baseline, landed the funded
  set; the draw redrawn to one balanced within each measure (under 1.2 per cent), where every reading of the lottery
  files insulation alone.
- 2026-11-08, the ratio of totals in the golden family: it put heating controls at 2.6 per cent (3 in whole per cent)
  against 2.1 for the mean of the buildings' gaps; the plan now files the rate as the average over the works buildings.
- 2026-11-08, an insulation cost of €72 a square metre to push the lottery to fund nothing: it left two shallow routes
  at 0.98 and 0.99 of the limit and a default answer of no measure at all, which a run would question; kept at €54.5.
- 2026-11-08, stage 4 judge: the saving rates unforced (heating optimisation 5, 6 or 7 per cent as the comparison's
  share was pooled, averaged or differenced and the seasons chosen), the call forced under every estimator; the plan's
  4.2 now files the construction (each works building's use as a share of its 2018/19 use against the comparison
  buildings' average share, one less the ratio, averaged over buildings and seasons), never which buildings compare;
  critical component 2 restated at whole points and the 2018/19 rival at 500 tonnes.
- 2026-11-09, platform review of architecture 6 (version 17; stumped, determinism, solution and type checks passed;
  prelim verdict sent back for fixes): the funding answer turns on one thing, the service visits in the meter file
  (about 7 per cent off most passed-over buildings and none of the works buildings, `TUNE_EFFECT = 0.070` on `~w.works`
  only), constructed, only in the comparison arm, fixed by one exclusion; past it the plan's 4.2 and 4.4 formulas carried
  every figure. The reviewer kept the lottery and the per-measure projection to the offer's close. Re-rooted at stage 1
  as architecture 7 in the same world at the reviewer's direction (client text decides what is allowed).
- 2026-11-09, architecture 7 at design: the reviewer's suggestion of buildings that changed floor area as a lever
  (an insulation works arm whose owners converted their attics after the roof works): every reading that sets the
  converted buildings aside or censors them at the change is unbiased when converters save like the rest, so the fix is
  one filter, and when they save more it needs the new space's gas estimated from conversions that themselves include
  roof insulation; kept only as texture (extensions and empty floors across the stock, balanced by the draw).
- 2026-11-09, the visits kept as a modelled factor (deferred in the works arm, uneven, logged from 2021): a constant
  visit term in the comparison corrects the bias once the visits are known, which is the one extra term the client
  names; the visits now reach both arms by district and decide nothing.
- 2026-11-09, the saving as the average building's share (mean of logs): controls 1.3 points and insulation 0.8 points
  over the gas-weighted share and the 2025/26 saving 11 per cent apart by use; plan 4.2 now files the share of the gas.
- 2026-11-09, heating optimisation keeping 20 to 40 per cent of its first season: the flat route and the golden
  family sat within the 90 per cent range of each other; it now keeps about 5 per cent, levelling by the fourth season.
- 2026-11-09, the prompt's rounding sentence (savings to one decimal, grant per tonne to the euro, counts to 10, grants
  to EUR 10,000, round totals to EUR 0.1 million, tonnes to 10, the 2025/26 CO2 to 100): dropped at the author's word;
  the golden and the answer blocks now state each figure at its natural precision, every value unchanged (the widest
  printed shift under the old rounding was 94 application rows under 10 tonnes printed as 0 or 10).
- 2026-11-09, architecture 7 on the platform (the author's test run, `runs/arch7/run1.md`, no score pasted): the run read
  the lottery as drawn (instrumented on completion), priced each use's saving to this year's applications, carried
  heating optimisation's fade on its last three seasons and projected the round measure by measure, landing the call at
  87, 95 and 139 euro a tonne; it lost only the round's insulation count (312 against 343) and heating optimisation's
  figure. Every judgment of the chain was one a frontier run makes unprompted, so the chain priced nothing; re-rooted as
  architecture 8 at the author's choice, the transport moved onto each measure's driver read from another record.
- 2026-11-09, architecture 8 at design: the service team's burner checks setting the boiler's clock to the building's
  hours as the controls driver (a check that finds the clock unset sets it): controls saved about 7 per cent against
  unchecked buildings and 2 per cent against checked ones, but the use-priced route landed within 2 per cent of the
  golden (4.06 against 4.21 per cent), no separation, and a check is an event in both arms the reviewer names.
- 2026-11-09, a size-aware projection of the round (late answers reweighted by size and use): 343 to 348 insulation
  applications against the world's 395, no closer than the golden's; R8a's band widened to 10 per cent instead, so a
  recipient-level response model like architecture 7's run (312) lands inside it.
- 2026-11-09, heating optimisation's fade by occupancy class as the second lever (hotels and care homes turning the
  curve back up at night): each use's seven-season level already carries most of it, so the pooled fade on use levels
  and the class fade sat 4 to 7 per cent apart; the second lever moved to the roof.
- 2026-11-09, the round at close as the funding population (late insulation applications larger and capped): received
  and late applications' grant per tonne differed by 1 to 6 per cent in the world; no lever.
- 2026-11-09, the lived-in rule on a weekend maximum over minimum of 1.10: the base load's 3 per cent hour-to-hour noise
  put every closed conference house and day-care centre over it; the rule now sets weekend days against weekend nights
  at 1.08, agreeing with the world on 99.98 per cent of buildings.
- 2026-11-09, the 2019 owners choosing on the drivers at a third of the 2026 strength: it halved both levers (controls
  125 by use against 119 by the empty week); 2019 owners now lean only slightly towards controls in an emptier
  building and not at all towards insulation on the roof.
- 2026-11-09, profiles and roofs only for buildings still on gas: 3 per cent of the pilot's answers (buildings that left
  the network) lost both; every building standing in 2025 now has a profile, every building standing at the 2023
  flight a roof.
- 2026-11-09, every drawn owner counted as treated (the offer's effect): with the roof driving insulation it now
  dilutes insulation past the limit, so SF3 is closed by plan 4.2's "the buildings that had them" rather than by
  convergence; the draw's effect scaled by completion stays within a point of the golden every season.
- 2026-11-09, a straight line through every band of controls' saving, the lived-in band included: 115.83 euro a tonne,
  funding controls on a line that fits the bands twice as badly as the threshold and rise; a hurried route outside the
  band, not a rival (SF18).
- 2026-11-09, stage 4, first judge pass (DETERMINISTIC, APPROVE, `determinism_check_report_pass1.md`): a single
  sentence naming both drivers rescued about half the chain, because a hotel's load then read about 60 per cent empty
  and fitting every building off its load still funded controls (112 euro a tonne); the lived-in buildings now carry
  their honest activity (a hotel's breakfast and evening peaks over a long low day and night, a care home's meals), so
  read off the load alone they look two thirds empty, the pilot's lived-in bands sit under the curve, and controls
  fail at 156.47; the both-drivers sentence rescues R4 and R5a only.
- 2026-11-09, stage 4, the reader: the profiles read as "a handful of standard shapes" (plateaus with sharp edges); a
  working day's shape (lunch, the afternoon tail, a restaurant's lull, shift breaks), part-staffed Saturdays, outdoor
  lighting at night and a day-to-day spread were added, and a continuous-operation rule (a load that never falls below
  three quarters of its peak has no empty hours) keeps a control room or a three-shift line from reading its night
  dip as an empty building.
- 2026-11-09, stage 4, second judge pass (NOT_DETERMINISTIC, SEND_BACK, `determinism_check_report.md`): the lived-in
  test written as "a hotel or care home whose weekend days run above its weekend nights" carried no margin; read as
  strict hour-by-hour dominance it held 2 per cent of the pilot's hotels and care homes lived in and put controls near
  the load-alone figure, over the limit. Repaired by a construction with no margin (every hotel and care home lived in
  round the clock, by its use on the register, which the lottery's own hotels and care homes bear out: two thirds
  empty off their load, under 1.5 per cent saved), the weekend test kept as a rival family that lands inside the band
  at every margin to 15 per cent once the lived-in buildings carry an honest base load (6 and 5 W a square metre for
  hotels and care homes, against 14 and 12 in use), and strict dominance inside R3's band with the same call.
- 2026-11-09, stage 4, third judge pass (NOT_DETERMINISTIC, SEND_BACK, `determinism_check_report.md`): with the lived-in
  step decisive for controls, no filed sentence made hotels and care homes lived in, so reading them off their load
  (159.57) survived as a rival, and a line through the lived-in band sat at 120.02. The step can be decisive only if
  it is filed, and filed it is a definition read; at the author's choice the lived-in buildings went back to their
  milder activity (a hotel reads over half the week empty off its load, not two thirds), so the step moves controls'
  figures, not the call (114.12), the use rule and the honest base loads kept, and the both-drivers hint recorded at
  6 of 13 as the build's level-4 risk.
- 2026-11-09, every hotel and care home made lived in by overriding the conference houses and day-care centres after
  the draw: it changed a few 2019 choices, redrew the lottery and shrank both levers (controls 115.4 against 132.5 by
  use), so it was reverted; the line through the lived-in band stays at 120.02, ruled out by its misfit.
- 2026-11-10, a run on the READY cut (pasted by the author, the audit in this session's record): it set the load
  profiles and the cadastre aside in one sentence, carried each use's saving and lost every point it lost there; the
  both-drivers sentence would have taken it from about 47 to 73 to 86 on the house split, and the controls driver alone
  would have landed the call through its own reading of the round at close. Level 3 in practice; levelled up rather
  than re-rooted, the backup in ~/Documents.
- 2026-11-10, buildings leaving gas as the heat plan's networks arrive (each measure's tonnes counted only while the
  building burns gas, the take-up read off an existing network's history), set aside at its scratch gate: with 8 per
  cent margins on both sides it decides the call only if about 83 per cent of insulation's reference consumption sits in
  the priority areas (21 per cent today), a concentration that would sit where it decides; with real shares the
  survival curve a careful run fits on the visible removals lands the golden's side. Controls sits near the line (128 by
  use, 103 on its own building), so a second judgment on the call has to leave controls almost untouched.
- 2026-11-10, the round at close as the basis of the €120 test (as plan 4.4 and terms 3 would read), with taller
  buildings answering later, set aside: this year's owners chose insulation on the roof, so few tall buildings are among
  the early applications and the late mix would rest on a handful of them, and the run's own forecast already hung a
  quarter of insulation's tonnes on two applications; the committee's request now files the basis instead (SF21).
- 2026-11-10, 16 of the 26 roofers still trading, rejected at calibration: the works then pay about three quarters of
  insulation's grant, and the funded pair lands within 8 per cent of every budget that also keeps insulation alone,
  paid in full, clearly over it; with 12 the pair pays 85 per cent of €8.2 million, every rival under 88, while paid in
  full (131) or counted in jobs (109) it runs over.
- 2026-11-10, after judge pass 5 (which approved the cut it read): the 2019 roofing record made less tidy (one working
  day in seven lost to rain, the same days for every firm; some firms starting a few days late; each roof faster or
  slower than its area alone says), the pace retuned so every 2019 roof still finished by 20 September, and the heating
  firms given more fitters so the two heating measures together would fit (the busiest firm at 81 per cent of its
  room); a data-only change, re-checked by the generator's assertions and leak.py, every graded figure moving by under a
  per cent bar the round's payment (6.99 million, inside the published bands).
- 2026-11-11, platform review of architecture 8 (returned; the holistic audit on the same version had passed it at
  level 5, pinned): the deciding step was one constructed hidden factor, the roofers' capacity on this year's larger
  roofs, which bit only in insulation (the heating firms had room) and left one routine step once named (pace times
  working days per firm; every reading within a tenth). The test responses reproduced the pilot seasons, both
  per-building transports (the empty week from the load profiles with the lived-in buildings, the roof per floor from
  the cadastre), the fade, the round at close and every carbon call, so the effort test's careful column, which priced
  both transports as lost, was 40 to 60 points optimistic as the run record warns. Agreed with the return, no
  rebuttal (`runs/review_2026-11-11.md`); re-rooted at stage 1 as architecture 9 in the same world at the reviewer's
  direction, the call moved onto analysis and the capacity out of the decision.
- 2026-11-11, architecture 9 at design: the service visits kept from architecture 8 in both arms as a decomposition (the
  reviewer's third suggestion) with a check resetting the curve in every building: in a world where a reset creeps back
  faster in a balanced building than an unbalanced one the visits nearly cancel between the arms (1.3 points early, 0.2
  late, about 7 per cent of the life), and with visits in the comparison arm only it is architecture 6 again; built
  instead as a campaign whose check a balanced system holds (the physics of balancing), with the first round's checks
  tuning burners only.
- 2026-11-11, architecture 9 at design: the decomposition's first estimator, an event study of the checks by arm with
  season effects, under-removed the works buildings' held lift (the lift collinear with the works' own seasons in a
  four-cohort rollout) and landed near the measured seasons; the golden reads the works buildings' seasons before
  their own check instead, and the level the works settle at is the last three such seasons weighted by the gas each
  rests on (a fitted approach to a level on the thin late seasons swung from €53 to €600 across seeds).
- 2026-11-11, architecture 9 at design: controls' range at the owner, with the owners' facility-management spread on the
  saving alone, came out only 1.10 times the building-level range at its upper end (seed 70707), too thin to force;
  the world now gives a portfolio's buildings a shared slow drift and controls a wider facility-management spread with
  less building-level noise, and seeds 70701 to 70715 were scanned for the scale-free margins; seed 70706 holds every
  call by 12 per cent or more under the golden and lands every shortcut on the other side.
- 2026-11-11, architecture 9 at build: the asks first carried each measure's saving season by season, the pilot's
  2025/26 CO2 and every application received; effort.py measured the careful but hurried pass at 61.7, the earned asks
  outweighing the two judgments, so the seasons and the 2025/26 CO2 left the asks (the seasons stay in the workbook as
  working) and the listing asks only for the funded measures' applications and their total, which a run that funds the
  wrong set gets wrong. The range's low ends were taken out of the grading: a symmetric range or a leave-one-owner-out
  spread puts them 20 to 70 per cent from the percentiles while every construction keeps the upper end, the end the
  committee judges, inside its band.
- 2026-11-11, stage 4: the judge read the feeder, hosting and heat-pump lines at the head of this section as another
  build's; they are this slot's own earlier draws (the co-op heat-pump architectures retired in October), kept under
  the append-only rule.
- 2026-11-12, architecture 9 at the platform: the run landed the call (insulation alone) and both deciding judgments by
  reflex: it clustered its bootstrap at the owner because the pilot rules filed the draw by owner, and separated the
  check campaign from the measure's ageing because the heat plan filed it (task7/runs/arch9/run1.md). It lost only
  insulation's transport (it set the solar cadastre aside as unrelated) and second-decimal figures. A judgment whose
  trigger a document files is executed; the world is spent, and architecture 10 moves to another world, dataset and
  shell.
- 2026-11-12, the READY prompt's framing: it restated the renewal bar, opened its second sentence on why the answer has
  to be an estimate (task457's approved opening) and pinned each kW to "the 4CP intervals of a summer like 2024 to 2026".
  Cut at the author's direction: Board Policy 412 files the bar, the intervals, the alerts as called and the devices
  counted, so the clauses were context the files hold, and "estimated from the last three summers" pointed at the data
  window. The prompt now asks the question, the two files and the asks only; no graded figure moved.
- 2026-11-12, architecture 10 (Cedar Brake co-op's thermostat providers at ERCOT's 4CP, READY at 03:15, never uploaded): the client's overused-strategies page, filed at 09:37 the same day, closes all three deciding carries (the 4CP days late in heat waves is
  'Repeated exposure behaves differently from a one-off', whose own example is smart-thermostat demand response fading over
  consecutive hot event days; the 2027 retail cohort and the fleet's homes are 'The pooled effect does not transfer to a target with
  a different mix'), so the call was a stack of closed lessons; the guard read it only as near because the card named another key.
  The world, its dataset and its shell go with it; architecture 11 decides on coincidence at a shared transformer, off the page.
- 2026-11-12, architecture 11 at calibration: half the chargers in the managed half made the 2026 meters alone call 'keep own
  schedules' (the metered summer's count fell below Sequence's), so a step near the closed 'outcome hidden by the intervention' card
  would have decided; the pilot manages one charger in four instead, and the route that reads own schedules off the meters now
  leaves the call standing (no_own in effort.json).
- 2026-11-12, architecture 11 at calibration: the managed half's own settings drawn from the own half's distribution or set to the
  commonest timer moved the own count by 13 (64 against 77); the roster now carries the usual charging each member gave at
  enrolment, as the rate schedule says it is asked, and the declared-only rival sits inside the band.
- 2026-11-12, architecture 11 at calibration: the monitored transformers' option-by-option peak lift as the golden put Stagger 6
  above the world's quarter-hour truth; the per-hour excess lands closest to the truth and is the golden, the peak lift a rival.
- 2026-11-13, architecture 11 after the holistic check: the Sequence count (11, USD 160,300) and the flip fee (USD 156) rested on three readings no file settled (whether the queue waits for a late charger: 7 if not; the ready-by for a session with none in the app: 14 or 16 at 15 or 30 minutes before the unplug; how hourly reads become quarter-hours: the golden's per-hour excess scaled by the square root of homes was filed nowhere). Closed by filing all three at their authority (the proposal's rule now says each charger waits for every one before it, the earlier plug-in first, both products on the quarter-hour; EV-4 4.1 the replay's frame and ready-by at the unplug time rounded down; DPS-7 revision 5's 2.2 and Table 2 peaking factors by nameplate, set from the 48 monitors and applied monitored or not, with Table 1's missing 50 kVA pole-mount row), not by keeping any open: the golden moved (own 53, Stagger 29.7, Sequence 13 and USD 196,700, flip USD 153) and the bands carry the rivals plus one marginal unit either side. The quarter-hour lift is no longer a judgment, so the depth line is level 4 on three judgments, not 5 on four. Re-judged once (Sequence replayed transformer by transformer to 13; Stagger sampled to 29.5 once the judge's own script stopped applying 0.95 twice and piling pre-July blocks onto 1 July): DETERMINISTIC, FIX_NOW, three answer-block sentences (the late charger counts ahead of every later one, energy over the recorded charge time, the clock six hours behind UTC), applied; the leak reader found no leak.
- 2026-11-13, architecture 11 (Hollins Creek's EV Overnight default) retired: the platform run landed every graded result (task7/runs/arch11/run1.md); its retrofits were each tried and refused on paper: per-device Stagger persistence (contradicts the proposal's wording; filing it hands it over), offline fallback on shared nights (a literal replay catches it, or nothing pins it), Sequence on the uncorrected GIS (plus or minus 2 transformers), charging taper (moves every figure, never the default, one sentence rescues four results).
- 2026-11-13, architecture 12 prototypes: per-feeder tap-event cells (too noisy alone: the commercial morning ramp and on-the-hour temperature steps contaminated them; the same-class peer control fixed the ramps, but heat pumps and resistive heat could not be told apart in the fit, so the compressor response was left to the trial's scale with every non-thermostatic load answering in proportion); an energy-weighted trial scale (one noisy trial feeder moved it 10 per cent; the median of the trial feeders' ratios holds it to 2.3 per cent).
