"""task10 architecture 6: an independent recomputation of the graded figures from target/, written without the
generator's estimators (pandas and least squares only), set against generator/figures.json.
python3 task10/generator/verify.py"""
import datetime as dt
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import parse as PA   # noqa: E402  (the pack's own reading: registers, PDFs, revisions)

HOL = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29), dt.date(2024, 12, 25),
       dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
PROV = {"PS40617": "Corvane Flex Ltd", "PS41236": "Corvane Flex Ltd", "PS41108": "Quillon Energy Services Ltd",
        "PS41474": "Quillon Energy Services Ltd"}


def winter(d):
    y = d.year if d.month >= 7 else d.year - 1
    return "%d/%02d" % (y, (y + 1) % 100)


def workday(d):
    return d.weekday() < 5 and d not in HOL and not ((d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 2))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    X = PA.load(TARGET)
    d = X["demand"].copy()
    loc = d["t_utc"].dt.tz_convert("Europe/London")
    start = loc - pd.Timedelta(minutes=30)
    d["day"] = start.dt.date
    d["hh"] = loc.dt.strftime("%H:%M")
    wx = X["weather"].copy()
    wx["day"] = wx["t_utc"].dt.date
    tm = wx.groupby("day")["temp_c"].agg(["mean", "size"])
    tm = tm[tm["size"] >= 20]["mean"]
    sw = X["switching"]
    bad, rows = [], []
    shares = {}
    per_zone = {}
    for code, name in sorted(((c, X["names"][c]) for c in PROV), key=lambda x: x[1]):
        z = d[d["code"] == code]
        ev = X["events"][X["events"]["zone"] == code]
        sched = set(ev["date"])
        swd = set()
        for r in sw.itertuples():
            if code in (r.frm, r.to):
                a = r.start.tz_convert("Europe/London").date()
                b = r.end.tz_convert("Europe/London").date()
                swd |= {a + dt.timedelta(days=i) for i in range((b - a).days + 1)}
        # R1: the 2025/26 daily peaks on the guideline's days, corrected to minus 3.0 C, grown
        pk = z.groupby("day")["mw"].agg(["max", "size"])
        pk = pk[pk["size"] >= 44]["max"]
        days = [x for x in pk.index if workday(x) and winter(x) == "2025/26" and x in tm.index and x not in sched and x not in swd]
        A = np.column_stack([np.ones(len(days)), [max(0.0, 15.5 - tm[x]) for x in days]])
        b, *_ = np.linalg.lstsq(A, np.array([pk[x] for x in days]), rcond=None)
        d26 = b[0] + b[1] * 18.5
        r1, r2 = X["rates"][code]
        before = d26 * (1 + r1 / 100) * (1 + r2 / 100) + X["growth"].get(code, 0.0)
        # each event's megawatts delivered at 17:30 and 18:00 against a baseline with winter levels and one slope
        tab = z[z["hh"].isin(["17:30", "18:00"])].pivot_table(index="day", columns="hh", values="mw")
        base_days = [x for x in tab.index if workday(x) and x in tm.index and x not in sched and x not in swd]
        res = {}
        for h in ("17:30", "18:00"):
            use = [x for x in base_days if not math.isnan(tab.loc[x, h])]
            ws = sorted({winter(x) for x in use})
            M = np.column_stack([[1.0 if winter(x) == w else 0.0 for x in use] for w in ws] + [[max(0.0, 15.5 - tm[x]) for x in use]])
            c, *_ = np.linalg.lstsq(M, np.array([tab.loc[x, h] for x in use]), rcond=None)
            res[h] = (dict(zip(ws, c[:-1])), c[-1])
        done = ev[ev["status"] == "Completed"]
        for r in done.itertuples():
            x = r.date
            if x not in tab.index or x not in tm.index or x in swd or tab.loc[x].isna().any():
                continue
            w = winter(x)
            fall = np.mean([res[h][0][w] + res[h][1] * max(0.0, 15.5 - tm[x]) - tab.loc[x, h] for h in ("17:30", "18:00")])
            rows.append((code, x, float(tm[x]), r.scheduled_mw, X["previous"][name][w], float(fall)))
        per_zone[name] = dict(before=before)
    E = pd.DataFrame(rows, columns=["zone", "day", "T", "sched", "contract", "fall"])
    for prov in sorted(set(PROV.values())):
        e = E[np.array([PROV[z] == prov for z in E["zone"]]) & (E["T"] <= -1.0).values]
        c = np.polyfit(e["T"], e["fall"] / e["contract"], 1)
        shares[prov] = float(np.polyval(c, -3.0))
    out = []
    for name in sorted(per_zone):
        code = [c for c in PROV if X["names"][c] == name][0]
        deliv = shares[PROV[code]] * X["contracts"][name]
        for key, val in (("r1_before", per_zone[name]["before"]), ("r2_delivered", deliv)):
            ok = abs(val - F[key][name]) <= 0.051
            out.append(ok)
            print("%s %-12s %-16s independent %.3f figures.json %.1f" % ("PASS" if ok else "FAIL", key, name, val, F[key][name]))
    for prov, s in shares.items():
        ok = abs(s - F["providers"][prov]["share"]) <= 0.0051
        out.append(ok)
        print("%s share        %-28s independent %.4f figures.json %.2f" % ("PASS" if ok else "FAIL", prov, s, F["providers"][prov]["share"]))
    n = int(sum(1 for _ in rows))
    ok = n == F["record"]["completed_total"]
    out.append(ok)
    print("%s events       completed events measured: %d against %d" % ("PASS" if ok else "FAIL", n, F["record"]["completed_total"]))
    print("verify: %s" % ("PASS" if all(out) else "FAIL"))
    return 0 if all(out) else 1


if __name__ == "__main__":
    sys.exit(main())
