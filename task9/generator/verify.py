"""task9 verify: an independent recomputation from the shipped files, by a different road.

pandas instead of the analysis module's readers; a cohort table of default rates by rating and years since buyout
instead of a probit; each sector's loading on the year from pair moments (company pairs at risk in the same year in
different sectors and under different houses, inverted through the bivariate normal at each sector's own default
rate, one loading per sector fitted to the correlations); the sector-year's share from same-sector cross-house pairs;
the house's share by its own Gauss-Hermite fit on house-years against cohort sector-year rates; its own recovery
link; 300,000 paths. It must land on the golden's call with both notes over the test.
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
    # each sector's loading on the year: pairs in different sectors, at risk in the same year, under different houses
    def bvn(a, b, r):
        return float(multivariate_normal(mean=[0, 0], cov=[[1, r], [r, 1]]).cdf([a, b]))
    sec_rate = P.groupby("sector").d.mean().clip(1e-4, 0.5)
    tsec = norm.ppf(sec_rate)
    n_sy = P.pivot_table(index="sector", columns="year", values="d", aggfunc="size", fill_value=0).values.astype(float)
    d_sy = P.pivot_table(index="sector", columns="year", values="d", aggfunc="sum", fill_value=0).values.astype(float)
    Npair, Jpair = n_sy @ n_sy.T, d_sy @ d_sy.T
    hy = P.groupby(["house", "year", "sector"]).d.agg(["size", "sum"]).reset_index()
    for (h, y), g in hy.groupby(["house", "year"]):
        n_ = np.zeros(16)
        j_ = np.zeros(16)
        n_[g.sector.values] = g["size"].values
        j_[g.sector.values] = g["sum"].values
        Npair -= np.outer(n_, n_)
        Jpair -= np.outer(j_, j_)
    pairs, rho, wts = [], [], []
    for a in range(16):
        for b in range(a + 1, 16):
            q = Jpair[a, b] / Npair[a, b]
            lo_, hi_ = bvn(tsec[a], tsec[b], -0.3) - q, bvn(tsec[a], tsec[b], 0.9) - q
            r = brentq(lambda x: bvn(tsec[a], tsec[b], x) - q, -0.3, 0.9) if lo_ < 0 < hi_ else (0.9 if hi_ <= 0 else -0.3)
            pairs.append((a, b))
            rho.append(r)
            wts.append(np.sqrt(Npair[a, b]))
    from scipy.optimize import least_squares
    pairs, rho, wts = np.array(pairs), np.array(rho), np.array(wts)
    fit = least_squares(lambda x: wts * (x[pairs[:, 0]] * x[pairs[:, 1]] - rho), np.full(16, 0.2), bounds=(0, 0.8))
    lv = np.clip(fit.x ** 2, 0, 0.6)
    # the sector-year's share: same sector, same year, different houses, against the sector's own loading
    ks, kw = [], []
    for s_ in range(16):
        g = P[P.sector == s_]
        a = g.groupby("year").d.agg(["size", "sum"])
        ah_ = g.groupby(["year", "house"]).d.agg(["size", "sum"])
        n_c = float((a["size"] * (a["size"] - 1) / 2).sum() - (ah_["size"] * (ah_["size"] - 1) / 2).sum())
        j_c = float((a["sum"] * (a["sum"] - 1) / 2).sum() - (ah_["sum"] * (ah_["sum"] - 1) / 2).sum())
        t = tsec[s_]
        q = j_c / n_c
        r = brentq(lambda x: bvn(t, t, x) - q, -0.3, 0.95) if bvn(t, t, -0.3) < q < bvn(t, t, 0.95) else 0.0
        ks.append(max(r - lv[s_], 0.0))
        kw.append(n_c)
    k = float(np.average(ks, weights=kw))
    # the house's share: each house-year's defaults against its companies' cohort rates moved by their sector-year's
    # own experience, the house shock integrated by Gauss-Hermite, the share on the latent scale
    gh_x, gh_w = np.polynomial.hermite_e.hermegauss(40)
    gh_w = gh_w / gh_w.sum()
    sy = P.groupby(["sector", "year"]).agg(dd=("d", "sum"), n=("d", "size"), p=("p", "mean"))
    P["psy"] = [(sy.loc[(s_, y), "dd"] + 4 * sy.loc[(s_, y), "p"]) / (sy.loc[(s_, y), "n"] + 4) for s_, y in zip(P.sector, P.year)]
    P["pky"] = norm.cdf(norm.ppf(P.p.clip(1e-6, 1 - 1e-6)) + norm.ppf(P.psy.clip(1e-6, 1 - 1e-6)) - norm.ppf(
        P.groupby(["sector", "year"]).p.transform("mean").clip(1e-6, 1 - 1e-6)))
    room = 1 - lv[P.sector.values] - k
    groups = [g.index.values for _, g in P.groupby(["house", "year"]) if len(g) >= 2]
    tk_ = norm.ppf(P.pky.values.clip(1e-6, 1 - 1e-6))
    dv = P.d.values

    def nll(ah_):
        tot = 0.0
        for gi in groups:
            c = np.clip(ah_ / room[gi], 1e-6, 0.999)
            pu = norm.cdf((tk_[gi][:, None] - np.sqrt(c)[:, None] * gh_x[None, :]) / np.sqrt(1 - c)[:, None])
            lk = np.where(dv[gi][:, None] == 1, pu, 1 - pu)
            tot += np.log(max((np.prod(lk, axis=0) * gh_w).sum(), 1e-300))
        return -tot
    from scipy.optimize import minimize_scalar
    ah = float(minimize_scalar(nll, bounds=(1e-3, 0.6), method="bounded", options={"xatol": 1e-4}).x)
    ldf = pd.read_csv(os.path.join(TGT, "lenderbase_workout_recoveries_2008-2026.csv"), dtype=str).fillna("")
    ldf = ldf[ldf.recovery != ""].copy()
    ldf["r"] = ldf.recovery.astype(float).map(lambda x: x / 100 if x > 1 else x)
    ldf["y"] = ldf.default_date.str[:4].astype(int)
    lgd = 1 - ldf[ldf.y <= 2019].r.mean()
    # the recovery link, its own way: each house-year's shock by Gauss-Hermite quadrature over its company-years against
    # their cohort rates moved by the year's shock (the year's shock from the excess of its default rate), then recovery
    # on the shocks over the 2008 to 2019 workouts
    lbar = float(np.average(lv[P.sector.values]))
    zy = {}
    for y, g in P.groupby("year"):
        dr = min(max(g.d.mean(), 1e-4), 0.5)
        zy[y] = (norm.ppf(g.p.mean()) - norm.ppf(dr)) * np.sqrt(1 - lbar) / np.sqrt(lbar)
    gh_x, gh_w = np.polynomial.hermite_e.hermegauss(60)
    gh_w = gh_w / gh_w.sum()
    P["c"] = np.clip(ah / room, 1e-6, 0.999)
    zh = {}
    for (h, y), g in P.groupby(["house", "year"]):
        t = norm.ppf(g.pky.values.clip(1e-6, 1 - 1e-6))
        c = g.c.values[:, None]
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
    for key, fn, sheet, cols in (("KL", "klcp_static_portfolio_2026-12-31.xlsx", "Portfolio", ("Obligor", "LEI", "Industry", "Currency", "Par (m)", "Rating at origination (Moody's equivalent)")),
                                 ("OS", "ostvale_collateral_tape_20261231.xlsx", "Collateral", ("Borrower", "Borrower LEI", "GICS industry group", "CCY", "Commitment (CCY m)", "S&P equivalent at close"))):
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
        cum = MD.simulate(port, pdt, am=lv, ak=k, ah=ah, lgd=lgd, nsim=300_000, seed=77, link=link)
        out[key] = float((cum[-1] > {"KL": 0.150, "OS": 0.165}[key]).mean())
    gk, go = F["golden"]["KL"]["p5_raw"], F["golden"]["OS"]["p5_raw"]
    ok_k, ok_o = out["KL"] < 0.01, out["OS"] < 0.01
    callv = ("Kestrel Lane" if out["KL"] < out["OS"] else "Ostvale") if (ok_k and ok_o) else \
        "Kestrel Lane" if ok_k else "Ostvale" if ok_o else "neither"
    print("verify: company-years %d defaults %d | loadings %s k %.3f house %.3f (golden %.3f) lgd %.3f | link %.3f %.3f %.3f "
          "(golden %.3f %.3f %.3f) | KL %.2f (golden %.2f) OS %.2f (golden %.2f) | call %s"
          % (len(P), P.d.sum(), np.round(lv, 2).tolist(), k, ah, F["house_share"], lgd, link[0], link[1], link[2],
             F["link"]["a"], F["link"]["bm"], F["link"]["bh"], 100 * out["KL"], 100 * gk, 100 * out["OS"], 100 * go, callv))
    sw = [i_ for i_ in range(16) if lv[i_] > 0.10]
    ok = (len(P) == F["panel"]["company_years"] and int(P.d.sum()) == F["panel"]["defaults"] and callv == F["call"] == "neither"
          and out["KL"] > 0.011 and out["OS"] > 0.011 and abs(100 * lgd - F["lgd"]["lgd_pct"]) < 0.06
          and len(sw) == len(F["sectors"]["swing"]))
    print("VERIFY", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
