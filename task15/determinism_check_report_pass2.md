# determinism-check report (pass 2), task15, 2026-11-11

Pass 1 report left untouched (determinism_check_report.md). Scratch: /tmp/determinism-check-task15-382041/ (verdict.md, own_derivation.md; the thread derived first, then opened graded_blocks.md). One thread, no retries.

## Verdict
DETERMINISTIC, conditional on residual forks listed below. No SOLUTION_WRONG.
**Disposition:** SEND_BACK, on Gate H (one_thing: shallow_hidden_factor; one_fact rescues 5 of 12, above a third). Rebuild needed.
**Stumping type:** mechanism: decomposition_attribution with treatment-effect heterogeneity (method/model selection), stumping_family: mixed, surface_read_dependency: yes, sole_data_defect: no. Determinism-side taxonomy: none; Gate H: one_thing_flip.

## Why
The recommendation is forced by the files once the weekend-share moderator is found: To Go saves 2,400 DKK a store (range -6,300 to 6,400) against a 9,000 licence, while reading the format off its three high-street pilot stores gives 23,800 and the wrong switch. The moderator is built into the stores (3 To Go pilots all "Man-lor 08-21, son 10-18"; 3 commuter Kvarter pilots at weekend share 0.17 to 0.19; Kornblomst's weekend ratio 2.42 times AutoOrdre's in commuter stores and 0.91 elsewhere). One sentence ("the forecast only saves in weekend-trading stores, and the pilot's To Go stores are the exceptions") rescues the recommendation, asks 3, 4, 5, 7 and Critical Component 3. Gates A to E otherwise pass. The pass-1 Super fork is now closed by SF14 to SF16 (see below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot / other sales growth, gap | 3.9 / 5.9, -2.0 | 3.87 / 5.88, -2.01 | yes (ties to dashboard) |
| Waste at cost, pilot / other, gap | -9.6 / +7.9, -17.5 | -9.61 / +7.91, -17.52 | yes |
| 840 re-sent 2025 rows; dairy renumbering | yes | yes | yes |
| Quick reading Super / Kvarter / To Go | 60,200 / 45,500 / 23,400 | 60.3k / 45.5k / 23.3k | yes |
| Format growth, AutoOrdre no-opening stores | 4.8 / 4.8 / 10.8 | 4.81 / 4.81 / 10.82 | yes |
| Mix part of sales gap | -0.6 | -0.66 | yes |
| Units turned away, one sale fewer, 2026 / 2025 | 94,100 / 81,300 | 100,100 / 86,700 | inside bands (clipping differs) |
| Units turned away, every sale | 125,000 / 109,200 | 124.7k / 108.5k | yes |
| Overstatement counting every sale, in-stock days with 2+ sales | 9.7 (40.9 on 6 or fewer); one fewer 0.2 | 9.6 (40.3); 0.17 | yes |
| Waste avoided, weekend-trading / commuter pilot stores | 19.7 / -1.3 | 19.2 / -1.2 | inside bands |
| Kornblomst weekend ratio, commuter / weekend-trading | 2.42 / 0.91 | 2.42 / 0.91 | yes (pass-1 0.97 mismatch gone) |
| Openings | -7.0, -4.7, -1.6 / -6.6, -4.3, -0.5 | weekly ratios noisy (about 5 per cent); signs agree for 2131, 3031, 4224; 3012 and 2146 not separable from noise | partial |
| Per-format savings 40,200 / 28,000 / 2,400 and the 400-resample ranges | as stated | not rebuilt end to end by the thread | not independently confirmed |

## Competing answers that survived
1. Super margin route: 4.2 read as recorded margin format by format gives Super -10,800 (stay) against 40,200. The golden rules it out with a placebo on AutoOrdre stores (noise about 20,600 a store-year) and store 2158's recorded margin (63,000 below its format against 3,700 for its turned-away units). The pooled recorded route (30,500) still switches. Thread accepts it as ruled out by named data and asks that it stay closed in the answer text. SF14 to SF16 close the pass-1 fork.
2. Commuter-week counterfactual: using only commuter-week comparators (one Kvarter store, 3170, waste +12.4 per cent) moves the commuter rate to about +4 per cent, outside the stated -4.5 to 2.0 band. It rests on one store. This is Gate C on that result.
3. "80 per cent range" read as uncertainty of the mean (resampling) against a spread across stores: the prompt does not say; the golden takes the first (SF13 names it).
4. "Causes" of the gaps are the author's split (forecast with its 0.75 service factor, mix, openings, residual). The forecast and the service factor are bundled, so the split cannot separate them.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 (8 CSV, 4 XLSX, 1 PDF) | yes |
| Categories | 2 or more | spreadsheet and text by metadata; thread notes thin variety (no image or code) | yes, thin |
| Large messy CSVs | 20,000 rows or more; a 10 to 20 page one | 389,960 / 309,760 rows; bi_uge 19,656 rows | yes |
| Distractors | 2 or more, unlabelled | vejr_dmi, personaletimer (metadata); kampagneplan also unused | yes |
| Deliverables | 1 to 3, all in golden | xlsx and pptx; golden.zip holds exactly them | yes |
| Asks, units, no rounding dictated | yes | yes | yes |
| Answer shape, 4 or more checkable results | yes | 12 graded results by the thread's count | yes |
| LLM tells / realism | none | none found; pilotaftale PDF spells out valuation 4.2 to 4.3 (hands over the saving formula, not an authoring disclosure) | yes |

## Gate G reconciliation
Thread: decomposition_attribution with treatment-effect heterogeneity, stumping_family mixed, surface_read_dependency yes, sole_data_defect no, and "borderline banned scaffold: the format call turns on rejecting the unrepresentative pilot read". The note's Hidden factor record says the commuter-week pattern is constructed across 16 stores of two formats (3 in the pilot) and "not only in deciding units". These disagree on the one point that matters: the thread places the factor in the pilot To Go and commuter Kvarter stores that decide the calls, and says one cross-tab (weekend share against waste change) plus the shadow-forecast ratio and the register's opening hours finish it, so a careful run finds it unprompted. The note's `Largest single hint` says the plain-estimate sentence rescues 2 of 10 and the trading-week sentence 2 and half of R9.

## Stump power (Gate F)
Gate H line: domain pass; layers pass; results 12 graded across 6 areas; one_thing shallow_hidden_factor; effort quick 2, careful 7, thorough 11 of 12; one_fact "the forecast only saves in stores that trade a full weekend, and the pilot's To Go stores are the exceptions" rescues 5 of 12 (recommendation, asks 3, 4, 5, Critical Component 3; ask 7 follows).
Note's effort test: 1, 4 and 10 of 10. The thread's careful grade (7 of 12) is well above the note's 4 of 10, and the one-fact count (5 of 12, about 42 per cent) against the note's 2 of 10. Part of the gap is counting: the thread scores asks and components separately, the note scores ten chain results. The note's own text says the careful pass finding the trading week would earn R7, the call and half of R9. The thread also says the frontier risk is that the moderator is one cross-tab. The careful but hurried run most likely loses To Go 23,800 and Kvarter 16,800 (switching Super and To Go) and the 125,000 units turned away. Results a standard method reaches: headline gaps, mix, openings read off ambient rows, the quick-reading valuation.

## Findings, ranked
1. Gate H one_thing: the trading-week moderator (shallow hidden factor) carries the recommendation, asks 3 to 5, ask 7 and Critical Component 3; one sentence rescues 5 of 12 (above a third). The factor is constructed, sits in the pilot To Go and commuter Kvarter stores that decide the calls, and one cross-tab plus one stratification finishes it. The recommendation turns on rejecting the three high-street To Go pilots as unrepresentative. Disposition SEND_BACK.
2. Thread's effort grades (careful 7 of 12) separate the careful from the thorough pass less than the note's 4 and 10 of 10, and the one-fact count exceeds a third; main thread to weigh this against the effort test and recount on the thread's 12-result basis.
3. Commuter-week rate under a commuter-only comparator is about +4 per cent, outside the stated band -4.5 to 2.0 (one store, 3170). Gate C on that result.
4. Openings: 3012 (-1.6) and 2146 (-0.5) are not distinguishable from noise in the thread's read; the stated "within 2 points" band may be the only thing holding them.
5. Final savings and the 400-resample ranges were not independently rebuilt by the thread; confirmed only by input reproduction and the quick-reading arithmetic.
6. Thin file variety: only three formats (CSV, XLSX, PDF), no image or code file.

## Next action for the author
The thread's fix for the build: spread the heterogeneity across several mechanisms visible through different files (store-specific forecast error by category, shelf life, delivery frequency) and across formats and non-deciding stores; add a pilot To Go store that is a commuter store, so the format call does not rest on the three high-street pilots; keep the Super margin route closed in the answer text; name which causes the two gaps are to be split into. Re-root through `/fix-determinism` or redesign from stage 2 per the main thread's call. The harness allows no further re-judge on this build.
