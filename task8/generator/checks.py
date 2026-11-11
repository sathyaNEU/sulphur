"""task8: the generator's assertions on the cut pack (python3 checks.py): the input gates, the assembly against the
simulator's record, every semantic fork row, the bar block (rivals, hurried figures outside their bands, the
level-5 mark, the one-fact test), the forcing line, the hidden factors' footprints, realism, the distractor
deletion test and agreement with the simulator's clean truth. Exit 1 on any failure."""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD  # noqa: E402
import load  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402
import routes as RT  # noqa: E402
import world  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
OUT = []


def check(label, ok, detail=""):
    OUT.append((label, bool(ok), str(detail)))


def pdf_text(path):
    return " ".join(subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.split())


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    files = sorted(f for f in os.listdir(TARGET) if not f.startswith("."))
    # ---------------------------------------------------------------- input gates
    check("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    check("gate: two or more file categories", {"csv", "xlsx", "pdf"} <= {f.rsplit(".", 1)[1] for f in files})
    rows = {f: sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    check("gate: a CSV of 20,000 rows or more (the Quill session log)", rows[PK.FILES["quilllog"]] >= 20000,
          rows[PK.FILES["quilllog"]])
    check("gate: a messy CSV of ten printed pages or more (KS2, codes and repeated rows)", rows[PK.FILES["ks2"]] >= 500,
          rows[PK.FILES["ks2"]])
    check("gate: two or more distractors, unlabelled", len(PK.DISTRACTORS) >= 2 and not any(
        re.search(r"distract|unused|decoy", f, re.I) for f in files))
    check("gate: no file describes the data", not any(re.search(r"readme|dictionary|manifest|field.?notes|schema|notes",
                                                                f, re.I) for f in files))
    check("gate: no file named after a mechanism", not any(re.search(r"gain|practice|order|dip|transition|norm|equat",
                                                                     f, re.I) for f in files))
    # ---------------------------------------------------------------- assembly against the simulator's record
    W = world.build()
    D = load.load(TARGET)
    on_roll = [s for s in W["students"] if not s["left"]]
    check("R1 assembly: every student on roll at the census is in the census extract", len(on_roll) == len(D["students"]),
          "%d against %d" % (len(on_roll), len(D["students"])))
    by_upn = {s["upn"]: s for s in D["students"]}
    miss, wrong = 0, 0
    for s in on_roll:
        d = by_upn[s["upn"]]
        true_first = None
        for x in sorted([x for x in W["sittings"] if x["student"] is s], key=lambda x: (x["date"], x["test"])):
            if x["status"] == "Complete" and (x["test"] != "QUILL" or x["items"] >= P.QUILL_MIN_ITEMS) and x["date"] <= P.CENSUS:
                true_first = x
                break
        f = R.first_valid(d)
        if (true_first is None) != (f is None):
            miss += 1
        elif f is not None and (f["test"] != true_first["test"] or f["sas"] != true_first["sas"] or
                                f["date"] != true_first["date"]):
            wrong += 1
    check("R1 assembly: the first valid sitting the golden reads is the record's for every student on roll",
          miss == 0 and wrong == 0, "%d missed, %d wrong" % (miss, wrong))
    left_rows = D["unmatched"]
    check("R1 assembly: the export rows that match no one on roll are the students who left before the census",
          sum(left_rows.values()) <= sum(1 for s in W["students"] if s["left"]) * 2, str(left_rows))
    # ---------------------------------------------------------------- the golden and its rivals
    G = GD.compute(TARGET)
    g = G["golden"]
    check("golden equals figures.json: programme by academy", all(int(g["R6"][a]) == F["programme"][a] for a in g["R6"]))
    check("golden equals figures.json: total and cost", g["R6_total"] == F["programme_total"] and
          int(round(g["R8_cost"])) == F["cost_total"])
    riv = G["rivals"]
    spread = {a: max(abs(riv[n]["R6"][a] - g["R6"][a]) for n in riv) for a in g["R6"]}
    check("R7 rivals: every rival within a few students of the golden at every academy (whole score groups)",
          max(spread.values()) <= 8 and sum(spread.values()) <= 24,
          "widest %d, total %d" % (max(spread.values()), sum(spread.values())))
    check("R7 rivals: every rival's trust total inside the total's band",
          all(G["bands"]["R6_total"][0] <= riv[n]["R6_total"] <= G["bands"]["R6_total"][1] for n in riv))
    # the hurried figures outside their bands
    car = G["routes"]["careful"]
    b = G["bands"]
    check("R3 hurried: the trial's pairs as they stand file a gain of 0 outside R2's band", not (b["R2"][0] <= car["R2"] <= b["R2"][1]))
    check("R3 hurried: the July sittings as they stand file a level of 0 outside R5's band", not (b["R5"][0] <= car["R5"] <= b["R5"][1]))
    out3 = [x for x in R.POINTS if not (b["R3"][x][0] <= car["R3"][x] <= b["R3"][x][1])]
    check("R3 hurried: the uncorrected trial link lands outside R3's band at most points", len(out3) >= 4, out3)
    nom = G["routes"]["the other tests' standardised scores read as Lexis scores"]
    out4 = [x for x in R.POINTS if not (b["R4"][x][0] <= nom["R4"][x] <= b["R4"][x][1])]
    check("R3 hurried: reading Quill as Lexis lands outside R4's band at every point above the scales' shared floor",
          len(out4) >= len(R.POINTS) - 1 and all(x in out4 for x in R.POINTS[1:]), out4)
    out4c = [x for x in R.POINTS if not (b["R4"][x][0] <= car["R4"][x] <= b["R4"][x][1])]
    check("R3 hurried: the careful pass's Quill link (KS2 to Lexis on every Lexis sitting) outside R4's band at most points",
          len(out4c) >= 4, out4c)
    bad = [a for a in g["R6"] if b["R6"][a][0] <= car["R6"][a] <= b["R6"][a][1]]
    share = {}
    for p in g["placements"]:
        a = p["s"]["academy"]
        share.setdefault(a, [0, 0])
        share[a][0] += p["basis"] in ("brightway", "july")
        share[a][1] += 1
    moved = {a for a, (k, n) in share.items() if k > 0.5 * n}
    check("R3 hurried: the careful pass misses the count at most Brightway and July academies",
          sum(1 for a in moved if a not in bad) >= len(moved) - 1, "inside at %s" % ", ".join(sorted(set(bad) & moved)))
    check("R3 hurried: the careful total sits outside the total's band", not (b["R6_total"][0] <= car["R6_total"] <= b["R6_total"][1]),
          "%d against %s" % (car["R6_total"], b["R6_total"]))
    for nm in RT.SINGLE:
        r = G["routes"][nm]
        check("R3 hurried: '%s' total outside the band" % nm, not (b["R6_total"][0] <= r["R6_total"] <= b["R6_total"][1]),
              r["R6_total"])
    # level 5: different shortcuts, different wrong answers
    answers = {json.dumps(r["R6"], sort_keys=True) for nm, r in G["routes"].items()}
    check("level 5: the shortcuts place students in four or more different ways", len(answers) >= 4, len(answers))
    worst = max(len(h["rescues"]) for h in E["hints"])
    check("one-fact test: no hint rescues more than a third of the results", worst <= 3, "%d of 9" % worst)
    check("one-fact test: no hint rescues the tutor time", not any("R8" in h["rescues"] for h in E["hints"]))
    # forcing: the provisional budget between the shortcuts and the golden family
    line = P.PROVISIONAL_BUDGET
    check("forcing: every rival's cost above the provisional budget", all(r["R8_cost"] > line for r in riv.values()))
    check("forcing: every shortcut's cost at or below the provisional budget",
          all(G["routes"][nm]["R8_cost"] <= line for nm in ["careful"] + list(RT.SINGLE)
              if nm != "Brightway through KS2 rather than the trial"),
          {nm: round(G["routes"][nm]["R8_cost"]) for nm in ["careful"] + list(RT.SINGLE)})
    check("forcing: every fitted input moved by its spread keeps the cost above the budget",
          all(p["value"] > line for p in G["perturbations"]), [p["students"] for p in G["perturbations"]])
    check("forcing: the provisional budget is last October's numbers at this year's rate",
          abs(P.LAST_OCTOBER * P.HOURS_PER_STUDENT * P.WEEKS * P.RATE - line) < 50)
    # ---------------------------------------------------------------- the factors run across the data
    gains = [x["student"]["gain"] for x in W["sittings"] if x["kind"] in ("trial_second", "second")]
    check("footprint: the second-sitting gain is on every second sitting, both tests, every Brightway academy",
          len({x["academy"] for x in W["sittings"] if x["kind"] in ("trial_second", "second")}) == 5 and
          any(x["kind"] == "second" for x in W["sittings"]))
    check("footprint: the July level is on every student's Year 6 reading (KS2 carries it too)",
          abs(np.mean([s["july"] for s in W["students"]]) - P.JULY_LEVEL) < 0.02)
    check("footprint: the Quill norm sample sits under every Quill result, at all seven Quill academies",
          len({a["name"] for a in W["academies"] if a["test"] == "QUILL"}) == 7)
    check("realism: the effects carry noise (no clean step)", np.std(gains) > 0.05)
    # ---------------------------------------------------------------- semantic forks
    pol = pdf_text(os.path.join(TARGET, PK.FILES["policy"]))
    for sf, phrase in [("SF1 on roll", "on roll at an academy of the trust at the October census"),
                       ("SF2 the Lexis basis", "on the Lexis 2019 standardisation"),
                       ("SF3 a whole score", "as a whole standardised score"),
                       ("SF4 first valid sitting", "first valid sitting of an entry reading test after the May 2026 KS2"),
                       ("SF5 Quill validity", "answered at least 24 questions"),
                       ("SF6 equal reading", "result counts at the whole Lexis score of equal reading at the start of Year 7"),
                       ("SF7 KS2 placement", "placed from their KS2 reading scaled"),
                       ("SF8 below 85", "entry reading is below 85"),
                       ("SF9 tutor time", "0.4 tutor hours a week for each Reading Forward student"),
                       ("SF10 the budget", "is £339,500"),
                       ("SF13 the Brightway link", "to put Brightway results on the Lexis basis")]:
        check("%s: filed once in the policy" % sf, pol.count(phrase) == 1, phrase)
    check("SF11 a moved student counts at the census academy on the first sitting",
          all(p["s"]["academy"] in D["academies"] for p in g["placements"]))
    late = [s for s in D["students"] if any(x["valid"] and x["date"] > P.CENSUS for x in s["sittings"])
            and not any(x["valid"] and x["date"] <= P.CENSUS for x in s["sittings"])]
    check("SF12 a sitting after the census is not by the census (placed on KS2)", all(
        R.entry(s, g["links"])[1] in ("ks2", "none") for s in late), "%d students" % len(late))
    # ---------------------------------------------------------------- truth
    truth = {}
    for s in on_roll:
        d = by_upn[s["upn"]]
        if R.first_valid(d) is None and d["ks2"] is None:
            continue
        t = s["test"]
        truth[t] = truth.get(t, 0) + s["p_below"]
    gold_t = {}
    for p in g["placements"]:
        gold_t[p["s"]["test"]] = gold_t.get(p["s"]["test"], 0) + int(p["placed"])
    for t, v in truth.items():
        k = {"LEXIS": "Lexis", "QUILL": "Quill", "BRIGHTWAY": "Brightway"}[t]
        check("truth: the %s academies' count within 6 per cent of the simulator's expectation" % k,
              abs(gold_t[k] - v) <= 0.06 * v + 6, "%d against %.1f" % (gold_t[k], v))
    check("truth: the trust total within 4 per cent of the simulator's expectation",
          abs(g["R6_total"] - sum(truth.values())) <= 0.04 * sum(truth.values()), "%d against %.1f" % (
              g["R6_total"], sum(truth.values())))
    check("truth: the gain and the July level near the process's own", abs(g["R2"] - 15 * P.SECOND_SITTING_GAIN) < 1.2
          and abs(g["R5"] - 15 * P.JULY_LEVEL) < 1.2, "%.2f, %.2f" % (g["R2"], g["R5"]))
    # ---------------------------------------------------------------- realism
    cen = list(csv.DictReader(open(os.path.join(TARGET, PK.FILES["census"]), encoding="utf-8")))
    adm = sorted(int(r["admission_no"]) for r in cen)
    check("realism: admission numbers are not a sequence", len(set(np.diff(adm))) > 3)
    check("realism: no sitting after the exports", all(x["date"] <= P.EXPORTED + __import__("datetime").timedelta(days=6)
                                                         for s in D["students"] for x in s["sittings"]))
    check("realism: academies differ in size", len({len([1 for r in cen if r["academy"] == a]) for a in D["academies"]}) > 15)
    check("realism: the cost is not a round figure", F["cost_total"] % 1000 != 0)
    # distractors: deleting each changes nothing the golden reads
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in [PK.FILES[k] for k in PK.DISTRACTORS]:
                shutil.copy(os.path.join(TARGET, f), tmp)
        D2 = load.load(tmp)
        g2 = R.all_results(D2, R.GOLD)
        check("distractors: the golden is the same with every distractor deleted", g2["R6"] == g["R6"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bad = [o for o in OUT if not o[1]]
    for label, ok, detail in OUT:
        print("%s  %-96s %s" % ("PASS" if ok else "FAIL", label[:96], detail[:70]))
    print("%d checks, %d FAIL" % (len(OUT), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
