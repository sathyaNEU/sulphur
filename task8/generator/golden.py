"""task8: the golden from the cut pack alone, every rival run on the same pack to set each figure's band, the
hurried routes for the effort passes, the checks of another kind that rule out the routes the data reject, and
the range on the trust's total.

compute(target) returns {"golden", "rivals", "routes", "ruled_out", "bands", "quick", "checks", "boot"}."""
import csv
import os

import numpy as np

import link
import load
import pack as PK
import params as P
import results as R
import routes as RT

SCALAR = ["R2", "R5", "R6_total", "R8_hours", "R8_cost", "own_total"]
DICTS = ["R1", "R3", "R4", "R6", "R7", "R7_test", "R9"]
UNIT = {"R2": 0.1, "R5": 0.1, "R3": 0.1, "R4": 0.1, "R6": 1, "R6_total": 1, "R7": 1, "R7_test": 1, "R9": 0.1,
        "R8_hours": 0.1, "R8_cost": 1.0, "R1": 1, "own_total": 1}


# the least half-width of a fitted figure's band: about one standard deviation of the estimate when its linking
# samples are drawn again, for the estimators a run may reasonably choose that the rivals do not code
FLOOR = {"R2": 0.3, "R5": 0.45, "R3": 0.5, "R4": 0.5}


def bands(g, riv):
    out = {}
    for r in SCALAR:
        vals = [g[r]] + [riv[n][r] for n in riv]
        f = FLOOR.get(r, 0.0)
        out[r] = (min(min(vals) - UNIT[r] / 2, g[r] - f), max(max(vals) + UNIT[r] / 2, g[r] + f))
    for r in DICTS:
        out[r] = {}
        f = FLOOR.get(r, 0.0)
        for k, v in g[r].items():
            vals = [v] + [riv[n][r][k] for n in riv]
            out[r][k] = (min(min(vals) - UNIT[r] / 2, v - f), max(max(vals) + UNIT[r] / 2, v + f))
    return out


LUMP = 2          # a whole score group either side of the cut at an academy whose results are converted or moved
LUMP_TOTAL = 12


def widen(b, g):
    """Integer results on either side of a whole-score cut: a converted academy's count may differ by a score group
    under a defensible method the rivals do not reach, so its band carries one either side."""
    moved = {p["s"]["academy"] for p in g["placements"] if p["basis"] in ("quill", "brightway", "july")}
    for a in b["R6"]:
        if a in moved:
            lo, hi = b["R6"][a]
            b["R6"][a] = (min(lo, g["R6"][a] - LUMP - 0.5), max(hi, g["R6"][a] + LUMP + 0.5))
            lo, hi = b["R9"][a]
            b["R9"][a] = (min(lo, g["R9"][a] - LUMP * P.HOURS_PER_STUDENT - 0.05),
                          max(hi, g["R9"][a] + LUMP * P.HOURS_PER_STUDENT + 0.05))
    lo, hi = b["R6_total"]
    b["R6_total"] = (min(lo, g["R6_total"] - LUMP_TOTAL - 0.5), max(hi, g["R6_total"] + LUMP_TOTAL + 0.5))
    lo, hi = b["R8_hours"]
    b["R8_hours"] = (min(lo, g["R8_hours"] - LUMP_TOTAL * P.HOURS_PER_STUDENT - 0.05),
                     max(hi, g["R8_hours"] + LUMP_TOTAL * P.HOURS_PER_STUDENT + 0.05))
    for t in b["R7_test"]:
        if t != "Lexis" or any(p["basis"] == "july" for p in g["placements"]):
            lo, hi = b["R7_test"][t]
            b["R7_test"][t] = (min(lo, g["R7_test"][t] - 2 * LUMP - 0.5), max(hi, g["R7_test"][t] + 2 * LUMP + 0.5))
    return b


def strip(r):
    return {k: v for k, v in r.items() if k not in ("placements", "links")}


def quick(target, D):
    """Ten minutes: every exported row's own standardised score below 85, by the academy on the row."""
    acad = {a["urn"]: a["academy"] for a in csv.DictReader(open(os.path.join(target, PK.FILES["academies"]),
                                                                  encoding="utf-8"))}
    site = {a["quill_site_code"]: a["academy"] for a in csv.DictReader(open(os.path.join(target, PK.FILES["academies"]),
                                                                          encoding="utf-8"))}
    cnt = {a: 0 for a in D["academies"]}
    rows_ = {a: 0 for a in D["academies"]}
    test_of = {a: D["academies"][a]["entry_reading_test"] for a in D["academies"]}
    for r in csv.DictReader(open(os.path.join(target, PK.FILES["lexis"]), encoding="utf-8")):
        a = r["school_name"]
        if test_of.get(a) != "Lexis":
            continue
        rows_[a] += 1
        if r["standard_age_score"] and int(r["standard_age_score"]) < P.THRESHOLD:
            cnt[a] += 1
    for r in csv.DictReader(open(os.path.join(target, PK.FILES["quill"]), encoding="utf-8")):
        a = site.get(r["Site Code"])
        rows_[a] += 1
        if int(r["Standardised Score"]) < P.THRESHOLD:
            cnt[a] += 1
    for s in D["students"]:
        if s["test"] == "Brightway":
            for x in s["sittings"]:
                if x["test"] == "BRIGHTWAY":
                    rows_[s["academy"]] += 1
                    cnt[s["academy"]] += int(x["sas"] < P.THRESHOLD)
                    break
    q = {"R1": rows_, "R6": cnt, "R6_total": sum(cnt.values())}
    q["R9"] = {a: round(P.HOURS_PER_STUDENT * v, 1) for a, v in cnt.items()}
    q["R8_hours"] = round(P.HOURS_PER_STUDENT * q["R6_total"], 1)
    q["R8_cost"] = round(q["R8_hours"] * P.WEEKS * P.RATE, 2)
    return q


def evidence(D, g):
    """The checks of another kind that rule out the routes the data reject, as figures the write-up states."""
    sm = g["links"]["sm"]
    eKL = g["links"]["eKL"]
    ev = {}
    # the anchor route overstates the Brightway academies: at the switch academies, the students who sat Lexis
    # first (a first sitting) against what their KS2 results predict through the September Lexis academies
    first_l = [(l["sas"], s["ks2"]) for b, l, s in sm["pairs"] if l["date"] < b["date"] and s["ks2"] is not None]
    ev["switch_lexis_first_n"] = len(first_l)
    ev["switch_lexis_first_obs"] = float(np.mean([x for x, _ in first_l]))
    ev["switch_lexis_first_ks2_pred"] = float(np.mean([float(eKL(k)[0]) for _, k in first_l]))
    # the trial's second sitting against a first sitting, at the switch academies
    by = {}
    for b, l, s in sm["pairs"]:
        if s["academy"] in P.SWITCH_ACADEMIES:
            key = "lexis_second" if l["date"] > b["date"] else "lexis_first"
            by.setdefault(key, []).append(l["sas"] - b["sas"])
    ev["gap_lexis_second"] = float(np.mean(by["lexis_second"]))
    ev["gap_lexis_first"] = float(np.mean(by["lexis_first"]))
    ev["n_lexis_second"] = len(by["lexis_second"])
    ev["n_lexis_first"] = len(by["lexis_first"])
    # the KS2 intakes against the entry results: the students who sat Lexis in September (the reference), the
    # Quill academies' Quill sittings, the Brightway academies' first sittings, each with KS2
    ev["ks2_mean"], ev["sas_mean"] = {}, {}
    for t, rows_ in (("Lexis", [(k, x) for k, x, _ in sm["ref"]]), ("Quill", [(k, x) for k, x, _ in sm["quill"]]),
                     ("Brightway", [(s["ks2"], b["sas"]) for b, l, s in sm["pairs"] if s["ks2"] is not None
                                    and b["date"] < l["date"]])):
        ev["ks2_mean"][t] = float(np.mean([k for k, _ in rows_]))
        ev["sas_mean"][t] = float(np.mean([x for _, x in rows_]))
    # the July academies' September sitters against their July sitters, both against KS2
    return ev


def compute(target, with_rivals=True, with_routes=True, with_boot=False):
    D = load.load(target)
    g = R.all_results(D, R.GOLD)
    out = {"golden": g, "D": D}
    if with_rivals:
        riv = {nm: strip(R.all_results(D, RT.route(nm))) for nm in RT.RIVALS}
        out["rivals"] = riv
        out["bands"] = widen(bands(strip(g), riv), g)
    if with_routes:
        rt = {}
        for nm in ["careful"] + list(RT.SINGLE) + list(RT.PAIRS):
            rt[nm] = strip(R.all_results(D, RT.route(nm)))
        out["routes"] = rt
        out["ruled_out"] = {nm: strip(R.all_results(D, RT.route(nm))) for nm in RT.RULED_OUT}
    if with_boot:
        tot = R.boot(D)
        out["boot"] = {"reps": len(tot), "lo": int(np.percentile(tot, 5)), "hi": int(np.percentile(tot, 95))}
    out["quick"] = quick(target, D)
    out["evidence"] = evidence(D, g)
    out["perturbations"] = perturbations(D, g)
    return out


def perturbations(D, g):
    """Each fitted input moved by a fifth (the trial's gain, the July level) or by a whole point (the Quill
    conversion), every student placed again: the trust's cost under each."""
    Lk0 = g["links"]
    sm = Lk0["sm"]
    out = []
    for label, kind, f in [("the second-sitting gain 20 per cent lower", "gain", 0.8),
                           ("the second-sitting gain 20 per cent higher", "gain", 1.2),
                           ("the July level 20 per cent lower", "dip", 0.8),
                           ("the July level 20 per cent higher", "dip", 1.2),
                           ("the Quill conversion a point lower", "quill", -1.0),
                           ("the Quill conversion a point higher", "quill", 1.0)]:
        Lk = dict(Lk0)
        if kind == "gain":
            Lk["gain"] = Lk0["gain"] * f
            Lk["eBL"] = R.brightway_lexis(sm, R.GOLD, Lk["gain"], Lk0["eKL"])
        elif kind == "dip":
            Lk["dip"] = Lk0["dip"] * f
        else:
            base = Lk0["eQL"]
            Lk["eQL"] = (lambda b, d: (lambda x: np.asarray(b(x), float) + d))(base, f)
        n = sum(1 for p in R.place(D, Lk) if p["placed"])
        out.append({"input": label, "value": round(n * P.HOURS_PER_STUDENT * P.WEEKS * P.RATE, 2), "students": n})
    return out
