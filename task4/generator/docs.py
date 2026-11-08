"""task4 documents: Owenduff's offer letter and Brackloon's network planning standard NPS-3, both PDFs written the way
the two offices write them (a Word document exported by LibreOffice Writer)."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

IE = dt.timezone(dt.timedelta(hours=1))
IE_W = dt.timezone(dt.timedelta(hours=0))


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


def offer(path):
    body, h1, h2, small, cell = _styles()
    rows = [["District", "Brackloon code"]] + [[P.D[c][0], c] for c in P.OFFER]
    s = [Paragraph("Owenduff Couriers, Unit 7, Lannagh Business Park, Castlebar Road, Westport, Co. Mayo F28 X2K4", small),
         Paragraph("Tel. 098 52 714 | accounts@%s" % P.PARTNER_DOMAIN, small), Spacer(1, 10),
         Paragraph("21 October 2026", body),
         Paragraph("Niamh Gilbride, Head of Logistics, Brackloon Direct Ltd, Unit 4, Breaffy Business Park, Castlebar, "
                   "Co. Mayo", body), Spacer(1, 4),
         Paragraph("Delivery of Brackloon parcels in outlying districts, 2027", h1),
         Paragraph("Dear Niamh,", body),
         Paragraph("Thank you for the meeting at Breaffy on 7 October. As discussed, Owenduff would be glad to take on "
                   "delivery of Brackloon's parcels in some or all of the districts listed below from 1 January 2027. "
                   "We already deliver for four shippers across west Mayo and Connemara six days a week, so your "
                   "parcels would travel with theirs from our Westport hub.", body),
         Paragraph("Districts offered", h2), _grid(rows, [200, 120], cell), Spacer(1, 6),
         Paragraph("Brackloon tells us which of the districts above it is handing over by giving us the list by "
                   "30 November 2026.", body),
         Paragraph("Terms", h2),
         Paragraph("Price: EUR %s per parcel delivered, excluding VAT, fixed for the calendar year 2027. The price "
                   "covers parcels as Brackloon packs them today, up to 30 kg each." % ("%.2f" % P.PRICE_2027), body),
         Paragraph("Collection: our van collects the day's parcels for the handed-over districts from your Castlebar "
                   "depot by 08:15 each delivery day. Delivery is the same day for parcels collected by 08:15.", body),
         Paragraph("Failed deliveries are attempted again the next delivery day at no further charge; a parcel is "
                   "charged once, when it is delivered. Collections from customers in the handed-over districts are "
                   "included at no charge.", body),
         Paragraph("Invoicing monthly in arrears against our proof-of-delivery record, payment at 30 days. The "
                   "agreement runs for the calendar year 2027 and renews for 2028 at a price we would agree with you by "
                   "30 September 2027.", body),
         Paragraph("I look forward to hearing from you.", body), Paragraph("Yours sincerely,", body), Spacer(1, 6),
         Paragraph("Karl Eivers", body), Paragraph("Commercial Manager, Owenduff Couriers", small)]
    O.build(path, s, "Delivery of Brackloon parcels in outlying districts, 2027", "Karl Eivers",
            "Offer to Brackloon Direct Ltd", "Owenduff Couriers | Offer OC-2027-114",
            dt.datetime(2026, 10, 21, 15, 2, tzinfo=IE), dt.datetime(2026, 10, 21, 15, 9, tzinfo=IE))


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, Logistics" % P.ORG, small),
         Paragraph("NPS-3 Network planning standard: delivery districts and delivery partners", h1),
         Paragraph("Version 2, issued 3 March 2025. Replaces version 1 (May 2023). Owner: the Head of Logistics.", small),
         Spacer(1, 4)]
    sec = [
        ("1. Scope", [
            "This standard governs how Brackloon's delivery network is described for planning, and how the company "
            "decides each year whether to hand any delivery district to a delivery partner. It applies to every "
            "district in the district register and every run in the van run log."]),
        ("2. Terms", [
            "2.1 A delivery district is a district of the district register. Every customer address belongs to one "
            "district, and every district belongs to one run.",
            "2.2 A run is the daily route of one van over its territory, identified by its run code. A van leaves the "
            "Castlebar depot, delivers and collects in the districts of its run and returns to the depot.",
            "2.3 A van-hour is an hour of a van on a run, counted from depot out to depot in as the van run log "
            "records them.",
            "2.4 A parcel is a parcel delivered to a customer. A collection or an attempt at which nothing was "
            "delivered is not a parcel."]),
        ("3. Service in a district handed to a partner", [
            "3.1 A partner taking a district delivers every Brackloon parcel for that district, including the "
            "customer collections there, on the delivery day Brackloon would have delivered it.",
            "3.2 Brackloon's own runs then make no stop in the district. A district is handed over whole or not at "
            "all."]),
        ("4. The decision for a year", [
            "4.1 The saving of a hand-over for a year is the cost, at the year's all-in van-hour rate, of the "
            "van-hours the hand-over takes off Brackloon's runs in the year, less what the partner charges for the "
            "parcels it delivers in the handed-over districts in the year.",
            "4.2 The year's parcels are the commercial plan's parcels for the year, district by district; the year's "
            "rate is the fleet rate card's all-in van-hour rate for the year; the year's delivery days are the "
            "delivery calendar's.",
            "4.3 The districts handed over for a year are the selection from the partner's offer whose hand-over "
            "lowers the year's delivery cost most. Where no district's hand-over lowers it, none is handed over.",
            "4.4 The decision is made each autumn for the following calendar year, before the partner's offer lapses, "
            "and is reported with the year's saving."]),
        ("5. Review", [
            "5.1 This standard is reviewed every two years or when the network changes. Comments to the Head of "
            "Logistics."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    O.build(path, s, "NPS-3 Network planning standard", "Niamh Gilbride", "Delivery districts and delivery partners",
            "Brackloon Direct Ltd | NPS-3 version 2", dt.datetime(2025, 3, 3, 10, 14, tzinfo=IE_W),
            dt.datetime(2025, 3, 3, 11, 40, tzinfo=IE_W))
