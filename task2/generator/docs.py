"""task2 architecture 4: the pack's documents. The ore purchase agreement's term sheet and the 2027 mine plan
summary, each written as a Word document and exported to PDF by LibreOffice Writer (officepdf)."""
import datetime as dt

import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

reportlab.rl_config.invariant = 1
AWST = dt.timezone(dt.timedelta(hours=8))
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.8, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.0, leading=10.2, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=8.4, leading=10.4, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333"))]))
    return t


def term_sheet(path):
    tiers = P.TIERS
    s = [Paragraph("Yarrabin Ore Purchase Agreement 2027 to 2028: Term Sheet", H1),
         Paragraph("Between Tallowood Processing Pty Ltd (Yarrabin mill) and Ironbark Gold Ltd (Mount Carrow). "
                   "Non-binding except clauses 6 and 7. Revision 3, 22 October 2026.", SMALL),
         Spacer(1, 4),
         Paragraph("1. Ore", H2),
         Paragraph("1.1 Ore is material from the Mount Carrow Stage 5 cutback delivered to the Yarrabin run-of-mine pad in "
                   "the 2027 and 2028 calendar years.", BODY),
         Paragraph("1.2 Ore is selected and dispatched in mining blocks of 5 m by 5 m in plan by one 2.5 m flitch. A "
                   "block is ore when its gold grade is %.1f g/t or more; the contained gold of a block is its dry "
                   "tonnes times its grade." % P.CUT, BODY),
         Paragraph("2. Delivery commitment", H2),
         Paragraph("2.1 Ironbark commits to one delivery tier, stated as the contained gold of the ore it will deliver "
                   "over the term. The tiers are:", BODY),
         _table([["Tier", "Contained gold committed (oz)", "Treatment charge (AUD/t)"]] +
                [[t, "{:,}".format(v * 1000), "%d" % c] for (t, v), c in zip(tiers, (58, 54, 49))], [20, 60, 50]),
         Spacer(1, 4),
         Paragraph("2.2 Ironbark will deliver all ore Stage 5 yields over the term; a tier is the floor of the "
                   "commitment, not a cap.", BODY),
         Paragraph("3. Grade and weight", H2),
         Paragraph("3.1 Delivered ore is weighed over the Yarrabin weighbridge and sampled by Tallowood; payable gold "
                   "follows the mill's metallurgical balance.", BODY),
         Paragraph("4. Delivery", H2),
         Paragraph("4.1 Ironbark hauls ore to the Yarrabin run-of-mine pad at its own cost, at not less than 40,000 "
                   "dry tonnes in any calendar month from June 2027, with a fortnight's notice of the next month's "
                   "tonnes.", BODY),
         Paragraph("5. Title and risk", H2),
         Paragraph("5.1 Title and risk in delivered ore pass to Tallowood when the ore crosses the Yarrabin "
                   "weighbridge.", BODY),
         Paragraph("6. Shortfall", H2),
         Paragraph("6.1 If the contained gold delivered over the term falls short of the committed tier, Ironbark pays "
                   "Tallowood AUD 145 for each ounce short.", BODY),
         Paragraph("7. Election", H2),
         Paragraph("7.1 Ironbark elects its tier in writing by 15 December 2026.", BODY)]
    O.build(path, s, "Yarrabin Ore Purchase Agreement: Term Sheet", "Tallowood Processing Pty Ltd",
            "Yarrabin OPA 2027-2028 term sheet, revision 3", "Tallowood Processing Pty Ltd, commercial",
            dt.datetime(2026, 10, 22, 10, 15, tzinfo=AWST), dt.datetime(2026, 10, 22, 16, 48, tzinfo=AWST))


def plan_summary(path, n_holes):
    s = [Paragraph("Mount Carrow 2027 Mine Plan: Summary for the Board", H1),
         Paragraph("Ironbark Gold Ltd, Mount Carrow operations. 3 November 2026.", SMALL),
         Spacer(1, 4),
         Paragraph("Stage 5", H2),
         Paragraph("Stage 5 is the east cutback of the Mount Carrow pit, mined from RL 400 to RL 305 in 2.5 m flitches "
                   "over 2027 and 2028. The design's flitch outlines are in the Stage 5 design file on the mine grid.",
                   BODY),
         Paragraph("Fleet", H2),
         Paragraph("The 120 t excavator arriving in January 2027 digs Stage 5 selectively on 5 m by 5 m blocks within "
                   "each 2.5 m flitch, the block the ore purchase agreement measures ore by. Grade control blastholes "
                   "classify each block before it is dug.", BODY),
         Paragraph("Data", H2),
         Paragraph("The Stage 5 drilling is %d vertical holes: the 2019 to 2021 reverse circulation programme on a 25 m "
                   "grid and the 2022 to 2024 reverse circulation and diamond infill at 12.5 m. Collars before 2022 are on "
                   "the mine grid; from 2022 the database stores MGA94 zone 51, and the mine grid is MGA94 zone 51 less "
                   "339,250.0 m east and 6,601,480.0 m north. Assays are 1 m reverse circulation samples and diamond "
                   "core intervals of 0.5 to 1.5 m, by fire assay at Goldfields Assay Laboratories to 2022 and Boulder "
                   "Analytical from 2023, with the QAQC results in their own file. Dry bulk densities are from diamond "
                   "core by weathering zone." % n_holes, BODY),
         Paragraph("Schedule", H2),
         Paragraph("Pre-strip from February 2027; first Stage 5 ore to the Yarrabin pad in May 2027; Stage 5 complete in "
                   "December 2028.", BODY)]
    O.build(path, s, "Mount Carrow 2027 Mine Plan: Summary for the Board", "Ironbark Gold Ltd",
            "Mount Carrow 2027 mine plan summary", "Ironbark Gold Ltd, Mount Carrow",
            dt.datetime(2026, 11, 3, 9, 30, tzinfo=AWST), dt.datetime(2026, 11, 3, 14, 12, tzinfo=AWST))
