"""task3 checks: the input gates, the Sulfur block (R1 to R6), every semantic fork (SF1 to SF21), the graded cells and
their margins, the back-test, the literal reader, the distractors and the realism sweep, on the installed pack."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import figures as FG  # noqa: E402
import freq as F  # noqa: E402
import pack as pk  # noqa: E402

RES = []


def check(label, ok, detail=""):
    RES.append((label, bool(ok), detail))


def pdf_text(path):
    raw = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout
    return re.sub(r"\s+", " ", raw)


def span_of(q):
    ok = [sp for sp, rated in DC.SPANS if rated >= q]
    return min(ok) if ok else None


def edge(v, unit=5000):
    """Distance from v to the nearest rounding edge of its unit, as a share of v."""
    return (unit / 2.0 - abs(v - round(v / unit) * unit)) / v


EST = {}


def estimates(tgt):
    if tgt not in EST:
        PV, TV, ZV = A.valley_daily(tgt)
        PR, TR = A.ridge_daily(tgt)
        sh = A.snotel(tgt, "snotel_1187_hatchet_meadow_daily.csv")
        sc = A.snotel(tgt, "snotel_1203_corbel_ridge_daily.csv")
        lapse = A.storm_lapse(PV, TV, PR, TR, ZV)[0]
        th, tc = A.rain_snow_temperature(sh), A.rain_snow_temperature(sc)
        t50, k = (th[0] + tc[0]) / 2.0, (th[1] + tc[1]) / 2.0
        st_list = A.storms(PV)
        g = A.orographic(st_list, PV, TV, PR, ZV, lapse, t50)[0]
        EST[tgt] = dict(lapse=lapse, t50=t50, k=k, g=g, bands=A.bands(tgt), lcd=A.read_lcd(tgt), fh=A.flood_hours(tgt),
                        PV=PV, TV=TV, ZV=ZV, PR=PR, sh=sh, sc=sc)
    return EST[tgt]


def carry(tgt, **kw):
    """The golden carry with options; returns the Bulletin 17C parameters, the quantiles and the series."""
    e = estimates(tgt)
    T, P, zv = kw.pop("lcd", None) or e["lcd"]
    fh, annual = e["fh"]
    zc, ar, ac, areas, area_c = e["bands"]
    lapse = kw.pop("lapse", e["lapse"])
    t50 = kw.pop("t50", e["t50"])
    g = kw.pop("g", e["g"])
    b = kw.pop("b", A.STATE_B)
    drop_years = kw.pop("drop_years", ())
    fh = [x for x in fh if (x[0].year + (1 if x[0].month >= 10 else 0)) not in drop_years]
    ser = A.transfer_hourly(fh, T, P, zc, ar, ac, lapse, t50, e["k"], g, b, zv, **kw)
    par, vals, missing = A.curve_of(ser, years=[y for y in range(1951, 2026) if y not in drop_years])
    return par, {a: F.quantile(par, a) for a in A.AEPS}, ser


def cells(par, ser):
    q50, q01 = F.quantile(par, 0.5), F.quantile(par, 0.01)
    return dict(q50=FG.k5000(q50), q01=FG.k5000(q01), span=span_of(q01),
                bands=tuple(FG.band(F.aep_of(par, rq)) for _, rq in DC.SPANS), top2=frozenset(FG.top_years(ser)))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    A.STATE_B = round(fig["equations"]["100"]["b"], 3)
    R = A.run(TGT)
    e = fig["equations"]["100"]
    R["regional_eq"] = e["a"] * R["area_c"] ** e["b"] * R["map_creek"] ** e["c"]
    q = R["q"]
    G = {a: q[a] for a in A.AEPS}
    GC = cells(R["par"], R["series"])
    files = sorted(os.listdir(TGT))
    V = R["variants"]

    # ------------------------------------------------------------------ input gates
    check("I1 ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {("spreadsheet" if f.endswith((".csv", ".xlsx")) else "text") for f in files}
    check("I2 two or more file categories", len(cats) >= 2, str(sorted(cats)))
    rows = {f: sum(1 for _ in open(os.path.join(TGT, f))) for f in files if f.endswith(".csv")}
    check("I3 a CSV of 20,000 rows or more", max(rows.values()) >= 20000, str(rows))
    check("I4 a second large CSV (10 to 20 printed pages or more, about 600 rows or more)",
          sorted(rows.values())[-2] >= 600, str(sorted(rows.values())[-2]))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("I5 two or more distractors, named only in metadata.json", len(meta["distractors"]) >= 2
          and not any("distract" in f.lower() for f in files), str(meta["distractors"]))
    check("I6 no file describes the data (readme, dictionary, notes, manifest)",
          not any(re.search(r"readme|dictionar|notes|manifest|field_guide", f, re.I) for f in files))
    check("I7 every shipped file has provenance in metadata.json", set(files) == set(meta["files"]))

    # ------------------------------------------------------------------ the call and the graded cells
    check("C1 the golden's 1 per cent flood lands the 185 ft span", GC["span"] == 185, "%.0f" % G[0.01])
    check("C2 figures.json carries the call and the cells", fig["call_span_ft"] == 185 and fig["q50_5000"] == GC["q50"]
          and fig["q01_5000"] == GC["q01"] and tuple(fig["bands"][str(s)] for s, _ in DC.SPANS) == GC["bands"]
          and frozenset(fig["top2"]) == GC["top2"])
    check("C3 the 50 per cent flow sits 5 per cent or more inside its 5,000 cfs cell", edge(G[0.5]) >= 0.05,
          "%.0f (%.3f)" % (G[0.5], edge(G[0.5])))
    check("C3 the 1 per cent flow sits 5 per cent or more inside its 5,000 cfs cell", edge(G[0.01]) >= 0.05,
          "%.0f (%.3f)" % (G[0.01], edge(G[0.01])))
    for sp, rq in DC.SPANS:
        aep = F.aep_of(R["par"], rq)
        edges = [x for x in (0.10, 0.01, 0.001)]
        dist = min(abs(np.log(aep / x)) for x in edges)
        check("C4 the %d ft span's exceedance band holds with a quarter of a band or more to spare" % sp, dist >= 0.30,
              "AEP %.4f, log distance %.2f" % (aep, dist))
    ser_sorted = sorted(R["series"].values(), reverse=True)
    check("C5 the second largest carried flood clears the third by 10 per cent or more", ser_sorted[1] >= 1.10 * ser_sorted[2],
          "%.0f against %.0f" % (ser_sorted[1], ser_sorted[2]))
    check("C6 the call carries margin both ways (1 per cent flood 8 per cent or more from each rated line)",
          G[0.01] >= 1.08 * dict(DC.SPANS)[140] and G[0.01] <= dict(DC.SPANS)[185] / 1.08, "%.0f" % G[0.01])

    # ------------------------------------------------------------------ the Sulfur block
    names = []
    for f in files:
        if f.endswith(".csv"):
            names += open(os.path.join(TGT, f)).readline().lower().split(",")
    check("R1 the decisive quantity has no column (no snow line, rain share or contributing area anywhere)",
          not any(re.search(r"snow.?line|freezing|contribut|rain.?share|lapse", n) for n in names))
    check("R1b the golden reads the peaks, the stations, the hourly record and the bands (raw material, not a list)",
          R["n_matched"] > 150 and R["n_lapse"] > 1000 and len(R["series"]) >= 70)
    D = fig["default"]
    check("R3a the analyst test: the drainage-area transfer files 140 ft", span_of(R["r0"]) == 140, "%.0f" % R["r0"])
    check("R3a the drainage-area transfer misses every graded cell but the 240 ft band",
          D["q50_5000"] != GC["q50"] and D["q01_5000"] != GC["q01"] and not (frozenset(D["top2"]) & GC["top2"])
          and [D["bands"][str(s)] == fig["bands"][str(s)] for s, _ in DC.SPANS] == [False, False, True])
    check("R3b a lower rung's single correction (a textbook snow line) files 240 ft", V["textbook"]["par"] is not None
          and span_of(V["textbook"][0.01]) == 240, "%.0f" % V["textbook"][0.01])
    no_line = carry(TGT, t50=-50.0)[1][0.01]
    check("R4 link 1 (rain only below the snow line) skipped: whole-basin rain files 140 ft", span_of(no_line) == 140,
          "%.0f" % no_line)
    check("R4 link 2 (the orographic rise) skipped files 240 ft", span_of(V["no_orography"][0.01]) == 240,
          "%.0f" % V["no_orography"][0.01])
    check("R4 link 3 (the storm lapse) skipped: the standard atmosphere files 240 ft", span_of(V["lapse_6.5"][0.01]) == 240,
          "%.0f" % V["lapse_6.5"][0.01])
    fac = float(np.median([r[6] / r[1] for r in R["rows"]]))
    single = F.quantile(R["river_par"], 0.01) * fac
    check("R4 link 4 (each flood at its own ratio) skipped: one median ratio on the river's curve files 240 ft",
          span_of(single) == 240, "%.0f (median ratio %.2f)" % (single, fac))
    dsm = cells(V["daily_storm_mean"]["par"], V["daily_storm_mean"]["series"])
    dwd = cells(V["daily_wettest_day"]["par"], V["daily_wettest_day"]["series"])
    check("R4 link 5 (the rain's own temperature) skipped: the valley's daily temperatures move graded cells",
          dsm["q01"] != GC["q01"] and dsm["bands"] != GC["bands"] and True,
          "storm mean %.0f %s; wettest day top2 %s" % (V["daily_storm_mean"][0.01], dsm["bands"][0], sorted(dwd["top2"])))
    check("R5 the one-fact test: the hint with the textbook constants it invites still files a wrong span",
          span_of(V["lapse_6.5"][0.01]) == 240 and span_of(V["textbook"][0.01]) == 240)
    check("R6 rival: the region's mean unit flood files 140 ft", span_of(R["regional_unit_flood"]) == 140,
          "%.0f" % R["regional_unit_flood"])
    check("R6 rival: the state equation files 140 ft and the creek's precipitation is under its range",
          span_of(R["regional_eq"]) == 140 and R["map_creek"] < fig["equation_ranges"]["map"][0],
          "%.0f, %.1f in against %s" % (R["regional_eq"], R["map_creek"], fig["equation_ranges"]["map"]))
    lo_, hi_ = R["elev_reg_interval"]
    check("R6 rival: an elevation regression over the five high gauges (mean elevations %d to %d ft, unit floods alike) "
          "carries no elevation effect to the creek and files 140 ft" % R["elev_range"], span_of(R["elev_reg"]) == 140,
          "%.0f (90 per cent interval %.0f to %.0f)" % (R["elev_reg"], lo_, hi_))
    family = ("gap_3", "gap_12", "gap_24", "rain_hour_mean", "wettest_24h", "sharp", "annual_only", "b_1.0", "b_0.70",
              "lapse_snotel", "t50_hatchet", "t50_corbel", "station_skew", "no_low_test")
    for name in family:
        c_ = cells(V[name]["par"], V[name]["series"])
        check("R6 standing family member %s files every graded cell the golden files" % name, c_ == GC,
              "%.0f, %.0f, %s" % (V[name][0.5], V[name][0.01], c_ if c_ != GC else ""))

    # ------------------------------------------------------------------ the semantic forks
    std = pdf_text(os.path.join(TGT, "pelton_county_road_standards_ch7_excerpt.pdf"))
    check("P0 positive control: the standard's text is read", "Road Design Standards" in std and len(std) > 2000)
    check("SF1 the instantaneous peak is filed", "instantaneous peak discharge at the bridge" in std)
    check("SF2 the records' climate is filed, no future-climate allowance", "No allowance for a future climate" in std)
    wb = A.bands(TGT)[3]
    check("SF3 the nearest gauged basin with 25 years is the Coyner River (the workbook's distances)",
          "nearest gauged basin" in std and "12183450" in wb)
    check("SF4 Bulletin 17C filed; the station skew keeps every cell", "Bulletin 17C" in std
          and cells(V["station_skew"]["par"], R["series"]) == GC)
    tm = pdf_text(os.path.join(TGT, "hess_tm_durrow_creek_bridge_span_ratings.pdf"))
    check("SF5 the rated flows are the memorandum's (2.0 ft freeboard)", all("{:,}".format(qq) in tm for _, qq in DC.SPANS)
          and "freeboard" in tm and "2.0 ft" in tm)
    check("SF6 at least the flood", "at least the design flood" in std)
    p7 = A.curve_of({y: v for y, v in R["series"].items()}, years=[y for y in range(1951, 2026) if y in R["series"]])[0]
    check("SF7 the year with no flood fed by rain, dropped instead of censored, keeps every cell",
          cells(p7, R["series"]) == GC, "%.0f" % F.quantile(p7, 0.01))
    for back in (24, 48):
        p8, _, s8 = carry(TGT, back=back)
        check("SF8 a %d-hour look-back for the rain keeps every cell" % back, cells(p8, s8) == GC)
    for how in ("mean", "core"):
        p9, _, s9 = carry(TGT, how=how)
        check("SF9 the %s temperature weighting keeps every cell" % how, cells(p9, s9) == GC)
    check("SF10 a sharp rain-snow threshold keeps every cell", cells(V["sharp"]["par"], V["sharp"]["series"]) == GC)
    for b in (0.6, 1.0):
        pb, qb, sb = carry(TGT, b=b)
        check("SF11 a drainage-area exponent of %.1f keeps every cell" % b, cells(pb, sb) == GC, "%.0f" % qb[0.01])
    p12, _, s12 = carry(TGT, lapse=_spliced_lapse(TGT))
    check("SF12 the 1988 station move read as one elevation keeps the call", span_of(F.quantile(p12, 0.01)) == 185,
          "%.0f" % F.quantile(p12, 0.01))
    check("SF13 multi-day totals on their last day keep every cell", _mdpr_last(TGT) == GC)
    p14, _, s14 = carry(TGT, drop_years=(1991, 2004))
    check("SF14 the two estimated peaks dropped keep the call, the flows and the bands",
          {k_: v_ for k_, v_ in cells(p14, s14).items() if k_ != "top2"} == {k_: v_ for k_, v_ in GC.items() if k_ != "top2"})
    check("SF14b the estimated peaks are not among the creek's largest floods",
          not set(GC["top2"]) & set(pk.ESTIMATED))
    check("SF15 the SNOTEL pair's lapse keeps every cell", cells(V["lapse_snotel"]["par"], V["lapse_snotel"]["series"]) == GC,
          "%.2f" % R["lapse_snotel"])
    g_wy = _wy_gain(TGT)
    p16, _, s16 = carry(TGT, g=g_wy)
    check("SF16 the orographic gain from water-year station means keeps the call", span_of(F.quantile(p16, 0.01)) == 185,
          "g %.3f" % g_wy)
    check("SF17 the river's snowmelt peaks carry no rain (left out of the carry)", R["n_matched"] < R["n_floods"])
    gcsv = open(os.path.join(TASK, "golden", "durrow_creek_estimated_annual_peaks.csv")).read().strip().split("\n")
    check("SF18 the CSV holds 75 water years, the year without a rain flood marked less than",
          len(gcsv) == 76 and sum(1 for ln in gcsv[1:] if ",<," in ln) == len(fig["missing_years"]))
    T19, P19, z19 = _lcd_all_reports(TGT)
    p19, _, s19 = carry(TGT, lcd=(T19, P19, z19))
    check("SF19 the specials (FM-16) summed with the routine reports keep every cell", cells(p19, s19) == GC)
    for gap in (3, 12, 24):
        check("SF20 dry spells of %d hours keep every cell" % gap, cells(V["gap_%d" % gap]["par"], V["gap_%d" % gap]["series"]) == GC)
    check("SF22 the temperature at the river's peak hour is not the rain's: no rain in that hour in a third of the floods or "
          "more, and the air a median half a degree C or more colder", R["peak_hour"]["dry_share"] >= 1 / 3.0
          and R["peak_hour"]["median_diff"] <= -0.5, "%.2f dry, %.2f C" % (R["peak_hour"]["dry_share"], R["peak_hour"]["median_diff"]))
    tz = [r[2] for r in R["rows"]]
    PV, TV = estimates(TGT)["PV"], estimates(TGT)["TV"]
    dd = [TV[r[0]] - r[2] for r in R["rows"] if r[0] in TV]
    check("SF21 the valley's daily mean misses the rain's own temperature by more than 1 C (about 600 ft of snow line) in a "
          "sixth of the floods or more (why the hourly record decides)", np.mean(np.abs(dd) > 1.0) >= 1 / 6.0,
          "%.2f of %d floods" % (np.mean(np.abs(dd) > 1.0), len(dd)))

    zcb, arb, acb = A.bands(TGT)[:3]

    def share_of(tv, areas):
        tz = tv - R["lapse"] * (zcb - R["zv"]) / A.FT_PER_KM
        rain = 1 - 1 / (1 + np.exp((tz - R["t50"]) / R["k"]))
        return float((areas * rain).sum() / areas.sum())
    by_wy = {}
    for r in R["rows"]:
        wy = r[0].year + (1 if r[0].month >= 10 else 0)
        if wy not in by_wy or r[6] > by_wy[wy][6]:
            by_wy[wy] = r
    rec = [next(r for r in R["rows"] if r[0] == R["annual"][wy][0]) for wy in fig["river_top2"]]
    check("H3 the report's flood history holds: the river's record floods rained over more than half its basin, the "
          "creek's two largest left more than half of it under snow, and the creek drained whole in every flood",
          all(share_of(r[2], arb) > 0.5 for r in rec) and all(share_of(by_wy[wy][2], arb) < 0.5 for wy in fig["top2"])
          and all(share_of(r[2], acb) >= 0.95 for r in R["rows"]))

    # ------------------------------------------------------------------ back-test, literal reader, oracles
    check("B1 the drainage-area transfer validates among the region's gauged basins (median error under 5 per cent)",
          _backtest(TGT) < 0.05, "%.3f" % _backtest(TGT))
    check("L1 the literal reader: the river's floods follow its rain below the snow line, not its whole-basin rain",
          R["own_r"] > R["total_rain_r"] + 0.10, "r %.2f against %.2f" % (R["own_r"], R["total_rain_r"]))
    st = pdf_text(os.path.join(TGT, "wsdot_region3_flood_frequency_excerpt.pdf"))
    check("O1 positive control and no transfer formula in the state report",
          "Regional regression equations" in st and not re.search(r"ungaged sites near|drainage-area ratio|area ratio", st))
    check("O2 no document mentions snow, elevation bands or storms", all(
        not re.search(r"snow|freezing|storm", pdf_text(os.path.join(TGT, f)), re.I)
        for f in files if f.endswith(".pdf")))
    check("O3 the memorandum makes no flood estimate", "makes no" in tm and "estimate of flood frequency" in tm)

    # ------------------------------------------------------------------ distractors
    tmp = tempfile.mkdtemp(prefix="t3d-")
    try:
        for f in files:
            shutil.copy(os.path.join(TGT, f), tmp)
        for d in meta["distractors"]:
            os.remove(os.path.join(tmp, d))
        pd_, qd, sd = carry(tmp)
        check("D1 the golden is unchanged with every distractor deleted", all(abs(qd[a] - G[a]) < 0.5 for a in A.AEPS))
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------ realism sweep
    ids = ["12183450", "12187200", "12181650", "12189500", "12184900"]
    steps = np.diff(sorted(int(x) for x in ids))
    check("S1 no id column is an arithmetic sequence", len(set(steps)) > 1)
    for f in files:
        if f.endswith(".txt") and "annual_peaks" in f:
            vals = [float(r["peak_va"]) for r in A.read_rdb(os.path.join(TGT, f))]
            check("S2 %s holds no repeated block of five peaks" % f, not _repeat_block(vals))
    peaks = [float(r["peak_va"]) for r in A.read_rdb(os.path.join(TGT, "usgs_12183450_coyner_r_annual_peaks.txt"))]
    check("S3 the river's peaks are not round", sum(1 for p in peaks if p % 1000 == 0) <= 3)
    people = set(re.findall(r"(Amy Rasmussen|Frederick Hess)", std + tm))
    check("S4 personas are the drawn ones only", people <= {"Amy Rasmussen", "Frederick Hess"} and len(people) >= 1)
    check("S5 no document dated after the pull", all(dt.date.fromisoformat(v["date"]) <= dt.date(2026, 10, 14)
                                                     for v in meta["files"].values()))
    meta_txt = json.dumps(meta).lower()
    check("S6 metadata.json names no method or mechanism", not re.search(r"snow|lapse|freezing|contribut|elevation band", meta_txt))
    stamps = set()
    for f in files:
        if f.startswith("usgs_"):
            m = re.search(r"# Retrieved (.*)", open(os.path.join(TGT, f)).read())
            stamps.add(m.group(1) if m else None)
    check("S7 each USGS download carries its own retrieval clock", len(stamps) == sum(1 for f in files if f.startswith("usgs_")))
    lcd_types = {}
    with open(os.path.join(TGT, A.LCD_FILE)) as fh_:
        for row in csv.DictReader(fh_):
            lcd_types[row["REPORT_TYPE"]] = lcd_types.get(row["REPORT_TYPE"], 0) + 1
    check("S8 the hourly record carries specials beside its routine reports", lcd_types.get("FM-16", 0) > 1000
          and lcd_types.get("FM-15", 0) > 600000, str(lcd_types))

    bad = [r for r in RES if not r[1]]
    for label, ok, detail in RES:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    print("CHECKS %d of %d passed" % (len(RES) - len(bad), len(RES)))
    return 0 if not bad else 1


def _spliced_lapse(tgt):
    """The storm lapse with both Tessel stations read at the first station's elevation."""
    PV, TV, ZV = A.valley_daily(tgt)
    PR, TR = A.ridge_daily(tgt)
    Z1 = {d: 1180.0 for d in ZV}
    return A.storm_lapse(PV, TV, PR, TR, Z1)[0]


def _lcd_all_reports(tgt):
    """The hourly record with every report's rain summed into its hour (specials counted twice)."""
    T = np.full(A.NH, np.nan)
    P = np.full(A.NH, np.nan)
    z = None
    with open(os.path.join(tgt, A.LCD_FILE)) as f:
        for row in csv.DictReader(f):
            if z is None:
                z = float(row["ELEVATION"]) / 0.3048
            d = dt.datetime.fromisoformat(row["DATE"])
            i = int((d - A.T0).total_seconds() // 3600)
            if not 0 <= i < A.NH:
                continue
            t = row["HourlyDryBulbTemperature"].rstrip("s*").strip()
            if t and row["REPORT_TYPE"] == "FM-15":
                T[i] = (float(t) - 32.0) * 5.0 / 9.0
            p = row["HourlyPrecipitation"].rstrip("s*").strip()
            v = 0.001 if p == "T" else (float(p) if p else None)
            if v is not None:
                P[i] = (0.0 if np.isnan(P[i]) else P[i]) + v
    return T, P, z


def _mdpr_last(tgt):
    """The golden with multi-day totals put on their last day."""
    orig = A.valley_daily

    def last_day(t):
        P, T, Z = orig(t)
        rows = A.read_ghcn(os.path.join(t, "ghcnd_tessel_daily_1950-2025.csv"))
        for r in rows:
            md, da = A._num(r.get("MDPR")), A._num(r.get("DAPR"))
            if md is not None and da:
                d = dt.date.fromisoformat(r["DATE"])
                for k in range(int(da)):
                    P[d - dt.timedelta(days=k)] = 0.0
                P[d] = md
        return P, T, Z
    A.valley_daily = last_day
    try:
        EST.pop(tgt, None)
        p_, _, s_ = carry(tgt)
        return cells(p_, s_)
    finally:
        A.valley_daily = orig
        EST.pop(tgt, None)


def _wy_gain(tgt):
    PV, TV, ZV = A.valley_daily(tgt)
    PR, TR = A.ridge_daily(tgt)
    sh = A.snotel(tgt, "snotel_1187_hatchet_meadow_daily.csv")
    sc = A.snotel(tgt, "snotel_1203_corbel_ridge_daily.csv")
    zc, ar, ac, areas, area_c = A.bands(tgt)
    _, means = A.station_map(PV, PR, [(4160.0, sh), (5630.0, sc)], zc, ac)
    z = np.array(sorted(means)) - 1000.0
    p = np.array([means[k] for k in sorted(means)])
    sl, ic = np.polyfit(z, p, 1)
    return float(sl / ic * 1000.0)


def _backtest(tgt):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(tgt, "region3_basin_characteristics.xlsx"), data_only=True)
    pts = {}
    for row in wb["Gauged basins"].iter_rows(min_row=4, values_only=True):
        if not row or not row[0]:
            continue
        site = str(row[0])
        fn = "usgs_12183450_coyner_r_annual_peaks.txt" if site == "12183450" else "usgs_%s_annual_peaks.txt" % site
        qq = np.array([float(r["peak_va"]) for r in A.read_rdb(os.path.join(tgt, fn))])
        pts[site] = (float(row[2]), F.quantile(F.fit(qq), 0.01))
    errs = [abs(pts[a][1] * (pts[b][0] / pts[a][0]) ** A.STATE_B / pts[b][1] - 1) for a in pts for b in pts if a != b]
    return float(np.median(errs))


def _repeat_block(vals, n=5):
    seen = set()
    for i in range(len(vals) - n + 1):
        key = tuple(vals[i:i + n])
        if key in seen:
            return True
        seen.add(key)
    return False


if __name__ == "__main__":
    sys.exit(main())
