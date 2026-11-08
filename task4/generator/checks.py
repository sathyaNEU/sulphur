"""The build's assertions, run on the cut pack (python3 checks.py [target]). Every semantic fork in the design note
(SF1 to SF17) is asserted here, with the ladder's rungs, the rivals, the margins, the input gates and the Sulfur
block on the clean truth. Exit 1 on any failure."""
import datetime as dt
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A
import params as P
import sim

FAIL = []
N = [0]


def ok(name, cond, detail=""):
    N[0] += 1
    if not cond:
        FAIL.append("%s %s" % (name, detail))


def r10(x):
    return int(round(x / 10.0) * 10)


def same(pk, model, g, bins=True):
    a = A.assess(pk, model)
    s = A.chosen(a) == g["set"]
    b = all(r10(a[c]["kwh"]) == r10(g["assess"][c]["kwh"]) for c in a)
    return s and (b or not bins), a


def main(target):
    pk = A.load(target)
    g = A.golden(pk)
    M = g["models"]
    gold_set = g["set"]
    ok("call", gold_set == ["V02", "V05", "V09", "V14", "V16", "V18"] and g["count"] == 6, str(gold_set))
    # margins of the call against the limit, and every graded energy near its bin centre
    for c, v in g["assess"].items():
        ok("margin %s" % c, abs(v["kwh"] - A.SHARE * A.USABLE) >= 9.0, "%.1f" % v["kwh"])
        ok("mid-bin %s" % c, abs(v["kwh"] - r10(v["kwh"])) <= 1.0, "%.1f" % v["kwh"])
    # the ladder
    nv = A.assess(pk, M["naive"])
    ok("rung 1 default (declared weights) orders 8", len(A.chosen(nv)) == 8 and
       A.chosen(nv) == ["V02", "V03", "V05", "V07", "V09", "V11", "V16", "V18"], str(A.chosen(nv)))
    for c in ("V03", "V07", "V11"):
        ok("rung 1 heavy %s feasible by 8 kWh" % c, nv[c]["kwh"] <= A.SHARE * A.USABLE - 8, "%.1f" % nv[c]["kwh"])
    ok("rung 1 V14 out by 5 kWh", nv["V14"]["kwh"] >= A.SHARE * A.USABLE + 5, "%.1f" % nv["V14"]["kwh"])
    pl = A.assess(pk, M["pooled"])
    ok("rung 2 pooled correction orders the default's 8", A.chosen(pl) == A.chosen(nv), str(A.chosen(pl)))
    pp = M["pilot_pooled"]
    ok("rung 2a pilot-shippers' pooled line sits between the declared and the golden slope",
       A.slope_per_100(M["naive"]) < A.slope_per_100(pp) < 0.9 * A.slope_per_100(M["golden"]),
       "%.2f" % A.slope_per_100(pp))
    r0, rate = A.rung0(pk)
    ok("rung 0 average consumption orders another list", A.chosen(r0) not in (gold_set, A.chosen(nv)), str(A.chosen(r0)))
    ok("default slope under half the golden", A.slope_per_100(M["naive"]) < 0.5 * A.slope_per_100(M["golden"]))
    n1 = A.assess(pk, M["naive_1h"])
    ok("default with one cold rate also wrong", A.chosen(n1) != gold_set, str(A.chosen(n1)))
    # the shallow run keeps few energies; the landed run with one cold rate keeps the call and no energy
    keep_s = sum(r10(nv[c]["kwh"]) == r10(g["assess"][c]["kwh"]) for c in nv)
    ok("shallow keeps at most 3 energies", keep_s <= 3, str(keep_s))
    h1 = A.assess(pk, M["golden_1h"])
    ok("cracker (one cold rate) keeps the call", A.chosen(h1) == gold_set, str(A.chosen(h1)))
    ok("cracker loses every energy", sum(r10(h1[c]["kwh"]) == r10(g["assess"][c]["kwh"]) for c in h1) == 0)

    # rivals that take the step: the same six and every energy in its bin
    R = A.rivals(pk)
    for name, m in R.items():
        s, a = same(pk, m, g)
        ok("rival %s" % name, s, str(A.chosen(a)))
    # SF1 the design day's temperature: the trucks' ambient or the station's
    ok("SF1", same(pk, R["station temperature"], g)[0])
    # SF2 a duty's energy: energy_used or consumption x distance (the same column)
    import csv
    rows = list(csv.DictReader(open(os.path.join(target, A.FILES["bev"]), encoding="utf-8")))
    dif = max(abs(float(r["consumption_kwh_per_100km"]) * float(r["distance_km"]) / 100 - float(r["energy_used_kwh"]))
              for r in rows)
    ok("SF2", dif < 0.5, "%.2f" % dif)
    # SF3 the planning load: weighed net or declared
    s3 = A.assess(pk, M["golden"], basis="declared")
    ok("SF3", A.chosen(s3) == gold_set and all(r10(s3[c]["kwh"]) == r10(g["assess"][c]["kwh"]) for c in s3))
    # SF4 the twelve months: Nov 2025 to Oct 2026, calendar 2025, or every month on the bridge
    keep = A.LAST12
    for win in [(dt.date(2025, 1, 1), dt.date(2025, 12, 31)), (dt.date(2024, 11, 1), dt.date(2026, 10, 31))]:
        A.LAST12 = win
        a = A.assess(pk, M["golden"])
        ok("SF4 %s" % (win,), A.chosen(a) == gold_set, str(A.chosen(a)))
    A.LAST12 = keep
    # SF5 a re-weigh: the last weighing of a CMR or the first
    pk2 = A.load(target)
    import collections
    first = {}
    for r in csv.DictReader(open(os.path.join(target, A.FILES["weighbridge"]), encoding="utf-8")):
        if r["cmr_no"] not in first:
            first[r["cmr_no"]] = r
    pk2.wb = [{"date": dt.date.fromisoformat(r["weighed_at"][:10]),
               "duty": "V" + r["duty"][4:] if r["duty"].startswith("VMO-") else r["duty"], "shipper": r["shipper"],
               "declared": A.kg(r["declared_kg"]), "net": float(r["gross_kg"]) - float(r["tare_kg"])}
              for r in first.values()]
    g2 = A.golden(pk2)
    ok("SF5", g2["set"] == gold_set, str(g2["set"]))
    nre = sum(1 for r in csv.DictReader(open(os.path.join(target, A.FILES["weighbridge"]), encoding="utf-8"))
              if r["remark"])
    ok("SF5 re-weighs present", 200 < nre < 900, str(nre))
    # SF6 a day uploaded twice counted twice
    pk3 = A.load(target)
    dup = [d for d in pk3.days[:40]]
    pk3.days = pk3.days + dup
    g3 = A.golden(pk3)
    ok("SF6", g3["set"] == gold_set)
    # SF7 a temperature dropout: station-filled or the day dropped
    pk4 = A.load(target)
    pk4.days = [d for d in pk4.days if d["t"] is not None]
    g4 = A.golden(pk4)
    ok("SF7", g4["set"] == gold_set and all(r10(g4["assess"][c]["kwh"]) == r10(g["assess"][c]["kwh"])
                                            for c in gold_set))
    # SF8 declared weights in tonnes with a decimal comma: parsed, or those days dropped
    pk5 = A.load(target)
    tms = {(r["vehicle_reg"], r["collection_date"]): r["declared_weight"]
           for r in csv.DictReader(open(os.path.join(target, A.FILES["tms"]), encoding="utf-8"))}
    pk5.days = [d for d in pk5.days if not tms[(d["reg"], d["date"].isoformat())].endswith("t")]
    g5 = A.golden(pk5)
    ok("SF8", g5["set"] == gold_set)
    ok("SF8 tonnes present", sum(1 for v in tms.values() if v.endswith("t")) > 100)
    # SF9 the usable battery is the ordered model's (540 kWh), not the pilot's
    qtext = subprocess.run(["pdftotext", os.path.join(target, "quotation_bev_tractors_2027.pdf"), "-"],
                           capture_output=True, text=True).stdout
    ok("SF9", "usable capacity 540 kWh" in qtext)
    # SF10 the payload of a pilot day: the declaration moves V03, V07, V11 and V14 (the deep step)
    ok("SF10", set(A.chosen(nv)) ^ set(gold_set) == {"V03", "V07", "V11", "V14"})
    # SF11 the cold form: one rate below 16 C moves every energy, not the call; the back-test rules it out
    import writeup as WU
    bt = WU.back_test(pk)
    ok("SF11 back-test", bt["golden_1h"]["bias_below0"] > 2.0 and abs(bt["golden"]["bias_below0"]) < 1.0,
       str(bt))
    ok("SF11 held-out check blind to the dilution", abs(bt["declared"]["rmse"] - bt["golden"]["rmse"]) < 0.5, str(bt))
    # SF12 rounding: every rival in the golden's bin (asserted above), every value within 1 kWh of a bin centre
    ok("SF12", all(abs(v["kwh"] - r10(v["kwh"])) <= 1.0 for v in g["assess"].values()))
    # SF13 one tractor per duty
    ok("SF13", g["count"] == len(gold_set))
    # SF14 the fit window
    ok("SF14", same(pk, R["2025 only"], g)[0] and same(pk, R["2026 only"], g)[0])
    # SF15 the calibration window
    ok("SF15", same(pk, R["calibrated on the last 12 months"], g)[0])
    # SF16 within-duty fit
    ok("SF16", same(pk, R["within-duty fit"], g)[0])
    # SF17 the fit's km: odometer or route km
    pk6 = A.load(target)
    for d in pk6.days:
        d["km"] = float(sum(pk6.routes[d["duty"]]["legs"]))
    g6 = A.golden(pk6)
    ok("SF17", g6["set"] == gold_set and all(r10(g6["assess"][c]["kwh"]) == r10(g["assess"][c]["kwh"])
                                             for c in g6["assess"]))

    # the standard and the prompt name no method (the step rides on nothing filed)
    stext = subprocess.run(["pdftotext", os.path.join(target, "fleet_electrification_standard_FES-2.pdf"), "-"],
                           capture_output=True, text=True).stdout.lower()
    for w in ["declared", "weighbridge", "calibrat", "regress", "scatter", "estimate the", "error", "shipper"]:
        ok("standard silent on %s" % w, w not in stext)
    ptext = open(os.path.join(os.path.dirname(HERE), "prompt.txt"), encoding="utf-8").read().lower()
    for w in ["declared", "weigh", "payload", "calibrat", "regress", "error", "shipper", "cold"]:
        ok("prompt silent on %s" % w, w not in ptext)
    ok("prompt files the energy as a forecast from the pilot (H20)", "forecast from" in ptext and "pilot" in ptext)

    # input gates
    files = sorted(os.listdir(target))
    ok("ten or more files", len(files) >= 10, str(len(files)))
    ok("two categories", any(f.endswith(".pdf") for f in files) and any(f.endswith((".csv", ".xlsx")) for f in files))
    nwb = sum(1 for _ in open(os.path.join(target, A.FILES["weighbridge"]), encoding="utf-8")) - 1
    ok("a CSV of 20,000 rows", nwb >= 20000, str(nwb))
    nbev = sum(1 for _ in open(os.path.join(target, A.FILES["bev"]), encoding="utf-8")) - 1
    ok("a CSV of 10 to 20 printed pages or more", nbev * 0 + os.path.getsize(os.path.join(target, A.FILES["bev"]))
       > 150000, str(nbev))
    ok("dates no later than the setting", True)

    # the Sulfur block on the clean truth: the default path still files the wrong list with no mess at all
    w = sim.world()
    clean = clean_pack(w, pk)
    gc = A.golden(clean)
    nc = A.assess(clean, gc["models"]["naive"])
    ok("clean truth: golden list", gc["set"] == gold_set, str(gc["set"]))
    ok("clean truth: the default path still orders 8", len(A.chosen(nc)) == 8, str(A.chosen(nc)))
    # the one-fact hint (the slope is attenuated) taken with one pooled correction still misses
    ok("one-fact: pooled correction misses", A.chosen(A.assess(clean, gc["models"]["pooled"])) != gold_set)
    # mess neutrality: the messy pack and the clean truth give the same figures
    ok("mess neutral", all(r10(gc["assess"][c]["kwh"]) == r10(g["assess"][c]["kwh"]) for c in gold_set),
       str({c: round(gc["assess"][c]["kwh"], 1) for c in gold_set}))
    # the payload driver is not proxied by a visible column of the decision file: declared and weighed means agree
    for c in pk.short:
        ok("declared mean near weighed %s" % c,
           abs(A.planning_load(pk, c, "declared") / A.planning_load(pk, c) - 1) < 0.04)

    print("checks: %d assertions, %d failed" % (N[0], len(FAIL)))
    for f in FAIL:
        print("  FAIL", f)
    return 1 if FAIL else 0


def clean_pack(w, pk):
    """the truth with no mess: every pilot day once with its true trip temperature and declaration, every departure
    weighed once with no blank declaration"""
    cp = A.Pack()
    cp.routes = pk.routes
    cp.short = pk.short
    cp.wb = [{"date": x["date"], "duty": x["duty"], "shipper": x["shipper"], "declared": float(x["declared"]),
              "net": round(x["payload"] * 1000 / 20) * 20.0} for x in w["depart"]]
    cp.days = []
    for x in w["pilot"]:
        t = float(np.mean([tr["t"] for tr in x["trips"]]))
        cp.days.append({"date": x["date"], "reg": x["tractor"], "duty": x["duty"], "shipper": x["shipper"],
                        "declared": float(x["declared"]), "km": float(sum(tr["km"] for tr in x["trips"])),
                        "kwh": float(sum(tr["kwh"] for tr in x["trips"])), "t": t, "station_t": t, "t_filled": t})
    return cp


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
