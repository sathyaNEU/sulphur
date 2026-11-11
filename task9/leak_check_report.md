# leak check, task9

**Verdict: REVIEW.** 27 files read, 61 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: missed, serial, counts, result, record, fallout, burn-in, receipts, inputs, independent, supplier, latent, stores, final-test, assembly, proportion, costing, prompt, method, shortcut, candidate, dose-response, carried, baseline, failures

## 1 file names (REVIEW 3)
- **REVIEW** `die_geometry.py`: code shipped in the input pack, confirm it is in-fiction and carries no construction of the answer
- **REVIEW** `excursion_ticket_YE-2026-031.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `pm_spec_history.md`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `wafer_sort_zones.csv`: golden figure 67,100 appears: ...2:28,T-04,PC-A2,PA_R7,1276,1111,4,14,8,13,12,43,4,67,100,144,152,164,172,164,272,108,27,49,38,51,EDGE_RING...

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 27 usable files (10 or more required)
- **INFO** `-`: 6 file categories: code, database, document, image or presentation, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 4 design-note vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader: one isolated general-purpose agent (Sonnet, medium), 2026-11-11, on fresh copies of prompt.txt and target/
only; it read every text, markdown, YAML and Python file and the headers, rows and schemas of the data files, and
computed nothing.

1. How the analysis should be done: the prompt's "counting what the ring costs at sort and at final test" and "on the
   parts it will be fitted with from September"; the spec's "Intervals count wafers polished on the unit since its last
   full PM", "they do not restart the full PM count", the Rev G line "[part]: every [N] wafers since it was last
   replaced, [N] set per unit" and the EW-118 retained-disk entry; the cost inputs' Rev G costing note and "a unit
   scrapped at final test costs its die value and its assembly and test"; die_geometry.py's zone convention.
   Ruling: each pins a WHAT (the count's cost, R4's population, the spec's own intervals, the decision's form, two filed
   conventions, SF9 and SF10); none names a step, a comparison or a grouping, and nothing points at the disk lots or at
   final test's response shape.
2. A file that ranks or scores the candidates: none (the classifier's EDGE_RING label is its own record).
3. A file that exists only to help: die_geometry.py, the yield database's own helper (rev 3), in-fiction.
4. A figure or name that reads as the answer: none as a figure; the Rev G draft pre-states that the part responsible
   comes out of the full PM and leaves the part unnamed. Ruling: the decision's form, which the prompt asks for.
5. Filed sentences that fix a graded figure: the spec's full-PM interval (Rev F's 2,800-wafer cycle in R6, the golden),
   the Rev G line's "since it was last replaced" (the golden's clock for the part, SF5), the waiver's window and limit,
   the costing note (SF9), the plan's volume by unit and mix (SF12), the final-test unit value (SF10), and the prompt's
   windows and populations (SF3, SF4). Ruling: each executes to the golden.
6. One thing that makes it routine: none; the reader names the part's identity as the nearest, settled by data work
   across the FDC, PM log and zone files, and reads the count as arithmetic once the curve is known. Ruling: the curve
   that count rests on is the current lot's (R4), and the count prices final test's own rise (R3); both are analysis,
   and the costing convention is filed. The reader's "catching something that looks planted" names the back-entered
   rows and the retained disks: Layer 1 mess and a filed waiver, neither deciding a result beyond R4's assembly.
REVIEW lines: die_geometry.py harmless (the yield database's helper, zone arithmetic only); excursion ticket harmless
(the team's own ticket, symptom only); pm_spec_history.md harmless in provenance (the Rev G placeholder and the
counting sentences are the spec's own WHAT); wafer_sort_zones.csv harmless (ordinary per-wafer record data).
Realism tells, fixed in the generator: the A140 disks' receipt serial ranges overlapped and ran backwards (now one
running sequence with gaps); the PM log's routine rows were exact multiples of the weeks (now with missed checks and
follow-up checks, 125, 123 and 62 rows). Kept: product aliases from the tester's program names (4 per cent of
records), the slurry certificates (a distractor) and the all-in figures (sums of round inputs).
