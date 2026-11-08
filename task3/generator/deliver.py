"""task3's golden deliverables from one figure set: kinnard_road_culvert_design_flow.docx (the Roads Division's design
flow memorandum for the state floodplain review: the culvert, the design flow, how it was estimated from the records,
the frequency chart, the floods on today's watershed) and ollery_creek_design_peak_table.csv (the table of
annual peak flows the estimate rests on, as the reviewer re-runs it)."""
import csv
import io
from decimal import Decimal, ROUND_HALF_UP

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402
from docx import Document               # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH   # noqa: E402
from docx.shared import Cm, Pt, RGBColor        # noqa: E402

import common as K   # noqa: E402
import freq as FQ    # noqa: E402

matplotlib.rcParams["svg.hashsalt"] = "task3"
matplotlib.rcParams["font.family"] = "DejaVu Sans"


def whole(x):
    return int(Decimal(repr(float(x))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def nearest(x, step):
    return whole(float(x) / step) * step


def comma(x):
    return "{:,}".format(int(x))


def names(lst):
    return ", ".join(lst[:-1]) + " and " + lst[-1] if len(lst) > 1 else lst[0]


def figures(R, band, rungs):
    pick = R["pick"]
    F = {"pick": pick[0], "pick_barrels": pick[1], "pick_capacity": comma(pick[2]), "pick_cost": comma(pick[3]),
         "capacity": {a: comma(cap) for a, d, cap, cost in K.CULVERTS},
         "design_flow": comma(nearest(R["q1"], 10)),
         "band_low": comma(nearest(band[0], 10)), "band_high": comma(nearest(band[1], 10)),
         "raw_q1": comma(nearest(R["raw_q1"], 10)), "raw_pick": R["raw_pick"][0],
         "rungs_high": comma(nearest(rungs, 10)),
         "mk_p": "%.2f" % R["mk_p"], "mk_tau": "%.2f" % R["mk_tau"], "area_sqmi": "%.1f" % K.AREA_SQMI,
         "c": "%.2f" % R["c"], "n_pairs": R["n_pairs"],
         "factor": "%.1f" % R["factor_1960"], "imp_1956": "%d" % whole(100 * R["imp_1956"]),
         "imp_2025": "%d" % whole(100 * R["imp_2025"]),
         "largest_year": R["top5"][0], "top4": R["top5"][:4], "raw_largest_year": R["raw_top5"][0],
         "raw_top4": R["raw_top5"][:4], "years": "%d to %d" % (K.YEAR0, K.YEAR1), "n_years": K.YEAR1 - K.YEAR0 + 1,
         "recorded_largest": comma(nearest(max(R["ann"]), 10)),
         "largest_recorded": comma(nearest(R["ann"][list(R["years"]).index(R["top5"][0])], 10)),
         "largest_today": comma(nearest(R["adj"][list(R["years"]).index(R["top5"][0])], 10))}
    return F


def chart_png(R, F):
    fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=150)
    aeps = np.array([0.5, 0.2, 0.1, 0.04, 0.02, 0.01, 0.005])
    ret = 1 / aeps
    q_raw = [FQ.lp3_quantile(R["ann"], p) for p in aeps]
    q_adj = [FQ.lp3_quantile(R["adj"], p) for p in aeps]
    ax.plot(ret, q_raw, color="#7f8c8d", lw=1.8, label="recorded peaks, 1956 to 2025")
    ax.plot(ret, q_adj, color="#1f4e79", lw=2.4, label="the same storms on today's watershed")
    n = len(R["ann"])
    for arr, col in ((np.sort(R["ann"])[::-1], "#7f8c8d"), (np.sort(R["adj"])[::-1], "#1f4e79")):
        rank = np.arange(1, n + 1)
        ax.scatter((n + 1) / rank, arr, s=10, color=col, alpha=0.7)
    for a, d, cap, cost in K.CULVERTS:
        ax.axhline(cap, color="#c0392b" if a == F["pick"] else "#b0b0b0", lw=1.0, ls="--")
        ax.text(1.05, cap * 1.015, "Alternative %s, %s cfs" % (a, comma(cap)), fontsize=7.5,
                color="#c0392b" if a == F["pick"] else "#606060")
    ax.axvline(100, color="#404040", lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_xlim(1, 220)
    ax.set_ylim(0, K.CULVERTS[-1][2] * 1.12)
    ax.set_xlabel("Return period (years); the dotted line is the 1 per cent flood", fontsize=8.5)
    ax.set_ylabel("Peak flow (cfs)", fontsize=8.5)
    ax.set_title("Ollery Creek at Kinnard Road: 1 per cent flood %s cfs on today's watershed" % F["design_flow"],
                 fontsize=9.5, loc="left")
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _p(doc, text, bold=False, size=10.5, italic=False, space=4):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold, run.italic = bold, italic
    run.font.size = Pt(size)
    para.paragraph_format.space_after = Pt(space)
    return para


def write_docx(path, R, F):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
        sec.top_margin = sec.bottom_margin = Cm(2.0)
    _p(doc, "Tamsett County Roads Division", bold=True, size=9)
    _p(doc, "To: State floodplain review    From: %s, hydraulics engineer    Date: 12 January 2026"
       % K.PEOPLE["engineer"], size=9, space=0)
    _p(doc, "Ref: RD-2026-07, Kinnard Road over Ollery Creek, design flow memorandum (Drainage Standard 4.6)", size=9,
       space=10)
    _p(doc, "Alternative %s carries Kinnard Road over the design flood" % F["pick"], bold=True, size=16, space=8)
    _p(doc, "The design flow at Kinnard Road is %s cfs, the peak with a 1 per cent chance of being equalled or "
            "exceeded in any year of the crossing's first ten years. Alternative %s (%s, capacity %s cfs, USD %s) is "
            "the least costly alternative that passes it; Alternative A (capacity %s cfs) would overtop."
       % (F["design_flow"], F["pick"], F["pick_barrels"], F["pick_capacity"], F["pick_cost"], F["capacity"]["A"]),
       bold=True, size=11, space=8)
    _p(doc, "The gauge's %d annual peaks (%s) show no trend (Kendall's tau %s, p = %s) and a log-Pearson III fit to "
            "them gives %s cfs. That figure describes the watershed the record came from, not the one the culvert will "
            "serve. Over the record the paved area grew from %s to %s per cent of the 11.5 square miles, with storm "
            "drains in every subdivision, while the storms of the last three decades ran lighter than those of the "
            "1960s to 80s; the two cancel in the annual peaks, so the record reads as if nothing had changed."
       % (F["n_years"], F["years"], F["mk_tau"], F["mk_p"], F["raw_q1"], F["imp_1956"], F["imp_2025"]), space=6)
    _p(doc, "Set against the storm that made it, each flood shows the change. Pairing the %d peaks above base made by "
            "storms of an inch or more with the rain gauge's totals for the storm (the peak day and the two days "
            "before), the log peak rises by %s per unit of paved fraction at a fixed storm: the same storm makes "
            "about %s times the peak on today's watershed that it made in 1960. Each year's peak was put on today's "
            "watershed by that rise and the series refitted; every sound pairing (windows of two to four days, "
            "storms of half an inch to three inches, the annual peaks against their own storms, decade effects; "
            "log-Pearson III or the generalized extreme value) gives %s to %s cfs."
       % (F["n_pairs"], F["c"], F["factor"], F["band_low"], F["band_high"]), space=8)
    doc.add_picture(io.BytesIO(chart_png(R, F)), width=Cm(16.0))
    _p(doc, "Dots are the 70 annual peaks by plotting position (Weibull); the dashed lines are the three alternatives' "
            "capacities.", italic=True, size=8.5, space=10)
    _p(doc, "Floods of the record on today's watershed", bold=True, size=12, space=4).paragraph_format.keep_with_next = True
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = "Table Grid"
    for i, h in enumerate(["Rank", "Water year", "Recorded peak (cfs)", "On today's watershed (cfs)"]):
        tbl.rows[0].cells[i].text = h
        tbl.rows[0].cells[i].paragraphs[0].runs[0].bold = True
    yrs = list(R["years"])
    for k, y in enumerate(R["top5"][:4], 1):
        i = yrs.index(y)
        row = tbl.add_row().cells
        for j, v in enumerate([str(k), str(y), comma(nearest(R["ann"][i], 10)), comma(nearest(R["adj"][i], 10))]):
            row[j].text = v
            if j:
                row[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _p(doc, "Source: ollery_creek_annual_peak_flows.csv, ollery_creek_peaks_above_base_1956-2025.csv, "
            "tamsett_rain_gauge_daily_1956-2025.csv and tamsett_stormwater_impervious_parcels.xlsx. The record's "
            "largest recorded flood, water year %d (%s cfs), falls out of the four largest on today's watershed; "
            "water year %d's, %s cfs as recorded, would run at about %s cfs." % (F["raw_largest_year"], F["recorded_largest"],
                                                               F["largest_year"], F["largest_recorded"],
                                                               F["largest_today"]), italic=True, size=8.5, space=8)
    _p(doc, "Records and conventions", bold=True, size=12, space=4).paragraph_format.keep_with_next = True
    _p(doc, "Rain: the gauge in service (TAM-RG-01 to its move in June 1987, then TAM-RG-02); weekend readings "
            "accumulated into Monday's through 1978 spread over the days they cover. Peaks: the 2009 and 2010 water "
            "years' duplicate export counted once. Paved fraction: the stormwater utility's Ollery basin parcels by the "
            "year their impervious area was built, a split parcel carried under both numbers counted once, over the "
            "basin's area. The 2027 to 2036 service years are taken on the 2025 watershed; the basin's parcels have "
            "added under a tenth of a percentage point a year since 2015.", size=9.5, space=6)
    _p(doc, "Flows are rounded to the nearest 10 cfs; the table of annual peaks is filed beside this memorandum as "
            "ollery_creek_design_peak_table.csv.",
       italic=True, size=8.5)
    footer = doc.sections[0].footer.paragraphs[0]
    footer.text = "RD-2026-07 design flow memorandum"
    footer.runs[0].font.size = Pt(8)
    cp = doc.core_properties
    import datetime as dt
    cp.author = K.PEOPLE["engineer"]
    cp.last_modified_by = K.PEOPLE["engineer"]
    cp.created = dt.datetime(2026, 1, 9, 10, 5)
    cp.modified = dt.datetime(2026, 1, 12, 16, 40)
    cp.title = "Kinnard Road culvert design flow"
    cp.comments = ""
    cp.revision = 4
    doc.save(path)


def write_csv(path, R):
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["water_year", "peak_date", "recorded_peak_cfs", "storm_rain_in", "paved_fraction_pct",
                     "peak_current_watershed_cfs"])
        for i, y in enumerate(R["years"]):
            wr.writerow([int(y), R["dates"][i], comma(nearest(R["ann"][i], 10)).replace(",", ""),
                         "%.2f" % R["storm"][i], "%.1f" % (100 * R["imp"][i]),
                         str(nearest(R["adj"][i], 10))])
