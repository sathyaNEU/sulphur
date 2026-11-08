# leak check, task5

**Verdict: REVIEW.** 12 files read, 51 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: quarters, missing, outcome, closed, register, reading, section, account, ostrom, transmission, lateness, imputation, design, nothing, history, agreement, decisive, window, division, garrow, statewide, bureaus, sentence, outcomes, status

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `ui_contribution_rate_notice_2027.docx`: golden figure 3.0 appears: ...6.9 1.90 3.0 to 4.9 2.50...
- **REVIEW** `ui_contribution_rate_notice_2027.docx`: golden figure 0.0 appears: ...2.9 3.20 0.0 to 0.9 4.00...
- **REVIEW** `ui_contribution_rate_notice_2027.docx`: golden figure 0.1 appears: ...4.00 -2.0 to -0.1 5.10 -4.0...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `community_transition_fund_act_2026.docx`: 3 of 25 stump-paragraph terms appear (section, account, design); read whether the document names the move
- **REVIEW** `ui_lmi_data_sharing_agreement_2025.docx`: 7 of 25 stump-paragraph terms appear (closed, section, account, history, agreement, division); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 12 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 3, read 1 on target.zip 250434913d558e4b (md5 882e5301b1d84d153bf7784bbdd57c7a), an isolated Sonnet
reader at medium with a fresh copy of prompt.txt and target/ only, 2026-11-08.

1. Decisive step: no sentence or file states how a missing report becomes a December 2026 figure; the nearest are the
   prompt's "how many of them are estimated for employers whose report had not arrived" and the Act's section 2(c)
   ("as reported or estimated"), which fix that an estimate is owed and for whom, never how.
2. Ranking file: none; no December 2026 figure exists anywhere. The published Q4 2025 county table gives each county's
   December 2025 jobs, and the reader rebuilt it exactly from the raw files.
3. Helper file: franklin_county_codes.csv, a bare code-to-name, region and seat table with no letterhead.
4. Answer-like figure: the published table's December 2025 column (the other half of the comparison, finished).
5. Literal sentences: the Act's 2(c) (every liable employer, filed or not, needs a figure), 2(d) (liable on any day of
   the quarter, read against the history's effective dates), 5(a) (both Decembers from the reports in by 15 February),
   Schedule C (a closure's effective date is the first day with no workers, so an account closed before 12 December
   reads as nought), Schedules B and D (multiple worksite employers through the worksite file).
6. What decides: an analytical choice; everything mechanical is written down, and no file says how to produce a
   December figure for a liable employer that has not filed. Flagged: the inactivation reason text "NO WAGE REPORTS 2
   QTRS" could be mistaken for an estimation rule.
7. Realism: thousands of reports share one received_at second (892 on one stamp); the three PDFs name ReportLab as
   Creator; every CLOSED and INACTIVATED change takes effect on the first of its month (3,842 of 3,842); the published
   table reconciles to the raw files with no residual.
   Rate notice: background (a tax-rating schedule on a June 30, 2026 computation date, no county, no employment); its
   "-2.0 to -0.1" band is a coincidence of digits.

Rulings (main thread):
- 1, 6: no announcement; the decisive step is an analytical choice. Pass.
- 2, 4: harmless. The published table answers another question correctly (December 2025, a final vintage released after
  every amendment to those reports had arrived), which every route files the same way; SF7 asserts the tie.
- 3: harmless. A code crosswalk the Department keeps is data (reduce-house-fixes H9), and it carries no gloss.
- 5: Schedule C read literally was a live fork: one outstanding employer's closing notice had been entered by the
  cut-off while its final report rode its agent's late batch. Fixed in the generator: a notice of closing is entered
  with the employer's final report, and checks.py asserts that no outstanding employer carries a closure effective by
  12 December entered by the cut-off (SF1). The other four sentences execute to the golden.
- 6, the reason text: harmless. It is the Division's own inactivation trigger, which cues the default path's
  two-quarter refinement (R1x), not the decisive step.
- 7, shared seconds: harmless. A payroll agent's file of reports is received at once and the Division's system stamps
  each report with the file's receipt time ("the date and time the Division's system received the report",
  Schedule A); it is the organ the decisive step reads, and most of the file's rows are not in one.
- 7, ReportLab: harmless. A PDF keeps the library that wrote it in Producer and Creator, with the issuing organisation
  as Author and a real Subject (reduce-house-fixes H1).
- 7, closing dates all on the first: fixed. An employer's notice of closing now names the day after its last payroll
  (any day between the pay period including the 12th of its last month with workers and the next one), and checks.py
  asserts the spread; the Division's own inactivations keep the first of the month.
- 7, the published table's exact tie: harmless, as under 2 and 4.
- Rate notice: harmless (design note, Oracles).
