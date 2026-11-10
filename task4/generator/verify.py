"""An independent recomputation of the golden from the shipped files, sharing no code with analysis.py: its own
parsers, its own de-duplication, a per-shipper errors-in-variables correction by moments (the declared weight's
error variance read from the weighbridge for each shipper and each period its notes keep one practice, removed from
the pilot's within-shipper spread), normal equations solved directly, the batteries' first-year loss fitted tractor
by tractor, and the FES-2 assessment. Exit 1 unless it gives the golden's duties and every energy within 10 kWh of
the golden's.

    python3 verify.py [target]
"""
import csv
import json
import os
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def sheet_rows(path, name):
    z = zipfile.ZipFile(path)
    wbx = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = [s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
           for s in wbx.find("m:sheets", NS) if s.get("name") == name][0]
    target = [r.get("Target") for r in rels if r.get("Id") == rid][0]
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    ws = ET.fromstring(z.read("xl/" + target.lstrip("/").replace("xl/", "")))
    out = []
    for row in ws.find("m:sheetData", NS):
        vals = []
        for c in row:
            col = 0
            for ch in c.get("r"):
                if ch.isalpha():
                    col = col * 26 + ord(ch) - 64
            while len(vals) < col - 1:
                vals.append(None)
            v = c.find("m:v", NS)
            t = c.get("t")
            if t == "s":
                vals.append(shared[int(v.text)])
            elif t == "inlineStr":
                vals.append("".join(x.text or "" for x in c.iter("{%s}t" % NS["m"])))
            else:
                vals.append(None if v is None else float(v.text))
        out.append(vals)
    return out


def weight(s):
    s = s.strip().replace(" ", " ")
    if s.endswith(" t"):
        return float(s[:-2].replace(",", ".")) * 1000.0
    return float(s.replace(" kg", "").replace(" ", ""))


def main(target):
    j = lambda f: os.path.join(target, f)
    routes = {}
    for r in sheet_rows(j("route_register_2026.xlsx"), "Duties")[1:]:
        routes[r[0]] = (r[3], (r[6], r[7], r[8]), r[10], (r[6] + r[7] + r[8]) / r[12])
    short = [r[0] for r in sheet_rows(j("fleet_plan_2027.xlsx"), "Shortlist 2027")[1:]]
    stops = {}
    for r in sheet_rows(j("route_register_2026.xlsx"), "Stops")[1:]:
        stops.setdefault(r[0], {})[r[2]] = r[3]
    trl = {r[1]: (r[2], r[4] or "", r[7]) for r in sheet_rows(j("fleet_register_2026.xlsx"), "Trailers")[1:]}
    tractor = {r[1]: r[7] for r in sheet_rows(j("fleet_register_2026.xlsx"), "Tractors")[1:] if r[7]}

    def ride(duty, drops):
        """tonne-km share of the loaded run: walk the stops in km order, taking each drop's note weight off"""
        L = routes[duty][1][1]
        tot = sum(w for _, w in drops)
        acc, left, at = 0.0, 1.0, 0.0
        for km, w in sorted((stops[duty][t], w) for t, w in drops):
            acc += left * (km - at)
            left -= w / tot
            at = km
        return acc / L
    # weighbridge: per CMR the latest weighing
    latest = {}
    with open(j("weighbridge_varnamo_2024-11_2026-10.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["cmr_no"] not in latest or r["weighed_at"] > latest[r["cmr_no"]]["weighed_at"]:
                latest[r["cmr_no"]] = r
    by_ship = {}
    loads = {}
    month_gap = {}
    for r in latest.values():
        net = float(r["gross_kg"]) - float(r["tare_kg"])
        duty = r["duty"].replace("VMO-", "V")
        if "2025-11-01" <= r["weighed_at"][:10] <= "2026-10-31":
            loads.setdefault(duty, []).append(net)
        if r["declared_kg"]:
            month_gap.setdefault((r["shipper"], r["weighed_at"][:7]), []).append(abs(float(r["declared_kg"]) - net))
    # a month in which a shipper's notes carry its scale weight: the median gap is inside the bridge's resolution
    ticket = {k for k, v in month_gap.items() if np.median(v) <= 20}
    full = {s for s in {k[0] for k in month_gap} if all((s, m) in ticket for (ss, m) in month_gap if ss == s)}
    per = lambda s, ym: (s, "t" if (s, ym) in ticket and s not in full else "n")
    for r in latest.values():
        if r["declared_kg"]:
            net = float(r["gross_kg"]) - float(r["tare_kg"])
            by_ship.setdefault(per(r["shipper"], r["weighed_at"][:7]), []).append((float(r["declared_kg"]), net))
    # each shipper's declaration error: classical (variance of declared less weighed), standard (no spread) or nil
    err = {}
    for s, v in by_ship.items():
        D, W = np.array(v).T
        if D.std() < 1.0:
            err[s] = ("std", W.mean())
        else:
            err[s] = ("classical", np.var(D - W, ddof=1), D.mean(), W.mean())
    # pilot days
    tms = {}
    with open(j("tms_consignments_jonkoping_2025-2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r["vehicle_reg"], r["collection_date"])
            if k not in tms:
                tms[k] = dict(r, drops=[])
            tms[k]["drops"].append((r["delivery_town"], weight(r["declared_weight"])))
    vnotes = {}
    with open(j("tms_consignments_varnamo_2025-11_2026-10.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = r["duty"].replace("VMO-", "V")
            vnotes.setdefault(d, {}).setdefault(r["collection_date"], {"t": r["trailer_reg"], "drops": []})["drops"].append(
                (r["delivery_town"], weight(r["declared_weight"])))
    vtrl = {}
    with open(j("weighbridge_varnamo_2024-11_2026-10.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if "2025-11-01" <= r["weighed_at"][:10] <= "2026-10-31" and not r["remark"]:
                vtrl.setdefault(r["duty"].replace("VMO-", "V"), []).append(trl[r["trailer_reg"]][2])
    station = {}
    with open(j("daily_mean_temperature_2016-2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["station"] == "Jönköping":
                station[r["date"]] = float(r["temperature (C)"])
    days = {}
    with open(j("bev_daily_summary_2025-03_2026-10.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            days.setdefault((r["registration"], r["operating_date"]), r)
    rows = []
    for k, r in days.items():
        c = tms.get(k)
        if not c:
            continue
        import datetime as dt
        span = (dt.datetime.fromisoformat(r["last_arrival_utc"][:19]) -
                dt.datetime.fromisoformat(r["first_departure_utc"][:19])).total_seconds() / 3600
        body, equip, ttare = trl[c["trailer_reg"]]
        rows.append((c["duty"], per(c["shipper"], k[1][:7]), sum(w for _, w in c["drops"]), float(r["distance_km"]),
                     float(r["energy_used_kwh"]), float(r["ambient_mean_c"]) if r["ambient_mean_c"] else None,
                     station[k[1]], k[0], k[1], float(r["soc_start_pct"]) - float(r["soc_end_pct"]),
                     float(r["distance_km"]) / float(r["driving_time_h"]),
                     (tractor[k[0]] + ttare) / 1000.0, ride(c["duty"], c["drops"]),
                     span if "ePTO" in equip else 0.0, span - float(r["driving_time_h"]), len(c["drops"])))
    off = np.mean([x[5] - x[6] for x in rows if x[5] is not None])
    duty = np.array([x[0] for x in rows])
    ship = np.empty(len(rows), dtype=object)
    ship[:] = [x[1] for x in rows]
    dec = np.array([x[2] for x in rows])
    km = np.array([x[3] for x in rows])
    y = np.array([x[4] for x in rows])
    T = np.array([x[5] if x[5] is not None else x[6] + off for x in rows])
    lk = np.array([routes[d][1][1] for d in duty], float)
    cl = np.array([routes[d][2] for d in duty], float)
    # the payload by moments: within each shipper, the pilot's declared spread less the error variance
    pay = np.zeros(len(rows))
    for s in set(ship):
        m = np.array([x == s for x in ship])
        e = err[s]
        if e[0] == "std":
            pay[m] = e[1]
        else:
            vd = np.var(dec[m], ddof=1)
            lam = max(0.0, vd - e[1]) / vd if vd > 0 else 1.0
            pay[m] = dec[m].mean() + lam * (dec[m] - dec[m].mean())
    pay /= 1000.0
    vday = np.array([x[10] for x in rows])
    combo = np.array([x[11] for x in rows])
    rideshare = np.array([x[12] for x in rows])
    fridge_h = np.array([x[13] for x in rows])
    X = np.column_stack([km, km * cl, km * np.maximum(0, 16 - T), km * np.maximum(0, -T),
                         km * (vday ** 2 - 65.0 ** 2) / 1000.0, km * (combo - 19.0), pay * lk * rideshare, fridge_h])
    # time at the collection and the drops, by the number of drops: the mean of each group
    stay = {}
    for x in rows:
        stay.setdefault(x[15], []).append(x[14])
    stay = {n: float(np.mean(v)) for n, v in stay.items()}
    per_drop = (stay[max(stay)] - stay[1]) / (max(stay) - 1)
    # the speed a duty keeps on a -5 C day: its routing-tool speed times the pilot's actual-to-planned ratio on the
    # days within 3 C of -5
    ratio = vday / np.array([routes[d][3] for d in duty])
    rr = float(ratio[np.abs(T + 5.0) <= 3.0].mean())
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    # the first-year loss, tractor by tractor: energy per full charge on age and degrees below 20 C
    import datetime as dt
    cap = y / np.array([x[9] for x in rows]) * 100
    age = np.array([(dt.date.fromisoformat(x[8]) - dt.date(2025, 2, 17)).days / 365.25 for x in rows])
    regs = np.array([x[7] for x in rows])
    loss = []
    for g in sorted(set(regs)):
        m = regs == g
        A = np.column_stack([np.ones(m.sum()), age[m], np.maximum(0, 20 - T[m])])
        b = np.linalg.solve(A.T @ A, A.T @ cap[m])
        loss.append(-b[1] / b[0])
    loss = float(np.mean(loss))
    limit = 0.85 * 540 * (1 - loss)
    qt = subprocess.run(["pdftotext", "-layout", j("quotation_bev_tractors_2027.pdf"), "-"], capture_output=True, text=True).stdout
    import re
    t27 = float(re.search(r"Unladen weight\s+([\d,]+) kg", qt).group(1).replace(",", "")) / 1000.0
    res = {}
    for c in short:
        s, legs, climb, vplan = routes[c]
        tot = sum(legs)
        v5 = vplan * rr
        notes = list(vnotes[c].values())
        rs = float(np.mean([ride(c, x["drops"]) for x in notes]))
        epto = np.mean(["ePTO" in trl[x["t"]][1] for x in notes])
        hours = tot / v5 + stay[1] + per_drop * (len(stops[c]) - 1)
        cb = t27 + np.mean(vtrl[c]) / 1000.0
        e = beta @ np.array([tot, tot * climb, tot * 21.0, tot * 5.0, tot * (v5 ** 2 - 65.0 ** 2) / 1000.0,
                             tot * (cb - 19.0), np.mean(loads[c]) / 1000 * legs[1] * rs, epto * hours])
        res[c] = (float(e), e <= limit)
    go = sorted(c for c, v in res.items() if v[1])
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    okset = go == fig["call_set"]
    far = {c: (round(v[0]), fig["energy"][c]) for c, v in res.items() if abs(v[0] - fig["energy"][c]) > 10}
    okloss = abs(100 * loss - fig["loss_pct"]) <= 0.2
    print("verify: %d pilot days, payload %.2f kWh per t per 100 km, fridge %.2f kW, loss %.2f per cent, limit %.1f, "
          "%d tractors %s; set %s, energies %s, loss %s" % (len(rows), beta[-2] * 100, beta[-1], 100 * loss, limit,
                                                           len(go), go,
                                             "agree" if okset else "DIFFER", "within 10 kWh" if not far else
                                             "DIFFER " + str(far), "agrees" if okloss else "DIFFERS"))
    return 0 if okset and not far and okloss else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
