"""Every owed figure, computed once from the shipped files: the golden, the rival methods that set each band, the
hurried and quick routes the effort test scores, each shortcut's call, and the perturbations the forcing block
records. golden.py, writeup.py, effort_passes.py and checks.py all read this one object."""
import copy
import math

import numpy as np
import pandas as pd

import analysis as A
import params as P

REPS = 600


def _forecast_with(F, D, **kw):
    """The golden forecast with one modelling choice changed (a rival in the band)."""
    X = A.expo_2027(F)
    fr = A.frost_clim(F)
    out = {}
    for k in A.PARTS:
        p = P.PART[k]
        drv = D[k]["driver"]
        b = D[k]["beta"]
        if kw.get("nff_pooled"):
            nr0 = A.nff_rates(F, k, drv)
            R = F["removals"]
            R = R[(R["k"] == k) & (R["reason"] == "UNSCH") & (R["finding"] == "NFF") & (R["date"] <= A.Y26[1])]
            Dd = F["day"][F["day"]["date"] <= A.Y26[1]]
            tot = float({"cyc": Dd["cyc"].sum(), "fh": Dd["fh"].sum(), "days": len(Dd)}[drv]) * p["pos"]
            pooled = len(R) / tot
            nr = {s: pooled for s in nr0}
        else:
            nr = A.nff_rates(F, k, drv)
        cf = nf = 0.0
        for _, r in X.iterrows():
            st = A.station_of(r["grp"])
            e = {"cyc": r["cyc"], "fh": r["fh"], "days": r["acdays"]}[drv] * p["pos"]
            frost = fr.get((st, int(r["month"])), 0.0)
            if kw.get("both") and drv != "days":
                bb = kw["both"][k]
                ratio = (r["fh"] / r["cyc"]) if r["cyc"] > 0 else 0.0
                lam = r["cyc"] * p["pos"] * math.exp(bb[0] + bb[1] * math.log(max(ratio, 1e-6)) + bb[2] * frost)
            else:
                lam = e * math.exp(b[0] + (b[1] * frost if len(b) > 1 else 0.0))
            cf += lam
            nf += e * nr.get(st, np.mean(list(nr.values())))
        out[k] = cf + nf
    # the propeller control converts through its own removals whatever the rest of the model
    fhm = X.groupby("month")["fh"].sum().to_dict()
    fhm = {m: fhm.get(m, 0.0) * P.PART["PEC"]["pos"] for m in range(1, 13)}
    sp = A.pec_split(F)
    nff_fh = (out["PEC"] - _cf_only(F, D, "PEC")) / max(sum(fhm.values()), 1.0)
    out["PEC"] = A.pec_forecast(F, fhm, max(nff_fh, 0.0), sp)[0]
    return out


def _cf_only(F, D, k):
    X = A.expo_2027(F)
    fr = A.frost_clim(F)
    b = D[k]["beta"]
    drv = D[k]["driver"]
    cf = 0.0
    for _, r in X.iterrows():
        st = A.station_of(r["grp"])
        e = {"cyc": r["cyc"], "fh": r["fh"], "days": r["acdays"]}[drv] * P.PART[k]["pos"]
        cf += e * math.exp(b[0] + (b[1] * fr.get((st, int(r["month"])), 0.0) if len(b) > 1 else 0.0))
    return cf


def both_fit(F):
    """A rival that lets the data weigh landings and hours together: landings as the offset, the hours a landing
    as a covariate (an elasticity), frost beside them."""
    out = {}
    for k in A.PARTS:
        g = A.panel(F, k, "CF")
        ok = (g["cyc"] > 0) & (g["fh"] > 0)
        g = g[ok]
        X = np.column_stack([np.ones(len(g)), np.log(g["fh"].values / g["cyc"].values), g["frost_rate"].values])
        b, ll = A.poisson_fit(g["n"].values.astype(float), X, np.log(g["cyc"].values))
        out[k] = b
    return out


def nb_ranges(F, fc):
    from scipy.stats import nbinom
    out = {}
    for k in A.PARTS:
        mu = float(fc[k]["total"])
        n_ev = int(((F["removals"]["k"] == k) & (F["removals"]["reason"] == "UNSCH")).sum())
        var = float(fc[k]["cf"]) + A.nff_dispersion(F, k) * float(fc[k]["nff"]) + mu * mu / max(n_ev, 1)
        if var <= mu * 1.0001:
            var = mu * 1.0001
        p = mu / var
        r = mu * mu / (var - mu)
        out[k] = (int(nbinom.ppf(0.10, r, p)), int(nbinom.ppf(0.90, r, p)))
    return out


def calls_family(E):
    """Each golden-family member's change line by line, from effort.json's forcing block (the answers are signs)."""
    out = []
    for x in E["forcing"]["golden_family"]:
        d = {}
        for a in x["answer"]:
            act, k = a.split(":")
            d[k] = 1 if act == "BUY" else -1
        out.append({k: d.get(k, 0) for k in set(d) | set(a.split(":")[1] for a in E["forcing"]["golden_answer"])})
    return out


def calls(need, pool=None):
    """The plan's lines that change: each part number's spares needed against what its pool holds."""
    pool = pool or P.POOL
    return {k: int(need[k]) - int(pool[k]) for k in A.PARTS}


def call_set(ch, min_step=2):
    """The lines the recommendation names: a purchase or a cut of two units or more."""
    return sorted(["BUY:%s" % k for k, v in ch.items() if v >= min_step] + ["CUT:%s" % k for k, v in ch.items() if v <= -min_step])


def compute(target, reps=REPS):
    F = A.load(target)
    D = A.drivers_cache(F)
    fc = A.forecast(F, D)
    MC = A.simulate(F, fc, D, reps=reps, seed=20271)
    need = {k: MC[k]["need"] for k in A.PARTS}
    W, saving = A.watch_golden(F, fc, "mixture")
    Wr, saving_raw = A.watch_golden(F, fc, "raw")
    We, saving_eb = A.watch_golden(F, fc, "eb")
    Hw = A.watch_hurried(F)
    H = A.hurried(F)                                   # careful but hurried: per flight hour, average turnaround
    Hd = A.hurried(F, exposure="drv", D=D)             # the exposure put right alone
    Hg = A.hurried(F, exposure="golden", fc=fc)        # the golden removals on the average turnaround
    # rivals for the removals
    bf = both_fit(F)
    riv = {"both exposures": _forecast_with(F, D, both=bf),
           "no frost term": {k: v["total"] for k, v in A.forecast(F, A.drivers(F, cold=False)).items()},
           "no-fault-found pooled over stations": _forecast_with(F, D, nff_pooled=True)}
    # the window rival: the fits on 2024 to 2026
    F2 = copy.copy(F)
    F2["removals"] = F["removals"][F["removals"]["date"] >= pd.Timestamp("2024-01-01")]
    F2["day"] = F["day"][F["day"]["date"] >= pd.Timestamp("2024-01-01")]
    A._DCACHE.pop(id(F2), None)
    riv["fitted on 2024 to 2026"] = {k: v["total"] for k, v in A.forecast(F2, A.drivers(F2)).items()}
    # the last twelve months alone (the report's window) on each part's own exposure; the propeller control keeps its
    # conversion, which the repairers' bulletin dates force whatever the window
    riv["the last twelve months on each part's own exposure"] = {k: (fc[k]["total"] if k == "PEC" else Hd[k]["proj"])
                                                                for k in A.PARTS}
    # rivals for the spares (the golden family): another stream of replays, the no-fault-found removals without
    # their month-to-month spread, the frost of an average winter, the queue calibrated on the last eighteen months,
    # the removals of the both-exposures fit
    MC2 = A.simulate(F, fc, D, reps=reps, seed=31337)
    need2 = {k: MC2[k]["need"] for k in A.PARTS}
    fam = {"a second stream of replays": MC2,
           "no-fault-found removals without their monthly spread": A.simulate(F, fc, D, reps=reps, seed=4242, no_disp=True),
           "every winter at its average frost": A.simulate(F, fc, D, reps=reps, seed=5151, no_frost=True),
           "the shop calibrated on 2025 to 2026 alone": A.simulate(F, fc, D, reps=reps, seed=6161, cap_since="2025-01-01")}
    fc_both = copy.deepcopy(fc)
    for k in A.PARTS:
        m = riv["both exposures"][k] / fc[k]["total"] if fc[k]["total"] > 0 else 1.0
        for c in ("total", "cf", "nff"):
            fc_both[k][c] = fc[k][c] * m
    fam["the both-exposures removals"] = A.simulate(F, fc_both, D, reps=reps, seed=7171)
    fc_12 = copy.deepcopy(fc)
    for k in A.PARTS:
        m = riv["the last twelve months on each part's own exposure"][k] / fc[k]["total"] if fc[k]["total"] > 0 else 1.0
        for c in ("total", "cf", "nff"):
            fc_12[k][c] = fc[k][c] * m
    fam["the last twelve months' removals"] = A.simulate(F, fc_12, D, reps=reps, seed=8282)
    fam_need = {n: {k: m[k]["need"] for k in A.PARTS} for n, m in fam.items()}
    # a repairer's line has no shared queue, so Palm's theorem on the golden removals and the repairer's own
    # turnaround is a defensible method there; the in-house lines keep the replay
    fam_need["Palm's theorem on the golden removals for the repairers' lines"] = {
        k: (need[k] if P.PART[k]["shop"] == "BOO" else Hg[k]["spares"]) for k in A.PARTS}
    # the recommendation's lines: those every member of the golden family moves the same way
    gold_calls = calls(need)
    fam_calls = {n: calls(v) for n, v in fam_need.items()}
    robust = {}
    for k in A.PARTS:
        vals = [gold_calls[k]] + [c[k] for c in fam_calls.values()]
        if all(v > 0 for v in vals):
            robust[k] = ("BUY", min(vals), max(vals))
        elif all(v < 0 for v in vals):
            robust[k] = ("CUT", min(vals), max(vals))
    need_band = {k: (min([need[k]] + [v[k] for v in fam_need.values()]), max([need[k]] + [v[k] for v in fam_need.values()]))
                 for k in A.PARTS}
    def lines(ch):
        return sorted(["BUY:%s" % k for k, v in ch.items() if v > 0] + ["CUT:%s" % k for k, v in ch.items() if v < 0])
    robust_set = sorted("%s:%s" % (v[0], k) for k, v in robust.items())
    routes = [{"name": "golden", "label": "This plan", "answer": robust_set, "golden": True,
               "changes": {k: (gold_calls[k] if k in robust else 0) for k in A.PARTS}},
              {"name": "careful but hurried: each part per flight hour, the 2026 average turnaround, Palm's spares",
               "label": "Every part per flight hour, the 2026 turnaround, Palm's formula",
               "answer": lines(calls({k: H[k]["spares"] for k in A.PARTS})),
               "changes": calls({k: H[k]["spares"] for k in A.PARTS})},
              {"name": "quick: the October outlook and the pool as it stands", "label": "The pool as it stands",
               "answer": [], "changes": {k: 0 for k in A.PARTS}},
              {"name": "the landing-driven parts on landings alone, the average turnaround",
               "label": "Landings for the landing-driven parts, the 2026 turnaround, Palm's formula",
               "answer": lines(calls({k: Hd[k]["spares"] for k in A.PARTS})),
               "changes": calls({k: Hd[k]["spares"] for k in A.PARTS})},
              {"name": "the golden removals on the 2026 average turnaround, Palm's spares",
               "label": "This plan's removals, the 2026 turnaround, Palm's formula",
               "answer": lines(calls({k: Hg[k]["spares"] for k in A.PARTS})),
               "changes": calls({k: Hg[k]["spares"] for k in A.PARTS})}]
    G = {"fam": fam, "fam_need": fam_need,
         "F": F, "D": D, "fc": fc, "MC": MC, "MC2": MC2, "need": need, "need2": need2, "W": W, "saving": saving,
         "saving_raw": saving_raw, "saving_eb": saving_eb, "W_raw": Wr, "W_eb": We, "Hw": Hw, "H": H, "Hd": Hd,
         "Hg": Hg, "riv": riv, "calls": gold_calls, "call_set": robust_set, "robust": robust, "need_band": need_band,
         "fam_calls": fam_calls, "routes": routes}
    # removal bands: the golden and every rival, a whole removal either side; range bands from the family's replays
    G["rem_band"] = {k: (min([fc[k]["total"]] + [riv[n][k] for n in riv]) - 1.0,
                         max([fc[k]["total"]] + [riv[n][k] for n in riv]) + 1.0) for k in A.PARTS}
    # the range's rival without a replay: a negative binomial on the golden's mean, its variance the confirmed
    # failures' Poisson part, the no-fault-found removals' own monthly overdispersion and the rate's sampling error
    nb = nb_ranges(F, fc)
    G["nb_range"] = nb
    G["p10_band"] = {k: (min([MC[k]["p10"], nb[k][0]] + [m[k]["p10"] for m in fam.values()]) - 1,
                         max([MC[k]["p10"], nb[k][0]] + [m[k]["p10"] for m in fam.values()]) + 1) for k in A.PARTS}
    G["p90_band"] = {k: (min([MC[k]["p90"], nb[k][1]] + [m[k]["p90"] for m in fam.values()]) - 1,
                         max([MC[k]["p90"], nb[k][1]] + [m[k]["p90"] for m in fam.values()]) + 1) for k in A.PARTS}
    G["saving_band"] = (min(saving, saving_raw) * 0.95, max(saving, saving_raw) * 1.05)
    G["scrap"] = sorted(W.index[W["scrap"]])
    G["tat_in"] = MC["_tat_in"]
    import docs
    G["qproj"] = {x["k"]: x["proj"] for x in docs.report_figures(F)["rows"]}
    return G
