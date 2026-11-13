# leak check, task22

**Verdict: REVIEW.** 22 files read, 24 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: station, industrial, riverside, pressure, correctors, missed, reflex, lakeview, sundquist, supercompressibility, stations, conditions, customer, booked, modelling, furnace, sentence, recorded, constructed, repeats, dual-fuel, decides, downtown, careful, factor

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `lauf_reduction_program_rules_2026.pdf`: golden figure 1.0 appears: ...twelve months ending September 30, 2026 exceeded 1.0 per cent of the gas delivered into it in the same...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `gas_rate_schedules_2026.pdf`: 4 of 25 stump-paragraph terms appear (industrial, pressure, customer, factor); read whether the document names the move
- **REVIEW** `gas_temperature_study_memo_2025-06.pdf`: 5 of 25 stump-paragraph terms appear (riverside, lakeview, sundquist, recorded, downtown); read whether the document names the move
- **REVIEW** `lauf_reduction_program_rules_2026.pdf`: 9 of 25 stump-paragraph terms appear (station, pressure, correctors, stations, conditions, customer); read whether the document names the move
- **REVIEW** `lauf_study_fy2019_consultant_report.pdf`: 3 of 25 stump-paragraph terms appear (station, pressure, factor); read whether the document names the move

## 6 ranking artifacts (REVIEW 4)
- **REVIEW** `gas_temperature_study_memo_2025-06.pdf`: names 3 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `premise_meter_register_2026-11-02.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `third_party_damage_reports_2023-2026.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `utility_own_use_2023-2026.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `meter_changeout_plan_2027.xlsx`: 976 ISO dates after 2026-11-05, e.g. 2027-04-05, 2027-04-06, 2027-04-07, 2027-04-08, 2027-04-09

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 33% of 24 prompts (cap 30%); deliverable set 'pptx+xlsx' at 25% of 24 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 22 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## Solver's-eye read

Architecture 2, redesign loop 1 (2026-11-13), one isolated reader (general-purpose, Sonnet, medium) on fresh copies of
`prompt.txt` and `target/` only, after the realism sweep. Its answers, then the main thread's ruling on each.

1. **How the analysis should be done.** Quoted the program rules' Rule 1, Rule 2 and Rule 3, the rate schedules'
   billing volume, Schedule G-3 billing, estimated bills and gas day, and the 2025 memo's straight line on the air.
   Ruling: harmless. Each is the WHAT the governing documents file (the decision lines, the estimand's terms, the
   billing conventions); none names a step any graded result turns on. The memo's line is the incumbent method, which
   reproduces exactly from its own loggers and which the golden supersedes; the temperature work is a reflex.
2. **A file that ranks the districts.** None. Ruling: agreed.
3. **A file that only helps the analyst.** None; two footnote rows inside the LAUF report and the own-use sheet
   describe that sheet's own scope. Ruling: harmless, each is the issuing team's own note on its own figures.
4. **A figure or name that reads as the answer.** The 2027 plan's two districts with Rule 3. Ruling: harmless, filed by
   design (Rule 3 keeps the scheduled Old Town and Downtown changeouts out of Rule 2, and both districts sit below the
   3.5 per cent line anyway); the city-wide LAUF figure is a reconciliation anchor, as the reader says.
5. **Sentences that fix a graded quantity.** The rules' leak loss and base conditions, the customers including the
   corrector accounts, own use as the station heaters, under-registration, and gas taken without authorization. Each
   executes to the golden: the golden subtracts every term at base conditions, counts the corrector customers, keeps
   the gate heater out, and books only bypasses and taps. The reader read Schedule G-3's corrected volume as already at
   base conditions; that literal reading of a billing description is the hurried route the chain prices (the rules'
   base conditions and the EVC-II stations' records refute it), not a fork.
6. **One thing that settles most of it.** The program rules as a whole, for the two lines and the carve-out; the
   reader found that it settles only the final comparisons, and that the balance, the gas temperature and the
   unauthorized-use detection stay analysis. Ruling: harmless; no sentence or file names the supercompressibility, the
   May test or the cold-day test, and the reader made none of them.

**Flagged files.** The memo, the register, the damage reports and the own-use sheet: harmless (raw records, no score).
The 2027 plan's dates after the extracts: natural for a forward plan. The prompt: harmless.
**Realism.** No em dash, no generated tell, PDF and workbook metadata consistent with each issuer and date.
**Reader's verdict and ruling.** The reader wrote LEAK on the filed thresholds and the carve-out; ruled harmless above:
the thresholds are the decision lines the governing document must file, and nothing in the pack hands over a step a
graded result turns on.
