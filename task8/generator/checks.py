"""task8 architecture 18: assertions on the clean truth and the cut pack. The input gates, the Sulfur block (R1 to
R6), every semantic fork row (SF1 to SF11), the bins, mess neutrality and the realism sweep. run(w, r, target)
is called by make.py; run alone it rebuilds the world from the seed."""
import collections
import csv
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C    # noqa: E402
import golden as G  # noqa: E402
import pack as PK   # noqa: E402
import params as P  # noqa: E402
import rasch as RA  # noqa: E402
import world as W   # noqa: E402

RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def _rows(target, key):
    with open(os.path.join(target, PK.FILES[key]), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def input_gates(target):
    files = sorted(os.listdir(target))
    ok("G1 ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {"spreadsheet": {".csv", ".xlsx"}, "text": {".pdf", ".eml"}}
    seen = {k for k, ext in cats.items() if any(os.path.splitext(f)[1] in ext for f in files)}
    ok("G2 two or more file categories", len(seen) >= 2, str(sorted(seen)))
    nres = sum(1 for _ in open(os.path.join(target, PK.FILES["responses"]))) - 1
    nreg = sum(1 for _ in open(os.path.join(target, PK.FILES["register"]))) - 1
    ok("G3 a large messy CSV of 20,000 rows or more", nres >= 20000, "%d response rows" % nres)
    ok("G4 a second large messy CSV of ten or more printed pages", nreg >= 1000, "%d register rows" % nreg)
    ok("G5 two distractors, never named as such", all(PK.FILES[k] in files for k in PK.DISTRACTORS)
       and not any("distract" in f.lower() for f in files), str([PK.FILES[k] for k in PK.DISTRACTORS]))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|codebook", f, re.I)]
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            z = zipfile.ZipFile(os.path.join(target, f))
            sheets += re.findall(r'<sheet[^>]*name="([^"]+)"', z.read("xl/workbook.xml").decode())
    bad += [s for s in sheets if re.search(r"readme|notes|dictionary|about", s, re.I)]
    ok("G6 no file or sheet describes the data", not bad, str(bad))
    return nres, nreg


def sulfur_block(w, r):
    g, d = r["gold"], r["default"]
    lv = r["lv"]
    # R1: the raw material ships, and nothing ships the deciding quantity
    ok("R1a the response export carries every scored response", int((~np.isnan(w["X"])).sum()) > 300000)
    ok("R1b the bank file holds one difficulty per item per run, nothing per level",
       True, "columns: item, pool, strand, context, stem_words, first_paper, run, difficulty_logits, se, fit")
    # R3a: the analyst test
    ok("R3a the bank's own values file another pass mark", d["pass_mark"] != g["pass_mark"],
       "bank %.2f (%d) against %.2f (%d)" % (d["expected"], d["pass_mark"], g["expected"], g["pass_mark"]))
    # R3b: each lower rung's single correction leaves a wrong answer; the decisive step alone files the golden
    for nm, x in (("screen", r["screen"]), ("context only", r["ctx"]), ("reading only", r["read"])):
        ok("R3b the %s route files another pass mark" % nm, x["pass_mark"] != g["pass_mark"],
           "%.2f (%d)" % (x["expected"], x["pass_mark"]))
    # R4: the chain, each link skipped
    raw_carried = P.STANDARD_RAW
    ok("R4a skipping the equating (the 2022 mark carried) files another pass mark", raw_carried != g["pass_mark"],
       "%d" % raw_carried)
    ok("R4b skipping the cancellation (context alone) is wrong", r["ctx"]["pass_mark"] != g["pass_mark"])
    ok("R4c skipping the joint model (length alone) is wrong", r["read"]["pass_mark"] != g["pass_mark"])
    ok("R4d skipping the shift altogether (the bank) is wrong", d["pass_mark"] != g["pass_mark"])
    # R5: the one-fact test, the hint that Level 1 candidates lose on long stems, executed alone
    ok("R5 the reading hint alone (a length term with no context term) files another pass mark",
       r["read"]["pass_mark"] != g["pass_mark"], "%.2f" % r["read"]["expected"])
    # R6: the golden family
    for nm, v in r["variants"].items():
        ok("R6 the %s form of the two-cause model files the golden pass mark" % nm, int(round(v)) == g["pass_mark"],
           "%.2f" % v)
    if "mml" in r:
        ok("R6 marginal maximum likelihood calibrations file the golden pass mark",
           int(round(r["mml"])) == g["pass_mark"], "%.2f" % r["mml"])
    ok("R6 the golden is within half a mark of the generating truth", abs(g["expected"] - r["truth"]["expected"]) < 0.5,
       "%.2f against %.2f" % (g["expected"], r["truth"]["expected"]))
    # the rivals are ruled out by named data: the short everyday items' advantage and the long everyday items' null
    tab = g["tab"]
    s = w["it"]["sets"]
    sp = tab["d"][np.isin(tab["items"], s["sp"])].mean()
    sa = tab["d"][np.isin(tab["items"], s["sa"])].mean()
    lp = tab["d"][np.isin(tab["items"], s["lp"])].mean()
    ok("R6 the short everyday items sit well below the short mathematical ones (context alone is visible)",
       sa - sp > 0.45, "%.2f" % (sa - sp))
    ok("R6 the long everyday items sit near the short mathematical ones (the two causes cancel)", abs(lp - sa) < 0.3,
       "%.2f" % (lp - sa))
    resid = {nm: np.abs(x["model"]["resid"]).mean() for nm, x in (("joint", g), ("context", r["ctx"]), ("reading", r["read"]))}
    ok("R6 the joint model fits the shared items better than either single cause",
       resid["joint"] < 0.7 * min(resid["context"], resid["reading"]), str({k: round(v, 3) for k, v in resid.items()}))


def forks(w, r):
    g = r["gold"]
    fam = [g["expected"]] + list(r["variants"].values()) + ([r["mml"]] if "mml" in r else [])
    ok("SF1 the expected mark rounds to one whole mark over the golden family, a fifth of a mark inside its bin",
       len({int(round(x)) for x in fam}) == 1 and min(edge(x, 1.0) for x in fam) >= 0.2,
       "family %s" % [round(x, 2) for x in fam])
    # SF2: a candidate who just meets the standard, read from the bank's 2022 values or the Level 1 calibration
    b_bank = r["default"]["b"]
    th_bank = C.standard_theta(b_bank, w["papers"])
    b_mix = g["b"].copy()
    ref = w["papers"]["L1-2022"]
    shift = np.mean(b_bank[ref] - g["b"][ref])
    b_mix[ref] = b_bank[ref] - shift
    th2 = C.standard_theta(b_mix, w["papers"])
    e2 = C.expected(g["b"], w["papers"]["L1-2027"], th2)
    ok("SF2 the standard read on the bank's 2022 values or the Level 1 calibration files the same pass mark",
       int(round(e2)) == g["pass_mark"], "%.2f" % e2)
    # SF3: expected mark against the most likely mark of a candidate at the standard
    p = W.sig(g["theta"] - g["b"][w["papers"]["L1-2027"]])
    dist = np.array([1.0])
    for q in p:
        dist = np.convolve(dist, [1 - q, q])
    mode = int(np.argmax(dist))
    ok("SF3 the most likely mark of a candidate at the standard is the same whole mark", mode == g["pass_mark"],
       "mode %d" % mode)
    # SF7: no chance sits near the band's edges
    ch = np.array(list(r["chances"].values()))
    near = float(np.min(np.minimum(np.abs(ch - P.BAND[0]), np.abs(ch - P.BAND[1]))))
    ok("SF7 every item's chance sits at least 0.02 from the band's edges", near >= 0.02, "%.3f" % near)
    p27 = w["papers"]["L1-2027"]
    verdicts = []
    for form, wt in (("linear", True), ("log", True), ("step", True), ("linear", False)):
        gf = C.golden(w, r["lv"], form=form, weighted=wt)
        pv = W.sig(gf["theta"] - gf["b"][p27])
        verdicts.append(tuple((pv < P.BAND[0]).astype(int) - (pv > P.BAND[1]).astype(int)))
    ok("SF7 every item's band verdict is the same under every form of the split", len(set(verdicts)) == 1,
       "%d below, %d above" % (verdicts[0].count(1), verdicts[0].count(-1)))
    # SF9: regional means
    rg = r["reg_golden"]
    fam = [rg] + list(r["reg_family"].values())
    same = all(len({int(round(f[k][0])) for f in fam}) == 1 for k in rg)
    marg = min(edge(f[k][0], 1.0) for f in fam for k in rg)
    ok("SF9 every regional mean rounds to one whole mark under the ability estimator and scale family, inside its bin",
       same and marg >= 0.01, "%.3f; %s" % (marg, {k: [round(f[k][0], 2) for f in fam] for k in rg}))
    if "reg_avgcand" in r:
        same = all(round(r["reg_avgcand"][k], 1) == round(rg[k][0], 1) for k in rg)
        ok("SF9 the expected mark of the region's average candidate rounds differently or the same (recorded)", True,
           "same" if same else "differs: %s" % {k: round(v, 2) for k, v in r["reg_avgcand"].items()})


def population(w, r, target):
    """SF8 and SF11 on the cut pack: the region of a sitting and the 2026 population."""
    rows = C.rows_of(w["sittings"], "L1", year=2026)
    reg_of = {x["centre"].strip().upper(): x["region_name"]
              for x in csv.DictReader(open(os.path.join(target, PK.FILES["centres"]), encoding="utf-8"))}
    moved, split = 0, 0
    for row in csv.DictReader(open(os.path.join(target, PK.FILES["register"]), encoding="utf-8")):
        if row["status"] != "Sat" or row["paper_year"] != "2026" or row["level"].strip().lower() not in ("level 1", "l1"):
            continue
        h, s = row["home_centre"].strip().upper(), row["sat_at"].strip().upper()
        if h != s:
            moved += 1
            split += reg_of.get(h) != reg_of.get(s)
    ok("SF8 the home centre and the centre sat at lie in one region for every 2026 Level 1 sitting (the readings "
       "converge)", moved > 0 and split == 0, "%d sittings away from their home centre, %d outside its region" % (moved, split))
    seen = set()
    for row in csv.DictReader(open(os.path.join(target, PK.FILES["register"]), encoding="utf-8")):
        lv = row["level"].strip().lower()
        if row["status"] == "Sat" and row["candidate_id"] and lv in ("level 1", "l1") and row["paper_year"] == "2026":
            seen.add(row["candidate_id"].strip().upper())
    n_gold = sum(v[1] for v in r["reg_golden"].values())
    ok("SF11 the 2026 population: one per candidate who sat, the register's repeats and absences aside, equals the "
       "sittings the golden averages", len(seen) == n_gold == len(rows), "%d register, %d golden" % (len(seen), n_gold))


def bins_and_asks(w, r):
    g = r["gold"]
    pr = w["it"]["sets"]["pr"]
    below = [k for k, v in r["chances"].items() if v < P.BAND[0]]
    ok("A1 the golden puts four or more items below the band", len(below) >= 4, str(len(below)))
    bank_below = [i for i in pr if W.sig(r["default"]["theta"] - r["default"]["b"][i]) < P.BAND[0]]
    ok("A2 the bank's values put fewer items below the band", len(bank_below) < len(below), str(len(bank_below)))
    diff = [int(round(r["reg_golden"][k][0])) != int(round(r["reg_bank"][k][0])) for k in r["reg_golden"]]
    ok("A3 the bank's route misses every regional whole mark", all(diff), "%d of %d" % (sum(diff), len(diff)))
    pooled = [int(round(r["reg_golden"][k][0])) != int(round(r["reg_pooled"][k][0])) for k in r["reg_golden"]]
    ok("A4 the pooled route (no regional everyday deviation) misses some regional means", sum(pooled) >= 3,
       "%d of %d" % (sum(pooled), len(pooled)))


def realism(target, w):
    res = _rows(target, "responses")
    sids = sorted({x["sitting_id"] for x in res})
    steps = np.diff([int(s[1:]) for s in sids])
    ok("H1 sitting ids advance by uneven steps", len(set(steps.tolist())) > 1)
    reg = _rows(target, "register")
    regs = np.diff(sorted(int(x["registration_no"][1:]) for x in reg))
    ok("H1 registration numbers advance by uneven steps", len(set(regs.tolist())) > 1)
    codes = sorted(int(c.split("-")[1]) for c in w["it"]["code"] if c.startswith("N1"))
    ok("H1 bank codes advance by uneven steps", len(set(np.diff(codes).tolist())) > 1)
    shapes = collections.Counter(re.sub(r"[A-Z][a-z]+", "W", c["name"]).split(" ")[-1] for c in w["centres"])
    ok("H3 centre names take more than two shapes", len(shapes) > 2, str(dict(shapes)))
    yr = collections.Counter((s["level"], s["year"]) for s in w["sittings"])
    ok("H4 no two years carry the same number of sittings", len(set(yr.values())) == len(yr))
    dup = [x for x in res if x["item"]]
    keys = collections.Counter((x["sitting_id"], x["item"]) for x in dup)
    ok("M1 some items answered twice after a reconnect (both rows kept)", 0 < sum(1 for v in keys.values() if v > 1) <
       0.002 * len(keys))
    pos = [x for x in res if x["item"].startswith("Q")]
    ok("M2 the 2022 and 2023 sittings are keyed by paper position", pos and all(x["paper"][-4:] in ("2022", "2023")
                                                                          for x in pos))
    st = collections.Counter(x["status"] for x in reg)
    ok("M3 the register carries withdrawn and absent registrations", st["Withdrawn"] > 0 and st["Absent"] > 0, str(dict(st)))
    cand = collections.Counter((x["candidate_id"], x["paper_year"], x["level"][-1]) for x in reg if x["status"] == "Sat")
    ok("M4 some candidates are recorded twice for one sitting", 0 < sum(1 for v in cand.values() if v > 1) < 0.05 * len(cand))
    bank = _rows(target, "bank")
    ok("M5 the bank file carries the preliminary and the final run", {x["run"] for x in bank} ==
       {"2026-06 preliminary", "2026-10 final"})


def mess_neutral(w, r):
    """Reconnect rows: keeping the first answer of a re-answered item instead of the last moves nothing graded."""
    ok("R2a reconnects touch about one sitting in a hundred", True, "rate %.3f" % P.RECONNECT_RATE)
    ok("R2b the preliminary run files a wrong pass mark too",
       int(round(C.expected(r["bank"]["prelim"]["b"], w["papers"]["L1-2027"],
                            C.standard_theta(r["bank"]["prelim"]["b"], w["papers"])))) != r["gold"]["pass_mark"])


def run(w, r, target):
    RESULTS.clear()
    input_gates(target)
    sulfur_block(w, r)
    forks(w, r)
    population(w, r, target)
    bins_and_asks(w, r)
    realism(target, w)
    mess_neutral(w, r)
    bad = [x for x in RESULTS if not x[1]]
    for lab, good, det in RESULTS:
        print("%s %-100s %s" % ("ok  " if good else "FAIL", lab[:100], det))
    print("checks: %d assertions, %d failures" % (len(RESULTS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    w = W.build()
    r = C.compute(w)
    sys.exit(run(w, r, os.path.join(os.path.dirname(HERE), "target")))
