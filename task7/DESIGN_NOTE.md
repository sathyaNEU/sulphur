# task7: the EV Overnight rate's charging default for summer 2027, and the transformer replacements it leaves

## Draw

Subdomain: Energy efficiency & demand response evaluation (tariff-demand-response-evaluation)
Analysis type: Experiment & Causal
Answer shape: scenarios with the flip point (three charging defaults, each with the transformers it leaves over their limit, its fee
  and its total, and the fee at which the call would change)
Weight: a hard-to-measure quantity: each distribution transformer's highest 15-minute load of a summer like 2026 under charging
  designs the record holds only in part (own schedules for half the chargers, random start for the other half, coordination for
  none), on a meter that reads hourly; task22 sat in assembly and task20 in validation (task13's hard-to-measure is one of the last
  five, a WARN answered here: its quantity is an outage's unrecorded duration, this one a coincident peak)
Data-native sentence: the pilot randomised chargers, not transformers, so the randomised comparison measures what a design does to an
  average charger's quarter-hour, while the limit is each transformer's single worst quarter-hour of the summer, which depends on how
  often a handful of 7 to 11 kW blocks land together on the same nights, and the meters that see every home read only hourly
People: Eileen Casey (manager of distribution planning), Chad Wyatt (pilot manager), Rebekah Fleming (rates analyst), Joshua Baker
  (Quillpoint's account manager), Sandra Bernard (engineering, the planning standard)

## Deep reasoning

Task type: energy efficiency & demand response evaluation (tariff-demand-response-evaluation): a randomised managed-charging pilot on a time-of-use EV rate, evaluated for the rate's default on the distribution transformers it loads
Domain test: every result is a distribution-planning or demand-response quantity: the pilot's randomised change in a charger's load at the off-peak start, each distribution transformer's highest 15-minute load of a summer under a charging design (how often a few 7.2 to 11.5 kW blocks coincide on one transformer on top of its homes' evening and night load), the replacements DPS-7's 120 per cent limit calls for, and each option's cost for the year
Swap: "which charging default for a cooperative's EV rate, judged on its distribution transformers' summer peaks" with servers and jobs for transformers and chargers: the tariff's 23:00 off-peak start, the 15-minute kVA limit at a 0.95 planning power factor, the summer air-conditioning base, the transformer sizes and the work plan's change-outs stop making sense
Where the weight sits: R4 and R5, each of the 382 transformers' highest quarter-hour of July and August under two designs the record holds only in part: Stagger replayed night by night with 400 draws of every session's random start, Sequence (never piloted) replayed by its filed rule on each night's plug-ins, energy and unplug times; long because every transformer-night is rebuilt from records at two grains (hourly reads at the homes, minute-level sessions at the chargers), not clever
Layer 1: hourly reads exported per substation in local time, hour-ending, with estimated hours filled by interpolation and a re-sent block in each file; meters exchanged mid-summer (the exchange day split across two meter numbers); the session log in UTC with a re-sent batch and empty plug-ins; chargers swapped under new serials; the roster's re-imported rows with the account number unpadded; one split's service transfers not yet posted to the GIS; three change-outs the register has not caught up with; monitor gaps and the transformer's own losses in the monitors; each made by the system that keeps the file, none deciding a result
Not one thing: the call needs two independent judgments: Stagger's season coincidence replayed night by night (without it the pilot's average managed night files Stagger with 1 over) and Sequence replayed by its rule (without it Sequence is either the pilot's managed quarter, which files Stagger, or one charger at a time, which files Sequence with 1 replacements); the members' own schedules restored moves the own count (52 against 28 off the 2026 meters) and the 15-minute lift moves each count by a few; one sentence rescues one result
One-fact test: the strongest sentence ("a few chargers on one transformer still land together on some night of the summer under a random start, so replay every night") rescues R4 alone; the call still needs Sequence's own replay and the budget its forced overlaps (effort.json: 1 of 9)
Not semantics: every field read right (hour-ending reads, UTC sessions, swaps, exchanges, transfers, change-outs, the halves, the ready-by column) and the careful route still files Stagger with 0 replacements, because none of the judgments is a reading: one is a maximum over nights of a sum, one a schedule replayed under a rule, one a status quo rebuilt charger by charger
Not rule application: EV-4 files what is compared (an option's expected fee plus replacements in a summer like the last one, the chargers the quote covers, own schedules as their owners set them), DPS-7 the limit, the kVA convention and the installed costs, the proposal the two products' rules and fees; nothing files how a transformer's summer peak is estimated under a design from hourly reads and sessions, that the pilot's average night misprices it, or how the managed quarter's own settings are known
Estimand: Board Policy EV-4 sections 3 and 4.1 to 4.3; DPS-7 sections 2.1 to 2.3, 3 and 4; the proposal (fees per enrolled charger per year, the chargers enrolled on 1 November 2026, each product's rule); the pilot plan section 3 (R2's comparison and its per-charger, every-night footing); the prompt
No decoy: no memo, draft or stakeholder figure; the proposal describes its products' rules and prices and ranks nothing; the state's EV registrations and the net-metering list rank nothing and decide nothing
No replay: no result re-derives a published figure and no stated number is wrong
Pinned: the rivals run on the cut pack (the monitored transformers' option-by-option peak lift in place of the per-hour excess, no lift at all, every charger on its declared setting, two other random seeds) all call Sequence; own schedules span 49 to 59, Stagger 25.5 to 33.5, Sequence 10 to 12, the flip fee USD 145 to 204; the ready-by is the unplug time (EV-4 4.1)
Run forecast: a frontier run reads every file, cleans the reads and the sessions, measures the pilot's change at 23:00 from the randomised halves (-4.95 kW, R2 earned), and then carries the pilot's average managed night to each transformer (R4 lost: 0 over), takes Sequence as one charger at a time or as the pilot's managed quarter (R5 lost), reads own schedules off the 2026 meters (R3 lost: 28), and files Stagger (R6 to R8 lost); method shortcut at R4 and R5, dismissed own evidence at R3
Strategy label: OWN (no client strategy carries a randomised per-charger effect to shared transformers' season peaks; the nearest, Engineering and Physical Sciences 9, sizing a battery when the month's peak is not known in advance, works a peak functional on one meter)
Depth level: 5 on the client's scale: four independent judgments (Stagger's season coincidence, Sequence's replay, own schedules restored, the quarter-hour lift), the call needing the first two together, and the shortcuts landing on different wrong answers (Stagger with 0 or 1 replacements, Stagger again with Sequence taken as the pilot's quarter, Sequence with 1 replacements, own schedules at 28)
Lesson: an effect randomised on the units is not the effect on the shared resource they load: the decision's quantity is the summer's maximum of a sum of a few blocks on each transformer, which the average night hides, and a design the pilot never ran is replayed on the record's own windows; no task on file teaches it (non_additive_aggregation untaught, skeleton.py lessons)

## Stump screen

Run after the build (the card was registered before the screen existed), every candidate through the nine tests of
stumping/references/stump-screen.md (1 off the closed page, 2 not a reflex, 3 nothing filed, 4 clean data, 5 two records at
two grains, 6 an assumption waved through with its precedent, 7 a plausible shallower story, 8 across the data, 9 worth the
call):

| Candidate | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | Kept |
|---|---|---|---|---|---|---|---|---|---|---|
| A: Stagger's season coincidence on each transformer (the average managed night against the summer's worst quarter-hour) | yes | yes | yes | yes | yes (hourly reads, minute sessions) | yes (N01) | yes (the pilot's own profile reproduces its means) | yes | yes (flips the call to Stagger alone) | kept: the deciding trap |
| B: Sequence's forced overlaps (its rule replayed on each night's windows) | yes | yes | no: the proposal files the rule, its late-charger clause included | yes | yes | yes (N04) | yes (one charger at a time) | yes | yes (as the pilot's quarter it flips the call) | dropped as a trap, kept as a result: its trigger is filed, so a careful run that replays the rule earns it |
| C: own schedules restored for the managed quarter | near a closed card (supporting only) | yes | no: the pilot plan files the managed quarter | yes | yes (halves against sessions) | yes (L04) | yes (the 2026 meters reconcile) | yes | no: alone it leaves the call standing | dropped as a trap, kept as a supporting result |
| D: the quarter-hour lift over hourly reads | yes | yes | no: DPS-7 files the 15-minute support | yes | yes (monitors) | no | no | yes | no: every lift stays inside the bands | dropped: texture |

Read straight, the screen keeps one trap (A), which the call needs; B and C are graded work a hurried route skips (the
measured routes lose them) but a careful run can earn, because their triggers are written down. Depth rests on A plus the
work around it, not on three independent traps.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | chargers enrolled on 1 November 2026 (1,313) | assembly-reconciliation | the proposal's basis; the roster (swaps, closures, re-imported rows) | exact | narrow look at broad data: the roster's Active rows counted with the re-imported duplicates (the quick pass); the careful pass is right | independent: the roster | Ask 7 |
| R1b | transformers serving them (382, the CSV's rows) | assembly-reconciliation | DPS-7 4: the GIS as corrected by the work orders | exact | narrow look at broad data: the GIS alone, without the split's transfers; the careful pass is right | R1 | Ask 10 |
| R2 | the pilot's change at 23:00 to 23:15 (-4.95 kW per enrolled charger) | causal-reasoning | the pilot plan 3 (per enrolled charger, every night, managed quarter against own schedules) | plus or minus 0.1 | method shortcut: the hourly reads at 23:00 to 24:00 in place of the quarter (the quick pass); the careful pass is right | independent: the sessions and the halves | Component 4, Ask 6 |
| R3 | own schedules' transformers over their limit (52) | causal-reasoning | EV-4 4.2 (as each owner set it) | 49 to 59 | dismissed own evidence: the 2026 meters as the status quo (28) | R1b | Component 3, Ask 2 |
| R4 | Stagger's transformers over their limit, at their chance (27.5) | modeling | EV-4 4.1, 4.3; the proposal's rule | 25.5 to 33.5 | method shortcut: the pilot's average night times the chargers (0) | R1b | Component 1, Ask 2 |
| R5 | Sequence's transformers over their limit (11) | modeling | EV-4 4.1; the proposal's rule | 10 to 12 | method shortcut: one charger at a time (1) or the pilot's quarter (27.5) | R1b | Component 2, Ask 2 |
| R6 | each option's fee, replacements and total (Sequence USD 212,800, Stagger USD 365,200, own USD 794,600) | synthesis | EV-4 3; DPS-7 3; the proposal's fees | each total's rivals' span | method shortcut, carried from the hurried counts | R3, R4, R5 | Asks 3 to 5 |
| R7 | the default and the work plan's replacements (Sequence, 11, USD 160,300) | synthesis | EV-4 3 and 5 | the call exact; the count 10 to 12 | method shortcut: Stagger | R4, R5 | Recommendation, Ask 1 |
| R8 | the Sequence fee at which the call changes (USD 156 a charger) | uncertainty | EV-4 3 | USD 145 to 204 | method shortcut, carried from the hurried counts | R4, R5, R6 | Ask 8 |

Carry-forward: R1, R2 stand alone; R3, R4 and R5 each rest only on the assembly (R1b) and each other's judgments are independent, so a slip on one costs only its own count and the totals built on it; R6 to R8 fall with the counts they use.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| random starts that still coincide on some night | constructed, the process of random starts over 62 nights | no: every transformer with two or more chargers | modelling (a maximum over nights of a sum) | modelling | keep |
| Sequence's forced overlaps on heavy nights | constructed, energy against the hours to departure | no: every transformer on its heavy nights | modelling (the rule replayed on each night's windows) | modelling | keep |
| the managed quarter inside the 2026 meters | constructed, the pilot's design | no: a quarter of chargers on every substation | a targeted query (the halves against the sessions) | modelling (each charger's own setting) | keep (supporting; its omission alone leaves the call standing) |
| peaks inside the hour the hourly reads cannot see | constructed, appliances and air-conditioning cycling | no: every transformer, every hour | the monitors at another grain | modelling (a lift from the monitored transformers) | keep (texture: every reasonable lift stays inside the bands) |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 chargers enrolled | Missed | Right | Right |
| R1b transformers serving them | Right | Right | Right |
| R2 the pilot's change at 23:00 | Missed | Right | Right |
| R3 own schedules' transformers over | Missed | Missed | Right |
| R4 Stagger's transformers over | Missed | Missed | Right |
| R5 Sequence's transformers over | Missed | Missed | Right |
| R6 each option's cost | Missed | Missed | Right |
| R7 the default and its replacements | Missed | Missed | Right |
| R8 the flip fee | Missed | Missed | Right |
| Roughly | 1 of 9 | 3 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (quick 20.8, careful but hurried 40.5, thorough 100)
Largest single hint: "a few chargers on one transformer still land together on some night of the summer under a random start, so replay every night"; rescues 1 of 9 results (R4); each of the other two sentences rescues one (R5, R3)
Pair estimate: 40.5
Judge's note: the stage 4 judge put the careful pass at about 4 to 6 of 9 results where the measured routes give 3 of 9; the table is the generator's measurement of the coded routes, and the platform's runs are the measurement that counts

## Data provenance

Source: generated by task7/generator (world.py simulates the association's homes, EVs, chargers, pilot, network and systems; pack.py writes each file the way its system writes it); no public data
Behaves like the real thing: homes' load at the quarter-hour from a household baseline, central air that follows a Front Range summer's heat with each house's thermal lag and compressor cycling, dryers, cooking, hot tubs and rooftop solar; EVs that drive, come home between 16:00 and 21:00, plug in on most evenings, leave around 07:00 and charge at 7.2, 9.6 or 11.5 kW; an off-peak price from 23:00 that most own schedules start at; a randomised pilot that managed one charger in four; a meter data system that keeps hourly reads and fills gaps; a platform that logs sessions in UTC; a GIS and a register that lag the work orders
Genuine patterns: (1) the 23:00 step on own schedules against a spread under Stagger, (2) evening air-conditioning peaks that follow the heat with a lag and drop through the night, (3) weekday and weekend driving with Sunday-night top-ups and weekend trips, (4) adoption clustered by street (transformers with none to nine chargers), (5) peaks inside the hour that hourly reads average away
Problems by process: estimated hours (the meter data system's interpolation), a re-sent block in each meter export and a re-sent session batch (export retries), meters exchanged mid-summer (failed registers and a recall), chargers swapped under warranty (new serials linked in the roster), re-imported roster rows (a migration that dropped leading zeros), a split's transfers not yet in the GIS and three change-outs not yet in the register (posting lag), monitor gaps (communications)
License: none needed: generated for this task and released with it as CC BY 4.0 (metadata.json)
Used as is: nothing public is used
Breadth: 19 files in three formats; 382 transformers serving 1,313 enrolled chargers, about 3,500 meters' hourly reads, 257,000 sessions over three summers, 48 monitored transformers; which transformers, nights and chargers decide a count is the work

## Template check

Chain signature: assembly-reconciliation, causal-reasoning, causal-reasoning, modeling, modeling, synthesis, synthesis, uncertainty
Question form: what (the default, and what its replacements cost the work plan)
Nearest build: task22 (Delmont Power and Light's feeder energy balance): another utility network, but its answer is a ranked set of feeders from a loss bridge, its lessons the square of current, a switching log and a residual; this one picks one of three charging designs from a randomised pilot on each transformer's coincident summer peak; skeleton severity none against every card and client task
Guard warnings: repeat.decision (a pick among a few options, as task16's) is a cooperative's choice of three charging designs, not a record-linkage method; skeleton.house_lesson (queue_or_capacity_replay on mark117 and task4 v12) is a supporting move here (Sequence's rule replayed), the deciding lesson being non_additive_aggregation; precut's nearest chains (task21, scenarios with the flip point) has its weight in modeling quote feeds, this one in a hard-to-measure quantity
Abstraction sentence: none writable against a build on file: no card carries a randomised per-unit effect replayed onto shared capacities' season maxima with an unpiloted design replayed on the record's windows

## Frontier check

Precedents: R3 L04 and L01 (dismissed own evidence: the 2026 meters read as the status quo though the halves file shows a managed quarter); R4 L15 and N01 (method shortcut: the pilot's per-charger change carried as an average night, an enlarged fleet assumed to scale in proportion); R5 L15 and N04 (method shortcut: Sequence assumed one charger at a time, or the pilot's quarter, instead of replayed); R6 to R8 L15 (they rest on the hurried counts)
Shallow path checks: R4: the average managed night reproduces the managed quarter's mean load at every quarter-hour and the pilot's -4.95 kW change exactly; refuted by a check of another kind, the monitored transformers' 15-minute load (transformer_monitors_15min_2026-07_08.csv, another grain) on transformers with two or more managed chargers, which shows them landing together on some nights; R5: one charger at a time is what the product's name suggests and keeps every transformer under; refuted by the rule's own clause run on each night's sessions (energy and unplug times in the session log); R3: the 2026 meters reconcile to the monitors; refuted by the halves file and the sessions' control mode (a quarter of chargers under Stagger all summer)
Assumption made false: "a managed design's effect on a transformer is the pilot's average change per charger times its chargers" (diversity smooths it): false here because a transformer serves two to nine chargers and its limit is the summer's single worst quarter-hour, so the average hides the nights they coincide; tested on the monitored transformers and by replaying the sessions
Forcing: the line is the cheapest option; the golden family (the per-hour lift, the monitored-peak lift, no lift, declared settings, two seeds) all call Sequence, the nearest at USD 231,000 against Stagger's lowest USD 341,100; the shortcuts call Stagger (the average night, Sequence taken as the pilot's quarter) or Sequence with 1 replacements; the lift moved 20 per cent each way, replacement costs down 20 per cent and Sequence's fee up 20 per cent all keep Sequence; the flip fee is USD 156 against the quoted 40
Noun swap: nearest on file by skeleton.py check is depth:279e74f2 (a crew's days replayed through capacity): the replay move and the queue lesson carry across; the decision form, the deciding lesson, the mechanisms, the detection and the file roles do not; severity none
Closed strategies: the call turns on non_additive_aggregation (a transformer's summer maximum of a sum of a few chargers' blocks), on no card of the client's page (none of the five families touches a maximum over a shared resource's season; skeleton.py closed lists no neighbour); the supporting step R3 (own schedules restored because the 2026 meters hold a managed quarter) sits near "Outcomes are hidden by the intervention itself" and "Controls were partly treated" (no selection on risk and no interference here, but the metered record carries the treatment): its route alone (no_own in effort.json) moves the own count to 28 and the call stays Sequence; the 15-minute lift is texture (no_lift stays inside every band)

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | chargers counted | enrolled 1 November 2026; on the board's date; on 1 June 2026 | 1 November 2026 | the proposal ("quoted on the chargers enrolled on 1 November 2026"); EV-4 3 |
| SF2 | a summer like the last one | July and August 2026 as metered; June to September; weather-normalised | July and August 2026 | EV-4 4.1; DPS-7 2.1 |
| SF3 | over its limit | 15-minute kVA above 120 per cent; hourly; monitored kVA | 15-minute kW / 0.95 | DPS-7 2.1, 2.2 ("whether or not the transformer is monitored") |
| SF4 | nameplate | register; register corrected by change-outs | corrected | DPS-7 2.3, 4 |
| SF5 | transformers serving | GIS; GIS corrected by work orders | corrected | DPS-7 4 |
| SF6 | own schedules for the managed quarter | own-schedule history then declared; declared only | history then declared | EV-4 4.2 (rival in band: declared only, 51) |
| SF7 | a random option's count | expected (each at its chance); one draw; majority | expected | EV-4 4.3 (an option's cost is its expected cost) |
| SF8 | ready-by in the replay | unplug time; recorded ready-by | unplug time | EV-4 4.1 ("each session finishing by the time it was unplugged") |
| SF9 | Sequence's rule | the proposal's text | as filed | the proposal |
| SF10 | replacement cost | DPS-7's installed cost by unit; times the chance for Stagger | as filed | DPS-7 3; EV-4 3, 4.3 |
| SF11 | fee | per enrolled charger per year times the chargers covered | as filed | the proposal; EV-4 3 |
| SF12 | the pilot's change | per enrolled charger, every night of July and August, 23:00 to 23:15, managed less own | as filed | the pilot plan 3; the prompt |
| SF13 | chargers that left the rate | as metered; removed | as metered | EV-4 4.2 |
| SF14 | the lift to 15 minutes | per-hour excess; monitored peak; none | per-hour excess | same call (all rivals Sequence; bands span them) |
| SF15 | sessions plugged in on 30 June | their July quarters counted; left out | counted | EV-4 4.1 (July as metered holds them); same call |
| SF16 | 31 August's night after midnight | outside; inside | outside | DPS-7 2.1 (July and August) |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | chargers enrolled on 1 November 2026; transformers serving them | filed: the proposal; DPS-7 4 |
| 2 | Unit of account | transformers over their limit; USD for the year; kW per enrolled charger | filed: EV-4 3; the pilot plan 3 |
| 3 | Attribution window | July and August 2026 as metered | filed: EV-4 4.1; DPS-7 2.1 |
| 4 | As-of dating | the roster of 2 November, the quote of 1 November 2026 | the files' own dates |
| 5 | Version basis | a swapped charger's sessions under both serials | the roster's replaces_serial |
| 6 | Denominator | every enrolled charger, every night (R2) | filed: the pilot plan 3 |
| 7 | Weighting | Stagger's transformers at their chance | filed: EV-4 4.3 |
| 8 | Window length | the season's highest quarter-hour | filed: DPS-7 2.1 |
| 9 | Boundary inclusivity | over when above 120 per cent | filed: DPS-7 2.1 ("exceeds") |
| 10 | Rounding path | none in the prompt; figures at their natural precision | the answer blocks |
| 11 | Tie-break | none needed (the totals differ by USD 150,000 and more) | - |
| 12 | Maturity and censoring | 2027 not observed; judged on a summer like the last one | filed: EV-4 3, 4.1 |
| 13 | Order of operations | assemble, base, replay each option, lift, test, cost | the golden's steps; same call in every order |
| 14 | Row order | the CSV by substation then location | - |
| 15 | Duplicate resolution | re-sent meter rows, re-sent sessions, re-imported roster rows dropped | keys: meter and date; session id; service point, serial and date |
| 16 | Identity normalisation | old meters to service points; swapped serials to one charger | the exchange log; the roster |
| 17 | Netting against gross | net kWh at solar homes; enrolled charging removed from the base | EV-4 4.1 ("as metered") |
| 18 | Dimensional units | kWh in an hour to kW; kW to kVA at 0.95 | the export's header; DPS-7 2.2 |
| 19 | Code and status semantics | control modes; Active, Closed, Replaced | the files' own codes |
| 20 | Integerisation | counts whole except Stagger's chance-weighted count | filed: EV-4 4.3 |
| 21 | Clause scope | EV-4 section 4 for all three options | filed |
| 22 | Forward window contents | 2027 judged on 2026's sessions and loads | filed: EV-4 4.1 |

## Literal reader

EV-4 section 3 makes the default the cheapest option for the year; 4.1 to 4.3 make an option's cost its fee plus the replacements it leaves when every covered charger replays its July and August 2026 sessions as the option would, each finishing by its unplug time, the members' own schedules as each owner set them and every option at its expected cost (so Stagger's transformers at their chance); DPS-7 2.1 to 2.3 make a transformer over when its highest 15-minute load in July and August is above 120 per cent of the nameplate in service, at kW / 0.95, and section 3 prices the replacement; the proposal fixes the fees, the chargers covered and each product's rule. Executed word for word on the cut pack these give Sequence with 11 replacements; the literal reader's open choices (how to lift hourly reads to the quarter-hour, which record shows an owner's setting) are run as rivals and all give Sequence.

## Prompt contract

May not drop or change: the question (the EV Overnight rate's charging default from summer 2027, and what the replacements it leaves cost the 2027 work plan); a short memo with the call and a CSV with a row for each transformer serving the rate's chargers; for each option the transformers it leaves over their limit, the platform's fee, the replacements' cost and the total; the kW per charger the pilot's managed charging took off an enrolled home's load from 23:00 to 23:15; the chargers enrolled; the fee per charger at which the call would change. Must never add: the policy's comparison or its summer, the limit, a method (an average night, a replay, a chance, a lift, a monitor, a setting), a warning, an attached file's name, a role, a rounding instruction or a count the data hold.

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
