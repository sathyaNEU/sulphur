"""Build the two golden deliverables strictly from figures.json:
1. vesterdal_substation_conformed_2026.csv — one row per in-scope substation holding conformed 2026 peak metrics
   and the assigned 2027-2029 relief phase.
2. vesterdal_relief_schedule_2027_2029.xlsx — opens on Relief_Schedule with the Final Recommendation, full
   conformed substation schedule, pool aggregates, and an embedded chart comparing Firm N-1 Loading % against
   the 85% and 100% planning lines, followed by Critical_Components, Referee_Validation, Routes_Comparison,
   and Variant_Battery tabs.
"""
import csv
import os

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
    ordered = sorted(targets, key=lambda s: -fig["substations"][s]["loading_pct"])
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


def _sheet_schedule(wb, fig):
    ws = wb.active
    ws.title = "Relief_Schedule"
    p1 = ", ".join(fig["schedule_groups"]["phase1"])
    p2 = ", ".join(fig["schedule_groups"]["phase2"])
    df = ", ".join(fig["schedule_groups"]["defer"])
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

    ordered = sorted(fig["targets"], key=lambda s: -fig["substations"][s]["loading_pct"])
    for idx, s in enumerate(ordered):
        r = fig["substations"][s]
        row = 6 + idx
        ws.append([
            s, r["firm_n1_mva"], r["p60_peak_mw"], r["p15_peak_mw"], r["q_peak_h_mvar"],
            r["w_max_pct"], r["lim_mva"], r["loading_pct"], r["relief_mva"], r["phase"],
        ])
        ws.cell(row=row, column=2).number_format = "0.0"
        for col in (3, 4, 5, 6, 7, 8, 9):
            ws.cell(row=row, column=col).number_format = "0.00"
        ws.cell(row=row, column=10).alignment = Alignment(horizontal="center")
        fill = P1_FILL if "Phase 1" in r["phase"] else (P2_FILL if "Phase 2" in r["phase"] else DEF_FILL)
        ws.cell(row=row, column=10).fill = fill
        ws.cell(row=row, column=8).fill = fill

    tot_row = 6 + len(ordered)
    ws.append([
        "In-Scope Pool Total / Avg",
        round(sum(fig["substations"][s]["firm_n1_mva"] for s in ordered), 1),
        fig["r1_p60_sum_mw"],
        fig["c1_total_p15_mw"],
        fig["c2_total_qpeak_mvar"],
        fig["c3_mean_lim_phase_pct"],
        fig["pool_lim_mva_sum"],
        None,
        fig["total_relief_mva"],
        "3 Phase 1 / 3 Phase 2 / 1 Defer",
    ])
    for col in range(1, 11):
        c = ws.cell(row=tot_row, column=col)
        c.font = Font(bold=True, name="Calibri", size=10)
        c.fill = TOT_FILL
        c.border = Border(top=THIN, bottom=MED)
    ws.cell(row=tot_row, column=2).number_format = "0.0"
    for col in (3, 4, 5, 6, 7, 9):
        ws.cell(row=tot_row, column=col).number_format = "0.00"
    ws.cell(row=tot_row, column=10).alignment = Alignment(horizontal="center")

    # Add native Excel horizontal bar chart comparing Firm N-1 Loading % by substation
    # In openpyxl BarChart(type='bar'), x_axis is the vertical category axis and y_axis is the horizontal value axis.
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


def _sheet_components(wb, fig):
    ws = wb.create_sheet("Critical_Components")
    ws["A1"] = "Critical Components & Conformed Substation Bands (21-Variant Battery)"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws.append([])
    ws.append(["Component / Metric", "Golden Value", "Band Low", "Band High", "Reflex Route", "Rigorous Route", "Units"])
    _hdr(ws, 3, 7, 30)
    rf = fig["routes"]["S1+S2+S3"]
    rg = fig["routes"]["rigorous"]
    rows = [
        ("C1: Pool Combined 15-Min Active Demand", fig["c1_total_p15_mw"], fig["c1_band"][0], fig["c1_band"][1],
         rf["c1_total_p15_mw"], rg["c1_total_p15_mw"], "MW"),
        ("C2: Pool Combined Peak-Hour Reactive Demand", fig["c2_total_qpeak_mvar"], fig["c2_band"][0], fig["c2_band"][1],
         rf["c2_total_qpeak_mvar"], rg["c2_total_qpeak_mvar"], "MVAr"),
        ("C3: Pool Average Limiting-Phase Share", fig["c3_mean_lim_phase_pct"], fig["c3_band"][0], fig["c3_band"][1],
         rf["c3_mean_lim_phase_pct"], rg["c3_mean_lim_phase_pct"], "%"),
        ("Total Relief Capacity Needed", fig["total_relief_mva"], fig["total_relief_band"][0], fig["total_relief_band"][1],
         rf["total_relief_mva"], rg["total_relief_mva"], "MVA"),
    ]
    for r in rows:
        ws.append(list(r))
        ri = ws.max_row
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


def _sheet_referee(wb, fig):
    ws = wb.create_sheet("Referee_Validation")
    ws["A1"] = "Validation on Modernized Non-Target Reference Substations (Fossheim, Lindberg, Ostervik & Solberg)"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    rp = fig["ref_params"]
    n_qh_tot = len(fig["refs"]) * 35040
    ws["A2"] = (f"Calibrated parameters from {n_qh_tot:,} 15-min PQ intervals: rho_park = {rp['rho_park']:.4f}, "
                f"rho_indep = {rp['rho_indep']:.4f}, k_ord = {rp['k_ord']:.4f}, dQ/dP = {rp['dq_dp']:.4f}; "
                f"Phase-ID accuracy vs 2025 field phase-tracer audit: {rp['tracer_matched']}/{rp['tracer_total']} (100.0%) "
                f"vs GIS {rp['gis_tracer_matched']}/{rp['tracer_total']} ({rp['gis_tracer_pct']:.1f}%).")
    ws["A2"].font = Font(italic=True, size=9, color="444444", name="Calibri")
    ws.append([])
    ws.append(["Reference Substation", "Firm N-1 (MVA)", "Measured 15m P (MW)", "Estimated P15 (MW)",
               "Measured Q_peak (MVAr)", "Estimated Q_peak (MVAr)", "Measured w_max (%)", "Estimated w_max (%)",
               "Measured Loading (%)", "Estimated Loading (%)", "Abs Error (pp)"])
    _hdr(ws, 4, 11, 34)
    for r in sorted(fig["refs"]):
        rec = fig["substations"][r]
        ws.append([
            r, rec["firm_n1_mva"], rec["truth_p15_mw"], rec["p15_peak_mw"],
            rec["truth_q_peak_mvar"], rec["q_peak_h_mvar"], rec["truth_w_max_pct"], rec["w_max_pct"],
            rec["truth_loading_pct"], rec["loading_pct"], rec["abs_loading_err_pp"],
        ])
        ri = ws.max_row
        for c in range(2, 12):
            ws.cell(row=ri, column=c).number_format = "0.00"

    ws.append([])
    ws.append(["Estimator / Rival Route", "Mean Abs Loading Error on 4 Reference Sites (pp)", "Multiple of Golden MAE"])
    _hdr(ws, ws.max_row, 3, 30)
    labels = [
        ("golden", "Golden conformed estimator (S1+S2+S3)"),
        ("s1_cf_zone", "S1 shortcut: zone-matched register coincidence factor (CF_park / CF_nonpark * sum M15)"),
        ("s1_cf_pooled", "S1 shortcut: pooled register coincidence factor (CF_pooled * sum M15)"),
        ("s1_linear_sum", "S1 shortcut: linear sum of feeder 15m/60m ratios at peak hour (rho = 1)"),
        ("s1_flat_ratio", "S1 shortcut: flat reference 15m/60m multiplier"),
        ("s2_net_kvarh", "S2 shortcut: monthly net kVARh power factor"),
        ("s2_raw_dv_no_demean", "S2 shortcut: raw HV/LV voltage drop without PT demeaning"),
        ("s3_gis_phase", "S3 shortcut: GIS lateral phase tags"),
        ("s1_scada60", "S1 shortcut: hourly 60-minute SCADA peak"),
        ("rigorous", "Rigorous standard shortcut (CF_60 * sum M15, class PF, GIS phase)"),
        ("direct", "Direct route (SCADA 60m, net kVARh PF, balanced 33.3% phases)"),
    ]
    for k, lbl in labels:
        mae = fig["ref_mae"][k]
        mult = 1.0 if k == "golden" else fig["ref_ratios"][k]
        ws.append([lbl, mae, mult])
        ri = ws.max_row
        ws.cell(row=ri, column=2).number_format = "0.00"
        ws.cell(row=ri, column=3).number_format = '0.0"x"'
    _widths(ws, [72, 26, 18, 16, 16, 16, 16, 16, 16, 16, 14])


def _sheet_routes(wb, fig):
    ws = wb.create_sheet("Routes_Comparison")
    ws["A1"] = "Comparison of Golden Conformed Route vs Shortcut Lattice & Standard Routes"
    ws["A1"].font = Font(bold=True, size=12, name="Calibri", color="1F3B5C")
    ws.append([])
    hdr = ["Route", "C1 P15 (MW)", "C2 Q (MVAr)", "C3 w_max (%)", "Total Relief (MVA)", "Ref MAE (pp)"] + [
        f"{s} Load %" for s in fig["targets"]
    ]
    ws.append(hdr)
    _hdr(ws, 3, len(hdr), 34)
    order = ["golden", "S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3", "direct", "rigorous",
             "s1_cf_zone", "s1_cf_pooled", "s1_linear_sum", "s1_flat_ratio", "s2_raw_dv_no_demean"]
    for rname in order:
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
    ws["A1"] = "21-Variant Honest Modeling Battery & +/-20% Forcing Perturbations"
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


def build(out_dir, fig):
    os.makedirs(out_dir, exist_ok=True)
    _write_csv(out_dir, fig)
    wb = Workbook()
    _sheet_schedule(wb, fig)
    _sheet_components(wb, fig)
    _sheet_referee(wb, fig)
    _sheet_routes(wb, fig)
    _sheet_variants(wb, fig)
    wb.save(os.path.join(out_dir, FILES["wb"]))
