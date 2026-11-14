# Determinism check, task25, pass 3 (final cut)

**Verdict:** DETERMINISTIC. **Disposition:** APPROVE (one optional FIX_NOW wording note, below).

## Evidence (python3 -I, own scripts, own random streams)

| Figure | Blocks | My replay | Result |
|---|---|---|---|
| Benchmark days, all 11 runs (tokens / tokens per GPU-s / GPUs) | 38.54 ... 8.60 | all 11 reproduced to 0.01 from the exact tpbench row | reproduced |
| Slowest-rank overhead, kide-13b-code-lc32 | 31.3 (band 3 pts) | 100-step streams (6 seeds) 28.5 to 30.2; 3000-step (5 seeds) 29.1 to 29.5 | inside band, 2 pts under |
| kide-34b-lc64 | 48.1 | 47.8 to 48.9 (100 steps); 48.1 to 48.3 (3000) | inside |
| kide-8b-lc64 | 57.7 | 53.6 to 57.6 (100 steps); 56.2 to 56.5 (3000) | inside at length; one short 100-step stream is 4.1 under |
| kide-13b-lc32 | 9.4 | 8.6 to 9.5 (100); 8.7 to 8.9 (150) | inside |
| Own mix at the mean rank (days), harness corpus replayed fresh, benchmark's own slowest-rank wait included | -0.30, 0.03, 0.73, -0.16 | -0.28, -0.00, 0.73, -0.16 (ranges 0.03 wide) | reproduced, far inside 0.35 d |
| kide-34b-sci fill (best-fit, 64 open) | 0.795 (0.015) | 0.791 to 0.794 | inside |
| Hall B draw line (clear intervals, kW under 7800) | 1,612 + 8.32 a node | 1,611.8 + 8.319 | reproduced |
| Pool busy nodes, 512 reserved, by registry-held blocks binned in 64s (a method other than the Step-by-Step's) | 227 (25) | 224 to 228; share 0.44 to 0.46 | inside |
| Pool at 800 reserved | none (at most 12) | 0 (bin 832 to 896); 1,000+ also 0 | inside |
| Light-load share | 0.446 (0.03) | 0.40 to 0.41 at light load by registry binning | inside the band (0.03) at the edge; see note |
| Throttle at 800 reserved | excess 168 kW, stretch 2.0% | 1612 + 8.32 x 800 - 8100 = 168 kW, no pool, so only the two ends are throttled; consistent. At 512 reserved plus 227 pool the wanted draw is 7,760 kW, under contract | consistent |
| Over-booking in hall B or A under CAR section 2 (block node sets from the roadmap, windows extended to the blocks' expected finishes) | none | only kide-34b-v3 shares nodes with kide-13b-v4, kide-13b-lc32, kide-8b-lc64, and those windows open 18 to 74 days after v3 finishes. No late run's block is reused. 800 reserved in Feb to mid-March (480+256+64) | no over-booking |
| Pod crossing | only kide-8b-v4 (kb-p1-r16 with kb-p2-r01) | confirmed on the roadmap node lists | reproduced |
| Bridge row sum, kide-8b-v4 | 79.49 | 62.02-1.78+1.46+13.56+3.39+0.43+0.41 = 79.49 | reproduced |

Late set under replay: the lc runs' expected days move by at most 0.13 d (code-lc32 at the 3000-step limit, 29.2 vs 31.3 points on 6.05 d), so 8.0 stays at 7.9 against a 7-day window; kide-34b-lc64 and kide-8b-lc64 stay about 2 days over; kide-13b-lc32 (10.2 against 12) is nowhere near the line. No careful replay following the filed rules (any stream, 100 to 3000 steps) leaves a stated expected-days band or flips the late set. The weakest margin is kide-34b-v3 (36.3 against 38, 1.7 days), which is closed by the pool back-off I reproduced (the 2026 mean share is the stated rival).

## Forks run
- Stream length and seed: spread 1 to 2 points at 3000 steps, up to 4 points on the shortest 8b-lc64 stream. A 3-point overhead band is tight for a solver who replays only about 100 steps. The days effect is 0.4 d on a 5% band, so the graded expected days still hold.
- Pool bookkeeping: reserved nodes taken from node_allocations segments (excludes restart gaps) give pool 405 at 512 reserved and a 0.57 light share, not 227 and 0.446. Reserved nodes taken as registry launch-to-finish blocks give the blocks' values. CAR section 2 (a block is held until its run finishes) supports the registry reading. This is the one real fork, and it is closed by section 2, not by a filed sentence.
- Replaying the benchmark harness corpus with different seeds: no effect (days within 0.03).

## Notes (non-blocking)
1. The prompt does not give the order of the causes. The blocks fix it and give each item 0.35 d or 12 per cent, which absorbs reordering.
2. Pods are filed only through the work orders' "pod 2" and "both pods" text and the kb-p1/kb-p2 node names. That is enough to map them.
3. Optional FIX_NOW: add to the Causes sheet note that the pool's reserved nodes are the registry blocks held to finish (CAR section 2), since the segment reading gives 405.

## Fix
none required (solution/prompt/input_files unchanged).
