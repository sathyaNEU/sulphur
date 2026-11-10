# determinism-check report, task7, 2026-11-09

## Verdict
DETERMINISTIC

**Disposition:** APPROVE (judge thread's call), with one open risk flagged below that the author should close before shipping: the one-fact test may be undercounted in the design note.

**Stumping type:** mechanism: method_or_model_selection (with causal-reasoning and decomposition/forecasting layers); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.

## Why

The judge thread independently recomputed every load-bearing figure it could reach without fitting the generator's own curves, and all of them reproduced: the pilot's structure (3,040/1,368/1,330), the applications dedup (858 rows → exactly 829 buildings, €4,959,800 grant, matching ask 8 to the cent), five sampled reference-consumption figures (exact), the per-measure lifetime tonnes and grant/tonne (within rounding of 108.74/196.03/104.40), and the flip-rate arithmetic. It confirmed the two deciding covariates (empty-week share for controls, roof-per-floor for insulation) are genuine, continuous, population-wide distributions across all ~24,000 buildings and ~24,000 customers, not an effect confined to the applicant pool, which is the key Gate G/H evidence that this is covariate-adjustment/model-selection under covariate shift rather than a planted or shallow hidden factor. It did not re-derive the controls sigmoid fit, the insulation log-linear fit, the bootstrap 90% ranges, the heating-optimisation fade-decay curve or the round-close withdrawal/lateness model; those were assessed only for internal consistency, not independently rebuilt from raw rows.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot answers/drawn/completed | 3,040 / 1,368 / 1,330 | 3,040 / 1,368 / 1,330 | Yes, exact |
| Applications after revision-replaces-earlier dedup | 829 rows, €4,959,800 | 858 raw rows → 829 unique buildings, €4,959,800 | Yes, exact |
| Reference consumption (5 sampled applications) | per-application | recomputed from 2025/26 "round 2026" notice row × heated_floor_area_m2 | Yes, exact on all 5 |
| Lifetime tonnes by measure | 26,835 / 4,292 / 11,498 (total 42,625) | ≈26,826 / ≈4,293 / ≈11,490 (total 42,625 stated) | Within rounding |
| Grant per tonne | €108.74 / €196.03 / €104.40 | reproduced to the cent from grant÷tonnes | Yes |
| Flip-rate thresholds | 20.34% / 3.18% / 7.44% | reproduces mechanically from rate×(grant/tonne)/120 | Yes, self-consistent |
| Empty-week share distribution (controls driver) | "70.50% vs 41.99%" | measured across all ~24,000 customers in electricity_load_profiles_2025.csv: continuous, p10 0.43–p90 0.76, not confined to applicants | Consistent, broad |
| Roof-per-floor distribution (insulation driver) | "1.13 vs 0.79" | measured across all ~24,000 buildings joining the cadastre to the register: continuous, p10 0.25–p90 1.17 | Consistent, broad |
| Controls/insulation band fits, bootstrap ranges, fade-decay curve, round-close withdrawal model | various | **not independently re-derived**; assessed for internal consistency only | Not verified numerically |

## Competing answers that survived

None. The judge enumerated the two alternate pricings the submission itself names (each use's own saving: €132.06/€128.67; the pilot's own mix: €140.94/€195.06) and found no basis in the files to prefer either over the covariate-indexed pricing, since the covariates are genuine population-wide variables and the files pin the WHAT (0.201 t/MWh, service lives, the €120 rule, the revision-replaces rule, which notice row is reference consumption) while leaving only the HOW open with a stated, checkable band. No fork survived open on the main call or on any supplementary ask.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 19 (no system files) | Pass |
| File categories | 2 or more | spreadsheet (xlsx x4), text/csv (csv x8), document (pdf x6, docx x1) — 3 categories | Pass |
| Large messy CSV ≥20,000 rows | 1 or more | gas_meter_reads_2013_2026.csv, 389,105 rows | Pass |
| Messy CSV 10-20+ printed pages | 1 or more | benchmarking_notices_2019_2026.csv, 37,214 rows (also electricity_load_profiles_2025.csv, 178,514 rows) | Pass |
| metadata.json names 2+ distractors, unlabelled in ZIP | required | 3 named (electricity_customers_annual_2019_2025.csv, municipal_heat_plan_2026_summary.pdf, federal_funding_overview_2025.pdf); nothing inside target.zip labels them | Pass |
| Each distractor relevant-but-unused; one reproduces a graded quantity arithmetically and is ruled out by a shipped fact | required | all 3 are domain-relevant and unused by the solution steps; none of the three actually reproduces a graded quantity by itself (electricity_customers_annual is annual-only, not an alternate route to the empty-week share; the two PDFs state unrelated federal/zoning programmes with no numbers that land near a graded figure) | Partial — distractors are relevant and unused but none is a near-miss arithmetic trap |
| 1-3 deliverables, all present in golden, no format family forced | required | 2 requested (note.docx, appraisal.xlsx), both present in golden.zip exactly | Pass |
| Asks multi-dimensional, unit+rounding stated | required | asks are genuinely multi-dimensional (multi-season, multi-measure, ranges); prompt.txt states no rounding convention anywhere (confirmed independently and already flagged by leak_check_report.md item 11: "no rounding words anywhere; every derived figure needs one") | Fail (minor, prompt-level) |
| Answer is one of the 14 shapes, 4+ checkable results | required | "scenarios with the flip point... with the round's settled grant beside it" (DESIGN_NOTE Draw section); 10 results (R1-R10) in the results chain, more than 4 | Pass |
| Golden ZIP holds exactly what prompt requests, requested formats | required | golden.zip: grant_round_2026_appraisal.xlsx, grant_round_2026_note.docx — exactly the two requested files | Pass |
| Nothing LLM-generated, goldens read as real work product | required | judge found PDFs/docx read as genuine municipal/utility documents (named officials, dates, realistic structure); no tells observed in its sample | Pass (per judge's sampling; not separately re-verified by me) |

## Gate G reconciliation

The judge's classification (`mechanism: method_or_model_selection`, `surface_read_dependency: no`, `sole_data_defect: no`) matches the design note's own account: the note's "Strategy label" is population selection on unrecorded properties (a randomised effect carried to units that chose their treatment on properties the trial's outcome records do not carry), which is squarely a method/model-selection-under-covariate-shift shape, not a flip away from a misleading reported number. The note explicitly states "No decoy: no memo, draft, stakeholder figure or copied block; no shipped file states a saving, a rate, a grant per tonne or a recommendation" and "Not rule application: no filed procedure performs a result" — both consistent with the judge's independent finding that the two covariates (empty-week share, roof-per-floor) are continuous and population-wide rather than planted in the deciding units. No conflict on Gate G.

## Gate H reconciliation

| Item | Design note | Judge thread | Match |
|---|---|---|---|
| one_thing | "Not one thing": the two drivers (R3, R4) are the strongest single pieces but a run told either still has to measure it, fit it, price every application and carry the fade, and still files the *other* measure's call wrong | one_thing: none; covariate-banding is load-bearing across several results but genuine and population-wide, not a constructed artifact | Match |
| Effort grades | quick 0.5/13 (~4%), careful 6/13 (~46%), thorough 13/13 | quick ~1-2/8 (~12-25%), careful ~4-5/8 (~50-62%), thorough 8/8 | Roughly consistent in shape (quick low, careful ~half, thorough full); the thread's coarser 8-result grouping inflates the quick-pass share somewhat but not past a third |
| Results/areas | 10 results (R1-R10) across causal reasoning, forecasting, missingness-measurement, modeling, synthesis, uncertainty | 8 results across ≥5 areas | Consistent after re-grouping |
| Largest single hint / one-fact test | Tests each driver sentence **separately**: the empty-week sentence alone rescues R3 and R5c (2 of 13); the roof sentence alone rescues R4 and R5a (2 of 13); explicitly states "the call and the funded round's totals need both" | Tests a **combined** sentence naming both drivers at once ("this year's applicant pool sits on a different point of the same empty-week/roof-per-floor curve the pilot sample does, so price each application off that curve, not off a flat or use-type average") and estimates it rescues 3-4 of 8 (~40-50%), reaching into R5a, R5c, R6, and downstream R7/R8b for insulation and controls | **Mismatch, flagged below** |

**The one finding worth the author's attention.** The design note's one-fact test is built from two single-driver sentences and concludes neither alone clears more than 2 of 13 results (about 15%), supporting H5. The judge thread, working independently from the shipped files with no knowledge of the note, converged on a single *combined* sentence that states the general mechanism for both drivers at once without being told either curve's shape or thresholds, and estimated it rescues 3-4 of 8 graded results (about 40-50%) by its own coarser grouping, i.e. clearing the "about a third" ceiling the client's H5 rule sets, even though it still leaves the quantitative curve-fitting, bootstrap ranges, fade-decay and round-close work undone. This is exactly the reconciliation pattern the contract calls out: "the thread's best single sentence rescues more results than the note's `Largest single hint:` says." It does not by itself overturn the DETERMINISTIC verdict (Gates A-E are unaffected and nothing here is a planted or shallow factor), but it is a legitimate open question on whether the note's H5 test should be re-run with a combined-driver sentence before the task is treated as cleared on Gate H, since a reviewer under the 2026-11-09 bar is likely to construct the same combined sentence the judge did.

## Stump power (Gate F)

The judge's assessment: the task stacks several real moves (an RCT-vs-naive comparison the critical components say would otherwise book the pandemic/price-shock/burner-check noise as savings; the heating-optimisation fade recognition; the covariate-shift pricing for controls/insulation; the round-close withdrawal/lateness projection), and the likeliest loss for a careful-but-hurried run is reporting a cruder per-measure saving rate (its own use's average, or the pilot's pooled mix) that puts insulation and/or controls over €120/tonne, flipping the fund/no-fund call on exactly those two measures and the round totals with it. The judge flagged, but did not resolve to its own satisfaction, whether the combined-driver insight is easier to state as "the single lesson" than the note's test credits (see Gate H reconciliation above); that is the one place this review would benefit from a second, skeptical look if the design intent differs from what the shipped files show.

## Findings, ranked

1. **(Gate H, open question, not disqualifying on its own)** The design note's one-fact test undercounts the task's vulnerability to a single combined-driver sentence; the note tests each driver's hint separately (2/13 each) but a natural single sentence spanning both drivers rescues materially more (the judge's own estimate: 3-4/8, roughly 40-50%). Recommend the author re-run the one-fact test in `.claude/skills/stumping` with a combined-driver sentence and confirm the rescued share stays at or under about a third before relying on the current H5 pass.
2. **(Prompt hygiene, minor, already caught by leak_check_report.md item 11)** `prompt.txt` states no rounding convention anywhere; every derived figure (€, %, tonnes) needs one stated once at the end per house style. This is a prompt-polish item, not a determinism defect: the submission's own figures are internally consistent on precision, so no committed answer is actually ambiguous because of it.
3. **(Spec gate, minor)** None of the three declared distractors is a near-miss arithmetic trap that reproduces a graded quantity before being ruled out by a shipped fact; they are relevant-but-inert rather than relevant-and-tempting. Not disqualifying (the gate only requires relevance and non-use as a floor), but a lever available if the author wants to add stump power later.
4. No Gate A-E failure found by either the judge's independent recomputation or my own spec-gate pass; no competing answer survives; no missing decisive fact; no semantic fork; no surface-read-rejection.

## Next action for the author

Before treating Gate H as settled, re-run the design note's one-fact test with a single sentence that names both drivers at once (not each driver separately) and record how many of the 13 results it actually rescues; if it clears materially more than a third, either split the sentence's power across more independently-gated results or accept the task as "thinner" (per H4's carve-out) rather than claiming the current H5 margin.
