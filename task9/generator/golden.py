"""task9: the golden deliverables the prompt asks for (a few slides for the committee and a spreadsheet), written from
the figures as stated (F). Nothing is typed: every number below is read from F.

    write_all(F, golden_dir)

The deck and the workbook pass through the house container writers, each with its own stamps after the pack's.
"""
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

import params as P
import postprocess as PP

DECK, BOOK = "Harbourne_2027_plan_review.pptx", "Harbourne_2027_plan_workbook.xlsx"
AUTHOR = "Portfolio Analytics"
STAMPS = {BOOK: ("2026-11-10T14:06:31Z", "2026-11-11T19:41:52Z"), DECK: ("2026-11-11T13:20:00Z", "2026-11-11T21:07:00Z")}
INK, INK2 = RGBColor(0x0B, 0x0B, 0x0B), RGBColor(0x52, 0x51, 0x4E)
BLUE, ORANGE, GRAY = RGBColor(0x2A, 0x78, 0xD6), RGBColor(0xEB, 0x68, 0x34), RGBColor(0x7D, 0x7B, 0x76)
HEAD_FILL = PatternFill("solid", fgColor="E9EEF4")
THIN = Side(style="thin", color="B8BEC6")


NUMBER = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def kinds(F, pods):
    """The strategy groups a set of increases belongs to, as words ("credit and currency")."""
    word = {"Credit": "credit", "Currencies": "currency", "Equity long/short": "equity", "Quantitative equity": "quantitative equity",
            "Rates": "rates", "Commodities": "commodity", "Volatility": "volatility"}
    g = []
    for x in F["increases"]:
        if x["pod"] in pods and word[x["group"]] not in g:
            g.append(word[x["group"]])
    return g[0] if len(g) == 1 else ", ".join(g[:-1]) + " and " + g[-1]


def m(v):
    """USD millions as the committee reads them."""
    return "USD %s million" % "{:,.0f}".format(v)


def mb(v):
    return ("USD %.2f billion" % (v / 1000.0)) if v >= 1000 else m(v)


def pct(v, k=1):
    return ("%." + str(k) + "f%%") % v


def joined(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


# ------------------------------------------------------------------------------------------------------ workbook
def _head(ws, row, labels, widths=None):
    for j, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=t)
        c.font = Font(bold=True, size=10)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(size=10, color="52514E")


def _row(ws, r, vals, fmts=None, bold=False):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=j, value=v)
        f = (fmts or {}).get(j)
        if f:
            c.number_format = f
        if bold:
            c.font = Font(bold=True)
        if isinstance(v, str) and len(v) > 44:
            c.alignment = Alignment(wrap_text=True, vertical="top")


def write_workbook(path, F):
    wb = openpyxl.Workbook()
    usd, p2 = "#,##0.0", "0.00"
    pl = F["platform"]
    # 1. the plan
    ws = wb.active
    ws.title = "2027 plan"
    _title(ws, "Draft 2027 allocation plan: expected net P&L and the increases that fall short",
           "Record to %s. USD millions. Markets expected to earn nothing (policy 8a); net of funding, PM payouts and platform costs." %
           dt.date.fromisoformat(F["record"]["last"]).strftime("%-d %B %Y"))
    _head(ws, 4, ["Item", "USD m", "Note"], [46, 12, 70])
    rows = [("Expected 2027 net P&L at the draft plan", F["R4_net"], "%d pods, %s of capital" % (pl["pods"], mb(pl["capital_2027"]))),
            ("80% range: 10th percentile", F["R5_range"]["P10"], "Year's net P&L, markets resampled from the record a quarter at a time"),
            ("80% range: 90th percentile", F["R5_range"]["P90"], None),
            ("Pods' expected trading P&L", pl["trade"], "Alpha at each pod's 2027 capital, after the drawdown rules"),
            ("Funding charge", -pl["funding"], "Bill rate %.2f%% on the review date, plus 0.35%%, on 20%% of capital" % pl["bill"]),
            ("PM payouts", -pl["payouts"], "18% of each pod's positive year, pod by pod"),
            ("Platform costs (2027 budget)", -pl["costs"], None)]
    for k, (a, b, c) in enumerate(rows):
        _row(ws, 5 + k, [a, b, c], {2: usd}, bold=(k == 0))
    r0 = 5 + len(rows) + 1
    _row(ws, r0, ["Increases that do not earn the 1.5% hurdle", None, joined(F["R6_fail"])], bold=True)
    _row(ws, r0 + 1, ["Borderline (inside the spread of sound methods)", None, joined(F["R6_either"]) if F["R6_either"] else "None"])
    _row(ws, r0 + 2, ["Capital those increases add", round(sum(x["added"] for x in F["increases"] if x["pod"] in F["R6_fail"]), 1),
                      "Their expected net P&L added: %s" % m(sum(x["added_net"] for x in F["increases"] if x["pod"] in F["R6_fail"])).replace("USD ", "USD ")], {2: usd})
    _row(ws, r0 + 3, ["Expected 2027 net P&L without those increases", F["R7_net"], None], {2: usd})
    _row(ws, r0 + 5, ["A pod's alpha per dollar falls by this share when its capital doubles", F["R3_fall"] / 100.0,
                      "Read within pods (pod-years, constant elasticity); across pods the record shows %s" % pct(F["R3_rivals"]["pooled"])],
         {2: "0.0%"})
    _row(ws, r0 + 6, ["Draft priced the way past plans were", F["quick"]["mean"], "Each pod's 3-year return on capital times its 2027 capital"], {2: usd})
    ws.freeze_panes = "A5"
    # 2. the increases
    wi = wb.create_sheet("Increases")
    _title(wi, "The draft's increases: expected net P&L per dollar added", "Hurdle 1.5% a year after the pod's payout and funding (policy 9).")
    _head(wi, 4, ["Pod", "Strategy group", "Capital 2026 (USD m)", "Capital 2027 (USD m)", "Added (USD m)", "Net P&L added (USD m)",
                  "Per dollar added (% a year)", "Call"], [10, 22, 13, 13, 11, 13, 13, 30])
    calls = {"fails": "Below hurdle", "passes": "Clears hurdle", "either way": "Borderline"}
    for k, x in enumerate(sorted(F["increases"], key=lambda x: x["per_dollar"])):
        _row(wi, 5 + k, [x["pod"], x["group"], x["k2026"], x["k2027"], x["added"], x["added_net"], x["per_dollar"] / 100.0, calls[x["call"]]],
             {3: usd, 4: usd, 5: usd, 6: "#,##0.00", 7: "0.00%"})
    wi.freeze_panes = "A5"
    # 3. the groups
    wg = wb.create_sheet("Strategy groups")
    _title(wg, "Alpha and risk by strategy group, January 2017 to %s" % dt.date.fromisoformat(F["record"]["last"]).strftime("%B %Y"),
           "Alpha: P&L beyond a passive holding of the group's markets (carry included), per cent of capital a year.")
    _head(wg, 4, ["Strategy group", "Alpha a year (%)", "Risk model's specific P&L a year (%)", "Return on capital, nothing taken out (%)"],
          [24, 13, 18, 18])
    for k, g in enumerate(F["R1_alpha"]):
        _row(wg, 5 + k, [g, F["R1_alpha"][g] / 100.0, F["R1_risk_model"][g] / 100.0, F["R1_raw"][g] / 100.0], {2: "0.00%", 3: "0.00%", 4: "0.00%"})
    wg.freeze_panes = "A5"
    # 4. the pods
    wp = wb.create_sheet("Pods 2027")
    _title(wp, "Every pod in the draft: what to expect of it in 2027", "Edge at USD 150 million is the pod's own record pulled toward its group's by how much the group's pods really differ.")
    _head(wp, 4, ["Pod", "Strategy group", "Change", "Capital 2026 (USD m)", "Capital 2027 (USD m)", "Edge at USD 150m (%)", "Alpha at 2027 capital (%)",
                  "Trading P&L (USD m)", "Funding (USD m)", "Payout (USD m)", "Net (USD m)"], [10, 22, 12, 12, 12, 12, 12, 12, 11, 11, 11])
    lab = {"increase": "Increase", "decrease": "Decrease", "unchanged": "No change", "onboarding": "Onboarding"}
    for k, x in enumerate(F["pods"]):
        _row(wp, 5 + k, [x["pod"], x["group"], lab[x["change"]], x["k2026"], x["k2027"], x["edge_c0"] / 100.0, x["alpha_2027"] / 100.0,
                         x["trade"], -x["funding"], -x["payout"], x["net"]],
             {4: usd, 5: usd, 6: "0.00%", 7: "0.00%", 8: "#,##0.00", 9: "#,##0.00", 10: "#,##0.00", 11: "#,##0.00"})
    wp.freeze_panes = "A5"
    # 5. sensitivity
    wsn = wb.create_sheet("Sensitivity")
    _title(wsn, "How the expected figure moves with each judgment behind it", "Each line changes one judgment from the plan's and keeps the rest.")
    _head(wsn, 4, ["Taken instead", "Expected net P&L (USD m)", "10th percentile", "90th percentile", "Increases below hurdle"], [58, 14, 12, 12, 40])
    _row(wsn, 5, ["The plan (as on the first sheet)", F["R4_net"], F["R5_range"]["P10"], F["R5_range"]["P90"], joined(F["R6_fail"])], {2: usd, 3: usd, 4: usd}, bold=True)
    sens = [("Alpha read on the risk model's factors (carry left in)", "risk model's factors"),
            ("Each pod's own record taken as its edge", "each pod's own record"),
            ("Capacity read across pods", "capacity across pods"),
            ("Drawdown rules left out of the year", "no drawdown rules"),
            ("Markets resampled a day at a time", "daily resampling"),
            ("Each increase judged on the pod's net return at its new size", "average return at the new size")]
    for k, (a, key) in enumerate(sens):
        r = F["routes"][key]
        _row(wsn, 6 + k, [a, r["mean"], r["p10"], r["p90"], joined(r["fail"]) if r["fail"] else "None"], {2: usd, 3: usd, 4: usd})
    k = 6 + len(sens)
    for a, v in F["R4_rivals"].items():
        _row(wsn, k, ["Sound alternative: " + a, v], {2: usd})
        k += 1
    wb.save(path)
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, STAMPS[BOOK][0], STAMPS[BOOK][1], excel=True, company=P.PLATFORM_LEGAL)


# ------------------------------------------------------------------------------------------------------ deck
W16, H9 = Emu(12192000), Emu(6858000)


def _text(slide, x, y, w, h, paras, size=16, color=INK, bold_first=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for k, t in enumerate(paras):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text = t
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.bold = bold_first and k == 0
        p.space_after = Pt(8)
    return tb


def _title_of(slide, text):
    slide.shapes.title.text = text
    tf = slide.shapes.title.text_frame
    for p in tf.paragraphs:
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = INK
        p.alignment = PP_ALIGN.LEFT


def _source(slide, text):
    _text(slide, Inches(0.6), Inches(6.85), Inches(12.1), Inches(0.4), [text], size=10, color=INK2)


def write_deck(path, F):
    pr = Presentation()
    pr.slide_width, pr.slide_height = W16, H9
    blank_title = pr.slide_layouts[5]
    last = dt.date.fromisoformat(F["record"]["last"]).strftime("%-d %B %Y")
    pl = F["platform"]
    fail = F["R6_fail"]
    fail_added = sum(x["added"] for x in F["increases"] if x["pod"] in fail)
    # 1. the answer
    s = pr.slides.add_slide(pr.slide_layouts[5])
    _title_of(s, "Plan %s of net P&L for 2027, and drop %s %s increases" % (m(F["R4_net"]), NUMBER.get(len(fail), str(len(fail))), kinds(F, fail)))
    _text(s, Inches(0.6), Inches(1.6), Inches(12.1), Inches(4.8), [
        "Expected 2027 net P&L at the draft plan: %s after funding, PM payouts and platform costs; four years in five between %s and %s." % (
            m(F["R4_net"]), m(F["R5_range"]["P10"]), mb(F["R5_range"]["P90"])),
        "%s of the draft's %d increases add less than 1.5%% a year on the money they add: %s, %s pods with %s of capital between them. "
        "Without them the plan expects %s." % (NUMBER.get(len(fail), str(len(fail))).capitalize(), pl["increases"], joined(fail), kinds(F, fail),
                                               m(fail_added), m(F["R7_net"])),
        "Priced the way past plans were (each pod's three-year return on capital times its new capital), the draft would show %s. That figure "
        "counts market and carry returns as the pods' own, assumes a pod earns as much per dollar at its new size, and takes the luckiest "
        "records at face value." % mb(F["quick"]["mean"]),
    ], size=17)
    _source(s, "Record to %s; %s simulated plan years; Capital Review Policy as approved 14 October 2026." % (last, "{:,}".format(pl["sims"])))
    # 2. where the figure comes from
    s = pr.slides.add_slide(blank_title)
    _title_of(s, "Most of the pods' expected alpha goes to funding, payouts and costs")
    cd = CategoryChartData()
    cats = ["Pods' trading P&L", "Funding", "PM payouts", "Platform costs", "Net P&L"]
    steps = [pl["trade"], -pl["funding"], -pl["payouts"], -pl["costs"]]
    base, run = [], 0.0
    for v in steps:
        base.append(run if v >= 0 else run + v)
        run += v
    base.append(0.0)
    vals = [abs(v) for v in steps] + [F["R4_net"]]
    cd.categories = cats
    cd.add_series("base", [round(b, 1) for b in base])
    cd.add_series("USD m", [round(v, 1) for v in vals])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(0.6), Inches(1.5), Inches(8.2), Inches(5.1), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.plots[0].gap_width = 70
    ch.plots[0].overlap = 100
    ser_base, ser = ch.series[0], ch.series[1]
    ser_base.format.fill.background()
    ser_base.format.line.fill.background()
    for k, pt in enumerate(ser.points):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = BLUE if k in (0, len(vals) - 1) else GRAY
    ser.data_labels.show_value = True
    ser.data_labels.number_format = '#,##0'
    ser.data_labels.number_format_is_linked = False
    ser.data_labels.position = XL_LABEL_POSITION.INSIDE_END
    ser.data_labels.font.size = Pt(12)
    ser.data_labels.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xE3, 0xE2, 0xDE)
    va.tick_labels.font.size = Pt(11)
    va.tick_labels.font.color.rgb = INK2
    va.tick_labels.number_format = '#,##0'
    va.tick_labels.number_format_is_linked = False
    ch.category_axis.tick_labels.font.size = Pt(11)
    ch.category_axis.tick_labels.font.color.rgb = INK2
    _text(s, Inches(9.1), Inches(1.6), Inches(3.7), Inches(5.0), [
        "USD millions, expected values for 2027.",
        "Trading P&L is each pod's alpha at its 2027 capital, after the drawdown rules halve or close the pods that hit them; markets are expected to earn nothing (policy 8a).",
        "Payouts are 18%% of each pod's own positive year, so a losing pod still costs nothing while a winning one pays: %s, %.0f%% of trading P&L after funding." % (
            m(pl["payouts"]), 100.0 * pl["payouts"] / (pl["trade"] - pl["funding"])),
    ], size=13, color=INK2)
    _source(s, "Funding at the bill rate on the review date (%.2f%%) plus 0.35%% on 20%% of capital; platform costs from the 2027 budget." % pl["bill"])
    # 3. the hurdle
    s = pr.slides.add_slide(blank_title)
    _title_of(s, "The %s increases fall short of the 1.5%% hurdle" % kinds(F, fail))
    inc = sorted(F["increases"], key=lambda x: x["per_dollar"])
    cd = CategoryChartData()
    cd.categories = [x["pod"] for x in inc]
    cd.add_series("Net P&L per dollar added (% a year)", [round(x["per_dollar"], 2) for x in inc])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.45), Inches(12.1), Inches(4.6), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.plots[0].gap_width = 45
    ser = ch.series[0]
    for k, (pt, x) in enumerate(zip(ser.points, inc)):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = ORANGE if x["call"] == "fails" else GRAY
        if x["call"] != "passes":
            pt.data_label.has_text_frame = False
            pt.data_label.show_value = True
            pt.data_label.number_format = '0.0'
            pt.data_label.number_format_is_linked = False
            pt.data_label.position = XL_LABEL_POSITION.OUTSIDE_END
            pt.data_label.font.size = Pt(10)
            pt.data_label.font.color.rgb = INK
    va = ch.value_axis
    va.major_unit = 0.5
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xE3, 0xE2, 0xDE)
    va.tick_labels.font.size = Pt(10)
    va.tick_labels.font.color.rgb = INK2
    va.tick_labels.number_format = '0.0'
    va.tick_labels.number_format_is_linked = False
    ch.category_axis.tick_labels.font.size = Pt(9)
    ch.category_axis.tick_labels.font.color.rgb = INK2
    either = F["R6_either"]
    _text(s, Inches(0.6), Inches(6.1), Inches(12.1), Inches(0.75), [
        "Expected net P&L each increase adds per dollar, %% a year, after the pod's payout and funding; hurdle 1.5%% (policy 9). Orange: below the hurdle. "
        "%s" % ("%s sit%s close enough to the hurdle that sound methods split on %s." % (joined(either), "s" if len(either) == 1 else "", "it" if len(either) == 1 else "them")
                if either else "")], size=12, color=INK2)
    # 4. the groups
    s = pr.slides.add_slide(blank_title)
    _title_of(s, "Net of carry, credit earns the least alpha of the seven groups")
    groups = list(F["R1_alpha"])
    rows, cols = len(groups) + 1, 4
    tb = s.shapes.add_table(rows, cols, Inches(0.6), Inches(1.55), Inches(8.0), Inches(4.2)).table
    for j, t in enumerate(["Strategy group", "Alpha a year", "Risk model's specific P&L", "Return on capital"]):
        tb.cell(0, j).text = t
    for i, g in enumerate(groups, 1):
        for j, t in enumerate([g, pct(F["R1_alpha"][g], 2), pct(F["R1_risk_model"][g], 2), pct(F["R1_raw"][g], 2)]):
            tb.cell(i, j).text = t
    for i in range(rows):
        for j in range(cols):
            for p in tb.cell(i, j).text_frame.paragraphs:
                p.font.size = Pt(13)
                p.font.bold = i == 0
                if j:
                    p.alignment = PP_ALIGN.RIGHT
    tb.columns[0].width = Inches(2.6)
    for j in (1, 2, 3):
        tb.columns[j].width = Inches(1.8)
    cr = "Credit"
    _text(s, Inches(8.9), Inches(1.6), Inches(3.9), Inches(4.9), [
        "Per cent of capital, January 2017 to %s." % last,
        "Alpha is what each group earned beyond a passive holding of its markets. A holding of Baa credit earns the spread as well as its "
        "price moves; the risk model's factors carry only the price moves, so its specific P&L leaves %.1f points a year of credit's "
        "return labelled as alpha." % (F["R1_risk_model"][cr] - F["R1_alpha"][cr]),
        "Return on capital is what each group made with nothing taken out: equities' market exposure and credit's and currencies' "
        "carry are in it, and the plan expects the markets to earn nothing (policy 8a).",
    ], size=13, color=INK2)
    _source(s, "Risk system daily P&L reconciled to the administrator's month-end statements; FRED and Cboe series as published.")
    # 5. capacity
    s = pr.slides.add_slide(blank_title)
    _title_of(s, "A pod gives up about a quarter of its alpha per dollar when its capital doubles")
    _text(s, Inches(0.6), Inches(1.6), Inches(12.1), Inches(4.8), [
        "Read within each pod, as its capital moved (onboarding steps, reviews, halvings), alpha per dollar fell by %s for each doubling of capital "
        "(sound alternatives on the same record: %s to %s)." % (pct(F["R3_fall"]), pct(min(F["R3_rivals"][k] for k in ("pod-weighted", "pod-quarter", "ramp", "onboard", "pod200"))),
                                                               pct(max(F["R3_rivals"][k] for k in ("pod-weighted", "pod-quarter", "ramp", "onboard", "pod200")))),
        "Across pods the record shows almost no fall (%s per doubling): the committee has always given more capital to stronger records and "
        "hired larger pods for better ones, so the biggest pods are the best pods, not pods that grew without cost." % pct(F["R3_rivals"]["pooled"]),
        "At the draft's sizes this is what separates a pod's average return from what its next dollar earns: an increase earns the pod's "
        "alpha at its new size on the added capital less what the existing capital gives up.",
    ], size=17)
    _source(s, "Pod-years with at least 120 trading days; alpha per dollar taken to fall by the same share at any size (policy 8e).")
    # 6. the range and what it rests on
    s = pr.slides.add_slide(blank_title)
    _title_of(s, "What the plan rests on, and what would move it")
    sens = F["routes"]
    _text(s, Inches(0.6), Inches(1.55), Inches(12.1), Inches(5.1), [
        "Range: four years in five between %s and %s. The markets are drawn from the record a quarter at a time, which keeps the weeks-long "
        "runs in credit spreads and the quick reversals in volatility; drawn a day at a time the bad years look milder (10th percentile %s)." % (
            m(F["R5_range"]["P10"]), mb(F["R5_range"]["P90"]), m(sens["daily resampling"]["p10"])),
        "Each pod's edge is its own record pulled toward its group's by how much the group's pods really differ; taken at face value, the "
        "records the draft rewards would put the year at %s." % m(sens["each pod's own record"]["mean"]),
        "Read on the risk model's factors, credit's carry stays in alpha and the year shows %s; leaving the drawdown rules out of the year adds "
        "the P&L of pods the rules would halve or close (%s)." % (m(sens["risk model's factors"]["mean"]), m(sens["no drawdown rules"]["mean"])),
        "Read across pods, capacity disappears and the year shows %s. Judged on each pod's net return at its new size rather than on "
        "what the added dollar earns, only %s fail%s." % (mb(sens["capacity across pods"]["mean"]),
                                                       joined(sens["average return at the new size"]["fail"]) if sens["average return at the new size"]["fail"] else "none",
                                                       "s" if len(sens["average return at the new size"]["fail"]) == 1 else ""),
    ], size=15)
    _source(s, "Spreadsheet, Sensitivity sheet: each line changes one judgment and keeps the rest.")
    pr.save(path)
    PP.normalize_pptx(path, AUTHOR, AUTHOR, STAMPS[DECK][0], STAMPS[DECK][1], "Draft 2027 allocation plan review", P.PLATFORM_LEGAL)


def write_all(F, out):
    os.makedirs(out, exist_ok=True)
    write_workbook(os.path.join(out, BOOK), F)
    write_deck(os.path.join(out, DECK), F)
    return [BOOK, DECK]
