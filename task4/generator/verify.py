"""The independent verifier: reads only the shipped bundle (csv module and openpyxl, no generator module but the
calendar of public holidays it re-derives itself), recomputes every graded result on its own code path and holds
it to figures.json. Exit 1 on any miss."""
import csv
import datetime as dt
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def rows(name, delim=","):
    with open(os.path.join(T, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = divmod(b, 4)
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l_) // 433
    month = (h + l_ - 7 * m + 90) // 25
    return dt.date(y, month, (h + l_ - 7 * m + 33 * month + 19) % 32)


def closed(d):
    y = d.year
    e = easter(y)
    fixed = {(1, 1), (1, 6), (5, 1), (12, 6), (12, 24), (12, 25), (12, 26)}
    if (d.month, d.day) in fixed or d in (e - dt.timedelta(days=2), e + dt.timedelta(days=1), e + dt.timedelta(days=39)):
        return True
    if d.month == 6 and ((d.weekday() == 4 and 19 <= d.day <= 25) or (d.weekday() == 5 and 20 <= d.day <= 26)):
        return True
    if d.weekday() == 5 and (d.month == 10 and d.day == 31 or d.month == 11 and d.day <= 6):
        return True
    return False


def working(d):
    if closed(d):
        return False
    return d.weekday() < 5 or (d.weekday() == 5 and 46 <= d.isocalendar()[1] <= 50)


def nextwork(d):
    x = d
    while not working(x):
        x += dt.timedelta(days=1)
    return x


def main():
    # V1 the 2025 peak's picker hours
    seen = set()
    hrs = defaultdict(float)
    for r in rows("timesheets_2024-01_2026-10.csv"):
        key = (r["work_date"], r["person_id"], r["cost_centre"], r["shift"], r["paid_hours"], r["absence_code"])
        if key in seen:
            continue
        seen.add(key)
        d = dt.date.fromisoformat(r["work_date"])
        y, w, _ = d.isocalendar()
        if y == 2025 and 46 <= w <= 50 and not r["absence_code"]:
            hrs[r["cost_centre"].replace("SAA-", "")] += float(r["paid_hours"])
    for z in ("P1", "P2", "B1"):
        ok("V1 %s 2025 peak picker hours %.0f against %s" % (z, hrs[z], FIG["r1"][z]), abs(hrs[z] - FIG["r1"][z]) <= 1)

    # the zone hours, once each
    zh, seen = [], set()
    for r in rows("wms_zone_hours_2022-01_2026-10.csv"):
        k = tuple(r.values())
        if k in seen:
            continue
        seen.add(k)
        zh.append(r)
    picked = defaultdict(float)
    for r in zh:
        d = dt.date.fromisoformat(r["date"])
        y, w, _ = d.isocalendar()
        picked[(y, w, r["zone"])] += float(r["lines"]) - float(r["lines_hui"])

    # V2 the pooled overstatement
    bud = {}
    for r in rows("kotikaari_forecast_archive_2021-10_2026-10.csv"):
        if not r["round"].startswith("budget"):
            continue
        k = (r["round"], r["group"], int(r["iso_year"]), int(r["iso_week"]))
        if k not in bud or r["issued"] >= bud[k][0]:
            bud[k] = (r["issued"], float(r["order_lines"]))
    placed = defaultdict(float)
    for r in rows("wms_order_import_kotikaari_2022-01_2026-10.csv"):
        d = dt.date.fromisoformat(r["received"])
        y, w, _ = d.isocalendar()
        placed[(y, w, r["group"])] += float(r["web_lines"]) + float(r["store_lines"])
    num = sum(v[1] for k, v in bud.items() if 2022 <= k[2] <= 2025 and 46 <= k[3] <= 50)
    den = sum(v for k, v in placed.items() if 2022 <= k[0] <= 2025 and 46 <= k[1] <= 50)
    r2 = 100.0 * (num / den - 1.0)
    ok("V2 pooled overstatement %.2f against %s" % (r2, FIG["r2"]), abs(r2 - FIG["r2"]) <= 0.15)

    # V3 congestion, on its own grid and weights
    small = [r for r in zh if r["zone"] in ("P1", "P2") and int(r["lines"]) >= 30]
    n = np.array([float(r["lines"]) for r in small])
    d_ = np.array([dt.date.fromisoformat(r["date"]) >= dt.date(2024, 1, 8) for r in small])
    ais = np.where(d_, np.where([r["zone"] == "P1" for r in small], 12, 11), np.where([r["zone"] == "P1" for r in small], 8, 7))
    dpa = np.array([float(r["pickers_logged"]) for r in small]) / ais
    y = np.array([float(r["task_min"]) for r in small]) / n
    X0 = np.column_stack([np.array([float(r["lines_cls_" + c]) for r in small]) / n for c in "abcdf"] +
                         [(np.array([float(r["units"]) for r in small]) - n) / n,
                          np.array([r["zone"] == "P1" for r in small], float),
                          np.array([float(r["lines_hui"]) for r in small]) / n])
    best = None
    for kn in np.arange(0.40, 1.21, 0.05):
        for pw in np.arange(1.4, 2.61, 0.1):
            X = np.column_stack([X0, np.maximum(0.0, dpa - kn) ** pw])
            sw = np.sqrt(n)
            c, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
            sse = float(((y - X @ c) ** 2 * n).sum())
            if best is None or sse < best[0]:
                best = (sse, kn, pw, c)
    _, kn, pw, c = best
    r3 = c[8] * max(0.0, 1.8 - kn) ** pw
    ok("V3 congestion at 1.8 an aisle %.3f against %s" % (r3, FIG["r3"]), abs(r3 - FIG["r3"]) <= 0.03)

    # V4 Huippu Sport's extra minutes
    wb = load_workbook(os.path.join(T, "wms_item_master_2026-11-02.xlsx"), read_only=True)
    cls = {}
    for r in wb.active.iter_rows(min_row=2, values_only=True):
        if r[1] == "HUI":
            cls[str(r[2])] = r[5]
    wb = load_workbook(os.path.join(T, "huippu_slotting_2027.xlsx"), read_only=True)
    zone = {str(r[0]): r[2] for r in wb.active.iter_rows(min_row=4, values_only=True) if r[0]}
    agg = {z: [np.zeros(5), 0.0, 0.0] for z in ("P1", "P2")}
    for r in rows("huippu_article_lines_2024-11_2026-10.csv"):
        if r["month"] not in ("2025-11", "2025-12"):
            continue
        z = zone.get(r["article_no"])
        if z not in agg:
            continue
        agg[z][0]["ABCDF".index(cls[r["article_no"]])] += float(r["order_lines"])
        agg[z][1] += float(r["units"])
        agg[z][2] += float(r["order_lines"])
    th = 0.0
    tot = agg["P1"][2] + agg["P2"][2]
    for z, (cc, u, l_) in agg.items():
        t_ = float(cc / l_ @ c[:5] + c[5] * (u / l_ - 1.0) + c[6] * (z == "P1") + c[7])
        th += t_ * l_ / tot
    tk = 0.0
    kp = {z: [np.zeros(5), 0.0, 0.0] for z in ("P1", "P2")}
    for r in zh:
        d = dt.date.fromisoformat(r["date"])
        yy, ww, _ = d.isocalendar()
        if yy == 2025 and 46 <= ww <= 50 and r["zone"] in kp:
            kp[r["zone"]][0] += np.array([float(r["lines_cls_" + x]) for x in "abcdf"])
            kp[r["zone"]][1] += float(r["units"])
            kp[r["zone"]][2] += float(r["lines"])
    kt = kp["P1"][2] + kp["P2"][2]
    for z, (cc, u, l_) in kp.items():
        tk += float(cc / l_ @ c[:5] + c[5] * (u / l_ - 1.0) + c[6] * (z == "P1")) * l_ / kt
    r4 = th - tk
    ok("V4 Huippu Sport's extra minutes %.3f against %s" % (r4, FIG["r4"]), abs(r4 - FIG["r4"]) <= 0.03)

    # V5 the calibration
    pts = []
    plans = {}
    for r in rows("kotikaari_forecast_archive_2021-10_2026-10.csv"):
        if r["note"].startswith("Budget"):
            yy = int(r["note"].split()[1].rstrip(":"))
            nums = [float(x) for x in __import__("re").findall(r"\+(\d+) %", r["note"])]
            plans[yy] = (nums[0] / 100, nums[1] / 100)
    for yy in range(2022, 2026):
        for g, zones in (("small parts", ("P1", "P2")), ("bulky", ("B1",))):
            fb = sum(v[1] for k, v in bud.items() if k[1] == g and k[2] == yy)
            pk = sum(v for k, v in placed.items() if k[0] == yy and k[2] == g)
            pts.append((math.log1p(plans[yy][0 if g == "small parts" else 1]), math.log(fb / pk)))
    A_ = np.array([[1.0, p[0]] for p in pts])
    cf, *_ = np.linalg.lstsq(A_, np.array([p[1] for p in pts]), rcond=None)
    k27 = 100.0 * math.expm1(cf[0] + cf[1] * math.log1p(plans[2027][0]))
    ok("V5 the 2027 overstatement, Kotikaari small parts %.2f against %s" % (k27, FIG["r5"]["K_sp"]),
       abs(k27 - FIG["r5"]["K_sp"]) <= 0.3)

    # V6 week 47's share once 2025's orders move to 2027's days
    picks = defaultdict(float)
    for r in rows("wms_order_import_kotikaari_2022-01_2026-10.csv"):
        if r["group"] != "small parts":
            continue
        d = dt.date.fromisoformat(r["received"])
        if d.year not in (2025,):
            continue
        nd = d + dt.timedelta(days=728)
        picks[nextwork(nd + dt.timedelta(days=1))] += float(r["web_lines"])
        if float(r["store_lines"]) and d.weekday() < 5:
            q = nd
            while not (working(q) and q.weekday() < 5):
                q += dt.timedelta(days=1)
            picks[q] += float(r["store_lines"])
    wk = defaultdict(float)
    for p, v in picks.items():
        yy, ww, _ = p.isocalendar()
        if yy == 2027 and 46 <= ww <= 50:
            wk[ww] += v
    r6 = 100.0 * wk[47] / sum(wk.values())
    ok("V6 week 47's share %.2f against %s" % (r6, FIG["r6"]), abs(r6 - FIG["r6"]) <= 0.3)

    # V7 the evening cells, on this verifier's own capacity at each zone's limit
    crew = defaultdict(int)
    seen2 = set()
    for r in rows("timesheets_2024-01_2026-10.csv"):
        key = (r["work_date"], r["person_id"], r["cost_centre"], r["shift"])
        if key in seen2 or r["absence_code"]:
            continue
        seen2.add(key)
        d = dt.date.fromisoformat(r["work_date"])
        if 46 <= d.isocalendar()[1] <= 50 and r["cost_centre"] in ("SAA-P1", "SAA-P2"):
            crew[(r["work_date"], r["cost_centre"][4:], r["shift"])] += 1
    logged, heads = defaultdict(float), defaultdict(float)
    for r in zh:
        d = dt.date.fromisoformat(r["date"])
        if d.year not in (2024, 2025) or not 46 <= d.isocalendar()[1] <= 50 or r["zone"] not in ("P1", "P2"):
            continue
        if crew.get((r["date"], r["zone"], "EVE")):
            continue
        h = int(r["hour"])
        logged[h] += float(r["pickers_logged"])
        heads[h] += crew.get((r["date"], r["zone"], "DAY"), 0)
    ls = {h: logged[h] / heads[h] for h in range(6, 15) if heads[h]}
    limit = {"P1": 24, "P2": 22}
    aisles = {"P1": 12, "P2": 11}
    tz = {}
    for z in ("P1", "P2"):
        cc, u, l_ = kp[z]
        tz[(z, "k")] = float(cc / l_ @ c[:5] + c[5] * (u / l_ - 1.0) + c[6] * (z == "P1"))
        cc, u, l_ = agg[z]
        tz[(z, "h")] = float(cc / l_ @ c[:5] + c[5] * (u / l_ - 1.0) + c[6] * (z == "P1") + c[7])
    for z in ("P1", "P2"):
        ev = []
        for w in range(46, 51):
            days = sum(1 for k in range(1, 8) if working(dt.date.fromisocalendar(2027, w, k)))
            lk, lh = FIG["lines_split"][z][str(w)]
            t_ = (lk * tz[(z, "k")] + lh * tz[(z, "h")]) / (lk + lh)
            cap = days * sum(limit[z] * 60.0 * v / (t_ + c[8] * max(0.0, limit[z] * v / aisles[z] - kn) ** pw)
                             for v in ls.values())
            if lk + lh > cap:
                ev.append(w)
        ok("V7 %s evening weeks %s against %s" % (z, ev, FIG["evening"][z]), ev == FIG["evening"][z])

    bad = [x for x in OUT if not x[1]]
    for label, good, d in OUT:
        print(("PASS  " if good else "FAIL  ") + label)
    print("verify: %d of %d" % (len(OUT) - len(bad), len(OUT)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
