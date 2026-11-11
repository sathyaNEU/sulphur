# determinism-check report, task9 (architecture 10), 2026-11-11

## Verdict
DETERMINISTIC on the main call and the win-share ask; Gate A only partly reproduced (see ledger); one open fork on the 80% range (R6).
**Disposition:** FIX_NOW (confined to ask 1's range; gate failed is C on R6, not G or H, so no architecture is spent)
**Stumping type:** mechanism: method_or_model_selection (measurement horizon and replay on honest data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Thread order: kept (own_derivation.md written from prompt and bundle first, graded_blocks.md opened after). Thread files: scratchpad/determinism-check-task9-a10/{own_derivation.md,verdict.md}.

## Why
The request base (two audit generations, latest version, 144A mapping), segments, quoter mechanics, v3 repricing and the win comparison against rivals' levels (cover on wins, tape print on losses) reproduce from the files. The thread did NOT rebuild the post-trade cost, edge/offload roll-up, 2027 totals, bridge or percentiles, so the money asks were checked for internal consistency only (bridge sums to 5,061k = 10.30 - 5.24; four losers sum to -2,900k vs 2,901k). The horizon claim ("25 and 45 days give the same answers") is unconfirmed by an independent run.
The literal reading of policy 6(c) ("251 trading days drawn from the record's own days") is days drawn one at a time. The thread, and the design note's own results chain, record that this gives 7.68 to 13.02 million, outside the golden's P10 band (4.98 to 6.69) and P90 band (13.70 to 16.41). The golden uses 21-day runs. Nothing filed says runs; the closure rests on a data fact (first-order autocorrelation 0.19 against a noise bound 0.06) that the answer blocks do not state.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Win share, current v3, 12 segments (IG liq AM ... HY thin HF) | 28.6, 12.9, 23.8, 15.2, 16.3, 24.8, 4.8, 12.1, 6.7, 16.4, 9.8, 6.6 | 28.4, 12.5, 23.4, 15.0, 16.1, 24.5, 4.7, 12.0, 6.7, 16.3, 9.7, 6.6 | yes, within +-2 band |
| Win share, draft, 12 segments | 36.3, 32.6, 44.3, 35.3, 37.4, 48.6, 13.2, 26.3, 20.1, 34.3, 24.7, 16.3 | 36.3, 32.5, 44.2, 35.2, 37.3, 48.6, 13.2, 26.3, 20.2, 34.3, 24.7, 16.3 | yes (0.1 to 0.4 pt); denominator all vs excluding Passed differs 1 to 2 pt, inside band |
| Request base: 281,204 audit rows, 1,117 exact duplicates, 279,249 requests; Done 39,192 = blotter | (assembly) | same | yes |
| Cost per million, current wins and added trades (24 figures) | ask 4 | not rebuilt | no |
| 2027 P&L 5.24 / 10.30 / 13.20 million | asks 1 | not rebuilt | no |
| Bridge items (12) and loss set | ask 2 | internal sum only | no (consistency only) |
| 80% range 5.71 to 15.01 | ask 1 | day-by-day literal reading 7.68 to 13.02 (golden's own days, per note) | fork, outside band |

## Competing answers that survived
1. Range: days drawn one at a time (7.68 to 13.02 million) vs runs of 21 days (5.71 to 15.01). Both are executions of "drawn from the record's own days"; the shipped rule (policy 6(c)) does not choose. Closure exists only in the note's SF18 and is not in the pack or the answer blocks.
2. Horizon of "as soon as that move is complete": not a filed number; closed by the Ashcote month-end lag in the data (unconfirmed by the thread's rebuild).
3. Win-share denominator: inside band, not a fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 27 | yes |
| File categories | 2 or more | csv, xlsx (spreadsheet), pdf (text): 2 | yes (minimum) |
| Large messy CSVs | 20,000 rows and 10 to 20 pages | tape 497,437 rows; audit 149,366 and 131,838 rows | yes |
| Distractors in metadata.json, none labelled inside ZIP | 2 or more | SOFR.csv, SPX_History.csv, league tables xlsx | yes on count; that each reproduces a graded quantity and is ruled out by a shipped fact NOT verified |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx); golden.zip holds exactly those | yes |
| Asks | multi-dimensional, units, no rounding dictated | six asks, USD and per cent stated, no rounding instruction | yes |
| Shape and results | one of 14 shapes, 4+ results | bridge/flagged set with range, 8 results | yes |
| Realism | not LLM-looking | not assessed beyond thread hygiene (no leakage seen); the answer blocks carry no em dashes found | not fully checked |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Note: the month-end lag is across every medium and thin bond, the tape level across every lost request, informed flow across every segment; none sits only in the deciding units. Consistent. Gate G line: no shipped artifact found ranking the candidates wrongly; the lag is a construct of the process across all medium and thin buckets, and the thread found no sole planted defect.

## Stump power (Gate F)
Strong in the thread's reading: next-day markouts (22.15 million, wrong set), a week's marks (14.67 million), win model on own quotes (6.54 million), added trades costed like today's wins (6.55 million). Results a careful hurried run earns by the field's method: assembly and win shares by tape matching, and the range by a block bootstrap if it runs one unprompted (note: bands admit runs of 10 to 63 days).

## Findings, ranked
1. FIX_NOW, R6/ask 1: literal "days drawn" (7.68 to 13.02) sits outside the P10 and P90 bands. Close by naming the data fact in the answer blocks, or by a filed sentence in policy 6(c) that the draw keeps consecutive days, or widen the bands to the 7.68 to 13.02 rival (which would then not separate the careful 6.30 to 6.79 from the golden; weigh).
2. Gate H divergence (below): the thread puts the careful pass at 3 of 7 and the month-end sentence at about 3 of 7; the note puts them at 0.5 of 8 and 1 of 8. The thread did not rebuild costs, so its figure is an estimate; the main thread should weigh it against `effort.py`, since 3 of 7 is over a third.
3. Gate A not independently reproduced for costs, totals, bridge and percentiles; the loss set rests on the horizon claim.
4. Thread counted distractors as DAAA/DBAA/DGS*/SOFR/SPX; metadata names SOFR, SPX and the league tables. Check the declared three weigh enough.
5. Thread unexplained: a ~+11% implied-jitter bump in the week of 2024-10-14 and a smaller one in October 2025 (334 outliers); decides nothing asked.

## Gate H line
domain pass; layers pass; results 7 graded in 5 areas (note: 8 results across assembly, measurement, modelling, causal, forecasting, uncertainty, decomposition, synthesis); one_thing: none (note agrees: tape level alone rescues R2 only); effort (thread): quick 1, careful 3, thorough 6 of 7 vs note 0, 0.5, 8 of 8; one_fact: thread "read the move at month-end for medium and thin bonds" about 3 of 7 (43 per cent) vs note's "the level a rival won at is on the tape" 1 of 8; thread's estimate exceeds a third and is unverified.

## Next action for the author
Close SF18 in the pack-visible text: add the autocorrelation fact and the 10-to-63-day block range to the answer blocks (Step-by-Step 6 and ask 1), or file runs-of-days in policy 6(c), then reconcile the one-fact and careful-pass counts with effort.py. A change to the policy PDF or to a graded band moves the pack or figures and voids this pass; wording confined to the answer blocks does not.
