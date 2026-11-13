"""The district's own documents and workbooks: the voltage optimization program standard, the 2026 trial's protocol,
an extract of the 2025 annual report, the feeder register and the 2027 capital plan's estimates. PDFs are Word documents
exported by LibreOffice Writer through the house writer; workbooks pass through the house workbook writer."""
import datetime as dt
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as OP  # noqa: E402
import params as P  # noqa: E402

ORG = "Platte Ridge Public Power District"
CST = dt.timezone(dt.timedelta(hours=-6))
CDT = dt.timezone(dt.timedelta(hours=-5))
FILES = {
    "std": "VO-1_voltage_optimization_program_standard.pdf",
    "proto": "vo_trial_protocol_2026.pdf",
    "ar": "annual_report_2025_system_statistics.pdf",
}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=13.4, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.9, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, header_rows, sections, author, subject, footer, created, modified, widths=None, producer=None):
    body, h1, h2, small, cell = _styles()
    story = [Paragraph(title, h1), _grid(header_rows, [44 * 2.83, 118 * 2.83], cell), Spacer(1, 6)]
    for head, paras in sections:
        story.append(Paragraph(head, h2))
        for p in paras:
            if isinstance(p, list):
                n = len(p[0])
                w = widths or {2: [70, 92], 3: [54, 54, 54], 4: [40, 40, 40, 42]}[n]
                story.append(_grid(p, [x * 2.83 for x in w], cell))
            else:
                story.append(Paragraph(p, body))
    OP.build(path, story, title=title, author=author, subject=subject, footer=footer, created=created, modified=modified,
             font="Liberation Sans", producer=producer)


STANDARD = [
    ("1. Purpose", [
        "This standard sets which distribution feeders receive voltage optimization (VO) equipment in the District's "
        "capital program, and how the decision is made. It binds Distribution Engineering, System Planning and "
        "Finance."]),
    ("2. The decision", [
        "2.1 A feeder receives VO in the 2027 program when the present value of its yearly energy saving equals or "
        "exceeds its installed cost in the 2027 capital plan.",
        "2.2 A feeder's yearly energy saving is the reduction in the energy delivered into the feeder at its substation "
        "breaker over a year like 2026: the feeder's 2026 load, hour by hour, as it would have been drawn under VO, "
        "against 2026 as the feeder normally runs. The 2026 trial's ON days are not part of normal running.",
        "2.3 Under VO the feeder-head voltage is lowered hour by hour as far as keeps every customer on the feeder at or "
        "above 114 V plus a 1 V margin (115 V on the 120 V base) in that hour, and never by more than 4 percent "
        "(4.8 V on the 120 V base).",
        "2.4 Energy saved is valued at USD 48 per MWh, the District's avoided wholesale energy cost for 2027, and a "
        "year's saving is carried over the equipment's 15-year life at a present-value factor of 9.4 (6.5 percent)."]),
    ("3. Records", [
        "3.1 Customer energy is the meter data management system's feeder interval sums. Voltages at the far end of each "
        "feeder are its AMI bellwether meters' hourly minimum readings. Feeder-head voltage is the substation bus as "
        "SCADA records it, or a pilot regulator's output where one is installed.",
        "3.2 Installed costs are the 2027 capital plan's estimates, which include any mid-line regulator retrofit the "
        "feeder needs."]),
]

PROTOCOL = [
    ("1. Design", [
        "Eight feeders, drawn at random from the District's 24 in January 2026, were fitted with pilot regulators at the "
        "feeder head. In two windows, 16 March to 12 June and 14 September to 13 November 2026, each trial day was "
        "assigned ON or OFF for each trial feeder independently, with even odds, by the System Planning random draw. On an ON day the regulator's schedule lowers its output by 4 percent "
        "(4.8 V) from midnight, returning to normal at the following midnight. On an OFF day the regulator follows the "
        "bus.",
        "The regulators report their mode and output voltage each quarter-hour to the SCADA historian."]),
    ("2. Measurements", [
        "Customer energy on each feeder is taken from the meter data management system's feeder interval sums. Weather "
        "is the Grand Island (KGRI) ASOS station's hourly record."]),
    ("3. Responsibilities", [
        "System Planning holds the assignment draw and the analysis. Distribution Operations maintains the pilot "
        "regulators and their communications."]),
]

AR = [
    ("System statistics, 2025", [
        [["Measure", "2025"], ["Retail customers", "52,140"], ["Energy delivered to the distribution system", "1,206,400 MWh"],
         ["Retail sales", "1,132,800 MWh"], ["Distribution losses", "6.1 percent of energy delivered"],
         ["Distribution feeders", "24, on six substations"], ["Miles of distribution line", "1,872"],
         ["System peak", "268.4 MW (21 July 2025, 17:00)"], ["SAIDI, excluding major event days", "88.6 minutes"]]]),
    ("Residential load research, 2024", [
        [["End use (homes that have it)", "Average annual use"], ["Electric water heater", "3,200 kWh"],
         ["Electric resistance space heating", "12,100 kWh"], ["Heat pump space heating", "4,350 kWh"],
         ["Central air conditioning", "2,300 kWh"], ["Homes metered by end use", "212"]]]),
    ("Notes", [
        "Distribution losses are energy delivered to the distribution system less retail sales and the District's own "
        "use, as a share of energy delivered. Retail sales are billed sales adjusted to the calendar year. Load research "
        "averages are for the homes in the 2024 end-use metering sample that have each end use, weather-normalized to the "
        "District's 30-year normal."]),
]


def write_pdfs(target):
    _doc(os.path.join(target, FILES["std"]), "VO-1 Voltage optimization program standard",
         [["Standard", "VO-1, revision 2"], ["Approved", "8 October 2026, Board of Directors"], ["Owner", "Distribution Engineering"]],
         STANDARD, "Joseph Harmon", "VO-1", "Platte Ridge PPD  VO-1 rev 2", dt.datetime(2026, 9, 21, 10, 4, tzinfo=CDT),
         dt.datetime(2026, 10, 8, 15, 26, tzinfo=CDT))
    _doc(os.path.join(target, FILES["proto"]), "Voltage optimization trial, 2026: protocol",
         [["Document", "SP-2026-03"], ["Issued", "6 January 2026"], ["Owner", "System Planning"]], PROTOCOL, "Mary Wilson",
         "VO trial protocol", "Platte Ridge PPD  SP-2026-03", dt.datetime(2026, 1, 5, 14, 12, tzinfo=CST),
         dt.datetime(2026, 1, 6, 9, 40, tzinfo=CST), producer="LibreOffice 25.8")
    _doc(os.path.join(target, FILES["ar"]), "Annual Report 2025: system statistics",
         [["Extract", "pages 14 and 15"], ["Published", "April 2026"], ["Prepared by", "Finance"]], AR, "Bruce Hart",
         "Annual report 2025", "Platte Ridge PPD  Annual Report 2025", dt.datetime(2026, 3, 30, 11, 2, tzinfo=CDT),
         dt.datetime(2026, 4, 9, 16, 45, tzinfo=CDT), widths=[90, 72], producer="LibreOffice 26.2")


CONDUCTOR = {(0.15, 0.22): "477 AAC", (0.22, 0.30): "336.4 ACSR", (0.30, 0.42): "4/0 ACSR", (0.42, 0.52): "2/0 ACSR", (0.52, 1.0): "1/0 ACSR"}


def conductor(r):
    for (a, b), n in CONDUCTOR.items():
        if a <= r < b:
            return n
    return "1/0 ACSR"


def write_register(path, w, O, ids):
    wb = Workbook()
    ws = wb.active
    ws.title = "Feeders"
    hdr = ["Feeder", "Substation", "Class", "Customers", "Main line length (km)", "Main conductor", "Positive-sequence ohms per km",
           "Mid-line regulator", "Substation revenue meter", "Nominal kV"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="D9E1F2")
    cls = {"res": "Residential", "com": "Commercial", "rural": "Rural"}
    for i, f in enumerate(w.F):
        ws.append([ids[i], f["sub"], cls[f["kind"]], f["customers"], round(f["L"], 1), conductor(f["r"]), round(f["r"], 3),
                   "Yes" if f["midreg"] else "No", "Yes" if i in O.headmetered else "No", 12.47])
    for col, wd in zip("ABCDEFGHIJ", (11, 13, 12, 11, 14, 15, 16, 12, 14, 10)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "B2"
    wb.save(path)


def write_plan(path, w, ids):
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 estimates"
    ws.append(["Feeder", "Scope", "Estimated installed cost (USD)", "Estimate class"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E2EFDA")
    for i, f in enumerate(w.F):
        scope = "Head regulator, VO controller, AMI integration" + ("; mid-line regulator retrofit" if f["midreg"] else "")
        ws.append([ids[i], scope, int(round(f["cost"], -2)), "Class 4"])
    for col, wd in zip("ABCD", (11, 52, 18, 12)):
        ws.column_dimensions[col].width = wd
    wb.save(path)
