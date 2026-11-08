# task10: Wealdmoor Power Networks, which Halverton primaries need reinforcement committed for winter 2027/28 (architecture 5)

Private, never ships. Architectures 1 to 4 were each spent on the platform: Millrind's paid moderation pool (product
analytics), the pump station's consented overflows (physical and environmental sciences), the union branch's protected
action ballots (political science) and the Irish rapid-charging operator's 2027 availability plan (energy systems,
both runs on the golden 12 hubs on 2026-11-08). The author fixed the client domain at Energy Systems & Utilities for
this re-root, so architecture 5 stays in the domain and moves world, data, decision, quantity, mechanism, prompt shell
and deliverables; architecture 4's build outputs leave the folder at this draw (git history keeps them, and its two
platform runs stay under `runs/`), and the four identities sit in the card's `lineage` with their fates.

## Draw

| Axis | Value |
|---|---|
| Card | `fingerprint/cards/task10.json`, architecture v5, registered 2026-11-08T17:13:57Z, `guard.py check` WARN (answered below), no BLOCK |
| Client domain, subdomain | Energy Systems & Utilities / `load-forecasting`, task type Load, price & renewable forecasting (the deciding quantity is each primary's design-day demand after its credited flexibility), which serves Forecasting |
| Objective | Forecasting & Predictive Modeling: each primary's half-hour of highest demand on the winter 2027/28 design day, a window not yet open, with the flexibility contracted for that winter credited at what its provider will deliver |
| Decision | `designation_set`, answer unit `set_of_items`: the primaries whose reinforcement Wealdmoor commits at its December 2026 investment committee for winter 2027/28 |
| Shape | 10, a scorecard against thresholds: each primary's design-day demand before and after credited flexibility against its firm capacity, each flexibility zone's delivery per megawatt scheduled, each zone's median-winter event days and dispatch cost |
| Mechanism | gap objective (the zone's measured event-window reduction is a correct measurement and is not the provider's delivery the guideline credits), then time (the record's event days had a neighbour with evening headroom; the design day's credit is the provider alone); generators G4 (the drop at each event's start is attributed to the provider when a feeder section was switched away at the same moment), G5 (the moved section was supplied elsewhere, by the neighbouring primary), G3 (the record shows one fall where the operation was two actions) |
| Strategy | `causal_design`, Part A "A comparison that is actually clean", WORKS IN FORM: the contamination shows only through a relation in the data (the neighbour's rise in the same half-hours, through an 11 kV open point in the feeder schedule), never a column or a filed sentence; the comparison is not filed in the estimand; two inferences follow the clean comparison |
| Layer 2 | `estimand_identification`, `own:flexibility-relief-net-of-control-room-transfers-mirrored-at-the-neighbour` (the client lists no Energy rigor card) |
| Stakeholder | the head of DSO for the Halverton zone (Marion Todd in the documents, never in the prompt), who takes the reinforcement list to the investment committee; `role_family` operations_director (the DSO function runs the flexibility service and network operation; capacity_planner is task3's in the last three) |
| Forum, forcing event, org family | committee_or_panel (Wealdmoor's investment committee, 9 December 2026); vote_or_meeting (the committee commits the transformer orders a winter 2027/28 reinforcement needs); utility_or_infrastructure |
| World | England: Wealdmoor Power Networks plc (a fictional distribution network operator), its Halverton city zone (nine 33/11 kV primaries fed from Halverton grid supply point), providers Corvane Flex (domestic heat pump and battery aggregation) and Quillon Energy Services (commercial demand response); GBP; people drawn with `guard.py names --geo uk --seed 1005`: Marion Todd, Clifford Evans, Irene Carpenter |
| Shell | question form which (a designation asks which); second sentence led by "Build"; deliverables `halverton_primary_capacity_2027-28.xlsx` and `investment_committee_2027-28.pptx` (pptx+xlsx, under the corpus quota where docx+xlsx stood at 40 per cent); no lineage shell repeated (how-many/put, whether/the, where/the, where/return) |

**Guard WARNs, answered.** `overuse.objective` and `overuse.gate_g`: Forecasting is the author's fixed objective for
this slot and the client's most wanted; the mechanism under it is new to the corpus. `repeat.gate_g` against task4
v5: task4 forecasts each duty's energy from shipper-declared payloads whose recording errs; here nothing is
mis-recorded, and the forecast's credit is an intervention effect separated from a concurrent operator action.
`repeat.question_form` against task3 v5: a designation asks which, and the second sentence, deliverable set and
component roles differ.

**Data-native sentence.** Wealdmoor's control room armed its pre-planned 11 kV transfer schemes for exactly the event
windows its flexibility providers were scheduled for, at the two zones whose open point reaches a primary with evening
headroom (Ashcombe Road to Brindle Lane, Fenwick Street to Greaves Hill), so the SCADA demand that measures each
provider also carries a moved feeder section, and only the neighbouring primary's rise in the same half-hours shows it.

**The abstraction sentence** (what a reviewer holding this build beside its nearest would say is the same, domain nouns
stripped): "an intervention's measured effect at a unit includes load an operator moved from it to a neighbour in the
same hours, which the neighbour, the natural comparison, mirrors." No approved build on file says it. The nearest on
file: the client's Example 4 (controls improved because a shared floor's freed time went to them; the effect was
understated and the clean comparison was the untouched states), mark124 v1 to v3 (analogs' draw held down by the
organisation's own dispatch, the quantity needed for new units), task7 arch 4 (a borrower's failure removed through
payments between customers). Here the treated unit's own drop is inflated by a concurrent action, the comparison is
inflated by the same action in the other direction, and the credit is read where the two cancel.

**Same-puzzle and library tests.** Gap objective, decisive generator G4 and decision designation_set repeat no build
in the last twelve (`test.same_puzzle` and `test.same_driver` clear; G5 and G3 were tried first and collided with
task4 v4 and task5 v2). The library test: the stump sentence is not "use X on Y" with X a named correction; the field's
M&V baseline (weather-adjusted, with or without in-day adjustment or a neighbouring control) is the default path, and
the deep step is that every baseline route measures the primary, not the provider.

**Sources, one line each.** All files are constructed for task10 (no real dataset; external hosts are closed to this
session) and declared in `metadata.json` outside the ZIP. Spine: `primary_demand_halfhourly_2023-2026.csv`, the
Halverton zone's SCADA export (nine primaries, half-hourly MW and Mvar, UTC, October to March of three winters, point
names re-keyed in a May 2024 asset ID migration). Operating extracts: `flexibility_events_2024-2026.csv` (the zones'
dispatch log in UK local time, re-issued and cancelled events), `halverton_weather_hourly_2023-2026.csv` (the
reference station, UTC), `halverton_daily_mean_temperature_1991-2020.csv` (the station's long daily record).
Lookups and registers: `primary_substation_register.xlsx` (codes old and new, transformers, firm capacity, DFES
growth), `network_feeders_11kv.xlsx` (the 11 kV feeders each primary supplies, customers, normally-open points),
`load_growth_register_2026-27.xlsx` (accepted connections by feeder). Governing documents:
`capacity_assessment_guideline_2026.pdf` (the design condition, firm capacity, how flexibility is credited, the
commit rule), `flexibility_contract_awards_2027-28.pdf` (the 2027/28 awards, the service window and its scheduling
trigger, prices). Distractors (named only in `metadata.json`): `customer_interruptions_2025-26.xlsx` and
`duos_charging_statement_2027-28.pdf`.

## Tried and rejected


- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.
- Architecture 1 as a whole (2026-10-31, the batch 1 triage): the moderation pool's world, prompt and asks had been
  solved once on the portal and loop 3 kept them, so the slot is re-rooted in a new world with a new mechanism; the
  pool's leaving rate falling as fast leavers go first is spent for this slot.
- Re-root draw screens (2026-10-31), each rejected before any data was cut: a mixed-population flood frequency (spent
  in task273 and task130's notes); an event-driven trial's event count (task171 and task174 hold it); a dialysis
  cohort's eGFR slopes (a patient-level slope is the obvious route and the method forks); a vineyard's frost nights
  under inversions (dead in task170's notes); a health system's access change and a climate-extremes count (both
  measured dead in task174 and task170's notes); this slot's own frailty and tenure hazard (architecture 1).
- The first card probe for this draw carried `validated_decoy` true and Gap 1 first: BLOCKed on
  `two_layer.validated_decoy` (a closed record built to bless the wrong method) and on a structural signature spent in
  five builds. The design is drawn so the meter's own high-water-table storms and the overflow log refute one response
  per millimetre for anyone who checks them, and population (the meter's days are not the replay's) is the decisive gap.
- A June 2025 high river with storms in it (the spell centred in August): the meter logged three overflows in it that one
  response per millimetre misses, so the overflow log refuted the stop rung at the count level, a search signal; the spell
  now falls in a dry month of 2025 and the meter's logged overflows are dry-ground storms every rung reproduces.
- The spell's peak held below the replay's wettest days (12.6 km of sewer below the water table against 20): 812 replay
  days sat above anything the meter saw, so the deciding configuration was out of sample and the infiltration had to be
  extrapolated; the spell now reaches the replay's wettest days (one replay day above the meter's maximum).
- Pumps below the wet-winter base (92 to 100 L/s): the station spilled in dry weather on groundwater alone and the
  consent's 24-hour rule merged wet weeks into single long overflows, so more inflow could file fewer overflows and the
  count was not monotone in the flow; the pumps now sit above the wettest dry-weather peak and every overflow needs rain.
- Assumed unit hydrograph shapes and a crown or centreline reference for the submerged length: the replay spread 2.1 to
  5.0 a year, but only because those variants fit the meter two to three times worse; among fits within a few per cent of
  the best the figures agree inside the whole-number bin, so the figures are graded to whole overflows a year.
- Architecture 2 (the PS03 overflow replay with each day's own water table), returned FAILED_TO_STUMP on 2026-11-07:
  both responses landed the hold call. Response 1 replayed 2004 to 2023 and filed 48 overflows against the 40 the
  consent allows, then 2 after the upgrade; Response 2 filed the same hold. Any full-record replay with the subdivision
  already broke the consent, so the decisive step (each replay day's own water table) was never needed. Lesson: the easy
  route has to be the one strong solvers actually file, and it has to land on the wrong side; a count of rare
  exceedances spreads with every modelling choice, so the call now sits on a mean quantity whose naive family is tight.
- Judge round 1 (2026-11-07, FIX_NOW on the asks; the call forced, Gate G analytical_non_defect, Gate H pass). Ask A's
  window read literally dropped the platform councils' last run (a 2 July 2026 date in the period-end column): FP-04 now
  files the record's own convention (a pay period ends on a Sunday and is paid later that week; credited to the year it
  ends in), naming no platform and no weekday the advices carry. Ask B's unit was open (raw, per invitation and day, or
  per organiser, invitation and day): the asking sentence now files it (a visit two organisers made counts for both, a
  moved booking once as held). Both asks were scoped to the 30 councils the branch covers while the prompt read as the
  round: cut to the round's 24, the regional platform's twelve councils re-sited inside the round on the same pay
  cycles, so no in-round figure moved. Ask 1's turnout figures had no rounding and a refit evaluating members at the
  extract sat about 0.7 points under: the guide now files each member as they will stand when the ballot period closes
  and the tracker files that period (1 to 15 March 2027); whole-per-cent figures were not adopted because five councils
  sit within 0.05 of a half point (Corrigan Valley 62.53, Halston 59.53, Pellham 58.49, Rosedene 45.51, Underhill 40.54),
  so a worksite-effects refit (lift 1.027) can cross a rounding edge; the prompt asks only whether each council reaches
  half, the side being determinate under every refit. freeze.py: the main side unmoved; the twelve out-of-round ask
  figures and block 4's turnout percentages were dropped by the repair (allowed, this line).
- Hardening noted, not applied (the judge rated stump power moderate to good: a model that fits the delegate term lands
  the call): ship the 2026-28 term as the organising coordinator's separate July 2026 election return rather than a
  sheet of the delegate register, so the register a solver opens holds the terms the online votes cover and the new
  term sits in a file read for its own purpose; the call, the stump and every figure would stay frozen.
- Judge round 2 (2026-11-07): DETERMINISTIC, the call reproduced with 6 points either side and no respecification
  flipping a council, stump power moderate to high. Before ship: step 8 reworded (the golden keeps the later, last
  updated row of a moved booking); the xlsx inputs' creator and last-modified-by set to the branch, the body that
  issues them; the 2021 declarations given the Producer of the LibreOffice release current at their June 2021 export
  (7.1; the info dictionary is the last object, so startxref moves and every object offset is asserted unchanged), the
  other four PDFs dated after 24.2's February 2024 release; and the hardening above applied: the 2026-28 term now ships
  as `delegate_election_return_2026.xlsx`, the returning officer's return, and `delegate_register_2018-2026.xlsx` holds
  the terms to 2024-26. No graded figure moved (freeze.py); the input gates hold (17 files).
- Surface at ship promoted three pairs on card axes alone: task157 (back to back, the same domain and objective; a
  petition sample's pair defects, not a turnout forecast, differentiated on the card), task154 (the calibration form
  realised_outcome_roster repeated two builds apart: redrawn to counterparty_acknowledgement, the agent's declared
  results being a counterparty's record) and task265 (left truncation in a descriptive survival estimate,
  differentiated on the card); heart PASS; left for the author's adjudicated clone check.
- Architecture 3 (the union branch's protected action ballots, each member read with the delegate in post at the
  ballot): FAILED_TO_STUMP on the portal 2026-11-07, both responses on the golden 11 councils. Both put worksite
  delegate coverage in the turnout model from the start and evaluated it at the ballot close with the 2026-28
  delegates, so the decisive step was the forecaster's reflex (a recorded covariate's forward value), and the July
  2026 election return, read by nothing else, announced it. Re-rooted to architecture 4 in a new domain and world.
- Architecture 4 draw screens (2026-11-08), each rejected before any card or data: vacancy chains through a
  fixed-post hierarchy (dead in task174's and task137's notes, and a stock-and-flow check of posts finds it); a
  programme's lead-in audience (task115 and task174); one facility's overflow into a sibling removed by an expansion
  (task308's reader named railheading and the full car park's hidden demand, and the swap reads the same for wards
  or car parks); ward acquisitions per colonised patient-day (task181: infection prevention's own reflex); errors
  per interruption or per handover (task198 and task173); wear accrued only in hours inside a band after a duty
  change, and pump failures per start after a control change (task307's driver); admissions that rise with spare
  beds (a filed bed opening prompts the question, and the forecast needs a fixed point whose estimator forks);
  speculative double bookings (the hygiene battery's de-duplication reaches it and the identity match is Layer 1);
  bus headways under a denser timetable (task308's probe replayed the operation and carried every knock-on).
- First prototype of this draw (hangs on days since power-up, any site-wide power-down a reset): the parameters put
  every hub below 99 per cent; the legacy cabinet repairs now isolate the hub every few weeks, hangs start only after
  about 75 days, and the high-power units sit near 99.5 per cent on the record.
- Hang restarts isolating the whole hub: the units then restart one another and the programme hubs stay above 99 per
  cent; a hung unit is restarted at its own breaker, and only the legacy unit's cabinet repairs, planned visits and
  supply interruptions restart the whole hub.
- Three hubs whose legacy units rarely needed the cabinet opened, failing on both routes: the hubs' legacy repair
  counts then predict the high-power hangs across hubs, and a hub covariate (legacy units at the hub, or their
  repairs) would extrapolate to the golden, architecture 3's failure again; every hub now has exactly one legacy unit
  with cabinet repairs of 10 to 12.5 a year, and the hubs that fail on both routes are three coastal hubs whose
  high-power units suffer ordinary corrosion faults.
- The learner given the hub's legacy jobs in the last 60 days, the days since its last legacy job or the days since
  its last planned visit (prototype, clean truth): none reaches the golden; at the programme hubs they carry 0.7, a
  noisy 0 to 1.4 and 0.4 to 0.7 hangs a unit-year against about 3.3, so each files the default path's set.
- Prototype 7 (the RC50's cabinet repairs at random, 10 to 12.5 a year, every unit at a hub on one pillar): the
  hub-year count of the RC50's work orders predicts the HX150 hangs (z of minus 4.8), and the Poisson model carried at
  the programme's zero files the golden plus a rural spur hub; the count of pillar power-downs files the golden
  exactly. A covariate's forward value lands the call, architecture 3's failure again.
- Prototype 8 (motorway visits two-monthly only from April 2024, rural spurs at 4.5 interruptions a year): the
  full-covariate model filed the naive set with programme hubs 0.01 to 0.3 from 99, a coin flip per hub over redraws.
- Prototype 9 (the coastal hubs' HX150 units on their own pillar, the RC50's repairs still random): the model on the
  RC50's work orders alone still filed the golden exactly; the random repairs carry the signal however the pillars sit.
- Prototype 10, adopted: the RC50's cabinet service is monthly, so its work orders a year carry no hang signal (z of
  0.3) and the HX150 units on its pillar never run 75 days; the hubs whose HX150 units sit on a pillar of their own
  carry every hang on record. Two inland hubs share that arrangement with the three coastal ones, because a record in
  which only coastal units ever ran long could not tell the sea air from the uptime (the deciding configuration has to
  be on record off the coast).
- Ask screens refused: double counting on a meter shared by two connectors (a billing defect a real operator fixes, so
  planted); tariff re-rate copies with new session IDs (a near-duplicate the battery's de-duplication reaches); a hub
  code renumbering (the battery re-derives the code from the charge point); meter replacements to break a register
  shortcut for Ask B (each needs a work order in a main-call file, an ask organ there), so a solver who takes each
  unit's register advance over the window keeps Ask B.
- The first cut's register opened on its Charge points sheet: leak.py sweep 12 read the first two rows' cells (the
  units' IDs, makes and models, which the programme names) as column names and called the programme a dictionary
  (LEAK); the register now opens on its Hubs sheet, the order an asset team keeps it in, and no figure moved.
- The full-covariate model before the RC50's work rose with the coast (the RC50's repairs as random at every hub): it
  filed 11 of the 12 on the clean truth, because the hang hubs' RC50 jobs ran low by chance and the zero at the
  programme hubs extrapolated far below the record; the RC50s at the five own-pillar hubs now need about twice the
  repairs (the coastal units' corrosion, the inland pair's 2017 units), so its removal lowers that model's forecast.
- Stage 4 round 1 (2026-11-08, on 4bf9959c): the judge DETERMINISTIC (APPROVE), the leak reader clean on questions 1
  to 6 with one mild item (every HX150 freeze call-out on record at the five own-pillar hubs, read as placed). Worked
  in one generator pass, the lines below; the call, the stump and the twelve hubs unchanged.
- RC50 outages awaiting Tavrin parts in 2026, to give the shared-pillar units some long uptimes (a module on order for
  weeks, the RC50 out of service and its pillar live): the outage months carried a signal the full-covariate model
  read, and it filed 12 hubs with seven standard programme hubs among them; the outage path is empty, and the shared
  units' occasional long uptimes come from the RC50's inspection-only months (one in five, the cabinet not opened)
  and skipped services instead.
- RC50 cabinet repairs cut to 1.0 a year at the shared-pillar hubs (fewer isolations, more shared hangs on record):
  the shared units then hung often enough at a thirteenth hub to list it; the repairs stay at 3.5 a year there and
  6.8 at the five own-pillar hubs.
- The five own-pillar hubs' HX150 units commissioned in 2022 and 2023 like much of the fleet: the full-covariate model
  read the commissioning year (the hang hubs' units among the newest) and carried it to the programme's new units,
  filing standard programme hubs; their units are now commissioned in 2021.
- Callout attendance read from each Faulted spell's length: the RC50's long repair spells inflated it at the shared
  hubs and the verifier's own forecast sat 0.05 points from 99; attendance is read from the work orders (attended less
  logged) over every callout, in the golden and the verifier alike.
- The day-step members of the standing family counted a hang's first day whole and released it a day late (about a day
  of downtime too many a hang): they sat up to 0.7 points under the simulation (Annagh Cross 99.05 against 99.30), the
  verifier's copy too; both now count the part of each day a hang is down, from a hang at mid-day on average, and agree
  with the simulation within about 0.15.
- Ordinary faults at about 0.4 a unit-year everywhere, the standard hubs' callouts at 2.3 days, the rural spurs at 7.4
  and 7.9 interruptions a year and comms faults at 0.15 a unit-year: the hubs outside the list sat 0.22 to 0.4 points
  above 99 on the golden, two of 20 redraws filed another set, the rate route's back-tests drifted past half a point,
  and the standard hubs' 2026 faults at that attendance put four of them under 99 in the January to October 2026
  record, so carrying 2026 held four of the seven; faults now run about a quarter a unit-year outside the coast, the
  standard hubs' callouts about 2.05 days, the spurs about nine interruptions a year and comms faults a tenth a
  unit-year, every hub's true side at least 0.48 points from 99.
- The five own-pillar hubs at 3.4 to 4.1 charges a day (the quietest after the spurs): the full-covariate model leaned
  on charges a day and the hub's unit count (the standard hubs gain a unit in 2027) and filed 13 hubs, ten of the
  golden's; the five now take 4.8 to 5.6 charges a day, inside the standard hubs' range, and the model files 3.
- A rate-route back-test bound of 0.4 points: with comms repairs and faults at their real scatter a unit-year's own
  noise is about 0.4 points, so the bound is half a point with 85 per cent of units on their side, and the back-test
  prediction now carries the comms repairs' downtime as the rate route does.
- Load bank tests of about 55 kWh a connector with session drops of up to 18 minutes two and a half times a day: a
  column total (the gaps out, the tests in) cancelled to the golden figure at three hubs; tests now run about a
  quarter of an hour (30 to 40 kWh), drops three times a day for 6 to 15 minutes (inside the three missed heartbeats
  that write Offline), and the generator's clearance holds the gaps and the tests at least 0.16 MWh apart at every hub,
  the tests across a rounding step and no hub's charges on a round hundred.
- Work orders written from six to nine fixed sentences a job kind (one repeated 118 times) and planned jobs attended a
  whole number of days after logging: each write-up is now composed from the job's parts in its technician's habits
  (2,465 distinct over 3,546 jobs, none more than 9 times), planned jobs are logged at the planner's minute and
  attended at the technician's, and the parser's reading of every job's kind from its words is asserted against the
  truth.
- The plan's addressee typed rather than drawn (Bronagh Allis): now Ailis Fee from `guard.py names --geo ireland
  --seed 156`, the schedules signed by Darcy McGlinchey and Domhnall Linehan from the same draw.
- The prompt's question as "Which of our hubs will have..." (the which shell at 32 per cent of the prompts on file, and
  task482's form), then "Where will we have..." (the voice check and the heart read "will we" as whether): it now asks
  "Where in our network will a high-power charge point fall below...", read as where by both.
- "No forecast within 0.3 of 99" (the first hand-off's SF4 and closure line) was not what the build measured (0.21 to
  0.25 then): both now quote the measured margin, asserted at 0.2 or more.
- CRITICAL_COMPONENTS 1's hang count (84, which the judge read as 83 with a power-up before it on record and 90 in
  all): dropped, the onset day kept with its definition.
- The surface screen on the cached corpus (127 builds, 0 promoted at the first hand-off): the full re-extract screens
  314 and promotes 9 pairs on card axes or surface percentile, each differentiated on the card.
- The planned maintenance schedule writing 08:30 to 14:30 on every row while the world's visits ran in each
  contractor's own windows (the first fix pass varied the windows in the world, not in the schedule): the schedule now
  carries each hub's window for each year (motorway hubs early, rural spurs late, town centres before the shops open,
  moving with each year's plan), and Schedule 4's exclusions, the golden's and the verifier's, are read from it.
- Stage 4 round 2 (2026-11-08, on 3a6e329b): the leak reader clean, the judge DETERMINISTIC (APPROVE, no FIX_NOW). The
  ship pass worked the coordinator's fixes 1 to 7 in one generator pass; the call, the stump, the ladder and the default
  path unchanged. freeze.py's --allow, with its reasons: charges.Annagh Cross, energy_mwh.Annagh Cross,
  charges.Cloonfin Crossroads and energy_mwh.Cloonfin Crossroads (the spurs' interruption record raised by half, fix 5,
  which re-draws their 2026 sessions: 1738 to 1786 charges and 57.3 to 57.5 MWh, 2545 to 2507 and 81.9 to 81.0);
  pack.status_rows (the export cut at 31 October 24:00 and the spurs' extra power-downs), pack.dso_rows (the spurs'
  extra interruptions), pack.session_rows, pack.resent and pack.resent_hubs (the session numbering moves with the
  spurs' sessions, so the export's September re-sent page falls on other hubs; no other hub's records change),
  pack.wo_a and pack.wo_b (planned jobs raised by each contractor's own practice, the jobs open at the save, the spurs'
  callouts) and salt.NM125 (the clearance re-drew Annagh Cross's sessions once more).
- The status history ran past its stated coverage (rows to 8 November, from intervals that ended after 31 October) and
  the work orders held jobs attended and closed after the workbook's save: each export now ends at its own moment, a job
  raised before the save and not yet attended or closed stands open, and a spell still Offline when the record ends is
  censored rather than read as a hang (the golden and the verifier alike). The schedule's visits on 30 and 31 October
  stood Completed in a workbook saved on 29 October; a visit is Completed now only once its window closed before the save.
- Planned jobs raised 3 to 20 or 6 to 30 days ahead by both contractors (the same ceilings in two systems): Lissane's
  technician booked the next RC50 job on leaving the last one and its planner raised site visits in a batch the month
  before; Corran raises a site visit on the day the operator notifies the partnership and an RC50 job a fortnight ahead,
  about one in six then moved; the operator's notice runs from a fortnight to about six weeks. The jobs' write-ups are
  drawn in the order they always were, so every write-up outside the spurs' callouts stands as it did.
- The spurs at 7.3 and 9.4 interruptions a year: their lowest unit sat at 99.31 and 99.47 on the golden and 99.15 on the
  judge's own simulation, their expected lowest unit at 98.9 to 99.05 and their event probability at 0.41 to 0.48. The
  long rural overhead spurs now carry 42 and 54 interruptions on the record (about 11 and 14 a year): the extra faults
  are drawn on a stream of their own, so every other hub keeps its record, its sessions and its jobs (the spurs' old
  draws replayed where other hubs share a stream).
- The spurs' extra faults first drawn as a Poisson stream (4.6 and 4.9 a year): its draw moved the smoothed route to 9
  hubs (Cloonfin Crossroads in) and the rate route's back-tests to 0.42 and 0.43, figures the frozen ladder and default
  path state; the record now holds a stated count (14 and 18 beyond the base), and the stream is chosen, as the
  clearance chooses the asks' salts, so that the re-drawn spur record leaves every cheap route's set and the back-tests
  as they stand.
- The programme's document control table split across its page break (heading on page 1, rows on page 2): kept with its
  heading on page 2; no word changed.
- The PDFs' Creator (fix 4, optional): left as Writer. officepdf renders every document through LibreOffice Writer, so
  any other Creator would be contradicted by the file's own structure.
- The expected lowest unit, the event reading, each unit's own fault rate and a Weibull onset (the judge's optional
  items): asserted as SF17 to SF20, each on the same 12; the Weibull's fit is worse than the fitted onset's by 27.5 AIC.
- The RC50's 2027 isolations drawn as a Poisson stream at the hubs where it stays: they forecast 0.05 to 0.53 hangs a
  unit-year there against 0.00 to 0.39 on the record, which thins those hubs' expected-lowest-unit margins (Eskerbrook
  Shopping Centre at 99.07); drawn from the record's own calendar the member lists the same 12 at 99.23 and 0.32 at
  worst, measured and asserted, and the golden keeps the Poisson draw (no golden change).

- Architecture 4, the rapid-charging operator's 2027 availability plan (2026-11-08, platform round 1, target.zip
  5356713d): both runs landed the golden 12 hubs (the author reports not stumped; no rubric). Both read the hang ages
  off the first histogram (no hang before day 76 after a power-up), fitted a censored hazard on time since restart with
  the work orders' power cycles as the remedy, simulated the renewed network and back-tested on 2026: a mechanism the
  rows carry in one plot, with its remedy written in the work orders, was modelled on sight. Its asks fell (93,640 and
  94,297 charges against the golden's 90,612) but the platform rules a landed call before grading. World spent.
- Architecture 5 draw, a heat pump conversion programme's second phase forecast from homes that under-heated on gas and
  will heat fully on a heat pump (each home's uplift conditioned on its own pre-conversion balance point): rejected at
  the draw, because it is task3 architecture 1's driver in other nouns (the gain an upgrade adds conditioned on how much
  of each unit the old level already served), which one of that build's runs landed by regressing each earlier unit's
  gain on its own prior coverage; conditioning a carried gain on a covariate each unit's history prints is a reflex.
- Architecture 5 draw, a pilot of hybrid heat pumps whose gas backup flattened the cold-day electrical load carried to
  an all-electric second phase: rejected at the draw on the one-fact test (the pilot's units are hybrids), and the
  backup's discovery would be finding a population fact rather than analysing.
- Architecture 5 draw, stations whose winter peak responds in opposite directions to the gas-to-electricity price ratio
  (hybrids switching fuel, all-electric homes economising) carried to the 2027 energy tax shift: rejected at the draw,
  because a per-station forecast is the natural default, so each station's own slope is a reflex there (the grouping
  dichotomy), and the decision weights no population mix.
- Architecture 5 draw, measurement error in the heat pump count by substation (postcode allocation) attenuating the per
  heat pump coefficient: rejected at the draw, task4 architecture 5 carries an errors-in-variables driver in flight.
- Architecture 5 draw, phase imbalance (single-phase heat pumps landing on one phase, the transformer's per-phase limit
  binding first): rejected at the draw, because per-phase columns invite the per-phase reading and the installers'
  allocation is readable off the first phase's increments.
- Architecture 5 draw, latent excavation damage behind a spike in cable faults read as ageing: rejected at the draw, an
  activity elsewhere, linked by place and time, driving failures repeats architecture 4's family in this slot.
- Architecture 5 draw, export from PV-saturated feeders censored by inverter overvoltage trips: rejected at the draw, a
  trip is not a clean cap, and the capped-quantity family is crowded on this repository's cards (mark124, mark162,
  task4 architecture 2).
- Architecture 5 prototype, the partners' own design-day demand reconstructed by removing the moved sections as the
  deciding step: kept off the call, because removing a moved load from a series is cleaning; the partners' flags hold
  under every route by margin and the moved sections decide only their ask figures, while the call moves on what
  the credited flexibility is.
- Architecture 5 prototype, an unadjusted customer baseline (the mean of the ten previous non-event weekdays): measured
  0.33, minus 0.38 and 0.25 per megawatt scheduled at the three zones, its cold-day bias cancelling part of the moved
  section at one zone and turning another negative; it files a fourth primary (Charlecote Way) and misses, and its
  negative zone sends a run to the weather-adjusted baseline, which carries the whole moved section.
