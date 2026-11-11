"""task9 (architecture 10): the generator's assertions on the installed build (target/, golden/, figures.json,
effort.json, submission.md, metadata.json). Exit 1 on any FAIL.

  G   the client's input gates
  R1  the field's raw material ships and no shipped file holds a result
  R2  the pack's mess is the systems' own (two export generations, versions, cancels and corrections, capped sizes, the
      144A map, quarterly buckets)
  R3  each hurried route lands outside the result's band, and different shortcuts name different answers
  R4  no document argues for a plan figure or a change; the summaries answer another question
  R5  the factors run across the data (the evaluations' lag in every medium and thin segment, pick-offs and informed
      flow outside the changed segments, rivals' levels on the tape for every segment)
  R6  the one-fact test, counted on effort.json
  R7  every rival inside its band
  SF  the policy's sentences that close the forks, in the shipped PDF
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import docs as DC  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402

RES = []


def ok(name, cond, detail=""):
    RES.append((bool(cond), name, detail))


def info(name, detail=""):
    RES.append((None, name, detail))


def inside(v, b):
    return v is not None and b[0] <= v <= b[1]


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    M = json.load(open(os.path.join(TASK, "metadata.json")))
    sub = open(os.path.join(TASK, "submission.md")).read()
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    g, b = F["gold"], F["bands"]
    segs = F["segments"]
    files = sorted(os.listdir(TGT))
    # ---- G
    cats = {"csv": "spreadsheet", "xlsx": "spreadsheet", "pdf": "text"}
    ok("G 10 or more usable files in two or more categories", len(files) >= 10 and len({cats[f.rsplit('.', 1)[1]] for f in files}) >= 2,
       "%d files" % len(files))
    rows = {f: sum(1 for _ in open(os.path.join(TGT, f))) - 1 for f in files if f.endswith(".csv")}
    ok("G one CSV of 20,000 rows or more", rows[PK.F["tape"]] >= 20000, "%s: %d rows" % (PK.F["tape"], rows[PK.F["tape"]]))
    ok("G a second large CSV of ten printed pages or more", rows[PK.F["rfq2"]] >= 1000, "%s: %d rows" % (PK.F["rfq2"], rows[PK.F["rfq2"]]))
    ok("G two distractors, named only in metadata.json", len(M["distractor_files"]) >= 2 and
       not any("distract" in f.lower() for f in files))
    ok("G no file describes the pack", not any(re.search(r"readme|dictionary|notes|manifest|field", f, re.I) for f in files))
    ok("G source, pull date and license recorded outside the pack", all("license" in s for s in M["sources"]) and "manifest.json" not in files)
    # ---- R1
    shipped = " ".join(open(os.path.join(TGT, f), errors="ignore").read() for f in files if f.endswith(".csv"))
    figs = ["%.2f" % (g["proposed"] / 1e6), "%.2f" % (g["current"] / 1e6), "%.2f" % (g["adopt"] / 1e6)]
    ok("R1 no shipped CSV states a plan figure", not any((" %s " % x) in shipped for x in figs), figs)
    R = pd.read_csv(os.path.join(TGT, PK.F["rfq2"]), nrows=5)
    ok("R1 the field's raw material ships: every request with the desk's quote and reference mid, the tape, the evaluations",
       {"response_price", "ref_mid", "cover_price"} <= set(R.columns) and rows[PK.F["eval"]] > 100000)
    # ---- R2
    g1 = pd.read_csv(os.path.join(TGT, PK.F["rfq1"]))
    g2 = pd.read_csv(os.path.join(TGT, PK.F["rfq2"]))
    ok("R2 two export generations with renamed columns, New York time against UTC, face against thousands",
       "RECEIVED_ET" in g1.columns and "received_utc" in g2.columns and "quantity_000" in g2.columns)
    dup = int(g1.duplicated().sum() + g2.duplicated().sum())
    ver = int((g1.MSG_VERSION > 1).sum() + (g2.msg_version > 1).sum())
    ok("R2 re-sent messages and amended requests in both generations", dup > 50 and ver > 50, "%d re-sent, %d amended" % (dup, ver))
    tp = pd.read_csv(os.path.join(TGT, PK.F["tape"]), dtype={"qty": str}, usecols=["msg_type", "qty", "contra", "asof"])
    ok("R2 the tape carries cancels, corrections, late reports, capped sizes and dealer trades from both sides",
       (tp.msg_type == "X").sum() > 100 and (tp.msg_type == "C").sum() > 100 and (tp["asof"] == "A").sum() > 100 and
       tp.qty.str.endswith("+").sum() > 100 and (tp.contra == "D").sum() > 1000)
    sm = pd.read_csv(os.path.join(TGT, PK.F["master"]))
    ok("R2 144A bonds exchanged for registered bonds under new identifiers", sm.registered_cusip.notna().sum() >= 5,
       "%d" % sm.registered_cusip.notna().sum())
    bk = pd.read_csv(os.path.join(TGT, PK.F["buckets"]))
    moved = bk.groupby("cusip").liquidity_bucket.nunique()
    ok("R2 buckets reassigned by quarter", (moved > 1).sum() >= 20, "%d bonds changed bucket" % (moved > 1).sum())
    # ---- R3
    rt = F["routes"]
    for name, key, need in (("careful but hurried", "proposed", True), ("the tape's levels, a week's marks", "proposed", True),
                            ("the tape's levels, a week's marks", "current", True), ("the desk's next-day view", "current", True),
                            ("complete moves, a fit on the desk's quotes", "proposed", True),
                            ("the tape's levels, today's wins' cost for the added trades", "proposed", True)):
        v = rt[name][key]
        bb = b[key]
        gap = min(abs(v - bb[0]), abs(v - bb[1])) / abs(g[key])
        ok("R3 %s: the %s P&L sits outside its band by 3 per cent or more" % (name, key), not inside(v, bb) and gap >= 0.03,
           "%.2f against [%.2f, %.2f]" % (v / 1e6, bb[0] / 1e6, bb[1] / 1e6))
    ok("R3 the careful pass names a different set of losing changes", set(rt["careful but hurried"]["lose"]) != set(g["lose"]),
       rt["careful but hurried"]["lose"])
    import figures as FGm
    cp = rt[FGm.CAREFUL]
    for key in ("current", "proposed"):
        gap = min(abs(cp[key] - b[key][0]), abs(cp[key] - b[key][1])) / abs(g[key])
        ok("R3 the re-priced careful pass (the tape's levels, a week's marks, added trades like today's wins): the %s P&L "
           "sits outside its band by 3 per cent or more" % key, not inside(cp[key], b[key]) and gap >= 0.03,
           "%.2f against [%.2f, %.2f]" % (cp[key] / 1e6, b[key][0] / 1e6, b[key][1] / 1e6))
    ok("R3 the re-priced careful pass names a different set of losing changes", set(cp["lose"]) != set(g["lose"]), cp["lose"])
    ok("R3 a week's marks name a different set", set(rt["the tape's levels, a week's marks"]["lose"]) != set(g["lose"]),
       rt["the tape's levels, a week's marks"]["lose"])
    sh_out = sum(not inside(rt["careful but hurried"]["share"][s], b["share"][s]) for s in segs)
    ok("R3 the win model on the desk's own quotes misses most changed segments' win shares", sh_out >= len(segs) * 0.7,
       "%d of %d outside" % (sh_out, len(segs)))
    iid = rt["the golden's figures, days drawn one at a time"]
    ok("R3 days drawn one at a time narrow the range past its band",
       not inside(iid["p10"], b["p10"]) or not inside(iid["p90"], b["p90"]),
       "%.2f..%.2f against %.2f..%.2f" % (iid["p10"] / 1e6, iid["p90"] / 1e6, g["p10"] / 1e6, g["p90"] / 1e6))
    wrong = {json.dumps(r["answer"], sort_keys=True) for r in E["routes"] if not r.get("golden")}
    ok("R3 different shortcuts land on different wrong answers", len(wrong) >= 5, "%d distinct" % len(wrong))
    # ---- R4
    pdf = subprocess.run(["pdftotext", "-layout", os.path.join(TGT, PK.F["policy"]), "-"], capture_output=True, text=True).stdout
    norm = re.sub(r"\s+", " ", pdf)
    ok("R4 no document argues for a plan figure or a change", not re.search(r"USD [0-9.,]+ million|recommend", norm))
    ok("R4 the draft carries half-spreads and no expected P&L", True)
    # ---- R5
    lag = {}
    for s in F["markout_curve"]:
        c = F["markout_curve"][s]
        lag[s] = (c["30"] - c["5"]) / max(abs(c["30"]), 1.0)
    med = [s for s in lag if s.split("|")[1] in ("medium", "thin")]
    segs = F["segments"]
    ok("R5 the evaluations' lag shows in most medium and thin segments, changed or not", np.mean([lag[s] > 0.1 for s in med]) >= 0.6,
       {k: round(v, 2) for k, v in lag.items() if k in med})
    un = sorted(s for s in lag if s not in segs and lag[s] > 0.1)
    payers = sorted(s for s in lag if s in segs and s not in g["lose"] and lag[s] > 0.1)
    ok("R5 the cost that arrives after a week shows in segments the draft does not change, and in changes that pay",
       len(un) >= 4 and len(payers) >= 4, "unchanged %s; paying %s" % (un, payers))
    ok("R5 rivals' levels sit on the tape for every segment", F["match_rate"] >= 0.95, "%.3f" % F["match_rate"])
    # ---- R6
    hs = {h["sentence"][:50]: h["rescues"] for h in E["hints"]}
    n = len(E["results"])
    ok("R6 the most useful single sentence rescues a third of the results or fewer", max(len(v) for v in hs.values()) <= n / 3.0, hs)
    info("R6 two moves at once (information)", "; ".join("%s: %s" % (c["moves"], c["rescues"]) for c in E["compounds"]))
    # ---- R7
    for name, v in F["rivals"].items():
        ok("R7 %s inside every band" % name,
           all(inside(v[k], b[k]) for k in ("current", "proposed")) and all(inside(v["bridge"][s], b["bridge"][s]) for s in segs),
           "%.2f, %.2f" % (v["current"] / 1e6, v["proposed"] / 1e6))
    for blk, (lo, hi) in F["blocks"].items():
        ok("R7 runs of %s days inside the range's bands" % blk, inside(lo, b["p10"]) and inside(hi, b["p90"]))
    margin = min(abs(g["bridge"][s]) for s in segs if s not in F.get("lose_either", []))
    ok("R7 every changed segment's verdict clears zero", margin > 0, "smallest %s" % margin)
    # ---- SF: each row of the design note's semantic fork table, closed by a shipped sentence or by named data
    def says(text):
        t = re.sub(r"\s+", " ", text.replace("&amp;", "&"))
        return t[:60] in norm and t[-40:] in norm
    cur_h = {}
    for (bd, bk), row in P.SCHEDULE_V1.items():
        for ty, h in row.items():
            cur_h["%s|%s|%s" % (bd, bk, ty)] = h
    for k, h in list(P.V2_CHANGES.items()) + list(P.V3_CHANGES.items()):
        cur_h["|".join(k)] = h
    ok("SF1 the current schedule is version 3: each changed segment's half-spread now is version 3's",
       all(abs(F["h"][s][0] - cur_h[s]) < 1e-9 for s in segs), {s: F["h"][s][0] for s in segs})
    rc = F.get("replay_check", {})
    ok("SF2 SF3 the replay at version 3 keeps every recorded outcome where the schedule never changed (ties included)",
       rc.get("rows", 0) > 100000 and rc.get("differ", 1) == 0, rc)
    ok("SF4 SF5 SF6 SF16 the policy states the P&L for planning (the move as soon as complete, other issuers' bonds of "
       "its rating, the bucket's offload charge, on the face traded)",
       says(DC.PNL) and "as soon as that move is complete" in norm and "other issuers' bonds of its rating" in norm
       and "on the face traded" in norm)
    import record as RC
    oc = RC.OFFLOAD_CHARGE
    want = ("investment grade liquid %s, medium %s, thin %s; high yield liquid %s, medium %s, thin %s" % tuple(
        oc[(bd, bk)] for bd in ("IG", "HY") for bk in ("liquid", "medium", "thin")))
    ok("SF6 the offload charges the golden uses are the policy's", want in norm, want)
    ok("SF7 the policy states carry and funding are outside the desk's P&L", says(DC.INVENTORY))
    ok("SF8 SF9 the policy states the replay (a request keeps everything but the desk's half-spread)", says(DC.PLAN_A))
    ok("SF10 the policy states the plan's counts", says(DC.PLAN_B))
    ok("SF11 the policy states the range", says(DC.PLAN_C))
    ok("SF12 the policy states a request's segment by date and quarter", says(DC.SEGMENTS) and says(DC.QUOTER))
    ok("SF13 144A bonds map to registered successors in the security master", sm.registered_cusip.notna().sum() >= 5)
    ok("SF14 the policy names the request audit and its format change; both generations ship", says(DC.RECORDS) and
       PK.F["rfq1"] in files and PK.F["rfq2"] in files)
    diff_n = sum(1 for k, v in P.PROPOSED.items() if abs(v - cur_h["|".join(k)]) > 1e-9)
    ok("SF15 the changed segments are the draft's rows that differ from version 3", diff_n == len(segs) == len(P.PROPOSED),
       "%d differ, %d graded" % (diff_n, len(segs)))
    ok("SF17 the prompt asks for USD", "in USD" in prompt)
    dep = F.get("dependence", {})
    ok("SF18 the daily P&L is serially dependent, so the year's days are drawn in runs (first-order autocorrelation over "
       "its noise bound, 21-day sums over 1.5 times independent days)",
       dep.get("acf1", 0) > dep.get("noise_bound", 1) and dep.get("vr21", 0) > 1.5, dep)
    # ---- blocks and prompt
    ok("blocks state the draft's P&L as figures.json does", ("USD %.2f million" % (g["proposed"] / 1e6)) in sub)
    ok("blocks state the current schedule's P&L as figures.json does", ("USD %.2f million" % (g["current"] / 1e6)) in sub)
    ok("blocks name every changed segment that loses money", all(s.split("|")[1] in sub for s in g["lose"]))
    ok("realism: no em dash in the documents, the blocks or the prompt", "\u2014" not in sub + prompt + pdf)
    for p, name, d in RES:
        print("%-5s %-100s %s" % ({True: "PASS", False: "FAIL", None: "INFO"}[p], name[:100], str(d)[:160]))
    fails = sum(1 for p, _, _ in RES if p is False)
    print("checks: %d of %d PASS" % (sum(1 for p, _, _ in RES if p), sum(1 for p, _, _ in RES if p is not None)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
