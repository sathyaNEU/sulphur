"""task19 analysis on the cut pack: the golden, the hurried passes, the rival methods and the routes, each run end to
end by golden.run with its switches (no pass reads the prompt; this is the paper argument computed)."""
import numpy as np

import golden as G

DNAME = {"D01": "Port Ardain", "D02": "Ballinrea", "D03": "Drumcastle", "D04": "Fort Larrick", "D05": "Tullaghvane",
         "D06": "Carnmoyle", "D07": "Newbrook", "D08": "Rossmullan", "D09": "Glenarra", "D10": "Loughmeen",
         "D11": "Ardvale", "D12": "Fennabeg"}
B_GOLDEN = 400


def r10(x):
    return int(round(float(x) / 10.0) * 10)


def r100(x):
    return int(round(float(x) / 100.0) * 100)


def call_of(r):
    out = {"qualifies": [], "too close to call": [], "does not qualify": []}
    for d, c in zip(r["dists"], r["call"]):
        out[c].append(d)
    return out


def call_key(r):
    c = call_of(r)
    return {"qualifies": sorted(c["qualifies"]), "too close to call": sorted(c["too close to call"])}


def lr10(values, total):
    """Each value to the nearest 10 so the rounded values add to the rounded total (largest remainder)."""
    keys = list(values)
    fl = {k: int(np.floor(values[k] / 10.0)) * 10 for k in keys}
    left = int(round((total - sum(fl.values())) / 10.0))
    order = sorted(keys, key=lambda k: values[k] - fl[k], reverse=True)
    for k in (order[:left] if left > 0 else []):
        fl[k] += 10
    for k in (order[::-1][:-left] if left < 0 else []):
        fl[k] -= 10
    return fl


def summary(r):
    """The figures one run files, in the units the answer blocks use."""
    nat = r10(r["national"])
    s = {"national": nat, "districts": lr10({d: float(e) for d, e in zip(r["dists"], r["est"])}, nat)}
    if "sd" in r:
        s["nat_half_pct"] = round(100 * 1.6449 * r["sd_national"] / r["national"], 2)
        s["nat_interval"] = [r100(r["nat_lo"]), r100(r["nat_hi"])]
        s["intervals"] = {d: [r10(lo), r10(hi)] for d, lo, hi in zip(r["dists"], r["lo"], r["hi"])}
        s["p_line"] = {d: round(float(p), 2) for d, p in zip(r["dists"], r["p_line"])}
        s["call"] = call_key(r)
    s["coverage"] = {"nationals": round(100 * r["coverage_nationals"], 1), "others": round(100 * r["coverage_others"], 1)}
    s["linked"] = {"nationals": round(100 * r["linked_nationals"], 1), "others": round(100 * r["linked_others"], 1)}
    s["recall"] = {"nationals": round(100 * r["recall_nationals"], 1), "others": round(100 * r["recall_others"], 1)}
    s["k"] = {"18-29": round(float(r["k"][0]), 3), "30-44": round(float(r["k"][1]), 3)}
    s["da"] = {"18-29": round(float(r["da"][0]), 4), "30-44": round(float(r["da"][1]), 4)}
    br = r["bridge"]
    s["over"] = {d: r10(br[d]["over_total"]) for d in r["dists"]}
    s["listed_elsewhere"] = {d: r10(br[d]["listed_elsewhere"]) for d in r["dists"]}
    s["register"] = {d: int(round(br[d]["register"])) for d in r["dists"]}
    s["over_parts"] = {d: lr10(dict(br[d]["over"]), s["over"][d]) for d in r["dists"]}
    # the last part takes the rounding, so each district's bridge adds to its estimate exactly
    fz = int(r["forces"]["total"]) if r.get("forces_added") else 0
    s["serving_personnel"] = fz
    s["on_no_list"] = {d: s["districts"][d] - (fz if d == "D04" else 0) - s["register"][d] + s["over"][d]
                       - s["listed_elsewhere"][d] for d in r["dists"]}
    acc = r["accounts"]
    s["official"] = int(acc["official_2026"])
    s["gap"] = r10(acc["official_2026"] - r["national"])
    s["imm_not_in_accounts"] = int(acc["imm_not_in_accounts"])
    s["unrecorded_emigration"] = r10(r["emig"]["unrecorded"])
    s["remainder"] = r10(s["gap"] - s["unrecorded_emigration"] + s["imm_not_in_accounts"])
    return s


def compute(target):
    prep = G.prepare(target)
    out = {"prep": prep}
    gold = G.run(prepared=prep, bootstrap="full", B=B_GOLDEN)
    out["golden_raw"] = gold
    out["golden"] = summary(gold)
    # the careful but hurried pass, as the judge's own first pass worked: the links corrected on the clerical review and
    # every step repeated in the bootstrap, but independence within age and sex kept and the gap to the rolled-forward
    # figure read as emigration
    car = G.run(prepared=prep, dependence="none", bootstrap="full", B=B_GOLDEN)
    cs = summary(car)
    cs["unrecorded_emigration"] = r10(max(0, cs["gap"] + cs["imm_not_in_accounts"]))
    cs["remainder"] = r10(cs["gap"] - cs["unrecorded_emigration"] + cs["imm_not_in_accounts"])
    out["careful_raw"], out["careful"] = car, cs
    # the survey blocks resampled on their own, the linkage correction and the factors held fixed
    out["survey_only"] = summary(G.run(prepared=prep, bootstrap="survey", B=B_GOLDEN, seed=2026))
    # how well the sample blocks' entries, expanded by their selection probabilities, reproduce each district's count
    D_, A_, _, _ = prep
    fu_, reg_ = A_["fu"], A_["reg"]
    exp_ = fu_.groupby("district")["w"].sum()
    cnt_ = reg_.groupby("district").size()
    out["ht_register_ratio"] = {d: round(float(exp_[d] / cnt_[d]), 3) for d in gold["dists"]}
    # the quick pass: the register's own counts, the register's correct-looking share as coverage, no interval
    reg = gold["bridge"]
    q = {"national": int(round(sum(reg[d]["register"] for d in gold["dists"]))),
         "districts": {d: int(round(reg[d]["register"])) for d in gold["dists"]}}
    q["call"] = {"qualifies": sorted(d for d in gold["dists"] if reg[d]["register"] >= G.LINE), "too close to call": []}
    q["coverage"] = {"nationals": 100.0, "others": 100.0}
    q["k"] = {"18-29": 1.0, "30-44": 1.0}
    q["nat_half_pct"] = None
    q["unrecorded_emigration"] = None
    out["quick"] = q
    # rivals the golden family runs (each a defensible method the pack allows)
    rivals = {
        "unresolved records imputed within district and dwelling type": dict(impute="cells"),
        "unresolved records imputed at their district's resolved rate": dict(impute="district"),
        "linkage measured by nationality alone": dict(linkage="gold_nat"),
        "one raising factor for men aged 18 to 44": dict(dependence="single"),
        "the 2021 Census as the sex-ratio benchmark": dict(benchmark="census"),
        "raising Kilvarran men only": dict(dependence="nationals_only"),
    }
    out["rivals"] = {}
    for name, o in rivals.items():
        r = G.run(prepared=prep, bootstrap="full", B=200, seed=2027, **o)
        out["rivals"][name] = summary(r)
    # shortcuts, each run end to end on its own
    shortcuts = {
        "linked share read as coverage": dict(linkage="none"),
        "independence within age and sex": dict(dependence="none"),
        "a survey person found anywhere on the register counted as matched": dict(scope="national"),
        "every register entry taken as correct": dict(ce_mode="one"),
        "movers with no district recorded counted as gone": dict(mv_unknown="not_ce"),
        "the estimate scaled to the rolled-forward total": dict(calibrate_official=True),
        "serving personnel in the dual-system estimate": dict(forces_mode="in_dse"),
        "the sex ratio taken without serving personnel on the estimate's side": dict(dependence="births_no_domain"),
        "the sample blocks' estimate expanded by their selection probabilities": dict(estimator="ht"),
    }
    out["shortcuts"] = {}
    for name, o in shortcuts.items():
        r = G.run(prepared=prep, bootstrap="survey", B=200, seed=2028, **o)
        out["shortcuts"][name] = summary(r)
    # the one-fact test: the careful pass given each hint, run end to end
    hinted = {
        "the register and the coverage survey miss the same young men": dict(dependence="births", bootstrap="full"),
        "the rolled-forward estimate misses the same emigrants": dict(dependence="none", bootstrap="full"),
    }
    out["hinted"] = {}
    for name, o in hinted.items():
        r = G.run(prepared=prep, B=200, seed=2029, **o)
        s = summary(r)
        if not name.startswith("the rolled-forward"):
            s["unrecorded_emigration"] = r10(max(0, s["gap"] + s["imm_not_in_accounts"]))
            s["remainder"] = r10(s["gap"] - s["unrecorded_emigration"] + s["imm_not_in_accounts"])
        out["hinted"][name] = s
    # rivals on the emigration the accounts never recorded: the border matcher's threshold either way, the undated
    # leavers shared at the national dated share
    D0, A0 = prep[0], prep[1]
    out["emig_rivals"] = {}
    for name, kw in (("the border match taken at a lower weight", dict(thr=4.0)),
                     ("the border match taken at a higher weight", dict(thr=6.0)),
                     ("the undated leavers shared at the national dated share", dict(undated="national"))):
        out["emig_rivals"][name] = r10(G.emigration_still_listed(A0, D0, gold["ce"], **kw)["unrecorded"])
    # perturbations: each fitted input moved by its defensible spread
    out["perturb"] = perturbations(prep, gold)
    return out


def perturbations(prep, gold):
    """Each fitted input moved by the spread its own estimation gives (or 20 per cent where none is known); the
    call recomputed with the golden's intervals."""
    out = {}
    sdk = gold["k_reps"].std(0, ddof=1)
    base_sd = gold["sd"]
    for name, adj in (("raising factors up by one bootstrap standard deviation", +1.0),
                      ("raising factors down by one bootstrap standard deviation", -1.0)):
        r = G.run(prepared=prep, bootstrap=None, k_override=gold["k"] + adj * sdk)
        out[name] = _call_with_sd(r, base_sd)
    for name, f in (("missed links 20 per cent fewer", 0.8), ("missed links 20 per cent more", 1.2)):
        r = G.run(prepared=prep, bootstrap=None, miss_scale=f)
        out[name] = _call_with_sd(r, base_sd)
    cv = float(np.nanstd(gold["nc_mean_reps"], ddof=1) / gold["nc_mean"])
    for name, f in (("no-contact records' chance of being resident up by one bootstrap standard deviation", 1 + cv),
                    ("no-contact records' chance of being resident down by one bootstrap standard deviation", 1 - cv)):
        r = G.run(prepared=prep, bootstrap=None, nc_scale=f)
        out[name] = _call_with_sd(r, base_sd)
    for name, f in (("intervals 20 per cent wider", 1.2), ("intervals 20 per cent narrower", 0.8)):
        out[name] = _call_with_sd(gold, base_sd * f)
    return out


def _call_with_sd(r, sd):
    lo, hi = r["est"] - 1.6449 * sd, r["est"] + 1.6449 * sd
    q = sorted(d for d, l in zip(r["dists"], lo) if l >= G.LINE)
    c = sorted(d for d, l, h in zip(r["dists"], lo, hi) if l < G.LINE <= h)
    return {"qualifies": q, "too close to call": c, "est": {d: r10(e) for d, e in zip(r["dists"], r["est"])}}
