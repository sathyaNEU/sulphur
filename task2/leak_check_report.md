# leak check, task2

**Verdict: REVIEW.** 13 files read, 29 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: hospitals, architecture, clinicians, starters, effect, record, release, clinician, missed, population, smaller, golden, effects, points, carried, months, method, shortcut, compelled, go-lives, fourth, volume, harmless, reader, family

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `QA-07_recognition_quality_audit.pdf`: golden figure 2.5 appears: .... 1 Sample Each month, at each customer hospital, 2.5 per cent of the month's dictations, rounded to th...
- **REVIEW** `draft_schedule4_quality_2027.docx`: golden figure 4.1 appears: ...our chosen ceiling by 15 January 2027. 4.1 Definitions Audited dictation: a dictatio...
- **REVIEW** `recognition_releases_2023_2026.pdf`: golden figure 7.8 appears: ...rate on Larkmoor's LCB-2 clinical benchmark down 7.8 per cent on the release before. Release 5.2 (18 M...
- **REVIEW** `recognition_releases_2023_2026.pdf`: golden figure 6.0 appears: ...down 3.9 per cent on the release before. Release 6.0 (4 November 2025) Noise-robust front end; better...
- **REVIEW** `service_notice_SN-2026-14.pdf`: golden figure 6.0 appears: ...ide those weekends. Recognition stays on release 6.0 for every Irish customer from 1 January to 31 Dec...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `QA-07_recognition_quality_audit.pdf`: 3 of 25 stump-paragraph terms appear (record, release, clinician); read whether the document names the move
- **REVIEW** `draft_schedule4_quality_2027.docx`: 3 of 25 stump-paragraph terms appear (hospitals, record, clinician); read whether the document names the move
- **REVIEW** `services_agreement_schedule2_deployment.pdf`: 3 of 25 stump-paragraph terms appear (hospitals, record, clinician); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "A short memo should open on the ceiling and the first quarter that would pass each lower one, with a chart of each quarter's expected share against the ceilings, and a workbook should hold each quarter's lowest ceiling, "

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (Sonnet, medium), 2026-11-08, saw only fresh copies of prompt.txt and target/ and solved nothing.

1. Decisive step: none named. The nearest sentence is Schedule 4.2's scope ("every dictation made under the Service in
   the quarter ... including hospitals where dictation becomes compulsory during the year"), which puts the two
   teaching hospitals in the 2027 population and says nothing of how to project their share.
2. A file ranking or scoring the ceilings for 2027: none; the quality reports hold only past quarters.
3. Files that exist only to help: none. The rollout plan's Scope sheet defines its own headcount (clinicians in post,
   those already dictating included); QA-07 reads as a procedure, not a how-to.
4. Answer-like figures: none; the ceilings and fees are the offered options, the past shares are history.
5. Literal sentences: Schedule 4.2 read literally makes each quarter's share the pooled audited share across all the
   hospitals, each weighted by its audited volume, with the weights moving in 2027 as the teaching hospitals' volumes
   rise (the golden's construction); 4.3 one ceiling for every quarter; 4.1 above 15 per cent on the adjudicated
   score; QA-07 4 and 5 the adjudicated row supersedes the first pass and unscorable audio is out.
6. What decides: an analytical, modelling choice, projecting each 2027 quarter's pooled share as the hospital mix
   changes, with the earlier compulsory go-lives as the visible reference; the cleaning rules are filed and are not
   the stump; nothing planted.

Review items: (a) the release notes and SN-2026-14 state no 2027 ceiling or share; harmless. (b) the rollout plan's
2027 dates are the plan's own forward dates, matching Schedule 2; harmless.

Ruling: no finding to fix. Question 5's literal reading is the golden's population and weighting; question 6's
"earlier go-lives as the visible reference" is ladder rung 2 (the go-live step carried in points, which lands on the
10 per cent ceiling).

## Solver's-eye read

One isolated reader (general-purpose, Sonnet, medium), 2026-11-10, on fresh copies of prompt.txt and target/ only; it read all 13 files and solved nothing.

- Q1 (a sentence or file telling how to do the analysis): draft_schedule4_quality_2027.docx 4.2 ("the heavy correction share is the number of the quarter's audited dictations needing heavy correction divided by the number of the quarter's audited dictations. Every dictation made under the Service in the quarter ... including hospitals where dictation becomes compulsory during the year") and QA-07 4 (the adjudicated score replaces the first pass). Ruled: both file the WHAT (the metric, its population, the version basis), which the literal reader executes to the golden; neither names a step of any result.
- Q2 (a file ranking the candidates): none; the quality reports hold 2023 to 2026 only.
- Q3 (a file existing only to help): none; every file has its organisational use.
- Q4 (a figure reading as the answer): none; the schedule's four ceiling and fee pairs restate the prompt's options.
- Q5 (filed sentences fixing a graded figure): Schedule 4.1 (the adjudicated score) and QA-07 5 (unscorable audio left out of every rate); the golden executes both.
- Q6 (one thing settling most of the asks): none. The nearest candidate, the university hospitals' low shares in the reports' By hospital sheet, "IS the subject of the decomposition ask, not a shortcut around it, and it settles nothing for the BKU volume count or the P90 tail"; every ask turns on analysis (the forecast, the hospital shares, the volume with its ramp, the distributional tail, the attribution), the release notes' LCB-2 cuts read as a trap their own caveat heads off, nothing turns on catching a planted defect.
- Realism: one nit, the quality reports' shares stored to sixteen digits; fixed in the generator (four decimals). Otherwise the records read as an organisation's own (names, metadata, release spellings across systems, adjudication rows, dictation_id collisions, SLA noise).
- REVIEW lines handed over (numbers withheld): (a) QA-07's sampling rate, harmless; (b) the schedule's clause numbers, harmless; (c) a release-notes benchmark percentage, harmless (the document's own caveat), with the note to check the golden's release effect is no benchmark figure (it is not: 6.1 for 5.0, 10.6 for 4.0 to 6.0); (d) release names, harmless; (e) the rollout plan's 2027 dates, harmless (planning inputs the forward call needs).
