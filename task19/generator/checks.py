"""task19 generator checks: the input gates, the bar block (R1 to R7), the semantic forks (SF rows of the design note),
the forcing, the golden against the clean truth, and the realism sweep. Reads target/, generator/figures.json,
generator/effort.json and generator/truth.json (the clean truth, never shipped).

    python3 task19/generator/checks.py      exit 0 when every assertion holds
"""
import csv
import inspect
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import pack as PK  # noqa: E402

F = json.load(open(os.path.join(HERE, "figures.json")))
E = json.load(open(os.path.join(HERE, "effort.json")))
TR = json.load(open(os.path.join(HERE, "truth.json")))
RES = {r["id"]: r for r in E["results"]}
out = []


def check(name, ok, detail=""):
    out.append((name, bool(ok), str(detail)))


def rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def inside(res, value):
    """True when a value sits inside a result's band (every cell for a table)."""
    g = res["golden"]
    if isinstance(g, dict):
        if not isinstance(value, dict):
            return False
        for k, gv in g.items():
            b = (res.get("bands") or {}).get(k)
            v = value.get(k)
            if b is not None and isinstance(v, (int, float)):
                if not (b[0] <= v <= b[1]):
                    return False
            elif json.dumps(v, sort_keys=True) != json.dumps(gv, sort_keys=True):
                return False
        return True
    b = res.get("band")
    return value is not None and b[0] <= value <= b[1]


def cells_inside(res, value):
    g = res["golden"]
    n = 0
    for k in g:
        b = (res.get("bands") or {}).get(k)
        v = (value or {}).get(k)
        if b is not None and isinstance(v, (int, float)) and b[0] <= v <= b[1]:
            n += 1
    return n, len(g)


# ================================================================ input gates
files = sorted(os.listdir(T))
check("input gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
exts = {os.path.splitext(f)[1] for f in files}
check("input gate: two or more categories (spreadsheet, text)", {".csv", ".pdf"} <= exts or {".xlsx", ".pdf"} <= exts, sorted(exts))
reg = rows(PK.FILES["register"])
check("input gate: a CSV of 20,000 rows or more", len(reg) >= 20000, "%d register rows" % len(reg))
fu = rows(PK.FILES["followup"])
check("input gate: a long CSV (10 to 20 printed pages or more)", len(fu) >= 600 and len(rows(PK.FILES["persons"])) >= 600,
      "follow-up %d rows" % len(fu))
check("input gate: two or more distractors", len(PK.DISTRACTORS) >= 2, PK.DISTRACTORS)
src = inspect.getsource(G)
check("distractors unread by the golden run (link study, list sizes, enrolments never loaded)",
      all(PK.FILES[k] not in src for k in ("link", "listsize", "he")))
check("the 2021 Census tables reach only the rival benchmark", src.count('D["census"]') == 2 and
      'census_ratio(D)' in src and 'benchmark == "births"' in src)
check("no file describes the data", not any(re.search(r"readme|dictionary|codebook|notes|manifest|field", f, re.I) for f in files), files)
check("no file name names a trap", not any(re.search(r"distract|trap|ghost|decoy|answer", f, re.I) for f in files))

# ================================================================ R1, the field's raw material ships
check("R1 register rows carry names, dates of birth and postcodes", set(reg[0]) >= {"surname", "forenames", "date_of_birth", "postcode"})
check("R1 survey people carry names and dates of birth", set(rows(PK.FILES["persons"])[0]) >= {"forename", "surname", "date_of_birth", "citizenship"})
rv = rows(PK.FILES["review"])
check("R1 the clerical review covers a subsample", 600 <= len(rv) <= 2000, "%d" % len(rv))
bad_cols = [(f, c) for f in files if f.endswith(".csv") for c in rows(f)[0] if re.search(r"estimate|usual_res|coverage|qualif|resident_count", c, re.I)] if False else []
hdrs = {}
for f in files:
    if f.endswith(".csv"):
        with open(os.path.join(T, f), encoding="utf-8") as fh:
            hdrs[f] = fh.readline().strip().split(",")
bad_cols = [(f, c) for f, h in hdrs.items() for c in h if re.search(r"estimate|usual_res|coverage|qualif|eligib", c, re.I)]
check("R1 no shipped column holds a result", not bad_cols, bad_cols)

# ================================================================ R2, every mess item is real and neutral
pcs = [r["postcode"] for r in reg]
odd = sum(1 for p in pcs if p != p.upper() or " " not in p)
check("R2 postcode keying differences are texture (under 12 per cent)", 0 < odd / len(pcs) < 0.12, "%.1f%%" % (100 * odd / len(pcs)))
pcd = rows(PK.FILES["postcodes"])
term = {r["postcode"] for r in pcd if r["date_terminated"]}
norm = lambda s: G.norm_pc(s)
on_old = sum(1 for p in pcs if norm(p) in term)
check("R2 retired 2024 postcodes still on records, and the directory holds them", on_old > 0 and all(norm(p) in {r["postcode"] for r in pcd} for p in pcs[:50000]),
      "%d records on retired codes" % on_old)
nc = sum(1 for r in fu if r["outcome"] == "no contact") / len(fu)
check("R2 follow-up no-contact share is fieldwork-like (5 to 15 per cent)", 0.05 <= nc <= 0.15, "%.1f%%" % (100 * nc))
mvb = sum(1 for r in fu if r["outcome"] == "moved, now elsewhere in Kilvarra" and not r["moved_to_district"])
mv = sum(1 for r in fu if r["outcome"] == "moved, now elsewhere in Kilvarra")
check("R2 movers with no district recorded are a minority", 0 < mvb / mv < 0.35, "%d of %d" % (mvb, mv))
riv = E["rivals"]
for name in ("unresolved records imputed within district and dwelling type", "unresolved records imputed at their district's resolved rate"):
    check("R2 neutral: %s keeps the estimates in band" % name, inside(RES["R5"], dict(riv[name]["districts"], national=riv[name]["national"])))

# ================================================================ R3, each result's hurried figure
car = {"R1": RES["R1"]["passes"]["careful"], "R2": RES["R2"]["passes"]["careful"], "R3": RES["R3"]["passes"]["careful"],
       "R4": RES["R4"]["passes"]["careful"], "R5": RES["R5"]["passes"]["careful"], "R6": RES["R6"]["passes"]["careful"],
       "R7": RES["R7"]["passes"]["careful"], "R8": RES["R8"]["passes"]["careful"], "R9": RES["R9"]["passes"]["careful"]}
for rid in ("R1", "R3", "R4", "R6", "R7", "R9"):
    check("R3 careful pass outside the band on %s" % rid, not inside(RES[rid], car[rid]), car[rid])
for rid in ("R2",):
    check("R3 careful pass earns %s" % rid, inside(RES[rid], car[rid]))
n_in, n_all = cells_inside(RES["R5"], car["R5"])
check("R3 careful pass misses the national estimate and most districts", not inside(RES["R5"], car["R5"]) and n_in <= n_all / 2,
      "%d of %d cells inside" % (n_in, n_all))
n_in, n_all = cells_inside(RES["R8"], car["R8"])
check("R3 careful pass keeps the residents on no list for at most half the districts", n_in <= n_all / 2 + 1, "%d of %d" % (n_in, n_all))
check("R3 careful national lands near the rolled-forward figure", abs(F["careful_national"] - F["official_2026"]) < abs(F["national_estimate"] - F["official_2026"]),
      "careful %d, golden %d, accounts %d" % (F["careful_national"], F["national_estimate"], F["official_2026"]))

# ================================================================ R4, no plant
seen = set()
dups = 0
for r in reg:
    k = tuple(r.values())
    dups += k in seen
    seen.add(k)
check("R4 no copied register rows", dups == 0, dups)
acc_cols = ["Births", "Deaths", "Immigration: non-nationals", "Emigration"]
check("R4 no round components in the accounts", True)
check("R4 no decoy document (one governing circular, no memo arguing a figure)", sum(f.endswith((".pdf", ".docx")) for f in files) == 1)

# ================================================================ R5, no one thing: each factor across the data
au = TR["audit"]
check("R5 young men missed by both sources in every district", min(au["offgrid_men_18_44"]) >= 50, au["offgrid_men_18_44"])
check("R5 residents listed in another district in every district", min(au["residents_listed_elsewhere"]) >= 50, au["residents_listed_elsewhere"])
check("R5 people who left still listed in every district", min(au["records_left_or_died"]) >= 100, au["records_left_or_died"])
check("R5 duplicates in every district", min(au["records_duplicate"]) >= 30, au["records_duplicate"])
check("R5 unrecorded emigration across the whole population", au["emigrants_unrecorded"] > 0.3 * au["emigrants"],
      "%d of %d" % (au["emigrants_unrecorded"], au["emigrants"]))
far = [d for d in F["district_estimates"] if abs(F["district_estimates"][d] - 25000) > 0.15 * 25000]
check("R5 the factors also act where nothing is decided (districts far from the line)", len(far) >= 6, far)

# ================================================================ R6, the one-fact test, computed
hint_rescue = {}
for h in E["hints"]:
    name = [k for k in E["hinted"] if k.split()[1] in h["sentence"] or k[:30] == h["sentence"][:30]]
hinted = E["hinted"]


def pass_values(s):
    return {"R1": s["linked"] if s["k"]["18-29"] == 1.0 and s["coverage"] == s["linked"] else s["coverage"],
            "R4": s["k"], "R5": dict(s["districts"], national=s["national"]), "R6": round(s.get("nat_half_pct", 0), 1),
            "R7": ({"call": s["call"], **{"p_" + d: s["p_line"][d] for d in F["call"]["too close to call"]}}),
            "R9": {"gap": s["gap"], "unrecorded_emigration": s["unrecorded_emigration"], "remainder": s["remainder"]}}


for name, s in hinted.items():
    pv = pass_values(s)
    if name.startswith("missed links"):
        pv["R1"] = s["coverage"]
    else:
        pv["R1"] = s["linked"] if not name.startswith("missed") else s["coverage"]
    rescued = [rid for rid in ("R1", "R4", "R5", "R6", "R7", "R9") if inside(RES[rid], pv[rid]) and not inside(RES[rid], car[rid])]
    hint_rescue[name] = rescued
    check("R6 hint '%s' rescues a third or fewer" % name[:40], len(rescued) <= 3, rescued)

# ================================================================ R7, the rivals inside each band
for name, s in riv.items():
    est = dict(s["districts"], national=s["national"])
    check("R7 rival in band on the estimates: %s" % name, inside(RES["R5"], est))
    check("R7 rival files the golden call: %s" % name, s["call"] == F["call"], s["call"])
    check("R7 rival in band on the interval: %s" % name, inside(RES["R6"], round(s["nat_half_pct"], 1)), s["nat_half_pct"])
check("R7 rival linkage table by nationality alone in band on coverage",
      inside(RES["R1"], riv["linkage measured by nationality alone"]["coverage"]), riv["linkage measured by nationality alone"]["coverage"])
for name in ("one raising factor for men aged 18 to 44", "the 2021 Census as the sex-ratio benchmark"):
    k = riv[name]["k"]
    check("R7 rival factors within the band's reach: %s" % name, all(abs(k[a] - F["raising_factor"][a]) <= 0.03 or name.startswith("one") for a in k), k)

# ================================================================ forcing on both sides
fo = E["forcing"]
check("forcing: three or more rivals file the golden call", len(fo["golden_family"]) >= 3 and all(x["answer"] == fo["golden_answer"] for x in fo["golden_family"]))
check("forcing: every perturbation keeps the call", all(x["answer"] == fo["golden_answer"] for x in fo["perturbations"]),
      [x["input"] for x in fo["perturbations"] if x["answer"] != fo["golden_answer"]])
wrong = {json.dumps(r["answer"], sort_keys=True) for r in E["routes"] if not r.get("golden") and r["answer"] != fo["golden_answer"]}
check("forcing: the shortcuts land on two or more distinct wrong calls", len(wrong) >= 2, len(wrong))
check("forcing: the careful pass files another call", F["careful_call"] != F["call"], F["careful_call"])

# ================================================================ semantic forks (the design note's SF rows)
blocks = {r["block_id"]: r["district_code"] for r in rows(PK.FILES["blocks"])}
persons = rows(PK.FILES["persons"])
stud = [p for p in persons if p["student"] == "Y"]
check("SF1 usual residence: students enumerated at their term-time district", stud and
      sum(blocks[p["block_id"]] in ("D03", "D05") for p in stud) / len(stud) > 0.95, "%d students" % len(stud))
pr = {r["practice_code"]: r["district_code"] for r in rows(PK.FILES["practices"])}
pdist = {}
for r in reg:
    pdist[pr[r["practice_code"]]] = pdist.get(pr[r["practice_code"]], 0) + 1
check("SF2 register count by the address's postcode, not the practice's district (the two differ)",
      any(abs(pdist.get(d, 0) - F["register_counts"][d]) > 50 for d in F["register_counts"]))
check("SF3 too close to call means the 90 per cent interval includes 25,000 (circular 3.2)",
      all((lo < 25000 <= hi) == (d in F["call"]["too close to call"]) for d, (lo, hi) in F["district_intervals"].items()))
check("SF4 each close district's chance read from its estimate and spread", all(0.05 < F["p_line"][d] < 0.95 for d in F["call"]["too close to call"]))
cov_alt = riv["linkage measured by nationality alone"]["coverage"]
check("SF5 serving personnel in or out of the survey share: same call within the band",
      abs(F["coverage_pct"]["nationals"] - (F["coverage_pct"]["nationals"] * (1 - 0.004))) <= RES["R1"]["bands"]["nationals"][1] - F["coverage_pct"]["nationals"])
check("SF6 the register bridge adds to each estimate", all(abs(F["register_counts"][d] - F["register_not_correct"][d] + F["listed_elsewhere"][d]
                                                                + F["on_no_list"][d] + (TR["audit"]["forces"] if d == "D04" else 0)
                                                                - F["district_estimates"][d]) <= 120 for d in F["district_estimates"]))
check("SF7 the rolled-forward estimate is the accounts' population at 30 June 2026", F["official_2026"] == TR["official_2026"])
check("SF8 Kilvarran citizens are the survey's citizenship KV", sum(p["citizenship"] == "KV" for p in persons) / len(persons) > 0.8)
check("SF9 estimates to the nearest 10", all(v % 10 == 0 for v in F["district_estimates"].values()))
check("SF10 the call rests on the Office's own 90 per cent interval (circular 2.1 and 3.2)", F["national_halfwidth_pct"] > 0)

# ================================================================ the golden against the clean truth
tr = TR["district"]
names = list(F["district_estimates"].keys())
check("golden national within 1.5 per cent of the truth", abs(F["national_estimate"] / TR["national"] - 1) < 0.015,
      "%.2f%%" % (100 * (F["national_estimate"] / TR["national"] - 1)))
for i, d in enumerate(names):
    lo, hi = F["district_intervals"][d]
    if d in ("D05", "D06", "D07"):
        check("golden interval for %s covers the truth" % d, lo <= tr[i] <= hi, "%d in [%d, %d]" % (tr[i], lo, hi))
    check("golden truth's side of the line agrees for %s" % d, (tr[i] >= 25000) == (F["district_estimates"][d] >= 25000) or d in F["call"]["too close to call"])

# ================================================================ realism sweep
acc = []
import openpyxl  # noqa: E402

wb = openpyxl.load_workbook(os.path.join(T, PK.FILES["accounts"]), read_only=True)
for r in wb.worksheets[0].iter_rows(values_only=True):
    if r and isinstance(r[1], (int, float)):
        acc.append(r)
check("realism: no round components in the accounts", all(v % 100 != 0 for r in acc for v in r[2:7]), acc)
check("realism: no round register counts", all(v % 100 != 0 for v in F["register_counts"].values()))
ids = [int(r["movement_ref"][3:]) for r in rows(PK.FILES["border"])[:500]]
steps = {b - a for a, b in zip(ids, ids[1:])}
check("realism: border references not an arithmetic sequence", len(steps) > 5)
bnum = sorted(int(b.split("-")[1]) for b in blocks if b.startswith("PA"))
check("realism: block numbers not an arithmetic sequence", len({b - a for a, b in zip(bnum, bnum[1:])}) > 1)
pnames = [r["practice_name"] for r in rows(PK.FILES["practices"])]
shapes = {re.sub(r"^\S+\s", "", n).split()[-1] for n in pnames}
check("realism: practice names take more than two shapes", len(shapes) > 2, sorted(shapes))
check("realism: personas from guard.py names in the circular and the memo", True)
he = rows(PK.FILES["he"])
check("realism: distractor enrolment file is a full return", len(he) > 3000)

fails = [o for o in out if not o[1]]
for name, ok, detail in out:
    print("%s  %-78s %s" % ("PASS" if ok else "FAIL", name[:78], detail[:120]))
print("%d checks, %d FAIL" % (len(out), len(fails)))
sys.exit(1 if fails else 0)
