"""task9: the golden deliverable the prompt asks for (a short deck for the module review), written from the figures as
computed and as stated (F). Nothing is typed: every number below is read from F.

    write_all(F, golden_dir)

The deck passes through the house container writer with its own stamps after the pack's.
"""
import datetime as dt
import os

from pptx import Presentation
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

import params as P
import postprocess as PP

DECK = "tessaline_fab2_edge_ring_review.pptx"
FILES = [DECK]
AUTHOR = "Fab 2 Yield Engineering"
STAMPS = {DECK: ("2026-09-08T15:12:00Z", "2026-09-10T18:41:00Z")}
INK, INK2 = RGBColor(0x1A, 0x1A, 0x1A), RGBColor(0x55, 0x55, 0x55)
BLUE, ORANGE, GRAY = RGBColor(0x2A, 0x6F, 0xB8), RGBColor(0xD9, 0x6A, 0x1E), RGBColor(0x9A, 0x9A, 0x9A)
HEAD, TOTAL, WHITE = RGBColor(0x33, 0x40, 0x52), RGBColor(0xEE, 0xF0, 0xF3), RGBColor(0xFF, 0xFF, 0xFF)
W16, H9 = Emu(12192000), Emu(6858000)
LABEL = {"disk": "Conditioner disk wear", "pad": "Pad life (on top of the disk's wear)", "ring": "Retaining ring wear",
         "dep3": "Deposition chamber DEP-3", "sc4": "Scanner SC-4 at M1", "rf": "Deposition chambers' RF hours"}
PRODUCT = {"P-A": "P-A (MCU32)", "P-B": "P-B (MCU64)", "P-C": "P-C (MCU16)"}


def n(v):
    return "{:,}".format(int(round(v)))


def usd(v):
    return "USD " + n(v)


def pct(v, k=0):
    return ("%." + str(k) + "f%%") % (100 * v)


def _text(slide, x, y, w, h, paras, size=16, color=INK, bold_first=False, space=8):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for k, t in enumerate(paras):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text = t
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.bold = bold_first and k == 0
        p.space_after = Pt(space)
    return tb


def _title_of(slide, text):
    slide.shapes.title.text = text
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.6), Inches(0.35), Inches(12.1), Inches(1.0)
    for p in t.text_frame.paragraphs:
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = INK
        p.alignment = PP_ALIGN.LEFT


def _source(slide, text):
    _text(slide, Inches(0.6), Inches(6.9), Inches(12.1), Inches(0.4), [text], size=10, color=INK2)


def _table(slide, x, y, w, rows, widths, size=12, header=True):
    shp = slide.shapes.add_table(len(rows), len(rows[0]), x, y, w, Inches(0.32) * len(rows))
    tb = shp.table
    tb.horz_banding = False
    for j, wd in enumerate(widths):
        tb.columns[j].width = wd
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = tb.cell(i, j)
            c.text = str(v)
            c.fill.solid()
            c.fill.fore_color.rgb = HEAD if (header and i == 0) else (TOTAL if str(r[0]).startswith(("All ", "Four ")) else WHITE)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(size)
                p.font.bold = (header and i == 0) or str(r[0]).startswith(("All ", "Four "))
                p.font.color.rgb = WHITE if (header and i == 0) else INK
                if j > 0:
                    p.alignment = PP_ALIGN.RIGHT
    return tb


def _axes(ch, size=11):
    ch.font.size = Pt(size)
    ch.font.color.rgb = INK2
    for ax in (ch.category_axis, ch.value_axis):
        ax.has_major_gridlines = ax is ch.value_axis
        ax.format.line.color.rgb = GRAY
        ax.tick_labels.font.size = Pt(size)
    ch.value_axis.major_gridlines.format.line.color.rgb = RGBColor(0xE2, 0xE2, 0xE2)


def _line_chart(s, x, y, w, h, series, title, xlab, ylab, colors, dashed=()):
    xy = XyChartData()
    for name, pts in series:
        se = xy.add_series(name)
        for a, b in pts:
            se.add_data_point(a, b)
    gf = s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES, x, y, w, h, xy)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(10)
    _axes(ch)
    for k, (ser, colr) in enumerate(zip(ch.plots[0].series, colors)):
        ser.format.line.color.rgb = colr
        ser.format.line.width = Pt(2)
        if k in dashed:
            ser.format.line.dash_style = 4
        ser.marker.style = XL_MARKER_STYLE.CIRCLE
        ser.marker.size = 6
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = colr
        ser.marker.format.line.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        ser.smooth = False
    ch.has_title = True
    ch.chart_title.text_frame.text = title
    ch.chart_title.text_frame.paragraphs[0].font.size = Pt(12)
    for ax, label in ((ch.category_axis, xlab), (ch.value_axis, ylab)):
        ax.has_title = True
        ax.axis_title.text_frame.text = label
        ax.axis_title.text_frame.paragraphs[0].font.size = Pt(11)
        ax.axis_title.text_frame.paragraphs[0].font.bold = False
    return ch


def write_deck(path, F):
    S, B, G = F["stated"], F["bands"], F["gold"]
    A = F["A"]
    lo, hi = A.pairs["low"], A.pairs["high"]
    pr = Presentation()
    pr.slide_width, pr.slide_height = W16, H9
    layout = pr.slide_layouts[5]
    c = S["REC_counts"]
    dose = S["R4_dose"]
    L1 = S["R1_loss"]
    lot = F["fwd_lot"]
    lotn = lot.split("-")[-1]
    psi = F["downforce"]

    # 1. the answer
    s = pr.slides.add_slide(layout)
    _title_of(s, "Change the conditioner disk on its own count: %s wafers on %s and %s, %s on %s and %s" % (
        n(c[lo[0]]), lo[0], lo[1], n(c[hi[0]]), hi[0], hi[1]))
    _text(s, Inches(0.6), Inches(1.55), Inches(12.1), Inches(5.2), [
        "The edge ring cost %s points of mean wafer sort yield on wafers sorted 1 April to 31 August: %s good die of P-A, %s of "
        "P-B and %s of P-C, about %s at the cost inputs' die values." % (
            "%.2f" % L1["points"], n(L1["P-A die"]), n(L1["P-B die"]), n(L1["P-C die"]), usd(S["R1_usd"])),
        "It is the conditioner disk's own wear (%s of the loss, the pad's life adding %s on top of it). The retaining ring, "
        "DEP-3, SC-4 and the deposition chambers' RF hours each account for none of it." % (
            pct(S["R2_shares"]["disk"], 1), pct(S["R2_shares"]["pad"], 1)),
        "Final test scrapped %s more units of the same wafers at burn-in on the lots it finished in those months: %s of P-A, "
        "%s of P-B and %s of P-C, about %s with their assembly and test." % (
            n(S["R3_total"]), n(S["R3_ft_units"]["P-A"]), n(S["R3_ft_units"]["P-B"]), n(S["R3_ft_units"]["P-C"]), usd(S["R3_usd"])),
        "The disks stores issue now are lot %s, the lot on all four units since %s, and they wear faster than the lots before "
        "them: the loss at sort starts at %s wafers of a disk's use on %s and %s and at %s on %s and %s, and climbs %s and %s "
        "points of the outer zone's fail rate per 1,000 wafers after it." % (
            lotn, F["fwd_all_since"], n(dose["%s onset" % lo[0]]), lo[0], lo[1], n(dose["%s onset" % hi[0]]), hi[0], hi[1],
            "%.1f" % dose["%s climb" % lo[0]], "%.1f" % dose["%s climb" % hi[0]]),
        "At these counts the module saves about %s a year against Rev F as it stands. Counts set on every lot's curve, or with "
        "final test left out or taken in proportion to the sort loss, would sit %d to %d per cent longer and give back part of "
        "that." % (usd(S["R5_saving"]), F["shortcut_range"][0], F["shortcut_range"][1]),
    ], size=16)
    _source(s, "Sort, MES, FDC and PM records 5 January to 31 August 2026; stores receipts; final test lot summary; cost inputs of "
               "28 August 2026; YE-2026-031.")

    # 2. the loss at sort
    s = pr.slides.add_slide(layout)
    _title_of(s, "The ring cost %s points of sort yield from April to August, and it was there in the first quarter" % (
        "%.2f" % L1["points"]))
    cd = CategoryChartData()
    months = sorted(F["monthly"])
    cd.categories = [dt.date.fromisoformat(m + "-01").strftime("%b") for m in months]
    cd.add_series("Ring loss, points of mean wafer sort yield", [round(F["monthly"][m], 2) for m in months])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.5), Inches(7.0), Inches(5.0), cd)
    ch = gf.chart
    ch.has_legend = False
    _axes(ch)
    plot = ch.plots[0]
    plot.gap_width = 60
    ser = plot.series[0]
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = BLUE
    plot.has_data_labels = True
    plot.data_labels.number_format = "0.00"
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.font.size = Pt(10)
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    ch.has_title = True
    ch.chart_title.text_frame.text = "Ring loss by sort month, points of mean wafer sort yield"
    ch.chart_title.text_frame.paragraphs[0].font.size = Pt(12)
    rows = [["Product", "Good die lost", "Value at the cost inputs"]]
    for p in ("P-A", "P-B", "P-C"):
        rows.append([PRODUCT[p], n(L1["%s die" % p]), usd(S["R1_usd_by"][p])])
    rows.append(["All products", n(sum(L1["%s die" % p] for p in ("P-A", "P-B", "P-C"))), usd(S["R1_usd"])])
    _table(s, Inches(7.9), Inches(1.6), Inches(4.8), rows, [Inches(1.8), Inches(1.4), Inches(1.6)], size=12)
    _text(s, Inches(7.9), Inches(3.5), Inches(4.8), Inches(3.2), [
        "Each wafer's outermost zone is set against its own interior fail rate plus the zone's fallout on disks short of their "
        "onset (%s to %s of the zone's die), on every sorted wafer, a retest replacing its first pass." % (
            pct(min(f["r0"] for f in G["fits"].values()), 1), pct(max(f["r0"] for f in G["fits"].values()), 1)),
        "The ring already cost %s points on wafers sorted January to March; measured against that quarter's level the April to "
        "August loss would read %s." % ("%.2f" % G["R1_q1"], "%.2f" % F["routes"]["R1_q1_baseline"]),
        "The classifier's EDGE_RING wafers carry %s of the loss; the rest sits on wafers it labels otherwise." % pct(1 - G["unflagged_share"]),
    ], size=12)
    _source(s, "%s wafers sorted 1 April to 31 August 2026 (%s in the record); good die at the cost inputs' values per good die." % (
        n(F["n_window"]), n(F["record"]["sorted"])))

    # 3. the cause
    s = pr.slides.add_slide(layout)
    _title_of(s, "The conditioner disk's own wear carries the loss; the rivals carry none of it")
    rows = [["Candidate", "Share of the loss"]]
    for k in ("disk", "pad", "ring", "dep3", "sc4", "rf"):
        rows.append([LABEL[k], pct(S["R2_shares"][k], 1)])
    _table(s, Inches(0.6), Inches(1.6), Inches(5.6), rows, [Inches(4.0), Inches(1.6)], size=13)
    steps = [x[2] for x in G["ring_swaps"]]
    t_cl = max(abs(t[1]) for t in G["ring_t"].values())
    _text(s, Inches(6.6), Inches(1.55), Inches(6.1), Inches(5.2), [
        "The disk, the pad and the retaining ring are changed together at a full PM, so their counters move together. The log's "
        "own exceptions separate them: the disk-only swaps change the disk alone, the EW-118 PMs replace pad and ring and leave it.",
        "The six ring-only swaps leave the outer zone where it was: the step at each runs from %+.3f to %+.3f." % (min(steps), max(steps)),
        "One fit per pair over every disk gives the retaining ring a share below zero, with a t of %.1f at most once each disk's "
        "life is the unit that varies; fitted on each disk lot it has none." % t_cl,
        "DEP-3 sends most of its wafers to %s and %s, which is all its apparent link; SC-4 joined M1 a week after Rev F. "
        "Neither moves the outer zone on wafers with the same disk use." % (hi[0], hi[1]),
    ], size=13)
    _source(s, "Shares of the April to August loss, one model per downforce pair and disk lot with every candidate beside it; a "
               "share below zero is shown as none.")

    # 4. the disks
    s = pr.slides.add_slide(layout)
    _title_of(s, "Lot %s's disks start the ring at %s wafers on %s and %s and at %s on %s and %s" % (
        lotn, n(dose["%s onset" % lo[0]]), lo[0], lo[1], n(dose["%s onset" % hi[0]]), hi[0], hi[1]))
    series = []
    for p, us in (("low", lo), ("high", hi)):
        for lab in ("earlier", "current"):
            nm = "%s/%s, %s" % (us[0], us[1], "lot %s" % lotn if lab == "current" else "earlier lots")
            series.append((nm, [(x, round(100 * y, 2)) for x, y, _ in F["binned"]["%s %s" % (p, lab)]]))
    _line_chart(s, Inches(0.6), Inches(1.5), Inches(7.4), Inches(5.0), series,
                "Outermost zone's excess over the interior, by wafers of disk use", "Wafers since the disk was changed",
                "Excess fail rate, points", (BLUE, BLUE, ORANGE, ORANGE), dashed=(0, 2))
    rows = [["Unit", "Onset (wafers)", "Climb after it"]]
    for u in lo + hi:
        rows.append([u, n(dose["%s onset" % u]), "%.1f" % dose["%s climb" % u]])
    _table(s, Inches(8.3), Inches(1.6), Inches(4.4), rows, [Inches(1.2), Inches(1.5), Inches(1.7)], size=12)
    old = F["old_onsets"]
    _text(s, Inches(8.3), Inches(3.4), Inches(4.4), Inches(3.3), [
        "Climb: points of the outermost zone's fail rate per 1,000 wafers of disk use past the onset, at a pad half through its life.",
        "Each disk's lot comes from the serial its PM entry fitted, in the serial range stores received. The earlier lots start "
        "the ring at %s wafers on %s and %s and %s on %s and %s; the %s receipt is the only lot left on the shelf (%s disks)." % (
            n(old["low"]), lo[0], lo[1], n(old["high"]), hi[0], hi[1], F["fwd_received"], n(F["stock_left"][lot])),
        "Each pair is fitted together: its two units run one downforce recipe (%.2f and %.2f psi), and %s and %s have run one "
        "short disk each from this lot." % (psi["low"], psi["high"], F["short_units"][0], F["short_units"][1]),
    ], size=12)
    _source(s, "Every polished wafer 5 January to 16 August, in bins of 200 wafers of disk use with 60 wafers or more.")

    # 5. final test
    s = pr.slides.add_slide(layout)
    _title_of(s, "Final test lost %s more units to the same wear, and its losses start before the ring shows at sort" % n(S["R3_total"]))
    cd = CategoryChartData()
    fm = sorted(m for m in F["ft_monthly"] if m >= "2026-02")
    cd.categories = [dt.date.fromisoformat(m + "-01").strftime("%b") for m in fm]
    cd.add_series("Burn-in failures, per cent of units in", [round(F["ft_monthly"][m]["burnin_pct"], 3) for m in fm])
    cd.add_series("of which the ring's, per cent of units in", [round(F["ft_monthly"][m]["ring_pct"], 3) for m in fm])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(1.5), Inches(7.0), Inches(5.0), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(10)
    _axes(ch)
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.overlap = 0
    for ser, colr in zip(plot.series, (GRAY, ORANGE)):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = colr
    plot.has_data_labels = True
    plot.data_labels.number_format = "0.00"
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.font.size = Pt(9)
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    ch.has_title = True
    ch.chart_title.text_frame.text = "Burn-in failures by final-test month"
    ch.chart_title.text_frame.paragraphs[0].font.size = Pt(12)
    rows = [["Product", "Units lost at final test", "Value with assembly and test"]]
    for p in ("P-A", "P-B", "P-C"):
        rows.append([PRODUCT[p], n(S["R3_ft_units"][p]), usd(S["R3_usd_by"][p])])
    rows.append(["All products", n(S["R3_total"]), usd(S["R3_usd"])])
    _table(s, Inches(7.9), Inches(1.6), Inches(4.8), rows, [Inches(1.6), Inches(1.5), Inches(1.7)], size=12)
    _text(s, Inches(7.9), Inches(3.5), Inches(4.8), Inches(3.2), [
        "Each lot's burn-in failures are its units at the base rate (%s per cent) plus a share of its wafers' outer-zone good die "
        "that rises with each disk's wear and levels off at %s per cent." % ("%.2f" % S["ft_base"], "%.1f" % S["ft_level"]),
        "It starts at %s wafers of disk use on %s and %s and %s on %s and %s, and is full by %s and %s: well before the ring "
        "shows at sort." % (n(S["ft_start"][lo[0]]), lo[0], lo[1], n(S["ft_start"][hi[0]]), hi[0], hi[1],
                            n(S["ft_full"][lo[0]]), n(S["ft_full"][hi[0]])),
        "Taking burn-in in proportion to the ring's die at sort reads %s units; a base from the lots with no ring label reads %s." % (
            n(round(sum(F["routes"]["R3_proportional"].values()), -2)), n(round(sum(F["routes"]["R3_clean_lot_base"].values()), -2))),
    ], size=12)
    _source(s, "%s lots finished at final test 1 April to 31 August 2026 (%s in the summary), sub-lots added back to their lot." % (
        n(F["record"]["ft_lots_window"]), n(F["record"]["ft_lots"])))

    # 6. the count
    s = pr.slides.add_slide(layout)
    _title_of(s, "Rev G: the disk on its own count saves about %s a year against Rev F" % usd(S["R5_saving"]))
    rows = [["Unit", "Count (wafers)", "Rev F, USD per wafer", "Rev G, USD per wafer", "Saving a year"]]
    for u in lo + hi:
        cpw = F["cost_per_wafer"][A.pair_of[u]]
        rows.append([u, n(c[u]), "%.2f" % cpw["Rev F as it stands"], "%.2f" % cpw["Rev G at the pair's count"],
                     usd(round(G["R5_unit"][u], -2))])
    rows.append(["Four units", "", "", "", usd(sum(round(G["R5_unit"][u], -2) for u in lo + hi))])
    _table(s, Inches(0.6), Inches(1.6), Inches(12.1), rows, [Inches(1.6), Inches(2.2), Inches(2.9), Inches(2.9), Inches(2.5)], size=13)
    pert = F["perturbations"]
    lo_rng = (min(v[lo[0]] for v in pert.values()), max(v[lo[0]] for v in pert.values()))
    hi_rng = (min(v[hi[0]] for v in pert.values()), max(v[hi[0]] for v in pert.values()))
    R = F["routes"]
    _text(s, Inches(0.6), Inches(4.0), Inches(12.1), Inches(2.8), [
        "Cost per wafer counts the maintenance (the full PM every 2,800 wafers, less the disk's price under Rev G, and each disk "
        "change at its all-in of %s), the good die the ring takes at sort and the units final test scraps, each at the plan's "
        "product mix." % usd(A.allin["disk_change"]),
        "The count is where a disk's cost per wafer of changes and ring loss is lowest. It stays between %s and %s on %s and %s "
        "and between %s and %s on %s and %s with every climb 15 per cent either way, every onset 5 per cent, final test's level "
        "15 per cent, its start 8 per cent or its span 20 per cent, the die values or the disk change 10 per cent." % (
            n(round(lo_rng[0], -1)), n(round(lo_rng[1], -1)), lo[0], lo[1], n(round(hi_rng[0], -1)), n(round(hi_rng[1], -1)), hi[0], hi[1]),
        "Set on every lot's curve the counts would be %s and %s; with final test left out, %s and %s; with final test in "
        "proportion to the sort loss, %s and %s." % (
            n(round(R["REC_pooled"][lo[0]], -1)), n(round(R["REC_pooled"][hi[0]], -1)), n(round(R["REC_sort_only"][lo[0]], -1)),
            n(round(R["REC_sort_only"][hi[0]], -1)), n(round(R["REC_proportional"][lo[0]], -1)), n(round(R["REC_proportional"][hi[0]], -1))),
    ], size=13)
    _source(s, "The FY27 plan's wafers per unit and product mix; cost inputs of 28 August 2026. Counts rounded to 10 wafers, savings "
               "to USD 100 in the table and to USD 1,000 in the title.")

    # 7. notes
    s = pr.slides.add_slide(layout)
    _title_of(s, "How the figures were built")
    _text(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(5.3), [
        "Records: the sort database (latest record per wafer, aliases mapped to P-A, P-B and P-C), the MES chamber steps, the "
        "units' polish record and maintenance log. Each part's use is counted from its own last replacement in the log's parts "
        "text, blank counters placed on the unit's polish record by time; each disk's lot from its fitted serial and the stores "
        "receipts' serial ranges.",
        "Loss at sort: each wafer's outermost-zone fails less its tested die times its interior fail rate plus the zone's fallout "
        "on disks short of their onset; averaged over wafers as points of sort yield and summed by product as good die.",
        "Dose: weighted least squares of the outermost zone's excess over the interior on a hinge in the disk's use, the pad's "
        "life multiplying the slope, the onset profiled, one fit per downforce pair and disk lot.",
        "Causes: the same model with the retaining ring's use, DEP-3, SC-4 and the chambers' RF hours beside it; each share is "
        "that term's loss over the window; the ring-only swaps checked as before-and-after steps.",
        "Final test: Poisson regression of each lot's burn-in failures on its units and on its wafers' outer-zone good die times "
        "a rise in the disk's use as a share of its lot's onset, the rise's start and span profiled.",
        "Count and saving: the count minimises the disk's cost per wafer on the pair's current-lot curve with both stages of "
        "loss; the saving is against Rev F's own 2,800-wafer cycle on the same disks.",
    ], size=13, space=10)
    for k, sl in enumerate(pr.slides, 1):
        _text(sl, Inches(12.2), Inches(6.9), Inches(0.6), Inches(0.4), [str(k)], size=10, color=INK2)
    pr.save(path)
    PP.normalize_pptx(path, AUTHOR, AUTHOR, STAMPS[DECK][0], STAMPS[DECK][1], "Fab 2 edge ring: cause, cost and the Rev G disk count",
                      P.FIRM)


def write_all(F, gold):
    os.makedirs(gold, exist_ok=True)
    write_deck(os.path.join(gold, DECK), F)
