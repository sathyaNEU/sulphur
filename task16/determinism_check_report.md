# determinism-check report, task16, 2026-11-10 (pass 3)

## Verdict
DETERMINISTIC (the thread's advisory: A's figure and the bands on C and D are judgment-based)
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (with method_or_model_selection and decomposition_attribution), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

**Order kept:** yes. The thread wrote own_derivation.md before opening graded_blocks.md (the task prompt had been moved to task_prompt.md so the answers stayed gated). It ran Python with -I and touched only files inside the run directory.

## Why
The call (B, not C) holds once the pilot is read at the right grain and the size curve is validated out of sample.
- Per-item dev loss on the 6,000 EXP-H items tracks the benchmark: offset 0.0131, SD 0.0059, line 0.0078 + 1.007x.
- The pooled 8,000-item logged loss does not track it, because the vendor-labelled items sit in the pool.
- Once route costs are separated from the size curve, the level at 128k, 256k and 512k expert-equivalent labels is 0.662, 0.611-0.615 and 0.587 (dev). That is a bend: 0.050, then 0.025 per doubling.
- A power law fitted on totals up to 256k undershoots the two 512k-total pilots by 0.016 when they are held back.
- The single-curve reading, which names C, therefore fails validation. B stays ahead of C under every bend-aware reading.

The thread's own cold derivation did fall for the single-curve reading and named C at 0.650, with B 0.657 under the width-specific slope. The thread classes that as a legitimate analytical failure, not a fork.

## Per-gate lines A to H
The thread did not print a separate line for each lettered gate. Its verdict file gives these dispositions, mapped here by content.
- **A (recompute / reproduce):** pass. Every load-bearing figure reproduced from the bundle, except A's point, which is not reproducible (see the ledger).
- **B (literal reading, forks):** pass. The four surviving alternatives are all bounded by the stated bands. The thread records no open fork.
- **C (files and hygiene):** pass. See Files/Hygiene below.
- **D (answer vs files):** pass. No `answer_contradicts_files` was found.
- **E (objective pinned):** pass with an advisory. A's learning rate is unpinned in the prompt and the meeting notes. The golden fixes 0.00027 inside its step text, and the band covers the defensible rates.
- **F (stump power):** high. The hurried reads land on C: the logged pooled dev loss, the size-ladder line, or one curve through all runs. The thread's own cold pass fell for the single-curve read.
- **G (stumping type):** mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. See Gate G classification.
- **H (deep reasoning):** see the Gate H line.

## Gate G classification
`mechanism: forecasting (with method_or_model_selection and decomposition_attribution)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The pooled dev loss is a measurement-grain step, but the task still stumps on clean data. The decisive work is an out-of-sample-validated forecast past the observed totals plus a cost decomposition. The thread judges this not a banned scaffold.

## Gate H line
`domain: pass` (scaling laws, label-route economics, learning-rate scaling for a training-run proposal), `layers: pass` (L1: two logger dialects, restarts, mid-run and duplicate submissions, lost dump, pooled dev items; L2: calibration, composition-cost decomposition, bend forecast, selection), `results: 6 graded across 5 areas` (framing/measurement, assembly, decomposition, forecasting, validation/uncertainty), `one_thing: none`, `effort: quick 1, careful 3, thorough 5 of 6`, `one_fact: "score only the expert-labelled dev items" rescues 2 of 6 (pilot match and per-tenth costs), not the bend, 512k, ranking or range.`

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Finished runs / scored finals | 129 of 134 / 28 of 32 | 129 / 28 (2 duplicates, 2 mid-run checkpoints excluded) | yes |
| Benchmark vs EXP-H dev loss | 0.0078 + 1.007x, resid 0.0059 | 0.0078 + 1.0068x, resid 0.0059 (offset 0.0131) | yes |
| Pilot w128, 128k exp + 384k map | 0.685 (0.680-0.690) | 0.6724 + 0.0131 = 0.6855 (model 0.682) | yes |
| Contractor cost per tenth | 0.0020 (0.0005-0.0032) | 0.0018-0.0028 across structures | yes, inside band |
| Map cost per tenth | 0.0114 (0.0095-0.0125) | 0.0112-0.0120 | yes, inside band |
| Linear in share | 0.0115 at half, 0.0114 at three quarters | consistent, composition-fit RMSE 0.0049 at noise level | yes |
| 512k expert, w128, lr 0.002 | 0.600 (0.595-0.613) | pilot less 7.5 tenths = 0.600; power-law fits 0.592-0.597 | yes (power-law low end 0.592 sits just below the band) |
| Bend | 0.050 then 0.025 | levels 0.662, 0.611-0.615, 0.587; held-back power law misses 0.016 (floor free) to 0.025 (floor 0) | yes |
| B w512 lr5e-4 | 0.625 (0.615-0.650) | 0.633-0.647 bend-aware; 0.638 shared slope; 0.657 width-specific naive power law | point sits 0.008-0.02 low; band holds most readings; 0.657 falls outside |
| C w256 lr1e-3 | 0.670 (0.648-0.689) | bend-aware 0.653 to about 0.69; naive power law 0.644-0.650 | yes under the bend-aware reading |
| D | 0.680 (0.660-0.697) | bend-aware 0.664-0.694; naive 0.656-0.661 | yes under the bend-aware reading |
| A w1024 | 0.661 (0.650-0.720) | no finished 1024 run; thread estimate 0.68-0.695 at 1/width LR | band wide enough to hold it; point not reproducible |
| B range 0.604-0.645 | half-width 0.021 | components 0.0051, 0.014 (thread 0.016), 0.0059 plausible | yes |
| Timings (shortlist sheet) | all fit 120 h | 4.46 s/step at w512, 9.5 s/step at w1024 | yes |

## Competing answers that survived
1. **C as the named option**, if the size curve is one power law through every run. The thread's own cold derivation did this and named C at 0.650. The width-specific-slope variant gives C 0.644-0.650 against B 0.657. It is eliminated by the hold-out check, not by any file stating it. The thread calls it a legitimate analytical failure, not a fork.
2. **The B-versus-C margin is thin at the extremes.** B is 0.647 when w512 carries the dev-loss reading, which makes w512 worse than w256 by 0.014. C's best case is 0.653. B still leads, but the golden's own bands overlap (B up to 0.650, C down to 0.648).
3. **A's number depends on an unpinned learning rate.** The golden fixes 0.00027 in its step text. The band 0.650-0.720 covers the defensible rates, so it does not flip the call, but it is wide enough that it grades little.
4. **Calibration form** (line, offset, or class-reweighted EXP items). It moves any figure by under 0.005, inside every band.

## Files/Hygiene
The thread gave PASS. 16 files, in formats csv (12), xlsx, md, yaml and sh: 10 or more, in 2 or more categories. (The count is the thread's and is right: the main session checked it against target.zip, 16 entries. The first draft of this report miscounted 15 and has been corrected.)
- Large CSVs: tracking_metrics (190,531 data rows) and dev_item_loss (8,000 rows, 7.2 MB, 128 columns).
- Distractors the thread observed in the pack: gpu probe, slurm accounting, sediment classes, class counts. None is labelled.
- Messiness the process produces: two logger vocabularies, restarts with repeated steps, killed and failed runs, a lost item dump, duplicate benchmark uploads, mid-run checkpoints submitted.
- The timeline is coherent. No authoring leakage and no exclusion-level issue was found.

## Spec gates
I checked these against the unzipped bundle and the current prompt.txt and submission.md. I did not open metadata.json, the golden ZIP or the design note, as instructed.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files and categories | 10 or more files, 2 or more categories | 16 files: csv (12), xlsx, md, yaml, sh | yes |
| Large messy files | a CSV of 20,000 rows or more, and a CSV of 10 to 20 printed pages or more | tracking_metrics 190k rows; dev_item_loss 8,000 rows by 128 columns (7.2 MB) | yes (the second file is a wide CSV, so page length is a judgment) |
| metadata.json names 2 or more distractors; none labelled in the ZIP | per the contract | none labelled in the ZIP; the metadata count was not checked | partial (the metadata side was not read) |
| Distractors unused yet weighty | per the contract | gpu probe and slurm accounting are timing-adjacent. The solution uses neither beyond the timing sanity check | plausible; not audited against the design note |
| 1 to 3 deliverables, all in the golden | 1 to 3 | 2 (xlsx and docx) in submission.md, consistent with the prompt's "a spreadsheet and a short note" | yes |
| Asks multi-dimensional, unit and rounding stated | per the contract | the prompt states "three decimals, per-tenth costs to four"; the asks are 5 numeric results plus the note | yes |
| Answer shape identifiable | per the contract | a forecast plus a ranked list, with many gradable cells downstream of the bend | yes |
| Golden ZIP holds exactly the requested files | per the contract | not checked, since golden/ was out of scope | not checked |
| No LLM read | per the contract | the prompt is one plain paragraph under 1,000 characters with no method named. The thread found nothing | yes |

## Advisory notes
- A's ask carries no pinned learning rate. The optional in-house tightening is to say in the prompt or sheet that the solver chooses it. No rerun is needed if only the rubric wording changes.
- B's point 0.625 leans on averaging width steps across compositions (0.640 on the other reading). The C and D bands are extrapolation judgments. All are covered by the stated bands.
- The power-law low end for the 512k figure (0.592) sits just below the 0.595 band edge.

## Fix
none. The thread's Fix line is "none. Advisory only", with the advisory items listed above.

## Next action for the author
Proceed on APPROVE. If the author tightens the wording, state that A's learning rate is the solver's to choose.

## Main session's notes on the gates this report could not reach
The report writer was kept away from `metadata.json`, the golden files and the design note, so three spec gates were left partial. The main session's own checks on the final cut (`generator/checks.py`, `generator/verify.py`, `audit_containers.py`):
- `metadata.json` names two distractors (the September throughput probe and the shard class counts); neither is labelled in a file name or inside the ZIP, and nothing in the golden's path reads them (asserted against the loader's source). The scheduler accounting and the Folk class list, which the thread also took for distractors, are context the golden does not need either.
- The second large CSV of the input gate is `checkpoint_store_listing_2026-11-04.csv` (839 rows, about seventeen printed pages); `dev_item_loss_final_checkpoints.csv` is a third.
- The golden ZIP holds exactly the two requested files (`scale_up_forecast.xlsx`, `proposal_evidence_note.docx`); the independent verifier asserts it.
- The pack and the prompt this pass judged are the final ones: `target.zip` is byte-identical to the fresh unzip the thread read, and nothing graded moved after the verdict.
