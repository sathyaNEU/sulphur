"""task24: the generator's assertions on the installed build (the bar block R1 to R7, the fork rows, the input gates,
mess neutrality, the factorial and the realism sweep). Exit 1 on any failure.

    python3 checks.py            # reads ../target, ../submission.md, effort.json, figures.json
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import golden as GD  # noqa: E402
import readpack as RP  # noqa: E402
import world as Wd  # noqa: E402

TGT = os.path.join(TASK, "target")
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def main():
    FG = json.load(open(os.path.join(HERE, "figures.json")))
    EF = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TGT))
    # ---------------- input gates
    ok("input: 10 or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {os.path.splitext(f)[1] for f in files}
    ok("input: 2 or more file categories", len(cats & {".csv", ".xlsx"}) and len(cats & {".pdf", ".json"}) and ".sqlite" in cats,
       ", ".join(sorted(cats)))
    big = pd.read_csv(os.path.join(TGT, RP.FILES["passes"]), usecols=["pass_id"])
    ok("input: a messy CSV of 20,000 rows or more", len(big) >= 20000, "%d rows" % len(big))
    rv = pd.read_csv(os.path.join(TGT, RP.FILES["reviews"]), usecols=["review_id"])
    ok("input: a second large CSV (10 to 20 printed pages or more)", len(rv) >= 1000, "%d rows" % len(rv))
    ok("input: 2 or more distractors named only in metadata", len(meta["distractor_files"]) >= 2 and
       not any("distract" in f.lower() for f in files))
    ok("input: no readme, dictionary, notes or manifest file", not any(re.search(r"readme|dictionar|manifest|notes", f, re.I) for f in files))
    # ---------------- the golden on the pack
    G = GD.compute(TGT, quick=True)
    gold = G["call"]
    ok("R7 golden call: accept B, C and E", gold == ["B", "C", "E"], str(gold))
    ok("figures.json call matches", FG["call"] == " ".join(gold))
    for k in "ABCDE":
        c = G["requests"][k]["cost"]
        ok("R6 golden cost %s matches figures.json" % k, abs(round(c, 4 if k == "C" else 2) - FG["R6_cost_%s" % k]) < 1e-9)
        line = Wd.OFFERED[k] / Wd.MARGIN
        ok("R6 %s at least 8 per cent from its line" % k, abs(c / line - 1) >= 0.08, "%.1f per cent" % (100 * (c / line - 1)))
    # ---------------- R3 bar: each hurried figure outside its band where the careful pass loses
    by = {r["id"]: r for r in EF["results"]}

    def outside(rid, cells):
        b, cv = by[rid]["bands"], by[rid]["passes"]["careful"]
        return [c for c in cells if not (b[c][0] <= cv.get(c, float("nan")) <= b[c][1])]
    ok("R3 bar: the careful pass's costs on Corvane, Shelfgrid and Ardley sit outside their bands",
       outside("R6", "ABC") == list("ABC"), str(outside("R6", "ABC")))
    ok("R3 bar: careful QA reviews outside the band on the crowded street and shelf requests", outside("R2", "AB") == list("AB"))
    ok("R3 bar: careful paid minutes outside the band on the crowded street and the video", outside("R3", "AC") == list("AC"))
    ok("R3 bar: careful floor top-up outside the band on the crowded street", outside("R4", "A") == ["A"])
    ok("R3 bar: careful costing outside the band on the parking-lot video", outside("R5", ["P26-0434"]) == ["P26-0434"])
    ok("R3 bar: careful ranges miss on Corvane, Shelfgrid and Ardley",
       all(c in outside("R8", list(by["R8"]["golden"])) for c in ("A_lo", "A_hi", "B_hi", "C_lo", "C_hi")))
    # ---------------- R7 bar: the rivals and perturbations hold the call; shortcuts leave it
    ok("R7 rivals: six defensible variants file the golden set", len(G["rivals"]) == 6 and
       all(d["answer"] == gold for d in G["rivals"].values()))
    ok("R7 perturbations: each fitted input moved by its spread files the golden set", len(G["perturb"]) == 6 and
       all(d["answer"] == gold for d in G["perturb"].values()))
    wrong = [tuple(d["answer"]) for r, d in G["routes"].items() if r != "golden"] + [tuple(d["answer"]) for d in G["extra"].values()]
    ok("R7 shortcuts: every factorial route and shortcut misses the call", tuple(gold) not in wrong)
    alt = G["alternatives"]
    lg = alt["QA re-returns extrapolated by a logistic on the counts"]
    bn = alt["QA returns and re-returns read from 2026's density bins"]
    ok("R7 the over-extrapolating QA alternative files a wrong set (declines Shelfgrid)", "B" not in lg["answer"] and lg["answer"] != gold)
    ok("R7 the density-bin alternative (2026's rates carried to the request's density mix) accepts Corvane: a wrong set",
       "A" in bn["answer"] and bn["answer"] != gold, "%s, Corvane USD %.2f against its line USD %.2f" % (
           bn["answer"], bn["costs"]["A"], Wd.OFFERED["A"] / Wd.MARGIN))
    distinct = set(wrong) | {tuple(lg["answer"]), tuple(bn["answer"])}
    ok("R7 shortcuts: six distinct wrong sets", len(distinct) == 6, str(sorted(distinct)))
    # ---------------- the factorial: two stumps, each necessary, neither sufficient
    rt = G["routes"]
    ok("factorial: the careful pass (reflex route) misses the call", rt["reflex"]["answer"] != gold, str(rt["reflex"]["answer"]))
    ok("factorial J1 QA chain necessary (dropped alone the call moves)", rt["drop_c1"]["answer"] != gold)
    ok("factorial J3 video turnover necessary (dropped alone the call moves)", rt["drop_c3"]["answer"] != gold)
    ok("factorial: neither stump alone on the reflex route reaches the call (the other's drop)",
       rt["drop_c3"]["answer"] != gold and rt["drop_c1"]["answer"] != gold)
    ok("factorial J2 floor is a reflex: the floor on the average paid time leaves the golden set",
       rt["golden"]["answer"] == gold and G["extra"]["the careful pass with the floor on the request's average paid time"]["answer"]
       == rt["reflex"]["answer"])
    # ---------------- R5 bar: no one thing; each factor's footprint across 2026
    T = RP.load(TGT)
    P, R = T["P"], T["R"]
    j = P[(P.kind == "box") & (P.pass_no == 1)].merge(R[["pass_key", "found_missed", "found_misplaced"]], on="pass_key")
    j["ret"] = (j.found_missed + j.found_misplaced) > 0
    pj = j.groupby("project").agg(ret=("ret", "mean"), n=("nobj", "mean"))
    ok("R5 footprint: returns rise with objects per image across every box project", pj[["ret", "n"]].corr().iloc[0, 1] > 0.8,
       "corr %.2f over %d projects" % (pj[["ret", "n"]].corr().iloc[0, 1], len(pj)))
    k2 = P[(P.kind == "box") & (P.pass_no > 1)].merge(R[["pass_key", "found_missed", "found_misplaced"]], on="pass_key")
    k2["ret"] = (k2.found_missed + k2.found_misplaced) > 0
    pk = k2.groupby("project").agg(ret=("ret", "mean"), n=("nobj", "mean"), m=("ret", "size"))
    pk = pk[pk.m >= 200]
    ok("R5 footprint: corrected tasks' re-return rises with objects per image across the box projects",
       pk[["ret", "n"]].corr().iloc[0, 1] > 0.8, "corr %.2f over %d projects" % (pk[["ret", "n"]].corr().iloc[0, 1], len(pk)))
    WK = T["WK"]
    act = P.groupby(["annotator_id", "week", "project"]).active_seconds.sum().reset_index()
    topped = WK[WK.topup > 0].merge(act, on=["annotator_id", "week"]).project.nunique()
    ok("R5 footprint: floor top-ups paid on weeks of many 2026 projects", topped >= 10, "%d projects" % topped)
    ch = T["chunks"]
    ch["proj"] = ch.sequence_id.str[4:8]
    turn = ch.groupby("proj").apply(lambda g: g.starts.sum() / max(1, g.frame_objects.sum()) * 1000)
    ok("R5 footprint: video turnover per object on screen varies across the 2026 video projects", turn.max() / turn.min() > 10)
    # ---------------- R2 mess neutrality: each mess item mishandled leaves the call
    raw = pd.read_csv(os.path.join(TGT, RP.FILES["passes"]))
    ok("R2 mess: sync-retry duplicates exist and are a small share", 0 < raw.duplicated().sum() < 0.005 * len(raw))
    ok("R2 mess: released tasks exist and carry no submission", (raw.pass_type == "released").sum() > 0 and
       raw[raw.pass_type == "released"].submitted_at.isna().all())
    pu = pd.read_csv(os.path.join(TGT, RP.FILES["punch"]))
    ok("R2 mess: shifts closed at midnight each carry a supervisor's edit", (pu.source == "AUTO_CLOSE").sum() ==
       (pu.source == "SUPERVISOR_EDIT").sum() > 0)
    ok("R2 mess: the clock and the register agree on paid hours", abs(T["clock"].paid_hours.sum() - WK.paid_hours.sum() -
                                                                      T["pay_r"].paid_hours.sum()) < 2.0)
    raw_reg = T["pay_raw"]
    ok("R2 mess: the voided re-run nets to nothing", abs(raw_reg[raw_reg.run_id.str.startswith("PR-10B")].piece_pay_usd.sum()) < 0.01)
    # ---------------- semantic fork rows
    ok("SF2 the video request is priced per frame", "per frame" in open(os.path.join(TASK, "prompt.txt")).read())
    ok("SF1 every image is delivered: no chain runs past the fourth review", int(P.pass_no.max()) == 4)
    wk = T["WK"].copy()
    fl = wk.centre.map({"KSM": 2.40, "ILO": 2.70})
    ok("SF4 the register's top-ups are the floor settled per annotator per pay week",
       (np.maximum(0.0, fl * wk.paid_hours - wk.piece) - wk.topup).abs().max() < 0.02,
       "largest gap USD %.3f" % (np.maximum(0.0, fl * wk.paid_hours - wk.piece) - wk.topup).abs().max())
    st = A.staff_for(T, "box")
    ok("SF5 the staffing basis: the roster's box annotators at the pull, shares by contracted hours",
       abs(st.share.sum() - 1) < 1e-9 and st.annotator_id.isin(T["ann"][T["ann"].left_date.isna()].annotator_id).all())
    ok("SF7 overhead is USD 1.55 per paid hour of annotators and reviewers",
       abs(FG["R1_overhead"] - round(1.55 * (FG["R1_ann_hours"] + FG["R1_rev_hours"]))) <= 1)
    weeks = sorted(T["WK"].week.unique())
    ok("SF8 April to October 2026 is the register's 30 pay weeks from 6 April", weeks == list(range(30)), "%d weeks" % len(weeks))
    ok("SF9 the range is the expected cost's uncertainty from the sample; the call rests on the expected cost alone",
       all((FG["R6_range_%s" % k][0] > FG["line_%s" % k]) == (FG["R6_cost_%s" % k] > FG["line_%s" % k]) ==
           (FG["R6_range_%s" % k][1] > FG["line_%s" % k]) for k in "ABCDE"))
    first = P[P.pass_no == 1]
    units = first.groupby(["annotator_id", "week"]).apply(lambda g: float(
        (g.nobj.where(g.kind == "box", 0)).sum() * Wd.RATES["box"] + (g.nobj.where(g.kind == "polygon", 0)).sum() * Wd.RATES["polygon"]
        + (g.nobj.where(g.kind == "video", 0)).sum() * Wd.RATES["track"] + g.frames.fillna(0).sum() * Wd.RATES["frame"]))
    pw = T["WK"].set_index(["annotator_id", "week"]).piece
    jj = pd.concat([units.rename("u"), pw.rename("p")], axis=1).dropna()
    ok("SF10 corrections are unpaid: piece pay is first submissions times the filed rates", (jj.u - jj.p).abs().max() < 0.05,
       "largest gap USD %.3f over %d annotator-weeks" % ((jj.u - jj.p).abs().max(), len(jj)))
    ok("SF6 every review counts (re-reviews included in R2)", FG["R2_reviews_A"] > 2.0)
    proj = pd.read_csv(os.path.join(TGT, RP.FILES["projects"])).set_index("project_code")
    ok("SF12 R5 is graded only on projects closed before the pull", all(proj.loc[p, "end_date"] <= "2026-10-18"
                                                                         for p in ("P26-0446", "P26-0441", "P26-0434")))
    ok("SF13 the golden costing is within 6 per cent on most closed projects", FG["R5_within_6pct"] >= FG["R5_projects"] - 2
       and FG["R5_max_gap_pct"] < 9.0, "%d of %d, max %.1f" % (FG["R5_within_6pct"], FG["R5_projects"], FG["R5_max_gap_pct"]))
    ok("SF11 lowest acceptable price is 1.18 times the expected cost",
       all(abs(FG["R7_lowest_price_%s" % k] - round(Wd.MARGIN * G["requests"][k]["cost"], 4 if k == "C" else 2)) < 0.011
           for k in FG["call_decline"]))
    ok("SF3 expected cost is the mean (the range brackets it)", all(FG["R6_range_%s" % k][0] < FG["R6_cost_%s" % k] < FG["R6_range_%s" % k][1] for k in "ABCDE"))
    # ---------------- realism sweep
    ids = raw.pass_id.drop_duplicates().str[2:].astype(int).sort_values().diff().dropna()
    ok("realism: pass ids are not an arithmetic sequence", ids.nunique() > 1)
    ok("realism: no round headline total", FG["R1_total"] % 100 != 0)
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("realism: no em dash in the answer blocks", "\u2014" not in sub)
    ok("realism: the punch clock stays inside the extract", pu.punch_local.str[:10].max() <= "2026-11-01")
    fails = [r for r in RES if not r[1]]
    for label, good, det in RES:
        print("%s  %-80s %s" % ("PASS" if good else "FAIL", label[:80], det))
    print("%d checks, %d FAIL" % (len(RES), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
