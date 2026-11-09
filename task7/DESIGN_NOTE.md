# task7: which retrofit measures Haldenau's 2026 grant round funds, and what the round will pay (architecture 7)

Architecture 6 (the lottery's passed-over arm reached district by district by the service team's burner visits, which
skipped the works buildings) was returned at the platform's preliminary review on 2026-11-09 for turning on one thing;
its note, generator and goldens are in git at commit aa2fe65 and the review is in `runs/review_2026-11-09.md`. This
architecture keeps the world, the lottery and the per-measure projection to the offer's close, which the reviewer named
as what works, and rebuilds every result as a chain. Architectures 1 to 5 survive in the Tried and rejected record.

## Draw

Subdomain: Energy Systems & Utilities, energy efficiency and demand response evaluation (`efficiency-savings-verification`)
Analysis type: Experiment & Causal Analysis (assigned on the platform task; what each measure's works did to a
  building's normal-weather gas use, against the comparison the 2019 lottery supports, carried to the 2026 round)
Answer shape: scenarios with the flip point (each measure's grant per lifetime tonne on this year's applications against
  the €120 limit, with its range and the saving rate at which its call flips), with the round's settled grant beside it
Weight: modeling (each measure's saving by works age and by how a building is occupied, carried over the measure's life
  and to this year's applicants); the last two live builds sit on hard-to-measure (task6) and the retired single step,
  and the client's six weightings put modeling apart from both
Data-native sentence: the pilot's places were drawn by lot, so the passed-over owners give each measure's saving season
  by season, but the lottery's buildings are not this year's applicants (the pilot's controls answers came heavily from
  care homes and hotels heated round the clock, this year's mostly from offices, shops and workshops) and seven seasons
  are not a service life (heating optimisation's saving falls back as heating curves are turned up again, insulation's
  holds), while the round's own applications arrive by measure on the pilot's timing, the late insulation jobs larger and
  likelier to be withdrawn
People: Magda Peukert (chair, Committee for Climate and Environment) and Torben Römer (head of Energy Services,
  Stadtwerke Haldenau), from `guard.py names --geo Germany --seed 11`; neither is named in the prompt
Card: `.claude/skills/fingerprint/cards/task7.json`, v7, registered 2026-11-09 at WARN; v6 moved into lineage with its
  fate. WARNs answered: `overuse.strategy` composition_mix (3 of 12; the honest family of the transport result, one of
  eight); `overuse.gate_g` forecasting (the call needs a forward round and horizon the past does not pin);
  `repeat.decision` designation_set and `repeat.question_form` which against task6 (the decision picks measures, so
  "which" is its form); `repeat.deliverables` docx+xlsx against task12 (a committee note and the workbook the office
  issues grants from). The forcing event was redrawn from budget_or_appropriation (task6) and vote_or_meeting (task12),
  both in the ban window and as honest, to launch_or_rollout: the round's offer is live to 30 June and its grant
  letters go out once the committee sets it. `test.same_driver_older` against mark124, mark132 and mark175 differentiated
  on the card. The shell is new: which, see, a note and a workbook (v6 was which, put, a deck and a workbook).

## Deep reasoning

Task type: efficiency-savings-verification (energy efficiency and demand response evaluation), which serves Experiment & Causal Analysis
Domain test: every result is a measurement and verification quantity on weather-normalised metered gas: each measure's saving against the lottery's passed-over owners season by season, its persistence over the measure's service life, its dependence on how a building is occupied and how much of its gas heats water, carried into grant per lifetime tonne of CO2 and into what a grant round will pay
Swap: "fund insulation and controls, not heating optimisation, because the optimisation's saving fades as heating curves are turned back up and controls save nothing in buildings heated round the clock, which this year's applicants are not" read with a hospital's nouns keeps a skeleton and loses what decides: degree-day normalisation, a hot-water share that caps what insulation can save, a heating curve that creeps back, a setback that saves nothing at 24/7 occupancy, and lifetime tonnes of gas CO2
Where the weight sits: modeling, in R2 to R4: each measure's seven seasons carried over a service life two to four times longer than the record, each use's saving estimated from its own arms, and both carried to this year's applications building by building
Layer 1: cumulative index reads at 30 April with late and early periodic reads (the billing system's read calendar), meter exchanges with removal and fitting reads, five-digit counters that roll over, estimates replaced by corrections, customer typos corrected, rows imported twice, meters in tens of cubic metres, z-numbers per meter and calorific values per network area and season (the L-gas to H-gas change of 2017), second meter points, connections and disconnections, the service team's visit reads, extensions and empty floors in the register and on the notices, revised applications sent twice; each is the producing system's own and none decides a result (R2 assertions in checks.py)
Not one thing: the strongest single piece is the heating optimisation fade (R2); a run that nails it still has to estimate each use's saving (R3), price this year's applications at them (R4), carry the ranges and flip rates (R6), project the round with its timing, sizes and withdrawals (R7), take the 2025/26 saving on the right base (R8) and price every funded application (R9), and it still fails heating controls
One-fact test: "controls save almost nothing where the heating runs round the clock, and this year's controls applicants are mostly offices, shops and workshops" rescues R3 and R4 (2 of 9); the fade hint rescues only the call, the timing hint only R7
Not semantics: every field read correctly (the read reasons, the draw, the measure, the notices' use and floor area, the reference consumption, a revised application replacing the earlier one) and every Layer 1 item handled, the careful pass still files R4, R8 and R9 wrong and the call short of heating controls
Not rule application: no filed procedure performs a result; the plan files what a saving is, what lifetime tonnes and a round's rate are and the limit; how the pilot estimates a saving, how it carries over a life or to a building, and how the round is projected are left to the analysis
Estimand: plan 4.2 (a saving as a share of the gas the buildings that had the works would have used, normal weather), 4.3, 4.4 (lifetime tonnes over the measure's life on the application's reference consumption, the round's saving rate, grant per tonne, the limit), 4.5 (reference consumption), 4.6 (the season saving); the 2026 terms (applications to 30 June, a revised application replacing the earlier one, payment on completion, nothing to a withdrawn owner); the prompt (the applications received so far, a 90 per cent range, the flip rate, each measure's applications at close with the grant they ask for and what would be paid on them, the funded round's totals)
No decoy: no memo, draft, stakeholder figure or copied block; no shipped file states a saving, a rate, a grant per tonne or a recommendation; the committee request asks and states nothing
No replay: no result re-derives a published figure and no stated number is wrong
Pinned: every rival in the fork table run on the cut pack by checks.py lands inside its result's band (SF5 to SF10) or is ruled out by a filed sentence (SF1 to SF3) or named data (SF6, the levelling seasons); each hurried route lands outside by an asserted margin
Run forecast: R4 unfinished chain (the pilot's pooled rate on this year's mix), R8 method shortcut (the rate on the 2018/19 use), R9 unfinished chain, R7 method shortcut (late applications priced like early ones, one withdrawal rate), R6 self-confirming check (the range taken on the pooled rate), R3 narrow look (one rate per measure); runs that carry heating optimisation flat lose R2 and the call another way
Strategy label: heterogeneity that pooling hides, weighted to the population the decision serves, beside a forecast over a service life and a projection of a round from its own pilot's timing (WORKS IN FORM, sulfur-strategies.md)
Depth level: 5: five independent judgments each move a graded figure (the fade carried over the life, each use's saving, the transport to this year's applications, the round's timing with its sizes and withdrawals, the 2025/26 base), and the shortcuts land on three different wrong funded sets (all three by before and after or by each use carried flat; insulation and heating optimisation by the pilot's average carried flat; insulation alone by the pilot's mix faded), the golden holding across every defensible variant
Lesson: a lottery's effect is exact for the pilot's own buildings over the seasons it ran and nothing else; carrying it to a service life and to a new round's applicants takes its persistence and its heterogeneity, each estimated and weighted to the round, and the round's cost takes its own pilot's arrival, size and withdrawal record measure by measure; no build on file teaches these together (task2 weights a rate to a new mix in one step; the v6 slot spent the comparison group)

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each measure's saving in the pilot's works buildings in each season 2019/20 to 2025/26, against the owners the draw passed over | causal reasoning | the draw by lot within each measure (rules 3); plan 4.2 and 4.3 | 0.8 points a cell (two-season baseline, comparison by use) | method shortcut: the works buildings' own before and after, 25.7, 14.1 and 15.6 per cent on average | - | Ask 2 |
| R2 | each measure's saving over its service life in the pilot's buildings: 16.5, 2.2, 4.3 per cent | forecasting | plan 4.4 lives; the seasons levelling off (data) | 0.4, 0.2 and 0.2 points (the last season or the last three carried, a two-season baseline) | method shortcut: the seven seasons' average carried flat (heating optimisation 3.3) | R1 | Component 1 |
| R3 | each measure's saving by building use: controls 10.4 in offices, 0.3 and 0.1 in hotels and care homes | modeling | the data, each use's own arms | 1 point a cell | narrow look: one rate per measure | R1 | Component 2 |
| R4 | each measure's saving rate on the applications received, over its life: 15.9, 2.3 and 7.0 per cent | causal reasoning | plan 4.4 (in the building applied for, the round's saving rate) | 0.45, 0.2 and 0.45 points (two occupancy classes, the last seasons carried) | unfinished chain: the pilot's pooled rate on this year's mix (controls 4.3) | R2, R3 | Ask 3 |
| R5 | grant per tonne and the funded set: insulation and controls at 88 and 99 euro, heating optimisation 158 | synthesis | plan 4.4 and the limit | 7 per cent; the set exact | unfinished chain: insulation alone at the pooled rates | R4 | Recommendation |
| R6 | each grant per tonne's 90 per cent range and the saving rate at which each call flips: 11.7, 3.0, 5.8 per cent | uncertainty | the applications; the pilot's buildings drawn again within use and arm | flips exact to 0.05; range ends 8 euro | self-confirming check: a range on the pooled rate | R4 | Ask 4 |
| R7 | each measure's applications once the offer closes, the grant they ask for and what would be paid on them once the works are done; the funded round asks 7.7 million and pays 7.3 million | forecasting | the 2026 terms; the 2019 answers' dates, quotes and withdrawals | 3 per cent (one withdrawal rate) | method shortcut: late jobs priced like early ones, one withdrawal rate (6.1 million paid; one share for every measure 4.9 million) | independent: the 2019 responses and the 2026 applications | Component 3 |
| R8 | the CO2 the pilot's works saved in 2025/26, about 3,300 tonnes | synthesis | plan 4.6 | 3 per cent (each use's own 2025/26 saving) | method shortcut: the 2025/26 rate on the 2018/19 use (3,600) | R1 | Ask 6 |
| R9 | every funded application's lifetime tonnes (655 rows) | synthesis | plan 4.4 and 4.5 | 5 per cent a row | unfinished chain: the pooled rate on every row, controls rows missing | R4, R5 | Ask 5 |

Carry-forward: R7 is graded on inputs of its own (the 2019 responses and the 2026 applications) and stands whatever the rates; R8 needs only R1's last season; R2 and R3 each fall only with R1, which the careful pass earns; R4 needs both R2 and R3 (an AND), so a run that carries the fade but pools the uses, or the reverse, loses R4 to the step it skipped, and R5, R6 and R9 follow R4 alone.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| heating optimisation's saving falling back as heating curves are turned up, each building at its own pace | constructed (simulated building by building) | no: every heating optimisation works building, and a milder fall in every controls building, where it moves the life figure and decides nothing | the by-season comparison, one plot of the seasons | modelling: the level the saving settles at, fitted on seven seasons and carried to year fifteen | keep: the effect's own persistence, one of several results |
| savings that differ by use (the hot-water share for insulation, round-the-clock heating for controls) and an applicant mix unlike the pilot's | constructed (each building's own cut drawn around its use's) | no: every measure and use; insulation's differences move its figures and decide nothing, controls' decide its call | a targeted query, savings by use from each use's own arms | modelling: each use's saving estimated, faded with its measure and carried to each application's reference consumption | keep |
| the service team's burner checks | constructed | no: both arms alike, every measure (69 and 70 per cent of works and passed-over buildings) | a read reason in the meter file | none for the comparison, which the draw balances; they move the before and after and the 2025/26 base only | keep, texture |
| late insulation answers larger and more often withdrawn | constructed | no: every measure's answers carry a size and a withdrawal record; only insulation's move the round's figure much | a targeted query on the 2019 responses | modelling: count, size and withdrawal projected measure by measure | keep |
| extensions and empty floors | constructed | no: across the stock, both arms | the floor area on the notices | none: the draw balances them; a reading that sets changed buildings aside stays in every band | keep, texture |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each measure's saving by season | Missed | Right | Right |
| R2 each measure's saving over its life | Missed | Right | Right |
| R3 the savings by building type | Missed | Partly | Right |
| R4 each measure's rate on this year's applications | Missed | Missed | Right |
| R5 the funded set at the limit | Partly | Partly | Right |
| R6 each range and flip rate | Missed | Partly | Right |
| R7 the round at close and what it pays | Missed | Partly | Right |
| R8 the pilot's 2025/26 CO2 | Missed | Missed | Right |
| R9 every funded application's lifetime tonnes | Missed | Missed | Right |
| Roughly | 0.5 of 9 | 4 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (each pass computed end to end by checks.effort on the cut pack; three cells hand-graded with reasons)
Largest single hint: "controls save almost nothing where the heating runs round the clock, and this year's controls applicants are mostly offices, shops and workshops"; rescues 2 of 9 results
Pair estimate: 46.5

## Data provenance

Source: generated by task7/generator (world.py simulates the utility's commercial gas customers, the weather station, the benchmarking notices, the 2019 lottery, the service team's visits and the 2026 offer; pack.py writes each system's export; docs.py the council's and the utility's documents)
Behaves like the real thing: buildings carry their own level, a slow drift and season noise, weather through degree days on the type's hot-water share, the pandemic winters and the 2022 price shock by use, extensions and empty floors, burner checks of uneven effect, and quotes and answer dates driven by job size; the billing system writes reads on its own calendar with exchanges, rollovers, estimates and corrections
Genuine patterns: (1) degree-day weather response with use-specific hot-water shares (2) a slow building drift and season noise (3) the pandemic winters and the price shock, different by use (4) each measure's saving varying building by building around its use's, and fading for the operational measures at each building's own pace (5) answer timing and quote size scaling with the job (6) uneven burner-check effects
Problems by process: periodic reads taken days off 30 April, meter exchanges, counter rollovers, estimates later corrected, customer typos, re-imported rows, meters counting tens of cubic metres, the 2017 gas-quality change in one network area, second meter points, connections and disconnections mid-series, revised applications sent twice
Breadth: 24,000 buildings and 25,900 meter points over thirteen seasons, 389,000 reads, 37,000 notices, 3,055 pilot answers across six uses and three measures, 902 applications; choosing which comparison, which seasons, which uses and which answers carry each result is the work

## Template check

Chain signature: causal reasoning, forecasting, modeling, causal reasoning, synthesis, uncertainty, forecasting, synthesis, synthesis
Question form: which (a pick of measures), with the round's grant asked beside it
Nearest build: task2 (a recognizer's error rate weighted to each 2027 clinician mix): one transport step deciding a tier, against a chain here where the transport is one of five judgments beside a lifetime forecast and a round projection; task7 v6 (the same world, a comparison treated after the draw), spent and not reused: the visits now reach both arms and decide nothing

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "saving" in a season | the share of the gas the works buildings would have used (aggregate); the average building's share | aggregate | plan 4.2 ("the gas its works save, as a share of the gas the buildings that had them would have used") |
| SF2 | the average of building shares | equal-weight against gas-weight | gas-weight | plan 4.2; controls 1.3 points apart, asserted |
| SF3 | "the buildings that had them" | works buildings; every drawn owner, withdrawals included | works buildings | plan 4.2; same funded set, asserted |
| SF4 | a building's use | its 2019 notice; the 2026 register | the 2019 notice | same call, asserted |
| SF5 | the baseline and the comparison | the 2018/19 season, every passed-over owner of the measure; two seasons; the comparison taken use by use | 2018/19, the measure's passed-over owners | inside R1's band, asserted |
| SF6 | the saving after the seventh season | the fitted level; the last season or the last three carried; flat; an exponential fall to nothing; a line | the fitted level | the last seasons in the band; flat, the first season, the exponential and the line ruled out by the seasons' levelling (asserted) |
| SF7 | the saving "in the building applied for" | each use's saving faded; two occupancy classes; the last seasons carried | each use's | inside R4 and R5's bands, same set, asserted |
| SF8 | the 90 per cent range | resampling buildings within use and arm, every step repeated, two seeds | the first seed | within 6 and 8 euro, asserted |
| SF9 | withdrawals | early and late rates by measure; one rate by measure | early and late | inside R7's band, asserted |
| SF10 | the 2025/26 saving | the measure's 2025/26 saving on each works building's use; each use's own | the measure's | inside R8's band, asserted |
| SF11 | reads off 30 April | shared by degree-day weight; counted whole to the nearer season | shared (method 1) | same call, figures within 5 per cent, asserted |
| SF12 | estimates without a correction | kept; dropped | kept (method 1) | same call, asserted |
| SF13 | normal weather | the method's normalisation; raw use | normalised (plan 4.3) | same call, asserted |
| SF14 | a revised application | the later replaces the earlier; both kept | the later (2026 terms 2) | same call, asserted |
| SF15 | "what would be paid once the works are done" | net of withdrawals; net of withdrawals and works not completed (terms 4) | both | converge: every drawn 2019 owner either withdrew or completed, asserted |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the pilot's works buildings and passed-over owners by measure; the applications received by 12 June; the round's applications to 30 June | filed: rules 3, terms 1 to 3, the prompt |
| 2 | Unit of account | the building (an application is a building and a measure) | filed: plan 4.4, terms 2 |
| 3 | Attribution window | the season, 1 May to 30 April | filed: plan 4.3 |
| 4 | As-of dating | the applications received by 12 June; the 2019 answers' own dates | the request; C1 |
| 5 | Version basis | a revised application replaces the earlier one | filed: terms 2 (SF14) |
| 6 | Denominator | the gas the works buildings would have used | filed: plan 4.2 (SF1) |
| 7 | Weighting | the gas: buildings by their use, applications by reference consumption | filed: plan 4.2 and 4.4 (SF2) |
| 8 | Window length | seven seasons observed, the service lives filed | filed: plan 4.4; SF6 |
| 9 | Boundary inclusivity | €120 or less funds | filed: plan 4.4; no grant per tonne within 10 per cent of the limit |
| 10 | Rounding path | none in the prompt (the author's call, 2026-11-09): every figure stated at its natural precision, percentages to two decimals, grant per tonne to the cent, money to the euro, counts and totals whole, an application's tonnes to a tenth | C1: the bands are wider than any printing choice, asserted |
| 11 | Tie-break | none needed | C1 |
| 12 | Maturity and censoring | the 2026 round open to 30 June; seasons after the seventh unobserved | the prompt and R7; SF6 |
| 13 | Order of operations | normalise, compare, carry, weight | C1 |
| 14 | Row order | export order | C1 |
| 15 | Duplicate resolution | re-imported reads once; a revised application replaces the earlier | C1; SF14 |
| 16 | Identity normalisation | meter points to buildings through the meter list | the meter list's crosswalk |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | cubic metres to kWh by z-number and calorific value | method 2 |
| 19 | Code and status semantics | read reasons; drawn, withdrawn and completed | the files' own columns |
| 20 | Integerisation | applications at close whole, as an estimate | C1 |
| 21 | Clause scope | plan 4.4 for each measure in the round | filed |
| 22 | Forward window contents | the applications still to come, from the 2019 answers' timing, sizes and withdrawals | R7, the 2019 responses ship |

## Literal reader

Executed word for word, plan 4.2 and 4.3 with the pilot rules give each season's saving as a share of the gas the works buildings would have used against the owners the draw passed over (R1); plan 4.4 asks for each application's saving in the building applied for over the measure's life and the round's saving rate as a share of the tonnes its reference consumption carries (R2 to R5, R9); 4.6 gives the 2025/26 saving (R8); the 2026 terms give the round at close and what is paid (R7). No sentence names the comparison, the persistence, the use split or the projection, and the readings a literal reader can take are the fork table's, each asserted.

Leak rulings (leak.py, 2026-11-09, --asof 2026-06-24, REVIEW, no LEAK): the "golden figures" 4.1, 4.3, 4.4 and 4.6 in
the plan and the request are the plan's own section numbers, harmless; the call's words (insulation, heating controls)
in the plan, the 2019 rules and the 2026 terms are the measures' names, which every governing document must carry; the
design-note vocabulary hits (heating, insulation, record, building, carried) are the field's ordinary words, and no
sentence names a comparison, a fade, a split by use or a projection.

## Prompt contract

May not drop or change: the question (which measures, under €120 of grant per lifetime tonne of CO2); for each measure its saving in the pilot's works buildings in each season since the works, its saving rate on the applications received so far, their grant per tonne with a 90 per cent range and the saving rate at which the answer would flip, and how many applications it will have once the offer closes, the grant they ask for and what would be paid on them once the works are done, with the funded round's totals; every funded application received so far with its grant and lifetime tonnes; the pilot's 2025/26 CO2; a short note with the answer first and a workbook. The prompt carries no rounding sentence at the author's word; the answer blocks and the golden state every figure at its natural precision. Must never add: a method (a comparison, a fade, a split by use, a projection), a warning, an attached file's name, a role or a count the data hold.

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
