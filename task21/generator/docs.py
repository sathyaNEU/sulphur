"""Halvergate Mutual's own documents and workbooks: the executive pricing team's 2027 planning basis (PLN-2027-03),
the renewal pricing policy (CMP-RP-04), the comparison-site commission schedule (PCW-COM-2026), the motor excess of
loss programme summary, the reserving team's triangles, the renewal retention MI, the comparison-site rate change log
and the direct channel's monthly figures. The PDFs are Word documents exported by LibreOffice Writer through the
house writer; the workbooks pass through the house workbook writer with their owners' stamps."""
import datetime as dt
import os
import sys

import numpy as np
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
import params as P  # noqa: E402
import world  # noqa: E402

ORG = "Halvergate Mutual Insurance Society Limited"
GMT = dt.timezone.utc
BST = dt.timezone(dt.timedelta(hours=1))

FILES = {
    "plan": "PLN-2027-03_pcw_rate_plan_2027_planning_basis.pdf",
    "policy": "CMP-RP-04_renewal_pricing_policy.pdf",
    "comm": "PCW-COM-2026_comparison_site_commissions.pdf",
    "xol": "motor_xol_reinsurance_programme_2026.pdf",
    "tri": "reserving_triangles_2026Q3.xlsx",
    "ret": "renewal_retention_mi_65plus_2025-2026.xlsx",
    "rates": "pcw_rate_change_log_2024-2026.xlsx",
    "direct": "direct_web_quotes_sales_2025_2026.xlsx",
}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=12.9, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.5,
                        spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.6,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.6, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, sections, meta, header_rows, author, subject, footer, created, modified, producer=None,
         font="Liberation Sans"):
    body, h1, h2, small, cell = _styles()
    story = [Paragraph(title, h1)]
    story.append(_grid(header_rows, [42 * 2.83, 120 * 2.83], cell))
    story.append(Spacer(1, 6))
    for head, paras in sections:
        story.append(Paragraph(head, h2))
        for p in paras:
            if isinstance(p, list):
                story.append(_grid(p, [60 * 2.83, 40 * 2.83, 60 * 2.83][:len(p[0])], cell))
            else:
                story.append(Paragraph(p, body))
    if meta:
        story.append(Spacer(1, 8))
        story.append(Paragraph(meta, small))
    O.build(path, story, title=title, author=author, subject=subject, footer=footer, created=created,
            modified=modified, producer=producer, font=font)


PLAN = [
    ("1. Purpose", [
        "1.1 This paper fixes the basis on which the executive pricing team sets the rate changes for Halvergate's "
        "private car new business sold through comparison sites from 1 January 2027, and against which proposals for "
        "those changes are judged.",
        "1.2 The business is divided by the age of the main driver on the quote: under 25, 25 to 64, and 65 and over.",
        "1.3 The comparison sites are Kitecompare, Covertide, Brightquote and Pricelark. Business sold direct or "
        "through brokers is outside this paper."]),
    ("2. Measures", [
        "2.1 A segment's loss ratio is its ultimate claims, each claim capped at £%s, at 2027 cost levels, "
        % format(int(P.CLAIM_CAP), ",") +
        "divided by its written premium net of insurance premium tax, for the policies it writes in the year, each "
        "over its own policy year.",
        "2.2 Claims at 2026 cost levels are taken to 2027 cost levels by raising them 5.5 per cent.",
        "2.3 Halvergate's 2027 premium for a risk is the premium the rates in force on 31 October 2026 give it, with "
        "the segment's 2027 change applied; the pricing model's claims-cost index stays at its 2026 level through "
        "2027."]),
    ("3. Records", [
        "3.1 Experience is read from the policy and claims extracts as at 31 October 2026 and from the reserving "
        "team's triangles to 30 September 2026."]),
    ("4. The 2027 market", [
        "4.1 The comparison sites are taken to return 2027 quotes in the number and mix they returned from 1 February "
        "2026 to 31 October 2026, scaled to twelve months.",
        "4.2 Rivals' prices on the sites are taken to rise 2 per cent on 1 January 2027 and not to move again during "
        "2027."]),
    ("5. Setting the changes", [
        "5.1 A segment's change is the smallest change, in whole per cent, at which the expected loss ratio of its "
        "2027 comparison-site new business is 75 per cent or below.",
        "5.2 Where a range is given for a loss ratio it is the range within which 80 per cent of the year's outcomes "
        "would fall: the claims the year's policies bring, drawn policy by policy, around the expected loss ratio."]),
    ("6. Underwriting profit", [
        "6.1 Underwriting profit is written premium net of insurance premium tax, less capped claims at 2027 cost "
        "levels, less the site's commission on each sale (PCW-COM-2026, unchanged for 2027) and less servicing of £34 "
        "a policy.",
        "6.2 A segment's 2027 underwriting profit counts its comparison-site new business written in 2027 and its "
        "customers first sold through a comparison site who renew in 2027, as the 2027 renewal schedule lists them.",
        "6.3 A change that lowers a segment's loss ratio and its underwriting profit together goes to the executive "
        "with both figures."]),
]

POLICY = [
    ("1. Scope", [
        "1.1 This policy governs the premiums Halvergate offers at renewal on private car and home insurance. It "
        "gives effect to the general insurance pricing rules in force from 1 January 2022 (ICOBS 6B)."]),
    ("2. Setting renewal premiums", [
        "2.1 Renewal premiums are set by the renewal pricing team from the customer's risk, claims record and the "
        "renewal rates approved for the year.",
        "2.2 Renewal invitations are issued at least 21 days before the renewal date."]),
    ("3. The equivalent new-business price", [
        "3.1 At renewal the premium offered to a customer may not exceed the equivalent new-business price: the "
        "premium Halvergate would quote, on the renewal date, to a new customer with the same risk through the channel "
        "through which the customer was first sold, at the new-business rates then in force.",
        "3.2 The renewal system compares each renewal premium with its equivalent new-business price before the "
        "invitation is issued and reduces the premium to that price where it is higher.",
        "3.3 Compliance attests each quarter to the board that the comparison has been made on every renewal."]),
    ("4. Records", [
        "4.1 The renewal pricing team keeps, for each renewal, the premium intended, the equivalent new-business "
        "price at the date of the schedule and the premium offered."]),
]

COMMISSION = [
    ("Commission on comparison-site sales", [
        "Commission is payable to the site on each policy sold through it, net of policies cancelled within the "
        "14-day cooling-off period. The rates below apply to private car policies from 1 January 2026 and are "
        "unchanged for 2027 under the agreements renewed in September 2026.",
        [["Site", "Per policy sold", "Agreement"],
         ["Kitecompare", "£52.00", "KC-HM-2024-07, renewed 2026-09-12"],
         ["Covertide", "£48.00", "CT/HAL/22, renewed 2026-09-03"],
         ["Brightquote", "£44.00", "BQ-0417, renewed 2026-09-19"],
         ["Pricelark", "£55.00", "PLK-2025-HM, renewed 2026-09-26"]]]),
    ("Invoicing", [
        "Sites invoice monthly in arrears from their own sale records; Finance reconciles each invoice to the policy "
        "system's sales by quote reference before payment."]),
]

XOL = [
    ("2026 programme", [
        "The motor excess of loss programme runs from 1 January 2026 to 31 December 2026 on a losses-occurring "
        "basis and protects the private car and commercial vehicle accounts together.",
        [["Layer", "Cover", "Rate on line"],
         ["1", "£4m xs £1m", "11.8%"],
         ["2", "£10m xs £5m", "3.9%"],
         ["3", "£35m xs £15m", "1.2%"],
         ["4", "Unlimited xs £50m (Pool Re style vertical)", "0.31%"]],
        "Each layer carries one reinstatement at 100 per cent additional premium. Periodical payment orders are "
        "capitalised at the indexation clause's base date of 1 January 2026."]),
    ("Large losses notified to the panel, 2024 to 2026", [
        "Fourteen private car losses were notified to the panel over the three years, all third-party injury, five "
        "of them still open at 30 September 2026. The 2027 renewal is being placed on the same structure with a "
        "retention of £1.25m."]),
]


def write_pdfs(folder):
    _doc(os.path.join(folder, FILES["plan"]),
         "Comparison-site new business: 2027 rate plan, planning basis", PLAN, None,
         [["Document", "PLN-2027-03, issue 2"], ["Owner", "Frances Green, Head of Personal Lines Pricing"],
          ["Approved", "Christopher Smith, Chief Underwriting Officer"], ["Date", "4 November 2026"]],
         author="Halvergate Mutual, Personal Lines Pricing", subject="2027 comparison-site rate plan planning basis",
         footer="PLN-2027-03 issue 2", created=dt.datetime(2026, 11, 3, 16, 41, 7, tzinfo=GMT),
         modified=dt.datetime(2026, 11, 4, 9, 12, 33, tzinfo=GMT))
    _doc(os.path.join(folder, FILES["policy"]), "Renewal pricing policy", POLICY, None,
         [["Document", "CMP-RP-04, issue 3"], ["Owner", "Compliance"], ["Approved", "Board Risk Committee"],
          ["Effective", "1 January 2022, reviewed 16 September 2026"]],
         author="Halvergate Mutual, Compliance", subject="Renewal pricing policy",
         footer="CMP-RP-04 issue 3", created=dt.datetime(2026, 9, 16, 11, 2, 48, tzinfo=BST),
         modified=dt.datetime(2026, 9, 17, 14, 25, 9, tzinfo=BST), producer="LibreOffice 7.6", font="Carlito")
    _doc(os.path.join(folder, FILES["comm"]), "Comparison-site commission schedule 2026", COMMISSION, None,
         [["Document", "PCW-COM-2026"], ["Owner", "Distribution Finance"], ["Issued", "30 September 2026"]],
         author="Halvergate Mutual, Distribution Finance", subject="Comparison-site commission schedule",
         footer="PCW-COM-2026", created=dt.datetime(2026, 9, 30, 10, 14, 52, tzinfo=BST),
         modified=dt.datetime(2026, 9, 30, 15, 38, 6, tzinfo=BST), producer="LibreOffice 24.2", font="DejaVu Sans")
    _doc(os.path.join(folder, FILES["xol"]), "Motor excess of loss reinsurance programme 2026", XOL, None,
         [["Document", "Programme summary"], ["Owner", "Reinsurance and Capital"], ["Date", "14 October 2026"]],
         author="Halvergate Mutual, Reinsurance and Capital", subject="Motor XoL programme summary",
         footer="Reinsurance and Capital", created=dt.datetime(2026, 10, 14, 13, 50, 21, tzinfo=BST),
         modified=dt.datetime(2026, 10, 14, 17, 2, 44, tzinfo=BST), producer="LibreOffice 7.6", font="Caladea")


# ---- workbooks ---------------------------------------------------------------------------------------------------
BOLD = Font(bold=True)
HEAD_FILL = PatternFill("solid", fgColor="DCE3EE")


def _sheet(ws, header, rows, widths=None, fmt=None):
    ws.append(header)
    for c in ws[1]:
        c.font = BOLD
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(list(r))
    if widths:
        for k, w in enumerate(widths):
            ws.column_dimensions[chr(65 + k) if k < 26 else "A" + chr(65 + k - 26)].width = w
    if fmt:
        for col, f in fmt.items():
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for c in row:
                    c.number_format = f
    ws.freeze_panes = "B2"


def quarter_ends(a, b):
    out, y, q = [], a.year, (a.month - 1) // 3 + 1
    while (y, q) <= (b.year, (b.month - 1) // 3 + 1):
        m = q * 3
        out.append(dt.date(y, m, 30 if m in (6, 9) else 31))
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


def write_triangles(path, books):
    """Accident quarter by development quarter, by claim type: cumulative claims notified and cumulative incurred
    (paid plus case estimates, uncapped) as at each quarter end to 30 September 2026."""
    qe = quarter_ends(P.HIST_START, dt.date(2026, 9, 30))
    vals = {(k, d): b.value(d) for k, b in enumerate(books) for d in qe}
    acc_q = lambda o: (dt.date.fromordinal(int(o)).year, (dt.date.fromordinal(int(o)).month - 1) // 3)
    wb = Workbook()
    first = True
    for t in P.CLAIM_TYPES:
        for kind in ("notified", "incurred"):
            ws = wb.active if first else wb.create_sheet()
            first = False
            ws.title = "%s %s" % (t, kind)
            rows = []
            for ai, aq in enumerate(qe):
                a0 = dt.date(aq.year, aq.month - 2, 1).toordinal()
                a1 = aq.toordinal()
                row = ["%dQ%d" % (aq.year, (aq.month - 1) // 3 + 1)]
                for dj, vq in enumerate(qe[ai:]):
                    tot = 0.0
                    for k, b in enumerate(books):
                        rep, paid, case, st = vals[(k, vq)]
                        m = (b.type == t) & (b.acc >= a0) & (b.acc <= a1) & rep
                        tot += m.sum() if kind == "notified" else (paid[m] + case[m]).sum()
                    row.append(int(tot) if kind == "notified" else round(float(tot), 0))
                rows.append(row)
            header = ["Accident quarter"] + ["Dev %d" % (k + 1) for k in range(len(qe))]
            _sheet(ws, header, rows, widths=[16] + [11] * len(qe),
                   fmt={k + 2: "#,##0" for k in range(len(qe))})
    wb.save(path)


def write_retention(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Renewal invitations"
    out = []
    for (d, band, inv, ren) in rows:
        lo = band
        out.append((d.strftime("%Y-%m"), "%+.0f%% to %+.0f%%" % (lo * 100, (lo + 0.02) * 100), inv, ren,
                    round(ren / inv, 4) if inv else None))
    _sheet(ws, ["Invitation month", "Price change on last year", "Invitations", "Renewed", "Retention"], out,
           widths=[16, 24, 13, 11, 11], fmt={3: "#,##0", 4: "#,##0", 5: "0.0%"})
    wb.save(path)


def write_rates(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rate changes"
    rows = []
    for (d, seg, c) in P.RATE_CHANGES:
        note = "with HPM v7.0" if d == P.REFIT else ""
        rows.append((d.isoformat(), P.SEG_LABEL[seg], "All four sites", round(c, 4), note))
    _sheet(ws, ["Effective", "Main driver age", "Sites", "Change to new-business rates", "Note"], rows,
           widths=[13, 16, 15, 26, 18], fmt={4: "+0.0%;-0.0%"})
    wb.save(path)


def write_direct(path, rng):
    """The direct channel's monthly web quotes and sales by segment (a neighbouring channel the plan excludes)."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Direct web"
    rows = []
    for d in world.months(dt.date(2025, 1, 1), P.AS_AT):
        for seg in P.SEGMENTS:
            q = int({"u25": 6100, "mid": 18400, "o65": 7900}[seg] * P.QUOTE_SEASON[d.month - 1]
                    * float(np.exp(rng.normal(0, 0.05))))
            s = int(q * {"u25": 0.071, "mid": 0.096, "o65": 0.132}[seg] * float(np.exp(rng.normal(0, 0.06))))
            prem = {"u25": 1612, "mid": 668, "o65": 597}[seg] * world.sev_index(d) * float(np.exp(rng.normal(0, 0.02)))
            rows.append((d.strftime("%Y-%m"), P.SEG_LABEL[seg], q, s, round(prem, 2)))
    _sheet(ws, ["Month", "Main driver age", "Web quotes", "Sales", "Average written premium"], rows,
           widths=[10, 16, 12, 10, 22], fmt={3: "#,##0", 4: "#,##0", 5: "£#,##0.00"})
    wb.save(path)
