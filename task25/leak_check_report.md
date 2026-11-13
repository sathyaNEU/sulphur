# leak check, task25

**Verdict: REVIEW.** 31 files read, 152 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: packing, record, window, per-rank, missed, sequences, excess, reflex, attention, length, expected, throttle, interruptions, documents, long-context, formula, best-fit, planned, method, sequence, provider, measured, sample, shortcut, independent

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `profiling/rank_step_samples_2026.csv`: golden figure 18,900 appears: ...kide-8b-v3,936000,2026-09-10T10:27:13Z,81,ka-r06-18,900.0,46.4,23.8 kide-8b-v3,936000,2026-09-10T10:27:13...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `policy/compute_allocation_rules_CAR-2027-1.pdf`: 7 of 25 stump-paragraph terms appear (window, sequences, length, expected, planned, sequence); read whether the document names the move
- **REVIEW** `provider/service_schedule_S3_kaivola.pdf`: 3 of 25 stump-paragraph terms appear (record, planned, provider); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `runs/interruptions_2026.csv`: Python-style nulls or booleans (nan/None/True/False) in the first rows

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'xlsx' at 21% of 24 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 31 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)


## Solver's-eye read

### 1. Sentence or file that tells you how to do a step
`policy/compute_allocation_rules_CAR-2027-1.pdf` is the one filed rulebook and pins several steps directly:
- Window: "A reservation holds a block of whole nodes in one hall. Its window runs from 00:00 UTC on the window's start date to 00:00 UTC on its end date, as listed in the H1 2027 roadmap. A block's run launches when its window opens."
- Finish definition: "A run finishes when the trainer's token count reaches the run's token budget. The trainer counts training tokens; padding positions in a packed sequence are not tokens and are not counted."
- The comparison and the 80 per cent: "A run is planned to finish inside its window when its expected finish falls at or before 00:00 UTC on the window's end date. The committee asks for each run's expected days from its window's start to its finish, and the range within which it will finish four times in five." This is the literal source of the prompt's "inside the window" test and "80 per cent range."
- Provider works: "Works the provider has notified stop every job in the hall they affect for as long as they last; jobs resume from their last checkpoint when the hall is handed back."
- The 2026 bridge formulas (quoted under Q5).

Minor: `benchmark/tpbench_harness.yaml` states "hall_load: other jobs drained from the slice's rows during timing," telling the solver what the benchmark excludes, not what to compute.

### 2. File that already ranks or scores the candidates
None. `plan_2027/roadmap_h1_2027.xlsx` ("H1 2027 runs") lists the 11 candidate runs (window_start, window_end, token_budget, config) with no risk flag, note or finish-date column; neither workbook has a hidden sheet, comment or formula. No CSV/YAML/JSONL contains "risk," "late," "miss," "delay," "flag," or a totals row. Nothing pre-scores any run.

### 3. File that exists only to help the analyst
`benchmark/tpbench_harness.yaml`: a short methods note on how `tpbench_results.csv` was produced (synthetic corpus, warmup/timed steps, the drained-hall condition); it describes that file, measuring nothing itself. `provider/service_schedule_S3_kaivola.pdf` does the same for the provider files: contracted node counts per hall, metering cadence ("reported as a five-minute average in kW"), notice periods for works, field notes rather than data.

### 4. Figure or name that reads as the answer
None found: no pre-flagged run, no totals row, nothing hidden in either workbook, nothing unusual in the PDFs. The only name that draws the eye is `kide-120b-v1`, the single 120B "flagship" run (largest token_budget, 17.2 trillion, window 1 Feb to 17 Apr 2027), a property of the data, not a stated verdict.

### 5. Filed sentence that literally fixes a graded figure or population
`policy/compute_allocation_rules_CAR-2027-1.pdf`, section 6: "For the review of 2026 the committee counts a run's GPU-days held as its allocated nodes, times eight GPUs a node, times the hours from its launch to its final checkpoint, divided by 24. A run still training at the end of the review period (00:00 UTC on 1 November 2026) counts to then. Every run launched in 2026 is in the review." Literal result: for every run in `runs/run_registry_2026.csv` (all 53, including the one still "running"), GPU-days held = nodes x 8 x (hours launch-to-final-checkpoint, capped at 2026-11-01) / 24, nothing subtracted for interruptions or idle time.

Same section: "The GPU-days a run's benchmark implies are its training tokens divided by the benchmark's tokens per GPU-second for its configuration (model, sequence length, sequences per rank and hall), divided by 86,400." Literal result: join each run to its one matching row in `benchmark/tpbench_results.csv` on those four keys, divide tokens by that rate and by 86,400. I verified all 53 2026 runs and all 11 2027 runs match exactly one benchmark row on (model, context_tokens, seqs_per_rank, hall), so the join never needs interpolation.

Section 3's padding sentence (quoted under Q1) also literally excludes `pad` entries in `profiling/packing_manifests_2026.jsonl`, and any padding implicit in a "sequential" cut, from any token count measured against a budget.

### 6. One thing that would make most of it routine?
No. At least four separately filed, independent mechanisms sit between benchmark days and real days: (a) the benchmark's idle-hall condition versus real contention (`tpbench_harness.yaml` vs. `cluster/node_states_2026.csv`); (b) unplanned hardware, software and facility interruptions with checkpoint rewind (`runs/interruptions_2026.csv`, 297 rows, 4 kinds); (c) scheduled provider works stopping a whole hall for a fixed span, some forward-dated into H1 2027 itself (`provider/planned_works_h1_2027.pdf`, `provider/work_orders_2025_2026.csv`); (d) data-mix and packing differences (`kide-34b-sci` alone uses "best_fit" packing; mixes range from 92 per cent papers to 63 per cent web; `data/doc_length_sample.csv` gives per-source length distributions unlike the benchmark's synthetic corpus).

The rulebook settles outright only: both endpoints of the 2026 fleet-wide bridge (formula plus a clean 1:1 lookup), and the wording of the "inside window" test and "80 per cent" ask (naming the question, not answering it). Everything else (the per-run 2027 forecast, each run's cause-by-cause split, the range's actual width, the finish date, the recommendation) requires combining the remaining files and is not resolved by any single sentence. So: the window-test comparison and the token-counting convention are read-the-definition items; the 2026 bridge's endpoints are follow-the-formula-and-look-up items; the rest turns on analysis.

### Realism tells
- The three PDFs are LibreOffice Writer exports with distinct authors/dates (`Esa Airaksinen`, 2 Nov 2026; `Tauno Kainulainen`, 28 Oct 2026 and 18 Dec 2025); no FPDF/ReportLab signature.
- `data/doc_length_sample.csv` has exactly 20,000 rows for each of its 8 sources (160,000 total): an unusually even split, though the filename ("sample") makes a deliberate fixed-size draw plausible.
- `provider/hall_it_load_2026.csv` genuinely carries about 83-84 gaps per hall, matching the service schedule's "collector outages leave gaps in the meter export; the provider does not backfill them": documented mess, not sloppy mess.
- Every 2026 and 2027 run matches exactly one `tpbench_results.csv` config: convenient (no gaps to interpolate across), but plausible for a team that benchmarks every config it runs.

### Rulings (main thread, 2026-11-13)

- Question 1 and 5 (the allocation rules): harmless. The quoted sentences are the WHAT the determinism contract
  requires filed (the window, the real-token budget, the test, the extension, the 2026 accounting); they name no
  step of the analysis, and executed literally they give the golden's endpoints (the GPU-days held and the
  benchmark's GPU-days).
- Question 3 (the harness config and the service schedule): harmless. The harness config is the benchmark's own
  configuration file and the service schedule the provider's contract schedule, each in its genre; neither names a
  mechanism.
- Question 6: no single fact settles the task; the reader named four separately filed mechanisms and none of the
  three judgments the call turns on.
- Realism: the 20,000 documents per source are the data team's stratified sample (a fixed n per source), kept; every
  run matching a benchmark row is the harness's job (it times every planned configuration), kept.
- Sweep REVIEW lines: 2027 dates in the plan files are plans; 18,900 inside a node name followed by a millisecond
  value is a coincidence; the PDFs' generic words name no move; the work orders now carry the export's own headers.
