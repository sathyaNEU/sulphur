# determinism-check report, task9 (architecture 8), 2026-11-10

Cut judged: target.zip sha256 4a76ff2f7a1a06df79268d72bfa793365bc9839bab42b327fd7ccf84ff29108c, fresh unzip at /tmp/determinism-check-task9-1794304326/target/ (21 files). One medium-effort thread, read-only under that scratch path. It reports it kept the order (own_derivation.md written before graded_blocks.md was opened); it adds that its dealer-basis refit and plan-range replication were done after reading the blocks. Both are marked as such in its verdict.

## Verdict
**Verdict:** DETERMINISTIC
**Disposition:** FIX_NOW. Pin in one clause of the prompt (or in the Supplementary wording) whether "the 12-month ladder's peak collateral" is at its actual USD 50,000 a point or per USD 100,000 a point, and which ladder's size the collateral CSV uses ("that size"); no data change, no change to the stump. Otherwise ship.
**Stumping type:** mechanism: method_or_model_selection (with forecasting and statistical_rigor), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

**Gate G line (thread):** mechanism: method_or_model_selection (with forecasting and statistical_rigor), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

**Gate H line (thread):** domain: pass, layers: pass, results: 9 graded across 6 areas, one_thing: none, effort: quick 2, careful 5, thorough 9 of 9, one_fact: "the 3-month strikes before September 2009 have to be rebuilt from the 1-month and the next longer index, not from the 1-month alone" rescues about 3 to 4 of 9.

## Why
The golden reproduces from the shipped files. The thread's independent engine reproduced all 104 rows of CFF_VolPremium_Settlements.csv to USD 0.005 and all 28,812 dealer valuation rows to within USD 3. It landed on a 3-month size of 111,800 to 113,800 depending on the strike rebuild (golden 114,400, band 100,000 to 117,000), a 6-month size of 58,530 (golden 58,700), the 12-month peak of 25,874,000 on 2020-03-18 (golden 25,876,000), open swaps of 2,487,000 with 80% range 394,000 to 4,247,000, and a plan range of minus 4,205,000 to 12,219,000 (golden minus 4,203,000 to 12,204,000). Every committed answer is pinned by the data or carries a band that the rivals the thread ran fall inside. The one real softness is the unit and scope wording of two asks (Gate E, below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 3M size, limit, day | 114,400, collateral, 2008-11-20 | 111,769 (interpolation), 113,758 (least squares on VIX and next longer index), 113,726 (geometric), 113,882 (midpoint); collateral limit on 2008-11-20 in every variant | yes, in band |
| 3M settlement-limit-alone size | 157,900 | 156,500 to 161,100 | yes |
| 30-day stand-in size | 124,500 (wrong) | 131,046 on the thread's valuation basis; outside band | direction yes, figure differs |
| 6M size | 58,700 | 58,530, collateral, 2008-11-20; settlement alone 108,337 | yes |
| 3M average per sale per 100,000 | 284,000 (282,000 to 287,000) | 282,957 to 285,608 across rebuilds | yes |
| 3M worst year | 2008, 16,154,000 (15.65M to 16.39M) | 2008, 16,300,000 | yes |
| 80% range, 3M and 12M averages | 143k to 413k; 63k to 552k | 3M block 142k to 407k, HAC 146k to 420k; 12M block 69k to 556k, HAC(12) 77k to 553k; iid 194k to 372k and 228k to 402k fall outside | yes |
| 12M peak collateral at 50,000 | 25,876,000 (2020-03-18; 2008-11-20 at 25,287,000) | 25,874,000 on 2020-03-18; 25,340,000 on 2008-11-20 | yes |
| Open swaps 2027 | 2,494,000; 394,000 to 4,247,000 | 2,487,000; p10 393,900, p90 4,247,200 (4,761 start dates); dealer value 1,883,000 | yes |
| Plan 2027 | 5,728,000; minus 4,203,000 to 12,204,000 | 12M leg 2,806,000, 3M leg at 114,400 2,924,000; range minus 4,205,000 to 12,219,000 over 4,717 start dates, 10.9% negative | yes |

Dealer basis: the days-weighted blend of realized and implied variance is exact. The implied term is not a filed rule, but total-variance interpolation on the nodes VIX9D 6, VIX 21, VIX3M 63, VIX6M 126, VIX1Y 252 business days (anchored at zero) fits the dealers' implied volatility at rounding level (mean error 0.01, sd 0.16). Linear-in-volatility interpolation is biased 0.2 and gives a 12-month peak of 26.56M and a 6-month size of 53,800, both outside the golden's bands.

## The thread's own first pass
What own_derivation.md reached before graded_blocks.md was opened, against the band in the graded blocks. The first pass used linear-in-volatility interpolation for the dealers' implied term, so its mean implied-vol error was about 0.2 points.

| Result | First-pass figure (before blocks) | Band in graded blocks | Inside |
|---|---|---|---|
| Strike rebuilds tried and 3M size (collateral limit, 2008-11-20 in each) | interpolation 105,000; VIX-and-1Y interpolation 110,100; total variance 96,400; VIX itself as strike 118,100. Base case 105,000 | 100,000 to 117,000 | base case yes; 110,100 yes; 96,400 no; 118,100 no |
| Binding limit and day (3M) | collateral, 2008-11-20 | collateral, 2008-11-20 | yes |
| 6-month size | 53,800 (53,400 with a +0.2 implied bias); collateral | 54,000 to 59,000 | no |
| 3M average per sale per 100,000 | 285,807 | 282,000 to 287,000 | yes |
| 3M worst year | 2008, 15.84M paid | 2008, 15,650,000 to 16,390,000 | yes |
| 3M average range, iid | 199k to 372k | low 131k to 159k, high 399k to 436k | no |
| 3M average range, block / HAC | 154k to 407k / 154k to 417k | same | yes |
| 12M average range, iid | 228k to 402k | low 14k to 82k, high 537k to 616k | no |
| 12M average range, block / HAC | 75k to 556k | same | yes |
| 12-month peak collateral | 53.13M on 2008-11-20, per 100,000 a point (about 26.56M at 50,000; 2020-03-18 not reported as the peak) | 25,800,000 to 26,500,000 on the 50,000 ladder | no |
| Open swaps' expected settlement | about 2.48M (dealer-basis value 1.91M) | 2,390,000 to 2,890,000 | yes |
| Open swaps' 80% range | about 0.30M to 4.25M | low 200k to 420k, high 4.10M to 4.43M | yes |
| 12M plan leg | about 2.8M | 2,705,000 to 3,205,000 | yes |
| 3M plan leg (at its own 105,000, illustrative) | 2.70M | 2,530,000 to 3,030,000 | yes |
| Sleeve plan | about 5.5M | 5,235,000 to 6,235,000 | yes |
| Plan 80% range | not derived ("not pinned to one figure by the files") | low -4.3M to -1.9M, high 11.2M to 12.4M | not reached |

Count: of 14 first-pass results in the table (base case on the size row), 11 sit inside their band (3M size base case, limit and day, 3M average, 3M worst year, 3M block/HAC range, 12M block/HAC range, open swaps expectation, open swaps range, 12M leg, 3M leg, sleeve plan), 2 sit outside (6-month size, 12-month peak), and 1 was not reached (plan range). The iid ranges and two of the four rebuild sizes fall outside, as the blocks say they should. The thread noted before reading the blocks that the 3M size spread was about plus or minus 10 percent from the unstated pre-2009 strike, and that the 6M size was proxy-independent but set by the dealer curve reading. After reading the blocks it refit the dealer curve and moved both outside figures into band (58,530; 25,874,000).

## Competing answers that survived
- Unit of the 12-month ladder's peak collateral: "per USD 100,000 a point" opens the clause listing the average, worst year and ranges, and the peak follows a semicolon. The golden reads it at the ladder's actual 50,000 a point (25,876,000); the other reading is 51,747,000 per 100,000. The first pass took the second reading. Real prompt-scope fork (Gate E).
- Which size the collateral CSV uses ("at that size"): 3M at 114,400 in the golden; the 6M size is the other literal reading. Same fork class.
- Pre-publication 3M strikes: no rule gives them; reasonable rebuilds span 111.8k to 113.9k, inside the band. The band is wide (about 15 percent) and its upper end would breach the limit by roughly USD 0.4M at the golden's own strikes. A looseness of the band, not a surviving rival.
- Short-lag HAC on the 12-month range (123k to 507k): excluded by the band, the one range-method rival with weight.
- A GARCH-type forecast of the open swaps was not run by the thread and could land near the band edges.
- Pooled against per-dealer collateral: D.5(d) "taken together" governs. Closed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 21 (7 PDF, 12 CSV, 1 XLSX) | yes |
| File categories | 2 or more | spreadsheet (xlsx, csv), text (pdf) | yes |
| Large messy CSVs | one of 20,000 rows or more, one of 10 to 20 printed pages or more | Larkhill_DealerValuations_Daily.csv 28,812 rows; Larkhill_CollateralLedger.csv 3,984 rows, VIX_History 9,312, SKEW 9,266, SPX 13,073 | yes |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | VVIX_History.csv, SKEW_History.csv; the thread names SKEW, VVIX, VIX9D (node only) and the collateral ledger as deciding nothing | yes |
| Distractors unused yet relevant | weigh, not answer a graded quantity | thread found none that answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, csv, docx); golden.zip holds exactly these 3; CSV has 4,995 data rows | yes |
| Asks multi-dimensional with unit and rounding | yes | 9 asks, units and rounding stated, except the two scope wordings above | partial (see Findings) |
| Answer shape | one of the fourteen, 4 or more checkable results | allocation with its sensitivity and a forecast with bands; 11 results in the note, 9 graded per the thread | yes |
| Reads as real work product | yes | thread found no authoring language; cosmetic wrapped dates in statement PDFs | yes |

I did not independently audit realism of the golden documents or the page length of each CSV; the thread's hygiene read covers the pack only.

## Gate G reconciliation
The note's Hidden factor record lists four factors, all marked real (public data used as is) and none only in the deciding units. The thread agrees: stumping_family analytical_non_defect, sole_data_defect no, surface_read_dependency no, one_thing none. The thread names the early-strike rebuild as the common input of four results, which matches the note's carry-forward (a slip on the rebuild costs R1, R2, R4, R7, R10, R11). One discrepancy: the thread counts 33 pre-September-2009 3M sale dates, the note and golden say 32 strikes. This does not move any figure but the author should check the count in the prose.

## Gate H and effort reconciliation
- Thread: quick 2, careful 5, thorough 9 of 9. Note: quick 0, careful 3, thorough 11 of 11. The thread's quick pass is under a third. Its careful pass at 5 of 9 (56 percent) is above the note's 3 of 11; the thread and the note place the careful-run losses differently. The note grades R3 (12-month peak) and R5 (6-month size) as Right for the careful but hurried run. The thread's own first pass lost both (53,800 and 53.13M per 100,000) because it read the dealers' curve linearly and read the unit differently. The note should either price R3 and R5 as Missed for a hurried reader of the dealer curve, or the data should pin the interpolation by one filed statement of the dealers' basis. This is a pricing question for the main thread against the effort test.
- One-fact: the thread's sentence rescues 3 to 4 of 9 (33 to 44 percent), borderline against the one-third limit. The note's own largest hint rescues 3 of 11 (27 percent). On the thread's 9-result count the hint is at or just over a third. The main thread should recount against the graded rubric.
- The note's two-move rescue (rebuild plus expectation) is consistent with the thread's finding that the dealer curve, the expectation, the ranges and the plan need their own work.

## Stump power (Gate F)
Good. Hurried routes cost several results at once and the losses are analytical: the VIX-only strike stand-in (124,500 against 114,400; average 300,000; worst year 14.1M), the linear-in-volatility dealer curve (6M size 53,800 and 12M peak 26.56M, both outside), iid ranges, valuing open swaps at the dealer value (1.88M against 2.49M), and independent draws for the plan range (0.5M to 9.8M). The thread's own first pass, by a medium-effort route that was neither hurried nor complete, still lost 2 results and left the plan range unreached while earning the rest, which is the profile of a careful run with unfinished chain. Results this thread reached by the field's standard method with little judgment: the 3M average and worst year (once the rebuild uses both neighbours), the open swaps' expectation (once the ratio of realized to implied is tried), and the block/HAC ranges. Weakness: the 3M strike rebuild is the common input of four results.

## Findings, ranked
1. Gate E (ask scope): the unit of the 12-month peak collateral and the size used for the CSV are not pinned by the prompt's wording. Repairable in one clause. It sits in a supplementary ask, with the main call forced and G and H passing, so it is an ask-layer wording fix and spends no architecture.
2. The 3M size band (100,000 to 117,000) is wide; its upper end breaches the limit at the golden's own strikes by about USD 0.4M. Optional: narrow the band toward 110,000 to 117,000.
3. The dealers' implied-vol interpolation is not filed; the data pins it (total variance) but a linear reader lands outside the bands on two results. Decide whether that is intended difficulty (then price R3 and R5 accordingly in the effort table) or a fork to close.
4. Effort-table mismatch with the thread's grades (careful 5 of 9 against 3 of 11) and a one-fact count at or over a third on the thread's reckoning.
5. Count of pre-publication 3M strikes (33 against 32): check the prose.
6. No GARCH-type forecast of the open swaps was run; a residual unknown, not a finding.

## Next action for the author
Add one clause to the prompt pinning that the 12-month ladder's peak collateral is at its present USD 50,000 a point (not per USD 100,000) and that the collateral CSV is at the new ladder's recommended size; then re-check that no graded figure moved, and reconcile the effort table (R3, R5 careful column) with the dealer-curve finding.

Scratch files: /tmp/determinism-check-task9-1794304326/verdict.md, /tmp/determinism-check-task9-1794304326/own_derivation.md.
