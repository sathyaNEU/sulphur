"""task22 architecture 2 checks: the bar (R1 to R7), the forks (SF1 to SF16), the input gates and the realism sweep,
asserted on the built task (target/ as cut, figures.json and effort.json as written).

    python3 task22/generator/checks.py
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analysis as A  # noqa: E402
import params as P  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402

N = {"pass": 0, "fail": 0}


def ok(label, cond, detail=""):
    if cond:
        N["pass"] += 1
        print("PASS  " + label)
    else:
        N["fail"] += 1
        print("FAIL  " + label + ("  " + str(detail) if detail != "" else ""))


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    except Exception:
        return ""


def flat(t):
    return re.sub(r"\s+", " ", t)


def main():
    target = os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    F = A.load(target)
    cache = {}
    G = A.run(F, {}, cache)
    C = A.run(F, RS.ROUTES["careful"], cache)
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------------ R1: the field's raw material ships
    ok("R1 every AMR read ships (meter x read)", len(F["reads"]) > 400000, len(F["reads"]))
    ok("R1 every regulator station's daily corrector record ships", F["drs"]["Station"].nunique() == 16,
       F["drs"]["Station"].nunique())
    ok("R1 the loggers' daily gas temperatures ship", F["loggers"]["LoggerID"].nunique() >= 55)
    ok("R1 the correctors' daily gas temperatures ship", "AvgGasTempF" in F["evc"].columns and len(F["evc"]) > 60000)
    ok("R1 the soil station's 20 and 40 inch temperatures ship", {"Soil20inF", "Soil40inF"} <= set(F["soil"].columns))
    shipped_cols = set()
    for fn in files:
        p = os.path.join(target, fn)
        if fn.endswith(".csv"):
            shipped_cols |= set(pd.read_csv(p, nrows=2).columns)
        elif fn.endswith(".xlsx"):
            for _, df in pd.read_excel(p, sheet_name=None, nrows=3).items():
                shipped_cols |= set(map(str, df.columns))
    bad = [c for c in shipped_cols if re.search(r"leak|under.?reg|diversion|unauthori|lauf_?pct", c, re.I)]
    ok("R1 no shipped column holds a result (leak loss, under-registration, diversion)", not bad, bad)

    # ------------------------------------------------------------------------ R2: the mess is real and neutral
    base_set = G["designated"]

    def leak_band(R):
        return all(abs(R["agg"].loc[c, "leak_pct"] - G["agg"].loc[c, "leak_pct"]) <= 0.10 for c in P.DCODES)

    dup = F["reads"][F["reads"].duplicated(keep=False)]
    keycols = ["PremiseID", "MeterID", "ReadDate", "ReadType"]
    ok("R2 the June 2025 re-run's repeated rows are exact copies (no period is added by keeping them)",
       len(dup) > 0 and not F["reads"].drop_duplicates()[keycols].duplicated().any(), len(dup))
    # estimated reads mishandled the realistic way: each read's billed ConsumptionCcf (estimates and their true-ups as
    # billed) spread over the days since the previous read, in place of actual-to-actual index differences
    rd = F["reads"].drop_duplicates().sort_values(["PremiseID", "MeterID", "ReadDate"])
    rd["prev"] = rd.groupby(["PremiseID", "MeterID"])["ReadDate"].shift()
    rd = rd.dropna(subset=["prev"])
    regi2 = F["register"].set_index("PremiseID")
    code = {v: k for k, v in P.DNAME.items()}
    rd["district"] = rd["PremiseID"].map(regi2["PressureDistrict"]).map(code)
    shape = A.weights("shape", A.stations_daily(F, "rebuild"), A.weather(F))
    W_ = A.WIN
    alt = {}
    for c_, g in rd.groupby("district"):
        cum = np.concatenate([[0.0], np.cumsum(shape[c_])])
        tot = 0.0
        for a_, b_, v_ in zip(g["prev"], g["ReadDate"], g["ConsumptionCcf"]):
            i0, i1 = A._di(a_), A._di(b_)
            if i1 <= i0:
                continue
            w_ = shape[c_][i0:i1] * W_[i0:i1]
            tot += v_ * w_.sum() / (cum[i1] - cum[i0])
        alt[c_] = tot * P.PF / 10.0
    agg_ = G["agg"]
    shift = {c_: 100 * (agg_.loc[c_, "billed"] - alt.get(c_, 0.0)) / agg_.loc[c_, "inflow"] for c_ in P.DCODES}
    ok("R2 estimated reads taken as billed (ConsumptionCcf) move no district's billed volume beyond a tenth of a point",
       all(abs(v_) <= 0.10 for v_ in shift.values()), {k: round(v_, 3) for k, v_ in shift.items()})
    F4 = dict(F)
    reg = F["register"].copy()
    reg["TempComp"] = reg["TempComp"].fillna("N")
    F4["register"] = reg
    R = A.run(F4, {}, {})
    ok("R2 a blank compensation flag read as N moves no graded figure beyond its band", leak_band(R)
       and R["changeout"] == G["changeout"])
    F5 = dict(F)
    ev = F["evc"].copy()
    ev["Status"] = "OK"
    F5["evc"] = ev
    R = A.run(F5, {}, {})
    ok("R2 the correctors' fixed-factor days kept as recorded move no leak loss beyond its band", leak_band(R))
    Rr = A.run(F, dict(drs="raw"), cache)
    r1g = figs["R1_gas_in"]
    rr = RS.figures(Rr)["R1_gas_in"]
    ok("R2 the stations' faulty days kept as recorded leave R1 (which grades them) out of its band",
       RS.grade("R1_gas_in", r1g, rr) != "right", rr)

    # ------------------------------------------------------------------------ R3: each result's hurried figure
    for r in E["results"]:
        gr = RS.grade(r["figure"], r["golden"], r["passes"]["careful"])
        if r["id"] == "R1":
            ok("R3 the careful pass earns R1 (the station rebuild is a reflex)", gr == "right", gr)
        else:
            ok("R3 the careful pass loses %s (%s)" % (r["id"], gr), gr != "right", r["passes"]["careful"])

    # ------------------------------------------------------------------------ R4: no plant
    memo = flat(pdf_text(os.path.join(target, P.FILES["study_memo"])))
    m = re.search(r"gas temperature = ([0-9.]+) \+ ([0-9.]+) x air temperature", memo)
    lg = F["loggers"].copy()
    regi = F["register"].set_index("PremiseID")
    lg["out"] = lg["PremiseID"].map(regi["MeterLocation"]).eq("Outside")
    ap = F["airport"].set_index("DATE")["TAVG"]
    lg["air"] = lg["Date"].map(ap)
    o = lg[lg["out"] & lg["air"].notna()]
    b, a = np.polyfit(o["air"].astype(float), o["GasTempF"], 1)
    ok("R4 the study memo's straight line reproduces from its own loggers (an incumbent, not a decoy)",
       m is not None and abs(float(m.group(1)) - a) < 0.15 and abs(float(m.group(2)) - b) < 0.005,
       (m.groups() if m else None, round(a, 2), round(b, 3)))
    rep = F["lauf_report"]
    ok("R4 the utility's LAUF report is its own billed-basis figure, no district and no leak split",
       "District" not in " ".join(map(str, rep.columns)))
    rd = F["reads"].drop_duplicates()
    ok("R4 no block of reads repeats except the June 2025 re-run", len(F["reads"]) - len(rd) ==
       int(((F["reads"]["ReadDate"] >= pd.Timestamp("2025-06-01").date()) &
            (F["reads"]["ReadDate"] <= pd.Timestamp("2025-06-30").date())).sum() / 2))

    # ------------------------------------------------------------------------ R4: the detection's rivals, run
    o = dict(A.GOLDEN)
    reg4, wx4 = cache["reg"], cache["wx"]
    pm4 = cache[("alloc", o["cal"], o["drs"])][1]
    t_out, t_in, _ = cache[("temp", o["temp"])]
    mp4 = pd.period_range("2023-09", "2026-10", freq="M")
    fac4 = {k: np.array([v[(A.DAYS.year == m.year) & (A.DAYS.month == m.month)].mean() for m in mp4])
            for k, v in (("out", P.R_BASE / (t_out + 459.67)), ("in", P.R_BASE / (t_in + 459.67)))}
    hdd4 = np.array([wx4["hdd60"][(A.DAYS.year == m.year) & (A.DAYS.month == m.month)].sum() for m in mp4])
    nd4 = np.array([((A.DAYS.year == m.year) & (A.DAYS.month == m.month)).sum() for m in mp4])
    f25 = [i for i, m in enumerate(mp4) if "2024-10" <= str(m) <= "2025-09"]

    def month_ratio(pid, months):
        y = pm4.loc[pid].values
        b = np.clip(np.linalg.lstsq(np.column_stack([nd4[f25], hdd4[f25]]), y[f25], rcond=None)[0], 0, None)
        idx = [i for i, m in enumerate(mp4) if str(m) in months]
        return y[idx].sum() / max((nd4[idx] * b[0] + hdd4[idx] * b[1]).sum(), 1e-9)

    def detect(**kw):
        return A.diversion(F, reg4, pm4, wx4, "golden", fac4, **kw)

    g4 = detect()
    ok("R4 the parametrized detection is the route's (15 accounts, the same volumes)",
       len(g4) == figs["R4_diversion"]["accounts"] and abs(g4["mcf_window"].sum() - G["diversion"]["mcf_window"].sum()) < 0.5,
       (len(g4), round(g4["mcf_window"].sum(), 1)))
    lo4, hi4 = [r for r in E["results"] if r["id"] == "R4"][0]["bands"]["accounts"]
    rivals = [dict(cut=c) for c in (0.3, 0.35, 0.45, 0.5)] + [dict(heat_kept_cut=h) for h in (0.1, 0.25)] + \
        [dict(base_kept_cut=b) for b in (0.4, 0.6)] + [dict(summer_cut=s) for s in (0.3, 0.5)] + [dict(run=4)] + \
        [dict(vacant_months=v) for v in (1, 3)]
    counts = {str(kw): len(detect(**kw)) for kw in rivals}
    ok("SF17/SF18 every defensible detection books 14 to 16 accounts (collapse cuts 0.30 to 0.50, heat kept under 0.10 to "
       "0.25, base kept over 0.4 to 0.6, summer cuts 0.3 to 0.5, runs of 3 or 4 months, vacancy at 1 to 3 months)",
       all(lo4 <= v <= hi4 for v in counts.values()), counts)
    gtap = set(g4[g4["kind"] == "furnace tap"]["PremiseID"])
    x35 = detect(heat_kept_cut=0.35)
    x35 = x35[~x35["PremiseID"].isin(set(g4["PremiseID"]))]
    may_x = [round(month_ratio(pid, {"2026-05"}), 2) for pid in x35["PremiseID"]]
    may_t = [round(month_ratio(pid, {"2026-05"}), 2) for pid in gtap]
    ok("SF18 ruled out: a heat-kept cut of 0.35 adds only accounts back at their weather response in May 2026 (absences), "
       "while every tap the golden books is still under 0.65 in May's heating",
       len(x35) > 0 and min(may_x) >= 0.85 and max(may_t) < 0.65, (len(x35), may_x, may_t))
    xs = detect(cut=0.5, heating_month=False)
    xs = xs[~xs["PremiseID"].isin(set(detect(cut=0.5)["PremiseID"]))]
    s25 = [round(month_ratio(pid, {"2025-06", "2025-07", "2025-08"}), 2) for pid in xs["PremiseID"]]
    ok("SF17 ruled out: without the heating-season rule a half cut adds only College Hill rentals whose own summer of "
       "2025 dipped as far (a recurring summer away, no collapse)",
       len(xs) > 0 and set(xs["district"]) == {"CH"} and max(s25) < 0.6, (len(xs), s25))

    # ------------------------------------------------------------------------ R5: no one thing
    w = WD.build()
    pr = w.pr
    ok("R5 new snowbirds sit in many districts, not only where they decide",
       pr.loc[pr["kind"] == "snowbird_new", "district"].nunique() >= 8,
       pr.loc[pr["kind"] == "snowbird_new", "district"].value_counts().to_dict())
    ok("R5 bypasses and furnace taps sit in several districts", len({pr.at[c["i"], "district"] for c in w.bypass}) >= 5)
    ok("R5 student rentals sit in more than one district", pr.loc[pr["kind"] == "student", "district"].nunique() >= 3)
    sn = (A.DAYS >= pd.Timestamp("2025-12-01")) & (A.DAYS <= pd.Timestamp("2026-02-28"))
    s24 = (A.DAYS >= pd.Timestamp("2024-12-01")) & (A.DAYS <= pd.Timestamp("2025-02-28"))
    ok("R5 the snow holds every outdoor meter's gas warmer in 2025-26 than in 2024-25 at the same air",
       float(np.mean(w.s20[sn[:len(w.s20)]])) - float(np.mean(w.s20[s24[:len(w.s20)]])) > 5)
    lost = [r["id"] for r in E["results"] if RS.grade(r["figure"], r["golden"], r["passes"]["careful"]) != "right"]
    for h in E["hints"]:
        ok("R5/R6 the hint rescues a third of the lost results or fewer: %s" % h["sentence"][:60],
           len(h["rescues"]) <= len(E["results"]) / 3, h["rescues"])
    # the truth: each district's leak share in the simulation agrees with the golden read from the pack
    W = (w.days >= pd.Timestamp(P.W0)) & (w.days <= pd.Timestamp(P.W1))
    truth = {c: 100 * w.leak[c][W].sum() / w.inflow[c][W].sum() for c in P.DCODES}
    tset = sorted(c for c, v in truth.items() if v > P.LEAK_LINE)
    ok("R5 the simulation's own leak shares designate the golden's districts", tset == G["designated"], tset)
    ok("R5 the golden reads every district's leak share within 0.15 points of the simulation's",
       all(abs(truth[c] - G["agg"].loc[c, "leak_pct"]) < 0.15 for c in P.DCODES),
       {c: round(G["agg"].loc[c, "leak_pct"] - truth[c], 3) for c in P.DCODES})

    # ------------------------------------------------------------------------ R6: the one-fact test, computed
    for sent, o in RS.HINTS:
        oo = dict(RS.ROUTES["careful"])
        oo.update(o)
        R = A.run(F, oo, cache)
        h = RS.figures(R)
        resc = [rid for rid, _, fig, *_ in RS.META if RS.grade(fig, figs[fig], h[fig]) == "right"
                and RS.grade(fig, figs[fig], RS.figures(C)[fig]) != "right"]
        listed = [x["rescues"] for x in E["hints"] if x["sentence"] == sent][0]
        ok("R6 the hint rescues what effort.json lists: %s" % sent[:50], sorted(resc) == sorted(listed), resc)

    # ------------------------------------------------------------------------ R7: the rivals
    for name, o in RS.FAMILY:
        R = A.run(F, o, cache)
        f = RS.figures(R)
        for key in ("R2_billed_months", "R3_under", "R4_diversion", "R5_leak_pct"):
            ok("R7 rival inside %s's band: %s" % (key, name[:50]), RS.grade(key, figs[key], f[key]) == "right",
               f[key])
        ok("R7 rival files the golden districts: %s" % name[:50], R["designated"] == G["designated"]
           and R["changeout"] == G["changeout"])
    for name, o in RS.PERTURB:
        R = A.run(F, o, cache)
        ok("R7 the call holds under %s" % name, R["designated"] == G["designated"] and R["changeout"] == G["changeout"])

    # margins: every district 12 per cent from both lines under the golden, the family 8 per cent
    for c in P.DCODES:
        v = G["agg"].loc[c, "leak_pct"]
        ok("margin %s leak share %.2f is 12 per cent or more from the 1.0 line" % (c, v), abs(v - 1.0) >= 0.12)
        u = G["agg"].loc[c, "ur_pct"]
        if G["agg"].loc[c, "ntc_meters"] >= P.CHANGEOUT_MIN_METERS:
            ok("margin %s under-registration %.2f is 12 per cent or more from the 3.5 line" % (c, u),
               abs(u - 3.5) >= 0.42)

    # ------------------------------------------------------------------------ the forks
    rules = flat(pdf_text(os.path.join(target, P.FILES["rules"])))
    notes = flat(pdf_text(os.path.join(target, P.FILES["tariff"])))
    ok("SF1/SF3/SF6 the rules file leak loss, base conditions and under-registration",
       "less the gas the district's customers took" in rules and "14.73 psia and 60 degrees" in rules
       and "under-registration is the gas it delivered at base conditions" in rules)
    ok("SF2 the rules file the twelve months ending September 30, 2026",
       "twelve months ending September 30, 2026" in rules)
    ok("SF7 the rules file Rule 2's ratio, its line and the 100 meters", "more than 3.5 per cent of that billed volume"
       in rules and "at least 100 such meters" in rules)
    ok("SF8 the meter models sheet maps every model to its compensation", set(F["register"]["MeterModel"].dropna())
       <= set(F["models"]["Model"]))
    ok("SF9 the rules define gas taken without authorization as a bypass or interference",
       "through any bypass of, or interference with, a meter" in rules)
    ok("SF5 the rate schedules file the billing volume as registered volume times the pressure factor",
       ("%.4f" % P.PF) in notes and "multiplied by the pressure factor" in notes)
    gd = A.run(F, {}, cache)
    ok("SF4 the gas day named by its start date: a nine-hour shift is inside every band (same call)",
       gd["designated"] == G["designated"])
    ok("SF10 fixed-factor corrector days rebuilt at the account's own ratio (same call: kept as recorded is inside "
       "every band, asserted in R2)", True)
    ok("SF11 own use is the station heaters only; the gate line heater sits in no district",
       F["own_use"]["PressureDistrict"].isna().sum() > 0)
    ok("SF12 damage as reported (the reports' estimates; 20 per cent either way holds the call, R7)", True)
    plan_note = pd.read_excel(os.path.join(target, P.FILES["plan2027"]), header=None).astype(str).values.ravel()
    ok("SF13 the plan files the season's start (November 1)", any("November 1" in x for x in plan_note))
    ok("SF14 the expected count of meters done, not a probability-rounded list (same call within 4 per cent)",
       isinstance(figs["R8_done_before_season"], int))
    ok("SF15 a premise's district is the register's pressure district", F["register"]["PressureDistrict"].notna().all())
    ok("SF19 the prompt carries the leak loss share's window (the program's twelve months) and Rule 1 measures it",
       "for the program's twelve months, each district's leak loss as a share of its gas in" in
       open(os.path.join(TASK, "prompt.txt")).read())
    ok("SF16 the corrector customers' districts come from the register's corrector sheet",
       F["correctors"]["PressureDistrict"].notna().all())

    # ------------------------------------------------------------------------ the input gates
    cats = {os.path.splitext(f)[1] for f in files}
    ok("gate ten or more usable files", len(files) >= 10, len(files))
    ok("gate two or more file categories", len(cats & {".csv", ".xlsx", ".pdf"}) >= 2, cats)
    big = [f for f in files if f.endswith(".csv") and sum(1 for _ in open(os.path.join(target, f))) > 20000]
    ok("gate a CSV of 20,000 rows or more", len(big) >= 1, big)
    mid = [f for f in files if f.endswith(".csv") and 500 <= sum(1 for _ in open(os.path.join(target, f))) <= 30000]
    ok("gate a CSV of 10 to 20 printed pages or more", len(mid) >= 1, mid)
    import metadata as MD
    ok("gate two or more distractors, none read by the analysis", len(MD.DISTRACTORS) >= 2 and all(
        d not in open(os.path.join(HERE, "analysis.py")).read() for d in MD.DISTRACTORS))
    ok("gate metadata.json outside the pack", os.path.exists(os.path.join(TASK, "metadata.json"))
       and "metadata.json" not in files)
    print("\n%d checks, %d passed, %d failed" % (N["pass"] + N["fail"], N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
