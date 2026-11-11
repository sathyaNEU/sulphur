"""task9: the generator's assertions on the built pack: the bar block (R1 to R7), the semantic fork table's closures,
each result's golden, band and margins, the input gates, the realism sweep and the distractors' deletion test.

    python3 task9/generator/checks.py        (after build.py; exit 1 on any FAIL)
"""
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "stumping"))
import analysis as AN  # noqa: E402
import docs as DC  # noqa: E402
import effort as EFF  # noqa: E402
import effort_passes as EP  # noqa: E402
import golden as GD  # noqa: E402
import market as MK  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import record as RC  # noqa: E402
import world as WD  # noqa: E402

TGT = os.path.join(TASK, "target")
ROWS = []


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond)))
    print("%s  %-96s %s" % ("PASS" if cond else "FAIL", label, str(detail)[:150]))


def info(label, detail):
    print("INFO  %-96s %s" % (label, str(detail)[:220]))


def pdf(name):
    out = subprocess.run(["pdftotext", "-layout", os.path.join(TGT, name), "-"], capture_output=True, text=True).stdout
    return " ".join(out.split())


def said(text, sentence):
    return " ".join(sentence.replace("&amp;", "&").split()) in text


def inside(v, b):
    return v is not None and b[0] <= v <= b[1]


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    sub = open(os.path.join(TASK, "submission.md")).read()
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    files = sorted(os.listdir(TGT))
    pol, rmd = pdf(PK.F["policy"]), pdf(PK.F["riskmodel"])
    G = P.GROUP_ORDER
    name = {g: P.GROUPS[g]["name"] for g in G}

    # ------------------------------------------------------------------ the build on disk is this build
    E2 = EP.build(dict(F))
    ok("effort.json on disk is the effort passes laid out from figures.json", json.loads(json.dumps(E2, sort_keys=True)) == json.loads(json.dumps(E, sort_keys=True)))
    ok("the grader here is effort.py's on every cell", all(EFF.grade(r["passes"][p], r)[0] == (
        r["passes"][p]["grade"] if isinstance(r["passes"][p], dict) and "grade" in r["passes"][p] else EP.grade(r["id"], r["passes"][p], F))
        for r in E["results"] for p in ("quick", "careful", "thorough")))
    W = WD.World(mk=MK.Market(), seed=P.SEED)
    R = RC.Record(TGT)
    A = AN.Analysis(R)

    # ------------------------------------------------------------------ input gates
    cats = {"spreadsheet" if f.endswith((".csv", ".xlsx")) else "text" for f in files}
    leg = pd.read_csv(os.path.join(TGT, PK.F["legacy"]))
    cur = pd.read_csv(os.path.join(TGT, PK.F["current"]))
    ok("G 10 or more usable files in two or more categories", len(files) >= 10 and len(cats) >= 2, "%d files, %s" % (len(files), sorted(cats)))
    ok("G one CSV of 20,000 rows or more", len(leg) >= 20000, "%s: %d rows" % (PK.F["legacy"], len(leg)))
    ok("G a second large CSV of ten printed pages or more", len(cur) >= 600, "%s: %d rows" % (PK.F["current"], len(cur)))
    ok("G two distractors, named only in metadata.json", meta["distractor_files"] == PK.DISTRACTORS and all(d in files for d in PK.DISTRACTORS)
       and not any("distract" in f.lower() for f in files))
    ok("G no file describes the pack", not any(re.search(r"readme|dictionary|notes|manifest|guide|codebook", f, re.I) for f in files))
    man = MK.manifest()
    same = []
    for x in man["files"]:
        raw = open(os.path.join(MK.RAW, x["file"]), newline="").read()
        shipped = open(os.path.join(TGT, x["file"]), newline="").read()
        same.append(raw.startswith(shipped) and len(shipped) > 0.9 * len(raw))
    ok("G every public series ships as pulled, cut at the record's last day", all(same) and len(same) == len(man["files"]), "%d of %d" % (sum(same), len(same)))
    ok("G source, pull date and license recorded outside the pack", all(k in s for s in meta["sources"] for k in ("origin", "date", "license")))

    # ------------------------------------------------------------------ the bar block
    figs = ["{:,.0f}".format(F["R4_net"]), "{:,.0f}".format(F["R5_range"]["P10"]), "{:,.0f}".format(F["R5_range"]["P90"]), "%.1f%%" % F["R3_fall"]]
    docs_text = pol + " " + rmd
    ok("R1 no shipped document holds a result", not any(x in docs_text for x in figs), figs)
    wsd = load_workbook(os.path.join(TGT, PK.F["draft"]), data_only=True)
    dtext = " ".join(str(c) for ws in wsd.worksheets for row in ws.iter_rows(values_only=True) for c in row if c is not None)
    ok("R1 the draft carries capital and costs, and no expected P&L or hurdle test", not re.search(r"expected|hurdle|P&L", dtext, re.I), wsd.sheetnames)
    ok("R1 the field's raw material ships: every pod's daily P&L and capital, the market series behind it",
       len(R.days) > 2400 and len(R.groups) > 150 and all(x["file"] in files for x in man["files"]), "%d days, %d pods" % (len(R.days), len(R.groups)))
    # the record rebuilt from the pack is the world's books
    world = W.pod_frame()
    B = PK.Books(W)
    world["code"] = [B.last_code(n) for n in world.n]
    rp = R.panel.copy()
    rp["code"] = rp.n.map(R.code)
    j = world.merge(rp, left_on=["date", "code"], right_on=["date", "code"], how="outer", suffixes=("_w", "_r"), indicator=True)
    miss = j[j._merge != "both"]
    ok("R2 the record on one footing holds every pod-day of the books but the feed's three missed days", set(miss.date.dt.strftime("%Y-%m-%d")) <= {
        x.strftime("%Y-%m-%d") for x in PK.OUTAGES} and len(miss) > 0, "%d pod-days off, on %s" % (len(miss), sorted(set(miss.date.dt.strftime("%Y-%m-%d")))))
    both = j[j._merge == "both"]
    ok("R2 capital on one footing matches the books to the export's rounding", float((both.capital_w - both.capital_r).abs().max()) <= 5.1e4,
       float((both.capital_w - both.capital_r).abs().max()))
    ok("R2 the legacy file repeats one day and the 2023 file states thousands and millions", R.n_dupes > 0 and list(cur.columns) ==
       ["trade_date", "book_id", "pnl_usd_000", "alloc_capital_usd_mm"], R.n_dupes)
    adm = pd.read_csv(os.path.join(TGT, PK.F["admin"]), dtype={"sleeve": str})
    cmap = pd.read_csv(os.path.join(TGT, PK.F["codes"]), dtype=str)
    to_new = dict(zip(cmap.old_pod_code, cmap.new_book_id))
    adm["pod"] = adm.sleeve.map(lambda c: to_new.get(c, c))
    adm["m"] = adm.period_end.str[:7]
    rp["m"] = rp.date.dt.strftime("%Y-%m")
    mon = rp.groupby(["code", "m"]).pnl.sum()
    am = adm.set_index(["pod", "m"]).gross_trading_pnl
    jj = pd.concat([mon.rename("risk"), am.rename("admin")], axis=1, join="inner")
    off = (jj.risk - jj.admin).abs()
    ok("R2 the risk system's months agree with the administrator's apart from the month-end true-ups", float((off <= 5e4).mean()) > 0.5 and
       float(abs(jj.risk.sum() - jj.admin.sum()) / abs(jj.admin.sum())) < 0.002, "%.0f%% of pod-months within USD 50,000; totals %.4f%% apart" % (
           100 * float((off <= 5e4).mean()), 100 * float(abs(jj.risk.sum() - jj.admin.sum()) / abs(jj.admin.sum()))))
    g = lambda rid, v: EP.grade(rid, v, F)
    quick, careful, gold, hints, compounds = EP.passes(F)
    want = {"R1": "partly", "R2": "right", "R3": "missed", "R4": "missed", "R5": ("partly", "missed"), "R6": "missed"}
    for rid, w in want.items():
        ok("R3 careful pass on %s is %s" % (rid, w if isinstance(w, str) else " or ".join(w)), g(rid, careful[rid]) in (w if isinstance(w, tuple) else (w,)),
           json.dumps(careful[rid])[:110])
    ok("R3 the thorough pass earns everything and the quick pass a third or less", all(g(r, gold[r]) == "right" for r in want) and
       sum({"right": 1, "partly": 0.5, "missed": 0}[g(r, quick[r])] for r in want) <= len(want) / 3.0)
    rt = F["routes"]
    for k in ("risk model's factors", "each pod's own record", "careful but hurried", "capacity across pods"):
        ok("R3 %s: the expected year sits outside its band by 3 per cent or more" % k, rt[k]["mean"] >= F["R4_band"][1] * 1.03,
           "%.1f against %s" % (rt[k]["mean"], F["R4_band"]))
    ok("R3 careful: credit's alpha on the risk model's factors sits above its band", F["R1_risk_model"]["Credit"] > F["R1_bands"]["Credit"][1] + 0.5,
       "%.2f against %s" % (F["R1_risk_model"]["Credit"], F["R1_bands"]["Credit"]))
    ok("R3 careful: a year of independent days puts the 10th percentile above its band", rt["daily resampling"]["p10"] > F["R5_bands"]["P10"][1],
       "%.1f against %s" % (rt["daily resampling"]["p10"], F["R5_bands"]["P10"]))
    ok("R3 careful: judged on the pod's return at its new size, a failing increase passes", not set(F["R6_fail"]) <= set(rt["average return at the new size"]["fail"]),
       rt["average return at the new size"]["fail"])
    ok("R3 across pods capacity reads a fifth of the within-pod fall or less", F["R3_rivals"]["pooled"] <= F["R3_fall"] / 5.0, F["R3_rivals"]["pooled"])
    hash_ = {f: hashlib.sha256(open(os.path.join(TGT, f), "rb").read()).hexdigest() for f in files}
    ok("R4 no file is a copy of another", len(set(hash_.values())) == len(files))
    ok("R4 no document argues for a plan figure or an increase", not re.search(r"recommend|we expect|should be|forecast", docs_text, re.I))
    ok("R4 the past plans answer past years only", load_workbook(os.path.join(TGT, PK.F["plans"])).sheetnames == ["Plan %d" % y for y in P.PLAN_YEARS])
    # genuine patterns, across the data
    Ah, Ar = A.attribution("hold"), A.attribution("risk")
    cr = [n for n, a in Ah.items() if a["g"] == "CREDIT" and a["days"] >= 252]
    up = [n for n in cr if Ar[n]["alpha"] > Ah[n]["alpha"]]
    ok("R5 carry shows in the risk model's alpha for nearly every credit pod with a year of record", len(up) >= 0.85 * len(cr), "%d of %d" % (len(up), len(cr)))
    vr = {f: MK.annual_sd(R.hold[f], "monthly") / MK.annual_sd(R.hold[f], "daily") for f in ("CREDIT", "VOL", "MKT", "RATES")}
    ok("R5 the markets' own serial dependence: credit trends and the VIX reverts", vr["CREDIT"] > 1.2 and vr["VOL"] < 0.8, {k: round(v, 2) for k, v in vr.items()})
    per = {}
    for gg in G:
        D = A.pod_years("hold")
        D = D[D.g == gg]
        per[gg] = AN.Analysis.fit_theta(D, by="n") if D.n.nunique() >= 5 else float("nan")
    ok("R5 capacity is in every strategy group, not only the deciding pods", all(v > 0.15 for v in per.values() if v == v), {k: round(v, 2) for k, v in per.items()})
    chg = pd.read_csv(os.path.join(TGT, PK.F["changes"]))
    rev = chg[chg.reason == "Annual review"]
    ok("R5 the committee moves capital at every review from 2019 (the launch allocations held through 2018)", rev.effective_date.str[:4].nunique() >= 8
       and "2018" not in set(rev.effective_date.str[:4]), sorted(rev.effective_date.str[:4].unique()))
    ok("R5 the drawdown rules acted in every year of the record", chg[chg.reason.str.startswith("Halved")].effective_date.str[:4].nunique() >= 9)
    hs = {x["sentence"]: x["rescues"] for x in E["hints"]}
    n = len(E["results"])
    ok("R6 the most useful single sentence rescues a third of the results or fewer", max(len(v) for v in hs.values()) <= n / 3.0,
       "; ".join("%s: %s" % (k[:40], v) for k, v in hs.items()))
    info("R6 two moves at once (information)", "; ".join("%s: %d of %d" % (x["moves"], len(x["rescues"]), n) for x in E["compounds"]))
    wrong = {json.dumps(r["answer"], sort_keys=True) for r in E["routes"] if not r.get("golden")}
    ok("R6 different shortcuts land on different wrong answers", len(wrong) >= 4, "%d distinct" % len(wrong))
    for key, gb in (("R1_rivals", "R1_bands"),):
        bad = [(k, gg) for k, v in F[key].items() for gg, x in v.items() if not inside(x, F[gb][gg])]
        ok("R7 every %s rival inside its band" % key[:2], not bad, bad[:3])
    ok("R7 every capacity rival within pods inside R3's band", all(inside(F["R3_rivals"][k], F["R3_band"]) for k in ("pod", "pod-weighted", "pod-quarter", "ramp", "onboard", "pod200")))
    ok("R7 every forecast rival inside R4's band", all(inside(v, F["R4_band"]) for v in F["R4_rivals"].values()), F["R4_rivals"])
    ok("R7 every forecast rival's percentiles inside R5's bands", all(inside(v["P10"], F["R5_bands"]["P10"]) and inside(v["P90"], F["R5_bands"]["P90"])
                                                                     for v in F["R5_rivals"].values()))
    ok("R7 the failing increases are four or more and the borderline ones six or fewer", len(F["R6_fail"]) >= 4 and len(F["R6_either"]) <= 6,
       (F["R6_fail"], F["R6_either"]))
    ok("R7 the plan with the borderline increases also dropped stays inside R7's band", inside(F["R7_with_either_dropped"], F["R7_band"]))

    # ------------------------------------------------------------------ the semantic fork table, closed in the files
    for label, s in (("SF1 alpha is net of a passive holding of a pod's markets", DC.ALPHA), ("SF2 markets expected to earn nothing", DC.PLAN_A),
                     ("SF3 every pod runs the year under the drawdown rules", DC.PLAN_B), ("SF4 net of funding, payouts and platform costs", DC.PLAN_C),
                     ("SF5 the range is the 10th to the 90th percentile", DC.PLAN_D), ("SF6 capacity as one share per doubling", DC.PLAN_E),
                     ("SF15 each pod's expected alpha from its whole record beside its group's", DC.PLAN_F),
                     ("SF7 the hurdle on the capital added", DC.HURDLE),
                     ("SF8 payouts pod by pod", DC.PAYOUT), ("SF9 the drawdown rules", DC.DRAWDOWN), ("SF10 funding", DC.FUNDING),
                     ("SF11 the onboarding schedule", DC.ONBOARD)):
        ok(label + " (policy text)", said(pol, s))
    ok("SF14 alpha on the record's gross P&L, the administrator's statements the books of account (policy text)", said(pol, DC.RECORDS) and said(pol, DC.PAYOUT))
    ok("SF12 the draft names each increase in its own column", set(r[4] for r in wsd["Draft 2027"].iter_rows(min_row=4, values_only=True) if r[0] and r[0] != "Total")
       == {"Increase", "Decrease", "No change", "Onboarding"})
    ok("SF13 the prompt asks since 2017 and the record starts there", "2017" in prompt and F["record"]["first"] == "2017-01-03")

    # ------------------------------------------------------------------ goldens and the blocks agree
    for k, v in (("R4", "USD {:,.0f} million".format(F["R4_net"])), ("R5 P10", "USD {:,.0f} million".format(F["R5_range"]["P10"])),
                 ("R5 P90", "USD {:,.0f} million".format(F["R5_range"]["P90"])), ("R3", "%.1f%%" % F["R3_fall"])):
        ok("blocks state %s as figures.json does" % k, v in sub, v)
    ok("blocks name every failing increase", all(p in sub for p in F["R6_fail"]))
    ok("blocks state every group's alpha", all("%s %.2f%%" % (gg, F["R1_alpha"][gg]) in sub for gg in F["R1_alpha"]))
    gw = load_workbook(os.path.join(TASK, "golden", GD.BOOK), data_only=True)
    ok("the golden workbook's first figure is figures.json's", abs(gw["2027 plan"]["B5"].value - F["R4_net"]) < 1e-6, gw["2027 plan"]["B5"].value)
    ok("the golden holds exactly the requested files", sorted(os.listdir(os.path.join(TASK, "golden"))) == sorted([GD.BOOK, GD.DECK]))

    # ------------------------------------------------------------------ realism sweep
    alltext = docs_text + " " + sub + " " + prompt
    ok("realism: no em dash in the pack's documents, the blocks or the prompt", "—" not in alltext and "–" not in alltext)
    ok("realism: personas are the card's", (P.CIO, P.CRO, P.CFO) == ("Christine Owen", "Nicholas Riddle", "Kathryn Roberts"))
    step = chg[chg.reason == "Onboarding step"].set_index(["pod", "effective_date"]).capital_after_usd
    caps = [float(step.get((r.pod, r.effective_date), r.capital_after_usd)) for r in rev.itertuples()]
    ok("realism: review figures are in USD 5 million steps (once a same-day onboarding step lands)", all(x % 5e6 == 0 for x in caps))
    halv = chg[chg.reason.str.startswith("Halved")]
    rate = len(halv) / (len(R.panel) / 252.0)
    ok("realism: halvings run at a few in a hundred pod-years to under a third (5 per cent drawdowns on 3 to 8 per cent risk)", 0.03 <= rate <= 0.30, round(rate, 3))
    sr = []
    for nn, a in Ah.items():
        if a["days"] >= 504:
            r = (a["resid"] + 0.0)
            sr.append(float(r.mean() / r.std() * np.sqrt(252)))
    ok("realism: pods' alpha Sharpe ratios sit between 0 and 3 for most", float(np.mean([(0 < s < 3) for s in sr])) > 0.8, round(float(np.median(sr)), 2))

    # ------------------------------------------------------------------ the distractors decide nothing
    ok("D the market build reads neither distractor", not any(d.replace(".csv", "") in open(os.path.join(HERE, "market.py")).read() for d in PK.DISTRACTORS))

    fails = [r for r in ROWS if not r[1]]
    print("checks: %d of %d PASS" % (len(ROWS) - len(fails), len(ROWS)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
