"""task14: the Statistics Office's definition paper for the private rents measure, issued by its Methods Board (a Word
document exported to PDF by LibreOffice, dated to its approval)."""
import datetime as dt

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.6, spaceAfter=5, leading=12.8)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8, spaceAfter=2)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.2, spaceAfter=0, leading=10)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", parent=SS["Heading1"], fontSize=15, spaceAfter=4)
LH = ParagraphStyle("lh", parent=BODY, fontSize=8, leading=10, textColor="#444444")

# the definitions the measure rests on, numbered as the paper numbers them (checks.py and verify.py read them back)
DEFS = {
    "2.1": "A dwelling is the unit a bond is lodged for: a house, a townhouse or unit, a flat or apartment, or a room let "
           "under its own tenancy agreement.",
    "2.2": "A tenancy is a private residential tenancy whose bond the Tenancy Bond Board holds or has held. It covers each "
           "day from its start date up to the day before its bond is refunded, or up to the day before the next tenancy at "
           "the same dwelling starts if that is earlier. A dwelling is let on a day when a tenancy covers that day; where two "
           "tenancies would cover the same day, the later one is the tenancy in place.",
    "2.3": "The rent payable on a day is the rent the tenant is liable to pay under the tenancy agreement as it stands on "
           "that day, expressed as a weekly amount: a fortnightly rent is halved, and a calendar-monthly rent is multiplied "
           "by twelve and divided by fifty-two.",
    "2.4": "For a quarter, the measure compares the dwellings let on the last day of the quarter that were also let on the "
           "last day of the same quarter a year earlier. It is the total weekly rent payable on those dwellings on the later "
           "day, divided by the total weekly rent payable on the same dwellings on the earlier day, less one, expressed as a "
           "percentage. A dwelling let under different tenancies on the two days enters at each tenancy's rent payable on "
           "its own day.",
    "2.5": "With each quarter's measure the Office publishes the same comparison for the dwellings let under the same "
           "tenancy on both days and for the dwellings let under different tenancies on the two days (dwellings re-let), "
           "each computed in the same way over its own dwellings, with the number of dwellings in each.",
    "2.6": "The measure is published for Penmarra and for each of the seven regions in use from 1 July 2024. A dwelling "
           "belongs to the region of its suburb as the Office's concordance places it, for every quarter including those "
           "before July 2024. The figure for Penmarra covers every dwelling in the comparison.",
    "2.7": "Tenancies let without a bond lodged with the Board are outside the measure.",
}


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths_mm):
    return Table([[P(c, CELL) if isinstance(c, str) else c for c in r] for r in rows],
                 colWidths=[w * 72 / 25.4 for w in widths_mm])


def aware(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def write_method(path):
    story = [
        P("<b>PENMARRA STATISTICS OFFICE</b>  |  Prices Statistics", LH),
        P("Customhouse Chambers, 22 Albert Street, Port Hallam", LH),
        Spacer(1, 8),
        P("Private rents measure: definition and scope", TITLE),
        P("Methods paper PS-2026-07, issue 2. Approved by the Methods Board on 28 October 2026.", BODY),
        P("1. Purpose", H2),
        P("From the December 2026 quarter the Office publishes a private rents measure for Penmarra and each region, for "
          "private tenancies whose bond is lodged with the Tenancy Bond Board. It replaces the private rents index the "
          "Office has compiled from its Rent Survey since 2018, which is published for the last time for the December 2026 "
          "quarter. This paper sets out what the measure is: the dwellings, days and rents it compares."),
        P("2. Definitions", H2),
    ]
    heads = {"2.1": "Dwelling", "2.2": "Tenancy, and the days it covers", "2.3": "Rent payable", "2.4": "The measure",
             "2.5": "Breakdowns", "2.6": "Regions", "2.7": "Coverage"}
    for k in ("2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7"):
        story.append(P("<b>%s %s.</b> %s" % (k, heads[k], DEFS[k])))
    story += [
        P("3. Publication", H2),
        P("The measure is published quarterly, in the fourth week after the quarter, to one decimal place, with a 90 per "
          "cent interval on the figure for Penmarra. The December 2026 quarter is published on 27 January 2027 together "
          "with every quarter back to the March 2022 quarter."),
        P("4. Document history", H2),
        T([["Issue", "Date", "Change", "By"],
           ["1", "19/08/2026", "Draft for consultation with the Tenancy Bond Board and users", "C. Buckley"],
           ["2", "28/10/2026", "Approved; 2.2 restated for a refund still pending when the next tenancy starts",
            "C. Buckley"]], [14, 24, 104, 26]),
        Spacer(1, 6),
        P("Owner: Christine Buckley, Manager, Prices Statistics. Approved by the Methods Board.", SMALL),
    ]
    officepdf.build(path, story, "Private rents measure: definition and scope", "Prices Statistics",
                    "Methods paper PS-2026-07 issue 2", "PS-2026-07 issue 2  |  Penmarra Statistics Office",
                    aware("2026-10-28T02:41:16Z"), aware("2026-10-28T03:02:49Z"), producer="LibreOffice 7.6",
                    font="Liberation Sans", page_of=True)
