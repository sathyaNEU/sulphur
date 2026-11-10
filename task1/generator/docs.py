"""Tekenbord's ARR reporting policy, version 4: the finance team's Word document exported to PDF by LibreOffice
Writer (officepdf.build). It files what ARR is, the plan rate, what is left out, how a Team subscription's ARR is
read, and the movement categories in their order; it says nothing about how a forecast is made."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

CET = dt.timezone(dt.timedelta(hours=1))

POLICY = [
    ("1. Purpose and scope", [
        "1.1 This policy sets how Tekenbord B.V. measures annual recurring revenue (ARR) in its management accounts, "
        "its board reports and its annual plan. It applies to every figure labelled ARR, whether a month-end "
        "actual or a plan figure, and to every report of the movement in ARR between two dates.",
        "1.2 Revenue recognition in the statutory accounts follows the accounting policies in the annual report and "
        "is not governed by this policy."]),
    ("2. What ARR is", [
        "2.1 ARR at a month end is the sum, over every subscription in force on the last day of that month, of its "
        "recurring subscription charge annualised. A Business contract is in force from its service start to its "
        "service end. Its ARR is the seats in force on that day multiplied by the contracted price per seat per "
        "month, multiplied by twelve. Seats added to a contract during its term count from the start of the "
        "true-up line that adds them.",
        "2.2 One-off charges are not ARR: onboarding fees, training and the part-term charge raised on a true-up "
        "line for the rest of the term. Taxes are excluded.",
        "2.3 Amounts in pounds sterling are converted to euros at the plan rate of EUR %.2f per GBP. The plan "
        "rate is used for every ARR figure dated in 2026 and for the 2027 plan, so that movements are not affected "
        "by exchange rates." % P.PLAN_RATE_GBP,
        "2.4 A Team subscription is in force on a day when a paid Team invoice's service period includes that day. "
        "Its ARR is the seats billed on that invoice multiplied by the price per seat on it, multiplied by "
        "twelve. An invoice whose payment did not go through is not a paid invoice.",
        "2.5 Customers who sign after a date are part of ARR from the service start of their first contract or "
        "first paid Team invoice."]),
    ("3. Accounts and plans", [
        "3.1 ARR is held by the billing account. A Business account holds an annual Business contract; a Team "
        "account pays monthly on the Team plan. Logo counts are counts of billing accounts with ARR at the month "
        "end.",
        "3.2 List prices, minimum seats and their effective dates are set in the price book approved by the CFO. "
        "Contracted prices are those on the contract's billing lines."]),
    ("4. The movement in ARR", [
        "4.1 The movement between two month ends is reported in the categories below, in this order, and the "
        "categories add up to the change in total ARR: new Business, Business seat additions, price, Business seat "
        "reductions, Business accounts lost, and the change in Team.",
        "4.2 New Business is the ARR of a Business contract's first term, at its service start, including accounts "
        "that move to Business from the Team plan. Business seat additions are the seats added to a Business "
        "contract during its term or at its renewal, at the contract's price at the time.",
        "4.3 Price is the change in the price per seat when a Business contract renews, multiplied by the seats the "
        "contract held immediately before the renewal.",
        "4.4 Business seat reductions are the seats removed when a Business contract renews, at the renewed price.",
        "4.5 Business accounts lost is the ARR of a Business contract that ends without a renewal, as it stood on "
        "its last day in force.",
        "4.6 The change in Team is the change in Team ARR between the two month ends. A Team account that moves to "
        "Business leaves Team ARR, and its Business contract is new Business."]),
    ("5. Plan figures", [
        "5.1 ARR figures in the plan and in board reports for months that have not ended are forecasts made from "
        "the company's own records: the billing system, the product's usage data and the CRM. Finance reviews "
        "every plan figure before it goes to the board.",
        "5.2 A figure put to the board as a commitment states the chance of meeting it."]),
    ("6. Ownership and review", [
        "6.1 The CFO owns this policy. Revenue operations prepares the monthly ARR report and its movement; Finance "
        "reconciles it to the billing system each month.",
        "6.2 The policy is reviewed every year before the plan cycle. Questions to the finance team."]),
]


def policy(path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4,
                          spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17,
                        spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    s = [Paragraph("Tekenbord B.V., Finance", small),
         Paragraph("ARR reporting policy", h1),
         Paragraph("Version 4, approved 9 February 2026 by Naomi Weijters, CFO. Replaces version 3 (February 2025).",
                   small), Spacer(1, 4)]
    for head, paras in POLICY:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    rows = [["Version", "Date", "Change"],
            ["2", "March 2024", "Team plan ARR added"],
            ["3", "February 2025", "Movement categories split into seat additions, price and seat reductions"],
            ["4", "February 2026", "Plan rate for 2026 and the 2027 plan; one-off charges listed"]]
    t = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[50, 80, 330], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s += [Spacer(1, 6), Paragraph("Document history", h2), t]
    O.build(path, s, "ARR reporting policy", "Naomi Weijters", "ARR reporting policy, version 4",
            "Tekenbord B.V. | ARR reporting policy v4", dt.datetime(2026, 2, 9, 9, 40, tzinfo=CET),
            dt.datetime(2026, 2, 9, 11, 2, tzinfo=CET), producer="LibreOffice 25.8.4.2")
