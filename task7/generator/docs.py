"""The pack's documents and workbooks: the paging site register and the radio shop's outage log (Excel), the 2027 work
plan's load-management section (Word), last year's programme report and the supplier's 2026 invoices (PDF, exported
by Writer through the house writer), and TriCounty's published coverage map (PNG). Each states facts about the
cooperative's world in its owner's voice; none describes the data or how to use it."""
import datetime as dt
import os
import sys

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as OP  # noqa: E402
import common as CM  # noqa: E402
import params as P  # noqa: E402


def usd(x, dec=0):
    return ("USD {:,.%df}" % dec).format(x)


# ---- the paging site register -----------------------------------------------------------------------------------
def site_rows(W):
    e30 = P.EVENT_DAYS[30]
    e29 = P.EVENT_DAYS[29]
    pruett_on = e29 + dt.timedelta(1) if (e30 - e29).days > 1 else e30
    rows = [("VHF-00", "Larkin old tower", "VHF", "153.875", 0.42, 1.83, dt.date(1996, 8, 14), dt.date(2019, 5, 14),
             P.ORG_SHORT, 120, 140, "Taken down when the headquarters tower went up")]
    on = [dt.date(2003, 6, 2), dt.date(2004, 3, 15), dt.date(2005, 5, 9)]
    erp = [250, 180, 180]
    agl = [180, 120, 140]
    for k, (sid, name, _) in enumerate(P.VHF_SITES):
        rows.append((sid, name, "VHF", "153.875", float(W["vt"][k][0]), float(W["vt"][k][1]), on[k], None, P.ORG_SHORT,
                     erp[k], agl[k], ""))
    on_c = [dt.date(2015, 9, 28), dt.date(2016, 11, 7), dt.date(2016, 4, 18), pruett_on, dt.date(2017, 8, 21)]
    note = ["", "", "", "Commissioned 2026", ""]
    for k, (sid, name, _) in enumerate(P.FLEX_SITES):
        rows.append((sid, name, "FLEX", "929.6125", float(W["ct"][k][0]), float(W["ct"][k][1]), on_c[k], None, P.CARRIER,
                     [500, 350, 350, 350, 350][k], [150, 260, 220, 240, 300][k], note[k]))
    return rows, pruett_on


def sites_xlsx(path, W):
    rows, pruett_on = site_rows(W)
    wb = Workbook()
    ws = wb.active
    ws.title = "Paging sites"
    hdr = ["Site ID", "Site", "System", "Frequency (MHz)", "Grid X (km)", "Grid Y (km)", "On air", "Off air", "Owner",
           "ERP (W)", "Antenna AGL (ft)", "Notes"]
    ws.append(hdr)
    for rr in rows:
        ws.append(list(rr))
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="D9E1F2")
    for row in ws.iter_rows(min_row=2):
        row[6].number_format = "yyyy-mm-dd"
        row[7].number_format = "yyyy-mm-dd"
        row[4].number_format = "0.000"
        row[5].number_format = "0.000"
    for col, wd in zip("ABCDEFGHIJKL", [9, 24, 8, 15, 11, 11, 12, 12, 34, 9, 15, 40]):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Revision")
    ws2.append(["Revised", "By", "Change"])
    ws2.append([dt.date(2019, 5, 20), P.PEOPLE["radio"], "Larkin old tower taken off the air"])
    ws2.append([dt.date(2021, 2, 9), P.PEOPLE["radio"], "ERP and antenna heights re-surveyed"])
    ws2.append([pruett_on + dt.timedelta(3), P.PEOPLE["radio2"], "TriCounty Pruett site added"])
    for row in ws2.iter_rows(min_row=2):
        row[0].number_format = "yyyy-mm-dd"
    ws2.column_dimensions["A"].width = 12
    ws2.column_dimensions["B"].width = 18
    ws2.column_dimensions["C"].width = 44
    wb.save(path)
    return rows, pruett_on


# ---- the radio shop's outage log --------------------------------------------------------------------------------
def outage_rows(r):
    E = P.EVENT_DAYS
    T = lambda d, h, m: dt.datetime(d.year, d.month, d.day, h, m)
    rows = [
        ("Hal sub VHF", T(E[12] - dt.timedelta(1), 21, 40), T(E[19], 20, 15), "Lightning. PA and exciter replaced",
         P.PEOPLE["radio"], "Waited on parts from the vendor"),
        ("Halverson VHF", T(E[12], 7, 10), T(E[19], 19, 55), "Off since the storm", P.PEOPLE["radio2"],
         "Same outage as KM entry"),
        ("TCP Ostrander", T(E[33], 11, 5), T(E[37], 21, 10), "Carrier outage, TriCounty ticket 4471 (backhaul)",
         P.PEOPLE["radio2"], "Per TriCounty notice"),
        ("MF sub stick", T(E[40], 7, 45), T(E[45], 20, 40), "Antenna and feedline replacement", P.PEOPLE["radio"],
         "Crane on site three days"),
    ]
    quiet = [d for d in P.NON_EVENT if d.month in (6, 8, 9)]
    sat = [dt.date(2026, 6, 1) + dt.timedelta(k) for k in range(122)]
    sat = [d for d in sat if d.weekday() == 5]
    sun = [d + dt.timedelta(1) for d in sat]
    rows += [
        ("Hal sub VHF", T(dt.date(2026, 5, 8), 13, 20), T(dt.date(2026, 5, 8), 15, 5), "Power supply", P.PEOPLE["radio"], ""),
        ("HQ tower", T(quiet[2], 9, 10), T(quiet[2], 10, 35), "Scheduled feedline swap", P.PEOPLE["radio"], ""),
        ("MF sub stick", T(quiet[4], 8, 0), T(quiet[4], 11, 45), "Antenna survey ahead of replacement", P.PEOPLE["radio2"], ""),
        ("TCP Bluestem", T(sat[3], 2, 0), T(sat[3], 5, 30), "Carrier maintenance window", P.PEOPLE["radio2"], "Per TriCounty notice"),
        ("TCP Larkin", T(sun[9], 14, 0), T(sun[9], 16, 40), "Water tower painting, carrier notice", P.PEOPLE["radio"], ""),
        ("HQ tower", T(sat[13], 23, 15), T(sat[13] + dt.timedelta(1), 0, 50), "Utility power out at HQ, generator did not start",
         P.PEOPLE["radio"], "Generator battery replaced"),
    ]
    rows.sort(key=lambda t: t[1])
    return rows


def outages_xlsx(path, r):
    rows = outage_rows(r)
    wb = Workbook()
    ws = wb.active
    ws.title = "2026"
    ws.append(["Site", "Down", "Back up", "Cause", "Logged by", "Notes"])
    for rr in rows:
        ws.append(list(rr))
    for c in ws[1]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=2):
        row[1].number_format = "m/d/yy h:mm"
        row[2].number_format = "m/d/yy h:mm"
    for col, wd in zip("ABCDEF", [15, 14, 14, 46, 16, 30]):
        ws.column_dimensions[col].width = wd
    wb.save(path)
    return rows


# ---- the work plan ---------------------------------------------------------------------------------------------
def plan_text():
    S = P
    props = [
        ("LM-27-01", "Kettle Ridge VHF repeater",
         "One new transmitter site on the cooperative's 153.875 MHz VHF paging system at Kettle Ridge, grid -31.0 km, "
         "12.0 km, carrying the same group addresses as the present VHF sites.",
         "USD 16,300 a year (site lease, power and upkeep, and the transmitter over ten years)"),
        ("LM-27-02", "Halverson carrier fill-in site",
         "One new TriCounty Paging 929.6125 MHz FLEX site at the Halverson elevator, grid 3.0 km, 25.0 km, added to the "
         "paging contract.", "USD 24,600 a year (TriCounty's quoted fee)"),
        ("LM-27-03", "Larkin find-and-fix round",
         "A visit to every A/C switch installed through 2015 in the Larkin district at a premise not on the "
         "reconnection lists (LM-27-05 and LM-27-06). The technician replaces the switch with a new one on the same "
         "paging system and group.", "USD 15.60 a year for each premise visited (the visit and the new switch over ten years)"),
        ("LM-27-04", "Medora Flats find-and-fix round",
         "The same visit to every A/C switch installed through 2015 in the Medora Flats district at a premise not on "
         "the reconnection lists.", "USD 28.40 a year for each premise visited"),
        ("LM-27-05", "Reconnection round within 14 km",
         "A visit to every premise with an active A/C switch where a cooperative rebate or a county mechanical permit "
         "for a replacement central air conditioner or central heat pump is dated after the switch was installed, and "
         "the switch is within 14 km of the nearest transmitter serving it. The technician connects the switch to the "
         "condensing unit wherever it is not connected.", "USD 13.70 a year for each premise visited"),
        ("LM-27-06", "Outlying reconnection round",
         "The same visit to the premises on that list whose switch is more than 14 km from the nearest transmitter "
         "serving it.", "USD 24.50 a year for each premise visited"),
    ]
    return props


def plan_docx(path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    sec.left_margin = sec.right_margin = Mm(24)
    sec.top_margin, sec.bottom_margin = Mm(22), Mm(20)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    h = doc.add_paragraph()
    run = h.add_run("2027 Work Plan")
    run.bold = True
    run.font.size = Pt(16)
    h2 = doc.add_paragraph()
    r2 = h2.add_run("Section 6. Load management")
    r2.bold = True
    r2.font.size = Pt(13)
    meta = doc.add_table(rows=4, cols=2)
    meta.style = "Table Grid"
    for i, (a, b) in enumerate([("Status", "Draft for the Board, December 2026 meeting"),
                                ("Prepared by", "Energy Services, %s" % P.PEOPLE["energy"]),
                                ("Appraisal constants", "Finance, %s" % P.PEOPLE["finance"]),
                                ("Draft of", "12 November 2026")]):
        meta.cell(i, 0).text = a
        meta.cell(i, 1).text = b
    doc.add_paragraph()

    def head(t):
        p = doc.add_paragraph()
        rr = p.add_run(t)
        rr.bold = True
        rr.font.size = Pt(11.5)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.keep_with_next = True

    def para(t):
        p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(5)
        return p

    head("6.1 The programme")
    para("The summer load management programme sheds enrolled members' central air conditioners on afternoons when "
         "Sunflower Basin Power's monthly coincident peak is likely. Each A/C load control switch belongs to one of "
         "sixteen A/C paging groups, and shed and restore commands go out by group over the cooperative's own VHF "
         "paging system and TriCounty Paging's 900 MHz FLEX service. The switches are one-way receivers and members' "
         "meters are read once a month, so no premise reports what its switch did. A water heater programme runs "
         "in winter on its own groups and is not part of this section.")
    head("6.2 The 2026 dispatch trial")
    para("Energy Services called load management on 60 weekday afternoons between 1 June and 30 September 2026. On each "
         "of them a set of the sixteen A/C groups, drawn by lot that morning, was shed from 16:00 to 19:00, one group "
         "every ten minutes from 16:00 in an order also drawn by lot; the other groups were not paged that day. The "
         "restores went out from 19:00, one group a minute in the same order. The 380 interval-metered load research "
         "homes recruited in 2019 were shed or held out home by home on each of those afternoons by the load research "
         "contractor, from 15:45 to 18:45.")
    head("6.3 Proposals")
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for j, hh in enumerate(["No.", "Proposal", "Scope", "Annual cost"]):
        t.rows[0].cells[j].text = hh
        for p_ in t.rows[0].cells[j].paragraphs:
            for rr in p_.runs:
                rr.bold = True
    for no, name, scope, cost in plan_text():
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text, row[3].text = no, name, scope, cost
    for row in t.rows:
        for j, wmm in enumerate([18, 36, 80, 34]):
            row.cells[j].width = Mm(wmm)
    doc.add_paragraph()
    head("6.4 Appraisal")
    para("A kilowatt off the cooperative's load in Sunflower Basin's monthly coincident peak hour saves the demand charge "
         "of USD 22.00 a kW-month in each of the four summer months, June to September: USD 88 a kW-year.")
    para("Each proposal is appraised on its own, against present practice, as the kilowatts it adds during a shed in "
         "summer 2027 for the A/C switches active on the switch register at 30 September 2026, with every transmitter "
         "listed on the paging site register on the air, on an afternoon at Sunflower Basin's cooling index of the four "
         "2026 coincident-peak afternoons, 1.15. A proposal is worth funding when those kilowatts, at USD 88 a kW-year, "
         "cover its annual cost.")
    para("Paging performance is reported for the fringe, premises more than 20 km from the nearest transmitter serving "
         "them, against premises within 8 km.")
    para("The shed is reported as a bridge from what the switches could take off, each taking off what a working switch "
         "near a transmitter does, to what they deliver, in this order, each switch counted once against the first of "
         "these that stops it: commands not received; received but the switch failed; working but not connected to "
         "the air conditioner; delivered.")
    head("6.5 Timing")
    para("Approved proposals start in January 2027. The repeater and the fill-in site would be on the air by 1 June 2027; "
         "the rounds would be finished by 15 May 2027.")
    doc.save(path)


# ---- PDFs --------------------------------------------------------------------------------------------------------
def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=13.4, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, header_rows, sections, author, subject, footer, created, modified, widths=None, producer=None):
    body, h1, h2, cell = _styles()
    story = [Paragraph(title, h1), _grid(header_rows, [44 * 2.83, 118 * 2.83], cell), Spacer(1, 6)]
    for head, paras in sections:
        if head:
            story.append(Paragraph(head, h2))
        for p in paras:
            if isinstance(p, list):
                n = len(p[0])
                w = (widths or {}).get(n) or {2: [92, 70], 3: [70, 46, 46], 4: [52, 36, 36, 38], 5: [40, 32, 30, 30, 30]}[n]
                story.append(_grid(p, [x * 2.83 for x in w], cell))
                story.append(Spacer(1, 4))
            elif p == "PAGE":
                from reportlab.platypus import PageBreak
                story.append(PageBreak())
            else:
                story.append(Paragraph(p, body))
    OP.build(path, story, title=title, author=author, subject=subject, footer=footer, created=created, modified=modified,
             font="Liberation Sans", producer=producer)


def report_pdf(path, counts_2025):
    tot = sum(counts_2025["ac"].values())
    wh = sum(counts_2025["wh"].values())
    plan_kw = tot * 1.0
    sections = [
        ("1. Enrolment at 31 December 2025", [
            [["District", "A/C switches", "Water heater switches"]] +
            [[d, format(counts_2025["ac"][d], ","), format(counts_2025["wh"][d], ",")] for d in P.DISTRICTS] +
            [["Total", format(tot, ","), format(wh, ",")]],
            "New A/C enrolments in 2025: %s. Switches removed at members' request or on a vacated premise: %s." % (
                format(counts_2025["new"], ","), format(counts_2025["removed"], ","))]),
        ("2. Operations", [
            "Load management was called on 37 weekday afternoons in 2025, 16:00 to 19:00, with every A/C group shed. "
            "All four of Sunflower Basin's summer coincident peak hours fell on a called afternoon. The water heater "
            "programme was called on 31 winter mornings and evenings."]),
        ("3. Planned load reduction", [
            "The programme plans on 1.0 kW of reduction for each enrolled A/C switch during a shed (the planning figure "
            "set when the programme began in 2004; it is not a measurement). At 31 December 2025 that is %s kW, worth "
            "%s a year at the 2025 summer demand charge of USD 21.35 a kW-month." % (format(int(plan_kw), ","),
                                                                                        usd(plan_kw * 21.35 * 4))]),
        ("4. Costs", [
            [["Item", "2025"], ["TriCounty paging contract", "USD 41,880"], ["VHF paging (power, leases, upkeep)", "USD 18,240"],
             ["Switch installs and replacements", "USD 52,910"], ["Member incentives (bill credits)", "USD 286,140"],
             ["Load research contract", "USD 38,500"], ["Total", "USD 437,670"]]]),
        ("5. For 2026", [
            "Energy Services will run a dispatch trial in summer 2026, with the A/C groups to be shed each afternoon drawn "
            "by lot."]),
    ]
    _doc(path, "Load Management Program: 2025 Annual Report",
         [["Report", "LM-AR-2025"], ["Issued", "17 February 2026"], ["Prepared by", "Energy Services"]], sections,
         P.PEOPLE["energy"], "Load management 2025", "%s  LM-AR-2025" % P.ORG_SHORT,
         dt.datetime(2026, 2, 12, 10, 26, tzinfo=P.CST), dt.datetime(2026, 2, 17, 15, 3, tzinfo=P.CST), producer="LibreOffice 25.8")


def invoices_pdf(path, peaks):
    """One invoice a month, June to September: the cooperative's load in the supplier's coincident peak hour sets the
    demand charge."""
    secs = []
    first = True
    for mo, (day, he, kw, idx) in sorted(peaks.items()):
        mname = dt.date(2026, mo, 1).strftime("%B 2026")
        energy = {6: 46820.4, 7: 55163.9, 8: 53902.2, 9: 40115.7}[mo]
        dem = round(kw * 22.00, 2)
        en = round(energy * 41.85, 2)
        tr = round(kw * 4.10, 2)
        fac = round(energy * {6: 1.62, 7: 2.08, 8: 1.94, 9: 1.21}[mo], 2)
        tot = dem + en + tr + fac
        if not first:
            secs.append((None, ["PAGE"]))
        first = False
        inv = "SBP-%d-%04d" % (2026, {6: 661, 7: 702, 8: 749, 9: 793}[mo])
        secs.append(("Invoice %s, %s" % (inv, mname), [
            [["Item", "Basis", "Amount"],
             ["Demand", "%s kW at USD 22.00 a kW-month" % format(int(round(kw)), ","), usd(dem, 2)],
             ["Energy", "%s MWh at USD 41.85 a MWh" % format(energy, ",.1f"), usd(en, 2)],
             ["Transmission", "%s kW at USD 4.10 a kW-month" % format(int(round(kw)), ","), usd(tr, 2)],
             ["Fuel and purchased power adjustment", "%s MWh" % format(energy, ",.1f"), usd(fac, 2)],
             ["Total due", "", usd(tot, 2)]],
            "Billing demand is the member's metered load in the Sunflower Basin coincident peak hour: %s, hour ending "
            "%02d:00 CDT. Sunflower Basin cooling index for that afternoon: %.3f." % (day.strftime("%A %d %B %Y"), he, idx),
            "Payment due 20 days from the invoice date. Questions: Member Billing, %s." % P.PEOPLE["billing"]]))
    _doc(path, "Sunflower Basin Power Cooperative: wholesale power invoices to %s, summer 2026" % P.ORG_SHORT,
         [["Member", "%s (member 14)" % P.ORG_SHORT], ["Statements", "June to September 2026"], ["Issued by", "Member Billing"]],
         secs, P.PEOPLE["billing"], "Wholesale invoices", "%s  member statements 2026" % P.SUPPLIER,
         dt.datetime(2026, 10, 6, 9, 12, tzinfo=P.CDT), dt.datetime(2026, 10, 9, 14, 37, tzinfo=P.CDT),
         widths={3: [62, 70, 30]}, producer="LibreOffice 25.8")


# ---- the coverage map --------------------------------------------------------------------------------------------
def coverage_png(path, W, pruett_on):
    """TriCounty's published coverage map for the cooperative: outdoor coverage of both paging systems, drawn as each
    system's published contour. Every premise in the territory is inside both."""
    Wpx, Hpx = 1500, 1150
    img = Image.new("RGB", (Wpx, Hpx), (250, 250, 247))
    dr = ImageDraw.Draw(img, "RGBA")
    x0, x1, y0, y1 = -50.0, 46.0, -22.0, 48.0
    sx = lambda x: int(70 + (x - x0) / (x1 - x0) * (Wpx - 140))
    sy = lambda y: int(Hpx - 90 - (y - y0) / (y1 - y0) * (Hpx - 200))
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 26)
        f2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 17)
        f3 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 14)
    except Exception:
        f1 = f2 = f3 = ImageFont.load_default()
    # grid
    for gx in range(-50, 47, 10):
        dr.line([(sx(gx), sy(y0)), (sx(gx), sy(y1))], fill=(220, 220, 215), width=1)
        dr.text((sx(gx) - 10, sy(y0) + 6), "%d" % gx, fill=(120, 120, 120), font=f3)
    for gy in range(-20, 49, 10):
        dr.line([(sx(x0), sy(gy)), (sx(x1), sy(gy))], fill=(220, 220, 215), width=1)
        dr.text((sx(x0) - 34, sy(gy) - 8), "%d" % gy, fill=(120, 120, 120), font=f3)
    # published outdoor contours: generous circles around each site, merged
    rr_ = np.random.default_rng(P.SEED + 404)

    def contour(sites, rad, colour):
        """Each site's published contour: never inside its nominal radius, pushed out where the terrain carries."""
        for (x, y), rr in zip(sites, rad):
            th = np.linspace(0, 2 * np.pi, 181)
            a = rr_.uniform(0, 2 * np.pi, 3)
            bump = 0.07 * (1 + np.sin(3 * th + a[0])) + 0.04 * (1 + np.sin(5 * th + a[1])) + 0.02 * (1 + np.sin(8 * th + a[2]))
            r = rr * (1 + bump)
            dr.polygon([(sx(x + r[k] * np.cos(th[k])), sy(y + r[k] * np.sin(th[k]))) for k in range(len(th))], fill=colour)
    # each system's contour reaches past the farthest premise on that system
    rv = float(W["dv"].min(1)[W["vhf"]].max()) + 2.6
    rc = float(W["dc"].min(1)[~W["vhf"]].max()) + 2.4
    contour([tuple(v) for v in W["vt"]], [rv, rv - 0.8, rv - 1.4], (60, 120, 200, 46))
    contour([tuple(v) for v in W["ct"]], [rc, rc - 0.6, rc + 0.4, rc - 1.0, rc + 0.8], (230, 140, 40, 42))
    # towns and sites
    for k, (town, (tx, ty)) in P.TOWNS.items():
        dr.rectangle([sx(tx) - 4, sy(ty) - 4, sx(tx) + 4, sy(ty) + 4], fill=(60, 60, 60))
        dr.text((sx(tx) - 20, sy(ty) + 10), town, fill=(40, 40, 40), font=f2)
    for k, (sid, name, _) in enumerate(P.VHF_SITES):
        x, y = W["vt"][k]
        dr.polygon([(sx(x), sy(y) - 10), (sx(x) - 8, sy(y) + 6), (sx(x) + 8, sy(y) + 6)], fill=(30, 80, 170))
        dr.text((sx(x) + 10, sy(y) - 22), name + " (VHF)", fill=(30, 60, 140), font=f3)
    for k, (sid, name, _) in enumerate(P.FLEX_SITES):
        x, y = W["ct"][k]
        dr.ellipse([sx(x) - 7, sy(y) - 7, sx(x) + 7, sy(y) + 7], fill=(200, 110, 20))
        dr.text((sx(x) + 10, sy(y) + 2), "TriCounty " + name, fill=(150, 80, 10), font=f3)
    dr.text((70, 22), "Paging coverage, Cottonwood Draw Electric Cooperative service territory", fill=(20, 20, 20), font=f1)
    dr.text((70, 56), "Published outdoor coverage, %s 2026 edition. TriCounty Paging LLC." % (pruett_on + dt.timedelta(9)).strftime("%B"),
            fill=(60, 60, 60), font=f2)
    ly = Hpx - 60
    dr.rectangle([70, ly, 96, ly + 18], fill=(60, 120, 200, 110))
    dr.text((104, ly), "Cottonwood Draw VHF 153.875 MHz, outdoor coverage", fill=(40, 40, 40), font=f3)
    dr.rectangle([560, ly, 586, ly + 18], fill=(230, 140, 40, 110))
    dr.text((594, ly), "TriCounty FLEX 929.6125 MHz, outdoor coverage", fill=(40, 40, 40), font=f3)
    dr.text((1040, ly), "Grid: cooperative planning grid, km", fill=(90, 90, 90), font=f3)
    img.save(path, format="PNG", optimize=False)
