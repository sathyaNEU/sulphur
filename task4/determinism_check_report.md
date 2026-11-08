# determinism-check report, task4, 2026-11-08

## Verdict
DETERMINISTIC (no SOLUTION_WRONG on any graded figure; one solution-block imprecision, Critical Component 1)
**Disposition:** APPROVE (optional touch-up of Critical Component 1, no rerun, no FIX_NOW item)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, scratch /tmp/determinism-check-task4-043108 (verdict.md there). The runtime had no Agent tool, so the main session spawned the thread from judge_brief.md.

## Why
NPS-3 4.1/4.3 (saving = all-in van-hours taken off the runs less Owenduff's charges, set chosen to lower the year's cost most), the offer ("any combination", EUR 12.60 a parcel), the rate card (EUR 58.00), calendar, plan and stop log force one set: Mulranny, Achill, Bangor Erris, Belmullet, Louisburgh, Ballycastle. Rivals land elsewhere: cost-to-serve adds Leenane and Letterfrack (EUR 20,000), one-at-a-time pricing drops Mulranny and Bangor Erris (EUR 34-35k), proportional carry keeps the list at EUR 55,000. Net saving rounds to EUR 50,000 under every defensible fit tried.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2027 hours as they stand R03..R09 | 1300/1550/1700/1200/1600/1550/1600 | 1291/1551/1698/1201/1601/1552/1609 | yes |
| Saved R03/R04/R07/R08 | 300/650/600/200 | 300/648/592/208 | yes after rounding |
| R05, R06, R09 saved | 0 | no combination pays | yes |
| Net saving | EUR 50,000 | 49,459 (49.4k-50.9k across fits) | yes |
| Mulranny alone / Bangor Erris alone | 80 / 70 h | 81 / 70 h | yes |
| Charges Mulranny / Bangor / Leenane+Letterfrack | 7,800 / 6,300 / 12,200 | 7,812 / 6,300 / 12,222 | yes |
| One-at-a-time list | EUR 35,000 | 34.0k | yes |
| Proportional carry | EUR 55,000 | 54.6k-56.8k | yes |
| Leenane+Letterfrack hours (CC1) | 110 h, EUR 6,300; run EUR 50,800 | about 118-124 h, about EUR 6.9-7.2k, run about 51.9k | no, 7-12 percent high; decision unchanged |

## Competing answers that survived
None on the call. Two thin edges, neither a fork on the call: (1) NPS-3 4.3 read as a set versus district by district; "most" and "any combination" force the set, but it is the one place a literal reader could split. (2) Rounding to 50: R04 saved 648 (boundary 675; a 2026-only fit gives 680, rounds to 700) and R07 592 (17 h above the 575 boundary); the pooled two-year fit stated in the solution is stable.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 11 | yes |
| File categories | 2 or more | spreadsheet (4 xlsx), text (5 csv, 2 pdf) | yes |
| Large messy CSVs | 20,000 rows plus a 10-20 page CSV | stops 106,641 rows (11 MB); van run log 4,160 rows (358 KB, far over 20 printed pages) | yes |
| Distractors | 2 or more in metadata.json, none labelled in ZIP | 3 (fuel card, customer contacts, fleet register); no label in ZIP; judge saw none; fleet lease ends unused by NPS-3 4.2 | yes |
| Deliverables | 1 to 3, all in golden | 2; golden.zip holds exactly district_handover_2027.xlsx and handover_2027.png | yes |
| Asks multi-dimensional, unit and rounding stated | yes | seven run-level cells plus net; nearest 50 and EUR 5,000 stated | yes |
| Answer shape | gradable cells downstream of deep step | per-run hours table and paired bars, all downstream of the run model and 2027 forecast | yes |
| No build-revealing files, nothing LLM-looking | yes | judge saw no authoring or benchmark language; dates coherent. I did not open the golden xlsx or png for realism (golden-realism covers it) | yes (judge-based) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note declares the same shape (analyst test: cost-to-serve gives about EUR 20,000 with Leenane and Letterfrack; deep step is the run model, set pricing and 2027 reach forecast; strategy label WORKS IN FORM). The declared distractors (fuel card, contacts, fleet register) were not the surface read; the thread named the cost-to-serve build as the lure. Match, no mismatch finding.

Gate H line: domain: pass, layers: pass, decisive_step: analytical, chain: 4 inferences (clean and order the stop log, fit the run model by least squares, price sets not districts, forecast 2027 reach days with Poisson check), one_fact: none rescues the whole (closest, "price each run with and without each combination", settles the list but not the 2027 hours or the net).

## Stump power (Gate F)
Good on paper but with one soft spot, for the main thread to weigh against the ladder. NPS-3 4.1 already says "van-hours the hand-over takes off the runs", so a solver that prices each run with and without each combination reaches the list directly; the forecast step then separates exact hours and the net. The set-versus-single and drive-through steps are the field's own reasoning but the filed wording partly names the step ("anything written down is executed"). The wrong paths each lose several graded cells (EUR 20,000, EUR 35,000, EUR 55,000), and the asks make a run on any of them lose many cells. Sets and combination pricing being textbook make-or-buy moves puts the call within reach of a strong solver; platform runs are the measurement.

## Findings, ranked
1. Critical Component 1 (110 h, EUR 6,300, run EUR 50,800) does not reproduce exactly (about 118-124 h, about EUR 6.9-7.2k). Decision unchanged (charges EUR 12.2k). Not a FIX_NOW; optionally re-emit from the generator or word as "about".
2. R04 and R07 saved hours sit close to 50-hour rounding boundaries on single-year fits; stable on the pooled fit.
3. Set reading of NPS-3 4.3 is forced by wording but is the single literal split point.
4. NPS-3 4.1 wording hands over part of the method (stump-power note above).

## Next action for the author
Optionally restate Critical Component 1 as "about 120 van-hours" or re-emit it from the generator's model, then proceed; no rebuild or re-judge needed.
