"""task10 architecture 6: the golden deliverables, as Wealdmoor's DSO planning team would hand them to the
December capital expenditure review: the capacity workbook (the zones with a chart, the bridge, the backtest, the
cold days behind the provider figures, the routes) and five slides."""
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


def _head(ws, hdr, widths, height=48):
    ws.append(hdr)
    for c in ws[1]:
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.row_dimensions[1].height = height
    ws.freeze_panes = "A2"


def r1(v):
    v = round(float(v) + 1e-9, 1)
    return 0.0 if v == 0 else v


PALETTE = ("A6A6A6", "5B9BD5", "1F3864", "C00000")   # before, expected, nine days in ten, firm capacity


def _formats(ws, fmts, first=2):
    """Number formats by column letter, from row `first` down."""
    for col, fmt in fmts.items():
        for cell in ws[col][first - 1:]:
            if isinstance(cell.value, (int, float)):
                cell.number_format = fmt
                cell.alignment = Alignment(horizontal="right")


def write_workbook(G, F, R, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zones"
    _head(ws, ["Constraint managed zone", "Primary substation", "Provider", "Contracted 2027/28 (MW)",
               "Design-day demand before flexibility (MW)", "Share of contracted MW available on the design day",
               "Delivered 17:30 to 18:00, design day (MW)", "Half-hour of the day's peak with flexibility (ending)",
               "Taken off the day's peak (MW)", "Expected design-day peak with flexibility (MW)",
               "Peak not exceeded on nine design days in ten (MW)", "Firm capacity (MW)", "Reinforce",
               "Over firm capacity at that level by (MW)"], [24, 20, 28, 12, 15, 15, 14, 14, 12, 15, 15, 11, 10, 14])
    for z in G["zones"]:
        ws.append([z["zone"], z["primary"], z["provider"], z["award"], r1(z["before"]), round(z["share"], 2),
                   r1(z["delivered"]), z["peak_hh"], r1(z["off_peak"]), r1(z["peak"]), r1(z["p90"]), z["firm"],
                   "Yes" if z["over"] else "No", r1(z["over_by"]) if z["over"] else None])
    n = len(G["zones"])
    _formats(ws, {"D": "0.0", "E": "0.0", "F": "0.00", "G": "0.0", "I": "0.0", "J": "0.0", "K": "0.0", "L": "0.0", "N": "0.0"})
    ws.cell(row=n + 3, column=1, value="Design day: a working weekday at a daily mean of minus 3.0 C at Halverton weather "
                                       "station, the 2027/28 contracts scheduled in full (WPN-NP-G-014, issue 4).")
    ws.cell(row=n + 4, column=1, value="Reinforce where the day's highest half-hour would exceed firm capacity on more than "
                                       "one design day in ten (guideline 7).")
    ws.cell(row=n + 6, column=1, value="Megawatts are rounded to one decimal after the arithmetic, so a figure can differ by 0.1 "
                                       "from the difference of its rounded parts.")
    ws.cell(row=n + 5, column=1, value="Demand before flexibility from the 2025/26 working weekdays outside 24 December to "
                                       "2 January, scheduled days and days with a logged transfer at the primary: %s days."
                                       % ", ".join(str(z["n_base_days"]) for z in G["zones"]))
    ch = BarChart()
    ch.type = "col"
    ch.grouping = "clustered"
    ch.title = "%s exceed firm capacity on more than one design day in ten" % _join(z["primary"] for z in G["zones"] if z["over"])
    ch.y_axis.title = "MW, winter 2027/28 design day"
    ch.y_axis.number_format = "0"
    ch.y_axis.scaling.min = 0
    cats = Reference(ws, min_col=2, min_row=2, max_row=n + 1)
    for col in (5, 10, 11, 12):
        ch.add_data(Reference(ws, min_col=col, min_row=1, max_row=n + 1), titles_from_data=True)
    ch.set_categories(cats)
    for ser, colour in zip(ch.series, PALETTE):
        ser.graphicalProperties.solidFill = colour
        ser.graphicalProperties.line.solidFill = colour
    ch.legend.position = "b"
    ch.height, ch.width = 9.5, 22
    ws.add_chart(ch, "A%d" % (n + 9))

    br = wb.create_sheet("Bridge")
    _head(br, ["Constraint managed zone", "Contracted 2027/28 (MW)", "Not available on the design day (MW)",
               "Delivered 17:30 to 18:00 (MW)", "Lost as load comes back after the window (MW)",
               "Taken off the day's peak (MW)"], [24, 14, 16, 14, 18, 14])
    tot = [0.0] * 5
    for z in G["zones"]:
        na = F["r8_bridge"]["%s, not available" % z["primary"]]
        lost = F["r8_bridge"]["%s, lost as load comes back" % z["primary"]]
        row = [z["award"], na, r1(z["delivered"]), lost, r1(r1(z["delivered"]) - lost)]
        br.append([z["zone"]] + row)
        tot = [a + b for a, b in zip(tot, row)]
    br.append(["Four zones"] + [r1(v) for v in tot])
    for c in br[br.max_row]:
        c.font = HEAD_FONT
    _formats(br, {"B": "0.0", "C": "0.0", "D": "0.0", "E": "0.0", "F": "0.0"})

    bt = wb.create_sheet("Backtest")
    b = G["backtest_all"]
    _head(bt, ["Service date", "Constraint managed zone", "Daily mean temperature (C)", "Scheduled (MW)", "Contracted (MW)",
               "Predicted from 2023/24 and 2024/25 (MW)", "Delivered 17:30 to 18:00 (MW)", "Miss (MW)"],
          [12, 24, 12, 11, 11, 16, 14, 10])
    rows = []
    for p in sorted(G["backtest"]):
        rows += G["backtest"][p]["rows"]
    for r in sorted(rows, key=lambda x: (x["date"], ZL[x["zone"]])):
        bt.append([r["date"].strftime("%d/%m/%Y"), ZL[r["zone"]], round(r["T"], 1), r["scheduled"], r["contract"],
                   round(r["predicted"], 2), round(r["delivered"], 2), round(abs(r["predicted"] - r["delivered"]), 2)])
    _formats(bt, {"C": "0.0", "D": "0.0", "E": "0.0", "F": "0.00", "G": "0.00", "H": "0.00"})
    k = len(rows) + 3
    bt.cell(row=k, column=1, value="Winter 2025/26, %d completed events, each predicted from winters 2023/24 and 2024/25 alone: "
                                   "the average miss is %.2f MW." % (b["n"], b["mae"]))
    bt.auto_filter.ref = "A1:H%d" % (len(rows) + 1)

    cd = wb.create_sheet("Cold days")
    _head(cd, ["Service date", "Constraint managed zone", "Daily mean temperature (C)", "Scheduled (MW)", "Contracted (MW)",
               "Delivered 17:30 to 18:00 (MW)", "Delivered over contracted"], [12, 24, 12, 11, 11, 14, 12])
    for r in G["cold_rows"]:
        cd.append([r["date"].strftime("%d/%m/%Y"), r["zone"], round(r["T"], 1), r["scheduled"], r["contract"],
                   round(r["delivered"], 2), round(r["share"], 3)])

    _formats(cd, {"C": "0.0", "D": "0.0", "E": "0.0", "F": "0.00", "G": "0.000"})

    rt = wb.create_sheet("Routes")
    _head(rt, ["Route", "Zone", "Delivered 17:30 to 18:00 (MW)", "Taken off the day's peak (MW)",
               "Expected peak (MW)", "Nine days in ten (MW)", "Firm capacity (MW)", "Reinforce"], [58, 20, 14, 14, 12, 12, 11, 10])
    for name, tab in R:
        for z in G["zones"]:
            t = tab[z["primary"]]
            rt.append([name, z["primary"], r1(t["delivered"]), r1(t["off_peak"]), r1(t["peak"]),
                       r1(t["one_in_ten"]) if t["one_in_ten"] is not None else None, z["firm"], "Yes" if t["over"] else "No"])
    _formats(rt, {"C": "0.0", "D": "0.0", "E": "0.0", "F": "0.0", "G": "0.0"})
    wb.save(path)
    PP.normalize_ooxml(path, "Marion Todd", "Marion Todd", _z(BOOK_CREATED), _z(BOOK_SAVED), excel=True, company=ORG)


ZL = {"PS40617": "Ashcombe Road CMZ", "PS41108": "Charlecote Way CMZ", "PS41474": "Fenwick Street CMZ",
      "PS41236": "Hartwell Common CMZ"}


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


def _join(names):
    names = list(names)
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def write_deck(G, F, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[5]
    W_ = 12192000
    commit = [z for z in G["zones"] if z["over"]]
    hold = [z for z in G["zones"] if not z["over"]]
    b = G["backtest_all"]

    s = prs.slides.add_slide(blank)
    _title(s, "Halverton flexibility zones: reinforcement for winter 2027/28", 28, top=420000, height=900000)
    _text(s, 600000, 1500000, W_ - 1200000, 4300000, [
        "Commit reinforcement now at %s." % _join(z["primary"] for z in commit),
        "%s within firm capacity on nine design days in ten with the flexibility contracted for 2027/28." %
        (_join(z["primary"] for z in hold) + (" stays" if len(hold) == 1 else " stay")),
        "With the contracts called in full on a minus 3 C day, nine days in ten the peaks stay under %s."
        % _join("%.1f MW at %s (firm %.1f)" % (r1(z["p90"]), z["primary"], z["firm"]) for z in commit),
        "On such an evening %s; at Ashcombe Road the load that comes back after the window sets the day's peak."
        % _join("%s has about %.2f of its contracted megawatts available" % (p.replace(" Ltd", ""), f["share"])
                for p, f in sorted(G["providers"].items())),
        "DSO capital expenditure review, December 2026. Prepared by the Halverton DSO planning team."], size=18)

    s = prs.slides.add_slide(blank)
    _title(s, "%s go over firm capacity on more than one design day in ten" % _join(z["primary"] for z in commit), 22)
    cd = CategoryChartData()
    cd.categories = [z["primary"] for z in G["zones"]]
    cd.add_series("Before flexibility", [r1(z["before"]) for z in G["zones"]])
    cd.add_series("Expected peak with flexibility", [r1(z["peak"]) for z in G["zones"]])
    cd.add_series("Nine design days in ten", [r1(z["p90"]) for z in G["zones"]])
    cd.add_series("Firm capacity", [z["firm"] for z in G["zones"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(700000), Emu(1100000), Emu(W_ - 1400000), Emu(5200000), cd)
    ch = gf.chart
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "MW, winter 2027/28 design day"
    ch.value_axis.axis_title.text_frame.paragraphs[0].font.size = Pt(11)
    ch.value_axis.tick_labels.number_format = "0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    for ser, colour in zip(ch.plots[0].series, PALETTE):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = RGBColor.from_string(colour)
        ser.data_labels.show_value = True
        ser.data_labels.number_format = "0.0"
        ser.data_labels.number_format_is_linked = False
        ser.data_labels.font.size = Pt(10)

    s = prs.slides.add_slide(blank)
    _title(s, "What the 2027/28 contracts take off the peak: %.1f of %.1f MW contracted"
           % (sum(r1(z["off_peak"]) for z in G["zones"]), sum(z["award"] for z in G["zones"])), 22)
    lines = []
    for z in G["zones"]:
        t = "%s: %.1f MW contracted, %.1f MW delivered at 17:30 to 18:00" % (z["primary"], z["award"], r1(z["delivered"]))
        if r1(z["comeback_loss"]) > 0:
            t += ", %.1f MW off the peak because the day then peaks in the half-hour to %s" % (r1(z["off_peak"]), z["peak_hh"])
        else:
            t += ", all of it off the peak"
        lines.append(t + ".")
    lines.append("On the cold days nearly every call came in short of the megawatts scheduled: what was delivered tracked "
                 "the megawatts contracted, not the megawatts scheduled.")
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, lines, size=17)

    s = prs.slides.add_slide(blank)
    pivot = [z for z in commit if z["peak"] <= z["firm"]]
    _title(s, ("%s is inside firm capacity on the expected day but over it on more than one design day in ten"
               % _join(z["primary"] for z in pivot)) if pivot else "Expected peaks and the nine-days-in-ten level", 22)
    lines = ["%s: expected %.1f MW, nine days in ten under %.1f MW, firm %.1f MW." % (z["primary"], r1(z["peak"]), r1(z["p90"]),
                                                                                 z["firm"]) for z in G["zones"]]
    lines.append("Fitted on winters 2023/24 and 2024/25 alone, the same approach is out by %.2f MW on average on winter "
                 "2025/26's events." % b["mae"])
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, lines, size=17)

    s = prs.slides.add_slide(blank)
    _title(s, "Commit %s reinforcements at this review; keep %s on its flexibility contract"
           % ({1: "one", 2: "two", 3: "three", 4: "four"}.get(len(commit), str(len(commit))), _join(z["primary"] for z in hold)), 22)
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, [
        "Commit the reinforcement of %s at this review, for energisation before November 2027." % _join(z["primary"] for z in commit),
        "Keep the 2027/28 flexibility contract at %s; no reinforcement there this year." % _join(z["primary"] for z in hold),
        "Ashcombe Road: beyond about %.0f MW delivered, the day's peak moves to the half-hour after the window; ask Corvane "
        "Flex for a staggered release before the next tender." % F["ashcombe_limit"],
        "Re-run the provider figures after winter 2026/27, with another winter of calls on record."],
          size=18)
    prs.save(path)
    PP.normalize_pptx(path, "Marion Todd", "Marion Todd", _z(DECK_CREATED), _z(DECK_SAVED),
                      "Halverton flexibility zones: reinforcement for winter 2027/28", ORG, revision=9, total_time=118)


def write(G, F, R, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    write_workbook(G, F, R, os.path.join(golden_dir, F_XLSX))
    write_deck(G, F, os.path.join(golden_dir, F_PPTX))
