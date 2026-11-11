"""task19 independent verifier: reads only the shipped files (target/, golden/) and figures.json, on its own code path
(csv, openpyxl, python-docx, pdftotext), and recomputes every figure that does not need the survey linked to the
register; the linked figures are checked against the clerical review's own direct estimate.

    python3 task19/generator/verify.py      exit 0 when every check passes
"""
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
F = json.load(open(os.path.join(HERE, "figures.json")))
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pc_key(s):
    s = "".join(ch for ch in s.upper() if ch.isalnum())
    return s[:-3] + " " + s[-3:] if len(s) >= 5 else s


def r10(x):
    return int(round(x / 10.0) * 10)


# ---------------------------------------------------------------- formats read back, with positive controls
pdf = [f for f in os.listdir(T) if f.endswith(".pdf")][0]
txt = subprocess.run(["pdftotext", "-layout", os.path.join(T, pdf), "-"], capture_output=True, text=True).stdout
txt1 = re.sub(r"\s+", " ", txt)
check("circular read back (positive control)", "Grant determination 2027/28" in txt1 and len(txt1) > 1500, "%d chars" % len(txt1))
check("circular files the line", "25,000 usual residents or more" in txt1)
check("circular files the half-rate rule", "includes 25,000" in txt1 and "half the supplement" in txt1)
check("circular files term-time students and serving personnel at base",
      "term-time address" in txt1 and "base where they are stationed" in txt1)

import openpyxl  # noqa: E402

wb = openpyxl.load_workbook(os.path.join(T, "KSO_population_accounts_2021-2026.xlsx"), read_only=True)
acc = [r for r in wb.worksheets[0].iter_rows(values_only=True) if r and isinstance(r[1], (int, float))]
check("accounts read back (positive control)", len(acc) == 5, "%d rows" % len(acc))
official = acc[-1][7]
check("rolled-forward figure", official == F["official_2026"], "%s against %s" % (official, F["official_2026"]))
imm_nn = sum(r[4] for r in acc)
border = rows("KBA_permit_holder_movements_2021-07_to_2026-06.csv")
arrivals = sum(1 for r in border if r["movement"] == "arrival")
check("arrivals missing from the accounts", arrivals - imm_nn == F["immigration_not_in_accounts"],
      "%d - %d against %d" % (arrivals, imm_nn, F["immigration_not_in_accounts"]))

# ---------------------------------------------------------------- the register placed by postcode
pcd = {pc_key(r["postcode"]): r["district_code"] for r in rows("KSO_postcode_directory_2026-06.csv")}
reg = rows("KHS_register_extract_2026-06-30.csv")
count = {}
unplaced = 0
for r in reg:
    d = pcd.get(pc_key(r["postcode"]))
    if d is None:
        unplaced += 1
        continue
    count[d] = count.get(d, 0) + 1
check("every register record placed by the directory", unplaced == 0, "%d unplaced" % unplaced)
for d, n in F["register_counts"].items():
    check("register count %s" % d, count.get(d) == n, "%s against %s" % (count.get(d), n))

# ---------------------------------------------------------------- the follow-up's parts, from its own outcomes
blocks = {r["block_id"]: r["district_code"] for r in rows("CS26_blocks.csv")}
fu = rows("CS26_register_followup.csv")
by = {}
for r in fu:
    by.setdefault(blocks[r["block_id"]], []).append(r)
for d, recs in by.items():
    n = len(recs)
    L = count[d]
    left = sum(1 for r in recs if r["outcome"] in ("left Kilvarra", "died")) / n * L
    dup = sum(1 for r in recs if r["outcome"] == "duplicate registration") / n * L
    unplaced = sum(1 for r in recs if r["outcome"] in ("not known at address", "address vacant", "no contact")) / n * L
    moved = sum(1 for r in recs if r["outcome"] == "moved, now elsewhere in Kilvarra") / n * L
    p = F["register_not_correct_parts"][d]
    check("follow-up parts %s" % d, abs(dup - p["duplicate registrations"]) <= 0.04 * dup + 10
          and 0.96 * left - 10 <= p["left Kilvarra or died"] <= 1.04 * (left + unplaced) + 10
          and p["living elsewhere in Kilvarra"] <= 1.04 * (moved + unplaced) + 10,
          "left %d dup %d unplaced %d moved %d against %s" % (left, dup, unplaced, moved, p))
    tot = sum(p.values())
    check("parts sum to the entries not correct %s" % d, abs(tot - F["register_not_correct"][d]) <= 30,
          "%d against %d" % (tot, F["register_not_correct"][d]))

# ---------------------------------------------------------------- the bridges add up
for d in F["district_estimates"]:
    forces = 0
    if d == "D04":
        forces = sum(int(r["personnel"]) for r in rows("DF_personnel_by_location_2026-06-30.csv"))
    est = F["register_counts"][d] - F["register_not_correct"][d] + F["listed_elsewhere"][d] + F["on_no_list"][d] + forces
    check("register bridge adds to the estimate %s" % d, abs(est - F["district_estimates"][d]) <= 40,
          "%d against %d" % (est, F["district_estimates"][d]))
nat = F["official_2026"] - F["unrecorded_emigration"] + F["immigration_not_in_accounts"] - F["official_remainder"]
check("national bridge adds to the estimate", abs(nat - F["national_estimate"]) <= 20, "%d against %d" % (nat, F["national_estimate"]))
check("districts add to Kilvarra", abs(sum(F["district_estimates"].values()) - F["national_estimate"]) <= 60,
      "%d against %d" % (sum(F["district_estimates"].values()), F["national_estimate"]))

# ---------------------------------------------------------------- the call under paragraph 3.2
for d, (lo, hi) in F["district_intervals"].items():
    want = "qualifies" if lo >= 25000 else ("does not qualify" if hi < 25000 else "too close to call")
    got = "qualifies" if d in F["call"]["qualifies"] else ("too close to call" if d in F["call"]["too close to call"] else "does not qualify")
    check("call %s under 3.2" % d, want == got, "%s against %s" % (got, want))

# ---------------------------------------------------------------- the benchmark from births and the life table
wb = openpyxl.load_workbook(os.path.join(T, "KSO_vital_statistics_2026.xlsx"), read_only=True)
b = {}
for r in wb["Births"].iter_rows(values_only=True):
    if r and r[0] is not None and isinstance(r[1], int):
        b[int(str(r[0])[:4])] = (r[1], r[2])
lt = {}
for r in wb["Life table 2019-21"].iter_rows(values_only=True):
    if r and r[0] is not None and isinstance(r[2], int):
        lt[int(str(r[0]).rstrip("+"))] = (r[2], r[4])
check("births read back (positive control)", len(b) == 72 and 1990 in b, "%d years" % len(b))
for lo_, hi_, key in ((18, 29, "18-29"), (30, 44, "30-44")):
    M = sum(0.5 * (b[2025 - a][0] + b[2026 - a][0]) * lt[a][0] for a in range(lo_, hi_ + 1))
    Fm = sum(0.5 * (b[2025 - a][1] + b[2026 - a][1]) * lt[a][1] for a in range(lo_, hi_ + 1))
    check("men per woman from births %s" % key, abs(M / Fm - F["da_ratio"][key]) < 0.0005, "%.4f against %.4f" % (M / Fm, F["da_ratio"][key]))

# ---------------------------------------------------------------- coverage against the clerical review's direct estimate
persons = {r["person_id"]: r for r in rows("CS26_persons.csv")}
regd = {}
for r in reg:
    regd[r["khs_number"]] = pcd.get(pc_key(r["postcode"]))
for grp, lab, tol in (("KV", "nationals", 2.0), ("X", "others", 4.5)):
    n = on = 0
    for r in rows("CS26_clerical_review.csv"):
        p = persons[r["person_id"]]
        if p["defence_forces"] == "Y":
            continue
        if (p["citizenship"] == "KV") != (grp == "KV"):
            continue
        n += 1
        if r["review_outcome"] == "matched" and regd.get(r["khs_number"]) == blocks[p["block_id"]]:
            on += 1
    direct = 100.0 * on / n
    check("coverage %s within the clerical review's own estimate" % lab, abs(direct - F["coverage_pct"][lab]) <= tol,
          "review %.1f against %.1f (n %d)" % (direct, F["coverage_pct"][lab], n))

# ---------------------------------------------------------------- the golden files read back
gw = openpyxl.load_workbook(os.path.join(GOLD, [f for f in os.listdir(GOLD) if f.endswith(".xlsx")][0]), read_only=True)
est_sheet = [r for r in gw["Estimates"].iter_rows(values_only=True) if r and isinstance(r[2], int)]
check("golden workbook read back (positive control)", len(est_sheet) == 13, "%d rows" % len(est_sheet))
for r in est_sheet[:12]:
    check("workbook estimate %s" % r[0], r[2] == F["district_estimates"][r[0]], "%s against %s" % (r[2], F["district_estimates"][r[0]]))
from docx import Document  # noqa: E402

doc = Document(os.path.join(GOLD, [f for f in os.listdir(GOLD) if f.endswith(".docx")][0]))
dtext = " ".join(p.text for p in doc.paragraphs)
check("memo read back (positive control)", "Mid-2026 district estimates" in dtext and len(dtext) > 1500, "%d chars" % len(dtext))
check("memo states the national estimate", "{:,}".format(F["national_estimate"]) in dtext)
for d in F["call"]["too close to call"]:
    check("memo names the close district %s" % d, F["district_names"][d] in dtext)

fails = [r for r in results if not r[1]]
for name, ok, detail in results:
    print("%s  %-60s %s" % ("PASS" if ok else "FAIL", name, detail))
print("%d checks, %d FAIL" % (len(results), len(fails)))
sys.exit(1 if fails else 0)
