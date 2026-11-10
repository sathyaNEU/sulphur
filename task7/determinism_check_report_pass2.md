# determinism-check report, task7, 2026-11-09

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no

## Why

The main recommendation and Critical Component 2 turn on classifying each hotel/care-home building in the controls arm as either "lived in round the clock" (held out of the empty-week banding) or banded normally, per SOLUTION_STEPS step 4's prose rule: "a hotel or care home whose weekend days run above its weekend nights is lived in round the clock." This rule governs about 30% of the controls pilot pool (366 of 1,222 controls-arm responses) and sits directly upstream of the headline **€104.15/tonne controls figure** that decides whether heating controls clear the €120 cap.

The isolated judge thread rebuilt this literally from `electricity_load_profiles_2025.csv` (summed by `customer_number` via `buildings_register_2026.xlsx`, as the method steps describe) and found the rule carries **no stated numeric margin**, and is not recoverable from any of the six shipped PDFs (confirmed by full-text search of all six; only `benchmarking_method_2022.pdf` exists among the method documents and it covers gas benchmarking only — nothing about electricity load shape or occupancy). Depending on which textually-equally-valid reading of "run above" is used, the share of the 366 buildings classified as lived-in-round-the-clock ranges from **2.2%** (strict dominance: every weekend daytime hour exceeds every weekend nighttime hour) to **95.6%** (any positive average margin, the literal zero-margin reading of the stated prose). The underlying day-vs-night gap across these buildings is a smooth continuum with no natural break (5th pctile −1.8pp, median +13.7pp, 95th pctile +42.5pp), so this is a live Gate C operationalization fork, not a cosmetic one.

The design note's own step-by-step (and SF18 in the semantic fork table) names the rival figure that a different, equally defensible handling of this exact classification step produces: **€156.47/tonne**, which is **above the €120 cap** — i.e., a reasonable alternative reading of the stated occupancy rule flips heating controls from funded to rejected, which flips the Final Recommendation's named grant list. The design note's closure/fork table (SF17) asserts this fork is closed ("every hotel and care home inside the band, same call (asserted)"), but that assertion was only checked against the two extremes (every hotel/care home as lived-in, versus none/read-off-load-alone); it was not checked against the realistic middle-ground literal readings of the stated prose rule itself, which is exactly where the judge thread's reconstruction shows the fork actually lives. The stated 90% range for controls (€94.82–€113.57) does not bound the €156.47 rival.

This is Gate B (the deciding margin is not stated in any shipped file) and Gate C (a reasonable alternative reading of the stated rule survives and flips the call) jointly, governing the Final Recommendation and Critical Component 2 / Supplementary asks 4, 6 and 8 (heating-controls rows).

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hotel/care-home lived-in share (zero-margin literal reading of "run above") | n/a (not a golden figure, but feeds R3) | 95.6% (350/366) | Diverges sharply from golden's implicit near-0% |
| Hotel/care-home lived-in share (strict dominance reading) | n/a | 2.2% (8/366) | Close to golden's implicit near-0% |
| Hotel/care-home lived-in share ("3/4 of peak" rule tested as an alternative) | n/a | 0% (max floor/peak ratio observed = 0.742, rule never fires) | N/A — rule as stated never classifies anyone lived-in under this candidate |
| Controls grant/tonne under golden's occupancy reading | €104.15 | not independently re-derived to the cent within the review's time budget (full weather-normalised, decay-fitted pipeline not rebuilt) | Not falsified, but not independently confirmed either |
| Controls grant/tonne under an adjacent misclassification (named in the design note itself) | n/a (design note names it as a rejected variant) | €156.47 (design-note-stated; judge confirmed this exceeds €120) | Crosses the decision threshold |
| Rough (non-weather-normalised) controls dose-response shape by empty-share band | rise starting ~39.0% | directionally consistent rise starting in the high-30s/40s band (−0.4pp @0–30%, +7.9pp @30–39%, +5.7pp @39–50%, −0.5pp @50–60%, +8.5pp @60–70%, +7.0pp @70–80%) | Directionally consistent, not exact-cent verified |
| File/format/hygiene inventory | 19 files, 4 formats | confirmed: xlsx×4, csv×8, pdf×6, docx×1 | Reproduced |

## Competing answers that survived

- **Fork:** the occupancy test "weekend days run above its weekend nights" (SF17 in the design note). **Answer A** (strict/near-literal dominance reading, or the generator's actual implemented margin, whatever it is): controls priced near €104.15/tonne, funded. **Answer B** (zero-margin or small-margin literal reading of the same prose sentence, which 95.6% of the 366 hotel/care-home buildings satisfy): controls price closer to the design note's own named rival, €156.47/tonne, over the €120 cap, rejected. The shipped files state no number that closes this fork; the design note's closure table marks it "asserted" rather than filed. This fork is not closed by any shipped sentence, rule, or threshold, so it survives Gate C.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | ≥10 | 19 (target/), 2 deliverables in golden.zip | Pass |
| File categories | ≥2 | 4 (spreadsheet: xlsx; database/tabular: csv; text: pdf; document: docx) | Pass |
| Large messy files | 1 CSV ≥20,000 rows + 1 CSV 10–20 printed pages | gas_meter_reads_2013_2026.csv (389,105 rows), electricity_load_profiles_2025.csv (178,514 rows), benchmarking_notices_2019_2026.csv (37,213 rows) all clear the row floor; no single CSV was separately verified against the printed-page metric, but breadth and messiness are amply satisfied by the files above | Pass (by breadth) |
| Distractors named outside ZIP, unlabelled inside | ≥2, unused but relevant | metadata.json names 3 (electricity_customers_annual_2019_2025.csv, municipal_heat_plan_2026_summary.pdf, federal_funding_overview_2025.pdf); none labelled inside target.zip | Pass |
| Deliverables | 1–3, all present in golden | 2 requested (note.docx, appraisal.xlsx), golden.zip holds exactly those 2 | Pass |
| Asks multi-dimensional, unit+rounding stated | — | Supplementary asks 2–9 each state unit (%, €, tonnes) and are multi-row/multi-season; rounding is the author's own natural-precision call per the design note's closure axis 10, which is a legitimate convention | Pass |
| Answer shape | one of 14 | an allocation/funding decision with a flip-point and a 90% range per measure (close to "scenarios with the flip point" / "an allocation with its sensitivity"), 4+ checkable results | Pass |
| Golden ZIP exact match to requested files/formats | — | grant_round_2026_note.docx + grant_round_2026_appraisal.xlsx, matches prompt's file request exactly | Pass |
| Nothing LLM-generated, reads as real work product | — | judge thread reported no LLM-authorship tells or provenance leakage across the six opened PDFs and the csv/xlsx files it inspected | Pass (as far as reviewed) |

## Gate G reconciliation

Thread: `mechanism: method_or_model_selection` (primary), with a `single_conceptual_flip`-adjacent risk flagged in the hotel/care-home classification step; `stumping_family: analytical_non_defect`; `surface_read_dependency: no`; `sole_data_defect: no`.

Design note's strategy label: "population selection on unrecorded properties (a randomised effect carried to units that chose their treatment on properties the trial's outcome records do not carry, each measured from a record at another grain), beside a persistence fit and a round projection" (`population_selection`). This is consistent with the thread's `analytical_non_defect` / `method_or_model_selection` call — both describe a legitimate covariate-matched pricing method, not a surface-read-rejection shape. No reconciliation conflict on Gate G: the main stumping mechanism is sound and of the type the client wants. The live defect is narrower and sits inside this otherwise-legitimate method (the occupancy sub-rule's missing margin), which is why the verdict is NOT_DETERMINISTIC on Gate B/C rather than a Gate G banned-type finding.

## Gate H reconciliation

Thread's Gate H line: `domain: pass`, `layers: pass`, `results: ~14 graded across 6+ areas`, `one_thing: data_semantics` (the occupancy rule is an unpinned reading, not a planted shallow factor), `effort: quick ~2 of 14, careful ~7 of 14, thorough ~13 of 14`, `one_fact: "price every application on its own building's covariate ... never its own use's average or the pilot's population mix" rescues ~5 of 14 (~36%)`.

Design note's Effort test table: quick 0.5 of 13, careful-but-hurried 6 of 13, thorough 13 of 13; Largest single hint ("price controls along the share of the week each building stands empty ... and roof insulation along its roof per floor") rescues 2 of 13 (~15%).

Reconciliation: the result counts and the quick/careful/thorough shape are consistent in direction (quick << careful << thorough, each clearing noticeably more). But the thread's one-fact rescue estimate (~36%, "at or just over a third, close to the line") is meaningfully higher than the design note's own Largest-single-hint rescue (15%, 2 of 13) for what is substantially the same sentence (both drivers named). This is one of the findings the client's bar treats as predictive of a send-back ("the thread's best single sentence rescues more results than the note's Largest single hint says"), and it is corroborated independently by the concrete Gate C finding above: the thread's reconstruction shows the "both-drivers" sentence alone does not finish controls (R3, R5c, R6, R8b still need the lived-in step, matching the note's own claim), but the note's claim that the lived-in step itself is a settled, non-forking step is what the thread's Evidence table disproves. H3's `one_thing: data_semantics` call (rather than `shallow_hidden_factor` or `none`) is the correct read: nothing was planted or hidden, but one term in a filed procedure ("weekend days run above its weekend nights") was left as unpinned prose where a number was needed, and a reasonable alternative reading of that same sentence crosses the €120 funding threshold.

No Gate H reconciliation conflict changes the bottom line; the dominant finding remains the Gate B/C defect, which already forces SEND_BACK on its own.

## Stump power (Gate F)

Independent of the Gate B/C defect, the chain has genuine breadth: gas-season reconstruction, the controls dose-response, the insulation roof/floor curve, the heating-optimisation decay fit, 90%-range resampling, the application-volume projection to close, and the 2025/26 saving are each separately checkable, and a ten-minute read could not plausibly reproduce more than one or two of them. The decisive trap for a hurried solver is almost certainly pricing applications on each use's own average saving or the pilot's population mix instead of each application's own building-level covariate — a genuine, non-trivial matching/regression error, not a coin-flip. This part of the design is sound and, once the occupancy-rule margin is pinned, should stump capable models for the right reason.

## Findings, ranked

1. **(Gate B/C, governing)** The hotel/care-home "lived in round the clock" test is stated only as prose ("weekend days run above its weekend nights") with no numeric margin, in no shipped file. Readings range from 2.2% to 95.6% of the 366 affected buildings; a named rival reading prices controls at €156.47/tonne, over the €120 cap, flipping the Final Recommendation and Critical Component 2. The design note's own closure table (SF17) marks this fork "asserted" closed, but the thread's fresh reconstruction shows the assertion does not hold against the realistic middle readings of the stated sentence, only against the two extremes.
2. **(Gate H, secondary, does not independently change the verdict)** The thread's one-fact rescue estimate (~36%) runs higher than the design note's own Largest-single-hint claim (15%) for essentially the same sentence, which is consistent with finding 1: the "both drivers" sentence is doing more work than the note credits, because the lived-in sub-step it depends on is not actually pinned.
3. Everything else the thread checked (the gas-season reconstruction, the roof/floor curve, the dose-response shape, file/format hygiene, the prompt's determinacy on what is asked) reproduced cleanly or was directionally consistent with the golden; no other Gate A–E failure was found.

## Next action for the author

Pin the "lived in round the clock" test to an explicit, numeric rule (the exact margin or ratio the golden actually uses — e.g., a stated day-minus-night percentage-point threshold, or a stated floor-to-peak ratio), confirm that reading against the Evidence table's range of candidate readings, and reverify that every reasonable reading of the now-pinned rule keeps heating controls on the same side of €120; if any reasonable reading still reaches the €156.47-range rival, the occupancy test needs a different, unambiguous construction entirely (not just a restated threshold) before this is re-judged. A rerun of the two platform runs is required after the fix, per the SEND_BACK disposition.
