# Determinism check, task25, pass 2

**Verdict:** DETERMINISTIC (one soft spot on the slowest-rank overheads, below).
**Disposition:** APPROVE. Optional FIX_NOW in the blocks (see Fix).

## Evidence

| Item | Blocks | Recomputed | Result |
|---|---|---|---|
| 2026 GPU-days held (CAR s.6, registry, running run to 1 Nov) | 1,505,010 (A 236,323, B 1,268,687) | 1,505,009.8 (A 236,323, B 1,268,687) | reproduced |
| Benchmark days (tokens/(tps x GPUs)/86400) | 38.5, 78.8, 62.0, 30.96, 17.10, 7.97 | 38.5, 78.8, 62.0, 30.97, 17.10, 7.97 | reproduced |
| Hall B draw line (node_states x hall_it_load, Helsinki to UTC) | 1,612 kW + 8.32 kW/node | 1,610-1,617 and 8.31-8.32 for clear thresholds 7,500 to 8,050 kW or allocated <650/700/740; quadratic gives the same excess | reproduced |
| Pool busy nodes, reserved held per node_allocations (strings parsed properly) | 227 at 512 reserved; none at 800 (at most 12); 0.446 light share | 227 at 496-528 (n=35k); about 3 at 704-768; about 0 at 832-896 (n=2.6k, max 0); light share 0.45 (0.449 in 192-256, 0.444 in 448-512) | reproduced; the back-off is measured, not extrapolated |
| Pod penalty 22.0% | kide-34b-v1b, v2, 70b-v1-r3 | 0.816, 0.837, 0.832 of benchmark vs 1.025 and 1.007 for one-pod runs: about 1.22 | reproduced; "pod" is named in work_orders (pod 2, both pods) and node names p1/p2 |
| Slowest-rank overhead (stream replay, 1.324) | 31.3 / 48.1 / 57.7 | 35 / 48.5 / 63 (my quick Monte Carlo) | see the soft spot |

### (a) Throttle on hall B

I rebuilt the draw and the response and replayed the 2027 hall B timeline. The timeline uses the roadmap's blocks, extended to each run's finish. It is 800 nodes from Feb 1, 768 from Mar 15, 896 from Mar 29, then falling. The pool is none at those levels, as measured. The inputs to the replay are the Step-by-Step's pre-throttle days plus the golden's post-throttle items.

Step stretch against excess from the 2026 capped days, measured against each run's own clear-step baseline, is clearly piecewise-linear:

| Excess (kW) | Stretch |
|---|---|
| 100-200 | 2.0% |
| 300-500 | 5.3% |
| 800-1200 | 12.5% |
| 1200-2000 | 32% |

I ran six forms. Shifts are against the golden's expected days.

| Form | 120b | v3 | 8b-v4 | 16k | 13b-v4 | Late set (hall B) |
|---|---|---|---|---|---|---|
| Binned response, contract 8,100 | -0.6 | -0.15 | -0.6 | -0.4 | -0.4 | 120b, 8b-v4, 16k |
| Binned response, contract at the meter ceiling 8,089 | -0.45 | -0.11 | -0.46 | -0.21 | -0.22 | same |
| Physical cap, draw/contract-1 | -0.21 | +0.02 | -0.23 | -0.10 | -0.11 | same |
| Physical cap, contract 8,089 | -0.12 | +0.07 | -0.14 | -0.07 | -0.07 | same |
| Linear in kW through the origin (1.53e-4 per kW) | +0.63 | +0.19 | +0.54 | +0.60 | +0.59 | same |
| Linear in excess/draw through the origin (k 1.47) | +1.00 | +0.34 | +0.89 | +0.81 | +0.80 | same |

- **Largest shift:** +1.0 day on kide-120b-v1, in the worst rival form. That is 1.2% of 85.5, well inside the 3% band.
- **Finish date:** the date can move by one day in that rival, which is the edge of the "within one day" band.
- **That rival is not careful:** it overstates the stretch at small excess (3.0% against a measured 2.0% in the 100-200 kW bin), so a competent analyst who looks at the curve rejects it.
- **Fits and late set:** kide-34b-v3 stays inside its window (36.1 to 36.6 against 38) and kide-13b-v4 inside (33.9 to 35.1 against 40). The hall B late set never changes. Margins are 120b +10.5, 8b-v4 +4.5, 16k +7.8 days.
- **16k and the May 17 works:** its finish stays before the May 17 06:00 local works start, about 1.4 days clear, so the 4-day major-works add does not apply.
- **Rival ruled out:** the pool at its 2026 mean share (about 0.40 of the free nodes, about 90 nodes at 800 reserved) would flip v3. The rows ruling it out are the 704-768 and 832-896 reserved bins, where the pool is about 0 (n over 7,700). The author's own rival list already carries this one.

### (b) H1 2027 feasibility, hall B

Every pair of blocks was checked from the roadmap rows against CAR s.2.

| Pair | Verdict |
|---|---|
| kide-34b-v3 rows p1 r01-08 with kide-13b-v4 (r01-04, from Mar 29) | the only overlap in rows; v3 finishes about Mar 9 (window Mar 11), 18+ days clear |
| kide-34b-v3 with kide-13b-lc32 (r05-06, from May 3) and kide-8b-lc64 (r07, from May 24) | same, long clear |
| All other hall B blocks, and the whole of hall A (including the extensions of 120b to Apr 27, 8b-v4 to Apr 21, 16k to May 15, sci to May 4) | disjoint rows, nothing booked on extended nodes |

- **No block is over-booked, and no launch is delayed.** Node counts match: the blocks are 480 / 256 / 224 / 64 / 128 / 64 / 32 nodes, with at most 896 nodes concurrent, below 1,024.
- **Silent rules, same call under both readings:** whether backfill nodes of a finished run still count towards the draw (I counted them as allocated), and what happens if a prior run overruns into the next block. Neither bites, because v3 has 18+ days of slack.
- **Hall B total reserved** is 800 on Feb 1, as the blocks state.

### Other checks

- **Asks:** each pins its unit (days, per-cent, GPU-days) and one answer. CAR s.4 files "days from window start", and s.2 and s.3 file the extension and finish rules.
- **Filed facts:** contract (S-3 table), the works list, the overrun history in work_orders, the pod names, the pool and the benchmark table are all in shipped files, extracted properly from PDF and CSV. The prompt's "H1 2027 runs" and "windows" appear in the roadmap.

### Soft spot (not a flip)

My quick Monte Carlo of the slowest-rank overhead gives 35.2 / 48.5 / 63.3 against 31.3 / 48.1 / 57.7 on kide-13b-code-lc32, kide-34b-lc64 and kide-8b-lc64. That is up to 5.6 points off on the 8b run. My replica is not the golden's stream (my document draw and rank layout are guesses). It reaches about +0.5 day on kide-8b-lc64, which is the 3% edge of 15.3. No late-or-fit call flips: 13b-code-lc32 stays late (1.0 day), 8b-lc64 late by 2.3 or more, 34b-lc64 late by 2.2. The blocks' "within 3 points" band on the overheads could fail an honest solver on the 8b-lc64 value.

## Fix

Where: solution only, optional. Widen the overhead tolerance on kide-8b-lc64 and kide-13b-code-lc32 to about 6 points, and state the expected-days tolerance for kide-8b-lc64 as 5% (15.3 +/- 0.8). No prompt or pack change is needed.
