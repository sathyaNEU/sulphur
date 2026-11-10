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


GOLD_SET = ["V02", "V03", "V05", "V09", "V11", "V14", "V16", "V18"]
CAREFUL = "careful but hurried"
HINTS = ("careful, own-duty loads", "careful, curved loss", "careful, design-day speed")


def main(target):
    TARGET_DIR[0] = target
    import writeup as WU
    PAY_BAND, LOSS_BAND, RATIO_BAND = WU.PAY_BAND, WU.LOSS_BAND, WU.RATIO_BAND
    pk = A.load(target)
    g = A.golden(pk)
    M = g["models"]
    gold_set = g["set"]
    L = g["limit"]
    ok("call", gold_set == GOLD_SET and g["count"] == 8, str(gold_set))
    for c, v in g["assess"].items():
        ok("margin %s 10 kWh or more" % c, abs(v["kwh"] - L) >= 10.0, "%.1f against %.1f" % (v["kwh"], L))
    R = A.routes(pk)
    AS = {k: A.assess(pk, m, lim=lm) for k, (m, lm) in R.items()}
    sets = {k: A.chosen(a) for k, a in AS.items()}
    # the careful pass (the recorded runs' union) loses the order by two or more duties, each 10 kWh or more from the
    # golden's limit, and keeps a cushion of 4 kWh on its own wrong side
    diff = set(sets[CAREFUL]) ^ set(gold_set)
    ok("careful order differs by two or more duties", len(diff) >= 2, str(sorted(diff)))
    for c in diff:
        ok("careful flip %s 10 kWh or more from the golden limit" % c, abs(g["assess"][c]["kwh"] - L) >= 10.0)
        ok("careful flip %s 4 kWh or more past its own limit" % c, abs(AS[CAREFUL][c]["kwh"] - R[CAREFUL][1]) >= 4.0,
           "%.1f" % (AS[CAREFUL][c]["kwh"] - R[CAREFUL][1]))
    dw = set(sets["careful, design-day speed"]) ^ set(gold_set)
    ok("careful at the design-day speed differs by two or more duties", len(dw) >= 2, str(sorted(dw)))
    ok("careful and its design-day variant name different wrong orders",
       sets[CAREFUL] != sets["careful, design-day speed"])
    for h in HINTS:
        ok("one estimate put right still orders wrongly: %s" % h, sets[h] != gold_set, str(sets[h]))
    wrong = {tuple(v) for k, v in sets.items() if v != gold_set}
    ok("five or more distinct wrong orders", len(wrong) >= 5, str(len(wrong)))
    # the careful pass misreads energies where nothing turns on them (the factors run across the shortlist)
    off = [c for c in pk.short if abs(AS[CAREFUL][c]["kwh"] - g["assess"][c]["kwh"]) > 10 and c not in diff]
    ok("careful misreads three or more energies where nothing turns", len(off) >= 3, str(off))
    # R1: the payload term
    pt = A.slope_per_100(M["golden"])
    ok("payload term inside the band by 0.15", PAY_BAND[0] + 0.15 < pt < PAY_BAND[1] - 0.15, "%.3f" % pt)
    for k in (CAREFUL, "the terminal's calibration line", "declared weights", "one pooled correction"):
        v = A.slope_per_100(R[k][0])
        ok("payload term outside the band by 0.15 on %s" % k, v < PAY_BAND[0] - 0.15 or v > PAY_BAND[1] + 0.15,
           "%.3f" % v)
    gp, cp = A.payloads(pk, "lane"), A.careful_payloads(pk)
    fe, fse = A.fe_slope_se(pk, gp)
    fec = A.fe_slope_se(pk, cp)[0]
    ok("the within-duty fit agrees with the duties' own loads", PAY_BAND[0] <= fe <= PAY_BAND[1] and abs(fe - pt) < 0.2,
       "%.2f" % fe)
    ok("the within-duty fit on the terminal's line lands in the band (the runs' dismissed figure)",
       PAY_BAND[0] <= fec <= PAY_BAND[1], "%.2f" % fec)
    ok("payload term within 0.3 of the truth", abs(pt - 100 * P.LOAD) < 0.3, "%.3f" % pt)
    ok("tare and payload terms agree within 0.6 (a tonne is a tonne)", abs(g["tare_term"] - pt) < 0.6,
       "%.2f against %.2f" % (g["tare_term"], pt))
    # the lane loads: a footprint on every pilot duty, the terminal's line too heavy on every one
    lt = WU.lane_table(pk)
    ok("every pilot duty lighter than its shipper's terminal loads", all(v["share"] < 0.93 for v in lt.values()),
       str({k: v["share"] for k, v in lt.items()}))
    ok("the terminal's line too heavy on every pilot duty by 0.3 t or more",
       all(v["terminal_line"] - v["lane"] >= 0.3 for v in lt.values()),
       str({k: round(v["terminal_line"] - v["lane"], 2) for k, v in lt.items()}))
    sc = WU.scale_check(pk)
    for du, v in sc.items():
        ok("scale days %s bear out the duty's own loads" % du,
           abs(v["scale_mean"] - v["own_before"]) < 0.8 and v["terminal_line_before"] - v["scale_mean"] > 1.0, str(v))
        ok("scale days %s under 60" % du, 15 <= v["scale_days"] <= 60, str(v["scale_days"]))
    cal = A.calibration(pk)
    pilot = {d["shipper"] for d in pk.days}
    est = [v[1] for (s, rr), v in cal.items() if s in pilot and P.SHIPPERS[s][2] == "est" and rr != "ticket"]
    ok("estimating clerks' weighed-on-declared slopes under 0.3", all(0.05 <= x <= 0.3 for x in est), str(est))
    ok("no pilot shipper's notes exact over the whole window", not any(
        abs(v[1] - 1) < 0.05 for (s, r), v in cal.items() if s in pilot and r == "all"))
    # R2: the first-year loss
    f = g["fade"]
    ok("loss inside the band by 0.2", LOSS_BAND[0] + 0.2 <= 100 * f <= LOSS_BAND[1] - 0.2, "%.3f" % (100 * f))
    for h in A.LOSS_RIVALS + ("first_year",):
        ok("loss form %s in the band" % h, LOSS_BAND[0] <= 100 * A.fade(pk, h) <= LOSS_BAND[1],
           "%.3f" % (100 * A.fade(pk, h)))
    for h in ("cold", "yoy", "age"):
        ok("loss %s outside the partial band" % h, 100 * A.fade(pk, h) < 3.8 - 0.2, "%.3f" % (100 * A.fade(pk, h)))
    ok("the straight line fits far worse than the curve", A.fade_fit(pk, "cold")[1] > 1.1 * A.fade_fit(pk, "curve")[1])
    ok("loss within 0.4 of the truth", abs(f - float(np.mean(list(sim.world()["fade"].values())))) <= 0.004,
       "%.4f" % f)
    # the early loss on every tractor: each tractor's curve beats its straight line
    for reg in sorted({d["reg"] for d in pk.days}):
        sub = A.Pack()
        sub.days = [d for d in pk.days if d["reg"] == reg]
        ok("early-life loss on tractor %s" % reg, A.fade_fit(sub, "exp0.30")[0] > A.fade_fit(sub, "cold")[0] + 0.008)
    ok("limit gap between the golden and the careful loss 5 kWh or more", R[CAREFUL][1] - L >= 5.0)
    # R3: the speed ratio
    rr = A.speed_ratio(pk)
    ok("winter speed ratio near the truth", abs(rr - sim.ratio(P.DESIGN_T)) < 0.012, "%.3f" % rr)
    ok("speed ratio inside the band", RATIO_BAND[0] < rr < RATIO_BAND[1], "%.3f" % rr)
    ok("the year's ratio outside the band", A.speed_ratio(pk, how="mean") > RATIO_BAND[1] + 0.05)
    vmax = max(d["v"] for d in pk.days)
    ok("every shortlisted duty's routing-tool speed above any pilot day's actual",
       min(A.plan_speed(pk, c) for c in pk.short) > vmax, "%.1f" % vmax)
    # every route that takes all the steps: the same order, every energy within 10 kWh, each band held
    RV = A.rivals(pk)
    for name, (m, lm) in RV.items():
        a = A.assess(pk, m, lim=lm)
        ok("rival %s keeps the order" % name, A.chosen(a) == gold_set, str(A.chosen(a)))
        ok("rival %s clear of the limit by 4 kWh" % name, min(abs(a[c]["kwh"] - lm) for c in a) >= 4.0)
        ok("rival %s energies within 10 kWh" % name, max(abs(a[c]["kwh"] - g["assess"][c]["kwh"]) for c in a) <= 10.0)
        v = A.slope_per_100(m)
        ok("rival %s payload term in the band" % name, PAY_BAND[0] <= v <= PAY_BAND[1], "%.3f" % v)
    for h in ("hinge8", "hinge12", "linear", "bins"):
        ok("speed ratio form %s in the band" % h, RATIO_BAND[0] <= A.speed_ratio(pk, how=h) <= RATIO_BAND[1])
    # the cold form, out of sample
    b1, b2, bq = A.backtest(pk, gp, A.H1), A.backtest(pk, gp, A.H2), A.backtest(pk, gp, ("quad", 16))
    ok("one cold rate under-forecasts held-out sub-zero days by 3 per cent or more", b1[0] <= -3.0, str(b1))
    ok("two rates within 1.5 per cent", abs(b2[0]) <= 1.5 and abs(bq[0]) <= 1.5, str((b2, bq)))
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
    # SF14 the fit window, SF15 the error model's window, SF16 within-duty fit, SF18 note periods, SF19 to SF22 the loss
    for k in ("2025 only", "2026 only", "loads: error read on the last 12 months", "loads: additive declaration error",
              "loads: each day at its duty's mean declared", "loss: the day's temperature", "loss: degrees below 15 C",
              "loss: a straight line on the first year's days") + tuple("loss: %s" % h for h in A.LOSS_RIVALS):
        ok("SF %s" % k, same(pk, RV[k][0], g, RV[k][1])[0])
    ok("SF18 the drinks maker's scale period kept apart", A.regime(pk, "GDR", dt.date(2026, 9, 15)) == "ticket"
       and A.regime(pk, "GDR", dt.date(2026, 3, 16)) == "note")
    ok("SF19 the loss's temperature term", all(abs(A.fade(pk, "curve", h) - f) <= 0.003 for h in ("linear", "cold15")))
    ok("SF20 the loss estimator: the same months a year apart is ruled out (it starts a year after the early loss)",
       A.fade(pk, "yoy") < f - 0.012)
    ok("SF21 the cold's capacity loss is reversible", A.fade(pk, "age") < A.fade(pk, "cold") - 0.002)
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
    # SF28 the pilot's loads: each duty's own, or the terminal's line (ruled out by the scale days, asserted above)
    ok("SF28", sets["the terminal's calibration line"] != gold_set)
    # SF29 the drops' shares: declared shares, or equal shares (inside the band, same call)
    ok("SF29", same(pk, RV["drops: equal shares"][0], g)[0])
    # SF30 the tare term: its own coefficient, or the payload's (same call, payload term in the band)
    ok("SF30", same(pk, RV["tare: one coefficient with the payload"][0], g)[0])
    # SF31 the loss's age form: every curved form keeps the order (asserted with the rivals)
    ok("SF35 the declaration error additive or multiplicative", same(pk, RV["loads: additive declaration error"][0], g)[0])
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
              "hour", "part load", "regional", "early", "curve"]:
        ok("standard silent on %s" % w, w not in stext)
    ok("standard files the duty's drops (2.1)", "drops" in stext)
    ptext = open(os.path.join(os.path.dirname(HERE), "prompt.txt"), encoding="utf-8").read().lower()
    for w in ["declared", "weigh", "calibrat", "regress", "error", "shipper", "cold", "temperature", "hold",
              "scatter", "freez", "state of charge", "trailer", "tare", "fridge", "refrig", "reefer", "drop", "speed",
              "weight of", "terminal", "regional", "part load", "full load", "early", "curve", "line"]:
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
    ok("clean truth: loss", abs(gc["fade"] - f) < 0.004, "%.4f" % gc["fade"])
    RC = A.routes(clean)
    for k in ("declared weights", "the terminal's calibration line", "no first-year loss", "the year's mean speed ratio",
              CAREFUL, "careful, design-day speed") + HINTS:
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
                        "combo": x["combo"], "epto": False, "reefer": tl["kind"] == "REEF",
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
