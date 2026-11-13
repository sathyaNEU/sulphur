"""The golden deliverables: the fleet workbook (the bridge from the register to the order by size, and every result
behind it) and the order note as a PDF exported by LibreOffice Writer. Figures come from writeup.flat, so the workbook,
the note and submission.md carry one set of numbers."""
import datetime as dt
import os
import sys

import openpyxl
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import params as P  # noqa: E402

XLSX = "wrenfold_keg_fleet_2027.xlsx"
PDF = "wrenfold_keg_order_2027.pdf"
SIZES = (50, 30, 20)
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="D9E1EC")


def _hdr(ws, row):
    ws.append(row)
    for c in ws[ws.max_row]:
        c.font = BOLD
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def workbook(f, G, path):
    g = G["golden"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Order"
    ws.append(["Wrenfold keg fleet, 2027 order (kegs)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    _hdr(ws, ["", "50 l", "30 l", "20 l"])
    rows = [("Register, active kegs at 30 Nov 2026", "register"),
            ("less kegs lost since the Nov 2023 reconciliation and not written off", "untraced"),
            ("Fleet at 30 Nov 2026 (usable)", "fleet"),
            ("less kegs lost from 1 Dec to the busiest week", "lost_to_week"),
            ("Fleet in the busiest week", "have"),
            ("Kegs in circulation in the busiest week", "circ"),
            ("Washer float (two days' season fills)", "float"),
            ("Kegs needed", "need"),
            ("Kegs to buy", "buy")]
    for lab, key in rows:
        ws.append([lab] + [f["%s_%d" % (key, s)] for s in SIZES])
    ws.append(["Busiest week (week ending)"] + [f["week_%d" % s] for s in SIZES])
    for r in (ws.max_row - 1, ws.max_row - 2):
        pass
    ws.column_dimensions["A"].width = 62
    for c in "BCD":
        ws.column_dimensions[c].width = 12
    ws2 = wb.create_sheet("Loss 2026")
    _hdr(ws2, ["Twelve months to 30 Nov 2026", "50 l", "30 l", "20 l"])
    for lab, key in (("Kegs filled (sent out)", "sent"), ("Own kegs back at the washer", "back"),
                     ("Kegs out at 30 Nov 2025 (filled, not yet back)", "out1"),
                     ("Kegs out at 30 Nov 2026", "out2"), ("Kegs lost in the trade", "loss"),
                     ("Depot gate counters: fulls out less empties in", "gate")):
        ws2.append([lab] + [f["%s_%d" % (key, s)] for s in SIZES])
    ws2.column_dimensions["A"].width = 50
    ws3 = wb.create_sheet("Busiest week deliveries")
    _hdr(ws3, ["2027 season, normal weather", "50 l", "30 l", "20 l"])
    ws3.append(["Kegs delivered in the busiest delivery week"] + [f["deliv_%d" % s] for s in SIZES])
    ws3.append(["80% range, low"] + [f["deliv_lo_%d" % s] for s in SIZES])
    ws3.append(["80% range, high"] + [f["deliv_hi_%d" % s] for s in SIZES])
    ws3.append(["Week ending"] + [f["deliv_week_%d" % s] for s in SIZES])
    ws3.append([])
    _hdr(ws3, ["Week ending", "50 l", "30 l", "20 l"])
    wk = {s: g["_R3"][s]["weekly"] for s in SIZES}
    for i, d in enumerate(wk[50].index):
        ws3.append([d.date()] + [round(float(wk[s].iloc[i])) for s in SIZES])
    ws3.column_dimensions["A"].width = 44
    ws4 = wb.create_sheet("Circulation 2027")
    _hdr(ws4, ["Week ending", "50 l", "30 l", "20 l", "of which Foundry cold store"])
    R6 = g["_R6"]
    for d in R6[50]["weekly"].index:
        ws4.append([d.date()] + [round(float(R6[s]["weekly"].loc[d, "total"])) for s in SIZES] +
                   [round(float(R6[20]["weekly"].loc[d, "foundry_store"]))])
    ch = LineChart()
    ch.title = "Kegs in circulation, 2027 season"
    ch.y_axis.title = "kegs"
    ch.height, ch.width = 7.5, 17
    data = Reference(ws4, min_col=2, max_col=4, min_row=1, max_row=ws4.max_row)
    cats = Reference(ws4, min_col=1, min_row=2, max_row=ws4.max_row)
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ws4.add_chart(ch, "G2")
    ws4.column_dimensions["A"].width = 13
    ws5 = wb.create_sheet("Need by component")
    _hdr(ws5, ["Busiest week", "50 l", "30 l", "20 l"])
    for lab, key in (("Existing customers and their kegs on the way (carried from 2026)", "part_existing"),
                     ("Maplestead pubs and new Foundry taps, at the pubs", "part_new"),
                     ("their kegs filled, at depots and on the way back", "part_pipe"),
                     ("Foundry beers full in the cold store", "part_store"),
                     ("Kegs in circulation", "circ"), ("Washer float", "float"), ("Kegs needed", "need")):
        ws5.append([lab] + [f["%s_%d" % (key, s)] for s in SIZES])
    ws5.append([])
    ws5.append(["Maplestead pubs' kegs at the pubs in the busiest week", f["estate_50"], f["estate_30"], ""])
    ws5.append(["Foundry cold store in the 20 l busiest week", "", "", f["store"]])
    ws5.column_dimensions["A"].width = 62
    wb.save(path)


def note(f, G, path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6,
                        spaceAfter=2)
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.4, leading=10.2)
    rows = [["", "50 l", "30 l", "20 l"],
            ["Kegs to buy"] + [_c(f["buy_%d" % s]) for s in SIZES],
            ["Usable fleet, 30 Nov 2026"] + [_c(f["fleet_%d" % s]) for s in SIZES],
            ["Register says"] + [_c(f["register_%d" % s]) for s in SIZES],
            ["Lost in the trade, year to Nov 2026"] + [_c(f["loss_%d" % s]) for s in SIZES],
            ["Busiest week's deliveries (80% range)"] + ["%s (%s to %s)" % (_c(f["deliv_%d" % s]), _c(f["deliv_lo_%d" % s]),
                                                                          _c(f["deliv_hi_%d" % s])) for s in SIZES],
            ["Fleet to cover in the busiest week"] + [_c(f["need_%d" % s]) for s in SIZES]]
    t = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[62 * 2.835, 34 * 2.835, 34 * 2.835, 34 * 2.835])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB"))]))
    s = [Paragraph("Keg order for summer 2027", h1),
         Paragraph("%s, supply chain. Prepared by %s for %s, %s." % (P.ORG, P.PEOPLE["analyst"], P.PEOPLE["head"],
                                                                     "7 December 2026"), body),
         Paragraph(f["rec"], body), Spacer(1, 4), t,
         Paragraph("Why the register is not the fleet", h2), Paragraph(f["note_fleet"], body),
         Paragraph("What the new business needs", h2), Paragraph(f["note_new"], body),
         Paragraph("How sure", h2), Paragraph(f["note_range"], body)]
    O.build(path, s, "Keg order for summer 2027", P.PEOPLE["analyst"], P.ORG, "%s. Keg order for summer 2027." % P.ORG,
            dt.datetime(2026, 12, 7, 9, 12, tzinfo=dt.timezone.utc),
            dt.datetime(2026, 12, 7, 11, 40, tzinfo=dt.timezone.utc), producer="LibreOffice 7.6")


def _c(x):
    return "{:,}".format(int(x))


def write(f, G, folder):
    os.makedirs(folder, exist_ok=True)
    workbook(f, G, os.path.join(folder, XLSX))
    note(f, G, os.path.join(folder, PDF))
