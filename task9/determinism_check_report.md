# determinism-check report, task9, 2026-11-11

## Verdict
DETERMINISTIC (every graded figure reproduced inside its band on the careful path; three wording defects and two unreproduced side figures). SOLUTION_WRONG does not apply.
**Disposition:** FIX_NOW (answer blocks only; pack and prompt unchanged), plus a Gate H flag for the main thread: the blind first pass earned more of the chain than the design note's effort test allows (see Gate G reconciliation).
**Stumping type:** mechanism: decomposition_attribution (with method_or_model_selection and a cost optimisation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet judge, medium effort, scratch /tmp/determinism-check-task9-224350/. It kept the order of work: prompt section only, then own_derivation.md, then graded_blocks.md (the addendum in own_derivation.md is marked as written after opening the blocks). This report supersedes the earlier report written on the first chain.

## Why
The ring is zone 8 only; the cause is the conditioner disk's own use. Ring age, pad age, downforce, DEP-3 and SC-4 carry nothing once the disk curve is in. The disk lot (A165-L2603, about 1.5x faster wear than L2509/L2511) and the downforce pair set onset and climb. Final test's burn-in shows the ring from about 0.55 of the sort onset. The decision follows from cost_inputs.yaml. The shortcuts land on different figures (classifier or pre-April baseline 0.62 to 0.71; all-lot pooling counts about 1,700 and 1,250; sort-only costing 1,240 to 1,290; final test from the sort curve 9k to 16k units).

## Blind first pass against each stated band (own_derivation.md above the addendum only)
| Result | Stated (band) | First pass | Inside? | How it got there |
|---|---|---|---|---|
| Loss at sort, points | 0.90 (0.84 to 0.96) | 0.909 (first-row 0.913, all rows 0.914) | inside | wafer_sort_zones.csv, latest retest row, window by sort_end_ts (24,414 wafers); zone 8 fails minus product young-disk floor times tested die; mean of per-wafer excess/gross |
| Good die P-A | 139,000 (128,000 to 150,000) | 140,654 | inside | same, floor fitted |
| Good die P-B | 14,000 (13,000 to 15,000) | 14,553 | inside | same |
| Good die P-C | 226,000 (208,000 to 244,000) | 221,916 | inside | same |
| Causes' shares | disk 96.3 (88 to 100), pad 3.7 (0 to 10), rest none | named the disk as the cause; ring age, pad age, downforce, month, tester found null; shares not produced in the golden's frame, ranked instead by disk-age band (48/28/24), lot (54/25/21), unit (34/32/22/12) | not comparable: disk named, no share table, cause frame left open | rebuilt part ages from PM log and FDC counters, residuals by ring age after a disk model; EW-118 retentions break the co-reset |
| Final test units lost P-A | 44,300 (39,000 to 49,600) | 9,300 to 11,500 | outside | lot burn-in rate regressed on lot exposure from the sort-hinge excess (slopes 0.137, 0.086, 0.123) |
| Final test P-B | 3,500 (3,100 to 3,900) | about 700 | outside | same |
| Final test P-C | 67,100 (59,000 to 75,200) | 13,100 to 16,400 | outside | same |
| Onset PU-1 / PU-2 | 840 (760 to 920) | 913 / 900 (direct L2603-only: 803 / 893) | inside | joint hinge fit on L2603 disks, lot multipliers (onset x0.658, slope x1.445), product floors, disk age from serial lot |
| Onset PU-3 / PU-4 | 640 (580 to 700) | 628 / 560 (direct: 628 / 637) | PU-3 inside, PU-4 joint fit outside (560), direct inside | same |
| Climb PU-1 / PU-2 | 15.8 (13.4 to 18.2) | 16.3 / 16.3 (direct PU-1 11.2, PU-2 16.0) | inside; direct PU-1 outside | same; PU-1 has about 1,140 wafers of L2603 history |
| Climb PU-3 / PU-4 | 23.5 (20.0 to 27.0) | 24.1 / 23.8 (direct 24.5 / 24.6) | inside | same |
| Count PU-1, PU-2 | 1,010 (930 to 1,090) | 1,244 / 1,235 | outside | cost-per-wafer minimum, change cost 5,720, sort loss plus FT at a latent coefficient from the regression above |
| Count PU-3, PU-4 | 840 (770 to 910) | 937 / 896 | outside | same |
| Yearly saving | 519,000 (467,000 to 571,000) | about 556,000 (88k + 90k + 186k + 192k); pairs 178k and 378k against 186k and 332k | total inside, PU-3/PU-4 split 14 per cent high; no pair band stated | savings against Rev F at 2,800 wafers on the same disks |

Addendum (written after the blocks were open, so not a blind result): with a latent burn-in ramp the judge reached 43,906 / 3,690 / 67,299 (114,895), counts 1,020 / 850 (golden parameters) or 1,050 / 1,040 / 840 / 820 (own L2603 parameters), saving 483k to 498k. That path used knowledge of the filed plateau and base, so it shows the golden is reachable, not that a blind run finds the ramp.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Loss at sort | 0.90 points | 0.909 | yes |
| Good die P-A / P-B / P-C | 139k / 14k / 226k | 140.7k / 14.6k / 221.9k | yes |
| USD 243k at die values, USD 104k at final test | as stated | 242k, 103.6k | yes |
| Final test units | 44.3k / 3.5k / 67.1k, 114.9k | 43.9k / 3.7k / 67.3k, 114.9k (ramp model) | yes, after the ramp |
| Onset, climb by pair on L2603 | 840 / 15.8; 640 / 23.5 | 870 / 16.2; 622 / 24.7 (pair fits) | yes |
| Counts | 1,010 / 840 | 1,020 / 850 (golden parameters) | yes |
| Saving | 519k (186k + 332k) | 483k to 498k (177k + 306k to 321k) | total yes; split 4 to 8 per cent low |
| Classifier-only loss | 0.70 | 0.62 | no |
| Pre-April baseline | 0.69 | 0.71 | no (near) |
| Six ring-only swaps, L2603 vs earlier lots (about 0.66x onset, 1.45x slope), pooled onsets | as stated | six UNSCHED ring entries; lot ratios match; pooled counts about 1,700 / 1,250 | yes |
| SC-4 start | "a week after Rev F" | 7 April vs 2 April (design note says 10 April) | wording loose |

## Competing answers that survived
1. Causes ranked by share has no filed frame. By disk-age band the ranking is Rev F extension 48, old interval 28, EW-118 beyond 2,800 24; by lot 54/25/21. The golden's frame (physical candidates) is the natural reading of "what is causing", but the prompt does not fix it. Gate E, mild; close in the ask text.
2. PU-1's own L2603 fit is thin (about 1,140 wafers): free floors give 803 / 11.2 (climb outside), fixed floors 896 / 14.6. The sentence "a unit's own fit inside these bands is accepted" does not cover a fit that lands outside; PU-4's joint fit (560) is outside the onset band the same way.
3. Final-test base from lots under 500 wafers (0.26 per cent) puts P-A at about 38.3k, 2 per cent under the band floor. Edge case.
4. Hinge onset moves 100 to 150 wafers with the functional form (curve mildly concave); bands cover the hinge fits except the PU-4 joint one.
5. Retests (734 wafers): latest, first, both rows change the loss by at most 0.005 points. No effect.
No fork changes the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 27 (15 data files plus 12 wafer-map PNGs) | yes |
| Categories | 2 or more | 5 (spreadsheet, database, text, image, code) | yes |
| Large messy CSVs | 20,000 rows or more, and one 10 to 20 pages or more | process_history.csv 277,063 rows (26 MB); wafer_sort_zones.csv 37,930 rows (5.3 MB) | yes |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | 3 named (scanner_sc4_edge_focus, slurry_lot_coa, facility_particle_counts); file names carry no label | yes |
| Distractors unused yet weighing | arithmetic and a shipped fact rule out | SC-4 raw z8 0.214 vs 0.14 and DEP-3 raw 0.168 vs 0.155 reproduce; residual after the disk curve 0.001 and 0.000; routing and the 7 April start rule them out | yes |
| Deliverables | 1 to 3, all in golden | 1 (pptx), golden ZIP holds exactly it | yes |
| Asks | multi-dimensional, units stated, no rounding dictated | seven asks in one deck; units in the sentence; no rounding in the prompt (887 characters) | yes |
| Answer shape | one of fourteen, 4 or more checkable results | schedule/allocation with sensitivity; 6 results | yes |
| Nothing LLM generated | | judge found no authoring language, no README, noise present (aliases, retests, a back-entered PM entry, a blank counter, sub-lots); golden realism not re-read here | yes (judge) |

## Gate G reconciliation
Judge: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: every factor constructed but across all units, lots, months and products; none only in the deciding units; hidden factor record says the lot factor is "modelling" depth, which matches the judge (a joint fit with lot multipliers found it, and the blind first pass did so unprompted). No single thing carries most results.

## Gate H
domain: pass. layers: pass (aliases, retests, counter gaps, serial-to-lot join, sub-lots; attribution, lot-pair curves, latent final-test model, cost optimisation). results: 7 asks over about 7 areas. one_thing: none. effort: quick 1, careful 3, thorough 7 of 7. one_fact: "the current disks are lot L2603, fit that lot" rescues asks 5, 6 and 7 in part, 3 of 7.
Weighed against the note's effort test (quick 0 of 6, careful 2 of 6, thorough 6 of 6, hint rescues 2 of 6):
- Careful column. The blind first pass earned R1 fully, R4 on three of four units and the joint-fit onset/climb inside the bands without any hint (it fitted the lot as a multiplier on its own), and R6's total (556k inside 467k to 571k). It missed R3 and R5 and gave no R2 share table. That is 3 to 4 of 6 results, against the note's 2 of 6 with R4 and R6 Missed. The note's R4 and R6 cells are therefore too hard; the lot link is found by a standard serial-to-receipts join and a joint fit.
- Quick pass 1 of 7 (the loss at sort) against the note's 0.
- One fact: 3 of 7 is above a third (note says 2 of 6, exactly a third); the note's "largest single hint" understates what the lot sentence rescues, though final test stays unsolved after it.
- What does price the task: R3 (final test), a factor of four off from a regression on the sort exposure, and R5, which inherits it. Both need the early burn-in ramp, which the judge found only after reading the blocks. If the platform runs also find the ramp unprompted, the task will score high.
- R1 and R2 are Right in the careful column as the note says; R2's frame is open (fork 1).

## Stump power (Gate F)
Hurried paths fail on different figures, as listed under Why. A strong careful run earns the loss, the cause and the lot-corrected curves; final test, the counts and the pair split are where it can lose. Plausible score 45 to 60; the main thread should weigh the upper end against the 60 line given the first pass's reach.

## Findings, ranked
1. Effort test on paper is too hard for R4 and R6 (blind first pass reached them); the chain's price rests on R3 and R5.
2. Ask 3 has no filed frame for "causes ranked by their share" (Gate E).
3. "The only disk lot left in stores" has no inventory record in the pack; the files show only issue order and no later receipt. Reword to "the lot every unit runs now".
4. PU-1 own-fit and PU-4 joint-fit land outside their bands; the "own fit accepted" sentence does not cover them. Add the fixed-floor caveat or widen PU-1's climb to 11 to 18.2 and PU-4's onset floor.
5. Unreproduced side figures: classifier-only 0.70 (judge 0.62), pre-April 0.69 (0.71), per-pair saving split (4 to 8 per cent low), SC-4 "a week after" (5 days in the record, 10 April in the note). Restate from the data or drop.

## Next action for the author
Reword the answer blocks (findings 2 to 5) in one pass without touching the pack, then decide with the main thread whether the effort test and the note's R4 and R6 cells need rewriting to the blind first pass's reach before READY. No second judge run.
