"""Build the two golden deliverables strictly from figures.json (v3):
1. vesterdal_substation_conformed_2026.csv - one row per in-scope substation holding conformed 2026 peak metrics
   and the assigned 2027-2029 relief phase.
2. vesterdal_relief_schedule_2027_2029.xlsx - opens on Relief_Schedule with the Final Recommendation, live
   formula-driven conformed substation schedule, pool aggregates, and an embedded horizontal bar chart comparing
   Firm N-1 Loading % across substations, followed by Critical_Components, Physics_Validation, Routes_Comparison,
   and Variant_Battery tabs.
"""
import csv
import os
import re
import zipfile
from xml.sax.saxutils import escape as xml_escape

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import pack as PK

FILES = {
    "csv": "vesterdal_substation_conformed_2026.csv",
    "wb": "vesterdal_relief_schedule_2027_2029.xlsx",
}

HEAD_FILL = PatternFill("solid", fgColor="1F3B5C")
P1_FILL = PatternFill("solid", fgColor="F5D5D2")
P2_FILL = PatternFill("solid", fgColor="FAE9C8")
DEF_FILL = PatternFill("solid", fgColor="D9ECD8")
TOT_FILL = PatternFill("solid", fgColor="EEF2F7")
PARAM_FILL = PatternFill("solid", fgColor="F2F5F9")
THIN = Side(style="thin", color="B8BEC8")
MED = Side(style="medium", color="1F3B5C")


def _hdr(ws, row, ncols, height=34):
    for c in ws[row][:ncols]:
        c.font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
        c.fill = HEAD_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(bottom=MED)
    ws.row_dimensions[row].height = height


def _widths(ws, widths):
    for i, w in enumerate(widths):
        col = chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)
        ws.column_dimensions[col].width = w
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = 9
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0


def _write_csv(out_dir, fig):
    path = os.path.join(out_dir, FILES["csv"])
    targets = fig["targets"]
    ordered = sorted(targets, key=lambda s: -fig["substations"][s]["loading_pct_raw"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "substation_id", "firm_n1_mva", "scada_60min_peak_mw", "peak_15min_active_mw",
            "peak_hour_reactive_mvar", "peak_limiting_phase_share_pct",
            "peak_15min_limiting_phase_mva", "firm_n1_loading_pct",
            "relief_capacity_needed_mva", "assigned_relief_phase",
        ])
        for s in ordered:
            rec = fig["substations"][s]
            w.writerow([
                s,
                f"{rec['firm_n1_mva']:.1f}",
                f"{rec['p60_peak_mw']:.2f}",
                f"{rec['p15_peak_mw']:.2f}",
                f"{rec['q_peak_h_mvar']:.2f}",
                f"{rec['w_max_pct']:.2f}",
                f"{rec['lim_mva']:.2f}",
                f"{rec['loading_pct']:.2f}",
                f"{rec['relief_mva']:.2f}",
                rec["phase"],
            ])


def _sheet_schedule(wb, fig, cache):
    ws = wb.active
    ws.title = "Relief_Schedule"
    sc = cache.setdefault("xl/worksheets/sheet1.xml", {})
    g_p1 = fig["schedule_groups"]["phase1"]
    g_p2 = fig["schedule_groups"]["phase2"]
    g_df = fig["schedule_groups"]["defer"]
    p1 = ", ".join(g_p1)
    p2 = ", ".join(g_p2)
    df = ", ".join(g_df)
    ws["A1"] = (f"2027-2029 Firm-Capacity Relief Schedule: Phase 1 (2027) = {p1}; "
                f"Phase 2 (2028-2029) = {p2}; Defer = {df} (Total Relief = {fig['total_relief_mva']:.2f} MVA)")
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws["A2"] = (f"Vesterdal Nett AS | Network Planning Standard NS-2026 (Phase 1 >= 100%, Phase 2 >= 85%, "
                f"Relief above 85% Firm N-1 MVA) | Prepared by {PK.PEOPLE['analyst']}, 20 January 2027")
    ws["A2"].font = Font(italic=True, size=9, color="555555", name="Calibri")

    ws["A3"] = (f"Conformed pool components across the seven in-scope substations: combined 15-minute active demand = "
                f"{fig['c1_total_p15_mw']:.2f} MW (band {fig['c1_band'][0]:.1f} to {fig['c1_band'][1]:.1f} MW), "
                f"combined peak-hour reactive demand = {fig['c2_total_qpeak_mvar']:.2f} MVAr "
                f"(band {fig['c2_band'][0]:.1f} to {fig['c2_band'][1]:.1f} MVAr), average peak limiting-phase share = "
                f"{fig['c3_mean_lim_phase_pct']:.2f}% (band {fig['c3_band'][0]:.2f}% to {fig['c3_band'][1]:.2f}%), "
                f"and total relief capacity needed = {fig['total_relief_mva']:.2f} MVA "
                f"(band {fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA). "
                f"Fossheim, Lindberg, Ostervik, and Solberg completed 2023-2024 bay modernization and are excluded from the 2027-2029 relief pool.")
    ws["A3"].font = Font(size=9, color="333333", name="Calibri")
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:J3")
    ws.row_dimensions[3].height = 42

    hdr = [
        "Substation", "Firm N-1 Rating (MVA)", "60-Min SCADA Peak (MW)", "Peak 15-Min Active (MW)",
        "Peak-Hour Reactive (MVAr)", "Limiting-Phase Share (%)", "Peak 15-Min Lim-Phase (MVA)",
        "Firm N-1 Loading (%)", "Relief Needed (MVA)", "2027-2029 Relief Phase",
    ]
    ws.append([])
    ws.append(hdr)
    _hdr(ws, 5, len(hdr), 38)

    ordered = sorted(fig["targets"], key=lambda s: -fig["substations"][s]["loading_pct_raw"])
    for idx, s in enumerate(ordered):
        r = fig["substations"][s]
        row = 6 + idx
        ws.append([
            s,
            r["firm_n1_mva"],
            r["p60_peak_mw_raw"],
            r["p15_peak_mw_raw"],
            r["q_peak_h_mvar_raw"],
            r["w_max_pct_raw"],
            f"=3*(F{row}/100)*SQRT(D{row}^2+E{row}^2)",
            f"=100*G{row}/B{row}",
            f"=MAX(0,G{row}-0.85*B{row})",
            f'=IF(H{row}>=100,"Phase 1 (2027)",IF(H{row}>=85,"Phase 2 (2028-2029)","Defer"))',
        ])
        sc[f"G{row}"] = r["lim_mva_raw"]
        sc[f"H{row}"] = r["loading_pct_raw"]
        sc[f"I{row}"] = r["relief_mva_raw"]
        sc[f"J{row}"] = r["phase"]

        ws.cell(row=row, column=2).number_format = "0.0"
        for col in (3, 4, 5, 6, 7, 8, 9):
            ws.cell(row=row, column=col).number_format = "0.00"
        ws.cell(row=row, column=10).alignment = Alignment(horizontal="center")
        fill = P1_FILL if "Phase 1" in r["phase"] else (P2_FILL if "Phase 2" in r["phase"] else DEF_FILL)
        ws.cell(row=row, column=10).fill = fill
        ws.cell(row=row, column=8).fill = fill

    tot_row = 6 + len(ordered)
    end_row = tot_row - 1
    ws.append([
        "In-Scope Pool Total / Avg",
        f"=SUM(B6:B{end_row})",
        f"=SUM(C6:C{end_row})",
        f"=SUM(D6:D{end_row})",
        f"=SUM(E6:E{end_row})",
        f"=AVERAGE(F6:F{end_row})",
        f"=SUM(G6:G{end_row})",
        None,
        f"=SUM(I6:I{end_row})",
        f"{len(g_p1)} Phase 1 / {len(g_p2)} Phase 2 / {len(g_df)} Defer",
    ])
    sc[f"B{tot_row}"] = sum(fig["substations"][s]["firm_n1_mva"] for s in ordered)
    sc[f"C{tot_row}"] = sum(fig["substations"][s]["p60_peak_mw_raw"] for s in ordered)
    sc[f"D{tot_row}"] = sum(fig["substations"][s]["p15_peak_mw_raw"] for s in ordered)
    sc[f"E{tot_row}"] = sum(fig["substations"][s]["q_peak_h_mvar_raw"] for s in ordered)
    sc[f"F{tot_row}"] = sum(fig["substations"][s]["w_max_pct_raw"] for s in ordered) / len(ordered)
    sc[f"G{tot_row}"] = sum(fig["substations"][s]["lim_mva_raw"] for s in ordered)
    sc[f"I{tot_row}"] = sum(fig["substations"][s]["relief_mva_raw"] for s in ordered)

    for col in range(1, 11):
        c = ws.cell(row=tot_row, column=col)
        c.font = Font(bold=True, name="Calibri", size=10)
        c.fill = TOT_FILL
        c.border = Border(top=THIN, bottom=MED)
    ws.cell(row=tot_row, column=2).number_format = "0.0"
    for col in (3, 4, 5, 6, 7, 9):
        ws.cell(row=tot_row, column=col).number_format = "0.00"
    ws.cell(row=tot_row, column=10).alignment = Alignment(horizontal="center")

    chart = BarChart()
    chart.type = "bar"
    chart.style = 10
    chart.title = "2026 Conformed Firm N-1 Loading (%) by In-Scope Substation"
    chart.x_axis.title = "Substation"
    chart.y_axis.title = "Firm N-1 Loading (%)"
    chart.x_axis.axPos = "l"
    chart.y_axis.axPos = "b"
    chart.legend = None
    data_ref = Reference(ws, min_col=8, min_row=5, max_row=5 + len(ordered))
    cats_ref = Reference(ws, min_col=1, min_row=6, max_row=5 + len(ordered))
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.width = 20
    chart.height = 11
    ws.add_chart(chart, "A16")
    _widths(ws, [22, 16, 16, 16, 17, 16, 18, 16, 16, 30])


ROUTE_LABELS = {
    "golden": "Conformed Physics Model (Golden)",
    "S1": "60-Min SCADA Active (No 15-Min Coincidence)",
    "S2": "Annual Net kVARh PF (No 66 kV Corridor Inversion)",
    "S3": "AMI-Only Balanced Remainder (No Multi-Class Bus Sag)",
    "S1+S2": "60-Min SCADA + Net kVARh PF",
    "S1+S3": "60-Min SCADA + AMI-Only Balanced",
    "S2+S3": "Net kVARh PF + AMI-Only Balanced",
    "S1+S2+S3": "Baseline Operational (SCADA 60m + Net kVARh + AMI)",
    "reflex": "Baseline Operational (SCADA 60m + Net kVARh + AMI)",
    "direct": "Raw Operational Logs (SCADA 60m + Net kVARh + Balanced)",
    "rigorous": "Standard Utility Planning (Pooled CF + Winter Q(P) + AMI)",
    "response1_v2": "Register-Rho + Monthly Q(P) + Scalar Bus-Sag OLS",
    "run_generous": "Conservative Upper (Linear Sum + Class PF + Evening OLS)",
    "run_calibrated": "Parametric Proxy (Register-Rho + Winter Q(P) + Manual PF)",
    "run_hedge": "Uncorrelated Baseline (Indep Quad + Net kVARh + AMI)",
    "run_cutoff": "Window-Sliced Proxy (1-PC + Winter kVARh + Evening OLS)",
    "s1_scada60": "S1: 60-Min SCADA Peak (No 15-Min Uplift)",
    "s1_register_rho": "S1: 12-Month Register Ratio Correlation",
    "s1_pca1": "S1: 1-Mode Regional Stripping",
    "s1_pca2": "S1: 2-Mode Regional Stripping",
    "s1_raw_corr": "S1: Raw Unstripped Hourly Feeder Correlation",
    "s1_indep_quad": "S1: Independent Feeder Quadrature",
    "s1_cf_pooled": "S1: Pooled Register Coincidence Factor",
    "s1_flat_ratio": "S1: Flat Commissioning Peak Ratio",
    "s1_linear_sum": "S1: Additive Feeder Ratio Sum",
    "s2_net_kvarh": "S2: Annual Net kVARh Power Factor",
    "s2_winter_kvarh": "S2: Winter-Only Net kVARh Power Factor",
    "s2_monthly_qp": "S2: Monthly Linear Q(P) Regression",
    "s2_monthly_win": "S2: Monthly Q(P + Winter Indicator)",
    "s2_monthly_quad": "S2: Monthly Quadratic Q(P^2)",
    "s2_class_pf": "S2: Engineering Manual Class Nominal PFs",
    "s2_targets_only": "S2: Corridor Inversion Dropping Upstream Hubs",
    "s2_local_dv": "S2: Local Single-Site GSP Voltage Drop",
    "s2_rp_only": "S2: 66 kV R*P-Only Drop (No X*Q Coupling)",
    "s2_raw_dv": "S2: Un-Demeaned Corridor dV (No PT Calibration)",
    "s3_gis": "S3: Uncorrected GIS Lateral Phase Tags",
    "s3_ami_only": "S3: Partial 20/40 AMI + Balanced Remainder",
    "s3_ami_plus_gis": "S3: AMI Phases + GIS on Legacy Laterals",
    "s3_ami_grossup": "S3: Partial AMI Grossed Up 40/20",
    "s3_scalar_ols": "S3: Scalar Bus-Sag OLS (dV_ph ~ P_tot)",
    "s3_evening_cut": "S3: Evening 17-21h Bus-Sag OLS (Mean Z)",
    "s3_even_zres": "S3: Evening 17-21h Bus-Sag OLS (Res Z)",
    "s3_handbook_pf": "S3: Multi-Class Bus-Sag OLS (Manual PF)",
    "s3_sub_pf": "S3: Multi-Class Bus-Sag OLS (Substation PF)",
    "s3_raw_vbus": "S3: Raw Bus Voltage Difference (No PT Removal)",
}


def _sheet_components(wb, fig, cache):
    ws = wb.create_sheet("Critical_Components")
    sc = cache.setdefault("xl/worksheets/sheet2.xml", {})
    n_var = len(fig["variants"])
    ws["A1"] = f"Critical Components & Conformed Substation Bands ({n_var}-Variant Battery)"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws.append([])
    ws.append(["Component / Metric", "Conformed Value", "Band Low", "Band High",
               "Operational Baseline", "Standard Utility Proxy", "Units"])
    _hdr(ws, 3, 7, 30)
    rf = fig["routes"]["S1+S2+S3"]
    rg = fig["routes"]["rigorous"]
    targets = fig["targets"]
    c1_raw = sum(fig["substations"][s]["p15_peak_mw_raw"] for s in targets)
    c2_raw = sum(fig["substations"][s]["q_peak_h_mvar_raw"] for s in targets)
    c3_raw = sum(fig["substations"][s]["w_max_pct_raw"] for s in targets) / len(targets)
    rel_raw = sum(fig["substations"][s]["relief_mva_raw"] for s in targets)
    rows = [
        ("C1: Pool Combined 15-Min Active Demand", "=Relief_Schedule!D13", c1_raw,
         fig["c1_band"][0], fig["c1_band"][1], rf["c1_total_p15_mw"], rg["c1_total_p15_mw"], "MW"),
        ("C2: Pool Combined Peak-Hour Reactive Demand", "=Relief_Schedule!E13", c2_raw,
         fig["c2_band"][0], fig["c2_band"][1], rf["c2_total_qpeak_mvar"], rg["c2_total_qpeak_mvar"], "MVAr"),
        ("C3: Pool Average Limiting-Phase Share", "=Relief_Schedule!F13", c3_raw,
         fig["c3_band"][0], fig["c3_band"][1], rf["c3_mean_lim_phase_pct"], rg["c3_mean_lim_phase_pct"], "%"),
        ("Total Relief Capacity Needed", "=Relief_Schedule!I13", rel_raw,
         fig["total_relief_band"][0], fig["total_relief_band"][1], rf["total_relief_mva"], rg["total_relief_mva"], "MVA"),
    ]
    for label, formula, val_raw, blo, bhi, vrf, vrg, unit in rows:
        ws.append([label, formula, blo, bhi, vrf, vrg, unit])
        ri = ws.max_row
        sc[f"B{ri}"] = val_raw
        for c in range(2, 7):
            ws.cell(row=ri, column=c).number_format = "0.00"
        ws.cell(row=ri, column=7).alignment = Alignment(horizontal="center")

    ws.append([])
    ws.append(["Substation", "P15 MW (Band)", "Q_peak MVAr (Band)", "Lim-Phase % (Band)",
               "Lim-Phase MVA (Band)", "Firm Loading % (Band)", "Assigned Phase"])
    _hdr(ws, ws.max_row, 7, 30)
    b = fig["bands"]
    for s in fig["targets"]:
        rec = fig["substations"][s]
        ws.append([
            s,
            f"{rec['p15_peak_mw']:.2f} ({b['p15_mw'][s][0]:.2f} to {b['p15_mw'][s][1]:.2f})",
            f"{rec['q_peak_h_mvar']:.2f} ({b['q_peak_mvar'][s][0]:.2f} to {b['q_peak_mvar'][s][1]:.2f})",
            f"{rec['w_max_pct']:.2f} ({b['w_max_pct'][s][0]:.2f} to {b['w_max_pct'][s][1]:.2f})",
            f"{rec['lim_mva']:.2f} ({b['lim_mva'][s][0]:.2f} to {b['lim_mva'][s][1]:.2f})",
            f"{rec['loading_pct']:.2f} ({b['loading_pct'][s][0]:.1f} to {b['loading_pct'][s][1]:.1f})",
            rec["phase"],
        ])
    _widths(ws, [44, 22, 22, 22, 22, 22, 20])


def _sheet_physics(wb, fig, cache):
    ws = wb.create_sheet("Physics_Validation")
    sc = cache.setdefault("xl/worksheets/sheet3.xml", {})
    ws["A1"] = "Internal Physics-Balance Validation (Sep-Oct Commissioning Surge, 66 kV/LV Voltages, kVARh, 3-Ph Bus Sag & AMI)"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    rp = fig["ref_params"]
    ws["A2"] = (f"No target-site 15-min PQ, reactive Q, or 3-phase main-bay archive is shipped. Every estimator is checked against "
                f"Sep-Oct active commissioning surges on Fossheim & Lindberg, 66 kV/22 kV voltage conservation (22 kV bus basis, V), "
                f"12-month kVARh balance, 3-phase bus-sag RMSE (V), and AMI q_kvar consistency (AMI tracer check: "
                f"{rp['tracer_matched']}/{rp['tracer_total']} = 100.0% vs GIS {rp['gis_tracer_pct']:.1f}%).")
    ws["A2"].font = Font(italic=True, size=9, color="444444", name="Calibri")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 32

    ws.append([
        "k_ord (Sep-Oct)", rp["k_ord_raw"], "AMI tan_phi_res", rp["tan_phi_res_raw"],
        "AMI tan_phi_com", rp["tan_phi_com_raw"], "Drangvik R_off (pca4)", rp["rho_sync_drangvik"],
        "Malmnes R_off (pca4)", rp["rho_stag_malmnes"], f"Reg rho: {rp['reg_rho_drangvik']:.2f} vs {rp['reg_rho_malmnes']:.2f}",
    ])
    for col in range(1, 12):
        c = ws.cell(row=3, column=col)
        c.fill = PARAM_FILL
        c.border = Border(top=THIN, bottom=THIN)
        c.font = Font(bold=(col % 2 == 1), name="Calibri", size=9, color="1F3B5C" if col % 2 == 1 else "000000")
        if col in (2, 4, 6, 8, 10):
            c.number_format = "0.0000"

    ws.append([])
    ws.append(["Estimation Method", "Sep-Oct Surge MAE (MW)", "LV Bus Balance RMSE (V)",
               "12-Mo kVARh Err (MVAr)", "3-Ph Bus Sag RMSE (V)", "AMI q_kvar RMSE (kVAr)",
               "Composite Physics Index", "Multiple of Conformed"])
    _hdr(ws, 5, 8, 34)
    pd_map = fig["phys_details"]
    ordered_keys = ["golden"] + sorted([k for k in pd_map if k != "golden"], key=lambda k: pd_map[k]["phys_idx"])
    gold_row = 6
    g_d = pd_map["golden"]
    g_comp = (g_d["s1_comm_mae_mw"] / 0.35) + (g_d["s2_vlv_rmse_v"] / 8.0) + (g_d["s2_kvarh_err_mvar"] / 0.40) + (g_d["s3_bus_rmse_v"] / 2.5) + (g_d["s3_ami_q_rmse_kvar"] / 2.5)
    for k in ordered_keys:
        d = pd_map[k]
        ri = ws.max_row + 1
        ws.append([
            ROUTE_LABELS.get(k, k), d["s1_comm_mae_mw"], d["s2_vlv_rmse_v"], d["s2_kvarh_err_mvar"],
            d["s3_bus_rmse_v"], d["s3_ami_q_rmse_kvar"],
            f"=(B{ri}/0.35)+(C{ri}/8)+(D{ri}/0.4)+(E{ri}/2.5)+(F{ri}/2.5)",
            f"=G{ri}/$G${gold_row}",
        ])
        comp_val = (d["s1_comm_mae_mw"] / 0.35) + (d["s2_vlv_rmse_v"] / 8.0) + (d["s2_kvarh_err_mvar"] / 0.40) + (d["s3_bus_rmse_v"] / 2.5) + (d["s3_ami_q_rmse_kvar"] / 2.5)
        sc[f"G{ri}"] = comp_val
        sc[f"H{ri}"] = comp_val / g_comp
        for c in (2, 3, 4, 5, 6, 7):
            ws.cell(row=ri, column=c).number_format = "0.00"
        ws.cell(row=ri, column=8).number_format = '0.0"x"'
    _widths(ws, [50, 20, 22, 20, 20, 20, 20, 18, 16, 16, 22])


def _sheet_routes(wb, fig):
    ws = wb.create_sheet("Routes_Comparison")
    ws["A1"] = "Comparison of Conformed Physics Model vs Single-Component Ablations & Alternative Proxies"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws.append([])
    hdr = ["Estimation Method", "Misplaced / 7", "C1 P15 (MW)", "C2 Q (MVAr)", "C3 w_max (%)", "Total Relief (MVA)", "Physics Idx"] + [
        f"{s} Load %" for s in fig["targets"]
    ]
    ws.append(hdr)
    _hdr(ws, 3, len(hdr), 34)
    order = [
        "golden", "S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3",
        "direct", "rigorous", "response1_v2", "run_generous", "run_calibrated", "run_hedge", "run_cutoff",
        "s1_register_rho", "s1_pca1", "s1_raw_corr", "s1_indep_quad", "s1_cf_pooled", "s1_flat_ratio", "s1_linear_sum",
        "s2_winter_kvarh", "s2_monthly_qp", "s2_monthly_win", "s2_class_pf", "s2_targets_only", "s2_local_dv", "s2_rp_only", "s2_raw_dv",
        "s3_gis", "s3_ami_plus_gis", "s3_ami_grossup", "s3_scalar_ols", "s3_evening_cut", "s3_even_zres", "s3_handbook_pf", "s3_sub_pf",
    ]
    for rname in order:
        if rname not in fig["routes"]:
            continue
        r = fig["routes"][rname]
        ws.append([
            ROUTE_LABELS.get(rname, rname), r["wrong_count"], r["c1_total_p15_mw"], r["c2_total_qpeak_mvar"], r["c3_mean_lim_phase_pct"],
            r["total_relief_mva"], r["phys_idx"],
        ] + [r["loading_pct"][s] for s in fig["targets"]])
        ri = ws.max_row
        ws.cell(row=ri, column=2).alignment = Alignment(horizontal="center")
        for c in range(3, len(hdr) + 1):
            ws.cell(row=ri, column=c).number_format = "0.00"
    _widths(ws, [50, 12, 13, 13, 13, 16, 13] + [13] * len(fig["targets"]))


def _sheet_variants(wb, fig):
    ws = wb.create_sheet("Variant_Battery")
    n_var = len(fig["variants"])
    ws["A1"] = f"{n_var}-Variant Honest Modeling Battery & +/-20% Forcing Perturbations"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws.append([])
    hdr = ["Variant / Perturbation", "Schedule Holds", "C1 P15 (MW)", "C2 Q (MVAr)", "C3 w_max (%)",
           "Total Relief (MVA)"] + [f"{s} %" for s in fig["targets"]]
    ws.append(hdr)
    _hdr(ws, 3, len(hdr), 32)
    for v in fig["variants"]:
        ws.append([
            v["name"], "YES" if v["holds"] else "NO", v["c1_total_p15_mw"], v["c2_total_qpeak_mvar"],
            v["c3_mean_lim_phase_pct"], v["total_relief_mva"],
        ] + [v["loading_pct"][s] for s in fig["targets"]])
        ri = ws.max_row
        for c in range(3, len(hdr) + 1):
            ws.cell(row=ri, column=c).number_format = "0.00"
    ws.append([])
    ws.append(["Forcing Perturbation", "Schedule Holds", "", "", "", ""] + [f"{s} %" for s in fig["targets"]])
    _hdr(ws, ws.max_row, len(hdr), 30)
    for p in fig["forcing"]:
        ws.append([p["input"], "YES" if p["holds"] else "NO", None, None, None, None] +
                  [p["loading_pct"][s] for s in fig["targets"]])
        ri = ws.max_row
        for c in range(7, len(hdr) + 1):
            ws.cell(row=ri, column=c).number_format = "0.00"
    _widths(ws, [44, 14, 13, 13, 13, 16] + [11] * len(fig["targets"]))


def _inject_caches_and_fix_chart(xlsx_path, cache):
    """Deterministically inject cached <v> results into every formula cell and fix <c:cat><c:numRef> -> <c:strRef>."""
    cell_pat = re.compile(r'<c r="([A-Z]+\d+)"([^>]*)>(<f[^>]*>.*?</f>)(?:<v>.*?</v>)?</c>')
    with zipfile.ZipFile(xlsx_path, "r") as zin:
        items = [(zi.filename, zin.read(zi.filename)) for zi in zin.infolist()]
    new_items = []
    for name, data in items:
        if name in cache:
            cmap = cache[name]
            txt = data.decode("utf-8")

            def _repl(m):
                ref, attrs, ftag = m.group(1), m.group(2), m.group(3)
                if ref not in cmap:
                    return m.group(0)
                val = cmap[ref]
                attrs_clean = re.sub(r' t="[^"]*"', "", attrs)
                if isinstance(val, str):
                    return f'<c r="{ref}"{attrs_clean} t="str">{ftag}<v>{xml_escape(val)}</v></c>'
                return f'<c r="{ref}"{attrs_clean}>{ftag}<v>{float(val):.12g}</v></c>'

            txt = cell_pat.sub(_repl, txt)
            data = txt.encode("utf-8")
        elif name.startswith("xl/charts/chart") and name.endswith(".xml"):
            txt = data.decode("utf-8")
            txt = re.sub(r'(<(?:c:)?cat>)\s*<((?:c:)?)numRef>(.*?)</\2numRef>\s*(</(?:c:)?cat>)',
                         r'\1<\2strRef>\3</\2strRef>\4', txt, flags=re.S)
            data = txt.encode("utf-8")
        new_items.append((name, data))
    with zipfile.ZipFile(xlsx_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in new_items:
            zout.writestr(name, data)


def build(out_dir, fig):
    os.makedirs(out_dir, exist_ok=True)
    _write_csv(out_dir, fig)
    wb = Workbook()
    cache = {}
    _sheet_schedule(wb, fig, cache)
    _sheet_components(wb, fig, cache)
    _sheet_physics(wb, fig, cache)
    _sheet_routes(wb, fig)
    _sheet_variants(wb, fig)
    wb_path = os.path.join(out_dir, FILES["wb"])
    wb.save(wb_path)
    _inject_caches_and_fix_chart(wb_path, cache)
