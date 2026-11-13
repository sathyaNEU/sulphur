# task13: what Laguna Prieta Electric Cooperative's line crews fix on the 69 kV system this winter and before summer 2027, from one conformed table of every fault since January 2022

## Draw

Subdomain: Energy Systems & Utilities, grid reliability and outage analysis (`grid-reliability-outage-analysis`; the
  69 kV fault record a cooperative's reliability engineer conforms from relays, SCADA, the control room and the field)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build): the author's assignment of 2026-11-12. Two
  relay vendors' event exports, a legacy target log, the SCADA sequence of events, the control room's outage log, the
  outage system's database, a solar farm's own protection export, five weather records, the lightning record and the
  field records (patrols, the environmental team's roost survey, test insulators, washing, vegetation and maintenance
  work) conformed to one row per fault, with the counts, locations, causes and member impact computed from it
Answer shape: a flagged set with the evidence (the repeat locations and sections the work list flags, each with its
  cause, its located faults and the fix), on top of the conformed fault table
Weight: assembly (building one fault record a crew can be sent from: each fault located, timed and caused from
  instruments that each see part of it); the last two live cards sit on measurement (task22) and attribution (task4)
Data-native sentence: a 69 kV fault is recorded by the relays at both ends of its line, each computing its own
  distance on its own clock as if the fault had no resistance and nothing fed it from the side, by a SCADA clock that
  knows only breakers, by a control room that codes a cause from what the weather looked like, and by nothing at all
  where no crew went, so where a fault was and what caused it exist only in the relation between the two ends'
  residual currents and the network behind each end on that date, the weather at the line rather than the airport,
  the conductor's temperature that afternoon and the field teams' own records
People: Brittany Melton (reliability engineer, the golden's author), Thomas Evans (manager of engineering), Derek
  Hart (system operations supervisor), Joanna Choi (environmental compliance specialist), Allison Ward (vegetation
  management coordinator), Andrew Russell (transmission planning engineer), Julie Peterson (line superintendent), from
  `guard.py names --geo "United States" --seed 1305` and `--seed 1306`; none is named in the prompt. Card WARNs answered: people.first Thomas against mark126 (an older Mark build, a different world); overuse.objective (ETL on 4 of the last 12) is the author's assignment. ban.pairing (energy x etl against task22) registered with --force at the author's direction of 2026-11-12

## Stump screen

Written at the draw on 2026-11-13, before the card and before any code. Tests: 1 off the closed page, 2 not a reflex,
3 nothing filed, 4 clean data, 5 two records, 6 the waved-through assumption, 7 a plausible shallower story, 8 across
the data, 9 worth the call.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Fault resistance and load flow move each relay's own distance toward the sending end (tree contacts by 1 to 6 km, arcs by under a span); the residual current's split between the two ends follows only the zero-sequence network | the relay's distance taken as the location, both ends averaged (L22: the formula's no-resistance assumption, contradicted by the tree contacts' low currents) | the other terminal's export at another format and clock, and the protection study's line-out zero-sequence source impedances | none | kept (S1) |
| Inland's 138/69 kV autotransformer replaced in March 2024 (a stronger ground source behind Inland), so the split of a 2022 or 2023 fault on an Inland line reads against the 2022 study | today's network for the whole history (N09) | the 2022 protection study beside the 2025 one, and Inland's relay settings changed in 2024 | none | kept (S2) |
| The solar farm tapped on Shell Ridge-Ponder Creek steps the 69 kV through a grounded-wye transformer, so it feeds ground current into every fault beyond the tap, by night as well as by day; Ponder Creek's electromechanical relays keep no record | the farm's export set aside as a generator's log with its own clock and names (L38, N27), or no infeed at night | the solar farm's own protection export (local standard time, kA) and the substation register's transformer windings | none | kept (S3) |
| Night faults on the coast come from three causes: fog flashovers on salted porcelain, bird streamers at roost structures, failing insulators in light rain; the coastal airport's visibility misses the bay's fog and finds fog the bay never had | the airport stands for the conditions at the line (N26) and the environmental survey is unrelated (L38); every humid-night coastal fault booked as contamination (L26) | the cooperative's own substation weather stations by the bay (dewpoint spread, from March 2023), the environmental team's roost survey, the washing log | none | kept (S4) |
| A grow-in contact needs the conductor hot (sagged) on a still afternoon; fall-ins and storm debris come on gusty afternoons; both are summer afternoon faults with no stroke | every non-lightning summer afternoon fault, or the control room's TREE code, taken as vegetation (L26, L04) | the hourly line loading beside the bay and inland weather (conductor temperature), the lightning record on the true time | none | kept (S5) |
| A coastal section's salt deposit builds from its last wash or soaking rain at its own rate and flashes over only past a level, so the sections due before the fog season are not the ones that flashed over before | the past flashovers taken as the present state, or October's test readings as December's (N02, N13) | the test insulators' monthly deposits, the washing log and daily rain, against the deposit at each past flashover | none | kept (S6) |
| Lightning backflashovers recurring at towers with high footing resistance | a tower's count read at face value | footing resistance survey | 2 (stroke matching is R32), lineage (architecture 3's lightning protection referral) | dropped |
| Member-minutes from the outage system's dispatcher-closed times instead of the SCADA restorations | the outage system's durations | the sequence of events | 2 (R46: the architecture 4 run rebuilt every time from the device record) | dropped (kept as a Right-scored result, R5) |
| A field switching move the GIS never recorded, found from paired load steps | today's topology | hourly loading | 8 (one transfer, only in the deciding units), 4 (a re-key once found) | dropped |
| Conductor sag at the 2027 planning case's loads against the vegetation survey | the 2026 peak carried to 2027 | the planning case | 3 (the planning case files the loads, and the sag formula is executed), and a forward total | dropped |

Kept: six, each independent (no one sentence of help rescues two of them): S1 and S2 move the located spans of the
grow-in contacts, S3 the tap line's repeat location, S4 the night repeat locations and their fixes, S5 which summer
faults are grow-ins, S6 the sections washed before the fog season.

## Deep reasoning

Task type: Grid reliability & outage analysis, the client's task type in Energy Systems & Utilities that serves Data Extraction & Conformation here: the 69 kV fault record conformed from the relays, SCADA, the control room, the outage system, the weather and the field records, with each fault's location, cause and member impact and the work list computed from it
Domain test: the results are the protection and reliability engineer's own quantities (a fault's place from the zero-sequence network behind each end of its line on its date, the ground current a grounded-wye generator step-up adds beyond a tap, a conductor's temperature from its heat balance, a porcelain string's salt deposit against its flashover level, member interruptions on the five-minute line), and the engineer uses them to send crews to structures
Swap: rewritten for a water utility's main breaks ("which mains to replace, from the pressure loggers at both ends"), nothing carries: no fault resistance biases a distance calculation, no residual current splits between two ends, no ground source sits at a tap, no conductor sags hot and no salt flashes over, so every result stops making sense
Where the weight sits: assembly: one row per fault a crew can be sent from, built from two vendors' exports on two clocks and units, SCADA, the control room and the outage system, each fault located from both ends' residual currents against the network on its date and caused from the weather at the line, the strokes, the survey and the conductor's heat; the work is long because every one of 436 faults needs all of it
Layer 1: relay exports in two formats (UTC and miles; local time, km and kA), two relay clocks drifting until resynchronised (Mesquite Flat in 2024, Caney Bend in 2025), records lost to overwritten buffers, Ponder Creek's electromechanical relays keeping only targets, structures renumbered on Lines 8 and 13 after their 2023 rebuilds, dispatcher-closed restorations in the outage system, operators' cause codes from the weather look, station telemetry gaps, airport units and the solar farm's export on standard time all year; every careful run cleans each the same way and none decides a result
Not one thing: the strongest single piece is S1 (each fault placed by the split of its residual current between the two ends): a run that nails it still files the wrong grow-in list without S2 and S5, the wrong night list without S4, the wrong tap location without S3 and the wrong wash list without S6, and earns no result from it alone
One-fact test: the most useful single sentence is "the solar farm's step-up feeds ground current into every fault beyond the tap, by night as well", which rescues R4 alone, 1 of 10 results; the residual-current sentence rescues none alone
Not semantics: every field, unit and RP-04 clause read correctly (the fault, the year, the causes, the location, the repeat location, the member interruption, the washing rule) still leaves the relays' distances biased, the airport's fog off the line, the roosts unseen, the tap infeed uncorrected and each section's deposit on 31 October unknown, so every hurried result is still wrong
Not rule application: RP-04 defines what a fault, a repeat location, a member interruption and a due section are, and performs none of the location, cause, infeed or deposit work; once every filed rule is applied, where each fault was, what caused it and each section's salt on 31 October are still left to judge
Estimand: RP-04 Rev 4 files the fault (one protection sequence on one line, switching and tests excluded), the year (in a November report 2026 runs 1 January to 31 October), the location (the structure nearest, numbered as on today's inventory; a span by both numbers), the nine causes, the member interruption (more than five minutes, to the restoration of supply to the member's substation), the repeat location (three or more faults of one cause on one line within 400 m since 1 January 2022, salt left to washing), the work list (each open repeat location with its fix, and each section due) and due for washing (the 31 October deposit at or above the deposit at which the porcelain has flashed over in fog); the prompt asks for each by type
No decoy: nothing is written to carry a wrong answer: the relays' distances are what real locators print, the airports' records are the airports', the control room's codes are the operators' own at the time and the outage system's restorations are the dispatchers' closings; none argues a list, and deleting every one leaves each result as hard
No replay: no result re-derives a published figure; the locations, causes, 2026 member figures and work list exist only in the conformed record
Pinned: 18 rival methods (fog at a dew point spread of 0.3 or 0.8 C, storms at 2 or 5 strokes or within 6 or 10 km, the conductor at 36 or 44 C, front gusts of 8.5 or 11 m/s, the flashover level at the 5th or 10th percentile, the deposit rate from the nearest test site or linear in distance, soaking rain keeping 35 or 60 per cent, the repeat window at 350 or 450 m) each file the golden's 25-item work list, six perturbations (the deposit rate and the flashover level by 20 per cent, the conductor threshold by 4 C) hold it, and the counts sit inside 1 a year and 2 a cause, the member figures inside 2 per cent
Run forecast: R2 (method shortcut: the relays' own distances on today's network), R3 and R6 (dismissed own evidence: the roost survey and the bay stations set aside for the airport), R4 (dismissed own evidence: the solar farm's export set aside), R7 (dismissed own evidence: past flashovers taken as today's salt), and R8, R9 and the recommendation (R10) with them; R1 and R5 are expected landed
Strategy label: own (nearest in the atlas, Quantitative Finance and Trading 5, trade reports conformed into one record per trade, Data Extraction & Conformation, assembly then a quantity the public data hide; none of its chain is used)
Depth level: 5: six independent stumps, each necessary and none sufficient, the single drops landing on six different wrong work lists (1 to 18 items off the golden's 25) and the reflex route on a seventh (32 items off)
Lesson: a fault record is built, not read: each instrument computes its own number under its own assumptions (a locator's distance with no resistance and no infeed, an airport's weather, an operator's code), and where a fault was, what caused it and what the crews do next come from the physics joining two ends' records, the conditions at the asset and its maintained state; no build on file teaches fault location from the network behind both ends (skeleton.py: position_on_network_effect untaught; severity none against everything on file)

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the 69 kV faults by year: 2022 96, 2023 93, 2024 83, 2025 84, 2026 (January to October) 80; 436 in all | assembly and reconciliation | RP-04's fault and year; the SCADA sequence of events and both relay exports | 1 a year | narrow look at broad data in the quick pass (the control room log's trip rows, 2025 at 90); a careful run conforms both exports to SCADA by reflex (R01, R28, R29, R46) and lands it | - | Ask 1 |
| R6 | the 2026 faults by cause: lightning 9, bird or other animal 6, salt contamination 16, insulator failure 16, vegetation grown in 14, vegetation from outside the right of way 8, vehicle 5, hardware 2, unknown 4 | exploration and triage | RP-04's nine causes; the strokes, the bay stations, the roost survey, the loading, the patrols | 2 a cause | dismissed own evidence: the roost survey set aside as an environmental file and the airport's codes taken for the line's weather, so the birds read as failing strings (bird 0, insulator 20) | R1 | Ask 2 |
| R5 | the 2026 member interruptions and member-minutes: 57,024 and 1,227,611, by line (Line 2 16,115 and 179,995; Line 5 11,171 and 172,224; Line 8 10,259 and 354,807; Line 9 1,168 and 27,196; Line 10 14,894 and 199,267; Line 13 3,417 and 294,124) | decomposition and attribution | RP-04's member interruption; SCADA trips, recloses and transfers; members by feeder | 2 per cent | unfinished chain in the quick pass (the outage system's dispatcher-closed restorations, 2,350,200 member-minutes); a careful run rebuilds the restorations from SCADA by reflex (R46) and lands it | R1 | Ask 3 |
| R2 | the vegetation repeat locations: spans to clear at Line 10 47-48 and 88-89, Line 14 63-64, Line 6 57-58; hazard trees at Line 11 118-120 and Line 13 103-107 | missingness and measurement | RP-04's location and repeat location; both ends' residual currents; the 2022 and 2025 studies' line-out sources with the register's 14 March 2024; the hourly loading and weather | a structure within 2, a span within 1 | method shortcut: the relays' own distances (both ends averaged) taken as the location though they assume no fault resistance and no infeed; dismissed own evidence on today's network for 2022 and 2023; stopped at the first story that a summer afternoon fault with no stroke is a tree: spans at Line 10 35-36, Line 13 90-91 and Line 6 48-49 and a stand at Line 13 93-96 | R1 | Component 1 |
| R3 | the night repeat locations: perch guards at Line 6 79, Line 7 31 and 52, Line 12 104, Line 14 117, Line 16 23; strings to replace at Line 2 63, Line 5 88, Line 15 57 | investigation loops | RP-04's causes and repeat location; the bay stations' dew point, the roost survey's structures, rain and hour | a structure within 2 | dismissed own evidence: the roost survey and the bay stations set aside for the airport's codes; stopped at the first story that a repeated night fault on porcelain is a failing string: strings at 11 places and no guards | R1 | Component 2 |
| R4 | the tap line's repeat location: Line 9 structure 137, 3.2 km past the solar tap | missingness and measurement | the solar farm's export and the 2025 study's step-up data; Shell Ridge's record | a structure within 2 | dismissed own evidence: the solar farm's export set aside as a generator's log on another clock with no structure numbers, so Shell Ridge's distance stands at structure 148 | R1 | Component 3 |
| R7 | the washing sections due before the fog season: Line 2 sections 1 to 5 and 7, Line 3 sections 4, 5 and 7 | forecasting | RP-04's washing rule; the test insulators, the washing log, daily rain and the fog flashovers | exact (every level and rate rival files the same nine) | dismissed own evidence: every section that ever flashed over taken as due, so Line 1 section 3 and Line 2 section 6, washed in October, go on and Line 3 sections 4, 5 and 7 and Line 2 section 7 drop off | independent: the test insulators, the washing log and daily rain (its level also reads R6's fog flashovers) | Component 4 |
| R8 | every open repeat location with its cause and fix (the 16 of R2, R3 and R4) and the seven fixed after their last fault | synthesis | RP-04's repeat location and work list; the maintenance and vegetation work orders | a structure within 2, a span within 1 | dismissed own evidence and method shortcut as at R2 to R4 | R2, R3, R4 | Ask 4 |
| R9 | the memo's work list: each open repeat location's fix and the nine sections washed before 1 December | synthesis | RP-04's work list | exact set (every rival files the same 25 items) | dismissed own evidence and method shortcut as at R2, R3, R4 and R7 | R2, R3, R4, R7 | Ask 5 |
| R10 | the work list: 6 perch guards, 4 strings, 9 sections washed, 2 hazard-tree stands, 4 spans cleared | synthesis | RP-04's work list | exact set | dismissed own evidence and method shortcut as at R2, R3, R4 and R7 | R2, R3, R4, R7 | Recommendation |

Carry-forward: R7 is graded on inputs of its own (the test insulators, the washing log and rain; only its flashover level reads R6's fog faults, and that level moved 20 per cent leaves the same nine); R4 stands on Line 9's records alone; R2 and R3 fall only with their own stumps, never with each other; R8, R9 and the recommendation (R10) fall with whichever of R2, R3, R4 and R7 a run misses, and R1 and R5 stand on the conformed record a careful run builds by reflex.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Fault resistance and load flow biasing each single-ended relay distance (tree contacts at 14 to 38 ohms, insulator arcs under 1) | constructed by the physics: every fault solved on its sequence networks with its cause's resistance | no: every fault on every line, largest at the tree contacts | modelling: both ends' residual currents against the zero-sequence network | modelling | keep |
| Inland's autotransformer replaced on 14 March 2024, a stronger ground source behind Inland | constructed and filed (the substation register, both protection studies, the 2024 settings) | no: every fault on an Inland line before the date | a targeted query: the register's dates beside the studies' | routine once seen, inside S1's modelling | keep |
| The solar farm's grounded-wye step-up and neutral reactor feeding every fault beyond the tap | constructed by the physics and filed (the register and the 2025 study) | no: every Line 9 fault beyond the tap since February 2023, day and night | modelling: the infeed ratio from two exports on two clocks | modelling | keep |
| Bay fog the airport's codes miss and report; streamers at roosts; cracked strings in light rain | constructed by the weather and bird processes | no: every coastal night fault and every surveyed roost | modelling: the stations' dew point, the survey's structures, rain and hour | modelling | keep |
| Conductor heat on still afternoons for grow-ins; storms and fronts for fall-ins | constructed by the load and weather processes | no: every summer afternoon fault on every line | modelling: a heat balance per fault hour | modelling | keep |
| Each section's salt carried from its last wash or soaking rain | constructed by the deposit process | no: every coastal section | modelling: the rate fitted on the test insulators, carried through the washing log and rain | modelling | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the 69 kV faults by year, January 2022 to October 2026 | Partly | Right | Right |
| R6 the 2026 faults by cause | Missed | Partly | Right |
| R5 the 2026 member interruptions, member-minutes and momentary member events from 69 kV faults | Missed | Right | Right |
| R3 the night repeat locations: roost structures for perch guards and failing strings | Missed | Missed | Right |
| R4 the tap line's repeat location | Missed | Missed | Right |
| R2 the vegetation repeat locations: grow-in spans to clear and hazard-tree stands | Missed | Missed | Right |
| R7 the washing sections due before the fog season | Missed | Missed | Right |
| R8 every open repeat location with its cause and fix | Missed | Missed | Right |
| R9 the memo's work list: each open repeat location's fix and the sections washed before 1 December | Missed | Missed | Right |
| R10 the work list | Missed | Missed | Right |
| Roughly | 0.5 of 10 | 2.5 of 10 | 10 of 10 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: the solar farm's ground infeed taken out of Shell Ridge's distance; rescues 1 of 10 results
Pair estimate: 34.5

## Stump factorial

Reflex route: every move a run makes unprompted set right (one fault per protection sequence across both terminals' exports, the SCADA sequence of events and the control room log, vendor B's local time and the drifting clocks set on SCADA, R01, R28, R29, R46; lightning matched to strokes on the true time, R32; member impact from the sequence of events and members by feeder, R46; the patrols read and the work already done applied, R02), every stump hurried. It files the fault counts and the 2026 member figures right and misses the call: the relays' own distances on today's network place the grow-in spans at Line 10 35-36 and Line 6 48-49 and add Line 13 90-91, the airport's codes with no survey turn the roosts into failing strings (strings at 11 places, no guards), Shell Ridge's distance puts the tap line's string at structure 148, and every section that ever flashed over is washed (Line 1 section 3 and Line 2 sections 1 to 6, two of them washed in October). This route is the careful but hurried pass, 32 items off the golden's 25.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 each fault located by the split of its residual current between the two ends against the line-out zero-sequence sources | stump | the relays' own distances, both ends averaged | L22 | spans at Line 10 35-36 and Line 6 48-49, Line 13's stand split into 84-91 and 93-96, Line 11's stand, Line 14's span and Line 14 117's guards lost: 12 items off, R2, R3 and R6 move | the clearing list still carries Line 13 90-91 (S5) and misses Line 10 47-48 (S2), the night list stays strings: no result rescued | no (a two-port zero-sequence solution per fault) |
| S2 faults before 14 March 2024 read against the 2022 study | stump | the 2025 study for every fault | N09 | Line 10 47-48 loses its 2022 and 2023 contacts and drops off: 1 item, R2 moves | nothing else fixed: no result rescued | yes (the date-matched study), but invisible in any one table and only beside S1 |
| S3 the solar farm's ground infeed corrected out of Shell Ridge's distance with the farm's own residual current | stump | Shell Ridge's distance as recorded, the farm's export set aside | L38, N27 | the tap line's string moves from structure 137 to 148: 2 items, R4 moves | R4 only (1 of 10) | no (the infeed ratio per fault from two exports on two clocks) |
| S4 night coastal faults split three ways on the bay stations' dew point, the roost survey and the light-rain signature | stump | the airport's codes as the fog, the survey set aside | N26, L38, L26 | the six roosts and three other places as strings, no guards, Line 1 sections 2 and 3 and Line 2 section 6 washed: 18 items off, R3, R6 and R7 move | R3 only on the night faults' cause, still placed by the relays: no result rescued | no |
| S5 grow-in contacts told by the conductor's temperature on still afternoons, storms and fronts set apart | stump | every summer afternoon fault with no stroke | L26, L04 | Line 13's pine stand also listed as a span at 104-105: 1 item, R2 and R6 move | with S1 hurried the spans stay misplaced: no result rescued | no (a conductor heat balance per fault hour) |
| S6 each coastal section's deposit carried from its last wash or soaking rain at its own rate against the flashover level | stump | every section with past flashovers | N02, N13 | Line 2 section 6 (washed 21 October) on, Line 3 sections 4 and 5 off: 3 items, R7 moves | with S4 hurried the flashover level is learned from mixed faults: R7 still wrong | no |
| X1 one fault per protection sequence, clocks set on SCADA | reflex | - | R01, R28, R29, R46 | the fault count moves by several a year | - | - |
| X2 lightning matched to strokes on the true time | reflex | - | R32 | lightning counted under other causes | - | - |
| X3 member impact from the sequence of events and members by feeder | reflex | - | R46 | the 2026 member-minutes from the dispatchers' closing times | - | - |
| X4 the work already done applied (guards fitted, strings replaced, spans trimmed after a contact) | reflex | - | R02 | fixed places stay on the list | - | - |

Level: 5 (six stumps, each necessary; none reaches the call alone; the single drops land on six different wrong work lists)

## Data provenance

Source: generated by the generator (task13/generator, seeds 51301 to 51303) from a simulated cooperative: a 69 kV network of 12 substations, 16 lines and 1,868 structures with its weather, loads, fault processes, protection, operations and field work, each written into its own system's export
Behaves like the real thing: single-line-to-ground faults solved on sequence networks with each cause's fault resistance, so single-ended reactance distances run long or short with resistance and infeed as published single-ended locator studies show (IEEE C37.114); conductor temperature from an IEEE 738-style heat balance; equivalent salt deposit density building with nearness to the Gulf, partly kept by soaking rain and reset by washing, flashing over in fog above a level as contamination studies describe; streamer faults at roosts before dawn in the roost season; member interruptions on IEEE 1366's five-minute line
Genuine patterns: (1) summer convective lightning and grow-ins against the winter roost and fog seasons (2) the deposit gradient from the shore inland (3) daily load and solar cycles carried into conductor temperature, load growth across 2022 to 2026 and the 2026 drought after June
Problems by process: two relay vendors' exports (UTC and miles; local time, km and kA); relay clocks drifting until resynchronised; records lost to overwritten buffers; electromechanical relays at Ponder Creek keeping only targets; structures renumbered after rebuilds; outage-system restorations closed late by dispatchers; operators' cause codes from the weather look; station telemetry gaps; airport units; the solar farm's export on standard time all year
Breadth: 28 files, two of them unused; 436 faults on 16 lines; 1,868 structures; 2,070 relay records; 42,779 SCADA events; 62,856 strokes; 184,944 station-hours; 42,332 hourly loading rows; 12,617 outage-system rows; which record sees which part of a fault is the work

## Template check

Chain signature: assembly and reconciliation, missingness and measurement, investigation loops, missingness and measurement, decomposition and attribution, exploration and triage, forecasting, synthesis (the card's)
Question form: what (what goes on the work list), with three deliverables asked by type
Nearest build: task6 v7 shares the flagged-set shape (precut's nearest-chain WARN), but its chain runs from a trace store's keep rate through uncertainty to attribution and none of its steps carries here; task9 v3 by skeleton (a fab's sort-yield shortfall split across tools, ranked causes with their contributions): one shared lesson, a 0.50 file-role overlap, severity none; task22's feeder energy balance (energy and ETL, the pairing registered with --force at the author's direction) sat on measurement with a reconciled balance as its answer, another chain and shape

## Frontier check

Precedents: R2 L22 (method shortcut), N09 and L04 (dismissed own evidence), L26 (stopped at the first story); R3 N26 and L38 (dismissed own evidence), L26 (first story); R4 L38 and N27 (dismissed own evidence); R6 N26 and L38; R7 N02 and N13 (dismissed own evidence); R8 L22, N09, N26, L38, N27, L26; R9 and the recommendation L22, N26, N02; R1 and R5 are Right, earned by the runs' reflexes (the hygiene battery and the SCADA rebuild)
Shallow path checks: R2's hurried clusters repeat tightly because each relay's bias is the same at every contact, so a consistency check passes; the residual split from both exports against the studies refutes it, and the patrols sent to the relays' distances found nothing; R3's and R6's hurried labels agree with the control room's contamination codes, both read off the airport; the stations' dew point at the line, the survey's structures and the pre-dawn November to March timing in any weather refute them; R4's Shell Ridge distances agree with one another at structure 148; the farm's own residual current (another export, another clock) with the step-up's data in the 2025 study refutes it at 137; R7's history list reproduces every past fog flashover by construction; the washing log (two of its sections washed in October) and the deposit carried to 31 October from the test insulators' rate and the rain refute it
Assumption made false: a run lists "the relay's fault location is accurate", "the airport's weather stands for the lines", "the network has not changed", "the generator's log is unrelated" and "past flashovers mark where the salt is" and waves them through; here the locators assume no fault resistance and no infeed while tree contacts burn at 14 to 38 ohms, the bay fog misses the airport, Inland's ground source changed in March 2024, the farm's step-up feeds ground current at all hours, and a section washed in October holds little salt, each tested from a second file at another grain (the other end's export and the studies, the stations and survey, the register, the farm's export, the washing log and test insulators)
Forcing: a set decision of 25 items; the 18 golden-family rivals each file the identical 25 (nearest distance 0), six input perturbations (the deposit rate and the flashover level by 20 per cent, the conductor threshold by 4 C) each file the identical 25, and the shortcuts land 1 to 32 items away on seven distinct wrong lists (S2 or S5 hurried 1, S3 2, S6 3, S1 12, S4 18, the reflex route 32)
Noun swap: the nearest by skeleton.py check is task9 v3 (a fab's sort-yield shortfall by tool): its nouns swapped in carry no decision form (a reconciled record against a ranked bridge), one lesson (position on a network), none of the mechanisms and only generic detections and answer pattern; severity none, and none against the client's corpus or this slot's lineage
Closed strategies: the call turns on position_on_network_effect (each fault's place from the zero-sequence network behind both ends), which is not on the client's closed page; the nearest closed cards are instrument change (no instrument changed: the locators compute as they always did, and their bias is physics on every fault) and dependent capture (the relays capture every fault; their number is biased, not their capture); the chain keeps no closed lesson as a supporting step (skeleton.py closed: 0 of 4 lessons closed)

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a fault | each breaker trip; each protection sequence on one line | one protection sequence (trips, reclosing, lockout within 60 s) on one line | RP-04 "Fault": the sequence counts once; switching, testing and maintenance operations are not faults; a fault another line's relay sees without tripping is not that line's |
| SF2 | since January 2022, each year, 2026 | calendar years; 2026 to date of the files | 2022 to 2025 whole, 2026 1 January to 31 October | RP-04 "Year"; no fault crosses a year boundary between UTC and Central |
| SF3 | where it was | the relay's distance; the structure | the structure nearest the fault, numbered as today; a span by both numbers | RP-04 "Fault location" |
| SF4 | what caused it | the operators' codes; the outage system's codes; the procedure's categories | the nine causes | RP-04 "Cause" |
| SF5 | repeat location | any two faults near each other; three of one cause within 400 m | three or more of one cause on one line within a run of 400 m or less since 1 January 2022, salt left to washing | RP-04 "Repeat location"; the 350 m and 450 m windows file the same list (same call) |
| SF6 | fixed | any fix ever; a fix after the last fault | a fix of that cause after the location's last fault | RP-04 "Work list": "whose cause has not been fixed since its last fault" |
| SF7 | member interruption | any outage; more than five minutes | more than five minutes; five or less is momentary | RP-04 "Member interruption"; no restoration falls between 21 seconds and 6 minutes |
| SF8 | member-minutes | to the dispatcher's closing; to supply restored at the member's substation | to the restoration of supply to the member's substation | RP-04 "Member interruption" |
| SF9 | by line | the line serving the members; the faulted line | the faulted line, which is the line serving its tap's members at the time | same call |
| SF10 | the work list | the repeat locations; with the washing | each open repeat location with its fix and each section due for washing | RP-04 "Work list" |
| SF11 | due for washing | sections with past flashovers; the latest test reading; the section's deposit on 31 October | the section's deposit on 31 October at or above the flashover deposit | RP-04 "Due for washing before the fog season": the deposit is on the section's porcelain on 31 October, and the test insulators are never washed |
| SF12 | the deposit at which the porcelain has flashed over | the lowest at a past fog flashover; the 5th or 10th percentile | the lowest at a past fog flashover | same call (all three file the same nine sections) |
| SF13 | this winter and before summer 2027 | the order of the work; the list | the list; washing before 1 December, the fog season's start | RP-04 "The fog season runs from 1 December to 31 March"; no other timing is graded |
| SF14 | the 69 kV system | the lines; the lines and taps | the 16 lines in the line register, the solar tap's spur part of Line 9 | the line register's Lines and Solar tap sheets (same call) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every protection sequence on the 16 lines from 1 January 2022 to 31 October 2026 (RP-04 "Fault" and "Year"); feeder breakers are 12 kV, single-ended trips with no fault record are relay tests, backup-zone pickups are other lines' faults; C1 asserted on the count |
| 2 | Unit of account: one fault per sequence per line; one repeat location per structure or run; one washing section per the log's Sections sheet |
| 3 | Attribution window: each fault's Central date sets its year; none crosses a year boundary between UTC and Central (C1, asserted) |
| 4 | As-of dating: 31 October 2026 for the deposit and the work done; today's inventory for structure numbers (RP-04) |
| 5 | Version basis: the network as it stood at each fault (the register's 14 March 2024, both studies); structure numbers as today (RP-04) |
| 6 | Denominator: none; every result is a count, a sum or a set |
| 7 | Weighting: none |
| 8 | Window length: repeat locations since 1 January 2022 (RP-04); the deposit rate fitted on every test reading, its rivals filing the same nine (C1) |
| 9 | Boundary inclusivity: "at or above", "more than five minutes", "no more than 400 m", "three or more" (RP-04); nothing sits on a boundary (the level moved 20 per cent, the window 50 m, the same list) |
| 10 | Rounding path: counts exact; member-minutes summed then rounded once, graded within 2 per cent |
| 11 | Tie-break: none; no ranking is graded |
| 12 | Maturity and censoring: 2026 runs to 31 October (RP-04); no outage is open at that date |
| 13 | Order of operations: locate, cause, group, then take off what was fixed after the last fault (RP-04 "Work list"); grouping before or after the fixed check files the same list |
| 14 | Row order: none; faults sorted by time |
| 15 | Duplicate resolution: each export's rows per reclose shot collapse to one fault per sequence; two terminals' records are one fault (RP-04 "Fault") |
| 16 | Identity normalisation: relay names to lines through the settings workbook; Lines 8 and 13's former numbers through the inventory; the solar farm's events to Line 9 faults by time on standard time |
| 17 | Netting against gross: none |
| 18 | Dimensional units: miles and km, amperes and kA, Fahrenheit, knots, statute miles and inches at the airports, mg/cm2 for deposits; each carried in its file |
| 19 | Code and status semantics: the operators' and the outage system's cause codes are their own records, not RP-04's causes, and no result reads them as such |
| 20 | Integerisation: counts and members are whole by construction |
| 21 | Clause scope: salt contamination is left to washing and is not a repeat location (RP-04); insulator failure is one |
| 22 | Forward window contents: the fog season, 1 December to 31 March (RP-04); the washing is judged on the deposit on 31 October, and no future fault count is asked |

## Literal reader

The prompt asks what goes on the 69 kV work list, a CSV of every 69 kV fault since January 2022 with where it was, what caused it and its member interruptions and member-minutes, a workbook with faults by line and cause each year, the 2026 member interruptions and member-minutes by line and every repeat location with its cause and whether it has been fixed since its last fault, and a one-page memo with the work list. Read word for word against RP-04 Rev 4 those execute to: 436 faults (96, 93, 83, 84, 80 by year); the 2026 causes (9, 6, 16, 16, 14, 8, 5, 2, 4); 57,024 member interruptions and 1,227,611 member-minutes, by line; the 16 open repeat locations with their causes and the seven fixed after their last fault; the nine sections whose 31 October deposit is at or above the lowest deposit at a past fog flashover; and the 25-item work list. No sentence names a method, and every reading a sentence leaves open files the same results or is ruled out in the fork table.

## Prompt contract

A voice rewrite keeps: the question (what goes on the 69 kV work list for the 2026-27 winter and before summer 2027); the CSV of every 69 kV fault since January 2022 with where it was, what caused it and its member interruptions and member-minutes; the workbook's three parts (faults by line and cause for each year, the 2026 member interruptions and member-minutes by line, every repeat location with its cause and whether it has been fixed since its last fault); the one-page memo with the work list; three deliverables, each by type. It never adds a rounding instruction, a method or step (no "two-ended", "residual", "infeed", "fog stations", "survey", "conductor temperature", "deposit model"), a warning, an attached file's name, a role or reader, or a count the data hold (436 faults, 16 lines, 25 items).

## Leak review

leak.py (as of 2026-11-12) REVIEW, each line ruled: `lightning_strokes_2022-2026.csv` "294,124" is one stroke's error-ellipse axes (semi-major 294 m, semi-minor 124 m) sitting side by side, a coincidence of digits with Line 13's member-minutes, harmless; `reliability_reporting_procedure_rev4.docx` carries the stump terms and column words because it is the cooperative's own reporting procedure defining the fault, the location, the causes, the member interruption, the repeat location, the work list and the washing rule (the WHAT), and its records section lists the systems of record by owner, naming no step, comparison or method, harmless; `relay_records_gridvue_2022-2026.json` "generated" and "device" are the vendor export's own envelope and record keys, harmless; `substation_weather_stations_2023-2026.csv` "air_temp_c" is the station historian's export header beside "rh_pct" and "rain_mm", harmless.

## Pre-ship check

- Card registered with --force on ban.pairing only (energy x ETL against task22, the author's assignment of 2026-11-12,
  reason in the card's notes); skeleton severity none against every card, lineage entry and client task (nearest
  task9 v3); the deciding lesson (position on a network) off the closed page; the frontier check written; the cited
  pair estimate 34.5.
- The process behind the files simulated before any result was named (network, weather, loads, fault processes,
  protection, operations, field work); the weight (assembly) differs from the last two live cards (measurement,
  attribution).
- Ten results across seven areas, each pinned, banded and graded; no analytical result is the only input of more than
  half the others (R8, R9 and R10 are the synthesis rows).
- Every factor runs across the data (the hidden factor record): fault resistance on every fault, Inland's source on
  every Inland-line fault before March 2024, the solar step-up on every Line 9 fault past the tap, the bay fog, roosts
  and cracked strings on every coastal night fault, conductor heat on every summer afternoon fault, the deposit on
  every coastal section; checks.py holds the golden against the world (37 of 37).
- The effort test measured by effort.py: quick 12.5, careful but hurried 34.5, thorough 100; the largest single hint
  rescues 1 of 10; the stump factorial at level 5 (six stumps, each necessary, none sufficient).
- Forcing on both sides: 18 rivals and six perturbations file the identical 25-item list; the shortcuts land 1 to 32
  items away on seven distinct wrong lists.
- Gates on the final cut: precut, effort, voice, leak (REVIEW, ruled), figures, containers, surface; heart BLOCKs only
  on the pairing above; checks.py 37 of 37, verify.py 12 of 12 (an independent recompute from the pack); two builds
  byte-identical.

## Tried and rejected



- A smart-meter outage-alert rollout recording small outages that customer calls missed, as the decisive layer:
  rejected at the draw, 2026-11-09. Which comparison is clean (recorded against experienced) is the estimand, so
  filing it spends the layer and leaving it open is a fork (`determinism-check` section 1).
- A random scratch world (feeder size and tree density drawn freely): the three-year count and the wind-normalised
  rate alone reproduced four to six of the golden six on five seeds, because size dominated; the world is built from
  groups (overdue northern feeders, dense plantation feeders trimmed recently, southern late-cycle feeders, overdue
  feeders with few trees) so each shortcut lands on a different wrong list.
- A one-year wind anomaly carried by the station's mean level: the decomposition fitted without the wind still landed
  four to five of the six, because one year is a small share of the outage record and a higher mean moves every gust
  alike; replaced by three years in which the storm track sat south (fewer strong-wind days in the north, about twice
  as many in the south, mean wind within 6 per cent) over an outage record from April 2022.
- Plantation feeders trimmed early in 2025 on a four-year cycle: their growth left them among the golden six; moved to
  a three-year cycle cut in the second half of 2025, which keeps them first on every recent count and on expected
  interruptions and last on the growth a catch-up removes.
- Major event days set by the 2.5-beta rule on the record: wind-storm days crossed the boundary and carried a fifth of
  the strong-wind hours, so the projection's treatment of those days moved the six's total by half; the filed
  boundary values now sit above every storm day, and the major event days are the five snow days.
- Hours of gusts of 60 km/h or more as the golden's exposure: 30 feeder-months with vegetation interruptions had no
  exposure at all, and the six's total moved 28 per cent across thresholds; the gust load, which fits the record best, is
  the golden, and the hour counts stay in the family (same six).
- Architecture 1 as a whole (Kotuku Networks' 2027 vegetation catch-up, READY 2026-11-09, never run on the platform):
  re-rooted 2026-11-11 at the author's word, for a stronger chain with at least three independent analytical failure
  points. Cut under the retired single-deep-step design: one Poisson fit carried every graded figure, the plantation
  feeders' dense corridor sat only in the deciding units with one filter as its fix, and the storm-track swing showed
  in one plot of gust hours by station.
- Architecture 2 at the prototype, a referral on the latest season alone: with about eight sound faults a zone-season
  the failed zones (2.2 to 3 times their sound rate) were referred at p near the threshold; the window became the
  seasons since the zone's last cyclic inspection, as the programme terms file it.
- Architecture 2 at the prototype, the sound expectation fitted on the season after each inspection only: 172
  zone-seasons of about eight faults could not show the sound zones' spread (the moment estimate of the negative
  binomial size ran to infinity) and the referral set swung from 0 to 10 zones with the dispersion; the expectation and
  its spread are fitted on every season a later cyclic inspection confirmed sound (410 zone-seasons, size near 25).
- Architecture 2 at the prototype, line arresters with no effect on direct strikes: losing them lifted a zone's
  lightning faults about 1.9 times, inside the scatter of sound zones around any design model; arresters every few
  spans now also drain part of a direct strike's current, so a zone that loses its ground leads or arresters runs 2.5
  to 4.5 times its sound rate, as the field's line arrester studies show.
- Architecture 2 at the build, the likely failed part at each referred zone (ground leads from burnt transformers per
  lightning fault, arresters from arrester failures in fair weather, insulators from the lockout share) as a graded
  result: on the cut pack 8 of the 15 referred zones carried no signature above one standard error and the pick agreed
  with the simulated state on 10; a result whose golden turns on noise is an open fork, so it left the chain, the
  prompt and the programme terms (3(c)).
- Architecture 2 at the build, the careful pass at one fixed offset per radio-less controller: it finds one fault in
  fourteen on those zones (19 of 259 in 2026), a gap a run would see; the careful pass matches them on a ten-minute
  window around their own stamps instead, which counts storm trips as lightning (212 logged against 163).
- Architecture 2 at the build, the inspection check counted per referral (terms 5 as first drafted: a referral is
  confirmed when the zone's next inspection finds failed protection): a zone referred after three seasons counted
  three times under one reading and once under another, and on a one-zone band a hurried rule landed it by chance;
  terms 5 now checks each inspection against the rule after the season before it, and the three counts are exact.
- Architecture 2 at the build, 2026's faults caused by failed protection left to the question's words: the referred
  zones' excess (199) and the sum of every zone's positive excess (415) read it as well as the network's faults less
  every zone sound (279); terms 2(f) files the quantity.
- Architecture 2 as built (the radio-less clocks, the overwritten and unread months, and the inspection-confirmed
  baseline as its three difficulties), judged DETERMINISTIC and FIX_NOW at stage 4 on 2026-11-11 and sent back to stage
  2 by the judge thread's own first pass, which landed five of the eight results and part of a sixth in seven minutes:
  each difficulty was noticing a property the files show plus the field's standard remedy (a scheduled self-test that
  leaks the clock offset, event-number gaps that announce the losses, an inspection book whose time order names the
  confirmed seasons), which a careful run does by reflex.
- Architecture 3 at the design, each zone's own level on the 2022 to 2026 record alone: with at most four confirmed
  seasons a zone, the worlds where the levels moved the set (4 to 14 zones against a pooled scatter) were the ones whose
  golden moved under its own rivals (the level shape at 0.7 and 1.4 times its estimate, the match radius), and the
  robust worlds were the ones where the levels decided nothing; the record now runs from December 2016, two inspection
  cycles confirm 779 zone-seasons, and every rival refers the same set.
- Architecture 3 at the design, the hurried route as one negative binomial over the whole record: it behaves as a level
  per zone by accident and lands within a zone of the golden; the routes a run takes treat the seasons as independent
  (quasi-Poisson, as the stage 4 judge did, or a negative binomial each season), and those refer 13 zones to the
  golden's 11 and check sound zones at inspection.
- Architecture 3 at the build, the alert counts and the rule's sound referrals graded as two results: the prompt asks
  them in one sentence as the rule's alert load, and as two the levels sentence rescued three of eight; one result of
  six cells, and the chain is seven.
- Architecture 3 revision 1 (as judged at stage 4 on 2026-11-11, DETERMINISTIC and APPROVE): its judge thread's own
  first pass missed the set, the season totals and the failed-protection count but landed two results the note priced
  as lost, the refit's avoided faults (terms 4(c) filed "the faults its zones ran in the last lightning season", a
  method, and the pass executed it: 102 to 121 against 116) and the rule's sound referrals (the pass computed the
  rule's own rate, 0.13 to 0.15; quoting the budget's 0.2 was never a run's reading). Repriced on that pass the careful
  column came to about 56, 65 with the replay's cells, over 50, so the build went back to stage 2: terms 4(c) now files
  the state at the end of 2026 and leaves how to read it to the data, the level's uncertainty is priced as its own
  judgment (the known-level rule refers 17), and every band is the rival family's span.
- Architecture 3 as a whole (Kalumpang Valley Electric Cooperative's lightning referral rule, READY at 17912c6 on
  2026-11-11): a platform run landed every result (task13/runs/run1.md: the same 11 zones, the season totals, the
  failed-protection count, the alert load, the inspection check and the avoided faults inside their bands): each zone's
  level as a random effect with its uncertainty in the predictive tail, the threshold checked by an all-sound
  simulation, the clocks rebuilt from upstream and downstream pairs on a whole-visit hold-out and the latest window for
  the refit were reflexes (precedents R26 to R32), and every assumption it named and waved through (the 2026 topology
  for all history, missing periods at the observed rate, a passed inspection as proof of soundness, the latest rate as
  the end state) was true in that world; the lightning world had spent two architectures, so architecture 4 moved to a
  new world, dataset and shell, each priced result built on one of those assumptions made false by the process.
- Architecture 4 at the draw, a distribution transformer fleet (EV overloads, a defective 2015-18 batch, the 2026 heat):
  its judgments sat on survival and thermal-ageing fits, the frontier run's home ground, and its decision was a list of
  some 300 units no rubric can grade; the FLISR fleet maps each priced result onto an assumption the run names.
- Architecture 4 at the draw, URD cable sections for a 2027 replacement programme: survival with left truncation,
  vintage and frailty, which the run fits by reflex; the decision a long list of sections.
- Architecture 4 at stage 4 (judge, 2026-11-11: DETERMINISTIC, SEND_BACK on Gate G), the call headed by the walk
  from the vendor dashboard's 27,370: two of its bars were a definition (the five minutes) and a coverage gap applied to
  the same sequences, so the headline read as a surface-read rejection whatever the netting beneath it; re-framed in the
  same world, the call now leads with the controls, the receiving settings and 2027, the 2026 figure is asked as one
  number on the order's definition, and the dashboard stays in the pack as the vendor's report (deleting it leaves
  every result as hard).
- Architecture 4 at the design, the counterfactual customer minutes (control room switching time by workload) as a
  result: the automation's restorations and the control room's own remote switching ran at the same workloads, so the
  conditioned and pooled counterfactuals agreed within 2 per cent; a careful run would land it.
- Architecture 4 at the design, the summer receiving-feeder figure asked in the prompt: the asking sentence would have
  told every run that transfers interrupt the receiving feeders and handed over the 2026 netting; it stays a component
  of the summer recommendation, asked only as what to change before next summer.
- Architecture 4 at the design, turning summer auto-transfer off where it does net harm: with the restored customers
  outnumbering the receiving section's, a transfer's expected net stayed positive on every direction; the decision is
  the receiving settings, which always pay, and the figure is the harm left if they stand.
- Architecture 4 at the design, the 2025-26 failed restorations by cause: the cold-crank failures numbered two or three
  in two winters, too few to grade the radio against battery split; the batteries carry their own forward result.
- Closing the summer window (judge p2, Gate E on R4) by convergence alone: June to August (364) and May to September (432) land inside 318 to 455, but 21 June to 22 September (about 300) and July to August (241) do not, and the receiving trips the record holds fall in March, June, July, August and November, so the record does not define the season; the design basis now files the seasons as its own line.
- Grading the summer figure as a Critical Component: the prompt asks for the memo's what and why, not the figure, so a heavily weighted criterion on it would be graded on something not asked; it moved to the memo's ask (Supplementary 5), and the components' second share goes to R5, which the recommendation and the third component carry (the careful pass's estimate stays 34.5).
- A summer-transfers sheet described in Supplementary 4: the prompt never asks for it; the sheet stays in the golden workbook as working, undescribed.
- The golden's R1 counted the breaker's re-close onto section 1 only when the ADMS also closed the tie, and the world-truth check in checks.py shared that condition, so both missed GTH531 on 14 February 2026 (452 customers, re-closed at 110 s, the tie close timed out) after READY 5f9b2ca; the p3 judge's straight outage-record route found it at 25,508. Fixed in operations(), the walk (the failed sequences' item), verify.py's own breaker pass, and a truth anchor rebuilt from the world's outage steps.
- The 2027 forecast credited only the transfers (24,679 at READY, 24,394 on the corrected record): the record shows the breaker re-closing onto section 1 in 11 of 15 breaker lockouts for a section 2 fault, about 1,400 customers a year; and breaker lockouts the scheme never located defaulted to section 1, where the repair step types three of them as section 2. Both now in forecast(); the transfers-only figure is a ruled-out route.
- Architecture 4 as a whole (Blue Earth Valley Power's 22 automated loops, READY at 5f9b2ca and RESHIPPED at 7a6d186,
  uploaded): the platform run landed R1, R2 and R3 (the five yearly restorations exactly, 21,780 by the same walk, the
  golden's 16 controls plus RCL-20378) and the holistic audit of 2026-11-12 returned it on determinism (the battery list
  turned on the fitting window, the 2027 figure on four unpinned treatments, task13/runs/arch4_run1.md). Every priced
  move was made unprompted (the lockouts rebuilt from SCADA, the receiving trips netted, each battery's ageing fitted),
  and a forecast total carrying four conventions could not be both forced and hard; the world was spent, and the author
  reassigned the slot to Energy Systems & Utilities x Data Extraction & Conformation on 2026-11-12, so architecture 5
  moved to a new world, dataset, decision form and shell.
- Architecture 5 at the build, the Line 13 stand's pines falling only with fronts: no fall-in cluster carried summer
  afternoon faults, so the conductor's temperature (S5) moved nothing; the dead pines now come down in summer storms as
  well as fronts, some of them permanent, so counting every summer afternoon fault with no stroke as a tree lists the
  stand as a span.
- Architecture 5 at the build, each summer fault caused by its own hour's conductor temperature alone: the 44 C rival
  moved two spans; a cluster's cause is settled on the share of its faults on still summer afternoons, and every
  threshold from 36 to 44 C files the same list.
- Architecture 5 at the build, insulator flashovers at up to 5 ohms of fault resistance: the tap line's infeed
  correction carried errors near 0.85 km (about four structures) and the tap string's band failed; an arc across a
  cracked porcelain bell burns at 0.3 to 0.9 ohms, and the corrected distance now lands within a structure.
