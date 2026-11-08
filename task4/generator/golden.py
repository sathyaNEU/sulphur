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


def write_xlsx(path, pk, g, target):
    names = _shippers(target)
    wb = Workbook()
    ws = wb.active
    ws.title = "Assessment"
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="D9E1EA")
    thin = Side(style="thin", color="A6A6A6")
    ws["A1"] = "Värnamo duties shortlisted for battery-electric tractors, 2027: FES-2 assessment"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("January design day (FES-2 4.1, mean ambient -5 C) at each duty's planning load (FES-2 4.2, mean net "
                "payload weighed at Värnamo, November 2025 to October 2026). Limit 85 per cent of the 540 kWh usable "
                "battery of quotation Q-26-1187: 459 kWh.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:L2")
    ws.row_dimensions[2].height = 30
    hdr = ["Duty", "Shipper", "Delivery", "Depot to collection km", "Loaded km", "Back km", "Round trip km",
           "Climb m/100 km", "Planning load t", "Design-day energy kWh", "Share of usable battery",
           "Battery-electric 2027"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    a = g["assess"]
    for c in sorted(pk.short):
        r = pk.routes[c]
        legs = r["legs"]
        e = a[c]["kwh"]
        ws.append([c, names[r["shipper"]], pk.routes[c]["delivery"], legs[0], legs[1], legs[2], sum(legs), r["climb"],
                   round(A.planning_load(pk, c), 1), r10(e), round(r10(e) / A.USABLE, 3),
                   "Yes" if a[c]["go"] else "No, stays diesel"])
        ws.cell(ws.max_row, 11).number_format = "0%"
    n = ws.max_row
    ws.append([])
    ws.append(["Tractors to order", None, None, None, None, None, None, None, None, None, None, g["count"]])
    ws.cell(ws.max_row, 1).font = bold
    ws.cell(ws.max_row, 12).font = bold
    ws.append(["Duties going electric", None, None, None, None, None, None, None, None, None, None,
               ", ".join(g["set"])])
    for i, wd in enumerate([7, 26, 13, 11, 9, 8, 10, 9, 9, 11, 10, 18], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "B5"
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1

    m = g["model"]["coef"]
    ws2 = wb.create_sheet("Energy model")
    ws2.append(["Battery energy per duty-day, Jönköping pilot, March 2025 to October 2026"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append(["Fitted by least squares on %d duty-days (daily summaries joined to the TMS consignments)" %
                len(pk.days)])
    ws2.append([])
    ws2.append(["Term", "Coefficient", "Unit"])
    for c in ws2[4]:
        c.font = bold
        c.fill = head_fill
    rows = [("Base, per km driven", m[0], "kWh per km"), ("Climb", m[1], "kWh per km per m/100 km"),
            ("Cold, per degree below 16 C", m[2], "kWh per km per degree"),
            ("Further cold, per degree below 0 C", m[3], "kWh per km per degree"),
            ("Payload, per tonne on the loaded run", m[4] * 100, "kWh per tonne per 100 km loaded")]
    for t, v, u in rows:
        ws2.append([t, round(float(v), 5 if abs(v) < 0.1 else 3), u])
    ws2.append([])
    ws2.append(["Payload of each pilot day: the declared weight on the TMS consignment taken to the weighed "
                "load it stands for, shipper by shipper, from the Värnamo weighbridge (sheet Payload calibration)."])
    ws2.append(["Root mean square error of a duty-day: %.1f per cent of its energy." % g["model"]["rmse_pct"]])
    ws2.column_dimensions["A"].width = 44
    ws2.column_dimensions["B"].width = 13
    ws2.column_dimensions["C"].width = 34

    ws3 = wb.create_sheet("Payload calibration")
    ws3.append(["Shipper", "Name", "Departures weighed", "Mean declared kg", "Mean weighed net kg",
                "Weighed against declared, slope", "Weighed load taken for a declaration of d kg"])
    for c in ws3[1]:
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    cal = A.calibration(pk)
    import numpy as np
    for s in sorted(cal):
        rr = [r for r in pk.wb if r["shipper"] == s and r["declared"] is not None]
        md = float(np.mean([r["declared"] for r in rr]))
        mw = float(np.mean([r["net"] for r in rr]))
        a0, lam = cal[s]
        if lam == 0.0:
            rule = "%d kg whatever is declared (one standard weight declared)" % round(a0, -1)
        elif abs(lam - 1) < 0.02:
            rule = "d (the declared weight is the shipper's weighbridge ticket)"
        else:
            rule = "%d + %.3f x d" % (round(a0, -1), lam)
        ws3.append([s, names[s], len(rr), round(md), round(mw), round(lam, 3), rule])
    for i, wd in enumerate([8, 26, 11, 12, 12, 13, 48], 1):
        ws3.column_dimensions[get_column_letter(i)].width = wd
    ws3.freeze_panes = "A2"
    ws4 = wb.create_sheet("Notes")
    for line in ["As of 6 November 2026. Pilot records: fleet portal daily summaries, 3 March 2025 to 30 October 2026; "
                 "a day uploaded twice is counted once.",
                 "Payloads on the pilot days are the TMS consignment's declared weight, read in kilograms or tonnes.",
                 "Ambient temperature: the tractor's own reading; on days the sensor dropped out, the Jönköping "
                 "station's daily mean moved by the average difference between the two (%.1f C)." % pk.offset,
                 "Weighbridge: where a departure was weighed twice after a reload, the later weighing is used.",
                 "Usable battery 540 kWh (quotation Q-26-1187); one tractor per duty assigned (FES-2 4.3)."]:
        ws4.append([line])
    ws4.column_dimensions["A"].width = 120
    wb.save(path)


def write_pdf(path, pk, g, target):
    names = _shippers(target)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.4, spaceAfter=5)
    h1 = ParagraphStyle("h", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.4)
    a = g["assess"]
    slope = A.slope_per_100(g["model"])
    rows = [["Duty", "Shipper", "Delivery", "Round trip km", "Planning load t", "Design-day kWh", "Electric"]]
    for c in sorted(pk.short, key=lambda x: (not a[x]["go"], x)):
        r = pk.routes[c]
        rows.append([c, names[r["shipper"]], pk.routes[c]["delivery"], sum(r["legs"]), "%.1f" % A.planning_load(pk, c),
                     r10(a[c]["kwh"]), "Yes" if a[c]["go"] else "No"])
    t = Table([[Paragraph(str(x), cell) for x in rr] for rr in rows], colWidths=[34, 140, 70, 58, 62, 62, 44])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    src = Paragraph("Energies to the nearest 10 kWh, at −5 C and each duty's planning load (the mean of the last "
                    "weighing of each CMR at Värnamo, November 2025 to October 2026, gross less tare). Limit 459 kWh "
                    "under FES-2 4.3.", small)
    heavy = [c for c in sorted(pk.short) if not a[c]["go"] and A.planning_load(pk, c) > 25]
    go = g["set"]
    nv = A.assess(pk, g["models"]["naive"])
    top_go = r10(max(a[c]["kwh"] for c in go))
    heavy_e = r10(sum(a[c]["kwh"] for c in heavy) / len(heavy))
    heavy_nv = r10(sum(nv[c]["kwh"] for c in heavy) / len(heavy))
    v14_nv = r10(nv["V14"]["kwh"])
    n_nv = len(A.chosen(nv))
    naive_slope = A.slope_per_100(g["models"]["naive"])
    s = [Paragraph("Fryele Åkeri AB | To the management group | 6 November 2026", small),
         Paragraph("Battery-electric tractors for Värnamo, 2027: order %d" % g["count"], h1),
         Paragraph("<b>Recommendation.</b> Order %d battery-electric tractors under quotation Q-26-1187 for duties "
                   "%s. On the January design day each needs no more than %d kWh against the 459 kWh FES-2 allows "
                   "(85 per cent of 540 kWh usable). The heavy steel, ballast and metal duties %s need about %d kWh "
                   "and stay on diesel, as do %s." % (g["count"], ", ".join(go), top_go, ", ".join(heavy), heavy_e,
                                                      ", ".join(c for c in sorted(pk.short) if not a[c]["go"]
                                                                and c not in heavy)), body),
         t, Spacer(1, 2), src, Spacer(1, 6),
         Paragraph("<b>How the energy was estimated.</b> From the %d duty-days the six Jönköping tractors ran in the "
                   "pilot, joined to the TMS consignments, with distance, climb and temperature (below 16 C and a "
                   "further rate below 0 C) as the other terms. The pilot's payloads are the shippers' declared "
                   "weights. The Värnamo weighbridge shows the declarations are right on average but that the "
                   "furniture, packaging, drinks and builders' merchants' clerks estimate them (their declared weight "
                   "scatters around what the truck carries), the dairy writes one standard weight on every note, and "
                   "Tabergs Trävaror prints its own weighbridge figure. Fitted on the declared weights, the model "
                   "puts a tonne of payload at about %.1f kWh per 100 km loaded, because the scatter in the "
                   "declarations dilutes the effect. Taking each declaration to the weighed load it stands for, "
                   "shipper by shipper, puts it at %.1f kWh, which the Tabergs days confirm on their own." %
                   (len(pk.days), naive_slope, slope), body),
         Paragraph("<b>What this changes.</b> On the declared weights the heavy duties look feasible at about %d "
                   "kWh and the light insulation duty V14 does not (about %d kWh): that would order %d tractors and "
                   "send %d duties out that cannot finish a cold day on 85 per cent of the battery. The "
                   "duty-by-duty figures are in ev_duty_assessment_2027.xlsx with the model and the calibration." %
                   (heavy_nv, v14_nv, n_nv, len(heavy)), body),
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
