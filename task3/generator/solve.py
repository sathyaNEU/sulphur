"""task3 architecture 4: the solution, read from the cut pack alone. Every rung and rival is a variant of run() with
its options; the golden is run() with the defaults.

The golden: (1) each well's and the entry point's annual means from the laboratory results (nitrate as NO3 to
nitrate-N, duplicates and re-runs averaged); (2) the county network's matured conversions (pasture, dry cropland,
grass or forest put under irrigation 1987 to 2010) each step up after a delay, measured at the midpoint between the
site's level before and its level since 2019; the delay less the site's water-table age, regressed on the site's
depth to water, is the unsaturated travel time a + b x depth; (3) each class's leachate by land-surface year from the
network's steady sites, each sample dated back by its own age and unsaturated travel time; (4) each protection-area
parcel's water reaches its well after its unsaturated travel time and the wellhead model's groundwater time of
travel, mixed by acres times recharge; (5) each well's model carried to the observed level (its 2019-2026 mean
residual), the plan's shares from 2027, the first year the entry point's annual mean reaches 10 mg/L."""
import csv
import datetime as dt
import math
import os
from collections import defaultdict

import numpy as np
import openpyxl

import params as P

CODE_CLASS = {"F1": "FOR", "F2": "FOR", "141": "FOR", "142": "FOR", "G1": "GRS", "G2": "GRS", "176": "GRS",
              "37": "GRS", "A1": "DRY", "A2": "DRY", "24": "DRY", "36": "DRY", "A3": "IRC", "301": "IRC",
              "A4": "IRV", "304": "IRV", "U1": "RES", "121": "RES", "W": "WAT", "111": "WAT"}
DESC_CLASS = {"forest": "FOR", "grass and pasture": "GRS", "cropland, not irrigated": "DRY",
              "irrigated corn and soybean": "IRC", "irrigated vegetables": "IRV", "residential": "RES",
              "wetland": "WAT"}
F = {"results": "corlinden_raw_water_nitrate_results_1988-2026.csv",
     "pumping": "corlinden_well_pumping_daily_2009-2026.csv",
     "network": "ravell_county_groundwater_network_samples_1990-2026.csv",
     "sites": "ravell_county_groundwater_network_sites.xlsx",
     "landcover": "ravell_county_parcel_land_cover_1986-2026.csv",
     "attrs": "sallow_road_WHPA_parcel_attributes_2019.xlsx",
     "ages": "ravell_county_groundwater_age_survey_2019.xlsx"}
POINT = {"WELL 3": "W3", "WELL 5": "W5", "WELL 6": "W6", "WELL 7": "W7", "HR-W03": "W3", "HR-W05": "W5",
         "HR-W06": "W6", "HR-W07": "W7", "EP-01": "EP"}


def dec(s):
    d = dt.date.fromisoformat(s[:10])
    y0 = dt.date(d.year, 1, 1)
    return d.year + (d - y0).days / (dt.date(d.year + 1, 1, 1) - y0).days


def to_n(result, units, nd="half"):
    r = result.strip()
    cen = r.startswith("<")
    v = float(r.lstrip("<"))
    if cen:
        v = v / 2.0 if nd == "half" else (0.0 if nd == "zero" else v)
    if "NO3" in units:
        v /= P.NO3_PER_N
    return v


# ---------------------------------------------------------------- reading the pack
def read(target, nd="half"):
    D = {}
    rows = list(csv.DictReader(open(os.path.join(target, F["results"]), encoding="utf-8")))
    by = defaultdict(list)
    for r in rows:
        by[(POINT[r["sample_point"]], r["collected"])].append(to_n(r["result"], r["units"], nd))
    samp = defaultdict(list)
    for (w, d), v in by.items():
        samp[w].append((dec(d), float(np.mean(v))))
    D["well_samples"] = {w: sorted(v) for w, v in samp.items()}
    ann = {}
    for w, v in D["well_samples"].items():
        g = defaultdict(list)
        for t, x in v:
            g[int(t)].append(x)
        ann[w] = {y: float(np.mean(x)) for y, x in g.items()}
    D["well_annual"] = ann
    # network sites
    wb = openpyxl.load_workbook(os.path.join(target, F["sites"]), read_only=True)
    sites = {}
    alias = {}
    for r in list(wb["Sites"].iter_rows(values_only=True))[1:]:
        sid, pid, _, _, _, _, _, dtw, status, note = r
        if str(status).startswith("abandoned"):
            alias[sid] = str(note).replace("replaced by ", "").strip()
            continue
        sites[sid] = dict(pid=pid, dtw=float(dtw))
    D["sites"] = sites
    # ages
    wb = openpyxl.load_workbook(os.path.join(target, F["ages"]), read_only=True)
    ages = {}
    for r in list(wb["Results"].iter_rows(values_only=True))[1:]:
        if str(r[5]).startswith("water-table"):
            ages[r[0]] = float(r[4])
    D["ages"] = ages
    # network samples
    ns = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(target, F["network"]), encoding="utf-8")):
        sid = alias.get(r["site_id"], r["site_id"])
        ns[sid].setdefault(r["sample_date"], []).append(to_n(r["nitrate_result"], r["units"], nd))
    D["net"] = {s: sorted((dec(d), float(np.mean(v))) for d, v in x.items()) for s, x in ns.items()}
    # land cover
    lc = defaultdict(dict)
    parent = {}
    for r in csv.DictReader(open(os.path.join(target, F["landcover"]), encoding="utf-8")):
        lc[r["parcel_id"]][int(r["year"])] = CODE_CLASS[r["land_cover_code"]]
        if r["parent_parcel_id"]:
            parent[r["parcel_id"]] = r["parent_parcel_id"]
    for child, par in parent.items():
        for y, c in lc.get(par, {}).items():
            lc[child].setdefault(y, c)
    D["lc"] = dict(lc)
    # protection area parcels
    wb = openpyxl.load_workbook(os.path.join(target, F["attrs"]), read_only=True)
    parcels = []
    for r in list(wb["Parcels"].iter_rows(values_only=True))[1:]:
        pid, ac, zone, dtw, T, lc18, owner = r
        parcels.append(dict(pid=pid, acres=float(ac), zone="W" + str(zone).split()[-1], dtw=float(dtw), T=float(T)))
    D["parcels"] = parcels
    rech = {}
    for r in list(wb["Recharge"].iter_rows(values_only=True))[1:]:
        rech[DESC_CLASS[r[0]]] = float(r[1])
    rech["WAT"] = 0.0
    D["recharge"] = rech
    return D


def lc_at(D, pid, y):
    h = D["lc"][pid]
    y = int(min(max(y, 1986), 2026))
    return h[y]


# ---------------------------------------------------------------- the unsaturated delay
def cohort(D, lo=1987, hi=2010):
    out = []
    for sid, s in D["sites"].items():
        h = D["lc"][s["pid"]]
        ch = [y for y in range(1987, 2027) if h[y] != h[y - 1]]
        if len(ch) != 1:
            continue
        c = ch[0]
        if not (lo <= c <= hi and h[c - 1] in ("FOR", "GRS", "DRY") and h[c] in P.IRRIGATED):
            continue
        out.append(dict(sid=sid, c=c, dtw=s["dtw"], series=D["net"][sid]))
    return out


def arrival(series, c, post_from=2019.0, rule="mid"):
    pre = [x for t, x in series if c - 3 <= t < c + 1.0]
    post = [x for t, x in series if t >= post_from]
    if not pre or not post:
        return None
    lo, hi = float(np.mean(pre)), float(np.mean(post))
    if rule == "step":
        pts = [(t, x) for t, x in series if c - 3 <= t]
        best = None
        for k in range(1, len(pts)):
            a1 = float(np.mean([x for _, x in pts[:k]]))
            a2 = float(np.mean([x for _, x in pts[k:]]))
            e = sum((x - a1) ** 2 for _, x in pts[:k]) + sum((x - a2) ** 2 for _, x in pts[k:])
            if best is None or e < best[0]:
                best = (e, 0.5 * (pts[k - 1][0] + pts[k][0]))
        return best[1]
    lvl = lo + (hi - lo) * (0.5 if rule == "mid" else (0.25 if rule == "quarter" else 0.75))
    prev = None
    for t, x in series:
        if t < c:
            prev = (t, x)
            continue
        if x >= lvl and prev is not None and prev[1] < lvl:
            t0, x0 = prev
            return t0 + (lvl - x0) / (x - x0) * (t - t0)
        prev = (t, x)
    return None


def delay_fit(D, opts):
    co = cohort(D)
    X, Yv = [], []
    for s in co:
        t = arrival(s["series"], s["c"], rule=opts.get("rule", "mid"))
        if t is None:
            continue
        age = D["ages"].get(s["sid"], opts.get("default_age", float(np.mean(list(D["ages"].values())))))
        if opts.get("age", True) is False:
            age = 0.0
        X.append(s["dtw"])
        Yv.append(t - s["c"] - age)
    X, Yv = np.array(X), np.array(Yv)
    if opts.get("delay") == "pooled":
        return dict(a=float(np.mean(Yv)), b=0.0, n=len(X), X=X, Y=Yv)
    if opts.get("delay") == "origin":
        b = float(np.sum(X * Yv) / np.sum(X * X))
        return dict(a=0.0, b=b, n=len(X), X=X, Y=Yv)
    b, a = np.polyfit(X, Yv, 1)
    res = Yv - (a + b * X)
    return dict(a=float(a), b=float(b), n=len(X), X=X, Y=Yv, rmse=float(np.sqrt(np.mean(res ** 2))))


# ---------------------------------------------------------------- leachate by class and land-surface year
def class_curves(D, fit, opts):
    bins = defaultdict(lambda: defaultdict(list))
    for sid, s in D["sites"].items():
        h = D["lc"][s["pid"]]
        if len(set(h[y] for y in range(1986, 2027))) != 1:
            continue
        c = h[2026]
        age = D["ages"].get(sid, float(np.mean(list(D["ages"].values()))))
        lag = age + fit["a"] + fit["b"] * s["dtw"]
        if opts.get("curve_lag") == "none":
            lag = 0.0
        for t, x in D["net"][sid]:
            bins[c][int(math.floor(t - lag))].append(x)
    curves = {}
    for c, b in bins.items():
        ys = sorted(b)
        raw = {y: float(np.mean(b[y])) for y in ys}
        sm = {}
        k = opts.get("smooth", 1)
        for y in ys:
            v = [raw[z] for z in range(y - k, y + k + 1) if z in raw]
            sm[y] = float(np.mean(v))
        tail = opts.get("tail", 5)
        last = float(np.mean([raw[y] for y in ys])) if tail == "all" else float(np.mean([sm[y] for y in ys[-tail:]]))
        curves[c] = dict(years=ys, val=sm, first=sm[ys[0]], last=last)
    if opts.get("leach_from") == "cohort":
        for c in P.IRRIGATED:
            vals = []
            for s in cohort(D):
                if D["lc"][D["sites"][s["sid"]]["pid"]][2026] != c:
                    continue
                t = arrival(s["series"], s["c"])
                vals += [x for tt, x in s["series"] if t is not None and tt >= t + 1.0]
            lvl = float(np.mean(vals))
            curves[c] = dict(years=[2100], val={}, first=lvl, last=lvl, flat=True)
    return curves


def L(curves, c, s):
    if c == "WAT":
        return 0.0
    cv = curves[c]
    if cv.get("flat"):
        return cv["last"]
    y = int(math.floor(s))
    if y in cv["val"]:
        return cv["val"][y]
    if y < cv["years"][0]:
        return cv["first"]
    if y > cv["years"][-1]:
        return cv["last"]
    near = min(cv["years"], key=lambda z: abs(z - y))
    return cv["val"][near]


# ---------------------------------------------------------------- the well field
_RC = {}


def recent_clearings(D):
    """protection-area parcels whose land cover turned to an irrigated class after 2012"""
    key = id(D)
    if key not in _RC:
        out = set()
        for p in D["parcels"]:
            h = D["lc"][p["pid"]]
            if any(h[y] in P.IRRIGATED and h[y - 1] not in P.IRRIGATED for y in range(2013, 2027)):
                out.add(p["pid"])
        _RC[key] = out
    return _RC[key]


def fit_k(target, D, **opts):
    """the clearing's effect fitted to the wells' 2019-2026 record (Wells 6 and 7, the model unanchored)"""
    best = None
    for k in np.arange(0.0, 1.501, 0.05):
        r = run(target, D=D, k=float(k), anchor=False, **opts)
        e = sum((r["obs"][w][y] - r["model"][w][y]) ** 2 for w in ("W6", "W7") for y in range(2019, 2027))
        if best is None or e < best[0]:
            best = (e, float(k))
    return best[1]

def model_well(D, fit, curves, w, y, opts):
    num = den = 0.0
    for p in D["parcels"]:
        if p["zone"] != w:
            continue
        acc = 0.0
        wsum = 0.0
        for f in (0.125, 0.375, 0.625, 0.875):
            t = y + f
            T = 0.0 if opts.get("sat") == "none" else p["T"]
            if opts.get("delay") == "lag":
                s = t - opts["lag"]
            elif opts.get("delay") == "none":
                s = t - T
            else:
                s = t - T - (fit["a"] + fit["b"] * p["dtw"])
            c = lc_at(D, p["pid"], math.floor(s))
            # the water a parcel sends at t left the water table at t - T, at the recharge the parcel then had
            cq = lc_at(D, p["pid"], math.floor(t - T)) if opts.get("weight", "current") == "current" else c
            q = D["recharge"][cq] if opts.get("flux", True) else (0.0 if cq == "WAT" else 1.0)
            x = p["acres"] * q
            v = L(curves, c, s)
            if "k" in opts and c in P.IRRIGATED and p["pid"] in recent_clearings(D):
                v = L(curves, "FOR", s) + opts["k"] * (v - L(curves, "FOR", s))
            acc += x * v
            wsum += x
        num += acc
        den += wsum
    return num / den if den else 0.0


def run(target, D=None, **opts):
    D = D or read(target, opts.get("nd", "half"))
    fit = delay_fit(D, opts)
    if "b_override" in opts:
        fit = dict(fit, b=opts["b_override"])
    curves = class_curves(D, fit, opts)
    years = list(range(1992, 2041))
    model = {w: {y: model_well(D, fit, curves, w, y, opts) for y in years} for w in P.WELLS}
    obs = D["well_annual"]
    resid = {}
    for w in P.WELLS:
        r = [obs[w][y] - model[w][y] for y in range(2019, 2027) if y in obs[w]]
        resid[w] = float(np.mean(r))
    anchor = opts.get("anchor", True)
    fc = {w: {y: model[w][y] + (resid[w] if anchor else 0.0) for y in years} for w in P.WELLS}
    share = opts.get("share", P.PLAN_SHARE)
    ep = {y: sum(share[w] * fc[w][y] for w in P.WELLS) / sum(share.values()) for y in P.FC_YEARS}
    cross = next((y for y in P.FC_YEARS if ep[y] >= P.LIMIT), None)
    rmse = {w: float(np.sqrt(np.mean([(obs[w][y] - fc[w][y]) ** 2 for y in range(1998, 2027) if y in obs[w]])))
            for w in P.WELLS}
    call = 2027 if (cross is not None and cross < P.CYCLES[2031]) else 2031
    return dict(fit={k: v for k, v in fit.items() if k not in ("X", "Y")}, fitXY=(list(map(float, fit["X"])),
                list(map(float, fit["Y"]))), curves={c: {"last": v["last"]} for c, v in curves.items()},
                model=model, fc=fc, ep=ep, cross=cross, call=call, resid=resid, rmse=rmse, obs=obs, D=D,
                curves_full=curves)
