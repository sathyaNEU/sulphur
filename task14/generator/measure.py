"""The measure on a conformed register: the rent panel's review rates, every tenancy's rent payable on a day, and the
matched-dwelling comparison of the methods note 2.4 with its 2.5 breakdowns."""
import datetime as dt

import numpy as np
import pandas as pd

REGIONS = ["HC", "HN", "HE", "HS", "KC", "MV", "WS"]
EPOCH = dt.date(1970, 1, 1)
Y0, Y1 = 1995, 2027


def day(y, m, d):
    return (dt.date(y, m, d) - EPOCH).days


def ymd(n):
    d = EPOCH + dt.timedelta(days=int(n))
    return d.year, d.month, d.day


def quarter_end(y, q):
    return {1: day(y, 3, 31), 2: day(y, 6, 30), 3: day(y, 9, 30), 4: day(y, 12, 31)}[q]


def quarters(first=(2022, 1), last=(2026, 3)):
    out = []
    y, q = first
    while (y, q) <= last:
        out.append((y, q))
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


# ------------------------------------------------------------------------------------------------ the panel
def panel_pairs(PN):
    """Each panel tenancy's rent either side of one anniversary: (year, region, weight, factor, rose)."""
    R = PN[PN["response"] == "R"].copy()
    R["rd"] = (pd.to_datetime(R["reference_date"]) - pd.Timestamp("1970-01-01")).dt.days
    R["sd"] = (pd.to_datetime(R["tenancy_start"]) - pd.Timestamp("1970-01-01")).dt.days
    R["rent"] = R["weekly_rent"].astype(float)
    R["w"] = R["design_weight"].astype(float)
    R = R.sort_values(["dwelling_ref", "rd"], kind="stable")
    nxt = R.groupby("dwelling_ref").shift(-1)
    ok = nxt["rd"].notna() & (nxt["sd"] == R["sd"])
    a = R[ok]
    b = nxt[ok]
    sm = pd.to_datetime(a["tenancy_start"])
    rows = []
    for rd1, rd2, s, r1, r2, reg, w, ref in zip(a["rd"].values, b["rd"].values, sm, a["rent"].values,
                                                b["rent"].values, a["region"].values, a["w"].values,
                                                a["dwelling_ref"].values):
        y1 = ymd(rd1)[0]
        y2 = ymd(rd2)[0]
        hits = []
        for y in range(y1, y2 + 1):
            if y <= s.year:
                continue
            try:
                an = (dt.date(y, s.month, s.day) - EPOCH).days
            except ValueError:
                an = (dt.date(y, s.month, 28) - EPOCH).days
            if rd1 < an <= rd2:
                hits.append(y)
        if len(hits) == 1:
            f = r2 / r1
            rows.append((hits[0], reg, w, f, f > 1.0 + 1e-9, ref))
    return pd.DataFrame(rows, columns=["year", "region", "w", "factor", "rose", "dwelling_ref"])


def review_model(pairs, by_region=True, weighted=True, first_year=2018, last_year=2026):
    """m[(year, region)]: the mean factor at an anniversary; p[(year, region)]: the share with a rise."""
    m, p = {}, {}
    w = pairs["w"] if weighted else pd.Series(1.0, index=pairs.index)
    df = pairs.assign(ww=w)
    for y in range(first_year, last_year + 1):
        sub = df[df["year"] == y]
        nat_m = (sub["ww"] * sub["factor"]).sum() / sub["ww"].sum()
        nat_p = (sub["ww"] * sub["rose"]).sum() / sub["ww"].sum()
        for r in REGIONS:
            s = sub[sub["region"] == r] if by_region else sub
            if len(s) >= 20:
                m[(y, r)] = (s["ww"] * s["factor"]).sum() / s["ww"].sum()
                p[(y, r)] = (s["ww"] * s["rose"]).sum() / s["ww"].sum()
            else:
                m[(y, r)], p[(y, r)] = nat_m, nat_p
    for y in range(Y0, first_year):
        for r in REGIONS:
            m[(y, r)], p[(y, r)] = m[(first_year, r)], p[(first_year, r)]
    for y in range(last_year + 1, Y1 + 1):
        for r in REGIONS:
            m[(y, r)], p[(y, r)] = m[(last_year, r)], p[(last_year, r)]
    return m, p


def cumlog(m):
    """CL[r][y] = sum of log m over years Y0..y."""
    CL = np.zeros((len(REGIONS), Y1 - Y0 + 2))
    for ri, r in enumerate(REGIONS):
        acc = 0.0
        for y in range(Y0, Y1 + 1):
            acc += np.log(m[(y, r)])
            CL[ri, y - Y0 + 1] = acc
    return CL


# ------------------------------------------------------------------------------------------------ the engine
class Engine:
    def __init__(self, T, tops):
        self.T = T.reset_index(drop=True)
        self.tops_raw = tops
        self._cache = {}
        T = self.T
        self.n = len(T)
        st = pd.to_datetime(T["start"], unit="D")
        self.sy = st.dt.year.values
        md = st.dt.month.values * 100 + st.dt.day.values
        md = np.where(md == 229, 228, md)
        self.md = md
        self.ri = T["region"].map({r: i for i, r in enumerate(REGIONS)}).fillna(0).astype(int).values
        self.op = T["operator"].values.astype(bool)
        self.rent0 = T["rent0"].values.astype(float)
        self.start = T["start"].values
        self.end = T["end"].values
        self.dw_key = T["dwelling"].values
        self.dw, self.dw_uniques = pd.factorize(T["dwelling"])
        self.key = T["key"].values
        pos = {k: i for i, k in enumerate(self.key)}
        tp = tops.copy()
        tp["i"] = tp["key"].map(pos)
        tp = tp[tp["i"].notna()].copy()
        tp["i"] = tp["i"].astype(int)
        tp["when"] = np.where(tp["effective"].notna(), tp["effective"], tp["day"])
        self.tops = tp.sort_values(["i", "when"], kind="stable")
        self._inplace = {}

    def as_of(self, cut):
        """The register as it stood at the close of a cut day: only tenancies and additional bonds lodged by then, and
        nothing known of a refund after it (2.2 applied to what was on file)."""
        if ("as_of", cut) in self._cache:
            return self._cache[("as_of", cut)]
        T = self.T[self.T["lodged"] <= cut].copy()
        T["refund"] = np.where(T["refund"] <= cut, T["refund"], np.nan)
        T = T.sort_values(["dwelling", "start", "lodged"], kind="stable").reset_index(drop=True)
        nxt = T.groupby("dwelling")["start"].shift(-1)
        end = (T["refund"] - 1).values
        end = np.where(nxt.notna().values & (nxt.values - 1 < np.nan_to_num(end, nan=1e9)), nxt.values - 1, end)
        T["end"] = pd.Series(end).fillna(1e9).values
        tp = self.tops_raw[self.tops_raw["day"] <= cut]
        E = Engine(T, tp)
        self._cache[("as_of", cut)] = E
        return E

    def in_place(self, t):
        if t in self._inplace:
            return self._inplace[t]
        m = (self.start <= t) & (self.end >= t)
        idx = np.flatnonzero(m)
        df = pd.DataFrame({"i": idx, "dw": self.dw[idx], "s": self.start[idx]})
        df = df.sort_values(["dw", "s"], kind="stable").drop_duplicates("dw", keep="last")
        out = df.set_index("dw")["i"]
        self._inplace[t] = out
        return out

    def last_anniv_year(self, idx, t):
        if np.ndim(t):
            dd = pd.to_datetime(np.asarray(t), unit="D")
            y = dd.year.values
            tmd = dd.month.values * 100 + dd.day.values
        else:
            y, mo, d = ymd(t)
            tmd = mo * 100 + d
        ya = np.where(self.md[idx] <= tmd, y, y - 1)
        return np.maximum(ya, self.sy[idx])

    def recorded_rent(self, idx, t, which=None):
        """The start rent updated by the additional bonds in force by day t (effective date where given)."""
        r = self.rent0[idx].copy()
        tp = self.tops[self.tops["when"] <= t]
        if which is not None:
            tp = tp[tp["i"].isin(which)]
        last = tp.groupby("i")["rent"].last()
        pos = pd.Series(np.arange(len(idx)), index=idx)
        hit = last.index.intersection(pos.index)
        r[pos.loc[hit].values] = last.loc[hit].values
        return r

    def recorded_with_day(self, idx, t):
        """The recorded rent on day t and the day it was recorded from (the start, or the latest additional bond)."""
        r = self.rent0[idx].copy()
        w = self.start[idx].astype(float).copy()
        tp = self.tops[self.tops["when"] <= t]
        g = tp.groupby("i")
        last = g["rent"].last()
        when = g["when"].last()
        pos = pd.Series(np.arange(len(idx)), index=idx)
        hit = last.index.intersection(pos.index)
        r[pos.loc[hit].values] = last.loc[hit].values
        w[pos.loc[hit].values] = when.loc[hit].values
        return r, w

    def rent_on(self, idx, t, CL, small_from="model", ops_from="recorded"):
        """Rent payable on day t for tenancies idx. Small landlords: the start rent carried by the panel's mean
        factor at each anniversary (model), the recorded rent (recorded), the recorded rent carried by the panel's
        factor at each anniversary after it was recorded (carry), or the recorded rent where an additional bond has
        been lodged and the model otherwise (hybrid). Operators: their recorded reviews (recorded), the panel's
        factors (model) or the carried record (carry)."""
        idx = np.asarray(idx)
        out = np.zeros(len(idx))
        ya = self.last_anniv_year(idx, t)
        ri = self.ri[idx]
        lf = CL[ri, ya - Y0 + 1] - CL[ri, self.sy[idx] - Y0 + 1]
        model = self.rent0[idx] * np.exp(lf)
        rec = self.recorded_rent(idx, t)
        want = {small_from, ops_from}
        if "carry" in want:
            rr, ww = self.recorded_with_day(idx, t)
            yr = self.last_anniv_year(idx, ww.astype(int))
            carry = rr * np.exp(CL[ri, ya - Y0 + 1] - CL[ri, yr - Y0 + 1])
        pick = {"model": model, "recorded": rec}
        if "carry" in want:
            pick["carry"] = carry
        if small_from == "hybrid":
            pick["hybrid"] = np.where(rec != self.rent0[idx], rec, model)
        op = self.op[idx]
        out[~op] = pick[small_from][~op]
        out[op] = pick[ops_from][op]
        return out

    def matched(self, t2, t1, keep=None):
        A = self.in_place(t1)
        B = self.in_place(t2)
        common = A.index.intersection(B.index)
        a = A.loc[common].values
        b = B.loc[common].values
        if keep is not None:
            k = keep(a, b)
            a, b = a[k], b[k]
        return a, b

    def measure(self, t2, t1, CL, small_from="model", ops_from="recorded", keep=None, earlier="paying", P=None):
        a, b = self.matched(t2, t1, keep)
        r1 = self.rent_on(a, t1, CL, small_from, ops_from)
        r2 = self.rent_on(b, t2, CL, small_from, ops_from)
        same = a == b
        if earlier == "start":
            r1 = np.where(same, r1, self.rent0[a])
        elif earlier == "recorded":
            r1 = np.where(same, r1, self.recorded_rent(a, t1))
        reg = self.ri[b]
        res = {}
        for gi, g in enumerate(["NAT"] + REGIONS):
            mk = np.ones(len(a), bool) if g == "NAT" else (reg == gi - 1)
            res[g] = {
                "measure": 100 * (r2[mk].sum() / r1[mk].sum() - 1),
                "same": 100 * (r2[mk & same].sum() / r1[mk & same].sum() - 1),
                "relet": 100 * (r2[mk & ~same].sum() / r1[mk & ~same].sum() - 1),
                "n": int(mk.sum()), "n_same": int((mk & same).sum()), "n_relet": int((mk & ~same).sum()),
                "nonop": 100 * (r2[mk & ~self.op[b] & ~self.op[a]].sum() / r1[mk & ~self.op[b] & ~self.op[a]].sum() - 1),
            }
            if P is not None:
                ss = np.flatnonzero(mk & same)
                ii = a[ss]
                ya = self.last_anniv_year(ii, t2)
                pr = np.array([P[(int(y), REGIONS[int(r)])] for y, r in zip(ya, self.ri[ii])])
                rose_op = r2[ss] > r1[ss] + 1e-9
                share = np.where(self.op[ii], rose_op.astype(float), pr)
                res[g]["share_rose"] = 100 * share.mean() if len(share) else float("nan")
        return res

    def held_on(self, t):
        A = self.in_place(t)
        reg = self.ri[A.values]
        out = {"NAT": int(len(A))}
        for gi, g in enumerate(REGIONS):
            out[g] = int((reg == gi).sum())
        return out
