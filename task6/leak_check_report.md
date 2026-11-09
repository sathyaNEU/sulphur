# leak check, task6

**Verdict: REVIEW.** 15 files read, 45 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: notifications, missed, architecture, method, rejected, reading, survey, points, golden, gullhaven, weighted, hourly, partner-gateway, accounts, seat-map, record, weights, dropped, decisive, default, wrenhaven, payments, weighting, careful, attribution

## 1 file names (REVIEW 1)
- **REVIEW** `capacity_review_2026-Q4.md`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 2.3 appears: ...own health probes are not requests. 2.3 The server-side duration of a request is the dur...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 1.0 appears: ...rney-search 1 1,500 1.0% fares 1 300...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 2.0 appears: ...accounts 1 600 2.0% partner-gateway 2...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 0.5 appears: ...booking 1 3,000 0.5% payments 1 2,000...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: carries 10 of 13 distinctive words of the committed call: 'Put reliability engineers on places, partner-gateway, fares, seat-map and notifications, in that order: the five ran ove'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: 6 of 25 stump-paragraph terms appear (notifications, partner-gateway, accounts, seat-map, record, payments); read whether the document names the move
- **REVIEW** `capacity_review_2026-Q4.md`: 5 of 25 stump-paragraph terms appear (notifications, partner-gateway, accounts, seat-map, payments); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'csv+docx' at 29% of 14 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (REVIEW 1)
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: names 13 column(s) of the data files verbatim (Service, Tier, commit, component, cost, deployment): confirm it is the organisation's own record and not a note written for the analyst

## 12 client quality check (INFO 2)
- **INFO** `-`: 15 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read (architecture 7)

Reader (isolated, Sonnet, medium), 2026-11-09, on a fresh copy of prompt.txt and the 15-file pack. It read the pack for
leaks and solved nothing.

1. How the analysis should be done: PR-SLO-3 3.1 to 3.4 and 5.2 (the December window in Lisbon time, the incident
   exclusion from when the tool added a service until the status page showed every component operational, unless the
   service owned the root cause, and 3.3's definition of owning it). Ruled: the standard files the WHAT; no sentence says
   how an owner is found or that the spans are a sample to be weighted.
2. A file ranking the candidates: none. incidents_2026.csv's root_cause_service is blank on every December row (reviews
   open).
3. A file existing only to help: none. The service catalogue reads as a real platform directory needed for the joins.
4. A figure or name reading as the answer: none. Softest tell: the capacity review's 2027 plan names partner-gateway's
   connection pools beside journey-search's index move. Ruled harmless (narrative, no figure; a careful run filing
   partner-gateway within budget on its own hourly count is not moved by it).
5. A filed sentence fixing a graded figure: PR-SLO-3 3.1 and 3.2, fixing every SLI's population and the incident
   adjustment. As designed.
6. One thing making most of the asks routine: no. Two pieces need analysis no file states: reconciling the span sample
   (about 284,000 server spans) against the balancer's 75.4 million December requests, and walking each December
   incident's spans to decide which named service owned the cause.

Realism notes: the balancer's hourly grid has no missing hour (ruled harmless: a balancer's per-minute counts export
whole, and the quietest target group's quietest hour still serves 93 requests); the incident titles read as ten canned
phrases with an "(N services)" suffix (fixed in the generator: each title is now the commander's phrasing of the
first-named service's symptom, drawn from the incident id, and no graded figure moved). Everything else read as
genuine: distinct container stamps, non-round durations with a long tail, 1,322 re-sent spans, multilingual reviews.
