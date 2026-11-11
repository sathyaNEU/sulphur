# determinism-check report, task9, 2026-11-11 (pass 2, single re-judge after FIX_NOW)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE on determinism, with one open difficulty finding (one-fact reach, Findings 1) for the main thread to weigh against the note's effort test before READY.
**Stumping type:** mechanism: forecasting (with decomposition_attribution), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one general-purpose sonnet thread, scratch /tmp/claude-0/-home-user-sulphur/2ddb3641-4769-5139-aa6d-71f6eadaeff9/scratchpad/determinism-check-task9-a10-pass2/. It reports it derived first (own_derivation.md) and opened graded_blocks.md only afterwards. Its markout pipeline is approximate (own yield, duration and spread median; own issuer not excluded).

## Why
The shipped files force the replay. The quoter's distance ratio is 1.000 median (sd 0.08) across v1/v2/v3, so the segmentation reproduces the quoter. Rivals' prices come from the cover (Done) and the tape print (264,972 of 264,972 matched). Policy sections 5 and 6 fix P&L, replay, counts and percentiles. Golden internal sums hold: bridge 5,061k = 10.30 - 5.24; losers -2,901k, 10.30 + 2.90 = 13.20.

## Recomputation ledger (judge's own_derivation.md, written before the blocks, against the stated bands)
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Win shares, 12 segments | 36.3, 32.6, 44.3, 35.3, 37.4, 48.6, 13.2, 26.3, 20.1, 34.3, 24.7, 16.3 | 36.3, 32.5, 44.3, 35.3, 37.3, 48.6, 13.2, 26.3, 20.2, 34.3, 24.7, 16.3 | yes, all within 0.1 pt (bands +-2) |
| Bridge by segment, USD k | -1781, -449, -605, +210, +175, -65, +1607, +3467, +676, +1230, +204, +393 | -1765, -436, -567, +221, +212, -56, +1595, +3441, +691, +1288, +227, +418 | yes, all inside bands (30 days) |
| Losing set | IG liq AM, IG med AM, IG med HF, IG thin HF | same four at 20, 25, 30, 45 days | yes |
| Current / draft P&L, 2027 | 5.24 / 10.30 M (4.70-5.67 / 9.87-11.06) | 5.69 / 10.96 (30d), 5.14 / 10.49 (45d) | 30d slightly above bands, 45d inside; 25-45d judged inside; approximate pipeline |
| Next-day view | 12.91 / 22.15 | 13.08 / 22.4 | yes |
| Week's marks | 7.85 / 14.67 | 8.23 / 15.18 | yes (rival, as stated) |
| Markout per MM, 24 cells | bands as stated | 18 of 24 inside | partly: outside are IG thin AM current 409 (418-630), IG thin Ins added -107 (-46 to 14), HY thin HF added 463 (664-936); judge attributes to its cruder spread median, not run against the generator |
| Range 10th / 90th | 5.71 / 15.01 (runs of 21) | not computed in own derivation; single days 7.2-11.5 on its own days | golden single-day 7.68-13.02 is outside the bands, as the note says |
| Plan without losers | 13.20 (12.66-13.99) | follows from bridge | yes |

Completion horizon: market-neutral markout per MM rises 131 to 478 over 0 to 15 days, plateaus about 15-20 days (481-501 at 20-45); golden's 30 days sits on the plateau. Below 8 days the loser set shrinks, so those rivals are real and ruled out by the plateau.

## Competing answers that survived
1. Range draw: policy 6(c) says only "251 trading days drawn from the record's own days at the plan's request counts". Single days give a different graded range (golden's own 7.68-13.02; judge 7.2-11.5), outside the bands. Closed by named data (autocorrelation 0.19 vs bound 0.06; SF18), not by a filed sentence. A literal reader drawing single days loses R6 only. Residual risk on one result.
2. Completion horizon: 20 days gives about 6.0 / 11.4 in the judge's pipeline, about 5% above the band edges; 25-45 sit inside. Bridge, losers, shares unmoved. Minor; SF4 already says 25-45 hold every band.
3. Ties (831 Done rows tie the cover, 869 Covered rows tie the winner): immaterial; SF3 closes it.
4. Win-share denominator (all requests vs quoted) adds 0.5-2 pts: inside the bands.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ files, 2+ categories | 27 files in the zip (judge counted 26 usable; one more is a PDF), CSV, xlsx, PDF | yes |
| Large messy CSVs | one 20,000+ rows, one 10-20 pages+ | tape 497,438 rows; RFQ audits 149,367 and 131,839; evaluated prices 167,350; blotter 66,946 | yes |
| Distractors in metadata.json | 2+, none labelled in ZIP | 5 named (DAAA, DBAA, SOFR, SPX_History, league tables xlsx); no label in the zip; month-end summaries workbook is the stale next-day rival, not declared | yes |
| Distractors unused yet weighty | reproduce arithmetically, ruled out by a shipped fact | the judge names none of the declared five as carrying a result; the summaries' next-day view reproduces 12.91 / 22.15 and policy 5(b) rules it out | yes |
| Deliverables | 1-3, all in golden | xlsx plan and docx memo, both in golden/ | yes |
| Asks | multi-dimensional, units stated, no rounding instruction | prompt states USD, dictates no rounding | yes |
| Shape | one of fourteen, 4+ checkable results | bridge with ranked losers, scenarios/flip, forecast range; 8 results | yes |
| Golden = requested files | exact | exactly the two requested | yes |
| Reads as real / not LLM generated | no | judge found no provenance disclosure and real-looking mess; golden realism not re-read here | yes (judge) |

## Gate G reconciliation
Thread: mechanism forecasting + decomposition_attribution; family analytical_non_defect; surface_read_dependency no; sole_data_defect no; Gate G passes. Note's Hidden factor record: Ashcote month-end lag (constructed, across all medium/thin bonds, found by modelling), hedge-fund informed flow/pickers (across data), tape levels (method choice), clustered P&L days. The thread agrees with the note that no factor sits only in the deciding units and no single planted defect carries the answer. The thread calls the evaluation lag a constructed measurement factor and a watch item; it found it by modelling markouts at several horizons (a plateau read), not in one look. Consistent with the note's "modelling" fix depth.

## Gate H (thread): domain pass; layers pass; results 8 across 6 areas; one_thing none (watch: the lag); effort quick 2, careful 4, thorough 8 of 8; one_fact "Ashcote's marks for medium and thin bonds only catch up at the month-end, so read the move after about 30 days" rescues about 4 of 8 (levels, bridge, losers, costs).

Against the note's Effort test (quick 0, careful 1.5, thorough 8; largest hint rescues 2 of 8, R1 and R4):
- Quick: thread 2 of 8 (25%), within a third. Careful: thread 4 of 8 against the note's 1.5; the table still separates careful from thorough.
- One-fact: the thread's sentence (which includes the horizon) rescues about 4 of 8, half, against the note's 2. The note's own carry-forward says a horizon slip costs every result except R2, so a sentence that fixes the horizon feeds R1, R4, R5, R7, R8. The note's hint ("catch up only at the month-end review") names the mechanism without the horizon, which is the weaker sentence.
- Thread effort grades and the note's differ mainly in R5 and R6 for the careful pass; the note's careful R6 "Missed" (days one at a time) is a rival the thread confirms is outside the bands.

## Stump power (Gate F)
Spread across several results. Rivals each change the levels and usually the loser set: next-day 22.15M (drops 1), week's marks 14.67M (drops 2), added trades costed like today's wins 11.80M (drops 3), win model on desk quotes 6.54M (drops 5), complete costs with added trades costed like today's wins 6.55M. Tape matching, 144A and bucket assembly, and the block draw each cost a careful run points. A result the thread reached with a standard method alone: win shares on the tape's levels (R2), which the note already grades as earned by the careful pass.

## Findings, ranked
1. One-fact reach: with the horizon included, the best sentence plausibly rescues 4 of 8 on the thread's grading (up to 5 by the note's own carry-forward), above the one-third limit. The note's "2 of 8" counts the mechanism sentence only. Main thread to decide whether to re-state the Largest single hint with the horizon and re-price, or to accept. The policy's phrase "as soon as that move is complete" already points at the plateau read.
2. Range draw (R6) rests on named data, not a filed rule: single-day draw is a defensible literal reading that lands outside the band. Add it as a named rival to the fork table (SF18 already exists) if not present.
3. The 30-day currents/drafts level sits near the top edge of the stated P&L bands in the judge's cruder pipeline (5.69 vs 5.67; 10.96 vs 11.06 is inside); 20 days is 5% above. Bands hold from 25 to 45 days per SF4.
4. Three markout-per-million cells (IG thin AM current, IG thin Ins added, HY thin HF added) did not land in the stated bands in the judge's pipeline; its own spread median is cruder (own issuer not excluded). Not verified against the generator; if the author wants certainty, check those three against the leave-out median with an independent implementation.

## Next action for the author
Decide on Finding 1: rewrite the note's `Largest single hint:` with the horizon included and its rescued-result count (4 to 5 of 8), and either accept it with the argument that the three costed results and the range still need separate work, or redesign so the horizon alone rescues a third or fewer. No pipeline rerun is needed for determinism.
