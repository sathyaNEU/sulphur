# leak check, task14

**Verdict: REVIEW.** 12 files read, 64 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, carried, earlier, change, survey, record, missed, review, records, operators, reader, recorded, methods, tenancy, prompt, question, result, stands, golden, regions, office, lodged, reading, method, docket

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `pso_private_rents_measure_definition.pdf`: golden figure 2.5 appears: ...s at each tenancy's rent payable on its own day. 2.5 Breakdowns. With each quarter's measure the Offic...
- **REVIEW** `pso_private_rents_measure_definition.pdf`: golden figure 2.7 appears: ...Penmarra covers every dwelling in the comparison. 2.7 Coverage. Tenancies let without a bond lodged wit...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `pso_private_rents_measure_definition.pdf`: 10 of 25 stump-paragraph terms appear (earlier, change, survey, methods, tenancy, stands); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 2)
- **REVIEW** `pso_house_price_index_2026q3.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pso_private_rents_index_survey_2026q3.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `pso_suburb_region_concordance_2024.csv`: names 5 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `tbb_code_lists.xlsx`: names 5 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'pptx+xlsx' at 24% of 17 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 12 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: files[11].covers shares the design note's stump vocabulary (register, records, tenancy): say what the task decides, not how

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

One isolated reader (Sonnet, medium) on fresh copies of prompt.txt and target/, 2026-11-11. It solved nothing.

1. How-to sentences: the methods paper's 2.2 to 2.7 (tenancy cover, weekly conversion, the matched-dwelling ratio, the breakdowns, regions by suburb, bonded coverage) and section 3 (one decimal, a 90 per cent interval on the national figure); the prompt names no step. Ruling: harmless, the filed estimand (population, window, unit, comparison) the doctrine requires; none says where the rent payable on a day comes from, how a re-letting finds its earlier tenancy, or how December is reached.
2. Ranking files: none.
3. Helper files: the code lists and the concordance, as lookups. Ruling: harmless, the systems' own lookups, mapping codes without glosses.
4. Answer-like figures: none (the survey index's 4.0 is the retired survey series, a different measure). Ruling: harmless.
5. Literal sentences: 2.4, 2.2, 2.3, 2.6, 2.5, each executing to the golden's estimand. Ruling: no fork; every literal reading is the golden's quantity.
6. One thing: the methods paper as a full specification. Ruling: the reader's account of a route, overruled by measurement: the same definitions executed on the register's recorded rents file 4.2 for September and 2.7 for December (routes table, checks.py), outside their bands, because the register does not hold most rent rises, the operators' rents follow their own records, the migrated bonds carry no identifier and December's reviews and re-lettings are not yet on file.

Mechanical REVIEW items, reader's verdicts: the methods paper's and the events file's flagged numbers harmless (section numbers, dates, conversion constants; a rent beside a date); the house price index and the survey index harmless (unrelated or retired series, no ranking); the prompt names no method.

Realism notes, ruled: the events run to 27 November 2026 and the golden is dated 1 to 3 December, after the session's date: by design, the setting is forward (the December 2026 quarter, launched 27 January 2027) and the container gate's band accepts it; one landlord identifier across thousands of dwellings is the largest build-to-rent landlord, as the register holds it; named document authors are the fiction's own; small code lists and a 121-suburb concordance are the size those lookups have.

### Second read (after the prompt changed: "in place", and the split of the move from September to December)

One isolated reader (Sonnet, medium) on fresh copies, 2026-11-11. It solved nothing.
1. How-to: the methods paper's 2.2 to 2.7 and section 3; the prompt names no method. Ruling: harmless, the filed estimand.
2. Ranking files: none (the retired survey index is a different measure).
3. Helper files: the methods paper and the lookups. Ruling: harmless, the organisation's governing definition and its systems' lookups.
4. Answer-like figures: none.
5. Literal sentences: 2.4, 2.2, 2.3, 2.6 and the prompt's populations; nothing names an interval or decomposition method. Ruling: every literal reading is the golden's estimand.
6. One thing: the methods paper. Ruling: overruled by measurement as in the first read; the reader assumed the additional bonds give the rent in force ("rent changes via TOPUP rows"), which is the route that files 4.2 for September and misses every group figure.
Prompt wording: no method, warning, file name or presupposition about what the data hold (the reader noted the December figure must be forecast, which is the question).
Realism notes, ruled: every bond at four weeks' rent: fixed in the generator (now four, three or two weeks or a round sum); suburb names repeating a few endings: fixed (endings rotated); the mixed area-and-region column, the sparse property identifiers on events other than lodgements, and a one-row-per-suburb concordance are how those systems and lookups are kept.
