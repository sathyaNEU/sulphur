# task13: what Blue Earth Valley Power's automated loops really avoided in 2026, what to change before the winter and the 2027 summer, and what they will avoid in 2027

## Draw

Subdomain: Energy Systems & Utilities, task type grid reliability and outage analysis (`grid-reliability-outage-analysis`, the only energy task type serving the assigned analysis type)
Analysis type: Anomaly Detection & Diagnostics
Answer shape: a bridge that reconciles two totals (the ADMS dashboard's 2026 "customer interruptions saved" walked to the
  sustained interruptions the automation really avoided, net of the ones its own switching caused), with the diagnosis
  of every loop, control and transfer direction under it and the 2027 forecast on top
Weight: a hard-to-measure quantity: what an automatic restoration scheme changed across the whole network is in no
  record; the ADMS archive holds what the scheme logged, minus what it lost on storm days, and none of what its
  transfers did to the receiving feeders hours later; the last two live builds sit on investigation (task7 v9) and
  metric or rule design (task9 v2), and architecture 3 sat on metric or rule design
Data-native sentence: a FLISR restoration is worth the customers it moves from a sustained interruption to a momentary
  one, less the customers its own switching then puts out, and whether a transfer holds depends on the coincident
  load through every protective device on the receiving path at the hours after the fault, while the archive that
  records the scheme loses its busiest days and the controls that carry it out are tested only in mild weather.
People: Shawn Hudson (manager of grid modernization performance, files the 2026 report with the commission), Nathan
  Reeves (distribution automation engineer, the golden's author), Elaine Stewart (system protection engineer), Jacob
  Barton (distribution operations superintendent), Debra Reed (regulatory affairs director, signs the filing),
  Ruben Nicholson (capital projects manager); drawn with `guard.py names --geo "United States"` at seeds 1341 and 1347;
  none is named in the prompt

**The decision.** Blue Earth Valley Power, an investor-owned distribution utility in southern Minnesota, runs 13.8 kV
feeders from nine substations; 44 of them are paired into 22 loops automated for fault location, isolation and
service restoration (a substation breaker, two midline reclosers and a normally open tie switch per loop, run by the
ADMS). The commission's grid modernization order has the utility report each year the sustained customer
interruptions the automation avoided. The vendor's dashboard reports a gross figure from the ADMS archive. Before the
March 2027 filing the utility must say what the loops really avoided in 2026, which loops, controls and transfer
directions are not performing and why, what it will change before the 2026-27 winter and the 2027 summer, and what the
loops will avoid in 2027.

**Card.** `.claude/skills/fingerprint/cards/task13.json`, architecture v4, registered 2026-11-11 (23:18Z), guard verdict
WARN. Answered: `repeat.decision` against task7 v9 (there one fund-or-not call per measure; here which controls to
re-battery and which transfer directions to run without summer auto-transfer, a designation unit by unit beside the
net figures); `repeat.deliverables` against task7 v9 (the commission's filing takes a PDF memo, and the workbook is the
engineer's); `skeleton.lesson_once` (downstream_offset is taught once, by the client's turbine-wake task 8ec45b05, as a
go or hold on one unit's repair; here it is netted across 44 transfer directions inside a chain of four lessons whose
other three no accepted task teaches); `skeleton.house_lesson` on validation_cannot_see_condition (mark258, task20 v2,
task7 v9) and linkage_missing_not_at_random (task16 v2, task19 v1): both are supporting judgments here, each priced on
its own result (the cold-crank controls; the storm days the archive lost), never the lesson the call turns on.

## Results chain (sketch at the draw; the full table at stage 2)

- R1 assembly and reconciliation: FLISR sequences on the 22 loops and the customers restored within five minutes, each
  year 2022 to 2026, with the sequences the ADMS archive lost on storm days restored from the outage record's
  restoration steps and the devices' own operation records; hurried: the archive taken as complete, or its gaps filled
  at the observed success rate (N10, N14), though the archive loses exactly the days the scheme fails most.
- R2 decomposition and attribution: 2026's bridge from the dashboard's figure to the net sustained interruptions
  avoided (the lost sequences, restorations after five minutes, closes onto mislocated faults, and the receiving
  feeders' midline reclosers tripping on the combined load hours after a summer transfer, coded no cause found);
  hurried: the restored loop priced alone (L16), or only the closes the log shows netted (L06).
- R3 investigation loops: 2025-26's failed and blocked restorations by cause (radio, control battery in the cold, fault
  indicator, capacity, scheme disarmed); hurried: every no-response timeout read as a radio fault (L26), though a
  control whose battery cannot crank browns out its own radio.
- R4 missingness and measurement: the controls to re-battery before the 2026-27 winter, read from weekly self-test sag
  against temperature carried to the design cold; hurried: the spring and autumn functional tests taken as proof of
  health (N11), the mild-season readings carried to the cold (N12), or the controls that failed in past cold snaps,
  most of which were re-batteried after failing.
- R5 causal reasoning: the transfer directions that must run without summer auto-transfer on 1 July 2027, from the
  receiving path's coincident load against its pickups at the storm hours faults strike, with 2027's load growth and
  the four reinforcements carried at the completion the capital works history supports; hurried: the plan's in-service
  dates taken as given (N03), or the 2025-26 trips counted direction by direction.
- R6 forecasting: 2027's net sustained interruptions avoided on the 22 loops with the changes, with its range;
  hurried: each shortcut above carried forward, on its own route.
- One-fact test: "a summer transfer can trip the receiving feeder's midline recloser hours later, with no fault found"
  rescues R2 and part of R5 (at most 2 of 6); the lost storm days, the cold-crank controls and the reinforcements'
  slip each carry their own result.

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
- Architecture 3 as a whole (Kalumpang Valley Electric Cooperative's lightning referral rule, READY at 17912c6 on
  2026-11-11): a platform run landed every result (task13/runs/run1.md: the same 11 zones, the season totals, the
  failed-protection count, the alert load, the inspection check and the avoided faults inside their bands): each zone's
  level as a random effect with its uncertainty in the predictive tail, the threshold checked by an all-sound
  simulation, the clocks rebuilt from upstream and downstream pairs on a whole-visit hold-out and the latest window for
  the refit were reflexes (precedents R26 to R32), and every assumption it named and waved through (the 2026 topology
  for all history, missing periods at the observed rate, a passed inspection as proof of soundness, the latest rate as
  the end state) was true in that world; the lightning world had spent two architectures, so architecture 4 moved to a
  new world, dataset and shell, each priced result built on one of those assumptions made false by the process.
- Architecture 4 at the draw, a distribution transformer fleet (EV overloads, a defective 2015-18 batch, the 2026 heat):
  its judgments sat on survival and thermal-ageing fits, the frontier run's home ground, and its decision was a list of
  some 300 units no rubric can grade; the FLISR fleet maps each priced result onto an assumption the run names.
- Architecture 4 at the draw, URD cable sections for a 2027 replacement programme: survival with left truncation,
  vintage and frailty, which the run fits by reflex; the decision a long list of sections.
