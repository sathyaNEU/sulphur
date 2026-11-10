"""effort.json: the client's effort test computed on the cut pack (python3 effort_passes.py [target]). Each pass is
the author's implementation of a named method, run end to end on the shipped files by golden.compute; nothing reads
the prompt.

  quick      the plan's arithmetic: node-hours available at the mean availability over the pooled use ratio; the
             other asks unanswered
  careful    the union of what frontier runs do unprompted: every batch de-duplicated, every clock read, the use
             ratios by standing computed because they are asked, the outage record read from the log, the run-time
             family chosen by AIC on the censored record (a Weibull), submissions resampled, availability carried as
             a constant, requeues seen but the lost work not priced, the grants read through one pooled ratio for the
             forward load, a backtest run and explained away
  thorough   the golden

Each hint is executed literally: the careful pass with that one input done right (the single-shortcut routes run the
other way round: the golden with one input in its hurried form, so the hint's rescue is the complement).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD

STEP = GD.STEP


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    g = json.load(open(os.path.join(HERE, "golden_state.json")))
    cap = figs["cap"]
    req = figs["requests_total"]
    rc = figs["route_caps"]
    cut = lambda c: int(round(100 * max(0.0, 1.0 - c / req)))
    # the careful pass's figures result by result
    lost = figs["lost_by_quarter"]
    r4_gold = {"q1": lost["1"], "q2": lost["2"], "q3": lost["3"], "multi": figs["multi_share_pct"], "sw": figs["repair_software_h"],
               "hw": figs["repair_hardware_d"], "rack": figs["repair_rack_h"]}
    rows_med = figs["rows_not_rejoined"]
    r4_careful = dict(r4_gold)
    r4_careful.update({"sw": int(round(rows_med["software_h"])), "hw": round(rows_med["hardware_d"] * 2) / 2.0, "rack": int(round(rows_med["rack_h"]))})
    r2_gold = {"new": figs["use_new_pct"], "cont": figs["use_cont_pct"], "expected": figs["expected_use_requests"], "burst": figs["burst_index"]}
    r2_careful = {"new": figs["use_new_pct"], "cont": figs["use_cont_pct"], "expected": figs["expected_use_requests"], "burst": 1}
    r2_quick = {"new": figs["use_pooled_pct"], "cont": figs["use_pooled_pct"], "expected": figs["expected_use_pooled"], "burst": None}
    r3_gold = {"mean96": figs["mean96_h"], "share48": figs["share48_pct"]}
    r3_careful = {"mean96": figs["weibull_mean96_h"], "share48": figs["weibull_share48_pct"]}
    r3_quick = {"mean96": figs["cut48_mean96_h"], "share48": 0}
    m96lo, m96hi = figs["passing_mean96_range"]
    s48lo, s48hi = figs["passing_share48_range"]
    res = [
        {"id": "R1", "name": "the Q3 2026 record: jobs and node-hours", "graded_as": "Ask 5", "figure": "q3_record",
         "depends": [], "independent": "", "golden": {"jobs": figs["q3_jobs"], "nh": figs["q3_nh"]},
         "bands": {"jobs": [figs["q3_jobs"] - 5, figs["q3_jobs"] + 5], "nh": [figs["q3_nh"] - 500, figs["q3_nh"] + 500]},
         "passes": {"quick": {"jobs": int(round(figs["q3_segments"] / 10.0) * 10), "nh": figs["q3_nh"]},
                    "careful": {"jobs": figs["q3_jobs"], "nh": figs["q3_nh"]}, "thorough": {"jobs": figs["q3_jobs"], "nh": figs["q3_nh"]}}},
        {"id": "R2", "name": "use of grants by standing, the round's expected use, the burst index", "graded_as": "Ask 3 and Component 1",
         "figure": "r2_cells", "depends": [], "independent": "", "golden": r2_gold,
         "bands": {"new": [r2_gold["new"] - 0.5, r2_gold["new"] + 0.5], "cont": [r2_gold["cont"] - 0.5, r2_gold["cont"] + 0.5],
                   "expected": [r2_gold["expected"] - 5000, r2_gold["expected"] + 5000], "burst": [r2_gold["burst"] - 0.5, r2_gold["burst"] + 0.5]},
         "passes": {"quick": r2_quick, "careful": r2_careful, "thorough": r2_gold}},
        {"id": "R3", "name": "the run time under 96 h and the work beyond 48 h", "graded_as": "Ask 4 and Component 2",
         "figure": "r3_cells", "depends": [], "independent": "", "golden": r3_gold,
         "bands": {"mean96": [min(m96lo, r3_gold["mean96"] - 0.5), max(m96hi, r3_gold["mean96"] + 0.5)],
                   "share48": [min(s48lo, r3_gold["share48"] - 2.5), max(s48hi, r3_gold["share48"] + 2.5)]},
         "passes": {"quick": r3_quick, "careful": r3_careful, "thorough": r3_gold}},
        {"id": "R4", "name": "the 2026 outage record", "graded_as": "Ask 6 and Component 3", "figure": "r4_cells",
         "depends": [], "independent": "", "golden": r4_gold,
         "bands": {"q1": [r4_gold["q1"] - 5, r4_gold["q1"] + 5], "q2": [r4_gold["q2"] - 5, r4_gold["q2"] + 5], "q3": [r4_gold["q3"] - 5, r4_gold["q3"] + 5],
                   "multi": [r4_gold["multi"] - 0.5, r4_gold["multi"] + 0.5], "sw": [r4_gold["sw"] - 0.5, r4_gold["sw"] + 0.5],
                   "hw": [r4_gold["hw"] - 0.25, r4_gold["hw"] + 0.25], "rack": [r4_gold["rack"] - 0.5, r4_gold["rack"] + 0.5]},
         "passes": {"quick": None, "careful": r4_careful, "thorough": r4_gold}},
        {"id": "R5", "name": "the share of 2026's work redone after node failures", "graded_as": "Ask 7 and Component 4",
         "figure": "rework_pct", "depends": [], "independent": "", "golden": figs["rework_pct"],
         "band": [figs["rework_pct"] - 0.5, figs["rework_pct"] + 0.5],
         "passes": {"quick": None, "careful": figs["rework_whole_segment_pct"], "thorough": figs["rework_pct"]}},
        {"id": "R6", "name": "the backtest on Q3 2026", "graded_as": "Ask 2 and Component 5", "figure": "backtest_p90_h",
         "depends": ["R2", "R3", "R4", "R5"], "independent": "", "golden": figs["backtest_p90_h"],
         "band": [figs["backtest_p90_h"] - 0.5, figs["backtest_p90_h"] + 0.5],
         "passes": {"quick": None, "careful": figs["backtest_careful_h"], "thorough": figs["backtest_p90_h"]}},
        {"id": "R7", "name": "the cap and the cut", "graded_as": "Recommendation and Ask 1", "figure": "cap",
         "depends": ["R2", "R3", "R4", "R5"], "independent": "", "golden": cap, "band": [cap - STEP / 2, cap + STEP / 2],
         "passes": {"quick": figs["quick_cap"], "careful": rc["careful but hurried"], "thorough": cap}},
    ]
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping"))
    import effort as EF
    # hints: the careful pass with one input put right; a hint rescues the results it turns to Right
    one = {
        "the run-time families must be validated on the May 2026 change (fit on jobs censored at 24 hours, predict the "
        "24 to 48 hour window) rather than chosen by AIC, and the tail extrapolated to 96 hours":
            {"R3": r3_gold, "R7": rc["careful but hurried"]},
        "node failures cluster by rack (a switch or a power feed) and repairs take hours to days; availability is not a "
        "constant": {"R4": r4_gold, "R7": rc["careful but hurried"]},
        "a job killed by a node failure restarts from its last checkpoint, so the work since then is done twice; price "
        "it from the requeued jobs' excess over like jobs": {"R5": figs["rework_pct"], "R7": rc["careful but hurried"]},
        "submissions arrive in sessions of near-identical jobs, so the forward demand must keep that burst structure":
            {"R2": r2_gold, "R7": rc["careful but hurried"]},
    }
    hints = []
    for sent, fix in one.items():
        rescued = []
        for r in res:
            gc = EF.grade(r["passes"]["careful"], r)[0]
            v = fix.get(r["id"], r["passes"]["careful"])
            gh = EF.grade(v, r)[0]
            if gh == "right" and gc != "right":
                rescued.append(r["id"])
        hints.append({"sentence": sent, "rescues": rescued})
    routes = [{"name": "the golden", "answer": cap, "golden": True}]
    for k, v in rc.items():
        routes.append({"name": k, "answer": int(v), "golden": False})
    out = {"results": res, "hints": hints, "routes": routes,
           "route_cuts_pct": {k: cut(v) for k, v in rc.items()},
           "careful_backtest_h": figs["backtest_careful_h"], "careful_family": "weibull",
           "single_input_caps": {k: int(v) for k, v in rc.items()}}
    json.dump(out, open(os.path.join(HERE, "effort.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print("effort.json: golden cap %d; careful %d; quick %d; routes %s; hints rescue %s" % (
        cap, rc["careful but hurried"], figs["quick_cap"], {k: int(v) for k, v in rc.items()}, [h["rescues"] for h in hints]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
