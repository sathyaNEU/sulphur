# determinism-check report, task9, 2026-11-11

## Verdict
NOT_DETERMINISTIC (ask 2 and R8: the migration call, per-vault split and flip point; the fleet path, batch identity and batch counts hold)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: forecasting (with method selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread note: judge kept the order (own_derivation.md before the blocks). Derivation was bounded: interval, spares and back-test were not rebuilt. Judge files: /tmp/determinism-check-task9-1794418786/verdict.md and own_derivation.md.

## Why
1. Cost convention is open. procurement_and_costs.yaml gives failure_handling_cost_usd 250 ("per replacement: rebuild, technician time, shipping"), unit_cost_usd HX18T8A 210 and vault_migration_cost_usd 60,000 ("move a vault's data to new drives and retire it"). Readings: (a) 250 vs 60,000, break-even 240: B15 runs, B16-B19 migrate (golden); (b) 460 per replacement, break-even 130: all five migrate; (c) 460 vs 60,000 + 1,200 x 210, break-even 678: none migrates. Three files-licensed readings, three calls, three flip points. The design note's fork row 6 pins only 1,200 drives per vault; the 250-only reading is not closed by a shipped sentence.
2. Decision unit is open. The prompt asks one yes/no for "its vaults" and one doubling time; the golden decides per vault and computes the flip for "a vault made wholly of the batch". The aggregate reading migrates all five and gives a different flip point.
3. Per-vault 24-month figures do not follow the vault's own record. Observed replacements in the last four quarters: B15 19, B16 93, B17 75, B18 34, B19 57; golden 24-month: 146, 309, 387, 414, 346. B18 has the lowest observed batch rate (3.2% in Q3 2026) yet the highest golden figure. The call rests on a fitted frailty and ramp.
4. Batch four-quarter band (520 to 665) excludes a plateau reading (about 330) that the record supports: batch Q3 rate eased from Q2 (8.35% to 7.69%), and the ramp shapes are not separated by the data. Gate C on R3.
5. R1 band 720 to 862 contains the rejected inventory-age rival (751).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Replacement definition (FAIL+PULL, tickets for blanks, reseats out, dedup) | as stated | 5,682 deduped flags, 9,697 duplicate rows, 64 reseats | yes |
| Data drives in service 30 Sep 2026 | not stated | 68,387 plus 4 x 2,400 TS24000E installs | yes |
| Batch drives in service (2024 w16-w30) | 4,160 | 4,160 | yes |
| Batch Q3 2026 annualized rate | 7.8% (7.2 to 8.5) | 7.69% (81 over 384,677 drive-days) | yes, in band |
| Firmware story | 5,148 at 6.8% | 5,148 at 6.75% | yes |
| Weeks 10-15 builds | normal rate | 2.8% | yes |
| Vault batch shares B15-B19 | 387, 792, 1,021, 1,122, 825 | same | yes |
| Per-vault 24-month replacements | 146, 309, 387, 414, 346 | not forced by record (last four quarters 19, 93, 75, 34, 57) | no |
| Batch four-quarter replacements | 567 (520 to 665) | plateau about 330 | no, rival outside band |
| Close-out carry-forward | 1,861 | about 1,860 | yes |
| Path 553/587/642/701, 2,483 (2,266 to 2,713) | as stated | not rebuilt; Q3 run rate 465, flat 455 to 487 over four quarters | not recomputed |
| Spares orders, back-test 78.1% | as stated | not rebuilt | not recomputed |
| DC-3 784 / OM-6 281 | as stated | not rebuilt | not recomputed |

## Competing answers that survived
- Migration economics: break-even 240 (golden), 130 or 678 under the other cost readings; calls: B16-B19, all five, none.
- Decision unit: per vault (golden) vs the batch's vaults together; different flip point.
- Batch four-quarter replacements: ramp-weighted 567 vs plateau about 330.
- DC-3: inventory ages 751 versus golden 784, same band.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ | 13 | yes |
| Categories | 2+ | spreadsheet, text, image, code (csv, xlsx, pdf, md, yaml, png) | yes |
| Large messy CSVs | 20,000+ rows and a 10 to 20 page CSV | drive_quarter_stats 979,011 rows; drive_inventory 84,507 rows | yes |
| Distractors in metadata.json | 2+, none labelled in ZIP | 3 (dc_environment_daily.csv, vendor_datasheets.pdf, ssd_boot_drive_stats.csv); unlabelled | yes |
| Distractors weigh but unused | yes | judge: relevant-looking, not carrying a result | yes |
| Deliverables | 1 to 3, all in golden | spreadsheet and PNG; golden ZIP holds exactly these two | yes |
| Asks multi-dimensional, units, no rounding dictated | yes | prompt dictates no rounding; asks multi-part | yes |
| Answer shape, 4+ checkable results | forecast path with bands plus decision | 8 results (R1-R8), 4+ checkable | yes |
| Each result checkable on its own | yes | R8 not independent of the cost convention; R3 band excludes a rival | no |
| Realism | no LLM tells | judge found no authoring disclosure; golden realism not re-audited here | yes (judge) |

## Gate G reconciliation
Judge: one_thing = shallow_hidden_factor (the build-window batch), limited to the batch results; Gate G passes. The note's record calls the build window "modelling" (fix depth), and the judge found it by one by-build-week table: this matches the "found in one look, fixed with one regroup" warning, but the batch carries only R2, R3 and R8 (3 of 8). Note's "not only in deciding units" claim: the judge's finding is that the window sits only in B15-B19 and a mismatch with the note's claim ("no: the window's drives also sit as spares in DC-1") is minor but should be re-checked by the author. Mechanism and stumping family agree with the note (forecasting, analytical).

## Gate H line
domain: pass; layers: pass; results: 9 graded across 6 areas (the note lists 8); one_thing: shallow_hidden_factor, limited to the batch results; effort: quick 2, careful 4, thorough 8 of 9; one_fact: "the bad HX18 drives are the 2024 w16 to w30 builds, not the HX8.2.0 firmware" rescues about 3 of 9. Note's hint: "the vaults retired at the reviews were failing fastest", 2 of 8.
Reconciliation: the judge's careful column (4 of 9, 44%) is close to the note's 4.5 of 8, fine; quick pass 2 of 9 (22%) under a third; the note's quick 0.5 of 8 is lower. The judge's one-fact sentence rescues 3 of 9 (a third), the note's 2 of 8 is understated. The judge saw the DC-3 band contain the rival, so R1 is partly earned by the quick pass.

## Stump power (Gate F)
Honest stumps: build-window batch vs firmware label, DC-3 age rebuild, OM-6 survivorship, P2 pull transient. Careful-but-hurried loses the batch figures (5,148 at 6.8%, flip 18.1 months) and the OM-6 pooled-curve figure (345). Weakened by: the DC-3 band containing the 751 rival; a back-test band (67.0 to 89.2) that contains the hurried 75.0 coverage; wide path bands. Results the field's standard method reaches: Poisson-count-free carry-forward and the pooled-curve paths are separated; the back-test and the quarterly path are within reach of a careful bootstrap run.

## Findings, ranked
1. R8 migration call rests on an unfiled cost convention (three readings, three calls). Underspecified objective.
2. Decision unit (per vault vs the batch's vaults together) and the flip-point definition are not set by the prompt.
3. Per-vault 24-month projections conflict with the vault's own observed record (B18).
4. R3 band excludes a plateau rival (about 330); ramp shapes not separated by the data.
5. R1 band contains the rival (751); ask 4 band contains the hurried method.
6. "Accelerating rate" is weakly supported by Q3 versus Q2.
7. Interval, spares and back-test figures not independently recomputed in this pass.

## Next action for the author
Run /fix-determinism on R8: pin the migration cost convention in procurement_and_costs.yaml (replacement price and what migration buys), state in the prompt whether one decision is asked for the batch's vaults or per vault and for what the doubling time is computed, rebuild the per-vault 24-month projections from the vault's own record or file the vault-effect process behind them, and tighten the R1 band and widen or justify the R3 band against the plateau reading. A rerun is required afterwards.
