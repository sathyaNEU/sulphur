"""task14: the generator's assertions on the cut pack: the input gates, the realism sweep, the bar block (each result's
golden inside its band, every rival inside, every shortcut route and the hurried passes outside where the note says,
nothing planted, the one-fact test computed), every semantic fork row (SF1 to SF19), each hidden factor's footprint
across the data, the distractor deletion and the golden against the simulated truth.

    python3 task14/generator/checks.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import analysis as AN  # noqa: E402
import conform as CF  # noqa: E402
import docs as DC  # noqa: E402
import measure as MS  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import project as PJ  # noqa: E402

FAILS = []
COUNT = [0]


def check(name, ok, detail=""):
    COUNT[0] += 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + str(detail)) if detail != "" else ""))
    if not ok:
        FAILS.append(name)


def inside(v, b):
    if isinstance(b, dict):
        return all(k in v and b[k][0] - 1e-9 <= v[k] <= b[k][1] + 1e-9 for k in b)
    return b[0] - 1e-9 <= v <= b[1] + 1e-9


def cells_in(v, b):
    return sum(1 for k in b if k in v and b[k][0] - 1e-9 <= v[k] <= b[k][1] + 1e-9), len(b)


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def main():
    target = os.path.join(TASK, "target")
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(target))
    B = F["band_table"]

    # ---------------------------------------------------------------- input gates
    check("ten or more usable files", len(files) >= 10, len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    cats = set()
    for e in exts:
        cats.add({".csv": "spreadsheet", ".xlsx": "spreadsheet", ".pdf": "text"}.get(e, "other"))
    check("two or more file categories", len(cats - {"other"}) >= 2, sorted(cats))
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    big = max(rows.values())
    check("a CSV of 20,000 rows or more", big >= 20000, big)
    long_csv = [f for f, n in rows.items() if n >= 1000 and f != max(rows, key=rows.get)]
    check("a second large CSV of ten printed pages or more", len(long_csv) >= 1, long_csv)
    dis = meta["distractor_files"]
    check("two or more distractors", len(dis) >= 2, dis)
    src = "".join(open(os.path.join(HERE, m)).read() for m in ("conform.py", "measure.py", "project.py", "analysis.py"))
    for d in dis:
        stem = d.split("_20")[0].split(".")[0]
        check("distractor %s read by no golden step" % d, stem not in src and d not in src)
    check("no file name names a trap", not any(re.search(r"readme|dictionary|manifest|notes|known|issue|trap|decoy",
                                                         f, re.I) for f in files))
    check("metadata outside target/", not os.path.exists(os.path.join(target, "metadata.json")))

    # ---------------------------------------------------------------- realism sweep
    texts = {}
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            texts[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".pdf"):
            texts[f] = pdf_text(p)
    alltext = "\n".join(texts.values())
    check("no em or en dash in any shipped text", "\u2014" not in alltext and "\u2013" not in alltext)
    meth = texts.get(PK.FILES["method"], "")
    check("methods paper carries its definitions", all(DC.DEFS[k][:40].split()[0] in meth for k in DC.DEFS) and
          "2.4" in meth, "pdftotext %d chars" % len(meth))
    lw = meth.lower()
    check("methods paper names no method, source or mechanism", not any(w in lw for w in (
        "additional bond", "top-up", "topup", "panel", "operator", "harbourline", "quayside", "migrat", "impute",
        "bootstrap", "project", "survey's rises", "anniversar")), "")
    for f in files:
        if f.endswith(".csv"):
            head = texts[f].splitlines()[0].lower()
            check("%s header describes no process" % f, not re.search(r"impute|derived|adjusted|corrected|flag", head))
    goldnums = ["%.1f per cent" % F["dec26"]["NAT"], "%.1f per cent" % F["sep26"]["NAT"]]
    check("no golden figure sentence in the pack", not any(g in alltext for g in goldnums))

    # ---------------------------------------------------------------- the bar block
    res = {r["id"]: r for r in E["results"]}
    for rid, r in res.items():
        band = r.get("bands") or r.get("band")
        check("%s golden inside its band" % rid, inside(r["golden"], band) if isinstance(band, dict) else
              band[0] - 1e-9 <= r["golden"] <= band[1] + 1e-9)
    # every rival inside its band on every result it touches
    for name, vals in F["rival_values"].items():
        for rid, v in vals.items():
            check("rival '%s' inside %s's band" % (name, rid), inside(v, B[rid]),
                  "%s of %s cells" % cells_in(v, B[rid]) if isinstance(v, dict) else round(v, 3))
    defensible = ["a t multiplier for three back-test years", "the two errors added", "the back-test bias removed",
                  "the projection's error alone"]
    for name in defensible:
        check("range rival '%s' inside R6's band" % name, inside(F["range_rivals"][name], B["R6"]),
              F["range_rivals"][name]["half"])
    check("range rival 'the panel's error alone' inside R6's band (a sampling-error-only range)",
          inside(F["range_rivals"]["the panel's error alone"], B["R6"]),
          F["range_rivals"]["the panel's error alone"]["half"])
    for y, v in F["validation"].items():
        check("on the dwellings both sources hold, rents carried from each starting rent match the survey's reported "
              "rents best (%s)" % y, abs(v["model"]) < 0.5 and v["carry"] > 0.5 and v["recorded"] < -3.0 and
              v["hybrid"] < -0.5 and v["n"] > 2000, v)
    bts = [d for d in F["dec_backtests"] if d["year"] < 2026]
    check("the projection missed each earlier December by 0.1 point or less", all(abs(e) <= 0.1 for e in
                                                                                  F["proj_bt_err"]), F["proj_bt_err"])
    check("a straight trend missed the earlier Decembers by more than the projection did",
          max(abs(e) for e in F["trend_bt_err"]) > max(abs(e) for e in F["proj_bt_err"]), F["trend_bt_err"])
    check("the register as it stands fell short of every earlier December by half a point or more",
          all(s_ >= 0.5 for s_ in F["asstands_short"]), F["asstands_short"])
    check("December 2026's re-letting part is smaller than any earlier December's", F["rest_part_2026"] <
          min(F["rest_part"]), "%.2f against %s" % (F["rest_part_2026"], F["rest_part"]))
    check("the reviews not yet on file add to December 2026 as they did before", F["reviews_part"][-1] > 0.1,
          F["reviews_part"])
    dc = F["dec_churn"]
    check("December 2026's re-lettings let at a smaller margin over the rents they replace than in 2024 or 2025",
          dc["2026"]["margin"] < min(dc["2024"]["margin"], dc["2025"]["margin"]) - 2.0,
          "%.1f against %.1f and %.1f" % (dc["2026"]["margin"], dc["2024"]["margin"], dc["2025"]["margin"]))
    check("the 27 November reading plus earlier years' change to December back-tests worse than the projection",
          F["analog"]["max_error"] > max(abs(e) for e in F["proj_bt_err"]) + 0.05 and
          abs(F["analog"]["dec26"] - F["dec26"]["NAT"]) > B["R7"][1] - F["dec26"]["NAT"],
          "max error %.2f; December %.1f" % (F["analog"]["max_error"], F["analog"]["dec26"]))
    pl = F["panel_link"]
    check("the panel links to the register by address", pl["linked"] >= 0.95 * pl["dwellings"],
          "%d of %d" % (pl["linked"], pl["dwellings"]))
    for y, d in pl["years"].items():
        check("panel anniversaries with an additional bond rose more, and those without less, than the survey's "
              "average in %s" % y, d["with"] > d["all"] > d["without"] and d["n_with"] > 200,
              "%.1f, %.1f, %.1f" % (d["with"], d["all"], d["without"]))
    # every shortcut route's December figure outside R7's band
    for name, d in F["routes_dec"].items():
        if name == "the golden":
            continue
        rv = F["route_values"][name]["R7"]
        check("route '%s' files a December figure outside R7's band" % name, not inside(rv, B["R7"]), round(rv, 3))
    wrong = {v for k, v in F["routes_dec"].items() if k != "the golden" and v != F["routes_dec"]["the golden"]}
    check("shortcuts land on five or more different wrong December figures", len(wrong) >= 5, sorted(wrong))
    # September: the engine shortcuts outside R5's national band
    for name in ("the additional bonds read as every rise", "re-lettings tied by property identifier alone",
                 "re-lettings against the earlier tenancy's starting rent",
                 "careful but hurried: the panel's rises carried to every landlord"):
        v = F["route_values"][name]["R5"]["2026Q3"]
        check("route '%s' outside the September national band" % name, not inside(v, B["R5"]["2026Q3"]), round(v, 3))
    cf = "careful but hurried: the latest recorded rent carried forward at the panel's rate"
    gaps = [F["route_values"][cf]["R5"][q] - F["series"][q] for q in F["series"] if q.startswith(("2023", "2024"))]
    check("recorded rents carried forward run above the measure through 2023 and 2024", max(gaps) > 0.2 and
          min(gaps) > 0.0, "%.2f to %.2f" % (min(gaps), max(gaps)))
    check("recorded rents carried forward miss the re-letting change", not inside(F["route_values"][cf]["R4"], B["R4"]),
          F["route_values"][cf]["R4"])
    # the passes
    care = {rid: r["passes"]["careful"] for rid, r in res.items()}
    quick = {rid: r["passes"]["quick"] for rid, r in res.items()}
    for rid in ("R3", "R6", "R7", "R8"):
        band = res[rid].get("bands") or res[rid].get("band")
        check("careful pass misses %s" % rid, not inside(care[rid], band))
    check("careful pass not right on R5", not inside(care["R5"], res["R5"]["bands"]))
    check("quick pass misses every result", all(not inside(quick[rid], res[rid].get("bands") or res[rid].get("band"))
                                                for rid in res))
    worst = max(len(h["rescues"]) for h in E["hints"])
    check("no single sentence rescues more than a third of the results", worst <= len(res) / 3.0,
          "%d of %d" % (worst, len(res)))
    check("every careful variant scores 50 or under", max(E["careful_variants"].values()) <= 50.0, E["careful_variants"])
    check("the careful pass is the best-scoring variant", E["careful_variants"][E["careful_pass"]] ==
          max(E["careful_variants"].values()), E["careful_pass"])

    # ---------------------------------------------------------------- the files themselves
    D = CF.load(target)
    G = AN.Golden(target, "golden")
    Eng = G.E
    T = Eng.T
    O = D["O"]
    # SF rows
    check("SF1 unbonded tenancies are outside (2.7): the register holds only bonds", "2.7" in DC.DEFS and
          "without a bond" in DC.DEFS["2.7"])
    sep26, sep25 = MS.quarter_end(2026, 3), MS.quarter_end(2025, 3)
    check("SF2 the quarter's day is its last day (2.4)", "last day of the quarter" in DC.DEFS["2.4"])
    check("SF3 rent payable as the agreement stands (2.3)", "as it stands" in DC.DEFS["2.3"])
    fr = D["L"]["RENT_FREQ"].value_counts().to_dict()
    check("SF4 fortnightly and monthly rents ship and convert by 2.3", fr.get("F", 0) > 0 and fr.get("M", 0) > 0 and
          "twelve and divided by fifty-two" in DC.DEFS["2.3"], fr)
    a, b = Eng.matched(sep26, sep25)
    check("SF5 the comparison holds only dwellings let on both days", len(a) == len(b) and len(a) > 50000, len(a))
    overl = T.sort_values(["dwelling", "start"]).groupby("dwelling")["start"].shift(-1)
    n_over = int(((overl.notna()) & (T.sort_values(["dwelling", "start"])["refund"] - 1 >= overl)).sum())
    check("SF6 refunds pending when the next tenancy starts occur and resolve to the later tenancy", n_over > 1000, n_over)
    Ts = T.sort_values(["dwelling", "start", "lodged"], kind="stable")
    nx = Ts.groupby("dwelling")["start"].shift(-1)
    want = np.fmin(Ts["refund"].fillna(np.inf).values - 1, nx.fillna(np.inf).values - 1)
    got = np.where(Ts["end"].values >= 1e9, np.inf, Ts["end"].values)
    never = int((Eng.end < Eng.start).sum())
    check("SF7 a tenancy ends the day before its refund or the next start (2.2)", "day before its bond is refunded" in
          DC.DEFS["2.2"] and bool(np.all(np.isclose(got, want) | (np.isinf(got) & np.isinf(want)))) and
          never < 0.0005 * Eng.n, "%d tenancies at merged room keys never cover a day" % never)
    check("SF8 a re-let dwelling's earlier rent is its own day's rent (2.4)", "rent payable on its own day" in
          DC.DEFS["2.4"])
    conc = D["C"]
    check("SF9 regions by suburb from the concordance for every quarter (2.6)", conc["region_code"].nunique() == 7 and
          "including those before July 2024" in DC.DEFS["2.6"])
    r = Eng.measure(sep26, sep25, G.CL)
    w = np.array([r[g]["n"] for g in MS.REGIONS])
    avg = float(np.average([r[g]["measure"] for g in MS.REGIONS], weights=w))
    check("SF10 the national figure is the ratio of all totals, not the regions' average", abs(avg - r["NAT"]["measure"])
          > 1e-6 and abs(F["sep26"]["NAT"] - round(r["NAT"]["measure"] + 1e-12, 1)) < 1e-9, round(avg, 3))
    check("SF11 rooms let under their own agreement are dwellings", (T["dtype"] == "room").sum() > 1000)
    ev = O["event"].value_counts().to_dict()
    opened = set(O[O["event"].isin(["LODGE", "MIGRATED"])]["bond_id"])
    check("SF12 transfers and changes of parties are events on one bond", ev.get("TRANSFER", 0) > 0 and
          ev.get("PARTIES", 0) > 0 and O[O["event"].isin(["TRANSFER", "PARTIES"])]["bond_id"].isin(opened).all(), ev)
    rr = Eng.measure(sep26, sep25, G.CL, P=G.p)
    check("SF13 the share of continuing tenancies is a count of tenancies", abs(F["cont_share"] - round(
        rr["NAT"]["share_rose"] + 1e-12, 1)) < 1e-9, rr["NAT"]["share_rose"])
    check("SF14 each group's change is its own ratio of totals (2.5)", "computed in the same way" in DC.DEFS["2.5"] and
          abs(F["cont_change"] - round(rr["NAT"]["same"] + 1e-12, 1)) < 1e-9)
    check("SF15 re-let dwellings are let on both days under different tenancies (2.5)",
          F["relet_n"]["NAT"] == rr["NAT"]["n_relet"], rr["NAT"]["n_relet"])
    check("SF16 tenancies held are those covering 30 September 2026 (2.2)", F["held"]["NAT"] == Eng.held_on(sep26)["NAT"])
    check("SF17 the range combines the panel's sampling error and the projection's back-test error",
          abs(F["dec26_half"] - round(1.645 * np.hypot(json.load(open(os.path.join(HERE, "figures.json")))
                                                       ["range_variants"]["the panel's error alone"] / 1.645,
                                                       F["range_variants"]["the projection's error alone"] / 1.645),
                                      2)) <= 0.011, F["dec26_half"])
    c26, cdec = F["contrib26"], F["contrib_dec"]
    check("SF18 the two groups' contributions add back to the measure, in September and in December",
          abs(c26["continuing"] + c26["relet"] - F["sep26"]["NAT"]) < 0.06 and
          abs(cdec["continuing"] + cdec["relet"] - F["dec26"]["NAT"]) < 0.06,
          "%.2f, %.2f" % (c26["continuing"] + c26["relet"], cdec["continuing"] + cdec["relet"]))
    check("SF18 the split is the change in each group's contribution and adds to the change in the measure",
          abs(F["slow"]["fall"] - (F["slow"]["continuing"] + F["slow"]["relet"])) < 1e-9 and
          abs(F["slow"]["fall"] - (F["dec26"]["NAT"] - F["sep26"]["NAT"])) < 0.11, F["slow"])
    lod = O[O["event"] == "LODGE"]
    pk = [(pc,) + tuple(CF.parse_address(a_) or ()) for pc, a_ in zip(lod["postcode"], lod["address"])]
    npid = pd.DataFrame({"k": pk, "pid": lod["property_id"].values}).groupby("k")["pid"].nunique()
    check("SF20 a dwelling's address and its property identifier name the same dwelling (no address carries two)",
          int((npid > 1).sum()) == 0 and len(npid) > 40000, "%d of %d addresses" % (int((npid > 1).sum()), len(npid)))
    check("SF19 the December quarter is 31 December 2026 against 31 December 2025 (2.4)",
          MS.quarter_end(2026, 4) == AN.DEC26 and MS.quarter_end(2025, 4) == AN.DEC25)

    # ---------------------------------------------------------------- hidden factors, across the data
    small = ~Eng.op
    same = a == b
    ii = a[same]
    rec1 = Eng.recorded_rent(ii, sep25)
    rec2 = Eng.recorded_rent(ii, sep26)
    up = rec2 > rec1 + 1e-9
    for gi, g in enumerate(MS.REGIONS):
        k = (Eng.ri[ii] == gi) & small[ii]
        check("additional bonds record under a third of small landlords' continuing tenancies in %s" % g,
              k.sum() > 300 and up[k].mean() < 0.33, round(float(up[k].mean()), 3))
    pairs = G.pairs
    for y in (2019, 2022, 2025):
        check("the panel shows rises for most anniversaries in %d" % y, pairs[pairs["year"] == y]["rose"].mean() > 0.4,
              round(float(pairs[pairs["year"] == y]["rose"].mean()), 3))
    sched = PJ.review_schedule(Eng, cpi=G.cpi)
    check("two operators review on fixed days every year", sorted((v[0], v[1]) for v in sched.values()) ==
          [(11, 1), (12, 1)], {k: v[:3] for k, v in sched.items()})
    for lid, (mo, dd, sh, rule, rises) in sched.items():
        check("operator %s reviews in each of 2023 to 2025" % lid, len(rises) == 3, rises)
        check("operator %s's reviews follow the September CPI plus a fixed margin" % lid,
              rule is not None and rule[0] == 1 and all(abs(rises[y] - G.cpi[(y, 3)] - rule[1]) < 0.06 for y in rises),
              rule)
    a_lid = [k for k, v in sched.items() if (v[0], v[1]) == (12, 1)][0]
    b_lid = [k for k, v in sched.items() if (v[0], v[1]) == (11, 1)][0]
    land = T["landlord_id"].values
    n_a26 = int(((Eng.tops["effective"] == MS.day(2026, 12, 1)) & (land[Eng.tops["i"].values] == a_lid)).sum())
    check("no 1 December 2026 review is on file at the extract's close", n_a26 == 0, n_a26)
    on = F["reviewed_onfile_n"]
    pend = F["pending_n"]
    check("Quayside's 1 November 2026 review is partly on file (between a third and two thirds)",
          0.33 < on / float(on + pend) < 0.67, "%d lodged, %d pending" % (on, pend))
    mig = O[O["event"] == "MIGRATED"]
    by_reg = mig.groupby(mig["postcode"].map(dict(zip(conc["postcode"], conc["region_code"]))))["property_id"].apply(
        lambda s: (s.fillna("") == "").mean())
    check("every migrated bond lacks a property identifier, in every region", len(by_reg) == 7 and
          bool((by_reg > 0.999).all()), by_reg.round(3).to_dict())
    lod = O[O["event"] == "LODGE"]
    check("online lodgements carry property identifiers", (lod["property_id"].fillna("") != "").mean() > 0.99)
    PN = D["PN"]
    blk = {s.upper() for (_o, _r, _d, _u, s, _n, _m) in P.BLOCKS}
    pstreets = PN["address"].str.upper().str.extract(r"\d+[A-Z]?\s+(.+?)\s+(?:STREET|ROAD|AVENUE|TERRACE|CRESCENT|PLACE|"
                                                     r"DRIVE|LANE|GROVE|PARADE|CLOSE|WAY)$")[0]
    opn = {(s.upper(), str(n)) for (_o, _r, _d, _u, s, n, _m) in P.BLOCKS}
    hits = PN["address"].str.upper().apply(lambda s: any(("%s %s " % (n, st)) in s + " " for st, n in opn))
    check("the rent panel holds no operator block", int(hits.sum()) == 0, int(hits.sum()))
    check("operators hold a material share of the bonds held", 0.08 < Eng.op[Eng.in_place(sep26).values].mean() < 0.25,
          round(float(Eng.op[Eng.in_place(sep26).values].mean()), 3))
    ix = G.ix
    gj, gn = [], []
    for ri, g in enumerate(MS.REGIONS):
        s = ix[ri]
        gj.append(s.loc[pd.Period("2026-05", "M"):pd.Period("2026-07", "M")].mean() -
                  s.loc[pd.Period("2025-05", "M"):pd.Period("2025-07", "M")].mean())
        gn.append(s.loc[pd.Period("2026-09", "M"):pd.Period("2026-11", "M")].mean() -
                  s.loc[pd.Period("2025-09", "M"):pd.Period("2025-11", "M")].mean())
    falls = sum(1 for a_, b_ in zip(gj, gn) if b_ < a_)
    check("going rents' annual growth fell from July to November 2026 in most regions", falls >= 5,
          "%d of 7" % falls)
    check("going rents' annual growth fell by a point or more on the regions' average",
          float(np.mean(gj) - np.mean(gn)) >= 0.01, "%.3f to %.3f" % (np.mean(gj), np.mean(gn)))

    # ---------------------------------------------------------------- house fixes on the write-up and golden
    held_by = pd.Series(land[Eng.in_place(sep26).values]).value_counts()
    check("the prompt asks for tenancies in place and the move from September to December",
          "in place at 30 September 2026" in open(os.path.join(TASK, "prompt.txt")).read() and
          "from the September figure to the December one" in open(os.path.join(TASK, "prompt.txt")).read())
    check("the 1 December landlord is the larger build-to-rent landlord (slide 1)", F["a_landlord"] == a_lid and
          F["b_landlord"] == b_lid and held_by.get(a_lid, 0) > held_by.get(b_lid, 0) > 2000,
          "%d against %d bonds held" % (held_by.get(a_lid, 0), held_by.get(b_lid, 0)))
    sub = open(os.path.join(TASK, "submission.md")).read()
    named = set(re.findall(r"\b(?:tbb|pso)_[\w.-]+\.(?:csv|xlsx|pdf)", sub))
    check("every file the write-up names ships in the pack", named <= set(files) and len(named) >= 5, sorted(named))
    cited = set(re.findall(r"\b2\.[1-7]\b", sub))
    check("every methods paper section the write-up cites exists", cited <= set(DC.DEFS), sorted(cited))
    check("the write-up and golden name no business", not re.search(r"Harbourline|Quayside|Student Halls", sub))
    check("one submission.md and one prompt.txt in the task tree",
          sum(1 for r_, _d, fs in os.walk(TASK) for f_ in fs if f_ == "submission.md") == 1 and
          sum(1 for r_, _d, fs in os.walk(TASK) for f_ in fs if f_ in ("prompt.txt", "prompt.md")) == 1)

    # ---------------------------------------------------------------- distractor deletion
    tmp = tempfile.mkdtemp(prefix="task14-nodis-")
    try:
        for f in files:
            if f not in dis:
                shutil.copy(os.path.join(target, f), tmp)
        G2 = AN.Golden(tmp, "golden")
        r2 = G2.E.measure(sep26, sep25, G2.CL)
        d2 = PJ.project(G2.E, G2.CL, ix=G2.ix, cpi=G2.cpi)
        check("deleting the distractors leaves September unchanged", abs(r2["NAT"]["measure"] - r["NAT"]["measure"])
              < 1e-9)
        check("deleting the distractors leaves December unchanged", abs(round(d2["NAT"] + 1e-12, 1) -
                                                                         F["dec26"]["NAT"]) < 1e-9, round(d2["NAT"], 3))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---------------------------------------------------------------- the golden against the simulated truth
    sys.path.insert(0, HERE)
    import truth as TR
    tr = TR.truth()
    check("September 2026 within 0.1 of the truth", abs(r["NAT"]["measure"] - tr["sep26"]["NAT"]) < 0.1,
          "%.3f against %.3f" % (r["NAT"]["measure"], tr["sep26"]["NAT"]))
    check("December 2026 within 0.15 of the truth", abs(F["dec26"]["NAT"] - tr["dec26"]["NAT"]) < 0.15,
          "%.1f against %.3f" % (F["dec26"]["NAT"], tr["dec26"]["NAT"]))
    dev = max(abs(F["series"][q] - tr["series"][q]) for q in F["series"])
    check("every quarter of the back series within 0.15 of the truth", dev < 0.15, round(dev, 3))
    check("tenancies held within 0.3 per cent of the truth", abs(F["held"]["NAT"] / tr["held"] - 1) < 0.003,
          "%d against %d" % (F["held"]["NAT"], tr["held"]))
    check("re-lettings within 2 per cent of the truth", abs(F["relet_n"]["NAT"] / tr["sep26"]["n_relet"] - 1) < 0.02,
          "%d against %d" % (F["relet_n"]["NAT"], tr["sep26"]["n_relet"]))
    check("continuing change within its band of the truth", abs(F["cont_change"] - tr["sep26"]["same"]) < 0.15,
          "%.1f against %.3f" % (F["cont_change"], tr["sep26"]["same"]))
    check("re-letting change within its band of the truth", abs(F["relet_change"] - tr["sep26"]["relet"]) < 0.5,
          "%.1f against %.3f" % (F["relet_change"], tr["sep26"]["relet"]))
    print("%d checks, %d failed" % (COUNT[0], len(FAILS)))
    if COUNT[0] < 40:
        print("FAIL  fewer than forty assertions")
        return 1
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
