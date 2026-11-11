"""The golden deliverables: saarnela_peak_plan_2027.xlsx (the plan by week and zone, the volumes, the forecast record,
the time a line and the routes) and saarnela_peak_plan_2027.docx (the one-page memo for the management team), both
from analysis.py's figures on the shipped pack, written by the house writers."""
import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Mm, Pt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)

import analysis as A  # noqa: E402
import params as P  # noqa: E402

XLSX = "saarnela_peak_plan_2027.xlsx"
DOCX = "saarnela_peak_plan_2027.docx"
WEEKS = list(P.PEAK_WEEKS)
FIXES = ("calendar", "calibration", "congestion", "huippu")
FIX_NAME = {"calendar": "the 2027 weeks re-keyed to their dates", "calibration": "the overstatement read from the plan's growth",
            "congestion": "the time a line at the zone limit", "huippu": "Huippu Sport at its full assortment"}


def r10(x):
    return int(round(x / 10.0) * 10)


def pct(x, nd=1):
    return round(100.0 * x, nd)


def compute(target):
    f = A.load(target)
    G = A.golden(f)
    z = A.zone_hours(f)
    rg, sd = A.ranges(f, z, G)
    H = A.hurried(f)
    routes = {fx: A.hurried(f, (fx,)) for fx in FIXES}
    figs = {
        "evening": {zz: [w for w in WEEKS if G["evening"][(zz, w)]] for zz in A.Z_SMALL},
        "day_only": {zz: [w for w in WEEKS if not G["evening"][(zz, w)]] for zz in A.Z_SMALL},
        "r1": {zz: int(round(G["r1"][zz])) for zz in P.ZONES},
        "logged_share": round(G["logged_share"], 3),
        "r2": pct(G["r2"]),
        "r3": round(G["r3"], 2),
        "r4": round(G["r4"], 2),
        "t_hui": round(G["t_hui"], 2), "t_kot": round(G["t_kot"], 2),
        "r5": {k: pct(v) for k, v in G["r5"].items()},
        "plan_growth": {"K": [pct(v, 0) for v in A.plans_2027(f)[0]], "H": [pct(v, 0) for v in A.plans_2027(f)[1]]},
        "r6": pct(G["r6"]), "r6_budget": pct(G["r6_budget"]),
        "hours": {zz: {w: r10(G["plan"][(zz, w)]["hours"]) for w in WEEKS} for zz in P.ZONES},
        "range": {zz: {w: [r10(rg[(zz, w)][0]), r10(rg[(zz, w)][1])] for w in WEEKS} for zz in P.ZONES},
        "ratio": {zz: {w: round(G["plan"][(zz, w)]["ratio"], 2) for w in WEEKS} for zz in A.Z_SMALL},
        "lines": {zz: {w: r10(G["plan"][(zz, w)]["lines"]) for w in WEEKS} for zz in P.ZONES},
        "lines_split": {zz: {w: [round(G["plan"][(zz, w)]["lines_k"]), round(G["plan"][(zz, w)]["lines_h"])]
                             for w in WEEKS} for zz in A.Z_SMALL},
        "agency": {w: r10(G["agency"][w]) for w in WEEKS},
        "agency_total": r10(sum(G["agency"].values())),
        "own": {w: {zz: r10(G["own"][w][zz]) for zz in P.ZONES} for w in WEEKS},
        "sd": {k: round(v, 4) for k, v in sd.items()},
        "fit": {"knot": G["fit"]["knot"], "power": G["fit"]["power"],
                "coef": {k: round(float(v), 4) for k, v in G["fit"]["coef"].items()}},
        "hurried": {"evening": {zz: [w for w in WEEKS if H["evening"][(zz, w)]] for zz in A.Z_SMALL},
                    "agency": {w: r10(H["agency"][w]) for w in WEEKS}, "agency_total": r10(sum(H["agency"].values())),
                    "r4": round(H["r4"], 2), "pilot_t": round(H["pilot_t"], 2), "p2_t": round(H["p2_t"], 2),
                    "r2_applied": pct(H["r2"]),
                    "hours": {zz: {w: r10(H["plan"][(zz, w)]["hours"]) for w in WEEKS} for zz in P.ZONES},
                    "rate": {zz: round(H["rate"][zz], 3) for zz in P.ZONES}},
        "routes": {fx: {"evening": {zz: [w for w in WEEKS if R["evening"][(zz, w)]] for zz in A.Z_SMALL},
                        "agency_total": r10(sum(R["agency"].values()))} for fx, R in routes.items()},
    }
    return f, G, figs, rg


def _head(ws, row, fill="D9E1EA"):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, widths):
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd


def weeks_text(ws_):
    if not ws_:
        return "none"
    if len(ws_) > 2 and ws_ == list(range(ws_[0], ws_[-1] + 1)):
        return "%d to %d" % (ws_[0], ws_[-1])
    if len(ws_) == 2:
        return "%d and %d" % tuple(ws_)
    return ", ".join(str(w) for w in ws_)


def wk_phrase(ws_):
    if not ws_:
        return "in no week"
    return ("week %s" if len(ws_) == 1 else "weeks %s") % weeks_text(ws_)


def write_xlsx(path, f, G, figs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan"
    ws.append(["Saarnela peak 2027: picker hours by zone and week, the evening shifts and the agency booking"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Evening shift: P1 weeks %s; P2 weeks %s. Agency hours over the peak: %s." % (
        weeks_text(figs["evening"]["P1"]), weeks_text(figs["evening"]["P2"]), "{:,}".format(figs["agency_total"]).replace(",", " "))])
    ws.append([])
    ws.append(["ISO week 2027", "Zone", "Lines", "Day-shift capacity at the limit (lines)", "Evening shift",
               "Picker hours", "80% range, low", "80% range, high", "Own picker hours", "Agency hours"])
    _head(ws, 4)
    for w in WEEKS:
        for zz in P.ZONES:
            p = G["plan"][(zz, w)]
            cap = r10(p["cap"]) if zz != "B1" else None
            ev = ("yes" if p["evening"] else "no") if zz != "B1" else "n/a"
            ag = max(0.0, p["hours"] - G["own"][w][zz])
            ws.append([w, zz, figs["lines"][zz][w], cap, ev, figs["hours"][zz][w], figs["range"][zz][w][0],
                       figs["range"][zz][w][1], figs["own"][w][zz], r10(ag)])
    ws.append([])
    ws.append(["ISO week 2027", "Agency hours to book"])
    _head(ws, ws.max_row)
    for w in WEEKS:
        ws.append([w, figs["agency"][w]])
    ws.append(["Peak", figs["agency_total"]])
    ws.freeze_panes = "A5"
    _widths(ws, [13, 7, 11, 22, 13, 13, 14, 14, 16, 13])
    for row in ws.iter_rows(min_row=5):
        for c in row:
            if isinstance(c.value, (int, float)) and c.column > 2:
                c.number_format = "#,##0"

    ws = wb.create_sheet("Volumes")
    ws.append(["Order lines by week: the 2027 budget as issued, and the lines expected once its week numbers are moved "
               "onto 2027's dates and its overstatement taken out"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Brand", "Group", "ISO week 2027", "Budget as issued", "Expected lines"])
    _head(ws, 2)
    for (brand, grp), v in G["vol"].items():
        bud = A.budget_totals(f, brand, grp, 2027)
        for w in WEEKS:
            ws.append([brand, grp, w, int(bud[w]), r10(v[w])])
    ws.append([])
    ws.append(["Week 47 (Black Friday 26.11.2027) share of the peak's Kotikaari small-parts lines: expected %.1f %%, "
               "budget %.1f %%" % (figs["r6"], figs["r6_budget"])])
    _widths(ws, [14, 12, 13, 17, 15])
    for row in ws.iter_rows(min_row=3, min_col=4, max_col=5):
        for c in row:
            c.number_format = "#,##0"

    ws = wb.create_sheet("Forecast record")
    ws.append(["Kotikaari's year-ahead budgets against the order lines it placed (the WMS order import)"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Budget year", "Group", "Commercial plan growth %", "Budget lines (year)", "Order lines placed (year)",
               "Overstatement %"])
    _head(ws, 2)
    for r in G["cal"]["table"].itertuples(index=False):
        ws.append([int(r.year), r.group, pct(r.plan, 0), int(r.forecast), int(r.placed), pct(r.over)])
    ws.append([])
    ws.append(["Peak weeks 46 to 50 of 2022 to 2025, all lines: overstatement %.1f %%" % figs["r2"]])
    ws.append(["Expected overstatement of the 2027 budget: Kotikaari small parts %.1f %%, bulky %.1f %%; Huippu Sport "
               "small parts %.1f %%, bulky %.1f %%" % (figs["r5"]["K_sp"], figs["r5"]["K_bu"], figs["r5"]["H_sp"],
                                                        figs["r5"]["H_bu"])])
    _widths(ws, [12, 13, 22, 18, 18, 15])
    for row in ws.iter_rows(min_row=3, max_row=10):
        for c in row[3:5]:
            c.number_format = "#,##0"
        for c in (row[2], row[5]):
            c.number_format = "0.0"

    ws = wb.create_sheet("Time a line")
    ws.append(["Task minutes a line in the small-parts zones, fitted on the WMS zone hours 2022 to 2026"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Term", "Minutes"])
    _head(ws, 2)
    for k in ("A", "B", "C", "D", "F"):
        ws.append(["handling class %s, a line" % k, round(float(G["fit"]["coef"][k]), 3)])
    ws.append(["each unit after the first", round(float(G["fit"]["coef"]["unit"]), 3)])
    ws.append(["a line in P1", round(float(G["fit"]["coef"]["P1"]), 3)])
    ws.append(["a Huippu Sport line", round(float(G["fit"]["coef"]["HUI"]), 3)])
    ws.append([])
    ws.append(["Pickers logged in an aisle", "Congestion, minutes a line"])
    _head(ws, ws.max_row)
    for d in (0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0):
        ws.append([d, round(A.cong(G["fit"], d), 3)])
    ws.append([])
    ws.append(["A Huippu Sport line in the 2027 peak, small-parts zones", figs["t_hui"]])
    ws.append(["A Kotikaari line in the peak, small-parts zones", figs["t_kot"]])
    ws.append(["Difference", figs["r4"]])
    _widths(ws, [52, 24])

    ws = wb.create_sheet("Routes")
    ws.append(["What each shorter route gives"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Route", "Evening shift, P1", "Evening shift, P2", "Agency hours, peak"])
    _head(ws, 2)
    ws.append(["This plan", weeks_text(figs["evening"]["P1"]), weeks_text(figs["evening"]["P2"]), figs["agency_total"]])
    ws.append(["The draft's method: the budget as issued over the pooled overstatement, the 2025 rate, the pilot's "
               "time a line", weeks_text(figs["hurried"]["evening"]["P1"]), weeks_text(figs["hurried"]["evening"]["P2"]),
               figs["hurried"]["agency_total"]])
    for fx in FIXES:
        r = figs["routes"][fx]
        ws.append(["The draft's method with %s only" % FIX_NAME[fx], weeks_text(r["evening"]["P1"]),
                   weeks_text(r["evening"]["P2"]), r["agency_total"]])
    _widths(ws, [80, 18, 18, 18])
    for row in ws.iter_rows(min_row=3, min_col=4, max_col=4):
        for c in row:
            c.number_format = "#,##0"
    ws = wb.create_sheet("Notes")
    notes = [
        ("As of", "WMS, payroll and order extracts to 1 November 2026; Kotikaari Oy budget 2027 of 15 October 2026"),
        ("Picker hours", "paid hours worked in a pick zone as the payroll books them (planning standard 2.2); packing "
                         "and absence excluded; to the nearest 10"),
        ("Lines", "order lines picked, as the WMS counts them (2.3); 2027 lines are expected lines, to the nearest 10"),
        ("Evening shift", "opened for a small-parts zone in a peak week when the day shifts at the zone's limit (P1 24, "
                          "P2 22 pickers on the floor) cannot pick the week's lines (3.4)"),
        ("Range", "80 per cent: the budget's year-ahead error after its overstatement is taken out, the weekly profile's "
                  "error and the time model's error (3.5)"),
        ("Own pickers", "the roster's own pickers on the day shift of every working weekday less their zone's sickness "
                        "absence in weeks 46 to 50 of 2025 (4.1)"),
        ("Calendar", "week 49 of 2027 has five day shifts (Independence Day, Monday 6 December); Black Friday is "
                     "26 November 2027, in week 47"),
        ("Sources", "WMS zone hours 2022 to 2026, payroll exports 2022 to 2026, WMS order import, Kotikaari Oy forecast "
                    "archive and budget 2027, Huippu Sport order exports, WMS item master, slotting run of 30.10.2026, "
                    "HR roster 2027, pilot confirmations weeks 37 to 44 of 2026"),
    ]
    ws.append(["Notes"])
    ws["A1"].font = Font(bold=True)
    for k, v in notes:
        ws.append([k, v])
    _widths(ws, [16, 110])
    wb.save(path)


def chart(figs, G):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), sharey=True)
    for ax, zz in zip(axes, A.Z_SMALL):
        lines = [G["plan"][(zz, w)]["lines"] / 1000 for w in WEEKS]
        caps = [G["plan"][(zz, w)]["cap"] / 1000 for w in WEEKS]
        x = np.arange(len(WEEKS))
        ax.bar(x, lines, color=["#c0504d" if G["plan"][(zz, w)]["evening"] else "#7f9fbf" for w in WEEKS], width=0.6)
        ax.plot(x, caps, color="#333333", marker="_", markersize=18, linestyle="none")
        ax.set_xticks(x)
        ax.set_xticklabels(["wk %d" % w for w in WEEKS], fontsize=8)
        ax.set_title("%s (limit %d pickers)" % (zz, P.LIMIT[zz]), fontsize=8.5)
        ax.tick_params(axis="y", labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    axes[0].set_ylabel("thousand lines a week", fontsize=8)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    axes[0].legend(handles=[Patch(color="#c0504d", label="evening shift needed"), Patch(color="#7f9fbf", label="day shifts only"),
                            Line2D([0], [0], color="#333333", marker="_", markersize=12, linestyle="none",
                                   label="day shifts' capacity at the limit")], fontsize=6.5, frameon=False, loc="upper left")
    fig.suptitle("Weeks 47 to 50 carry more lines than the day shifts can pick at the zone limit", fontsize=9)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_docx(path, figs, G):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(18)
    sec.top_margin = sec.bottom_margin = Mm(15)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(9.5)
    doc.add_heading("Peak 2027: evening shifts in weeks %s, %s agency hours" % (
        weeks_text(figs["evening"]["P1"]) if figs["evening"]["P1"] == figs["evening"]["P2"] else "by zone",
        "{:,}".format(figs["agency_total"]).replace(",", " ")), level=1)
    blk = doc.add_paragraph()
    blk.add_run("To: ").bold = True
    blk.add_run("the management team, %s\n" % P.ORG)
    blk.add_run("From: ").bold = True
    blk.add_run("%s, operations director\n" % P.PEOPLE["director"])
    blk.add_run("Date: ").bold = True
    blk.add_run("10 November 2026\n")
    blk.add_run("Subject: ").bold = True
    blk.add_run("Saarnela peak plan 2027, evening-shift agreement and agency booking")
    p = doc.add_paragraph()
    p.add_run("Recommendation. ").bold = True
    same = figs["evening"]["P1"] == figs["evening"]["P2"]
    where = ("weeks %s in both small-parts zones, P1 and P2" % weeks_text(figs["evening"]["P1"])) if same else \
        ("weeks %s in P1 and weeks %s in P2" % (weeks_text(figs["evening"]["P1"]), weeks_text(figs["evening"]["P2"])))
    p.add_run("Agree the evening shift in %s, and book %s agency picker hours over the "
              "peak (%s). Week 46 runs on day shifts only." % (
                  where,
                  "{:,}".format(figs["agency_total"]).replace(",", " "),
                  "; ".join("week %d %s" % (w, "{:,}".format(figs["agency"][w]).replace(",", " ")) for w in WEEKS)))
    t = doc.add_table(rows=1, cols=7)
    t.style = "Table Grid"
    for i, h in enumerate(["Week", "P1 hours (80% range)", "P2 hours (80% range)", "B1 hours (80% range)",
                           "Evening P1", "Evening P2", "Agency hours"]):
        t.rows[0].cells[i].text = h
    for w in WEEKS:
        c = t.add_row().cells
        c[0].text = str(w)
        for j, zz in enumerate(P.ZONES):
            c[1 + j].text = "%s (%s to %s)" % tuple("{:,}".format(v).replace(",", " ") for v in
                                                   (figs["hours"][zz][w], figs["range"][zz][w][0], figs["range"][zz][w][1]))
        c[4].text = "yes" if w in figs["evening"]["P1"] else "no"
        c[5].text = "yes" if w in figs["evening"]["P2"] else "no"
        c[6].text = "{:,}".format(figs["agency"][w]).replace(",", " ")
    for row in t.rows:
        for c in row.cells:
            for par in c.paragraphs:
                for r in par.runs:
                    r.font.size = Pt(8.5)
    src = doc.add_paragraph("Picker hours are paid hours to the nearest 10 (planning standard 2.2); ranges at 80 per cent "
                            "(3.5). Week 49 has five day shifts (Independence Day, Monday 6 December).")
    for r in src.runs:
        r.font.size = Pt(8)
        r.italic = True
    doc.add_picture(io.BytesIO(chart(figs, G)), width=Mm(172))
    pts = [
        ("The zones slow as they fill.",
         "With the mix of lines held fixed, a line takes %s minutes longer at 1.8 pickers logged in an aisle than on "
         "an empty floor; the 2025 peak ran its day shifts well below the limit, so its hours a line do not carry to "
         "2027's day shifts at 24 and 22 pickers." % ("%.2f" % figs["r3"])),
        ("Huippu Sport's lines are heavier than the pilot's.",
         "The pilot carried polybag apparel only; at the full assortment's peak mix (footwear boxes, boots, multi-unit "
         "lines) a Huippu Sport line takes %.2f minutes longer than a Kotikaari line." % figs["r4"]),
        ("The budgets overstate by more when they plan more.",
         "Kotikaari's budgets have overstated the peak's lines by %.1f per cent on average (2022 to 2025); the 2027 "
         "budget's %d per cent plan for Kotikaari small parts points to %.1f per cent, its %d per cent plan for Huippu "
         "Sport to %.1f." % (figs["r2"], figs["plan_growth"]["K"][0], figs["r5"]["K_sp"], figs["plan_growth"]["H"][0],
                             figs["r5"]["H_sp"])),
        ("Black Friday is in week 47.",
         "The budget phases 2027 by 2025's week numbers and 2026 has 53 ISO weeks; week 47 of 2027 carries %.1f per "
         "cent of the peak's Kotikaari small-parts lines, not the budget's %.1f." % (figs["r6"], figs["r6_budget"])),
        ("The draft's route.",
         "The budget as issued, the 2025 hours a line and the pilot's time a line open the evening shift in P1 %s "
         "and P2 %s and book %s agency hours." % (
             wk_phrase(figs["hurried"]["evening"]["P1"]), wk_phrase(figs["hurried"]["evening"]["P2"]),
             "{:,}".format(figs["hurried"]["agency_total"]).replace(",", " "))),
    ]
    for lead, rest in pts:
        par = doc.add_paragraph()
        par.add_run(lead + " ").bold = True
        par.add_run(rest)
        par.paragraph_format.space_after = Pt(3)
    doc.save(path)


def write(target, gold):
    os.makedirs(gold, exist_ok=True)
    f, G, figs, rg = compute(target)
    write_xlsx(os.path.join(gold, XLSX), f, G, figs)
    write_docx(os.path.join(gold, DOCX), figs, G)
    return f, G, figs
