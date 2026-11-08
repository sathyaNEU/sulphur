# task4 design note

## Draw

Card `.claude/skills/fingerprint/cards/task4.json`, architecture 4, registered 2026-11-08 (a re-root: architecture 3,
the Polish parcel carrier's October scan alerts, was landed by both platform runs, which reached the golden's call and
every graded figure, so the platform returned not stumped before any rubric; the card's lineage records it spent with
architectures 1 and 2). One architecture per world: a new world (the west of Ireland), a new dataset (van run stop
sequences), a new organisation family (an online retailer's own fleet) and a new shell (which | i'd | png+xlsx against
whether | the | pptx+xlsx and how-many | in | png+xlsx).

Guard on the registered card (`heart`, the last act before stage 3): WARN only, `repeat.decision` (designation_set
after task6 v6): task6 designates a different kind of set in another domain; the honest decision type here is a set
of districts. Axes redrawn: the forcing event at the draw (purchase_order_or_contract BLOCKed against task1 and task3,
budget_or_appropriation against mark456; now the November meeting that approves the courier contract, vote_or_meeting),
the second persona (a first name in mark39), and at the heart screen the forum (executive_team BLOCKed against task6,
registered after this draw; now committee_or_panel, the 2027 budget committee that approves the contract, the body
that actually decides). Heart nearest 0.06 (mark171), mark106's stump 0.04. `surface` exit 0, one pair promoted for
the author: task4 against task5's re-draw (same decisive gap, objective, and decision type, designation_set, back to
back); both builds are in flight and each label is the honest one for its own build.

- **Pairing.** Supply Chain & Logistics (house domain) in its client domain Urban & Regional Science, task type
  forecasting (demand, load and capacity prediction), which serves Forecasting & Predictive Modeling. The deciding
  quantity is a 2027 capacity figure: the van-hours Brackloon's runs would no longer take in 2027 if a set of outlying
  districts went to a regional courier.
- **Niche.** Brackloon Direct Ltd, an online farm, pet and garden supplies retailer delivering heavy orders across Mayo
  and west Galway from one depot at Castlebar with its own vans. Nine runs, each a van's territory swept outward in
  road order with the day's stops and driven back from the farthest district it served. Owenduff Couriers, a regional
  courier already carrying other shippers' rural parcels, offers eleven outlying districts from 1 January 2027 at
  EUR 13.40 a parcel delivered, for any of the districts Brackloon lists.
- **The call.** Which districts go to Owenduff and what the hand-over saves over 2027. NPS-3 section 4 files the WHAT:
  the saving is the cost, at the 2027 all-in van-hour rate (EUR 58.00), of the van-hours the hand-over takes off the
  runs, less Owenduff's charges for the districts' plan parcels; the districts handed over are those whose hand-over
  lowers the year's delivery cost most. Forward facing: a contract for a year not yet run.
- **Shape.** other: the list of offered districts going and staying, the van-hours each run that serves one saves in
  2027 (seven runs, to the nearest 100), the year's net saving (to the nearest EUR 5,000) and a chart of each of those
  runs' 2027 van-hours before and after the hand-over (fourteen values). Decision designation_set, answer
  set_of_items, question form which.
- **Strategy.** decomposition_attribution: a run's time belongs to its districts only through what each set of them
  takes off it. Gap objective (decisive: the time a district's stops take is a correct measure and not what NPS-3 4.1
  scores) then population (the set, not the district, is what a run's far end prices); generators G5 (provision
  elsewhere: the road through a district is driven for the districts beyond it) decisive, G8 (reachability: a
  district ends its run only once the districts beyond it go), G16 (method selection: the 2027 year forecast from the
  plan's stops, chosen by a back-test); Gate G forecasting; calibration none; context artifact register; Layer 2
  family estimand_identification, pattern own:avoidable-drive-on-shared-runs.
- **Forum, event, organisation.** committee_or_panel (the 2027 budget committee), vote_or_meeting (its November
  meeting, before the offer lapses on 30 November), retailer_or_ecommerce. Role operations_director (the head of
  logistics, who takes the list to the committee).
- **People** (`guard.py names --geo Ireland --seed 404`, locale en_IE): Niamh Gilbride, head of logistics, who asks
  and owns NPS-3; Aislinn Duffin, transport planner, whose workbook the golden is; Karl Eivers, Owenduff's commercial
  manager, who signs the offer. None appears in the prompt.
- **Deliverables.** district_handover_2027.xlsx (the districts, the runs, the net saving) and handover_2027.png (each
  run's 2027 van-hours before and after): xlsx and png.
- **Data-native sentence.** A Brackloon van sweeps its territory outward and drives back from the farthest district it
  served, so the Connemara van drives the road through Leenane and Letterfrack every day to reach Clifden, which a
  handful of hotels and shops make cheap to keep, while on the Achill and Erris runs Mulranny and Bangor Erris cost
  little only as long as Achill and Belmullet stay beyond them.
- **Abstraction sentence** (the one a reviewer holding this build beside its nearest approved build would say is the
  same, without domain nouns): none writable. Against mark106 (candidates sized against a shared finite pool of spare
  return-leg time, which double-books the pool) nothing is shared or rationed; against mark67 (a denser period
  re-priced from a stem-and-drop split recovered from a shipped field) nothing is recovered from a field; against
  mark162 and mark151 (history replayed through a setting) nothing is replayed through a setting. The quantity is the
  counterfactual run time when a set of stops leaves a run, priced set by set.
- **Same-puzzle and library tests.** Gap objective, decisive pattern G5 and designation_set repeat no build in the last
  twelve (`check`); the stump is no named correction applied as a card states it.
- **Sources.** Last-mile cost-to-serve practice (van time charged to stops by the drive in and the door time);
  territory runs swept in road order; regional couriers consolidating rural parcels; avoidable-cost reasoning in the
  organisation's own standard; the client's two-layer standard. All files constructed (`metadata.json`), real place
  names on approximate public centroids.

## Default path

1. Read Owenduff's offer (eleven districts, EUR 13.40 a parcel delivered in 2027, any of them), NPS-3 section 4, the
   2027 rate card (EUR 58.00 a van-hour), the 2027 plan (parcels by district and month) and the 2027 calendar.
2. Clean the stop log (re-synced copies dropped, CBN and CBS mapped back to Castlebar town, failed attempts and
   collections kept as stops) and give each offered district its van time on each run-day of the last twelve months:
   the drive in from the stop before, the drives between its stops and the door time (the field's cost-to-serve
   build, which reconciles every run-day to the minute with the depot legs and the break).
3. Carry each district's van time to 2027 by its plan parcels, price it at EUR 58.00, set it against Owenduff's
   charges and hand over every district whose van time costs more.

Ends on: hand over Leenane and Letterfrack with Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh and Ballycastle,
claiming about EUR 20,000.

Golden: hand over Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh and Ballycastle and keep Leenane, Letterfrack,
Clifden, Cong and Charlestown, about EUR 50,000 net in 2027.

## Stump sentence

A competent solver prices each offered district at the van time its stops take and hands Leenane and Letterfrack to
the courier with Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh and Ballycastle, claiming about EUR 20,000; the
Connemara van drives through Leenane and Letterfrack to reach Clifden, which stays, so they save only their own stops,
and the solver who prices the run without them but one district at a time keeps Mulranny and Bangor Erris, which end
the Achill and Erris runs once Achill and Belmullet go: only every combination priced on the run hands over Mulranny,
Achill, Bangor Erris, Belmullet, Louisburgh and Ballycastle, about EUR 50,000 net in 2027.

## Deep reasoning

Task type: forecasting (Urban & Regional Science: demand, load and capacity prediction), the client domain the house domain supply-chain-logistics sits in, a task type the taxonomy tags for Forecasting & Predictive Modeling; the forecast is each run's 2027 van-hours with and without each set of offered districts.
Domain test: the quantity that decides is each set of districts' 2027 avoidable van-hours, the route network's own capacity measure, estimated as the run time the runs would no longer take: each run's road sections and district access times fitted by least squares on the stop log's observed drives, door and local times measured per district, and a 2027 year in which a section is driven on the days some district beyond it has a stop.
Swap: "which of our outlying wards should go to an agency nurse service from January, and what will that save" keeps a cost comparison but loses the van run that drives through one district to reach the next and the run's far end a district inherits when the one beyond it goes, so nothing ties a ward's saving to the wards beyond it and the call stops reading the same.
Layer 1: the retailer's handhelds and fleet app produce it: stop rows sent again when a handheld re-synced (same stop and times, a later sync time), departure scans missing, failed attempts and collection-only stops, the Castlebar town district split in the register on 1 April 2026 with a crosswalk, the fleet app re-exporting some run-days twice, blank closing odometers, run names re-keyed with an ampersand after the March 2026 upgrade, a handheld swapped at the summer service; each is neutral on the call (SF5, SF6, SF7, SF15 asserted) and none is placed to be caught.
Layer 2: estimand_identification: NPS-3 4.1 files the saving as the cost of the van-hours the hand-over takes off the runs; the methodological choice is how a district's share of a run is valued: by stops or parcels (allocation), by the time its stops take (cost-to-serve), by the run time its removal takes off one district at a time, or by the run time each combination takes off, priced set by set, with the 2027 year carried by parcels or forecast from the plan's stops.
Decisive step: the run time a set of districts takes off its run, the road sections a run must still drive to reach the districts beyond them put back, priced over every combination on the run, because a district ends its run only once the districts beyond it go.
Not semantics: every field read right (sequence numbers, the break rows, the crosswalk, failed and collection stops, the plan's parcels, the calendar, the rate card) still leaves a solver pricing a district at the time its stops take: no field says which road a run would drive without a district, and the time-in-district build reconciles every run-day to the minute.
Not rule application: NPS-3 files the WHAT (4.1 the saving, 4.2 the year's parcels, rate and days, 4.3 the districts whose hand-over lowers the year's cost most) and nothing filed says how a district's removal is valued; the enumerated family (allocation by stops; time in district with and without the exit leg; removal one district at a time; removal set by set; each with the year carried by parcels or forecast) names four different lists (the golden; the golden plus Leenane and Letterfrack; the golden plus Leenane, Letterfrack and Cong; the golden less Mulranny and Bangor Erris, with allocation adding Leenane and Letterfrack and dropping Louisburgh) and spreads the net saving from EUR 20,000 to EUR 55,000; the standing family after a literal read of 4.1 and 4.3 keeps time in district (the time the stops take reads as the time the hand-over takes off) and one-at-a-time removal, and what rules them out is quiet: run-days that skipped a district, which look like any other run-day.
Analyst test: a strong analyst who cleans the stop log and reads the offer, NPS-3, the plan, the rate card and the calendar correctly prices each district at the time its stops take, carries it to 2027 and and hands over Leenane and Letterfrack with Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh and Ballycastle, claiming about EUR 20,000, the default path's Ends on; on the generator's clean truth (no mess) the same route files the same list (checks.py R2).
Estimand: NPS-3 4.1 to 4.3 (network_planning_standard_NPS-3.pdf), with 2.3 and 3.2: population the districts in Owenduff's offer, outcome the 2027 delivery cost (van-hours depot out to depot in at the 2027 all-in rate, plus Owenduff's charges), window the calendar year 2027 at the delivery calendar's days, unit EUR and van-hours, comparison the year's cost with and without the hand-over.
No decoy: nothing is planted: the offer, the plan and the rate card are ordinary commercial documents, the register is the planning team's own, no memo, earlier cost-to-serve report, draft or stakeholder figure ranks the districts, and no file is shipped to carry the wrong answer.
No certified replay: the method is not recovered by reproducing a published figure: no file states a district's van time, cost to serve or saving, and nothing filed is reproduced to recover the valuation.
Chain: (1) a district's saving is the run time its hand-over takes off its run, not the time its stops take, so (2) the road sections a run still drives to reach the districts beyond it are put back, estimated by least squares on the observed drives and checked on the run-days that skipped the district, which (3) makes a district's saving depend on whether the districts beyond it go, so every combination on each run is priced, and (4) the 2027 year is forecast from the plan's stops month by month with each section driven on the days a district beyond it has a stop, which the 2025 to 2026 back-test chooses over carrying the hours in proportion, giving the list and the year's saving.
Judgment: the counterfactual run time is a fitted model of the run, not a lookup: road sections and access times from least squares on 2025 and 2026 drives (each section within 8 per cent of the truth, checks.py R5), and the 2027 year forecast with a section driven with the Poisson probability that some district beyond it has a stop; fitted on 2025 and forecasting 2026, it errs by 21 hours across the seven runs against 177 for the proportional carry (checks.py back-test).
One-fact test: the likeliest hint ("the van still drives through a district to reach the next one") leaves the sections to fit, the combinations to price and the 2027 year to forecast, and the one-at-a-time pricing it invites still keeps Mulranny and Bangor Erris; the other hint ("a district at the end of a run saves the drive to it") leaves Leenane and Letterfrack priced at their time in district; no one sentence makes the rest routine.
No replay: the call does not re-derive any published figure, and no stated number in the pack is wrong.
Pinned: run on the cut pack and the clean truth: the fit on 2025 alone, on 2026 alone, with median drives, with annual instead of monthly stops, and a regression of run-day hours on the sections reached, the districts entered and their stops (verify.py) all give the golden list, a net saving that rounds to EUR 50,000 (49,171 to 50,798) and every run figure at its rounding; time in district with or without the exit leg, allocation by stops and one-at-a-time removal each file another list (SF9, SF10); the proportional carry rounds to EUR 55,000 (SF11).
Run forecast: method shortcut at rung 1 (the field's cost-to-serve time in district, validated by its own reconciliation); a run that reaches removal stops one inference short at rung 2 (one district at a time, keeping Mulranny and Bangor Erris), an unfinished chain; a run that lands the list and carries the year in proportion files EUR 55,000, an unfinished chain on the forecast.
Strategy label: WORKS IN FORM (Urban 03, net not gross: the drive the runs make anyway is estimated, never filed, in the live form; with Part A's separating-explanations form for the run's far end, where only the run priced without the set, rebuilt from the fitted run, separates the district's own cost from the road it sits on).
Lesson: a district's saving from leaving a route network is the run time its removal takes off, which for a district the run drives through is only its own stops and for a district near the end depends on the districts beyond it, forecast for the year from the days each road section is needed; no build on file prices a set of route members at the counterfactual run time.

## Survivor anatomy

Actor: which road a run would drive without a district has no column in any file; it is a relation between a district's place in the stop sequences, the drives either side of it and the run-days that skipped it.
Link: each district's saving is tied to the road sections beyond it and to the run-days that skipped it, a relation no key offers (no field carries a road section, a through-road or a run's far end) and no sentence invites.
Reflex: the field's cost-to-serve build (each district's drive in, the drives between its stops, its door time) and the allocation builds sit at rungs 0 and 1 and file the default list (Ends on), not the golden.
Back-test: the time-in-district build reconciles every run-day's time to the minute with the depot legs and the break, so it passes the only check the records offer a cost allocation; one-district-at-a-time removal reproduces every single skipped run-day.
Second use: every file the step reads sits in the pack for its own reason: the stop log is the population every figure is over, the run log gives depot out and in for the van-hours NPS-3 2.3 counts, the register gives the districts and runs, the offer, plan, rate card and calendar price the year.
Shock: the movement the step recovers reads as ordinary: Leenane and Letterfrack look costly per parcel on every shipped statistic, and sorted on distance from the depot, parcels, stops or time in district the golden list is not an interval (Louisburgh goes at 33 km while Leenane stays at 45 km; Clifden, the farthest, stays).
Pins: NPS-3 files the WHAT (the saving, the year's figures, the list that lowers the year's cost most, van-hours depot out to depot in, a district handed over whole) in the organisation's own standard; no filed sentence names a road, a drive, a run's far end, a skipped run-day, a combination or how a district's removal is valued (asserted: checks.py searches the standard's text).

## Readability screen

Seven tests per rung: 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a column, key or
marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or corpus scores
the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of a reported
figure; 7 a file the step alone reads.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 allocation by stops: golden less Louisburgh plus Leenane and Letterfrack | NPS-3 2.3 counts van-hours by run | run-day hours over stops | yes, pro-rata cost | none | no | a share | none | readable |
| 1 (default) time in district: golden plus Leenane and Letterfrack | 4.1's "van-hours the hand-over takes off" read as the time its stops take | the stop times | yes, the field's cost-to-serve | none refutes it | no | a sum | none | readable |
| 2 removal one district at a time: golden less Mulranny and Bangor Erris | none | the sequences | yes, avoidable cost | none | no | a difference per district | none | readable |
| 3 (decisive) every combination priced on the fitted run, the year forecast from the plan's stops | no sentence names a road section, a far end, a combination or a skipped run-day; 4.3 names only the outcome (lowers the year's cost most) | no column holds a section or a far end | no: the reflexes are cost-to-serve and avoidable cost per district | nothing scores it | no | not linear: a fitted run priced over subsets and a Poisson year | the stop log is the population file | silent |

**Condition 1 (the review's Gate F risk), measured on the wording.** The prompt asks for "the van-hours it saves" and
"van-hours before and after the hand-over"; NPS-3 4.1 says "the van-hours the hand-over takes off Brackloon's runs".
Nothing in the pack computes run time with a district removed: the stop log records the stops made, the run log
depot out and in, the register districts and runs, and no file holds a road section, a distance between districts or
a run planned without a district (checks.py asserts the standard names no road, drive, through-road, combination or
skipped run-day). From a stop-level log the direct build of "what a district's hand-over saves" is the time its stops
take, which is rung 1, and the evidence against it sits only in ordinary run-days on which a district had no stop.
The asking sentence was cut from "the van-hours our runs would no longer drive" and "the van-hours each run would
shed" (the draw's draft) to "the van-hours it saves", which names the outcome and no counterfactual.

**Condition 2, the forecasting objective.** The 2027 year is a forecast judgment that moves graded figures: the
plan's monthly parcels become stops at each district's own stops a parcel, and a road section is driven on a
delivery day with the probability that some district beyond it has a stop; the proportional carry of the last twelve
months' hours files EUR 55,000 against the golden EUR 50,000, and every run's before and after figures differ (the
landed run misses 16 of 23 ask figures, ceiling.py). The back-test chooses the model: fitted on 2025, it forecasts
2026 January to October within 21 van-hours across the seven runs against 177 for the proportional carry. The tag
stays Forecasting & Predictive Modeling.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | 2027 | the calendar year at the delivery calendar's 251 delivery days | weekdays | same call | NPS-3 4.2; same call (asserted, SF16) |
| SF2 | a van-hour | depot out to depot in as the run log records, the break inside | the stop log's drives and door times only | same list and figures | NPS-3 2.3; the verifier regresses run-log hours (verify.py) |
| SF3 | the break | taken once on every run-day and never saved | saved with a district | same call | every run-day carries one break (asserted); NPS-3 3.2 removes stops, not the break |
| SF4 | the year's parcels | the commercial plan's 2027 parcels | the last twelve months' parcels | same list | NPS-3 4.2; same list (asserted) |
| SF5 | failed attempts and collections | stops the run makes | dropped | same list | NPS-3 2.4 and 3.1; same list (asserted) |
| SF6 | a stop sent again at re-sync | one stop | two | same call | the same stop and times with a later sync time; the copies sit on existing run-days (asserted) |
| SF7 | CBN and CBS | Castlebar town, split in the register | separate districts | same call | the register's Code changes; Castlebar town's run serves no offered district (asserted) |
| SF8 | Owenduff's charge | EUR 13.40 a parcel delivered | per stop, or per attempt | same call | the offer (a parcel is charged once, when delivered) |
| SF9 | the districts handed over | the combination that lowers the year's cost most, run by run | each district on its own merit | moves Mulranny and Bangor Erris | NPS-3 4.3's selection whose hand-over lowers the year's cost most, an outcome and no search (asserted: the offer names no combination) |
| SF10 | the van-hours a hand-over takes off | the run's time with the set's stops removed, the road to the districts beyond still driven | the time the set's stops take | moves Leenane and Letterfrack | NPS-3 4.1 and 3.2 (the runs make no stop in the district and still serve the districts beyond it); run-days that skipped a district (asserted) |
| SF11 | the 2027 hours | forecast from the plan's stops month by month, each section driven on the days a district beyond it has a stop | the last twelve months' hours carried by parcels | net saving EUR 55,000 | the 2025 to 2026 back-test (21 against 177 van-hours, asserted) |
| SF12 | rounding | van-hours saved to the nearest 100, other van-hours to the nearest 50, the net saving to the nearest EUR 5,000, every graded figure mid-bin | finer | same figures | the prompt; saved hours within 25 of their bin centre, before hours within 12, the net saving within EUR 1,500, and every variant in the same bin (asserted); the judge's independent fit moved a run's saved hours by about 30 |
| SF13 | the runs that serve an offered district | R03 to R09 | all nine runs | same figures | the prompt ("each run that serves one"); asserted |
| SF14 | the fit | 2025 and 2026 drives, least squares on the mean of each from-to pair | 2025 alone, 2026 alone, medians, annual stops, a run-day regression | same list and rounded figures | asserted for each, and verify.py |
| SF15 | a stop with no departure scan | its drive to the next stop left out of the fit | the run-day dropped | same list and saving | asserted |
| SF16 | delivery days | the 2027 calendar | weekdays | same list | asserted |

## Ladder

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | allocation by stops: each run-day's hours shared over its stops, carried by parcels | Mulranny, Achill, Bangor Erris, Belmullet, Leenane, Letterfrack and Ballycastle | NPS-3 4.1: the van-hours taken off the run, not the run's average; Louisburgh's run drives 2 x 0.6 h for it alone |
| 1 (default) | time in district (drive in, between its stops, door time), carried by parcels | the golden plus Leenane and Letterfrack (ratios 1.48 and 1.42), EUR 20,000; with the exit leg also Cong | the run-days that skipped Leenane or Letterfrack: the Connemara van drove the same road to Clifden |
| 2 | removal one district at a time on the fitted run | the golden less Mulranny and Bangor Erris (0.58 and 0.66), EUR 35,000 | NPS-3 4.3: with Achill and Belmullet gone, Mulranny and Bangor Erris end their runs (marginal 1.78 and 2.37) |
| 2b | every combination, the year carried in proportion to parcels | the golden list, EUR 55,000 | the back-test (177 against 21 van-hours) |
| 3 (golden) | every combination on the fitted run, the year forecast from the plan's stops | the golden list, EUR 50,000 (50,020 before rounding) | |

- **Margins.** Every handed-over district's marginal saving within the golden list is at least 1.78 times its charge
  (Louisburgh 1.90, Achill 2.64, Belmullet 2.75, Bangor Erris 2.37, Ballycastle 1.86, Mulranny 1.78); every kept
  district's at most 0.67 (Cong), and the largest Connemara combination 0.78 (asserted at 1.15 and 0.87). Rung 1's
  wrong cells, Leenane and Letterfrack, sit at 1.48 and 1.42; rung 2's at 0.58 and 0.66.
- **Position.** Three different wrong lists on rungs 0 to 2; the decisive move reverses the direction of rung 1 on
  Connemara and of rung 2 on Achill and Erris.
- **Worth.** The decisive step moves four districts and the net saving from EUR 20,000 (rung 1) or EUR 35,000 (rung 2)
  to EUR 50,000.
- **Pricing on the clean truth** (a pack with no mess, checks.py R1 to R5): the same golden list, the default on
  Leenane and Letterfrack, the one-at-a-time list another, the fitted sections within 8 per cent of the generator's.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | the districts in Owenduff's offer | filed, the offer and NPS-3 4.3 |
| 2 Unit of account | a district, handed over whole | filed, NPS-3 3.2 |
| 3 Attribution window | the calendar year 2027 | filed, NPS-3 4.2 (SF1) |
| 4 As-of dating | the extract to 30 October 2026, the plan of 19 October | C1: the call reads no later record |
| 5 Version basis | NPS-3 version 2, the offer OC-2027-114 | filed |
| 6 Denominator | none: euros and van-hours | n/a |
| 7 Weighting | the plan's parcels by month | filed, NPS-3 4.2 (SF4) |
| 8 Window length | one year | filed |
| 9 Boundary inclusivity | a hand-over that lowers the cost; none at equal | C1, no combination within 13 per cent of break-even (asserted) |
| 10 Rounding path | figures unrounded to the end, van-hours to 50, net to EUR 5,000 | the prompt; C1 (SF12) |
| 11 Tie-break | none | no two combinations tie (asserted by the margins) |
| 12 Maturity and censoring | none: the history is complete to its last day | n/a |
| 13 Order of operations | copies dropped, then drives timed, then fitted | C1 (SF6) |
| 14 Row order | stops ordered by sequence number | C1 |
| 15 Duplicate resolution | a re-synced stop once; a re-exported run-day once | C1 (SF6) |
| 16 Identity normalisation | district codes through the crosswalk | C1 (SF7) |
| 17 Netting against gross | net saving after Owenduff's charges | filed, NPS-3 4.1 |
| 18 Dimensional units | hours and euros | the rate card |
| 19 Code and status semantics | a parcel delivered; failed attempts and collections are stops | filed, NPS-3 2.4 (SF5, SF8) |
| 20 Integerisation | none before the rounding | n/a |
| 21 Clause scope | NPS-3 section 4 for the call, 2.3 and 3.2 for the hours | filed |
| 22 Forward window contents | the plan's 2027 parcels, the calendar, the rate card | filed (SF11 the forecast's form, chosen by the back-test) |

## Literal reader

Executed word for word, NPS-3 4.1 to 4.3 price each combination of offered districts at the cost of the van-hours the
hand-over takes off the runs, depot out to depot in, less Owenduff's charges, and hand over the combination that
lowers the year's cost most; the one step the text leaves open is how the runs' 2027 hours without the combination are
estimated, and every route that rebuilds the run without the combination's stops (the fit on observed drives, the
run-day regression on sections reached, each on either year) gives the golden list, while the time the stops take,
allocation and one-at-a-time pricing are not the hours taken off the runs. SF1 to SF16 close every term and
convention.

## Oracles

None. No file states a district's van time, cost to serve, saving or a run's hours without a district; the fuel card
statement, the customer contact log and the van fleet register (distractors) rank nothing on the decision basis; the
offer names no saving.

## Ask sheet

Four asks, 23 figures, every one computed from the deep step's output: the list (1, the call itself), the van-hours
each run that serves an offered district saves (7), the year's net saving (1), and the chart's before and after
figures for those runs (14). Each ask's second judgment is the 2027 forecast (SF11): a run that lands the list and
carries the year in proportion files other before, after and net figures.

| Ask | Figures | Deep-step output it reads | Second judgment | Shallow run against the golden | Landed run's risk | Mess on its path |
|---|---|---|---|---|---|---|
| 1 the list | 1 | the combinations priced | none | Leenane and Letterfrack added | none | the copies, the crosswalk |
| 2 van-hours saved per run | 7 | the hours each run's combination takes off | the 2027 forecast | 5 of 7 differ (R06 and R09 zero both ways) | R07 and R08 move a bin under the proportional carry | the break, missing departures |
| 3 net saving | 1 | the list and its hours | the 2027 forecast | EUR 20,000 | EUR 55,000 | none |
| 4 before and after per run | 14 | each run's 2027 hours with and without | the 2027 forecast | 12 of 14 differ | 12 of 14 differ | the break in depot out to in |

| Ask figure | Golden | Shallow (the default path) | Cracker (lands the list, carries the year in proportion) |
|---|---|---|---|
| 1 the list | the golden six | miss | keep |
| 2 van-hours saved, R03, R04, R05, R06 and R09 | 300, 700, 0, 0, 0 | miss | keep |
| 2 van-hours saved, R07 and R08 | 600, 200 | miss | miss |
| 3 the net saving | EUR 50,000 | miss | miss |
| 4 before and after, R06 | 1,200 and 1,200 | keep | keep |
| 4 before and after, R03, R04, R05, R07, R08 and R09 | 12 figures | miss | miss |

- **Span:** the stop log, the run log, the register, the plan, the rate card and the calendar; no ask reads a file the
  call does not.
- **Realism:** the depot-out-to-in hours with the break inside, the plan's months and the calendar's holidays are what
  a transport planner works from.
- Shallow keep: 8.7 per cent of ask weight (2 of 23 figures).
- Pair ceiling: 39.3 (the landed run C = 38 + 7 + 55 x 0.304 = 61.7, the shallow run S = 5 + 7 + 55 x 0.087 = 16.8).
- Measured by: generator/ceiling.py on the cut pack (pack digest printed with the sheet).

## Prompt contract

What the author's voice rewrite may not drop or change:
- The question: which of the offered outlying delivery districts go to Owenduff Couriers from January 2027 under their
  offer, and what that saves over 2027.
- The hold option is implicit in "which" and NPS-3 4.3 (none may go); keep "which" open, never "which four".
- Deliverables: district_handover_2027.xlsx (every district in the offer marked going or staying; for each run that
  serves one, the van-hours it saves in 2027; the year's net saving after Owenduff's charges) and handover_2027.png
  (each of those runs' 2027 van-hours before and after the hand-over).
- Units and rounding: van-hours saved to the nearest hundred, other van-hours to the nearest fifty; the net saving to the nearest five thousand euros.
- Never add: a district or run count, a road, a drive, "through", "beyond", "combination", "on its own", "no longer
  drive", "shed", "cost to serve", or any method word.

## Pre-ship check

Re-read against the Sulfur standard on the final cut (target.zip 4a9ccea1, golden.zip 801703c8), 2026-11-08.
- Analyst test: a solver that cleans every file and reads every rule still prices each district at its own stops' time
  and hands over Leenane and Letterfrack (EUR 20,000), or prices districts one at a time and keeps Mulranny and Bangor
  Erris (EUR 35,000); both builds pass their own reconciliation to the run log. Yes, analytical.
- Deep chain: removal saving, not time in district; the through-road leg re-estimated from a leg model checked on the
  run-days that skipped a district (the modeling judgment); spur districts evaluated as sets; the 2027 reach forecast
  month by month (back-test 21 h against 180 h for the proportional carry).
- One-fact test: the judge named "price each run with and without each combination of districts" as settling the
  list; it is not in the pack (the offer's "in any combination" was removed at stage 4, NPS-3 4.3 names the selection
  as an outcome), and the forecast still separates the graded figures.
- Banned kinds: no filed procedure, no field reading, no plant, no replay, no single fact; the stop-log re-syncs, the
  Castlebar code split, click-and-collect and failed deliveries are texture off every graded path (mess neutrality
  asserted).
- Gate G: no shipped artefact ranks the districts; the offer lists the candidates only.
- Determinism: every sound fit (2025, 2026, both, median, annual, run-day regression) gives the same list and every
  graded figure in its bin; the judge's independent fit lands the call and EUR 50,000.
- Leak: leak.py REVIEW (the offer names the candidates; generic shared words; 2027 calendar dates), no LEAK. The
  reader's re-read is owed for the two documents changed at stage 4 (the offer's sentence, NPS-3 4.3).

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
