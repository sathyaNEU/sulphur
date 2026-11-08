# task3 architecture 4: Sallow Road well field, the nitrate plant's loan cycle

Physical & Environmental Sciences, hydrology (Sulfur task type: physical-model calibration and data assimilation,
spatiotemporal exposure and source apportionment), Forecasting & Predictive Modeling. Re-root of the slot after the
platform landed architecture 3 (both runs on the golden at every ask, `runs/triage.md`): one architecture per world, so
a new world, dataset and shell.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task3.json` v4, registered 2026-11-08 at PASS (differentiated against
  mark181, mark166, mark451, mark234 and task3 v1; lineage carries v1 to v3 with their fates).
- **Pairing:** a city water utility on Wisconsin's central sand plain must choose the state loan cycle for its nitrate
  removal plant; a plant funded in 2027 enters service on 1 January 2030, one funded in 2031 on 1 January 2034, and the
  plan requires it in service before the first year the entry point's annual flow-weighted mean nitrate reaches 10 mg/L.
- **Shape:** a when-question (2027 or 2031) with a yearly forecast 2027 to 2040, the first year at 10, the 2034 entry
  point and the well highest in 2034; a memo PDF, a forecast workbook and a chart PNG.
- **Strategy:** outcomes that have not finished happening (Part A, WORKS IN FORM, F4's live form: completion speed
  differs by a unit no pooled factor captures, here each parcel's depth to water) fused with separating two
  explanations for one pattern (the recent clearing's absent response read as no effect or as not yet arrived).
- **Data-native sentence:** a sand-plain well field whose nearest recharge land is an ice-contact ridge with 57 to 94 ft
  of dry sand above the water table, cleared for irrigated vegetables from 2017 to 2021, beside a county network whose
  older conversions, mostly on 11 to 49 ft of sand, step up later the deeper the water table.
- **Abstraction sentence (written, then tested):** "a recent change at sources that sit deeper in an unobserved stage
  than every earlier change that matured, so every check on the output reads its absence as no effect." Against every
  approved and delivered build in `guard.py mechanisms --objective forecasting` and the F4 cards, no decisive step
  separates an unarrived effect from a nil one through a depth-specific delay read from matured changes; mark181 (each
  courier route's own reporting delay), mark451 (a handler's delay that collapsed), mark166 (departures linked at a
  lagged yield) and mark234 (a loss in transit) each spend a different insight.
- **Sources** (all synthetic, authored for this task, CC0; `metadata.json`): the utility's nitrate results 1988 to 2026
  (raw water and EP-01), its SCADA daily pumping 2009 to 2026, the county network's samples 1990 to 2026 and site
  register, the county's parcel land cover 1986 to 2026, the 2019 wellhead protection plan with its parcel attributes and
  Figure 3, the county's 2019 tritium-helium survey, the 2025 water supply plan, and three distractors (the wells'
  construction records, their specific capacity tests, county fertiliser sales).
- **People:** drawn with `guard.py names --geo "United States"` (seeds 4417 and 3311): Chloe Griffin (general manager),
  Dennis Diaz (operations superintendent), Patricia Gaines (Fenwright's hydrogeologist), Cindy Beard, Danny Sharp and Lindsey
  Waller (county samplers, initials only in the data).

## Default path

1. Convert the utility's results to nitrate-N (the county laboratory's nitrate before 2004 over 4.427), average the
   duplicates and re-runs, map the 2014 point names: EP-01 fell from 6.2 mg/L in 2012 to 5.3 in 2025, Wells 6 and 7
   from 6.9 and 5.7 in 2010 to 5.4 and 4.5 in 2026.
2. Trend each well over 2015 to 2026 and blend by the plan's shares: EP-01 near 4.7 mg/L in 2034, never at 10.
3. A strong analyst does not stop at the trend: the parcel land cover shows the Sallow Ridge, 1,099 acres in the zones
   of Wells 6 and 7, cleared for irrigated vegetables from 2017 to 2021, one to three years' groundwater travel from the
   wells. It builds the protection area's mix (each parcel's land cover, its leachate from the network, its wellhead
   model travel time), fits one lag to the wells' 1998 to 2018 record (4.5 years, residual 0.41 mg/L), and finds the
   ridge should have raised Well 6 by about 10 mg/L by 2026.
4. Wells 6 and 7 show no rise, nor do the network's three wells under the 2017 to 2020 upland clearings; fitted to
   the 2019 to 2026 record the clearing's effect comes out at nil (the fit's squared error 1.2 at nil against 581 at
   the network's leachate), so the model forecasts EP-01 near 5.5 mg/L in 2034 and never at 10.

Ends on: the 2031 cycle
Golden: the 2027 cycle

## Stump sentence

A strong analyst who finds the ridge clearing tests it against the wells and the county wells under recent clearings,
sees no rise where the wellhead model's travel time or one lag fitted to the wells' own record says it should already
be, sets the clearing's effect at nil and files the 2031 cycle with EP-01 near 5.5 mg/L through 2040; only each parcel's
delay through its own unsaturated thickness, read from the county's matured conversions (0.132 years a foot), puts the
ridge's leachate at the wells late in 2030, EP-01 at 10 in 2031 and the 2027 cycle.

## Deep reasoning

- **Task type:** hydrology flood frequency is the vocab key; the Sulfur task type is physical-model calibration and data
  assimilation with spatiotemporal exposure (a well field's nitrate forecast from the land over its zones), serving
  forecasting.
- **Domain test:** the deciding quantity is a well field's blended nitrate over the next decade, which groundwater
  quality forecasting builds by convolving land-surface leaching with the travel time to the well, usually the
  groundwater travel time from a wellhead protection model or a lag fitted to the wells' record.
- **Swap:** "when does the blended nitrate reach 10 mg/L" becomes "when does a retailer's blended margin reach 10 per
  cent": there is no water table, no unsaturated sand whose thickness sets a delay, no recharge to mix by and no
  conversion whose leachate is still above the water table, so the delay and the absent response stop meaning anything.
- **Layer 1:** nitrate as NO3 at the county laboratory before 2004 and '<' values at two reporting limits (laboratory),
  field duplicates and re-runs as extra rows and the 2014 SCADA point names (utility), two network wells rebuilt under
  new numbers in 2011, fall-only sampling in 2009 and 2010 and keyed-twice rows (county network), local land-cover codes
  to 2007 and cropland-layer codes after, assessor splits in 2012 and the ridge re-numbered at its 2015 sale, a 2016
  township exported twice (land cover), gallons then thousand gallons at a 2019 meter change and a duplicated export week
  (SCADA); nothing is placed to be caught.
- **Layer 2:** outcomes not finished: the leachate of a recent clearing is still above the water table, at a depth no
  sample sees, and its arrival is timed by each parcel's own unsaturated thickness, which only the matured conversions
  calibrate.
- **Decisive step:** reading the absent response at Wells 6 and 7 and at the network's recent clearings as leachate not
  yet arrived, with each parcel's delay to the water table built from its depth to water on the relation the matured
  conversions show, not as the clearing leaching nothing under a pooled lag.
- **Not semantics:** every field, unit, code and key read correctly (nitrate-N, the rebuilt wells, the parcel splits,
  the code change) still leaves the delay to be chosen, and the wellhead model's travel time, one lag fitted to the
  wells, and the matured conversions' average delay each put the ridge at the wells before 2026.
- **Not rule application:** the plan files the cycles, the in-service dates, the 10 mg/L test at EP-01 and the shares;
  no filed sentence names a delay, the unsaturated zone, a conversion cohort or a mixing weight.
- **Analyst test:** a strong analyst cleans every file, builds the parcel mix with the network's leachate and the
  wellhead model's travel time (or one lag fitted to the wells), finds the clearing's predicted rise absent, fits its
  effect to nil and files the 2031 cycle.
- **Estimand:** the 2025 water supply plan sections 2 to 4 (EP-01's annual flow-weighted mean nitrate as N, the plan's
  shares from 2027, the plant in service before the first year that mean reaches 10 mg/L, 2027 cycle in service 1
  January 2030, 2031 cycle 1 January 2034) and the prompt (land cover held at 2026; each year 2027 to 2040; the 2034
  means to the nearest whole mg/L).
- **No decoy:** no memo, plan or report states a nitrate forecast, a delay or a judgement on the cycle; the wellhead
  plan delineates and inventories, the supply plan schedules.
- **No certified replay:** no published forecast exists for the method to reproduce.
- **Chain:** (1) the wells' falling-then-flat record is the nutrient-management era's water arriving and cannot show
  leachate still above the water table; (2) the county's matured conversions step up after a delay that grows with
  depth to water (0.132 years a foot, residual 0.3 years) while their water-table ages are under half a year, so the
  delay is in the unsaturated sand and the wellhead model's travel time starts below it; (3) the ridge sits on 57 to
  94 ft against the 11 to 49 ft under all but three matured conversions, so no pooled delay applies and its leachate
  reaches the water table from 2028 and the wells late in 2030; (4) the leachate under irrigated vegetables since
  nutrient management (20.9 mg/L) mixed into each well by the recharge each parcel had when its water left the water
  table; (5) the plan's shares from 2027, EP-01 at 10 in 2031, before 1 January 2034.
- **Judgment:** separating "the clearing does not raise nitrate" from "its leachate has not arrived" with the matured
  conversions' delays against depth, the network's three recent upland clearings as the check (silent at 69 to 90 ft,
  as the depth predicts), and carrying the depth-specific delay, not a pooled one, to each ridge parcel.
- **One-fact test:** the likeliest hint, "the ridge clearing will raise nitrate", rescues nothing: with the travel time
  or the fitted lag the rise should already show, it does not, and the reasonable fit sets it to nil; the hint "the
  water table is deep under the ridge" still leaves the delay per foot to be read from the matured conversions, the
  leachate level, the mixing and the blend.
- **No replay:** the call is a forecast for 2027 to 2040; no shipped number is re-derived or wrong.
- **Pinned:** the rivals run on the cut pack (`generator/rungs.json`, asserted in `checks.py`): the arrival read
  half-way, as a fitted step, at a quarter or three quarters of the rise; the delay with or without an intercept and
  with or without the water-table age; the leachate's current level over 3, 5 or 8 land-surface years or from the
  matured conversions' post-arrival samples; nondetects at half, zero or the limit; the model carried to the wells'
  level or not; the class record smoothed over one, three or five years. Every one files the 2027 cycle, 2031, 12 mg/L
  in 2034 and Well 7 at 16.
- **Run forecast:** a run first goes wrong by a self-confirming check (it fits the clearing's effect to the wells'
  2019 to 2026 record, which under the travel time or a pooled lag rejects the effect outright) or by dismissing its
  own evidence (the matured conversions and the recent upland clearings it reads as evidence of a small effect); a
  trend run takes a method shortcut.
- **Strategy label:** WORKS IN FORM (outcomes that have not finished happening, live form: completion speed differs by
  a unit no pooled factor captures, the pooled factor files a named wrong answer; and separating two explanations, live
  form: only a like-for-like comparison rebuilt from history separates them).
- **Lesson:** an absent response is evidence of no effect only once the effect has had time to arrive, and the time
  it needs is a property of each source, read from the sources whose changes matured; no build on file pairs the two.

## Survivor anatomy

- **Actor:** every ridge parcel has rows (land cover by year, acres, depth to water, travel time); the property that
  decides (when its leachate reaches the water table) is held in no column and comes from relating the network's
  conversions to their depths.
- **Link:** the delay per foot is read by aligning each network well's sample history with its parcel's land-cover
  history and its depth, a join the wellhead model and the wells' record never ask for.
- **Reflex:** the trend (rung 0) and the protection-area mix on the wellhead model's travel time or one fitted lag with
  the clearing tested against the record (rung 1) both file the 2031 cycle.
- **Back-test:** the textbook routes validate: the single lag fits the wells' 1998 to 2018 record to 0.41 mg/L, and
  with the clearing set to nil every rung-1 model fits 2019 to 2026 as well as the golden does.
- **Second use:** every file the decisive step reads has its own use: the network is the county's groundwater program,
  the land cover its inventory, the parcel attributes and their depths the wellhead plan's appendix, the age survey the
  state survey's dating of the network.
- **Shock:** the clearing is an ordinary land sale and conversion in the land-cover panel, ten parcel-years among 5,700
  rows, never a step in any well's record or the pack's largest anomaly.
- **Pins:** the WHAT sits in the supply plan (EP-01, the annual flow-weighted mean, 10 mg/L, the in-service dates, the
  shares) and the prompt (land cover held at 2026, the rounding); no sentence names a delay, the unsaturated zone, a
  conversion cohort or a mixing weight.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 Trend on each well | no | no | yes | no | no | no | no | readable |
| 1 Parcel mix on the travel time or one fitted lag, the clearing fitted to the record | no | no | yes | no | no | no | no | readable |
| 2 Each parcel's delay from its depth on the matured conversions' relation (decisive) | no | no | no | no | no | no | no | silent |
| 3 Mixing by recharge and the plan's blend | no | no | yes | no | no | no | no | readable |

## Semantic fork table

| Id | Term or convention | Reading A (golden) | Reading B | Golden under A | Under B | Ruled out by |
|---|---|---|---|---|---|---|
| SF1 | the compliance measure | EP-01's annual flow-weighted mean (plan 3, prompt) | a single sample or a well's own level | 2027 cycle | not computed | plan section 3 and the prompt file the annual flow-weighted mean at EP-01 |
| SF2 | pumping from 2027 | the plan's shares (8, 30, 32, 30) | the 2009-2026 shares | 2031 | 2031 (2034 mean 11) | plan section 2 fixes the shares for 2027 to 2040 |
| SF3 | land cover after 2026 | held as in 2026 | trends continued | 2031 | not computed | the prompt holds each parcel's land cover as it stood in 2026 |
| SF4 | in service | 1 January 2030 or 2034 | the cycle year | 2027 cycle | 2027 cycle | plan section 4 files the dates |
| SF5 | the arrival point | half-way between the levels | a fitted step, a quarter or three quarters | 2031, 12, 16 | 2031, 12, 16 | same call (asserted) |
| SF6 | the delay's form | a + b x depth | through the origin; without the water-table age | 2031, 12, 16 | 2031, 12, 16 | same call (asserted) |
| SF7 | the current leachate | the five latest land-surface years | three or eight years; the matured conversions after arrival | 2031, 12, 16 | 2031, 12, 16 | same call (asserted) |
| SF8 | nondetects | half the reporting limit | zero or the limit | 2031, 12, 16 | 2031, 12, 16 | same call (asserted) |
| SF9 | carrying the model to the record | each well's 2019-2026 residual | uncarried | 2031, 12, 16 | 2031, 12, 16 | same call (asserted) |
| SF10 | the mixing weight | acres times the recharge when the water left the water table | acres alone; the recharge when it left the root zone | Well 7 16, EP-01 12 | Well 7 15, EP-01 11 | the wellhead model's water balance (recharge differs by land cover) and continuity at the water table (the recharge arriving is the land's recharge then) |
| SF11 | vegetable leachate's level | since nutrient management | the mean over every year | Well 7 16 | Well 7 17 | the network's unchanged irrigated sites fall from about 34 to 21 mg/L by land-surface year 2005 and stay there |

## Ladder

- **Rungs and winners:** rung 0 trend on each well files the 2031 cycle (EP-01 4.7 mg/L in 2034, linear or Sen); rung 1
  the parcel mix with the clearing fitted to 2019 to 2026 files the 2031 cycle under the wellhead model's travel time
  (squared error 0.9 at nil against 1,195 at the network's leachate), one lag fitted to 1998 to 2018 (4.5 years; 1.2
  against 581) or the matured conversions' average delay (4.7 years; 1.1 against 156), each EP-01 near 5.5 mg/L; the
  decisive rung (each parcel's delay from its depth) files the 2027 cycle, EP-01 at 10 in 2031 (6.0 in 2030, 11.8 in
  2031), 11.9 in 2034, Well 7 15.9. Off the ladder: mixing by acres alone or at the root-zone recharge keeps the call
  and puts Well 7 at 15; the all-years vegetable leachate keeps the call and puts Well 7 at 17.
- **Margins:** the golden's crossing sits 3 years before the 2031 cycle's in-service year; every standing rival keeps
  2031 (EP-01 5.4 to 8.6 in 2030, 10.2 to 12.3 in 2031), 2034 at 11.8 to 12.3 and Well 7 at 15.8 to 16.3.
- **Pricing:** (1) the residue the WHAT leaves is the delay, a method; (2) the move the call needs (EP-01 from 5.5 to
  past 10 before 2034) is the ridge's arrival inside the window, which only the depth-specific delay gives; (3) the
  one-group-by route (the cohort's average delay) is a rung 1 shortcut; (4) the delay per foot spreads 0.128 to 0.136
  across the arrival readings and forms, and the call holds from 0.10 (below it the ridge would already show in 2026)
  to 0.17 years a foot (above it the ridge arrives after 2033); (5) no variance is the lever; (6) the wells' record cannot calibrate the ridge's delay
  (its squared error is flat in the clearing's effect under the golden's delays: 1.109 at nil and at full); (7) no
  subset of rows hands over the delay; (8) every visible grouping of the network (land cover, installation year,
  sampler, laboratory) was swept and only depth to water carries the delay.
- **Dominance:** each lower rung's single correction leaves it on the wrong cycle (`checks.py` R3).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 population | EP-01's blended water | plan section 3 |
| 2 outcome | annual flow-weighted mean nitrate as N | plan section 3, prompt |
| 3 window | each year 2027 to 2040 | prompt |
| 4 unit | mg/L as N, the 2034 means to the nearest whole | prompt |
| 5 comparison | the first year at 10 against the in-service dates | plan section 4 |
| 6 shares | 8, 30, 32 and 30 per cent from 2027 | plan section 2 |
| 7 in service | 1 January 2030 and 2034 | plan section 4 |
| 8 land cover after 2026 | held | prompt |
| 9 nitrate units | as N, NO3 over 4.427 | laboratory units column |
| 10 duplicates | averaged with their sample | data |
| 11 rebuilt wells | old numbers to the new | sites register notes |
| 12 parcel splits | through parent_parcel_id | land cover file |
| 13 codes | the legend sheet | sites workbook |
| 14 meter change | per-row units | pumping file |
| 15 water-table ages | the 2019 survey, the survey mean elsewhere | age survey |
| 16 recharge by land cover | the wellhead model's table | parcel attributes, Recharge |
| 17 the delay | from the matured conversions, by depth | the data (decisive) |
| 18 the clearing's effect | the network's current leachate | the data (decisive) |
| 19 rounding | whole mg/L for the 2034 means | prompt |
| 20 tie at 10 | none within 0.6 mg/L in 2031 | asserted |
| 21 the cycle rule | in service before the first year at 10 | plan section 4 |
| 22 as-of | 6 November 2026 | the data's end and the memo date |

## Literal reader

Executing the plan and the prompt word for word gives the estimand (EP-01's annual flow-weighted mean under the plan's
shares, each year 2027 to 2040, land cover held at 2026, the plant in service before the first year at 10) and leaves
the delay and the mixing to the data; every reading of the filed sentences that the data leave standing files the 2027
cycle.

## Oracles

none: no control, published figure or corpus ties under any basis; the network wells are evidence, not a scored bench,
and the three recent upland clearings agree with the golden's delay and with a nil effect alike (neither has arrived).

## Ask sheet

- **Asks:** (A1) the first year EP-01's annual mean reaches 10 (2031); (A2) EP-01's 2034 annual mean, nearest whole
  mg/L (12); (A3) the well with the highest 2034 annual mean and that mean, nearest whole mg/L (Well 7, 16); the memo,
  the workbook's yearly forecast and the chart (instruction following).
- **Devices:** every graded figure rides the decisive step (the default path files no crossing, EP-01 near 5 and Well 5
  highest at 7), and A2 and A3's value carry a second judgment of their own: the mixing weight (acres alone, or the
  recharge at the time the water left the root zone with the model carried to the wells' level, puts EP-01 at 11 and
  Well 7 at 15) and the leachate's era (the all-years vegetable mean puts EP-01 at 13 and Well 7 at 17).
- **Spans:** A1 2031 across the standing family and every second judgment; A2 11.8 to 12.3; A3 Well 7 at 15.8 to 16.3.
- **Pair ceiling:** 42.2 (the cracker lands the call and A1 but mixes at the root-zone recharge, 72.5; the mirror on
  rung 1, 12.0); with acres alone and its 2034 entry point counted kept, 49.1.
- **Shallow keep:** 0 per cent of ask weight kept by the default path.
- **Measured by:** generator/ceiling.py

| Ask | Golden | Default path (rung 1, one lag) | Cracker (deep step, root-zone recharge weights) | Verdict |
|---|---|---|---|---|
| A1 first year at 10 | 2031 | none | 2031 | yes |
| A2 EP-01 2034 | 12 | 5 | 11 | miss |
| A3 highest well | Well 7 | Well 5 | Well 7 | yes |
| A3 its 2034 mean | 16 | 7 | 15 | miss |

## Prompt contract

The author's rewrite keeps: the question (the 2027 or the 2031 cycle for Project NR-1); the plan as the source of the
in-service dates, the 10 mg/L test on EP-01's annual flow-weighted mean and the shares from 2027; land cover held as it
stood in 2026; `corlinden_nitrate_plant_timing_memo.pdf` with the call; `corlinden_entry_point_nitrate_forecast.xlsx` with
EP-01's annual mean for each year 2027 to 2040; `corlinden_entry_point_nitrate_2027-2040.png` charting it against 10 mg/L;
the first year at 10, EP-01's 2034 mean, the well highest in 2034 with its mean; nitrate as N, the 2034 means to the
nearest whole mg/L. The as-of is 6 November 2026, with data to October 2026.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call rests on the depth-specific delay (R3 and R4 asserted);
  no field reading, filed procedure or planted catch decides it; the one-fact hint leaves rung 1 on the 2031 cycle.
- Free gates and stage 4 are recorded in `pipeline.json` and the two reports.

## Tried and rejected


Architecture 1 (Quellbrook rock salt), carried from its note:


- Pattern E on the card: E's discriminator is an absolute split, which this build does not have (the gain falls
  continuously with coverage), and the structural tests collided with five older builds; the pattern is none with G14.
- The city named Halbrook: within one letter of Holbrook (a real place); renamed Quellbrook after a check.
- The first collector parameters (Priority 1 hazard spots at 10.0 t and Priority 2 at 9.0 t a lane-km): the golden
  (2,206 t) sat on the midpoint of the default (2,652 t) and the pooled gain (1,768 t), so a response averaging two
  rivals filed the call; the hazard rates were re-set (9.7 and 10.2) and the earlier transit moves given inner-suburb
  coverage, so every midpoint of rivals now files 2,000 to 2,100 t.
- Centreline km asserted as neutral on the call: rates and lengths taken in centreline km throughout file 1,900 t,
  because collectors have two or four lanes; closed by the plan's application rates set per lane-km (SF3), not by data.
- One device carrying Ask B (the run totals alone): a cracker who dedupes per run recovered all twelve figures; the
  combined salt and brine mass (B1b) was added on the same controllers.
- Ask A's second device as transfers alone: it moved two yards only; the weighings at another yard's scale (A2) move
  all four, and the transfers stay as a hazard.
- Passes of one truck overlapping in time (two runs entering one segment in the same second): the sweep found them; a
  circuit's passes now run one after another on its one truck, with every tonnage unchanged.
- The forum `line_manager_or_team` (the director of roads signing the commitment): `ban.forum` blocked registration
  against task247, so the forum was redrawn to `council_or_assembly` in the build itself: procedure RO-PR-07 5 sends
  spending above the contract quantity to council under the procurement by-law, the deliverable became a one-page
  report to council, and the prompt names council; every figure unchanged.
- The supplier named Brackwater and the contractor Pellard: one letter from Blackwater and Pollard (H21); renamed
  Northgrit and Kettlewood after a search, every tonnage unchanged.
- The 2025-26 winter at 52.6 WSI points: the default netting at last winter's severity, or last winter's totals netted
  with no planning severity, landed 2,200 t by coincidence (52.6 sat inside the band, about 51 to 54 points, where the
  netting's figure scales into the golden's bin); the storm sequence was redrawn to 58.4 points, the per-point golden
  unchanged, and the route now files 2,400 t (asserted, LADDER R1c and HEDGE).
- Street rates as steady as a model (a 4 per cent winter-to-winter variation, the gain line at r = -0.98) and coverage
  blind to block length: each street now carries its own winter-to-winter multiplier, Priority 2 salt rises as blocks
  shorten, and the earlier moves were raised from 202 to 431 so that one standard error stays under 16 t; the golden
  came out at 2,202.6 t, inside the re-centring rule's 15 t, so R_MID did not move.
- The earlier flat moves given less coverage than the new streets (a different hazard share): the banded estimators
  then filed 2,100 t; the flat streets each reason brought in now carry the redesign's own hazard share, and every
  standard banding files 2,200 t.
- Ask B's arterial figures to one decimal with the yard basis left to the reader: the judge found the register's
  current yard a licensed second reading (about 800 t a winter at Kelvin Road and Mapleford) and no exact route for the
  older controllers; the ask now files the yard each circuit belonged to that winter, the plan files the pre-wet rate
  that makes the combined mass exactly checkable, and the figures are asked to the nearest tonne, which every honest
  construction shares.
- Every circuit run by one truck for three winters: trucks now swap between circuits of their yard and kind about one
  storm in seven; every tonnage unchanged in kind.
- The council item filed as a memo: a council item is a staff report, so the deliverable is
  `seasonal_salt_commitment_council_report.docx`, with the chart introduced as the programme the rolled-over contract
  carries.
- Cross streets named without a suffix (a naming bug in the second round of street names): fixed in the generator,
  every tonnage unchanged.
- Winters as steady as the index (the Priority 1 collector rate per point within 2 per cent across winters of 38.9 to
  67.2 points, the recheck's realism finding): each winter now carries a swing the index does not carry, common to every
  road (a winter's multiplier drawn with a 3 per cent spread, the realised rate per point spanning 14 per cent, inside the
  10 to 25 per cent real fleets show); R_MID then moved by the re-centring rule alone.
- Salt in proportion to severity closed by the data (the never-moved collectors' intercept near nil): under each
  winter's swing five winters tilt the line (an intercept of about a fifth of a winter's salt), so the plan now files
  that salt is planned per WSI point (SF6).
- One-winter windows as plain family members: each carries its winter's own swing; the family reads them netted against
  the never-moved collectors' same winter, and un-netted they stay in the bin, no longer a quarter-bin clear.
- 431 earlier moves in steady yearly counts (122, 112, 107, 90): each year now carries its own programmes (136, 69, 119,
  53, 377 in all); one standard error rose from 14.7 to 15.0 t.
- Three equal-count bands as a family member: on the new draw its second band (2.2 to 5.2 t a lane-km) holds the new
  streets' upper eighth and sits 1.1 t above them, and it files 2,147.8 t; it is listed with the median split and the
  wide kernels as a coarse setting that closes on the golden as it is refined, and nothing was moved to bring it back.
- The 10 earlier moves nearest the pool's mean as a crude setting that lands: it files 2,294.9 t on this draw; thin
  settings are asserted from 30 streets up, where they settle in the bin.
- R2i (the earlier moves inside the new streets' range, averaged) as a rung 100 t or more from the golden: it now sits
  77 t below (2,136.4 t), so it is listed with the crude conditioned forms.
- The gain component at one decimal (5.2, 0.045 from its edge, with four family members at 5.1 on the previous draw):
  stated as about 5 t a lane-km, the precision every construction shares (SF12).
- The own-salt component at one decimal (1.7 lane-km weighted against 1.8 as the streets' unweighted mean, the
  recheck's fork): stated over the five winters as about 700 t, under 2 t a lane-km, which every basis shares (SF13).
- The arterial figures to the nearest tonne: the loading-log calibration came within 0.2 to 6.6 t of the records'
  route, so the correction of the older controllers was unpinned at the tonne; the figures are asked to the nearest
  50 t and every cell sits a quarter-bin or more from its edge under both routes (asserted), while the brine left in
  still lands a full cell high and the run totals summed every row miss by a tonne a row.
- Route audit entries keyed row by row (the redesign over 52 days, a segment's priority and route rows on one day 2.8
  per cent of the time): the audit keys each change in a few sittings on working days, both rows of a segment together,
  and the change numbers follow the keying order.
- The one-sigma claim as written (every family member within one standard error): it holds with the golden's own
  error, not each member's; restated in `## Ladder` and in SIGMA.
- "On every pool alike" for the length effect: measured, it shows plainly on the redesign's streets and hardly on the
  earlier moves; the note now says what the data show and both pools are asserted.
- A2, the weighings at another yard's scale with the receiving dome in the remarks: the stage 4 blind reader read the
  four spellings and moved each load to the dome they name (Lakeshore's only after its flight), keeping all eight dome
  figures; re-sited as A3 and A4, the trucks still weighed on the way for a day after each scale came back, which the same
  remark routing counts twice or keeps at the weighing yard; the outage weighings stay as texture (HA5).
- A1, the survey's capture window in UTC: the reader converted the flight log to Eastern daylight time and cut at each
  flight's start; a clock re-sited onto the scale houses (a terminal on standard time, or one stamping UTC) was tried and
  dropped, since the yards held deliveries through every flight, so a cut at the flight's start agrees with one at its
  end for any offset under an hour, and a log stamped in UTC has nothing in the pack that forces the reading; it stays as
  texture (HA4).
- HA1, the dispatch re-issue: the reader took the latest issue's BOOKED October lines; re-siting it as an October booking
  delivered early in late September was tried and dropped, since nothing in the pack ties a September weighing to an
  October booking without a filed note; it stays as texture.
- B2, the contractor's circuits: the reader added every row of Kettlewood's returns, which is right; two re-sitings were
  tried and dropped, relief operators on City trucks reported in the returns (the rows would have to name City units,
  which announces it, and a contractor reporting a City truck's salt reads as planted) and returns by billing period, the
  26th to the 25th (it moves only Kelvin Road's and Mapleford's 2024-25 cells, the one winter with storms after 25
  March); it stays as the mirror device.
- HB2, the register's current yard: the reader took the yard from the route code as run and kept MPF-A01 and MPF-A02 at
  Mapleford; re-sited as B3, the platform carrying the two circuits' current Kelvin Road codes on every pass they made,
  so the code a pass carries is the misreading and the revision log's 1 July 2026 entries are the key.
- B1 and B1b, the run totals and the combined mass: they held six cells, and the reader landed the other six by halving
  the fleet list's M410 rows after reading them double against the loader log (a yard's runs average about two segments,
  so halving sits inside a cell where the brine and the run lengths offset); the evidence is re-sited from the fleet
  list's controller columns and the loader log to the rows' own run references and litres, the rows untouched (R0 and R0b
  read them as written).
- The yard loading log: each unit's winter at its loader tonnes is the salt it spread within its hopper's carry, so a
  loader-only route lands every arterial cell and the per-unit ratio hands any reader the halving, an oracle under ban 3;
  withdrawn, with the settle that kept the loader calibration inside each cell left as it was so the arterial rows stay
  byte for byte.
- The changeover weighings as one device: with every copy on the receiving yard's stored tare, dropping exact repeats gave
  back all eight dome figures (a pair of 42.8 with one device found, against the build's 40); the two unremarked copies
  carry their own scale house's older stored tare, so only the truck, the day and the gross tie them (A4).
- HB1, the UTC season dates: the reader converted them; nothing at a season boundary carries enough salt to move a cell,
  so it stays as texture.
- A3 and A4 as built in the repair's first round: invisible to a grader who checks consistency, since the supplier's
  trucks were drawn at random for each load (some at two scale houses minutes apart on ordinary days) and the tares at
  random for each weighing, so nothing contradicted a load weighed twice; the re-judge (judge-task3d) kept both
  weighings and could not find the golden's rule. The trucks now run round trips from the terminal and each scale house
  keeps one stored tare a truck for each account, so the five pairs are the only trucks back inside a round trip.
- B1 and B1b with nothing naming the controllers (the first round): the re-judge read the counting once as inferred and
  the brine as an unfiled convention, its brine's salt off every row keeping seven cells; Fleet Services' work orders
  now carry the four replacements and every tandem's calibration at 40 L/t, so the litres a tonne force the brine's whole
  weight and the work orders tie the repeated totals to the controller.
- A supplier's delivery statement by docket as Ask A's referee: one reconciliation would expose all five weighings at
  once and its loadout weights would offer a second dome basis beside the scale houses; the trucks' own times between
  scale houses do the work inside the log the ask already reads.
- Filing the older controllers' conventions in the dictionary (the re-judge's fix): a filed sentence that adjudicates,
  handing B1 and B1b to every reader; not taken.
- The controller model on every calibration work order: a controller list by unit and winter, the fleet list's
  withdrawn columns in another file; the model is named only where a controller was replaced.
- The asks' handling left to the pack alone (rounds 1 and 2): both re-judges, cold on the pack, took the readers' paths,
  and judge-task3e never tested the trucks' round trips, so the dome figures read as wrong although every arterial
  cell reproduced; block 3 now names each ask's handling, its filed basis and its result (steps 6 and 7), the pack
  unchanged.
- Step 6's first wording (round 3): the dome stocks followed the dispatch file's BOOKED October loads, and
  judge-task3f read them as the booked loads; each figure now carries its label, and the home yard's ticket cites
  RO-PR-07 section 2's "weighed at the yard's scale house".
- 2026-10-31, reship under the learning loop's rules: the data dictionary and the export manifest withdrawn (shipped
  files may not describe the data); the conventions they carried are the data's own (the KG and applied_t headers, UTC
  in entry_utc, the crosswalk file), and the plan's materials section names the codes RS, SALT, SS and SAND/SALT in the
  organisation's own words. The prompt dropped the 424 lane-km (a count the register holds) and drew a fresh shell.
- 2026-10-31, remarks on the two A4 pairs to close the judge's Gate C residual: rejected before cutting; it moves A4's double count onto Lakeshore and Mapleford and hands back Ridge's and Kelvin Road's four dome figures on every careful path.
- 2026-11-07, architecture 1 on the portal: R1 regressed each earlier move's gain on its own Priority 2 salt, read it at
  the new streets' and filed 2,200 t (100 per cent); R2 filed the default 2,600 t and kept 70 per cent through the asks.
  Conditioning a carried gain on a covariate every unit's own history prints is the strong solver's reflex, and the
  ask devices (double weighings, older controllers, realigned circuits) were found and handled; the world is spent and
  the slot re-roots (architecture 2, the Clay Street tank).

Architecture 2 (the Clay Street tank):

- 2026-11-07, a redesign inside the salt world (a stronger decisive step on the same streets): rejected before any
  data; one architecture per world, and every candidate step there was again a covariate the record prints.
- 2026-11-07, a sewer overflow world first framed with shape 10, a board forum and a statutory filing: blocked by the
  guard against task156 v3; redrawn to shape 08, the regulator receiving the facility plan and the design task order.
- 2026-11-07, the city named Vellmore, then Marrowgate and Tarnhollow: within two letters of Fillmore, Harrowgate and
  Tar Hollow; named Quessling after a search.
- 2026-11-07, tanks of 12, 20, 26 and 34 MG on the first tuning: the room moved the counts by under one event at the
  smaller tanks with too little rain (33 inches a year); the storms were deepened to about 40 inches a year (the
  Pennsylvania norm), the regulator raised to 26 MGD and the sizes redrawn to 19, 26, 38 and 50 MG.
- 2026-11-07, Alternative A at 18 MG: its golden count (111 events, 9.25 a year) sat on a twelfth's half at one
  decimal; moved to 19 MG (104 events, 8.7).
- 2026-11-07, storms wettest by far in late April (8 inches in April 2025, 0.3 in July): unlike Pennsylvania; the storm
  season was flattened and the spring weight left to the groundwater's reach into the Southside sewers.
- 2026-11-07, calibration pours whose logged visit always covered them: a path that found the loggers' clocks and cut
  the pours by the logged window kept 43 of 48 rainfall cells; the log now gives times to five minutes and departure
  as the van leaves, which a pour's tail often outlasts (35 of 48 on that path).
- 2026-11-07, RG-4's 0.2 mm mechanism from August 2025: it moved five cells; moved to 15 May 2025 (eight cells), the
  hour chosen so that no cell sits within 0.03 hundredths of a rounding edge.
- 2026-11-07, Northside returns at the first draw of Outfall 006's runoff: 2022 sat 0.02 MG from a rounding edge; the
  runoff factor moved from 9.5 to 9.9, every Northside year now 0.1 MG or more from an edge.
- 2026-11-07, the Northside plant at 110 MGD: its room bound the tank's pumps in a few hours, so the rating replay and
  the room replay could part at Northside; rated 125 MGD, the room never binds while the station pumps (asserted).
- 2026-11-07, Appendix C 1.3 saying flow above the headworks capacity is held back in the interceptor: it states the
  mechanism the decisive step recognises; cut to the plant's rating alone.
- 2026-11-07, the first ask layer at stage 3 (pours in about half the gauge-months, one gauge's 0.2 mm mechanism,
  the transducer alone on the Northside returns): the cracker kept 43.4 per cent of the ask weight and one crack (the
  loggers' clocks, or the pours by their run) kept 70, a pair near 67 if both top responses found it. Each figure a
  device moves now carries a second, independent reconstruction: the contract's monthly cal checks and every gauge's
  new mechanism from July 2025 on the same cells; SG-600's leak-by metered by FIT-600 on the same years as the
  transducer. The main call, the stump and every main-call figure frozen (freeze.py rubric PASS).
- 2026-11-07, the contract and the new mechanisms from January 2025: no device-free cell was left (the cracker kept
  0 of 53), harder than the ask layer needs and short of the third the asks aim at; moved to July 2025 (24.5 per cent
  kept, worst single crack 35.8).
- 2026-11-07, O&M Table 4-1 printed at 0.25 ft steps with levels to one decimal: the extracted table paired 0.25 ft
  rows with 0.2 ft labels; printed at 0.1 ft in the hopper, levels to two decimals and volumes to four, so the
  mass balance reproduces the delivered volume within 0.4 MG a year.
- 2026-11-07, the Northside tank's inflow added before its pumps ran in a quarter hour: a full tank sent the storm
  tail over the crest in the same quarter hour the pumps started, which no meter sees; the pumps now draw down while
  the trickle enters.
- 2026-11-07, judge round 1 forks on the rainfall ask: the month basis (Eastern civil time against fixed Eastern Standard
  Time, 0.03 in in March and April) closed by filing "on local Eastern time" in the asking sentence; the RG-1 install
  inside a rain spell on 8 July (0.09 in on which mechanism counted) closed by moving every install to a day without
  rain at its gauge, not by a sentence. Six cells moved by 0.01 in through the bucket remainder.
- 2026-11-07, the 2025 notices with the other outfalls' times copied from Clay Street's and one action string, work
  orders with stock texts on any asset, the field log authored by a technician from 2014 (the leak reader's realism
  read): each outfall's detector now lags and tails on its own, texts follow asset class and order type, and the
  contractor authored the log at its June 2025 mobilisation.
- 2026-11-07, the final-pack leak read's realism notes:
  - Outfall 014's notices started on the quarter hour, set apart from the others; every outfall now carries its
    detector's own trip and reset minutes, inside its first and last overflowing quarter hours.
  - The notices drew one shared pool of six actions; each outfall now has its own wording.
  - The four FIT-600 leak-by reports were one verbatim text; each now reads as a different operator wrote it.
  - The CMMS held only the assets the questions need; it now carries the authority's other pump stations,
    regulators, screens, standby generators and meters.
  - The field log was saved with inline strings and ten template notes; it now has shared strings and a wider pool of
    notes, drawn from a stream of its own so that no visit moves.
  - Pours are now found from the logged volume ("NNN mL"), because an abbreviated "Cal chk" note would otherwise pass
    unseen.
  - No graded figure moved.

- 2026-11-08, architecture 2 (the Clay Street tank sized by a replay bounded by Southside's hourly headroom): the
  platform's two runs both bounded the dewatering by the plant's headroom without prompting and filed Alternative C
  with every ask; a physical bound the files lay side by side is modelled on sight. The world is spent.
- 2026-11-08, draw stage: a strip aquifer whose test sees the walls and whose long record shows leakage (walls 3,400
  ft apart, leakage factor 6,000 ft): the test's derivative showed the walls inside a day and the leaky strip was
  identifiable from the test alone, so a run reading the plate could land the call without the record; walls 5,000
  ft apart with a 3,500 ft leakage factor cancel inside the test window (Theis residual 0.08 ft).
- 2026-11-08, draw stage: options at 500, 750, 1,000 and 1,350 gpm: the 500 and 1,350 gpm peaks sat within 0.1 ft of
  a rounding edge across the standing family; 450 and 1,300 gpm put every peak mid-bin.
- 2026-11-08, draw stage: calibrating on MS-MW and OW-S only left the OW-S-only rival at 1,300 gpm; the golden
  calibrates on every well the Mill Street wells measurably drew down (MS-MW, CV-07, OW-S), and OW-S alone is ruled
  out by its unidentified profile.
- 2026-11-08, build stage: 750 gpm sat 0.18 ft from a rounding edge once Cooper-Jacob transmissivities entered the
  family; the second schedule moved to 700 gpm (peak 5.96 ft). 1,300 gpm sat 0.01 ft from an edge; the top schedule
  moved to 1,250 gpm (9.92 ft).
- 2026-11-08, build stage: asks riding only the decisive step left the run that lands the call with every ask (pair
  ceiling 56); Rule WR-4 4.4's nearest domestic well (the walls decide it, the record does not) and MS-MW's
  like-for-like window give the landed run two second judgments (pair ceiling 46.8).

Architecture 3 (Reidel Road well field, Rule WR-4 sentinel drawdown):


- The far field calibrated on an existing well field's cone, read against natural levels from reference wells beyond
  the cone, with the nearest network well (CV-07) inside the cone as the trap: spent on the platform 2026-11-08. Both
  runs fitted a leaky strip with the plate's walls to the test itself (the far field was identifiable from the test once
  the mapped walls were honoured) and took CV-02 and CV-11 as controls by reflex, landing Schedule C and every ask
  (`runs/triage.md`). A physical mechanism the test rows carry, and a control choice the field makes by default, are
  both modelled on sight.

Architecture 4 (Sallow Road well field, the nitrate plant's loan cycle), while built:


- Ridge arrivals spread over 2029 to 2032 (first truth model): the first year at 10 moved between 2030 and 2032 with
  the arrival reading (quarter, half-way, three quarters of the rise); the ridge parcels' depths were set so every
  reading files 2031 (EP-01 5.8 to 9.0 in 2030, 10.6 to 12.3 in 2031), asserted in `checks.py` R4.
- Farmland parcels in the zones 8 to 19 years' groundwater travel away: one lag fitted to the wells' record came out
  at 9 to 10 years, long enough to put the ridge after 2026 and before 2034, so the single-lag route landed the call;
  the zones' farmland was moved near the wells on a shallow water table (one lag of 4.5 years, which puts the ridge
  at the wells by 2025 and is rejected by the 2019-2026 record), asserted R2.
- Mixing at the recharge that carried the nitrate from the root zone, with the model carried to the wells' level:
  in the truth an irrigated parcel's higher recharge pushes the old forest water out ahead of its nitrate, diluting
  Wells 6 and 7 before the rise, so that weighting reads the dilution as bias and sets the 2034 figures a whole mg/L
  low; the golden mixes at the recharge the parcel had when its water left the water table, and the other weighting
  is kept as the asks' second judgment (SF10).
- Parcel-to-parcel leaching spread of 7 per cent: each well's model was off its record by up to 1 mg/L and carrying it
  to the record moved the per-well figures across a rounding edge; set to 3 per cent, residuals under 0.35 mg/L.
- Each well's 2034 mean as an ask: Well 5 lands at 7 on every route, deep or shallow, so the default path kept a
  fifth of the ask weight; the ask is the well highest in 2034 and its mean, which the default path misses (Well 5).
- The data dictionary sheets (the network register's Fields sheet, the parcel attributes' Notes sheet, the age
  survey's Method sheet, house-fixes H9): removed; the age survey's Method sheet also said a production well's age is
  a mixture, a pointer the pack does not need.
- Tarrow County, Wexmoor and the Holcomb Road well field: one letter from Barrow County, containing Exmoor, and a real
  place name (house-fixes H21); renamed Ravell County, Corlinden and Sallow Road, every figure unchanged. Colin Hanna
  (a first name in a recent build, a surface BLOCK) became Patricia Gaines.
- The Utility Commission as the deciding forum: `guard.py heart` blocked `committee_or_panel` against task4 v4,
  registered four hours earlier and pulled in after this card's check; redrawn to the Common Council
  (`council_or_assembly`), which in Wisconsin authorises a municipal utility's borrowing, every figure unchanged.
- REVIEW, stump vocabulary in the wellhead plan (travel, recharge, wellhead, county, effect, weight): harmless, the
  words a wellhead delineation report is made of; it states the groundwater time of travel and recharge by land cover,
  and nowhere a delay above the water table, a conversion, or nitrate.
- The ridge's arrivals spread from 2030.6 to 2031.5 (the build's first cut): the stage 4 judge found the first year
  at 10 thin against a later reading of the arrival (a third of a year late put it in 2032) and Well 7's 2034 mean
  0.26 above the rounding line; the ridge parcels' depths and travel times were set so their arrivals cluster at
  2030.85 to 2030.92 (every reading from a half year early to a half year late files 2031) and Well 7's ridge acreage
  raised 7 per cent (15.92, and 15.85 at the low end of the vegetable leachate), asserted in `checks.py` R5.
