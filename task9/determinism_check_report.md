# task9 determinism check (Gates A to E)

Read: `prompt.txt`, the four answer blocks of `submission.md`, and `target.zip` unzipped fresh to
`/tmp/determinism-task9-1795363402/target/` (29 files: 23 CSV, 1 JSONL, 3 XLSX, 2 PDF). Nothing else of the build was opened.

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW. One sentence goes into Step-by-Step step 5: where the 2027 pinned-view lag clock starts. Solvers see nothing new, so no rerun is needed.

## Why

The call is forced. Each placement holds under every defensible rival I ran, and every rival that crosses a line (5.5 or 8) is ruled out by a figure computed from the shipped files.

- **Label revisions, 9.98:** sits 2 points above the 8 line on every route.
- **Retunes, 4.47:** sits 1 point under the 5.5 line on every route.
- **Optimisation noise, 6.89:** the admitted variants run from 6.15 to 7.02.
- **Feature releases, 6.65:** the consistent clocks run from 6.44 to 6.71.
- **Training data, 6.62:** the variants run from 6.54 to 6.76.

There is one gap in the blocks. To reproduce 55.0 per cent pinned, I had to choose where the 2027 lag clock starts. The 2027 calendar rows carry no `completed_on`, and the Step-by-Step never says the origin is the planned week plus the past rollouts' mean slip of 1.5 weeks.

A solver who fits the lag from completion dates and then starts it at the bare planned week, with no reverts, gets:
- 59.8 to 60.4 per cent pinned (band top 60.0);
- feature releases at 6.25 to 6.29 points (band floor 6.34);
- a feature-release share of 15.6 to 15.8 per cent (band floor 16.3).

The call does not move (feature releases stay in a plan), and the calendar's own dates refute that route (see the fork list). It is still the "which of two dates starts a clock" case, so the missing sentence is a FIX_NOW.

## Evidence: figures recomputed by the blocks' own method

| Figure | Blocks (band) | Recomputed | Note |
|---|---|---|---|
| Panel merchants / identifiers / merchant-weeks | 29,580 / 34,148 / 3,360,865 | 29,580 / 34,148 / 3,360,865 | Kept the later load; mapped IDs through the Tolka migration file |
| Manifest lines / runs / production | 2,473 / 2,464 / 1,764 | 2,473 / 2,464 / 1,764 | |
| Pair register (by kind) | 644 (84/56/168/224/112) | same | |
| Bootstrap, replicate pair variance | 259.89, 12.73 pt² | 260.12, 12.74 | 0.1% high; I found no rule that closes the gap. Moves nothing |
| Retunes | 4.47 (4.41 to 4.52) | 4.47 | 13/4 retunes per pair; the log shows 15 per family in 60 weeks |
| Label revisions | 9.98 (9.92 to 10.05) | 9.987 | Prints as 9.99; inside the band |
| Training data at face (net of seed) | 15.72 | 15.73 | |
| **Training data, 2027 (CC1)** | **6.62 (6.35 to 7.44)** | **6.615** | Formula: s²(1/N1 + 1/N2 - 2S/(N1·N2)); s² = (bootstrap - replicate)·N/2; windows from the manifests; rows from the warehouse plus the plan |
| Replicate at face | 3.57 | 3.57 | |
| Persistence p by family | 0.79 to 0.95 | 0.7925 to 0.9475 | |
| **Optimisation noise (CC2)** | **6.89 (6.05 to 7.40)** | **6.890** | Exact reproduction of the stated fit |
| Free fit / implied replicate | 8.77 / 17.44 | 8.77 / 17.44 | |
| Line through gaps 8 to 26 / 13 × replicate | 5.96 / 12.87 | 5.96 / 12.87 | |
| Rollouts: count, lag range, median, reverts | 42; 3 to 31 weeks; median 14; 4.4% | 42; 3 to 31; median 14; 4.40% | Median 14 counts lag in whole refreshes (fractional median 13.4) |
| Fitted lag at 0 and 5 components | 6.3 and 28.8 weeks | 6.31 and 28.76 | |
| Pinned share at planned weeks / completed dates | 90.9 / 87.1 | 90.93 / 87.09 | "Completed dates" = planned week + mean slip 1.52 weeks |
| **Pinned share (CC3)** | **55.0 (53.2 to 60.0)** | **54.5 to 55.1** | Needs the planned week + 1.52-week origin (see Fix) |
| Feature releases: model / planned / completed | 6.65 / 4.00 / 4.46 | 6.655 / 4.001 / 4.457 | |
| Record mean-square change: 13 weeks / 1 week | 509.15 / 42.34 | 509.15 / 42.34 | |
| Step 7 check: this assessment / face value | 42.23 / 279.06 | 42.29 / 281.3 | Face value overshoots the record about 6.6 times |
| Shares of model-side movement (L/O/F/T/R) | 39.1 / 18.6 / 17.3 / 17.2 / 7.8 | 39.07 / 18.60 / 17.35 / 17.14 / 7.84 | All inside their bands |
| Merchants' own share | 43.9 (41.9 to 46.7) | 44.3 | 2026's three closed pairs alone: 42.7 (blocks 43.7) |
| Own share of the record's movement | 39.2 | 39.9 | A refused figure; I did not chase the last 0.7 |
| 2026 panel tier-change rate | 14.8 | 14.82 | Covenant monitor file and the panel agree |
| Tier changes 2027 / with plan and escalation sources removed | 14.0 (13.7 to 14.6) / 9.7 (9.4 to 10.3) | 14.05 / 9.80 | |

The figures agree across all four blocks: every number in the Final Recommendation appears identically in Supplementary Questions 1, CC1 and CC2, and steps 3 to 5.

## Forks run (Gate C)

| # | Choice | Alternative(s) | Result | Ruling |
|---|---|---|---|---|
| 1 | Settled-week start for the gap fit | No floor; first warm retrain after the last cold one; the last rollout's first use; floor only; 2026 only | Optimisation noise 6.15 to 7.02 (weighted and flat) | Inside the band |
| 2 | Gap range | 20 / 26 / 30 gaps | 6.85 / 6.89 / 6.94 | Inside |
| 3 | Gap weights | Flat in place of inverse square | 7.00 | Inside |
| 4 | Replicate constraint (strongest rival) | Free A and b | 8.77, escalation | **Ruled out:** the fit implies replicate pairs of 17.44 against 12.74 measured in the pair file |
| 5 | Persistence p → 1 (random walk) | Noise adds 13 × half a replicate pair | 9.10, escalation (12.87 if double counted) | **Ruled out:** at p = 0.985 the weighted error is 2.7 (GAME) to 90 (TRVL) times the best fit, above it in every family, and D(26)/2D(13) is 0.90 to 0.985, so the record is not linear |
| 6 | Straight line through late gaps | Intercept of the line from gap 8 to 26 | 5.96 (plan, below the 6.05 floor) | **Ruled out:** the intercept climbs as the start gap moves out (gap 4: 5.21, gap 8: 5.96, gap 12: 6.60, gap 16: 7.14, gap 20: 7.50), so the curve has not reached its ceiling |
| 7 | Training-data noise per row | Not net of replicate; family average; latest bootstrap week; planned book | 6.76 / 6.62 / 6.60 / 6.54 | Inside |
| 8 | Bootstrap read as the movement | Face value | 15.72, escalation | **Ruled out:** the manifests' 52- and 104-week windows share all but 13 weeks in and 13 out; the face-value route predicts gap-1 change of 281 against 42.34 in the record |
| 9 | Pinned-view lag: form and pooling | Log-linear, linear, plug-in median, per-family mean lag (each with slip and reverts) | 54.5 to 57.0 pinned; feature releases 6.47 to 6.71 | Inside |
| 10 | Pinned-view clock (strongest clean neighbour) | Refit lag from planned week to first use, apply from the 2027 planned week | 55.07 pinned (57.60 without reverts); feature releases 6.655 / 6.44; share 17.35 / 16.43 | Inside, on either revert choice |
| 11 | Pinned-view clock (mixed) | Lag fitted from completion dates, started at the bare 2027 planned week, no reverts (or per-family median lag) | 59.8 to 60.4 pinned; feature releases 6.25 to 6.29; feature-release share 15.6 to 15.8 | Outside three bands; call holds. **Ruled out by the calendar:** past `completed_on` ran 0 to 3.6 weeks after the planned week (mean 1.52, never earlier), so a completion-based lag cannot start at the planned week. The blocks do not state this clock: FIX_NOW |
| 12 | Which retrains count as 2027's | Calendar 2027 (4 Jan to 27 Dec 2027) in place of the snapshot-pair refreshes | 56.8 | Inside |
| 13 | Pinned share weighting | Book-weighted family-weeks | 62.6 to 65.5 | Not a fork: the ask counts retrains (one per family-week), and the blocks say family-weeks |
| 14 | Tier mapping | Gaussian crossing simulation on panel scores, raw and calibrated to 2026 | 14.07 to 14.09 / 9.86 to 9.87 | Inside |
| 15 | Tier scaling linear in variance | 14.8 × mean-square ratio | 13.3 | **Ruled out:** the panel simulation in row 14 gives 14.07, so crossings scale with the root |
| 16 | Merchants' own change basis | Section 5.2's literal 2026 pairs; all 13-week gaps from July 2024 | 42.7 (blocks 43.7) / 49.2 | Pairs inside. July 2024 ruled out: before the settled weeks the manifests show cold 26-week retrains |
| 17 | Feature-release level | Settled-weeks release rate in place of the roadmap | 9.67 | Ruled out: standard section 2.1 makes the roadmap the year's releases |
| 18 | Family weights | Panel weights in place of the 21 Sep 2026 book | Optimisation noise 6.89 | Inside; standard section 3.1 pins the book anyway |

## Filed facts and asks (Gates B, D and E)

**Gate B passes.**
- The standard PDF carries the bands, sources and placements; sections 3.1 and 3.2 define movement, 5.1 the shares, 5.2 merchants' own change, and 6.1 the covenant test.
- Covenant Schedule C carries the tiers, the 12 per cent cap, the 2027 snapshots and the panel.
- The roadmap and the row plan (2027 inputs, including the book sheet) and the calendar (PC-26-058 "Pinned feature views") are filed.
- The windows, warm starts and rollout first-use come from the manifests.
- Every term in the recommendation (escalate, remediation plan, monitor, label revisions, optimisation noise, feature releases, training data, retunes) appears in the standard.

**Gates D and E pass.** Each ask states its unit and its basis:
- points between consecutive quarter-end snapshots, book weighted per the standard;
- per cent of model-side movement, and merchants' own share of all movement;
- per cent of retrains;
- per cent of merchants, against the covenant.

No ask splits on how a word is read.

## Fix

- **Where:** the solution (Step-by-Step step 5 only). Nothing else.
- **What to add**, after "A lag model on custom components carries this to the pinned views:":
  > "each family's 2027 rollout is placed at its planned week plus the past rollouts' mean slip from planned week to completion (1.5 weeks), lags are counted in weekly refreshes from completion to first use and fitted log-linear on custom components with the spread integrated, and 4.4 per cent of on-weeks are netted for reverts;"
- **Bands:** no edit needed. Routes 10 and 11 show every consistent clock lands inside the current pinned, feature-release and share bands.
- **Optional, not blocking:**
  - Step 3 could state the training-data formula in one clause (the row turnover over twice the window, s²(1/N1 + 1/N2 - 2S/(N1·N2))). I rebuilt it from the prose and got 6.615.
  - The pair-variance aggregates (259.89, 12.73) and label revisions (9.98) come out 0.1 per cent higher by the literal method (260.12, 12.74, 9.99). Every figure stays inside its band.
