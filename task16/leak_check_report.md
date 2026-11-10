# leak check, task16

**Verdict: REVIEW.** 16 files read, 42 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: careful, yardstick, forecast, examples, trials, largest, ladder, results, scored, nothing, routes, result, carried, golden, scores, logged, prompt, missed, scaling, ranked, return, development, priced, forecasting, vendor

## 1 file names (REVIEW 2)
- **REVIEW** `launch_vendor_trials.sh`: code shipped in the input pack, confirm it is in-fiction and carries no construction of the answer
- **REVIEW** `mml_group_meeting_2026-11-05.md`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0140 appears: ...,0.0821,0.0549,0.0922,0.0655,0.0287,0.0454,0.0318,0.0140,0.0298,0.0183,0.0112,0.0297,0.0167,0.0617,0.0165,...
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0032 appears: ...3613,0.4278,0.2390 62,0.0116,0.0074,0.0049,0.0033,0.0032,0.0025,0.0055,0.0028,0.0155,0.0150,0.0030,0.0229,...
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0059 appears: ...,0.0129,0.0043,0.0048,0.0107,0.0026,0.0011,0.0046,0.0059,0.0072,0.0836,0.2424,0.0943,0.0998,0.1187,0.0075,...
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0051 appears: ...,0.0103,0.1678,0.0876,0.0645,0.0409,0.0192,0.0219,0.0051,0.0118,0.1181,0.0666,0.0854,0.0644,0.0233,0.0228,...
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0125 appears: ...,0.0862,0.0139,0.1197,0.0511,0.0180,0.0259,0.0153,0.0125,0.0090,0.0284,0.1160,0.0821,0.0549,0.0922,0.0655,...
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0095 appears: ...,0.0177,0.0128,0.0029,0.0026,0.0011,0.0438,0.0058,0.0095,0.0075,0.0014,0.0063,0.0013,0.0121,0.0036,0.1520,...
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0020 appears: ...,0.0084,0.1190,0.0357,0.0307,0.0163,0.0048,0.0040,0.0020,0.0045,0.1005,0.0344,0.0242,0.0101,0.0026,0.0031,...
- **REVIEW** `dev_item_loss_final_checkpoints.csv`: golden figure 0.0114 appears: ...,0.0344,0.0982,0.0610,0.0750,0.0535,0.0111,0.1132,0.0114,0.0376,0.0992,0.0846,0.0860,0.0179,0.1033,0.0176,...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `mml_group_meeting_2026-11-05.md`: 5 of 25 stump-paragraph terms appear (scored, nothing, result, scores, ranked); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `tracking_runs_export_2026-11-04.csv`: columns a generator names and an organisation does not: seed

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'whether' at 31% of 16 prompts (cap 30%); deliverable set 'xlsx' at 25% of 16 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 16 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

One isolated reader (general-purpose, sonnet, medium effort), 2026-11-10, on a fresh copy of `prompt.txt` (the six-ask prompt) and the unzipped `target.zip`; it read the prompt, the notes, the defaults file and the launch script in full, both sheets of the shortlist workbook, and the header, a sample and the low-cardinality values of every CSV. It solved nothing and computed nothing. This read replaces the first one, which was made on the nine-ask prompt before the determinism repair and returned the same six answers.

1. A sentence or file that says how the analysis should be done: none. The closest is the notes' "We keep our standard recipe for the slot: batch 128, twelve epochs, cosine schedule with 3 per cent warm-up, the final checkpoint, no early stopping", which is the recipe of the run to be forecast and no analysis step; "Teams are ranked on the expected value, and a team whose result lands outside its own range drops a place" frames the range and gives no method.
2. A file that ranks or scores the candidates: none. The benchmark file holds the pilot's scores per upload; the shortlist workbook holds hours and steps and no losses.
3. A file that exists only to help the analyst: none. `label_routes.csv` and `sediment_classes_folk.csv` are small lookups of the ordinary kind.
4. A figure or name that reads as the answer: none. Values such as 0.6665 to 0.6739 in the benchmark file are the pilot's scores for other configurations.
5. Filed sentences that fix a graded figure or population, read literally: "It is trained once, with the recipe the proposal states, and the programme scores the final checkpoint on the verified benchmark: mean log loss over the 20,000 grab-sample points" (one run, the final checkpoint, the benchmark's loss); "expected benchmark log loss of that final checkpoint and a range we expect the result to fall in four times out of five" (a four-in-five range for the single run); "Lyngvær's lot 1 (128,000 points) ... is all the contractor labelling in this year's budget. Lots 2 to 4 are not funded" (the contractor labels stop at 128,000); "B, C and D use the rates we took for 512 and 256 after the week 42 check" and "option A still needs a learning rate" (A's rate is open, the others are in the sheet); the shortlist table (each option's width, labels and rate). Main-thread ruling: each executes to the golden's estimand and to no easier figure.
6. One thing that would make most of the asks routine: none. "No single file or sentence settles most of it"; the pack points at "real modelling over many runs, with several separate pieces". By ask: the four expected losses and the range, analysis; the configuration to name, analysis; the loss matching the width-128 trial, analysis with a little reading of run names and shard ranges; the per-tenth costs, analysis with a small definition read; the loss at 512,000 expert labels, analysis, an extrapolation. "Nothing relies on a stated rule or procedure ... I do not see anything built only to be caught."

Review lines: `launch_vendor_trials.sh` harmless (a plausible launcher for the week 44 trials that states no result); `mml_group_meeting_2026-11-05.md` harmless (the group's own record of the slot's rules and the shortlist; it describes no file); `dev_item_loss_final_checkpoints.csv` harmless (raw per-item losses, nothing that reads as an answer); the `seed` column harmless (the field's own word, matched by s1 to s3 in the run names).

Realism: minor notes only. Two headers of the shortlist sheet read slightly written for the occasion ("Hidden width", "Sec per step (our g1 nodes)"): renamed in the generator to "Width" and "s/step (g1)", data only. The notes' action for Magne mirrors the request: it is the meeting's own action and the origin of the request, left as it is. Tidy run names: what a launch script writes. Nothing else.
