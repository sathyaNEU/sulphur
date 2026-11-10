# leak check, task9

**Verdict: REVIEW.** 13 files read, 29 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: recovery, loading, sector, carried, default, record, architecture, closed, missed, workout, economy, house-year, average, golden, sentence, pooled, defaults, five-year, carries, method, million, orders, workouts, estimator, patients

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `kestrel_lane_senior_note_term_sheet.pdf`: golden figure 15.0 appears: ...ecured floating rate notes due 2034 Subordination 15.0 per cent of the aggregate par of the collateral,...
- **REVIEW** `ostvale_senior_note_term_sheet.pdf`: golden figure 16.5 appears: ...and the equity retained by Ostvale together equal 16.5 per cent of the collateral principal balance, ab...
- **REVIEW** `ostvale_senior_note_term_sheet.pdf`: golden figure 15.0 appears: ...t of the collateral principal balance, above the 15.0 per cent Kadeweg's request for proposals of 2 Oct...
- **REVIEW** `phl_rated_note_standard_2026.pdf`: golden figure 2.2 appears: ...s from its portfolio date is below 1.0 per cent. 2.2 Where more than one note offered for the same all...
- **REVIEW** `phl_rated_note_standard_2026.pdf`: carries 10 of 13 distinctive words of the committed call: "Buy neither note: Kestrel Lane's chance of any loss of principal over 2027 to 2031 is 3.7 per cent at its 15.0 per cent "

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `kestrel_lane_senior_note_term_sheet.pdf`: 3 of 25 stump-paragraph terms appear (record, million, orders); read whether the document names the move
- **REVIEW** `phl_rated_note_standard_2026.pdf`: 7 of 25 stump-paragraph terms appear (recovery, default, record, closed, workout, defaults); read whether the document names the move

## 9 dates after the setting (REVIEW 4)
- **REVIEW** `euribor_forward_curve_2026-12-31.csv`: 24 ISO dates after 2027-02-17, e.g. 2027-03-28, 2027-06-28, 2027-09-28, 2027-12-31, 2028-03-28
- **REVIEW** `klcp_static_portfolio_2026-12-31.xlsx`: 98 ISO dates after 2027-02-17, e.g. 2027-03-02, 2027-04-02, 2027-04-06, 2027-04-19, 2027-04-22
- **REVIEW** `lenderbase_loan_performance_2008-2026.csv`: 19213 ISO dates after 2027-02-17, e.g. 2027-02-20, 2027-02-21, 2027-02-22, 2027-02-25, 2027-02-26
- **REVIEW** `ostvale_collateral_tape_20261231.xlsx`: 100 ISO dates after 2027-02-17, e.g. 2027-03-05, 2027-04-25, 2027-05-19, 2027-05-25, 2027-06-22

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Results-chain rebuild of architecture 7. One isolated Sonnet reader at medium effort, on target.zip 29757c9b (the
final build's pack, the same bytes as build 2's) with a fresh copy of prompt.txt and target/ only; it computed no
figure and gave no answer.

1. Decisive step: none. The nearest sentence is MP-RN-2 4.2 ("Credit standings are normally distributed and are
   correlated as far as the record of comparable loans shows them to be, and so is what lenders recover on the loans
   that default"), read as naming the model family and leaving open "the estimation of PD, correlation and LGD". It
   names no shock, grain, sector loading or owner; ruled the filed WHAT the literal reading needs (forks SF4 and SF14,
   the copula family and correlated recoveries), as the two reads of the single-step form ruled it.
2. Ranking file: none; the term sheets give the offered terms only.
3. Helping file: none; the sector crosswalk reads as the vendor's utility for the two tapes' taxonomies, and the
   reader took the deal file for a distractor.
4. Answer figure or name: none; 15.0 and 17.0 are the offered subordination, 1.0 per cent the standard's test.
5. Population sentences: MP-RN-2 2.1, 2.2, 3.1 to 3.5, 4.1 and 4.2, each executing to the golden's construction
   (portfolio date, static pool with ageing and like-for-like replacement, ECB rate of the cut-off, Lenderbase's
   defaults, each default's own unrecovered share booked in its year, the record from 2008 with its open workouts,
   Gaussian standings and recoveries correlated as the record shows).
6. What decides: estimation at every graded result (default chances, correlation and loss given default from the
   record, then the simulation); 4.2 settles the framework only, the recommendation is the test applied once the
   chances exist, and the reader named no file, column or pattern that settles most of the asks.

Sweep lines, each harmless: 15.0 and 17.0 are the offered subordination and 15.0 again the request for proposals'
floor in Ostvale's terms; 2.2 is a section number; the call's shared words are the standard's test; the vocabulary
lines are the standard's definitions of default, loss and the record, and the term sheet's deal words. The reader's
mild realism note (the standard is unusually well specified, 4.2 reads as written to pin the model) is kept as is:
without 4.2 the copula family is an open fork on R4 to R9.

Realism: largely realistic by the reader's verdict (a vendor-style multi-lender panel, two issuer tapes with
different conventions, plausible reference and distractor files); nothing padded or carrying a trap.

Sweep 9 (as of 2027-02-17): every later date is a loan's maturity (Lenderbase's maturity_date, both tapes' Maturity column) or a forward date on the EURIBOR curve, each in the future by nature.

After the stage-4 repair (cut 4a97e7b6): MP-RN-2 4.1, the Ostvale term sheet and both tapes' rating headers changed, and
the sweeps above were re-run on that cut; the reader above has not re-read it, because the build paused at stage 4.
