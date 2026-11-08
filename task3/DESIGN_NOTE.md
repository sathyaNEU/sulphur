# task3 architecture 5: Kinnard Road culvert on Ollery Creek, the 1 per cent flood of its first decade

Physical & Environmental Sciences, hydrology-flood-frequency (Sulfur task type: extreme-value and environmental-hazard
return-period analysis), Forecasting & Predictive Modeling. Re-root of the slot at the author's word after the
platform landed architecture 3 (both runs on the golden at every ask, `runs/triage.md`); architecture 4 (a nitrate
forecast) was rolled back unrun. One architecture per world, so a new world, dataset and shell. Architecture 3's
design sections are in git history at 1fffdf5, architecture 4's at 0931661.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task3.json` v5, registered 2026-11-08. `guard.py check` on the filed card:
  WARN only. `overuse.objective` (forecasting in 8 of the last 12): the slot's assigned objective. `repeat.deliverables`
  (csv and docx, against task9 v6): a design-flow memo and the peak table a hydraulics reviewer re-runs are the
  analyst's own pair here; the shell differs in question form and roles. Three axes were redrawn from the first draft
  for honest reasons, not to pass: the decisive generator is G6 (the population the flood record was drawn from
  shifted under it; G14 repeated task7), the forcing event is the state floodplain review of the crossing's hydraulic
  design (the budget repeated task7), and the decisive gap is population (the record's floods come from a watershed
  that no longer exists; time against G6 repeated task6's lineage).
- **Pairing:** Tamsett County's roads division replaces the failing culvert where Kinnard Road crosses Ollery Creek;
  the county's drainage standard requires a crossing to pass the 1 per cent annual exceedance peak flow of its first
  ten years of service without overtopping the road; three box culverts are costed, rated by the division's hydraulic
  model at 8,500, 14,000 and 19,500 cfs; the call is the smallest that passes.
- **Shape:** 04, setting one dial (the culvert) among allowed settings, with the frequency curve's quantiles, the
  crossing's overtopping odds and the peak table the state reviewer re-runs.
- **Strategy:** separating two explanations for one pattern (Part A, WORKS IN FORM, the live form: a like-for-like
  comparison rebuilt from history, no dated cutover, no filed sentence naming the split). The two explanations for a
  flood record that looks stationary are a watershed that never changed and a watershed whose response rose while its
  storms fell; only each flood set against the storm that made it separates them.
- **Data-native sentence:** a Piedmont creek gauged since 1956 whose watershed went from farms and woodlots to
  subdivisions with storm drains between 1975 and 2010 (the paved fraction 6 to 30 per cent, the time to peak nearly
  halved), while the storms of 1990 to 2025 ran about a fifth lighter than those before; in the annual peaks the two
  cancel, so the trend test, the outlier test and the frequency fit all pass on a record drawn from a watershed that no
  longer exists.
- **Abstraction sentence (written, then tested):** "a rare-event level read from a record whose response to its driver
  rose while the driver weakened, separated by pairing each event with its driver and re-running the whole driver
  record through today's response." Against `guard.py mechanisms --objective forecasting` and every lineage driver: the
  nearest (0.11, mark182 v1 lineage) carries a shared driver through each unit's own lag to read a change; none prices
  a rare-event level from a record whose response and forcing moved in opposite directions.
- **Domain fit (the user's swap test, run on the sentence):** "which culvert passes the 1 per cent flood of its first
  ten years" with any other field's nouns loses the rainfall forcing, the rainfall-runoff response, the lag shortened
  by storm drains and the exceedance probability of an annual peak flow; nothing is left to compute.
- **Prototype** (scratch `proto3.py`, 2026-11-08): on most seeds the Mann-Kendall p on the annual peaks is 0.13 to 0.70;
  the stationary family (Bulletin 17C log-Pearson III and an L-moment GEV on all 70 peaks, the post-1995 peaks alone,
  the peaks regressed on the paved fraction) files 5,800 to 8,000 cfs; the deep-step family (each storm's flood
  regressed on its depth and the paved fraction, storms above 1.0, 1.5 or 2.0 inches or the annual-maximum pairs
  only, log-Pearson III or GEV) files 9,800 to 13,000; the build's seed is chosen so both families clear their
  culvert's rating by 1.15.
- **People:** drawn with `guard.py names --geo us --locale en_US --seed 517`: Lisa Horne, James Reynolds.

## Default path

Every figure is built by `generator/analysis.py` from the shipped pack and asserted in `generator/checks.py` (seed 96).

1. Read the Drainage Standard section 4: the design flow is the peak with a 1 per cent chance of being equalled or
   exceeded in any year of the crossing's first ten years (4.2), estimated from the full length of the gauge's record
   with the county's other records (4.3); the least costly alternative whose capacity reaches it is recommended (4.5).
2. Read the three alternatives' capacities (7,460, 13,380 and 18,720 cfs) from the roads division's memo.
3. Take the gauge's 70 annual peaks (water years 1956 to 2025), check them the field's way: Kendall's tau 0.02,
   p = 0.79, no trend; no low outliers; the log-Pearson III fit (moments of the base-10 logs, the station skew) sits on
   the Weibull plotting positions.
4. The 1 per cent flow is 5,090 cfs (the generalized extreme value gives 5,300), under Alternative A's 7,460 cfs.

Ends on: Alternative A (5,090 cfs).

Golden: Alternative B (10,570 cfs on today's watershed).

## Stump sentence

A strong analyst fits Bulletin 17C's log-Pearson III to the 70 annual peaks, finds no trend (p = 0.79) and files
Alternative A at 5,090 cfs; the peaks since 1995, the peaks regressed on the paved fraction or detrended in time keep it
there (at most 5,870 cfs), because the lighter storms since 1990 offset the paved watershed's faster floods in the
annual maxima; only setting each flood against the storm that made it (the peaks above base paired with the rain
gauge's storm totals, the response's rise with the paved fraction read at a fixed storm) and putting every year's peak
on today's watershed files Alternative B at 10,570 cfs.

## Deep reasoning

- **Task type:** physical-environmental-sciences `hydrology-flood-frequency`, which serves Forecasting & Predictive
  Modeling: the design flood of a crossing's coming decade from a gauged record (Sulfur task type: extreme-value and
  environmental-hazard return-period analysis).
- **Domain test:** the deciding quantity is the 1 per cent annual exceedance peak flow at Kinnard Road for 2027 to
  2036; the field estimates it with a frequency distribution fitted to annual peak flows (log-Pearson III under
  Bulletin 17C, or the generalized extreme value), which assumes the record is homogeneous; replace the frequency curve
  of the record with any generic summary and there is no exceedance probability to read.
- **Swap:** "which culvert passes the 1 per cent flood of its first ten years" becomes "which warehouse passes the 1
  per cent peak of its first ten years of orders"; orders have no storm that makes them, no watershed response, no lag
  shortened by drains and no rain gauge to pair against, so the sentence stops making sense.
- **Layer 1:** the rain gauge's 1987 move with two months on both sites, observers' weekend readings accumulated into
  Monday's through 1978, trace codes and missed days (the climate office's export); the peak listing's 2009 and 2010
  water years exported twice and its estimate codes (the gauge's data unit); split parcels carried under both numbers
  after the 2004 reassessment and every basin of the county on one bill (the stormwater utility); the daily
  discharge's provisional months, ice and equipment days (the data unit). Each is the systems' own, none is placed to
  be caught, and each careful handling gives the same call (SF1 to SF4).
- **Layer 2:** forecast_uncertainty, a design flood from a record that is not homogeneous: the response of the
  watershed rose through the record while its storm climate fell, so the frequency curve of the record describes a
  watershed that no longer exists; the choice that flips the call is whether each flood is read against its storm.
- **Decisive step:** separating the watershed's response from the storm climate by pairing each peak above base with
  the rain gauge's total for its storm, reading the rise of the log peak with the paved fraction at a fixed storm
  (2.96 per unit), and putting each year's annual peak on today's watershed before fitting the frequency curve.
- **Not semantics:** every field read correctly (the gauge in service, Monday accumulations spread, the duplicate peaks
  once, split parcels once, water years as the standard's years, the capacities as filed) still files Alternative A
  on the record fitted as it stands; no column, code or definition changes when the floods are read against storms,
  because no file stores a storm's flood response or the watershed's change.
- **Not rule application:** no filed rule says how the record is used beyond its full length; executing section 4
  word for word leaves the estimator open. The enumerated family (the record as it stands, the peaks since 1995 or
  2005, the peaks regressed on the paved fraction, the peaks detrended in time, each in log-Pearson III and the
  generalized extreme value; and every pairing of peaks with storms in windows of two to four days, storms of half an
  inch to three inches, the annual peaks against their own storms, decade effects) spans 3,750 to 11,250 cfs and files
  A or B; the standing family (the pairings, which the record's own storm totals license) spans 9,570 to 11,250 cfs and
  files B in every member; the ruling-out is quiet: the storms since 1990 are lighter in the rain gauge and the same
  storm makes about twice the 1960 peak, both visible only once the two records are set side by side.
- **Analyst test:** a strong analyst who reads every record and rule correctly, fits the 70 annual peaks under
  Bulletin 17C, finds no trend (p = 0.79) and no outlier, and confirms the fit on the plotting positions files
  Alternative A at 5,090 cfs, the default path's `Ends on:`.
- **Estimand:** Drainage Standard 4.2 and 4.3 in `tamsett_drainage_standard_section_4.docx`: the peak discharge with a
  1 per cent chance of being equalled or exceeded in any year of the crossing's first ten years of service, from the
  full length of the gauge's record with the county's other records for the watershed.
- **No decoy:** nothing is planted to be caught: the offset is the storms' own run of lighter decades and the
  subdivisions' own drains; no document states a design flow, a trend, a response or a ranking, and the inspection,
  the cross sections, the grab samples and the daily discharge are records the county keeps that the solution never
  reads.
- **No certified replay:** no shipped figure is a design flow or a frequency estimate; nothing certifies a route.
- **Chain:** (1) the 70 annual peaks look homogeneous, so the question is whether the watershed and the storms each
  stayed put; (2) the rain gauge shows the storms since 1990 lighter, so a flat flood record with lighter storms means
  the response rose; (3) pairing each peak above base with its storm's total and reading the log peak against the
  paved fraction at a fixed storm measures the rise (2.96 per unit, about twice the 1960 peak); (4) every year's peak
  put on today's watershed and refitted gives the 1 per cent flow (10,570 cfs), so Alternative B, the four largest
  floods 1968, 1983, 1978 and 1962.
- **Judgment:** separating two explanations for one flat record (a watershed that never changed, or one whose
  response rose while its storms fell) by a like-for-like comparison: the same storm's flood across the decades,
  justified from the paired records, then a frequency model of a record made homogeneous on today's watershed.
- **Hidden by:** two effects offsetting inside the observed window: the paved fraction's rise from 6 to 30 per cent and
  the storms' fall since 1990 cancel in the annual maxima (Kendall p = 0.79), so the trend test, the outlier test and
  the fit all pass; the pairing that shows the change needs two files no key joins.
- **After the notice:** a run that suspects the paving still owes (1) reading the change at a fixed storm, where the
  easy turns (the annual peaks regressed on the paved fraction, 5,460 cfs, or detrended in time, 5,670) keep the storms'
  fall inside the estimate and stay on A; and (2) carrying the measured rise to every year of the record and refitting,
  where truncating to the developed years (since 1995: 4,300) or to today's storms only (since 1991: 4,490, ruled out
  by 4.3) lands on A.
- **One-fact test:** the likeliest hint, "the watershed has urbanized", still leaves a run to find that the annual
  peaks do not show it, decide the storms are hiding it, pair two records no key joins, read the rise at a fixed storm
  and rebuild the record; told it, the obvious moves (regress the peaks on the paved fraction, keep the recent years)
  stay on A.
- **No replay:** the call re-derives no published figure and no stated number is wrong.
- **Pinned:** every rival a careful analyst would run is run in `checks.py`: the stationary family (ten members) files
  A; the pairing family (32 members, windows, storm sizes, annual pairs, decade effects, two distributions) files B;
  only-the-recent-storms routes file A and are ruled out by 4.3's full length (SF13); each Layer 1 reading lands on B
  (SF1 to SF4, SF9, SF11).
- **Run forecast:** a run that applies the field's method stops at a method shortcut (the record fitted as it stands,
  no trend found) and files A at 5,090 cfs; a run that suspects the paving and regresses the peaks on it dismisses its
  own evidence (no significant slope) and stays on A; a run that pairs the records lands B.
- **Strategy label:** WORKS IN FORM (separating two explanations for one pattern; the live form: a like-for-like
  comparison rebuilt from history, no dated cutover, no filed sentence naming the split).
- **Lesson:** a flood record can look stationary because its watershed and its storms moved in opposite directions;
  the trend test on the maxima cannot see it, and only each flood against its storm separates the two; no build on
  file prices a design flood from a record whose response and forcing offset.

## Survivor anatomy

- **Actor:** the deciding property is each flood's response to its storm, which no column stores: it is a relation
  between a row of the peak listing and the rain gauge's rows for the same days.
- **Link:** the peaks and the storms share no key; the link is a date window (the peak day and the days before) across
  two agencies' exports, and the paved fraction is a third file's parcels summed by year; no sentence invites it.
- **Reflex:** the field's method (log-Pearson III under Bulletin 17C on the annual peaks, with its trend and outlier
  checks) sits at rung 0 and files A.
- **Back-test:** the textbook route validates: no trend (p = 0.79), no low outliers, the fit on the plotting positions.
- **Second use:** every file the decisive step reads is in the folder for its own reason: the rain gauge is the
  county's climate record, the peak listing is the gauge's publication, the parcels are the stormwater bill.
- **Shock:** the change reads as ordinary: the record's largest flood is 1990's, the recent decades look like the
  early ones, and the storms' fall is a decade-scale dry spell of the kind the Piedmont's records carry.
- **Pins:** the WHAT sits in the county's drainage standard (4.2 the probability, the window and the overtopping
  criterion; 4.3 the full length of the record; 4.5 the least costly passing alternative); no filed sentence names
  the paving, the storms, a pairing, a trend or a response.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the record fitted as it stands | 4.3 names the gauge's record | the peak file | yes, Bulletin 17C | the trend test passes | no | yes | no | readable |
| R1 the developed years only | none | the peak file | yes, a homogeneous subset | none | no | yes | no | readable |
| R2 the peaks regressed on the paved fraction or on time | none | parcels summed by year | yes, a covariate adjustment | slope not significant | no | yes | no | readable |
| R3 (decisive) each flood against its storm, the record put on today's watershed | none: no sentence names a storm, a pairing or a response | no key joins a peak to a storm | no: the reflex adjusts the maxima | none: the maxima's checks pass on R0 | no | no: a pairing across files, a regression at a fixed storm, a rebuild and a refit | no: the rain gauge, the peak listing and the parcels are the county's own records | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives and their call | Ruled out by |
|---|---|---|---|---|
| SF1 | the rain gauge across its 1987 move | the gauge in service, the old site to 14 June 1987 | the new site's overlap readings: B | same call, asserted |
| SF2 | weekend readings accumulated into Monday's | spread over the days covered | left on Monday: B | same call, asserted |
| SF3 | the 2009 and 2010 peaks exported twice | counted once | counted twice: B | same call, asserted |
| SF4 | split parcels under both numbers | counted once | counted twice: B | same call, asserted |
| SF5 | the storm total's window | the peak day and the two days before | two or four days: B | same call, asserted |
| SF6 | the storms paired | an inch or more | half an inch to three inches: B | same call, asserted |
| SF7 | the frequency distribution | log-Pearson III, station skew | the generalized extreme value: B | same call, asserted |
| SF8 | the rise's estimator | the regression on the paved fraction | the annual peaks against their own storms, decade effects: B | same call, asserted |
| SF9 | the service years' watershed | the 2025 watershed | the paved fraction carried to 2036: B | same call, asserted |
| SF10 | the years of the record | water years (October to September), as the peak file publishes them | none | 4.3, the gauge's record |
| SF11 | when a parcel's impervious area counts | from the year built | from the year after: B | same call, asserted |
| SF12 | rounding | the design flow to the nearest ten cfs | the nearest hundred: B | same call, asserted |
| SF13 | the storms the estimate stands on | the full record's | only those since 1981, 1991 or 2001 (B, A, A) | 4.3 ("the full length of the gauge's record") |

## Ladder

| Rung | Construction | 1 per cent flow (cfs) | Pick | Dies to |
|---|---|---|---|---|
| R0 | the 70 annual peaks fitted as they stand (log-Pearson III; GEV 5,300) | 5,090 | A | the storms' fall hiding the response's rise |
| R1 | the peaks since 1995 or 2005 only | 3,750 to 4,530 | A | the developed years are the dry years; 4.3's full length |
| R2 | the peaks regressed on the paved fraction or detrended in time | 5,460 to 5,870 | A | the storms' fall stays inside the slope |
| R3 | each flood against its storm, the record on today's watershed (golden) | 10,570 (family 9,570 to 11,250) | B | |

Margins: every stationary rung and the record's largest flood (4,510 cfs) sit 1.27 under Alternative A's 7,460; the
golden family sits 1.28 over it and 1.19 under Alternative B's 13,380. Seed 96 from a sweep of 300 (scratch
`scan6.py`), chosen for the widest joint margin with the trend test over p = 0.3 and the four largest stable across
the family.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the floods of the crossing's first ten years of service | filed 4.2 |
| 2 | Unit of account | the annual peak flow (cfs) | filed 4.2, the peak file |
| 3 | Attribution window | a flood to its water year | the peak file; SF10 |
| 4 | As-of dating | the records as exported in January 2026 | metadata; one export each |
| 5 | Version basis | approved and provisional flows alike; peaks as published | C1, the daily flows unread |
| 6 | Denominator | none: a quantile | C1 |
| 7 | Weighting | each year's peak once | C1 |
| 8 | Window length | the full record, 1956 to 2025 | filed 4.3; SF13 |
| 9 | Boundary inclusivity | equalled or exceeded | filed 4.2 |
| 10 | Rounding path | flows to the nearest ten cfs, compared unrounded | prompt; SF12 |
| 11 | Tie-break | the least costly passing alternative | filed 4.5 |
| 12 | Maturity and censoring | the peak listing's 50 cfs base below every paired storm's flood | the paired storms an inch or more; SF6 |
| 13 | Order of operations | clean, pair, regress, rebuild, fit | C1, each order gives the same rebuild |
| 14 | Row order | file order | C1 |
| 15 | Duplicate resolution | the duplicate peaks and split parcels once | SF3, SF4 |
| 16 | Identity normalisation | the rain gauge across its move | SF1 |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | cfs, inches, square feet over the basin's square miles | the files' own units |
| 19 | Code and status semantics | estimate codes kept as peaks; A, A3, T and M rain flags | SF2 |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | section 4 for a stream over one square mile | filed 4.1 |
| 22 | Forward window contents | the 2027 to 2036 watershed as 2025's | SF9 |

## Literal reader

Executed word for word, section 4 gives the golden: 4.2 asks for the peak with a 1 per cent chance in each year of the
first ten years of service, which is a property of the floods the culvert will meet; 4.3 sends the estimate to the
full gauge record and the county's other records; the record's floods came from a watershed that the parcels show
changed and whose same-size storms now make twice the flood, so the record must be put on today's watershed before
its curve speaks for the service years. Readings that differ fit the record as if its floods were today's (R0 to R2),
or drop part of it, which 4.3 rules out (SF13).

## Oracles

- The trend and outlier tests on the annual peaks: pass on every route; they confirm nothing.
- The plotting positions: every frequency curve sits on its own series' positions.
- No shipped figure is a design flow, a frequency quantile, a response or a ranking.

## Ask sheet

Four asks besides the call, every one read off the series the estimate rests on, so a run that fits the record as it
stands files a different value in every cell; the run that takes the deep step keeps them, since the pack carries no
second judgment the asks could ride without opening a fork.

**Ask 1: the design flow** (1 figure, nearest ten cfs). Golden 10,570 cfs; the family 9,570 to 11,250, stated as
that band in the answer blocks; the default path 5,090.

**Ask 2: the largest flood in the table the estimate rests on** (1 figure, a water year). Golden 1968 on every member
of the family; the recorded table names 1990.

**Ask 3: the four largest in order** (4 positions). Golden 1968, 1983, 1978, 1962 on every member; recorded 1990,
1983, 1968, 1978. The fourth and fifth largest sit 3 per cent apart, so the ask stops at four.

**Ask 4: the table the estimate rests on** (70 rows). Graded through the four largest years' rows inside the family's
band; the default path files the recorded peaks.

| Path (cracker = lands the call, runs the battery, executes filed documents) | Design flow | Largest year | Four largest | Table rows | Verdict |
|---|---|---|---|---|---|
| landed | 1 | 1 | 1 | 1.00 | keeps |
| shallow (recorded peaks) | 0 | 0 | 0 | 0.00 | miss |
| rung 2 (peaks regressed on paved fraction) | 0 | 0 | 0 | 0.00 | miss |

Shallow keep: 0.0 per cent of ask weight.

Pair ceiling: 56.0 (landed 100.0, shallow 12.0). Above the paper target of 50: the landed run has no second judgment
left on these asks; one could be added only by an ask whose figure the family does not pin, which would open a fork.

Measured by: generator/ceiling.py, run on the cut pack.

## Prompt contract

What a voice rewrite of `prompt.txt` may not drop or change:
- The question: which box culvert costed for the Kinnard Road crossing of Ollery Creek the county should build.
- The criterion: the road may not overtop in the flood with a 1 per cent chance of being equalled or exceeded in any
  year of the culvert's first ten years of service.
- kinnard_road_culvert_design_flow.docx: the design flow and the culvert; the flood frequency charted against each
  costed culvert's capacity; the water year whose flood is the largest in the table of annual peaks the estimate rests
  on, and the four largest in order.
- ollery_creek_design_peak_table.csv: that table, a row per water year.
- Rounding: flows in cubic feet per second to the nearest ten.
- No word for paving, urbanization, storms, rainfall, pairing, trend or adjustment; no count of the alternatives.

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
- 2026-11-08, architecture 3 (Reidel Road, the sentinel forecast calibrated against a clean natural reference): the
  platform's two runs both fitted the leaky strip with the plate's walls and took the remote wells beyond the cone as
  the control by default, landing 1,000 gpm and every ask; a hydrogeologist's default control is no stump. The world is
  spent.
- 2026-11-08, architecture 5 draw: mixed flood populations (snowmelt against rain floods) set aside, because one
  group-by of the peak file's dates shows the two seasons and the runs model a structure one group-by displays;
  historical-flood censoring set aside, because the expected-moments treatment of a perception threshold is the
  field's flagship method and is executed by reflex.
