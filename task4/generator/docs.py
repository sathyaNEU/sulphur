"""Wrenfold's own documents and its suppliers': the fleet standard FS-04, the trade quality cellar check form TQ-02,
the maker's quotation and the pooling company's seasonal hire terms (each exported from a word processor through the
house writer), the 2027 brew plan, the Maplestead supply agreement's schedule, the route plan and the trade price
list."""
import datetime as dt
import os
import sys

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
sys.path.insert(0, HERE)
import officepdf as O  # noqa: E402
import core as C  # noqa: E402
import pack as PK  # noqa: E402
import world as WL  # noqa: E402

ORG = WL.ORG
GMT = dt.timezone.utc
BST = dt.timezone(dt.timedelta(hours=1))
CET = dt.timezone(dt.timedelta(hours=1))
FILES = {
    "standard": "FS-04_returnable_container_fleet_issue3.pdf",
    "form": "TQ-02_cellar_quality_check.pdf",
    "quotation": "lindqvist_quotation_Q26-1187.pdf",
    "hire": "pennine_seasonal_hire_terms_2027.pdf",
    "plan": "brew_plan_2027.xlsx",
    "schedule": "maplestead_supply_agreement_schedules.xlsx",
    "routes": "route_plan_autumn_2026.xlsx",
    "prices": "trade_price_list_2026.xlsx",
}
SEASON_FIRST = WL.week_start(C.SEASON[0])
SEASON_LAST = WL.week_start(C.SEASON[-1])
PLAN_SUMMER = WL.week_start(C.RUNS_WEEK)
MOQ = {p: C.W[p]["moq"] for p in WL.POOLS}
LISTING = [WL.week_start(C.ESTATE_WEEK + k) for k in range(3)]
EST_NAMES = ["Maplestead Arms", "Old Mill", "Packhorse", "Shoulder of Mutton", "Fleece", "White Bear", "Hare and Hounds",
             "Bridge", "Waggon and Horses", "Griffin", "Royal Oak", "Black Swan", "Turks Head", "Three Horseshoes",
             "Railway", "Boot and Shoe", "Nags Head", "Wheatsheaf", "Duke of York", "Golden Fleece", "Brown Cow",
             "New Inn", "Cross Keys", "Ring o' Bells", "Stanley Arms"]
EST_TOWNS = ["Keighley", "Bingley", "Shipley", "Brighouse", "Halifax", "Sowerby Bridge", "Cleckheaton", "Heckmondwike",
             "Mirfield", "Ossett", "Normanton", "Garforth", "Rothwell", "Horsforth", "Guiseley", "Yeadon", "Baildon",
             "Silsden", "Barnoldswick", "Colne", "Nelson", "Burnley", "Accrington", "Rawtenstall", "Bacup", "Rochdale",
             "Oldham", "Glossop", "Buxton", "Matlock", "Worksop", "Retford", "Goole", "Howden", "Beverley", "Driffield"]


def fmt(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.4, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.6,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.7, leading=10.6)
    return body, h1, h2, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[w * 2.83 for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


STANDARD = [
    ("1. Purpose and scope", [
        "1.1 This standard sets how the fleet of each returnable container type is reviewed each year ahead of the "
        "summer season, and the cover that is put in place. It applies to the five container types Wrenfold fills: "
        "the 50 litre keg (K50), the 30 litre keg (K30), the 20 litre keg (K20), the firkin (FIR) and the kilderkin "
        "(KIL). Each type is reviewed on its own.",
        "1.2 The review follows the count of every Wrenfold site at the end of November and is reported to the order "
        "meeting in December, so that an order placed with the maker in January is delivered before the season "
        "opens.",
    ]),
    ("2. Definitions", [
        "2.1 Requirement. A container type's requirement in a week is the number of its containers that are, in that "
        "week, at customers (full, on dispense, or empty and awaiting collection), full in the cold store, at the "
        "depots, and in wash and repair (empties awaiting wash are counted under wash), together with a float of two "
        "sevenths of the containers delivered in the week.",
        "2.2 Fleet. A container type's fleet in a week is the number of its containers that are on Wrenfold's sites or "
        "at its customers in that week.",
        "2.3 Shortfall. The shortfall in a week is the requirement less the fleet, taken with no purchase and no hire "
        "after the annual count. A negative shortfall is a surplus and is reported as a negative figure.",
    ]),
    ("3. The figure reviewed", [
        "3.1 Season. The summer season is the 21 weeks from the week beginning on the first Monday of May. For the "
        "2027 review these are the weeks beginning Monday %s to Monday %s. A week runs Monday to Sunday." % (
            fmt(SEASON_FIRST), fmt(SEASON_LAST)),
        "3.2 Planning case. The figure reviewed is the largest weekly shortfall in the season, with every week taken "
        "at the Calder Vale weather station's normal temperature for that week.",
        "3.3 Hot case. The season is also run on the recorded weather of each of the last ten summers (for the 2027 "
        "review, 2017 to 2026), each summer's 21 season weeks taken in order and every other week at its normal. Each "
        "summer gives a largest weekly shortfall, and the hot case is the second highest of the ten.",
        "3.4 The season is taken as contracted and planned at the date of the review: the accounts supplied and those "
        "under a signed supply agreement, and the range and the brew plan as issued.",
    ]),
    ("4. Cover", [
        "4.1 The cover for a container type is read on the planning case. Where the largest weekly shortfall is nil or "
        "negative, no cover is put in place. Where it is above nil and below the maker's minimum order run for the "
        "type, it is covered by a seasonal hire. Where it is the minimum order run or more, it is covered by a "
        "purchase. The hot case is reported beside the planning case and does not change the cover.",
        "4.2 The maker's minimum order run for each type is taken from the maker's quotation in force at the review.",
    ]),
    ("5. Collection", [
        "5.1 Empty containers are collected by the dray at its next delivery to the account. The driver takes every "
        "Wrenfold empty on the premises, of every type.",
        "5.2 Containers are returned through the depot that serves the account and trunked to Brighouse for washing.",
    ]),
    ("6. Report", [
        "6.1 The review reports, for each container type, the largest weekly shortfall of the season in the planning "
        "case and in the hot case, in containers, the week in which the planning case's figure falls, and the cover.",
        "6.2 The report is kept with the count sheets of the year it follows.",
    ]),
    ("7. Changes from issue 2", [
        "7.1 The float is restated as two sevenths of the week's deliveries (issue 2 gave it as two days' deliveries, "
        "which was read both as two of seven days and as two of five delivery days).",
        "7.2 The hot case is defined on the ten most recent summers; issue 2 used the single hottest summer on record.",
        "7.3 The review follows the count of every site in the last week of November, which replaces the annual "
        "count of early December.",
    ]),
]


def write_standard(target):
    body, h1, h2, cell = _styles()
    title = "FS-04 Returnable container fleet: annual review and cover"
    head = [["Document", "Fleet standard FS-04, issue 3"],
            ["Owner", "%s, Head of Supply Chain" % WL.PEOPLE["head"]],
            ["In force from", "1 October 2026"],
            ["Replaces", "issue 2 of 16 September 2024"]]
    story = [Paragraph(title, h1), _grid(head, [36, 130], cell), Spacer(1, 6)]
    for hd, paras in STANDARD:
        story.append(Paragraph(hd, h2))
        for p in paras:
            story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES["standard"]), story, title=title, author=WL.PEOPLE["head"],
            subject="Returnable containers, fleet review", footer="%s, fleet standard FS-04, issue 3" % ORG,
            created=dt.datetime(2026, 9, 24, 15, 12, tzinfo=BST), modified=dt.datetime(2026, 9, 24, 15, 12, tzinfo=BST),
            font="Liberation Sans")


def write_form(target):
    """the blank cellar quality check the trade quality reps carry, one form a call"""
    body, h1, h2, cell = _styles()
    title = "TQ-02 Cellar quality check"
    head = [["Account no.", "", "Date of call", ""], ["Account name", "", "Rep", ""],
            ["Cellar temperature, C", "", "Licensee present", "Yes / No"]]
    rows = [["Line", "Beer", "Container", "Full in cellar", "On dispense", "Oldest date code", "Condition / comments"]]
    rows += [["", "", "", "", "", "", ""] for _ in range(12)]
    story = [Paragraph(title, h1), _grid(head, [34, 50, 34, 50], cell), Spacer(1, 6),
             Paragraph("One form for each call. Enter each Wrenfold line you check, by the line number on the account's "
                       "line list.", body),
             _grid(rows, [12, 40, 20, 20, 20, 26, 44], cell), Spacer(1, 6),
             Paragraph("Full in cellar: unbroached Wrenfold containers of the line's beer in the cellar. On dispense: "
                       "1 where a Wrenfold container is coupled to the line, 0 where none is.", body),
             Paragraph("Oldest date code: the earliest best-before date on a full container of the line's beer.", body),
             Paragraph("Condition: report any container past its date, any line due for cleaning, gas below the "
                       "reserve mark, or a cellar above 13 C, on the account's quality record.", body),
             Spacer(1, 10),
             _grid([["Rep signature", "", "Licensee signature", ""]], [30, 54, 30, 54], cell)]
    O.build(os.path.join(target, FILES["form"]), story, title=title, author="Trade Quality",
            subject="Cellar quality check", footer="%s, Trade Quality, form TQ-02 rev. 4 (03/24)" % ORG,
            created=dt.datetime(2024, 3, 11, 10, 4, tzinfo=GMT), modified=dt.datetime(2024, 3, 11, 10, 9, tzinfo=GMT),
            font="Liberation Sans")


def write_quotation(target):
    body, h1, h2, cell = _styles()
    title = "Quotation Q26-1187: stainless steel kegs and casks"
    head = [["To", "%s, Calder Works, Brighouse, for the attention of %s" % (ORG, WL.PEOPLE["fleet"])],
            ["From", "%s, Vertrieb Export, Lindqviststrasse 4, 57482 Wenden" % WL.MAKER],
            ["Date", "9 November 2026"], ["Valid until", "29 January 2027"]]
    price = {"K50": 64.90, "K30": 55.70, "K20": 62.30, "FIR": 78.40, "KIL": 101.20}
    spec = {"K50": "50 l keg, DIN, flat fitting, embossed chime", "K30": "30 l keg, DIN, flat fitting, embossed chime",
            "K20": "20 l keg, slim, flat fitting, embossed chime", "FIR": "Firkin, 40.9 l, stainless, shive and keystone bushes",
            "KIL": "Kilderkin, 81.8 l, stainless, shive and keystone bushes"}
    lead = {"K50": 12, "K30": 12, "K20": 13, "FIR": 14, "KIL": 14}
    rows = [["Item", "Description", "Unit price, EUR", "Minimum order run, units", "Lead time, weeks from order"]]
    for j, p in enumerate(WL.POOLS):
        rows.append(["%d" % (j + 1), spec[p], "%.2f" % price[p], "{:,}".format(MOQ[p]), "%d" % lead[p]])
    story = [Paragraph(title, h1), _grid(head, [26, 140], cell), Spacer(1, 6),
             Paragraph("Thank you for your enquiry of 2 November. We are pleased to quote as follows for containers to "
                       "your drawings on file, embossed WRENFOLD BREWERY and serial numbered in sequence with your "
                       "previous lots.", body),
             _grid(rows, [10, 70, 24, 30, 32], cell), Spacer(1, 4),
             Paragraph("Each item is made as one production run. An order for an item below its minimum order run "
                       "cannot be accepted; quantities above it are accepted in multiples of 100 units.", body),
             Paragraph("Prices are per unit, delivered at place Brighouse (DAP, Incoterms 2020), excluding VAT. Payment "
                       "30 per cent with order, the balance 30 days from delivery.", body),
             Paragraph("Lead times run from receipt of order and deposit. An order received by 15 January 2027 will be "
                       "delivered complete by 23 April 2027.", body),
             Paragraph("Tooling for the embossing is held at our works and is not charged. Each container is stamped "
                       "on the chime with your lot reference and serial.", body),
             Paragraph("Yours faithfully, Henrik Brandt, Export Sales", body)]
    O.build(os.path.join(target, FILES["quotation"]), story, title=title, author="Henrik Brandt",
            subject="Quotation Q26-1187", footer="%s, quotation Q26-1187" % WL.MAKER,
            created=dt.datetime(2026, 11, 9, 10, 37, tzinfo=CET), modified=dt.datetime(2026, 11, 9, 10, 41, tzinfo=CET),
            font="Liberation Sans")


def write_hire(target):
    body, h1, h2, cell = _styles()
    title = "Seasonal container hire 2027: terms and rates"
    head = [["Customer", ORG], ["Issued", "16 November 2026"], ["Hire period", "Monday 26 April to Sunday 3 October 2027"]]
    rate = {"K50": 0.92, "K30": 0.84, "K20": 0.88, "FIR": 1.05, "KIL": 1.30}
    name = {p: PK.DESCR[p][0] for p in WL.POOLS}
    rows = [["Container", "Rate per container per week, GBP", "Delivery and collection per pallet, GBP"]]
    for p in WL.POOLS:
        rows.append([name[p], "%.2f" % rate[p], "38.00"])
    story = [Paragraph(title, h1), _grid(head, [30, 136], cell), Spacer(1, 6),
             Paragraph("1. %s hires clean, pressure tested containers of the types below for the whole hire period. "
                       "Containers are hired in whole pallets and there is no upper limit on a booking made by "
                       "26 February 2027." % WL.HIRER, body),
             _grid(rows, [60, 52, 54], cell), Spacer(1, 4),
             Paragraph("2. Hired containers carry the pool's own markings and serial numbers and are not entered on "
                       "the customer's register.", body),
             Paragraph("3. The rate is charged for every week of the hire period on the quantity booked, whether or "
                       "not the containers are in use.", body),
             Paragraph("4. Containers are returned washed to the pool's Wakefield yard by 17 October 2027. A container "
                       "not returned by that date is invoiced at the replacement price on the pool's current list.", body),
             Paragraph("5. A booking is confirmed by purchase order and may be reduced without charge until "
                       "26 March 2027.", body)]
    O.build(os.path.join(target, FILES["hire"]), story, title=title, author="Pennine Container Pool, Customer Desk",
            subject="Seasonal hire 2027", footer="%s, seasonal hire 2027" % WL.HIRER,
            created=dt.datetime(2026, 11, 16, 9, 22, tzinfo=GMT), modified=dt.datetime(2026, 11, 16, 9, 22, tzinfo=GMT),
            font="Liberation Sans")


def _sheet(ws, header, rows, widths, dates=()):
    ws.append(header)
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    top = ws.max_row
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    for col in dates:
        for r in ws.iter_rows(min_row=top + 1, min_col=col, max_col=col):
            r[0].number_format = "dd/mm/yyyy"
    ws.freeze_panes = "A%d" % (top + 1)


def plan_rows():
    """the 2027 brew plan: each beer and container type, its racking run and its on-sale dates, by half of the year"""
    y0, y1 = dt.date(2027, 1, 4), dt.date(2028, 1, 2)
    before = PLAN_SUMMER - dt.timedelta(days=1)
    rows = []
    for p in WL.POOLS:
        w = C.W[p]
        for c, sh, q26, q27 in w["beers"]:
            rows.append([PK.sku(p, c), WL.BEER_NAMES[c], p, "Winter and spring", y0, before, q26])
            rows.append([PK.sku(p, c), WL.BEER_NAMES[c], p, "Summer and autumn", PLAN_SUMMER, y1, q27])
        for c, q in w["new27"]:
            rows.append([PK.sku(p, c), WL.BEER_NAMES[c], p, "Summer range", PLAN_SUMMER,
                         dt.date(2027, 10, 31) if p == "FIR" else dt.date(2027, 9, 26), q])
    return rows


def write_plan(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Brew plan 2027"
    ws.append(["Brew plan 2027, issue 1"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Issued", dt.date(2026, 11, 12), "", "Head Brewer", WL.PEOPLE["brewer"]])
    ws["B2"].number_format = "dd/mm/yyyy"
    ws.append([])
    rows = sorted(plan_rows(), key=lambda r: (WL.POOLS.index(r[2]), r[4], r[0]))
    _sheet(ws, ["sku", "beer", "container", "plan period", "first on sale", "last on sale", "racking run, containers"],
           rows, [12, 30, 11, 20, 14, 14, 16], dates=(5, 6))
    wb.save(os.path.join(target, FILES["plan"]))


def estate_rows(seed=WL.SEED):
    """the Maplestead pubs: listing date, delivery day and lines by container type; 300 pubs in three tranches"""
    rng = np.random.default_rng([seed, 200])
    n = 300                                                      # the estate's pubs
    lines = {p: C.W[p]["estate"][0] for p in WL.POOLS}
    cut = {p: [int(round(lines[p] * (k + 1) / 3.0)) for k in range(3)] for p in WL.POOLS}
    pubs = []
    seen = set()
    per = n // 3
    for k in range(3):
        alloc = {p: WL.split(cut[p][k] - (cut[p][k - 1] if k else 0), rng.gamma(2.5, 1.0, per)) for p in WL.POOLS}
        for j in range(per):
            while True:
                name = "The %s, %s" % (EST_NAMES[int(rng.integers(0, len(EST_NAMES)))], EST_TOWNS[int(rng.integers(0, len(EST_TOWNS)))])
                if name not in seen:
                    seen.add(name)
                    break
            row = {"name": name, "tranche": k, "day": PK.DAYNAME[int(rng.integers(0, 5))]}
            for p in ("K50", "K30", "K20", "FIR"):
                row[p] = int(alloc[p][j])
            pubs.append(row)
    order = rng.permutation(len(pubs))
    return [pubs[int(i)] for i in order]


def write_schedule(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Schedule A outlets"
    ws.append(["Supply agreement between %s and %s, signed 23 October 2026" % (ORG, WL.ESTATE)])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Schedule A: outlets, listing dates and lines installed at listing"])
    ws.append([])
    rows = [["MI-%03d" % (j + 1), r["name"].split(", ")[0], r["name"].split(", ")[1], LISTING[r["tranche"]], r["day"],
             r["K50"], r["K30"], r["K20"], r["FIR"]] for j, r in enumerate(estate_rows())]
    _sheet(ws, ["outlet", "name", "town", "listing date", "delivery day", "50 litre keg lines", "30 litre keg lines",
                "20 litre keg lines", "firkin lines"], rows, [9, 26, 18, 13, 12, 11, 11, 11, 10], dates=(4,))
    ws2 = wb.create_sheet("Schedule B volumes")
    ws2.append(["Schedule B: committed volumes"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    _sheet(ws2, ["container", "lines at full listing",
                 "average weekly volume per line over the twelve months to September 2026, containers"],
           [[{"K50": "50 litre keg", "K30": "30 litre keg", "K20": "20 litre keg", "FIR": "firkin"}[p],
             C.W[p]["estate"][0], C.W[p]["estate"][1]] for p in ("K50", "K30", "K20", "FIR")], [24, 16, 34])
    ws2.append([])
    ws2.append(["Contract year: 12 April 2027 to 9 April 2028. Each outlet is supplied once a week on its delivery day."])
    wb.save(os.path.join(target, FILES["schedule"]))


def write_routes(target, WD):
    R = PK.routes(WD)
    wb = Workbook()
    ws = wb.active
    ws.title = "Routes"
    rows = []
    for a in WD.accounts:
        days, names, drops = R[a["k"]]
        for d, nm, dr in zip(days, names, drops):
            rows.append([nm, a["depot"], PK.DAYNAME[d], (dr - 1) % 28 + 1, a["id"], a["name"], len(days)])
    rows.sort(key=lambda r: (r[1], PK.DAYNAME.index(r[2]), r[0], r[3]))
    _sheet(ws, ["route", "depot", "day", "drop", "account_no", "account", "deliveries a week"], rows, [10, 8, 7, 7, 12, 40, 12])
    wb.save(os.path.join(target, FILES["routes"]))


def write_prices(target, WD):
    rng = np.random.default_rng([WL.SEED, 201])
    wb = Workbook()
    ws = wb.active
    ws.title = "Price list"
    ws.append(["Trade price list, effective 2 March 2026 (prices per container, GBP, excluding VAT)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    base = {"K50": 142.0, "K30": 96.0, "K20": 84.0, "FIR": 98.0, "KIL": 188.0}
    rows = []
    for p in WL.POOLS:
        for c, sh, q26, q27 in C.W[p]["beers"]:
            x = base[p] * float(np.exp(rng.normal(0, 0.06)))
            rows.append([PK.sku(p, c), WL.BEER_NAMES[c], PK.DESCR[p][0], round(x, 2), round(x * 0.955, 2), round(x * 0.92, 2)])
    _sheet(ws, ["sku", "beer", "container", "list", "band B (30+ a month)", "band C (80+ a month)"], rows,
           [12, 30, 26, 10, 14, 14])
    wb.save(os.path.join(target, FILES["prices"]))


def write_all(target, WD):
    write_standard(target)
    write_form(target)
    write_quotation(target)
    write_hire(target)
    write_plan(target)
    write_schedule(target)
    write_routes(target, WD)
    write_prices(target, WD)
