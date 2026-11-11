# determinism-check report, task13, pass 2, 2026-11-11

## Verdict
DETERMINISTIC on the main call (SOLUTION_WRONG on a few answer-block lines, see Findings)
**Disposition:** FIX_NOW (repair in the answer blocks; prompt and pack stay byte-identical)
**Stumping type:** mechanism: statistical_rigor / method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one isolated sonnet/medium thread; it reports keeping the order (own_derivation.md written before graded_blocks.md was opened). Scratch: /tmp/determinism-check-task13-p2/ (verdict.md, own_derivation.md).

## Why
The thread's independent build reproduced the 15-zone referral set exactly (weakest referred p 1e-4, next left out 0.0016, PGP-F3-R3), and most figures land in band. Three things are not closed by the filed text and blocks:
1. Supplementary 7 / Critical Component 4 state "each count exact" (15 inspected-and-confirmed, 26 misses). The thread got 16 confirmed / 25 misses under Poisson and 14 / 27 with dispersion 1.2. Not determinate across reasonable scatter models.
2. Supplementary 6 (sound referrals per season): the thread's first pass wrote the 0.2 budget; the rule's own rate (0.126) is inside the band only once the reading is pinned.
3. The CSV's faults-since-inspection column is restored counts, but the referral test uses recorded faults against the expectation over observed months. A literal reader applying the rule to the CSV figures gets another set (the blocks themselves say SRQ-F4-R3 would be added). The pack's gaps (event numbers, read dates) show the unobserved months, so the thread rates it closed by data, but it is not written in the blocks.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Referral set after 2026 | 15 named zones | same 15 | yes |
| Season faults 2022-2026 | 892, 682, 924, 747, 1,075 (3%) | 876, 668, 914, 723, 1,055 (exposure-adjusted) | yes except 2025 (-3.2%) |
| Radio-less zones 2026 | 259 (163 kept) | 248 (155 kept) | yes (band 243-275) |
| Sound-confirmed zone-seasons | 193 | 193 | yes |
| Referrals after each season | 11, 10, 12, 10, 15 | 11, 11, 13, 11, 15 | yes (each within one) |
| Sound referrals per season | 0.13 | 0.126 (rule's own); 0.2 (budget) | yes on the rule's own reading |
| Inspections check | 15 confirmed, 26 misses, exact | 16 / 25 Poisson; 14 / 27 dispersion 1.2 | no (not exact) |
| 2026 caused by failed protection | 279 (237-321) | 254 adjusted, 224 raw | yes adjusted, no raw |
| Avoided faults, average season | 107 (91-123) | 103 | yes |
| Per-zone figures | within 10% | BGS-F3-R2 20/5.4, PGP-F1-R2 20/2.6, BTG-F1-R3 73/12.5, LRD-F2 61/8.4 (golden 62/7.0) | LRD-F2 expectation 20% off, BTG borderline |

## First-pass figures against the stated bands (the thread's own_derivation.md)
| Result | Thread's first-pass figure | Stated band | Inside? |
|---|---|---|---|
| S1/S8 2022 faults | 876 | 892 +/-3% (865-919) | inside |
| 2023 | 668 | 682 +/-3% (662-702) | inside |
| 2024 | 914 | 924 +/-3% | inside |
| 2025 | 723 | 747 +/-3% (725-769) | outside (-3.2%) |
| 2026 | 1,055 | 1,075 +/-3% (1,043-1,107) | inside |
| S1 radio-less 2026 faults | 248 | 243 to 275 | inside |
| S1 radio-less kept | 155 | 163 (no band) | differs |
| S2 per-zone (4 checked) | 20/5.4, 20/2.6, 73/12.5, 61/8.4 | within 10% | yes, yes, borderline, no |
| S3 / Recommendation set | 15, identical list | exact set | inside |
| S5 after 2022..2026 | 11, 11, 13, 11, 15 | 11, 10, 12, 10, 15 each within one | inside, all |
| S6 sound referrals per season | 0.2 (budget reading, first pass); 0.126 in checking | 0.11 to 0.15 | outside as first written; inside on the rule's own rate |
| S7/CC4 vs inspections | 39/33/23/31 inspected by season; 17 referred-inspected, 16 confirmed, 25 misses (Poisson) | 15 confirmed, 26 misses, exact | outside (exact) |
| S9/CC2 2026 caused | 254 adjusted (224 raw) | 279 (237 to 321) | inside adjusted, outside raw |
| S10 avoided | 103 | 91 to 123 | inside |

Pricing note: the first pass of a single medium thread, with no hint, got the 15-zone set, the five referral counts, the 2026 caused figure and the avoided faults inside the stated bands, and it found the sound-baseline time-order reading unprompted (zones taken sound in seasons before a later clean inspection, 193 zone-seasons). Only the exact-count inspections result, the sound-referral reading and one season total (by 0.2 point) fell outside.

## Competing answers that survived
- Inspections check: 15/26 (golden) vs 16/25 (Poisson) vs 14/27 (dispersion 1.2). Closing rule: none filed; needs bands or a pinned scatter model.
- Sound referrals per season: 0.13 (rule's own rate) vs 0.2 (the programme budget). Terms 3(b) is a ceiling; the ask does not say which is wanted.
- Referral test on recorded versus restored faults: golden set (15) vs set with SRQ-F4-R3 (16) on restored counts. Closed by the like-for-like (observed months) reading, not written in the blocks.
- Scatter treatment: golden says Poisson refers 17; the thread's Poisson refers 15 (thread's referral-count rival band 13 to 17).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 12 | yes |
| File categories | 2 or more | csv, xlsx, docx, pdf, geojson (spreadsheet, text, code/data) | yes |
| Large messy CSVs | 20,000 rows; a 10-20 page one | strokes 149,410 rows (11.2 MB); recloser downloads 72,858 rows (5.8 MB); SCADA 38,782 rows | yes |
| Distractors in metadata.json only | 2 or more, none labelled in the zip | 3 (rain gauge, materials quotation, transformer replacements) | yes |
| Distractors unused yet weighable | yes | rain gauge, quotation, replacements decide nothing; OMS remarks mention thunderstorm but do not answer a graded quantity | yes (thread: no exclusion finding) |
| Deliverables | 1 to 3, all in golden | 2 (CSV, docx); golden.zip holds exactly those two | yes |
| Asks multi-dimensional, unit and rounding | yes | per-zone seasons, record since inspection, referral, rule, per-season counts, validation, caused, avoided; units in the blocks | yes |
| Answer shape | one of fourteen, 4 or more checkable results | flagged set with false-alarm rate; 9 graded results | yes |
| Realism | nothing LLM-looking, no builder trace | thread found no README or authoring language; mixed date formats and clock noise present; terms dated 26 Oct before the season's end (minor) | yes (not independently audited by me) |

## Gate G reconciliation
Thread: mechanism statistical_rigor / method_or_model_selection; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Gate G classification: pass, no shipped number overturned, the work is estimation and rule design. Note's Hidden factor record: clock drift, memory overwrite, contaminated baseline, extra-Poisson scatter, all `not only in deciding units`, fix depth modelling. The thread agrees these are process features across the 46 radio-less zones and every zone, not planted in the deciding units. No conflict with the note. The thread did not name a distractor as carrying a result.

## Stump power (Gate F)
Thread's likely hurried losses: radio-less clocks (a ten-minute window counts storm trips; one fixed offset finds 19 of 259), lost and unread months (about 90 faults of 2026), and the pooled baseline (about 126 to 150 caused instead of 279; 2 referrals). A solid run still diverges on scatter (15 vs 17), the exact inspection counts and the sound-referral reading, so part of the loss sits on forks, not analysis, until the bands are stated. The thread reached the referral set, R3 and R8 on a first pass without the note's hard steps being supplied, which bears on the note's careful column.

## Gate H
Thread line: domain pass; layers pass; results 9 graded across 6 areas; one_thing none; effort quick 2, careful 5, thorough 8 of 9; one_fact: "learn the sound rate only from seasons a later inspection confirmed sound" rescues about 3 of 9 (referral set, 2026 caused, avoided faults); the clock/restoration sentence also about 3 of 9.
Note: 8 results, quick 0, careful 0.5, thorough 8; Largest single hint (radio-less clocks and last events) rescues 2 of 8.
Reconciliation:
- The thread's careful pass (5 of 9) is well above the note's 0.5 of 8 and above a third. This is the findings pattern that predicts a send-back: the note's careful column assumes the careful run misses the baseline time-order step ("a clean inspection proves the seasons before it"), and the thread made it unprompted. The thread's `one_fact` hint (the baseline sentence) rescues 3 of 9, against the note's hint naming the clocks at 2 of 8; the larger single sentence is the baseline, not the one the note lists. Both are at or just above a third (3/9 = one third, exactly at the limit).
- No single hidden thing (`one_thing` none), and no factor only in the deciding units.
- Bands: LRD-F2 (7.0 vs 8.4) and the 2025 total sit just outside their bands; R6 and R7 need the pinning described above. No band found too wide to grade.

## Findings, ranked
1. R7 "each count exact" is not determinate across scatter models (16/25 and 14/27 against 15/26): FIX_NOW in Supplementary 7 and Critical Component 4 (bands, or pin the scatter model).
2. R6 reading: state the rule's own expected rate, not the ceiling.
3. Referral test over observed months against the restored CSV column: state in the blocks (and note beside the CSV column) that restored counts are reported, recorded counts are tested; give the referral-count band for rivals.
4. Thin per-zone and per-season bands: LRD-F2 expectation (7.0 vs 8.4), 2025 total (-3.2%).
5. Effort test: the thread's careful column (5 of 9) exceeds the note's 0.5 of 8 because the baseline time-order step was made unprompted; the main thread should weigh this against the note's effort test and the price of the task.

## Next action for the author
Edit the answer blocks only: replace the "exact" counts in Supplementary 7 and Critical Component 4 with bands (confirmed 14 to 16, misses 25 to 27) or the pinned scatter model, add the sound-referral reading to Supplementary 6, add the recorded-versus-restored line to the referral description, widen the two thin bands; then re-judge once under `/fix-determinism`, and weigh the careful-column finding against the note's effort test.
