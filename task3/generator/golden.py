"""task3 goldens: the county's hydrology report for the state's structures review (a Word document exported to PDF the
way the department files it) and the creek's estimated annual peaks."""
import datetime as dt
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle  # noqa: E402
from scipy import stats  # noqa: E402

import officepdf as O  # noqa: E402

PST = dt.timezone(dt.timedelta(hours=-8))


def fmt(v):
    return "{:,}".format(int(v))


def chart(F, path):
    par, rpar = F["par"], F["river_par"]
    aep = np.array([0.5, 0.3, 0.2, 0.1, 0.05, 0.04, 0.02, 0.01, 0.005, 0.002])
    z = stats.norm.ppf(1 - aep)

    def curve(p):
        return 10 ** (p["mean"] + stats.pearson3.ppf(1 - aep, p["skew"]) * p["sd"])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5})
    fig, ax = plt.subplots(figsize=(6.3, 3.6), dpi=150)
    ax.plot(z, curve(par), color="#1f4e79", lw=2.0, label="Durrow Creek at Ransom Bar Rd (carried record)")
    ax.plot(z, curve(rpar), color="#7f7f7f", lw=1.3, ls="--", label="Coyner River near Tessel (gauged, 12183450)")
    for (sp, q), c in zip(sorted((int(k), v) for k, v in F["spans"].items()), ("#b0413e", "#3a7d44", "#6b4c9a")):
        ax.axhline(q, color=c, lw=0.9, ls=":")
        ax.text(z[0] + 0.02, q * 1.015, "%d ft span, rated %s cfs" % (sp, fmt(q)), color=c, fontsize=7.4)
    ax.set_xticks(stats.norm.ppf(1 - np.array([0.5, 0.2, 0.1, 0.04, 0.02, 0.01, 0.002])))
    ax.set_xticklabels(["50", "20", "10", "4", "2", "1", "0.2"])
    ax.set_xlabel("Annual exceedance probability (per cent)")
    ax.set_ylabel("Peak flow (cfs)")
    ax.set_ylim(0, 45000)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,.0f}".format(v)))
    ax.grid(True, color="#dddddd", lw=0.5)
    ax.legend(loc="upper left", fontsize=7.2, frameon=False, bbox_to_anchor=(0.0, 0.93))
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def _date(s):
    d = dt.date.fromisoformat(s)
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def report(F, path, scratch):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.5, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.6, leading=10.6)
    sp = sorted((int(k), v) for k, v in F["spans"].items())
    call = F["call_span_ft"]
    png = os.path.join(scratch, "frequency.png")
    chart(F, png)
    V = F["variants"]

    def grid(rows, widths):
        t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        return t
    flow_rows = [["Annual exceedance probability", "Durrow Creek at Ransom Bar Rd (cfs)", "Coyner River near Tessel (cfs)"],
                 ["50 per cent (2-year)", fmt(F["q50_5000"]), fmt(F["river_50pct"])],
                 ["1 per cent (100-year), the design flood", fmt(F["q01_5000"]), fmt(F["river_1pct"])]]
    span_rows = [["Span (ft)", "Rated flow, 2.0 ft freeboard (cfs)", "How often the rated flow would be exceeded",
                  "Carries the design flood"]]
    for s_, q in sp:
        span_rows.append([str(s_), fmt(q), F["bands"][str(s_)], "yes" if q >= F["golden_raw"]["0.01"] else "no"])
    flood_rows = [["Water year", "Storm (Coyner River peak)", "Coyner River peak (cfs)"]]
    for wy, d in zip(F["top2"], F["top2_dates"]):
        rq = next(p["river_cfs"] for p in F["peaks"] if p["water_year"] == wy)
        flood_rows.append([str(wy), _date(d), fmt(rq)])
    s = [Paragraph("Pelton County Department of Public Works, Engineering Division", small),
         Paragraph("Durrow Creek Bridge 2209-04, Ransom Bar Road: the %d ft span carries the design flood" % call, h1),
         Paragraph("Hydrology report for the WSDOT Local Programs structures review. Prepared by Amy Rasmussen, PE, Bridge "
                   "Engineer. 6 November 2026. Subject: design flood and span selection, Ransom Bar Road over Durrow Creek "
                   "(County Road 2209, milepost 4.31).", small),
         Spacer(1, 4),
         Paragraph("1. Recommendation", h2),
         Paragraph("Build the %d ft span. Durrow Creek's 1 per cent annual exceedance flood at the bridge is about %s cfs, "
                   "which the %d ft span carries within its rated %s cfs; the %d ft span, rated %s cfs, does not. The %d ft "
                   "span is not needed." % (call, fmt(F["q01_5000"]), call, fmt(F["spans"][str(call)]), sp[0][0],
                                            fmt(sp[0][1]), sp[2][0]), body),
         Paragraph("2. Basin and records", h2),
         Paragraph("Durrow Creek at the Ransom Bar Road crossing drains %.1f square miles of foothills between 610 and 4,380 "
                   "ft (mean %s ft). The creek has never been gauged. Under section 7.4.3(b) of the County standard the "
                   "record carried to the site is that of the nearest gauged basin with 25 years or more of annual peaks: "
                   "the Coyner River near Tessel (USGS 12183450), %.1f square miles, 6.2 miles away, with %d annual peaks "
                   "from water year 1951 to 2025 and its peaks above the 2,500 cfs base." % (
                       F["area_c"], fmt(F["mean_elev_c"]), F["area_r"], F["river_par"]["n"]), body),
         Paragraph("3. Carrying the Coyner River's record to the creek", h2),
         Paragraph("The two basins are the same size but not the same height. The Coyner River drains the flank of the "
                   "volcano up to 10,380 ft (mean %s ft); in a winter storm only its area below the snow line drains rain, "
                   "and above that line the storm's precipitation goes into the snowpack. Durrow Creek's basin lies below "
                   "the snow line in nearly every storm. Each Coyner River flood was therefore carried to the creek at the "
                   "ratio of the storm rain each basin took below that storm's snow line, not at the ratio of the drainage "
                   "areas." % fmt(F["mean_elev_r"]), body),
         Paragraph("For each of the %d floods in the river's annual and above-base peak files fed by rain, the storm is the "
                   "run of wet hours in the Tessel Field Airport record (the routine hourly reports) leading to the peak. Its "
                   "snow line was placed from the airport's temperature while the rain fell, weighted by the hour's rain, "
                   "with the lapse rate the Tessel and Durrow Ridge stations show on days both catch 0.5 in or more, %.1f "
                   "degrees C per kilometre (%s days; the Hatchet Meadow and Corbel Ridge pair gives %.1f), and the "
                   "temperature at which half the precipitation falls as rain at the two SNOTEL pillows, %.1f degrees C. "
                   "Precipitation rises about %d per cent per 1,000 ft (Durrow Ridge's totals run %.2f times Tessel's in the "
                   "storms warm enough for both to catch rain). In those floods the river drained rain over a median %d per "
                   "cent of its basin (%d per cent in its largest tenth) and the creek over %d per cent of its own. The "
                   "river's own peaks follow the rain over its area below the snow line (correlation %.2f in logarithms, %d "
                   "floods) much more closely than the storm's rain over the whole basin (%.2f)." % (
                       F["n_matched"], F["lapse"], fmt(F["n_lapse"]), F["lapse_snotel"], F["t50"], F["g_pct"], F["g_ratio"],
                       F["share_river_median_pct"], F["share_river_big_pct"], F["share_creek_median_pct"], F["own_r"],
                       F["own_n"], F["total_rain_r"]), body),
         Paragraph("The creek's flood in each water year is the largest of its carried floods. Water year %s holds no flood "
                   "fed by rain in the river's files, only a spring melt peak, and enters the fit as below the low-flood "
                   "threshold (%s cfs). Bulletin 17C was fitted by expected moments; the Multiple Grubbs-Beck test flags %d "
                   "low floods, and the station skew (%.2f) weighted with the Region 3 regional skew (%.2f) gives %.2f." % (
                       " and ".join(str(y) for y in F["missing_years"]), fmt(F["low_threshold"]), F["par"]["low"] - len(F["missing_years"]),
                       F["par"]["station_skew"], F["regional_skew"], F["par"]["skew"]), body),
         Paragraph("4. Flows at the bridge", h2),
         grid(flow_rows, [150, 130, 130]),
         Spacer(1, 4),
         Paragraph("Table 1. The creek's flows to the nearest 5,000 cfs, the precision the carried record supports; the "
                   "Coyner River's Bulletin 17C flows to the nearest 100 cfs.", small),
         Image(png, width=6.3 * 72 * 0.98, height=3.6 * 72 * 0.98),
         Paragraph("Figure 1. Frequency curves and the rated flows of the span alternatives (Hess Hydraulic Engineering, TM "
                   "26-118).", small),
         Paragraph("5. Span selection under section 7.4.2", h2),
         grid(span_rows, [55, 110, 150, 95]),
         Spacer(1, 4),
         Paragraph("6. Flood history at the crossing", h2),
         Paragraph("The creek's two largest floods since 1951 in the carried record came in water years %s and %s, each well "
                   "above the next largest. They are not the Coyner River's largest: the river's record peaks (water years "
                   "%s and %s) came in storms warm enough to rain over most of its basin, while these two storms left much "
                   "of the river's basin under snow and rained over all of the creek's. The estimated annual peaks are filed "
                   "with this report as durrow_creek_estimated_annual_peaks.csv." % (
                       F["top2"][0], F["top2"][1], F["river_top2"][0], F["river_top2"][1]), body),
         grid(flood_rows, [80, 160, 130]),
         Spacer(1, 4),
         Paragraph("7. Checks", h2),
         Paragraph("Carried by drainage area alone, the Coyner River's 1 per cent flood (%s cfs) gives the creek about %s cfs, "
                   "and that transfer reproduces the region's other gauged basins closely, because every one of them is a high "
                   "basin like the Coyner River's; on it the 140 ft span would have been selected. The state's Region 3 "
                   "equation is not used (section 7.4.3(c)). A snow line placed with the standard atmosphere's 6.5 degrees C "
                   "per kilometre sits too low in storms and gives about %s cfs; leaving out the rise of precipitation with "
                   "elevation gives about %s cfs; the valley's daily mean temperature in place of the hourly record mixes in "
                   "the air before and after the rain. The design flood holds at %s cfs for every storm definition and "
                   "temperature weighting the hourly record allows." % (
                       fmt(F["river_1pct"]), fmt(F["drainage_area"]), fmt(V["lapse_6.5"]["q01_5000"]),
                       fmt(V["no_orography"]["q01_5000"]), fmt(F["q01_5000"])), body)]
    O.build(path, s, "Durrow Creek Bridge 2209-04: hydrology report", "Pelton County Public Works", "Hydrology report",
            "Pelton County Public Works, bridge 2209-04 hydrology", dt.datetime(2026, 11, 5, 15, 12, tzinfo=PST),
            dt.datetime(2026, 11, 6, 9, 48, tzinfo=PST))


def csv(F, path):
    lines = ["water_year,estimated_peak_flow_cfs,qualifier,coyner_river_peak_date,coyner_river_peak_cfs"]
    for p in F["peaks"]:
        lines.append("%d,%d,%s,%s,%s" % (p["water_year"], p["cfs"], p["qualifier"], p["river_date"],
                                         "" if p["river_cfs"] is None else "%d" % p["river_cfs"]))
    open(path, "w", newline="\n").write("\n".join(lines) + "\n")


def write(F, gld, scratch):
    os.makedirs(gld, exist_ok=True)
    report(F, os.path.join(gld, "durrow_creek_bridge_hydrology_report.pdf"), scratch)
    csv(F, os.path.join(gld, "durrow_creek_estimated_annual_peaks.csv"))
