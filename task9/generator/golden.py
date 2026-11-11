"""task9: the golden deliverables the prompt asks for, a spreadsheet and a chart, written from the figures as computed
(F) and as stated (F["stated"]). Nothing is typed: every number below is read from F.

    write_all(F, golden_dir)
"""
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import params as P
import postprocess as PP

BOOK = "halden_replacement_forecast_2026Q4_2027Q3.xlsx"
CHART = "halden_replacement_path_2026Q4_2027Q3.png"
FILES = (BOOK, CHART)
STAMPS = {BOOK: ("2026-10-13T14:02:11Z", "2026-10-15T21:37:48Z")}
HEAD = PatternFill("solid", fgColor="E8EDF3")
THIN = Side(style="thin", color="B9C0C8")
FAM_ORDER = ["OM-6", "M-14", "M-16", "T-20", "W-22", "HX-8", "KS-10", "VB-12", "X-24"]
FAM_NAME = {f: "%s (%s)" % (f, P.FAMILY[f]["model"].split(" ", 1)[1]) for f in FAM_ORDER}
QLAB = {q: q.replace("Q", "-Q") for q in P.FORECAST_Q + P.BACKTEST_Q + ["2024Q4", "2025Q1", "2025Q2", "2025Q3"]}


def r0(v):
    return int(round(v))


def week_label(w):
    y, k = w.split("-W")
    return "%s week %d" % (y, int(k))


def _head(ws, row, labels, widths=None):
    for j, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=t)
        c.font = Font(bold=True, size=10)
        c.fill = HEAD
        c.border = Border(bottom=THIN)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w


def _title(ws, text, note=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12)
    if note:
        ws["A2"] = note
        ws["A2"].font = Font(italic=True, size=9, color="52514E")


def book(F, path):
    g, S = F["gold"], F["stated"]
    wb = openpyxl.Workbook()
    # ---- the path
    ws = wb.active
    ws.title = "Quarterly path"
    _title(ws, "Drive replacements (failures plus health pulls), October 2026 to September 2027",
           "Mean of 3,000 posterior predictive draws; P10 and P90 bound the 80% interval. Drives in service on 30 Sep 2026 "
           "plus the X-24 installs in the capacity plan.")
    _head(ws, 4, ["Quarter", "Mean", "P10", "P90"] + ["%s mean" % dc for dc in ("DC-1", "DC-2", "DC-3")],
          [12, 10, 10, 10, 11, 11, 11])
    r = 5
    for q in P.FORECAST_Q:
        ws.append([QLAB[q], S["path"][q], S["path_band"][q][0], S["path_band"][q][1]] +
                  [r0(g["by_dc_q"][dc][q]) for dc in ("DC-1", "DC-2", "DC-3")])
        r += 1
    ws.append(["Four quarters", S["total"], S["total_band"][0], S["total_band"][1]] +
              [S["by_dc"][dc] for dc in ("DC-1", "DC-2", "DC-3")])
    for c in ws[r]:
        c.font = Font(bold=True)
    ws.append([])
    ws.append(["80% interval width, four quarters", S["total_width"]])
    ws.append([])
    _head(ws, r + 4, ["Data centre", "Four-quarter mean", "P10", "P90"])
    for dc in ("DC-1", "DC-2", "DC-3"):
        b = g["by_dc_band"][dc]
        ws.append([dc, S["by_dc"][dc], r0(b[0]), r0(b[1])])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for c in row[1:]:
            c.number_format = "#,##0"
    # ---- by family
    ws = wb.create_sheet("By family")
    _title(ws, "Replacements by drive family, mean per quarter", "Bands are the 80% interval of the four-quarter total.")
    _head(ws, 4, ["Family"] + [QLAB[q] for q in P.FORECAST_Q] + ["Four quarters", "P10", "P90"], [24, 10, 10, 10, 10, 13, 9, 9])
    for f in FAM_ORDER:
        b = g["by_family_band"][f]
        ws.append([FAM_NAME[f]] + [round(g["by_family_q"][f][q], 1) for q in P.FORECAST_Q] + [S["by_family"][f], r0(b[0]), r0(b[1])])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for c in row[1:5]:
            c.number_format = "0.0"
        for c in row[5:]:
            c.number_format = "#,##0"
    # ---- the batch
    ws = wb.create_sheet("HX-8 bad builds")
    w0, w1 = g["hot_window"]
    _title(ws, "HX-8 drives built %s to %s: the batch with the rising hazard" % (week_label(w0), week_label(w1)),
           "Build week read from the serial (KS + plant + YYWW). Rate = replacements in Jul-Sep 2026 per drive-year in service.")
    _head(ws, 4, ["Item", "Value"], [58, 14])
    rows = [
        ("Drives of the batch in service, 30 Sep 2026", S["hot_batch"]["drives"], "#,##0"),
        ("Current annualized replacement rate", S["hot_batch"]["rate"], "0.0%"),
        ("Replacements, Oct 2026 to Sep 2027 (mean)", S["hot_count"], "#,##0"),
        ("  P10", r0(g["hot_band"][0]), "#,##0"),
        ("  P90", r0(g["hot_band"][1]), "#,##0"),
        ("Expected share of the batch replaced within 24 months", S["frac24"], "0.0%"),
        ("Break-even share (migration USD %s / (1,200 drives x USD %s))" % ("{:,}".format(P.COSTS["migrate_vault"]),
                                                                            P.COSTS["failure_handling"]),
         P.COSTS["migrate_vault"] / (P.VAULT_DRIVES * P.COSTS["failure_handling"]), "0.0%"),
        ("Doubling time (months) above which a vault made wholly of the batch stops paying for its migration",
         S["rec"]["flip"], "0.0"),
    ]
    for label, v, fmt in rows:
        ws.append([label, v])
        if fmt:
            ws.cell(row=ws.max_row, column=2).number_format = fmt
    ws.append([])
    line = P.COSTS["migrate_vault"] / P.COSTS["failure_handling"]
    r = ws.max_row + 1
    _head(ws, r, ["Vault (24 months from 1 Oct 2026)", "Drives in service", "Of the batch", "Expected replacements",
                  "Break-even", "Chance it pays", "Call"])
    for v, s in sorted(S["vaults"].items()):
        ws.append([v, s["drives"], s["batch"], s["mean"], int(line), s["p_pays"],
                   "migrate in Q4 2026" if v in S["rec"]["migrate"] else "run to failure"])
        ws.cell(row=ws.max_row, column=6).number_format = "0%"
    for col, wdt in zip("CDEFG", (12, 14, 11, 13, 18)):
        ws.column_dimensions[col].width = max(ws.column_dimensions[col].width or 0, wdt)
    ws.append([])
    ws.append(["Ramp shapes weighted by likelihood"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    for k, lab in (("exp", "exponential in months since build"), ("lin", "linear in months since build"), ("pow", "power of age")):
        ws.append([lab, round(g["hot_weights"].get(k, 0.0), 3)])
        ws.cell(row=ws.max_row, column=2).number_format = "0.00"
    # ---- spares
    ws = wb.create_sheet("Q4 spares")
    _title(ws, "Spare drives to order for Oct-Dec 2026 (chance of running short at most 10%)",
           "Order = 90th percentile of the quarter's replacements minus stock on hand on 30 Sep 2026, never below zero.")
    _head(ws, 4, ["Family", "Q4 mean", "Q4 P90", "On hand", "Order"], [24, 10, 10, 10, 10])
    for f in FAM_ORDER:
        if f not in g["spares"]:
            continue
        ws.append([FAM_NAME[f], round(g["by_family_q"][f][P.FORECAST_Q[0]], 1), r0(g["spares_p90"][f]), P.SPARES_ON_HAND.get(f, 0),
                   S["spares"][f]])
    ws.append(["Total", None, None, sum(P.SPARES_ON_HAND.get(f, 0) for f in g["spares"]), sum(S["spares"].values())])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    # ---- the back-test
    ws = wb.create_sheet("Back-test")
    _title(ws, "Intervals built the same way from the record to 30 Sep 2025, against Oct 2025 to Sep 2026",
           "Vaults in service on 30 Sep 2025 that were not retired; one cell per drive family and quarter.")
    _head(ws, 4, ["Quarter", "Family", "P10", "P90", "Mean", "Actual", "Inside"], [11, 12, 9, 9, 9, 9, 9])
    for c in F["gold"]["backtest_detail"]:
        ws.append([QLAB[c["q"]], c["family"], r0(c["lo"]), r0(c["hi"]), round(c["mean"], 1), c["actual"], "yes" if c["inside"] else "no"])
    n = len(F["gold"]["backtest_detail"])
    ws.append([])
    ws.append(["Coverage", None, None, None, None, None, S["coverage"]])
    ws.cell(row=ws.max_row, column=7).number_format = "0.0%"
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    ws.append(["Cells", None, None, None, None, None, n])
    # ---- drivers
    ws = wb.create_sheet("Drivers")
    _title(ws, "What moves the forecast")
    _head(ws, 3, ["Driver", "Figure"], [70, 14])
    lag = F["record"]["deploy_lag"]
    src = F["record"]["age_sources"]
    drv = [
        ("DC-3 replacements, four quarters (ages rebuilt: %s drives from the Brightstore manifest, %s from power-on hours, "
         "%s from the serial's build week plus a %d-day deploy lag)" % ("{:,}".format(src.get("manifest", 0)),
                                                                       "{:,}".format(src.get("power-on hours", 0)),
                                                                       "{:,}".format(src.get("build week", 0)), round(lag)),
         S["dc3"]),
        ("OM-6 vaults still in service, four quarters", S["om6"]),
        ("HX-8 bad builds, four quarters", S["hot_count"]),
        ("Infant term decay, months (chosen by likelihood)", g["infant_months"]),
        ("Health pulls of healthy drives under P2 (SMART 187 > 0), per drive-year since Sep 2025", round(g["spur_rate"], 4)),
        ("Extra-Poisson dispersion of vault-quarter counts (gamma shape)",
         round(g["dispersion_k"], 1) if g["dispersion_k"] < 1e6 else "none beyond each vault's own level"),
    ]
    for label, v in drv:
        ws.append([label, v])
    for wsx in wb.worksheets:
        wsx.sheet_view.showGridLines = False
        wsx.freeze_panes = None
    wb.save(path)
    PP.normalize_ooxml(path, P.PEOPLE["capacity"], P.PEOPLE["capacity"], STAMPS[BOOK][0], STAMPS[BOOK][1], excel=True,
                       company=P.FIRM)


def chart(F, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pack as PK
    g, S = F["gold"], F["stated"]
    hist = F["history"]
    hq = list(hist)
    fq = P.FORECAST_Q
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    xs_h = list(range(len(hq)))
    xs_f = list(range(len(hq), len(hq) + len(fq)))
    ax.plot(xs_h, [hist[q] for q in hq], color="#52514e", lw=2, marker="o", ms=4, label="Actual")
    lo = [S["path_band"][q][0] for q in fq]
    hi = [S["path_band"][q][1] for q in fq]
    ax.fill_between(xs_f, lo, hi, color="#86b6ef", alpha=0.45, lw=0, label="80% interval")
    ax.plot([xs_h[-1]] + xs_f, [hist[hq[-1]]] + [S["path"][q] for q in fq], color="#2a78d6", lw=2, marker="o", ms=4,
            label="Forecast (mean)")
    for x, q in zip(xs_f, fq):
        ax.annotate("{:,}".format(S["path"][q]), (x, S["path"][q]), textcoords="offset points", xytext=(0, 8), ha="center",
                    fontsize=8, color="#0b0b0b")
    ax.set_xticks(xs_h + xs_f)
    ax.set_xticklabels([q.replace("Q", "\nQ") for q in hq + fq], fontsize=8)
    ax.set_ylabel("Replacements per quarter")
    top = max(max(hi), max(hist.values()))
    ax.set_ylim(0, top * 1.12)
    qh = max(hq, key=lambda q: hist[q])
    xh = hq.index(qh)
    ax.annotate("health-pull policy P2:\nhealthy drives with SMART 187 pulled", (xh, hist[qh]), textcoords="offset points",
                xytext=(14, -6), ha="left", va="top", fontsize=7.5, color="#52514e")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e4e3df", lw=0.6)
    ax.axvline(xs_h[-1] + 0.5, color="#b9c0c8", lw=0.8, ls=":")
    ax.set_title("Halden Vault drive replacements: actuals to Q3 2026, forecast to Q3 2027", loc="left", fontsize=10)
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)
    PK.strip_png(path)


def write_all(F, out):
    os.makedirs(out, exist_ok=True)
    book(F, os.path.join(out, BOOK))
    chart(F, os.path.join(out, CHART))
    return [os.path.join(out, f) for f in FILES]
