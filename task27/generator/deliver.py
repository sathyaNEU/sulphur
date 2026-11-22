"""Build the three golden deliverables strictly from figures.json and cut target.zip and golden.zip:
  1. weserfrucht_delay_attribution_2027.csv
  2. weserfrucht_coldchain_remediation_2027.xlsx (100% live Excel formulas + charts, normalized OOXML)
  3. weserfrucht_remediation_review_2027.pptx (7-slide executive close-out deck + clean PNG charts, normalized OOXML)

Every container passes through house postprocess.py with distinct realistic timestamps after as_of
(2027-01-19), and both ZIPs are cut via postprocess.zip_folder(..., zone="Europe/Berlin").
"""
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import sys
import zipfile
from xml.sax.saxutils import escape as xml_escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
REPO = os.path.dirname(TASK_DIR)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".agents", "skills", "reduce-house-fixes", "scripts", "writers"))

import postprocess  # noqa: E402
import core  # noqa: E402
import pack as PK  # noqa: E402

UTC = dt.timezone.utc

GOLDEN_FILES = {
    "csv": "weserfrucht_delay_attribution_2027.csv",
    "xlsx": "weserfrucht_coldchain_remediation_2027.xlsx",
    "pptx": "weserfrucht_remediation_review_2027.pptx",
}

# Palette (deliberate Weserfrucht maritime-navy / terracotta-alert / sage-monitor)
NAVY_HEX = "1B365D"
SLATE_HEX = "3B5373"
REM_FILL_HEX = "F8DDD9"
MON_FILL_HEX = "DCECE2"
TOT_FILL_HEX = "EAF0F7"
ZEBRA_HEX = "F6F8FB"
PARAM_HEX = "EEF3F9"

HEAD_FILL = PatternFill("solid", fgColor=NAVY_HEX)
REM_FILL = PatternFill("solid", fgColor=REM_FILL_HEX)
MON_FILL = PatternFill("solid", fgColor=MON_FILL_HEX)
TOT_FILL = PatternFill("solid", fgColor=TOT_FILL_HEX)
ZEBRA_FILL = PatternFill("solid", fgColor=ZEBRA_HEX)
PARAM_FILL = PatternFill("solid", fgColor=PARAM_HEX)
THIN = Side(style="thin", color="C4CDD8")
MED = Side(style="medium", color=NAVY_HEX)
B_CELL = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
B_HDR = Border(bottom=MED)
B_TOT = Border(top=MED, bottom=MED, left=THIN, right=THIN)


def _set_formula(ws, cache_sheet, ref, formula, cached_val, num_fmt=None, bold=False, fill=None, align="right"):
    c = ws[ref]
    c.value = formula
    c.font = Font(name="Calibri", size=10, bold=bold, color="111111")
    if num_fmt:
        c.number_format = num_fmt
    if fill:
        c.fill = fill
    c.alignment = Alignment(horizontal=align, vertical="center")
    c.border = B_TOT if bold else B_CELL
    cache_sheet[ref] = cached_val


def _style_hdr(ws, row, ncols, height=30):
    for col_i in range(1, ncols + 1):
        c = ws.cell(row=row, column=col_i)
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = HEAD_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = B_HDR
    ws.row_dimensions[row].height = height


def _set_widths(ws, widths, freeze="A6"):
    for i, w in enumerate(widths):
        col = chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)
        ws.column_dimensions[col].width = w
    ws.freeze_panes = freeze
    ws.views.sheetView[0].showGridLines = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = 9
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0


def _inject_formula_cache(xlsx_path, cache):
    """Inject exact evaluated formula cached values (<v>...) into openpyxl-saved XML before postprocess."""
    with zipfile.ZipFile(xlsx_path, "r") as zin:
        items = [(i.filename, zin.read(i.filename)) for i in zin.infolist()]
    out_items = []
    for name, data in items:
        if name in cache and cache[name]:
            txt = data.decode("utf-8")
            for ref, val in cache[name].items():
                if isinstance(val, str):
                    pat = re.compile(rf'(<c r="{ref}"[^>]*?)(><f[^>]*>.*?</f>)(?:<v>.*?</v>)?(</c>)', re.S)
                    def _rep_s(m, v=val):
                        head = m.group(1)
                        if ' t="' in head:
                            head = re.sub(r' t="[^"]*"', ' t="str"', head)
                        else:
                            head = head + ' t="str"'
                        return f'{head}{m.group(2)}<v>{xml_escape(v)}</v>{m.group(3)}'
                    txt = pat.sub(_rep_s, txt, count=1)
                else:
                    pat = re.compile(rf'(<c r="{ref}"[^>]*?><f[^>]*>.*?</f>)(?:<v>.*?</v>)?(</c>)', re.S)
                    txt = pat.sub(rf'\g<1><v>{val}</v>\g<2>', txt, count=1)
            data = txt.encode("utf-8")
        out_items.append((name, data))
    with zipfile.ZipFile(xlsx_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in out_items:
            zout.writestr(name, data)


# ------------------------------------------------------------------
# 1. Golden CSV
# ------------------------------------------------------------------
def write_csv(out_dir, fig):
    path = os.path.join(out_dir, GOLDEN_FILES["csv"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["cause_id", "cdays_2026", "cdays_2027", "share_2027_pct", "eur_2027", "designation"])
        for row in fig["causes"]:
            wr.writerow([
                row["cause_id"],
                f"{row['cdays_2026']:.2f}",
                f"{row['cdays_2027']:.2f}",
                f"{row['share_2027_pct']:.2f}",
                f"{row['eur_2027']:.2f}",
                row["designation"],
            ])
    return path


# ------------------------------------------------------------------
# 2. Golden Workbook (100% live Excel formulas + embedded charts)
# ------------------------------------------------------------------
def write_xlsx(out_dir, fig):
    path = os.path.join(out_dir, GOLDEN_FILES["xlsx"])
    wb = Workbook()
    cache = {}

    # Sheet 1: Remediation_Summary
    ws1 = wb.active
    ws1.title = "Remediation_Summary"
    c1 = cache.setdefault("xl/worksheets/sheet1.xml", {})

    remed_names = ", ".join(r["cause_id"] for r in fig["causes"] if r["designation"] == "REMEDIATE")
    mon_names = ", ".join(r["cause_id"] for r in fig["causes"] if r["designation"] == "MONITOR")
    ws1["A1"] = (
        f"2027 Mandatory Remediation Slate: Fund {remed_names} "
        f"({fig['A_remed_days']:,} c-days, EUR {fig['A_avoidable_eur_m']:.3f}M); "
        f"Monitor {mon_names} (rejects TMS/rigorous slate naming rail_handoff while omitting coldstore_dock and empty_depot)"
    )
    ws1["A1"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEX)
    ws1["A2"] = (
        f"{PK.ORG} | Charter RC-2027 Annual Carrier Close-Out Review (>= 2,500 c-day threshold) | "
        f"Prepared by {PK.PEOPLE['analyst']}, 21 January 2027"
    )
    ws1["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    ws1["A4"] = "Ranked Operational Causes (2026 Conserved Attribution and 2027 Projected Schedule under Charter RC-2027)"
    ws1["A4"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)

    hdrs1 = [
        "Rank", "Cause ID", "Operational Bottleneck", "2026 Excess C-Days",
        "2027 Projected C-Days", "2027 Share (%)", "Daily Tariff (EUR)",
        "2027 Exposure (EUR)", "Charter RC-2027 Designation",
        "22-Variant 2027 Band", "Direct TMS 2027", "Rigorous Std 2027",
    ]
    for ci, h in enumerate(hdrs1, start=1):
        ws1.cell(row=5, column=ci, value=h)
    _style_hdr(ws1, 5, len(hdrs1), height=32)

    tot26 = sum(r["cdays_2026"] for r in fig["causes"])
    tot27 = sum(r["cdays_2027"] for r in fig["causes"])
    tot_eur = sum(r["eur_2027"] for r in fig["causes"])
    rem_days = sum(r["cdays_2027"] for r in fig["causes"] if r["designation"] == "REMEDIATE")
    rem_eur = sum(r["eur_2027"] for r in fig["causes"] if r["designation"] == "REMEDIATE")

    for idx, row in enumerate(fig["causes"], start=1):
        r = 5 + idx
        is_rem = row["designation"] == "REMEDIATE"
        row_fill = REM_FILL if is_rem else MON_FILL
        ws1.cell(row=r, column=1, value=idx).alignment = Alignment(horizontal="center", vertical="center")
        ws1.cell(row=r, column=2, value=row["cause_id"]).alignment = Alignment(horizontal="left", vertical="center")
        ws1.cell(row=r, column=3, value=row["cause_name"]).alignment = Alignment(horizontal="left", vertical="center")
        ws1.cell(row=r, column=4, value=row["cdays_2026"]).number_format = "#,##0.00"
        ws1.cell(row=r, column=5, value=row["cdays_2027"]).number_format = "#,##0.00"
        for col_i in (1, 2, 3, 4, 5):
            cc = ws1.cell(row=r, column=col_i)
            cc.font = Font(name="Calibri", size=10, bold=(col_i == 2), color="111111")
            cc.border = B_CELL
            if col_i in (4, 5):
                cc.alignment = Alignment(horizontal="right", vertical="center")

        _set_formula(
            ws1, c1, f"F{r}", f"=E{r}/$E$14", row["cdays_2027"] / tot27, num_fmt="0.00%",
        )
        _set_formula(
            ws1, c1, f"G{r}", f"=INDEX(Inputs_Plan_2027!$B$6:$B$13,MATCH(B{r},Inputs_Plan_2027!$A$6:$A$13,0))",
            row["tariff_eur"], num_fmt="#,##0",
        )
        _set_formula(
            ws1, c1, f"H{r}", f"=E{r}*G{r}", row["cdays_2027"] * row["tariff_eur"], num_fmt="#,##0.00",
        )
        _set_formula(
            ws1, c1, f"I{r}", f'=IF(E{r}>=Inputs_Plan_2027!$B$4,"REMEDIATE","MONITOR")',
            row["designation"], bold=True, fill=row_fill, align="center",
        )
        band_txt = f"{row['band_2027'][0]:,} to {row['band_2027'][1]:,}"
        for ci, val, fmt, al in (
            (10, band_txt, None, "center"),
            (11, row["direct_2027_int"], "#,##0", "right"),
            (12, row["rigorous_2027_int"], "#,##0", "right"),
        ):
            cc = ws1.cell(row=r, column=ci, value=val)
            cc.font = Font(name="Calibri", size=10, color="333333")
            cc.alignment = Alignment(horizontal=al, vertical="center")
            cc.border = B_CELL
            if fmt:
                cc.number_format = fmt
        ws1.row_dimensions[r].height = 20

    # Row 14: Network Total (live SUM formulas)
    ws1.cell(row=14, column=1, value="")
    ws1.cell(row=14, column=2, value="TOTAL_NETWORK")
    ws1.cell(row=14, column=3, value="All 8 Operational Causes Combined")
    for ci in (1, 2, 3, 7, 9, 10):
        cc = ws1.cell(row=14, column=ci)
        cc.font = Font(name="Calibri", size=10, bold=True, color="111111")
        cc.fill = TOT_FILL
        cc.border = B_TOT
    _set_formula(ws1, c1, "D14", "=SUM(D6:D13)", tot26, num_fmt="#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "E14", "=SUM(E6:E13)", tot27, num_fmt="#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "F14", "=SUM(F6:F13)", 1.0, num_fmt="0.00%", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "H14", "=SUM(H6:H13)", tot_eur, num_fmt="#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "K14", "=SUM(K6:K13)", sum(r["direct_2027_int"] for r in fig["causes"]), num_fmt="#,##0", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "L14", "=SUM(L6:L13)", sum(r["rigorous_2027_int"] for r in fig["causes"]), num_fmt="#,##0", bold=True, fill=TOT_FILL)
    ws1.row_dimensions[14].height = 22

    # Row 15: Mandatory Remediation Subtotal (live SUMIF / COUNTIF)
    ws1.cell(row=15, column=1, value="")
    ws1.cell(row=15, column=2, value="REMEDIATE_SLATE")
    ws1.cell(row=15, column=3, value="Designated Mandatory Remediation (5 Causes)")
    for ci in (1, 2, 3, 7, 10, 11, 12):
        cc = ws1.cell(row=15, column=ci)
        cc.font = Font(name="Calibri", size=10, bold=True, color="111111")
        cc.fill = REM_FILL
        cc.border = B_TOT
    _set_formula(ws1, c1, "D15", '=SUMIF(I6:I13,"REMEDIATE",D6:D13)', sum(r["cdays_2026"] for r in fig["causes"] if r["designation"] == "REMEDIATE"), num_fmt="#,##0.00", bold=True, fill=REM_FILL)
    _set_formula(ws1, c1, "E15", '=SUMIF(I6:I13,"REMEDIATE",E6:E13)', rem_days, num_fmt="#,##0.00", bold=True, fill=REM_FILL)
    _set_formula(ws1, c1, "F15", "=E15/E14", rem_days / tot27, num_fmt="0.00%", bold=True, fill=REM_FILL)
    _set_formula(ws1, c1, "H15", '=SUMIF(I6:I13,"REMEDIATE",H6:H13)', rem_eur, num_fmt="#,##0.00", bold=True, fill=REM_FILL)
    _set_formula(ws1, c1, "I15", '=COUNTIF(I6:I13,"REMEDIATE")&" of 8 causes"', "5 of 8 causes", bold=True, fill=REM_FILL, align="center")
    ws1.row_dimensions[15].height = 22

    # KPI Summary Block (Rows 17-22) linked live to Table & Corridor_Q3_Breakdown
    ws1["A17"] = "Headline 2027 Financial and Network Exposure Summary"
    ws1["A17"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    kpis = [
        ("Total 2027 Network Excess Container-Days", "=E14", tot27, "#,##0.00", f"{fig['agg_bands']['total_2027'][0]:,} to {fig['agg_bands']['total_2027'][1]:,}"),
        ("Total 2027 Designated Remediation Container-Days", "=E15", rem_days, "#,##0.00", f"{fig['agg_bands']['remed_days'][0]:,} to {fig['agg_bands']['remed_days'][1]:,}"),
        ("Total 2027 Detention & Demurrage Exposure (EUR Millions)", "=H14/1000000", tot_eur / 1e6, "0.000", f"{fig['agg_bands']['cost_eur_m'][0]:.3f} to {fig['agg_bands']['cost_eur_m'][1]:.3f}"),
        ("Avoidable 2027 Exposure on Designated Causes (EUR Millions)", "=H15/1000000", rem_eur / 1e6, "0.000", f"{fig['agg_bands']['avoidable_eur_m'][0]:.3f} to {fig['agg_bands']['avoidable_eur_m'][1]:.3f}"),
        ("Bremerhaven (BHV) 2027 Total Excess Container-Days", "=Corridor_Q3_Breakdown!B6", fig["by_port_2027"]["BHV"], "#,##0.00", f"{fig['agg_bands']['bhv_2027'][0]:,} to {fig['agg_bands']['bhv_2027'][1]:,}"),
        ("Hamburg (HAM) 2027 Total Excess Container-Days", "=Corridor_Q3_Breakdown!B7", fig["by_port_2027"]["HAM"], "#,##0.00", f"{fig['agg_bands']['ham_2027'][0]:,} to {fig['agg_bands']['ham_2027'][1]:,}"),
        ("Q3 2027 (Jul-Sep) Total Excess Container-Days", "=Corridor_Q3_Breakdown!E8", fig["by_quarter_2027"]["Q3"], "#,##0.00", f"{fig['agg_bands']['q3_2027'][0]:,} to {fig['agg_bands']['q3_2027'][1]:,}"),
    ]
    ws1["A18"], ws1["C18"], ws1["D18"] = "Metric", "2027 Value", "22-Variant Band"
    ws1.merge_cells("A18:B18")
    _style_hdr(ws1, 18, 4, height=24)
    for k_i, (lbl, fml, val, nf, bnd) in enumerate(kpis, start=19):
        ws1.merge_cells(f"A{k_i}:B{k_i}")
        ws1.cell(row=k_i, column=1, value=lbl).font = Font(name="Calibri", size=9.5, color="111111")
        ws1.cell(row=k_i, column=1).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws1.cell(row=k_i, column=1).border = B_CELL
        ws1.cell(row=k_i, column=2).border = B_CELL
        _set_formula(ws1, c1, f"C{k_i}", fml, val, num_fmt=nf, bold=True, fill=PARAM_FILL)
        cc = ws1.cell(row=k_i, column=4, value=bnd)
        cc.font = Font(name="Calibri", size=9.5, color="444444")
        cc.alignment = Alignment(horizontal="center", vertical="center")
        cc.border = B_CELL
        ws1.row_dimensions[k_i].height = 22

    # Embedded horizontal BarChart on Sheet 1 (F17:L31) - note in openpyxl bar charts x_axis=category, y_axis=value!
    ch1 = BarChart()
    ch1.type = "bar"
    ch1.style = 10
    ch1.title = "Projected 2027 Excess Container-Days by Cause (Threshold = 2,500)"
    ch1.x_axis.title = "Operational Cause"
    ch1.y_axis.title = "2027 Excess Container-Days"
    ch1.legend.position = "b"
    data_ref = Reference(ws1, min_col=5, min_row=5, max_row=13)
    cats_ref = Reference(ws1, min_col=2, min_row=6, max_row=13)
    ch1.add_data(data_ref, titles_from_data=True)
    ch1.set_categories(cats_ref)
    ch1.series[0].graphicalProperties.solidFill = NAVY_HEX
    ch1.width = 18.5
    ch1.height = 9.5
    ws1.add_chart(ch1, "F17")

    _set_widths(ws1, [7, 22, 40, 18, 20, 14, 16, 20, 24, 20, 16, 17], freeze="A6")

    # Sheet 2: Critical_Components
    ws2 = wb.create_sheet("Critical_Components")
    c2 = cache.setdefault("xl/worksheets/sheet2.xml", {})
    ws2["A1"] = "Three Independent Decisive Operational Judgments (Critical Components C1-C3)"
    ws2["A1"].font = Font(name="Calibri", size=12, bold=True, color=NAVY_HEX)
    ws2["A2"] = "Each component owns one open remediation call and is linked live to Remediation_Summary"
    ws2["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    hdrs2 = [
        "Component", "Cause ID", "2027 Golden C-Days", "22-Variant Band",
        "Charter Designation", "Rigorous Std 2027", "Direct TMS 2027",
        "Native Physical Conservation Check",
    ]
    for ci, h in enumerate(hdrs2, start=1):
        ws2.cell(row=4, column=ci, value=h)
    _style_hdr(ws2, 4, len(hdrs2))

    # Map cause_id -> row number on Remediation_Summary
    cause_row = {row["cause_id"]: 5 + idx for idx, row in enumerate(fig["causes"], start=1)}
    diag = fig["R5_diagnostics"]
    cc_specs = [
        ("C1", "coldstore_dock", f"F1 same-vessel unsaturated twin dwell gap = +{diag['F1_twin_gap_h']:.2f} h (vs +{diag['F1_rigorous_h']:.2f} h rigorous); 0-pallet DC stock-flow error"),
        ("C2", "rail_handoff", f"F2 shared-train weighbridge mass deficit = {diag['F2_tonnes_per_slot']:.2f} t/slot (vs {diag['F2_rigorous_t']:.2f} t rigorous) on 24h CHED-locked wagons"),
        ("C3", "empty_depot", f"F3 same-DC same-day closed-vs-open ocean-line return gap = +{diag['F3_line_gap_h']:.2f} h (vs {diag['F3_rigorous_h']:.2f} h rigorous); {diag['F3_retry_mult']:.2f}x portal retry ratio"),
    ]
    by_id = {r["cause_id"]: r for r in fig["causes"]}
    for idx, (cid, cause, chk) in enumerate(cc_specs, start=5):
        sr = cause_row[cause]
        rec = by_id[cause]
        ws2.cell(row=idx, column=1, value=cid).alignment = Alignment(horizontal="center", vertical="center")
        ws2.cell(row=idx, column=2, value=cause).alignment = Alignment(horizontal="left", vertical="center")
        ws2.cell(row=idx, column=1).font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
        ws2.cell(row=idx, column=2).font = Font(name="Calibri", size=10, bold=True)
        ws2.cell(row=idx, column=1).border = B_CELL
        ws2.cell(row=idx, column=2).border = B_CELL
        _set_formula(ws2, c2, f"C{idx}", f"=Remediation_Summary!E{sr}", rec["cdays_2027"], num_fmt="#,##0.00", bold=True)
        ws2.cell(row=idx, column=4, value=f"{rec['band_2027'][0]:,} to {rec['band_2027'][1]:,}").alignment = Alignment(horizontal="center", vertical="center")
        ws2.cell(row=idx, column=4).border = B_CELL
        _set_formula(ws2, c2, f"E{idx}", f"=Remediation_Summary!I{sr}", rec["designation"], bold=True,
                     fill=(REM_FILL if rec["designation"] == "REMEDIATE" else MON_FILL), align="center")
        _set_formula(ws2, c2, f"F{idx}", f"=Remediation_Summary!L{sr}", rec["rigorous_2027_int"], num_fmt="#,##0")
        _set_formula(ws2, c2, f"G{idx}", f"=Remediation_Summary!K{sr}", rec["direct_2027_int"], num_fmt="#,##0")
        cc = ws2.cell(row=idx, column=8, value=chk)
        cc.font = Font(name="Calibri", size=9.5, color="222222")
        cc.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cc.border = B_CELL
        ws2.row_dimensions[idx].height = 34
    _set_widths(ws2, [12, 18, 20, 20, 20, 18, 16, 68], freeze="A5")

    # Sheet 3: Corridor_Q3_Breakdown
    ws3 = wb.create_sheet("Corridor_Q3_Breakdown")
    c3 = cache.setdefault("xl/worksheets/sheet3.xml", {})
    ws3["A1"] = "2027 Projected Excess Container-Days by North Sea Port Corridor and Calendar Quarter"
    ws3["A1"].font = Font(name="Calibri", size=12, bold=True, color=NAVY_HEX)
    ws3["A2"] = "All 8 operational causes combined under Charter RC-2027 Clause 4.2 (calendar quarters: Q3 = 1 Jul to 30 Sep)"
    ws3["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    ws3["A4"] = "Port Corridor Breakdown (2027)"
    ws3["A4"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    for ci, h in enumerate(["Port", "2027 Excess C-Days", "Network Share (%)"], start=1):
        ws3.cell(row=5, column=ci, value=h)
    _style_hdr(ws3, 5, 3)

    p_order = [("BHV", "Bremerhaven (BHV)"), ("HAM", "Hamburg (HAM)"), ("WHV", "Wilhelmshaven (WHV)")]
    p_tot = sum(fig["by_port_2027"][p] for p, _ in p_order)
    for idx, (pc, plbl) in enumerate(p_order, start=6):
        val = fig["by_port_2027"][pc]
        ws3.cell(row=idx, column=1, value=plbl).border = B_CELL
        c_v = ws3.cell(row=idx, column=2, value=val)
        c_v.number_format = "#,##0.00"
        c_v.alignment = Alignment(horizontal="right", vertical="center")
        c_v.border = B_CELL
        _set_formula(ws3, c3, f"C{idx}", f"=B{idx}/$B$9", val / p_tot, num_fmt="0.00%")
        ws3.row_dimensions[idx].height = 20
    ws3.cell(row=9, column=1, value="TOTAL NETWORK").font = Font(name="Calibri", size=10, bold=True)
    ws3.cell(row=9, column=1).fill = TOT_FILL
    ws3.cell(row=9, column=1).border = B_TOT
    _set_formula(ws3, c3, "B9", "=SUM(B6:B8)", p_tot, num_fmt="#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "C9", "=SUM(C6:C8)", 1.0, num_fmt="0.00%", bold=True, fill=TOT_FILL)

    ws3["D4"] = "Calendar Quarter Breakdown (2027)"
    ws3["D4"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    for ci, h in enumerate(["Quarter", "2027 Excess C-Days", "Network Share (%)"], start=4):
        ws3.cell(row=5, column=ci, value=h)
    for ci in (4, 5, 6):
        cc = ws3.cell(row=5, column=ci)
        cc.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cc.fill = HEAD_FILL
        cc.alignment = Alignment(horizontal="center", vertical="center")
        cc.border = B_HDR
    q_order = [("Q1", "Q1 (Jan-Mar)"), ("Q2", "Q2 (Apr-Jun)"), ("Q3", "Q3 (Jul-Sep)"), ("Q4", "Q4 (Oct-Dec)")]
    q_tot = sum(fig["by_quarter_2027"][q] for q, _ in q_order)
    for idx, (qc, qlbl) in enumerate(q_order, start=6):
        val = fig["by_quarter_2027"][qc]
        ws3.cell(row=idx, column=4, value=qlbl).border = B_CELL
        c_v = ws3.cell(row=idx, column=5, value=val)
        c_v.number_format = "#,##0.00"
        c_v.alignment = Alignment(horizontal="right", vertical="center")
        c_v.border = B_CELL
        _set_formula(ws3, c3, f"F{idx}", f"=E{idx}/$E$10", val / q_tot, num_fmt="0.00%")
        if qc == "Q3":
            for cc_i in (4, 5, 6):
                ws3.cell(row=idx, column=cc_i).fill = REM_FILL
                ws3.cell(row=idx, column=cc_i).font = Font(name="Calibri", size=10, bold=True)
        ws3.row_dimensions[idx].height = 20
    ws3.cell(row=10, column=4, value="TOTAL NETWORK").font = Font(name="Calibri", size=10, bold=True)
    ws3.cell(row=10, column=4).fill = TOT_FILL
    ws3.cell(row=10, column=4).border = B_TOT
    _set_formula(ws3, c3, "E10", "=SUM(E6:E9)", q_tot, num_fmt="#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "F10", "=SUM(F6:F9)", 1.0, num_fmt="0.00%", bold=True, fill=TOT_FILL)
    _set_widths(ws3, [24, 20, 18, 22, 20, 18], freeze="A6")

    # Sheet 4: Conservation_Diagnostics
    ws4 = wb.create_sheet("Conservation_Diagnostics")
    ws4["A1"] = "Data Hygiene Tie-Outs and Native-Unit Cross-File Physical Conservation Checks"
    ws4["A1"].font = Font(name="Calibri", size=12, bold=True, color=NAVY_HEX)
    ws4["A2"] = "Every physical diagnostic is measured directly in native operational units from shipped 2026 extracts"
    ws4["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    cl = fig["cleaning"]
    cs = fig["chamber_stats"]
    diag_rows = [
        ["Layer 1 Hygiene", "Settled 2026 import containers (after VOID & superseded dedup)", f"{cl['milestones_settled_containers']:,} containers", f"Raw {cl['milestones_raw_rows']:,}; dropped {cl['milestones_void_dropped']} VOID and {cl['milestones_superseded_dropped']} superseded v1"],
        ["Layer 1 Hygiene", "Settled 2026 conserved network excess container-days", f"{fig['total_2026_cdays']:,.2f} c-days", f"Max timestamp-vs-field error across 8 stages = {cl['max_timestamp_excess_err_cdays']:.6f} c-days"],
        ["Layer 1 Hygiene", "Warehouse daily pallet stock-flow tie-out across 1,460 DC-days", f"{cl['stock_flow_max_diff_pallets']} pallets max diff", f"Deduped {cl['pallets_superseded_dropped']:,} superseded batches; converted {cl['pallets_case_unit_rows']:,} CASE rows; parsed {cl['pallets_de_date_rows']:,} DD.MM.YYYY dates"],
        ["Layer 1 Hygiene", "Physical empty-depot gate acceptance (depot_turnin_log_2026.csv)", f"{cl['turnin_physical_acceptance_pct']:.2f}%", f"{cl['turnin_turnaway_events']} physical turn-aways; deduped {cl['turnin_superseded_dropped']} rows; resolved {cl['turnin_legacy_carrier_rows']:,} legacy carrier codes"],
        ["F1 (S1: Cold-Store)", "Aggregate DC daily utilization range vs +2C chamber peak", f"{cs['total_dc_util_min_pct']:.1f}% to {cs['total_dc_util_max_pct']:.1f}% total | {cs['z02_util_max_pct']:.1f}% Z02", f"{cs['capped_boxes_count']:,} containers discharged against >=95% saturated destination chambers"],
        ["F1 (S1: Cold-Store)", "Same-vessel unsaturated-chamber twin port-dwell contrast", f"+{diag['F1_twin_gap_h']:.2f} hours", f"Rigorous total-DC regression predicts only +{diag['F1_rigorous_h']:.2f} h; reallocates {diag['cs_pb_26']:,.2f} 2026 c-days to coldstore_dock"],
        ["F2 (S2: Rail/BIP)", "Empirical CHED notice rail booking lock cutoff", f"<= {diag['empiric_lock_h']} hours pre-departure", f"{cs['locked_phyto_slots']} rail-booked containers frozen inside 24h lock across {cl['bip_notices_count']} BIP-inspected CHED lots"],
        ["F2 (S2: Rail/BIP)", "Shared-train weighbridge mass deficit per locked empty wagon", f"{diag['F2_tonnes_per_slot']:.2f} tonnes/slot", f"Declared loaded 40' reefer gross mass = {diag['measured_reefer_tonnes']:.2f} t (rigorous/rail-resale = 0.00 t); reallocates {diag['ph_bump_26']:,.2f} 2026 c-days to phyto_insp"],
        ["F3 (S3: Empty Depot)", "Same-DC same-day closed-quota vs open-quota ocean-line contrast", f"+{diag['F3_line_gap_h']:.2f} hours", f"{cs['closed_quota_boxes']:,} containers unloaded on quota-closed line-days; reallocates {diag['ed_blk_26']:,.2f} 2026 c-days to empty_depot"],
        ["F3 (S3: Empty Depot)", "Portal rejection retry-to-blocked-stock multiplicity ratio", f"{diag['F3_retry_mult']:.2f}x", f"{cs['portal_rejected_total']:,} total unlinked portal rejections / {diag['ed_blk_26']:,.1f} blocked c-days (refutes naive 1-to-1 portal counting)"],
    ]
    for ci, h in enumerate(["Check Group", "Diagnostic Quantity", "Measured Value", "Operational Proof & Reconciliation"], start=1):
        ws4.cell(row=4, column=ci, value=h)
    _style_hdr(ws4, 4, 4)
    for ri, rvals in enumerate(diag_rows, start=5):
        for ci, val in enumerate(rvals, start=1):
            cc = ws4.cell(row=ri, column=ci, value=val)
            cc.font = Font(name="Calibri", size=10, bold=(ci == 3), color="111111")
            cc.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            cc.border = B_CELL
            if ri % 2 == 0:
                cc.fill = ZEBRA_FILL
        ws4.row_dimensions[ri].height = 28
    _set_widths(ws4, [20, 44, 28, 66], freeze="A5")

    # Sheet 5: Routes_Comparison
    ws5 = wb.create_sheet("Routes_Comparison")
    ws5["A1"] = "Analytical Route and Shortcut Lattice Comparison (Projected 2027 Container-Days)"
    ws5["A1"].font = Font(name="Calibri", size=12, bold=True, color=NAVY_HEX)
    ws5["A2"] = "Every single shortcut, single-stump omission, over-correction, and 2026 unprojected route files a different wrong slate"
    ws5["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    m_cols = ["coldstore_dock", "rail_handoff", "empty_depot", "reefer_plug", "phyto_insp", "drayage_carrier", "vessel_berth", "edi_docs"]
    hdrs5 = ["Route / Shortcut"] + m_cols + ["Designated REMEDIATE Set", "Matches Golden"]
    for ci, h in enumerate(hdrs5, start=1):
        ws5.cell(row=4, column=ci, value=h)
    _style_hdr(ws5, 4, len(hdrs5), height=32)

    gold_set = fig["remediate_set"]
    route_list = [
        ("Golden (all 3 physical conservation splits)", fig["routes"]["golden"]),
        ("Drop S1 alone (chamber stock-flow missed)", fig["lattice"]["S1"]),
        ("Drop S2 alone (locked empty rail wagons missed)", fig["lattice"]["S2"]),
        ("Drop S3 alone (empty-depot portal quotas missed)", fig["lattice"]["S3"]),
        ("Drop S1 + S2 (only S3 solved)", fig["lattice"]["S1+S2"]),
        ("Drop S1 + S3 (only S2 solved)", fig["lattice"]["S1+S3"]),
        ("Drop S2 + S3 (only S1 solved)", fig["lattice"]["S2+S3"]),
        ("Reflex / Direct TMS codes (S1+S2+S3 missed)", fig["routes"]["direct"]),
        ("Rigorous Standard (total DC OLS + direct CHED siblings)", fig["routes"]["rigorous"]),
        ("S1 Over-corrected (unnetted port yard on tight chambers)", fig["routes"]["S1_over"]),
        ("S2 Over-corrected (all rollovers on any BIP shuttle)", fig["routes"]["S2_over"]),
        ("S3 Over-corrected (raw unadjusted portal rejections)", fig["routes"]["S3_over"]),
        ("Generous run route (unnetted over-corrections)", fig["routes"]["generous"]),
        ("Calibrated run route (documentary dispute credits)", fig["routes"]["calibrated"]),
        ("Hedge run route (12-15% haircuts only)", fig["routes"]["hedge"]),
        ("Cutoff run route (threshold cuts without netting)", fig["routes"]["cutoff"]),
        ("2026 History Unprojected (no 2027 plan scaling)", fig["routes"]["history_2026_unprojected"]),
    ]
    for ri, (rname, rdata) in enumerate(route_list, start=5):
        match = rdata["remediate_set"] == gold_set
        ws5.cell(row=ri, column=1, value=rname).font = Font(name="Calibri", size=9.5, bold=(ri == 5))
        ws5.cell(row=ri, column=1).border = B_CELL
        for mi, m in enumerate(m_cols, start=2):
            val = rdata["members"][m]
            cc = ws5.cell(row=ri, column=mi, value=round(val, 1))
            cc.number_format = "#,##0.0"
            cc.alignment = Alignment(horizontal="right", vertical="center")
            cc.border = B_CELL
            if ri == 5:
                cc.fill = TOT_FILL
                cc.font = Font(name="Calibri", size=9.5, bold=True)
        ws5.cell(row=ri, column=10, value=", ".join(rdata["remediate_set"])).font = Font(name="Calibri", size=9)
        ws5.cell(row=ri, column=10).border = B_CELL
        cm = ws5.cell(row=ri, column=11, value="YES" if match else "NO")
        cm.alignment = Alignment(horizontal="center", vertical="center")
        cm.font = Font(name="Calibri", size=9.5, bold=True)
        cm.fill = MON_FILL if match else REM_FILL
        cm.border = B_CELL
        ws5.row_dimensions[ri].height = 20
    _set_widths(ws5, [44] + [14] * 8 + [42, 14], freeze="B5")

    # Sheet 6: Variant_Battery
    ws6 = wb.create_sheet("Variant_Battery")
    ws6["A1"] = "22-Variant Implementation Sensitivity and +/-20% Parameter Forcing Check (Zero Flips)"
    ws6["A1"].font = Font(name="Calibri", size=12, bold=True, color=NAVY_HEX)
    ws6["A2"] = "Every defensible estimator across S1, S2, and S3 and all 8 +/-20% forcing perturbations preserve the exact 5-of-8 REMEDIATE slate"
    ws6["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    hdrs6 = ["Variant / Forcing Test", "coldstore_dock", "rail_handoff", "empty_depot", "reefer_plug", "phyto_insp", "drayage_carrier", "Total 2027", "Cost (EUR M)", "Slate Holds"]
    for ci, h in enumerate(hdrs6, start=1):
        ws6.cell(row=4, column=ci, value=h)
    _style_hdr(ws6, 4, len(hdrs6), height=30)

    r_ptr = 5
    for v in fig["variants"]:
        ws6.cell(row=r_ptr, column=1, value=v["name"]).border = B_CELL
        for ci, key in enumerate(["coldstore_dock", "rail_handoff", "empty_depot", "reefer_plug", "phyto_insp", "drayage_carrier"], start=2):
            cc = ws6.cell(row=r_ptr, column=ci, value=v["members"][key])
            cc.number_format = "#,##0.0"
            cc.alignment = Alignment(horizontal="right", vertical="center")
            cc.border = B_CELL
        cc_t = ws6.cell(row=r_ptr, column=8, value=v["total_2027"])
        cc_t.number_format = "#,##0.0"
        cc_t.alignment = Alignment(horizontal="right", vertical="center")
        cc_t.border = B_CELL
        cc_e = ws6.cell(row=r_ptr, column=9, value=v["cost_eur_m"])
        cc_e.number_format = "0.000"
        cc_e.alignment = Alignment(horizontal="right", vertical="center")
        cc_e.border = B_CELL
        ch = ws6.cell(row=r_ptr, column=10, value="HOLD" if v["remediate_set"] == gold_set else "FLIP")
        ch.alignment = Alignment(horizontal="center", vertical="center")
        ch.fill = MON_FILL
        ch.font = Font(name="Calibri", size=9.5, bold=True)
        ch.border = B_CELL
        ws6.row_dimensions[r_ptr].height = 19
        r_ptr += 1

    r_ptr += 1
    ws6.cell(row=r_ptr, column=1, value="Forcing +/-20% Perturbations").font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    r_ptr += 1
    for ci, h in enumerate(["Perturbation", "Min REMEDIATE C-Days", "Max MONITOR C-Days", "Slate Holds"], start=1):
        ws6.cell(row=r_ptr, column=ci, value=h)
    _style_hdr(ws6, r_ptr, 4, height=24)
    r_ptr += 1
    for p in fig["perturbations"]:
        ws6.cell(row=r_ptr, column=1, value=p["input"]).border = B_CELL
        c_min = ws6.cell(row=r_ptr, column=2, value=p["min_remediate"])
        c_min.number_format = "#,##0.0"
        c_min.alignment = Alignment(horizontal="right", vertical="center")
        c_min.border = B_CELL
        c_max = ws6.cell(row=r_ptr, column=3, value=p["max_monitor"])
        c_max.number_format = "#,##0.0"
        c_max.alignment = Alignment(horizontal="right", vertical="center")
        c_max.border = B_CELL
        ch = ws6.cell(row=r_ptr, column=4, value="HOLD" if p["answer"] == gold_set else "FLIP")
        ch.alignment = Alignment(horizontal="center", vertical="center")
        ch.fill = MON_FILL
        ch.font = Font(name="Calibri", size=9.5, bold=True)
        ch.border = B_CELL
        ws6.row_dimensions[r_ptr].height = 19
        r_ptr += 1
    _set_widths(ws6, [44, 15, 14, 14, 14, 13, 16, 14, 14, 13], freeze="B5")

    # Sheet 7: Inputs_Plan_2027 (referenced by live formulas in Remediation_Summary!)
    ws7 = wb.create_sheet("Inputs_Plan_2027")
    ws7["A1"] = "Charter RC-2027 Threshold, Schedule B Daily EUR Tariffs, and 2027 Import Schedule Parameters"
    ws7["A1"].font = Font(name="Calibri", size=12, bold=True, color=NAVY_HEX)
    ws7["A2"] = "Exact inputs filed in weserfrucht_remediation_charter_rc2027.pdf and import_plan_2027.csv"
    ws7["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    ws7["A4"] = "Mandatory Remediation Threshold (c-days)"
    ws7["A4"].font = Font(name="Calibri", size=10, bold=True)
    ws7["A4"].fill = PARAM_FILL
    ws7["A4"].border = B_CELL
    ws7["B4"] = int(fig["threshold_cdays"])
    ws7["B4"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    ws7["B4"].number_format = "#,##0"
    ws7["B4"].fill = PARAM_FILL
    ws7["B4"].border = B_CELL

    ws7["A5"], ws7["B5"] = "Cause ID (Schedule B)", "2027 Daily Tariff (EUR)"
    _style_hdr(ws7, 5, 2, height=24)
    for ri, cid in enumerate(core.MEMBERS, start=6):
        ws7.cell(row=ri, column=1, value=cid).border = B_CELL
        ct = ws7.cell(row=ri, column=2, value=int(core.TARIFF_EUR[cid]))
        ct.number_format = "#,##0"
        ct.alignment = Alignment(horizontal="right", vertical="center")
        ct.border = B_CELL
        ws7.row_dimensions[ri].height = 19

    ws7["D5"], ws7["E5"], ws7["F5"], ws7["G5"] = "Parameter Group", "Entity", "2026 Base", "2027 Value"
    for ci in (4, 5, 6, 7):
        cc = ws7.cell(row=5, column=ci)
        cc.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cc.fill = HEAD_FILL
        cc.alignment = Alignment(horizontal="center", vertical="center")
        cc.border = B_HDR
    p_entries = []
    for p in core.PORTS:
        p_entries.append(("vol_growth_port", p, 1.0, core.PLAN_2027["vol_growth_port"][p]))
    for p in core.PORTS:
        p_entries.append(("plug_capacity_factor_2027", p, 1.0, core.PLAN_2027["plug_capacity_factor_2027"][p]))
    for z in core.ZONES:
        p_entries.append(("dc_zone_load_factor_2027", z, 1.0, core.PLAN_2027["dc_zone_load_factor_2027"][z]))
    for p in core.PORTS:
        p_entries.append(("bip_sampling_factor_2027", p, 1.0, core.PLAN_2027["bip_sampling_factor_2027"][p]))
    p_entries.append(("rail_fleet_factor_2027", "NETWORK", 1.0, core.PLAN_2027["rail_fleet_factor_2027"]))
    p_entries.append(("dray_contract_factor_2027", "NETWORK", 1.0, core.PLAN_2027["dray_contract_factor_2027"]))
    for l in core.LINES:
        p_entries.append(("line_volume_share", l, core.PLAN_2027["line_share_2026"][l], core.PLAN_2027["line_share_2027"][l]))
    for l in core.LINES:
        p_entries.append(("depot_load_factor_2027", l, 1.0, core.PLAN_2027["depot_load_factor_2027"][l]))
    for ri, (pg, ent, v26, v27) in enumerate(p_entries, start=6):
        ws7.cell(row=ri, column=4, value=pg).border = B_CELL
        ws7.cell(row=ri, column=5, value=ent).border = B_CELL
        c26 = ws7.cell(row=ri, column=6, value=v26)
        c26.number_format = "0.00"
        c26.alignment = Alignment(horizontal="right", vertical="center")
        c26.border = B_CELL
        c27 = ws7.cell(row=ri, column=7, value=v27)
        c27.number_format = "0.00"
        c27.alignment = Alignment(horizontal="right", vertical="center")
        c27.border = B_CELL
        ws7.row_dimensions[ri].height = 19
    _set_widths(ws7, [38, 22, 4, 28, 12, 12, 12], freeze="A6")

    wb.save(path)
    _inject_formula_cache(path, cache)
    postprocess.normalize_ooxml(
        path,
        creator=PK.PEOPLE["analyst"],
        last_by=PK.PEOPLE["procurement"],
        created="2027-01-20T09:18:00Z",
        modified="2027-01-21T14:32:17Z",
        excel=True,
        company=PK.ORG,
    )
    return path


# ------------------------------------------------------------------
# 3. Golden Slide Deck (7 widescreen slides + clean matplotlib PNGs)
# ------------------------------------------------------------------
def _png_bytes(fig_mpl):
    buf = io.BytesIO()
    fig_mpl.savefig(buf, format="png", dpi=220, bbox_inches="tight", facecolor="white", metadata={"Software": None})
    plt.close(fig_mpl)
    buf.seek(0)
    return buf


def _chart_cause_comparison(fig):
    causes = fig["causes"]
    labels = [r["cause_id"] for r in causes][::-1]
    gold_v = [r["cdays_2027"] for r in causes][::-1]
    rig_v = [r["rigorous_2027_int"] for r in causes][::-1]
    y = np.arange(len(labels))
    h = 0.36
    f, ax = plt.subplots(figsize=(7.6, 4.3))
    colors_g = ["#B83A2D" if v >= 2500 else "#2E6F5E" for v in gold_v]
    ax.barh(y + h / 2, gold_v, height=h, color=colors_g, label="Reconciled 2027 (Red = REMEDIATE, Green = MONITOR)")
    ax.barh(y - h / 2, rig_v, height=h, color="#AEB9C7", label="Rigorous Single-System Standard (wrong on 3 open causes)")
    ax.axvline(2500, color="#1B365D", linestyle="--", linewidth=1.6, label="Charter RC-2027 Threshold (2,500 c-days)")
    for yi, gv, rv in zip(y, gold_v, rig_v):
        ax.text(gv + 55, yi + h / 2, f"{gv:,.0f}", va="center", ha="left", fontsize=8.5, fontweight="bold", color="#1B365D")
        ax.text(rv + 55, yi - h / 2, f"{rv:,.0f}", va="center", ha="left", fontsize=7.8, color="#666666")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5, fontweight="bold")
    ax.set_xlabel("Projected 2027 Excess Container-Days", fontsize=9.5)
    ax.set_xlim(0, 5350)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.25)
    ax.legend(loc="lower right", fontsize=7.8, frameon=True)
    ax.set_title("Five Causes Clear 2,500 c-days; Rigorous Standard Mis-Designates Three", fontsize=10.5, fontweight="bold", color="#1B365D", pad=10)
    return _png_bytes(f)


def _chart_three_conservation(fig):
    d = fig["R5_diagnostics"]
    f, axes = plt.subplots(1, 3, figsize=(10.2, 2.95))
    ax = axes[0]
    ax.bar(["Reconciled\nTwin Contrast", "Rigorous\nTotal-DC OLS"], [d["F1_twin_gap_h"], d["F1_rigorous_h"]], color=["#B83A2D", "#AEB9C7"], width=0.48)
    ax.set_ylabel("Port Dwell Gap (h)", fontsize=8.5)
    ax.set_title("S1: Same-Vessel Chamber\nSaturation Dwell Contrast", fontsize=9, fontweight="bold", color="#1B365D")
    ax.set_ylim(0, 25)
    ax.tick_params(axis="x", labelsize=8.2)
    for xi, v in enumerate([d["F1_twin_gap_h"], d["F1_rigorous_h"]]):
        ax.text(xi, v + 0.7, f"+{v:.2f} h", ha="center", fontsize=8.4, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    ax.bar(["Locked\nWagon", "40' Reefer\nBoL Mean", "Rail-Resale\nNull"], [abs(d["F2_tonnes_per_slot"]), d["measured_reefer_tonnes"], 0.0], color=["#1B365D", "#2E6F5E", "#AEB9C7"], width=0.50)
    ax.set_ylabel("Weight Drop (t / slot)", fontsize=8.5)
    ax.set_title("S2: Shared-Train Weighbridge\nEmpty-Wagon Mass Deficit", fontsize=9, fontweight="bold", color="#1B365D")
    ax.set_ylim(0, 35)
    ax.tick_params(axis="x", labelsize=8.2)
    for xi, v in enumerate([abs(d["F2_tonnes_per_slot"]), d["measured_reefer_tonnes"], 0.0]):
        ax.text(xi, v + 0.9, f"{v:.1f} t", ha="center", fontsize=8.4, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[2]
    ax.bar(["Closed vs Open\nOcean Line", "Rigorous\nGate-Only"], [d["F3_line_gap_h"], d["F3_rigorous_h"]], color=["#C77D26", "#AEB9C7"], width=0.48)
    ax.set_ylabel("Turnaround Gap (h)", fontsize=8.5)
    ax.set_title("S3: Same-DC Same-Day\nQuota-Closed Line Gap", fontsize=9, fontweight="bold", color="#1B365D")
    ax.set_ylim(0, 14)
    ax.tick_params(axis="x", labelsize=8.2)
    for xi, v in enumerate([d["F3_line_gap_h"], d["F3_rigorous_h"]]):
        ax.text(xi, v + 0.4, f"+{v:.2f} h", ha="center", fontsize=8.4, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    f.tight_layout(pad=1.1)
    return _png_bytes(f)


def _chart_corridor_quarter(fig):
    f, axes = plt.subplots(1, 2, figsize=(9.6, 3.05))
    ax = axes[0]
    p_lbls = ["Bremerhaven\n(BHV)", "Hamburg\n(HAM)", "Wilhelmshaven\n(WHV)"]
    p_vals = [fig["by_port_2027"]["BHV"], fig["by_port_2027"]["HAM"], fig["by_port_2027"]["WHV"]]
    ax.bar(p_lbls, p_vals, color=["#1B365D", "#3B5373", "#8FA3B8"], width=0.50)
    ax.set_ylabel("2027 Excess C-Days", fontsize=8.8)
    ax.set_title("2027 Excess Exposure by North Sea Port", fontsize=9.8, fontweight="bold", color="#1B365D")
    ax.set_ylim(0, max(p_vals) * 1.24)
    ax.tick_params(axis="x", labelsize=8.6)
    for xi, v in enumerate(p_vals):
        ax.text(xi, v + 300, f"{v:,.0f}\n({100*v/sum(p_vals):.1f}%)", ha="center", fontsize=8.4, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    q_lbls = ["Q1\n(Jan-Mar)", "Q2\n(Apr-Jun)", "Q3\n(Jul-Sep)", "Q4\n(Oct-Dec)"]
    q_vals = [fig["by_quarter_2027"][q] for q in ("Q1", "Q2", "Q3", "Q4")]
    ax.bar(q_lbls, q_vals, color=["#8FA3B8", "#8FA3B8", "#B83A2D", "#8FA3B8"], width=0.52)
    ax.set_ylabel("2027 Excess C-Days", fontsize=8.8)
    ax.set_title(f"2027 Quarterly Profile (Q3 = {100.0 * q_vals[2] / sum(q_vals):.1f}% of Annual Exposure)", fontsize=9.8, fontweight="bold", color="#1B365D")
    ax.set_ylim(0, max(q_vals) * 1.24)
    ax.tick_params(axis="x", labelsize=8.6)
    for xi, v in enumerate(q_vals):
        ax.text(xi, v + 280, f"{v:,.0f}\n({100*v/sum(q_vals):.1f}%)", ha="center", fontsize=8.4, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    f.tight_layout(pad=1.2)
    return _png_bytes(f)


def write_pptx(out_dir, fig):
    path = os.path.join(out_dir, GOLDEN_FILES["pptx"])
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    title_only = prs.slide_layouts[5]

    C_NAVY = RGBColor(0x1B, 0x36, 0x5D)
    C_SLATE = RGBColor(0x3B, 0x53, 0x73)
    C_RED = RGBColor(0xB8, 0x3A, 0x2D)
    C_GREEN = RGBColor(0x2E, 0x6F, 0x5E)
    C_TEXT = RGBColor(0x1F, 0x29, 0x37)
    C_MUTED = RGBColor(0x5A, 0x66, 0x77)
    C_BG_CARD = RGBColor(0xF3, 0xF6, 0xFA)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

    def _chrome(slide, title_text, slide_no, source_txt):
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.14))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_NAVY
        bar.line.fill.background()

        title_ph = slide.shapes.title
        title_ph.left, title_ph.top, title_ph.width, title_ph.height = Inches(0.55), Inches(0.24), Inches(12.2), Inches(0.68)
        tf = title_ph.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.text = title_text
        p.font.name = "Calibri"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(0.96), Inches(12.2), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(0xD0, 0xD8, 0xE2)
        line.line.fill.background()

        ft = slide.shapes.add_textbox(Inches(0.55), Inches(7.05), Inches(10.8), Inches(0.32))
        fp = ft.text_frame.paragraphs[0]
        fp.text = source_txt
        fp.font.name = "Calibri"
        fp.font.size = Pt(8.5)
        fp.font.color.rgb = C_MUTED

        pn = slide.shapes.add_textbox(Inches(11.8), Inches(7.05), Inches(0.95), Inches(0.32))
        pp = pn.text_frame.paragraphs[0]
        pp.alignment = PP_ALIGN.RIGHT
        pp.text = f"{slide_no} / 7"
        pp.font.name = "Calibri"
        pp.font.size = Pt(9)
        pp.font.bold = True
        pp.font.color.rgb = C_NAVY

    def _kpi_card(slide, left, top, width, height, label, big_val, sub_txt, accent=C_NAVY):
        shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shp.fill.solid()
        shp.fill.fore_color.rgb = C_BG_CARD
        shp.line.color.rgb = RGBColor(0xD0, 0xD8, 0xE2)
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left, tf.margin_right, tf.margin_top = Inches(0.16), Inches(0.16), Inches(0.12)
        p0 = tf.paragraphs[0]
        p0.text = label
        p0.font.name = "Calibri"
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = C_MUTED
        p1 = tf.add_paragraph()
        p1.text = big_val
        p1.font.name = "Calibri"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = sub_txt
        p2.font.name = "Calibri"
        p2.font.size = Pt(9)
        p2.font.color.rgb = C_TEXT

    def _bullets(slide, left, top, width, height, heading, items):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = heading
        p0.font.name = "Calibri"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = C_NAVY
        p0.space_after = Pt(6)
        for it in items:
            p = tf.add_paragraph()
            p.text = f"- {it}"
            p.font.name = "Calibri"
            p.font.size = Pt(11.5)
            p.font.color.rgb = C_TEXT
            p.space_after = Pt(6)

    d = fig["R5_diagnostics"]
    cs = fig["chamber_stats"]
    cl = fig["cleaning"]
    rt = fig["routes"]
    by_id = {r["cause_id"]: r for r in fig["causes"]}
    avoid_pct = 100.0 * fig["A_avoidable_eur_m"] / fig["A_cost_eur_m"]
    bhv_pct = 100.0 * fig["by_port_2027"]["BHV"] / fig["routes"]["golden"]["total_2027"]
    ham_pct = 100.0 * fig["by_port_2027"]["HAM"] / fig["routes"]["golden"]["total_2027"]
    q3_pct = 100.0 * fig["by_quarter_2027"]["Q3"] / fig["routes"]["golden"]["total_2027"]

    # Slide 1: Cover & Headline Call
    s1 = prs.slides.add_slide(title_only)
    band = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(2.55))
    band.fill.solid()
    band.fill.fore_color.rgb = C_NAVY
    band.line.fill.background()

    tb_kicker = s1.shapes.add_textbox(Inches(0.65), Inches(0.32), Inches(12.0), Inches(0.35))
    pk = tb_kicker.text_frame.paragraphs[0]
    pk.text = "WESERFRUCHT IMPORT GMBH  |  ANNUAL CARRIER CLOSE-OUT REVIEW (CHARTER RC-2027)"
    pk.font.name = "Calibri"
    pk.font.size = Pt(11)
    pk.font.bold = True
    pk.font.color.rgb = RGBColor(0xB8, 0xD0, 0xEB)

    s1_t = s1.shapes.title
    sp_tree = s1.shapes._spTree
    sp_tree.remove(s1_t._element)
    sp_tree.append(s1_t._element)
    s1_t.left, s1_t.top, s1_t.width, s1_t.height = Inches(0.65), Inches(0.72), Inches(12.0), Inches(1.15)
    tf1 = s1_t.text_frame
    tf1.word_wrap = True
    p2 = tf1.paragraphs[0]
    p2.alignment = PP_ALIGN.LEFT
    p2.text = f"Fund Five Mandatory Remediation Causes for 2027 (EUR {fig['A_avoidable_eur_m']:.3f}M Exposure); Remove Rail Handoff from Remediation"
    p2.font.name = "Calibri"
    p2.font.size = Pt(23)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    tb_sub = s1.shapes.add_textbox(Inches(0.65), Inches(1.96), Inches(12.0), Inches(0.45))
    p3 = tb_sub.text_frame.paragraphs[0]
    p3.text = f"2026 Conserved Attribution ({fig['total_2026_cdays_int']:,} c-days across 24,000 reefers) and 2027 Import Schedule Plan | Prepared by {PK.PEOPLE['analyst']}, 21 January 2027"
    p3.font.name = "Calibri"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(0xDE, 0xE7, 0xF2)

    _kpi_card(s1, 0.65, 2.85, 2.85, 1.45, "2027 NETWORK EXCESS", f"{fig['A_total_2027']:,} c-days", f"Band: {fig['agg_bands']['total_2027'][0]:,} to {fig['agg_bands']['total_2027'][1]:,}", C_NAVY)
    _kpi_card(s1, 3.70, 2.85, 2.85, 1.45, "2027 REMEDIATION SLATE", f"{fig['A_remed_days']:,} c-days", "5 of 8 causes >= 2,500 threshold", C_RED)
    _kpi_card(s1, 6.75, 2.85, 2.85, 1.45, "2027 TOTAL EXPOSURE", f"EUR {fig['A_cost_eur_m']:.3f}M", "Schedule B tariffs (EUR 140-285/d)", C_SLATE)
    _kpi_card(s1, 9.80, 2.85, 2.85, 1.45, "AVOIDABLE EXPOSURE", f"EUR {fig['A_avoidable_eur_m']:.3f}M", f"{avoid_pct:.1f}% of total network D&D cost", C_GREEN)

    _bullets(
        s1, 0.65, 4.55, 12.0, 2.3,
        "Executive Recommendation (Charter RC-2027 Clause 3.1)",
        [
            f"REMEDIATE (5 causes >= 2,500 c-days): vessel_berth ({by_id['vessel_berth']['cdays_2027_int']:,}), coldstore_dock ({by_id['coldstore_dock']['cdays_2027_int']:,}), drayage_carrier ({by_id['drayage_carrier']['cdays_2027_int']:,}), reefer_plug ({by_id['reefer_plug']['cdays_2027_int']:,}), and empty_depot ({by_id['empty_depot']['cdays_2027_int']:,}).",
            f"MONITOR (3 causes < 2,500 c-days): phyto_insp ({by_id['phyto_insp']['cdays_2027_int']:,}), rail_handoff ({by_id['rail_handoff']['cdays_2027_int']:,}), and edi_docs ({by_id['edi_docs']['cdays_2027_int']:,}).",
            f"Rejects direct TMS and rigorous single-system attributions, which wrongly fund rail_handoff ({rt['rigorous']['members']['rail_handoff']:,.0f} to {rt['direct']['members']['rail_handoff']:,.0f} c-days) while omitting coldstore_dock ({rt['direct']['members']['coldstore_dock']:,.0f} to {rt['rigorous']['members']['coldstore_dock']:,.0f}) and empty_depot ({rt['direct']['members']['empty_depot']:,.0f}).",
        ],
    )

    # Slide 2: Ranked 2027 Causes Chart
    s2 = prs.slides.add_slide(title_only)
    _chrome(s2, "Five Causes Clear 2,500 c-days in 2027; Single-System Attribution Mis-Designates Three", 2, "Source: Weserfrucht 2026 settled operational records reconciled to Charter RC-2027 and import_plan_2027.csv.")
    s2.shapes.add_picture(_chart_cause_comparison(fig), Inches(0.55), Inches(1.15), width=Inches(8.1))
    _bullets(
        s2, 8.85, 1.25, 3.9, 5.5,
        "Three Decisive Shifts",
        [
            f"coldstore_dock rises from {rt['direct']['members']['coldstore_dock']:,.0f} (TMS) / {rt['rigorous']['members']['coldstore_dock']:,.0f} (total-DC OLS) to {by_id['coldstore_dock']['cdays_2027_int']:,} c-days (REMEDIATE), offsetting reefer_plug from {rt['direct']['members']['reefer_plug']:,.0f} to {by_id['reefer_plug']['cdays_2027_int']:,}.",
            f"rail_handoff drops from {rt['direct']['members']['rail_handoff']:,.0f} (TMS) / {rt['rigorous']['members']['rail_handoff']:,.0f} (CHED sibling join) to {by_id['rail_handoff']['cdays_2027_int']:,} c-days (MONITOR), moving locked empty wagons to phyto_insp ({by_id['phyto_insp']['cdays_2027_int']:,}).",
            f"empty_depot climbs from {rt['direct']['members']['empty_depot']:,.0f} (physical gate only) to {by_id['empty_depot']['cdays_2027_int']:,} c-days (REMEDIATE), reducing drayage_carrier from {rt['direct']['members']['drayage_carrier']:,.0f} to {by_id['drayage_carrier']['cdays_2027_int']:,}.",
            "All 22 defensible estimator variants and all 8 +/-20% forcing checks preserve the identical 5-of-8 slate (0 flips).",
        ],
    )

    # Slide 3: Three Native-Unit Physical Conservation Proofs
    s3 = prs.slides.add_slide(title_only)
    _chrome(s3, "Three Independent Native-Unit Physical Conservation Laws Refute Single-System Readings", 3, "Source: Cross-file reconciliation of warehouse_pallet_movements, rail_shuttle_departures, bip_inspection_notices, and depot_portal_requests.")
    s3.shapes.add_picture(_chart_three_conservation(fig), Inches(0.55), Inches(1.18), width=Inches(12.2))
    _bullets(
        s3, 0.65, 5.05, 12.0, 1.85,
        f"Why Single-System Checks Passed on the Surface Yet Mis-Attributed {d['contrast_cdays_26']:,.0f} Conserved 2026 Container-Days",
        [
            f"F1 (Port vs Cold-Store): Aggregate DC occupancy sits flat at {cs['total_dc_util_min_pct']:.1f}% to {cs['total_dc_util_max_pct']:.1f}%, but SKU chamber stock-flow hits {cs['z02_util_max_pct']:.1f}% in +2C; same-vessel twins bound for saturated chambers dwell +{d['F1_twin_gap_h']:.2f} h longer in the exact same port stack.",
            f"F2 (Rail vs Border BIP): Shared trains drop {abs(d['F2_tonnes_per_slot']):.2f} tonnes per post-T-24h CHED-locked slot (matching declared {d['measured_reefer_tonnes']:.2f} t loaded reefer mass), proving locked wagons ran inland physically empty rather than resold.",
            f"F3 (Drayage vs Empty Depot): Physical gate acceptance reads {cl['turnin_physical_acceptance_pct']:.2f}%, yet same-DC same-day ocean lines facing portal closures dwell +{d['F3_line_gap_h']:.2f} h longer, with {d['F3_retry_mult']:.2f}x dispatcher retry multiplicity.",
        ],
    )

    # Slide 4: Deep Dive S1 & S2
    s4 = prs.slides.add_slide(title_only)
    _chrome(s4, "S1 and S2: Sealed Chamber Stock-Flow and 24-Hour Rail Wagon Locks Overturn TMS Labels", 4, "Source: dc_chamber_register_2026.csv, warehouse_pallet_movements_2026.csv, customs_consignment_bol_2026.csv, rail_shuttle_departures_2026.csv.")
    _bullets(
        s4, 0.60, 1.20, 5.9, 5.6,
        "S1: Inland Cold-Store Saturation Inside TERM_YARD_HOLD",
        [
            f"Cleaned {cl['pallets_raw_rows']:,} WMS lines ({cl['pallets_superseded_dropped']:,} superseded revisions, {cl['pallets_case_unit_rows']:,} CASE conversions, {cl['pallets_de_date_rows']:,} DD.MM.YYYY dates) reconcile to 0 pallets error against aggregate DC stock across all {cl['dc_days_total']:,} DC-days.",
            f"Anti-correlated berry (+2C summer), citrus (+7C winter), and tropical (+13C shoulder) seasons keep total DC utilization flat ({cs['total_dc_util_min_pct']:.1f}% to {cs['total_dc_util_max_pct']:.1f}%), driving total-DC OLS to near zero (+{d['F1_rigorous_h']:.2f} h).",
            f"Matching {cs['capped_boxes_count']:,} saturated-chamber boxes against same-vessel unsaturated twins separates {d['cs_pb_26']:,.1f} 2026 c-days of inland pull-backs from true port plug congestion.",
            f"Carrying +48% 2027 Z02 load factor pushes coldstore_dock to {by_id['coldstore_dock']['cdays_2027_int']:,} (REMEDIATE) while Berth 4 plugs leave reefer_plug at {by_id['reefer_plug']['cdays_2027_int']:,} (REMEDIATE).",
        ],
    )
    _bullets(
        s4, 6.80, 1.20, 5.9, 5.6,
        "S2: Post-T-24h CHED Border Locks Inside RAIL_CAP_ROLL",
        [
            f"Direct CHED sibling linkage across {cl['bip_notices_count']} BIP-inspected lots shifts only {d['phyto_sibling_rail_26']:,.1f} 2026 c-days, leaving rail_handoff at {rt['rigorous']['members']['rail_handoff']:,.0f} c-days (still wrongly REMEDIATE).",
            f"Comparing exam_notice_ts_utc to planned shuttle departures identifies an exact 24-hour booking lock: {cs['locked_phyto_slots']} rail-booked containers froze after T-24h, leaving booked slots un-reallocated.",
            f"Weighbridge regression holding train wagon count fixed measures {d['F2_tonnes_per_slot']:.2f} t per post-24h locked slot vs {d['measured_reefer_tonnes']:.2f} t loaded reefer gross weight, proving 1-to-1 empty-wagon displacement ({d['ph_bump_26']:,.1f} 2026 c-days).",
            f"Under Nordbahn's 0.84x fleet factor and 2027 EU BIP sampling, rail_handoff falls to {by_id['rail_handoff']['cdays_2027_int']:,} (MONITOR) and phyto_insp rises to {by_id['phyto_insp']['cdays_2027_int']:,} (MONITOR).",
        ],
    )

    # Slide 5: Deep Dive S3 & Two-Sided Over-Correction Risks
    s5 = prs.slides.add_slide(title_only)
    _chrome(s5, f"S3: Ocean-Line Depot Quotas Push Empty Depot to {by_id['empty_depot']['cdays_2027_int']:,} c-days Without Erasing Drayage Backlog", 5, "Source: depot_turnin_log_2026.csv, depot_portal_requests_2026.csv, container_milestones_2026.csv, import_plan_2027.csv.")
    _bullets(
        s5, 0.60, 1.20, 5.9, 5.6,
        "S3: Resolving Unlinked Portal Rejections and Retry Multiplicity",
        [
            f"Physical depot turn-in gates accepted {cl['turnin_physical_acceptance_pct']:.2f}% of arrivals ({cl['turnin_turnaway_events']} turn-aways) because drayage dispatchers hold empties in carrier yards when an ocean line closes its online booking portal.",
            f"Because depot_portal_requests_2026.csv carries no container_id and logs {cs['portal_rejected_total']:,} repeated daily rejections ({d['F3_retry_mult']:.2f}x blocked container-days), raw rejection counts overstate depot blocks by more than 4x.",
            f"Contrasting {cs['closed_quota_boxes']:,} containers unloaded on closed-quota line-days against open-quota lines at the exact same DC and unload day nets peak summer carrier tightness and isolates {d['ed_blk_26']:,.1f} 2026 c-days (+{d['F3_line_gap_h']:.2f} h/box).",
            f"2027 Ocean Alliance volume growth into LINE_A/B and depot rebalancing lift empty_depot from {by_id['empty_depot']['cdays_2026_int']:,} in 2026 (MONITOR) to {by_id['empty_depot']['cdays_2027_int']:,} in 2027 (REMEDIATE).",
        ],
    )
    _bullets(
        s5, 6.80, 1.20, 5.9, 5.6,
        "Two-Sided Over-Correction Discipline (Why Netting Matters)",
        [
            f"Over-correcting S1 (attributing all port dwell on tight chambers without netting same-vessel baseline congestion) collapses reefer_plug to {rt['S1_over']['members']['reefer_plug']:,.0f} (< 2,500), wrongly cancelling port plug remediation.",
            f"Over-correcting S2 (assigning all rollovers on any BIP shuttle without enforcing the T-24h lock and concurrent rail short-consists) inflates phyto_insp to {rt['S2_over']['members']['phyto_insp']:,.0f} (> 2,500), triggering an unnecessary BIP capital program.",
            f"Over-correcting S3 (counting raw portal rejections 1-to-1 without correcting {d['F3_retry_mult']:.2f}x retry multiplicity and summer carrier peaks) collapses drayage_carrier to {rt['S3_over']['members']['drayage_carrier']:,.0f} (< 2,500), underfunding inland trucking relief.",
            "Baseline netting at all three boundaries keeps all five true bottlenecks funded and all three sub-threshold causes on routine monitoring.",
        ],
    )

    # Slide 6: Corridor & Q3 Profile
    s6 = prs.slides.add_slide(title_only)
    _chrome(s6, f"Bremerhaven ({bhv_pct:.1f}%) and Peak Q3 ({q3_pct:.1f}%) Concentrate 2027 Cold-Chain Exposure", 6, "Source: Reconciled 2027 Import Schedule projections across all eight causes under Charter RC-2027 Clauses 4.1-4.2.")
    s6.shapes.add_picture(_chart_corridor_quarter(fig), Inches(0.55), Inches(1.18), width=Inches(12.2))
    _kpi_card(s6, 0.65, 5.35, 3.85, 1.40, "BREMERHAVEN (BHV) 2027", f"{fig['A_bhv_2027']:,} c-days", f"Band: {fig['agg_bands']['bhv_2027'][0]:,} to {fig['agg_bands']['bhv_2027'][1]:,} ({bhv_pct:.1f}% of network)", C_NAVY)
    _kpi_card(s6, 4.74, 5.35, 3.85, 1.40, "HAMBURG (HAM) 2027", f"{fig['A_ham_2027']:,} c-days", f"Band: {fig['agg_bands']['ham_2027'][0]:,} to {fig['agg_bands']['ham_2027'][1]:,} ({ham_pct:.1f}% of network)", C_SLATE)
    _kpi_card(s6, 8.83, 5.35, 3.85, 1.40, "THIRD QUARTER (Q3) 2027", f"{fig['A_q3_2027']:,} c-days", f"Band: {fig['agg_bands']['q3_2027'][0]:,} to {fig['agg_bands']['q3_2027'][1]:,} (Jul-Sep peak)", C_RED)

    # Slide 7: 2027 Action Slate & Robustness
    s7 = prs.slides.add_slide(title_only)
    _chrome(s7, "2027 Carrier Close-Out Action Plan and 30-Check Robustness Verification", 7, "Source: weserfrucht_coldchain_remediation_2027.xlsx (Variant_Battery and Routes_Comparison tabs).")
    _bullets(
        s7, 0.60, 1.22, 6.0, 5.5,
        f"2027 Mandatory Remediation Funding Slate (EUR {fig['A_avoidable_eur_m']:.3f}M Avoidable)",
        [
            f"1. vessel_berth ({by_id['vessel_berth']['cdays_2027_int']:,} c-days | EUR {by_id['vessel_berth']['eur_2027_m']:.3f}M): Enforce berth-window SLA penalties and winter buffer scheduling across BHV/HAM ocean calls.",
            f"2. coldstore_dock ({by_id['coldstore_dock']['cdays_2027_int']:,} c-days | EUR {by_id['coldstore_dock']['eur_2027_m']:.3f}M): Contract seasonal +2C overflow cold-storage bays before the 2027 Q3 berry expansion (+48% zone load).",
            f"3. drayage_carrier ({by_id['drayage_carrier']['cdays_2027_int']:,} c-days | EUR {by_id['drayage_carrier']['eur_2027_m']:.3f}M): Add July-August harvest flex chassis and driver shifts alongside the 2027 dedicated contract.",
            f"4. reefer_plug ({by_id['reefer_plug']['cdays_2027_int']:,} c-days | EUR {by_id['reefer_plug']['eur_2027_m']:.3f}M): Supplement Berth 4 upgrade with priority plug allocation at HAM and winter storm peak surge racks.",
            f"5. empty_depot ({by_id['empty_depot']['cdays_2027_int']:,} c-days | EUR {by_id['empty_depot']['eur_2027_m']:.3f}M): Secure contractual guaranteed empty-return intake floors with LINE_A and LINE_B during Q2/Q3 rebalancing.",
        ],
    )
    _bullets(
        s7, 6.85, 1.22, 5.9, 5.5,
        "Routine Monitoring (< 2,500 c-days) and Forcing Proof",
        [
            f"Monitor without capital release: phyto_insp ({by_id['phyto_insp']['cdays_2027_int']:,} c-days, EUR {by_id['phyto_insp']['eur_2027_m']:.3f}M), rail_handoff ({by_id['rail_handoff']['cdays_2027_int']:,} c-days, EUR {by_id['rail_handoff']['eur_2027_m']:.3f}M), and edi_docs ({by_id['edi_docs']['cdays_2027_int']:,} c-days, EUR {by_id['edi_docs']['eur_2027_m']:.3f}M).",
            "22-Variant Battery: Mean/median/trimmed/port-day/port-week/OLS (S1), empirical/22h/24h/26h lock and slot/mass/OLS/Huber (S2), daily/weekly/fortnight/Fourier/5-day/rej>=2 (S3), and 2 joint rebuilds -> 22/22 identical 5-of-8 slate.",
            f"Forcing +/-20% Perturbations: All 8 perturbations hold the exact 5-of-8 slate (minimum REMEDIATE = {fig['forcing_min_remed']:,}; maximum MONITOR = {fig['forcing_max_monitor']:,} under +/-20% stress).",
            "Operational Quick Win: Negotiating a T-12h (vs T-24h) rail slot release rule with Nordbahn recovers phyto_insp locked-slot rollovers without capital spend.",
        ],
    )

    prs.save(path)
    postprocess.normalize_pptx(
        path,
        creator=PK.PEOPLE["analyst"],
        last_by=PK.PEOPLE["procurement"],
        created="2027-01-20T14:05:00Z",
        modified="2027-01-21T16:48:09Z",
        title="Weserfrucht 2026 Cold-Chain Delay Attribution and 2027 Remediation Review",
        company=PK.ORG,
        revision=5,
        total_time=118,
    )
    return path


def build_all(fig=None):
    if fig is None:
        fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    gdir = os.path.join(TASK_DIR, "golden")
    if os.path.isdir(gdir):
        shutil.rmtree(gdir)
    os.makedirs(gdir)

    write_csv(gdir, fig)
    write_xlsx(gdir, fig)
    write_pptx(gdir, fig)

    golden_fallback = {
        GOLDEN_FILES["csv"]: dt.datetime(2027, 1, 21, 13, 14, 42, tzinfo=UTC),
    }
    postprocess.own_mtimes(gdir, golden_fallback)

    # Cut both archives with distinct Europe/Berlin entry times
    postprocess.zip_folder(os.path.join(TASK_DIR, "target"), os.path.join(TASK_DIR, "target.zip"), zone="Europe/Berlin")
    postprocess.zip_folder(gdir, os.path.join(TASK_DIR, "golden.zip"), zone="Europe/Berlin")
    return gdir


if __name__ == "__main__":
    gdir = build_all()
    print("Built golden deliverables and cut target.zip + golden.zip:")
    for name in sorted(os.listdir(gdir)):
        print("  golden/%-46s %10d" % (name, os.path.getsize(os.path.join(gdir, name))))
    for z in ("target.zip", "golden.zip"):
        print("  %-53s %10d" % (z, os.path.getsize(os.path.join(TASK_DIR, z))))
