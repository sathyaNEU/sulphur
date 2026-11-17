"""The two golden files: the workbook the head of the Service opens (the classing on its first sheet, the working
behind it) and the same three things for every crossing as the CSV the asset register loads. Every number comes from
figures.json."""
import csv
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

FILES = {"wb": "crossing_classes_2027.xlsx", "csv": "crossing_classes_2027.csv"}
FILL = {3: "F3D3CF", 2: "FBEBC8", 1: "D7EAD3"}
PROTECTION = {3: "automatic barrier", 2: "seasonal patrol, hand gates", 1: "signs"}
HEAD = PatternFill("solid", fgColor="2B3F4E")
THIN = Side(style="thin", color="B8BEC8")
LOST = {"S1": "Each station scaled to its storage gauge by one factor",
        "S2": "Stations carried to the source areas by the yearly rainfall",
        "S3": "Hail days' tips read as rain",
        "S1+S2+S3": "All three together",
        "direct": "Tips as logged, no correction",
        "radar": "Radar depths at the source pixel, adjusted to the stations by one factor",
        "mapped": "Radar depths at the source pixel, matched to the Rio Scuro weighing gauges",
        "carried": "Weighing gauges over the Rio Scuro bucket, applied everywhere"}
RIVAL = {"bucket put back by one factor": LOST["S1"], "source scaled by the rainfall normal": LOST["S2"],
         "tips taken as rain on hail days": LOST["S3"], "the gauge read raw": "The station's tips as logged"}


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def order(f):
    """the crossings in road order, up the valley"""
    return sorted(f["storms"], key=lambda s: f["road_km"][s])


def _hdr(ws, row, n, height=44):
    for c in ws[row][:n]:
        c.font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=THIN)
    ws.row_dimensions[row].height = height


def _widths(ws, ws_):
    for col, w in zip("ABCDEFGHIJKLMNOP", ws_):
        ws.column_dimensions[col].width = w


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12, name="Calibri")
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, size=9, color="555555", name="Calibri")


def _note(ws, row, text, span, height=30):
    c = ws.cell(row=row, column=1, value=text)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=9, color="444444", name="Calibri")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    ws.row_dimensions[row].height = height


def headline(f):
    b = f["by_class"]
    return "barrier at %s; patrol with hand gates at %s; signs at %s" % (_list(b["3"]), _list(b["2"]), _list(b["1"]))


def first_sheet(wb, f, names):
    ws = wb.active
    ws.title = "Classing 2027-2031"
    n, c = f["counts"], f["route_class_counts"]["S1+S2+S3"]
    _title(ws, "SP 141 gully crossings, 2027 to 2031: automatic " + headline(f),
           "Regulation rev. 4, sections 3.1, 3.2 and 4.1. Tip records of %d to %d, %d warm seasons. L. Comboni, 13 November 2026."
           % (n["first_year"], n["last_year"], n["seasons"]))
    r = f["routes"]["S1+S2+S3"]
    low = [s for s in names if r[s]["class"] != f["classes"][s]]
    ws["A3"] = ("This is not the classing the tip records give when each station is scaled to its storage gauge by one "
                "factor, carried to the source areas by the yearly rainfall and read as rain on hail days: that leaves %s "
                "barriers, with %s. The Routes sheet sets each of those three choices beside the estimate." % (
                    {2: "two", 1: "one", 3: "three"}.get(int(c["3"]), c["3"]),
                    _list("%s at %.2f" % (s, r[s]["storms"]) for s in low)))
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:K3")
    ws.row_dimensions[3].height = 44
    hdr = ["Crossing", "Gully", "Road km", "Governing station", "Triggering depth (mm in 60 min)",
           "Triggering storms a season to expect", "Class", "Protection",
           "60-minute depth the source area reaches %d times a season (mm)" % f["regulation"]["times_a_season"],
           "Class 2 from", "Class 3 from"]
    ws.append([])
    ws.append(hdr)
    _hdr(ws, 5, len(hdr), 58)
    for i, s in enumerate(names):
        k = f["classes"][s]
        ws.append([f["crossing_id"][s], s, f["road_km"][s], f["station"][s], f["trigger"][s], f["storms"][s], k,
                   PROTECTION[k], f["depth"][s], f["regulation"]["lines"][0], f["regulation"]["lines"][1]])
        row = 6 + i
        ws.cell(row=row, column=7).fill = PatternFill("solid", fgColor=FILL[k])
        ws.cell(row=row, column=7).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=6).number_format = "0.00"
        for col in (3, 5, 9, 10, 11):
            ws.cell(row=row, column=col).number_format = "0.0"
    last = 5 + len(names)
    notes = ["Class 3 at 3.0 triggering storms a season or more, class 2 at 1.0 or more and under 3.0, class 1 under 1.0 "
             "(regulation 4.1). A storm counts once (2.3); storms are separated by six hours without rain at the station (2.2).",
             "Triggering storms a season are the mean over the %d warm seasons of each governing station's tip record (3.1), "
             "counted on the rain put at the source area: tips with the bucket's loss by rate put back, hail and graupel "
             "storms placed on the detector's minutes, and each source area's burst factor against its station." % n["seasons"],
             "Storms to two decimals, depths to 0.1 mm. The working sheets carry the same figures; the estimate was checked "
             "against the weighing gauges of the Rio Scuro valley (sheet Rio Scuro check)."]
    for i, t in enumerate(notes):
        _note(ws, last + 2 + i, t, 11, 26)
    _widths(ws, (11, 12, 8, 13, 12, 13, 7, 24, 16, 8, 8))
    ws.freeze_panes = "C6"
    bar = BarChart()
    bar.type = "col"
    b = f["by_class"]
    bar.title = "%s clear %.1f storms a season; %s sits under %.1f" % (
        _list(s.replace("Rio ", "") for s in sorted(b["3"], key=lambda s: f["road_km"][s])), f["regulation"]["lines"][1],
        _list(s.replace("Rio ", "") for s in b["1"]), f["regulation"]["lines"][0])
    bar.y_axis.title = "Triggering storms a season to expect"
    bar.add_data(Reference(ws, min_col=6, min_row=5, max_row=last), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=2, min_row=6, max_row=last))
    bar.y_axis.scaling.min = 0
    bar.y_axis.number_format = "0"
    bar.y_axis.delete = False
    bar.x_axis.delete = False
    bar.series[0].graphicalProperties.solidFill = "3B6E8F"
    line = LineChart()
    line.add_data(Reference(ws, min_col=10, max_col=11, min_row=5, max_row=last), titles_from_data=True)
    line.series[0].graphicalProperties.line.solidFill = "52514E"
    line.series[1].graphicalProperties.line.solidFill = "52514E"
    line.series[0].graphicalProperties.line.dashStyle = "dash"
    for s in line.series:
        s.graphicalProperties.line.width = 19050
        s.marker.symbol = "none"
        s.smooth = False
    bar += line
    bar.height, bar.width = 8.4, 19.0
    bar.legend.position = "b"
    ws.add_chart(bar, "A%d" % (last + 6))
    ws.print_area = "A1:K%d" % (last + 24)


def stations_sheet(wb, f):
    ws = wb.create_sheet("Stations")
    st = f["stations"]
    n = f["counts"]
    rates = f["stated"]["rates"]
    _title(ws, "What each tipping bucket fails to record, from the storage gauge account",
           "Tips against the storage gauge between an emptying and the next read, %s visit intervals over the six stations."
           % format(n["intervals"], ","))
    ws.append([])
    hdr = ["Station", "Tipping bucket", "Bucket (mm)", "Storms in the tip record", "Storage gauge total (mm)", "Tipped total (mm)",
           "Storage over tipped", "Account left over with that one factor (mm rms)", "Account left over with the loss by rate (mm rms)",
           "Time lost a tip (hours per mm)"] + ["Under-read at %d mm/h" % r for r in rates]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 62)
    for i, (name, d) in enumerate(st.items()):
        ws.append([name, d["gauge"], d["bucket_mm"], d["storms"], d["storage_mm"], d["tipped_mm"], d["account_factor"],
                   d["resid_factor"], d["resid_rate"], d["loss_h_per_mm"]] + [d["under_read"][str(r)] / 100.0 for r in rates])
        row = 5 + i
        ws.cell(row=row, column=3).number_format = "0.0"
        for col in (4,):
            ws.cell(row=row, column=col).number_format = "#,##0"
        for col in (5, 6):
            ws.cell(row=row, column=col).number_format = "#,##0.0"
        ws.cell(row=row, column=7).number_format = "0.000"
        for col in (8, 9):
            ws.cell(row=row, column=col).number_format = "0.00"
        ws.cell(row=row, column=10).number_format = "0.00000"
        for col in range(11, 11 + len(rates)):
            ws.cell(row=row, column=col).number_format = "0.0%"
    r0 = 5 + len(st) + 1
    a = f["account_residual"]
    sm = a["small_bucket"]
    lines = [
        "One factor closes each station's totals and leaves the intervals with the hardest rain short: the left-over runs "
        "with the interval's rain rate (correlation %s). The loss is fitted as time lost a tip, one value a bucket model, on "
        "the minute-by-minute tip rates; a recorded rate r (mm/h) stands for r / (1 - k r)." % _list(
            "%.2f" % d["resid_r"] for d in st.values()),
        "Read tip by tip or on totals of one to five minutes, the loss leaves the account of the %s mm buckets open by "
        "%.2f to %.2f mm (rms; %.2f as used). Written first-order in the rate on the same minute totals it leaves %.2f to "
        "%.2f times as much (the bands carry it), as a power law %.2f to %.2f times and read on 10- or 15-minute totals "
        "%.2f to %.2f times (not used). All of them give the same seven classes." % (sm, a["kept"][sm][0], a["kept"][sm][1], a["golden"][sm], a["ratio"]["first-order form"][0],
                                    a["ratio"]["first-order form"][1], a["ratio"]["power law"][0], a["ratio"]["power law"][1],
                                    min(a["ratio"]["10-minute totals"][0], a["ratio"]["15-minute totals"][0]),
                                    max(a["ratio"]["10-minute totals"][1], a["ratio"]["15-minute totals"][1])),
        "Tip rows are counted once where a logger re-sent a block (%s rows) and the technicians' tip tests at visits are "
        "left out (%s tips)." % (format(sum(d["resent"] for d in st.values()), ","), format(sum(d["tests"] for d in st.values()), ","))]
    for i, t in enumerate(lines):
        _note(ws, r0 + i, t, 15, 30)
    _widths(ws, (12, 22, 8, 10, 12, 12, 9, 14, 14, 11, 10, 10, 10, 10, 10))
    ws.freeze_panes = "B5"


def sources_sheet(wb, f, names):
    ws = wb.create_sheet("Source areas")
    so = f["sources"]
    _title(ws, "Each source area's bursts against its governing station, from the radar cells",
           "Cells with 1 mm or more in both pixels, %d to %d; the burst factor is the mean ratio of the source pixel to the "
           "station's pixel, on logs." % tuple(f["counts"]["radar_years"]))
    ws.append([])
    hdr = ["Source area of", "Governing station", "Cells in both pixels", "Burst factor", "Yearly rainfall, source over station",
           "Burst factor by the median ratio", "By the ratio of sums", "Trimmed", "Cells of 3 mm or more in both",
           "Odd years against even years"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 58)
    rows = list(names) + [g for g in so if g not in names]
    for i, s in enumerate(rows):
        d = so[s]
        w = d["ways"]
        ws.append([s, d["station"], d["pairs"], d["burst_factor"], d["normal_ratio"], w["median"], w["sums"], w["trim"], w["geo3"],
                   d["geo_halves_pct"] / 100.0])
        row = 5 + i
        ws.cell(row=row, column=3).number_format = "#,##0"
        for col in (4, 5, 6, 7, 8, 9):
            ws.cell(row=row, column=col).number_format = "0.000"
        ws.cell(row=row, column=10).number_format = "0.0%"
    r0 = 5 + len(rows) + 1
    _note(ws, r0, "RS-W1 to RS-W4 are the university programme's weighing gauges above the Rio Scuro station, shown for the check. "
                  "The radar's own depths run low against the gauges (gauge-adjusted by a factor of %.2f), so they are used "
                  "only as ratios between pixels of the same cell." % f["radar_bias"], 10, 30)
    _widths(ws, (13, 13, 10, 9, 13, 12, 10, 9, 12, 11))
    ws.freeze_panes = "B5"


def hail_sheet(wb, f):
    ws = wb.create_sheet("Hail storms")
    st = f["stations"]
    _title(ws, "Hail and graupel storms: where the tips put the water against when the detector saw it fall",
           "Storms with a hail or graupel code in any ten-minute block; warm seasons %d to %d." % (
               f["counts"]["first_year"], f["counts"]["last_year"]))
    ws.append([])
    hdr = ["Station", "Hail and graupel storms", "Their tipped water in blocks with no precipitation at the detector",
           "The same for rain storms", "Share of their 60-minute maximum the tips miss"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 58)
    for i, (name, d) in enumerate(st.items()):
        ws.append([name, d["hail_storms"], d["late_hail_pct"] / 100.0, d["late_rain_pct"] / 100.0, d["hail_gap_pct"] / 100.0])
        row = 5 + i
        ws.cell(row=row, column=2).number_format = "#,##0"
        ws.cell(row=row, column=3).number_format = "0.0%"
        ws.cell(row=row, column=4).number_format = "0.00%"
        ws.cell(row=row, column=5).number_format = "0.0%"
    r0 = 5 + len(st) + 1
    _note(ws, r0, "On these storms each storm's tipped water (loss put back) is kept and placed on the ten-minute blocks in "
                  "which the detector saw precipitation, in proportion to the detector's intensity; the largest 60 "
                  "consecutive minutes are read from that. The detector's own amounts are not used: on rain storms they "
                  "scatter about the tips by a factor of %.2f (one standard deviation, on logs)." % (
                      2.718281828 ** max(d["optical_log_sd"] for d in st.values())), 5, 44)
    _widths(ws, (13, 12, 22, 14, 18))
    ws.freeze_panes = "B5"


def check_sheet(wb, f):
    ws = wb.create_sheet("Rio Scuro check")
    r = f["referee"]
    t = f["regulation"]["times_a_season"]
    _title(ws, "The estimate against the weighing gauges of the Rio Scuro valley, %d to %d" % tuple(f["counts"]["weigh_years"]),
           "Four source areas above the Rio Scuro station, %d warm seasons; none of the seven crossings is in this valley." % r["seasons"])
    ws.append([])
    hdr = ["", "Mean 60-minute depth of a gauge's %d largest storms (mm)" % r["rank"],
           "60-minute depth a gauge reaches %d times a season (mm)" % t, "Storms reaching the gauges' triggering depths"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 58)
    rows = [("Weighing gauges", r["seen"]), ("The estimate, made the same way as for the crossings", r["golden"])]
    rows += [(RIVAL[k], v) for k, v in r["rivals"].items()]
    for i, (name, v) in enumerate(rows):
        ws.append([name, v["top"], v["depth"], v["storms"]])
        row = 5 + i
        for col in (2, 3):
            ws.cell(row=row, column=col).number_format = "0.00"
        ws.cell(row=row, column=4).number_format = "#,##0"
        if i < 2:
            for col in (1, 2, 3, 4):
                ws.cell(row=row, column=col).font = Font(bold=True, name="Calibri")
    _widths(ws, (52, 20, 18, 18))
    ws.freeze_panes = "B5"


def routes_sheet(wb, f, names):
    ws = wb.create_sheet("Routes")
    _title(ws, "Triggering storms a season under each simpler choice, beside the estimate",
           "One choice changed at a time, then all three, then the other records read on their own; the class each would file.")
    ws.append([])
    keys = ["golden", "S1", "S2", "S3", "S1+S2+S3", "direct", "radar", "mapped", "carried"]
    hdr = ["Crossing", "Estimate"] + [LOST[k] for k in keys[1:]] + ["Class: estimate"] + ["Class: " + LOST[k][0].lower() + LOST[k][1:]
                                                                                         for k in keys[1:]]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 74)
    for i, s in enumerate(names):
        ws.append([s] + [f["routes"][k][s]["storms"] for k in keys] + [f["routes"][k][s]["class"] for k in keys])
        for col in range(2, 2 + len(keys)):
            ws.cell(row=5 + i, column=col).number_format = "0.00"
        for j, k in enumerate(keys):
            cell = ws.cell(row=5 + i, column=2 + len(keys) + j)
            cell.fill = PatternFill("solid", fgColor=FILL[f["routes"][k][s]["class"]])
            cell.alignment = Alignment(horizontal="center")
    r0 = 5 + len(names) + 1
    p = f["perturbations"]
    _note(ws, r0, "Moved by a fifth either way, the fitted loss, the burst factors' distance from one and the hail storms' "
                  "put-back each leave all seven classes where they are; the nearest any crossing comes to a line is %.2f "
                  "storms a season." % min(x["nearest"] for x in p), 19, 30)
    mp = f["mapped_route"]["station"]
    away = [d["pct"] for k, d in mp.items() if k != "Rio Scuro"]
    _note(ws, r0 + 2, "The radar's depths matched to the Rio Scuro weighing gauges and set on each station's own pixel file %d "
                      "to %d per cent of the %d mm storms the station's own depths hold in the same cells at the five "
                      "stations outside that valley (%d of %d at Rio Scuro)." % (
                          min(away), max(away), f["mapped_route"]["at_mm"], mp["Rio Scuro"]["route"], mp["Rio Scuro"]["station"]), 19, 30)
    _widths(ws, (12, 9, 13, 13, 11, 10, 10, 12, 13, 13, 9, 13, 13, 11, 10, 10, 12, 13, 13))
    ws.freeze_panes = "B5"


def build(folder, f):
    os.makedirs(folder, exist_ok=True)
    names = order(f)
    wb = Workbook()
    first_sheet(wb, f, names)
    stations_sheet(wb, f)
    sources_sheet(wb, f, names)
    hail_sheet(wb, f)
    check_sheet(wb, f)
    routes_sheet(wb, f, names)
    wb.save(os.path.join(folder, FILES["wb"]))
    with open(os.path.join(folder, FILES["csv"]), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["crossing", "gully", "class", "triggering_storms_per_season",
                    "depth_60min_%d_per_season_mm" % f["regulation"]["times_a_season"]])
        for s in names:
            w.writerow([f["crossing_id"][s], s, f["classes"][s], "%.2f" % f["storms"][s], "%.1f" % f["depth"][s]])
    return names
