# leak check, task2

**Verdict: REVIEW.** 13 files read, 1 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: release, architecture, compulsory, hospitals, record, starters, clinicians, clinician, steady, dictation, golden, family, carried, population, teaching, months, points, go-lives, landed, percent, weighed, fourth, frozen, go-live, graded

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `recognition_releases_2023_2026.pdf`: golden figure 6.0 appears: ...down 3.9 per cent on the release before. Release 6.0 (4 November 2025) Noise-robust front end; better...
- **REVIEW** `service_notice_SN-2026-14.pdf`: golden figure 6.0 appears: ...ide those weekends. Recognition stays on release 6.0 for every Irish customer from 1 January to 31 Dec...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `QA-07_recognition_quality_audit.pdf`: 4 of 25 stump-paragraph terms appear (release, record, clinician, dictation); read whether the document names the move
- **REVIEW** `draft_schedule4_quality_2027.docx`: 5 of 25 stump-paragraph terms appear (compulsory, hospitals, record, clinician, dictation); read whether the document names the move
- **REVIEW** `recognition_releases_2023_2026.pdf`: 3 of 25 stump-paragraph terms appear (release, architecture, dictation); read whether the document names the move
- **REVIEW** `services_agreement_schedule2_deployment.pdf`: 5 of 25 stump-paragraph terms appear (compulsory, hospitals, record, clinician, dictation); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Put the working in heavy_correction_2027.xlsx: for each 2027 quarter the lowest ceiling its share stays under, and the word error rate nine in ten fourth-quarter dictations stay under, rounded to the nearest whole per ce'

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `shannonside_dictation_rollout_2027.xlsx`: 3 ISO dates after 2027-01-11, e.g. 2027-02-01, 2027-08-16, 2027-10-01

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: files[11].covers shares the design note's stump vocabulary (hospitals, teaching, go-live): say what the task decides, not how

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
