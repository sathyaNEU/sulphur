# task3: which stations carry a relief ramp crew for the 2026-27 wet season (Kestrel Coast Ground Handling, architecture 9)

Architecture 9 below died on paper on 2026-11-21 and its world is retired; nothing in this note, `generator/core.py`
or `prompt.txt` is built from (`## Tried and rejected`, last lines).

## Draw

Subdomain: Physical & Environmental Sciences, climate and weather extremes (the card's `climate-weather-extremes`)
Analysis type: Forecasting & Predictive Modeling
Answer shape: scenarios with the flip point (`scenarios-flip`, prompt shape 13): every station's expected stand-down hours for the window, the same station in an average season, and the season, as a per cent of an average one, at which its answer changes
Weight: measurement. The work sits in what a lightning location network recorded against what fell: which strokes it located, what a legacy receiver adds, and what a clearance timer would have run on the strokes it missed.
Data-native sentence: the only record of past ground strokes is a location network whose chance of locating a stroke rises with its peak current and with the sensors in range and up that day, and the stand-down is the union of the 15 minute intervals the strokes open, so the strokes the network missed shorten stand-downs, split them and erase whole storm days by an amount that depends on each day's size and shape and on each station's sensors, never in proportion to the strokes missed.
People: Adrian Thompson, Mario Johnson, Alexandra Abbott, Joel Holmes, Cassidy Mcdonald, Jaime Fisher (`guard.py names --geo AU --seed 3909`; Karen Riley and Jennifer Lopez drawn and set aside, the first on the guard's first-name WARN, the second as a public figure's name)
Decision: Kestrel Coast Ground Handling adds a relief ramp crew at every station whose expected lightning stand-down in the wet season of 1 December 2026 to 31 March 2027 is over 25 hours. Forward facing: the window has not opened, and Ramp Lightning Standard GS-14 (a cloud-to-ground stroke within 8 km stops the ramp until 15 minutes after the last one, called by each station's new on-site detector) takes effect on its first day, so no station has a stand-down log under the rule.
Forum and forcing event: the handler's resourcing committee (`committee_or_panel`), forced by the season's start (`season_or_peak`).
Deliverables: a CSV of the station figures and a workbook with the call on its first sheet and a chart of each station's expected hours against the 25 hour line. No written document.
Slot: re-rooted on 2026-11-21. Architectures 2, 3, 6 and 8 were landed by both platform runs; architecture 8's runs (`runs/arch8/run1.md`, `run2.md`) are the adversary this core is built against, and nothing of rain, floods, culverts, tides or hydrology is kept.
Guard: `guard.py check task3` on the registered card, no BLOCK. Seven WARNs, each answered here: the weight (none of the last three builds by filing time, task9, task26 and task1, puts its weight where this one does; task8, five builds back, does, on an awarding body's marks linked across sittings, which shares no instrument, estimator or decision with this build); the deliverable set (a CSV and a workbook is the house set, the files' contents and the chart differ from task9's, task26's and task1's); the question form `which` after task1's (task1 asks which side of a go or hold figure one programme falls; here which names a set of stations over a filed line, the form the decision takes); the three skeleton WARNs on lessons and the house shell (`## Frontier check`, `Closed strategies:` and `## Template check`).
Stump ids: S1 and S3. S2 was the forward state at this architecture's first draw; it is a supporting step now (`## Tried and rejected`) and its id is not reused.

## Stump screen

Screened on paper and in `generator/core.py` before the card was registered (`references/stump-screen.md`, the twenty tests).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A: the stand-down is the union of the 15 minute intervals the strokes open, and the network misses the weak strokes, which sit at a cell's edges and outside it; so the strokes it missed shorten stand-downs, split them and erase whole small days, and recorded hours answer to detection by the day's size, never in proportion | recorded hours stand for the hours, or rise in proportion to the strokes missed (N21: an unmeasured component placed in proportion to the measured one; L56: the recording effect seen and kept as a sensitivity) | the sensor log against the stroke archive: the days six or more standard sensors saw, thinned by the filed chances to two and three sensors with the timer rerun | none | kept (stump S1) |
| B: a legacy receiver adds about a third of what a standard sensor adds to detection, and no document says so; the days it is in range show it only in how far the weak strokes are cut | every sensor the log lists counts alike in the filed table (N42: one instrument's correction put on a second model for want of a check) | the peak currents of the strokes located on the days a legacy receiver was up, against the peak-current law fitted on the days seen by standard sensors alone | none | kept (stump S3) |
| C: the region's storm days answer to the shelf index, the warm seasons of the record fell under the thin early network, and the bureau's outlook puts the window warm | the record's own mean is the window's expectation (N43: stationarity named and waved) | the strokes of 60 kA and over, which every network in the record locates, against the index season by season | 1 (next to two closed cards, a change of instrument and a co-occurring change, and its fix is theirs: rebuild on the signal the change could not move); 15 (the rigorous standard route, a level per sensor configuration with one pooled response, lands its figure) | kept as a supporting step only, never a stump: left out alone it leaves the call standing |
| D: the network logs some cloud pulses as weak ground strokes, more of them the more sensors are up, so the well-covered seasons over-count | every archive row typed as a ground stroke is one | the share of weak positive events by sensors up | 9 and 11 (a first core priced it: the golden over-estimated the contamination by 60 per cent and the family's spread swallowed the stump) | dropped |
| E: the network of the coming window differs from the record's (sensors commissioned in 2026), so the stand-downs the detector calls will differ from what the archive's network would have located | the archive's latest configuration is the window's | the sensor register's commissioning dates | 1 and 20 (the closed card of a projection that holds fixed what the change moves; and the estimand is what falls, which no network changes) | dropped |
| F: a location's error grows with fewer sensors, so strokes just inside and just outside the 8 km ring trade places | the located position is the position | the archive's error ellipse fields | 9 (with a locally even stroke density the trade is even: no bias in counts or hours to price) and 2 (an ellipse integrated over the ring is a reflex once the field ships) | dropped |
| G: station-days on which fewer than two sensors were up have no strokes because none could be located | a day with no located stroke was a day with no storm | the sensor log's days with fewer than two sensors up | 1 and 2 (the closed card of groups recorded less completely, fixed by a gross-up on the days a location was possible, which the runs do on sight) | dropped as a stump; done by every route and never a graded figure |
| H: each station's own response to the shelf index, one of them negative | one regional response | each station's season counts against the index | 9 and 10 (twenty four seasons cannot hold seven separate responses apart: a first core's golden was noise) | dropped |
| I: a thunder-day book written up by hand at each aerodrome that sees storm days the network missed | the archive's storm days are the storm days | the book against the archive, day by day | 16 and 18 (a second record of the days is a calibration set: a run fits the missed-day share from it in one regression) | dropped; no observer record of storms ships |

## Deep reasoning

Task type: climate weather extremes (Extreme-value & environmental-hazard analysis: the seasonal duration of a lightning hazard at a point, retrieved from a detection-limited instrument record and carried to a coming season), which serves Forecasting & Predictive Modeling
Domain test: every result is a quantity of lightning climatology put to an operational hazard rule: a location network's chance of locating a stroke by its peak current and by the sensors up, the peak-current law of ground strokes recovered through that cut, what a legacy receiver adds to detection, the hours a stroke-restarted clearance timer keeps a ramp closed, a season's storm activity against a sea-surface index. The field's analyst corrects a stroke climatology for detection efficiency before using it; here the quantity the decision uses is a non-additive functional of the strokes (a union of timers), so the field's own correction of counts does not carry to it.
Swap: "Which stores carry a relief shift this quarter, on the hours an alarm is expected to keep each one shut?" keeps the set over a line and loses everything else: nothing fixes a chance of recording an event by its size, nothing makes the shut hours a union of timers restarted by events the record missed, no receiver counts for a fraction of a sensor, and no index moves the season. The question stops making sense.
Where the weight sits: R3 and R4, the two measurement models. Each is long, not clever: the legacy receiver's worth is a profile likelihood over the located peak currents of 13,555 strokes on legacy days against a law fitted through the same filed curve elsewhere; the hours are a response matrix built by thinning 512 well-covered storm days to every sensor level in the record, rerunning the timer, and unfolding each station's recorded days by size, including the days that left no record.
Layer 1: stroke times in UTC against a sensor log kept by local day; re-sent archive batches and reprocessed solutions under a later version stamp; peak currents signed by polarity, with the network's cloud pulses in the same extract under their own type; sensor identifiers renumbered at the 2010 and 2018 upgrades; a square extract that returns strokes just outside the 8 km ring; station-days on which fewer than two sensors were up. Each is the archive's or the log's own process and none decides a result on its own: every route cleans them the same way.
Not one thing: the strongest single piece is the hours' answer to detection (S1). A run that nails it still files Weymoor Gap under the line (the legacy receivers counted as sensors put it at 17.2 hours against 28.6), still has the legacy worth to fit before Callory Downs', Yanda Creek's, Tarrick Tableland's and Burrel Bay's figures are right, cannot simply set the receivers aside (worth nothing, they put Burrel Bay over the line at 28.9 hours), and still has the season's state and each station's break-even season to carry.
One-fact test: "the strokes the network missed shorten stand-downs, split them and erase whole days, so recorded hours do not scale with the share of strokes located" rescues R4 and R5 on the reflex route (2 of 8 results) and 19 rubric points, with Weymoor Gap still wrong; the sentence leaves the replay to design, the recorded day size to condition on and the days with no record to estimate. "A legacy receiver is not worth a standard sensor" rescues R3 alone (1 of 8). Agrees with the Effort test's Largest single hint.
Not semantics: every field, unit, clock and clause read correctly leaves the reflex route where it is: the located strokes are the located strokes, the sensor log lists the sensors that were up, the table is the vendor's table. What the route lacks is two estimators.
Not rule application: the standard files what a stand-down is, the procedure files the window, the line and what an average season is, and the vendor's sheet files the chance of locating a stroke at each count of sensors up. None of them performs R3 or R4: no filed sentence says what a legacy receiver is worth, how recorded hours answer to missed strokes, or that the season's state matters. Once every filed rule is applied the judgments left are how to count the legacy receivers, what the timer would have run on the strokes the network missed, and how to carry the result to the window.
Estimand: the standard (`ramp_lightning_standard_GS14.pdf`, clauses 3.1 to 3.3: a stand-down begins at any cloud-to-ground stroke within 8 km of the station's reference point and ends 15 minutes after the last such stroke; the on-site detector registers every ground stroke inside that radius); the procedure (`wet_season_resourcing_procedure.pdf`, section 2: the window of 1 December to 31 March, the expected stand-down in hours counted across all hours of the day, a relief crew where it is over 25 hours, the expectation taken at the bureau's outlook value, an average season as the mean of the seasons on record); the prompt (the window, the line, the 2002-03 to 2025-26 record, each asked figure with its unit).
No decoy: nothing in the pack carries a wrong answer: no memo, draft or column ranks the stations, no document argues for a route, and no file holds a stand-down hour or a corrected count. The vendor's sheet is right as far as it goes (standard sensors); it is silent on legacy receivers.
No replay: no result re-derives a published figure and no filed number is wrong.
Pinned: 27 variants of the golden's conventions in `generator/core.py` (the law by polarity or pooled and from four sets of days, the legacy worth from all legacy stations, from Weymoor Gap alone, without it, from the count of strokes of 60 kA and over, or as a level of its own for every pairing of sensors up, the donors at six or seven standard sensors, the replay's seeds and thinnings, the day sizes unfolded together, level by level, in one step or in three, coarser and finer size classes, the strong strokes from 50, 60 or 75 kA, the state fitted four other ways and as a straight line in the index on the strong strokes or on the corrected hours) file one call, and every graded figure's band is their span with room. Every rival route is ruled on by a figure from the files (`## Semantic fork table`).
Run forecast: R4 lost to a method shortcut (the located strokes' hours taken as the hours, raised in proportion, or the missed strokes put back between the located ones: L56, N21, L57); R3 lost to dismissed own evidence (the legacy receivers counted as sensors for want of a filed figure, named as an assumption and left: N42, L58); R5 lost to a self-confirming check (a hold-out of seasons on the located hours, which both sides of the split share); R7 and R8 lost downstream of either.
Strategy label: other (an estimator for a rule's output on the events a record missed, and an unfiled instrument sensitivity fitted from the cut it leaves in what was recorded; no label in `references/sulfur-strategies.md` holds either). UNTESTED.
Depth level: 4 on the client's depth scale (`guidelines/client/depth-scale-2026-11-09.md`): two independent judgments, each necessary alone and neither sufficient, on two distinct wrong calls among the single drops (Callory Downs alone; Callory Downs, Penrow Sound and Mornay Inlet) and a third among the run routes (the proportional raise adds Tarrick Tableland and leaves Weymoor Gap out). Each stump is two-sided on its own: pushed past its fitted value alone, S1 (the hours raised in proportion) files a crew everywhere but Yanda Creek and S3 (a legacy receiver worth nothing) files a fifth crew at Burrel Bay. Level 5 was drawn and given up: the third judgment (the forward state) sits on closed cards and is landed by the rigorous standard route (`## Tried and rejected`).
Lesson: a rule's output on a thinned record is not the thinned record's output raised by a share: the rule has to be replayed on what the record would have missed, and an instrument nobody characterised has to be characterised from the cut it leaves in its own data. No build on file teaches the pair: the nearest lessons on file (`device_setting_replay` on mark162 and a spent task7 architecture, `latent_structure_estimation` on task18 and task5) sit in other decision forms on other records.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | The located ground strokes set against the sensor log, station-day by station-day: each day's standard sensors and legacy receivers in range and up, the days on which no location was possible, each station's seasons of exposure | assembly-reconciliation | the archive's type, version and position fields, the sensor register's range and dates, the standard's 8 km | exact | narrow look at broad data: the quick pass reads the strokes alone and never opens the sensor log | - | Step-by-Step (the counts and bases every route reaches; no graded figure) |
| R2 | The peak-current law of ground strokes by polarity, fitted through the filed detection curve, and with it the share of ground strokes located at each sensor level; the ground strokes an average season brings the stations no legacy receiver reaches | missingness-measurement | the vendor's table and width; the days seen by standard sensors alone | S at Penrow Sound 254.2 (251.2 to 255.4), Mornay Inlet 178.2 (176.4 to 178.9) | method shortcut: the quick pass counts the located strokes (70 and 60 a season); the careful pass fits the law and lands these | R1 | Ask 2 (inside each station's average-season line) |
| R3 | What a legacy receiver adds, in standard sensors (0.32), and the ground strokes an average season brings the stations it reaches: Weymoor Gap 258 | modeling | the peak currents located on legacy days against R2's law; the per-pairing fit and the count of strong strokes inside the band | Weymoor Gap 258.4 (240.1 to 262.6); Callory Downs 1,085 (1,053 to 1,093); Yanda Creek 139.2 (136.3 to 139.8); Tarrick Tableland 495.4 (479.9 to 499.7); Burrel Bay 235.8 (219.1 to 239.6) | dismissed own evidence: the legacy receivers counted like standard sensors, named as an assumption and left (119 at Weymoor Gap), or set aside altogether (426) | R1, R2 and the legacy stump; independent: Weymoor Gap's strokes move with the legacy stump alone | Component 2 (Weymoor Gap); Ask 2 |
| R4 | The hours an average season stands each ramp down: Penrow Sound 26.3 | modeling | the timer replayed on the well-covered days thinned to each sensor level; the replay test (R5) | Penrow Sound 26.25 (24.9 to 27.3); Callory Downs 48.99 (47.81 to 51.62); Mornay Inlet 26.01 (23.84 to 27.58); Weymoor Gap 26.47 (25.32 to 27.42); Yanda Creek 13.89 (13.51 to 14.33); Tarrick Tableland 20.29 (19.63 to 21.41); Burrel Bay 19.99 (19.09 to 20.46) | method shortcut: the located strokes' hours taken as the hours, or raised by the share of strokes missed, or the missed strokes put back between the located ones (11.8, 37.6 or 20.1 at Penrow Sound), or one share of hours read off the well-covered days or a cut of them | R1, R2, R3 and the hours stump; independent: Penrow Sound's hours move with the hours stump alone | Component 1 (Penrow Sound); Ask 2 |
| R5 | Every correction tested on the stations' own well-covered days: those days thinned to two and three sensors, the correction applied, against the hours and the strokes they carried on the full network, read by the day's size | validation | the days six or more standard sensors saw (512 storm days at Callory Downs and Yanda Creek) | the replay's largest miss 0.044 log points over four day sizes; the rivals 0.24 to 0.94 | self-confirming check: a hold-out of seasons on the located hours, which passes because both halves are the same thinned record; or a share calibrated on the small well-covered days and checked on those same days | R1, R2, R4 | Step-by-Step (the check that rules between the routes; no graded figure) |
| R6 | The region's response to the shelf index and this season against an average one: 108 per cent | forecasting | the strokes of 60 kA and over against the index; the outlook value of +0.5 | 107.9 (106.4 to 110.6) | stopped at the first story: the quick pass carries the record's mean (100 per cent); the careful pass fits a response and lands it | R1 | Ask 3 (one figure) |
| R7 | Each station's expected stand-down hours for 1 December 2026 to 31 March 2027 and the call: relief crews at Callory Downs, Mornay Inlet, Weymoor Gap and Penrow Sound; none at Tarrick Tableland, Burrel Bay or Yanda Creek | synthesis | R4 carried by R6; the 25 hour line | Callory Downs 52.87 (51.59 to 55.71); Mornay Inlet 28.07 (25.73 to 29.76); Weymoor Gap 28.57 (27.32 to 29.59); Penrow Sound 28.33 (26.87 to 29.46); Tarrick Tableland 21.9 (21.19 to 23.1); Burrel Bay 21.57 (20.57 to 22.25); Yanda Creek 14.99 (14.58 to 15.46) | unfinished chain: one correction made and the other left, or one pushed past its value, so the call moves to a different wrong set | R3, R4, R6 (both stumps) | Recommendation; Ask 1 |
| R8 | How strong a season, as a per cent of an average one, puts each station's stand-down at the 25 hour line | uncertainty | R4; the line; set against R6's 108 per cent | Callory Downs 51.0 (48.4 to 52.3); Mornay Inlet 96.1 (90.4 to 104.6); Weymoor Gap 94.5 (91.1 to 98.7); Penrow Sound 95.2 (91.5 to 100.3); Tarrick Tableland 123.2 (116.7 to 127.2); Burrel Bay 125.1 (122.1 to 130.9); Yanda Creek 180.0 (174.4 to 185) | unfinished chain: the hurried hours put the three stations a season of 108 per cent takes over the line at 200 to 221 per cent | R3, R4 (both stumps) | Ask 3 |

Carry-forward: every graded figure sits downstream of a stump. S1 moves every station's hours (the seven average-season hours, the seven season figures and the seven break-even seasons); S3 moves the hours, the strokes and the break-even seasons at the five stations a legacy receiver reaches (Callory Downs, Weymoor Gap, Yanda Creek, Tarrick Tableland, Burrel Bay), so fifteen of the twenty nine ask figures fall with both. S1 owns Penrow Sound's average-season hours (Component 1: it falls with S1 alone and is earned when S3 is lost) and S3 owns Weymoor Gap's average-season ground strokes (Component 2: it falls with S3 alone and is earned when S1 is lost). The supporting step (R6) carries one figure of its own inside a sentence the stumps decide, so the reflex route lands no whole sentence: it still lands the strokes at Mornay Inlet and Penrow Sound and the season's percentage, three figures in lines whose other figures it misses.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| The network locates a stroke with a chance that rises with its peak current and with the sensors up | constructed, from the filed table | no: every station, every season, every stroke | in plain sight (the vendor's sheet files it) | modelling: a law fitted through the cut, then the timer replayed on thinned days | keep |
| Recorded hours answer to detection by the day's size and shape (small days vanish, edges and strays are weak) | constructed, by the storm process | no: every station; largest where days are small and sensors few (Penrow Sound, Mornay Inlet, Weymoor Gap, Burrel Bay, Tarrick Tableland) | modelling: no one table shows it; the outage days show a fall in hours with a sampling error of its own | modelling: a response matrix by day size and an unfolding per station | keep |
| A legacy receiver adds about a third of a standard sensor | constructed | no: five stations in the first era, three in the second, two in the third; Callory Downs, Yanda Creek, Tarrick Tableland and Burrel Bay carry it beside Weymoor Gap, and Burrel Bay sits under the line where Weymoor Gap sits over it | a targeted query (peak currents by the sensors up, split by type) and then modelling | modelling: a profile likelihood against the law fitted elsewhere | keep |
| Storm days answer to the shelf index, and the warm seasons fell under the thin network | constructed | no: one regional response at every station | modelling: a response on the strong strokes | routine once seen; a supporting step and never a stump | keep as a supporting step |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the strokes against the sensor log | Partly | Right | Right |
| R2 the peak-current law and the share located | Missed | Right | Right |
| R3 the legacy receiver's worth and the strokes where it reaches | Missed | Missed | Right |
| R4 the hours an average season stands each ramp down | Missed | Missed | Right |
| R5 every correction tested on the well-covered days | Missed | Missed | Right |
| R6 the response to the index and this season against an average one | Missed | Right | Right |
| R7 each station's hours this season and the call | Missed | Missed | Right |
| R8 the season strength at which each station's answer changes | Missed | Missed | Right |
| Roughly | 0.5 of 8 | 3 of 8 | 8 of 8 |

Measured by: `generator/core.py` on `corelib.py` at the draw (the lattice, the routes and the rubric table below); `.claude/skills/stumping/effort.py` on `generator/effort.json` once the pack is cut
Largest single hint: "the strokes the network missed shorten stand-downs, split them and erase whole days, so recorded hours do not scale with the share of strokes located"; rescues 2 of 8 results (R4 and R5), 19 rubric points, the call still wrong at Weymoor Gap
Pair estimate: 19 (a run that loses either stump alone earns 19 on corelib's rubric; the reflex route earns 9, each of the four run routes 9, and the dearest of their further settings 42 with the wrong call). The paper is optimistic by this harness's own record; the platform's two runs are the measurement.

Ten minutes: the located strokes' hours averaged by station, Callory Downs alone over the line, nothing right but part of R1. An afternoon (the reflex route): the files joined and cleaned, the law fitted, the counts raised by the filed share, a response to the index fitted, the hours still the located strokes' (or raised in proportion) and every sensor counted alike: R1, R2 and R6. Two days: the two estimators and the replay test, everything.

## Stump core

Every figure below is printed by `python3 task3/generator/core.py` (seed 3909; exit 0; last line `CORE PASS level 4  task3 architecture 9`). Stations in the order Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Yanda Creek, Tarrick Tableland, Burrel Bay (core.py's A, Z, X, V, Y, W, B).

Unobserved part: the hours each ramp will be stood down in the window under the standard, which is the union of the 15 minute intervals opened by every ground stroke within 8 km. No record holds it: the standard starts on the window's first day, and the only record of past strokes located 27,002 of the 65,017 ground strokes that fell on 5,796 storm days (the share by station 0.54, 0.28, 0.35, 0.31, 0.61, 0.28, 0.30), with 1,766 storm days leaving no located stroke at all. The world's own expectation for the window: 56.2, 28.8, 30.1, 32.0, 16.3, 22.3 and 24.2 hours.
Instruments: (1) the network's archive of located strokes: sees a stroke with a chance that rises with its peak current and the sensors up; blind to the weak strokes, to the days that left none and to the days fewer than two sensors were up; read raw it files 35.5, 10.5, 10.8, 12.5, 10.3, 10.8 and 9.7 hours an average season and 606, 70, 60, 82, 88, 143 and 76 strokes. (2) The sensor log and register: which standard sensors and legacy receivers were in range and up each day; blind to what a legacy receiver is worth. (3) The vendor's sheet: the 50 per cent current at two to eight sensors up and the curve's width; silent on legacy receivers and on hours. (4) The days six or more standard sensors saw (512 storm days at Callory Downs and Yanda Creek): nearly the whole of what fell there; blind to every other station's storms and to how small their days run. (5) The shelf index's 24 seasons and the bureau's outlook value of +0.5: the season's state; blind to its effect.
Referee: none ships: no file observes a true stroke count, a true hour, a stand-down or a legacy receiver's worth, and no station was ever seen by two networks at once. The call is forced by a falsification check on the stations' own records, three statistics in log points, each what the record shows over what a route's own assumptions predict: K1 the replay test (the well-covered days thinned to two and three sensors by the filed chances, the route's correction applied, against the hours those days carried on the full network, in two folds, read by the day's size on the full network in four classes, one or two strokes, three to five, six to nineteen, twenty or more, the largest of the four misses); K2 the peak currents of the strokes located on legacy days against the route's sensor count; K3 the strong strokes' response to the index against the response the route carries and the one its corrected hours show. Score, the root mean square of the three: the golden 0.026 (K1 0.044, K2 0.006, K3 0.011). With each stump left out alone and both together: S1 lost 0.544 (K1 0.940), S3 lost 0.133 (K2 0.224), both lost 0.559. The run routes: generous 0.320 (K1 0.507, K2 0.224), calibrated 0.266 (K1 0.401, K2 0.224), hedge 0.561; the rigorous standard route 0.559; the missed strokes put back 0.265 (K1 0.398); the outage-day elasticity 0.371 (K1 0.599); one share of hours kept at each sensor count with the legacy worth fitted 0.233 (K1 0.404); the same share read off the well-covered days of at most 2 to 30 located strokes 0.141 to 0.269 (K1 0.243 to 0.465: a share fitted on days of one size passes on them and misses the days of another). Every rival is 5.1 times the golden's score or more. The supporting step left out (the record's mean carried) scores 0.063, on K3 alone (0.100), and files the golden's call. A fourth statistic is printed beside the score and kept out of it: recorded hours on the thin stations' own days with a standard sensor down against the days all were up (the golden 0.079, the located strokes' hours 0.169, the proportional raise 0.188, the strokes put back 0.026, one share at each sensor count 0.025). It rests on 332 outage days with a located stroke and carries a sampling error of 0.08, as large as the routes' differences, so it rules on nothing and no route is scored on it. The same experiment for the counts: the strokes left over the fitted law's share recover 1.01 and 1.00 of the full network's count at two and three sensors, and the strokes left weighted by one over their filed chance (capped at 50) 0.92 and 0.95. The check does not observe the target: it is run on other days and other stations than the ones the call turns on, and a calibration read off it flat (the calibrated route, at every cut of its days) files the wrong call.
Strongest standard route: the most rigorous standard design the pack affords: counts weighted by the filed chances at the sensors up, the located strokes' hours, a level for every station under every documented set of sensors in range, one response to the index fitted within those levels across the stations, the level read on the present network. It files 45.5, 13.7, 12.2, 15.6, 14.2, 13.3 and 11.8 hours and a crew at Callory Downs alone: Penrow Sound 13.7 against 28.3 (refuted by K1: its hours miss the replay test by 0.940) and Weymoor Gap 15.6 against 28.6 (refuted by K2: the peak currents located there miss its sensor count's prediction by 0.224). Its hold-out on the located hours passes (fit to 2017-18 and forecast over the eight seasons since, the record's mean and a regression on the index miss by 1.1 to 11.1 hours a season, the mean ahead at four stations, the regression at two, level at one) because both sides are the same thinned record.
Said out loud: S1: "The strokes the network missed shorten stand-downs, split them and erase whole days, so recorded hours do not answer to detection in proportion." Five steps left: fit the peak-current law through the filed curve; find the days seen well enough to stand for what fell; thin them to each station's sensor level and rerun the timer; read each recorded day by its recorded size and estimate the days that left no record; carry the hours to the season. S3: "A legacy receiver does not add what a standard sensor adds to detection." Four steps left: fit the law on the days no legacy receiver was up; write the located currents' likelihood under a level of standard sensors plus a fraction of the legacy receivers; profile the fraction; carry the level into both the strokes and the replay.
Worth: S1 is worth 15.6 hours on Penrow Sound, 15.3 times the family's spread there (1.02); S3 is worth 11.4 hours on Weymoor Gap, 13.2 times the family's spread there (0.862). Bands: Penrow Sound's average-season hours 26.25 (24.9 to 27.3; S1 lost 11.8); Weymoor Gap's average-season strokes 258.4 (240.1 to 262.6; S3 lost 119). Each stump is two-sided on its own (corelib's `sides`): S1 pushed past its fitted value alone, the hours raised in proportion to the strokes missed with the legacy worth fitted, files 78.5, 40.5, 35.0, 42.6, 18.9, 40.6 and 33.4 hours, a crew at every station but Yanda Creek; S3 pushed past its fitted value alone, a legacy receiver worth nothing, files 58.4, 27.9, 28.4, 39.3, 16.3, 23.5 and 28.9 hours, a fifth crew at Burrel Bay. Swept on the golden, the call needs the worth between about 0.15 and 0.46 (the world's 0.30, the fitted 0.32): at 0.0 and 0.1 Burrel Bay is over the line (28.9, 26.1), from 0.2 to 0.4 the call is the golden's (Weymoor Gap 32.5 to 26.7, Burrel Bay 24.1 to 20.1), at 0.5 and above Weymoor Gap is under it (24.1 and less).
Regimes: second stump. S1's correction is checked on the well-covered days (K1) and cannot be checked on a thin station's own record except through its outage days (K4, at a sampling error of 0.08, which rules on nothing); it opens Penrow Sound and with it Mornay Inlet. S3 opens Weymoor Gap: there the level itself is unfiled, and no day at the station is seen by standard sensors alone.
Sharp: S1: (1) its wrong route passes a hold-out of seasons on the located hours and a bootstrap of seasons, and a share calibrated on a cut of the well-covered days passes on the days it was cut to; (2) its right route needs a commitment to a simulated quantity (the hours a thinned day stands for) with no observed hour to score it at any thin station; (3) the evidence sits in the sensor log and the vendor's sheet, not in the strokes; (4) the correction differs across stations by their day sizes and sensors (the located strokes' hours are 0.73, 0.45, 0.43, 0.47, 0.74, 0.55 and 0.49 of the golden's), so no one share serves them: a share right for Mornay Inlet's days of one or two strokes over-corrects Tarrick Tableland's large ones; (5) its own figure is Penrow Sound's average-season hours. S3: (1) its wrong route passes every check a count of sensors can pass (the log is right, the table is right); (2) its right route commits to a number no document holds (0.32, the world's 0.30), and both defaults miss, a receiver counted as a sensor at Weymoor Gap and a receiver counted as nothing at Burrel Bay; (3) the evidence sits in the peak currents of the strokes against the sensor register's types; (4) it moves the five stations a legacy receiver reaches by different amounts (hours 0.85, 0.60, 0.87, 0.87 and 0.64 of the golden's at Callory Downs, Weymoor Gap, Yanda Creek, Tarrick Tableland and Burrel Bay) and leaves the other two; (5) its own figure is Weymoor Gap's average-season ground strokes.
Earns: on corelib's rubric (18 the call, 20 the two components, 53 the asks in eight sentences, 9 instruction-following): the golden 100; S1 lost alone 19; S3 lost alone 19; the reflex route (both lost) 9; the rigorous standard route 9; the run routes generous 9, calibrated 9, hedge 9, cut-off 9; S1 fixed alone on the reflex route 19, S3 fixed alone 19. Beside them: the missed strokes put back 9, the outage-day elasticity 9, one share of hours at each sensor count with the legacy worth fitted 19. The run routes' 55 further settings (the tables below) each file a wrong call; the dearest, a calibration cut at six located strokes with the legacy worth fitted, earns 42. Priced per figure in place of per sentence: S1 lost alone 34, S3 lost alone 35, both lost 14, and the dearest further setting 71 (it lands both components and 23 of the 29 ask figures inside their stretched bands while filing Tarrick Tableland over the line and Mornay Inlet under it). The reflex route still lands three figures (the strokes at Mornay Inlet and Penrow Sound, and the season's percentage) and no whole sentence; they are kept because each sits on a line whose other figures a stump decides. The supporting step left out alone (the response read on the corrected hours in place of the strong strokes) files the golden's call with the season at 107.3 per cent of an average one against 107.9, inside every band; with no state carried at all (the record's mean, the filed outlook ignored) the route earns 74, every season figure 7 per cent low, and still files the golden's call at the golden's conventions.

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| Callory Downs (A) | 25 | 52.87 | 2.15 | 38.34 | 35.53 | 45.45 | forced |
| Burrel Bay (B) | 25 | 21.57 | 0.718 | 10.49 | 9.725 | 11.76 | forced (it moves with S3 the other way: a receiver worth nothing puts it over the line) |
| Weymoor Gap (V) | 25 | 28.57 | 0.862 | 13.52 | 12.52 | 15.57 | S3 |
| Tarrick Tableland (W) | 25 | 21.9 | 0.889 | 12.04 | 10.79 | 13.3 | forced |
| Mornay Inlet (X) | 25 | 28.07 | 1.66 | 12.2 | 10.85 | 12.16 | forced (it moves with S1, as Penrow Sound does) |
| Yanda Creek (Y) | 25 | 14.99 | 0.324 | 11.09 | 10.28 | 14.15 | forced |
| Penrow Sound (Z) | 25 | 28.33 | 1.02 | 12.71 | 10.49 | 13.72 | S1 |

Leave-one-out and leave-two-out (expected stand-down hours this season; the call; the falsification score):

| Route | Callory Downs | Penrow Sound | Mornay Inlet | Weymoor Gap | Yanda Creek | Tarrick Tableland | Burrel Bay | Crews at | Score |
|---|---|---|---|---|---|---|---|---|---|
| golden | 52.9 | 28.3 | 28.1 | 28.6 | 15.0 | 21.9 | 21.6 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 0.026 |
| S1 left out | 38.3 | 12.7 | 12.2 | 13.5 | 11.1 | 12.0 | 10.5 | Callory Downs | 0.544 |
| S3 left out | 45.0 | 27.7 | 28.3 | 17.2 | 13.1 | 19.1 | 13.7 | Callory Downs, Penrow Sound, Mornay Inlet | 0.133 |
| both left out | 38.3 | 12.7 | 12.2 | 13.5 | 11.1 | 12.0 | 10.5 | Callory Downs | 0.559 |
| the supporting step left out (no state carried) | 49.0 | 26.3 | 26.0 | 26.5 | 13.9 | 20.3 | 20.0 | the golden's four | 0.063 |

| Run route | Callory Downs | Penrow Sound | Mornay Inlet | Weymoor Gap | Yanda Creek | Tarrick Tableland | Burrel Bay | Crews at | Earns |
|---|---|---|---|---|---|---|---|---|---|
| generous | 53.3 | 39.8 | 34.4 | 19.2 | 14.9 | 31.9 | 15.0 | Callory Downs, Penrow Sound, Mornay Inlet, Tarrick Tableland (Weymoor Gap under, Tarrick Tableland over) | 9 |
| calibrated | 40.1 | 20.2 | 18.3 | 14.2 | 11.5 | 17.5 | 11.0 | Callory Downs | 9 |
| hedge | 35.5 | 11.8 | 11.3 | 12.5 | 10.3 | 11.2 | 9.7 | Callory Downs | 9 |
| cut-off | 41.9 | 14.3 | 11.7 | 16.2 | 14.9 | 18.2 | 13.2 | Callory Downs | 9 |
| the missed strokes put back | 47.0 | 21.6 | 20.3 | 16.6 | 13.1 | 18.0 | 13.0 | Callory Downs | 9 |
| the outage-day elasticity | 41.5 | 18.3 | 16.9 | 14.8 | 11.8 | 16.3 | 11.5 | Callory Downs | 9 |
| one share of hours at each sensor count, legacy worth fitted | 49.6 | 21.9 | 19.8 | 23.1 | 13.2 | 21.3 | 18.0 | Callory Downs | 19 |

Each stump pushed past its fitted value alone, everything else the golden's (corelib's `sides`; expected stand-down hours this season):

| Over-correction | Callory Downs | Penrow Sound | Mornay Inlet | Weymoor Gap | Yanda Creek | Tarrick Tableland | Burrel Bay | Crews at |
|---|---|---|---|---|---|---|---|---|
| S1: hours raised in proportion, legacy worth fitted | 78.5 | 40.5 | 35.0 | 42.6 | 18.9 | 40.6 | 33.4 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Tarrick Tableland, Burrel Bay |
| S3: a legacy receiver worth nothing | 58.4 | 27.9 | 28.4 | 39.3 | 16.3 | 23.5 | 28.9 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Burrel Bay |

The legacy worth swept on the golden (the fitted value is 0.32; the last column is Weymoor Gap's average-season ground strokes):

| Worth of a legacy receiver | Callory Downs | Penrow Sound | Mornay Inlet | Weymoor Gap | Yanda Creek | Tarrick Tableland | Burrel Bay | Crews at | Weymoor Gap's strokes |
|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 58.4 | 27.9 | 28.4 | 39.3 | 16.3 | 23.5 | 28.9 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Burrel Bay | 426 |
| 0.10 | 56.5 | 27.9 | 28.1 | 35.3 | 15.8 | 22.9 | 26.1 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Burrel Bay | 362 |
| 0.20 | 54.8 | 27.4 | 28.0 | 32.5 | 15.4 | 22.4 | 24.1 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 313 |
| 0.30 | 53.3 | 28.1 | 28.6 | 29.6 | 15.0 | 21.9 | 21.9 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 268 |
| 0.40 | 51.8 | 27.4 | 28.0 | 26.7 | 14.6 | 21.4 | 20.1 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 231 |
| 0.50 | 50.5 | 28.1 | 28.1 | 24.1 | 14.3 | 21.1 | 18.8 | Callory Downs, Penrow Sound, Mornay Inlet | 200 |
| 0.60 | 48.9 | 28.2 | 27.9 | 22.2 | 14.0 | 20.5 | 17.3 | Callory Downs, Penrow Sound, Mornay Inlet | 175 |
| 1.00 | 45.0 | 27.7 | 28.3 | 17.2 | 13.1 | 19.1 | 13.7 | Callory Downs, Penrow Sound, Mornay Inlet | 119 |

The worth read off the count of strong strokes on legacy days (the located strokes at or over the threshold, over the fitted law's tail share), then the golden's replay. This is S3 made by one moment of the amplitudes, and it files the golden's call:

| Strong strokes from | Worth | Callory Downs | Penrow Sound | Mornay Inlet | Weymoor Gap | Yanda Creek | Tarrick Tableland | Burrel Bay | Crews at | Weymoor Gap's strokes |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kA | 0.45 | 51.0 | 28.0 | 28.2 | 25.1 | 14.4 | 21.2 | 19.4 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 215 |
| 60 kA | 0.38 | 52.2 | 28.0 | 28.6 | 27.1 | 14.7 | 21.5 | 20.6 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 239 |
| 80 kA | 0.39 | 51.8 | 27.4 | 28.0 | 26.7 | 14.6 | 21.4 | 20.1 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 231 |
| 40 kA, their own filed share located allowed for | 0.37 | 52.2 | 28.0 | 28.6 | 27.4 | 14.7 | 21.6 | 20.7 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 242 |
| 60 kA, their own filed share located allowed for | 0.36 | 52.3 | 27.4 | 28.0 | 27.7 | 14.7 | 21.6 | 20.8 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 246 |
| 80 kA, their own filed share located allowed for | 0.38 | 52.2 | 28.0 | 28.6 | 27.1 | 14.7 | 21.5 | 20.6 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap | 239 |

The run routes' further settings (`run_routes["<route>:<label>"]`; expected stand-down hours this season; the golden files crews at Callory Downs, Penrow Sound, Mornay Inlet and Weymoor Gap). The cut-off family keeps only the well-covered days on which the full network located at most k strokes, thins them to each sensor count, reads one share of hours per count and divides each station's recorded hours by it, with the golden's season factor:

| Setting | Callory Downs | Penrow Sound | Mornay Inlet | Weymoor Gap | Yanda Creek | Tarrick Tableland | Burrel Bay | Crews at | Furthest past the line, least over three thinning draws | Replay test by day size (largest miss) |
|---|---|---|---|---|---|---|---|---|---|---|
| cut-off at 2 located strokes, legacy worth fitted | 64.0 | 33.5 | 28.7 | 34.5 | 15.8 | 32.9 | 27.0 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Tarrick Tableland, Burrel Bay | Tarrick Tableland by 7.2 hours | 0.465 |
| cut-off at 2, legacy receivers as listed | 41.5 | 23.4 | 20.6 | 14.6 | 11.9 | 19.5 | 11.4 | Callory Downs | - | - |
| cut-off at 3 located strokes, legacy worth fitted | 62.1 | 31.1 | 26.8 | 33.3 | 15.4 | 31.1 | 26.0 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Tarrick Tableland, Burrel Bay | Tarrick Tableland by 5.7 hours | 0.412 |
| cut-off at 3, legacy receivers as listed | 41.6 | 22.8 | 20.4 | 14.7 | 11.9 | 19.3 | 11.4 | Callory Downs | - | - |
| cut-off at 4 located strokes, legacy worth fitted | 58.8 | 28.8 | 25.2 | 30.4 | 14.8 | 28.6 | 23.7 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Tarrick Tableland | Tarrick Tableland by 3.4 hours | 0.339 |
| cut-off at 4, legacy receivers as listed | 41.5 | 22.5 | 20.0 | 14.7 | 11.9 | 19.0 | 11.4 | Callory Downs | - | - |
| cut-off at 5 located strokes, legacy worth fitted | 57.4 | 27.7 | 24.4 | 29.0 | 14.6 | 27.6 | 22.7 | Callory Downs, Penrow Sound, Weymoor Gap, Tarrick Tableland | Tarrick Tableland by 2.3 hours | 0.294 |
| cut-off at 5, legacy receivers as listed | 41.3 | 22.2 | 19.9 | 14.6 | 11.9 | 18.8 | 11.4 | Callory Downs | - | - |
| cut-off at 6 located strokes, legacy worth fitted | 56.1 | 26.9 | 23.7 | 28.2 | 14.4 | 26.6 | 22.0 | Callory Downs, Penrow Sound, Weymoor Gap, Tarrick Tableland | Tarrick Tableland by 1.6 hours | 0.263 |
| cut-off at 6, legacy receivers as listed | 41.3 | 22.2 | 19.9 | 14.6 | 11.9 | 18.9 | 11.4 | Callory Downs | - | - |
| cut-off at 7 located strokes, legacy worth fitted | 55.5 | 26.3 | 23.4 | 27.8 | 14.3 | 26.0 | 21.7 | Callory Downs, Penrow Sound, Weymoor Gap, Tarrick Tableland | Mornay Inlet by 1.6 hours | 0.243 |
| cut-off at 7, legacy receivers as listed | 41.3 | 22.0 | 19.7 | 14.6 | 11.9 | 18.6 | 11.3 | Callory Downs | - | - |
| cut-off at 8 located strokes, legacy worth fitted | 55.4 | 25.8 | 22.8 | 27.5 | 14.2 | 25.5 | 21.5 | Callory Downs, Penrow Sound, Weymoor Gap, Tarrick Tableland | Mornay Inlet by 2.0 hours | 0.244 |
| cut-off at 8, legacy receivers as listed | 41.2 | 21.7 | 19.5 | 14.6 | 11.8 | 18.5 | 11.3 | Callory Downs | - | - |
| cut-off at 10 located strokes, legacy worth fitted | 54.0 | 25.0 | 22.0 | 26.4 | 14.0 | 24.6 | 20.6 | Callory Downs, Weymoor Gap | Mornay Inlet by 2.8 hours | 0.273 |
| cut-off at 10, legacy receivers as listed | 41.3 | 21.8 | 19.6 | 14.6 | 11.9 | 18.6 | 11.3 | Callory Downs | - | - |
| cut-off at 12 located strokes, legacy worth fitted | 54.0 | 25.0 | 22.3 | 26.2 | 14.0 | 24.6 | 20.5 | Callory Downs, Weymoor Gap | Mornay Inlet by 2.6 hours | 0.279 |
| cut-off at 12, legacy receivers as listed | 41.3 | 21.6 | 19.4 | 14.6 | 11.9 | 18.5 | 11.4 | Callory Downs | - | - |
| cut-off at 15 located strokes, legacy worth fitted | 53.1 | 24.6 | 22.0 | 25.9 | 13.9 | 24.2 | 20.2 | Callory Downs, Weymoor Gap | Mornay Inlet by 3.0 hours | 0.295 |
| cut-off at 15, legacy receivers as listed | 41.3 | 21.5 | 19.3 | 14.6 | 11.9 | 18.4 | 11.4 | Callory Downs | - | - |
| cut-off at 20 located strokes, legacy worth fitted | 52.5 | 23.9 | 21.5 | 25.3 | 13.8 | 23.4 | 19.8 | Callory Downs, Weymoor Gap | Mornay Inlet by 3.5 hours | 0.320 |
| cut-off at 20, legacy receivers as listed | 41.3 | 21.5 | 19.3 | 14.6 | 11.9 | 18.4 | 11.4 | Callory Downs | - | - |
| cut-off at 30 located strokes, legacy worth fitted | 51.7 | 23.3 | 21.0 | 24.5 | 13.6 | 22.9 | 19.2 | Callory Downs | Mornay Inlet by 3.9 hours | 0.344 |
| cut-off at 30, legacy receivers as listed | 41.3 | 21.4 | 19.3 | 14.6 | 11.9 | 18.3 | 11.4 | Callory Downs | - | - |
| calibrated: the well-covered days of Callory Downs alone | 48.5 | 20.9 | 19.1 | 22.0 | 13.0 | 20.3 | 17.2 | Callory Downs | - | - |
| calibrated: the well-covered days of Yanda Creek alone | 53.9 | 25.0 | 22.4 | 26.3 | 14.0 | 24.6 | 20.5 | Callory Downs, Penrow Sound, Weymoor Gap | - | - |
| calibrated: the well-covered days of 2010-11 to 2017-18 | 48.8 | 21.3 | 19.3 | 22.3 | 13.1 | 20.6 | 17.4 | Callory Downs | - | - |
| calibrated: the well-covered days since 2018-19 | 50.3 | 22.3 | 20.2 | 23.5 | 13.4 | 21.8 | 18.3 | Callory Downs | - | - |
| calibrated: a ratio by recorded size class, re-weighted to each station's recorded mix | 47.8 | 22.4 | 21.7 | 23.8 | 13.4 | 19.6 | 18.0 | Callory Downs | - | - |
| the same, legacy receivers as listed | 40.9 | 19.3 | 17.8 | 14.4 | 11.7 | 16.9 | 11.2 | Callory Downs | - | - |
| generous: hours raised in proportion, the worth from the count of strong strokes | 75.7 | 40.5 | 35.0 | 39.4 | 18.5 | 39.8 | 30.9 | Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap, Tarrick Tableland, Burrel Bay | - | - |

All 55 settings (the 31 rows above and two more thinning draws of each of the twelve cuts at the fitted worth) file a wrong call; none files the golden's. The cut family's least closure is 1.6 hours, at a cut of six located strokes. The replay test by the day's size, golden against the one-share routes (log points; days of one or two strokes, three to five, six to nineteen, twenty or more on the full network):

| Route | 1 or 2 | 3 to 5 | 6 to 19 | 20 or more | Largest |
|---|---|---|---|---|---|
| golden (the replay by recorded size) | 0.044 | 0.010 | 0.009 | 0.025 | 0.044 |
| one share, every well-covered day | 0.404 | 0.156 | 0.021 | 0.077 | 0.404 |
| one share, cut at 2 located strokes | 0.012 | 0.237 | 0.374 | 0.465 | 0.465 |
| one share, cut at 3 located strokes | 0.061 | 0.184 | 0.320 | 0.412 | 0.412 |
| one share, cut at 4 located strokes | 0.131 | 0.116 | 0.254 | 0.339 | 0.339 |
| one share, cut at 5 located strokes | 0.182 | 0.064 | 0.200 | 0.294 | 0.294 |
| one share, cut at 6 located strokes | 0.212 | 0.036 | 0.173 | 0.263 | 0.263 |
| one share, cut at 7 located strokes | 0.232 | 0.015 | 0.151 | 0.243 | 0.243 |
| one share, cut at 8 located strokes | 0.244 | 0.004 | 0.138 | 0.233 | 0.244 |
| one share, cut at 10 located strokes | 0.273 | 0.026 | 0.110 | 0.206 | 0.273 |
| one share, cut at 12 located strokes | 0.279 | 0.032 | 0.104 | 0.198 | 0.279 |
| one share, cut at 15 located strokes | 0.295 | 0.048 | 0.088 | 0.183 | 0.295 |
| one share, cut at 20 located strokes | 0.320 | 0.073 | 0.063 | 0.158 | 0.320 |
| one share, cut at 30 located strokes | 0.344 | 0.097 | 0.040 | 0.134 | 0.344 |

Read by day size the golden's largest miss is 0.044; the least of the one-share routes' largest misses is 0.243 (the cut at seven), 5.6 times it. The dearest further setting earns 42 per sentence and 71 per figure.

| Figure | Block | Golden | Band | S1 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|
| C1 average-season hours at Penrow Sound | components | 26.25 | 24.9 to 27.3 | moves | - | lost |
| C2 average-season ground strokes at Weymoor Gap | components | 258.4 | 240.1 to 262.6 | - | moves | lost |
| this season's hours, Callory Downs | asks | 52.87 | 51.59 to 55.71 | moves | moves | lost |
| this season's hours, Mornay Inlet | asks | 28.07 | 25.73 to 29.76 | flips | - | lost |
| this season's hours, Burrel Bay | asks | 21.57 | 20.57 to 22.25 | moves | moves | lost |
| this season's hours, Penrow Sound | asks | 28.33 | 26.87 to 29.46 | flips | - | lost |
| this season's hours, Weymoor Gap | asks | 28.57 | 27.32 to 29.59 | flips | flips | lost |
| this season's hours, Yanda Creek | asks | 14.99 | 14.58 to 15.46 | moves | moves | lost |
| this season's hours, Tarrick Tableland | asks | 21.9 | 21.19 to 23.1 | moves | moves | lost |
| average-season hours, Callory Downs | asks | 48.99 | 47.81 to 51.62 | moves | moves | lost |
| average-season hours, Mornay Inlet | asks | 26.01 | 23.84 to 27.58 | moves | - | lost |
| average-season hours, Burrel Bay | asks | 19.99 | 19.09 to 20.46 | moves | moves | lost |
| average-season hours, Penrow Sound | asks | 26.25 | 24.9 to 27.3 | moves | - | lost |
| average-season hours, Weymoor Gap | asks | 26.47 | 25.32 to 27.42 | moves | moves | lost |
| average-season hours, Yanda Creek | asks | 13.89 | 13.51 to 14.33 | moves | moves | lost |
| average-season hours, Tarrick Tableland | asks | 20.29 | 19.63 to 21.41 | moves | moves | lost |
| average-season strokes, Callory Downs | asks | 1085 | 1053 to 1093 | - | moves | lost |
| average-season strokes, Mornay Inlet | asks | 178.2 | 176.4 to 178.9 | - | - | earned |
| average-season strokes, Burrel Bay | asks | 235.8 | 219.1 to 239.6 | - | moves | lost |
| average-season strokes, Penrow Sound | asks | 254.2 | 251.2 to 255.4 | - | - | earned |
| average-season strokes, Weymoor Gap | asks | 258.4 | 240.1 to 262.6 | - | moves | lost |
| average-season strokes, Yanda Creek | asks | 139.2 | 136.3 to 139.8 | - | moves | lost |
| average-season strokes, Tarrick Tableland | asks | 495.4 | 479.9 to 499.7 | - | moves | lost |
| this season as a per cent of an average one | asks | 107.9 | 106.4 to 110.6 | - | - | earned |
| break-even season, Callory Downs | asks | 51.03 | 48.39 to 52.25 | moves | moves | lost |
| break-even season, Penrow Sound | asks | 95.24 | 91.48 to 100.3 | moves | - | lost |
| break-even season, Mornay Inlet | asks | 96.13 | 90.38 to 104.6 | moves | - | lost |
| break-even season, Weymoor Gap | asks | 94.45 | 91.08 to 98.65 | moves | moves | lost |
| break-even season, Yanda Creek | asks | 180 | 174.4 to 185 | moves | moves | lost |
| break-even season, Tarrick Tableland | asks | 123.2 | 116.7 to 127.2 | moves | moves | lost |
| break-even season, Burrel Bay | asks | 125.1 | 122.1 to 130.9 | moves | moves | lost |

Sentences (one criterion each): three of this season's hours (Callory Downs, Mornay Inlet, Burrel Bay; Penrow Sound, Weymoor Gap; Yanda Creek, Tarrick Tableland), three of an average season's hours and strokes for the same groups, the season's percentage with the break-even seasons of the four stations over the line, and the break-even seasons of the three under it (a break-even season is 25 hours over the station's average-season hours, as a per cent; it needs no form for the response). Seeds: the dials are placed on the record drawn at seed 3909, and of seeds 3909 to 3913 that one alone passes. The failures differ seed by seed and have one cause: a station's 24-season record moves its figure about 2 hours from draw to draw (Mornay Inlet 26.0 to 30.0 hours across the five seeds, Tarrick Tableland 18.9 to 23.2, Burrel Bay 20.6 to 25.4), and the cut-off family is closed only by stations within about 3 hours of the line on both sides of it. At 3910 a battery variant moves Mornay Inlet under the line; at 3911 Burrel Bay's record comes out over the line (25.4 against the world's 24.0) and the golden misses the world's call; at 3912 Tarrick Tableland draws low (18.9) and the cuts at two to six strokes file the golden's call; at 3913 the cuts at seven and eight do. So the world is the one at seed 3909 and the build draws no other; what holds there with little room is listed in `## Frontier check`, Forcing.

Last line: `CORE PASS level 4  task3 architecture 9` (corelib's verdict), followed by core.py's own lines: the three extra routes' prices, the supporting step read both ways (`it files AZXV, the golden's call` for the response on the corrected hours; for no state carried at all `the nearest station it keeps over the line is X, 4.0 per cent over; in the battery's lowest variant X is 2.1 per cent under the line`), the further settings' prices (`the dearest further setting earns 42 per sentence ... and 71 per figure`), the strong-stroke worth's price and `priced per figure in place of per sentence: S1 lost alone earns 34, S3 lost alone 35, both lost 14`

## Stump factorial

Reflex route: the strokes brought to local days and set against the sensor log; re-sent batches and superseded solutions counted once; cloud pulses and the strokes outside 8 km left out; the days on which no location was possible taken out of each season's exposure; the peak-current law fitted through the filed curve and the counts raised by the share located; a response to the shelf index fitted and carried to the outlook value; a hold-out of seasons and a bootstrap run on the result; the hours taken as the located strokes give them and every sensor in the log counted alike. It files a relief crew at Callory Downs alone (38.3, 12.7, 12.2, 13.5, 11.1, 12.0 and 10.5 hours) and earns 9. This route is the careful but hurried pass.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 what the timer would have run on the strokes the network missed: the hours rebuilt by replaying the rule on the well-covered days thinned to each sensor level, each recorded day read by its size | stump | the located strokes' hours, or those hours raised by the share of strokes missed, or the missed strokes put back between the located ones | L56, N21, L57 | a crew at Callory Downs alone (Penrow Sound 12.7, Mornay Inlet 12.2, Weymoor Gap 13.5) | a crew at Callory Downs, Penrow Sound and Mornay Inlet, Weymoor Gap still under at 17.2; rescues R4 and R5 | no: five steps |
| S3 what a legacy receiver adds to detection: fitted from the peak currents located on its days against the law fitted elsewhere | stump | every sensor in the log counted alike in the filed table | N42, L58 | a crew at Callory Downs, Penrow Sound and Mornay Inlet (Weymoor Gap 17.2) | a crew at Callory Downs alone (Weymoor Gap 13.5); rescues R3 | no: four steps |
| J3 the season's state: the response to the shelf index read on the strong strokes and carried to the outlook value | reflex (a supporting step next to closed cards) | the response read on the located or the corrected hours, or the record's mean carried | R03; the bureau's bulletin; the rigorous standard route fits it | same call (read on the corrected hours the season is 107.3 per cent against 107.9; with the record's mean every season figure is 7 per cent low) | - | - |
| J4 the strokes on local days against the sensor log, the days no location was possible out of the exposure | reflex | - | R01, R46; the vendor's sheet | same call | - | - |
| J5 re-sent batches, superseded solutions, cloud pulses and strokes outside the ring left out | reflex | - | R01; the operator's data notes | same call | - | - |
| J6 the peak-current law through the filed curve and the counts raised by the share located | reflex | - | R98 (a filed loss form fitted and put back event by event) | same call | - | - |
| J7 the stand-down as the union of the intervals, the window, the line and the average season as filed | reflex | - | the standard 3.1 to 3.3; the procedure 2 | same call | - | - |
| J8 a hold-out of seasons and a bootstrap of seasons on whatever route is built | reflex | - | R03, R04 | same call | - | - |

Level: 4: two necessary stumps, neither sufficient alone, each two-sided on its own, the two single drops on two distinct wrong calls, the generous run route on a third and the two over-corrections on a fourth and a fifth.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| Penrow Sound | 28.33 against the line of 25 (3.33 over, 3.3 spreads) | 1.02 | wrong: 12.71, no crew | wrong: 10.49, no crew | S1 |
| Weymoor Gap | 28.57 (3.57 over, 4.1 spreads) | 0.862 | wrong: 13.52, no crew | wrong: 12.52, no crew | S3 |
| Mornay Inlet | 28.07 (3.07 over, 1.8 spreads) | 1.66 | wrong: 12.2, no crew | wrong: 10.85, no crew | forced by S1 with Penrow Sound (not counted as a second open member) |
| Callory Downs | 52.87 (27.87 over) | 2.15 | right: 38.34, a crew | right: 35.53, a crew | forced |
| Tarrick Tableland | 21.9 (3.1 under, 3.5 spreads) | 0.889 | right: 12.04, no crew | right: 10.79, no crew | forced (the generous run route files it over, at 31.9, and so does every calibration cut at eight located strokes or fewer) |
| Burrel Bay | 21.57 (3.43 under, 4.8 spreads) | 0.718 | right: 10.49, no crew | right: 9.725, no crew | forced (a legacy receiver worth nothing files it over, at 28.9) |
| Yanda Creek | 14.99 (10.01 under) | 0.324 | right: 11.09, no crew | right: 10.28, no crew | forced |

Direct route: the pack's most direct evidence read at face value is the located strokes themselves: the timer run on them as they stand, averaged over the seasons on record (`route_direct` in core.py). It files 35.5, 10.5, 10.8, 12.5, 10.3, 10.8 and 9.7 hours and a crew at Callory Downs alone; it lands wrong at Penrow Sound, Mornay Inlet and Weymoor Gap because the network located 28, 35 and 31 per cent of their strokes and the days it missed whole are in no file.

## Data provenance

Source: generated by `task3/generator` from a simulated process: storm days at seven stations (a season's count answering to a regional sea-surface index, lognormal day sizes that run small at the coastal stations, a cell's duration growing with its size, a quarter of a day's strokes outside the main cell, peak currents lognormal by polarity and strongest in a cell's mature minutes), and a location network that locates each stroke with the filed chance at the sensors in range and up that day, with sensor outages day by day.
Behaves like the real thing: location networks' detection efficiency rises with peak current and with the number of reporting sensors, and long-range or thinly instrumented regions locate well under half of ground strokes; networks carry mixed sensor generations whose older receivers contribute less; first-stroke peak currents are close to lognormal with medians of 15 to 30 kA and positive strokes run stronger; a stroke-restarted clearance timer at an 8 km radius is the form aerodrome lightning rules take; wet season storm activity in the tropics follows sea-surface temperature indices season to season.
Genuine patterns: (1) storm days a season rising with the shelf index (a factor of about 1.5 across the index's range); (2) heavy-tailed day sizes, a few days carrying most of a season's strokes; (3) peak currents by polarity, positive strokes rarer and stronger; (4) weak strokes at a cell's edges and outside it, so the first and last minutes of a storm are the worst located; (5) a stand-down's length growing with a day's size at a falling rate; (6) the located share rising at each station as its sensors were added in 2010 and 2018.
Problems by process: two clock conventions (the archive in UTC, the sensor log by local day); re-sent batches and reprocessed solutions (the network operator's reprocessing after each upgrade); sensor identifiers renumbered at the upgrades (the register carries both); cloud pulses in the same extract (the network classifies and keeps them); a square extract around each reference point (the operator's query tool), so strokes beyond 8 km come with it; days with fewer than two sensors up (outages at the thin stations); the vendor's sheet covering the standard sensor alone (it was issued with the 2010 upgrade).
Breadth: seven stations by 24 wet seasons; about 27,000 located ground strokes inside the rings and several times that in the extract; a sensor-day status log of 48 sensors over 2,900 season days; 512 well-covered storm days to find among 4,030 with a located stroke; deciding which days stand for what fell, which sensors count for what and which strokes every network sees is the work.

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, modeling, modeling, validation, forecasting, synthesis, uncertainty
Question form: which (which stations carry a relief ramp crew)
Nearest build: by `skeleton.py check`, severity none against every card, the client's corpus and the slot's own lineage. Nearest by elements: task13 architecture 4 (spent; the same three detections, one shared move, a per-unit diagnosis), mark162 (the replay lesson inside a go or hold figure on a leakage forecast) and a spent task7 architecture (the replay lesson inside a pick of options). Architecture 8 of this slot shares the subdomain and the analysis type and nothing of the skeleton: its form was a banded class on a count, its lessons a loss convex in a rate, a support effect and a store that delays the record; this one is a set over a line on a duration, decided by a rule replayed on thinned records and an unfiled sensitivity fitted from a truncation. The gate's nearest-chain WARN names task20, whose weight line mentions this build's weight word in passing: its weight is investigation, its chain is another (assembly, investigation, modeling, two forecasts, two syntheses) and its decision a pick among a consultant's programmes; the two share the answer shape and nothing else. The house shell WARN (`set_over_threshold` on five live builds) is answered by the decision itself: a crew is added station by station against one filed line, and the answer pattern (two single drops and a run route on three different sets) is not shared with any of the five.

## Frontier check

Precedents: R4 careful Missed on L56 (a recording effect seen and kept as a sensitivity, the face-value figure central), N21 (an unmeasured component placed in proportion to the measured quantities) and L57 (a cut where a fitted model was needed). R3 careful Missed on N42 (one instrument's correction put on a second model because the pack holds no check on the second, recorded on this slot's own architecture 8 runs) and L58 (two recording conditions tangled with each other read one at a time). R5 careful Missed on L28 (the estimator certified with checks that cannot see the problem). R7 and R8 fall downstream of R3 and R4 (L63: one decisive step fitted and the other left, so the call moved to a different wrong answer). R1, R2 and R6 are Right.
Shallow path checks: the reflex route's hours pass a hold-out of seasons (fit to 2017-18, forecast the eight seasons since: the record's mean has a root mean square error of 10.6, 2.6, 2.4, 3.5, 4.1, 4.8 and 3.0 hours at the seven stations against 11.1, 2.8, 1.1, 3.8, 4.3, 4.6 and 3.0 for a regression on the index) and a bootstrap of seasons, because both sides of each are the same thinned record; its sensor counts pass every check of the log against the register; and a share of hours calibrated on a cut of the well-covered days passes a replay on the days it was cut to (a cut at eight located strokes misses the days of three to five strokes by 0.004 log points) while missing the days of one or two strokes by 0.244. The checks of another kind: the replay test on the well-covered days read by the day's size (the strokes against the sensor log and the vendor's sheet, at the grain of a storm day) refutes the hours, and the located peak currents by sensor type (the strokes against the register's types, at the grain of a stroke) refute the count.
Assumption made false: (1) recorded stand-down hours stand for the hours, or scale with the share of strokes located (false at every station: the stand-down is a union of intervals, small days vanish and the weak strokes are the edge strokes; the located strokes' hours are 0.43 to 0.74 of the golden's and the proportional raise 0.69 to 1.48; tested by the well-covered days thinned through the vendor's sheet). (2) Every sensor the log lists counts alike (false wherever a legacy receiver is in range: it adds 0.32 of a standard sensor; tested by the peak currents located on its days; and it is not worth nothing either, which the same currents show). Both are assumptions a run writes in its list and moves on from when no file holds the figure (N42).
Forcing: the line is 25 hours. The golden family's 27 variants all file the golden's call; the nearest a variant brings an over-the-line station to the line is Mornay Inlet's 26.4 (the day sizes taken in one step from the well-covered days' own mix, the variant that misses the replay test most, by 0.095; 1.4 hours over), with Penrow Sound's 27.3 next (the day sizes taken in three steps), and the nearest an under-the-line station comes is Tarrick Tableland's 22.8 (donors at seven sensors; 2.2 under), with Burrel Bay's 22.0 next. The shortcuts on the other side: Penrow Sound 12.7 (S1 lost), 21.6 (strokes put back), 20.2 (calibrated), 21.9 (one share at each sensor count); Weymoor Gap 17.2 (S3 lost); above the line, the generous route's Tarrick Tableland 31.9, Burrel Bay's 28.9 with the receivers worth nothing, and Tarrick Tableland's 25.1 to 33.1 under every calibration cut at eight located strokes or fewer. Each fitted input moved by its spread: the legacy worth across 0.32 to 0.36 (the call holds from about 0.15 to 0.46), the law across four sets of days and one or two polarities, the response across the battery's ten fits, two of them straight lines in the index (the season's percentage 107.1 to 109.9), the day-size classes coarser and finer, the unfolding in one step or to convergence: the call holds under every one. What holds with little room, said plainly: Mornay Inlet's 1.4 hours in the battery's lowest variant; the cut-off family's closure, least at a cut of six located strokes, where the station furthest past the line is 1.6 hours past it in the worst of three thinning draws (Tarrick Tableland over, Mornay Inlet under); the record's mean route, which keeps Mornay Inlet 4.0 per cent over the line at the golden's conventions and loses it in the battery's lowest variant; and the placement itself, which passes at seed 3909 and at none of 3910 to 3913. The build re-runs the battery on the cut pack and adds each input moved by 20 per cent.
Noun swap: nearest on file by `skeleton.py check`: severity none. Swapping task13 architecture 4's nouns in (feeders and fault causes) carries the three detections and one move and nothing else: no form, no lesson, no answer pattern. Swapping mark162's in (pressure zones and a valve setting replayed) carries one lesson and its move into a different decision form with different file roles. Severity none.
Closed strategies: the call turns on `device_setting_replay` (S1) and `latent_structure_estimation` (S3), both open. S1's nearest closed cards are "some groups are recorded far less completely than others" (fix already used: gross up by completeness) and "a straight line or an average misprices the margin": here the gross-up is the hurried route and files the wrong call on the high side (the generous route), and what is estimated beyond it is a response of a rule's output to the missed events, by the day's size, from a replay of the rule on thinned records, with the days that left no record estimated; no recording share, checked sample or curve hands it over. S3's nearest closed cards are "a source that reads high or low, calibrated on checked cases" and "the instrument changed": no checked case exists (no station was seen by two networks, no figure for a legacy receiver is filed), and what is estimated is a sensitivity identified only by the cut it leaves in the located peak currents, jointly with a law fitted on other days. One closed lesson is kept as a supporting step: `measurement_basis_break` (the season's response read on the strong strokes, the signal the network's changes could not move, next to the closed cards of a change of instrument and a co-occurring change). Left out alone (the response read on the corrected hours instead) it files the golden's call with the season at 107.3 per cent against 107.9; with no state carried at all (core.py's `mean` route, the corrected record's mean, the filed outlook ignored) every season figure is 7 per cent low and the call is still the golden's at the golden's conventions, so the call does not turn on it. `measurement_basis_break` is taught by two tasks on file and `latent_structure_estimation` sits on two of our live builds (task18, task5): here the first is one step among several and never decides, and the second is an instrument's unfiled sensitivity, where task18's and task5's are a dealing distribution and a population never listed.
Decisive steps: S1's answer: an average wet season stands Penrow Sound's ramp down for 26.3 hours (24.9 to 27.3). Asked for by "the hours ... that an average wet season on the 2002-03 to 2025-26 record would bring under the standard", for every station, in the CSV and the workbook. Evidence: the stroke extract's time and peak current fields against the sensor status log's daily counts and the vendor's sheet. Once named, five steps are left. S3's answer: an average wet season brings Weymoor Gap 258 cloud-to-ground strokes within 8 km (240 to 263). Asked for by "the cloud-to-ground strokes within 8 km that an average wet season ... would bring", for every station, in the same files. Evidence: the peak currents of the strokes located on the days the sensor register's legacy receivers were up. Once named, four steps are left. Independence, each step left out alone and together (Penrow Sound's hours; Weymoor Gap's strokes; the crews): golden 26.3; 258; Callory Downs, Penrow Sound, Mornay Inlet, Weymoor Gap. S1 left out 11.8; 258; Callory Downs. S3 left out 25.7; 119; Callory Downs, Penrow Sound, Mornay Inlet. Both left out 11.8; 119; Callory Downs.
Run routes: all four are estimator functions in core.py's `run_routes`, run on the simulated world, and each is priced at every setting a run could choose (55 further settings, tabled in `## Stump core`); every one files a wrong call. Generous (`route_generous`): every correction the files suggest at full strength: the law fitted, each day's strokes and hours raised by one over the filed share located at the sensors up, the response fitted on the raised hours; files crews at Callory Downs, Penrow Sound, Mornay Inlet and Tarrick Tableland: Weymoor Gap wrong on the low side (19.2) and Tarrick Tableland wrong on the high side (31.9); earns 9. Its further setting takes the legacy worth off the count of strokes of 60 kA and over (0.38) and raises in proportion: a crew everywhere but Yanda Creek. Calibrated (`route_flat`, end to end on the days the full network saw): those days thinned by the filed chances to each sensor count, the share of their hours left read off count by count, every station's recorded hours divided by it, the sensors counted as the log lists them; files Callory Downs alone: Penrow Sound (20.2), Mornay Inlet (18.3) and Weymoor Gap (14.2) wrong on the low side; earns 9. Its further settings, with the legacy worth fitted: the calibration days of one station (Callory Downs: a crew there alone; Yanda Creek: Mornay Inlet under at 22.4), of one era (a crew at Callory Downs alone either way) and a ratio by recorded size class re-weighted to each thin station's recorded mix (`route_sizemix`, no erased day estimated: Callory Downs alone). Hedge (every signal noticed and kept as a sensitivity, the located strokes' hours and the record's mean central): Callory Downs alone, the three wrong on the low side (11.8, 11.3, 12.5); earns 9. Cut-off (`route_cutoff`, the seasons on the present network only and the warm ones among them as the window's analogues): Callory Downs alone, the three wrong on the low side (14.3, 11.7, 16.2); earns 9. Its further settings are the cut a run puts in place of the replay's fit: the calibration days kept only where the full network located at most k strokes, k from 2 to 30, with the legacy worth fitted (three thinning draws each) and with the receivers as listed. With the worth fitted the cuts at 2 and 3 file six crews (Tarrick Tableland and Burrel Bay over), the cut at 4 five (Tarrick Tableland over), the cuts at 5 to 8 Tarrick Tableland over and Mornay Inlet under, the cuts at 10 to 20 Mornay Inlet under with Penrow Sound at or under the line beside it, the cut at 30 Callory Downs alone; the station furthest past the line is never less than 1.6 hours past it. With the receivers as listed every cut files Callory Downs alone. The dearest of the 55 earns 42 (71 priced per figure). Three more a run can build are priced beside them: the missed strokes put back and the timer rerun (9), the outage days' elasticity of hours to the filed share (9), and the calibrated route with the legacy worth fitted (19). The misses fall on both sides of the line. One estimator a run could reach is not a wrong route and is said plainly: the legacy worth read off the count of strong strokes (the strokes of 40, 60 or 80 kA and over on legacy days over the fitted law's tail share: 0.45, 0.38 and 0.39) is S3 made by one moment of the same amplitudes, and with the golden's replay it files the golden's call (Weymoor Gap 25.1, 27.1 and 26.7 hours); with the strong strokes' own filed share located allowed for (0.37, 0.36 and 0.38) it is a variant of the battery. Without the replay it earns S3's figures and loses S1's.
Validation handles: every shipped file against each stump's parameter: can a run that fits every free parameter by likelihood or least squares fit or score the parameter from that file alone or with one other?

| Shipped file | S1: what recorded hours stand for at a station's sensors | S3: what a legacy receiver adds |
|---|---|---|
| the stroke extract (located strokes: time, position, peak current, type, version) | no: it holds no hour and no stroke the network missed; alone it gives the located strokes' hours | no: alone it has no sensor counts |
| the sensor status log and the sensor register | no: counts and types of sensors, no strokes | no: it lists the legacy receivers and never what one adds |
| the stroke extract with the sensor log | no direct fit: no station-day is seen at two sensor levels, and a regression of recorded hours on the sensors up across outage days (the elasticity route) files the wrong call | no direct fit: recorded counts and hours on legacy days mix the receiver's worth with the day sizes; the worth comes only through the peak-current law, which needs the vendor's sheet |
| the vendor's detection sheet and the operator's data notes | no: chances for strokes and field descriptions, nothing on hours | no: silent on what a legacy receiver adds |
| the well-covered days (inside the extract: six or more standard sensors up) | a slice that observes hours close to the truth, at two stations whose days run larger: listed as the calibration set. The calibrated route on it (one share of hours kept at each sensor count) files the wrong call (Penrow Sound 20.2 at face count, 21.9 with the legacy worth fitted), and cut to its small days it files a wrong call at every cut from 2 to 30 located strokes and misses the replay test read by day size (0.243 or more against 0.044). Read by recorded day size it is the golden's own estimator, three steps past the calibration | no: those days have no legacy receiver worth fitting (one receiver beside six standard sensors) |
| the station register (reference points) | no | no |
| the shelf index history and the bureau's outlook | no | no |
| the standard and the procedure | no: they file what a stand-down is and the line, no figure | no |
| the flight schedule, the roster and pay file, the ground equipment register (unused) | no: none records a storm, a stroke or a stoppage | no |

No collocated pair ships for either parameter: no station was seen by two networks at once, no on-site detector ran before the window, no stand-down, thunder-day or delay record of any kind is in the pack. The one cell that is not a plain no is S1's on the well-covered days, and it is stated as it stands: a run that thinks to thin those days through the vendor's sheet and rerun the timer by recorded day size has built S1's estimator and earns its figure; the flat calibration a run reads off the same days files the wrong call. S3 has no handle: its parameter is identified only inside the located amplitudes (a profile likelihood, or one moment of it, the count of strong strokes), through the vendor's curve and the register's types together, and no file scores the result.
Forward window: the window's figure is not the record's mean restated: the region's storm days rise with the shelf index (the strong strokes' response, 0.40 log points a unit), the bureau's outlook for the window is +0.5 against a record mean of 0.25, and an average season is the mean of 24 seasons whose first eight ran warm (0.85) and whose last sixteen did not (-0.05). The history-mean route (the corrected record's mean carried) files 49.0, 26.3, 26.0, 26.5, 13.9, 20.3 and 20.0 hours against the golden's 52.9, 28.3, 28.1, 28.6, 15.0, 21.9 and 21.6: every season figure 7 per cent low, six of the seven outside their bands; it earns 74. It leaves a filed sentence unexecuted (the procedure takes the expectation at the bureau's outlook value), and at the golden's conventions it still files the golden's call, Mornay Inlet 4.0 per cent over the line. The outlook value sits inside the index's observed range (-0.6 to 1.3), so nothing is carried past the record.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a stand-down's length | the union of the 15 minute intervals after each stroke; 15 minutes added per stroke | the union | the standard 3.2: operations resume 15 minutes after the last stroke, and a stroke during a stand-down restarts the count |
| SF2 | the strokes that count | cloud-to-ground strokes of either polarity; every archive row; negative strokes only | cloud-to-ground, either polarity | the standard 3.1 and the extract's type field (cloud pulses carry their own type, per the operator's data notes) |
| SF3 | within 8 km | of the station's reference point, 8.0 km inclusive; of the terminal; of the extract's box | the reference point in the station register, inclusive | the standard 3.1 and the station register's reference point |
| SF4 | a stroke counted once | the latest solution of an event; every row | the latest version of each event | the operator's data notes (a reprocessed solution replaces the earlier one; a re-sent batch repeats event ids) |
| SF5 | the clock | the archive in UTC, the status roll by local day (UTC+9:30 all year, no daylight saving); a join on the UTC date | strokes moved to local days before the join | the operator's data notes (the extract's time is UTC, the roll's day is the local date); a UTC-date join puts the 5,075 located strokes that fell before 09:30 local time on the wrong roll day. No stroke on record falls within 15 minutes of local midnight |
| SF6 | sensors in range and up | within the vendor's stated range of the reference point and up for the local day; every sensor in the network | in range and up for the day | the vendor's sheet (the table's count is of sensors in range and up) and the status roll's day grain |
| SF7 | a day with fewer than two sensors up | no location possible, the day out of the season's exposure; a day with no storm; two sensors of the standard type only | out of the exposure, two sensors of either type | the operator's data notes (a solution is issued when two or more of the network's sensors, of either type, report the stroke) |
| SF8 | the hours of the day that count | every hour; operating hours only | every hour | the procedure 2 (stand-down counted across all hours of the day) |
| SF9 | the window and the line | 1 December 2026 to 31 March 2027; over 25 hours | as filed, strictly over | the prompt and the procedure 2 |
| SF10 | an average season | the mean of the 24 seasons 2002-03 to 2025-26 of what the standard would have stood down; a season at the index's mean value (the season's percentage 110.5 in place of 107.9) | the mean of the seasons | the prompt's words and the procedure 2; the other reading files the same call and its percentage sits inside the band |
| SF11 | the expectation for this season | at the bureau's outlook value of +0.5; at the record's mean | at the outlook value | the procedure 2 and the bulletin's single outlook value; the record's mean files every season figure 7 per cent low and misses K3 by 0.100 |
| SF12 | the response to the index | one regional response; a response for each station | one regional response | the bulletin (one index for the northern shelf, the stations' storm activity moving with it together); same call with each station's own |
| SF13 | where the response is read, and its form | the strokes of 60 kA and over; of 50 or 75 kA; the corrected hours; warm seasons against the rest; a constant per cent per index unit; a straight line in the index | 60 kA and over, a constant per cent per index unit | same call: the season's percentage 107.1 to 109.9 across the battery's ten fits, inside its band (the straight lines give 109.9 on the strong strokes and 109.0 on the corrected hours) |
| SF14 | how a legacy receiver counts | as a standard sensor; as nothing; as a fitted fraction, by the located amplitudes' likelihood or by the count of strong strokes; a level of its own for each pairing of sensors up | a fitted fraction (0.32) | named data: counted as a sensor the located peak currents on its days miss by 0.224 log points (K2) against 0.006, and Weymoor Gap files under the line (17.2); counted as nothing, Weymoor Gap's days with one standard sensor or none up could hold no located stroke, and they hold 1,412 of its 1,975, and Burrel Bay files over the line (28.9); the per-pairing fit and the count of strong strokes land inside every band |
| SF15 | what recorded hours stand for | the located strokes' hours; those hours raised by the share missed; the missed strokes put back; an elasticity from the outage days; one share at each sensor count, read off every well-covered day or off those of at most k located strokes; the timer replayed on thinned days by recorded size | the replay by recorded size | named data, the replay test read by day size (K1): 0.940, 0.507, 0.398, 0.599 and 0.404 log points, and 0.243 to 0.465 across the cuts at 2 to 30 strokes, against 0.044 |
| SF16 | the day sizes in the replay | unfolded to convergence; in one step from the well-covered days' own mix; level by level; coarser or finer classes | to convergence, levels together | same call, every one inside the bands (one step misses the replay test by 0.095) |
| SF17 | the ground strokes of a season | the located count over the fitted law's share at the day's level; each located stroke weighted by one over its own filed chance | over the law's share | named data: on the well-covered days thinned to two and three sensors the law's share recovers 1.01 and 1.00 of the count, the capped weights 0.92 and 0.95 |
| SF18 | the peak-current law | by polarity; one law; from days with two, three, four or six standard sensors | by polarity, three or more | same call, inside the bands |
| SF19 | the days that stand for what fell | six or more standard sensors up; seven or more | six or more | same call, inside the bands |
| SF20 | a leap day | in the window's record like any day; left out | like any day (the window of 2026-27 has none) | same call: no storm day on record falls on 29 February and the exposure moves by under one part in a hundred |
| SF21 | a station's break-even season | 25 hours over its average-season hours, as a per cent; the shelf index value at which its expectation meets 25 hours | 25 hours over the average-season hours | the prompt's words (how strong a season, as a per cent of an average one); the index reading needs a form for the response beyond the index's record (Callory Downs' answer would sit under the lowest index value on record, where a constant per cent and a straight line part ways) and is not asked |
| SF22 | a season's strength at a station | one regional per cent, the same at every station; the station's own | one regional per cent | the bulletin (one index for the northern shelf) and SF12: same call with each station's own |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| the clearance timer | 15 minutes after the last stroke | `ramp_lightning_standard_GS14.pdf`, clause 3.2 |
| the radius | 8 km of the station's reference point | `ramp_lightning_standard_GS14.pdf`, clause 3.1; `stations.csv` for the points |
| the window and the line | 1 December to 31 March; over 25 hours | `wet_season_resourcing_procedure.pdf`, section 2 |
| an average season | the mean of the seasons on record, 2002-03 to 2025-26 | `wet_season_resourcing_procedure.pdf`, section 2, and the prompt |
| the 50 per cent current by sensors up | 26, 19, 13, 9, 6.5, 4.8 and 3.5 kA at two to eight sensors | `aln_detection_performance_sheet.pdf`, the table |
| the curve's width | 0.35 in the natural log of peak current (a logistic) | `aln_detection_performance_sheet.pdf`, the note under the table |
| sensors needed for a location | two, of either type | `aln_data_notes.txt` |
| a sensor's range | the distance the sheet states, with each sensor's position | `aln_detection_performance_sheet.pdf` and `aln_sensor_register.csv` |
| the outlook value and the index's seasons | +0.5; 24 seasonal values | `seasonal_outlook_2026_27.pdf` and `nsi_seasonal_history.csv` |
| the curve between and below whole sensor counts | the table read on a straight line in the log of the 50 per cent current, carried below two sensors at its first step | measured: the per-pairing fit (a level of its own for each pairing of sensors up) frees it, and its spread is inside every band |
| a legacy receiver's worth | 0.32 of a standard sensor | measured from the pack: the family's spread is 0.32 to 0.36 across the battery, and the call holds from about 0.15 to 0.46 |
| the peak-current law | a lognormal by polarity through the filed curve | measured from the pack: the family's spread across one or two laws and four sets of days is inside every band |
| the strong-stroke level | 60 kA | measured: 50 and 75 kA are in the battery, the season's percentage 107.8 and 108.4, the spread inside its band |
| the response's form | a constant per cent per index unit | measured: a straight line on the strong strokes and one on the corrected hours are in the battery, the season's percentage 109.9 and 109.0, the spread inside its band |
| the days that stand for what fell | six or more standard sensors up | measured: seven or more is in the battery, its spread inside every band |
| the day-size classes | 1, 2, 3, 4 to 5, 6 to 9, 10 to 19, 20 to 39, 40 or more located strokes | measured: coarser and finer classes are in the battery, their spread inside every band |
| the replay's draws | six thinnings a level, a fixed seed | measured: two other seeds and twelve thinnings are in the battery, their spread inside every band |

Variant battery: 27 variants of the golden's conventions in `generator/core.py` (every row above marked measured, the legacy worth from three sets of stations, per pairing and from the count of strong strokes, the unfolding four ways, the state nine other ways), and every variant files the same call: crews at Callory Downs, Penrow Sound, Mornay Inlet and Weymoor Gap. Every graded figure's band is the battery's span with room. The build re-runs the battery on the cut pack and extends it to the full cross.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the seven stations of the station register; every cloud-to-ground stroke within 8 km of a station's reference point, located or not; every wet season day |
| 2 | Unit of account: hours of stand-down in a season; ground strokes in a season; per cent of an average season (this season's strength and each station's break-even) |
| 3 | Attribution window: a stroke opens 15 minutes from its own time; a stand-down belongs to the season its strokes fall in |
| 4 | As-of dating: the archive and the sensor log close on 31 March 2026; the window is 1 December 2026 to 31 March 2027; the outlook is the bureau's November 2026 bulletin |
| 5 | Version basis: the standard as it takes effect on 1 December 2026; the latest solution of each archive event; the sensor register's current identifiers with the former ones beside them |
| 6 | Denominator: the 24 seasons on record, each season's days on which a location was possible |
| 7 | Weighting: every season counts once in an average season; no stroke or day is weighted beyond its own correction |
| 8 | Window length: 1 December to 31 March (121 days in the window); 15 minutes; 8 km |
| 9 | Boundary inclusivity: a stroke at exactly 8.0 km counts; a crew is added strictly over 25 hours |
| 10 | Rounding path: full precision to the end; hours stated to one decimal, strokes to the whole stroke, the percentage and the break-even seasons to the whole per cent, each with its band in the answer blocks |
| 11 | Tie-break: none needed; the nearest any variant comes to the line is 1.4 hours (Mornay Inlet at 26.4) |
| 12 | Maturity and censoring: every season on record is complete; strokes under the network's reach are missing by the filed chance, never by a cut-off date |
| 13 | Order of operations: the versions and the ring, the local day, the sensors up, the law, the legacy worth, the replay and the unfolding, the season tables, the response, the window, the line |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: a re-sent batch counted once by event id; a reprocessed solution replaces the earlier one |
| 16 | Identity normalisation: one station code across the extract, the log and the registers; a sensor's former identifier mapped to its current one by the register |
| 17 | Netting against gross: cloud pulses and strokes outside the ring left out; nothing else netted |
| 18 | Dimensional units: kA (signed by polarity, the law on the magnitude); km from the reference point on the sphere; minutes and hours; the archive in UTC and the log by local day |
| 19 | Code and status semantics: the archive's type field (ground stroke, cloud pulse); the status log's up and down; the register's sensor type (standard, legacy receiver) |
| 20 | Integerisation: strokes are whole; no season figure is rounded before the line |
| 21 | Clause scope: the standard applies to every ramp the handler works; the procedure's line to every station in the register |
| 22 | Forward window contents: the wet season of 2026-27 at the bureau's outlook value of +0.5; the standard and the on-site detectors in force from its first day; no change of stations |

## Literal reader

The standard's clauses 3.1 to 3.3 and the procedure's section 2, executed word for word on the golden's season tables, file the golden: each station's stand-down in a season is the union of the 15 minute intervals after every cloud-to-ground stroke within 8 km of its reference point; an average season is the mean of the 24 seasons on record; the expectation for 1 December 2026 to 31 March 2027 is taken at the bureau's outlook value; a relief crew is added where it is over 25 hours. The prompt's sentences read literally land on the same figures: "the stand-down hours to expect this season" is the window's expectation (52.9, 28.3, 28.1, 28.6, 15.0, 21.9, 21.6); "the hours and the cloud-to-ground strokes within 8 km that an average wet season on the 2002-03 to 2025-26 record would bring under the standard" are the season tables' means (strokes that fell, not strokes located: the standard's detector registers every one); "how strong a season, as a per cent of an average one, would put the station's stand-down at 25 hours" is 25 hours over the station's average-season hours, as a per cent (51, 95, 96, 94, 180, 123, 125); "what this season is as a per cent of an average one" is the window's expectation over an average season's, 108, one figure for the region. No filed sentence says how the hours or the strokes that fell are to be recovered from the archive: that is the work, and the data force it (`## Semantic fork table`, SF14, SF15 and SF17).

## Prompt contract

A rewrite keeps: the reason the call rests on an estimate (the standard starts on 1 December and no station has logged a stand-down under it); the question in the which form; the window of 1 December 2026 to 31 March 2027 and the line of over 25 hours; a committed figure for every station on each of the four quantities (this season's hours; an average season's hours; an average season's cloud-to-ground strokes within 8 km; how strong a season, as a per cent of an average one, puts the stand-down at 25 hours) and this season as a per cent of an average one; "an average wet season on the 2002-03 to 2025-26 record" and "under the standard"; the CSV and the workbook with its chart against the line. A rewrite never adds: a method, a correction, the words detection, efficiency, missed, located, sensor, legacy, replay or simulate; a file name; a count of stations, seasons or strokes; a rounding; a role or a reader; a warning. The draft passes `voice-check.py` with no WARN at 901 characters.

## Build brief

World: Kestrel Coast Ground Handling works the ramp at seven regional airports of the Northern Territory's Top End and Gulf country: Callory Downs (the inland hub), Penrow Sound, Mornay Inlet, Weymoor Gap, Yanda Creek, Tarrick Tableland and Burrel Bay (core.py's A, Z, X, V, Y, W, B, in that order). Ramp Lightning Standard GS-14 takes effect on 1 December 2026: each station's new on-site detector registers every cloud-to-ground stroke within 8 km of the reference point, the ramp stops at the first and resumes 15 minutes after the last. The handler's wet season resourcing procedure adds a relief ramp crew wherever the expected stand-down for 1 December to 31 March is over 25 hours. The only history is the Austral Lightning Network's archive for the wet seasons 2002-03 to 2025-26: the network locates a stroke with a chance that rises with its peak current and with the sensors in range and up that day (the vendor's sheet), it was thin until its 2010 and 2018 upgrades (core.py's three eras, eight seasons each), and at five stations it leaned on legacy receivers kept from the 1990s network (two of them, Weymoor Gap and Burrel Bay, still do). The bureau's Northern Shelf Index has one value a season and an outlook of +0.5 for 2026-27. The generator wraps `generator/core.py`: `build()` is the world (every ground stroke, whether located, each station-day's sensors up) and `records()` is what the files hold, re-indexed to the station-days that hold a located stroke (a storm day that left none is in no file, and no estimator in core.py sees one); nothing in the pack may come from any other draw.
Frozen: everything in core.py: the seed (3909); the sites table (storm days a neutral season, the median day size, the standard sensors and legacy receivers in range by era); the timer, the line (25 hours) and the outlook value (+0.5); the index's 24 values; the vendor's table and width; the legacy worth, the outage chance, the response, the stray share, the phase effect and the season noise of the world; the golden estimator (`estimate`), its 27 battery variants, the lattice, every other route, the run routes' further settings (`CUTS`, the donor choices, `route_sizemix`, `tail_worth`), the two over-corrections and the worth sweep, and the falsification statistics, K1 read by day size in `SIZES`, (the replay test's folds are the odd and the even days of each season); every figure of `## Stump core`. The careful but hurried pass of `effort.json` is the reflex route (`estimate` with `s1=False, s3=False`), the quick pass `route_direct`, the thorough pass the golden; the careful losses cite L56, N21 and L57 (R4), N42 and L58 (R3), L28 (R5) and L63 (R7, R8). On the cut pack `effort.py` re-prices the run routes' further settings and reports the dearest per sentence and per figure beside the two stumps lost alone. A gate that cannot pass inside them goes back to the architect.
Files: every file is written from `build()` and core.py's constants, and the build asserts that reading the cut files back gives `records(build())`: the same located strokes on the same station-days with the same sensors up. A stroke's date is its season's 1 December plus `d_dos` days (29 February skipped: no storm falls on one) and its time of day is `t`, the local minute; local time is UTC+9:30 all year, and the extract's stamp is that moment in UTC. At this seed every stroke falls between 05:33 and 21:14 local time, so none is within 15 minutes of a local midnight. (1) `aln_strokes_station_extract.csv` (the network operator's query tool, a 16 km square about each reference point; one row per located event solution: event id, solution version, UTC time to the millisecond, latitude, longitude, signed peak current in kA to one decimal, type; 20,000 rows or more). The 27,002 located ground strokes sit inside each station's 8 km ring at positions the build draws evenly over the ring. Texture, all of it drawn from a stream of the build's own so that core.py's is untouched: corner events between the ring and the square's edge on core's storm days (a Poisson number with mean 0.27 times the day's ground strokes; each copies the minute, within two minutes, the polarity and the peak current, within a few per cent, of a ground stroke of the same day drawn at random, located or not, and is located by `de` at that day's level under the same two-sensor rule); cloud pulses, always typed as cloud pulses; superseded solutions (the latest version is core's stroke; an earlier one differs by under a kilometre and a few per cent); re-sent batches that repeat event ids. It must not carry: the sensors that took part in a solution or their number, an error ellipse or a quality figure of any kind, any detection chance, any stroke the network did not locate, any distance or in-ring flag. (2) `aln_sensor_status.csv` (the network's daily status roll, one row per sensor and local day: up or down; the second large file, well over twenty printed pages) and `aln_sensor_register.csv` (identifier, former identifier, type as standard or legacy receiver, position, commissioned and withdrawn dates; the 2010 and 2018 upgrades fall between the eighth and ninth and the sixteenth and seventeenth seasons). Each station's sensors are its own (no sensor is in range of two stations); the sensors in range by era are the sites table's; each station-day's counts of standard sensors and legacy receivers up equal core.py's `cal_std` and `cal_leg` exactly, and which sensors are down that day is the build's draw. On a 29 February every sensor in range is up. They must not carry: a range per sensor type, a sensitivity, gain, baseline or equivalence figure for any sensor type, a note on what the legacy receivers contribute or why they were withdrawn. (3) `aln_data_notes.txt` (the operator's notes sent with an extract: the fields of the extract and of the roll; the extract's time is UTC and the roll's day is the local date; a reprocessed solution carries a higher version and replaces the earlier one; the type codes; a solution is issued when two or more of the network's sensors, of either type, report the stroke). Fields only: no sentence on performance, coverage or completeness. (4) `aln_detection_performance_sheet.pdf` (the vendor's sheet for the standard sensor, issued with the 2010 upgrade: the 50 per cent peak current at two to eight sensors in range and up, 26, 19, 13, 9, 6.5, 4.8 and 3.5 kA; the curve a logistic of width 0.35 in the natural log of peak current; the distance within which a sensor counts as in range). It is silent on legacy receivers, on fewer than two sensors and on anything but single strokes. (5) `ramp_lightning_standard_GS14.pdf` (clauses 3.1 to 3.3 as in `## Deep reasoning`, Estimand; the detector's acceptance figure stated as registering every ground stroke inside the radius) and `wet_season_resourcing_procedure.pdf` (section 2: the window, all hours of the day, the line, the expectation at the bureau's outlook value, an average season as the mean of the seasons on record). Neither states a figure for any station. (6) `stations.csv` (code, name, reference point, the date the detector was commissioned, all in November 2026). (7) `nsi_seasonal_history.csv` (the index's 24 seasonal values) and `seasonal_outlook_2026_27.pdf` (the bureau's bulletin: one outlook value of +0.5 with no range, the index described as one value for the northern shelf with the northern stations' storm activity moving with it together; no coefficient, no count of storms or thunder days). (8) Two or more unused files that look relevant and record no storm, stroke or stoppage: the summer flight schedule by station, the ramp roster and pay scales, the ground equipment register. Never labelled as unused. No file of any kind observes a storm outside the archive: no thunder-day book, no delay codes, no incident log, no pilot or tower report, no detector trial, no second network, no satellite product, no rainfall.
Never filed: any sentence, column, label or file name that says or implies: what a legacy receiver is worth or that it is less sensitive than a standard sensor; that recorded stand-down hours or durations depend on detection, or how; that small storms or storm days are missed; that the strong strokes are located by every network; that the archive's early seasons under-count; a detection efficiency by station, season or era; a corrected or adjusted count or hour; the words replay, thinning, unfold, donor, legacy worth, equivalent sensors; the 60 kA level; a response of storms to the index as a number. The stations are never ranked on anything.
Goldens: `relief_crews_2026_27.csv` (one row per station: the crew call, this season's expected stand-down hours, an average season's hours, an average season's cloud-to-ground strokes within 8 km, the season as a per cent of an average one at which the stand-down meets 25 hours) and `relief_crews_2026_27.xlsx` (first sheet: the call, naming the located strokes' route it rejects and the four crews; a chart of each station's expected hours against the 25 hour line; the season as a per cent of an average one; a sheet for the legacy receiver's worth and the peak-current law; a sheet for the replay test with every rival route's miss; a routes sheet with the lattice). Every figure from `generator/figures.json`, which the build computes from the cut files with core.py's `estimate` and which agrees with `## Stump core` inside each band (the one decimal of the peak currents and the leap days' rows move a figure in its fourth digit). On the cut pack the build re-runs the battery and adds three variants, reporting to the architect if one leaves a band: the peak-current law fitted on every ground stroke of the extract, corners included; each fitted input moved by 20 per cent; the full cross of the battery's conventions. The answer blocks: Critical Components are the two decisive answers and nothing else (Penrow Sound's average-season hours; Weymoor Gap's average-season ground strokes), each as a figure with its unit and band and no method; the Supplementary Questions are three entries (this season's hours, in three lines; an average season's hours and strokes, in three lines; the season's percentage and the break-even seasons, in two lines), the lines grouped as core.py's sentences; the counts and bases every route reaches (located strokes, storm days with a located stroke, days with no location possible, the well-covered days) go to the Step-by-Step alone.
Free: the stations' coordinates and the sensors' positions (any layout that gives each station its own sensors and core.py's counts by era); the strokes' positions inside each ring; the texture events' volume beyond the corner rule; the documents' genre, numbering and look; the distractors' content; Layer 1 detail beyond the list in `## Deep reasoning`; nouns beyond the people and the names above.

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
- Architecture 8 (the SP 141's gully crossings), landed by both platform runs on 2026-11-21 (runs/arch8/): all seven classes filed by both. Each stump shipped a file that scores it: the storage gauge's account closed the bucket's loss (R98), the radar's pixel pairs read each source's ratio off (R99), the research valley's weighing gauges calibrated hail and then the whole chain end to end with the residual integrated (R100, R101). Every open member sat 1.1 to 1.5 storms above its line with every priced shortcut under it, so the runs' generous corrections were never punished; the critical components were never asked for in the prompt; the estimand was the record's own 18-season mean, so the programme window did no work. The precedents cited (N21, N26, N01, N30) were waved through by runs with no file to check them, so they never transferred. Dead: the world, the stumps and the shell.

Architecture 9 (Kestrel Coast's relief ramp crews), at the draw (2026-11-21):
- Worlds screened on paper before this one: sheltering growing around airport anemometers (the closed card of a
  change of instrument, found by wind sector); a crane wind alarm's setpoint change restated across its log (the
  closed card of old figures restated to the target basis); heat with era dummies or an urban dose response and
  frost with phenology and chill hours (the closed card of extrapolation past the observed range, and the field's
  textbook chain once the station records ship); a time-of-observation replay (the field's textbook homogenisation,
  a reflex); storm outages in a station record filled from neighbours (a reflex); a top-k call in place of a line
  (corelib skips the both-sides check on a ranked pick).
- The lightning world as architecture 8's draw rejected it (a response of the world read through a densifying
  network, two closed cards): answered, not reversed. This core takes the same instrument and decides on its
  observation process (what a timer would have run on the strokes it missed, what an unfiled receiver adds); the
  state's response is kept as a supporting step only.
- A cloud-pulse stump (pulses logged as weak ground strokes, more of them the more sensors are up, taken out by a
  two-population mixture on peak current and polarity): the golden filed 131, 78, 89, 40, 40, 19 and 23 hours
  against a truth of 84, 53, 52, 31, 31, 15 and 20, the mixture's errors and the replay's compounding. Dropped; the
  third judgment became the legacy receiver's worth.
- A three-stump core (CORE PASS level 5 on corelib, at a line of 40 hours and then 30) with the forward state as
  stump S2: the region's response to the shelf index, masked in recorded hours because the warm seasons fell under
  the thin early network, its component the season as a per cent of an average one. Given up when its own routes
  were priced: its remedy is the fix two closed cards already use (the series rebuilt on the signal a change of
  instrument could not move, beside a co-occurring change), and the rigorous standard route (a level per sensor
  configuration with one pooled response) landed its component inside the band (135 against 134.3 to 148.1). It is
  a supporting step now, at a response and an outlook the index's record supports (the season 108 per cent of an
  average one): left out alone it leaves the call standing and earns 67. The id S2 is not reused.
- A response of its own for each station, one of them negative, as S2's member: twenty four seasons cannot hold
  seven responses apart (the golden was noise), and a plain regression on the index gets a negative station right.
- The state fully masked by era, so that every regression with era levels failed: it cannot coexist with a golden
  that identifies the response robustly. And an index varied inside each era with mixed signs: the record's mean
  then fails its own hold-out and every regression route earns the step.
- A panel regression of recorded hours with a free elasticity to the located share as the rigorous standard route:
  unidentified (plus or minus 1.1 on the elasticity). The rigorous route is the level per sensor configuration.
- A state that also changes the day-size mix, so the recorded response differs from the true one: the season's
  percentage then depended on S1's unfolding and the components were no longer independent.
- A member opened by S1 alone far above the line (58 hours): the route that puts the missed strokes back lands at
  75 to 80 per cent of the golden, so no member sits under the line on that route while the other drops hold over.
- The contrast of corrected hours between the network's eras as a third falsification statistic: it cancels where
  the thin era and the warm seasons coincide.
- An uncapped inverse-chance weight and a trend carried to the end of the record as the generous route: weaker than
  a strong run would build. The generous route is the fitted law with each day's strokes and hours raised by one
  over the filed share located.
- A forward change of the network (sensors commissioned for the window) as what moves the window: the closed card
  of a projection that holds fixed what the change moves, beside the restated-basis card; and the estimand is what
  falls, which no network changes.
- The outage-day contrast (recorded hours on days a sensor was down against the days all were up) as the first
  falsification statistic: its sampling error is about 0.07 log points, and under two of three other seeds a fitted
  rival came within three times the golden's score. Replaced by the replay test on the well-covered days (the same
  days thinned and corrected, 0.014 for the golden against 0.22 to 0.76); the contrast is printed beside the score.
- A line of 24 hours: one share of hours kept at each sensor count, read off the well-covered days with the legacy
  worth fitted (a strong run's flat calibration), put Penrow Sound and Mornay Inlet 1.7 per cent under it. The line
  is 25 (that route 21.9 at both, 12 per cent under).
- The replay's day sizes taken in one step from the well-covered days' own mix, priced as a rival: it lands 0.96 to
  0.98 of the golden at the three open stations, so it is a member of the golden's family (in the battery, inside
  every band) and never a shortcut.
- The replay test's folds on the storm days' running number, and the estimators run on records that still listed
  the storm days with no located stroke: neither is in any file. The records are now the station-days that hold a
  located stroke and the folds the odd and even days of each season; the golden did not move and the core passes.
- A third stump in this world, for level 5: the location error trading strokes across the 8 km ring (no bias under
  a locally even stroke density, nothing to price); the days fewer than two sensors were up (the closed card of
  groups recorded less completely, a gross-up every route makes); a hand-kept thunder-day book (a calibration set
  for the missed days). None is open, so the core is level 4 on two stumps.
- The shelf index value at which each station's answer changes as the third ask: a straight line in the index and a
  constant per cent per index unit part company beyond the index's record (Callory Downs -0.89 against -1.26, Yanda
  Creek 2.11 against 1.68), no data on 24 seasons rule between them, and the bands that held both swallowed the
  stumps at three stations. The ask is the season, as a per cent of an average one, that puts a station at the
  line: it needs no form and never leaves the record. The straight lines joined the battery (the season's
  percentage 106.7 to 111.6).
- More room for the supporting step, by placing the three near-line stations higher (Penrow Sound, Mornay Inlet
  and Weymoor Gap at 39.5, 41.5 and 43.0 storm days in a neutral season, and seven other placements): the step
  left out then keeps 5.3 per cent in the battery's lowest variant, but a run's outage-day elasticity files Penrow
  Sound and Mornay Inlet over the line (26.6 and 26.2 hours), an easier route on S1's own member. A near-line
  station's hours move about 8 per cent from draw to draw, wider than the gap between the two pressures, so the
  stations stay at 37, 41 and 41, where every rival sits 12 per cent or more under the line at Penrow Sound and
  Mornay Inlet and the step left out keeps Penrow Sound 5.0 per cent over it (1.2 per cent in the lowest variant).
  core.py asserts that at the frozen seed; it fails at the four other seeds tried.
- S3 one-sided, at this architecture's first handed-back core: with Burrel Bay a plain three-sensor station no
  member crossed the line when the legacy receivers were over-discounted. A receiver worth nothing, or anything
  under about 0.45, filed the golden's call (Weymoor Gap 39.5 to 26.8), so a run that set the receivers aside
  landed the call and only Weymoor Gap's own figures punished a bad worth. Returned at review. Burrel Bay is
  re-placed as a legacy-heavy station under the line (one or two standard sensors and four or five receivers, as
  at Weymoor Gap), which a worth under about 0.15 takes over it.
- The cut-off family at the first placements: a calibration on the well-covered days of at most k located
  strokes, with the legacy worth fitted, filed the golden's call at k of 5 to 12 (Penrow Sound 25.8 at 5),
  because no member answered to mid cuts: Tarrick Tableland crossed only at 4 or fewer and Penrow Sound and
  Mornay Inlet only at 12 or more. The route first priced as the cut-off (present-network seasons and warm
  analogues) was not the cut a run puts in place of the replay's fit. Closed by re-placing Mornay Inlet as a
  station of very small storm days (a median of 1.5 strokes, three sensors throughout) and Tarrick Tableland
  nearer the line (21.9 hours), so every cut from 2 to 30 leaves one of them 1.6 hours or more on the wrong
  side.
- A station of very large storm days (a median of 40 strokes) as the member the small cuts over-correct: the
  golden under-reads its realised hours by 9 to 12 per cent while one share of hours is nearly right there, and
  its expected hours had to sit over the line for the golden to sit near it. Dropped for a median of 18.
- Burrel Bay as a legacy-heavy station at 24.5 to 26 storm days in a neutral season: the golden at 24.2 to 24.6
  hours, a battery variant over the line and the world's own expectation over 25. Placed at 23.5 (the world's
  expectation 24.2, the golden 21.6, the battery's top 22.0). Larger storm days there (a median of 8 to 14
  strokes) were tried to make the mid cuts dearer per figure and moved nothing (66 to 71).
- The assertion that the record's mean route keeps the call under every battery variant: it forced the over-line
  stations to 28 hours and more, where no mid cut reaches them. Replaced by what the closed-lesson rule asks:
  the supporting step left out alone is the response read on the corrected hours (a battery variant, the
  golden's call), and the record's mean route, which leaves a filed sentence unexecuted, is printed with its
  room (4.0 per cent at the golden's conventions; Mornay Inlet 2.1 per cent under the line in the battery's
  lowest variant).
- K1 as first written (the replay test read on the well-covered days of fewer than six strokes): a share
  calibrated on a cut of those days passes it by construction, so it could not rule on the cut-off family. K1 is
  now the replay test read by the day's size in four classes, the largest miss (the golden 0.044, every
  one-share route 0.243 or more), and the cuts are scored as rivals.
- Placements that pass at several seeds: tried and not found. Of seeds 3909 to 3913 only 3909 passes: a
  station's 24-season record moves its figure about 2 hours from draw to draw and the cut-off family is closed
  only by stations within about 3 hours of the line on both sides, so the two pull against each other. The seed
  stays frozen and the margins that are thin at it are listed under Forcing.
- The mid cuts on the per-figure grain: a calibration cut at five to seven located strokes with the legacy worth
  fitted files the wrong call and earns 42 per sentence, but 60 to 71 per figure, because it sits inside the
  stretched bands at five of the seven stations. Spreading the stations' day sizes further (so one cut serves
  fewer of them) would lower it and means re-placing Penrow Sound or Weymoor Gap, the two open members; not done
  in this pass and reported to the build.
- A third stump was not added: the screen's dropped candidates fail tests that do not depend on the placements
  (closed cards, a reflex once the field ships, a calibration set), so level 4 stands.
- The well-covered days as S1's ground (measured by the build after the second hand-over): a calibration cut
  chosen station by station (the cut whose thinned days match the station's recorded size mix, or three times
  its recorded median day) files the golden's call at 24 of 27 settings. With the vendor's curve filed, the
  well-covered days are a calibration set, and the unfold differs from a matched ratio in precision, not in
  what identifies it. S1 on those days is closed.
- S1 with no well-covered day (no station above three standard sensors; the storm process fitted to the thin
  records at every sensor level by simulated minimum distance, then run at full sight): determinate (0.91 to
  1.07 of the true hours at the world's own family over three seeds; seven rival families, all passing the
  fit's own statistic, within 6 to 13 per cent of each other at a station) and not live. A station's own
  located strokes thinned by the filed curve to lower levels, log hours on log share located, carried to share
  1, lands within 0.90 to 1.16 at every station and files the golden's call at 11 of 12 settings over three
  seeds (the straight-line form files two crews too many, the saturating form too few). The hidden curve of
  hours on share located has a near-constant elasticity (0.65 to 0.76 from one sensor to eight), so the call
  turns on the regression's form and nothing in the pack rules on it.
- The same with flash structure added to the storm process (each negative flash's later strokes within a
  second, weaker and tied to the first, at every station): the storm fit stays determinate (0.95 to 1.08 over
  three seeds; eight families within 4 to 11 per cent, two more refuted by the fit's statistic at 513 and 690
  against 366 on 395 statistics), and the ladders on the share of strokes now file wrong (1.06 to 1.56 on a log
  scale, 1.57 to 2.16 on a straight line). The ladder scaled by the textbook flash formula (one minus the
  share of strokes missed, to the power of the strokes a flash) files the golden's call at 7 of 16 settings (a
  log scale with two or three strokes a flash, on both seeds tried). Its natural settings miss by about 10 per
  cent either side, which is one family's spread and not three.
- What the three share, kept as the rule for the redraw: the hours a full network would log are the smooth
  limit of what the thin record shows at successive depths, so a one-line extrapolation shares the fitted
  estimator's accuracy whatever the storm process. A parameter of the recording system (what a legacy receiver
  adds) is no such limit, which is why S3 holds. The second decisive step has to come from another record;
  architecture 9's core is not built from as it stands.
- Architecture 9's lightning world retired with it (one architecture per world): no second system there passes the
  three tests, since a second network or an on-site counter is a collocated pair (and capture-recapture a closed
  card) and old-procedure stoppage logs are a calibration set.
- Architecture 10's first screen (eight sprayed-seal haul districts, heavy vehicles restricted while air and
  pavement both run hot on the new standard sensors) died on paper on 2026-11-21: the shield's solar gain is the
  calibrated-source card's trap word for word (an instrument biased against the truth and used at face value, the
  bias varying by group), however the gain is estimated, and the instrument-change card's own example is a
  weather station's summer highs; only the puck's depth (a conduction filter to invert) was open ground, and a
  frame with the history on one sensor basis and the rule on another hands every run both recognitions in the
  prompt, so the two were never independent.
- Architecture 10's second screen (kinds chosen before any world, 2026-11-21) found no pair: twelve candidates in
  seven worlds (vineyard bud kill, city snow disposal, an avalanche corridor, forest windthrow, rime ice on masts, a
  port gust archive, field camps) each died on a closed card, an end-to-end calibration or a textbook chain. Where the
  target has a history on file a run calibrates on it end to end; where it has none its scale comes from a
  conversion factor (the calibrated-source card, with boundary days as checked cases) or a published model; the
  forward-process kinds are algebra once their inputs ship and rest on the first step's state when they do not; and
  sources part by part come down to a completeness gross-up. The bud hardiness state was the one candidate off every
  card, and it stood alone. The slot is handed to the author with retirement recommended.
