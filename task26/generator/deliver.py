"""Build the two golden deliverables strictly from figures.json (v2):
1. vesterdal_substation_conformed_2026.csv - one row per in-scope substation holding conformed 2026 peak metrics
   and the assigned 2027-2029 relief phase.
2. vesterdal_relief_schedule_2027_2029.xlsx - opens on Relief_Schedule with the Final Recommendation, live
   formula-driven conformed substation schedule, pool aggregates, and an embedded horizontal bar chart comparing
   Firm N-1 Loading % across substations, followed by Critical_Components, Referee_Validation, Routes_Comparison,
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
                f"Fossheim, Lindberg, Ostervik, and Solberg were modernized in 2023-2024 and serve as non-target reference validation sites.")
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
            f"=3*(F{row}/100)*SQRT(D{row}^2+(E{row}+Referee_Validation!$D$3*(D{row}-C{row}))^2)",
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


def _sheet_components(wb, fig, cache):
    ws = wb.create_sheet("Critical_Components")
    sc = cache.setdefault("xl/worksheets/sheet2.xml", {})
    n_var = len(fig["variants"])
    ws["A1"] = f"Critical Components & Conformed Substation Bands ({n_var}-Variant Battery)"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws.append([])
    ws.append(["Component / Metric", "Golden Value", "Band Low", "Band High", "Reflex Route", "Rigorous Route", "Units"])
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


def _sheet_referee(wb, fig, cache):
    ws = wb.create_sheet("Referee_Validation")
    sc = cache.setdefault("xl/worksheets/sheet3.xml", {})
    ws["A1"] = "Validation on Modernized Non-Target Reference Substations (Fossheim, Lindberg, Ostervik & Solberg)"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    rp = fig["ref_params"]
    n_qh_tot = len(fig["refs"]) * 35040
    ws["A2"] = (f"Calibrated from {n_qh_tot:,} 15-min 3-phase main-bay PQ intervals; AMI phase-ID vs 2025 tracer audit: "
                f"{rp['tracer_matched']}/{rp['tracer_total']} (100.0%) vs GIS "
                f"{rp['gis_tracer_matched']}/{rp['tracer_total']} ({rp['gis_tracer_pct']:.1f}%).")
    ws["A2"].font = Font(italic=True, size=9, color="444444", name="Calibri")

    # Row 3: live numeric calibration strip referenced by Relief_Schedule!G6:G12 ($D$3 = dQ/dP)
    ws.append([
        "k_ord (cal)", rp["k_ord_raw"], "dQ/dP (winter)", rp["dq_dp_raw"],
        "tan_phi_u (cal)", rp["tan_phi_u_raw"], "Lindberg R_off", rp["rho_sync_lindberg"],
        "Fossheim R_off", rp["rho_stag_fossheim"], f"AMI Tracer {rp['tracer_matched']}/{rp['tracer_total']}",
    ])
    for col in range(1, 12):
        c = ws.cell(row=3, column=col)
        c.fill = PARAM_FILL
        c.border = Border(top=THIN, bottom=THIN)
        c.font = Font(bold=(col % 2 == 1), name="Calibri", size=9, color="1F3B5C" if col % 2 == 1 else "000000")
        if col in (2, 4, 6, 8, 10):
            c.number_format = "0.0000"

    ws.append([])
    ws.append(["Reference Substation", "Firm N-1 (MVA)", "Measured 15m P (MW)", "Estimated P15 (MW)",
               "Measured Q_peak (MVAr)", "Estimated Q_peak (MVAr)", "Measured w_max (%)", "Estimated w_max (%)",
               "Measured Loading (%)", "Estimated Loading (%)", "Abs Error (pp)"])
    _hdr(ws, 5, 11, 34)
    ref_errs = []
    for r in sorted(fig["refs"]):
        rec = fig["substations"][r]
        ri = ws.max_row + 1
        err_raw = abs(rec["loading_pct_raw"] - rec["truth_loading_pct_raw"])
        ref_errs.append(err_raw)
        ws.append([
            r, rec["firm_n1_mva"], rec["truth_p15_mw"], rec["p15_peak_mw_raw"],
            rec["truth_q_peak_mvar"], rec["q_peak_h_mvar_raw"], rec["truth_w_max_pct"], rec["w_max_pct_raw"],
            rec["truth_loading_pct_raw"], rec["loading_pct_raw"], f"=ABS(J{ri}-I{ri})",
        ])
        sc[f"K{ri}"] = err_raw
        for c in range(2, 12):
            ws.cell(row=ri, column=c).number_format = "0.00"

    gold_mae_raw = sum(ref_errs) / len(ref_errs)
    ws.append([])
    ws.append(["Estimator / Rival Route", "Mean Abs Loading Error on 4 Reference Sites (pp)", "Multiple of Golden MAE"])
    _hdr(ws, ws.max_row, 3, 30)
    label_map = {
        "golden": "Golden conformed estimator (S1+S2+S3)",
        "s1_raw_corr": "S1 shortcut: raw hourly feeder correlation (unstripped diurnal/weather mode)",
        "s2_class_pf": "S2 shortcut: engineering manual nominal class power factors",
        "s1_indep_quad": "S1 shortcut: independent quadrature (ignoring feeder synchronization)",
        "s1_cf_pooled": "S1 shortcut: pooled register coincidence factor (CF_pooled * sum M15)",
        "s1_class_ols": "S1 shortcut: 48-month class-share OLS diversity factor",
        "s2_raw_dv_no_demean": "S2 shortcut: coupled corridor dV without monthly net kVARh PT demeaning",
        "s1_flat_ratio": "S1 shortcut: flat reference 15m/60m multiplier",
        "s2_net_kvarh": "S2 shortcut: monthly net kVARh power factor",
        "s1_linear_sum": "S1 shortcut: linear sum of feeder 15m/60m ratios at peak hour",
        "s1_rigorous_cf60": "S1 shortcut: hourly coincidence factor times feeder 15m registers",
        "rigorous": "Rigorous standard shortcut (CF_pooled, class nominal PF, AMI-only balanced)",
        "s1_scada60": "S1 shortcut: hourly 60-minute SCADA peak",
        "s3_ami_plus_gis": "S3 shortcut: AMI-identified smart laterals + GIS tags for non-AMI legacy laterals",
        "s2_rp_only": "S2 shortcut: single-site dV subtracting 66 kV R*P only (ignoring X*Q coupling)",
        "s3_gis_phase": "S3 shortcut: GIS lateral phase tags",
        "s3_ami_only_bal": "S3 shortcut: AMI-identified smart laterals (20/36) + balanced remainder",
        "s3_raw_vbus_no_pt": "S3 shortcut: raw 3-phase bus voltage deviation without PT-offset slope removal",
        "s2_local_dv": "S2 shortcut: local transformer dV using GSP voltage directly (ignoring 66 kV lines)",
        "s3_ami_grossup": "S3 shortcut: AMI-identified smart laterals grossed up by 36/20",
        "direct": "Direct route (SCADA 60m, net kVARh PF, balanced 33.3% phases)",
        "frontier_combo": "Frontier shortcut combo (class-share OLS + local GSP dV + AMI-only balanced)",
    }
    ordered_keys = ["golden"] + sorted([k for k in fig["ref_mae"] if k != "golden"], key=lambda k: fig["ref_mae"][k])
    gold_row = ws.max_row + 1
    for k in ordered_keys:
        ri = ws.max_row + 1
        if k == "golden":
            ws.append([label_map[k], "=AVERAGE(K6:K9)", f"=B{ri}/$B${gold_row}"])
            sc[f"B{ri}"] = gold_mae_raw
            sc[f"C{ri}"] = 1.0
        else:
            mae = fig["ref_mae"][k]
            ws.append([label_map.get(k, k), mae, f"=B{ri}/$B${gold_row}"])
            sc[f"C{ri}"] = mae / gold_mae_raw
        ws.cell(row=ri, column=2).number_format = "0.00"
        ws.cell(row=ri, column=3).number_format = '0.0"x"'
    _widths(ws, [76, 26, 18, 16, 16, 16, 16, 16, 16, 16, 18])


def _sheet_routes(wb, fig):
    ws = wb.create_sheet("Routes_Comparison")
    ws["A1"] = "Comparison of Golden Conformed Route vs Shortcut Lattice & Rival Routes"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws.append([])
    hdr = ["Route", "C1 P15 (MW)", "C2 Q (MVAr)", "C3 w_max (%)", "Total Relief (MVA)", "Ref MAE (pp)"] + [
        f"{s} Load %" for s in fig["targets"]
    ]
    ws.append(hdr)
    _hdr(ws, 3, len(hdr), 34)
    order = [
        "golden", "S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3",
        "direct", "rigorous", "frontier_combo",
        "s1_raw_corr", "s1_indep_quad", "s1_class_ols", "s1_cf_pooled", "s1_flat_ratio", "s1_linear_sum",
        "s2_class_pf", "s2_raw_dv_no_demean", "s2_rp_only", "s2_local_dv",
        "s3_ami_plus_gis", "s3_ami_only_bal", "s3_ami_grossup", "s3_raw_vbus_no_pt",
    ]
    for rname in order:
        if rname not in fig["routes"]:
            continue
        r = fig["routes"][rname]
        ws.append([
            rname, r["c1_total_p15_mw"], r["c2_total_qpeak_mvar"], r["c3_mean_lim_phase_pct"],
            r["total_relief_mva"], r["ref_mae_pp"],
        ] + [r["loading_pct"][s] for s in fig["targets"]])
        ri = ws.max_row
        for c in range(2, len(hdr) + 1):
            ws.cell(row=ri, column=c).number_format = "0.00"
    _widths(ws, [22, 13, 13, 13, 16, 13] + [13] * len(fig["targets"]))


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
    _sheet_referee(wb, fig, cache)
    _sheet_routes(wb, fig)
    _sheet_variants(wb, fig)
    wb_path = os.path.join(out_dir, FILES["wb"])
    wb.save(wb_path)
    _inject_caches_and_fix_chart(wb_path, cache)
