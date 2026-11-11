# determinism-check report, task20, 2026-11-11

Thread: one general-purpose sonnet/medium judge, scratch /tmp/determinism-check-task20-r1/ (verdict.md, own_derivation.md, work/). The thread kept the order (prompt only, own derivation written, then graded_blocks.md). My runtime had no Agent tool, so the main session spawned it from my brief.

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer / underspecified_objective on one result family, the MRS-4 4(d) volatility rescaling). SOLUTION_WRONG does not apply: every other figure reproduces.
**Disposition:** FIX_NOW (band route, no pack change, one re-judge). If the author pins the EWMA timing inside MRS-4 instead, it becomes SEND_BACK with a rebuild and rerun.
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
MRS-4 4(d) says only "rescaled by the ratio of the current to the then-current exponentially weighted volatility (decay factor between 0.94 and 0.97)". Read literally (EWMA through the run date over EWMA through the scenario date, same convention), the sound model shows 3 exceptions (6 Sep 2024, 14 Feb 2025, 28 Mar 2025) at every decay 0.94 to 0.97, portfolio or name by name. That gives (d)=1 (6 May 2025) and (e)=2 (14 Feb, 28 Mar). The golden's 2 / (d)=2 / (e)=1 appears only under a forecast-style lag (scenario-date EWMA lagged one day) at portfolio level, decay 0.94. The golden's own bands (sound 0 to 2, (d) 2 to 3, (e) 0 to 1) exclude the literal reading, and fork SF7 closes decay and level only, not timing. Green and "14 against the model" hold under every variant. Affected: the Final Recommendation ("a sound model shows 2"), ask 1 rows 14 Feb and 28 Mar, ask 3, Step 6, the closing paragraph.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| ERE VaR, all 251 run-log runs | to the dollar | within 0.5 USD | Y |
| Published betas | 950 | OLS on 250 days, 3 dp | Y |
| Book held (extract + blotter bookings after cut) vs PC hypothetical | - | max diff 0.5 USD, 250 days | Y |
| Exceptions | 19 (15 booked, 18 hyp.) | 19 / 15 / 18 (14 on both); 4 hidden on booked; 3 Apr booked only | Y |
| (a) 1, (b) 4, (c) 11 and dates | as filed | same dates | Y |
| (d) / (e) | 2 / 1 | 1 / 2 literal | N |
| Against the model | 14 | 14 | Y |
| Stale-extract runs, 2 exceptions not theirs | 27; 4 Nov, 5 Feb | 27; ERE on held book 2.100M vs 2.223M and 1.189M vs 1.521M | Y |
| Median missing allocation gross | 39.2M | 39.16M | Y |
| "VaR too high on 129 runs" | 129 | 133 of 250 (132 of 249) | N (wording) |
| Sound count | 2, green | 3, green (literal) | N |
| Count with no volatility response | 3 | 3 | Y |
| Proxy counts Jul to Dec | 87, 82, 80, 73, 72, 67 | same | Y |
| Add-on Jul to Dec (USD m) | 0.32, 0.27, 0.11, 0.08, 0.03, 0.00 | 0.324, 0.273, 0.114, 0.076, 0.035, 0.000 | Y (inside bands) |
| 30 June mapping under plan ramp | 0.32, 0.28, 0.25, 0.30, 0.40, 0.40 | same | Y |

## Competing answers that survived
1. EWMA timing in 4(d): literal symmetric gives sound 3, (d)=1, (e)=2; lag gives sound 0 to 2, (d) 2 to 3, (e) 0 to 1. Not closed in MRS-4 or the engine note. Also, seeding the EWMA at the window start flips 14 Feb at decay 0.94 (0.994 of the loss with a full-history seed, 1.002 seeded at the window start).
2. Add-on base book: the plan says "as the desk held them in the risk engine's 30 June run". Literal is the extract the engine read (golden). A solver who has found the missed allocations can defensibly use the true 30 June book: 0.34, 0.42, 0.41, 0.36, 0.13, 0.14, outside the bands from August. Closed only by reading "run" literally; minor to moderate.
3. 6 Sep 2024 is (c) by a 1.4% margin (own-history 3.149M vs loss 3.106M). No estimation freedom ("as ERE computes it"), so thin but clean.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 20 files; csv 16, xlsx 3, pdf 2 (spreadsheet and text) | Y |
| Large messy CSVs | 20,000 rows and a 10 to 20 page one | vendor closes 147,250 rows, blotter 35,017, eqx v1 22,571 | Y |
| Distractors in metadata.json only | 2+ | 3 (weekly stress, GL journal, var limit utilisation); none labelled in the ZIP | Y |
| Distractors unused yet weighty | - | GL agrees with PC booked to the dollar and the stress file prices fixed shocks; no result needs them | Y |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in the answer blocks | Y |
| Asks multi-dimensional, units stated, no rounding dictated | - | prompt dictates none | Y |
| Answer shape, 4+ checkable results | one of fourteen | allocation-free classification with add-on schedule (flagged set with attribution and a month-by-month forecast); 9 results | Y |
| Realism / LLM tell | - | not examined beyond the thread's hygiene notes (no authoring disclosure found) | Y |
Hygiene notes from the thread: the business plan is "prepared 24 June, approved 27 June" yet cites the 30 June run and closes; v2 extracts and TH ids start 17 Jan 2025 while the crosswalk is "effective 2025-01-18"; 380 exact duplicate vendor rows on two dates (realistic mess). None is exclusion-level.

## Own first-pass figures against the stated bands
Source: own_derivation.md (written before graded_blocks.md was opened). Result IDs per the design note's Results chain.

| Result | Thread's own first-pass figure | Stated golden / band | Inside |
|---|---|---|---|
| R1 exceptions | 19 (15 booked, 18 hypothetical, 14 both) | 19, exact | Y |
| R2 stale-extract runs | 27 warning runs; 4 Nov 2024 and 5 Feb 2025 classified (c), not inputs | 27, the 2 not theirs, exact | Y |
| R3 inputs | 4: 2 Aug, 5 Aug, 23 Oct 2024, 4 Mar 2025 | 4, same dates, exact | Y |
| R4 risks not in model | 11, same dates (6 Sep margin 1.4%) | 11, exact | Y |
| R5 volatility / sound / zone | (d)=1 (6 May only); sound count 3 (6 Sep, 14 Feb, 28 Mar), same at decay 0.94 to 0.97; green. Lag reading: 0 corrected, 14 Feb and 28 Mar become (d). (The verdict also gives 2 under lag at portfolio, 0.94.) | (d) 2 to 3; sound 0 to 2; zone exact | N on (d) and count (literal); zone Y |
| R6 heading rows | 17 of 19 rows as golden; 28 Mar 2025 (e) not (d); counts a1 b4 c11 d1 e2 | per row exact; 14 Feb and 28 Mar may move (d)/(e); (d) 2 to 3, (e) 0 to 1 | rows Y, counts N |
| R7 July add-on | 324,155 (true-book alternative 341K) | 0.32, band 0.24 to 0.34 | Y (alternative at the edge) |
| R8 Aug to Dec add-on | 272,556; 113,888; 75,888; 34,604; 0 (rounding rivals: Oct 76 to 94K, Nov 22 to 35K; true-book alternative 423K, 414K, 361K, 132K, 143K; 30 June mapping 284K, 247K, 297K, 401K, 401K) | 0.27 (0.25 to 0.31), 0.11 (0.09 to 0.13), 0.08 (0.06 to 0.10), 0.03 (0.01 to 0.05), 0.00 (0 to 0.02) | golden route Y; rounding rivals Y; true-book alternative N from Aug |
| R9 call | 14 of 19 against the model; 4 inputs; sound 3, green; add-on 0.324 falling to 0 | 14; 4; sound 2, green; 0.32 to nil | 14, 4, green, add-on Y; sound count N |

Proxy counts 87, 82, 80, 73, 72, 67 are not in own_derivation.md; the thread confirmed them in the verdict.

Pricing note: the 30 June-mapping shortcut gives 0.284 for August, which sits inside August's band (0.25 to 0.31), so August alone does not separate the shortcut from the golden; September onward do (0.25, 0.30, 0.40, 0.40 against bands that stop at 0.13, 0.10, 0.05, 0.02).

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The note's Hidden factor record agrees: five factors, all process-generated across every run or quarter (closing allocations on 249 of 249 runs, proxies every quarter, store graduations monthly), none only in the deciding units. The thread finds `one_thing: none`, matching the note. The note's "too high on 129 runs" is wrong (133 of 250); the claim sits in the Hidden factor record and ask 2; correct it in both. The thread did not name a declared distractor as carrying a result.

## Gate H
domain: pass; layers: pass; results: 9 graded across 6 areas; one_thing: none; effort: quick 2, careful 5, thorough 8 of 9 (note: 0, 4.5, 9); one_fact: "ERE reads its extract before the closing-auction allocations are booked" rescues 3 of 9 (R3, R4, R6), matching the note's `Largest single hint:` (3 of 9). The thread's quick pass is 2 against the note's 0, a small gap (R1 and R2 are one look); the careful grades agree. Carefully but hurried, the thread loses R3, R4, R8, R9 as the note predicts.

## Stump power (Gate F)
Strong and spread over ask 1 rows, ask 2, ask 3 and ask 4. A hurried run files the official 15 and red, blames the 27 reused-extract runs (16 against the model), and holds the add-on flat or on the plan ramp. Results a careful run earns by the field's standard method (priced into the careful column): R1 (both P&Ls), R2 (read the run log), R5's zone, R7 (build the plan's book). The ERE replication to the dollar is the thread's first step and a self-confirming check for runs that stop there.

## Findings, ranked
1. EWMA timing fork in 4(d) (above). The golden's sound count, (d) and (e) counts sit on one of two defensible readings and the stated bands exclude the other.
2. "129 runs" is wrong; 133 of 250.
3. Add-on base-book wording ("the desk held ... in the engine's 30 June run") leaves the true-book reading open from August.
4. August band contains the 30 June-mapping shortcut (0.284 in 0.25 to 0.31).
5. Plan dated 24/27 June but cites 30 June data; crosswalk "effective 18 Jan" against 17 Jan v2 extract start.

## Next action for the author
Widen the answer blocks to the literal reading: sound model "2 to 3, green", (d) 1 to 3 and (e) 0 to 2 with 14 against the model unchanged, 14 Feb and 28 Mar as movable rows, add the symmetric reading to the Routes sheet and SF7; correct 129 to 133 of 250; add "the positions the engine read on 30 June" to the plan's Basis sheet or the fork table; narrow August's band or accept that August does not discriminate. Then re-judge once. If one count is wanted, pin the EWMA timing in MRS-4 4(d), which changes the pack and needs a rebuild.
