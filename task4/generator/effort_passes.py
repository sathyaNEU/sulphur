"""effort.json: the client's effort test computed on the cut pack (python3 effort_passes.py [target]). Each pass is
the author's implementation of a named method, run end to end on the shipped files; nothing reads the prompt.

  quick      the pilot's average consumption on January-like days times each duty's km, against 85 per cent of the
             quoted battery
  careful    the union of what the four recorded platform runs (architectures 7 and 8) did: every file cleaned, each
             declaration taken to its weighed equivalent on the terminal's weighed-on-declared line per shipper and
             note period, a curved cold form, the trailer's tare on every leg, each load taken off at its drops, the
             square of speed with each duty fed its routing-tool speed at the year's actual-to-planned ratio, the
             battery loss as a straight line in age beside a level per tractor and the day's cold; the within-duty
             payload slope, the same-months-a-year-apart loss and the first-year-only loss computed and set aside
  thorough   the golden

Each hint is executed literally: the careful pass with that one step done right, graded like the passes; a hint
rescues the results it turns from not Right to Right. The careful pass at the design-day speed (what the
architecture 8 runs' timing of the design day amounts to) is recorded beside it as a variant.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A
import golden as GD
import writeup as WU

r10 = GD.r10


def main(target):
    pk = A.load(target)
    g = A.golden(pk)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    R = A.routes(pk)

    def build(key, ratio, loss):
        m, lm = R[key]
        a = A.assess(pk, m, lim=lm)
        inp = g["inputs"]
        cells = {"V02 combination t": round(inp["V02"]["combo"], 1) if m["o"]["tare"] else round(g["pilot_combo"], 1),
                 "V14 combination t": round(inp["V14"]["combo"], 1) if m["o"]["tare"] else round(g["pilot_combo"], 1),
                 "V03 load share": round(inp["V03"]["phi"], 2) if m["o"]["drops"] == "yes" else 1.0,
                 "V11 load share": round(inp["V11"]["phi"], 2) if m["o"]["drops"] == "yes" else 1.0}
        return {"R1": round(A.slope_per_100(m), 1), "R2": round(100 * loss, 1),
                "R3": {c: r10(a[c]["kwh"]) for c in sorted(a)},
                "R4": {c: "yes" if a[c]["go"] else "no" for c in sorted(a)}, "R5": A.chosen(a),
                "assembly": cells, "speed_ratio": round(ratio, 2)}

    ry, rw = A.speed_ratio(pk, how="mean"), A.speed_ratio(pk)
    lc, lg = A.careful_fade(pk), g["fade"]
    gold = build("golden", rw, lg)
    car = build("careful but hurried", ry, lc)
    qa, _ = A.rung0(pk)
    quick = {"R1": None, "R2": None, "R3": {c: r10(qa[c]["kwh"]) for c in sorted(qa)},
             "R4": {c: "yes" if qa[c]["go"] else "no" for c in sorted(qa)}, "R5": A.chosen(qa)}
    pb, lb, rb = WU.PAY_BAND, WU.LOSS_BAND, WU.RATIO_BAND
    res = [
        {"id": "R1", "name": "payload term, kWh per t per 100 loaded km", "graded_as": "Component 1",
         "figure": "payload_term", "depends": [], "independent": "", "golden": figs["payload_term"],
         "band": list(pb), "partly": [1.6, 2.6]},
        {"id": "R2", "name": "first-year battery loss, per cent", "graded_as": "Component 2", "figure": "loss_pct",
         "depends": [], "independent": "", "golden": figs["loss_pct"], "band": list(lb), "partly": [3.8, 6.0]},
        {"id": "R3", "name": "the 14 design-day energies", "graded_as": "Ask 1", "figure": "energy",
         "depends": ["R1"], "independent": "", "golden": figs["energy"],
         "bands": {c: [v - 10, v + 10] for c, v in figs["energy"].items()}},
        {"id": "R4", "name": "each duty's verdict", "graded_as": "Ask 2", "figure": "verdict",
         "depends": ["R2", "R3"], "independent": "", "golden": figs["verdict"], "partly_share": 0.75,
         "partly_share_why": "a constant answer (every duty electric) already gets 8 of 14 verdicts, so partial credit "
                             "starts at three quarters of the duties"},
        {"id": "R5", "name": "the order", "graded_as": "Recommendation", "figure": "call_set",
         "depends": ["R2", "R3"], "independent": "", "golden": figs["call_set"]},
    ]
    for r in res:
        r["passes"] = {"quick": quick[r["id"]], "careful": car[r["id"]], "thorough": gold[r["id"]]}
        if r["id"] == "R5":
            for p in ("quick", "careful"):
                v = r["passes"][p]
                if v != r["golden"]:
                    r["passes"][p] = {"value": v, "grade": "missed",
                                      "why": "the order is graded as the count and the duties; %d is not %d" %
                                             (len(v), len(r["golden"]))}
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping"))
    import effort as EF
    one = {
        "the pilot's regional duties carry lighter loads than the same shippers' terminal runs, so the terminal's "
        "calibration line does not carry to them": ("careful, own-duty loads", ry, lc),
        "the batteries lose most of their first year's capacity in the first months": ("careful, curved loss", ry, lg),
        "the duties drive slower than the routing tool plans on a -5 C day than over the year":
            ("careful, design-day speed", rw, lc),
    }
    hints = []
    for sent, (key, ratio, loss) in one.items():
        h = build(key, ratio, loss)
        rescued = []
        for r in res:
            gc = EF.grade(car[r["id"]], r)[0]
            gh = EF.grade(h[r["id"]], r)[0]
            if gh == "right" and gc != "right":
                rescued.append(r["id"])
        hints.append({"sentence": sent, "rescues": rescued, "order": h["R5"]})
    routes = []
    for k, (m, lm) in R.items():
        aa = A.assess(pk, m, lim=lm)
        routes.append({"name": k, "answer": A.chosen(aa), "golden": k == "golden"})
    routes.append({"name": "quick (average cold-day consumption)", "answer": A.chosen(qa), "golden": False})
    variant = build("careful, design-day speed", rw, lc)
    grades = {r["id"]: EF.grade(variant[r["id"]], r)[0] for r in res}
    if variant["R5"] != figs["call_set"]:
        grades["R5"] = "missed"
    singles = {}
    for key, ratio, loss in (("careful, own-duty loads", ry, lc), ("careful, curved loss", ry, lg),
                             ("careful, design-day speed", rw, lc)):
        v = build(key, ratio, loss)
        gr = {r["id"]: EF.grade(v[r["id"]], r)[0] for r in res}
        if v["R5"] != figs["call_set"]:
            gr["R5"] = "missed"
        singles[key] = {"grades": gr, "order": v["R5"],
                        "assembly_cells_right": all(abs(v["assembly"][k] - figs["combination_and_drops"][k]) < 1e-9
                                                    for k in v["assembly"])}
    out = {"results": res, "hints": hints, "routes": routes,
           "careful_dismissed": {"within-duty payload slope": figs["payload_term_fe_careful"],
                                 "loss, same months a year apart": figs["loss_pct_yoy"],
                                 "loss, straight line on the first year's days": figs["loss_forms"]["first_year"]},
           "careful_variant_design_day_speed": {"values": variant, "grades": grades},
           "careful_with_one_correction": singles,
           "careful_assembly": car["assembly"]}
    json.dump(out, open(os.path.join(HERE, "effort.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print("effort.json: careful order %d %s, variant %d, quick %d; hints rescue %s" %
          (len(car["R5"]), car["R5"], len(variant["R5"]), len(quick["R5"]), [len(h["rescues"]) for h in hints]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
