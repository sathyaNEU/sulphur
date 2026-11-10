"""effort.json: the client's effort test computed on the cut pack (python3 effort_passes.py [target]). Each pass is the
author's implementation of a named method, run end to end on the shipped files; nothing reads the prompt.

  quick      the pilot's mean energy per km on days at or below -5 C times each block's kilometres, against 85 per cent
             of the quoted usable battery, the per-block verdicts summed; no diesel work, no night
  careful    the union of what the six recorded Fryele runs did, on this pack: every file cleaned and joined, the diesel
             use per block tank to tank by least squares for the fuel ask, the pilot's energy per km by block, a
             piecewise-linear cold response fitted on the pilot's own HVAC record and read at -15 C, the pilot's fit
             carried to the blocks it never ran on climb and hours per km, the first-winter loss on a curved age form,
             the charging efficiency from the sessions, the night scheduled under the agreement's capacity
  thorough   the golden

Each hint is executed literally: the careful pass with that one step done right, graded like the passes; a hint
rescues the results it turns from not Right to Right.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import writeup as WU  # noqa: E402

r10 = WU.r10


def main(target):
    pk = A.load(target)
    g = A.golden(pk)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    car = A.careful(pk)
    qk = A.quick(pk)
    pilot = figs["pilot_blocks"]
    others = [c for c in pk.weekday if c not in pilot]

    def gap(rates):
        import numpy as np
        return round(float(np.mean([rates[c] for c in others]) - np.mean([rates[c] for c in pilot])), 1)

    def pack(E, rates, lim, taken, grid, loss, heater, gapv):
        return {"R1": {c: round(rates[c], 1) for c in pk.weekday} if rates else None,
                "R2": gapv, "R3": heater,
                "R4": {c: r10(E[c]) for c in pk.weekday},
                "R6": {c: "yes" if E[c] <= lim else "no" for c in pk.weekday},
                "R5": loss, "R7": round(grid / 1000.0, 1), "R8": sorted(taken)}

    gold = pack(g["E"], g["rates"], g["limit"], g["taken"], g["demand_kwh"], figs["loss_pct"], figs["heater_kw"], figs["pilot_gap"])
    careful = pack(car["E"], car["rates"], car["limit"], car["taken"], car["demand_kwh"], round(100 * car["loss"], 1), None, None)
    careful["R2"] = {"value": None, "grade": "missed", "why": "the pass computes every block's diesel figure for the fuel ask and never "
                     "sets the pilot blocks against the rest: the fuel-card file is dismissed for the forecast because litres do not measure "
                     "battery energy, so the selection is never stated"}
    careful["R3"] = {"value": None, "grade": "missed", "why": "the pass reads the pilot's own HVAC record at -15 C and files no figure for "
                     "the heat the fuel heaters supplied: the electric buses' HVO fills are not read as cabin heat"}
    quick = pack(qk["E"], None, qk["limit"], qk["taken"], qk["demand_kwh"], None, None, None)
    bands = {c: [v - WU.E_TOL, v + WU.E_TOL] for c, v in figs["energy"].items()}
    res = [
        {"id": "R1", "name": "diesel l/100 km per weekday block (48 cells)", "graded_as": "Ask 1", "figure": "diesel",
         "depends": [], "independent": "", "golden": figs["diesel"],
         "bands": {c: [v - WU.R1_TOL, v + WU.R1_TOL] for c, v in figs["diesel"].items()}, "partly_share": 0.6},
        {"id": "R2", "name": "the pilot blocks' diesel gap to the rest, l/100 km", "graded_as": "Component 1", "figure": "pilot_gap",
         "depends": ["R1"], "independent": "", "golden": figs["pilot_gap"],
         "band": [figs["pilot_gap"] - WU.GAP_TOL, figs["pilot_gap"] + WU.GAP_TOL], "partly": [figs["pilot_gap"] - 2.0, figs["pilot_gap"] + 2.0]},
        {"id": "R3", "name": "the fuel heaters' heat at -15 C, kW", "graded_as": "Component 2", "figure": "heater_kw",
         "depends": [], "independent": "", "golden": figs["heater_kw"], "band": list(figs["conventions"]["heat_band"]),
         "partly": [figs["conventions"]["heat_band"][0] - 0.6, figs["conventions"]["heat_band"][1] + 0.6]},
        {"id": "R4", "name": "the 48 design-day energies", "graded_as": "Ask 2", "figure": "energy",
         "depends": ["R1", "R3"], "independent": "", "golden": figs["energy"], "bands": bands, "partly_share": 0.6},
        {"id": "R5", "name": "first-winter loss of usable battery, per cent", "graded_as": "Ask 4", "figure": "loss_pct",
         "depends": [], "independent": "", "golden": figs["loss_pct"], "band": list(WU.LOSS_BAND),
         "partly": [WU.LOSS_BAND[0] - 0.6, WU.LOSS_BAND[1] + 0.6]},
        {"id": "R6", "name": "each block's verdict", "graded_as": "Ask 3", "figure": "verdict",
         "depends": ["R4", "R5"], "independent": "", "golden": figs["verdict"], "partly_share": 0.8,
         "partly_share_why": "a constant answer (every block electric) already gets %d of 48 verdicts, so partial credit starts "
                             "at four fifths of the blocks" % figs["qualifying_count"]},
        {"id": "R7", "name": "the design night's demand of every qualifying block at the connection point, MWh", "graded_as": "Ask 5",
         "figure": "demand_mwh", "depends": ["R4", "R6"], "independent": "", "golden": figs["demand_mwh"],
         "band": [figs["demand_mwh"] - WU.NIGHT_TOL, figs["demand_mwh"] + WU.NIGHT_TOL],
         "partly": [figs["demand_mwh"] - 0.6, figs["demand_mwh"] + 0.6]},
        {"id": "R8", "name": "the order: the count and the blocks", "graded_as": "Recommendation", "figure": "call_set",
         "depends": ["R4", "R5"], "independent": "", "golden": figs["call_set"]},
    ]
    for r in res:
        r["passes"] = {"quick": quick[r["id"]], "careful": careful[r["id"]], "thorough": gold[r["id"]]}
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping"))
    import effort as EF
    # the hints: the careful pass with one step put right
    E1, _ = A.design_energies(pk, "j2_wrong", g["rates"])        # the bridge right, the heaters still missing
    t1 = A.night_cut(pk, E1, car["limit"], car["eta"])
    h1 = pack(E1, car["rates"], car["limit"], t1[0], sum(E1[c] / car["eta"] for c in t1[4]), round(100 * car["loss"], 1), None, figs["pilot_gap"])
    E2, _ = A.design_energies(pk, "j1_wrong", g["rates"])        # the heaters right, the bridge still missing
    t2 = A.night_cut(pk, E2, car["limit"], car["eta"])
    h2 = pack(E2, car["rates"], car["limit"], t2[0], sum(E2[c] / car["eta"] for c in t2[4]), round(100 * car["loss"], 1), figs["heater_kw"], None)
    h3 = dict(careful)                                           # the night's cap is already applied by the careful pass
    hints = []
    for sent, h in (("the pilot blocks were chosen for their low diesel use, and the diesel figures carry the difficulty the "
                     "timetable's kilometres, climb and speed miss", h1),
                    ("the pilot buses heated the cabin with fuel below about -4 C, and the quoted buses take that heat from the "
                     "battery", h2),
                    ("the night period's capacity caps the order below the blocks that pass the limit", h3)):
        rescued = []
        for r in res:
            gc = EF.grade(careful[r["id"]], r)[0]
            gh = EF.grade(h[r["id"]], r)[0]
            if gh == "right" and gc != "right":
                rescued.append(r["id"])
        hints.append({"sentence": sent, "rescues": rescued, "count": len(h["R8"])})
    routes = [{"name": k, "answer": v, "golden": k == "golden"} for k, v in figs["route_sets"].items()]
    out = {"results": res, "hints": hints, "routes": routes,
           "careful_dismissed": {"the fuel-card file for the forecast": "diesel litres do not measure battery energy",
                                 "the electric buses' HVO fills": "read as fuel purchases, not as cabin heat"},
           "careful_variants": {"careful without the night's supply": figs["routes"]["the careful pass without the night's supply"]}}
    json.dump(out, open(os.path.join(HERE, "effort.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print("effort.json: careful order %d, quick %d, golden %d; hints rescue %s" %
          (len(careful["R8"]), len(quick["R8"]), len(gold["R8"]), [h["rescues"] for h in hints]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
