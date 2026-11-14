# leak check, task25

**Verdict: REVIEW.** 31 files read, 150 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reflex, missed, packing, record, penalty, window, expected, excess, method, shortcut, modelling, rebuilt, throttle, research, reservations, blocks, unprompted, hurried, constructed, replayed, best-fit, interruptions, slowest, rescues, per-rank

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `profiling/packing_manifests_2026.jsonl`: golden figure 236,323 appears: ...50,3431,3385,173,3588,4021,657,2373,1525,345,1548,236,323,551],[1490,670,752,729,593,908,66,161,1931,2710,8...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `policy/compute_allocation_rules_CAR-2027-1.pdf`: 4 of 25 stump-paragraph terms appear (window, expected, research, blocks); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `runs/interruptions_2026.csv`: Python-style nulls or booleans (nan/None/True/False) in the first rows

## 9 dates after the setting (REVIEW 12)
- **REVIEW** `plan_2027/configs/kide-120b-v1.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-02-01, 2027-04-17
- **REVIEW** `plan_2027/configs/kide-13b-code-lc32.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-01-18, 2027-01-25
- **REVIEW** `plan_2027/configs/kide-13b-lc32.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-05-03, 2027-05-15
- **REVIEW** `plan_2027/configs/kide-13b-v4.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-03-29, 2027-05-08
- **REVIEW** `plan_2027/configs/kide-34b-16k.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-03-15, 2027-05-08
- **REVIEW** `plan_2027/configs/kide-34b-lc64.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-03-01, 2027-03-14
- **REVIEW** `plan_2027/configs/kide-34b-sci.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-04-12, 2027-05-02
- **REVIEW** `plan_2027/configs/kide-34b-v3.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-02-01, 2027-03-11
- **REVIEW** `plan_2027/configs/kide-70b-v2.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-01-11, 2027-02-27
- **REVIEW** `plan_2027/configs/kide-8b-lc64.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-05-24, 2027-06-06
- **REVIEW** `plan_2027/configs/kide-8b-v4.yaml`: 2 ISO dates after 2026-11-06, e.g. 2027-02-01, 2027-04-17
- **REVIEW** `plan_2027/roadmap_h1_2027.xlsx`: 22 ISO dates after 2026-11-06, e.g. 2027-01-11, 2027-01-18, 2027-01-25, 2027-02-01, 2027-02-27

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

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and the unzipped `target.zip`, 2026-11-14, no design
note, generator or answer blocks, the six questions plus two more; verdict **CLEAN**.

1. Methods stated: only the conventions of `policy/compute_allocation_rules_CAR-2027-1.pdf` (section 2 the window clock
   and the block's extension and hand-back, section 3 padding is not counted, section 4 the committee's test and the
   expected days, section 5 works stop every job in the hall, section 6 the GPU-days held and the benchmark GPU-days).
   The reader read them as definitions and conventions, not analytical moves; the harness config's conditions
   (`checkpointing: off`, `hall_load: other jobs drained`) as a description of the benchmark naming no step.
2. No file ranks or scores the candidates; the roadmap lists windows and budgets only.
3. No file exists only to help the analyst; the profiling files read as the organisation's own data, the energy
   invoices and checkpoint evaluations as plausible and unused.
4. No figure or name reads as the answer; the roadmap's Changes sheet is context.
5. The filed sentences, read literally, are the window clock, the finish definition (real tokens, padding excluded), the
   committee's test, the works' stop and the section 6 formulas; the reader found no sentence that states the
   decomposition the prompt asks for. They execute to the golden's endpoints (the GPU-days held and the benchmark days).
6. No single dominant item: the rules settle a clock and two definitions (reading a convention), the causes sit across
   interruptions, manifests, rank samples, the hall's meter, node states and document lengths and need analysis; nothing
   looks planted beyond ordinary mess (mixed spellings of one fault code, local-time dates in the provider's logs).
7. Machine-made tells: only `kind: synthetic` and `seed: 1729` in the benchmark harness config (rated mild); the corpus
   kind is reworded to `random_tokens` in the generator. Containers are the word processor's and the spreadsheet
   application's, with shared strings and real-looking authors; no hidden sheets, comments or defined names.
8. The sweep's flagged files, each read: the provider's service schedule holds facts and a timezone convention only;
   the manifests' coinciding number is a document length; the allocation rules file rules and name no move; the
   interruptions file has 104 blank node fields on software and hall events and no null or boolean tokens; the plan
   files are the organisation's forward plan.

### Rulings on the sweep's REVIEW lines

- Sweep 3, `packing_manifests_2026.jsonl` (a figure of the answer blocks inside a list of document lengths): a
  coincidence, harmless. `provider/service_schedule_S3_kaivola.pdf` (hall B's and hall A's node counts, 1,024 and 512,
  also named in the answer blocks as the reservation levels' base): the schedule's own stated parameters, listed under
  `stated_inputs` in `metadata.json`, which cleared the sweep's LEAK.
- Sweep 4, the allocation rules (window, expected, research, blocks): ordinary rule vocabulary; the reader found no
  move named. Harmless.
- Sweep 8, `interruptions_2026.csv`: blank node fields on software and hall events, no tokens. Harmless.
- Sweep 9, the plan files: the 2027 plan's own dates, forward-looking by design. Harmless.
- Sweep 11, the prompt shell quota (a spreadsheet in 21 per cent of 24 prompts): the author rewrites the prompt for voice.
