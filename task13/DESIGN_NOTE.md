# task13: what Blue Earth Valley Power's automated loops really avoided in 2026, what to change before the winter and the 2027 summer, and what they will avoid in 2027

## Draw

Subdomain: Energy Systems & Utilities, task type grid reliability and outage analysis (`grid-reliability-outage-analysis`, the only energy task type serving the assigned analysis type)
Analysis type: Anomaly Detection & Diagnostics
Answer shape: a flagged set with the evidence (the recloser controls to re-battery before the winter and the transfer
  directions whose receiving settings must change before the summer, each with its evidence), beside 2026's customer
  interruptions avoided on the commission's definition and 2027's as the loops stand
Weight: a hard-to-measure quantity: what an automatic restoration scheme changed across the whole network is in no
  record; the ADMS archive holds what the scheme logged, minus what it lost on storm days, and none of what its
  transfers did to the receiving feeders hours later; the last two live builds sit on investigation (task7 v9) and
  metric or rule design (task9 v2), and architecture 3 sat on metric or rule design
Data-native sentence: a FLISR restoration is worth the customers it moves from a sustained interruption to a momentary
  one, less the customers its own switching then puts out, and whether a transfer holds depends on the coincident
  load through every protective device on the receiving path at the hours after the fault, while the archive that
  records the scheme loses its busiest days and the controls that carry it out are tested only in mild weather.
People: Shawn Hudson (manager of grid modernization performance, files the 2026 report with the commission), Nathan
  Reeves (distribution automation engineer, the golden's author), Elaine Stewart (system protection engineer), Jacob
  Barton (distribution operations superintendent), Debra Reed (regulatory affairs director, signs the filing),
  Ruben Nicholson (capital projects manager); drawn with `guard.py names --geo "United States"` at seeds 1341 and 1347;
  none is named in the prompt

**The decision.** Blue Earth Valley Power, an investor-owned distribution utility in southern Minnesota, runs 13.8 kV
feeders from nine substations; 44 of them are paired into 22 loops automated for fault location, isolation and
service restoration (a substation breaker, two midline reclosers and a normally open tie switch per loop, run by the
ADMS). The commission's grid modernization order has the utility report each year the sustained customer
interruptions the automation avoided. The vendor's dashboard reports a gross figure from the ADMS archive. Before the
March 2027 filing the utility must say what the loops really avoided in 2026, which loops, controls and transfer
directions are not performing and why, what it will change before the 2026-27 winter and the 2027 summer, and what the
loops will avoid in 2027.

**Card.** `.claude/skills/fingerprint/cards/task13.json`, architecture v4, registered 2026-11-11 (23:18Z), guard verdict
WARN. Answered: `repeat.decision` against task7 v9 (there one fund-or-not call per measure; here which controls to
re-battery and which transfer directions to run without summer auto-transfer, a designation unit by unit beside the
net figures); `repeat.deliverables` against task7 v9 (the commission's filing takes a PDF memo, and the workbook is the
engineer's); `skeleton.lesson_once` (downstream_offset is taught once, by the client's turbine-wake task 8ec45b05, as a
go or hold on one unit's repair; here it is netted across 44 transfer directions inside a chain of four lessons whose
other three no accepted task teaches); `skeleton.house_lesson` on validation_cannot_see_condition (mark258, task20 v2,
task7 v9) and linkage_missing_not_at_random (task16 v2, task19 v1): both are supporting judgments here, each priced on
its own result (the cold-crank controls; the storm days the archive lost), never the lesson the call turns on.

## Deep reasoning

Task type: grid reliability and outage analysis (`grid-reliability-outage-analysis`), the energy task type serving Anomaly Detection & Diagnostics.
Domain test: the results are the quantities a distribution automation engineer owes the commission: sustained customer interruptions avoided under the five-minute rule, the receiving path's coincident load against each recloser's pickup at the hours faults strike, a control battery's cranking voltage at the design minimum, and a forecast at the record's lockout rate with the planned works at their likely dates.
Swap: with a hospital's or a warehouse's nouns there is no tie switch carrying one feeder's load through another's reclosers, no settings group, no five-minute momentary line, no cold crank at 30 A; the net, the summer figure and the battery set stop making sense.
Where the weight sits: the 2026 figure the order defines is in no record: the archive holds what the scheme logged minus its storm overflows, the outage record holds the receiving feeders' trips as no cause found, and only the device record joins them; the work is long because every operation has to be rebuilt and its consequence on the next feeder found.
Layer 1: the archive in UTC under two message formats and device tags either side of the March 2025 upgrade, with the standby server's echoes; the outage record in Central prevailing time with the feeder written two ways; the SCADA historian in Central Standard Time, wide, with gaps where a radio path was down; the airport weather in Fahrenheit and knots with M for missing; each is what that system writes, and none moves a graded figure once read correctly.
Not one thing: a run told that transfers trip unswitched receiving reclosers still has to find them in the device record, net them by the order's definition (the restored customers undone and the receiving customers added), carry them to the 2027 summer at the reinforcements' likely dates, fit every battery to the cold and age it to February, and rebuild the storm overflows' operations; that one sentence rescues none of the five results by itself.
One-fact test: every hint executed on the careful pass end to end (effort.json hints): the transfer-trip sentence rescues R2 only (R5 moves to 26,482, outside 23,712 to 25,405; R4 needs the replay and the slip); the battery sentence rescues R3; the reinforcement-slip sentence and the duration-and-overflow sentence rescue nothing the careful pass lacks.
Not semantics: every column and clause read correctly still leaves the receiving trips unlinked to the transfers, the batteries judged at a temperature they will not meet, and the reinforcements in service months early.
Not rule application: no filed procedure finds the receiving trips, fits a battery's cold resistance, replays a transfer on the summer loads or dates a planned project; the order files only what is counted.
Estimand: order paragraphs 2 to 5 file CIA (sustained interruptions they would have had without automatic restoration, less those they had), the five minutes from the first loss of supply, the usual switching as the counterfactual, all days, and the forecast at the average annual lockout rate since 1 January 2022 with the schemes as they stand; the design basis files -27 C, the 5 A test, the 30 A operation at 21.2 V and the seasons (summer 1 June to 30 September, winter 1 December to the end of February); the prompt files 2022 to October 2026, the end of February 2027 and the 80 per cent range.
No decoy: the vendor dashboard is the incumbent figure, the right count of a shallower quantity (completed sequences in the archive); the walk prices it on the order's footing; no document argues a wrong answer.
No replay: no published figure is re-derived; the dashboard is superseded, not reproduced as the answer.
Pinned: each result's rivals run on the cut pack: R3 under a per-battery cold coefficient, the end of January, -26 C, -28 C and a mixed model (each control's level and ageing drawn around the fleet's) moves at most two controls at the 21.2 V line (stated as the margin), and the tests themselves rule out one fleet fit, one per control type, a linear resistance and each control's level with the fleet's ageing (control levels F 218.3 on 87 and 9,395, control ageing F 101.2 on 87 and 9,308, both p below 1e-15, cold slopes F 1.2, p 0.11; fitted to October 2025 those miss last winter's 170 tests below -15 C by 0.31 to 0.64 V at 30 A against 0.12 V for each battery's own fit, naming 0 to 11 controls); R4 under a 1.05 peak factor, every summer hour alike and a reconductoring-only slip lands 328 to 441, inside 318 to 455, on the design basis's summer (June to August gives 364 and May to September 432, both inside; July to August 241 and 21 June to 22 September, about 300, fall outside, hence the filed seasons); R2 and R1 count from the records.
Run forecast: R2 method shortcut (the restored loop priced alone); R3 dismissed own evidence (the battery judged where it was tested); R4 dismissed own evidence (the plan's dates, the past summers carried); R5 method shortcut; R1 is earned by careful runs.
Strategy label: UNTESTED (no client strategy covers a FLISR fleet diagnosis)
Depth level: 5. Four independent judgments (the storm overflows' operations from the device record, the receiving trips netted by the order, each battery carried to the cold and to February, the reinforcements at the completion the record supports), each moving its own result, and the shortcuts land on four different wrong answers (the dashboard's, the gap-filled archive's, the careful pass's and the plan-trusting route's).
Lesson: an automatic action's value is what it changed across the system, net of what it did to the units that absorbed it, read from the record that saw every operation rather than the one that logged the action; no build on file teaches the netting inside a fleet diagnosis.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | customers restored within five minutes of the first loss of supply, each year: 2022 32,875; 2023 25,796; 2024 28,781; 2025 22,561; 2026 25,056 | assembly-reconciliation | order paras 2 and 3; the device record's closes timed from the first trip | 2 per cent each year | dismissed own evidence: the lockouts the archive does not hold filled at its own success rate (2026 27,654), or the dashboard's counts | - | Ask 1 |
| R2 | 2026's customer interruptions avoided on the order's definition: 21,328 (25,056 restored within five minutes, less 2,407 undone and 1,321 receiving customers) | decomposition-attribution | order para 2; the receiving trips between the ADMS tie close and the operators' opening | 2.5 per cent | method shortcut: the restored loop priced alone, no receiving trip netted (25,056) | - | Component 1 |
| R3 | the 16 controls whose batteries will not operate at -27 C by 28 February 2027 (14 at every rival, RCL-20188, RCL-21643 and RCL-21281 at the line) | missingness-measurement | design basis (5 A, 30 A, 21.2 V, -27 C); prompt's end of February; each battery's own ageing, which the load tests select over a fleet or per-type fit | the 14 with or without the three at the line | dismissed own evidence: each battery judged at last winter's coldest test as it stood (2 controls) | - | Recommendation |
| R4 | the receiving feeders' own customers June to September 2027 transfers would interrupt if the settings stand: 388 | causal-reasoning | the design basis's summer; the unswitched directions read from the archive and the register; the capital works record; the approved load | 318 to 455 | dismissed own evidence: the 2025-26 summers' average carried forward (582), or the plan's in-service dates (237) | - | Ask 3 (the memo's why) |
| R5 | 2027 customer interruptions avoided as the schemes stand: 24,679, 80 per cent range 17,912 to 31,580 | forecasting | order para 5 | 23,712 to 25,405 (the rivals' span, 2 per cent beyond) | method shortcut: the restored loop priced alone with the plan's dates and the archive's rate (28,729) | R4 | Component 2 (and the recommendation) |

Carry-forward: R1, R2, R3 and R4 stand on inputs of their own (the device record; the dashboard and the 2026 records; the load tests and temperatures; the hourly amps, register and capital works); R5 carries R4's replay and R3's batteries, so a run that misses the netting loses R2 and R5 and keeps R1, R3 and R4's other parts.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Receiving reclosers on CTL-4C controls are never switched to their transfer group, and their old pickups trip on the combined load after a transfer | constructed by the simulated settings (set at commissioning, never revisited), loads and protection | no: 16 unswitched directions trip at different rates, most summer peaks, two year-round, and several never in the record | investigation: linking outage-record trips with no cause found to transfers through the device record | modeling: netted by the order, then replayed on the summer loads | keep |
| The archive's event queue overflows in storms and the front end slows with it | constructed by the simulated alarm load | no: overflows in every year, most lockouts in them restored late or not at all | reconciliation of the device record against the archive | reconstruction from the device record | keep |
| Control batteries age at their own rates and fail to crank in the cold, unseen by line-powered functional tests | constructed by the simulated batteries, tests and replacements | no: across the fleet, renewed after failures and alarms | modeling: resistance against temperature and age per battery | modeling: carried to -27 C and to February | keep |
| Planned works finish late | constructed by the simulated capital programme | no: every category of project slips | the capital works record | modeling: the completion distribution carried to the summer | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 customers restored within five minutes, each year 2022 to 2026 | Missed | Right | Right |
| R2 2026's customer interruptions avoided, walked from the dashboard | Missed | Missed | Right |
| R3 the controls to re-battery before the winter | Missed | Missed | Right |
| R4 the receiving feeders' customers June to September 2027 transfers would interrupt | Missed | Missed | Right |
| R5 2027 customer interruptions avoided as the schemes stand | Missed | Missed | Right |
| Roughly | 0 of 5 | 1 of 5 | 5 of 5 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "a transfer onto a receiving feeder whose reclosers the ADMS does not switch can trip them later, with no fault found"; rescues 1 of 5 results (R2; executed end to end, the careful forecast moves to 26,482, still outside R5's band)
Pair estimate: 34.5

The quick pass reads the dashboard. The careful pass is calibrated to the run on architecture 3: it reconciles every log (so it earns R1), and stops where the six places say runs stop: it prices each restoration at its own loop, judges a battery where it was tested, and takes the plan's dates and the past summers as the coming one.

## Data provenance

Source: generated by task13/generator from a simulated utility (network, loads, weather, faults, protection, the ADMS scheme, radio links, control batteries, maintenance, capital works); no LLM-written data.
Behaves like the real thing: loads follow households' and businesses' daily shapes and a lagged cooling response; faults follow thunderstorm cells, wind, ice and deep cold; reclosers lock out after reclosing; the scheme reads fault indicators, isolates, checks the receiving breaker and closes the tie; commands fail on weak radio paths and in storms; batteries' resistance rises with age and cold as VRLA cells do; projects slip as distribution capital work does.
Genuine patterns: (1) summer afternoon storm peaks in faults and the evening cooling peak in load (2) feeders' own fault exposure and section growth, new subdivisions with evening charging (3) battery fade by unit and the winter's arctic outbreaks (4) chronic weak radio paths and a base site's months-long outage.
Problems by process: the archive's overflow in storms; the standby server's echoes; the March 2025 upgrade's message text and tags; the October 2024 relocations; manual keying and two feeder spellings in the outage record; historian gaps when a radio path is down; airport gaps.
Breadth: 16 files; 22 loops, 44 feeders, 110 automated devices, 88 control batteries, five years of operations; deciding which loops, directions and controls matter is the work.

## Template check

Chain signature: assembly-reconciliation, decomposition-attribution, missingness-measurement, causal-reasoning, forecasting
Question form: how many (how many sustained customer interruptions the loops avoided, then what to change)
Nearest build: task4 v12 (a per-unit diagnosis at triage weight, a flagged set of spares lines) shares the decision form only; its exposures, queue and conversions are not here, and this chain's netting, cold crank and storm-lost record are not there. Abstraction: no sentence fits both.

## Frontier check

Precedents: R2 L16 (priced the unit alone where the system nets it against the units it affects), L06 (did one correction and declined the second); R3 N12 (a rate learned in one condition carried to another), N13 (the latest observed state taken as the state at the decision date); R4 N02 (history assumed informative of the forward window), N03 (scheduled works assumed to happen as planned); R5 L16, N03. R1 is Right: the runs reconcile every log by reflex.
Shallow path checks: R2's shallow path reproduces the dashboard after the five-minute rule and passes a reconciliation of the archive with the outage record; only the device record's receiving trips between a tie close and its opening, a second record at the device grain, refute it. R3's shallow path passes every functional test and last winter's cold tests; only each battery's resistance fitted on temperature and age and carried to February refutes it, and a fleet or per-type fit that passes its own residual check names 0 to 8 controls until its misses on last winter's cold tests are scored. R4's shallow path matches the 2025-26 summers' observed trips; only the replay at the hours faults strike with the reinforcements at their record-based dates refutes it. R5's shallow path back-tests on the record's success rate; only the netting refutes it.
Assumption made false: a run lists "the archive's sequences represent the operations", "a passed functional test means a sound battery" and "the approved works finish on their planned dates" and moves on. The archive loses its storm overflows, the line-powered test cannot see a cold crank, and comparable projects finished a median 3.9 months late; the device record, the load tests with the airport temperatures and the capital works record test each.
Forcing: R2's golden family (lost sequences counted from the configuration or the outage steps, receiving trips from the outage record or the device record) all give 21,328, against the dashboard's 27,370 across the line; section customers moved 10 per cent either way hold the call. R4's family spans 328 to 441 against the shortcuts' 237 and 582.
Noun swap: the nearest on file is task4 v12 (skeleton severity none); swapped in, its decision form (a per-unit diagnosis) carries, its lessons (exposure decoupled, staggered conversion, a shared queue) do not, nor do this build's netting, cold crank or storm-lost record; the guard's WARNs (downstream_offset taught once by the client's turbine wake; house lessons validation_cannot_see_condition and linkage_missing_not_at_random) are answered in the Draw.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | avoided | gross restored, or net of what the switching caused | net | order para 2 (would have had less had) |
| SF2 | five minutes | from the lockout, or from the first loss of supply | first loss | order para 3 |
| SF3 | 2026 | calendar year, or to the extract | January to October | the prompt (to October 2026) |
| SF4 | without automatic restoration | no restoration, or the usual switching | usual switching | order para 4 |
| SF5 | the batteries that would fail | at a test's temperature, or at the design minimum by end of February | design minimum, 28 February 2027 | the prompt and the design basis |
| SF6 | as they stand | including or excluding approved works | approved works at their likely dates, no unplanned change | order para 5; same call for R4's set |
| SF7 | average year | 2022-2025 complete years, or the rate since 1 January 2022 | the rate since 1 January 2022 | order para 5 |
| SF8 | major event days | excluded or included | included | order para 2 |
| SF9 | the restored customers a later trip put out again | counted as avoided (only the receiving customers netted, 23,735), or not | not | order para 2 (they had a sustained interruption either way) |
| SF10 | summer 2027 (R4's window) | June to August (364), June to September (388), May to September (432), 21 June to 22 September (about 300), July to August (241) | June to September | the design basis's seasons (summer 1 June to 30 September); the first three land inside 318 to 455 in any case |

## Closure table

| Axis | Closure |
|---|---|
| 1 | population: lockouts on in-service loops, every one the device record holds (order para 2) |
| 2 | unit: customers, sustained interruptions (order paras 2 and 3) |
| 3 | attribution window: Central calendar year by the lockout's time; nothing within an hour of a year's edge decides |
| 4 | as-of: the extract of 31 October 2026; batteries at 28 February 2027 (prompt) |
| 5 | version: the ADMS messages of both releases read alike; same call |
| 6 | denominator: none graded |
| 7 | weighting: the forecast weights by the record's lockout rates (order para 5) |
| 8 | window length: since 1 January 2022 (order para 5) |
| 9 | boundary: five minutes strict at 300 s; no restoration within 10 s of the line |
| 10 | rounding: whole customers, summed once |
| 11 | tie-break: none |
| 12 | maturity: 2026 to October, stated |
| 13 | order of operations: the walk's items are additive |
| 14 | row order: C1, every table keyed by device and time |
| 15 | duplicates: the standby server's echoes within a second, C1 |
| 16 | identity: the register's tag crosswalk and the device asset numbers |
| 17 | netting: order para 2 nets |
| 18 | units: amps at 13.8 kV; MW to amps at 0.96 power factor |
| 19 | codes: no cause found read with the device record, never alone |
| 20 | integers: customers whole |
| 21 | clause scope: order paras apply per calendar year |
| 22 | forward window: the capital works and large load workbooks |
| 23 | model structure (R3): each battery's own ageing with the fleet's cold coefficient, which the load tests select (control levels F 218.3, control ageing F 101.2, cold slopes F 1.2, p 0.11); the mixed model names the same 16; each core control fails in at least 0.9998 of its own fit's draws, RCL-20188 0.93, RCL-21643 0.83, RCL-21281 0.40, and no control outside them more than 0.035 |
| 24 | the oldest battery (RCL-21299, installed 22 February 2021, 6.02 years at the end of February): one asset key in the device events either side of the March 2025 upgrade (166 and 83 tests, no gap over 14 days), no replacement in the book, ageing 0.110 a year (two of 85 batteries slower); it holds 21.73 V, 0.53 V clear, so any fleet slope ranks it first and its own tests clear it |
| 25 | comparable projects (R4's slip): reconductoring and control replacements, a median 3.9 months late, or reconductoring alone, 4.5; R4 lands 388 or 409, both inside, and no reinforcement reaches a 0.25 chance of being in service by 1 June either way (0.23 and 0.12 at most) |
| 26 | distractors: the AMI notifications are daily counts per feeder for 2025 and 2026 only, so they cannot time a restoration to five minutes or reach 2022 to 2024 and are no second route to R1 or R2; the vegetation cycle status dates trimming, not operations |

## Literal reader

Order para 2 executed word for word gives 21,328 for 2026 (every operation's customers restored within five minutes, less the restored customers re-interrupted and the receiving customers interrupted by the switching); para 3 gives the five-minute line from the first trip; para 5 gives 24,679. The design basis's -27 C, 5 A, 30 A and 21.2 V give the 16. Every literal reading of the prompt's asks lands on the golden.

## Prompt contract

The rewrite keeps: the question (what to change before this winter and next summer, and 2027 as the loops stand), 2026 on the commission's definition as one figure, the years 2022 to October 2026, the controls whose batteries fail at the design minimum by the end of February 2027, the 2027 figure as the loops stand with an 80 per cent range, a spreadsheet and a short PDF memo. It never adds a rounding, a method, a warning, a file name, a role or a count the data hold, and never mentions the receiving feeders, the archive's losses, the reinforcements, the vendor dashboard or its figure.

## Leak rulings

- Sweep 3 (answer figures in data): the flagged numbers are recloser asset numbers (RCL-20188, RCL-21281, RCL-21643) that every record carrying those devices names; identifiers, not figures; harmless.
- Sweep 4 (design-note vocabulary): the design basis carries record, result, battery, feeders, control and, since judge p2, season; the order record, faults, control and outage; neither names a step (the order defines what is counted, the design basis the equipment's ratings and its seasons); harmless.
- Sweep 8 (column names): "Device" is the SCADA sequence-of-events export's and the register's own column; harmless.
- Sweep 9 (dates after the as-of): the capital works' planned 2027 in-service dates and the large loads' requested 2027 dates are forward plans, dated in the future by their nature; harmless.
- Sweep 11 (prompt gate, no roll call): the one attributed figure is the commission's (the 2026 figure it wants), the regulator whose definition the filing owes; no opinion is stated; harmless.
- Third reader's realism tells: the order printed paragraphs 7 and 8 after 9 to 12 (renumbered into sequence, 7 to 10 then 11 and 12; nothing cites them by number), both PDFs on A4 (US Letter now, the golden memo too), "programme" in the capital works register ("program"), documents created on round times (every stamp carries its seconds); Celsius before Fahrenheit in the design basis kept (equipment ratings are stated in Celsius, the airport's record in Fahrenheit, and the line gives both). checks.py asserts the sequence, the Letter page and US spelling across the pack.
- The design basis's Seasons line (added for judge p2's Gate E finding): it defines summer and winter by date and names no transfer, recloser, load or setting (asserted in checks.py); a design basis that states its ambient range states its seasons, and the prompt already names next summer; harmless, and read by the stage 4 reader again.

## Pre-ship check

- precut.py exit 0 (WARN nearest chains: task1 and task6 share the chain or the shape and the weight, none this chain's netting, cold crank or storm-lost record); effort.py exit 0 (quick 7.0, careful 34.5, thorough 100.0; the largest hint rescues 1 of 5; four shortcuts on four wrong answers); voice-check PASS; figures_check 70 of 70; audit_containers exit 0; guard heart WARN (answered in the Draw), surface clean; checks.py 79 of 79; verify.py 10 of 10 from target.zip on its own code path; two builds byte-identical (target 549db717, golden a20cf7a5; target.zip 2b4cbfaa, golden.zip ea3bc2c9); gates.py 0 FAIL, 3 WARN.
- Stage 4: judge p1 SEND_BACK (Gate G, closed by the re-frame); p2 DETERMINISTIC FIX_NOW (Gate C on R3's model structure, Gate E on the summer window; both closed in the generator); p3 DETERMINISTIC, APPROVE. Three leak readers: no method leak, nothing ranks or exists for the analyst, no one thing; the realism tells each found were fixed in the generator. Standing note from p2 and p3, informational: no judge pass recomputed R2's netting terms, R4 or R5 to the exact figure (the mechanisms were confirmed present and joinable each time); verify.py recomputes R2's two terms and the net from target.zip on its own code path, and R4 and R5 are model estimates whose bands come from the rivals run on the cut pack.

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
