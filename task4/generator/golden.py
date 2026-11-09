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
    gp = A.payloads(pk, "shipper")
    ws2 = wb.create_sheet("Energy model")
    ws2.append(["Battery energy per duty-day, Jönköping pilot, Mar 2025 to Oct 2026 (%d duty-days)" % len(pk.days)])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    ws2.append(["Term", "Coefficient", "Unit"])
    _head(ws2, 3, fill)
    for t, v, u in (("Per km driven", m[0], "kWh/km"), ("Climb", m[1], "kWh/km per m/100 km"),
                    ("Below 16 C", m[2], "kWh/km per degree"), ("Further, below 0 C", m[3], "kWh/km per degree"),
                    ("Speed, (v squared - 65 squared)/1000", m[4], "kWh/km per (km/h)^2/1000"),
                    ("Payload on the loaded run", m[5] * 100, "kWh per tonne per 100 km")):
        ws2.append([t, round(float(v), 5 if abs(v) < 0.1 else 2), u])
    ws2.append([])
    ws2.append(["Cold form, Jan-Feb 2026 held out", "Error, days below 0 C", "Error, all held-out days"])
    _head(ws2, ws2.max_row, fill)
    for lab, form in (("One rate below 16 C", A.H1), ("Below 16 C and below 0 C (used)", A.H2),
                      ("Quadratic below 16 C", ("quad", 16))):
        b = A.backtest(pk, gp, form)
        ws2.append([lab, "%+.1f%%" % b[0], "%+.1f%%" % b[1]])
    ws2.append([])
    ws2.append(["Duty-day RMSE %.1f per cent. Payload per pilot day: see Payload calibration." %
                g["model"]["rmse_pct"]])
    ws2.column_dimensions["A"].width = 36
    ws2.column_dimensions["B"].width = 20
    ws2.column_dimensions["C"].width = 24

    ws3 = wb.create_sheet("Payload calibration")
    ws3.append(["Shipper", "Name", "Notes", "Departures weighed", "Mean declared kg", "Mean weighed kg",
                "Slope, weighed on declared", "Load taken for declared d kg"])
    _head(ws3, 1, fill)
    cal = A.calibration(pk)
    pilot = sorted({d["shipper"] for d in pk.days})
    for (s, reg) in sorted(cal):
        if s not in pilot:
            continue
        rr = [r for r in pk.wb if r["shipper"] == s and r["declared"] is not None and
              A.regime(pk, s, r["date"]) == reg]
        a0, lam = cal[(s, reg)]
        per = {"all": "Nov 2024 to Oct 2026", "note": "before the scale", "ticket": "scale weight on the note"}[reg]
        if reg == "ticket":
            months = sorted(A.ticket_months(pk, s))
            per = "scale weight, from %s %d" % (dt.date(*months[0], 1).strftime("%b"), months[0][0])
        if lam == 0.0:
            rule = "%d whatever is declared" % round(a0, -1)
        elif abs(lam - 1) < 0.02:
            rule = "d"
        else:
            rule = "%d + %.3f d" % (round(a0, -1), lam)
        ws3.append([s, names[s], per, len(rr), round(float(np.mean([r["declared"] for r in rr]))),
                    round(float(np.mean([r["net"] for r in rr]))), round(lam, 3), rule])
    ws3.append([])
    ws3.append(["Each pilot day's declared weight (TMS) is replaced by the weighed load it stands for at its "
                "shipper and note period, from the Värnamo weighbridge."])
    for i, wd in enumerate([8, 26, 22, 11, 12, 12, 12, 24], 1):
        ws3.column_dimensions[get_column_letter(i)].width = wd

    ws4 = wb.create_sheet("Battery")
    ws4.append(["Energy per full charge: kWh used / (SOC start - SOC end), per duty-day"])
    ws4["A1"].font = Font(bold=True, size=12)
    ws4.append(["Fitted with a level per tractor, age in service and degrees below 20 C on the day"])
    ws4.append([])
    ws4.append(["Item", "Value"])
    _head(ws4, 4, fill)
    for lab, v in (("First-year permanent loss", "%.1f%%" % (100 * g["fade"])),
                   ("Quoted usable battery, kWh", 540), ("Usable after first year, kWh", round(g["usable_y1"])),
                   ("Limit, 85 per cent, kWh", round(lim)),
                   ("Same months a year apart (check)", "%.1f%%" % (100 * A.fade(pk, "yoy")))):
        ws4.append([lab, v])
    ws4.column_dimensions["A"].width = 36
    ws4.column_dimensions["B"].width = 14

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
    show = {"golden": "As assessed: weighed-equivalent loads, two cold rates, loss net of cold",
            "declared weights": "Declared weights", "one pooled correction": "One correction line over the bridge",
            "one line over the pilot shippers": "One correction line over the pilot shippers",
            "one cold rate": "One cold rate below 16 C", "no first-year loss": "No first-year loss",
            "no speed term": "No speed term (energy in proportion to distance)",
            "the routing tool's speed": "Speed at the routing tool's planned speed",
            "the year's mean speed ratio": "Speed at the year's mean actual-to-planned ratio"}
    for k, (mod, lm) in A.routes(pk).items():
        if k not in show:
            continue
        aa = A.assess(pk, mod, lim=lm)
        loss = 1 - lm / (A.SHARE * A.USABLE)
        ws5.append([show[k], round(A.slope_per_100(mod), 1), "%.1f%%" % (100 * loss), round(lm), len(A.chosen(aa)),
                    ", ".join(A.chosen(aa))])
    for i, wd in enumerate([34, 12, 11, 9, 9, 52], 1):
        ws5.column_dimensions[get_column_letter(i)].width = wd

    ws6 = wb.create_sheet("Notes")
    for line in ["As of 6 November 2026.",
                 "Pilot: fleet portal summaries 3 Mar 2025 to 30 Oct 2026, a day uploaded twice counted once, joined "
                 "to TMS consignments on registration and date.",
                 "Declared weights read in kg or tonnes (decimal comma).",
                 "Ambient: the tractor's reading; on sensor dropouts the Jönköping station mean plus %.1f C." % pk.offset,
                 "Weighbridge: the last weighing of each CMR; duty codes VMO-nn read as Vnn.",
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
    R = {k: (m, lm, A.chosen(A.assess(pk, m, lim=lm))) for k, (m, lm) in A.routes(pk).items()}
    go = g["set"]
    near = sorted({c for k, v in R.items() if k in ("declared weights", "no speed term", "no first-year loss")
                   for c in v[2]} - set(go))
    rest = [c for c in sorted(pk.short) if not a[c]["go"] and c not in near]
    dec, one, nol = R["declared weights"], R["one cold rate"], R["no first-year loss"]
    nsp, pln = R["no speed term"], R["the routing tool's speed"]
    rr = A.speed_ratio(pk)
    s = [Paragraph("Fryele Åkeri AB | To the management group | 6 November 2026", small),
         Paragraph("Battery-electric tractors for Värnamo, 2027: order %d" % g["count"], h1),
         Paragraph("<b>Recommendation.</b> Order %d tractors under quotation Q-26-1187, for %s. Not more: the "
                   "duties %s need %d to %d kWh on the January design day against a limit of %d kWh, and %s "
                   "are further over." % (g["count"], ", ".join(go), ", ".join(near),
                                          min(r10(a[c]["kwh"]) for c in near), max(r10(a[c]["kwh"]) for c in near),
                                          lim, ", ".join(rest)), body),
         t, Spacer(1, 2),
         Paragraph("Energies to the nearest 10 kWh at -5 C and each duty's planning load. Limit: 85 per cent of the "
                   "%d kWh a 540 kWh battery keeps after its first year." % round(g["usable_y1"]), small),
         Spacer(1, 5),
         Paragraph("<b>Basis.</b> A model of each pilot duty-day's energy (%d days) on distance, climb, cold, "
                   "speed and payload. Four things move the order. (1) The pilot's payloads are shippers' declarations; at "
                   "Värnamo, where the same shippers' loads are weighed, the clerks' figures scatter widely around "
                   "the weighed load, and the dairy declares its planned pallets at a standard weight each. Fitted on the declarations a "
                   "tonne costs %.1f kWh per 100 loaded km; taking each declaration to the weighed load it stands "
                   "for, shipper by shipper, %.1f. (2) Below freezing the draw rises faster: one rate below 16 C "
                   "fitted without Jan-Feb 2026 under-forecast those sub-zero days by %.1f per cent, a further rate "
                   "below 0 C by %+.1f. (3) The pilot batteries lost %.1f per cent of their capacity for good in "
                   "their first year, once the cold days' temporary loss is taken out. (4) The Värnamo duties are "
                   "long runs on the E4, E6, 25 and 27, planned faster than any pilot day ran, and each 10 km/h costs about "
                   "%.0f kWh per 100 km at their speeds; on a -5 C day the pilot drove at %.0f per cent of the "
                   "routing tool's speed, so each duty is forecast at that share of its own." %
                   (len(pk.days), A.slope_per_100(dec[0]), A.slope_per_100(g["model"]),
                    -A.backtest(pk, A.payloads(pk, "shipper"), A.H1)[0],
                    A.backtest(pk, A.payloads(pk, "shipper"), A.H2)[0], 100 * g["fade"],
                    100 * g["model"]["coef"][4] * (2 * 68 * 10 + 100) / 1000, 100 * rr), body),
         Paragraph("<b>If any one is skipped.</b> No speed term: %d tractors (%s in). The routing tool's speed: "
                   "%d. Declared weights: %d (%s in, V14 out). One cold rate: %d. No first-year loss: %d. The "
                   "workbook has each route, the model, the calibration and the speeds." %
                   (len(nsp[2]), ", ".join(c for c in nsp[2] if c not in go), len(pln[2]), len(dec[2]),
                    ", ".join(c for c in dec[2] if c not in go), len(one[2]), len(nol[2])), body),
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
