"""task3 documents: the utility's tidal low point inventory (an Excel export of its asset register) and the FY2028
tide valve round's guidelines (a Word document exported to PDF by LibreOffice Writer)."""
import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import world as W

EDT = dt.timezone(dt.timedelta(hours=-4))
EST = dt.timezone(dt.timedelta(hours=-5))
PLANNING_MSL = 0.70  # ft above the gauge's 1983-2001 mean sea level, tide year 2027-28
HARBOR_MINOR = 8.6  # ft MLLW
ROUND_N = 2
IDS = {"front": "LP-01", "marsh": "LP-02", "river": "LP-03", "wharf": "LP-04", "oyster": "LP-05"}
RIM_BELOW = {"front": 0.33, "marsh": 0.26, "river": 0.27, "wharf": 0.27, "oyster": 0.24}
PLATFORM = {"marsh": 4.29, "oyster": 3.93}  # marsh platform, ft NAVD88 (2019 LiDAR, median of marsh cells)


def nav(level_mllw):
    return level_mllw + W.NAVD88_OF_MLLW


def lane_navd88(site):
    return round(nav(W.SITES[site]["level"]), 2)


def rim_navd88(site):
    return round(nav(W.SITES[site]["level"] - RIM_BELOW[site]), 2)


def inventory(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Low points"
    hdr = ["LP ID", "Low point", "Latitude", "Longitude", "Catchment", "Outfall ID", "Receiving water", "Outfall flap gate",
           "Lowest inlet rim (ft NAVD88)", "Travel lane low point (ft NAVD88)", "Lane survey", "Street sensor", "Notes"]
    rows = [
        ["LP-01", W.SITES["front"]["name"], 31.40418, -81.30122, "Ferry Lane", "OF-112", "Brayle River (harbor)", "None (removed 2017)",
         rim_navd88("front"), None, "", "PT-FRONT-01 (May 2024)", "Lane not surveyed; sensor over the travel lane at the sag"],
        ["LP-02", W.SITES["marsh"]["name"], 31.42177, -81.33860, "Pellam Creek west", "OF-207", "Pellam Creek", "Failed (2019 inspection)",
         rim_navd88("marsh"), lane_navd88("marsh"), "RTK, 2023-06-21", "", "Logger campaign Sep-Nov 2024"],
        ["LP-03", W.SITES["river"]["name"], 31.47902, -81.37415, "Hensley", "OF-318", "Brayle River", "None",
         rim_navd88("river"), lane_navd88("river"), "RTK, 2023-06-22", "", "Logger campaign Jan-Apr 2025"],
        ["LP-04", W.SITES["wharf"]["name"], 31.40266, -81.29874, "Market Lane", "OF-104", "Brayle River (harbor)", "Missing",
         rim_navd88("wharf"), lane_navd88("wharf"), "RTK, 2023-06-21", "", ""],
        ["LP-05", W.SITES["oyster"]["name"], 31.43711, -81.31452, "Oyster Creek", "OF-221", "Oyster Creek", "Failed (2021 inspection)",
         rim_navd88("oyster"), lane_navd88("oyster"), "RTK, 2023-06-23", "", "Logger campaign Aug-Oct 2025"],
    ]
    ws.append(hdr)
    for r in rows:
        ws.append(r)
    ws2 = wb.create_sheet("Tidal creeks")
    ws2.append(["Creek", "Reach", "Low points draining to it", "Channel invert at outfall (ft NAVD88)",
                "Marsh platform (ft NAVD88, 2019 LiDAR median)", "Marsh area (acres)", "Notes"])
    ws2.append(["Pellam Creek", "Marsh Rd bridge to mouth", "LP-02", -3.9, PLATFORM["marsh"], 412, "Spartina marsh both banks"])
    ws2.append(["Oyster Creek", "Culvert to Brayle confluence", "LP-05", -3.1, PLATFORM["oyster"], 268, "Marsh east bank, bluff west"])
    ws2.append(["Brayle River", "Hensley Landing reach", "LP-03", -11.5, None, None, "Forested banks; no marsh in reach"])
    ws2.append(["Brayle River", "Harbor (entrance)", "LP-01, LP-04", -24.0, None, None, "Bulkheaded waterfront"])
    ws3 = wb.create_sheet("Logger campaigns")
    ws3.append(["Site", "Logger S/N", "Deployed (local)", "Retrieved (local)", "Sensor elevation (ft NAVD88, RTK)",
                "Staff check at deployment (logger minus staff, ft)", "Staff check at retrieval (logger minus staff, ft)",
                "Interval", "Notes"])
    ws3.append(["LP-02 Marsh Road at Pellam Creek", "21187431", "2024-09-15 11:00", "2024-11-21 10:00", -1.35, 0.01, -0.01, "15 min",
                "Sensor in creek channel 40 ft below outfall; dry at low water"])
    ws3.append(["LP-05 Oyster Creek Road", "21187433", "2025-08-25 10:00", "2025-10-30 15:00", -1.10, 0.00, 0.02, "15 min",
                "Sensor on culvert headwall"])
    ws3.append(["LP-03 River Road at Hensley Landing", "21187432", "2025-01-20 12:00", "2025-04-20 09:00", -4.80, 0.01, 0.02, "15 min",
                "Sensor on boat ramp piling; river high at deployment"])
    for sh in (ws, ws2, ws3):
        for c in sh[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DDE4EE")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        sh.freeze_panes = "A2"
        for col in sh.columns:
            w = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            sh.column_dimensions[col[0].column_letter].width = min(max(10, w * 0.9), 44)
    wb.save(path)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=10.6)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def guidelines(path):
    body, h1, h2, small, cell = _styles()
    lp = [["ID", "Low point", "Outfall"]] + [[IDS[k], W.SITES[k]["name"], o] for k, o in
                                              (("front", "OF-112"), ("marsh", "OF-207"), ("river", "OF-318"),
                                               ("wharf", "OF-104"), ("oyster", "OF-221"))]
    s = [Paragraph("Port Tolliver Stormwater Utility", small),
         Paragraph("Tidal Backflow Prevention Program: FY2028 valve round", h1),
         Paragraph("Round guidelines, issued 16 October 2026. Approved by the Stormwater Advisory Board on 8 October 2026.", small),
         Spacer(1, 6),
         Paragraph("1. Purpose", h2),
         Paragraph("The FY2028 capital budget funds inline check valves at the outfalls of %s tidal low points, installed "
                   "before 1 May 2027. A valve stops tidewater backing up the outfall pipe into the street. This round "
                   "chooses which low points receive them." % ("two" if ROUND_N == 2 else str(ROUND_N)), body),
         Paragraph("2. Low points in the round", h2),
         _grid(lp, [40, 230, 70], cell),
         Spacer(1, 4),
         Paragraph("3. Ranking", h2),
         Paragraph("The low points are ranked on their expected tidal flood days in the 2027-28 tide year. The two with "
                   "the most receive valves in FY2028; the others are carried to the FY2029 round.", body),
         Paragraph("4. Definitions", h2),
         Paragraph("<b>Tide year.</b> 1 May to 30 April. The 2027-28 tide year runs from 1 May 2027 to 30 April 2028.", body),
         Paragraph("<b>Tidal flood day.</b> A calendar day, in Eastern Standard Time, on which the tide brings the water "
                   "at the low point itself, at its outfall, to or above its flooding elevation. Rain alone does not make a "
                   "tidal flood day.", body),
         Paragraph("<b>Flooding elevation.</b> The elevation of the travel lane's low point, in feet NAVD88, as surveyed "
                   "for the utility's low point inventory. Where the lane has not been surveyed, it is the water level at "
                   "which the utility's street sensor over the travel lane records water on the lane.", body),
         Paragraph("<b>Expected tidal flood days.</b> A low point's average number of tidal flood days in the tide year "
                   "over the weather and river flows of the tide years 1990-91 to 2025-26, with the tide year's astronomical "
                   "tide taken from the published predictions of the Port Tolliver harbor gauge (NOAA station %s) and the "
                   "gauge's mean sea level for the tide year at the program's planning value. The 90 per cent range is the "
                   "range the tide year's count falls within in nine of every ten of those weather years." % "8673718", body),
         Paragraph("<b>Planning mean sea level.</b> For the 2027-28 tide year the program plans on the harbor gauge's mean "
                   "sea level standing %.2f ft above its 1983-2001 mean sea level, the value of the regional sea level "
                   "outlook the utility adopted on 14 October 2026." % PLANNING_MSL, body),
         Paragraph("<b>Harbor gauge flood threshold.</b> The harbor gauge's minor flood threshold is %.1f ft above MLLW; "
                   "the utility reports the gauge's days at that threshold beside the low points' each round." % HARBOR_MINOR, body),
         Spacer(1, 6),
         Paragraph("Contact: Capital Program, Port Tolliver Stormwater Utility.", small)]
    O.build(path, s, "Tidal Backflow Prevention Program: FY2028 valve round", "Port Tolliver Stormwater Utility",
            "FY2028 tide valve round guidelines", "Port Tolliver Stormwater Utility, FY2028 tide valve round guidelines",
            dt.datetime(2026, 10, 16, 9, 14, 37, tzinfo=EDT), dt.datetime(2026, 10, 16, 9, 14, 37, tzinfo=EDT))
