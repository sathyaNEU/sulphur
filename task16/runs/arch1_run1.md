Reviewed 76 resources· 28m
Recommendation. Name option B for February 2027: width 512, 128,000 expert labels plus 128,000 contractor labels, learning rate 0.0005.
Its expected benchmark log loss is 0.6341, versus 0.6533 for runner-up C, an advantage of 0.0192. Its 29.5 GPU hours fit within the 120-hour slot.
Final answers. All results are saved in `February_2027_training_recommendation.xlsx`.

* Configuration to name: B, with batch size 128, 12 epochs, cosine schedule, 3% warm-up, and the final checkpoint without early stopping. See `Decision` and `Shortlist`.
* Expected benchmark log loss for one run: A 0.6751; B 0.6341; C 0.6533; D 0.6657. A’s previously unspecified learning rate is set to 0.00025. See `Shortlist`, “Expected loss” and “Learning rate.”
* Four-in-five range for B: 0.618 to 0.650. This is a provisional central 80% prediction interval for one run, not a confidence interval for an average across runs. See `Decision` and `Shortlist`.
* Benchmark-equivalent loss for the width-128 pilot with 128,000 expert plus 384,000 map-transfer labels: 0.6848, using the mean of its three completed seeds. If “the trial” means the seed-3 launch listed first in the launch script, its value is 0.6817. These are calibrated estimates, not actual benchmark uploads. See `Pilot and Labels`, pilot summary and run table.
* Replacing one tenth of the entire training set’s expert labels with contractor labels: adds 0.0021 benchmark log-loss units, holding total size and recipe fixed. See `Pilot and Labels`, “Label-source replacement.”
* The equivalent replacement with map-transfer labels: adds 0.0115 benchmark log-loss units. See the same section.
* 512,000 expert labels, width 128, learning rate 0.002: expected benchmark log loss 0.5953. This is an extrapolated counterfactual, not an observed or currently available training configuration. See `Pilot and Labels`, “512,000 expert labels.”

Step-by-step process.

1. Read all supplied inputs. The archive `input-assets/t16.zip` contains the shortlist workbook, meeting notes, trainer defaults, vendor launch script, tracking runs and metrics, scheduler accounting, checkpoint listing, development-item losses and metadata, benchmark submissions, label routes and register, class definitions and counts, and throughput probes. The shortlist and meeting notes establish the decision criterion: lowest expected benchmark loss from one final checkpoint, subject to the slot limit.
2. Reconstructed independent completed trials. From 134 tracking runs, 129 reached their target steps and had final checkpoint artifacts. Five incomplete launches were excluded. One completed run lacked its item-loss dump, leaving 128 usable runs across 53 configurations. Scheduler matching identified 134 training jobs represented by 153 accounting rows; restart segments were not counted as additional trials. The other 86 accounting rows were unrelated to these training runs.
3. Cleaned metrics and label inventories. Harmonizing old and new metric names and retaining the latest event for each run, metric and step removed 2,971 repeated records from 190,531, leaving 187,560. The label register contained 325 rows; removing one superseded contractor record left 320 training shards and four development shards. Actual shard ranges determined training counts, rather than potentially misleading run names. The 120 blank contractor ranges and 105 blank map ranges mean zero labels, not missing quantities. Class-count totals matched every active shard.
4. Separated development losses by label source. The item-loss export contains 8,000 development items for each usable run. These comprise 6,000 expert, 1,000 contractor, and 1,000 map-transfer items. There were no unmatched item indices, invalid class codes, or negative/nonfinite losses. Final all-development item means matched the logged final losses, with a maximum absolute difference of 0.0000014375, consistent with export rounding. No outliers were trimmed.
5. Matched the correct benchmark checkpoints. All 32 submission hashes matched stored artifacts. Two submissions were duplicate attempts without new scores. Two scored submissions used intermediate checkpoints and could not be paired with the final item dumps. This left 28 final-checkpoint calibration pairs, each scored on 20,000 benchmark points. An affine calibration using expert-only development loss had leave-one-out RMSE 0.006108, compared with 0.020493 using mixed-source development loss.
6. Estimated the training response surface. The model controls for training-set size, width, learning rate and label-source fractions, allowing sample-size gains to slow after a fitted breakpoint. This matters empirically: at width 128 and 75% map-transfer labels, the improvement from 128,000 to 256,000 labels was 0.0471 expert-development loss units, but the next doubling improved loss by only 0.0274. The selected model’s configuration-held-out RMSE was 0.009932. Its held-out 512,000-label error was 0.008736, versus 0.036258 for a straight log-size trend.
7. Constructed the one-run interval. The workbook retains 2,000 accepted bootstrap draws, obtained from 2,011 attempts after rejecting 11 rank-deficient fits. Entire configurations were resampled together, calibration pairs were resampled separately, and fresh-run/model error plus benchmark-transfer error were added. Seed variation was not added twice. The resulting central prediction bounds were rounded outward to produce B’s 0.618 to 0.650 proposal range.
8. Verified the finished spreadsheet. Independently recalculated every formula against its stored dependencies and checked its cached result. Reopened the workbook, checked archive integrity, reconciled the audit populations, and confirmed that B remains the lowest-loss shortlist option. Temporary analysis files were removed. Throughput probes, class distributions and cost information were inspected but were not used as substitute predictors of benchmark loss.

Assumptions and judgment calls.

* Calibration must transfer to vendor-trained models. All 28 calibration checkpoints were trained on expert labels only. Expert-only development loss is the closest available proxy for the verified benchmark, but its calibration has not been directly tested on contractor/map-trained submissions.
* Source penalties are model-adjusted replacement effects. Total labels and the training recipe remain fixed. These are not the effects of simply adding labels, nor independently randomized causal estimates.
* The all-expert counterfactual is especially uncertain. Expert-only pilots stop at 128,000 labels. A nearly equally predictive model that attributes the slowdown specifically to map-transfer data gives 0.5535, rather than 0.5953, for the 512,000-expert counterfactual. Both slowdown models still select B.
* A’s learning rate is extrapolated. Its 0.00025 rate follows inverse-width scaling from the checked width-512 rate. No completed width-1024 final trial is available.
* The 80% range is conditional. It assumes the fitted response surface, approximately normal predictive errors and stable benchmark calibration. It does not certify coverage under an unforeseen distribution or implementation change.

Alternatives rejected.

* A and D: Their expected losses, 0.6751 and 0.6657, exceed B’s 0.6341. All options fit the time limit, so spending more of the slot does not justify selecting them.
* C: It is the runner-up at 0.6533 under the selected model. Straight log-size extrapolation favors C, which is evidence against an unconditional claim that B must win. However, that trend predicts the held-out large pilot trials substantially worse because it ignores the observed slowdown.
* Mixed-source development loss as the benchmark proxy: Its calibration error is materially larger than that of expert-only development loss.
* A seed-only uncertainty range: This would omit uncertainty in extrapolation and benchmark calibration. The supplied range includes those components.
* Treating the pilot’s observed mean as the fitted expectation: The workbook distinguishes the calibrated observed mean, 0.6848, from the pooled model expectation, 0.6818, rather than silently substituting one for the other.

Files produced.

* `February_2027_training_recommendation.xlsx`: the recommendation, shortlist forecasts, prediction ranges, pilot and label-source calculations, model formulas, validation results, provenance, run/checkpoint audits, and predictive draws.

Packages installed. NumPy, pandas, SciPy, statsmodels, openpyxl and XlsxWriter, plus their dependencies.
