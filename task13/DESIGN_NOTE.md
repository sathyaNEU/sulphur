# task13: the co-op's 2027 lightning protection refit and the referral rule behind it

## Draw

Subdomain: Energy Systems & Utilities, task type grid reliability and outage analysis (`grid-reliability-outage-analysis`, the only energy task type serving the assigned analysis type)
Analysis type: Anomaly Detection & Diagnostics
Answer shape: a monitoring rule with its expected alert count (the rule, the zones it refers now, its referrals after each season since 2022 and the sound zones a season's referrals should hold, checked against the cyclic inspections), with the refit on top
Weight: metric or rule design: most of the work is building the referral signal itself (lightning faults reconstructed on each device's own clock and memory, an expectation in which every zone keeps a level of its own learned only from inspection-confirmed seasons, a threshold carried on that two-level scatter); the last three builds sat on assembly (task14), a hard-to-measure quantity (task3) and validation (task10)
Data-native sentence: a lightning fault exists only as a coincidence between two clocks (a recloser's own record of a trip and a lightning network's record of a stroke near the line), and what a zone's lines give with sound protection is partly the zone's own (the soil its grounds are driven into, its hardware and route), so the referral must judge each zone against the seasons a later inspection confirmed it sound, and a scatter taken season by season refers the zones that always run high.
People: Lucas Ramirez (technical services manager, takes the refit to the management committee), Donna Rodriguez (reliability and protection engineer, the golden's author), Laurie Diaz (line inspection supervisor), Elizabeth Hernandez (general manager, issues the programme terms), John Fuentes (SCADA supervisor), Michelle Garcia (materials and warehouse); drawn with `guard.py names --geo Philippines` at seeds 1302, 1307 and 1311

**The decision.** Kalumpang Valley Electric Cooperative, a member-owned distribution co-op in Central Luzon, runs 13.2 kV
overhead lines from its substations, cut into protection zones by substation breakers and line reclosers. Lightning is
its largest cause of trips. Its 2015-2016 line arrester programme fitted arresters along the exposed lines; since then
ground leads have been stolen for their copper, a contract lot of line arresters has started failing and a batch of
porcelain pin insulators has been cracking. A cyclic line inspection reaches every zone once in five dry seasons, and
the co-op keeps ten years of SCADA history, recloser downloads and lightning records. The board's 2027 budget funds a
dry-season refit (grounds, arresters and insulators restored) on the zones a referral rule names before the 2027
lightning season, and the co-op will run the same rule after every season from now on.

**Card.** `.claude/skills/fingerprint/cards/task13.json`, architecture v3, re-registered 2026-11-11, guard verdict WARN.
Answered: `overuse.forum` (the management committee approves the dry-season work programme inside the board's budget,
the honest forum for a refit list); `repeat.gate_g` against task15 (there a growth gap split across drivers; here each
zone's excess assigned to failed protection only beyond the level the zone keeps when sound); `repeat.question_form`
(the decision is a rule, so the question asks what it is); `repeat.decision` against task15 (there a set of drivers
named once; here a set of zones named by a rule the co-op reruns after every season, so the rule's alert load and its
check are graded beside the set). Architecture 3 keeps architecture 2's world and replaces its
three difficulties after the stage 4 judge's first pass landed them; its revision of 2026-11-11 replaces the two that
architecture 3's own judge landed (the refit's valuation filed as a method, the budget read as the rule's rate) with the
state each failure had reached and the uncertainty of each zone's level (`## Tried and rejected`).

## Deep reasoning

Task type: Grid reliability & outage analysis (the energy subdomain's task type that serves Anomaly Detection &
  Diagnostics: a referral rule over a network's protection zones, with its alert load and its check)
Domain test: every result is a quantity a distribution reliability engineer computes from protection and lightning
  records: lightning faults attributed by coincidence between a protective device's operations and the strokes the
  lightning location network placed near its lines, each device on its own clock; what a line with sound grounds,
  arresters and insulators gives under that lightning, which depends on the line's construction and also on its own
  site (earth resistance, hardware, route), a level learned from the seasons an inspection confirmed sound; a threshold
  carried on that two-level scatter at a stated budget of sound zones referred; the alert load, the check against
  cyclic line inspections, and the faults a protection refit removes. The field's analyst builds the fault record,
  learns each line's sound performance, sets the alarm and proves it against the line crews' findings.
Swap: "what rule refers the units whose protection has failed" still parses with a hospital's or a fleet's nouns,
  but trips lined up with located strokes on each controller's drifting clock, memories that overwrite their oldest
  events, the lightning that fell within reach of a line, a line's own earth and route and a line inspection that
  verifies the seasons before it all stop meaning anything: the results are this protection system's.
Where the weight sits: designing the referral signal itself. The fault record (R1) is rebuilt from two clocks and
  from memories that overwrite; the sound expectation carries every zone's own level, learned from its 779
  inspection-confirmed zone-seasons, which spread with a coefficient of variation of 0.42 while a zone moves from
  season to season hardly beyond Poisson (R4, R2); the threshold carries that level's uncertainty, not its estimate
  (R3), and the alert load (R5) and the inspection check (R6) follow from the two-level design; the refit's value (R7)
  rests on the state each failure had reached by the end of 2026, which the record since inspection does not show
  when averaged.
Layer 1: the SCADA history carries the breakers and the radio reclosers with upstream breakers tripping on downstream
  faults and comms-fail gaps; the downloads re-read each whole memory at every visit on the controller's own clock in
  day-first format, the weekly battery test logged at 03:00 by that clock; the lightning extract is in UTC with cloud
  pulses and weak positive discharges mixed in while every co-op system keeps Philippine time; the OMS codes each
  outage's cause by the dispatcher's word; the register names zones in two shapes and three telemetry labels; the
  inspection book counts findings per zone and round; the transformer book counts replacements. None decides a result:
  checks.py moves no referral when the re-reads are counted twice or the weak discharges left out.
Not one thing: four judgments carry the chain beyond the reconstruction, each in different results, each with its
  own wrong answer: each zone's own sound level (R4 and R2; without it a scatter taken season by season refers 13),
  that level carried with its uncertainty into the tail (R3, R5, R6; taken as known it refers 17 and would refer a
  sound zone 1.2 times a season against the budget's 0.2), the state each failure had reached by the end of 2026 (R7;
  the record since inspection averaged gives 72 against 116, because in the first season after inspection 9 of the 11
  referred zones ran at under half the multiple of their own sound level they reached in 2026), and the reconstruction
  itself (R1), which the stage 4 judge of
  architecture 2 made unprompted and is priced as earned even though architecture 3's judge did not restore it.
One-fact test: "a zone that runs high when its protection is sound runs high every season: judge each zone against
  its own confirmed-sound seasons", executed the way a run acts on it (each zone's level estimated from its confirmed
  seasons and taken as known), rescues R2 and R4 (2 of 7) and refers 17 zones; "a zone's own level is only as certain
  as its few confirmed seasons make it" rescues nothing on its own; "most referred zones failed partway through their
  record since inspection" rescues R7 (1 of 7); the clocks-and-memories sentence rescues nothing from the measured
  careful pass, which already rebuilds the record. The sentence that names the whole method (each zone's own level,
  carried uncertain into a predictive tail) would also rescue R3, R5 and R6: that is the method itself, a legitimate
  choice the data force (2 dlogL 165.6 for the levels, terms 3(b) for their uncertainty), not a hidden fact
  (`stumping` 2.3), and the chain is built around it: R1, R7 and R2 stand on other judgments.
Not semantics: every column and clause read correctly (the controller time is the device's own, the register says
  which reclosers are read on site, the terms define the season, the record since the last inspection, the budget, the
  faults failed protection caused and the state the refit is valued at) still leaves a run to estimate each drift,
  each memory's losses, a level for every zone from its own confirmed seasons, the tail of a record under that level's
  uncertainty, and the state each failure had reached; a wrong choice at each is an estimate made wrongly.
Not rule application: the terms file what is referred (faults since the last cyclic inspection against what its lines
  would have had with sound protection under the lightning near them, beyond chance, at no more than one sound zone in
  five seasons across the network), never how: no shipped sentence matches faults to strokes, fits a drift, fills a
  memory, names a zone level, a scatter structure, a level's uncertainty or the seasons a level is learned from, or
  says which seasons show the state the refit removes.
Estimand: programme terms 2(b) the season (1 April to 31 October), 2(c) a lightning fault counted once against the
  zone whose lines it was on, 2(d) sound and failed protection, 2(e) the record since the last cyclic inspection, 2(f)
  the faults failed protection caused (the network's lightning faults less those its lines would have had with every
  zone sound), 2(g) the lightning near a zone (ground strokes within 400 m), 3(a) the comparison ("more than its lines
  would have had with sound protection"), 3(b) the budget (one sound zone in five seasons across the network: 1/(5 x
  143) a zone a season), 4(c) the avoided faults (what its zones would run with their protection as it stood at the
  end of the 2026 season, above what their lines would have with sound protection, at the 2022 to 2026 average
  lightning: the state is filed, not how to read it), 5 the check per inspection; the prompt fixes the seasons 2022 to
  2026 and the 2027 refit.
No decoy: no memo, draft, ranking or scorecard of zones ships; the OMS cause code answers its own question (the
  dispatcher's cause of a sustained outage) correctly; the rain gauges, the materials quotation and the transformer
  book answer their own questions and decide nothing; nothing is written to carry a wrong answer.
No replay: no result re-derives a published figure and no shipped number is wrong; every graded figure is a quantity
  no file states.
Pinned: the golden family (match windows of -0.4 to 0.5 s and -1.0 to 1.2 s, faults matched within 300 or 500 m, no
  transformer term, weak positive discharges left out, each level from every confirmed season, the level shape at both
  ends of its 95 per cent interval, a stroke-level sound model from each stroke's current and distance, the replay with
  only the inspections completed by then, unread months restored at the zone's rate since inspection, the refit valued
  on the seasons since each failure began) refers the same 11 zones and lands every graded figure inside its band
  (checks.py R7 rows); every covariate set within 2 AIC of the best refers the same 11 (SF16); the confirmed seasons
  reject a pooled season scatter for a level per zone (2 dlogL 165.6) and Poisson for the pooled scatter (79.2); terms
  3(b) rejects the level taken as known (SF19); the independent verifier, on its own clocks, grouping, Simpson grid and
  exact convolution of the seasons, refers the same 11.
Run forecast: R1 earned by a careful run (the record rebuilt); R2 within reach of it (204 against a band of 170 to
  200: the levels move the network's sound expectation by 4 per cent); R4, R3, R5 and R6 lost to a scatter taken season
  by season (quasi-Poisson or one negative binomial a season: method shortcut), which refers 13 zones, 4 of them
  differently, and checks 8 referrals at inspection with one found sound; a run that finds the levels and takes them as
  known (unfinished chain: the level estimated, its uncertainty never carried into the tail) earns R4 and R2 but refers
  17, replays 7, 4, 5, 11 and 17 and claims 0.13 sound referrals a season for a rule that makes 1.2 (self-confirming
  check); R7 lost to valuing the refit on each zone's record since its inspection, averaged (72, or 83 on the
  season-by-season set: unfinished chain); a run that ignores zone levels entirely refers 8.
Strategy label: Engineering and Physical Sciences 2, "Finding the breaks in a station network before trusting its
  trend" (an instrument network repaired before anything is flagged), read with Product Analytics 5's alarm against a
  baseline that swings by itself; neither's chain is used
Depth level: 5: four analytical judgments (each zone's own level, its uncertainty in the tail, the state each failure
  had reached, the reconstruction's drift and losses), each landing its own results; 9 distinct wrong referral sets
  over 12 shortcuts, from 7 zones to 22, the known-level rule's 17 and the season scatter's 13 among them
Lesson: an alarm over many units is only as good as the null it judges each unit against; when units differ
  persistently, a scatter fitted season by season passes the units that always run high as failures and hides the
  low ones that fail, and only each unit's own verified history separates the two, while the value of acting is the
  state now, not the record's average. No build on file teaches it: task6 rebuilt events a store dropped at a known keep
  rate, task2 cut a drifting process at a limit, and neither judged units against their own verified history.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the network's lightning faults each season: 561, 413, 593, 620 and 655 (2022 to 2026), 130 of 2026's on the 32 radio-less zones (87 kept by their memories) | assembly and reconciliation | terms 2(b), 2(c); faults matched to strokes on each device's clock; each zone's own rate over its observed months carried to the months its memory lost or nobody has read | 4 per cent each season; 120 to 138 | method shortcut: a ten-minute window around the radio-less stamps counts storm trips as lightning and nothing lost is restored (630 in 2026); narrow look at broad data: the logged events taken as every fault (87) | - | Component 1 |
| R2 | 2026's lightning faults failed protection caused: 186 (655 against 469 with every zone sound at its own level) | decomposition and attribution | terms 2(d), 2(f); the rate and the zone levels learned from the 779 confirmed-sound zone-seasons | 170 to 200 | method shortcut: no level of its own (204); a sound rate fitted on unverified seasons leaves 165; the referred zones' excess alone 120 | R1 | Component 3 |
| R3 | the 11 zones referred for the 2027 refit | modeling | terms 3(a), 3(b); each zone's record against the predictive tail of its own level at 1/(5 x 143) | exact set | method shortcut: a scatter taken season by season refers 13 (4 different); unfinished chain: each level taken as known refers 17 (6 more); no level of its own 8; Poisson 22; the whole record 7 | R1 | Recommendation |
| R4 | the referred zones' record since inspection against what sound protection would have given them, zone by zone (BGS-F3-R1 31.6 against 9.4 to TGP-F3-R1 39 against 8.9) | exploration and triage | terms 2(e), 3(a); each zone's own level from its confirmed seasons times the register-feature rate times the strokes within 400 m | 20 per cent each zone | method shortcut: every zone at the network rate (7 of the 11 expectations off by more than a fifth) | R1 | Ask (record since inspection) |
| R5 | the alert load: 2, 2, 4, 8 and 11 zones referred after 2022 to 2026, and 0.14 sound zones a season's referrals should hold | uncertainty | the same rule replayed after each season, each level learned outside the record judged; each zone's predictive tail at the smallest count it is referred at | 1 to 3, 1 to 3, 3 to 5, 7 to 10, 10 to 12; 0.12 to 0.16 | method shortcut: the season-by-season scatter refers 2, 5, 4, 10 and 13; self-confirming check: the known-level rule replays 7, 4, 5, 11 and 17 and claims 0.13 sound referrals a season for a rule that makes 1.2 | R3 | Ask (alert load) |
| R6 | against the inspections of 2022-23 to 2025-26: 5 referred zones inspected, 5 confirmed, 21 misses | validation | terms 5 (each inspection against the rule after the season before it); the inspection book | 3 to 6, 3 to 6 and 20 to 23 | self-confirming check: the season-by-season and known-level rules check 8 referrals, 7 confirmed, and 19 misses, and a run reads the near-perfect confirmation as its rule validated, though any rule confirms the failed zones it refers and only the sound zones it refers separate the rules | R3, R5 | Ask (inspection check) |
| R7 | the lightning faults the refit avoids in a season of average lightning: 116 | forecasting | terms 4(c) (the state at the end of 2026); each referred zone's seasons since its inspection against its own sound level show the failure beginning partway; its 2026 season above that level, at its 2022 to 2026 mean lightning | 104 to 128 | method shortcut: the record since each inspection pooled though its seasons ran at different rates before and after the failure began (72; 83 on the season-by-season set), the run naming that record as informative of the coming season and moving on | R1, R3 | Component 2 |

Carry-forward: R1 stands on the reconstruction alone; R2 and R4 add the confirmed-sound expectation with each zone's
level; R3, R5 and R6 fall with the level's uncertainty as well as the level; R7 falls with the state each failure had
reached, and only loosely with the set (the season-by-season set valued on the 2026 state gives 117, inside the band).
A run that slips on the levels keeps R1 and R7's method; one that takes the levels as known keeps R1, R2 and R4; one
that slips on the state keeps everything but R7.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Each zone keeps its own sound level (earth resistance, hardware, route), lognormal across zones, beyond the register's features | constructed by the simulated site factor on every zone (coefficient of variation 0.42 as fitted) | no: all 143 zones; 4 of the season-by-season rule's 13 referrals differ from the golden's 11, and most high-level zones decide nothing | modelling: the confirmed seasons' residuals stay with the zone from season to season (2 dlogL 165.6 for the zone level) | modelling: a two-level model, each level learned from the zone's own confirmed seasons outside the record judged, the tail under the level's uncertainty | keep |
| The radio-less controllers' clocks drift between site visits and are set at each read | constructed by the simulated controllers and visit rounds | no: all 32 radio-less controllers drift; 3 of the 11 referred zones are radio-less | modelling: each controller's trip-to-stroke lags against time, or its loss-of-supply events against upstream lockouts | modelling, earned by a careful run | keep |
| The controllers' memories overwrite their oldest events and the months since each last read are unread | constructed by the simulated memories, weekly battery tests and visit rounds | no: 63 of 947 reads lost 1,346 events on 18 zones, most not referred; every radio-less zone has an unread tail | a targeted query (event-number jumps, read dates) then modelling | modelling, earned by a careful run | keep |
| Failures begin partway through each zone's record since inspection (thefts on their own dates, the arrester lot ageing, the insulator batch cracking) | constructed by the simulated theft, Weibull arrester ageing and cracking hazard across every substation | no: failures begin and grow across the network; in the first season after inspection 9 of the 11 referred zones ran at under half the multiple of their own sound level they reached in 2026, and the 21 failures the inspections found unreferred are mostly the same pattern caught early | modelling: each zone's seasons since inspection against its own sound level | modelling: the state at the end of 2026 read from the seasons since the failure began, carried into the avoided faults (terms 4(c) files the state, not the reading) | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 lightning faults per season, the radio-less zones' 2026 | Missed | Right | Right |
| R2 2026 faults failed protection caused | Missed | Partly | Right |
| R3 zones referred for the 2027 refit | Missed | Partly | Right |
| R4 the referred zones against sound protection | Missed | Missed | Right |
| R5 the alert load: referrals each season, sound ones | Missed | Partly | Right |
| R6 referrals against the following inspections | Missed | Missed | Right |
| R7 faults the refit avoids, average season | Missed | Missed | Right |
| Roughly | 0 of 7 | 2.5 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "a zone that runs high when its protection is sound runs high every season: judge each zone against its own confirmed-sound seasons"; rescues 2 of 7 results
Pair estimate: 35.2

The quick pass reads the OMS LIGHTNING code as the lightning record. The careful pass is calibrated to both stage 4
judges' own first passes and graded up wherever either went further: it rebuilds the radio-less clocks and restores
the lost and unread months (architecture 2's pass did; architecture 3's did not, and is not priced), learns the sound
rate only from seasons a later inspection confirmed sound, fits the register's features, reads the window and the
budget right and computes the rule's own sound referrals (architecture 3's pass did, 0.13 to 0.15, so R5's sound cell
is priced Right); it takes the scatter season by season (quasi-Poisson, as architecture 2's pass did) and values the
refit on each zone's record since its inspection, averaged. Each hint is executed the way a run acts on it: told that a
zone keeps its own level, the pass estimates each level from the zone's confirmed seasons and takes it as known, which
mends the expectations (R4) and the network's sound count (R2) and refers 17 zones. Priced on the same split (generator
runs): the careful pass with the levels taken as known scores 48.3, with the 2026 state alone 43.2, with the levels
carried uncertain 92.0, and with that and the state 100; a pass that drifts the clocks but restores nothing scores 31.2,
and one that also keeps one clock for every device 11.0, which is where architecture 3's judge sat. The build's risk is
a run that carries each zone's level uncertain into a predictive tail: the levels alone (a random effect per zone,
read off as each zone's estimate) leave it at 48.3, and only the predictive tail lifts it past the bar.

## Frontier check

Precedents: R2 L09 (the pooled figure decided on after the split was seen); R3 L35 (an independence binomial where
  units share shocks: a zone's seasons share its level), L09, L33 (units never checked for varying beyond sampling
  error); R4 L09, L33; R5 L35, L28 (the known-level rule certified by its own tails, a check that cannot see the
  problem); R6 L28, L29 (a rule's near-perfect confirmation taken as its validation); R7 L12 (cohorts pooled though
  their rates drift), N02 (history assumed informative of the forward window). R1 is priced Right: its repairs are
  the field's standard ones, which the run record counts as reflexes, though architecture 3's judges restored nothing
  on either pass.
Shallow path checks: the season-by-season scatter (R3, R5, R6) passes its own checks: its dispersion is fitted on the
  same zone-seasons (quasi-Poisson 1.6) and its referrals run 7 of 8 confirmed at the next inspection; a check of
  another kind refutes it, a split-half replication of each zone's ratio over
  its confirmed-sound seasons (odd against even seasons correlate 0.45 to 0.59, both stage 4 judges), which needs the
  inspection book's rounds (zone by round) beside the fault record (zone by season). The known-level rule (R5) passes
  its own check, 0.13 sound referrals a season computed on its own tails; a check of another kind, the same rule's
  tails under each level's uncertainty from its few confirmed seasons, finds 1.2. The averaged record (R7) passes its
  own check, every referred zone above its sound level since inspection; a check of another kind, each zone's seasons
  against its own sound level in time order, dated from the inspection book's repair completions (zone by round),
  shows 9 of the 11 below half their 2026 multiple in the first season after inspection.
Assumption made false: a run lists "a zone's seasons are exchangeable once its features and lightning are counted" and
  "the record since inspection is informative of the zone's state" and moves on. The world's process makes both false:
  each zone keeps its own site (earth resistance, hardware, route), constant through time and lognormal across zones,
  and protection fails on its own date (a theft, an arrester ageing, a crack) inside the record. The pack tests the
  first on the inspection-confirmed seasons and the second on each referred zone's seasons since its repairs.
Forcing: the call is a set. The golden family (ten rival methods: the match windows, the match radii, no transformer
  term, weak discharges left out, each level from every confirmed season, a stroke-level sound model, the as-of replay,
  the unread months at the zone's rate since inspection) files the same 11; every fitted input moved by its defensible
  spread files the same 11 (the sound rate 10 per cent either way, about five standard errors of its 2,692 confirmed
  faults; the level shape at both ends of its 95 per cent interval, 4.05 and 8.16; the seasons' scatter size 20 per cent
  either way); the weakest referral sits at 9.4e-5 and the strongest left out at 3.6e-3 against 1.4e-3; the shortcuts
  file 9 other sets, from 7 zones to 22.
Noun swap: the nearest on file is task6 v7 (a ticketing marketplace's latency SLIs from a trace store) at severity
  none: decision form new (a monitoring rule with its alerts against a set over a threshold), answer pattern shared
  but generic (the naive set swaps members, which the guard does not count), one lesson shared (observation_window_coverage, supporting here), detection the same
  (record time against event time), moves partly shared (impute_by_model_at_own_drivers), file roles 0.75; swapped
  into task13 its nouns leave the zone's own level learned from inspection-confirmed seasons, the level's uncertainty in
  the tail and the state each failure had reached unmatched. The guard's two WARNs: observation_window_coverage sits on
  task16 v2 and task3 v7, and here it is a supporting repair, not the deciding lesson; variance_beyond_sampling_noise is
  taught once, by the client's example 15 (a cohort term for reading partnership places, the cut of a ranked list),
  and here it is learned per zone from inspection-confirmed seasons and carried uncertain into an alarm's tail, beside
  the state valuation and the reconstruction.

## Data provenance

Source: generated by `task13/generator` from a simulated process
Behaves like the real thing: thunderstorm cells drift across the franchise and drop flashes of several strokes with
  lognormal peak currents; the lightning network detects each stroke with an efficiency that falls below about 4 kA
  and places it with an error ellipse, reporting cloud pulses beside ground strokes; each stroke near a line flashes
  it over by induction or by a direct hit at a rate set by the span's construction, the arrester cover, the state of
  its ground leads, arresters and pin insulators, and the zone's own site (earth resistance, hardware and route,
  lognormal across zones and constant through time); breakers and reclosers run their trip, reclose and lockout
  sequences; radio-less controllers keep their own clocks and fixed-size memories, run their weekly battery test at
  03:00 on their own clock, and are read and reset at site visits on a round of about four months; dispatchers log
  sustained outages with their own cause codes; crews inspect each zone once in five dry seasons over two cycles and
  find about nine failures in ten; ground leads are stolen near towns, one arrester lot ages out from 2023 and one
  insulator batch cracks from 2020.
Genuine patterns: (1) the lightning season and the dry season (storms April to October, typhoons, inspections and
  most site visits December to May); (2) spatial structure (storm tracks, hills and towns, tree cover, construction
  types and the 2017-18 arrester programme); (3) a persistent level per zone and a season-to-season swing; (4) stroke
  multiplicity and the current distribution; (5) the arrester lot's ageing and the insulator batch's cracking hazard;
  (6) theft falling off with distance from town; (7) year-to-year storm activity over ten seasons
Problems by process: controllers' clocks drift and are reset when a technician reads them; fixed memories overwrite
  their oldest events under weekly battery tests and busy seasons; the months since a controller's last read are
  unread at the pull; every download re-exports the whole memory; the lightning extract runs in UTC with cloud pulses
  included; upstream breakers trip sympathetically on downstream faults; the SCADA history drops events during comms
  failures; dispatchers code causes by judgment; inspections miss about one failure in ten
Breadth: 12 files; 143 zones on 1,177 overhead routes, 32 of them on controllers read on site; ten seasons (2017 to
  2026) of 250,565 located strokes, 63,558 SCADA events, 133,973 downloaded events from 947 reads, 4,537 outages and
  286 inspections over two cycles; every zone is reconstructed and scored every season, and which devices, which
  seasons and which levels to trust is work

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, modeling, exploration-triage, uncertainty,
  validation, forecasting
Question form: what (the rule and the zones it refers)
Nearest build: task6 (events a store dropped, restored before a flagged set): there whole traces were kept at a known
  hourly rate and the weight sat on a hard-to-measure quantity; here the losses are each controller's own and the
  weight sits on designing an alarm whose null carries a level per unit learned from that unit's independently
  verified history, with the alert load, the false-alarm rate and the inspection check graded. Against mark119 (excess
  failures over expected per unit) there was one expectation shared by every unit and no record to repair; against
  task13's earlier architectures nothing of the scatter structure or the last-season valuation survives.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "lightning fault" | every trip; every fault start on the zone's device; faults the OMS codes LIGHTNING | each fault start whose first trip lines up with a stroke near the zone's lines, counted once against that zone | terms 2(c); the OMS records sustained outages only |
| SF2 | "near" and the radius a fault is matched over | exposure within 400 m, 800 m or 1 km; matching within 300 m to 1 km | exposure within 400 m; matching within 400 m | terms 2(g) files the exposure; the matching radius is same call from 300 m to 1 km (checks.py SF2) |
| SF3 | "lightning season" | the calendar year; 1 April to 31 October | 1 April to 31 October | terms 2(b) |
| SF4 | "since its last cyclic inspection" | from the inspection's start; from the day after its repairs; the whole record | the day after the repairs were completed to the season's end | terms 2(e); the whole record refers 7 |
| SF5 | the seasons a sound rate is learned from | seasons a later inspection found sound; every season not yet found failed; every season | seasons a later inspection found sound | terms 2(d) makes soundness a state only a later inspection records; the book shows zones inspected clean and found failed at the next round |
| SF6 | "more than its lines would have had ... by more than chance explains" | a scatter taken season by season (Poisson, quasi-Poisson, one negative binomial a season); each zone's own level and a season scatter | each zone's own level (gamma, shape 5.74) and a season scatter | 3(a) says "its lines"; the confirmed seasons carry a level per zone beyond any season-by-season scatter (2 dlogL 165.6) and reject Poisson (79.2) |
| SF7 | "no more than once in five lightning seasons on average" across the network | 0.2 a zone a season; 0.2 a season across the network; 0.2 a season spread over the sound zones only | 0.2 a season across the network, 1/(5 x 143) a zone | terms 3(b) "Across the network"; spread over the sound zones only (any count from 60 to 143) the threshold stays between the weakest referral and the strongest non-referral, same call (checks.py SF7) |
| SF8 | "how many of a season's referrals should be zones with sound protection" | the budget (0.2); the rule's own expected count | the rule's own (0.14), each zone's tail under its level's uncertainty | the budget is a ceiling ("no more than", 3(b)); the ask is what the rule will do |
| SF9 | "the network's lightning faults in each season" | the faults the logs kept; every fault the season had | every fault, the lost and unread restored | terms 2(c) defines a fault by the flash; the downloads' event numbers show events the memories lost |
| SF10 | "how many of 2026's were caused by failed protection" | the network less every zone sound; the referred zones' excess; each zone's positive excess summed | the network less every zone sound (186) | terms 2(f); the referred zones' excess (120) leaves out failed zones not yet referred, the positive parts (298) count chance on sound zones |
| SF11 | "how its referrals compare with what the next cyclic inspections found" | per referral; per inspection | per inspection, against the rule after the season before | terms 5 |
| SF12 | "a season of average lightning" | each zone's 2022 to 2026 mean; 2026 scaled to the network mean | each zone's 2022 to 2026 mean | terms 4(c); 2026 scaled to the network mean lands inside the band, same call |
| SF13 | the CSV's "faults since its last cyclic inspection against what sound protection would have given it" | logged against the full-season expectation; restored against the full expectation; logged against the observed months' expectation | restored against the full expectation at the zone's own level, the same ratio as logged against the observed months | same call on the ratio and the referral by construction |
| SF14 | which zones | the register's 143; the zones with SCADA | the register's 143 | terms 2(a) |
| SF15 | the count the chance is judged on | the faults the records hold against the expectation for the same months; the restored count against the full season | the records' own count | a restored count is an estimate; judged as if counted it adds LRD-F2-R2 (16 recorded against 5.4 expected) |
| SF16 | which of a zone's features the sound rate carries | any subset of the register's construction, area, arrester and transformer shares | the full set | every subset within 2 AIC of the best refers the same 11 under the zone levels (checks.py SF16) |
| SF17 | the seasons a zone's level is learned from | every confirmed season; those outside the record being judged | those outside the record being judged | same call on the set and within one on every season's referrals (checks.py SF17); a level learned from the seasons judged would judge them by themselves |
| SF18 | "with their protection as it stood at the end of the 2026 lightning season" | each zone's 2026 season above its own sound level; the seasons since its failure began; its record since inspection averaged | the 2026 season (116); the seasons since the failure began (115) land in the band, same call | terms 4(c) files the state; the referred zones' own seasons show the failures beginning partway (in the first season after inspection 9 of 11 under half the multiple of their sound level they reached in 2026; all 11 above twice it in 2026), so the average (72) values states they have left (checks.py SF18) |
| SF19 | "by more than chance explains" for a zone whose own level is estimated | the level taken as known; the level as uncertain as its confirmed seasons leave it | the level carried uncertain into the tail | terms 3(b) budgets the sound zones the rule refers: with each level taken as known the rule refers 17 and, under the levels' own uncertainty, would refer a sound zone 1.2 times a season against 0.2 (checks.py SF19) |
| SF20 | "what its lines would have had with sound protection, under the lightning that fell near them" | a rate times the strokes within 400 m; each stroke's chance from its current and its distance to the lines | the rate times the strokes | same call: the stroke-level model refers the same 11 and lands every graded figure in its band (checks.py SF20, R7 rows) |
| SF21 | the rate a zone's lost and unread months are restored at | the same season's observed months; the zone's record since inspection; its sound level | the same season's observed months | same call on the record since inspection (every season inside its band, the same 11); the sound level undercounts a failed zone's months and is ruled out by the zone's own observed rate (checks.py SF21) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the register's 143 zones (terms 2(a)); every zone scored after every season, none excluded |
| 2 | Unit of account: the protection zone; a fault counted once against the zone whose lines it was on (2(c)), an upstream breaker's sympathetic trip is not its zone's fault |
| 3 | Attribution window: a fault belongs to the season of its first trip (2(b)); the matched stroke and trip sit within a second, so no fault straddles a season's edge (C1) |
| 4 | As-of dating: the rule after the 2026 season, on the inspection book as it stands (rounds through 2025-26) and the register of September 2026 |
| 5 | Version basis: one register, one inspection book, no revised extracts; C1 |
| 6 | Denominator: the expectation is a rate times the strokes within 400 m in the zone's observed months, times the zone's own level (3(a)); the CSV's ratio divides by that expectation since inspection |
| 7 | Weighting: none; each confirmed zone-season enters the fits as a count with its exposure; the false referrals are summed over zones (3(b)) |
| 8 | Window length: the record since the last cyclic inspection (2(e)); the rate and the levels use every confirmed-sound season of 2017 to 2026 |
| 9 | Boundary inclusivity: strict ("more than"); no 2026 zone sits near the threshold (weakest referred chance 9.4e-5, strongest unreferred 3.6e-3, threshold 1.40e-3; C1); the earlier replays' borderline zones are carried in R5's and R6's bands |
| 10 | Rounding path: counts whole, the CSV to one decimal, each graded figure rounded once at the end at the precision the answer blocks state |
| 11 | Tie-break: none needed; no two zones tie at the threshold (C1) |
| 12 | Maturity and censoring: the radio-less controllers' unread months and overwritten events restored at each zone's own rate (R1); every SCADA zone's 2026 season is complete |
| 13 | Order of operations: match, then collapse each fault, then season, then the rate and the levels, then the tail; the referral compares logged faults with the observed months' expectation, the same ratio as the restored faults against the full season (C1) |
| 14 | Row order: no result depends on file order (every match sorts by device and time; C1) |
| 15 | Duplicate resolution: a re-read event (same controller, same event number) kept once; counting repeats moves no referral (checks.py R2) |
| 16 | Identity normalisation: every system keys the zone by its register name or its device point, which map one to one |
| 17 | Netting against gross: R2 nets by definition (2(f)); a sound zone's shortfall offsets another's chance excess |
| 18 | Dimensional units: counts of faults and of strokes only |
| 19 | Code and status semantics: the register's telemetry label says which controllers are read on site; the OMS cause codes are not read by the golden |
| 20 | Integerisation: none in any computation; graded counts rounded at the end |
| 21 | Clause scope: 3(b)'s budget holds in every season the rule is run after, across the network, on the sound zones the rule refers whatever its own estimates; 4(c)'s state is each refitted zone's protection at the end of the 2026 season and its average lightning each zone's 2022 to 2026 mean |
| 22 | Forward window contents: 2027 is not observed; R7's season of average lightning is the 2022 to 2026 mean terms 4(c) names, so no forecast of 2027's storms is needed |

## Literal reader

Terms 2(c) executed word for word on the device histories gives each zone's lightning faults only once each fault's
first trip is placed on the same clock as the lightning extract, which for the 32 controllers read on site means
fitting each one's clock; 2(c) defines the fault by the flash, so the events their memories overwrote and the months
nobody has read are faults the season had (R1). 3(a) asks for what "its lines" would have had with sound protection,
and 2(d) makes soundness a state only a later inspection records, so the expectation is learned from the confirmed
seasons, and since those seasons show every zone keeping a level of its own, its lines' expectation carries that level
(R4, R2); 3(b) budgets the sound zones the rule refers across the network, which a rule holds only when the chance it
judges by carries each level's uncertainty (R3, R5); 5 checks each inspection against the rule after the season before
it (R6); 2(f) defines R2's quantity, and 4(c) files R7's as the zones' state at the end of 2026, which their own
seasons since inspection show. Every literal reading gives the golden's quantities; the hurried figures come from
easier methods on the same estimands (a scatter taken season by season, a level taken as known, the record since
inspection averaged), never from another reading. No shipped sentence names a method, a clock, a memory, a level, a
level's uncertainty, a scatter, the seasons a level is learned from or the seasons that show a failed zone's state.

## Prompt contract

A voice rewrite may not drop or change: the question (what rule to run after each lightning season to refer the
zones whose lightning protection has failed, and what zones it refers for the 2027 refit); for every zone, a CSV with
its lightning faults in each season from 2022 to 2026, its faults since its last cyclic inspection against what sound
protection would have given it, and whether it is referred; a short note with a chart giving the rule and the zones it
refers, how many zones it would have referred after each season since 2022, how many of a season's referrals should
be zones with sound protection, how its referrals compare with what the next cyclic inspections found, the network's
lightning faults in each season, how many of 2026's were caused by failed protection, and the faults the refit should
avoid in a season of average lightning. It must never add: a rounding instruction, a method or a comparison (clocks,
drift, memories, filling, levels, a scatter, the seasons a rate is fitted on, a window), a warning, an attached file's
name, a role, a count the data hold (143 zones, 32 radio-less reclosers), or a fact the files carry.

## Leak rulings

- leak.py 4 (design-note vocabulary) on the programme terms (record, seasons, referral, strokes): harmless; the terms
  define the season, the record since an inspection, what the rule refers and the lightning near a zone's lines in the
  co-op's own words, and no sentence names a clock, a memory, a level or its uncertainty, a scatter, the seasons a rate
  is learned from or which seasons show a failed zone's state.
- leak.py 11 (shell quota): a corpus count of other prompts' question form; this prompt asks what rule, the form its
  decision takes.
- The isolated reader (full read of architecture 3, re-read of the two files the revision changed): Q1 and Q5 the terms'
  definitions, each the filed WHAT (the revised 4(c) "fixes the estimand ... not the method"); Q2 to Q4 none; Q6 none
  ("No single sentence or file does"). Rulings in leak_check_report.md.

## Pre-ship check

On the final cut (gates.py task13 --full, 2026-11-11: 11 gates, 0 FAIL, 3 WARN; checks.py 200 of 200, verify.py PASS,
two builds byte-identical, figures_check and the container gate PASS):

- Hidden factor record against the cut data (checks.py R5, SF6, SF18): every zone keeps its own sound level (gamma
  shape 5.74, coefficient of variation 0.42 across the 779 confirmed-sound zone-seasons, 2 dlogL 165.6 over a
  season-by-season scatter), and the season-by-season rule's 13 differ from the golden's 11 in 4 zones; all 32
  radio-less controllers drift, 3 of them on referred zones; 63 of 947 reads lost 1,346 events on 18 zones, most not
  referred; in the first season after inspection 9 of the 11 referred zones ran at under half the multiple of their
  own sound level they reached in 2026, and all 11 above twice it in 2026, while the 21 failures the inspections found
  unreferred sit on 21 zones under 8 of the 12 substations. No factor sits only where it decides.
- Effort test against effort.py on the final cut: quick 7.0, careful but hurried 35.2, thorough 100; the largest
  single hint (the zone's own level, executed as a run acts on it) rescues 2 of 7 and refers 17; the level's
  uncertainty alone rescues nothing; the failures-began-partway sentence rescues 1; 12 shortcuts give 9 different
  wrong referral sets; every lost cell cites a frontier precedent of its class (the cited pair 35.2), and the forcing
  record has 10 rival methods and 6 fitted-input perturbations all filing the same 11. The careful pass with the
  levels carried uncertain scores 92.0 and is the build's risk.
- Rivals (checks.py R7 rows, SF7, SF16 to SF21, verify.py): 13 members of the golden family (the match windows, the
  match radii, no transformer term, weak discharges left out, levels from every confirmed season, the level shape at
  both ends of its interval, a stroke-level sound model, the as-of replay, the unread months at the zone's rate since
  inspection, the refit valued since each failure began) refer the same 11 and land every graded figure in its band;
  every covariate set within 2 AIC refers the same 11; the budget spread over the sound zones only keeps the set; the
  independent verifier refers the same 11 with its back-test at 3, 3 and 23, inside the band.
- Leak reader (full read of architecture 3, re-read of the revised terms and register on the final cut): no ranking
  file, no answer figure, nothing planted; Q1 and Q5 the filed WHAT ("fixes the estimand ... not the method"), Q6 none.
- Judge (p4, on the final pack and blocks, its thread's own derivation written before it opened the blocks):
  DETERMINISTIC, APPROVE. Gate G: method_or_model_selection, analytical_non_defect, no surface read, no sole data
  defect. Gate H: domain pass, layers pass, 10 results across 6 areas, one thing none (borderline). Its first pass,
  read against the careful column: the 2022 to 2025 totals inside (555, 408, 574, 610, unrestored), 2026 out (607),
  the failed-protection count out (135), the set out (10 zones, BGS-F3 in, BGS-F3-R1 and CLB-F2 out), the alert load
  inside after 2024 to 2026 only, and the refit valued on the record since each inspection averaged (66, out): nothing
  it landed sits where the careful column prices less than Right, so the pair stays 35.2. Its best single sentence (the
  clocks and memories) rescues about 4 of 10 against its own pass, which restored nothing; the careful column restores,
  so it rescues none there. p3, on revision 1, is recorded in `## Tried and rejected` and determinism_check_report.md.
- Duplicate check: guard.py heart WARN, no BLOCK (overuse.forum, repeat.gate_g and repeat.decision answered in Draw);
  surface exit 0.
- Dates: the pack pulled 4 November 2026; the golden's files and its note dated 9 and 10 November 2026, before the
  upload.


## Tried and rejected

- A smart-meter outage-alert rollout recording small outages that customer calls missed, as the decisive layer:
  rejected at the draw, 2026-11-09. Which comparison is clean (recorded against experienced) is the estimand, so
  filing it spends the layer and leaving it open is a fork (`determinism-check` section 1).
- A random scratch world (feeder size and tree density drawn freely): the three-year count and the wind-normalised
  rate alone reproduced four to six of the golden six on five seeds, because size dominated; the world is built from
  groups (overdue northern feeders, dense plantation feeders trimmed recently, southern late-cycle feeders, overdue
  feeders with few trees) so each shortcut lands on a different wrong list.
- A one-year wind anomaly carried by the station's mean level: the decomposition fitted without the wind still landed
  four to five of the six, because one year is a small share of the outage record and a higher mean moves every gust
  alike; replaced by three years in which the storm track sat south (fewer strong-wind days in the north, about twice
  as many in the south, mean wind within 6 per cent) over an outage record from April 2022.
- Plantation feeders trimmed early in 2025 on a four-year cycle: their growth left them among the golden six; moved to
  a three-year cycle cut in the second half of 2025, which keeps them first on every recent count and on expected
  interruptions and last on the growth a catch-up removes.
- Major event days set by the 2.5-beta rule on the record: wind-storm days crossed the boundary and carried a fifth of
  the strong-wind hours, so the projection's treatment of those days moved the six's total by half; the filed
  boundary values now sit above every storm day, and the major event days are the five snow days.
- Hours of gusts of 60 km/h or more as the golden's exposure: 30 feeder-months with vegetation interruptions had no
  exposure at all, and the six's total moved 28 per cent across thresholds; the gust load, which fits the record best, is
  the golden, and the hour counts stay in the family (same six).
- Architecture 1 as a whole (Kotuku Networks' 2027 vegetation catch-up, READY 2026-11-09, never run on the platform):
  re-rooted 2026-11-11 at the author's word, for a stronger chain with at least three independent analytical failure
  points. Cut under the retired single-deep-step design: one Poisson fit carried every graded figure, the plantation
  feeders' dense corridor sat only in the deciding units with one filter as its fix, and the storm-track swing showed
  in one plot of gust hours by station.
- Architecture 2 at the prototype, a referral on the latest season alone: with about eight sound faults a zone-season
  the failed zones (2.2 to 3 times their sound rate) were referred at p near the threshold; the window became the
  seasons since the zone's last cyclic inspection, as the programme terms file it.
- Architecture 2 at the prototype, the sound expectation fitted on the season after each inspection only: 172
  zone-seasons of about eight faults could not show the sound zones' spread (the moment estimate of the negative
  binomial size ran to infinity) and the referral set swung from 0 to 10 zones with the dispersion; the expectation and
  its spread are fitted on every season a later cyclic inspection confirmed sound (410 zone-seasons, size near 25).
- Architecture 2 at the prototype, line arresters with no effect on direct strikes: losing them lifted a zone's
  lightning faults about 1.9 times, inside the scatter of sound zones around any design model; arresters every few
  spans now also drain part of a direct strike's current, so a zone that loses its ground leads or arresters runs 2.5
  to 4.5 times its sound rate, as the field's line arrester studies show.
- Architecture 2 at the build, the likely failed part at each referred zone (ground leads from burnt transformers per
  lightning fault, arresters from arrester failures in fair weather, insulators from the lockout share) as a graded
  result: on the cut pack 8 of the 15 referred zones carried no signature above one standard error and the pick agreed
  with the simulated state on 10; a result whose golden turns on noise is an open fork, so it left the chain, the
  prompt and the programme terms (3(c)).
- Architecture 2 at the build, the careful pass at one fixed offset per radio-less controller: it finds one fault in
  fourteen on those zones (19 of 259 in 2026), a gap a run would see; the careful pass matches them on a ten-minute
  window around their own stamps instead, which counts storm trips as lightning (212 logged against 163).
- Architecture 2 at the build, the inspection check counted per referral (terms 5 as first drafted: a referral is
  confirmed when the zone's next inspection finds failed protection): a zone referred after three seasons counted
  three times under one reading and once under another, and on a one-zone band a hurried rule landed it by chance;
  terms 5 now checks each inspection against the rule after the season before it, and the three counts are exact.
- Architecture 2 at the build, 2026's faults caused by failed protection left to the question's words: the referred
  zones' excess (199) and the sum of every zone's positive excess (415) read it as well as the network's faults less
  every zone sound (279); terms 2(f) files the quantity.
- Architecture 2 as built (the radio-less clocks, the overwritten and unread months, and the inspection-confirmed
  baseline as its three difficulties), judged DETERMINISTIC and FIX_NOW at stage 4 on 2026-11-11 and sent back to stage
  2 by the judge thread's own first pass, which landed five of the eight results and part of a sixth in seven minutes:
  each difficulty was noticing a property the files show plus the field's standard remedy (a scheduled self-test that
  leaks the clock offset, event-number gaps that announce the losses, an inspection book whose time order names the
  confirmed seasons), which a careful run does by reflex.
- Architecture 3 at the design, each zone's own level on the 2022 to 2026 record alone: with at most four confirmed
  seasons a zone, the worlds where the levels moved the set (4 to 14 zones against a pooled scatter) were the ones whose
  golden moved under its own rivals (the level shape at 0.7 and 1.4 times its estimate, the match radius), and the
  robust worlds were the ones where the levels decided nothing; the record now runs from December 2016, two inspection
  cycles confirm 779 zone-seasons, and every rival refers the same set.
- Architecture 3 at the design, the hurried route as one negative binomial over the whole record: it behaves as a level
  per zone by accident and lands within a zone of the golden; the routes a run takes treat the seasons as independent
  (quasi-Poisson, as the stage 4 judge did, or a negative binomial each season), and those refer 13 zones to the
  golden's 11 and check sound zones at inspection.
- Architecture 3 at the build, the alert counts and the rule's sound referrals graded as two results: the prompt asks
  them in one sentence as the rule's alert load, and as two the levels sentence rescued three of eight; one result of
  six cells, and the chain is seven.
- Architecture 3 revision 1 (as judged at stage 4 on 2026-11-11, DETERMINISTIC and APPROVE): its judge thread's own
  first pass missed the set, the season totals and the failed-protection count but landed two results the note priced
  as lost, the refit's avoided faults (terms 4(c) filed "the faults its zones ran in the last lightning season", a
  method, and the pass executed it: 102 to 121 against 116) and the rule's sound referrals (the pass computed the
  rule's own rate, 0.13 to 0.15; quoting the budget's 0.2 was never a run's reading). Repriced on that pass the careful
  column came to about 56, 65 with the replay's cells, over 50, so the build went back to stage 2: terms 4(c) now files
  the state at the end of 2026 and leaves how to read it to the data, the level's uncertainty is priced as its own
  judgment (the known-level rule refers 17), and every band is the rival family's span.
