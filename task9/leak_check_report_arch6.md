# leak check, task9

**Verdict: REVIEW.** 13 files read, 20 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: default, record, sentence, effect, copula, architecture, carried, dependence, method, decisive, golden, factor, sponsor, house-year, million, dealtrail, buyout, component, carries, letter, sector, standard, fitted, industry, question

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `kestrel_lane_senior_note_term_sheet.pdf`: golden figure 15.0 appears: ...ecured floating rate notes due 2034 Subordination 15.0 per cent of the aggregate par of the collateral,...
- **REVIEW** `ostvale_senior_note_term_sheet.pdf`: golden figure 15.0 appears: ...and the equity retained by Ostvale together equal 15.0 per cent of the collateral principal balance, th...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `kestrel_lane_senior_note_term_sheet.pdf`: 4 of 25 stump-paragraph terms appear (record, sponsor, million, industry); read whether the document names the move
- **REVIEW** `ostvale_senior_note_term_sheet.pdf`: 3 of 25 stump-paragraph terms appear (sponsor, million, industry); read whether the document names the move
- **REVIEW** `phl_rated_note_standard_2026.pdf`: 5 of 25 stump-paragraph terms appear (default, record, effect, sponsor, standard); read whether the document names the move

## 9 dates after the setting (REVIEW 4)
- **REVIEW** `euribor_forward_curve_2026-12-31.csv`: 24 ISO dates after 2027-02-17, e.g. 2027-03-28, 2027-06-28, 2027-09-28, 2027-12-31, 2028-03-28
- **REVIEW** `klcp_static_portfolio_2026-12-31.xlsx`: 95 ISO dates after 2027-02-17, e.g. 2027-02-22, 2027-04-15, 2027-06-22, 2027-08-06, 2027-09-28
- **REVIEW** `lenderbase_loan_performance_2008-2026.csv`: 19066 ISO dates after 2027-02-17, e.g. 2027-02-18, 2027-02-19, 2027-02-22, 2027-02-23, 2027-02-24
- **REVIEW** `ostvale_collateral_tape_20261231.xlsx`: 99 ISO dates after 2027-02-17, e.g. 2027-03-06, 2027-03-12, 2027-05-21, 2027-07-20, 2027-07-28

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'csv+docx' at 22% of 9 prompts (cap 20%); reword at the role level, not the verb
- **REVIEW** `prompt.txt`: templating signals: 1 of seven: files listed up front (ic_note_senior_notes_2027.docx, senior_note_loss_by_year.csv) (the portal marks two as borderline and three as templated: one question, each file named in the sentence that gives its reason, no closing list)

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## Solver's-eye read

Four isolated reads (general-purpose, Sonnet at medium), each given only a fresh copy of prompt.txt and target/, never the
design note, generator, submission or reports. Read 1 ran on 2e83c33f with a stale prompt; reads 2, 3 and 4 on 150c10c4,
076bb4b7 and the final cut 2e2598bc.

1. Decisive step: none at any read. The nearest sentence named each time is MP-RN-2 4.2 ("Credit standings are normally
   distributed and are correlated as far as the record of comparable loans shows them to be"), read as the method family
   (a Gaussian latent-factor model) "but not how to estimate the correlation" (read 4), with "no grouping, sector or
   country structure" (read 4) and no "sector, country, factor, vintage or any correlation estimator" (read 3).
2. Ranking or scoring file: none at any read.
3. Helper-only file: none; the sector crosswalk reads as a vendor code map and the standard as a governing document.
4. Answer-like figure or name: none; the 15.0 per cent subordination reads as context ("as the request for proposals
   asked").
5. Filed sentences: MP-RN-2 2.1, 3.2, 3.4, 3.5, 4.1 and 4.2, each read literally to the golden's construction (a static
   pool that ages, the ECB rate of the cut-off, Lenderbase's defaults, one average loss over every comparable default
   with open workouts included and booked at default, a defaulted loan leaving the pool, cumulative loss against
   subordination, the 2008 to 2026 record, Gaussian standings correlated as the record shows).
6. What decides the answer: an analytical choice at every read ("how to estimate default chance and correlation from the
   record, including age and rating dependence and the unresolved workouts", read 4).

Sweep lines ruled by the readers: the term sheets' shared number is the offered subordination, an input (harmless); the
EURIBOR forwards and the loans' maturities are contractual future dates (harmless); no submission or report date passes
the pulls (harmless); the deliverable names give away no method (harmless).

Fixed from the reads: read 1, the prompt's stale 1.5 per cent bar and single target (now the standard's 1 per cent and the
three targets at one decimal), the two term sheets written in one template (now two layouts and voices), the trimmed ECB
file (now its thirty currencies); read 3, the tapes' creator field (the namespace attribute had slipped the scrub).
Prompt and standard agree on every threshold and rounding at reads 2, 3 and 4.
