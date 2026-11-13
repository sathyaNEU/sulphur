"""task9: the generator's assertions on a built output folder (python3 checks.py <out>): the input gates, the bar block
(R1 to R7 of dataset-generation 7.1), mess neutrality, the bands and the hurried figures, distractors, the realism sweep."""
import csv
import json
import os
import re
import sqlite3
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import effort_passes as EP  # noqa: E402
import pack as PK  # noqa: E402

RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def inside(v, b):
    return b[0] <= v <= b[1]


def main(out=None):
    """out: a build folder (build.py --out), or None for the installed task folder"""
    gen = HERE if out is None else out
    out = os.path.dirname(HERE) if out is None else out
    tgt = os.path.join(out, "target")
    fg = json.load(open(os.path.join(gen, "figures.json")))
    E = json.load(open(os.path.join(gen, "effort.json")))
    B = fg["bands"]
    names = sorted(os.listdir(tgt))
    exts = {n.rsplit(".", 1)[1] for n in names}
    cats = {"csv": "spreadsheet", "xlsx": "spreadsheet", "sqlite": "database", "jsonl": "text", "txt": "text",
            "pdf": "text", "yaml": "code"}
    # ---- input gates
    ok("gate: ten or more usable files", len(names) >= 10, "%d files" % len(names))
    ok("gate: two or more file categories", len({cats[x] for x in exts}) >= 2, str(sorted({cats[x] for x in exts})))
    n_mes = sum(1 for _ in open(os.path.join(tgt, PK.F["mes"]))) - 1
    ok("gate: a CSV of 20,000 rows or more", n_mes >= 20000, "%s %d rows" % (PK.F["mes"], n_mes))
    n_sds = sum(1 for _ in open(os.path.join(tgt, PK.F["sds"]))) - 1
    ok("gate: a long CSV (10 to 20 printed pages or more)", n_sds >= 1000, "%s %d rows" % (PK.F["sds"], n_sds))
    ok("gate: two or more distractors", len(PK.DISTRACTORS) >= 2 and all(d in names for d in PK.DISTRACTORS))
    ok("gate: no file names a distractor or a readme", not any(re.search(r"distract|readme|dictionary|manifest|notes_on", n, re.I) for n in names))
    con = sqlite3.connect(os.path.join(tgt, PK.F["sort"]))
    tabs = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    ok("gate: the yield database carries its six tables", len(tabs) == 6, str(tabs))
    size = sum(os.path.getsize(os.path.join(tgt, n)) for n in names)
    ok("gate: the pack is about 40 MB", 30e6 <= size <= 60e6, "%.1f MB" % (size / 1e6))
    cut = PK.P.PULL.strftime("%Y-%m-%d %H:%M:%S")
    late_sort = con.execute("SELECT COUNT(*) FROM sort_wafer WHERE end_time >= ?", (cut,)).fetchone()[0]
    late_mes = sum(1 for r in csv.DictReader(open(os.path.join(tgt, PK.F["mes"]), newline=""))
                   if r["TRACK_IN"] >= cut or (r["TRACK_OUT"] or "") >= cut)
    late_wat = sum(1 for r in csv.DictReader(open(os.path.join(tgt, PK.F["wat"]), newline="")) if r["test_time"] >= cut)
    ok("gate: no sort, MES or e-test record falls after the pull", late_sort == late_mes == late_wat == 0,
       "sort %d, MES %d, WAT %d" % (late_sort, late_mes, late_wat))
    # ---- R1: the raw material ships, no result precomputed
    ok("R1 raw: die maps for every sorted wafer", con.execute("SELECT COUNT(DISTINCT wafer_key) FROM sort_map").fetchone()[0] > 10000)
    heads = []
    for n in names:
        if n.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(tgt, n), newline="", encoding="utf-8")))
    bad = [h for h in heads if re.search(r"cause|yield_loss|bath_ppb|polymer|attribut|scratch_kill|edge_offset|loop_cost", h, re.I)]
    ok("R1 raw: no shipped column holds a result", not bad, str(bad))
    ok("R1 raw: the bench log carries every batch, spike and drain", sum(1 for _ in open(os.path.join(tgt, PK.F["bench"]))) > 15000)
    # ---- the golden from the cut pack, and its rivals and hurried routes
    F, X = A.run_all(tgt)
    R, H = EP.rivals(F, X), EP.hurried(F, X)
    ok("R7 rivals: every rival's VR90 plan yield inside its band", all(inside(100 * v["y_plan"], B["R7"]["plan"]) for v in R.values()),
       str([round(100 * v["y_plan"], 2) for v in R.values()]))
    ok("SF9 R7 rivals: every rival's VR90 yield with every cause fixed inside its band (the cluster fit read three ways)",
       all(inside(100 * v["y_fixed"], B["R6"]) for v in R.values()))
    ok("SF5 R7 rivals: VR90 split evenly on CM1 and CM3 inside every band",
       inside(R["VR90 split evenly between CM1 and CM3"]["cost"]["loop"], B["R2"]["VR90"]) and
       inside(100 * R["VR90 split evenly between CM1 and CM3"]["y_plan"], B["R7"]["plan"]))
    g0 = X["vr"]
    ok("SF3 each fix alone is read on the plan: the four gains sum to less than the plan-to-fixed gap (they do not add)",
       sum(g0["cost"].values()) < 100 * (g0["y_fixed"] - g0["y_plan"]), "%.2f against %.2f" % (sum(g0["cost"].values()), 100 * (g0["y_fixed"] - g0["y_plan"])))
    late = A.vr90_etch(X["pk"], X["ec"], g0["no_flake"] + 150, 0.21)["p"]
    ok("SF4 a clean 150 wafers past the flaking point keeps VR90's fixed yield inside its band",
       inside(100 * g0["y_fixed"] * (1 - late), B["R6"]), "%.2f" % (100 * g0["y_fixed"] * (1 - late)))
    import subprocess as _sp
    plan_txt = " ".join(_sp.run(["pdftotext", os.path.join(tgt, PK.F["plan"]), "-"], capture_output=True, text=True).stdout.split())
    ok("SF6 the plan files the bench loading", "31 lots a day" in plan_txt)
    ok("SF7 the plan files CM3's return to R7 before VR90's first ILD0 lot", "fleet standard R7" in plan_txt and "23 November 2026" in plan_txt)
    ok("SF8 the plan files the back-end yields", "99.2 per cent" in plan_txt and "98.1 per cent" in plan_txt)
    for c, rid in (("loop", "R2"), ("bath", "R3"), ("edge", "R4"), ("etch", "R5")):
        ok("R7 rivals: every rival's VR90 gain from the %s fix inside its band" % c,
           all(inside(v["cost"][c], B[rid]["VR90"]) for v in R.values()))
    ok("SF1 R7 rivals: the first-insertion reading of the shortfall inside its band",
       all(inside(F["R1_first"][p], B["R1"][p]) for p in ("VX40", "VP12")), str(F["R1_first"]))
    ok("SF2 R7 rivals: the die-killed reading of each VX40 cost inside its band",
       inside(F["R2"]["excess_vx40"], B["R2"]["VX40"]) and inside(F["R3"]["raw_vx40"], B["R3"]["VX40"]) and
       inside(F["R4"]["raw_vx40"], B["R4"]["VX40"]) and inside(F["R5"]["raw_vx40"], B["R5"]["VX40"]))
    # golden figures inside their own bands, mid-band
    g = fg
    for rid, key in (("R2", "R2_loop"), ("R3", "R3_bath"), ("R4", "R4_edge"), ("R5", "R5_etch")):
        for cell in ("VX40", "VR90"):
            ok("band: %s %s golden inside its band" % (rid, cell), inside(g[key][cell], B[rid][cell]), "%s in %s" % (g[key][cell], B[rid][cell]))
    ok("band: R6 golden inside", inside(g["R6_fixed"], B["R6"]))
    ok("R6 rival ruled out: four VX40 die tiled from January to March sit above VR90's fixed band (VX40's own polish, "
       "loading, polisher share and edge die)", fg["vr90_tile_fixed"] > B["R6"][1], "%s against %s" % (fg["vr90_tile_fixed"], B["R6"]))
    ok("R6 composition: the stated parts multiply to the fixed yield", abs(fg["vr90_random_yield_pct"] * fg["vr90_fixed_parts"]["scratch"]
       * fg["vr90_fixed_parts"]["gate_oxide"] * fg["vr90_fixed_parts"]["edge_die"] / 1e6 * 0.981 - fg["R6_fixed"]) < 0.25)
    ok("band: R7 plan golden inside", inside(g["R7_plan"]["plan"], B["R7"]["plan"]))
    ok("band: R7 starts golden inside", inside(g["R7_plan"]["starts"], B["R7"]["starts"]))
    ok("band: R5 interval golden inside", inside(g["R5_etch"]["interval"], B["R5"]["interval"]))
    # the ranking is determinate: the four VX40 bands do not overlap
    order = sorted((B[r]["VX40"] for r in ("R2", "R3", "R4", "R5")), key=lambda b: b[0])
    ok("SF10 band: the causes' VX40 bands do not overlap (the ranking is forced)", all(order[i][1] < order[i + 1][0] for i in range(3)), str(order))
    # ---- R3: each hurried figure outside its band by a margin
    sh = fg["shortcut"]
    ok("R3 hurried: the far polishers' consumables reading leaves VR90's loop gain outside", sh["uniform_loop_vr90"] < B["R2"]["VR90"][0] - 1.0,
       "%s against %s" % (sh["uniform_loop_vr90"], B["R2"]["VR90"]))
    ok("R3 hurried: the summer's loading leaves VR90's bath gain outside", sh["q3_bath_vr90"] < B["R3"]["VR90"][0] - 0.4,
       "%s against %s" % (sh["q3_bath_vr90"], B["R3"]["VR90"]))
    ok("R3 hurried: RF time alone leaves VR90's etch gain outside", sh["kappa1_vr90"] < B["R5"]["VR90"][0] - 1.0)
    ok("R3 hurried: RF time alone leaves the interval outside", sh["kappa1_interval"] > B["R5"]["interval"][1] + 150)
    ok("R3 hurried: CM3's harmonisation as the edge fix leaves VR90's edge gain outside", B["R4"]["VR90"][0] > 0.3)
    ok("R3 hurried: CM3 to R7 alone recovers far less than the thin excess", g["harmonise_alone_vx40"] < 0.4 * g["harmonise_claimed_vx40"])
    ok("R3 hurried: a cluster factor of 2 leaves VR90's fixed yield outside", sh["alpha2_fixed"] < B["R6"][0] - 0.8)
    ok("R3 hurried: Poisson leaves VR90's fixed yield outside", sh["poisson_fixed"] < B["R6"][0] - 2.0)
    ok("R3 hurried: the careful pass leaves VR90's plan yield outside", sh["careful_plan"] > B["R7"]["plan"][1] + 3.0)
    # ---- R2: mess neutrality (each item mishandled moves only what grades it)
    pk = X["pk"]
    import copy
    shifted = {k: (v[0], v[1] + __import__("datetime").timedelta(minutes=4), v[2]) if v[0] == "CM1" else v for k, v in pk.cmp.items()}
    pk2 = copy.copy(pk)
    pk2.cmp = shifted
    sc2 = A.scratch_cause(pk2)
    ok("R2 mess: CM1's clock left uncorrected moves VR90's loop gain by under 0.2 points",
       abs(A.vr90_build(pk2, sc2, X["bc"], X["ec"], X["eg"], None, blocks=X["vr"]["blocks"])["cost"]["loop"] - X["vr"]["cost"]["loop"]) < 0.2)
    ok("R2 mess: first insertions move only the shortfall (the assembly result that grades them), inside its band",
       all(inside(F["R1_first"][p], B["R1"][p]) for p in ("VX40", "VP12")), str({p: round(F["R1_first"][p], 2) for p in F["R1_first"]}))
    ok("R2 mess: the bench log's restart repeats are dropped (no duplicate tool and seq)",
       len({(e["tool"], e["seq"]) for b in pk.bench.values() for e in b}) == sum(len(b) for b in pk.bench.values()))
    # ---- R5: no one thing; each factor runs across the data
    br = fg["bin5_by_polisher"]
    ok("R5 footprint: the loop's summer excess shows on every polisher, graded by distance",
       all(br[t]["slow"] > br[t]["spring"] for t in br) and (br["CM2"]["slow"] - br["CM2"]["spring"]) < (br["CM4"]["slow"] - br["CM4"]["spring"])
       < (br["CM1"]["slow"] - br["CM1"]["spring"]) < (br["CM3"]["slow"] - br["CM3"]["spring"]))
    cls = F["R4"]["cls"]["VX40"]
    ok("R5 footprint: the thick edge shows on DP2B wafers off CM3 and the thin edge on others' wafers on CM3, in both products",
       cls["thick"]["b3"] > 20 and cls["thin"]["b4"] > 15 and F["R4"]["cls"]["VP12"]["thick"]["b3"] > 20)
    ok("R5 footprint: the pair's wafers carry no edge excess", abs(cls["pair"]["b3"]) < 2 and abs(cls["pair"]["b4"]) < 2)
    lb = X["bc"]["lot_bath"]
    vx_lots = [l for l in lb if l.startswith("VXA")]
    ok("R5 footprint: the bath runs above its threshold on many lots before July too",
       sum(1 for l in vx_lots if lb[l][0] > X["bc"]["goi"]["c_th"] and lb[l][2].month < 7) >= 5)
    ok("R5 one thing: the careful pass with the loop alone corrected still loses five of the seven results",
       sum(1 for r in E["results"] if r["passes"]["careful"] != r["golden"]) >= 5)
    # ---- R6: the hints rescue only what they list
    ok("R6 hints: the largest single hint rescues one of seven", max(len(h["rescues"]) for h in E["hints"]) <= 2)
    # ---- R4: no plant, and the realism sweep
    lots = sorted({int(l[3:]) for l in lb if l.startswith("VXA")})
    steps = np.diff(lots)
    ok("realism: lot numbers are not an arithmetic sequence", len(set(steps.tolist())) > 2, str(sorted(set(steps.tolist()))[:6]))
    goods = [r[0] for r in con.execute("SELECT good FROM sort_wafer WHERE product='VX40' LIMIT 3000")]
    ok("realism: no repeated block of good-die counts", len(set(goods)) > 120)
    ok("realism: no round headline figure", g["R6_fixed"] not in (60.0, 65.0, 70.0) and g["R7_plan"]["plan"] not in (40.0, 45.0, 50.0))
    import subprocess
    meta = subprocess.run(["pdfinfo", os.path.join(tgt, PK.F["plan"])], capture_output=True, text=True).stdout
    ok("realism: the plan PDF is a Writer export", "Writer" in meta and "LibreOffice" in meta, meta.split("Producer:")[-1].split("\n")[0].strip())
    # ---- distractors: deleting them changes nothing the golden reads
    read = open(os.path.join(HERE, "analysis.py")).read()
    ok("distractors: the golden reads none of them", not any(d in read for d in PK.DISTRACTORS))
    # ---- the golden zip holds exactly the requested files
    with zipfile.ZipFile(os.path.join(out, "task9_golden.zip")) as z:
        ok("golden zip: exactly a spreadsheet and a note", sorted(z.namelist()) == sorted(["vr90_ramp_yield_note.docx", "vr90_ramp_yield_review.xlsx"]))
    sub = open(os.path.join(out, "submission.md")).read()
    ok("write-up: no em dash", "—" not in sub and "–" not in sub)
    ok("write-up: four blocks and tags", all(h in sub for h in ("## Tags", "## Final Recommendation", "## Supplementary Questions",
                                                               "## Critical Components", "## Step-by-Step")))
    fails = [r for r in RES if not r[1]]
    for label, good, detail in RES:
        print("%s  %s  %s" % ("PASS" if good else "FAIL", label, detail))
    print("%d assertions, %d failed" % (len(RES), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
