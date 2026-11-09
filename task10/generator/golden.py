"""task10 architecture 5: the golden deliverables, as Wealdmoor's DSO planning team would hand them to the
December capital expenditure review: the capacity workbook (the zones, the event evidence, a chart) and four slides."""
import datetime as dt
import os

import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Emu, Pt

import postprocess as PP

ORG = "Wealdmoor Power Networks plc"
F_XLSX = "halverton_primary_capacity_2027-28.xlsx"
F_PPTX = "capex_review_2027-28.pptx"
# the workbook started the morning the SCADA export landed and last saved two days later; the deck built from it next
BOOK_CREATED = dt.datetime(2026, 11, 3, 10, 22, 0, tzinfo=dt.timezone.utc)
BOOK_SAVED = dt.datetime(2026, 11, 5, 16, 41, 9, tzinfo=dt.timezone.utc)
DECK_CREATED = dt.datetime(2026, 11, 5, 13, 48, 0, tzinfo=dt.timezone.utc)
DECK_SAVED = dt.datetime(2026, 11, 6, 9, 12, 44, tzinfo=dt.timezone.utc)
HEAD_FONT = Font(name="Calibri", bold=True, size=11)
HEAD_FILL = PatternFill("solid", fgColor="DDEBF7")


def _z(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_workbook(G, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zones"
    hdr = ["Constraint managed zone", "Primary substation", "Asset code", "Provider", "Contracted 2027/28 (MW)",
           "Provider delivery per MW scheduled, design day", "Flexibility credited (MW)",
           "Design-day demand before flexibility (MW)", "Design-day demand after flexibility (MW)", "Firm capacity (MW)",
           "Over firm capacity after flexibility", "Exceeds firm capacity by (MW)"] + \
          ["Over firm capacity, working weekday at minus %.1f C" % -t for t in G["sens_Ts"]]
    ws.append(hdr)
    for c in ws[1]:
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for z in G["zones"]:
        ws.append([z["zone"], z["primary"], z["code"], z["provider"], z["mw28"], round(z["delivery"], 1),
                   int(round(z["credited"])), int(round(z["before"])), int(round(z["after"])), z["firm"],
                   "Yes" if z["over"] else "No", int(round(z["over_by"])) if z["over"] else None] +
                  ["Yes" if z["sens"][t]["over"] else "No" for t in G["sens_Ts"]])
    for i, wd in enumerate([24, 20, 11, 28, 13, 18, 13, 16, 16, 12, 14, 13, 16, 16]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.row_dimensions[1].height = 48
    ws.freeze_panes = "A2"
    n = len(G["zones"])
    ws.cell(row=n + 3, column=1, value="Design day: a working weekday at a daily mean of minus 3.0 C at Halverton weather "
                                       "station (WPN-NP-G-014, issue 4). Demand in MW at the primary's SCADA total.")
    ws.cell(row=n + 4, column=1, value="Colder working weekdays: the same 2025/26 correction and growth read at that daily "
                                       "mean, less each provider's reduction at that temperature on its 2027/28 contract.")
    ch = BarChart()
    ch.type = "col"
    ch.title = "%s over firm capacity after flexibility (MW, 2027/28 design day)" % " and ".join(
        z["primary"] for z in G["zones"] if z["over"])
    ch.y_axis.title = "MW"
    data = Reference(ws, min_col=8, max_col=10, min_row=1, max_row=n + 1)
    cats = Reference(ws, min_col=2, min_row=2, max_row=n + 1)
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.height, ch.width = 9.5, 19
    ws.add_chart(ch, "B%d" % (n + 6))

    ev = wb.create_sheet("Event evidence")
    eh = ["Service date", "Constraint managed zone", "Scheduled MW", "Daily mean temperature (C)",
          "Fall at the zone primary, 17:00 to 18:00 (MW)", "Linked primary", "Rise at the linked primary, 17:00 to 18:00 (MW)",
          "Provider's reduction (MW)", "Provider's reduction per MW scheduled"]
    ev.append(eh)
    for c in ev[1]:
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for r in G["evidence"]:
        ev.append([r["date"].strftime("%d/%m/%Y"), r["zone"], r["mw"], round(r["T"], 1), round(r["fall"], 2),
                   r["linked"], round(r["rise"], 2), round(r["fall"] - r["rise"], 2),
                   round((r["fall"] - r["rise"]) / r["mw"], 3)])
    for i, wd in enumerate([12, 24, 11, 13, 18, 18, 18, 14, 14]):
        ev.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ev.row_dimensions[1].height = 48
    ev.freeze_panes = "A2"
    wb.save(path)
    PP.normalize_ooxml(path, "Marion Todd", "Marion Todd", _z(BOOK_CREATED), _z(BOOK_SAVED), excel=True, company=ORG)


def _text(slide, left, top, width, height, lines, size=16, bold_first=False, color=None):
    tb = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.bold = bold_first and i == 0
        if color:
            p.font.color.rgb = RGBColor.from_string(color)
        p.space_after = Pt(6)
    return tb


def _title(slide, text, size, color="1F3864", top=300000, height=700000):
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Emu(600000), Emu(top), Emu(12192000 - 1200000), Emu(height)
    t.text = text
    tf = t.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = 1
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = RGBColor.from_string(color)
    return t


def write_deck(G, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[5]
    W_, H_ = 12192000, 6858000
    commit = [z for z in G["zones"] if z["over"]]
    hold = [z for z in G["zones"] if not z["over"]]

    s = prs.slides.add_slide(blank)
    _title(s, "Halverton flexibility zones: reinforcement for winter 2027/28", 28, top=420000, height=900000)
    _text(s, 600000, 1500000, W_ - 1200000, 3800000, [
        "Commit reinforcement now at %s." % " and ".join(z["primary"] for z in commit),
        "%s hold firm capacity on the design day with the flexibility contracted for 2027/28." %
        " and ".join(z["primary"] for z in hold),
        "Credited at what each provider delivers on a minus 3 C day, the 2027/28 contracts take %s to %s."
        % (" and ".join(z["primary"] for z in commit),
           " and ".join("%d MW against %.1f MW firm" % (round(z["after"]), z["firm"]) for z in commit)),
        "The reinforcements must cover %s." % " and ".join("%d MW at %s" % (round(z["over_by"]), z["primary"])
                                                           for z in commit),
        "DSO capital expenditure review, December 2026. Prepared by the Halverton DSO planning team."], size=18)

    s = prs.slides.add_slide(blank)
    _title(s, "%s stay over firm capacity after their flexibility (MW, 2027/28 design day)"
           % " and ".join(z["primary"] for z in G["zones"] if z["over"]), 22)
    cd = CategoryChartData()
    cd.categories = [z["primary"] for z in G["zones"]]
    cd.add_series("Before flexibility", [int(round(z["before"])) for z in G["zones"]])
    cd.add_series("After credited flexibility", [int(round(z["after"])) for z in G["zones"]])
    cd.add_series("Firm capacity", [z["firm"] for z in G["zones"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(700000), Emu(1100000), Emu(W_ - 1400000), Emu(5200000), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    plot = ch.plots[0]
    for k, ser in enumerate(plot.series):
        ser.data_labels.show_value = True
        ser.data_labels.number_format = "0.0" if k == 2 else "0"
        ser.data_labels.number_format_is_linked = False
        ser.data_labels.font.size = Pt(11)

    s = prs.slides.add_slide(blank)
    lo, hi = min(round(z["delivery"], 1) for z in G["zones"]), max(round(z["delivery"], 1) for z in G["zones"])
    _title(s, "Net of the rise across the open points, the providers deliver %.1f to %.1f per MW scheduled on the design day"
           % (lo, hi), 22)
    lines = []
    for z in G["zones"]:
        if z["linked_rise"] > 0.3:
            lines.append("%s: the primary fell %.1f MW per MW scheduled at 17:00 to 18:00 on event days, but %s rose by %.1f MW "
                         "in the same half-hours; the provider's own reduction is %.1f per MW at minus 3 C."
                         % (z["primary"], z["measured"], z["linked"], z["linked_rise"], z["delivery"]))
        else:
            lines.append("%s: no linked primary rose on event days; the provider's reduction is %.1f per MW at minus 3 C."
                         % (z["primary"], z["delivery"]))
    lines.append("Both providers reduce less as the day gets colder, so each zone is credited at its minus 3 C delivery.")
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, lines, size=16)

    s = prs.slides.add_slide(blank)
    t1 = G["sens_Ts"][0]
    first = [z for z in G["zones"] if z["sens"][t1]["over"] and not z["over"]]
    _title(s, "A colder winter: on a working weekday at minus %.1f C, %s would also exceed firm capacity"
           % (-t1, " and ".join(z["primary"] for z in first)), 22)
    lines = []
    for z in G["zones"]:
        lines.append("%s: %s firm capacity after flexibility on the design day, %s at minus %.1f C."
                     % (z["primary"], "over" if z["over"] else "within", "over" if z["sens"][t1]["over"] else "within", -t1))
    lines.append("Both providers deliver less per MW scheduled on a colder day, so the credit falls as the demand rises.")
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, lines, size=18)

    s = prs.slides.add_slide(blank)
    _title(s, "Recommendation and next steps", 22)
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, [
        "Commit the reinforcement of %s at this review, for energisation before November 2027." %
        " and ".join(z["primary"] for z in commit),
        "Keep the 2027/28 flexibility contracts at %s; they hold firm capacity on the design day." %
        " and ".join(z["primary"] for z in hold),
        "%s: their flexibility holds them on the design day but not on a working weekday at minus %.1f C; review both at "
        "next year's assessment." % (" and ".join(z["primary"] for z in first), -t1),
        "Ask the control room to log the switching state of the %s open points for each flexibility event."
        % ", ".join(z["linked"] for z in G["zones"] if z["linked"])],
          size=18)
    prs.save(path)
    PP.normalize_pptx(path, "Marion Todd", "Marion Todd", _z(DECK_CREATED), _z(DECK_SAVED),
                      "Halverton flexibility zones: reinforcement for winter 2027/28", ORG, revision=9, total_time=118)


def write(G, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    write_workbook(G, os.path.join(golden_dir, F_XLSX))
    write_deck(G, os.path.join(golden_dir, F_PPTX))
