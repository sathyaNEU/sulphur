"""The golden deliverables the prompt asks for: a workbook (price_rises_2027.xlsx) and a short deck for the
management team (price_rises_2027.pptx), built from the same objects that write figures.json."""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Emu, Pt

BLUE, GREY, INK, MUTED = "2A78D6", "8A8984", "0B0B0B", "52514E"
FILES = {"wb": "price_rises_2027.xlsx", "deck": "price_rises_2027.pptx"}
PL = ["Flex", "Standaard", "Onbeperkt", "Gezin"]
REG = ["Netherlands", "Flanders"]
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="DCE3EE")


def _sheet(ws, header, rows, widths, fmts=None, start=1):
    for j, h in enumerate(header, 1):
        c = ws.cell(row=start, column=j, value=h)
        c.font, c.fill = BOLD, HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(rows, start + 1):
        for j, v in enumerate(r, 1):
            c = ws.cell(row=i, column=j, value=v)
            if fmts and fmts.get(j):
                c.number_format = fmts[j]
    for j, w in enumerate(widths):
        ws.column_dimensions[chr(65 + j)].width = w
    ws.freeze_panes = ws.cell(row=start + 1, column=2)


def workbook(path, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rises"
    rows = [[p, f["price26"][p], f["price27"][p], f["paying_oct"][p], f["change_2027"][p],
             "go ahead" if p in f["raise"] else "hold at 2026 price"] for p in PL]
    _sheet(ws, ["Plan", "2026 price (EUR)", "2027 price (EUR)", "Paying subscriptions at 31 Oct 2026",
                "Change in their 2027 contribution if the rise goes ahead (EUR per subscription)", "Decision"],
           rows, [12, 11, 11, 14, 24, 18], {2: "0.00", 3: "0.00", 5: "0.0"}, start=3)
    ws["A1"] = "January 2027 price rises: go ahead on %s, hold %s" % (", ".join(f["raise"]), ", ".join(f["hold"]))
    ws["A1"].font = Font(bold=True, size=12)
    ws = wb.create_sheet("Response")
    rows = []
    for p in PL:
        for r in REG:
            k = "%s %s" % (p, r)
            rows.append([p, r, f["rival_nl" if r == "Netherlands" else "rival_be"][p], f["extra_cancel"][k],
                         f["extra_down"].get(k, None)])
    _sheet(ws, ["Plan", "Region", "Rival's comparable plan, last scan (EUR)",
                "Extra cancellations per 100 at the first 2027 bill", "Extra downgrades per 100"], rows,
           [12, 13, 16, 18, 16], {3: "0.00", 4: "0.0", 5: "0.0"})
    ws = wb.create_sheet("Past rises")
    rows = [[e["year"], e["country"], e["plan"], e["subscriptions"], "yes" if e["crossed"] else "no",
             e["extra_cancel"], e["extra_down"]] for e in f["events"]]
    _sheet(ws, ["January", "Region", "Plan", "Subscriptions facing the rise", "New price past the rival's",
                "Extra cancellations per 100", "Extra downgrades per 100"], rows, [9, 13, 12, 14, 12, 14, 14],
           {6: "0.0", 7: "0.0"})
    ws = wb.create_sheet("Downgraders and leavers")
    rows = [[p, f["downgrader_value"].get(p), f["leaver_hours_ratio"][p]] for p in PL]
    _sheet(ws, ["Plan", "What a subscription moving down brings in 2027 (EUR)",
                "Leavers' listening against the plan's average"], rows, [12, 22, 22], {2: "0.0", 3: "0.00"})
    ws = wb.create_sheet("Base")
    rows = [[p, f["paying_oct"][p], f["counted_per_month"][p]] for p in PL] + [["All plans", f["paying_oct_total"], None]]
    _sheet(ws, ["Plan", "Paying subscriptions at 31 October 2026",
                "Counted hours per paying subscription-month, Nov 2025 to Oct 2026"], rows, [12, 18, 24], {3: "0.00"})
    ws = wb.create_sheet("Other readings")
    rows = [[nm, ", ".join(r["raise"]) or "none"] + [r["change_2027"][p] for p in PL] for nm, r in f["routes"].items()]
    _sheet(ws, ["Reading", "Rises it would let through"] + ["%s (EUR)" % p for p in PL], rows,
           [70, 30, 10, 11, 11, 10], {3: "0.0", 4: "0.0", 5: "0.0", 6: "0.0"})
    ws = wb.create_sheet("Notes")
    notes = ["A rise's response is read at each subscription's first bill at the new price (January and February), "
             "against the same plan in the other region over the same months (guideline 3.10).",
             "Whether a rise put a plan's price past the rival's comparable plan uses the rival scan of the December "
             "before (promotions left out); for 2027, the October 2026 scan (guideline 3.8).",
             "Subscriptions that move down a plan stay in the October base and are valued on their own months on the "
             "lower plan after the 2025 and 2026 rises; those that leave on the listening of those who left at the "
             "plan's past rises of the same kind.",
             "Contribution: net revenue less EUR %.2f per counted hour (schedule B), counted hours from the live "
             "roll-up and the licence renewals, attributed to the account each charge lists." % f["rate"]]
    for i, n in enumerate(notes, 1):
        ws.cell(row=i, column=1, value=n).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 110
    wb.save(path)


def deck(path, f):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, lines, size=16):
        tf = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)).text_frame
        tf.word_wrap = True
        for k, line in enumerate(lines):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.runs[0].font.size = Pt(size)
            p.runs[0].font.color.rgb = RGBColor.from_string(INK)
            p.space_after = Pt(10)
        return tf

    def title(slide, t, sub=None):
        tf = text(slide, 457200, 300000, 11277600, 700000, [t], 24)
        tf.paragraphs[0].runs[0].font.bold = True
        if sub:
            q = tf.add_paragraph()
            q.text = sub
            q.runs[0].font.size = Pt(13)
            q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
        for x, w, s in ((457200, 10800000, "Billing, warehouse, licence server and rival scan to 31 October 2026; "
                                           "SUL schedule B; growth planning guideline"),
                        (11300000, 500000, str(len(prs.slides)))):
            q = slide.shapes.add_textbox(Emu(x), Emu(6400000), Emu(w), Emu(300000)).text_frame.paragraphs[0]
            q.text = s
            q.runs[0].font.size = Pt(9)
            q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)

    c = f["change_2027"]
    s = prs.slides.add_slide(blank)
    title(s, "January 2027: raise %s, hold %s" % (", ".join(f["raise"]), ", ".join(f["hold"])),
          "Management team, November 2026")
    text(s, 457200, 1500000, 11277600, 4600000, [
        "Standaard's rise to EUR %.2f takes it past the rival's comparable plan in both regions: about %.1f in every "
        "100 leave at the first bill and %.1f move down, and its October subscriptions bring EUR %.1f less each in "
        "2027." % (f["price27"]["Standaard"], f["extra_cancel"]["Standaard Netherlands"],
                   f["extra_down"]["Standaard Netherlands"], -c["Standaard"]),
        "Onbeperkt and Gezin pass the rival only in the Netherlands; with the light listeners who move down kept "
        "and the heavy listeners who leave costing more in hours than they pay, they gain EUR %.1f and EUR %.1f a "
        "subscription." % (c["Onbeperkt"], c["Gezin"]),
        "Flex stays above the rival either way and gains EUR %.1f." % c["Flex"]], 17)
    s = prs.slides.add_slide(blank)
    title(s, "Only Standaard's rise loses money in 2027",
          "Change in the October 2026 subscriptions' 2027 contribution if the rise goes ahead, EUR per subscription")
    cd = CategoryChartData()
    cd.categories = PL
    cd.add_series("Change", [c[p] for p in PL])
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(4900000),
                            cd).chart
    ch.has_legend = False
    ch.font.size = Pt(11)
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.0"
    pl.data_labels.number_format_is_linked = False
    for i, p in enumerate(PL):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor.from_string(BLUE if p in f["raise"] else GREY)
    s = prs.slides.add_slide(blank)
    title(s, "Past rises answered only where they passed the rival",
          "Extra cancellations and downgrades per 100 at the first bill, January 2025 and 2026")
    rows = [["January", "Region", "Plan", "Past the rival", "Cancellations", "Downgrades"]] + [
        [str(e["year"]), e["country"], e["plan"], "yes" if e["crossed"] else "no", "%.1f" % e["extra_cancel"],
         "%.1f" % e["extra_down"]] for e in f["events"]]
    tbl = s.shapes.add_table(len(rows), 6, Emu(457200), Emu(1400000), Emu(11277600), Emu(4300000)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            tbl.cell(i, j).text = v
            tbl.cell(i, j).text_frame.paragraphs[0].runs[0].font.size = Pt(13)
    s = prs.slides.add_slide(blank)
    title(s, "The base the rises apply to", "Paying subscriptions at 31 October 2026 and their listening")
    text(s, 457200, 1500000, 11277600, 4600000, ["%s: %s paying, %.2f counted hours per paying month" % (
        p, format(f["paying_oct"][p], ","), f["counted_per_month"][p]) for p in PL], 17)
    prs.save(path)


def build(folder, fig):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), fig)
    deck(os.path.join(folder, FILES["deck"]), fig)
