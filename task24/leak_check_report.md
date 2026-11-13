# leak check, task24

**Verdict: REVIEW.** 22 files read, 52 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: corvane, ardley, objects, shelfgrid, shortcut, missed, method, kestrin, hurried, reflex, re-return, carried, tracks, screen, object, images, projects, closed, modeling, brindle, record, re-review, per-object, accepts, annotators

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `pricing_policy_FIN-POL-04.pdf`: golden figure 1.55 appears: ...d in proportion to review time; (c) overhead: USD 1.55 per paid hour of annotators and of reviewers on t...
- **REVIEW** `pricing_policy_FIN-POL-04.pdf`: golden figure 1.18 appears: ...e client offers per image (per frame) is at least 1.18 times its expected cost of delivery. Where it is...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `annotator_pay_policy_2026.pdf`: 3 of 25 stump-paragraph terms appear (object, record, annotators); read whether the document names the move
- **REVIEW** `pricing_policy_FIN-POL-04.pdf`: 3 of 25 stump-paragraph terms appear (projects, record, annotators); read whether the document names the move
- **REVIEW** `qa_review_standard_QA-STD-03.pdf`: 3 of 25 stump-paragraph terms appear (objects, missed, object); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 32% of 22 prompts (cap 30%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 22 usable files (10 or more required)
- **INFO** `-`: 4 file categories: database, document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## Solver's-eye read

Isolated reader (Sonnet, medium effort), fresh copies of prompt.txt and target/ only, 2026-11-13.

1. How-to sentences: the pricing policy's cost definition, its three cost lines, the sharing of a week's pay across projects by tool active time and of a reviewer's paid time by review time, the staffing basis (the roster at the costing date, shares by contracted hours) and paid time from the punch clock; the pay policy's punch rules and unpaid corrections; the QA standard's fourth-review acceptance. The prompt names no method. Ruling: the filed WHAT (what is counted and how a cost is allocated), pinning R1, R5 and R6's estimand; none names an estimation step.
2. Ranking or scoring file: none.
3. Files only to help the analyst: none (the three policies are governing documents; the preview JSONs are the requests' samples).
4. Figures that read as the answer: the pay register's "period totals" sheet, a monthly summary of piece pay, top-ups, reviewer pay, allowances, adjustments and gross. Ruling: harmless; the workbook's own summary, reconciled to the weekly sheets once the voided re-run nets out (verify.py asserts it); its gross includes allowances and adjustments the pricing policy leaves out of the cost lines, and R1 also needs the overhead on paid hours.
5. Literal readings: the cost per delivered image as the three lines with USD 1.55 per paid hour; allowances, adjustments and compute left out; a week's pay split by tool active time; staffing by the current roster; accept at price at least 1.18 times cost, the decline floor at 1.18 times cost; the floor, paid hours and the Monday to Sunday week; the return rule and the fourth review. Each is the golden's convention.
6. One thing: none filed or planted settles most of the prompt; the pricing policy settles the framing and the accept line, while the estimates (work, returns and re-returns from the previews and the history, the range) remain open work.

Rulings on the REVIEW lines: (a) the pricing policy's two figures, harmless (filed conventions, not computed results); (b) the question-form quota, harmless (a style quota).
