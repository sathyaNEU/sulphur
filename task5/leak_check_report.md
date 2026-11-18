# leak check, task5

**Verdict: REVIEW.** 14 files read, 44 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: arrivals, register, missed, shares, departures, record, counts, closed, registered, generator, orlava, arrival, skarholm, fenmark, reflex, dismissed, evidence, reports, events, different, people, fullest, recorder, nothing, dropped

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `consular_establishment_order_14_2025.pdf`: carries 16 of 19 distinctive words of the committed call: 'Set the 2027 to 2029 establishment at 8 officers in Skarholm, 10 in Brennia, 8 in Marovia, 7 in Tesmar, 3 in Kestria, 5 '

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `consular_establishment_order_14_2025.pdf`: 6 of 25 stump-paragraph terms appear (register, registered, orlava, skarholm, fenmark, reports); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
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

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and the pack as judged (stage 4, 2026-11-17). It solved nothing and saw no design file. Its answers, then the build's ruling on each.

1. Sentences that say how part of the analysis is done: it quoted the Order's clauses 2.1 (one officer for every 5,000 citizens or part, on 1 January of the cycle's first year), 2.4 (each district on its own, no smallest or largest establishment) and 4.1 (emigrations from the last census to the day before that date); the Board's request (the two quantities asked for); Regulation 7/2009 articles 2(a) to 2(e), 3, 4(1), 5, 6(2), 6(3) and 7(1) (usual residence, immigration and emigration, citizenship as registered on arrival, the reference year, the tables, the releases and the codes); and the header of the establishment in force ("set ... on the census counts of 1 January 2021"). Ruling: harmless. Each is the organisation's definition of what is counted, when and in which unit, or a release rule every run applies by reflex. None says what a state's tables hold or miss, which record sees which part of the count, or how the years after 2023 are reached. The reader's own summary: "No single sentence resolves it; the work is assigning each part of the estimand to the source that sees it. The files themselves do not say this."
2. A file that ranks or scores the districts on the question: none (the establishment in force is the previous allocation).
3. A file that exists only to help the analyst: none. The code list and the municipality list are reference tables a register keeps; no dictionary, readme or notes file.
4. A figure or name that reads as the answer: none. No file holds a 2027 figure.
5. Filed sentences that fix a graded figure's computation or population: the Order's 2.1 to 2.4 and 4.1, the request, and the Regulation's 2(c), 2(d), 2(e), 4(1) and 6(3). Ruling: executed literally they give the golden's estimand (Orlavan citizens usually resident in the district on 1 January 2027, whole persons, each district alone; emigrations whatever the state moved to, from 1 January 2021 to 31 December 2026; the latest release of a cell) and fix no estimate.
6. One thing that makes most of it routine: none named. Part by part it read the officers as a stated rule on top of an estimate, and the citizens, the leavers and the yearly account as analysis and reconciliation of several sources. The register's mixed state codes and texts, its entries after the move date and the restated releases read to it as normal register mess.
7. `consular_establishment_order_14_2025.pdf` (flagged by the sweep for sharing words with the recommendation): harmless, a legal order that states the rule, the date, whole persons and independent districts; it does not name how the 2027 population is estimated.
8. Realism: (a) the states' whole populations were round (3,910,000 in 2011, totals ending in 00 in 2021). Fixed in the generator: each state's whole population has its own level and growth on a stream of its own, so only the own-citizens cell and the total of each state changed in the census workbook, the 2016 count and the population file; no foreign-citizenship cell moved and every golden file is byte for byte as before (`checks.py`, realism). (b) The establishment in force equals the 5,000 rule on the 2021 census counts: that is the Board's own earlier decision under the same kind of order, and it is what the request says. (c) File stamps of different years (the 2021 census table in 2022, the 2016 count in 2017): each is its issuer's own save date. (d) The register's mixed state text: the clerks' free text, by design of the register. Nothing else quoted.

Verdict of the read: no leak, no helping file, no ranking artifact, one realism tell fixed. The fix changed data cells only (no document, no sentence of the prompt), so the reader was not run again; `leak.py` was re-run on the final cut (REVIEW, the same two lines, ruled in the design note).
