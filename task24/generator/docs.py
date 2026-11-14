"""task24: the pack's documents (Penvale's launch policy, the signed Tallyfield order, the Ardentdesk quote and
Tallyfield's quality summary), each a Word document exported to PDF by LibreOffice Writer through the house writer,
with its owner's name and its own issue and save times."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import world as Wd

NZ = dt.timezone(dt.timedelta(hours=13))       # New Zealand daylight time (October to April)
NZS = dt.timezone(dt.timedelta(hours=12))
MNL = dt.timezone(dt.timedelta(hours=8))
PT = dt.timezone(dt.timedelta(hours=-8))
MM = 2.83

TYPE_NAMES = {"order_delivery": "Orders and delivery", "returns_refunds": "Returns and refunds",
              "account_billing": "Account and billing", "product_howto": "Product how-to",
              "device_troubleshooting": "Device troubleshooting"}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.0, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.2,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.4)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.4, textColor=colors.HexColor("#444444"))
    return body, h1, h2, cell, small


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def launch_policy(path):
    body, h1, h2, cell, small = _styles()
    s = [Paragraph("Draftline auto-send: launch standard and label purchasing", h1),
         _grid([["Policy", "DL-03, version 2"], ["Owner", "Bridget Sanders, Support Automation, Penvale Electronics Ltd"],
                ["Standard owner", "Sam Bartlett, Lead Senior Technician, Penvale Service Centre"],
                ["Issued", "26 October 2026"], ["Applies to", "the auto-send launch and the Q1 2027 label purchase"]],
               [40 * MM, 134 * MM], cell),
         Paragraph("1. Purpose", h2),
         Paragraph("Draftline drafts two replies to each support ticket and its reward model chooses the one an agent "
                   "reviews. Auto-send would send the reward model's choice without an agent's review. This policy "
                   "sets the standard the reward model is held to before auto-send launches and how the labels bought "
                   "for its next training run are sized.", body),
         Paragraph("2. The standard", h2),
         Paragraph("A pair of draft replies to a ticket is judged under the standard by three senior technicians of "
                   "the Penvale Service Centre, each choosing, without seeing the others' choices, the reply they "
                   "would send. The standard's reply is the one at least two of the three choose.", body),
         Paragraph("The reward model's accuracy on a ticket type is the share of that type's draft pairs on which "
                   "the reply it prefers is the standard's reply. Every pair counts, whatever the split of the three "
                   "choices.", body),
         Paragraph("3. The launch bar", h2),
         Paragraph("Auto-send launches for every ticket type at once when the reward model in production is expected "
                   "to reach %.1f per cent accuracy on the planned 2027 ticket mix: each ticket type's accuracy "
                   "weighted by its share of the tickets the 2027 operating plan forecasts for the year. Expected "
                   "accuracy is the point forecast of section 7, not a high or low case." % (100 * Wd.BAR), body),
         Paragraph("4. The Q1 2027 model", h2),
         Paragraph("The next reward model will be trained in April 2027 on every usable comparison delivered in 2026 "
                   "and every usable comparison delivered in Q1 2027, and put into production if it is expected to "
                   "reach the bar. A usable comparison is one in which the judge preferred one of the two replies; a "
                   "'no preference' judgment is paid for under the vendor's terms but is not used in training.", body),
         Paragraph("5. Sizing the Q1 2027 purchase", h2),
         Paragraph("The Tallyfield order for Q1 2027 is signed (order TF-PEN-2027-Q1). Procurement adds to it only "
                   "as far as the bar needs, at the least cost, from the order's option volume, from Ardentdesk, or "
                   "from both, on each vendor's terms: the purchase is the cheapest one with which the Q1 2027 "
                   "model's expected accuracy reaches the bar. If the signed order alone reaches the bar, nothing is "
                   "added. If no purchase within the option and Ardentdesk's capacity for the quarter reaches it, "
                   "nothing is added and the launch moves to the next quarter's review.", body),
         Paragraph("6. Records", h2),
         Paragraph("The reward-model run register, the evaluation pipeline's item records, the shadow review log and "
                   "the 2026 label audit are kept by Support Automation. Vendor deliveries are kept as each vendor "
                   "exports them.", body),
         Paragraph("7. Forecasting accuracy", h2),
         Paragraph("7.1 Accuracy is forecast from the record of past training runs. On a pair one of whose replies is "
                   "better than the other, the chance that the reward model prefers the better reply rises with the "
                   "training signal it has had on the pair's ticket type as 1 - 0.5 x (1 + T/K)^(-b), where T is that "
                   "training signal, K a scale fitted for each ticket type and b a single bend fitted for all ticket "
                   "types together. The curve has no ceiling below 1. On a pair whose two replies are as good as each "
                   "other, the reward model's preferred reply is the standard's reply half of the time.", body),
         Paragraph("7.2 A reward model that always preferred the better reply would reach, on a ticket type, the share "
                   "of the type's pairs on which the standard's reply is the better one, plus half the share of pairs "
                   "whose replies are as good as each other. Forecast accuracy against the standard is read on that "
                   "basis.", body),
         Paragraph("7.3 The forecast is the curve at the values fitted on the record: the point forecast. A range may "
                   "be reported beside it and does not move it.", body),
         Spacer(1, 6),
         Paragraph("Approved by Bridget Sanders, Head of Support Automation, 26 October 2026.", small)]
    created = dt.datetime(2026, 10, 26, 10, 12, tzinfo=NZ)
    O.build(path, s, "Draftline auto-send: launch standard and label purchasing", "Bridget Sanders",
            "Policy DL-03", "Penvale Electronics Ltd  |  Policy DL-03 v2", created,
            created + dt.timedelta(minutes=41), page_of=True)
    return created + dt.timedelta(minutes=41)


def tallyfield_order(path):
    body, h1, h2, cell, small = _styles()
    by_type = Wd.order_rows()
    rows = [["Ticket type", "Comparisons"]] + [[TYPE_NAMES[t], "{:,}".format(n)] for t, n in by_type] + \
        [["Total", "{:,}".format(sum(n for _, n in by_type))]]
    s = [Paragraph("Order form TF-PEN-2027-Q1", h1),
         _grid([["Customer", "Penvale Electronics Ltd, 41 Nelson Street, Auckland 1010, New Zealand"],
                ["Supplier", "Tallyfield Inc., 2200 Western Avenue, Seattle, WA 98121, USA"],
                ["Service", "Pairwise reply comparisons, one judgment per pair, Penvale guideline v3"],
                ["Delivery", "weekly batches, 11 January to 26 March 2027"],
                ["Order date", "30 October 2026"]], [36 * MM, 138 * MM], cell),
         Paragraph("1. Volume", h2),
         Paragraph("Tallyfield will complete 300,000 comparisons on pairs Penvale supplies. Penvale draws the pairs "
                   "from its 2027 ticket stream by ticket type as follows.", body),
         _grid(rows, [90 * MM, 40 * MM], cell),
         Paragraph("2. Price", h2),
         Paragraph("USD 0.42 per completed comparison. A completed comparison is a judgment a qualified worker "
                   "submits, including a 'no preference' judgment where the guideline allows one. Total USD "
                   "126,000.00, invoiced monthly in arrears.", body),
         Paragraph("3. Option", h2),
         Paragraph("Penvale may add up to 300,000 further comparisons on the same terms and price, in steps of "
                   "10,000, by written notice before 30 November 2026. Option comparisons are drawn from Penvale's "
                   "2027 ticket stream in the same proportions by ticket type as section 1 and are delivered with "
                   "the ordered volume.", body),
         Paragraph("4. Quality", h2),
         Paragraph("Workers qualify on Tallyfield's guideline v3 test and are monitored on Tallyfield's gold "
                   "questions. Batches are delivered as CSV exports through the Tallyfield portal.", body),
         Spacer(1, 6),
         _grid([["For Penvale Electronics Ltd", "For Tallyfield Inc."],
                ["Sophie Gibson, Procurement Lead, signed 30 October 2026",
                 "Emily Dickson, Account Manager, signed 30 October 2026"]], [87 * MM, 87 * MM], cell)]
    created = dt.datetime(2026, 10, 30, 15, 2, tzinfo=NZ)
    O.build(path, s, "Order form TF-PEN-2027-Q1", "Sophie Gibson", "Tallyfield order Q1 2027",
            "Order TF-PEN-2027-Q1", created, created + dt.timedelta(minutes=26), page_of=True)
    return created + dt.timedelta(minutes=26)


def ardentdesk_quote(path):
    body, h1, h2, cell, small = _styles()
    s = [Paragraph("Quotation AD-Q-2611-07", h1),
         _grid([["To", "Sophie Gibson, Procurement, Penvale Electronics Ltd, Auckland"],
                ["From", "Amanda Estrada, Client Services, Ardentdesk Solutions Inc., Ortigas Center, Pasig City, "
                         "Metro Manila"],
                ["Date", "6 November 2026"], ["Valid until", "30 November 2026"]], [30 * MM, 144 * MM], cell),
         Paragraph("1. Service", h2),
         Paragraph("Pairwise reply comparisons on device troubleshooting tickets by Ardentdesk's device-support "
                   "team, on pairs Penvale supplies, under Penvale guideline v3. Agents choose one reply on every "
                   "pair; the tool does not offer 'no preference'.", body),
         Paragraph("2. Price and capacity", h2),
         _grid([["Item", "Terms"],
                ["Price", "USD 3.60 per comparison"],
                ["Capacity in Q1 2027", "120,000 comparisons, delivered 11 January to 26 March 2027"],
                ["Order size", "at least 10,000 comparisons, in steps of 1,000"],
                ["Order deadline", "30 November 2026 for Q1 2027 delivery"]], [50 * MM, 124 * MM], cell),
         Paragraph("3. Delivery", h2),
         Paragraph("Daily exports from Ardentdesk's labelling tool, in the format of the 2026 deliveries: each "
                   "record shows which reply the agent saw on the left and which side the agent chose.", body),
         Spacer(1, 6),
         Paragraph("Amanda Estrada, Client Services Manager, Ardentdesk Solutions Inc.", small)]
    created = dt.datetime(2026, 11, 6, 16, 40, tzinfo=MNL)
    O.build(path, s, "Quotation AD-Q-2611-07", "Amanda Estrada", "Ardentdesk quotation for Q1 2027",
            "Ardentdesk Solutions Inc.  |  AD-Q-2611-07", created, created + dt.timedelta(minutes=18),
            page_of=True)
    return created + dt.timedelta(minutes=18)


def quality_report(path, rows):
    """Tallyfield's account quality summary: its gold-question accuracy by month (its own monitoring)"""
    body, h1, h2, cell, small = _styles()
    tab = [["Month", "Comparisons completed", "Active workers", "Gold-question accuracy", "Median minutes to deliver"]]
    for r in rows:
        tab.append([r["month"], "{:,}".format(r["completed"]), str(r["workers"]), "%.1f%%" % r["gold"],
                    "%.0f" % r["turnaround"]])
    s = [Paragraph("Account quality summary: Penvale Electronics, 2026", h1),
         _grid([["Account", "Penvale Electronics Ltd (PEN-0412)"], ["Prepared by", "Emily Dickson, Tallyfield Inc."],
                ["Period", "January to September 2026"], ["Issued", "9 October 2026"]], [36 * MM, 138 * MM], cell),
         Paragraph("1. Volume and workforce", h2),
         Paragraph("Comparisons completed include 'no preference' judgments. Active workers are those who "
                   "completed at least one comparison in the month.", body),
         _grid(tab, [26 * MM, 38 * MM, 30 * MM, 38 * MM, 42 * MM], cell),
         Paragraph("2. Gold questions", h2),
         Paragraph("Tallyfield seeds each worker's queue with gold questions from its own bank of reply pairs whose "
                   "answer its quality team has fixed. Gold-question accuracy is the share of gold questions "
                   "answered as the bank records. Workers below 80 per cent over their last 50 gold questions are "
                   "removed from the account.", body),
         Paragraph("Penvale's guideline v3 replaced guideline v2 for all Penvale work from 5 January 2026; every "
                   "worker on the account re-qualified on the v3 test before that date.", body),
         Paragraph("3. Platform", h2),
         Paragraph("Tallyfield moved Penvale's account to its new task platform in June 2026. Batches TF26-022 to "
                   "TF26-024 were exported again after the move; the second exports repeat the first.", body),
         Spacer(1, 6),
         Paragraph("Tallyfield Inc. | quality@tallyfield.io", small)]
    created = dt.datetime(2026, 10, 9, 11, 25, tzinfo=dt.timezone(dt.timedelta(hours=-7)))
    O.build(path, s, "Account quality summary 2026", "Emily Dickson", "Penvale Electronics quality summary",
            "Tallyfield Inc.  |  PEN-0412", created, created + dt.timedelta(minutes=12), page_of=True)
    return created + dt.timedelta(minutes=12)
