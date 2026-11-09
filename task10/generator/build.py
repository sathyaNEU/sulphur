"""task10 architecture 5: builds the pack, the golden deliverables, figures.json, submission.md and metadata.json.
python3 task10/generator/build.py"""
import json
import os
import shutil
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import docs as D            # noqa: E402
import estim as E           # noqa: E402
import golden as GO         # noqa: E402
import pack as PK           # noqa: E402
import parse as PA          # noqa: E402
import postprocess as PP    # noqa: E402
import world as W           # noqa: E402
import writeup as WU        # noqa: E402

TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")


def rungs(X, G):
    """The rival routes the write-up names, on the pack: the linked primary as the control, the pair taken together,
    the providers at the average event day."""
    prep = X["_prep"]
    tm = E.daily_mean(X["weather"])
    ev = X["events"]
    out = {}
    for z in G["zones"]:
        code, linked = z["code"], z["linked_code"]
        recs_np = E.delivery_records(prep, tm, ev, code, partner=linked, partner_clean=False) if linked else \
            E.delivery_records(prep, tm, ev, code)
        did = E.delivery_at(recs_np, net=False, did=True, temperature=False)
        pair = E.delivery_at(E.pair_records(prep, tm, ev, code, linked), net=False) if linked else z["delivery"]
        recs = E.delivery_records(prep, tm, ev, code, partner=linked) if linked else E.delivery_records(prep, tm, ev, code)
        avg = E.delivery_at(recs, net=True, temperature=False)
        gross = E.delivery_at(E.delivery_records(prep, tm, ev, code), net=False)   # the zone's own fall read at -3.0 C
        out[z["primary"]] = dict(did=did, pair=pair, avg_delivery=avg, avg_credited=avg * z["mw28"], fall_delivery=gross,
                                 fall_after=z["before"] - gross * z["mw28"], fall_over_by=z["before"] - gross * z["mw28"] - z["firm"])
    # the colder working weekday with the design day's credit held (the unfinished chain the write-up names)
    held = E.golden_from(X, hold_credit=True)
    hz = {z["primary"]: z for z in held["zones"]}
    for p in out:
        out[p]["held_after"] = {"%.1f" % -t: hz[p]["sens"][t]["after"] for t in held["sens_Ts"]}
    return out, {"%.1f" % -t: held["commit_sens"][t] for t in held["sens_Ts"]}


def form_validation(X, G):
    """winter 2023/24 (no flexibility) checks the correction's form: the linear's largest mean error on its sub-zero
    working weekdays, and the quadratic's range."""
    fc = E.form_check(X, G["zones"])
    return dict(by_zone=fc, linear_bias_max=max(abs(v["linear"]) for v in fc.values()),
                quad_bias_min=min(v["quadratic"] for v in fc.values()),
                quad_bias_max=max(v["quadratic"] for v in fc.values()))


def figures(X, G, info):
    rg, held_sets = rungs(X, G)
    zones = {}
    for z in G["zones"]:
        zones[z["primary"]] = dict(zone=z["zone"], code=z["code"], provider=z["provider"], mw28=z["mw28"], d26=z["d26"],
                                   before=z["before"], delivery=z["delivery"], credited=z["credited"], after=z["after"],
                                   firm=z["firm"], over=bool(z["over"]), measured=z["measured"], linked=z["linked"],
                                   linked_rise=z["linked_rise"], n_events=z["n_events"], over_by=z["over_by"],
                                   sens={"%.1f" % -t: dict(after=v["after"], over=bool(v["over"]), delivery=v["delivery"])
                                         for t, v in z["sens"].items()}, **rg[z["primary"]])
    ev = X["events"]
    counts = {}
    for z in G["zones"]:
        counts[z["primary"]] = int(((ev["zone"] == z["code"]) & (ev["status"] == "Completed")).sum())
    shallow = [p for p, v in zones.items() if v["before"] - v["measured"] * v["mw28"] > v["firm"]]
    fall_call = [p for p, v in zones.items() if v["fall_over_by"] > 0]
    F = dict(call=G["commit"], default_call=shallow, fall_at_day_call=fall_call, zones=zones, steps=dict(events=counts),
             sens={"%.1f" % -t: dict(degrees_below_zero=-t, commit=G["commit_sens"][t], held_credit_commit=held_sets["%.1f" % -t])
                   for t in G["sens_Ts"]},
             validation=form_validation(X, G),
             pack=dict(scada_rows=info["scada_rows"], event_rows=info["event_rows"], weather_rows=info["weather_rows"]),
             conventions=dict(design_day_degrees_below_zero=-E.T_DESIGN, heating_base_c=E.BASE_T),
             event_temperature_c=dict(coldest_below_zero=-min(r["T"] for r in G["evidence"]),
                                      mildest=max(r["T"] for r in G["evidence"])))
    return F


def round_floats(o, nd=6):
    if isinstance(o, float):
        return round(o, nd)
    if isinstance(o, dict):
        return {k: round_floats(v, nd) for k, v in o.items()}
    if isinstance(o, list):
        return [round_floats(v, nd) for v in o]
    return o


def metadata(info):
    covers = {
        PK.F_SCADA: "The Halverton zone's SCADA historian export: the nine 33/11 kV primaries' half-hourly demand, "
                    "November to March of winters 2023/24 to 2025/26, UTC.",
        PK.F_EVENTS: "The DSO's flexibility dispatch log for the four Halverton constraint managed zones, winters 2024/25 and "
                     "2025/26, UK local time.",
        PK.F_WX: "Hourly observations at Halverton weather station, October to March of winters 2023/24 to 2025/26.",
        PK.F_REG: "The primary substation register (asset codes, SCADA points, transformers) and the DFES 2026 growth rates.",
        PK.F_FDR: "The 11 kV feeder schedule and normally-open points of the Halverton zone.",
        PK.F_GROW: "The connections team's load growth register.",
        PK.F_GUIDE: "Network Planning's winter capacity assessment guideline, issue 4, September 2026.",
        PK.F_AWARD: "The DSO's flexibility contract award notice for winter 2027/28.",
        PK.F_CI: "Customer interruptions and minutes lost by 11 kV feeder, regulatory year 2025/26.",
        PK.F_COND: "Primary transformer oil analysis and health indices, 2026.",
        PK.F_DUOS: "The use of system charging statement effective 1 April 2027.",
    }
    files = [dict(path="target/" + f, source="constructed for task10; no real dataset", date="2026-11-03",
                  licence="CC0 1.0 (constructed)", covers=covers[f]) for f in PK.FILES]
    return dict(task="task10",
                decision="the Halverton flexibility zones' primary substations whose reinforcement Wealdmoor Power Networks "
                         "commits for winter 2027/28, with each zone's provider delivery, credited flexibility and design-day "
                         "demand",
                deliverables=[GO.F_XLSX, GO.F_PPTX],
                distractor_files=["target/" + f for f in PK.DISTRACTORS],
                files=files,
                rows=dict(scada=info["scada_rows"], events=info["event_rows"], weather=info["weather_rows"]))


def main():
    T = W.build()
    shutil.rmtree(TARGET, ignore_errors=True)
    os.makedirs(TARGET)
    info = PK.write_data(T, TARGET)
    D.write_docs(TARGET)
    PP.own_mtimes(TARGET, PK.EXPORTED)
    X = PA.load(TARGET)
    G = E.golden_from(X)
    shutil.rmtree(GOLDEN, ignore_errors=True)
    GO.write(G, GOLDEN)
    PP.own_mtimes(GOLDEN, {})
    F = figures(X, G, info)
    json.dump(round_floats(F), open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    WU.write(F, os.path.join(TASK, "submission.md"))
    json.dump(metadata(info), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    # the golden ZIP: exactly the two requested files, each entry at its own last save
    PP.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"))
    print("call:", G["commit"])
    for z in G["zones"]:
        print("  %-16s delivery %.3f measured %.3f credited %.2f before %.2f after %.2f firm %.1f over %s linked %s rise %.2f"
              % (z["primary"], z["delivery"], z["measured"], z["credited"], z["before"], z["after"], z["firm"], z["over"],
                 z["linked"] or "none", z["linked_rise"]))
    return T, X, G, F


if __name__ == "__main__":
    main()
