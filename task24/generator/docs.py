"""task24: the vendor's governing documents and the clients' requests for quotation, each a Word document exported
to PDF by LibreOffice Writer through the house writer, with its owner's name and its own issue and save times."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import world as Wd

EAT = dt.timezone(dt.timedelta(hours=3))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.0, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.2,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.4)
    return body, h1, h2, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def pricing_policy(path):
    body, h1, h2, cell = _styles()
    mm = 2.83
    s = [Paragraph("Pricing policy for annotation requests", h1),
         _grid([["Document", "FIN-POL-04, version 4"], ["Owner", "Loice Mumo, Finance, Pellucid Annotation Ltd"],
                ["Issued", "14 September 2026"], ["Applies to", "requests for quotation received from 1 October 2026"]],
               [40 * mm, 130 * mm], cell),
         Paragraph("1. Purpose", h2),
         Paragraph("Clients send requests for quotation with a price they are prepared to pay per image or per frame. This "
                   "policy sets how Finance costs a request before it is accepted and the line a request must clear.", body),
         Paragraph("2. The cost of delivering a request", h2),
         Paragraph("A request is costed as its expected cost of delivery per delivered image (per frame for video tracking). "
                   "A delivered image is an image of the request accepted by QA and handed to the client. The cost of "
                   "delivery is the sum of three lines:", body),
         Paragraph("(a) annotator pay: the piece pay and the floor top-ups the annotator pay policy would pay for the "
                   "request's work;", body),
         Paragraph("(b) QA: the paid time of the QA reviewers who review the request's work, at their hourly rates, a "
                   "reviewer's paid time being shared across the work reviewed in proportion to review time;", body),
         Paragraph("(c) overhead: USD 1.55 per paid hour of annotators and of reviewers on the request.", body),
         Paragraph("Paid time is the time the punch clock records under the annotator pay policy. Transport allowances, pay "
                   "adjustments and pre-labelling compute sit in the overhead rate and are not costed separately. Where an "
                   "annotator's pay week spans more than one project, the week's pay and paid hours are shared across the "
                   "projects in proportion to the labelling tool's active time.", body),
         Paragraph("3. Who works a request", h2),
         Paragraph("A request is costed as worked at both delivery centres by the annotators on the staff roster at the "
                   "costing date who hold the request's skill (bounding boxes, polygons or video tracking), each annotator's "
                   "share of the work in proportion to their contracted weekly hours, and an annotator's weeks on the request "
                   "spent on it. The work is reviewed by the QA reviewers of the annotator's centre.", body),
         Paragraph("4. Acceptance", h2),
         Paragraph("A request is accepted when the price the client offers per image (per frame) is at least 1.18 times its "
                   "expected cost of delivery. Where it is not, the lowest price at which it could be accepted is 1.18 times "
                   "that cost, and Sales may go back to the client with it.", body),
         Paragraph("5. Records", h2),
         Paragraph("Costing uses the delivery centres' own records: the labelling tool's task passes, the QA system's "
                   "reviews, the punch clock, the pay register and the video delivery archive.", body)]
    O.build(path, s, title="Pricing policy for annotation requests", author="Loice Mumo", subject="FIN-POL-04 v4",
            footer="FIN-POL-04 v4  |  Pellucid Annotation Ltd", created=dt.datetime(2026, 9, 14, 10, 12, tzinfo=EAT),
            modified=dt.datetime(2026, 9, 14, 16, 41, tzinfo=EAT))


def pay_policy(path):
    body, h1, h2, cell = _styles()
    mm = 2.83
    s = [Paragraph("Annotator pay policy 2026", h1),
         _grid([["Document", "HR-PAY-2026"], ["Owner", "Mourine Kipngetich, People and Payroll"], ["Issued", "15 December 2025"],
                ["Applies to", "annotators at Kisumu and Iloilo, pay weeks from 5 January 2026"]], [40 * mm, 130 * mm], cell),
         Paragraph("1. Piece rates", h2),
         _grid([["Work", "Piece rate (USD)"], ["Bounding boxes", "0.0128 per object"], ["Polygon segmentation", "0.0330 per polygon"],
                ["Video tracking", "0.0260 per track and 0.0075 per frame worked"]], [80 * mm, 90 * mm], cell),
         Spacer(1, 5),
         Paragraph("Piece pay is credited when a task is first submitted, in the pay week of the submission. A correction "
                   "made after QA returns a task is not paid as a piece.", body),
         Paragraph("2. The hourly floor", h2),
         Paragraph("An annotator's pay for a pay week is at least the centre's floor times the week's paid hours: USD 2.40 per "
                   "paid hour at Kisumu and USD 2.70 at Iloilo. Where the week's piece pay falls short of that, payroll pays the "
                   "difference as a floor top-up for the week.", body),
         Paragraph("3. Paid hours", h2),
         Paragraph("Paid hours are the time between a shift's IN and OUT punches less the unpaid lunch break (45 minutes at "
                   "Kisumu, 60 minutes at Iloilo). A second IN punch within five minutes of the first counts once. A shift the "
                   "clock closes at midnight is paid as the supervisor's edit records it.", body),
         Paragraph("4. The pay week and allowances", h2),
         Paragraph("The pay week runs Monday to Sunday. A transport allowance is paid for each week worked (USD 3.50 at Kisumu, "
                   "USD 4.00 at Iloilo); it is not part of the floor test.", body)]
    O.build(path, s, title="Annotator pay policy 2026", author="Mourine Kipngetich", subject="HR-PAY-2026",
            footer="HR-PAY-2026  |  People and Payroll", created=dt.datetime(2025, 12, 15, 9, 5, tzinfo=EAT),
            modified=dt.datetime(2025, 12, 15, 11, 52, tzinfo=EAT))


def qa_standard(path):
    body, h1, h2, cell = _styles()
    mm = 2.83
    s = [Paragraph("QA review standard", h1),
         _grid([["Document", "QA-STD-03, version 3"], ["Owner", "Collins Mutuku, Quality"], ["Issued", "2 March 2026"],
                ["Applies to", "every task submitted at Kisumu and Iloilo"]], [40 * mm, 130 * mm], cell),
         Paragraph("1. Review", h2),
         Paragraph("Every submitted task is reviewed by a QA reviewer of the annotator's centre, and each review's time is "
                   "logged against it.", body),
         Paragraph("2. Returns", h2),
         Paragraph("A reviewer returns a task to its annotator when the review finds any missed object, or any box, polygon or "
                   "track placed outside the client's tolerance. A task with nothing found is accepted.", body),
         Paragraph("3. Corrections", h2),
         Paragraph("The annotator re-checks the whole returned task and fixes what was found; the corrected task is reviewed "
                   "again under section 2. After a task's fourth review the QA lead completes any fix still needed and the "
                   "task is accepted.", body),
         Paragraph("4. Counting objects", h2),
         Paragraph("The labelling tool counts a task's boxes by size: small under 32 by 32 pixels of box area, medium under 96 "
                   "by 96, large otherwise; occluded as the annotator marks it.", body)]
    O.build(path, s, title="QA review standard", author="Collins Mutuku", subject="QA-STD-03 v3",
            footer="QA-STD-03 v3  |  Quality", created=dt.datetime(2026, 3, 2, 8, 40, tzinfo=EAT),
            modified=dt.datetime(2026, 3, 2, 13, 18, tzinfo=EAT))


RFQ = {
    "A": dict(file="RFQ_Corvane_CRV-2027-014.pdf", ref="CRV-2027-014", contact="Maria Osborn, Data Operations",
              data="dashcam stills at crowded city-centre junctions and market streets, 1920 by 1080, daytime and dusk", spec="bounding boxes on every road user "
              "(cars, pedestrians, cyclists, buses), occlusion flag on each", unit="image",
              sent=dt.datetime(2026, 10, 27, 17, 5, tzinfo=dt.timezone(dt.timedelta(hours=-4)))),
    "B": dict(file="RFQ_Shelfgrid_SG27-03.pdf", ref="SG27-03", contact="Eleanor Wilson, Computer Vision",
              data="supermarket shelf photographs, 1920 by 1080", spec="bounding boxes on every product facing, price tag, "
              "gap and promotion, occlusion flag on each", unit="image",
              sent=dt.datetime(2026, 10, 28, 15, 22, tzinfo=dt.timezone(dt.timedelta(hours=0)))),
    "C": dict(file="RFQ_Ardley_HWY-Q1-27.pdf", ref="HWY-Q1-27", contact="Malte Mosemann, Perception",
              data="highway dashcam video, 10 frames per second, sequences of about 30 seconds", spec="a box and track "
              "identity on every vehicle in every frame", unit="frame",
              sent=dt.datetime(2026, 10, 29, 9, 48, tzinfo=dt.timezone(dt.timedelta(hours=1)))),
    "D": dict(file="RFQ_Brindle_BPS-2027-02.pdf", ref="BPS-2027-02", contact="Wayne Carter, Automation",
              data="warehouse dock camera stills of wrapped and unwrapped pallets, 2448 by 2048", spec="polygon on every "
              "pallet, wrapped load and loose item, following the load's outline, occlusion flag on each", unit="image",
              sent=dt.datetime(2026, 10, 30, 8, 31, tzinfo=dt.timezone(dt.timedelta(hours=11)))),
    "E": dict(file="RFQ_Kestrin_KW-2701.pdf", ref="KW-2701", contact="Jorge Berry, Inventory Systems",
              data="rack-face photographs of shelf labels and cartons, 1920 by 1080", spec="bounding boxes on every label, "
              "barcode, carton and pallet tag, occlusion flag on each", unit="image",
              sent=dt.datetime(2026, 11, 2, 11, 14, tzinfo=dt.timezone(dt.timedelta(hours=0)))),
}


def rfq(path, key, price, sample_file):
    body, h1, h2, cell = _styles()
    mm = 2.83
    rq, r = Wd.REQUESTS[key], RFQ[key]
    vol = "{:,}".format(rq["volume"])
    s = [Paragraph("Request for quotation %s" % r["ref"], h1),
         _grid([["Client", rq["client"]], ["Contact", r["contact"]], ["To", "Pellucid Annotation Ltd, Sales"],
                ["Sent", r["sent"].strftime("%d %B %Y").lstrip("0")]], [40 * mm, 130 * mm], cell),
         Paragraph("Work", h2),
         _grid([["Item", "Detail"], ["Data", r["data"]], ["Annotation", r["spec"]], ["Volume", "%s %ss" % (vol, r["unit"])],
                ["Delivery", "in weekly batches from 11 January 2027, complete by 26 March 2027"],
                ["Quality", "your own QA; we audit 2 per cent of each batch"],
                ["Our price", "USD %.4f per %s, all in" % (price, r["unit"]) if r["unit"] == "frame" else
                 "USD %.2f per %s, all in" % (price, r["unit"])]],
               [40 * mm, 130 * mm], cell),
         Spacer(1, 6),
         Paragraph("A random sample from the full set, labelled to the same specification by our previous supplier, is "
                   "attached as %s so you can see what the work involves. Please confirm by 20 November 2026 whether you can "
                   "take the work at our price." % sample_file, body)]
    O.build(path, s, title="Request for quotation %s" % r["ref"], author=r["contact"].split(",")[0],
            subject="%s annotation" % rq["client"], footer="%s  |  %s" % (r["ref"], rq["client"]),
            created=r["sent"] - dt.timedelta(hours=2, minutes=11), modified=r["sent"] - dt.timedelta(minutes=7))
