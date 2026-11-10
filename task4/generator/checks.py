"""The build's assertions, run on the cut pack (python3 checks.py [target]). Every semantic fork in the design note
(SF1 to SF23) is asserted here, with each hurried route's order, the rivals, the margins, the back-test, the
battery loss, the no-free-check screen, the input gates and the clean truth. Exit 1 on any failure."""
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


def same(pk, model, g, lim=None, tol=10.0):
    a = A.assess(pk, model, lim=g["limit"] if lim is None else lim)
    s = A.chosen(a) == g["set"]
    near = all(abs(a[c]["kwh"] - g["assess"][c]["kwh"]) <= tol for c in a)
    return s and near, a


GOLD_SET = ["V03", "V05", "V09", "V11", "V16", "V18", "V33"]
# each shortcut's designed flips against the golden order
FLIPS = {
    "no speed term": {"V14", "V30"},
    "the routing tool's speed": set(GOLD_SET),
    "the year's mean speed ratio": {"V03", "V11", "V33"},
    "declared weights": {"V07"},
    "one cold rate": {"V14", "V30"},
    "no first-year loss": {"V14", "V30"},
    "no trailer weight": {"V02", "V14"},
    "no fridge draw": {"V24", "V30"},
    "every reefer draws": {"V30", "V33"},
    "the load to the last drop": {"V03", "V11"},
    "careful but hurried": {"V03", "V11"},
}
NEW = ("no trailer weight", "no fridge draw", "every reefer draws", "the load to the last drop")
PAY_BAND = (1.95, 2.45)


def main(target):
    TARGET_DIR[0] = target
    pk = A.load(target)
    g = A.golden(pk)
    M = g["models"]
    gold_set = g["set"]
    L = g["limit"]
    ok("call", gold_set == GOLD_SET and g["count"] == 7, str(gold_set))
    for c, v in g["assess"].items():
        ok("margin %s 13 kWh or more" % c, abs(v["kwh"] - L) >= 13.0, "%.1f against %.1f" % (v["kwh"], L))
    # the routes: each hurried step alone lands on its own wrong order, clear of the limit
    R = A.routes(pk)
    sets = {k: A.chosen(A.assess(pk, m, lim=lm)) for k, (m, lm) in R.items()}
    for k, want in FLIPS.items():
        ok("route %s flips %s" % (k, sorted(want)), set(sets[k]) ^ set(gold_set) == want, str(sets[k]))
    for k in NEW:
        ok("new judgment %s flips two or more" % k, len(FLIPS[k]) >= 2)
    wrong = {tuple(v) for k, v in sets.items() if v != gold_set}
    ok("five or more distinct wrong orders", len(wrong) >= 5, str(len(wrong)))
    for k, (m, lm) in R.items():
        if k == "golden":
            continue
        a = A.assess(pk, m, lim=lm)
        ok("route %s no duty within 1.5 kWh of its limit" % k, min(abs(a[c]["kwh"] - lm) for c in a) >= 1.5,
           str({c: round(a[c]["kwh"] - lm, 1) for c in a if abs(a[c]["kwh"] - lm) < 1.5}))
        if k in FLIPS and k != "no first-year loss":
            out = [c for c in pk.short if abs(a[c]["kwh"] - g["assess"][c]["kwh"]) > 10]
            ok("route %s misreads two or more energies by over 10 kWh" % k, len(out) >= 2, str(out))
            moved = [c for c in out if c not in FLIPS[k]]
            ok("route %s misreads a duty where nothing turns on it" % k, len(moved) >= 1 or k == "every reefer draws",
               str(moved))
    # R1: the payload term, every rival inside its band and every hurried route outside it
    pt = A.slope_per_100(M["golden"])
    ok("payload term mid-band", PAY_BAND[0] + 0.1 < pt < PAY_BAND[1] - 0.1, "%.3f" % pt)
    for k in ("declared weights", "one pooled correction", "no trailer weight", "no fridge draw",
              "the load to the last drop", "careful but hurried", "no speed term"):
        v = A.slope_per_100(R[k][0])
        ok("payload term outside the band on %s" % k, not PAY_BAND[0] <= v <= PAY_BAND[1], "%.3f" % v)
    gp = A.payloads(pk, "shipper")
    fe, fse = A.fe_slope_se(pk, gp)
    ok("the within-duty slope's error four times the pooled fit's", fse >= 4 * A.golden_se(pk, gp),
       "%.3f against %.3f" % (fse, A.golden_se(pk, gp)))
    ok("tare and payload terms agree within 0.6 (a tonne is a tonne)", abs(g["tare_term"] - pt) < 0.6,
       "%.2f against %.2f" % (g["tare_term"], pt))
    ok("payload term near the truth", abs(pt - 100 * P.LOAD) < 0.2, "%.3f" % pt)
    # R3: the fridge unit, read from the pilot's dairy duty: the ePTO units draw, the others do not
    ok("fridge draw near the truth", abs(g["tru_kw"] - P.TRU_KW) < 0.4, "%.2f" % g["tru_kw"])
    y = np.array([d["kwh"] for d in pk.days])
    X = A.design(pk, gp, g["model"]["o"])
    res = y - X @ g["model"]["coef"]
    other = np.array([d["reefer"] and not d["epto"] for d in pk.days])
    ok("the diesel and axle-generator reefers' days show no draw", abs(res[other].mean()) < 3.0,
       "%.2f" % res[other].mean())
    ok("the shortlisted reefer duties: V24 and V30 ePTO, V33 diesel",
       [c for c in pk.short if g["inputs"][c]["epto"] == 1.0] == ["V24", "V30"]
       and [c for c in pk.short if g["inputs"][c]["reefer"] == 1.0] == ["V24", "V30", "V33"]
       and all(g["inputs"][c]["epto"] in (0.0, 1.0) for c in pk.short))
    # the footprints: every structure runs across the terminal, not only through the deciding duties
    tr = pk.trailer
    vdut = {c for c, v in pk.vdep.items() if any("ePTO" in tr[x["trailer"]]["equip"] for x in v)}
    ok("ePTO units on Värnamo duties off the shortlist", len(vdut - set(pk.short)) >= 2, str(sorted(vdut)))
    md = {c for c, v in pk.vdep.items() if len(pk.stops[c]) > 1}
    ok("multi-drop duties off the shortlist", len(md - set(pk.short)) >= 6, str(len(md - set(pk.short))))
    heavy = {r["duty"] for r in pk.wb if tr[r["trailer"]]["tare"] >= 10000}
    ok("heavy trailers off the shortlist", len(heavy - set(pk.short)) >= 3, str(sorted(heavy - set(pk.short))))
    ok("the pilot carries every structure", any(d["epto"] for d in pk.days) and any(d["n_drops"] > 1 for d in pk.days)
       and np.std([d["combo"] for d in pk.days]) > 1.0)
    # every route that takes all the steps: the same seven, every energy within 10 kWh
    RV = A.rivals(pk)
    for name, (m, lm) in RV.items():
        a = A.assess(pk, m, lim=lm)
        ok("rival %s keeps the order" % name, A.chosen(a) == gold_set, str(A.chosen(a)))
        ok("rival %s clear of the limit" % name, min(abs(a[c]["kwh"] - lm) for c in a) >= 1.5)
        if name != "within-duty fit":
            ok("rival %s energies within 10 kWh" % name,
               max(abs(a[c]["kwh"] - g["assess"][c]["kwh"]) for c in a) <= 10.0)
            v = A.slope_per_100(m)
            ok("rival %s payload term in the band" % name, PAY_BAND[0] <= v <= PAY_BAND[1], "%.3f" % v)
    # the cold form, out of sample
    gp = A.payloads(pk, "shipper")
    b1, b2, bq = A.backtest(pk, gp, A.H1), A.backtest(pk, gp, A.H2), A.backtest(pk, gp, ("quad", 16))
    ok("one cold rate under-forecasts held-out sub-zero days by 4 per cent or more", b1[0] <= -4.0, str(b1))
    ok("two rates within 1.5 per cent", abs(b2[0]) <= 1.5 and abs(bq[0]) <= 1.5, str((b2, bq)))
    bd = A.backtest(pk, A.payloads(pk, "declared"), A.H2)
    ok("held-out days blind to the declarations", abs(bd[1] - b2[1]) < 1.0, str((bd, b2)))
    # the first-year loss
    f = g["fade"]
    for how in ("linear", "quad", "cold15", "yoy"):
        ok("loss %s within 0.2 points" % how, abs(A.fade(pk, how) - f) <= 0.002, "%.4f" % A.fade(pk, how))
    ok("loss by age alone low by 0.4 points or more", A.fade(pk, "age") <= f - 0.004, "%.4f" % A.fade(pk, "age"))
    ok("loss near the truth", abs(f - P.FADE_Y1) <= 0.003, "%.4f" % f)
    # no free check: no pilot shipper declares exactly over the whole pilot, the drinks maker's scale days too few
    import writeup as WU
    cal = A.calibration(pk)
    pilot = {d["shipper"] for d in pk.days}
    ok("no pilot shipper's notes exact over the whole window", not any(
        abs(v[1] - 1) < 0.05 for (s, r), v in cal.items() if s in pilot and r == "all"))
    tm = A.ticket_months(pk, "GDR")
    mk = np.array([d["shipper"] == "GDR" and (d["date"].year, d["date"].month) in tm for d in pk.days])
    ok("scale-weight pilot days under 90", 20 < mk.sum() < 90, str(mk.sum()))
    dp = A.payloads(pk, "declared")
    X = A.design(pk, dp, form=A.H1, tare=None, tru=None)
    y = np.array([d["kwh"] for d in pk.days])
    keep = [k for k in range(X.shape[1]) if np.ptp(X[mk][:, k]) > 1e-9]
    Xm = X[mk][:, keep]
    c = np.linalg.lstsq(Xm, y[mk], rcond=None)[0]
    r = y[mk] - Xm @ c
    se = np.sqrt(r @ r / (mk.sum() - Xm.shape[1]) * np.linalg.inv(Xm.T @ Xm)[-1, -1]) * 100
    ok("scale-weight days alone cannot pin the payload term", se >= 0.4, "%.2f" % se)
    est = [v[1] for (s, rr), v in cal.items() if s in pilot and P.SHIPPERS[s][2] == "est" and rr != "ticket"]
    ok("estimating clerks' slopes 0.1 to 0.25", all(0.1 <= x <= 0.25 for x in est), str(est))
    # the battery never runs below its reserve on a pilot day
    # the speed transfer: the pilot cannot show the Varnamo duties' speeds directly, and a model without speed
    # validates on the pilot
    nos = A.fit(pk, gp, A.H2, speed=None)
    ok("speed term improves the pilot fit only modestly", 0.05 < nos["rmse_pct"] - g["model"]["rmse_pct"] < 0.6,
       "%.2f against %.2f" % (nos["rmse_pct"], g["model"]["rmse_pct"]))
    vmax = max(d["v"] for d in pk.days)
    ok("every shortlisted duty's routing-tool speed above any pilot day's actual",
       min(A.plan_speed(pk, c) for c in pk.short) > vmax, "%.1f" % vmax)
    rr = A.speed_ratio(pk)
    ok("winter speed ratio near the truth", abs(rr - sim.ratio(P.DESIGN_T)) < 0.01, "%.3f" % rr)
    ok("pilot SOC end at 5 per cent or more", min(d["soc1"] for d in pk.days) >= 5, str(min(d["soc1"] for d in pk.days)))
    # SF1 the design day's temperature: the trucks' ambient or the station's
    ok("SF1", same(pk, RV["station temperature"][0], g)[0])
    # SF2 a duty's energy: energy_used or consumption x distance (the same column)
    import csv
    rows = list(csv.DictReader(open(os.path.join(target, A.FILES["bev"]), encoding="utf-8")))
    dif = max(abs(float(r["consumption_kwh_per_100km"]) * float(r["distance_km"]) / 100 - float(r["energy_used_kwh"]))
              for r in rows)
    ok("SF2", dif < 0.5, "%.2f" % dif)
    # SF3 the planning load: weighed net or declared
    s3 = A.assess(pk, M["golden"], basis="declared", lim=L)
    ok("SF3", A.chosen(s3) == gold_set and all(abs(s3[c]["kwh"] - g["assess"][c]["kwh"]) <= 6 for c in s3))
    # SF4 the twelve months: Nov 2025 to Oct 2026, calendar 2025, or every month on the bridge
    keep = A.LAST12
    for win in [(dt.date(2025, 1, 1), dt.date(2025, 12, 31)), (dt.date(2024, 11, 1), dt.date(2026, 10, 31))]:
        A.LAST12 = win
        a = A.assess(pk, M["golden"], lim=L)
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
               "declared": A.kg(r["declared_kg"]), "net": float(r["gross_kg"]) - float(r["tare_kg"]),
               "trailer": r["trailer_reg"]} for r in first.values()]
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
    ok("SF7", g4["set"] == gold_set and all(abs(g4["assess"][c]["kwh"] - g["assess"][c]["kwh"]) <= 6
                                            for c in gold_set))
    # SF8 declared weights in tonnes with a decimal comma: parsed, or those days dropped
    pk5 = A.load(target)
    tms = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(target, A.FILES["tms"]), encoding="utf-8")):
        tms[(r["vehicle_reg"], r["collection_date"])].append(r["declared_weight"])
    pk5.days = [d for d in pk5.days if not any(v.endswith("t") for v in tms[(d["reg"], d["date"].isoformat())])]
    g5 = A.golden(pk5)
    ok("SF8", g5["set"] == gold_set)
    ok("SF8 tonnes present", sum(1 for v in tms.values() if any(x.endswith("t") for x in v)) > 100)
    # SF9 the usable battery is the ordered model's (540 kWh), not the pilot's
    qtext = subprocess.run(["pdftotext", os.path.join(target, "quotation_bev_tractors_2027.pdf"), "-"],
                           capture_output=True, text=True).stdout
    ok("SF9", "usable capacity 540 kWh" in qtext)
    # SF10 the payload of a pilot day: the declaration moves V03, V07, V11 and V14 (asserted with the routes)
    # SF11 the cold form: asserted with the back-test above
    # SF12 rounding: every rival within 6 kWh of the golden (asserted above); energies graded within 10 kWh
    # SF13 one tractor per duty
    ok("SF13", g["count"] == len(gold_set))
    # SF14 the fit window, SF15 the calibration window, SF16 within-duty fit, SF18 note periods, SF19 to SF22 the loss
    for k in ("2025 only", "2026 only", "calibrated on the last 12 months",
              "one shipper line over both note periods", "loss: the day's temperature",
              "loss: temperature and its square", "loss: degrees below 15 C", "loss: the same months a year apart"):
        ok("SF %s" % k, same(pk, RV[k][0], g, RV[k][1])[0])
    ok("SF18 the drinks maker's notes, one line over both periods",
       same(pk, *[RV["one shipper line over both note periods"][i] for i in (0,)], g, RV["one shipper line over both note periods"][1])[0])
    ok("SF19 the loss's temperature term", all(abs(A.fade(pk, h) - f) <= 0.002 for h in ("linear", "quad", "cold15")))
    ok("SF20 the loss estimator: the same months a year apart", abs(A.fade(pk, "yoy") - f) <= 0.002)
    # SF21 "permanently": the cold's loss returns each spring, so the age trend alone is low (asserted above)
    ok("SF21 the cold's capacity loss is reversible", A.fade(pk, "age") < f - 0.004)
    ok("SF22 the limit", abs(L - A.SHARE * A.USABLE * (1 - f)) < 1e-9)
    ok("SF24 the design-day speed: the routing tool's and the year's ratio each order otherwise",
       sets["the routing tool's speed"] != gold_set and sets["the year's mean speed ratio"] != gold_set
       and A.speed_ratio(pk) < A.speed_ratio(pk, how="mean") - 0.05)
    ok("SF25 the speed term's form", same(pk, RV["speed: a straight line"][0], g, RV["speed: a straight line"][1])[0])
    ok("SF26 the ratio's form", all(same(pk, RV[k][0], g, RV[k][1])[0] for k in RV if k.startswith("speed ratio")))
    ok("SF16 the within-duty fit keeps the order", A.chosen(A.assess(pk, RV["within-duty fit"][0], lim=L)) == gold_set)
    # SF27 the trailers a duty runs with: its own, from the weighbridge's trailer registrations or from its notes
    for c in pk.short:
        wbt = np.mean([pk.trailer[r["trailer"]]["tare"] for r in pk.wb if r["duty"] == c and A.LAST12[0] <= r["date"] <= A.LAST12[1]])
        nt = np.mean([pk.trailer[x["trailer"]]["tare"] for x in pk.vdep[c]])
        ok("SF27 %s trailer tare from the bridge or the notes" % c, abs(wbt - nt) < 60, "%.0f %.0f" % (wbt, nt))
    # SF28 which units draw from the battery: ePTO only (asserted with the routes: every reefer flips V30 and V33)
    ok("SF28", sets["every reefer draws"] != gold_set and sets["no fridge draw"] != gold_set)
    # SF29 the drops' shares: declared shares, or equal shares (inside the band, same call)
    ok("SF29", same(pk, RV["drops: equal shares"][0], g)[0])
    # SF30 the tare term: its own coefficient, or the payload's (same call, payload term in the band)
    ok("SF30", same(pk, RV["tare: one coefficient with the payload"][0], g)[0])
    # SF31 the fridge unit's hours: depot out to depot in, driving hours, or per km (same call)
    ok("SF31", same(pk, RV["fridge unit: by driving hours"][0], g)[0] and same(pk, RV["fridge unit: by km"][0], g)[0])
    # SF32 the 2027 tractor's own weight: the quotation's, or the pilot tractors' (same call)
    keep_t = A.TRACTOR_2027_KG
    A.TRACTOR_2027_KG = float(np.mean(list(pk.tractor_tare[r] for r in {d["reg"] for d in pk.days})))
    pk.__dict__.pop("_inp", None)
    a32 = A.assess(pk, g["model"], lim=L)
    A.TRACTOR_2027_KG = keep_t
    pk.__dict__.pop("_inp", None)
    ok("SF32", A.chosen(a32) == gold_set and max(abs(a32[c]["kwh"] - g["assess"][c]["kwh"]) for c in a32) <= 10)
    ok("SF32 the quotation states the unladen weight", "11,980 kg" in qtext)
    # SF33 the combination's tare: the register's trailer tare, or the bridge's stored tare less the diesel tractor
    dvt = {}
    for r in csv.DictReader(open(os.path.join(target, A.FILES["weighbridge"]), encoding="utf-8")):
        if r["tractor_reg"] in pk.tractor_tare:
            dvt.setdefault(r["trailer_reg"], set()).add(round(float(r["tare_kg"]) - pk.tractor_tare[r["tractor_reg"]]))
    ok("SF33", all(v == {round(pk.trailer[t]["tare"])} for t, v in dvt.items()), str(len(dvt)))
    # SF34 a duty's combination tare over several trailers: each departure's trailer, or each distinct trailer once
    tt = g["tare_term"] / 100
    for c in pk.short:
        regs = [r["trailer"] for r in pk.wb if r["duty"] == c and A.LAST12[0] <= r["date"] <= A.LAST12[1]]
        simple = A.TRACTOR_2027_KG / 1000 + np.mean([pk.trailer[t]["tare"] for t in set(regs)]) / 1000
        d = abs(simple - g["inputs"][c]["combo"])
        ok("SF34 %s combination within 0.3 t and 3 kWh" % c, d <= 0.3 and d * tt * sum(pk.routes[c]["legs"]) <= 3.0,
           "%.3f t" % d)
    # SF23 the usable battery: the quoted 540 less the loss, not the pilot's
    ok("SF23", abs(g["usable_y1"] - 540 * (1 - f)) < 1e-6)
    # SF17 the fit's km: odometer or route km
    pk6 = A.load(target)
    for d in pk6.days:
        d["km"] = float(sum(pk6.routes[d["duty"]]["legs"]))
    g6 = A.golden(pk6)
    ok("SF17", g6["set"] == gold_set and all(abs(g6["assess"][c]["kwh"] - g["assess"][c]["kwh"]) <= 6
                                             for c in g6["assess"]))

    # the standard and the prompt name no method (the step rides on nothing filed)
    stext = subprocess.run(["pdftotext", os.path.join(target, "fleet_electrification_standard_FES-2.pdf"), "-"],
                           capture_output=True, text=True).stdout.lower()
    for w in ["declared", "weighbridge", "calibrat", "regress", "scatter", "estimate the", "error", "shipper",
              "state of charge", "below 0", "freez", "trailer", "tare", "fridge", "refrig", "reefer", "pto", "speed",
              "hour"]:
        ok("standard silent on %s" % w, w not in stext)
    ok("standard files the duty's drops (2.1)", "drops" in stext)
    ptext = open(os.path.join(os.path.dirname(HERE), "prompt.txt"), encoding="utf-8").read().lower()
    for w in ["declared", "weigh", "calibrat", "regress", "error", "shipper", "cold", "temperature", "hold",
              "scatter", "freez", "state of charge", "trailer", "tare", "fridge", "refrig", "reefer", "drop", "speed",
              "weight of"]:
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
    ntv = sum(1 for _ in open(os.path.join(target, A.FILES["tmsv"]), encoding="utf-8")) - 1
    ok("the Värnamo consignments over 10,000 rows", ntv > 10000, str(ntv))

    # the clean truth: no mess, the same order, and each hurried step still wrong
    w = sim.world()
    clean = clean_pack(w, pk)
    gc = A.golden(clean)
    ok("clean truth: golden order", gc["set"] == gold_set, str(gc["set"]))
    ok("clean truth: loss", abs(gc["fade"] - f) < 0.003, "%.4f" % gc["fade"])
    RC = A.routes(clean)
    for k in ("declared weights", "one cold rate", "no first-year loss", "no trailer weight", "no fridge draw",
              "the load to the last drop", "careful but hurried"):
        m, lm = RC[k]
        ok("clean truth: %s still wrong" % k, A.chosen(A.assess(clean, m, lim=lm)) != gold_set)
    ok("mess neutral", all(abs(gc["assess"][c]["kwh"] - g["assess"][c]["kwh"]) <= 7 for c in pk.short),
       str({c: round(gc["assess"][c]["kwh"] - g["assess"][c]["kwh"], 1) for c in pk.short}))
    for c in pk.short:
        ok("declared mean near weighed %s" % c,
           abs(A.planning_load(pk, c, "declared") / A.planning_load(pk, c) - 1) < 0.05)
    # the answer blocks: no em dash
    sub = open(os.path.join(os.path.dirname(HERE), "submission.md"), encoding="utf-8").read()
    ok("no em dash in the blocks", "\u2014" not in sub)

    print("checks: %d assertions, %d failed" % (N[0], len(FAIL)))
    for f in FAIL:
        print("  FAIL", f)
    return 1 if FAIL else 0


def clean_pack(w, pk):
    """the truth with no mess: every pilot day once with its true trip temperature, declaration, drop shares and
    trailer, every departure weighed once with no blank declaration, every Varnamo note at its true share"""
    import sim as S
    regs = {}
    wbk = load_regs(pk)
    cp = A.Pack()
    cp.routes, cp.short, cp.stops, cp.trailer, cp.tractor_tare = pk.routes, pk.short, pk.stops, pk.trailer, pk.tractor_tare
    cp.wb = [{"date": x["date"], "duty": x["duty"], "shipper": x["shipper"], "declared": float(x["declared"]),
              "net": round(x["payload"] * 1000 / 20) * 20.0, "trailer": wbk[x["trailer"]]} for x in w["depart"]]
    cp.vdep = {}
    for x in w["depart"]:
        if A.LAST12[0] <= x["date"] <= A.LAST12[1]:
            towns = [t for t, _ in pk.stops[x["duty"]]]
            cp.vdep.setdefault(x["duty"], []).append({"trailer": wbk[x["trailer"]],
                                                      "drops": [(t, 1000 * s) for t, s in zip(towns, x["shares"])]})
    cp.days = []
    for x in w["pilot"]:
        t = float(np.mean([tr["t"] for tr in x["trips"]]))
        drive = sum(tr["km"] / tr["speed"] for tr in x["trips"])
        towns = [tw for tw, _ in pk.stops[x["duty"]]]
        drops = [(tw, 1000 * s) for tw, s in zip(towns, x["shares"])]
        tl = w["trailers"][x["trailer"]]
        cp.days.append({"date": x["date"], "reg": x["tractor"], "duty": x["duty"], "shipper": x["shipper"],
                        "declared": float(x["declared"]), "km": float(sum(tr["km"] for tr in x["trips"])),
                        "kwh": float(sum(tr["kwh"] for tr in x["trips"])), "t": t, "station_t": t, "t_filled": t,
                        "cap": x["cap"], "age": (x["date"] - A.IN_SERVICE).days / 365.25,
                        "v": sum(tr["km"] for tr in x["trips"]) / drive, "drive_h": drive, "span_h": x["span"],
                        "combo": x["combo"], "epto": x["etru"], "reefer": tl["kind"] == "REEF",
                        "drops": drops, "phi": A.phi_of(pk, x["duty"], drops),
                        "phi_eq": A.phi_of(pk, x["duty"], drops, equal=True), "n_drops": len(drops)})
    return cp


def load_regs(pk):
    """trailer fleet number to registration, from the fleet register"""
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TARGET_DIR[0], A.FILES["fleet"]), read_only=True)
    return {r[0]: r[1] for r in list(wb["Trailers"].iter_rows(values_only=True))[1:]}


TARGET_DIR = [None]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
