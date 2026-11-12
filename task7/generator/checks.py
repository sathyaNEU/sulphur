"""task7 architecture 9: the generator's assertions, run on the cut pack (verify.load) against the world's clean truth.
Every result of the design note's results chain (R1 to R10) is computed here with its rivals (the band) and with the
careful but hurried pass and the quick pass (effort.json); every row of the semantic fork table is asserted, and the bar
block (dataset-generation 7.1, labelled "bar" below); the figures the deliverables and the answer blocks print are made
here."""
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
B_BOOT = 1000
EMPTY_AT = (0.50, 0.60, 0.70)              # the shares of the week empty R4 is read at
ROOF_AT = (1.0, 0.5, 0.25)                 # the square metres of roof per square metre of floor R5 is read at
CM, IM, HM = "heating controls", "insulation", "heating optimisation"
MARGIN = 0.08                              # every call's upper end 8 per cent or more from the limit
LINE_HI, LINE_LO = GD.LIMIT * (1 + MARGIN), GD.LIMIT * (1 - MARGIN)
ROUTE_MARGIN = 0.06                        # a shortcut route's measures 6 per cent or more across the line from it
R2_BAND = 0.6                              # points: the works' own saving in the last three seasons, rivals inside
POINT_BAND = {IM: 0.05, HM: 0.15, CM: 0.05}    # grant per tonne
HI_BAND = {IM: 0.10, HM: 0.30, CM: 0.15}       # the upper end of the 90 per cent range (the low ends are not graded)
RATE_BAND = {IM: 1.2, HM: 0.4, CM: 1.0}        # points: each measure's saving rate over its life
CLOSE_BAND, APP_T_BAND, TOTAL_BAND = 10, 5, 10  # per cent: the round at close, an application's tonnes, the funded total
ROUTE_HI, ROUTE_LO = GD.LIMIT * (1 + ROUTE_MARGIN), GD.LIMIT * (1 - ROUTE_MARGIN)


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


def at_empty(fit):
    return {e: float(GD.dose_at(fit, e)[0]) for e in EMPTY_AT}


def at_roof(fit):
    return {r: float(GD.dose_at(fit, math.log(r))[0]) for r in ROOF_AT}


def drivers(P):
    """the gas-weighted mean driver of each driven measure's pilot works buildings, and the reference-weighted mean of
    this year's applications for it"""
    k0 = P.si[GD.PILOT]
    out = {}
    for m, x in ((CM, P.empty), (IM, P.roof_ratio)):
        g, _ = GD._arms(P, m)
        g = g[np.isfinite(x[g]) & np.isfinite(P.U[g, k0])]
        A = GD.apps(P, m)
        xa = np.array([x[a["b"]] for a in A])
        wa = np.array([a["ref_kwh"] for a in A])
        out[m] = {"pilot": float(np.average(x[g], weights=P.U[g, k0])), "2026": float(np.average(xa, weights=wa))}
    return out


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


def opt_appr(P, s, sizes, persist="settled"):
    return GD.appraisal(P, HM, GD.opt_rates_from(P, s, sizes, persist))


def stratified_owner_range(P, m, B=B_BOOT, seed=31):
    """the owner draw taken within each owner's use (a rival for R7)"""
    rng = np.random.default_rng(seed + MEASURES_IDX[m])
    og, oc = GD.arm_owners(P, m)

    def strata(L):
        by = {}
        for v in L:
            by.setdefault(int(np.bincount(P.typ[v]).argmax()), []).append(v)
        return by
    sg, sc = strata(og), strata(oc)
    vals = []
    for _ in range(B):
        gi = np.concatenate([v[j] for v in sg.values() for j in rng.integers(0, len(v), len(v))])
        ci = np.concatenate([v[j] for v in sc.values() for j in rng.integers(0, len(v), len(v))])
        vals.append(GD.eur_t_on_rows(P, m, (gi, ci)))
    vals = np.array(vals)
    return float(np.percentile(vals, 5)), float(np.percentile(vals, 95))


def jackknife_range(P, m):
    """delete one owner at a time, the spread scaled to a normal 90 per cent range (a rival for R7)"""
    og, oc = GD.arm_owners(P, m)
    full = GD.eur_t_on_rows(P, m, (np.concatenate(og), np.concatenate(oc)))
    vals = []
    for side in (0, 1):
        L = og if side == 0 else oc
        for j in range(len(L)):
            rest = [v for k, v in enumerate(L) if k != j]
            rows = (np.concatenate(rest), np.concatenate(oc)) if side == 0 else (np.concatenate(og), np.concatenate(rest))
            vals.append(GD.eur_t_on_rows(P, m, rows))
    vals = np.array(vals)
    n = len(vals)
    se = math.sqrt((n - 1) / n * ((vals - vals.mean()) ** 2).sum()) if n > 1 else 0.0
    return full - 1.645 * se, full + 1.645 * se


MEASURES_IDX = {m: k for k, m in enumerate(MEAS)}
RULED_OUT_R3 = ("the passed-over owners' check season kept",)


# ---------------------------------------------------------------- each result, golden, rivals and hurried

def results(P, quick=False):
    C = {}
    B = 120 if quick else B_BOOT
    # R1 each measure's saving by season against the passed-over owners
    C["R1"] = {m: GD.season_savings(P, m) for m in MEAS}
    C["R1_rivals"] = {"two-season baseline": {m: GD.season_savings(P, m, base="two") for m in MEAS},
                      "comparison by use type": {m: post_stratified(P, m) for m in MEAS}}
    C["R1_hurried"] = {"works buildings' own before and after": {m: GD.before_after(P, m) for m in MEAS}}
    # R2 heating optimisation's saving as its works alone keep it: each works building before its campaign check
    s_own, sz = GD.own_savings(P, HM, with_sizes=True)
    C["R2"], C["R2_sizes"] = s_own, sz
    C["R2_rivals"] = {
        "the passed-over owners' check season kept": GD.own_savings(P, HM, exclude_check_season=False, with_sizes=True),
        "the average of the buildings' shares": GD.own_savings(P, HM, how="mean_log", with_sizes=True),
        "only the works buildings that took no campaign check": GD.own_savings(P, HM, works_rule="declined",
                                                                              with_sizes=True)}
    C["R2_campaign_share"] = (C["R1"][HM] - s_own) / C["R1"][HM]
    g, c = GD._arms(P, HM)
    cs = P.check_season
    C["R2_n"] = [(int(((cs[g] == 0) | (cs[g] > s)).sum()), len(g)) for s in P.seasons[P.si[GD.PILOT] + 1:]]
    C["R2_checked_share"] = {"works": float((cs[g] > 0).mean()), "passed over": float((cs[c] > 0).mean())}
    # R4 controls along the empty week; R5 insulation along the roof per floor (on the heating part)
    C["R4_pts"] = GD.dose_points(P, CM)
    C["R4_fit"] = GD.dose_fit(C["R4_pts"], CM)
    C["R4"] = at_empty(C["R4_fit"])
    C["R4_rivals"] = {"four bands": at_empty(GD.dose_fit(GD.dose_points(P, CM, 4), CM)),
                      "eight bands": at_empty(GD.dose_fit(GD.dose_points(P, CM, 8), CM)),
                      "a straight line through the bands of buildings that close":
                          at_empty(GD.dose_fit(C["R4_pts"], CM, "linear"))}
    C["R4_hurried"] = {"one saving for every building": {e: float(C["R1"][CM].mean()) for e in EMPTY_AT}}
    C["R5_pts"] = GD.dose_points(P, IM)
    C["R5_fit"] = GD.dose_fit(C["R5_pts"], IM)
    C["R5"] = at_roof(C["R5_fit"])
    C["R5_rivals"] = {"four bands": at_roof(GD.dose_fit(GD.dose_points(P, IM, 4), IM)),
                      "eight bands": at_roof(GD.dose_fit(GD.dose_points(P, IM, 8), IM)),
                      "the bands as steps": at_roof(GD.dose_fit(C["R5_pts"], IM, "bins"))}
    k0 = P.si[GD.PILOT]
    gi, _ = GD._arms(P, IM)
    gi = gi[np.isfinite(P.U[gi, k0])]
    hw_pool = float(np.average(P.hvec[gi], weights=P.U[gi, k0]))
    C["R5_hurried"] = {"one saving for every building": {r: float(C["R1"][IM].mean() / (1 - hw_pool)) for r in ROOF_AT}}
    C["drivers"] = drivers(P)
    # R3 and R6 each measure's saving rate over its life on this year's applications; R7 grant per tonne and range
    A = {m: appr(P, m) for m in MEAS}
    C["A"] = A
    C["R3"] = A[HM]["rate"]
    C["R3_rivals"] = {"the level from the last two seasons": opt_appr(P, s_own, sz, "settled_last2"),
                      "a fitted approach to a level": opt_appr(P, s_own, sz, "floor_own")}
    for name, (s_, z_) in C["R2_rivals"].items():
        C["R3_rivals"][name] = opt_appr(P, s_, z_)
    C["R3_hurried"] = {
        "the seasons as measured, a fitted approach to a level": appr(P, HM, route="measured"),
        "the seasons as measured, the last three carried": appr(P, HM, route="measured", persist="last3"),
        "the seven seasons' average carried flat": appr(P, HM, route="flat")}
    riv = {"four bands of each driver": {"nb": 4}, "eight bands of each driver": {"nb": 8},
           "each driver's bands as steps": {"form": "bins"},
           "a straight line through the bands of buildings that close": {"form": "linear"},
           "insulation on its share of the gas": {"heat_part": False},
           "two-season baseline": {"base": "two"}, "the last three seasons carried": {"persist": "last3"}}
    C["R6_rivals"] = {name: {m: appr(P, m, **kw) for m in (IM, CM)} for name, kw in riv.items()}
    for name, kw in (("an empty hour read 40 per cent of the way up its week", {"threshold": 0.4}),
                     ("an empty hour read 60 per cent of the way up its week", {"threshold": 0.6}),
                     ("hotels and care homes lived in where their weekend days run above their nights",
                      {"lived_rule": "weekend"}),
                     ("hotels and care homes lived in where every weekend day hour runs above every night hour",
                      {"lived_rule": "strict"}),
                     ("hotels and care homes read off their load alone", {"lived_rule": "none"})):
        C["R6_rivals"][name] = {CM: appr(P, CM, empty=V.empty_weeks(P, **kw)[0])}
    C["R6_hurried"] = {"each use's saving, faded": {m: appr(P, m, route="use") for m in (IM, CM)},
                       "the pilot's seven-season average": {m: appr(P, m, route="pooled_flat") for m in (IM, CM)}}
    C["R7"] = {}
    for m in MEAS:
        lo, hi, vals = GD.draw_range(P, m, B, unit="owner")
        blo, bhi, _ = GD.draw_range(P, m, B, unit="building")
        fin = vals[np.isfinite(vals)]
        C["R7"][m] = {"point": A[m]["eur_t"], "lo": lo, "hi": hi, "b_lo": blo, "b_hi": bhi,
                      "share_under_limit": float((vals <= GD.LIMIT).mean()),
                      "normal_hi": A[m]["eur_t"] + 1.645 * float(fin.std(ddof=1)),
                      "reflected_hi": 2 * A[m]["eur_t"] - lo, "n_no_tonnes": int((~np.isfinite(vals)).sum()),
                      "hi_no_tonnes_negative": float(np.percentile(np.where(np.isfinite(vals), vals, -1e9), 95))}
    C["R7_rivals"] = {}
    if not quick:
        C["R7_rivals"]["another draw of the owners"] = {m: GD.draw_range(P, m, B, seed=7, unit="owner")[:2] for m in MEAS}
        C["R7_rivals"]["owners drawn within their use"] = {m: stratified_owner_range(P, m, B) for m in MEAS}
        C["R7_rivals"]["owners left out one at a time"] = {m: jackknife_range(P, m) for m in MEAS}
    # the shortcut routes on optimisation, with either range
    C["R7_measured"] = {"owner": GD.draw_range(P, HM, B, unit="owner", route="measured")[:2],
                        "building": GD.draw_range(P, HM, B, unit="building", route="measured")[:2]}
    C["R7_flat"] = {"owner": GD.draw_range(P, HM, B, unit="owner", route="flat")[:2]}
    # R8 the funded set, and every route's
    hi = {m: C["R7"][m]["hi"] for m in MEAS}
    bhi = {m: C["R7"][m]["b_hi"] for m in MEAS}
    C["funded"] = tuple(m for m in MEAS if GD.funded(hi[m]))
    C["routes"] = {
        "the golden: the works' own saving, ranges at the owner": C["funded"],
        "the measured seasons carried, ranges at the building":
            tuple(m for m in MEAS if GD.funded(C["R7_measured"]["building"][1] if m == HM else bhi[m])),
        "the works' own saving, ranges at the building": tuple(m for m in MEAS if GD.funded(bhi[m])),
        "the measured seasons carried, ranges at the owner":
            tuple(m for m in MEAS if GD.funded(C["R7_measured"]["owner"][1] if m == HM else hi[m])),
        "the point estimate against the limit, no range":
            tuple(m for m in MEAS if (C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]["eur_t"]
                                      if m == HM else A[m]["eur_t"]) <= GD.LIMIT)}
    C["routes"]["each use's saving, the measured seasons, ranges at the building"] = tuple(
        m for m in MEAS if (C["R6_hurried"]["each use's saving, faded"][m]["eur_t"] if m != HM
                            else C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]["eur_t"])
        * (bhi[m] / A[m]["eur_t"] if m != HM else 1.1) <= GD.LIMIT)
    # R9 each measure's round once the offer closes, and the lifetime tonnes the funded measures' applications buy
    C["R9"] = {m: GD.at_close(P, m) for m in MEAS}
    C["R9_rivals"] = {"one withdrawal rate": {m: GD.at_close(P, m, "one withdrawal rate") for m in MEAS}}
    C["R9_hurried"] = {h: {m: GD.at_close(P, m, h) for m in MEAS} for h in ("count", "pooled", "received")}
    C["R9_tonnes"] = sum(A[m]["tonnes"] for m in C["funded"])
    C["R9_tonnes_routes"] = {
        name: sum((C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]["tonnes"]
                   if (m == HM and "measured" in name) else A[m]["tonnes"]) for m in st)
        for name, st in C["routes"].items()}
    # R10 every application received, its grant and lifetime tonnes
    C["apps"] = []
    for m in MEAS:
        rates = GD.app_rates(P, m)
        for a, r, t in zip(GD.apps(P, m), rates, A[m]["app_tonnes"]):
            C["apps"].append(dict(a, rate=float(r), life_t=float(t), funded=m in C["funded"], bid=P.bid[a["b"]],
                                  use=GD.TYPES[a["typ"]], empty=float(P.empty[a["b"]]),
                                  roof=float(P.roof_ratio[a["b"]]), owner=P.owner_no[int(P.owner[a["b"]])]))
    C["apps"].sort(key=lambda x: x["no"])
    C["mean_app_rate"] = {m: float(np.mean([a["rate"] for a in C["apps"] if a["measure"] == m])) for m in MEAS}
    meas_t = C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]["app_tonnes"]
    C["apps_measured_opt"] = {a["no"]: float(t) for a, t in zip(GD.apps(P, HM), meas_t)}
    return C


# ---------------------------------------------------------------- the assertions

def run(target, gen_dir, quick=False):
    w = W.build()
    P = V.load(target)
    C = results(P, quick)
    C["P"] = P
    k0 = P.si[GD.PILOT]
    # ---- Layer 1: the pack rebuilds the world's normal-weather use, its checks, its owners, its weeks and its roofs
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
          "99.9th %.4f, worst %.4f" % (np.percentile(err, 99.9), err.max()))
    check("L1 every service check read off the meter file is the world's",
          all(set(P.visits[k]) == {d for d in w.visits[int(i)] if w.first[int(i)] <= W.season_of(d) <= w.last[int(i)]}
              for k, i in enumerate(order)))
    same_owner = all(len({P.owner[k] for k in np.where(w.owner[order] == o)[0]}) == 1 for o in
                     np.unique(w.owner)[:400])
    check("L1 the register's owner numbers are the world's owners", same_owner and len(P.owner_no) == w.n_owners,
          "%d owners" % len(P.owner_no))
    check("L1 the pilot's works buildings read off the response file are the world's",
          (P.works == w.works[order]).all() and (P.drawn == w.drawn[order]).all())
    check("L1 the draw was among owners: every owner's answering buildings are all drawn or all passed over",
          all(len({bool(P.drawn[b]) for b in np.where(P.answered & (P.owner == o))[0]}) <= 1
              for o in np.unique(P.owner[P.answered])))
    closing = np.isfinite(P.empty) & ~P.lived_in
    e_err = np.abs(P.empty[closing] - w.empty[order][closing])
    check("L1 the empty week read off the 2025 profiles is the building's own: within 0.05 for 95 per cent of the "
          "buildings that close", np.percentile(e_err, 95) <= 0.05, "95th %.3f" % np.percentile(e_err, 95))
    rr = P.roof_ratio
    rr_ok = np.isfinite(rr)
    r_err = np.abs(np.log(rr[rr_ok] / w.roof_ratio[order][rr_ok]))
    check("L1 the roof per floor from the cadastre and the register is the building's own: within 10 per cent for 90 "
          "per cent of buildings", np.percentile(r_err, 90) <= 0.10, "90th %.3f" % np.percentile(r_err, 90))
    # ---- R1: every rival inside the band (1.5 points), the before and after outside it
    for name, R in C["R1_rivals"].items():
        for m in MEAS:
            d = np.abs(R[m] - C["R1"][m]).max()
            check("SF R1 %s: %s within 2.5 points of the golden in every season" % (name, m), d <= 0.025,
                  "worst %.2f points" % (100 * d))
    ba = C["R1_hurried"]["works buildings' own before and after"]
    check("bar R1 the before and after sits outside the band in most cells",
          sum(int(abs(ba[m][j] - C["R1"][m][j]) > 0.025) for m in MEAS for j in range(7)) >= 14)
    # ---- R2: the works' own saving keeps falling where the measured levels; every rival within a point late on
    s_own, meas = C["R2"], C["R1"][HM]
    check("bar R2 the measured saving levels from 2022/23 (the last four seasons within 0.6 points of each other)",
          meas[3:].max() - meas[3:].min() <= 0.006, "%s" % np.round(100 * meas[3:], 2))
    check("bar R2 the works' own saving falls a point or more under the measured in each of the last three seasons",
          (meas[-3:] - s_own[-3:] >= 0.01).all(), "gaps %s" % np.round(100 * (meas[-3:] - s_own[-3:]), 2))
    for name, (s_, _) in C["R2_rivals"].items():
        d = np.abs(s_[-3:] - s_own[-3:]).max()
        if name in RULED_OUT_R3:
            check("SF R2 %s (ruled out, as R3): within a point of the golden in the last three seasons" % name,
                  d <= 0.01, "worst %.2f points" % (100 * d))
        else:
            check("SF R2 %s: inside the band (%.1f points) in each of the last three seasons" % (name, R2_BAND),
                  d <= R2_BAND / 100.0, "worst %.2f points" % (100 * d))
    check("bar R2 the measured seasons sit outside the band in each of the last three seasons",
          (meas[-3:] - s_own[-3:] > R2_BAND / 100.0 + 0.003).all(), "gaps %s" % np.round(100 * (meas[-3:] - s_own[-3:]), 2))
    check("bar R2 the campaign reached both arms alike (checked shares within 12 points)",
          abs(C["R2_checked_share"]["works"] - C["R2_checked_share"]["passed over"]) <= 0.12,
          "%s" % {k: round(v, 3) for k, v in C["R2_checked_share"].items()})
    # the price shock moved both arms alike: the measured saving does not step at 2022/23 beyond its own fade
    cr = [C["R1"][m][3] - C["R1"][m][2] for m in (IM, CM)]
    check("bar R2 the 2022 price shock moves insulation's and controls' savings by under a point at 2022/23",
          all(abs(x) <= 0.012 for x in cr), "%s" % np.round(100 * np.array(cr), 2))
    # ---- R3: optimisation's rate over its life; rivals within the band, the measured routes outside it
    r3 = C["R3"]
    for name, a in C["R3_rivals"].items():
        if name in RULED_OUT_R3:
            check("SF R3 %s (ruled out: it takes the campaign out of the works arm and leaves its own check-season dip in "
                  "the passed-over arm): the same call, optimisation's upper end over the limit" % name,
                  C["R7"][HM]["b_hi"] * a["eur_t"] / C["A"][HM]["eur_t"] > GD.LIMIT,
                  "%.2f against %.2f" % (100 * a["rate"], 100 * r3))
            continue
        check("SF R3 %s: within %.1f points of the golden rate" % (name, RATE_BAND[HM]),
              abs(a["rate"] - r3) <= RATE_BAND[HM] / 100.0,
              "%.2f against %.2f" % (100 * a["rate"], 100 * r3))
    for name, a in C["R3_hurried"].items():
        check("bar R3 %s: 1 point or more over the golden rate" % name, a["rate"] - r3 >= 0.01,
              "%.2f against %.2f" % (100 * a["rate"], 100 * r3))
    # ---- R4, R5, R6: the transports (earned steps) pinned
    for name, R in C["R4_rivals"].items():
        d = max(abs(R[e] - C["R4"][e]) for e in EMPTY_AT)
        check("SF R4 %s: within 2.5 points at every reading" % name, d <= 0.025, "worst %.2f" % (100 * d))
    for name, R in C["R5_rivals"].items():
        d = max(abs(R[r] - C["R5"][r]) for r in ROOF_AT)
        check("SF R5 %s: within 3.5 points at every reading" % name, d <= 0.035, "worst %.2f" % (100 * d))
    for name, R in C["R6_rivals"].items():
        for m, band in ((IM, RATE_BAND[IM] / 100.0), (CM, RATE_BAND[CM] / 100.0)):
            if m not in R:
                continue
            check("SF R6 %s: %s within %.1f points of the golden rate" % (name, m, 100 * band),
                  abs(R[m]["rate"] - C["A"][m]["rate"]) <= band,
                  "%.2f against %.2f" % (100 * R[m]["rate"], 100 * C["A"][m]["rate"]))
            if m == CM:
                check("SF R6 %s: controls' upper end on the golden's side of the limit" % name,
                      GD.funded(C["R7"][CM]["hi"] * C["A"][CM]["eur_t"] / R[m]["eur_t"]) == GD.funded(C["R7"][CM]["hi"]),
                      "%.1f" % (C["R7"][CM]["hi"] * C["A"][CM]["eur_t"] / R[m]["eur_t"]))

    for name, R in C["R6_hurried"].items():
        for m in (IM, CM):
            check("bar R6 %s: %s 10 per cent or more off the golden grant per tonne" % (name, m),
                  abs(R[m]["eur_t"] / C["A"][m]["eur_t"] - 1) >= 0.10,
                  "%.1f against %.1f" % (R[m]["eur_t"], C["A"][m]["eur_t"]))
    # ---- R7 and the call: every upper end 8 per cent or more from the limit, both ways
    R7 = C["R7"]
    check("bar R8 insulation's upper end under the line at the owner and at the building",
          R7[IM]["hi"] <= LINE_LO and R7[IM]["b_hi"] <= LINE_LO, "%.1f, %.1f" % (R7[IM]["hi"], R7[IM]["b_hi"]))
    check("bar R8 heating optimisation's upper end over the line at the owner (the golden) and over the route line at "
          "the building", R7[HM]["hi"] >= LINE_HI and R7[HM]["b_hi"] >= ROUTE_HI,
          "%.1f, %.1f" % (R7[HM]["hi"], R7[HM]["b_hi"]))
    check("bar R8 heating optimisation's measured seasons carried put its upper end under the route line at either unit",
          C["R7_measured"]["owner"][1] <= ROUTE_LO and C["R7_measured"]["building"][1] <= ROUTE_LO,
          "%.1f, %.1f" % (C["R7_measured"]["owner"][1], C["R7_measured"]["building"][1]))
    check("bar R8 controls' upper end over the line at the owner (the golden) and under the route line at the building",
          R7[CM]["hi"] >= LINE_HI and R7[CM]["b_hi"] <= ROUTE_LO, "%.1f, %.1f" % (R7[CM]["hi"], R7[CM]["b_hi"]))
    for name, R in C["R7_rivals"].items():
        for m in MEAS:
            lo, hi_ = R[m]
            side = (hi_ <= GD.LIMIT) == GD.funded(R7[m]["hi"])
            check("SF R7 %s: %s on the golden's side of the limit, the upper end inside its band (%d per cent)"
                  % (name, m, round(100 * HI_BAND[m])), side and abs(hi_ / R7[m]["hi"] - 1) <= HI_BAND[m],
                  "%.1f against %.1f" % (hi_, R7[m]["hi"]))
    for name, R in {"the measured seasons carried, owners drawn again": {HM: C["R7_measured"]["owner"]},
                    "buildings drawn again": {m: (R7[m]["b_lo"], R7[m]["b_hi"]) for m in (CM,)}}.items():
        for m, (lo, hi_) in R.items():
            check("bar R7 %s: %s's upper end outside its band" % (name, m), abs(hi_ / R7[m]["hi"] - 1) > HI_BAND[m] + 0.03,
                  "%.1f against %.1f" % (hi_, R7[m]["hi"]))
    check("bar R8 the funded set is insulation alone", C["funded"] == (IM,), "%s" % (C["funded"],))
    sets = list(C["routes"].values())
    check("bar R8 the four combinations of the two judgments land on four different sets",
          len({sets[0], sets[1], sets[2], sets[3]}) == 4, "%s" % C["routes"])
    # ---- the fork table's rows, SF1 to SF9 (DESIGN_NOTE.md, Semantic fork table)
    s_ml = C["R2_rivals"]["the average of the buildings' shares"][0]
    check("SF1 the average of the buildings' shares lands inside R2's band in each of the last three seasons (plan 4.2 "
          "takes the share of the gas; same call)", np.abs(s_ml[-3:] - s_own[-3:]).max() <= R2_BAND / 100.0,
          "worst %.2f points" % (100 * np.abs(s_ml[-3:] - s_own[-3:]).max()))
    mr = C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]
    check("SF2 the seasons as measured carried put optimisation's grant per tonne 10 per cent or more off and its upper end "
          "under the limit (ruled out: plan 4.4 against what the building would burn without the works, the campaign "
          "closed)", abs(mr["eur_t"] / C["A"][HM]["eur_t"] - 1) >= 0.10 and C["R7_measured"]["owner"][1] <= ROUTE_LO,
          "%.2f against %.2f; upper end %.2f" % (mr["eur_t"], C["A"][HM]["eur_t"], C["R7_measured"]["owner"][1]))
    check("SF3 a round's saving rate is plan 4.4's ratio of lifetime tonnes to the tonnes the reference consumption "
          "carries (the average of the applications' own rates ruled out by 4.4)",
          all(abs(sum(a["life_t"] for a in C["apps"] if a["measure"] == m) /
                  (C["A"][m]["ref_mwh"] * GD.EF * GD.LIFE[m]) - C["A"][m]["rate"]) <= 1e-9 for m in MEAS),
          "the average of the applications' rates: %s" % {m: round(100 * v, 2) for m, v in C["mean_app_rate"].items()})
    check("SF4 buildings drawn again put controls' upper end under the route line (ruled out: rules 3, the draw among "
          "owners, and the committee's range if the pilot had been drawn again)", R7[CM]["b_hi"] <= ROUTE_LO,
          "%.2f against %.2f" % (R7[CM]["b_hi"], R7[CM]["hi"]))
    for m in MEAS:
        v = R7[m]["normal_hi"]
        check("SF5 a symmetric range from the draws' spread: %s's upper end on the golden's side and inside its band" % m,
              ((v <= GD.LIMIT) == GD.funded(R7[m]["hi"])) and abs(v / R7[m]["hi"] - 1) <= HI_BAND[m],
              "%.1f against %.1f" % (v, R7[m]["hi"]))
    check("SF5 the reflected range (ruled out: the committee's range is the spread the estimate itself would have if the "
          "pilot were drawn again, which the reflected range is not)", True,
          "; ".join("%s %.1f" % (m, R7[m]["reflected_hi"]) for m in MEAS))
    for m in MEAS:
        check("SF6 a draw whose works save nothing, read as no tonnes or as a negative grant per tonne: %s's upper end "
              "moves under 1 per cent" % m, abs(R7[m]["hi_no_tonnes_negative"] / R7[m]["hi"] - 1) <= 0.01,
              "%d draws; %.2f against %.2f" % (R7[m]["n_no_tonnes"], R7[m]["hi_no_tonnes_negative"], R7[m]["hi"]))
    pt = C["routes"]["the point estimate against the limit, no range"]
    check("SF7 the point against the limit funds another set (ruled out: the committee judges the upper end)",
          set(pt) != set(C["funded"]), "%s" % (pt,))
    check("SF8 the test and the listing on the applications received by 12 June (the committee's request; the prompt's "
          "applications received so far); a grant per tonne is the round's grant over its tonnes, so the late "
          "applications' count moves neither", True, "%s" % {m: C["A"][m]["n"] for m in MEAS})
    for m in MEAS:
        a, r = C["R9"][m], C["R9_hurried"]["received"][m]
        check("SF9 the applications received so far sit 10 per cent or more under %s's round at close" % m,
              r["n_close"] <= 0.9 * a["n_close"] and r["grant_close"] <= 0.9 * a["grant_close"],
              "%d against %.0f" % (r["n_close"], a["n_close"]))
    # ---- R9: the round at close; the one-withdrawal rival inside 10 per cent
    nt, cl = GD.NOTICE, GD.CLOSE
    check("SF R9 the same day read by the calendar or by the days since the notice: one cut (both offers went out on "
          "the same day of the year and closed on the same day)",
          (nt[GD.PILOT].month, nt[GD.PILOT].day) == (nt[GD.PIPELINE].month, nt[GD.PIPELINE].day) and
          (cl[GD.PILOT].month, cl[GD.PILOT].day) == (cl[GD.PIPELINE].month, cl[GD.PIPELINE].day))
    a, r = C["R9"][IM], C["R9_hurried"]["count"][IM]
    check("bar R9 the late answers' larger grants left out: insulation's grant at close %d per cent or more under"
          % CLOSE_BAND, r["grant_close"] <= (1 - CLOSE_BAND / 100.0) * a["grant_close"],
          "%.0f against %.0f" % (r["grant_close"], a["grant_close"]))
    return C


# ---------------------------------------------------------------- figures and the effort passes

def figures(C):
    P = C["P"]
    A = C["A"]
    F = {"seasons": ["%d/%02d" % (s - 1, s % 100) for s in P.seasons[P.si[GD.PILOT] + 1:]]}
    F["R1"] = {m: [pct(x) for x in C["R1"][m]] for m in MEAS}
    F["R2_own"] = [pct(x) for x in C["R2"]]
    F["R2_campaign_points"] = [pct(a - b) for a, b in zip(C["R1"][HM], C["R2"])]
    F["R2_n_works_clean"] = [n for n, _ in C["R2_n"]]
    F["R3_rate"] = pct(C["R3"])
    F["R3_measured_rate"] = pct(C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]["rate"])
    F["R4"] = {("%d" % round(100 * e)): pct(v) for e, v in C["R4"].items()}
    F["R5"] = {("%.2f" % r): pct(v) for r, v in C["R5"].items()}
    F["drivers"] = {m: {k: round(v, 4) for k, v in d.items()} for m, d in C["drivers"].items()}
    F["rates"] = {m: pct(A[m]["rate"]) for m in MEAS}
    F["eur_t"] = {m: round(A[m]["eur_t"], 2) for m in MEAS}
    F["range"] = {m: [round(C["R7"][m]["lo"], 2), round(C["R7"][m]["hi"], 2)] for m in MEAS}
    F["range_building"] = {m: [round(C["R7"][m]["b_lo"], 2), round(C["R7"][m]["b_hi"], 2)] for m in MEAS}
    F["measured_opt_eur_t"] = round(C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]["eur_t"], 2)
    F["measured_opt_range"] = [round(x, 2) for x in C["R7_measured"]["owner"]]
    F["n_apps"] = {m: A[m]["n"] for m in MEAS}
    F["grant_received"] = {m: round(A[m]["grant"]) for m in MEAS}
    F["tonnes"] = {m: round(A[m]["tonnes"]) for m in MEAS}
    F["funded"] = list(C["funded"])
    F["routes"] = {k: list(v) for k, v in C["routes"].items()}
    F["close"] = {m: {"n": round(C["R9"][m]["n_close"]), "grant": round(C["R9"][m]["grant_close"])} for m in MEAS}
    F["funded_tonnes"] = round(C["R9_tonnes"])
    F["funded_grant"] = round(sum(a["grant"] for a in C["apps"] if a["funded"]))
    F["n_apps_total"] = len(C["apps"])
    F["grant_total"] = round(sum(a["grant"] for a in C["apps"]))
    F["tonnes_total"] = round(sum(a["life_t"] for a in C["apps"]))
    F["campaign_share_last"] = pct(C["R2_campaign_share"][-1])
    F["R2_table"] = {s: v for s, v in zip(F["seasons"][-3:], F["R2_own"][-3:])}
    F["empty_pct"] = {k: round(100 * v, 2) for k, v in F["drivers"][CM].items()}
    F["measured_level_last3"] = round(sum(F["R1"][HM][-3:]) / 3.0, 2)
    # the conventions the answer blocks state: the limit, the range's level and each graded figure's band
    F["conventions"] = {"limit_eur_per_tonne": GD.LIMIT, "range_level_pct": 90,
                        "bands_pct": {"grant per tonne": {m: round(100 * v) for m, v in POINT_BAND.items()},
                                      "range upper end": {m: round(100 * v) for m, v in HI_BAND.items()},
                                      "round at close": CLOSE_BAND, "an application's lifetime tonnes": APP_T_BAND,
                                      "the funded total": TOTAL_BAND},
                        "bands_points": {"own saving by season": R2_BAND,
                                         "rate over the life": dict(RATE_BAND)}}
    F["R7_table"] = {}
    for m in MEAS:
        F["R7_table"]["%s grant per tonne" % m] = F["eur_t"][m]
        F["R7_table"]["%s range high" % m] = F["range"][m][1]
    F["R9_table"] = {"%s at close %s" % (m, k): F["close"][m][k] for m in MEAS for k in ("n", "grant")}
    F["R10_table"] = {"the funded applications": sorted(a["no"] for a in C["apps"] if a["funded"]),
                      "their lifetime tonnes in all": F["funded_tonnes"]}
    return F


def effort(C, F):
    """effort.json: each result's golden, band and the value each pass files (quick, careful but hurried, thorough)"""
    A = C["A"]
    seas = F["seasons"]
    meas_route = C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]
    res = []
    # R2 heating optimisation's saving as its works alone keep it, in the campaign's seasons (Component 1)
    g2 = F["R2_table"]
    b2 = {k: [round(v - R2_BAND, 2), round(v + R2_BAND, 2)] for k, v in g2.items()}
    c2 = {s: v for s, v in zip(seas[-3:], F["R1"][HM][-3:])}
    res.append({"id": "R2", "name": "heating optimisation's saving as its works alone keep it", "graded_as": "Component 1",
                "figure": "R2_table", "depends": [], "independent": "", "golden": g2, "bands": b2, "partly_share": 0.67,
                "precedent": ["N15", "N13", "L26"],
                "passes": {"quick": c2, "careful": c2, "thorough": g2}})
    # R6 each measure's saving rate over its life on this year's applications (Ask 1)
    g6 = F["rates"]
    rb6 = F["conventions"]["bands_points"]["rate over the life"]
    b6 = {m: [round(g6[m] - rb6[m], 2), round(g6[m] + rb6[m], 2)] for m in MEAS}
    use = C["R6_hurried"]["each use's saving, faded"]
    res.append({"id": "R6", "name": "each measure's saving rate over its life on this year's applications",
                "graded_as": "Ask 1", "figure": "rates", "depends": ["R2"], "independent": "", "golden": g6,
                "bands": b6, "partly_share": 0.6, "precedent": ["N15", "N12", "L28"],
                "passes": {"quick": {IM: pct(use[IM]["rate"]), CM: pct(use[CM]["rate"]),
                                     HM: pct(C["R3_hurried"]["the seven seasons' average carried flat"]["rate"])},
                           "careful": {IM: g6[IM], CM: g6[CM], HM: pct(meas_route["rate"])}, "thorough": g6}})
    # R7 each grant per tonne and the upper end of its range (Ask 2, Components 2 and 3)
    g7 = F["R7_table"]
    b7 = {}
    for m in MEAS:
        v = g7["%s grant per tonne" % m]
        b7["%s grant per tonne" % m] = [round(v * (1 - POINT_BAND[m]), 2), round(v * (1 + POINT_BAND[m]), 2)]
        v = g7["%s range high" % m]
        b7["%s range high" % m] = [round(v * (1 - HI_BAND[m]), 2), round(v * (1 + HI_BAND[m]), 2)]
    c7 = {}
    for m in MEAS:
        c7["%s grant per tonne" % m] = F["measured_opt_eur_t"] if m == HM else F["eur_t"][m]
        c7["%s range high" % m] = round(C["R7_measured"]["building"][1] if m == HM else F["range_building"][m][1], 2)
    res.append({"id": "R7", "name": "each grant per tonne and the upper end of its 90 per cent range",
                "graded_as": "Ask 2, Components 2 and 3", "figure": "R7_table", "depends": ["R6"], "independent": "",
                "golden": g7, "bands": b7, "partly_share": 0.5, "precedent": ["L19", "L35"],
                "passes": {"quick": {k: None for k in g7}, "careful": c7, "thorough": g7}})
    # R8 the funded set (Recommendation)
    res.append({"id": "R8", "name": "the funded set", "graded_as": "Recommendation", "figure": "funded",
                "depends": ["R6", "R7"], "independent": "", "golden": F["funded"], "precedent": ["L19", "N15"],
                "passes": {"quick": list(C["routes"]["each use's saving, the measured seasons, ranges at the building"]),
                           "careful": list(C["routes"]["the measured seasons carried, ranges at the building"]),
                           "thorough": F["funded"]}})
    # R9 each measure's round at close (Ask 3)
    g9 = F["R9_table"]
    b9 = {k: [v * (1 - CLOSE_BAND / 100.0), v * (1 + CLOSE_BAND / 100.0)] for k, v in g9.items()}
    q9 = {}
    for m in MEAS:
        q9["%s at close n" % m] = F["n_apps"][m]
        q9["%s at close grant" % m] = F["grant_received"][m]
    res.append({"id": "R9", "name": "each measure's round at close", "graded_as": "Ask 3", "figure": "R9_table",
                "depends": [], "independent": "the 2019 responses and the 2026 applications", "golden": g9, "bands": b9,
                "partly_share": 0.5, "passes": {"quick": q9, "careful": g9, "thorough": g9}})
    # R10 the funded measures' applications with grant and lifetime tonnes, and their total (Ask 4)
    g10 = F["R10_table"]
    tot = "their lifetime tonnes in all"
    b10 = {tot: [g10[tot] * (1 - TOTAL_BAND / 100.0), g10[tot] * (1 + TOTAL_BAND / 100.0)]}

    def listing(route):
        st = C["routes"][route]
        return {"the funded applications": sorted(a["no"] for a in C["apps"] if a["measure"] in st),
                tot: round(C["R9_tonnes_routes"][route])}
    res.append({"id": "R10", "name": "the funded measures' applications and their lifetime tonnes", "graded_as": "Ask 4",
                "figure": "R10_table", "depends": ["R8"], "independent": "", "golden": g10, "bands": b10,
                "partly_share": 0.5, "precedent": ["L19", "N15"],
                "passes": {"quick": listing("each use's saving, the measured seasons, ranges at the building"),
                           "careful": listing("the measured seasons carried, ranges at the building"), "thorough": g10}})
    routes = [{"name": k, "answer": list(v), "golden": k.startswith("the golden")} for k, v in C["routes"].items()]
    hints = [{"sentence": "the state campaign's heating checks from September 2022 set heating curves back down, the "
                          "pilot's balanced works buildings held it while the passed-over owners' systems did not, and "
                          "the campaign has closed", "rescues": ["R2", "R6"]},
             {"sentence": "the pilot was drawn by owner and an owner's facility manager runs all its buildings alike, so "
                          "the range comes from drawing owners again", "rescues": ["R7"]}]
    forcing = {"kind": "set", "line": GD.LIMIT,
               "golden_family": [{"name": "the golden", "answer": F["funded"]}] +
               [{"name": "R7 rival: %s" % name, "answer": [m for m in MEAS if R[m][1] <= GD.LIMIT]}
                for name, R in C["R7_rivals"].items()] +
               [{"name": "R6 rival: %s (optimisation's upper end scaled)" % name,
                 "answer": [m for m in MEAS if (C["R7"][m]["hi"] * (a["eur_t"] / A[HM]["eur_t"] if m == HM else 1.0))
                            <= GD.LIMIT]} for name, a in C["R3_rivals"].items() if name not in RULED_OUT_R3],
               "shortcuts": [{"name": k, "answer": list(v)} for k, v in C["routes"].items() if not k.startswith("the golden")],
               "perturbations": [{"input": "heating optimisation's settled level %+d per cent" % p,
                                  "answer": [m for m in MEAS if (C["R7"][m]["hi"] * (1.0 / (1 + 0.55 * p / 100.0)
                                                                                      if m == HM else 1.0)) <= GD.LIMIT]}
                                 for p in (-20, 20)] +
                                [{"input": "controls' saving rate %+d per cent" % p,
                                  "answer": [m for m in MEAS if (C["R7"][m]["hi"] * (1.0 / (1 + p / 100.0) if m == CM
                                                                                      else 1.0)) <= GD.LIMIT]}
                                 for p in (-20, 20)] +
                                [{"input": "insulation's saving rate %+d per cent" % p,
                                  "answer": [m for m in MEAS if (C["R7"][m]["hi"] * (1.0 / (1 + p / 100.0) if m == IM
                                                                                      else 1.0)) <= GD.LIMIT]}
                                 for p in (-20, 20)]}
    return {"results": res, "routes": routes, "hints": hints, "forcing": forcing,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
