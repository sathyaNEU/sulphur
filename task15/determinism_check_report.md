# determinism-check report, task15, 2026-11-11

## Verdict
DETERMINISTIC (one advisory fork on the Super figure)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution with method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scratch: /tmp/determinism-check-task15-381148/ (verdict.md, own_derivation.md). The thread derived its own answer first, then opened graded_blocks.md. One thread, one pass. The brief was spawned by the main session because this runtime has no Agent tool.

## Why
Headline gaps, conformance (re-sent 2025 rows, renumbered dairy items), format-mix and opening parts, unseen-demand figures and the trading-week split reproduce from the files. Agreement clauses 4.1 to 4.3 fix the saving, the x2 annualisation and the all-stores-in-format average. One live fork remains: Super's saving rests on a margin rate estimated from four pilot stores, and the judge built a defensible rival below the licence that lies outside the stated Super band (28,300 to 47,000).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Sales growth pilot / other, gap | 3.9 / 5.9, -2.0 | 3.87 / 5.88, -2.01 | yes |
| Waste at cost growth, gap | -9.6 / +7.9, -17.5 | -9.61 / +7.91, -17.52 | yes |
| Pilot list | 16 stores | 16 (Annex 1 = order basis) | yes |
| Format growth, AutoOrdre no-opening stores | 4.8 / 4.8 / 10.8 | 4.81 / 4.73 / 10.82 | yes |
| Format mix part, sales / waste | -0.6 / -1.2 | -0.647 / -1.239 | yes |
| Units turned away, every sale | 125,000 / 109,200 | 125,253 / 109,072 | yes |
| Units turned away, one sale fewer | 94,100 / 81,300 | 100,100 / 86,700 (interpolated; last-sale-missing days dropped) | inside bands (90,300-104,700 / 78,000-91,100) |
| Waste avoided, weekend-trading / commuter-week pilot stores | 19.7 / -1.3 | 19.2 / -1.2 | inside bands |
| Weekend/weekday ratio, Kornblomst over AutoOrdre | 2.42 commuter, 0.91 weekend | 2.42, 0.97 | commuter yes; weekend 0.97 vs 0.91 (no band stated) |
| Weekend-share split | 0.23 | gap between 0.205 and 0.253, midpoint 0.23 | yes |
| Sales / waste parts sum | -2.0 / -17.5 | ok | yes |
| Super saving | 40,200 (28,300 to 47,000) | 49,400 (pooled, recorded margin); about 20,600 (Super-only rate, recorded margin) | pooled inside band; Super-only rival outside it |
| Kvarter saving | 28,000 | every route above the 20,000 licence (43,700 recorded-margin route) | forced |
| To Go saving | 2,400 | stays off against 9,000 | yes |

## Competing answers that survived
1. Super: pooled-by-trading-week rate with recorded gross margin gives 49,400. A Super-only rate with recorded margin (waste rate 17.2 per cent, margin -0.44 per cent of sales) gives about 20,600, below the 27,000 licence, and lies outside the 28,300 to 47,000 band. The golden's choice (pool by trading week, take the margin from the units the empty shelves turned away because recorded margin is noisy store to store) is the better analysis, but it is stated as a result, not closed as a convention in the fork table. The 80 per cent range (22,200 to 55,800) already straddles the licence.
2. "Gap in percentage points" is read as a difference of growth rates, which the answer blocks state. A level reading (waste share of sales, -0.81) is a second reading that the prompt alone does not exclude.
3. To Go: carrying the commuter-week rate to To Go stores that have no commuter pilot store is an assumption, but the shadow forecasts show the same weekend over-weighting there (ratios 1.95 to 3.07). Judge accepted it as carried by the files.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 | yes |
| File categories | 2 or more | CSV, XLSX, PDF (spreadsheet and text) | yes |
| Large messy CSVs | one of 20,000 rows or more; one of 10 to 20 printed pages or more | 389,960 / 309,760 / 309,760 rows; bi_uge 19,656 rows (about 400 pages), staff hours 1,470, profile 1,435 | yes |
| Distractors in metadata.json | 2 or more, unlabelled in ZIP | vejr_dmi_2025_2026.csv, personaletimer_frisk_2026.csv; unlabelled | yes |
| Distractor weighs, unused | relevant, ruled out by a shipped fact | weather and staff hours; judge found them unused and unlabelled; I did not re-run them | yes (not independently run) |
| Deliverables | 1 to 3, all in golden | xlsx and pptx; golden.zip holds exactly these two | yes |
| Asks multi-dimensional, units stated, no rounding dictated | yes | prompt dictates none; units stated (points, DKK) | yes |
| Answer shape, 4 or more checkable results | one of the fourteen | gaps split into causes plus an allocation/switch with its range; 9 to 10 results | yes |
| No LLM tells / real work product | yes | judge: dashboard reads as a real BI report; no authoring language; no em dashes in submission | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution with method_or_model_selection; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. The note's Hidden factor record lists three constructed factors (censored demand, the commuter-week weekly pattern, discounter openings), each "not only in deciding units": the commuter-week pattern sits in 16 stores of two formats (3 in the pilot), though it decides To Go (12 stores) and not Kvarter. Thread and note agree on classification. Risk to watch: the trading week is a constructed factor, and the one-fact count sits at the edge (see Stump power).

## Stump power (Gate F)
Gate H line: domain pass; layers pass (L1: re-sent rows, renumbered items, layout drift, category-code renames; L2: attribution, censored demand, effect heterogeneity, resampled ranges); results 9 graded across 6 areas; one_thing none; effort quick 2, careful 4, thorough 8 of 9; one_fact "the forecast only saves in stores that trade through the weekend" rescues about 3 of 9.
Note's effort test: 1, 4 and 10 of 10; largest hint rescues 2 of 10 (the trading-week sentence, 2 and half of R9). The thread's careful grade (4) matches the note. Its thorough grade (8 of 9, against 10 of 10) is the Super fork, so the thorough pass is not guaranteed to earn all results. A careful but hurried strong model likely earns the dedup, renumbering, mix and headline gaps (the thread expects it to file Super 33,100, Kvarter 16,800 not switched, To Go 23,800 switched) and loses the demand correction, the trading-week saving and the ranges.
Results a standard method reaches without the data forcing a judgment (earned by the runs): the headline gaps, the openings (R4, graded Right in the careful column by the note), and the two gap splits.

## Findings, ranked
1. Super band excludes a rival the thread ran (Gate C on R8/R9): Super-only rate with recorded margin, about 20,600, below the 27,000 licence and outside 28,300 to 47,000. The pooling convention (rates pooled by trading week across formats) and the margin source (units turned away, not recorded margin) are not closed rows in the fork table. The submission's own "recorded-margin route" figure (Super 29,400 in the note, 30,500 per the thread) uses a different route from the thread's 20,600.
2. Weekend-trading shadow-forecast ratio: block says 0.91, thread recomputed 0.97 (commuter 2.42 matches). No band on this figure; the Critical Component 3 sentence quotes it. Check the generator's population or weighting and either state a band or restate.
3. "Gap in percentage points" is a difference of growth rates, not stated in the prompt; blocks pin it. Add to the fork table and ask 2's text.
4. One-fact count is about 3 of 9 (the note says 2 of 10): at the one-third limit. The trading-week sentence carries R7, R8's Kvarter and To Go cells, R10 and half of R9. Not a send-back on its own, but there is no slack.
5. One-sale-fewer unseen demand: thread got 100,100 / 86,700 against 94,100 / 81,300; inside bands, but the top of the band absorbs the thread's route. Informational.

## Next action for the author
Close Finding 1 in the generator and note: add two fork rows (pool the rates by trading week across formats; margin part from the units turned away), run the Super-only recorded-margin rival, and either rule it out with named data (the within-type spread of waste rates, store 2131's opening) or widen the Super band to include it; then re-run `checks.py`, rebuild, and re-judge once if the band changes. In the same pass restate or band the 0.91 ratio (Finding 2) and add the percentage-point reading to the fork table (Finding 3). No pack change expected.
