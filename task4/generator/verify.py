"""An independent rebuild of the golden from the bundle alone, written a second way: it shares no code with
analysis.py and reads only target/ (the minimum order runs from the quotation's own text, the fleet standard's
clauses from its own text). Where the golden works on arrays by week index this works on dated tables joined by
merge_asof; the season is placed by the day of the year over 365.25 days, the bend is found on a tenth-of-a-degree
grid, the cellar relation is solved from its normal equations. It must reproduce the account at the count exactly,
file the same five covers and land every stated figure inside the band the answer blocks give.

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
DAY = pd.Timedelta(days=1)


def pdf_text(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout)


def may_monday(year):
    d = dt.date(year, 5, 1)
    return pd.Timestamp(d + dt.timedelta(days=(7 - d.weekday()) % 7))


def rows_of(path, sheet):
    wb = load_workbook(path, read_only=True, data_only=True)
    return [list(r) for r in wb[sheet].iter_rows(values_only=True)]


def strip_lot(s):
    s = str(s).upper()
    return s[2:] if s.startswith(("CC", "LF")) else s


def rebuild(target):
    p = lambda name: os.path.join(target, name)
    out = {"checks": []}
    ok = lambda label, cond, detail="": out["checks"].append((label, bool(cond), str(detail)))
    # the documents, read back through pdftotext with a positive control on the same path
    quo = pdf_text(p("lindqvist_quotation_Q26-1187.pdf"))
    std = pdf_text(p("FS-04_returnable_container_fleet_issue3.pdf"))
    form = pdf_text(p("TQ-02_cellar_quality_check.pdf"))
    ok("verify: the quotation reads back (control: its own number)", "Q26-1187" in quo and len(quo) > 500)
    runs = [int(x.replace(",", "")) for x in re.findall(r"\d+\.\d\d (\d{1,3}(?:,\d{3})?) \d{2}", quo)]
    run = dict(zip(TYPES, runs))
    ok("verify: five minimum order runs from the quotation's text", len(runs) == 5, run)
    ok("verify: FS-04 reads back with 2.1's states and 5.1's collection", "empty and awaiting collection" in std and
       "collected by the dray at its next delivery to the account" in std)
    ok("verify: TQ-02 reads back with its two count boxes", "Full in cellar" in form and "On dispense" in form)
    codes = pd.read_csv(p("container_codes.csv"), dtype=str)
    typ = {}
    for col in ("container", "docket_code", "register_code"):
        typ.update(dict(zip(codes[col], codes["container"])))
    prod = pd.read_csv(p("products.csv"), dtype=str, keep_default_na=False)
    sku_type = dict(zip(prod["sku"], prod["container"].map(typ)))
    acc = pd.read_csv(p("trade_accounts.csv"), dtype=str, keep_default_na=False)
    now = {a: b for a, b in zip(acc["former_account_no"], acc["account_no"]) if a}
    dk = pd.read_csv(p("delivery_dockets_dec2023_nov2026.csv"), dtype=str, keep_default_na=False,
                     usecols=["docket_no", "line_no", "delivery_date", "account_no", "sku", "qty"])
    dk = dk[~dk.duplicated(["docket_no", "line_no"])].copy()
    dk["type"] = dk["sku"].map(sku_type)
    dk["acct"] = dk["account_no"].map(lambda a: now.get(a, a))
    dk["qty"] = dk["qty"].astype(float)
    dk["date"] = pd.to_datetime(dk["delivery_date"])
    first = dk["date"].min()
    d0 = first - pd.Timedelta(days=first.weekday())
    dk["monday"] = d0 + pd.to_timedelta((dk["date"] - d0).dt.days // 7 * 7, unit="D")
    dk["line"] = np.where(dk["type"] == "K20", dk["acct"] + "/K20", dk["acct"] + "/" + dk["sku"])
    weekly = dk.groupby(["type", "monday"])["qty"].sum().unstack(0).sort_index()
    n_weeks = len(weekly)
    # the count and the register
    sheets = load_workbook(p("container_count_30nov2026.xlsx"), read_only=True).sheetnames
    site, tally = [], []
    for s in sheets:
        rows = rows_of(p("container_count_30nov2026.xlsx"), s)
        asof = pd.Timestamp(dt.datetime.strptime(rows[1][1][4:], "%d %b %Y"))
        for r in rows[4:]:
            if r[0] is None:
                continue
            (tally if s == "Lots" else site).append((s, r[0], r[1], r[2], r[3]))
    site = pd.DataFrame(site, columns=["sheet", "area", "code", "state", "n"])
    site["type"] = site["code"].astype(str).map(typ)
    lots_n = pd.DataFrame(tally, columns=["sheet", "code", "lot", "ring", "n"])
    lots_n["type"] = lots_n["code"].astype(str).map(typ)
    lots_n["lot"] = lots_n["lot"].map(strip_lot)
    reg = pd.read_csv(p("container_register.csv"), dtype=str, keep_default_na=False)
    reg["type"] = reg["container"].map(typ)
    reg["lot"] = reg["lot"].map(strip_lot)
    reg["bought"] = pd.to_datetime(reg["purchased"])
    reg["gone"] = pd.to_datetime(reg["condemned_on"].replace("", None))
    reg["live"] = (reg["bought"] < asof) & (reg["gone"].isna() | (reg["gone"] >= asof))
    out["asof"] = asof
    # route plan, weather, store, racking, plan, schedule
    routes = rows_of(p("route_plan_autumn_2026.xlsx"), "Routes")
    calls = {r[4]: int(r[6]) for r in routes[1:]}
    wx = pd.read_csv(p("calder_vale_station_weekly.csv"))
    wx["monday"] = pd.to_datetime(wx["week_beginning"])
    temp = dict(zip(wx["monday"], wx["mean_daily_max_c"]))
    norm = dict(zip(wx["monday"], wx["normal_1991_2020_c"]))
    store = pd.read_csv(p("cold_store_monday_position.csv"), dtype={"product": str})
    store["type"] = store["container"].map(typ)
    store["date"] = pd.to_datetime(store["position_date"])
    rk = pd.read_csv(p("racking_log.csv"), dtype={"container": str})
    rk["type"] = rk["container"].map(typ)
    rk["date"] = pd.to_datetime(rk["racked_on"])
    plan = rows_of(p("brew_plan_2027.xlsx"), "Brew plan 2027")[4:]
    plan = [(r[0], typ[r[2]], pd.Timestamp(r[4]), pd.Timestamp(r[5]), float(r[6])) for r in plan if r[0]]
    sch = rows_of(p("maplestead_supply_agreement_schedules.xlsx"), "Schedule A outlets")
    head = sch[3]
    col = {"K50": head.index("50 litre keg lines"), "K30": head.index("30 litre keg lines"),
           "K20": head.index("20 litre keg lines"), "FIR": head.index("firkin lines")}
    outlets = [r for r in sch[4:] if r[0]]
    vols = {r[0]: float(r[2]) for r in rows_of(p("maplestead_supply_agreement_schedules.xlsx"), "Schedule B volumes")[3:]
            if r[0] and isinstance(r[2], (int, float))}
    vol = {"K50": vols.get("50 litre keg", 0), "K30": vols.get("30 litre keg", 0), "K20": vols.get("20 litre keg", 0),
           "FIR": vols.get("firkin", 0), "KIL": 0.0}
    # the cellar checks, each joined to the dray's last call at its account and to four weeks of its line's dockets
    ck = pd.read_csv(p("cellar_quality_checks_2025_2026.csv"), dtype=str, keep_default_na=False)
    ck = ck[~ck.duplicated(["check_ref", "account_no", "line"])].copy()
    ck["type"] = ck["container"].map(typ)
    ck["acct"] = ck["account_no"].map(lambda a: now.get(a, a))
    ck["date"] = pd.to_datetime(ck["check_date"])
    ck["line_key"] = np.where(ck["type"] == "K20", ck["acct"] + "/K20", ck["acct"] + "/" + ck["product"])
    ck["full"] = ck["full_in_cellar"].astype(float) + ck["on_dispense"].astype(float)
    visits = dk[["acct", "date"]].drop_duplicates().sort_values("date")
    c2 = ck.sort_values("date")
    c2["before"] = c2["date"] - DAY
    j = pd.merge_asof(c2, visits.rename(columns={"date": "dray"}), left_on="before", right_on="dray", by="acct")
    j["days"] = (j["date"] - j["dray"]).dt.days.astype(float)
    ld = dk.groupby(["line", "date"])["qty"].sum().reset_index().sort_values("date")
    ld["cum"] = ld.groupby("line")["qty"].cumsum()
    j = j.sort_values("before")
    a1 = pd.merge_asof(j, ld[["line", "date", "cum"]].rename(columns={"date": "d1"}), left_on="before", right_on="d1",
                       left_by="line_key", right_by="line")
    a1["edge"] = a1["date"] - pd.Timedelta(days=29)
    a1 = a1.sort_values("edge")
    a2 = pd.merge_asof(a1, ld[["line", "date", "cum"]].rename(columns={"date": "d0", "cum": "cum0", "line": "line0"}),
                       left_on="edge", right_on="d0", left_by="line_key", right_by="line0")
    # a line's weekly sales at a check: its share of its type's deliveries over the record times the type's deliveries
    # in the week of the check (own dockets are lumpy: a line takes whole containers)
    line_tot = dk.groupby("line")["qty"].sum()
    type_tot = dk.groupby("type")["qty"].sum()
    a2["wk"] = d0 + pd.to_timedelta((a2["date"] - d0).dt.days // 7 * 7, unit="D")
    a2["rate"] = [line_tot.get(l, 0.0) / type_tot[t] * weekly[t].get(w, weekly[t].iloc[-1])
                  for l, t, w in zip(a2["line_key"], a2["type"], a2["wk"])]
    a2["iv"] = a2["acct"].map(lambda a: 0.5 if calls[a] == 2 else 1.0)
    out["n_checks"] = len(a2)
    # what the line holds: the count plus the containers sold since the dray, on the line's sales and interval
    rel, fall = {}, []
    for t in TYPES:
        x = a2[a2["type"] == t]
        X = np.column_stack([np.ones(len(x)), x["rate"], x["rate"] * x["iv"]])
        y = (x["full"] + x["rate"] * x["days"] / 7.0).to_numpy()
        rel[t] = np.linalg.solve(X.T @ X, X.T @ y)
    out["rel"] = rel
    # the lots: a weighted line through log(found on site / on the register) against the lot's age
    lots = {}
    for t in TYPES:
        r = reg[(reg["type"] == t)]
        g = r.groupby("lot").agg(reg_n=("live", "sum"), age=("bought", lambda s: ((asof - s).dt.days / 365.25).mean()))
        g["found"] = lots_n[lots_n["type"] == t].groupby("lot")["n"].sum().reindex(g.index).fillna(0.0)
        g = g[g["found"] > 0]
        w = g["found"].to_numpy()
        A = np.column_stack([np.ones(len(g)), g["age"].to_numpy()])
        coef = np.linalg.solve(A.T @ (A * w[:, None]), A.T @ (w * np.log(g["found"] / g["reg_n"]).to_numpy()))
        lam = -coef[1]
        alive = float((r.groupby("lot")["live"].sum().reindex(g.index) * np.exp(-lam * g["age"])).sum())
        lots[t] = dict(lam=lam, alive=alive, loss=alive * (math.exp(lam) - 1.0))
    out["lots"] = lots
    # the cold store, beer by beer: each beer's mean Monday stock over the last 104 Mondays on its mean weekly
    # deliveries (one cover) and its median racking run (one share), no intercept
    last104 = sorted(store["date"].unique())[-104:]
    sb = store[store["date"].isin(last104)].groupby("product")["full_containers"].mean()
    recent = rk[rk["date"] >= d0 + pd.Timedelta(days=364)]
    runs_b = recent.groupby("sku")["containers_filled"].median()
    dkw = dk[(dk["monday"] >= pd.Timestamp(last104[0]) - pd.Timedelta(days=7)) &
             (dk["monday"] < pd.Timestamp(last104[-1]))].groupby("sku")["qty"].sum() / 104.0
    beers = sorted(runs_b.index)
    Xs = np.column_stack([[dkw.get(s, 0.0) for s in beers], [runs_b[s] for s in beers]])
    cs, th = np.linalg.lstsq(Xs, np.array([sb.get(s, 0.0) for s in beers]), rcond=None)[0]
    out["store_cover"], out["store_share"] = float(cs), float(th)
    ok("verify: the run share measured between beers", 0.3 < th < 0.7, "%.3f on %d beers, cover %.3f" % (th, len(beers), cs))
    # the 2027 weeks
    season = [may_monday(asof.year + 1) + pd.Timedelta(days=7 * k) for k in range(21)]
    weeks27 = pd.date_range(asof, season[-1], freq="7D")
    res = {}
    for t in TYPES:
        fl = weekly[t].to_numpy()
        mondays = weekly.index
        tt = np.array([temp[m] for m in mondays])
        idx = np.arange(n_weeks)

        def design(ix, mons, tv, h0, lev=1.0):
            ang = np.array([2 * math.pi * ((m + pd.Timedelta(days=3)).dayofyear) / 365.25 for m in mons])
            cols = [np.full(len(ix), lev), lev * ix / 52.0, np.cos(ang), np.sin(ang), np.cos(2 * ang), np.sin(2 * ang),
                    np.maximum(tv - h0, 0.0), np.minimum(tv - h0, 0.0)]
            return np.column_stack(cols)
        best = None
        for h0 in np.arange(12.0, 22.001, 0.1):
            X = design(idx, mondays, tt, h0)
            b = np.linalg.lstsq(X, np.log(fl), rcond=None)[0]
            e = float(((X @ b - np.log(fl)) ** 2).sum())
            if best is None or e < best[0]:
                best = (e, h0, b)
        _, h0, b = best
        yr_shape = float(np.mean(np.exp(design(idx[-52:], mondays[-52:], np.array([norm[m] for m in mondays[-52:]]), h0,
                                              0.0) @ b)))
        a, b1, b2 = rel[t]
        lines = pd.read_csv(p("dispense_lines.csv"), dtype=str)
        lines = lines[lines["container"].map(typ) == t]
        keys = np.where(t == "K20", lines["account_no"] + "/K20", lines["account_no"] + "/" + lines["product"])
        tot = dk[dk["type"] == t].groupby("line")["qty"].sum().reindex(keys).fillna(0.0).to_numpy()
        iv = lines["account_no"].map(lambda x: 0.5 if calls[x] == 2 else 1.0).to_numpy()
        per_sale = float(((b1 + b2 * iv) * tot).sum() / tot.sum())        # per container delivered a week, weighted
        b_est = (b1 + b2) / 2.0
        lev = float(np.exp(design(idx[-1:], mondays[-1:], tt[-1:], h0) @ b)[0])   # the fit's value for the count's week
        on_site = float(site[site["type"] == t]["n"].sum())
        other = float(site[(site["type"] == t) & (site["area"] != "Cold store") & (site["state"] != "clean empty")]["n"].sum())
        cover, theta = out["store_cover"], out["store_share"]
        loss = lots[t]["loss"] / float(fl[-52:].sum())
        cond = float(((reg["type"] == t) & (reg["gone"] >= d0 + pd.Timedelta(days=7 * (n_weeks - 52))) &
                      (reg["gone"] < asof)).sum()) / float(fl[-52:].sum())
        ix27 = np.array([(m - d0).days // 7 for m in weeks27])

        def path(tv27):
            F = np.exp(design(ix27, weeks27, tv27, h0) @ b)
            shape = np.exp(design(ix27, weeks27, tv27, h0, 0.0) @ b) / yr_shape
            live = np.array([sum(int(r[col[t]] or 0) for r in outlets if pd.Timestamp(r[3]) <= m) if t in col else 0
                             for m in weeks27])
            es = live * vol[t] * shape
            D = F + es
            swing = per_sale * (F - lev) + a * live + b_est * 2.0 * es
            runs_on = np.array([sum(rn for s, ty, f0, l0, rn in plan if ty == t and f0 <= m <= l0) for m in weeks27])
            store27 = cover * D + theta * runs_on
            drain = np.cumsum((loss + cond) * D)
            short = swing + store27 + other / lev * D + D * 2.0 / 7.0 - on_site + drain
            ins = np.isin(weeks27, season)
            return short[ins].max(), swing[ins].max(), store27[ins].max()
        plan_v, rise, full27 = path(np.array([norm[m] for m in weeks27]))
        hots = []
        for y in range(2017, 2027):
            m0 = may_monday(y)
            tv = np.array([norm[m] for m in weeks27])
            for k_, m in enumerate(weeks27):
                if m in season:
                    tv[k_] = temp[m0 + pd.Timedelta(days=7 * season.index(m))]
            hots.append(path(tv)[0])
        res[t] = dict(plan=plan_v, hot=sorted(hots)[-2], rise=rise, full=full27, loss=lots[t]["loss"], hinge=h0,
                      register=int(reg[(reg["type"] == t) & reg["live"]].shape[0]), on_site=int(on_site),
                      cover=("nothing" if plan_v <= 0 else "hire" if plan_v < run[t] else "buy"))
    out["res"] = res
    return out


def main(target):
    out = rebuild(target)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    chk = out["checks"]
    ok = lambda label, cond, detail="": chk.append((label, bool(cond), str(detail)))
    res = out["res"]
    for t in TYPES:
        r = res[t]
        ok("verify: %s account at the count exactly" % t, r["register"] == fig["account"][t]["register"] and
           r["on_site"] == fig["account"][t]["on_site"], (r["register"], r["on_site"]))
        ok("verify: %s cover" % t, r["cover"] == fig["cover"][t], "%s against %s" % (r["cover"], fig["cover"][t]))
        lo, hi = fig["plan_band"][t]
        ok("verify: %s planning case inside its band" % t, lo <= r["plan"] <= hi, "%.0f in [%d, %d]" % (r["plan"], lo, hi))
        lo, hi = fig["hot_band"][t]
        ok("verify: %s hot case inside its band" % t, lo <= r["hot"] <= hi, "%.0f in [%d, %d]" % (r["hot"], lo, hi))
    for key, field in (("trade_rise", "rise"), ("store_2027", "full"), ("year_loss", "loss")):
        for t in TYPES:
            lo, hi = fig[key + "_band_by_pool"][t]
            ok("verify: %s %s inside its band" % (t, key), lo <= res[t][field] <= hi,
               "%.0f in [%d, %d]" % (res[t][field], lo, hi))
    for key, field in (("trade_rise", "rise"), ("store_2027", "full"), ("year_loss", "loss")):
        v = sum(res[t][field] for t in TYPES)
        lo, hi = fig[key + "_band"]
        ok("verify: %s inside its band" % key, lo <= v <= hi, "%.0f in [%d, %d]" % (v, lo, hi))
    ok("verify: line checks used", out["n_checks"] == fig["counts"]["checks"], out["n_checks"])
    bad = [c for c in chk if not c[1]]
    for label, good, detail in chk:
        print("%s  %-58s %s" % ("PASS" if good else "FAIL", label, detail))
    print("verify: %d of %d PASS" % (len(chk) - len(bad), len(chk)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
