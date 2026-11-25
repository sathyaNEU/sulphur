# leak check, task6

**Verdict: REVIEW.** 16 files read, 45 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: export, journey-search, places, metrics, seat-map, partner-gateway, hourly, bucket, causes, leaves, weights, missed, balancer, record, sample, shortcut, design, method, notifications, pr-slo-, evidence, nothing, another, shares, payments

## 1 file names (REVIEW 1)
- **REVIEW** `capacity_review_2026-Q4.md`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 1.0 appears: ...rney-search 1 1,500 1.0% fares 1 300...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 0.5 appears: ...booking 1 2,500 0.5% payments 1 1,000...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 2.3 appears: ...own health probes are not requests. 2.3 The server-side duration of a request is the dur...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: golden figure 2.0 appears: ...accounts 1 600 2.0% partner-gateway 2...
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: carries 10 of 13 distinctive words of the committed call: 'Put reliability engineers on partner-gateway, places, fares, seat-map and notifications, in that order: the five ran ove'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: 11 of 25 stump-paragraph terms appear (journey-search, places, seat-map, partner-gateway, balancer, record); read whether the document names the move
- **REVIEW** `capacity_review_2026-Q4.md`: 6 of 25 stump-paragraph terms appear (journey-search, places, seat-map, partner-gateway, notifications, payments); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: deliverable formats: asks for a written document (report.docx): the house set is a CSV, a workbook and at most a deck; keep one only where the decision's reader needs it, with the reason in the design note

## 12 describing content (REVIEW 1)
- **REVIEW** `PR-SLO-3_service_level_objectives_2026.docx`: names 14 column(s) of the data files verbatim (Service, Tier, commit, component, cost, deployment): confirm it is the organisation's own record and not a note written for the analyst

## 12 client quality check (INFO 2)
- **INFO** `-`: 16 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


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

## Solver's-eye read (repaired cut, 2026-11-25)

One isolated reader (general-purpose, Sonnet at medium) on a fresh copy of prompt.txt and the sixteen files of
target.zip; it solved nothing.

1. Method-telling text: PR-SLO-3's definitions only (2.1, 2.2, 3.1, 3.2, 5.2, 5.4), and the prompt's ordering
   clause and "counting it from when the incident tool added it". No sentence names a step, a weighting, a
   comparison or an adjustment.
2. Ranking file: none.
3. Analyst-only file: none (capacity_review_2026-Q4.md read as context that is not needed).
4. Answer-like figure or name: none; the standard's table holds thresholds and budgets, and
   incidents_2026.csv's root_cause_service is context for closed reviews.
5. Filed sentences that fix a computation: PR-SLO-3 2.1 and 2.2 (over-threshold requests over all requests a
   service handled, kept or not), 2.3 (the service's own server span), 3.1 (December, Lisbon time), 3.2 (incident
   time left out unless the service owned the root cause), 3.3 (owning a root cause), 3.4 (a breach), 5.2 and 5.4
   (the minutes and the halves). Each executes to the golden's population and windows.
6. One thing: none. The reader's nearest candidate is 2.2 with the catalogue's name mapping, which sets up the
   SLI's denominator and settles no result.

Rulings on the mechanical REVIEW lines: the capacity review is Platform Infrastructure's own record and describes
no data file (harmless); PR-SLO-3's coinciding figures are its own thresholds, budgets and a section number, and
its service names are the catalogue's (harmless); PR-SLO-3 is the organisation's standard, not a note for the
analyst (harmless); the prompt's report and CSV are deliverables by type (harmless).

Realism notes, each checked in the main thread: the timeline's "event" row is the file's header; incident ids step
unevenly (3 to 17), not by a fixed 8; the H1 and H2 balancer exports differing in layout is the July rename, as
filed in the catalogue.

