# leak check, task4

**Verdict: REVIEW.** 24 files read, 38 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: deliveries, missed, register, record, cellar, delivery, account, firkins, generator, reflex, kilderkins, nothing, change, dockets, weather, tagged, november, estate, purchase, whatever, interval, tracked, racking, monday, dropped

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `FS-04_returnable_container_fleet_issue3.pdf`: 8 of 25 stump-paragraph terms appear (deliveries, record, delivery, account, change, weather); read whether the document names the move
- **REVIEW** `pennine_seasonal_hire_terms_2027.pdf`: 5 of 25 stump-paragraph terms appear (register, delivery, november, purchase, monday); read whether the document names the move

## 9 dates after the setting (REVIEW 3)
- **REVIEW** `brew_plan_2027.xlsx`: 96 ISO dates after 2026-12-02, e.g. 2027-01-04, 2027-05-02, 2027-05-03, 2027-09-26, 2027-10-31
- **REVIEW** `calder_vale_station_weekly.csv`: 43 ISO dates after 2026-12-02, e.g. 2026-12-07, 2026-12-14, 2026-12-21, 2026-12-28, 2027-01-04
- **REVIEW** `maplestead_supply_agreement_schedules.xlsx`: 300 ISO dates after 2026-12-02, e.g. 2027-04-12, 2027-04-19, 2027-04-26

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 24 usable files (10 or more required)
- **INFO** `-`: 3 file categories: database, document, spreadsheet (2 or more required)

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: files.delivery_dockets_dec2023_nov2026.csv.covers shares the design note's stump vocabulary (delivery, dockets, november): say what the task decides, not how

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and `target/` (cut 7958b08792b776fb), 2026-11-17. It read the pack for leaks and computed nothing.

1. How any part of the analysis should be done: only the fleet standard's own clauses, which say what each quantity is (2.1 the requirement's parts and the float, 2.2 the fleet, 2.3 the shortfall, 3.1 the season, 3.2 the planning case, 3.3 the hot case, 3.4 the season as contracted and planned, 4.1 and 4.2 the cover and the minimum order run), with the quotation's "An order for an item below its minimum order run cannot be accepted", the hire terms' "Containers are hired in whole pallets" and "are not entered on the customer's register", and the supply agreement's "Each outlet is supplied once a week on its delivery day". Its words: "No file tells you how to estimate containers at customers or losses."
2. A file that ranks, scores or sizes the container types on the question: none. The quotation's minimum runs and the hire rates are price and order inputs; the brew plan is a volume plan; the counts and purchases are history.
3. A file that exists only to help the analyst: one suspect, `container_codes.csv`, "a mild dictionary" bridging the systems' codes. Ruled harmless below.
4. A figure or name that reads as the answer: none. The minimum order runs are the thresholds the cover rule needs.
5. Filed sentences that fix a computation: the standard's 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2 and 5.1, each fixing what a quantity is (parts, fleet, sign, season, cases, lines). Each executes to the golden's own definition (the design note's Literal reader). It noted that 2.1 does not list the packaging hall's clean empties, which the count sheets carry: they are fleet under 2.2 and no part of the requirement, which is how the golden reads them.
6. One thing that makes most of it routine: none. "FS-04 supplies definitions and the cover rule, but not the estimate of containers in trade or the losses." The cover is rule application once the planning figure exists; the planning and hot figures need analysis; nothing looks planted.

Realism: forward dates are plan dates; the count sheets share one layout and the same two signatories each year; the brew plan's runs and the agreement's schedule are round, as plans and schedules are; the three PDFs read as business documents; purchase prices rise gradually.

The sweep's date lines: `brew_plan_2027.xlsx` harmless (a forward plan issued 12 November 2026); `maplestead_supply_agreement_schedules.xlsx` harmless (listing dates in an agreement signed 23 October 2026); `calder_vale_station_weekly.csv` harmless if the recorded column is empty after the review date, which the reader did not verify. Verified in the main thread: 43 rows after 2 December 2026, none with a recorded value; the last recorded week begins 23 November 2026.

Rulings: no fix owed on questions 1, 2, 4, 5 and 6. Question 3, `container_codes.csv`: harmless, a master table of the five container types with their litres and the codes the docket and register systems use, which any brewery's systems keep; it glosses no column and says nothing of how the files fit. One realism repair made after this read: the station's weekly series behaves as the mean of the daily maximum (about 6 degrees in January and 21 in July), so its column is named for that.
