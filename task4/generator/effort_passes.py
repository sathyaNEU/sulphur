"""effort.json: the client's effort test computed on the cut pack (python3 effort_passes.py [target]). Each pass is the
author's implementation of a named method, run end to end on the shipped files; nothing reads the prompt.

  quick      the pilot's mean energy per km on days at or below -5 C times each block's kilometres, against 85 per cent
             of the quoted usable battery, the per-block verdicts summed; the night as battery energy; no diesel work
  careful    what a frontier run does unprompted, on this pack: every file cleaned and joined, the diesel use per block
             tank to tank by least squares for the fuel ask, the pilot's energy per km by block, the fuel heaters' share
             read from the HVO fills once the register's heater line and the quotation's heating row are read side by
             side (graded up: a leak reader noticed the heaters on a read), the pilot's fit carried to the blocks it never
             ran on climb and hours per km, the first-winter loss on a curved age form, the charging losses as the
             sessions' pooled ratio, the night scheduled exactly on those figures
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

    def pack(E, rates, lim, taken, dem, loss, heater, gapv, cond):
        return {"R1": {c: round(rates[c], 1) for c in pk.weekday} if rates else None,
                "R2": gapv, "R3": heater,
                "R4": {c: r10(E[c]) for c in pk.weekday},
                "R5": loss,
                "R6": {c: "yes" if E[c] <= lim else "no" for c in pk.weekday},
                "R7": cond, "R8": round(dem / 1000.0, 1), "R9": sorted(taken)}

    gold = pack(g["E"], g["rates"], g["limit"], g["taken"], g["demand_kwh"], figs["loss_pct"], figs["heater_kw"], figs["pilot_gap"],
                figs["cond_kw"])
    careful = pack(car["E"], car["rates"], car["limit"], car["taken"], car["demand_kwh"], round(100 * car["loss"], 1),
                   round(car["parts"]["heater_lph"] * A.HEATER_KWH_PER_L, 1), None, None)
    careful["R2"] = {"value": None, "grade": "missed", "why": "the pass computes every block's diesel figure for the fuel ask and never "
                     "sets the pilot blocks against the rest: the fuel-card file is dismissed for the forecast because litres do not measure "
                     "battery energy, so the selection is never stated"}
    careful["R7"] = {"value": None, "grade": "missed", "why": "the pass takes the charging losses as the sessions' pooled ratio of the "
                     "battery's gain to the metered energy and files no draw beside the recharge: a year of mostly mild nights averages the "
                     "battery's conditioning into one efficiency, read as if every night were the same"}
    quick = pack(qk["E"], None, qk["limit"], qk["taken"], qk["demand_kwh"], None, None, None, None)
    bands = {c: [v - WU.E_TOL, v + WU.E_TOL] for c, v in figs["energy"].items()}
    cb = figs["conventions"]["cond_band"]
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
        {"id": "R7", "name": "the conditioning draw on charge at -15 C, kW", "graded_as": "Component 3", "figure": "cond_kw",
         "depends": [], "independent": "", "golden": figs["cond_kw"], "band": list(cb), "partly": [cb[0] - 0.6, cb[1] + 0.6]},
        {"id": "R8", "name": "the design night's draw with every qualifying block on charge, MWh", "graded_as": "Ask 5",
         "figure": "demand_mwh", "depends": ["R4", "R6", "R7"], "independent": "", "golden": figs["demand_mwh"],
         "band": [round(figs["demand_mwh"] - WU.NIGHT_TOL, 2), round(figs["demand_mwh"] + WU.NIGHT_TOL, 2)],
         "partly": [round(figs["demand_mwh"] - 0.6, 2), round(figs["demand_mwh"] + 0.6, 2)]},
        {"id": "R9", "name": "the order: the count and the blocks", "graded_as": "Recommendation", "figure": "call_set",
         "depends": ["R4", "R5", "R7"], "independent": "", "golden": figs["call_set"]},
    ]
    for r in res:
        r["passes"] = {"quick": quick[r["id"]], "careful": careful[r["id"]], "thorough": gold[r["id"]]}
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping"))
    import effort as EF
    # the hints: the careful pass with one step put right
    hb = A.careful(pk, "golden")                       # the bridge put right (the heaters already read from the fills)
    h1 = pack(hb["E"], hb["rates"], hb["limit"], hb["taken"], hb["demand_kwh"], round(100 * hb["loss"], 1),
              round(hb["parts"]["heater_lph"] * A.HEATER_KWH_PER_L, 1), gap(hb["rates"]), None)
    hc = A.careful(pk, "j1_wrong", True)               # the conditioning put right, the bridge still missing
    h2 = pack(hc["E"], hc["rates"], hc["limit"], hc["taken"], hc["demand_kwh"], round(100 * hc["loss"], 1),
              round(hc["parts"]["heater_lph"] * A.HEATER_KWH_PER_L, 1), None, round(hc["cond_kw"], 1))
    h3 = dict(careful)                                 # the heaters are already read and the night already capped
    hints = []
    for sent, h in (("the pilot blocks were chosen for their low diesel use, and the diesel figures carry the difficulty the "
                     "timetable's kilometres, climb and speed miss", h1),
                    ("on a cold night a bus on charge also takes power through its charger to keep its battery warm, which "
                     "the sessions' average ratio spreads over a year of mild nights", h2),
                    ("the pilot buses heated the cabin with fuel below about -4 C, and the night period's capacity caps the "
                     "order below the blocks that pass the limit", h3)):
        rescued = []
        for r in res:
            gc = EF.grade(careful[r["id"]], r)[0]
            gh = EF.grade(h[r["id"]], r)[0]
            if gh == "right" and gc != "right":
                rescued.append(r["id"])
        hints.append({"sentence": sent, "rescues": rescued, "count": len(h["R9"])})
    routes = [{"name": k, "answer": v, "golden": k == "golden"} for k, v in figs["route_sets"].items()]
    out = {"results": res, "hints": hints, "routes": routes,
           "careful_dismissed": {"the fuel-card file for the forecast": "diesel litres do not measure battery energy",
                                 "the sessions' cold nights": "averaged into one charging efficiency"},
           "careful_variants": {"careful without the night's supply": figs["routes"]["the careful pass without the night's supply"]}}
    json.dump(out, open(os.path.join(HERE, "effort.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print("effort.json: careful order %d, quick %d, golden %d; hints rescue %s" %
          (len(careful["R9"]), len(quick["R9"]), len(gold["R9"]), [h["rescues"] for h in hints]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
