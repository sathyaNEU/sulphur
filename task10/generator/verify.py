"""task10 architecture 5: an independent verifier. It reads target/ with its own code (the csv module, zoneinfo for the
UK clock, pypdf for the two governing PDFs, openpyxl for the registers), recomputes the golden by the guideline, and
compares every graded figure with generator/figures.json. It imports nothing from the generator.
python3 task10/generator/verify.py [target]"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
LONDON = ZoneInfo("Europe/London")
BANK = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29), dt.date(2024, 12, 25),
        dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
BASE, DESIGN = 15.5, -3.0


def rows(path, sheet):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[sheet]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it if r and r[0] is not None]


def winter(d):
    return d.year if d.month >= 7 else d.year - 1


def workday(d):
    xmas = (d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 2)
    return d.weekday() < 5 and d not in BANK and not xmas


def ols(X, y):
    b, *_ = np.linalg.lstsq(np.asarray(X, float), np.asarray(y, float), rcond=None)
    return b


def pdf_text(path):
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)


def main():
    t = lambda f: os.path.join(TARGET, f)
    reg = rows(t("primary_substation_register.xlsx"), "Primaries")
    point = {}
    for r in reg:
        point[r["SCADA point (to 13/05/2024)"]] = r["Asset code"]
        point[r["SCADA point (from 14/05/2024)"]] = r["Asset code"]
    name = {r["Asset code"]: r["Primary substation"] for r in reg}
    code_of = {v: k for k, v in name.items()}
    dfes = {r["Asset code"]: (float(r["Underlying peak growth 2026/27 (%)"]), float(r["Underlying peak growth 2027/28 (%)"]))
            for r in rows(t("primary_substation_register.xlsx"), "DFES 2026") if str(r["Asset code"]).startswith("PS")}
    feeders = rows(t("network_feeders_11kv.xlsx"), "Feeders")
    fmap = {}
    for r in feeders:
        fmap[r["Feeder ID"]] = r["Primary asset code"]
        fmap[r["Circuit (legacy)"]] = r["Primary asset code"]
    nbr = defaultdict(set)
    for r in rows(t("network_feeders_11kv.xlsx"), "Open points"):
        nbr[r["Primary (side 1)"]].add(r["Primary (side 2)"])
        nbr[r["Primary (side 2)"]].add(r["Primary (side 1)"])
    # growth: accepted offers, the energised included, energising 1 April 2026 to 31 October 2027 (guideline 4)
    conn = {}
    for r in rows(t("load_growth_register_2026-27.xlsx"), "Register"):
        if r["Status"] not in ("Accepted", "Energised") or not r["Planned energisation"]:
            continue
        when = r["Energised on"] or r["Planned energisation"]
        d = dt.datetime.strptime(when, "%d/%m/%Y").date()
        if dt.date(2026, 4, 1) <= d <= dt.date(2027, 10, 31):
            conn[r["Reference"]] = (fmap[r["11 kV feeder"]], float(r["Design demand (kW)"]) / 1000)
        else:
            conn.pop(r["Reference"], None)
    growth = defaultdict(float)
    for c, mw in conn.values():
        growth[c] += mw
    # the governing PDFs, read with pypdf
    guide = pdf_text(t("capacity_assessment_guideline_2026.pdf"))
    firm = {m.group(1): float(m.group(2)) for m in re.finditer(r"(PS\d{5})\s*\d+\s*\+\s*\d+\s*(\d+\.\d)", guide)}
    award = pdf_text(t("flexibility_contract_awards_2027-28.pdf"))
    # the awards table (section 2), its cells wrapped over lines: zone, primary, provider, MW, two prices
    block = " ".join(award[award.index("2. Awards"):award.index("3. Payment")].split())
    contract = {m.group(1): float(m.group(2)) for m in
                re.finditer(r"(Ashcombe Road|Charlecote Way|Fenwick Street|Hartwell Common) CMZ .*?(\d+\.\d) (\d+\.\d\d) (\d+)",
                            block)}
    # weather: the latest version of each hour, daily mean over the GMT day
    hours = {}
    with open(t("halverton_weather_hourly_2023-2026.csv"), newline="") as f:
        for r in csv.DictReader(f):
            k = r["ob_end_time"]
            if k not in hours or int(r["version_num"]) >= hours[k][0]:
                hours[k] = (int(r["version_num"]), float(r["air_temperature"]))
    acc = defaultdict(list)
    for k, (_, v) in hours.items():
        acc[dt.datetime.strptime(k, "%Y-%m-%d %H:%M").date()].append(v)
    tmean = {d: float(np.mean(v)) for d, v in acc.items() if len(v) >= 20}
    # dispatch log: the latest revision of each instruction
    latest = {}
    with open(t("flexibility_events_2024-2026.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["instruction_ref"] not in latest or int(r["revision"]) > int(latest[r["instruction_ref"]]["revision"]):
                latest[r["instruction_ref"]] = r
    sched = defaultdict(set)
    done = defaultdict(dict)
    for r in latest.values():
        d = dt.datetime.strptime(r["service_date"], "%d/%m/%Y").date()
        sched[r["primary_asset"]].add(d)
        if r["status"] == "Completed":
            done[r["primary_asset"]][d] = float(r["scheduled_mw"])
    # SCADA: quality G, each half-hour once, its start in UK local time
    peak = defaultdict(dict)
    count = defaultdict(dict)
    hh = defaultdict(dict)
    seen = set()
    with open(t("primary_demand_halfhourly_2023-2026.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["quality"] != "G":
                continue
            c = point[r["point"]]
            key = (c, r["interval_end_uk_local"])
            if key in seen:
                continue
            seen.add(key)
            loc = dt.datetime.strptime(r["interval_end_uk_local"], "%Y-%m-%d %H:%M").replace(tzinfo=LONDON)
            day = (loc - dt.timedelta(minutes=30)).date()
            v = float(r["value_mw"])
            peak[c][day] = max(peak[c].get(day, -1e9), v)
            count[c][day] = count[c].get(day, 0) + 1
            if loc.strftime("%H:%M") in ("17:30", "18:00"):
                hh[c].setdefault(day, {})[loc.strftime("%H:%M")] = v
    winters = [2023, 2024, 2025]

    def fit_days(days, val):
        X = [[1.0 if winter(d) == w else 0.0 for w in winters] + [max(0.0, BASE - tmean[d])] for d in days]
        return ols(X, [val(d) for d in days])

    def fit_2526(days, val):
        """guideline 3: the 2025/26 winter's own daily peaks, straight against the daily mean below the base"""
        days = [d for d in days if winter(d) == 2025]
        return ols([[1.0, max(0.0, BASE - tmean[d])] for d in days], [val(d) for d in days])

    def excess(c, days, skip):
        """actual less the weather-adjusted baseline, mean of the two credited half-hours, per day"""
        out = {}
        coefs = {}
        for h in ("17:30", "18:00"):
            train = [d for d in hh[c] if workday(d) and d in tmean and d not in skip and h in hh[c][d]]
            coefs[h] = fit_days(train, lambda d: hh[c][d][h])
        for d in days:
            v = [hh[c][d][h] - (coefs[h][winters.index(winter(d))] + coefs[h][-1] * max(0.0, BASE - tmean[d]))
                 for h in ("17:30", "18:00") if d in hh[c] and h in hh[c][d]]
            out[d] = float(np.mean(v)) if v else None
        return out

    figs = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    call = []
    colder = {t: [] for t in (-4.5, -6.0)}
    for zone in ("Ashcombe Road", "Charlecote Way", "Fenwick Street", "Hartwell Common"):
        c = code_of[zone]
        days = [d for d in peak[c] if workday(d) and d in tmean and d not in sched[c] and count[c][d] >= 44]
        b = fit_2526(days, lambda d: peak[c][d])
        d26 = b[0] + b[1] * (BASE - DESIGN)
        before = d26 * (1 + dfes[c][0] / 100) * (1 + dfes[c][1] / 100) + growth[c]
        evd = sorted(done[c])
        fall = {d: (-v if v is not None else None) for d, v in excess(c, evd, sched[c]).items()}
        rises = {n: excess(n, evd, sched[c]) for n in sorted(nbr[c])}
        mean_rise = {n: np.mean([v for v in r.values() if v is not None]) for n, r in rises.items()}
        linked = max(mean_rise, key=mean_rise.get)
        linked = linked if mean_rise[linked] > 0.3 else None
        y, T = [], []
        for d in evd:
            rise = rises[linked][d] if linked else 0.0
            if fall[d] is None or rise is None:
                continue
            y.append((fall[d] - rise) / done[c][d])
            T.append(tmean[d])
        k = ols([[1.0, x] for x in T], y)
        delivery = k[0] + k[1] * DESIGN
        credited = delivery * contract[zone]
        after = before - credited
        over = after > firm[c]
        if over:
            call.append(zone)
        # the asks: how far a primary to reinforce exceeds firm, and the colder working weekdays read the same way
        for tc in colder:
            before_c = (b[0] + b[1] * (BASE - tc)) * (1 + dfes[c][0] / 100) * (1 + dfes[c][1] / 100) + growth[c]
            if before_c - (k[0] + k[1] * tc) * contract[zone] > firm[c]:
                colder[tc].append(zone)
        z = figs["zones"][zone]
        if over and int(round(after - firm[c])) != int(round(z["over_by"])):
            print("DIFF %s exceeds firm by %.2f (generator %.2f)" % (zone, after - firm[c], z["over_by"]))
            bad.append(zone + " exceedance")
        mine = (round(delivery, 1), int(round(credited)), int(round(after)), over)
        theirs = (round(z["delivery"], 1), int(round(z["credited"])), int(round(z["after"])), z["over"])
        ok = mine == theirs and abs(delivery - z["delivery"]) < 0.002 and abs(after - z["after"]) < 0.02
        print("%-4s %-16s delivery %.3f credited %.2f after %.2f firm %.1f over %s linked %s  (generator %.3f %.2f %.2f)"
              % ("OK" if ok else "DIFF", zone, delivery, credited, after, firm[c], over, name.get(linked, "none"),
                 z["delivery"], z["credited"], z["after"]))
        if not ok:
            bad.append(zone)
    print("call %s (generator %s)" % (call, figs["call"]))
    if call != figs["call"]:
        bad.append("call")
    for tc, zs in colder.items():
        theirs = figs["sens"]["%.1f" % -tc]["commit"]
        print("%-4s over firm at minus %.1f C: %s (generator %s)" % ("OK" if zs == theirs else "DIFF", -tc, zs, theirs))
        if zs != theirs:
            bad.append("colder %.1f" % tc)
    print("VERIFY %s" % ("PASS" if not bad else "FAIL: " + ", ".join(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
