"""The golden deliverables the prompt asks for: a workbook (spring_campaign_2027_plans.xlsx) and a short deck for
the growth committee (spring_campaign_2027.pptx), built from the same objects that write figures.json."""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Emu, Pt

import params as P

BLUE, ORANGE, GREY, INK, MUTED = "2A78D6", "EB6834", "8A8984", "0B0B0B", "52514E"
FILES = {"wb": "spring_campaign_2027_plans.xlsx", "deck": "spring_campaign_2027.pptx"}
PL = ["Flex", "Standaard", "Onbeperkt", "Gezin"]
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="DCE3EE")


def _sheet(ws, header, rows, widths, fmts=None, start=1):
    for j, h in enumerate(header, 1):
        c = ws.cell(row=start, column=j, value=h)
        c.font = BOLD
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(rows, start + 1):
        for j, v in enumerate(r, 1):
            c = ws.cell(row=i, column=j, value=v)
            if fmts and fmts.get(j):
                c.number_format = fmts[j]
    for j, w in enumerate(widths):
        ws.column_dimensions[chr(65 + j)].width = w


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lead plan"
    ws["A1"] = "Spring campaign 2027: contribution per trial start over its first 24 months"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Spring 2024 campaign trial starts (January to March 2024) re-rated at the 2027 prices, VAT and store "
                "fees, less EUR %.2f per counted hour and the agency's fee per trial start (guideline 3.4 to 3.7)."
                % fig["rate"])
    rows = []
    s24, det = fig["spring24"], fig["contribution_detail"]
    for p in PL:
        rows.append([p, fig["spring24_trial_starts"][p], s24["%s share paying" % p] / 100, s24["%s paying months" % p],
                     s24["%s net revenue" % p], det[p]["counted hours"], det[p]["remuneration (EUR)"], fig["fee"][p],
                     fig["contribution"][p]])
    _sheet(ws, ["Plan", "Spring 2024 trial starts", "Share paying after the trial", "Paying months per trial start",
                "Net revenue per trial start at 2027 prices (EUR)", "Counted hours per trial start",
                "Remuneration per trial start (EUR)", "Agency fee per trial start (EUR)",
                "Contribution per trial start (EUR)"], rows, [12, 11, 12, 12, 16, 13, 15, 14, 15],
           {3: "0.0%", 4: "0.00", 5: "#,##0.00", 6: "#,##0.0", 7: "#,##0.00", 8: "#,##0.00", 9: "#,##0.0"}, start=4)
    ws.freeze_panes = "B5"
    ws.cell(row=10, column=1, value="Lead with %s: EUR %.1f per trial start, EUR %.1f ahead of %s." % (
        fig["lead_plan"], fig["contribution"][fig["lead_plan"]], fig["lead_margin_eur"], fig["runner_up"])).font = BOLD

    ws = wb.create_sheet("Base October 2026")
    rows = [[p, fig["paying_oct"][p], fig["counted_per_month"][p]] for p in PL]
    rows.append(["All plans", fig["paying_oct_total"], None])
    ws.freeze_panes = "A2"
    _sheet(ws, ["Plan", "Paying subscriptions at 31 October 2026",
                "Counted hours per paying subscription-month, Nov 2025 to Oct 2026"], rows, [14, 18, 24],
           {3: "0.00"})
    ws.cell(row=8, column=1, value="2027 remuneration on the subscriptions paying at 31 October 2026 (EUR)").font = BOLD
    ws.cell(row=9, column=1, value="Estimate")
    ws.cell(row=9, column=2, value=fig["remuneration_2027_base"]).number_format = "#,##0"
    ws.cell(row=10, column=1, value="Range over the survival and listening forms")
    ws.cell(row=10, column=2, value="%s to %s" % (format(fig["remuneration_2027_band"][0], ","),
                                                  format(fig["remuneration_2027_band"][1], ",")))

    ws = wb.create_sheet("Other readings")
    rows = []
    for nm, r in fig["routes"].items():
        rows.append([nm, r["lead"]] + [r["contribution"][p] for p in PL] + [r["remuneration_2027"]])
    _sheet(ws, ["Reading", "Leads with"] + ["%s (EUR per trial start)" % p for p in PL] +
           ["2027 remuneration, October base (EUR)"], rows, [58, 12, 12, 12, 12, 12, 16],
           {3: "0.0", 4: "0.0", 5: "0.0", 6: "0.0", 7: "#,##0"})

    ws = wb.create_sheet("Notes")
    notes = [
        "Counted hours follow schedule B 2.2 and 2.3: per profile and title, the rise in the furthest position "
        "reported, in the month reported. Positions come from the warehouse's monthly roll-up of live playback and "
        "from the licence server's renewals of downloaded titles; a re-sent roll-up row is counted once.",
        "Each profile's hours go to the account whose charge that month lists it (guideline 3.3); a trial month "
        "takes the account of the profile's first charge.",
        "Own productions and public-domain titles are left out (B2.4). The 2026 statements reproduce from the live "
        "roll-up's streamed seconds, the 2026 basis; they do not hold the 2027 count.",
        "The 2027 remuneration of the October base: survival by plan and paid-tenure band from November 2024 to "
        "October 2026, counted hours per paying month by plan and calendar month from November 2025 to October 2026."]
    for i, n in enumerate(notes, 1):
        c = ws.cell(row=i, column=1, value=n)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 110
    wb.save(path)


def _style(chart, legend=False):
    chart.font.size = Pt(11)
    chart.font.color.rgb = RGBColor.from_string(MUTED)
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False


def deck(path, fig):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, lines, size=16, bold_first=False):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for k, line in enumerate(lines):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.runs[0].font.size = Pt(size)
            p.runs[0].font.color.rgb = RGBColor.from_string(INK)
            p.space_after = Pt(10)
        return tb

    def title(slide, t, sub=None):
        tb = text(slide, 457200, 300000, 11277600, 700000, [t], 24)
        tb.text_frame.paragraphs[0].runs[0].font.bold = True
        if sub:
            q = tb.text_frame.add_paragraph()
            q.text = sub
            q.runs[0].font.size = Pt(13)
            q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
        f = slide.shapes.add_textbox(Emu(457200), Emu(6400000), Emu(10800000), Emu(300000)).text_frame.paragraphs[0]
        f.text = "Billing, warehouse and licence server exports to 31 October 2026; SUL schedule B; growth planning guideline"
        nb = slide.shapes.add_textbox(Emu(11300000), Emu(6400000), Emu(500000), Emu(300000)).text_frame.paragraphs[0]
        nb.text = str(len(prs.slides))
        nb.runs[0].font.size = Pt(9)
        nb.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
        f.runs[0].font.size = Pt(9)
        f.runs[0].font.color.rgb = RGBColor.from_string(MUTED)

    c = fig["contribution"]
    s = prs.slides.add_slide(blank)
    title(s, "Spring campaign 2027: lead with %s" % fig["lead_plan"], "Growth committee, November 2026")
    text(s, 457200, 1500000, 11277600, 4600000, [
        "%s brings EUR %.1f per trial start over its first 24 months, after the publishers' EUR %.2f per counted hour "
        "and the agency's fee; %s EUR %.1f, Standaard EUR %.1f, Onbeperkt EUR %.1f." % (
            fig["lead_plan"], c[fig["lead_plan"]], fig["rate"], "Flex", c["Flex"], c["Standaard"], c["Onbeperkt"]),
        "Not Onbeperkt: its listeners play much of their listening from downloads, which reach us at licence renewal, "
        "and at %.2f counted hours per paying month it costs more than it brings." % fig["counted_per_month"]["Onbeperkt"],
        "The October base: %s paying subscriptions; its 2027 remuneration about EUR %s (EUR %s to %s)." % (
            format(fig["paying_oct_total"], ","), format(fig["remuneration_2027_base"], ","),
            format(fig["remuneration_2027_band"][0], ","), format(fig["remuneration_2027_band"][1], ","))], 17)

    s = prs.slides.add_slide(blank)
    title(s, "%s brings the most per trial start once listening is counted in full" % fig["lead_plan"],
          "Contribution per trial start over its first 24 months, EUR, after remuneration and the agency's fee")
    cd = CategoryChartData()
    cd.categories = PL
    cd.add_series("Contribution", [c[p] for p in PL])
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(4900000),
                            cd).chart
    _style(ch)
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.0"
    pl.data_labels.number_format_is_linked = False
    for i, p in enumerate(PL):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor.from_string(BLUE if p == fig["lead_plan"] else GREY)

    s = prs.slides.add_slide(blank)
    title(s, "Onbeperkt counts the most hours per paying month",
          "Counted hours per paying subscription-month, November 2025 to October 2026")
    cd = CategoryChartData()
    cd.categories = PL
    cd.add_series("Counted hours", [fig["counted_per_month"][p] for p in PL])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1300000), Emu(7000000), Emu(4900000),
                            cd).chart
    _style(ch)
    ch.plots[0].has_data_labels = True
    ch.plots[0].data_labels.number_format = "0.00"
    ch.plots[0].data_labels.number_format_is_linked = False
    text(s, 7800000, 1500000, 3900000, 4600000, ["Paying subscriptions at 31 October 2026:"] +
         ["%s %s" % (p, format(fig["paying_oct"][p], ",")) for p in PL], 15)

    s = prs.slides.add_slide(blank)
    title(s, "Gezin's trial starts pay for the longest",
          "Spring 2024 campaign trial starts, first 24 months, at 2027 prices, VAT and store fees")
    s24 = fig["spring24"]
    rows = [["Plan", "Trial starts", "Share paying", "Paying months", "Net revenue (EUR)"]]
    for p in PL:
        rows.append([p, str(fig["spring24_trial_starts"][p]), "%.1f%%" % s24["%s share paying" % p],
                     "%.2f" % s24["%s paying months" % p], "%.2f" % s24["%s net revenue" % p]])
    tbl = s.shapes.add_table(len(rows), 5, Emu(457200), Emu(1400000), Emu(11277600), Emu(2600000)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            cell = tbl.cell(i, j)
            cell.text = v
            cell.text_frame.paragraphs[0].runs[0].font.size = Pt(15)
    prs.save(path)


def build(folder, fig):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), fig)
    deck(os.path.join(folder, FILES["deck"]), fig)
