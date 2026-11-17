# task3: the protection class of every gully crossing on the SP 141 for the 2027 to 2031 programme

## Draw

Subdomain: Extreme-value & environmental-hazard (return-period) analysis (Physical & Environmental Sciences, climate-weather-extremes)
Analysis type: Forecasting & Predictive Modeling
Answer shape: a distribution and where it is cut (each source area's seasonal distribution of 60-minute storm maxima, cut at the crossing's triggering depth for the storms a season to expect and at five a season for the depth, with the class the two regulation lines put on it)
Weight: modeling: the work is three instrument models (what a tipping bucket loses by rate, what a radar's pixel pairs carry of the contrast between a source area and its road station, what an unheated funnel does to a hail storm's minutes), each fitted through a second record and checked on a slice the crossings do not reach; none of the last three builds on file (task16 hard-to-measure, task13 attribution, task1 measurement) puts its work there
Data-native sentence: the only long record of short-duration rain on the SP 141 is each road station's tipping bucket, which loses water while it tips (more the harder it rains), stands one to five kilometres below the source area whose cloudbursts set off the flows, and on hail days tips the funnel's melt an hour or two after the storm, so how often a source area reaches its triggering depth in 60 minutes has to be estimated from the tips, the storage gauges' monthly account, the detector's ten-minute record of what fell and when, and the radar's storm maxima, each read for the part it sees.
People: Piero Brancaccio (head of the Servizio Strade Alta Ardesa, who signs the programme and issues the regulation), Biagio Borroni (geologist, author of the crossings register and the triggering depths), Luca Comboni (hydrologist of the service, whose workbook the golden is), Alfio Cundari and Bartolomeo Panatta (station technicians, who keep the visit book) (`guard.py names --geo IT --seed 3008 --n 6`). None appears in the prompt.

Architecture 8, a new world drawn on 2026-11-16. Architecture 7 (a Georgia port's tidal low points, READY at a175067 and never uploaded) was set aside before any platform round: its two priced results were response-model corrections on mechanisms of the world, the kind the review of 2026-11-13 returned at 75 to 83, its harbor results were asks sited away from the stumps, and its deciding lesson sits on four live builds. One architecture per world, so the slot moves to a mountain road service, a new dataset and a new core, proved in `generator/core.py` before any file exists. The decision has three classes on two lines (a plain set over one line is on six live builds). A written document is not asked for: the programme's reader works in the workbook, and the classing sits on its first sheet.

## Stump screen

Screened on paper and in `generator/core.py` before the card was registered (`references/stump-screen.md`, the seventeen tests).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A: a tipping bucket loses the water that falls while it tips, so its shortfall grows with the rate and is largest in the minutes that make a triggering storm | the storage gauge's excess over the tips is spread like the tipped water, one factor per station (N21, L28) | the storage gauges' reads in the visit book against the tips' minute rates, visit interval by visit interval | none | kept |
| B: a source area's cloudbursts differ from its road station's by a factor of its own (0.78 to 1.38) that the yearly rainfall does not carry | the station stands for its source area, or is carried there by the ratio of their yearly rainfall (N26, N01) | the radar's 60-minute maxima on the source pixel and the station pixel in the same storm, 2013 to 2026, and the research valley's weighing gauges | none | kept |
| C: on hail and graupel days the unheated funnel holds the ice and the bucket tips its melt over the next hour or two, so the tips have the storm's water and not its minutes | the minutes the tips arrive are the minutes the rain fell (N30, L26) | the detector's ten-minute record of what fell and when against the tips' minutes in the same storm | none | kept |
| D: the radar's 60-minute maximum on a one-kilometre pixel is an area average and under-reads the point depth the triggering depths are filed in | the radar product at the source pixel is the rain at the source | the radar's station pixel against the station's own corrected maxima | 13 (it opens no member of its own) | not a stump: it is what lands the radar route wrong on every open member, and sits inside B |
| E: loggers that lose power in the largest storms leave them out of the tip record | the record is complete | the storage gauge account in the months of an outage | 1 and 2 (the client's closed card on outcomes hidden by the event; runs fill a documented gap from a neighbour unprompted, R30 and R74) | dropped |
| F: older loggers stored clock-hour totals, and a clock hour under-reads the largest 60 consecutive minutes | the hourly total is the 60-minute maximum | the tip-resolution years of the same station | 1, 2 and 3 (closed card: a change of instrument; the fixed-to-sliding factor is the field's textbook constant) | dropped |
| G: wind takes rain past the orifice of the exposed stations | the gauge catches the rain | a wind record | 2 and 11 (a textbook correction once wind ships, and not measurable from this pack at the precision the lines need) | dropped |
| H: a crossing fed by several source areas, any of which can set off a flow, counted on the union of their storms | one source area per crossing | the register's list of source areas | 2 and 3 (once the register lists them the union is a join, and a join is a reflex) | dropped |
| I: storm seasons getting more frequent, the programme's expectation read on a trend | the long-run mean holds | the seasonal counts against the year | 9 and 11 (eighteen seasons of counts cannot carry a trend at the precision the lines need; the regulation files the long-run mean) | dropped |

## Deep reasoning

Task type: climate weather extremes (Extreme-value & environmental-hazard (return-period) analysis), which serves Forecasting: the frequency with which a short-duration rain depth is reached at ungauged places, carried to a five-year programme.
Domain test: every result is a quantity of mountain hydrometeorology: a tipping bucket's loss by rain rate, closed against a storage gauge; the contrast between a source area's cloudbursts and its station's, seen by a radar only as pixel averages; hail and graupel held in an unheated funnel and tipped as melt; the seasonal frequency of a 60-minute depth at a place with no gauge. The field's analyst builds each from the instrument that sees it and checks it on a research catchment.
Swap: "Which stores go on the weekly audit list, judged on how often their hourly sales pass a filed level?" keeps the three classes and nothing else: no instrument loses in proportion to the rate it measures, nothing holds part of the input and releases it afterwards, no second instrument sees the place and the point together as area averages, and the filed level is not a point depth. The task stops making sense.
Where the weight sits: R2 to R4, the three instrument models. Each is long, not clever: the loss is fitted through 648 visit intervals and applied to every tipped minute before any window is taken; the contrast is measured on 712 to 877 storm pairs a source area and carried to four seasons the radar never saw; the hail storms' water is put back in time on 72 to 391 storms a station.
Layer 1: the tips and the detector's blocks on the loggers' clock (UTC+1 all year), the visit book in civil time and the radar and the research valley in UTC; logger blocks re-sent after a restart (1,802 rows); the technician's tip tests at a visit, which tip the bucket and are entered in the visit book (1,820 tips); visit days that slip around the first of the month; a station's radar pixel renumbered when the agency re-gridded its product; long light rain between storms that fills the account and never nears a triggering depth. None decides a result: every route cleans them the same way, and each one left uncleaned keeps every graded figure in its band and the classes where they are (`checks.py`, the five R2 rows).
Not one thing: the strongest single piece is the bucket's loss by rate. A run that nails it still files Rio Marden in class 2 and Rio Sass in class 1 on the yearly rainfall ratio, and Rio Bianc in class 2 on the hail days' tips (S1 fixed alone on the reflex route: three classes wrong, 27 on the rubric).
One-fact test: "the tipping buckets lose water while they tip, more the harder it rains" rescues R2 and nothing else (1 of 7 results): the burst factors, the hail storms and every figure downstream still fall with S2 and S3.
Not semantics: every field, unit, clock and clause read correctly leaves the reflex route where it is: the tips are the tips, the storage gauge is the storage gauge, the triggering depth is a point depth at the source area in 60 consecutive minutes, and the route still files four classes wrong because of what three instruments do to the rain, not because of what a column means.
Not rule application: the regulation files what a triggering storm is, the season, the lines and the expectation's basis; it performs none of R2 to R6. After every filed rule is applied the analyst still has to decide what the tips lost, what a source area gets against its station, and when a hail storm's water fell.
Estimand: regulation 2.1 to 2.4 (the warm season of 1 May to 31 October; a storm as rain separated by six hours or more without rain; a triggering storm as the rain at the crossing's source area reaching the crossing's triggering depth in any 60 consecutive minutes, a storm counted once and an equal depth reaching it; the triggering depth a point rain depth at the source area), 3.1 (the storms a season to expect in a program are the seasonal mean over every complete warm season of the governing station's tip record), 3.2 (the 60-minute depth a source area reaches five times a season, on the same seasons), 4.1 (class 3 at 3.0 a season or more, class 2 at 1.0 or more and under 3.0, class 1 under 1.0), 1.2 (one class for a whole program); the crossings register (each crossing's governing station and its triggering depth as point rain at the source area, mm in 60 minutes).
No decoy: no memo, draft or column carries a wrong answer; no document argues for a route; the crossings register holds no class. The rainfall normal, the radar extract and the research valley's gauges are what they say they are.
No replay: no result re-derives a published figure and no filed number is wrong.
Pinned: 1,216 variants of the golden's conventions on the cut pack (the tipping-time loss alone or with a fixed factor beside it, one a bucket model or one a station, the rate read tip by tip or on totals of one, two, three and five minutes with a tip's water spread over the time since the tip before or kept in its own minute, eight ways of the burst factor, four ways of the hail storms) file one classing, and with the first-order form of the loss on minute totals (512 more crosses the account does not refuse) they set every band; the cruder rivals are each ruled out by a figure from the files (## Semantic fork table).
Run forecast: R2 lost to a self-confirming check (one factor closes every station's account, and a hold-out of seasons confirms it); R3 lost to dismissed own evidence (the radar extract is opened, found to undercount against the gauges and set aside for the rainfall normal, or used as the answer); R4 lost to stopping at the first story (the hail days' totals close, so the tips are taken as rain); R5 to R7 fall with whichever of the three a run loses. The strongest run is expected to make one of the three corrections and lose two.
Strategy label: other (each part of an unrecorded quantity assigned to the instrument that sees it; no label in `references/sulfur-strategies.md` names three instrument blind spots)
Depth level: 5: three independent judgments, each necessary and none sufficient, the three single drops on three different wrong classings and the seven shortcut routes of the lattice on seven.
Lesson: a record is the output of its instrument, so the same storm is three different numbers in three files, and the estimate is built by giving each part of the quantity to the instrument that sees it: amounts to the bucket once its loss by rate is put back, place to the radar's pairs as a contrast and never as a depth, timing to the detector. No build on file teaches a loss that is convex in the measured rate, a second instrument used only for a ratio, or a store that delays a record.

## Results chain

Every figure below is the cut pack's (`generator/figures.json`, target digest cdbf08e67703c82d); the draw's figures on the minute arrays are in ## Stump core.

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each station's tips on one clock set against its storage gauge, visit interval by visit interval: the storage gauges hold 2.2 to 6.0 per cent more water than the tips (Valfosca 1.060, Forcella 1.053, Rio Scuro 1.044, Malga Sora 1.037, Pradalt 1.028, Costarossa 1.022) | assembly-reconciliation | the tip logs, the visit book's reads and its tip-test entries | exact to three decimals on the cut pack | narrow look at broad data: the ten-minute pass never opens the visit book; the careful pass builds the account station by station (reflex R93) | - | Step-by-Step |
| R2 | each bucket model's loss by rate, stated as what Valfosca's bucket fails to record at a true 100 mm an hour (20.2 per cent) | missingness-measurement | the account of R1 fitted on the tips' rates; the station register's bucket models | 17.6 to 24.9 per cent | self-confirming check: one factor per station closes every season's account and holds on held-out seasons, and puts the shortfall at 5.65 per cent at any rate | independent: the tip logs' rates and the visit book's storage gauge reads | Component 1 |
| R3 | each source area's burst factor against its governing station (Rio Marden against Pradalt 1.38; 0.948 at Rio Larin to 1.381) | modeling | the radar's 60-minute maxima on the source pixel and the station pixel in the same storm, 2013 to 2026 | Rio Marden 1.33 to 1.43 | dismissed own evidence: the radar extract is in hand and undercounts against the gauges, so the station is carried to its source by the rainfall normal's ratio (1.06 at Rio Marden) | independent: the radar extract's pixel pairs | Component 2 |
| R4 | the share of the hail storms' 60-minute maximum that the tips miss at Costarossa (23.4 per cent) | investigation-loops | the detector's ten-minute record of what fell and when; the tips of the same storms | 22.7 to 28.6 per cent | stopped at the first story: the hail days' totals close against the storage gauge like any other day's, so the tips are taken as rain where they stand (a share of nil) | independent: the detector's blocks against the tips of the same storms | Component 3 |
| R5 | the triggering storms a season to expect at each crossing (Rio Toval 12.39, Rio Ciadin 10.50, Rio Marden 4.50, Rio Gelt 4.44, Rio Bianc 4.11, Rio Sass 1.83, Rio Larin 0.50) | forecasting | regulation 2.1 to 2.4 and 3.1; the crossings register's triggering depths; R2 to R4 carried to every storm of 2009 to 2026 | per crossing (Rio Gelt 3.55 to 5.00, Rio Marden 3.77 to 4.94, Rio Bianc 3.83 to 5.05) | dismissed own evidence: one factor, the rainfall normal's ratio and the hail days' tips together file Rio Gelt 1.17, Rio Marden 0.50 and Rio Bianc 1.94 | R2, R3, R4 | Ask 1 |
| R6 | the 60-minute depth each source area reaches five times a season (Rio Marden 18.6 mm, Rio Toval 17.7, Rio Ciadin 17.1, Rio Gelt 16.3, Rio Larin 15.2, Rio Bianc 15.1, Rio Sass 13.2) | uncertainty | regulation 2.3, 3.1 and 3.2; R2 to R4 | per crossing (Rio Gelt 15.7 to 17.1 mm, Rio Marden 18.1 to 19.4, Rio Bianc 14.7 to 16.1) | dismissed own evidence: read on the same three shortcuts' storm maxima it files Rio Gelt 14.1 with S1 lost, Rio Marden 14.3 with S2 lost and Rio Bianc 13.0 with S3 lost | R2, R3, R4 | Ask 2 |
| R7 | each crossing's class: class 3 at Rio Toval, Rio Ciadin, Rio Marden, Rio Gelt and Rio Bianc; class 2 at Rio Sass; class 1 at Rio Larin | synthesis | regulation 4.1 (class 3 from 3.0 a season, class 2 from 1.0) | exact | dismissed own evidence: the reflex route files Rio Gelt and Rio Bianc in class 2 and Rio Marden and Rio Sass in class 1 | R5 | Recommendation |

Carry-forward: every graded figure sits downstream of a stump and ten of the fourteen ask figures of two or three. R2's under-read at Valfosca falls with S1 alone and is S1's own figure; R3's burst factor at Rio Marden falls with S2 alone and is S2's own; R4's share at Costarossa falls with S3 alone and is S3's own. On the cut pack R5's seven counts leave their bands with S1 on three (Rio Gelt, Rio Ciadin, Rio Sass), with S2 on five (all but Rio Gelt and Rio Larin, whose count at 0.83 sits a storm inside the room above its band's top) and with S3 on six (all but Rio Gelt: Valfosca sees hail in 72 of its storms); R6's seven depths with S1 on five (all but Rio Bianc and Rio Larin), with S2 on six (all but Rio Toval) and with S3 on four (Rio Bianc, Rio Ciadin, Rio Marden, Rio Sass). Four figures hang on one stump (Rio Gelt's count and Rio Toval's depth on S1, Rio Larin's depth on S2, Rio Larin's count on S3). R7 moves when any one stump is lost. S1 moves fewer figures than the other two because the 0.2 mm buckets of Pradalt, Costarossa and Malga Sora lose 12.6 per cent at 100 mm an hour against 20.2 on the 0.1 mm buckets, which is why a run that loses S1 alone earns the most of the three (45). R1's account is reflex work every route does; its factors are stated only in the Step-by-Step.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a tipping bucket loses the water that arrives while it tips, in proportion to the rate | constructed, the documented behaviour of tipping-bucket gauges | no: all six stations, both bucket models, every tipped minute of eighteen seasons (a true 100 mm an hour reads 12.6 per cent low on the 0.2 mm buckets and 20.2 on the 0.1 mm ones) | modelling: one factor leaves an account residual at every station that runs with each interval's rain rate (1.88 to 5.59 mm rms, r 0.81 to 0.92) | modelling (a loss fitted on the rate through the account and put back before any 60-minute window) | keep |
| a source area's cloudbursts stand in a ratio of their own to its station's, unrelated to the ratio of their yearly rainfall | constructed, orographic and convective contrast between a valley floor and the slopes above it | no: all eleven source areas (0.79 to 1.38), the four of the research valley included | modelling: the radar's pixel pairs storm by storm, set against the rainfall normal | modelling (a contrast measured on pairs and carried to the station's corrected maxima, the radar's own depths never used) | keep |
| an unheated funnel holds hail and graupel and the bucket tips the melt over the next hour or two | constructed, the documented behaviour of unheated gauges in solid precipitation | no: every station (72 storms at Valfosca to 391 at Costarossa) | modelling: the tips of a hail storm against the detector's blocks (22.5 to 27.0 per cent of the tipped water lies in blocks where the detector saw no precipitation, 0.01 to 0.02 per cent on rain storms) | modelling (the storm's water placed in time by the detector's record, the amount kept from the bucket) | keep |
| the radar's 60-minute maximum carries an error common to a cell's whole footprint, wider where the radar sees a valley worse, and reads low overall | constructed, the documented behaviour of a weather radar in mountain terrain (partial beam blockage, range, the vertical profile) | no: every cell at all six stations, its spread 0.12 on logs at Valfosca to 0.37 at Rio Scuro, with no crossing governed by the noisiest station | modelling: the radar on a station's own pixel against the station's depths, station by station (a scatter of 0.27 to 0.44 on logs) | none on the golden's route (the factor is one number over a cell's footprint and leaves the ratio of two pixels of the same cell untouched); it is why the radar's depths cannot be counted against a point depth or carried from one valley's gauges to another | keep: it opens no member and no figure of the golden moves with it |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each station's account against its storage gauge | Missed | Right | Right |
| R2 each bucket model's loss by rate | Missed | Missed | Right |
| R3 each source area's burst factor | Missed | Missed | Right |
| R4 the share of hail storms' 60-minute maximum the tips miss | Missed | Missed | Right |
| R5 the triggering storms a season at each crossing | Missed | Missed | Right |
| R6 the 60-minute depth each source area reaches five times a season | Missed | Missed | Right |
| R7 each crossing's class | Missed | Missed | Right |
| Roughly | 0 of 7 | 1 of 7 | 7 of 7 |

Measured by: generator/core.py on corelib.py at the draw (the rubric table of ## Stump core); .claude/skills/stumping/effort.py on generator/effort.json on the cut pack (2026-11-17, cut cdbf08e67703c82d: quick 9.0, careful 26.7, thorough 100), and corelib re-run on the cut pack by generator/results.py (level 5; figure by figure, one stump lost: S1 45.0, S2 33.7, S3 37.5; one stump fixed alone 27.0, 15.7, 23.2; the reflex route 12.8; the rigorous standard route 9.0)
Largest single hint: the tipping buckets lose water while they tip, more the harder it rains; rescues 1 of 7 results (R2; 27 rubric points with S1 fixed alone on the reflex route, three classes still wrong)
Pair estimate: 26.7 (effort.py on the cut pack: the reflex route earns instruction-following and R1, the account every route rebuilds, which effort.py counts as a third of the asks' weight although no block grades it; figure by figure corelib prices the same route at 12.8, where the one figure it lands is Rio Larin's depth. A model, not a measurement: the platform's two runs are the measurement)

## Stump core

From `python3 task3/generator/core.py` (seed 20270213; six stations, eighteen seasons, 6,228 storms on the minute arrays, before any file), every figure as printed; the cut pack's tables, recomputed from the shipped files by `generator/results.py`, follow them.

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| Rio Bianc | 1/3 | 4.222 | 0.222 | 1.889 | 1.167 | 2.214 | S3 |
| Rio Ciadin | 1/3 | 10.39 | 0.611 | 15.56 | 5.444 | 7.643 | forced |
| Rio Gelt | 1/3 | 4.333 | 0.389 | 1.167 | 0.6667 | 2.071 | S1 |
| Rio Larin | 1/3 | 0.5 | 0.167 | 0.3333 | 0.3333 | 0.07143 | forced |
| Rio Marden | 1/3 | 4.333 | 0.389 | 0.5 | 0.2222 | 1.286 | S2 |
| Rio Sass | 1/3 | 1.778 | 0.333 | 0.5 | 0.5 | 0.4286 | forced |
| Rio Toval | 1/3 | 12.39 | 0.556 | 7.111 | 6.167 | 8.5 | forced |

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| C1 the Valfosca bucket's under-read at 100 mm an hour (per cent) | components | 19.46 | 18.88 to 22.42 | moves | - | - | lost |
| C2 burst factor, Rio Marden against Pradalt | components | 1.381 | 1.339 to 1.422 | - | moves | - | lost |
| C3 hail storms' 60-minute maximum the tips miss, Costarossa (per cent) | components | 24.44 | 23.7 to 25.17 | - | - | moves | lost |
| Rio Bianc | asks | 4.222 | 4.053 to 4.444 | moves | moves | flips | lost |
| Rio Ciadin | asks | 10.39 | 9.778 to 10.8 | moves | moves | moves | lost |
| Rio Gelt | asks | 4.333 | 4 to 4.722 | flips | moves | - | lost |
| Rio Larin | asks | 0.5 | 0.48 to 0.6667 | moves | moves | moves | lost |
| Rio Marden | asks | 4.333 | 3.944 to 4.611 | moves | flips | moves | lost |
| Rio Sass | asks | 1.778 | 1.707 to 2.111 | moves | flips | moves | lost |
| Rio Toval | asks | 12.39 | 11.83 to 12.88 | moves | moves | moves | lost |
| depth on the line, Rio Bianc | asks | 15.06 | 14.84 to 15.34 | moves | moves | moves | lost |
| depth on the line, Rio Ciadin | asks | 17.09 | 16.69 to 17.35 | moves | moves | moves | lost |
| depth on the line, Rio Gelt | asks | 16.26 | 16.01 to 16.76 | moves | moves | - | lost |
| depth on the line, Rio Larin | asks | 15.22 | 14.67 to 15.45 | moves | moves | moves | lost |
| depth on the line, Rio Marden | asks | 18.72 | 18.44 to 19 | moves | moves | moves | lost |
| depth on the line, Rio Sass | asks | 13.26 | 13.06 to 13.46 | moves | moves | moves | lost |
| depth on the line, Rio Toval | asks | 17.67 | 17.04 to 17.93 | moves | moves | moves | lost |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 22 |
| S2 lost alone | wrong | 22 |
| S3 lost alone | wrong | 30 |
| S1 fixed alone | wrong | 23 |
| S2 fixed alone | wrong | 16 |
| S3 fixed alone | wrong | 23 |
| reflex route (every stump lost) | wrong | 9 |
| rigorous standard route | wrong | 9 |

CORE PASS level 5

The cut pack (`python3 task3/generator/results.py`: the same corelib on figures recomputed from the shipped files, the tips quantised to whole buckets and whole seconds, 1,216 variants):

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| Rio Bianc | 1/3 | 4.111 | 0.389 | 1.944 | 1.222 | 2.214 | S3 |
| Rio Ciadin | 1/3 | 10.5 | 0.833 | 15.89 | 5.722 | 7.643 | forced |
| Rio Gelt | 1/3 | 4.444 | 0.667 | 1.167 | 0.6667 | 2.071 | S1 |
| Rio Larin | 1/3 | 0.5 | 0.111 | 0.3333 | 0.3333 | 0.07143 | forced |
| Rio Marden | 1/3 | 4.5 | 0.667 | 0.5 | 0.2778 | 1.286 | S2 |
| Rio Sass | 1/3 | 1.833 | 0.389 | 0.5 | 0.5556 | 0.4286 | forced |
| Rio Toval | 1/3 | 12.39 | 0.778 | 7.222 | 6.111 | 8.571 | forced |

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| C1 the Valfosca bucket's under-read at 100 mm an hour (per cent) | components | 20.16 | 17.6 to 24.9 | moves | - | - | lost |
| C2 burst factor, Rio Marden against Pradalt | components | 1.381 | 1.33 to 1.43 | - | moves | - | lost |
| C3 hail storms' 60-minute maximum the tips miss, Costarossa (per cent) | components | 23.44 | 22.7 to 28.6 | - | - | moves | lost |
| Rio Bianc | asks | 4.111 | 3.83 to 5.05 | - | moves | flips | lost |
| Rio Ciadin | asks | 10.5 | 9.66 to 11.17 | moves | moves | moves | lost |
| Rio Gelt | asks | 4.444 | 3.55 to 5 | flips | - | - | lost |
| Rio Larin | asks | 0.5 | 0.44 to 0.73 | - | - | moves | lost |
| Rio Marden | asks | 4.5 | 3.77 to 4.94 | - | flips | moves | lost |
| Rio Sass | asks | 1.833 | 1.55 to 2.47 | moves | flips | moves | lost |
| Rio Toval | asks | 12.39 | 11.61 to 13.3 | - | moves | moves | lost |
| depth on the line, Rio Bianc | asks | 15.05 | 14.7 to 16.1 | - | moves | moves | lost |
| depth on the line, Rio Ciadin | asks | 17.11 | 16.5 to 17.6 | moves | moves | moves | lost |
| depth on the line, Rio Gelt | asks | 16.26 | 15.7 to 17.1 | moves | moves | - | lost |
| depth on the line, Rio Larin | asks | 15.24 | 14.4 to 15.6 | - | moves | - | earned |
| depth on the line, Rio Marden | asks | 18.62 | 18.1 to 19.4 | moves | moves | moves | lost |
| depth on the line, Rio Sass | asks | 13.19 | 12.9 to 13.9 | moves | moves | moves | lost |
| depth on the line, Rio Toval | asks | 17.71 | 16.8 to 18.3 | moves | - | - | lost |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 45 |
| S2 lost alone | wrong | 34 |
| S3 lost alone | wrong | 37 |
| S1 fixed alone | wrong | 27 |
| S2 fixed alone | wrong | 16 |
| S3 fixed alone | wrong | 23 |
| reflex route (every stump lost) | wrong | 13 |
| rigorous standard route | wrong | 9 |

CORE PASS level 5  task3 architecture 8, cut pack

The labelled lines below state the cut pack's figures, with the draw's beside them where a line turns on one.

Unobserved part: the storms a season in which the rain at a crossing's source area reaches the crossing's triggering depth in 60 consecutive minutes, over the 2027 to 2031 programme. No record holds it: no gauge stands in a source area, the seasons have not happened, and three parts of the quantity are missing from the one long record there is: the water the bucket lost in the hardest minutes, what the source area got against the station in each storm, and when a hail storm's water fell.
Instruments: the tipping bucket sees every storm of eighteen seasons tip by tip at the station, less what it loses by rate and with hail storms' water delayed; read raw against the triggering depths it files Rio Gelt 0.67, Rio Marden 0.28 and Rio Bianc 1.22 storms a season (the direct route). The storage gauge sees the true depth of each visit interval and nothing inside it. The detector sees when precipitation fell and of what kind every ten minutes, with an optical intensity that scatters around the tipped totals by 0.30 to 0.32 on logs. The radar sees the source pixel and the station pixel in the same storm from 2013, as area averages on its own scale, with an error common to a cell's footprint whose spread differs valley by valley; read as the answer it files Rio Gelt 2.29, Rio Marden 2.21 and Rio Bianc 2.64 adjusted to the stations by one factor, and 2.07, 1.29 and 2.21 matched to the research valley's weighing gauges. The rainfall normal sees yearly totals at every cell; read as the transfer it files Rio Marden 1.39 and Rio Ciadin 18.94.
Referee: the Rio Scuro research valley, where weighing gauges stood at four source areas for fourteen seasons (2013 to 2026) above a road station with the same bucket, storage gauge and detector as the others; none of the seven crossings is in it. The mean 60-minute depth of each source's five largest storms a season is 15.53 mm at the weighing gauges; the golden's method files 15.47 (off by 0.06), the bucket put back by one factor 14.01, the source scaled by the rainfall normal 21.24, the hail days' tips taken as rain 14.35 and the gauge read raw 14.22 (each rival's miss 1.18 to 5.71 mm against the golden's 0.06). The depth reached five times a season and the triggering storms seen agree: 11.62 mm and 190 storms at the weighing gauges, 11.68 and 197 by the golden, 10.81 and 141 by one factor, 16.03 and 556 by the rainfall normal, 10.72 and 149 with hail taken as rain. The radar's own depths are not scored here: both radar routes are in sample at the valley (the one-factor product counts 197 storms and the gauge-matched depths 193), so they are ruled on where the stations stand (Strongest standard route). Read raw as a calibration of the bucket (source over bucket 0.996, carried to every crossing) the valley files the direct route's classing, because its sources get 0.79 to 0.90 of their station's bursts and the crossings' sources 0.95 to 1.38.
Strongest standard route: on every open member, the radar's own depths matched rank for rank to the research valley's weighing gauges and counted at the source pixel against the triggering depth (Rio Gelt 2.07, Rio Marden 1.29, Rio Bianc 2.21, Rio Sass 0.43: class 2, 2, 2 and 1), with the one-factor product beside it (2.29, 2.21, 2.64 and 0.43, the same four classes). Neither holds outside the valley it was made in: set on each station's own pixel the gauge-matched depths file 51 to 67 per cent of the 12 mm storms the station's own depths hold at the five stations outside the valley (101 of 110 at Rio Scuro), the radar's scatter about the station's depth runs from 0.27 on logs at Valfosca to 0.44 at Rio Scuro, and the radar holds 14 of the 18 seasons regulation 3.1 counts (`checks.py` SF22). The careful gauge route (one factor, the rainfall normal's ratio, the hail days' tips) files Rio Gelt 1.17, Rio Marden 0.50, Rio Bianc 1.94 and Rio Sass 0.50; refuted piece by piece by the account's residual (5.59 mm against 1.36 at Valfosca), the valley's sources against the rainfall normal (0.79 to 0.89 seen where it says 1.09 to 1.24) and the detector (22.5 per cent of Costarossa's hail storms' tipped water in blocks where it saw no precipitation).
Said out loud: S1 "the tipping buckets lose water while they tip, more the harder it rains": four steps left (the account interval by interval on the tips' rates, the loss fitted by bucket model, the tipped water put back before any window, the form and the reading of the rate chosen and defended). S2 "a source area's cloudbursts are not its station's and do not scale with its yearly rainfall": four steps left (the pixel pairs matched storm by storm on one clock, the contrast estimated as a ratio and not as a depth, its carry to the four seasons before the radar, the check on the valley's sources). S3 "on hail days the funnel holds the ice and the bucket tips its melt after the storm has gone": four steps left (the hail storms found from the detector's codes, the tipped water placed in time on the detector's profile, the amount kept from the bucket after the loss is put back, the check on the valley's hail storms).
Worth: on the cut pack S1 is worth 2.06 storms a season on Rio Gelt, 3.1 times the family's spread of 0.667; S2 3.11 on Rio Marden, 4.7 times 0.667; S3 1.56 on Rio Bianc, 4.7 times 0.333 (at the draw 2.00, 2.94 and 1.61, 5.1, 7.6 and 7.2 times). Each open member's family stays 0.78 to 0.83 above the line of 3.0 (Rio Gelt 3.78, Rio Marden 3.83, Rio Bianc 3.83 at the lowest) and each stump's drop lands 0.44 to 1.61 under it (2.39, 1.39, 2.56).
Regimes: second stump on every member. S1's loss is checked on every station's account and cannot be checked inside a single storm; it is largest at the two 0.1 mm stations of the crossings (Valfosca and Forcella) and opens Rio Gelt. S2's contrast is checked on the research valley's four sources and cannot be checked at a crossing's source; it runs from 0.95 to 1.38 against rainfall ratios of 0.90 to 1.40 with no relation between them, and opens Rio Marden (and moves Rio Sass with it). S3's timing is checked on the valley's hail storms; it matters by the station's count of hail storms (72 at Valfosca, 391 at Costarossa) and opens Rio Bianc.
Sharp: S1: its wrong route passes the control total (one factor closes each station's account in every season, and on held-out seasons); its right route commits to a loss by rate that no file states; the evidence is in the visit book against the tips' rates; the correction is not a constant (20 per cent at 100 mm an hour on one bucket, 13 on the other, a few per cent in ordinary rain); its own figure is Valfosca's under-read. S2: its wrong route is the field's standard index (the rainfall normal) and agrees with the station on ordinary days; its right route commits to a ratio from an instrument whose depths are wrong; the evidence is in the radar's pairs and the valley's gauges; the correction's sign differs across members (Rio Marden up by 30 per cent against the normal, Rio Ciadin down by 24, Rio Sass up by 9); its own figure is Rio Marden's burst factor. S3: its wrong route passes the account (a hail day's total is right); its right route commits to moving water in time on a record that has no amounts; the evidence is in the detector's blocks against the tips; the correction runs from nil at a station with little hail to a quarter of the 60-minute maximum on Costarossa's hail storms; its own figure is that share.
Earns: on the cut pack a run that loses only S1 earns 45, only S2 34, only S3 37 (50 or under each); the reflex route earns 13 and the rigorous standard route 9 (30 and 50 or under), and the reflex route lands one graded figure as a near miss (Rio Larin's depth, 14.3 against a floor of 14.4); S1 fixed alone earns 27, S2 fixed alone 16, S3 fixed alone 23 (each more than the reflex route's 13 and a third at most). At the draw the same lines were 22, 22 and 30, 9 and 9, and 23, 16 and 23; the cut pack is higher because the battery now holds every reading of the rate the account cannot refuse, which widens the bands on the stations where S1 moves least, and because each band's top stands a storm and a tenth of a millimetre above its widest way (the judge's rebuild room, SF26), which lets the S2-lost route's Rio Larin count (0.83) in as a near miss.

## Stump factorial

Reflex route: the tips, the detector, the visit book and the radar brought to one clock; re-sent logger blocks and the technicians' tip tests left out; storms separated as the regulation files them; the 60-minute maximum taken over every sliding window, a storm counted once; each station's account closed against its storage gauge with one factor; each station carried to its source areas by the rainfall normal's ratio; the hail days' tips taken as rain; the mean over the eighteen seasons, with a hold-out of seasons and a bootstrap. On the cut pack it files class 3 at Rio Ciadin (15.89) and Rio Toval (7.22), class 2 at Rio Bianc (1.94) and Rio Gelt (1.17) and class 1 at Rio Marden (0.50), Rio Sass (0.50) and Rio Larin (0.33): four classes wrong, 13 on the rubric.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 what the bucket loses rises with the rate, so the loss is fitted on the tips' rates through the storage gauge account and put back before any window | stump | one factor per station that closes the account | N21, L28 | Rio Gelt class 2 (2.39) | Rio Bianc class 2 (2.00), Rio Marden class 2 (1.00) and Rio Sass class 1 (0.67), three classes still wrong; rescues R2 | no: the account on rates, the fit by bucket model, the put-back before any window, the form and the reading of the rate |
| S2 a source area's bursts against its station's are measured on the radar's pixel pairs as a ratio, and the yearly rainfall does not carry them | stump | the station carried to its source by the rainfall normal's ratio | N26, N01 | Rio Marden class 2 (1.39) and Rio Sass class 1 (0.94) | Rio Bianc class 2 (2.06), Rio Gelt class 2 (2.17), Rio Marden class 2 (2.50) and Rio Sass class 1 (0.56), four classes still wrong; rescues R3 | no: the pairs on one clock, a ratio and not a depth, the seasons before the radar, the valley's check |
| S3 on hail days the tips have the storm's water and the detector has its minutes | stump | the hail days' tips taken as rain where they stand | N30, L26 | Rio Bianc class 2 (2.56) | Rio Gelt class 2 (1.39), Rio Marden class 1 (0.83) and Rio Sass class 1 (0.78), three classes still wrong; rescues R4 | no: the hail storms from the detector's codes, the water placed on its profile, the amount kept from the bucket, the valley's check |
| J4 the tips and the detector on the loggers' clock, the visit book in civil time, the radar and the research valley in UTC, brought to one clock | reflex | - | R01, R46 | same call | - | - |
| J5 re-sent logger blocks and the technicians' tip tests left out | reflex | - | R01 | same call | - | - |
| J6 the largest total over every 60 consecutive minutes, a storm counted once | reflex | - | R06; regulation 2.3 | same call | - | - |
| J7 the season, the storm separation, the lines and the eighteen-season mean as filed | reflex | - | regulation 2.1, 2.2, 3.1 and 4.1 | same call | - | - |
| J8 each station's account set against its storage gauge | reflex | - | R93 | same call | - | - |
| J9 a hold-out of seasons and a bootstrap of seasons on whatever route is built | reflex | - | R03, R04 | same call | - | - |

Level: 5: three necessary stumps, none sufficient alone, the three single drops on three distinct wrong classings and the seven shortcut routes of the lattice on seven.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| Rio Gelt | 4.44, class 3 (1.44 above 3.0) | 0.667 | 1.17, class 2 (wrong) | 0.67, class 1 (wrong) | S1 |
| Rio Marden | 4.50, class 3 (1.50 above 3.0) | 0.667 | 0.50, class 1 (wrong) | 0.28, class 1 (wrong) | S2 |
| Rio Bianc | 4.11, class 3 (1.11 above 3.0) | 0.333 | 1.94, class 2 (wrong) | 1.22, class 2 (wrong) | S3 |
| Rio Sass | 1.83, class 2 (0.83 above 1.0) | 0.389 | 0.50, class 1 (wrong) | 0.56, class 1 (wrong) | S2 (with Rio Marden: S2 dropped alone files 0.94; it has no stump of its own, and on the reflex route it comes back only with S2 and one of the other two) |
| Rio Ciadin | 10.50, class 3 (7.50 above 3.0) | 0.833 | 15.89, class 3 (right) | 5.72, class 3 (right) | forced (its figures are wrong on every shortcut route) |
| Rio Toval | 12.39, class 3 (9.39 above 3.0) | 0.778 | 7.22, class 3 (right) | 6.11, class 3 (right) | forced (as Rio Ciadin) |
| Rio Larin | 0.50, class 1 (0.50 under 1.0) | 0.111 | 0.33, class 1 (right) | 0.33, class 1 (right) | forced |

Direct route: the pack's most direct evidence read at face value is each governing station's tips as they stand, their largest 60 consecutive minutes counted against the crossing's triggering depth (the `direct` route of `generator/analysis.py`; `estimate(W, "raw", "one", "tips")` in `generator/core.py`): it loses the buckets' shortfall, the source areas' contrast and the hail storms' minutes at once and files Rio Gelt 0.67, Rio Marden 0.28, Rio Bianc 1.22 and Rio Sass 0.56, four classes wrong. The research valley read as a calibration and carried to every crossing (`carried`) files the same classing (0.67, 0.28, 1.17, 0.50), and the radar product counted at the source pixel (`radar`) files 2.57, 2.36, 2.21 and 0.43, four classes wrong.

## Data provenance

Source: generated by `task3/generator` from a simulated process: convective storms over a valley (a cell's strength, its place-to-place variation with a reach of about five kilometres, a burst of 5 to 24 minutes with a trailing rain), long light rain between them, and the instruments that record them (tipping buckets of two models, storage gauges read at a monthly visit, present-weather detectors, a weather radar's storm maxima, four weighing gauges in one research valley). Synthetic; the valley, the road and the service are invented.
Behaves like the real thing: tipping buckets under-read in proportion to the rate (12.6 and 20.2 per cent at 100 mm an hour here, inside the range intercomparisons report for uncorrected gauges); unheated gauges delay solid precipitation by the funnel's melt; a radar's hourly accumulation on a one-kilometre pixel is smoother than a point gauge, reads low overall and carries an error common to a cell's footprint that is wider where the radar sees a valley worse (0.12 to 0.37 on logs across the six stations); storm counts are Poisson by season, 60-minute maxima are heavy-tailed, storms cluster in June to August, and long rain makes more than half of a season's water.
Genuine patterns: (1) the seasonal cycle of storms (30 per cent in July, 4 in October); (2) heavy-tailed 60-minute maxima whose largest storms are the shortest and hardest; (3) hail and graupel in the stronger cells and at the higher stations (72 hail storms at Valfosca, 391 at Costarossa); (4) season-to-season variation in storm counts and in the account's closure; (5) place-to-place variation inside a storm that decays with distance, so nearer source areas follow their station more closely.
Problems by process: three clock conventions (the loggers on UTC+1 all year, the visit book in civil time, the radar and the research valley in UTC); logger restarts that re-send a block; the technicians' tip tests at visits; visit days that slip; a radar pixel renumbered at the agency's re-gridding; no radar before 2013; no weighing gauge anywhere but the research valley's sources. Each comes from the instrument or the routine that produces the file, and none sits only where a result is decided.
License: none needed (generated).
Used as is: not applicable (generated).
Breadth: six stations by eighteen seasons of tips (905,097 rows), 648 visit intervals, six stations' detector blocks in one database, the radar's maxima on the station and source pixels and their neighbours for fourteen seasons (56,065 rows), a rainfall normal grid, eleven source areas, four weighing gauges; which storms, which stations and which pixels to read for which part of the quantity is the work. Nineteen files, 51 MB.

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, modeling, investigation-loops, forecasting, uncertainty, synthesis
Question form: where (where an automatic barrier, where a seasonal patrol, where signs)
Nearest build: task17 and task10 architecture 7 share the answer shape and the weight (a distribution cut, modeling). task17 counts units over a line from one fitted relation after an assembly; task10's last architecture read a design-day demand where a service never ran. Here the distribution is each source area's seasonal storm maxima, cut at two lines into three classes, and the modeling is three instrument models with nothing shared: no chain step of either build recurs in the same place. The deliverable set (a CSV and a workbook) repeats task1's by the house rule; what differs is what each holds (one row per crossing with its class, storms a season and depth; a workbook that opens on the classing with the station corrections and the research valley's check behind it). `stock_flow_accounting` is on three live builds (mark120, task4, task9) as a balance closed over periods; here it labels the funnel's ice store, read in reverse, and is one of three lessons. `precut.py` also names task2 (the approved correction ceiling for a speech recognizer's 2027 staff) on the answer shape: it carries a tail to people who have not used the system by assigning three partial samples, and nothing is transported to a new population here (the units are storms at fixed places, and what differs between records is the instrument). mark126 shares the gap, generator and Gate G triple and nothing of the work (it split joined units to restate a median duration; nothing here is joined or split).

## Frontier check

Precedents: R2 careful Missed on L28 (the estimator certified with checks that cannot see the problem) and N21 (an unmeasured component placed across the system in proportion to the metered quantities); R3 Missed on N26 (one remote station taken to stand for the conditions at the place, named and left untested) and N01 (a quantity assumed to scale in proportion); R4 Missed on L26 (a plausible shallower explanation that passes its own checks) and N30 (a total taken as constant over its duration); R5 to R7 Missed on N21, N26 and L26 together.
Shallow path checks: one factor per station closes every season's account exactly and predicts held-out seasons' totals, so its own check passes; only the account interval by interval against the tips' rates refutes it (a residual of 5.59 mm rms at Valfosca that runs with the interval's rain rate, r 0.90, against 1.36 mm once the loss is fitted on the rate), and the research valley's gauges (14.01 mm against 15.53). The rainfall normal's ratio is the field's standard index and no check on the stations can see it fail; only the radar's pixel pairs (1.381 at Rio Marden against 1.06) and the valley's sources (0.79 to 0.89 of their station's bursts where the normal says 1.09 to 1.24) refute it. The hail days' tips pass the account (a hail day's total is right) and any check on totals; only the detector's blocks refute them (22.5 per cent of the hail storms' tipped water at Costarossa lies in blocks where the detector saw no precipitation, 0.01 per cent of the rain storms'), and the valley's gauges (14.35 against 15.53).
Assumption made false: the storage gauge's excess is spread like the tipped water (false: the bucket loses in proportion to the rate; tested by the visit book against the tips' rates); the station stands for its source area up to the ratio of their yearly rainfall (false: bursts are convective and local, totals are orographic; tested by the radar's pairs and the research valley); the minutes the tips arrive are the minutes the rain fell (false on hail and graupel days: the funnel is unheated; tested by the detector's blocks).
Forcing: the lines are 3.0 and 1.0 storms a season. On the cut pack the 1,216 variants' nearest approach to a line is Rio Larin at 0.61, 0.39 under 1.0, then Rio Sass at 1.56 (0.56 above 1.0), Rio Gelt at 3.78 (0.78 above 3.0), Rio Marden and Rio Bianc at 3.83; every variant files the golden's seven classes, and so do the 512 crosses of the first-order form (Rio Gelt 3.56 at the lowest), the 432 crosses of the hail storms' water laid on the hail-coded blocks alone (304 with the battery and 128 with the first-order form; held in the bands, SF24) and the 190 crosses of the two pixels matched rank for rank (refused, SF23; Rio Sass 2.72 at the highest, 0.28 under 3.0). The shortcuts land across a line: S1 lost puts Rio Gelt at 2.39, S2 lost Rio Marden at 1.39 and Rio Sass at 0.94, S3 lost Rio Bianc at 2.56, the reflex route 1.17, 0.50, 1.94 and 0.50, the radar's depths matched to the valley's gauges 2.07, 1.29, 2.21 and 0.43. Each fitted input moved by a fifth leaves the classing unchanged: the fitted loss times 0.8 and 1.2 (Rio Gelt 3.56 and 5.22), each burst factor's distance from one times 0.8 and 1.2 (Rio Marden 3.39 and 5.56), the hail storms' put-back times 0.8 and 1.2 (Rio Bianc 3.89 and 4.72); the nearest any of the six comes to a line is 0.33 (Rio Larin at 0.67 with the loss times 1.2). Thin: the loss at 0.8 leaves Rio Gelt 0.56 above the line and the burst factor at 0.8 leaves Rio Marden 0.39 above it. A seed sweep at the draw (run once with the depth ask then at three a season, not kept as a script) passed every corelib check on 14 of 48 seeds, so the build reuses `core.build(SEED)` and moves nothing.
Noun swap: nearest on file by `skeleton.py check`: severity none against every card, the client's corpus and the slot's lineage. task23 and task6 share the anatomy of a quantity no instrument holds and one detection (a control total that does not close); their decision forms, answer patterns, lessons and mechanisms differ, and swapping either's nouns in carries no deciding lesson across.
Closed strategies: the call turns on nonlinear_functional_of_path (a loss convex in the rate, so the factor that closes the totals is its mean and not its value in the minutes that decide), on support_effect (an area average against a point depth, used only as a ratio) and on stock_flow_accounting read in reverse (a store that delays the record). Nearest closed cards: a change of instrument (no instrument changes here: each has one behaviour throughout, and the fix is a model of it, not a splice at a date); a noisy explanatory variable flattening a slope (the bucket's error is a bias that grows with the rate, not noise, and the fix is fitted through a second record); counts still filling in (the hail storms' water arrives within two hours and no completion by age recovers its minutes); transport to a new mix (the burst factor is a contrast between two places in the same storms, not a rate carried to another population). No closed lesson is kept as a supporting step: the regulation files the long-run mean, so no trend, selection or censoring step exists on any route.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a storm | rain separated from the next by six hours without a tip at the governing station; three hours; eight hours | six hours | regulation 2.2 files six hours; no station's record holds a dry gap between three and eight hours, so the three readings give one catalogue: same call |
| SF2 | 60 consecutive minutes | every sliding window of 60 minutes by the minute; clock hours; windows anchored on the tips in continuous time | every sliding window, by the minute | regulation 2.3 ("any 60 consecutive minutes") rules out clock hours; windows anchored on the tips (the second implementation, `verify.py`) land inside every band: same call |
| SF3 | a storm with several exceedances | counted once; counted per exceedance | once | regulation 2.3 ("a storm counts once") |
| SF4 | the season | 1 May to 31 October, a storm by the day in which its largest 60 minutes fall (the day that holds their last second; the day they open; the day of the storm's first tip; the day on civil summer time or on UTC in place of the loggers' clock); the calendar year | 1 May to 31 October, a storm by the day that holds the last second of its largest 60 consecutive minutes | regulation 2.1 files the season and the day; the day the largest 60 minutes open moves one storm of the six stations to another season, the day of the first tip five, the day on UTC one and the day on civil summer time none, none of 9 mm in 60 minutes, and none of the four moves a graded figure (`checks.py` SF4): same call |
| SF5 | the storms a season to expect in the program | the mean over every complete warm season of the governing station's tip record (2009 to 2026); the radar years; the last ten seasons; a trend carried to 2027 to 2031 | the eighteen-season mean | regulation 3.1 files it; every season is complete at every station (5.1: in service from the opening round to the closing round; the visit book's opening rounds fall on 22 to 29 April and its closing rounds on 3 to 8 November in each of the eighteen years, `checks.py` SF5), and a mean of the seasons' counts is the pooled count over eighteen |
| SF6 | rain at the source area | the point depth at the source area; the catchment's average depth; the depth at the crossing | the point depth at the source area | the crossings register's column (triggering depth, point rain at the source area, mm in 60 minutes) and regulation 2.4 |
| SF7 | the lines | class 3 from 3.0 inclusive, class 2 from 1.0 inclusive; exclusive | inclusive | regulation 4.1; no variant puts a crossing within 0.38 of a line: same call |
| SF8 | the class's period | one class for the 2027 to 2031 program; a class a year | one class | regulation 1.2 |
| SF9 | the governing station | the station the crossings register files; the nearest station on the map | the register's | the crossings register; the two agree for every crossing: same call |
| SF10 | the rate the loss acts on | tip by tip (a tip's water over the time since the tip before); totals of one, two, three and five minutes, a tip's water spread or kept in its own minute; totals of ten and fifteen minutes | one-minute totals, a tip's water spread over the time since the tip before | tip by tip and totals of one to five minutes are all in the battery (same call, inside every band; the account on the 0.1 mm buckets is left open by 1.27 to 1.93 mm rms, 1.28 as fitted); ten- and fifteen-minute totals leave it open by 1.73 to 2.44 times the fitted reading's and are not used, and they file the golden's classes all the same |
| SF11 | the loss's form and pooling | the tipping-time form; the same with a fixed factor fitted beside it; its first-order form; a power law of the recorded rate; one loss a bucket model or one a station | the tipping-time form, one a bucket model | the tipping-time form with and without the fixed factor, both poolings, and tip by tip the first-order form are in the battery: same call, inside every band. The first-order form on minute totals leaves the account open by 1.09 to 1.37 times the tipping-time form's on the same reading, which does not rule it out, so every stated band holds its 512 crosses and they file the golden's classes. A power law leaves it open by 1.44 to 2.25 times and is not used; it files the golden's classes too |
| SF12 | the under-read at 100 mm an hour | the share of a true rate of 100 mm an hour the bucket fails to record, under the fitted loss | 20.2 per cent | the band (17.6 to 24.9) holds every reading of the rate and form of the loss the account does not refuse (tip by tip 17.7 to 18.2, one-minute totals 19.4 to 20.4, five-minute totals up to 24.9) and the second implementation's 18.2 |
| SF13 | the burst factor | the mean log ratio of the source pixel's to the station pixel's 60-minute maximum over the storms where both reach 1 mm; the median; the ratio of sums; a trimmed mean; both pixels over 3 mm; the station pixel over 3 mm; the upper quarter by joint size; each storm carried by its own pair | the mean log ratio | all eight in the battery (1.377 to 1.388 at Rio Marden): same call, inside every band |
| SF14 | cruder burst factors | the source pixel regressed on the station pixel through the origin; the largest quarter of storms chosen on the station pixel; the two pixels' upper deciles unpaired | not used | each by a figure from the radar extract: the regression gives 1.370 at Rio Marden and its reverse 1.393; the largest quarter chosen on the station pixel gives 1.361 and chosen on the source pixel 1.399; the unpaired upper deciles differ between odd and even seasons by up to 5.8 per cent where the paired mean differs by 1.5 at most. All three file the golden's classes |
| SF15 | the burst factor before 2013 | the factor measured on 2013 to 2026 applied to 2009 to 2012; the radar years only | applied to all eighteen seasons | regulation 3.1 (every complete season of the tip record); the station register shows no station or source moved |
| SF16 | a hail storm | a storm with one or more detector blocks coded hail or graupel; every storm of a day that holds such a block | a storm with such a block | the detector's code list; the day reading adds 105 storms across the six stations and moves no graded figure out of its band and no class: same call |
| SF17 | when a hail storm's water fell | placed on the detector's ten-minute profile; the same with the hail blocks' intensity rescaled to close the hail storms' totals; the tips kept up to the first hail block; one hail-day multiplier read at the research valley | the detector's profile | all four in the battery: same call, inside every band |
| SF18 | cruder hail handlings | only the water tipped in detector-dry blocks moved; the water spread evenly over the wet blocks; the detector's own amounts | not used | each by a figure: at the research valley the first files 15.02 mm and 173 triggering storms and the second 14.44 and 154 against 15.53 and 190 seen (golden 15.47 and 197); the detector's storm totals scatter around the tipped totals by 0.30 to 0.32 on logs on rain storms and its amounts file 16.01 and 224 |
| SF19 | the share of the hail storms' maximum the tips miss | one minus the hail storms' tipped 60-minute maxima (loss put back) over the same storms' maxima after placement, summed over Costarossa's hail storms of 2009 to 2026 | 23.4 per cent | the band (22.7 to 28.6) holds every loss reading and hail way of the battery, the hail-coded placing of SF24 (27.3 to 28.5) and the second implementation's 23.7 |
| SF20 | the depth reached five times a season | the 90th largest storm maximum of the eighteen seasons; an interpolated quantile; a level read from a fitted tail | the 90th largest | regulation 3.2 files a count on 3.1's seasons ("counted as in 2.3, in a mean of five or more storms a warm season": five a season over eighteen seasons is 90 storms), which a fitted level is not; the interpolated reading and a generalised Pareto tail over thresholds of 8 to 20 storms a season land inside every band (same call), and an exponential tail's level leaves two bands by 0.1 to 0.2 mm at depths the record reaches in 82 storms, fewer than five a season (`checks.py` SF20) |
| SF21 | the long rain between storms | in the account and in the catalogue; left out of the catalogue | in both | its largest 60-minute total is 5.95 mm against a lowest triggering depth of 12.5: same call |
| SF22 | the radar's own depths as the answer | the source pixel adjusted to the stations by one factor and counted against the triggering depth; the source pixel matched rank for rank to the research valley's weighing gauges and counted the same way | not used | each by figures from the radar extract and the tip logs: set on each station's own pixel the gauge-matched depths file 51 to 67 per cent of the station's own 12 mm storms at the five stations outside the valley (101 of 110 at Rio Scuro) and the one-factor product 51 to 69 per cent (102 of 110); the radar's scatter about the station's depth is 0.27 on logs at Valfosca and 0.44 at Rio Scuro; the radar holds 14 of the 18 seasons 3.1 counts; the triggering depths are point depths (SF6). Both land across the line on all four open crossings |
| SF23 | the burst factor without pairing the storms | the two pixels' depths matched rank for rank, each station depth carried by the pixels' ratio at its own rank | not used | its own halves: made on the odd and on the even seasons of the radar it moves a crossing's depth by up to 1.40 mm and its storms a season by up to 2.06, the paired mean by 0.26 mm and 0.56; crossed with the battery's 190 other choices it files the golden's seven classes: same call |
| SF24 | a hail storm's water laid on its hail-coded blocks alone | every drop of the storm placed on the blocks coded hail or graupel, by the detector's intensity | held in the bands | not refused cleanly (218 triggering storms at the research valley against 190 seen and the golden's 197), so its 432 crosses (304 with the battery, 128 with the first-order form of the loss, the other way the bands hold) sit inside every band; every one files the golden's seven classes and every shortcut lands below the bands it widens upward: same call |
| SF25 | the depth of 3.2, its count | the greatest depth reached in a mean of five or more storms a season over 3.1's seasons (the 90th largest of eighteen seasons); the mean of each season's fifth largest storm | the first | regulation 3.2 files it in those words; the second is another figure (Rio Bianc 16.0 against 15.1, Rio Ciadin 17.8 against 17.1) and the sentence does not read that way |
| SF26 | a tip's time stamp, and how the 60 minutes slide | the stamp as the end of its second and the 60 minutes on the loggers' clock minutes (a hail storm: six consecutive ten-minute blocks of the detector); the stamp as the start of its second; the 60 minutes slid by the second | the first | the Step-by-Step states it (steps 3, 4 and 6); the other readings move a count by one storm at up to four crossings (Rio Gelt 79, Rio Bianc 75, Rio Ciadin 190, Rio Toval 224) and a depth by up to 0.02 mm, no class moves, and every band's top stands a storm and a tenth of a millimetre above its widest way (`checks.py` SF26): same call |
| SF27 | which ways of the loss the bands hold | every reading of the tipping-time form in the battery and the first-order form (held); a power law of the recorded rate, and the tipping-time form on 10- or 15-minute totals (refused) | the cut on the storage account | each way refitted through the same account and scored on the 0.1 mm buckets' intervals: every way used or held leaves 2.14 mm or less and every way refused 2.22 mm or more (the fitted reading 1.28); the power law's exponent fits at 1.03 to 1.08, inside its limits, and the coarse totals' figure is stated with the fit's limit of 0.0075 hours per mm (a tighter limit leaves more); every one of them files the golden's seven classes (`checks.py` SF27): same call |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| the lines | 3.0 and 1.0 triggering storms a season | the regulation (.pdf), 4.1 |
| the season, the storm separation, the 60 consecutive minutes | 1 May to 31 October; six hours; any 60 consecutive minutes, once a storm | the regulation (.pdf), 2.1 to 2.3 |
| the expectation's basis | every complete warm season of the tip record, 2009 to 2026 | the regulation (.pdf), 3.1 |
| the depth's frequency | five times a season | the regulation (.pdf), 3.2 |
| each crossing's triggering depth and governing station | 17.0, 19.5, 16.0, 13.0, 12.5, 17.0, 29.0 mm in 60 minutes | the crossings register (.xlsx) |
| each station's bucket model and bucket size | 0.1 mm and 0.2 mm | the station register (.xlsx) and the tip logs' own increments (.csv) |
| the loggers' clock | UTC+1 all year | the station register (.xlsx) and the tip logs' own timestamps (.csv) |
| the loss per unit of rate | 0.00252 and 0.00144 hours per mm, fitted | estimated from the tip logs and the visit book (.csv); measured spread across the battery's nineteen ways of the loss and two poolings (17.7 to 24.9 per cent at 100 mm an hour on Valfosca's bucket) |
| each source area's burst factor | 0.948 to 1.381, fitted | estimated from the radar extract (.csv); measured spread across eight ways (1.377 to 1.388 at Rio Marden) |
| the hail storms' placement in time | the detector's ten-minute profile | the detector's blocks (.sqlite, read with the code list .csv); measured spread across four ways and the loss readings (22.7 to 24.8 per cent of the maximum at Costarossa, the stated band) |
| the hail-day multiplier of one battery way | 1.309 | estimated from the research valley's weighing gauges (.csv); measured spread: it is one of the four hail ways |
| the rainfall normal's ratios (the reflex route only) | 0.90 to 1.40 | the rainfall normal grid (.csv); no golden figure uses them |

Variant battery: 1,216 variants of the golden route on the cut pack in `generator/analysis.py` (nineteen ways of the loss: the tipping-time form alone or with a fixed factor beside it, on the rate read tip by tip or on totals of one, two, three and five minutes with a tip's water spread or kept in its own minute, and tip by tip its first-order form; by two poolings, by eight ways of the burst factor, by four ways of the hail storms), and every variant files the same call, the golden's seven classes; `generator/core.py` runs 512 on the minute arrays to the same call. The stated bands are the battery's range together with the first-order form on minute totals (512 more crosses, which the account does not refuse and which file the same classes), never tighter than the rebuild floor. The cruder rivals are run beside it and ruled out by named figures (SF10, SF11, SF14, SF18, SF22), and an independent second implementation (`generator/verify.py`, windows anchored on the tips in continuous time, the rate tip by tip) reproduces 30 of 30 stated figures inside their bands.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the seven gully crossings of the crossings register; each crossing's source area; every storm of the governing station's eighteen warm seasons |
| 2 | Unit of account: triggering storms a season; mm in 60 minutes; per cent of a rate; a ratio of 60-minute maxima |
| 3 | Attribution window: any 60 consecutive minutes inside a storm, a storm counted once (regulation 2.3) |
| 4 | As-of dating: the records close on 31 October 2026; the program is 2027 to 2031 |
| 5 | Version basis: the regulation in force for the 2027 to 2031 program (revision 4); the crossings register's current survey |
| 6 | Denominator: eighteen complete warm seasons (regulation 3.1) |
| 7 | Weighting: every season counts once; no storm is weighted |
| 8 | Window length: 1 May to 31 October; six dry hours between storms; 60 minutes |
| 9 | Boundary inclusivity: class 3 from 3.0 inclusive, class 2 from 1.0 inclusive; a depth equal to the triggering depth reaches it (regulation 2.3) |
| 10 | Rounding path: full precision to the end; storms a season stated to two decimals, depths to 0.1 mm, each with its band in the answer blocks |
| 11 | Tie-break: none needed; the nearest any variant comes to a line is 0.38 |
| 12 | Maturity and censoring: every season of the record is complete; nothing is still filling in |
| 13 | Order of operations: the clocks, the account, the loss put back, the hail storms placed, the 60-minute maxima, the carry to the source area, the count and the depth, the class |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: a re-sent logger block (same station, same tip times) counted once |
| 16 | Identity normalisation: one station code across the tip logs, the visit book, the detector's blocks and the registers; the radar's pixels by the pixel table's ids, the current numbering and the one in use until 2018 both listed there |
| 17 | Netting against gross: the technicians' tip tests left out of the tips (the visit book enters each visit's count beside its time); nothing else netted |
| 18 | Dimensional units: mm; mm an hour; the tips and the detector on the loggers' clock (UTC+1), the visit book in civil time, the radar and the research valley in UTC |
| 19 | Code and status semantics: the detector's precipitation codes as its code list gives them (rain; hail or graupel); the visit book's entry types |
| 20 | Integerisation: storms are whole; the seasonal mean is not rounded before the class |
| 21 | Clause scope: the classes apply to the gully crossings of the SP 141 in the register |
| 22 | Forward window contents: the 2027 to 2031 warm seasons, expected at the long-run seasonal mean (regulation 3.1); no change of stations, crossings or triggering depths |

## Literal reader

Regulation 2.1 to 2.4, 3.1, 3.2 and 4.1 executed word for word on the golden's storm maxima file the golden: each crossing's count is the storms of 1 May to 31 October, 2009 to 2026, in which the rain at its source area reaches the register's triggering depth in any 60 consecutive minutes, each counted once, over eighteen seasons; 3.0 or more is class 3, 1.0 or more class 2, less class 1; the depth reached five times a season is the 90th largest of those eighteen seasons' storm maxima. The same sentences executed on the tips as they stand file the direct route (Rio Gelt 0.67, Rio Marden 0.28, Rio Bianc 1.22), and nothing in them says the tips are the rain at the source area: the regulation names the rain at the source area, the register says no gauge stands there, and the station register describes the gauges as equipment. No sentence in any file states a loss, a factor, a delay, a correction or which record to use for what.

## Prompt contract

A rewrite keeps: the question in the where form with all three classes; the reason the classing rests on an estimate (no gauge stands in the source areas and the program's seasons have not happened); a committed figure for every crossing; the two figures by their plain definitions and units (the triggering storms a season to expect at each crossing; the 60-minute rain depth, in mm, that each source area reaches five times a season); the 2027 to 2031 program; a workbook that opens on the classing and a CSV with one row per crossing. It never adds: a method, a correction, an instrument to trust or distrust, a file name, the number of crossings or stations, a rounding rule, a warning, who is asking, or the lines' values as a procedure.

## Build brief

World: the Servizio Strade Alta Ardesa keeps the provincial road SP 141 dell'Alta Ardesa (eastern Alps, Italy; the valley, the road and the service are invented; files in English with local names). Seven gully crossings (Rio Gelt, Rio Marden, Rio Bianc, Rio Ciadin, Rio Toval, Rio Sass, Rio Larin) are classed for the 2027 to 2031 protection program. Six road stations (Valfosca, Pradalt, Costarossa, Malga Sora, Forcella, Rio Scuro) each run an unheated tipping bucket logged tip by tip (0.1 mm buckets at Valfosca, Forcella and Rio Scuro, 0.2 mm at the others), a storage gauge the technician reads and empties at a monthly visit, and a present-weather detector logging every ten minutes with precipitation. The regional agency's radar gives 60-minute storm maxima on one-kilometre pixels from 2013. A university programme ran weighing gauges at four source areas of the Rio Scuro valley from 2013 to 2026. The world is `core.build(SEED)` exactly: the build imports `generator/core.py`, calls `build(SEED)` once and writes every file from its arrays (`rec`, `opt`, `wet`, `hail10`, `check`, `front_rec`, `rb`, `rnu`, `e`, `x_true`, each crossing's `T`); it lays the storms and the long rain out on dates and clock times, turns the recorded minutes into tips by continuous accumulation, and adds Layer 1 texture that leaves those arrays recoverable.
Frozen: SEED 20270213; the seasons (18 of tips, 14 of radar, 14 of weighing gauges); the lines 3.0 and 1.0; the depth's frequency (five times a season, an architect's re-siting of the ask during the build, ## Tried and rejected); every dial of `DEPOTS`, `CROSSINGS` (the triggering depths 17.0, 19.5, 16.0, 13.0, 12.5, 17.0 and 29.0 mm, the governing stations, the rainfall-normal ratios), `RESEARCH`, `KAPPA`, `THETA`, `PHI`, `HAIL_Z`, `GAMMA`, `SIG_*`, `MONTH_P`, `RAD_LOW` and each station's `rad` (the architect's repair of the radar's process on 2026-11-17, ## Tried and rejected); the golden estimator (`estimate(W)`: the tipping-time loss fitted per bucket model on minute rates through the account, the mean log ratio of the radar's pixel pairs, the detector's profile on hail storms) and the battery's ways; the three stumps, their members and the graded figures of the figure matrix. Each visit interval holds exactly the storms and the long rain core.py assigns to it (`ivl`), so the account's arrays are core's. The cut pack re-proves the core: the golden's seven classes, each stump's flip of its own member, and the rubric's two lines (one stump lost 50 or under, the reflex route 30 or under) are asserted on figures recomputed from the shipped files, and a figure that leaves its band or a class that moves goes back to the architect.
Files: as cut, nineteen files. (1) the tip logs, one CSV per station (`tips_<code>_2009-2026.csv`: tip time to the second with the logger's offset, the bucket's increment in mm), 905,097 rows in all with re-sent blocks after restarts and the technicians' tip tests at visits; the 20,000-row file and the long printed files are here. (2) the visit book (CSV): station, visit date and local time, technician, storage gauge read in mm since the last emptying, whether it was emptied, the count of tip-test tips, remarks; visits near the first of each month that slip by a day or three. (3) the detector's blocks (one SQLite table: station, block start on the logger's clock, block length, weather code, optical intensity; one row per ten minutes with precipitation, storms and long rain alike) with its code list (CSV). (4) the radar extract (CSV): cell id, first and last scan in UTC, pixel, 60-minute maximum in mm, for the station pixels, the source pixels and their neighbours, 2013 to 2026, with the pixel table (CSV: each pixel's current id, its id until 2018 and its centre). (5) the rainfall normal grid (CSV): cell centre, 1991 to 2020 mean annual precipitation, carrying the frozen ratios at the station and source cells. (6) the station register (XLSX, two sheets): code, name, road km, coordinates, elevation, rain gauge and bucket size, funnel heating (none), logger clock, storage gauge, detector, in service from; access notes. (7) the crossings register (XLSX, two sheets): crossing id by chainage, gully, road km, structure, governing station and source area; each source area's coordinates, elevation, area, slope, deposit and triggering depth as point rain in mm in 60 minutes with the survey's date; no class column. (8) the research valley's event table and gauge list (CSV): gauge, event start and end in UTC, the weighing gauge's 60-minute maximum, 2013 to 2026; each gauge's site, type and triggering depth. (9) the regulation, revision 4 (PDF by the house office writer): the program 1.2, definitions 2.1 to 2.4, the expectation's basis 3.1, the depth 3.2, the classes 4.1; fields and quantities only. (10) two distractors that look relevant and are unused: the daily precipitation series of the valley town since 1961 and the SP 141's daily traffic counts by section. Three file categories (spreadsheet, database, text), cross-file reasoning required throughout; `metadata.json` outside the ZIP.
Never filed: a tip duration or any mechanical timing of the bucket; a loss, an intensity correction, a dynamic calibration or a calibration curve; a sentence that the buckets under-read in heavy rain; "melt", "delay", "lag" or "retention" for hail days, or a sentence on what an unheated funnel does; a burst factor, an areal reduction, a representativeness note or any ratio of a source area to a station; a sentence on which record to use for amounts, place or timing; a column or file named for any of the three; a class, a count of triggering storms or a ranking of the crossings anywhere in the pack; the research valley described as a validation or calibration set.
Goldens: `crossing_classes_2027.xlsx`: the first sheet states the classing and what it rejects (crossing, class, triggering storms a season to expect, the 60-minute depth its source area reaches five times a season, its triggering depth) with one chart of the seven counts against the two lines; behind it the station sheet (each bucket's fitted loss and its under-read by rate), the source sheet (each burst factor beside the rainfall normal's ratio), the hail sheet (hail storms by station and the share of the maximum the tips miss), the research valley's check and the routes with their figures. `crossing_classes_2027.csv`: one row per crossing (crossing, gully, class, triggering storms a season, the depth). Every figure from `generator/figures.json`, one set of numbers in both files and in the answer blocks.
Free: document genre and wording inside the Never filed list (the pack spells it "program", as the prompt does); the stations' and crossings' coordinates, elevations and road km; the layout of storms and long rain on dates (no dry gap between three and eight hours, no storm of 9 mm in 60 minutes across midnight at the season's ends, the long rain's 60-minute totals under 7 mm); the neighbour pixels' values; Layer 1 texture and its sizes; the distractors; file names (none naming a stump); the sheet design of the goldens.

## Leak rulings

- `regulation_gully_crossings_SP141_rev4.pdf`, six of the stump paragraph's words (station, record, minutes, gauges,
  regulation, classes): harmless; they are the regulation's own vocabulary. It files what each quantity is (the season
  and a storm's day in 2.1, a storm in 2.2, a triggering storm in 2.3, the point depth in 2.4, the eighteen-season
  mean in 3.1, the depth of 3.2, the class lines in 4.1) and names no instrument model, estimator or adjustment (the
  reader's question 1: none, both passes).
- `gully_crossings_register.xlsx`, all seven crossings beside numbers: harmless; structure, width, year, governing
  station, source area and survey depth. No class, rank, storms-a-season figure or depth of 3.2 is anywhere in the
  pack (Gate G; the reader's questions 2 and 4: none).
- `prompt.txt`, "seasonal": harmless; it is the regulation's own name for class 2's protection (4.1, a seasonal patrol
  with hand gates), not a pointer to a step.
- The heart's three WARNs (the chain against task17 and task10 architecture 7, the CSV and workbook set against
  task1, `stock_flow_accounting` on three live builds) are answered in ## Template check.
- Stage 4 reader, pass 1 (Sonnet, medium, cut 5607fbdb8831364c): nothing on questions 1 to 4 and 6. Question 5 found
  regulation 3.2 open between storms and 60-minute windows, and 2.1 read by the day of the largest 60 minutes where
  the golden had used the day of the first tip: both fixed (3.2 reworded, the golden's season on 2.1's day, SF4 and
  SF25). Its realism notes were fixed in the generator: the source areas carry the province's inventory numbers and
  were surveyed in two campaigns, and the visit book's clock checks carry the seconds found.
- Stage 4 reader, pass 2 (Sonnet, medium, cut cdbf08e67703c82d, the reworded 3.2 and the changed radar extract):
  nothing on questions 1 to 4 and 6 ("No filed sentence says which record to use for which part"). On question 5 it
  executed 3.2 as the golden does (the largest depth a mean of five or more storms a season reach) and asked three
  things of the wording, each measured and asserted with no change to the pack: the clock of 2.1's day (civil time
  moves no storm and UTC one, no graded figure either way, SF4); whether every season is complete under 3.1 (the
  opening rounds fall on 22 to 29 April and the closing rounds on 3 to 8 November every year, SF5); 3.2 from a fitted
  tail (SF20). Regulation 5.2's sentence on the monthly rounds says what the visit book is and names no use of it;
  the account against the storage gauge is reflex work on every route (R1). Realism: nothing found.

## Pre-ship check

- The bar re-read against the cut (cdbf08e67703c82d): seven results across assembly, missingness and measurement,
  modeling, investigation loops, forecasting, uncertainty and synthesis; three stumps on different axes (what the
  bucket loses, where the source stands to its station, when a hail storm's water fell), each moving its own crossing
  across a line and none reaching the classing alone (corelib on the cut pack: level 5, no failure); none of the three
  is a closed strategy (Frontier check, Closed strategies).
- The hidden factor record against the cut pack: each process runs across every unit it can reach (the loss on all six
  stations and both bucket models; a burst factor of its own at all eleven source areas, 0.79 to 1.38; hail held and
  tipped late at every station, 72 to 391 storms; the radar's cell error at every station, 0.27 to 0.44 on logs about
  the station's depth), and no document mentions any of them (`checks.py`, never filed).
- The effort test against effort.py: quick 9.0, careful but hurried 26.7, thorough 100; a run that loses one stump
  earns 45 (S1), 34 (S2) or 37 (S3) figure by figure, the reflex route 13 and the rigorous standard route 9; the largest
  single hint rescues a third of the results or fewer.
- Forcing on both sides: 1,216 variants on the golden's side, the nearest 0.39 storms a season from a line; 512 crosses
  of the first-order loss and 432 of the hail-coded placing inside every band; each shortcut across its line, and the
  radar's own depths (one factor to the stations, or matched to the valley's gauges) across the line on all four open
  crossings and refused at the stations' own pixels (51 to 67 per cent of the stations' storms outside the valley).
- The judge's first pass (NOT_DETERMINISTIC, a narrow send-back on 3.2) and its strongest rival are answered in the
  generator: 3.2 files its count, each stated statistic carries its rule in the Step-by-Step, and the rival that
  reached the classing without a stump (the radar matched to the weighing gauges) no longer does, by the radar's own
  process (## Tried and rejected, 2026-11-17).
- The judge's second pass (`determinism_check_report.md`, cut cdbf08e67703c82d): DETERMINISTIC, FIX_NOW on the
  answer blocks only. About 300 runs of the blocks' own method file the seven classes; 3.2 executes to all seven
  depths; the radar matched to the gauges and the one-factor product are refused at the stations' own pixels by
  figures it reproduced. Its eight fixes were taken in one generator pass with the pack and the prompt unchanged
  (target cdbf08e67703c82d, both zips byte-identical to the judged cut), so no third pass is owed: the band tops
  given a storm and a tenth of a millimetre of room and the hail-coded placing crossed with the first-order loss
  (SF24, SF26); the tip's stamp and the sliding hour stated (the convention behind Rio Gelt's 80 and Rio Bianc's 74,
  found by rebuilding its route: SF26); the account's cut stated in millimetres (SF27); each hail placing, the
  dry-block share, the rate the residual runs with and the rank carry given their rules; both radar routes shown to
  meet the valley's gauges and to fail at the station pixels. The golden files were not opened by the judge; the
  generator's `figures_check.py`, `checks.py` (129 of 129) and `verify.py` (30 of 30) cover them.

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
- Architecture 6 (the Durrow Creek bridge span, READY at f54d048): landed on the platform on 2026-11-09, both runs on every graded
  figure (185 ft, 10,000 and 25,000 cfs, the three bands, water years 2008 and 2011, the 75-row file; runs/arch6/runs.md). Each
  calibrated the snow-line carry on the Selby Creek gauge, validated it leave-one-out and bootstrapped it unasked. One insight
  carried every graded figure, the single-deep-step design the 2026-11-09 review returns; the world is spent and the re-root
  moves to another world, dataset and shell.
- Architecture 7 at the draw, the tide year's mean sea level as a graded forecast: the defensible family (linear trends from 1990
  or 1996, quadratics from 1955 or 1980, with or without an AR(1) carry of the latest anomaly, annual or monthly) spread the
  harbor's expected days 13.9 to 29.0 on one world, so no band could hold it; the planning sea level is filed instead, the
  regional outlook's figure the program adopts, and the forecasting judgments sit where the data pin them.
- Architecture 7 round 1 (target.zip 5cc1927b), the judge NOT_DETERMINISTIC narrowly: "rank all five" graded ranks 3
  and 4, which River Road's flow form moves (linear 15.9 against curved 18.3 days, the fits alike); the ask now takes each
  low point's expected days and the funded two, and every flow form within 6 per cent of the best fit sits in the band.
- Front Street's sensor reporting depth over its dry-road baseline: the onset (8.61 ft) and a depth-on-harbor regression
  intercept (8.66 ft) read the guideline two ways and moved Front Street by 2 to 5 days; the sensor now reports the water
  level on the lane, and its lowest persistent reading is the lane.
- The logger exports sampled at 30 minutes (the common multiple of the 6-minute model and a 15-minute mask) and the
  inventory's River Road campaign left at an earlier window; both found by the leak reader, the loggers interpolated to 15
  minutes and the inventory set to 20 January to 20 April 2025; the site levels re-set for margins (Marsh Road 8.42,
  River Road 8.37, Wharf Street 8.555 ft) so four shortcuts still name four different pairs.
- Architecture 7 round 2 (target.zip 521db5d2), the judge DETERMINISTIC with FIX_NOW: River Road's figures did not
  reproduce (12.2 to 13.5 expected days against 18.7) and the pair's years (32 against 28). The world had read each
  day's river flow by its UTC date while the USGS file and every analyst read local days, which is why a three-day
  smoothed flow fitted better than the day's own; flows are now local days (the fits tighten five-fold, the power
  form leads), every form within a fifth of the best sits in the sweep, and the bands cover the judge's figures.

Architecture 7 (the Georgia port's tide valves), set aside on 2026-11-16 before any upload:
- The whole architecture: READY at a175067 and never uploaded. Its two priced results were response-model corrections
  on mechanisms of the world (the kind the review of 2026-11-13 returned at 75 to 83), its harbor results were asks sited
  away from the stumps (collected in full by a run off the call under the rule of 18a93a7), and its deciding lesson sits
  on four live builds. Spent; the slot moves to a new world.

Architecture 8 (the SP 141's gully crossings), at the draw:
- The frost-night, flood-routing, heat, wind, hail-count, lightning and low-flow worlds: each core was a response of the
  world the rows carry (modelled on sight) or a textbook return-period fit whose inputs ship (one reflex).
- An ENSO state response, new gauges replacing old ones, an overlap season, network densification, gauge reassignments:
  closed cards (a change of instrument, a co-occurring change) or a splice at a date, which is a join.
- Totalizers at the source areas, a threshold filed in station-gauge units, a weighing gauge beside the research
  station's bucket: each hands a stump over (the transfer, the loss) as a filed comparison.
- Logger outages, clock hours against sliding 60 minutes, drizzle gaps, funnel blockage, wind undercatch: screened out
  (candidates E to G of the stump screen and their kin: closed, textbook or not measurable from the pack).
- The union across a corridor's source areas as the third stump: once the register lists the areas it is a join.
- A union nested inside a radar-absolute S2: the radar read as a depth is the rigorous route, which has to land wrong.
- A line of one storm a season over 16 seasons, and a plain set over one line: counts of 16 storms sit inside any
  family's spread, and a set over one line is on six live builds; three classes on two lines over 18 seasons instead.
- The network total as a component, and the 40 largest storms' depth loss as S1's own figure: the first is reflex work,
  the second moved under S2 and S3 as well, so S1 had no figure of its own.
- Research sources with a burst factor near one: the valley read as a calibration then landed the open members; the
  valley's sources sit at 0.78 to 0.90 of their station.
- Crude hail estimators inside the family (dry intervals only, an even spread, the detector's own amounts): each widened
  Rio Bianc's band past the stump; each is now refuted by a figure at the research valley (SF18).
- Hail probability tied to the station's own burst alone: every station then saw the same hail share and S3 opened no
  member of its own; hail goes with the cell's strength and the station's height.
- The valley's hail-day multiplier ruled out at the count referee: it files the golden's classes and its tail mean is
  15.41 against 15.53 seen, so it stays in the family (SF17).
- Weight hard-to-measure, and real toponyms: the weight is on task16, and real places would make the triggering depths
  checkable against the outside.
- A golden family of conventions listed singly: the wider rivals an auditor would run left figures outside the bands;
  the battery is now the full cross of 384.
- One random stream shared by all stations: moving one crossing moved every station's storms; each station has its own
  stream and the source areas a side stream.
- The triggering-storm count at the research valley as the referee statistic, then the depth reached three times a
  season: the first agreed by luck of the realization and the second passed on 1 of 8 seeds; the mean depth of each
  source's five largest storms a season replaces them (golden off by 0.08 mm, rivals by 1.2 to 5.7).
- Radar pixel noise at 0.11: it biased the storm-by-storm pair carry upward and widened the family; 0.07.
- The unpaired upper-decile ratio inside the family: it does not replicate between odd and even seasons (up to 6.2 per
  cent against 1.5); refuted (SF14).
- The loss read on 10- and 15-minute totals inside the family: Rio Gelt fell to 3.50 and 3.11; the account refuses both
  (2.26 and 3.45 mm rms against 1.25), so they are refuted rivals (SF10).
- Triggering depths derived from a target rate on the long run: the 18-season realization sits up to 15 per cent off the
  long run, so the depths are filed dials.
- A pixel keeping 0.40 of the local factor: the radar route filed the right class at an open member on many seeds; 0.28.
- Valfosca's hail share at 0.24: the hail dimension widened the family on S1's member (S1 at 2.4 times the spread);
  0.10, with a wetter valley floor, gives 3.6.
- Rio Gelt's rainfall-normal ratio at 1.00: Rio Gelt's figures were downstream of S1 alone and S1 fixed alone earned 31;
  at 1.03 S2 moves its count without flipping it and S1 fixed alone earns 27.
- The research valley's rainfall-normal ratios at 1.22 to 1.44 over 0.4 to 1.7 km (changed at the build's first step,
  before any file): no climatological grid steps by a third in 400 m; 1.09, 1.14, 1.19 and 1.24, rising with the
  distance. Only the referee's rainfall-normal rival moves (24.07 to 21.21 mm, 773 to 554 storms); every crossing's
  figure, the lattice and the rubric table are unchanged (`core.py` exit 0, CORE PASS level 5).

Architecture 8, at the build (2026-11-16):

- The depth ask at three times a season (the 54th largest): on the cut pack S1 moved it at three of seven crossings and a
  run that lost only S1 earned 49; re-sited at five times a season (the 90th largest, regulation 3.2, the prompt, core.py
  re-proved at level 5), where all three stumps move it.
- A battery of 384 variants with the rate read by the minute or on five-minute totals only: the independent second
  implementation (rate tip by tip, windows anchored on tips) put Valfosca's under-read at 18.2 per cent, outside the
  first band (19.4 to 20.8). The storage gauge account cannot refuse the tip-by-tip reading or totals of two, three and
  five minutes, so all of them went into the battery (1,216 variants, one classing) and the band is 17.6 to 24.9.
- The first-order form of the loss refused by the account's residual: on the same minute totals it leaves the account
  open by 1.09 to 1.37 times the tipping-time form's, too thin to refuse, so its 512 crosses are carried inside every
  stated band (they file the same classes); a power law (1.44 to 2.25 times) and ten- and fifteen-minute totals (1.73 to
  2.44 times) stay out, each named with its figure in the blocks.
- Five-minute totals refused by the account (1.5 times the fitted reading's): the line between five and ten minutes was
  an argument, not a measurement; five-minute totals moved into the battery.
- A hail storm read by its day against by its own blocks asserted as one catalogue: 105 storms differ across the six
  stations (a day can hold a hail storm and another event); measured instead, the day reading moves no graded figure
  out of its band and no class.
- A season-boundary check at 5 mm in 60 minutes: long rain crosses midnight at the season's ends at that depth; the
  check is at 9 mm, the least any triggering depth or stated depth asks of a station's storm.
- Field-check pours of water at visits: replaced by the technicians' tip tests (a counted number of tips by hand, in
  the visit book), which a real visit round records and which leave whole buckets in the log.
- A head of service typed by hand: replaced by Piero Brancaccio of the registered persona draw.
- The crossings register created in 2012: outside the container gate's twelve-year band; created 2016, its author the
  geologist who keeps it.
- One stump lost at the draw's 22, 22 and 30: the cut pack prices 45, 30 and 37, because the honest battery widens the
  bands most at the 0.2 mm stations where the loss by rate is smallest; the gate (50 or under) holds and the core is
  unmoved. Raising the 0.2 mm bucket's loss to pull S1 down was not done: it is a frozen dial of the proved core.
- The radar with one error spread at every station (the draw's `SIG_B` 0.15): the judge's fork audit matched the
  radar's depths on the weighing gauges' pixels rank for rank to the gauges, counted them at the source pixels and
  filed the golden's seven classes with none of the three stumps (Rio Gelt 4.86, Rio Marden 4.71, Rio Bianc 4.43). A
  radar whose error is the same everywhere makes the research valley a calibration set for every crossing. The
  architect's repair, 2026-11-17: a cell's error is one factor over its footprint with a spread of its own at each
  station (`rad`, 0.12 to 0.37 on logs, widest in the narrow research valley) and the product reads low (`RAD_LOW`);
  the golden's pixel-pair ratios see neither, and core.py re-proves level 5 with the gauge-matched radar as the
  rigorous standard route (2.07, 1.29 and 2.21 at Rio Gelt, Rio Marden and Rio Bianc).
- Holding the gauge-matched radar inside the bands instead: a route with no stump would have earned about 80.
- Refusing it on regulation 3.1's eighteen seasons alone: a window argument against a rival that filed the right
  classes; kept as a second ground beside the stations' own pixels.
- The per-station spread without the under-read: the raw radar's counts drifted up to the right classes (3.21, 3.00
  and 3.57 in the prototype).
- Rio Scuro mid-rank in the spread: a map made at each station on its own corrected depths and shaped on the valley's
  gauges still filed the classes; the valley is the noisiest of the six.
- The radar product as a scored rival at the referee: on the repaired world both radar routes are in sample at the
  valley (197 and 193 storms against 190 seen), so they are ruled on at the stations' own pixels (SF22).
- Regulation 3.2 as "reached at the crossing's source area by five storms a season, on the mean of the same seasons":
  still readable as the mean of each season's fifth largest storm; it now files the greatest depth reached in a mean
  of five or more storms a warm season (SF25).
- The two pixels matched rank for rank held in the bands: Rio Bianc's depth floor would fall to 14.2 mm and the routes
  that lose S1 or S2 would land it; refused by its own halves instead (1.40 mm between odd and even seasons, SF23).
- The hail-coded blocks alone refused at the referee (218 storms against 190): too thin a margin to call out beside
  the detector's own amounts at 224, so its 304 crosses are held in the bands, upward, where no shortcut lands (SF24).
- Rio Larin's band top left on the family's last storm (0.67) to keep the S2-lost price at 29.9: not done. The judge's
  second pass asked for a storm of rebuild room above every top; with it the S2-lost route's Rio Larin count (0.83)
  comes in as a near miss and that route prices at 33.7. A band an honest rebuild can leave costs a return.
- A power law of the recorded rate and the 10- and 15-minute totals carried in the bands: Rio Gelt's floor would fall
  to 3.11 storms a season, a storm from letting the S1-lost route (2.39) in as a near miss. They stay refused, by a
  cut stated on the storage account in millimetres (2.14 held, 2.22 refused: SF27).
- The same room below every band's floor: Rio Bianc's depth floor at 14.6 mm would leave the S2-lost route (14.3)
  0.05 mm from a near miss. The judge's 300 runs left no floor, so only the tops were given room.
