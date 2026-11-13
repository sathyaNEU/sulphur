"""Writes the record files of target/ from the world (sim.py). Each file is the output of the process that keeps it:
the exchange's settlement file, the risk system's curve store, the clearing house's notices and statements, the trade
capture system, the hydrology database, the plant SCADA monthly export, the billing system and the day-ahead
market's settlements. Mess comes from those processes, never from a decision."""
import csv
import datetime as dt
import math
import os
import numpy as np
import common as C
import sim as S
from common import mi, mi_date, month_hours, cprice

F_SETTLE = "nex_daily_settlement_2018_2026.csv"
F_CURVE = "hk_risk_curve_daily_2018_2026.csv"
F_PARAMS = "nex_margin_parameters_2018_2026.csv"
F_STMT = "nex_clearing_statements_2018_2026.csv"
F_POS = "nex_positions_month_end_2017_2026.csv"
F_TRADES = "hk_trade_capture_2018_2026.csv"
F_HYDRO = "hk_hydrology_weekly_2017_2026.csv"
F_PLANT = "hk_plant_output_monthly_2017_2026.csv"
F_LEDGER = "hk_sales_ledger_2018_2026.csv"
F_DA = "nex_dayahead_settlements_2018_2026.csv"
F_FX = "eurnok_daily_2018_2026.csv"
F_HDD = "hk_heating_degree_days_weekly.csv"

CUST_NAME = {"SMELTER": "Fjordal Aluminium AS", "PULP": "Nesbyen Treforedling AS", "AFFILIATE": "Hallingvass Straum AS",
             "GRID": "Bygdenett AS"}
PLANTS = [("Kvitebrekka", "run-of-river", 0.55), ("Tinnhylla", "run-of-river", 0.45),
          ("Hallingvass I", "reservoir", 0.40), ("Hallingvass II", "reservoir", 0.35), ("Djupetjern", "reservoir", 0.25)]
START = dt.date(2018, 1, 1)
NEW_CODES = dt.date(2020, 4, 1)
MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def w(path, header, rows):
    with open(path, "w", newline="") as f:
        cw = csv.writer(f, lineterminator="\r\n")
        cw.writerow(header)
        cw.writerows(rows)
    return len(rows)


def contract_code(t, k, d):
    s = mi_date(k)
    q = (s.month - 1) // 3 + 1
    if d < NEW_CODES:
        yy = "%02d" % (s.year % 100)
        return {"M": "ENOM%s-%s" % (MON[s.month - 1], yy), "Q": "ENOQ%d-%s" % (q, yy), "Y": "ENOYR-%s" % yy}[t]
    return {"M": "NSBM %d-%02d" % (s.year, s.month), "Q": "NSBQ %d-Q%d" % (s.year, q), "Y": "NSBY %d" % s.year}[t]


def listed(d):
    k0 = mi(d.year, d.month)
    out = [("M", [k0 + j]) for j in range(1, 7)]
    fq0 = mi(d.year, 3 * ((d.month - 1) // 3) + 1) + 3
    out += [("Q", [fq0 + 3 * (j - 1) + x for x in range(3)]) for j in range(1, 7)]
    out += [("Y", C.year_months(d.year + j)) for j in range(1, 5)]
    return out


PRODUCT = {"M": "Base Month", "Q": "Base Quarter", "Y": "Base Year"}


def settlement(W, tgt):
    rows = []
    dup = []
    for i, d in enumerate(W.days):
        if d < START or d == dt.date(2019, 11, 21):
            continue
        for t, ks in listed(d):
            e = mi_date(ks[-1] + 1) - dt.timedelta(days=1)
            r = [d.isoformat(), contract_code(t, ks[0], d), PRODUCT[t], mi_date(ks[0]).isoformat(), e.isoformat(),
                 "%.3f" % cprice(W.curves[i], ks)]
            rows.append(r)
            if dt.date(2023, 5, 8) <= d <= dt.date(2023, 5, 12):
                dup.append(list(r))
    # the exchange's re-sent file for the week of 8 May 2023 was appended twice
    at = next(j for j, r in enumerate(rows) if r[0] == "2023-05-15")
    rows = rows[:at] + dup + rows[at:]
    return w(os.path.join(tgt, F_SETTLE), ["trade_date", "contract", "product", "delivery_start", "delivery_end",
                                           "settlement_eur_mwh"], rows)


def curve(W, tgt):
    rows = []
    for i, d in enumerate(W.days):
        if d < START:
            continue
        k0 = mi(d.year, d.month)
        for k in range(k0 + 1, k0 + 49):
            s = mi_date(k)
            rows.append([d.isoformat(), "%d-%02d" % (s.year, s.month), "%.3f" % W.curves[i][k], "HK_SYS"])
            # the June 2021 parallel run of the new curve builder, a second curve id carried for a month
            if dt.date(2021, 6, 1) <= d <= dt.date(2021, 6, 30) and k <= k0 + 36:
                rows.append([d.isoformat(), "%d-%02d" % (s.year, s.month), "%.3f" % (W.curves[i][k] * (1 + 0.0004 * ((k * 7 + i) % 5 - 2))), "HK_SYS_V2"])
    return w(os.path.join(tgt, F_CURVE), ["as_of", "delivery_month", "forward_eur_mwh", "curve_id"], rows)


def params(W, tgt):
    rows, n = [], 4100
    first = {}
    for d, t, r in W.notices:
        if d < START:
            first[t] = (d, r)
    cls = {"M": "Base Month", "Q": "Base Quarter", "Y": "Base Year"}
    for t in "MQY":
        d, r = first[t]
        n += 1
        rows.append(["NEX-CM-%d" % n, "2017-12-29", "2018-01-02", cls[t], "%.2f" % W.rates[t][W.didx[dt.date(2018, 1, 2)]]])
    for d, t, r in sorted((x for x in W.notices if x[0] >= START), key=lambda x: (x[0], "MQY".index(x[1]))):
        n += 1
        rows.append(["NEX-CM-%d" % n, C.prev_bday(d).isoformat(), d.isoformat(), cls[t], "%.2f" % r])
    return w(os.path.join(tgt, F_PARAMS), ["notice_no", "published", "effective_date", "product_class",
                                           "margin_eur_per_mwh"], rows)


def statements(W, tgt):
    r = W.res
    rows = []
    im_prev = None
    for i, d in enumerate(W.days):
        im = r["im"][i]
        if d < START:
            im_prev = im
            continue
        vm, dl = r["vm"][i], r["dlv"][i]
        dim = im - im_prev
        im_prev = im
        row = [d.isoformat(), "HKK-HEDGE", "EUR", "%.2f" % vm, "%.2f" % dl, "%.2f" % im, "%.2f" % dim,
               "%.2f" % (vm + dl + dim), ""]
        if d == dt.date(2022, 3, 8):
            bad = list(row)
            bad[3] = "%.2f" % (vm * 1.07)
            bad[7] = "%.2f" % (vm * 1.07 + dl + dim)
            bad[8] = "superseded"
            rows.append(bad)
            row[8] = "restated"
        rows.append(row)
    return w(os.path.join(tgt, F_STMT), ["statement_date", "account", "currency", "variation_margin",
                                         "delivery_settlement", "initial_margin_requirement", "initial_margin_change",
                                         "net_cash_to_nex", "status"], rows)


def positions(W, tgt):
    rows = []
    months = sorted({mi(d.year, d.month) for d in W.days})
    for k in months:
        ds = [d for d in W.days if mi(d.year, d.month) == k]
        d = ds[-1]
        if d < dt.date(2017, 12, 1):
            continue
        mw = W.res["mw_by_day"][W.didx[d]]
        seen = set()
        for kk in sorted(mw):
            cl = C.margin_class(kk, d)
            s = mi_date(kk)
            if cl == "Y":
                key, ks = ("Y", s.year), C.year_months(s.year)
            elif cl == "Q":
                q0 = mi(s.year, 3 * ((s.month - 1) // 3) + 1)
                key, ks = ("Q", q0), [q0, q0 + 1, q0 + 2]
            else:
                key, ks = ("M", kk), [kk]
            if key in seen:
                continue
            seen.add(key)
            if mi_date(ks[-1] + 1) <= d:
                continue
            e = mi_date(ks[-1] + 1) - dt.timedelta(days=1)
            rows.append([d.isoformat(), "HKK-HEDGE", contract_code(cl, ks[0], d), PRODUCT[cl],
                         mi_date(ks[0]).isoformat(), e.isoformat(), "%.1f" % mw[kk]])
    return w(os.path.join(tgt, F_POS), ["month_end", "account", "contract", "product", "delivery_start",
                                        "delivery_end", "position_mw"], rows)


def trades(W, tgt):
    rng = np.random.default_rng(404)
    rows = []
    n = 70000
    traders = ["MHA", "MHA", "SSA", "MHA", "TBR"]
    for d, add in W.res["trades"]:
        if d < START:
            continue
        years = sorted({mi_date(k).year for k in add})
        for y in years:
            ks = C.year_months(y)
            mw = -add[ks[0]]
            px = cprice(W.curves[W.didx[d]], ks)
            n += 1
            # clips of up to 10 MW, as the desk executes on screen
            left = int(round(mw))
            while left > 0:
                clip = int(min(left, rng.integers(3, 11)))
                left -= clip
                n += 1
                unit, qty = ("MW", "%d" % clip)
                if d < dt.date(2021, 2, 1) and rng.random() < 0.35:
                    unit, qty = ("MWh", "%d" % (clip * C.hours_year(y)))
                t = dt.time(9 + int(rng.integers(0, 7)), int(rng.integers(0, 60)))
                pr = px * (1 + rng.normal(0, 0.0015))
                rows.append(["HK%06d" % n, d.isoformat(), t.strftime("%H:%M"), "HKK-HEDGE", contract_code("Y", ks[0], d),
                             "SELL", qty, unit, "%.2f" % pr, "NEW", traders[int(rng.integers(0, len(traders)))], "NEX"])
    # amendments and cancellations, as the capture system logs them
    out = []
    for j, r in enumerate(rows):
        out.append(r)
        if j % 53 == 7:
            a = list(r)
            a[9] = "AMEND"
            a[8] = "%.2f" % (float(r[8]) + 0.05)
            out.append(a)
        if j % 97 == 31:
            c = list(r)
            c[9] = "CANCEL"
            out.append(c)
            nb = list(r)
            nb[0] = r[0] + "R"
            out.append(nb)
    return w(os.path.join(tgt, F_TRADES), ["trade_id", "trade_date", "trade_time", "account", "contract", "side",
                                           "quantity", "unit", "price_eur_mwh", "status", "trader", "venue"], out)


def hydrology(W, tgt):
    rows = []
    g = W.guide()
    for i, wk in enumerate(W.weeks):
        iso = wk.isocalendar()
        n = min(iso[1], 52)
        infl = "%.1f" % W.inflow[i]
        status = "final"
        if dt.date(2019, 2, 4) <= wk <= dt.date(2019, 2, 18):
            infl = ""
            status = "gauge outage"
        if wk >= dt.date(2026, 11, 16):
            status = "provisional"
        rows.append(["%d-W%02d" % (iso[0], iso[1]), wk.isoformat(), infl, "%.1f" % W.level[i],
                     "%.1f" % (100 * W.level[i] / S.P["res_cap"]), "%.1f" % W.normal_week(n),
                     "%.1f" % (100 * g[n] / S.P["res_cap"]), status])
    return w(os.path.join(tgt, F_HYDRO), ["iso_week", "week_start", "inflow_gwh", "storage_gwh", "storage_pct",
                                          "normal_inflow_gwh", "normal_storage_pct", "status"], rows)


def plant_output(W, tgt):
    rng = np.random.default_rng(77)
    ror, rel = {}, {}
    for i, wk in enumerate(W.weeks):
        for dd in range(7):
            c = wk + dt.timedelta(days=dd)
            k = mi(c.year, c.month)
            ror[k] = ror.get(k, 0.0) + W.ror_w[i] / 7.0 * 1000.0
            rel[k] = rel.get(k, 0.0) + W.rel_w[i] / 7.0 * 1000.0
    rows = []
    for k in sorted(ror):
        s = mi_date(k)
        if s.year > 2026:
            continue
        for name, typ, sh in PLANTS:
            base = ror[k] if typ == "run-of-river" else rel[k]
            val = base * sh
            nm = name
            if name == "Djupetjern" and s >= dt.date(2021, 1, 1):
                nm = "Djupetjern kraftverk"
            rows.append(["%d-%02d" % (s.year, s.month), nm, typ, "%.0f" % val])
    return w(os.path.join(tgt, F_PLANT), ["month", "plant", "plant_type", "output_mwh"], rows)


def ledger(W, tgt):
    rows = []
    n = 220000
    for x in W.invoices:
        cu, k, inv = x["cu"], x["k"], x["doc"]
        if inv > dt.date(2026, 12, 31):
            continue  # the extract was taken on 31 December 2026
        s = mi_date(k)
        n += 1
        acct = {"SMELTER": "10411", "PULP": "10388", "AFFILIATE": "10102" if s < dt.date(2023, 4, 1) else "10977",
                "GRID": "10560"}[cu]
        paid = x["pay"].isoformat() if x["pay"] <= dt.date(2026, 12, 31) else ""
        amt = x["amt"]
        row = ["F%d" % n, "INV", CUST_NAME[cu], acct, "%d-%02d" % (s.year, s.month), "%.0f" % x["mwh"], "%.2f" % x["px"],
               "%.2f" % amt, inv.isoformat(), (inv + dt.timedelta(days=30)).isoformat(), paid, "%.2f" % amt if paid else ""]
        # the pulp mill pays some invoices in two parts
        if cu == "PULP" and k % 17 == 5 and paid:
            part = round(amt * 0.6, 2)
            row[11] = "%.2f" % part
            rows.append(row)
            later = S.pay_date(x["pay"], 9)
            rows.append(["F%d" % n, "PAY", CUST_NAME[cu], acct, row[4], "", "", "", "", "", later.isoformat(),
                         "%.2f" % (amt - part)])
            continue
        rows.append(row)
        if cu == "GRID" and k % 23 == 11:
            n += 1
            cr = round(x["mwh"] * 0.012)
            rows.append(["F%d" % n, "CRN", CUST_NAME[cu], acct, row[4], "%.0f" % -cr, "%.2f" % x["px"],
                         "%.2f" % (-cr * x["px"]), (inv + dt.timedelta(days=12)).isoformat(), "", "", ""])
    return w(os.path.join(tgt, F_LEDGER), ["doc_no", "doc_type", "customer", "customer_account", "period", "mwh",
                                           "price_eur_mwh", "amount_eur", "doc_date", "due_date", "paid_date",
                                           "paid_eur"], rows)


def dayahead(W, tgt):
    rows = []
    for c in W.cdays:
        if c < START:
            continue
        k = mi(c.year, c.month)
        com = sum(S.committed(k).values()) / C.month_days(k)
        out = W.out_day[c]
        net = out - com
        sold, bought = (net, 0.0) if net > 0 else (0.0, -net)
        sp = W.spot[c]
        settle = C.next_bday(c)
        rows.append([c.isoformat(), "%.1f" % sold, "%.1f" % bought, "%.2f" % sp, "%.2f" % (net * sp), settle.isoformat()])
    return w(os.path.join(tgt, F_DA), ["delivery_date", "sold_mwh", "bought_mwh", "system_price_eur_mwh",
                                       "net_amount_eur", "settlement_date"], rows)


def fx(W, tgt):
    rng = np.random.default_rng(12)
    x, rows = math.log(9.6), []
    for d in W.days:
        x += rng.normal(0, 0.004) + 0.00004
        if d >= START:
            rows.append([d.isoformat(), "%.4f" % math.exp(x)])
    return w(os.path.join(tgt, F_FX), ["date", "eur_nok"], rows)


def hdd(W, tgt):
    rng = np.random.default_rng(13)
    rows = []
    for wk in W.weeks:
        n = wk.isocalendar()[1]
        base = max(0.0, 15.5 + 9.5 * math.cos(2 * math.pi * (n - 3) / 52.0))
        rows.append([wk.isoformat(), "%.1f" % max(0.0, 7 * base + rng.normal(0, 9))])
    return w(os.path.join(tgt, F_HDD), ["week_start", "heating_degree_days"], rows)


def write_all(W, tgt):
    os.makedirs(tgt, exist_ok=True)
    n = {}
    for name, fn in ((F_SETTLE, settlement), (F_CURVE, curve), (F_PARAMS, params), (F_STMT, statements),
                     (F_POS, positions), (F_TRADES, trades), (F_HYDRO, hydrology), (F_PLANT, plant_output),
                     (F_LEDGER, ledger), (F_DA, dayahead), (F_FX, fx), (F_HDD, hdd)):
        n[name] = fn(W, tgt)
    return n
