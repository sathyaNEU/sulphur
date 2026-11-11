"""task9 documents: the capital review policy the allocation committee works under and the risk model's factor
definitions. Each is a Word document exported by LibreOffice Writer through the house writer, with its owner as
author and its own issue time."""
import datetime as dt

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf as O
import params as P

EST = dt.timezone(dt.timedelta(hours=-5))
EDT = dt.timezone(dt.timedelta(hours=-4))

# ---- the policy's sentences, kept once so the checks and the verifier read the same text
REVIEW = ("The allocation committee meets each December and sets the capital every pod will run in the coming calendar "
          "year, effective on its first trading day. It reviews each pod on its record over the past three years, or "
          "since it started, and on its strategy group's year, and moves capital toward the pods whose records have been "
          "strongest, within the platform's capital budget for the year. A pod whose record would move its capital by "
          "less than 10 per cent keeps its capital; other figures are rounded to USD 5 million. No pod runs less than "
          "USD 40 million or more than USD 1.4 billion.")
ONBOARD = ("A new pod starts at 25 per cent of the capital it is hired to run, moves to 50 per cent after 126 trading "
           "days and to its full capital after 252 trading days. It is not reviewed until its onboarding is complete.")
DRAWDOWN = ("A pod's capital is halved for the rest of the calendar year when its P&amp;L for the year falls 5 per cent of "
            "its capital below the highest point that P&amp;L has reached in the year, and the pod is closed when it falls "
            "7.5 per cent below that point. Both are measured on the capital the pod ran before any halving that year.")
FUNDING = ("Each pod is charged funding on 20 per cent of its capital, at the 3-month Treasury bill rate plus 0.35 per "
           "cent a year, accrued on calendar days at the latest published bill rate.")
PAYOUT = ("A pod's PM team is paid 18 per cent of the pod's P&amp;L for the calendar year after its funding charge, when "
          "that P&amp;L is positive, and nothing when it is negative. A pod that is closed, or whose PM team leaves, "
          "during the year is paid on its P&amp;L to its last trading day. Each pod is paid on its own result.")
ALPHA = ("A pod's alpha is the P&amp;L it earns beyond what a passive holding of the markets it trades would have earned "
         "over the same days, the holding sized to the pod's exposures over its whole record on the platform and measured "
         "on the published market series the platform keeps, and is stated as a per cent of its capital a year.")
PLAN_A = ("The plan budgets alpha only: it expects the markets themselves to earn nothing over the plan year.")
PLAN_B = ("Each pod in the plan runs the whole year at its planned capital, a pod on its onboarding schedule at its "
          "scheduled capital, under the drawdown rules. The plan does not anticipate departures or new pods.")
PLAN_C = ("The plan's net P&amp;L is after funding, at the bill rate on the review date, after PM payouts, and after the "
          "platform's own costs in the year's budget.")
PLAN_D = "The plan's range is the 10th to the 90th percentile of the year's net P&amp;L."
PLAN_E = ("Capacity is stated as the share of its alpha per dollar a pod gives up when its capital doubles, the same "
          "share at any size.")
PLAN_F = ("The plan reads each pod's expected alpha from its whole record on the platform together with its strategy "
          "group's, giving the pod's own record the more weight the longer and less noisy it is.")
HURDLE = ("An increase in a pod's capital is approved only if the plan expects it to add at least 1.5 per cent a year of "
          "net P&amp;L, after the pod's PM payout and funding, on the capital it adds.")
RECORDS = ("The risk system's daily P&amp;L and capital are the record for the review. The administrator's month-end "
           "statements are the books of account.")

RM_INTRO = ("The risk model attributes each pod's daily P&amp;L to eight market factors. Each factor is a daily return "
            "built from published closing levels; a pod's betas are estimated on its daily P&amp;L over its last 252 "
            "trading days, and what the factors do not explain is the pod's specific P&amp;L.")
RM_FILL = "On a day a series is not published, its last published level is carried forward."
RM_ROWS = [
    ("MKT", "Daily return of the S&amp;P 500 index", "Cboe SPX"),
    ("TECH", "Daily return of the Nasdaq-100 index less that of the S&amp;P 500", "FRED NASDAQ100"),
    ("RATES", "Minus 8 times the daily change in the 10-year Treasury yield (in decimals)", "FRED DGS10"),
    ("CURVE", "4 times the daily change in the 10-year less the 2-year Treasury yield", "FRED DGS10, DGS2"),
    ("CREDIT", "Minus 6 times the daily change in Moody's Baa yield less the 10-year Treasury yield", "FRED DBAA, DGS10"),
    ("USD", "Daily return of the nominal broad dollar index", "FRED DTWEXBGS"),
    ("OIL", "Daily return of Brent crude", "FRED DCOILBRENTEU"),
    ("VOL", "Minus the daily change in the VIX, divided by 100", "Cboe VIX"),
]
RM_HISTORY = [("v1", "January 2017", "Seven factors; CREDIT on Moody's Aaa yield less the 10-year Treasury yield"),
              ("v2", "April 2020", "VOL added"),
              ("v3", "July 2023", "CREDIT moved to the Baa yield; carried to the new risk system")]


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    head = ParagraphStyle("head", parent=body, fontName="Helvetica-Bold", fontSize=10.4, spaceBefore=6, spaceAfter=3)
    title = ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=2)
    small = ParagraphStyle("small", parent=body, fontSize=8.4, leading=11, textColor="#444444")
    cell = ParagraphStyle("cell", parent=body, fontSize=8.8, leading=11.4, spaceAfter=0)
    return body, head, title, small, cell


def policy(path):
    body, head, title, small, cell = _styles()
    s = [Paragraph("%s" % P.PLATFORM_LEGAL, small), Paragraph("Capital Review Policy", title),
         Paragraph("Owner: Office of the Chief Investment Officer. Approved by the allocation committee on 14 October 2026; "
                   "replaces the edition of 3 October 2023.", small), Spacer(1, 6),
         Paragraph("1. Scope", head),
         Paragraph("This policy sets how the allocation committee reviews the platform's portfolio-manager pods, sets the "
                   "capital each runs, and prepares its plan for the coming year.", body),
         Paragraph("2. The annual review", head), Paragraph(REVIEW, body),
         Paragraph("3. New pods", head), Paragraph(ONBOARD, body),
         Paragraph("4. Drawdown rules", head), Paragraph(DRAWDOWN, body),
         Paragraph("5. Funding", head), Paragraph(FUNDING, body),
         Paragraph("6. PM payouts", head), Paragraph(PAYOUT, body),
         Paragraph("7. Alpha", head), Paragraph(ALPHA, body),
         Paragraph("8. The plan for the year", head),
         Paragraph("The plan the committee approves sets out each pod's capital for the year and the platform's expected "
                   "net P&amp;L with its range.", body),
         Paragraph("(a) " + PLAN_A, body), Paragraph("(b) " + PLAN_B, body), Paragraph("(c) " + PLAN_C, body),
         Paragraph("(d) " + PLAN_D, body), Paragraph("(e) " + PLAN_E, body), Paragraph("(f) " + PLAN_F, body),
         Paragraph("9. Increases", head), Paragraph(HURDLE, body),
         Paragraph("10. Records", head), Paragraph(RECORDS, body),
         Spacer(1, 8),
         Paragraph("Questions on this policy go to the Office of the Chief Investment Officer. The policy is reviewed every "
                   "three years or when the committee's process changes.", small)]
    O.build(path, s, "Capital Review Policy", P.CIO, "Capital review policy", "%s | Capital Review Policy | Internal" % P.PLATFORM,
            dt.datetime(2026, 10, 14, 10, 12, 0, tzinfo=EDT), dt.datetime(2026, 10, 14, 16, 48, 33, tzinfo=EDT), page_of=True)


def risk_model(path):
    body, head, title, small, cell = _styles()
    rows = [[Paragraph("<b>Factor</b>", cell), Paragraph("<b>Definition</b>", cell), Paragraph("<b>Series</b>", cell)]]
    rows += [[Paragraph(a, cell), Paragraph(b, cell), Paragraph(c, cell)] for a, b, c in RM_ROWS]
    hist = [[Paragraph("<b>Version</b>", cell), Paragraph("<b>Effective</b>", cell), Paragraph("<b>Change</b>", cell)]]
    hist += [[Paragraph(a, cell), Paragraph(b, cell), Paragraph(c, cell)] for a, b, c in RM_HISTORY]
    s = [Paragraph("%s | Risk" % P.PLATFORM, small), Paragraph("Risk Model Methodology (version 3)", title),
         Paragraph("Owner: %s, Chief Risk Officer. Effective 3 July 2023 with the new risk system." % P.CRO, small), Spacer(1, 6),
         Paragraph("Purpose", head), Paragraph(RM_INTRO, body), Paragraph(RM_FILL, body),
         Paragraph("Factors", head), Table(rows, colWidths=[52, 300, 120]),
         Spacer(1, 6),
         Paragraph("Use", head),
         Paragraph("Factor betas set each pod's market risk limits and the daily risk report. Factor P&amp;L on a day is a "
                   "pod's beta to each factor times the factor's return times the pod's capital.", body),
         Paragraph("Version history", head), Table(hist, colWidths=[52, 90, 330])]
    O.build(path, s, "Risk Model Methodology", P.CRO, "Risk model factor definitions, version 3",
            "%s | Risk Model Methodology (version 3) | Internal" % P.PLATFORM,
            dt.datetime(2023, 6, 27, 9, 31, 0, tzinfo=EDT), dt.datetime(2023, 6, 29, 15, 6, 44, tzinfo=EDT), page_of=True,
            producer="LibreOffice 7.5")
