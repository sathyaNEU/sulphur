"""The golden deliverables: ev_duty_assessment_2027.xlsx (every shortlisted duty's January design-day energy and
verdict, the number of tractors, the model and the payload calibration behind it) and tractor_order_memo.pdf (one page
for the management group), both from analysis.py's figures on the shipped pack."""
import datetime as dt
import os

import matplotlib
matplotlib.use("Agg")
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import analysis as A
import officepdf as O

XLSX = "ev_duty_assessment_2027.xlsx"
PDF = "tractor_order_memo.pdf"
SE = dt.timezone(dt.timedelta(hours=1))
NAMES = {}


def r10(x):
    return int(round(x / 10.0) * 10)


def compute(target):
    pk = A.load(target)
    g = A.golden(pk)
    return pk, g


def _shippers(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "shipper_register_2026.xlsx"), read_only=True)
    return {r[0]: r[1] for r in list(wb["Shippers"].iter_rows(values_only=True))[1:]}


def _head(ws, row, fill):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_xlsx(path, pk, g, target):
    import numpy as np
    names = _shippers(target)
    wb = Workbook()
    ws = wb.active
    ws.title = "Assessment"
    bold = Font(bold=True)
    fill = PatternFill("solid", fgColor="D9E1EA")
    lim = g["limit"]
    ws["A1"] = "Värnamo shortlist 2027: battery-electric assessment under FES-2"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("January design day (FES-2 4.1, -5 C), each duty at its planning load (FES-2 4.2: mean net payload "
                "weighed at Värnamo, Nov 2025 to Oct 2026). Usable battery after the first year %d kWh (540 kWh "
                "quoted, less %.1f per cent first-year loss); limit 85 per cent, %d kWh." %
                (round(g["usable_y1"]), 100 * g["fade"], round(lim)))
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:L2")
    ws.row_dimensions[2].height = 30
    ws.append([])
    ws.append(["Duty", "Shipper", "Delivery", "Depot to collection km", "Loaded km", "Back km", "Round trip km",
               "Climb m/100 km", "Planning load t", "Design-day energy kWh", "Share of year-1 usable battery",
               "Electric 2027"])
    _head(ws, 4, fill)
    a = g["assess"]
    for c in sorted(pk.short):
        r = pk.routes[c]
        legs = r["legs"]
        e = a[c]["kwh"]
        ws.append([c, names[r["shipper"]], r["delivery"], legs[0], legs[1], legs[2], sum(legs), r["climb"],
                   round(A.planning_load(pk, c), 1), r10(e), round(r10(e) / g["usable_y1"], 3),
                   "Yes" if a[c]["go"] else "No"])
        ws.cell(ws.max_row, 11).number_format = "0.0%"
    ws.append([])
    for label, v in (("Usable battery after first year, kWh", round(g["usable_y1"])), ("Limit (85 per cent), kWh",
                     round(lim)), ("Tractors to order", g["count"]), ("Duties", ", ".join(g["set"]))):
        ws.append([label] + [None] * 10 + [v])
        ws.cell(ws.max_row, 1).font = bold
    for i, wd in enumerate([7, 26, 13, 11, 9, 8, 10, 9, 9, 11, 11, 16], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "B5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1

    m = g["model"]["coef"]
    gp = A.payloads(pk, "lane")
    ws2 = wb.create_sheet("Energy model")
    ws2.append(["Battery energy per duty-day, Jönköping pilot, Mar 2025 to Oct 2026 (%d duty-days)" % len(pk.days)])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    ws2.append(["Term", "Coefficient", "Unit"])
    _head(ws2, 3, fill)
    for t, v, u in (("Per km driven", m[0], "kWh/km"), ("Climb", m[1], "kWh/km per m/100 km"),
                    ("Below 16 C", m[2], "kWh/km per degree"), ("Further, below 0 C", m[3], "kWh/km per degree"),
                    ("Speed, (v squared - 65 squared)/1000", m[4], "kWh/km per (km/h)^2/1000"),
                    ("Combination tare above 19 t, every km", m[5] * 100, "kWh per tonne per 100 km"),
                    ("Payload, tonne-km on the loaded run", m[6] * 100, "kWh per tonne per 100 km")):
        ws2.append([t, round(float(v), 5 if abs(v) < 0.1 else 2), u])
    ws2.append([])
    ws2.append(["Cold form, Jan-Feb 2026 held out", "Error, days below 0 C", "Error, all held-out days"])
    _head(ws2, ws2.max_row, fill)
    for lab, form in (("One rate below 16 C", A.H1), ("Below 16 C and below 0 C (used)", A.H2),
                      ("Quadratic below 16 C", ("quad", 16))):
        b = A.backtest(pk, gp, form)
        ws2.append([lab, "%+.1f%%" % b[0], "%+.1f%%" % b[1]])
    ws2.append([])
    ws2.append(["Duty-day RMSE %.1f per cent. Payload per pilot day: see Payloads." %
                g["model"]["rmse_pct"]])
    ws2.column_dimensions["A"].width = 36
    ws2.column_dimensions["B"].width = 20
    ws2.column_dimensions["C"].width = 24

    import writeup as WU
    ws3 = wb.create_sheet("Payloads")
    ws3.append(["Pilot duty", "Shipper", "Mean declared t (notes)", "Shipper's mean declared at Värnamo t",
                "Share", "Mean load on the terminal's line t", "Mean load from the duty's own declarations t"])
    _head(ws3, 1, fill)
    for du, v in WU.lane_table(pk).items():
        ws3.append([du, names[v["shipper"]], v["declared"], v["terminal_declared"], v["share"], v["terminal_line"],
                    v["lane"]])
    ws3.append([])
    ws3.append(["Declaration error on the Värnamo weighbridge (declared less weighed)"])
    ws3.cell(ws3.max_row, 1).font = bold
    ws3.append(["Shipper", "Name", "Notes", "Departures weighed", "Error sd kg", "Error sd, share of load"])
    _head(ws3, ws3.max_row, fill)
    em = A.error_model(pk)
    pilot = sorted({d["shipper"] for d in pk.days})
    for (s, reg), (ea, er) in sorted(em.items()):
        if s not in pilot:
            continue
        nrow = sum(1 for r in pk.wb if r["shipper"] == s and r["declared"] is not None and
                   A.regime(pk, s, r["date"]) == reg)
        per = {"all": "Nov 2024 to Oct 2026", "note": "before the scale", "ticket": "scale weight on the note"}[reg]
        ws3.append([s, names[s], per, nrow, round(float(np.sqrt(ea))), round(float(np.sqrt(er)), 3)])
    ws3.append([])
    ws3.append(["Gränna Dryckes' dock scale (notes carry the weighed load from August 2026)"])
    ws3.cell(ws3.max_row, 1).font = bold
    ws3.append(["Pilot duty", "Scale-weighed days", "Mean weighed t", "Before: from own declarations t",
                "Before: on the terminal's line t"])
    _head(ws3, ws3.max_row, fill)
    for du, v in WU.scale_check(pk).items():
        ws3.append([du, v["scale_days"], v["scale_mean"], v["own_before"], v["terminal_line_before"]])
    ws3.append([])
    ws3.append(["Each pilot day's declared weight is taken to its expected load on its own duty: the shipper's "
                "declaration error from the weighbridge removed from the spread of the duty's own declarations."])
    for i, wd in enumerate([10, 26, 14, 16, 10, 16, 18], 1):
        ws3.column_dimensions[get_column_letter(i)].width = wd

    wst = wb.create_sheet("Trailers and drops")
    wst.append(["Each duty with the 2027 tractor (%.2f t, quotation Q-26-1187) and the trailers it pulled at Värnamo, "
                "Nov 2025 to Oct 2026" % (A.TRACTOR_2027_KG / 1000)])
    wst["A1"].font = Font(bold=True, size=12)
    wst.append(["Pilot combinations %.1f to %.1f t, mean %.1f t. Load share: tonne-km the departing load rides over "
                "the loaded run, each note taken off at its stop (TMS notes, routing tool's stops)." %
                (min(d["combo"] for d in pk.days), max(d["combo"] for d in pk.days), g["pilot_combo"])])
    wst.append([])
    wst.append(["Duty", "Trailer kind", "Combination t", "Stops", "Load share of loaded km"])
    _head(wst, 4, fill)
    for c in sorted(pk.short):
        inp = g["inputs"][c]
        deps = pk.vdep[c]
        kinds = sorted({pk.trailer[x["trailer"]]["type"] for x in deps})
        wst.append([c, "; ".join(kinds), round(inp["combo"], 1), inp["n_drops"], round(inp["phi"], 2)])
    for i, wd in enumerate([7, 38, 12, 7, 12], 1):
        wst.column_dimensions[get_column_letter(i)].width = wd

    ws4 = wb.create_sheet("Battery")
    ws4.append(["Energy per full charge: kWh used / (SOC start - SOC end), per duty-day"])
    ws4["A1"].font = Font(bold=True, size=12)
    ws4.append(["Fitted with a level per tractor, degrees below 20 C on the day, and an age form: an early-life loss "
                "settling over %.2f years (chosen by the fit) plus a steady loss" % g["tau"]])
    ws4.append([])
    ws4.append(["Item", "Value"])
    _head(ws4, 4, fill)
    for lab, v in (("First-year permanent loss", "%.1f%%" % (100 * g["fade"])),
                   ("Quoted usable battery, kWh", 540), ("Usable after first year, kWh", round(g["usable_y1"])),
                   ("Limit, 85 per cent, kWh", round(lim))):
        ws4.append([lab, v])
    ws4.append([])
    ws4.append(["Age form", "First-year loss", "Residual sum of squares"])
    _head(ws4, ws4.max_row, fill)
    for lab, h in (("Early loss settling, fitted time scale (used)", "curve"), ("Square root of age", "sqrt"),
                   ("Square root and straight line", "sqrtlin"), ("Log of age and straight line", "loglin"),
                   ("Piecewise straight, knots 3, 6, 12 months", "spline"), ("Straight line", "cold")):
        loss, rss, _ = A.fade_fit(pk, h)
        ws4.append([lab, "%.1f%%" % (100 * loss), round(rss)])
    ws4.append(["Same months a year apart", "%.1f%%" % (100 * A.fade(pk, "yoy")), ""])
    ws4.column_dimensions["A"].width = 44
    ws4.column_dimensions["B"].width = 14
    ws4.column_dimensions["C"].width = 22

    wsv = wb.create_sheet("Speed")
    wsv.append(["Average speed on the design day: routing-tool speed x the pilot's actual-to-planned ratio at -5 C"])
    wsv["A1"].font = Font(bold=True, size=12)
    rr, rm = A.speed_ratio(pk), A.speed_ratio(pk, how="mean")
    wsv.append(["Pilot actual / routing-tool speed: %.3f at -5 C (slope below 10 C), %.3f over the year" % (rr, rm)])
    wsv.append([])
    wsv.append(["Duty", "Routing-tool km/h", "Design-day km/h"])
    _head(wsv, 4, fill)
    for c in sorted(pk.short):
        vp = A.plan_speed(pk, c)
        wsv.append([c, round(vp, 1), round(vp * rr, 1)])
    wsv.column_dimensions["A"].width = 12
    wsv.column_dimensions["B"].width = 18
    wsv.column_dimensions["C"].width = 16

    ws5 = wb.create_sheet("Routes")
    ws5.append(["Route", "Payload kWh/t/100 km", "First-year loss", "Limit kWh", "Tractors", "Duties"])
    _head(ws5, 1, fill)
    show = {"golden": "As assessed",
            "the terminal's calibration line": "Pilot loads on the terminal's weighed-on-declared line",
            "declared weights": "Declared weights", "one pooled correction": "One correction line over the bridge",
            "a straight-line loss": "Battery loss as a straight line in age",
            "the same months a year apart": "Battery loss from the same months a year apart",
            "no first-year loss": "No first-year loss",
            "the year's mean speed ratio": "Speed at the year's mean actual-to-planned ratio",
            "the routing tool's speed": "Speed at the routing tool's planned speed",
            "no speed term": "No speed term (energy in proportion to distance)",
            "one cold rate": "One cold rate below 16 C",
            "no trailer weight": "Trailer left out (pilot's average combination)",
            "the load to the last drop": "Every load carried to the last drop",
            "careful but hurried": "Terminal's line, straight-line loss, the year's speed ratio",
            "careful, design-day speed": "Terminal's line and straight-line loss at the design-day speed"}
    for k, (mod, lm) in A.routes(pk).items():
        if k not in show:
            continue
        aa = A.assess(pk, mod, lim=lm)
        loss = 1 - lm / (A.SHARE * A.USABLE)
        ws5.append([show[k], round(A.slope_per_100(mod), 1), "%.1f%%" % (100 * loss), round(lm), len(A.chosen(aa)),
                    ", ".join(A.chosen(aa)) or "none"])
    for i, wd in enumerate([34, 12, 11, 9, 9, 52], 1):
        ws5.column_dimensions[get_column_letter(i)].width = wd

    ws6 = wb.create_sheet("Notes")
    for line in ["As of 6 November 2026.",
                 "Pilot: fleet portal summaries 3 Mar 2025 to 30 Oct 2026, a day uploaded twice counted once, joined "
                 "to TMS consignments on registration and date.",
                 "Declared weights read in kg or tonnes (decimal comma).",
                 "Ambient: the tractor's reading; on sensor dropouts the Jönköping station mean plus %.1f C." % pk.offset,
                 "Weighbridge: the last weighing of each CMR; duty codes VMO-nn read as Vnn.",
                 "TMS notes: one per drop; a pilot day's declared weight is the sum of its notes.",
                 "One tractor per duty assigned (FES-2 4.3)."]:
        ws6.append([line])
    ws6.column_dimensions["A"].width = 110
    wb.save(path)


def write_pdf(path, pk, g, target):
    names = _shippers(target)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.0, leading=12.0, spaceAfter=5)
    h1 = ParagraphStyle("h", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.4)
    a = g["assess"]
    lim = round(g["limit"])
    rows = [["Duty", "Shipper", "Delivery", "Round trip km", "Planning load t", "Design-day kWh", "Electric"]]
    for c in sorted(pk.short, key=lambda x: (not a[x]["go"], x)):
        r = pk.routes[c]
        rows.append([c, names[r["shipper"]], r["delivery"], sum(r["legs"]), "%.1f" % A.planning_load(pk, c),
                     r10(a[c]["kwh"]), "Yes" if a[c]["go"] else "No"])
    t = Table([[Paragraph(str(x), cell) for x in rr] for rr in rows], colWidths=[34, 140, 70, 58, 62, 62, 44])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    import writeup as WU
    R = {k: (m, lm, A.chosen(A.assess(pk, m, lim=lm))) for k, (m, lm) in A.routes(pk).items()}
    go = g["set"]
    no = [c for c in sorted(pk.short) if c not in go]
    rr = A.speed_ratio(pk)
    inp = g["inputs"]
    cnt = lambda k: len(R[k][2])
    lt = WU.lane_table(pk)
    sc = WU.scale_check(pk)
    car = R["careful but hurried"]
    s = [Paragraph("Fryele Åkeri AB | To the management group | 6 November 2026", small),
         Paragraph("Battery-electric tractors for Värnamo, 2027: order %d" % g["count"], h1),
         Paragraph("<b>Recommendation.</b> Order %d tractors under quotation Q-26-1187, for %s. The other %d "
                   "duties need %d to %d kWh on the January design day against a limit of %d kWh." %
                   (g["count"], ", ".join(go), len(no), min(r10(a[c]["kwh"]) for c in no),
                    max(r10(a[c]["kwh"]) for c in no), lim), body),
         t, Spacer(1, 2),
         Paragraph("Energies to the nearest 10 kWh at -5 C and each duty's planning load. Limit: 85 per cent of the "
                   "%d kWh a 540 kWh battery keeps after its first year." % round(g["usable_y1"]), small),
         Spacer(1, 5),
         Paragraph("<b>Basis.</b> A model of each pilot duty-day's energy (%d days) on distance, climb, cold, speed, "
                   "the combination's weight and the payload. (1) The pilot's payloads are shippers' declarations, "
                   "and the regional pilot duties carry %.0f to %.0f per cent of the loads the same shippers declare "
                   "at Värnamo. The Värnamo weighbridge gives each shipper's declaration error; taking each pilot "
                   "duty's loads from its own declarations, a tonne costs %.1f kWh per 100 loaded km. Read through "
                   "the Värnamo calibration line instead, every pilot duty comes out %.1f to %.1f t too heavy and the "
                   "figure falls to %.1f; Gränna Dryckes' scale-weighed days (J07 %.1f t, J08 %.1f t) bear out the "
                   "duties' own loads. (2) The batteries lost %.1f per cent for good in their first year, most of it "
                   "in the first months; a straight line in age gives %.1f. (3) On a -5 C day the pilot drove at "
                   "%.0f per cent of the routing tool's speed, against %.0f over the year. (4) The tractor and "
                   "trailer weigh on every leg (V02 and V14's double decks %.1f and %.1f t with the 2027 tractor), "
                   "and a multi-drop load comes off along the run (V03's rides %.0f per cent of its loaded km). (5) "
                   "Below freezing the draw rises faster (a second rate below 0 C, chosen on Jan-Feb 2026 held out)."
                   % (len(pk.days), 100 * min(v["share"] for v in lt.values()),
                      100 * max(v["share"] for v in lt.values()), A.slope_per_100(g["model"]),
                      min(v["terminal_line"] - v["lane"] for v in lt.values()),
                      max(v["terminal_line"] - v["lane"] for v in lt.values()), A.slope_per_100(car[0]),
                      sc["J07"]["scale_mean"], sc["J08"]["scale_mean"], 100 * g["fade"], 100 * A.careful_fade(pk),
                      100 * rr, 100 * A.speed_ratio(pk, how="mean"), inp["V02"]["combo"], inp["V14"]["combo"],
                      100 * inp["V03"]["phi"]), body),
         Paragraph("<b>If one is skipped.</b> The Värnamo calibration line, the straight-line loss and the year's "
                   "speed ratio together: %d tractors (%s). The same at the design-day speed: %d. The year's speed "
                   "ratio alone: %d; the routing tool's speed: %d; no speed term: %d. Declared weights: %d. Trailer "
                   "left out: %d. Loads to the last drop: %d. One cold rate: %d. No first-year loss: %d. The "
                   "workbook has each route." %
                   (cnt("careful but hurried"), ", ".join(car[2]), cnt("careful, design-day speed"),
                    cnt("the year's mean speed ratio"), cnt("the routing tool's speed"), cnt("no speed term"),
                    cnt("declared weights"), cnt("no trailer weight"), cnt("the load to the last drop"),
                    cnt("one cold rate"), cnt("no first-year loss")), body),
         Paragraph("Inger Norman, Transport planning", small)]
    O.build(path, s, "Battery-electric tractors for Värnamo, 2027", "Inger Norman", "Tractor order memo",
            "Fryele Åkeri AB | Management group, December 2026", dt.datetime(2026, 11, 6, 10, 12, tzinfo=SE),
            dt.datetime(2026, 11, 6, 15, 48, tzinfo=SE))


def write(target, outdir):
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        os.remove(os.path.join(outdir, f))
    pk, g = compute(target)
    write_xlsx(os.path.join(outdir, XLSX), pk, g, target)
    write_pdf(os.path.join(outdir, PDF), pk, g, target)
    return pk, g
