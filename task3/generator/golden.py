"""task3 goldens: the ranking workbook the capital program keeps and the memo to the Stormwater Advisory Board, every
figure from figures.json."""
import datetime as dt
import os
import tempfile

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

import analysis as A
import officepdf as O

XLSX = "fy2028_tide_valve_ranking.xlsx"
MEMO = "fy2028_tide_valve_memo.pdf"
EST = dt.timezone(dt.timedelta(hours=-5))
BASIS = {
    "front": "Street sensor over the lane (May 2024 to Oct 2026); harbor high waters",
    "marsh": "Sep-Nov 2024 logger campaign; transfer bending above the marsh",
    "river": "Jan-Apr 2025 logger campaign with the Brayle's daily flows",
    "wharf": "Inventory lane survey (2023); harbor high waters",
    "oyster": "Aug-Oct 2025 logger campaign; transfer bending above the marsh",
}


def harbor_equiv(F, k):
    if k == "front":
        return F["front_level_mllw"]
    if k == "wharf":
        return None
    if k == "marsh":
        return F["marsh_Hstar"]
    if k == "oyster":
        return F["oyster_Hstar"]
    return None


def workbook(F, inv_lane, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Ranking"
    ws.append(["FY2028 tide valve round: low points ranked on expected tidal flood days, 2027-28 tide year"])
    ws.append(["Expected days are averages over the weather and river flows of the tide years 1990-91 to 2025-26, on the "
               "harbor gauge's published predictions at the planning mean sea level (0.70 ft above the 1983-2001 mean)."])
    ws.append([])
    hdr = ["Rank", "Low point", "LP ID", "Flooding elevation (ft NAVD88)", "2025-26 tidal flood days",
           "Expected tidal flood days 2027-28", "90% range, low", "90% range, high", "Funded FY2028", "Basis"]
    ws.append(hdr)
    for i, k in enumerate(F["rank_keys"], start=1):
        lane = F["front_level_navd88"] if k == "front" else inv_lane[k]
        ws.append([i, A.NAMES[k], A.SITE_IDS[k], lane, F["hind"][k], F["exp"][k], F["exp_range"][k][0], F["exp_range"][k][1],
                   "Yes" if k in F["call_keys"] else "No (FY2029 round)", BASIS[k]])
    ws.append([])
    ws.append(["Front Street's flooding elevation is set from the street sensor (the lane was not surveyed); the inlet rim is "
               "lower, and the lane, not the rim, is where the program counts a flood day."])
    ws.append(["The funded pair is the top two in %d of the %d weather years; in the other %d River Road takes Front Street's place."
               % (F["pair_hold"], F["n_weather_years"], F["n_weather_years"] - F["pair_hold"])])
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws["A1"].font = Font(bold=True, size=12)
    for col, w in zip("ABCDEFGHIJ", (6, 30, 8, 14, 12, 14, 10, 10, 18, 56)):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=5, max_row=9):
        row[3].number_format = "0.00"
        row[5].number_format = "0.0"
    ws.freeze_panes = "A5"

    h = wb.create_sheet("Harbor gauge")
    h.append(["Port Tolliver harbor gauge (NOAA 8673718): days at the minor flood threshold, %.1f ft MLLW" % F["harbor_minor"]])
    h.append([])
    h.append(["Measure", "Days", "Note"])
    h.append(["2025-26 tide year, observed", F["harbor_2025"], "verified high waters"])
    h.append(["2027-28 tide year, expected", F["harbor_exp"], "planning mean sea level %.2f ft above the 1983-2001 mean" % F["plan"]])
    h.append(["2027-28, 90% range low", F["harbor_lo"], "nine weather years in ten"])
    h.append(["2027-28, 90% range high", F["harbor_hi"], ""])
    h.append([])
    h.append(["Change from 2025-26 to 2027-28", "Days", "Across the six orders of applying the changes"])
    for k, lab in (("sea", "Sea level (%.2f ft in 2025-26 to %.2f ft)" % (F["A25"], F["plan"])), ("tides", "Tides (2027-28 predictions for 2025-26's)"),
                   ("weather", "Weather (the 36 weather years for 2025-26's)")):
        h.append([lab, F["bridge"][k], "%.1f to %.1f" % tuple(F["bridge_range"][k])])
    h.append(["Total", F["bridge"]["total"], "%d to %.1f" % (F["harbor_2025"], F["harbor_exp"])])
    for r_ in (3, 9):
        for c in h[r_]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DDE4EE")
    h["A1"].font = Font(bold=True, size=12)
    for col, w in zip("ABC", (46, 10, 58)):
        h.column_dimensions[col].width = w
    for rr in h.iter_rows(min_row=4, max_row=h.max_row):
        if isinstance(rr[1].value, float):
            rr[1].number_format = "0.0"

    y = wb.create_sheet("Weather years")
    y.append(["Tidal flood days in 2027-28 under each weather year's surges and river flows"])
    y.append(["Weather year"] + [A.NAMES[k] for k in A.ORDER] + ["Harbor gauge (minor)", "Top two that year"])
    pyr = F["per_year"]
    for i, yr in enumerate(A.WX_YEARS):
        vals = {k: pyr[k][i] for k in A.ORDER}
        top = sorted(A.ORDER, key=lambda k: (-vals[k], A.ORDER.index(k)))[:2]
        y.append(["%d-%02d" % (yr, (yr + 1) % 100)] + [vals[k] for k in A.ORDER] + [pyr["harbor"][i],
                 " and ".join(A.NAMES[k].split(" at ")[0] for k in top)])
    y.append(["Average"] + [F["exp"][k] for k in A.ORDER] + [F["harbor_exp"], ""])
    for c in y[2]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    y["A1"].font = Font(bold=True, size=12)
    y.column_dimensions["A"].width = 12
    for col in "BCDEFG":
        y.column_dimensions[col].width = 14
    y.column_dimensions["H"].width = 30
    y.freeze_panes = "B3"

    v = wb.create_sheet("Variants")
    v.append(["The method under every defensible variant: expected tidal flood days 2027-28 and the funded pair"])
    v.append(["Weather-year alignment", "Residual sea level", "River Road flow form", "Marsh Road bend", "Front Street lane",
              "Front St", "Marsh Rd", "River Rd", "Wharf St", "Oyster Ck Rd", "Funded pair", "Years the pair leads"])
    form_names = {"lin": "linear", "pow": "power", "linq": "linear, curved in height", "sqrt": "square root", "log": "logarithmic"}
    for s_ in F["sweep"]:
        v.append([s_["align"], s_["detrend"], form_names.get(s_["river"], s_["river"]), s_["marsh"], s_["front"]]
                 + [s_["means"][k] for k in A.ORDER] + [" and ".join(p.split(" at ")[0] for p in s_["pair"]), s_["hold"]])
    for c in v[2]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    v["A1"].font = Font(bold=True, size=12)
    for col, w in zip("ABCDEFGHIJKL", (12, 12, 22, 16, 14, 9, 9, 9, 9, 10, 28, 10)):
        v.column_dimensions[col].width = w
    for rr in v.iter_rows(min_row=3, max_row=v.max_row):
        for c in rr[5:10]:
            c.number_format = "0.0"
    v.freeze_panes = "A3"

    r = wb.create_sheet("Routes")
    r.append(["The funded pair under the shortcuts the records rule out"])
    r.append(["Route", "Front St", "Marsh Rd", "River Rd", "Wharf St", "Oyster Ck Rd", "Funded pair", "Ruled out by"])
    why = {
        "golden": "",
        "marsh straight line": "the 2024 campaign's high waters above the marsh platform fall below the line",
        "river one offset": "the 2025 campaign's offset falls with the river's flow; late winter flows are not the year's",
        "both (careful but hurried)": "both of the above",
        "no transfer, drain rim (quick)": "each low point's own record; the program counts the lane, not the rim",
    }
    label = {"golden": "Recommended: each low point's own transfer",
             "marsh straight line": "Marsh Road and Oyster Creek Road on one straight line",
             "river one offset": "River Road on its campaign's single offset",
             "both (careful but hurried)": "Both of those",
             "no transfer, drain rim (quick)": "No transfer; Front Street at its drain rim"}
    for name, pair in F["routes"].items():
        e = dict(F["exp"])
        e.update(F["route_exp"].get(name, {}))
        if name == "both (careful but hurried)":
            e.update(F["route_exp"]["marsh straight line"])
            e.update(F["route_exp"]["river one offset"])
        r.append([label[name]] + [e[k] for k in A.ORDER] + [" and ".join(p.split(" at ")[0] for p in pair), why[name]])
    for c in r[2]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EE")
    r["A1"].font = Font(bold=True, size=12)
    for rr in r.iter_rows(min_row=3, max_row=r.max_row):
        for c in rr[1:6]:
            c.number_format = "0.0"
    for col, w in zip("ABCDEFGH", (44, 10, 10, 10, 10, 12, 30, 70)):
        r.column_dimensions[col].width = w
    wb.save(path)


def chart(F, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    keys = F["rank_keys"]
    lab = [A.NAMES[k].replace(" at ", "\nat ") for k in keys]
    fig, ax = plt.subplots(figsize=(6.4, 3.0), dpi=160)
    col = ["#1f5a96" if k in F["call_keys"] else "#a9b4c2" for k in keys]
    vals = [F["exp"][k] for k in keys]
    lo = [F["exp"][k] - F["exp_range"][k][0] for k in keys]
    hi = [F["exp_range"][k][1] - F["exp"][k] for k in keys]
    ax.bar(range(len(keys)), vals, color=col, width=0.62)
    ax.errorbar(range(len(keys)), vals, yerr=[lo, hi], fmt="none", ecolor="#333333", elinewidth=0.9, capsize=3)
    for i, (v, k) in enumerate(zip(vals, keys)):
        ax.text(i + 0.33, v, "%.1f" % v, ha="left", va="center", fontsize=7.5, color="#222222")
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(lab, fontsize=7)
    ax.set_ylabel("Tidal flood days, 2027-28", fontsize=8)
    ax.tick_params(axis="y", labelsize=7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Wharf Street and Front Street lead; River Road's wet years reach past them", fontsize=8.5, loc="left")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def memo(F, inv_lane, path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceAfter=4)
    small = ParagraphStyle("s", parent=body, fontSize=8.0, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.4, leading=10.2)
    n = A.NAMES
    w1, w2 = F["call_keys"]
    others = [k for k in F["rank_keys"] if k not in F["call_keys"]]
    rows = [["Low point", "Flooding elevation (ft NAVD88)", "2025-26 days", "Expected 2027-28", "90% range"]]
    for k in F["rank_keys"]:
        lane = F["front_level_navd88"] if k == "front" else inv_lane[k]
        rows.append([n[k], "%.2f" % lane, "%d" % F["hind"][k], "%.1f" % F["exp"][k], "%d to %d" % tuple(F["exp_range"][k])])
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[150, 92, 62, 72, 62])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    png = os.path.join(tempfile.mkdtemp(prefix="t3chart-"), "chart.png")
    chart(F, png)
    img = Image(png, width=440, height=206)
    b = F["bridge"]
    s = [Paragraph("Port Tolliver Stormwater Utility, Capital Program", small),
         Paragraph("FY2028 tide valves: Wharf Street at Market Lane and Front Street at Ferry Lane", h1),
         Paragraph("To: Stormwater Advisory Board. From: Cheryl Olsen, PE. 10 November 2026.", small),
         Spacer(1, 4),
         Paragraph("Fund the FY2028 valves at %s (%.1f expected tidal flood days in the 2027-28 tide year) and %s (%.1f). "
                   "%s (%.1f), %s (%.1f) and %s (%.1f) go to the FY2029 round. The same two come out on top in %d of the %d "
                   "weather years (in the others, wet late winters on the Brayle, River Road takes Front Street's place) and "
                   "under all %d variants of the method we could defend, by at least %.2f times."
                   % (n[w1], F["exp"][w1], n[w2], F["exp"][w2], n[others[0]], F["exp"][others[0]], n[others[1]], F["exp"][others[1]],
                      n[others[2]], F["exp"][others[2]], F["pair_hold"], F["n_weather_years"], F["sweep_n"],
                      F["sweep_margin"]), body),
         t, Spacer(1, 6), img, Spacer(1, 4),
         Paragraph("<b>Harbor gauge.</b> At its %.1f ft minor flood threshold the gauge expects %.1f days in 2027-28 (%d to %d in "
                   "nine weather years in ten) against %d observed in 2025-26. The planning sea level, %.2f ft above the "
                   "1983-2001 mean against %.2f ft in 2025-26, adds %.1f days; the 2027-28 tides take %.1f and the weather years "
                   "against 2025-26's add %.1f, a change of %.1f (each share averaged over the six orders of applying the "
                   "three changes; sea level adds %.1f to %.1f across them)."
                   % (F["harbor_minor"], F["harbor_exp"], F["harbor_lo"], F["harbor_hi"], F["harbor_2025"], F["plan"], F["A25"],
                      b["sea"], -b["tides"], b["weather"], b["total"], F["bridge_range"]["sea"][0], F["bridge_range"]["sea"][1]), body),
         Paragraph("<b>Front Street.</b> The lane sits at %.2f ft NAVD88, the lowest water level the street sensor records on "
                   "it in readings that persist; the inlet rim is lower but the program counts the lane. The sensor itself "
                   "recorded %d of the %d tidal flood days of 2025-26; the other %d fell in its September-October outage and "
                   "come from the harbor's high waters." % (F["front_level_navd88"], F["front_sensor_days"],
                                                            F["hind"]["front"], F["front_outage_days"]), body),
         Paragraph("<b>Marsh Road and Oyster Creek Road.</b> Pellam Creek's high water follows the harbor's at %.2f ft per foot "
                   "until the tide tops the marsh (harbor about %.2f ft) and at %.2f above it, so Marsh Road floods at a harbor "
                   "high water of %.2f ft, not the %.2f ft one straight line through the 2024 campaign gives (%d of its %d "
                   "high waters stood above the bend). Oyster Creek bends the same way and floods only at %.2f ft."
                   % (F["marsh_slopes"][0], F["marsh_P"], F["marsh_slopes"][1], F["marsh_Hstar"], F["marsh_Hlin"], F["marsh_above"],
                      F["marsh_n"], F["oyster_Hstar"]), body),
         Paragraph("<b>River Road.</b> The only campaign ran from January to April 2025 with the Brayle at %s to %s cfs "
                   "(%s on average); Hensley's high waters stand about %.2f ft higher at 25,000 cfs than at 5,000. Carried day "
                   "by day on the river's flows, River Road flooded on %d days in 2025-26; the campaign's average offset carried "
                   "to the dry autumn king tides would have given %d."
                   % ("{:,}".format(F["river_q"][0]), "{:,}".format(F["river_q"][1]), "{:,}".format(F["river_q"][2]),
                      F["river_setup_25k"], F["hind"]["river"], F["variants_hind"]["river_pooled"]), body),
         Spacer(1, 4),
         Paragraph("Expected days are averages over the weather and river flows of the tide years 1990-91 to 2025-26, on the "
                   "gauge's published predictions at the planning sea level (round guidelines, 16 October 2026).", small)]
    O.build(path, s, "FY2028 tide valves", "Port Tolliver Stormwater Utility", "FY2028 tide valve round recommendation",
            "Port Tolliver Stormwater Utility, Capital Program", dt.datetime(2026, 11, 10, 8, 52, 14, tzinfo=EST),
            dt.datetime(2026, 11, 10, 8, 52, 14, tzinfo=EST))
