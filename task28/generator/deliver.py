#!/usr/bin/env python3
"""task28/generator/deliver.py (v2): Build the two requested golden deliverables in task28/golden/
and cut target.zip and golden.zip:
  1. golden/barlavento_swro_overhaul_plan_2027.xlsx (7 formula-driven tabs, styled, chart, postprocess scrubbed)
  2. golden/barlavento_train_diagnostics_2027.csv (exact SWRO-Q27 Annex B 8-column schema)

Every graded figure is computed live from analysis.run_all(target_dir); zero hardcoded totals.
"""
import csv
import datetime as dt
import os
import shutil
import sys

import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.drawing.text import CharacterProperties, ParagraphProperties
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(
    os.path.dirname(os.path.dirname(HERE)),
    ".agents",
    "skills",
    "reduce-house-fixes",
    "scripts",
    "writers",
)
sys.path.insert(0, HERE)
sys.path.insert(0, WRITERS)
import analysis as AN  # noqa: E402
import core  # noqa: E402
import pack as PK  # noqa: E402
import postprocess  # noqa: E402

UTC = dt.timezone.utc
GOLDEN_XLSX = "barlavento_swro_overhaul_plan_2027.xlsx"
GOLDEN_CSV = "barlavento_train_diagnostics_2027.csv"


def _styles():
    thin = Side(style="thin", color="CBD5E1")
    med_bot = Side(style="medium", color="163A5F")
    dbl_bot = Side(style="double", color="163A5F")
    return {
        "title_font": Font(name="Calibri", size=14, bold=True, color="163A5F"),
        "sub_font": Font(name="Calibri", size=10, italic=True, color="475569"),
        "sec_font": Font(name="Calibri", size=11, bold=True, color="163A5F"),
        "hdr_font": Font(name="Calibri", size=10, bold=True, color="FFFFFF"),
        "body_font": Font(name="Calibri", size=10, color="1E293B"),
        "bold_font": Font(name="Calibri", size=10, bold=True, color="0F172A"),
        "note_font": Font(name="Calibri", size=9, italic=True, color="475569"),
        "ov_font": Font(name="Calibri", size=10, bold=True, color="9A3412"),
        "mo_font": Font(name="Calibri", size=10, bold=True, color="166534"),
        "hdr_fill": PatternFill("solid", fgColor="163A5F"),
        "subhdr_fill": PatternFill("solid", fgColor="2B5B84"),
        "zebra_fill": PatternFill("solid", fgColor="F8FAFC"),
        "tot_fill": PatternFill("solid", fgColor="E2EDF7"),
        "call_fill": PatternFill("solid", fgColor="EDF4FA"),
        "ov_fill": PatternFill("solid", fgColor="FFEDD5"),
        "mo_fill": PatternFill("solid", fgColor="DCFCE7"),
        "border": Border(left=thin, right=thin, top=thin, bottom=thin),
        "tot_border": Border(left=thin, right=thin, top=Side(style="thin", color="163A5F"), bottom=dbl_bot),
        "hdr_border": Border(left=thin, right=thin, top=thin, bottom=med_bot),
    }


def _style_header_row(ws, row_idx, n_cols, S, fill_key="hdr_fill"):
    for c in range(1, n_cols + 1):
        cell = ws.cell(row=row_idx, column=c)
        cell.fill = S[fill_key]
        cell.font = S["hdr_font"]
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = S["hdr_border"]
    ws.row_dimensions[row_idx].height = 28


def _set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def _setup_print(ws, max_col, max_row, repeat_row=None):
    ws.views.sheetView[0].showGridLines = True
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_area = f"A1:{get_column_letter(max_col)}{max_row}"
    if repeat_row:
        ws.print_title_rows = f"{repeat_row}:{repeat_row}"


def write_csv(golden_dir, res):
    ordered = sorted(core.TRAINS, key=lambda u: res["train_rows"][u]["total_2027_h"], reverse=True)
    path = os.path.join(golden_dir, GOLDEN_CSV)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "train_id",
                "boron_2027_h",
                "scaling_2027_h",
                "struct_2027_h",
                "total_2027_h",
                "q3_2027_h",
                "energy_2027_mwh",
                "designation",
            ]
        )
        for u in ordered:
            tr = res["train_rows"][u]
            w.writerow(
                [
                    u,
                    f"{tr['boron_2027_h']:.1f}",
                    f"{tr['scaling_2027_h']:.1f}",
                    f"{tr['struct_2027_h']:.1f}",
                    f"{tr['total_2027_h']:.1f}",
                    f"{tr['q3_2027_h']:.1f}",
                    f"{tr['energy_2027_mwh']:.2f}",
                    tr["designation"],
                ]
            )
    return path, ordered


def write_workbook(golden_dir, res, ordered_trains):
    wb = openpyxl.Workbook()
    S = _styles()

    ws_exec = wb.active
    ws_exec.title = "Overhaul_Triage_2027"
    ws_s1 = wb.create_sheet("S1_Boron_Flux_Support")
    ws_s2 = wb.create_sheet("S2_TwoPath_Hydraulics")
    ws_s3 = wb.create_sheet("S3_DualCIP_LCA")
    ws_fal = wb.create_sheet("Falsification_And_Routes")
    ws_plan = wb.create_sheet("Operating_Plan_2027")
    ws_sens = wb.create_sheet("Sensitivity_And_QA_2026")

    # ==========================================================================
    # TAB 6: Operating_Plan_2027 (built first so Overhaul_Triage_2027 links to it)
    # ==========================================================================
    ws_plan["A1"] = "Barlavento SWRO 2026-to-2027 Quarterly Failure-Mode Forecast (Protocol SWRO-Q27 Annex A)"
    ws_plan["A1"].font = S["title_font"]
    ws_plan["A2"] = "Uniform Annex A quarterly multipliers from operating_plan_2027.csv applied to estimated 2026 physical mode hours."
    ws_plan["A2"].font = S["sub_font"]

    plan_hdrs = [
        "Train",
        "Quarter",
        "2026 Boron (h)",
        "2026 Scaling (h)",
        "2026 Struct (h)",
        "Duty Ratio",
        "Boron Temp Mult",
        "Scaling Rec Mult",
        "2027 Boron (h)",
        "2027 Scaling (h)",
        "2027 Struct (h)",
        "2027 Total (h)",
        "2027 Energy Penalty (MWh)",
    ]
    ws_plan.append([])
    ws_plan.append(plan_hdrs)  # row 4
    _style_header_row(ws_plan, 4, len(plan_hdrs), S)

    q_names = ["2027-Q1", "2027-Q2", "2027-Q3", "2027-Q4"]
    plan_row = 5
    for u in core.TRAINS:
        tr = res["train_rows"][u]
        sr = res["plan"]["sched_ratio"][u]
        for q in range(4):
            r = plan_row
            ws_plan.cell(r, 1, u)
            ws_plan.cell(r, 2, q_names[q])
            ws_plan.cell(r, 3, round(tr["boron_2026_q"][q], 6))
            ws_plan.cell(r, 4, round(tr["scaling_2026_q"][q], 6))
            ws_plan.cell(r, 5, round(tr["struct_2026_q"][q], 6))
            ws_plan.cell(r, 6, sr[q])
            ws_plan.cell(r, 7, res["plan"]["boron_temp_q"][q])
            ws_plan.cell(r, 8, res["plan"]["scaling_rec_q"][q])
            ws_plan.cell(r, 9, f"=C{r}*G{r}*F{r}")
            ws_plan.cell(r, 10, f"=D{r}*H{r}*F{r}")
            ws_plan.cell(r, 11, f"=E{r}*F{r}")
            ws_plan.cell(r, 12, f"=SUM(I{r}:K{r})")
            ws_plan.cell(
                r,
                13,
                f"=(I{r}*{int(core.ENERGY_BORON_KWH)}+J{r}*{int(core.ENERGY_SCALING_KWH)}+K{r}*{int(core.ENERGY_STRUCT_KWH)})/1000",
            )
            for c in range(1, len(plan_hdrs) + 1):
                cell = ws_plan.cell(r, c)
                cell.font = S["body_font"]
                cell.border = S["border"]
                if r % 2 == 0:
                    cell.fill = S["zebra_fill"]
                if c <= 2:
                    cell.alignment = Alignment(horizontal="center")
                elif c in (6, 7, 8):
                    cell.number_format = "0.00"
                    cell.alignment = Alignment(horizontal="right")
                elif c == 13:
                    cell.number_format = "#,##0.00"
                    cell.alignment = Alignment(horizontal="right")
                else:
                    cell.number_format = "#,##0.0"
                    cell.alignment = Alignment(horizontal="right")
            plan_row += 1

    # Row 37 totals
    tot_p = plan_row
    ws_plan.cell(tot_p, 1, "Plant Total")
    ws_plan.cell(tot_p, 2, "All 4 Qtrs")
    for c in (3, 4, 5, 9, 10, 11, 12, 13):
        col_l = get_column_letter(c)
        ws_plan.cell(tot_p, c, f"=SUM({col_l}5:{col_l}{tot_p - 1})")
    for c in range(1, len(plan_hdrs) + 1):
        cell = ws_plan.cell(tot_p, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c == 13:
            cell.number_format = "#,##0.00"
        elif c in (3, 4, 5, 9, 10, 11, 12):
            cell.number_format = "#,##0.0"
    ws_plan.freeze_panes = "C5"
    _set_widths(ws_plan, [11, 12, 14, 15, 14, 12, 15, 15, 14, 15, 14, 14, 20])
    _setup_print(ws_plan, len(plan_hdrs), tot_p, repeat_row=4)

    # ==========================================================================
    # TAB 1: Overhaul_Triage_2027 (Executive summary + live formulas + bar chart)
    # ==========================================================================
    n_var = len(res["variants_named"])
    ws_exec["A1"] = "Barlavento SWRO 2027 Vessel Overhaul Diagnostics: Pull TR07, TR06, TR02, and TR01 (>= 400 h)"
    ws_exec["A1"].font = S["title_font"]
    ws_exec["A2"] = (
        f"Estacao Dessalinizadora de Alvor | Engineering Protocol SWRO-Q27 Membrane Reliability Diagnostics | "
        f"Prepared by {PK.PEOPLE['lead']} | Archive As-Of {PK.AS_OF}"
    )
    ws_exec["A2"].font = S["sub_font"]

    ws_exec.merge_cells("A4:J5")
    ov_str = ", ".join(
        f"{u} ({res['train_rows'][u]['total_2027_h']:,.1f} h)"
        for u in ordered_trains
        if res["train_rows"][u]["designation"] == "OVERHAUL"
    )
    mo_str = ", ".join(
        f"{u} ({res['train_rows'][u]['total_2027_h']:,.1f} h)"
        for u in ordered_trains
        if res["train_rows"][u]["designation"] == "MONITOR"
    )
    rig_m = res["rig_r1_asm"]["members"]
    ws_exec["A4"] = (
        f"Recommendation: Schedule four SWRO trains for 2027 vessel overhaul under Engineering Protocol SWRO-Q27 (>= 400 h): "
        f"{ov_str}, totaling {res['gold_asm']['A_overhaul_2027']:,.1f} overhaul-train hours and "
        f"{res['gold_asm']['A_overhaul_mwh']:,.1f} MWh projected energy penalty; retain {mo_str} on routine monitoring "
        f"(plant-wide {res['gold_asm']['A_total_2027']:,.1f} h; {res['gold_asm']['A_energy_mwh']:,.1f} MWh). "
        f"Rejects both raw monitoring and single-stream textbook models (stationary AR(1), 1D single-plug V_eff, pooled-CIP EM), "
        f"which miss TR01 ({rig_m['TR01']:,.1f} h) and TR02 ({rig_m['TR02']:,.1f} h) while mis-flagging TR03 ({rig_m['TR03']:,.1f} h), "
        f"TR04 ({rig_m['TR04']:,.1f} h), and TR05 ({rig_m['TR05']:,.1f} h)."
    )
    ws_exec["A4"].font = Font(name="Calibri", size=10, bold=True, color="0F172A")
    ws_exec["A4"].fill = S["call_fill"]
    ws_exec["A4"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    for rr in (4, 5):
        for cc in range(1, 11):
            ws_exec.cell(rr, cc).border = S["border"]
    ws_exec.row_dimensions[4].height = 29
    ws_exec.row_dimensions[5].height = 29

    # Main Triage Table (rows 7..18)
    t_hdrs = [
        "Train",
        "Bay",
        "2027 Boron (h)",
        "2027 Scaling (h)",
        "2027 Struct (h)",
        "2027 Total (h)",
        "2027 Q3 (h)",
        "2027 Energy (MWh)",
        "Criterion (h)",
        "Designation",
    ]
    for c, h in enumerate(t_hdrs, 1):
        ws_exec.cell(7, c, h)
    _style_header_row(ws_exec, 7, len(t_hdrs), S)

    for idx, u in enumerate(ordered_trains):
        r = 8 + idx
        tr = res["train_rows"][u]
        ws_exec.cell(r, 1, u)
        ws_exec.cell(r, 2, tr["plant_bay"])
        ws_exec.cell(r, 3, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$I$5:$I$36)")
        ws_exec.cell(r, 4, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$J$5:$J$36)")
        ws_exec.cell(r, 5, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$K$5:$K$36)")
        ws_exec.cell(r, 6, f"=SUM(C{r}:E{r})")
        ws_exec.cell(
            r,
            7,
            f'=SUMIFS(Operating_Plan_2027!$L$5:$L$36,Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$B$5:$B$36,"2027-Q3")',
        )
        ws_exec.cell(
            r,
            8,
            f"=(C{r}*{int(core.ENERGY_BORON_KWH)}+D{r}*{int(core.ENERGY_SCALING_KWH)}+E{r}*{int(core.ENERGY_STRUCT_KWH)})/1000",
        )
        ws_exec.cell(r, 9, int(core.THRESHOLD))
        ws_exec.cell(r, 10, f'=IF(F{r}>=I{r},"OVERHAUL","MONITOR")')

        is_ov = tr["designation"] == "OVERHAUL"
        for c in range(1, 11):
            cell = ws_exec.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if r % 2 == 0:
                cell.fill = S["zebra_fill"]
            if c in (1, 2):
                cell.alignment = Alignment(horizontal="center")
            elif c == 10:
                cell.alignment = Alignment(horizontal="center")
                cell.font = S["ov_font"] if is_ov else S["mo_font"]
                cell.fill = S["ov_fill"] if is_ov else S["mo_fill"]
            elif c == 8:
                cell.number_format = "#,##0.00"
                cell.alignment = Alignment(horizontal="right")
            elif c == 9:
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right")
            else:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")
                if c == 6:
                    cell.font = S["bold_font"]

    # Summary rows 16 (Plant Total), 17 (Overhaul Subtotal), 18 (Monitor Subtotal)
    ws_exec.cell(16, 1, "Plant Total")
    ws_exec.cell(16, 2, "8 Trains")
    for c in (3, 4, 5, 6, 7, 8):
        col_l = get_column_letter(c)
        ws_exec.cell(16, c, f"=SUM({col_l}8:{col_l}15)")
    ws_exec.cell(16, 10, '=COUNTIF(J8:J15,"OVERHAUL")&" OVERHAUL"')

    ws_exec.cell(17, 1, "Overhaul Subtotal")
    ws_exec.cell(17, 2, ">= 400 h")
    for c in (3, 4, 5, 6, 7, 8):
        col_l = get_column_letter(c)
        ws_exec.cell(17, c, f'=SUMIF($J$8:$J$15,"OVERHAUL",{col_l}8:{col_l}15)')
    ws_exec.cell(17, 10, "OVERHAUL")

    ws_exec.cell(18, 1, "Monitor Subtotal")
    ws_exec.cell(18, 2, "< 400 h")
    for c in (3, 4, 5, 6, 7, 8):
        col_l = get_column_letter(c)
        ws_exec.cell(18, c, f'=SUMIF($J$8:$J$15,"MONITOR",{col_l}8:{col_l}15)')
    ws_exec.cell(18, 10, "MONITOR")

    for rr in (16, 17, 18):
        for c in range(1, 11):
            cell = ws_exec.cell(rr, c)
            cell.font = S["bold_font"]
            cell.fill = S["tot_fill"] if rr == 16 else S["call_fill"]
            cell.border = S["tot_border"] if rr == 16 else S["border"]
            if c in (1, 2, 10):
                cell.alignment = Alignment(horizontal="center")
            elif c == 8:
                cell.number_format = "#,##0.00"
                cell.alignment = Alignment(horizontal="right")
            elif c in (3, 4, 5, 6, 7):
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    # KPI & Critical Components block (rows 20..29)
    ws_exec.cell(20, 1, f"Key Diagnostic Forecasts & {n_var}-Variant Estimation Uncertainty Ranges").font = S["sec_font"]
    kpi_hdrs = ["Diagnostic Metric", "Point Estimate", "Unit", f"{n_var}-Variant Range", "Protocol Ref"]
    for c, h in enumerate(kpi_hdrs, 1):
        ws_exec.cell(21, c, h)
    _style_header_row(ws_exec, 21, len(kpi_hdrs), S, fill_key="subhdr_fill")

    bnds = res["bands"]
    kpis = [
        ("Plant-wide 2027 Permeate Boron Hours (Component 1)", "=C16", "hours", f"{bnds['C1_boron_2027'][0]:,.1f} to {bnds['C1_boron_2027'][1]:,.1f}", "Clause 2.1 + Annex A", "#,##0.0"),
        ("Plant-wide 2027 Pretreatment-to-RO Scaling Hours (Component 2)", "=D16", "hours", f"{bnds['C2_scaling_2027'][0]:,.1f} to {bnds['C2_scaling_2027'][1]:,.1f}", "Clause 2.2 + Annex A", "#,##0.0"),
        ("Plant-wide 2027 Persistent Structural Fault Hours (Component 3)", "=E16", "hours", f"{bnds['C3_struct_2027'][0]:,.1f} to {bnds['C3_struct_2027'][1]:,.1f}", "Clause 2.3 + Annex A", "#,##0.0"),
        ("Plant-wide 2027 Total Anomalous Operating Hours", "=F16", "hours", f"{bnds['A_total_2027'][0]:,.1f} to {bnds['A_total_2027'][1]:,.1f}", "Clause 3.1", "#,##0.0"),
        ("Overhaul-Train 2027 Anomalous Hours (TR07, TR06, TR02, TR01)", "=F17", "hours", f"{bnds['A_overhaul_2027'][0]:,.1f} to {bnds['A_overhaul_2027'][1]:,.1f}", "Clause 3.1", "#,##0.0"),
        ("Plant-wide Summer Q3 2027 Anomalous Hours", "=G16", "hours", f"{bnds['A_q3_2027'][0]:,.1f} to {bnds['A_q3_2027'][1]:,.1f}", "Annex A", "#,##0.0"),
        ("Plant-wide 2027 Excess Desalination Energy Penalty", "=H16", "MWh", f"{bnds['A_energy_mwh'][0]:,.1f} to {bnds['A_energy_mwh'][1]:,.1f}", "Clause 4.3", "#,##0.0"),
        ("Overhaul-Train 2027 Excess Desalination Energy Penalty", "=H17", "MWh", f"{bnds['A_overhaul_mwh'][0]:,.1f} to {bnds['A_overhaul_mwh'][1]:,.1f}", "Clause 4.3", "#,##0.0"),
    ]
    for i, (lbl, fml, unit, btxt, ref, nfmt) in enumerate(kpis):
        r = 22 + i
        ws_exec.cell(r, 1, lbl)
        ws_exec.cell(r, 2, fml)
        ws_exec.cell(r, 3, unit)
        ws_exec.cell(r, 4, btxt)
        ws_exec.cell(r, 5, ref)
        for c in range(1, 6):
            cell = ws_exec.cell(r, c)
            cell.font = S["bold_font"] if c == 2 else S["body_font"]
            cell.border = S["border"]
            if r % 2 == 0:
                cell.fill = S["zebra_fill"]
            if c == 2:
                cell.number_format = nfmt
                cell.alignment = Alignment(horizontal="right")
            elif c in (3, 4):
                cell.alignment = Alignment(horizontal="center")

    # Bar chart on Overhaul_Triage_2027 comparing every train's 2027 total vs 400h criterion
    chart = BarChart()
    chart.type = "bar"
    chart.style = 10
    chart.grouping = "clustered"
    chart.title = "Forecasted 2027 Anomalous Hours vs 400-Hour Overhaul Criterion"
    chart.title.tx.rich.p[0].pPr = ParagraphProperties(defRPr=CharacterProperties(sz=1100, b=True))
    chart.x_axis.title = "SWRO Train"
    chart.y_axis.title = "Projected 2027 Operating Hours"
    chart.x_axis.delete = False
    chart.y_axis.delete = False
    chart.legend.position = "t"
    data_ref = Reference(ws_exec, min_col=6, max_col=6, min_row=7, max_row=15)
    thr_ref = Reference(ws_exec, min_col=9, max_col=9, min_row=7, max_row=15)
    cats_ref = Reference(ws_exec, min_col=1, min_row=8, max_row=15)
    chart.add_data(data_ref, titles_from_data=True)
    chart.add_data(thr_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.series[0].graphicalProperties.solidFill = "163A5F"
    chart.series[1].graphicalProperties.solidFill = "C2410C"
    chart.width = 17.5
    chart.height = 11.4
    ws_exec.add_chart(chart, "F20")

    ws_exec.freeze_panes = "C8"
    _set_widths(ws_exec, [48, 14, 15, 18, 18, 15, 13, 16, 13, 14])
    _setup_print(ws_exec, 10, 44, repeat_row=7)

    # ==========================================================================
    # TAB 2: S1_Boron_Flux_Support
    # ==========================================================================
    ws_s1["A1"] = "Mode 1 Backup: Permeate Boron Solute-Flux Coupling (1/Q) & Multi-Support AR(1) Deconvolution (Clause 2.1)"
    ws_s1["A1"].font = S["title_font"]
    ws_s1["A2"] = "C_comp = alpha_{u,q} + beta_u / Q_bar_k + eps_bar_k^(Q) inverted to 1-hour support across 8,760 hourly flows (0.004 mg/L lab SD subtracted)."
    ws_s1["A2"].font = S["sub_font"]

    s1_hdrs = [
        "Train",
        "Fit Flux Slope beta (mg*m3/L*h)",
        "Mean alpha (mg/L)",
        "Obs Res V8/V4",
        "Fit Res V8/V4",
        "Obs Res r1(4h)",
        "Fit Res r1(4h)",
        "Fit Corr Scale lam (h)",
        "Fit 1h Res SD (mg/L)",
        "2027 Raw Comp (h)",
        "2027 Stat AR1 MLE (h)",
        "2027 Flux+AR1 Boron (h)",
    ]
    ws_s1.append([])
    ws_s1.append(s1_hdrs)  # row 4
    _style_header_row(ws_s1, 4, len(s1_hdrs), S)

    for idx, u in enumerate(ordered_trains):
        r = 5 + idx
        tr = res["train_rows"][u]
        ws_s1.cell(r, 1, u)
        ws_s1.cell(r, 2, round(tr["s1_beta_hat"], 2))
        ws_s1.cell(r, 3, round(sum(tr["s1_alphas"]) / 4.0, 4))
        ws_s1.cell(r, 4, round(tr["s1_v8_v4_obs"], 4))
        ws_s1.cell(r, 5, round(tr["s1_v8_v4_pred"], 4))
        ws_s1.cell(r, 6, round(tr["s1_r1_4_obs"], 4))
        ws_s1.cell(r, 7, round(tr["s1_r1_4_pred"], 4))
        ws_s1.cell(r, 8, round(tr["s1_lam_h"], 2))
        ws_s1.cell(r, 9, round(tr["s1_sd1"], 4))
        ws_s1.cell(r, 10, round(tr["s1_raw_2027_h"], 1))
        ws_s1.cell(r, 11, round(tr["s1_stat_ar1_2027_h"], 1))
        ws_s1.cell(r, 12, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$I$5:$I$36)")
        for c in range(1, len(s1_hdrs) + 1):
            cell = ws_s1.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if r % 2 == 0:
                cell.fill = S["zebra_fill"]
            if c == 1:
                cell.alignment = Alignment(horizontal="center")
            elif c in (2, 8):
                cell.number_format = "0.00"
                cell.alignment = Alignment(horizontal="right")
            elif c in (3, 4, 5, 6, 7, 9):
                cell.number_format = "0.000"
                cell.alignment = Alignment(horizontal="right")
            else:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    ws_s1.cell(13, 1, "Plant Total / Mean")
    for c in (2, 3, 4, 5, 6, 7, 8, 9):
        col_l = get_column_letter(c)
        ws_s1.cell(13, c, f"=AVERAGE({col_l}5:{col_l}12)")
    for c in (10, 11, 12):
        col_l = get_column_letter(c)
        ws_s1.cell(13, c, f"=SUM({col_l}5:{col_l}12)")
    for c in range(1, 13):
        cell = ws_s1.cell(13, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c in (2, 8):
            cell.number_format = "0.00"
        elif c in (3, 4, 5, 6, 7, 9):
            cell.number_format = "0.000"
        elif c in (10, 11, 12):
            cell.number_format = "#,##0.0"
    ws_s1.freeze_panes = "B5"
    _set_widths(ws_s1, [18, 18, 14, 13, 13, 13, 13, 17, 16, 16, 17, 18])
    _setup_print(ws_s1, 12, 13, repeat_row=4)

    # ==========================================================================
    # TAB 3: S2_TwoPath_Hydraulics
    # ==========================================================================
    ws_s2["A1"] = "Mode 2 Backup: Two-Path Bimodal DAF/DMF Hydraulic Short-Circuit Recovery (Clause 2.2)"
    ws_s2["A1"].font = S["title_font"]
    ws_s2["A2"] = "Conservative seawater conductivity c_out(Phi) = f_fast * c_in(Phi - V_fast) + (1 - f_fast) * c_in(Phi - V_main) profiled in cumulative flow Phi(t)."
    ws_s2["A2"].font = S["sub_font"]

    s2_hdrs = [
        "Train",
        "Nominal V_nom (m3)",
        "Bypass Share f_fast",
        "Fast V_fast (m3)",
        "Main V_main (m3)",
        "Two-Path Cond RMS (mS/cm)",
        "Single-Plug Cond RMS (mS/cm)",
        "Same-Time Cond RMS (mS/cm)",
        "2027 Same-Time (h)",
        "2027 Single-Plug V_eff (h)",
        "2027 Two-Path Scaling (h)",
    ]
    ws_s2.append([])
    ws_s2.append(s2_hdrs)  # row 4
    _style_header_row(ws_s2, 4, len(s2_hdrs), S)

    for idx, u in enumerate(ordered_trains):
        r = 5 + idx
        tr = res["train_rows"][u]
        ws_s2.cell(r, 1, u)
        ws_s2.cell(r, 2, tr["v_nom_m3"])
        ws_s2.cell(r, 3, round(tr["s2_f_fast_hat"], 4))
        ws_s2.cell(r, 4, round(tr["s2_v_fast_hat"], 1))
        ws_s2.cell(r, 5, round(tr["s2_v_main_hat"], 1))
        ws_s2.cell(r, 6, round(tr["s2_cond_rms"], 4))
        ws_s2.cell(r, 7, round(tr["s2_sp_cond_rms"], 4))
        ws_s2.cell(r, 8, round(tr["s2_raw_cond_rms"], 4))
        ws_s2.cell(r, 9, round(tr["s2_raw_2027_h"], 1))
        ws_s2.cell(r, 10, round(tr["s2_sp_2027_h"], 1))
        ws_s2.cell(r, 11, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$J$5:$J$36)")
        for c in range(1, len(s2_hdrs) + 1):
            cell = ws_s2.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if r % 2 == 0:
                cell.fill = S["zebra_fill"]
            if c == 1:
                cell.alignment = Alignment(horizontal="center")
            elif c == 3:
                cell.number_format = "0.0%"
                cell.alignment = Alignment(horizontal="right")
            elif c in (6, 7, 8):
                cell.number_format = "0.000"
                cell.alignment = Alignment(horizontal="right")
            else:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    ws_s2.cell(13, 1, "Plant Total / Mean")
    for c in (2, 3, 4, 5, 6, 7, 8):
        col_l = get_column_letter(c)
        ws_s2.cell(13, c, f"=AVERAGE({col_l}5:{col_l}12)")
    for c in (9, 10, 11):
        col_l = get_column_letter(c)
        ws_s2.cell(13, c, f"=SUM({col_l}5:{col_l}12)")
    for c in range(1, 12):
        cell = ws_s2.cell(13, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c == 3:
            cell.number_format = "0.0%"
        elif c in (6, 7, 8):
            cell.number_format = "0.000"
        elif c >= 2:
            cell.number_format = "#,##0.0"
    ws_s2.freeze_panes = "B5"
    _set_widths(ws_s2, [18, 16, 15, 14, 15, 18, 19, 18, 16, 19, 19])
    _setup_print(ws_s2, 11, 13, repeat_row=4)

    # ==========================================================================
    # TAB 4: S3_DualCIP_LCA
    # ==========================================================================
    ws_s3["A1"] = "Mode 3 Backup: 4-State Dual-Recipe CIP-Invariant Latent-Class Diagnostics (Clause 2.3)"
    ws_s3["A1"].font = S["title_font"]
    p_bio = res["train_rows"]["TR01"]["s3_p_bio"]
    p_min = res["train_rows"]["TR01"]["s3_p_min"]
    p_str = res["train_rows"]["TR01"]["s3_p_str"]
    ws_s3["A2"] = (
        f"192-cell EM (8 trains x 3 regimes [Pre, Post-ALK, Post-ACID] x 8 triples): "
        f"Bio=({p_bio[0]:.2f},{p_bio[1]:.2f},{p_bio[2]:.3f}), "
        f"MinCrust=({p_min[0]:.2f},{p_min[1]:.2f},{p_min[2]:.2f}), "
        f"Struct=({p_str[0]:.2f},{p_str[1]:.2f},{p_str[2]:.2f})."
    )
    ws_s3["A2"].font = S["sub_font"]

    s3_hdrs = [
        "Train",
        "CIP_ALK Washes",
        "CIP_ACID Washes",
        "Obs D3 Drop ALK (pp)",
        "Obs D3 Drop ACID (pp)",
        "Fit Bio-Foul Prev",
        "Fit Min-Crust Prev",
        "Fit Struct Prev",
        "2027 2-of-3 MV (h)",
        "2027 Pooled-CIP 3-St (h)",
        "2027 Post-CIP 2-Cl DS (h)",
        "2027 4-State Dual-CIP (h)",
    ]
    ws_s3.append([])
    ws_s3.append(s3_hdrs)  # row 4
    _style_header_row(ws_s3, 4, len(s3_hdrs), S)

    for idx, u in enumerate(ordered_trains):
        r = 5 + idx
        tr = res["train_rows"][u]
        obs = tr["s3_obs_drops"]
        ws_s3.cell(r, 1, u)
        ws_s3.cell(r, 2, tr["s3_n_alk"])
        ws_s3.cell(r, 3, tr["s3_n_acid"])
        ws_s3.cell(r, 4, round(100.0 * obs["drop_d3_alk"], 2))
        ws_s3.cell(r, 5, round(100.0 * obs["drop_d3_acid"], 2))
        ws_s3.cell(r, 6, round(tr["s3_pi_bio_hat"], 5))
        ws_s3.cell(r, 7, round(tr["s3_pi_min_hat"], 5))
        ws_s3.cell(r, 8, round(tr["s3_pi_s_hat"], 5))
        ws_s3.cell(r, 9, round(tr["s3_raw_2027_h"], 1))
        ws_s3.cell(r, 10, round(tr["s3_r1_2027_h"], 1))
        ws_s3.cell(r, 11, round(tr["s3_r2_2027_h"], 1))
        ws_s3.cell(r, 12, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$K$5:$K$36)")
        for c in range(1, len(s3_hdrs) + 1):
            cell = ws_s3.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if r % 2 == 0:
                cell.fill = S["zebra_fill"]
            if c == 1:
                cell.alignment = Alignment(horizontal="center")
            elif c in (2, 3):
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right")
            elif c in (4, 5):
                cell.number_format = "0.00"
                cell.alignment = Alignment(horizontal="right")
            elif c in (6, 7, 8):
                cell.number_format = "0.00%"
                cell.alignment = Alignment(horizontal="right")
            else:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    ws_s3.cell(13, 1, "Plant Total / Mean")
    ws_s3.cell(13, 2, "=SUM(B5:B12)")
    ws_s3.cell(13, 3, "=SUM(C5:C12)")
    for c in (4, 5, 6, 7, 8):
        col_l = get_column_letter(c)
        ws_s3.cell(13, c, f"=AVERAGE({col_l}5:{col_l}12)")
    for c in (9, 10, 11, 12):
        col_l = get_column_letter(c)
        ws_s3.cell(13, c, f"=SUM({col_l}5:{col_l}12)")
    for c in range(1, 13):
        cell = ws_s3.cell(13, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c in (2, 3):
            cell.number_format = "#,##0"
        elif c in (4, 5):
            cell.number_format = "0.00"
        elif c in (6, 7, 8):
            cell.number_format = "0.00%"
        elif c in (9, 10, 11, 12):
            cell.number_format = "#,##0.0"
    ws_s3.freeze_panes = "B5"
    _set_widths(ws_s3, [18, 14, 15, 16, 17, 15, 16, 14, 16, 19, 19, 19])
    _setup_print(ws_s3, 12, 13, repeat_row=4)

    # ==========================================================================
    # TAB 5: Falsification_And_Routes
    # ==========================================================================
    ws_fal["A1"] = "Physical Falsification Checks (F1-F3) & Analytical Routes Comparison"
    ws_fal["A1"].font = S["title_font"]
    ws_fal["A2"] = "Direct native-unit physical identities across 2026 logs (zero anomaly labels required) paired with every alternative model's triage result."
    ws_fal["A2"].font = S["sub_font"]

    f_hdrs = [
        "Method / Route",
        "F1 Flux+Moment Err",
        "F2 Cond RMS (mS/cm)",
        "F3 Dual-CIP Drop Err (pp)",
        "Flagged Overhaul Set",
        "Total 2027 (h)",
        "Energy Penalty (MWh)",
    ]
    ws_fal.append([])
    ws_fal.append(f_hdrs)  # row 4
    _style_header_row(ws_fal, 4, len(f_hdrs), S)

    route_lookup = [
        ("Golden (Flux+AR1 + Two-Path Hydraulics + 4-State Dual-CIP EM)", "golden", res["gold_asm"]),
        ("Direct / Raw Monitoring (Raw Comp + Same-Time + 2-of-3 MV)", "direct", res["lattice_asm"]["S1+S2+S3"]),
        ("Textbook R1 (Stationary AR1 + 1D Single-Plug V_eff + 3-State Pooled-CIP)", "rigorous_r1", res["rig_r1_asm"]),
        ("Textbook R2 (Stationary AR1 + 1D Single-Plug V_eff + Post-CIP 2-Class DS)", "rigorous_r2", res["rig_r2_asm"]),
        ("Cutoff Filter (4h-Only + Fixed Lag + Post-CIP MV)", "cutoff", res["cut_asm"]),
        ("Generous Upper (i.i.d. sqrt(m) + Comonotonic + Post-CIP 2-Class DS)", "generous", res["gen_asm"]),
        ("Hedge Blend (80% Direct / 20% Physical)", "hedge", res["hedge_asm"]),
        ("Drop S1 Only (Raw Boron + Golden S2 & S3)", "S1_lost", res["lattice_asm"]["S1"]),
        ("Drop S2 Only (Same-Time Scaling + Golden S1 & S3)", "S2_lost", res["lattice_asm"]["S2"]),
        ("Drop S3 Only (2-of-3 MV + Golden S1 & S2)", "S3_lost", res["lattice_asm"]["S3"]),
        ("Over-Correct S1 (i.i.d. sqrt(m) + Golden S2 & S3)", "S1_over", res["over"]["S1"]),
        ("Over-Correct S2 (Comonotonic + Golden S1 & S3)", "S2_over", res["over"]["S2"]),
        ("Over-Correct S3 (Uninverted Raw D3 Post-Acid + Golden S1 & S2)", "S3_over", res["over"]["S3"]),
    ]

    for idx, (label, fkey, asm) in enumerate(route_lookup):
        r = 5 + idx
        fl = res["fal_by_route"][fkey]
        sl = ", ".join(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD))
        ws_fal.cell(r, 1, label)
        ws_fal.cell(r, 2, round(fl["f1"], 4))
        ws_fal.cell(r, 3, round(fl["f2_ms_cm"], 3))
        ws_fal.cell(r, 4, round(fl["f3_pp"], 3))
        ws_fal.cell(r, 5, sl)
        ws_fal.cell(r, 6, round(asm["A_total_2027"], 1))
        ws_fal.cell(r, 7, round(asm["A_energy_mwh"], 1))
        for c in range(1, 8):
            cell = ws_fal.cell(r, c)
            cell.font = S["bold_font"] if idx == 0 else S["body_font"]
            cell.fill = S["call_fill"] if idx == 0 else (S["zebra_fill"] if r % 2 == 0 else PatternFill(fill_type=None))
            cell.border = S["border"]
            if c == 2:
                cell.number_format = "0.0000"
                cell.alignment = Alignment(horizontal="right")
            elif c in (3, 4):
                cell.number_format = "0.000"
                cell.alignment = Alignment(horizontal="right")
            elif c in (6, 7):
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    # Table 2: Per-train figures across major routes (rows 20..34)
    ws_fal.cell(20, 1, "Per-Train 2027 Forecasted Anomalous Hours Across Routes (Criterion = 400.0 h)").font = S["sec_font"]
    rt_hdrs = ["Method / Route"] + core.TRAINS + ["C1 Boron", "C2 Scaling", "C3 Struct"]
    for c, h in enumerate(rt_hdrs, 1):
        ws_fal.cell(21, c, h)
    _style_header_row(ws_fal, 21, len(rt_hdrs), S, fill_key="subhdr_fill")

    for idx, (label, _fkey, asm) in enumerate(route_lookup):
        r = 22 + idx
        ws_fal.cell(r, 1, label)
        for j, u in enumerate(core.TRAINS):
            ws_fal.cell(r, 2 + j, round(asm["members"][u], 1))
        ws_fal.cell(r, 10, round(asm["C1_boron_2027"], 1))
        ws_fal.cell(r, 11, round(asm["C2_scaling_2027"], 1))
        ws_fal.cell(r, 12, round(asm["C3_struct_2027"], 1))
        for c in range(1, 13):
            cell = ws_fal.cell(r, c)
            cell.font = S["bold_font"] if idx == 0 else S["body_font"]
            cell.border = S["border"]
            if c >= 2:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    ws_fal.freeze_panes = "B5"
    _set_widths(ws_fal, [58, 19, 17, 21, 30, 14, 17, 11, 11, 13, 13, 13])
    _setup_print(ws_fal, 12, 34, repeat_row=4)

    # ==========================================================================
    # TAB 7: Sensitivity_And_QA_2026 (26-variant battery + 6 forcing perturbations + QA)
    # ==========================================================================
    ws_sens["A1"] = f"Barlavento SWRO {n_var}-Variant Uncertainty Battery, Forcing Perturbations & 2026 Data QA"
    ws_sens["A1"].font = S["title_font"]
    ws_sens["A2"] = "Every defensible estimator specification and +/-20% independent mode perturbation preserves the exact 4-of-8 overhaul slate."
    ws_sens["A2"].font = S["sub_font"]

    v_hdrs = ["Variant / Perturbation", "Overhaul Slate", "TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08", "Plant Total", "Matches Golden"]
    ws_sens.append([])
    ws_sens.append(v_hdrs)  # row 4
    _style_header_row(ws_sens, 4, len(v_hdrs), S)

    vr = 5
    g_sl_str = ", ".join(res["golden_slate"])
    for nm, asm in res["variants_named"]:
        sl = ", ".join(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD))
        ws_sens.cell(vr, 1, nm)
        ws_sens.cell(vr, 2, sl)
        for j, u in enumerate(core.TRAINS):
            ws_sens.cell(vr, 3 + j, round(asm["members"][u], 1))
        ws_sens.cell(vr, 11, round(asm["A_total_2027"], 1))
        ws_sens.cell(vr, 12, "HOLD" if sl == g_sl_str else "FLIP")
        for c in range(1, 13):
            cell = ws_sens.cell(vr, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if vr % 2 == 0:
                cell.fill = S["zebra_fill"]
            if 3 <= c <= 11:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")
            elif c == 12:
                cell.alignment = Alignment(horizontal="center")
        vr += 1

    for pt in res["perturbations"]:
        sl = ", ".join(pt["answer"])
        ws_sens.cell(vr, 1, f"Forcing: {pt['input']}")
        ws_sens.cell(vr, 2, sl)
        ws_sens.cell(vr, 3, f"min OV={pt['min_overhaul']:.1f}")
        ws_sens.cell(vr, 4, f"max MO={pt['max_monitor']:.1f}")
        ws_sens.cell(vr, 12, "HOLD" if pt["holds"] else "FLIP")
        for c in range(1, 13):
            cell = ws_sens.cell(vr, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if c == 12:
                cell.alignment = Alignment(horizontal="center")
        vr += 1

    # Cleaning & conventions notes
    nr = vr + 1
    ws_sens.cell(nr, 1, "2026 Operational Archive Conformance & QA Audit").font = S["sec_font"]
    cl = res["cleaning"]
    notes = [
        f"As-of archive date: {PK.AS_OF}; diagnostics finalized 2027-01-21 under Engineering Protocol SWRO-Q27 (BDM-ENG-Q27-2026).",
        f"LIMS permeate boron assays cleaned from {cl['boron_raw_rows']:,} raw rows to {cl['boron_clean_rows']:,} unique bottles ({cl['boron_superseded_dropped']} superseded rev-1 rows removed, {cl['boron_ug_rows']:,} South-bay ug/L rows converted to mg/L, {cl['boron_dmy_rows']:,} DD/MM/YYYY dates parsed, {cl['boron_legacy_rows']} legacy LINE tags mapped).",
        f"15-minute chemistry cleaned from {cl['intake_raw_rows']:,} intake ({cl['intake_dups_dropped']} dup frames removed) and {cl['ro_feed_raw_rows']:,} RO-feed ({cl['ro_feed_dups_dropped']} dup frames removed) to 280,320 exact intervals each; first 32 burn-in intervals excluded per Clause 2.2.",
        f"Hourly SCADA hydraulics cleaned from {cl['hydraulics_raw_rows']:,} to {cl['hydraulics_clean_rows']:,} rows ({cl['hydraulics_dups_dropped']} retry polls removed, {cl['hydraulics_ls_rows']:,} South-bay L/s rows converted to m3/h). Shift diagnostics (17,520 blocks) and {cl['cip_rows']} CIP washes ({cl['cip_alk_rows']} CIP_ALK_pH11, {cl['cip_acid_rows']} CIP_ACID_pH2) aligned via Europe/Lisbon ISO offsets.",
        "Out-of-scope regional files (mibel_iberian_power_spot_2026.csv, algarve_reservoir_levels_2026.xlsx) excluded from membrane reliability estimation.",
    ]
    for i, txt in enumerate(notes, 1):
        ws_sens.cell(nr + i, 1, txt).font = S["note_font"]

    ws_sens.freeze_panes = "B5"
    _set_widths(ws_sens, [50, 22, 14, 13, 13, 13, 13, 13, 13, 13, 15, 15])
    _setup_print(ws_sens, 12, nr + len(notes), repeat_row=4)

    path = os.path.join(golden_dir, GOLDEN_XLSX)
    wb.save(path)
    return path


def build_goldens_and_zips(task_dir=None, res=None):
    task_dir = task_dir or os.path.dirname(HERE)
    target_dir = os.path.join(task_dir, "target")
    golden_dir = os.path.join(task_dir, "golden")
    if res is None:
        res = AN.run_all(target_dir)

    if os.path.isdir(golden_dir):
        shutil.rmtree(golden_dir)
    os.makedirs(golden_dir)

    csv_path, ordered = write_csv(golden_dir, res)
    xlsx_path = write_workbook(golden_dir, res, ordered)

    postprocess.normalize_ooxml(
        xlsx_path,
        PK.PEOPLE["lead"],
        PK.PEOPLE["lead"],
        "2027-01-20T09:15:00Z",
        "2027-01-21T16:42:18Z",
        excel=True,
        company=PK.ORG,
    )
    postprocess.own_mtimes(
        golden_dir,
        {
            GOLDEN_CSV: dt.datetime(2027, 1, 21, 16, 47, 5, tzinfo=UTC),
        },
    )

    target_zip = os.path.join(task_dir, "target.zip")
    golden_zip = os.path.join(task_dir, "golden.zip")
    postprocess.zip_folder(target_dir, target_zip, zone="Europe/Lisbon")
    postprocess.zip_folder(golden_dir, golden_zip, zone="Europe/Lisbon")

    return {
        "csv": csv_path,
        "xlsx": xlsx_path,
        "target_zip": target_zip,
        "golden_zip": golden_zip,
    }


if __name__ == "__main__":
    out = build_goldens_and_zips()
    for k, p in out.items():
        print(f"{k:12s} {os.path.getsize(p):10d}  {p}")
