"""task4 documents: Fryele's fleet electrification standard FES-2 and the dealer's quotation for the 2027
battery-electric tractors, both PDFs written the way the two offices write them (a Word document exported by
LibreOffice Writer)."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

SE_W = dt.timezone(dt.timedelta(hours=1))
SE_S = dt.timezone(dt.timedelta(hours=2))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.6, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, Fleet and transport planning" % P.ORG, small),
         Paragraph("FES-2 Fleet electrification standard: assigning duties to battery-electric tractors", h1),
         Paragraph("Version 3, issued 22 September 2025. Replaces version 2 (June 2025). Owner: the Fleet Manager.",
                   small), Spacer(1, 4)]
    sec = [
        ("1. Scope", [
            "This standard governs which of the company's regular duties are run with battery-electric tractors. It "
            "applies to every depot and to every order of battery-electric tractors put to the management group."]),
        ("2. Terms", [
            "2.1 A duty is a regular round trip from a depot as the route register records it: the run from the "
            "depot to the collection, the loaded run from the collection to the delivery, with any drops it makes "
            "on the way, and the run back to the depot.",
            "2.2 A duty's energy is the energy the tractor draws from its battery for the round trip, depot out to "
            "depot in, in kWh, as the tractor's own battery system reports it.",
            "2.3 The usable battery of a tractor model is the usable energy its manufacturer states for it, less the "
            "share of its usable energy a battery permanently loses in its first twelve months in service. That "
            "share is taken from the company's own battery-electric tractors."]),
        ("3. Planning figures", [
            "3.1 Energy figures for planning are estimated from the company's own operating records of its "
            "battery-electric tractors. Manufacturers' range and consumption figures are not used for planning.",
            "3.2 A duty is charged at its depot before it departs. No charging on the road is planned."]),
        ("4. Assigning duties", [
            "4.1 The January design day is a working day with a mean ambient temperature of minus 5 degrees Celsius.",
            "4.2 A duty's planning load is the mean net payload of its departures in the twelve months to the end of "
            "the last full month before the assessment.",
            "4.3 A duty is assigned to a battery-electric tractor when its energy on the January design day, carrying "
            "its planning load, is no more than 85 per cent of the usable battery of the tractor model being "
            "ordered. The other 15 per cent is the reserve for traffic, diversions and the unexpected. Each duty "
            "assigned takes one tractor.",
            "4.4 Duties are assessed each autumn for the following year, before any order is placed, and reported to "
            "the management group duty by duty with the energy each needs on the January design day."]),
        ("5. Review", [
            "5.1 This standard is reviewed every two years or when a new tractor model is ordered. Comments to the "
            "Fleet Manager."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    O.build(path, s, "FES-2 Fleet electrification standard", "Georg Pålsson",
            "Assigning duties to battery-electric tractors", "Fryele Åkeri AB | FES-2 version 3",
            dt.datetime(2025, 9, 22, 9, 22, tzinfo=SE_S), dt.datetime(2025, 9, 22, 10, 5, tzinfo=SE_S),
            producer="LibreOffice 25.8.1.1")


def quotation(path):
    body, h1, h2, small, cell = _styles()
    rows = [["Item", "Specification"],
            ["Tractor", "Battery-electric 6x2 tractor, low-entry cab, approved for 64 tonnes gross combination weight"],
            ["Battery", "Installed capacity 630 kWh; usable capacity %d kWh" % P.USABLE_2027],
            ["Charging", "CCS2, up to 375 kW DC; on-board 43 kW AC"],
            ["Drive", "Three electric motors, continuous output 425 kW"],
            ["Unladen weight", "11,980 kg (tractor, fifth wheel, full equipment)"],
            ["Power take-off", "Electric PTO, 400 V AC, up to 40 kW, for body and trailer equipment"],
            ["Warranty", "Battery 8 years or 1,000,000 km, to 75 per cent of usable capacity"],
            ["Price", "SEK 3,940,000 per tractor excluding VAT, delivered Värnamo"],
            ["Delivery", "January to February 2027 for orders placed by 11 December 2026"]]
    s = [Paragraph("Norrvik Lastvagnar AB, Industrigatan 14, 331 44 Värnamo", small),
         Paragraph("Tel. 0370-48 210 | order@norrviklastvagnar.se", small), Spacer(1, 10),
         Paragraph("2 October 2026", body),
         Paragraph("Georg Pålsson, Fleet Manager, Fryele Åkeri AB, Terminalvägen 6, 331 53 Värnamo", body),
         Spacer(1, 4),
         Paragraph("Quotation Q-26-1187: battery-electric tractors for delivery in 2027", h1),
         Paragraph("Dear Georg,", body),
         Paragraph("Thank you for the meeting at Terminalvägen on 24 September. As agreed, we quote below for "
                   "battery-electric tractors for your Värnamo terminal, for delivery in early 2027. The quotation "
                   "is valid for any number of tractors from one to twelve.", body),
         _grid(rows, [90, 380], cell), Spacer(1, 6),
         Paragraph("Service and battery monitoring are included for the first three years under our standard "
                   "agreement, from your Värnamo workshop. Your existing fleet portal account will show the new "
                   "tractors' daily summaries as it does for the Jönköping tractors.", body),
         Paragraph("We would need your order by 11 December 2026 to hold the January and February 2027 build "
                   "slots.", body),
         Paragraph("Kind regards,", body), Spacer(1, 6), Paragraph("Pierre Kjellberg", body),
         Paragraph("Key account manager, Norrvik Lastvagnar AB", small)]
    O.build(path, s, "Quotation Q-26-1187", "Pierre Kjellberg", "Battery-electric tractors for delivery in 2027",
            "Norrvik Lastvagnar AB | Quotation Q-26-1187", dt.datetime(2026, 10, 2, 14, 11, tzinfo=SE_S),
            dt.datetime(2026, 10, 2, 14, 20, tzinfo=SE_S))
