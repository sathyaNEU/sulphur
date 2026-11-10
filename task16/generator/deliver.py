"""The golden deliverables: the workbook and the short note the prompt asks for, written from golden.compute().

    write_all(G, F, golden_dir, scratch) -> the two file paths

Every number comes from G (unrounded working) or F (the figures as stated); nothing is typed. The workbook and the
note pass through the house container writer, each with its own stamps after the pack's as-of date.
"""
import math
import os

import numpy as np
import openpyxl
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Mm, Pt, RGBColor
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A
import postprocess
import results as RS
import sweep as S

WORKBOOK = "scale_up_forecast.xlsx"
NOTE = "proposal_evidence_note.docx"
ORG = "MML group"
AUTHOR = "Magne Aas"
STAMPS = {WORKBOOK: ("2026-11-06T08:17:00Z", "2026-11-09T14:52:00Z"), NOTE: ("2026-11-09T09:40:00Z", "2026-11-09T15:26:00Z")}

INK, INK2, GRID = "#0b0b0b", "#52514e", "#e3e2de"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"     # validated together (dataviz palette, light surface)
HEAD_FILL = PatternFill("solid", fgColor="E9EEF4")
THIN = Side(style="thin", color="B8BEC6")
ROUTE = {"A": "expert labels only", "B": "expert and contractor labels", "C": "expert, contractor and map-transfer labels",
         "D": "expert and map-transfer labels"}


def lr_text(x):
    m, e = ("%.2e" % x).split("e")
    m = m.rstrip("0").rstrip(".")
    return "%se%d" % (m, int(e))


def opt_by_key():
    return {o["key"]: o for o in S.SHORTLIST}


# ------------------------------------------------------------------------------------------------------ workbook
def _head(ws, row, labels, widths=None):
    for j, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=t)
        c.font = Font(bold=True, size=10)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(size=10, color="52514E")


def write_workbook(path, G, F):
    g = G["golden"]; yr = G["yr"]; rm = G["rm"]; fc = G["fc"]
    opts = opt_by_key()
    wb = openpyxl.Workbook()

    # 1. the ranking
    ws = wb.active; ws.title = "Ranking"
    _title(ws, "NSSMP 2027 slot: name option %s, expected benchmark log loss %.3f (four in five between %.3f and %.3f)"
           % (F["call"], F["expected"][F["call"]], F["range_low"], F["range_high"]),
           "Expected benchmark log loss of the final checkpoint for one run of each shortlisted configuration. "
           "Pilot exports of 4 November 2026.")
    _head(ws, 4, ["Rank", "Option", "Hidden width", "Expert points", "Contractor points", "Map-transfer points",
                  "Learning rate", "Expected benchmark log loss", "Four in five, low", "Four in five, high",
                  "Gap to option %s" % F["call"], "Comment"], [6, 8, 9, 11, 12, 13, 11, 13, 10, 10, 10, 58])
    order = g["call"]["order"]
    comment = {
        "B": "Named. The pilot ran these labels at widths 128 and 256; one further width step is carried.",
        "A": "Learning rate from the width rule (sheet Learning rate); the pilot's own 1,024-wide job did not finish.",
        "C": "Past the pilot's largest trial: the level is carried on the curve of sheet Levels, the routes' costs at this mix.",
        "D": "As C without the contractor's lot.",
    }
    for i, k in enumerate(order, 1):
        o = opts[k]; r = 4 + i
        lr = o["lr"] if o["lr"] is not None else F["lr_1024"]
        vals = [i, k, o["width"], o["nA"], o["nB"], o["nC"], lr, g["expected"][k],
                g["range"]["low"] if k == F["call"] else None, g["range"]["high"] if k == F["call"] else None,
                g["expected"][k] - g["expected"][F["call"]] if k != F["call"] else None, comment[k]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j in (4, 5, 6):
                c.number_format = "#,##0"
            elif j == 7:
                c.number_format = "0.0E+00"
            elif j in (8, 9, 10, 11):
                c.number_format = "0.000"
            if j == 12:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        if k == F["call"]:
            for j in range(1, 12):
                ws.cell(row=r, column=j).font = Font(bold=True)
    ws["A10"] = ("Options ranked 2 to 4 sit within %.3f of each other, less than the forecast can separate; their order "
                 "is not a finding." % (max(g["expected"][k] for k in order[1:]) - min(g["expected"][k] for k in order[1:])))
    ws["A10"].font = Font(italic=True, size=9)
    under = [
        ("Benchmark loss matching the width-128 trial on 128,000 expert plus 384,000 map-transfer labels", g["trial"]["exp128k_map384k"], "0.000"),
        ("Added to the benchmark loss by each tenth of a training set moved from expert to contractor labels", g["costs"]["ctr_per10"], "0.0000"),
        ("Added by each tenth moved from expert to map-transfer labels", g["costs"]["map_per10"], "0.0000"),
        ("Benchmark loss 512,000 expert labels would give at width 128 and learning rate 0.002", g["level"], "0.000"),
    ]
    ws["A12"] = "Underneath"; ws["A12"].font = Font(bold=True)
    for i, (label, v, fmt) in enumerate(under, 13):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=7)
        ws.cell(row=i, column=1, value=label).alignment = Alignment(wrap_text=True, vertical="top")
        c = ws.cell(row=i, column=8, value=v)
        c.number_format = fmt
        c.alignment = Alignment(vertical="top")
        ws.row_dimensions[i].height = 30
    ws.freeze_panes = "C5"

    # 2. the figures underneath
    ws = wb.create_sheet("Drivers")
    _title(ws, "What the ranking rests on")
    _head(ws, 3, ["Quantity", "Value", "Unit or basis"], [74, 12, 64])
    rows = [
        ("Benchmark loss matching the width-128 trial on 128,000 expert plus 384,000 map-transfer labels", g["trial"]["exp128k_map384k"],
         "expert-item loss carried to the benchmark on the %d scored final checkpoints" % F["cal_n"], "0.000"),
        ("Added to the benchmark loss by each tenth of a training set moved from expert to contractor labels", g["costs"]["ctr_per10"],
         "same examples, width and learning rate", "0.0000"),
        ("Added by each tenth moved from expert to map-transfer labels", g["costs"]["map_per10"], "same examples, width and learning rate", "0.0000"),
        ("Benchmark loss 512,000 expert labels would give at width 128, learning rate 0.002", g["level"],
         "the two 512,000-example trials with each route's cost taken out", "0.000"),
        ("Run-to-run spread of one run", g["range"]["parts"]["run"], "standard deviation within pilot cells", "0.0000"),
        ("Forecast error on the runs held back", g["range"]["parts"]["forecast"], "root mean square", "0.0000"),
        ("Yardstick error", g["range"]["parts"]["yardstick"], "residual of the benchmark on the expert-item loss, scored runs", "0.0000"),
        ("Mean absolute gap to the pilot configurations above 256,000 examples, forecast built without them", g["heldback"],
         "three configurations (sheet Held back)", "0.0000"),
        ("Learning rate option A is forecast at", g["rate"], "each width's best rate carried one doubling (sheet Learning rate)", "0.0E+00"),
        ("Pilot run records", F["run_records"], "tracking server export", "0"),
        ("Runs that finished their schedule", F["runs_finished"], "status FINISHED and last logged step equal to the schedule", "0"),
        ("Finished runs with item scores of the final checkpoint", F["runs_with_item_scores"], "one dump lost to the scratch quota", "0"),
        ("Benchmark rows for the team", F["bench_rows"], "benchmark server export", "0"),
        ("Final checkpoints the benchmark scored", F["bench_final"],
         "%d rows scored a part-way checkpoint and %d repeat an upload" % (F["bench_part_way"], F["bench_repeats"]), "0"),
    ]
    for i, (a, v, b, fmt) in enumerate(rows, 4):
        ws.cell(row=i, column=1, value=a).alignment = Alignment(wrap_text=True, vertical="top")
        c = ws.cell(row=i, column=2, value=v); c.number_format = fmt
        ws.cell(row=i, column=3, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A4"

    # 3. the level by total examples
    ws = wb.create_sheet("Levels")
    _title(ws, "Benchmark log loss on expert-quality labels at width 128, learning rate 0.002, by training-set size")
    _head(ws, 3, ["Examples", "Benchmark log loss", "Gain on the previous doubling", "Read from"], [12, 12, 14, 70])
    lv = g["_levels"]; ks = sorted(lv)
    trial_totals = {sum(k) for k in rm["cells"]}
    f128 = fc["f128"]
    r = 4
    for i, n in enumerate(ks):
        if n in trial_totals:
            src = "the trials at this size with each route's cost taken out"
        elif n == 32000:
            src = "expert-label runs at this size, at the trials' learning rate"
        else:
            src = "expert-label ladder, put on the trials' learning rate"
        vals = [n, lv[n], (lv[ks[i - 1]] - lv[n]) if i else None, src]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            c.number_format = "#,##0" if j == 1 else "0.000"
        r += 1
    for n in (1024000, 1152000, 1280000):
        vals = [n, f128(n), None, "carried on: each doubling returns %.2f of the one before" % g["_form"]["ratio"]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            c.number_format = "#,##0" if j == 1 else "0.000"
            c.font = Font(italic=True)
        r += 1
    ws.freeze_panes = "A4"

    # 4. the vendor-label trials
    ws = wb.create_sheet("Trials")
    _title(ws, "Vendor-label trials at width 128: benchmark-equivalent loss against the level at the same size",
           "Each total has a level of its own; the routes' costs come from the contrasts between mixes at one total. "
           "The expert-label run at 128,000 examples and the trials' rate stands in the fit as a mix with no vendor labels.")
    _head(ws, 4, ["Expert points", "Contractor points", "Map-transfer points", "Total", "Runs", "Benchmark-equivalent loss",
                  "Expert level at this total", "Excess", "Share cost fitted", "Residual"], [11, 12, 13, 11, 6, 13, 12, 9, 11, 9])
    r = 5
    for (a, b, c), (m, n) in sorted(rm["cells"].items(), key=lambda kv: (sum(kv[0]), kv[0][1], kv[0][2])):
        t = a + b + c
        cost = rm["kB"] * b / t + rm["kC"] * c / t
        vals = [a, b, c, t, n, m, rm["levels"][t], m - rm["levels"][t], cost, m - rm["levels"][t] - cost]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.number_format = "#,##0" if j <= 4 else ("0" if j == 5 else "0.0000")
        r += 1
    ws.cell(row=r + 1, column=1, value="Cost of a full training set of contractor labels in place of expert labels")
    ws.cell(row=r + 1, column=6, value=rm["kB"]).number_format = "0.000"
    ws.cell(row=r + 2, column=1, value="Cost of a full training set of map-transfer labels in place of expert labels")
    ws.cell(row=r + 2, column=6, value=rm["kC"]).number_format = "0.000"
    ws.freeze_panes = "A5"

    # 5. the check on the runs held back
    ws = wb.create_sheet("Held back")
    _title(ws, "The forecast built from runs of 256,000 examples or fewer, against the pilot's larger configurations")
    _head(ws, 3, ["Hidden width", "Expert points", "Contractor points", "Map-transfer points", "Runs", "Forecast",
                  "Observed", "Gap"], [9, 11, 12, 13, 6, 10, 10, 10])
    r = 4
    for (w, a, b, c), (fv, ov, n) in sorted(G["held"]["top"].items()):
        for j, v in enumerate([w, a, b, c, n, fv, ov, fv - ov], 1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.number_format = "#,##0" if j in (2, 3, 4) else ("0" if j in (1, 5) else "0.0000")
        r += 1
    ws.cell(row=r + 1, column=1, value="Mean absolute gap, this forecast"); ws.cell(row=r + 1, column=6, value=g["heldback"]).number_format = "0.0000"
    alt = [("the same levels, a floor fitted by least squares to every level", G["ls_floor"]["heldback"]),
           ("the same levels, a quadratic in log examples", G["rivals"][RS.QUADRATIC]["heldback"]),
           ("the ladder's straight line carried on", G["also"]["the straight line through the levels"]["heldback"]),
           ("one curve fitted through every run", G["careful"]["heldback"])]
    for i, (name, v) in enumerate(alt, 2):
        ws.cell(row=r + i, column=1, value="Mean absolute gap, %s" % name)
        ws.cell(row=r + i, column=6, value=v).number_format = "0.0000"
    ws.freeze_panes = "A4"

    # 6. the learning rate
    ws = wb.create_sheet("Learning rate")
    _title(ws, "Best learning rate by width, from the week 42 check at 32,000 expert examples")
    _head(ws, 3, ["Hidden width", "Best rate", "Rates tried", "Note"], [9, 11, 40, 48])
    opt = g["_lr_opt"]
    tried = {}
    for q in yr:
        if q["nA"] == 32000 and q["nB"] + q["nC"] == 0:
            tried.setdefault(q["width"], set()).add(q["lr"])
    r = 4
    for w in sorted(opt):
        ws.cell(row=r, column=1, value=w)
        ws.cell(row=r, column=2, value=opt[w]).number_format = "0.0E+00"
        ws.cell(row=r, column=3, value=", ".join(lr_text(x) for x in sorted(tried[w])))
        ws.cell(row=r, column=4, value="lowest point of a curve through the rates round the best")
        r += 1
    ws.cell(row=r, column=1, value=1024)
    ws.cell(row=r, column=2, value=g["rate"]).number_format = "0.0E+00"
    ws.cell(row=r, column=4, value="the best rate falls as width to the power %.1f" % g["rate_exponent"])
    for j in (1, 2, 4):
        ws.cell(row=r, column=j).font = Font(bold=True)
    ws.freeze_panes = "A4"

    # 7. what other routes give
    ws = wb.create_sheet("Routes")
    _title(ws, "What other ways of reading the pilot give, beside this forecast")
    _head(ws, 3, ["Route", "A", "B", "C", "D", "Names", "Note"], [58, 8, 8, 8, 8, 8, 74])
    lead = lambda res: "names the same option, by %.3f" % res["call"]["margin"]
    routes = [
        ("This forecast", g, "-"),
        ("The same, with the level at or under the expert pool taken from the expert-label runs (the ladder put on the trials' rate)", G["pool"],
         "a sound reading: contractor %.4f and map transfer %.4f a tenth; %s" % (G["pool"]["costs"]["ctr_per10"], G["pool"]["costs"]["map_per10"], lead(G["pool"]))),
        ("The same, with every run on the carried expert-item loss, the benchmark's own scores set aside", G["carried"],
         "a sound reading: moves option A most, whose 512-wide runs the benchmark scored; %s" % lead(G["carried"])),
        ("The same, the last doubling's gain carried on undiminished past 512,000 examples", G["bound_last"],
         "the most the examples past the largest trial can be taken to return; %s" % lead(G["bound_last"])),
        ("The same, no gain past 512,000 examples", G["bound_none"],
         "the least they can return; %s" % lead(G["bound_none"])),
        ("The same levels, a floor fitted by least squares to every level", G["ls_floor"],
         "lands at the first of those two bounds; %s" % lead(G["ls_floor"])),
        ("Logged development loss carried to the benchmark, the ladder's straight line", G["quick"],
         "not used: the logged loss is scored on a split a quarter of whose items carry a vendor's label; it runs %.2f to %.2f above the benchmark-equivalent loss for expert-label runs and %.2f to %.2f for map mixes"
         % (F["hurried"]["logged_gap_expert"][0], F["hurried"]["logged_gap_expert"][1], F["hurried"]["logged_gap_map"][0], F["hurried"]["logged_gap_map"][1])),
        ("One scaling curve fitted through every run (the best of a line, a quadratic and a floor)", G["careful"],
         "not used: it misses the configurations above 256,000 examples by %.3f when built without them, every miss on the same side, and puts C below what the last doubling's gain carried on gives" % G["careful"]["heldback"]),
        ("The ladder's straight line carried past the expert pool", G["line"],
         "not used: the 512,000-example trials sit %.3f above it once the routes' costs are out" % (g["level"] - G["line"]["level"])),
        ("The two vendor routes read as one", G["one_vendor"],
         "not used: the contractor's labels cost %.4f a tenth and the map-transfer labels %.4f" % (g["costs"]["ctr_per10"], g["costs"]["map_per10"])),
    ]
    r = 4
    for name, res, why in routes:
        ws.cell(row=r, column=1, value=name).alignment = Alignment(wrap_text=True, vertical="top")
        for j, k in enumerate("ABCD", 2):
            ws.cell(row=r, column=j, value=res["expected"][k]).number_format = "0.000"
        ws.cell(row=r, column=6, value=res["call"]["pick"])
        ws.cell(row=r, column=7, value=why).alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    ws.cell(row=r, column=1, value="Only the runs the benchmark scored")
    ws.cell(row=r, column=2, value=G["scored_only"]["expected"]["A"]).number_format = "0.000"
    ws.cell(row=r, column=6, value="A")
    ws.cell(row=r, column=7, value="no vendor-label run was scored, so B, C and D get no figure at all")
    for j in range(1, 8):
        ws.cell(row=4, column=j).font = Font(bold=True)
    ws.freeze_panes = "B4"

    # 8. the runs
    ws = wb.create_sheet("Runs")
    _title(ws, "Finished pilot runs with item scores (%d)" % len(yr))
    _head(ws, 3, ["Run id", "Run name", "Hidden width", "Learning rate", "Expert points", "Contractor points",
                  "Map-transfer points", "Logged development loss", "Loss on expert items", "Benchmark score",
                  "Benchmark-equivalent loss", "Read from"], [11, 40, 9, 10, 11, 12, 13, 12, 11, 11, 13, 22])
    r = 4
    for q in sorted(yr, key=lambda q: (q["stage"] != "ladder", q["stage"], q["width"], A.total(q), q["nB"], q["nC"], q["lr"], q["seed"])):
        vals = [q["run_id"], q["name"], q["width"], q["lr"], q["nA"], q["nB"], q["nC"], q["dev"], q["devE"], q["bench"], q["y"],
                "benchmark score" if q["bench"] is not None else "expert items, carried"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j == 4:
                c.number_format = "0.0E+00"
            elif j in (5, 6, 7):
                c.number_format = "#,##0"
            elif j in (8, 9, 10, 11):
                c.number_format = "0.0000"
        r += 1
    ws.freeze_panes = "C4"
    ws.auto_filter.ref = "A3:L%d" % (r - 1)

    # 9. notes
    ws = wb.create_sheet("Notes")
    ws.column_dimensions["A"].width = 118
    notes = [
        "Basis: tracking, scheduler, store and benchmark exports of 2 to 4 November 2026; shortlist and slot rules from the group meeting of 5 November.",
        "Benchmark log loss: the benchmark's mean log loss of a final checkpoint over its %s points. %d pilot runs carry their own score." % ("{:,}".format(20000), F["cal_n"]),
        "For every other run the loss on the %s expert-labelled development items is carried to the benchmark: benchmark = %.4f + %.3f x expert-item loss on the scored runs, residual %.4f."
        % ("{:,}".format(F["dev_expert_items"]), G["cal"]["a"], G["cal"]["b"], G["cal"]["sd"]),
        "A run counts as finished when its status is FINISHED and its last logged step equals its schedule. A step logged twice by a resumed job is read from the later row.",
        "Examples are labelled points in the training set, counted from the shard register; the superseded receipt of contractor shard 19 is counted once.",
        "A route's cost is read against expert-label runs of the same size, width and learning rate. The size ladder ran at tabled rates, about %.3f above the trials' rate at width 128; it is put on the trials' rate before the comparison."
        % F["hurried"]["lr_cost_128"],
        "Expected loss is for one run of the stated recipe (batch 128, twelve epochs, cosine schedule, final checkpoint). The range is for that single run: run-to-run spread, the forecast's error on the held-back runs and the yardstick's error, combined.",
        "No vendor-label run was scored by the benchmark, and no pilot run used the contractor's lot together with map-transfer labels; option C rests on the two routes' costs adding.",
    ]
    ws["A1"] = "Notes"; ws["A1"].font = Font(bold=True, size=12)
    for i, t in enumerate(notes, 3):
        c = ws.cell(row=i, column=1, value=t); c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    created, modified = STAMPS[WORKBOOK]
    postprocess.normalize_ooxml(path, AUTHOR, AUTHOR, created, modified, excel=True, company=ORG)


# --------------------------------------------------------------------------------------------------------- chart
def write_chart(path, G, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    g = G["golden"]; fc = G["fc"]
    lv = g["_levels"]; ks = sorted(lv)
    line = A.ladder_line(G["yr"], 128, "y", "matched")[0]
    xs_line = np.array([8000, 1280000], float)
    xs_curve = np.geomspace(512000, 1280000, 40)
    fig, ax = plt.subplots(figsize=(6.4, 3.7), dpi=200)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    ax.plot(xs_line, [line(x) for x in xs_line], color=ORANGE, lw=2, ls=(0, (5, 3)), solid_capstyle="round",
            label="Size ladder's straight line, carried on", zorder=2)
    ax.plot(ks, [lv[k] for k in ks], color=BLUE, lw=2, solid_capstyle="round", solid_joinstyle="round", zorder=3)
    ax.plot(ks, [lv[k] for k in ks], ls="none", marker="o", ms=7.5, mfc=BLUE, mec="white", mew=1.6,
            label="Level on expert-quality labels, from the pilot", zorder=4)
    ax.plot(xs_curve, [fc["f128"](x) for x in xs_curve], color=AQUA, lw=2, solid_capstyle="round", label="Forecast curve", zorder=3)
    ax.plot([1280000], [fc["f128"](1280000)], ls="none", marker="o", ms=7.5, mfc=AQUA, mec="white", mew=1.6, zorder=4)
    ax.set_xscale("log", base=2)
    ticks = [8000, 32000, 128000, 512000, 1280000]
    ax.set_xticks(ticks); ax.set_xticklabels(["8K", "32K", "128K", "512K", "1.28M"])
    ax.set_xlim(6500, 1900000)
    ax.set_ylim(0.44, 0.98)
    ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9])
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, length=0, labelsize=8)
    ax.set_xlabel("Labelled examples in the training set (log scale)", color=INK2, fontsize=8)
    ax.set_ylabel("Benchmark log loss, width 128", color=INK2, fontsize=8)
    ax.annotate("%.3f" % lv[512000], (512000, lv[512000]), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=8, color=INK)
    ax.annotate("%.3f" % lv[128000], (128000, lv[128000]), textcoords="offset points", xytext=(4, 8), ha="left", fontsize=8, color=INK)
    ax.annotate("%.3f" % fc["f128"](1280000), (1280000, fc["f128"](1280000)), textcoords="offset points", xytext=(8, 2), ha="left", fontsize=8, color=INK)
    ax.annotate("%.3f" % line(1280000), (1280000, line(1280000)), textcoords="offset points", xytext=(8, -3), ha="left", fontsize=8, color=INK)
    ax.set_title("More examples return less past 128,000: %.3f, then %.3f a doubling" % (F["gain_first"], F["gain_second"]),
                 loc="left", fontsize=9.5, color=INK, pad=10)
    leg = ax.legend(loc="upper right", frameon=False, fontsize=8, handlelength=2.4)
    for t in leg.get_texts():
        t.set_color(INK2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------- note
def note_paragraphs(G, F):
    """The note's prose, built from the figures (also read by the checks, so the words and the numbers cannot part)."""
    g = G["golden"]; h = F["hurried"]; ex = F["expected"]
    call = F["call"]
    p = {}
    p["title"] = "Name option %s for the February slot: expected benchmark log loss %.3f, four in five between %.3f and %.3f" % (
        call, ex[call], F["range_low"], F["range_high"])
    p["call"] = ("Name option %s, the %d-wide model on our 128,000 expert labels and Lyngvær's 128,000, at the learning rate we "
                 "already took for that width. I expect its final checkpoint to score %.3f on the benchmark, and one run to "
                 "land between %.3f and %.3f four times in five. The other three options come out at %.3f (A), %.3f (C) and "
                 "%.3f (D), all at least %.3f behind on this forecast, and behind under every reading of the pilot I can "
                 "defend." % (call, F["call_width"], ex[call], F["range_low"], F["range_high"], ex["A"], ex["C"], ex["D"],
                              F["margin"]))
    p["notc"] = ("Option C is the one our own tracking plots favour, and it is the one to leave out. The logged development "
                 "loss puts it first by a wide margin, but that loss is scored on a split a quarter of whose items carry a "
                 "vendor's label, so a model trained on a vendor's labels is partly marked against them. Scored on the "
                 "expert-labelled items and carried to the benchmark on the %d final checkpoints the programme scored, a "
                 "single scaling curve through all the pilot runs still puts C first, at %.3f against %.3f for %s. That curve "
                 "does not survive its own check: built without the pilot's configurations above 256,000 examples it misses "
                 "them by %.3f, every one on the optimistic side." % (F["cal_n"], h["careful_expected"]["C"],
                                                                     h["careful_expected"][call], call, h["careful_gap"]))
    p["how"] = ("The large trials sit above the size ladder for two reasons at once, and they have to be separated before "
                "anything is carried further. Read from mixes at the same size, width and learning rate, contractor labels "
                "cost %.4f for each tenth of the training set they replace and map-transfer labels %.4f. "
                "With those costs taken out of the trials at 256,000 and 512,000 examples, expert-quality labels would give "
                "%.3f and %.3f at width 128: a doubling that returned about %.3f up to the expert pool returns %.3f and then "
                "%.3f. Carrying that on, and checking it the same way, misses the held-back configurations by %.4f."
                % (F["cost_ctr"], F["cost_map"], F["level_256k"], F["level_512k"], F["gain_ladder"], F["gain_first"],
                   F["gain_second"], F["gap"]))
    p["rest"] = ("So the million map-transfer labels buy less than they cost: at option C's mix they add about %.3f to the "
                 "loss while the extra examples take off about %.3f. Option A needs a learning rate; the best rate falls with "
                 "width and the rule gives %s for 1,024. The range round %s combines the spread between runs (%.4f), the "
                 "forecast's error on the held-back runs (%.4f) and the error of carrying expert-item loss to the benchmark "
                 "(%.4f). Four things the pilot cannot tell us: no vendor-label run was ever scored by the benchmark; no "
                 "run used Lyngvær's lot together with the map labels, so C rests on the two costs adding; no run took "
                 "%s's labels to width 512, and the step I carry (%.3f) rests on the benchmark's scores of %s runs (read on "
                 "the carried loss instead, %s would be %.3f, still first); and what the examples past our largest trial "
                 "return can only be bounded. With the last doubling's gain carried on undiminished C comes out at %.3f, "
                 "with no further gain at %.3f, and %s is ahead either way."
                 % (G["fc"]["forecast"]["C"]["cost"], G["fc"]["level"](256, 256000) - G["fc"]["forecast"]["C"]["level"],
                    lr_text(F["lr_1024"]), call, F["range_parts"]["run"], F["range_parts"]["forecast"], F["range_parts"]["yardstick"],
                    call, F["width_step_512"], {2: "two", 3: "three", 4: "four"}.get(F["width_step_512_runs"], str(F["width_step_512_runs"])), call, F["carried_B"],
                    F["bounds"]["C"][0], F["bounds"]["C"][1], call))
    p["caption"] = ("Benchmark log loss on expert-quality labels at width 128 and learning rate 0.002. Points to 32,000 "
                    "examples are expert-label runs; from 64,000 on they are the trials at that size with each route's cost "
                    "taken out.")
    p["source"] = "Source: tracking, store and benchmark exports of 4 November 2026; workings in %s." % WORKBOOK
    return p


def write_note(path, G, F, png):
    P_ = note_paragraphs(G, F)
    g = G["golden"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(24); sec.top_margin = Mm(22); sec.bottom_margin = Mm(20)
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    hp = sec.header.paragraphs[0]; hp.text = "MML group, NSSMP 2027 slot"; hp.runs[0].font.size = Pt(8); hp.runs[0].font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
    t = doc.add_paragraph(); r = t.add_run(P_["title"]); r.bold = True; r.font.size = Pt(13)
    for k, v in (("To", "Helene Svendsen"), ("From", "Magne Aas"), ("Date", "9 November 2026"),
                 ("Re", "which configuration the proposal names, and the loss and range it states")):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
        a = p.add_run("%s: " % k); a.bold = True
        p.add_run(v)
    doc.add_paragraph()
    for key in ("call", "notc", "how"):
        p = doc.add_paragraph(P_[key]); p.paragraph_format.space_after = Pt(6)
    doc.add_picture(png, width=Mm(150))
    c = doc.add_paragraph(P_["caption"]); c.runs[0].font.size = Pt(8.5); c.runs[0].italic = True
    p = doc.add_paragraph(P_["rest"]); p.paragraph_format.space_after = Pt(6)
    opts = opt_by_key()
    tb = doc.add_table(rows=1, cols=5)
    tb.style = "Light Grid Accent 1"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Option", "Hidden width", "Labels", "Learning rate", "Expected benchmark log loss"]):
        tb.rows[0].cells[j].text = h
    for k in g["call"]["order"]:
        o = opts[k]
        cells = tb.add_row().cells
        cells[0].text = k
        cells[1].text = "{:,}".format(o["width"])
        cells[2].text = "{:,} points, {}".format(o["nA"] + o["nB"] + o["nC"], ROUTE[k])
        cells[3].text = lr_text(o["lr"] if o["lr"] is not None else F["lr_1024"])
        cells[4].text = "%.3f" % g["expected"][k] + (" (%.3f to %.3f)" % (F["range_low"], F["range_high"]) if k == F["call"] else "")
    for row in tb.rows:
        for cell in row.cells:
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(9)
    s = doc.add_paragraph(P_["source"]); s.runs[0].font.size = Pt(8.5)
    doc.save(path)
    created, modified = STAMPS[NOTE]
    postprocess.normalize_docx(path, AUTHOR, AUTHOR, created[:16] + ":00Z", modified[:16] + ":00Z", 6, 87, "task16-note",
                               title="NSSMP 2027 slot: configuration to name", company=ORG)


def write_all(G, F, golden_dir, scratch):
    os.makedirs(golden_dir, exist_ok=True)
    png = os.path.join(scratch, "levels.png")
    write_chart(png, G, F)
    wbp = os.path.join(golden_dir, WORKBOOK)
    ntp = os.path.join(golden_dir, NOTE)
    write_workbook(wbp, G, F)
    write_note(ntp, G, F, png)
    return wbp, ntp, png
