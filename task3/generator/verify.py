"""task3's independent verifier: reads only the bundle (target/), the goldens and figures.json on its own code path
(no generator module imported), recomputes the call and every graded figure, and reports each disagreement.

    python3 verify.py [task_dir]"""
import csv
import datetime as dt
import json
import os
import sys

import numpy as np
from docx import Document
from openpyxl import load_workbook
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))


def lp3(x, aep):
    lx = np.log10(np.asarray(x, dtype=float))
    return 10 ** (lx.mean() + lx.std(ddof=1) * stats.pearson3.ppf(1 - aep, stats.skew(lx, bias=False)))


def r10(x):
    from decimal import Decimal, ROUND_HALF_UP
    return int(Decimal(repr(float(x) / 10)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) * 10


def run(task_dir):
    t = os.path.join(task_dir, "target")
    pick = lambda pre: os.path.join(t, [f for f in os.listdir(t) if f.startswith(pre)][0])
    bad = []
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    # rain: the gauge in service, accumulations spread
    keep = {}
    for r in csv.DictReader(open(pick("tamsett_rain"))):
        d = dt.date.fromisoformat(r["date"])
        want = "TAM-RG-01" if d < dt.date(1987, 6, 14) else "TAM-RG-02"
        if r["station_id"] == want:
            keep[d] = (r["precip_in"], r["mflag"])
    rain, days = {}, sorted(keep)
    for i, d in enumerate(days):
        v, f = keep[d]
        if f[:1] == "A" and f[1:].isdigit():
            for j in range(int(f[1:])):
                rain[days[i - j]] = float(v) / int(f[1:])
        elif f in ("A", "M") or v == "":
            rain.setdefault(d, 0.0)
        else:
            rain[d] = float(v)
    tot = lambda d: sum(rain.get(d - dt.timedelta(days=j), 0.0) for j in range(3))
    # paved fraction
    wb = load_workbook(pick("tamsett_stormwater"), read_only=True)
    rows = list(wb["billing_parcels"].iter_rows(min_row=2, values_only=True))
    area = [r for r in wb["basins"].iter_rows(min_row=2, values_only=True) if r[0] == "OLL"][0][2] * 640 * 43560
    priors = {r[1] for r in rows if r[0] and r[1]}
    add = {}
    for r in rows:
        if r[2] == "OLL" and not (not r[0] and r[1] in priors):
            add[int(r[5])] = add.get(int(r[5]), 0) + float(r[4])
    frac, run_ = {}, 0.0
    for y in range(1900, 2026):
        run_ += add.get(y, 0)
        frac[y] = run_ / area
    # peaks and pairs
    ann = {int(r["water_year"]): float(r["peak_cfs"]) for r in csv.DictReader(open(pick("ollery_creek_annual")))}
    seen, X, Y = set(), [], []
    for r in csv.DictReader(open(pick("ollery_creek_peaks_above"))):
        k = (r["peak_date"], r["peak_time"])
        if k in seen:
            continue
        seen.add(k)
        P = tot(dt.date.fromisoformat(r["peak_date"]))
        if P >= 1.0:
            X.append([1.0, np.log(P), frac[int(r["water_year"])]])
            Y.append(np.log(float(r["peak_cfs"])))
    c = np.linalg.lstsq(np.array(X), np.array(Y), rcond=None)[0][2]
    years = sorted(ann)
    a = np.array([ann[y] for y in years])
    adj = a * np.exp(c * (frac[2025] - np.array([frac[y] for y in years])))
    q1, raw = lp3(adj, 0.01), lp3(a, 0.01)
    caps = {}
    doc = Document(pick("kinnard_road_culvert_alternatives"))
    for row in doc.tables[0].rows[1:]:
        caps[row.cells[0].text] = int(row.cells[2].text.replace(",", ""))
    choice = next(k for k in sorted(caps) if caps[k] >= q1)
    if choice != figs["pick"]:
        bad.append("call %s against %s" % (choice, figs["pick"]))
    if "{:,}".format(r10(q1)) != figs["design_flow"]:
        bad.append("design flow %.0f against %s" % (q1, figs["design_flow"]))
    if "{:,}".format(r10(raw)) != figs["raw_q1"]:
        bad.append("recorded-peak flow %.0f against %s" % (raw, figs["raw_q1"]))
    order = [years[i] for i in np.argsort(-adj)]
    if order[0] != figs["largest_year"] or order[:4] != figs["top4"]:
        bad.append("largest floods %s against %s %s" % (order[:4], figs["largest_year"], figs["top4"]))
    if "%.2f" % c != figs["c"]:
        bad.append("response rise %.3f against %s" % (c, figs["c"]))
    # the goldens carry the figures
    gold = os.path.join(task_dir, "golden")
    memo = "\n".join(p.text for p in Document(os.path.join(gold, "kinnard_road_culvert_design_flow.docx")).paragraphs)
    for want in (figs["design_flow"], "Alternative %s" % figs["pick"], str(figs["largest_year"])):
        if want not in memo:
            bad.append("memo lacks %s" % want)
    rows = list(csv.DictReader(open(os.path.join(gold, "ollery_creek_design_peak_table.csv"))))
    if len(rows) != len(years):
        bad.append("table has %d rows" % len(rows))
    for r, y, v in zip(rows, years, adj):
        if int(r["water_year"]) != y or int(r["estimate_peak_cfs"]) != r10(v):
            bad.append("table row %s: %s against %.0f" % (y, r["estimate_peak_cfs"], v))
            break
    return bad


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    b = run(task)
    print("verify: %s" % ("PASS" if not b else "FAIL\n  " + "\n  ".join(b)))
    sys.exit(1 if b else 0)
