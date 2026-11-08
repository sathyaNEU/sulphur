"""task3 architecture 4: the golden deliverables from the solution on the cut pack. The memo to the Common Council
(PDF), the forecast workbook and the chart of the entry point's annual mean against 10 mg/L."""
import datetime as dt
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font
from PIL import Image as PImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

import officepdf as O
import ooxml
import params as P
import solve as S

CST = dt.timezone(dt.timedelta(hours=-6))
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
NAMES = {"FOR": "Forest", "GRS": "Grass and pasture", "DRY": "Cropland, not irrigated",
         "IRC": "Irrigated corn and soybean", "IRV": "Irrigated vegetables", "RES": "Residential", "WAT": "Wetland"}


WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def mg(x):
    return int(math.floor(x + 0.5))


def ep_observed(D):
    out = {}
    for t, x in D["well_samples"].get("EP", []):
        out.setdefault(int(t), []).append(x)
    return {y: float(np.mean(v)) for y, v in out.items()}


def cohort_rows(res):
    D = res["D"]
    fit = res["fit"]
    rows = []
    for s in sorted(S.cohort(D), key=lambda s: s["dtw"]):
        ser = s["series"]
        pre = [x for t, x in ser if s["c"] - 3 <= t < s["c"] + 1.0]
        post = [x for t, x in ser if t >= 2019.0]
        t = S.arrival(ser, s["c"])
        if not pre:
            continue
        age = D["ages"].get(s["sid"], float(np.mean(list(D["ages"].values()))))
        h = D["lc"][D["sites"][s["sid"]]["pid"]]
        rows.append([s["sid"], D["sites"][s["sid"]]["pid"], s["dtw"], s["c"], "%s to %s" % (NAMES[h[s["c"] - 1]],
                     NAMES[h[s["c"]]]), round(float(np.mean(pre)), 2), round(float(np.mean(post)), 2),
                     None if t is None else round(t, 2), round(age, 2),
                     None if t is None else round(t - s["c"] - age, 2),
                     round(fit["a"] + fit["b"] * s["dtw"], 2)])
    return rows


def parcel_rows(res):
    D = res["D"]
    fit = res["fit"]
    rows = []
    for p in sorted(D["parcels"], key=lambda p: (p["zone"], p["pid"])):
        h = D["lc"][p["pid"]]
        cl = next((y for y in range(2013, 2027) if h[y] in P.IRRIGATED and h[y - 1] not in P.IRRIGATED), None)
        u = fit["a"] + fit["b"] * p["dtw"]
        rows.append([p["pid"], P.WELL_NAMES[p["zone"]], p["acres"], p["dtw"], p["T"], NAMES[h[2026]],
                     D["recharge"][h[2026]], cl, round(u, 2), None if cl is None else round(cl + u + p["T"], 2)])
    return rows


def workbook(res, path):
    D = res["D"]
    bold = Font(bold=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Decision"
    hi = max(P.WELLS, key=lambda w: res["fc"][w][2034])
    ws.append(["Project NR-1: nitrate removal plant, loan cycle"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    rows = [["Cycle to apply in", "%d cycle (intent to apply by 15 December 2026)" % res["call"]],
            ["First year the entry point's annual mean reaches 10 mg/L as N", res["cross"]],
            ["In service, 2027 cycle", "1 January %d" % P.CYCLES[2027]],
            ["In service, 2031 cycle", "1 January %d" % P.CYCLES[2031]],
            ["Entry point annual mean, 2034 (mg/L as N)", round(res["ep"][2034], 2)],
            ["Well with the highest annual mean in 2034", P.WELL_NAMES[hi]],
            ["Its annual mean, 2034 (mg/L as N)", round(res["fc"][hi][2034], 2)],
            ["Basis", "annual flow-weighted mean at EP-01 under the 2025 plan's shares; land cover held at 2026"]]
    for r in rows:
        ws.append(r)
        ws.cell(ws.max_row, 1).font = bold
    f = wb.create_sheet("Forecast")
    hdr = ["Year"] + ["%s (mg/L as N)" % P.WELL_NAMES[w] for w in P.WELLS] + \
          ["Share %s" % P.WELL_NAMES[w] for w in P.WELLS] + ["Entry point EP-01 (mg/L as N)", "At or above 10"]
    f.append(hdr)
    for c in f[1]:
        c.font = bold
    for y in P.FC_YEARS:
        f.append([y] + [round(res["fc"][w][y], 2) for w in P.WELLS] + [P.PLAN_SHARE[w] for w in P.WELLS] +
                 [round(res["ep"][y], 2), "yes" if res["ep"][y] >= P.LIMIT else "no"])
    u = wb.create_sheet("Unsaturated delay")
    u.append(["County network wells whose parcel was put under irrigation, 1987 to 2010"])
    u["A1"].font = bold
    u.append(["Site", "Parcel", "Depth to water (ft)", "Irrigated from", "Change", "Level before (mg/L)",
              "Level since 2019 (mg/L)", "Half-way arrival (year)", "Water-table age (yr)",
              "Delay to the water table (yr)", "Fitted delay (yr)"])
    for c in u[2]:
        c.font = bold
    for r in cohort_rows(res):
        u.append(r)
    u.append([])
    fit = res["fit"]
    u.append(["Delay to the water table = a + b x depth to water"])
    u.cell(u.max_row, 1).font = bold
    u.append(["a (yr)", round(fit["a"], 3)])
    u.append(["b (yr per ft)", round(fit["b"], 4)])
    u.append(["Wells", fit["n"]])
    u.append(["Residual (yr, rms)", round(fit["rmse"], 2)])
    lch = wb.create_sheet("Leachate")
    lch.append(["Land cover", "Nitrate reaching the water table, current farming (mg/L as N)",
                "Recharge (in/yr, wellhead model)"])
    for c in lch[1]:
        c.font = bold
    for c in ("FOR", "GRS", "DRY", "IRC", "IRV", "RES"):
        lch.append([NAMES[c], round(res["curves"][c]["last"], 2), D["recharge"][c]])
    lch.append([])
    lch.append(["Land-surface year", "Irrigated vegetables (mg/L)", "Irrigated corn and soybean (mg/L)",
                "Cropland, not irrigated (mg/L)"])
    for c in lch[lch.max_row]:
        c.font = bold
    cf = res["curves_full"]
    for y in range(1986, 2025):
        lch.append([y] + [round(cf[c]["val"][y], 2) if y in cf[c]["val"] else None for c in ("IRV", "IRC", "DRY")])
    pp = wb.create_sheet("Protection area parcels")
    pp.append(["Parcel", "Zone", "Acres", "Depth to water (ft)", "Groundwater time of travel (yr)", "Land cover 2026",
               "Recharge (in/yr)", "Irrigated from (since 2013)", "Delay to the water table (yr)",
               "Half-way arrival at the well (year)"])
    for c in pp[1]:
        c.font = bold
    for r in parcel_rows(res):
        pp.append(r)
    wr = wb.create_sheet("Wells record")
    wr.append(["Year"] + ["%s observed" % P.WELL_NAMES[w] for w in P.WELLS] +
              ["%s model" % P.WELL_NAMES[w] for w in P.WELLS] + ["EP-01 observed"])
    for c in wr[1]:
        c.font = bold
    epo = ep_observed(D)
    for y in range(1990, 2027):
        wr.append([y] + [round(res["obs"][w][y], 2) if y in res["obs"][w] else None for w in P.WELLS] +
                  [round(res["model"][w][y], 2) if y >= 1992 else None for w in P.WELLS] +
                  [round(epo[y], 2) if y in epo else None])
    wr.append([])
    wr.append(["Model carried to each well's 2019-2026 level (mg/L)"] + [round(res["resid"][w], 2) for w in P.WELLS])
    nt = wb.create_sheet("Notes")
    for line in [
        "Nitrate results converted to mg/L as N (county laboratory results reported as nitrate divided by 4.427); "
        "field duplicates and re-runs averaged with their sample.",
        "Each county network well's arrival is the time its nitrate first passed half-way from its level before "
        "irrigation to its level since 2019; the delay to the water table is that time less the year irrigation began "
        "and the well's tritium-helium age (2019 survey; the survey mean where a well was not sampled).",
        "Leachate by land cover: the network's wells on unchanged land, each sample dated back to the year its water "
        "left the root zone; the current level is the mean of the five latest land-surface years.",
        "Each protection-area parcel's water reaches its well after the delay to the water table for its depth and the "
        "wellhead model's groundwater time of travel; each well mixes its parcels by acres times the recharge the "
        "parcel had when the water left the water table.",
        "Each well's model is carried to its observed 2019-2026 level; the entry point blends the wells by the 2025 "
        "plan's shares; land cover after 2026 held as it stood in 2026.",
        "Sources: corlinden_raw_water_nitrate_results_1988-2026.csv, ravell_county_groundwater_network_samples_1990-2026"
        ".csv, ravell_county_groundwater_network_sites.xlsx, ravell_county_parcel_land_cover_1986-2026.csv, "
        "ravell_county_groundwater_age_survey_2019.xlsx, sallow_road_WHPA_parcel_attributes_2019.xlsx, "
        "corlinden_water_supply_plan_2025.pdf."]:
        nt.append([line])
    for s in wb.worksheets:
        if s.title not in ("Decision", "Notes"):
            s.freeze_panes = "B2" if s.title in ("Forecast", "Wells record", "Protection area parcels") else "A3"
        for row in s.iter_rows():
            for cell in row:
                if isinstance(cell.value, float):
                    cell.number_format = "0.00"
        for col in s.columns:
            s.column_dimensions[col[0].column_letter].width = max(10, min(44, max(len(str(x.value or "")) for x in col) + 2))
    wb["Decision"].column_dimensions["A"].width = 62
    wb["Decision"].column_dimensions["B"].width = 60
    wb["Notes"].column_dimensions["A"].width = 120
    wb.properties.creator = "Corlinden Water Utility"
    wb.properties.lastModifiedBy = "Corlinden Water Utility"
    wb.save(path)
    ooxml.normalize(path, dt.datetime(2026, 11, 5, 16, 20), dt.datetime(2026, 11, 6, 15, 48), "Corlinden Water Utility")


def chart(res, path):
    W_, H_ = 2000, 1120
    img = PImage.new("RGB", (W_, H_), "white")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 30)
    fs = ImageFont.truetype(FONT, 26)
    fb = ImageFont.truetype(FONTB, 34)
    L_, R_, T_, B_ = 150, 1950, 150, 950
    y0, y1, vmax = 2010, 2040, 14.0
    X = lambda y: L_ + (R_ - L_) * (y + 0.5 - y0) / (y1 + 1 - y0)
    Y = lambda v: B_ - (B_ - T_) * v / vmax
    for v in range(0, 15, 2):
        d.line([(L_, Y(v)), (R_, Y(v))], fill=(230, 230, 230), width=2)
        d.text((L_ - 50, Y(v) - 16), str(v), font=fs, fill=(60, 60, 60))
    for yy in range(2010, 2041, 5):
        d.line([(X(yy), B_), (X(yy), B_ + 10)], fill=(60, 60, 60), width=2)
        d.text((X(yy) - 34, B_ + 16), str(yy), font=fs, fill=(60, 60, 60))
    d.line([(L_, B_), (R_, B_)], fill=(60, 60, 60), width=2)
    d.line([(L_, T_), (L_, B_)], fill=(60, 60, 60), width=2)
    x = L_
    while x < R_:
        d.line([(x, Y(P.LIMIT)), (min(x + 26, R_), Y(P.LIMIT))], fill=(190, 30, 30), width=4)
        x += 40
    d.text((L_ + 20, Y(P.LIMIT) - 42), "Nitrate standard, 10 mg/L as N", font=fs, fill=(190, 30, 30))
    for k, (cyc, yr) in enumerate(sorted(P.CYCLES.items())):
        xx = X(yr) - (X(yr) - X(yr - 1)) / 2
        ty = T_ + 20 + 44 * k
        d.line([(xx, ty), (xx, B_)], fill=(120, 120, 120), width=2)
        lab = "%d cycle in service" % cyc
        w = d.textlength(lab, font=fs)
        d.text((xx - w - 10, ty), lab, font=fs, fill=(90, 90, 90))
    epo = ep_observed(res["D"])
    pts = [(X(y), Y(v)) for y, v in sorted(epo.items()) if y >= y0]
    d.line(pts, fill=(80, 80, 80), width=4)
    for p in pts:
        d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=(80, 80, 80))
    fpts = [(X(y), Y(res["ep"][y])) for y in P.FC_YEARS]
    d.line([pts[-1]] + fpts, fill=(25, 70, 150), width=6)
    for p in fpts:
        d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=(25, 70, 150))
    d.text((L_, 34), "EP-01 passes 10 mg/L as N in %d, %d years before a 2031-cycle plant could run" %
           (res["cross"], P.CYCLES[2031] - res["cross"]), font=fb, fill=(20, 20, 20))
    d.text((L_, 78), "Annual flow-weighted mean nitrate at entry point EP-01 (mg/L as N)", font=fs, fill=(70, 70, 70))
    cx, cy = X(res["cross"]), Y(res["ep"][res["cross"]])
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=(190, 30, 30), width=4)
    d.text((cx + 22, cy + 18), "%d: %.1f" % (res["cross"], res["ep"][res["cross"]]), font=f, fill=(190, 30, 30))
    d.line([(R_ - 560, B_ - 120), (R_ - 510, B_ - 120)], fill=(80, 80, 80), width=5)
    d.text((R_ - 495, B_ - 136), "EP-01 record, %d-2026" % min(epo), font=f, fill=(20, 20, 20))
    d.line([(R_ - 560, B_ - 70), (R_ - 510, B_ - 70)], fill=(25, 70, 150), width=6)
    d.text((R_ - 495, B_ - 86), "Forecast, 2025 pumping plan", font=f, fill=(20, 20, 20))
    img.save(path, format="PNG", optimize=True)


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


def memo(res, rungs, F, path, png):
    hi = F["hi_well_name"]
    s = [Paragraph("Project NR-1 belongs on the 2027 loan cycle", H1),
         Paragraph("To the Corlinden Common Council, for its December 2026 meeting. From Chloe Griffin, general "
                   "manager. 6 November 2026.", SMALL),
         Spacer(1, 4),
         Paragraph("<b>Put the nitrate removal plant on the 2027 cycle.</b> The entry point's annual mean nitrate "
                   "first reaches 10 mg/L as N in %d and is about %d mg/L by 2034, so a plant funded in the 2031 "
                   "cycle, in service on 1 January %d, would come %s years late. Funded in 2027 it is in service "
                   "on 1 January %d." % (F["cross"], F["ep2034_int"], P.CYCLES[2031], WORDS[P.CYCLES[2031] - F["cross"]],
                                          P.CYCLES[2027]), BODY),
         _table([["", "2027", "2029", "2030", "2031", "2032", "2034", "2040"],
                 ["EP-01 annual mean (mg/L as N)"] + ["%.1f" % res["ep"][y] for y in (2027, 2029, 2030, 2031, 2032, 2034, 2040)]],
                [52, 16, 16, 16, 16, 16, 16, 16]),
         Paragraph("Source: corlinden_entry_point_nitrate_forecast.xlsx, sheet Forecast. Nitrate as N throughout; the "
                   "county laboratory's results before 2004, reported as nitrate, are divided by 4.427.", SMALL),
         Spacer(1, 4),
         Image(png, width=150 * mm, height=84.0 * mm),
         Paragraph("The forecast blends the wells by the 2025 plan's shares (Well 3 at 8 per cent from 2027) with "
                   "land cover held as it stood in 2026. %s carries the most nitrate, about %d mg/L in 2034." %
                   (hi, F["hi_2034_int"]), SMALL),
         Paragraph("Why the record looks safe", H2),
         Paragraph("EP-01 fell from about %.1f mg/L in %d to %.1f in 2025 as water from the years of nutrient "
                   "management reached the wells, and Wells 6 and 7 show no rise. Their zones of contribution take in "
                   "the Sallow Ridge, about %s acres of timber Hartvale Produce cleared for irrigated vegetables from "
                   "%d to %d, %.0f to %.0f years' groundwater travel from the wells. Taken at that travel time, or at "
                   "the one lag of about %.1f years that fits the wells' own record before the clearing, the ridge's "
                   "nitrate should already show at Wells 6 and 7; it does not, and a model fitted to the record sets "
                   "the clearing's effect to nothing." % (F["ep_obs_2010"], F["ep_obs_first_year"], F["ep_obs_2025"],
                                                            "{:,}".format(F["ridge_acres"]), F["ridge_years"][0],
                                                            F["ridge_years"][1], F["ridge_T"][0], F["ridge_T"][1],
                                                            F["single_lag"]), BODY),
         Paragraph("Why it is coming", H2),
         Paragraph("The wellhead model's travel time starts at the water table, and on the ridge the water table is "
                   "%d to %d ft down through dry sand. The county's own wells show how long that takes: the %d network "
                   "wells whose land was put under irrigation between %d and %d each stepped up after a delay that "
                   "grew with the depth to water, about %.2f years a foot (about %.0f year at %d ft, %.0f at %d ft), "
                   "while their water-table ages are under half a year. The %s network wells under the %d to %d "
                   "upland clearings, at %d to %d ft, show nothing yet, as that delay says they should. Carried to each "
                   "ridge parcel's own depth, the leachate reaches the water table from %d and the wells late in "
                   "%d." % (F["ridge_dtw"][0], F["ridge_dtw"][1], F["n"], F["cohort_years"][0], F["cohort_years"][1],
                            F["b"], F["cohort_delay_ends"][0], F["cohort_dtw"][0], F["cohort_delay_ends"][1],
                            F["cohort_dtw"][1], WORDS[F["recent_n"]], F["recent_years"][0], F["recent_years"][1],
                            F["recent_dtw"][0], F["recent_dtw"][1], F["wt_arrive_lo"], F["arrive_lo"]), BODY),
         Paragraph("Under irrigated vegetables the network's water now carries about %d mg/L as N, down from about "
                   "%d before nutrient management. Mixed into each well by its parcels' recharge, the ridge takes "
                   "Well 6 to about %d and Well 7 to about %d mg/L, and the entry point past 10 in %d." %
                   (F["irv_int"], F["irv_pre_int"], F["w6_2034_int"], F["w7_2034_int"], F["cross"]), BODY),
         Paragraph("What the forecast rests on", H2),
         Paragraph("The delay comes from the network's matured conversions, fitted with a residual of %.1f years; "
                   "the result does not move if the half-way arrival is read as a fitted step, if the delay is taken "
                   "through the origin, or if the model is left uncarried to the wells' 2019-2026 level (the first "
                   "year at 10 stays %d, the 2034 entry point %d mg/L). The forecast holds the land cover of 2026; "
                   "further clearing in the zones would bring the date forward. The working is in "
                   "corlinden_entry_point_nitrate_forecast.xlsx." % (F["fit_rmse"], F["cross"], F["ep2034_int"]), BODY)]
    O.build(path, s, "Project NR-1 belongs on the 2027 loan cycle", "Corlinden Water Utility",
            "Nitrate removal plant loan cycle, memo to the Common Council", "Corlinden Water Utility",
            dt.datetime(2026, 11, 6, 9, 30, tzinfo=CST), dt.datetime(2026, 11, 6, 15, 52, tzinfo=CST))


def write(res, rungs, F, gdir, scratch):
    os.makedirs(gdir, exist_ok=True)
    workbook(res, os.path.join(gdir, "corlinden_entry_point_nitrate_forecast.xlsx"))
    png = os.path.join(gdir, "corlinden_entry_point_nitrate_2027-2040.png")
    chart(res, png)
    memo(res, rungs, F, os.path.join(gdir, "corlinden_nitrate_plant_timing_memo.pdf"), png)
