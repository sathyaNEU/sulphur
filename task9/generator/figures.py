"""task9: every figure the answer blocks, the deck and effort.json state, computed by analysis.py from the cut pack,
with the golden family of rival methods behind each band and the fitted inputs' perturbations behind the call.

    compute(tgt) -> F     write(F, path) -> figures.json
"""
import datetime as dt
import json

import numpy as np
import pandas as pd

import analysis as AN

UNITS = AN.UNITS
PRODS = ["P-A", "P-B", "P-C"]


def r(x, n=0):
    return None if x is None or x != x else (round(float(x), n) if n else int(round(float(x))))


def clip_shares(s):
    """A cause whose fitted share is below zero has none."""
    return {k: max(0.0, float(v)) for k, v in s.items()}


def r1_cells(points, die):
    out = {"points": r(points, 2)}
    out.update({"%s die" % p: int(round(die.get(p, 0.0), -3)) for p in PRODS})
    return out


def r3_cells(units):
    return {p: int(round(units.get(p, 0.0), -2)) for p in PRODS}


def r4_cells(m):
    out = {}
    for u in UNITS:
        on, sl = m[u]
        out["%s onset" % u] = int(round(on, -1))
        out["%s climb" % u] = r(sl * 100, 1)
    return out


def counts(c):
    return {u: int(round(v, -1)) for u, v in c.items()}


def compute(tgt):
    A = AN.Analysis(tgt)
    o = A.routes()
    d, w = A.d, A.d[A.d.win]
    F = {"pairs": A.pairs, "n_window": A.n_win, "allin": A.allin, "fwd_lot": A.fwd_lot, "stock_left": A.stock_left,
         "mix": A.mix, "vol": A.vol}

    # ---------------------------------------------------------------- the golden, as computed
    G = {
        "R1_points": A.R1, "R1_die": dict(A.R1_die), "R1_usd": A.R1_usd, "R1_q1": A.R1_q1, "unflagged_share": A.unflagged_share,
        "R1_fwd_share": A.R1_fwd_share, "R2_shares": dict(A.R2), "R3_units": dict(A.R3), "R3_observed": dict(A.R3_observed),
        "R3_usd": A.R3_usd, "ft": {k: v for k, v in A.ft.items() if k != "latent"},
        "R4": {u: {"onset": A.onset[u], "climb": A.slope[u]} for u in UNITS}, "REC": dict(A.REC), "R5": A.R5,
        "R5_unit": dict(A.R5_unit), "R5_pair": dict(A.R5_pair),
        "fits": {"%s|%s" % k: {x: f[x] for x in ("w0", "r0", "beta", "gamma", "n")} for k, f in A.gfit.items()},
        "ring_swaps": A.ring_swaps, "ring_t": o["R2_joint_ring_t"],
    }
    F["gold"] = G

    # ---------------------------------------------------------------- the stated figures (the answer blocks' precision)
    S = {
        "R1_loss": r1_cells(A.R1, A.R1_die),
        "R2_shares": {k: r(v, 3) for k, v in clip_shares(A.R2).items()},
        "R3_ft_units": r3_cells(A.R3),
        "R4_dose": r4_cells({u: (A.onset[u], A.slope[u]) for u in UNITS}),
        "REC_counts": counts(A.REC),
        "R5_saving": int(round(A.R5, -3)),
    }
    S["R1_usd_by"] = {p: int(round(A.R1_die[p] * A.value[p], -3)) for p in PRODS}
    S["R1_usd"] = sum(S["R1_usd_by"].values())
    S["R3_usd_by"] = {p: int(round(A.R3[p] * (A.value[p] + A.assy[p]), -3)) for p in PRODS}
    S["R3_usd"] = sum(S["R3_usd_by"].values())
    S["R3_total"] = sum(S["R3_ft_units"].values())
    S["R5_pair"] = {p: int(round(v, -3)) for p, v in A.R5_pair.items()}
    S["ft_base"] = r(A.ft["base"] * 100, 2)              # per cent of units
    S["ft_level"] = r(A.ft["L"] * 100, 1)                # per cent of the outer band's good die
    S["ft_start"] = {u: int(round(A.ft["u0"] * A.onset[u], -1)) for u in UNITS}
    S["ft_full"] = {u: int(round((A.ft["u0"] + A.ft["us"]) * A.onset[u], -1)) for u in UNITS}
    F["stated"] = S

    # ---------------------------------------------------------------- the golden family: rival methods run on the pack
    riv = {}

    def loss_with(r0):
        die = d.tested_band * (d.y - r0)
        ww, sub = die[d.win], d[d.win]
        return float(np.mean(ww / sub.gross) * 100), {p: float(v) for p, v in ww.groupby(sub["product"]).sum().items()}
    young = d[d.wear < 0.5]
    riv["R1"] = {
        "the band's excess on wafers under half their lot's onset, by pair": loss_with(d.pair.map(
            young.groupby("pair").apply(lambda g: np.average(g.y, weights=g.tested_band)))),
        "the same by product": loss_with(d["product"].map(young.groupby("product").apply(lambda g: np.average(g.y, weights=g.tested_band)))),
        "each pair's fit over every lot": (o["R1_pooled"], o["R1_die_pooled"]),
        "an unweighted fit's intercept on the current lot, by pair": loss_with(d.pair.map(
            {p: AN.hinge_fit(d[(d.pair == p) & d.fwd], weight=False)["r0"] for p in A.pairs})),
        "one fallout for the fab": loss_with(pd.Series(float(np.average(young.y, weights=young.tested_band)), index=d.index)),
    }
    riv["R2"] = {"one joint fit per pair over every lot": clip_shares(o["R2_joint"]),
                 "per pair and lot without the rivals": clip_shares(A.cause_shares(
                     {"%s|%s" % k: dict(f, ring=0.0) for k, f in A.gfit.items()}, lambda g: g.pair + "|" + g.disk_lot))}
    # R3: the latent units read other sound ways
    ft = A.R.ft
    split = A.ft_fit("wear", split="pair")
    A.ft_design("wear")
    riv["R3"] = {"observed burn-in less the fitted base": dict(A.R3_observed),
                 "the same rise and level on the disk's raw use": o["R3_raw_age"],
                 "each pair's own level": A.ft_by_product(split["latent"])}
    # R4: per unit on the current lot, unweighted, with the ring term, below 3,000 wafers
    alt = {"an unweighted pair fit": {p: AN.hinge_fit(d[(d.pair == p) & d.fwd], weight=False) for p in A.pairs},
           "the pair fit with the ring's usage beside it": {p: AN.hinge_fit(d[(d.pair == p) & d.fwd], ring=True) for p in A.pairs},
           "the pair fit below 3,000 wafers": {p: AN.hinge_fit(d[(d.pair == p) & d.fwd & (d.disk < 3000)]) for p in A.pairs},
           "the pair fit with the rivals beside it": {p: A.cfit["%s|%s" % (p, A.fwd_lot)] for p in A.pairs}}
    riv["R4"] = {k: {u: (fits[A.pair_of[u]]["w0"], fits[A.pair_of[u]]["beta"] * 1000) for u in UNITS} for k, fits in alt.items()}
    riv["R4"]["each unit's own fit on the current lot (PU-2, PU-4)"] = {u: o["R4_unit_fwd"][u] if u in ("PU-2", "PU-4") else
                                                                        (A.onset[u], A.slope[u]) for u in UNITS}
    # REC, R5: the counts and the saving on the rivals
    fwd = lambda u: A.fwd_fit[A.pair_of[u]]
    pair_ft = {p: dict(split, L=split["L_by"][p]) for p in A.pairs}
    riv["REC"] = {
        "each unit's own fit on the current lot": o["REC_unit_fwd"],
        "final test's rise on the disk's raw use": o["REC_raw_age_ft"],
        "each pair's own final-test level": {u: A.tstar(A.loss_curve(fwd(u), ftm=pair_ft[A.pair_of[u]])) for u in UNITS},
        "the pad's term left out": {u: A.tstar(A.loss_curve(dict(fwd(u), gamma=0.0))) for u in UNITS},
    }
    for k, fits in alt.items():
        riv["REC"][k] = {u: A.tstar(A.loss_curve(fits[A.pair_of[u]])) for u in UNITS}
    riv["R5"] = {k: float(sum(A.yearly(A.loss_curve(fits[A.pair_of[u]]), riv["REC"][k][u], A.vol[u]) for u in UNITS))
                 for k, fits in alt.items()}
    riv["R5"]["final test's rise on the disk's raw use"] = float(sum(A.yearly(A.loss_curve(fwd(u), ftm=A.ft_raw),
                                                                             o["REC_raw_age_ft"][u], A.vol[u]) for u in UNITS))
    riv["R5"]["each pair's own final-test level"] = float(sum(A.yearly(A.loss_curve(fwd(u), ftm=pair_ft[A.pair_of[u]]),
                                                                      riv["REC"]["each pair's own final-test level"][u], A.vol[u]) for u in UNITS))
    riv["R5"]["each unit's share of the summer's wafers"] = o["R5_summer_share"]
    F["rivals"] = riv
    F["ft_split"] = {k: v for k, v in split.items() if k != "latent"}

    # ---------------------------------------------------------------- bands: the rivals' spread, held off every shortcut
    B = {}
    B["R1_loss"] = {"points": [round(S["R1_loss"]["points"] * 0.93, 2), round(S["R1_loss"]["points"] * 1.07, 2)]}
    B["R1_loss"].update({"%s die" % p: [int(round(S["R1_loss"]["%s die" % p] * 0.92, -3)), int(round(S["R1_loss"]["%s die" % p] * 1.08, -3))]
                         for p in PRODS})
    B["R2_shares"] = {"disk": [0.88, 1.0], "pad": [0.0, 0.10], "ring": [0.0, 0.03], "dep3": [0.0, 0.03], "sc4": [0.0, 0.03],
                      "rf": [0.0, 0.03]}
    B["R3_ft_units"] = {p: [int(round(v * 0.88, -2)), int(round(v * 1.12, -2))] for p, v in S["R3_ft_units"].items()}
    B["R4_dose"] = {}
    for u in UNITS:
        on, sl = S["R4_dose"]["%s onset" % u], S["R4_dose"]["%s climb" % u]
        B["R4_dose"]["%s onset" % u] = [int(round(on * 0.90, -1)), int(round(on * 1.10, -1))]
        B["R4_dose"]["%s climb" % u] = [round(sl * 0.85, 1), round(sl * 1.15, 1)]
    B["REC_counts"] = {u: [int(round(v * 0.92, -1)), int(round(v * 1.08, -1))] for u, v in S["REC_counts"].items()}
    B["R5_saving"] = [int(round(S["R5_saving"] * 0.90, -3)), int(round(S["R5_saving"] * 1.10, -3))]
    F["bands"] = B

    # ---------------------------------------------------------------- the passes
    thorough = {k: S[k] for k in ("R1_loss", "R2_shares", "R3_ft_units", "R4_dose", "REC_counts", "R5_saving")}
    careful = {"R1_loss": r1_cells(o["R1_pooled"], o["R1_die_pooled"]),
               "R2_shares": {k: r(v, 3) for k, v in clip_shares(o["R2_joint"]).items()},
               "R3_ft_units": r3_cells(o["R3_proportional"]),
               "R4_dose": r4_cells(o["R4_pooled"]),
               "REC_counts": counts(o["REC_pooled_proportional"]),
               "R5_saving": int(round(o["R5_pooled_proportional"], -3))}
    quick = {"R1_loss": r1_cells(o["R1_labels"], o["R1_die_labels"]),
             "R2_shares": {k: (r(v, 3) if k in ("dep3", "sc4") else None) for k, v in o["R2_commonality"].items()},
             "R3_ft_units": r3_cells(o["R3_clean_lot_base"]),
             "R4_dose": r4_cells(o["R4_fleet"]),
             "REC_counts": counts(o["REC_fleet_sort_only"]),
             "R5_saving": int(round(o["R5_summer_rate"], -3))}
    F["passes"] = {"quick": quick, "careful": careful, "thorough": thorough}
    F["routes"] = o

    # ---------------------------------------------------------------- the call's perturbations
    pert = {}

    def with_ft(**kw):
        return dict(A.ft, **{k: A.ft[k] * v for k, v in kw.items()})
    for name, mod in (("every climb 15 per cent steeper", dict(beta=1.15)), ("every climb 15 per cent flatter", dict(beta=0.85)),
                      ("every onset 5 per cent earlier", dict(w0=0.95)), ("every onset 5 per cent later", dict(w0=1.05)),
                      ("the pad's term doubled", dict(gamma=2.0))):
        pert[name] = {u: A.tstar(A.loss_curve(dict(fwd(u), **{k: fwd(u)[k] * v for k, v in mod.items()}))) for u in UNITS}
    for name, mod in (("final test's level 15 per cent higher", dict(L=1.15)), ("final test's level 15 per cent lower", dict(L=0.85)),
                      ("final test's rise starting 8 per cent sooner", dict(u0=0.92)), ("final test's rise starting 8 per cent later", dict(u0=1.08)),
                      ("final test's rise 20 per cent shorter", dict(us=0.8)), ("final test's rise 20 per cent longer", dict(us=1.2))):
        pert[name] = {u: A.tstar(A.loss_curve(fwd(u), ftm=with_ft(**mod))) for u in UNITS}
    for name, c in (("the disk change 10 per cent dearer", A.allin["disk_change"] * 1.1),
                    ("the disk change 10 per cent cheaper", A.allin["disk_change"] * 0.9)):
        pert[name] = {u: A.tstar(A.loss_curve(fwd(u)), c=c) for u in UNITS}
    for name, k in (("die values 10 per cent higher", 1.1), ("die values 10 per cent lower", 0.9)):
        save = dict(A.value)
        A.value = {p: v * k for p, v in save.items()}
        pert[name] = {u: A.tstar(A.loss_curve(fwd(u))) for u in UNITS}
        A.value = save
    F["perturbations"] = pert

    # ---------------------------------------------------------------- what the deck shows beside the graded figures
    d["sort_month"] = d.sort_ts.dt.strftime("%Y-%m")
    mo = d[d.sort_ts < "2026-09-01"].groupby("sort_month")
    F["monthly"] = {k: float(np.mean(g.ring_die / g.gross) * 100) for k, g in mo}
    F["monthly_wafers"] = {k: int(len(g)) for k, g in mo}
    ftm = ft.assign(month=ft.ft_date.dt.strftime("%Y-%m"), latent=A.ft["latent"])
    F["ft_monthly"] = {k: {"burnin_pct": float(g.burnin_fail.sum() / g.units_in.sum() * 100),
                           "ring_pct": float(g.latent.sum() / g.units_in.sum() * 100), "lots": int(len(g))}
                       for k, g in ftm.groupby("month")}
    bins = {}
    for p in A.pairs:
        for lab, sub in (("current", d[(d.pair == p) & d.fwd]), ("earlier", d[(d.pair == p) & ~d.fwd])):
            b = (sub.disk // 200).astype(int)
            rows = []
            for k, gg in sub.groupby(b):
                if len(gg) >= 60 and k * 200 < 3200:
                    rows.append((int(k * 200 + 100), float(np.average(gg.y, weights=gg.tested_band)), int(len(gg))))
            bins["%s %s" % (p, lab)] = rows
    F["binned"] = bins
    F["fitted"] = {}
    for p in A.pairs:
        for lab, f in (("current", A.fwd_fit[p]), ("earlier", A.old_fit[p])):
            F["fitted"]["%s %s" % (p, lab)] = [(x, float(f["r0"] + A.excess(x, f))) for x, _, _ in bins["%s %s" % (p, lab)]]
    full, dp = A.allin["full_pm"], A.disk_price
    cost = {}
    for p in A.pairs:
        lc = A.curve[p]
        u = A.pairs[p][0]
        cost[p] = {"Rev F as it stands": full / AN.REV_F_DISK + float(np.sum(lc[:AN.REV_F_DISK])) / AN.REV_F_DISK,
                   "back to Rev E (full PM every 2,000)": full / 2000 + float(np.sum(lc[:2000])) / 2000,
                   "Rev G at the pair's count": (full - dp) / AN.REV_F_DISK + A.cpw_g(lc, A.REC[u]),
                   "Rev G at the count set on every lot's curve": (full - dp) / AN.REV_F_DISK + A.cpw_g(lc, o["REC_pooled"][u])}
    F["cost_per_wafer"] = cost
    F["pooled_vs_g"] = float(sum(A.vol[u] * (cost[A.pair_of[u]]["Rev G at the count set on every lot's curve"] -
                                            cost[A.pair_of[u]]["Rev G at the pair's count"]) for u in UNITS))
    F["downforce"] = {p: float(A.R.fdc[A.R.fdc.unit.isin(us)].downforce_psi.median()) for p, us in A.pairs.items()}
    F["old_onsets"] = {p: int(round(A.old_fit[p]["w0"], -1)) for p in A.pairs}
    F["fwd_received"] = dt.date.fromisoformat(str(A.R.disk_lots.set_index("supplier_lot").receipt_date[A.fwd_lot])[:10]).strftime("%-d %B")
    F["fwd_all_since"] = max(d[(d.unit == u) & d.fwd].polish_ts.min() for u in UNITS).strftime("%-d %B")
    ex = [o[k][u] / A.REC[u] - 1 for k in ("REC_pooled", "REC_sort_only", "REC_proportional") for u in UNITS]
    F["shortcut_range"] = (int(np.floor(100 * min(ex))), int(np.ceil(100 * max(ex))))
    F["short_units"] = sorted(u for u in UNITS if d[(d.unit == u) & d.fwd].disk.max() < 1500)
    F["record"] = {"sorted": int(len(d)), "window": A.n_win, "retests": int(A.R.retests), "first_sort": str(d.sort_ts.min())[:10],
                   "last_sort": str(d.sort_ts.max())[:10], "ft_lots": int(len(ft)), "ft_lots_window": A.n_ft_win,
                   "lives": {L: int(d[d.disk_lot == L].disk_life.nunique()) for L in A.lot_names},
                   "fwd_lives": {u: int(d[(d.unit == u) & d.fwd].disk_life.nunique()) for u in UNITS}}
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
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, set):
        return sorted(x)
    return x


def write(F, path):
    out = {k: v for k, v in F.items() if k not in ("A",)}
    out = dict(out["stated"], **{k: v for k, v in out.items() if k != "stated"})
    json.dump(jsonable(out), open(path, "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    import sys
    F = compute(sys.argv[1])
    S, B = F["stated"], F["bands"]
    for k in ("R1_loss", "R2_shares", "R3_ft_units", "R4_dose", "REC_counts", "R5_saving"):
        print(k, S[k], "band", B[k])
        for p in ("quick", "careful"):
            print("   ", p, F["passes"][p][k])
    for k, v in F["rivals"].items():
        for name, val in v.items():
            print("rival", k, name, val if not isinstance(val, tuple) else (round(val[0], 3), {a: round(b) for a, b in val[1].items()}))
    for k, v in F["perturbations"].items():
        print("pert", k, v)
    print("ft split", F["ft_split"])
    print("stated extras", {k: S[k] for k in ("R1_usd", "R3_usd", "R3_total", "R5_pair", "ft_base", "ft_level", "ft_start", "ft_full")})
    print("record", F["record"])
    print("cost", F["cost_per_wafer"], "pooled_vs_g", round(F["pooled_vs_g"]))
