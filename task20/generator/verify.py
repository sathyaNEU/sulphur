"""task20 verify: an independent recompute of the load-bearing figures from target/ alone, on its own code path (no
import of analysis.py), compared with figures.json. Exit 1 on any mismatch.

    python3 task20/generator/verify.py
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), "target")
REG = ["Northeast", "Southeast", "Midwest", "West"]
BAD = []


def ok(label, a, b, tol):
    good = abs(a - b) <= tol
    print("%s  %s: %.4f against figures.json %.4f" % ("PASS" if good else "FAIL", label, a, b))
    if not good:
        BAD.append(label)


def f(name):
    m = [x for x in os.listdir(TGT) if x.startswith(name)]
    return os.path.join(TGT, m[0])


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    res = pd.read_csv(f("bmh_quarterly_results"), parse_dates=["period_start", "period_end"]).set_index("fiscal_quarter")
    pan = pd.read_csv(f("kestrel_bmh_panel_weekly_delivery"), parse_dates=["week_start"])
    hist = pd.read_csv(f("kestrel_bmh_delivery_history"), parse_dates=["delivery_date", "week_start"])
    desc = pd.read_csv(f("kestrel_bmh_descriptor_detail"))
    txt = subprocess.run(["pdftotext", "-layout", f("bmh_10k_"), "-"], capture_output=True, text=True).stdout

    # completion: the first-delivered value of each issuer's latest three weeks against the value three weeks on
    piv = hist.pivot_table(index=["issuer_code", "week_start"], columns="delivery_date", values="spend_usd")
    dels = sorted(hist.delivery_date.unique())
    shares = {}
    for (iss, wk), row in piv.iterrows():
        seen = [d for d in dels if not np.isnan(row.get(d, np.nan))]
        if not seen:
            continue
        first = seen[0]
        lag = (pd.Timestamp(first) - pd.Timestamp(wk)).days // 7 - 1
        later = [d for d in seen if pd.Timestamp(d) >= pd.Timestamp(first) + pd.Timedelta(days=21)]
        if lag in (0, 1, 2) and later:
            shares.setdefault((iss, lag), []).append(row[first] / row[later[-1]])
        # the same week at later lags, as each later delivery first shows it at that lag
        for k, d in enumerate(seen[1:3], 1):
            lg = lag + k
            later2 = [x for x in seen if pd.Timestamp(x) >= pd.Timestamp(d) + pd.Timedelta(days=21)]
            if lg in (1, 2) and later2:
                shares.setdefault((iss, lg), []).append(row[d] / row[later2[-1]])
    cf = {k: float(np.median(v)) for k, v in shares.items()}
    ok("lag-0 completion, KS-01", 100 * cf[("KS-01", 0)], F["cf_last_week_pct"]["KS-01"], 0.3)

    # the entity: licensed shops and cafes out of the brand id by month; Fernhollow from 2 June 2024
    b = desc[desc.merchant_id == "M0412"]
    ex = b[b.descriptor.str.contains("HOLLISTERS|CAFE")].groupby("month").spend_usd.sum() / b.groupby("month").spend_usd.sum()
    qm = ["2025-11", "2025-12", "2026-01"]
    bb = b[b.month.isin(qm)]
    ok("excluded share, November to January (%)", 100 * bb[bb.descriptor.str.contains("HOLLISTERS|CAFE")].spend_usd.sum()
       / bb.spend_usd.sum(), F["excluded_share_pct"], 0.01)
    pan = pan[(pan.merchant_id != "M2290") | (pan.week_start >= "2024-06-02")].copy()
    m = pan.week_start.dt.strftime("%Y-%m")
    pan.loc[pan.merchant_id == "M0412", "spend_usd"] *= 1 - m[pan.merchant_id == "M0412"].map(ex).values
    last = pan.week_start.max()
    lag = ((last - pan.week_start).dt.days // 7)
    for l in (0, 1, 2):
        sel = lag == l
        pan.loc[sel, "spend_usd"] /= pan.loc[sel, "issuer_code"].map({k[0]: v for k, v in cf.items() if k[1] == l}).values

    q4 = pan[(pan.week_start >= "2025-11-02") & (pan.week_start <= "2026-01-25")]
    q4b = pan[(pan.week_start >= "2024-11-03") & (pan.week_start <= "2025-01-26")]
    both = sorted(set(q4.issuer_code) & set(q4b.issuer_code))
    q4, q4b = q4[q4.issuer_code.isin(both)], q4b[q4b.issuer_code.isin(both)]

    def cells(d):
        s = d.groupby(["billing_region", "card_open_year"]).spend_usd.sum() / 13.0
        c = d.drop_duplicates(["week_start", "issuer_code", "billing_region", "card_open_year"]).groupby(
            ["billing_region", "card_open_year"]).panel_cards.sum() / 13.0
        return s, c
    s1, c1 = cells(q4)
    s0, c0 = cells(q4b)
    growth = {}
    for r in REG:
        num = den = 0.0
        for (rr, y), cards in c0.items():
            if rr != r or (r, y + 1) not in c1.index:
                continue
            num += cards * s1[(r, y + 1)] / c1[(r, y + 1)]
            den += s0[(r, y)]
        growth[r] = num / den - 1
        ok("growth on same-age cards, %s (%%)" % r, 100 * growth[r], F["regional_pct"][r], 0.01)

    block = txt.split("Net sales by region")[1].split("Acquisition")[0]
    fy24 = {r: float(re.search(r"^\s*%s\s+.*?([\d,]+\.\d)\s*$" % r, block, re.M).group(1).replace(",", "")) for r in REG}
    tot = sum(fy24.values())
    g_idx = sum(growth[r] * fy24[r] / tot for r in REG)
    ok("card-visible growth at the fiscal 2024 mix (%)", 100 * g_idx, F["visible_growth_pct"], 0.01)
    pl = {"FY%s Q%s" % (a, q): float(v) for a, q, v in re.findall(r"Fiscal (\d{4}) Q(\d)\s+(\d+\.\d)", txt)}
    plt = pl["FY2025 Q3"] + (pl["FY2025 Q3"] - pl["FY2024 Q4"]) / 3.0
    ok("private-label share carried (%)", plt, F["pl_target_pct"], 0.005)
    d = (1 - pl["FY2024 Q4"] / 100 - 0.12) / (1 - plt / 100 - 0.12)
    g = (1 + g_idx) * d - 1
    ok("growth (%)", 100 * g, F["growth_pct"], 0.01)
    base = float(res.net_sales_usd_m["FY2024 Q4"])
    ok("net sales estimate (USD m)", base * (1 + g), F["forecast_m"], 0.1)
    st = pd.read_csv(f("bmh_q4fy25_street"))
    ok("street mean (USD m)", st.q4_fy2025_net_sales_usd_m.mean(), F["street_m"], 0.05)
    ok("range top (USD m)", base * (1 + g + 1.2816 * F["golden_rmse_pp"] / 100), F["range_high_m"], 0.15)
    print("\n%d mismatches" % len(BAD) if BAD else "\nverify: every figure recomputes")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
