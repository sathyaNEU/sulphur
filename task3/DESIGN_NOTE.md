# task3 architecture 6 (revision 2): the Durrow Creek bridge on Ransom Bar Road, an ungauged foothill creek's 1 per cent flood

Physical & Environmental Sciences, hydrology-flood-frequency (Sulfur task type: extreme-value and environmental-hazard
return-period analysis), Forecasting & Predictive Modeling. Re-root at the author's word: a total rework of the slot,
with the domain fit (the swap test must break) and the difficulty named. Architecture 5 (Ollery Creek, READY at a19fc6c
from a parallel session, never uploaded) is superseded; architecture 3 landed on the platform (`runs/triage.md`). One
architecture per world: the western Washington Cascades, a high river's gauge beside valley, ridge, airport and SNOTEL
stations and both basins' elevation bands, a which-question with a PDF report and a CSV. Revision 2 answers the stage 4
judge (NOT_DETERMINISTIC, r1): the storm-by-storm carry read each flood's snow line from a daily valley temperature,
and the defensible ways of choosing that day spread the creek's 1 per cent flood from 27,000 to 92,000 cfs; the pack
now ships the airport's hourly record, the snow line is read from the temperature the rain fell at, and the asks are
graded at the precision the carried record supports. Earlier architectures are in git history (3 at 1fffdf5, 4 at
0931661, 5 at a19fc6c).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task3.json` v6, registered 2026-11-08T16:34:09Z; `guard.py check` on the
  filed card: WARN only. `overuse.objective` (forecasting in 7 of the last 12): the slot's assigned objective.
  `repeat.question_form` (which, against task7 v6 and task9 v7): the decision is a pick among three spans, and a pick
  asks which. `test.same_driver_older` against mark253 v1 (lineage) is differentiated on the card: that build adjusted a
  count for nonresponse within classes; here every storm is observed and each is transferred between two basins. The
  axes were redrawn from the first draft for honest reasons (G1 blocked against task4, G14 against task7 v6 and task9
  v7); G6 (the population of flood-making storms shifts between the two basins, cold storms counting at the creek and
  hardly at the river) is the generator, with G14 and G1 beneath it.
- **Pairing:** Pelton County's public works department replaces bridge 2209-04 where Ransom Bar Road crosses Durrow
  Creek, a foothill creek of 85.3 square miles that has never been gauged; the county's road standard (chapter 7)
  sizes a bridge to carry the 1 per cent annual exceedance instantaneous peak flow with 2.0 ft of freeboard, on the
  climate of the records, and for a basin over 10 square miles sends the designer to the nearest gauged basin holding
  25 years or more of annual peaks, carried to the site, with Bulletin 17C frequency curves; that basin is the Coyner
  River near Tessel (86.4 square miles of a glaciated volcano's flank, 6.2 miles away, peaks since water year 1951);
  three spans are rated by the consultant's hydraulic model (140, 185 and 240 ft at 20,500, 29,000 and 40,000 cfs); the
  call is the shortest that carries the creek's flood.
- **Shape:** 04, setting one dial (the span) among allowed settings, with the creek's 50 and 1 per cent flows, each
  span's exceedance band (a three-cell grid), the creek's two largest floods, and the creek's estimated annual peaks as
  a CSV.
- **Strategy:** heterogeneity that pooling hides (`references/sulfur-strategies.md`, WORKS IN FORM), in the live
  form: the storms respond differently (each storm's snow line, rebuilt from the airport's hourly temperatures and the
  station pairs, leaves a different share of each basin draining rain; no column holds it), and the decision weights
  every storm to a basin whose response to it differs from the gauged basin's.
- **Data-native sentence:** the Coyner River drains a high Cascade basin (1,640 to 10,380 ft, mean 6,350 ft) whose
  floods come from rain over the part of it below each storm's snow line, half of it in its median flood and three
  fifths in its largest tenth, while Durrow Creek's foothill basin (610 to 4,380 ft, mean 1,860 ft) lies below the snow
  line in every storm that made a river flood; the river's annual peaks look like any flood record and transfer by
  drainage area to within 2 per cent between the region's other gauged basins, all high ones, so nothing in them shows
  that the creek's floods are drawn from a different part of each storm, or that its largest floods came in other years.
- **Abstraction sentence (written, then tested):** "a rare-event level at an unmeasured unit transferred from a
  measured neighbour whose events each drew on only the part of it below a threshold that moved from event to event,
  while the unmeasured unit lies wholly below that threshold." Against `guard.py mechanisms --objective forecasting`
  and every lineage driver: the nearest (0.09, this slot's architecture 5) offsets a rising response against weaker
  storms inside one record; none transfers a level between two units whose events draw on different shares of
  themselves.
- **Domain fit (the user's swap test, run on the sentence):** "which span carries the creek's 1 per cent flood,
  transferred from the river's gauge" with any other field's nouns loses the snow line, rain falling over a
  contributing area, the saturated lapse rate that places the snow line from a valley thermometer, the rain-snow
  temperature a snow pillow measures, the orographic rise of precipitation, the elevation bands of two basins and the
  exceedance probability of an annual peak flow; nothing is left to compute.
- **Prototype and world** (`generator/world.py`, seed 3069): an hourly simulation of 1950 to 2025 (two storm types,
  250-ft bands, a degree-hour snowpack with rain-on-snow melt, an HBV soil and response routine, triangular routing)
  over the river, the creek, four regional gauges and twelve unshipped regression basins; in 1,200 pooled years the
  creek's 1 per cent flood is 24,384 cfs against the river's 17,666. The revision's prototype (scratch `a7/`): with the
  world's exact hourly valley temperature and rain, 96 storm definitions (dry spells of 3 to 24 hours, rain-weighted,
  plain or wettest-24-hour temperature, sharp or logistic transition, annual or every flood) put the creek's 1 per cent
  flood between 24,317 and 27,677 cfs, all inside the 185 ft span; on the built pack the standing family spans 23,800 to
  25,600 and every member files every graded cell the golden files.
- **People:** drawn with `guard.py names --geo us --locale en_US --seed 611`: Amy Rasmussen (the county's bridge
  engineer), Frederick Hess (the hydraulic consultant). `guard.py surface` also reads "Ransom Bar" as a name: it is the
  road.

## Default path

The pipeline a competent flood hydrologist builds from the prompt's words, the county standard and the files' grain,
the field's own method for the deciding quantity in it (`stumping` 1.1b).

1. Conform the Coyner River's annual peaks (water years 1951 to 2025, two peaks estimated during washouts) and fit
   Bulletin 17C (expected moments, the Multiple Grubbs-Beck test, which flags nothing, the station skew of -0.18
   weighted with the regional -0.12): the river's 50 per cent flood 5,800 cfs, its 1 per cent flood 18,900 cfs.
2. Take the donor the standard names (7.4.3(b)): the nearest gauged basin with 25 years or more, the Coyner River at
   6.2 miles.
3. Carry the curve to the creek by drainage area, the field's transfer, at the state equations' exponent (0.856):
   18,863 x (85.3 / 86.4)^0.856, about 18,700 cfs; the creek's 50 per cent flow about 5,700 cfs; the river's annual
   peaks carried the same way are the creek's estimated annual peaks, its largest floods the river's (1983, 2001).
4. Back-test it: the same transfer between the region's five gauged basins reproduces each one's curve to a median 2
   per cent; the state's equation gives 14,100 cfs; the region's mean unit flood 18,700 cfs; a regression of the five
   gauges' unit floods on mean elevation finds no elevation effect and gives 17,000. Everything agrees on a creek flood
   under 20,500 cfs.
5. The 140 ft span's rated flow (20,500 cfs) carries it, exceeded once in 100 to 1,000 years on that curve.

Ends on: build the 140 ft span, the creek's 1 per cent flood about 20,000 cfs
Golden: build the 185 ft span, the creek's 1 per cent flood about 25,000 cfs

## Stump sentence

The default path builds the 140 ft span on a creek flood of about 18,700 cfs; the step that lands it there is carrying
the Coyner River's record by drainage area, when the river's floods drain only the part of its high basin below each
storm's snow line (half of it in its median flood, three fifths in its largest tenth) while the creek's foothill basin
drains whole in every one of those storms, so each flood carries to the creek at the ratio of the two basins' rain
below the snow line the airport's hourly temperature places (a median 1.57 times, 1.26 in the river's largest floods)
and the creek's 1 per cent flood is about 25,000 cfs, beyond the 140 ft span's 20,500 and inside the 185 ft span's
29,000, with its two largest floods in water years 2008 and 2011 rather than the river's 1983 and 2001.

## Deep reasoning

- Task type: extreme-value and environmental-hazard return-period analysis in physical and environmental sciences
  (the vocabulary's hydrology flood frequency key): the 1 per cent annual exceedance flood at an ungauged site,
  serving Forecasting (a peak flow for the coming 75 years on the record's climate).
- Domain test: the quantity that decides is the creek's 1 per cent annual exceedance instantaneous peak flow, and the
  field's estimator is a Bulletin 17C log-Pearson III curve at a gauge carried to the ungauged site by drainage area
  or a regional regression of quantiles on basin characteristics.
- Swap: "which warehouse should the firm lease, sized to the 1 per cent busiest day of a sister site scaled by floor
  area" keeps a pick against a capacity but loses the snow line, the rain-contributing area, the lapse rate, the snow
  pillow's rain-snow temperature and the orographic rise; with them goes the reason one site's busiest days would
  scale differently from another's, and why its busiest days fall in other years.
- Layer 1: the gauge's daily file has an equipment gap, two estimated washout winters and ice-affected days; the
  peak file carries estimate codes, missing early peak times and gage heights on a datum lowered in 1985; the valley
  observer missed weekends before 1979 (multi-day totals in MDPR) and the station moved 35 ft up the valley in 1988
  with a three-month overlap; the ridge station lost three winters; the airport's hourly export carries specials
  (FM-16) that repeat rain the next routine report holds, traces, suspect flags and missing hours; the SNOTEL sites
  start in 1981 and 1983 with temperatures only from 1987 and 1989; elevations are in metres in the station files,
  feet in the workbook (its station sheet lists each station's elevation in feet). Each is what the system does;
  none is placed to be caught, and none moves a graded cell (SF12, SF13, SF19).
- Layer 2: heterogeneity that pooling hides, read through physics: each storm's snow line leaves a different share of
  each basin draining rain, so the transfer between two basins varies storm by storm and depends on their elevation
  bands.
- Decisive step: the river's floods drain rain only below each storm's snow line, so the record is carried to the
  creek flood by flood at the ratio of the two basins' rain below that line (placed from the temperature the rain fell
  at in the airport's hourly record, with the storm lapse rate and the rain-snow temperature the stations measure and
  the orographic rise), and the creek's frequency curve is fitted to the carried series.
- Not semantics: with every field read, every unit conformed and every clause applied, the drainage-area transfer
  still files 18,700 cfs, because nothing in any file records how much of either basin drained rain in a flood: it is
  a relation between a flood's peak hour, the temperature the rain fell at, a lapse rate measured at a station pair
  and two basins' elevation bands.
- Not rule application: the standard says only "carried to the site"; the enumerated family (drainage area at any
  exponent, the regional unit flood, the state equation, an elevation regression, the snow-line transfer with textbook
  constants, with the stations' constants, with and without the orographic rise, from daily or hourly temperatures)
  spreads the creek's 1 per cent flood from 14,100 to 37,000 cfs and splits the call three ways; the standing family
  (the snow-line transfer from the hourly record with the constants the stations measure and the orographic rise,
  every storm definition, either transition shape, either station pair's lapse, annual peaks or every flood, the
  station skew) spans 23,600 to 25,400 cfs and files every graded cell alike; the ruling-out is loud (the river's own
  floods track rain below the snow line at r 0.76 against 0.55 for the whole basin's rain; the station pair measures
  5.36 degrees C a kilometre on storm days, the snow pillows 0.89 degrees C).
- Analyst test: the easy route a strong hydrologist takes with every record conformed and every clause read is
  Bulletin 17C at the Coyner River carried by drainage area and back-tested between the region's gauges, which ends on
  build the 140 ft span, the creek's 1 per cent flood about 18,700 cfs.
- Estimand: the county standard (pelton_county_road_standards_ch7_excerpt.pdf) 7.4.1 to 7.4.4: the 1 per cent annual
  exceedance instantaneous peak at the bridge, on the climate of the records, from the nearest gauged basin with 25
  years or more carried to the site, by Bulletin 17C with the regional skew; 7.4.2: the shortest span whose rated flow
  is at least that flood; 7.4.5: the report's contents (the 50 and 1 per cent flows, how often each span's rated flow
  is exceeded).
- No decoy: nothing is planted; no memo, draft, consultant estimate or score sizes the creek's flood or ranks the
  spans; the consultant's memorandum rates the openings and states it makes no flood estimate; the state report gives
  no transfer formula; no document mentions snow, elevation or storms.
- No certified replay: no figure in the pack is to be reproduced and the method is not recovered by matching one.
- Chain: (1) the river's floods drain rain only below each storm's snow line, placed for each flood from the
  temperature its rain fell at (the airport's hourly record) with the storm lapse rate the Tessel and Durrow Ridge pair
  measures on storm days and the rain-snow temperature the SNOTEL sites' snow and rain days give; (2) the creek's
  foothill basin lies below that line in every one of those storms, so its rain below the line, with the orographic
  rise the stations show, is a different function of the snow line from the river's; (3) each flood in the river's
  peak files carries to the creek at the ratio of the two basins' rain, smallest in the warm storms behind the river's
  largest floods, and the creek's flood in a year is the largest of its storms', which reorders the record (the creek's
  largest floods are 2008 and 2011, not 1983 and 2001); (4) Bulletin 17C on the carried series, a year with no flood fed
  by rain entered below the low-flood threshold, gives the creek's curve, the span and each span's exceedance band.
- Judgment: a physical model of each basin's flood response (rain over the area below the snow line, with the
  orographic rise) fitted from the stations and checked on the river's own floods: rain below the snow line explains
  the river's peaks at r 0.76 against 0.55 for the whole basin's rain; the storm lapse rate (5.36 degrees C a
  kilometre, 2,161 storm days, the SNOTEL pair 5.21), the rain-snow temperature (0.89 degrees C, a logistic fit to the
  pillows' snow share) and the orographic gain (10 per cent a thousand feet, 865 warm storms) are each estimated from
  the records; the snow line is read from the rain's own hourly temperature, not a daily mean that mixes in the air
  before and after the rain (it misses the rain's temperature by more than 1 degree C, about 600 ft of snow line, in a
  fifth of the floods); and the frequency fit is to a carried series, not a gauged one.
- Hidden by: a sampling property the creek does not share with the river's history: every gauged basin in the region
  is a high one, so the drainage-area transfer validates between them (a median 2 per cent) and the state's equation
  fits them; the river's peaks pass every Bulletin 17C check; the creek has no record; only each flood set against its
  storm's snow line and the two basins' elevation bands shows that the river's floods came from half its basin.
- After the notice: (1) placing the snow line: the storm lapse rate the station pair measures (5.36) and the pillows'
  rain-snow temperature (0.89 degrees C), where the textbook 6.5 degrees C a kilometre files the creek's flood at 35,100
  cfs (240 ft) and the freezing level at 21,200 (185 ft, the 1 per cent cell off); (2) the orographic rise: the river's draining half sits higher
  and wetter than the creek, and area alone files 31,700 cfs (240 ft); (3) the rain's own temperature from the hourly
  record, where a daily storm mean files 29,200 and the reading at the river's peak hour 30,800 (both 240 ft); (4) every
  storm's flood carried and the year's largest taken, which names the creek's largest floods.
- One-fact test: the likeliest hint is "the creek is rain-dominated and the river snow-affected"; the run still has
  to place every flood's snow line from the stations (a lapse rate measured on storm days, a rain-snow temperature from
  the pillows, the rain's own hourly temperature), weight rain by the orographic rise, carry every flood and refit
  Bulletin 17C; the textbook constants that hint invites file the 240 ft span with every flow and band off.
- No replay: the call re-derives no published figure and no stated number is wrong; every figure in the pack is right
  as it stands.
- Pinned: every rival run on the pack in checks.py: the drainage-area transfer, the regional unit flood and the state
  equation file 140 ft, an elevation regression over the five high gauges 240 ft; the snow line with textbook constants
  or without the orographic rise files 240 ft, the freezing level 140 ft; the standing family files 185 ft and every
  graded cell; the standard's 7.4.3 order rules out the regional equation and another gauge as donor, 7.4.4 rules out
  another distribution.
- Run forecast: run 1 takes a method shortcut (Bulletin 17C carried by drainage area, back-tested between the high
  gauges, 140 ft); run 2 an unfinished chain (notices the creek is far lower than every gauged basin and places a snow
  line with the textbook lapse rate, 240 ft) or a self-confirming check (the regional back-test, 140 ft).
- Strategy label: WORKS IN FORM (heterogeneity that pooling hides), built in the live form: the storms respond
  differently, each storm's snow line rebuilt from the hourly record and the station pairs with no column holding it,
  and the decision weights every storm to a basin whose response differs; the field's transfer at rung 0.
- Lesson: a flood record carries to another basin only as far as the two basins drain the same storms; where the snow
  line moves from storm to storm, two basins of one size answer the same storm differently, and the transfer has to be
  rebuilt storm by storm from the atmosphere's own measurements, at the grain the rain fell at.

## Survivor anatomy

- Actor: the floods have rows (peaks in the annual and above-base files); the property that decides, how much of
  each basin drained rain in each flood's storm, has no column in any file: it is a relation between a flood's peak
  hour, the airport's hourly temperature and rain before it, a lapse rate measured at another station pair, a rain-snow
  temperature measured at the snow pillows, and two basins' elevation bands.
- Link: flood to storm (the USGS peak times against the airport's hourly rain), storm to snow line (the rain-weighted
  temperature with the storm lapse from the Tessel and Durrow Ridge pair and the pillows' rain-snow temperature), snow
  line to each basin's draining area (the workbook's bands for every gauged basin and the crossing); no key joins a flood to a basin
  share, no sentence invites it, and the comparison that shows it (the river's peaks against rain below the snow line,
  r 0.76, against the whole basin's rain, r 0.55) is one the field's transfer never asks for.
- Reflex: the field's method, Bulletin 17C at the gauge carried by drainage area, sits at rung 0 and files 18,700 cfs
  and the 140 ft span; the regional equation (14,100), the regional unit flood (18,700) and an elevation regression
  over the five gauges (17,000) agree.
- Back-test: the textbook route validates: the drainage-area transfer reproduces each of the region's five gauged
  basins from the others to a median 2 per cent, because all five are high basins whose floods drain the same share of
  each storm (checks.py B1).
- Second use: the airport's hourly record is the county's weather record for the road (wind, visibility, present
  weather); the station records and SNOTEL files are the state study's precipitation network (the workbook's station
  sheet); the peak files are the gauge record 7.4.3 requires. Deleting the decisive step leaves every file in the pack.
- Shock: no flood, year or gauge stands out: the river's record passes the low-flood test with nothing flagged, its
  largest flood (16,300 cfs, November 1982) is unremarkable, and the creek has no record.
- Pins: the county standard files the WHAT (the 1 per cent instantaneous peak at the bridge, the records' climate,
  the nearest gauged basin, Bulletin 17C with the regional skew, the rated-flow rule, the report's contents) and names
  no way of carrying the record.

## Readability screen

Tests: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 dedicated organ, 8 framing.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 Bulletin 17C at the gauge carried by drainage area | no | area column | yes (the field's transfer) | no | no | yes (one ratio) | no | no | readable |
| 0b the regional unit flood, the state equation | no | area, precipitation columns | yes (the field's regression) | no | no | no | no | no | readable |
| 1 a snow line with textbook constants (6.5 degrees C a km, 0 degrees C) | no | no | partly (the constants are the reflex once a snow line is drawn) | no | no | no | no | no | readable |
| 2 the snow line from the rain's hourly temperature, the stations' storm lapse and the pillows' rain-snow temperature, rain with the orographic rise, every flood carried (decisive) | no (7.4.3 says carried, nothing more) | no (no column holds a basin share or a snow line) | no (no flood transfer practice carries storm by storm) | no (the back-test confirms rung 0) | no (the battery conforms and dedupes, it does not set floods against storms) | no (a ratio per flood inside a refitted curve) | no (the hourly record and the stations serve other uses) | no (the prompt says only that the creek was never gauged) | silent |

## Semantic fork table

| SF | Term or convention | Readings | Ruled out by |
|---|---|---|---|
| SF1 | the 1 per cent annual exceedance peak flow | the instantaneous annual peak; the annual maximum daily mean | the standard 7.4.1 ("the instantaneous peak discharge at the bridge") |
| SF2 | on the climate the records show | the record as it stands; a climate-adjusted record; the recent decades only | the standard 7.4.1 ("No allowance for a future climate") and the full gauged record |
| SF3 | the record carried | the nearest gauged basin with 25 years (the Coyner River, 6.2 mi); a regional gauge; the state equation | the standard 7.4.3 order and the workbook's distances |
| SF4 | the frequency distribution | Bulletin 17C (expected moments, Multiple Grubbs-Beck, weighted skew); a GEV; the station skew | the standard 7.4.4; the station skew keeps every cell (checks.py) |
| SF5 | a span's rated flow | the consultant's discharge with 2.0 ft of freeboard | the standard 7.4.2 and the memorandum's table 1 |
| SF6 | the shortest span that carries the flood | rated flow at least the flood | the standard 7.4.2 ("at least") |
| SF7 | the year with no flood fed by rain (1997) | below the low-flood threshold (an expected-moments interval); dropped | same cells (checks.py) |
| SF8 | how far before a peak its rain may end | 36 hours; 24 or 48 | same cells (checks.py) |
| SF9 | the temperature the rain fell at | rain-weighted over the storm; the plain mean of its wet hours; the wettest 24 hours | same cells (checks.py) |
| SF10 | the rain-snow transition | the pillows' logistic share; a sharp threshold at its midpoint | same cells (checks.py) |
| SF11 | carrying a peak between basins of 86.4 and 85.3 sq mi | drainage-area exponent 0.6 to 1.0 | same cells (checks.py) |
| SF12 | the valley station's 1988 move (35 ft) | each record at its own elevation; the two read at one elevation | the same lapse to the second decimal (checks.py) |
| SF13 | multi-day precipitation totals | spread over their days; on the last day | same cells (checks.py) |
| SF14 | the two estimated peaks (1991, 2004) | kept, as USGS publishes them and Bulletin 17C reads them as record; dropped | same call, flows and bands; neither is among the creek's largest floods (checks.py) |
| SF15 | the storm lapse rate's station pair | Tessel and Durrow Ridge (5.36); Hatchet Meadow and Corbel Ridge (5.21) | same cells (checks.py) |
| SF16 | the orographic gain | warm-storm ridge over valley totals (0.100); water-year station means | same call (checks.py) |
| SF17 | the river's snowmelt peaks (no rain in the 36 hours before) | left out of the carry; carried | left out: nothing fell as rain to carry (checks.py) |
| SF18 | the annual-peaks file | 75 water years, the year without a rain flood marked less than the low-flood threshold | the prompt ("each water year from 1951 to 2025") |
| SF19 | the airport's specials (FM-16) | routine reports only; every report's rain summed into its hour | same cells (checks.py) |
| SF20 | the dry spell that ends a storm | 6 hours; 3, 12 or 24 | same cells (checks.py) |
| SF21 | daily against hourly temperature | the rain's hourly temperature; the valley's daily mean | the hourly record: the daily mean misses the rain's temperature by more than 1 degree C in a fifth of the floods (checks.py) |
| SF22 | the temperature that places a flood's snow line | the rain-weighted hourly temperature; the airport's reading at the river's peak hour | the hourly record: no rain fell in the peak hour in 48 per cent of the floods and the air then ran a median 0.7 degrees C colder (checks.py) |

## Ladder

| Rung | Construction | Creek 1 per cent flood (cfs) | Files | Dies to |
|---|---|---|---|---|
| 0 | Bulletin 17C at the Coyner River carried by drainage area | 18,700 | 140 ft | the river's floods drain only the area below each storm's snow line |
| 0b | the region's mean unit flood; the state equation out of range; an elevation regression over the five gauges | 18,700; 14,100; 17,000 | 140 ft | the same, and 7.4.3 and the equation's range |
| 1 | a snow line with the textbook lapse (6.5 degrees C a km) and 0 degrees C, area alone | 37,000 | 240 ft | the stations' storm lapse, the pillows' rain-snow temperature, the orographic rise |
| 1b | the stations' lapse and the pillows' temperature, area alone | 31,700 | 240 ft | the orographic rise the stations show |
| 1c | the freezing level as the snow line | 21,200 | 185 ft, the 1 per cent cell off | the pillows' rain-snow temperature |
| 1d | the stations' constants from the valley's daily storm-mean temperature, or from the airport's reading at the river's peak hour | 29,200; 30,800 | 240 ft | the rain's own temperature in the hourly record (SF21, SF22) |
| 2 (decisive) | the stations' storm lapse, the pillows' rain-snow temperature, the orographic rise, the rain's hourly temperature, every flood | 24,781 | 185 ft | nothing |

Margins: rung 0 files the creek's flood 9 per cent under the 140 ft span's rating and the golden 21 per cent over it;
the standing family's lowest member (23,600) sits 15 per cent over it, and every data-supported estimator combination
(108 of them, the lapse from either pair, the rain-snow temperature 0.85 to 0.94 degrees C, the orographic gain 0.095
to 0.11, either transition, any rain weighting) 11.6 per cent or more over it; the golden sits 15 per cent under the
185 ft span's rating and the family's highest member (25,400) 12 per cent under it; rung 1 files 28 per cent over the
185 ft span. Pricing: the residue the WHAT leaves is the carrying method (a method, not a knob); the one-group-by route
to the call is "the creek is lower than every gauge", which files no figure and, quantified by an elevation regression
across the five high gauges (their unit floods alike), finds no elevation effect and files 17,000 (140 ft); the
decisive step's worth (the 1 per cent flood from 18,700 to 25,000) is 1.3 cells of the asks' 5,000 cfs and moves two
of the three bands; the standing family's spread is a third of a cell; the long-run truth of the simulated climate
(24,384 cfs in 1,200 years) sits inside the 185 ft span and the golden's cell.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the creek's annual instantaneous peaks at the bridge | the standard 7.4.1 |
| 2 Unit of account | a water year's peak | the standard 7.4.1, 7.4.4 |
| 3 Attribution window | water years (October to September) | the USGS peak files |
| 4 As-of dating | the records through water year 2025 | the files' retrieval and record ends |
| 5 Version basis | approved records | the files (approved through 2025) |
| 6 Denominator | an annual exceedance probability | the standard 7.4.1 |
| 7 Weighting | none (each year one peak) | n/a |
| 8 Window length | water years 1951 to 2025 | the standard 7.4.1 (the records' climate) and the prompt |
| 9 Boundary inclusivity | rated flow at least the flood; a band's lower edge exclusive | the standard 7.4.2; no rated flow sits on a band edge (checks.py C4) |
| 10 Rounding path | the report's creek flows to the nearest 5,000 cfs, the file's to the nearest 100 cfs, at the end | the prompt; both graded flows 10 per cent or more inside their cells (C3) |
| 11 Tie-break | the shortest span; the two largest floods | the standard 7.4.2; the second largest flood clears the third by 22 per cent (C5) |
| 12 Maturity and censoring | low floods by the Multiple Grubbs-Beck test; the year with no rain flood below the threshold | the standard 7.4.4; SF7 |
| 13 Order of operations | carry each flood, take each year's largest, fit the curve | the design (a curve of annual peaks); checks.py runs the curve-then-carry order to 240 ft (R4) |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | a peak in both files; the airport's specials | counted once (same date); routine reports only (SF19) |
| 16 Identity normalisation | stations across the 1988 move | the two station identifiers, both kept |
| 17 Netting against gross | none | n/a |
| 18 Dimensional units | metres, feet, square miles, Fahrenheit | the files' own headers; the workbook's station sheet in feet |
| 19 Code and status semantics | peak codes, qualifiers, GHCN attributes, LCD report types and flags | the files' own legends |
| 20 Integerisation | none | n/a |
| 21 Clause scope | chapter 7.4 applies to this bridge | the standard 7.1 |
| 22 Forward window contents | the coming 75 years drawn from the record's climate | the standard 7.4.1 |

## Literal reader

A judge executing the standard word for word takes the nearest gauged basin with 25 years or more of annual peaks
(the Coyner River at 6.2 miles), carries its record to the site, fits Bulletin 17C and picks the shortest span whose
rated flow is at least the 1 per cent flood. "Carried to the site" names no method, so the judge must carry the
record the way the records support: the river's own floods track rain below each storm's snow line (r 0.76 over 183
floods) far better than the whole basin's rain (0.55), and the creek's bands lie below that line in every one of those
storms, so the drainage-area carry is refuted by the records and the storm-by-storm carry is what they support; every
storm definition and temperature weighting the hourly record allows files the same cells (checks.py L1, R6, SF8,
SF9, SF19, SF20), and the independent verifier's road (pandas, the SNOTEL pair's lapse, a binned sharp rain-snow line,
plain-moment log-Pearson III) lands the same span, cells and floods.

## Oracles

- The drainage-area transfer between the region's gauged basins and the state equation's fit confirm the easy route
  (controls that tie on the high basins under every method), kept: they are the field's own checks.
- No figure in the pack sizes the creek's flood or ranks the spans; the consultant's memorandum states it makes no
  flood estimate, and the state report gives no transfer formula.

## Ask sheet

Every ask figure is computed from the deep step's output (the creek's carried annual series and its Bulletin 17C
curve), graded at the precision the carried record supports.

| Ask | Figures | Second judgment | Shallow (drainage area) | Golden |
|---|---|---|---|---|
| A1 the creek's 50 per cent flow | 1 | every flood carried and the year's largest taken | 5,000 | 10,000 |
| A2 the creek's 1 per cent flow | 1 | the rain's hourly temperature (the daily storm mean files 30,000) | 20,000 | 25,000 |
| A3 each span's exceedance band | 3 | the curve's tail on a carried series | 100 to 1,000; beyond 1,000; beyond 1,000 | 10 to 100; 100 to 1,000; beyond 1,000 |
| A4 the creek's two largest floods | 2 | every flood carried (the river's record years are not the creek's) | 1983, 2001 | 2008, 2011 |
| A5 the annual-peaks file | 75 rows | the year without a rain flood marked below the threshold | the river's peaks scaled | the carried series |

Mess on the ask paths: the same conforming every careful run applies (weekend totals, the station move, units,
codes, specials, outages); none moves a graded cell between careful runs (SF12, SF13, SF19).

| Ask | Why the landed run misses or keeps it | Cracker (the landed run: the snow-line carry taken, every mess item cleaned, every rule read, the second judgments at their reflex) |
|---|---|---|
| A1 | the textbook lapse and flat precipitation file the 50 per cent flow at 15,000 | miss |
| A2 | the same file the 1 per cent flow at 35,000 | miss |
| A3 | the same put the spans' bands at more often than once in 10, 10 to 100 and 100 to 1,000 | miss |
| A4 | the snow-line carry reorders the record whatever its constants | keep |
| A5 | the same flood selection marks the same year | keep |

Shallow keep: 14.3 per cent of ask cells (the 240 ft span's band)
Landed shortcut (stated, not hidden): one median concurrent ratio from the foothill gauge on the river's curve scores 84.3
(the call, both flows and the bands; it misses the creek's two floods and the file); against a shallow run the pair is
52.1, under the bar but with one run on the call, so the build rests on most runs taking the drainage-area transfer or
the textbook constants (ceiling.py).
Pair ceiling: 23.8 (ceiling.py: the cracker 27.7 against the shallow run 19.9; the full includer, every second judgment taken, 100.0 against a shallow run gives 59.9)
Measured by: generator/ceiling.py

## Prompt contract

The author's voice rewrite may not drop or change: the decision (which span the county should build for the Durrow
Creek bridge on Ransom Bar Road, 140, 185 or 240 ft); the rule (the shortest whose rated flow carries the creek's 1
per cent annual exceedance peak flow); the climate (the records'); the fact that the creek has never been gauged; the
deliverables durrow_creek_bridge_hydrology_report.pdf (the span, the creek's 50 and 1 per cent flows, each span's
exceedance band in the four named decade bands (once in 10, 100 and 1,000 years), the water years of the creek's two largest floods since 1951) and
durrow_creek_estimated_annual_peaks.csv (the creek's estimated peak for each water year 1951 to 2025); the rounding
(the report's flows to the nearest 5,000 cfs, the file's to the nearest 100 cfs).

## Stage 4

Round 1 (target.zip 7e873e87, the daily-temperature carry). The leak reader quoted no sentence naming the decisive step
and found no file ranking the spans; its question 6 answer called the donor choice and 7.4.3 to 7.4.4 rule application
and the rest an analytical judgment no filed sentence states. Its realism findings, each fixed in the generator: the
elevation-band sheet read as a two-basin comparison aid (it now carries every gauged basin's bands); a free-text
gage-house note on the river's peak file, with estimated peaks of ordinary size (the note is gone and the estimated
peaks sit inside the daily file's washout windows); one retrieval minute on all seven USGS files (each carries its
own); the 2019 and 2023 excerpts exported by LibreOffice 24.2 (now exported in 2024 and 2026, as excerpts are); the
memorandum's PDF created three days before its date (now the issue date). The determinism judge returned
NOT_DETERMINISTIC (SEND_BACK): the carry is not prescribed and its parameters and day choices land every span. The
main thread reproduced it: 80 defensible daily-record implementations put the creek's 1 per cent flood from 27,055 to
92,536 cfs, the golden at the bottom, because a daily valley mean on a storm's edge mixes in the air before and after
the rain and the snow line is steep in it. Repair (revision 2): the airport's hourly record ships, the snow line is
read from the rain's own temperature (the family of storm definitions and weightings collapses to 23,800 to 25,600
cfs), the spans were re-rated so the call and every band carry margin (round 2 below), the asks are graded
at the nearest 5,000 cfs and as bands, the two largest floods and a 75-row file, and the judge's unit point is closed by
the workbook's station sheet in feet. The judge's other point (the drainage-area transfer as the only filed carry)
stands answered by the records: the river's floods follow rain below the snow line at r 0.76 against 0.55.

Round 2 (revision 2). The leak reader quoted no sentence naming the decisive step and found no file ranking the spans
or reading as the answer; its question 6 called the transfer from the high gauge to the low creek the analytical piece
and the filed text the procedure around it, as designed. Its realism findings, each fixed in the generator: export
stamps on the whole minute (now with seconds), the creek's bands in acres beside the county's own square miles (now
square miles), the workbook's writing-library dialect and one entry clock (now Excel's dialect and 1980 entry stamps,
the container gate audit_containers.py at 0 FAIL), every zip entry on one clock (each now at its file's own save), the
hourly reports on a :53 grid back to 1950 (56 minutes past before the automated station), and a report number from a
real series on the state excerpt (dropped). The workbook's station list naming three stations with no file is the
state study's wider network; harmless.

Round 2 (revision 2), the determinism judge: NOT_DETERMINISTIC on margin, not mechanism. It called the storm-by-storm
contributing-area carry the correct route, rejected the area transfer and the state equation, passed Gates G and H
(one_fact: none), and found in its own cold derivation, before reading the answer, that the regional gauges' flood
ratios follow the area below each storm's freezing level. Its fragility: lapse estimates of 4.77 to 5.36 degrees C a
kilometre took the creek's 1 per cent flood under the 22,000 cfs rating, and the temperature at the river's peak hour
took it over the 28,000. The main thread reproduced the lapse spread exactly as one reading of the Tessel record at a
single elevation across the 1988 move (each station at its own elevation, every statistic and temperature variable gives
5.32 to 5.39): mess deciding, so the move is now 35 ft and both readings give the same lapse (SF12). The peak-hour
reading is not the temperature the rain fell at (no rain in that hour in 48 per cent of the floods, the air a median
0.7 degrees C colder, SF22), stated in the Step-by-Step. The spans are re-rated 20,500, 29,000 and 40,000 cfs so every
data-supported estimator combination keeps the call with 11.6 per cent or more to spare, the bands are decades (once in
10, 100 and 1,000 years) so each span's band holds across the family, and the four regional gauges' precipitation is set
so their unit floods agree with the Coyner River's (they are the alike high basins the design says), which puts the
regional unit flood (18,700) and an elevation regression over them (17,000) on the default's 140 ft. The leak reader
re-ran on the changed prompt (round 3) beside the re-judge.

Round 3 (revision 2), the determinism judge: NOT_DETERMINISTIC again; its carry from daily station temperatures and
its own lapse set filed 30,000 to 55,000 cfs. Three judges, three constructions: the carry was a physical model the
files left open. The author chose the repair (the main thread's option 2): the pack now holds the deciding configuration
in its own record, a foothill crest-stage gauge (Selby Creek near Hollis, USGS 12186050, 62 square
miles between 420 and 3,900 ft, water years 2012 to 2025, 14 years, too short to carry under 7.4.3).
Carried from the river's concurrent floods, the golden construction reproduces its 11 floods to a median
+5 per cent (median absolute log error 0.07); every rival construction does
worse by 0.04 or more: the drainage-area transfer -26, the standard atmosphere's lapse
+47, rain without the orographic rise +37, the freezing level
-11, the valley's daily mean +11 and the peak-hour reading
+25 per cent (checks.py V1 to V3). The data, not the author, now select the carry. The
shortcuts the short record invites: MOVE.1 extension carried by area files 18,300 cfs (140 ft, V4); the
record's own curve is barred by 7.4.3 (V5); one median concurrent ratio on the river's curve files 25,300 cfs,
the golden's span and 1 per cent cell, and misses the creek's floods and the file (V6). Its cost is stated in the ask
sheet. Round 3's minor note (the creek's mean elevation 1,860 against the workbook's 1,870 ft) is fixed: the write-up
reads the workbook's figure.

Round 4 (option 2, the final cut d36f2053), the determinism judge: DETERMINISTIC, APPROVE. It forced the 185 ft span,
reproduced the foothill gauge's validation (median -0.4 per cent against the golden's +5), put the creek's 1 per cent
flood at about 23,500 cfs (21,000 to 27,500 over the parameter ranges the data support) and its 50 per cent flood at 8,800,
both in the golden's cells, found water years 2008 and 2011 the two largest in all eight of its variants and every band
reproduced; Gates G and H pass (one_fact none). Its advisory, the 1 per cent cell about 1,000 cfs from its edge in its
replication, is a rubric-tolerance note. The leak reader (round 4) quoted no sentence naming the step; its rulings are in
the leak report. guard.py surface promotes task2 against this build (G6 back to back): task2 was re-drawn after this card
(22:01 against 16:34), in another domain and on another driver, so the rule falls on the later draw.

leak.py on target.zip d36f2053 (--asof 2026-10-14): REVIEW, no LEAK once the memorandum's stage table moved off the
5,000 cfs grid the graded flows now sit on. The main thread's rulings, one line each:
- the six USGS text files (sweep 1): the agency's own peak records in its RDB layout; harmless.
- the standard and the state report carrying generic design-note words (sweep 4: record, carried, station, regional,
  design, bulletin): read whole, the standard names the record to carry and never how; harmless.
- the prompt's shell quota (sweep 11): csv with pdf at 22 per cent of nine prompts, this prompt itself counted;
  harmless.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call turns on carrying the river's floods at each storm's
  snow line (checks.py R3a, R3b); the drainage-area transfer files 140 ft, misses every graded cell but the 240 ft band
  and validates between the region's high gauges (R3a, B1); no column, sentence or document names a snow line, a storm
  or an elevation band's share (R1, O2); the one-fact hint executed with the constants it invites files 240 ft (R5);
  each of five links skipped moves the call or graded cells (R4); every rival is run (R6).
- Mess neutral: the weekend totals on their last day, the station move read at one elevation, the estimated peaks
  dropped, either station pair's lapse, either orographic estimate and the specials summed keep the call (SF12 to
  SF16, SF19).
- Determinism: twenty-two forks closed and asserted (SF1 to SF22); fourteen standing family members file every graded
  cell the golden files; the verifier's independent road lands on 185 ft, the 5,000 cfs cells and the two floods with
  its 1 per cent flood at 23,074 against 24,781.
- The pack (final cut d36f2053): seventeen files in two categories (spreadsheet, text); the airport's hourly record of
  659,041 reports and three CSVs of 27,000 rows or more; five distractors named only in metadata.json; every file's
  source, pull date and licence in metadata.json; no writer signature; two builds byte-identical over twenty-two files.
- The goldens: exactly the two requested files; one set of numbers across the report, the CSV, the chart and the
  four blocks (figures_check.py, 110 of 110); the container gate (audit_containers.py) at 0 FAIL.

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

Architecture 6 (the Durrow Creek bridge):

- 2026-11-08, architecture 5 (Ollery Creek's culvert from a record whose response rose while its storms fell): built
  to READY by a parallel session while this one drew (a19fc6c, Alternative B at about 10,570 cfs, judge DETERMINISTIC
  and APPROVE), never uploaded; superseded at the author's word, a total rework of the slot asked for after every
  run architecture landed, so it carries no platform measurement. Its design sections are in git history at a19fc6c.
- 2026-11-08, draw stage: the snow line under a planned warming (the state's planning temperature filed for the
  design life) set aside, because the framing names the axis and the field's climate scaling of rainfall is a
  reflex; a transfer between two basins of different elevation keeps the axis unnamed.
- 2026-11-08, draw stage: the prototype's first gauged basin (1,100 to 7,600 ft, storm temperature and wetness
  correlated at 0.30): the storm-by-storm transfer sat 1.1 to 1.2 times the drainage-area transfer, inside the
  gauge's sampling noise; the gauged basin was raised (1,500 to 9,500 ft) and the correlation set at 0.20, which
  moves it to 1.6 to 2.0.
- 2026-11-08, draw stage: a high-water mark or an overtopping log for the old bridge set aside: one recorded creek
  flood hands the answer's scale to any reader (a single-fact rescue). A low-elevation regional gauge set aside: its
  short record offers a noisy direct donor and an elevation regression one point wide.
- 2026-11-08, draw stage: the decisive pattern G1 blocked against task4 (`ban.pattern`), then G14 against task7 v6 and
  task9 v7 once the parallel sessions' cards reached this checkout; Gate G forecasting with gap population and G14
  blocked against task1 (`test.same_driver`); the deliverable sets docx with csv (33 per cent of
  prompts) and docx with xlsx (44 per cent) broke the shell quota.
- 2026-11-08, design stage: the Sierra Nevada setting: the largest warm atmospheric rivers rain over nearly all of a
  Sierra west-slope basin, so the snow-line effect vanished at the 1 per cent level (the creek's 1 per cent flood at
  0.93 of the river's against 0.66 by area only once the river's basin rose to a glaciated volcano's flank); the world
  moved to the western Washington Cascades, where the river's largest storms leave two fifths of its basin under snow.
- 2026-11-08, design stage: the river's annual peaks fell mostly in April to July (snowmelt) in the first tuning, unlike
  western Washington; two storm types (atmospheric rivers and ordinary storms) and a slower spring melt put them in
  October to February.
- 2026-11-08, design stage: a storm generator whose summer gaps could skip a wet season (creek annual peaks of 20 to
  120 cfs, a log skew of -3): rebuilt as a thinned non-homogeneous Poisson process.
- 2026-11-08, design stage: storm temperatures that replaced the hour's climatology abruptly: the valley's daily means
  mixed storm and pre-storm air, the snow lines sat 1,000 ft low and the pack golden came out at 74,000 cfs; the storm's
  air mass now arrives with the rain and lingers after it.
- 2026-11-08, design stage: the valley and ridge observers reading at 17:00 and 08:00: their daily means covered
  different hours and the storm lapse read 5.97 against a true 5.2 degrees C a kilometre; both read at 17:00, and the
  SNOTEL pair (calendar days) agrees (5.21).
- 2026-11-08, design stage: the orographic gain from water-year station means (0.063): the higher gauges undercatch
  snow; the golden takes it from warm-storm ridge over valley totals (0.100).
- 2026-11-08, design stage: each flood's snow line from the storm's precipitation-weighted temperature over its whole
  wet run: post-frontal days pulled it 1,000 ft or more low in the worst floods; the run is cut at the peak and the
  snow line read from the flood's wettest day (per-flood error against the world's own median -0.01, unbiased for the
  largest floods).
- 2026-11-08, design stage: the creek at 51.7 square miles: the transfer's drainage-area exponent (0.7 to 1.0) moved
  every figure 7 per cent, a fork on the asks; the creek was redrawn at 85.3 square miles beside the river's 86.4, which
  makes the exponent inert.
- 2026-11-08, design stage: four regional gauges lower than the Coyner River (mean elevations 4,400 to 5,900 ft): their
  unit floods ran 30 per cent above the river's and the region's mean unit flood filed the 185 ft span with no snow
  line; every gauged basin in the region is now a high one (5,400 to 6,700 ft) and the drainage-area transfer
  validates between them.
- 2026-11-08, design stage: the state equations fitted on basins of one climate (precipitation 73 to 79 in, a
  precipitation exponent of -3 to -6); the twelve unshipped regression basins carry their own precipitation, soils and
  routing.
- 2026-11-08, design stage: a design-life chance of exceedance as an ask: it reads the curve's tail at the rated flow
  and the standing family spread it 20 to 31 per cent; dropped. The 50 per cent flood at the nearest 1,000 cfs: the
  golden's 9,568 sat 68 cfs from a rounding edge; dropped.
- Architecture 6 round 1, the storm-by-storm carry with each flood's snow line from the valley's daily mean on its
  wettest day: the determinism judge's replication filed 56,000 cfs and the main thread's 80 defensible daily-record
  implementations spread the creek's 1 per cent flood 27,055 to 92,536 cfs, the golden at the bottom (a daily mean on a
  storm's edge mixes in the air before and after the rain, and the snow line is steep in it); revised to the airport's
  hourly record, where 96 storm definitions collapse to 24,317 to 27,677.
- Revision 2 as first cut (spans 22,000, 28,000 and 40,000 cfs, the Tessel station moved 160 ft in 1988, bands at 25,
  100 and 500 years): the round 2 judge's lapse read at one elevation across the move (5.07) took the creek's flood
  under 22,000 and the peak-hour temperature took it over 28,000; the move shrunk to 35 ft, the spans re-rated and the
  bands set at decades. A storm air mass lingering 30 hours after the rain (to bring the peak-hour reading to the rain's)
  re-rolled the whole flood record and widened the peak-hour spread; dropped for the refutation in SF22.
- Architecture 6 revision 2 after round 3: the third isolated judge carried the record with daily station temperatures
  and its own lapse set and filed 30,000 to 55,000 cfs (240 ft), with other largest floods (2008, 1973, 1999); three
  judges, three constructions, two spans off the golden's. The storm-by-storm snow-line carry is a physical model the
  files leave open, and its answer moves across the spans' margins with the construction; paused for the author.
- Option 2's foothill gauge at 41 and 48 square miles (and from water year 2008 at 62 and 68): at the small sizes the
  golden overran the gauge's floods by 7 to 10 per cent and the freezing level fit them better, so the data would have
  chosen a wrong construction; from 2008 MOVE.1 reached the golden's span; 62 square miles from 2012 leaves the golden
  the best fit by 0.05 and MOVE.1 on the 140 ft span.
