"""task3 architecture 4: the build's assertions, on generator/rungs.json, generator/figures.json, the cut pack and the
goldens. Each line prints PASS or FAIL; exit 1 on any FAIL.

Semantic forks (the design note's SF ids) and ladder claims (R ids) are asserted by name."""
import csv
import json
import math
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import params as P   # noqa: E402
import solve as S    # noqa: E402

R = json.load(open(os.path.join(HERE, "rungs.json")))
F = json.load(open(os.path.join(HERE, "figures.json")))
TARGET = os.path.join(TASK, "target")
out = []


def ok(name, cond, detail=""):
    out.append((name, bool(cond), detail))


def mg(x):
    return int(math.floor(x + 0.5))


def cells(r):
    return (r["call"], r["cross"], mg(float(r["ep"]["2034"])), r["hi_well"], mg(r["hi_2034"]))


g = R["golden"]
GOLD = cells(g)
ok("golden call", GOLD == (2027, 2031, 12, "W7", 16), str(GOLD))
ok("figures agree with the rungs", (F["call"], F["cross"], F["ep2034_int"], F["hi_well"], F["hi_2034_int"]) == GOLD)

# SF5 to SF9: every standing construction files the golden's cells
for name in R["standing"]:
    ok("standing %s" % name, cells(R[name]) == GOLD, str(cells(R[name])))
ok("SF5 the arrival point (half-way, fitted step, a quarter, three quarters)",
   all(cells(R[n]) == GOLD for n in ("golden", "arrival_step", "arrival_quarter", "arrival_threequarter")))
ok("SF6 the delay's form (intercept, origin, without the water-table age)",
   all(cells(R[n]) == GOLD for n in ("golden", "delay_origin", "delay_origin_noanchor", "no_age")))
ok("SF7 the current leachate (3, 5, 8 latest years; the matured conversions)",
   all(cells(R[n]) == GOLD for n in ("tail3", "golden", "tail8", "leach_cohort", "leach_cohort_noanchor")))
ok("SF8 nondetects (half, zero, the limit)", all(cells(R[n]) == GOLD for n in ("golden", "nd_zero", "nd_full")))
ok("SF9 the model carried to the wells' level or not", all(cells(R[n]) == GOLD for n in ("golden", "no_anchor")))
# SF1, SF3, SF4: filed in the plan and the prompt
plan = open(os.path.join(TARGET, "corlinden_water_supply_plan_2025.pdf"), "rb").read()
prompt = open(os.path.join(TASK, "prompt.txt")).read()
ok("SF1 the compliance measure filed (EP-01's annual flow-weighted mean)",
   "annual flow-weighted mean nitrate at entry point EP-01" in prompt)
ok("SF3 land cover after 2026 held", "hold each parcel's land cover as it stood in 2026" in prompt)
ok("SF4 in-service dates from the plan", P.CYCLES == {2027: 2030, 2031: 2034})
# SF2: the plan's shares; the historical shares keep the call and the crossing (instruction following moves A2 only)
ok("SF2 the plan's shares", abs(sum(P.PLAN_SHARE.values()) - 1) < 1e-9 and P.PLAN_SHARE["W3"] == 0.08)
ok("SF2 historical shares keep the call", R["history_shares"]["call"] == 2027 and R["history_shares"]["cross"] == 2031)
# SF10, SF11: the second judgments move the asks' figures and never the call
for n in ("area_weights", "leachtime_anchored"):
    ok("SF10 %s moves Well 7's 2034 mean" % n, mg(R[n]["hi_2034"]) == 15 and R[n]["call"] == 2027, str(cells(R[n])))
ok("SF10 root-zone recharge weights move the 2034 entry point", mg(float(R["leachtime_anchored"]["ep"]["2034"])) == 11)
ok("SF11 the all-years vegetable leachate moves both figures",
   mg(float(R["leach_all_years"]["ep"]["2034"])) == 13 and mg(R["leach_all_years"]["hi_2034"]) == 17 and
   R["leach_all_years"]["call"] == 2027)

# R1 the default path and the rungs file the 2031 cycle
for n in ("rung0_trend", "rung0_trend_sen", "rung1_gw_travel_time", "rung1_pooled_cohort_delay", "rung1_single_lag",
          "rung2_dismissed"):
    ok("R1 %s files the 2031 cycle" % n, R[n]["call"] == 2031 and R[n]["cross"] is None, str((R[n]["call"], R[n]["cross"])))
# R2 under every shallower delay the record rejects the clearing outright; under the golden's it is silent
for n in ("rung1_gw_travel_time", "rung1_pooled_cohort_delay", "rung1_single_lag"):
    sse = R[n]["sse_2019_2026"]
    ok("R2 %s rejects the clearing" % n, R[n]["k"] <= 0.1 and sse["1.0"] > 50 * sse["0.0"], str(sse))
ok("R2 the golden's record is silent on the clearing",
   abs(g["sse_2019_2026"]["1.0"] - g["sse_2019_2026"]["0.0"]) < 0.05 * g["sse_2019_2026"]["0.0"], str(g["sse_2019_2026"]))
ok("R2 the single lag fits the pre-clearing record", R["rung1_single_lag"]["lag"] <= 6.0 and
   R["rung1_single_lag"]["lag_rmse_1998_2018"] < 0.6, str((R["rung1_single_lag"]["lag"], R["rung1_single_lag"]["lag_rmse_1998_2018"])))

# R3 dominance: one correction on a lower rung leaves it on the wrong cycle (the single lag with the network's
# leachate but no clearing fitted puts the rise before 2026, contradicted; the travel time likewise)
ok("R3 the pooled and travel-time delays predict the ridge before 2026",
   min(R["rung1_gw_travel_time"]["misfit_2026_k1"].values()) > 3 and min(R["rung1_single_lag"]["misfit_2026_k1"].values()) > 3)

# R4 the delay and the window
D = S.read(TARGET)
fit = S.delay_fit(D, {})
ok("R4 the matured conversions", fit["n"] >= 12 and 0.12 <= fit["b"] <= 0.145 and fit["rmse"] < 0.6,
   "n %d b %.4f rmse %.2f" % (fit["n"], fit["b"], fit["rmse"]))
lo, hi_ = None, None
for b in np.arange(0.06, 0.26, 0.01):
    r = S.run(TARGET, D=D, b_override=float(b))
    vis = max(r["model"][w][2026] - r["obs"][w][2026] for w in ("W6", "W7"))
    if r["call"] == 2027 and vis < 1.0:
        lo = b if lo is None else lo
        hi_ = b
ok("R4 the call's window in the delay per foot covers the estimates",
   lo is not None and lo <= 0.115 and hi_ >= 0.155, "window %.2f to %.2f" % (lo or -1, hi_ or -1))
# the ridge is invisible in 2026 at the wells and at the network's own recent clearings
obs = D["well_annual"]
ok("R4 Wells 6 and 7 show no rise in 2026", obs["W6"][2026] <= obs["W6"][2022] + 0.3 and
   obs["W7"][2026] <= obs["W7"][2022] + 0.3)
rec = []
for sid, s in D["sites"].items():
    h = D["lc"][s["pid"]]
    if any(h[y] in P.IRRIGATED and h[y - 1] not in P.IRRIGATED for y in range(2013, 2027)):
        rec.append(max(x for t, x in D["net"][sid] if t >= 2025))
ok("R4 the network's recent clearings show nothing yet", len(rec) == 3 and max(rec) < 1.5, str(rec))
ok("R4 the 2031 margin", float(g["ep"]["2031"]) >= 10.5 and float(g["ep"]["2030"]) <= 9.3,
   "%s %s" % (g["ep"]["2030"], g["ep"]["2031"]))

# R5 the judge's stress cases (2026-11-08): a timing shift of a third to half a year either way, and the vegetable
# leachate at the low end of its estimates, keep every graded figure
for lab, kw in (("shift -0.45", {"shift": -0.45}), ("shift +0.45", {"shift": 0.45}), ("no age", {"age": False}),
                ("vegetable leachate 20.0", {"irv_override": 20.0}), ("vegetable leachate 21.5", {"irv_override": 21.5})):
    r = S.run(TARGET, D=D, **kw)
    hw = max(P.WELLS, key=lambda w: r["fc"][w][2034])
    c5 = (r["call"], r["cross"], mg(r["ep"][2034]), hw, mg(r["fc"][hw][2034]))
    ok("R5 %s keeps the golden's cells" % lab, c5 == GOLD, str(c5))
ok("R5 Well 7's 2034 mean sits clear of the rounding line", 0.3 <= abs(g["hi_2034"] - 15.5) and g["hi_2034"] < 16.3,
   str(g["hi_2034"]))

# ceiling
C = json.load(open(os.path.join(HERE, "ceiling.json")))
ok("pair ceiling at or under 50", C["pair_ceiling"] <= 50 and C["pair_ceiling_area"] <= 50, str(C))
ok("shallow keep under 25", C["shallow_keep"] < 25)

# the pack
files = sorted(os.listdir(TARGET))
ok("thirteen pack files", len(files) == 13, str(len(files)))
rows = {f: sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
ok("a CSV of 20,000 rows or more", max(rows.values()) >= 20000, str(rows))
ok("a second CSV of ten printed pages or more", sorted(rows.values())[-2] >= 600, str(rows))
cats = {os.path.splitext(f)[1] for f in files}
ok("three file categories", {".csv", ".xlsx", ".pdf", ".png"} <= cats)
md = json.load(open(os.path.join(TASK, "metadata.json")))
ok("two or more distractors", len(md["distractor_files"]) >= 2)
# the prompt and the goldens
ok("prompt under 1,000 characters", len(prompt.strip()) < 1000, str(len(prompt.strip())))
banned = re.findall(r"unsaturat|vadose|lag\b|delay|travel time|ridge|clear|convers|depth|leach|age survey", prompt, re.I)
ok("prompt names no step", not banned, str(banned))
gz = zipfile.ZipFile(os.path.join(TASK, "golden.zip")).namelist() if os.path.exists(os.path.join(TASK, "golden.zip")) else \
    sorted(os.listdir(os.path.join(TASK, "golden")))
ok("golden holds exactly the requested files", sorted(gz) == sorted(md["deliverables"]), str(gz))
sub = open(os.path.join(TASK, "submission.md")).read()
ok("submission blocks", all(h in sub for h in ("## 1. Final Recommendation", "## 2. Supplementary Questions",
                                                  "## 3. Critical Components", "## 4. Step-by-Step")))
ok("no em dash in the build", not any(chr(0x2014) in open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
                                      for dp in (HERE, TASK) for f in os.listdir(dp)
                                      if f.endswith((".py", ".md", ".txt", ".json"))))

bad = 0
for name, cond, detail in out:
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name, ("  [" + detail + "]") if detail and not cond else ""))
    bad += 0 if cond else 1
print("checks: %d of %d" % (len(out) - bad, len(out)))
sys.exit(1 if bad else 0)
