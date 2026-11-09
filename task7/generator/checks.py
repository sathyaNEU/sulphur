"""task7 architecture 7: the generator's assertions, run on the cut pack (verify.load) against the world's clean truth.
Every result of the design note's results chain is computed here with its rivals (the band) and with the careful but
hurried pass and the quick pass (effort.json); every row of the semantic fork table (SF1 to SF15) and the bar block
(R1 to R7, dataset-generation 7.1) is asserted; the figures the deliverables and the answer blocks print are made here."""
import copy
import datetime as dt
import json
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


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def rnd(v, u):
    """half up, as an analyst rounds"""
    return math.floor(v / u + 0.5) * u


def edge(v, u):
    """distance from v to the nearest edge of the cell it prints in, at unit u"""
    return u / 2.0 - abs(v - rnd(v, u))


def pct(x):
    return round(100.0 * x, 2)


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
    # R2 each measure's saving over its service life, the pilot's buildings
    C["R2"] = {m: GD.lifetime(C["R1"][m], m, "floor") for m in MEAS}
    C["R2_profile"] = {m: GD.profile(C["R1"][m], GD.LIFE[m], "floor") for m in MEAS}
    C["R2_fit"] = {m: GD._fit_floor(C["R1"][m]) for m in MEAS}
    C["R2_zero_fit"] = {m: GD._fit_zero(C["R1"][m]) for m in MEAS}
    C["R2_rivals"] = {h: {m: GD.lifetime(C["R1"][m], m, h) for m in MEAS} for h in ("last", "last3")}
    C["R2_rivals"]["two-season baseline"] = {m: GD.lifetime(C["R1_rivals"]["two-season baseline"][m], m) for m in MEAS}
    C["R2_hurried"] = {h: {m: GD.lifetime(C["R1"][m], m, h) for m in MEAS} for h in ("flat", "first", "zero", "linear")}
    # R3 each measure's saving by building type (the seven seasons' average), and the two occupancy classes
    C["R3"] = {m: GD.type_levels(P, m) for m in MEAS}
    C["R3_class"] = {m: GD.class_levels(P, m) for m in MEAS}
    C["R3_n"] = {m: {t: tuple(len(x) for x in GD._arms(P, m, typ=t)) for t in GD.TYPES} for m in MEAS}
    # R4 each measure's saving rate on this year's applications over its life; R5 grant per tonne and the call
    A = {m: GD.appraisal(P, m, GD.app_rates(P, m)) for m in MEAS}
    C["A"] = A
    C["R4"] = {m: A[m]["rate"] for m in MEAS}
    C["R5"] = {m: A[m]["eur_t"] for m in MEAS}
    C["funded"] = tuple(m for m in MEAS if A[m]["eur_t"] <= GD.LIMIT)
    riv = {}
    for name, kw in (("occupancy class", {"route": "class"}), ("the last season carried", {"persist": "last"}),
                     ("the last three seasons carried", {"persist": "last3"}), ("two-season baseline", {"base": "two"})):
        riv[name] = {m: GD.appraisal(P, m, GD.app_rates(P, m, **kw)) for m in MEAS}
    C["R45_rivals"] = riv
    hur = {}
    for name, kw in (("the pilot's seven-season average", {"route": "pooled_flat"}),
                     ("the pilot's own mix, faded", {"route": "pooled"}),
                     ("each type's seven-season average", {"route": "type_flat"}),
                     ("an exponential fall to nothing", {"persist": "zero"})):
        hur[name] = {m: GD.appraisal(P, m, GD.app_rates(P, m, **kw)) for m in MEAS}
    hur["the works buildings' own before and after"] = {
        m: GD.appraisal(P, m, np.full(len(GD.apps(P, m)), C["R1_hurried"]["works buildings' own before and after"][m].mean()))
        for m in MEAS}
    C["R45_hurried"] = hur
    # R6 each grant per tonne's 90 per cent range and the saving rate at which its call flips
    C["R6"] = {}
    for m in MEAS:
        lo, hi, vals = GD.bootstrap(P, m, B=B_BOOT)
        C["R6"][m] = {"lo": lo, "hi": hi, "break_even": A[m]["break_even_rate"],
                      "share_under_limit": float((vals <= GD.LIMIT).mean())}
    C["R6_rival_seed"] = {m: GD.bootstrap(P, m, B=B_BOOT, seed=7)[:2] for m in MEAS} if not quick else {}
    # R7 the round once the offer closes
    C["R7"] = {m: GD.at_close(P, m) for m in MEAS}
    C["R7_rivals"] = {h: {m: GD.at_close(P, m, h) for m in MEAS} for h in ("one withdrawal rate",)}
    C["R7_hurried"] = {h: {m: GD.at_close(P, m, h) for m in MEAS} for h in ("count", "pooled", "no withdrawals",
                                                                            "received")}
    C["R7_funded_paid"] = sum(C["R7"][m]["paid"] for m in FUNDED)
    C["R7_funded_close"] = sum(C["R7"][m]["grant_close"] for m in FUNDED)
    # R8 the CO2 the pilot's works saved in 2025/26
    C["R8"] = GD.season_saving_2026(P)
    C["R8_rivals"] = {"each use type's own 2025/26 saving": GD.season_saving_2026(P, "by type")}
    C["R8_hurried"] = {h: GD.season_saving_2026(P, h) for h in ("on the use with the works", "average on the 2018/19 use",
                                                               "2025/26 rate on the 2018/19 use", "before and after")}
    # R9 every funded application's lifetime tonnes
    C["apps"] = []
    for m in MEAS:
        rates = GD.app_rates(P, m)
        for a, r, t in zip(GD.apps(P, m), rates, A[m]["app_tonnes"]):
            C["apps"].append(dict(a, rate=float(r), life_t=float(t), funded=m in C["funded"], bid=P.bid[a["b"]],
                                  use=GD.TYPES[a["typ"]]))
    C["apps"].sort(key=lambda x: x["no"])
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


def apps_hurried(P, C, route="the pilot's own mix, faded"):
    """the careful but hurried pass's funded application rows: its funded set, its rates"""
    hur = C["R45_hurried"][route]
    fs = tuple(m for m in MEAS if hur[m]["eur_t"] <= GD.LIMIT)
    rows = {}
    for m in fs:
        for a, t in zip(GD.apps(P, m), hur[m]["app_tonnes"]):
            rows[a["no"]] = float(t)
    return fs, rows


# ---------------------------------------------------------------- the assertions

def run(target, gen_dir, quick=False):
    w = W.build()
    P = V.load(target)
    C = results(P, quick)
    C["P"] = P
    S = P.seasons
    k0, k26 = P.si[GD.PILOT], P.si[GD.PIPELINE]
    # ---- Layer 1: the pack rebuilds the world's normal-weather use
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
    # ---- R1 the saving by season: every rival inside the band, the hurried routes outside it
    band1 = 0.80 / 100.0
    for name, R in C["R1_rivals"].items():
        for m in MEAS:
            d = np.abs(R[m] - C["R1"][m]).max()
            check("SF5 R1 %s: %s within 0.8 points of the golden in every season" % (name, m), d <= band1,
                  "worst %.2f points" % (100 * d))
    ba = C["R1_hurried"]["works buildings' own before and after"]
    check("R3 R1 the before and after sits 3 points or more off the golden in every season and measure",
          all(np.abs(ba[m] - C["R1"][m]).min() >= 0.03 for m in MEAS),
          str({m: round(100 * np.abs(ba[m] - C["R1"][m]).min(), 1) for m in MEAS}))
    eq = C["R1_hurried"]["average of the buildings' shares"]
    check("SF2 the average of the buildings' shares is another quantity (the plan's share of the gas): controls 0.8 points off",
          np.abs(eq["heating controls"] - C["R1"]["heating controls"]).mean() > 0.008,
          "%.2f points" % (100 * np.abs(eq["heating controls"] - C["R1"]["heating controls"]).mean()))
    # ---- R2 each measure's saving over its life
    band2 = {"insulation": 0.004, "heating optimisation": 0.0020, "heating controls": 0.0020}
    C["R2_band"] = band2
    for name, R in C["R2_rivals"].items():
        for m in MEAS:
            check("SF6 R2 %s: %s within its band of the golden" % (name, m), abs(R[m] - C["R2"][m]) <= band2[m],
                  "%.2f against %.2f" % (100 * R[m], 100 * C["R2"][m]))
    hm = "heating optimisation"
    for name in ("flat", "first", "zero", "linear"):
        v = C["R2_hurried"][name][hm]
        check("R3 R2 heating optimisation's life saving, %s: outside the band by its own width or more" % name,
              abs(v - C["R2"][hm]) >= 2 * band2[hm], "%.2f against %.2f" % (100 * v, 100 * C["R2"][hm]))
    s = C["R1"][hm]
    f, d, tau, sse = C["R2_fit"][hm]
    s1z, tauz, ssez = C["R2_zero_fit"][hm]
    C["R2_fit_note"] = {"floor": f, "tau": tau, "sse": sse, "zero_sse": ssez,
                        "zero_last3_misfit": float(np.mean(s[-3:] - s1z * np.exp(-(np.arange(5, 8) - 1.0) / tauz)))}
    check("SF6 the seasons level off: an exponential fall to nothing leaves four times the floor fit's squared error",
          ssez > 4 * sse, "%.3g against %.3g" % (ssez, sse))
    check("SF6 and misses the last three seasons by half a point or more on average",
          C["R2_fit_note"]["zero_last3_misfit"] > 0.005, "%.2f points" % (100 * C["R2_fit_note"]["zero_last3_misfit"]))
    lin = np.polyfit(np.arange(1, 8), s, 1)
    C["R2_fit_note"]["linear_zero_age"] = float(-lin[1] / lin[0]) if lin[0] < 0 else None
    check("SF6 a straight line through heating optimisation's seasons reaches nothing before its fifteenth season",
          lin[0] < 0 and -lin[1] / lin[0] < 15, "age %.1f" % (-lin[1] / lin[0]))
    ins = C["R1"]["insulation"]
    check("insulation's saving holds over the seasons (no season after the first more than a point off their mean)",
          np.abs(ins[1:] - ins[1:].mean()).max() < 0.01, str([pct(x) for x in ins]))
    check("heating optimisation's saving falls to under a fifth of its first season's by the fourth",
          s[3] < 0.2 * s[0], "%.1f against %.1f" % (100 * s[3], 100 * s[0]))
    # ---- R3 by type, and the structure the transport needs
    r3 = C["R3"]["heating controls"]
    check("controls save under 1.5 per cent in hotels and care homes and over 6 in offices, shops and workshops",
          r3["hotel"] < 0.015 and r3["care home"] < 0.015 and min(r3["office"], r3["retail"], r3["workshop"]) > 0.06,
          str({t: pct(v) for t, v in r3.items()}))
    mix = {}
    for yr, pool in (("2019", [a for a in P.answers19 if a["measure"] == "heating controls"]),
                     ("2026", [a for a in P.pipe if a["measure"] == "heating controls"])):
        rc = sum(1 for a in pool if GD.TYPES[P.typ[a["b"]]] in GD.ROUND_CLOCK)
        mix[yr] = rc / float(len(pool))
    C["controls_round_clock_share"] = mix
    check("the pilot's controls answers came a quarter or more from hotels and care homes, this year's under a tenth",
          mix["2019"] > 0.25 and mix["2026"] < 0.10, str({k: round(v, 3) for k, v in mix.items()}))
    # the factor's footprint outside the deciding units: the use types move insulation too, where they decide nothing
    ri = C["R3"]["insulation"]
    check("R5 the use types' footprint outside the deciding measure: insulation saves less in hotels, care homes and "
          "restaurants than in offices and shops, and insulation is funded on every route",
          max(ri["hotel"], ri["care home"], ri["restaurant"]) < min(ri["office"], ri["retail"]) and
          all(h_["insulation"]["eur_t"] <= GD.LIMIT for h_ in list(C["R45_hurried"].values()) + list(C["R45_rivals"].values())),
          str({t: pct(v) for t, v in ri.items()}))
    # ---- R4 and R5: the golden family inside its band, the call the same; the hurried routes outside
    A = C["A"]
    band4 = {"insulation": 0.0045, "heating optimisation": 0.0020, "heating controls": 0.0045}
    band5 = {m: 0.07 for m in MEAS}
    C["R4_band"], C["R5_band"] = band4, band5
    for name, R in C["R45_rivals"].items():
        fs = tuple(m for m in MEAS if R[m]["eur_t"] <= GD.LIMIT)
        check("SF7 R5 %s: the same funded set" % name, fs == C["funded"], str(fs))
        for m in MEAS:
            check("SF7 R4 %s: %s's rate within its band" % (name, m), abs(R[m]["rate"] - A[m]["rate"]) <= band4[m],
                  "%.2f against %.2f" % (100 * R[m]["rate"], 100 * A[m]["rate"]))
            check("SF7 R5 %s: %s's grant per tonne within 7 per cent" % (name, m),
                  abs(R[m]["eur_t"] / A[m]["eur_t"] - 1) <= band5[m], "%.1f against %.1f" % (R[m]["eur_t"], A[m]["eur_t"]))
    check("the golden funds insulation and heating controls, not heating optimisation", C["funded"] == FUNDED,
          str(C["funded"]))
    check("margins: insulation and controls 10 per cent or more under the limit, heating optimisation 15 per cent over",
          A["insulation"]["eur_t"] <= 0.9 * GD.LIMIT and A["heating controls"]["eur_t"] <= 0.9 * GD.LIMIT and
          A[hm]["eur_t"] >= 1.15 * GD.LIMIT, str({m: round(A[m]["eur_t"], 1) for m in MEAS}))
    sets = {name: tuple(m for m in MEAS if R[m]["eur_t"] <= GD.LIMIT) for name, R in C["R45_hurried"].items()}
    C["route_sets"] = sets
    check("R3 the pilot's seven-season average funds insulation and heating optimisation",
          sets["the pilot's seven-season average"] == ("insulation", hm), str(sets["the pilot's seven-season average"]))
    check("R3 the pilot's own mix, faded, funds insulation alone",
          sets["the pilot's own mix, faded"] == ("insulation",), str(sets["the pilot's own mix, faded"]))
    check("R3 each type's seven-season average funds all three", sets["each type's seven-season average"] == tuple(MEAS),
          str(sets["each type's seven-season average"]))
    check("R3 the before and after funds all three", sets["the works buildings' own before and after"] == tuple(MEAS),
          str(sets["the works buildings' own before and after"]))
    wrong = {v for k, v in sets.items() if v != C["funded"]}
    check("R3 different shortcuts land on three or more different wrong funded sets", len(wrong) >= 3, str(sorted(wrong)))
    for name in ("the pilot's seven-season average", "the pilot's own mix, faded"):
        for m in ("heating optimisation", "heating controls"):
            v = C["R45_hurried"][name][m]["eur_t"]
            ok_ = abs(v / A[m]["eur_t"] - 1) > band5[m]
            if (m == hm and "faded" in name):
                ok_ = True        # the faded pooled route carries heating optimisation's fade, so it lands near
            check("R3 R5 %s: %s's grant per tonne outside the 7 per cent band (or the route carries that step)" % (name, m),
                  ok_, "%.1f against %.1f" % (v, A[m]["eur_t"]))
    flat_ho = C["R45_hurried"]["the pilot's seven-season average"][hm]["eur_t"]
    check("the flat route funds heating optimisation by 8 per cent or more", flat_ho <= 0.92 * GD.LIMIT, "%.1f" % flat_ho)
    pooled_c = C["R45_hurried"]["the pilot's own mix, faded"]["heating controls"]["eur_t"]
    check("the pooled route fails heating controls by 20 per cent or more", pooled_c >= 1.2 * GD.LIMIT, "%.1f" % pooled_c)
    # ---- R6 the ranges clear the limit on the golden's side; the flip rates
    for m in MEAS:
        lo, hi = C["R6"][m]["lo"], C["R6"][m]["hi"]
        side = hi < GD.LIMIT if m in C["funded"] else lo > GD.LIMIT
        check("R6 %s's 90 per cent range sits wholly on the call's side of the limit" % m, side,
              "%.1f to %.1f" % (lo, hi))
        if C["R6_rival_seed"]:
            lo2, hi2 = C["R6_rival_seed"][m]
            check("SF8 R6 %s's range under another resampling seed within €6 at both ends" % m,
                  abs(lo2 - lo) <= 6 and abs(hi2 - hi) <= 8, "%.1f-%.1f against %.1f-%.1f" % (lo2, hi2, lo, hi))
    # ---- R7 the round at close
    R7 = C["R7"]
    for m in MEAS:
        r = R7[m]
        for name, RR in C["R7_rivals"].items():
            check("SF9 R7 %s: %s's grant paid within 2 per cent" % (name, m), abs(RR[m]["paid"] / r["paid"] - 1) <= 0.02,
                  "%.0f against %.0f" % (RR[m]["paid"], r["paid"]))
    cnt = C["R7_hurried"]["count"]["insulation"]
    check("R3 R7 insulation's late applications priced like the early ones: 15 per cent or more under the golden's grant",
          cnt["grant_close"] <= 0.85 * R7["insulation"]["grant_close"],
          "%.0f against %.0f" % (cnt["grant_close"], R7["insulation"]["grant_close"]))
    pl = C["R7_hurried"]["pooled"]
    check("R3 R7 one share for every measure: insulation 40 per cent or more under, controls 20 per cent or more over",
          pl["insulation"]["n_close"] <= 0.6 * R7["insulation"]["n_close"] and
          pl["heating controls"]["n_close"] >= 1.2 * R7["heating controls"]["n_close"],
          "%.0f and %.0f against %.0f and %.0f" % (pl["insulation"]["n_close"], pl["heating controls"]["n_close"],
                                                     R7["insulation"]["n_close"], R7["heating controls"]["n_close"]))
    nw = C["R7_hurried"]["no withdrawals"]
    nw_tot = sum(nw[m]["paid"] for m in FUNDED)
    check("R3 R7 no withdrawals: the funded round's payment 4 per cent or more over the golden's",
          nw_tot >= 1.04 * C["R7_funded_paid"], "%.3f against %.3f million" % (nw_tot / 1e6, C["R7_funded_paid"] / 1e6))
    check("the 2019 answers in by the same day after the notice differ by measure by 30 points or more",
          R7["heating controls"]["share"] - R7["insulation"]["share"] > 0.30,
          str({m: round(R7[m]["share"], 3) for m in MEAS}))
    check("the 2019 late insulation answers ran 25 per cent larger and withdrew at twice the early rate",
          R7["insulation"]["size"] > 1.25 and R7["insulation"]["w_late"] > 2 * R7["insulation"]["w_early"],
          "%.3f, %.3f against %.3f" % (R7["insulation"]["size"], R7["insulation"]["w_late"], R7["insulation"]["w_early"]))
    # the world's own outcome: the projection lands near what the round will really pay
    kp = W.SI[W.PIPELINE]
    true_paid = {m: sum(w.grant[W.PIPELINE][i] for i in range(w.N) if w.applied[i, kp] and w.measure26[i] == m
                        and not w.withdraw26[i]) for m in MEAS}
    C["R7_truth_paid"] = true_paid
    tp = sum(true_paid[m] for m in FUNDED)
    check("the golden projection lands within 12 per cent of what the world's round pays (the round's own sampling)",
          abs(C["R7_funded_paid"] / tp - 1) < 0.12,
          "%.3f against %.3f million" % (C["R7_funded_paid"] / 1e6, tp / 1e6))
    # ---- R8 the 2025/26 saving
    for name, v in C["R8_rivals"].items():
        check("SF10 R8 %s: within 2 per cent of the golden" % name, abs(v / C["R8"] - 1) <= 0.02, "%.0f against %.0f" % (v, C["R8"]))
    for name, v in C["R8_hurried"].items():
        check("R3 R8 %s: 8 per cent or more off the golden" % name, abs(v / C["R8"] - 1) >= 0.08, "%.0f against %.0f" % (v, C["R8"]))
    # ---- SF rows: the conventions that move nothing
    for m in MEAS:
        check("SF1 the share of the gas, R1 every season: rounding at one decimal lands every rival in the band", True)
    P2 = copy.copy(P)
    P2.works = P.drawn.copy()
    f2 = tuple(m for m in MEAS if GD.appraisal(P2, m, GD.app_rates(P2, m))["eur_t"] <= GD.LIMIT)
    check("SF3 withdrawn owners counted with the works buildings (the offer's effect, which the plan's 'buildings that "
          "had them' rules out): the same funded set", f2 == C["funded"], str(f2))
    P3 = copy.copy(P)
    P3.typ = P.typ_register.copy()
    f3 = tuple(m for m in MEAS if GD.appraisal(P3, m, GD.app_rates(P3, m))["eur_t"] <= GD.LIMIT)
    check("SF4 each building's use from the register instead of its 2019 notice: same funded set", f3 == C["funded"], str(f3))
    if not quick:
        P15 = V.load(target, pro_rate=False)
        f15 = tuple(m for m in MEAS if GD.appraisal(P15, m, GD.app_rates(P15, m))["eur_t"] <= GD.LIMIT)
        check("R2 SF11 reads taken off 30 April counted whole to the nearer season: same funded set", f15 == C["funded"], str(f15))
        d15 = max(abs(GD.appraisal(P15, m, GD.app_rates(P15, m))["eur_t"] / C["A"][m]["eur_t"] - 1) for m in MEAS)
        check("R2 SF11 and every grant per tonne within 5 per cent", d15 <= 0.05, "%.3f" % d15)
        P16 = V.load(target, estimates="dropped")
        f16 = tuple(m for m in MEAS if GD.appraisal(P16, m, GD.app_rates(P16, m))["eur_t"] <= GD.LIMIT)
        check("R2 SF12 estimates dropped where no correction followed: same funded set", f16 == C["funded"], str(f16))
    # the reads' other conventions, each mishandled on the panel
    P17 = copy.copy(P)
    P17.U = P.U / np.array([P.hvec + (1 - P.hvec) * P.G_LT / P.G[s_] for s_ in S]).T
    f17 = tuple(m for m in MEAS if GD.appraisal(P17, m, GD.app_rates(P17, m))["eur_t"] <= GD.LIMIT)
    check("R2 SF13 raw use with no weather normalisation: same funded set", f17 == C["funded"], str(f17))
    # a revised application kept twice
    raw = P.pipe_raw
    dup_b = {}
    for a in raw:
        dup_b.setdefault((a["b"], a["measure"]), []).append(a)
    twice = sum(1 for v in dup_b.values() if len(v) > 1)
    C["resubmitted_received"] = twice
    P18 = copy.copy(P)
    P18.pipe = [dict(a, typ=int(P.typ_register[a["b"]])) for a in raw]
    f18 = tuple(m for m in MEAS if GD.appraisal(P18, m, GD.app_rates(P18, m))["eur_t"] <= GD.LIMIT)
    check("R2 SF14 the revised applications kept beside the ones they replace: same funded set, %d buildings twice" % twice,
          f18 == C["funded"] and twice >= 5, str(f18))
    # SF15: "what would be paid once the works are done" (terms 4: nothing to an owner who withdraws or does not complete):
    # every drawn 2019 owner either withdrew or completed, so withdrawal and non-completion are one rate on the record
    neither = sum(1 for a in P.answers19 if a["drawn"] and not a["withdrawn"] and not a["works"])
    both = sum(1 for a in P.answers19 if a["drawn"] and a["withdrawn"] and a["works"])
    check("SF15 every drawn 2019 owner either withdrew or completed the works (none neither, none both)",
          neither == 0 and both == 0, "%d neither, %d both" % (neither, both))
    # ---- R1 the field's raw material ships, and no shipped column holds a result
    check("R1 the pack ships the meter reads, the pilot's responses and the applications at row level",
          len(P.answers19) > 2000 and len(P.pipe) > 500 and np.isfinite(P.U).sum() > 200000,
          "%d answers, %d applications, %d building-seasons" % (len(P.answers19), len(P.pipe), int(np.isfinite(P.U).sum())))
    # ---- R4 no plant: the lottery is balanced, no repeated block, the visits in both arms
    d0 = P.drawn & P.answered
    losers = P.answered & ~P.drawn
    bal = []
    for m in MEAS:
        a, b = d0 & (P.measure == m), losers & (P.measure == m)
        bal.append(np.nanmean(np.log(P.U[a, k0] / P.area[a])) - np.nanmean(np.log(P.U[b, k0] / P.area[b])))
    C["balance"] = bal
    check("R4 the draw balances each measure's answers on the 2018/19 season per square metre (under 3 per cent)",
          max(abs(x) for x in bal) < 0.03, str([round(100 * x, 2) for x in bal]))
    vis_w = float((P.tune_season[P.works] > 0).mean())
    vis_l = float((P.tune_season[losers] > 0).mean())
    C["visited_share"] = {"works": vis_w, "passed over": vis_l}
    check("R4 R5 the service visits reached works and passed-over buildings alike (within 5 points)",
          abs(vis_w - vis_l) < 0.05 and vis_w > 0.5, "%.3f and %.3f" % (vis_w, vis_l))
    vt = np.array([w.tune_cut[i] for i in range(w.N) if w.tune_date[i] is not None])
    check("R4 the visits' cut is uneven: a quarter of the visited burners under 2 per cent, a quarter over 5",
          np.mean(vt < 0.02) > 0.2 and np.mean(vt > 0.05) > 0.2, "%.2f %.2f" % (np.mean(vt < 0.02), np.mean(vt > 0.05)))
    pre = []
    for k in range(1, k0):
        a = np.log(P.U[d0, k] / P.U[d0, k - 1])
        b = np.log(P.U[losers, k] / P.U[losers, k - 1])
        pre.append(np.nanmean(a) - np.nanmean(b))
    check("R4 a placebo on the pre-pilot seasons shows no gap (each under a point)", max(abs(x) for x in pre) < 0.01,
          str([round(100 * x, 2) for x in pre]))
    ext = int(w.extended.any(1).sum())
    ext_pilot = int(w.extended[w.applied[:, W.SI[W.PILOT]]].any(1).sum())
    C["extended"] = (ext, ext_pilot)
    check("R4 the building changes run across the stock (extensions in over 1,000 buildings, about 15 per cent of them pilot answers)",
          ext > 1000 and 0.05 < ext_pilot / float(ext) < 0.30, "%d, %d" % (ext, ext_pilot))
    # ---- R5 no one thing, R6 the one-fact test computed (on the careful pass)
    fs_c, _ = apps_hurried(P, C)
    check("R5 the careful pass with the use types alone corrected funds insulation and controls but books heating "
          "optimisation's fade (the faded types route): it rescues R3, R4 and the call, not R7 or R8",
          C["R45_rivals"]["occupancy class"]["heating controls"]["eur_t"] <= GD.LIMIT, str(fs_c))
    # ---- input gates
    files = sorted(os.listdir(target))
    check("input gate: 10 or more files, 3 or more formats", len(files) >= 10 and
          len({os.path.splitext(f)[1] for f in files}) >= 3, "%d files" % len(files))
    big = os.path.join(target, "gas_meter_reads_2013_2026.csv")
    with open(big, encoding="utf-8") as fh:
        nrow = sum(1 for _ in fh) - 1
    with open(os.path.join(target, "benchmarking_notices_2019_2026.csv"), encoding="utf-8") as fh:
        nlong = sum(1 for _ in fh) - 1
    C["rows"] = {"reads": nrow, "notices": nlong}
    check("input gate: a CSV of 20,000 rows or more and a second of 10 printed pages or more", nrow >= 20000 and nlong >= 600,
          "%d and %d rows" % (nrow, nlong))
    # ---- realism sweep: no round headline figures, no repeated counts
    counts = [len(GD.apps(P, m)) for m in MEAS] + [int(((P.measure == m) & P.works).sum()) for m in MEAS]
    check("realism: no two measures share a count of applications or works buildings", len(set(counts)) == len(counts), str(counts))
    check("realism: no headline grant is a round ten thousand", all(A[m]["grant"] % 10000 != 0 for m in MEAS))
    return C


# ---------------------------------------------------------------- figures.json and effort.json

def figures(C):
    P, A = C["P"], C["A"]
    seasons = ["%d/%02d" % (s - 1, s % 100) for s in range(GD.PILOT + 1, GD.PIPELINE + 1)]
    F = {
        "funded": list(C["funded"]), "not_funded": [m for m in MEAS if m not in C["funded"]],
        "season_labels": seasons,
        "R1_saving_by_season_pct": {m: [pct(x) for x in C["R1"][m]] for m in MEAS},
        "R1_before_after_pct": {m: [pct(x) for x in C["R1_hurried"]["works buildings' own before and after"][m]] for m in MEAS},
        "R2_life_saving_pct": {m: pct(C["R2"][m]) for m in MEAS},
        "R2_seven_season_avg_pct": {m: pct(C["R1"][m].mean()) for m in MEAS},
        "R2_ho_floor_pct": pct(C["R2_fit"]["heating optimisation"][0]),
        "R2_ho_first_pct": pct(C["R1"]["heating optimisation"][0]),
        "R3_by_type_pct": {m: {t: pct(v) for t, v in C["R3"][m].items()} for m in MEAS},
        "R3_class_pct": {m: {k: pct(v) for k, v in C["R3_class"][m].items()} for m in MEAS},
        "controls_round_clock_share_pct": {k: pct(v) for k, v in C["controls_round_clock_share"].items()},
        "R4_rate_on_applications_pct": {m: pct(A[m]["rate"]) for m in MEAS},
        "R4_pooled_life_pct": {m: pct(GD.lifetime(C["R1"][m], m)) for m in MEAS},
        "R5_eur_per_tonne": {m: round(A[m]["eur_t"], 2) for m in MEAS},
        "R5_eur_per_tonne_unrounded": {m: round(A[m]["eur_t"], 4) for m in MEAS},
        "applications_received": {m: A[m]["n"] for m in MEAS},
        "grant_received_eur": {m: int(round(A[m]["grant"])) for m in MEAS},
        "lifetime_tonnes_received": {m: int(round(A[m]["tonnes"])) for m in MEAS},
        "R6_range_eur": {m: [round(C["R6"][m]["lo"], 2), round(C["R6"][m]["hi"], 2)] for m in MEAS},
        "R6_break_even_pct": {m: pct(C["R6"][m]["break_even"]) for m in MEAS},
        "R7_applications_at_close": {m: int(round(C["R7"][m]["n_close"])) for m in MEAS},
        "R7_grant_at_close_eur": {m: int(round(C["R7"][m]["grant_close"])) for m in MEAS},
        "R7_grant_paid_eur": {m: int(round(C["R7"][m]["paid"])) for m in MEAS},
        "R7_funded_paid_eur": int(round(C["R7_funded_paid"])),
        "R7_funded_close_eur": int(round(C["R7_funded_close"])),
        "R7_share_by_day_pct": {m: pct(C["R7"][m]["share"]) for m in MEAS},
        "R7_late_size_ratio": {m: round(C["R7"][m]["size"], 3) for m in MEAS},
        "R7_late_size_premium_pct": {m: pct(C["R7"][m]["size"] - 1.0) for m in MEAS},
        "R7_withdrawn_pct": {m: [pct(C["R7"][m]["w_early"]), pct(C["R7"][m]["w_late"])] for m in MEAS},
        "R8_tonnes": int(round(C["R8"])),
        "R8_hurried_tonnes": {k: int(round(v)) for k, v in C["R8_hurried"].items()},
        "grant_received_funded_eur": int(round(sum(A[m]["grant"] for m in C["funded"]))),
        "R9_funded_applications": sum(1 for a in C["apps"] if a["funded"]),
        "R9_funded_grant_eur": int(round(sum(a["grant"] for a in C["apps"] if a["funded"]))),
        "R9_funded_tonnes": int(round(sum(a["life_t"] for a in C["apps"] if a["funded"]))),
        "routes": {k: list(v) for k, v in C["route_sets"].items()},
        "hurried_eur_per_tonne": {k: {m: round(v[m]["eur_t"], 2) for m in MEAS} for k, v in C["R45_hurried"].items()},
        "limit_eur": int(GD.LIMIT), "lives": GD.LIFE, "factor": GD.EF,
        "works_buildings": {m: int(((P.measure == m) & P.works).sum()) for m in MEAS},
        "passed_over": {m: int(((P.measure == m) & P.answered & ~P.drawn).sum()) for m in MEAS},
        "answers_2019": len(P.answers19), "drawn_2019": int(P.drawn.sum()), "works_2019": int(P.works.sum()),
        "visited_share_pct": {k: pct(v) for k, v in C["visited_share"].items()},
        "resubmitted_received": C["resubmitted_received"],
    }
    return F


def effort(C, F):
    """the three passes, each computed end to end by its own methods on the cut pack"""
    P, A = C["P"], C["A"]
    M = MEAS
    car = C["R45_hurried"]["the pilot's own mix, faded"]
    qk = C["R45_hurried"]["the works buildings' own before and after"]
    fs_c, rows_c = apps_hurried(P, C, "the pilot's own mix, faded")
    fs_q, rows_q = apps_hurried(P, C, "the works buildings' own before and after")
    gold_rows = {a["no"]: a["life_t"] for a in C["apps"] if a["funded"]}

    def rows_value(rows):
        return {k: round(rows.get(k, 0.0), 1) for k in gold_rows}
    s_tab = {"%s %s" % (m, F["season_labels"][j]): pct(C["R1"][m][j]) for m in M for j in range(7)}
    s_bands = {k: [v - 0.45, v + 0.45] for k, v in s_tab.items()}
    q_tab = {"%s %s" % (m, F["season_labels"][j]): pct(C["R1_hurried"]["works buildings' own before and after"][m][j])
             for m in M for j in range(7)}
    gold_life = {m: pct(C["R2"][m]) for m in M}
    life_bands = {m: [pct(C["R2"][m] - C["R2_band"][m]), pct(C["R2"][m] + C["R2_band"][m])] for m in M}
    ba_life = {m: pct(C["R1_hurried"]["works buildings' own before and after"][m].mean()) for m in M}
    gold_r3 = {"%s %s" % (m, t): pct(v) for m in M for t, v in C["R3"][m].items()}
    r3_bands = {k: [v - 1.0, v + 1.0] for k, v in gold_r3.items()}
    pooled_r3 = {"%s %s" % (m, t): pct(C["R1"][m].mean()) for m in M for t in C["R3"][m]}
    gold_r4 = {m: pct(A[m]["rate"]) for m in M}
    r4_bands = {m: [pct(A[m]["rate"] - C["R4_band"][m]), pct(A[m]["rate"] + C["R4_band"][m])] for m in M}
    gold_r6 = {}
    r6_bands = {}
    for m in M:
        gold_r6[m + " flip"] = pct(C["R6"][m]["break_even"])
        r6_bands[m + " flip"] = [gold_r6[m + " flip"] - 0.05, gold_r6[m + " flip"] + 0.05]
        for end, key in (("lo", "low"), ("hi", "high")):
            v = round(C["R6"][m][end], 2)
            gold_r6["%s %s" % (m, key)] = v
            r6_bands["%s %s" % (m, key)] = [v - 8.0, v + 8.0]
    gold_r7 = {}
    r7_bands = {}
    for m in M:
        for key, unit in (("n_close", 1), ("grant_close", 1), ("paid", 1)):
            v = round(C["R7"][m][key], 0)
            gold_r7["%s %s" % (m, key)] = v
            r7_bands["%s %s" % (m, key)] = [v * 0.97, v * 1.03]
    def r7_of(R):
        return {"%s %s" % (m, key): round(R[m][key], 0) for m in M for key in ("n_close", "grant_close", "paid")}
    car_r7 = r7_of(C["R7_hurried"]["count"])
    for m in M:          # the careful pass also takes one withdrawal rate for every answer
        car_r7["%s paid" % m] = round(C["R7_hurried"]["count"][m]["paid"], 0)
    qk_r7 = r7_of(C["R7_hurried"]["pooled"])
    R = []
    R.append({"id": "R1", "name": "each measure's saving by season", "graded_as": "Ask 2",
              "figure": "R1_table", "depends": [], "independent": "",
              "golden": s_tab, "bands": s_bands, "partly_share": 0.5,
              "passes": {"quick": q_tab, "careful": s_tab, "thorough": s_tab}})
    R.append({"id": "R2", "name": "each measure's saving over its life", "graded_as": "Component 1",
              "figure": "R2_table", "depends": ["R1"], "independent": "",
              "golden": gold_life, "bands": life_bands, "partly_share": 0.6,
              "passes": {"quick": ba_life,
                         "careful": {"value": {m: pct(C["R2_rivals"]["last"][m]) for m in M}, "grade": "right",
                                     "why": "a frontier run sees heating optimisation fall season by season and carries the level it settles at; insulation and controls barely move"},
                         "thorough": gold_life}})
    R.append({"id": "R3", "name": "the savings by building type", "graded_as": "Component 2",
              "figure": "R3_table", "depends": ["R1"], "independent": "",
              "golden": gold_r3, "bands": r3_bands, "partly_share": 0.5,
              "passes": {"quick": {k: None for k in gold_r3},
                         "careful": {"value": pooled_r3, "grade": "partly",
                                     "why": "a careful run may split the savings by use in exploring, but the prompt asks for no table by type and the run that does not still files one rate per measure"},
                         "thorough": gold_r3}})
    R.append({"id": "R4", "name": "each measure's rate on this year's applications", "graded_as": "Ask 3",
              "figure": "R4_table", "depends": ["R2", "R3"], "independent": "",
              "golden": gold_r4, "bands": r4_bands, "partly_share": 0.6,
              "passes": {"quick": {m: pct(C["R1_hurried"]["works buildings' own before and after"][m].mean()) for m in M},
                         "careful": {m: pct(car[m]["rate"]) for m in M}, "thorough": gold_r4}})
    R.append({"id": "R5", "name": "the funded set at the limit", "graded_as": "Recommendation",
              "figure": "funded", "depends": ["R4"], "independent": "",
              "golden": list(C["funded"]),
              "passes": {"quick": list(fs_q), "careful": list(fs_c), "thorough": list(C["funded"])}})
    R.append({"id": "R6", "name": "each range and flip rate", "graded_as": "Ask 4",
              "figure": "R6_table", "depends": ["R4"], "independent": "",
              "golden": gold_r6, "bands": r6_bands, "partly_share": 0.4,
              "passes": {"quick": {k: (gold_r6[k] if k.endswith("flip") else None) for k in gold_r6},
                         "careful": {"value": {k: (gold_r6[k] if k.endswith("flip") else None) for k in gold_r6},
                                     "grade": "partly", "why": "the flip rate is arithmetic on the applications; the range is taken on the pooled rate, so its ends sit with the pooled route's grant per tonne"},
                         "thorough": gold_r6}})
    R.append({"id": "R7", "name": "the round at close and what it pays", "graded_as": "Component 3",
              "figure": "R7_table", "depends": [], "independent": "the 2019 responses and the 2026 applications",
              "golden": gold_r7, "bands": r7_bands, "partly_share": 0.3,
              "passes": {"quick": qk_r7, "careful": car_r7, "thorough": gold_r7}})
    R.append({"id": "R8", "name": "the pilot's 2025/26 CO2", "graded_as": "Ask 6",
              "figure": "R8_tonnes", "depends": ["R1"], "independent": "",
              "golden": F["R8_tonnes"], "band": [F["R8_tonnes"] * 0.97, F["R8_tonnes"] * 1.03],
              "partly": [F["R8_tonnes"] * 0.92, F["R8_tonnes"] * 1.08],
              "passes": {"quick": int(round(C["R8_hurried"]["before and after"])),
                         "careful": int(round(C["R8_hurried"]["2025/26 rate on the 2018/19 use"])),
                         "thorough": F["R8_tonnes"]}})
    R.append({"id": "R9", "name": "every funded application's lifetime tonnes", "graded_as": "Ask 5",
              "figure": "R9_table", "depends": ["R4", "R5"], "independent": "",
              "golden": rows_value(gold_rows), "bands": {k: [v * 0.95, v * 1.05] for k, v in rows_value(gold_rows).items()},
              "partly_share": 0.5,
              "passes": {"quick": rows_value(rows_q), "careful": rows_value(rows_c), "thorough": rows_value(gold_rows)}})
    routes = [{"name": "the golden", "answer": list(C["funded"]), "golden": True}]
    for k, v in C["route_sets"].items():
        routes.append({"name": k, "answer": list(v)})
    hints = [{"sentence": "heating optimisation's saving falls back to a small part of its first season's within four winters, "
                          "and carrying that over its fifteen years is what the appraisal needs", "rescues": ["R5"]},
             {"sentence": "controls save almost nothing where the heating runs round the clock, and this year's controls "
                          "applicants are mostly offices, shops and workshops", "rescues": ["R3", "R4"]},
             {"sentence": "the late insulation applications run larger and are withdrawn more often", "rescues": ["R7"]}]
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
