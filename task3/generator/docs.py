"""task3 architecture 3: the pack's documents. The district's Rule WR-4, Harlow Springs Utilities' application
summary and the drillers' logs, each written as a Word document and exported to PDF by LibreOffice Writer
(officepdf), with the issuing body as author and the document's own dates."""
import datetime as dt

import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

import officepdf as O
import pack as K
import params as P

reportlab.rl_config.invariant = 1
EST = dt.timezone(dt.timedelta(hours=-5))
EDT = dt.timezone(dt.timedelta(hours=-4))
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.8, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.0, leading=10.2, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=8.4, leading=10.4, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")
DISTRICT = "Corrin Valley Water Conservancy District"
UTILITY = "Harlow Springs Utilities"


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(rows, widths):
    data = [[Paragraph(_esc(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


RULE_SENTINELS = [("North reach", "OW-N", "Corrin Valley aquifer, Brennan Road to the county line", "6.0"),
                  ("Harlow reach", "OW-S", "Corrin Valley aquifer, Brennan Road to the Little Ossey confluence",
                   "%.1f" % P.LIMIT),
                  ("Ossey reach", "OW-E", "Little Ossey tributary valley aquifer", "7.5")]


def rule_wr4(path):
    s = [Paragraph("Rule WR-4: Groundwater Withdrawal Permits", H1),
         Paragraph("Corrin Valley Water Conservancy District. Adopted by the Board of Directors 12 March 2019 under "
                   "the District's plan for the Corrin Valley aquifer; amended 14 June 2023 (Table 1).", SMALL),
         Spacer(1, 4),
         Paragraph("1. Scope", H2),
         Paragraph("1.1 This rule applies to any new or increased withdrawal of groundwater from the Corrin Valley "
                   "aquifer or a tributary valley aquifer within the District at a facility capable of withdrawing "
                   "100,000 gallons or more in a day.", BODY),
         Paragraph("1.2 A permit issued under this rule is for a term of twenty years ending on 31 December of the "
                   "twentieth calendar year after the year the application is filed.", BODY),
         Paragraph("2. Definitions", H2),
         Paragraph("2.1 <b>Drawdown</b> means the lowering of the potentiometric surface of the aquifer caused by "
                   "withdrawals.", BODY),
         Paragraph("2.2 <b>Existing permitted withdrawal</b> means a withdrawal from the same aquifer authorised by a "
                   "District permit or registration on the date an application is filed, at the rates the holder's "
                   "most recent filed projection gives for each year of the new permit's term.", BODY),
         Paragraph("2.3 <b>Sentinel well</b> means a District monitoring well listed in Table 1 for an aquifer reach. "
                   "The limit in Table 1 protects the domestic and farm wells of that reach.", BODY),
         Paragraph("2.4 <b>Requested schedule</b> means the monthly withdrawal an applicant proposes for each month of "
                   "the permit term.", BODY),
         Paragraph("3. Application", H2),
         Paragraph("3.1 An application shall include: (a) the requested schedule, or up to four alternative "
                   "requested schedules, at the proposed facility; (b) a constant-rate aquifer test of at least 72 "
                   "hours at a proposed production well, with observation wells, and the test's records; (c) the "
                   "applicant's records of its existing withdrawals and of water levels in its own monitoring wells "
                   "in the same reach; and (d) the demonstration required by section 4.", BODY),
         Paragraph("3.2 The District's network water-level records and well register are provided to applicants on "
                   "request.", BODY),
         Paragraph("4. Demonstration", H2),
         Paragraph("4.1 The applicant shall demonstrate that, under the requested schedule, the drawdown at the "
                   "sentinel well of the reach, from the proposed withdrawal together with all existing permitted "
                   "withdrawals in the reach, will not exceed the limit in Table 1 in any month of the permit term.",
                   BODY),
         Paragraph("4.2 Where an application carries alternative requested schedules, the demonstration is made for "
                   "each alternative, and the District will permit the largest alternative that meets 4.1.", BODY),
         Paragraph("4.3 The demonstration states, for each alternative, the greatest monthly drawdown at the "
                   "sentinel well in the final year of the permit term.", BODY),
         Paragraph("4.4 For the alternative the District will permit, the demonstration also states the greatest "
                   "monthly drawdown in the final year of the term at the registered domestic well nearest the "
                   "proposed facility.", BODY),
         Paragraph("5. Conditions", H2),
         Paragraph("5.1 A permit holder reports monthly withdrawals by source to the District each quarter and "
                   "measures each of its monitoring wells at least monthly.", BODY),
         Paragraph("5.2 The District may require a permit holder to reduce a withdrawal where the drawdown at a "
                   "sentinel well exceeds the limit in Table 1.", BODY),
         Spacer(1, 4),
         Paragraph("Table 1. Sentinel wells and drawdown limits (amended 14 June 2023)", CELLB),
         _table([["Reach", "Sentinel well", "Aquifer", "Limit (ft)"]] + [list(r) for r in RULE_SENTINELS],
                [26, 24, 92, 22])]
    O.build(path, s, "Rule WR-4: Groundwater Withdrawal Permits", DISTRICT,
            "Rule WR-4, groundwater withdrawal permits, as amended 14 June 2023", "CVWCD Rule WR-4",
            dt.datetime(2023, 6, 14, 10, 5, tzinfo=EDT), dt.datetime(2023, 6, 20, 15, 31, tzinfo=EDT))


def application_summary(path):
    rates = P.OPTIONS
    s = [Paragraph("Reidel Road Well Field: Withdrawal Permit Application, Requested Schedules", H1),
         Paragraph("Harlow Springs Utilities, Water Division. For filing with the Corrin Valley Water Conservancy "
                   "District under Rule WR-4. Draft for the Utilities Board, 30 October 2026.", SMALL),
         Spacer(1, 4),
         Paragraph("1. The facility", H2),
         Paragraph("The Reidel Road well field is two production wells, PW-1 and PW-2, 410 ft apart in the Corrin "
                   "Valley aquifer, completed in June 2026. Each alternative below is shared equally by the two wells. "
                   "Withdrawals would begin in April 2027, when the Reidel Road treatment plant and the Kestrel Foods "
                   "connection are commissioned.", BODY),
         Paragraph("2. Alternative requested schedules", H2),
         Paragraph("The Board has asked for four alternatives at annual average rates of %s gpm. In each month the "
                   "rate is the annual average times the month's factor below, the factors following the plant's "
                   "summer process load and the city's irrigation peak." % ", ".join("{:,}".format(r) for r in rates),
                   BODY),
         _table([["Alternative", "Annual average (gpm)", "Annual average (MGD)"]] +
                [[chr(65 + k), "{:,}".format(r), "%.2f" % (r * 1440 / 1e6)] for k, r in enumerate(rates)],
                [30, 44, 44]),
         Spacer(1, 4),
         _table([["Month"] + [dt.date(2027, m, 1).strftime("%b") for m in range(1, 13)],
                 ["Factor"] + ["%.2f" % f for f in P.NEW_SEASON]], [18] + [12.5] * 12),
         Paragraph("3. The Mill Street wells", H2),
         Paragraph("The city's existing supply is the Mill Street well field (TW-1, in service March 2009; TW-2, in "
                   "service June 2014), registered with the District as an existing permitted withdrawal. The "
                   "projection below is the one filed with the District in the 2026 water supply plan update; TW-1 "
                   "carries 56 per cent of each month's withdrawal and TW-2 44 per cent. Monthly withdrawals are the "
                   "annual average times the Mill Street monthly factors.", BODY),
         _table([["Year", "Annual average (gpm)"]] +
                [[str(y), "%.0f" % (P.TOWN_PROJ_BASE * (1 + P.TOWN_PROJ_GROWTH) ** (y - 2026))]
                 for y in (2026, 2027, 2030, 2035, 2040, 2046)], [30, 44]),
         Paragraph("Annual averages between the years shown grow at %.1f per cent a year from 2026." %
                   (P.TOWN_PROJ_GROWTH * 100), SMALL),
         _table([["Month"] + [dt.date(2027, m, 1).strftime("%b") for m in range(1, 13)],
                 ["Factor"] + ["%.2f" % f for f in P.TOWN_MONTH_FACTORS]], [18] + [12.5] * 12),
         Paragraph("4. Supporting records", H2),
         Paragraph("The 72-hour constant-rate test of PW-1 was run from 09:00 on 14 September to 09:00 on 17 September "
                   "2026 by Tillbrook Hydrogeologic, with PW-2, OW-1, OW-2, OW-3 and the District's sentinel well "
                   "OW-S logged; the logger export, the barologger record and the field notes accompany this summary, "
                   "with the August step test of PW-1. The Mill Street wells' monthly production and the Mill Street "
                   "monitoring well's readings are from the Water Division's monthly operating reports. The District "
                   "supplied its network water levels and well register on 2 October 2026.", BODY),
         Paragraph("5. Wells of the Reidel Road field", H2),
         _table([["Well", "Purpose", "Screen (ft bgs)", "Distance to PW-1 (ft, taped)"],
                 ["PW-1", "production", "95 to 135", "0"],
                 ["PW-2", "production", "93 to 133", "410"],
                 ["OW-1", "observation", "108 to 118", "150"],
                 ["OW-2", "observation", "102 to 112", "620"],
                 ["OW-3", "observation", "105 to 115", "1,450"]], [18, 30, 30, 50])]
    O.build(path, s, "Reidel Road Well Field: Withdrawal Permit Application, Requested Schedules", UTILITY,
            "Reidel Road well field, WR-4 application, requested schedules", "Harlow Springs Utilities, Water Division",
            dt.datetime(2026, 10, 30, 11, 20, tzinfo=EDT), dt.datetime(2026, 10, 30, 16, 2, tzinfo=EDT))


LOGS = [
    ("PW-1", "2026-06-11", "Hoosier Rotary Drilling", [(0, 2, "topsoil, black, organic"),
     (2, 49, "clay, gray, silty, stiff, with scattered pebbles (till)"), (49, 53, "silt and fine sand, gray, wet"),
     (53, 141, "sand and gravel, brown to gray, medium to coarse, clean, water-bearing"),
     (141, 146, "shale, black, fissile (New Albany)")]),
    ("OW-3", "2026-07-16", "Hoosier Rotary Drilling", [(0, 3, "topsoil"), (3, 51, "clay, gray, silty, pebbly (till)"),
     (51, 139, "sand and gravel, coarse, some cobbles"), (139, 142, "shale, black")]),
    ("OW-S", "2004-09-21", "Wabash Test Drilling", [(0, 2, "fill and topsoil"), (2, 47, "clay, gray-brown, pebbly (till)"),
     (47, 52, "sand, fine, silty"), (52, 136, "sand and gravel, gray, medium to coarse"), (136, 138, "shale")]),
    ("TW-1", "2008-05-20", "Wabash Test Drilling", [(0, 4, "topsoil and fill"), (4, 55, "clay, gray, stiff, pebbly (till)"),
     (55, 139, "sand and gravel, coarse, water-bearing"), (139, 143, "shale, black")]),
    ("CV-07", "2004-10-05", "Wabash Test Drilling", [(0, 3, "topsoil"), (3, 50, "clay, silty, gray (till)"),
     (50, 131, "sand and gravel"), (131, 133, "shale")]),
    ("CV-02", "2004-08-17", "Wabash Test Drilling", [(0, 5, "topsoil, sandy"), (5, 61, "clay, gray-brown (till)"),
     (61, 150, "sand and gravel, medium"), (150, 152, "shale, gray")]),
    ("CV-11", "2004-11-03", "Wabash Test Drilling", [(0, 2, "topsoil"), (2, 38, "clay, gray (till), sand lens 21 to 24"),
     (38, 112, "sand and gravel"), (112, 115, "shale")]),
    ("CV-04", "2004-10-06", "Wabash Test Drilling", [(0, 1, "topsoil"), (1, 27, "sand, fine to medium, brown (outwash)"),
     (27, 32, "clay, gray (till)")]),
    ("CV-13", "2006-03-15", "Hoosier Rotary Drilling", [(0, 6, "clay, brown"), (6, 31, "clay, gray (till)"),
     (31, 230, "shale, black to gray, fractured 160 to 205")]),
]


def drillers_logs(path):
    s = [Paragraph("Drillers' Logs, Corrin Valley Wells (selected)", H1),
         Paragraph("Compiled from the well records filed with the District. Depths in feet below ground surface.",
                   SMALL), Spacer(1, 4)]
    for k, (w, date, driller, rows) in enumerate(LOGS):
        s.append(Paragraph("%s: completed %s, %s" % (w, date, driller), H2))
        s.append(_table([["From (ft)", "To (ft)", "Description"]] + [[str(a), str(b), d] for a, b, d in rows],
                        [20, 20, 120]))
        if k in (3,):
            s.append(PageBreak())
    O.build(path, s, "Drillers' Logs, Corrin Valley Wells", DISTRICT, "Drillers' logs, Corrin Valley wells (selected)",
            "CVWCD well records", dt.datetime(2026, 10, 2, 9, 12, tzinfo=EDT), dt.datetime(2026, 10, 2, 9, 40, tzinfo=EDT))
