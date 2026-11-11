"""The December 2026 quarter projected from the register as extracted at the close of 27 November 2026.

Every dwelling let on 31 December 2025 is carried to 31 December 2026 from the state the extract shows it in on the
cut day: a tenancy on file as in place then stays to the year's end, or ends and the dwelling is re-let or stands
empty, at the rates the same weeks of 2023, 2024 and 2025 showed when the register is read as it stood on their own
27 November, by the tenancy's age and its landlord's class; a dwelling not shown as let on the cut day is let by the
year's end at the rate those years showed. A tenancy that stays is priced at its rent payable on 31 December (the
panel's rates at any anniversary, the operators' recorded reviews, with an operator review still being lodged on the
cut day completed at the rise its lodged bonds show); a dwelling let afresh is priced at its going rent, its last
letting rent carried by the register's own index of new lettings."""
import numpy as np
import pandas as pd

import measure as MS

AGE_BANDS = [0, 335, 400, 730, 100000]     # days since the tenancy began: under 11 months, the twelfth, to two years, after


def letting_index(E, by="region"):
    """Monthly index of new-letting rents by region from the register: the log rent of each new tenancy against the
    dwelling's own previous letting, chained month to month (a repeat-letting index), so the dwelling mix drops out."""
    T = E.T
    df = pd.DataFrame({"dw": E.dw, "start": E.start, "rent": E.rent0, "ri": E.ri})
    df = df.sort_values(["dw", "start"], kind="stable")
    prev = df.groupby("dw").shift(1)
    ok = prev["rent"].notna() & (df["start"] - prev["start"] > 60)
    p = df[ok].copy()
    p["m1"] = pd.to_datetime(prev.loc[ok, "start"], unit="D").dt.to_period("M")
    p["m2"] = pd.to_datetime(p["start"], unit="D").dt.to_period("M")
    p["lr"] = np.log(p["rent"] / prev.loc[ok, "rent"])
    p = p[(p["m2"] >= pd.Period("2016-01", "M"))]
    months = pd.period_range("2016-01", "2026-11", freq="M")
    midx = {m: k for k, m in enumerate(months)}
    p = p[p["m1"].isin(midx) & p["m2"].isin(midx)]
    out = {}
    for ri in range(len(MS.REGIONS)):
        s = p[p["ri"] == ri]
        # least squares on month dummies: lr = I[m2] - I[m1], I[first] = 0 (a repeat-sales regression)
        a = s["m1"].map(midx).values
        b = s["m2"].map(midx).values
        n = len(months)
        # normal equations for a sparse difference design, solved densely (132 unknowns)
        A = np.zeros((n, n))
        y = np.zeros(n)
        w = np.ones(len(a))
        np.add.at(A, (b, b), w)
        np.add.at(A, (a, a), w)
        np.add.at(A, (a, b), -w)
        np.add.at(A, (b, a), -w)
        np.add.at(y, b, s["lr"].values)
        np.add.at(y, a, -s["lr"].values)
        A[0, :] = 0
        A[0, 0] = 1
        y[0] = 0
        A = A + np.eye(n) * 1e-6
        idx = np.linalg.solve(A, y)
        out[ri] = pd.Series(idx, index=months)
    return out


def index_gap(ix, ris, starts, hold="trend"):
    """Index at December 2026 less the index at each start month, per region, vectorised."""
    months = ix[0].index
    base = months[0]
    st = pd.to_datetime(starts, unit="D")
    mstart = (st.year.values - base.year) * 12 + (st.month.values - base.month)
    mstart = np.clip(mstart, 0, len(months) - 1)
    out = np.zeros(len(ris))
    for r in np.unique(ris):
        arr = ix[r].values
        last3 = arr[-4:]
        slope = (last3[-1] - last3[0]) / 3.0 if hold == "trend" else 0.0
        dec = arr[-1] + slope * 1
        k = ris == r
        out[k] = dec - arr[mstart[k]]
    return out


def _index_at(ix, ri, period, hold="trend"):
    s = ix[ri]
    if period <= s.index[-1]:
        return float(s.loc[period])
    last3 = s.iloc[-4:]
    slope = (last3.iloc[-1] - last3.iloc[0]) / 3.0 if hold == "trend" else 0.0
    k = (period - s.index[-1]).n
    return float(s.iloc[-1] + slope * k)


def landlord_class(E, idx):
    """0 small landlords and companies, 1 the build-to-rent operators, 2 rooms let by the student operator."""
    room = (E.T["dtype"].values[idx] == "room")
    return np.where(E.op[idx], np.where(room, 2, 1), 0)


def _bands(cut, starts):
    return np.searchsorted(AGE_BANDS, cut - starts, side="right") - 1


def rates(E, cut_md=(11, 27), years=(2023, 2024, 2025), by_class=True):
    """The same weeks of earlier years read as the register stood on their own cut day. For dwellings let on the
    earlier 31 December: of the tenancies the register then showed in place, the share still in place on 31 December
    (by age band and landlord class) and, of those that were not, the share of dwellings let again by then; of the
    dwellings the register then showed as not let, the share let on 31 December. Outcomes are read from E."""
    key = ("rates", cut_md, tuple(years), by_class)
    if key in E._cache:
        return E._cache[key]
    rs, rv = [], []
    kpos = pd.Series(np.arange(E.n), index=E.key)
    for y in years:
        cut = MS.day(y, *cut_md)
        ye, t1 = MS.day(y, 12, 31), MS.day(y - 1, 12, 31)
        Ec = E.as_of(cut)
        A = E.in_place(t1)
        dk = E.dw_uniques[A.index.values]
        C = Ec.in_place(cut)
        ckey = pd.Series(Ec.key[C.values], index=Ec.dw_uniques[C.index.values])
        F = E.in_place(ye)
        fkey = pd.Series(E.key[F.values], index=E.dw_uniques[F.index.values])
        has = pd.Index(dk).isin(ckey.index)
        hk = dk[has]
        ii = kpos.reindex(ckey.loc[hk].values).values
        okk = ~np.isnan(ii)
        ii = ii[okk].astype(int)
        hk = hk[okk]
        band = _bands(cut, E.start[ii])
        cls = landlord_class(E, ii) if by_class else np.zeros(len(ii), int)
        stay = fkey.reindex(hk).values == ckey.loc[hk].values
        let = pd.Index(hk).isin(fkey.index)
        rs.append(pd.DataFrame({"band": band, "cls": cls, "stay": stay, "let": let}))
        rv.append(pd.DataFrame({"let": pd.Index(dk[~has]).isin(fkey.index)}))
    S, V = pd.concat(rs), pd.concat(rv)
    out = (S.groupby(["band", "cls"])["stay"].mean().to_dict(), S[~S["stay"]].groupby("cls")["let"].mean().to_dict(),
           float(V["let"].mean()))
    E._cache[key] = out
    return out


def rates_hindsight(E, cut_md=(11, 27), years=(2023, 2024, 2025), by_class=True):
    """A rival: the same weeks read with hindsight (tenancies truly in place on the cut day, whatever the register
    then showed)."""
    key = ("rates_h", cut_md, tuple(years), by_class)
    if key in E._cache:
        return E._cache[key]
    rows_same, rows_vac = [], []
    lodged = E.T["lodged"].values
    for y in years:
        cut = MS.day(y, *cut_md)
        ye = MS.day(y, 12, 31)
        m = (E.start <= cut) & (E.end >= cut) & (lodged <= cut)
        idx = np.flatnonzero(m)
        band = _bands(cut, E.start[idx])
        cls = landlord_class(E, idx)
        stay = E.end[idx] >= ye
        letd = pd.Index(E.in_place(ye).index)
        let = np.isin(E.dw[idx], letd)
        rows_same.append(pd.DataFrame({"band": band, "cls": cls if by_class else 0, "stay": stay, "let": let}))
        inpl = set(E.dw[idx])
        j = np.flatnonzero((E.end < cut) & (E.end >= cut - 90) & (lodged <= cut))
        dws = pd.Series(E.dw[j]).drop_duplicates()
        dws = dws[~dws.isin(inpl)]
        rows_vac.append(pd.DataFrame({"let": dws.isin(letd).values}))
    S, V = pd.concat(rows_same), pd.concat(rows_vac)
    out = (S.groupby(["band", "cls"])["stay"].mean().to_dict(), S[~S["stay"]].groupby(["cls"])["let"].mean().to_dict(),
           float(V["let"].mean()))
    E._cache[key] = out
    return out


def review_schedule(E, back=(2023, 2024, 2025), cpi=None):
    key = ("sched", tuple(back), cpi is not None)
    if key in E._cache:
        return E._cache[key]
    E._cache[key] = _review_schedule(E, back, cpi)
    return E._cache[key]


def quarter_before(y, mo, dd, k):
    """The k-th latest consumers price index quarter published before day (y, mo, dd); a quarter's figure is out
    three weeks after it ends."""
    rd = MS.day(y, mo, dd)
    found = []
    yy, qq = y, 4
    while len(found) < k:
        if MS.quarter_end(yy, qq) + 21 <= rd:
            found.append((yy, qq))
        qq -= 1
        if qq == 0:
            yy, qq = yy - 1, 4
    return found[-1]


def _review_schedule(E, back, cpi):
    """Each operator's portfolio review as its additional bonds show it: the day of year the reviews take effect on;
    the shortest run (days since the tenancy began) among the tenancies reviewed on that day in earlier years; and,
    with the price index release, the published quarter whose annual change the reviews follow most closely and the
    margin over it (the mean of the median review rise less that quarter's change)."""
    tp = E.tops[E.tops["effective"].notna()]
    tp = tp[E.op[tp["i"].values]]
    land = E.T["landlord_id"].values
    out = {}
    for lid in np.unique(land[tp["i"].values]):
        t = tp[land[tp["i"].values] == lid]
        d = pd.to_datetime(t["effective"], unit="D")
        md = (d.dt.month * 100 + d.dt.day).value_counts()
        if not len(md) or md.iloc[0] < 200:
            continue
        mo, dd = divmod(int(md.index[0]), 100)
        shortest, rises = None, {}
        for y in back:
            rd = MS.day(y, mo, dd)
            got = t[t["effective"] == rd].sort_values("i")
            if len(got):
                run = int((rd - E.start[got["i"].values]).min())
                shortest = run if shortest is None else min(shortest, run)
                prev = E.recorded_rent(got["i"].values, rd - 1)
                rises[y] = 100 * float(np.median(got["rent"].values / prev - 1))
        rule = None
        if cpi and rises:
            best = None
            for k in range(1, 5):
                diffs = [r - cpi[quarter_before(y, mo, dd, k)] for y, r in rises.items()
                         if quarter_before(y, mo, dd, k) in cpi]
                if len(diffs) == len(rises):
                    sd = float(np.std(diffs))
                    if best is None or sd < best[0] - 1e-9:
                        best = (sd, k, float(np.mean(diffs)))
            rule = (best[1], best[2]) if best else None
        if shortest is not None:
            out[lid] = (mo, dd, shortest, rule, rises)
    return out


def pending_reviews(E, cut, sched):
    """Operator tenancies on file on the cut day whose review fell in the eight weeks before it and whose additional
    bond is not yet lodged: the factor the review's lodged bonds show (their median rise), by tenancy."""
    land = E.T["landlord_id"].values
    fac = {}
    y = MS.ymd(cut)[0]
    for lid, (mo, dd, shortest, rule, _) in sched.items():
        rd = MS.day(y, mo, dd)
        if not (cut - 56 <= rd <= cut):
            continue
        t = E.tops[(E.tops["effective"] == rd) & (land[E.tops["i"].values] == lid)].sort_values("i")
        if not len(t):
            continue
        prev = E.recorded_rent(t["i"].values, rd - 1)
        rise = float(np.median(t["rent"].values / prev))
        inpl = np.flatnonzero((E.start < rd) & (E.end >= cut) & (land == lid) & (rd - E.start >= shortest))
        done = set(t["i"].values)
        for i in inpl:
            if i not in done:
                fac[int(i)] = rise
    return fac


def scheduled_reviews(E, cut, t2, sched, cpi):
    """Operator reviews that fall after the cut day and by t2: the factor the operator's rule gives (the published
    price index quarter it follows plus its margin) for its tenancies on file on the cut day that will have run long
    enough by the review day."""
    land = E.T["landlord_id"].values
    fac = {}
    y = MS.ymd(t2)[0]
    for lid, (mo, dd, shortest, rule, _) in sched.items():
        rd = MS.day(y, mo, dd)
        if rule is None or not (cut < rd <= t2):
            continue
        k, margin = rule
        q = quarter_before(y, mo, dd, k)
        f = 1 + (cpi[q] + margin) / 100.0
        for i in np.flatnonzero((E.start < rd) & (E.end >= cut) & (land == lid) & (rd - E.start >= shortest)):
            fac[int(i)] = f
    return fac


def project(E, CL, t1=None, t2=None, cut=None, hold="trend", by_class=True, ix=None, rate_years=(2023, 2024, 2025),
            rate_E=None, how="as_of", complete=True, ops_from="recorded", small_from="model", sched=None, cpi=None,
            scheduled=True):
    """The expected measure on 31 December from the register as it stood on the cut day (E). rate_E is the register
    the earlier years' rates are read from (E itself for the December 2026 projection)."""
    t1 = t1 or MS.day(2025, 12, 31)
    t2 = t2 or MS.day(2026, 12, 31)
    cut = cut or MS.day(2026, 11, 27)
    ix = ix or letting_index(E)
    RE = rate_E if rate_E is not None else E
    rt = rates(RE, years=rate_years, by_class=by_class) if how == "as_of" else \
        rates_hindsight(RE, years=rate_years, by_class=by_class)
    p_stay, p_new, p_vac = rt
    A = E.in_place(t1)
    dws = A.index.values
    i1 = A.values
    r1 = E.rent_on(i1, t1, CL, small_from, ops_from)
    C = E.in_place(cut)
    has = np.isin(dws, C.index.values)
    ic = np.where(has, C.reindex(dws).fillna(-1).values, -1).astype(int)
    prob_let = np.zeros(len(dws))
    exp_rent = np.zeros(len(dws))
    last_i = np.where(has, ic, i1)
    going = E.rent0[last_i] * np.exp(index_gap(ix, E.ri[last_i], E.start[last_i], hold))
    k = np.flatnonzero(has)
    if len(k):
        ii = ic[k]
        band = _bands(cut, E.start[ii])
        cls = landlord_class(E, ii) if by_class else np.zeros(len(ii), int)
        ps = np.array([p_stay.get((b, c), p_stay.get((b, 0), 0.95)) for b, c in zip(band, cls)])
        pn = np.array([p_new.get(c, p_new.get(0, 0.3)) for c in cls])
        stay_rent = E.rent_on(ii, t2, CL, small_from, ops_from)
        if ops_from == "recorded" and (complete or scheduled):
            sc = sched if sched is not None else review_schedule(RE, cpi=cpi)
            fac = pending_reviews(E, cut, sc) if complete else {}
            if scheduled and cpi:
                fac2 = scheduled_reviews(E, cut, t2, sc, cpi)
                for i_, f_ in fac2.items():
                    fac[i_] = fac.get(i_, 1.0) * f_
            if fac:
                f = np.array([fac.get(int(i), 1.0) for i in ii])
                stay_rent = stay_rent * f
        prob_let[k] = ps + (1 - ps) * pn
        exp_rent[k] = (ps * stay_rent + (1 - ps) * pn * going[k]) / np.maximum(prob_let[k], 1e-9)
    v = np.flatnonzero(~has)
    if len(v):
        prob_let[v] = p_vac
        exp_rent[v] = going[v]
    reg = E.ri[i1]
    out = {}
    for gi_, g in enumerate(["NAT"] + MS.REGIONS):
        mk = np.ones(len(dws), bool) if g == "NAT" else (reg == gi_ - 1)
        out[g] = 100 * ((prob_let[mk] * exp_rent[mk]).sum() / (prob_let[mk] * r1[mk]).sum() - 1)
    # each group's expected contribution to the national figure (2.5): the same tenancy on both days, or another
    base = (prob_let * r1).sum()
    cont = np.zeros(len(dws))
    rel = np.zeros(len(dws))
    if len(k):
        same = ic[k] == i1[k]
        stay_part = ps * (stay_rent - r1[k])
        new_part = (1 - ps) * pn * (going[k] - r1[k])
        cont[k] = np.where(same, stay_part, 0.0)
        rel[k] = np.where(same, 0.0, stay_part) + new_part
    if len(v):
        rel[v] = p_vac * (going[v] - r1[v])
    out["_parts"] = {"continuing": 100 * cont.sum() / base, "relet": 100 * rel.sum() / base}
    return out
