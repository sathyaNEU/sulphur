"""The golden deliverables: Pia Kuosmanen's workbook (every H1 2027 run bridged from its benchmark days to its expected
days, the 2026 bridge, the causes as measured, the shortcuts' late sets) and her note to the compute committee."""
import datetime as dt
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import params as P
import postprocess
import results as RS

HDR = PatternFill("solid", fgColor="DCE6F1")
LATE = PatternFill("solid", fgColor="F8CBAD")
THIN = Side(style="thin", color="B7B7B7")
LABELS_27 = ["Benchmark days", "Own mix at the mean rank", "Waiting for the slowest rank", "Padding",
             "Block across both pods", "Hall B held to its contract", "Interruptions and restarts",
             "Works and window opening", "Expected days"]
LABELS_26 = ["Benchmark GPU-days", "Own mixes at the mean rank", "Waiting for the slowest rank", "Padding",
             "Blocks across both pods", "Hall B held to its contract", "Hall A row 6 cooling fault",
             "Interruptions and restarts", "Provider works", "Other (start-ups, final checkpoints, step drift)",
             "GPU-days held"]


def _hdr(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = Font(bold=True)
        cell.fill = HDR
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=THIN)
    if widths:
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w


def order(G, fig):
    late = set(fig["call_late_runs"])
    rows = sorted(G["runs"], key=lambda r: (r["ws"], r["run_id"]))
    return rows, late


def workbook(path, G, fig, X):
    wb = Workbook()
    rows, late = order(G, fig)
    ws = wb.active
    ws.title = "Runs H1 2027"
    ws["A1"] = "Seven of the eleven H1 2027 runs finish past their reserved windows"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Expected days from 00:00 UTC on each window's start (CAR-2027-1 section 2). Late runs shaded. "
                "%s, training infrastructure, 6 November 2026." % P.INFRA_LEAD)
    ws.freeze_panes = "B5"
    cols = ["Run", "Hall", "Window start", "Window end", "Window days", "Benchmark days", "Expected days",
            "80% range low", "80% range high", "Expected finish", "Inside window", "Days past window end"]
    _hdr(ws, 4, cols, [21, 6, 12, 12, 9, 11, 10, 10, 10, 12, 9, 12])
    for i, r in enumerate(rows, 5):
        k = r["run_id"]
        vals = [k, r["hall"], r["ws"], r["we"], r["window_days"], fig["bench_days_%s" % k], fig["days_%s" % k],
                fig["p10_%s" % k], fig["p90_%s" % k], dt.date.fromisoformat(fig["finish_%s" % k]),
                "no" if k in late else "yes", fig["short_%s" % k] if k in late else None]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "yyyy-mm-dd"
            elif isinstance(v, float):
                c.number_format = "0.0"
            if k in late:
                c.fill = LATE
    n = len(rows)
    ch = BarChart()
    ch.type = "bar"
    ch.title = "Expected days against the reserved window"
    ch.y_axis.title = "days from the window's start"
    ch.x_axis.title = None
    data = Reference(ws, min_col=5, max_col=5, min_row=4, max_row=4 + n)
    data2 = Reference(ws, min_col=7, max_col=7, min_row=4, max_row=4 + n)
    cats = Reference(ws, min_col=1, min_row=5, max_row=4 + n)
    ch.add_data(data, titles_from_data=True)
    ch.add_data(data2, titles_from_data=True)
    ch.set_categories(cats)
    ch.height, ch.width = 9.5, 17
    ch.series[0].graphicalProperties.solidFill = "A6A6A6"
    ch.series[1].graphicalProperties.solidFill = "1F4E79"
    ws.add_chart(ch, "A%d" % (n + 7))

    wb2 = wb.create_sheet("Bridge 2027")
    wb2["A1"] = "Each run from its benchmark days to its expected days, cause by cause (days, in this order)"
    wb2["A1"].font = Font(bold=True, size=12)
    _hdr(wb2, 3, ["Run"] + LABELS_27, [21, 11, 12, 13, 9, 12, 13, 13, 13, 10])
    wb2.freeze_panes = "B4"
    for i, r in enumerate(rows, 4):
        k = r["run_id"]
        wb2.cell(row=i, column=1, value=k)
        for j in range(len(LABELS_27)):
            c = wb2.cell(row=i, column=2 + j, value=fig["bridge_%s_%d" % (k, j)])
            c.number_format = "0.00"
    wb2.cell(row=5 + n, column=1, value="Order: benchmark, then mix, slowest rank, padding, the block across both pods, hall B, "
                                         "interruptions, works; each cause added to the ones before it.").font = Font(italic=True, size=9)

    w3 = wb.create_sheet("Bridge 2026")
    w3["A1"] = "2026 as a whole: the benchmark's GPU-days to the GPU-days the runs held (CAR-2027-1 section 6)"
    w3["A1"].font = Font(bold=True, size=12)
    _hdr(w3, 3, ["Item", "GPU-days"], [46, 14])
    for i, lab in enumerate(LABELS_26):
        w3.cell(row=4 + i, column=1, value=lab)
        c = w3.cell(row=4 + i, column=2, value=fig["b26_%d" % i])
        c.number_format = "#,##0"
    w3.cell(row=17, column=1, value="Held by hall: A").font = Font(bold=True)
    w3.cell(row=17, column=2, value=fig["held_2026_A"]).number_format = "#,##0"
    w3.cell(row=18, column=1, value="Held by hall: B").font = Font(bold=True)
    w3.cell(row=18, column=2, value=fig["held_2026_B"]).number_format = "#,##0"

    w4 = wb.create_sheet("Causes")
    w4["A1"] = "The causes as measured on the 2026 record"
    w4["A1"].font = Font(bold=True, size=12)
    _hdr(w4, 3, ["Quantity", "Value", "From"], [58, 12, 60])
    lines = [
        ("Attention cost per FLOP against dense compute (coefficient)", fig["beta"],
         "rank_step_samples joined to packing_manifests, %d rank-steps" % G["CM"]["rows"]),
        ("Step overhead beyond the slowest rank (per cent)", fig["ovh_pct"], "rank_step_samples"),
    ]
    for k in RS.LC_RUNS:
        lines.append(("Slowest-rank overhead over the mean rank, %s (per cent)" % k, fig["overhead_pct_%s" % k],
                      "packing replay on doc_length_sample at the run's mix, width and sequences per rank"))
    lines.append(("Packing fill, kide-34b-sci (real tokens per position)", fig["fill_kide-34b-sci"],
                  "best-fit rule replayed on doc_length_sample"))
    for x in (5, 10, 15, 20):
        lines.append(("Hall B step stretch at %d per cent over contract (per cent)" % x, fig["throttle_pct_x%02d" % x],
                      "step_log against excess rebuilt from node_states, %d capped days" % fig["capped_days_2026"]))
    lines.append(("Extra time per step for a job with nodes in both hall B pods (per cent)", fig["pod_penalty_pct"],
                  "steady step over the step its benchmark, mix and width predict: %s against %s, runs in both pods "
                  "against runs in one" % ("%.3f" % fig["pod_ratio_both"], "%.3f" % fig["pod_ratio_one"])))
    lines.append(("2026 runs with nodes in both pods", ", ".join(fig["pod_runs_2026"]), "node_allocations_2026"))
    lines.append(("2027 runs with a block across both pods", ", ".join(fig["pod_runs_2027"]), "the roadmap's blocks"))
    for k in sorted(X["stretch"]):
        lines.append(("Mean step stretch in 2027, %s (per cent)" % k, fig["stretch_pct_%s" % k],
                      "2027 reservations, the pool at its measured back-off"))
    lines += [("Hall B draw line: kW at no allocated node, kW per allocated node", "%s, %s" % tuple(fig["draw_line"]),
               "hall_it_load on the intervals clear of the contract against node_states"),
              ("Research pool's busy share of unreserved hall B nodes at light reserved load", fig["pool_share"],
               "node_states less registered runs"),
              ("Research pool's busy nodes with 512 of hall B's nodes reserved", fig["pool_nodes_512"],
               "its share by reserved load"),
              ("Research pool's busy nodes with 800 of hall B's nodes reserved", fig["pool_nodes_800"],
               "its share by reserved load"),
              ("Major works, actual over planned hours (mean)", fig["works_ratio_major"], "work_orders_2025_2026"),
              ("Routine works, actual over planned hours (mean)", fig["works_ratio_routine"], "work_orders_2025_2026")]
    for i, (a, b, c) in enumerate(lines, 4):
        w4.cell(row=i, column=1, value=a)
        w4.cell(row=i, column=2, value=b)
        w4.cell(row=i, column=3, value=c)

    w5 = wb.create_sheet("Routes")
    w5["A1"] = "What each shortcut files, beside the expected days"
    w5["A1"].font = Font(bold=True, size=12)
    _hdr(w5, 3, ["Route", "Runs it files as late"], [44, 110])
    w5.cell(row=4, column=1, value="Expected days (this workbook)")
    w5.cell(row=4, column=2, value=", ".join(fig["call_late_runs"]))
    names = [("the benchmark's days alone", "quick: benchmark days"),
             ("benchmark at each run's mean rank with interruptions and planned works hours",
              "shallow: mean rank, full sequences, no throttle, planned works hours"),
             ("each run's benchmark days over its nearest 2026 run's realised rate", "direct: the nearest 2026 run's realised rate"),
             ("every cause but the pod boundary and the pool's back-off (the pool at its mean share)", "careful but hurried"),
             ("expected days with no pod penalty", "drop P (no pod penalty)"),
             ("expected days with the pool at its 2026 mean share of free nodes", "drop Q (the pool at its mean share)"),
             ("the full-context FLOPs formula for attention", "the full-context FLOPs formula"),
             ("2026's held-over-benchmark ratio (%.3f) on every run" % fig["f26_ratio"], "the 2026 benchmark-to-held ratio"),
             ("expected days with each rank at its mean", "drop S1 (the mean rank)"),
             ("expected days with every sequence full", "drop S18 (full sequences)"),
             ("expected days with no hall B throttle", "drop S3 (no throttle)")]
    for i, (label, key) in enumerate(names, 5):
        w5.cell(row=i, column=1, value=label)
        v = fig["route_late__%s" % key]
        w5.cell(row=i, column=2, value=", ".join(v) if v else "none")
    w6 = wb.create_sheet("Notes")
    notes = [
        ("As of", "2026 record to 31 October 2026, pulled 6 November 2026; roadmap version 7 of 4 November 2026."),
        ("Window", "From 00:00 UTC on the window's start date to 00:00 UTC on its end date (CAR-2027-1 section 2)."),
        ("Finished", "When the trainer's token count, which excludes padding, reaches the run's budget (section 3)."),
        ("Inside its window", "Expected finish at or before the window's end (section 4)."),
        ("Late blocks", "Kept until the run finishes, nothing else booked on them (section 2); hall B's load carries them. "
                        "No block shares rows with an earlier one inside its window, so no later run waits for nodes."),
        ("Pods", "A block's pod is read from its node names in the roadmap; the penalty is read from the 2026 runs "
                 "whose allocations name both."),
        ("Bridge order", "Benchmark, own mix at the mean rank, slowest rank, padding, the block across both pods, hall B, "
                         "interruptions, works; each cause added to the ones before it, so the items add to the "
                         "expected days."),
        ("80 per cent range", "160 draws of the 2026 record: interruption counts, restart and lost-work times, the "
                              "throttle fit by capped day, each work's overrun from its type's 2025-26 ratios, the "
                              "pod penalty and the pool's light-load share."),
        ("Rounding", "Days to 0.1 (bridge items to 0.01), GPU-days to the unit, shares and ratios to three places."),
    ]
    w6.column_dimensions["A"].width = 20
    w6.column_dimensions["B"].width = 112
    for i, (a, b) in enumerate(notes, 1):
        w6.cell(row=i, column=1, value=a).font = Font(bold=True)
        w6.cell(row=i, column=2, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    postprocess.normalize_ooxml(path, P.INFRA_LEAD, P.INFRA_LEAD, "2026-11-05T08:14:00Z", "2026-11-06T16:52:27Z",
                                excel=True, company=P.ORG)


def note(path, G, fig, X):
    rows, late = order(G, fig)
    L = []
    L.append("# Seven H1 2027 runs will not finish inside their windows")
    L.append("")
    L.append("To: compute committee (Esa Airaksinen). From: Pia Kuosmanen, training infrastructure. 6 November 2026. "
             "Before the H1 2027 windows are locked.")
    L.append("")
    late_rows = [r for r in rows if r["run_id"] in late]
    fit_rows = [r for r in rows if r["run_id"] not in late]
    L.append("These will not reach their token budgets inside their windows (expected days against window days):")
    L.append("")
    for r in late_rows:
        k = r["run_id"]
        L.append("- %s: %.1f against %d, %.1f days past its window, finishing about %s" % (
            k, fig["days_%s" % k], r["window_days"], fig["short_%s" % k], fig["finish_%s" % k]))
    L.append("")
    L.append("These fit: " + "; ".join("%s (%.1f days against %d)" % (r["run_id"], fig["days_%s" % r["run_id"]],
                                                                    r["window_days"]) for r in fit_rows) + ".")
    L.append("")
    L.append("Every window was sized on the throughput benchmark, and the benchmark runs at conditions none of these "
             "runs will see. Four things make up most of the gap.")
    L.append("")
    L.append("1. **The step waits for the slowest rank.** Attention cost grows with the square of each document's "
             "length, and each step ends when the data-parallel rank holding the longest documents finishes. With one or "
             "two sequences per rank the slowest rank runs %.1f, %.1f and %.1f per cent over the mean rank for "
             "kide-13b-code-lc32, kide-34b-lc64 and kide-8b-lc64. The 2026 extension runs ran four sequences per rank "
             "on lighter mixes and never showed this." % (fig["overhead_pct_kide-13b-code-lc32"],
                                                        fig["overhead_pct_kide-34b-lc64"], fig["overhead_pct_kide-8b-lc64"]))
    L.append("2. **The scientific run pads.** Best-fit packing that keeps each paper whole fills %.1f per cent of each "
             "16k sequence on the kide-34b-sci mix, so the run needs %.1f more days for the same real tokens."
             % (100 * fig["fill_kide-34b-sci"], fig["bridge_kide-34b-sci_3"]))
    L.append("3. **Hall B is held to its contract.** Its jobs' steps stretch when the hall would draw past its %s kW "
             "(%.1f per cent at 20 per cent over, on 2026's %d capped days), and the research pool is what keeps "
             "the hall under it: the pool took about %d of the 512 unreserved nodes in 2026 when the reservations were light "
             "and none once they held 768 or more, so in February to mid-March, with 800 nodes reserved, the pool is "
             "off and the stretch is small (kide-34b-v3 %.1f per cent), and from the end of March, with 896 reserved "
             "and no pool, it is %.1f per cent on kide-13b-v4. That adds %.1f, %.1f and %.1f days to kide-120b-v1, "
             "kide-34b-v3 and kide-34b-16k."
             % (format(8100, ","), fig["throttle_pct_x20"], fig["capped_days_2026"], int(fig["pool_nodes_512"]),
                fig["stretch_pct_kide-34b-v3"], fig["stretch_pct_kide-13b-v4"], fig["bridge_kide-120b-v1_5"],
                fig["bridge_kide-34b-v3_5"], fig["bridge_kide-34b-16k_5"]))
    L.append("4. **A block across both pods runs slower.** The 2026 runs whose nodes sat in both of hall B's pods "
             "(%s) took %.1f per cent longer per step than their benchmark, mix and width predict, and the runs inside "
             "one pod did not. kide-8b-v4's block, %s and %s in the roadmap, is the only 2027 booking "
             "across the boundary: it adds %.1f days and is what puts a 75-day window at %.1f."
             % (", ".join(fig["pod_runs_2026"]), fig["pod_penalty_pct"], fig["pod_block_names"][0], fig["pod_block_names"][1],
                fig["bridge_kide-8b-v4_4"], fig["days_kide-8b-v4"]))
    L.append("")
    L.append("Works matter at the margin: in 2025 and 2026 major works ran %.2f times their planned hours, so the hall A "
             "re-cabling in March costs kide-34b-lc64 %.1f days, about twice what the notice's planned hours imply."
             % (fig["works_ratio_major"], fig["works_days_kide-34b-lc64"]))
    L.append("")
    L.append("**What I would change before the windows lock.** Extend each late window to its expected days, or remove "
             "the cause. For the three long-context runs, deal sequences to ranks by their attention cost rather than in "
             "turn. For kide-34b-sci, let papers split across sequences. For kide-8b-v4, give it a block inside one pod "
             "(kide-34b-16k at 192 nodes leaves pod 1 two rows free) or extend its window to %.0f days. Hall B's load "
             "in March and April is what the 120b and the 16k run on; take load out of it only if their windows "
             "cannot move." % fig["days_kide-8b-v4"])
    L.append("")
    L.append("2026 bears this out: the runs held %s GPU-days against the %s their benchmarks implied. Waiting for the "
             "slowest rank added %s, blocks across both pods %s, interruptions and restarts %s, hall B's cap %s and "
             "provider works %s; shorter documents than the benchmark's corpus gave back %s. The workbook has every "
             "run's bridge and range."
             % (format(int(fig["b26_10"]), ","), format(int(fig["b26_0"]), ","), format(int(fig["b26_2"]), ","),
                format(int(fig["b26_4"]), ","), format(int(fig["b26_7"]), ","), format(int(fig["b26_5"]), ","),
                format(int(fig["b26_8"]), ","), format(int(-fig["b26_1"]), ",")))
    L.append("")
    L.append("Days are counted from 00:00 UTC on each window's start, as CAR-2027-1 counts them, and every late block "
             "is kept until its run finishes, which is what keeps hall B loaded into April. The ranges in the workbook "
             "are four-in-five ranges from the 2026 record's own spread.")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")


def write(golden_dir, G, fig, X):
    if os.path.isdir(golden_dir):
        for f in os.listdir(golden_dir):
            os.remove(os.path.join(golden_dir, f))
    os.makedirs(golden_dir, exist_ok=True)
    workbook(os.path.join(golden_dir, "h1_2027_throughput_bridge.xlsx"), G, fig, X)
    note(os.path.join(golden_dir, "h1_2027_run_windows_note.md"), G, fig, X)
