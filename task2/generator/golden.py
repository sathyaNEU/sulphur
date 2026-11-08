"""task2 architecture 4: the golden deliverables from the solution on the cut pack. The resource workbook (the
grade-tonnage table at block support, the declustering, the variogram and the block variance, the composites'
and the kriged model's tables for comparison) and the board deck with its chart."""
import datetime as dt
import math

import openpyxl
from openpyxl.styles import Font
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Emu, Inches, Pt

import ooxml
import solve as S


def r50(oz):
    return int(50000 * math.floor(oz / 50000 + 0.5))


def workbook(g, rungs, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Grade-tonnage"
    b = Font(bold=True)
    ws.append(["Stage 5, 5 m x 5 m x 2.5 m mining blocks (block support)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Cut-off (g/t)", "Tonnes (Mt)", "Grade (g/t)", "Contained gold (koz)"])
    for c in ws[3]:
        c.font = b
    for c in S.CUTS:
        x = g["gt"][c]
        ws.append([c, round(x["t"] / 1e6, 2), round(x["g"], 2), round(x["oz"] / 1e3, 1)])
    ws.append([])
    oz = g["gt"][S.CUT]["oz"]
    ws.append(["Gold above the agreement's %.1f g/t cut-off (oz, nearest 50,000)" % S.CUT, r50(oz)])
    ws.append(["Tier the gold covers", "Tier %s (%s oz)" % (g["tier"], "{:,}".format(dict(S.TIERS)[g["tier"]] * 1000))])
    for row in ws.iter_rows(min_row=ws.max_row - 1, max_row=ws.max_row):
        for c in row:
            c.font = b
    d = wb.create_sheet("Declustering")
    d.append(["Quantity", "Value"])
    for c in d[1]:
        c.font = b
    d.append(["Stage 5 composites (2.5 m flitch)", g["n"]])
    d.append(["Holes with Stage 5 composites", g["holes"]])
    d.append(["Mean grade, composites as drilled (g/t)", round(g["mean_raw"], 3)])
    d.append(["Mean grade, declustered on 25 m cells by flitch (g/t)", round(g["mean_decl"], 3)])
    d.append(["Coefficient of variation, declustered composites", round(g["cv_decl"], 3)])
    d.append(["Stage 5 tonnes (Mt)", round(g["T"] / 1e6, 2)])
    for z in ("OX", "TR", "FR"):
        d.append(["Mean dry bulk density, %s (t/m3)" % z, round(g["rho"][z], 3)])
    v = wb.create_sheet("Variogram")
    v.append(["Experimental", "Lag (m)", "Gamma (g/t)^2", "Pairs"])
    for c in v[1]:
        c.font = b
    for a, gm, n in g["dh"]:
        v.append(["downhole", round(a, 1), round(gm, 4), n])
    for a, gm, n in g["hz"]:
        v.append(["across holes", round(a, 1), round(gm, 4), n])
    c0, c1, a1, a2, r = g["model"]
    v.append([])
    v.append(["Model (share of the sill)", "nugget %.2f; spherical %.2f, range %d m; spherical %.2f, range %d m; "
              "vertical ranges x %.1f" % (c0, c1, a1, 1 - c0 - c1, a2, r)])
    v.append(["Average of the model within a 5 x 5 x 2.5 m block", round(g["gamma_bar"], 3)])
    v.append(["Block variance as a share of the composites'", round(g["ratio"], 3)])
    k = wb.create_sheet("Comparison")
    k.append(["Cut-off (g/t)", "Declustered composites (koz)", "Kriged block model (koz)", "Mining blocks (koz)"])
    for c in k[1]:
        c.font = b
    for c in S.CUTS:
        k.append([c, round(rungs["rung1_declustered"]["gt"][str(c)]["oz"] / 1e3, 1),
                  round(rungs["kriged"]["gt"][str(c)]["oz"] / 1e3, 1), round(g["gt"][c]["oz"] / 1e3, 1)])
    for s in wb.worksheets:
        for col in s.columns:
            s.column_dimensions[col[0].column_letter].width = max(12, min(70, max(len(str(x.value or "")) for x in col) + 2))
    wb.properties.creator = "Ironbark Gold"
    wb.properties.lastModifiedBy = "Ironbark Gold"
    wb.save(path)
    ooxml.normalize(path, dt.datetime(2026, 11, 5, 1, 20), dt.datetime(2026, 11, 6, 6, 45), "Ironbark Gold")


def deck(g, rungs, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    tier_oz = dict(S.TIERS)
    oz = g["gt"][S.CUT]["oz"]

    def text(slide, x, y, w, h, lines, size=18, bold_first=False):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = ln
            p.font.size = Pt(size)
            p.font.bold = bold_first and i == 0
        return tb
    s1 = prs.slides.add_slide(blank)
    text(s1, 0.6, 0.35, 12, 0.9, ["Commit Stage 5 to Tier %s of the Yarrabin agreement" % g["tier"]], 30, True)
    text(s1, 0.6, 1.15, 12.2, 1.0,
         ["Stage 5's mining blocks at %.1f g/t or more hold about %s oz, above Tier %s (%s oz) and short of Tier C "
          "(%s oz)." % (S.CUT, "{:,}".format(r50(oz)), g["tier"], "{:,}".format(tier_oz[g["tier"]] * 1000),
                        "{:,}".format(tier_oz["C"] * 1000))], 18)
    cd = CategoryChartData()
    cd.categories = ["%.1f" % c for c in S.CUTS]
    cd.add_series("Mining blocks (koz)", [round(g["gt"][c]["oz"] / 1e3, 1) for c in S.CUTS])
    cd.add_series("Declustered composites (koz)", [round(rungs["rung1_declustered"]["gt"][str(c)]["oz"] / 1e3, 1)
                                                   for c in S.CUTS])
    cd.add_series("Kriged block model (koz)", [round(rungs["kriged"]["gt"][str(c)]["oz"] / 1e3, 1) for c in S.CUTS])
    for t, v in S.TIERS:
        cd.add_series("Tier %s (%d koz)" % (t, v), [v] * len(S.CUTS))
    gf = s1.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.6), Inches(2.0), Inches(8.6), Inches(5.1), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.RIGHT
    ch.legend.include_in_layout = False
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "Contained gold above the cut-off (koz)"
    ch.category_axis.has_title = True
    ch.category_axis.axis_title.text_frame.text = "Cut-off grade (g/t)"
    cols = [(25, 70, 150), (150, 150, 150), (120, 160, 210), (200, 60, 60), (200, 60, 60), (200, 60, 60)]
    for ser, col in zip(ch.series, cols):
        ser.format.line.color.rgb = RGBColor(*col)
        ser.format.line.width = Emu(38100 if col == cols[0] else 19050)
        ser.smooth = False
    text(s1, 9.5, 2.2, 3.5, 4.6,
         ["At the 2.5 g/t cut-off:",
          "Mining blocks: %d koz" % round(oz / 1e3),
          "Declustered composites: %d koz" % round(rungs["rung1_declustered"]["oz"] / 1e3),
          "Kriged block model: %d koz" % round(rungs["kriged"]["oz"] / 1e3),
          "",
          "The composites spread wider than a 5 m x 5 m x 2.5 m block; the kriged model narrower."], 14, True)
    s2 = prs.slides.add_slide(blank)
    text(s2, 0.6, 0.35, 12, 0.8, ["How the block gold was read"], 26, True)
    text(s2, 0.6, 1.2, 12.2, 5.8, [
        "1. %d Stage 5 composites (2.5 m flitches) from %d holes; the 2022 to 2024 infill sits where the 2019 to 2021 "
        "grid ran high, so the composites as drilled average %.2f g/t and %.2f g/t declustered on the 25 m grid's cells."
        % (g["n"], g["holes"], g["mean_raw"], g["mean_decl"]),
        "2. Variogram: nugget %d per cent of the sill, a %d m and a %d m structure; within a 5 m x 5 m x 2.5 m block the "
        "model averages %.2f of the sill, so a block's grades vary %.2f times as much as a composite's."
        % (round(g["model"][0] * 100), g["model"][2], g["model"][3], g["gamma_bar"], g["ratio"]),
        "3. The declustered composite distribution carried to that block variance (lognormal-shaped correction) gives "
        "the grade-tonnage curve of the mining blocks; Stage 5 tonnes from the flitch outlines and the oxide, "
        "transitional and fresh densities (%.1f Mt)." % (g["T"] / 1e6),
        "4. The composites themselves put %d koz above 2.5 g/t (Tier C) and the kriged model %d koz (Tier A); the "
        "kriging validates point by point, but its block estimates vary less than the blocks do."
        % (round(rungs["rung1_declustered"]["oz"] / 1e3), round(rungs["kriged"]["oz"] / 1e3)),
        "Working: stage5_high_grade_resource.xlsx"], 16)
    prs.core_properties.author = "Ironbark Gold"
    prs.core_properties.last_modified_by = "Ironbark Gold"
    prs.core_properties.title = "Stage 5 OPA tier"
    prs.save(path)
    ooxml.normalize(path, dt.datetime(2026, 11, 5, 2, 10), dt.datetime(2026, 11, 6, 7, 5), "Ironbark Gold")


def write(g, rungs, gdir):
    import os
    os.makedirs(gdir, exist_ok=True)
    workbook(g, rungs, os.path.join(gdir, "stage5_high_grade_resource.xlsx"))
    deck(g, rungs, os.path.join(gdir, "stage5_OPA_tier_board.pptx"))
