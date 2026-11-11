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
    for j, wd in enumerate(widths):
        tb.columns[j].width = wd
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = tb.cell(i, j)
            c.text = str(v)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(size)
                p.font.bold = header and i == 0
                p.font.color.rgb = INK
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


def write_deck(path, F):
    S, B, G = F["stated"], F["bands"], F["gold"]
    A = F["A"]
    lo, hi = A.pairs["low"], A.pairs["high"]
    pr = Presentation()
    pr.slide_width, pr.slide_height = W16, H9
    layout = pr.slide_layouts[5]
    c = S["R6_counts"]
    dose = S["R4_dose"]

    # 1. the answer
    s = pr.slides.add_slide(layout)
    _title_of(s, "Change the conditioner disk on its own count: %s wafers on %s and %s, %s on %s and %s" % (
        n(c[lo[0]]), lo[0], lo[1], n(c[hi[0]]), hi[0], hi[1]))
    _text(s, Inches(0.6), Inches(1.55), Inches(12.1), Inches(5.2), [
        "The edge ring cost %s points of mean wafer sort yield on wafers sorted 1 April to 31 August: %s good die of P-A, %s of "
        "P-B and %s of P-C, about %s at the cost inputs' die values." % (
            "%.2f" % S["R1_points"], n(S["R2_die"]["P-A"]), n(S["R2_die"]["P-B"]), n(S["R2_die"]["P-C"]), usd(S["R2_usd"])),
        "It is the conditioner disk's own wear (%s of the loss, the pad's life adding %s on top of it). The retaining ring, "
        "DEP-3, SC-4 and the deposition chambers' RF hours each account for none of it." % (
            pct(S["R3_shares"]["disk"], 1), pct(S["R3_shares"]["pad"], 1)),
        "The loss starts at %s wafers of a disk's use on %s and %s and at %s on %s and %s, whose higher downforce wears the "
        "disk faster." % (n(dose["%s onset" % lo[0]]), lo[0], lo[1], n(dose["%s onset" % hi[0]]), hi[0], hi[1]),
        "Of the loss, %s is what the 2,000-wafer rule would have cost anyway, %s is what Rev F's move to 2,800 added and %s is "
        "what the EW-118 retained disks added." % (pct(S["R5_bridge"]["old_rule"]), pct(S["R5_bridge"]["rev_f"]),
                                                   pct(S["R5_bridge"]["ew118"])),
        "With the disk out of the full PM at these counts, the module saves about %s a year against Rev F as it stands. One count "
        "for all four units would give back %s of that, and going back to Rev E would cost %s a year more than Rev G." % (
            usd(S["R7_saving"]), usd(F["fleet_vs_g"]), usd(F["rev_e_vs_g"])),
    ], size=17)
    _source(s, "Sort, MES, FDC and PM records 5 January to 31 August 2026; cost inputs of 28 August 2026; YE-2026-031.")

    # 2. the loss
    s = pr.slides.add_slide(layout)
    _title_of(s, "The ring cost %s points of sort yield from April to August, and it was already there in the first quarter" %
              ("%.2f" % S["R1_points"]))
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
        rows.append([PRODUCT[p], n(S["R2_die"][p]), usd(S["R2_die"][p] * A.value[p])])
    rows.append(["All products", n(sum(S["R2_die"].values())), usd(S["R2_usd"])])
    _table(s, Inches(7.9), Inches(1.6), Inches(4.8), rows, [Inches(1.8), Inches(1.4), Inches(1.6)], size=12)
    _text(s, Inches(7.9), Inches(3.5), Inches(4.8), Inches(3.2), [
        "Each wafer's outermost zone is set against its own interior fail rate plus the zone's fallout at a fresh disk (%s of "
        "the zone's die), on every sorted wafer, a retest replacing its first pass." % pct(G["r0"]["low"], 1),
        "The ring already cost %s points on wafers sorted January to March, on disks past their onset under the 2,000-wafer "
        "rule; measured against that quarter's level the April to August loss would read %s." % (
            "%.2f" % G["R1_q1"], "%.2f" % F["routes"]["R1_q1_baseline"]),
        "The classifier's EDGE_RING wafers carry %s of the loss; the rest sits on wafers it labels otherwise." % pct(1 - G["unflagged_share"]),
    ], size=12)
    _source(s, "%s wafers sorted 1 April to 31 August 2026 (%s in the record); good die at the cost inputs' values per good die." % (
        n(F["n_window"]), n(F["record"]["sorted"])))

    # 3. the cause
    s = pr.slides.add_slide(layout)
    _title_of(s, "The conditioner disk's own wear carries the loss; the rivals carry none of it")
    rows = [["Candidate", "Share of the loss"]]
    for k in ("disk", "pad", "ring", "dep3", "sc4", "rf"):
        rows.append([LABEL[k], pct(S["R3_shares"][k], 1)])
    _table(s, Inches(0.6), Inches(1.6), Inches(5.6), rows, [Inches(4.0), Inches(1.6)], size=13)
    steps = [x[2] for x in G["ring_swaps"]]
    t_iid = max(t[0] for t in G["ring_t"].values())
    t_cl = max(abs(t[1]) for t in G["ring_t"].values())
    _text(s, Inches(6.6), Inches(1.55), Inches(6.1), Inches(5.2), [
        "The disk, the pad and the retaining ring are changed together at a full PM, so their counters move together. The log's "
        "own exceptions separate them: the disk-only swaps take the ring away, the EW-118 PMs replace pad and ring and leave it.",
        "The six ring-only swaps leave the outer zone where it was: the step at each runs from %+.3f to %+.3f." % (min(steps), max(steps)),
        "Each disk wears at its own rate. A fit that reads every wafer as independent gives the retaining ring %s of the loss "
        "with a t of %.0f; with each disk's life as the unit that varies its t is %.1f at most, and a fit with each disk's own "
        "slope puts it at %s." % (pct(F["routes"]["R3_joint"]["ring"], 1), t_iid, t_cl, pct(S["R3_shares"]["ring"], 1)),
        "DEP-3 sends most of its wafers to %s and %s, which is all its apparent link; SC-4 joined M1 a week after Rev F. "
        "Neither moves the outer zone on wafers with the same disk use." % (hi[0], hi[1]),
    ], size=13)
    _source(s, "Shares of the April to August loss, one model per downforce pair with each disk life's own slope and every candidate beside it.")

    # 4. the dose
    s = pr.slides.add_slide(layout)
    _title_of(s, "The loss starts at %s wafers of disk use on %s and %s and at %s on %s and %s" % (
        n(dose["%s onset" % lo[0]]), lo[0], lo[1], n(dose["%s onset" % hi[0]]), hi[0], hi[1]))
    xy = XyChartData()
    for p, col_name in (("low", "%s and %s (%.2f psi)" % (lo[0], lo[1], P.UNIT_DOWNFORCE[lo[0]])),
                        ("high", "%s and %s (%.2f psi)" % (hi[0], hi[1], P.UNIT_DOWNFORCE[hi[0]]))):
        se = xy.add_series(col_name)
        for x, y, _ in F["binned"][p]:
            se.add_data_point(x, round(100 * y, 2))
    gf = s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES, Inches(0.6), Inches(1.5), Inches(7.4), Inches(5.0), xy)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(11)
    _axes(ch)
    for ser, colr in zip(ch.plots[0].series, (BLUE, ORANGE)):
        ser.format.line.color.rgb = colr
        ser.format.line.width = Pt(2)
        ser.marker.style = XL_MARKER_STYLE.CIRCLE
        ser.marker.size = 7
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = colr
        ser.marker.format.line.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        ser.smooth = False
    ch.has_title = True
    ch.chart_title.text_frame.text = "Outermost zone's excess over the interior, points, by wafers of disk use"
    ch.chart_title.text_frame.paragraphs[0].font.size = Pt(12)
    rows = [["Unit", "Onset (wafers)", "Climb after it"]]
    for u in lo + hi:
        rows.append([u, n(dose["%s onset" % u]), "%.1f" % dose["%s slope" % u]])
    _table(s, Inches(8.3), Inches(1.6), Inches(4.4), rows, [Inches(1.2), Inches(1.5), Inches(1.7)], size=12)
    _text(s, Inches(8.3), Inches(3.4), Inches(4.4), Inches(3.3), [
        "Climb: points of the outermost zone's fail rate per 1,000 wafers of disk use past the onset, at a pad half through "
        "its life (the pad adds %s per cent of the disk's effect at the end of its 600 wafers on %s and %s, %s on %s and %s)." % (
            "%.0f" % (100 * G["gamma"]["low"]), lo[0], lo[1], "%.0f" % (100 * G["gamma"]["high"]), hi[0], hi[1]),
        "Each pair is fitted together: the two units in a pair run one downforce recipe and their own fits differ by less than "
        "their disks do. Usage counts from the disk's own last change in the PM log, not from the last full PM.",
    ], size=12)
    _source(s, "Every polished wafer 5 January to 16 August, in bins of 200 wafers of disk use with 60 wafers or more.")

    # 5. the rules
    s = pr.slides.add_slide(layout)
    _title_of(s, "A fifth of the loss would have come under the old rule; Rev F and the waiver made the rest")
    cd = CategoryChartData()
    cats = ["The 2,000-wafer rule's own exposure", "Rev F's move to 2,800 wafers", "The EW-118 retained disks"]
    vals = [S["R5_bridge"]["old_rule"], S["R5_bridge"]["rev_f"], S["R5_bridge"]["ew118"]]
    cd.categories = cats
    cd.add_series("Share of the April to August loss", vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.6), Inches(1.6), Inches(7.4), Inches(4.2), cd)
    ch = gf.chart
    ch.has_legend = False
    _axes(ch)
    ch.category_axis.reverse_order = True
    ch.value_axis.maximum_scale = 0.6
    ch.value_axis.minimum_scale = 0.0
    ch.value_axis.tick_labels.number_format = "0%"
    ch.value_axis.tick_labels.number_format_is_linked = False
    plot = ch.plots[0]
    plot.gap_width = 70
    plot.series[0].format.fill.solid()
    plot.series[0].format.fill.fore_color.rgb = BLUE
    plot.has_data_labels = True
    plot.data_labels.number_format = "0%"
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.font.size = Pt(12)
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    _text(s, Inches(8.3), Inches(1.6), Inches(4.4), Inches(5.0), [
        "Each rule is run on each unit's own polish sequence from its state on 5 January: full PMs every 2,000 wafers, then "
        "Rev F's 2,800 from 2 April, then the four PMs that kept their disk under EW-118, with the unscheduled swaps where they "
        "happened and pads every 600 wafers.",
        "The ring each sequence gives is read off the pair's fitted curve, so the three shares add to the loss.",
        "Splitting the observed loss by the disk's use at 2,000 and 2,800 wafers instead gives %s, %s and %s: it misses that "
        "the old rule's disks would have been at other points in their lives on the same wafers." % (
            pct(F["routes"]["R5_slice"]["old_rule"]), pct(F["routes"]["R5_slice"]["rev_f"]), pct(F["routes"]["R5_slice"]["ew118"])),
    ], size=12)
    _source(s, "Shares of the ring's loss on wafers sorted 1 April to 31 August 2026.")

    # 6. the count
    s = pr.slides.add_slide(layout)
    _title_of(s, "Rev G: the disk on its own count saves about %s a year against Rev F" % usd(S["R7_saving"]))
    rows = [["Unit", "Count (wafers)", "Rev F, USD per wafer", "Rev G, USD per wafer", "Saving a year"]]
    for u in lo + hi:
        cpw = F["cost_per_wafer"][A.pair_of[u]]
        rows.append([u, n(c[u]), "%.2f" % cpw["Rev F as it stands"], "%.2f" % cpw["Rev G at the pair's count"], usd(G["R7_unit"][u])])
    rows.append(["Four units", "", "", "", usd(S["R7_saving"])])
    _table(s, Inches(0.6), Inches(1.6), Inches(12.1), rows, [Inches(1.6), Inches(2.2), Inches(2.9), Inches(2.9), Inches(2.5)], size=13)
    pert = F["perturbations"]
    lo_rng = (min(v[lo[0]] for v in pert.values()), max(v[lo[0]] for v in pert.values()))
    hi_rng = (min(v[hi[0]] for v in pert.values()), max(v[hi[0]] for v in pert.values()))
    _text(s, Inches(0.6), Inches(4.0), Inches(12.1), Inches(2.8), [
        "Cost per wafer counts the maintenance (the full PM every 2,800 wafers, less the disk's price under Rev G, and each disk "
        "change at its all-in of %s) and the good die the ring takes at the summer's product mix." % usd(A.allin["disk_change"]),
        "The count is where a disk's yearly cost of changes and ring loss is lowest. It stays between %s and %s on %s and %s and "
        "between %s and %s on %s and %s with every slope 20 per cent either way, every onset 5 per cent, the die value or the "
        "disk change 10 per cent, or the pad's term doubled or removed." % (n(lo_rng[0]), n(lo_rng[1]), lo[0], lo[1], n(hi_rng[0]),
                                                                             n(hi_rng[1]), hi[0], hi[1]),
        "One count of %s for all four units costs %s a year more than the pair counts; going back to Rev E costs %s a year more "
        "than Rev G." % (n(F["routes"]["R6_fleet"][lo[0]]), usd(F["fleet_vs_g"]), usd(F["rev_e_vs_g"])),
    ], size=13)
    _source(s, "A year of %s wafers through ILD-CMP, split by each unit's share since 1 June; cost inputs of 28 August 2026." % n(F["wpy"]))

    # 7. notes
    s = pr.slides.add_slide(layout)
    _title_of(s, "How the figures were built")
    _text(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(5.3), [
        "Records: the sort database (latest record per wafer, aliases mapped to P-A, P-B and P-C), the MES chamber steps, the "
        "units' polish record and maintenance log. Each part's use is counted from its own last replacement in the log's parts "
        "text, blank counters placed on the unit's polish record by time and back-entered rows by their counter.",
        "Loss: each wafer's outermost-zone fails less its tested die times its interior fail rate plus the zone's fallout on "
        "disks short of their onset; averaged over wafers as points of sort yield and summed by product as good die.",
        "Dose: weighted least squares of the outermost zone's excess over the interior on a hinge in the disk's use, with the "
        "pad's life multiplying the slope, the onset profiled, one fit per downforce pair.",
        "Causes: the same model with each disk life's own slope, the retaining ring's use, DEP-3, SC-4 and the chambers' RF "
        "hours beside it; each share is that term's loss over the window; the ring-only swaps checked as before-and-after steps.",
        "Rules: Rev E, Rev F and the actual history run on each unit's own polish sequence; shares in that order.",
        "Count and saving: the count minimises the disk's cost per wafer on the pair's curve; the saving is against Rev F's own "
        "2,800-wafer cycle with the waiver ended.",
    ], size=13, space=10)
    pr.save(path)
    PP.normalize_pptx(path, AUTHOR, AUTHOR, STAMPS[DECK][0], STAMPS[DECK][1], "Fab 2 edge ring: cause, cost and the Rev G disk count",
                      P.FIRM)


def write_all(F, gold):
    os.makedirs(gold, exist_ok=True)
    write_deck(os.path.join(gold, DECK), F)
