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
LABEL = {
    "the golden": "This workbook",
    "the careful route: no return after a stop, the stayers listening as before":
        "Stops final, stayers' hours as before",
    "returns after a stop, the stayers listening as before": "Returns after a stop, stayers' hours as before",
    "the stayers' extra listening, no return after a stop": "Stayers' extra hours, stops final",
    "the careful route with each plan's own rises read together":
        "Each plan's two past rises averaged; stops final, hours as before",
    "the careful route with each plan's own rise in its country":
        "Each plan's past rise in its own country; stops final, hours as before",
    "the careful route with the response at the first bill alone":
        "First bill only, no December leaving; stops final, hours as before",
    "the careful route with one response for every rise": "One response for every plan; stops final, hours as before",
    "the careful route on the 2026 basis (52 per cent of net revenue)":
        "2026 basis, 52% of net revenue; stops final, hours as before",
    "the careful route with the stayers' listening read off the plan's averages":
        "Stayers' hours from plan averages; stops final",
    "returns at one rate for every listener, the stayers listening as before":
        "One return rate for every listener; stayers' hours as before",
    "the golden with returns at one rate for every listener": "One return rate for every listener",
    "the golden with the stayers' listening read off the plan's averages": "Stayers' hours from plan averages",
    "the golden with the stayers' extra listening held at its first months": "Stayers' extra hours held at the first months",
    "the golden with every subscription answering at its plan's rate": "Every subscription at its plan's average response",
    "the golden on the 2026 basis": "2026 basis, 52% of net revenue",
    "the quick route": "Plan averages, streamed hours, 2026 basis",
}
HEAD = PatternFill("solid", fgColor="DCE3EE")


def _and(xs):
    xs = list(xs)
    if not xs:
        return "none"
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _sheet(ws, header, rows, widths, fmts=None, start=1, freeze=True):
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
    if freeze:
        ws.freeze_panes = ws.cell(row=start + 1, column=2)


def workbook(path, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rises"
    rows = [[p, f["price26"][p], f["price27"][p], f["paying_oct"][p], f["change_2027"][p], f["paying_end27"][p],
             f["remun_2027"][p], "go ahead" if p in f["raise"] else "hold at 2026 price"] for p in PL]
    _sheet(ws, ["Plan", "2026 price (EUR)", "2027 price (EUR)", "Paying subscriptions at 31 Oct 2026",
                "Change in their 2027 contribution with the rise (EUR per subscription)",
                "Of them, paying on any plan at 31 Dec 2027 with the rise",
                "2027 publisher remuneration on them with the rise (EUR per subscription)", "Decision"],
           rows, [12, 11, 11, 14, 22, 18, 22, 18], {2: "0.00", 3: "0.00", 5: "0.0", 7: "0.0"}, start=3)
    ws["A1"] = "January 2027 price rises: go ahead on %s, hold %s" % (_and(f["raise"]), _and(f["hold"]))
    ws["A1"].font = Font(bold=True, size=12)
    ws = wb.create_sheet("First bill")
    rows = []
    for p in PL:
        for r in REG:
            k = "%s %s" % (p, r)
            rows.append([p, r, f["rival_2027"][k], "yes" if f["cross_2027"][p] else "no", f["extra_cancel"][k],
                         f["extra_down"].get(k, None)])
    _sheet(ws, ["Plan", "Region", "Rival's comparable plan, October 2026 scan (EUR)", "2027 price past it",
                "Extra cancellations per 100 reaching the first 2027 bill",
                "Extra downgrades per 100 (Flex has no plan below)"], rows, [12, 13, 16, 11, 20, 18],
           {3: "0.00", 5: "0.0", 6: "0.0"})
    ws = wb.create_sheet("Past rises")
    ann = {(e["year"], e["country"], e["plan"]): e["announce"] for e in f["announce_events"]}
    rows = [[e["year"], e["country"], e["plan"], e["subscriptions"], "yes" if e["crossed"] else "no",
             ann[(e["year"], e["country"], e["plan"])], e["extra_cancel"], e["extra_down"]] for e in f["events"]]
    _sheet(ws, ["January", "Region", "Plan", "Subscriptions paying in the December before",
                "New price past the rival's (December scan)",
                "Extra leaving at the December bill after the 1 December e-mail, per 100 paying in November",
                "Extra cancellations per 100 at the first bill", "Extra downgrades per 100 at the first bill"], rows,
           [9, 13, 12, 14, 13, 22, 16, 16], {6: "0.0", 7: "0.0", 8: "0.0"})
    ws = wb.create_sheet("Stopped and back")
    rows = [[b, v] for b, v in f["back12_by_band"].items()]
    _sheet(ws, ["Counted hours per paying month before stopping",
                "Of 100 that stop in December, paying again within 12 months"], rows, [26, 24], {2: "0.0"})
    r0 = len(rows) + 4
    rows = [[p, f["back_share"][p]] for p in PL]
    _sheet(ws, ["Plan", "Of 100 October subscriptions that stop by December 2027 (with the rise), paying then"],
           rows, [26, 24], {2: "0.0"}, start=r0, freeze=False)
    ws = wb.create_sheet("Stayers' listening")
    ks = list(range(1, 12))
    rows = []
    for p in PL:
        obs = {k: u for k, u in f["uplift_obs"][p]}
        rows.append([p] + [obs.get(k) for k in ks] + [f["uplift_first_month"][p], f["sal_hours"][p]])
    _sheet(ws, ["Plan"] + ["Month %d" % k for k in ks] + ["Fitted, first month", "Extra counted hours over 2027"],
           rows, [12] + [8] * 11 + [11, 12], dict({j: "0.0" for j in range(2, 15)}))
    ws.cell(row=len(rows) + 3, column=1, value="Per cent more counted hours than the same accounts' October to "
            "December, the rising region against the other, accounts on the plan through the month; months counted "
            "from the first bill at the higher price. Fitted fade: %.1f months. Extra hours per subscription staying "
            "on the plan through 2027." % f["fade_months"])
    ws = wb.create_sheet("Base")
    rows = [[p, f["paying_oct"][p], f["counted_per_month"][p]] for p in PL] + [["All plans", f["paying_oct_total"],
                                                                                 None]]
    _sheet(ws, ["Plan", "Paying subscriptions at 31 October 2026",
                "Counted hours per paying subscription-month, Nov 2025 to Oct 2026"], rows, [12, 18, 24], {3: "0.00"})
    ws = wb.create_sheet("Other readings")
    rows = [[LABEL.get(nm, nm), _and(r["raise"])] + [r["change_2027"][p] for p in PL] for nm, r in f["routes"].items()]
    _sheet(ws, ["Reading", "Rises it would let through"] + ["%s (EUR)" % p for p in PL], rows,
           [74, 30, 10, 11, 11, 10], {3: "0.0", 4: "0.0", 5: "0.0", 6: "0.0"})
    ws = wb.create_sheet("Notes")
    notes = ["Every October 2026 subscription is carried month by month to December 2027 with the rise and with the "
             "2026 price held, on its own paying months, listening, country and billing route; the other plans at the "
             "price list's 2027 prices (guideline 3.8).",
             "The first bill's response is read from the eight past rises against the same plan in the other region "
             "(guideline 3.10), by listening band, in proportion to the rise, with the downgrades among subscriptions "
             "whose profiles fit the plan below; in both regions only Flex's 2027 rise passes the rival's comparable "
             "plan (Basis 10 uur at EUR %.2f since July 2026), as both of Flex's past rises did." %
             f["rival_2027"]["Flex Netherlands"],
             "A subscription that stops pays again at the chance seen in every stop since 2024, by its listening, "
             "the months since it stopped and the calendar month, at the price then in force.",
             "The subscriptions that stay through the first bill listen as much more as the past rises' stayers did, "
             "fading over the months.",
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
    title(s, "January 2027: raise %s, hold %s" % (" and ".join(f["raise"]), " and ".join(f["hold"])),
          "Management team, November 2026")
    text(s, 457200, 1500000, 11277600, 4600000, [
        "Standaard's rise to EUR %.2f brings EUR %.1f per October subscription in 2027: it loses %.1f in every 100 at "
        "the December bill and %.1f at the first bill, but about %.0f in every 100 who stop take a plan up again "
        "before the end of 2027, at the new price." % (
            f["price27"]["Standaard"], c["Standaard"], f["announce_pct"]["Standaard"],
            f["extra_cancel"]["Standaard Netherlands"], f["back_share"]["Standaard"]),
        "Onbeperkt's rise costs EUR %.1f a subscription: those who stay listen %.0f per cent more in January and "
        "about %.0f hours more over the year, each at EUR %.2f." % (
            -c["Onbeperkt"], f["uplift_first_month"]["Onbeperkt"], f["sal_hours"]["Onbeperkt"], f["rate"]),
        "Flex's rise passes the rival's Basis 10 uur and loses EUR %.1f a subscription; Gezin's adds EUR %.1f." % (
            -c["Flex"], c["Gezin"])], 17)
    s = prs.slides.add_slide(blank)
    title(s, "%s and %s add to 2027" % tuple(f["raise"]) if len(f["raise"]) == 2 else "What each rise adds to 2027",
          "Change in the October 2026 subscriptions' 2027 contribution with the rise, EUR per subscription")
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
    title(s, "What a rise loses, and what comes back",
          "Per 100 subscriptions: extra leaving at the December bill and the first bill; of those stopping by December "
          "2027, paying again then")
    rows = [["Plan", "December bill", "First bill: leave", "First bill: move down", "Paying again, Dec 2027"]] + [
        [p, "%.1f" % f["announce_pct"][p], "%.1f" % f["extra_cancel"]["%s Netherlands" % p],
         "%.1f" % f["extra_down"]["%s Netherlands" % p] if p != "Flex" else "-", "%.0f" % f["back_share"][p]]
        for p in PL]
    tbl = s.shapes.add_table(len(rows), 5, Emu(457200), Emu(1500000), Emu(11277600), Emu(2600000)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            tbl.cell(i, j).text = v
            tbl.cell(i, j).text_frame.paragraphs[0].runs[0].font.size = Pt(14)
    text(s, 457200, 4400000, 11277600, 1600000, [
        "Light listeners leave first and come back soonest: %s in every 100 who stop with under 3 counted hours a "
        "month pay again within a year, %s of the heaviest." % (
            "%.0f" % f["back12_by_band"]["under 3"], "%.0f" % f["back12_by_band"]["20 and more"])], 15)
    s = prs.slides.add_slide(blank)
    title(s, "Those who stay listen more after a rise",
          "Per cent more counted hours than before the rise, accounts staying on the plan, against the other region")
    cd = CategoryChartData()
    cd.categories = ["Month %d" % k for k, u in f["uplift_obs"]["Onbeperkt"]]
    for p in ("Onbeperkt", "Standaard", "Gezin"):
        cd.add_series(p, [u for k, u in f["uplift_obs"][p]])
    ch = s.shapes.add_chart(XL_CHART_TYPE.LINE, Emu(457200), Emu(1300000), Emu(11277600), Emu(4300000), cd).chart
    ch.has_legend = True
    ch.font.size = Pt(11)
    text(s, 457200, 5650000, 11277600, 600000, [
        "Over 2027 that is about %.0f extra counted hours for each Onbeperkt subscription that stays, %.0f for Gezin "
        "and %.0f for Standaard." % (f["sal_hours"]["Onbeperkt"], f["sal_hours"]["Gezin"], f["sal_hours"]["Standaard"])],
         14)
    s = prs.slides.add_slide(blank)
    title(s, "The base and its 2027 publisher cost",
          "Paying subscriptions at 31 October 2026; with the rise, paying at the end of 2027 and remuneration in 2027")
    text(s, 457200, 1500000, 11277600, 4600000, ["%s: %s paying, %s paying at the end of 2027, EUR %.1f remuneration "
                                                  "each in 2027" % (p, format(f["paying_oct"][p], ","),
                                                                    format(f["paying_end27"][p], ","),
                                                                    f["remun_2027"][p]) for p in PL], 17)
    prs.save(path)


def build(folder, fig):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), fig)
    deck(os.path.join(folder, FILES["deck"]), fig)
