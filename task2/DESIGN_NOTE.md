# task2 architecture 6: the heavy-correction ceiling Larkmoor Speech commits to in Shannonside Hospital Group's 2027 quality schedule

## Draw

Subdomain: Robustness analysis (distribution shift, out-of-distribution generalization, calibration)
Analysis type: Descriptive & Distribution
Answer shape: a distribution and where it is cut (each 2027 quarter's expected share of audited dictations above 15 per cent word error rate against the four offered ceilings, the fourth quarter's 90th percentile), with the 2023 to 2026 record bridged beside it
Weight: hard-to-measure (the heavy-correction share of 1,549 clinicians who have never dictated and each university hospital's own effect on error, neither observed directly, both read through partial views: the volunteers, the smaller hospitals' whole staffs since their go-lives, and the clinicians who moved); redrawn at filing from modeling, which task10 v7 filed this morning; the last two live builds weigh allocation (task9 v8) and modeling (task10 v7)
Data-native sentence: the university hospitals' 2027 dictations come from staffs that are mostly not dictating yet, whose levels the record shows only through who chose to dictate there (the few it worked best for), through the smaller hospitals' whole staffs since their go-lives, and through the 248 moves the register records under a new staff number, while every past go-live switched over department by department across four months.
People: drawn with `guard.py names --geo ie --seed 5205` for this world: Jody Cahir, Yasmine Ganley, Colum Wallace, Pearce Stapleton, Alexander Sigerson, Kristopher McLoughlin.

## Deep reasoning

Task type: robustness analysis (distribution shift): a recognizer's tail error rate carried from the audited population to a deployment population the record never held.
Domain test: the results are the field's own objects for a shifted deployment: a tail share of a mixture of per-clinician error distributions, the transport of that mixture to a new population once selection into the audited sample and the setting's own effect are separated, the go-live exposure that weights it, and a bridge of the observed metric into model changes and population change.
Swap: "the lowest handle-time ceiling a contact-centre vendor can commit to" with handle times for error rates: the release steps measured within clinicians, the acoustic effect of a hospital, the selection into voluntary uptake and the switch-over all stop meaning anything, and a trend on an aggregate is what is left.
Where the weight sits: R4 and R6, the university hospitals' 2027 staffs: their levels are built from the smaller hospitals' whole staffs by grade and specialty, moved by each hospital's own effect (measured within the clinicians who moved), less what the volunteers already carry, then weighted by the switch-over; each piece is long, and each has its own tempting shortcut.
Layer 1: re-audited dictations with a first and an adjudicated score (QA-07 4); unscorable audio; the export's error rate as a fraction to 2024 and a percentage from 2025; release strings in three forms; the volume export for March and April 2025 run twice and both kept; staff numbers reissued on 248 moves between the group's hospitals (the register's previous_staff_no); the audit export holding only what had been scored by 8 January 2027. None decides a result on its own; the moves are load-bearing for R3 once linked.
Not one thing: the strongest single piece is each university hospital's own effect (R3); a run that nails it still has to build the staffs less their volunteers (R4) rather than borrow the smaller hospitals' compelled clinicians, weight the go-lives by the switch-over (R5), and bridge the record within clinicians (R2); with R3 alone and the compelled rate the fourth quarter passes 16.
One-fact test: the most useful single sentence is "the hospitals' own effects on error show in the clinicians who moved between them"; it rescues R3 alone (1 of 9), because the starters' rate, the switch-over and the bridge each need their own work. The nearest rival sentence, "the university hospitals' low rate is who chose to dictate, not the place", points a run at the smaller hospitals' whole staffs but without each hospital's own effect, which files the fourth quarter at 11.4 and Ceiling B; it rescues none of R4 to R9, which need R3, R4 and R5 together (the carry-forward), and it moves only the direction of the call.
Not semantics: every field, code and clause read correctly still leaves the record carried at 9.0 per cent, the university hospitals at their volunteers' 4.1 and 4.4 per cent, and the starters at whichever comparison group looks closest; no definition says who the starters resemble, how a hospital moves a clinician's error, or how a go-live ramps.
Not rule application: no filed procedure projects 2027 (Schedule 4 defines the metric and the ceilings, Schedule 2 and the rollout plan the dates and staff, SN-2026-14 the frozen release, QA-07 the audit); the hospital effects, the starters' rate, the switch-over and the bridge are estimated from the record.
Estimand: the share of each 2027 quarter's audited dictations with a word error rate above 15 per cent, every dictation made under the service in the quarter including those of clinicians not yet dictating on the as-of date (Schedule 4.2), and the lowest offered ceiling no quarter passes (Schedule 4.3); each university hospital's expected fourth-quarter share and Ballykeel's fourth-quarter dictations on the same basis; the fourth quarter's 90th percentile of dictations (the prompt); the change in the audited share from the second quarter of 2023 to the last of 2026, split into the releases and everything else (the prompt).
No decoy: nothing is written to carry a wrong answer: the quarterly reports state the record truthfully, the release notes label LCB-2 as Larkmoor's own benchmark, no memo or thread carries a 2027 figure, a hospital effect or a starters' rate.
No replay: no result re-derives a published figure; R1 ties to the quarterly reports as a check and decides nothing.
Pinned: every rival a careful analyst would run is run on the cut pack (`generator/checks.py`): first-pass scores, quarters by audit date, the dictators' rate from every audit carried by its release step, population cells by grade alone, the population from every clinician dictating after a go-live, the population read straight off the smaller hospitals' audits by grade, no calendar adjustment, the ramp from the four go-lives since 2023 and volume from six months all land every graded figure inside its band; the hospital effects agree with a joint three-way fit within 0.3 points; the fits on release 6.0 or on 2025 and 2026 alone are ruled out by named data (4 and 11, then 14 and 35, clinicians seen at two hospitals against 36 and 64); unlinked staff numbers leave no clinician at two hospitals.
Run forecast: R2 lost by a method shortcut (the change put to the releases, the LCB-2 cuts or a shift-share by hospital); R3 by stopping at the first story (the university hospitals' volunteers read as the place); R4 by a narrow look (the smaller hospitals' compelled clinicians taken as the closest group, as both architecture 5 runs did); R5 by a method shortcut (full volume, or each clinician's own first months, from the date); R6 to R9 fall with them, at different calls.
Strategy label: Heterogeneity that pooling hides, carried to the population the decision serves, with selection into the observed sample and the setting's own effect separated (`references/sulfur-strategies.md`, Machine Learning Research); the clean-comparison lesson enters through the moves.
Depth level: 4, reaching 5: four independent judgments (the hospital effects through the moves, the staff less its volunteers, the switch-over, the releases within clinicians), the call needing the first three at once; the shortcuts land on four different wrong calls (10 from the record, 12 without the hospital effects, 16 from full-volume go-lives, none from the compelled clinicians' rate), and the call holds across the rivals' sweep (the fourth quarter 12.9 to 13.0).
Lesson: a deployment population reached by compulsion is neither the self-selected users on record nor the hard core who held out elsewhere, and the place it moves into has its own effect that only the clinicians who moved can show; carried with the go-live's exposure, three corrections are needed together, and none alone lands the call.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the group's audited share in the second quarter of 2023 (10.1 per cent) and the last of 2026 (7.8), from the cleaned audits tied to every quarterly report | assembly-reconciliation | QA-07 3 and 4 (the adjudicated score, unscorable out, the rate from the counts); quality_reports_2023_2026.xlsx | each end within 0.1 | method shortcut: the first-pass score kept where a dictation was re-scored, every quarter moving off the reports | - | Ask 7 |
| R2 | the change split: the releases about -4.1 points, everything else about +1.9 | decomposition-attribution | the releases measured within each clinician's stay at one hospital; the prompt's window | releases -4.7 to -3.5, the rest +1.2 to +2.5 (the two orders) | method shortcut: the whole change put to the releases (-2.2), the release notes' LCB-2 cuts (-5.9), a shift-share by hospital (-1.7) or the jumps at each release month (-2.1) | R1 | Component 4 |
| R3 | each university hospital's own effect on a clinician's word error: Shannonside University +5.0 per cent, Ballykeel +8.6, against the six smaller hospitals' average | investigation-loops | the register's previous_staff_no (248 moves; 36 and 64 clinicians audited at a university hospital and another) | 3.5 to 6.5 and 7.0 to 10.0 | stopped at the first story: the university hospitals' current dictators (4.1 and 4.4 per cent heavy correction) read as the best places to dictate, or no hospital effect at all | - | Component 1 |
| R4 | the heavy-correction share of each university hospital's 2027 starters: 18.2 and 21.7 per cent | causal-reasoning | the register's staff in post on 31 December 2026, the rollout plan's count; Schedule 4.2's population | 17.0 to 19.5 and 20.5 to 23.0 | narrow look: the smaller hospitals' compelled clinicians (27.7 per cent) taken as the closest group, though uptake there ran 58 to 87 per cent and the university hospitals' starters are most of their staff | R3 | Component 2 |
| R5 | Ballykeel University Hospital's fourth-quarter dictations: about 88,000 | missingness-measurement | the six past go-lives in dictation_volumes_2022_2026.csv; the register's staff in post | 85,000 to 91,000 | method shortcut: every starter at full volume from 1 October (161,000), or at their own first months' volume from the date (133,000) | independent: the six past go-lives' volumes and the register's staff in post | Ask 5 |
| R6 | each university hospital's expected fourth-quarter share: Shannonside University 14.9 per cent, Ballykeel 12.9 | forecasting | SN-2026-14 (release 6.0 through 2027); Schedule 2's dates; the staff in post held as on 31 December 2026 | 14.3 to 15.5 and 12.3 to 13.5 | unfinished chain: a hospital effect left uncarried (12.5 and 10.0), or the starters at the compelled rate with every clinician starting on the date (22.1 and 19.8) | R3, R4, R5 | Ask 4 |
| R7 | each 2027 quarter's lowest ceiling: 10, 12, 12 and 14 per cent | forecasting | Schedule 4.2 and 4.3 | exact | method shortcut: the 2026 share carried (10, 10, 10, 10) or the compelled rate (12, 14, 16, none) | R6 | Ask 3 |
| R8 | the word error rate nine in ten fourth-quarter dictations stay under: about 16.1 per cent | modeling | the prompt's "dictations" | 15.8 to 16.3 | method shortcut: read off clinicians' typical levels (13.5), dropping each clinician's own scatter | R4, R5 | Ask 6 |
| R9 | the ceiling: 14 per cent (Ceiling C), 10 passed from the second quarter and 12 in the fourth | synthesis | Schedule 4.3 (the lowest offered ceiling no quarter passes) | exact | method shortcut, a different wrong call by route: 10 from the record, 12 without the hospital effects, 16 from full-volume go-lives, none from the compelled rate | R7 | Recommendation |

Carry-forward: R1, R3 and R5 stand on inputs of their own (the reports, the moves, the past go-lives); R2 needs only R1's cleaning; R4 falls with R3; R6 needs R3, R4 and R5 together, so a run that gets any one of them right still misses R6 to R9, and a run that misses one keeps the others; R8 falls with R4 and R5, R7 and R9 with R6.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| selective uptake: who chose to dictate is who it worked for | constructed (simulated adoption on each clinician's own trial) | no: every hospital's voluntary period, six followed by a go-live in the record at uptakes of 58 to 87 per cent, the university hospitals at 13 and 15 | modelling (the chose, compelled and hired shares against each hospital's uptake; the whole staff less the volunteers) | modelling | keep |
| each hospital's own acoustic effect | constructed (simulated per hospital) | no: all eight hospitals, the six smaller from -5.4 to +5.5 per cent | modelling (within-clinician comparisons through 248 moves, 103 clinicians audited at two hospitals) | modelling | keep |
| the department-by-department switch-over | constructed (simulated waves over four months) | no: all six past go-lives | a targeted query (volume per clinician in post by month from each compulsory date, the calendar out) | modelling (the curve measured and carried to two go-lives) | keep |
| the release steps | constructed (each release a factor on every clinician) | no: every clinician on record | modelling (within each clinician's stay) | modelling | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the audited share at the bridge's two ends, from the cleaned audits tied to the quarterly reports | Right | Right | Right |
| R2 the 2023 to 2026 change split into the releases and the mix of dictations | Missed | Right | Right |
| R3 each university hospital's own effect on a clinician's word error, against the six smaller hospitals | Missed | Missed | Right |
| R4 the heavy-correction share of each university hospital's 2027 starters | Missed | Missed | Right |
| R5 Ballykeel University Hospital's fourth-quarter dictations | Missed | Missed | Right |
| R6 each university hospital's expected fourth-quarter share | Missed | Missed | Right |
| R7 each 2027 quarter's lowest ceiling | Missed | Missed | Right |
| R8 the word error rate nine in ten fourth-quarter dictations stay under | Missed | Missed | Right |
| R9 the ceiling | Missed | Missed | Right |
| Roughly | 1 of 9 | 2 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "The hospitals' own effects on error show in the clinicians who moved between them."; rescues 1 of 9 results
Pair estimate: 26.0, the careful but hurried pass calibrated to this world's last platform round (both runs typed clinicians on sight, split the compulsory starters by appointment and gave the university hospitals' starters the incumbents' rate, one starting every go-live at full volume and one at each clinician's own first months)

## Data provenance

Source: generated by `task2/generator/world.py` from a simulated process (seed 60607): each post's occupants, their grades, specialties and own recognisability, adoption by each clinician's trial, moves within the group under a new staff number, each hospital's acoustic effect, the switch-over at each go-live, four releases, monthly dictations and QA-07's random 2.5 per cent audit with adjudication.
Behaves like the real thing: speaker-dependent recognition error that is lognormal within and between speakers, release gains that apply to every speaker, adoption that selects on how well the system works for the user, setting effects from room acoustics and workflow, and phased clinical go-lives; the audited share moves between 7.8 and 11.3 per cent over sixteen quarters with no quarter since the middle of 2024 above 10.
Genuine patterns: (1) release steps (4.0 about 1.7 per cent, 5.0 about 6.1, 5.2 about 2.2, 6.0 about 2.7, within clinicians) (2) selective uptake that differs by hospital (58 to 87 per cent at the smaller hospitals, 13 and 15 at the university hospitals) (3) each hospital's own acoustic effect (4) grade and specialty differences in error and in dictation volume (5) a calendar pattern in dictation volume (August and December low) (6) the switch-over waves at every go-live (7) turnover of about nine per cent a year and moves between hospitals.
Problems by process: the second scoring and adjudication (QA-07 4); unscorable audio; the audit export's unit change at the 2025 format change; three release string forms across two export formats and the adjudication rows; the volume export re-run for March and April 2025 with both runs kept; a new staff number at every move; audits scored after 8 January 2027 missing from the export.
Breadth: 13 files (two CSVs of 76,166 and 81,519 rows, five workbooks, five PDFs, one Word document), eight hospitals, 4,408 posts, 72 months of volumes, 48 months of audits; three distractors (the service desk tickets, the headset inventory, the EHR integration uptime).

## Template check

Chain signature: assembly-reconciliation, decomposition-attribution, investigation-loops, causal-reasoning, missingness-measurement, forecasting, forecasting, modeling, synthesis
Question form: how much (how low a ceiling)
Guard at filing (remote corpus, 2026-11-10): WARN only, overuse.weight against task3 v7 (a rare-event level carried between basins, nothing of selection or place), overuse.domain and overuse.gate_g; three axes redrawn at filing because task9 v8 and task10 v7 filed after the draw now hold them: the weight (modeling to hard-to-measure, the honester label for the heaviest results), the context artifact (close_out_summary to monitoring_export, the QA-07 audit export the head of quality works from) and the forcing event (launch_or_rollout to purchase_order_or_contract, the schedule returned by 15 January 2027).
Nearest build: task17 (General Statistics, Descriptive & Distribution, a distribution cut): its chain is a queue simulation fed by four fitted inputs with a back-test and an uncertainty band; here the weight sits on transporting a population across selection and place, with a bridge and an exposure ramp, and no simulation. The lineage's architecture 5 typed clinicians by start against the compulsory date as its one step; that typing is now texture every run does.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "share of audited dictations" | among the audited; among all dictations | the audited, expected | same call: QA-07 1, a random sample within hospital and month |
| SF2 | word error rate | the export's column; the counts over the reference words | the counts | same call: QA-07 3; the column agrees once its units are read |
| SF3 | a re-audited dictation | first pass; adjudicated | adjudicated | same call, asserted: every graded figure inside its band |
| SF4 | a quarter | by dictation date; by audit date | dictation date | same call, asserted |
| SF5 | "above 15 per cent" | strictly above; at or above | strictly above | same call: Schedule 4.1 |
| SF6 | the 2027 population | every dictation under the service; today's dictators | every dictation, the compulsory hospitals included | Schedule 4.2 |
| SF7 | the release in 2027 | 6.0 throughout; a 2027 release | 6.0 | SN-2026-14 |
| SF8 | "passing" a ceiling | above it; at or above | above | same call: Schedule 4.3 |
| SF9 | the staff in post through 2027 | held as on 31 December 2026; the record's turnover with replacements at full volume | held, a leaver replaced like for like | the rollout plan counts the staff on the HR system at 31 December 2026; a replacement hired before a go-live switches over with the department |
| SF10 | the ramp's go-lives | all six; the four since 2023 | all six | same call, asserted |
| SF11 | the dictators' rate under 6.0 | their 6.0 audits; every audit carried by its release step | 6.0 audits | same call, asserted |
| SF12 | "the word error rate nine in ten fourth-quarter dictations stay under" | of dictations; of clinicians' levels | dictations | the prompt's "dictations" |
| SF13 | the population's cells | grade and specialty; grade alone | grade and specialty | same call, asserted |
| SF14 | moves between hospitals | linked through previous_staff_no; left unlinked | linked | asserted: unlinked, no clinician is seen at two hospitals and the hospital effects cannot be measured |
| SF15 | the audits the hospital effects rest on | every audit with its release step; release 6.0 alone; 2025 and 2026 alone | every audit | named data: 4 and 11, or 14 and 35, clinicians seen at two hospitals against 36 and 64 |
| SF16 | the ceiling | the lowest offered at or above every quarter; the share rounded up | the lowest offered | Schedule 4.3 offers four ceilings |
| SF17 | a dictator's settled volume | the last three months; the last six | three | same call, asserted |
| SF18 | the population's members | the smaller hospitals' December 2026 staff; every clinician dictating there after a go-live | December 2026 | same call, asserted |
| SF19 | the population's levels | the error model's cells; the smaller hospitals' audits by grade | the model | same call, asserted |
| SF20 | the bridge's order | the two orders averaged; either order | averaged | the band spans both orders |
| SF21 | the bridge's window | the second quarter of 2023 to the last of 2026 | as stated | the prompt |
| SF22 | a hospital's own effect | against the six smaller hospitals' average; against one hospital | the six's average | the answer blocks state the basis |
| SF23 | the calendar | dictation volume adjusted for the month; unadjusted | adjusted | same call, asserted |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | every dictation under the service in each 2027 quarter, the not-yet-dictating staff included: Schedule 4.2 (SF6) |
| 2 Unit of account | the audited dictation: Schedule 4.1 |
| 3 Attribution window | calendar quarters by dictation date: asserted (SF4) |
| 4 As-of dating | the record to 31 December 2026; the schedule returned by 15 January 2027: the draft schedule |
| 5 Version basis | the adjudicated score: QA-07 4 (SF3) |
| 6 Denominator | a quarter's audited dictations: Schedule 4.2 |
| 7 Weighting | each dictation alike: Schedule 4.2 |
| 8 Window length | four 2027 quarters; the bridge from 2023 Q2 to 2026 Q4: the prompt |
| 9 Boundary inclusivity | above 15 per cent; a ceiling passed when the share is above it: Schedule 4.1 and 4.3 (SF5, SF8) |
| 10 Rounding path | none dictated by the prompt; each figure stated once in the answer blocks with its band |
| 11 Tie-break | none needed: one ceiling is the lowest at or above the highest quarter |
| 12 Maturity and censoring | none: 2027 is projected whole; audits scored after 8 January 2027 are out of the export and of every figure |
| 13 Order of operations | levels, then the staff, then the switch-over, then the share: every order asserted to the same figures |
| 14 Row order | no rule reads row order |
| 15 Duplicate resolution | the volume export's repeated rows once; re-audits by the adjudicated score |
| 16 Identity normalisation | staff numbers linked through previous_staff_no (SF14) |
| 17 Netting against gross | none in the metric |
| 18 Dimensional units | the error rate as a fraction or a percentage by export format, read once |
| 19 Code and status semantics | three release strings read as one release |
| 20 Integerisation | dictations stated to the nearest thousand with their band |
| 21 Clause scope | Schedule 4 covers every hospital in Schedule 2 |
| 22 Forward window contents | the go-live dates (Schedule 2, the rollout plan), the staff in post (the register and the rollout plan), release 6.0 (SN-2026-14) |

## Literal reader

Executed word for word, the prompt and Schedule 4 give the golden: the ceiling is the lowest of the offered ceilings that no 2027 quarter's share of audited dictations above 15 per cent passes, every dictation made under the service in the quarter counts (the university hospitals' staff from Schedule 2's dates, the rollout plan's count of staff in post), recognition stays at release 6.0 (SN-2026-14), each university hospital's fourth-quarter share and Ballykeel's fourth-quarter dictations are read on the same basis, the percentile is of dictations, and the bridge runs from the second quarter of 2023 to the last of 2026 with the releases' part and the rest; every convention the projection needs has a fork row closed by a filed sentence, a named count, or an assertion that every graded figure stays inside its band.

## Prompt contract

A voice rewrite may not drop or change: the question (the lowest heavy-correction ceiling Larkmoor Speech can commit to); the ceilings offered (10, 12, 14 and 16 per cent in Shannonside Hospital Group's draft 2027 schedule); the deciding outcome (no 2027 quarter's share of audited dictations above 15 per cent word error rate passing it); a short memo opening on the ceiling and the first quarter that would pass each lower one, with a chart of each quarter's expected share against the ceilings; a workbook with each quarter's lowest ceiling, each university hospital's expected fourth-quarter share, Ballykeel University Hospital's dictations in that quarter, the word error rate nine in ten fourth-quarter dictations stay under, and how much of the change in the group's audited share between the second quarter of 2023 and the last quarter of 2026 came from the recognition releases and how much from everything else. It may never add a rounding instruction, the compulsory dates, the go-lives, the moves or staff numbers, voluntary or compulsory use, selection, a hospital's own effect, the switch-over or a ramp, a release step, a projection, a mix, a count of hospitals or clinicians, or any hint that the record hides a change.

## Leak rulings

`leak.py --asof 2027-01-11` (REVIEW, no LEAK), each line ruled in the main thread:

- QA-07_recognition_quality_audit.pdf, 2.5: the audit's sampling rate in the procedure's own words; no result is a sampling rate. Harmless (the reader agrees).
- draft_schedule4_quality_2027.docx, 4.1: a clause number of the schedule; it matches the dictators' share and the releases' part only by coincidence. Harmless (the reader agrees).
- recognition_releases_2023_2026.pdf, 7.8: LCB-2's cut for release 5.0, equal to the 2026 Q4 audited share by coincidence; the release step the golden measures within clinicians is 6.1 for 5.0 and 10.6 for 4.0 to 6.0, none of them a benchmark figure. Harmless.
- recognition_releases_2023_2026.pdf and service_notice_SN-2026-14.pdf, 6.0: the release's name. Harmless.
- QA-07_recognition_quality_audit.pdf, design-note vocabulary (record, release, clinician): the procedure's sampling, scoring and adjudication in its own words; it names no kind of clinician, no hospital effect and nothing of 2027. Harmless.
- draft_schedule4_quality_2027.docx, design-note vocabulary (hospitals, record, clinician): 4.2 files the population (every dictation under the service, compulsory hospitals included), the WHAT the literal reader executes; it says nothing of who dictates worse or why. Harmless.
- services_agreement_schedule2_deployment.pdf, design-note vocabulary (hospitals, record, clinician): the contract's dates and its compulsory-use term; it says who dictates, never how well. Harmless.
- prompt.txt, two stump terms in one sentence: the deliverables sentence asks for the results themselves (quarters, ceilings, the university hospitals' shares); it names no method. Harmless.
- shannonside_dictation_rollout_2027.xlsx, three 2027 dates: the go-live and training dates the forward call needs, planned before the as-of date. Harmless (the reader agrees).
- The reader's realism nit (the quality reports' shares stored to sixteen digits) is fixed in the generator: the reports hold each share to four decimals.

## Pre-ship check

- Free gates on the final cut: generator checks 51 of 51, `figures_check.py` 0 absent, `precut.py` exit 0 (2 WARN: R3 upstream of five results, which `effort.py`'s largest hint shows no single sentence exploits; nearby chains on file), `effort.py` exit 0, `voice-check.py` exit 0 with no rounding instruction, `leak.py` REVIEW with no LEAK, `audit_containers.py` 0 FAIL, `guard.py surface` exit 0, `guard.py heart` WARN on the remote card corpus, two byte-identical builds.
- The leak reader (one isolated Sonnet read of the prompt and the pack): no method sentence beyond the filed WHAT, no ranking or helper file, no answer-like figure, the filed sentences execute to the golden, and no one thing settles most of the asks; one realism nit fixed (the quality reports' shares to four decimals).
- The determinism judge, run under the current protocol (the thread derived blind, then opened the blocks): DETERMINISTIC, APPROVE; Gate G analytical_non_defect with no surface-read dependency; Gate H one_thing none, stump power spread across at least three independently failable steps. An earlier pass the same day, under the older protocol, also returned DETERMINISTIC and APPROVE; its polish items are applied (the mover filter cut from Critical Component 1 as incidental, the one-fact line answering the rival hint).
- The thread's blind first pass priced against the careful column: inside its band only R1 (the record's ends, 10.06 and 7.82); Shannonside University's fourth quarter 4 to 6 per cent (the volunteers read as the place), Ballykeel's fourth-quarter dictations 1,600 to 2,300 (the audit sample read as the dictations), the percentile 17 to 20, no figure for the bridge's split, the ceiling undecided between 12 and 14. R1 is already Right in the careful column, so the pair estimate stays 26.0.
- The judge's hand-check: the selection insight alone (the staff less its volunteers, no hospital effect) is the generator's no-hospital-effect route, which files 11.4 in the fourth quarter and Ceiling B; it moves the direction of the call, not the call.
- A caution on the paper estimate: a medium-effort blind pass is not a platform run; the platform's two runs are the measurement.

## Tried and rejected

- The seed's own quantity (the Medicaid gap on the "would recommend" top-box rate across a state report's hospitals), every route screened at the draw: composition and patient mix settle the comparison population (WHAT screen); shrinkage of small cells repeats task253; design weighting repeats task264's lesson and task268 v2's reflex; nonresponse either fails determinacy or repeats the inverse-probability weighting of task264, task267 and task268; survey mode effects belong to Experiment & Causal Analysis; misclassification is the spent sensitivity-and-specificity family; nowcasting the late returns repeats task181; telescoping sits next to task453.
- A race-probability (BISG) regression for the equity gap (prototype `p1.py`): a strong ladder, but the same linear unmixing of a mixed population as task263, a clone of its driver.
- Traffic count factor groups for an annual average (prototype `t1.py`): count differences of one or two units at tiny margins, and the ground overlaps task474.
- The sequence effect at queues of 4 to 14 determinations with effects of 2 to 13 points (`s1.py`, `s2.py`): the two corrected estimators (the excess over reordering by counts, the held-day slope less its reordering expectation) disagreed on 1 to 3 hospitals a seed, with the closest margins 0.01 to 0.3 points; the queues were lengthened and the effect hospitals separated from the line.
- Effects of 12 to 17 points (`s4.py`, `s5.py`): the family agreed, but the day's rate without the pair as a control landed 10 or 11 of the 11 hospitals, its bias of 3 to 5 points smaller than the gap to the line; the effects were lowered to 9.5 to 12.5 with a wider day mix (`s6.py`), where it lands 9.
- Ask B as presumptive approvals with nightly re-runs replayed under fresh application numbers (D1): dropped at stage 2, because no asking sentence makes the count determinate without naming the device (a replay is a fresh application record, so "each application once" counts it, and any wording that excludes it narrates the re-run); replaced by the reason list renumbered on 1 July 2025 (D2).
- Queues of 6 to 28 a day with counsellors sitting on 55 percent of working days: the held-day route filed 28 of 31, an answer a reader distrusts on sight; queues of 8 to 32 on 48 percent of days put it at 23 with the family still closed (1.81 points).
- Effects of 9.5 to 12.5 points with the day's rate over the other determinations as a reflex: it landed the golden set (the others' count is the day's sufficient statistic), so it was moved into the family and the construction made every member agree, rather than the world bent to break it.
- Architecture 1 (each counsellor's sequence effect measured against the reordering of each working day's own determinations): spent at stage 4, both scored readers corrected the within-day contrast for the short-queue bias by permuting each day's determinations and landed the 11; a decisive step that is a named small-sample bias correction falls to a reader who knows the bias by name, however the ladder below it is tuned.
- The outcome "did not get free care in full" (a denial or any discount below 100 percent): noise in the year-round households' calendars inflated the shares at the 200 percent line, where the 2025 policy's full-care boundary sits on the eligibility line; the outcome moved to owing more than half of the balance (a denial or a 25 percent discount), whose policy boundary at 300 percent no year-round household's pay crosses.
- Households timing their applications to a low quarter (selection on the quarter): dropped in the prototype, no separation the seasons did not already give.
- Every hospital's designed share at 7.5 or 4.5 percent (the first build of this architecture): under the golden calendars 13 hospitals landed between 7.50 and 7.56 percent and 8 between 4.50 and 4.54, a cluster that confirms the golden route to a reader trying several calendars and reads as made in the chart; the designed shares were spread to irregular values, and the three set below what misassessment alone gives them (H04, H07 and H27, which then denied almost no one for documents) were raised to 4.29 to 4.68.
- Flat pay for year-round households and a fixed seasonal shape (the first builds of this architecture): a household's repeat applications carried the same three-month total to the cent, which reads as made; pay now rises unevenly from year to year and varies month to month, a household reapplies when its work takes its pay down (the season it knows) rather than on a month's luck, and the fixed-effects member falls back to a cell's month means where the cell does not identify its own calendar (the Olympic Peninsula's resort households: left unadjusted there, it had read H28 at 6.31; the reapplication change did not move that figure, the missing cell did).
- Also weighed at the re-root draw and dropped before any prototype, no reasons written down at the time: CGM, cash fills, TTR, a hungry-judges time-of-day effect, and heaping (already on file as spent in this lane).
- Architecture 2 (each household's twelve-month income rebuilt from the 2025 policy's quarter through its region's calendar for its kind of work): spent at stage 4, both scored readers read criteria 2.3's twelve months against the guide's three months times four, fitted a seasonal profile per hospital or region and kind of work and landed the 16; a decisive step that answers a gap the documents state outright falls to a reader who reads both documents, however finely the calendar has to be cut.
- Screens run at the architecture 3 draw on 2026-10-21, each set aside with its record. None cleared, so the number retires.
  - Demand censored at a stock or a capacity: task18, task108, task147, task168, task133, task141, task120 and task179 record it as spent.
  - Event times known only between periodic inspections, or at a single inspection: task476's leak starts, and the onsets set aside at task270's draw.
  - A share past a line taken from model predictions with their error added back, as in poverty mapping or an exposure model's Berkson error: task123 records it as task253's insight, task185 measured the exceedance route dead on the lever against the plug-in, and task143 records a strong analyst adding the stated validation error by reflex.
  - Realised variance against microstructure noise: task270 and task271.
  - A hot deck whose donor cells leave out the grouping variable, pulling each group's imputed earnings toward the other groups': dropping the allocated values is the filter route the partial-coverage screen kills, and reweighting the respondents within cells is task253 v1's nonresponse adjustment within classes.
  - Immortal time, and the period-analysis estimate of current survival: both are delayed entry into the risk set, task265's lesson.
  - A point-in-time count's elapsed durations turned into a year's flow: length bias, task264's size-biased sampling.
  - Recall decay across a survey's recall period: the latest month is a filter route and the decay form forks; telescoping sits next to task453.
  - Persistence beyond a panel's span by a mover-stayer chain: mover-stayer, latent Markov and second-order chains extrapolate apart.
  - Bunching below the free-care line: the counterfactual density's degree, window and bin width are open.
  - The own-children estimate of fertility, and extinct-generation old-age death rates: named methods, each with an open adjustment; the second was set aside at task271's re-root.
  - A closing auction's own impact net of the liquidity its imbalance drew: task197's design, abandoned there on the taxonomy; here, which offsetting orders were responsive is a judgment no record settles.
  - Roll-call ideal points: task269 and task270.
  - The tail of a sum of correlated parts by simulation: each unit's recorded totals are a filter route.
  - Minimum-night-flow leakage through the night-day factor: no utility task type serves Descriptive & Distribution Analysis.
  - Medication persistence, pharmacology's one Descriptive task type, set aside at task270 and task271: the reverse waiting time forks, and the new-user washout is a WHAT.
  - The Fair Assistance world itself: its quantities are filed rules once its two estimation hooks (a counsellor's sequence effect, a season inside a quarter) are spent. Its presumptive-screen incomes are the Berkson case above, and take-up through verified applicants is the transported error-rate family (task192, task267).
- Architecture 2 retired by this session's batch audit (2026-10-31), short of the survivor anatomy the approved builds share: its actor had a column (every application named the main earner's kind of work) and its link was stated outright (the criteria's twelve months against the guide's three months times four), so only the field's-method rung held; it is re-rooted, not repaired, so the portal sees one strong build.
- 2026-10-31, at the architecture 3 draw: a clinic medication refrigerator's product temperature rebuilt from the
  building system's air probe through each model's thermal response, calibrated on pilot units carrying a buffered
  probe (the card first drafted): the same insight as task482 v8 (a slow quantity carried through a lag measured on a
  short overlap), spent there at stage 4 because two records of one unit side by side are compared on reflex.
- 2026-10-31, at the architecture 3 draw: the drift-between-resets stump in a precision machining plant (inserts
  wearing between tool changes, hand checks at intervals, containment sorts): the guard banned the organisation
  family (manufacturer, task482 v16 in the last three builds) with the context artifact and the forcing event; the
  hospital pharmacy's compounding unit carries the same structure honestly.
- 2026-10-31, at the architecture 3 draw, set aside before any prototype: an assay's drift between calibrations read
  from quality control (task274's calibration-specific bias on an immunoassay sits too close); hypochlorite decaying
  between deliveries at small water works (operators' grab samples land in most low spells, so the sampled share
  files nearly the golden); a dental milling centre's burs (every crown is seated on its die before release, so the
  checks are not sparse); medication adherence, roll-call ideal points and small-area opinion (rules, spent, or an
  open model specification); low-depth genotype calls (a named reflex).
- 2026-11-01, at the build: weighing every fortieth dose: the long sets' tails were weighed and caught, so the
  weighed share and the sorts filed nearly the golden; the procedure weighs the first dose of each batch and then every
  hundredth syringe or twentieth bag, and the long sets' tails fall after the third batch's last weighed dose.
- 2026-11-01, at the build: the start fixed per set as the golden: one or two weighed doses per set make the start
  noisy and inflate the tails (piperacillin-tazobactam crossed 10 at 20.4 against a truth of zero); the golden takes
  the start as varying about its mean, and the bag sets start high so that no member of the family puts a bag near
  the line.
- 2026-11-01, at the build: a third ask, each product's mean delivered volume in each quarter: the gross and net
  weights are in the register's own headers and the specific gravity in the procedure, so a careful solver banks it;
  dropped, and Ask A moved to months, whose fill times carry no zone.
- 2026-11-01, at the build: bag sets ending lower (a start of 2.05 and a five per cent loss) to break the
  lowest-weighed-dose ordering: ampicillin crossed 10 under the golden and the family split; reverted, and the
  ordering is recorded as a WARN in the Readability screen.
- 2026-11-01, at the build: seeds where a pooled Johnson SB fit to the weighed doses files the four (27203, 27235,
  27251, 27259 of the ten screened): the seed was chosen where it does not (27267, cefazolin 2 g at 0.4); a bounded
  fit lands only when the long sets' third batches leave a visible shoulder in the weighed doses, so this is the rung
  to watch at stage 4.
- 2026-11-07, Domains Fit return (the prompt read as PH-QP-07's 10 per cent rule applied to rates, with counting asks): the prompt now asks for each product's estimated 2026 rate with its 90 per cent interval and where the limit sits against it, the chart drawing each interval; the interval's endpoints are left ungraded because they move with the method (the estimate itself ranges 131 to 205 for cefazolin 2 g across the family), only the side of the limit is graded, and it holds under every method tried (SF12). The call, the stump and every earlier figure stay as they were.
- 2026-11-08, architecture 3 (each product's out-of-tolerance rate rebuilt dose by dose on its tubing set): the
  platform's two runs both modelled the drift with the litres a set had pumped as their first move and landed the four
  products and every ask; a mechanism the weighed doses show is modelled on sight. The world is spent.
- 2026-11-08, draw stage: a lead service line inventory estimated from a random verification sample beside opt-in
  identifications: mark124 v5 spent the remainder accounting already.
- 2026-11-08, draw stage: a fraud or risk-targeting model's precision under label shift with verification-biased
  labels: mark267 spent the verification bias, and label shift alone is one insight.
- 2026-11-08, build stage: the 2.0 g/t cut-off left the kriged model 2 koz from Tier B's edge; 2.5 g/t, above the
  mean, separates the composites, the blocks and the kriged estimates into three tiers.
- 2026-11-08, build stage: without short horizontal lags the variogram's nugget was unidentified (an independent fit
  put the block variance at 0.41 and the gold in Tier A); the 2024 grade-control trial's 5 m pattern pins it. Placed
  first on a low-grade patch, its pairs understated the variance (the proportional effect) and swung the fit the
  other way; moved to a patch of typical grade.
- 2026-11-08, build stage: one graded figure that only the decisive step reaches left a landed run with every ask
  (pair 56); the cracker's second judgment is the variance the block ratio applies to (the declustered one, not the
  composites' as drilled), which moves the gold to 200,000 oz while the tier holds.
- 2026-11-08, architecture 4 on the platform: the one run filed Tier B by plain inverse-distance-squared blocks
  (159,610 oz) with no declustering, variogram or support correction, and the domain fit return read the prompt as
  summing tabulated blocks against stated tiers. Measured afterwards on the shipped pack: inverse distance files 92 to
  162 koz across powers 2 and 3, 3 to 16 composites, in three dimensions or within the flitch (nearest neighbour 217),
  and at 4 composites it reproduces the golden's tonnes, grade and gold at every cut-off, so no tier floor separates
  it. Seven re-tuned worlds (a larger short structure, flat supergene lenses 12 to 25 m across and 2 to 3 m thick on a
  1.25 m vertical grid, a smaller nugget) moved where it crosses but never removed the crossing: a smoother whose
  neighbourhood is a free knob sweeps through the true block variance, and the composite-support variogram read the
  thin lenses as nugget, biasing the golden low. The support stump is spent; the slot re-roots.
- 2026-11-08, architecture 5 draw: a recognizer's error falling with each user's own count of dictations, carried
  to a new market of new users: the right clock as cumulative use is Mark 46's held driver (a rate law stationary in
  cumulative service exposure), and "a new market's users are all new" names the axis in the decision's framing.
- 2026-11-08, architecture 5 draw: a contaminant's share of private wells above a new limit from a random survey with
  a detection limit above it and targeted low-limit sampling near sources: the targeted samples stratified on what
  drove the targeting and carried to the register's mix is mark124's driver.
- 2026-11-08, architecture 5 draw: pass@k at a budget beyond the samples drawn, from a latent per-problem solve-rate
  distribution with unsolvable problems: a deep-sampled subset either reads the answer directly or, if itself
  selected, reduces to two-phase design weighting (task264's lesson); the pattern also sits on the client's Example 9.
- 2026-11-08, architecture 5 draw: benchmark contamination separated from item-difficulty drift by each model's own
  training cutoff: a causal split whose objective is Experiment & Causal Analysis, not this slot's.
- 2026-11-08, architecture 5 draw: the same cancelling structure with the hidden property a recording device read
  from a device inventory: the customer's IT plan to move everyone to the phone app names the axis, so noticing is
  the whole stump.
- 2026-11-08, architecture 5 prototype: a single "sign the 10 per cent ceiling or not" call is landed by two cheap
  routes that over- or under-shoot past the line (recent starters' average level; a linear trend in starters' level
  extrapolated to 2027), so the call moved to the lowest of four offered ceilings, the cheap routes landing on 10 or
  12 and the trend extrapolation on 16; and the past compulsory go-lives were made small hospitals with high
  voluntary uptake, because a per-hospital event study at go-lives of the same size as 2027's would carry the step
  to the teaching hospitals without any clinician-level reasoning.
- 2026-11-08, architecture 5 build: each quarter's share above 15 per cent graded in whole per cent: a 1 per cent error
  in a clinician level moves the tail share by about half a point, and the 6.0 audits alone against every audit
  carried by its release step differ by that much, so the shares are graded as the band each stays under.
- 2026-11-08, architecture 5 build: each hospital's fourth-quarter share and 90th percentile, and each quarter's 90th
  percentile: one of eight hospitals, or one of four quarters, always sat within a tenth of a rounding line across
  seeds; only the fourth quarter's percentile is asked.
- 2026-11-08, architecture 5 build: each quarter's dictations to the nearest 10,000 or 50,000: an incumbent's volume
  read from three months or six moves every quarter about 1 per cent, across a rounding line.
- 2026-11-08, architecture 5 build: past go-lives at small hospitals with half their clinicians dictating by choice:
  the record climbed 3.6 points in the 2023 to 2024 release gap, so a run carrying the gap's drift forward had a free
  window that swept through 14; the small hospitals' voluntary uptake was raised to seven in ten and the releases made
  smaller, so no route through the record's drift passes 12.
- 2026-11-08, architecture 5 build: the teaching hospitals' new hires dictating at their incumbents' rate: the 2025 and
  2026 starters were then nearly all compulsory starters and their average reached 12.4 in the fourth quarter (14);
  new hires at a teaching hospital take the service up at four in ten, so recent starters mix both kinds.
- 2026-11-08, architecture 5 build: a 1.2 per cent audit and a last release in June 2026: the 6.1 audits alone and the
  pooled estimate differed by up to a point; the audit is 2.5 per cent and the frozen release has been in force since
  November 2025.
- 2026-11-10, architecture 5 on the platform: both runs typed clinicians on sight (their cohort counts matched the golden's typing to the audit, 16,307, 3,063 and 3,761), split the compulsory starters by appointment into compelled incumbents (21.25 per cent) and post-go-live hires (17.20), a gap the pack could not confirm (clinician-cluster permutation p 0.09; the world drew both from one distribution), gave the university hospitals' starters the incumbents' rate and, with one upward mix choice each (no ramp and no turnover; a per-clinician start and 2026 trends), filed 16 against the golden's 14; the call rested on one constructed subgroup found by one cross-tab (level 3 on the client's depth scale), so the slot was rebuilt as a results chain in the same world at the author's word.
- 2026-11-10, architecture 6 build: the university hospitals' acoustic effects at +15 and +11 per cent put their starters at the smaller hospitals' compelled clinicians' rate, so that shortcut landed the call; cut to +6 and +8.
- 2026-11-10, architecture 6 build: a specialty tilt at the university hospitals (radiology, oncology, cardiology) made the transport ride on noisy cell coefficients; removed, the grade mix kept.
- 2026-11-10, architecture 6 build: moves drawn from every hospital alike left about 45 clinicians audited at two hospitals and Ballykeel's effect 3.7 points off; moves into the university hospitals now come mostly from the smaller hospitals, as careers run, giving 36 and 64.
- 2026-11-10, architecture 6 build: a three-month switch-over moved no call (full-volume go-lives kept 14); the departments now switch over across four months, so a full-volume start passes 14 in the fourth quarter and 10 in the first.
- 2026-11-10, architecture 6 build: leavers replaced by hires dictating at full volume from the go-live put Ballykeel's fourth quarter 10 per cent above the world's; a replacement hired before a go-live switches over with the department, so the staff is held like for like.
- 2026-11-10, architecture 6 build: a seed search of twenty at the raised level; seed 60607 is the one whose golden sits mid-band (the fourth quarter 12.9 to 13.0 across the rivals) with the first quarter under 10 and the third under 12.
- 2026-11-10, architecture 6 build: the uptake's selection also lands the smaller hospitals' pooled compulsory starters near the starters' rate, so that route keeps the call (14) while missing the third quarter, the first quarter past 12 and both university hospitals; kept as a route, not broken by tuning, because it ignores the 27.7 against 10.0 gap the record shows.
