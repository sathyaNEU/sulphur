# determinism-check report, task8 (architecture 18), 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (judge's recommendation; author may close the regional-centring convention on paper, see Findings)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no (borderline), sole_data_defect: no

## Why
The judge (one sonnet thread, scratch /tmp/determinism-check-task8-20261108063652/, derivation written before graded blocks opened) executed the shipped text literally. The standard is expected 26/40 on the 2022 paper (specification 4.1/4.2, LN1-SS-2022 s3). The bank alone gives 21.57 and pass mark 22. The 36 shared Level 2 items show a Level 1 shift explained by stem length and everyday context together (residual SD 0.105 logits; context alone 0.26, length alone 0.32, none 0.33). Carried to the twelve long mathematical items this gives 19.14 (golden 19.09) and pass mark 19 under every functional form tried (19.14 to 19.34). Single-cause and no-shift routes give 20.8 to 21.5 and are rejected by the fit. Band classification reproduces (Q29 to Q33 below, seven inside, none above). Regional whole marks reproduce exactly (15/16/17/16/17/17) under response-weighted centring of regional everyday offsets.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Bank expected mark at standard (2027) | 21.57, pass 22 | 21.568 (26.2 target 21.80; preliminary run 21.56), all 22 | yes |
| Two-cause expected mark | 19.09, pass 19 | 19.14, pass 19 | yes (0.05 apart; method-level) |
| Items below band | Q29 to Q33, 0.11 to 0.14 | Q29 to Q33, 0.12 to 0.15 | yes on class; 2dp differs by 0.01 on some items |
| Seven other patterns items | 0.25 to 0.40 inside | 0.25 to 0.40 inside | yes |
| Regions | 15,16,17,16,17,17 | 14.91, 15.61, 17.15, 16.38, 16.72, 17.20 = 15,16,17,16,17,17 | yes |
| Bank-only regions (wrong route) | n/a | 20,19,19,19,16,18 | n/a |
| Context only / length only | 20.81 / 21.35 | 20.8 / 21.4 | yes |

## Competing answers that survived
- Regional centring: unweighted centring puts PKN at 16.53 (17 against 16); dropping the offset on the 2027 everyday items puts WPG at 15.69 (16 against 15). Neither is closed by a shipped sentence; the principled specification (response-weighted centring, offset applied to the paper it describes) lands on the golden. PKN 16.38 and WST 15.61 sit about 0.1 from a rounding edge. Not a surviving fork by the judge's verdict, but thin.
- Item chances at 2dp move by 0.01 on some items with calibration method (JML vs separate Rasch); band flags are unaffected.
- No fork on the pass mark: 0.36 from the 19.5 edge.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ files, 2+ categories | 11 files (3 pdf, 5 csv, 2 xlsx, 1 eml); spreadsheet, text, code-free but csv/pdf/eml text; categories spreadsheet and text | pass (categories borderline: no database, image or code; spreadsheet plus text = 2) |
| Large messy files | CSV 20,000+ rows; CSV 10 to 20 printed pages | responses 400,052 rows (23 MB); register 10,550 rows (1.0 MB) | pass |
| Distractors | 2+ in metadata.json, none labelled in ZIP | learner_confidence_survey_2026.csv, centre_computer_suite_audit_2026.xlsx; ZIP names are neutral | pass |
| Distractor weight | unused, relevant, ruled out by a shipped fact | judge found both unused and relevant-looking; neither named as carrying the task | pass (not separately arithmetic-tested) |
| Deliverables | 1 to 3, all in golden | pass_mark_2027.docx, l1_2027_items.xlsx; both in golden/ | pass |
| Asks | multi-dimensional, unit and rounding stated | 40-row item table plus six regions; whole marks and 2dp stated | pass |
| Answer shape | many gradable cells downstream of deep step | 40 chances, 40 band flags, 6 regional means | pass |
| Golden ZIP exact | only requested files | golden.zip 47,821 bytes; golden/ holds exactly the two files | pass (zip listing not opened) |
| Reads real | no LLM tells, realistic goldens | judge found no authoring language; mess realistic | pass |
Leak check (separate report) is REVIEW, not LEAK: spec PDF contains 0.20/0.90 band values (legitimate, filed) and some vocabulary overlap.

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no (borderline), sole_data_defect no. Design note: decisive step is the joint two-cause split (constant, cost per 100 words, everyday advantage) carried to the long mathematical items, classed as separating two explanations for one pattern; clean data still files 22; Layer 1 mess "nothing placed to be caught". These match. The judge did not name a distractor as the surface read. Judge's caveat: if a reviewer reads the bank as a misleading reported number, route to live testing. Design note's easy route (22) and careful route (21) agree with the judge's.

## Gate H line
domain: pass (psychometric standard maintenance and equating); layers: pass (L1 position/item codes, duplicates, register variants, preliminary vs final bank; L2 population DIF transport plus regional everyday offsets); decisive_step: analytical; chain: 5 inferences (standard to theta*; Level 1 vs Level 2 shift on shared items; joint two-cause fit extrapolated to long mathematical items; recompute chances and pass mark; regional offsets and re-estimated abilities); one_fact: none that makes it routine.

## Stump power (Gate F)
High per the judge: the bank route is clean and passes its own checks (22, every item in band), and the decision needs linking across two populations and extrapolating to a cell with no shared items. The two-cause fit is the field's differential-functioning idea, but the extrapolation to unseen long mathematical items and the cancellation on long everyday items are dataset-specific; recorded for the main thread to weigh against the ladder. Transport of bank difficulties to a second population is a textbook concern a strong solver may reach (stumping 1.3), and the single-cause routes landing on 21 are the intended miss.

## Findings, ranked
1. Regional means rest on a convention the Step-by-Step does not state (response-weighted centring of regional everyday offsets, offset applied to the 2027 everyday items). Two rival conventions move one region each by one mark. Close in the generator and writeup.
2. PKN 16.38 and WST 15.61 sit about 0.1 from a rounding edge.
3. Golden 19.09 vs independent 19.14 and item chances at 2dp vary by 0.01 with calibration; graders should tolerate 0.01.
4. Surface risk: bank-as-misleading-number reading (judge's borderline note).
5. Leak check REVIEW items (band values in spec; prompt shell quota 'whether' and docx+xlsx deliverable set over caps) are for the leak process, not the judge.

## Next action for the author
State the weighted-centring convention for the regional offsets in the filed material or Step-by-Step (or assert it in checks.py with the unweighted rival shown to land on the same marks, or move the regions off the edge), then proceed to stage 5.
