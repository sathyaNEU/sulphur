"""task3 architecture 3: the golden deliverables from the solution on the cut pack. The forecast workbook (the
demonstration table, the test fit, the Mill Street record and its separated drawdown, the calibration, the monthly
forecast for every schedule) and the WR-4 demonstration PDF with its chart."""
import datetime as dt
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill
from PIL import Image as PImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

import officepdf as O
import ooxml
import solve as S

EDT = dt.timezone(dt.timedelta(hours=-4))
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
COLS = {450: (95, 140, 190), 700: (60, 150, 110), 1000: (25, 70, 150), 1250: (200, 120, 40)}


def ft(x):
    return int(math.floor(x + 0.5))


def chart(res, path):
    W_, H_ = 2000, 1100
    img = PImage.new("RGB", (W_, H_), "white")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 30)
    fs = ImageFont.truetype(FONT, 26)
    fb = ImageFont.truetype(FONTB, 34)
    L, R, T, B = 150, 1960, 110, 940
    idx = [i for i, ym in enumerate(S.MONTHS) if (2027, 1) <= ym <= (2046, 12)]
    ymax = 12.0
    X = lambda k: L + (R - L) * k / (len(idx) - 1)
    Y = lambda v: B - (B - T) * v / ymax
    for v in range(0, 13, 2):
        d.line([(L, Y(v)), (R, Y(v))], fill=(228, 228, 228), width=2)
        d.text((L - 50, Y(v) - 16), str(v), font=fs, fill=(60, 60, 60))
    for yy in range(2027, 2047, 3):
        k = idx.index(S.MI[(yy, 1)])
        d.line([(X(k), B), (X(k), B + 10)], fill=(60, 60, 60), width=2)
        d.text((X(k) - 34, B + 16), str(yy), font=fs, fill=(60, 60, 60))
    d.line([(L, B), (R, B)], fill=(60, 60, 60), width=2)
    d.line([(L, T), (L, B)], fill=(60, 60, 60), width=2)
    x = L
    while x < R:
        d.line([(x, Y(S.LIMIT)), (min(x + 26, R), Y(S.LIMIT))], fill=(190, 30, 30), width=4)
        x += 40
    d.text((R - 330, Y(S.LIMIT) - 42), "WR-4 limit at OW-S, 9.0 ft", font=fs, fill=(190, 30, 30))
    for r in S.OPTIONS:
        town, field = res["series"][r]
        tot = (town + field)[idx]
        pts = [(X(k), Y(v)) for k, v in enumerate(tot)]
        d.line(pts, fill=COLS[r], width=5 if r == res["call"] else 3)
    d.text((L, 30), "Drawdown at OW-S by month, 2027 to 2046 (ft), each requested schedule", font=fb, fill=(20, 20, 20))
    lx = L + 30
    for r in S.OPTIONS:
        d.line([(lx, T + 24), (lx + 50, T + 24)], fill=COLS[r], width=6)
        d.text((lx + 60, T + 8), "{:,} gpm".format(r), font=f, fill=(20, 20, 20))
        lx += 230
    img.save(path, format="PNG")


def workbook(res, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Demonstration"
    bold = Font(bold=True)
    ws.append(["Reidel Road well field: Rule WR-4 demonstration at OW-S (limit %.1f ft)" % S.LIMIT])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Schedule (annual average gpm)", "Greatest monthly drawdown at OW-S in 2046 (ft)", "Nearest foot",
               "Greatest in the term (ft)", "Meets 4.1"])
    for c in ws[3]:
        c.font = bold
    for r in S.OPTIONS:
        ws.append([r, round(res["peaks"][r], 2), ft(res["peaks"][r]), round(res["peak_term"][r], 2),
                   "yes" if res["peaks"][r] <= S.LIMIT else "no"])
    ws.append([])
    ws.append(["Schedule the district will permit (WR-4 4.2)", "{:,} gpm".format(res["call"])])
    ws.cell(ws.max_row, 1).font = bold
    ws.cell(ws.max_row, 2).font = bold
    ws.append(["Drawdown the Mill Street wells caused at MS-MW, 2025 average (ft)", round(res["msmw_2025"], 2),
               ft(res["msmw_2025"])])
    ws.append(["Greatest monthly drawdown in 2046 at %s, nearest domestic well, %s gpm schedule (ft)" %
               (res["dw_id"], "{:,}".format(res["call"])), round(res["dw"], 2), ft(res["dw"])])
    t = wb.create_sheet("Aquifer test")
    t.append(["Quantity", "Value", "Basis"])
    for c in t[1]:
        c.font = bold
    t.append(["Average rate, PW-1 (gpm)", round(res["q_avg"], 1), "totalizer, 14 Sep 09:00 to 17 Sep 08:54"])
    t.append(["Transmissivity (ft2/day)", round(res["T"], 0), "Theis fit to OW-1, OW-2, OW-3"])
    t.append(["Storativity", float("%.3g" % res["S"]), "Theis fit to OW-1, OW-2, OW-3"])
    t.append(["Fit residual (ft, rms)", round(res["rms"], 3), "two minutes to three days"])
    for w in ("OW-1", "OW-2", "OW-3"):
        t.append(["Distance PW-1 to %s (ft)" % w, round(res["dist"][w], 0), "register coordinates"])
    for w, be in sorted(res["be"].items()):
        t.append(["Barometric efficiency, %s" % w, round(float(be), 2), "hourly first differences, 8 to 14 Sep"])
    m = wb.create_sheet("Mill Street record")
    m.append(["Month", "TW-1 (gpm)", "TW-2 (gpm)", "MS-MW elev (ft)", "CV-07 elev (ft)", "OW-S elev (ft)",
              "CV-02 elev (ft)", "CV-11 elev (ft)", "Drawdown MS-MW (ft)", "Drawdown CV-07 (ft)", "Drawdown OW-S (ft)",
              "Model MS-MW (ft)", "Model CV-07 (ft)", "Model OW-S (ft)"])
    for c in m[1]:
        c.font = bold
    q = res["q"]
    mods = {w: S.model_town(q["TW-1"], q["TW-2"], res["frame"], w, res["T"], res["S"], res["B"], res["width"])
            for w in ("MS-MW", "CV-07", "OW-S")}
    rnd = lambda v: None if (v is None or (isinstance(v, float) and math.isnan(v))) else round(float(v), 2)
    for i, (y, mo) in enumerate(S.MONTHS):
        if (y, mo) > (2026, 9):
            break
        m.append(["%04d-%02d" % (y, mo), rnd(q["TW-1"][i]), rnd(q["TW-2"][i]),
                  rnd(res["lv"]["MS-MW"][i]), rnd(res["lv"]["CV-07"][i]), rnd(res["lv"]["OW-S"][i]),
                  rnd(res["lv"]["CV-02"][i]), rnd(res["lv"]["CV-11"][i]),
                  rnd(res["att"]["MS-MW"][i]), rnd(res["att"]["CV-07"][i]), rnd(res["att"]["OW-S"][i]),
                  rnd(mods["MS-MW"][i]) if (y, mo) >= (2009, 3) else None,
                  rnd(mods["CV-07"][i]) if (y, mo) >= (2009, 3) else None,
                  rnd(mods["OW-S"][i]) if (y, mo) >= (2009, 3) else None])
    c = wb.create_sheet("Calibration")
    c.append(["Quantity", "Value"])
    for cc in c[1]:
        cc.font = bold
    c.append(["Natural level reference", "CV-02 and CV-11 (confined aquifer, beyond the Mill Street cone)"])
    c.append(["Walls", "Plate 3 mapped edges of saturated sand and gravel, %.0f ft apart" % res["width"]])
    c.append(["Leakage factor (ft)", res["B"]])
    c.append(["Wells fitted", "MS-MW, CV-07, OW-S, March 2009 to September 2026"])
    c.append(["Residual, MS-MW (ft, rms)", round(res["resid"]["MS-MW"], 2)])
    c.append(["Residual, CV-07 (ft, rms)", round(res["resid"]["CV-07"], 2)])
    c.append(["Residual, OW-S (ft, rms)", round(res["resid"]["OW-S"], 2)])
    f = wb.create_sheet("Forecast OW-S")
    hdr = ["Month", "Mill Street projection (gpm)", "Drawdown from Mill Street (ft)"]
    for r in S.OPTIONS:
        hdr += ["Reidel Road %d gpm schedule (gpm)" % r, "Total drawdown at %d gpm (ft)" % r]
    f.append(hdr)
    for cc in f[1]:
        cc.font = bold
    proj = S.town_projection()
    for i, (y, mo) in enumerate(S.MONTHS):
        if not (2027, 1) <= (y, mo) <= (2046, 12):
            continue
        town = res["series"][S.OPTIONS[0]][0][i]
        row = ["%04d-%02d" % (y, mo), round(float(proj[i]), 1), round(float(town), 2)]
        for r in S.OPTIONS:
            rate = r * S.NEW_SEASON[mo - 1] if (y, mo) >= (2027, 4) else 0.0
            tw, fd = res["series"][r]
            row += [round(rate, 1), round(float(tw[i] + fd[i]), 2)]
        f.append(row)
    for s in wb.worksheets:
        for col in s.columns:
            s.column_dimensions[col[0].column_letter].width = max(10, min(46, max(len(str(x.value or "")) for x in col) + 2))
    s = wb["Demonstration"]
    s.column_dimensions["A"].width = 52
    wb.properties.creator = "Harlow Springs Utilities"
    wb.properties.lastModifiedBy = "Harlow Springs Utilities"
    wb.save(path)
    ooxml.normalize(path, dt.datetime(2026, 11, 6, 14, 10), dt.datetime(2026, 11, 6, 16, 45))


SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.8, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.0, leading=10.2, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=8.4, leading=10.4, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333"))]))
    return t


def memo(res, rungs, path, png):
    call = res["call"]
    nxt = min(r for r in S.OPTIONS if r > call)
    s = [Paragraph("Reidel Road Well Field: Rule WR-4 Demonstration at Sentinel Well OW-S", H1),
         Paragraph("Harlow Springs Utilities, Water Division. For the Corrin Valley Water Conservancy District, with the "
                   "Reidel Road application. 6 November 2026.", SMALL),
         Spacer(1, 4),
         Paragraph("<b>The district will permit the %s gpm schedule.</b> Its greatest monthly drawdown at OW-S in 2046 is "
                   "%d ft against the Table 1 limit of %.1f ft; the %s gpm schedule reaches %d ft." %
                   ("{:,}".format(call), ft(res["peaks"][call]), S.LIMIT, "{:,}".format(nxt), ft(res["peaks"][nxt])), BODY),
         _table([["Schedule (annual average)", "Greatest monthly drawdown at OW-S, 2046", "Within 9.0 ft"]] +
                [["{:,} gpm".format(r), "%d ft" % ft(res["peaks"][r]), "yes" if res["peaks"][r] <= S.LIMIT else "no"]
                 for r in S.OPTIONS], [48, 70, 30]),
         Spacer(1, 6),
         Image(png, width=170 * mm, height=93.5 * mm),
         Paragraph("Each line is the drawdown at OW-S in every month from January 2027 to December 2046 from the "
                   "Reidel Road schedule and the Mill Street wells at their filed projection. Every schedule's "
                   "greatest month falls in 2046.", SMALL),
         Paragraph("At %s, the registered domestic well nearest the field (Rule WR-4 4.4), the %s gpm schedule's "
                   "greatest monthly drawdown in 2046 is %d ft." % (res["dw_id"], "{:,}".format(call), ft(res["dw"])), BODY),
         Paragraph("The aquifer test", H2),
         Paragraph("The 72-hour test of PW-1 (14 to 17 September 2026, %.0f gpm on the totalizer) fits the Theis "
                   "solution at OW-1, OW-2 and OW-3 to %.2f ft: transmissivity %s ft2/day, storativity %.1e. Over three "
                   "days the test cannot see what limits the drawdown over twenty years: carried forward unchanged, "
                   "the same fit puts the Mill Street wells' 2025 drawdown at their monitoring well near %d ft." %
                   (res["q_avg"], res["rms"], "{:,}".format(int(round(res["T"], -1))), res["S"],
                    ft(rungs["theis_msmw_2025"])), BODY),
         Paragraph("The Mill Street record", H2),
         Paragraph("The monitoring readings since 2005 rise and fall with the region's wet and dry years, and the "
                   "2010s and early 2020s were wet against the 2005 to 2008 baseline. CV-07, the nearest network well "
                   "in the aquifer, sits inside the Mill Street cone: its departure from the far network wells deepens "
                   "with each step in Mill Street pumping and follows the summer peak. CV-02 and CV-11, beyond the "
                   "cone, move together and moved with OW-S before pumping began, so they carry the natural level. "
                   "Against it the Mill Street wells drew MS-MW down %d ft on average in 2025." %
                   ft(res["msmw_2025"]), BODY),
         Paragraph("The far field", H2),
         Paragraph("With the valley walls at the mapped edges of the saturated sand and gravel on Plate 3 (%s ft apart) "
                   "and the test's transmissivity and storativity, leakage through the till with a leakage factor of "
                   "%s ft reproduces the drawdown at MS-MW, CV-07 and OW-S from March 2009 to September 2026. "
                   "Read against CV-07 or the wells' own 2005 to 2008 levels, the same record would ask for a leakage "
                   "factor near %s ft and put every schedule under %d ft at OW-S, crediting the wet years to leakage." %
                   ("{:,}".format(int(res["width"])), "{:,}".format(int(res["B"])),
                    "{:,}".format(int(round(rungs["cv07_B"], -2))), ft(rungs["cv07_peak_max"]) + 1), BODY),
         Paragraph("Schedules", H2),
         Paragraph("Reidel Road begins in April 2027, shared equally by PW-1 and PW-2, at each schedule's monthly "
                   "factors; the Mill Street wells follow the projection filed in the 2026 water supply plan update "
                   "(56 per cent TW-1, 44 per cent TW-2). The monthly working is in reidel_road_sentinel_forecast.xlsx.",
                   BODY)]
    O.build(path, s, "Reidel Road Well Field: Rule WR-4 Demonstration", "Harlow Springs Utilities",
            "WR-4 demonstration at OW-S for the Reidel Road schedules", "Harlow Springs Utilities, Water Division",
            dt.datetime(2026, 11, 6, 15, 30, tzinfo=EDT), dt.datetime(2026, 11, 6, 16, 52, tzinfo=EDT))


def write(res, rungs, gdir, scratch):
    os.makedirs(gdir, exist_ok=True)
    workbook(res, os.path.join(gdir, "reidel_road_sentinel_forecast.xlsx"))
    png = os.path.join(scratch, "ows_chart.png")
    chart(res, png)
    memo(res, rungs, os.path.join(gdir, "reidel_road_WR-4_demonstration.pdf"), png)
