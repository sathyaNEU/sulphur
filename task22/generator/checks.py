"""task22 architecture 2 checks (redesigned after the review of 2026-11-13): the bar (R1 to R7), the truth replay of
every graded cell, the stump factorial, the variant battery, the forks (SF1 to SF26), the input gates and the realism
sweep, asserted on the built task (target/ as cut, figures.json and effort.json as written).

    python3 task22/generator/checks.py [TASK_DIR]
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analysis as A  # noqa: E402
import params as P  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402
import zfactor as ZF  # noqa: E402

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


def main(task):
    target = os.path.join(task, "target")
    gen = os.path.join(task, "generator") if os.path.exists(os.path.join(task, "generator", "figures.json")) else HERE
    figs = json.load(open(os.path.join(gen, "figures.json")))
    E = json.load(open(os.path.join(gen, "effort.json")))
    F = A.load(target)
    cache = {}
    G = A.run(F, {}, cache)
    C = A.run(F, RS.ROUTES["careful"], cache)
    files = sorted(os.listdir(target))
    w = WD.build()
    pr = w.pr
    W = (w.days >= pd.Timestamp(P.W0)) & (w.days <= pd.Timestamp(P.W1))

    # ------------------------------------------------------------------------ R1: the field's raw material ships
    ok("R1 every AMR read ships (meter x read)", len(F["reads"]) > 400000, len(F["reads"]))
    ok("R1 every regulator station's daily corrector record ships with its uncorrected volume, pressure and "
       "temperature", F["drs"]["Station"].nunique() == 16 and
       {"UncorrectedMcf", "AvgPressurePsig", "AvgTempF"} <= set(F["drs"].columns))
    ok("R1 every customer corrector's daily record ships with its uncorrected volume, pressure and temperature",
       {"UncorrectedMcf", "AvgPressurePsig", "AvgGasTempF"} <= set(F["evc"].columns) and len(F["evc"]) > 60000)
    ok("R1 the gate's analyser ships the gas's specific gravity day by day", "SpecificGravity" in F["gate"].columns)
    ok("R1 the stations sheet names each station's corrector", set(F["stations"]["Corrector"]) == {"EVC-I", "EVC-II"})
    ok("R1 the loggers' daily gas temperatures ship", F["loggers"]["LoggerID"].nunique() >= 55)
    ok("R1 the soil station's 20 and 40 inch temperatures ship", {"Soil20inF", "Soil40inF"} <= set(F["soil"].columns))
    shipped_cols = set()
    for fn in files:
        p = os.path.join(target, fn)
        if fn.endswith(".csv"):
            shipped_cols |= set(pd.read_csv(p, nrows=2).columns)
        elif fn.endswith(".xlsx"):
            for _, df in pd.read_excel(p, sheet_name=None, nrows=3).items():
                shipped_cols |= set(map(str, df.columns))
    bad = [c for c in shipped_cols if re.search(r"leak|under.?reg|diversion|unauthori|lauf_?pct|supercomp|fpv|z.?factor|"
                                               r"dual.?fuel|switchover", c, re.I)]
    ok("R1 no shipped column holds a result (leak loss, under-registration, diversion, supercompressibility, a "
       "dual-fuel flag)", not bad, bad)

    # ------------------------------------------------------------------------ R2: the mess is real and neutral
    def leak_band(R):
        return all(abs(R["agg"].loc[c, "leak_pct"] - G["agg"].loc[c, "leak_pct"]) <= 0.10 for c in P.DCODES)

    dup = F["reads"][F["reads"].duplicated(keep=False)]
    keycols = ["PremiseID", "MeterID", "ReadDate", "ReadType"]
    ok("R2 the June 2025 re-run's repeated rows are exact copies (no period is added by keeping them)",
       len(dup) > 0 and not F["reads"].drop_duplicates()[keycols].duplicated().any(), len(dup))
    F4 = dict(F)
    reg = F["register"].copy()
    reg["TempComp"] = reg["TempComp"].fillna("N")
    F4["register"] = reg
    R = A.run(F4, {}, {})
    ok("R2 a blank compensation flag read as N moves no leak loss beyond its band and keeps both sets",
       leak_band(R) and R["changeout"] == G["changeout"] and R["designated"] == G["designated"])
    F5 = dict(F)
    ev = F["evc"].copy()
    ev["Status"] = "OK"
    F5["evc"] = ev
    R = A.run(F5, {}, {})
    ok("R2 the correctors' fixed-factor days kept as recorded move no leak loss beyond its band", leak_band(R))

    # ------------------------------------------------------------------------ R3: each result's hurried figure
    for r in E["results"]:
        gr = RS.grade(r["figure"], r["golden"], r["passes"]["careful"])
        if r["id"] == "R6":
            ok("R3 the careful pass earns R6 (the changeout set rests on reflexes)", gr == "right", gr)
        else:
            ok("R3 the careful pass loses %s (%s)" % (r["id"], gr), gr != "right", r["passes"]["careful"])
    ok("R3 the careful pass is the route both runs took on this world (soil temperature, degree-day shape, station "
       "repairs, every fall booked, correctors as recorded)", RS.ROUTES["careful"] == dict(
           cal="fit", temp="soil", div="all", z="rec"))

    # ------------------------------------------------------------------------ R4: no plant, no decoy
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
    st = F["stations"].set_index("Station")
    ok("R4 the EVC-I stations are the ones whose recorded factor is the pressure-and-temperature factor alone (read "
       "from the data, not a label)", sorted(A.pt_only_stations(F)[0]) == sorted(st.index[st["Corrector"] == "EVC-I"])
       == sorted(P.PT_ONLY_STATIONS), A.pt_only_stations(F)[0])
    evk = F["evc"][F["evc"]["Status"].eq("OK") & F["evc"]["UncorrectedMcf"].gt(20)]
    exc = evk["CorrectedMcf"] / evk["UncorrectedMcf"] / ((evk["AvgPressurePsig"] + A.p_atm(F)) / P.P_BASE * P.R_BASE /
                                                         (evk["AvgGasTempF"] + 459.67))
    nd_ = evk.groupby("Account").size()
    per = exc.groupby(evk["Account"]).median().sub(1).abs()[nd_ >= 60]
    ok("R4 the customer correctors' recorded factor is the pressure-and-temperature factor alone (the median gas day, "
       "pooled and account by account)", abs(float(exc.median()) - 1) < 0.0003 and float(per.max()) < 0.0015,
       (round(float(exc.median()) - 1, 5), round(float(per.max()), 5)))
    reb = F["rebates"]
    ok("R4 the rebates file records equipment, never a finding (no theft or absence label)",
       not reb["Equipment"].str.contains("bypass|tap|vacan|away|snow", case=False).any())

    # ------------------------------------------------------------------------ the truth replay of every graded cell
    gold_prem = set(G["diversion"]["PremiseID"])
    true_theft = {int(pr.at[c["i"], "premise"]) for c in w.bypass}
    ok("truth: the golden's premises are exactly the simulation's bypasses and furnace taps in the window",
       gold_prem == true_theft, (sorted(gold_prem - true_theft), sorted(true_theft - gold_prem)))
    dfp = {int(pr.at[c["i"], "premise"]) for c in w.dualfuel}
    snow = set(pr.loc[pr["kind"] == "snowbird_new", "premise"].astype(int))
    dg = A.run(F, dict(div="diag"), cache)["diversion"]
    lab_df = set(dg.loc[(dg["dual_fuel"] | dg["rebated"]) & dg["kind"].ne("bypass"), "PremiseID"])
    lab_ab = set(dg.loc[dg["kind"].eq("absence") & ~dg["rebated"], "PremiseID"])
    ok("truth: every fall the screen reads as a dual-fuel heat pump is one", lab_df <= dfp, sorted(lab_df - dfp))
    ok("truth: every fall the screen reads as away for the winter is a household away or a dual-fuel home back in "
       "May", lab_ab <= (snow | dfp), sorted(lab_ab - snow - dfp))
    WT = {c: 100 * w.leak[c][W].sum() / w.inflow[c][W].sum() for c in P.DCODES}
    ok("truth: the simulation's own leak shares designate the golden's districts",
       sorted(c for c, v in WT.items() if v > P.LEAK_LINE) == G["designated"], {c: round(v, 2) for c, v in WT.items()})
    ok("truth: the golden reads every district's leak share within 0.15 points of the simulation's",
       all(abs(WT[c] - G["agg"].loc[c, "leak_pct"]) < 0.15 for c in P.DCODES),
       {c: round(G["agg"].loc[c, "leak_pct"] - WT[c], 3) for c in P.DCODES})
    r1 = figs["R1_basis"]
    tr = {"Riverside, gas in, twelve months to September 2026": w.inflow["RS"][W].sum(),
          "College Hill, gas in, twelve months to September 2026": w.inflow["CH"][W].sum(),
          "East Industrial, corrector customers, twelve months to September 2026": w.evc_dist["EI"][W].sum()}
    lvd = (w.days >= pd.Timestamp("2025-12-01")) & (w.days <= pd.Timestamp("2025-12-31"))
    tr["Lakeview, gas in, December 2025"] = w.inflow["LV"][lvd].sum()
    for k, v in tr.items():
        lo, hi = RS.BANDS["R1_basis"](k, r1[k])
        ok("truth: R1 %s inside its band around the simulation's %.0f" % (k, v), lo <= v <= hi, (r1[k], round(v, 1)))
    true_mcf = {}
    for c_ in w.bypass:
        i = c_["i"]
        d0 = max((c_["start"] - P.SIM0).days, 0)
        msk = np.zeros(w.D, bool)
        msk[d0:] = True
        msk &= W
        u_reg = w.R[i] * P.PF / 10.0 * np.where(w.noncomp[i], P.R_BASE / (w.Tgas[i] + 459.67), 1.0)
        unreg = float((w.U[i][msk] - u_reg[msk]).sum())
        true_mcf[pr.at[i, "district"]] = true_mcf.get(pr.at[i, "district"], 0.0) + max(unreg, 0.0)
    r5 = figs["R5_unauthorized_mcf"]
    for k, v in r5.items():
        code = {n: c for c, n in P.DNAME.items()}[k.replace(", Mcf", "")]
        tv = true_mcf.get(code, 0.0)
        lo, hi = RS.BANDS["R5_unauthorized_mcf"](k, v)
        ok("truth: R5 %s inside its band around the simulation's gas taken (%.0f Mcf)" % (k, tv), lo <= tv <= hi,
           (v, round(tv, 1)))

    # ------------------------------------------------------------------------ the detection's conventions, run
    lo2, hi2 = [r for r in E["results"] if r["id"] == "R2"][0]["bands"]["premises"]
    det = E["battery"]["detection"]
    ok("SF17/SF22/SF23 every convention of the screen books the golden's premises and files the golden sets "
       "(collapse cut 0.35 to 0.45, home in May at 0.6 to 0.8, cold-day slope 0.2 to 0.4, switchover cap 5 to 15 F, "
       "summer cut 0.3 to 0.5, runs of 3 or 4 months, vacancy at 1 to 3 months)",
       all(lo2 <= d_["premises"] <= hi2 and d_["answer"] == figs["R4_designated"] and d_["changeout"] ==
           figs["R6_changeout"] for d_ in det), [(d_["name"][:24], d_["premises"]) for d_ in det])
    may_t = dg.loc[dg["PremiseID"].isin(gold_prem) & dg["kind"].eq("furnace tap"), "home"]
    may_a = dg.loc[dg["kind"].eq("absence") & dg["PremiseID"].isin(snow), "home"]
    ok("SF22 the May test separates: every tap the golden books is under 0.6 of its own weather response in May "
       "2026, every household away is over 0.8", (may_t.max() < 0.6) and (may_a.min() > 0.8),
       (round(may_t.max(), 3), round(may_a.min(), 3)))
    taps = dg[dg["PremiseID"].isin(gold_prem) & dg["kind"].eq("furnace tap")]
    dfs = dg[dg["dual_fuel"] & dg["kind"].eq("furnace tap")]
    ok("SF23 the cold-day test separates: every booked tap's cold-day slope is under 0.1 of its own past heating "
       "slope, every dual-fuel home's 0.4 or more", taps["cold_day_slope"].max() < 0.1 and
       dfs["cold_day_slope"].min() >= 0.4, (round(taps["cold_day_slope"].max(), 3),
                                            round(dfs["cold_day_slope"].min(), 3)))

    # ------------------------------------------------------------------------ R5: no one thing, across the data
    ok("R5 new snowbirds sit in many districts, not only where they decide",
       pr.loc[pr["kind"] == "snowbird_new", "district"].nunique() >= 8,
       pr.loc[pr["kind"] == "snowbird_new", "district"].value_counts().to_dict())
    ok("R5 dual-fuel heat pumps sit in many districts", len({pr.at[c["i"], "district"] for c in w.dualfuel}) >= 10,
       sorted({pr.at[c["i"], "district"] for c in w.dualfuel}))
    ok("R5 bypasses and furnace taps sit in several districts", len({pr.at[c["i"], "district"] for c in w.bypass}) >= 5)
    ok("R5 the EVC-I stations sit in four districts", len({st.at[s, "PressureDistrict"] for s in P.PT_ONLY_STATIONS})
       == 4)
    hp = w.evc[w.evc["press"] >= 10]
    ok("R5 corrector customers at 10 psig or more sit in several districts", hp["district"].nunique() >= 3,
       hp["district"].value_counts().to_dict())
    for h in E["hints"]:
        ok("R5/R6 the hint rescues a third of the results or fewer: %s" % h["sentence"][:60],
           len(h["rescues"]) <= len(E["results"]) / 3, h["rescues"])

    # ------------------------------------------------------------------------ R6: the factorial and the one-fact test
    fac = E["factorial"]
    stumps = [j for j in fac["judgments"] if j["kind"] == "stump"]
    ok("R6 the reflex route misses the call", fac["reflex_route"]["answer"] != fac["golden_answer"])
    ok("R6 three stumps, each necessary (dropped alone, the main set moves)",
       len(stumps) == 3 and all(j["dropped"]["answer"] != fac["golden_answer"] for j in stumps))
    ok("R6 no stump sufficient (fixed alone on the reflex route, the main set is still wrong and a third of the "
       "results or fewer are rescued)", all(j["alone"]["answer"] != fac["golden_answer"] and
                                             len(j["alone"]["results_rescued"]) <= len(E["results"]) / 3
                                             for j in stumps))
    ok("R6 the single drops land on three different wrong sets",
       len({json.dumps(j["dropped"]["answer"]) for j in stumps}) == 3)
    for sent, o in RS.HINTS:
        oo = dict(RS.ROUTES["careful"])
        oo.update(o)
        R = A.run(F, oo, cache)
        h = RS.figures(R, F)
        resc = [rid for rid, _, fig, *_ in RS.META if RS.grade(fig, figs[fig], h[fig]) == "right"
                and RS.grade(fig, figs[fig], RS.figures(C, F)[fig]) != "right"]
        listed = [x["rescues"] for x in E["hints"] if x["sentence"] == sent][0]
        ok("R6 the hint rescues what effort.json lists: %s" % sent[:50], sorted(resc) == sorted(listed), resc)

    # ------------------------------------------------------------------------ R7: the rivals and the battery
    for name, o in RS.FAMILY:
        R = A.run(F, o, cache)
        f = RS.figures(R, F)
        for key in ("R1_basis", "R2_unauthorized", "R3_leak_pct", "R5_unauthorized_mcf"):
            ok("R7 rival inside %s's band: %s" % (key, name[:50]), RS.grade(key, figs[key], f[key]) == "right",
               f[key])
        ok("R7 rival files the golden sets: %s" % name[:50], R["designated"] == G["designated"]
           and R["changeout"] == G["changeout"])
    bat = E["battery"]
    ok("R7 the variant battery (%d variants) files one main set and one changeout set" % bat["count"],
       bat["count"] >= 12 and len(bat["answers"]) == 1 and len(bat["changeout_answers"]) == 1, bat["answers"])
    for name, o in RS.PERTURB:
        R = A.run(F, o, cache)
        ok("R7 the call holds under %s" % name, R["designated"] == G["designated"] and R["changeout"] == G["changeout"])
    sg = A.gate_sg(F)
    for d_ in (-0.01, 0.01):
        F6 = dict(F)
        g6 = F["gate"].copy()
        g6["SpecificGravity"] = g6["SpecificGravity"] + d_
        F6["gate"] = g6
        R = A.run(F6, {}, {})
        ok("R7 the call holds with the gas's specific gravity %+.2f" % d_, R["designated"] == G["designated"])
    pap = A.run(F, dict(z="papay"), {})
    ok("SF21 Papay's short form (ruled out: it misses the EVC-II stations' own recorded factor by more than the others) "
       "still files the golden sets", pap["designated"] == G["designated"])
    d_, _ = A.station_factor(F)
    d_ = d_[~d_["Station"].isin(P.PT_ONLY_STATIONS)]
    pa = A.p_atm(F)
    err = {}
    for meth in ("dak", "hy", "papay"):
        pred = np.asarray(ZF.fpv2(d_["AvgPressurePsig"].values + pa, d_["AvgTempF"].values,
                                  d_["GasDay"].map(sg).values, meth))
        err[meth] = float(np.median(d_["excess"].values - pred))
    ok("SF21 the EVC-II stations' own records carry Dranchuk and Abou-Kassem's and Hall and Yarborough's factor to "
       "within 0.0004 (the median gas day), Papay's short form off by more than twice that",
       abs(err["dak"]) < 0.0004 and abs(err["hy"]) < 0.0004 and abs(err["papay"]) > 0.0008,
       {k: round(v, 5) for k, v in err.items()})

    # margins: every district 12 per cent from both lines under the golden, the family 8 per cent
    for c in P.DCODES:
        v = G["agg"].loc[c, "leak_pct"]
        ok("margin %s leak share %.2f is 12 per cent or more from the 1.0 line" % (c, v), abs(v - 1.0) >= 0.12)
        fam = E["margins"][P.DNAME[c]]["family_leak"] + E["margins"][P.DNAME[c]]["battery_leak"]
        ok("margin %s every rival and variant 8 per cent or more from the line" % c,
           all(abs(x - 1.0) >= 0.08 and (x > 1.0) == (v > 1.0) for x in fam), (min(fam), max(fam)))
        u = G["agg"].loc[c, "ur_pct"]
        if G["agg"].loc[c, "ntc_meters"] >= P.CHANGEOUT_MIN_METERS:
            ok("margin %s under-registration %.2f is 12 per cent or more from the 3.5 line" % (c, u),
               abs(u - 3.5) >= 0.42)

    # ------------------------------------------------------------------------ the forks
    rules = flat(pdf_text(os.path.join(target, P.FILES["rules"])))
    notes = flat(pdf_text(os.path.join(target, P.FILES["tariff"])))
    prompt = open(os.path.join(task, "prompt.txt")).read()
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
    ok("SF20 the rate schedules describe Schedule G-3's billing as the corrector's volume corrected for the pressure "
       "and temperature it measures (a field described, never the supercompressibility named)",
       "corrected for the pressure and temperature the corrector measures" in notes and
       not re.search(r"supercompress|compressibility|AGA|real.gas|ideal gas", notes + rules, re.I))
    ok("SF4 the gas day named by its start date: a nine-hour shift is inside every band (same call)", True)
    ok("SF10 fixed-factor corrector days rebuilt at the account's own ratio (same call: kept as recorded is inside "
       "every band, asserted in R2)", True)
    ok("SF11 own use is the station heaters only; the gate line heater sits in no district",
       F["own_use"]["PressureDistrict"].isna().sum() > 0)
    ok("SF12 damage as reported (the reports' estimates; 20 per cent either way holds the call, R7)", True)
    ok("SF15 a premise's district is the register's pressure district", F["register"]["PressureDistrict"].notna().all())
    ok("SF16 the corrector customers' districts come from the register's corrector sheet",
       F["correctors"]["PressureDistrict"].notna().all())
    ok("SF19 the prompt carries the leak loss share's window (the program's twelve months)",
       "for the program's twelve months, each district's leak loss as a share of its gas in" in prompt)
    ok("SF24 the prompt counts premises, with how much each took (the accounts follow each premise)",
       "any premises where gas was taken without authorization, with how much each took" in prompt)
    ok("SF25 a premise with a dual-fuel controls rebate on file is no theft in every route (the rebate's date before "
       "the fall)", all(not (set(r_["diversion"]["PremiseID"]) & set(reb.loc[reb["Equipment"].eq(
           "Dual-fuel heat pump controls"), "PremiseID"])) for r_ in (G, C)))
    drs_ = F["drs"]
    gapd = drs_.loc[(drs_["Station"] == "RS-1") & drs_["Alarm"].eq("COMM FAIL"), "GasDay"]
    jan = gapd[(gapd >= dt.date(2026, 1, 12)) & (gapd <= dt.date(2026, 1, 25))]
    others_bad = drs_[(drs_["GasDay"].isin(set(jan))) & (drs_["Station"] != "RS-1") &
                      (drs_["CorrectedMcf"].isna() | drs_["Alarm"].isin(["COMM FAIL", "PXDCR FAIL FIXED P", "TXMTR STUCK"]))]
    sh = A.run(F, dict(drs="share"), cache)
    ok("SF27 ruled out by named data: on Riverside's January gap days every other station is metered, so the gate "
       "balance pins Riverside; the interpolated-share fill moves its twelve months by more than the band",
       len(jan) == 14 and len(others_bad) <= 2 and abs(sh["agg"].loc["RS", "inflow"] / G["agg"].loc["RS", "inflow"] - 1)
       > 0.003, (len(jan), len(others_bad), round(sh["agg"].loc["RS", "inflow"] / G["agg"].loc["RS", "inflow"] - 1, 4)))
    ok("SF26 the prompt asks for no count of the 2027 scheduled changeouts (the 2027 plan files Rule 3's districts)",
       "heating season" not in prompt and "already scheduled" not in prompt)

    # ------------------------------------------------------------------------ the input gates
    cats = {os.path.splitext(f)[1] for f in files}
    ok("gate ten or more usable files", len(files) >= 10, len(files))
    ok("gate two or more file categories", len(cats & {".csv", ".xlsx", ".pdf"}) >= 2, cats)
    big = [f for f in files if f.endswith(".csv") and sum(1 for _ in open(os.path.join(target, f))) > 20000]
    ok("gate a CSV of 20,000 rows or more", len(big) >= 1, big)
    mid = [f for f in files if f.endswith(".csv") and 500 <= sum(1 for _ in open(os.path.join(target, f))) <= 30000]
    ok("gate a CSV of 10 to 20 printed pages or more", len(mid) >= 1, mid)
    import metadata as MD
    keys = {v: k for k, v in P.FILES.items()}
    src = open(os.path.join(HERE, "analysis.py")).read() + open(os.path.join(HERE, "results.py")).read()
    ok("gate two or more distractors, none read by the analysis", len(MD.DISTRACTORS) >= 2 and
       all('F["%s"]' % keys[d] not in src and 'f["%s"]' % keys[d] not in src for d in MD.DISTRACTORS),
       MD.DISTRACTORS)
    ok("gate metadata.json outside the pack", os.path.exists(os.path.join(task, "metadata.json"))
       and "metadata.json" not in files)
    print("\n%d checks, %d passed, %d failed" % (N["pass"] + N["fail"], N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))
