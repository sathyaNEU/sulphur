"""task19: the Local Government Grants Commission's circular on the population basis of the 2027/28 grant
determination (a Word document exported to PDF by LibreOffice Writer, dated to its issue)."""
import datetime as dt

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf
import params as PR

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.6, spaceAfter=5, leading=12.8)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.4, spaceAfter=0, leading=10.4)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", parent=SS["Heading1"], fontSize=15, spaceAfter=4)
LH = ParagraphStyle("lh", parent=BODY, fontSize=8, leading=10, textColor="#444444")

DUBLIN = dt.timezone(dt.timedelta(hours=1))
ISSUED = dt.datetime(2026, 9, 2, 9, 40, 12, tzinfo=DUBLIN)
SAVED = dt.datetime(2026, 9, 2, 11, 6, 51, tzinfo=DUBLIN)

# the filed sentences the estimates and the call rest on, numbered as the circular numbers them
PARA = {
    "2.1": "The population basis of the 2027/28 determination is the number of usual residents of each district on "
           "30 June 2026, as estimated by the Kilvarra Statistics Office. No census has been taken since March 2021, and "
           "the Office will supply its estimates, each with a 90 per cent interval, by 4 December 2026.",
    "2.2": "A usual resident is a person who on 30 June 2026 had lived in Kilvarra for at least twelve months, or had "
           "arrived intending to stay for at least twelve months, counted in the district of the address where they "
           "spend most of their time. Students in full-time education are counted at their term-time address, and "
           "serving members of the Defence Forces at the base where they are stationed.",
    "2.3": "District boundaries are those in force on 30 June 2026, and an address belongs to the district that the "
           "Office's postcode directory assigns to its postcode.",
    "3.1": "Each district with 25,000 usual residents or more receives the urban-services supplement for 2027/28, worth "
           "1.2 per cent of the grant pool, in addition to its share of the pool in proportion to its usual residents.",
    "3.2": "Where the Office's 90 per cent interval for a district lies wholly at or above 25,000, the district "
           "qualifies. Where the interval includes 25,000, the Commission treats the district's eligibility as "
           "unconfirmed and pays half the supplement for 2027/28, settling the balance on the Office's mid-2027 "
           "estimates. Where the interval lies wholly below 25,000, the district does not qualify.",
}


def P(t, st=BODY):
    return Paragraph(t, st)


def write(path):
    rows = [[P(x, CELL) for x in r] for r in [
        ["Date", "Step"],
        ["2 September 2026", "This circular issued to the twelve district councils and the Statistics Office"],
        ["4 December 2026", "The Office's mid-2026 district estimates of usual residents, with 90 per cent intervals"],
        ["29 January 2027", "Provisional determination published; councils' representations close 26 February"],
        ["26 March 2027", "Final determination"],
    ]]
    story = [
        P("<b>LOCAL GOVERNMENT GRANTS COMMISSION</b>  |  Kilvarra", LH),
        P("Commission House, 3 Quay Street, Port Ardain PA1 2QD", LH),
        Spacer(1, 8),
        P("Grant determination 2027/28: the population basis", TITLE),
        P("Circular LGGC 2026/14. Issued 2 September 2026 to the chief executives of the district councils and the "
          "Director General of the Kilvarra Statistics Office."),
        P("1. Purpose", H2),
        P("This circular sets out the population figures on which the Commission will make the 2027/28 grant "
          "determination, and how the urban-services supplement will be decided. The grant pool for 2027/28 will be "
          "announced with the provisional determination."),
        P("2. The population basis", H2),
    ]
    heads = {"2.1": "Figures used", "2.2": "Usual residents", "2.3": "Districts"}
    for k in ("2.1", "2.2", "2.3"):
        story.append(P("<b>%s %s.</b> %s" % (k, heads[k], PARA[k])))
    story += [P("3. The urban-services supplement", H2)]
    heads = {"3.1": "Eligibility", "3.2": "Districts near the threshold"}
    for k in ("3.1", "3.2"):
        story.append(P("<b>%s %s.</b> %s" % (k, heads[k], PARA[k])))
    story += [
        P("4. Timetable", H2),
        Table(rows, colWidths=[38 * 72 / 25.4, 128 * 72 / 25.4]),
        Spacer(1, 8),
        P("Enquiries to the Secretary to the Commission, Carla McCaffrey, at the address above.", BODY),
    ]
    officepdf.build(path, story, title="Grant determination 2027/28: the population basis",
                    author="Local Government Grants Commission", subject="Circular LGGC 2026/14",
                    footer="LGGC 2026/14", created=ISSUED, modified=SAVED)
