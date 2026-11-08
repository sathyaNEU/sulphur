# leak check, task9

**Verdict: REVIEW.** 13 files read, 17 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: recovery, default, house-year, record, defaults, carried, architecture, sentence, closed, workouts, counts, latent, decisive, workout, average, cohorts, sponsor, companies, economy, inferred, patients, co-defaults, golden, million, recoveries

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `kestrel_lane_senior_note_term_sheet.pdf`: golden figure 15.0 appears: ...ecured floating rate notes due 2034 Subordination 15.0 per cent of the aggregate par of the collateral,...
- **REVIEW** `kestrel_lane_senior_note_term_sheet.pdf`: golden figure 2.5 appears: ...rs may be added Portfolio limits No obligor above 2.5 per cent and no industry above 15 per cent of agg...
- **REVIEW** `ostvale_senior_note_term_sheet.pdf`: golden figure 13.0 appears: ...and the equity retained by Ostvale together equal 13.0 per cent of the collateral principal balance and...
- **REVIEW** `ostvale_senior_note_term_sheet.pdf`: golden figure 15.0 appears: ...lass A notes. Kadeweg's request for proposals set 15.0 per cent; Ostvale offers the thinner enhancement...
- **REVIEW** `phl_rated_note_standard_2026.pdf`: golden figure 1.0 appears: ...calendar years from its portfolio date is below 1.0 per cent. 2.2 Where more than one note offered fo...
- **REVIEW** `phl_rated_note_standard_2026.pdf`: golden figure 2.2 appears: ...s from its portfolio date is below 1.0 per cent. 2.2 Where more than one note offered for the same all...
- **REVIEW** `phl_rated_note_standard_2026.pdf`: golden figure 3.5 appears: .... Interest, fees and excess spread are left out. 3.5 Subordination: the share of the portfolio's par t...
- **REVIEW** `phl_rated_note_standard_2026.pdf`: carries 15 of 20 distinctive words of the committed call: "Buy neither note: Kestrel Lane's chance of any loss of principal over 2027 to 2031 is 3.9 per cent and Ostvale's 7.8 per"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `kestrel_lane_senior_note_term_sheet.pdf`: 3 of 25 stump-paragraph terms appear (record, sponsor, million); read whether the document names the move
- **REVIEW** `ostvale_senior_note_term_sheet.pdf`: 3 of 25 stump-paragraph terms appear (sponsor, companies, million); read whether the document names the move
- **REVIEW** `phl_rated_note_standard_2026.pdf`: 7 of 25 stump-paragraph terms appear (recovery, default, record, defaults, workouts, workout); read whether the document names the move

## 9 dates after the setting (REVIEW 4)
- **REVIEW** `euribor_forward_curve_2026-12-31.csv`: 24 ISO dates after 2027-02-17, e.g. 2027-03-28, 2027-06-28, 2027-09-28, 2027-12-31, 2028-03-28
- **REVIEW** `klcp_static_portfolio_2026-12-31.xlsx`: 97 ISO dates after 2027-02-17, e.g. 2027-04-15, 2027-04-16, 2027-04-20, 2027-08-06, 2027-11-05
- **REVIEW** `lenderbase_loan_performance_2008-2026.csv`: 19066 ISO dates after 2027-02-17, e.g. 2027-02-18, 2027-02-19, 2027-02-22, 2027-02-23, 2027-02-24
- **REVIEW** `ostvale_collateral_tape_20261231.xlsx`: 100 ISO dates after 2027-02-17, e.g. 2027-03-06, 2027-06-19, 2027-08-19, 2027-08-21, 2027-08-28

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: shell quota: question form 'whether' at 33% of 9 prompts (cap 30%); second-sentence opener 'the' at 22% of 9 prompts (cap 20%); deliverable set 'csv+docx' at 22% of 9 prompts (cap 20%); reword at the role level, not the verb
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

Architecture 7. Read 1 on target.zip bed0980b and read 2 on the final cut 7c395ae0, each an isolated Sonnet reader at
medium effort with a fresh copy of prompt.txt and target/ only.

1. Decisive step: none at either read. The nearest sentences, MP-RN-2 3.4, 4.1 and 4.2, name the model family
   (Gaussian standings correlated as the record shows, recoveries with them, the open workouts kept) and not which
   shock recovery moves with or at which grain; read 2: "hands over the model family ... but not the estimation".
2. Ranking file: none; the term sheets give the offered terms only.
3. Helping file: none; the sector crosswalk reads as the vendor's utility for two managers' scales.
4. Answer figure or name: none; 15.0 and 13.0 are the offered subordination, the 1 per cent the standard's test.
5. Population sentences: MP-RN-2 2.1, 2.2, 3.1 to 3.5, 4.1 and 4.2, each executing to the golden's construction
   (portfolio date, static pool with ageing, ECB rate of the cut-off, Lenderbase's defaults, each default's own loss
   booked at default, the record with its open workouts, the record's conditions, correlated standings and recoveries).
6. What decides: an analytical choice at both reads (how the record shows default and recovery moving together,
   estimated from Lenderbase and Dealtrail); read 1 noted 4.2 writes the model's form down, ruled in the design note's
   Stage 4 as the filed WHAT the literal reading needs.

Read 1's one finding, fixed in the generator: Ostvale's term sheet sized its Class A notes at 85 per cent of par
against its 13.0 per cent enhancement; both term sheets now size the notes as par less the stated enhancement
(checks.py K19), and read 2 found both consistent. Sweep lines: every one harmless at both reads (the offered terms,
the standard's test and section numbers, maturity and forward dates, the prompt's voice warnings).

Realism: nothing generated-looking beyond synthetic names; the two tapes carry different schemas and rating scales,
the ECB file thirty currencies, the Lenderbase extract mixed code vocabularies and date formats.
