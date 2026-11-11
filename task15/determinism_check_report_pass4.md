# determinism-check report (pass 4), task15, 2026-11-11

Passes 1 to 3 untouched. Scratch: /tmp/determinism-check-task15-408067/ (verdict.md, own_derivation.md). The thread derived first from the bundle alone, then opened graded_blocks.md. One thread. Cut: agreement 4.2 now files the margin part as the change in out-of-stock sales, valued at gross margin; Step-by-Step rewritten; no graded band moved. I re-diffed the current submission.md (14:46) against the extracted blocks and found no content change.

## Verdict
NOT_DETERMINISTIC (Super decision margin; the gap and trading-week blocks reproduce). No SOLUTION_WRONG.
**Disposition:** SEND_BACK. Pin or widen the Super margin and the "same expectation" convention in the shipped text or data, and spread the savings difficulty over more independent results (Gate H5). New runs are required.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (the thread adds that without the constructed commuter-week forecast bias the format-only reading would be right and the task would collapse).

## Why
The Super call (40,200 against the 34,000 licence, lead 6,200, band 35,800 to 47,000) turns on an unpinned convention. Pilot stores 2131, 3031 and 3012 are cut by discounter openings. The golden's Step 7 adjusts their expected waste for the trade the opening took and books the margin part "against the same expectation", but nothing shipped says whether the expected turned-away units carry the opening. With the rest of the method fixed (S-1 estimator, trading-week pooling, 52-week year):
- the golden's replica (no adjustment) gives Super 41.4k pooled and 39.2k format by format, matching the golden (40.2k and 39.7k);
- the consistent reading (the opening trims expected turned-away units as it trims expected waste) gives Super 33.9k pooled and 28.7k format by format, at or below the licence, with Kvarter 25.6k and To Go 2.1k unchanged in decision;
- excluding the three opening-hit pilot stores gives Super 48.5k to 54.1k, outside the band.
This is Gate C (margin_or_boundary_fragility) on the Super switch, hence on the recommendation and asks 3 and 5. The thread's estimators approximate the golden's, so the swing size is indicative; the direction and the straddle of the licence are robust to its choices.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Sales gap | 3.9 / 5.9, -2.0 | +3.87 / +5.88, -2.0 | yes (matches dashboard) |
| Waste gap | -9.6 / +7.9, -17.5 | -9.61 / +7.91, -17.5 | yes |
| 840 duplicate rows; 451348/451355 renumbering | yes | yes | yes |
| Control growth, no-opening AutoOrdre stores; mix | 4.8 / 4.8 / 10.8; about -0.6 | same | yes |
| Turned away, S-1 form | 94,100 / 81,300 | 94.8k / 81.5k | yes |
| Turned away, every sale | 125,000 / 109,200 | 125.0k / 109.3k | yes |
| Trading week split | 0.23; 16 commuter, 26 weekend-trading; 3 commuter pilot | 0.201 to 0.252; 16 / 26; 3 / 13 | yes |
| Shadow forecast weekend ratio | 2.42 / 0.91 | 2.42 / 0.91 (ranges 1.48 to 3.08 and 0.83 to 1.08) | yes |
| Pilot waste saving, weekend / commuter | 19.7 / -1.3 | 19.0 to 20.4 / -1.3 | yes |
| Margin parts, weekend / commuter (per cent of 2025 sales) | -0.32 / -0.19 | -0.33 / -0.16 | yes |
| Saving per store-year, pooled / format by format | 40.2k, 28.0k, 2.4k / 39.7k, 26.2k, 3.5k | 41.4k, 29.2k, 2.8k / 39.2k, 27.8k, 4.2k | yes |
| Super with opening adjustment on expected turned-away units | inside band | 33.9k pooled / 28.7k format by format | fork |
| Super excluding opening-hit pilot stores | inside band | 48.5k to 54.1k (Kvarter 30.5k to 35.2k, To Go 3.8k to 4.2k) | outside the Super and Kvarter bands |
| 80% ranges, openings read | as stated | not rebuilt end to end | not independently confirmed |

## Competing answers that survived
1. Opening-adjusted expected turned-away units: Super 33.9k pooled, 28.7k format by format, at or below 34,000. Decisions on Kvarter and To Go hold.
2. Opening-hit pilot stores excluded: Super 48.5k to 54.1k, Kvarter 30.5k to 35.2k, outside both bands, same decisions.
3. Gap cause list is not named in the prompt (mix, openings, forecast, residual); the golden's split is the author's. Decisions are stable under all open readings except the Super fork.
4. Format-only DiD with every sale counted switches To Go (23k); the data refutes it through the pilot's To Go stores all trading a weekend week, so the solver must find the split.
5. Weather and the campaign plan move nothing between the groups.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 (CSV, XLSX, PDF) | yes |
| Categories | 2 or more | spreadsheet, text | yes, thin |
| Large messy CSVs | one of 20,000 rows or more; one 10 to 20 pages | 389,960 / 309,760 rows; bi_uge 19,656 | yes |
| Distractors | 2 or more, unlabelled | vejr_dmi_2025_2026.csv and personaletimer_frisk_2026.csv (metadata); campaign plan also unused | yes |
| Deliverables | 1 to 3, all in golden | xlsx and pptx | yes |
| Asks, units, no rounding | yes | yes | yes |
| Shape, 4 or more checkable results | yes | 11 graded results by the thread | yes |
| Realism | none LLM-looking | no authoring banner; dates coherent; minor oddity: store 2146 (Silkeborg) listed 2.6 km from a Galten Lidl | yes |
I did not re-check the golden files myself beyond the thread's reading and the structure checked in earlier passes.

## Gate G reconciliation
Thread: analytical_non_defect, surface_read_dependency no, sole_data_defect no. The commuter-week bias is constructed, but it sits in the shadow forecasts of all 42 stores, which keeps it short of a decider-only plant. Consistent with the note's Hidden factor record. The pass fails on the Super margin convention, not on a defect.

## Stump power (Gate F)
Gate H line: domain pass; layers pass; results 11 graded across 6 areas; one_thing shallow_hidden_factor (the commuter-week bias: one cross-tab of pilot saving against weekend share shows it, one stratification fixes it); effort quick 2, careful 5, thorough 11 of 11; one_fact "the forecast only pays in stores that trade through the weekend" rescues the recommendation, asks 3 to 5 and Critical Component 3, 5 of 11, above a third.
Reconcile with the note (read after the thread returned): the note's effort test gives 1, 4 and 10 of 10, and says the trading-week sentence rescues R7 and half of R9 and, with the careful pass, would still miss R2, R3, R8 and the call because Super stays off at 28,800 against 34,000 under every-sale counting. The thread credits the single sentence with the recommendation and asks 3 to 5 anyway, because the format-table figures follow from the trading week. The two counts do not agree and the thread's reading of the one-sentence rescue is above a third on its own 11-result basis; the main thread should weigh this against the note. A careful but hurried run likeliest files Super 33,100 or 28,800, Kvarter 16,800 and To Go 23,800, switching To Go.

## Findings, ranked
1. Super decision margin (Gate C, margin_or_boundary_fragility): whether the expected turned-away units in opening-hit pilot stores carry the opening is unpinned by shipped text; the consistent reading puts Super at 33.9k pooled and 28.7k format by format, at or below the 34,000 licence; the opening-excluded rival gives 48.5k to 54.1k, outside the Super band.
2. Gate H: one_thing shallow_hidden_factor, one-fact rescues 5 of 11 (above a third); the savings cluster carries the recommendation, asks 3 to 5 and Critical Component 3.
3. Super lead is thin (6,200 to the licence, 1,800 to the band's lower end), and four Super pilot stores carry it.
4. The cause list for the two gaps is not named in the prompt.
5. The 80% ranges and the openings were not independently rebuilt by the thread.
6. Thin file variety (CSV, XLSX, PDF).

## Next action for the author
State in the agreement or the answer text which expectation the turned-away units use in opening-hit pilot stores, and assert that every defensible variant (including the opening-adjusted and opening-excluded readings) leaves Super on one side of 34,000 by a margin, widening the Super gap if it does not; put the opening-excluded figures inside the bands or rule them out by named data; spread the savings difficulty over more independent results so the trading-week finding is not the one sentence that rescues five of eleven. Run the platform runs afterwards.
