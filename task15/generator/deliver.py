"""The golden deliverables: the rollout workbook and the note for the board, both from figures.json and the golden's
own tables, through the house writers."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.util import Emu, Pt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402

import golden as GD  # noqa: E402
import postprocess as PP  # noqa: E402

WORKBOOK = "fresh_forecast_rollout_2027.xlsx"
NOTE = "fresh_forecast_board_2027.pptx"
ORG = "Fjordkøb A/S"
AUTHOR = "Elna Johnsen"
STAMPS = {WORKBOOK: ("2026-09-21T08:41:00Z", "2026-09-28T14:56:00Z"), NOTE: ("2026-09-28T15:22:00Z", "2026-09-29T08:47:00Z")}
FMT = GD.FORMATS
FMT_NAME = {"Super": "Super", "Kvarter": "Kvarter", "To Go": "To Go"}
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
         11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen",
         18: "eighteen"}
BLUE, ORANGE, INK, INK2, RULE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#c3c2b7"
HEAD = PatternFill("solid", fgColor="E3E8EF")
THIN = Border(bottom=Side(style="thin", color="9AA0AB"))


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(size=9, color="52514E")


def _head(ws, row, labels, widths=None):
    for j, lab in enumerate(labels, start=1):
        c = ws.cell(row=row, column=j, value=lab)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = THIN
    if widths:
        for j, wd in enumerate(widths, start=1):
            ws.column_dimensions[chr(64 + j)].width = wd


def _fmt(ws, rows, cols, number_format):
    for r in rows:
        for c in cols:
            ws.cell(row=r, column=c).number_format = number_format


def write_workbook(path, R, F):
    G = R["G"]
    sp, P = G["sp"].copy(), G["P"].copy()
    names = R["T"]["stores"].set_index("store")["name"]
    wb = Workbook()
    # ------------------------------------------------------------------ the decision
    ws = wb.active
    ws.title = "Decision"
    _title(ws, "Switch the Super and Kvarter stores to Kornblomst's forecast for 2027; keep To Go on AutoOrdre",
           "Expected saving per store and year against the 2027 licence, DKK excluding VAT (agreement FK-2026-014, 4.1 to 4.3 and Annex 2)")
    _head(ws, 4, ["Store format", "Stores", "Of which commuter-week", "Pilot stores", "Expected saving per store and year",
                  "80% range, low", "80% range, high", "Licence per store and year", "Saving less licence", "2027"],
          [14, 8, 13, 9, 16, 12, 12, 14, 13, 22])
    r = 5
    for f in FMT:
        ws.append([FMT_NAME[f], F["n_stores"][f], F["n_commuter"][f], F["n_pilot"][f], F["saving"][f], F["range"][f][0],
                   F["range"][f][1], F["licence"][f], F["margin_over_licence"][f],
                   "Switch to Kornblomst" if f in F["switch"] else "Stay on AutoOrdre"])
        r += 1
    _fmt(ws, range(5, r), range(5, 10), "#,##0")
    ws.append([])
    ws.append(["The saving is the waste avoided at cost plus the gross margin on fresh units gained, less the margin on units "
               "no longer sold, against the same store on AutoOrdre; a year is twice the 26 pilot weeks; each format's figure "
               "is the average over all its stores (4.2, 4.3)."])
    ws.append(["Each store's saving is carried from the pilot stores of its own trading week (weekend-trading or "
               "commuter-week), not of its own format: the forecast saves in stores that trade like a supermarket and loses "
               "in stores whose trade falls away at the weekend, and the three To Go pilot stores are high-street stores."])
    for rr in (r + 1, r + 2):
        ws.cell(row=rr, column=1).alignment = Alignment(wrap_text=False)
        ws.cell(row=rr, column=1).font = Font(size=9, color="52514E")
    ws.freeze_panes = "B5"
    # ------------------------------------------------------------------ the two gaps
    ws = wb.create_sheet("Gap causes")
    _title(ws, "Why the pilot stores' fresh sales grew less and their waste fell further than the other stores'",
           "Pilot weeks (ISO weeks 10 to 35, 2026) against the same weeks of 2025; percentage points of the pilot stores' 2025 figure")
    _head(ws, 4, ["Fresh sales growth", "Per cent / points"], [58, 16, 12])
    rows = [("Pilot stores' fresh sales growth, %", F["pilot_growth_pct"]),
            ("Other stores' fresh sales growth, %", F["other_growth_pct"]),
            ("Gap, points", F["sales_split"]["gap"]),
            ("of which Kornblomst's forecast at its recommended setting (sales the pilot stores' empty shelves turned away)",
             F["sales_split"]["forecast"]),
            ("of which the pilot stores' format mix (more Super, fewer To Go stores)", F["sales_split"]["format_mix"]),
            ("of which the competitor openings near pilot stores", F["sales_split"]["competitors"]),
            ("of which not explained by the three", F["sales_split"]["rest"])]
    for lab, v in rows:
        ws.append([lab, v])
    _fmt(ws, range(5, 5 + len(rows)), [2], "0.0")
    ws.append([])
    r0 = ws.max_row + 1
    _head(ws, r0, ["Fresh waste at cost", "Per cent / points"])
    rows = [("Pilot stores' change in fresh waste, %", F["pilot_waste_change_pct"]),
            ("Other stores' change in fresh waste, %", F["other_waste_change_pct"]),
            ("Gap, points", F["waste_split"]["gap"]),
            ("of which Kornblomst's forecast at its recommended setting", F["waste_split"]["forecast"]),
            ("of which the pilot stores' format mix", F["waste_split"]["format_mix"]),
            ("of which the competitor openings near pilot stores", F["waste_split"]["competitors"]),
            ("of which not explained by the three", F["waste_split"]["rest"])]
    for lab, v in rows:
        ws.append([lab, v])
    _fmt(ws, range(r0 + 1, r0 + 1 + len(rows)), [2], "0.0")
    ws.append([])
    ws.append(["Each format's own change, from its stores that kept AutoOrdre and had no opening near them: fresh sales "
               + ", ".join("%s %+.1f%%" % (f, F["growth_by_format_pct"][f]) for f in FMT) + "; waste "
               + ", ".join("%s %+.1f%%" % (f, F["waste_change_by_format_pct"][f]) for f in FMT) + "."])
    ws.cell(row=ws.max_row, column=1).font = Font(size=9, color="52514E")
    # ------------------------------------------------------------------ every store
    ws = wb.create_sheet("Stores")
    _title(ws, "Every store's expected saving per year on Kornblomst's forecast",
           "2025 figures are the same weeks as the pilot (ISO weeks 10 to 35); DKK excluding VAT; waste at cost")
    _head(ws, 4, ["Store", "Name", "Format", "Pilot", "Weekend share of fresh units 2025", "Trading week",
                  "Fresh sales 2025", "Fresh waste 2025", "Waste part per year", "Margin part per year",
                  "Expected saving per year"], [7, 30, 9, 7, 12, 13, 13, 12, 12, 12, 13])
    rw, rm = G["rates"]["waste"], G["rates"]["margin"]
    order = sorted(sp.index, key=lambda s: (FMT.index(sp.loc[s, "format"]), s))
    for s in order:
        t = sp.loc[s, "type"]
        wpart = rw[t] * sp.loc[s, "waste_base"] * 2
        mpart = rm[t] * sp.loc[s, "sales_base"] * 2
        ws.append([int(s), names[s], sp.loc[s, "format"], "yes" if sp.loc[s, "pilot"] else "", round(float(sp.loc[s, "weekend_share"]), 3),
                   "weekend-trading" if t == "weekend" else "commuter-week", round(float(sp.loc[s, "sales_base"])),
                   round(float(sp.loc[s, "waste_base"])), round(float(wpart)), round(float(mpart)), round(float(wpart + mpart))])
    n = len(order)
    _fmt(ws, range(5, 5 + n), [5], "0.000")
    _fmt(ws, range(5, 5 + n), range(7, 12), "#,##0")
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = "A4:K%d" % (4 + n)
    # ------------------------------------------------------------------ the pilot stores
    ws = wb.create_sheet("Pilot stores")
    _title(ws, "What Kornblomst's forecast saved in each pilot store over the 26 pilot weeks",
           "Against the same store on AutoOrdre: its 2025 figure carried by its format's change and by the trade an opening took; DKK")
    _head(ws, 4, ["Store", "Format", "Trading week", "Fresh waste 2025", "Waste expected on AutoOrdre", "Fresh waste 2026",
                  "Waste saving", "Margin change on units turned away", "Saving, 26 weeks"], [7, 9, 15, 12, 13, 12, 11, 15, 12])
    shares = GD.opening_share(R["T"], G["eff"])
    hit = set(G["eff"])
    ctrl = sp[(~sp["pilot"]) & (~sp.index.isin(hit))]
    rwf = ctrl.groupby("format")["waste_pilot"].sum() / ctrl.groupby("format")["waste_base"].sum()
    for s in sorted(P.index, key=lambda s: (FMT.index(P.loc[s, "format"]), s)):
        adj = (1 - shares.get((s, "pilot"), 0.0)) / (1 - shares.get((s, "base"), 0.0))
        exp_w = P.loc[s, "waste_base"] * rwf[P.loc[s, "format"]] * adj
        ws.append([int(s), P.loc[s, "format"], P.loc[s, "type"], round(float(P.loc[s, "waste_base"])), round(float(exp_w)),
                   round(float(P.loc[s, "waste_pilot"])), round(float(P.loc[s, "waste_saving"])),
                   round(float(P.loc[s, "margin_change"])), round(float(P.loc[s, "saving"]))])
    m = len(P)
    _fmt(ws, range(5, 5 + m), range(4, 10), "#,##0")
    ws.append([])
    r0 = ws.max_row + 1
    _head(ws, r0, ["Rate by trading week", "Weekend-trading", "Commuter-week"])
    ws.append(["Waste saving, % of the stores' 2025 fresh waste", F["waste_rate_pct"]["weekend"], F["waste_rate_pct"]["commuter"]])
    ws.append(["Margin change, % of the stores' 2025 fresh sales", F["margin_rate_pct"]["weekend"], F["margin_rate_pct"]["commuter"]])
    ws.append(["Kornblomst's weekend forecast over its working-day forecast, as a multiple of AutoOrdre's (every store, pilot weeks)",
               F["shadow_ratio"]["weekend"], F["shadow_ratio"]["commuter"]])
    ws.cell(row=r0 + 1, column=2).number_format = "0.0"
    ws.cell(row=r0 + 1, column=3).number_format = "0.0"
    ws.cell(row=r0 + 2, column=2).number_format = "0.00"
    ws.cell(row=r0 + 2, column=3).number_format = "0.00"
    ws.cell(row=r0 + 3, column=2).number_format = "0.00"
    ws.cell(row=r0 + 3, column=3).number_format = "0.00"
    ws.append([])
    ws.append(["A store's trading week is read from its own 2025 record: Saturday and Sunday's share of its fresh units, "
               "weekend-trading at %.2f or more (the widest gap between stores)." % F["weekend_cut"]])
    ws.cell(row=ws.max_row, column=1).font = Font(size=9, color="52514E")
    # ------------------------------------------------------------------ empty shelves
    ws = wb.create_sheet("Empty shelves")
    _title(ws, "Fresh units turned away by empty shelves",
           "A day's demand after the shelf emptied, from the time of its last sale and the hourly sales profile; units")
    _head(ws, 4, ["", "Same weeks 2025", "Pilot weeks 2026"], [52, 16, 16])
    ws.append(["Pilot stores", F["lost_units"]["pilot_2025"], F["lost_units"]["pilot_2026"]])
    ws.append(["Other stores", F["lost_units_other"]["other_2025"], F["lost_units_other"]["other_2026"]])
    ws.append(["Pilot stores, share of demand turned away, %", F["lost_share_pilot_2025_pct"], F["lost_share_pilot_2026_pct"]])
    _fmt(ws, [5, 6], [2, 3], "#,##0")
    _fmt(ws, [7], [2, 3], "0.0")
    ws.append([])
    _head(ws, 9, ["Check on the %s store-item days the shelf did not run out" % "{:,}".format(F["check_days"]), "All such days", "Days with six sales or fewer"])
    ws.append(["Sales so far over the share of the day gone, overstatement of the day's sales, %", F["check_plain_over_pct"], F["check_plain_over_small_pct"]])
    ws.append(["The same, one sale fewer, overstatement, %", F["check_os_over_pct"], F["check_os_over_small_pct"]])
    _fmt(ws, [10, 11], [2, 3], "0.0")
    ws.append([])
    ws.append(["On a day the shelf does not run out, the last sale is the day's last customer, so the day's demand is what "
               "sold; reading those days as if the shelf had emptied at the last sale shows which form overstates."])
    ws.cell(row=ws.max_row, column=1).font = Font(size=9, color="52514E")
    # ------------------------------------------------------------------ openings
    ws = wb.create_sheet("Openings")
    _title(ws, "Discounter openings near Fjordkøb stores in the record",
           "Effect on the store's ambient (non-fresh) trade, 2026 against the same weeks of 2025, against its format's stores with no opening")
    _head(ws, 4, ["Store", "Format", "Opened", "Distance, km", "Effect on trade, %"], [8, 10, 12, 12, 16])
    st = R["T"]["stores"].set_index("store")
    for s, e in sorted(G["eff"].items(), key=lambda kv: kv[1]["date"]):
        ws.append([int(s), st.loc[s, "format"], e["date"].strftime("%d %b %Y"), e["km"], F["competitor_effect_pct"][str(s)]])
    _fmt(ws, range(5, 5 + len(G["eff"])), [4], "0.0")
    _fmt(ws, range(5, 5 + len(G["eff"])), [5], "0.0")
    # ------------------------------------------------------------------ routes
    ws = wb.create_sheet("Routes")
    _title(ws, "What each way of reading the pilot gives",
           "Expected saving per store and year, DKK, and the formats it would switch")
    _head(ws, 4, ["Route", "Super", "Kvarter", "To Go", "Switches"], [70, 11, 11, 11, 26])
    routes = [("The answer: turned-away units from the last-sale time (one sale fewer), each store carried by its trading week",
               F["saving"], F["switch"]),
              ("Each format's saving read off its own pilot stores, plain turned-away estimate", F["careful"]["saving"], F["careful"]["switch"]),
              ("Each format's saving read off its own pilot stores", F["routes"]["by_format"]["saving"], F["routes"]["by_format"]["switch"]),
              ("By trading week, plain turned-away estimate", F["routes"]["plain_type"]["saving"], F["routes"]["plain_type"]["switch"]),
              ("By trading week, turned-away units from in-stock weekday averages", F["routes"]["instock_type"]["saving"], F["routes"]["instock_type"]["switch"]),
              ("By trading week, waste only", F["routes"]["waste_only_type"]["saving"], F["routes"]["waste_only_type"]["switch"]),
              ("By trading week, the whole saving carried on fresh sales", F["routes"]["single_sales_type"]["saving"], F["routes"]["single_sales_type"]["switch"]),
              ("By trading week, the margin part read off the recorded gross margin", F["routes"]["recorded_type"]["saving"], F["routes"]["recorded_type"]["switch"]),
              ("The dashboard's waste gap applied to every store's waste", F["quick"]["saving"], F["quick"]["switch"])]
    for lab, sv, sw in routes:
        ws.append([lab, sv["Super"], sv["Kvarter"], sv["To Go"], ", ".join(sw) if sw else "none"])
    _fmt(ws, range(5, 5 + len(routes)), [2, 3, 4], "#,##0")
    # ------------------------------------------------------------------ notes
    ws = wb.create_sheet("Notes")
    _title(ws, "Notes")
    notes = [
        "Pilot weeks: ISO weeks 10 to 35 of 2026 (2 March to 30 August). Same weeks of 2025: ISO weeks 10 to 35 of 2025.",
        "Sales are the extracts' sales excluding VAT; waste is the units written off at that year's cost price, as booked.",
        "The 2025 daily extract repeats %s store-item rows that the export job re-sent; each counted once." % "{:,}".format(F["duplicate_rows_2025"]),
        "Two dairy items were renumbered on 1 January 2026; the item register's former number joins them to 2025.",
        "A store that scans its write-offs the next morning books them on the next day; they are taken as booked.",
        "The BI weekly history's category codes changed at week 2 of 2026; the ambient (Kolonial) rows are read under both codes.",
        "Licence prices are Kornblomst's 2027 price list (agreement FK-2026-014, Annex 2), per store and year, excluding VAT.",
        "Ranges are the 10th and 90th percentiles of 400 resamples of the stores (pilot stores within their trading week, "
        "other stores within their format), every step redone.",
    ]
    for t in notes:
        ws.append([t])
    ws.column_dimensions["A"].width = 120
    wb.save(path)
    created, modified = STAMPS[WORKBOOK]
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, created, modified, excel=True, company=ORG)


def write_chart(path, F):
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=200)
    bg = "#fcfcfb"
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    order = ["To Go", "Kvarter", "Super"]
    for i, f in enumerate(order):
        col = BLUE if f in F["switch"] else ORANGE
        lo, hi = F["range"][f]
        ax.plot([lo / 1000, hi / 1000], [i, i], color=col, lw=2.2, solid_capstyle="round")
        ax.plot([F["saving"][f] / 1000], [i], "o", color=col, ms=8, mec=bg, mew=1.5, zorder=3)
        ax.plot([F["licence"][f] / 1000], [i], marker="|", color=INK2, ms=18, mew=2, zorder=4)
        ax.text(F["saving"][f] / 1000, i + 0.27, "{:,}".format(F["saving"][f]), ha="center", va="bottom", fontsize=8.5, color=INK)
        ax.text(F["licence"][f] / 1000, i - 0.30, "licence {:,}".format(F["licence"][f]), ha="center", va="top", fontsize=7.5, color=INK2)
    ax.axvline(0, color=RULE, lw=0.8)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=9, color=INK)
    ax.set_ylim(-0.7, len(order) - 0.35)
    ax.set_xlim(-10, 65)
    ax.set_xlabel("Expected saving per store and year, thousand DKK (dot), with 80% range (bar)", fontsize=8.5, color=INK2)
    ax.tick_params(axis="x", labelsize=8, colors=INK2)
    ax.tick_params(axis="y", length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.grid(axis="x", color="#e6e5df", lw=0.6)
    ax.set_axisbelow(True)
    ax.plot([], [], "o", color=BLUE, label="Switch for 2027")
    ax.plot([], [], "o", color=ORANGE, label="Stay on AutoOrdre")
    ax.plot([], [], marker="|", color=INK2, ls="", ms=10, mew=2, label="2027 licence")
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    ax.set_title("Super and Kvarter stores save more than the licence; To Go stores do not", fontsize=10, loc="left", color=INK, pad=8)
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)


SW, SH = 12192000, 6858000


def _box(slide, left, top, width, height, lines, size=16, color="0B0B0B", bold_first=False):
    tb = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = RGBColor.from_string(color)
        p.font.bold = bool(bold_first and i == 0)
        p.space_after = Pt(8)
    return tb


def _heading(slide, text):
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Emu(560000), Emu(300000), Emu(SW - 1120000), Emu(800000)
    t.text = text
    p = t.text_frame.paragraphs[0]
    p.alignment = 1
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor.from_string("0B0B0B")
    t.text_frame.word_wrap = True


def _foot(slide, n, total):
    _box(slide, 560000, SH - 430000, SW - 1120000, 300000,
         ["Fjordkøb supply chain planning with BI. Pilot agreement FK-2026-014, section 4. Workings in %s.   %d of %d"
          % (WORKBOOK, n, total)], size=10, color="7F7F7F")


def _table(slide, left, top, width, rows, widths, size=13):
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Emu(left), Emu(top), Emu(width), Emu(380000 * nr)).table
    for j, wd in enumerate(widths):
        gt.columns[j].width = Emu(int(width * wd))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = gt.cell(i, j)
            cell.text = str(val)
            for par in cell.text_frame.paragraphs:
                par.font.size = Pt(size)
                par.font.bold = i == 0
                par.alignment = 1 if j == 0 else 3
    return gt


def write_deck(path, F, png):
    sv, lic, rg = F["saving"], F["licence"], F["range"]
    k = lambda x: "{:,}".format(x)
    c = F["careful"]["saving"]
    total = 4
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(SW), Emu(SH)
    lay = prs.slide_layouts[5]
    # 1: the call
    s1 = prs.slides.add_slide(lay)
    _heading(s1, "Take Kornblomst's fresh forecast for the Super and Kvarter stores in 2027, not for To Go")
    s1.shapes.add_picture(png, Emu(560000), Emu(1250000), width=Emu(7300000))
    _box(s1, 8100000, 1350000, SW - 8100000 - 560000, 4700000, [
        "Expected saving per store and year against the 2027 licence:",
        "Super %s against %s" % (k(sv["Super"]), k(lic["Super"])),
        "Kvarter %s against %s" % (k(sv["Kvarter"]), k(lic["Kvarter"])),
        "To Go %s against %s" % (k(sv["To Go"]), k(lic["To Go"])),
        "80%% ranges: Super %s to %s, Kvarter %s to %s, To Go %s to %s." % (
            k(rg["Super"][0]), k(rg["Super"][1]), k(rg["Kvarter"][0]), k(rg["Kvarter"][1]), k(rg["To Go"][0]), k(rg["To Go"][1])),
        "Reading each format off its own pilot stores, every sale counted, switches %s (To Go %s a store, Kvarter %s, Super %s)."
        % (" and ".join(F["careful"]["switch"]) or "nothing", k(c["To Go"]), k(c["Kvarter"]), k(c["Super"]))],
        size=15, bold_first=True)
    _foot(s1, 1, total)
    # 2: the trading week
    s2 = prs.slides.add_slide(lay)
    _heading(s2, "The forecast saves where a store trades through the weekend, whatever its format")
    _box(s2, 560000, 1250000, SW - 1120000, 2300000, [
        "Kornblomst's chain-wide model reads every store's week like a big weekend store's: relative to the working days, "
        "its weekend forecast in a station or office store is %.2f times what the store's own history (AutoOrdre) gives, "
        "against %.2f in the other stores." % (F["shadow_ratio"]["commuter"], F["shadow_ratio"]["weekend"]),
        "Weekend-trading pilot stores avoided %.1f per cent of the fresh waste they would have written off; the "
        "commuter-week pilot stores %.1f per cent, and gave up margin on the working days." % (
            F["waste_rate_pct"]["weekend"], F["waste_rate_pct"]["commuter"]),
        "%s of the %s To Go stores trade a commuter week. The %s To Go stores in the pilot are high-street stores that do not."
        % (WORDS[F["n_commuter"]["To Go"]].capitalize(), WORDS[F["n_stores"]["To Go"]], WORDS[F["n_pilot"]["To Go"]])], size=16)
    rows = [["Trading week", "Waste saving, % of 2025 waste", "Margin change, % of 2025 fresh sales",
             "Stores (pilot)"],
            ["Weekend-trading", "%.1f" % F["waste_rate_pct"]["weekend"], "%.2f" % F["margin_rate_pct"]["weekend"],
             "%d (%d)" % (F["n_stores_total"] - sum(F["n_commuter"].values()), sum(F["n_pilot"].values()) - sum(F["n_commuter_pilot"].values()))],
            ["Commuter-week", "%.1f" % F["waste_rate_pct"]["commuter"], "%.2f" % F["margin_rate_pct"]["commuter"],
             "%d (%d)" % (sum(F["n_commuter"].values()), sum(F["n_commuter_pilot"].values()))]]
    _table(s2, 1400000, 3900000, SW - 2800000, rows, [0.28, 0.24, 0.30, 0.18], size=14)
    _foot(s2, 2, total)
    # 3: the gaps
    s3 = prs.slides.add_slide(lay)
    _heading(s3, "The dashboard's two gaps are not the saving: they carry the format mix and two discounter openings")
    ss, ws = F["sales_split"], F["waste_split"]
    rows = [["Pilot against other stores, same weeks of 2025", "Fresh sales growth", "Fresh waste at cost"],
            ["Pilot stores, %", "%.1f" % F["pilot_growth_pct"], "%.1f" % F["pilot_waste_change_pct"]],
            ["Other stores, %", "%.1f" % F["other_growth_pct"], "%.1f" % F["other_waste_change_pct"]],
            ["Gap, points", "%.1f" % ss["gap"], "%.1f" % ws["gap"]],
            ["Kornblomst's forecast and its recommended setting", "%.1f" % ss["forecast"], "%.1f" % ws["forecast"]],
            ["Format mix (fewer To Go stores in the pilot)", "%.1f" % ss["format_mix"], "%.1f" % ws["format_mix"]],
            ["Discounter openings near pilot stores", "%.1f" % ss["competitors"], "%.1f" % ws["competitors"]],
            ["Not explained", "%.1f" % ss["rest"], "%.1f" % ws["rest"]]]
    _table(s3, 1000000, 1350000, SW - 2000000, rows, [0.52, 0.24, 0.24], size=14)
    _box(s3, 1000000, 4700000, SW - 2000000, 1200000, [
        "Each format's own change comes from its stores that kept AutoOrdre and had no opening nearby: fresh sales %s per "
        "cent in Super, %s in Kvarter and %s in To Go." % ("%.1f" % F["growth_by_format_pct"]["Super"],
                                                          "%.1f" % F["growth_by_format_pct"]["Kvarter"],
                                                          "%.1f" % F["growth_by_format_pct"]["To Go"])], size=14)
    _foot(s3, 3, total)
    # 4: empty shelves and the routes
    s4 = prs.slides.add_slide(lay)
    _heading(s4, "Empty shelves are the cost the waste figures do not show")
    _box(s4, 560000, 1250000, SW - 1120000, 1700000, [
        "The pilot stores turned away about %s fresh units in the pilot weeks against %s in the same weeks of 2025 (%.1f and "
        "%.1f per cent of demand), read from each sold-out day's last sale against BI's hourly profile, one sale fewer than "
        "made: counting every sale overstates an in-stock day's sales by %.1f per cent." % (
            k(F["lost_units"]["pilot_2026"]), k(F["lost_units"]["pilot_2025"]), F["lost_share_pilot_2026_pct"],
            F["lost_share_pilot_2025_pct"], F["check_plain_over_pct"])], size=15)
    r = F["routes"]
    rows = [["How the pilot is read", "Super", "Kvarter", "To Go", "Switches"],
            ["The answer", k(sv["Super"]), k(sv["Kvarter"]), k(sv["To Go"]), ", ".join(F["switch"])],
            ["By format, every sale counted", k(c["Super"]), k(c["Kvarter"]), k(c["To Go"]), ", ".join(F["careful"]["switch"])],
            ["By format", k(r["by_format"]["saving"]["Super"]), k(r["by_format"]["saving"]["Kvarter"]),
             k(r["by_format"]["saving"]["To Go"]), ", ".join(r["by_format"]["switch"])],
            ["By trading week, saving carried on fresh sales", k(r["single_sales_type"]["saving"]["Super"]),
             k(r["single_sales_type"]["saving"]["Kvarter"]), k(r["single_sales_type"]["saving"]["To Go"]),
             ", ".join(r["single_sales_type"]["switch"]) or "none"],
            ["By trading week, every sale counted", k(r["plain_type"]["saving"]["Super"]), k(r["plain_type"]["saving"]["Kvarter"]),
             k(r["plain_type"]["saving"]["To Go"]), ", ".join(r["plain_type"]["switch"])],
            ["The dashboard's waste gap on every store", k(F["quick"]["saving"]["Super"]), k(F["quick"]["saving"]["Kvarter"]),
             k(F["quick"]["saving"]["To Go"]), ", ".join(F["quick"]["switch"])]]
    _table(s4, 560000, 3050000, SW - 1120000, rows, [0.36, 0.13, 0.13, 0.13, 0.25], size=13)
    _foot(s4, 4, total)
    prs.save(path)
    created, modified = STAMPS[NOTE]
    PP.normalize_pptx(path, AUTHOR, "Jakob Lauritsen", created, modified, "Kornblomst Fresh Forecast 2027", ORG,
                      revision=9, total_time=118)


def write_all(R, F, golden_dir, scratch):
    os.makedirs(golden_dir, exist_ok=True)
    for nm in os.listdir(golden_dir):
        os.remove(os.path.join(golden_dir, nm))
    png = os.path.join(scratch, "saving_vs_licence.png")
    write_chart(png, F)
    write_workbook(os.path.join(golden_dir, WORKBOOK), R, F)
    write_deck(os.path.join(golden_dir, NOTE), F, png)
    return png
