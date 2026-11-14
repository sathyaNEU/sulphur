"""The golden deliverables: Ester Rey's workbook (the 2027 bands and the figures behind them) and her one-page note
to Bernardo Pombo and Magdalena Requena."""
import os

from docx import Document
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import params as P

FILES = {"wb": "paid_channels_2027.xlsx", "note": "paid_channels_2027_note.docx"}
FILL = {"scale": "D9EAD3", "hold": "FFF2CC", "cut": "F4CCCC"}


def _sheet(ws, header, rows, widths, fmts):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE6F0")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        for i, c in enumerate(row):
            if i < len(fmts) and fmts[i]:
                c.number_format = fmts[i]
    ws.freeze_panes = "B2"


def workbook(path, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bands 2027"
    rows = []
    for c in P.ORDER:
        rows.append([c, f["plan_weekly_avg"][c], f["installs_week_2027"][c], f["vpi_2027"][c], f["roas_2027"][c],
                     f["bands"][c].capitalize()])
    _sheet(ws, ["Channel", "2027 plan, average weekly spend (EUR)", "Installs a week at the plan's spend",
                "12-month net revenue per install at the plan's spend (EUR)", "2027 return per euro", "Band"],
           rows, [20, 18, 16, 20, 14, 10], [None, "#,##0", "#,##0", "0.00", "0.00", None])
    for i, c in enumerate(P.ORDER):
        ws.cell(row=i + 2, column=6).fill = PatternFill("solid", fgColor=FILL[f["bands"][c]])
    ws.append([])
    ws.append(["Lines: cut under 0.90, hold from 0.90, scale from 1.20 (growth policy v2, section 3)."])
    w2 = wb.create_sheet("2025 installs")
    rows = []
    for c in P.ORDER:
        rows.append([c, f["installs_2025"][c], f["spend_2025"][c], f["v12_2025"][c], f["roas_2025"][c],
                     f["unrecorded_share_2025"].get(c)])
    _sheet(w2, ["Channel", "Installs bought, 4 Nov 2024 to 2 Nov 2025", "Spend, those weeks (EUR)",
                "12-month net revenue per install (EUR)", "Return per euro at 2025's spend",
                "Share of that revenue not in the billing records"],
           rows, [20, 16, 16, 18, 16, 18], [None, "#,##0", "#,##0", "0.00", "0.00", "0.0%"])
    w3 = wb.create_sheet("Charges not synced")
    w3.append(["Store charges the billing records do not hold, rebuilt against the stores' daily reports"])
    w3["A1"].font = Font(bold=True)
    for k, v in (("Subscriptions last seen still set to renew, no open after the next charge", f["candidates_renewal"]),
                 ("Trials last seen still set to renew, nothing charged on file", f["candidates_trial"]),
                 ("Share of those trials charged at the trial's end", f["trial_end_share"]),
                 ("Monthly continuation of a subscription the app no longer sees", f["silent_q"])):
        w3.append([k, v])
    w3.column_dimensions["A"].width = 78
    w3.column_dimensions["B"].width = 12
    w4 = wb.create_sheet("iOS networks")
    _sheet(w4, ["Network", "Installs (postbacks)", "Share in the attribution export (tracking allowed)",
                "12-month net revenue per install, users who allowed tracking (EUR)",
                "12-month net revenue per install, every install (EUR)"],
           [[c, f["installs_2025"][c], f["consent_share_2025"][c], f["v12_consenters_2025"][c], f["v12_2025"][c]]
            for c in ("Meta iOS", "TikTok iOS")], [14, 14, 18, 22, 22], [None, "#,##0", "0.0%", "0.00", "0.00"])
    wb.save(path)


def note(path, f):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("Paid channels for 2027: bands at the media plan's spend", level=1)
    d.add_paragraph("To Bernardo Pombo and Magdalena Requena, from Ester Rey, 10 November 2026")
    b = f["bands"]
    by = lambda band: [c for c in P.ORDER if b[c] == band]
    d.add_paragraph(
        "Scale Apple Search Ads; hold Meta iOS, Meta Android, Google Android and AppLovin; cut TikTok on both "
        "platforms. Each channel's 2027 return is the 12-month net revenue per euro of the installs its 2027 weekly "
        "spend buys, estimated from the installs we bought between November 2024 and October 2025, whose twelve "
        "months are complete.")
    t = d.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    for i, h in enumerate(["Channel", "Return per euro", "Band", "12-month net revenue per install, 2025 installs"]):
        t.rows[0].cells[i].text = h
    for c in P.ORDER:
        r = t.add_row().cells
        r[0].text = c; r[1].text = "%.2f" % f["roas_2027"][c]; r[2].text = b[c].capitalize()
        r[3].text = "EUR %.2f" % f["v12_2025"][c]
    d.add_paragraph(
        "Three things move the figures from what the dashboards show. Our billing records hold a store charge only "
        "once the subscriber opens the app again, and subscribers who stop opening it keep paying for months: the "
        "stores charged about two fifths more than we recorded, most of it on AppLovin and TikTok, whose "
        "subscribers stop opening soonest, so spreading the stores' excess over every account in proportion would cut "
        "AppLovin wrongly. On iOS, the attribution export holds only users who allowed tracking, who are the more "
        "engaged: Meta iOS's consenting users bring EUR %.2f per install against EUR %.2f over all its installs, read "
        "from the networks' install postbacks. And the plan raises Google Android's weekly spend by about %.0f per cent "
        "over 2025; the 2025 weeks of heavier spend show dearer and weaker installs, which takes its return from "
        "%.2f at 2025's spend to %.2f." % (
            f["v12_consenters_2025"]["Meta iOS"], f["v12_2025"]["Meta iOS"],
            100 * f["google_plan_rise"],
            f["roas_2025"]["Google Android"], f["roas_2027"]["Google Android"]))
    d.add_paragraph("The workbook has each channel's figures and the steps behind them.")
    d.save(path)


def build(folder, f):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), f)
    note(os.path.join(folder, FILES["note"]), f)
