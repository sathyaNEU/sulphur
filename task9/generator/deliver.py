"""task9 architecture 5, the golden deliverables: the model risk team's workbook of 2027 placements and the few
slides for the committee, both leading with the call. Every figure comes from results.py (figures.json) or from
the golden route's own arrays on the loaded pack, at the blocks' rounding."""
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Emu, Inches, Pt

import core as C
import load as L
import pack as P
import results as RS

FILES = {"wb": "garrane_score_stability_sources_2027.xlsx", "deck": "garrane_stability_review_2027.pptx"}
NAMES = RS.NAMES
ORDER = RS.ORDER
BANDNAME = {"monitor": "Monitor", "a remediation plan": "Remediation plan", "escalation": "Escalation"}
NAVY = "1F3A5F"
THIN = Side(style="thin", color="B7BEC8")


def _hdr(ws, row, ncol):
    for j in range(1, ncol + 1):
        c = ws.cell(row=row, column=j)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="center")


def _box(ws, r0, r1, ncol):
    for r in range(r0, r1 + 1):
        for j in range(1, ncol + 1):
            ws.cell(row=r, column=j).border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)


def _cols(ws, widths):
    from openpyxl.utils import get_column_letter
    for j, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = wd


def _fmt(ws, row, col, f):
    ws.cell(row=row, column=col).number_format = f


def workbook(path, fig, pk, g):
    codes = pk.w["codes"]
    wt = pk.w["merch"] / pk.w["merch"].sum()
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 placements"
    ws["A1"] = "Garrane Merchant Score: model-side sources of movement, 2027 assessment"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Points a source alone moves a merchant's score between consecutive quarter-end snapshots in 2027, "
                "book weighted, against the standard's lines of 5.5 and 8 points. Records to the refresh of 23 November 2026.")
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 30
    ws.append([])
    ws.append(["Source", "Points, 2027", "Band", "What it requires"])
    _hdr(ws, 4, 4)
    req = {"monitor": "quarterly reporting", "a remediation plan": "plan filed by 31 January 2027",
           "escalation": "board risk committee, plan filed by 31 January 2027"}
    for s in ORDER:
        n = NAMES[s]
        ws.append([n[0].upper() + n[1:], round(fig["points"][n], 2), BANDNAME[fig["band_of"][n]],
                   req[fig["band_of"][n]]])
        _fmt(ws, ws.max_row, 2, "0.00")
    _box(ws, 4, ws.max_row, 4)
    ws.append([])
    r0 = ws.max_row + 1
    ws.append(["Measure", "2027", "", "Note"])
    _hdr(ws, r0, 4)
    ws.append(["Share of 2027's weekly retrains expected to run on pinned feature views (%)", round(fig["cc3"], 1), "",
               "family-weeks, 28 December 2026 to 20 December 2027"])
    for r in range(r0 + 1, ws.max_row + 1):
        _fmt(ws, r, 2, "0.0")
    _box(ws, r0, ws.max_row, 4)
    _cols(ws, (58, 14, 18, 62))
    ws.freeze_panes = "A5"

    # instruments by family
    s2 = wb.create_sheet("Instruments by family")
    s2.append(["Family", "Scored merchants, 21 Sep 2026", "Book weight", "Replicate pairs, mean-square difference",
               "Bootstrap pairs, mean-square difference", "Bootstrap net of replicate", "Retune shadows",
               "Release shadows", "Label freezes", "Bootstrap runs' training rows"])
    _hdr(s2, 1, 10)
    I = pk.inst
    for f in range(C.F):
        s2.append([codes[f], int(pk.w["merch"][f]), round(float(wt[f]), 4), round(float(I["rep"][f]), 2),
                   round(float(I["boot"][f]), 1), round(float(g["face"][f]), 1), round(float(I["ret"][f]), 2),
                   round(float(I["rel"][f]), 2), round(float(I["lab"][f]), 2), int(round(I["boot_n"][f]))])
        for j, fm in ((2, "#,##0"), (3, "0.0000"), (10, "#,##0")):
            _fmt(s2, s2.max_row, j, fm)
    s2.append(["Book weighted", int(pk.w["merch"].sum()), 1.0] +
              [round(float((wt * v).sum()), 2) for v in (I["rep"], I["boot"], g["face"], I["ret"], I["rel"], I["lab"])] + [""])
    s2.cell(row=s2.max_row, column=1).font = Font(bold=True)
    _fmt(s2, s2.max_row, 2, "#,##0")
    _box(s2, 1, s2.max_row, 10)
    _cols(s2, (10, 16, 11, 16, 16, 14, 12, 12, 12, 16))
    s2.freeze_panes = "B2"

    # training data
    s3 = wb.create_sheet("Training data")
    s3.append(["Family", "Window (weeks)", "Per-row noise (mean-square x rows)", "Turned-over factor, 2026 pairs",
               "Turned-over factor, 2027 pairs", "Mean-square movement, 2027", "Points, 2027"])
    _hdr(s3, 1, 7)
    w = pk.w
    for f in range(C.F):
        t26 = np.mean([C.turnover_factor(w, f, a, b, w["window"][f]) for a, b in C.SPANS26])
        t27 = np.mean([C.turnover_factor(w, f, a, b, w["window"][f]) for a, b in C.SPANS27])
        s3.append([codes[f], int(w["window"][f]), round(float(g["row2"][f]), 0), float("%.4g" % t26),
                   float("%.4g" % t27), round(float(g["tur"][f]), 2), round(math.sqrt(float(g["tur"][f])), 2)])
        _fmt(s3, s3.max_row, 3, "#,##0")
        _fmt(s3, s3.max_row, 4, "0.000E+00")
        _fmt(s3, s3.max_row, 5, "0.000E+00")
    s3.append(["Book weighted", "", "", "", "", round(float((wt * g["tur"]).sum()), 2), round(fig["points"]["training data"], 2)])
    s3.cell(row=s3.max_row, column=1).font = Font(bold=True)
    _box(s3, 1, s3.max_row, 7)
    _cols(s3, (10, 12, 18, 18, 18, 18, 12))

    # gap curves
    s4 = wb.create_sheet("Gap curves")
    s4.append(["Family", "Settled from", "Persistence", "Level", "Optimisation, 13 weeks", "Points"] +
              ["Gap %d" % h for h in range(1, 27)])
    _hdr(s4, 1, 32)
    for f in range(C.F):
        s4.append([codes[f], P.monday(pk.t0[f]), round(float(g["phi"][f]), 4), round(float(g["A"][f]), 2),
                   round(float(g["opt13"][f]), 2), round(math.sqrt(float(g["opt13"][f])), 2)] +
                  [round(float(x), 1) for x in pk.curves[f][:26]])
        _fmt(s4, s4.max_row, 2, "dd/mm/yyyy")
    s4.append(["Book weighted", "", "", "", round(float((wt * g["opt13"]).sum()), 2), round(fig["points"]["optimisation noise"], 2)])
    s4.cell(row=s4.max_row, column=1).font = Font(bold=True)
    _box(s4, 1, s4.max_row, 32)
    _cols(s4, [10, 12, 11, 9, 13, 8] + [7] * 26)
    s4.freeze_panes = "B2"

    # pinned feature views
    s5 = wb.create_sheet("Pinned feature views")
    m = pk.models["loglin"]
    s5.append(["Family", "Custom training components", "Planned week", "Median weeks to first use",
               "Share of 2027 retrains on pinned views (%)", "Release shadows", "Feature releases, points 2027"])
    _hdr(s5, 1, 7)
    exp = C.release_exposure(w, g["cov"])
    for f in range(C.F):
        s5.append([codes[f], int(w["custom"][f]), P.monday(int(w["fv_planned"][f])), round(math.exp(m["mu"][f]), 1),
                   round(100.0 * float(np.mean(g["cov"][f, 1:])), 1), round(float(pk.inst["rel"][f]), 2),
                   round(math.sqrt(float(pk.inst["rel"][f] * exp[f])), 2)])
        _fmt(s5, s5.max_row, 3, "dd/mm/yyyy")
    s5.append(["All families", "", "", "", round(fig["cc3"], 1), "", round(fig["points"]["feature releases"], 2)])
    s5.cell(row=s5.max_row, column=1).font = Font(bold=True)
    _box(s5, 1, s5.max_row, 7)
    s5.append([])
    s5.append(["Past rollouts left out one at a time", "Share of first 39 weeks on, record (%)", "Model without it (%)"])
    _hdr(s5, s5.max_row, 3)
    for k, lab in (("runtime", "Runtime image 4.1.0"), ("warm", "Warm start and long window"), ("amp", "Mixed precision")):
        s5.append([lab, round(100 * fig["loo"][k]["record"], 1), round(100 * fig["loo"][k]["model"], 1)])
    _cols(s5, (34, 18, 14, 16, 20, 14, 16))

    # the check
    s6 = wb.create_sheet("Weekly check")
    s6.append(["Route", "Weekly score-change variance it implies", "Record, settled warm weeks", "Off by"])
    _hdr(s6, 1, 4)
    fa = fig["falsification"]
    rows = [("This assessment", fa["golden"])] + [(k[0].upper() + k[1:], v) for k, v in fa["rivals"].items()]
    for k, v in rows:
        s6.append([k, round(v, 2), round(fa["record"], 2), round(v - fa["record"], 2)])
    _box(s6, 1, s6.max_row, 4)
    _cols(s6, (44, 22, 18, 10))

    # hurried routes
    s7 = wb.create_sheet("Other routes")
    s7.append(["Route", "Optimisation noise", "Training data", "Retunes", "Feature releases", "Label revisions",
               "Bands it files"])
    _hdr(s7, 1, 7)
    show = [("Bootstrap pairs as the movement, refits' noise added in full", fig["reflex"]),
            ("Bootstrap pairs with the seeds left in, refits added in full, calendar planned weeks", fig["direct"])]
    for k, e in show:
        p = e["points"]
        s7.append([k] + [round(p[NAMES[s]], 2) for s in C.SOURCES] +
                  ["; ".join(e["call"])])
    _box(s7, 1, s7.max_row, 7)
    _cols(s7, (44, 12, 12, 10, 12, 12, 80))

    s8 = wb.create_sheet("Notes")
    day = lambda t: "%d %s" % (P.monday(t).day, P.monday(t).strftime("%B %Y"))
    for line in (
            ["Notes"],
            ["Records to the refresh of %s; the assessment year is the four snapshot pairs closing on 22 March, "
             "21 June, 20 September and 20 December 2027 (covenant schedule, C2)." % day(C.T - 1)],
            ["Points are root-mean-square score points between consecutive quarter-end snapshots, the root of the "
             "mean of the four pairs' mean-square changes, book weighted by scored merchants at the %s snapshot "
             "(stability standard, 3.1 and 3.2)." % day(C.SPANS26[-1][1])],
            ["Bands: monitor under 5.5 points, remediation plan 5.5 to under 8, escalation 8 or more (4.1)."],
            ["Panel: where a weekly refresh was re-sent, the later load is used; Tolka Pay merchants re-keyed from "
             "the refresh of %d %s are joined through the migration map." % (
                 P.monday(P.MIGRATION_T).day, P.monday(P.MIGRATION_T).strftime("%B %Y"))],
            ["Feature releases for 2027 are the roadmap as filed; labelled rows for 2027 are the data plan as filed "
             "(standard, 2.1)."]):
        s8.append(line)
    s8["A1"].font = Font(bold=True)
    _cols(s8, (140,))
    wb.save(path)


def _title(slide, text, sub=None):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(12.3), Inches(0.9))
    p = tb.text_frame.paragraphs[0]
    p.text = text
    p.font.size, p.font.bold = Pt(26), True
    p.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
    if sub:
        q = tb.text_frame.add_paragraph()
        q.text = sub
        q.font.size = Pt(13)
        q.font.color.rgb = RGBColor(0x55, 0x5E, 0x6B)


def _table(slide, rows, left, top, width, height, widths=None, size=13):
    sh = slide.shapes.add_table(len(rows), len(rows[0]), left, top, width, height)
    tbl = sh.table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            cell = tbl.cell(i, j)
            cell.text = str(v)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(size)
                p.font.bold = i == 0
    if widths:
        for j, wd in enumerate(widths):
            tbl.columns[j].width = Inches(wd)
    return tbl


def _strip(slide, n):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(12.3), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = ("Source: model risk instrument pairs, training scheduler runs, monitoring panel and change calendar to "
              "23 November 2026; stability standard 2026; Schedule C.      %d" % n)
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)


def deck(path, fig):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    _title(s, "2027: label revisions to escalation; optimisation noise, feature releases and training data to "
              "remediation plans; retunes stay on monitor",
           "Points a source alone moves a merchant's score between quarter-end snapshots in 2027 (lines 5.5 and 8)")
    rows = [["Source", "Points", "Band"]]
    for k in ORDER:
        n = NAMES[k]
        rows.append([n[0].upper() + n[1:], "%.2f" % fig["points"][n], BANDNAME[fig["band_of"][n]]])
    _table(s, rows, Inches(0.6), Inches(1.9), Inches(8.2), Inches(2.9), widths=(3.8, 1.8, 2.6), size=15)
    tb = s.shapes.add_textbox(Inches(9.2), Inches(1.9), Inches(3.7), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(("%.1f per cent of 2027's weekly retrains are expected to actually run on pinned feature views." % fig["cc3"],
                              "Feature releases move scores only in the weeks a family still reads live views, "
                              "so they stay on a plan at %.2f points." % fig["points"]["feature releases"])):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(15)
        p.space_after = Pt(10)

    s = prs.slides.add_slide(blank)
    _title(s, "Four of five sources sit above the plan line",
           "Points, 2027; dashed lines at the standard's 5.5 (remediation plan) and 8 (escalation)")
    cd = CategoryChartData()
    cats = [NAMES[k][0].upper() + NAMES[k][1:] for k in reversed(ORDER)]
    vals = [round(fig["points"][NAMES[k]], 2) for k in reversed(ORDER)]
    cd.categories = cats
    cd.add_series("Points, 2027", vals)
    L, Tp, W, H = Inches(0.7), Inches(1.6), Inches(11.8), Inches(5.4)
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, L, Tp, W, H, cd)
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = False
    va = ch.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = 0, 12, 2
    va.has_major_gridlines = False
    pl = ch.plots[0]
    pl.gap_width = 60
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.00"
    pl.data_labels.number_format_is_linked = False
    col = {"monitor": (0x7A, 0x8C, 0x9E), "a remediation plan": (0xE0, 0xA4, 0x3A), "escalation": (0xB8, 0x3B, 0x3B)}
    for i, k in enumerate(reversed(ORDER)):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor(*col[fig["band_of"][NAMES[k]]])
    X0, Y0, WF, HF = 0.22, 0.04, 0.74, 0.86          # the plot's inner area, fixed so the lines can be placed
    pa = ch._chartSpace.chart.plotArea
    from lxml import etree
    ns = "http://schemas.openxmlformats.org/drawingml/2006/chart"
    lay = etree.SubElement(pa, "{%s}layout" % ns)
    pa.remove(lay)
    pa.insert(0, lay)
    ml = etree.SubElement(lay, "{%s}manualLayout" % ns)
    for tag, val in (("layoutTarget", "inner"), ("xMode", "edge"), ("yMode", "edge"), ("x", X0), ("y", Y0),
                     ("w", WF), ("h", HF)):
        etree.SubElement(ml, "{%s}%s" % (ns, tag)).set("val", str(val))
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    for v, rgb in ((5.5, (0xE0, 0xA4, 0x3A)), (8.0, (0xB8, 0x3B, 0x3B))):
        x = L + int(W * (X0 + WF * v / 12.0))
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, Tp + int(H * Y0), x, Tp + int(H * (Y0 + HF)))
        ln.line.color.rgb = RGBColor(*rgb)
        ln.line.width = Pt(1.75)
        ln.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    s = prs.slides.add_slide(blank)
    b, pr = fig["base"], fig["probe"]
    _title(s, "%.1f per cent of 2027's retrains are expected to run on pinned views, not the calendar's %.1f" % (
               fig["cc3"], b["cov_plan"]),
           "Weekly refreshes of the four snapshot pairs closing in 2027, family-weeks across the fourteen families")
    _table(s, [["Reading", "On pinned views (%)", "Feature releases, points"],
               ["The change calendar's planned weeks", "%.1f" % b["cov_plan"],
                "%.2f" % pr["feature releases on the calendar's planned weeks"]],
               ["The change calendar's completed dates", "%.1f" % b["cov_declared"],
                "%.2f" % fig["rigorous"]["points"]["feature releases"]],
               ["Expected actual use, from the three past rollouts", "%.1f" % fig["cc3"],
                "%.2f" % fig["points"]["feature releases"]]],
           Inches(0.8), Inches(2.0), Inches(11.6), Inches(2.6), widths=(6.4, 2.6, 2.6), size=16)
    for n, sl in enumerate(prs.slides, 1):
        _strip(sl, n)
    prs.save(path)


def build(folder, fig, pk, g):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), fig, pk, g)
    deck(os.path.join(folder, FILES["deck"]), fig)
