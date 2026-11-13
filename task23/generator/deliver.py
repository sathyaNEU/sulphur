"""task23 architecture 1, the golden deliverables: the landfill gas engineer's workbook (the package call against the
Council's limit, the 2025 bridge from the report and the survey to what the site emitted, cell 4's wells since
recirculation, cell 5's 2027 generation and its cover's oxidation, 2027 by cell under each package) and the short
deck for the Council's January 2027 budget amendment, both from the golden run that writes figures.json."""
import math
import os

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_LABEL_POSITION
from pptx.util import Emu, Pt

import analysis as A
import params as P
import postprocess

WORKBOOK = "fernhallow_methane_2025_2027.xlsx"
DECK = "council_briefing_2027_gas_package.pptx"
INK, MUTED, BLUE, GRAY, RED = "1F1F1F", "6B6B6B", "2A78D6", "B5B4AE", "C0504D"
T0 = "#,##0"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WORKS = {"A": "No new works (cell 5 collection at final grade in 2029)",
         "B": "Horizontal collectors in cell 5 from May 1",
         "C": "B, and pumps in cell 4's flooded wells from May 1",
         "D": "C, and 18 vertical wells with pumps in cell 5 from %s %d" % (P.WORKS["wells5"].strftime("%B"),
                                                                          P.WORKS["wells5"].day),
         "E": "D, and a geomembrane cap on cell 4 from October 1"}


def _hdr(ws, row, cols, widths=None):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for j, wd in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd


def _title(ws, t, sub=None):
    ws["A1"] = t
    ws["A1"].font = Font(bold=True, size=12)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, size=9, color=MUTED)


def workbook(path, R, figs, F, cache):
    lim = P.LIMIT_T
    wb = openpyxl.Workbook()
    # ---- the call
    ws = wb.active
    ws.title = "Package call"
    _title(ws, "2027 gas collection packages against Resolution 2025-41 (limit %s t of methane in 2027)"
           % "{:,.0f}".format(lim), "Methane leaving the site in calendar 2027 in a year of normal weather, metric tons")
    _hdr(ws, 4, ["Package", "Works", "Capital cost, USD million", "2027 methane emitted, t", "Under the limit",
                 "Margin to the limit, t"], [9, 54, 13, 15, 10, 14])
    for p in P.PACKAGES:
        v = figs["R7_emissions_2027_t"]["package %s" % p]
        ws.append([p, WORKS[p], P.PACKAGES[p]["cost"], v, "Yes" if v <= lim else "No", round(lim - v)])
    for r in range(5, 10):
        ws["C%d" % r].number_format = "0.00"
        ws["D%d" % r].number_format = T0
        ws["F%d" % r].number_format = T0
        if ws["A%d" % r].value == R["R8"]:
            for col in "ABCDEF":
                ws["%s%d" % (col, r)].fill = PatternFill("solid", fgColor="DDEBF7")
    ws["A11"] = ("Recommended: package %s, the cheapest package at or under the limit (USD %.2f million). Package C "
                 "leaves 2027 at %s t, %s t over." % (R["R8"], P.PACKAGES[R["R8"]]["cost"],
                                                       "{:,.0f}".format(figs["R7_emissions_2027_t"]["package C"]),
                                                       "{:,.0f}".format(figs["R7_emissions_2027_t"]["package C"] - lim)))
    ws["A11"].font = Font(bold=True)
    ws["A12"] = ("Normal weather: each month's soil temperature at 10 cm is its 2016 to 2025 mean at the site station; "
                 "the pressure response averages to one over a year.")
    ws["A12"].font = Font(italic=True, size=8)
    # ---- 2025 bridge
    ws = wb.create_sheet("2025 bridge")
    _title(ws, "What Fernhallow emitted in 2025, and why the report and the survey differ from it",
           "Metric tons of methane, calendar 2025")
    b = figs["R6_bridge"]
    _hdr(ws, 4, ["Step", "t", "Running total, t"], [62, 12, 16])
    rows = [("The 2025 greenhouse gas report (the state rule's collection-based method)", figs["report_2025_t"]),
            ("Collection efficiency: methane generated in 2025 in place of the rule's area-weighted efficiency",
             b["collection efficiency"]),
            ("Oxidation: each cover's oxidation at its own monthly flux in place of the rule's 10 per cent",
             b["oxidation"]),
            ("Everything else (destruction at the flare and engines, rounding)", figs["residual_2025_t"])]
    run = 0
    for k, (lab, v) in enumerate(rows):
        run += v
        ws.append([lab, v, run])
    ws.append(["The site's actual 2025 emission", figs["R2_actual_2025_t"], figs["R2_actual_2025_t"]])
    ws.append([])
    run = figs["survey_2025_t"]
    ws.append(["The state survey's 2025 figure (the 2025 campaigns' mean rate over 8,760 hours)", run, run])
    ws.append(["The hours the campaigns did not sample (the pressure the waste held and released)",
               b["the hours the campaigns did not sample"], run + b["the hours the campaigns did not sample"]])
    ws.append(["The site's actual 2025 emission", figs["R2_actual_2025_t"], figs["R2_actual_2025_t"]])
    for r in range(5, 14):
        for col in "BC":
            ws["%s%d" % (col, r)].number_format = T0
    for r in (9, 13):
        ws["A%d" % r].font = Font(bold=True)
    c = R["campaigns"]
    c25 = c[pd.to_datetime(c["date"]).dt.year == 2025]
    r0 = 16
    ws.cell(row=r0 - 1, column=1, value="The 2025 campaigns carried to every hour").font = Font(bold=True)
    _hdr(ws, r0, ["Campaign", "Date", "Window (local)", "Measured, kg/h", "Pressure factor over the window",
                  "Annual-mean rate, kg/h"])
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 16
    for k, (_, x) in enumerate(c25.iterrows(), r0 + 1):
        ws.cell(row=k, column=1, value=x["campaign"])
        ws.cell(row=k, column=2, value=pd.Timestamp(x["date"]).date()).number_format = "yyyy-mm-dd"
        ws.cell(row=k, column=3, value="%s to %s" % (x["start_local"], x["end_local"]))
        ws.cell(row=k, column=4, value=int(x["site_kg_h"]))
        ws.cell(row=k, column=5, value=round(float(x["m"]), 3)).number_format = "0.000"
        ws.cell(row=k, column=6, value=round(float(x["site_corr"]), 1)).number_format = "#,##0.0"
    k = r0 + 1 + len(c25)
    ws.cell(row=k, column=1, value="Mean")
    ws.cell(row=k, column=4, value=round(float(c25["site_kg_h"].mean()), 1)).number_format = "#,##0.0"
    ws.cell(row=k, column=5, value=round(float(c25["m"].mean()), 3)).number_format = "0.000"
    ws.cell(row=k, column=6, value=round(float(c25["site_corr"].mean()), 1)).number_format = "#,##0.0"
    ws.cell(row=k + 2, column=1, value=(
        "Pressure factor: the chambers' flux on cells 4 and 5 rises %.3f in the log per hPa of the gap between the "
        "barometer's %d-hour exponential mean and its reading; the factor is that response over the campaign's hours "
        "against its mean over the year." % (R["baro"]["c"], R["baro"]["tau"]))).font = Font(italic=True, size=8)
    # ---- cell 4
    ws = wb.create_sheet("Cell 4")
    z = R["z"]
    _title(ws, "Cell 4: methane generation since leachate recirculation began (April 2023)",
           "Wells' methane flow, calendar 2022 against the twelve months to October 2026")
    _hdr(ws, 4, ["Wells", "Count", "Read in both periods", "Flow ratio, 2026 to 2022", "Note"], [38, 8, 12, 14, 60])
    ws.append(["Wells the leachate never reached (no liquid over the screen)", z["n_dry"], z["n_dry_read"],
               round(z["r_dry"], 3), "the waste the leachate did not reach"])
    ws.append(["Wells with liquid over the screen since 2023, pumped from June 2025", z["n_pumped"],
               z["n_pumped_read"], round(z["r_pump"], 3), "the reached waste, read through a pumped screen"])
    ws.append(["  the same, at full yield", z["n_pumped"], z["n_pumped_read"], round(z["r_wet"], 3),
               "a pumped screen keeps %.2f of its length under liquid; yield loss %.2f per unit submerged"
               % (z["s_after"], z["L"])])
    ws.append(["Wells with liquid over the screen, not pumped", z["n_wet"] - z["n_pumped"], None, None,
               "flooded: their flow fell with the liquid, not the gas"])
    ws.append(["All cell 4 wells (the gas system's cell 4 flow)", z["n_wells"], None, round(z["r_collected"], 3),
               "what the collected gas shows"])
    for r in range(5, 10):
        ws["D%d" % r].number_format = "0.000"
    ws["A11"] = "Share of cell 4's wells in the reached waste"
    ws["D11"] = round(R["share_wet"], 3)
    ws["A12"] = "Change in cell 4's methane generation, 2022 to the twelve months to October 2026, per cent"
    ws["D12"] = figs["R3_cell4_generation_change_pct"]
    ws["D12"].number_format = "0.0"
    ws["A12"].font = Font(bold=True)
    ws["A13"] = "Decay rate of the waste the leachate did not reach, per year (the closed cells' decline)"
    ws["D13"] = round(R["kd"], 4)
    ws["A14"] = "Decay rate of the reached waste, per year (fitted to the pumped wells at full yield)"
    ws["D14"] = round(R["kw"], 4)
    ws["A15"] = "Cell 4's collection efficiency, August to October 2026"
    ws["D15"] = round(R["ce4_now"], 3)
    # ---- cell 5
    ws = wb.create_sheet("Cell 5")
    _title(ws, "Cell 5: waste placed, 2027 methane generation and its cover's oxidation",
           "Municipal waste in short tons as weighed; methane in metric tons")
    ws["A4"] = "Municipal waste placed in cell 5, February 2025 to October 2026, short tons"
    ws["E4"] = figs["R1_cell5_msw_tons"]
    ws["E4"].number_format = T0
    ws["A4"].font = Font(bold=True)
    ws["A5"] = "of which %s's trailers, %s to October 2026" % (figs["_extra"]["contract"]["hauler"],
                                                            figs["_extra"]["contract"]["start"])
    ws["E5"] = figs["_extra"]["contract"]["tons_to_oct_2026"]
    ws["E5"].number_format = T0
    _hdr(ws, 6, ["Month, 2027", "Methane generated, t", "Soil temperature, normal, C",
                 "Flux reaching the cover, g/m2/d", "Share oxidized, per cent", "Methane oxidized, t"],
         [14, 14, 14, 16, 14, 14])
    G5 = R["G"][5]
    tot_g, tot_ox = 0.0, 0.0
    for k in range(12):
        m = A.mi(2027, k + 1)
        g = float(G5[m])
        T = R["norm"][k + 1]
        J = g * 1e6 / P.CELLS[5]["area"] / A.dim(m)
        f = A.ox_share(R["OX"], "active", J, T)
        tot_g += g
        tot_ox += g * f
        ws.append([MONTHS[k], round(g, 1), round(T, 1), round(J, 1), round(100 * f, 1), round(g * f, 1)])
    ws.append(["2027", round(tot_g), None, None, figs["R5_cell5_oxidized_share_2027_pct"], round(tot_ox)])
    for r in range(7, 20):
        ws["B%d" % r].number_format = "#,##0.0"
        ws["F%d" % r].number_format = "#,##0.0"
    ws["B19"].number_format = T0
    ws["F19"].number_format = T0
    ws["A19"].font = Font(bold=True)
    ws["A21"] = ("Generation: cell 5's waste on the decay rate of reached waste from August 2026 (recirculation across "
                 "the cell from July 13, 2026), its level set by the spring 2026 two-tracer campaigns on cell 5. "
                 "Oxidation: the 2019 study's plots fitted as a capacity that saturates with the flux through the cover, "
                 "with its temperature factor; share for the plan of record, with all of cell 5's methane reaching the "
                 "cover.")
    ws["A21"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A21:F24")
    ws["A21"].font = Font(italic=True, size=8)
    # ---- 2027 by cell
    ws = wb.create_sheet("2027 by cell")
    _title(ws, "2027 methane emitted by source under each package, metric tons (normal weather)")
    _hdr(ws, 3, ["Source"] + ["Package %s" % p for p in P.PACKAGES], [30, 12, 12, 12, 12, 12])
    cells = R["R7_cells"]
    for lab, key in (("Cells 1 to 3 (closed)", (1, 2, 3)), ("Cell 4", (4,)), ("Cell 5", (5,))):
        ws.append([lab] + [round(sum(cells[p][c] for c in key)) for p in P.PACKAGES])
    ws.append(["Flare and engines (unburned)"] + [round(R["R7_slip"][p]) for p in P.PACKAGES])
    ws.append(["Total"] + [figs["R7_emissions_2027_t"]["package %s" % p] for p in P.PACKAGES])
    ws["A8"].font = Font(bold=True)
    for r in range(4, 9):
        for col in "BCDEF":
            ws["%s%d" % (col, r)].number_format = T0
    # ---- routes
    x = figs["_extra"]
    ws = wb.create_sheet("Routes")
    _title(ws, "2027 methane by package under each route, metric tons, and the package each route picks",
           "The same files and code; one judgment changed at a time")
    _hdr(ws, 4, ["Route"] + ["Package %s" % p for p in P.PACKAGES] + ["Picks"], [58, 11, 11, 11, 11, 11, 11])
    cap = lambda s_: s_[0].upper() + s_[1:]
    plain = {"the careful but hurried route": "the campaigns' rates as measured, one decay rate and the 2019 study's shares"}
    ws.append(["This workbook"] + [figs["R7_emissions_2027_t"]["package %s" % p] for p in P.PACKAGES]
              + [cap(figs["R8_package"])])
    ws["A5"].font = Font(bold=True)
    for name, v in x["shortcuts"].items():
        ws.append([cap(plain.get(name, name))] + [v["R7"]["package %s" % p] for p in P.PACKAGES]
                  + [cap(v["answer"])])
    ws.append([])
    ws.append(["Defensible variants of this workbook's method"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    for name, v in x["family"].items():
        if name.startswith("the golden"):
            continue
        ws.append([cap(name)] + [v["R7"]["package %s" % p] for p in P.PACKAGES] + [cap(v["answer"])])
    for r in range(5, ws.max_row + 1):
        for col in "BCDEF":
            ws["%s%d" % (col, r)].number_format = T0
    wb.save(path)


def deck(path, R, figs):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    lim = P.LIMIT_T

    def text(slide, x, y, w, h, lines, size=16):
        tf = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)).text_frame
        tf.word_wrap = True
        for k, line in enumerate(lines):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.runs[0].font.size = Pt(size)
            p.runs[0].font.color.rgb = RGBColor.from_string(INK)
            p.space_after = Pt(9)
        return tf

    def title(slide, t, sub=None):
        tf = text(slide, 457200, 300000, 11277600, 700000, [t], 24)
        tf.paragraphs[0].runs[0].font.bold = True
        if sub:
            q = tf.add_paragraph()
            q.text = sub
            q.runs[0].font.size = Pt(13)
            q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
        q = slide.shapes.add_textbox(Emu(457200), Emu(6400000), Emu(10800000), Emu(300000)).text_frame.paragraphs[0]
        q.text = "Fernhallow Regional Landfill. Kelloway County Solid Waste Division, November 2026"
        q.runs[0].font.size = Pt(9)
        q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)

    e = figs["R7_emissions_2027_t"]
    f = lambda x: "{:,.0f}".format(x)
    s = prs.slides.add_slide(blank)
    title(s, "Fund package %s: it is the cheapest that keeps 2027 under %s t" % (R["R8"], f(lim)),
          "2027 gas collection, January 2027 budget amendment")
    text(s, 457200, 1500000, 11277600, 4600000, [
        "Package %s (USD %.2f million) leaves 2027 at about %s t of methane in a normal-weather year; package C "
        "(USD %.2f million) leaves it at about %s t, over the limit." % (
            R["R8"], P.PACKAGES[R["R8"]]["cost"], f(e["package %s" % R["R8"]]), P.PACKAGES["C"]["cost"],
            f(e["package C"])),
        "Fernhallow emitted about %s t in 2025: more than twice the %s t in our report and %s t above the state "
        "survey's %s t." % (f(figs["R2_actual_2025_t"]), f(figs["report_2025_t"]),
                            f(figs["R6_bridge"]["the hours the campaigns did not sample"]), f(figs["survey_2025_t"])),
        "Cell 5 drives 2027: it will generate about %s t, now that the leachate it takes speeds its decay, and its "
        "thin cover will oxidize only about %.0f per cent of what reaches it." % (
            f(figs["R4_cell5_generation_2027_t"]), figs["R5_cell5_oxidized_share_2027_pct"])], 17)
    s = prs.slides.add_slide(blank)
    title(s, "2027 methane by package against the limit",
          "Metric tons in a normal-weather year; the limit is %s t (red: over it)" % f(lim))
    cd = CategoryChartData()
    cd.categories = ["%s (USD %.2fM)" % (p, P.PACKAGES[p]["cost"]) for p in P.PACKAGES]
    cd.add_series("2027 methane, t", [e["package %s" % p] for p in P.PACKAGES])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(4900000), cd)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = False
    ch.font.size = Pt(12)
    ch.value_axis.has_major_gridlines = True
    ch.value_axis.tick_labels.number_format = "#,##0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    pl = ch.plots[0]
    pl.gap_width = 80
    pl.has_data_labels = True
    pl.data_labels.number_format = "#,##0"
    pl.data_labels.number_format_is_linked = False
    for i, p in enumerate(P.PACKAGES):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        v = e["package %s" % p]
        pt.format.fill.fore_color.rgb = RGBColor.from_string(BLUE if p == R["R8"] else (RED if v > lim else GRAY))
    s = prs.slides.add_slide(blank)
    title(s, "Why our report and the state survey were both low for 2025", "Metric tons of methane, calendar 2025")
    b = figs["R6_bridge"]
    cd = CategoryChartData()
    cd.categories = ["Our report", "Collection efficiency", "Oxidation", "Everything else", "Actual 2025",
                     "State survey", "Hours not sampled"]
    cd.add_series("t", [figs["report_2025_t"], b["collection efficiency"], b["oxidation"], figs["residual_2025_t"],
                        figs["R2_actual_2025_t"], figs["survey_2025_t"], b["the hours the campaigns did not sample"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1300000), Emu(6400000), Emu(4900000), cd)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = False
    ch.font.size = Pt(11)
    ch.category_axis.reverse_order = True
    ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ch.value_axis.tick_labels.number_format = "#,##0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.number_format = "#,##0"
    pl.data_labels.number_format_is_linked = False
    for i in range(7):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor.from_string(BLUE if i == 4 else GRAY)
    text(s, 7100000, 1400000, 4600000, 4800000, [
        "Our report divides the gas we collected by the rule's collection efficiency. Cell 4's flooded wells and "
        "cell 5's uncollected waste left far more gas uncollected than the rule assumes.",
        "The covers oxidized more than the rule's 10 per cent of the small flux through the closed cells.",
        "The state's crews measure only on settled days after a front passes, while rising pressure holds gas in "
        "the waste; carried to every hour through the chambers' pressure response, their campaigns give %s t."
        % f(figs["R2_actual_2025_t"])], 13)
    s = prs.slides.add_slide(blank)
    title(s, "What changed underground since 2023", "Cells 4 and 5")
    z = R["z"]
    text(s, 457200, 1450000, 11277600, 4700000, [
        "Cell 4: its methane generation rose %.1f per cent from 2022 to the twelve months to October 2026. Its "
        "collected gas rose only %.1f per cent, because the leachate that sped the decay also flooded the wells "
        "that reach that waste; the wells it never reached rose %.1f per cent and the pumped wells, at full yield, "
        "%.1f per cent." % (figs["R3_cell4_generation_change_pct"], 100 * (z["r_collected"] - 1),
                             100 * (z["r_dry"] - 1), 100 * (z["r_wet"] - 1)),
        "Cell 5: %s short tons of municipal waste through October 2026, %s of them from %s's trailers since %s. "
        "Leachate across the whole cell since July 2026 puts all of it on the faster decay: about %s t generated in "
        "2027." % (f(figs["R1_cell5_msw_tons"]), f(figs["_extra"]["contract"]["tons_to_oct_2026"]),
                   figs["_extra"]["contract"]["hauler"], figs["_extra"]["contract"]["start"],
                   f(figs["R4_cell5_generation_2027_t"])),
        "Cell 5's daily cover oxidizes a nearly fixed amount per square meter, so at the flux it will carry in 2027 it takes about "
        "%.1f per cent, not the share the 2019 study measured at lower fluxes." % figs["R5_cell5_oxidized_share_2027_pct"]],
        16)
    prs.save(path)


def write(F, R, out, figs, gold_dir):
    os.makedirs(gold_dir, exist_ok=True)
    wbp = os.path.join(gold_dir, WORKBOOK)
    dkp = os.path.join(gold_dir, DECK)
    workbook(wbp, R, figs, F, out)
    deck(dkp, R, figs)
    postprocess.normalize_ooxml(wbp, P.ENGINEER, P.ENGINEER, "2026-11-09T17:12:00Z", "2026-11-12T22:47:33Z",
                                excel=True, company=P.ORG)
    postprocess.normalize_pptx(dkp, P.ENGINEER, P.ENGINEER, "2026-11-11T18:30:00Z", "2026-11-12T23:05:41Z",
                               title="2027 gas collection package", company=P.ORG)
    postprocess.own_mtimes(gold_dir, {})
