"""task9 (architecture 10): the credit desk's electronic quoting policy, the document the electronic trading committee
works under. A Word document exported by LibreOffice Writer through the house writer, with its owner as author and its
own issue time. Its sentences are kept once here so the checks and the verifier read the same text.
"""
import datetime as dt

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table

import officepdf as O
import params as P

EDT = dt.timezone(dt.timedelta(hours=-4))

SCOPE = ("This policy governs the desk's automated responses to requests for quote in USD investment grade and high yield "
         "corporate bonds on Tidewell Credit Network, the schedule the auto-quoter prices them from, and how the desk "
         "plans the year's P&amp;L when the electronic trading committee approves a new schedule. Voice trading and new "
         "issues are outside it.")
SEGMENTS = ("A request's segment is its bond's rating band on the request's date (investment grade for an issuer rated BBB "
            "or above in the issuer ratings history, high yield below), its bond's liquidity bucket in the security master "
            "for the request's quarter, and the client's type in the Tidewell client list. The security master sets each "
            "bond's bucket at the start of a quarter from the trades the bond printed in the quarter before.")
QUOTER = ("The auto-quoter answers a request with a price at a distance from the reference mid: Ashcote's evaluated mid at "
          "the prior close, moved with the day's Treasury curve and with the rating band's spread move as the desk's "
          "pricing feed streams them. The distance is set by the schedule in force for the request's segment, together "
          "with the size and VIX multiples, the quoter's jitter and its inventory skew, as the schedule workbook states. "
          "The auto-quoter passes on a request that would take a bond's position past its limit, and on its own checks.")
INVENTORY = ("The desk hedges each day's interest rate risk with Treasuries and sells positions to other dealers over the "
             "days after it takes them on. The inventory's coupon accrual and its funding are booked to Treasury's carry "
             "ledger and are not part of the desk's P&amp;L.")
PNL = ("For planning, the desk counts a trade's P&amp;L as (a) its edge at execution, the distance between the trade price "
       "and the reference mid on the face traded; less (b) the move in the bond's value against the desk after the trade, "
       "net of the move of the Treasury curve and of the median move in the evaluated spreads of other issuers' bonds of its rating, read as soon as that move is complete; less (c) "
       "the offload charge for the bond's bucket, in cents per 100 face: investment grade liquid 1.2, medium 2.4, thin "
       "4.8; high yield liquid 4.2, medium 8.4, thin 15.6.")
PLAN_A = ("A schedule is priced by what the desk's requests since it began quoting on Tidewell on 3 January 2023 would "
          "have made at that schedule's quotes. Each request keeps everything but the desk's half-spread: its size, time, VIX and inventory terms and "
          "its jitter, the other dealers' prices and whether its client traded; a request its client did not trade, or "
          "the desk passed, stays as it was.")
PLAN_B = "Each segment is carried at the number of requests it received in the twelve months to 31 October 2026."
PLAN_C = ("The plan's range is the 10th to the 90th percentile of the year's P&amp;L, its 251 trading days drawn from the "
          "record's own days at the plan's request counts.")
RECORDS = ("Tidewell's request audit is the record of the requests and the desk's responses; its export moved to a new "
           "format on 7 April 2025. The desk's blotter is the record of its trades, and Ashcote's evaluated prices are "
           "its marks.")


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    head = ParagraphStyle("head", parent=body, fontName="Helvetica-Bold", fontSize=10.4, spaceBefore=6, spaceAfter=3)
    title = ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=2)
    small = ParagraphStyle("small", parent=body, fontSize=8.4, leading=11, textColor="#444444")
    return body, head, title, small


def policy(path):
    body, head, title, small = _styles()
    s = [Paragraph("%s | Credit trading" % P.FIRM, small), Paragraph("Electronic Quoting Policy (2026 edition)", title),
         Paragraph("Owner: %s, head of credit trading. Approved by the electronic trading committee on 15 October 2026; "
                   "replaces the 2024 edition." % P.HEAD, small),
         Paragraph("1. Scope", head), Paragraph(SCOPE, body),
         Paragraph("2. Segments", head), Paragraph(SEGMENTS, body),
         Paragraph("3. The auto-quoter", head), Paragraph(QUOTER, body),
         Paragraph("4. Inventory", head), Paragraph(INVENTORY, body),
         Paragraph("5. P&amp;L for planning", head), Paragraph(PNL, body),
         Paragraph("6. The year's plan", head),
         Paragraph("When the committee is asked to approve a new schedule, the desk sets out the year's P&amp;L under the "
                   "schedule in force and under the new one.", body),
         Paragraph("(a) " + PLAN_A, body), Paragraph("(b) " + PLAN_B, body), Paragraph("(c) " + PLAN_C, body),
         Paragraph("7. Records", head), Paragraph(RECORDS, body),
         Paragraph("Changes to the schedule are proposed by the desk's strategist and approved by the committee; the "
                   "committee meets in March, June, October and December.", small)]
    O.build(path, s, "Electronic Quoting Policy", P.HEAD, "Credit electronic quoting policy",
            "%s | Electronic Quoting Policy (2026) | Internal" % P.FIRM,
            dt.datetime(2026, 10, 15, 16, 22, 0, tzinfo=EDT), dt.datetime(2026, 10, 16, 9, 41, 27, tzinfo=EDT),
            producer="LibreOffice 7.6")
