# task2 architecture 5: Larkmoor Speech, the 2027 heavy-correction ceiling for Shannonside Hospital Group

General Statistics & Data Science, robustness analysis (distribution shift), Descriptive & Distribution Analysis.
Re-root of the slot after the platform landed architecture 4 (one run filed Tier B with inverse-distance blocks,
`runs/arch4_platform_feedback.md`): one architecture per world, so a new world, dataset and shell.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task2.json` v5, registered 2026-11-08T22:01:37Z at WARN; lineage carries
  v1 to v4, the v4 shell (what, for, pptx and xlsx) among the dead shells. Answered: `overuse.strategy`
  (composition_mix in 3 of the last 12): task3 v5 transfers a rare-event level between two basins by each event's own
  threshold and task1 an exit curve by provider tenure; neither splits a steady aggregate into a cancelling
  improvement and drift, and the label is the honest one because the ceiling is a mixture carried to a forward mix.
  `repeat.gate_g` (decomposition_attribution, task7 v6): task7 splits a lottery gap into the works and a contaminating
  visit; here the split is of a steady share into release steps and a composition drift, with no comparison group.
- **Pairing:** a medical speech-recognition vendor commits a ceiling in a hospital group's 2027 quality schedule: the
  share of a quarter's audited dictations whose word error rate exceeds 15 per cent (heavy correction) may not pass
  the ceiling in any quarter, and the schedule offers ceilings of 10, 12, 14 and 16 per cent at falling fees.
- **Shape:** 14, cuts of a distribution: each 2027 quarter's share above 15 per cent and its 90th-percentile word
  error rate, each hospital's share in the fourth quarter, and the lowest offered ceiling no quarter breaches.
- **Strategy:** composition_mix, Part A "Heterogeneity that pooling hides", WORKS IN FORM: the groups differ and the
  decision weights them to a population whose mix the record never held, with the group property rebuilt from a
  history (a clinician's start set against the hospital's compulsory date) and never read off a column; GSDS 02 (a
  held-out record that does not look like deployment) in the live form, the deployment population rebuilt from the
  record.
- **Data-native sentence:** the audited share has held between about 6 and 8 per cent for four years because each
  of the four model releases cut every clinician's error by 3 to 6 per cent while the dictation mix drifted toward
  clinicians who began only once their hospital made dictation compulsory, whose heavy-correction share is about
  eight times theirs; the six hospitals that went compulsory were small, with seven in ten of their clinicians
  already dictating by choice, and the two that go compulsory in 2027 (Shannonside University on 1 February,
  Ballykeel University on 1 October) are the teaching hospitals, larger than the other six together, where about
  one in eight did, under a model frozen at release 6.0 for the platform migration.
- **The lessons it is drawn against** (`sulfur-record.md`): a mechanism the rows visibly carry is modelled on sight,
  so the structure here is one the rows in view hide (two effects cancelling inside the observed window) with the
  deciding evidence in a second file at another grain (the contract's compulsory dates against each clinician's first
  dictation); noticing was the whole stump in task7 arch 4 and task8 arch 17, so after the notice the 2027 mix still
  has to be projected through turnover and two go-live ramps with the model frozen, and the cheap routes all err the
  same way (low), so no intermediate shortcut can cross into the golden's ceiling by chance (architecture 4's death).
- **People:** drawn with `guard.py names --geo ie --seed 5205`: Jody Cahir, Yasmine Ganley, Colum Wallace, Pearce
  Stapleton, Alexander Sigerson, Kristopher McLoughlin.

## Default path

1. Build each 2023 to 2026 quarter's share of audited dictations above 15 per cent word error rate from
   `dictation_audits_2023_2026.csv`, as the draft Schedule 4 defines it: the adjudicated score where a dictation was
   re-audited, the rate recomputed from substitutions, deletions and insertions over the reference words, the three
   release strings read as one release; the shares tie to `quality_reports_2023_2026.xlsx`.
2. Read the record: the share sits between 6.3 and 7.9 per cent in every quarter, 6.3 to 7.7 since the middle of 2024;
   no quarter has passed 10.
3. Carry it to 2027 the field's way for a shifted deployment population: post-stratify each hospital's 2026 share to
   its 2027 share of dictations, which the rollout plan sets when Shannonside University and Ballykeel University go
   compulsory; their 2026 shares are a few per cent, so the 2027 quarters fall to 7.2, 6.2, 6.1 and 5.3 per cent.

Ends on: commit to the 10 per cent ceiling (every quarter at or under 10).

Golden: commit to 14 per cent; the expected shares are 8.9, 11.1, 11.4 and 13.1 per cent, so 10 is passed from the
second quarter and 12 in the fourth, and nine in ten fourth-quarter dictations stay under 16 per cent.

## Stump sentence

The default path reweights the audited share's steady 7 per cent to 2027's hospital mix, sees it fall because the
teaching hospitals' rows show a few per cent, and commits to the 10 per cent ceiling; the step that lands it there is
reading those rows as the hospitals' 2027 clinicians, when today only the one in four who chose to dictate appear in
them, and the clinicians who begin once a hospital is compulsory carry a heavy-correction share about eight times
theirs under the frozen release, the steadiness of 2023 to 2026 being each release cancelling the drift toward such
clinicians; with no release in 2027 and both teaching hospitals compulsory, the fourth quarter reaches about 13 per
cent.

## Deep reasoning

- **Task type:** robustness analysis (distribution shift): a recognizer's tail error rate carried from the audited
  population to a deployment population the record never held.
- **Domain test:** the deciding quantity is a tail share of a mixture, each dictation's word error rate above 15 per
  cent, estimated from each kind of clinician's dictation-level rates under the frozen release, weighted to each 2027
  quarter's dictation mix; the field's estimator for a shifted population is post-stratification on the observed
  covariates, which here moves the wrong way.
- **Swap:** "the lowest handle-time ceiling a contact-centre vendor can commit to" with handle times for error rates:
  the release steps, the compulsory start dates and the frozen release stop meaning anything, and a trend on a steady
  aggregate is what is left.
- **Layer 1:** re-audited dictations carrying a first and an adjudicated score (QA-07's adjudication), release strings
  in three forms (two export formats and the adjudication rows), the error rate as a fraction before 2025 and in per
  cent after, staff numbers reissued when clinicians move hospitals (the register's previous numbers), two months of
  the volume export repeated by a re-run, unscorable audio; nothing placed to be caught, and none moves the ceiling
  (asserted: first-pass scores and unlinked movers file every graded figure as the golden's).
- **Layer 2:** composition_mix, heterogeneity weighted to a population whose mix the record never held: which kind of
  clinician 2027's new dictators are, and so what each 2027 quarter's mix is, flips the ceiling.
- **Decisive step:** separating the within-clinician release effect from the drift of the dictation mix toward
  clinicians who began once their hospital was compulsory, then carrying the frozen release's mixture to the mix the
  teaching hospitals' go-lives make.
- **Not semantics:** every field, code, release string and definition read correctly still leaves the steady share and
  its hospital reweighting at 7 and 5 to 7 per cent; the property that decides (a clinician's first dictation on or
  after the hospital's compulsory date) is no field, and no definition says whom 2027's new dictators resemble.
- **Not rule application:** no filed rule projects 2027 (the schedule defines the metric and the ceilings, the rollout
  plan the dates and staff, the migration notice the frozen release); the enumerated family of projections spans 5.3 to
  13.1 per cent in the fourth quarter (steady, reweighted, gap drift added, go-live step, average clinician, recent
  starters, compulsory starters) and the standing family (the 6.0 audits alone or every audit carried by its release
  step, turnover or none, the boundary a month either way, first-pass scores, movers linked or not, volumes from three
  or six months) spans 12.54 to 13.11, every member on 14; the ruling-out is the data's own (the release steps within
  clinicians, the go-lives' starters).
- **Analyst test:** a strong analyst who cleans the audits and reads the schedule sees the share steady at about 7 per
  cent, reweights it to 2027's hospital mix, which lowers it, and commits to 10 per cent; the fourth quarter reaches
  about 13.
- **Estimand:** the share of each 2027 quarter's audited dictations with a word error rate above 15 per cent, every
  dictation made under the service in the quarter including those of clinicians not yet dictating on the as-of date,
  and the lowest of the offered ceilings no quarter passes (draft Schedule 4, 4.2 and 4.3).
- **No decoy:** nothing is planted: the quarterly reports state the record's shares truthfully, the release notes'
  benchmark is labelled as Larkmoor's own set, no memo or briefing carries a 2027 figure, and the hospital reweighting
  is the analyst's own construction.
- **No certified replay:** no published figure is reproduced to recover a method; the quarterly reports agree with
  every route on the record and decide nothing about 2027.
- **Chain:** (1) each audited dictation's error read as its clinician's own level times the release in force, the
  release steps measured within clinicians (4.0 about 3 per cent, 5.0 about 6, 5.2 and 6.0 about 3 each); (2) the steady
  aggregate under falling clinician levels means the mix drifted, and the 2023 to 2024 release gap shows it (about 6.6
  to 7.3 per cent with no release); (3) the drift is toward clinicians whose first dictation came on or after their
  hospital's compulsory date, read from the volume file's first month against Schedule 2's dates: under release 6.0
  19.2 per cent of their dictations need heavy correction against 2.4 for those who chose, at every one of the six
  go-lives alike; (4) each 2027 quarter's mix: clinicians leaving at the record's rate (about 9 per cent a year) and
  replaced by compulsory starters, and the teaching hospitals' 2,070 clinicians in post, 503 dictating today, starting
  at their compulsory dates with the go-live ramp the record shows (about 23, 53 and 82 per cent of a full month); (5)
  each kind's dictation-level rates weighted to each quarter give the share and the percentile, and the ceiling.
- **Judgment:** whom 2027's new dictators resemble, justified by the record: the compulsory starters at each of the six
  go-lives sit at one level whatever the hospital and the year (typical error 9.8 to 10.4 per cent under 6.0), unlike
  those who chose, and the steady aggregate is shown to be cancellation, not stability, by the release steps within
  clinicians; and the percentile needs each clinician's dictations' scatter, not the spread of clinicians' averages.
- **Hidden by:** the rows in view mimic stability: the audited share is steady because releases cancel the drift, the
  teaching hospitals' rows hold only those who chose to dictate, and the kind of clinician is a relation (first
  dictation month against the compulsory date) across two files at different grains.
- **After the notice:** once a run sees that compulsory starters sit higher, it still owes (1) each 2027 quarter's mix,
  built from the record's turnover, the go-live ramp and the teaching hospitals' clinicians not yet dictating, (2) the
  release held at 6.0 rather than the record's run of releases carried on, and (3) the starters' level taken from the
  compulsory starters rather than the recent starters, who mix both kinds; the recent starters' average files 10.3 in
  the fourth quarter and commits to 12.
- **One-fact test:** the likeliest hint, "clinicians who begin once dictation is compulsory are harder to recognise",
  still leaves the 2027 mix to be built from the rollout plan, the turnover and the ramp, and the release to be held;
  the recent-starters shortcut keeps the call at 12, and a mix built without the ramp passes 10 a quarter early.
- **No replay:** the call re-derives no published figure and no stated number is wrong.
- **Pinned:** every rival a careful analyst would run is run on the cut pack (`generator/checks.py`): the steady share,
  the hospital reweighting, the release gap's drift, the go-live step at the small hospitals and the average
  clinician land on 10, the recent starters on 12; the standing family lands on 14 with every graded figure the same.
- **Run forecast:** a method shortcut at rung 1 (the hospital reweighting) or a self-confirming check (the steady record
  back-tested on itself); a run that finds the release steps and looks for the drift at the hospitals' go-lives carries
  their few-point step and stops at 10 (unfinished chain).
- **Strategy label:** WORKS IN FORM, heterogeneity that pooling hides, in the live form: the decision weights the groups
  to a population whose mix the record never held, the group property rebuilt from a history (first dictation against
  the compulsory date), never a column.
- **Lesson:** a steady metric can be two moves cancelling, and a deployment-shift correction on observed covariates can
  move the wrong way when a covariate's current rows hold only the self-selected; no build on file teaches the
  cancellation read off release steps within clinicians.

## Survivor anatomy

- **Actor:** the deciding property (a clinician began dictating on or after the hospital's compulsory date) has no
  column: the volume file has months and staff numbers, the register grade, specialty and post dates, Schedule 2 a date
  per hospital.
- **Link:** read through the relation between each clinician's first month in the volume file and the hospital's
  compulsory date in Schedule 2, at another grain; no key or sentence ties them, and the field's reweighting never asks
  when a clinician began.
- **Reflex:** the field's method (post-stratifying the audited share to the deployment mix by hospital) sits at rung 1
  and lowers the share, because the teaching hospitals' current rows are those who chose to dictate.
- **Back-test:** the steady route validates: 2026 back-cast from 2025's level holds within a point, and no quarter on
  record passes 8 per cent since the middle of 2024.
- **Second use:** the same mixture prices the fourth quarter's 90th percentile.
- **Shock:** 2027 departs from the record twice: no release, and the two largest hospitals go compulsory.
- **Pins:** Schedule 4 pins the metric (the share of a quarter's audited dictations above 15 per cent), the ceilings
  and the quarters; nothing pins the projection, which the data force.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | 8 Framing | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 the steady audited share carried forward | Schedule 4's metric | the audit file | yes, the last level | no | no | yes | no | no | readable |
| 1 each hospital's share at 2027's hospital mix | the rollout plan's staff | site codes | yes, post-stratification | no | no | no | no | no | readable |
| 2 the go-live step at the small hospitals carried to the teaching hospitals | Schedule 2's dates | site codes | yes, an event study | no | no | no | no | no | readable |
| 3 (decisive) 2027's new dictators at the compulsory starters' level | no | no, first month against a date in another file | no, no field method asks when a clinician began | no | no | no | no | no, the prompt names only the ceilings and the quarters | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "share of audited dictations" | the share among the quarter's audited dictations, expected | the share among all dictations | same call | QA-07 1: a random sample within hospital and month; equal in expectation |
| SF2 | "word error rate" | substitutions, deletions and insertions over the reference words | the export's own column | same call | QA-07 3; the export's column agrees once its units are read |
| SF3 | a re-audited dictation | the adjudicated score | the first pass | same call, every graded figure | asserted |
| SF4 | a quarter | by the dictation's date | by the audit's date | same call, every graded figure | asserted |
| SF5 | "above 15 per cent" | strictly above | at or above | same call | Schedule 4.1; C1 on the frozen rates |
| SF6 | the 2027 population | every dictation under the service in the quarter | the clinicians dictating on the as-of date | 10 | Schedule 4.2 "every dictation made under the Service ... including hospitals where dictation becomes compulsory" |
| SF7 | the release in 2027 | 6.0 throughout | a 2027 release | lower | SN-2026-14 |
| SF8 | "passing" a ceiling | above it | at or above | same call | Schedule 4.3; C1 (the fourth quarter 0.9 from 14) |
| SF9 | turnover | the record's leaving rate | none | same call, every graded figure | asserted |
| SF10 | the go-live ramp | the record's first months at each go-live | full volume from the date | same ceiling; the first quarter past 10 and its band move | the six go-lives on record; the ask's second judgment |
| SF11 | the kinds' rates under 6.0 | every audit carried by its release step | the 6.0 audits alone | same call, every graded figure | asserted |
| SF12 | "the word error rate nine in ten fourth-quarter dictations stay under" | the 90th percentile of dictations | of clinicians' average rates | same call (the ask moves) | the prompt's "dictations" |
| SF13 | the compulsory boundary | first dictation on or after the date | a month earlier | same call, every graded figure | asserted; a month later contradicts Schedule 2's first-of-month dates |
| SF14 | movers between hospitals | linked through the register's previous staff numbers | treated as new clinicians | same call, every graded figure | asserted |
| SF16 | the ceiling | the lowest offered ceiling at or above every quarter | the expected share rounded up | same call | Schedule 4.3 offers four ceilings |
| SF17 | a clinician's volume | the last three months; a starter's from 2026 | the last six; a starter's from 2025 and 2026 | same call, every graded figure | asserted |
| SF18 | "the word error rate nine in ten fourth-quarter dictations stay under" | the 90th percentile rounded to the nearest whole per cent (16) | the smallest whole rate with nine in ten under (17) | the ask moves | the prompt's "rounded to the nearest whole per cent" |
| SF19 | a starter's early months | the same level as later months | a learning curve that lowers the first months | 12 if it held | asserted absent: the first three months within 0.05 (log) of later months across every release |

## Ladder

The pricing sequence, run on the cut pack (`generator/checks.py`, `generator/ceiling.py`):

1. **The residue the filed WHAT leaves** is a method question, whom 2027's new dictators resemble and so what each
   quarter's mix is, not a knob: the schedule files the metric and the ceilings, the rollout plan the dates and staff,
   the migration notice the frozen release.
2. **The move against the ceiling:** the fourth quarter must pass 12 per cent to move the call from 12 to 14; the
   teaching hospitals' new dictators carry about 19 per cent against the 7 per cent the average clinician carries, and
   they make about half of the fourth quarter's dictations.
3. **The one-group-by route** is the hospital reweighting (rung 1), which files 5.3 per cent; the golden needs each
   clinician's first month set against the compulsory date in another file and a 2027 mix built clinician by
   clinician.
4. **The family:** the standing family spans 12.54 to 13.11 in the fourth quarter (14), every route that skips the step
   5.3 to 10.3 (10 or 12).

| Rung | Route | 2027 quarters (per cent) | Ceiling |
|---|---|---|---|
| 0 | the 2026 share carried forward | 7.4, 7.4, 7.4, 7.4 | 10 |
| 1 | each hospital's 2026 share at 2027's hospital mix | 7.2, 6.2, 6.1, 5.3 | 10 |
| 1 | starters at the average clinician's level | 7.5, 7.2, 7.1, 6.9 | 10 |
| 2 | the release gap's drift added | 7.9, 8.1, 8.4, 8.6 | 10 |
| 2 | the go-live step at the small hospitals, in points, at the teaching hospitals | 7.7, 8.0, 8.0, 8.1 | 10 |
| 2 | starters at the 2025 and 2026 starters' level | 8.2, 9.3, 9.4, 10.3 | 12 |
| golden | starters at the compulsory starters' rates, turnover, ramp, release frozen | 8.9, 11.1, 11.4, 13.1 | 14 |

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every dictation made under the service in each 2027 quarter, clinicians not yet dictating included | filed (Schedule 4.2); SF6 |
| 2 Unit of account | the audited dictation | filed (Schedule 4.1) |
| 3 Attribution window | calendar quarters by the dictation's date | filed; SF4 asserted |
| 4 As-of dating | the record to 31 December 2026; the schedule returned by 15 January 2027 | filed in the draft schedule |
| 5 Version basis | the adjudicated score of a re-audited dictation | filed (QA-07 4); SF3 |
| 6 Denominator | a quarter's audited dictations | filed (Schedule 4.2) |
| 7 Weighting | each dictation alike | filed (Schedule 4.2) |
| 8 Window length | four 2027 quarters | filed |
| 9 Boundary inclusivity | above 15 per cent; a ceiling passed when the share is above it | C1 (SF5, SF8) |
| 10 Rounding path | each quarter's band from its unrounded share; the percentile in whole per cent once | asserted; the prompt's rounding |
| 11 Tie-break | none needed | one ceiling is the lowest at or above the highest quarter |
| 12 Maturity and censoring | none: 2027 is projected whole; every 2026 audit is scored | filed (QA-07) |
| 13 Order of operations | rates per release, then the mix, then the share | C1 across orders (asserted) |
| 14 Row order | none | no rule reads row order |
| 15 Duplicate resolution | the volume export's repeated rows counted once; re-audits by the adjudicated score | asserted (Layer 1) |
| 16 Identity normalisation | staff numbers reissued on a move linked by the register | asserted (SF14) |
| 17 Netting against gross | none | no netting in the metric |
| 18 Dimensional units | the error rate as a fraction or per cent by export | asserted (Layer 1) |
| 19 Code and status semantics | release strings in three forms read as one release | asserted (Layer 1) |
| 20 Integerisation | the percentile in whole per cent | the prompt's rounding |
| 21 Clause scope | Schedule 4 covers every hospital in Schedule 2 | filed |
| 22 Forward window contents | the go-live dates and staff from the rollout plan and Schedule 2, release 6.0 from SN-2026-14 | filed |

## Literal reader

Executed word for word, the prompt and Schedule 4 give the golden: the ceiling is the lowest of the offered ceilings
that no 2027 quarter's share of audited dictations above 15 per cent passes, every dictation made under the service in
the quarter counts (the teaching hospitals' compulsory clinicians included from their dates, as Schedule 2 and the
rollout plan set them), and recognition stays at release 6.0 (SN-2026-14); the reweighting that reads the teaching
hospitals' 2026 rows as their 2027 clinicians takes a population Schedule 4.2 does not (SF6), and every convention the
projection needs has a fork row closed by a filed sentence or asserted as the same call with every graded figure.

## Oracles

- **The quarterly quality reports** state each 2023 to 2026 quarter's audited dictations and heavy-correction share;
  they tie to the cleaned audits on every route and confirm the Layer 1 build, and say nothing of 2027.
- **The release notes' benchmark figures** (each release's relative error reduction on Larkmoor's own LCB-2 set) agree
  in direction with the within-clinician release steps and size none of them for this customer.
- No document, control or reconciliation in the pack states a 2027 share, a ceiling or whom the new dictators resemble.

## Ask sheet

- **Ask 1, the PDF's opening (the call):** the 14 per cent ceiling; 10 passed from the second quarter, 12 in the fourth.
- **Ask 2, the chart (four bands):** each quarter's expected share against the ceilings: under 10, between 10 and 12
  twice, between 12 and 14.
- **Ask 3, each quarter's lowest ceiling (four):** golden 10, 12, 12 and 14; a mix built without the go-live ramp 12,
  12, 12 and 14 (its first quarter 10.2); the reweighting 10 each; the recent starters 10, 10, 10 and 12.
- **Ask 4, the fourth quarter's 90th-percentile word error rate (whole per cent), its own second judgment:** the mixture
  of dictation-level rates: golden 16; read off clinicians' average rates 15; the 2026 mix 14.
- **Pair ceiling:** 44.3 (`ceiling.py` on the cut pack: the recommendation 20, four components 4.5 each,
  instruction-following 7, the asks 55 over the four answers, each kept in proportion to its figures; the landed run
  that takes the compulsory starters but starts the go-lives at full volume and reads the percentile off clinicians'
  averages scores 74.8, the steady route 13.9).
- **Shallow keep:** 12.5 per cent of the ask weight (the steady route keeps the first quarter's band).
- **Measured by:** task2/generator/ceiling.py on the cut pack.

| Ask figure | Golden | Landed run (compulsory starters found, go-lives at full volume, percentile of averages) | Shallow run (the steady share) | Cracker verdict on the landed run |
|---|---|---|---|---|
| the ceiling | 14 | 14 | 10 | keeps |
| the first quarters past 10 and 12 | second; fourth | first; fourth | none | misses |
| each quarter's lowest ceiling | 10, 12, 12, 14 | 12, 12, 12, 14 | 10, 10, 10, 10 | misses |
| the fourth quarter's 90th percentile | 16 | 15 | 14 | misses |

## Leak rulings

The design-note vocabulary sweep's lines (`leak.py` sweep 4), ruled in the main thread and never handed to the reader:

- `QA-07_recognition_quality_audit.pdf` (release, record, clinician, dictation): the audit's sampling, scoring and
  adjudication in the procedure's own words; it names no kind of clinician and nothing about 2027. Harmless.
- `draft_schedule4_quality_2027.docx` (hospitals, compulsory, record, clinician, dictation): 4.2 files the population
  (every dictation under the service, hospitals going compulsory during the year included), the WHAT that closes SF6;
  it says nothing of who dictates worse. Harmless.
- `recognition_releases_2023_2026.pdf` (release, architecture, dictation, rebuilt): each release's changes and
  Larkmoor's own benchmark, labelled as not a customer's. Harmless.
- `services_agreement_schedule2_deployment.pdf` (hospitals, compulsory, record, clinician, dictation): the contract's
  dates and its compulsory-use term (every clinician in post dictates from the date, and every later starter); it
  says who dictates, never how well. Harmless.
- The prompt's workbook sentence (quarter, dictation): the asks themselves. Harmless.

## Prompt contract

A voice rewrite may not drop or change: the question (the lowest heavy-correction ceiling Larkmoor Speech can commit
to); the ceilings offered (10, 12, 14 and 16 per cent in Shannonside Hospital Group's draft 2027 service schedule); the
deciding outcome (no 2027 quarter's share of audited dictations above 15 per cent word error rate passing it);
quality_schedule_2027_ceiling.pdf opening on the ceiling and the first quarter that would pass each lower one, with a
chart of each quarter's expected share against the ceilings; heavy_correction_2027.xlsx with each 2027 quarter's lowest
ceiling its share stays under and the word error rate nine in ten fourth-quarter dictations stay under; rates in whole
per cent. It may never add the compulsory dates, the go-lives, the teaching hospitals, the clinicians' start, voluntary
or compulsory use, a release, a frozen model or the migration, a projection, a mix, turnover, a ramp, reweighting, a
count of hospitals or clinicians, or any hint that the steady record hides a change.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call rests on the projection that types each clinician by
  the first month dictated against the hospital's compulsory date, with the hospital reweighting at rung 1 and the
  steady share at rung 0; no route that skips the typing lands the ceiling (Gate F, asserted); the asks ride the
  same step, two of them with judgments of their own (the go-live ramp in the first quarter, the dictation-level
  scatter in the percentile).
- Free gates on the final cut: generator checks 37 of 37, figures_check 58 of 58, precut 75 with 0 FAIL and 0 WARN,
  voice-check clean, leak.py REVIEW with no LEAK, the container gate clean, two byte-identical builds,
  `guard.py surface` clean, `guard.py heart` WARN (repeat.gate_g against task7 v6, answered in the Draw).
- Stage 4: the isolated leak reader found no decisive-step sentence, ranking, helper or answer file, read Schedule
  4.2 literally as the golden's population and weighting, and called the deciding step an analytical modelling
  choice; the judge's first pass returned DETERMINISTIC with a FIX_NOW (the percentile's rounding, closed by the
  prompt's "rounded to the nearest whole per cent"; audit times after the as-of date, closed by holding the export
  to what was scored by 8 January 2027; two figures stated finer than the data carry, restated), reproducing every
  graded figure independently (the fourth quarter 12.4 to 13.3 across its variants); its closest fork, a learning
  curve in a starter's first months, is asserted absent (SF19). The one targeted re-judge returned DETERMINISTIC
  and APPROVE, its nit (the record's range to a tenth) restated as about 6 to 8 per cent
  (`determinism_check_report.md`).
- Pair ceiling 44.3 (`ceiling.py` on the cut pack), shallow keep 12.5 per cent.

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
