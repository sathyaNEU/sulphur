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
    m = sorted(x for x in os.listdir(TGT) if x.startswith(name))
    return os.path.join(TGT, m[0])


def releases():
    """quarter -> net sales, contract, Fernhollow (quarter or fiscal year), deposits, and the nine months' columns"""
    out = {}
    for fn in sorted(os.listdir(TGT)):
        if not fn.startswith("bmh_8k_"):
            continue
        t = open(os.path.join(TGT, fn)).read()
        m = re.search(r"the (\w+) quarter of fiscal (\d{4}), the (\w+) weeks ended (\w+ \d+, \d{4})", t)
        qn = {"first": 1, "second": 2, "third": 3, "fourth": 4}[m.group(1)]
        key = "FY%s Q%d" % (m.group(2), qn)

        def row(section, label):
            for ln in section.splitlines():
                if re.match(r"^\s*%s\s{2,}" % re.escape(label), ln):
                    rest = ln[ln.index(label) + len(label):]
                    return [0.0 if x == "--" else float(x.replace(",", "")) for x in re.findall(r"[\d,]{3,}|--", rest)]
            return None
        inc = t[t.index("STATEMENTS OF INCOME"):t.index("NET SALES BY BRAND")]
        brand = t[t.index("NET SALES BY BRAND"):t.index("BALANCE SHEETS")]
        bs = t[t.index("BALANCE SHEETS"):]
        out[key] = dict(q=qn, weeks={"thirteen": 13, "fourteen": 14}[m.group(3)], end=pd.Timestamp(m.group(4)),
                        ns=row(inc, "Net sales")[0], ct=(row(brand, "Contract") or row(brand, "B&M Contract")),
                        fern=row(brand, "Fernhollow") or [0.0, 0.0, 0.0, 0.0], dep=row(bs, "Customer deposits"))
    return out


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    rel = releases()
    q = {}
    for k, r in rel.items():
        if r["q"] < 4:
            ct, fe = r["ct"][0], r["fern"][0]
        else:
            n9 = rel[k[:-1] + "3"]
            ct, fe = r["ct"][0] - n9["ct"][2], r["fern"][0] - n9["fern"][2]
        q[k] = dict(ns=r["ns"] / 1000, ct=ct / 1000, fern=fe / 1000, dep=r["dep"][0] / 1000, weeks=r["weeks"], end=r["end"])
    ok("contract, fourth quarter fiscal 2024 (USD m)", q["FY2024 Q4"]["ct"], F["contract_base_m"], 0.05)
    keys = sorted(q, key=lambda k: q[k]["end"])
    i = keys.index("FY2025 Q3")
    ct_hat = float(np.median([q[k]["ct"] for k in keys[i - 7:i + 1]]))
    ok("contract run rate (USD m)", ct_hat, F["contract_q4_m"], 0.05)

    pan = pd.read_csv(f("kestrel_bmh_panel_weekly"), parse_dates=["week_start"], dtype={"card_open_year": str})
    hist = pd.read_csv(f("kestrel_bmh_delivery_history"), parse_dates=["delivery_date", "week_start"])
    desc = pd.read_csv(f("kestrel_bmh_descriptor_detail"))
    txt = subprocess.run(["pdftotext", "-layout", f("bmh_10k_"), "-"], capture_output=True, text=True).stdout
    canon = {"NE": "Northeast", "NORTHEAST": "Northeast", "SE": "Southeast", "SOUTHEAST": "Southeast", "MW": "Midwest",
             "MIDWEST": "Midwest", "W": "West", "WEST": "West"}
    pan["billing_region"] = pan.billing_region.map(lambda s: canon[re.sub(r"[^A-Z]", "", s.upper())])

    # completion: the first-delivered value of each issuer's latest three weeks against the value three weeks on
    piv = hist.pivot_table(index=["issuer_code", "week_start"], columns="delivery_date", values="spend_usd")
    dels = sorted(hist.delivery_date.unique())
    shares = {}
    for (iss, wk), row in piv.iterrows():
        seen = [d for d in dels if not np.isnan(row.get(d, np.nan))]
        for k_, d in enumerate(seen[:3]):
            lag = (pd.Timestamp(d) - pd.Timestamp(wk)).days // 7 - 1
            later = [x for x in seen if pd.Timestamp(x) >= pd.Timestamp(d) + pd.Timedelta(days=21)]
            if lag in (0, 1, 2) and later:
                shares.setdefault((iss, lag), []).append(row[d] / row[later[-1]])
    cf = {k: float(np.median(v)) for k, v in shares.items()}
    ok("lag-0 completion, KS-01", 100 * cf[("KS-01", 0)], F["cf_last_week_pct"]["KS-01"], 0.3)

    # the entity: licensed shops and cafes out of the brand id by month; Fernhollow from 2 June 2024
    b = desc[desc.merchant_id == "M0412"]
    ex = b[b.descriptor.str.contains("HOLLISTERS|CAFE")].groupby("month").spend_usd.sum() / b.groupby("month").spend_usd.sum()
    pan = pan[(pan.merchant_id != "M2290") | (pan.week_start >= "2024-06-02")].copy()
    m = pan.week_start.dt.strftime("%Y-%m")
    pan.loc[pan.merchant_id == "M0412", "spend_usd"] *= 1 - m[pan.merchant_id == "M0412"].map(ex).values
    last = pan.week_start.max()
    lag = ((last - pan.week_start).dt.days // 7)
    for l in (0, 1, 2):
        s = lag == l
        pan.loc[s, "spend_usd"] /= pan.loc[s, "issuer_code"].map({k[0]: v for k, v in cf.items() if k[1] == l}).values

    # issuers in every week of both quarters, less any whose cards in a region rose 5 per cent in four weeks between them
    cards = pan.drop_duplicates(["week_start", "issuer_code", "billing_region", "card_open_year"])
    cw = cards.groupby(["issuer_code", "billing_region", "week_start"]).panel_cards.sum()
    lo, hi = pd.Timestamp("2024-11-03"), pd.Timestamp("2026-01-31")
    jumped = set()
    for (iss, reg), s in cw.groupby(level=[0, 1]):
        s = s.droplevel([0, 1]).sort_index()
        r4 = (s / s.shift(4) - 1).iloc[8:]
        if ((r4 > 0.05) & (r4.index >= lo) & (r4.index <= hi)).any():
            jumped.add(iss)
    q4 = pan[(pan.week_start >= "2025-11-02") & (pan.week_start <= "2026-01-25")]
    q4b = pan[(pan.week_start >= "2024-11-03") & (pan.week_start <= "2025-01-26")]
    n4, n4b = q4.week_start.nunique(), q4b.week_start.nunique()
    both = [i for i in sorted(set(q4.issuer_code) & set(q4b.issuer_code))
            if q4[q4.issuer_code == i].week_start.nunique() == n4 and q4b[q4b.issuer_code == i].week_start.nunique() == n4b
            and i not in jumped]
    print("issuers used:", both, "set aside:", sorted(jumped & set(q4.issuer_code)))
    growth = {}
    for r in REG:
        def per_card(d):
            d = d[(d.issuer_code.isin(both)) & (d.billing_region == r)]
            c = d.drop_duplicates(["week_start", "issuer_code", "billing_region", "card_open_year"]).panel_cards.sum()
            return d.spend_usd.sum() / c
        growth[r] = per_card(q4) / per_card(q4b) - 1
        ok("growth per open card, %s (%%)" % r, 100 * growth[r], F["regional_pct"][r], 0.01)
    block = txt.split("Net sales by brand and region")[1].split("Acquisition")[0]
    fy24 = {r: float(re.search(r"^\s*%s\s+.*?([\d,]+\.\d)\s*$" % r, block, re.M).group(1).replace(",", "")) for r in REG}
    tot = sum(fy24.values())
    g = sum(growth[r] * fy24[r] / tot for r in REG)
    ok("card-visible growth at the fiscal 2024 mix (%)", 100 * g, F["visible_growth_pct"], 0.01)

    # deposits: last year's closing deposits scaled by the brand's payments, the last eight weeks' share and custom share
    dep = {k: q[k]["dep"] for k in q}
    pay = lambda k, kp, fern=True: q[k]["ns"] - q[k]["ct"] - (0 if fern else q[k]["fern"]) + dep[k] - dep[kp]
    pay_b = pay("FY2024 Q4", "FY2024 Q3")
    pay_q = pay_b * (1 + g)
    bp_b = pay("FY2024 Q4", "FY2024 Q3", False)
    bp_q = pay_q * bp_b / pay_b

    def last8(lo_, hi_):
        sub = pan[(pan.week_start >= lo_) & (pan.week_start <= hi_) & (pan.merchant_id != "M2290")]
        nw = sub.week_start.nunique()
        cov = sub.groupby("issuer_code").week_start.nunique()
        wk = sub[sub.issuer_code.isin(cov[cov == nw].index)].groupby("week_start").spend_usd.sum().sort_index()
        return wk.iloc[-8:].sum() / wk.sum()

    def custom(end):
        win = pd.date_range(end - pd.Timedelta(days=55), end, freq="D")
        wts = pd.Series(1.0, index=win).groupby(win.strftime("%Y-%m")).sum()
        b2 = desc[desc.merchant_id.isin(["M0412", "M0413"]) & ~desc.descriptor.str.contains("HOLLISTERS|CAFE")]
        b2 = b2[b2.month.isin(wts.index)]
        m_ = b2[b2.descriptor.str.contains("DESIGN STUDIO|CUSTOM")].groupby("month").spend_usd.sum()
        a_ = b2.groupby("month").spend_usd.sum()
        wd = pd.Series({k: wts[k] / pd.Period(k).days_in_month for k in wts.index})
        return float((m_.reindex(wd.index).fillna(0) * wd).sum() / (a_.reindex(wd.index).fillna(0) * wd).sum())
    tq = last8(pd.Timestamp("2025-11-02"), pd.Timestamp("2026-01-25"))
    tb = last8(pd.Timestamp("2024-11-03"), pd.Timestamp("2025-01-26"))
    cq, cb = custom(pd.Timestamp("2026-01-31")), custom(pd.Timestamp("2025-02-01"))
    ok("custom-order share, last eight weeks of the quarter (%)", 100 * cq, F["custom_q4_pct"], 0.01)
    dep_q4 = dep["FY2024 Q4"] * (bp_q * tq * cq) / (bp_b * tb * cb)
    ok("customer deposits at the quarter's end (USD m)", dep_q4, F["deposits_q4_m"], 0.6)
    rev_ret = pay_q - (dep_q4 - dep["FY2025 Q3"])
    total = rev_ret + ct_hat
    base = q["FY2024 Q4"]["ns"]
    ok("growth (%)", 100 * (total / base - 1), F["growth_pct"], 0.05)
    ok("net sales estimate (USD m)", total, F["forecast_m"], 0.6)
    st = pd.read_csv(f("bmh_q4fy25_street"))
    ok("street mean (USD m)", st.q4_fy2025_net_sales_usd_m.mean(), F["street_m"], 0.05)
    ok("range top (USD m)", base * (total / base + 1.2816 * F["golden_rmse_pp"] / 100), F["range_high_m"], 0.15)
    print("\n%d mismatches" % len(BAD) if BAD else "\nverify: every figure recomputes")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
