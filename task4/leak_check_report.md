# leak check, task4

**Verdict: REVIEW.** 13 files read, 17 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, exposure, blocks, landings, golden, careful, standard, record, counts, in-house, missed, method, removal, aircraft, winter, replay, result, partly, shortcut, modelling, carried, programme, graded, component, energy

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `pool_support_offer_2026.pdf`: \bdesign note\b|\bgenerator\b x1: ...fee per aircraft (NOK) Exchange fee per unit (NOK) 23085-016 Starter-generator 673 48,842 2-1577-3 Main wheel brake assembly 232 23,867 3214552-2 Bl...
- **REVIEW** `reliability_report_2026-10.pdf`: \bdesign note\b|\bgenerator\b x3: ...ol Unscheduled removals MTBUR (FH) No fault found 23085-016 Starter-generator 2 5 47 1,226 28% 2-1577-3 Main wheel brake assembly 4 5 42 2,744 5% 3...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `pool_support_offer_2026.pdf`: 3 of 25 stump-paragraph terms appear (removal, aircraft, component); read whether the document names the move
- **REVIEW** `reliability_programme_and_spares_standard.pdf`: 6 of 25 stump-paragraph terms appear (standard, record, removal, aircraft, programme, component); read whether the document names the move
- **REVIEW** `reliability_report_2026-10.pdf`: 3 of 25 stump-paragraph terms appear (standard, removal, aircraft); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `fleet_register.xlsx`: 36 ISO dates after 2026-11-30, e.g. 2026-12-19, 2026-12-31, 2027-01-12, 2027-01-14, 2027-01-19
- **REVIEW** `flying_programme_2027.xlsx`: 2300 ISO dates after 2026-11-30, e.g. 2027-01-01, 2027-02-01, 2027-03-01, 2027-03-27, 2027-03-28

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read (architecture 12, stage 4, 2026-11-12, one isolated reader on target.zip 183ee655a14c4f36; answers condensed, rulings by the main thread)

1. Method stated: the standard's 3.2 (MTBUR per flight hour, the report's own measure), 4.2 to 4.4 (the fill rate over the year's removals, 95 per cent, the 80 per cent range with the rate's own uncertainty) and 5.1 (the 1.5-removal withdrawal test). The reader: "These fix the estimand/rule ... but not the forecasting method itself." Ruling: the filed WHAT, by design; harmless.
2. Ranking or scoring the candidates: the October report's section 3, "2027 removals at October's MTBUR", a projection of every part's 2027 removals at the trailing MTBUR on the programme's planned hours, which "a hurried solver could copy"; and section 4's budget line replacing every listed serial. Ruling: the budget line is the incumbent's plan, which ask 5 prices on the golden's footing (the saving of the whole list); section 3 is ruled with the judge's Gate G classification (repair pass below).
3. Files whose only job is to help: none; the standard reads as a governed CAME document.
4. Figures that read as answers: the same section 3 column and the budget line; as in 2.
5. Filed sentences fixing a computation: 2.1 (the unscheduled population), 2.3 (the pool), 3.3 (the watch list), 4.1 (the units in service under the 2027 programme), 5.2 (the saving counted for the position). Ruling: each executes to the golden's estimand (fork table SF1, SF4, SF6, SF7, SF9, SF10).
6. One thing that settles most of it: none. Work left ungiven: flight hours as air time against block time (the report's 28,810 reproduces on air time; the programme states block minutes), ordinary hygiene in the component changes (the -R1 corrections, the install-only fits, the 2023 part numbers without dashes), and each serial's own removal propensity. By ask: the removals and ranges turn on analysis, the spares and withdrawals on analysis with the standard's rule at the end, the change against the pool on reading 2.3 against the snapshot once the spares are known. Ruling: no banned finding; the air-time convention gets its own fork row (SF17) asserted in checks.py.
Mechanical flags: (a) the register's planned checks and the 2027 programme are planning files whose future dates are the point; harmless. (b) nothing reads as generated; the roster's fixed 7.5-hour shifts suit a three-person shop.

## Solver's-eye read, reader 2 (architecture 12, stage 4 repair, 2026-11-12, one isolated reader on target.zip 8bd9892f7f054b07; condensed, rulings by the main thread)

1 and 5. The standard's 2.1, 4.3, 4.4, 5.1 and 5.2 quoted as fixing what each ask means: the unscheduled population, the fill-rate objective, what the 80 per cent range carries, the withdrawal threshold and the saving's unit of account. The reader's own breakdown leaves each part's 2027 rate, the step from a forecast and a turnaround to a stock-out probability ("no formula given anywhere") and each serial's own rate as analysis. Ruling: the filed WHAT, each executing to the golden's estimand (SF1, SF3, SF5, SF8, SF9); harmless.
2. No file forecasts a 2027 figure or ranks parts or serials on buy, cut or scrap; the report's MTBUR table and watch list are last year's reliability and the candidate universe. The repair holds.
3. None. 4. Nothing names itself as the answer.
6. No single fact: what stays open is the 2027 rate per part under the new programme, the bulletin's effect read from the snapshot and the repairers' orders, and a rogue's signature found only by joining the changes' dwell times to the repairers' findings. Ruling: analysis throughout, no banned finding.
Realism: nothing reads as generated (invoice amounts in three currencies at their own rates, a gradual engine-trend drift, FERIE and SYK absence codes, a rogue's repeat no-fault-found pattern that reads as real behaviour).
