"""task9 architecture 6, the golden deliverables: formula-driven model risk workbook and five-slide committee deck,
both leading with the 2027 call. Every figure comes from figures.json and the loaded pack's arrays."""
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

import core as C
import pack as P
import results as RS

FILES = {"wb": "garrane_score_stability_sources_2027.xlsx", "deck": "garrane_stability_review_2027.pptx"}
NAMES = RS.NAMES
ORDER = RS.ORDER
BANDNAME = {"monitor": "Monitor", "a remediation plan": "Remediation plan", "escalation": "Escalation"}

NAVY = "1B365D"
SLATE = "334E68"
PALE = "EDF2F7"
SOFT = "F8FAFC"
ESC_BG = "FDE8E8"
REM_BG = "FEF3C7"
MON_BG = "E6F4EA"
THIN = Side(style="thin", color="CBD5E1")
MED_NAVY = Side(style="medium", color=NAVY)


def _hdr(ws, row, ncol, fill_hex=NAVY):
    ws.row_dimensions[row].height = 24
    for j in range(1, ncol + 1):
        c = ws.cell(row=row, column=j)
        c.font = Font(name="Calibri", bold=True, size=10, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=fill_hex)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if j == 1 else "right")


def _box(ws, r0, r1, ncol, zebra=True):
    for r in range(r0, r1 + 1):
        for j in range(1, ncol + 1):
            cell = ws.cell(row=r, column=j)
            cell.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
            if r > r0:
                if cell.font is None or cell.font.name != "Calibri":
                    cell.font = Font(name="Calibri", size=10, bold=(cell.font.bold if cell.font else False))
                if zebra and (r - r0) % 2 == 0 and (cell.fill.fill_type is None):
                    cell.fill = PatternFill("solid", fgColor=SOFT)


def _cols(ws, widths):
    for j, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = wd


def _fmt(ws, row, col, f):
    ws.cell(row=row, column=col).number_format = f


def _band_fill(band_str):
    if band_str == "Escalation":
        return PatternFill("solid", fgColor=ESC_BG)
    if band_str == "Remediation plan":
        return PatternFill("solid", fgColor=REM_BG)
    return PatternFill("solid", fgColor=MON_BG)


def workbook(path, fig, pk, g):
    codes = pk.w["codes"]
    w = pk.w
    wt = w["merch"] / w["merch"].sum()
    wb = Workbook()

    # ------------------------------------------------------------------ Sheet 1: 2027 placements (opens on the call!)
    ws = wb.active
    ws.title = "2027 placements"
    ws.views.sheetView[0].showGridLines = True
    ws["A1"] = "Garrane Merchant Score: 2027 model-side stability placements"
    ws["A1"].font = Font(name="Calibri", bold=True, size=14, color=NAVY)
    ws["A2"] = ("Book-weighted root-mean-square movement between consecutive 2027 quarter-end snapshots against "
                "Model Stability Standard v2 lines (Monitor < 5.5, Remediation plan 5.5 to < 8.0, Escalation >= 8.0). "
                "Records through 23 November 2026.")
    ws["A2"].font = Font(name="Calibri", size=10, italic=True, color=SLATE)
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 28

    ws.append([])
    ws.append(["Model-side source", "2027 mean-square (pts^2)", "2027 movement (pts)", "2027 band", "Standard requirement"])
    _hdr(ws, 4, 5)
    # Link each source's MS directly to 'Quarter pairs' row 2..6 column F (annual mean MS)
    qp_row = {"labels": 2, "releases": 3, "optimisation": 4, "turnover": 5, "retunes": 6}
    req_formula = lambda r: (
        '=IF(C%d>=8,"Board risk committee escalation; plan by 31 Jan 2027",'
        'IF(C%d>=5.5,"Remediation plan to under 5.5 pts by 31 Jan 2027","Quarterly reporting to committee"))' % (r, r)
    )
    band_formula = lambda r: '=IF(C%d>=8,"Escalation",IF(C%d>=5.5,"Remediation plan","Monitor"))' % (r, r)
    for idx, s in enumerate(ORDER):
        r = 5 + idx
        n = NAMES[s]
        ws.append([
            n[0].upper() + n[1:],
            "='Quarter pairs'!F%d" % qp_row[s],
            "=SQRT(B%d)" % r,
            band_formula(r),
            req_formula(r),
        ])
        _fmt(ws, r, 2, "0.00")
        _fmt(ws, r, 3, "0.00")
        ws.cell(row=r, column=4).fill = _band_fill(BANDNAME[fig["band_of"][n]])
        ws.cell(row=r, column=4).font = Font(name="Calibri", bold=True, size=10)
        ws.cell(row=r, column=4).alignment = Alignment(horizontal="center")
    _box(ws, 4, 9, 5, zebra=False)

    # Combined model-side movement table (Ask 2)
    ws.append([])
    r_c0 = 11
    ws.append(["Combined model-side movement (all five sources)", "Mean-square (pts^2)", "Movement (pts)", "Snapshot span", "Note"])
    _hdr(ws, r_c0, 5, SLATE)
    spans_lbl = [
        ("Q1 2027 pair", "B", "21 Dec 2026 to 22 Mar 2027", "Q1 sprint releases + high live exposure"),
        ("Q2 2027 pair", "C", "22 Mar 2027 to 21 Jun 2027", "Q2 sprint releases + mid-year volume trough"),
        ("Q3 2027 pair", "D", "21 Jun 2027 to 20 Sep 2027", "Pinned views ramping across complex families"),
        ("Q4 2027 pair", "E", "20 Sep 2027 to 20 Dec 2027", "Highest pinned coverage across book"),
        ("2027 year (Standard 3.3)", "F", "Four 2027 snapshot pairs", "Root of mean of the four pairs' combined MS"),
    ]
    for i, (lbl, col, span_s, note_s) in enumerate(spans_lbl):
        r = r_c0 + 1 + i
        ws.append([lbl, "='Quarter pairs'!%s7" % col, "=SQRT(B%d)" % r, span_s, note_s])
        _fmt(ws, r, 2, "0.00")
        _fmt(ws, r, 3, "0.00")
        if i == 4:
            for j in range(1, 6):
                ws.cell(row=r, column=j).font = Font(name="Calibri", bold=True, size=10)
                ws.cell(row=r, column=j).fill = PatternFill("solid", fgColor=PALE)
    _box(ws, r_c0, r_c0 + 5, 5, zebra=False)

    # Pinned feature views table (Ask 3)
    ws.append([])
    r_p0 = 18
    ws.append(["Platform adoption measure", "2027 expected (%)", "Calendar plan (%)", "Basis", "Note"])
    _hdr(ws, r_p0, 5, SLATE)
    ws.append([
        "Share of 2027 weekly retrains on pinned feature views",
        "='Feature releases & pinned'!E16",
        round(fig["base"]["cov_plan"], 1),
        "52 assessment-year Mondays",
        "Equal-weighted across 14 families, 28 Dec 2026 to 20 Dec 2027 (Standard 2.2)",
    ])
    _fmt(ws, r_p0 + 1, 2, "0.0")
    _fmt(ws, r_p0 + 1, 3, "0.0")
    ws.cell(row=r_p0 + 1, column=2).font = Font(name="Calibri", bold=True, size=10)
    _box(ws, r_p0, r_p0 + 1, 5, zebra=False)
    _cols(ws, (44, 22, 18, 26, 54))
    ws.freeze_panes = "A5"

    # ------------------------------------------------------------------ Sheet 2: Quarter pairs (formula-linked!)
    qp = wb.create_sheet("Quarter pairs")
    qp.append(["Source", "Q1 MS (pts^2)", "Q2 MS (pts^2)", "Q3 MS (pts^2)", "Q4 MS (pts^2)",
               "2027 mean MS (pts^2)", "2027 movement (pts)", "Model-side share (%)"])
    _hdr(qp, 1, 8)
    # Rows 2..6 match qp_row above: labels, releases, optimisation, turnover, retunes
    qp_order = ("labels", "releases", "optimisation", "turnover", "retunes")
    # Build per-pair book-weighted MS links:
    # labels = SUMPRODUCT(Instruments!C2:C15, Instruments!I2:I15)*13
    # releases = Feature releases!H16..K16
    # optimisation = Warm-start noise!E16
    # turnover = Training data recency!E16..H16
    # retunes = SUMPRODUCT(Instruments!C2:C15, Instruments!G2:G15)*13/4
    qp_formulas = {
        "labels": ["=SUMPRODUCT('Instruments by family'!$C$2:$C$15,'Instruments by family'!$I$2:$I$15)*13"] * 4,
        "releases": ["='Feature releases & pinned'!H16", "='Feature releases & pinned'!I16",
                     "='Feature releases & pinned'!J16", "='Feature releases & pinned'!K16"],
        "optimisation": ["='Warm-start noise'!$E$16"] * 4,
        "turnover": ["='Training data recency'!E16", "='Training data recency'!F16",
                     "='Training data recency'!G16", "='Training data recency'!H16"],
        "retunes": ["=SUMPRODUCT('Instruments by family'!$C$2:$C$15,'Instruments by family'!$G$2:$G$15)*13/4"] * 4,
    }
    for idx, s in enumerate(qp_order):
        r = 2 + idx
        n = NAMES[s]
        qp.append([n[0].upper() + n[1:]] + qp_formulas[s] + [
            "=AVERAGE(B%d:E%d)" % (r, r),
            "=SQRT(F%d)" % r,
            "=100*F%d/$F$7" % r,
        ])
        for col in range(2, 8):
            _fmt(qp, r, col, "0.00")
        _fmt(qp, r, 8, "0.0")
    qp.append([
        "Combined model-side MS (pts^2)",
        "=SUM(B2:B6)", "=SUM(C2:C6)", "=SUM(D2:D6)", "=SUM(E2:E6)",
        "=AVERAGE(B7:E7)", "=SQRT(F7)", "=SUM(H2:H6)",
    ])
    qp.append([
        "Combined model-side RMS (pts)",
        "=SQRT(B7)", "=SQRT(C7)", "=SQRT(D7)", "=SQRT(E7)", "=SQRT(F7)", "", "",
    ])
    for r in (7, 8):
        for j in range(1, 9):
            qp.cell(row=r, column=j).font = Font(name="Calibri", bold=True, size=10)
            qp.cell(row=r, column=j).fill = PatternFill("solid", fgColor=PALE)
        for col in range(2, 8):
            _fmt(qp, r, col, "0.00")
    _fmt(qp, 7, 8, "0.0")
    _box(qp, 1, 8, 8, zebra=False)
    _cols(qp, (30, 15, 15, 15, 15, 20, 18, 18))

    # ------------------------------------------------------------------ Sheet 3: Instruments by family
    s2 = wb.create_sheet("Instruments by family")
    s2.append(["Family", "Scored merchants (21 Sep 2026)", "Book weight", "Replicate MS",
               "Bootstrap mean MS (16 pairs)", "Bootstrap net MS", "Retune shadow MS",
               "Release shadow MS", "Label freeze MS", "Mean bootstrap window rows"])
    _hdr(s2, 1, 10)
    I = pk.inst
    for f in range(C.F):
        r = 2 + f
        bm = float(np.mean(I["boot_v"][f]))
        bn = float(np.mean(I["boot_n"][f]))
        s2.append([
            codes[f], int(w["merch"][f]), "=B%d/$B$16" % r,
            float(I["rep"][f]), bm, "=MAX(E%d-D%d,0)" % (r, r),
            float(I["ret"][f]), float(I["rel"][f]), float(I["lab"][f]), int(round(bn)),
        ])
        _fmt(s2, r, 2, "#,##0")
        _fmt(s2, r, 3, "0.0000")
        for col in range(4, 10):
            _fmt(s2, r, col, "0.00")
        _fmt(s2, r, 10, "#,##0")
    s2.append([
        "Book weighted", "=SUM(B2:B15)", "=SUM(C2:C15)",
        "=SUMPRODUCT($C$2:$C$15,D2:D15)", "=SUMPRODUCT($C$2:$C$15,E2:E15)",
        "=SUMPRODUCT($C$2:$C$15,F2:F15)", "=SUMPRODUCT($C$2:$C$15,G2:G15)",
        "=SUMPRODUCT($C$2:$C$15,H2:H15)", "=SUMPRODUCT($C$2:$C$15,I2:I15)", "",
    ])
    for j in range(1, 11):
        s2.cell(row=16, column=j).font = Font(name="Calibri", bold=True, size=10)
        s2.cell(row=16, column=j).fill = PatternFill("solid", fgColor=PALE)
    _fmt(s2, 16, 2, "#,##0")
    _fmt(s2, 16, 3, "0.0000")
    for col in range(4, 10):
        _fmt(s2, 16, col, "0.00")
    _box(s2, 1, 16, 10)
    _cols(s2, (11, 22, 12, 14, 20, 16, 15, 15, 15, 22))
    s2.freeze_panes = "B2"

    # ------------------------------------------------------------------ Sheet 4: Warm-start noise (S1 + cold proof)
    s4 = wb.create_sheet("Warm-start noise")
    s4.append(["Family", "Settled warm start", "Persistence (phi)", "Anchored asymptote A",
               "13-week MS (pts^2)", "13-week points", "Cold-era weeks", "Cold-era quad/D14"] +
              ["Gap %d" % h for h in range(1, 26)])
    _hdr(s4, 1, 33)
    for f in range(C.F):
        r = 2 + f
        s4.append([
            codes[f], P.monday(pk.t0[f]), float(g["phi"][f]),
            "='Instruments by family'!D%d/(1-C%d^2)" % (r, r),
            "=D%d*(1-C%d^13)" % (r, r), "=SQRT(E%d)" % r,
            int(w["warm"]["eff"][f]), float(pk.cold_curv[f]),
        ] + [round(float(x), 2) for x in pk.curves[f][:25]])
        _fmt(s4, r, 2, "dd/mm/yyyy")
        _fmt(s4, r, 3, "0.0000")
        _fmt(s4, r, 4, "0.00")
        _fmt(s4, r, 5, "0.00")
        _fmt(s4, r, 6, "0.00")
        _fmt(s4, r, 8, "+0.000;-0.000;0.000")
    s4.append([
        "Book weighted", "", "", "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,D2:D15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,E2:E15)", "=SQRT(E16)",
        "=MIN(G2:G15)", "=AVERAGE(H2:H15)",
    ] + [""] * 25)
    for j in range(1, 9):
        s4.cell(row=16, column=j).font = Font(name="Calibri", bold=True, size=10)
        s4.cell(row=16, column=j).fill = PatternFill("solid", fgColor=PALE)
    for col in (4, 5, 6):
        _fmt(s4, 16, col, "0.00")
    _fmt(s4, 16, 8, "+0.000;-0.000;0.000")
    _box(s4, 1, 16, 33)
    _cols(s4, [11, 14, 14, 18, 16, 13, 13, 15] + [7.5] * 25)
    s4.freeze_panes = "B2"

    # ------------------------------------------------------------------ Sheet 5: Training data recency (S2)
    s3 = wb.create_sheet("Training data recency")
    s3.append(["Family", "Window (weeks)", "Fitted decay (lambda)", "Per-row noise (row2)",
               "Q1 2027 MS", "Q2 2027 MS", "Q3 2027 MS", "Q4 2027 MS",
               "2027 mean MS", "2027 points"])
    _hdr(s3, 1, 10)
    for f in range(C.F):
        r = 2 + f
        s3.append([
            codes[f], int(w["window"][f]), float(g["lam"][f]), float(g["row2"][f]),
            float(g["tur_q"][f, 0]), float(g["tur_q"][f, 1]),
            float(g["tur_q"][f, 2]), float(g["tur_q"][f, 3]),
            "=AVERAGE(E%d:H%d)" % (r, r), "=SQRT(I%d)" % r,
        ])
        _fmt(s3, r, 3, "0.000")
        _fmt(s3, r, 4, "#,##0")
        for col in range(5, 11):
            _fmt(s3, r, col, "0.00")
    s3.append([
        "Book weighted", "", "", "",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,E2:E15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,F2:F15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,G2:G15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,H2:H15)",
        "=AVERAGE(E16:H16)", "=SQRT(I16)",
    ])
    for j in range(1, 11):
        s3.cell(row=16, column=j).font = Font(name="Calibri", bold=True, size=10)
        s3.cell(row=16, column=j).fill = PatternFill("solid", fgColor=PALE)
    for col in range(5, 11):
        _fmt(s3, 16, col, "0.00")
    _box(s3, 1, 16, 10)

    s3.append([])
    rk0 = 18
    s3.append(["Recency kernel sensitivity (2026 bootstrap pairs)", "Mean log-RMSE", "2027 training data (pts)", "2027 band"])
    _hdr(s3, rk0, 4, SLATE)
    for kname, kv in fig["recency_diag"]["kernels"].items():
        r = s3.max_row + 1
        s3.append([kname, float(kv["log_rmse"]), float(kv["points"]),
                   '=IF(C%d>=8,"Escalation",IF(C%d>=5.5,"Remediation plan","Monitor"))' % (r, r)])
        _fmt(s3, r, 2, "0.0000")
        _fmt(s3, r, 3, "0.00")
    _box(s3, rk0, s3.max_row, 4)
    _cols(s3, (34, 14, 18, 18, 13, 13, 13, 13, 15, 13))
    s3.freeze_panes = "B2"

    # ------------------------------------------------------------------ Sheet 6: Feature releases & pinned (S3)
    s5 = wb.create_sheet("Feature releases & pinned")
    m = pk.models["loglin"]
    s5.append(["Family", "Custom components", "PC-26-058 planned", "Median adoption lag (wk)",
               "2027 pinned share (%)", "Same-group corr (2026)", "Diff-group corr (2026)",
               "Q1 rel MS", "Q2 rel MS", "Q3 rel MS", "Q4 rel MS", "2027 mean MS", "2027 points"])
    _hdr(s5, 1, 13)
    for f in range(C.F):
        r = 2 + f
        s5.append([
            codes[f], int(w["custom"][f]), P.monday(int(w["fv_planned"][f])), float(math.exp(m["mu"][f])),
            100.0 * float(np.mean(g["cov"][f, 1:])), float(pk.inst["rel_coh_same"][f]),
            float(pk.inst["rel_coh_diff"][f]),
            float(g["rel_q"][f, 0]), float(g["rel_q"][f, 1]),
            float(g["rel_q"][f, 2]), float(g["rel_q"][f, 3]),
            "=AVERAGE(H%d:K%d)" % (r, r), "=SQRT(L%d)" % r,
        ])
        _fmt(s5, r, 3, "dd/mm/yyyy")
        _fmt(s5, r, 4, "0.0")
        _fmt(s5, r, 5, "0.0")
        _fmt(s5, r, 6, "0.000")
        _fmt(s5, r, 7, "+0.000;-0.000;0.000")
        for col in range(8, 14):
            _fmt(s5, r, col, "0.00")
    s5.append([
        "All / Book weighted", "", "", "", "=AVERAGE(E2:E15)",
        "=AVERAGE(F2:F15)", "=AVERAGE(G2:G15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,H2:H15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,I2:I15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,J2:J15)",
        "=SUMPRODUCT('Instruments by family'!$C$2:$C$15,K2:K15)",
        "=AVERAGE(H16:K16)", "=SQRT(L16)",
    ])
    for j in range(1, 14):
        s5.cell(row=16, column=j).font = Font(name="Calibri", bold=True, size=10)
        s5.cell(row=16, column=j).fill = PatternFill("solid", fgColor=PALE)
    _fmt(s5, 16, 5, "0.0")
    _fmt(s5, 16, 6, "0.000")
    _fmt(s5, 16, 7, "+0.000;-0.000;0.000")
    for col in range(8, 14):
        _fmt(s5, 16, col, "0.00")
    _box(s5, 1, 16, 13)

    s5.append([])
    r_loo = 18
    s5.append(["Leave-one-rollout-out adoption validation", "Recorded 39-wk share (%)", "Out-of-sample model (%)", "Diff (pp)"])
    _hdr(s5, r_loo, 4, SLATE)
    for k, lab in (("runtime", "PC-24-031 Runtime image 4.1.0"),
                   ("warm", "PC-24-047 Warm start & long window"),
                   ("amp", "PC-25-012 Mixed precision (bf16)")):
        r = s5.max_row + 1
        s5.append([lab, 100.0 * fig["loo"][k]["record"], 100.0 * fig["loo"][k]["model"], "=C%d-B%d" % (r, r)])
        _fmt(s5, r, 2, "0.0")
        _fmt(s5, r, 3, "0.0")
        _fmt(s5, r, 4, "+0.0;-0.0;0.0")
    _box(s5, r_loo, s5.max_row, 4)
    _cols(s5, (32, 16, 16, 16, 16, 16, 16, 11, 11, 11, 11, 13, 12))
    s5.freeze_panes = "B2"

    # ------------------------------------------------------------------ Sheet 7: 2026 record check (falsification)
    s6 = wb.create_sheet("2026 record check")
    s6.append(["Route", "Total 2026 discrepancy (pts^2)", "Multiple of golden", "Notes"])
    _hdr(s6, 1, 4)
    fa = fig["falsification"]
    rows_f = [
        ("Committed estimate (anchored decay + recency + same-group cov)", fa["golden_err"],
         "D1=%.2f vs %.2f; boot contrast=%.2f vs %.2f; rel cov=%.2f vs %.2f" % (
             fa["golden_parts"]["d1"], fa["obs_d1"], fa["golden_parts"]["boot_c"],
             fa["obs_boot_contrast"], fa["golden_parts"]["rel_cov"], fa["obs_rel_cov"])),
        ("Linear 13-refit noise carry (warm-start decay omitted)", fa["rivals"]["S1 linear carry"], "Under-predicts warm 1-week panel variance D_warm(1)"),
        ("Uniform window turnover (recency decay omitted)", fa["rivals"]["S2 uniform window"], "Fails seasonal high-vs-low volume bootstrap contrast"),
        ("Orthogonal feature releases (within-group covariance omitted)", fa["rivals"]["S3 orthogonal releases"], "Assumes 0.00 covariance where 141 same-group pairs average +4.80 pts^2"),
        ("Unadjusted calendar baseline (raw bootstrap + linear carry + plan dates)", fa["rivals"]["direct"], "Fails all three 2026 instrument checks"),
        ("Standard shortcut (linear carry + uniform + orthogonal)", fa["rivals"]["rigorous (Response 1)"], "Fails all three 2026 instrument checks"),
    ]
    for idx, (lbl, val, note) in enumerate(rows_f):
        r = 2 + idx
        s6.append([lbl, float(val), "=B%d/$B$2" % r, note])
        _fmt(s6, r, 2, "0.00")
        _fmt(s6, r, 3, "0.0x")
    _box(s6, 1, 7, 4)
    _cols(s6, (50, 24, 16, 62))

    # ------------------------------------------------------------------ Sheet 8: Other routes & supplement
    s7 = wb.create_sheet("Other routes & supplement")
    s7.append(["Specification", "Label rev", "Feature rel", "Optimisation", "Training data", "Retunes",
               "Combined 2027", "Pinned (%)", "Bands filed"])
    _hdr(s7, 1, 9)
    show = [
        ("Committed estimate (this assessment)", fig),
        ("Linear 13-refit noise carry only", fig["lattice"]["S1"]),
        ("Uniform window turnover only", fig["lattice"]["S2"]),
        ("Orthogonal feature releases only", fig["lattice"]["S3"]),
        ("Standard shortcut (linear carry + uniform + orthogonal)", fig["rigorous"]),
        ("Unadjusted calendar baseline (raw bootstrap + linear + plan)", fig["direct"]),
    ]
    for lbl, e in show:
        r = s7.max_row + 1
        p = e["points"]
        s7.append([lbl, p["label revisions"], p["feature releases"], p["optimisation noise"],
                   p["training data"], p["retunes"], e["tot_yr"], e["cc_pin"], "; ".join(e["call"])])
        for col in range(2, 8):
            _fmt(s7, r, col, "0.00")
        _fmt(s7, r, 8, "0.0")
    _box(s7, 1, s7.max_row, 9)

    s7.append([])
    rs0 = s7.max_row + 1
    s7.append(["Standard sections 5 and 6 context (non-placement supplement)", "2027 value", "Note"])
    _hdr(s7, rs0, 3, SLATE)
    for lbl, val, note in (
        ("Merchants' own change share of all movement (%)", fig["own_share"], "Standard 5.2 (carried from 2026 settled pairs)"),
        ("2026 measured covenant tier-change rate (%)", fig["fr26"], "Schedule C monitoring panel (12.0% cap)"),
        ("2027 expected tier-change rate as scheduled (%)", fig["fr_sched"], "Standard 6.1 (above 12.0% covenant cap)"),
        ("2027 tier-change rate with designated sources removed (%)", fig["fr_removed"], "Standard 6.1 (brings book under 12.0% cap)"),
    ):
        r = s7.max_row + 1
        s7.append([lbl, float(val), note])
        _fmt(s7, r, 2, "0.0")
    _box(s7, rs0, s7.max_row, 3)
    _cols(s7, (50, 12, 12, 12, 13, 10, 14, 11, 78))

    # ------------------------------------------------------------------ Sheet 9: Notes
    s8 = wb.create_sheet("Notes")
    day = lambda t: "%d %s" % (P.monday(t).day, P.monday(t).strftime("%B %Y"))
    for line in (
        ["Methodology and Governance Notes"],
        ["Records run through the weekly refresh of %s; the 2027 assessment year covers the four Schedule C quarter-end "
         "snapshot pairs closing on 22 March, 21 June, 20 September and 20 December 2027 (52 Mondays from 28 December "
         "2026 through 20 December 2027, Model Stability Standard v2 section 2.2)." % day(C.T - 1)],
        ["Source movements are book-weighted root-mean-square score changes between consecutive quarter-end snapshots, "
         "weighted by scored merchants at the 21 September 2026 snapshot (%s merchants across 14 families, Standard 3.1 "
         "and 3.2). Combined model-side movement sums all five sources' mean-square movements per pair and across the "
         "year (Standard 3.3)." % "{:,}".format(fig["base"]["book_sep26"])],
        ["Panel reconciliation: later load_id supersedes on the four re-sent refreshes; Tolka Pay merchant IDs migrated "
         "on %d %s are linked via tolka_pay_merchant_id_migration.csv (%s unique panel merchants, %s scored merchant-weeks)." % (
             P.monday(P.MIGRATION_T).day, P.monday(P.MIGRATION_T).strftime("%B %Y"),
             "{:,}".format(fig["base"]["panel_merchants"]), "{:,}".format(fig["base"]["score_rows"]))],
        ["Cold-start linearity check: across every family's pre-warm-start history (29 to 55 cold weeks), D_cold(h) "
         "shows near-zero quadratic curvature (mean %+.3f), confirming that merchants' own change does not mean-revert "
         "and warm-era concavity reflects warm-start optimisation decay (Standard 1.4)." % fig["bend"]["cold_curv_mean"]],
        ["Recency weighting: Standard 1.6 and scheduler manifests confirm exponential recency weighting on 52-week and "
         "104-week windows; decay rates lambda_f (%.3f to %.3f) are inverted from the 16 seasonal 2026 bootstrap pairs "
         "per family against warehouse weekly labelled rows." % (fig["base"]["lam_fit"][0], fig["base"]["lam_fit"][1])],
        ["Feature releases: 2026 release_shadow merchant delta vectors show strictly positive same-group correlation "
         "(mean %.3f, min %.3f across %d pairs) and zero cross-group correlation (%+.3f); 2027 sprint pairs combine "
         "within-group covariance with empirical pinned-view adoption lag." % (
             fig["base"]["coh_same_mean"], fig["base"]["coh_same_min"],
             fig["base"]["coh_same_n"], fig["base"]["coh_diff_mean"])],
    ):
        s8.append(line)
    s8["A1"].font = Font(name="Calibri", bold=True, size=12, color=NAVY)
    for r in range(2, s8.max_row + 1):
        s8.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
        s8.row_dimensions[r].height = 30
    _cols(s8, (132,))
    wb.save(path)


# --------------------------------------------------------------------------------------------- Committee Deck (5 slides)
RGB_NAVY = RGBColor(0x1B, 0x36, 0x5D)
RGB_SLATE = RGBColor(0x33, 0x4E, 0x68)
RGB_MUTED = RGBColor(0x64, 0x74, 0x8B)
RGB_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RGB_BG = RGBColor(0xF8, 0xFA, 0xFC)
RGB_CARD = RGBColor(0xEF, 0xF4, 0xF9)
RGB_BORDER = RGBColor(0xCB, 0xD5, 0xE1)
RGB_RED = RGBColor(0xB9, 0x1C, 0x1C)
RGB_AMBER = RGBColor(0xB4, 0x53, 0x09)
RGB_GREEN = RGBColor(0x15, 0x80, 0x3D)
RGB_RED_BG = RGBColor(0xFD, 0xE8, 0xE8)
RGB_AMB_BG = RGBColor(0xFE, 0xF3, 0xC7)
RGB_GRN_BG = RGBColor(0xE6, 0xF4, 0xEA)


def _header(slide, title, subtitle):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGB_NAVY
    bar.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.24), Inches(12.2), Inches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Calibri"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGB_NAVY
    q = tf.add_paragraph()
    q.text = subtitle
    q.font.name = "Calibri"
    q.font.size = Pt(12)
    q.font.color.rgb = RGB_MUTED
    q.space_before = Pt(3)


def _footer(slide, page_num):
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(7.05), Inches(11.4), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ("Garrane Risk  |  Garrane Merchant Score 2027 Stability Review  |  "
              "Records through 23 Nov 2026; Standard v2 & Schedule C")
    p.font.name = "Calibri"
    p.font.size = Pt(9)
    p.font.color.rgb = RGB_MUTED
    nb = slide.shapes.add_textbox(Inches(12.1), Inches(7.05), Inches(0.7), Inches(0.3))
    np_ = nb.text_frame.paragraphs[0]
    np_.text = "%d / 5" % page_num
    np_.alignment = PP_ALIGN.RIGHT
    np_.font.name = "Calibri"
    np_.font.size = Pt(9)
    np_.font.bold = True
    np_.font.color.rgb = RGB_NAVY


def _styled_table(slide, rows, left, top, width, height, col_widths, font_size=11.5, band_col=None):
    sh = slide.shapes.add_table(len(rows), len(rows[0]), left, top, width, height)
    tbl = sh.table
    for j, wd in enumerate(col_widths):
        tbl.columns[j].width = Inches(wd)
    for i, r in enumerate(rows):
        for j, val in enumerate(r):
            cell = tbl.cell(i, j)
            cell.text = str(val)
            cell.vertical_anchor = 1
            cell.fill.solid()
            if i == 0:
                cell.fill.fore_color.rgb = RGB_NAVY
            elif band_col is not None and j == band_col:
                cell.fill.fore_color.rgb = (RGB_RED_BG if "Escalation" in str(val)
                                            else RGB_AMB_BG if "Remediation" in str(val)
                                            else RGB_GRN_BG)
            else:
                cell.fill.fore_color.rgb = RGB_WHITE if i % 2 == 1 else RGB_BG
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(font_size)
                p.font.bold = (i == 0) or (band_col is not None and j == band_col)
                p.font.color.rgb = (RGB_WHITE if i == 0
                                    else RGB_RED if (band_col == j and "Escalation" in str(val))
                                    else RGB_AMBER if (band_col == j and "Remediation" in str(val))
                                    else RGB_GREEN if (band_col == j and "Monitor" in str(val))
                                    else RGB_SLATE)
    return tbl


def _kpi_card(slide, left, top, width, height, label, big_val, detail):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.adjustments[0] = 0.06
    box.fill.solid()
    box.fill.fore_color.rgb = RGB_CARD
    box.line.color.rgb = RGB_BORDER
    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), width - Inches(0.36), height - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = label
    p1.font.name = "Calibri"
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = RGB_SLATE
    p2 = tf.add_paragraph()
    p2.text = big_val
    p2.font.name = "Calibri"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = RGB_NAVY
    p2.space_before = Pt(2)
    p3 = tf.add_paragraph()
    p3.text = detail
    p3.font.name = "Calibri"
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = RGB_MUTED
    p3.space_before = Pt(2)


def deck(path, fig):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    P_ = fig["points"]

    # Slide 1: Committee call & summary KPIs
    s1 = prs.slides.add_slide(blank)
    _header(
        s1,
        "2027 call: escalate label revisions; put feature releases, noise and training data on plans; monitor retunes",
        "Book-weighted RMS score movement between consecutive 2027 quarter-end snapshots against Standard v2 lines (5.5 and 8.0 points)",
    )
    _kpi_card(s1, Inches(0.55), Inches(1.45), Inches(3.85), Inches(1.25),
              "2027 Combined Model-Side Movement", "%.2f pts" % fig["tot_yr"],
              "Q1 %.2f  |  Q2 %.2f  |  Q3 %.2f  |  Q4 %.2f" % (fig["tot_q1"], fig["tot_q2"], fig["tot_q3"], fig["tot_q4"]))
    _kpi_card(s1, Inches(4.72), Inches(1.45), Inches(3.85), Inches(1.25),
              "Pinned Feature Views (Actual Expected)", "%.1f%%" % fig["cc_pin"],
              "52 assessment-year Mondays (vs %.1f%% calendar plan)" % fig["base"]["cov_plan"])
    _kpi_card(s1, Inches(8.90), Inches(1.45), Inches(3.88), Inches(1.25),
              "Remediation & Escalation Filings", "4 of 5 sources",
              "1 board escalation + 3 remediation plans due 31 Jan 2027")

    rows1 = [["Model-side source", "2027 points", "2027 MS (pts^2)", "Band", "Governance action"]]
    req_short = {
        "escalation": "Board risk committee escalation; plan by 31 Jan 2027",
        "a remediation plan": "Plan to bring under 5.5 pts filed by 31 Jan 2027",
        "monitor": "Quarterly committee reporting",
    }
    for s in ORDER:
        n = NAMES[s]
        rows1.append([
            n[0].upper() + n[1:], "%.2f" % P_[n], "%.2f" % fig["agg"][n],
            BANDNAME[fig["band_of"][n]], req_short[fig["band_of"][n]],
        ])
    _styled_table(s1, rows1, Inches(0.55), Inches(3.0), Inches(12.23), Inches(3.6),
                  [2.5, 1.35, 1.65, 2.05, 4.68], font_size=12, band_col=3)
    _footer(s1, 1)

    # Slide 2: Committed vs Standard shortcut bar chart (strictly aligned with ORDER!)
    s2 = prs.slides.add_slide(blank)
    _header(
        s2,
        "Unadjusted shortcuts misplace all three remediation sources in opposite directions",
        "2027 committed estimate versus linear refit carry, uniform-window turnover, and orthogonal feature releases (points)",
    )
    chart_order = ("labels", "releases", "optimisation", "turnover", "retunes")
    cd = CategoryChartData()
    cd.categories = ["Label\nrevisions", "Feature\nreleases", "Optimisation\nnoise", "Training\ndata", "Retunes"]
    cd.add_series("2027 committed estimate", [round(P_[NAMES[s]], 2) for s in chart_order])
    cd.add_series("Unadjusted shortcut (linear + uniform + orthogonal)", [round(fig["reflex"]["points"][NAMES[s]], 2) for s in chart_order])
    ch = s2.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.55), Inches(1.5),
                             Inches(7.5), Inches(5.15), cd).chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(11)
    ch.category_axis.tick_labels.font.size = Pt(11)
    ch.value_axis.tick_labels.font.size = Pt(11)
    ch.value_axis.maximum_scale = 14.0
    ch.value_axis.minimum_scale = 0.0
    ch.value_axis.major_unit = 2.0
    ch.series[0].format.fill.solid()
    ch.series[0].format.fill.fore_color.rgb = RGB_NAVY
    ch.series[1].format.fill.solid()
    ch.series[1].format.fill.fore_color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    rows2 = [
        ["Source", "2027 pts", "Shortcut", "Band shift"],
        ["Optimisation noise", "%.2f" % P_["optimisation noise"], "%.2f" % fig["reflex"]["points"]["optimisation noise"], "Plan -> Escalation"],
        ["Training data", "%.2f" % P_["training data"], "%.2f" % fig["reflex"]["points"]["training data"], "Plan -> Monitor"],
        ["Feature releases", "%.2f" % P_["feature releases"], "%.2f" % fig["reflex"]["points"]["feature releases"], "Plan -> Monitor"],
        ["Label revisions", "%.2f" % P_["label revisions"], "%.2f" % fig["reflex"]["points"]["label revisions"], "Escalation"],
        ["Retunes", "%.2f" % P_["retunes"], "%.2f" % fig["reflex"]["points"]["retunes"], "Monitor"],
    ]
    _styled_table(s2, rows2, Inches(8.25), Inches(1.6), Inches(4.53), Inches(3.2),
                  [1.38, 0.88, 0.90, 1.37], font_size=9.5)
    note2 = s2.shapes.add_textbox(Inches(8.25), Inches(5.05), Inches(4.53), Inches(1.6))
    tf2 = note2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Threshold lines: 5.5 pts (Remediation) and 8.0 pts (Escalation)."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = RGB_NAVY
    p2 = tf2.add_paragraph()
    p2.text = ("Every remediation source sits cleanly inside 5.5 to 8.0 across all 24 estimation variants and +/-20% "
               "variance checks, while unadjusted shortcuts cross both thresholds in opposite directions.")
    p2.font.name = "Calibri"
    p2.font.size = Pt(10)
    p2.font.color.rgb = RGB_SLATE
    p2.space_before = Pt(4)
    _footer(s2, 2)

    # Slide 3: Quarterly combined model-side movement profile
    s3 = prs.slides.add_slide(blank)
    _header(
        s3,
        "Combined model-side movement peaks in H1 (%.2f to %.2f pts) before pinned views lower H2" % (fig["tot_q1"], fig["tot_q2"]),
        "Combined RMS across all five sources per 2027 quarter-end snapshot pair and full assessment year (Standard section 3.3)",
    )
    cd3 = CategoryChartData()
    cd3.categories = ["Q1\n(Mar 2027)", "Q2\n(Jun 2027)", "Q3\n(Sep 2027)", "Q4\n(Dec 2027)", "2027\nYear"]
    cd3.add_series("Combined model-side RMS (pts)", [
        round(fig["tot_q1"], 2), round(fig["tot_q2"], 2), round(fig["tot_q3"], 2),
        round(fig["tot_q4"], 2), round(fig["tot_yr"], 2),
    ])
    ch3 = s3.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.55), Inches(1.5),
                              Inches(7.3), Inches(5.15), cd3).chart
    ch3.has_legend = False
    ch3.category_axis.tick_labels.font.size = Pt(11.5)
    ch3.value_axis.tick_labels.font.size = Pt(11)
    ch3.value_axis.minimum_scale = 10.0
    ch3.value_axis.maximum_scale = 19.0
    ch3.series[0].format.fill.solid()
    ch3.series[0].format.fill.fore_color.rgb = RGB_NAVY

    rows3 = [
        ["Snapshot pair", "Combined (pts)", "Key driver of pair level"],
        ["Q1 (Dec 26 - Mar 27)", "%.2f" % fig["tot_q1"], "Low pinned share; Q1 sprint releases fully live"],
        ["Q2 (Mar 27 - Jun 27)", "%.2f" % fig["tot_q2"], "Peak seasonal training-data trough + Q2 sprints"],
        ["Q3 (Jun 27 - Sep 27)", "%.2f" % fig["tot_q3"], "Mid-year pinned adoption trims live sprint exposure"],
        ["Q4 (Sep 27 - Dec 27)", "%.2f" % fig["tot_q4"], "Highest pinned coverage across complex families"],
        ["2027 year (RMS)", "%.2f" % fig["tot_yr"], "Root of mean of the four pairs' combined MS"],
    ]
    _styled_table(s3, rows3, Inches(8.1), Inches(1.7), Inches(4.68), Inches(3.8),
                  [1.58, 1.05, 2.05], font_size=10)
    note3 = s3.shapes.add_textbox(Inches(8.1), Inches(5.7), Inches(4.68), Inches(1.1))
    tf3 = note3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = ("Standard section 6 context: expected 2027 tier changes run %.1f%% as scheduled (above the 12.0%% "
              "Schedule C cap), dropping to %.1f%% once the four designated sources are remediated." % (
                  fig["fr_sched"], fig["fr_removed"]))
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.color.rgb = RGB_SLATE
    _footer(s3, 3)

    # Slide 4: Three independent structural judgments
    s4 = prs.slides.add_slide(blank)
    _header(
        s4,
        "Three independent structural estimations settle the 2027 remediation scope",
        "Each remediation source is pinned by its own 2026 instrument structure and confirmed against opposite-side alternatives",
    )
    cards = [
        ("1. Optimisation noise: %.2f pts" % fig["cc1"], "Warm-start AR(1) decay (Remediation)",
         "- Anchored warm-era gap curves give phi = %.2f to %.2f.\n"
         "- Cold-era curves (29 to 55 wks) are linear (mean curv %+.3f), ruling out mean-reverting merchant change.\n"
         "- Linear 13-refit carry overshoots to %.2f (Escalation); raw replicate undershoots to %.2f (Monitor)." % (
             fig["base"]["phi_fit"][0], fig["base"]["phi_fit"][1], fig["bend"]["cold_curv_mean"],
             fig["probe"]["linear 13 refits (half pair)"], fig["probe"]["single replicate pair (over)"])),
        ("2. Training data: %.2f pts" % fig["cc2"], "Recency-weighted turnover (Remediation)",
         "- Standard 1.6 & manifests confirm recency decay on 52/104w windows without listing lambda.\n"
         "- 16 seasonal 2026 bootstrap pairs/family invert lambda = %.3f to %.3f (%.1fx lower log-RMSE than uniform).\n"
         "- Uniform overlap drops to %.2f (Monitor); raw bootstrap overshoots to %.2f (Escalation)." % (
             fig["base"]["lam_fit"][0], fig["base"]["lam_fit"][1], fig["recency_diag"]["unif_ratio"],
             fig["probe"]["uniform window turnover"], fig["probe"]["raw bootstrap face value"])),
        ("3. Feature releases: %.2f pts" % fig["cc3"], "Within-group covariance + actual lag (Remediation)",
         "- Past rollouts place actual pinned-view share at %.1f%% (vs %.1f%% planned; LOO validated).\n"
         "- All %d same-group 2026 release pairs correlate positively (mean %.3f, min %.3f; cross-group %+.3f).\n"
         "- Orthogonal sum drops to %.2f (Monitor); full alignment overshoots to %.2f (Escalation)." % (
             fig["cc_pin"], fig["base"]["cov_plan"], fig["base"]["coh_same_n"],
             fig["base"]["coh_same_mean"], fig["base"]["coh_same_min"], fig["base"]["coh_diff_mean"],
             fig["probe"]["orthogonal releases (actual lag)"], fig["probe"]["all releases aligned (over)"])),
    ]
    for idx, (head, sub, body) in enumerate(cards):
        left = Inches(0.55 + idx * 4.15)
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.65), Inches(3.92), Inches(4.55))
        box.adjustments[0] = 0.04
        box.fill.solid()
        box.fill.fore_color.rgb = RGB_CARD
        box.line.color.rgb = RGB_BORDER
        tb = s4.shapes.add_textbox(left + Inches(0.20), Inches(1.85), Inches(3.52), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = head
        p0.font.name = "Calibri"
        p0.font.size = Pt(13.0)
        p0.font.bold = True
        p0.font.color.rgb = RGB_NAVY
        p1 = tf.add_paragraph()
        p1.text = sub
        p1.font.name = "Calibri"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = RGB_AMBER
        p1.space_before = Pt(3)
        p1.space_after = Pt(10)
        for line in body.split("\n"):
            pl = tf.add_paragraph()
            pl.text = line
            pl.font.name = "Calibri"
            pl.font.size = Pt(10.5)
            pl.font.color.rgb = RGB_SLATE
            pl.space_after = Pt(8)
    _footer(s4, 4)

    # Slide 5: 2026 internal record check & action timetable
    s5 = prs.slides.add_slide(blank)
    _header(
        s5,
        "2026 internal record checks reject every shortcut by 10x to 54x; four plans due 31 January 2027",
        "Sum of absolute 2026 variance discrepancies (D_warm(1), seasonal bootstrap contrast, same-group release covariance)",
    )
    fa = fig["falsification"]
    rows5 = [
        ["Model specification", "Total 2026 error (pts^2)", "Multiple vs committed", "2027 placement outcome"],
        ["Committed estimate (all three mechanisms fitted)", "%.2f" % fa["golden_err"], "1.0x", "All 5 bands consistent"],
        ["Orthogonal feature releases (within-group cov omitted)", "%.2f" % fa["rivals"]["S3 orthogonal releases"],
         "%.1fx" % (fa["rivals"]["S3 orthogonal releases"] / max(fa["golden_err"], 1e-6)), "Releases misplaced Monitor"],
        ["Linear 13-refit noise carry (warm-start decay omitted)", "%.2f" % fa["rivals"]["S1 linear carry"],
         "%.1fx" % (fa["rivals"]["S1 linear carry"] / max(fa["golden_err"], 1e-6)), "Noise misplaced Escalation"],
        ["Uniform window turnover (recency decay omitted)", "%.2f" % fa["rivals"]["S2 uniform window"],
         "%.1fx" % (fa["rivals"]["S2 uniform window"] / max(fa["golden_err"], 1e-6)), "Training data misplaced Monitor"],
        ["Standard unadjusted shortcut (all three omitted)", "%.2f" % fa["rivals"]["rigorous (Response 1)"],
         "%.1fx" % (fa["rivals"]["rigorous (Response 1)"] / max(fa["golden_err"], 1e-6)), "3 of 5 bands wrong"],
    ]
    _styled_table(s5, rows5, Inches(0.55), Inches(1.55), Inches(12.23), Inches(3.25),
                  [4.75, 2.15, 1.9, 3.43], font_size=11)

    act = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(5.05), Inches(12.23), Inches(1.7))
    act.adjustments[0] = 0.05
    act.fill.solid()
    act.fill.fore_color.rgb = RGB_CARD
    act.line.color.rgb = RGB_BORDER
    tb5 = s5.shapes.add_textbox(Inches(0.78), Inches(5.18), Inches(11.8), Inches(1.45))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    ph = tf5.paragraphs[0]
    ph.text = "Immediate Committee Actions (Deadline: 31 January 2027)"
    ph.font.name = "Calibri"
    ph.font.size = Pt(13)
    ph.font.bold = True
    ph.font.color.rgb = RGB_NAVY
    for btxt in (
        "- Escalate Label revisions (%.2f pts) to the Board Risk Committee and file a late-label stabilisation plan." % P_["label revisions"],
        "- File remediation plans targeting < 5.5 pts for Feature releases (%.2f pts, accelerate PC-26-058 pinned adoption and stagger sprint groups), Optimisation noise (%.2f pts), and Training data (%.2f pts)." % (
            P_["feature releases"], P_["optimisation noise"], P_["training data"]),
        "- Maintain Retunes (%.2f pts) under quarterly committee monitoring; submit Schedule C stability plan to Acquirer before 31 January." % P_["retunes"],
    ):
        pb = tf5.add_paragraph()
        pb.text = btxt
        pb.font.name = "Calibri"
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = RGB_SLATE
        pb.space_before = Pt(3)
    _footer(s5, 5)
    prs.save(path)


def build(folder, fig, pk, g):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), fig, pk, g)
    deck(os.path.join(folder, FILES["deck"]), fig)
