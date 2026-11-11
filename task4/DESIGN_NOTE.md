# task4: which weeks of the 2027 peak Saarnela's two small-parts zones need the evening shift, and how many agency picker hours to book for each peak week, once Huippu Sport's orders share those zones with Kotikaari's

## Draw

Subdomain: Regression, classification & model diagnostics (General Statistics & Data Science; house domain Supply Chain & Logistics, an e-commerce fulfilment centre's peak labour plan)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A schedule under capacity (for each small-parts zone and each peak week of 2027, whether the day shifts at the zone's limit of pickers on the floor can pick the week's lines or the evening shift opens, with each zone's paid picker hours and 80 per cent range and the agency hours booked on top of the own pickers each week)
Weight: modeling: the time a line takes on the 2027 floor (a time per line by handling class and units with an aisle-congestion term that the peak's lighter lines hide, and the new brand at its own assortment), where the last three live builds weighed allocation (task9), measurement (task16) and modeling's neighbour validation (task17's distribution); the volume side (the forecaster's calibration and the calendar re-key) is forecasting work beside it
Data-native sentence: the WMS logs each zone's hour with its pickers, task minutes and lines by handling class, so a time per line is measurable only at the zone-hour grain, where the morning e-commerce wave packs the aisles with the lightest lines and the afternoon store replenishment thins them with the heaviest, while the client's forecasts come as weekly vintages keyed to week numbers and the new brand's lines exist only as a pilot of its lightest articles and an order history from another warehouse
People: Helena Korhonen, Telkkä's operations director, who signs the 2027 peak plan, the agency booking and the evening-shift agreement (the golden workbook and memo are hers); Tapio Nieminen, the Saarnela site manager, author of the draft peak plan; Tarja Huhtala, Kotikaari Oy's demand planning manager, who issues the forecasts; Marko Autio, Saarnela's continuous improvement engineer, who ran the Huippu Sport pilot

Architecture 11, 2026-11-11, a new world after architecture 10 (the Niittylä bus order) was landed by both platform runs (`runs/arch10/`, triage REDESIGN): each judgment it priced was one recognition followed by a routine fit (a quantity asked beside the forecast used as its predictor, a logged outage read as the natural experiment, a metered total split by one regression). Five architectures (6 to 10) counted vehicles for duties under an energy limit and a night supply and every one was landed or returned, so the scaffold is left with the world: a new decision form (a schedule of evening shifts by zone and week with the weekly agency booking), new deciding lessons (congestion past a density, a pilot's selected assortment, a forecaster's claim-dependent optimism, a week-numbered profile after a 53-week year) and a new shell.

## Deep reasoning

Task type: Regression, classification & model diagnostics, serving Forecasting & Predictive Modeling: each 2027 peak week's paid picker hours by pick zone, through a time-per-line regression and a calibrated volume forecast, with the evening-shift weeks and the agency booking read off them
Domain test: the results are regression and model-diagnostic objects: an omitted density term whose effect a correlated mix masks at every grain but the mix-adjusted zone-hour fit; a model chosen on a check that can see the 2027 condition rather than the draft's back-test, which confirms the proportional rate; a covariate-shift correction from a pilot sample selected on handling class to the brand's full peak mix; a forecaster's calibration conditioned on its own stated claim and measured at the lead the plan is made at; a seasonal profile re-keyed from a calendar grid to the dates of the events; the 80 per cent range built from the calibrated forecast's error at that lead
Swap: "which weeks the clinic needs an evening session and how many locum hours to book, now that a second practice's patients share its rooms" keeps a forecast of workload, but the aisle density per picker, the handling classes, the forecast vintages keyed to ISO weeks, the 53-week year and the zone's limit of pickers on the floor stop making sense
Where the weight sits: R3 and R7: the time a line takes needs the zone-hour log's task minutes regressed on lines by handling class, units and pickers per aisle together, because the morning wave's light lines and the afternoon replenishment's heavy ones cancel the congestion in every raw view, and the 2027 hours then need that rate at each zone's limit and at the evening's density, week by week
Layer 1: the payroll system changed in January 2024 (semicolon export with decimal commas before, comma export after); floating pickers' timesheet rows carry zone FLEX and are split only by their WMS log; agency badges were re-issued in April 2025 and the roster keeps the crosswalk; the WMS re-ran its nightly export on several dates so some zone-hours appear twice; forecast vintages are re-issued mid-month with revised rows; the pilot's scanners confirmed some picks twice; the old warehouse's order history uses Huippu's own article numbers, crosswalked in the item master; none decides a result
Not one thing: four independent judgments each move the hours and the evening-shift cells (congestion; the pilot's mix; the forecaster's claim-dependent optimism; the calendar re-key), two of them move the volume and two the time per line, in opposite directions, and each is graded on its own figure; any one put right with the others left as the careful pass leaves them lands a different set of evening-shift weeks
One-fact test: the strongest single sentence ("time per line rises with pickers per aisle once the handling-class mix is held fixed") rescues R3 alone; the weekly hours, the agency hours and the evening-shift cells still carry the pilot's mix, the pooled overstatement and the week-late profile
Not semantics: every field read right (the zone-hour log's minutes and classes, the timesheets' paid hours and absence codes, the vintages' issue dates and week keys, the pilot's pick confirmations, the item master's classes) still leaves each priced result to estimation: no field holds a congestion term, a full-mix time per line, a calibration or a date-keyed profile
Not rule application: the planning standard files the WHAT (the peak weeks, paid picker hours, the zones' limits of pickers on the floor, the evening-shift rule on the day shifts' capacity at the limit, the range's coverage, the own pickers' availability); no filed procedure computes a time per line, a congestion term, a calibration or a profile
Estimand: the planning standard 2.1 to 2.4, 3.2 to 3.5 and 4.1 to 4.2 with the prompt: population each pick zone's lines in ISO weeks 46 to 51 of 2027, both brands, members not yet observed; outcome paid picker hours as the timesheet records them, the evening-shift verdict by small-parts zone, agency hours by week; the overstatement over the year-ahead (October) vintages' peak weeks of 2022 to 2025 against picked lines, ratio of totals; the extra minutes a Huippu Sport line takes over a Kotikaari line in the small-parts zones in those weeks
No decoy: the draft peak plan reproduces exactly by its own method (the 2025 peak's paid hours per line carried to the 2027 forecast) and answers a shallower quantity, the hours at 2025's floor; the pilot review states the pilot's own times correctly; neither states an evening-shift verdict, and no file argues for one
No replay: no result re-derives a published figure and no stated number in the pack is wrong
Strategy label: own (congestion past a density masked by a correlated mix, beside a selected pilot reweighted to its population, a claim-dependent forecaster calibration and a calendar re-key)
Depth level: 5. Four independent judgments each move the evening-shift cells and the hours, two raising the hours (congestion, the full Huippu mix) and two lowering or moving them (the claim-dependent overstatement, the date-keyed profile), so the careful pass and each single correction land different sets of weeks
Lesson: a rate measured on a floor with fewer workers holds only below the density the forward plan needs, and the record shows it only once the mix that moves with density is held fixed; a pilot measures the articles it carried, not the brand; a forecaster's error is a function of what it claims; a profile keyed to week numbers is a week late after a 53-week year

## Results chain

Drawn 2026-11-11; bands, figures and the effort table are measured at stage 3 on the cut pack.

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the 2025 peak's paid picker hours by pick zone, floaters split by their WMS log | assembly and reconciliation | standard 2.2; the two payroll exports over the WMS log | measured | earned (the hygiene battery) | - | Component |
| R2 | the share by which Kotikaari's year-ahead peak forecasts overstated the lines picked, 2022 to 2025 | missingness and measurement | the vintages' October issues against the WMS lines, ratio of totals over weeks 46 to 51 | measured | earned | independent: the vintages and the WMS lines | Ask |
| R3 | the aisle-congestion term: minutes a line at two pickers an aisle over an empty floor, the mix held fixed | modeling | the zone-hour log regressed on lines by class, units and pickers per aisle | measured | method shortcut: the mix fitted without density, or the 2025 peak's rate carried | independent: the zone-hour log | Component |
| R4 | how many more minutes a Huippu Sport line takes than a Kotikaari one in the small-parts zones in the 2027 peak | modeling | the class and unit rates from the pilot lines and the zone-hour log, at each brand's peak mix from the order history and the item master | measured | method shortcut: the pilot's own mix | independent: the pilot, the order history, the item master | Ask |
| R5 | the overstatement the 2027 forecasts carry, by brand and zone group, from the growth each plans | validation | the October vintages' errors against their stated planned growth | measured | method shortcut: the pooled share applied to the largest planned growth on record | independent: the vintages | Component |
| R6 | the 2027 weekly profile re-keyed from the forecast's week numbers to the dates of Black Friday and the Christmas cut-offs | forecasting | the 2022 year-ahead vintage (also copied across a 53-week year) and the daily lines | measured | dismissed own evidence: the client's week-numbered profile kept | independent: the vintages and the daily lines | Component |
| R7 | each pick zone's paid picker hours for weeks 46 to 51 of 2027 | forecasting | standard 2.1 to 2.4, 3.2 to 3.4 | measured | unfinished chain | R3 to R6 | Ask |
| R8 | the 80 per cent range on each of them | uncertainty | standard 3.5 | measured | earned in form | R7 | Ask |
| R9 | the weeks each small-parts zone needs the evening shift | synthesis | standard 3.4 | exact | unfinished chain | R3 to R7 | Recommendation, Ask |
| R10 | the agency hours to book each week | synthesis | standard 4.1 and 4.2 | measured | unfinished chain | R7, R9 | Ask |

Carry-forward: R1 to R6 stand on their own inputs; R7, R9 and R10 fall with any of R3 to R6, so a run that puts one of them right and leaves the others still lands a different set of weeks.

## Tried and rejected

- 2026-11-11, architecture 10 (the Niittylä order, landed by both platform runs, `runs/arch10/`): every graded figure inside its band on both runs (order 17 exact); the diesel bridge was the obvious join once the prompt asked each block's diesel figure beside its energy, the heater-out days were read as the record of all-electric heating, and the charging split was one regression on the sessions. The world and its scaffold (a count of vehicles for duties under an energy limit and a night supply, architectures 5 to 10) are left together.

- 2026-11-10, architecture 10 stage 4, the first judge pass (FIX_NOW): a rank list in component 1 that depended on
  which blocks count as short (out of the blocks; the component states the means and the gap); the 19th block's kWh
  shortfall, whose magnitude depended on the plug-in margins assumed (out of the blocks; the windows are now the
  standard's words, each block's return to its departure inside the night period, the supply rescanned for
  balanced margins under them); M111 within the 10 kWh grading tolerance of the limit (every block now 26 kWh clear in
  the truth and 18 in the golden). The reader's figure 20 (outlets, the quotation's range) moved apart (26 outlets, four to thirty buses).
- 2026-11-10, architecture 10 stage 4, the second judge pass (DETERMINISTIC, one item owed): the heaters' band edges
  propagated to the cut, now asserted (SF27, both bands' edges land the same 18 and the same verdicts, the band half a
  kW either side of the golden); the re-read's realism line (a session starting under zero state of charge): the
  pilot's blocks, stand-ins and weekend blocks now pass the planner's own range check (the pilot buses' 480 kWh as the
  quoted model's), the boosters on a heater-out day capped at 12 kW, no electric day ends under 15 per cent; the
  stand-ins are the next three on the planner's list, so the pilot's record reaches no hard block; the heater fit
  leaves the heater-out days' hours out of its intervals.
- 2026-11-10, architecture 10 stage 3, the night's energy for the recommended buses as ask 5: every route capped by the
  night lands near the capacity's energy (the careful pass's 21 lighter buses sum to the golden's 18), so the figure
  graded nothing; replaced by the night demand of every qualifying block (8.7 MWh against 13.0 on the careful pass).
- 2026-11-10, architecture 10 stage 3, the telematics days uploaded twice in March 2026 (cold days): kept, they halve
  the heater fit's slope through the degree-days without litres and move every energy 7 to 11 kWh; the portal's outage
  moved to May, where the duplicates touch nothing (SF6 asserted within 8 kWh).
- 2026-11-10, architecture 10 stage 3, electric stand-ins on any short weekday block: 37 stand-in days spread over 30
  blocks gave almost every qualifying block its own electric days and the hurried fit nothing to miss; the dispatcher
  now keeps three approved stand-in blocks, so the bridge reaches the hard blocks through them and the weekend blocks
  while the pilot's covariate fit stays light on the 39 blocks it never ran.
- 2026-11-10, architecture 10 stage 3, the pilot's energy model with a per-hour auxiliary term beside block effects:
  kilometres and hours are collinear within a block, the term was unidentified (15.7 kW against 2.2) and every block
  effect biased; the per-km rate by block now carries the auxiliaries, and the diesel rate carries the idle draw the
  same way, so the bridge is one line.
- 2026-11-10, architecture 10 stage 3, charging allowed from the bus's return: the night's windows summed to 17 hours
  and no realistic supply bound the order; the connection agreement's night period (21:00 to 07:00, the load-control
  relay) is the operating arrangement, and the supply scanned at 5 kW steps for balanced margins (700 kW under the exact windows: the 18 hold
  3 per cent up, the 19th fits only 2 per cent down, 10 or 20 minute plug-in margins cut at the same 18, and the heaters'
  band edges leave the 18).
- 2026-11-10, architecture 10 stage 3, the pilot blocks as the thriftiest of all 48: the planner also needs the range,
  so the pick was from the blocks of 225 km or less, and the pilot sits at ranks 11 to 23 of the 48; the component
  states the gap and the ranks among the short blocks as computed.
- 2026-11-10, architecture 10 stage 2, the cold-day selection (the planner keeping the electric buses in on the
  coldest days) as the heating judgment: with fuel heaters the pilot has no range problem on cold days, and a handful
  of cold days the forecast missed would be outliers one residual plot shows; replaced by the heaters' share, which
  sits on every winter day and in a file the runs dismiss.
- 2026-11-10, architecture 10 stage 2, a 2027 timetable that re-cuts the blocks (line-level difficulty decomposed from
  the 2026 blocks): a second attribution the task did not need and a re-keying a solver would read as a trap; the 2027
  blocks are the 2026 autumn timetable's.
- 2026-11-10, architecture 9 (the calibration's transfer to the pilot's part loads, the early-life loss, the winter
  speed, in the Fryele world): both platform runs landed the golden exactly (`runs/arch9/`): run 1 by per-shipper
  calibration carried to each duty's own declarations, a square-root age form and a separate winter driving-time
  model; run 2 by the same with a declaration regime split found from the error itself. Each estimate the design
  priced as a step the runs had named and not taken was a mechanism one file's plot or one join carried. The world is
  left after five architectures; the lesson (what beats these runs is evidence in a file they dismiss, a structure
  across files nothing names, a count over many units, and selection into the training record) is this
  architecture's design.

- 2026-11-10, stage 4 re-judge, a stronger early-life loss so the straight-line loss flips a duty on its own (early
  loss 4.0 to 5.0 per cent over 0.18 to 0.30 years): the limit gap reached only 11.7 to 12.5 kWh against margins of
  10 or more, the curved forms spread 4.2 to 7.0 per cent, and the change would move graded figures after the one
  re-judge; not built. The -5 C speed ratio left the graded components instead (the re-judge thread put it within a
  careful run's reach), every figure unmoved.

- 2026-11-10, stage 4, the combination's tare and the drops as a graded component (R4 at first): the judge flagged it
  as earned by reflex and its isolated thread put a careful pass at 50 to 62 per cent on a grid that counted it
  twice; cut from the graded chain (kept in the model and the workbook), the verdicts' partial credit raised to
  three quarters of the duties; the careful pass 26.8 to 20.8, its design-day-speed variant 46.5 to 42.5.

- 2026-11-10, architecture 8 (three register joins beside the winter speed: the combination's tare by trailer, a
  multi-drop load taken off at its stops, ePTO fridge units drawing by the hour): both platform runs landed the golden
  exactly (order 7; payload 2.24 and 2.23, loss 3.78 and 3.79, every energy within about 3 kWh; `runs/arch8/`). Each
  join was to a register the runs already read, the new export, sheet and quotation line announced the steps, and the
  hourly fridge term made both runs time the design day, which is the winter speed. The judge's warning that the
  careful pass would earn 4 to 5 of 8 was recorded as a caveat instead of a blocker. Re-rooted as architecture 9: the
  fridge draw removed, the work moved into what the runs named and did not test.
- 2026-11-10, stage 2, the declaration practice differing by depot for the same shipper, read from an axle-load or
  gross-weight column in the daily summary: the summary carries no such column, and adding one would be a column that
  exists for the step; replaced by the pilot's part loads, which the pack already shows through each duty's own notes.
- 2026-11-10, stage 2, a battery-management or SOC-window update partway through, tractor by tractor: a timing break
  one residual plot per tractor shows and one indicator fixes (the client's shallow hidden factor, and this note's own
  earlier rejection of a drive-software update); replaced by the early-life loss, a form chosen by fit across every
  tractor.
- 2026-11-10, stage 2, the trailer body's air drag as the between-duty confounder of the payload slope (dense loads on
  low bodies): the tipper and the inloader have no pilot twin, so their drag would be a fork, and a flatbed's drag
  against a box is not physically one-signed; dropped.
- 2026-11-10, stage 2 pricing, the pilot duties at 80 to 93 per cent of the terminal's loads with drag 0.060: the
  careful pass's light-duty flips cleared its own limit by under 2 kWh; at 74 to 90 per cent, drag 0.066 and the
  winter fall 0.0125 a degree they clear it by 5 kWh or more.

- 2026-11-09, architecture 7 (the speed transfer as the deciding step beside the three reflex steps): both platform runs
  (`runs/arch7/run1.md`, `run2.md`, summaries) earned the payload term (1.98, 1.97), the loss (3.75), the cold curve and
  12 of 14 energies, fitted squared routing-tool speed (the year's ratio absorbed) and ordered 5, V14 out at 444.4 and
  443.0 kWh against the 442 kWh limit (golden 435.4). One duty, one judgment, 1 to 3 kWh: a thin level 3, and the
  graded 10 kWh band held both verdicts on V14; run 2 offered the golden's answer as a defensible alternative. Re-rooted
  as architecture 8: three more covariates the pilot's own rows do not show (the combination's tare by trailer, the
  tonne-km of a multi-drop load, the ePTO fridge units), each flipping two duties of its own, and no duty within 13 kWh.
- 2026-11-09, stage 2 pricing, the trailer pools one kind per pilot duty: the tare term (1.6) and the payload term (2.4)
  were confounded between duties and one shared coefficient gave 2.0, a 0.4 spread on R1; mixed pools (a mega on a box
  duty, a forklift on half the building-materials flatbeds) identify the tare within duty and bring the spread to 0.2.
- 2026-11-09, stage 2 pricing, the fridge unit at 3.4 kW: "every reefer draws" moved V33 13 kWh, no flip at a 13 kWh
  margin; at 4.4 kW it flips V30 and V33 clear of the limit.
- 2026-11-09, stage 2 pricing, V11 with two drops (0.56 at 44 per cent of the run): carried to the last drop it moved only
  9 kWh; three drops with a first stop at a fifth of the run move it 18.
- 2026-11-09, stage 2 pricing, the winter ratio at 0.0100 a degree and drag 0.046: the year's ratio moved every energy
  11 to 13 kWh and flipped nothing at a 13 kWh margin; at 0.0120 and 0.054 it moves 12 to 20 and flips V03, V11, V33.
- 2026-11-09, stage 2, a payload elevation term (the loaded leg's net descent): within-duty payload spread times a fixed
  elevation is under 1 kWh against 7 kWh of trip noise, so the term is set by physics constants (an efficiency and a
  regeneration share) the pack cannot pin: a fork, dropped.
- 2026-11-09, stage 2, a 2027 annual electricity figure over a normal year (the convexity of the cold curve): the gap
  between the year's energy at the mean temperature and over the ten-year distribution is about 2.5 per cent, inside the
  honest family's spread; dropped.

- 2026-11-09, architecture 6 (three estimates each moving the order: the payload term under declaration error, the
  sub-zero cold curve, the first-year battery loss net of the cold): the platform's run 1 landed the call and every
  graded figure (13 of 14 energies in their bin, 2.0 and 3.8 exact). It corrected the declarations by their measured
  error variance, kept a temperature quadratic on its fit, and regressed energy per full charge on age, temperature
  and tractor: each step a reflex for a frontier run once the asks named the quantity. Its own assumptions list named
  the gap it left untested: "Energy scales linearly with route distance ... the new round trips are 266-355 km,
  compared with 202-241 km for the pilot routes, so this remains a transfer assumption." Architecture 7 keeps the
  three steps in the chain and puts the deciding work in that transfer.
- 2026-11-09, stage 2, a second scenario (the order on a -10 C or -8 C day) as a further graded result: duties sit
  within 1 kWh of the limit across the honest rivals at both temperatures; dropped.
- 2026-11-09, stage 2, the drag coefficient at 0.032: leaving speed out moved every energy only 6 to 15 kWh, so half
  stayed within the graded 10 kWh and the careful pass priced at 58.5; at 0.046 (air drag about a sixth of the draw
  at 70 km/h) the shift is 9 to 21 kWh.
- 2026-11-09, stage 2, a drive-software update logged in the workshop file as the second judgment (the pilot's
  efficiency stepping down at each tractor's own update date): a timing break built into the data, found by one
  residual plot and fixed by one indicator, the client's shallow hidden factor; not built.

- 2026-11-09, stage 4, the dairy and the pallet maker writing one standard full-load weight on every note (13,500 kg
  on all 389 of the dairy's pilot notes): the determinism judge read a column with no spread at all as an authored
  device; both now declare the load plan's pallets at a standard weight each (540 and 360 kg), the pallet count on
  the note agreeing, and the per-shipper calibration carries them like any other.
- 2026-11-09, architecture 5 (one deep step: the declared payloads' dilution, with the cold form and every other step
  never moving a duty): returned by the portal, version 13, reward 68.5, not stumped. The review: the decision rests on
  one recognition, Tabergs Trävaror's exact declarations confirm the corrected term for free (2.19 against 2.20), and
  under calibration V03, V07 and V11 stay over the limit under every cold form. Rebuilt in the same world on the
  client's instruction as a results chain in which three estimates each move the order.
- 2026-11-09, stage 2 pricing, the drinks maker's scale from November 2025 or June 2026: its scale-weight pilot days
  alone (340 or 128) pinned the payload term at 2.03 with a standard error of 0.33, a second free check; from 17
  August 2026 they are about 60 and give 2.2 with a standard error of 0.52, a band from 1.2 to 3.2 that does not tell 2.0 from the declared fit's 1.2.
- 2026-11-09, stage 2 pricing, Forsheda Gummi in place of Tabergs: the pilot shippers' mean loads spanned only 10.8 to
  13.6 t, so the payload term was confounded with the duties' own route effects (2.5 to 2.7 on the true payloads
  against 2.15); the glassworks at 21 t widens the span and the route effect is halved.
- 2026-11-09, stage 2 pricing, the sub-zero curve at 0.0175 kWh per km per degree: one cold rate shifted every energy
  about 8.5 kWh, leaving no room between the one-rate route's margin and the golden's on V03; at 0.024 the shift is
  about 12.5 kWh.
- 2026-11-09, stage 2, a cold figure of its own (the design day's extra energy per 100 km over a mild day): one rate
  and the curved forms agree on it within the honest family's spread, because the one-rate fit lowers its base
  instead; the cold form is graded through the fourteen energies.
- 2026-11-09, stage 3, the pilot's 468 kWh usable battery: on cold days late in the pilot the logged state of charge
  went below zero (the architecture 5 pack had days ending at -13 per cent); the pilot battery is now 520 kWh usable
  and the longest duties are shorter, so no day ends below 5 per cent.
- 2026-11-09, stage 3, the quotation's warranty at 70 per cent after 8 years (3.75 per cent a year): inside the loss
  band, so the manufacturer's floor would have given the graded loss; at 75 per cent it gives 3.1, outside the band,
  and still orders the six.

- 2026-11-08, stage 5, the forum and context artifact as drawn (board_of_directors, register): `guard.py heart` on
  the final pull BLOCKed both (`ban.forum`, `ban.artifact`) against task2 v4, registered after this card; redrawn to
  executive_team (the management group approves the order) and operations_log (the weighbridge and telematics logs
  carry the evidence), the prompt, FES-2 1 and 4.4 and the memo reworded; no figure moved.

- 2026-11-08, stage 4, narrowing the pilot shippers' mean loads (11.7 to 12.9 t) so the pilot-shippers' pooled line
  (rung 2a) falls clear of the limit: the golden lost the between-shipper spread its estimate leans on (slope 1.95, the
  within-duty fit and the shipper-mean route left the golden's bins and the latter its six); reverted, the rung is
  ruled out by the per-shipper slopes and recorded as straddling the limit.

- 2026-11-08, architecture 4 (the Irish retailer's outlying districts handed to a courier, each set priced on the
  fitted van run): spent on the platform; the author reports not stumped, run texts not supplied to the repo. The van
  that drives through a district to reach the next one is a mechanism the stop sequences visibly carry (the run-days
  that skipped a district show it), modelled on sight like every earlier Sulfur landing. The world is left; the next
  deep step must sit in a property the rows in view cannot show, with its evidence in another file.
- 2026-11-08, stage 2 pricing, the pilot's telematics at trip grain (each leg's energy): the empty legs carry a payload
  of exactly zero, an error-free contrast with the loaded leg, so the declared fit's payload term came out at 2.0
  against 2.2 and the dilution vanished; the fleet portal's daily summary is the pilot's record.
- 2026-11-08, stage 2 pricing, clerks' error at 21 to 24 per cent: the declared slope fell to 0.6 kWh per tonne per
  100 km, below what rolling resistance alone costs, a figure a solver sanity-checks against physics; at 17 per cent
  it is 1.0, low but not absurd.
- 2026-11-08, stage 2, an ask on each going duty's spare load to the nearest tonne: the standing family spread it over
  a tonne on four of six duties (a fork on the asks); dropped.
- 2026-11-08, stage 2, the shortlist on mid-weight loads: duties near the pilot's mean load (12 t) give the same energy
  on any slope, so the shallow run kept 6 of 14 energies; the shortlist's shippers now sit far from the mean.

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
- 2026-11-10, architecture 10 stage 4, pass 7 on target.zip 67186f2dd19abb65 (the 690 kW world): judge DETERMINISTIC APPROVE (17 needs a charging efficiency under 0.894, never observed; 19 needs 0.948 or more, one outlier session in 3,291; the heater band, 10 to 20 minute margins and both schedules land 18; careful but hurried about 2.5 of 8, ordering about 21; the diesel ask does not hand over the bridge). Its two findings: the six pilot buses after delivery, closed as SF30 (one bus a block assigned, the night on the assigned blocks); and the Step-by-Step's earliest-departure clause, which its thread could not reproduce because it took every block as in the depot the whole night (3 of the 18 are; the generator's least-slack schedule recharges the 18 and earliest-departure-first leaves 98 kWh short), so the clause is cut to the exact flow and the least-slack schedule. The fourth leak reader quoted no process sentence, found no helper file and no one thing, and noticed the fuel heaters on a read, so R3's notice is a careful-pass move and its price rests on the figure from the HVO fills. No graded figure and neither zip moved.
- 2026-11-10, architecture 10 loop 1, the platform's holistic audit (0 of 1 items addressed): the order count was not
  forced (the agreement's "except for the workshop's two outlets at 22 kW" beside DES-1 3.2's "in the periods the
  agreement gives it" and the quotation's 22 kW AC inlet put M124 in, 19 for 18), and "a yes or no on going electric"
  (23 or 18), "every block that passes" (8.7 or 6.7 MWh) and "deliver" (8.0 or 8.7 MWh) each read two ways. Closed by
  WHAT pins (DES-1 3.2: the charging lane's chargers, the workshop's outlets for buses under repair, the draw as the
  chargers take it; the agreement and the plan on the outlets; the prompt's "qualifies under the standard" and "the bus
  of every qualifying block on charge" at the connection point). With the heaters already read by a careful run (the
  leak reader noticed them), the heater fix alone landed the old count (18), so the chain was one judgment short: the
  charging sessions now carry what a bus on charge draws beside its recharge (the battery held at charging temperature
  on a cold night), a third independent judgment graded as component 3, which moves the order to 17; the six pilot
  buses move to Kauppala in the plan, closing SF30 by the data.
- 2026-11-10, architecture 10 loop 1, the least night-period capacity at which every qualifying block can be
  recharged, as a sixth ask (the reinforcement's size): the exact flow needs 921 kW against 913 kW for the night's draw
  over its ten hours, because almost every qualifying bus is in the depot from 21:00 and leaves after 05:00, so the
  averaging shortcut lands inside any honest band and the ask would grade nothing; not built.
- 2026-11-10, architecture 10 loop 1, a cabin preconditioning load before departure from the charger (the quotation's
  earlier row): the relay holds the chargers off from 07:00, so the blocks departing after 07:00 (and the afternoon
  blocks departing after 11:00) could not precondition from the charger and the draw's timing forked; replaced by the
  battery's thermal management over the released hours, which the relay bounds on every block.
- 2026-11-10, architecture 10 loop 1, the clean re-judge (FIX_NOW, order kept): the loss band of 3.8 to 5.0 excluded a
  straight line in age (2.96 on that pack, 2.80 on the judge's refit) with nothing shipped ruling it out; the loss moves no
  verdict and no bus, so the band is widened to 2.7 to 5.0 rather than a document naming the age form (a HOW pin). The
  same pass recomputed the 17 and M145 by its own max-flow and least-slack schedules across its own readings of the
  charging split and the workshop outlets, the night at 9.23 MWh and the conditioning at 2.98 to 3.46 kW, all inside
  their bands; its simplified diesel refit (19 blocks, no swipe merge) did not reproduce ask 1, which `verify.py`
  reproduces on all 48 within 0.7 on its own code path, so Step 2 now says the fit is joint over every block the
  intervals touch. The answer blocks dropped the context figures an earlier audit read as rival answers (the energy
  into the batteries, the draw for the assigned blocks, the fit's unbanded efficiency and parameters from component 3).
- 2026-11-10, architecture 10 loop 1, the main thread's check on the FIX_NOW re-judge (APPROVE, order kept), whose own
  conditioning fit came out at 2.23 kW: the battery's gain on charge read on the fitted fade curve without the
  reversible cold capacity put the draw at 2.27 kW, the efficiency at 0.958 and the order at 18 (M124 refused), and fitted
  the sessions better than the day's own record, a fork on the call. The reversible cold capacity was 0.16 per cent a
  degree below 10 C (4 per cent at -15 C), riding in the gain on exactly the cold nights the conditioning is read from;
  at 0.04 per cent a degree (1 per cent at -15 C, a pack its thermal management keeps warm) every capacity basis but the
  bare quoted 480 kWh lands 17 with M145 refused (SF42), and the loss, the verdicts, the energies and the order do not
  move (the limit 390.5 to 390.3 kWh). The APPROVE was scoped to the earlier pack, so the judge runs once more.
- 2026-11-10, architecture 10 loop 1, the platform's Domains Fit return on the READY prompt (979f04f): it read every ask as
  a lookup or a certified figure applied to a stated rule ("look up diesel use per 100 km, compare a quoted kWh figure
  against a design-day threshold, count qualifying blocks, and sum connection-point energy ... nothing needs to be
  estimated, modelled, forecast or validated"), the "quoted 2027 model" taken for a quoted energy. The prompt now leads
  with the forecast's population (most of the blocks never run by an electric bus) and names each result as what it is
  (an estimate of the diesel use, a forecast from the company's own operating records of the design-day energy, an
  estimate of the loss, a forecast of the night's draw), as this slot's architecture 5 did when the same review read it
  as route arithmetic; the answer blocks say the same. A 90 per cent interval on the loss, the review's own example, was
  measured and not built: the iid, by-bus clustered and per-bus intervals all read 4.2 to 4.5 on this pack, so it would
  grade nothing, and its bounds would inherit the age-form fork the band was widened for. No graded figure and neither
  zip moved.
