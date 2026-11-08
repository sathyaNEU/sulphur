"""task2 architecture 4: every rung and rival on the cut pack, written to generator/rungs.json."""
import json
import math
import sys

import numpy as np

import solve as S

VARIANTS = [
    ("golden", {}),
    ("affine", {"how": "affine"}),
    ("cell_30", {"cell": 30.0}),
    ("cell_20", {"cell": 20.0}),
    ("disc_332", {"disc": (3, 3, 2)}),
    ("disc_10101", {"disc": (10, 10, 4)}),
    ("lag_10", {"lag": 10.0}),
    ("reassay_mean", {"reassay": "mean"}),
    ("reassay_last", {"reassay": "reassay"}),
    ("nugget_dup", {"nugget": "dup"}),
    # the wrong rungs
    ("rung0_raw", {"support": False, "decl": False}),
    ("rung1_declustered", {"support": False}),
    ("rung_cos_no_decl", {"decl": False}),
    ("cracker_raw_variance", {"raw_variance": True}),
]
STANDING = ["golden", "affine", "cell_30", "cell_20", "disc_332", "disc_10101", "lag_10", "reassay_mean",
            "reassay_last", "nugget_dup"]


def nugget_from_duplicates(target):
    """The field duplicates' share of the sample variance: half the mean squared pair difference over the
    composites' variance (a nugget floor a run might fix)."""
    import csv
    import os
    assays = {}
    with open(os.path.join(target, S.FILES["assays"]), newline="") as f:
        for r in csv.DictReader(f):
            assays.setdefault(r["sample_id"], 0.005 if r["au"].startswith("<") else float(r["au"]))
    d = []
    with open(os.path.join(target, "MC_qaqc_results_2019-2024.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["qc_type"] == "FIELD_DUP" and r["parent_sample_id"] in assays:
                v = 0.005 if r["result_au"].startswith("<") else float(r["result_au"])
                d.append((assays[r["parent_sample_id"]], v))
    a = np.array(d)
    return float(0.5 * np.mean((a[:, 0] - a[:, 1]) ** 2)), len(d)


def summarise(r):
    return {"oz": round(r["oz"], 0), "tier": r["tier"], "ratio": round(r["ratio"], 4), "mean_decl": round(r["mean_decl"], 4),
            "cv_decl": round(r["cv_decl"], 4),
            "model": [round(float(x), 3) for x in r["model"]], "T": round(r["T"], 0),
            "gt": {str(c): {k: round(v, 4) for k, v in r["gt"][c].items()} for c in S.CUTS}}


def main(target, out):
    res = {}
    full = {}
    dup_var, n_dup = nugget_from_duplicates(target)
    for name, kw in VARIANTS:
        kw = dict(kw)
        if kw.get("nugget") == "dup":
            s5 = S.stage5(target)
            g = np.array([c[4] for c in s5])
            # 1 m duplicate scatter carried to a 2.5 m composite of 2.5 samples, over the composites' variance
            kw["nugget"] = round(min(0.6, dup_var / 2.5 / float(np.var(g))), 3)
        r = S.run(target, **kw)
        res[name] = summarise(r)
        if name == "golden":
            full[name] = r
        print("  %-18s %6.0f koz tier %s ratio %.3f" % (name, r["oz"] / 1e3, r["tier"], r["ratio"]), flush=True)
    g = full["golden"]
    s5 = S.stage5(target)
    w = S.decluster(s5)
    krig = {}
    for name, mn, rad in (("kriged", 24, 45.0), ("kriged_n12", 12, 45.0), ("kriged_n32", 32, 60.0)):
        est, fl = S.krige_blocks(target, g["model"], s5, max_n=mn, radius=rad)
        kt = S.kriged_tonnage(target, s5, est, fl, w)
        krig[name] = {"oz": round(kt[S.CUT]["oz"], 0), "tier": S.tier(kt[S.CUT]["oz"]),
                      "gt": {str(c): {k: round(v, 4) for k, v in kt[c].items()} for c in S.CUTS},
                      "cv": round(float(est.std() / est.mean()), 3), "mean": round(float(est.mean()), 4)}
        print("  %-18s %6.0f koz tier %s cv %.2f" % (name, kt[S.CUT]["oz"] / 1e3, krig[name]["tier"], est.std() / est.mean()),
              flush=True)
    res.update(krig)
    # the kriging's own check: leave-one-hole-out cross-validation slope at composite support (the self-confirming
    # check), on a systematic tenth of the holes
    comps = np.array([(c[1], c[2], c[3], c[4]) for c in s5])
    hole = np.array([c[0] for c in s5])
    names = sorted(set(hole))[::10]
    est_cv, obs_cv = [], []
    for h in names:
        mask = hole != h
        q = comps[mask]
        for p in comps[hole == h]:
            dist = np.sqrt((q[:, 0] - p[0]) ** 2 + (q[:, 1] - p[1]) ** 2 + ((q[:, 2] - p[2]) / g["model"][4]) ** 2)
            sel = np.argsort(dist)[:24]
            qq = q[sel]
            n = len(sel)
            A = np.ones((n + 1, n + 1))
            A[n, n] = 0
            A[:n, :n] = 1 - S.gamma_model(np.hypot(qq[:, None, 0] - qq[None, :, 0], qq[:, None, 1] - qq[None, :, 1]),
                                          np.abs(qq[:, None, 2] - qq[None, :, 2]), g["model"])
            np.fill_diagonal(A[:n, :n], 1.0)
            b = np.ones(n + 1)
            b[:n] = 1 - S.gamma_model(np.hypot(qq[:, 0] - p[0], qq[:, 1] - p[1]), np.abs(qq[:, 2] - p[2]), g["model"])
            lam = np.linalg.solve(A, b)[:n]
            est_cv.append(float(lam @ qq[:, 3]))
            obs_cv.append(float(p[3]))
    e, o = np.array(est_cv), np.array(obs_cv)
    slope = float(np.polyfit(e, o, 1)[0])
    res["kriging_cv"] = {"n": len(e), "mean_error": round(float((e - o).mean()), 4), "slope_obs_on_est": round(slope, 3)}
    res["dup"] = {"half_msd": round(dup_var, 4), "pairs": n_dup}
    res["standing"] = STANDING
    res["experimental"] = {"dh": [[round(a, 1), round(b, 4), n] for a, b, n in g["dh"]],
                           "hz": [[round(a, 1), round(b, 4), n] for a, b, n in g["hz"]]}
    json.dump(res, open(out, "w"), indent=1, sort_keys=True)
    return res, full


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
