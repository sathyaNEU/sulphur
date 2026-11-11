# task13: the co-op's 2027 lightning protection refit and the referral rule behind it

## Draw

Subdomain: Energy Systems & Utilities, task type grid reliability and outage analysis (`grid-reliability-outage-analysis`, the only energy task type serving the assigned analysis type)
Analysis type: Anomaly Detection & Diagnostics
Answer shape: a monitoring rule with its expected alert count (the rule, the zones it refers now, its false referrals a season and its referrals after each season since 2022, checked against the cyclic inspections), with the refit on top
Weight: metric or rule design: most of the work is building the referral signal itself (lightning faults reconstructed on each device's own clock and memory, an expectation learned only from inspection-confirmed sound seasons, a threshold carried on their spread); the last three builds sat on assembly (task14), a hard-to-measure quantity (task3) and validation (task10)
Data-native sentence: a lightning fault exists only as a coincidence between two clocks (a recloser's own record of a trip and a lightning network's record of a stroke near the line), and the reclosers with no radio link keep their own drifting time and only their last 64 or 100 events between site visits, so the zones whose protection has failed, which trip most, are the zones whose records lose the most and line up the worst; what a sound zone should do is visible only in seasons a later cyclic inspection confirmed sound.
People: Lucas Ramirez (technical services manager, takes the refit to the management committee), Donna Rodriguez (reliability and protection engineer, the golden's author), Laurie Diaz (line inspection supervisor), Elizabeth Hernandez (general manager, issues the programme terms), John Fuentes (SCADA supervisor), Michelle Garcia (materials and warehouse); drawn with `guard.py names --geo Philippines` at seeds 1302, 1307 and 1311

**The decision.** Kalumpang Valley Electric Cooperative, a member-owned distribution co-op in Central Luzon, runs 13.2 kV
overhead lines from twelve substations, cut into protection zones by substation breakers and line reclosers. Lightning
is its largest cause of trips. Its 2017-2018 line arrester programme fitted arresters along the exposed lines; since
then ground leads have been stolen for their copper, a contract lot of line arresters has started failing and a batch
of porcelain pin insulators has been cracking. A cyclic line inspection reaches every zone once in five dry seasons. The
board's 2027 budget funds a dry-season refit (grounds, arresters and insulators restored) on the zones a referral rule
names before the 2027 lightning season, and the co-op will run the same rule after every season from now on.

**Card.** `.claude/skills/fingerprint/cards/task13.json`, architecture v2, registered 2026-11-11, guard verdict WARN.
Answered: `overuse.forum` (the management committee approves the dry-season work programme inside the board's budget,
the honest forum for a refit list); `repeat.gate_g` against task15 (there a growth gap split across drivers; here each
zone's faults assigned to lightning on its device's own clock and its excess to failed protection rather than to the
spread sound zones show); `repeat.question_form` (the decision is a rule, so the question asks what it is). Redrawn after
syncing with origin/main, when task14 v3, task15 v2 and task16 v2 entered the window: forum, decisive pattern (G7, the
operating window a recloser's record holds) and Gate G (card `notes`). The v1 card's identity moved into `lineage`.

## Deep reasoning

Task type: Grid reliability & outage analysis (the energy subdomain's task type that serves Anomaly Detection &
  Diagnostics: a referral rule over a network's protection zones, with its alert load and its check)
Domain test: every result is a quantity a distribution reliability engineer computes from protection and lightning
  records: lightning faults attributed by coincidence between a protective device's operations and the strokes a
  lightning location network placed near its lines, each device on its own clock; faults per season against the
  lightning a zone's lines received; what a line with sound grounds, arresters and insulators gives under that
  lightning, and how widely sound zones scatter around it; a threshold carried on that scatter at a stated budget of
  sound zones referred; the alert load a season, the check against cyclic line inspections, and the faults a
  protection refit removes. The field's analyst builds the fault record, learns the sound line's rate, sets the alarm
  and proves it against the line crews' findings.
Swap: "what rule refers the units whose protection has failed" still parses with a hospital's or a fleet's nouns,
  but trips lined up with located strokes on each controller's drifting clock, memories that overwrite their oldest
  events, the lightning that fell within reach of a line and a line inspection that verifies the seasons before it
  all stop meaning anything: the results are this protection system's, not a rate looked up in any field.
Where the weight sits: designing the referral signal itself. The fault record each zone's rule reads (R1, R2) is
  rebuilt from two clocks and from memories that overwrite, and the expectation (R3) and its spread are learned only
  from seasons a later inspection proved sound; the threshold, its alert load (R5, R6) and its check (R7) follow from
  that design. The work is long, not clever: 46 controllers' drifts fitted read by read, 710 reads walked for lost
  events, 855 zone-seasons sorted by what the inspection book can and cannot say about them.
Layer 1: the SCADA history carries the breakers and the radio reclosers with upstream breakers tripping on downstream
  faults and comms-fail gaps; the downloads re-read each whole memory at every visit (the same event numbers on several
  downloads) on the controller's own clock in day-first format; the lightning extract is in UTC with cloud pulses and
  weak positive discharges mixed in while every co-op system keeps Philippine time; the OMS codes each outage's cause by
  the dispatcher's word; the register names zones in two shapes and three telemetry labels; the inspection book counts
  findings per zone and round; the transformer book counts replacements. None decides a result: checks.py moves no
  referral when the re-reads are counted twice or the weak discharges left out.
Not one thing: the strongest single piece is the radio-less reconstruction (each drift fitted per read, the lost and
  unread months filled), and a run that nails it earns R1 and R2 and still loses R3 to R8 to a sound rate fitted on
  seasons nobody verified (40.5 on the rubric split, 0 to 4 zones referred). A run that fits the confirmed-sound
  seasons but matches the radio-less trips on a wide window and counts what was logged still refers 17 zones, six of
  them differently, and misses R1, R2, R3, R5 and R7 (50.7). Only both together, with the spread, the window and the
  budget, reach the golden.
One-fact test: "a season counts as sound only when the next cyclic inspection found nothing" rescues R6, R7 and R8
  (3 of 8, at the third) on the measured careful pass; "the reclosers with no radio link keep their own drifting
  clocks and only their last events between site visits" rescues R1 and R2 (2 of 8); no single sentence rescues R3,
  R4 or R5. The stage 4 judge thread needed neither sentence (Effort test, first-pass reading).
Not semantics: every column and clause read correctly (the controller time is the device's own, the register says
  which reclosers are read on site, the terms define the season, the record since the last inspection, the budget
  and the faults failed protection caused) still leaves a run to estimate each drift from the trips themselves, to
  estimate what each memory lost, and to choose which seasons can teach a sound rate and how widely sound zones
  scatter; a wrong choice at each is an estimate made wrongly, not a field misread.
Not rule application: the terms file what is referred (faults since the last cyclic inspection against what sound
  protection would have given under the lightning near the lines, beyond chance, at no more than one sound zone in
  five seasons across the network), never how: no shipped sentence matches faults to strokes, fits a drift, fills a
  memory, picks the seasons a sound rate is fitted on, chooses a spread or computes the false referrals.
Estimand: programme terms 2(b) the season (1 April to 31 October), 2(c) a lightning fault counted once against the
  zone whose lines it was on, 2(d) sound and failed protection, 2(e) the record since the last cyclic inspection,
  2(f) the faults failed protection caused (the network's lightning faults less those its lines would have had with
  every zone sound), 2(g) the lightning near a zone (ground strokes within 400 m), 3(a) the comparison, 3(b) the budget (one sound zone in five seasons across the network: 1/(5 x
  171) a zone a season), 4(c) the avoided faults in a season with the 2022 to 2026 average lightning, 5 the check per
  inspection; the prompt fixes the seasons 2022 to 2026 and the 2027 refit.
No decoy: no memo, draft, ranking or scorecard of zones ships; the OMS cause code answers its own question (the
  dispatcher's cause of a sustained outage) correctly; the rain gauge file and the materials quotation answer their own
  questions and decide nothing; nothing is written to carry a wrong answer.
No replay: no result re-derives a published figure and no shipped number is wrong; every graded figure is a quantity
  no file states.
Pinned: the golden family (the spread's size by moments, match windows of -0.4 to 0.5 s and -1.0 to 1.2 s, strokes
  within 300 or 500 m, no transformer term, weak positive discharges left out) refers the same 15 zones and lands every
  graded figure inside its band (checks.py R7 rows); every covariate set within 4 AIC of the best refers the same 15
  (SF16); a fault matched over anything from 300 m to 1 km refers the same 15 (SF2); a Poisson spread is ruled out by the confirmed-sound
  seasons (2 dlogL 4.95 for the negative binomial's one parameter, Poisson chi-square 1.23 a degree of freedom), and
  every wider fit set by the inspection book itself (a clean inspection verifies the seasons before it, and the book
  shows zones inspected clean and found failed at the next round).
Run forecast: R1 and R2 lost to a wide or fixed-offset match on the radio-less controllers and to counting the logged
  events (method shortcut; narrow look at broad data, the 125 synchronised zones matched well and the 46 radio-less
  taken as they come); R3, R4, R5, R7 and R8 lost to a sound rate fitted on every season no inspection has yet found
  failed or on every season (self-confirming check: the zones to be found sit inside the baseline that judges them);
  R6 lost to quoting the budget, 0.2, as the rule's false referrals (self-confirming check); R4 also lost to a Poisson
  spread (17 zones, method shortcut) or to the whole record instead of the record since inspection (25 zones,
  unfinished chain).
Strategy label: Engineering and Physical Sciences 2, "Finding the breaks in a station network before trusting its
  trend" (an instrument network repaired before anything is flagged), read with Product Analytics 5's alarm against a
  baseline that swings by itself; neither's chain is used
Depth level: 5: three independent judgments carry most of the score (each controller's drift, each memory's losses,
  which seasons verify a sound rate) and three smaller ones sit beside them (the spread, the record since inspection,
  the budget per zone); 10 distinct wrong referral sets over 11 shortcuts, from 1 zone to 25
Lesson: a monitoring rule is only as good as the record it reads and the baseline it learns from; the units an alarm
  must catch are the ones whose records lose most (they trip most) and the ones that contaminate a baseline fitted on
  unverified periods, so the rule is designed against both and its false-alarm rate is measured, not quoted. No build
  on file teaches it: task6 rebuilt events a store dropped at a known keep rate, task2 cut a drifting process at a
  limit, and neither learned an alarm's baseline from periods an independent check verified.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the network's lightning faults each season: 892, 682, 924, 747 and 1,075 (2022 to 2026) | assembly and reconciliation | terms 2(b), 2(c); faults matched to strokes within 400 m on each device's clock; the golden family | 4 per cent each season | method shortcut: a ten-minute window around the radio-less stamps counts storm trips as lightning and nothing lost is restored (937, 727, 980, 791, 1,028); a fixed offset per controller finds a fourteenth of their faults (686 to 835) | - | Component 1 |
| R2 | the 46 radio-less zones' 2026 lightning faults: 259 (163 logged) | missingness and measurement | the downloads' event numbers and read times; each zone's own rate over its observed months carried to the months its memory lost or nobody has read | 243 to 275 | narrow look at broad data: the logged events taken as every fault (163 on the drift-fitted clocks, 212 on a wide window) | R1 | Ask 1 |
| R3 | 2026's lightning faults failed protection caused: 279 (1,075 against 796 with every zone sound) | modeling | terms 2(d), 2(f), 3(a); the expectation fitted on the 193 zone-seasons a later inspection confirmed sound | 237 to 321 | self-confirming check: the rate fitted on every season not yet found failed absorbs the failing zones (42) | R1, R2 | Component 2 |
| R4 | the 15 zones referred for the 2027 refit | exploration and triage | terms 3(a), 3(b); each zone's faults since inspection against a negative binomial tail at 1/(5 x 171) | exact set | self-confirming check: the careful pass refers 2 (BTG-F1-R3, PGP-F1-R2); method shortcut: a Poisson spread refers 17; unfinished chain: the whole record 25 | R1, R2, R3 | Recommendation |
| R5 | zones referred after each season: 11, 10, 12, 10, 15 | validation | the same rule replayed after each season on the record since each zone's inspection at the time | 1 each season | self-confirming check: the contaminated baseline's spread refers 6, 5, 3, 1, 2 | R3, R4 | Component 3 |
| R6 | the sound zones the rule refers in a season: 0.13 | uncertainty | terms 3(b); each zone's tail at the smallest count the rule refers it at, summed over zones and averaged over seasons | 0.11 to 0.15 | self-confirming check: the budget, 0.2, quoted as the rule's own rate; on the contaminated spread 0.16 | independent: each zone's expectation and the spread | Ask 2 |
| R7 | against the inspections of 2022-23 to 2025-26: 15 referred zones inspected, 15 confirmed, 26 misses | validation | terms 5 (each inspection against the rule after the season before it); the inspection book | 14 to 17, 14 to 16 and 25 to 27 | dismissed own evidence: a rule that refers 2 zones checks 8 referrals and 33 misses, and a run reads 100 per cent confirmed as success without the misses | R4, R5 | Component 4 |
| R8 | the lightning faults the refit avoids in a season of average lightning: 107 | forecasting | terms 4(c); each referred zone's ratio since inspection less one, times its 2022 to 2026 mean sound expectation | 91 to 123 | unfinished chain: 2026's own lightning (133), or the contaminated set and ratios (19) | R3, R4 | Ask 3 |

Carry-forward: R6 stands on each zone's expectation and spread alone, and R7's misses and R1's SCADA-zone faults are
largely independent of the radio-less work; R2 falls with R1's match, R3 with R1 and the fit set, R5, R7 and R8 with
R4's rule. A run that slips on the radio-less records loses R1 and R2 and keeps the rest if its baseline is right,
and the reverse holds for a slip on the baseline: neither slip costs the whole chain.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| The radio-less controllers' clocks drift between site visits and are set at each read (drift 1.7 s a day across controllers, read every 113 days at the median) | constructed by the simulated controllers and visit rounds | no: all 46 radio-less controllers drift; 4 of the 15 referred zones are radio-less, 42 radio-less zones decide nothing | modelling: each controller's trip-to-stroke lags against time show a line per read among coincidences | modelling: a drift and an offset per read, fitted from the trips | keep |
| The controllers' memories overwrite their oldest events (64 or 100 events, four with 1,024) and the months since each last read are unread | constructed by the simulated memories, weekly battery tests and visit rounds | no: 58 of 710 reads lost 1,154 events on 22 zones, most not referred; every radio-less zone has an unread tail (last reads from May to October 2026) | a targeted query (event-number jumps, read dates) then modelling | modelling: each zone's own rate over its observed months carried to the lost ones | keep |
| Failed protection sits inside the seasons since each zone's last inspection, so the zones to find sit in any baseline fitted on unverified seasons | constructed by the simulated theft (near towns), the failing arrester lot (Weibull ageing from 2017-18) and the cracking insulator batch, across every substation | no: 7.5 per cent of the not-yet-found-failed zone-seasons and 11.7 per cent of all carry failed protection; 19 zones carry it in 2026, 15 are referred, and the inspections found 26 failed zones the rule had not referred | modelling: which seasons can teach a sound rate, and the spread each fit set gives (size 22.8 on the confirmed seasons, 1.2 to 4.4 on wider sets) | modelling | keep |
| Sound zones scatter more than Poisson (each zone's susceptibility and each season's shocks) | constructed by the simulated susceptibility (sd 0.20) and season shocks (sd 0.12) on every zone | no: every zone | modelling (the field's negative binomial once the scatter is measured) | modelling, thin | keep as one of several; the careful pass earns it |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 lightning faults per season | Missed | Missed | Right |
| R2 radio-less zones, 2026 faults | Missed | Missed | Right |
| R3 2026 faults failed protection caused | Missed | Missed | Right |
| R4 zones referred for the 2027 refit | Missed | Missed | Right |
| R5 referrals after each season since 2022 | Missed | Missed | Right |
| R6 sound zones referred in a season | Missed | Partly | Right |
| R7 referrals against the following inspections | Missed | Missed | Right |
| R8 faults the refit avoids, average season | Missed | Missed | Right |
| Roughly | 0 of 8 | 0.5 of 8 | 8 of 8 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "a season counts as sound only when the next cyclic inspection found nothing"; rescues 3 of 8 results
Pair estimate: 16.2

The quick pass reads the OMS LIGHTNING code as the lightning record. The careful pass does everything the run record
says a frontier run does unprompted: it cleans every export, drops the re-read events, converts the lightning
extract's UTC, matches on a tight window where clocks are synchronised and on a ten-minute window around the
radio-less controllers' own stamps, counts the logged events, fits a negative binomial sound rate with every covariate
on every season no inspection has yet found failed, and reads the window, the budget and the false-referral sum
right. It is not graded up on the baseline: the confirmed-sound reading needs the time-order judgment (a clean
inspection proves the seasons before it, not after), and that move is the build's third difficulty. The risk the
build carries is a run that makes it without the reconstruction: priced on the same split, a wide window on the
confirmed seasons scores 50.7, a drift fit on them without the fill 53.5, a fixed offset on them 41.5; a run that
reconstructs the record and fits every unverified season scores 40.5. A run reaches the 80s only with both the
reconstruction and the confirmed seasons (81.0 with a Poisson spread, 100 with the golden's).

First-pass reading, 2026-11-11 (`determinism_check_report_pass2.md`): the stage 4 judge thread's own derivation, a
medium-effort run written before it opened the blocks, landed the 15 zones, the referrals after each season (11, 11,
13, 11, 15), the radio-less zones' 2026 faults (248), the faults failed protection caused in 2026 (254) and the
avoided faults (103) inside their bands, and four of the five season totals, in about seven minutes. It aligned the
radio-less clocks from the weekly battery tests, which the generator fires at 03:00 true time, so every test's stamp
gives its controller's offset away (a real controller runs its self-test at 03:00 on its own clock); it restored the
unread and overwritten months by exposure as a matter of course; and it took the seasons a later inspection found
sound as the baseline unprompted. Priced on that pass the careful column earns R2, R3, R4, R5 and R8 and part of R1,
about 73, so the 16.2 above does not stand and the build is back at stage 2. It lost only R6 (it wrote the 0.2
ceiling) and R7 (its scatter gave other counts).

## Data provenance

Source: generated by `task13/generator` from a simulated process
Behaves like the real thing: thunderstorm cells drift across the franchise and drop flashes of several strokes with
  lognormal peak currents; the lightning network detects each stroke with an efficiency that falls below about 4 kA
  and places it with an error ellipse, reporting cloud pulses beside ground strokes; each stroke near a line flashes
  it over by induction or by a direct hit at a rate set by the span's construction, the arrester cover and the state
  of its ground leads, arresters and pin insulators (losing grounds or arresters lifts a zone's lightning faults 2.5 to
  4.5 times, as line arrester studies find); breakers and reclosers run their trip, reclose and lockout sequences;
  radio-less controllers keep their own clocks and fixed-size memories, read and reset at site visits on a round of
  about four months; dispatchers log sustained outages with their own cause codes; crews inspect each zone once in
  five dry seasons and find about nine failures in ten; ground leads are stolen near towns, one arrester lot ages out
  from 2023 and one insulator batch cracks from 2020.
Genuine patterns: (1) the lightning season and the dry season (storms April to October, typhoons, inspections and
  most site visits December to May); (2) spatial structure (storm tracks, hills and towns, tree cover, construction
  types and the 2017-18 arrester programme); (3) overdispersion (each zone's susceptibility and each season's shocks);
  (4) stroke multiplicity and the current distribution; (5) the arrester lot's ageing and the insulator batch's
  cracking hazard; (6) theft falling off with distance from town
Problems by process: controllers' clocks drift and are reset when a technician reads them; fixed memories overwrite
  their oldest events under weekly battery tests and busy seasons; the months since a controller's last read are
  unread at the pull; every download re-exports the whole memory; the lightning extract runs in UTC with cloud pulses
  included; upstream breakers trip sympathetically on downstream faults; the SCADA history drops events during comms
  failures; dispatchers code causes by judgment; inspections miss about one failure in ten
Breadth: 12 files; 171 zones on 1,312 overhead routes, 46 of them on controllers read on site; 149,410 located strokes,
  38,782 SCADA events, 72,858 downloaded events from 710 reads, 2,925 outages, 342 inspections over two five-year
  cycles; every zone is reconstructed and scored every season, and which devices and which seasons to trust is work

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, modeling, exploration-triage, validation,
  uncertainty, validation, forecasting
Question form: what (the rule and the zones it refers)
Nearest build: task6 (events a store dropped, restored before a flagged set): there whole traces were kept at a known
  hourly rate and the weight sat on a hard-to-measure quantity; here the losses are each controller's own (an
  unknown drift, a memory that overwrites under load, months nobody read) and the weight sits on designing an alarm
  whose baseline only an independent check can verify, with the alert load, the false-alarm rate and the inspection
  check graded. Against mark119 (excess failures over expected per unit) there was one expectation and no record to
  repair; against task13 v1 nothing survives (a gust-load fit and a trim split on six feeders).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "lightning fault" | every trip; every fault start on the zone's device; faults the OMS codes LIGHTNING | each fault start whose first trip lines up with a stroke near the zone's lines, counted once against that zone | terms 2(c) (started by a flash on the zone's lines, counted once however many trips); the OMS records sustained outages only |
| SF2 | "near" (the lightning that fell near the lines) and the radius a fault is matched over | exposure within 400 m, 800 m or 1 km; matching within 300 m to 1 km | exposure within 400 m; matching within 400 m | terms 2(g) files the exposure (within 800 m or 1 km the set moves by 2 to 4); the matching radius is same call from 300 m to 1 km (checks.py SF2) |
| SF3 | "lightning season" | the calendar year; 1 April to 31 October | 1 April to 31 October | terms 2(b) |
| SF4 | "since its last cyclic inspection" | from the inspection's start; from the day after its repairs; the whole record | the day after the repairs were completed to the season's end | terms 2(e); the whole record refers 25 |
| SF5 | the seasons a sound rate is learned from | seasons a later inspection found sound; every season not yet found failed; every season | seasons a later inspection found sound | terms 2(d) makes soundness a state of the protection; only a later inspection records that state for a past season, and the book shows zones inspected clean and found failed at the next round |
| SF6 | "more than chance explains" | a Poisson tail; the sound zones' own scatter | the sound zones' own scatter (negative binomial, size 22.8) | the confirmed seasons reject Poisson (2 dlogL 4.95); Poisson refers 17 |
| SF7 | "no more than once in five lightning seasons on average" across the network | 0.2 a zone a season; 0.2 a season across the network | 0.2 a season across the network, 1/(5 x 171) a zone | terms 3(b) "Across the network" |
| SF8 | "how many of a season's referrals should be zones with sound protection" | the budget (0.2); the rule's own expected count | the rule's own (0.13) | the budget is a ceiling ("no more than", 3(b)); the ask is what the rule will do |
| SF9 | "the network's lightning faults in each season" | the faults the logs kept; every fault the season had | every fault, the lost and unread restored | terms 2(c) defines a fault by the flash, not by the record; the downloads' event numbers show events the memories lost |
| SF10 | "how many of 2026's were caused by failed protection" | the network less every zone sound; the referred zones' excess; each zone's positive excess summed | the network less every zone sound (279) | terms 2(f); the referred zones' excess (199) leaves out failed zones not yet referred, the positive parts (415) count chance on sound zones |
| SF11 | "how its referrals compare with what the next cyclic inspections found" | per referral (a zone-season); per inspection | per inspection, against the rule after the season before | terms 5 |
| SF12 | "a season of average lightning" | each zone's 2022 to 2026 mean; 2026's lightning scaled to the network mean; 2026 as it fell | each zone's 2022 to 2026 mean sound expectation (107) | terms 4(c); 2026 scaled to the network mean gives 109, same call; 2026 as it fell (133) is not an average season |
| SF13 | the CSV's "faults since its last cyclic inspection against what sound protection would have given it" | logged faults against the full-season expectation; restored faults against the full expectation; logged against the observed months' expectation | restored faults against the full expectation, which carries the same ratio as logged against the observed months | same call on the ratio and the referral by construction; logged against full understates the radio-less zones (SF9) |
| SF14 | which zones | the register's 171; the zones with SCADA | the register's 171 | terms 2(a) |
| SF15 | the count the chance is judged on | the faults the records hold against the expectation for the same months; the restored count against the full season | the records' own count | a restored count is an estimate (the zone's rate carried to months nobody recorded); a chance computed on it as if counted overstates the evidence, and it alone adds SRQ-F4-R3 (7 faults recorded against 2.1 expected in its recorded months) |
| SF16 | which of a zone's features the sound rate carries | any subset of the register's construction, area, arrester and transformer shares | the full set | the data: every subset within 4 AIC of the best on the confirmed seasons refers the same 15; every subset that refers otherwise sits 5 or more AIC worse (checks.py SF16) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the register's 171 zones (terms 2(a)); every zone scored after every season, none excluded |
| 2 | Unit of account: the protection zone; a fault counted once against the zone whose lines it was on (2(c)), an upstream breaker's sympathetic trip is not its zone's fault |
| 3 | Attribution window: a fault belongs to the season of its first trip (2(b)); the matched stroke and trip sit within a second, so no fault straddles a season's edge (C1) |
| 4 | As-of dating: the rule after the 2026 season, on the inspection book as it stands (rounds through 2025-26) and the register of September 2026 |
| 5 | Version basis: one register, one inspection book, no revised extracts; C1 |
| 6 | Denominator: the expectation is a rate times the strokes within 400 m in the zone's observed months (3(a)); the CSV's ratio divides by the sound expectation since inspection |
| 7 | Weighting: none; each zone-season enters the fit as a count with its exposure; the false referrals are summed over zones (3(b)) |
| 8 | Window length: the record since the last cyclic inspection (2(e)); the fit uses every confirmed-sound season of 2022 to 2026 |
| 9 | Boundary inclusivity: strict ("more than"); no zone sits near the threshold (weakest referred chance 2.9e-4, strongest unreferred 4.0e-3, threshold 1.17e-3; C1) |
| 10 | Rounding path: counts whole, the CSV to one decimal, each graded figure rounded once at the end at the precision the answer blocks state |
| 11 | Tie-break: none needed; no two zones tie at the threshold (C1) |
| 12 | Maturity and censoring: the radio-less controllers' unread months and overwritten events restored at each zone's own rate (R2); every SCADA zone's 2026 season is complete |
| 13 | Order of operations: match, then collapse each fault, then season, then fit, then threshold; the referral compares logged faults with the observed months' expectation, which carries the same ratio as the restored faults against the full season (C1) |
| 14 | Row order: no result depends on file order (every match sorts by device and time; C1) |
| 15 | Duplicate resolution: a re-read event (same controller, same event number) kept once; counting repeats moves no referral (checks.py R2) |
| 16 | Identity normalisation: every system keys the zone by its register name or its device point ("ZONE CB", "ZONE ACR", the recloser id), which map one to one |
| 17 | Netting against gross: R3 nets by definition (2(f)); a sound zone's shortfall offsets another's chance excess |
| 18 | Dimensional units: counts of faults and of strokes only |
| 19 | Code and status semantics: the register's telemetry label says which controllers are read on site; the OMS cause codes are not read by the golden |
| 20 | Integerisation: none in any computation; graded counts rounded at the end |
| 21 | Clause scope: 3(b)'s budget holds in every season the rule is run after, across the network; 4(c)'s average is each zone's 2022 to 2026 lightning |
| 22 | Forward window contents: 2027 is not observed; R8's season of average lightning is the 2022 to 2026 mean each terms 4(c) names, so no forecast of 2027's storms is needed |

## Literal reader

Terms 2(c) executed word for word on the device histories gives each zone's lightning faults only once each fault's
first trip is placed on the same clock as the lightning extract, which for the 46 controllers read on site means
fitting each one's clock from its own trips; 2(c) defines the fault by the flash, so the events their memories
overwrote and the months nobody has read are faults the season had (R1, R2). 3(a) asks for what the lines would have
had with sound protection under the lightning near them, and 2(d) makes soundness a state only a later inspection
records, so the expectation and its scatter come from the confirmed seasons (R3); 3(b) sets the threshold across the
network (R4, R5) and its own false referrals follow from the same tails (R6); 5 checks each inspection against the
rule after the season before it (R7); 2(f) and 4(c) define R3's and R8's quantities. Every literal reading gives the
golden's quantities; the hurried figures come from easier methods on the same estimands (a wide window, the logged
events, an unverified baseline, the budget quoted), never from another reading. No shipped sentence names a method, a
clock, a memory, a spread or the seasons a rate is fitted on.

## Prompt contract

A voice rewrite may not drop or change: the question (what rule to run after each lightning season to refer the
zones whose lightning protection has failed, and what zones it refers for the 2027 refit); for every zone, a CSV with
its lightning faults in each season from 2022 to 2026, its faults since its last cyclic inspection against what sound
protection would have given it, and whether it is referred; a short note with a chart giving the rule and the zones it
refers, how many zones it would have referred after each season since 2022, how many of a season's referrals should
be zones with sound protection, how its referrals compare with what the next cyclic inspections found, the network's
lightning faults in each season, how many of 2026's were caused by failed protection, and the faults the refit should
avoid in a season of average lightning. It must never add: a rounding instruction, a method or a comparison (clocks,
drift, memories, filling, the seasons a rate is fitted on, a spread, a window), a warning, an attached file's name, a
role, a count the data hold (171 zones, 46 radio-less reclosers, twelve substations), or a fact the files carry.

## Leak rulings

- leak.py 4 (design-note vocabulary) on the programme terms (record, seasons, referral, strokes): harmless; the terms
  define the season, the record since an inspection, what the rule refers and the lightning near a zone in the
  co-op's own words, and no sentence names a clock, a memory, the seasons a rate is learned from or a spread.
- leak.py 3 (400 in the terms): the exposure definition of terms 2(g), filed as a stated input in metadata.json, not a
  result.
- leak.py 11 (shell quota): a corpus count of other prompts' question form; this prompt asks what.

## Pre-ship check

Written at stage 5 against the built pack.

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
