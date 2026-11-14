# Seven H1 2027 runs will not finish inside their windows

To: compute committee (Esa Airaksinen). From: Pia Kuosmanen, training infrastructure. 6 November 2026. Before the H1 2027 windows are locked.

These will not reach their token budgets inside their windows (expected days against window days):

- kide-13b-code-lc32: 8.0 against 7, 1.0 days past its window, finishing about 2027-01-26
- kide-120b-v1: 85.5 against 75, 10.5 days past its window, finishing about 2027-04-27
- kide-8b-v4: 79.5 against 75, 4.5 days past its window, finishing about 2027-04-21
- kide-34b-lc64: 15.0 against 13, 2.0 days past its window, finishing about 2027-03-15
- kide-34b-16k: 61.8 against 54, 7.8 days past its window, finishing about 2027-05-15
- kide-34b-sci: 23.0 against 20, 3.0 days past its window, finishing about 2027-05-05
- kide-8b-lc64: 14.8 against 13, 1.8 days past its window, finishing about 2027-06-07

These fit: kide-70b-v2 (39.5 days against 47); kide-34b-v3 (36.3 days against 38); kide-13b-v4 (34.3 days against 40); kide-13b-lc32 (10.2 days against 12).

Every window was sized on the throughput benchmark, and the benchmark runs at conditions none of these runs will see. Four things make up most of the gap.

1. **The step waits for the slowest rank.** Attention cost grows with the square of each document's length, and each step ends when the data-parallel rank holding the longest documents finishes. With one or two sequences per rank the slowest rank runs 31.3, 48.1 and 57.7 per cent over the mean rank for kide-13b-code-lc32, kide-34b-lc64 and kide-8b-lc64. The 2026 extension runs ran four sequences per rank on lighter mixes and never showed this.
2. **The scientific run pads.** Best-fit packing that keeps each paper whole fills 79.5 per cent of each 16k sequence on the kide-34b-sci mix, so the run needs 4.7 more days for the same real tokens.
3. **Hall B is held to its contract.** Its jobs' steps stretch when the hall would draw past its 8,100 kW (24.6 per cent at 20 per cent over, on 2026's 123 capped days), and the research pool is what keeps the hall under it: the pool took about 227 of the 512 unreserved nodes in 2026 when the reservations were light and none once they held 768 or more, so in February to mid-March, with 800 nodes reserved, the pool is off and the stretch is small (kide-34b-v3 2.0 per cent), and from the end of March, with 896 reserved and no pool, it is 10.0 per cent on kide-13b-v4. That adds 3.6, 0.7 and 2.9 days to kide-120b-v1, kide-34b-v3 and kide-34b-16k.
4. **A block across both pods runs slower.** The 2026 runs whose nodes sat in both of hall B's pods (kide-34b-v1b, kide-34b-v2, kide-70b-scale, kide-70b-v1-r3) took 22.0 per cent longer per step than their benchmark, mix and width predict, and the runs inside one pod did not. kide-8b-v4's block, kb-p1-r16 and kb-p2-r01 in the roadmap, is the only 2027 booking across the boundary: it adds 13.6 days and is what puts a 75-day window at 79.5.

Works matter at the margin: in 2025 and 2026 major works ran 1.98 times their planned hours, so the hall A re-cabling in March costs kide-34b-lc64 3.1 days, about twice what the notice's planned hours imply.

**What I would change before the windows lock.** Extend each late window to its expected days, or remove the cause. For the three long-context runs, deal sequences to ranks by their attention cost rather than in turn. For kide-34b-sci, let papers split across sequences. For kide-8b-v4, give it a block inside one pod (kide-34b-16k at 192 nodes leaves pod 1 two rows free) or extend its window to 80 days. Hall B's load in March and April is what the 120b and the 16k run on; take load out of it only if their windows cannot move.

2026 bears this out: the runs held 1,505,010 GPU-days against the 1,217,311 their benchmarks implied. Waiting for the slowest rank added 59,128, blocks across both pods 152,513, interruptions and restarts 31,962, hall B's cap 49,968 and provider works 34,582; shorter documents than the benchmark's corpus gave back 42,066. The workbook has every run's bridge and range.

Days are counted from 00:00 UTC on each window's start, as CAR-2027-1 counts them, and every late block is kept until its run finishes, which is what keeps hall B loaded into April. The ranges in the workbook are four-in-five ranges from the 2026 record's own spread.
