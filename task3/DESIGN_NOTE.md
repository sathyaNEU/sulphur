# task3 architecture 3: Reidel Road well field, Rule WR-4 sentinel drawdown

Physical & Environmental Sciences, hydrology (Sulfur task type: inverse problems, physical-model calibration and
uncertainty propagation), Forecasting & Predictive Modeling. Re-root of the slot after the platform landed
architecture 2 (both runs on the golden at every ask, `runs/triage.md`): one architecture per world, so a new world,
dataset and shell.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task3.json` v3, registered 2026-11-08 at PASS (differentiated against
  mark166, mark247 and mark308; lineage carries v1 and v2 with their fates).
- **Pairing:** a city water utility's groundwater withdrawal permit; the conservancy district's Rule WR-4 caps the
  drawdown at a sentinel well in every month of a twenty-year term; four requested schedules for a new well field in a
  buried-valley aquifer; the district permits the largest that meets the cap.
- **Shape:** a which-of-four with each schedule's 2046 peak drawdown, the existing well field's drawdown at its own
  monitoring well, a monthly forecast workbook and a demonstration PDF with the chart.
- **Strategy:** a forecast that has to earn its place (Part A, WORKS IN FORM) fused with a clean comparison (Part A,
  WORKS IN FORM): the far-field model is calibrated on the cone an existing well field has already drawn, and the
  drawdown that record carries is only clean against natural levels from reference wells beyond the cone.
- **Data-native sentence:** a confined valley aquifer whose no-flow walls and leaking till cap pull a three-day
  test's drawdown in opposite directions and cancel inside its window, beside seventeen years of an existing well
  field pumping into the same aquifer through a run of wet years, with the nearest network well sitting inside that
  well field's cone.
- **Abstraction sentence (written, then tested):** "a short trial's model fits the trial and is calibrated for the
  long run on a sibling load's history read against a reference outside that load's reach." Against every approved
  and delivered build in `guard.py mechanisms --objective forecasting`, no build's decisive step pairs an
  out-of-window calibration with a contaminated-reference choice; mark166 (departures linked across groups), mark247
  (gap-filled running sums), mark308 (unmet requests rebuilt from movements), mark138 (store at the forecast date) and
  mark156 (infiltration below a water table) each spend a different insight.
- **Sources** (all synthetic, authored for this task, CC0; `metadata.json`): the consultant's logger export for the
  14 to 17 September 2026 test at PW-1 (six wells, one-minute absolute pressure, two logger brands and clocks), the
  on-site barologger, the field-notes workbook, the August step test (distractor), Harlow Springs' monthly operating
  report extract 2009 to 2026, the Mill Street monitoring well's tape readings 2008 to 2026, the district's network
  water levels 2005 to 2026 and well register, Rule WR-4, the application's requested schedules, the drillers' logs,
  Plate 3 of the 2019 bedrock surface study (PNG), and the raw-water quality workbook (distractor).
- **People:** drawn with `guard.py names --geo US` (seeds 3303 and 3): Mitchell Munoz, Todd Robinson (test field
  crew), Wendy Ruiz, Mary Alvarez, John Ponce (Mill Street readers).

## Default path

1. Put the six loggers on one clock (the Level TROLLs on local EDT, the Leveloggers on UTC), subtract the barologger,
   take the OW-2 re-hang from the field notes, drop the rewritten records, and turn pressure into drawdown at PW-1's
   observation wells against the pre-test trend.
2. Fit Theis to OW-1, OW-2 and OW-3 (the field's method for a constant-rate test): T about 8,160 ft2/day, S about
   1.0e-3, residual 0.08 ft over three days, the late-time derivative flat (no boundary, no leakage visible).
3. Project the 2027 to 2046 drawdown at OW-S with that Theis aquifer and the requested schedules: nearly 22 ft even
   at 450 gpm, so the hindcast of the Mill Street wells is run to check it, and Theis puts 12 ft of 2025 drawdown at
   the Mill Street monitoring well where the record shows 3 to 5.
4. Recalibrate: a leaky aquifer (Hantush, with the plate's walls) whose leakage factor reproduces the Mill Street
   record, the drawdown at each monitoring well taken against the nearest network well in the same aquifer, CV-07,
   as the natural level (or against the well's own 2005 to 2008 mean, or with a fitted trend): leakage factor near
   1,900 ft, the record fitted closely.
5. Forecast with that aquifer: every schedule's 2046 peak at OW-S under 3.5 ft, all four within the 9 ft limit.

Ends on: 1,250 gpm
Golden: 1,000 gpm

## Stump sentence

A strong analyst who sees the test's Theis forecast overshoot the Mill Street record recalibrates the leakage on the
monitoring wells' drawdown read against the nearest network well CV-07 (or the wells' own pre-pumping levels, or a
fitted trend), puts every schedule under 3.5 ft at OW-S and files 1,250 gpm; CV-07 sits inside the Mill Street cone and
the region's wet years lift every reading, so only the natural level carried from the confined-aquifer wells beyond
the cone (CV-02 and CV-11) gives a leakage factor near 3,500 ft and files 1,000 gpm, 8 ft against 1,250 gpm's 10.

## Deep reasoning

- **Task type:** hydrology flood frequency is the vocab key; the Sulfur task type is inverse problems and
  physical-model calibration (the aquifer's far field calibrated on an existing record), serving forecasting.
- **Domain test:** the deciding quantity is a 20-year drawdown forecast at a sentinel well; the field's estimator is
  a pumping-test analysis (Theis or Cooper-Jacob type curves) carried forward by superposition of the schedule.
- **Swap:** "which schedule keeps the sentinel's drawdown within 9 ft" becomes "which price keeps churn within 9 per
  cent": there is no confined aquifer, no leakage through till, no no-flow wall and no cone of depression for a
  reference well to sit inside, so the reference choice and the far-field calibration stop meaning anything.
- **Layer 1:** two logger clocks (consultant's two brands), absolute pressure and the barologger, the OW-2 re-hang
  and the OW-3 rewritten records (download routine), the aquifer's barometric response and earth tides (physics),
  thousand gallons then gallons and the wells renamed at the 2016 SCADA change, the May 2019 meter month from run
  hours (operating reports), readings taken with TW-1 running and the 2017 casing extension (the town's tape
  readings), CV-07's 2013 measuring-point reset, keyed-twice rows, estimated readings and the 2020 months without a
  field run (the district's network); nothing is placed to be caught.
- **Layer 2:** forecast uncertainty: a far-field model that earns its place out of the test's window, calibrated on
  a record whose drawdown must be separated from natural variation with a clean reference.
- **Decisive step:** taking each monitoring well's natural level from the confined-aquifer network wells beyond the
  Mill Street cone, so that the drawdown the record carries is the pumping's alone and the leakage factor it
  calibrates is the aquifer's.
- **Not semantics:** every field, unit, clock and code read correctly (the readings, the measuring points, the
  operating report's units) still leaves a natural level to be chosen, and the nearest same-aquifer well, the
  well's own baseline and a trend each read the region's wet years as leakage.
- **Not rule application:** Rule WR-4 defines drawdown as the lowering the withdrawals cause and lists the records
  an application carries; no filed sentence names a reference well, a far-field model or a calibration. Enumerated
  family (Theis from the test; leaky or bounded leaky calibrated against own baseline, trend, CV-07, CV-02, CV-11,
  CV-02 and CV-11; walls 4,000 ft to none; T from any observation well) spreads the 1,000 gpm peak from 2.0 ft to
  34.4 ft; the standing family (the clean references, every wall width, every test fit) spreads it 7.95 to 8.29 ft,
  all filing 1,000 gpm; the ruling-out is loud in the data (CV-07's record steps down with each Mill Street increase
  and cycles with summer pumping; CV-02 and CV-11 agree with each other and with OW-S before 2009).
- **Analyst test:** a strong analyst compensates the loggers, fits Theis (an excellent fit), sees its hindcast
  overshoot the Mill Street record, recalibrates a leaky aquifer against CV-07 or the wells' own baselines and files
  1,250 gpm.
- **Estimand:** Rule WR-4 sections 1.2, 2.1, 2.2, 4.1 to 4.3 and Table 1 (the drawdown at OW-S caused by the
  Reidel Road schedule and the Mill Street wells at their filed projection, in every month through December 2046,
  against 9.0 ft; the largest schedule meeting it is permitted; 4.4 the nearest registered domestic well's 2046
  peak under the permitted schedule); the schedules and the projection in the application summary.
- **No decoy:** no memo, draft, briefing or stakeholder figure states a drawdown, a leakage factor or a reference
  well; the application carries schedules and projections only.
- **No certified replay:** no published or certified drawdown exists for the method to reproduce.
- **Chain:** (1) the test's Theis fit is exact inside three days but its hindcast of the Mill Street wells
  overshoots the record fivefold, so the far field must be calibrated on that record; (2) the record's drawdown is
  each reading's fall below its natural level, which only the confined-aquifer wells beyond the cone carry (CV-07
  is inside it, a trend absorbs the pumping); (3) the leakage factor that reproduces the separated drawdown at MS-MW,
  CV-07 and OW-S with the plate's walls; (4) the 2027 to 2046 monthly superposition at OW-S under each schedule and
  the town's projection, and the largest schedule under 9.0 ft.
- **Judgment:** which wells carry the natural level, justified from the data (CV-07's offset from the far wells
  steps with each Mill Street increase and follows the summer pumping; CV-02 and CV-11 move together and with OW-S in
  2005 to 2008), and which far-field model reproduces the separated drawdown that the test cannot see.
- **One-fact test:** the likeliest hint, "the aquifer leaks through the till", rescues nothing: the default path
  already calibrates a leaky aquifer, and on the CV-07-referenced or raw record it calibrates to 1,250 gpm. The
  hint "CV-07 is inside the cone" still leaves the reference to be built, the calibration and the superposition.
- **No replay:** the call is a forecast for 2027 to 2046; no shipped number is re-derived or wrong.
- **Pinned:** the rivals run on the cut pack (`generator/checks.py` R6): references CV-02, CV-11 or both; walls
  4,000, 5,000, 6,500 ft or none; T and S from OW-1, OW-2, OW-3, all three, or with PW-2 and OW-S; barometric
  correction on or off; calibration on MS-MW alone, or on MS-MW, CV-07 and OW-S. Every one files 1,000 gpm with the
  peaks at 4, 6, 8 and 10 ft. Calibration on OW-S alone (1,250 gpm) is ruled out by the record it leaves out: its
  leakage factor of 3,065 ft puts MS-MW's 2025 drawdown at 4.4 ft against the record's 4.9; the leaky fit to the test
  alone (700 gpm) misses MS-MW the other way (5.4 ft).
- **Run forecast:** a run first goes wrong by a method shortcut (Theis extrapolated, filing none of the four) or,
  more likely for a strong run, a self-confirming check: it calibrates the leakage on the record against CV-07 or
  its own baseline, the fit reproduces the record, and it files 1,250 gpm; a run that notices the wet years and fits
  a trend is dismissing its own evidence (the far wells).
- **Strategy label:** WORKS IN FORM (a forecast that has to earn its place, live form: the invariant constructed from
  a log, the back-test the solver's own; and a clean comparison whose contamination is read from a relation in the
  data, never a column).
- **Lesson:** a model whose fit inside the trial is excellent can still be wrong for the decision's horizon, and an
  out-of-window calibration is only as clean as the reference that separates the signal from the background; no
  build on file couples the two.

## Survivor anatomy

- **Actor:** the monitoring readings have rows; the property that decides (which wells sit inside the Mill Street
  cone, and so carry the natural level and which do not) is a relation between the network wells' series and the
  Mill Street pumping, held in no column; the register's unit code says only that CV-07, CV-02 and CV-11 are all
  in the confined aquifer.
- **Link:** the natural level is read by comparing network wells' records with each other and with the operating
  reports, a comparison the pumping-test method never asks for and no key offers.
- **Reflex:** Theis on the test (rung 0) and a leaky aquifer calibrated on the record against the nearest reference
  (rung 1) both file a wrong answer (none of the four; 1,250 gpm).
- **Back-test:** the textbook routes validate: Theis fits the test to 0.08 ft; the CV-07-referenced calibration
  reproduces the Mill Street record it was calibrated on.
- **Second use:** every file the decisive step reads has its own use: the network export and register are what Rule
  WR-4 3.2 supplies to every applicant and carry the sentinel OW-S; the Mill Street records are the existing
  permitted withdrawal the demonstration must include; the operating reports give that withdrawal's history.
- **Shock:** the wet years are ordinary weather in a 22-year record, and CV-07's offset (about 1.7 ft by 2025) grows
  with the town's slow growth, never a step or the pack's largest anomaly.
- **Pins:** the WHAT sits in Rule WR-4 (drawdown, existing withdrawals at their filed projection, every month of a
  term ending 2046, Table 1's 9.0 ft, the largest schedule permitted) and the application (schedules, projection);
  no sentence names a reference well, the leakage, the walls' role or a calibration window.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 Theis from the test | no | no | yes | no | no | no | no | readable |
| 1 Leaky calibrated against CV-07, own baseline or trend | no | no | yes | no | no | no | no | readable |
| 2 Natural level from CV-02 and CV-11 beyond the cone (decisive) | no | no | no | no | no | no | no | silent |
| 3 Superposition of the schedules and the projection | no | no | yes | no | no | no | no | readable |

## Semantic fork table

| Id | Term or convention | Reading A (golden) | Reading B | Golden under A | Under B | Ruled out by |
|---|---|---|---|---|---|---|
| SF1 | drawdown at OW-S | caused by withdrawals (Rule 2.1) | the reading's fall from 2005 to 2008 | 1,000 gpm | 1,250 gpm (raw rung) | Rule WR-4 2.1, "caused by withdrawals" |
| SF2 | existing withdrawals in the future | the filed projection, 56 and 44 per cent | the 2025 rate held | 1,000 gpm | not computed | Rule WR-4 2.2 files the holder's projection |
| SF3 | which month counts | greatest monthly drawdown in 2046 (4.3) and every month (4.1) | annual mean | 1,000 gpm | 1,250 gpm | Rule WR-4 4.1 "any month" and 4.3 "greatest monthly drawdown" |
| SF4 | walls | the plate's mapped edges, 5,000 ft | none, or 4,000 to 6,500 ft | 1,000 gpm | 1,000 gpm | same call (asserted) |
| SF5 | T and S | Theis on OW-1 to OW-3 | any single well, or five wells | 1,000 gpm | 1,000 gpm | same call (asserted) |
| SF6 | readings with TW-1 running | dropped | kept | 1,000 gpm | 1,000 gpm | same call (asserted) |
| SF7 | the natural reference | CV-02 and CV-11 | either alone | 1,000 gpm | 1,000 gpm | same call (asserted) |
| SF8 | the term's start | April 2027 per the application | January 2027 | 1,000 gpm | not computed | application section 1 files April 2027 |
| SF9 | walls for the domestic well | the plate's mapped edges | none (the record fits either way) | DW-17 7 ft | DW-17 6 ft | Plate 3 maps the edges of the saturated sand and gravel |

## Ladder

- **Rungs and winners:** rung 0 Theis from the test files none of the four (450 gpm at 21.7 ft, the Mill Street wells
  alone over the limit by 2046); rung 1 leaky calibrated against CV-07 files 1,250 gpm (peak 3.4 ft), against the
  wells' own baseline 1,250 gpm (2.4 ft), with a trend 1,250 gpm (2.5 ft), against CV-07 averaged with the far wells
  1,250 gpm (7.2 ft); the decisive rung (CV-02 and CV-11) files 1,000 gpm at 8.12 ft, 1,250 gpm at 9.92 ft. Off the
  ladder: the leaky fit to the test alone files 700 gpm, annual averages in place of the monthly schedule 1,250 gpm.
- **Margins:** the golden's 1,000 gpm peak sits 0.88 ft under the 9.0 ft limit and its 1,250 gpm peak 0.92 ft over;
  every standing rival keeps 1,000 gpm at 7.95 to 8.29 ft and 1,250 gpm at 9.72 to 10.12 ft.
- **Pricing:** (1) the residue the WHAT leaves is the natural level, a method; (2) the move the call needs (1,250 gpm
  from 3.4 ft to over 9.0) is a factor of 2.6 in the far-field response, which the reference choice produces; (3)
  the one-group-by route (difference to the nearest same-aquifer well) is the rung 1 shortcut; (4) the leakage
  factor's spread across the clean references and test fits is about 4 per cent (3,457 to 3,584 ft) against the 47
  per cent the reference choice moves it; (5) no variance is the lever; (6) OW-S's own record carries 0.5 ft of
  Mill Street drawdown, so OW-S alone cannot carry the calibration (asserted through the MS-MW miss); (7) no subset
  of rows hands over the leakage factor; (8) every visible grouping of the network (unit code, distance, record
  length) was swept as a reference and only the beyond-the-cone confined wells land the call.
- **Dominance:** each lower rung's single correction leaves it on a wrong answer (R3b in `checks.py`).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 population | the sentinel OW-S, Table 1 | filed in Rule WR-4 |
| 2 outcome | drawdown caused by withdrawals | Rule WR-4 2.1 |
| 3 window | every month through December 2046 | Rule WR-4 1.2 and 4.1 |
| 4 unit | feet, nearest foot | prompt |
| 5 comparison | each schedule against 9.0 ft | Table 1 |
| 6 existing withdrawals | the Mill Street wells at the filed projection | Rule WR-4 2.2, application section 3 |
| 7 schedule shape | the monthly factors | application section 2 |
| 8 start | April 2027 | application section 1 |
| 9 split of the new field | equal between PW-1 and PW-2 | application section 1 |
| 10 split of Mill Street | 56 and 44 per cent | application section 3 |
| 11 test rate | totalizer average | field notes |
| 12 clocks | per logger | field notes, Loggers |
| 13 re-hang | per logger | field notes, Loggers |
| 14 measuring points | MP history | register |
| 15 units of production | per row | operating report column |
| 16 aquifer geometry | the mapped edges | Plate 3 |
| 17 natural level | beyond the cone | the data (decisive) |
| 18 far-field model | calibrated on the record | the data (decisive) |
| 19 rounding | nearest foot | prompt |
| 20 tie at the limit | none within 0.9 ft | asserted |
| 21 largest permitted | the largest meeting 4.1 | Rule WR-4 4.2 |
| 22 as-of | 6 November 2026 | the application's date and the data's end |

## Literal reader

Executing Rule WR-4 and the application word for word gives the estimand (OW-S, every month through 2046, the
schedules plus the Mill Street projection, 9.0 ft, the largest passing schedule) and leaves the far-field model and
the natural level to the data; every reading of the filed sentences that the data leave standing files 1,000 gpm.

## Oracles

none: no control, published figure or corpus ties under any basis; the network wells are evidence, not a scored
bench, and the far wells agree with each other on every basis.

## Ask sheet

- **Asks:** (A1) each schedule's greatest monthly drawdown at OW-S in 2046, nearest foot (4, 6, 8, 10); (A2) the
  2025 average drawdown the Mill Street wells caused at MS-MW, nearest foot (5); (A3) the greatest monthly drawdown
  in 2046 at the nearest registered domestic well (DW-17) under the permitted schedule, nearest foot (7); the
  demonstration PDF with the 2027 to 2046 chart against the limit and the workbook's monthly working (instruction
  following).
- **Devices:** every graded figure rides the decisive step (A1 moves with the leakage factor; A2 with the natural
  reference; A3 with both), and A2 and A3 each carry a second judgment of their own: A2 the like-for-like window (the
  far wells' change measured from MS-MW's own pre-pumping months, not from 2005 to 2008: 4.4 ft, rounding to 4), A3
  the plate's walls (left out, the record still fits and DW-17 reads 5.8 ft, rounding to 6).
- **Spans:** A1 across the standing family 4.05 to 4.26, 5.83 to 6.09, 7.95 to 8.29, 9.72 to 10.12 ft; A2 4.87 to
  4.93 ft; A3 across the plate's readings (walls 4,500 to 5,500 ft) 6.59 to 6.92 ft.
- **Pair ceiling:** 46.8 (the cracker lands the call and A1 but takes both second judgments' shallow forms, 81.7; the
  mirror on rung 1, 12.0).
- **Mirror leakage:** 0 per cent of ask weight kept by the default path.
- **Measured by:** generator/ceiling.py

| Ask | Golden | Default path (rung 1, CV-07) | Cracker (deep step, shallow second judgments) | Verdict |
|---|---|---|---|---|
| A1 450 gpm | 4 | 1 | 4 | yes |
| A1 700 gpm | 6 | 2 | 6 | yes |
| A1 1,000 gpm | 8 | 3 | 8 | yes |
| A1 1,250 gpm | 10 | 3 | 10 | yes |
| A2 MS-MW 2025 | 5 | 3 | 4 | miss |
| A3 DW-17 2046 | 7 | 2 | 6 | miss |

## Prompt contract

The author's rewrite keeps: the question (which schedule the district will permit under Rule WR-4, no count of the
schedules); OW-S, the Table 1 limit and 2027 to 2046; `reidel_road_WR-4_demonstration.pdf` with the chart of each
schedule's monthly drawdown at OW-S against the limit; `reidel_road_sentinel_forecast.xlsx` with the monthly
working for every schedule; each schedule's greatest monthly drawdown at OW-S in 2046; the Mill Street wells'
drawdown at the Mill Street monitoring well as a 2025 average; the greatest monthly drawdown in 2046 at the nearest
registered domestic well under the permitted schedule; drawdowns to the nearest foot. The as-of is the
application's date, 30 October 2026, with data to September 2026.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call rests on the natural reference and the far-field
  calibration (R3a, R3b, R4 asserted); no field reading, filed procedure or planted catch decides it (the leak reader
  answered Q6 analytical); the one-fact hint leaves the default path on 1,250 gpm (R5).
- Free gates on the final cut: checks 132 of 132, the verifier, byte-identical rebuild, precut 72 of 72, figures_check
  63 of 63, leak.py REVIEW (no LEAK; the schedules, limit and clauses filed as stated inputs), guard heart PASS and
  surface exit 0 (names WARN on place names only).
- Stage 4: the leak reader found no step named, no ranking file and no helper file; the plate's machine-made note
  removed. The determinism judge's verdict is recorded in determinism_check_report.md.

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
