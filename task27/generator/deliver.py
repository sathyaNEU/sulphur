"""Build the three Architecture 2 golden deliverables strictly from figures.json and cut target.zip & golden.zip:
  1. weserfrucht_corridor_allocation_2027.csv (exact Charter RC-2027 Rev 3 Section 5.2 schema)
  2. weserfrucht_corridor_capital_model_2027.xlsx (100% live Excel formulas + chart, normalized OOXML)
  3. weserfrucht_remediation_allocation_2027.pptx (10-slide executive deck + crisp matplotlib charts, normalized OOXML)

Every Office container passes through house postprocess.py with distinct realistic timestamps after
as_of (2027-01-19), and both ZIPs are cut deterministically via postprocess.zip_folder(..., zone="Europe/Berlin").
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
    "csv": "weserfrucht_corridor_allocation_2027.csv",
    "xlsx": "weserfrucht_corridor_capital_model_2027.xlsx",
    "pptx": "weserfrucht_remediation_allocation_2027.pptx",
}

NAVY_HEX = "1B365D"
SLATE_HEX = "3B5373"
FUND_FILL_HEX = "D9EFE2"
DEFER_FILL_HEX = "F9E2DC"
TOT_FILL_HEX = "EAF0F7"
ZEBRA_HEX = "F6F8FB"
PARAM_HEX = "EEF3F9"

HEAD_FILL = PatternFill("solid", fgColor=NAVY_HEX)
FUND_FILL = PatternFill("solid", fgColor=FUND_FILL_HEX)
DEFER_FILL = PatternFill("solid", fgColor=DEFER_FILL_HEX)
TOT_FILL = PatternFill("solid", fgColor=TOT_FILL_HEX)
ZEBRA_FILL = PatternFill("solid", fgColor=ZEBRA_HEX)
PARAM_FILL = PatternFill("solid", fgColor=PARAM_HEX)
THIN = Side(style="thin", color="C4CDD8")
MED = Side(style="medium", color=NAVY_HEX)
B_CELL = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
B_HDR = Border(bottom=MED)
B_TOT = Border(top=MED, bottom=MED, left=THIN, right=THIN)


def _set_val(ws, ref, val, num_fmt=None, bold=False, fill=None, align="right"):
    c = ws[ref]
    c.value = val
    c.font = Font(name="Calibri", size=10, bold=bold, color="111111")
    if num_fmt:
        c.number_format = num_fmt
    if fill:
        c.fill = fill
    c.alignment = Alignment(horizontal=align, vertical="center")
    c.border = B_TOT if bold else B_CELL


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
# 1. Golden CSV (Charter RC-2027 Rev 3 Section 5.2 exact schema)
# ------------------------------------------------------------------
def write_csv(out_dir, fig):
    path = os.path.join(out_dir, GOLDEN_FILES["csv"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([
            "corridor_id", "port_id", "dc_id", "budget_eur",
            "c1_coldstore_pullback_2026", "c2_phyto_rail_roll_2026", "c3_depot_backlog_2026",
            "carrier_ctrl_cdays_2026", "carrier_ctrl_cdays_2027",
            "avoidable_eur_2027", "bcr_2027", "rank", "decision",
        ])
        for r in fig["corridors"]:
            wr.writerow([
                r["corridor_id"],
                r["port_id"],
                r["dc_id"],
                f"{r['budget_eur']:.2f}",
                f"{r['c1_coldstore_pullback_2026']:.1f}",
                f"{r['c2_phyto_rail_roll_2026']:.1f}",
                f"{r['c3_depot_backlog_2026']:.1f}",
                f"{r['carrier_ctrl_cdays_2026']:.1f}",
                f"{r['carrier_ctrl_cdays_2027']:.1f}",
                f"{r['avoidable_eur_2027']:.2f}",
                f"{r['bcr_2027']:.3f}",
                int(r["rank"]),
                r["decision"],
            ])
    return path


# ------------------------------------------------------------------
# 2. Golden Workbook (100% live Excel formulas + embedded chart)
# ------------------------------------------------------------------
def write_xlsx(out_dir, fig):
    path = os.path.join(out_dir, GOLDEN_FILES["xlsx"])
    wb = Workbook()
    cache = {}
    corrs = fig["corridors"]
    rt = fig["routes"]
    bands = fig["bands"]
    diag = fig["diagnostics"]

    # Sheet 1: Executive_Allocation
    ws1 = wb.active
    ws1.title = "Executive_Allocation"
    c1 = cache.setdefault("xl/worksheets/sheet1.xml", {})

    ws1["A1"] = (
        f"2027 Carrier-Remediation Capital Slate (EUR 1.75M Cap): Fund {', '.join(fig['funded_slate'])} "
        f"(EUR {fig['funded_budget_eur']:,.0f} deployed, EUR {fig['funded_avoidable_eur_2027']:,.0f} avoidable, BCR {fig['funded_portfolio_bcr']:.3f}); "
        f"Defer {', '.join(fig['deferred_slate'])}"
    )
    ws1["A1"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEX)
    ws1["A2"] = (
        f"{PK.ORG} | Charter RC-2027 (Rev 3) Annual Carrier Remediation Committee Controlling Model | "
        f"Prepared by {PK.PEOPLE['analyst']}, 21 January 2027"
    )
    ws1["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    ws1["A4"] = "Ranked Corridor Capital Allocation under EUR 1,750,000 Fixed Cap (Live Link to Attribution & 2027 Economics Tabs)"
    ws1["A4"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)

    hdrs1 = [
        "Rank", "Corridor", "Port", "DC", "Budget (EUR)",
        "2026 Carrier C-Days", "2027 Carrier C-Days", "2027 Avoidable (EUR)",
        "2027 BCR", "Decision", "21-Variant BCR Band", "Naive TMS BCR", "Rigorous Std BCR",
    ]
    for ci, h in enumerate(hdrs1, start=1):
        ws1.cell(row=5, column=ci, value=h)
    _style_hdr(ws1, 5, len(hdrs1), height=32)

    for idx, r in enumerate(corrs):
        rr = 6 + idx
        fill = FUND_FILL if r["decision"] == "FUND" else DEFER_FILL
        _set_val(ws1, f"A{rr}", r["rank"], "0", fill=fill, align="center")
        _set_val(ws1, f"B{rr}", r["corridor_id"], fill=fill, align="left")
        _set_val(ws1, f"C{rr}", r["port_id"], fill=fill, align="center")
        _set_val(ws1, f"D{rr}", r["dc_id"], fill=fill, align="center")
        _set_formula(ws1, c1, f"E{rr}", f"='2027_Corridor_Economics'!E{rr}", r["budget_eur"], "#,##0.00", fill=fill)
        _set_formula(ws1, c1, f"F{rr}", f"='2026_Attribution_Bridge'!M{rr}", r["carrier_ctrl_cdays_2026"], "#,##0.0", fill=fill)
        _set_formula(ws1, c1, f"G{rr}", f"='2027_Corridor_Economics'!I{rr}", r["carrier_ctrl_cdays_2027"], "#,##0.0", fill=fill)
        _set_formula(ws1, c1, f"H{rr}", f"='2027_Corridor_Economics'!L{rr}", r["avoidable_eur_2027"], "#,##0.00", fill=fill)
        _set_formula(ws1, c1, f"I{rr}", f"=H{rr}/E{rr}", r["avoidable_eur_2027"] / r["budget_eur"], "0.000", bold=True, fill=fill)
        # Live cumulative budget cap check
        cum_expr = f"SUM($E$6:E{rr})"
        _set_formula(ws1, c1, f"J{rr}", f'=IF({cum_expr}<=$C$15,"FUND","DEFER")', r["decision"], bold=True, fill=fill, align="center")
        bk = "BCR_" + r["corridor_id"].replace("-", "_")
        _set_val(ws1, f"K{rr}", f"{bands[bk][0]:.3f} - {bands[bk][1]:.3f}", fill=fill, align="center")
        _set_val(ws1, f"L{rr}", rt["direct"]["bcrs"][r["corridor_id"]], "0.000", fill=fill)
        _set_val(ws1, f"M{rr}", rt["rigorous"]["bcrs"][r["corridor_id"]], "0.000", fill=fill)
        ws1.row_dimensions[rr].height = 21

    # Row 12: Network 6-corridor totals
    tot_bud_all = sum(r["budget_eur"] for r in corrs)
    tot_cc26 = sum(r["carrier_ctrl_cdays_2026"] for r in corrs)
    tot_cc27 = sum(r["carrier_ctrl_cdays_2027"] for r in corrs)
    tot_av27 = sum(r["avoidable_eur_2027"] for r in corrs)
    _set_val(ws1, "A12", "", fill=TOT_FILL)
    _set_val(ws1, "B12", "ALL 6 CORRIDORS", bold=True, fill=TOT_FILL, align="left")
    _set_val(ws1, "C12", "", fill=TOT_FILL)
    _set_val(ws1, "D12", "", fill=TOT_FILL)
    _set_formula(ws1, c1, "E12", "=SUM(E6:E11)", tot_bud_all, "#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "F12", "=SUM(F6:F11)", tot_cc26, "#,##0.0", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "G12", "=SUM(G6:G11)", tot_cc27, "#,##0.0", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "H12", "=SUM(H6:H11)", tot_av27, "#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws1, c1, "I12", "=H12/E12", tot_av27 / tot_bud_all, "0.000", bold=True, fill=TOT_FILL)
    _set_val(ws1, "J12", "3 FUND / 3 DEFER", bold=True, fill=TOT_FILL, align="center")
    _set_val(ws1, "K12", "0/21 Flips", bold=True, fill=TOT_FILL, align="center")
    _set_val(ws1, "L12", "", fill=TOT_FILL)
    _set_val(ws1, "M12", "", fill=TOT_FILL)
    ws1.row_dimensions[12].height = 22

    # Capital Governance Block (Rows 14-21)
    ws1["A14"] = "Capital Cap & Portfolio Summary (Charter RC-2027 Section 4.1)"
    ws1["A14"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    _set_val(ws1, "A15", "Board Capital Budget Cap (EUR)", fill=PARAM_FILL, align="left")
    _set_val(ws1, "C15", core.BUDGET_CAP_EUR, "#,##0.00", bold=True, fill=PARAM_FILL)
    _set_val(ws1, "A16", "Deployed Capital (FUND Slate, EUR)", fill=FUND_FILL, align="left")
    _set_formula(ws1, c1, "C16", '=SUMIF(J6:J11,"FUND",E6:E11)', fig["funded_budget_eur"], "#,##0.00", bold=True, fill=FUND_FILL)
    _set_val(ws1, "A17", "Unspent Contingency Reserve (EUR)", fill=ZEBRA_FILL, align="left")
    _set_formula(ws1, c1, "C17", "=C15-C16", fig["unspent_budget_eur"], "#,##0.00", bold=True, fill=ZEBRA_FILL)
    _set_val(ws1, "A18", "Funded 2027 Avoidable D&D Exposure (EUR)", fill=FUND_FILL, align="left")
    _set_formula(ws1, c1, "C18", '=SUMIF(J6:J11,"FUND",H6:H11)', fig["funded_avoidable_eur_2027"], "#,##0.00", bold=True, fill=FUND_FILL)
    _set_val(ws1, "A19", "Funded Portfolio BCR (Avoidable EUR / Deployed EUR)", fill=TOT_FILL, align="left")
    _set_formula(ws1, c1, "C19", "=C18/C16", fig["funded_avoidable_eur_2027"] / fig["funded_budget_eur"], "0.000", bold=True, fill=TOT_FILL)
    _set_val(ws1, "A20", "Deferred 2027 Avoidable Exposure (EUR)", fill=DEFER_FILL, align="left")
    _set_formula(ws1, c1, "C20", '=SUMIF(J6:J11,"DEFER",H6:H11)', tot_av27 - fig["funded_avoidable_eur_2027"], "#,##0.00", fill=DEFER_FILL)

    # Non-Carrier Attribution Summary (Cols E-H, Rows 14-18)
    ws1["E14"] = "2026 Non-Carrier Delays Removed from Carrier Scope (Critical Components)"
    ws1["E14"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    _set_val(ws1, "E15", "C1: Cold-Store Chamber Pull-Back (2026 c-days)", fill=PARAM_FILL, align="left")
    _set_formula(ws1, c1, "G15", "='2026_Attribution_Bridge'!G12", sum(r["c1_coldstore_pullback_2026"] for r in corrs), "#,##0.0", bold=True, fill=PARAM_FILL)
    _set_val(ws1, "H15", f"Band: {bands['C1_coldstore_pullback_2026'][0]:,.1f} - {bands['C1_coldstore_pullback_2026'][1]:,.1f}", fill=PARAM_FILL, align="center")
    _set_val(ws1, "E16", "C2: BIP Rail Rollover Bump (2026 c-days)", fill=PARAM_FILL, align="left")
    _set_formula(ws1, c1, "G16", "='2026_Attribution_Bridge'!H12", sum(r["c2_phyto_rail_roll_2026"] for r in corrs), "#,##0.0", bold=True, fill=PARAM_FILL)
    _set_val(ws1, "H16", f"Band: {bands['C2_phyto_rail_roll_2026'][0]:,.1f} - {bands['C2_phyto_rail_roll_2026'][1]:,.1f}", fill=PARAM_FILL, align="center")
    _set_val(ws1, "E17", "C3: Empty-Depot Portal Backlog (2026 c-days)", fill=PARAM_FILL, align="left")
    _set_formula(ws1, c1, "G17", "='2026_Attribution_Bridge'!I12", sum(r["c3_depot_backlog_2026"] for r in corrs), "#,##0.0", bold=True, fill=PARAM_FILL)
    _set_val(ws1, "H17", f"Band: {bands['C3_depot_backlog_2026'][0]:,.1f} - {bands['C3_depot_backlog_2026'][1]:,.1f}", fill=PARAM_FILL, align="center")
    _set_val(ws1, "E18", "Direct CHED Rail Sibling Holds (2026 c-days)", fill=ZEBRA_FILL, align="left")
    _set_formula(ws1, c1, "G18", "='2026_Attribution_Bridge'!F12", sum(r["phyto_sibling_rail_2026"] for r in corrs), "#,##0.0", fill=ZEBRA_FILL)
    _set_val(ws1, "H18", "Direct phyto_insp", fill=ZEBRA_FILL, align="center")

    chart = BarChart()
    chart.type = "col"
    chart.title = "Projected 2027 Corridor BCR: Attributed Golden vs Naive TMS"
    chart.y_axis.title = "Benefit-Cost Ratio (EUR Avoidable / EUR Budget)"
    chart.x_axis.title = "Corridor"
    data_ref = Reference(ws1, min_col=9, min_row=5, max_col=9, max_row=11)
    naive_ref = Reference(ws1, min_col=12, min_row=5, max_col=12, max_row=11)
    cats_ref = Reference(ws1, min_col=2, min_row=6, max_row=11)
    chart.add_data(data_ref, titles_from_data=True)
    chart.add_data(naive_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.width = 18
    chart.height = 10
    ws1.add_chart(chart, "A22")
    _set_widths(ws1, [7, 13, 8, 8, 15, 17, 17, 18, 12, 12, 18, 14, 15], freeze="A6")

    # Sheet 2: 2026_Attribution_Bridge
    ws2 = wb.create_sheet("2026_Attribution_Bridge")
    c2 = cache.setdefault("xl/worksheets/sheet2.xml", {})
    ws2["A1"] = "2026 Container-Day Attribution Bridge: Raw TMS Stage Timers to Carrier-Controllable Channels"
    ws2["A1"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEX)
    ws2["A2"] = "Exact container/shuttle conservation: Raw TMS stage days = Attributed Carrier-Controllable + Removed Non-Carrier (C1, C2, C3, direct CHED siblings)"
    ws2["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    hdrs2 = [
        "Corridor", "Containers", "Raw Port Yard", "Raw Rail TMS", "Raw Dray Empty",
        "Direct CHED Rail Sibling", "C1: Coldstore Pull-Back", "C2: BIP Rail Rollover", "C3: Depot Portal Backlog",
        "Carrier Reefer Plug 2026", "Carrier Rail Handoff 2026", "Carrier Drayage 2026", "Total Carrier-Ctrl 2026",
    ]
    for ci, h in enumerate(hdrs2, start=1):
        ws2.cell(row=5, column=ci, value=h)
    _style_hdr(ws2, 5, len(hdrs2), height=32)

    for idx, r in enumerate(corrs):
        rr = 6 + idx
        fill = ZEBRA_FILL if idx % 2 == 1 else None
        _set_val(ws2, f"A{rr}", r["corridor_id"], bold=True, fill=fill, align="left")
        _set_val(ws2, f"B{rr}", r["containers_2026"], "#,##0", fill=fill)
        _set_val(ws2, f"C{rr}", r["raw_port_yard_2026"], "#,##0.0", fill=fill)
        _set_val(ws2, f"D{rr}", r["raw_rail_tms_2026"], "#,##0.0", fill=fill)
        _set_val(ws2, f"E{rr}", r["raw_dray_empty_2026"], "#,##0.0", fill=fill)
        _set_val(ws2, f"F{rr}", r["phyto_sibling_rail_2026"], "#,##0.0", fill=fill)
        _set_val(ws2, f"G{rr}", r["c1_coldstore_pullback_2026"], "#,##0.0", fill=fill)
        _set_val(ws2, f"H{rr}", r["c2_phyto_rail_roll_2026"], "#,##0.0", fill=fill)
        _set_val(ws2, f"I{rr}", r["c3_depot_backlog_2026"], "#,##0.0", fill=fill)
        plug_v = r["raw_port_yard_2026"] - r["c1_coldstore_pullback_2026"]
        rail_v = r["raw_rail_tms_2026"] - r["phyto_sibling_rail_2026"] - r["c2_phyto_rail_roll_2026"]
        dray_v = r["raw_dray_empty_2026"] - r["c3_depot_backlog_2026"]
        _set_formula(ws2, c2, f"J{rr}", f"=C{rr}-G{rr}", plug_v, "#,##0.0", fill=fill)
        _set_formula(ws2, c2, f"K{rr}", f"=D{rr}-F{rr}-H{rr}", rail_v, "#,##0.0", fill=fill)
        _set_formula(ws2, c2, f"L{rr}", f"=E{rr}-I{rr}", dray_v, "#,##0.0", fill=fill)
        _set_formula(ws2, c2, f"M{rr}", f"=J{rr}+K{rr}+L{rr}", plug_v + rail_v + dray_v, "#,##0.0", bold=True, fill=fill)
        ws2.row_dimensions[rr].height = 20

    _set_val(ws2, "A12", "TOTAL 2026", bold=True, fill=TOT_FILL, align="left")
    col_keys = [
        ("B", "containers_2026", "#,##0"),
        ("C", "raw_port_yard_2026", "#,##0.0"),
        ("D", "raw_rail_tms_2026", "#,##0.0"),
        ("E", "raw_dray_empty_2026", "#,##0.0"),
        ("F", "phyto_sibling_rail_2026", "#,##0.0"),
        ("G", "c1_coldstore_pullback_2026", "#,##0.0"),
        ("H", "c2_phyto_rail_roll_2026", "#,##0.0"),
        ("I", "c3_depot_backlog_2026", "#,##0.0"),
        ("J", "reefer_plug_2026", "#,##0.0"),
        ("K", "rail_handoff_2026", "#,##0.0"),
        ("L", "drayage_carrier_2026", "#,##0.0"),
        ("M", "carrier_ctrl_cdays_2026", "#,##0.0"),
    ]
    for col_l, key_n, nf in col_keys:
        if col_l == "J":
            val_s = sum(r["raw_port_yard_2026"] - r["c1_coldstore_pullback_2026"] for r in corrs)
        elif col_l == "K":
            val_s = sum(r["raw_rail_tms_2026"] - r["phyto_sibling_rail_2026"] - r["c2_phyto_rail_roll_2026"] for r in corrs)
        elif col_l == "L":
            val_s = sum(r["raw_dray_empty_2026"] - r["c3_depot_backlog_2026"] for r in corrs)
        elif col_l == "M":
            val_s = sum(
                (r["raw_port_yard_2026"] - r["c1_coldstore_pullback_2026"])
                + (r["raw_rail_tms_2026"] - r["phyto_sibling_rail_2026"] - r["c2_phyto_rail_roll_2026"])
                + (r["raw_dray_empty_2026"] - r["c3_depot_backlog_2026"])
                for r in corrs
            )
        else:
            val_s = sum(r[key_n] for r in corrs)
        _set_formula(ws2, c2, f"{col_l}12", f"=SUM({col_l}6:{col_l}11)", val_s, nf, bold=True, fill=TOT_FILL)
    ws2.row_dimensions[12].height = 22
    _set_widths(ws2, [13, 12, 14, 14, 15, 16, 17, 16, 17, 17, 17, 16, 18], freeze="A6")

    # Sheet 3: 2027_Corridor_Economics
    ws3 = wb.create_sheet("2027_Corridor_Economics")
    c3 = cache.setdefault("xl/worksheets/sheet3.xml", {})
    ws3["A1"] = "2027 Corridor Carrier-Controllable Projection, Schedule B Valuation & Benefit-Cost Ratio Model"
    ws3["A1"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEX)
    ws3["A2"] = "Schedule B Tariffs: Reefer Plug EUR 210/day | Rail Handoff EUR 175/day | Drayage Carrier EUR 160/day (Charter RC-2027 Annex B & C)"
    ws3["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    # Tariff parameters in Row 14-16
    ws3["A14"] = "Schedule B Daily Tariffs (EUR/day)"
    ws3["A14"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    _set_val(ws3, "A15", "reefer_plug", fill=PARAM_FILL, align="left")
    _set_val(ws3, "B15", core.TARIFF_EUR["reefer_plug"], "#,##0.00", bold=True, fill=PARAM_FILL)
    _set_val(ws3, "A16", "rail_handoff", fill=PARAM_FILL, align="left")
    _set_val(ws3, "B16", core.TARIFF_EUR["rail_handoff"], "#,##0.00", bold=True, fill=PARAM_FILL)
    _set_val(ws3, "A17", "drayage_carrier", fill=PARAM_FILL, align="left")
    _set_val(ws3, "B17", core.TARIFF_EUR["drayage_carrier"], "#,##0.00", bold=True, fill=PARAM_FILL)

    hdrs3 = [
        "Corridor", "2027 Vol Growth", "Plug Cap Factor", "Rail Fleet Factor",
        "Budget (EUR)", "Plug 2027 Days", "Rail 2027 Days", "Dray 2027 Days",
        "Total Carrier 2027 Days", "Gross 2027 EUR", "Capture Rate", "Avoidable 2027 EUR", "BCR 2027", "Dray Factor",
    ]
    for ci, h in enumerate(hdrs3, start=1):
        ws3.cell(row=5, column=ci, value=h)
    _style_hdr(ws3, 5, len(hdrs3), height=32)

    for idx, r in enumerate(corrs):
        rr = 6 + idx
        fill = ZEBRA_FILL if idx % 2 == 1 else None
        p26 = r["raw_port_yard_2026"] - r["c1_coldstore_pullback_2026"]
        r26 = r["raw_rail_tms_2026"] - r["phyto_sibling_rail_2026"] - r["c2_phyto_rail_roll_2026"]
        d26 = r["raw_dray_empty_2026"] - r["c3_depot_backlog_2026"]
        p27 = p26 * r["vol_growth_2027"] * r["plug_factor_2027"]
        r27 = r26 * r["vol_growth_2027"] * r["rail_factor_2027"]
        d27 = d26 * r["vol_growth_2027"] * r["dray_factor_2027"]
        gr27 = p27 * 210.0 + r27 * 175.0 + d27 * 160.0
        av27 = gr27 * r["capture_rate_2027"]
        bcr27 = av27 / r["budget_eur"]

        _set_val(ws3, f"A{rr}", r["corridor_id"], bold=True, fill=fill, align="left")
        _set_val(ws3, f"B{rr}", r["vol_growth_2027"], "0.00", fill=fill)
        _set_val(ws3, f"C{rr}", r["plug_factor_2027"], "0.00", fill=fill)
        _set_val(ws3, f"D{rr}", r["rail_factor_2027"], "0.00", fill=fill)
        _set_val(ws3, f"E{rr}", r["budget_eur"], "#,##0.00", fill=fill)
        _set_formula(ws3, c3, f"F{rr}", f"='2026_Attribution_Bridge'!J{rr}*B{rr}*C{rr}", p27, "#,##0.0", fill=fill)
        _set_formula(ws3, c3, f"G{rr}", f"='2026_Attribution_Bridge'!K{rr}*B{rr}*D{rr}", r27, "#,##0.0", fill=fill)
        _set_formula(ws3, c3, f"H{rr}", f"='2026_Attribution_Bridge'!L{rr}*B{rr}*N{rr}", d27, "#,##0.0", fill=fill)
        _set_formula(ws3, c3, f"I{rr}", f"=F{rr}+G{rr}+H{rr}", p27 + r27 + d27, "#,##0.0", bold=True, fill=fill)
        _set_formula(ws3, c3, f"J{rr}", f"=F{rr}*$B$15+G{rr}*$B$16+H{rr}*$B$17", gr27, "#,##0.00", fill=fill)
        _set_val(ws3, f"K{rr}", r["capture_rate_2027"], "0.0%", fill=fill)
        _set_formula(ws3, c3, f"L{rr}", f"=J{rr}*K{rr}", av27, "#,##0.00", bold=True, fill=fill)
        _set_formula(ws3, c3, f"M{rr}", f"=L{rr}/E{rr}", bcr27, "0.000", bold=True, fill=fill)
        _set_val(ws3, f"N{rr}", r["dray_factor_2027"], "0.00", fill=fill)
        ws3.row_dimensions[rr].height = 20

    _set_val(ws3, "A12", "TOTAL 2027", bold=True, fill=TOT_FILL, align="left")
    for col_l in ("B", "C", "D", "K", "N"):
        _set_val(ws3, f"{col_l}12", "", fill=TOT_FILL)
    _set_formula(ws3, c3, "E12", "=SUM(E6:E11)", sum(r["budget_eur"] for r in corrs), "#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "F12", "=SUM(F6:F11)", sum(r["reefer_plug_2027"] for r in corrs), "#,##0.0", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "G12", "=SUM(G6:G11)", sum(r["rail_handoff_2027"] for r in corrs), "#,##0.0", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "H12", "=SUM(H6:H11)", sum(r["drayage_carrier_2027"] for r in corrs), "#,##0.0", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "I12", "=SUM(I6:I11)", sum(r["carrier_ctrl_cdays_2027"] for r in corrs), "#,##0.0", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "J12", "=SUM(J6:J11)", sum(r["gross_eur_2027"] for r in corrs), "#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "L12", "=SUM(L6:L11)", sum(r["avoidable_eur_2027"] for r in corrs), "#,##0.00", bold=True, fill=TOT_FILL)
    _set_formula(ws3, c3, "M12", "=L12/E12", sum(r["avoidable_eur_2027"] for r in corrs) / sum(r["budget_eur"] for r in corrs), "0.000", bold=True, fill=TOT_FILL)
    ws3.row_dimensions[12].height = 22
    _set_widths(ws3, [13, 14, 13, 13, 15, 14, 14, 14, 18, 17, 12, 18, 11, 11], freeze="A6")

    # Sheet 4: Validation_and_Routes
    ws4 = wb.create_sheet("Validation_and_Routes")
    ws4["A1"] = "Observable Two-Sided Physical Residual Validation and Alternative Route Comparison"
    ws4["A1"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEX)
    ws4["A2"] = "Lower observable residual error (fal_err) confirms both orthogonality to non-carrier drivers and preservation of genuine carrier sensitivity"
    ws4["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    hdrs4 = [
        "Method / Route", "Funded Slate", "WHV-OSN", "BHV-OSN", "HAM-HAN", "HAM-MAG", "BHV-HAN", "BHV-KAS",
        "C1 (2026)", "C2 (2026)", "C3 (2026)", "Observable Error (fal_err)",
    ]
    for ci, h in enumerate(hdrs4, start=1):
        ws4.cell(row=5, column=ci, value=h)
    _style_hdr(ws4, 5, len(hdrs4), height=30)

    route_order = [
        ("Golden (Joint S1+S2+S3)", "golden"),
        ("Direct TMS Stage Codes", "direct"),
        ("Rigorous Standard (Flat DC + Direct CHED)", "rigorous"),
        ("S1 Dropped Alone (No Chamber Pull-Back)", "S1_drop"),
        ("S2 Dropped Alone (No BIP Rail Model)", "S2_drop"),
        ("S3 Dropped Alone (No Depot Queue Model)", "S3_drop"),
        ("S1 Over-Corrected (Unnetted >=80%)", "S1_over"),
        ("S2 Over-Corrected (All BIP Shuttles <=48h)", "S2_over"),
        ("S3 Over-Corrected (Port-Aggregated Queue)", "S3_over"),
        ("S1 Shortcut: Binary >=92% Cut", "S1_one_fact"),
        ("S1 Shortcut: Symmetric Linear FE", "S1_sym_lin"),
        ("S2 Shortcut: Bivariate 24h OLS", "S2_one_fact"),
        ("S3 Shortcut: Unload-Day Portal Rejection", "S3_one_fact"),
        ("Cutoff Route (Binary Cuts All 3)", "cutoff"),
        ("Generous Route (Broad Over-Correction)", "generous"),
        ("Hedge Route (14% Uniform Haircut)", "hedge"),
    ]
    for idx, (label, rk) in enumerate(route_order):
        rr = 6 + idx
        rv = rt[rk]
        fill = FUND_FILL if rk == "golden" else (ZEBRA_FILL if idx % 2 == 1 else None)
        _set_val(ws4, f"A{rr}", label, bold=(rk == "golden"), fill=fill, align="left")
        _set_val(ws4, f"B{rr}", ", ".join(rv["funded_slate"]), bold=(rk == "golden"), fill=fill, align="left")
        for col_i, cn in enumerate(("WHV-OSN", "BHV-OSN", "HAM-HAN", "HAM-MAG", "BHV-HAN", "BHV-KAS"), start=3):
            col_l = chr(64 + col_i)
            _set_val(ws4, f"{col_l}{rr}", rv["bcrs"][cn], "0.000", bold=(rk == "golden"), fill=fill)
        _set_val(ws4, f"I{rr}", rv["C1_coldstore_pullback_2026"], "#,##0.0", fill=fill)
        _set_val(ws4, f"J{rr}", rv["C2_phyto_rail_roll_2026"], "#,##0.0", fill=fill)
        _set_val(ws4, f"K{rr}", rv["C3_depot_backlog_2026"], "#,##0.0", fill=fill)
        _set_val(ws4, f"L{rr}", rv["fal_err"], "#,##0.0", bold=(rk == "golden"), fill=fill)
        ws4.row_dimensions[rr].height = 19

    # Key observable physical diagnostics block
    ws4["A24"] = "Key Observable Physical Diagnostics (Shipped 2026 Logs)"
    ws4["A24"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    diag_rows = [
        ("Whole-DC Aggregate Daily Utilization Range (%)", f"{diag['s1_dc_total_util_min_pct']:.1f}% - {diag['s1_dc_total_util_max_pct']:.1f}%", "Flat across all 4 DCs despite severe single-chamber peaks"),
        ("S1 Raw Filling-vs-Draining Yard Hold Gap [84-94%] (hours)", f"{diag['s1_raw_asym_gap_h']:.2f} h", "Collapses to 0.08 h after asymmetric chamber separation"),
        ("S2 Empirical Terminal Rail Booking-Lock Cutoffs (hours)", f"BHV {diag['s2_emp_port_cuts_h']['BHV']:.0f}h / HAM {diag['s2_emp_port_cuts_h']['HAM']:.0f}h / WHV {diag['s2_emp_port_cuts_h']['WHV']:.0f}h", "Mean BIP pass-through slope 0.687 controlling for consist & loco cuts"),
        ("S3 Raw Open-Portal Drain-Tail Drayage Gap (hours)", f"{diag['s3_raw_open_drain_gap_h']:.2f} h", "Collapses to 0.28 h; 45.4% of depot backlog falls on open portal days"),
    ]
    for i_d, (dm, dv, dn) in enumerate(diag_rows):
        r_d = 25 + i_d
        _set_val(ws4, f"A{r_d}", dm, fill=PARAM_FILL, align="left")
        _set_val(ws4, f"B{r_d}", dv, bold=True, fill=PARAM_FILL, align="center")
        _set_val(ws4, f"C{r_d}", dn, fill=PARAM_FILL, align="left")
    _set_widths(ws4, [38, 28, 10, 10, 10, 10, 10, 10, 11, 11, 11, 20], freeze="A6")

    # Sheet 5: Robustness_and_Forcing
    ws5 = wb.create_sheet("Robustness_and_Forcing")
    c5 = cache.setdefault("xl/worksheets/sheet5.xml", {})
    ws5["A1"] = "21-Variant Specification Robustness Battery & 8 +/-15% Forcing Stress Tests"
    ws5["A1"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEX)
    ws5["A2"] = "Every honest modeling variant (21/21) and every +/-15% parameter stress (8/8) selects the identical funding slate: WHV-OSN, BHV-OSN, HAM-HAN"
    ws5["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

    hdrs5 = ["Specification Variant", "Funded Slate", "WHV-OSN", "BHV-OSN", "HAM-HAN", "HAM-MAG", "BHV-HAN", "BHV-KAS", "C1 (2026)", "C2 (2026)", "C3 (2026)"]
    for ci, h in enumerate(hdrs5, start=1):
        ws5.cell(row=5, column=ci, value=h)
    _style_hdr(ws5, 5, len(hdrs5), height=30)

    v_list = fig["variants"]
    for idx, v in enumerate(v_list):
        rr = 6 + idx
        fill = ZEBRA_FILL if idx % 2 == 1 else None
        _set_val(ws5, f"A{rr}", v["name"], fill=fill, align="left")
        _set_val(ws5, f"B{rr}", ", ".join(v["funded_slate"]), fill=FUND_FILL, align="center")
        for col_i, cn in enumerate(("WHV-OSN", "BHV-OSN", "HAM-HAN", "HAM-MAG", "BHV-HAN", "BHV-KAS"), start=3):
            col_l = chr(64 + col_i)
            _set_val(ws5, f"{col_l}{rr}", v["bcrs"][cn], "0.000", fill=fill)
        _set_val(ws5, f"I{rr}", v["C1_coldstore_pullback_2026"], "#,##0.0", fill=fill)
        _set_val(ws5, f"J{rr}", v["C2_phyto_rail_roll_2026"], "#,##0.0", fill=fill)
        _set_val(ws5, f"K{rr}", v["C3_depot_backlog_2026"], "#,##0.0", fill=fill)
        ws5.row_dimensions[rr].height = 19

    # Min / Max summary rows with LIVE Excel formulas
    r_min, r_max = 6 + len(v_list), 7 + len(v_list)
    _set_val(ws5, f"A{r_min}", "21-Variant Minimum", bold=True, fill=TOT_FILL, align="left")
    _set_val(ws5, f"B{r_min}", "0/21 Flips", bold=True, fill=FUND_FILL, align="center")
    _set_val(ws5, f"A{r_max}", "21-Variant Maximum", bold=True, fill=TOT_FILL, align="left")
    _set_val(ws5, f"B{r_max}", "100% Hold", bold=True, fill=FUND_FILL, align="center")
    for col_i, cn in enumerate(("WHV-OSN", "BHV-OSN", "HAM-HAN", "HAM-MAG", "BHV-HAN", "BHV-KAS"), start=3):
        col_l = chr(64 + col_i)
        vals = [v["bcrs"][cn] for v in v_list]
        _set_formula(ws5, c5, f"{col_l}{r_min}", f"=MIN({col_l}6:{col_l}{r_min-1})", min(vals), "0.000", bold=True, fill=TOT_FILL)
        _set_formula(ws5, c5, f"{col_l}{r_max}", f"=MAX({col_l}6:{col_l}{r_min-1})", max(vals), "0.000", bold=True, fill=TOT_FILL)
    for col_l, ck in (("I", "C1_coldstore_pullback_2026"), ("J", "C2_phyto_rail_roll_2026"), ("K", "C3_depot_backlog_2026")):
        vals = [v[ck] for v in v_list]
        _set_formula(ws5, c5, f"{col_l}{r_min}", f"=MIN({col_l}6:{col_l}{r_min-1})", min(vals), "#,##0.0", bold=True, fill=TOT_FILL)
        _set_formula(ws5, c5, f"{col_l}{r_max}", f"=MAX({col_l}6:{col_l}{r_min-1})", max(vals), "#,##0.0", bold=True, fill=TOT_FILL)

    # Forcing +/-15% Stress Table
    r_st = r_max + 2
    ws5[f"A{r_st}"] = "+/-15% Parameter Forcing Stress Tests (All 8/8 Hold Identical Slate)"
    ws5[f"A{r_st}"].font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEX)
    for idx, p in enumerate(fig["perturbations"]):
        rr = r_st + 1 + idx
        _set_val(ws5, f"A{rr}", f"Stress: {p['input']}", fill=PARAM_FILL, align="left")
        _set_val(ws5, f"B{rr}", ", ".join(p["answer"]), fill=FUND_FILL, align="center")
        for col_i, cn in enumerate(("WHV-OSN", "BHV-OSN", "HAM-HAN", "HAM-MAG", "BHV-HAN", "BHV-KAS"), start=3):
            col_l = chr(64 + col_i)
            _set_val(ws5, f"{col_l}{rr}", p["bcrs"][cn], "0.000", fill=PARAM_FILL)
    _set_widths(ws5, [28, 28, 10, 10, 10, 10, 10, 10, 12, 12, 12], freeze="A6")

    wb.save(path)
    _inject_formula_cache(path, cache)
    return path


# ------------------------------------------------------------------
# 3. Matplotlib Charts + 10-Slide Executive PPTX
# ------------------------------------------------------------------
def _make_charts(fig):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#C4CDD8",
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "grid.color": "#E6ECF2",
        "grid.linestyle": "--",
        "grid.alpha": 0.8,
    })
    corrs = fig["corridors"]
    rt = fig["routes"]
    bands = fig["bands"]
    charts = {}

    # Chart 1: Ranking Reversal (Golden BCR vs Naive TMS BCR)
    fig1, ax1 = plt.subplots(figsize=(7.6, 4.1), dpi=200)
    names = [r["corridor_id"] for r in corrs][::-1]
    g_vals = [r["bcr_2027"] for r in corrs][::-1]
    n_vals = [rt["direct"]["bcrs"][nm] for nm in names]
    y = np.arange(len(names))
    h = 0.36
    ax1.barh(y + h / 2, g_vals, height=h, color=["#B85D43" if v < 1.0 else "#1B365D" for v in g_vals], label="Attributed Golden 2027 BCR")
    ax1.barh(y - h / 2, n_vals, height=h, color="#A8B8CC", alpha=0.85, label="Naive TMS Stage BCR (Unseparated)")
    ax1.axvline(1.045, color="#2D7D59", linestyle="--", linewidth=1.4, label="Top-3 Budget Cap Cutoff (1.045)")
    for idx, (gv, nv) in enumerate(zip(g_vals, n_vals)):
        ax1.text(gv + 0.03, idx + h / 2, f"{gv:.3f}", va="center", fontsize=8.5, fontweight="bold", color="#1B365D")
        ax1.text(nv + 0.03, idx - h / 2, f"{nv:.2f}", va="center", fontsize=8, color="#556677")
    ax1.set_yticks(y)
    ax1.set_yticklabels(names, fontsize=9.5, fontweight="bold")
    ax1.set_xlim(0, 2.55)
    ax1.set_ylim(-0.6, 6.75)
    ax1.set_xlabel("Projected 2027 Benefit-Cost Ratio (EUR Avoidable / EUR Budget)", fontsize=9)
    ax1.set_title("Complete 3-for-3 Ranking Reversal After Removing Non-Carrier Delays", fontsize=10.5, fontweight="bold", color="#1B365D")
    ax1.legend(loc="upper center", ncol=2, fontsize=7.6, framealpha=0.95)
    fig1.tight_layout()
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png", dpi=200)
    plt.close(fig1)
    charts["reversal"] = buf1.getvalue()

    # Chart 2: 2026 Non-Carrier Deductions by Corridor (Stacked C1, C2, C3 vs Remaining Carrier-Ctrl)
    fig2, ax2 = plt.subplots(figsize=(7.6, 4.1), dpi=200)
    c_names = [r["corridor_id"] for r in corrs]
    c1_v = np.array([r["c1_coldstore_pullback_2026"] for r in corrs])
    c2_v = np.array([r["c2_phyto_rail_roll_2026"] for r in corrs])
    c3_v = np.array([r["c3_depot_backlog_2026"] for r in corrs])
    cc_v = np.array([r["carrier_ctrl_cdays_2026"] for r in corrs])
    x = np.arange(len(c_names))
    ax2.bar(x, cc_v, width=0.56, color="#1B365D", label="Carrier-Controllable 2026")
    ax2.bar(x, c1_v, width=0.56, bottom=cc_v, color="#D4764E", label="C1: Cold-Store Pull-Back (7,437)")
    ax2.bar(x, c2_v, width=0.56, bottom=cc_v + c1_v, color="#5C8AB8", label="C2: BIP Rail Rollover (4,304)")
    ax2.bar(x, c3_v, width=0.56, bottom=cc_v + c1_v + c2_v, color="#7AA68A", label="C3: Depot Portal Backlog (7,172)")
    for i_x in range(len(c_names)):
        tot_h = cc_v[i_x] + c1_v[i_x] + c2_v[i_x] + c3_v[i_x]
        ax2.text(i_x, tot_h + 140, f"{cc_v[i_x]:,.0f} carr.", ha="center", fontsize=8, fontweight="bold", color="#1B365D")
    ax2.set_xticks(x)
    ax2.set_xticklabels(c_names, fontsize=9, fontweight="bold")
    ax2.set_ylabel("2026 Excess Container-Days (Stages 3, 5, 7)", fontsize=9)
    ax2.set_title("2026 TMS Stage Totals Decomposed into Carrier vs Non-Carrier Drivers", fontsize=10.5, fontweight="bold", color="#1B365D", pad=10)
    ax2.set_ylim(0, max(cc_v + c1_v + c2_v + c3_v) * 1.34)
    ax2.legend(loc="upper center", ncol=2, fontsize=7.6, framealpha=0.95)
    fig2.tight_layout()
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png", dpi=200)
    plt.close(fig2)
    charts["bridge"] = buf2.getvalue()

    # Chart 3: Observable Residual Orthogonality Error (Golden vs Rivals)
    fig3, ax3 = plt.subplots(figsize=(7.4, 3.8), dpi=200)
    r_labels = [
        "Golden (Joint S1+S2+S3)", "S1 Shortcut (>=92%)", "S2 Shortcut (24h OLS)",
        "S3 Shortcut (Binary Rej.)", "Generous Over-Corr.", "Hedge (14% Cut)",
        "Rigorous Baseline", "Direct TMS", "Cutoff (All 3 Binary)",
    ]
    r_keys = ["golden", "S1_one_fact", "S2_one_fact", "S3_one_fact", "generous", "hedge", "rigorous", "direct", "cutoff"]
    errs = [rt[k]["fal_err"] for k in r_keys]
    y3 = np.arange(len(r_labels))[::-1]
    cols3 = ["#2D7D59"] + ["#B85D43"] * (len(r_labels) - 1)
    ax3.barh(y3, errs, height=0.62, color=cols3)
    for yp, ev in zip(y3, errs):
        ax3.text(ev + 25, yp, f"{ev:,.1f}", va="center", fontsize=8.3, fontweight="bold" if ev < 100 else "normal")
    ax3.set_yticks(y3)
    ax3.set_yticklabels(r_labels, fontsize=8.5)
    ax3.set_xlim(0, max(errs) * 1.16)
    ax3.set_xlabel("Two-Sided Observable Residual Error (Lower = Better Physical Fit)", fontsize=8.8)
    ax3.set_title("Observable Residual Diagnostics Reject Every Shortcut & Over-Correction", fontsize=10.2, fontweight="bold", color="#1B365D")
    fig3.tight_layout()
    buf3 = io.BytesIO()
    fig3.savefig(buf3, format="png", dpi=200)
    plt.close(fig3)
    charts["validation"] = buf3.getvalue()

    # Chart 4: 21-Variant Band Stability Across All 6 Corridors
    fig4, ax4 = plt.subplots(figsize=(7.4, 3.9), dpi=200)
    v_list = fig["variants"]
    x4 = np.arange(len(corrs))
    for i_c, r in enumerate(corrs):
        cn = r["corridor_id"]
        vals = [v["bcrs"][cn] for v in v_list]
        lo, hi = min(vals), max(vals)
        col = "#1B365D" if r["decision"] == "FUND" else "#B85D43"
        ax4.plot([i_c, i_c], [lo, hi], color=col, linewidth=5.5, alpha=0.38)
        ax4.scatter([i_c], [r["bcr_2027"]], color=col, s=65, zorder=5)
        if r["decision"] == "FUND":
            ax4.text(i_c, hi + 0.012, f"{r['bcr_2027']:.3f}\n[{lo:.2f}-{hi:.2f}]", ha="center", va="bottom", fontsize=7.8, fontweight="bold", color=col)
        else:
            ax4.text(i_c, lo - 0.014, f"{r['bcr_2027']:.3f}\n[{lo:.2f}-{hi:.2f}]", ha="center", va="top", fontsize=7.8, fontweight="bold", color=col)
    ax4.axhline(1.055, color="#2D7D59", linestyle="--", linewidth=1.4, label="Funding Cutoff (Zero Overlap Between #3 and #4)")
    ax4.set_xticks(x4)
    ax4.set_xticklabels([r["corridor_id"] for r in corrs], fontsize=9.2, fontweight="bold")
    ax4.set_ylim(0.81, 1.24)
    ax4.set_ylabel("Projected 2027 Corridor BCR", fontsize=9)
    ax4.set_title("21 Honest Specifications Hold Identical Top-3 Slate with Wide Margin", fontsize=10.2, fontweight="bold", color="#1B365D")
    ax4.legend(loc="lower left", fontsize=8.0, framealpha=0.95)
    fig4.tight_layout()
    buf4 = io.BytesIO()
    fig4.savefig(buf4, format="png", dpi=200)
    plt.close(fig4)
    charts["robustness"] = buf4.getvalue()

    return charts


def write_pptx(out_dir, fig):
    path = os.path.join(out_dir, GOLDEN_FILES["pptx"])
    charts = _make_charts(fig)
    corrs = fig["corridors"]
    diag = fig["diagnostics"]
    bands = fig["bands"]
    rt = fig["routes"]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    C_NAVY = RGBColor(0x1B, 0x36, 0x5D)
    C_SLATE = RGBColor(0x3B, 0x53, 0x73)
    C_GREEN = RGBColor(0x2D, 0x7D, 0x59)
    C_TERRA = RGBColor(0xB8, 0x5D, 0x43)
    C_BG = RGBColor(0xF6, 0xF8, 0xFB)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    C_TEXT = RGBColor(0x1E, 0x24, 0x2B)
    C_MUTED = RGBColor(0x5A, 0x67, 0x75)

    def _chrome(slide, title, subtitle, page_no):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_WHITE
        bg.line.fill.background()

        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.14))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_NAVY
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.28), Inches(12.2), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(18.5)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = "Calibri"
        p2.font.size = Pt(11.0)
        p2.font.color.rgb = C_MUTED

        ft = slide.shapes.add_textbox(Inches(0.55), Inches(7.08), Inches(12.2), Inches(0.32))
        ftf = ft.text_frame
        fp = ftf.paragraphs[0]
        fp.text = f"Weserfrucht Import GmbH  |  Charter RC-2027 (Rev 3) Carrier Remediation Committee  |  Slide {page_no} of 10"
        fp.font.name = "Calibri"
        fp.font.size = Pt(9)
        fp.font.color.rgb = C_MUTED

    def _card(slide, left, top, width, height, heading, big_val, note, accent=C_NAVY):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BG
        box.line.color.rgb = RGBColor(0xD5, 0xDE, 0xE8)
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.08), Inches(height))
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent
        strip.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.18), Inches(top + 0.10), Inches(width - 0.28), Inches(height - 0.18))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = heading
        p0.font.name = "Calibri"
        p0.font.size = Pt(10.0)
        p0.font.bold = True
        p0.font.color.rgb = C_SLATE
        p1 = tf.add_paragraph()
        p1.text = big_val
        p1.font.name = "Calibri"
        p1.font.size = Pt(18.0)
        p1.font.bold = True
        p1.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = note
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
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
        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = "Calibri"
            p.font.size = Pt(10.8)
            p.font.color.rgb = C_TEXT
            p.space_after = Pt(6)

    def _add_table(slide, left, top, width, height, headers, rows_data, col_widths):
        shape = slide.shapes.add_table(len(rows_data) + 1, len(headers), Inches(left), Inches(top), Inches(width), Inches(height))
        tbl = shape.table
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = Inches(cw)
        for j, h in enumerate(headers):
            cell = tbl.cell(0, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY
            p = cell.text_frame.paragraphs[0]
            p.text = h
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.alignment = PP_ALIGN.CENTER
        for i, row in enumerate(rows_data):
            is_fund = (len(row) > 0 and row[-1] == "FUND")
            is_defer = (len(row) > 0 and row[-1] == "DEFER")
            bg_c = RGBColor(0xE2, 0xF2, 0xE8) if is_fund else (RGBColor(0xFA, 0xE6, 0xE1) if is_defer else (C_BG if i % 2 == 1 else C_WHITE))
            for j, val in enumerate(row):
                cell = tbl.cell(i + 1, j)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg_c
                p = cell.text_frame.paragraphs[0]
                p.text = str(val)
                p.font.name = "Calibri"
                p.font.size = Pt(9.3)
                p.font.bold = (j == 0 or j == len(row) - 1)
                p.font.color.rgb = C_GREEN if (j == len(row) - 1 and is_fund) else (C_TERRA if (j == len(row) - 1 and is_defer) else C_TEXT)
                p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER

    # ---- Slide 1: Cover ----
    s1 = prs.slides.add_slide(blank)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()
    accent1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.75), Inches(13.333), Inches(0.08))
    accent1.fill.solid()
    accent1.fill.fore_color.rgb = C_GREEN
    accent1.line.fill.background()
    t1 = s1.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(11.4), Inches(3.8))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "WESERFRUCHT IMPORT GMBH  |  SUPPLY CHAIN GOVERNANCE"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x9E, 0xC2, 0xE6)
    p2 = tf1.add_paragraph()
    p2.text = "2027 Carrier-Remediation Capital Allocation Review"
    p2.font.name = "Calibri"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(14)
    p3 = tf1.add_paragraph()
    p3.text = "EUR 1,750,000 Corridor Capital Deployment under Charter RC-2027 (Rev 3)"
    p3.font.name = "Calibri"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(0xD8, 0xE4, 0xF0)
    p3.space_before = Pt(10)
    t1b = s1.shapes.add_textbox(Inches(0.9), Inches(6.05), Inches(11.4), Inches(1.0))
    pb = t1b.text_frame.paragraphs[0]
    pb.text = f"Annual Carrier Remediation Committee  |  21 January 2027  |  Prepared by {PK.PEOPLE['analyst']} & Supply Chain Controlling"
    pb.font.name = "Calibri"
    pb.font.size = Pt(11.5)
    pb.font.color.rgb = RGBColor(0xBD, 0xCE, 0xDF)

    # ---- Slide 2: Executive Decision ----
    s2 = prs.slides.add_slide(blank)
    _chrome(s2, "Executive Recommendation: Fund WHV-OSN, BHV-OSN, and HAM-HAN",
            "Complete 3-for-3 reversal of naive TMS rankings after removing 18,912.8 non-carrier container-days across C1, C2, and C3", 2)
    _card(s2, 0.55, 1.32, 2.95, 1.45, "APPROVED 2027 SLATE", "3 Corridors", "WHV-OSN, BHV-OSN, HAM-HAN\n(Defer HAM-MAG, BHV-HAN, BHV-KAS)", C_GREEN)
    _card(s2, 3.68, 1.32, 2.95, 1.45, "CAPITAL DEPLOYED", f"EUR {fig['funded_budget_eur']/1e6:.3f}M", f"of EUR 1.750M cap (EUR {fig['unspent_budget_eur']:,.0f} reserve)\nMatches exact integer knapsack", C_NAVY)
    _card(s2, 6.81, 1.32, 2.95, 1.45, "AVOIDABLE 2027 D&D", f"EUR {fig['funded_avoidable_eur_2027']/1e6:.3f}M", f"Funded portfolio BCR: {fig['funded_portfolio_bcr']:.3f}\nAll 3 funded lanes > 1.08 BCR", C_GREEN)
    _card(s2, 9.94, 1.32, 2.85, 1.45, "NON-CARRIER REMOVED", "18,912.8 c-days", f"C1: {fig['C1_coldstore_pullback_2026']:,.1f} | C2: {fig['C2_phyto_rail_roll_2026']:,.1f}\nC3: {fig['C3_depot_backlog_2026']:,.1f} c-days", C_TERRA)

    tbl_rows = []
    for r in corrs:
        tbl_rows.append([
            f"#{r['rank']} {r['corridor_id']}",
            f"EUR {r['budget_eur']:,.0f}",
            f"{r['carrier_ctrl_cdays_2026']:,.1f}",
            f"{r['carrier_ctrl_cdays_2027']:,.1f}",
            f"EUR {r['avoidable_eur_2027']:,.0f}",
            f"{r['bcr_2027']:.3f}",
            f"{rt['direct']['bcrs'][r['corridor_id']]:.3f}",
            r["decision"],
        ])
    _add_table(
        s2, 0.55, 3.05, 12.24, 3.65,
        ["Corridor", "Budget", "2026 Carrier Days", "2027 Carrier Days", "2027 Avoidable EUR", "Golden BCR", "Naive TMS BCR", "Decision"],
        tbl_rows,
        [1.55, 1.45, 1.65, 1.65, 1.85, 1.35, 1.44, 1.30],
    )

    # ---- Slide 3: Ranking Reversal Chart ----
    s3 = prs.slides.add_slide(blank)
    _chrome(s3, "Why Raw TMS Stage Codes Fund the Exact Wrong Three Corridors",
            "Every naive top-3 corridor (BHV-KAS, HAM-MAG, BHV-HAN) falls below 1.00 BCR once non-carrier bottlenecks are removed", 3)
    s3.shapes.add_picture(io.BytesIO(charts["reversal"]), Inches(0.55), Inches(1.30), width=Inches(7.75))
    _bullets(s3, 8.50, 1.40, 4.30, 5.2, "Three Distinct False Alarms Cleared", [
        "BHV-KAS drops from naive #1 (2.176) to #6 (0.901): Kassel's filling-heavy thermal chambers drive internal yard pull-backs (S1), not port plug failures.",
        "HAM-MAG drops from naive #2 (2.136) to #4 (0.988): late EU BIP notices past Hamburg's ~26-28h rail lock inflate standby rail rolls (S2).",
        "BHV-HAN drops from naive #3 (2.012) to #5 (0.949): 96% exposure to quota-constrained LINE_A/B empty depots inflates drayage turnaround (S3).",
        "All three winners (WHV-OSN 1.139, BHV-OSN 1.100, HAM-HAN 1.086) exceed 1.08 BCR and hold unanimously across 21 specifications.",
    ])

    # ---- Slide 4: 2026 Attribution Bridge ----
    s4 = prs.slides.add_slide(blank)
    _chrome(s4, "2026 Attribution Bridge: Separating Carrier vs Non-Carrier Delays",
            "24,000 settled containers reconciled from 24,525 raw milestones, 179,359 pallet rows, 732 rail block trains, and 4,596 portal days", 4)
    s4.shapes.add_picture(io.BytesIO(charts["bridge"]), Inches(0.55), Inches(1.32), width=Inches(7.75))
    _bullets(s4, 8.50, 1.40, 4.30, 5.2, "Channel-Dominant Winner Structure", [
        "WHV-OSN (#1, BCR 1.139): genuine drayage carrier turnaround hub (73% unconstrained LINE_C/D); highest return per euro invested.",
        "BHV-OSN (#2, BCR 1.100): genuine Bremerhaven reefer-plug exposure; Osnabrueck chambers spend ~90% of high-load days draining rather than filling.",
        "HAM-HAN (#3, BCR 1.086): genuine Nordbahn short-consist & loco-derate bottleneck; early-notice BIP filings avoid Hamburg's booking lock.",
        f"Direct CHED rail sibling holds ({fig['phyto_sibling_rail_2026']:,.1f} c-days) are separately assigned to phyto_insp outside C2 ({fig['C2_phyto_rail_roll_2026']:,.1f} c-days of BIP standby rollovers).",
    ])

    # ---- Slide 5: S1 Evidence ----
    s5 = prs.slides.add_slide(blank)
    _chrome(s5, "Mechanism S1: Asymmetric Convex Cold-Store Chamber Pull-Back (C1 = 7,436.9 c-days)",
            "Whole-DC occupancy stays flat (70.7% to 77.6%), masking steep filling-regime thermal-chamber pull-backs at port yards", 5)
    _card(s5, 0.55, 1.35, 3.85, 1.45, "C1 ATTRIBUTION (2026)", f"{fig['C1_coldstore_pullback_2026']:,.1f} c-days", f"21-variant band: {bands['C1_coldstore_pullback_2026'][0]:,.1f} - {bands['C1_coldstore_pullback_2026'][1]:,.1f}\nOpens BHV-KAS (-0.944 BCR impact)", C_NAVY)
    _card(s5, 4.70, 1.35, 3.85, 1.45, "RAW FILL vs DRAIN GAP", f"+{diag['s1_raw_asym_gap_h']:.2f} hours", f"At 84-94% chamber occupancy\nResidual after S1: {diag['s1_resid_asym_gap_h']:.2f} h", C_GREEN)
    _card(s5, 8.85, 1.35, 3.90, 1.45, "WHOLE-DC OCCUPANCY", f"{diag['s1_dc_total_util_min_pct']:.1f}% - {diag['s1_dc_total_util_max_pct']:.1f}%", "Opposing Z02 summer & Z07 winter\npeaks offset by Z13 tropical buffer", C_TERRA)
    _bullets(s5, 0.60, 3.10, 12.1, 3.7, "Empirical Findings & Why Shortcuts Fail Both Sides", [
        "Reconstructing daily (DC, zone) closing stock from 175,207 deduplicated SKU pallet movements reconciles identically to whole-building stock while exposing individual chamber peaks above 95%.",
        "Within-vessel fixed-effects estimation confirms sharply convex hysteresis: filling chambers (net_flow > 0) throttle port yards ~7.5x more steeply than draining chambers (net_flow <= 0) at the identical occupancy.",
        "Under-correction fails: checking whole-DC occupancy yields ~0 pullback; a binary >=92% cut recovers only 4,460 c-days (-40%) and still mis-funds BHV-KAS; symmetric linear FE ignores hysteresis and still mis-funds BHV-KAS (1.217).",
        "Over-correction fails: subtracting all yard dwell above 80% chamber occupancy wipes genuine carrier plug congestion on draining-heavy BHV-OSN (crashing BHV-OSN BCR to 0.739).",
    ])

    # ---- Slide 6: S2 Evidence ----
    s6 = prs.slides.add_slide(blank)
    _chrome(s6, "Mechanism S2: Terminal-Varying BIP Locks vs Nordbahn Consist Cuts (C2 = 4,304.4 c-days)",
            "Joint shuttle-level separation of port-specific BIP booking locks from correlated peak-day locomotive and wagon shortfalls", 6)
    _card(s6, 0.55, 1.35, 3.85, 1.45, "C2 ATTRIBUTION (2026)", f"{fig['C2_phyto_rail_roll_2026']:,.1f} c-days", f"21-variant band: {bands['C2_phyto_rail_roll_2026'][0]:,.1f} - {bands['C2_phyto_rail_roll_2026'][1]:,.1f}\nOpens HAM-MAG (-0.732 BCR impact)", C_NAVY)
    _card(s6, 4.70, 1.35, 3.85, 1.45, "PORT LOCK CUTOFFS", f"BHV {diag['s2_emp_port_cuts_h']['BHV']:.0f}h | HAM {diag['s2_emp_port_cuts_h']['HAM']:.0f}h", f"WHV {diag['s2_emp_port_cuts_h']['WHV']:.0f}h (empirical smooth logistic)\nMean BIP pass-through: {diag['s2_bip_slope']:.2f}", C_GREEN)
    _card(s6, 8.85, 1.35, 3.90, 1.45, "SHORTCUT OVER-COUNT", f"{rt['S2_one_fact']['C2_phyto_rail_roll_2026']:,.1f} c-days", "Bivariate 24h OLS omits consist cuts\n(+59% bias; crashes HAM-HAN to 0.716)", C_TERRA)
    _bullets(s6, 0.60, 3.10, 12.1, 3.7, "Empirical Findings & Why Shortcuts Fail Both Sides", [
        "Across 732 every-3-day corridor block trains, BIP exam notice lead times span 1.5h to 72h continuously with terminal-specific booking locks: Hamburg (~26-28h), Bremerhaven (~14-16h), and Wilhelmshaven (~10-12h).",
        "Shared seasonal freight peaks create strong correlation between late BIP notices and genuine Nordbahn short-consist wagon cuts & BR-193 locomotive derates; joint multivariate modeling with Poisson-thinning posterior sharing isolates both effects cleanly.",
        "Under-correction fails: treating rail rollovers as pure carrier delay leaves HAM-MAG inflated at 1.720 BCR, displacing BHV-OSN.",
        "Over-correction & naive bivariate OLS fail: attributing entire BIP-present shuttles or regressing rollovers on fixed-24h BIP counts without controlling for consist_wagons_short and loco_derate crashes genuine rail bottleneck HAM-HAN (0.488 to 0.716).",
    ])

    # ---- Slide 7: S3 Evidence ----
    s7 = prs.slides.add_slide(blank)
    _chrome(s7, "Mechanism S3: Conserved Ocean-Line Empty-Depot Return Queues (C3 = 7,171.5 c-days)",
            "Multi-day unbooked empty-container backlogs persist across 5-7 open portal days after episodic LINE_A/B quota closures", 7)
    _card(s7, 0.55, 1.35, 3.85, 1.45, "C3 ATTRIBUTION (2026)", f"{fig['C3_depot_backlog_2026']:,.1f} c-days", f"21-variant band: {bands['C3_depot_backlog_2026'][0]:,.1f} - {bands['C3_depot_backlog_2026'][1]:,.1f}\nOpens BHV-HAN (-0.746 BCR impact)", C_NAVY)
    _card(s7, 4.70, 1.35, 3.85, 1.45, "OPEN-PORTAL DRAIN GAP", f"+{diag['s3_raw_open_drain_gap_h']:.2f} hours", f"On quota_closed_rejections = 0 days\nResidual after S3: {diag['s3_resid_open_drain_gap_h']:.2f} h", C_GREEN)
    _card(s7, 8.85, 1.35, 3.90, 1.45, "OPEN-DAY BACKLOG SHARE", f"{diag['s3_open_day_backlog_share_pct']:.1f}% of C3", "Occurs AFTER portal reopens\nBinary rejection flag misses half of C3", C_TERRA)
    _bullets(s7, 0.60, 3.10, 12.1, 3.7, "Empirical Findings & Why Shortcuts Fail Both Sides", [
        "Reconstructing daily unbooked empty stock per (port, shipping_line) via exact stock-flow conservation cumsum(daily_unloads - confirmed_bookings) normalized by mean daily unloads reveals multi-day drain tails long after portal reopening.",
        "Fixed-effects estimation (DC-week / DC-day / port-day / corr-week / harmonic / Huber) with proportional Gamma posterior sharing confirms backlog delay scales with corridor inland haul distance (128 to 268 km).",
        "Under-correction fails: flagging only binary unload-day portal_rejected > 0 recovers only 3,722.8 c-days (-48%) and leaves BHV-HAN mis-funded at 1.337 BCR.",
        "Over-correction fails: aggregating depot queues at port level (ignoring shipping-line isolation) contaminates unconstrained LINE_C/D boxes and wipes out genuine drayage leader WHV-OSN (crashing BCR from 1.139 to 0.596).",
    ])

    # ---- Slide 8: Validation ----
    s8 = prs.slides.add_slide(blank)
    _chrome(s8, "Two-Sided Observable Physical Validation Rules Out Every Alternative",
            "Joint S1+S2+S3 reduces observable residual error to 36.3 vs 300.9 to 1,725.4 across shortcuts, baselines, and over-corrections", 8)
    s8.shapes.add_picture(io.BytesIO(charts["validation"]), Inches(0.55), Inches(1.32), width=Inches(7.65))
    _bullets(s8, 8.40, 1.42, 4.40, 5.2, "Both Sides Verified on Shipped Logs", [
        "Non-carrier orthogonality passed: residual filling-vs-draining plug gap drops from 27.7h to 0.08h; open-portal drayage drain gap drops from 53.7h to 0.28h; cross-24h rail residual contrast vanishes.",
        "Carrier sensitivity preserved: genuine port reefer-rack utilization slope stays intact on high-chamber days, Nordbahn consist-shortfall slope stays intact on BIP shuttles, and unconstrained ocean-line drayage stays intact.",
        "All 7 lattice drops produce 7 distinct wrong slates; generous, hedge, cutoff, and all 5 partial shortcuts fail validation by 8x to 48x.",
    ])

    # ---- Slide 9: Robustness & Forcing ----
    s9 = prs.slides.add_slide(blank)
    _chrome(s9, "Specification Robustness (21/21 Variants) & +/-15% Forcing Stability (8/8 Hold)",
            "Wide 0.098 BCR separation between #3 HAM-HAN (1.086) and #4 HAM-MAG (0.988) locks the funding slate", 9)
    s9.shapes.add_picture(io.BytesIO(charts["robustness"]), Inches(0.55), Inches(1.32), width=Inches(7.65))
    _bullets(s9, 8.40, 1.42, 4.40, 5.2, "Zero Flips Across All Defensible Models", [
        "21 honest variants tested across functional forms (quadratic, spline, binned, Huber, Poisson IRLS, hard step, harmonic, distance-parametric) and FE groupings: 21/21 select WHV-OSN, BHV-OSN, HAM-HAN.",
        "All 8 independent +/-15% parameter stress tests (S1, S2, S3, and baseline 2027 volume growth) hold the exact same 3-corridor slate.",
        "Greedy BCR ranking equals the exact integer knapsack optimum (EUR 1,705,000 <= EUR 1,750,000 cap; any 4 corridors require >= EUR 2,255,000).",
    ])

    # ---- Slide 10: Implementation & Governance ----
    s10 = prs.slides.add_slide(blank)
    _chrome(s10, "2027 Execution Plan: Carrier Remediation Capital & Non-Carrier Tracks",
            "Commit EUR 1,705,000 across three funded corridors by 19 Feb 2027 while routing C1, C2, and C3 to dedicated governance tracks", 10)
    plan_rows = [
        ["WHV-OSN", "EUR 560,000", "1.139", "Dedicated A29 reefer chassis pool + driver SLA commitment", "FUND"],
        ["BHV-OSN", "EUR 560,000", "1.100", "Bremerhaven priority reefer-plug rack allocation & crane gate SLA", "FUND"],
        ["HAM-HAN", "EUR 585,000", "1.086", "Nordbahn backup BR-193 traction & minimum wagon consist guarantee", "FUND"],
        ["HAM-MAG", "EUR 565,000", "0.988", "Defer capex; advance pre-arrival CHED filing ahead of HAM 26-28h lock", "DEFER"],
        ["BHV-HAN", "EUR 575,000", "0.949", "Defer capex; negotiate LINE_A/B minimum daily empty-depot booking quotas", "DEFER"],
        ["BHV-KAS", "EUR 570,000", "0.901", "Defer capex; smooth Kassel Z02/Z07 intake & lease peak overflow bays", "DEFER"],
    ]
    _add_table(
        s10, 0.55, 1.35, 12.24, 3.35,
        ["Corridor", "Budget", "2027 BCR", "2027 Primary Operational Action", "Decision"],
        plan_rows,
        [1.35, 1.45, 1.15, 7.04, 1.25],
    )
    _bullets(s10, 0.60, 5.00, 12.1, 1.9, "Committee Sign-Off & Q1-Q3 2027 Governance Gates", [
        "Approve EUR 1,705,000 deployment (retaining EUR 45,000 contingency reserve) and load weserfrucht_corridor_allocation_2027.csv into the governance tracker.",
        "Execute carrier SLA addenda by 19 Feb 2027; run pre-berry Z02/Z07 readiness audit on 15 May 2027 and pre-Q3 BCR tracking gate on 30 Jun 2027.",
    ])

    prs.save(path)
    return path


def build_all(fig=None):
    if fig is None:
        fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    gdir = os.path.join(TASK_DIR, "golden")
    if os.path.isdir(gdir):
        shutil.rmtree(gdir)
    os.makedirs(gdir)

    csv_p = write_csv(gdir, fig)
    xlsx_p = write_xlsx(gdir, fig)
    pptx_p = write_pptx(gdir, fig)

    # Normalize golden Office containers with realistic post-as_of analyst timestamps
    postprocess.normalize_ooxml(
        xlsx_p,
        PK.PEOPLE["analyst"],
        PK.PEOPLE["controlling"],
        "2027-01-20T09:12:00Z",
        "2027-01-21T14:28:15Z",
        excel=True,
        company=PK.ORG,
    )
    postprocess.normalize_pptx(
        pptx_p,
        PK.PEOPLE["analyst"],
        PK.PEOPLE["procurement"],
        "2027-01-20T13:45:00Z",
        "2027-01-21T16:04:42Z",
        "Weserfrucht 2027 Carrier-Remediation Capital Allocation Review",
        PK.ORG,
    )
    postprocess.own_mtimes(gdir, {
        GOLDEN_FILES["csv"]:  dt.datetime(2027, 1, 21, 14, 15, 22, tzinfo=UTC),
        GOLDEN_FILES["xlsx"]: dt.datetime(2027, 1, 21, 14, 28, 15, tzinfo=UTC),
        GOLDEN_FILES["pptx"]: dt.datetime(2027, 1, 21, 16,  4, 42, tzinfo=UTC),
    })

    # Cut deterministic target.zip and golden.zip
    tzip = os.path.join(TASK_DIR, "target.zip")
    gzip = os.path.join(TASK_DIR, "golden.zip")
    postprocess.zip_folder(os.path.join(TASK_DIR, "target"), tzip, zone="Europe/Berlin")
    postprocess.zip_folder(gdir, gzip, zone="Europe/Berlin")
    return {"csv": csv_p, "xlsx": xlsx_p, "pptx": pptx_p, "target_zip": tzip, "golden_zip": gzip}


if __name__ == "__main__":
    out = build_all()
    for k, p in out.items():
        print(f"{k:12s} {os.path.getsize(p):10d}  {p}")
