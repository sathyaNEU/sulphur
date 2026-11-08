# determinism-check report, task3 (architecture 4), pass 2, 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (wording-only FIX_NOW on the solution blocks, applied; no rerun)
**Stumping type:** mechanism: forecasting on honest data, stumping_family: outcomes not finished / two explanations for one absent response, surface_read_dependency: no, sole_data_defect: no

## Why
The re-judge rebuilt the model independently on the rebuilt target.zip: delay slope 0.129 to 0.137 years a foot (claimed 0.132), vegetable leachate about 21 mg/L against about 34 before nutrient management, the three upland clearings flat. EP-01 5.7 in 2030, 11.5 in 2031, 12.15 in 2034, Well 7 16.2: the 2027 cycle, 2031, 12 and Well 7 at 16 all reproduce, and the call holds under a two-year timing shift. Continuous arrival estimators (logistic, ramp, with or without the water-table age) all keep 2031; only a crude annual-mean crossing pushes it to 2032. The 2034 figures sit 0.32 to 0.35 inside their rounding edges.

## Findings and dispositions
1. The root-zone weighting, as stated, moves Well 7 only when the model is also carried to the wells' level: the write-up now says so (area-only mixing moves it in every build).
2. "Late in 2030" was 0.1 to 0.3 years early against other conversion-date conventions: now "around the start of 2031"; the first year at 10 is unaffected.
3. The nitrate-to-N factor (4.427) appeared in no file: the 2025 plan now states the standard as 10 mg/L as N (44.27 as nitrate).
4. The 2031 row of the forecast is a transition year: it is not a graded figure (the asks grade the first year at 10, the 2034 entry point and the highest well).

## The thread's verdict (verbatim)

# Determinism verdict, Corlinden NR-1 timing

**Verdict:** DETERMINISTIC (the call and the three Council answers reproduce from the bundle). Two small solution-narrative items need rewording, listed under Fix.

**Disposition:** APPROVE. An optional wording FIX_NOW applies to the solution blocks only; no change to the prompt or the pack, no model rerun.

## Why
The call (fund in the 2027 cycle) follows from files alone: supply plan s.4 (2027 cycle in service 1 Jan 2030, 2031 cycle 1 Jan 2034, plant must be in service before the first year EP-01's annual flow-weighted mean reaches 10 mg/L as N), Table 1 shares for 2027 to 2040, and the prompt's 2026 land-cover hold. I rebuilt the depth-dependent unsaturated delay from the 14 matured conversions, the leachate by land-surface year, and the parcel-by-parcel mixing. EP-01 first reaches 10 in 2031, is 12.15 mg/L in 2034, and Well 7 is highest at 16.2. Every rival I could construct either lands on the same call or is excluded by named data (the three upland clearings that show no rise).

## Evidence: recomputation ledger
| Figure | Claimed | My value | Reproduced | Source / field |
|---|---|---|---|---|
| Raw record: EP-01 2012 / 2025 | 6.2 / 5.3 | 6.16 / 5.31 | yes | raw_water_nitrate csv: result, NO3 / 4.427, 2014 HR-W0x names mapped, duplicates averaged |
| Well 6 / Well 7, 2010 to 2026 | 7.0, 5.5 to 5.5, 4.4 | 7.00, 5.52 to 5.47, 4.37 | yes | same |
| Matured conversions (irrigated, 1990 to 2008) | 14 | 14 (TCGW-010, 014, 024, 026, 034, 051, 055, 056, 062, 064, 068, 070, 072, 085) | yes | land_cover csv (codes mapped, parent_parcel_id joined) + sites xlsx |
| Delay slope b (yr/ft) | 0.132, resid 0.3 | 0.135 (logistic), 0.1347 (ramp), 0.129 (origin); resid 0.31 to 0.35 | yes (estimator spread 0.129 to 0.137) | network_samples nitrate_result vs sample_date, depth_to_water, age_survey apparent_age_yr |
| Mean delay | 4.7 yr | 4.74 | yes | same |
| Water-table ages | under 0.5 yr | 0.1 to 0.6 | yes | age_survey; note only 7 of the 14 conversion wells have an age row |
| Vegetable leachate latest / earlier | 20.9 / about 34 | 21.1 / 32 to 36 (step at land-surface year about 2000) | yes | network wells on unchanged land, sample date less age less delay |
| Corn and soybean leachate | 13.2 | 13.3 to 13.8 | yes | same |
| Ridge parcels | 1,099 ac, 57 to 94 ft, 1 to 3 yr | 1,099; 57 to 94; 1.4 to 2.6 | yes | WHPA parcel attributes + land cover (10 parcels cleared 2017 to 2021) |
| Ridge arrival at wells | "late in 2030" | 2031.0 to 2031.3 (b 0.132, a 0); 2030.8 to 2031.3 over b 0.129 to 0.137 | partly (about 0.1 to 0.3 yr later than the golden's wording) | land cover year + (a+b x depth) + gw_time_of_travel_yr |
| EP-01 annual mean 2030 | about 6 | 5.7 | yes | blend by plan shares |
| EP-01 annual mean 2031 | above 10 | 11.5 (11.3 with the 2019 to 2026 offset) | yes | same |
| First year at or above 10 | 2031 | 2031 | yes | same |
| EP-01 2034 | 12 | 12.15 (11.96 with offset) | yes | same |
| Well 7 2034 | 16 (highest) | 16.18 (16.04 with offset); Well 6 is 14.99 | yes | same |
| Obs vs model 2019 to 2026, wells | -0.31 to 0.01 | Well 3 +0.06, Well 5 -0.25, Well 6 -0.20, Well 7 -0.14 (my model less offset) | yes (same range) | raw_water results |
| Upland clearings TCGW-012, 053, 076 (69 / 90 / 79 ft; 2020 / 2017 / 2018) | no rise yet | flat at 0.5 to 0.6 through 2026; fit predicts arrival 2028 to 2029 | yes | network_samples |

## Competing answers stress-tested
- Trend or any record-fitted model (never reaches 10, 2031 cycle). Excluded: the matured conversions show a depth-dependent delay and the ridge's land cover is filed, so absence in 2019 to 2026 is the leachate not yet arrived. The three upland clearings confirm it.
- Travel time alone, or one 4.5-year lag. Both put the ridge at the wells by about 2022 to 2026, and both predict a rise at the three upland clearings that is not in the data. Excluded.
- Timing convention. The call survives anything: even a 2 year shift leaves the first year at or below 2033, so the 2027 cycle holds. The first-year figure moves only if ridge arrival moves later by more than about 0.25 yr (shift 0.3 gives EP 2031 = 9.6, first year 2032). Continuous estimators of the half-way arrival (logistic, ramp, with or without age subtraction) all stay inside this; only a crude annual-mean crossing estimator (crossing year + 0.5, a = +0.28) would shift to 2032.
- Acre-only mixing (ignoring the Recharge sheet) gives Well 7 = 15.1 and EP 2034 = 11.0, so the 2034 EP-01 and Well 7 figures differ (11 / 15 vs 12 / 16). The Recharge sheet (WHPP Table 1, and the "Recharge" sheet of the parcel workbook) is in the pack and the zone is defined as the land whose recharge reaches the well, so this is a method error, not an equal reading.
- Recharge keyed to land-surface time vs water-table time: I get identical 2034 values (16.18); the golden's remark that the root-zone variant gives Well 7 = 15 does not reproduce in my build (see Fix).

## Margins to rounding or threshold edges
- EP 2031 vs 10: 1.3 to 1.5 mg/L above (about 0.25 yr of arrival; regression se at 80 ft is about 0.19 yr, so this is about 1.3 sigma). Thin but clean: reasonable estimators all land inside.
- EP 2034 12.15 (edges 11.5 / 12.5): 0.35 from the upper edge. Well 7 16.18 (edges 15.5 / 16.5): 0.32 from the upper edge; neither moves with the offset or the 20.9 vs 21.0 leachate.
- Highest well: Well 7 beats Well 6 by 1.2.

## Files / Hygiene
PASS. 13 files, 4 formats (csv 5, xlsx 4, pdf 3, png 1). Real-looking utility and county provenance in docProps, no authoring leakage. Mess is texture: NO3 vs N units and lab change in 2004, 2014 point renaming, duplicates and re-runs, gal / kgal mix and out-of-service flags in the daily pumping csv, rebuilt wells, split parcels with parent ids. Distractors (fertilizer sales, specific capacity, construction records, pumping) are unlabelled. Minor: the NO3 to N factor 4.427 is not stated in any file (standard chemistry; the overlap of the two labs is not available, so it is the only outside fact). The 2019 age survey covers only 7 of the 14 conversion wells, so the other seven rely on the age being small. Neither moves a graded figure. No exclusion-level finding; no public-data contamination.

## Stump power
High. A competent analyst who cleans every file and reads every field will fit the wells' record or a trend, see Wells 6 and 7 falling, and say the 2031 cycle (EP-01 about 5). Even the strongest-looking rival (the wellhead model's travel time, or one fitted lag) predicts a rise by 2026 that the record does not show, so a run that goes that far still loses unless it builds the depth-specific delay. Reaching 2031 needs: land cover history to ridge clearing, delay vs depth from the matured conversions, leachate by land-surface year, and parcel mixing.

## Stumping type
mechanism: forecasting; stumping_family: analytical_non_defect; surface_read_dependency: no (the wells' record is correct, it simply does not pin the forward projection); sole_data_defect: no (on clean data the delay structure still has to be estimated). Passes Gate G.

## Deep reasoning
domain: pass | layers: pass (Layer 1: unit and lab change, renames, split parcels, rebuilt wells; Layer 2: unsaturated-zone transport lag identified from conversions and carried to deeper parcels) | decisive_step: analytical | chain: 5 inferences (conversion step times, delay vs depth fit, leachate by land-surface year, per-parcel arrival, recharge-weighted mixing and blend), judgment: model selection of the lag (depth-specific vs travel time vs one lag) tested against the upland clearings, plus extrapolation from the fit | one_fact: "the unsaturated delay grows with depth to water, about 0.13 yr per ft" would shorten the path, but the solver would still have to measure it, fit it and carry it through the parcel mixing, so it is not a one-line rescue.
The easy route is a trend or record-fitted model giving about 5 mg/L in 2034 and the 2031 cycle.

## Fix
Where: solution (wording only). None to the prompt or the pack.
1. The "recharge at the time the nitrate left the root zone puts Well 7 at 15" sentence does not reproduce; the acre-only mixing does (15.1). Reword so the 15 is attributed to acre-only mixing, or drop the root-zone variant.
2. Ridge arrival is described as "late in 2030"; my reconstruction puts it at 2031.0 to 2031.3 with 2031 still above 10. Either soften to "about the turn of 2030 to 2031" or keep, as the 2031 answer is unaffected.
3. Optional: the xlsx forecast row for 2031 is a transition year (11.3 to 11.5 in my builds) and depends on arrival timing to about 1 mg/L; the rubric should grade 2031 only as at or above 10, not a point value.
