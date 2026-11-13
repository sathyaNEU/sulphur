## Tags

**Domain:** Machine Learning Research, General Statistics & Data Science (benchmarking and ablations: a throughput benchmark bridged to production pretraining runs).
**Analytical objective:** Comparative Analysis & Explanation.

## Final Recommendation

**Re-plan seven of the eleven H1 2027 runs before the windows are locked: kide-13b-code-lc32 (8.0 days against 7), kide-120b-v1 (86.2 days against 75), kide-34b-v3 (43.8 days against 38), kide-34b-16k (62.1 days against 54), kide-34b-lc64 (14.9 days against 13), kide-34b-sci (23.0 days against 20), kide-8b-lc64 (15.1 days against 13) will not reach their token budgets inside their windows; kide-70b-v2, kide-8b-v4, kide-13b-v4, kide-13b-lc32 fit.** This rejects the benchmark-based plan, which (each run's own mix at its mean rank, interruptions and the notice's planned works added) files every run as fitting, because it misses three things the 2026 record shows: each step waits for the data-parallel rank holding the longest documents, best-fit packing pads the scientific mix to a fill of 0.795, and hall B is held to its contracted IT load through February to April with every job's steps stretched.

## Supplementary Questions

### h1_2027_throughput_bridge.xlsx

1. Sheet "Runs H1 2027": one row per run in window order with run, hall, window start and end, window days, benchmark days, expected days, the 80 per cent range, the expected finish date, whether it is inside its window and the days past the window's end, late runs shaded; a bar chart of expected against window days under the table. Expected days are graded to 0.1 within 3 per cent, the range ends within 5 per cent and the finish date within one day:
   - kide-70b-v2: benchmark 38.5 days; expected 39.5 days (80 per cent range 39.3 to 39.7); finishes 2027-02-19; window 47 days; inside its window.
   - kide-13b-code-lc32: benchmark 6.4 days; expected 8.0 days (80 per cent range 8.0 to 8.1); finishes 2027-01-26; window 7 days; late by 1.0 days.
   - kide-120b-v1: benchmark 69.8 days; expected 86.2 days (80 per cent range 85.5 to 86.9); finishes 2027-04-28; window 75 days; late by 11.2 days.
   - kide-34b-v3: benchmark 34.9 days; expected 43.8 days (80 per cent range 43.1 to 44.2); finishes 2027-03-16; window 38 days; late by 5.8 days.
   - kide-8b-v4: benchmark 51.8 days; expected 63.0 days (80 per cent range 62.4 to 63.6); finishes 2027-04-05; window 75 days; inside its window.
   - kide-34b-16k: benchmark 49.3 days; expected 62.1 days (80 per cent range 61.4 to 62.6); finishes 2027-04-25; window 54 days; late by 8.1 days.
   - kide-34b-lc64: benchmark 7.8 days; expected 14.9 days (80 per cent range 14.4 to 15.3); finishes 2027-03-15; window 13 days; late by 1.9 days.
   - kide-13b-v4: benchmark 27.9 days; expected 33.6 days (80 per cent range 33.2 to 33.9); finishes 2027-04-17; window 40 days; inside its window.
   - kide-34b-sci: benchmark 17.1 days; expected 23.0 days (80 per cent range 22.9 to 23.1); finishes 2027-05-04; window 20 days; late by 3.0 days.
   - kide-13b-lc32: benchmark 8.5 days; expected 10.1 days (80 per cent range 10.0 to 10.2); finishes 2027-04-29; window 12 days; inside its window.
   - kide-8b-lc64: benchmark 6.0 days; expected 15.1 days (80 per cent range 14.4 to 15.7); finishes 2027-05-25; window 13 days; late by 2.1 days.
2. Sheet "Bridge 2027": one row per run, columns in this order, each cause added to the ones before it (days, each item within 0.35 days or 12 per cent of itself, whichever is larger): benchmark days; own mix at the mean rank; waiting for the slowest rank; padding; hall B held to its contract; interruptions and restarts; works and the window's opening; expected days.
   - kide-70b-v2: benchmark days 38.54; own mix at the mean rank -0.90; waiting for the slowest rank 0.95; padding 0.00; hall B held to its contract 0.00; interruptions and restarts 0.50; works and the window's opening 0.38; expected days 39.48.
   - kide-13b-code-lc32: benchmark days 6.35; own mix at the mean rank -0.27; waiting for the slowest rank 1.91; padding 0.00; hall B held to its contract 0.00; interruptions and restarts 0.03; works and the window's opening 0.03; expected days 8.05.
   - kide-120b-v1: benchmark days 69.83; own mix at the mean rank -2.00; waiting for the slowest rank 2.46; padding 0.00; hall B held to its contract 13.47; interruptions and restarts 2.03; works and the window's opening 0.44; expected days 86.24.
   - kide-34b-v3: benchmark days 34.89; own mix at the mean rank -0.88; waiting for the slowest rank 0.94; padding 0.00; hall B held to its contract 7.52; interruptions and restarts 0.79; works and the window's opening 0.51; expected days 43.77.
   - kide-8b-v4: benchmark days 51.78; own mix at the mean rank -1.47; waiting for the slowest rank 1.22; padding 0.00; hall B held to its contract 10.51; interruptions and restarts 0.49; works and the window's opening 0.51; expected days 63.04.
   - kide-34b-16k: benchmark days 49.27; own mix at the mean rank -1.42; waiting for the slowest rank 2.10; padding 0.00; hall B held to its contract 11.24; interruptions and restarts 0.78; works and the window's opening 0.12; expected days 62.10.
   - kide-34b-lc64: benchmark days 7.76; own mix at the mean rank 0.19; waiting for the slowest rank 3.82; padding 0.00; hall B held to its contract 0.00; interruptions and restarts 0.06; works and the window's opening 3.10; expected days 14.93.
   - kide-13b-v4: benchmark days 27.93; own mix at the mean rank -1.05; waiting for the slowest rank 1.03; padding 0.00; hall B held to its contract 5.12; interruptions and restarts 0.43; works and the window's opening 0.12; expected days 33.57.
   - kide-34b-sci: benchmark days 17.09; own mix at the mean rank 0.45; waiting for the slowest rank 0.57; padding 4.66; hall B held to its contract 0.00; interruptions and restarts 0.18; works and the window's opening 0.03; expected days 22.98.
   - kide-13b-lc32: benchmark days 8.55; own mix at the mean rank -0.15; waiting for the slowest rank 0.79; padding 0.00; hall B held to its contract 0.77; interruptions and restarts 0.10; works and the window's opening 0.03; expected days 10.09.
   - kide-8b-lc64: benchmark days 6.01; own mix at the mean rank 0.73; waiting for the slowest rank 3.89; padding 0.00; hall B held to its contract 0.00; interruptions and restarts 0.04; works and the window's opening 4.45; expected days 15.11.
3. Sheet "Bridge 2026": 2026 as a whole in GPU-days under CAR-2027-1 section 6, each item within 12 per cent of itself or 1,500 GPU-days, held within 0.5 per cent: benchmark GPU-days 1,250,323; the runs' own mixes at the mean rank -42,558; waiting for the slowest rank 60,137; padding 6; hall B held to its contract 21,024; hall A row 6 cooling fault 5,228; interruptions and restarts 27,131; provider works 18,900; other (start-ups, final checkpoints, step drift) -7,244; GPU-days held 1,332,946; held in hall A 234,166 and hall B 1,098,781.
4. Sheet "Causes": the attention coefficient 1.325 (within 0.03) from 19,520 joined rank-steps; the slowest-rank overhead over the mean rank, within 3 points, of kide-13b-code-lc32 31.3 per cent, kide-34b-lc64 48.1 per cent, kide-8b-lc64 57.8 per cent, kide-13b-lc32 9.4 per cent, kide-34b-sci 3.3 per cent; kide-34b-sci's fill 0.795 (within 0.015); each hall B run's mean step stretch in 2027, within 2.5 points, of kide-120b-v1 19.7, kide-13b-lc32 9.6, kide-13b-v4 19.6, kide-34b-16k 23.4, kide-34b-v3 23.3, kide-8b-lc64 0.0, kide-8b-v4 21.7 per cent; the pool's busy share 0.368; the works overrun ratios 1.99 (major) and 1.09 (routine).
5. Sheet "Routes": each shortcut's late set beside the expected days: the benchmark alone and the benchmark at each run's mean rank with interruptions and planned works both file none; the full-context FLOPs formula files kide-13b-code-lc32, kide-13b-lc32, kide-34b-16k, kide-34b-lc64, kide-8b-lc64; 2026's held-over-benchmark ratio of 1.066 files none.

### h1_2027_run_windows_note.md

6. A one-page note to the compute committee: the seven late runs with expected and window days and the days past each window; the four that fit; the three causes with their figures (the slowest-rank overheads, the scientific run's fill and its padding days, hall B's stretch and the days it adds to kide-120b-v1, kide-34b-v3 and kide-34b-16k); the works overrun's days on kide-34b-lc64 and kide-8b-lc64; the change that removes each cause (sequences dealt to ranks by attention cost, papers allowed to split, hall B's February to April load brought under contract) or the window extended to the expected days; and the 2026 bridge in one sentence.

## Critical Components

1. Each step waits for the slowest data-parallel rank: with an attention coefficient of **1.325**, the slowest rank runs **31.3, 48.1 and 57.8 per cent** over the mean rank for kide-13b-code-lc32, kide-34b-lc64 and kide-8b-lc64 (kide-13b-lc32, on sixteen sequences per rank, only **9.4**).
2. Best-fit packing fills **0.795** of kide-34b-sci's sequence positions, **4.66 days** of padding on its benchmark.
3. Hall B's meter reads its contract whenever the hall wanted more; with the step stretch fitted on the excess rebuilt from the node states, the 2027 reservations stretch kide-34b-v3, kide-34b-16k and kide-120b-v1 by **23.3, 23.4 and 19.7 per cent**.
4. 2026 bridges from **1,250,323** benchmark GPU-days to **1,332,946** held: slowest rank **+60,137**, interruptions and restarts **+27,131**, hall B's contract **+21,024**, works **+18,900**, row 6 **+5,228**, shorter documents than the benchmark's corpus **-42,558**.

## Step-by-Step

1. Cleaned run_registry_2026, step_log_2026 and the other logs: exact repeats dropped, renamed runs mapped through previous_ids, progress read on tokens_seen (the step counter resets and replays after rollbacks), provider files moved from Helsinki time to UTC; the 2026 runs held **1,332,946 GPU-days** under CAR-2027-1 section 6.
2. Reproduced each run's benchmark days from tpbench_results (tokens over tokens per GPU-second over GPUs); the plan's shallow read adds interruptions and the notice's planned hours, attention at each run's own mix at its mean rank, and files every run as fitting.
3. Joined rank_step_samples to packing_manifests on run, step and rank: a rank's time follows its sequences' dense count plus **1.325** times L d C over N times the sum of squared document lengths over C squared (tokens per rank are equal, so a fit on tokens finds nothing and the spread reads as hardware); row 6's nodes in their September to October cooling fault and capped hall B intervals left out.
4. Replayed each 2027 run's loader rule on doc_length_sample at its mix, dealt sequences to its data-parallel ranks in turn and took each step's slowest rank: overheads of **31.3 to 57.8 per cent** on the few-sequence long-context runs, while the full-context FLOPs formula overstates kide-13b-lc32 and files it late.
5. Replayed the best-fit rule on kide-34b-sci's mix: fill **0.795**, against 2026's best-fit runs at nearly full; every sequence taken as full misses **4.66 days**.
6. Rebuilt hall B's would-be draw from node_states (the meter in hall_it_load reads the contract exactly when the hall wanted more), fitted the step stretch of every hall B job against that excess over 2026's capped days, and replayed the 2027 reservations with the pool's 2026 share of free nodes (**0.368**).
7. Priced interruptions from interruptions_2026 (hardware per node-day by hall, software per run-day by width, facility events from incident_log) with restart time and lost work since the last checkpoint, and provider works at the 2025-26 work orders' mean overrun (**1.99** major) on planned_works_h1_2027.
8. Replayed H1 2027 on a five-minute grid with every block kept until its run finishes (CAR-2027-1 section 2), each cause added in the bridge's order, and drew the 80 per cent range from the 2026 records' spread; seven runs finish past their windows.
9. Bridged 2026 the same way, cause by cause from the benchmark's **1,250,323** GPU-days to the **1,332,946** held, with the cost model's predicted steady steps within the measured ones.

No other conclusion survives: dropping the slowest rank lets kide-13b-code-lc32, kide-34b-lc64 and kide-8b-lc64 fit; taking every sequence as full lets kide-34b-sci fit; leaving hall B unthrottled lets kide-120b-v1, kide-34b-v3 and kide-34b-16k fit; the full-context formula wrongly files kide-13b-lc32 and 2026's pooled ratio files none. Eight rival constructions (the attention coefficient at the lowest and highest run's fit, lengths from a fitted lognormal, another packing seed, a normal approximation to the slowest rank, a straight-line throttle, the median works overrun, hardware stops pooled over halls) and each fitted input moved by 20 per cent file the same seven.
