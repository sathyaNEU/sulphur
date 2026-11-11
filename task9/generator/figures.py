"""task9: every figure the answer blocks, the deck and effort.json state, computed by analysis.py from the cut pack,
with the golden family of rival methods behind each band and the fitted inputs' perturbations behind the call.

    compute(tgt) -> F     write(F, path) -> figures.json
"""
import json

import numpy as np
import pandas as pd

import analysis as AN

UNITS = AN.UNITS


def r(x, n=0):
    return None if x is None or x != x else (round(float(x), n) if n else int(round(float(x))))


def counts_of(A, fits):
    return {u: A.tstar(fits[A.pair_of[u]] if isinstance(fits, dict) and A.pair_of[u] in fits else fits) for u in UNITS}


def compute(tgt):
    A = AN.Analysis(tgt)
    o = A.routes()
    d, w = A.d, A.d[A.d.win]
    F = {"pairs": A.pairs, "V": A.V, "n_window": A.n_win, "allin": A.allin}

    # ---------------------------------------------------------------- the golden, as computed
    G = {
        "R1_points": A.R1, "R2_die": dict(A.R2), "R2_usd": A.R2_usd, "R1_q1": A.R1_q1, "unflagged_share": A.unflagged_share,
        "R3_shares": dict(A.R3), "R4_dose": {u: {"onset": A.onset[u], "slope": A.slope[u]} for u in UNITS},
        "R5_bridge": dict(A.R5), "R5_L": dict(A.L), "R6_counts": dict(A.R6), "R7_saving": A.R7, "R7_unit": dict(A.R7_unit),
        "pair_fit": {p: dict(f) for p, f in A.pair_fit.items()}, "gamma": {p: f["gamma"] for p, f in A.pair_fit.items()},
        "r0": dict(A.r0), "ring_swaps": A.ring_swaps, "ring_t": o["R3_joint_ring_t"], "life": {
            p: {"w0": f["w0"], "ring": f["ring"], "n_lives": len(f["betas"]), "betas": {k: v * 1000 for k, v in f["betas"].items()}}
            for p, f in A.life.items()},
    }
    F["gold"] = G

    # ---------------------------------------------------------------- the stated figures (the answer blocks' precision)
    S = {
        "R1_points": r(A.R1, 2),
        "R2_die": {p: int(round(v, -3)) for p, v in A.R2.items()},
        "R3_shares": {k: r(v, 3) for k, v in A.R3.items()},
        "R4_dose": dict(sum([[("%s onset" % u, int(round(A.onset[u], -1))), ("%s slope" % u, r(A.slope[u] * 100, 1))] for u in UNITS], [])),
        "R5_bridge": {k: r(v, 2) for k, v in A.R5.items()},
        "R6_counts": {u: int(round(v, -1)) for u, v in A.R6.items()},
        "R7_saving": int(round(A.R7, -3)),
    }
    S["R2_usd"] = int(round(A.R2_usd, -3))
    F["stated"] = S

    # ---------------------------------------------------------------- the golden family: rival methods run on the pack
    riv = {}
    # R1, R2: the band's normal fallout read other ways
    def loss_with(r0map):
        die = d.f_band * d.tested_band - d.tested_band * (d.f_in + r0map)
        ww = die[d.win]
        sub = d[d.win]
        return float(np.mean(ww / sub.gross) * 100), {p: float(v) for p, v in ww.groupby(sub["product"]).sum().items()}
    fresh = d[d.disk < 600]
    riv["R1"] = {}
    riv["R1"]["the band's excess on wafers under 600 wafers of disk use, by pair"] = loss_with(d.pair.map(fresh.groupby("pair").y.mean()))
    riv["R1"]["the same by product"] = loss_with(d["product"].map(fresh.groupby("product").y.mean()))
    riv["R1"]["the disk-life model's intercept"] = loss_with(d.pair.map({p: f["r0"] for p, f in A.life.items()}))
    riv["R1"]["an unweighted fit's intercept"] = loss_with(d.pair.map({p: AN.hinge_fit(d[d.pair == p], weight=False)["r0"] for p in A.pairs}))
    riv["R1"]["one fallout for the fab"] = loss_with(pd.Series(float(np.average(fresh.y, weights=fresh.tested_band)), index=d.index))
    # R3: the shares with the ring held at what the swaps show, and from the pair fit with the rivals
    riv["R3"] = {}
    contrib = {k: 0.0 for k in AN.CAUSES}
    for p in A.pairs:
        g = d[d.pair == p]
        f = AN.hinge_fit(g, extra=AN.RIVALS)
        gw = w[w.pair == p]
        h = np.maximum(0.0, gw.disk.values - f["w0"])
        sc = gw.tested_band.values / gw.gross.values * 100 / len(w)
        contrib["disk"] += float(np.sum(f["beta"] * h * sc))
        contrib["pad"] += float(np.sum(f["beta"] * f["gamma"] * h * gw.pad.values / AN.PAD_LIFE * sc))
        contrib["dep3"] += float(np.sum(f["dep3"] * gw.dep3.values * sc))
        contrib["sc4"] += float(np.sum(f["sc4"] * gw.sc4.values * sc))
        contrib["rf"] += float(np.sum(f["rf100"] * (gw.rf100.values - g.rf100.min()) * sc))
    tot = contrib["disk"] + contrib["pad"]
    riv["R3"]["the ring left out once its swaps show no step"] = {k: v / tot for k, v in contrib.items()}
    j = dict(o["R3_joint"])
    clustered_t = max(abs(t[1]) for t in o["R3_joint_ring_t"].values())
    j["ring"] = 0.0 if clustered_t < 2.0 else j["ring"]
    riv["R3"]["the joint fit with the ring tested on its disk lives"] = j
    # R4: per unit, unweighted, with the ring term, below 2,800 wafers
    riv["R4"] = {
        "each unit's own fit": {u: {"onset": A.unit_fit[u]["w0"], "slope": A.unit_fit[u]["beta"] * 1000} for u in UNITS},
        "an unweighted pair fit": None, "the pair fit with the ring's usage beside it": None, "the pair fit below 2,800 wafers": None}
    alt = {"an unweighted pair fit": {p: AN.hinge_fit(d[d.pair == p], weight=False) for p in A.pairs},
           "the pair fit with the ring's usage beside it": {p: AN.hinge_fit(d[d.pair == p], ring=True) for p in A.pairs},
           "the pair fit below 2,800 wafers": {p: AN.hinge_fit(d[(d.pair == p) & (d.disk < 2800)]) for p in A.pairs}}
    for k, fits in alt.items():
        riv["R4"][k] = {u: {"onset": fits[A.pair_of[u]]["w0"], "slope": fits[A.pair_of[u]]["beta"] * 1000} for u in UNITS}
    # R5: the bridge on other fits and conventions
    riv["R5"] = {"the pair fit with the ring's usage beside it": o["R5_ring_term"], "an unweighted pair fit": o["R5_unweighted"],
                 "one fit for the fleet": o["R5_fleet"],
                 "the observed loss for what happened": {"old_rule": A.L["old_rule"] / A.R1, "rev_f": (A.L["rev_f"] - A.L["old_rule"]) / A.R1,
                                                         "ew118": (A.R1 - A.L["rev_f"]) / A.R1}}
    # R6, R7: per unit, the window's mix, the ring term, unweighted, the observed pad age
    riv["R6"] = {"each unit's own fit": o["R6_unit"], "the April to August mix": o["R6_apr_aug_mix"],
                 "the pair fit with the ring's usage beside it": o["R6_joint_ring"],
                 "an unweighted pair fit": {u: A.tstar(alt["an unweighted pair fit"][A.pair_of[u]]) for u in UNITS},
                 "the pair fit below 2,800 wafers": {u: A.tstar(alt["the pair fit below 2,800 wafers"][A.pair_of[u]]) for u in UNITS}}
    sh = A.unit_share()
    riv["R7"] = {"each unit's own fit": o["R7_unit"], "each unit's share of April to August": o["R7_apr_aug"],
                 "an unweighted pair fit": float(sum(A.yearly(alt["an unweighted pair fit"][A.pair_of[u]],
                                                              riv["R6"]["an unweighted pair fit"][u], sh[u]) for u in UNITS)),
                 "the pair fit below 2,800 wafers": float(sum(A.yearly(alt["the pair fit below 2,800 wafers"][A.pair_of[u]],
                                                                       riv["R6"]["the pair fit below 2,800 wafers"][u], sh[u]) for u in UNITS))}
    F["rivals"] = riv

    # ---------------------------------------------------------------- bands: the rivals' spread, held off every shortcut
    B = {}
    B["R1_points"] = [round(S["R1_points"] * 0.93, 2), round(S["R1_points"] * 1.07, 2)]
    B["R2_die"] = {p: [int(round(v * 0.92, -3)), int(round(v * 1.08, -3))] for p, v in S["R2_die"].items()}
    B["R3_shares"] = {"disk": [0.92, 1.0], "pad": [0.0, 0.08], "ring": [-0.025, 0.025], "dep3": [-0.02, 0.02], "sc4": [-0.02, 0.02],
                      "rf": [-0.02, 0.02]}
    B["R4_dose"] = {}
    for u in UNITS:
        on, sl = S["R4_dose"]["%s onset" % u], S["R4_dose"]["%s slope" % u]
        B["R4_dose"]["%s onset" % u] = [int(round(on * 0.85, -1)), int(round(on * 1.15, -1))]
        B["R4_dose"]["%s slope" % u] = [round(sl * 0.85, 1), round(sl * 1.15, 1)]
    B["R5_bridge"] = {k: [round(v - 0.03, 2), round(v + 0.03, 2)] for k, v in S["R5_bridge"].items()}
    B["R6_counts"] = {u: [int(round(v * 0.92, -1)), int(round(v * 1.08, -1))] for u, v in S["R6_counts"].items()}
    B["R7_saving"] = [int(round(S["R7_saving"] * 0.92, -3)), int(round(S["R7_saving"] * 1.08, -3))]
    F["bands"] = B

    # ---------------------------------------------------------------- the passes
    def r4_cells(m):
        out = {}
        for u in UNITS:
            on, sl = (m[u]["onset"], m[u]["slope"]) if isinstance(m[u], dict) else m[u]
            out["%s onset" % u] = int(round(on, -1))
            out["%s slope" % u] = r(sl * 100, 1)
        return out
    thorough = {"R1_points": S["R1_points"], "R2_die": S["R2_die"], "R3_shares": S["R3_shares"],
                "R4_dose": dict(S["R4_dose"]), "R5_bridge": S["R5_bridge"],
                "R6_counts": S["R6_counts"], "R7_saving": S["R7_saving"]}
    careful = {"R1_points": r(o["R1_q1_baseline"], 2), "R2_die": {p: r(v) for p, v in o["R2_q1_baseline"].items()},
               "R3_shares": {k: r(v, 3) for k, v in o["R3_joint"].items()},
               "R4_dose": r4_cells(o["R4_unit"]), "R5_bridge": {k: r(v, 2) for k, v in o["R5_slice"].items()},
               "R6_counts": {u: int(round(v, -1)) for u, v in o["R6_unit"].items()},
               "R7_saving": int(round(o["R7_summer_rate"], -3))}
    quick = {"R1_points": r(o["R1_labels"], 2), "R2_die": {p: r(v) for p, v in o["R2_labels"].items()},
             "R3_shares": {k: (r(v, 3) if k in ("dep3", "sc4") else None) for k, v in o["R3_commonality"].items()},
             "R4_dose": r4_cells(o["R4_pad_counter"]), "R5_bridge": o["R5_all_rev_f"],
             "R6_counts": {u: (None if v != v else int(round(v, -1))) for u, v in o["R6_pad_lever"].items()},
             "R7_saving": None}
    F["passes"] = {"quick": quick, "careful": careful, "thorough": thorough}
    F["routes"] = {k: v for k, v in o.items() if not k.startswith("R3_commonality_pair")}

    # ---------------------------------------------------------------- the call's perturbations
    pert = {}
    for name, mod in (("every slope 20 per cent higher", dict(beta=1.2)), ("every slope 20 per cent lower", dict(beta=0.8)),
                      ("every onset 5 per cent earlier", dict(w0=0.95)), ("every onset 5 per cent later", dict(w0=1.05)),
                      ("the pad's term doubled", dict(gamma=2.0)), ("the pad's term removed", dict(gamma=0.0))):
        fits = {p: dict(f, **{k: f[k] * v for k, v in mod.items()}) for p, f in A.pair_fit.items()}
        pert[name] = {u: A.tstar(fits[A.pair_of[u]]) for u in UNITS}
    for name, V in (("die value at risk 10 per cent higher", A.V * 1.1), ("die value at risk 10 per cent lower", A.V * 0.9)):
        pert[name] = {u: A.tstar(A.pair_fit[A.pair_of[u]], V=V) for u in UNITS}
    for name, c in (("the disk change 10 per cent dearer", A.allin["disk_change"] * 1.1),
                    ("the disk change 10 per cent cheaper", A.allin["disk_change"] * 0.9)):
        pert[name] = {u: A.tstar(A.pair_fit[A.pair_of[u]], c=c) for u in UNITS}
    F["perturbations"] = pert
    # ---------------------------------------------------------------- what the deck shows beside the graded figures
    d["sort_month"] = d.sort_ts.dt.strftime("%Y-%m")
    mo = d[d.sort_ts < "2026-09-01"].groupby("sort_month")
    F["monthly"] = {k: float(np.mean(g.ring_die / g.gross) * 100) for k, g in mo}
    F["monthly_wafers"] = {k: int(len(g)) for k, g in mo}
    bins = {}
    for p in A.pairs:
        g = d[d.pair == p]
        b = (g.disk // 200).astype(int)
        rows = []
        for k, gg in g.groupby(b):
            if len(gg) >= 60:
                rows.append((int(k * 200 + 100), float(np.average(gg.y, weights=gg.tested_band)), int(len(gg))))
        bins[p] = rows
    F["binned"] = bins
    F["fitted"] = {p: [(x, float(A.r0[p] + A.excess(x, AN.PAD_LIFE / 2, A.pair_fit[p]))) for x, _, _ in bins[p]] for p in A.pairs}
    # each pair's cost per wafer under the rules on the table (its maintenance and the ring's yield, dollars)
    full = A.allin["full_pm"]
    cost = {}
    for p in A.pairs:
        f = A.pair_fit[p]
        k = A.k_of(f)
        L = lambda T: k * max(0.0, T - f["w0"]) ** 2 / 2
        u = A.pairs[p][0]
        cost[p] = {"Rev F as it stands": full / 2800 + L(2800) / 2800,
                   "back to Rev E (full PM every 2,000)": full / 2000 + L(2000) / 2000,
                   "Rev G at the pair's count": (full - A.part_price["disk"]) / 2800 + A.cpw(f, A.R6[u]),
                   "Rev G at one fleet count": (full - A.part_price["disk"]) / 2800 + A.cpw(f, o["R6_fleet"][u])}
    F["cost_per_wafer"] = cost
    F["unit_share"] = {u: float(v) for u, v in A.unit_share().items()}
    F["wpy"] = A.wpy
    F["rev_e_vs_g"] = float(sum(A.wpy * F["unit_share"][u] * (cost[A.pair_of[u]]["back to Rev E (full PM every 2,000)"] -
                                                            cost[A.pair_of[u]]["Rev G at the pair's count"]) for u in UNITS))
    F["fleet_vs_g"] = float(sum(A.wpy * F["unit_share"][u] * (cost[A.pair_of[u]]["Rev G at one fleet count"] -
                                                            cost[A.pair_of[u]]["Rev G at the pair's count"]) for u in UNITS))
    F["record"] = {"sorted": int(len(d)), "window": A.n_win, "retests": int(A.R.retests), "first_sort": str(d.sort_ts.min())[:10],
                   "last_sort": str(d.sort_ts.max())[:10], "lives": {p: len(A.life[p]["betas"]) for p in A.pairs}}
    F["A"] = A
    return F


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if x != x else float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, set):
        return sorted(x)
    return x


def write(F, path):
    out = {k: v for k, v in F.items() if k not in ("A",)}
    out = dict(out["stated"], **{k: v for k, v in out.items() if k != "stated"})
    json.dump(jsonable(out), open(path, "w"), indent=1, sort_keys=True)
