"""task9 verify: an independent recomputation from the shipped files, by a different road.

pandas instead of the analysis module's readers; a cohort table of default rates by rating and years since buyout
instead of a probit; moment estimators for the dependence (the yearly default rates' excess variance for the
economy, the sector-year rates' for the sector, and the house's from joint defaults of same-house pairs in the same
sector-year, inverted through the bivariate normal); 300,000 paths. It must land on the golden's call, its latent
house correlation within 0.06 of the golden's, and both chances within a quarter of the golden's.
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import multivariate_normal, norm

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import model as MD  # noqa: E402

STATUS = {"P": "P", "W": "W", "D": "D", "R": "R", "Performing": "P", "Watchlist": "W", "Defaulted": "D", "Repaid": "R"}
RATING = {"B1": 0, "B2": 1, "B3": 2, "Caa1": 3, "B+": 0, "B": 1, "B-": 2, "CCC+": 3}
FORMS = re.compile(r"\b(gmbh|ag|sas|sa|bv|b v|nv|n v|ltd|limited|plc|ab|a s|aps|as|oy|s l|s l u|slu|sl|s p a|spa|s r l|srl|dac)\b")


def nn(s):
    s = re.sub(r"[.,/()'-]", " ", str(s).lower().replace("&", " and "))
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\s+", " ", FORMS.sub(" ", s)).strip()


def qend(p):
    m = re.fullmatch(r"(\d{4})Q([1-4])", p)
    if m:
        return pd.Timestamp(int(m.group(1)), 3 * int(m.group(2)), 1) + pd.offsets.MonthEnd(0)
    return pd.Timestamp(p)


def dparse(s):
    if not isinstance(s, str) or not s.strip():
        return pd.NaT
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y"):
        try:
            return pd.to_datetime(s, format=f)
        except ValueError:
            pass
    return pd.NaT


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    lei = pd.read_csv(os.path.join(TGT, "lei_reference_extract_2026-12-31.csv"), dtype=str).fillna("")
    lei = lei[lei.entity_category == "GENERAL"]
    name2lei = {}
    for _, r in lei.iterrows():
        name2lei[nn(r.legal_name)] = r.lei
        if r.other_names:
            name2lei[nn(r.other_names)] = r.lei
    lb = pd.read_csv(os.path.join(TGT, "lenderbase_loan_performance_2008-2026.csv"), dtype=str).fillna("")
    lb["q"] = lb.report_period.map(qend)
    lb = lb.sort_values("submission_ts").drop_duplicates(["lb_loan_id", "q"], keep="last")
    lb["st"] = lb.status.map(STATUS)
    lb["nm"] = lb.obligor_name.map(nn)
    first_lei = lb[lb.obligor_lei != ""].groupby("lb_loan_id").obligor_lei.first()
    name_mode = lb.groupby("lb_loan_id").nm.agg(lambda s: s.value_counts().index[0])
    last = lb.sort_values("q").groupby("lb_loan_id").tail(1).set_index("lb_loan_id")
    loans = pd.DataFrame({"company": [first_lei.get(i, name2lei.get(name_mode[i], "N:" + name_mode[i])) for i in last.index]},
                         index=last.index)
    loans["orig"] = last.origination_date.map(dparse)
    loans["rating"] = last.rating_at_origination.map(RATING)
    loans["sector"] = last.sector_code.str[2:].astype(int) - 1
    loans["dflt"] = np.where(last.st == "D", last.default_date.map(dparse), pd.NaT)
    ye = lb[(lb.q.dt.month == 12) & lb.st.isin(["P", "W"])][["lb_loan_id", "q"]]
    first_q = lb.groupby("lb_loan_id").q.min()

    dt_ = pd.read_csv(os.path.join(TGT, "dealtrail_buyout_transactions_1997-2026.csv"), dtype=str).fillna("")
    dt_ = dt_[(dt_.deal_status == "Completed") & dt_.deal_type.isin(["Primary buyout", "Secondary buyout"])].copy()
    dt_["date"] = dt_.completed.map(dparse)
    dt_["company"] = [r.target_lei or name2lei.get(nn(r.target), "N:" + nn(r.target)) for r in dt_.itertuples()]
    dt_["house"] = dt_.buyers.str.split(";").str[0].str.split().str[0]
    dt_ = dt_.sort_values("date")
    spells = {k: g[["date", "house"]].values.tolist() for k, g in dt_.groupby("company")}

    def spell(company, when):
        rows = [r for r in spells.get(company, []) if r[0] <= when + pd.Timedelta(days=31)]
        return rows[-1] if rows else None

    rows = []
    at_risk = set(zip(ye.lb_loan_id, ye.q.dt.year + 1))
    for lid, ln in loans.iterrows():
        sp = spell(ln.company, ln.orig)
        for y in range(2008, 2027):
            if y == 2008:
                ok = first_q[lid] <= pd.Timestamp(2008, 3, 31) and ln.orig < pd.Timestamp(2008, 1, 1)
            else:
                ok = (lid, y) in at_risk
            if not ok:
                continue
            d = int(pd.notna(ln.dflt) and ln.dflt.year == y)
            rows.append((y, ln.sector, ln.rating, max(1, y - sp[0].year), d, sp[1]))
    P = pd.DataFrame(rows, columns=["year", "sector", "rating", "age", "d", "house"])
    P["ageb"] = P.age.clip(upper=7)
    # cohort default rates by rating and age, the rating's relativity kept where a cell is thin
    rr = P.groupby("rating").d.mean()
    ar = P.groupby("ageb").d.mean() / P.d.mean()
    cell = P.groupby(["rating", "ageb"]).d.agg(["mean", "size"])
    pdt = np.zeros((4, 31))
    for r in range(4):
        for a in range(1, 31):
            ab = min(a, 7)
            prior = rr[r] * ar[ab]
            if (r, ab) in cell.index:
                m, n = cell.loc[(r, ab)]
                pdt[r, a] = (m * n + prior * 200) / (n + 200)
            else:
                pdt[r, a] = prior
    P["p"] = pdt[P.rating, P.age.clip(upper=30)]
    # economy: excess variance of yearly default rates over the binomial
    yr = P.groupby("year").agg(n=("d", "size"), dd=("d", "sum"), p=("p", "mean"))
    pbar = P.d.mean()

    def vas_var(rho, p):
        t = norm.ppf(p)
        return multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([t, t]) - p * p
    ex = np.var(yr.dd / yr.n) - np.mean(pbar * (1 - pbar) / yr.n)
    am = brentq(lambda r: vas_var(r, pbar) - ex, 1e-4, 0.9)
    # sector: joint defaults of pairs in the same sector-year against pairs across sectors in the same year
    def pairs(frame, keys):
        g = frame.groupby(keys).d.agg(["size", "sum"])
        return float((g["sum"] * (g["sum"] - 1) / 2).sum()), float((g["size"] * (g["size"] - 1) / 2).sum())
    j_y, n_y = pairs(P, ["year"])
    j_ky, n_ky = pairs(P, ["year", "sector"])
    j_hky, n_hky = pairs(P, ["year", "sector", "house"])
    q_y = j_y / n_y
    q_ky = j_ky / n_ky
    q_cross = (j_ky - j_hky) / (n_ky - n_hky)
    q_house = j_hky / n_hky
    rho_ky = brentq(lambda r: vas_var(r, pbar) + pbar * pbar - q_cross, 1e-4, 0.95)
    rho_hky = brentq(lambda r: vas_var(r, pbar) + pbar * pbar - q_house, 1e-4, 0.98)
    ak = max(rho_ky - am, 0.0)
    ah = rho_hky - rho_ky
    ch = ah / (1 - am - ak)
    ldf = pd.read_csv(os.path.join(TGT, "lenderbase_workout_recoveries_2008-2026.csv"), dtype=str).fillna("")
    ldf = ldf[ldf.recovery != ""].copy()
    ldf["r"] = ldf.recovery.astype(float).map(lambda x: x / 100 if x > 1 else x)
    ldf["y"] = ldf.default_date.str[:4].astype(int)
    lgd = 1 - ldf[ldf.y <= 2019].r.mean()
    # the recovery link, its own way: each house-year's shock by Gauss-Hermite quadrature over its company-years against
    # their cohort rates moved by the year's shock (the year's shock from the excess of its default rate), then recovery
    # on the shocks over the 2008 to 2019 workouts
    zy = {}
    for y, g in P.groupby("year"):
        dr = min(max(g.d.mean(), 1e-4), 0.5)
        zy[y] = (norm.ppf(g.p.mean()) - norm.ppf(dr)) * np.sqrt(1 - am) / np.sqrt(am)
    P["py"] = norm.cdf((norm.ppf(P.p) - np.sqrt(am) * P.year.map(zy)) / np.sqrt(1 - am))
    gh_x, gh_w = np.polynomial.hermite_e.hermegauss(60)
    gh_w = gh_w / gh_w.sum()
    c = ah / (1 - am)
    zh = {}
    for (h, y), g in P.groupby(["house", "year"]):
        t = norm.ppf(g.py.values.clip(1e-6, 1 - 1e-6))
        pz = norm.cdf((t[:, None] - np.sqrt(c) * gh_x[None, :]) / np.sqrt(1 - c))
        lk = np.prod(np.where(g.d.values[:, None] == 1, pz, 1 - pz), axis=0) * gh_w
        zh[(h, y)] = float((lk * gh_x).sum() / lk.sum())
    lid2 = {lid: (ln.company, ln.orig) for lid, ln in loans.iterrows()}
    X_, y_ = [], []
    for r in ldf.itertuples():
        if r.y > 2019 or r.lb_loan_id not in lid2:
            continue
        sp = spell(*lid2[r.lb_loan_id])
        if sp is None or (sp[1], r.y) not in zh:
            continue
        X_.append([1.0, zy[r.y], zh[(sp[1], r.y)]])
        y_.append(r.r)
    bl = np.linalg.lstsq(np.array(X_), np.array(y_), rcond=None)[0]
    link = (float(bl[0]), float(bl[1]), float(bl[2]))
    fx = pd.read_csv(os.path.join(TGT, "ecb_euro_reference_rates_2026-12.csv"))
    fx = fx[fx.Date == "2026-12-31"].iloc[0].to_dict()
    fx["EUR"] = 1.0
    out = {}
    hid = {h: i for i, h in enumerate(sorted(set(dt_.house)))}
    for key, fn, sheet, cols in (("KL", "klcp_static_portfolio_2026-12-31.xlsx", "Portfolio", ("Obligor", "LEI", "Industry", "Currency", "Par (m)", "Rating (Moody's equivalent)")),
                                 ("OS", "ostvale_collateral_tape_20261231.xlsx", "Collateral", ("Borrower", "Borrower LEI", "GICS industry group", "CCY", "Commitment (CCY m)", "S&P equivalent"))):
        t = pd.read_excel(os.path.join(TGT, fn), sheet_name=sheet, header=3)
        sec = json.load(open(os.path.join(TGT, "lenderbase_sector_codes.json")))["sectors"]
        smap = {s["agency_industry"]: int(s["code"][2:]) - 1 for s in sec}
        smap.update({s["gics_industry_group"]: int(s["code"][2:]) - 1 for s in sec})
        comp = [(str(l) if isinstance(l, str) and l else name2lei.get(nn(n), "N:" + nn(n))) for n, l in zip(t[cols[0]], t[cols[1]])]
        sp = [spell(c, pd.Timestamp(2026, 12, 31)) for c in comp]
        port = dict(w=(t[cols[4]] / t[cols[3]].map(fx)).values.astype(float), r=t[cols[5]].map(RATING).values,
                    a=np.array([max(1, 2027 - s[0].year) for s in sp]), k=t[cols[2]].map(smap).values,
                    h=np.array([hid[s[1]] for s in sp]), f=np.array([hid[s[1]] for s in sp]))
        port["w"] = port["w"] / port["w"].sum()
        cum = MD.simulate(port, pdt, am=am, ak=ak, ah=ah, lgd=lgd, nsim=300_000, seed=77, link=link)
        out[key] = float((cum[-1] > 0.15).mean())
    gk, go = F["golden"]["KL"]["p5_raw"], F["golden"]["OS"]["p5_raw"]
    ok_k, ok_o = out["KL"] < 0.01, out["OS"] < 0.01
    callv = ("Kestrel Lane" if out["KL"] < out["OS"] else "Ostvale") if (ok_k and ok_o) else \
        "Kestrel Lane" if ok_k else "Ostvale" if ok_o else "neither"
    print("verify: company-years %d defaults %d | am %.3f ak %.3f house %.3f (golden %.3f) lgd %.3f | link %.3f %.3f %.3f "
          "(golden %.3f %.3f %.3f) | KL %.2f (golden %.2f) OS %.2f (golden %.2f) | call %s | same-house pair rate %.4f, "
          "cross-house %.4f"
          % (len(P), P.d.sum(), am, ak, ch, F["estimates"]["ch"], lgd, link[0], link[1], link[2], F["link"]["a"],
             F["link"]["bm"], F["link"]["bh"], 100 * out["KL"], 100 * gk, 100 * out["OS"], 100 * go, callv, q_house, q_cross))
    ok = (len(P) == F["panel"]["company_years"] and int(P.d.sum()) == F["panel"]["defaults"] and callv == F["call"] == "neither"
          and abs(ch - F["estimates"]["ch"]) < 0.06 and abs(out["KL"] - gk) < 0.35 * gk and abs(out["OS"] - go) < 0.35 * go
          and abs(100 * lgd - F["lgd"]["lgd_pct"]) < 0.06)
    print("VERIFY", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
