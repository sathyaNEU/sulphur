# determinism-check report, task3 (architecture 4), 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (optional per the thread; APPROVE defensible)
**Stumping type:** mechanism: forecasting with a depth-specific delay read from matured conversions, stumping_family: outcomes not finished / two explanations for one absent response, surface_read_dependency: no, sole_data_defect: no

## Why
The thread executed the prompt and the plan literally (EP-01's annual flow-weighted mean, the plan's shares, land cover held at 2026, in service before the first year at 10) and reconstructed the forecast from the bundle: delay slope 0.133 years a foot (residual 0.28), vegetable leachate 20.5 to 20.9 mg/L, the ridge at the wells 2030.6 to 2031.5, EP-01 first at 10 in 2031, 11.87 in 2034, Well 7 highest at 15.76. The 2027 cycle is forced; the short-lag rivals predict a rise visible by 2026 that the record rejects; the three upland clearings are flat, as the depth delay says.

## Recomputation ledger
See the thread's verdict below (every figure reproduced; ask 6 and ask 8 thin).

## Competing answers that survived
None on the call. Two thin asks: the first year at 10 (a delay a third of a year later moved it to 2032) and Well 7's 2034 mean (0.26 above the rounding line; 15.28 at a vegetable leachate of 20.0 in the thread's model).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| usable files | 10 or more | 13 | yes |
| categories | 2 or more | spreadsheet, text (pdf), image | yes |
| CSV of 20,000+ rows | 1 | pumping, 26,080 rows | yes |
| CSV of 10-20 pages or more | 1 | network samples, 5,000+ rows; land cover 5,700 rows | yes |
| distractors | 2 or more, unlabelled | 3 in metadata.json | yes |
| deliverables | 1 to 3, all in golden | 3 of 3 | yes |
| golden ZIP exactly the requested files | yes | yes | yes |

## Gate G reconciliation
The thread's type (forecasting on honest data, stump power strong, no single sentence rescues a run) matches the card (decomposition_attribution, maturity_censoring, analytical) and the design note's deep step. The thread named no distractor as load-bearing.

## Stump power (Gate F)
Strong: the default path (the record, a trend, the wellhead travel time or one fitted lag with the clearing tested against 2019 to 2026) files the 2031 cycle; only the depth-specific delay files 2027.

## Findings, ranked
1. Ask 6 thin against a later arrival reading. Fixed: the ridge parcels' arrivals clustered at 2030.85 to 2030.92; every reading half a year early to half a year late files 2031 (checks.py R5).
2. Ask 8 thin (Well 7 0.26 above 15.5). Fixed: Well 7's ridge acreage raised; 15.92, and 15.85 at a vegetable leachate of 20.0 (R5).
3. The golden's mixing weight is not filed but fits the record best (rmse 0.21 against 0.40 at Well 6): kept as the asks' second judgment (SF10).

## Next action for the author
Re-judge once on the rebuilt target.zip.

## The thread's verdict (verbatim)

# Determinism verdict, task3 (Corlinden NR-1 timing)

**Verdict:** DETERMINISTIC on the main call (2027 cycle). Supplementary asks 6 and 8 are thin: ask 6 is a roughly 0.25-year timing margin, and ask 8 depends on an unpinned mixing weight and a leachate estimate. Reported as a Gate C risk, not a failure of the main call. SOLUTION_WRONG: none found.

**Disposition:** FIX_NOW (optional, no rerun). Pin or soften asks 6 and 8 only if the author wants them literal: file the mixing weight (acres x recharge of the land cover in force when the water left the water table) in the plan or prompt, and consider rounding Well 7 consistently. The main call, the stump and the files stay untouched. If the author prefers to leave it, APPROVE is defensible because the cycle decision holds under every reasonable variant.

## Why
- The decision (2027 vs 2031 cycle) is forced. Every depth-specific delay variant I ran puts the first year at 10 mg/L between 2031 and 2032, well before 2034. The 2031 cycle (in service 1 Jan 2034) fails in all of them.
- The only rival, "falling record or trend means no rise, so wait", is not defensible. It requires treating the Sallow Ridge clearing as leaching nothing, but the network shows irrigated vegetable land leaches about 21 mg/L. The depth-delay fit (0.133 yr/ft) from the 14 matured conversions also explains why the 3 upland clearings (TCGW-053, 076, 012) are still flat.
- Short-lag alternatives (wellhead travel time alone, one 4.5 or 4.7 yr lag) predict a rise already visible by 2026 (EP-01 about 10.4 from 2027 in my run). The record rejects them, so they cannot survive as defensible rivals.

## Evidence (recomputation ledger)
Source files: network samples + sites + age survey, parcel land cover, WHPA parcel attributes, raw water results, supply plan.

| Figure | Claimed | My value | Reproduced | Source |
|---|---|---|---|---|
| Matured conversions 1990 to 2008 | 14 | 14 (010, 014, 024, 026, 034, 051, 055, 056, 062, 064, 068, 070, 072, 085) | yes | land cover + sites |
| Delay slope b (yr/ft) | 0.13 (0.132) | 0.133; through origin 0.133 | yes | network samples, logistic half-way arrival minus conversion year |
| Fit residual (yr) | 0.3 | 0.28 | yes | same |
| Irrigated vegetable leachate, latest 5 land-surface years | 20.9 | 20.5 (3-yr smoothed) to 20.9 | yes, within estimation noise | network wells on unchanged land |
| Irrigated corn/soy leachate | 13.2 | 13.2 | yes | same |
| Irrigated vegetables before nutrient management | about 34 | 32 to 37 | yes | same |
| Ridge clearing area | 1,084 acres | 1,084 (10 parcels) | yes | WHPA attributes + land cover |
| Ridge depth to water | 54 to 95 ft | 54 to 95 | yes | WHPA attributes |
| Ridge arrival at wells | 2030 to 2031 | 2030.6 to 2031.5 | yes | model |
| Well model offsets vs 2019 to 2026 record | -0.31 to 0.01 | W3 +0.02, W5 -0.31, W6 -0.26, W7 -0.19 | yes | raw water results |
| EP-01 2030 | about 7 | 5.7 (consistent with water-table-age subtraction: 6.9) | approximately | model |
| First year EP-01 at or above 10 | 2031 | 2031 (EP 10.67; 11.6 if water-table age is subtracted) | yes, but thin (see fork) | model |
| EP-01 2034 | 12 | 11.87 | yes | model |
| Well 7 2034 | 16 | 15.76 | yes, but thin (see fork) | model |
| Well 6 2034 | not claimed | 14.9 | n/a | model |
| Plan shares 2027 to 2040 | 8/30/32/30 | as filed in plan Table 1 | yes | supply plan |
| Upland clearings flat to 2026 | "no rise yet" | flat at 0.5 to 0.6 mg/L N through 2026 | yes | network samples |

Forks and sensitivities (all from my own reconstruction):
- **Ask 6, first year.** Adding a +0.25 to +0.3 yr delay (for example a different step estimator, or double counting water-table age) turns the 2031 mean from 10.7 into 9.2 to 9.35, so the first year becomes 2032. Subtracting water-table age as the golden does moves it the other way (2031 = 11.6). A consistent conversion-date convention cancels out. Result: 2031 for the golden's own method and for the plain method, but the margin is thin. The cycle call does not move.
- **Ask 8, Well 7 2034.** The Well 7 mean is 15.76 under the golden's mixing (acres x recharge of the land cover at the time the water left the water table). It is 15.2 with acres only and 15.0 with recharge by the land cover at the land surface when the leachate left the root zone. The golden's mixing fits the record best (shifted rmse 0.21 vs 0.40 for Well 6), so it is data-supported but not filed in the prompt or files. Separately, Well 7 sits only 0.26 above the 15.5 rounding line. Irrigated vegetable leachate of 20.0 gives 15.28 (rounds to 15), 20.5 gives 15.56, 20.9 gives 15.78. EP-01 2034 stays at 12 for any irrigated vegetable leachate of 20 or more (11.6 to 12.1). Well 7 stays the highest well in every variant.
- **Ask 7.** 12 is robust across the variants above, except acres-only or low leachate, which give 11.4 to 11.5 (rounds to 11).

## Files/Hygiene
**PASS, no exclusion-level finding.**
- 13 files; formats: csv (5), xlsx (4), pdf (3), png (1).
- Two large CSVs: pumping daily (26,080 rows, mixed gal/kgal units, mixed well labels WELL n vs HR-Wn, and daily volumes in the 2019 onward rows that read very differently from the earlier ones) and network samples (5,114 rows, mixed NO3 vs N units, two labs, rebuilt wells).
- Unlabelled distractors: pumping data (plan shares are given), specific capacity workbook, fertilizer sales, well construction records.
- No provenance leakage seen. Data reads like real agency exports (lab changes, duplicates, re-runs, a well rebuild, a 2008 land cover recode, split parcels).
- Temporal coherence is fine (plan adopted Sep 2025, samples run to Nov 2026).
- One note: the 2019 onward pumping volumes appear to switch units for part of the file (status column, kgal mixed). That is texture only.

## Stump power
Strong. The trap that does the work is that the falling record, any trend on it, and every one-lag or travel-time-only model fitted to it reach "wait". Doing the right thing needs the depth-dependent unsaturated delay from the 14 conversions, the leachate by land-surface year, and the parcel-by-parcel carry to the wells. A solver that cleans everything perfectly and fits the record or the single average lag still lands on the 2031 cycle. I could not find a single sentence that rescues a run; the one-fact candidate ("the delay grows with depth to water") still leaves the fit, the leachate series and the mixing to be built.

## Stumping type
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported record and all figures are fine; the difficulty is a forward projection the correctly read past does not pin (outcome not yet finished happening). On clean data the task would still stump. Not banned.

## Deep reasoning
`domain: pass` (hydrogeologic travel-time modelling, wellhead protection, blended entry-point compliance), `layers: pass` (Layer 1: units NO3 vs N, two labs, rebuilt wells, split parcels, 2008 code recode, mixed pumping units; Layer 2: unsaturated delay and leachate projection), `decisive_step: analytical`, `chain: 5 inferences, judgment: depth-dependent delay fit and its out-of-range transfer to the ridge, justified against the upland clearings`, `one_fact: none`. The easy route is a per-well trend or a single-lag fit, giving EP-01 about 5 to 6 in 2034 and the 2031 cycle.

## Fix
Where: solution (optional) or prompt. Specific change: none needed for the main call. If asks 6 and 8 are to be graded literally, file the mixing convention and the leachate level in the answer blocks (solution wording), or state in the golden that Well 7 depends on it. No change to the input files.
