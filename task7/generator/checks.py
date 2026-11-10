"""task7 architecture 8: the generator's assertions, run on the cut pack (verify.load) against the world's clean truth.
Every result of the design note's results chain (R1 to R10) is computed here with its rivals (the band) and with the
careful but hurried pass and the quick pass (effort.json); every row of the semantic fork table (SF1 to SF20) is
asserted, and the bar block (dataset-generation 7.1, labelled "bar" below); the figures the deliverables and the answer
blocks print are made here."""
import copy
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as GD  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

RESULTS = []
MEAS = GD.MEASURES
FUNDED = ("insulation", "heating controls")
B_BOOT = 500
EMPTY_AT = (0.50, 0.60, 0.70)              # the shares of the week empty R3 is read at
ROOF_AT = (1.0, 0.5, 0.25)                 # the square metres of roof per square metre of floor R4 is read at
CM, IM, HM = "heating controls", "insulation", "heating optimisation"


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def rnd(v, u):
    """half up, as an analyst rounds"""
    return math.floor(v / u + 0.5) * u


def pct(x):
    return round(100.0 * x, 2)


def appr(P, m, **kw):
    return GD.appraisal(P, m, GD.app_rates(P, m, **kw))


def fset(R):
    return tuple(m for m in MEAS if R[m]["eur_t"] <= GD.LIMIT)


def at_empty(fit):
    return {e: float(GD.dose_at(fit, e)[0]) for e in EMPTY_AT}


def at_roof(fit):
    return {r: float(GD.dose_at(fit, math.log(r))[0]) for r in ROOF_AT}


def wsse(fit, pts):
    px, py, pw = (np.array(v) for v in zip(*pts))
    return float((pw * (GD.dose_at(fit, px) - py) ** 2).sum() / pw.sum())


def drivers(P, empty=None, roof=None):
    """the gas-weighted mean driver of each driven measure's pilot works buildings, and the reference-weighted mean of
    this year's applications for it"""
    k0 = P.si[GD.PILOT]
    out = {}
    for m, x in ((CM, P.empty if empty is None else empty), (IM, P.roof_ratio if roof is None else roof)):
        g, _ = GD._arms(P, m)
        g = g[np.isfinite(x[g]) & np.isfinite(P.U[g, k0])]
        A = GD.apps(P, m)
        xa = np.array([x[a["b"]] for a in A])
        wa = np.array([a["ref_kwh"] for a in A])
        out[m] = {"pilot": float(np.average(x[g], weights=P.U[g, k0])), "2026": float(np.average(xa, weights=wa))}
    return out


# ---------------------------------------------------------------- each result, golden, rivals and hurried

def results(P, quick=False):
    C = {}
    # R1 the saving by season against the passed-over owners, as a share of the gas the works buildings would have used
    C["R1"] = {m: GD.season_savings(P, m) for m in MEAS}
    C["R1_rivals"] = {
        "two-season baseline": {m: GD.season_savings(P, m, base="two") for m in MEAS},
        "comparison by use type": {m: post_stratified(P, m) for m in MEAS}}
    C["R1_hurried"] = {"works buildings' own before and after": {m: GD.before_after(P, m) for m in MEAS},
                       "average of the buildings' shares": {m: GD.season_savings(P, m, "mean_log") for m in MEAS}}
    # R2 each measure's saving over its service life, the pilot's buildings (graded on heating optimisation)
    C["R2"] = {m: GD.lifetime(C["R1"][m], m, "floor") for m in MEAS}
    C["R2_fit"] = {m: GD._fit_floor(C["R1"][m]) for m in MEAS}
    C["R2_zero_fit"] = {m: GD._fit_zero(C["R1"][m]) for m in MEAS}
    C["R2_rivals"] = {h: {m: GD.lifetime(C["R1"][m], m, h) for m in MEAS} for h in ("last", "last3")}
    C["R2_rivals"]["two-season baseline"] = {m: GD.lifetime(C["R1_rivals"]["two-season baseline"][m], m) for m in MEAS}
    C["R2_hurried"] = {h: {m: GD.lifetime(C["R1"][m], m, h) for m in MEAS} for h in ("flat", "first")}
    # R3 controls along the empty week; R4 insulation along the roof per floor (on the heating part)
    C["R3_pts"] = GD.dose_points(P, CM)
    C["R3_n"] = [(len(a), len(b)) for a, b in GD.dose_groups(P, CM)]
    C["R3_fit"] = GD.dose_fit(C["R3_pts"], CM)
    C["R3"] = at_empty(C["R3_fit"])
    ev = {"the empty week at 40 per cent of the load's range": V.empty_weeks(P, 0.4)[0],
          "the empty week at 60 per cent of the load's range": V.empty_weeks(P, 0.6)[0]}
    for mg in (0.0, 0.03, 0.08, 0.15):
        ev["hotels and care homes lived in where their weekend days run %d per cent above their nights" % round(100 * mg)] = \
            V.empty_weeks(P, 0.5, "weekend", mg)[0]
    C["e_strict"] = V.empty_weeks(P, 0.5, "strict")[0]
    C["e_variants"] = ev
    C["e_none"] = V.empty_weeks(P, 0.5, "none")[0]
    r3 = {"four bands": GD.dose_fit(GD.dose_points(P, CM, 4), CM),
          "eight bands": GD.dose_fit(GD.dose_points(P, CM, 8), CM),
          "a straight line through the bands of buildings that close": GD.dose_fit(C["R3_pts"], CM, "linear")}
    for name, e in ev.items():
        r3[name] = GD.dose_fit(GD.dose_points(P, CM, x=e), CM)
    C["R3_rival_fits"] = r3
    C["R3_rivals"] = {k: at_empty(f) for k, f in r3.items()}
    r3["hotels and care homes lived in only where every weekend day hour runs above every night hour"] = \
        GD.dose_fit(GD.dose_points(P, CM, x=C["e_strict"]), CM)
    C["R3_rivals"] = {k: at_empty(f) for k, f in r3.items()}
    C["R3_hurried_fits"] = {
        "a straight line through the lived-in band too": GD.dose_fit(C["R3_pts"], CM, "linear_all"),
        "the empty week read off the load alone": GD.dose_fit(GD.dose_points(P, CM, x=C["e_none"]), CM)}
    C["R3_hurried"] = {k: at_empty(f) for k, f in C["R3_hurried_fits"].items()}
    C["R3_hurried"]["one saving for every building"] = {e: float(C["R1"][CM].mean()) for e in EMPTY_AT}
    C["R4_pts"] = GD.dose_points(P, IM)
    C["R4_n"] = [(len(a), len(b)) for a, b in GD.dose_groups(P, IM)]
    C["R4_fit"] = GD.dose_fit(C["R4_pts"], IM)
    C["R4"] = at_roof(C["R4_fit"])
    C["R4_rivals"] = {"four bands": at_roof(GD.dose_fit(GD.dose_points(P, IM, 4), IM)),
                      "eight bands": at_roof(GD.dose_fit(GD.dose_points(P, IM, 8), IM)),
                      "the bands as steps": at_roof(GD.dose_fit(C["R4_pts"], IM, "bins"))}
    k0 = P.si[GD.PILOT]
    g, _ = GD._arms(P, IM)
    gg = g[np.isfinite(P.U[g, k0])]
    hw_pool = float(np.average(P.hvec[gg], weights=P.U[gg, k0]))
    C["R4_hurried"] = {"one saving for every building": {r: float(C["R1"][IM].mean() / (1 - hw_pool)) for r in ROOF_AT}}
    C["drivers"] = drivers(P)
    # R5 each measure's saving rate on this year's applications over its life; R6 grant per tonne and the call
    A = {m: appr(P, m) for m in MEAS}
    C["A"] = A
    C["R5"] = {m: A[m]["rate"] for m in MEAS}
    C["R6"] = {m: A[m]["eur_t"] for m in MEAS}
    C["funded"] = fset(A)
    riv = {"four bands of each driver": {"nb": 4}, "eight bands of each driver": {"nb": 8},
           "each driver's bands as steps": {"form": "bins"},
           "a straight line through the bands of buildings that close": {"form": "linear"},
           "insulation on its share of the gas": {"heat_part": False},
           "two-season baseline": {"base": "two"}, "the last season carried": {"persist": "last"},
           "the last three seasons carried": {"persist": "last3"}}
    for name, e in ev.items():
        riv[name] = {"empty": e}
    riv["hotels and care homes lived in only where every weekend day hour runs above every night hour"] = \
        {"empty": C["e_strict"]}
    C["R56_rivals"] = {name: {m: appr(P, m, **kw) for m in MEAS} for name, kw in riv.items()}
    hur = {"each use's saving, faded": {"route": "use"}, "the pilot's own mix, faded": {"route": "pooled"},
           "the pilot's seven-season average": {"route": "pooled_flat"},
           "each use's seven-season average": {"route": "type_flat"},
           "controls on a straight line through the lived-in band": {"form": "linear_all"},
           "the empty week read off the load alone": {"empty": C["e_none"]}}
    C["R56_hurried"] = {name: {m: appr(P, m, **kw) for m in MEAS} for name, kw in hur.items()}
    C["R56_hurried"]["the works buildings' own before and after"] = {
        m: GD.appraisal(P, m, np.full(len(GD.apps(P, m)), C["R1_hurried"]["works buildings' own before and after"][m].mean()))
        for m in MEAS}
    use = C["R56_hurried"]["each use's saving, faded"]
    C["R56_hurried"]["controls on its empty week, insulation by use"] = {IM: use[IM], HM: A[HM], CM: A[CM]}
    C["R56_hurried"]["insulation on its roof, controls by use"] = {IM: A[IM], HM: A[HM], CM: use[CM]}
    # R7 each grant per tonne's 90 per cent range and the saving rate at which its call flips
    C["R7"] = {}
    for m in MEAS:
        lo, hi, vals = GD.bootstrap(P, m, B=B_BOOT)
        C["R7"][m] = {"lo": lo, "hi": hi, "break_even": A[m]["break_even_rate"],
                      "share_under_limit": float((vals <= GD.LIMIT).mean())}
    C["R7_careful"] = {m: GD.bootstrap(P, m, B=B_BOOT, route="use")[:2] for m in GD.DRIVEN}
    C["R7_rival_seed"] = {m: GD.bootstrap(P, m, B=B_BOOT, seed=7)[:2] for m in MEAS} if not quick else {}
    # R8 the round once the offer closes
    C["R8"] = {m: GD.at_close(P, m) for m in MEAS}
    C["R8_rivals"] = {h: {m: GD.at_close(P, m, h) for m in MEAS} for h in ("one withdrawal rate",)}
    C["R8_hurried"] = {h: {m: GD.at_close(P, m, h) for m in MEAS} for h in ("count", "pooled", "no withdrawals",
                                                                            "received")}
    C["R8_funded_paid"] = sum(C["R8"][m]["paid"] for m in C["funded"])
    C["R8_funded_close"] = sum(C["R8"][m]["grant_close"] for m in C["funded"])
    # R9 every application received, its grant and lifetime tonnes
    C["apps"] = []
    for m in MEAS:
        rates = GD.app_rates(P, m)
        for a, r, t in zip(GD.apps(P, m), rates, A[m]["app_tonnes"]):
            C["apps"].append(dict(a, rate=float(r), life_t=float(t), funded=m in C["funded"], bid=P.bid[a["b"]],
                                  use=GD.TYPES[a["typ"]], empty=float(P.empty[a["b"]]),
                                  roof=float(P.roof_ratio[a["b"]])))
    C["apps"].sort(key=lambda x: x["no"])
    # R10 the CO2 the pilot's works saved in 2025/26
    C["R10"] = GD.season_saving_2026(P)
    C["R10_rivals"] = {"each use type's own 2025/26 saving": GD.season_saving_2026(P, "by type")}
    C["R10_hurried"] = {h: GD.season_saving_2026(P, h) for h in ("on the use with the works", "average on the 2018/19 use",
                                                                 "2025/26 rate on the 2018/19 use", "before and after")}
    return C


def post_stratified(P, m):
    """the comparison's change taken use type by use type, each type's works buildings set against its own passed-over
    owners, then summed back over the measure's works buildings (a rival for R1)"""
    k0 = P.si[GD.PILOT]
    out = []
    for k in range(k0 + 1, len(P.seasons)):
        num = den = 0.0
        for t in GD.TYPES:
            g, c = GD._arms(P, m, typ=t)
            g = g[np.isfinite(P.U[g, k0]) & np.isfinite(P.U[g, k])]
            c = c[np.isfinite(P.U[c, k0]) & np.isfinite(P.U[c, k])]
            if len(g) == 0:
                continue
            if len(c) < 3:
                g2, c2 = GD._arms(P, m)
                c = c2[np.isfinite(P.U[c2, k0]) & np.isfinite(P.U[c2, k])]
            ch = P.U[c, k].sum() / P.U[c, k0].sum()
            num += P.U[g, k].sum()
            den += P.U[g, k0].sum() * ch
        out.append(1.0 - num / den)
    return np.array(out)


def wald_seasons(P, m):
    """the draw's effect on each season (every drawn owner against the passed-over), as the ratio of totals, scaled by
    the share of the drawn owners' 2018/19 gas in buildings that had the works (a rival for R1)"""
    k0 = P.si[GD.PILOT]
    sel = P.measure == m
    dr = np.where(P.drawn & sel)[0]
    c = np.where(P.answered & ~P.drawn & sel)[0]
    out = []
    for k in range(k0 + 1, len(P.seasons)):
        dd = dr[np.isfinite(P.U[dr, k0]) & np.isfinite(P.U[dr, k])]
        cc = c[np.isfinite(P.U[c, k0]) & np.isfinite(P.U[c, k])]
        itt = 1.0 - (P.U[dd, k].sum() / P.U[dd, k0].sum()) / (P.U[cc, k].sum() / P.U[cc, k0].sum())
        comp = P.U[dd[P.works[dd]], k0].sum() / P.U[dd, k0].sum()
        out.append(itt / comp)
    return np.array(out)


def apps_route(P, C, route):
    """a route's lifetime tonnes for every application received, and its funded set"""
    R = C["R56_hurried"][route] if route in C["R56_hurried"] else C["R56_rivals"][route]
    rows = {}
    for m in MEAS:
        for a, t in zip(GD.apps(P, m), R[m]["app_tonnes"]):
            rows[a["no"]] = float(t)
    return fset(R), rows


# ---------------------------------------------------------------- the assertions

def run(target, gen_dir, quick=False):
    w = W.build()
    P = V.load(target)
    C = results(P, quick)
    C["P"] = P
    S = P.seasons
    k0 = P.si[GD.PILOT]
    # ---- Layer 1: the pack rebuilds the world's normal-weather use, its weeks and its roofs
    import pack as PK
    Pk = PK.assemble(w)
    order = np.argsort(Pk.bid)
    h = np.array([W.HW_SHARE[W.TYPES[t]] for t in w.typ])
    TU = np.full((w.N, W.K), np.nan)
    for k, s in enumerate(W.SEASONS):
        live = (w.first <= s) & (w.last >= s)
        TU[:, k] = np.where(live, w.actual[:, k] * (h + (1 - h) * w.G_LT / w.G[s]), np.nan)
    TU = TU[order]
    ratio = P.U / TU
    ok = np.isfinite(ratio)
    err = np.abs(ratio[ok] - 1)
    check("L1 every building-season rebuilds from the reads: 99.9 per cent within 1.5 per cent, none past 6",
          (np.isfinite(P.U) == np.isfinite(TU)).all() and np.percentile(err, 99.9) < 0.015 and err.max() < 0.06,
          "99.9th %.4f, worst %.4f, median %.5f" % (np.percentile(err, 99.9), err.max(), float(np.median(ratio[ok]))))
    check("L1 the service visits read off the meter file are the world's", (P.tune_season == np.array(
        [W.season_of(d) if d is not None else 0 for d in w.tune_date])[order]).all())
    check("L1 the pilot's works buildings read off the response file are the world's",
          (P.works == w.works[order]).all() and (P.drawn == w.drawn[order]).all())
    true_empty = w.empty[order]
    true_lived = w.lived_in[order]
    closing = np.isfinite(P.empty) & ~P.lived_in
    e_err = np.abs(P.empty[closing] - true_empty[closing])
    has = np.isfinite(P.empty)
    caught = (P.lived_in[true_lived & has]).mean()
    extra = int((P.lived_in & ~true_lived & has).sum())
    C["lived_extra"] = extra
    check("L1 the empty week read off the 2025 profiles is the building's own: within 0.05 for 95 per cent of the "
          "buildings that close; every building the world lives in round the clock is held lived in (the conference "
          "houses and day-care centres among the hotels and care homes held with them)",
          np.percentile(e_err, 95) <= 0.05 and caught == 1.0,
          "95th %.3f, lived in caught %.4f, %d conference houses and day-care centres held lived in" % (
              np.percentile(e_err, 95), caught, extra))
    rr = P.roof_ratio
    rr_ok = np.isfinite(rr)
    rr_true = w.roof_ratio[order]
    r_err = np.abs(np.log(rr[rr_ok] / rr_true[rr_ok]))
    check("L1 the roof per floor from the cadastre and the register is the building's own: within 10 per cent for 90 "
          "per cent of buildings (garages and sheds on some addresses)", np.percentile(r_err, 90) <= 0.10,
          "90th %.3f" % np.percentile(r_err, 90))
    need = np.where(P.answered)[0].tolist() + [a["b"] for a in P.pipe]
    check("L1 every pilot answer and every 2026 application has a 2025 profile and a roof in the cadastre",
          all(np.isfinite(P.empty[b]) and np.isfinite(P.roof_ratio[b]) for b in need), "%d buildings" % len(need))
    # ---- R1 the saving by season: every rival inside the band, the hurried routes outside it
    band1 = 1.00 / 100.0
    for name, R in C["R1_rivals"].items():
        for m in MEAS:
            d = np.abs(R[m] - C["R1"][m]).max()
            check("SF5 R1 %s: %s within a point of the golden in every season" % (name, m), d <= band1,
                  "worst %.2f points" % (100 * d))
    ba = C["R1_hurried"]["works buildings' own before and after"]
    check("bar R3 R1 the before and after sits 3 points or more off the golden in every season and measure",
          all(np.abs(ba[m] - C["R1"][m]).min() >= 0.03 for m in MEAS),
          str({m: round(100 * np.abs(ba[m] - C["R1"][m]).min(), 1) for m in MEAS}))
    eq = C["R1_hurried"]["average of the buildings' shares"]
    dif = max(np.abs(eq[m] - C["R1"][m]).mean() for m in MEAS)
    check("SF1 SF2 the average of the buildings' shares is another quantity (the plan's share of the gas): half a point "
          "off on some measure", dif > 0.005, "%.2f points" % (100 * dif))
    # ---- R2 each measure's saving over its life
    band2 = {"insulation": 0.004, "heating optimisation": 0.0025, "heating controls": 0.0025}
    C["R2_band"] = band2
    for name, R in C["R2_rivals"].items():
        for m in MEAS:
            check("SF6 R2 %s: %s within its band of the golden" % (name, m), abs(R[m] - C["R2"][m]) <= band2[m],
                  "%.2f against %.2f" % (100 * R[m], 100 * C["R2"][m]))
    for name in ("flat", "first"):
        v = C["R2_hurried"][name][HM]
        check("bar R3 R2 heating optimisation's life saving, %s: outside the band by its own width or more" % name,
              abs(v - C["R2"][HM]) >= 2 * band2[HM], "%.2f against %.2f" % (100 * v, 100 * C["R2"][HM]))
    s = C["R1"][HM]
    f, d, tau, sse = C["R2_fit"][HM]
    s1z, tauz, ssez = C["R2_zero_fit"][HM]
    C["R2_fit_note"] = {"floor": f, "tau": tau, "sse": sse, "zero_sse": ssez,
                        "zero_life": GD.lifetime(s, HM, "zero")}
    check("SF6 an exponential fall to nothing fits heating optimisation's seasons worse than the approach to a floor",
          ssez > 1.5 * sse, "%.3g against %.3g" % (ssez, sse))
    lin = np.polyfit(np.arange(1, 8), s, 1)
    C["R2_fit_note"]["linear_zero_age"] = float(-lin[1] / lin[0]) if lin[0] < 0 else None
    check("SF6 a straight line through heating optimisation's seasons reaches nothing before its fifteenth season",
          lin[0] < 0 and -lin[1] / lin[0] < 15, "age %.1f" % (-lin[1] / lin[0]))
    ins = C["R1"][IM]
    check("insulation's saving holds over the seasons (no season after the first more than a point off their mean)",
          np.abs(ins[1:] - ins[1:].mean()).max() < 0.01, str([pct(x) for x in ins]))
    check("heating optimisation's saving falls to under a fifth of its first season's by the fourth",
          s[3] < 0.2 * s[0], "%.1f against %.1f" % (100 * s[3], 100 * s[0]))
    # ---- R3 controls along the empty week
    fit3 = C["R3_fit"]
    band3 = 0.012
    C["R3_band"] = band3
    for name, R in C["R3_rivals"].items():
        d = max(abs(R[e] - C["R3"][e]) for e in EMPTY_AT)
        check("SF16 SF17 SF18 R3 %s: controls' saving at half, three fifths and seven tenths of the week empty within 1.2 "
              "points" % name, d <= band3, "worst %.2f points" % (100 * d))
    for name, R in C["R3_hurried"].items():
        d = max(abs(R[e] - C["R3"][e]) for e in EMPTY_AT)
        check("bar R3 R3 %s: controls' saving off the golden by 2 points or more at one of half, three fifths and "
              "seven tenths of the week empty" % name, d >= 0.02,
              "%s against %s" % ([pct(R[e]) for e in EMPTY_AT], [pct(C["R3"][e]) for e in EMPTY_AT]))
    check("controls save nothing until about two fifths of the week is empty (the threshold 0.30 to 0.50), and the "
          "buildings lived in round the clock under 2 per cent", 0.30 <= fit3["e0"] <= 0.50 and fit3["lived"] < 0.02,
          "threshold %.3f, lived in %.2f" % (fit3["e0"], 100 * fit3["lived"]))
    lin_all = C["R3_hurried_fits"]["a straight line through the lived-in band too"]
    w_h, w_l = wsse(fit3, C["R3_pts"]), wsse(lin_all, C["R3_pts"])
    C["R3_misfit"] = {"hinge": w_h, "line through the lived-in band": w_l}
    check("SF18 a straight line through the lived-in band fits the bands twice as badly as the threshold and rise",
          w_l >= 2.0 * w_h, "%.3g against %.3g" % (w_l, w_h))
    dr = C["drivers"]
    check("this year's controls applications stand empty for more of the week than the pilot's controls works "
          "buildings, by 0.15 or more", dr[CM]["2026"] - dr[CM]["pilot"] >= 0.15,
          "%.3f against %.3f" % (dr[CM]["2026"], dr[CM]["pilot"]))
    # the factor runs across the stock: within each use whose buildings close, the emptier half saves more
    within = {}
    for t in ("office", "retail", "workshop"):
        gt, ct = GD._arms(P, CM, typ=t)
        med = np.nanmedian(np.concatenate([P.empty[gt], P.empty[ct]]))
        hi_ = GD.season_savings(P, CM, rows=(gt[P.empty[gt] > med], ct[P.empty[ct] > med])).mean()
        lo_ = GD.season_savings(P, CM, rows=(gt[P.empty[gt] <= med], ct[P.empty[ct] <= med])).mean()
        within[t] = (hi_, lo_)
    C["R3_within_use"] = within
    check("bar R5 the empty week moves controls' saving inside every use whose buildings close (the emptier half saves "
          "more in offices, shops and workshops)", all(a_ > b_ for a_, b_ in within.values()),
          str({t: (pct(a_), pct(b_)) for t, (a_, b_) in within.items()}))
    # ---- R4 insulation along the roof per floor
    band4 = 0.030
    C["R4_band"] = band4
    for name, R in C["R4_rivals"].items():
        d = max(abs(R[r] - C["R4"][r]) for r in ROOF_AT)
        check("SF18 R4 %s: insulation's heating saving at one, a half and a quarter square metre of roof per floor "
              "within 3 points" % name, d <= band4, "worst %.2f points" % (100 * d))
    for name, R in C["R4_hurried"].items():
        d = min(abs(R[1.0] - C["R4"][1.0]), abs(R[0.25] - C["R4"][0.25]))
        check("bar R3 R4 %s: insulation's heating saving 4 points or more off the golden at a full roof and at a quarter"
              % name, d >= 0.04, "%.2f / %.2f against %.2f / %.2f" % (100 * R[1.0], 100 * R[0.25], 100 * C["R4"][1.0],
                                                                       100 * C["R4"][0.25]))
    check("insulation saves more of the heating the more roof per floor (the line's slope at least 0.08 a log unit)",
          C["R4_fit"]["b"] >= 0.08, "%.3f" % C["R4_fit"]["b"])
    check("this year's insulation applications have a third more roof per floor than the pilot's insulation works "
          "buildings, or more", dr[IM]["2026"] >= 1.33 * dr[IM]["pilot"],
          "%.3f against %.3f" % (dr[IM]["2026"], dr[IM]["pilot"]))
    withi = {}
    for t in ("office", "retail", "workshop"):
        gt, ct = GD._arms(P, IM, typ=t)
        med = np.nanmedian(np.concatenate([P.roof_ratio[gt], P.roof_ratio[ct]]))
        a_ = GD.season_savings(P, IM, rows=(gt[P.roof_ratio[gt] > med], ct[P.roof_ratio[ct] > med])).mean()
        b_ = GD.season_savings(P, IM, rows=(gt[P.roof_ratio[gt] <= med], ct[P.roof_ratio[ct] <= med])).mean()
        withi[t] = (a_, b_)
    C["R4_within_use"] = withi
    check("bar R5 the roof moves insulation's saving inside the uses with most of the works (the roofier half saves "
          "more in offices, shops and workshops)", all(a_ > b_ for a_, b_ in withi.values()),
          str({t: (pct(a_), pct(b_)) for t, (a_, b_) in withi.items()}))
    # the 2019 answers chose only weakly on the drivers: the pilot's answers stand close to the offered buildings
    off = np.where(P.offered2019)[0]
    for m, x, tol in ((CM, P.empty, 0.05), (IM, np.log(P.roof_ratio), 0.12)):
        ans = np.array([a["b"] for a in P.answers19 if a["measure"] == m])
        gap = []
        for t in range(len(GD.TYPES)):
            a_t = ans[P.typ[ans] == t]
            o_t = off[P.typ[off] == t]
            if len(a_t) >= 20:
                gap.append(abs(np.nanmean(x[a_t]) - np.nanmean(x[o_t])))
        check("bar R5 the 2019 %s answers chose little on the driver: within each use their mean sits within %.2f of the "
              "offered buildings'" % (m, tol), max(gap) <= tol, "worst %.3f" % max(gap))
    # ---- R5 and R6: the golden family inside its band, the call the same; the hurried routes outside
    A = C["A"]
    band5 = {"insulation": 0.008, "heating optimisation": 0.0025, "heating controls": 0.005}
    band6 = {"insulation": 0.05, "heating optimisation": 0.10, "heating controls": 0.05}
    C["R5_band"], C["R6_band"] = band5, band6
    for name, R in C["R56_rivals"].items():
        fs = fset(R)
        check("SF7 SF16 SF17 SF18 SF19 R6 %s: the same funded set" % name, fs == C["funded"], str(fs))
        for m in MEAS:
            check("SF7 R5 %s: %s's rate within its band" % (name, m), abs(R[m]["rate"] - A[m]["rate"]) <= band5[m],
                  "%.2f against %.2f" % (100 * R[m]["rate"], 100 * A[m]["rate"]))
            check("SF7 R6 %s: %s's grant per tonne within its band (5 per cent, heating optimisation 10)" % (name, m),
                  abs(R[m]["eur_t"] / A[m]["eur_t"] - 1) <= band6[m], "%.1f against %.1f" % (R[m]["eur_t"], A[m]["eur_t"]))
    check("the golden funds insulation and heating controls, not heating optimisation", C["funded"] == FUNDED,
          str(C["funded"]))
    check("margins: insulation and controls 8 per cent or more under the limit, heating optimisation 25 per cent over",
          A[IM]["eur_t"] <= 0.92 * GD.LIMIT and A[CM]["eur_t"] <= 0.92 * GD.LIMIT and A[HM]["eur_t"] >= 1.25 * GD.LIMIT,
          str({m: round(A[m]["eur_t"], 1) for m in MEAS}))
    sets = {name: fset(R) for name, R in C["R56_hurried"].items()}
    C["route_sets"] = sets
    use = C["R56_hurried"]["each use's saving, faded"]
    check("bar R3 each use's saving, faded (the pilot's lesson by use, carried to this year's applications) funds nothing",
          sets["each use's saving, faded"] == (), str(sets["each use's saving, faded"]))
    check("bar R3 and puts insulation and controls 6 per cent or more over the limit",
          use[IM]["eur_t"] >= 1.06 * GD.LIMIT and use[CM]["eur_t"] >= 1.06 * GD.LIMIT,
          "%.1f and %.1f" % (use[IM]["eur_t"], use[CM]["eur_t"]))
    check("bar R3 the pilot's seven-season average carried flat funds heating optimisation alone",
          sets["the pilot's seven-season average"] == (HM,), str(sets["the pilot's seven-season average"]))
    check("bar R3 the before and after funds all three", sets["the works buildings' own before and after"] == tuple(MEAS),
          str(sets["the works buildings' own before and after"]))
    check("bar R6 the empty week alone funds controls only, the roof alone insulation only",
          sets["controls on its empty week, insulation by use"] == (CM,) and
          sets["insulation on its roof, controls by use"] == (IM,),
          "%s, %s" % (sets["controls on its empty week, insulation by use"], sets["insulation on its roof, controls by use"]))
    wrong = {v for v in sets.values() if v != C["funded"]}
    check("bar R3 different shortcuts land on four or more different wrong funded sets", len(wrong) >= 4, str(sorted(wrong)))
    for name in ("each use's saving, faded", "the pilot's own mix, faded", "the empty week read off the load alone",
                 "controls on a straight line through the lived-in band"):
        R = C["R56_hurried"][name]
        for m in (CM,) if ("lived" in name or "load alone" in name) else (IM, CM):
            check("bar R3 R6 %s: %s's grant per tonne outside the 5 per cent band" % (name, m),
                  abs(R[m]["eur_t"] / A[m]["eur_t"] - 1) > band6[m], "%.1f against %.1f" % (R[m]["eur_t"], A[m]["eur_t"]))
    alone = C["R56_hurried"]["the empty week read off the load alone"][CM]["eur_t"]
    check("bar R6 the empty week read off the load alone (hotels and care homes at their night dip) keeps the call but "
          "moves controls' grant per tonne outside its band: the lived-in step moves figures, not the call",
          GD.LIMIT >= alone > (1 + C["R6_band"][CM]) * A[CM]["eur_t"], "%.1f against %.1f" % (alone, A[CM]["eur_t"]))
    lived_b = [p for p in C["R3_pts"] if p[0] <= 0.0]
    e_none = C["e_none"]
    lived_pilot = [b for b in np.concatenate(GD._arms(P, CM)) if P.lived_in[b]]
    strict_lived = V.empty_weeks(P, 0.5, "strict")[1]
    C["strict_lived_share"] = float(np.mean([strict_lived[b] for b in lived_pilot])) if lived_pilot else 0.0
    C["lived_load_read"] = float(np.nanmean(e_none[lived_pilot])) if lived_pilot else float("nan")
    check("SF17 the pilot's hotels and care homes read over half the week empty off their load alone and saved under "
          "1.5 per cent from controls, where the curve would give them 4 or more",
          C["lived_load_read"] >= 0.5 and lived_b and lived_b[0][1] < 0.015 and
          float(GD.dose_at(C["R3_fit"], C["lived_load_read"])[0]) >= 0.04,
          "%.3f empty, %.2f saved" % (C["lived_load_read"], 100 * lived_b[0][1] if lived_b else float("nan")))
    flat_ho = C["R56_hurried"]["the pilot's seven-season average"][HM]["eur_t"]
    check("the flat route funds heating optimisation by 8 per cent or more", flat_ho <= 0.92 * GD.LIMIT, "%.1f" % flat_ho)
    # ---- R7 the ranges and the flip rates
    for m in MEAS:
        lo, hi = C["R7"][m]["lo"], C["R7"][m]["hi"]
        side = hi < GD.LIMIT if m in C["funded"] else lo > GD.LIMIT
        check("R7 %s's 90 per cent range sits wholly on the call's side of the limit" % m, side, "%.1f to %.1f" % (lo, hi))
        if C["R7_rival_seed"]:
            lo2, hi2 = C["R7_rival_seed"][m]
            check("SF8 R7 %s's range under another resampling seed within 4 per cent at both ends" % m,
                  abs(lo2 / lo - 1) <= 0.04 and abs(hi2 / hi - 1) <= 0.04, "%.1f-%.1f against %.1f-%.1f" % (lo2, hi2, lo, hi))
    for m in GD.DRIVEN:
        lo_c, hi_c = C["R7_careful"][m]
        check("bar R3 R7 the range priced by use (%s) clears the limit on the wrong side" % m, lo_c > GD.LIMIT * 0.97,
              "%.1f to %.1f" % (lo_c, hi_c))
    # ---- R8 the round at close
    R8 = C["R8"]
    for m in MEAS:
        r = R8[m]
        for name, RR in C["R8_rivals"].items():
            check("SF9 R8 %s: %s's grant paid within 2 per cent" % (name, m), abs(RR[m]["paid"] / r["paid"] - 1) <= 0.02,
                  "%.0f against %.0f" % (RR[m]["paid"], r["paid"]))
    cnt = C["R8_hurried"]["count"][IM]
    check("bar R3 R8 insulation's late applications priced like the early ones: 15 per cent or more under the golden's grant",
          cnt["grant_close"] <= 0.85 * R8[IM]["grant_close"], "%.0f against %.0f" % (cnt["grant_close"], R8[IM]["grant_close"]))
    pl = C["R8_hurried"]["pooled"]
    check("bar R3 R8 one share for every measure: insulation 30 per cent or more under, controls 20 per cent or more over",
          pl[IM]["n_close"] <= 0.7 * R8[IM]["n_close"] and pl[CM]["n_close"] >= 1.2 * R8[CM]["n_close"],
          "%.0f and %.0f against %.0f and %.0f" % (pl[IM]["n_close"], pl[CM]["n_close"], R8[IM]["n_close"], R8[CM]["n_close"]))
    nw = C["R8_hurried"]["no withdrawals"]
    nw_tot = sum(nw[m]["paid"] for m in FUNDED)
    check("bar R3 R8 no withdrawals: the funded round's payment 3 per cent or more over the golden's",
          nw_tot >= 1.03 * C["R8_funded_paid"], "%.3f against %.3f million" % (nw_tot / 1e6, C["R8_funded_paid"] / 1e6))
    check("the 2019 answers in by the same day after the notice differ by measure by 30 points or more",
          R8[CM]["share"] - R8[IM]["share"] > 0.30, str({m: round(R8[m]["share"], 3) for m in MEAS}))
    check("the 2019 late insulation answers ran 25 per cent larger and withdrew at twice the early rate",
          R8[IM]["size"] > 1.25 and R8[IM]["w_late"] > 2 * R8[IM]["w_early"],
          "%.3f, %.3f against %.3f" % (R8[IM]["size"], R8[IM]["w_late"], R8[IM]["w_early"]))
    kp = W.SI[W.PIPELINE]
    true_paid = {m: sum(w.grant[W.PIPELINE][i] for i in range(w.N) if w.applied[i, kp] and w.measure26[i] == m
                        and not w.withdraw26[i]) for m in MEAS}
    C["R8_truth_paid"] = true_paid
    tp = sum(true_paid[m] for m in FUNDED)
    check("the golden projection lands within 15 per cent of what the world's round pays (the round's own sampling)",
          abs(C["R8_funded_paid"] / tp - 1) < 0.15, "%.3f against %.3f million" % (C["R8_funded_paid"] / 1e6, tp / 1e6))
    # ---- R10 the 2025/26 saving
    for name, v in C["R10_rivals"].items():
        check("SF10 R10 %s: within 3 per cent of the golden" % name, abs(v / C["R10"] - 1) <= 0.03,
              "%.0f against %.0f" % (v, C["R10"]))
    for name, v in C["R10_hurried"].items():
        check("bar R3 R10 %s: 6 per cent or more off the golden" % name, abs(v / C["R10"] - 1) >= 0.06,
              "%.0f against %.0f" % (v, C["R10"]))
    # ---- SF rows: the conventions that move nothing
    P2 = copy.copy(P)
    P2.works = P.drawn.copy()
    itt = {m: appr(P2, m) for m in MEAS}
    C["SF3_itt"] = {m: itt[m]["eur_t"] for m in MEAS}
    wald = {m: wald_seasons(P, m) for m in MEAS}
    C["SF3_wald"] = wald
    check("SF3 the draw's effect scaled by the share of drawn owners who had the works lands within a point of the "
          "golden in every season (the works buildings against the passed-over owners)",
          all(np.abs(wald[m] - C["R1"][m]).max() <= band1 for m in MEAS),
          str({m: round(100 * np.abs(wald[m] - C["R1"][m]).max(), 2) for m in MEAS}))
    check("SF3 withdrawn owners counted as if they had the works (the offer's effect, which plan 4.2's 'the buildings "
          "that had them' rules out) dilutes every saving", all(itt[m]["rate"] < A[m]["rate"] for m in MEAS),
          str({m: round(itt[m]["eur_t"], 1) for m in MEAS}))
    P3 = copy.copy(P)
    P3.typ = P.typ_register.copy()
    f3 = tuple(m for m in MEAS if appr(P3, m)["eur_t"] <= GD.LIMIT)
    check("SF4 each building's use from the register instead of its 2019 notice: same funded set", f3 == C["funded"], str(f3))
    if not quick:
        P15 = V.load(target, pro_rate=False)
        f15 = tuple(m for m in MEAS if appr(P15, m)["eur_t"] <= GD.LIMIT)
        check("bar R2 SF11 reads taken off 30 April counted whole to the nearer season: same funded set",
              f15 == C["funded"], str(f15))
        d15 = {m: appr(P15, m)["eur_t"] / A[m]["eur_t"] - 1 for m in MEAS}
        C["SF11_moves"] = d15
        check("bar R2 SF11 and insulation's and controls' grant per tonne within 5 per cent (heating optimisation's small "
              "late savings move most and it stays over the limit)",
              abs(d15[IM]) <= 0.05 and abs(d15[CM]) <= 0.05, str({m: round(v, 3) for m, v in d15.items()}))
        P16 = V.load(target, estimates="dropped")
        f16 = tuple(m for m in MEAS if appr(P16, m)["eur_t"] <= GD.LIMIT)
        check("bar R2 SF12 estimates dropped where no correction followed: same funded set", f16 == C["funded"], str(f16))
        P20 = V.load(target, outbuildings="dropped")
        f20 = tuple(m for m in MEAS if appr(P20, m)["eur_t"] <= GD.LIMIT)
        d20 = abs(appr(P20, IM)["eur_t"] / A[IM]["eur_t"] - 1)
        check("SF20 faces under 50 square metres beside a main roof (garages, sheds) left out of each address's roof: same funded set, "
              "insulation's grant per tonne within 5 per cent", f20 == C["funded"] and d20 <= 0.05, "%s %.3f" % (f20, d20))
    P17 = copy.copy(P)
    P17.U = P.U / np.array([P.hvec + (1 - P.hvec) * P.G_LT / P.G[s_] for s_ in S]).T
    f17 = tuple(m for m in MEAS if appr(P17, m)["eur_t"] <= GD.LIMIT)
    check("bar R2 SF13 raw use with no weather normalisation: same funded set", f17 == C["funded"], str(f17))
    raw = P.pipe_raw
    dup_b = {}
    for a in raw:
        dup_b.setdefault((a["b"], a["measure"]), []).append(a)
    twice = sum(1 for v in dup_b.values() if len(v) > 1)
    C["resubmitted_received"] = twice
    P18 = copy.copy(P)
    P18.pipe = [dict(a, typ=int(P.typ_register[a["b"]])) for a in raw]
    f18 = tuple(m for m in MEAS if appr(P18, m)["eur_t"] <= GD.LIMIT)
    check("bar R2 SF14 the revised applications kept beside the ones they replace: same funded set, %d buildings twice"
          % twice, f18 == C["funded"] and twice >= 5, str(f18))
    neither = sum(1 for a in P.answers19 if a["drawn"] and not a["withdrawn"] and not a["works"])
    both = sum(1 for a in P.answers19 if a["drawn"] and a["withdrawn"] and a["works"])
    check("SF15 every drawn 2019 owner either withdrew or completed the works (none neither, none both)",
          neither == 0 and both == 0, "%d neither, %d both" % (neither, both))
    # ---- bar R1 the field's raw material ships, and no shipped column holds a result
    check("bar R1 the pack ships the meter reads, the load profiles, the roofs, the pilot's responses and the "
          "applications at row level", len(P.answers19) > 2000 and len(P.pipe) > 500 and np.isfinite(P.U).sum() > 200000
          and len(P.week) > 20000 and rr_ok.sum() > 20000,
          "%d answers, %d applications, %d building-seasons, %d weeks, %d roofs" % (
              len(P.answers19), len(P.pipe), int(np.isfinite(P.U).sum()), len(P.week), int(rr_ok.sum())))
    # ---- bar R4 no plant: the lottery is balanced on use, on the 2018/19 season, on the empty week and the roof
    d0 = P.drawn & P.answered
    losers = P.answered & ~P.drawn
    bal = []
    for m in MEAS:
        a, b = d0 & (P.measure == m), losers & (P.measure == m)
        bal.append((np.nanmean(np.log(P.U[a, k0] / P.area[a])) - np.nanmean(np.log(P.U[b, k0] / P.area[b])),
                    np.nanmean(P.empty[a]) - np.nanmean(P.empty[b]),
                    np.nanmean(np.log(P.roof_ratio[a])) - np.nanmean(np.log(P.roof_ratio[b]))))
    C["balance"] = bal
    check("bar R4 the draw balances each measure's answers on the 2018/19 season per square metre (under 3 per cent), "
          "the empty week (under 0.03) and the roof per floor (under 8 per cent)",
          max(abs(x[0]) for x in bal) < 0.03 and max(abs(x[1]) for x in bal) < 0.03 and max(abs(x[2]) for x in bal) < 0.08,
          str([tuple(round(v, 3) for v in x) for x in bal]))
    vis_w = float((P.tune_season[P.works] > 0).mean())
    vis_l = float((P.tune_season[losers] > 0).mean())
    C["visited_share"] = {"works": vis_w, "passed over": vis_l}
    check("bar R4 the service visits reached works and passed-over buildings alike (within 5 points)",
          abs(vis_w - vis_l) < 0.05 and vis_w > 0.5, "%.3f and %.3f" % (vis_w, vis_l))
    pre = []
    for k in range(1, k0):
        a = np.log(P.U[d0, k] / P.U[d0, k - 1])
        b = np.log(P.U[losers, k] / P.U[losers, k - 1])
        pre.append(np.nanmean(a) - np.nanmean(b))
    check("bar R4 a placebo on the pre-pilot seasons shows no gap (each under a point)", max(abs(x) for x in pre) < 0.01,
          str([round(100 * x, 2) for x in pre]))
    ext = int(w.extended.any(1).sum())
    ext_pilot = int(w.extended[w.applied[:, W.SI[W.PILOT]]].any(1).sum())
    C["extended"] = (ext, ext_pilot)
    check("bar R4 the building changes run across the stock (extensions in over 1,000 buildings, 5 to 30 per cent of "
          "them pilot answers)", ext > 1000 and 0.05 < ext_pilot / float(ext) < 0.30, "%d, %d" % (ext, ext_pilot))
    # ---- input gates
    files = sorted(os.listdir(target))
    check("input gate: 10 or more files, 3 or more formats", len(files) >= 10 and
          len({os.path.splitext(f)[1] for f in files}) >= 3, "%d files" % len(files))
    nrow = {}
    for f_ in ("gas_meter_reads_2013_2026.csv", "electricity_load_profiles_2025.csv", "benchmarking_notices_2019_2026.csv"):
        with open(os.path.join(target, f_), encoding="utf-8") as fh:
            nrow[f_] = sum(1 for _ in fh) - 1
    C["rows"] = nrow
    check("input gate: two CSVs of 20,000 rows or more, one of 10 printed pages or more",
          nrow["gas_meter_reads_2013_2026.csv"] >= 20000 and nrow["electricity_load_profiles_2025.csv"] >= 20000, str(nrow))
    counts = [len(GD.apps(P, m)) for m in MEAS] + [int(((P.measure == m) & P.works).sum()) for m in MEAS]
    check("realism: no two measures share a count of applications or works buildings", len(set(counts)) == len(counts),
          str(counts))
    check("realism: no headline grant is a round ten thousand", all(A[m]["grant"] % 10000 != 0 for m in MEAS))
    return C


# ---------------------------------------------------------------- figures.json and effort.json

def figures(C):
    P, A = C["P"], C["A"]
    seasons = ["%d/%02d" % (s - 1, s % 100) for s in range(GD.PILOT + 1, GD.PIPELINE + 1)]
    car = C["R56_hurried"]["each use's saving, faded"]
    F = {
        "funded": list(C["funded"]), "not_funded": [m for m in MEAS if m not in C["funded"]],
        "season_labels": seasons,
        "R1_saving_by_season_pct": {m: [pct(x) for x in C["R1"][m]] for m in MEAS},
        "R1_before_after_pct": {m: [pct(x) for x in C["R1_hurried"]["works buildings' own before and after"][m]] for m in MEAS},
        "R2_life_saving_pct": {m: pct(C["R2"][m]) for m in MEAS},
        "R2_seven_season_avg_pct": {m: pct(C["R1"][m].mean()) for m in MEAS},
        "R2_ho_floor_pct": pct(C["R2_fit"][HM][0]),
        "R2_ho_first_pct": pct(C["R1"][HM][0]), "R2_ho_fourth_pct": pct(C["R1"][HM][3]),
        "R3_controls_at_empty_pct": {"%d" % round(100 * e): pct(v) for e, v in C["R3"].items()},
        "R3_threshold_empty_pct": round(100 * C["R3_fit"]["e0"], 1),
        "R3_slope_points_per_tenth": round(10 * C["R3_fit"]["slope"], 2),
        "R3_lived_in_pct": pct(C["R3_fit"]["lived"]),
        "R3_bands": [[pct(x), pct(v)] for x, v, _ in C["R3_pts"]],
        "R3_empty_week_pct": {k: pct(v) for k, v in C["drivers"][CM].items()},
        "R3_line_through_lived_in_at_70_pct": pct(C["R3_hurried"]["a straight line through the lived-in band too"][0.70]),
        "R4_heating_at_roof_pct": {("%.2f" % r).rstrip("0").rstrip("."): pct(v) for r, v in C["R4"].items()},
        "R4_line": [round(C["R4_fit"]["a"], 4), round(C["R4_fit"]["b"], 4)],
        "R4_bands": [[round(math.exp(x), 2), pct(v)] for x, v, _ in C["R4_pts"]],
        "R4_roof_per_floor": {k: round(v, 2) for k, v in C["drivers"][IM].items()},
        "R5_rate_on_applications_pct": {m: pct(A[m]["rate"]) for m in MEAS},
        "R5_by_use_rate_pct": {m: pct(car[m]["rate"]) for m in MEAS},
        "R5_pooled_life_pct": {m: pct(GD.lifetime(C["R1"][m], m)) for m in MEAS},
        "R6_eur_per_tonne": {m: round(A[m]["eur_t"], 2) for m in MEAS},
        "R6_eur_per_tonne_unrounded": {m: round(A[m]["eur_t"], 4) for m in MEAS},
        "R6_by_use_eur_per_tonne": {m: round(car[m]["eur_t"], 2) for m in MEAS},
        "applications_received": {m: A[m]["n"] for m in MEAS},
        "grant_received_eur": {m: int(round(A[m]["grant"])) for m in MEAS},
        "lifetime_tonnes_received": {m: int(round(A[m]["tonnes"])) for m in MEAS},
        "R7_range_eur": {m: [round(C["R7"][m]["lo"], 2), round(C["R7"][m]["hi"], 2)] for m in MEAS},
        "R7_break_even_pct": {m: pct(C["R7"][m]["break_even"]) for m in MEAS},
        "R7_by_use_range_eur": {m: [round(v, 2) for v in C["R7_careful"][m]] for m in GD.DRIVEN},
        "R8_applications_at_close": {m: int(round(C["R8"][m]["n_close"])) for m in MEAS},
        "R8_grant_at_close_eur": {m: int(round(C["R8"][m]["grant_close"])) for m in MEAS},
        "R8_grant_paid_eur": {m: int(round(C["R8"][m]["paid"])) for m in MEAS},
        "R8_funded_paid_eur": int(round(C["R8_funded_paid"])),
        "R8_funded_close_eur": int(round(C["R8_funded_close"])),
        "R8_share_by_day_pct": {m: pct(C["R8"][m]["share"]) for m in MEAS},
        "R8_late_size_premium_pct": {m: pct(C["R8"][m]["size"] - 1.0) for m in MEAS},
        "R8_withdrawn_pct": {m: [pct(C["R8"][m]["w_early"]), pct(C["R8"][m]["w_late"])] for m in MEAS},
        "R9_applications": len(C["apps"]),
        "R9_grant_eur": int(round(sum(a["grant"] for a in C["apps"]))),
        "R9_tonnes": int(round(sum(a["life_t"] for a in C["apps"]))),
        "R9_tonnes_by_measure": {m: int(round(sum(a["life_t"] for a in C["apps"] if a["measure"] == m))) for m in MEAS},
        "R10_tonnes": int(round(C["R10"])),
        "R10_hurried_tonnes": {k: int(round(v)) for k, v in C["R10_hurried"].items()},
        "routes": {k: list(v) for k, v in C["route_sets"].items()},
        "hurried_eur_per_tonne": {k: {m: round(v[m]["eur_t"], 2) for m in MEAS} for k, v in C["R56_hurried"].items()},
        "limit_eur": int(GD.LIMIT), "lives": GD.LIFE, "factor": GD.EF,
        "works_buildings": {m: int(((P.measure == m) & P.works).sum()) for m in MEAS},
        "passed_over": {m: int(((P.measure == m) & P.answered & ~P.drawn).sum()) for m in MEAS},
        "answers_2019": len(P.answers19), "drawn_2019": int(P.drawn.sum()), "works_2019": int(P.works.sum()),
        "visited_share_pct": {k: pct(v) for k, v in C["visited_share"].items()},
        "resubmitted_received": C["resubmitted_received"],
        "lived_in_applications": int(sum(1 for a in C["apps"] if a["measure"] == CM and P.lived_in[a["b"]])),
    }
    return F


def effort(C, F):
    """the three passes, each computed end to end by its own methods on the cut pack"""
    P, A = C["P"], C["A"]
    M = MEAS
    car = C["R56_hurried"]["each use's saving, faded"]
    qk = C["R56_hurried"]["the works buildings' own before and after"]
    fs_c, rows_c = apps_route(P, C, "each use's saving, faded")
    fs_q, rows_q = apps_route(P, C, "the works buildings' own before and after")
    gold_rows = {a["no"]: a["life_t"] for a in C["apps"]}

    def rows_value(rows):
        return {k: round(rows.get(k, 0.0), 1) for k in gold_rows}
    s_tab = {"%s %s" % (m, F["season_labels"][j]): pct(C["R1"][m][j]) for m in M for j in range(7)}
    s_bands = {k: [v - 0.45, v + 0.45] for k, v in s_tab.items()}
    q_tab = {"%s %s" % (m, F["season_labels"][j]): pct(C["R1_hurried"]["works buildings' own before and after"][m][j])
             for m in M for j in range(7)}
    gold_life = {m: pct(C["R2"][m]) for m in M}
    life_bands = {m: [pct(C["R2"][m] - C["R2_band"][m]), pct(C["R2"][m] + C["R2_band"][m])] for m in M}
    ba_life = {m: pct(C["R1_hurried"]["works buildings' own before and after"][m].mean()) for m in M}
    b3, b4 = 100 * C["R3_band"], 100 * C["R4_band"]
    gold_r3 = {"controls at %d per cent empty" % round(100 * e): pct(v) for e, v in C["R3"].items()}
    gold_r3["this year's controls applications, share of the week empty"] = pct(C["drivers"][CM]["2026"])
    r3_bands = {k: [v - b3, v + b3] for k, v in gold_r3.items()}
    r3_bands["this year's controls applications, share of the week empty"] = [gold_r3[
        "this year's controls applications, share of the week empty"] - 3.0, gold_r3[
        "this year's controls applications, share of the week empty"] + 3.0]
    flat_r3 = {k: (pct(C["R1"][CM].mean()) if k.startswith("controls at") else None) for k in gold_r3}
    gold_r4 = {"insulation's heating saving at %s m2 of roof per m2" % (("%.2f" % r).rstrip("0").rstrip(".")): pct(v)
               for r, v in C["R4"].items()}
    gold_r4["this year's insulation applications, roof per floor (x100)"] = pct(C["drivers"][IM]["2026"])
    r4_bands = {k: [v - b4, v + b4] for k, v in gold_r4.items()}
    r4_bands["this year's insulation applications, roof per floor (x100)"] = [
        gold_r4["this year's insulation applications, roof per floor (x100)"] * 0.93,
        gold_r4["this year's insulation applications, roof per floor (x100)"] * 1.07]
    flat_r4 = {k: (pct(C["R4_hurried"]["one saving for every building"][1.0]) if k.startswith("insulation's") else None)
               for k in gold_r4}
    R = []
    R.append({"id": "R1", "name": "each measure's saving by season", "graded_as": "Ask 2",
              "figure": "R1_table", "depends": [], "independent": "",
              "golden": s_tab, "bands": s_bands, "partly_share": 0.5,
              "passes": {"quick": q_tab, "careful": s_tab, "thorough": s_tab}})
    R.append({"id": "R2", "name": "heating optimisation's saving over its life", "graded_as": "Component 1",
              "figure": "R2_table", "depends": ["R1"], "independent": "",
              "golden": gold_life, "bands": life_bands, "partly_share": 0.6,
              "passes": {"quick": ba_life,
                         "careful": {"value": {m: pct(C["R2_rivals"]["last3"][m]) for m in M}, "grade": "right",
                                     "why": "a frontier run sees heating optimisation fall season by season and carries "
                                            "the level it settles at (the platform's architecture 7 run did, on the "
                                            "last three seasons)"},
                         "thorough": gold_life}})
    R.append({"id": "R3", "name": "controls along the empty week", "graded_as": "Component 2",
              "figure": "R3_table", "depends": ["R1"], "independent": "",
              "golden": gold_r3, "bands": r3_bands, "partly_share": 0.5,
              "passes": {"quick": {k: None for k in gold_r3}, "careful": flat_r3, "thorough": gold_r3}})
    R.append({"id": "R4", "name": "insulation along the roof per floor", "graded_as": "Component 3",
              "figure": "R4_table", "depends": ["R1"], "independent": "",
              "golden": gold_r4, "bands": r4_bands, "partly_share": 0.5,
              "passes": {"quick": {k: None for k in gold_r4}, "careful": flat_r4, "thorough": gold_r4}})
    for rid, m, dep in (("R5a", IM, ["R4"]), ("R5b", HM, ["R2"]), ("R5c", CM, ["R3"])):
        g = pct(A[m]["rate"])
        bd = 100 * C["R5_band"][m]
        R.append({"id": rid, "name": "%s's saving rate on this year's applications" % m, "graded_as": "Ask 3",
                  "figure": "R5_rate_%s" % m.replace(" ", "_"), "depends": dep, "independent": "",
                  "golden": g, "band": [g - bd, g + bd], "partly": [g - 2.5 * bd, g + 2.5 * bd],
                  "passes": {"quick": pct(qk[m]["rate"]), "careful": pct(car[m]["rate"]), "thorough": g}})
    R.append({"id": "R6", "name": "the funded set at the limit", "graded_as": "Recommendation",
              "figure": "funded", "depends": ["R5a", "R5b", "R5c"], "independent": "",
              "golden": list(C["funded"]),
              "passes": {"quick": list(fs_q), "careful": list(fs_c), "thorough": list(C["funded"])}})
    gold_r7, r7_bands = {}, {}
    for m in M:
        gold_r7[m + " flip"] = pct(C["R7"][m]["break_even"])
        r7_bands[m + " flip"] = [gold_r7[m + " flip"] - 0.05, gold_r7[m + " flip"] + 0.05]
        for end, key in (("lo", "low"), ("hi", "high")):
            v = round(C["R7"][m][end], 2)
            gold_r7["%s %s" % (m, key)] = v
            r7_bands["%s %s" % (m, key)] = [v * 0.95, v * 1.05]
    car_r7 = {k: (gold_r7[k] if k.endswith("flip") else None) for k in gold_r7}
    for m in GD.DRIVEN:
        car_r7[m + " low"], car_r7[m + " high"] = (round(v, 2) for v in C["R7_careful"][m])
    for key in (HM + " low", HM + " high"):
        car_r7[key] = gold_r7[key]
    R.append({"id": "R7", "name": "each range and flip rate", "graded_as": "Ask 4",
              "figure": "R7_table", "depends": ["R5a", "R5b", "R5c"], "independent": "",
              "golden": gold_r7, "bands": r7_bands, "partly_share": 0.4,
              "passes": {"quick": {k: (gold_r7[k] if k.endswith("flip") else None) for k in gold_r7},
                         "careful": car_r7, "thorough": gold_r7}})
    gold_r8, r8_bands = {}, {}
    for m in M:
        for key in ("n_close", "grant_close", "paid"):
            v = round(C["R8"][m][key], 0)
            gold_r8["%s %s" % (m, key)] = v
            r8_bands["%s %s" % (m, key)] = [v * 0.90, v * 1.10]

    def r8_of(RR):
        return {"%s %s" % (m, key): round(RR[m][key], 0) for m in M for key in ("n_close", "grant_close", "paid")}
    R.append({"id": "R8a", "name": "each measure's round at close", "graded_as": "Ask 5",
              "figure": "R8_table", "depends": [], "independent": "the 2019 responses and the 2026 applications",
              "golden": gold_r8, "bands": r8_bands, "partly_share": 0.4,
              "passes": {"quick": r8_of(C["R8_hurried"]["pooled"]),
                         "careful": {"value": r8_of(C["R8_rivals"]["one withdrawal rate"]), "grade": "right",
                                     "why": "the platform's architecture 7 run projected the round measure by measure "
                                            "with late quotes larger and completion by size and timing"},
                         "thorough": gold_r8}})
    tot = {"asked": round(C["R8_funded_close"], 0), "paid": round(C["R8_funded_paid"], 0)}
    car_tot = {"asked": round(sum(C["R8"][m]["grant_close"] for m in fs_c), 0),
               "paid": round(sum(C["R8"][m]["paid"] for m in fs_c), 0)}
    q_tot = {"asked": round(sum(C["R8_hurried"]["pooled"][m]["grant_close"] for m in fs_q), 0),
             "paid": round(sum(C["R8_hurried"]["pooled"][m]["paid"] for m in fs_q), 0)}
    R.append({"id": "R8b", "name": "the funded round's grant asked and paid", "graded_as": "Component 4",
              "figure": "R8_funded_table", "depends": ["R6", "R8a"], "independent": "",
              "golden": tot, "bands": {k: [v * 0.90, v * 1.10] for k, v in tot.items()}, "partly_share": 0.5,
              "passes": {"quick": q_tot, "careful": car_tot, "thorough": tot}})
    R.append({"id": "R9", "name": "every application's lifetime tonnes", "graded_as": "Ask 6",
              "figure": "R9_table", "depends": ["R5a", "R5b", "R5c"], "independent": "",
              "golden": rows_value(gold_rows),
              "bands": {k: [v * 0.95, v * 1.05] for k, v in rows_value(gold_rows).items()},
              "partly_share": 0.35,
              "passes": {"quick": rows_value(rows_q), "careful": rows_value(rows_c), "thorough": rows_value(gold_rows)}})
    R.append({"id": "R10", "name": "the pilot's 2025/26 CO2", "graded_as": "Ask 7",
              "figure": "R10_tonnes", "depends": ["R1"], "independent": "",
              "golden": F["R10_tonnes"], "band": [F["R10_tonnes"] * 0.97, F["R10_tonnes"] * 1.03],
              "partly": [F["R10_tonnes"] * 0.92, F["R10_tonnes"] * 1.08],
              "passes": {"quick": int(round(C["R10_hurried"]["before and after"])),
                         "careful": F["R10_tonnes"], "thorough": F["R10_tonnes"]}})
    routes = [{"name": "the golden", "answer": list(C["funded"]), "golden": True}]
    for k, v in C["route_sets"].items():
        routes.append({"name": k, "answer": list(v)})
    hints = [{"sentence": "this year's owners chose the measure that suits their building, so price controls along the share "
                          "of the week each building stands empty, from its load profile, and roof insulation along its "
                          "roof per floor, from the cadastre and the register",
              "rescues": ["R3", "R4", "R5a", "R5c", "R6", "R8b"]},
             {"sentence": "a hotel's or care home's load dips while its guests or residents sleep, so its profile reads it "
                          "as empty when it is lived in", "rescues": []},
             {"sentence": "controls save only while a building stands empty, nothing until about two fifths of the week, "
                          "and the meter operator's 2025 profiles show each building's week; this year's controls "
                          "applicants stand empty longer than the pilot's", "rescues": ["R3", "R5c"]},
             {"sentence": "roof insulation saves with how much roof a building has for its floor, which the solar cadastre "
                          "and the register give; this year's insulation applicants have more roof per floor than the "
                          "pilot's", "rescues": ["R4", "R5a"]},
             {"sentence": "heating optimisation's saving falls back to a small part of its first season's within four "
                          "winters", "rescues": ["R2"]},
             {"sentence": "the late insulation applications run larger and are withdrawn more often", "rescues": ["R8a"]}]
    return {"results": R, "routes": routes, "hints": hints,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}


def tables_for_figures(F, E):
    """the effort results' tables, written into figures.json under the keys effort.json names"""
    for r in E["results"]:
        if r["figure"] not in F:
            F[r["figure"]] = r["golden"]
    return F


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    C = run(target, HERE, quick="--quick" in sys.argv)
    for name, ok, d in RESULTS:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, d))
    print("%d checks, %d failed" % (len(RESULTS), sum(1 for r in RESULTS if not r[1])))
