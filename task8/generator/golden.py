"""task8 architecture 18: the golden figures from core.compute on the shipped seed, written to figures.json for
figures_check.py and drafted into the write-up and the deliverables."""
import json

import numpy as np

import params as P
import world as W

REGION_NAME = {r[0]: r[1] for r in P.REGIONS}


def item_rows(w, r):
    """One row per 2027 item, in paper order: position, code, pool, strand, context, stem words, difficulty for a
    Level 1 candidate, chance at the standard, inside the band."""
    it, g = w["it"], r["gold"]
    rows = []
    for pos, i in enumerate(w["papers"]["L1-2027"]):
        ch = float(W.sig(g["theta"] - g["b"][i]))
        rows.append(dict(pos="Q%02d" % (pos + 1), item=str(it["code"][i]), pool="Level %s" % it["pool"][i][1],
                         strand=W.STRAND_NAME[it["strand"][i]], context="everyday" if it["everyday"][i] else "mathematical",
                         words=int(it["words"][i]), b=float(g["b"][i]), chance=ch,
                         inside=bool(P.BAND[0] <= ch <= P.BAND[1])))
    return rows


def figures(w, r):
    g, d = r["gold"], r["default"]
    m = g["model"]["coef"]
    items = item_rows(w, r)
    pr_rows = [x for x in items if x["pool"] == "Level 2"]
    out = {
        "pass_mark": g["pass_mark"],
        "expected_golden": round(g["expected"], 2),
        "expected_bank": round(d["expected"], 2),
        "pass_mark_bank": d["pass_mark"],
        "standard_raw": P.STANDARD_RAW,
        "items_on_paper": len(w["papers"]["L1-2027"]),
        "band_low": P.BAND[0],
        "band_high": P.BAND[1],
        "stem_words_per_cost_unit": 100,
        "theta_standard": round(g["theta"], 2),
                "reading_cost_per_100_words": round(float(m[1]), 2),
        "everyday_advantage": round(float(m[2]), 2),
        "n_bridging": int(len(g["tab"]["items"])),
        "pr_items": len(pr_rows),
        "pr_mean_shift": round(float(np.mean([x["b"] for x in pr_rows]) - np.mean(
            [r["lv"]["l2"]["b"][int(np.where(w["it"]["code"] == x["item"])[0][0])] for x in pr_rows])), 2),
        "pr_expected_golden": round(sum(x["chance"] for x in pr_rows), 2),
        "pr_expected_bank": round(sum(float(W.sig(d["theta"] - d["b"][int(np.where(w["it"]["code"] == x["item"])[0][0])]))
                                      for x in pr_rows), 2),
        "items_below_band": [x["pos"] for x in items if not x["inside"] and x["chance"] < P.BAND[0]],
        "items_above_band": [x["pos"] for x in items if not x["inside"] and x["chance"] > P.BAND[1]],
        "chances": {x["pos"]: round(x["chance"], 2) for x in items},
        "regions": {REGION_NAME[k]: int(round(v[0])) for k, v in r["reg_golden"].items()},
        "regions_unrounded": {REGION_NAME[k]: round(v[0], 2) for k, v in r["reg_golden"].items()},
        "region_counts": {REGION_NAME[k]: v[1] for k, v in r["reg_golden"].items()},
        "rival_screen": round(r["screen"]["expected"], 2),
        "rival_context": round(r["ctx"]["expected"], 2),
        "rival_reading": round(r["read"]["expected"], 2),
        "lp_mean_shift_rel": None,
    }
    tab = g["tab"]
    sets = w["it"]["sets"]
    for nm in ("sp", "sa", "lp"):
        sel = np.isin(tab["items"], sets[nm])
        out["shift_%s" % nm] = round(float(tab["d"][sel].mean()), 2)
    out["lp_mean_shift_rel"] = round(out["shift_lp"] - out["shift_sa"], 2)
    out["sp_mean_shift_rel"] = round(out["shift_sp"] - out["shift_sa"], 2)
    return out


def write_figures(w, r, path):
    f = figures(w, r)
    open(path, "w").write(json.dumps(f, indent=1, sort_keys=True) + "\n")
    return f
