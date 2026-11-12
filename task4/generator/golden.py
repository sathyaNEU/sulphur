"""The golden deliverables, written from results.compute: the planning analyst's spreadsheet (the 2027 spares line by
line, the removals behind them, the watch list read serial by serial, the Bodø shop's year, the fill curves) and a few
slides for the technical director (the lines to buy and to cut, what moves each, the watch list)."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Emu, Pt

import analysis as A
import params as P

XLSX = "havorn_rotable_spares_2027.xlsx"
PPTX = "havorn_rotable_spares_2027.pptx"
DRV = {"cyc": "landings and starts", "fh": "flight hours", "days": "calendar time"}


def reasons(G):
    """What moves each line, from the analysis itself: the exposure its removals follow and how 2027 moves it, each
    in-house line's own summer turnaround in the 2027 replay against its 2026 average, the bulletin, and where most
    removals find no fault."""
    F, fc, D, H = G["F"], G["fc"], G["D"], G["H"]
    X = A.expo_2027(F)
    Dd = F["day"]
    m12 = (Dd["date"] >= A.Y26[0]) & (Dd["date"] <= A.Y26[1])
    cyc_ch = X["cyc"].sum() / Dd[m12]["cyc"].sum() - 1
    fh_ch = X["fh"].sum() / Dd[m12]["fh"].sum() - 1
    tat = {}
    for k, m, t, rep in G["tat_in"]:
        if m in (7, 8):
            tat.setdefault(k, []).append(t)
    summer = {k: float(np.mean(v)) for k, v in tat.items()}
    out = {}
    for k in A.PARTS:
        r = []
        drv = D[k]["driver"]
        if drv == "cyc":
            r.append("wears by landings and starts, %+.0f%% in 2027 while flight hours fall %.0f%%" % (cyc_ch * 100, -fh_ch * 100))
        elif drv == "fh":
            r.append("follows flight hours, %.0f%% fewer in 2027" % (-fh_ch * 100))
        else:
            r.append("ages by calendar time")
        if k in P.IN_HOUSE:
            r.append("Bodø shop turnaround about %.0f days in July and August 2027 against %.0f across 2026"
                     % (summer.get(k, 0.0), H[k]["tat"]))
        if k == "PEC":
            sp = fc["PEC"]["split"]
            r.append("SB 61-0042 cuts the confirmed failures by about %.0f%% and reaches more of the fleet at every removal"
                     % ((1 - sp["rate_mod"] / sp["rate_un"]) * 100))
        if fc[k]["nff"] > 0.4 * fc[k]["total"]:
            r.append("most removals find no fault, fewer once more of the flying is based at Bodø")
        ol = G["qproj"][k]
        if k != "PEC" and fc[k]["total"] < 0.75 * ol:
            r.append("its rate over the four years of record, below the last twelve months'")
        out[k] = "; ".join(r)
    return out, cyc_ch, fh_ch, summer


SHORT = {"SG": "starter-generator", "BRK": "brake", "BAV": "bleed valve", "NWS": "nose wheel steering",
         "BAT": "battery", "CPC": "cabin pressure controller", "FLA": "flap actuator", "ADC": "air data computer",
         "WXR": "weather radar", "VHF": "VHF transceiver", "PEC": "propeller control", "PDT": "de-ice timer",
         "HYP": "hydraulic pump", "FBP": "fuel boost pump", "WHC": "windshield heat controller",
         "FDU": "fire detection unit"}
SOURCE = ("Source: component changes, flight legs, Bodø shop work orders and roster, repairers' orders and the stores "
          "snapshot to 30 November 2026; the 2027 flying programme of 18 November 2026")
INK, MUTED, ACCENT, FILL = "1F2A3A", "8A94A6", "0E6E6B", "E3E8EF"


def _hdr(ws, cols, widths, row=None):
    ws.append(cols)
    r = ws.max_row
    for c in ws[r]:
        c.font = Font(bold=True, color=INK)
        c.fill = PatternFill("solid", fgColor=FILL)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A%d" % (r + 1)
    return r


def _fmt(ws, first, last, formats):
    """Number formats by column letter over rows first..last, numbers right-aligned."""
    for col, f in formats.items():
        for r in range(first, last + 1):
            c = ws["%s%d" % (col, r)]
            if isinstance(c.value, (int, float)):
                c.number_format = f
                c.alignment = Alignment(horizontal="right")


def action(G, k):
    """Buy or cut where every member of the golden family moves the line the same way; hold otherwise."""
    rob = G["robust"]
    return {"BUY": "buy", "CUT": "cut"}[rob[k][0]] if k in rob else "hold"


def outlook(G):
    import docs
    return {r["k"]: r["proj"] for r in docs.report_figures(G["F"])["rows"]}


def workbook(G, path):
    F, fc, MC, H = G["F"], G["fc"], G["MC"], G["H"]
    why, cyc_ch, fh_ch, summer = reasons(G)
    ol = outlook(G)
    wb = Workbook()
    ws = wb.active
    ws.title = "Spares plan 2027"
    buys = [k for k in A.PARTS if action(G, k) == "buy"]
    cuts = [k for k in A.PARTS if action(G, k) == "cut"]
    ws.append(["%s, 2027 rotable spares plan: buy %d spares on %d lines, cut %d on %d" %
               (P.ORG, sum(G["calls"][k] for k in buys), len(buys), -sum(G["calls"][k] for k in cuts), len(cuts))])
    ws["A1"].font = Font(bold=True, size=12, color=INK)
    ws.append(["Units in service at 30 November 2026 under the 2027 flying programme, 95 per cent fill rate (standard "
               "4.1 to 4.4). Prepared by %s, planning, 7 December 2026." % P.PEOPLE["analyst"]])
    ws["A2"].font = Font(italic=True, color=MUTED)
    ws.append([])
    h = _hdr(ws, ["Part number", "Description", "Installed", "Pool today", "Expected 2027 unscheduled removals",
                  "80% range, low", "80% range, high", "Spares needed", "Change", "Action", "What moves it"],
             [13, 34, 9, 9, 15, 10, 10, 10, 8, 9, 92])
    for k in A.PARTS:
        p = P.PART[k]
        ch = G["calls"][k]
        act = action(G, k)
        w = why[k] + ("; the methods differ by a unit here, so the line holds" if act == "hold" and ch else "")
        ws.append([p["pn"], p["name"], P.FLEET_N * p["pos"], P.POOL[k], round(fc[k]["total"]), int(MC[k]["p10"]),
                   int(MC[k]["p90"]), G["need"][k], ch if act != "hold" else 0, act, w[:1].upper() + w[1:]])
    last = ws.max_row
    ws.append(["Total", "", sum(P.FLEET_N * P.PART[k]["pos"] for k in A.PARTS), sum(P.POOL.values()),
               round(sum(fc[k]["total"] for k in A.PARTS)), "", "", sum(G["need"].values()),
               sum(G["calls"][k] for k in A.PARTS if action(G, k) != "hold")])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True, color=INK)
    _fmt(ws, h + 1, ws.max_row, {"C": "#,##0", "D": "0", "E": "0", "F": "0", "G": "0", "H": "0", "I": "+0;-0;0"})
    for r in range(h + 1, last + 1):
        ws["K%d" % r].alignment = Alignment(wrap_text=True, vertical="top")
    ws.append([])
    ws.append([SOURCE])
    ws["A%d" % ws.max_row].font = Font(italic=True, color=MUTED, size=9)
    ws.print_title_rows = "%d:%d" % (h, h)
    ws.print_area = "A1:K%d" % ws.max_row
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    # removals
    ws2 = wb.create_sheet("Removals 2027")
    h = _hdr(ws2, ["Part number", "Description", "Exposure the failures follow", "Expected confirmed failures",
                   "Expected no fault found", "Expected 2027 removals", "At October's MTBUR on 2027's flight hours",
                   "Difference"], [13, 34, 22, 14, 14, 14, 16, 11])
    for k in A.PARTS:
        p = P.PART[k]
        ws2.append([p["pn"], p["name"], DRV[G["D"][k]["driver"]], round(fc[k]["cf"], 1), round(fc[k]["nff"], 1),
                    round(fc[k]["total"]), round(ol[k]), round(fc[k]["total"]) - round(ol[k])])
    _fmt(ws2, h + 1, ws2.max_row, {"D": "0.0", "E": "0.0", "F": "0", "G": "0", "H": "+0;-0;0"})
    ws2.append([])
    ws2.append(["The 2027 programme against the twelve months to October 2026: landings %+.1f%%, flight hours %+.1f%%. "
                "Confirmed failures include those beyond economic repair; the comparison column carries each part at the "
                "October reliability report's MTBUR on 2027's flight hours." % (cyc_ch * 100, fh_ch * 100)])
    ws2["A%d" % ws2.max_row].font = Font(italic=True, color=MUTED, size=9)
    # watch list
    ws3 = wb.create_sheet("Watch list")
    W = G["W"]
    h = _hdr(ws3, ["Serial", "Part number", "Removals, 12 months to October", "Own removals since January 2023",
                   "Removals its aircraft drove", "Position removals saved a year by a new unit", "Withdraw",
                   "Reading"], [11, 13, 13, 13, 13, 16, 10, 80])
    for sn, r in W.sort_values(["scrap", "excess"], ascending=[False, False]).iterrows():
        if r["scrap"]:
            reading = "Removals follow the serial from aircraft to aircraft"
        elif r["by_aircraft"] >= max(2, r["own"]):
            reading = "Removed with other serials from a faulty aircraft position: the aircraft's fault, not the unit's"
        else:
            reading = "A short run of removals the rest of its record does not repeat"
        ws3.append([sn, P.PART[r["k"]]["pn"], int(r["n12"]), int(r["own"]), int(r["by_aircraft"]), round(r["excess"], 1),
                    "yes" if r["scrap"] else "no", reading])
    _fmt(ws3, h + 1, ws3.max_row, {"C": "0", "D": "0", "E": "0", "F": "0.0"})
    ws3.append([])
    ws3.append(["Withdrawing every listed serial saves about %.0f removals a year; the %d marked yes save about %.0f. "
                "Removals its aircraft drove are runs of three or more found serviceable from one aircraft position "
                "inside 120 days, by two or more serials (standard 5.1 and 5.2)."
                % (G["saving"], len(G["scrap"]), W[W["scrap"]]["excess"].sum())])
    ws3["A%d" % ws3.max_row].font = Font(italic=True, color=MUTED, size=9)
    # the Bodø shop
    ws4 = wb.create_sheet("Bodø shop")
    h = _hdr(ws4, ["Month of removal", "Expected turnaround 2027 (days)", "2026 average (days)"], [16, 18, 16])
    tat = {}
    for k, m, t, rep in G["tat_in"]:
        tat.setdefault(m, []).append(t)
    t26 = np.mean([H[k]["tat"] for k in P.IN_HOUSE])
    for m in range(1, 13):
        ws4.append([dt.date(2027, m, 1).strftime("%B"), round(float(np.mean(tat.get(m, [0]))), 1), round(float(t26), 1)])
    _fmt(ws4, h + 1, ws4.max_row, {"B": "0.0", "C": "0.0"})
    ws4.append([])
    ws4.append(["Starter-generators, brakes, bleed valves, nose wheel steering actuators and batteries; turnaround from "
                "removal to serviceable stock (standard 2.4). The shop's capacity is set so the replay of its own "
                "2024 to 2026 work reproduces the turnarounds it ran."])
    ws4["A%d" % ws4.max_row].font = Font(italic=True, color=MUTED, size=9)
    # routes: each method's change line by line
    ws5 = wb.create_sheet("Routes")
    rts = G["routes"]
    h = _hdr(ws5, ["Part number", "Description"] + [r["label"] for r in rts], [13, 34] + [20] * len(rts))
    for k in A.PARTS:
        ws5.append([P.PART[k]["pn"], P.PART[k]["name"]] + [int(r["changes"][k]) for r in rts])
    _fmt(ws5, h + 1, ws5.max_row, {get_column_letter(3 + i): "+0;-0;0" for i in range(len(rts))})
    ws5.append([])
    ws5.append(["Change in spares against the pool on each line, by method. Palm's formula sizes a line on a Poisson "
                "pipeline at the 2026 average turnaround."])
    ws5["A%d" % ws5.max_row].font = Font(italic=True, color=MUTED, size=9)
    # fill curves
    ws6 = wb.create_sheet("Fill by spares")
    h = _hdr(ws6, ["Part number"] + ["%d spare%s" % (s, "" if s == 1 else "s") for s in range(0, 13)], [13] + [9] * 13)
    for k in A.PARTS:
        ws6.append([P.PART[k]["pn"]] + [round(float(MC[k]["fill"][s]) * 100, 1) for s in range(0, 13)])
    _fmt(ws6, h + 1, ws6.max_row, {get_column_letter(2 + s): "0.0" for s in range(0, 13)})
    ws6.append([])
    ws6.append(["Expected fill rate over 2027, per cent of the year's unscheduled removals (standard 4.2 and 4.3), "
                "from the replay of each pool."])
    ws6["A%d" % ws6.max_row].font = Font(italic=True, color=MUTED, size=9)
    wb.save(path)


def deck(G, path):
    why, cyc_ch, fh_ch, summer = reasons(G)
    from pptx.dml.color import RGBColor
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    ink, muted, accent = RGBColor.from_string(INK), RGBColor.from_string(MUTED), RGBColor.from_string(ACCENT)
    count = [0]

    def title(s, text, sub=None):
        count[0] += 1
        tb = s.shapes.add_textbox(Emu(457200), Emu(300000), Emu(11277600), Emu(700000)).text_frame
        tb.word_wrap = True
        tb.text = text
        r0 = tb.paragraphs[0].runs[0]
        r0.font.size, r0.font.bold, r0.font.color.rgb = Pt(26), True, ink
        if sub:
            p = tb.add_paragraph()
            p.text = sub
            p.runs[0].font.size, p.runs[0].font.color.rgb = Pt(14), muted
        ft = s.shapes.add_textbox(Emu(457200), Emu(6380000), Emu(11277600), Emu(300000)).text_frame
        ft.text = "%s   |   %s   |   %d" % (P.ORG, SOURCE, count[0])
        ft.paragraphs[0].runs[0].font.size, ft.paragraphs[0].runs[0].font.color.rgb = Pt(9), muted

    def bullets(s, lines, top=1500000, left=457200, width=11277600, size=15):
        tf = s.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(4700000)).text_frame
        tf.word_wrap = True
        for i, l in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = l
            p.runs[0].font.size, p.runs[0].font.color.rgb = Pt(size), ink
            p.space_after = Pt(6)

    def colour(chart, colours, dash=()):
        for i, ser in enumerate(chart.plots[0].series):
            if chart.chart_type in (XL_CHART_TYPE.LINE_MARKERS,):
                ser.format.line.color.rgb = colours[i]
                ser.format.line.width = Pt(2.25)
                if i in dash:
                    ser.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
            else:
                ser.format.fill.solid()
                ser.format.fill.fore_color.rgb = colours[i]

    buys = [k for k in A.PARTS if action(G, k) == "buy"]
    cuts = [k for k in A.PARTS if action(G, k) == "cut"]
    ol = outlook(G)
    s = prs.slides.add_slide(blank)
    title(s, "2027 rotable spares: buy %d units on %d lines, cut %d on %d" %
          (sum(G["calls"][k] for k in buys), len(buys), -sum(G["calls"][k] for k in cuts), len(cuts)),
          "Units in service at 30 November 2026 under the 2027 flying programme, 95 per cent fill rate")
    rows = [("Buy", k) for k in buys] + [("Cut", k) for k in cuts]
    tbl = s.shapes.add_table(len(rows) + 1, 5, Emu(457200), Emu(1450000), Emu(11277600), Emu(300000 * (len(rows) + 1))).table
    for j, w in enumerate([1000000, 6077600, 1400000, 1400000, 1400000]):
        tbl.columns[j].width = Emu(w)
    white, band = RGBColor(0xFF, 0xFF, 0xFF), RGBColor.from_string(FILL)
    for j, hd in enumerate(["Action", "Part", "Holds", "Needs", "Change"]):
        c = tbl.cell(0, j)
        c.text = hd
        c.fill.solid()
        c.fill.fore_color.rgb = accent
        run = c.text_frame.paragraphs[0].runs[0]
        run.font.size, run.font.bold, run.font.color.rgb = Pt(12), True, white
    for i, (a, k) in enumerate(rows, 1):
        for j, v in enumerate([a, "%s %s" % (P.PART[k]["pn"], P.PART[k]["name"]), P.POOL[k], G["need"][k], "%+d" % G["calls"][k]]):
            c = tbl.cell(i, j)
            c.text = str(v)
            c.fill.solid()
            c.fill.fore_color.rgb = band if i % 2 else white
            run = c.text_frame.paragraphs[0].runs[0]
            run.font.size, run.font.color.rgb = Pt(11), ink
    # why the landing-driven parts are short
    s = prs.slides.add_slide(blank)
    title(s, "The parts that wear by landings are short in 2027",
          "October's MTBUR carries every part per flight hour; the 2027 programme adds landings and cuts hours")
    cd = CategoryChartData()
    ks = [k for k in A.PARTS if G["D"][k]["driver"] == "cyc" and k in buys]
    cd.categories = [SHORT[k][:1].upper() + SHORT[k][1:] for k in ks]
    cd.add_series("At October's MTBUR", [round(ol[k]) for k in ks])
    cd.add_series("Expected 2027", [round(G["fc"][k]["total"]) for k in ks])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1450000), Emu(6600000), Emu(4700000), cd)
    ch = gf.chart
    colour(ch, [muted, accent])
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.plots[0].has_data_labels = True
    ch.plots[0].data_labels.font.size = Pt(11)
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "Unscheduled removals in 2027"
    ch.value_axis.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
    ch.has_title = False
    bullets(s, ["Landings %+.0f%%, flight hours %+.0f%% against the twelve months to October" % (cyc_ch * 100, fh_ch * 100),
                "The Helgeland routes from 1 April: eight aircraft on sectors of about a quarter of an hour",
                "Across the four bases the record's sector lengths separate the two: these parts' confirmed failures "
                "follow landings and starts, not hours"], left=7300000, width=4450000, size=14)
    # the Bodø shop
    s = prs.slides.add_slide(blank)
    title(s, "The Bodø shop's summer queue lengthens every in-house line",
          "Expected turnaround by month of removal, 2027 against the 2026 average")
    tat = {}
    for k, m, t, rep in G["tat_in"]:
        tat.setdefault(m, []).append(t)
    cd = CategoryChartData()
    cd.categories = [dt.date(2027, m, 1).strftime("%b") for m in range(1, 13)]
    cd.add_series("2027", [round(float(np.mean(tat.get(m, [0]))), 1) for m in range(1, 13)])
    cd.add_series("2026 average", [round(float(np.mean([G["H"][k]["tat"] for k in P.IN_HOUSE])), 1)] * 12)
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Emu(457200), Emu(1450000), Emu(7600000), Emu(4700000), cd)
    ch = gf.chart
    colour(ch, [accent, muted], dash=(1,))
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "Days from removal to serviceable stock"
    ch.value_axis.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
    ch.has_title = False
    flat = [k for k in P.IN_HOUSE if abs(G["fc"][k]["total"] / max(ol[k], 1) - 1) < 0.15 and G["calls"][k] > 0]
    bullets(s, ["More removals from the landing-driven parts reach the same three technicians",
                "Each technician's three summer weeks run the shop on two from early July to late August"] +
            ["The %s line needs %d more though its own removals barely change" % (SHORT[k], G["calls"][k]) for k in flat],
            left=8300000, width=3450000, size=14)
    # the watch list
    s = prs.slides.add_slide(blank)
    W = G["W"]
    vict = int((~W["scrap"] & (W["by_aircraft"] >= W["own"].clip(lower=2))).sum())
    rest = len(W) - len(G["scrap"]) - vict
    title(s, "Withdraw %d of the %d watch-list serials" % (len(G["scrap"]), len(W)),
          "Withdrawing the whole list saves about %.0f removals a year, not the list's count" % G["saving"])
    Ws = W.sort_values("excess", ascending=True)
    cd = CategoryChartData()
    cd.categories = list(Ws.index)
    cd.add_series("Removals a year a new unit would save in the position", [round(float(v), 1) for v in Ws["excess"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1350000), Emu(6200000), Emu(4950000), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.plots[0].gap_width = 40
    ser = ch.plots[0].series[0]
    for i, sn in enumerate(Ws.index):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = accent if sn in G["scrap"] else muted
    ch.plots[0].has_data_labels = True
    ch.plots[0].data_labels.font.size = Pt(9)
    ch.plots[0].data_labels.number_format = "0.0"
    ch.plots[0].data_labels.number_format_is_linked = False
    ch.category_axis.tick_labels.font.size = Pt(9)
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.tick_labels.font.size = Pt(9)
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "Removals a year a new unit would save in the position (withdraw at 1.5)"
    ch.value_axis.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(10)
    ch.has_title = False
    bullets(s, ["Withdraw: " + ", ".join(G["scrap"]),
                "Their removals follow the serial from aircraft to aircraft",
                "%d others were removed with other serials from a faulty aircraft position: the aircraft's fault, "
                "which a new unit would not mend" % vict,
                "The other %d had a short run of removals their own record does not repeat" % rest],
            left=7000000, width=4750000, size=14)
    # the cuts
    s = prs.slides.add_slide(blank)
    title(s, "%d lines hold more spares than 2027 needs" % len(cuts),
          "Most follow flight hours, which fall %d per cent, and the propeller control carries SB 61-0042" % round(-fh_ch * 100))
    cd = CategoryChartData()
    cd.categories = [SHORT[k][:1].upper() + SHORT[k][1:] for k in cuts]
    cd.add_series("Holds", [P.POOL[k] for k in cuts])
    cd.add_series("Needs in 2027", [G["need"][k] for k in cuts])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1350000), Emu(5600000), Emu(4950000), cd)
    ch = gf.chart
    colour(ch, [muted, accent])
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.plots[0].has_data_labels = True
    ch.plots[0].data_labels.font.size = Pt(9)
    ch.category_axis.tick_labels.font.size = Pt(10)
    ch.category_axis.reverse_order = True
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.tick_labels.font.size = Pt(9)
    ch.has_title = False
    lines = []
    for k in cuts:
        w = why[k]
        lines.append("%s, cut %d: %s" % (P.PART[k]["name"], -G["calls"][k], w))
    bullets(s, lines, left=6300000, width=5450000, size=11)
    prs.save(path)


def write(G, gold):
    os.makedirs(gold, exist_ok=True)
    workbook(G, os.path.join(gold, XLSX))
    deck(G, os.path.join(gold, PPTX))
