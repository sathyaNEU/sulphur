"""A second implementation of the estimate, from the shipped files alone and sharing no code with analysis.py or
core.py: plain rows and dictionaries, the steps as the answer blocks state them.

    python3 task5/generator/verify.py [target]
"""
import csv
import json
import math
import os
import sys
from collections import defaultdict

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = "Orlava"
YEARS = list(range(2011, 2024))          # the years the released tables hold
LATE = [2024, 2025, 2026]


def _find(target, part):
    hit = [f for f in os.listdir(target) if part in f]
    assert len(hit) == 1, (part, hit)
    return os.path.join(target, hit[0])


def run(target):
    name = {}
    with open(_find(target, "state_codes"), newline="") as fh:
        for row in csv.DictReader(fh):
            for v in row.values():
                name[v.strip().lower()] = row["name"]
    hosts = [n for n in dict.fromkeys(name.values()) if n not in (HOME, "Other")]
    # --- the released tables: the latest release of every cell
    latest = {}
    with open(_find(target, "migration_tables"), newline="") as fh:
        for row in csv.DictReader(fh):
            key = (row["table"], row["reporting_state"], row["partner"], row["reference_year"], row["sex"], row["age_group"])
            if key not in latest or row["release"] > latest[key][0]:
                latest[key] = (row["release"], int(row["persons"]))
    T = defaultdict(float)
    for (t, rep, par, y, _s, _a), (_rel, v) in latest.items():
        T[t, name[rep.lower()], name[par.lower()], int(y)] += v
    # --- the register: one row an event, the year of the move
    seen = set()
    reg = defaultdict(float)
    with open(_find(target, "register_migration_events"), newline="") as fh:
        for row in csv.DictReader(fh):
            if row["event_no"] in seen:
                continue
            seen.add(row["event_no"])
            state = name[(row["state_code"].strip() or row["state_text"].strip()).lower()]
            cit = name[row["citizenship"].strip().lower()]
            y = int(row["move_date"][:4])
            out = row["event_type"] == "deregistration_abroad"
            if cit == HOME:
                reg["B" if out else "D", state, y] += 1
            else:
                reg["C" if out else "A", cit, y] += 1
    same = all(reg[t, h, y] == T[t, HOME, h, y] for t in "ABCD" for h in hosts for y in YEARS)
    # --- the counts
    wb = load_workbook(_find(target, "census_rounds"), read_only=True, data_only=True)

    def census(year):
        rows = list(wb["T1 citizenship %d" % year].iter_rows(values_only=True))
        col = [name.get(str(c).lower()) for c in rows[3]].index(HOME)
        return {name[str(r[0]).lower()]: float(r[col]) for r in rows[4:] if r[0] is not None and name.get(str(r[0]).lower()) in hosts}
    n11, n21 = census(2011), census(2021)
    nat = defaultdict(float)
    with open(_find(target, "vital_events"), newline="") as fh:
        for row in csv.DictReader(fh):
            if name[row["citizenship"].lower()] == HOME:
                nat[name[row["reporting_state"].lower()], int(row["reference_year"])] = int(row["live_births"]) - int(row["deaths"])
    abroad = {}
    for r in load_workbook(_find(target, "table_C14"), read_only=True, data_only=True).active.iter_rows(min_row=5, values_only=True):
        if r[0] is not None and name.get(str(r[0]).lower()) in hosts:
            abroad[name[str(r[0]).lower()]] = float(r[4])
    count16 = [float(r[1]) for r in load_workbook(_find(target, "population_count_2016"), read_only=True, data_only=True).active.iter_rows(
        values_only=True) if r[0] is not None and name.get(str(r[0]).lower()) == HOME][0]
    # --- step 2: what Orlava's register records of foreign arrivals
    a_home = sum(reg["A", i, 2020] for i in hosts) / sum(abroad.values())
    # --- step 3: each partner's share of its own emigrants, each host's share of arrivals
    b = {i: sum(T["B", i, HOME, y] for y in YEARS) / (sum(reg["A", i, y] for y in YEARS) / a_home) for i in hosts}
    a = {}
    for h in hosts:
        others = [i for i in hosts if i != h]
        a[h] = sum(T["A", h, i, y] for i in others for y in YEARS) / sum(T["B", i, h, y] / b[i] for i in others for y in YEARS)
    arr = {(h, y): T["A", h, HOME, y] / a[h] for h in hosts for y in YEARS}
    c1 = 100.0 * sum(reg["B", h, y] for h in hosts for y in YEARS) / sum(arr.values())
    out = dict(citizens={}, left={}, officers={}, same_as_released=same, share_home_arrivals_pct=100.0 * a_home, c1=c1)
    for h in hosts:
        # --- step 4: the exits between the censuses and the departures table's share of them
        decade = range(2011, 2021)
        gone = n11[h] + sum(arr[h, y] + nat[h, y] for y in decade) - n21[h]
        d = sum(T["C", h, HOME, y] for y in decade) / gone
        ex = {y: T["C", h, HOME, y] / d for y in YEARS}
        if h == "Skarholm":
            out["c2"] = 100.0 * d
        if h == "Fenmark":
            out["referee"] = n11[h] + sum(arr[h, y] + nat[h, y] - ex[y] for y in range(2011, 2016))
            out["referee_count"] = count16
        # --- step 6: the register's shares, the years after the tables, births less deaths at the 2021 to 2023 rate
        b_h = sum(reg["B", h, y] for y in YEARS) / sum(arr[h, y] for y in YEARS)
        r_h = sum(reg["D", h, y] for y in YEARS) / sum(ex[y] for y in YEARS)
        n, starts = n21[h], 0.0
        for y in (2021, 2022, 2023):
            starts += n
            n += arr[h, y] - ex[y] + nat[h, y]
        rate = sum(nat[h, y] for y in (2021, 2022, 2023)) / starts
        late = 0.0
        for y in LATE:
            x = reg["D", h, y] / r_h
            late += x
            n += reg["B", h, y] / b_h - x + n * rate
        early = sum(ex[y] for y in (2021, 2022, 2023))
        if h == "Tesmar":
            out["c3"] = late / early
        out["citizens"][h] = n
        out["left"][h] = early + late
        out["officers"][h] = int(math.ceil(n / 5000.0))
    return out


def compare(v, fig):
    bad = []
    for h, n in v["citizens"].items():
        if int(round(n)) != fig["citizens"][h]:
            bad.append(("citizens", h, n, fig["citizens"][h]))
        if int(round(v["left"][h])) != fig["left"][h]:
            bad.append(("left", h, v["left"][h], fig["left"][h]))
        if v["officers"][h] != fig["officers"][h]:
            bad.append(("officers", h))
    for k, nd in (("c1", 1), ("c2", 1), ("c3", 2), ("share_home_arrivals_pct", 1)):
        if round(v[k], nd) != fig[k]:
            bad.append((k, v[k], fig[k]))
    if int(round(v["referee"])) != fig["referee"]["golden"] or int(v["referee_count"]) != fig["referee"]["count"]:
        bad.append(("referee", v["referee"]))
    if not v["same_as_released"]:
        bad.append(("the register's counts differ from Orlava's released cells",))
    return bad


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    v = run(t)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = compare(v, fig)
    print("verify:", "PASS, the second implementation lands every stated figure" if not bad else "FAIL %s" % bad)
    sys.exit(1 if bad else 0)
