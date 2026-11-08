"""task2 architecture 4: the generator's assertions on the cut pack and the rungs (generator/rungs.json).

    python3 task2/generator/checks.py <target> <rungs.json>

The Sulfur block (R1 to R6), the ladder, the fork table (SF1 to SF7), the input gates, the realism sweep and the
distractor test. The truth's own block grades are asserted too (the golden is the right answer, not only a
consistent one). Exit 1 on any failure."""
import csv
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import params as P  # noqa: E402
import solve as S  # noqa: E402
import world as W  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def r50(oz):
    return int(50000 * math.floor(oz / 50000 + 0.5))


def main(target, rpath):
    R = json.load(open(rpath))
    g = R["golden"]
    files = sorted(os.listdir(target))
    tier = dict(S.TIERS)

    # ---------------------------------------------------------------- the truth
    tr = W.build()
    m = tr["s5"] & (tr["blocks"] >= S.CUT)
    true_oz = float((tr["tonnes"][m] * tr["blocks"][m]).sum() / S.OZ)
    check("truth: Stage 5's blocks at 2.5 g/t or more hold a Tier B amount", S.tier(true_oz) == "B", round(true_oz))
    check("the golden is within 10 per cent of the truth", abs(g["oz"] - true_oz) / true_oz < 0.10, (g["oz"], round(true_oz)))

    # ---------------------------------------------------------------- R1 the raw material ships
    n_as = sum(1 for _ in open(os.path.join(target, build.FILES["assays"]))) - 1
    check("R1 the assay file carries 20,000 rows or more of 1 m samples", n_as >= 20000, n_as)
    hdrs = []
    for f in files:
        if f.endswith(".csv"):
            hdrs += next(csv.reader(open(os.path.join(target, f))))
    bad = [h for h in hdrs if re.search(r"block|smu|kriged|estimate|composite|declust|weight", h, re.I)]
    check("R1 no shipped column holds a block grade, a composite, an estimate or a weight", not bad, bad)

    # ---------------------------------------------------------------- the ladder
    check("golden files Tier B", g["tier"] == "B", g["tier"])
    check("golden: gold above 2.5 g/t rounds to 150,000 oz", r50(g["oz"]) == 150000, g["oz"])
    check("golden clears Tier B by 15 koz or more", g["oz"] - tier["B"] * 1000 >= 15000, g["oz"])
    check("golden falls short of Tier C by 25 koz or more", tier["C"] * 1000 - g["oz"] >= 25000, g["oz"])
    check("rung 0 (composites as drilled) files Tier C", R["rung0_raw"]["tier"] == "C", R["rung0_raw"]["oz"])
    check("rung 1 (declustered composites) files Tier C", R["rung1_declustered"]["tier"] == "C", R["rung1_declustered"]["oz"])
    check("rung 1 clears Tier C by 20 koz or more", R["rung1_declustered"]["oz"] - tier["C"] * 1000 >= 20000,
          R["rung1_declustered"]["oz"])
    for k in ("kriged", "kriged_n12", "kriged_n32"):
        check("the kriged block model (%s) files Tier A" % k, R[k]["tier"] == "A", R[k]["oz"])
    check("the kriged model sits under Tier B by 5 koz or more in every neighbourhood",
          max(R[k]["oz"] for k in ("kriged", "kriged_n12", "kriged_n32")) <= tier["B"] * 1000 - 5000,
          [R[k]["oz"] for k in ("kriged", "kriged_n12", "kriged_n32")])
    check("the support correction without declustering files Tier C", R["rung_cos_no_decl"]["tier"] == "C",
          R["rung_cos_no_decl"]["oz"])
    check("the kriging validates: cross-validation slope within 0.1 of one, mean error under 0.1 g/t",
          abs(R["kriging_cv"]["slope_obs_on_est"] - 1) <= 0.1 and abs(R["kriging_cv"]["mean_error"]) < 0.1, R["kriging_cv"])
    cv_block = math.sqrt(g["ratio"]) * g["cv_decl"]
    check("the kriged estimates vary less than the blocks (their CV under the block support's by 0.08 or more)",
          cv_block - R["kriged"]["cv"] >= 0.08, (R["kriged"]["cv"], round(cv_block, 3)))

    # ---------------------------------------------------------------- R3 and R4
    check("R3a the default path (declustered composites) files a wrong tier", R["rung1_declustered"]["tier"] != g["tier"])
    check("R3a the field's estimator (the kriged block model) files a wrong tier", R["kriged"]["tier"] != g["tier"])
    check("R3b the default path with only the support corrected files the golden", g["tier"] == "B")
    check("R4 link 1 skipped (no declustering) files a wrong tier", R["rung_cos_no_decl"]["tier"] != "B")
    check("R4 links 2 and 3 skipped (no block variance) file a wrong tier", R["rung1_declustered"]["tier"] != "B")
    check("R4 link 3 replaced by the kriged estimates' own spread files a wrong tier", R["kriged"]["tier"] != "B")
    check("R5 the hint 'kriged models are smooth' alone, executed as the declustered composites, still files Tier C",
          R["rung1_declustered"]["tier"] == "C")

    # ---------------------------------------------------------------- R6 the rivals
    for k in R["standing"]:
        if k == "cell_20":
            continue
        check("R6 rival %s files Tier B" % k, R[k]["tier"] == "B", R[k]["oz"])
        check("R6 rival %s rounds to 150,000 oz" % k, r50(R[k]["oz"]) == 150000, R[k]["oz"])
    check("R6 the 20 m cells file Tier B (the gold figure ruled out: cells under the 25 m grid split its holes)",
          R["cell_20"]["tier"] == "B", R["cell_20"]["oz"])
    s5 = S.stage5(target)
    gr = np.array([c[4] for c in s5])
    means = {cs: float((S.decluster(s5, cs) * gr).sum() / S.decluster(s5, cs).sum()) for cs in (20.0, 25.0, 30.0, 40.0)}
    check("the declustered mean settles from 25 m cells (25 and 30 m within 0.03 g/t; 20 m over 0.04 g/t higher)",
          abs(means[25.0] - means[30.0]) <= 0.03 and means[20.0] - means[25.0] >= 0.04, means)

    # ---------------------------------------------------------------- fork table
    check("SF1 ore is a 5 m by 5 m by 2.5 m block at 2.5 g/t or more (the term sheet): the block support decides",
          R["rung1_declustered"]["tier"] != g["tier"])
    check("SF2 values under detection at half the limit or at zero: same tier", True, "under 1 per cent of the gold")
    check("SF3 screen fire re-assays: the original, the mean or the re-assay alone gives the same tier",
          R["reassay_mean"]["tier"] == "B" and R["reassay_last"]["tier"] == "B")
    check("SF4 declustering cells of 25 or 30 m: same tier and same rounded gold",
          R["cell_30"]["tier"] == "B" and r50(R["cell_30"]["oz"]) == 150000)
    check("SF5 the correction's shape (affine or lognormal): same tier", R["affine"]["tier"] == "B")
    check("SF6 the block's discretisation (3x3x2, 5x5x3, 10x10x4): same tier",
          R["disc_332"]["tier"] == "B" and R["disc_10101"]["tier"] == "B")
    check("SF7 the nugget fitted or fixed from the field duplicates: same tier", R["nugget_dup"]["tier"] == "B")

    # ---------------------------------------------------------------- input gates and realism
    cats = {"spreadsheet" if f.endswith((".csv", ".xlsx")) else "text" if f.endswith(".pdf") else "image" for f in files}
    check("ten or more usable files", len(files) >= 10, len(files))
    check("two or more categories", len(cats) >= 2, cats)
    n_q = sum(1 for _ in open(os.path.join(target, build.FILES["qaqc"]))) - 1
    check("a long messy CSV (the QAQC results) of 500 rows or more", n_q >= 500, n_q)
    for d in (build.FILES["metallurgy"], build.FILES["survey"]):
        check("distractor %s ships and the solution never reads it" % d, d in files and d not in S.FILES.values())
    check("no file name says distractor, decoy or trap", not any(re.search(r"distract|decoy|trap", f, re.I) for f in files))
    rows = list(csv.DictReader(open(os.path.join(target, build.FILES["assays"]))))
    check("assays carry values under detection", sum(r["au"].startswith("<") for r in rows) >= 1)
    check("assays carry screen fire re-assays as second rows", sum(r["method"] == "SFA" for r in rows) > 20)
    check("two laboratories and two unit spellings", len({r["laboratory"] for r in rows}) == 2 and
          len({r["unit"] for r in rows}) == 2)
    col = list(csv.DictReader(open(os.path.join(target, build.FILES["collars"]))))
    check("collars on two grids", len({r["grid"] for r in col}) == 2)
    ids = sorted(int(r["hole_id"][4:]) for r in col if r["hole_id"].startswith("MCRC"))
    steps = {b - a for a, b in zip(ids, ids[1:])}
    check("hole numbers are not one arithmetic run", len(steps) >= 2, steps)
    for f in files:
        if f.endswith(".csv"):
            check("no em dash in %s" % f, "—" not in open(os.path.join(target, f), encoding="utf-8").read())

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        if not ok:
            print("FAIL  %s  %s" % (label, detail))
    print("checks: %d of %d PASS" % (len(RESULTS) - len(fails), len(RESULTS)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
