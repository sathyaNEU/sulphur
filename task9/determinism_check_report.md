# determinism-check report, task9, 2026-11-11

## Verdict
DETERMINISTIC (the judge reproduced every graded figure inside its stated band; two band defects and one wording gap listed below). SOLUTION_WRONG does not apply.
**Disposition:** FIX_NOW (answer blocks only, no pack change), plus a Gate H flag the main thread must weigh: the judge's effort grades and one-fact count are worse than the design note's effort test (see Gate G reconciliation). That flag is the likeliest send-back predictor.
**Stumping type:** mechanism: decomposition_attribution (counterfactual policy simulation and a cost optimisation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread isolation: one thread (general-purpose, sonnet, medium) in /tmp/determinism-check-task9-210105/, fresh unzip as its universe, blocks in graded_blocks.md. Verdict says the order was kept: own_derivation.md written first, then the blocks opened. I spawned no second thread. (This session had no Agent tool; the main session spawned the thread from my judge_brief.md.)

## Why
The pack forces one cause. Zone-8 (outermost zone) fail rate depends only on conditioner-disk age since the disk's own last replacement (cmp_unit_pm_log.xlsx parts text and counters, the four EW-118 retentions, cmp_wafer_fdc.csv platen counter, wafer_sort_zones.csv zone fails). Ring age, pad age, FDC signals, SC-4, DEP-3, RF hours, tester, probe card, test-program rev, slurry lot and the ADC label leave no residual (correlations <= 0.035). Loss, die by product, shares, onsets, counts and saving all recompute from the shipped files.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Loss, points, 1 Apr to 31 Aug, 24,445 wafers | 1.32 (1.23 to 1.41) | 1.32 observed less fresh-disk baseline; 1.33 hinge model | yes |
| Good die P-A / P-B / P-C | 209k / 21k / 316k (each +/-8 %) | 208.6 to 210.4k / 21.2 to 22.6k / 309 to 316k | yes |
| USD value of the loss | about 353k | 355k | yes |
| Pre-April baseline rival | 1.06 (excluded) | 1.07 | yes |
| Classifier EDGE_RING rival | 1.13 (excluded) | about 1.03 | roughly; both below the band |
| Rule shares 2,000 / Rev F / waiver | 23 / 34 / 43 (20-26, 31-37, 40-46) | 25.3 / 33.3 / 41.5 | yes, 25.3 near the band's top |
| Slicing rival | 18 / 40 / 42 (excluded) | 18.6 / 39.7 / 41.8 | yes |
| Onset PU-1/2/3/4 | 1,300/1,300/910/910 | 1,224/1,201/975/768 | inside bands except PU-4 768 vs floor 770 |
| Climb PU-1/2/3/4 | 17.0/17.0/21.2/21.2 | 15.1/17.1/22.2/21.2 | inside |
| Counts | 1,570 (PU-1/2), 1,200 (PU-3/4) | 1,572 / 1,206 with graded pair curves; 1,543/1,489/1,245/1,104 with own unit fits | inside; PU-4 1,104 vs floor 1,100 |
| Yearly saving | 288k (265k to 311k) | 279k to 307k | yes |
| Per-pair split 86k / 203k | no band stated | PU-3/4 193k to 222k | unbanded |

## Thread's own first-pass figures (own_derivation.md, written before the blocks) against each band
| Result | Thread's first pass | Stated band | Inside |
|---|---|---|---|
| R1 loss, points | 1.32 observed less baseline; 1.33 hinge; rivals 1.329 (both retest rows), 1.43 (polish-date window) | 1.23 to 1.41 | yes; polish-date window 1.43 is just outside |
| R2 good die | P-A 208.6k to 210.4k; P-B 21.2k to 22.6k; P-C 309.2k to 315.6k | 192-226k / 19-23k / 291-341k | yes (P-B 22.6k near the top) |
| R3 cause shares | disk wear the only driver (read as 100 %); pad, ring, DEP-3, SC-4, RF hours, tester and the rest 0 (residual correlation <= 0.035); it gave no numeric pad share | disk 92 to 100, pad 0 to 8, others within 2.5 of zero | yes at the disk's upper edge; its ranking below the disk is unquantified, and the thread reads "cause" three ways (see forks) |
| R4 onset PU-1 / 2 / 3 / 4 | 1,224 / 1,201 / 975 / 768 (rivals: free-baseline OLS 1,350 / 1,254 / 1,007 / 826; age <= 2,800 only 1,400 / 1,275 / 1,025 / 875) | 1,100-1,490 / 1,100-1,490 / 770-1,050 / 770-1,050 | yes except PU-4 768, 2 wafers under the floor (its OLS rivals are inside) |
| R4 climb PU-1 / 2 / 3 / 4 | 15.1 / 17.1 / 22.2 / 21.2 | 14.4-19.5 / 14.4-19.5 / 18.0-24.4 / 18.0-24.4 | yes |
| R5 shares, 2,000 / Rev F / waiver | 25.3 / 33.3 / 41.5 | 20-26 / 31-37 / 40-46 | yes (25.3 near the top) |
| R6 counts PU-1 / 2 / 3 / 4 | 1,543 / 1,489 / 1,245 / 1,104 | 1,440-1,700 / 1,440-1,700 / 1,100-1,300 / 1,100-1,300 | yes (PU-4 4 above the floor) |
| R7 yearly saving | 299k to 310k with its own unit fits (279k to 286k with the graded pair parameters) | 265k to 311k | yes (310k near the top) |

The thread reached all seven results inside the bands from the bundle alone, with the field-standard hinge fit on a correctly rebuilt disk age and no help from the blocks.

## Competing answers that survived
None that flips a call. Forks, each with the golden on the right side or inside its bands:
1. Ask 3 "the causes ranked by their share" does not say what a cause is: disk against the named suspects (golden), the three policy components (waiver 41.5 > Rev F 33.3 > 2,000-rule 25.3), or the four units. All put the disk or its policy-driven wear first; the order below differs. Wording finding.
2. Per-unit against per-pair onsets: per-cycle onset spread within a unit is about 200 wafers, so a unit fit and the pair value are both defensible. PU-4 768 sits 2 wafers under the band floor and its count 1,104 sits 4 above. Band edge.
3. Wafer volume per unit (58,500 split equally or by share since 1 June) is not filed; effect about 3 % of the total, inside the band; the per-pair 86k / 203k has no band.
4. Retest handling (replace or keep both rows) moves the loss under 0.01 points and counts about 2 %. The fresh-disk against pre-April baseline fork is the only definition fork with a visible effect, closed by "what has the ring cost" and by Jan-Mar wafers already on worn disks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 25 files (13 non-image plus 12 PNG maps) | yes |
| File categories | 2 or more | 5 (spreadsheet, database, text, image, code) | yes |
| Large CSV, 20,000 rows or more | 1 | process_history.csv 277,077 rows (26 MB) | yes |
| CSV of 10 to 20 printed pages or more | 1 | wafer_sort_zones.csv 37,971 rows (5.3 MB); cmp_wafer_fdc.csv 37,591 rows | yes |
| metadata.json names 2 or more distractors; none labelled inside the ZIP | 2, unlabelled | scanner_sc4_edge_focus.csv, slurry_lot_coa.csv; no label in the ZIP (judge read the files) | yes |
| Distractors unused but weighing | unused by the solution, ruled out by a shipped fact | slurry_lot_coa.csv unused; scanner_sc4_edge_focus.csv is named in ask 3's ruled-out evidence (SC-4's start a week after Rev F), so it is used as a rival; the judge treats all five candidate files as inert for the answer | partly: see Findings 4 |
| Deliverables | 1 to 3, all in the golden | 1 (a deck), tessaline_fab2_edge_ring_review.pptx; golden ZIP holds exactly it | yes |
| Asks multi-dimensional, units stated, no rounding dictated | yes | prompt states units in the asking sentences, dictates no rounding; 7 asks | yes |
| Answer shape, 4 or more results each checkable | one of the 14 shapes | ranked causes with contributions plus a decomposition and a schedule; 7 results | yes |
| Nothing reads as LLM generated; goldens read as real work | yes | judge found real operational texture (mixed part spellings, back-entered rows, one missing PU-2 pad entry, retests, aliases); no README or generator language; I did not open the golden deck itself | yes on the pack; golden realism is for golden-realism |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: the disk's usage dose is a constructed factor across every unit, every disk life and all three products, found by modelling (hidden factor record, "keep, priced Right in the careful column"). Agreement on mechanism and defect class: nothing planted, nothing only in deciding units.

Disagreements the main thread should weigh (the send-back predictors):
- **One-fact.** The thread's best single sentence is "the conditioner disk is the part, counted from its own last replacement", rescuing about 4 of 7 (cause, onsets, counts, part of the saving) before the policy simulation and cost work. The note's `Largest single hint:` is the January to March ring at 2 of 7. That exceeds the "a third or fewer" rule, so the note's hint is not the largest.
- **Effort grades.** Thread: quick 2 of 7, careful but hurried 5 of 7 (loss, die, causes, onsets, counts), thorough 7 of 7. Note: quick 0, careful 2.5, thorough 7. Careful at 5 of 7 is far past a third and the careful column does not separate from the thorough one as the note's table does. The note prices R1, R2 and R5 as Missed in the careful column; the thread earned R1 and R2 by measuring excess against the fresh-disk baseline directly, which is what "what has it cost" reads as, and R5 by running the counterfactuals.
- **Bands.** R1 (1.23 to 1.41), R2 (+/-8 %), R4 (+/-15 % on onset, 1,100 to 1,490 for 1,300) and R7 (265k to 311k) are wide enough that a careful run that finds the disk lands most results. The excluded rivals do sit outside (pre-April 1.06, classifier 1.13, slicing 18/40/42, wafers-since-PM onsets 1,680/1,380, summer rate 781k), so Gate C holds, but the hurried column that stays inside the bands is the point of the effort flag. The note's carry-forward text says a fleet fit "still files R5's shares inside their band", which says the same for R5.
- **Distractors.** The thread does not name a declared distractor as carrying a result. scanner_sc4_edge_focus.csv does feed a named evidence line in ask 3, which weakens its "unused" status.

## Stump power (Gate F)
Moderate with a too-easy risk. The judge's first pass earned all seven results inside the bands. The work that separates careful from hurried is the age construction (retained disks at the four EW-118 PMs, unscheduled swaps changing one part; platen counter or wafers since full PM gives the 1,680/1,380 onsets) and the counterfactual simulation of Rev E and Rev F on each unit's own sequence (slicing gives 18/40/42, outside the bands for two shares). Results a careful but hurried strong model plausibly earns with the field's standard hinge fit: R1, R2, R3 (disk first, the rest none), R4, R6, and R7 if it simulates the cost optimum. The price of the task rests on R5 and the age rebuild; the main thread weighs this against the note's effort test.

## Gate H line
domain: pass; layers: pass (assembly mess: aliases, retests, free-text parts, back-entered and missing log rows, EW-118 retentions; then dose-response, counterfactual simulation, cost optimisation); results: 7 asks, 3 critical components, across 5 areas (assembly, missingness and measurement, modeling, decomposition and attribution, forecasting); one_thing: none; effort: quick 2, careful but hurried 5, thorough 7 (of 7); one_fact: "the conditioner disk is the part, counted from its own last replacement", about 4 of 7 rescued (over the one-third rule).

## Findings, ranked
1. Gate H effort and one-fact exceed the note's own table and the one-third rule (careful 5 of 7, one-fact about 4 of 7). Not a determinism defect; a difficulty one the main thread must price before READY.
2. Ask 4 and ask 6: the PU-3/PU-4 lower bands (onset 770, count 1,100) sit within 2 to 4 wafers of the judge's own unit fits (768, 1,104). Widen the low end (the judge suggests about 730 and 1,080) and say a per-unit fit inside the bands is accepted.
3. Ask 7: the 86,000 and 203,000 pair figures carry no band and the volume split is not filed (judge range about 75k to 95k and 185k to 225k); band them or accept either split inside the total band.
4. Ask 3: the rubric does not name the candidate causes, so the ranking below the disk is not gradable beyond "disk first, others none". Name the candidate list. scanner_sc4_edge_focus.csv and dep_chamber_rf_hours.csv are used as ruled-out evidence there, so check that metadata's distractor list still holds.
5. Step 2 states Jan-Mar ring cost as 0.28; the judge's unit-level fits give 0.28 to 0.35. Record the range.
6. R1's polish-date window rival (1.43) falls just outside the band; the prompt's "wafers sorted" closes it, so no change.

## Next action for the author
Apply findings 2 to 5 in the answer blocks only (no pack change, no rerun of the model), then have the main thread decide on finding 1: either tighten the bands and the effort test so R1, R2, R4 and R6 separate careful from thorough, or re-price the note's effort table to the judge's 5 of 7 before /build stage 5. The judge's disposition is FIX_NOW with one re-judge permitted.
