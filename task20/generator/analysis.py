"""The golden, computed from target/ alone: each process is recovered from its own record (NEX's rate rule from the
notices and settlement prices, the desk's rule from the trade capture, the plants from the hydrology and plant
output, the affiliate's price and every customer's payment habit from the sales ledger), then the liquidity
standard's stress year is replayed on the 2027 book. Also every hurried route, the rivals and the 2022 check."""
import csv
import datetime as dt
import math
import os
import re
import subprocess
from collections import defaultdict

import numpy as np
from docx import Document
from openpyxl import load_workbook

import common as C
import replay as RP
from common import mi, mi_date, month_hours, hours_year, year_months, cprice

D = dt.date.fromisoformat
CLS = {"Base Month": "M", "Base Quarter": "Q", "Base Year": "Y"}
CUSTOMERS = {"Fjordal Aluminium AS": "SMELTER", "Nesbyen Treforedling AS": "PULP", "Hallingvass Straum AS": "AFFILIATE",
             "Bygdenett AS": "GRID"}


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def pdftext(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


# ------------------------------------------------------------------------------------------------------ loading
def load(tgt):
    P = lambda f: os.path.join(tgt, f)
    Dd = {}
    # settlement prices: one row per (day, delivery period), duplicates dropped
    sp = defaultdict(dict)
    for r in rows(P("nex_daily_settlement_2018_2026.csv")):
        s, e = D(r["delivery_start"]), D(r["delivery_end"])
        ks = list(range(mi(s.year, s.month), mi(e.year, e.month) + 1))
        sp[D(r["trade_date"])][(r["product"], ks[0], len(ks))] = float(r["settlement_eur_mwh"])
    Dd["settle"] = dict(sp)
    Dd["sdays"] = sorted(sp)
    # the risk system's curve
    cv = defaultdict(dict)
    for r in rows(P("hk_risk_curve_daily_2018_2026.csv")):
        if r["curve_id"] != "HK_SYS":
            continue
        y, m = map(int, r["delivery_month"].split("-"))
        cv[D(r["as_of"])][mi(y, m)] = float(r["forward_eur_mwh"])
    Dd["curve"] = dict(cv)
    # notices
    Dd["notices"] = [(D(r["effective_date"]), CLS[r["product_class"]], float(r["margin_eur_per_mwh"]))
                     for r in rows(P("nex_margin_parameters_2018_2026.csv"))]
    # statements (the restated line replaces the superseded one)
    st = {}
    for r in rows(P("nex_clearing_statements_2018_2026.csv")):
        if r["status"] == "superseded":
            continue
        st[D(r["statement_date"])] = {k: float(r[k]) for k in ("variation_margin", "delivery_settlement",
                                                               "initial_margin_requirement", "initial_margin_change",
                                                               "net_cash_to_nex")}
    Dd["stmt"] = st
    # month-end positions, spread to delivery months
    pos = defaultdict(dict)
    for r in rows(P("nex_positions_month_end_2017_2026.csv")):
        s, e = D(r["delivery_start"]), D(r["delivery_end"])
        for k in range(mi(s.year, s.month), mi(e.year, e.month) + 1):
            pos[D(r["month_end"])][k] = pos[D(r["month_end"])].get(k, 0.0) + float(r["position_mw"])
    Dd["pos"] = dict(pos)
    # trade capture: the last state of each trade; cancelled trades out, rebooked ones in
    tr = {}
    for r in rows(P("hk_trade_capture_2018_2026.csv")):
        tid = r["trade_id"]
        if r["status"] == "CANCEL":
            tr.pop(tid, None)
            continue
        con = r["contract"]
        y = int(con[5:]) if con.startswith("NSBY ") else 2000 + int(con[-2:])
        q = float(r["quantity"])
        mw = q / hours_year(y) if r["unit"] == "MWh" else q
        tr[tid] = (D(r["trade_date"]), y, -mw if r["side"] == "SELL" else mw, float(r["price_eur_mwh"]))
    Dd["trades"] = sorted(tr.values())
    # hydrology
    hy = []
    for r in rows(P("hk_hydrology_weekly_2017_2026.csv")):
        hy.append(dict(week=D(r["week_start"]), iso=r["iso_week"], inflow=float(r["inflow_gwh"]) if r["inflow_gwh"] else None,
                       storage=float(r["storage_gwh"]), normal_inflow=float(r["normal_inflow_gwh"]),
                       normal_pct=float(r["normal_storage_pct"]), pct=float(r["storage_pct"])))
    Dd["hydro"] = hy
    # plant output
    po = defaultdict(lambda: defaultdict(float))
    for r in rows(P("hk_plant_output_monthly_2017_2026.csv")):
        y, m = map(int, r["month"].split("-"))
        po[mi(y, m)][r["plant_type"]] += float(r["output_mwh"])
    Dd["plant"] = {k: dict(v) for k, v in po.items()}
    # sales ledger
    led = []
    for r in rows(P("hk_sales_ledger_2018_2026.csv")):
        led.append(r)
    Dd["ledger"] = led
    # day-ahead (system price for every calendar day)
    da, spot = {}, {}
    for r in rows(P("nex_dayahead_settlements_2018_2026.csv")):
        c = D(r["delivery_date"])
        spot[c] = float(r["system_price_eur_mwh"])
        da[c] = (float(r["sold_mwh"]) - float(r["bought_mwh"]), float(r["net_amount_eur"]), D(r["settlement_date"]))
    Dd["da"], Dd["spot"] = da, spot
    # budgets
    wb = load_workbook(P("hk_budget_vintages_2016_2026.xlsx"), data_only=True)
    bud = []
    for r in list(wb["Budget vintages"].iter_rows(values_only=True))[1:]:
        s = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
        bud.append((s, int(r[1]), float(r[2]), float(r[3]) * 1e3))
    Dd["bud"] = bud
    # supply contracts and profiles
    wb = load_workbook(P("hk_supply_contracts_register.xlsx"), data_only=True)
    reg = list(wb["Supply contracts"].iter_rows(values_only=True))[1:]
    Dd["register"] = reg
    prof = list(wb["Profiles"].iter_rows(values_only=True))[1:]
    Dd["retail_prof"] = [float(r[1]) for r in prof]
    Dd["loss_prof"] = [float(r[2]) for r in prof]
    # policy ladder
    doc = Document(P("hk_hedging_policy_2025.docx"))
    lad = []
    for row in doc.tables[0].rows[1:]:
        c = [x.text for x in row.cells]
        tau = 0.0 if "started" in c[0] else int(re.match(r"(\d+)", c[0]).group(1)) / 12.0
        lad.append((tau, int(re.match(r"(\d+)", c[1]).group(1)) / 100.0, int(re.match(r"(\d+)", c[2]).group(1)) / 100.0))
    Dd["ladder"] = sorted(lad)
    lic = pdftext(P("hallingvass_regulation_licence_extract.pdf"))
    Dd["floor"] = float(re.search(r"below\s+([\d,]+)\s+GWh", lic).group(1).replace(",", ""))
    Dd["capacity"] = float(re.search(r"hold\s+([\d,]+)\s+GWh", lic).group(1).replace(",", ""))
    std = pdftext(P("hk_liquidity_standard_2026.pdf"))
    Dd["rounding"] = float(re.search(r"next EUR\s+(\d+)\s+million", std).group(1)) * 1e6
    Dd["facility_2026"] = float(re.search(r"committed for 2026 is EUR\s+(\d+)\s+million", std).group(1)) * 1e6
    return Dd


# ------------------------------------------------------------------------------------------------------ prices
def front_price_series(Dd, days):
    """front contract settlement price per class per day, and the same contract's daily log return."""
    px = {t: np.zeros(len(days)) for t in "MQY"}
    ret = {t: np.zeros(len(days)) for t in "MQY"}
    prevmap = None
    for i, d in enumerate(days):
        fm = C.front_months(d)
        today = Dd["settle"][d]
        for t, name in (("M", "Base Month"), ("Q", "Base Quarter"), ("Y", "Base Year")):
            key = (name, fm[t][0], len(fm[t]))
            px[t][i] = today[key]
            if prevmap is not None and key in prevmap:
                ret[t][i] = math.log(today[key] / prevmap[key])
        prevmap = today
    return px, ret


def rate_series_from_notices(Dd, days):
    out = {t: np.zeros(len(days)) for t in "MQY"}
    nts = sorted(Dd["notices"])
    for t in "MQY":
        cur, j, lst = None, 0, [x for x in nts if x[1] == t]
        for i, d in enumerate(days):
            while j < len(lst) and lst[j][0] <= d:
                cur = lst[j][2]
                j += 1
            out[t][i] = cur
    return out


def infer_rule(Dd):
    """the look-back, quantile, tolerance and review day that reproduce every notice from the settlement prices."""
    days = [d for d in Dd["sdays"] if d >= dt.date(2018, 1, 2)]
    px, ret = front_price_series(Dd, days)
    eff = [x for x in Dd["notices"] if x[0] > dt.date(2018, 1, 2)]
    wds = [d.weekday() for d, t, r in eff]
    review_wd = (max(set(wds), key=wds.count) - 1) % 7
    changes = []
    for t in "MQY":
        lst = sorted(x for x in Dd["notices"] if x[1] == t)
        changes += [abs(b[2] / a[2] - 1) for a, b in zip(lst, lst[1:])]
    # the smallest change, read through the two-decimal rounding of published rates
    band = max(b for b in (0.05, 0.10, 0.15, 0.20) if b <= min(changes) + 0.006)
    obs = rate_series_from_notices(Dd, days)
    best = None
    for look in (60, 120, 125, 250, 252, 500):
        for q in (0.95, 0.975, 0.98, 0.985, 0.99, 0.995):
            start = {t: obs[t][0] for t in "MQY"}
            r, _ = C.rule_rates(days, px, ret, look, q, band, review_wd, start)
            # compare from the second year, once the window is full of the file's own days
            sel = slice(260, None)
            err = sum(float(np.mean(np.abs(r[t][sel] / obs[t][sel] - 1))) for t in "MQY")
            if best is None or err < best[0]:
                best = (err, look, q)
    start = {t: obs[t][0] for t in "MQY"}
    _, sim = C.rule_rates(days, px, ret, best[1], best[2], band, review_wd, start)
    act = {(d, t): r for d, t, r in Dd["notices"] if d >= dt.date(2019, 1, 1)}
    got = {(d, t): r for d, t, r in sim if d >= dt.date(2019, 1, 1)}
    match = sum(1 for k, r in act.items() if k in got and abs(got[k] - r) < 0.006)
    return dict(look=best[1], q=best[2], band=band, review_wd=review_wd, fit_error=best[0], match=match,
                notices=len(act), extra=len(set(got) - set(act)))


# ------------------------------------------------------------------------------------------------------ the desk
def budget_fns(bud):
    def px(d, y):
        return max(((s, p) for (s, yy, p, g) in bud if yy == y and s <= d), key=lambda x: x[0])[1]

    def gen(d, y):
        return max(((s, g) for (s, yy, p, g) in bud if yy == y and s <= d), key=lambda x: x[0])[1]
    return px, gen


def smelter(Dd):
    r = next(x for x in Dd["register"] if x[0] == "Fjordal Aluminium AS")
    mw = float(re.match(r"([\d.]+)\s*MW", r[4]).group(1))
    price = float(re.search(r"EUR\s+([\d.]+)", r[5]).group(1))
    y0 = (r[2].date() if isinstance(r[2], dt.datetime) else r[2]).year
    y1 = (r[3].date() if isinstance(r[3], dt.datetime) else r[3]).year
    return mw, price, y0, y1


def fixed_phys_fn(Dd, count=True):
    mw, price, y0, y1 = smelter(Dd)
    return (lambda y: mw * hours_year(y) if (count and y0 <= y <= y1) else 0.0)


def curves_by_day(Dd, days):
    return [Dd["curve"][d] for d in days]


def desk_history(Dd, theta, speed, rule="step", count=True):
    """replays a candidate desk rule over 2018 to 2026 from the end-2017 book and returns its sales by week and year."""
    days = [d for d in Dd["sdays"] if d >= dt.date(2018, 1, 2)]
    bpx, bgen = budget_fns(Dd["bud"])
    mw = {k: v for k, v in Dd["pos"][max(x for x in Dd["pos"] if x.year == 2017)].items()}
    desk = C.make_desk(Dd["ladder"], bpx, bgen, fixed_phys_fn(Dd, count), rule, theta, speed)
    sales = defaultdict(float)
    for i, d in enumerate(days):
        curve = Dd["curve"][d]
        add = desk(i, d, curve, mw)
        for k, dm in add.items():
            mw[k] = mw.get(k, 0.0) + dm
        for y in {mi_date(k).year for k in add}:
            sales[(d, y)] += -add[year_months(y)[0]]
        for k in [k for k in mw if mi_date(k + 1) <= d]:
            mw.pop(k)
    return dict(sales)


def actual_sales(Dd):
    s = defaultdict(float)
    for d, y, mw, px in Dd["trades"]:
        s[(d, y)] += -mw
    return dict(s)


def infer_desk(Dd):
    act = actual_sales(Dd)
    res = []
    for th in [1.10 + 0.01 * j for j in range(31)]:
        for sp in (0.02, 0.025, 0.03, 0.035, 0.04):
            sim = desk_history(Dd, math.log(th), sp)
            keys = set(act) | set(sim)
            err = sum(abs(act.get(k, 0.0) - sim.get(k, 0.0)) for k in keys)
            res.append((err, th, sp))
    res.sort()
    best = res[0][0]
    ok = [r for r in res if r[0] <= best + 1e-6]
    ths = sorted(r[1] for r in ok)
    sp = ok[0][2]
    # without the smelter's contract in the ratio no threshold reproduces the sales
    alt = min(sum(abs(act.get(k, 0.0) - v.get(k, 0.0)) for k in set(act) | set(v))
              for v in [desk_history(Dd, math.log(t), sp, count=False) for t in (1.15, 1.25, 1.35)])
    return dict(theta_lo=ths[0], theta_hi=ths[-1], theta=0.5 * (ths[0] + ths[-1]), speed=sp, err=best,
                err_without_smelter=alt, total_mw=sum(act.values()))


# ------------------------------------------------------------------------------------------------------ the plants
def weeks_by_iso(Dd):
    return {(h["week"].isocalendar()[0], h["week"].isocalendar()[1]): h for h in Dd["hydro"]}


def infer_plants(Dd):
    """run-of-river share and cap from the run-of-river plants' monthly output; the reservoir plants' release policy
    from the weekly storage balance against the normal storage curve; the floor from the licence."""
    hy = Dd["hydro"]
    best = None
    for s in [0.20 + 0.005 * j for j in range(25)]:
        for cap in range(40, 85, 5):
            ror = defaultdict(float)
            bad = set()
            for h in hy:
                for dd in range(7):
                    c = h["week"] + dt.timedelta(days=dd)
                    k = mi(c.year, c.month)
                    if h["inflow"] is None:
                        bad.add(k)
                        continue
                    ror[k] += min(s * h["inflow"], cap) / 7.0 * 1000.0
            err = sum((ror[k] - v.get("run-of-river", 0.0)) ** 2 for k, v in Dd["plant"].items()
                      if k in ror and k not in bad and k >= mi(2017, 2))
            if best is None or err < best[0]:
                best = (err, s, cap)
    s, cap = best[1], best[2]
    capacity = Dd["capacity"]
    guide = {}
    for h in hy:
        n = min(h["week"].isocalendar()[1], 52)
        guide[n] = h["normal_pct"] / 100.0 * capacity
    ninfl = {}
    for h in hy:
        ninfl[min(h["week"].isocalendar()[1], 52)] = h["normal_inflow"]
    plan = {}
    for n in range(1, 53):
        prev = guide[n - 1] if n > 1 else guide[52]
        plan[n] = (1 - s) * ninfl[n] - (guide[n] - prev)
    # release by week from the storage balance, and its response to storage against normal
    xs, ys = [], []
    for a, b in zip(hy, hy[1:]):
        if b["inflow"] is None or b["storage"] >= capacity - 0.5 or b["storage"] <= Dd["floor"] + 0.5:
            continue
        n = min(b["week"].isocalendar()[1], 52)
        rel = a["storage"] + (1 - s) * b["inflow"] - b["storage"]
        xs.append(a["storage"] / guide[n] - 1)
        ys.append(rel / plan[n])
    xs, ys = np.array(xs), np.array(ys)
    hi = float(np.max(ys))
    inner = ys < hi - 0.01
    # release falls in a straight line with storage below normal; the licence floor is the only lower limit
    slope = float(np.sum(xs[inner] * (ys[inner] - 1)) / np.sum(xs[inner] ** 2))
    lo = 0.0
    return dict(ror_share=s, ror_cap=cap, plan=plan, guide=guide, slope=slope, lo=lo, hi=hi, floor=Dd["floor"],
                capacity=capacity, normal_inflow=ninfl)


def plant_run(pm, inflow, lev0, wnum):
    lev = lev0
    out, levs = [], []
    for infl, n in zip(inflow, wnum):
        ror = min(pm["ror_share"] * infl, pm["ror_cap"])
        to_res = (1 - pm["ror_share"]) * infl
        mult = min(max(1 + pm["slope"] * (lev / pm["guide"][n] - 1), pm["lo"]), pm["hi"])
        rel = min(pm["plan"][n] * mult, max(0.0, lev + to_res - pm["floor"]))
        lev = min(lev + to_res - rel, pm["capacity"])
        out.append(ror + rel)
        levs.append(lev)
    return np.array(out), np.array(levs)


# ------------------------------------------------------------------------------------------------------ customers
def monthly_spot(spot):
    acc = defaultdict(list)
    for c, v in spot.items():
        acc[mi(c.year, c.month)].append(v)
    return {k: float(np.mean(v)) for k, v in acc.items()}


def invoices_of(Dd, cu_key):
    out = []
    for r in Dd["ledger"]:
        if r["doc_type"] != "INV" or CUSTOMERS[r["customer"]] != cu_key:
            continue
        y, m = map(int, r["period"].split("-"))
        out.append(dict(k=mi(y, m), px=float(r["price_eur_mwh"]), mwh=float(r["mwh"]), amt=float(r["amount_eur"]),
                        doc=D(r["doc_date"]), paid=D(r["paid_date"]) if r["paid_date"] else None))
    return out


def infer_affiliate(Dd):
    spm = monthly_spot(Dd["spot"])
    inv = [x for x in invoices_of(Dd, "AFFILIATE") if x["k"] >= mi(2019, 3)]
    best = None
    k0 = min(spm)
    for win in range(1, 25):
        for lag in range(0, 5):
            use = [i for i in inv if i["k"] - lag - win + 1 >= k0]
            if len(use) < 36:
                continue
            err = max(abs(np.mean([spm[x] for x in range(i["k"] - lag - win + 1, i["k"] - lag + 1)]) - i["px"]) for i in use)
            if best is None or err < best[0]:
                best = (err, win, lag)
    spot_err = max(abs(spm[i["k"]] - i["px"]) / i["px"] for i in inv)
    return dict(window=best[1], lag=best[2], max_abs_err=best[0], spot_max_rel_err=spot_err)


def infer_lags(Dd):
    out = {}
    for cu in ("SMELTER", "PULP", "AFFILIATE", "GRID"):
        d = [(i["paid"] - i["doc"]).days for i in invoices_of(Dd, cu) if i["paid"]]
        out[cu] = float(np.median(d))
    return out


def committed_fn(Dd):
    mw_s = smelter(Dd)[0]
    pulp = next(x for x in Dd["register"] if x[0] == "Nesbyen Treforedling AS")
    mw_p = float(re.match(r"([\d.]+)\s*MW", pulp[4]).group(1))
    aff = next(x for x in Dd["register"] if x[0] == "Hallingvass Straum AS")
    gwh_a = float(re.match(r"([\d,.]+)\s*GWh", aff[4]).group(1).replace(",", ""))
    grid = next(x for x in Dd["register"] if x[0] == "Bygdenett AS")
    gwh_g = float(re.search(r"([\d,.]+)\s*GWh", grid[4]).group(1).replace(",", ""))
    rp, lp = Dd["retail_prof"], Dd["loss_prof"]

    def com(k):
        h, m = month_hours(k), k % 12
        return {"SMELTER": mw_s * h, "PULP": mw_p * h, "AFFILIATE": gwh_a * 1e3 * rp[m], "GRID": gwh_g * 1e3 * lp[m]}
    return com


def invoice_day(k):
    d, cnt = mi_date(k + 1), 0
    while True:
        if C.is_bday(d):
            cnt += 1
            if cnt == 3:
                return d
        d += dt.timedelta(days=1)


def pay_day(doc, lag):
    d = doc + dt.timedelta(days=int(round(lag)))
    while not C.is_bday(d):
        d += dt.timedelta(days=1)
    return d


# ------------------------------------------------------------------------------------------------------ the replay
def opening(Dd, rule, lags, aff, year_end=dt.date(2026, 12, 30)):
    """the state the stress year starts from, read from the records."""
    days = [d for d in Dd["sdays"] if dt.date(2018, 1, 2) <= d <= year_end]
    px, ret = front_price_series(Dd, days)
    obs = rate_series_from_notices(Dd, days)
    _, ret_full = front_price_series(Dd, days)
    hist_two = {t: list(ret[t] + np.concatenate([[0.0], ret[t][:-1]])) for t in "MQY"}
    mw = dict(Dd["pos"][year_end])
    f_last = {}
    for k in mw:
        s = mi_date(k)
        if s <= year_end:
            ltd = C.prev_bday(s)
            f_last[k] = Dd["settle"][ltd][("Base Month", k, 1)]
    st = Dd["stmt"][year_end]
    hyd = Dd["hydro"][-1]
    # receivables still open at the year end, paid on each customer's habit
    rec_open = []
    for r in Dd["ledger"]:
        if r["doc_type"] != "INV" or r["paid_date"]:
            continue
        cu = CUSTOMERS[r["customer"]]
        pay = pay_day(D(r["doc_date"]), lags[cu])
        rec_open.append((pay, float(r["amount_eur"])))
    return dict(mw=mw, open_curve=Dd["curve"][year_end], im0=st["initial_margin_requirement"], f_last=f_last,
                spot_hist={c: v for c, v in Dd["spot"].items() if c <= dt.date(2026, 12, 31)},
                rates_in_force={t: float(obs[t][-1]) for t in "MQY"}, hist_two=hist_two,
                last1={t: float(ret[t][-1]) for t in "MQY"}, level=hyd["storage"], last_week=hyd,
                rec_open=rec_open, spot_m=monthly_spot({c: v for c, v in Dd["spot"].items() if c <= dt.date(2026, 12, 31)}),
                ref_ret_hist=ret, ref_px_hist=px, rates_hist=obs, days_hist=days)


def stress_prices(Dd):
    bd22 = sorted(d for d in Dd["curve"] if d.year == 2022 or d == dt.date(2021, 12, 30))
    curves22 = {d: Dd["curve"][d] for d in bd22}
    spot22 = {c: v for c, v in Dd["spot"].items() if c.year == 2022}
    return RP.stress_prices(Dd["curve"][dt.date(2026, 12, 30)], curves22, spot22, bd22)


def models(Dd, P, desk_rule="step", rates_kind="rule", out_kind="res", aff_kind="formula", count_phys=True,
           rec_kind="habit", beta=0.30, theta=None, speed=None, year=2027):
    rule, desk_p, pm, aff, lags = P["rule"], P["desk"], P["plants"], P["aff"], P["lags"]
    com = committed_fn(Dd)

    def rates(days, curves, st):
        px, ret = C.ref_series(days, curves, st["open_curve"])
        if rates_kind == "rule":
            r, _ = C.rule_rates(days, px, ret, rule["look"], rule["q"], rule["band"], rule["review_wd"],
                                st["rates_in_force"], st["hist_two"], st["last1"])
            return r
        if rates_kind == "const":
            return {t: np.full(len(days), st["rates_in_force"][t]) for t in "MQY"}
        if rates_kind == "price":
            p0 = {t: st["ref_px_hist"][t][-1] for t in "MQY"}
            return {t: st["rates_in_force"][t] * px[t] / p0[t] for t in "MQY"}
        if rates_kind == "pct2022":
            hd = st["days_hist"]
            idx = {d: i for i, d in enumerate(hd)}
            out = {}
            for t in "MQY":
                ser = []
                for d in days:
                    c22 = RP.corresponding_2022(d, set(hd))
                    i22 = idx[c22]
                    ser.append(px[t][len(ser)] * st["rates_hist"][t][i22] / st["ref_px_hist"][t][i22])
                out[t] = np.array(ser)
            return out
        if rates_kind == "ewma":
            out = {}
            for t in "MQY":
                rh, ph, oh = st["ref_ret_hist"][t], st["ref_px_hist"][t], st["rates_hist"][t]
                v = float(np.var(rh[:60]))
                sig = []
                for x in rh:
                    v = 0.94 * v + 0.06 * x ** 2
                    sig.append(math.sqrt(v))
                sig = np.array(sig)
                kfit = float(np.exp(np.mean(np.log(oh[250:] / (sig[250:] * ph[250:])))))
                v = sig[-1] ** 2
                ser = []
                for j in range(len(days)):
                    v = 0.94 * v + 0.06 * ret[t][j] ** 2
                    ser.append(kfit * math.sqrt(v) * px[t][j])
                out[t] = np.array(ser)
            return out
        raise ValueError(rates_kind)

    def desk(days, curves, st):
        bud = [b for b in Dd["bud"] if b[0] < dt.date(year, 1, 1)]
        # the October budget of the stress year, set the way the vintages show: forward of the three months before
        oct1 = dt.date(year, 10, 1)
        idx = [j for j, d in enumerate(days) if d < oct1][-60:]
        set_on = next(d for d in days if d >= oct1)
        for y in range(year + 1, year + 5):
            ks = year_months(y)
            vals = [cprice(curves[j], ks) for j in idx if all(k in curves[j] for k in ks)]
            if vals:
                bud.append((set_on, y, round(P["budget_margin"] * float(np.mean(vals)), 2),
                            max(g for (s, yy, p, g) in bud if yy == max(x[1] for x in bud))))
        bpx, bgen = budget_fns(bud)
        th = math.log(theta if theta else desk_p["theta"])
        return C.make_desk(Dd["ladder"], bpx, bgen, fixed_phys_fn(Dd, count_phys), desk_rule, th,
                           speed or desk_p["speed"], beta)

    def supply(days, curves, spot_all, st):
        # output: the stress inflows through the plants from the year-end storage
        hy22 = {h["week"].isocalendar()[1]: h for h in Dd["hydro"] if h["week"].isocalendar()[0] == 2022}
        weeks, infl = RP.stress_inflows(lambda n: pm["normal_inflow"][min(n, 52)],
                                        {n: h["inflow"] for n, h in hy22.items()},
                                        {n: h["normal_inflow"] for n, h in hy22.items()}, year=year)
        wn = [min(w.isocalendar()[1], 52) for w in weeks]
        lw = st["last_week"]
        prev = Dd["hydro"][-2]
        last_rel = prev["storage"] + (1 - pm["ror_share"]) * lw["inflow"] - lw["storage"]
        last_out = min(pm["ror_share"] * lw["inflow"], pm["ror_cap"]) + last_rel
        if out_kind == "res":
            outw, _ = plant_run(pm, infl, st["level"], wn)
        else:
            norm = np.array([pm["normal_inflow"][n] for n in wn])
            nout = np.array([min(pm["ror_share"] * x, pm["ror_cap"]) + pm["plan"][n] for x, n in zip(norm, wn)])
            if out_kind == "budget":
                outw = nout
            elif out_kind == "inflow":
                outw = nout * infl / norm
            elif out_kind == "ratio22":
                # 2022's output against the normal week, carried to 2027
                o22 = {}
                for a, b in zip(Dd["hydro"], Dd["hydro"][1:]):
                    if b["week"].isocalendar()[0] == 2022:
                        n = b["week"].isocalendar()[1]
                        o22[n] = min(pm["ror_share"] * b["inflow"], pm["ror_cap"]) + (a["storage"] + (1 - pm["ror_share"]) * b["inflow"] - b["storage"])
                outw = np.array([nout[i] * o22[n] / nout[i] for i, n in enumerate(wn)])
            else:
                raise ValueError(out_kind)
        out_day = {}
        for c, (net, amt, sd) in Dd["da"].items():
            if (c.year == year - 1 and c.month == 12) or c < weeks[0] and c.year == year:
                k = mi(c.year, c.month)
                out_day[c] = net + sum(com(k).values()) / C.month_days(k)
        c = dt.date(year, 1, 1)
        while c < weeks[0]:
            if c not in out_day:
                out_day[c] = last_out / 7.0 * 1000.0
            c += dt.timedelta(days=1)
        for i, wk in enumerate(weeks):
            for dd in range(7):
                out_day[wk + dt.timedelta(days=dd)] = outw[i] / 7.0 * 1000.0
        com_day = {}
        c = dt.date(year - 1, 12, 1)
        while c <= dt.date(year, 12, 31):
            k = mi(c.year, c.month)
            com_day[c] = sum(com(k).values()) / C.month_days(k)
            c += dt.timedelta(days=1)
        spm = dict(st["spot_m"])
        acc = defaultdict(list)
        for c, v in spot_all.items():
            if c.year == year:
                acc[mi(c.year, c.month)].append(v)
        spm.update({k: float(np.mean(v)) for k, v in acc.items()})
        invoices = list(st["rec_open"])
        mw_s, px_s, y0, y1 = smelter(Dd)
        for k in range(mi(year - 1, 12), mi(year, 12) + 1):
            if year == 2022 and k == mi(2021, 12):
                continue  # December 2021's invoices are in the ledger with the day they were paid
            cm = com(k)
            for cu in ("SMELTER", "PULP", "AFFILIATE", "GRID"):
                if cu == "SMELTER":
                    price = px_s
                elif cu == "AFFILIATE" and aff_kind == "formula":
                    price = float(np.mean([spm[x] for x in range(k - aff["lag"] - aff["window"] + 1, k - aff["lag"] + 1)]))
                else:
                    price = spm[k]
                amt = cm[cu] * price
                if rec_kind == "sameday":
                    invoices.append(("month", k, amt))
                else:
                    invoices.append((pay_day(invoice_day(k), lags[cu]), amt))
        if rec_kind == "sameday":
            inv2 = []
            for x in invoices:
                if x[0] == "month":
                    _, k, amt = x
                    ds = [d for d in days if mi(d.year, d.month) == k]
                    inv2 += [(d, amt / len(ds)) for d in ds]
                else:
                    inv2.append(x)
            invoices = inv2
        return out_day, com_day, invoices

    return dict(rates=rates, desk=desk, supply=supply)


def infer_budget_margin(Dd):
    """the October budget price as a share of the year contract's average over the 60 business days before it."""
    r = []
    days = Dd["sdays"]
    for s, y, p, g in Dd["bud"]:
        if s.year < 2018:
            continue
        idx = [d for d in days if d < s][-60:]
        vals = [Dd["settle"][d].get(("Base Year", mi(y, 1), 12)) for d in idx]
        vals = [v for v in vals if v]
        if len(vals) > 50:
            r.append(p / float(np.mean(vals)))
    return round(float(np.median(r)), 3)


def params(Dd):
    return dict(rule=infer_rule(Dd), desk=infer_desk(Dd), plants=infer_plants(Dd), aff=infer_affiliate(Dd),
                lags=infer_lags(Dd), budget_margin=infer_budget_margin(Dd))


def run_stress(Dd, P, prices=None, **kw):
    st = opening(Dd, P["rule"], P["lags"], P["aff"])
    prices = prices or stress_prices(Dd)
    return RP.run(st, prices, models(Dd, P, **kw))


# ------------------------------------------------------------------------------------------------------ 2022 check
def actual_2022(Dd):
    """the hedge program's cumulative net cash outflow in 2022 as the records show it."""
    days = [d for d in Dd["sdays"] if d.year == 2022]
    idx = {d: i for i, d in enumerate(days)}
    flow = np.zeros(len(days))
    for d in days:
        flow[idx[d]] += Dd["stmt"][d]["net_cash_to_nex"]
    for c, (net, amt, sd) in Dd["da"].items():
        if sd in idx:
            flow[idx[sd]] -= amt
    for r in Dd["ledger"]:
        if r["paid_date"] and r["paid_eur"]:
            p = D(r["paid_date"])
            if p in idx:
                flow[idx[p]] -= float(r["paid_eur"])
    c = np.cumsum(flow)
    j = int(np.argmax(c))
    return dict(peak=float(c[j]), day=days[j], cum=c, days=days)


def method_2022(Dd, P):
    """the same method run on the book at the end of 2021 through 2022's own prices and inflows."""
    ye = dt.date(2021, 12, 30)
    st = opening(Dd, P["rule"], P["lags"], P["aff"], year_end=ye)
    st["rec_open"] = []
    for r in Dd["ledger"]:
        if r["doc_type"] == "INV" and r["period"] <= "2021-12" and r["paid_date"] and D(r["paid_date"]).year == 2022:
            st["rec_open"].append((D(r["paid_date"]), float(r["amount_eur"])))
    hyd = [h for h in Dd["hydro"] if h["week"] <= dt.date(2021, 12, 27)]
    st["level"], st["last_week"] = hyd[-1]["storage"], hyd[-1]
    bd22 = sorted(d for d in Dd["curve"] if d.year == 2022 or d == ye)
    curves22 = {d: Dd["curve"][d] for d in bd22}
    spot22 = {c: v for c, v in Dd["spot"].items() if c.year == 2022}
    prices = RP.stress_prices(Dd["curve"][ye], curves22, spot22, bd22, year=2022)
    m = models(Dd, P, year=2022)
    return RP.run(st, prices, m)


# ------------------------------------------------------------------------------------------------------ results
def snapshot(Dd, g):
    """the results a run reports from a stress path: the peak and its date, and the parts at the peak."""
    j = g["j"]
    d = g["peak_day"]
    mw = g["book"]["mw_by_day"][j]
    def left(k):
        # energy still to be delivered after the date: whole months ahead, the rest of the current month
        if mi_date(k) > d:
            return C.month_hours(k)
        return max((mi_date(k + 1) - d).days - 1, 0) * 24.0
    book = {y: round(-sum(mw.get(k, 0.0) * left(k) for k in year_months(y) if mi_date(k + 1) > d) / 1e6, 3)
            for y in (2027, 2028, 2029, 2030)}
    out_to = sum(v for c, v in g["out_day"].items() if dt.date(2027, 1, 1) <= c <= d) / 1e3
    return dict(peak=g["peak"] / 1e6, day=d, book=book, im=g["im"][j] / 1e6, da_net=-g["da"][:j + 1].sum() / 1e6,
                rec=g["rec"][:j + 1].sum() / 1e6, vm=g["vm"][:j + 1].sum() / 1e6, dlv=g["dlv"][:j + 1].sum() / 1e6,
                dim=g["dim"][:j + 1].sum() / 1e6, out=out_to)


def hedge_ratios(Dd, d=dt.date(2026, 12, 30)):
    bpx, bgen = budget_fns(Dd["bud"])
    fp = fixed_phys_fn(Dd)
    mw = Dd["pos"][d]
    out = {}
    for y in (2027, 2028, 2029):
        ex = -sum(mw.get(k, 0.0) * month_hours(k) for k in year_months(y))
        g = bgen(d, y)
        out[y] = dict(exchange=ex / g, policy=(ex + fp(y)) / g, exchange_twh=ex / 1e6, gen_twh=g / 1e6)
    return out


def below_minimum(Dd):
    """month ends since 2020 at which next year's exchange positions alone sat below the policy minimum."""
    bpx, bgen = budget_fns(Dd["bud"])
    n = b = 0
    for me, mw in Dd["pos"].items():
        if me < dt.date(2020, 1, 1):
            continue
        y = me.year + 1
        lo, hi = C.ladder(max((dt.date(y, 1, 1) - me).days / 365.25, 0.0), Dd["ladder"])
        ex = -sum(mw.get(k, 0.0) * month_hours(k) for k in year_months(y)) / bgen(me, y)
        n += 1
        b += ex < lo - 0.05
    return b, n


def facility(peak_m, rounding_m):
    return math.ceil(peak_m / rounding_m - 1e-9) * rounding_m


def full(tgt, quick_only=False):
    Dd = load(tgt)
    Pm = params(Dd)
    prices = stress_prices(Dd)
    R = dict(params=Pm, rounding=Dd["rounding"] / 1e6, facility_2026=Dd["facility_2026"] / 1e6)
    g = RP.run(opening(Dd, Pm["rule"], Pm["lags"], Pm["aff"]), prices, models(Dd, Pm))
    R["golden_path"] = g
    R["golden"] = snapshot(Dd, g)
    R["facility"] = facility(R["golden"]["peak"], R["rounding"])
    R["facility_of"] = lambda p: facility(p, R["rounding"])
    R["ratios"] = hedge_ratios(Dd)
    R["below"] = below_minimum(Dd)
    R["book_open"] = {y: round(-sum(Dd["pos"][dt.date(2026, 12, 30)].get(k, 0.0) * month_hours(k)
                                    for k in year_months(y) if mi_date(k) >= dt.date(2027, 1, 1)) / 1e6, 3)
                      for y in (2027, 2028, 2029, 2030)}
    a22, m22 = actual_2022(Dd), method_2022(Dd, Pm)
    R["check2022"] = dict(actual=a22["peak"] / 1e6, actual_day=a22["day"], method=m22["peak"] / 1e6, method_day=m22["peak_day"])
    st0 = opening(Dd, Pm["rule"], Pm["lags"], Pm["aff"])
    R["storage_open"] = st0["level"]
    if quick_only:
        return R

    def run(P=None, **kw):
        P = P or Pm
        return snapshot(Dd, RP.run(opening(Dd, P["rule"], P["lags"], P["aff"]), prices, models(Dd, P, **kw)))

    def with_(**ch):
        import copy
        P = copy.deepcopy(Pm)
        for path, v in ch.items():
            a, b = path.split("__")
            P[a][b] = v
        return P
    fam = [("the golden route", R["golden"]),
           ("a smooth response of the desk, sold up to the maximum in a straight line with the price", run(desk_rule="linear")),
           ("the desk's threshold at 1.20 of budget", run(theta=1.20)),
           ("the desk's threshold at 1.30 of budget", run(theta=1.30)),
           ("the desk at 2.5 points a week", run(speed=0.025)),
           ("the desk at 3.5 points a week", run(speed=0.035)),
           ("rates at the nearest-rank quantile", run(with_(rule__q=0.99, rule__look=250))),
           ("rates on a 252-day look-back", run(with_(rule__look=252))),
           ("release response 20 per cent flatter", run(with_(plants__slope=Pm["plants"]["slope"] * 0.8))),
           ("release response 20 per cent steeper", run(with_(plants__slope=Pm["plants"]["slope"] * 1.2))),
           ("payment habits three days slower", run(with_(**{"lags__" + c: v + 3 for c, v in Pm["lags"].items()}))),
           ("payment habits three days faster", run(with_(**{"lags__" + c: v - 3 for c, v in Pm["lags"].items()}))),
           ("the affiliate's window lagged one month", run(with_(aff__lag=Pm["aff"]["lag"] - 1))),
           ("the affiliate's window lagged three months", run(with_(aff__lag=Pm["aff"]["lag"] + 1)))]
    R["family"] = fam
    sc = [("the book as it stood, rates held, output at budget, every customer at spot (quick)",
           run(desk_rule="frozen", rates_kind="const", out_kind="budget", aff_kind="spot", rec_kind="sameday")),
          ("the policy's minimum ladder on exchange positions, 2022's rates as a share of price, output carried from "
           "2022's own shortfall, the affiliate at spot (careful but hurried)",
           run(desk_rule="min", count_phys=False, rates_kind="pct2022", out_kind="ratio22", aff_kind="spot")),
          ("the desk held to the policy minimum, nothing else", run(desk_rule="min")),
          ("the desk moved to the policy maximum at once, nothing else", run(desk_rule="max_now")),
          ("the book frozen at the year end, nothing else", run(desk_rule="frozen")),
          ("the smelter's contract left out of the hedge ratio, nothing else", run(count_phys=False)),
          ("rates held at the year end, nothing else", run(rates_kind="const")),
          ("rates scaled with the front price, nothing else", run(rates_kind="price")),
          ("2022's rates as a share of price, nothing else", run(rates_kind="pct2022")),
          ("output at budget, nothing else", run(out_kind="budget")),
          ("output carried from 2022's own shortfall, nothing else", run(out_kind="ratio22")),
          ("output scaled with the week's inflow, nothing else", run(out_kind="inflow")),
          ("the affiliate at spot, nothing else", run(aff_kind="spot")),
          ("customers paid on delivery, nothing else", run(rec_kind="sameday"))]
    R["shortcuts"] = sc
    R["ewma"] = run(rates_kind="ewma")
    return R
