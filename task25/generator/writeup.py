"""submission.md: the four answer blocks, every figure read from figures.json."""
import results as RS

ORDER = ["kide-70b-v2", "kide-13b-code-lc32", "kide-120b-v1", "kide-34b-v3", "kide-8b-v4", "kide-34b-16k",
         "kide-34b-lc64", "kide-13b-v4", "kide-34b-sci", "kide-13b-lc32", "kide-8b-lc64"]
LAB27 = ["benchmark days", "own mix at the mean rank", "waiting for the slowest rank", "padding",
         "block across both pods", "hall B held to its contract", "interruptions and restarts",
         "works and the window's opening", "expected days"]
LAB26 = ["benchmark GPU-days", "the runs' own mixes at the mean rank", "waiting for the slowest rank", "padding",
         "blocks across both pods", "hall B held to its contract", "hall A row 6 cooling fault",
         "interruptions and restarts", "provider works", "other (start-ups, final checkpoints, step drift)",
         "GPU-days held"]


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
    rc = fig["route_late__careful but hurried"]
    L.append("**Re-plan seven of the eleven H1 2027 runs before the windows are locked: %s will not reach their token "
             "budgets inside their windows; %s fit.** This rejects the benchmark-based plan, which (each run's own mix at "
             "its mean rank, interruptions and the notice's planned works added) files %s as late, and the "
             "plan that carries the causes the 2026 record shows one file at a time (the slowest rank, padding, hall B's "
             "capped meter, interruptions, works) but not where a block lies or what the pool does, which files %s late "
             "and %s fitting: it misses that a job with nodes in both of hall B's pods runs %s per cent slower, which "
             "puts kide-8b-v4's block across the boundary past its window, and that the research pool backs off as "
             "the reservations near hall B's contract (none from %d reserved nodes), so February to mid-March is "
             "nearly unthrottled and kide-34b-v3 fits."
             % (lt, ", ".join(k for k in ORDER if k in fit),
                ", ".join(k for k in ORDER if k in fig["route_late__shallow: mean rank, full sequences, no throttle, planned works hours"]) or "none",
                ", ".join(k for k in ORDER if k in rc and k not in late),
                ", ".join(k for k in ORDER if k in late and k not in rc), f1(fig["pod_penalty_pct"]),
                fig["pool_off_nodes"]))
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
             "(days, each item within 0.35 days or 12 per cent of itself, whichever is larger; a run whose block lies "
             "in one pod has none in the pod column): %s." % "; ".join(LAB27))
    for k in ORDER:
        L.append("   - %s: %s." % (k, "; ".join("%s %s" % (LAB27[i], "%.2f" % fig["bridge_%s_%d" % (k, i)])
                                              for i in range(len(LAB27)))))
    L.append("3. Sheet \"Bridge 2026\": 2026 as a whole in GPU-days under CAR-2027-1 section 6, each item within 12 per "
             "cent of itself or 1,500 GPU-days, held within 0.5 per cent: %s; held in hall A %s and hall B %s."
             % ("; ".join("%s %s" % (LAB26[i], g0(fig["b26_%d" % i])) for i in range(len(LAB26))),
                g0(fig["held_2026_A"]), g0(fig["held_2026_B"])))
    L.append("4. Sheet \"Causes\": the attention coefficient %s (within 0.03) from %s joined rank-steps; the slowest-rank "
             "overhead over the mean rank, within 3 points, of %s; kide-34b-sci's fill %s (within 0.015); the extra time "
             "per step of a job with nodes in both of hall B's pods, %s per cent (within 2.5 points), read off %s, "
             "the registered runs with nodes in both pods and steps outside capped hours, against the runs in one pod; "
             "each hall B run's mean step stretch in 2027, within 2.5 points, of %s per "
             "cent; the research pool's busy nodes in hall B with %s of its %s reserved, %s (within 25), and with "
             "%s reserved, none (at most 12); its busy share of the unreserved nodes at light reserved load %s (within "
             "0.03); the works overrun ratios %s (major) and %s (routine)."
             % ("%.3f" % fig["beta"], g0(G["CM"]["rows"]),
                ", ".join("%s %s per cent" % (k, f1(fig["overhead_pct_%s" % k])) for k in RS.LC_RUNS),
                "%.3f" % fig["fill_kide-34b-sci"], f1(fig["pod_penalty_pct"]),
                ", ".join(k for k in fig["pod_runs_2026"] if k != "kide-70b-scale"),
                ", ".join("%s %s" % (k[12:], f1(fig[k])) for k in sorted(fig) if k.startswith("stretch_pct_")),
                fig["pool_levels"][0], g0(fig["hall_b_nodes"]), g0(fig["pool_nodes_512"]), fig["pool_levels"][1],
                "%.3f" % fig["pool_share"], "%.2f" % fig["works_ratio_major"], "%.2f" % fig["works_ratio_routine"]))
    L.append("5. Sheet \"Routes\": each shortcut's late set beside the expected days: the benchmark alone files %s; every "
             "cause but the pod boundary and the pool's back-off files %s; the full-context FLOPs formula files %s; "
             "2026's held-over-benchmark ratio of %s files %s."
             % (", ".join(fig["route_late__quick: benchmark days"]) or "none",
                ", ".join(fig["route_late__careful but hurried"]),
                ", ".join(fig["route_late__the full-context FLOPs formula"]), "%.3f" % fig["f26_ratio"],
                ", ".join(fig["route_late__the 2026 benchmark-to-held ratio"]) or "none"))
    L.append("")
    L.append("### h1_2027_run_windows_note.md")
    L.append("")
    L.append("6. A one-page note to the compute committee: the seven late runs with expected and window days and the "
             "days past each window; the four that fit; the causes with their figures (the slowest-rank overheads, "
             "the scientific run's fill and its padding days, hall B's stretch with the pool's back-off and the days it "
             "adds to kide-120b-v1, kide-34b-v3 and kide-34b-16k, the pod boundary's days on kide-8b-v4); the works "
             "overrun's days on kide-34b-lc64; the change that removes each cause (sequences dealt to ranks by "
             "attention cost, papers allowed to split, kide-8b-v4's block inside one pod) or the window extended to "
             "the expected days; and the 2026 bridge in one sentence.")
    L.append("")
    L.append("## Critical Components")
    L.append("")
    L.append("1. A job with nodes in both of hall B's pods runs **%s per cent** slower per step: the three registered runs "
             "that straddled in 2026 (%s) ran %s of what their benchmark, mix and width predict against %s for the "
             "runs inside one pod, and kide-8b-v4's reserved rows 16 and 17 are the only 2027 block across the boundary, "
             "**%s days** of its %s."
             % (f1(fig["pod_penalty_pct"]), ", ".join(k for k in fig["pod_runs_2026"] if k != "kide-70b-scale"),
                "%.3f" % fig["pod_ratio_both"], "%.3f" % fig["pod_ratio_one"], "%.1f" % fig["bridge_kide-8b-v4_4"],
                f1(fig["days_kide-8b-v4"])))
    L.append("2. Hall B's meter reads its contract whenever the hall wanted more; with the draw fitted as a line in "
             "the allocated nodes (%s kW and %s kW a node) and the step stretch fitted on the excess rebuilt from "
             "the node states, and the research pool backing off to none once the reservations hold %d nodes, "
             "the 2027 reservations stretch kide-34b-v3, kide-34b-16k and kide-120b-v1 by **%s, %s and %s per cent**."
             % (g0(fig["draw_line"][0]), "%.2f" % fig["draw_line"][1], fig["pool_off_nodes"], f1(fig["stretch_pct_kide-34b-v3"]),
                f1(fig["stretch_pct_kide-34b-16k"]), f1(fig["stretch_pct_kide-120b-v1"])))
    L.append("3. The research pool backs off as the reservations near the contract: it keeps **%s** of hall B's unreserved "
             "nodes busy with %d of the %s reserved and **none** with %d reserved (at most 12), from **%s** of "
             "the unreserved nodes at light reserved load, so the plan's February to mid-March, with %d reserved, "
             "adds almost no stretch (kide-34b-v3 **%s per cent**) and a pool at its mean share would add about "
             "**%s** nodes of load there."
             % (g0(fig["pool_nodes_512"]), fig["pool_levels"][0], g0(fig["hall_b_nodes"]), fig["pool_levels"][1],
                "%.3f" % fig["pool_share"], fig["pool_levels"][1], f1(fig["stretch_pct_kide-34b-v3"]),
                g0(fig["pool_nodes_800_const"])))
    L.append("4. 2026 bridges from **%s** benchmark GPU-days to **%s** held: slowest rank **+%s**, blocks across both "
             "pods **+%s**, interruptions and restarts **+%s**, hall B's contract **+%s**, works **+%s**, row 6 **+%s**, "
             "shorter documents than the benchmark's corpus **%s**."
             % (g0(fig["b26_0"]), g0(fig["b26_10"]), g0(fig["b26_2"]), g0(fig["b26_4"]), g0(fig["b26_7"]),
                g0(fig["b26_5"]), g0(fig["b26_8"]), g0(fig["b26_6"]), g0(fig["b26_1"])))
    L.append("")
    L.append("## Step-by-Step")
    L.append("")
    L.append("1. Cleaned run_registry_2026, step_log_2026 and the other logs: exact repeats dropped, renamed runs mapped "
             "through previous_ids, progress read on tokens_seen (the step counter resets and replays after rollbacks), "
             "provider files moved from Helsinki time to UTC; the 2026 runs held **%s GPU-days** under CAR-2027-1 "
             "section 6." % g0(fig["held_2026_total"]))
    L.append("2. Reproduced each run's benchmark days from tpbench_results (tokens over tokens per GPU-second over "
             "GPUs); the plan's shallow read adds interruptions and the notice's planned hours, attention at each run's "
             "own mix at its mean rank, and files %s as late." % (", ".join(k for k in ORDER if k in
             fig["route_late__shallow: mean rank, full sequences, no throttle, planned works hours"]) or "none"))
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
             "when the hall wanted more; the draw is a line in the allocated nodes, **%s kW** and **%s kW** a node, "
             "fitted on the intervals clear of the contract), fitted the step stretch of every hall B job against that "
             "excess over 2026's capped days, and found the research pool's busy share of the unreserved nodes fall from "
             "**%s** at light reserved load to none once the registered runs alone held %d nodes, so the 2027 "
             "replay adds the pool at that back-off, not at the 2026 mean share (**%s**)."
             % (g0(fig["draw_line"][0]), "%.2f" % fig["draw_line"][1], "%.3f" % fig["pool_share"],
                fig["pool_off_nodes"], "%.3f" % fig["pool_share_mean"]))
    L.append("7. Compared each 2026 hall B run's steady step with the step its benchmark, mix and width predict: the "
             "runs whose nodes in node_allocations named both pods ran **%s per cent** slower, the runs in one pod "
             "did not, and the 2027 roadmap's blocks put kide-8b-v4 across the boundary." % f1(fig["pod_penalty_pct"]))
    L.append("8. Priced interruptions from interruptions_2026 (hardware per node-day by hall, software per run-day by "
             "width, facility events from incident_log) with restart time and lost work since the last checkpoint, and "
             "provider works at the 2025-26 work orders' mean overrun (**%s** major) on planned_works_h1_2027."
             % ("%.2f" % fig["works_ratio_major"]))
    L.append("9. Replayed H1 2027 on a five-minute grid with every block kept until its run finishes (CAR-2027-1 "
             "section 2), each cause added in the bridge's order, and drew the 80 per cent range from the 2026 records' "
             "spread; seven runs finish past their windows.")
    L.append("10. Bridged 2026 the same way, cause by cause from the benchmark's **%s** GPU-days to the **%s** held, with "
             "the cost model's predicted steady steps within the measured ones." % (g0(fig["b26_0"]), g0(fig["b26_10"])))
    L.append("")
    def sets(name):
        r = fig["route_late__%s" % name]
        miss = [k for k in ORDER if k in late and k not in r]
        extra = [k for k in ORDER if k in r and k not in late]
        out = []
        if miss:
            out.append("files %s as fitting" % ", ".join(miss))
        if extra:
            out.append(("files %s as late" if not miss else "%s as late") % ", ".join(extra))
        return " and ".join(out) or "files the same seven"
    clauses = [("dropping the slowest rank", "drop S1 (the mean rank)"), ("taking every sequence as full", "drop S18 (full sequences)"),
               ("dropping the pod penalty", "drop P (no pod penalty)"),
               ("taking the pool at its 2026 mean share of the free nodes", "drop Q (the pool at its mean share)"),
               ("the full-context FLOPs formula", "the full-context FLOPs formula"),
               ("2026's pooled held-over-benchmark ratio", "the 2026 benchmark-to-held ratio"),
               ("the nearest 2026 run's realised rate", "direct: the nearest 2026 run's realised rate")]
    L.append("No other conclusion survives: %s. Twenty rival constructions (the clear intervals at three distances, the "
             "draw line on busy intervals only, the contract at the meter's ceiling, a straight-line and a banded throttle, "
             "the stretch against local steady steps, the pod penalty from the registered runs and from each run's twin, "
             "the pool as a cut-off and as a logistic curve, its light-load share from runs below %d per cent, the "
             "median works overrun, another packing seed, no launch delay, the attention coefficient at its lowest and "
             "highest per-run fit, lengths from a fitted lognormal, a normal approximation to the slowest rank, hardware "
             "stops pooled over halls) and each fitted input moved by its spread (20 per cent on the rates and the "
             "responses, 4 points on the pod penalty, 0.1 on the pool's light-load share, 1 per cent on the draw line) "
             "file the same seven."
             % ("; ".join("%s %s" % (lab, sets(key)) for lab, key in clauses), fig["light_load_pct"]))
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")
