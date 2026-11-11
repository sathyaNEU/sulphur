"""The golden deliverables the prompt asks for: a workbook (pcw_rate_review_2027.xlsx) and a few slides for the
executive pricing team (pricing_committee_2027_rates.pptx), built from the same objects that write figures.json."""
import datetime as dt
import os
import sys

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.util import Emu, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import methods as M  # noqa: E402

BLUE, ORANGE, GREY, INK, MUTED = "2A78D6", "EB6834", "8A8984", "0B0B0B", "52514E"
FILES = {"wb": "pcw_rate_review_2027.xlsx", "deck": "pricing_committee_2027_rates.pptx"}
SEG_NAME = {"u25": "Under 25", "mid": "25 to 64", "o65": "65 and over"}
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="DCE3EE")


def curves(GD):
    D, S = GD["D"], GD["S"]
    sc = {g: G.shortcuts(D, S, g) for g in ("u25", "mid")}
    out = {}
    for g, top in (("u25", 30), ("mid", 20)):
        rows = []
        for k in range(0, top + 1):
            L = k / 100.0
            rows.append((k, S[g]["lr"](L), sc[g]["loss-ratio method, latest twelve months"](L),
                         sc[g]["loss-ratio method, 2026 to date"](L), sc[g]["loss-ratio method, 2025 and 2026 pooled"](L)))
        out[g] = rows
    return out, sc


def windows(fig):
    return [tuple(w) for w in fig["mid_windows"]]


def _sheet(ws, header, rows, widths, fmts=None):
    ws.append(header)
    for c in ws[1]:
        c.font = BOLD
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(list(r))
    for k, w in enumerate(widths):
        ws.column_dimensions[chr(65 + k)].width = w
    for col, f in (fmts or {}).items():
        for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
            for c in row:
                c.number_format = f


def wb_basis(wb, fig):
    """The basis the figures were built on, as the planning paper and the extracts set it."""
    c = fig["constants"]
    ws = wb.create_sheet("Basis")
    lines = [
        "Records as at 31 October 2026: the four sites' quote extracts, the policy extract and the claims extract; "
        "the reserving triangles to 30 September 2026.",
        "Loss ratio: ultimate claims, each capped at £%s, at 2027 cost levels (2026 claims raised %.1f per cent), "
        "over written premium net of insurance premium tax (PLN-2027-03 2.1 and 2.2)." % (format(c["cap"], ","),
                                                                                          c["inflation"]),
        "2027 business: the quotes returned from 1 February 2026 to 31 October 2026, scaled to twelve months, each "
        "replayed at its 2027 price against its three cheapest rivals raised %d per cent, and sold at the conversion "
        "its new rank carries on those quotes (PLN-2027-03 4.1 and 4.2)." % c["market"],
        "Experience: the business sold since the last rate change on 1 February 2026 (for 25 to 64, all the business "
        "HPM v7 has priced), each earned month weighted by its claims season; claims not yet notified valued at "
        "their type's mean cost.",
        "Selection: claims per predicted claim against the gap between our price and the cheapest rival's, on "
        "2025 and 2026 sales (25 to 64: HPM v7 sales), claims to 30 September 2026.",
        "Change: the smallest whole per cent at which the expected 2027 loss ratio is 75 per cent or below "
        "(PLN-2027-03 5.1); the range is the 10th to 90th percentile of %s draws of the year's policies and "
        "claims (5.2)." % format(c["draws"], ","),
        "Underwriting profit: premium net of IPT less capped claims, the site's commission on each sale "
        "(PCW-COM-2026) and £%d servicing a policy, on 2027 new business and on the 2027 renewal schedule, whose "
        "offered premiums may not exceed the equivalent new-business price (CMP-RP-04 3.1)." % c["servicing"],
        "Quotes the sites did not sell are sampled one in %d in their extracts and counted at that weight; the "
        "sites' ZZ99 monitoring quotes and Covertide's quotes of 14 May 2026 sent a second time are left out."
        % c["extract_weight"],
    ]
    ws.append(["Basis of this review"])
    ws["A1"].font = Font(bold=True, size=12)
    for line in lines:
        ws.append([line])
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 120


def workbook(path, fig, GD, cv, win):
    S, cut = GD["S"], GD["cut"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Calls"
    ws.append(["2027 comparison-site new-business rates: the executive pricing team's decision"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Segment", "2027 change", "Expected 2027 loss ratio", "2027 policies", "2027 written premium (£m)",
               "Note"])
    for c in ws[3]:
        c.font = BOLD
        c.fill = HEAD
    ws.append(["Under 25", fig["u25_rise"] / 100.0, round(fig["u25_lr_at_rise"] / 100.0, 4), fig["u25_policies_at_rise"],
               fig["u25_premium_at_rise_m"], "Rise; the team's +%d%% leaves the loss ratio at %.1f%%" %
               (fig["constants"]["proposal_u25"], fig["u25_lr_at_proposal"])])
    ws.append(["25 to 64", fig["mid_rise"] / 100.0, round(fig["mid_lr_at_rise"] / 100.0, 4), fig["mid_policies_at_rise"],
               fig["mid_premium_at_rise_m"], "80%% range on the loss ratio %.1f%% to %.1f%%" % (fig["mid_range_lo"],
                                                                                             fig["mid_range_hi"])])
    ws.append(["65 and over", 0.0, None, fig["o65_policies_at_hold"], None,
               "Hold: the 3%% cut would lower 2027 underwriting profit by £%.2fm" % fig["cut_net_loss_m"]])
    for r in range(4, 7):
        ws.cell(r, 2).number_format = "+0%;-0%;0%"
        ws.cell(r, 3).number_format = "0.0%"
        ws.cell(r, 4).number_format = "#,##0"
        ws.cell(r, 5).number_format = "0.0"
    for k, w in enumerate([14, 12, 22, 14, 24, 62]):
        ws.column_dimensions[chr(65 + k)].width = w
    ws.append([])
    ws.append(["Proposals", "Change", "2027 policies", "2027 loss ratio"])
    for c in ws[8]:
        c.font = BOLD
        c.fill = HEAD
    ws.append(["Under 25, the team's rise", fig["constants"]["proposal_u25"] / 100.0, fig["u25_policies_at_proposal"],
               round(fig["u25_lr_at_proposal"] / 100.0, 4)])
    ws.append(["65 and over, the proposed cut", -0.03, fig["o65_policies_at_cut"], None])
    for r in (9, 10):
        ws.cell(r, 2).number_format = "+0%;-0%"
        ws.cell(r, 3).number_format = "#,##0"
        ws.cell(r, 4).number_format = "0.0%"

    w2 = wb.create_sheet("Under 25")
    _sheet(w2, ["Rise", "Expected 2027 loss ratio", "Loss-ratio method, latest twelve months", "Target"],
           [(k / 100.0, round(a, 4), round(b, 4), 0.75) for (k, a, b, c, d) in cv["u25"]], [10, 24, 34, 10],
           {1: "+0%", 2: "0.0%", 3: "0.0%", 4: "0%"})
    r0 = len(cv["u25"]) + 3
    w2.cell(r0, 1, "Claims per predicted claim by price gap to the cheapest rival, under-25 sales January 2025 to "
                   "October 2026 (deciles, deepest first)").font = BOLD
    info = S["u25"]["info"]
    w2.cell(r0 + 1, 1, "Decile").font = BOLD
    w2.cell(r0 + 1, 2, "Mean gap (log of our price over the cheapest rival)").font = BOLD
    w2.cell(r0 + 1, 3, "Claims per predicted claim").font = BOLD
    for k, (x, y) in enumerate(zip(info["x"], info["y"])):
        w2.cell(r0 + 2 + k, 1, k + 1)
        w2.cell(r0 + 2 + k, 2, round(float(x), 4))
        w2.cell(r0 + 2 + k, 3, round(float(y), 3))

    w3 = wb.create_sheet("25 to 64")
    _sheet(w3, ["Rise", "Expected 2027 loss ratio", "Loss-ratio method, latest twelve months",
                "Loss-ratio method, v7 business to date", "Loss-ratio method, 2025 and 2026 pooled", "Target"],
           [(k / 100.0, round(a, 4), round(b, 4), round(c, 4), round(d, 4), 0.75) for (k, a, b, c, d) in cv["mid"]],
           [10, 24, 30, 30, 30, 10],
           {1: "+0%", 2: "0.0%", 3: "0.0%", 4: "0.0%", 5: "0.0%", 6: "0%"})
    r0 = len(cv["mid"]) + 3
    w3.cell(r0, 1, "Which experience represents the 2027 book").font = BOLD
    w3.cell(r0 + 1, 1, "Experience").font = BOLD
    w3.cell(r0 + 1, 2, "2026 loss ratio").font = BOLD
    w3.cell(r0 + 1, 3, "Smallest rise to 75%, the same replay").font = BOLD
    for k, (name, b, rise) in enumerate(win):
        w3.cell(r0 + 2 + k, 1, name)
        c = w3.cell(r0 + 2 + k, 2, round(b, 4))
        c.number_format = "0.0%"
        w3.cell(r0 + 2 + k, 3, rise)
    r1 = r0 + 3 + len(win)
    w3.cell(r1, 1, "Claims cost per unit of earned premium by calendar month, against the year's average").font = BOLD
    for m in range(12):
        w3.cell(r1 + 1 + m, 1, dt.date(2026, m + 1, 1).strftime("%B"))
        w3.cell(r1 + 1 + m, 2, round(float(GD["D"]["s_cost"][m]), 3))

    w4 = wb.create_sheet("Over 65 cut")
    w4.append(["The proposed 3% over-65 cut, 2027 underwriting profit (£m)", "Hold", "Cut", "Change"])
    for c in w4[1]:
        c.font = BOLD
        c.fill = HEAD
    w4.append(["Comparison-site new business", fig["cut_nb0_m"], fig["cut_nb1_m"], fig["cut_nb_m"]])
    w4.append(["Renewals of customers first sold through a site", fig["cut_rp0_m"], fig["cut_rp1_m"], fig["cut_ren_m"]])
    w4.append(["Total", round(fig["cut_nb0_m"] + fig["cut_rp0_m"], 2), round(fig["cut_nb1_m"] + fig["cut_rp1_m"], 2),
               fig["cut_net_m"]])
    w4.append([])
    w4.append(["2027 new-business policies", fig["o65_policies_at_hold"], fig["o65_policies_at_cut"], None])
    w4.append(["Renewal retention", round(cut["ret0"], 4), round(cut["ret1"], 4), None])
    for r in (2, 3, 4):
        for cc in (2, 3):
            w4.cell(r, cc).number_format = "0.00"
        w4.cell(r, 4).number_format = "+0.00;-0.00"
    for r in (6,):
        for cc in (2, 3):
            w4.cell(r, cc).number_format = "#,##0"
    for cc in (2, 3):
        w4.cell(7, cc).number_format = "0.0%"
    w4.column_dimensions["A"].width = 52
    for col in "BCD":
        w4.column_dimensions[col].width = 12

    w5 = wb.create_sheet("2026 by segment")
    rows = []
    for g in M.SEGS:
        q, s, cvr = GD["r1"][g]
        rows.append((SEG_NAME[g], q, s, cvr))
    _sheet(w5, ["Main driver age", "Quotes priced, January to October 2026", "Sales", "Conversion"], rows,
           [16, 34, 10, 12], {2: "#,##0", 3: "#,##0", 4: "0.00%"})

    w6 = wb.create_sheet("Routes")
    rt = [("This review", "+%d%%" % fig["u25_rise"], "+%d%%" % fig["mid_rise"], "Hold"),
          ("Loss-ratio method on the latest twelve months", "+%d%%" % fig["careful_u25_rise"],
           "+%d%%" % fig["careful_mid_rise"], "Cut (new business +£%.2fm)" % fig["cut_nb_only_m"]),
          ("2026 written business to date, as it stands", "+%d%%" % fig["todate_u25_rise"],
           "+%d%%" % fig["todate_mid_rise"], "Cut"),
          ("Loss-ratio method on the latest twelve months, the triangles' chain ladder",
           "+%d%%" % fig["careful_cl_u25_rise"], "+%d%%" % fig["careful_cl_mid_rise"], "Cut"),
          ("Current book over a full year, the won business unchanged", "+%d%%" % fig["completed_u25_rise"],
           "+%d%%" % fig["completed_mid_rise"], "Hold"),
          ("2025 and 2026 pooled on level", "+%d%%" % fig["pooled_u25_rise"], "+%d%%" % fig["pooled_mid_rise"], "Cut")]
    _sheet(w6, ["Route", "Under 25", "25 to 64", "65 and over"], rt, [58, 12, 12, 30])
    wb_basis(wb, fig)
    wb.save(path)


def _chart_style(chart, legend=True):
    chart.font.size = Pt(11)
    chart.font.color.rgb = RGBColor.from_string(MUTED)
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False


def deck(path, fig, GD, cv, win):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]

    def footer(slide, n):
        tb = slide.shapes.add_textbox(Emu(457200), Emu(6400000), Emu(10500000), Emu(300000))
        p = tb.text_frame.paragraphs[0]
        p.text = ("Source: comparison-site quote extracts, policy and claims extracts as at 31 October 2026; "
                  "planning basis PLN-2027-03")
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
        nb = slide.shapes.add_textbox(Emu(11100000), Emu(6400000), Emu(600000), Emu(300000))
        q = nb.text_frame.paragraphs[0]
        q.text = str(n)
        q.runs[0].font.size = Pt(9)
        q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)

    def title(slide, text, sub=None):
        footer(slide, len(prs.slides))
        tb = slide.shapes.add_textbox(Emu(457200), Emu(300000), Emu(11277600), Emu(700000))
        p = tb.text_frame.paragraphs[0]
        p.text = text
        p.runs[0].font.size = Pt(24)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor.from_string(INK)
        if sub:
            q = tb.text_frame.add_paragraph()
            q.text = sub
            q.runs[0].font.size = Pt(13)
            q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)

    s = prs.slides.add_slide(blank)
    title(s, "2027 comparison-site new-business rates", "Executive pricing team, December 2026")
    tb = s.shapes.add_textbox(Emu(457200), Emu(1500000), Emu(11277600), Emu(4600000))
    tf = tb.text_frame
    tf.word_wrap = True
    pu = fig["constants"]["proposal_u25"]
    lines = ["Under 25: raise %d%%, not the %d%% proposed. At +%d%% the business we would win runs at %.1f%%; at +%d%% "
             "it runs at %.1f%% on about %s policies." % (fig["u25_rise"], pu, pu, fig["u25_lr_at_proposal"],
                                                         fig["u25_rise"], fig["u25_lr_at_rise"],
                                                         format(fig["u25_policies_at_rise"], ",")),
             "25 to 64: raise %d%% (2027 loss ratio %.1f%%, 80%% range %.1f%% to %.1f%%), on the business HPM v7 has "
             "priced over a full year." % (fig["mid_rise"], fig["mid_lr_at_rise"], fig["mid_range_lo"],
                                          fig["mid_range_hi"]),
             "65 and over: hold. The 3%% cut adds £%.2fm on new business and costs £%.2fm on renewals, £%.2fm less in all."
             % (fig["cut_nb_m"], fig["cut_ren_loss_m"], fig["cut_net_loss_m"])]
    for k, line in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text = line
        p.runs[0].font.size = Pt(17)
        p.space_after = Pt(14)

    s = prs.slides.add_slide(blank)
    title(s, "Under 25: the rise has to clear more than the experience suggests",
          "Expected 2027 loss ratio of the business each rise would win")
    cd = CategoryChartData()
    cd.categories = ["+%d%%" % r[0] for r in cv["u25"]]
    cd.add_series("Business the rise would win", [round(r[1], 4) for r in cv["u25"]])
    cd.add_series("Latest twelve months, book unchanged", [round(r[2], 4) for r in cv["u25"]])
    cd.add_series("Target", [0.75] * len(cv["u25"]))
    ch = s.shapes.add_chart(XL_CHART_TYPE.LINE, Emu(457200), Emu(1300000), Emu(11277600), Emu(5200000), cd).chart
    _chart_style(ch)
    for ser, col, width in zip(ch.series, (BLUE, ORANGE, GREY), (2.25, 2.25, 1.25)):
        ser.format.line.color.rgb = RGBColor.from_string(col)
        ser.format.line.width = Pt(width)
        ser.smooth = False
    ch.value_axis.tick_labels.number_format = "0%"
    ch.value_axis.tick_labels.number_format_is_linked = False
    vals = [v for r in cv["u25"] for v in (r[1], r[2])]
    ch.value_axis.minimum_scale = np.floor(min(vals) * 20) / 20
    ch.value_axis.maximum_scale = np.ceil(max(vals) * 20) / 20
    ch.value_axis.major_unit = 0.05
    ch.value_axis.major_gridlines.format.line.color.rgb = RGBColor.from_string("E6E5E1")

    s = prs.slides.add_slide(blank)
    title(s, "Under 25: we sell where our price undercuts the market most",
          "Claims per predicted claim, by how far below the cheapest rival we priced (sales January 2025 to October 2026)")
    info = GD["S"]["u25"]["info"]
    cd = CategoryChartData()
    cd.categories = ["%d%% below" % round(-100 * (np.exp(x) - 1)) if x < 0 else "%d%% above" % round(100 * (np.exp(x) - 1))
                     for x in info["x"]]
    cd.add_series("Claims per predicted claim", [round(float(y), 3) for y in info["y"]])
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(5200000),
                            cd).chart
    _chart_style(ch, legend=False)
    ch.series[0].format.fill.solid()
    ch.series[0].format.fill.fore_color.rgb = RGBColor.from_string(BLUE)
    ch.value_axis.major_gridlines.format.line.color.rgb = RGBColor.from_string("E6E5E1")
    ch.value_axis.tick_labels.number_format = "0.00"
    ch.value_axis.tick_labels.number_format_is_linked = False

    s = prs.slides.add_slide(blank)
    title(s, "25 to 64: only the business HPM v7 priced represents 2027",
          "Smallest rise to a 75% loss ratio through the same replay, by the experience it is read from (orange: "
          "experience that carries HPM v6 business or has not yet seen its winter)")
    cd = CategoryChartData()
    cd.categories = [w[0] for w in win]
    cd.add_series("Smallest rise (per cent)", [w[2] for w in win])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(5200000),
                            cd).chart
    _chart_style(ch, legend=False)
    ch.series[0].format.fill.solid()
    ch.series[0].format.fill.fore_color.rgb = RGBColor.from_string(BLUE)
    for k, pt in enumerate(ch.series[0].points):
        if k >= 1:
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = RGBColor.from_string(ORANGE)
    ch.plots[0].has_data_labels = True
    ch.plots[0].data_labels.number_format = "0"
    ch.plots[0].data_labels.number_format_is_linked = False
    ch.value_axis.major_gridlines.format.line.color.rgb = RGBColor.from_string("E6E5E1")

    s = prs.slides.add_slide(blank)
    title(s, "65 and over: the cut costs more on renewals than it earns on new business",
          "Change in 2027 underwriting profit from the 3% cut, £m")
    cd = CategoryChartData()
    cd.categories = ["New business", "Renewals", "Total"]
    cd.add_series("Change, £m", [fig["cut_nb_m"], fig["cut_ren_m"], fig["cut_net_m"]])
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(5200000),
                            cd).chart
    _chart_style(ch, legend=False)
    ch.series[0].format.fill.solid()
    ch.series[0].format.fill.fore_color.rgb = RGBColor.from_string(BLUE)
    ch.series[0].invert_if_negative = False
    ch.plots[0].has_data_labels = True
    ch.plots[0].data_labels.number_format = "+0.00;-0.00"
    ch.plots[0].data_labels.number_format_is_linked = False
    ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ch.value_axis.major_gridlines.format.line.color.rgb = RGBColor.from_string("E6E5E1")
    prs.save(path)


def build(folder, fig, GD):
    os.makedirs(folder, exist_ok=True)
    cv, sc = curves(GD)
    win = windows(fig)
    workbook(os.path.join(folder, FILES["wb"]), fig, GD, cv, win)
    deck(os.path.join(folder, FILES["deck"]), fig, GD, cv, win)
    return cv, win
