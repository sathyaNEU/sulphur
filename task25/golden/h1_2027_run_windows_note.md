# Seven H1 2027 runs will not finish inside their windows

To: compute committee (Esa Airaksinen). From: Pia Kuosmanen, training infrastructure. 6 November 2026. Before the H1 2027 windows are locked.

These will not reach their token budgets inside their windows (expected days against window days):

- kide-13b-code-lc32: 8.0 against 7, 1.0 days past its window, finishing about 2027-01-26
- kide-120b-v1: 86.2 against 75, 11.2 days past its window, finishing about 2027-04-28
- kide-34b-v3: 43.8 against 38, 5.8 days past its window, finishing about 2027-03-16
- kide-34b-16k: 62.1 against 54, 8.1 days past its window, finishing about 2027-04-25
- kide-34b-lc64: 14.9 against 13, 1.9 days past its window, finishing about 2027-03-15
- kide-34b-sci: 23.0 against 20, 3.0 days past its window, finishing about 2027-05-04
- kide-8b-lc64: 15.1 against 13, 2.1 days past its window, finishing about 2027-05-25

These fit: kide-70b-v2 (39.5 days against 47); kide-8b-v4 (63.0 days against 75); kide-13b-v4 (33.6 days against 40); kide-13b-lc32 (10.1 days against 12).

Every window was sized on the throughput benchmark, and the benchmark runs at conditions none of these runs will see. Three things make up most of the gap.

1. **The step waits for the slowest rank.** Attention cost grows with the square of each document's length, and each step ends when the data-parallel rank holding the longest documents finishes. With one or two sequences per rank the slowest rank runs 31.3, 48.1 and 57.8 per cent over the mean rank for kide-13b-code-lc32, kide-34b-lc64 and kide-8b-lc64. The 2026 extension runs ran four sequences per rank on lighter mixes and never showed this.
2. **The scientific run pads.** Best-fit packing that keeps each paper whole fills 79.5 per cent of each 16k sequence on the kide-34b-sci mix, so the run needs 4.7 more days for the same real tokens.
3. **Hall B is held to its contract.** With the February to April reservations hall B would draw up to 23 per cent past its 8,100 kW contract, and the provider holds it there by lowering GPU power, which on 2026's 39 capped days stretched every hall B job's steps (27.0 per cent at 20 per cent over). That adds 13.5, 7.5 and 11.2 days to kide-120b-v1, kide-34b-v3 and kide-34b-16k.

Works matter at the margin: in 2025 and 2026 major works ran 1.99 times their planned hours, so the hall A re-cabling in March and the hall B chilled-water work in May cost kide-34b-lc64 and kide-8b-lc64 3.1 and 4.5 days, about twice what the notice's planned hours imply.

**What I would change before the windows lock.** Extend each late window to its expected days, or remove the cause. For the three long-context runs, deal sequences to ranks by their attention cost rather than in turn. For kide-34b-sci, let papers split across sequences. For hall B, take enough load out of February to April to keep it under contract, for example by moving kide-8b-v4 to hall A after kide-70b-v2.

2026 bears this out: the runs held 1,332,946 GPU-days against the 1,250,323 their benchmarks implied. Waiting for the slowest rank added 60,137, interruptions and restarts 27,131, hall B's cap 21,024 and provider works 18,900; shorter documents than the benchmark's corpus gave back 42,558. The workbook has every run's bridge and range.

Days are counted from 00:00 UTC on each window's start, as CAR-2027-1 counts them, and every late block is kept until its run finishes, which is what keeps hall B loaded into April. The ranges in the workbook are four-in-five ranges from the 2026 record's own spread.
