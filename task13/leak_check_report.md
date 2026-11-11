# leak check, task13

**Verdict: REVIEW.** 12 files read, 55 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: seasons, record, missed, spread, fitted, architecture, budget, window, events, radio-less, golden, baseline, referral, expectation, counts, result, controller, memory, confirmed, feeders, device, strokes, carried, months, logged

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `lightning_protection_refit_2027_programme_terms.docx`: 4 of 25 stump-paragraph terms appear (seasons, record, referral, strokes); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'whether' at 31% of 16 prompts (cap 30%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 12 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Isolated reader (general-purpose, Sonnet, medium effort), 2026-11-11, on fresh copies of prompt.txt and target/ only (architecture 2). Its answers, condensed with its quotations kept:

- Q1 (sentences that say how the analysis should be done): the programme terms' definitions, quoted: 3(a) "refers every zone whose lightning faults since its last cyclic inspection are more than its lines would have had with sound protection, under the lightning that fell near them, by more than chance explains"; 2(g) "The lightning near a zone's lines is the ground strokes the lightning location service placed within 400 m of them"; 2(e) the record "runs from the day after the inspection's repairs were completed to the end of the lightning season the rule is run after"; 2(c) "counted once, against the zone whose lines it was on, however many times breakers or reclosers trip and reclose on it"; 2(f) "the network's lightning faults in that season less the lightning faults its lines would have had in it with every zone's protection sound"; 3(b) "may refer a zone whose protection is sound no more than once in five lightning seasons on average"; 4(c) "taken in a season with the lightning of an average of the 2022 to 2026 lightning seasons"; 2(b) "from 1 April to 31 October"; 5 how the inspection check is scored. The reader: "every definition is a description of the estimand rather than a step-by-step recipe". The prompt names no method.
- Q2 (a file that ranks or scores the candidates): none.
- Q3 (a file that exists only to help): none is a readme or dictionary; nearest are the programme terms (a governing document), the inspection procedure (the inspection fields as crews record them) and the register's Substations sheet (a small lookup).
- Q4 (a figure or name that reads as the answer): none; no file lists zones to refer.
- Q5 (filed sentences that fix a computation literally): 2(e) with 3(a), the window from the day after the latest repairs to the season's end, observed against sound expectation with a chance test; 2(g), ground (type G) strokes within 400 m; 2(c), one fault however many trips; 2(f), the network's 2026 faults less the network's sound expectation; 4(c), the referred zones' excess at the 2022 to 2026 average lightning; 3(b), one sound zone in five seasons; 5, confirmed referrals and misses.
- Q6 (one thing that makes most of it routine): none; "No single column or file settles most of the asks. The expected-faults model, the fault de-duplication across three event sources, the chance threshold tied to the 3(b) budget, the back-test against later inspections and the average-season normalisation each need separate work." Per ask: the rule and the zones, analysis; the per-zone season faults, assembly with reading definitions, the expectation analysis; the referrals after each season and the sound referrals, analysis; the inspection comparison, the stated rule 5 with analysis in the counting; the network faults and 2026's from failed protection, counting by 2(c) and 2(f) plus the counterfactual's analysis; the avoided faults, 4(c) on top of the analysis. "I found nothing that looks planted."
- Extra note: no file or column name announces a trick; plausible unused files (transformer replacements, rain gauges, quotation); OMS free-text remarks against cause codes read as realistic mess; the inspection log header has a stray double period after "Inc."; the recloser downloads' "Clock Set" event, day-first controller time and some events stamped after their read time read as realistic clock mess, "nothing is annotated"; nothing dated after the setting.

Main-thread rulings: Q1 and Q5 quote the programme terms' definitions of what each result is (2(b), 2(c), 2(e), 2(f), 2(g), 3(a), 3(b), 4(c), 5); each executes literally to the golden and none names a clock, a memory, the seasons a rate is learned from or a spread: harmless, the filed WHAT. Q2 to Q4 none. Q6 none. Realism: the inspection log header's double period fixed in docs.py; events stamped after their read time are the controllers' own fast clocks, a property of the process, kept.
