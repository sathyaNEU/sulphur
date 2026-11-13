"""submission.md: the four answer blocks, every figure read from figures.json."""
import results as RS

ORDER = ["kide-70b-v2", "kide-13b-code-lc32", "kide-120b-v1", "kide-34b-v3", "kide-8b-v4", "kide-34b-16k",
         "kide-34b-lc64", "kide-13b-v4", "kide-34b-sci", "kide-13b-lc32", "kide-8b-lc64"]
LAB27 = ["benchmark days", "own mix at the mean rank", "waiting for the slowest rank", "padding",
         "hall B held to its contract", "interruptions and restarts", "works and the window's opening", "expected days"]
LAB26 = ["benchmark GPU-days", "the runs' own mixes at the mean rank", "waiting for the slowest rank", "padding",
         "hall B held to its contract", "hall A row 6 cooling fault", "interruptions and restarts", "provider works",
         "other (start-ups, final checkpoints, step drift)", "GPU-days held"]


def f1(x):
    return "%.1f" % x


def g0(x):
    return format(int(round(x)), ",")


def write(path, fig, G):
    runs = {r["run_id"]: r for r in G["runs"]}
    late = fig["call_late_runs"]
    fit = fig["call_fitting_runs"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Machine Learning Research, General Statistics & Data Science (benchmarking and ablations: a "
             "throughput benchmark bridged to production pretraining runs).")
    L.append("**Analytical objective:** Comparative Analysis & Explanation.")
    L.append("")
    L.append("## Final Recommendation")
    L.append("")
    lt = ", ".join("%s (%s days against %d)" % (k, f1(fig["days_%s" % k]), fig["window_%s" % k]) for k in ORDER if k in late)
    L.append("**Re-plan seven of the eleven H1 2027 runs before the windows are locked: %s will not reach their token "
             "budgets inside their windows; %s fit.** This rejects the benchmark-based plan, which (each run's own mix at "
             "its mean rank, interruptions and the notice's planned works added) files every run as fitting, because it "
             "misses three things the 2026 record shows: each step waits for the data-parallel rank holding the longest "
             "documents, best-fit packing pads the scientific mix to a fill of %s, and hall B is held to its "
             "contracted IT load through February to April with every job's steps stretched."
             % (lt, ", ".join(k for k in ORDER if k in fit), "%.3f" % fig["fill_kide-34b-sci"]))
    L.append("")
    L.append("## Supplementary Questions")
    L.append("")
    L.append("### h1_2027_throughput_bridge.xlsx")
    L.append("")
    L.append("1. Sheet \"Runs H1 2027\": one row per run in window order with run, hall, window start and end, window "
             "days, benchmark days, expected days, the 80 per cent range, the expected finish date, whether it is "
             "inside its window and the days past the window's end, late runs shaded; a bar chart of expected against "
             "window days under the table. Expected days are graded to 0.1 within 3 per cent, the range ends within 5 "
             "per cent and the finish date within one day:")
    for k in ORDER:
        r = runs[k]
        s = "   - %s: benchmark %s days; expected %s days (80 per cent range %s to %s); finishes %s; window %d days" % (
            k, f1(fig["bench_days_%s" % k]), f1(fig["days_%s" % k]), f1(fig["p10_%s" % k]), f1(fig["p90_%s" % k]),
            fig["finish_%s" % k], fig["window_%s" % k])
        s += ("; late by %s days." % f1(fig["short_%s" % k])) if k in late else "; inside its window."
        L.append(s)
    L.append("2. Sheet \"Bridge 2027\": one row per run, columns in this order, each cause added to the ones before it "
             "(days, each item within 0.35 days or 12 per cent of itself, whichever is larger): %s." % "; ".join(LAB27))
    for k in ORDER:
        L.append("   - %s: %s." % (k, "; ".join("%s %s" % (LAB27[i], "%.2f" % fig["bridge_%s_%d" % (k, i)])
                                              for i in range(len(LAB27)))))
    L.append("3. Sheet \"Bridge 2026\": 2026 as a whole in GPU-days under CAR-2027-1 section 6, each item within 12 per "
             "cent of itself or 1,500 GPU-days, held within 0.5 per cent: %s; held in hall A %s and hall B %s."
             % ("; ".join("%s %s" % (LAB26[i], g0(fig["b26_%d" % i])) for i in range(len(LAB26))),
                g0(fig["held_2026_A"]), g0(fig["held_2026_B"])))
    L.append("4. Sheet \"Causes\": the attention coefficient %s (within 0.03) from %s joined rank-steps; the slowest-rank "
             "overhead over the mean rank, within 3 points, of %s; kide-34b-sci's fill %s (within 0.015); each hall B run's mean step "
             "stretch in 2027, within 2.5 points, of %s per cent; the pool's busy share %s; the works overrun ratios %s "
             "(major) and %s (routine)."
             % ("%.3f" % fig["beta"], g0(G["CM"]["rows"]),
                ", ".join("%s %s per cent" % (k, f1(fig["overhead_pct_%s" % k])) for k in RS.LC_RUNS),
                "%.3f" % fig["fill_kide-34b-sci"],
                ", ".join("%s %s" % (k[12:], f1(fig[k])) for k in sorted(fig) if k.startswith("stretch_pct_")),
                "%.3f" % fig["pool_share"], "%.2f" % fig["works_ratio_major"], "%.2f" % fig["works_ratio_routine"]))
    L.append("5. Sheet \"Routes\": each shortcut's late set beside the expected days: the benchmark alone and the "
             "benchmark at each run's mean rank with interruptions and planned works both file none; the full-context "
             "FLOPs formula files %s; 2026's held-over-benchmark ratio of %s files %s."
             % (", ".join(fig["route_late__the full-context FLOPs formula"]), "%.3f" % fig["f26_ratio"],
                ", ".join(fig["route_late__the 2026 benchmark-to-held ratio"]) or "none"))
    L.append("")
    L.append("### h1_2027_run_windows_note.md")
    L.append("")
    L.append("6. A one-page note to the compute committee: the seven late runs with expected and window days and the "
             "days past each window; the four that fit; the three causes with their figures (the slowest-rank overheads, "
             "the scientific run's fill and its padding days, hall B's stretch and the days it adds to kide-120b-v1, "
             "kide-34b-v3 and kide-34b-16k); the works overrun's days on kide-34b-lc64 and kide-8b-lc64; the change "
             "that removes each cause (sequences dealt to ranks by attention cost, papers allowed to split, hall B's "
             "February to April load brought under contract) or the window extended to the expected days; and the 2026 "
             "bridge in one sentence.")
    L.append("")
    L.append("## Critical Components")
    L.append("")
    L.append("1. Each step waits for the slowest data-parallel rank: with an attention coefficient of **%s**, the "
             "slowest rank runs **%s, %s and %s per cent** over the mean rank for kide-13b-code-lc32, kide-34b-lc64 "
             "and kide-8b-lc64 (kide-13b-lc32, on sixteen sequences per rank, only **%s**)."
             % ("%.3f" % fig["beta"], f1(fig["overhead_pct_kide-13b-code-lc32"]), f1(fig["overhead_pct_kide-34b-lc64"]),
                f1(fig["overhead_pct_kide-8b-lc64"]), f1(fig["overhead_pct_kide-13b-lc32"])))
    L.append("2. Best-fit packing fills **%s** of kide-34b-sci's sequence positions, **%s days** of padding on its "
             "benchmark." % ("%.3f" % fig["fill_kide-34b-sci"], "%.2f" % fig["bridge_kide-34b-sci_3"]))
    L.append("3. Hall B's meter reads its contract whenever the hall wanted more; with the step stretch fitted on the "
             "excess rebuilt from the node states, the 2027 reservations stretch kide-34b-v3, kide-34b-16k and "
             "kide-120b-v1 by **%s, %s and %s per cent**."
             % (f1(fig["stretch_pct_kide-34b-v3"]),
                f1(fig["stretch_pct_kide-34b-16k"]), f1(fig["stretch_pct_kide-120b-v1"])))
    L.append("4. 2026 bridges from **%s** benchmark GPU-days to **%s** held: slowest rank **+%s**, interruptions and "
             "restarts **+%s**, hall B's contract **+%s**, works **+%s**, row 6 **+%s**, shorter documents than the "
             "benchmark's corpus **%s**."
             % (g0(fig["b26_0"]), g0(fig["b26_9"]), g0(fig["b26_2"]), g0(fig["b26_6"]), g0(fig["b26_4"]),
                g0(fig["b26_7"]), g0(fig["b26_5"]), g0(fig["b26_1"])))
    L.append("")
    L.append("## Step-by-Step")
    L.append("")
    L.append("1. Cleaned run_registry_2026, step_log_2026 and the other logs: exact repeats dropped, renamed runs mapped "
             "through previous_ids, progress read on tokens_seen (the step counter resets and replays after rollbacks), "
             "provider files moved from Helsinki time to UTC; the 2026 runs held **%s GPU-days** under CAR-2027-1 "
             "section 6." % g0(fig["held_2026_total"]))
    L.append("2. Reproduced each run's benchmark days from tpbench_results (tokens over tokens per GPU-second over "
             "GPUs); the plan's shallow read adds interruptions and the notice's planned hours, attention at each run's "
             "own mix at its mean rank, and files every run as fitting.")
    L.append("3. Joined rank_step_samples to packing_manifests on run, step and rank: a rank's time follows its "
             "sequences' dense count plus **%s** times L d C over N times the sum of squared document lengths over C "
             "squared (tokens per rank are equal, so a fit on tokens finds nothing and the spread reads as hardware); "
             "row 6's nodes in their September to October cooling fault and capped hall B intervals left out."
             % ("%.3f" % fig["beta"]))
    L.append("4. Replayed each 2027 run's loader rule on doc_length_sample at its mix, dealt sequences to its "
             "data-parallel ranks in turn and took each step's slowest rank: overheads of **%s to %s per cent** on the "
             "few-sequence long-context runs, while the full-context FLOPs formula overstates kide-13b-lc32 and files it "
             "late." % (f1(fig["overhead_pct_kide-13b-code-lc32"]), f1(fig["overhead_pct_kide-8b-lc64"])))
    L.append("5. Replayed the best-fit rule on kide-34b-sci's mix: fill **%s**, against 2026's best-fit runs at nearly "
             "full; every sequence taken as full misses **%s days**." % ("%.3f" % fig["fill_kide-34b-sci"],
                                                                      "%.2f" % fig["bridge_kide-34b-sci_3"]))
    L.append("6. Rebuilt hall B's would-be draw from node_states (the meter in hall_it_load reads the contract exactly "
             "when the hall wanted more), fitted the step stretch of every hall B job against that excess over 2026's capped "
             "days, and replayed the 2027 reservations with the pool's 2026 share of free nodes (**%s**)."
             % ("%.3f" % fig["pool_share"]))
    L.append("7. Priced interruptions from interruptions_2026 (hardware per node-day by hall, software per run-day by "
             "width, facility events from incident_log) with restart time and lost work since the last checkpoint, and "
             "provider works at the 2025-26 work orders' mean overrun (**%s** major) on planned_works_h1_2027."
             % ("%.2f" % fig["works_ratio_major"]))
    L.append("8. Replayed H1 2027 on a five-minute grid with every block kept until its run finishes (CAR-2027-1 "
             "section 2), each cause added in the bridge's order, and drew the 80 per cent range from the 2026 records' "
             "spread; seven runs finish past their windows.")
    L.append("9. Bridged 2026 the same way, cause by cause from the benchmark's **%s** GPU-days to the **%s** held, with "
             "the cost model's predicted steady steps within the measured ones." % (g0(fig["b26_0"]), g0(fig["b26_9"])))
    L.append("")
    L.append("No other conclusion survives: dropping the slowest rank lets kide-13b-code-lc32, kide-34b-lc64 and "
             "kide-8b-lc64 fit; taking every sequence as full lets kide-34b-sci fit; leaving hall B unthrottled lets "
             "kide-120b-v1, kide-34b-v3 and kide-34b-16k fit; the full-context formula wrongly files kide-13b-lc32 and "
             "2026's pooled ratio files none. Eight rival constructions (the attention coefficient at the lowest and "
             "highest run's fit, lengths from a fitted lognormal, another packing seed, a normal approximation to the slowest "
             "rank, a straight-line throttle, the median works overrun, hardware stops pooled over halls) and each fitted "
             "input moved by 20 per cent file the same seven.")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")
