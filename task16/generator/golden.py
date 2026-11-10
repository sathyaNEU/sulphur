"""Everything the answer blocks and the golden deliverables state, computed once from the built pack.

    G = compute(target_folder)      every result, its rivals and the hurried passes, unrounded
    F = figures(G)                  the figures as the blocks state them (written to figures.json)

Nothing here is typed: each figure is read from the pack through load.py and analysis.py, and the constants the
blocks mention are read from the generator's parameters.
"""
import math

import numpy as np

import analysis as A
import load
import params as P
import results as RS
import sweep as S

KEYS = list(RS.GRADED)                      # the six results the chain grades, in the chain's order
NAMES = {
    "trial": "the largest map trial on the benchmark's scale",
    "costs": "what each route's labels cost",
    "level": "the level at 512,000 expert labels",
    "expected": "each configuration's expected loss",
    "range": "the range round the named configuration",
    "call": "the configuration to name",
}
ROUTE_WORD = {"nA": "expert", "nB": "contractor", "nC": "map-transfer"}


def r3(x):
    return float("%.3f" % x)


def r4(x):
    return float("%.4f" % x)


def lr2(x):
    """A learning rate to two significant figures."""
    e = int(math.floor(math.log10(abs(x))))
    return round(x, 1 - e)


def compute(target):
    rows, facts = load.pilot(target)
    G = dict(rows=rows, facts=facts)
    G["golden"] = g = RS.run_pass(rows, facts, RS.GOLDEN)
    G["rivals"] = {k: RS.run_pass(rows, facts, c) for k, c in RS.rivals().items()}
    G["also"] = {k: RS.run_pass(rows, facts, c) for k, c in RS.also_ran().items()}
    G["careful"] = RS.run_pass(rows, facts, RS.CAREFUL)
    G["quick"] = RS.run_pass(rows, facts, RS.QUICK)
    G["line"] = RS.run_pass(rows, facts, RS.LINE)
    G["one_vendor"] = RS.run_pass(rows, facts, dict(RS.CAREFUL, one_vendor=True))
    G["pooled"] = {f: RS.run_pass(rows, facts, dict(RS.CAREFUL, pooled=f)) for f in RS.POOLED_FORMS}
    G["seed_range"] = RS.run_pass(rows, facts, dict(RS.GOLDEN, spread="seed"))
    # the careful pass given the levels in one sentence, two ways the sentence can be put
    G["hint_levels"] = RS.hinted(rows, facts, "free")
    G["hint_every"] = RS.hinted(rows, facts, "every")
    G["scored_only"] = RS.scored_only(rows, facts)
    # the two bounds on what more examples return past the largest runs, and the two other readings the bands hold
    G["bound_last"] = RS.run_pass(rows, facts, dict(RS.GOLDEN, form="last"))
    G["bound_none"] = RS.run_pass(rows, facts, dict(RS.GOLDEN, form="none"))
    G["pool"] = RS.run_pass(rows, facts, RS.POOL_READING)
    G["ls_floor"] = RS.run_pass(rows, facts, dict(RS.GOLDEN, form="wide"))
    G["carried"] = RS.run_pass(rows, facts, dict(RS.GOLDEN, prefer_bench=False))
    # the working the deliverables show
    yr, cal = A.with_yardstick(rows)
    G["yr"], G["cal"] = yr, cal
    rm = A.route_model(yr, 128, "y", RS.GOLDEN["lr_fix"], RS.GOLDEN["beyond"])
    G["rm"] = rm
    G["rm_unweighted"] = A.route_model(yr, 128, "y", RS.GOLDEN["lr_fix"], RS.GOLDEN["beyond"], weighted=False)
    fc = A.forecast(yr, S.SHORTLIST, "y", RS.GOLDEN["lr_fix"], RS.GOLDEN["beyond"], RS.GOLDEN["form"], RS.GOLDEN["width_rule"], rm=rm)
    G["fc"] = fc
    # the check on the runs held back, configuration by configuration
    kept = [r for r in yr if not (r["stage"] == "vend" and A.total(r) > 256000)]
    rmk = A.route_model(kept, 128, "y", RS.GOLDEN["lr_fix"], RS.GOLDEN["beyond"])
    held = {}
    for r in yr:
        if r["stage"] == "vend" and A.total(r) > 256000:
            held.setdefault((r["width"], r["nA"], r["nB"], r["nC"]), []).append(r["y"])
    G["held"] = {}
    for form in ("top", "wide", "quadratic", "line"):
        f128 = rmk["line"] if form == "line" else A.FORMS[form](rmk["levels"])[0]
        level, _ = A.level_fn(kept, rmk, f128, "y")
        out = {}
        for (w, a, b, c), v in sorted(held.items()):
            n = a + b + c
            out[(w, a, b, c)] = (level(w, n) + rmk["kB"] * b / n + rmk["kC"] * c / n, float(np.mean(v)), len(v))
        G["held"][form] = out
    G["held_by_run"] = float(np.mean([abs(G["held"]["top"][(r["width"], r["nA"], r["nB"], r["nC"])][0] - r["y"])
                                      for r in yr if r["stage"] == "vend" and A.total(r) > 256000]))
    # the logged development loss carried to the benchmark on the scored runs: what the quick pass reads
    lg, _ = RS.scored_rows(rows, RS.QUICK)
    G["logged_trial"] = A.cell(lg, "y", stage="vend", width=128, **dict(zip(("nA", "nB", "nC"), RS.BIG_CELLS["exp128k_map384k"])))[0]
    G["logged_gap"] = {}
    for r in yr:
        k = "expert" if r["nB"] + r["nC"] == 0 else ("contractor" if r["nC"] == 0 else "map")
        G["logged_gap"].setdefault(k, []).append(r["dev"] - r["y"])
    G["lr_cost"] = {w: A.table_lr_cost(yr, w) for w in (64, 128, 256)}
    # each route's cost read pair by pair at 128,000 examples, both sides on the carried loss: a trial against the
    # expert-label run of the same total, width and rate
    e128 = A.cell(yr, "yhat", width=128, nA=128000, nB=0, nC=0, lr=float(A.TUNED_LR[128]))[0]
    G["same_total"] = {}
    for a, b, c in ((64000, 0, 64000), (32000, 0, 96000), (64000, 64000, 0), (32000, 96000, 0)):
        m = A.cell(yr, "yhat", stage="vend", width=128, nA=a, nB=b, nC=c)[0]
        G["same_total"][(a, b, c)] = (m - e128) / (10.0 * (b + c) / float(a + b + c))
    return G


def figures(G):
    g = G["golden"]; f = G["facts"]; c = G["careful"]; q = G["quick"]
    lv = g["_levels"]
    order = g["call"]["order"]
    also = G["also"]
    fam = G["rivals"]; quad = fam[RS.QUADRATIC]
    cen = [v for k, v in fam.items() if RS.central(k)]
    mae = {"wide": G["ls_floor"]["heldback"],
           "quadratic": quad["heldback"],
           "line": also["the straight line through the levels"]["heldback"]}
    s_run, s_cal = g["range"]["parts"]["run"], g["range"]["parts"]["yardstick"]
    F = {
        "call": "B",
        "call_width": 512,
        "runner_up": order[1],
        "margin": r3(g["call"]["margin"]),
        "expected": {k: r3(v) for k, v in g["expected"].items()},
        "range_low": r3(g["range"]["low"]),
        "range_high": r3(g["range"]["high"]),
        "range_parts": {k: r4(v) for k, v in g["range"]["parts"].items()},
        "range_sd": r4(g["range"]["sd"]),
        "lr_1024": lr2(g["rate"]),
        "lr_exponent": float("%.1f" % g["rate_exponent"]),
        "lr_best": {str(w): lr2(v) for w, v in g["_lr_opt"].items()},
        "run_records": f["run_ids"], "runs_finished": f["complete"], "runs_unfinished": f["run_ids"] - f["complete"],
        "runs_with_item_scores": f["with_item_scores"],
        "bench_rows": f["sub_rows"], "bench_scored": f["sub_scored"], "bench_final": f["sub_final"],
        "bench_part_way": f["sub_part_way"], "bench_repeats": f["sub_duplicates"],
        "dev_items": f["items"], "dev_expert_items": f["expert_items"],
        "trial_map384": r3(g["trial"]["exp128k_map384k"]),
        "cal_intercept": r4(G["cal"]["a"]), "cal_slope": r3(G["cal"]["b"]), "cal_sd": r4(G["cal"]["sd"]), "cal_n": G["cal"]["n"],
        "cal_offset": r3(G["cal"]["a"] + (G["cal"]["b"] - 1.0) * 0.68),
        "cost_ctr": r4(g["costs"]["ctr_per10"]), "cost_map": r4(g["costs"]["map_per10"]),
        "level_128k": r3(lv[128000]), "level_256k": r3(lv[256000]), "level_512k": r3(g["level"]),
        "gain_first": r3(lv[128000] - lv[256000]), "gain_second": r3(lv[256000] - lv[512000]),
        "gain_ladder": r3(-A.ladder_line(G["yr"], 128, "y", "matched")[1]),
        "gap": r4(g["heldback"]), "gap_by_run": r4(G["held_by_run"]),
        "gap_floor_ls": r4(mae["wide"]), "gap_quadratic": r4(mae["quadratic"]), "gap_line": r4(mae["line"]),
        "width_step_512": r4(g["_width"]["g512"][128000]),
        "width_gap_256": {str(k // 1000): r4(v) for k, v in g["_width"]["g256"].items()},
        "hurried": {
            "careful_pick": c["call"]["pick"], "careful_margin": r3(c["call"]["margin"]),
            "careful_expected": {k: r3(v) for k, v in c["expected"].items()},
            "careful_level": r3(c["level"]), "careful_gap": r3(c["heldback"]), "careful_form": c["_form"],
            "careful_range": [r3(c["range"]["low"]), r3(c["range"]["high"])],
            "quick_pick": q["call"]["pick"], "quick_expected": {k: r3(v) for k, v in q["expected"].items()},
            "quick_trial": r3(G["logged_trial"]),
            "line_pick": G["line"]["call"]["pick"], "line_expected": {k: r3(v) for k, v in G["line"]["expected"].items()},
            "line_level": r3(G["line"]["level"]), "line_map": r4(G["line"]["costs"]["map_per10"]),
            "nomatch_ctr": r4(G["also"]["routes read against the ladder as it ran"]["costs"]["ctr_per10"]),
            "nomatch_map": r4(G["also"]["routes read against the ladder as it ran"]["costs"]["map_per10"]),
            "nomatch_level": r3(G["also"]["routes read against the ladder as it ran"]["level"]),
            "raw_expected_B": r3(G["also"]["expert items read without the benchmark calibration"]["expected"]["B"]),
            "floor_ls_expected": {k: r3(v) for k, v in G["ls_floor"]["expected"].items()},
            "floor_ls_margin": r3(G["ls_floor"]["call"]["margin"]),
            "hint_levels_expected": {k: r3(v) for k, v in G["hint_levels"]["expected"].items()},
            "hint_every_expected": {k: r3(v) for k, v in G["hint_every"]["expected"].items()},
            "quadratic_margin": r3(quad["call"]["margin"]),
            "careful_half": r3(RS.half_width(c["range"])),
            "seed_half": r4(RS.half_width(G["seed_range"]["range"])),
            "seed_range": [r3(G["seed_range"]["range"]["low"]), r3(G["seed_range"]["range"]["high"])],
            "scored_only_A": r3(G["scored_only"]["expected"]["A"]),
            "last_rate": S.TUNED_LR[512],
            "logged_gap_expert": [r3(min(G["logged_gap"]["expert"])), r3(max(G["logged_gap"]["expert"]))],
            "logged_gap_map": [r3(min(G["logged_gap"]["map"])), r3(max(G["logged_gap"]["map"]))],
            "lr_cost_128": r3(float(np.mean(list(G["lr_cost"][128].values())))),
        },
        "counts": {"finished": f["complete"], "final_scored": f["sub_final"]},
        "costs": {"contractor": r4(g["costs"]["ctr_per10"]), "map_transfer": r4(g["costs"]["map_per10"])},
        "range": {"B_low": r3(g["range"]["low"]), "B_high": r3(g["range"]["high"]), "half_width": r3(RS.half_width(g["range"]))},
        "range_half": r3(RS.half_width(g["range"])),
        "half_run_yardstick": r3(RS.Z80 * math.sqrt(s_run ** 2 + s_cal ** 2)),
        # the lead: over the runner-up here, across the family on the golden's continuation, and at its least
        "lead_over_C": r3(g["expected"]["C"] - g["expected"]["B"]),
        "lead_central": [r3(min(v["call"]["margin"] for v in cen)), r3(max(v["call"]["margin"] for v in cen))],
        "lead_least": r3(min(v["call"]["margin"] for v in fam.values())),
        "family_size": len(fam),
        "family_names": sorted({v["call"]["pick"] for v in fam.values()}),
        # what the continuation past the largest runs can be: the last gain undiminished, or none
        "bounds": {k: [r3(G["bound_last"]["expected"][k]), r3(G["bound_none"]["expected"][k])] for k in ("C", "D")},
        "gap_family": [r4(min(v["heldback"] for v in cen)), r4(max(v["heldback"] for v in cen))],
        # the other sound reading of the routes: the level at or under the pool from the expert-label runs themselves
        "pool_reading": {"ctr": r4(G["pool"]["costs"]["ctr_per10"]), "map": r4(G["pool"]["costs"]["map_per10"]),
                         "level_256k": r3(G["pool"]["_levels"][256000]), "level_512k": r3(G["pool"]["level"]),
                         "B": r3(G["pool"]["expected"]["B"])},
        # the same costs read pair by pair at 128,000 examples (half and three quarters of the set moved)
        "same_total_map": [r4(G["same_total"][(64000, 0, 64000)]), r4(G["same_total"][(32000, 0, 96000)])],
        "same_total_ctr": [r4(G["same_total"][(64000, 64000, 0)]), r4(G["same_total"][(32000, 96000, 0)])],
        "carried_B": r3(G["carried"]["expected"]["B"]),
        "width_step_512_runs": sum(1 for r in G["yr"] if r["bench"] is not None and r["nA"] == 128000 and r["nB"] + r["nC"] == 0 and
                                   ((r["width"] == 256 and abs(r["lr"] - A.TUNED_LR[256]) < 1e-12) or
                                    (r["width"] == 512 and abs(r["lr"] - A.TUNED_LR[512]) < 1e-12))),
        "carried_A": r3(G["carried"]["expected"]["A"]),
        "others_spread": r3(max(g["expected"][k] for k in order[1:]) - min(g["expected"][k] for k in order[1:])),
        "curve_ratio": float("%.2f" % g["_form"]["ratio"]),
        "careful_c_cost": r3(G["fc"]["forecast"]["C"]["cost"]),
        "c_examples_gain": r3(G["fc"]["level"](256, 256000) - G["fc"]["forecast"]["C"]["level"]),
        "pooled": {
            "C": [float("%.2f" % min(v["expected"]["C"] for v in G["pooled"].values())), float("%.2f" % max(v["expected"]["C"] for v in G["pooled"].values()))],
            "B": [float("%.2f" % min(v["expected"]["B"] for v in G["pooled"].values())), float("%.2f" % max(v["expected"]["B"] for v in G["pooled"].values()))],
            "level": [float("%.2f" % min(v["level"] for v in G["pooled"].values())), float("%.2f" % max(v["level"] for v in G["pooled"].values()))],
            "gap": float("%.2f" % float(np.mean([v["heldback"] for v in G["pooled"].values()]))),
            "names": sorted({v["call"]["pick"] for v in G["pooled"].values()}),
        },
        "quick_C": float("%.2f" % q["expected"]["C"]),
        "min_bench": r3(min(r["bench"] for r in G["rows"] if r["bench"] is not None)),
        "line_as_run_512k": r3(A.ladder_line(G["yr"], 128, "y", "none")[0](512000)),
        "bands": {"trial": list(RS.BANDS["trial"]["exp128k_map384k"]), "costs_contractor": list(RS.BANDS["costs"]["ctr_per10"]),
                  "costs_map": list(RS.BANDS["costs"]["map_per10"]), "level": list(RS.BANDS["level"]),
                  "rate": list(RS.BANDS["rate"]), "expected": {k: list(v) for k, v in RS.BANDS["expected"].items()},
                  "range_low": list(RS.BANDS["range"]["low"]), "range_high": list(RS.BANDS["range"]["high"]),
                  "range_half": list(RS.BANDS["range"]["half"])},
        "constants": {
            "widths": [64, 128, 256, 512, 1024], "ladder_sizes": list(S.LADDER_SIZES), "bench_points": P.BENCH_N,
            "batch": P.BATCH, "epochs": P.EPOCHS, "slot_hours": 120, "quota": 32,
            "shortlist": [{"option": o["key"], "width": o["width"], "expert": o["nA"], "contractor": o["nB"],
                           "map_transfer": o["nC"], "total": o["nA"] + o["nB"] + o["nC"], "lr": o["lr"]} for o in S.SHORTLIST],
            "trial": list(RS.BIG_CELLS["exp128k_map384k"]), "held_above": 256000, "level_at": 512000, "level_lr": 0.002,
            "held_totals": 512000, "expert_pool": P.POOL["A"], "contractor_lot": P.POOL["B"], "map_lot": P.POOL["C"],
        },
    }
    return F
