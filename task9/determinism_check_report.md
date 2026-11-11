# determinism-check report, task9 (architecture 9), 2026-11-11

## Verdict
NOT_DETERMINISTIC (narrow; the golden reproduces, but two committed answers carry bands that sound rivals fall outside). SOLUTION_WRONG on one supporting figure (step 7).
**Disposition:** SEND_BACK (the judge's reading; the fix needs a pinned convention in the policy PDF, which changes what solvers see. Widening bands only in the blocks would be FIX_NOW but would leave the headline band unable to separate 665 from the 720 to 776 of the hurried routes).
**Stumping type:** mechanism: method_or_model_selection (shrinkage, within-pod capacity, block-bootstrap range) plus a benchmark-definition layer (carry); stumping_family: mixed; surface_read_dependency: partly; sole_data_defect: no.
Judge thread kept the order (own_derivation.md written before graded_blocks.md). Scratch: /tmp/determinism-check-task9-051419/ (verdict.md, own_derivation.md, work/).

## Why
Supplementary 3 reproduces to 0.02 pt per group once the carry is netted; the four failing increases reproduce with a clear gap; capacity reproduces at the band edge; the headline reproduces only under a maximum-likelihood group prior. Sound estimator choices the files do not pin move it out of band: simple-mean prior with moment-fitted spread 752, three-year record window 596. Trailing-252-day betas (the methodology PDF's own window) put Currencies, Quantitative equity and Volatility alpha outside their bands. Step 7's 293 million does not reproduce (judge gets 226; 7 of 8 overshoot years holds).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Group alpha (Comm/Credit/Curr/ELS/QE/Rates/Vol) | 9.51/4.31/6.09/9.17/8.01/8.58/9.18 | 9.53/4.31/6.10/9.16/8.03/8.59/9.20 (carry netted) | Yes, 0.02 pt |
| Net 2027 P&L | 665 (643 to 686) | 679 ML prior; 752 simple prior; 596 last 3 yrs | Only under ML prior |
| 80% range | 270 to 999 | 294 to 1,054 (ML); 354 to 1,112 (simple) | P10/P90 slightly above band |
| Failing increases | HC1051 .43, HC1059 .79, HC1090 .12, HC1124 .66 | .55, .92, .22, .64 (next HC1119 1.31, HC1110 1.64, HC1104 1.73, HC1067 1.77) | Yes; borderline set differs (HC1067 in, HC1010/HC1065 out) |
| Capacity per doubling | 26.3% (24.8 to 27.3); across pods 5.1 | 24.2 onboarding NLS, 25.3 to 25.8 pod-years, 28.3 (>=200 days); across 2 to 5 | At band edges; onboarding bootstrap interval 17.5 to 28.4 |
| Past plans overshoot | 7 of 8, mean 293 | 7 of 8, mean 226 | Direction yes, 293 no |
| Data facts (74 duplicates, 3 missing dates, units, code map, 220 pods, 2,473 days, 165 halvings) | as stated | all hold | Yes |

## Competing answers that survived
1. Beta window for alpha (policy s7 silent, methodology says last 252 days): trailing-252 gives Currencies 5.07/5.73, QE 7.73/7.41, Vol 8.82/8.50 against bands 5.67 to 6.57, 7.80 to 8.58, 8.87 to 9.81. Not among the rivals step 2 says were run.
2. Expected-alpha estimator for the plan: ML prior 679, simple-mean prior 752, 3-year window 596, no shrinkage 832 (carry netted). Band 643 to 686 covers only the first.
3. Group aggregation: capital-pooled (forced by "percent of capital") vs mean of pods (QE 10.2, Rates 11.7, Vol 12.2); minor.
4. Carry convention comes from the blocks, not the policy; credit pods in fact earn about 2.7x that carry, so the data cannot confirm the scale.
5. Hurdle borderline set: handled as "either call stands"; sound.
6. Review-date bill rate 4.01 vs 2026 plan's 3.73 print: about USD 1 million, immaterial.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ | 41 in zip (judge: about 40; 36 CSV, 2 PDF, 2 XLSX) | Yes |
| File categories | 2+ | spreadsheet, text/CSV, PDF (document); no database/image/code. CSV-heavy | Yes (borderline, depends on whether PDF counts as text) |
| Large messy CSVs | 20k rows and a 10 to 20 page one | legacy 114,929 rows; new 77,447 rows; both messy | Yes |
| Distractors in metadata.json | 2+ named, none labelled in ZIP | DAAA.csv, IR3TIB01USM156N.csv; no label found in zip names | Yes |
| Distractor weight | unused yet relevant | DAAA (Aaa; Baa fits every era better) reproducibly rules itself out; IR3TIB01USM is an FX-carry-adjacent rate, optional basket changes Currencies by 0.01 | Yes (IR3TIB light) |
| Deliverables | 1 to 3, all in golden | xlsx + pptx, both in golden/ | Yes |
| Asks | multi-dimensional, units stated, no rounding dictated | prompt dictates none; units in asking sentence | Yes |
| Answer shape, 4+ results | one of fourteen | forecast with range plus flagged set (alloc/forecast), 6 graded | Yes |
| Realism / LLM-feel | none | judge saw no authoring language; I did not audit golden prose | Not independently checked |

## Gate G reconciliation
Judge: mechanism method_or_model_selection with carry layer; mixed; surface_read partly; sole_data_defect no. Design note's hidden factor record lists five factors, all real or across-the-data, fix depth "modelling", verdict keep; this agrees: no single planted thing. Notes: the DESIGN_NOTE results table is stale against the blocks (R3 663 vs 665; R4 258 to 1,000 vs 270 to 999; R1 credit band 3.89 to 4.59 vs 3.89 to 4.70), and it calls R2 "Right" in the careful column. The judge's "careful earns result 4 (all-days 27% inside band)" matches that. The note says the largest hint (carry) rescues 2 of 6; the judge agrees (about 2 of 6). The declared distractors do not carry a result.

## Stump power (Gate F)
Spread over credit alpha (6.42 vs 4.31), the headline (hurried 720 to 776, risk-model-days 733 vs 665), return-on-record pricing (1,304), HC1059/HC1124 calls. Risk is the opposite: bands are tight (headline about 3 per cent, group alphas +-0.3 to 0.5 pt), so a correct run can miss.

## Gate H line
domain: pass | layers: pass | results: 6 across 5 areas | one_thing: none | effort: quick 1 of 6, careful 3 of 6, thorough 5 to 6 of 6 | one_fact: carry sentence rescues about 2 of 6 (within a third). Note's effort table says careful 1.5 of 6; the judge's careful 3 of 6 is double that and above the quarter the note claims, though not over half.

## Judge first pass versus the blocks (before it opened them)
| Result | Judge first pass (price-only factors) | Blocks | Within band? |
|---|---|---|---|
| Group alpha Comm/Credit/Curr/ELS/QE/Rates/Vol | 9.52/6.42/6.25/9.17/8.03/8.64/9.14 | 9.51/4.31/6.09/9.17/8.01/8.58/9.18 | All but Credit (it hit the 6.42 hurried trap); Curr 6.25 inside 5.67 to 6.57 |
| Alpha-per-dollar fall | about 24% (band 20 to 28) | 26.3 (24.8 to 27.3), across 5.1 | 24% just outside; all-days 27% and pod-year 25.3 to 25.8 inside; across pods 2 to 5 right idea |
| Net 2027 P&L | 814 (gamma .4, group-mean prior, daily draws) | 665 (643 to 686) | No |
| 80% range | 470 to 1,150 | 270 to 999 | No |
| Failing increases | none robust; borderline HC1131, HC1051, HC1065, HC1090 | HC1051, HC1059, HC1090, HC1124 | No (MC noise 0.7 pt, 1,500 paths) |
| Recommendation | plan about 0.8 bn, drop none | 665, drop four | No |
After seeing the blocks and netting carry the judge reproduced the golden except as listed in the ledger. First pass earned about 2 of 6 (alpha non-credit groups are a partial, capacity near).

## Findings, ranked
1. Headline band covers one of three sound prior estimators (752 and 596 fall out); fork 2.
2. Beta window fork moves three group alphas outside bands.
3. Step 7's USD 293 million does not reproduce (about 226).
4. Capacity band is at the edge of the pod-year spread (25 to 28).
5. Design note is stale against the blocks; effort grades differ from the judge's (careful 3 of 6).

## Next action for the author
Add one sentence to the policy PDF pinning how a pod's expected alpha is read from its record (window and shrinkage target) and that betas use the full record, rebuild, rerun the pack; also correct step 7's figure to 226 or show the definition giving 293 and align the design note to the blocks. Do not widen the headline band alone.
