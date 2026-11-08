# determinism-check report, task4 (architecture 5), 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (errors-in-variables, regression calibration, plus cold-form selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge run: one isolated sonnet thread on a fresh unzip (target.zip f1a47765) at /tmp/determinism-check-task4-r1/target/. Its verdict is at /tmp/determinism-check-task4-r1/verdict.md. The pack is unchanged since the brief.

## Why
Executed literally (FES-2 4.1 to 4.3: -5 C design day, planning load = mean weighbridge net payload Nov 2025 to Oct 2026, limit 85 per cent of the quoted 540 kWh = 459 kWh), calibrating declared weights shipper by shipper against the weighbridge gives V02, V05, V09, V14, V16, V18 (6 tractors) on every defensible calibration. All fourteen design-day energies round to the golden's 10 kWh values. The declared-weight path orders 8, the one pooled correction 8, the one-cold-rate declared fit 10: the golden's rejected paths reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| BEV duty-days after de-duplication | 2334 | 2374 rows, 40 re-uploads, 2334; joins 1:1 to TMS | yes |
| Declared less weighed | -39 kg | -39.3 kg (20,971 CMRs, last weighing, gross less tare) | yes |
| Slopes TEN/HWP/GDR/LBY | 0.26 to 0.30 | 0.28, 0.30, 0.26, 0.28; TTV 1.00; BMJ constant 13,500 kg | yes |
| Pooled weighbridge slope | 0.94 | 0.94 | yes |
| Payload term, declared | 1.0 | 0.97 | yes (rounding) |
| Payload term, calibrated | 2.2 | 2.11 to 2.13 | form difference only, same bin and same duties |
| One-rate sub-zero under-prediction | 3.4 per cent | 3.5 per cent | yes (within 0.1) |
| Energies V02..V33 | 430,470,440,470,420,470,450,430,440,490,480,490,480,490 | 431,468,440,467,419,468,450,430,440,489,478,489,479,491 | all 14 round to golden |
| Tractors | 6 | 6 | yes |
| Declared-weight order | 8 | 8 | yes |

## Competing answers that survived
One fork, minor. A line pooled over the six pilot shippers including Tabergs (slope 0.49, payload 1.79) gives 7 (V07 at 458 against 459, 1 kWh). It mixes a slope-1.0 shipper with slope-0.28 shippers, which the per-shipper weighbridge slopes rule out, so the judge treated it as a poor method the data separates, not a licensed reading. The design note's enumerated family does not list this rival. Not a Gate C failure. One-rate calibrated model also lands the six (V03/V07/V11 at 460 to 461, thin, same side). 300 bootstrap resamples give the six in 299. Planning window shifted a month changes no duty.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 12 (6 CSV, 4 XLSX, 2 PDF) | yes |
| Categories | 2 or more | spreadsheet (CSV, XLSX) and text documents (PDF); thin, no image/code/database | yes (borderline) |
| Large CSV | 20,000 rows or more | weighbridge 21,430 data rows | yes |
| Second messy CSV | 10 to 20 printed pages or more | bev_daily_summary 2,374 rows x 15 columns (~315 KB, about 40 pages at 60 lines), also tms 3,501 rows, temperature 7,914 | yes |
| Distractors | 2 or more in metadata.json, none labelled in ZIP | fuel_card_statement and workshop_log in metadata.json; ZIP names unlabelled; quotation (468 vs 540 kWh usable) a third relevant-but-unused-for-limit file | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | judge did not name either as the surface read | yes |
| Deliverables | 1 to 3, all in golden | xlsx + pdf, both in golden.zip, exactly two files | yes |
| Asks | multi-dimensional, unit and rounding stated | 14 duties x energy, share, verdict, count; kWh to nearest 10 in the prompt | yes |
| Answer shape | gradable cells downstream of deep step | 14 energies, 14 verdicts, count, memo | yes |
| Realism | nothing LLM-looking | judge saw real-looking artifacts with incidental mess, no authoring disclosures; golden realism not independently re-read by me | yes (judge) |

## Gate G reconciliation
Thread: mechanism statistical_rigor (errors-in-variables), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, errors-in-variables with source-specific error structure, Gate G forecasting. Match. The thread does not name either declared distractor as carrying the task. The thread's caution that unreliable declarations could be read as a data defect is borderline, classed as honest measurement error, consistent with the note's "no decoy, nothing planted".

Gate H line: domain: pass; layers: pass (L1 re-uploads, mixed weight formats, duty-code rename, repeat weighings, dropouts; L2 calibrating a noisy covariate and choosing the cold form); decisive_step: analytical; chain: 4 inferences (energy model with held-out check; weighbridge shows per-shipper dilution; calibrate to expected weighed load and refit; apply to planning loads against 459); judgment: regression calibration under measurement error plus second sub-zero rate by back-test; one_fact: "the declared pilot weights are noisy proxies for the weighed load, calibrate them shipper by shipper against the weighbridge". The design note's own one-fact paragraph agrees and argues the sentence still leaves the fit, shipper heterogeneity and cold form. Reconciles with the note's chain (4 steps, same judgment).

## Stump power (Gate F)
Moderate to good. The reflex path (fit on declared weights, held-out check passes, declarations unbiased on average) lands on 8 and the pooled correction on 8, both wrong. Risk: a solver who simply regresses weighed on declared by shipper reaches the golden; errors-in-variables is a textbook method and the weighbridge is the obvious reference. The one-fact sentence exists and rescues most of the chain. The main thread should weigh this against the design note's ladder (rung 2 pooled correction 8, rung 3 per-shipper) and the stumping 1.3 caution; this is not a mismatch with the note.

## Findings, ranked
1. Pilot-six pooled line lands 7 (V07 by 1 kWh); not listed in the note's enumerated family. Optional: add it to the pinned-rival run in checks.py and a memo line rejecting it because Tabergs' slope of 1.0 differs.
2. Thin file categories (spreadsheet plus PDF only); borderline for the 2-category gate.
3. Calibrated payload term recomputes at 2.11 to 2.13 against the golden's 2.2 (form difference, no decision or bin moves); confirm the shipped 2.2 is the stated method's output.
4. No assessment date stated in the files; window choice moves no duty.

## Next action for the author
No rerun needed. Optionally add the pilot-six pooled rival to the checks.py rival table so the design note's fork list covers it, then proceed to stage 5.
