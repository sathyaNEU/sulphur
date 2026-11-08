"""The independent verifier (python3 verify.py <target>): rebuilt from the run log alone, not from analysis.fit.
Each run-day's van-hours (depot out to depot in, the break taken off) are regressed on which road sections the run
had to reach (any stop at or beyond a district), which districts it entered and how many stops each had; the 2027
year is forecast from the plan's parcels and the calendar's delivery days with Poisson stops; every combination of
offered districts is priced on each run. Asserts the golden's list, the rounded net saving and each run's rounded
van-hours saved."""
import collections
import csv
import itertools
import json
import math
import os
import sys

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))


def r50(x):
    return int(50 * math.floor(x / 50.0 + 0.5))


def r5000(x):
    return int(5000 * math.floor(x / 5000.0 + 0.5))


def main(target):
    F = lambda n: os.path.join(target, n)
    crow = list(load_workbook(F("district_register_2026.xlsx"), read_only=True)["Code changes"].iter_rows(values_only=True))[1:]
    back = {r[2]: r[0] for r in crow}
    regs = list(load_workbook(F("district_register_2026.xlsx"), read_only=True)["Districts"].iter_rows(values_only=True))[1:]
    plan = collections.defaultdict(lambda: [0] * 12)
    for r in list(load_workbook(F("volume_plan_2027.xlsx"), read_only=True)["Parcels by district"].iter_rows(values_only=True))[1:]:
        for k in range(12):
            plan[back.get(r[0], r[0])][k] += r[2 + k]
    rate = [r[1] for r in load_workbook(F("fleet_rate_card_2027.xlsx"), read_only=True)["Van-hour rate 2027"].iter_rows(values_only=True)
            if r[0] and str(r[0]).startswith("All-in")][0]
    days = [0] * 12
    for r in csv.DictReader(open(F("delivery_calendar_2027.csv"), encoding="utf-8")):
        if r["delivery_day"] == "Y":
            days[int(r["date"][5:7]) - 1] += 1
    hours = {}
    for r in csv.DictReader(open(F("van_run_log_2025-2026.csv"), encoding="utf-8")):
        a, b = r["depot_out"].split(":"), r["depot_in"].split(":")
        hours[(r["run_date"], r["run_code"])] = (int(b[0]) + int(b[1]) / 60) - (int(a[0]) + int(a[1]) / 60) - int(r["break_min"]) / 60
    stops = collections.defaultdict(collections.Counter)
    parcels = collections.Counter()
    seen = set()
    order = collections.defaultdict(collections.Counter)
    for r in csv.DictReader(open(F("delivery_stops_2025-2026.csv"), encoding="utf-8")):
        key = (r["run_date"], r["run_code"], r["stop_seq"], r["customer_ref"], r["arrived_local"])
        if key in seen or r["stop_type"] == "BREAK":
            continue
        seen.add(key)
        c = back.get(r["district_code"], r["district_code"])
        stops[(r["run_date"], r["run_code"])][c] += 1
        parcels[c] += int(r["parcels_delivered"])
        order[r["run_code"]][c] += int(r["stop_seq"])
    nstops = collections.Counter()
    for k, cnt in stops.items():
        for c, n in cnt.items():
            nstops[c] += n
    offer = ["MUL", "ACH", "BAN", "BLM", "LOU", "LEE", "LET", "CLI", "BCA", "CON", "CHA"]
    price = 12.60
    total, out, saved, before = 0.0, [], {}, {}
    for run in sorted({k[1] for k in hours}):
        ds = sorted({back.get(r[0], r[0]) for r in regs if r[5] == run},
                    key=lambda c: order[run][c] / max(1, nstops[c]))
        X, y = [], []
        for k, h in hours.items():
            if k[1] != run:
                continue
            cnt = stops[k]
            row = [1.0 if any(cnt[x] for x in ds[i:]) else 0.0 for i in range(len(ds))]
            row += [1.0 if cnt[c] else 0.0 for c in ds] + [float(cnt[c]) for c in ds] + [1.0]
            X.append(row)
            y.append(h)
        b = np.linalg.lstsq(np.array(X), np.array(y), rcond=None)[0]
        n = len(ds)
        spp = {c: nstops[c] / max(1, parcels[c]) for c in ds}
        mu = {c: [plan[c][k] * spp[c] / days[k] for k in range(12)] for c in ds}

        def yr(S):
            t = 0.0
            for k in range(12):
                lam = {c: 0.0 if c in S else mu[c][k] for c in ds}
                d = 0.0
                for i, c in enumerate(ds):
                    d += b[i] * (1 - math.exp(-sum(lam[x] for x in ds[i:])))
                    d += b[n + i] * (1 - math.exp(-lam[c])) + b[2 * n + i] * lam[c]
                t += (d + b[3 * n]) * days[k]
            return t
        cand = [c for c in ds if c in offer]
        best, bv, bh = (), 0.0, 0.0
        for kk in range(1, len(cand) + 1):
            for S in itertools.combinations(cand, kk):
                h = yr(()) - yr(S)
                v = h * rate - sum(sum(plan[c]) for c in S) * price
                if v > bv:
                    best, bv, bh = S, v, h
        out += list(best)
        total += bv
        if cand:
            saved[run] = r50(bh)
            before[run] = r50(yr(()) + 0.5 * sum(days))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    assert sorted(out) == sorted(figs["call_set"]), (out, figs["call_set"])
    assert r5000(total) == figs["net_saving_rounded"], (total, figs["net_saving_rounded"])
    assert saved == figs["runs_saved_h"], (saved, figs["runs_saved_h"])
    assert before == figs["runs_before_h"], (before, figs["runs_before_h"])
    print("verify: PASS (list %s, net saving %.0f rounds to %d, run hours %s)" % (sorted(out), total, r5000(total), saved))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
