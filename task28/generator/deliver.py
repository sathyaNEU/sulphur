#!/usr/bin/env python3
"""task28/generator/deliver.py (v3): Build the two requested golden deliverables in task28/golden/
and cut target.zip and golden.zip:
  1. golden/barlavento_swro_overhaul_plan_2027.xlsx (8 formula-driven tabs, styled, chart, postprocess scrubbed)
  2. golden/barlavento_train_diagnostics_2027.csv (exact SWRO-Q27 Annex B 9-column schema)

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
                "tds_2027_h",
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
                    f"{tr['tds_2027_h']:.1f}",
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
    ws_s1 = wb.create_sheet("S1_Boron_MassFlux")
    ws_s2 = wb.create_sheet("S2_TwoPath_Hydraulics")
    ws_s3 = wb.create_sheet("S3_KineticCIP_LCA")
    ws_s4 = wb.create_sheet("S4_BayTDS_Deconv")
    ws_fal = wb.create_sheet("Falsification_And_Routes")
    ws_plan = wb.create_sheet("Operating_Plan_2027")
    ws_sens = wb.create_sheet("Sensitivity_And_QA_2026")

    # ==========================================================================
    # TAB 7: Operating_Plan_2027 (built first so Overhaul_Triage_2027 links to it)
    # ==========================================================================
    ws_plan["A1"] = "Barlavento SWRO 2026-to-2027 Quarterly 4-Mode Failure Forecast (Protocol SWRO-Q27 Annex A)"
    ws_plan["A1"].font = S["title_font"]
    ws_plan["A2"] = "Uniform Annex A quarterly multipliers from operating_plan_2027.csv applied to estimated 2026 physical mode hours."
    ws_plan["A2"].font = S["sub_font"]

    plan_hdrs = [
        "Train", "Quarter",
        "2026 Boron (h)", "2026 Scaling (h)", "2026 Struct (h)", "2026 TDS (h)",
        "Duty Ratio", "Boron Temp", "Scaling Rec", "Salinity Temp",
        "2027 Boron (h)", "2027 Scaling (h)", "2027 Struct (h)", "2027 TDS (h)",
        "2027 Total (h)", "2027 Energy (MWh)",
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
            ws_plan.cell(r, 6, round(tr["tds_2026_q"][q], 6))
            ws_plan.cell(r, 7, sr[q])
            ws_plan.cell(r, 8, res["plan"]["boron_temp_q"][q])
            ws_plan.cell(r, 9, res["plan"]["scaling_rec_q"][q])
            ws_plan.cell(r, 10, res["plan"]["tds_sal_q"][q])
            ws_plan.cell(r, 11, f"=C{r}*H{r}*G{r}")
            ws_plan.cell(r, 12, f"=D{r}*I{r}*G{r}")
            ws_plan.cell(r, 13, f"=E{r}*G{r}")
            ws_plan.cell(r, 14, f"=F{r}*J{r}*G{r}")
            ws_plan.cell(r, 15, f"=SUM(K{r}:N{r})")
            ws_plan.cell(
                r, 16,
                f"=(K{r}*{int(core.ENERGY_BORON_KWH)}+L{r}*{int(core.ENERGY_SCALING_KWH)}"
                f"+M{r}*{int(core.ENERGY_STRUCT_KWH)}+N{r}*{int(core.ENERGY_TDS_KWH)})/1000",
            )
            for c in range(1, len(plan_hdrs) + 1):
                cell = ws_plan.cell(r, c)
                cell.font = S["body_font"]
                cell.border = S["border"]
                if r % 2 == 0:
                    cell.fill = S["zebra_fill"]
                if c <= 2:
                    cell.alignment = Alignment(horizontal="center")
                elif c in (7, 8, 9, 10):
                    cell.number_format = "0.00"
                    cell.alignment = Alignment(horizontal="right")
                elif c == 16:
                    cell.number_format = "#,##0.00"
                    cell.alignment = Alignment(horizontal="right")
                else:
                    cell.number_format = "#,##0.0"
                    cell.alignment = Alignment(horizontal="right")
            plan_row += 1

    tot_p = plan_row  # row 37
    ws_plan.cell(tot_p, 1, "Plant Total")
    ws_plan.cell(tot_p, 2, "All 4 Qtrs")
    for c in (3, 4, 5, 6, 11, 12, 13, 14, 15, 16):
        col_l = get_column_letter(c)
        ws_plan.cell(tot_p, c, f"=SUM({col_l}5:{col_l}{tot_p - 1})")
    for c in range(1, len(plan_hdrs) + 1):
        cell = ws_plan.cell(tot_p, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c == 16:
            cell.number_format = "#,##0.00"
        elif c in (3, 4, 5, 6, 11, 12, 13, 14, 15):
            cell.number_format = "#,##0.0"
    ws_plan.freeze_panes = "C5"
    _set_widths(ws_plan, [10, 11, 13, 14, 13, 13, 11, 12, 12, 13, 13, 14, 13, 13, 14, 16])
    _setup_print(ws_plan, len(plan_hdrs), tot_p, repeat_row=4)

    # ==========================================================================
    # TAB 1: Overhaul_Triage_2027 (Executive summary + live formulas + bar chart)
    # ==========================================================================
    n_var = len(res["variants_named"])
    ov_list = [u for u in ordered_trains if res["train_rows"][u]["designation"] == "OVERHAUL"]
    mo_list = [u for u in ordered_trains if res["train_rows"][u]["designation"] == "MONITOR"]
    ws_exec["A1"] = f"Barlavento SWRO 2027 Vessel Overhaul Diagnostics: Pull {', '.join(ov_list)} (>= 400 h)"
    ws_exec["A1"].font = S["title_font"]
    ws_exec["A2"] = (
        f"Estacao Dessalinizadora de Alvor | Engineering Protocol SWRO-Q27 4-Mode Reliability Diagnostics | "
        f"Prepared by {PK.PEOPLE['lead']} | Archive As-Of {PK.AS_OF}"
    )
    ws_exec["A2"].font = S["sub_font"]

    ws_exec.merge_cells("A4:K5")
    ov_str = ", ".join(f"{u} ({res['train_rows'][u]['total_2027_h']:,.1f} h)" for u in ov_list)
    mo_str = ", ".join(f"{u} ({res['train_rows'][u]['total_2027_h']:,.1f} h)" for u in mo_list)
    ws_exec["A4"] = (
        f"RECOMMENDATION: Schedule {len(ov_list)} SWRO trains for 2027 pressure-vessel overhaul (>= 400.0 h): {ov_str}. "
        f"Retain {len(mo_list)} trains on routine CIP monitoring: {mo_str}. "
        f"Plant-wide 2027 anomalous total is {res['gold_asm']['A_total_2027']:,.1f} h "
        f"({res['gold_asm']['A_energy_mwh']:,.1f} MWh total energy penalty; "
        f"{res['gold_asm']['A_overhaul_mwh']:,.1f} MWh on overhaul trains; "
        f"{res['gold_asm']['A_q3_2027']:,.1f} h in summer Q3). All {n_var} physical variants and all 8 +/-20% perturbations hold."
    )
    ws_exec["A4"].font = S["bold_font"]
    ws_exec["A4"].fill = S["call_fill"]
    ws_exec["A4"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    for r_m in (4, 5):
        ws_exec.row_dimensions[r_m].height = 24
        for c_m in range(1, 12):
            ws_exec.cell(r_m, c_m).border = S["border"]

    exec_hdrs = [
        "Train", "Plant Bay",
        "2027 Boron (h)", "2027 Scaling (h)", "2027 Struct (h)", "2027 TDS (h)",
        "2027 Total (h)", "2027 Q3 (h)", "2027 Energy (MWh)",
        f"{n_var}-Variant Range (h)", "2027 Designation",
    ]
    for c_i, h in enumerate(exec_hdrs, 1):
        ws_exec.cell(7, c_i, h)
    _style_header_row(ws_exec, 7, len(exec_hdrs), S)

    for idx, u in enumerate(ordered_trains):
        r = 8 + idx
        tr = res["train_rows"][u]
        lo, hi = res["bands"][u]
        ws_exec.cell(r, 1, u)
        ws_exec.cell(r, 2, tr["bay"])
        ws_exec.cell(r, 3, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$K$5:$K$36)")
        ws_exec.cell(r, 4, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$L$5:$L$36)")
        ws_exec.cell(r, 5, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$M$5:$M$36)")
        ws_exec.cell(r, 6, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$N$5:$N$36)")
        ws_exec.cell(r, 7, f"=SUM(C{r}:F{r})")
        ws_exec.cell(r, 8, f'=SUMIFS(Operating_Plan_2027!$O$5:$O$36,Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$B$5:$B$36,"2027-Q3")')
        ws_exec.cell(r, 9, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$P$5:$P$36)")
        ws_exec.cell(r, 10, f"{lo:,.1f} - {hi:,.1f}")
        ws_exec.cell(r, 11, f'=IF(G{r}>=400,"OVERHAUL","MONITOR")')
        for c in range(1, 12):
            cell = ws_exec.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if idx % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c in (1, 2, 10):
                cell.alignment = Alignment(horizontal="center")
            elif c == 9:
                cell.number_format = "#,##0.00"
                cell.alignment = Alignment(horizontal="right")
            elif c == 11:
                cell.alignment = Alignment(horizontal="center")
                cell.font = S["ov_font"] if tr["designation"] == "OVERHAUL" else S["mo_font"]
                cell.fill = S["ov_fill"] if tr["designation"] == "OVERHAUL" else S["mo_fill"]
            else:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")
                if c == 7:
                    cell.font = S["bold_font"]

    # Rows 16, 17, 18 summary rows
    for row_i, label, cond in [
        (16, "Plant Total (All 8 Trains)", None),
        (17, "Overhaul Subset (>= 400.0 h)", "OVERHAUL"),
        (18, "Monitor Subset (< 400.0 h)", "MONITOR"),
    ]:
        ws_exec.cell(row_i, 1, label)
        ws_exec.cell(row_i, 2, "Both Bays")
        for c in (3, 4, 5, 6, 7, 8, 9):
            col_l = get_column_letter(c)
            if cond is None:
                ws_exec.cell(row_i, c, f"=SUM({col_l}8:{col_l}15)")
            else:
                ws_exec.cell(row_i, c, f'=SUMIF($K$8:$K$15,"{cond}",{col_l}8:{col_l}15)')
        if cond is None:
            lo_t, hi_t = res["bands"]["A_total_2027"]
            ws_exec.cell(row_i, 10, f"{lo_t:,.1f} - {hi_t:,.1f}")
            ws_exec.cell(row_i, 11, '=COUNTIF(K8:K15,"OVERHAUL")&" OVERHAUL"')
        elif cond == "OVERHAUL":
            lo_o, hi_o = res["bands"]["A_overhaul_2027"]
            ws_exec.cell(row_i, 10, f"{lo_o:,.1f} - {hi_o:,.1f}")
            ws_exec.cell(row_i, 11, "OVERHAUL")
        else:
            ws_exec.cell(row_i, 10, "-")
            ws_exec.cell(row_i, 11, "MONITOR")
        for c in range(1, 12):
            cell = ws_exec.cell(row_i, c)
            cell.font = S["bold_font"]
            cell.fill = S["tot_fill"] if row_i == 16 else S["call_fill"]
            cell.border = S["tot_border"] if row_i == 16 else S["border"]
            if c in (2, 10, 11):
                cell.alignment = Alignment(horizontal="center")
            elif c == 9:
                cell.number_format = "#,##0.00"
                cell.alignment = Alignment(horizontal="right")
            elif c >= 3:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    # Headline Uncertainty Ranges Table (rows 20..30; merge A:C for wide metric labels so zero text clips)
    ws_exec["A20"] = f"Headline Plant-Wide 2027 Metrics and {n_var}-Variant Estimation Uncertainty Ranges"
    ws_exec["A20"].font = S["sec_font"]
    ws_exec.merge_cells("A21:C21")
    ws_exec.cell(21, 1, "Headline Metric")
    rng_hdrs = ["Golden Estimate", f"{n_var}-Variant Min", f"{n_var}-Variant Max", "Spread", "Unit"]
    for c_i, h in enumerate(rng_hdrs, 4):
        ws_exec.cell(21, c_i, h)
    _style_header_row(ws_exec, 21, 8, S, fill_key="subhdr_fill")
    ws_exec.cell(21, 1).alignment = Alignment(horizontal="left", vertical="center")

    hl_rows = [
        ("C1: Plant-Wide 2027 Permeate Boron Hours", "=C16", "C1_boron_2027", "hours"),
        ("C2: Plant-Wide 2027 Pretreatment-to-RO Scaling Hours", "=D16", "C2_scaling_2027", "hours"),
        ("C3: Plant-Wide 2027 Persistent Structural Fault Hours", "=E16", "C3_struct_2027", "hours"),
        ("C4: Plant-Wide 2027 Permeate TDS Breakthrough Hours", "=F16", "C4_tds_2027", "hours"),
        ("Plant-Wide 2027 Total Anomalous Hours (All 8 Trains)", "=G16", "A_total_2027", "hours"),
        ("Overhaul-Train 2027 Anomalous Hours (5 Trains >= 400 h)", "=G17", "A_overhaul_2027", "hours"),
        ("Summer 2027 Q3 Total Anomalous Hours (All 8 Trains)", "=H16", "A_q3_2027", "hours"),
        ("Plant-Wide 2027 Excess Desalination Energy Penalty", "=I16", "A_energy_mwh", "MWh"),
        ("Overhaul-Train 2027 Excess Desalination Energy Penalty", "=I17", "A_overhaul_mwh", "MWh"),
    ]
    for i, (lbl, formula, bkey, unit) in enumerate(hl_rows):
        r = 22 + i
        lo, hi = res["bands"][bkey]
        ws_exec.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        ws_exec.cell(r, 1, lbl)
        ws_exec.cell(r, 4, formula)
        ws_exec.cell(r, 5, lo)
        ws_exec.cell(r, 6, hi)
        ws_exec.cell(r, 7, f"=F{r}-E{r}")
        ws_exec.cell(r, 8, unit)
        for c in range(1, 9):
            cell = ws_exec.cell(r, c)
            cell.font = S["bold_font"] if i in (4, 7) else S["body_font"]
            cell.border = S["border"]
            if i % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c == 1:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c == 8:
                cell.alignment = Alignment(horizontal="center")
            elif c >= 4:
                cell.number_format = "#,##0.0"
                cell.alignment = Alignment(horizontal="right")

    # Stacked Bar Chart comparing all 8 trains against 400.0 h overhaul criterion (cleanly anchored at A32!)
    chart = BarChart()
    chart.type = "bar"
    chart.grouping = "stacked"
    chart.overlap = 100
    chart.title = "Projected 2027 Anomalous Hours by SWRO Train & Mode (Overhaul Criterion: 400.0 h)"
    chart.x_axis.title = "SWRO Train"
    chart.y_axis.title = "Projected 2027 Operating Hours"
    chart.style = 10
    data_ref = Reference(ws_exec, min_col=3, max_col=6, min_row=7, max_row=15)
    cats_ref = Reference(ws_exec, min_col=1, min_row=8, max_row=15)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    colors_hex = ["1D4ED8", "0D9488", "D97706", "7C3AED"]
    for s_idx, ser in enumerate(chart.series):
        ser.graphicalProperties.solidFill = colors_hex[s_idx % len(colors_hex)]
    chart.width = 25.0
    chart.height = 11.5
    chart.legend.position = "b"
    chart.y_axis.delete = False
    chart.x_axis.delete = False
    cp = CharacterProperties(sz=900)
    pp = ParagraphProperties(defRPr=cp)
    chart.x_axis.txPr = openpyxl.chart.text.RichText(p=[openpyxl.drawing.text.Paragraph(pPr=pp)])
    chart.y_axis.txPr = openpyxl.chart.text.RichText(p=[openpyxl.drawing.text.Paragraph(pPr=pp)])
    ws_exec.add_chart(chart, "A32")

    ws_exec.freeze_panes = "C8"
    _set_widths(ws_exec, [24, 11, 14, 15, 14, 13, 14, 13, 16, 19, 16])
    _setup_print(ws_exec, 11, 56, repeat_row=7)

    # ==========================================================================
    # TAB 2: S1_Boron_MassFlux
    # ==========================================================================
    ws_s1["A1"] = "Mode 1 (Clause 2.1): Spiegler-Kedem Solute Mass-Flux Boron Composite Deconvolution"
    ws_s1["A1"].font = S["title_font"]
    ws_s1["A2"] = "Mass-flux regression M_k = Q_bar_k * C_comp_k = alpha_q * Q_bar_k + mu_J + eta_bar_k and flux-space AR(1) 4h/8h support deconvolution (SD(C_t) = sigma_J / Q_t)."
    ws_s1["A2"].font = S["sub_font"]
    s1_hdrs = [
        "Train", "Alpha Q1", "Alpha Q2", "Alpha Q3", "Alpha Q4",
        "Mean mu_J (g/h)", "Flux SD sigma_J (g/h)", "Scale lambda (h)",
        "Flux Het Corr", "2026 Raw Comp (h)", "2026 R2 Homosc (h)",
        "2026 Golden (h)", "2027 Golden (h)",
    ]
    ws_s1.append([])
    ws_s1.append(s1_hdrs)
    _style_header_row(ws_s1, 4, len(s1_hdrs), S)
    for i, u in enumerate(core.TRAINS):
        r = 5 + i
        tr = res["train_rows"][u]
        als = tr["s1_alphas"]
        ws_s1.cell(r, 1, u)
        for q in range(4):
            ws_s1.cell(r, 2 + q, round(als[q], 4))
        ws_s1.cell(r, 6, round(tr["s1_mu_j"], 2))
        ws_s1.cell(r, 7, round(tr["s1_sd_j"], 2))
        ws_s1.cell(r, 8, round(tr["s1_lam_h"], 3))
        ws_s1.cell(r, 9, round(tr["s1_het_corr"], 4))
        ws_s1.cell(r, 10, round(tr["s1_raw_2026_h"], 1))
        ws_s1.cell(r, 11, round(tr["s1_r2_2026_h"], 1))
        ws_s1.cell(r, 12, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$C$5:$C$36)")
        ws_s1.cell(r, 13, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$K$5:$K$36)")
        for c in range(1, len(s1_hdrs) + 1):
            cell = ws_s1.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if i % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c == 1:
                cell.alignment = Alignment(horizontal="center")
            elif c <= 5 or c == 9:
                cell.number_format = "0.0000"
            elif c <= 8:
                cell.number_format = "0.00"
            else:
                cell.number_format = "#,##0.0"
    ws_s1.cell(13, 1, "Plant Total")
    for c in (10, 11, 12, 13):
        col_l = get_column_letter(c)
        ws_s1.cell(13, c, f"=SUM({col_l}5:{col_l}12)")
    for c in range(1, len(s1_hdrs) + 1):
        cell = ws_s1.cell(13, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c >= 10:
            cell.number_format = "#,##0.0"
    ws_s1.freeze_panes = "B5"
    _set_widths(ws_s1, [12, 11, 11, 11, 11, 15, 18, 15, 14, 16, 16, 15, 15])
    _setup_print(ws_s1, len(s1_hdrs), 13, repeat_row=4)

    # ==========================================================================
    # TAB 3: S2_TwoPath_Hydraulics
    # ==========================================================================
    ws_s2["A1"] = "Mode 2 (Clause 2.2): Variable-Flow Cumulative-Volume Two-Path DAF/DMF Hydraulic Mixing"
    ws_s2["A1"].font = S["title_font"]
    ws_s2["A2"] = "Profiled (f_fast, V_fast, V_main) on conservative ambient tidal seawater conductivity in cumulative flow Phi(t) = int Q dt."
    ws_s2["A2"].font = S["sub_font"]
    s2_hdrs = [
        "Train", "Nominal V_nom (m3)", "Fitted f_fast", "V_fast (m3)", "V_main (m3)",
        "2-Path Cond RMS", "1D Plug RMS", "Fixed-Lag RMS",
        "2026 Raw (h)", "2026 Lag (h)", "2026 1D Plug (h)",
        "2026 Golden (h)", "2027 Golden (h)",
    ]
    ws_s2.append([])
    ws_s2.append(s2_hdrs)
    _style_header_row(ws_s2, 4, len(s2_hdrs), S)
    for i, u in enumerate(core.TRAINS):
        r = 5 + i
        tr = res["train_rows"][u]
        ws_s2.cell(r, 1, u)
        ws_s2.cell(r, 2, int(round(tr["v_nom_m3"])))
        ws_s2.cell(r, 3, round(tr["s2_f_fast_hat"], 4))
        ws_s2.cell(r, 4, round(tr["s2_v_fast_hat"], 1))
        ws_s2.cell(r, 5, round(tr["s2_v_main_hat"], 1))
        ws_s2.cell(r, 6, round(tr["s2_cond_rms"], 4))
        ws_s2.cell(r, 7, round(tr["s2_sp_cond_rms"], 4))
        ws_s2.cell(r, 8, round(tr["s2_lag_cond_rms"], 4))
        ws_s2.cell(r, 9, round(tr["s2_raw_2026_h"], 1))
        ws_s2.cell(r, 10, round(tr["s2_lag_2026_h"], 1))
        ws_s2.cell(r, 11, round(tr["s2_sp_2026_h"], 1))
        ws_s2.cell(r, 12, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$D$5:$D$36)")
        ws_s2.cell(r, 13, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$L$5:$L$36)")
        for c in range(1, len(s2_hdrs) + 1):
            cell = ws_s2.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if i % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c == 1:
                cell.alignment = Alignment(horizontal="center")
            elif c == 2:
                cell.number_format = "#,##0"
            elif c == 3:
                cell.number_format = "0.0%"
            elif c in (6, 7, 8):
                cell.number_format = "0.000"
            else:
                cell.number_format = "#,##0.0"
    ws_s2.cell(13, 1, "Plant Total / Avg")
    for c in (6, 7, 8):
        col_l = get_column_letter(c)
        ws_s2.cell(13, c, f"=AVERAGE({col_l}5:{col_l}12)")
    for c in (9, 10, 11, 12, 13):
        col_l = get_column_letter(c)
        ws_s2.cell(13, c, f"=SUM({col_l}5:{col_l}12)")
    for c in range(1, len(s2_hdrs) + 1):
        cell = ws_s2.cell(13, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c in (6, 7, 8):
            cell.number_format = "0.000"
        elif c >= 9:
            cell.number_format = "#,##0.0"
    ws_s2.freeze_panes = "B5"
    _set_widths(ws_s2, [14, 15, 13, 12, 12, 15, 13, 14, 13, 13, 14, 14, 14])
    _setup_print(ws_s2, len(s2_hdrs), 13, repeat_row=4)

    # ==========================================================================
    # TAB 4: S3_KineticCIP_LCA
    # ==========================================================================
    ws_s3["A1"] = "Mode 3 (Clause 2.3): Continuous Post-CIP Fouling Re-Growth Kinetic Latent-Class Model"
    ws_s3["A1"].font = S["title_font"]
    ws_s3["A2"] = "Separating identical-emission reversible mineral crust (tau_min re-growth after CIP_ACID_pH2) and bio-fouling (after CIP_ALK_pH11) from persistent structural breaches."
    ws_s3["A2"].font = S["sub_font"]
    s3_hdrs = [
        "Train", "Fitted pi_min", "Fitted tau_min (h)", "Fitted pi_struct",
        "2026 Raw 2-of-3 (h)", "2026 R1 Uncond 3-Cl (h)", "2026 R2 Static 120h (h)",
        "2026 Golden (h)", "2027 Golden (h)",
    ]
    ws_s3.append([])
    ws_s3.append(s3_hdrs)
    _style_header_row(ws_s3, 4, len(s3_hdrs), S)
    for i, u in enumerate(core.TRAINS):
        r = 5 + i
        tr = res["train_rows"][u]
        ws_s3.cell(r, 1, u)
        ws_s3.cell(r, 2, round(tr["s3_pi_min_hat"], 4))
        ws_s3.cell(r, 3, round(tr["s3_tau_min_h"], 1))
        ws_s3.cell(r, 4, round(tr["s3_pi_s_hat"], 4))
        ws_s3.cell(r, 5, round(tr["s3_raw_2026_h"], 1))
        ws_s3.cell(r, 6, round(tr["s3_r1_2026_h"], 1))
        ws_s3.cell(r, 7, round(tr["s3_r2_2026_h"], 1))
        ws_s3.cell(r, 8, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$E$5:$E$36)")
        ws_s3.cell(r, 9, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$M$5:$M$36)")
        for c in range(1, len(s3_hdrs) + 1):
            cell = ws_s3.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if i % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c == 1:
                cell.alignment = Alignment(horizontal="center")
            elif c in (2, 4):
                cell.number_format = "0.00%"
            else:
                cell.number_format = "#,##0.0"
    ws_s3.cell(13, 1, "Plant Total")
    for c in (5, 6, 7, 8, 9):
        col_l = get_column_letter(c)
        ws_s3.cell(13, c, f"=SUM({col_l}5:{col_l}12)")
    for c in range(1, len(s3_hdrs) + 1):
        cell = ws_s3.cell(13, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c >= 5:
            cell.number_format = "#,##0.0"

    # Shared channel emission table
    ws_s3["A15"] = "Estimated Shared Inline Alarm Channel Emission Probabilities (D1, D2, D3)"
    ws_s3["A15"].font = S["sec_font"]
    em_hdrs = ["Latent State", "P(D1 Salt Passage)", "P(D2 Stage dP)", "P(D3 Acoustic Bypass)"]
    for c_i, h in enumerate(em_hdrs, 1):
        ws_s3.cell(16, c_i, h)
    _style_header_row(ws_s3, 16, 4, S, fill_key="subhdr_fill")
    tr1 = res["train_rows"]["TR01"]
    for idx_e, (nm, vec) in enumerate([
        ("Clean Baseline", tr1["s3_p_cl"]),
        ("Organic Bio-Fouling (CIP_ALK_pH11)", tr1["s3_p_fb"]),
        ("Mineral Crust (CIP_ACID_pH2) / Persistent Structural", tr1["s3_p_ms"]),
    ]):
        rr = 17 + idx_e
        ws_s3.cell(rr, 1, nm)
        for j in range(3):
            ws_s3.cell(rr, 2 + j, round(vec[j], 4))
        for c in range(1, 5):
            cell = ws_s3.cell(rr, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if c >= 2:
                cell.number_format = "0.000"
    ws_s3.freeze_panes = "B5"
    _set_widths(ws_s3, [34, 15, 16, 16, 18, 20, 20, 15, 15])
    _setup_print(ws_s3, len(s3_hdrs), 19, repeat_row=4)

    # ==========================================================================
    # TAB 5: S4_BayTDS_Deconv
    # ==========================================================================
    ws_s4["A1"] = "Mode 4 (Clause 2.4): Shared Bay Permeate Collector TDS Heteroscedastic Variance Deconvolution"
    ws_s4["A1"].font = S["title_font"]
    ws_s4["A2"] = "Quarterly flow-share OLS train means plus heteroscedastic Gaussian MLE removing 3.5 mg/L collector probe noise: Var(r_bay) = 3.5^2 + sum w_{u,t}^2 * sigma_u^2."
    ws_s4["A2"].font = S["sub_font"]
    s4_hdrs = [
        "Train", "Bay", "Q1 Mean (mg/L)", "Q2 Mean (mg/L)", "Q3 Mean (mg/L)", "Q4 Mean (mg/L)",
        "Heterosc SD (mg/L)", "Eq-Var SD (mg/L)",
        "2026 Direct Bay (h)", "2026 Eq-Var (h)", "2026 Golden (h)", "2027 Golden (h)",
    ]
    ws_s4.append([])
    ws_s4.append(s4_hdrs)
    _style_header_row(ws_s4, 4, len(s4_hdrs), S)
    for i, u in enumerate(core.TRAINS):
        r = 5 + i
        tr = res["train_rows"][u]
        mq = tr["s4_mu_q"]
        ws_s4.cell(r, 1, u)
        ws_s4.cell(r, 2, tr["bay"])
        for q in range(4):
            ws_s4.cell(r, 3 + q, round(mq[q], 2))
        ws_s4.cell(r, 7, round(tr["s4_sigma_hat"], 2))
        ws_s4.cell(r, 8, round(tr["s4_eq_sigma"], 2))
        ws_s4.cell(r, 9, round(tr["s4_raw_2026_h"], 1))
        ws_s4.cell(r, 10, round(tr["s4_eq_2026_h"], 1))
        ws_s4.cell(r, 11, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$F$5:$F$36)")
        ws_s4.cell(r, 12, f"=SUMIF(Operating_Plan_2027!$A$5:$A$36,A{r},Operating_Plan_2027!$N$5:$N$36)")
        for c in range(1, len(s4_hdrs) + 1):
            cell = ws_s4.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if i % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c <= 2:
                cell.alignment = Alignment(horizontal="center")
            elif c <= 8:
                cell.number_format = "0.00"
            else:
                cell.number_format = "#,##0.0"
    ws_s4.cell(13, 1, "Plant Total")
    ws_s4.cell(13, 2, "Both Bays")
    for c in (9, 10, 11, 12):
        col_l = get_column_letter(c)
        ws_s4.cell(13, c, f"=SUM({col_l}5:{col_l}12)")
    for c in range(1, len(s4_hdrs) + 1):
        cell = ws_s4.cell(13, c)
        cell.font = S["bold_font"]
        cell.fill = S["tot_fill"]
        cell.border = S["tot_border"]
        if c >= 9:
            cell.number_format = "#,##0.0"
    ws_s4.freeze_panes = "C5"
    _set_widths(ws_s4, [12, 10, 14, 14, 14, 14, 16, 15, 16, 15, 15, 15])
    _setup_print(ws_s4, len(s4_hdrs), 13, repeat_row=4)

    # ==========================================================================
    # TAB 6: Falsification_And_Routes
    # ==========================================================================
    ws_fal["A1"] = "Native-Unit Physical Falsification Checks (F1 to F4) and Competing Analytical Routes"
    ws_fal["A1"].font = S["title_font"]
    fal_g_c = res["fal_by_route"]["golden"]["combined"]
    fal_min_r = min(v["combined"] for k, v in res["fal_by_route"].items() if k != "golden")
    fal_max_r = max(v["combined"] for k, v in res["fal_by_route"].items() if k != "golden")
    ws_fal["A2"] = f"Direct validation against observed 2026 logs without anomaly labels: golden chi-squared = {fal_g_c:.2f} vs every rival {fal_min_r:.2f} to {fal_max_r:,.1f}."
    ws_fal["A2"].font = S["sub_font"]
    fal_hdrs = ["Model / Route", "F1 Boron Flux", "F2 Cond RMS (mS/cm)", "F3 CIP D3 (pp)", "F4 Bay TDS SD (mg/L)", "Combined Chi2", "vs Golden"]
    ws_fal.append([])
    ws_fal.append(fal_hdrs)
    _style_header_row(ws_fal, 4, len(fal_hdrs), S)
    fal_order = [
        ("Golden (All 4 Physical Models)", "golden"),
        ("S2 1D Single-Plug V_eff (Shortcut)", "S2_single_plug"),
        ("S1 Over-Correction (Flux i.i.d. sqrt(m))", "S1_over"),
        ("S3 Static 120h Post-CIP 4-Class EM", "S3_r2_120h"),
        ("S1 Homoscedastic (a + c/Q) AR(1)", "S1_r2_homosc"),
        ("S4 OLS + Equal-Variance Bay Pooling", "S4_eq_var"),
        ("S3 Unconditioned 3-Class LCA", "S3_r1_uncond"),
        ("S4 Unweighted Residual Inflation", "S4_over"),
        ("S2 Fixed Wall-Clock Lag TEP->Stress", "S2_r12_lag"),
        ("S3 Unanimous 3-of-3 Alarms (Over)", "S3_over"),
        ("Rigorous R2 (Exact 3.5h Frontier Solver)", "rigorous_r2"),
        ("Rigorous R1 (Exact 3.5h Frontier Solver)", "rigorous_r1"),
        ("S2 Comonotonic Upper Bound (Over)", "S2_over"),
        ("Generous Run Route (All Over)", "generous"),
        ("Cutoff Run Route", "cutoff"),
        ("Hedge Run Route (80/20 Blend)", "hedge"),
        ("Direct / Reflex (Raw Monitoring)", "direct"),
    ]
    for i, (lbl, key) in enumerate(fal_order):
        r = 5 + i
        fv = res["fal_by_route"][key]
        ws_fal.cell(r, 1, lbl)
        ws_fal.cell(r, 2, round(fv["f1"], 4))
        ws_fal.cell(r, 3, round(fv["f2_ms_cm"], 4))
        ws_fal.cell(r, 4, round(fv["f3_pp"], 3))
        ws_fal.cell(r, 5, round(fv["f4_mg_l"], 3))
        ws_fal.cell(r, 6, round(fv["combined"], 3))
        ws_fal.cell(r, 7, f"=F{r}/$F$5")
        for c in range(1, 8):
            cell = ws_fal.cell(r, c)
            cell.font = S["bold_font"] if i == 0 else S["body_font"]
            cell.border = S["border"]
            if i == 0:
                cell.fill = S["mo_fill"]
            elif i % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c == 2:
                cell.number_format = "0.000"
            elif c in (3, 4, 5):
                cell.number_format = "0.00"
            elif c == 6:
                cell.number_format = "#,##0.00"
            elif c == 7:
                cell.number_format = '0.0"x"'
    ws_fal.freeze_panes = "B5"
    _set_widths(ws_fal, [40, 15, 19, 15, 20, 15, 12])
    _setup_print(ws_fal, len(fal_hdrs), 4 + len(fal_order), repeat_row=4)

    # ==========================================================================
    # TAB 8: Sensitivity_And_QA_2026
    # ==========================================================================
    ws_sens["A1"] = f"{n_var}-Variant Estimator Convergence, 8-Way +/-20% Forcing, and 2026 Layer 1 QA Audit"
    ws_sens["A1"].font = S["title_font"]
    ws_sens["A2"] = "Every honest physical specification across S1, S2, S3, and S4 and every +/-20% mode perturbation preserves the exact 5-of-8 overhaul slate."
    ws_sens["A2"].font = S["sub_font"]

    v_hdrs = ["Variant", "TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08", "Total (h)", "Energy (MWh)", "Call Holds"]
    ws_sens.append([])
    ws_sens.append(v_hdrs)
    _style_header_row(ws_sens, 4, len(v_hdrs), S)
    g_sl = res["golden_slate"]
    for i, (nm, asm) in enumerate([("Golden_Base", res["gold_asm"])] + res["variants_named"]):
        r = 5 + i
        sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
        ws_sens.cell(r, 1, nm)
        for ui, u in enumerate(core.TRAINS):
            ws_sens.cell(r, 2 + ui, round(asm["members"][u], 1))
        ws_sens.cell(r, 10, round(asm["A_total_2027"], 1))
        ws_sens.cell(r, 11, round(asm["A_energy_mwh"], 1))
        ws_sens.cell(r, 12, "YES" if sl == g_sl else "NO")
        for c in range(1, 13):
            cell = ws_sens.cell(r, c)
            cell.font = S["bold_font"] if i == 0 else S["body_font"]
            cell.border = S["border"]
            if i == 0:
                cell.fill = S["call_fill"]
            elif i % 2 == 1:
                cell.fill = S["zebra_fill"]
            if c == 12:
                cell.alignment = Alignment(horizontal="center")
            elif c >= 2:
                cell.number_format = "#,##0.0"

    p_start = 5 + len(res["variants_named"]) + 3
    ws_sens.cell(p_start - 1, 1, "8-Way Independent +/-20% Mode Forcing Perturbations").font = S["sec_font"]
    p_hdrs = ["Perturbation", "Min Overhaul (h)", "Max Monitor (h)", "Call Holds", "Overhaul Slate"]
    for c_i, h in enumerate(p_hdrs, 1):
        ws_sens.cell(p_start, c_i, h)
    _style_header_row(ws_sens, p_start, 5, S, fill_key="subhdr_fill")
    for idx_p, pt in enumerate(res["perturbations"]):
        r = p_start + 1 + idx_p
        ws_sens.cell(r, 1, pt["input"])
        ws_sens.cell(r, 2, pt["min_overhaul"])
        ws_sens.cell(r, 3, pt["max_monitor"])
        ws_sens.cell(r, 4, "YES" if pt["holds"] else "NO")
        ws_sens.cell(r, 5, ", ".join(pt["answer"]))
        for c in range(1, 6):
            cell = ws_sens.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if c in (2, 3):
                cell.number_format = "#,##0.0"
            elif c == 4:
                cell.alignment = Alignment(horizontal="center")

    q_start = p_start + len(res["perturbations"]) + 3
    ws_sens.cell(q_start - 1, 1, "2026 Multi-Grain Data Hygiene & Control Totals (15 Shipped Files)").font = S["sec_font"]
    q_hdrs = ["Dataset / Check", "Raw Rows", "Clean Rows", "Dropped / Converted"]
    for c_i, h in enumerate(q_hdrs, 1):
        ws_sens.cell(q_start, c_i, h)
    _style_header_row(ws_sens, q_start, 4, S, fill_key="subhdr_fill")
    cl = res["cleaning"]
    qa_rows = [
        ("permeate_boron_composites_2026.csv", cl["boron_raw_rows"], cl["boron_clean_rows"], f"{cl['boron_superseded_dropped']} superseded rev-1; {cl['boron_ug_rows']} ug/L; {cl['boron_dmy_rows']} DD/MM/YYYY"),
        ("intake_chemistry_15m_2026.csv", cl["intake_raw_rows"], cl["intake_clean_rows"], f"{cl['intake_dups_dropped']} exact retry frames"),
        ("ro_feed_header_15m_2026.csv", cl["ro_feed_raw_rows"], cl["ro_feed_clean_rows"], f"{cl['ro_feed_dups_dropped']} exact retry frames"),
        ("train_hydraulics_hourly_2026.csv", cl["hydraulics_raw_rows"], cl["hydraulics_clean_rows"], f"{cl['hydraulics_dups_dropped']} retries; {cl['hydraulics_ls_rows']} L/s converted"),
        ("bay_permeate_tds_hourly_2026.csv", cl["bay_tds_raw_rows"], cl["bay_tds_clean_rows"], f"{cl['bay_tds_dups_dropped']} exact PLC retries"),
        ("shift_diagnostics_2026.csv", cl["shift_rows"], cl["shift_rows"], "Europe/Lisbon aligned to 1h UTC grid"),
        ("cip_wash_log_2026.csv", cl["cip_rows"], cl["cip_rows"], f"{cl['cip_alk_washes']} ALK / {cl['cip_acid_washes']} ACID ({cl['cip_carryover_2025']} late-Dec 2025 carryover)"),
    ]
    for idx_q, (nm, rr, cr, note) in enumerate(qa_rows):
        r = q_start + 1 + idx_q
        ws_sens.cell(r, 1, nm)
        ws_sens.cell(r, 2, rr)
        ws_sens.cell(r, 3, cr)
        ws_sens.cell(r, 4, note)
        for c in range(1, 5):
            cell = ws_sens.cell(r, c)
            cell.font = S["body_font"]
            cell.border = S["border"]
            if c in (2, 3):
                cell.number_format = "#,##0"
    ws_sens.freeze_panes = "B5"
    _set_widths(ws_sens, [34, 10, 10, 10, 10, 10, 10, 10, 10, 12, 13, 12])
    _setup_print(ws_sens, 12, q_start + len(qa_rows), repeat_row=4)

    xlsx_path = os.path.join(golden_dir, GOLDEN_XLSX)
    wb.save(xlsx_path)
    postprocess.normalize_ooxml(
        xlsx_path,
        PK.PEOPLE["lead"],
        PK.PEOPLE["lead"],
        "2027-01-16T09:15:00Z",
        "2027-01-17T16:40:22Z",
        excel=True,
        company=PK.ORG,
    )
    return xlsx_path


def build_goldens_and_zips(task_dir, res=None):
    target_dir = os.path.join(task_dir, "target")
    golden_dir = os.path.join(task_dir, "golden")
    if res is None:
        res = AN.run_all(target_dir)
    if os.path.isdir(golden_dir):
        shutil.rmtree(golden_dir)
    os.makedirs(golden_dir)

    csv_path, ordered = write_csv(golden_dir, res)
    xlsx_path = write_workbook(golden_dir, res, ordered)
    postprocess.own_mtimes(
        golden_dir,
        {
            GOLDEN_CSV: dt.datetime(2027, 1, 17, 16, 44, 18, tzinfo=UTC),
            GOLDEN_XLSX: dt.datetime(2027, 1, 17, 16, 40, 22, tzinfo=UTC),
        },
    )
    t_zip = os.path.join(task_dir, "target.zip")
    g_zip = os.path.join(task_dir, "golden.zip")
    postprocess.zip_folder(target_dir, t_zip)
    postprocess.zip_folder(golden_dir, g_zip)
    return {"csv": csv_path, "xlsx": xlsx_path, "target_zip": t_zip, "golden_zip": g_zip}


if __name__ == "__main__":
    tdir = os.path.dirname(HERE)
    print(build_goldens_and_zips(tdir))
