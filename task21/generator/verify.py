"""An independent recompute of every graded figure from target/ alone. It imports nothing from the generator (not
methods.py, golden.py or params.py), reads each file in its own format and rebuilds each step its own way, then
compares with generator/figures.json. Exit 1 on any difference beyond the stated precision.

    python3 verify.py [target]
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import zoneinfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
LDN = zoneinfo.ZoneInfo("Europe/London")
ASAT = dt.date(2026, 10, 31)
FROM = dt.date(2026, 2, 1)
CAP, INFL, MOVE, TGT, SERV, IPT = 100000.0, 0.055, 0.02, 0.75, 34.0, 0.12


def path(prefix):
    return os.path.join(TARGET, [f for f in sorted(os.listdir(TARGET)) if f.startswith(prefix)][0])


def band(age):
    return pd.cut(pd.Series(age), [-1, 24, 64, 200], labels=["u25", "mid", "o65"]).astype(str).values


# ---- the four sites, conformed --------------------------------------------------------------------------------------
def quotes():
    parts = []
    k = pd.read_csv(path("kitecompare"))
    parts.append(pd.DataFrame({"site": "Kitecompare", "ref": k.quote_ref,
                               "day": pd.to_datetime(k.quote_time_local).dt.date, "age": k.main_driver_age,
                               "pc": k.postcode_district, "gross": k.halvergate_premium_gbp,
                               "rank": k.halvergate_position, "c1": k.rival_1_gbp, "c2": k.rival_2_gbp,
                               "c3": k.rival_3_gbp, "wt": k.extract_weight}))
    c = pd.read_json(path("covertide"), lines=True)
    c = c[~c["ref"].duplicated()]
    top = np.vstack(c["top3"].values)
    parts.append(pd.DataFrame({"site": "Covertide", "ref": c["ref"].values,
                               "day": pd.to_datetime(c["ts"], unit="ms", utc=True).dt.tz_convert(LDN).dt.date.values,
                               "age": [r["age"] for r in c["risk"]], "pc": [r["postcode"] for r in c["risk"]],
                               "gross": c["quotedPremium"].values, "rank": c["rank"].values, "c1": top[:, 0],
                               "c2": top[:, 1], "c3": top[:, 2], "wt": c["weight"].values}))
    b = pd.read_csv(path("brightquote"), sep=";")
    parts.append(pd.DataFrame({"site": "Brightquote", "ref": b.QuoteID,
                               "day": pd.to_datetime(b.QuoteDate, dayfirst=True).dt.date, "age": b.DriverAge,
                               "pc": b.PostcodeDistrict, "gross": b.PremiumPence / 100, "rank": b.Rank,
                               "c1": b.Comp1Pence / 100, "c2": b.Comp2Pence / 100, "c3": b.Comp3Pence / 100,
                               "wt": b.Weight}))
    p = pd.read_csv(path("pricelark"))
    parts.append(pd.DataFrame({"site": "Pricelark", "ref": p.reference,
                               "day": pd.to_datetime(p.created_utc, utc=True).dt.tz_convert(LDN).dt.date,
                               "age": p.age, "pc": p.district, "gross": p.price, "rank": p.position,
                               "c1": p.cheapest_other, "c2": p.second_other, "c3": p.third_other,
                               "wt": p.sampling_weight}))
    q = pd.concat(parts, ignore_index=True)
    q = q[q.pc != "ZZ99"].reset_index(drop=True)
    q["seg"] = band(q.age.values)
    q["gap"] = np.log(q.gross.values / q.c1.values)
    q["rk"] = q["rank"].clip(upper=4)
    return q


# ---- policies, claims and exposure ------------------------------------------------------------------------------------
def policies():
    p = pd.read_csv(path("pcw_nb_policies"), keep_default_na=False, na_values=[""])
    p["inc"] = pd.to_datetime(p.inception_date)
    p["stop"] = pd.to_datetime(p.cancelled_on).fillna(pd.to_datetime(p.expiry_date))
    p["stop"] = p[["stop"]].assign(x=pd.to_datetime(p.expiry_date)).min(axis=1)
    p["seg"] = band(p.main_driver_age.values)
    return p


def months():
    return pd.date_range("2025-01-01", "2026-10-01", freq="MS")


def earned(p):
    """Vehicle-years each policy earns in each calendar month to the as-at date: policies x months."""
    ms = months()
    lo = np.maximum(p.inc.values[:, None], ms.values[None, :])
    edges = ms + pd.offsets.MonthBegin(1)
    hi = np.minimum(np.minimum(p.stop.values, np.datetime64(ASAT + dt.timedelta(days=1)))[:, None],
                    edges.values[None, :])
    d = (hi - lo).astype("timedelta64[D]").astype(float)
    return np.clip(d, 0, None) / 365.0


def claims():
    c = pd.read_csv(path("motor_claims_extract"), keep_default_na=False, na_values=[""])
    c["acc"] = pd.to_datetime(c.accident_date)
    c["lag"] = (pd.to_datetime(c.notified_date) - c.acc).dt.days
    c["age"] = (pd.Timestamp(ASAT) - c.acc).dt.days
    c["cap"] = c.incurred_gbp.clip(upper=CAP)
    # each type's notification pattern, read on accidents a full year old
    ref = c[(c.acc <= pd.Timestamp(2025, 10, 31)) & (c.lag <= 365)]
    share = np.ones(len(c))
    for t, g in c.groupby("claim_type"):
        lags = np.sort(ref[ref.claim_type == t].lag.values)
        share[g.index] = np.maximum(np.searchsorted(lags, g.age.values, side="right") / len(lags), 0.05)
    mean_cost = c[c.acc <= pd.Timestamp(2025, 10, 31)].groupby("claim_type").cap.mean()
    c["ult"] = c.cap + (1 / share - 1) * c.claim_type.map(mean_cost).values
    c["n"] = 1 / share
    return c


def seasons(p, c, E, kind):
    ms = months()
    keep = ms <= pd.Timestamp(2026, 9, 1)
    lab = c.acc.dt.to_period("M")
    v = c.ult if kind == "cost" else c.n
    num, den = np.zeros(12), np.zeros(12)
    wp = p.written_premium_gbp.values
    for j, m in enumerate(ms):
        if not keep[j]:
            continue
        num[m.month - 1] += v[lab == m.to_period("M")].sum()
        den[m.month - 1] += (E[:, j] * wp).sum() if kind == "cost" else E[:, j].sum()
    r = num / den
    return r * den.sum() / (r * den).sum()


# ---- the replay -----------------------------------------------------------------------------------------------------
def gap_fit(s):
    s = s[s.expn > 0]
    edges = np.quantile(s.gap, np.linspace(0, 1, 11))
    b = np.clip(np.searchsorted(edges[1:-1], s.gap.values, side="right"), 0, 9)
    g = pd.DataFrame({"b": b, "gap": s.gap.values, "n": s.cnt.values, "e": s.expn.values}).groupby("b")
    x = g.gap.mean().values
    y = (g.n.sum() / g.e.sum()).values
    w = g.e.sum().values
    A = np.polyfit(x, np.log(y), 1, w=np.sqrt(w))
    return (lambda z: np.exp(A[0] * np.clip(z, x.min(), x.max()) + A[1])), A[0], y


def rank_after(g, c1, c2, c3, L):
    new = g * (1 + L)
    return 1 + (new >= c1 * (1 + MOVE)).astype(int) + (new >= c2 * (1 + MOVE)) + (new >= c3 * (1 + MOVE))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    prop = int(re.search(r"wants (\d+) per cent for under-25s", open(os.path.join(os.path.dirname(HERE), "prompt.txt"))
                         .read()).group(1)) / 100
    q = quotes()
    p = policies()
    c = claims()
    E = earned(p)
    s_cost, s_cnt = seasons(p, c, E, "cost"), seasons(p, c, E, "count")
    cost = p.policy_number.map(c.groupby("policy_number").ult.sum()).fillna(0).values
    sep = c[c.acc <= pd.Timestamp(2026, 9, 30)]
    cnt = p.policy_number.map(sep.groupby("policy_number").n.sum()).fillna(0).values
    upto_sep = (months() <= pd.Timestamp(2026, 9, 1)).astype(float)
    mon = months().month.values - 1
    sold = q[q.wt == 1]
    sales = p.merge(sold[["ref", "day", "gross", "rank", "rk", "c1", "c2", "c3", "gap", "site"]], left_on="quote_reference",
                    right_on="ref", how="inner")
    idx = pd.Series(np.arange(len(p)), index=p.policy_number)
    out, bad = {}, []

    def check(name, got, want, tol):
        ok = abs(got - want) <= tol + 1e-9
        print("%-4s %-46s %14s %14s" % ("PASS" if ok else "FAIL", name, round(got, 4), want))
        if not ok:
            bad.append(name)

    # R1: the 2026 table
    y26 = q[q.day >= dt.date(2026, 1, 1)]
    for g in ("u25", "mid", "o65"):
        t = y26[y26.seg == g]
        qq, ss = t.wt.sum(), (t.wt == 1).sum()
        check("2026 quotes " + g, qq, F["r1_rows"][g][0], 0)
        check("2026 sales " + g, ss, F["r1_rows"][g][1], 0)
        check("2026 conversion % " + g, round(ss / qq * 100, 2), F["r1_rows"][g][2], 0.005)
    seg_fig = {}
    for g in ("u25", "mid", "o65"):
        cur = sales[(sales.seg == g) & (sales.day >= FROM)]
        j = idx.loc[cur.policy_number].values
        base = cost[j].sum() / (E[j] * p.written_premium_gbp.values[j, None] * s_cost[mon][None, :]).sum()
        allg = sales[(sales.seg == g) & (sales.day >= (dt.date(2026, 2, 1) if g == "mid" else dt.date(2025, 1, 1)))]
        ja = idx.loc[allg.policy_number].values
        fitf = allg.assign(cnt=cnt[ja], expn=p.predicted_claim_frequency.values[ja]
                           * (E[ja] * (s_cnt[mon] * upto_sep)[None, :]).sum(1))
        curve, slope, ys = gap_fit(fitf)
        qs = q[(q.seg == g) & (q.day >= FROM) & (q.day <= ASAT)]
        conv = {k: (qs[qs.rk == k].wt == 1).sum() / qs[qs.rk == k].wt.sum() for k in (1, 2, 3, 4)}
        seg_fig[g] = dict(cur=cur, base=base, curve=curve, conv=conv, qs=qs, slope=slope, ys=ys)
        check("2026 base loss ratio % " + g, round(base * 100, 1), F[g + "_base_lr"], 0.05)

    def lr(g, L):
        s = seg_fig[g]
        cur = s["cur"]
        v = np.array([s["conv"][k] for k in rank_after(cur.gross.values, cur.c1.values, cur.c2.values, cur.c3.values,
                                                       L)]) / np.array([s["conv"][k] for k in cur.rk.values])
        ae = s["curve"](cur.gap.values)
        a, w = cur.risk_premium_gbp.values * ae, cur.written_premium_gbp.values
        return s["base"] * ((v * a).sum() / (v * w).sum()) / (a.sum() / w.sum()) * (1 + INFL) / (1 + L)

    def rise(g):
        return next(k for k in range(61) if lr(g, k / 100) <= TGT + 1e-12)

    def vol(g, L):
        s = seg_fig[g]
        qs = s["qs"]
        pr = np.array([s["conv"][k] for k in rank_after(qs.gross.values, qs.c1.values, qs.c2.values, qs.c3.values, L)])
        n = (qs.wt.values * pr).sum() * 12 / 9
        prem = (qs.wt.values * pr * qs.gross.values / (1 + IPT) * (1 + L)).sum() * 12 / 9
        return n, prem

    check("under-25 gap slope", round(seg_fig["u25"]["slope"], 2), F["u25_slope"], 0.005)
    check("under-25 deepest decile", round(float(seg_fig["u25"]["ys"][0]), 2), F["u25_ae_deepest"], 0.005)
    check("under-25 loss ratio % at the team's rise", round(lr("u25", prop) * 100, 1), F["u25_lr_at_proposal"], 0.05)
    ru, rm = rise("u25"), rise("mid")
    check("under-25 smallest rise", ru, F["u25_rise"], 0)
    check("25-to-64 smallest rise", rm, F["mid_rise"], 0)
    check("under-25 loss ratio % at its rise", round(lr("u25", ru / 100) * 100, 1), F["u25_lr_at_rise"], 0.05)
    check("25-to-64 loss ratio % at its rise", round(lr("mid", rm / 100) * 100, 1), F["mid_lr_at_rise"], 0.05)
    for g, L, key in (("u25", ru / 100, "u25_policies_at_rise"), ("mid", rm / 100, "mid_policies_at_rise"),
                      ("u25", prop, "u25_policies_at_proposal"), ("o65", -0.03, "o65_policies_at_cut"),
                      ("o65", 0.0, "o65_policies_at_hold")):
        check(key, round(vol(g, L)[0], -1), F[key], 10)
    check("under-25 premium £m at its rise", round(vol("u25", ru / 100)[1] / 1e6, 1), F["u25_premium_at_rise_m"], 0.05)
    check("25-to-64 premium £m at its rise", round(vol("mid", rm / 100)[1] / 1e6, 1), F["mid_premium_at_rise_m"], 0.05)

    # the over-65 cut, both sides
    txt = subprocess.run(["pdftotext", "-layout", path("PCW-COM-2026"), "-"], capture_output=True, text=True).stdout
    comm = {s: float(re.search(s + r"\s+£([0-9.]+)", txt).group(1)) for s in
            ("Kitecompare", "Covertide", "Brightquote", "Pricelark")}
    o = seg_fig["o65"]
    cur = o["cur"]
    load = np.median(cur.written_premium_gbp.values / cur.risk_premium_gbp.values)
    k = o["base"] * cur.written_premium_gbp.sum() / (cur.risk_premium_gbp.values * o["curve"](cur.gap.values)).sum()
    qs = o["qs"]

    def nb(L):
        pr = np.array([o["conv"][r] for r in rank_after(qs.gross.values, qs.c1.values, qs.c2.values, qs.c3.values, L)])
        n = pr * qs.wt.values * 12 / 9
        net = qs.gross.values / (1 + IPT)
        clm = net / load * o["curve"](qs.gap.values) * k * (1 + INFL)
        return (n * (net * (1 + L) - clm - qs.site.map(comm).values - SERV)).sum()

    ren = pd.read_csv(path("renewal_schedule"))
    mi = pd.read_excel(path("renewal_retention_mi"), sheet_name="Renewal invitations")
    x = mi["Price change on last year"].str.extract(r"([+-]?\d+)%")[0].astype(float).values / 100 + 0.01
    yv, nv = mi["Retention"].values, mi["Invitations"].values
    ok = (yv > 0) & (yv < 1) & (nv >= 30)
    A = np.polyfit(x[ok], np.log(yv[ok] / (1 - yv[ok])), 1, w=np.sqrt(nv[ok]))

    def renew(L):
        off = np.minimum(ren.intended_renewal_premium_ex_ipt_gbp.values, ren.enbp_ex_ipt_at_current_nb_rates_gbp.values * (1 + L))
        r = 1 / (1 + np.exp(-(A[0] * (off / ren.current_premium_ex_ipt_gbp.values - 1) + A[1])))
        return (r * (off - ren.renewal_risk_premium_2027_gbp.values - SERV)).sum()

    dnb, dren = nb(-0.03) - nb(0.0), renew(-0.03) - renew(0.0)
    check("over-65 cut, new business £m", round(dnb / 1e6, 2), F["cut_nb_m"], 0.005)
    check("over-65 cut, renewals £m", round(dren / 1e6, 2), F["cut_ren_m"], 0.005)
    check("over-65 cut, in all £m", round((dnb + dren) / 1e6, 2), F["cut_net_m"], 0.005)

    # the 80 per cent range, by its own draws (a different stream, so within a point)
    g = seg_fig["mid"]
    cur = g["cur"]
    L = rm / 100
    v = np.array([g["conv"][r] for r in rank_after(cur.gross.values, cur.c1.values, cur.c2.values, cur.c3.values, L)]) \
        / np.array([g["conv"][r] for r in cur.rk.values])
    npol = int(round(vol("mid", L)[0]))
    mids = set(sales[sales.seg == "mid"].policy_number)
    sev = c[c.policy_number.isin(mids) & (c.cap > 0)].cap.values * (1 + INFL)
    lam = cur.predicted_claim_frequency.values * g["curve"](cur.gap.values)
    prem = cur.written_premium_gbp.values * (1 + L)
    rng = np.random.default_rng(7)
    draws = []
    for _ in range(1500):
        ii = rng.choice(len(cur), npol, p=v / v.sum())
        draws.append(rng.choice(sev, rng.poisson(lam[ii]).sum()).sum() / prem[ii].sum())
    draws = np.array(draws) / np.mean(draws) * lr("mid", L)
    check("25-to-64 range low %", round(np.quantile(draws, 0.1) * 100, 1), F["mid_range_lo"], 1.0)
    check("25-to-64 range high %", round(np.quantile(draws, 0.9) * 100, 1), F["mid_range_hi"], 1.0)
    print("verify: %d failures" % len(bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
