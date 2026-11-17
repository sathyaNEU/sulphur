"""The Servizio Strade Alta Ardesa's own documents: the regulation on the protection of gully crossings (exported
from a word processor through the house writer), the road stations register and the gully crossings register with
the source areas of the 2025 geotechnical survey."""
import datetime as dt
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
sys.path.insert(0, HERE)
import officepdf as O  # noqa: E402
import core as C  # noqa: E402
import world as WL  # noqa: E402

ORG = "Servizio Strade Alta Ardesa"
CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))
FILES = {
    "regulation": "regulation_gully_crossings_SP141_rev4.pdf",
    "stations": "road_stations_register.xlsx",
    "crossings": "gully_crossings_register.xlsx",
}
CROSSING_ID = {s: "GC-%04d" % int(round(km * 100)) for s, km in WL.CROSSING_KM.items()}      # by the road's chainage
# the province's inventory of source areas numbers them by sub-basin, not along the road
SOURCE_ID = {"Rio Gelt": "SA-21768", "Rio Sass": "SA-21704", "Rio Marden": "SA-21853", "Rio Ciadin": "SA-21731",
             "Rio Larin": "SA-21879", "Rio Toval": "SA-21802", "Rio Bianc": "SA-21815"}
STRUCTURE = {"Rio Gelt": ("box culvert", 3.0, 1987), "Rio Sass": ("ford with apron", 14.0, 1974),
             "Rio Marden": ("box culvert", 4.0, 1992), "Rio Ciadin": ("ford with apron", 22.0, 1968),
             "Rio Larin": ("pipe culvert, twin", 2.4, 2003), "Rio Toval": ("ford with apron", 18.0, 1971),
             "Rio Bianc": ("slab bridge", 6.5, 1998)}
# two field campaigns, the high dolomite basins in the autumn of 2024 and the rest in the summer of 2025
SURVEY = {"Rio Gelt": (11.8, 34, "talus and moraine", dt.date(2025, 6, 17)),
          "Rio Sass": (7.4, 31, "weathered flysch", dt.date(2025, 6, 19)),
          "Rio Marden": (16.3, 38, "dolomite scree", dt.date(2024, 9, 12)),
          "Rio Ciadin": (21.9, 41, "dolomite scree", dt.date(2024, 9, 25)),
          "Rio Larin": (9.6, 29, "moraine, vegetated", dt.date(2025, 7, 8)),
          "Rio Toval": (24.5, 42, "dolomite scree", dt.date(2024, 10, 3)),
          "Rio Bianc": (13.2, 36, "talus and moraine", dt.date(2025, 8, 5))}
GAUGE = {"A": ("Idromet TB-2 (200 cm2)", 0.2), "B": ("Idromet TB-1 (400 cm2)", 0.1)}
SINCE = {"Valfosca": dt.date(2008, 9, 18), "Pradalt": dt.date(2008, 9, 18), "Rio Scuro": dt.date(2008, 9, 25),
         "Malga Sora": dt.date(2008, 9, 25), "Forcella": dt.date(2008, 10, 2), "Costarossa": dt.date(2008, 10, 2)}
ACCESS = {"Valfosca": ("lay-by at km 6.4, 40 m on foot", "good"), "Pradalt": ("yard of the road depot", "good"),
          "Rio Scuro": ("forest track from km 18.0, gate key 14", "weak"),
          "Malga Sora": ("lay-by at km 21.3, 120 m on foot", "weak"),
          "Forcella": ("car park of the pass road junction", "good"),
          "Costarossa": ("service track from km 33.4, closed in winter", "none, data card")}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=12.9, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.2, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.4,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=10.3)
    return body, h1, h2, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


REGULATION = [
    ("1. Scope", [
        "1.1 This regulation sets how the gully crossings of the provincial road SP 141 dell'Alta Ardesa are classed "
        "for protection against debris flows, and what each class requires of the Service. It applies to the gully "
        "crossings entered in the gully crossings register.",
        "1.2 A crossing holds one class for a whole protection program. A program covers five warm seasons; the "
        "program now in preparation covers the warm seasons of 2027 to 2031. The classes of a program are set in "
        "the winter before its first season, on the Service's records to the close of the last warm season, and are "
        "not changed during the program.",
        "1.3 Works under a class are entered in the program's budget in the year of its first season."]),
    ("2. Definitions", [
        "2.1 The warm season runs from 1 May to 31 October of each year. A storm belongs to the day, and so to the "
        "season, in which its largest 60-minute rain depth falls.",
        "2.2 A storm at a road station is rain separated from any other rain by six hours or more without rain at "
        "that station.",
        "2.3 A triggering storm at a crossing is a storm at the crossing's governing station in which the rain at "
        "the crossing's source area reaches the crossing's triggering depth in any 60 consecutive minutes. A depth "
        "equal to the triggering depth reaches it. A storm counts once, however many times it does so.",
        "2.4 A crossing's source area, its triggering depth and its governing station are those entered in the gully "
        "crossings register. The triggering depth is a point rain depth at the source area, in millimetres in 60 "
        "minutes, taken from the geotechnical survey of the source areas."]),
    ("3. Basis of a program's classes", [
        "3.1 The triggering storms a season to expect at a crossing in a program are the mean number of triggering "
        "storms a warm season at that crossing over every complete warm season of its governing station's tip record.",
        "3.2 Where a class requires a warning system, its warning levels are set from the crossing's 60-minute rain "
        "depth reached five times a season: the greatest depth that the rain at the crossing's source area reaches, "
        "counted as in 2.3, in a mean of five or more storms a warm season over the same seasons as 3.1."]),
    ("4. Classes", [
        "4.1 Each crossing is placed in one of three classes on the triggering storms a season to expect in the "
        "program (3.1): class 3 at 3.0 or more, class 2 at 1.0 or more and under 3.0, and class 1 under 1.0.",
        [["Class", "Triggering storms a season to expect", "Protection during the program"],
         ["3", "3.0 or more", "automatic barrier with a warning system on the approach from both sides"],
         ["2", "1.0 or more and under 3.0", "seasonal patrol from 1 May to 31 October, with hand gates at the crossing"],
         ["1", "under 1.0", "warning signs on both approaches"]],
        "4.2 The classing goes to the head of the Service with, for every crossing, its class, the triggering storms "
        "a season to expect and the 60-minute rain depth of 3.2."]),
    ("5. Road stations", [
        "5.1 The road stations are in service from the opening round in the second half of April to the closing "
        "round in the first days of November. Outside those dates the gauges are covered and no record is kept.",
        "5.2 Each station is visited on a round at about the start of each month of the warm season. The station "
        "visit book is the record of the rounds and of any other visit to a station.",
        "5.3 This revision replaces revision 3 of 14 November 2021. It moves the start of the patrol season from "
        "15 May to 1 May (4.1) and adds 3.2."]),
]


def write_regulation(target):
    body, h1, h2, cell = _styles()
    title = "Regulation on the protection of gully crossings, SP 141 dell'Alta Ardesa"
    head = [["Document", "Regulation on the protection of gully crossings, SP 141 dell'Alta Ardesa, revision 4"],
            ["Issued by", "Piero Brancaccio, head of the Service"],
            ["In force from", "9 November 2026, for the 2027 to 2031 program"],
            ["Replaces", "revision 3 of 14 November 2021"]]
    story = [Paragraph(title, h1), _grid(head, [36 * 2.83, 130 * 2.83], cell), Spacer(1, 6)]
    for hd, paras in REGULATION:
        story.append(Paragraph(hd, h2))
        for p in paras:
            if isinstance(p, list):
                story.append(_grid(p, [x * 2.83 for x in (16, 54, 96)], cell))
            else:
                story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES["regulation"]), story, title=title, author="Piero Brancaccio",
            subject="Gully crossings, protection classes", footer="%s, regulation on the protection of gully crossings, rev. 4" % ORG,
            created=dt.datetime(2026, 11, 6, 11, 24, tzinfo=CET), modified=dt.datetime(2026, 11, 6, 11, 24, tzinfo=CET),
            font="Liberation Sans")


def _sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"


def write_stations(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stations"
    rows = []
    for d in WL.ORDER:
        code, km, e, n, elev, _ = WL.STATIONS[d]
        make, bucket = GAUGE[C.DEPOTS[d]["model"]]
        rows.append([code, d, km, e, n, elev, make, bucket, "none", "UTC+1 all year", "totaliser 200 cm2, dip rod 0.1 mm",
                     "optical present-weather sensor, 10 min", SINCE[d]])
    _sheet(ws, ["station", "name", "road_km", "x_etrs89_utm33n_m", "y_etrs89_utm33n_m", "elevation_m", "rain_gauge",
                "bucket_mm", "funnel_heating", "logger_clock", "storage_gauge", "weather_detector", "in_service_from"],
           rows, [9, 14, 9, 14, 14, 11, 24, 10, 14, 15, 30, 36, 15])
    for r in ws.iter_rows(min_row=2, min_col=13, max_col=13):
        r[0].number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("Access")
    _sheet(ws2, ["station", "access", "mobile_coverage", "power"],
           [[WL.STATIONS[d][0], ACCESS[d][0], ACCESS[d][1], "solar 20 W, 12 V 18 Ah" if d != "Pradalt" else "mains"] for d in WL.ORDER],
           [9, 46, 22, 24])
    wb.save(os.path.join(target, FILES["stations"]))


def write_crossings(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Crossings"
    order = sorted(C.CROSSINGS, key=lambda s: WL.CROSSING_KM[s])
    rows = []
    for s in order:
        st, span, year = STRUCTURE[s]
        rows.append([CROSSING_ID[s], s, WL.CROSSING_KM[s], st, span, year, WL.STATIONS[C.CROSSINGS[s]["depot"]][0], SOURCE_ID[s]])
    _sheet(ws, ["crossing", "gully", "road_km", "structure", "clear_width_m", "built", "governing_station", "source_area"],
           rows, [10, 13, 9, 22, 14, 8, 18, 13])
    ws2 = wb.create_sheet("Source areas")
    rows = []
    for s in sorted(order, key=lambda x: SOURCE_ID[x]):
        e, n = WL.point(s)
        area, slope, deposit, day = SURVEY[s]
        rows.append([SOURCE_ID[s], s, e, n, WL.SOURCES[s][2], area, slope, deposit, float(C.CROSSINGS[s]["T"]), day])
    _sheet(ws2, ["source_area", "gully", "x_etrs89_utm33n_m", "y_etrs89_utm33n_m", "elevation_m", "area_ha",
                 "mean_slope_deg", "deposit", "triggering_depth_point_mm_60min", "surveyed"],
           rows, [13, 13, 14, 14, 11, 9, 10, 20, 18, 12])
    for r in ws2.iter_rows(min_row=2, min_col=10, max_col=10):
        r[0].number_format = "yyyy-mm-dd"
    wb.save(os.path.join(target, FILES["crossings"]))


def write_all(target):
    write_regulation(target)
    write_stations(target)
    write_crossings(target)
