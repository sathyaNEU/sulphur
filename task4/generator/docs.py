"""The three documents: the company's depot electrification standard DES-1, the distribution company's connection
agreement for the charging installation, and the dealer's quotation for the 2027 buses. Each is a Word document
exported to PDF by LibreOffice Writer through the house writer, with the issuing office's own stamps."""
import datetime as dt
import os
import sys

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import params as P  # noqa: E402

FI_W = dt.timezone(dt.timedelta(hours=2))
FI_S = dt.timezone(dt.timedelta(hours=3))


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
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, Planning and fleet" % P.ORG, small),
         Paragraph("DES-1 Depot electrification standard: assigning blocks to battery-electric buses", h1),
         Paragraph("Version 2, approved by the management team 18 August 2026. Replaces version 1 (November 2024). "
                   "Owner: the electrification programme manager.", small), Spacer(1, 4)]
    sec = [
        ("1. Scope", [
            "This standard governs which of the depot's blocks are run with battery-electric buses and how an order of "
            "battery-electric buses put to the board is sized. It applies to every depot of the company."]),
        ("2. Terms", [
            "2.1 A block is one bus's day of work as the dispatch log and the block register record it: the run from the "
            "depot to the first trip, every trip and layover of the day, and the run back to the depot. A block's "
            "kilometres are its scheduled kilometres in the block register.",
            "2.2 A block's energy is the energy the bus draws from its traction battery over the block, depot out to depot "
            "in, in kWh, as the bus's own battery system reports it. Energy taken from the mains while the bus stands at "
            "the depot is not block energy.",
            "2.3 The usable battery of a bus model is the usable energy its manufacturer states for it when new, less the "
            "share of usable energy a traction battery permanently loses in its first twelve months in service. That share "
            "is taken from the company's own battery-electric buses.",
            "2.4 The design day is a January working day with a daily mean air temperature of minus 15 degrees Celsius at "
            "the town's airport weather station (Vehkasalo lentoasema)."]),
        ("3. Planning figures", [
            "3.1 Energy figures for planning are estimated from the company's own operating records. Manufacturers' range "
            "and consumption figures are not used for planning.",
            "3.2 A battery-electric bus is charged at its depot only, between its block's return and its next departure. "
            "No charging on the road or at termini is planned. The depot's chargers deliver up to 150 kW to a bus, and the "
            "charging installation draws no more than the capacity the distribution company's connection agreement "
            "gives it, in the periods the agreement gives it.",
            "3.3 Fuel use is reported per block as litres of diesel per 100 scheduled kilometres over the twelve months "
            "to the end of the last full month before the assessment, from the fuel-card statements and the dispatch "
            "log, for the business case of each block's electrification."]),
        ("4. Assigning blocks", [
            "4.1 A weekday block qualifies for a battery-electric bus when its energy on the design day is no more than "
            "85 per cent of the usable battery of the bus model being ordered. The other 15 per cent is the reserve for "
            "diversions, traffic and the unexpected. Each block assigned takes one bus.",
            "4.2 Qualifying blocks are assigned in the order of the fleet plan's priority list. The list is cut at the first "
            "block the depot cannot recharge, together with every block above it on the list, between the blocks' returns "
            "and their departures under 3.2. Blocks below the cut stay on diesel until the connection is reinforced.",
            "4.3 The order put to the board is one bus for each block assigned under 4.1 and 4.2, with the blocks named.",
            "4.4 Blocks are assessed each autumn for the following year's timetable, before any order is placed, and "
            "reported to the board block by block with the energy each needs on the design day."]),
        ("5. Review", [
            "5.1 This standard is reviewed every two years or when a new bus model is ordered. Comments to the "
            "electrification programme manager."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    O.build(path, s, "DES-1 Depot electrification standard", "Simo Virta",
            "Assigning blocks to battery-electric buses", "%s | DES-1 version 2" % P.ORG,
            dt.datetime(2026, 8, 18, 15, 12, tzinfo=FI_S), dt.datetime(2026, 8, 19, 9, 4, tzinfo=FI_S),
            producer="LibreOffice 25.2.4.3")


def agreement(path):
    body, h1, h2, small, cell = _styles()
    rows = [["Item", "Terms"],
            ["Connection point", "Niittylä depot, Varikkotie 8, metering point 643 102 11 (meter VLO-NIITTYLA-1)"],
            ["Installation", "Battery-electric bus charging installation, charging lane B, 150 kW DC chargers"],
            ["Capacity, charging installation", "%d kW from 21:00 to 07:00 (the night period). Outside the night period the "
             "installation is held off by the load-control relay, except for the workshop's two outlets at 22 kW." % int(P.SUPPLY_KW)],
            ["Capacity, depot otherwise", "The depot's other consumption remains within the main fuse rating of the connection "
             "(1,250 kVA transformer at Niittylä; the charging capacity above is its remaining share)"],
            ["Validity", "From 1 January 2026 until the connection is reinforced. A reinforcement application was received "
             "on 3 June 2026; the earliest completion is the fourth quarter of 2028."],
            ["Tariff", "Power tariff T4, night period 21:00 to 07:00 as above"]]
    s = [Paragraph("%s, Network services" % P.DSO, small),
         Paragraph("Sähkötie 2, 44100 %s | network@vsv.fi" % P.TOWN, small), Spacer(1, 10),
         Paragraph("12 November 2025", body),
         Paragraph("%s, Niittylä depot, Varikkotie 8, 44120 %s" % (P.ORG, P.TOWN), body), Spacer(1, 4),
         Paragraph("Connection agreement 2025-ND-117: charging installation at Niittylä depot", h1),
         Paragraph("Dear Ms Pajunen,", body),
         Paragraph("Following the commissioning inspection of 4 November 2025, we confirm the terms on which the "
                   "charging installation at Niittylä depot is connected to our network from 1 January 2026.", body),
         _grid(rows, [130, 340], cell), Spacer(1, 6),
         Paragraph("The capacity in the night period is the installation's draw at the connection point, measured on the "
                   "same meter as the rest of the depot. The load-control relay releases the chargers at 21:00 and holds "
                   "them off at 07:00; the chargers' own management system is responsible for staying within the capacity "
                   "while released.", body),
         Paragraph("Please confirm receipt. The reinforcement application is being handled separately and we will write to "
                   "you with a schedule once the substation works are planned.", body),
         Paragraph("Yours sincerely,", body), Spacer(1, 6), Paragraph(P.PEOPLE["dso"], body),
         Paragraph("Connection engineer, %s" % P.DSO, small)]
    O.build(path, s, "Connection agreement 2025-ND-117", P.PEOPLE["dso"], "Charging installation at Niittylä depot",
            "%s | 2025-ND-117" % P.DSO, dt.datetime(2025, 11, 12, 10, 36, tzinfo=FI_W),
            dt.datetime(2025, 11, 12, 10, 51, tzinfo=FI_W), producer="LibreOffice 24.8.2.1")


def quotation(path):
    body, h1, h2, small, cell = _styles()
    rows = [["Item", "Specification"],
            ["Bus", "%s %s, 12.2 m low-floor city bus, three doors, 38 seats" % (P.EMAKE, P.EMODEL)],
            ["Traction battery", "Installed 560 kWh (LFP); usable capacity %d kWh when new" % int(P.E_USABLE_2027)],
            ["Charging", "CCS2, up to 150 kW DC at the depot; on-board 22 kW AC"],
            ["Drive", "Central electric motor, continuous 180 kW, peak 260 kW"],
            ["Heating and cooling", "Fully electric: roof-mounted heat pump (heating mode to minus 10 degrees C) with "
             "two 12 kW resistive booster heaters below that; electric driver's heater. No fuel-fired heater, as required by "
             "the city's clean fleet terms for the 2027 contract"],
            ["Preconditioning", "Cabin and battery preconditioning from the charger before departure (not from the traction battery)"],
            ["Warranty", "Battery 8 years or 500,000 km, to 70 per cent of usable capacity"],
            ["Price", "EUR 548,000 per bus excluding VAT, delivered Niittylä; charger cabinets quoted separately"],
            ["Delivery", "August to September 2027 for orders placed by 15 January 2027; four to thirty buses"]]
    s = [Paragraph("%s, Teollisuuskatu 9, 90400 Oulu" % P.DEALER, small),
         Paragraph("Tel. 020 7421 300 | sales@pohjanmaanbussihuolto.fi", small), Spacer(1, 10),
         Paragraph("6 October 2026", body),
         Paragraph("%s, %s, Varikkotie 8, 44120 %s" % (P.PEOPLE["planner"], P.ORG, P.TOWN), body), Spacer(1, 4),
         Paragraph("Quotation 26-0931: %s %s battery-electric buses for delivery in 2027" % (P.EMAKE, P.EMODEL), h1),
         Paragraph("Dear Mr Virta,", body),
         Paragraph("Thank you for the visit to Niittylä on 29 September. As agreed, we quote below for the 2027 model "
                   "year %s %s for your Niittylä depot. The specification follows the city's clean fleet terms, which "
                   "differ from your 2025 pilot buses in the heating system." % (P.EMAKE, P.EMODEL), body),
         _grid(rows, [100, 370], cell), Spacer(1, 6),
         Paragraph("The buses report their daily summaries to the same telematics portal as your 2025 buses. Service and "
                   "battery monitoring for the first three years are included under our standard agreement, from your own "
                   "workshop with our support.", body),
         Paragraph("We would need your order by 15 January 2027 to hold the August and September 2027 build slots.", body),
         Paragraph("Kind regards,", body), Spacer(1, 6), Paragraph(P.PEOPLE["dealer"], body),
         Paragraph("Key account manager, %s" % P.DEALER, small)]
    O.build(path, s, "Quotation 26-0931", P.PEOPLE["dealer"], "Battery-electric buses for delivery in 2027",
            "%s | Quotation 26-0931" % P.DEALER, dt.datetime(2026, 10, 6, 13, 48, tzinfo=FI_S),
            dt.datetime(2026, 10, 6, 14, 2, tzinfo=FI_S), producer="LibreOffice 25.8.1.1")
