"""An independent rebuild of the golden from the bundle alone, written a second way: it shares no code with
analysis.py and reads only target/ and the fleet standard's constants. Where the golden works on arrays by week
index it works on dated tables; the season is placed by the day of the year over 365.25 days, the bend is found on a
tenth-of-a-degree grid, the cellar relation is solved from its normal equations, the minimum order runs are read from
the quotation's own text and the weekly path is built as a table. It must file the same five covers and land every
stated figure inside the band the answer blocks give.

    python3 task4/generator/verify.py [target]
"""
import datetime as dt
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = ["K50", "K30", "K20", "FIR", "KIL"]
TAGGED = "K20"
FLOAT, SEASON_WEEKS, SUMMERS = 2.0 / 7.0, 21, range(2017, 2027)          # FS-04 2.1, 3.1, 3.3
WEEK = pd.Timedelta(days=7)


def monday(ts):
    return ts - pd.to_timedelta(ts.dt.weekday, unit="D")


def may_monday(year):
    d = dt.date(year, 5, 1)
    return pd.Timestamp(d + dt.timedelta(days=(7 - d.weekday()) % 7))


def rows_of(path, sheet=0):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[sheet] if isinstance(sheet, int) else wb[sheet]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def rebuild(target):
    p = lambda name: os.path.join(target, name)
    codes = pd.read_csv(p("container_codes.csv"), dtype=str)
    any_code = {}
    for col in ("container", "docket_code", "register_code"):
        any_code.update(dict(zip(codes[col], codes["container"])))
    prod = pd.read_csv(p("products.csv"), dtype=str, keep_default_na=False)
    type_of_sku = dict(zip(prod["sku"], prod["container"].map(any_code)))
    acc = pd.read_csv(p("trade_accounts.csv"), dtype=str, keep_default_na=False)
    now = {a: b for a, b in zip(acc["former_account_no"], acc["account_no"]) if a}

    dk = pd.read_csv(p("delivery_dockets_dec2023_nov2026.csv"), dtype=str, keep_default_na=False,
                     usecols=["docket_no", "line_no", "delivery_date", "account_no", "sku", "qty"])
    dk = dk[~dk.duplicated(["docket_no", "line_no"])]
    dk["type"] = dk["sku"].map(type_of_sku)
    dk["acct"] = dk["account_no"].map(lambda a: now.get(a, a))
    dk["qty"] = dk["qty"].astype(float)
    dk["week"] = monday(pd.to_datetime(dk["delivery_date"]))
    weekly = dk.pivot_table(index="week", columns="type", values="qty", aggfunc="sum").sort_index()
    weeks = weekly.index
    dk["line"] = np.where(dk["type"] == TAGGED, dk["acct"] + "|GUEST-20L", dk["acct"] + "|" + dk["sku"])
    line_total = dk.groupby(["type", "line"])["qty"].sum()

    wx = pd.read_csv(p("calder_vale_station_weekly.csv"))
    wx["week"] = pd.to_datetime(wx["week_beginning"])
    seen = wx.set_index("week")["mean_daily_max_c"].dropna()
    norm = wx.set_index("week")["normal_1991_2020_c"]

    counts = {}
    wb = load_workbook(p("annual_container_counts.xlsx"), read_only=True, data_only=True)
    for ws in wb.worksheets:
        rr = [list(r) for r in ws.iter_rows(values_only=True)]
        when = pd.Timestamp(dt.datetime.strptime(" ".join(str(rr[1][1]).split()[1:]), "%d %b %Y"))
        t = pd.DataFrame([r[:5] for r in rr[4:] if r[2] is not None], columns=["site", "area", "type", "state", "n"])
        t["type"] = t["type"].map(any_code)
        counts[when] = t
    dates = sorted(counts)
    last, prev = dates[-1], dates[-2]

    reg = pd.read_csv(p("container_register.csv"), dtype=str, keep_default_na=False)
    reg["type"] = reg["container"].map(any_code)
    store = pd.read_csv(p("cold_store_monday_position.csv"))
    store["type"] = store["container"].astype(str).map(any_code)
    store["day"] = pd.to_datetime(store["position_date"])
    rack = pd.read_csv(p("racking_log.csv"), dtype={"container": str})
    rack["type"] = rack["container"].map(any_code)
    rack = rack[pd.to_datetime(rack["racked_on"]) >= dates[1]]
    au = pd.read_csv(p("cellar_audits_2025_2026.csv"), dtype={"account_no": str, "container": str}, keep_default_na=False)
    au["type"] = au["container"].map(any_code)
    au["line"] = au["account_no"].map(lambda a: now.get(a, a)) + "|" + au["product"]
    au["held"] = au["full"] + au["on_dispense"] + au["empty"]
    au["week"] = monday(pd.to_datetime(au["audit_date"]))
    calls = {r[4]: int(r[6]) for r in rows_of(p("route_plan_autumn_2026.xlsx"), "Routes")[1:]}
    plan = pd.DataFrame([r[:7] for r in rows_of(p("brew_plan_2027.xlsx"))[4:] if r[0]],
                        columns=["sku", "beer", "type", "period", "first", "last", "run"])
    plan["type"] = plan["type"].map(any_code)
    sched = [r for r in rows_of(p("maplestead_supply_agreement_schedules.xlsx"), 0)[4:] if r[0]]
    volume = {r[0]: float(r[2]) for r in rows_of(p("maplestead_supply_agreement_schedules.xlsx"), 1)[3:] if r[0] and r[1]}
    names = dict(zip(codes["description"].str.split(",").str[0], codes["container"]))
    volume = {names[k]: v for k, v in volume.items() if k in names}
    estate_col = {"K50": 5, "K30": 6, "K20": 7, "FIR": 8}
    cases = pd.read_csv(p("kegtrace_cases.csv"), dtype=str, keep_default_na=False)
    cases["week"] = monday(pd.to_datetime(cases["last_delivered_on"]))
    text = subprocess.run(["pdftotext", "-layout", p("lindqvist_quotation_Q26-1187.pdf"), "-"], capture_output=True, text=True).stdout
    runs = {}
    for line in text.splitlines():
        m = re.match(r"\s*(\d)\s+(50 l keg|30 l keg|20 l keg|Firkin|Kilderkin).*?\d+\.\d\d\s+([\d,]+)\s+\d+\s*$", line)
        if m:
            runs[TYPES[int(m.group(1)) - 1]] = int(m.group(3).replace(",", ""))
    assert len(runs) == 5, "the quotation's five minimum order runs were not read: %s" % runs

    season = [may_monday(last.year + 1) + k * WEEK for k in range(SEASON_WEEKS)]
    ahead = pd.date_range(last, season[-1], freq="7D")
    out = {}
    for t in TYPES:
        y = np.log(weekly[t].to_numpy())
        n = len(y)

        def design(wk, temp, bend, level=1.0):
            pos = 2 * math.pi * (wk + pd.Timedelta(days=3)).dayofyear / 365.25
            return [level, level * (wk - weeks[0]).days / 364.0, math.cos(pos), math.sin(pos), math.cos(2 * pos),
                    math.sin(2 * pos), max(temp - bend, 0.0), min(temp - bend, 0.0)]

        def solve(bend):
            Xm = np.array([design(w, seen[w], bend) for w in weeks])
            b = np.linalg.solve(Xm.T @ Xm, Xm.T @ y)
            return float(((Xm @ b - y) ** 2).sum()), b
        bend = min(np.arange(12.0, 22.001, 0.1), key=lambda h: solve(h)[0])
        beta = solve(bend)[1]
        at = lambda wk, temp: math.exp(float(np.dot(beta, design(wk, temp, bend))))
        shape = lambda wk, temp: math.exp(float(np.dot(beta, design(wk, temp, bend, 0.0))))
        level = {d: at(d - WEEK, seen[d - WEEK]) for d in dates}
        mean_shape = float(np.mean([shape(w, norm[w]) for w in weeks[-52:]]))

        a_t = au[au["type"] == t]
        share = line_total[t].reindex(a_t["line"]).fillna(0.0).to_numpy() / float(weekly[t].sum())
        sold = share * weekly[t].reindex(a_t["week"]).to_numpy()
        gap = np.array([1.0 / calls[a.split("|")[0]] for a in a_t["line"]])
        Z = np.column_stack([np.ones(len(sold)), sold, sold * gap])
        fixed, b1, b2 = np.linalg.solve(Z.T @ Z, Z.T @ a_t["held"].to_numpy(dtype=float))
        lt = line_total[t]
        lgap = np.array([1.0 / calls[k.split("|")[0]] for k in lt.index])
        per_delivered = float(((b1 + b2 * lgap) * lt.to_numpy()).sum() / lt.sum())

        def off_site(d):
            r = reg[reg["type"] == t]
            on_reg = ((r["purchased"] < d.date().isoformat()) & ((r["condemned_on"] == "") | (r["condemned_on"] >= d.date().isoformat()))).sum()
            c = counts[d]
            return float(on_reg - c.loc[c["type"] == t, "n"].sum())
        year = weekly[t][weeks >= prev]
        if t == TAGGED:
            first_open = cases.loc[cases["outcome"] == "OPEN", "week"].min()
            w0 = first_open - 52 * WEEK
            lost_n = ((cases["week"] >= w0) & (cases["week"] < first_open) & (cases["outcome"] == "NOT TRACED")).sum()
            rate = lost_n / float(weekly[t][(weeks >= w0) & (weeks < first_open)].sum())
        else:
            rate = (off_site(last) - off_site(prev) - per_delivered * (level[last] - level[prev])) / float(year.sum())
        r = reg[reg["type"] == t]
        condemned = ((r["condemned_on"] >= prev.date().isoformat()) & (r["condemned_on"] < last.date().isoformat())).sum() / float(year.sum())

        s = store[(store["type"] == t) & (store["day"] <= last)].sort_values("day")["full_containers"].to_numpy(dtype=float)[-104:]
        half_now = rack[rack["type"] == t].groupby("sku")["containers_filled"].median().sum() / 2.0
        cover = (s.mean() - half_now) / float(weekly[t].to_numpy()[-104:].mean())
        rest = []
        for d in dates:
            c = counts[d]
            c = c[(c["type"] == t) & (c["area"] != "Cold store") & (c["state"] != "clean empty")]
            rest.append(c["n"].sum() / level[d])
        rest = float(np.mean(rest))
        on_site = float(counts[last].loc[counts[last]["type"] == t, "n"].sum())
        pl = plan[plan["type"] == t]
        lines = [(pd.Timestamp(r[3]), int(r[estate_col[t]] or 0)) for r in sched] if t in estate_col else []
        vol = volume.get(t, 0.0)

        def largest(temps):
            gone, best, parts = 0.0, None, None
            for wk in ahead[1:] if ahead[0] == last else ahead:
                temp = temps.get(wk, norm[wk])
                own = at(wk, temp)
                live = sum(k for d, k in lines if d <= wk)
                new = live * vol * shape(wk, temp) / mean_shape
                D = own + new
                rise = per_delivered * (own - level[last]) + fixed * live + (b1 + b2) * new
                on_sale = pl[(pl["first"] <= wk) & (pl["last"] >= wk)]["run"].astype(float).sum() / 2.0
                full = cover * D + on_sale
                gone += (rate + condemned) * D
                short = rise + full + rest * D + FLOAT * D - on_site + gone
                if wk in season and (best is None or short > best):
                    best, parts = short, (rise, full)
            return best, parts
        plan_case, (rise, full) = largest({})
        tens = []
        for yr in SUMMERS:
            m0 = may_monday(yr)
            tens.append(largest({season[k]: float(seen[m0 + k * WEEK]) for k in range(SEASON_WEEKS)})[0])
        out[t] = dict(plan=plan_case, hot=sorted(tens)[-2], rise=rise, store=full,
                      year_loss=rate * float(year.sum()), run=runs[t], bend=float(bend))
    return out


def cover(x, run):
    return "nothing" if x <= 0 else "hire" if x < run else "buy"


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    V = rebuild(target)
    rows = []
    inside = lambda v, band: band[0] - 1e-9 <= round(v) <= band[1] + 1e-9
    for t in TYPES:
        rows.append(("%s planning case %.0f in %s" % (t, V[t]["plan"], fig["plan_band"][t]), inside(V[t]["plan"], fig["plan_band"][t])))
        rows.append(("%s hot case %.0f in %s" % (t, V[t]["hot"], fig["hot_band"][t]), inside(V[t]["hot"], fig["hot_band"][t])))
        rows.append(("%s cover %s" % (t, cover(V[t]["plan"], V[t]["run"])), cover(V[t]["plan"], V[t]["run"]) == fig["cover"][t]))
        rows.append(("%s minimum order run %d read from the quotation" % (t, V[t]["run"]), V[t]["run"] == fig["min_run"][t]))
    c1 = sum(V[t]["rise"] for t in TYPES)
    c2 = sum(V[t]["store"] for t in TYPES)
    c3 = sum(V[t]["year_loss"] for t in TYPES if t != TAGGED)
    rows.append(("the rise at customers %.0f in %s" % (c1, fig["trade_rise_band"]), inside(c1, fig["trade_rise_band"])))
    rows.append(("the cold store %.0f in %s" % (c2, fig["store_2027_band"]), inside(c2, fig["store_2027_band"])))
    rows.append(("the year's loss %.0f in %s" % (c3, fig["year_loss_band"]), inside(c3, fig["year_loss_band"])))
    for label, good in rows:
        print("%s  %s" % ("PASS" if good else "FAIL", label))
    bad = sum(1 for _, g in rows if not g)
    print("verify: %d of %d" % (len(rows) - bad, len(rows)))
    return V, bad


if __name__ == "__main__":
    V, bad = main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    sys.exit(1 if bad else 0)
