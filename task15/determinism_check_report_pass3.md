# determinism-check report (pass 3), task15, 2026-11-11

Passes 1 and 2 untouched. Scratch: /tmp/determinism-check-task15-383420/ (verdict.md, own_derivation.md). The thread derived first (partially: gaps, decomposition components, weekend split, turned-away units; no full bootstrap), then opened graded_blocks.md. One thread. This is a fresh stage 4 on the redesigned cut (2027 licences 34,000 / 20,000 / 12,000; register daily hours; "80% range on it"; SF15 and SF17).

## Verdict
NOT_DETERMINISTIC (open fork on the margin part of the saving, which carries the Super call). SOLUTION_WRONG on Step 7 as extracted, since repaired in `submission.md` (see Findings 2).
**Disposition:** SEND_BACK per the thread (model rerun required). The thread would downgrade to FIX_NOW if the author shows the literal-4.2 route lands inside the Super band once openings and store shocks are handled.
**Stumping type:** mechanism: decomposition_attribution plus method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

## Why
Agreement 4.2 says the saving is waste avoided at cost plus gross margin on units sold in addition less margin on units no longer sold, with gross margin as sales excluding VAT less cost of units sold. The golden reads the margin part off estimated turned-away units at -0.32 / -0.19 per cent of 2025 sales and itself says the recorded-margin route cannot place a format. A literal executor takes recorded margin. The thread's item-level recorded-margin rival (pilot store-item 2026 margin against 2025, carried by AutoOrdre no-opening stores of the same format and item) gives per 26 weeks Super -91k per pilot store (2117 -212k, 2131 -200k, 2104 +13k, 2158 +35k), Kvarter +23k, To Go -25k. Added to a Super waste part of about 69k a year, that puts Super below the 34,000 licence under a literal reading, against 40,200. The note rules this route out by named data (SF15: store 2158's recorded margin 63,000 below its format against 3,700 for its turned-away units; 20,600 a store-year of noise on four Super pilot stores). The thread holds that the shipped text does not license those two conventions.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot / other sales growth, gap | 3.9 / 5.9, -2.0 | +3.87 / +5.88, -2.01 | yes |
| Waste at cost growth, gap | -9.6 / +7.9, -17.5 | -9.61 / +7.91, -17.52 (matches dashboard; 2025 other-waste differs about 95 DKK) | yes |
| 840 duplicate rows; milk renumbering | yes | yes | yes |
| Format growth, AutoOrdre no-opening | 4.8 / 4.8 / 10.8 | 4.81 / 4.81 / 10.82 | yes |
| Mix part, sales / waste | -0.6 / -1.2 | -0.64 / -1.24 | yes |
| Weekend-share split | 0.23 | gap between 0.201 (3170) and 0.252 (4352); commuter pilot stores 3157, 3165, 3189 | yes |
| Waste avoided, weekend-trading / commuter pilot | 19.7 / -1.3 | 19.2 / -1.2 | inside band |
| Turned away, every sale, 2026 / 2025 | 125,000 / 109,200 | 124,728 / 105,196 | 2026 yes; 2025 differs 3.7 per cent (no band stated for this form) |
| Turned away, one sale fewer | 94,100 / 81,300 (90,300-104,700 / 78,000-91,100) | 99,632 / 82,945 | inside, but moves about 5,500 with interpolation choices |
| Waste part before margin, Super / Kvarter / To Go, a year | n/a | about 69k / 40k / 6k; with golden margin rates about 41k / 33k / 4k against 40.2k / 28.0k / 2.4k | within bands |
| Super saving vs literal recorded-margin route | 40,200 (35,800 to 47,000) | below 34,000 | not reproduced (fork) |
| Openings, 80% ranges, full bootstrap | as stated | not rebuilt | not independently confirmed |

## Competing answers that survived
1. Super margin route: recorded margin read literally (item-level, thread's own construction) puts Super below its 34,000 licence. The note's own run of a recorded route gave Super -10,800 and a pooled one 30,500; both are ruled out by the note's named data, not by a shipped sentence. The thread rates this Gate C, underspecified_objective / competing_defensible_answer.
2. "Recommended setting": forecast and the 0.75 safety factor changed together (agreement 2.3). The thread notes they cannot be separated; the cause list for the two gaps is not named in the prompt. The golden's four-line split is not forced by the prompt, and "taking all that is left" gives -1.0 against -0.7, held only by the band.
3. Thin Super margin: golden 40,200 against licence 34,000 (6,200); the lower band end 35,800 is 1,800 above the licence; the 80 per cent range 22,200 to 55,800 straddles it; four Super pilot stores carry it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 (CSV, XLSX, PDF) | yes |
| Categories | 2 or more | spreadsheet, text | yes, thin |
| Large messy CSVs | 20,000 rows or more; one 10 to 20 pages | 389,960 / 309,760 / 309,760; bi_uge 19,656 | yes |
| Distractors | 2 or more, unlabelled | vejr_dmi_2025_2026.csv, personaletimer_frisk_2026.csv (metadata); kampagneplan also unused | yes |
| Deliverables | 1 to 3, all in golden | xlsx and pptx; golden.zip holds exactly these | yes |
| Asks, units, no rounding dictated | yes | yes; prompt now says "with an 80% range on it" | yes |
| Shape, 4 or more checkable results | yes | 8 graded results by the thread, 10 in the note | yes |
| Realism / authoring leakage | none | none found; dates coherent | yes |

## Gate G reconciliation
Thread: analytical_non_defect, surface_read_dependency no, sole_data_defect no; the weekend-share driver sits across all 42 stores and shows through the shadow forecasts, so it is analysis. This agrees with the note's Hidden factor record. The determinism failure is the margin convention, not a hidden factor.

## Stump power (Gate F)
Gate H line: domain pass; layers pass; results 8 graded across 5 areas; one_thing none; effort quick 2, careful 5, thorough 8 of 8; one_fact "the forecast only saves in stores that trade through the weekend" rescues about 3 of 8 (asks 3 to 5 and Critical Component 3), borderline under a third.
Note: effort 1, 4 and 10 of 10; the trading-week sentence rescues R7 and half of R9 (about 1.5 of 10), and the careful pass finding the trading week keeps Super off at 28,800 against 34,000. The thread's careful grade (5 of 8) is above the note's 4 of 10 by count basis. The redesigned call needs both the estimator and the trading week, so no single sentence carries it: Gate H passes on the one-thing screen. A careful but hurried run likely loses the margin part (125,000 turned away, dashboard 17.5 per cent as saving: Super 60,200, Kvarter 45,500, To Go 23,400), the trading-week split and the ranges, and may mis-switch Super (33,100) or read recorded margin and file a negative figure.

## Findings, ranked
1. Margin convention (Gate C): the literal 4.2 route with recorded gross margin puts Super below 34,000, outside the 35,800 to 47,000 band. SF15 closes it with named data in the note but the shipped text (agreement, prompt) does not name the margin source. Super's cushion is thin (6,200 to the licence, 1,800 to the band end).
2. Step 7 stated the hurried reading as "switching Super and To Go" while Super 33,100 sits under the 34,000 licence. I re-diffed the current `submission.md` against the extracted blocks: Step 7 now reads "switching To Go", the only line that changed (07:58, after the 07:50 extract). The pack is unchanged (target.zip 07:48). The SOLUTION_WRONG is repaired in the file; the thread judged the earlier wording.
3. The two gaps' cause list is not named in the prompt (forecast with the safety factor as one cause, mix, openings, residual); the split is the author's.
4. The S-1 turned-away figure moves about 5,500 with interpolation choices; the band carries real method freedom. The 2025 every-sale figure (109,200 claimed, 105,196 recomputed) differs 3.7 per cent and has no band.
5. Final savings, ranges and openings were not independently rebuilt by the thread.

## Next action for the author
Close the margin source in what a solver sees, in observable terms without naming the method, or make the golden follow 4.2 literally with an opening-and-shock-adjusted expectation and show every rival (including the thread's item-level recorded-margin route) lands inside the Super band. Widen the Super gap to its licence or add Super pilot stores so the call is not within about 6,000 of 34,000 on four stores. Name the cause list for the two gaps in the ask. Step 7 is already corrected. Then rebuild and re-judge as the pipeline allows.
