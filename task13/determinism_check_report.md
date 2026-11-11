# determinism-check report, task13, 2026-11-11 (pass p4, architecture 3)

History: p3's first pass (architecture 2, report kept in git history at 0c259a0) was DETERMINISTIC, APPROVE, but its first pass landed the avoided faults (102 to 121) and the sound-referral rate (0.13 to 0.15), so the build went back to stage 2 on that pricing. This pass judges the rebuilt design. One thread, run p4, scratch /tmp/determinism-check-task13-p4/. Order kept: the thread wrote own_derivation.md before opening graded_blocks.md.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (the judge's; the Gate H caveat under Findings goes to the main thread)
**Stumping type:** mechanism: method_or_model_selection (with decomposition_attribution and forecasting-style valuation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every decisive fact sits in the shipped files: strokes in UTC against local SCADA stamps, per-controller clock drift visible only against strokes, event-number jumps (63 jumps, 1,346 events, 18 zones, reproduced exactly) and read dates showing the unread tail, the inspection book for confirmed-sound seasons, and the terms' false-referral budget. The data support the zone-level model: in sound seasons per-zone observed/expected ratios persist (odd/even-season correlation 0.45; MPD-F2-R2 about 2.4, CLB-F2 about 0.46). A season-by-season rule therefore refers sound high zones and misses low failed ones, as the golden argues. The thread's first pass reached 4 of the 5 seasonal totals and the 2026 sound expectation, and failed where the restoration and the zone level are needed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Event-number jumps (memory loss) | 63 reads, 1,346 events, 18 zones | same | yes |
| SCADA first trip to stroke, UTC+8h, 400 m | within about a second | about 0.03 s lag, sd 0.08 s | yes |
| Radio-less clock drift per read | fitted per recloser | 38% of recloser faults matched after a per-recloser fit | structure yes, size approximate |
| Network faults 2022 to 2025 | 561, 413, 593, 620 | 555, 408, 574, 610 (no restoration) | yes, inside 4 per cent |
| Network faults 2026 | 655 | 607 (no restoration) | no (the unread tail) |
| Sound-expected 2026 | 469 | 472 | yes |
| Failed-protection faults 2026 | 186 | 135 (unrestored) | no (the gap is the restored faults) |
| Referral set | 11 zones | 10 zones (plain regression), 9 on equivalent zones, BGS-F3 instead of BGS-F3-R1 and CLB-F2 | no (the golden's own rival, ruled out by the persistence test) |
| Weakest referred / strongest left out vs 1/715 | 0.000094 / 0.0036 | threshold margin 2.6x each side | yes |
| Avoided faults | 116 | 66 (record-since average; golden's rival 72), about 92 (2026 state, unrestored) | no as 66, in family as 92 |
| Restoration size, 32 radio-less zones 2026 | 130 | not pinned independently | not run |

## First-pass vs bands
Figures are the thread's from own_derivation.md, written before the blocks were opened.

| Graded result | First-pass figure | Stated band | In/out |
|---|---|---|---|
| Network faults 2022 | 555 | 561, 4% (539 to 583) | in |
| 2023 | 408 | 413 (397 to 430) | in |
| 2024 | 574 | 593 (569 to 617) | in |
| 2025 | 610 | 620 (595 to 645) | in |
| 2026 | 607 | 655 (629 to 681) | out (no restoration) |
| Radio-less zones' 2026 faults | not computed (no restoration) | 130 (120 to 138) | out |
| 2026 failed-protection faults | 135 | 186 (170 to 200, same in the note and the blocks) | out |
| Sound-expected 2026 | 472 | 469 | in |
| Referrals after 2022 / 23 / 24 / 25 / 26 | 4 / 4 / 4 / 9 / 10 | 1-3 / 1-3 / 3-5 / 7-10 / 10-12 | out / out / in / in / in |
| 2026 referred set | 10 zones incl. BGS-F3, lacking BGS-F3-R1 and CLB-F2 | exact 11 zones | out |
| Sound zones per season | not computed | 0.14 (0.12 to 0.16) | not run |
| Inspection check (5 / 5 / 21) | partial, 2-3 of 4 confirmed a year, not on the 4-round window | 3-6 / 3-6 / 20-23 | not comparable |
| Avoided faults, average season | 66 (about 92 on the 2026 state, unrestored) | 116 (104 to 128, same in the note and the blocks) | out as 66 |

By graded result, the first pass landed about 3 of 10 inside the bands (the 2022 to 2025 totals, the sound expectation and the 2024 to 2026 alert counts as partial credit); the rest fell outside or were not run. Contrast with p3, whose first pass landed the avoided faults and the sound rate.

## Competing answers that survived
Reported by the thread, none flips the main call:
- Alpha: 0.2 sound zones a season over 143 zones is 1/715, the literal terms 3(b) reading. Reading the budget over only the sound zones gives about 1/500 and the same 11 zones. The main session has since asserted this in checks.py (SF7, 200 checks, 0 FAIL): any sound-zone count from 60 to 143 leaves the same 11, because the threshold stays between 9.4e-5 and 3.6e-3. No input file and no graded figure changed.
- Restoration method for lost months (zone, feeder or network rate): the thread judged the alternatives inside the 4% and 120 to 138 bands but did not run them to completion.
- Fault grouping window and stroke window (the thread used 30 s and -0.5/+0.2 s): any window from 0.3 to 2 s gives the same matches.
- The referral list carries no band, so it is an exact set; its robustness is the 2.6x margin each side and the zone-level evidence.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 12 | yes |
| File categories | 2 or more | spreadsheet (4 xlsx), text (5 csv, pdf, docx), code/spatial (geojson) | yes |
| Large messy CSVs | one of 20,000 rows or more, one of 10 to 20 printed pages | strokes 250,565 rows; recloser downloads 133,973 and SCADA 63,558 rows; OMS 4,537 rows (about 90 pages) | yes |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | 3 (raingauge, materials quotation, transformer replacements), `labelled_in_pack` recorded outside the ZIP | yes |
| Distractors unused yet weighable | each | the thread did not use any as a result carrier; the three are relevant on their face and the metadata gives a shipped reason for each | yes |
| Deliverables | 1 to 3, all in the golden | 2 (CSV and docx), golden.zip holds exactly those two | yes |
| Asks multi-dimensional, units stated, no rounding dictated | yes | the prompt dictates no rounding; asks span 143 zones, five seasons and four quantities | yes |
| Answer shape | one of the fourteen, 4 or more checkable results | monitoring rule with its alert count (with a flagged set and its false-alarm rate); 10 graded results | yes |
| Reads as real work, not LLM generated | yes | thread found no authoring leakage and no temporal incoherence; the golden file stamps (2026-11-16 and 17) sat after the report date; the generator is moving them and the note's printed date to 9 and 10 November 2026 (after the 4 November pull, before today), which rebuilds golden.zip only, with target.zip and every figure unchanged | yes, with that check |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The note's `## Hidden factor record` lists four factors (zone level on all 143 zones, radio-less clock drift on 32, memory overwrite on 18 and unread tails on all 32, failures beginning partway across the network), each marked as spread across the network and as modelling. These agree: nothing planted sits only in the deciding units, and the thread found no sole defect. The thread's borderline note that the clock/memory sentence touches several results agrees with the note's R1, R2, R4, R7 dependencies on R1.

## Stump power (Gate F)
The thread's grades: quick 2 of 10, careful 5 of 10, thorough 10 of 10. A quick pass (naive matching, no clock fix, plain regression) gets the 2022 to 2025 totals and the sound expectation. A hurried careful run likely loses the 2026 total (about 607 against 655), the failed-protection count (about 135 against 186) and the referral set (10 to 13 zones including BGS-F3). The thread reached 2022 to 2025 by the field's standard method with no judgment the data had to settle; those totals are results the runs will earn.

## Findings, ranked
1. Gate H effort pricing. The thread's careful column is 5 of 10 where the note's table prices it at 2.5 of 7 (about 36 per cent) and its quick pass at 0. A careful level at half the results is above a third and is the finding most likely to be sent back; the main thread should weigh it against the note's effort test, remembering the thread's own first pass did not restore lost months or learn a zone level and still landed about 3 of 10.
2. Gate H one_fact. The thread's best single sentence ("the read-on-site recloser clocks drift between visits and their memories lost or have not yet been read months") rescues about 4 of 10 (network faults, failed-protection count, avoided faults, CSV season columns), against the note's `Largest single hint` of 2 of 7 (29 per cent) for the zone-level sentence. Above a third by the thread's count, though the model-work results (list, budget, zone level, back-test) stay unrescued. The thread also called `one_thing: none`, borderline.
3. Band consistency: the bands agree across the note and the blocks (failed-protection count 186, 170 to 200; avoided faults 116, 104 to 128). The earlier 158 to 214 and 99 to 133 were architecture 3 revision 1's p3 bands and are not in these blocks. The bands separate the hurried figures (135 and 66 to 92) from the golden.
4. The referral set has no band; open fork (4) above. The 2.6x margin and the thread's persistence test close it.
5. The restoration size was not pinned independently by the thread; its reproduction is the open item behind the 2026 totals.

## Next action for the author
Weigh Gate H findings 1 and 2 against the effort test (careful column at 5 of 10 and one_fact at about 4 of 10 by the thread's count), then proceed to stage 5 if the main thread judges the estimate pessimistic given the thread's unrestored first pass; no input file needs changing for determinism.
