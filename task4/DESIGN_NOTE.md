# task4 design note

## Draw

Card `.claude/skills/fingerprint/cards/task4.json`, architecture 4, registered 2026-11-08 (a re-root: architecture 3,
the Polish parcel carrier's October scan alerts, was landed by both platform runs, which reached the golden's call and
every graded figure, so the platform returned not stumped before any rubric; the card's lineage records it spent with
architectures 1 and 2). One architecture per world: a new world (the west of Ireland), a new dataset (van run stop
sequences), a new organisation family (an online retailer's own fleet) and a new shell (which | i'd | png+xlsx against
whether | the | pptx+xlsx and how-many | in | png+xlsx).

Guard `check` on the registered card: WARN only. `repeat.gate_g` (forecasting after task1): task1 projects a member's
paid twelfth month through their tutor's stopping; here the forward quantity is a route network's 2027 avoidable
van-hours, a different construction under the same mechanism key, which is the honest one because the call rests on a
2027 figure the 2025 and 2026 runs pin down. Two axes redrawn at the draw: the forcing event (purchase_order_or_contract
BLOCKed against task1 and task3; budget_or_appropriation BLOCKed against mark456) is now the executive meeting that
approves the 2027 courier contract, which is where the list is decided; the second persona (a first name in mark39)
redrawn from the same seed. Heart: nearest driver or stump 0.05 (mark171, mark472, mark106's stump 0.04).

- **Pairing.** Supply Chain & Logistics (house domain) in its client domain Urban & Regional Science, task type
  forecasting (demand, load and capacity prediction), which serves Forecasting & Predictive Modeling. The deciding
  quantity is a 2027 capacity figure: the van-hours the retailer's runs would no longer drive in 2027 if a set of
  outlying districts went to a regional courier, worked from the run records' stop sequences.
- **Niche.** Brackloon Direct Ltd, an online farm, pet and garden supplies retailer delivering heavy orders (feed,
  bedding, fencing, garden goods) across Mayo and west Galway from one depot at Castlebar with its own vans, each run a
  territory swept in road order with the day's stops. Owenduff Couriers, a regional courier already delivering for
  other shippers in the west, offers to take Brackloon's parcels in named outlying districts from 1 January 2027 at a
  per-parcel price, collected at the depot.
- **The call.** Which districts in Owenduff's offer go to Owenduff from January 2027, and what the hand-over saves over
  2027: the planning standard sets the saving as the 2027 cost of the van-hours the runs would no longer drive, at the
  2027 van-hour rate, less Owenduff's 2027 charges for those districts' parcels, and the set as the one that lowers the
  year's cost most. Forward facing: a contract for a year not yet run, decided at the November executive meeting.
- **Shape.** other: a per-district verdict grid with a predicted figure per district (the 2027 van-hours no longer
  driven, their cost, Owenduff's charge, in or out), the set, the year's saving, the district nearest the line and the
  van-hours each run sheds, with the chart of saving against charge. Decision designation_set, answer set_of_items,
  question form which.
- **Strategy.** decomposition_attribution: a run's time belongs to the districts on it only through what each set of
  them would take off it. Gap objective (decisive: the time a district's stops take is a correct measure and not what
  the decision is scored on) then population (the set, not the district, is the unit a spur prices); generators G5
  (provision elsewhere: the drive through a district is needed for the districts beyond it) decisive, G8
  (reachability: a spur's near district is the end of the run only once the far one goes), G16 (method selection: the
  counterfactual leg times from a model the skipped run-days check out of sample); Gate G forecasting; calibration none;
  context artifact register (the district register); Layer 2 family estimand_identification, pattern
  own:avoidable-drive-on-shared-runs.
- **Forum, event, organisation.** executive_team (the meeting that approves the 2027 courier contract), vote_or_meeting,
  retailer_or_ecommerce. Role operations_director (the head of logistics, who takes the list to that meeting).
- **People** (`guard.py names --geo Ireland --seed 404`, locale en_IE): Niamh Gilbride, head of logistics, who asks;
  Aislinn Duffin, transport planner, who pulled the run records; Karl Eivers, Owenduff's commercial manager, who signs
  the offer. None appears in the prompt.
- **Deliverables.** The hand-over workbook (the district grid and the runs) and one chart (each district's in-house
  saving against Owenduff's charge, the ones that go marked): xlsx and png.
- **Data-native sentence.** A Brackloon van sweeps its territory in road order, so on the Achill, Clifden and
  Ballycastle runs it drives through Mulranny, Leenane, Letterfrack and Killala to reach the far end, and on the Erris
  run it drives through Bangor Erris to Belmullet and back the same road: the time a through-road district's stops take
  includes drive the run makes anyway, and Bangor Erris costs the run little only while Belmullet stays.
- **Abstraction sentence** (the one a reviewer holding this build beside its nearest approved build would say is the
  same, without domain nouns): none writable. Against mark106 (candidates sized against a shared finite pool of spare
  return-leg time, which double-books the pool) nothing here is shared or rationed; against mark67 (a denser period
  re-priced from a stem-and-drop split recovered from a shipped field) nothing is re-priced from a field; against
  mark162 and mark151 (history replayed through a setting) nothing is replayed through a setting. The quantity is the
  counterfactual run time when a set of stops leaves a run.
- **Same-puzzle and library tests.** Gap objective, decisive pattern G5 and designation_set repeat no build in the last
  twelve (`check`); the stump is no named correction applied as a card states it: no rigor card carries a district's
  saving as the counterfactual run time without it, with a spur's districts priced together.
- **Sources.** Last-mile cost-to-serve practice (van time charged to stops by the drive in and the time at the door);
  the planning standard's avoidable-cost definition in the organisation's genre; territory runs swept in road order;
  regional couriers consolidating several shippers' rural parcels; the client's two-layer standard.

## Default path

1. Read Owenduff's offer (the districts, the 2027 price per parcel), the planning standard (the saving's definition, the
   2027 rate), the 2027 volume plan (parcels by district) and the 2027 rate card (the all-in van-hour rate).
2. Clean the handheld stop log (re-synced duplicate stops dropped, local times across the clock changes, failed attempts
   and collection-only stops kept as stops) and give each outlying district its van time on each run-day: the drive in
   from the stop before, the drives between its stops and the time at each door (the field's cost-to-serve build,
   which reconciles each run-day's time to the minute with the depot legs).
3. Carry each district's 2026 van time to 2027 by its plan parcels, price it at the 2027 rate, set it against
   Owenduff's charges and hand over every district whose in-house cost is the higher.

Ends on: hand over Mulranny, Leenane, Letterfrack and Killala with Achill, Clifden, Ballycastle, Belmullet and Louisburgh
(the through-road districts priced at drive the runs make anyway).

Golden: hand over Achill, Belmullet, Bangor Erris, Clifden, Ballycastle and Louisburgh and keep the through-road
districts, each set of districts priced at the run time it removes (sets and figures to be fixed by the generator).

## Stump sentence

A competent solver prices each outlying district at the van time its stops take, the drive in from the stop before, the
drive between its stops and the time at the door, and hands Mulranny, Leenane, Letterfrack and Killala to the courier
with the remote ends; the runs drive through those districts anyway to reach Achill, Clifden and Ballycastle, so the
time they would no longer take is only their stops' own, and only pricing each set of districts at the run time it
removes keeps them and hands Bangor Erris over with Belmullet, the end of the Erris spur once Belmullet goes.

## Deep reasoning

Task type: forecasting (Urban & Regional Science: demand, load and capacity prediction), the client domain the house domain supply-chain-logistics sits in, a task type the taxonomy tags for Forecasting & Predictive Modeling; the forecast is the network's 2027 van-hours with and without each set of districts.
Domain test: the quantity that decides is each set of districts' 2027 avoidable van-hours, the route network's own capacity measure, estimated as the run time the van runs would no longer take: the counterfactual run built from the stop sequences with the set's stops removed, its replacement legs taken from a leg-time model on the observed inter-district legs and checked against the run-days that skipped the set.
Swap: "which of our outlying wards should go to an agency nurse service from January, and what will it save" keeps a cost comparison but loses the van run that drives through one district to reach the next and the spur a far district hangs on, so nothing ties a ward's saving to the wards beyond it and the call stops reading the same.
Layer 1: the retailer's handheld and depot systems produce it: stop rows duplicated when a handheld re-syncs after a dead spot, stop times in local time across the March and October clock changes, failed attempts and collection-only stops, a district split in the register in 2026 with a crosswalk, missing departure scans, peak-day runs split across two vans; each is neutral on the call (to be asserted) and none is placed to be caught.
Layer 2: estimand_identification: the planning standard files the saving as the cost of the van-hours the runs would no longer drive; the methodological choice is how a district's or a set's share of a run is valued: by stops or parcels (allocation), by the time its stops take (cost-to-serve), by the run time its removal takes off one district at a time, or by the run time each set removes, spur districts together.
Decisive step: the 2027 van-hours a set of districts would take off the runs, the counterfactual run with the set's stops removed and the drive between the stops either side put back, evaluated set by set on each run because a spur's near district ends the run only once the districts beyond it go.
Not semantics: every field read right (the sequence numbers, the clock changes, the district crosswalk, failed and collection stops, the plan's parcels, the rate card) still leaves a solver pricing a district at the time its stops take: no field of a stop says which drive the run would make without it, and the time-in-district build reconciles every run-day to the minute.
Not rule application: the planning standard files the WHAT (the saving is the 2027 cost of the van-hours no longer driven, at the 2027 rate, less Owenduff's charges; the set is the one that lowers the year's cost most) and nothing filed says how a district's removal is valued; the enumerated family (allocation by stops, by parcels, by time; time in district with or without the exit leg; removal one district at a time; removal set by set) names four different sets; the standing family after a literal read of "no longer drive" keeps the time-in-district builds and the one-at-a-time removal, because nothing filed or in the schema rules them out; what rules them out is quiet: the run-days that skipped a district, which look like any other run-day (measured spreads to be asserted in checks.py once the generator exists).
Analyst test: a strong analyst who cleans the stop log and reads the offer, the standard, the plan and the rate card correctly prices each district at the time its stops take, carries it to 2027 and hands Mulranny, Leenane, Letterfrack and Killala over with the remote ends, the default path's Ends on, where the golden keeps them; on the generator's clean truth the same route files the same set (to be executed in checks.py).
Estimand: the planning standard (Brackloon's network planning standard, the section on handing districts to partners): the 2027 saving of a set of districts is the cost at the 2027 van-hour rate of the van-hours the runs would no longer drive in 2027 without those districts' stops, less the partner's 2027 charges for their parcels; the set handed over is the one that lowers the year's cost most; population the districts in the partner's offer, outcome the year's cost, window 1 January to 31 December 2027, unit EUR and van-hours.
No decoy: nothing is planted: the offer and the plan are ordinary commercial documents, the register is the planning team's own, no memo, earlier cost-to-serve report, draft or stakeholder figure ranks the districts, and no file is shipped to carry the wrong answer.
No certified replay: the method is not recovered by reproducing a published figure: no file states a district's van time, cost to serve or saving, and nothing filed is reproduced to recover the valuation.
Chain: (1) a district's saving is the run time its removal takes off the runs, not the time its stops take, so (2) on a through-road the drive between the stops either side is put back, estimated from a leg-time model on the observed inter-district legs and checked against the run-days that skipped the district, which (3) on a spur makes the near district's saving depend on whether the districts beyond it go, so the sets are evaluated run by run together, and (4) carried to the 2027 plan's parcels at the 2027 rate against Owenduff's charges, the set and the year's saving follow.
Judgment: the counterfactual run time without a set's stops is a model, not a lookup: replacement legs between stops that were never consecutive while the set was visited come from a leg-time model fitted on the observed inter-district legs (time against the register's centroid distance and road class), justified out of sample by predicting the run-days that skipped the set, where the counterfactual run was actually driven.
One-fact test: the likeliest hint ("the van still drives through a through-road district to reach the next one") leaves the replacement legs to estimate and check against the skipped run-days, the spur sets to evaluate together and the 2027 carry; the other hint ("Bangor Erris is the end of the spur once Belmullet goes") leaves the through-road districts priced at time in district; no one sentence makes the rest routine.
No replay: the call does not re-derive any published figure, and no stated number in the pack is wrong.
Pinned: the rivals to run on the clean truth at stage 2: allocation by stops, parcels and time; time in district with and without the exit leg; removal one district at a time; removal set by set with replacement legs from skipped run-days, from the leg-time model, and from a run-day regression on district visits with spur interactions; and the 2027 carry by parcels against by visit days; each must land on the golden's set or be ruled out by named data (to be asserted).
Run forecast: method shortcut at rung 1 (the field's cost-to-serve time in district, validated by its own reconciliation); a run that reaches removal stops one inference short at rung 2 (one district at a time, keeping Bangor Erris), an unfinished chain; either files a set the golden does not.
Strategy label: WORKS IN FORM (Urban 03, net, not gross: the drive the runs make anyway is estimated, never filed, in the live form; with Part A's separating-explanations form for the spur, where only a like-for-like run rebuilt from the run-days separates the two).
Lesson: a district's saving from leaving a route network is the run time its removal takes off, which for a through-road district is only its own stops and for a spur depends on the districts beyond it; no build on file prices a set of route members at the counterfactual run time.

## Survivor anatomy

Actor: which drive a run would make without a district has no column in any file; it is a relation between the stops either side of the district's stops in the sequence, and between run-days that did and did not visit it.
Link: each district's saving is tied to the leg between the stops either side of it and to the run-days that skipped it, a relation no key offers (no field carries a replacement leg, a through-road or a spur) and no sentence invites.
Reflex: the field's cost-to-serve build (each district's van time: the drive in, the drives between its stops, the time at each door) and the allocation builds sit at rungs 0 and 1 and file the default set (Ends on), not the golden.
Back-test: the time-in-district build reconciles every run-day's time to the minute with the depot legs, so it passes the only check the records offer a cost allocation; one-district-at-a-time removal matches every single skipped run-day.
Second use: every file the step reads sits in the pack for its own reason: the stop log is the population every figure is over, the run-day log gives the runs' hours for the run ask, the register gives the districts and their centroids for the chart and the joins, the offer, the plan and the rate card price the call.
Shock: the movement the step recovers reads as ordinary: through-road districts look costly per parcel on any statistic, and sorted on any shipped statistic (distance from the depot, parcels, stops, time in district) the golden set is not an interval (to be asserted).
Pins: the planning standard files the WHAT (the saving's definition, the 2027 window and rate, the set that lowers the year's cost most) in the organisation's own standard; no filed sentence names a through-road, a spur, a replacement leg, a skipped run-day or how a district's removal is valued.

## Tried and rejected

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
