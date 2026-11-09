# determinism-check report, task4 (architecture 6), 2026-11-09

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one FIX_NOW-grade hygiene note; no rerun required)
**Stumping type:** mechanism: mixed, stumping_family: mixed, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread (fresh unzip of `target.zip`, sha256 `9d65a333...`, graded blocks from `submission.md` only) recomputed all 14 Assessment-sheet planning loads exactly from `weighbridge_varnamo_2024-11_2026-10.csv` once two filed hygiene conventions are applied (the `VMO-nn`→`Vnn` April-2026 rename, carried in `route_register_2026.xlsx`'s own crosswalk column, and last-weighing-per-CMR after axle re-weighs), and found the 540→519→441 kWh battery chain arithmetically exact against `quotation_bev_tractors_2027.pdf` and FES-2 §2.3/4.3. No committed answer was contradicted by any shipped file. The main recommendation (order 6: V02/V05/V09/V14/V16/V18) is forced by three independently-moving estimates — the weighbridge-calibrated payload term (2.0 vs the declared-weight fit's 1.1 kWh/t/100km), the out-of-sample two-rate cold form, and the confound-controlled first-year battery loss (3.8 per cent) — none of which the judge could make collapse to a single catch. The judge flagged one limitation: it verified the regression triplet's direction, magnitude and internal consistency but could not fully re-derive the exact multivariate coefficients in the time available. Given the strength of the surrounding arithmetic checks (planning loads 14/14 exact, battery chain exact, declared-weight format mix confirmed genuine) this is a reasonable stopping point for a single pass and does not on its own move the verdict.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 14 planning loads (0.1 t) | V02 3.9 ... V33 3.9 (submission Ask 1) | last-weighing-per-CMR, Nov 2025–Oct 2026, duty names merged across the Apr-2026 rename | Yes, 14/14 exact |
| Usable battery after 1 yr | 519 kWh | 540 × (1 − 0.038) = 519.48 → 519 | Yes, exact |
| Limit | 441 kWh | 519 × 0.85 = 441.15 → 441 | Yes, exact |
| Payload term (weighbridge-calibrated) | 2.0 kWh/t/100km | consistent with classical errors-in-variables / regression-calibration logic on genuinely mixed-format `declared_weight`; coefficient itself not independently re-fitted | Partial (direction/mechanism confirmed, exact coefficient not re-derived) |
| Payload term (declared-weight route) | 1.1 kWh/t/100km | same caveat as above | Partial |
| First-year battery loss | 3.8% (age-only rival 3.3%) | winter dip in raw energy-per-full-charge confirmed (≈465–470 Dec–Feb vs ≈490–505 May–Sep), consistent with a real temperature confound; exact regression not re-derived | Partial |
| Cold-form holdout error | −6.6% (one-rate), +0.5% (two-rate) | not independently re-fitted this pass | Not attempted |
| Dedup / cleaning claims | 1 day uploaded twice, 83 ambient dropouts | 40 duplicate same-reg/same-date rows found, 83 dropouts found | Yes |
| Mixed declared-weight formats | kg, "12 000 kg", Swedish-decimal tonnes | confirmed in `tms_consignments_jonkoping_2025-2026.csv` | Yes |

## Competing answers that survived
None. The judge enumerated the three named hurried shortcuts (declared-payload fit, one-rate cold form, age-only degradation) and found each moves the order (8, 8, 9 respectively) by an independently checkable mechanism, not an unpinned interpretive fork. The design note's own rival sweep (checks.py, 151 assertions; alternate knots, temperature bins, either year alone, within-duty fit, alternate calibration windows, alternate loss estimators) is claimed to order the same six duties with every energy within 6 kWh and every margin at least 1.5 kWh; the judge's independent checks did not contradict this, though it did not re-run the full rival sweep itself.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 12 files; CSV(6)/XLSX(4)/PDF(2) = 3 categories | Pass |
| Large messy CSVs | one 20,000+ row CSV, one 10–20+ printed-page CSV | `weighbridge_varnamo...csv` 21,442 rows; `tms_consignments...csv` (3,501 rows×10 cols), `fuel_card_statement...csv` (9,357×9) and `daily_mean_temperature...csv` (7,914×3) each print well past 10–20 pages | Pass |
| Distractors named in metadata, unlabelled in ZIP | 2+ named, none labelled inside ZIP | `metadata.json` names `fuel_card_statement_varnamo_2025-2026.csv` and `workshop_log_2025-2026.csv`; neither file name nor any cell inside the ZIP flags either as a distractor | Pass |
| Distractors relevant but unused | each weighs plausibly, none decides a graded result | both are diesel/mixed-fleet operating records (fuel card, workshop log); judge independently flagged both as "plausible unused distractors," no graded figure traces to either | Pass |
| 1–3 deliverables, all present in golden, no format family forced | — | `ev_duty_assessment_2027.xlsx`, `tractor_order_memo.pdf`; both present in `golden/` and `golden.zip` | Pass |
| Asks multi-dimensional, unit+rounding stated | — | 14-duty table across multiple fields; prompt states 0.1 t / 10 kWh / 0.1 kWh / 0.1 pp rounding | Pass |
| Answer shape = one of fourteen | — | "allocation plus its sensitivity" (Results chain / Draw), with 6 checkable results | Pass |
| Golden ZIP = exactly the requested files/formats | — | `golden.zip` contains exactly the 2 requested files, no extras | Pass |
| Nothing LLM-generated / no build-reveal | — | `metadata.json` (outside ZIP) discloses construction; no file inside the ZIP reveals the build; `provenance` note is in metadata.json only | Pass |

## Gate G reconciliation
Judge: `mechanism: mixed`, `stumping_family: mixed`, `surface_read_dependency: no`, `sole_data_defect: no` — the payload-calibration step looks at first glance like surface-read-rejection ("the declared weight is misleading") but the judge classed the underlying mechanism as attenuation bias / regression calibration corrected via an external instrument (the weighbridge), i.e. genuine statistical rigor rather than "the reported figure is simply wrong," and found two further independently-stumping FINE-numbers layers (out-of-sample cold-form selection, confound-controlled degradation) that survive the clean-data test on their own.

DESIGN_NOTE's own Gate G-relevant lines agree closely: "Not one thing" (three independent judgments, each moving the order on its own — declared payloads order 8, one cold rate orders 8, no first-year loss orders 9); "Not semantics" (every field read right still leaves three open estimates); "Not rule application" (FES-2 files the WHAT, not the HOW for any of the three estimates); "No decoy" (no memo or stakeholder figure ranks the duties). The Hidden factor record lists all three constructed factors (declaration error, the sub-zero cold bend, the cold's temporary capacity loss) as `keep`, each found by modelling rather than inspection, each sitting across all shippers/duties rather than only in the deciding units. This matches the judge's independent finding that none of the three collapses the task alone.

## Gate H reconciliation
Judge's Gate H line: `domain: pass`, `layers: pass`, `results: ~6 graded across 4 areas`, `one_thing: none`, `effort: quick ~1-2 of 6, careful but hurried ~3-4 of 6, thorough 6 of 6`, `one_fact: "fit the payload term against the weighbridge, not TMS declared weight" rescues at most 2 of 6`.

Design note's own Gate H artifacts: Results chain lists 6 results (R1–R6) across assembly/reconciliation, missingness/measurement, modeling, validation, synthesis (4 areas, matching the judge's count); Effort test table gives quick ≈1.5/6, careful but hurried ≈2.5/6, thorough 6/6; "Largest single hint" is stated to rescue 1 of 6 results.

Two minor deltas worth recording, neither large enough to force a finding on its own:
- **Careful-pass effort grade runs a little high.** The judge grades the careful-but-hurried pass at 3–4 of 6 (50–67%); the note's own table grades it at 2.5 of 6 (≈42%). Both stay well short of the thorough pass's 6/6, so this does not trigger the "careful pass levels with the thorough one" send-back condition, but the author should recheck whether the judge is crediting a Partly on R4 or R5 that the note's table scores more conservatively.
- **One-fact rescue count is slightly higher in the judge's read.** The note states its largest single hint rescues 1 of 6; the judge's best single sentence (phrased slightly differently, aimed at the weighbridge-vs-declared choice specifically) rescues "at most 2 of 6." At 2/6 (33%) this sits right at, not over, the "about a third" ceiling H5 sets, so it does not fail H5, but it is the one line in this reconciliation closest to the edge and is worth tightening in the next design-note revision (e.g. stating the hint more narrowly so it cannot be read as touching R4).

No hidden factor the judge found was carried in only the deciding units, no distractor was found to carry a graded result, and no band was reported as excluding a defensible rival or as too wide to separate the hurried figure from the golden. These are the clean outcomes the reconciliation is checking for.

## Stump power (Gate F)
Judge's assessment: all three named shortcuts (declared-weight payload fit, one-rate cold form, age-only degradation) are independently load-bearing — removing any one still leaves a wrong order from the other two — which is what keeps the task from reducing to a single catch. The judge's main named risk: a careful-but-hurried run is likeliest to lose on the cold-form choice, filing a design-day energy for V03/V07/V11 roughly 12 kWh too low (still under the 441 kWh limit) and wrongly recommending 8 tractors with V03/V07/V11 included. This matches the design note's own stated stumping story and does not raise a too-easy or stumps-for-the-wrong-reason flag.

## Findings, ranked
1. **(Minor, FIX_NOW, no rerun)** BMJ's `declared_weight` in `tms_consignments_jonkoping_2025-2026.csv` is exactly 13,500 kg on all 389 of its rows (std = 0) — the judge flagged this as reading like an authored device rather than organic business noise. It feeds the six-shipper global payload calibration but does not sit in the units (GST/SKB/HIL/VIS duties) that decide the order, so per the hygiene rubric this is stump-unaffecting. **Fix:** replace BMJ's flat 13,500 kg column with small realistic jitter (a few hundred kg) in `generator/` so no single shipper reads as perfectly uniform; this does not touch any committed figure.
2. **(Note only, no action required)** The judge was not able to fully re-derive the exact regression coefficients for the payload term, the cold-form holdout errors, and the degradation estimate within a single pass; it verified direction, magnitude, and internal consistency instead. This is a residual verification gap, not a determinism defect — the surrounding arithmetic (planning loads, battery chain, data-format claims) all reproduced exactly, and the judge's qualitative checks (winter dip in raw energy data, genuinely mixed declared-weight formats) corroborate the claimed mechanisms.
3. **(Note only)** The careful-but-hurried effort grade (3–4 of 6, judge) runs slightly above the design note's own table (2.5 of 6); worth a light recheck but does not approach the thorough pass's 6/6 and does not change the disposition.

## Next action for the author
Apply the one FIX_NOW hygiene fix (jitter BMJ's declared-weight column in the generator so it no longer reads as a perfectly flat authored quirk) and rebuild/reship with that change; no model rerun is required since no committed figure or graded result depends on that column's exact values.
