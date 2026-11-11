"""task8: the two files the prompt asks for, as the trust's data and assessment lead hands them to the director of
education: the Reading Forward entry workbook (every Year 7 student on roll at the census with their entry reading
on the Lexis basis and their placement; each academy's numbers and tutor hours; the conversions; what the same
arithmetic gives on each shortcut) and a one-page note."""
import datetime as dt
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import postprocess  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402

XLSX = "reading_forward_entry_2026.xlsx"
PDF = "reading_forward_tutor_time_2026.pdf"
BST = dt.timezone(dt.timedelta(hours=1))
GMT = dt.timezone(dt.timedelta(hours=0))
BASIS = {"lexis": "Lexis, first sitting", "july": "Lexis at the July transition day, brought to September",
         "quill": "Quill, converted to Lexis", "brightway": "Brightway, converted to Lexis",
         "ks2": "No valid sitting: KS2 reading equivalent", "none": "No result: assessed on arrival"}
SHOW = [("careful", "The trial's pairs as they stand, the July sittings as entry reading and in the KS2 link"),
        ("the trial's pairs as they stand", "Brightway converted through the trial's pairs as they stand"),
        ("the July sittings as entry reading", "The July transition-day sittings as entry reading and in the KS2 link"),
        ("the other tests' standardised scores read as Lexis scores", "Each test's own standardised score read as Lexis"),
        ("Quill predicted from KS2 by regression", "Quill predicted from KS2 by regression")]


def money(x):
    return "£{:,.0f}".format(x)


def workbook(path, G):
    g = G["golden"]
    D = G["D"]
    acad = sorted(D["academies"])
    wb = Workbook()
    ws = wb.active
    ws.title = "Students"
    ws.append(["Reading Forward 2026-27: Year 7 entry reading on the Lexis basis (on roll at the 1 October 2026 census)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Hollinbrook Academies Trust · Data and assessment · policy version 3 (entry reading below 85 joins)"])
    ws.append([])
    head = ["UPN", "Academy", "Entry test", "Sitting used", "Date of sitting", "Result as recorded",
            "Entry reading (Lexis basis)", "How placed", "Reading Forward"]
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    rows = sorted(g["placements"], key=lambda p: (p["s"]["academy"], p["s"]["upn"]))
    for p in rows:
        s = p["s"]
        f = R.first_valid(s)
        used = {"LEXIS": "Lexis", "QUILL": "Quill", "BRIGHTWAY": "Brightway"}[f["test"]] if f else (
            "KS2" if p["basis"] == "ks2" else "")
        ws.append([s["upn"], s["academy"], s["test"], used, f["date"] if f else None,
                   (f["sas"] if f else (s["ks2"] if p["basis"] == "ks2" else None)), p["whole"], BASIS[p["basis"]],
                   "Yes" if p["placed"] else "No"])
        ws.cell(ws.max_row, 5).number_format = "dd/mm/yyyy"
    ws.freeze_panes = "C5"
    for col, w in zip("ABCDEFGHI", [16, 27, 11, 11, 12, 11, 13, 46, 10]):
        ws.column_dimensions[col].width = w
    ws.auto_filter.ref = "A4:I%d" % ws.max_row
    w2 = wb.create_sheet("Academies")
    w2.append(["Reading Forward numbers and tutor time by academy, 2026-27"])
    w2["A1"].font = Font(bold=True, size=12)
    w2.append([])
    w2.append(["Academy", "Entry test", "On roll at the census", "With a valid entry sitting", "Placed on KS2",
               "No result", "Reading Forward students", "Tutor hours a week", "On the academy's own test",
               "Change from own test"])
    for c in w2[3]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    tot = [0] * 7
    for a in acad:
        on = sum(1 for p in g["placements"] if p["s"]["academy"] == a)
        ks = sum(1 for p in g["placements"] if p["s"]["academy"] == a and p["basis"] == "ks2")
        no = sum(1 for p in g["placements"] if p["s"]["academy"] == a and p["basis"] == "none")
        vals = [on, g["R1"][a], ks, no, g["R6"][a], g["R9"][a], g["own"][a]]
        w2.append([a, D["academies"][a]["entry_reading_test"]] + vals + [g["R7"][a]])
        w2.cell(w2.max_row, 8).number_format = "0.0"
        tot = [x + y for x, y in zip(tot, vals)]
    w2.append(["All academies", None] + tot[:5] + [round(tot[5], 1), tot[6], g["R6_total"] - g["own_total"]])
    w2.cell(w2.max_row, 8).number_format = "0.0"
    for c in w2[w2.max_row]:
        c.font = Font(bold=True)
    w2.append([])
    w2.append(["Tutor time for the year: %.1f hours a week for 36 weeks at £27.80 an hour" % g["R8_hours"], None, None,
               None, None, None, None, g["R8_cost"]])
    w2.cell(w2.max_row, 8).number_format = "£#,##0"
    w2.append(["Provisional budget approved in July", None, None, None, None, None, None, P.PROVISIONAL_BUDGET])
    w2.cell(w2.max_row, 8).number_format = "£#,##0"
    if "boot" in G:
        lo, hi = G["boot"]["lo"], G["boot"]["hi"]
        w2.append(["Range (5th to 95th percentile of the conversions re-estimated)", None, None, None, None, None,
                   "%d to %d" % (lo, hi), round(lo * P.HOURS_PER_STUDENT, 1), round(hi * P.HOURS_PER_STUDENT, 1)])
    w2.freeze_panes = "B4"
    for col, w in zip("ABCDEFGHIJ", [30, 10, 11, 12, 10, 9, 12, 11, 12, 11]):
        w2.column_dimensions[col].width = w
    w3 = wb.create_sheet("Conversions")
    w3.append(["Results on the Quill and Brightway tests at the Lexis score of equal reading at the start of Year 7"])
    w3["A1"].font = Font(bold=True)
    w3.append(["Result", "Quill to Lexis", "Brightway to Lexis"])
    for c in w3[2]:
        c.font = Font(bold=True)
    for x in R.POINTS:
        w3.append([x, round(g["R4"][x], 1), round(g["R3"][x], 1)])
        w3.cell(w3.max_row, 2).number_format = "0.0"
        w3.cell(w3.max_row, 3).number_format = "0.0"
    w3.append([])
    w3.append(["A Lexis sitting at the July transition day stands %.1f points above the same student at the start of "
               "Year 7; each July result is brought down by it." % g["R5"]])
    w3.append(["The Lexis trial at the Brightway academies was a second sitting for most students; a second sitting ran "
               "%.1f points above a first, and the trial's results are taken back by it before the conversion." % g["R2"]])
    w3.column_dimensions["A"].width = 12
    w3.column_dimensions["B"].width = 16
    w3.column_dimensions["C"].width = 18
    w4 = wb.create_sheet("Checks")
    w4.append(["What the same placement gives when one step is done another way"])
    w4["A1"].font = Font(bold=True)
    w4.append(["Way of working", "Reading Forward students", "Tutor hours a week", "Cost for the year"])
    for c in w4[2]:
        c.font = Font(bold=True)
    w4.append(["This workbook", g["R6_total"], g["R8_hours"], g["R8_cost"]])
    for nm, label in SHOW:
        r = G["routes"][nm]
        w4.append([label, r["R6_total"], r["R8_hours"], r["R8_cost"]])
        w4.cell(w4.max_row, 4).number_format = "£#,##0"
    w4.cell(3, 4).number_format = "£#,##0"
    w4.append([])
    ev = G["evidence"]
    w4.append(["At the three academies where half the tutor groups sat Lexis first, Lexis ran %.1f points above "
               "Brightway when it came second and %.1f below when it came first (%d and %d students)." % (
                   ev["gap_lexis_second"], -ev["gap_lexis_first"], ev["n_lexis_second"], ev["n_lexis_first"])])
    w4.append(["The students who sat Lexis first there scored %.1f on average; their KS2 results, read through the "
               "September Lexis academies, give %.1f, so a conversion through KS2 would read these academies a "
               "little high; the trial is the trust's link for Brightway (policy section 6)."
               % (ev["switch_lexis_first_obs"], ev["switch_lexis_first_ks2_pred"])])
    tots = [r["R6_total"] for r in G["rivals"].values()] + [g["R6_total"]]
    w4.append(["Other reasonable versions of the conversions (no presmoothing, four or eight moments kept, Quill by "
               "frequency estimation, the gain from median gaps or the fixed-order academies alone, the July level by "
               "median or by regression) place %d to %d students; where they differ it is a whole score group at "
               "the cut." % (min(tots), max(tots))])
    w4.column_dimensions["A"].width = 70
    w4.column_dimensions["B"].width = 14
    w4.column_dimensions["C"].width = 12
    w4.column_dimensions["D"].width = 14
    w5 = wb.create_sheet("Notes")
    for line in [
            "As of: the October 2026 census (1 October) and the exports of 2 to 12 October 2026.",
            "Entry reading as in the Reading Forward policy, version 3: a student's reading at the start of Year 7 on "
            "the Lexis 2019 standardisation, as a whole score, from their first valid sitting after the May 2026 KS2 tests; "
            "a Quill session counts with 24 questions or more.",
            "Students with no valid sitting by the census are placed from their KS2 reading scaled score, at the Lexis "
            "score of equal reading at the start of Year 7; students with neither are assessed on arrival and are not "
            "counted.",
            "Students who left before the census are not included; a student who moved between academies counts at the "
            "academy on whose roll they were at the census, on their first sitting.",
            "Tutor time: 0.4 hours a week per Reading Forward student; hours to one decimal, money to the pound."]:
        w5.append([line])
    w5.column_dimensions["A"].width = 120
    wb.save(path)
    postprocess.normalize_ooxml(path, "Annette McDonald", "Annette McDonald", "2026-10-13T07:41:00Z",
                                "2026-10-14T16:12:00Z", excel=True, company=P.TRUST)


def note(path, G):
    g = G["golden"]
    D = G["D"]
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.0, leading=12.2, spaceAfter=4)
    h1 = ParagraphStyle("h", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.0, leading=15, spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=7.4, leading=8.8)
    acad = sorted(D["academies"], key=lambda a: (D["academies"][a]["entry_reading_test"], a))
    rows = [["Academy", "Test", "Reading Forward", "Hours a week", "Own test", "Change"]]
    for a in acad:
        rows.append([a, D["academies"][a]["entry_reading_test"], g["R6"][a], "%.1f" % g["R9"][a], g["own"][a],
                     "%+d" % g["R7"][a]])
    rows.append(["All academies", "", g["R6_total"], "%.1f" % g["R8_hours"], g["own_total"],
                 "%+d" % (g["R6_total"] - g["own_total"])])
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[150, 52, 66, 58, 52, 44])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9AA0AB")),
                           ("TOPPADDING", (0, 0), (-1, -1), 0.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6)]))
    extra = g["R8_cost"] - P.PROVISIONAL_BUDGET
    rng = G.get("boot", {})
    s = [Paragraph("Data and assessment · To: Rosemary Collier, director of education · From: Annette McDonald · "
                   "14 October 2026", small),
         Paragraph("Reading Forward needs %.1f tutor hours a week this year, %s more than the provisional budget" % (
             g["R8_hours"], money(extra)), h1),
         Paragraph("On the October census, %d Year 7 students join Reading Forward: their reading at the start of Year 7 "
                   "is below 85 on the Lexis basis. At 0.4 hours a week each that is %.1f tutor hours a week, %s for the "
                   "36 weeks at £27.80 an hour, against the provisional %s approved in July%s." % (
                       g["R6_total"], g["R8_hours"], money(g["R8_cost"]), money(P.PROVISIONAL_BUDGET),
                       (" (range %d to %d students, %s to %s, from re-estimating the conversions)" % (
                           rng["lo"], rng["hi"], money(rng["lo"] * P.HOURS_PER_STUDENT * P.WEEKS * P.RATE),
                           money(rng["hi"] * P.HOURS_PER_STUDENT * P.WEEKS * P.RATE))) if rng else ""), body),
         t, Paragraph("Source: census of 1 October 2026; Lexis, Quill and Brightway results to 30 September; KS2 2026.",
                      small), Spacer(1, 4),
         Paragraph("Each academy's own test gives %d students, %d fewer. Quill's standardised scores come from a softer "
                   "2024 sample, so a Quill 85 is a Lexis %.1f and the Quill academies' own lists miss %d students. The "
                   "Brightway academies' own lists run %d high, but their Lexis trial was a second sitting for most "
                   "students and ran %.1f points above a first sitting; taken back, a Brightway 85 is a Lexis %.1f. The "
                   "July transition-day Lexis results stand %.1f points above the start of Year 7 and are brought down "
                   "by it, which adds %d students at the four July academies." % (
                       g["own_total"], g["R6_total"] - g["own_total"], g["R4"][85],
                       G["golden"]["R7_test"].get("Quill", 0), -G["golden"]["R7_test"].get("Brightway", 0), g["R2"],
                       g["R3"][85], g["R5"], G["golden"]["R7_test"].get("Lexis", 0)), body),
         Paragraph("Conversions to the Lexis basis, Quill and Brightway: " + "; ".join(
             "%d: %.1f and %.1f" % (x, g["R4"][x], g["R3"][x]) for x in R.POINTS) + ".", body),
         Paragraph("Students without a valid sitting by the census are placed on their KS2 reading; those with neither "
                   "are assessed on arrival and are not in these numbers. Places are confirmed to families by each "
                   "academy after this note.", small)]
    O.build(path, s, "Reading Forward tutor time 2026-27", "Annette McDonald", "Note to the director of education",
            "Hollinbrook Academies Trust · Data and assessment", dt.datetime(2026, 10, 14, 15, 2, tzinfo=BST),
            dt.datetime(2026, 10, 14, 16, 8, tzinfo=BST))


def write(gold_dir, G):
    os.makedirs(gold_dir, exist_ok=True)
    for f in os.listdir(gold_dir):
        os.remove(os.path.join(gold_dir, f))
    workbook(os.path.join(gold_dir, XLSX), G)
    note(os.path.join(gold_dir, PDF), G)
    postprocess.own_mtimes(gold_dir, {})
