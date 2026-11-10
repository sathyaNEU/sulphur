"""task5 architecture 4: every route to each county's December covered jobs, read from the shipped tables.

A Pack holds the extract as parsed from its files (or as cut in memory). Everything is computed as the files stood at
a stated moment: latest() gives the versions of a quarter's reports on file then (a report counts once its account is
established), liable() the accounts liable then, view() the quarter's census with each outstanding report's kind,
outcomes() what earlier outstanding employers turned out to have, unregistered() the jobs at employers liable but
with no account yet, shares() the split of an employer's jobs over its worksite counties, and certify() carries one
route's choices into county totals. The golden route, its family and every shortcut are settings of one function, so
they differ only where they say they do."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

TS = pd.Timestamp
QSTART = [TS(dt.date(2023 + q // 4, 3 * (q % 4) + 1, 1)) for q in range(W.NQ + 1)]
QEND = [TS(W.quarter_end(q)) for q in range(W.NQ)]
M3START = [TS(dt.date(2023 + q // 4, 3 * (q % 4) + 3, 1)) for q in range(W.NQ)]
CUT = [TS(W.cutoff(q)) for q in range(W.NQ)]
DUE = [TS(W.due_date(q)) for q in range(W.NQ)]
EXTRACT = TS(W.EXTRACT)
ENDS = ("INACTIVATED", "CLOSED", "TRANSFERRED")
SIZE_EDGES = (9, 49)

GOLDEN = dict(classify="mates", thr=0.5, batch_min=3, alone="mature", batch="transport", cells="chain_size",
              seasonal=True, seasonal_ratio=0.6, twoq="hist", new="hist", ibnr="develop", ibnr_pool="same_quarter",
              sites="site", version="latest", mature_tol=0.02, mature_drop=None, k_by=None)


def qindex(year, quarter):
    return (int(year) - 2023) * 4 + int(quarter) - 1


def acct_key(s):
    """the account number without its hyphen: the register writes 1234567-8, the worksite file 12345678"""
    return str(s).replace("-", "").strip()


def size_class(p):
    return np.where(p <= SIZE_EDGES[0], 0, np.where(p <= SIZE_EDGES[1], 1, 2))


class Pack:
    def __init__(self, reports, accounts, status, worksites, counties, naics):
        r = reports[["account_no", "year", "quarter", "report_type", "month1_employment", "month2_employment",
                     "month3_employment", "total_wages", "received_at"]].copy()
        r["acct"] = r["account_no"].map(acct_key)
        r["q"] = (r["year"].astype(int) - 2023) * 4 + r["quarter"].astype(int) - 1
        r["t"] = pd.to_datetime(r["received_at"])
        for c in ("month1_employment", "month2_employment", "month3_employment"):
            r[c] = r[c].astype(int)
        r["total_wages"] = r["total_wages"].astype(float)
        r = r.sort_values(["acct", "q", "t"], kind="stable")
        # a resubmission repeats a report's values within two minutes: keep the first
        key = ["acct", "q", "report_type", "month1_employment", "month2_employment", "month3_employment", "total_wages"]
        prev_t = r.groupby(key, sort=False)["t"].shift(1)
        r = r[~((prev_t.notna()) & ((r["t"] - prev_t) <= pd.Timedelta(seconds=120)))]
        a = accounts.copy()
        a["acct"] = a["account_no"].map(acct_key)
        a["liab"] = pd.to_datetime(a["liability_date"], format="%m/%d/%Y")
        a["est"] = pd.to_datetime(a["account_established"], format="%m/%d/%Y")
        nx = naics.copy()
        ss = dict(zip(nx["naics_code"].astype(str), nx["supersector_code"].astype(str)))
        a["naics_code"] = a["naics_code"].astype(str)
        a["county_code"] = a["county_code"].astype(str).str.zfill(3)
        a["ss"] = a["naics_code"].map(ss)
        a["chain"] = a["naics_code"].isin(W.HOUSING_CHAIN) & (a["ownership"].astype(str) == "5")
        a["multi"] = a["multi_worksite"] == "Y"
        self.a = a.set_index("acct")
        r["est"] = r["acct"].map(self.a["est"])
        self.r = r.reset_index(drop=True)
        self.rq = {q: g for q, g in self.r.groupby("q", sort=True)}
        s = status.copy()
        s["acct"] = s["account_no"].map(acct_key)
        s["eff"] = pd.to_datetime(s["effective_date"])
        s["proc"] = pd.to_datetime(s["processed_date"])
        self.s = s
        wk = worksites.copy()
        wk["acct"] = wk["uiacct"].map(acct_key)
        wk["q"] = (wk["year"].astype(int) - 2023) * 4 + wk["quarter"].astype(int) - 1
        cmap = {n.upper(): c for c, n in zip(counties["county_code"].astype(str).str.zfill(3), counties["county_name"])}
        wk["county"] = wk["worksite_county"].str.upper().str.strip().map(cmap)
        assert wk["county"].notna().all()
        wk["recv"] = pd.to_datetime(wk["date_received"], format="%m/%d/%Y")
        wk["unit"] = wk["reporting_unit"].astype(str)
        for c in ("m1_emp", "m2_emp", "m3_emp"):
            wk[c] = wk[c].astype(int)
        self.wk = wk[["acct", "unit", "q", "county", "m1_emp", "m2_emp", "m3_emp", "recv"]].copy()
        self.codes = list(counties["county_code"].astype(str).str.zfill(3))
        self._cache = {}

    # ------------------------------------------------------------------------------------------- conformance
    def latest(self, q, asof, version="latest"):
        """per account, the version of quarter q's report on file at asof (its account established by then), with
        the first original's receipt time"""
        k = ("latest", q, asof, version)
        if k not in self._cache:
            if q not in self.rq or q < 0:
                self._cache[k] = pd.DataFrame(columns=["m1", "m2", "m3", "orig_t"])
            else:
                x = self.rq[q]
                x = x[(x["t"] <= asof) & (x["est"] <= asof)]
                g = x.groupby("acct", sort=False)
                last = (g.tail(1) if version == "latest" else g.head(1)).set_index("acct")
                out = last[["month1_employment", "month2_employment", "month3_employment"]].copy()
                out.columns = ["m1", "m2", "m3"]
                o = x[x["report_type"] == "ORIGINAL"].groupby("acct", sort=False)["t"].first()
                out["orig_t"] = o.reindex(out.index)
                out["orig_t"] = out["orig_t"].fillna(g["t"].first().reindex(out.index))
                self._cache[k] = out
        return self._cache[k]

    def liable(self, q, asof):
        """accounts liable for quarter q as the register and its history stood at asof"""
        k = ("liable", q, asof)
        if k not in self._cache:
            a = self.a
            ok = a.index[(a["est"] <= asof) & (a["liab"] <= QEND[q])]
            e = self.s[(self.s["change_type"].isin(ENDS)) & (self.s["proc"] <= asof) & (self.s["eff"] <= QSTART[q])]
            self._cache[k] = ok.difference(pd.Index(e["acct"].unique()))
        return self._cache[k]

    def ended(self, know):
        """accounts closed, inactivated or transferred by know, with the earliest effective date"""
        k = ("ended", know)
        if k not in self._cache:
            e = self.s[(self.s["change_type"].isin(ENDS)) & (self.s["proc"] <= know)]
            self._cache[k] = e.groupby("acct")["eff"].min()
        return self._cache[k]

    def batches(self, q, asof, batch_min=3):
        """quarter q's transmissions: batch_min or more electronic originals received in the same second"""
        k = ("batches", q, asof, batch_min)
        if k not in self._cache:
            lt = self.latest(q, asof)
            t = lt["orig_t"]
            t = t[(t.dt.hour + t.dt.minute + t.dt.second) > 0]          # paper is keyed by date alone
            size = t.groupby(t).transform("size")
            self._cache[k] = t[size >= batch_min]
        return self._cache[k]

    # ------------------------------------------------------------------------------------------- the census
    def view(self, q, asof=None, thr=0.5, batch_min=3, version="latest"):
        """quarter q's census at asof: every liable account, whether its report is on file, its jobs the quarter
        before, and for an outstanding report its kind (batch, habit, alone, twoq, new)"""
        asof = TS(asof) if asof is not None else CUT[q]
        k = ("view", q, asof, thr, batch_min, version)
        if k in self._cache:
            return self._cache[k]
        L = self.liable(q, asof)
        cur = self.latest(q, asof, version)
        prev = self.latest(q - 1, asof, version)
        df = self.a.loc[L, ["county_code", "ss", "chain", "naics_code", "multi", "liab"]].copy()
        df["m3"] = cur["m3"].reindex(L)
        df["rep"] = df["m3"].notna()
        df["prior"] = prev["m3"].reindex(L)
        bk = self.batches(q - 1, asof, batch_min).reindex(L)
        df["bkey"] = bk
        mem = df[df["bkey"].notna()]
        g = mem.groupby("bkey")["rep"]
        n_mem, n_rep = g.transform("size"), g.transform("sum")
        arrived = (n_rep / (n_mem - 1).clip(lower=1)).where(n_mem > 1, 0.0)
        df["mates"] = (n_mem - 1).reindex(L)
        df["arrived"] = arrived.reindex(L)
        # habitual: every report on file for the four quarters before came after its quarter's cut-off (two at least)
        on = pd.Series(0, index=L)
        late = pd.Series(0, index=L)
        for h in range(max(0, q - 4), q):
            ot = self.latest(h, asof, version)["orig_t"].reindex(L)
            on = on + ot.notna().astype(int)
            late = late + (ot > CUT[h]).astype(int)
        df["habit"] = (on >= 2) & (late == on)
        pa = pd.Series(np.nan, index=L)
        for h in range(q - 2, -1, -1):
            v = self.latest(h, asof, version)["m3"].reindex(L)
            pa = pa.where(pa.notna(), v)
        df["prior_any"] = pa
        out = ~df["rep"]
        hp = df["prior"].notna()
        inb = df["bkey"].notna()
        kind = np.where(~out, "rep",
               np.where(hp & inb & (df["arrived"] >= thr), "alone",
               np.where(hp & inb, "batch",
               np.where(hp & df["habit"], "habit",
               np.where(hp, "alone",
               np.where(df["prior_any"].notna(), "twoq", "new"))))))
        df["kind"] = kind
        df["size"] = size_class(df["prior"].fillna(df["prior_any"]).fillna(0).values)
        df.attrs.update(q=q, asof=asof)
        self._cache[k] = df
        return df

    def eventual(self, q, know, version="latest"):
        """each account's quarter-q month-three jobs as known at know: the version on file then, nought for an account
        ended with effect by the first day of that month, NaN while unresolved"""
        k = ("eventual", q, know, version)
        if k not in self._cache:
            fin = self.latest(q, know, version)["m3"].astype(float)
            end = self.ended(know)
            gone = end[end <= M3START[q]]
            zero = pd.Series(0.0, index=gone.index.difference(fin.index))
            self._cache[k] = pd.concat([fin, zero])
        return self._cache[k]

    def mature(self, know, upto, tol=0.02, thr=0.5, batch_min=3):
        """the closed quarters whose outstanding employers have (all but tol of their jobs) resolved by know"""
        out = []
        for h in range(4, upto):
            if CUT[h] >= know:
                continue
            v = self.view(h, CUT[h], thr, batch_min)
            o = v[(v["kind"].isin(["alone", "twoq"])) & (v["prior"].fillna(v["prior_any"]) > 0)]
            ev = self.eventual(h, know).reindex(o.index)
            p = o["prior"].fillna(o["prior_any"])
            if len(o) and p[ev.isna()].sum() / p.sum() <= tol:
                out.append(h)
        return out

    def outcomes(self, quarters, know, thr=0.5, batch_min=3, drop_unresolved=True):
        """what the outstanding turned out to have, by kind, over the quarters' cut-off censuses: jobs kept and the
        jobs the quarter before, for alone also by size, chain and filing channel; for new the mean jobs"""
        acc = {}
        rows = []
        for h in quarters:
            v = self.view(h, CUT[h], thr, batch_min)
            o = v[~v["rep"]].copy()
            o["ev"] = self.eventual(h, know).reindex(o.index)
            o["p"] = o["prior"].fillna(o["prior_any"])
            o["h"] = h
            rows.append(o[["kind", "p", "ev", "size", "chain", "bkey", "h"]])
        allr = pd.concat(rows) if rows else pd.DataFrame(columns=["kind", "p", "ev", "size", "chain", "bkey", "h"])
        res = allr[allr["ev"].notna()] if drop_unresolved else allr.assign(ev=allr["ev"].fillna(allr["p"]))
        out = {}
        for kd, g in res.groupby("kind"):
            gp = g[g["p"] > 0]
            out[kd] = gp["ev"].sum() / gp["p"].sum() if gp["p"].sum() > 0 else np.nan
            if kd == "new":
                out["new_mean"] = g["ev"].mean()
        al = res[(res["kind"] == "alone") & (res["p"] > 0)]
        for s in (0, 1, 2):
            g = al[al["size"] == s]
            out[("alone", "size", s)] = g["ev"].sum() / g["p"].sum() if g["p"].sum() > 0 else np.nan
        for c in (True, False):
            g = al[al["chain"] == c]
            out[("alone", "chain", c)] = g["ev"].sum() / g["p"].sum() if g["p"].sum() > 0 else np.nan
        for nm, g in (("agent", al[al["bkey"].notna()]), ("direct", al[al["bkey"].isna()])):
            out[("alone", "channel", nm)] = g["ev"].sum() / g["p"].sum() if g["p"].sum() > 0 else np.nan
        out["_rows"] = res
        return out

    # ------------------------------------------------------------------------------------- carrying the prior
    def move(self, v, by="county_ss", leave_out=None):
        """the reporting employers' change from the quarter before, by county and supersector (the county where a
        cell has fewer than ten reporters); leave_out names reporters kept out of it (the seasonal businesses, whose
        own pattern carries them)"""
        r = v[v["rep"] & (v["prior"] > 0)]
        if leave_out is not None and len(leave_out):
            r = r[~r.index.isin(leave_out)]
        cell = r.groupby(["county_code", "ss"]).agg(now=("m3", "sum"), before=("prior", "sum"), n=("m3", "size"))
        cty = r.groupby("county_code").agg(now=("m3", "sum"), before=("prior", "sum"))
        cr = (cty["now"] / cty["before"])
        if by == "county":
            return lambda county, ss: cr.reindex(county).values
        if by == "ss":
            st = r.groupby("ss").agg(now=("m3", "sum"), before=("prior", "sum"))
            sr = st["now"] / st["before"]
            return lambda county, ss: sr.reindex(ss).values
        nmin = 20 if by == "county_ss20" else (5 if by == "county_ss5" else 10)
        ok = cell[(cell["n"] >= nmin) & (cell["before"] > 0)]
        cellr = (ok["now"] / ok["before"])

        def f(county, ss):
            idx = pd.MultiIndex.from_arrays([county, ss])
            x = cellr.reindex(idx).values
            return np.where(np.isnan(x), cr.reindex(county).values, x)
        return f

    def trouble(self, v, cells="chain_size"):
        """this quarter's share of jobs at employers whose report is missing alone, among employers whose standing
        the census shows (those that reported and those missing alone), by cell"""
        o = v[(v["prior"] > 0) & (v["kind"].isin(["rep", "alone"]))].copy()
        o["al"] = np.where(o["kind"] == "alone", o["prior"], 0.0)
        keys = {"chain_size": ["chain", "size"], "ss_size": ["ss", "size"], "ss": ["ss"], "chain": ["chain"],
                "state": None, "county_chain": ["county_code", "chain"], "naics3_size": ["n3", "size"]}[cells]
        if cells == "naics3_size":
            o["n3"] = o["naics_code"].str[:3]
        tot = o["al"].sum() / o["prior"].sum()
        if keys is None:
            return lambda d: np.full(len(d), tot)
        g = o.groupby(keys).agg(al=("al", "sum"), p=("prior", "sum"), n=("prior", "size"))
        rate = (g["al"] / g["p"]).where(g["n"] >= 30)

        def f(d):
            dd = d.copy()
            if cells == "naics3_size":
                dd["n3"] = dd["naics_code"].str[:3]
            idx = pd.MultiIndex.from_frame(dd[keys]) if len(keys) > 1 else pd.Index(dd[keys[0]])
            x = rate.reindex(idx).values.astype(float)
            return np.where(np.isnan(x), tot, x)
        return f

    def own_seasonal(self, v, ratio=0.6):
        """an employer's own month three against the quarter before, in the two years before, where both are on file
        and both run under ratio (a seasonal business)"""
        q, asof = v.attrs["q"], v.attrs["asof"]
        rs = []
        for d_, s_ in ((q - 4, q - 5), (q - 8, q - 9)):
            if s_ < 0:
                return pd.Series(dtype=float)
            a, b = self.latest(d_, asof)["m3"], self.latest(s_, asof)["m3"]
            x = (a.reindex(v.index) / b.reindex(v.index).where(b.reindex(v.index) > 0))
            rs.append(x)
        both = pd.concat(rs, axis=1).dropna()
        both = both[(both.max(axis=1) < ratio)]
        return both.mean(axis=1)

    # -------------------------------------------------------------------------- employers with no account yet
    def unregistered_history(self, q, know, pool="same_quarter"):
        """for earlier cut-offs, the accounts liable by the quarter's end and established only after the cut-off (by
        know): how many, split by whether liability began in that quarter, and their month-three jobs as now known;
        beside the accounts whose liability began in the quarter and that were established by the cut-off"""
        hs = [h for h in range(q - 1, 2, -1) if CUT[h] < know and (pool == "all" or (q - h) % 4 == 0)]
        rows = []
        a = self.a
        for h in hs:
            late = a[(a["liab"] <= QEND[h]) & (a["est"] > CUT[h]) & (a["est"] <= know)]
            ev = self.eventual(h, know).reindex(late.index).fillna(0.0)
            own = late["liab"] >= QSTART[h]
            reg_own = a[(a["liab"] >= QSTART[h]) & (a["liab"] <= QEND[h]) & (a["est"] <= CUT[h])]
            reg_prev = a[(a["liab"] >= QSTART[max(0, h - 4)]) & (a["liab"] < QSTART[h]) & (a["est"] <= CUT[h])]
            rows.append(dict(h=h, n_own=int(own.sum()), n_old=int((~own).sum()), jobs_own=float(ev[own].sum()),
                             jobs_old=float(ev[~own].sum()), reg_own=len(reg_own), reg_prev=len(reg_prev),
                             late=late.assign(ev=ev, own=own), flash_jobs=float(self.latest(h, CUT[h])["m3"].sum())))
        return rows

    def unregistered(self, q, asof, know, how="develop", pool="same_quarter", by_county=True):
        """December jobs by county at employers liable for quarter q with no account at asof"""
        zero = pd.Series(0.0, index=self.codes)
        if how == "none":
            return zero, dict(n=0.0, jobs=0.0)
        H = self.unregistered_history(q, know, pool)
        if not H:
            return zero, dict(n=0.0, jobs=0.0)
        a = self.a
        reg_own = a[(a["liab"] >= QSTART[q]) & (a["liab"] <= QEND[q]) & (a["est"] <= asof)]
        reg_prev = a[(a["liab"] >= QSTART[max(0, q - 4)]) & (a["liab"] < QSTART[q]) & (a["est"] <= asof)]
        n_own_h, reg_own_h = sum(x["n_own"] for x in H), sum(x["reg_own"] for x in H)
        n_old_h, reg_prev_h = sum(x["n_old"] for x in H), sum(x["reg_prev"] for x in H)
        j_own = sum(x["jobs_own"] for x in H) / max(1, n_own_h)
        j_old = sum(x["jobs_old"] for x in H) / max(1, n_old_h)
        if how == "develop":
            c_own = reg_own.groupby("county_code").size().reindex(self.codes).fillna(0.0)
            c_prev = reg_prev.groupby("county_code").size().reindex(self.codes).fillna(0.0)
            n = c_own * (n_own_h / reg_own_h) + c_prev * (n_old_h / reg_prev_h)
            jobs = c_own * (n_own_h / reg_own_h) * j_own + c_prev * (n_old_h / reg_prev_h) * j_old
            if not by_county:        # the state's count shared out by each county's accounts
                sh = a[a["est"] <= asof].groupby("county_code").size().reindex(self.codes)
                n, jobs = sh / sh.sum() * n.sum(), sh / sh.sum() * jobs.sum()
            return jobs, dict(n=float(n.sum()), jobs=float(jobs.sum()), j_own=j_own, j_old=j_old,
                              c_own=n_own_h / reg_own_h, c_old=n_old_h / reg_prev_h, reg_own=len(reg_own))
        if how == "regsize":         # the same count at the size of the new employers already registered
            cur = self.latest(q, asof)["m3"].reindex(reg_own.index).dropna()
            jm = float(cur.mean()) if len(cur) else j_own
            c_own = reg_own.groupby("county_code").size().reindex(self.codes).fillna(0.0)
            c_prev = reg_prev.groupby("county_code").size().reindex(self.codes).fillna(0.0)
            n = c_own * (n_own_h / reg_own_h) + c_prev * (n_old_h / reg_prev_h)
            jobs = n * jm
            return jobs, dict(n=float(n.sum()), jobs=float(jobs.sum()))
        late = pd.concat([x["late"] for x in H])
        if how == "level":           # the latest comparable cut-off's jobs carried as they were
            x = H[0]["late"]
            jobs = x.groupby("county_code")["ev"].sum().reindex(self.codes).fillna(0.0)
            return jobs, dict(n=float(len(x)), jobs=float(jobs.sum()))
        if how == "ratio":           # the same share of the jobs on file as at the earlier cut-offs
            share = sum(x["jobs_own"] + x["jobs_old"] for x in H) / sum(x["flash_jobs"] for x in H)
            cur = self.latest(q, asof)["m3"]
            cj = cur.groupby(self.a["county_code"].reindex(cur.index)).sum().reindex(self.codes).fillna(0.0)
            jobs = cj * share
            return jobs, dict(n=float("nan"), jobs=float(jobs.sum()))
        raise ValueError(how)

    # ------------------------------------------------------------------------------------- worksite counties
    def shares(self, q, asof, how="site"):
        """each multiple worksite account's split over counties for quarter q as the worksite reports stood at asof:
        the quarter's own report where it is on file; otherwise the latest report on file, each worksite carried by its
        own change over the same quarters a year earlier (site), as it stands (latest), or the report of the same
        quarter a year earlier (yearago)"""
        k = ("shares", q, asof, how)
        if k in self._cache:
            return self._cache[k]
        wk = self.wk[(self.wk["recv"] <= asof) & (self.wk["q"] <= q)]
        own = wk[wk["q"] == q]
        have = set(own["acct"])
        rest = wk[~wk["acct"].isin(have) & (wk["q"] < q)]
        parts = [own.groupby(["acct", "county"])["m3_emp"].sum().rename("w").reset_index().assign(src="own")]
        if len(rest):
            lastq = rest.groupby("acct")["q"].transform("max")
            base = rest[rest["q"] == lastq].copy()
            base["L"] = base["q"]
            if how == "latest":
                base["w"] = base["m3_emp"].astype(float)
            elif how == "yearago":
                ya = wk[(wk["q"] == q - 4) & wk["acct"].isin(set(base["acct"]))]
                got = set(ya["acct"])
                b1 = ya.assign(w=ya["m3_emp"].astype(float))
                b2 = base[~base["acct"].isin(got)].assign(w=lambda d: d["m3_emp"].astype(float))
                base = pd.concat([b1, b2])
            else:
                key = wk.set_index(["acct", "unit", "q"])["m3_emp"]
                num = key.reindex(pd.MultiIndex.from_arrays([base["acct"], base["unit"], np.full(len(base), q - 4)])).values
                den = key.reindex(pd.MultiIndex.from_arrays([base["acct"], base["unit"], base["L"] - 4])).values
                base["num"], base["den"] = num, den
                okr = base["num"].notna() & base["den"].notna() & (base["den"] > 0)
                emp = base[okr].groupby("acct").agg(n=("num", "sum"), d=("den", "sum"))
                er = (emp["n"] / emp["d"]).reindex(base["acct"]).values
                r = np.where(okr, base["num"] / base["den"].where(base["den"] > 0), np.where(np.isnan(er), 1.0, er))
                base["w"] = base["m3_emp"] * r
            parts.append(base.groupby(["acct", "county"])["w"].sum().reset_index().assign(src="carried"))
        sh = pd.concat(parts)
        tot = sh.groupby("acct")["w"].transform("sum")
        sh = sh[tot > 0].copy()
        sh["share"] = sh["w"] / tot[tot > 0]
        self._cache[k] = sh[["acct", "county", "share", "src"]]
        return self._cache[k]

    def to_counties(self, est, q, asof, how="site"):
        """account estimates (a Series) to county totals and the rows behind them"""
        sh = self.shares(q, asof, how)
        multi = self.a["multi"].reindex(est.index).fillna(False).values
        m = est[multi & est.index.isin(set(sh["acct"]))]
        s = est.drop(m.index)
        rows = [pd.DataFrame({"acct": s.index, "county": self.a["county_code"].reindex(s.index).values, "jobs": s.values})]
        if len(m):
            x = sh[sh["acct"].isin(m.index)].copy()
            x["jobs"] = x["share"].values * m.reindex(x["acct"]).values
            rows.append(x[["acct", "county", "jobs"]])
        rows = pd.concat(rows, ignore_index=True)
        return rows.groupby("county")["jobs"].sum().reindex(self.codes).fillna(0.0), rows

    # ------------------------------------------------------------------------------------------- estimation
    def certify(self, q=W.FLASH_Q, asof=None, know=None, route=None):
        """one route's estimate of quarter q's month-three jobs from the files as they stood at asof, calibrated on
        what was known at know"""
        rt = dict(GOLDEN)
        rt.update(route or {})
        asof = TS(asof) if asof is not None else CUT[q]
        know = TS(know) if know is not None else asof
        thr, bm = rt["thr"], rt["batch_min"]
        v = self.view(q, asof, thr, bm, rt["version"]).copy()
        if rt["classify"] == "none":          # every outstanding report with a report the quarter before read alike
            v.loc[v["kind"].isin(["alone", "habit"]), "kind"] = "batch"
        elif rt["classify"] == "own":         # by the employer's own record alone: late as usual, or newly late
            v.loc[v["kind"] == "batch", "kind"] = "alone"
        qs = self.mature(know, q, rt["mature_tol"], thr, bm)
        if rt["mature_drop"] == "first":
            qs = qs[1:]
        elif rt["mature_drop"] == "last":
            qs = qs[:-1]
        if rt["alone"] == "mature":
            oc = self.outcomes(qs, know, thr, bm)
        elif rt["alone"] == "allclosed":      # every earlier quarter, the unresolved left out
            oc = self.outcomes([h for h in range(4, q) if CUT[h] < know], know, thr, bm)
        elif rt["alone"] == "latest":         # the four quarters before, the unresolved left out
            oc = self.outcomes([h for h in range(max(4, q - 4), q)], know, thr, bm)
        elif rt["alone"] == "assumed_alive":  # the unresolved taken at their earlier jobs
            oc = self.outcomes([h for h in range(4, q) if CUT[h] < know], know, thr, bm, drop_unresolved=False)
        else:
            raise ValueError(rt["alone"])
        ocm = oc if rt["alone"] == "mature" else self.outcomes(qs, know, thr, bm)
        k_alone = oc.get("alone", np.nan)
        k_twoq = ocm.get("twoq", 0.0) if rt["twoq"] == "hist" else 0.0
        k_batch_hist = ocm.get("batch", np.nan)
        if not np.isfinite(k_twoq):
            k_twoq = 0.0
        seas = self.own_seasonal(v, rt["seasonal_ratio"]) if rt["seasonal"] else pd.Series(dtype=float)
        mv = self.move(v, rt.get("move_by", "county_ss"), seas.index if rt.get("move_clean", True) else None)
        out = v[~v["rep"]]
        est = pd.Series(v["m3"].astype(float), index=v.index)
        kind = v["kind"].copy()
        p = out["prior"].fillna(out["prior_any"]).fillna(0.0)
        e = pd.Series(0.0, index=out.index)
        ig = out["kind"].isin(["batch", "habit"])
        if ig.any():
            d = out[ig]
            m = pd.Series(mv(d["county_code"].values, d["ss"].values), index=d.index)
            if rt["seasonal"]:
                sr = seas.reindex(d.index)
                m = sr.where(sr.notna(), m)
            if rt["batch"] == "transport":
                a = pd.Series(self.trouble(v, rt["cells"])(d), index=d.index)
                e[ig] = p[ig] * (m * (1 - a) + k_alone * a)
            elif rt["batch"] == "reporters":
                e[ig] = p[ig] * m
            elif rt["batch"] == "hist":
                e[ig] = p[ig] * (m if rt.get("hist_plain") is False else 1.0) * k_batch_hist
            elif rt["batch"] == "state_trouble":
                a = pd.Series(self.trouble(v, "state")(d), index=d.index)
                e[ig] = p[ig] * (m * (1 - a) + k_alone * a)
            elif rt["batch"] == "locf":
                e[ig] = p[ig]
            elif rt["batch"] == "zero_all":
                e[ig] = 0.0
            else:
                raise ValueError(rt["batch"])
        al = out["kind"] == "alone"
        if rt["k_by"] in ("size", "chain"):
            col = out["size"] if rt["k_by"] == "size" else out["chain"]
            kk = col.map(lambda s: oc.get(("alone", rt["k_by"], s), np.nan)).astype(float).fillna(k_alone)
            e[al] = p[al] * kk[al]
        elif rt["k_by"] == "channel":
            kk = pd.Series(np.where(out["bkey"].notna(), oc.get(("alone", "channel", "agent")), oc.get(("alone", "channel", "direct"))), index=out.index).astype(float).fillna(k_alone)
            e[al] = p[al] * kk[al]
        else:
            e[al] = p[al] * k_alone
        tq = out["kind"] == "twoq"
        e[tq] = p[tq] * k_twoq
        if rt["batch"] == "zero_all":
            e[:] = 0.0
        elif rt["classify"] == "none" and rt["batch"] == "locf":
            e[tq] = 0.0
        nw = out["kind"] == "new"
        if nw.any() and rt["batch"] != "zero_all":
            if rt["new"] == "hist" and np.isfinite(ocm.get("new_mean", np.nan)):
                e[nw] = ocm["new_mean"]
            else:
                newrep = v[v["rep"] & v["prior"].isna() & v["prior_any"].isna()]
                e[nw] = float(newrep["m3"].mean()) if len(newrep) else 0.0
        est[out.index] = e
        tot_rep, rows_rep = self.to_counties(est[v["rep"]], q, asof, rt["sites"])
        tot_out, rows_out = self.to_counties(est[~v["rep"]], q, asof, rt["sites"])
        un, uinfo = self.unregistered(q, asof, know, rt["ibnr"], rt["ibnr_pool"], rt.get("ibnr_by_county", True))
        total = tot_rep + tot_out + un
        return dict(q=q, asof=asof, know=know, route=rt, view=v, est=est, kind=kind, reported=tot_rep, outstanding=tot_out,
                    unregistered=un, total=total, uinfo=uinfo, k_alone=k_alone, k_twoq=k_twoq, k_batch_hist=k_batch_hist,
                    mature=qs, outcomes=ocm, rows_rep=rows_rep, rows_out=rows_out, new_mean=ocm.get("new_mean", np.nan))

    def base(self, q, asof, sites="site"):
        """quarter q's month-three jobs by county as the files stood at asof: every report on file, split by worksite"""
        lt = self.latest(q, asof)["m3"].astype(float)
        tot, rows = self.to_counties(lt, q, asof, sites)
        return tot

    def published_rows(self, q=W.BASE_Q, cut=None):
        """the Section's published county table for quarter q: reports posted through the cut, split by the worksite
        reports on file then (the latest on file where the quarter's had not come)"""
        cut = TS(cut or W.PUBLISHED_CUT)
        lt = self.latest(q, cut)
        x = self.rq[q]
        x = x[(x["t"] <= cut) & (x["est"] <= cut)].groupby("acct", sort=False).tail(1).set_index("acct")
        wages = x["total_wages"].reindex(lt.index)
        out = {}
        for col in ("m1", "m2", "m3"):
            out[col], rows = self.to_counties(lt[col].astype(float), q, cut, "latest")
        wg, _ = self.to_counties(wages, q, cut, "latest")
        units = rows.groupby("county").size().reindex(self.codes).fillna(0).astype(int)
        return out, wg, units


def changes(total, base):
    return (total / base - 1) * 100


def designated(ch):
    return [c for c in ch.index if round(float(ch[c]) + 1e-9, 1) <= W.THRESHOLD]


# ---------------------------------------------------------------------------------------- the routes, by name
# the standing family: every choice a careful analyst could defend inside the golden's method
FAMILY = [
    ("the golden", {}),
    ("a transmission arrived when a third of its other reports are in", dict(thr=0.34)),
    ("a transmission arrived when two thirds of its other reports are in", dict(thr=0.67)),
    ("a transmission as two or more reports in one second", dict(batch_min=2)),
    ("a transmission as four or more reports in one second", dict(batch_min=4)),
    ("this quarter's trouble by supersector and size", dict(cells="ss_size")),
    ("this quarter's trouble by supersector", dict(cells="ss")),
    ("this quarter's trouble by three-digit industry and size", dict(cells="naics3_size")),
    ("this quarter's trouble by housing chain alone", dict(cells="chain")),
    ("this quarter's trouble by county and housing chain", dict(cells="county_chain")),
    ("the resolved quarters without the earliest", dict(mature_drop="first")),
    ("the resolved quarters without the latest", dict(mature_drop="last")),
    ("resolved at 5 per cent of jobs outstanding", dict(mature_tol=0.05)),
    ("the missing-alone share by size", dict(k_by="size")),
    ("the missing-alone share by filing channel", dict(k_by="channel")),
    ("the missing-alone share by housing chain", dict(k_by="chain")),
    ("a seasonal business under half its September", dict(seasonal_ratio=0.5)),
    ("a seasonal business under 0.7 of its September", dict(seasonal_ratio=0.7)),
    ("a new account at this quarter's reporting new employers", dict(new="reporters")),
    ("two quarters out at nought", dict(twoq="zero")),
    ("the reporters' change in cells of five or more", dict(move_by="county_ss5")),
    ("the reporters' change in cells of twenty or more", dict(move_by="county_ss20")),
]
# variants a named fact in the files rules out (checks.py asserts each fact); they sit outside the family
RULED_OUT = [
    ("unregistered employers from every earlier cut-off", dict(ibnr_pool="all")),
    ("unregistered employers shared out by each county's accounts", dict(ibnr_by_county=False)),
    ("the reporters' change by supersector statewide", dict(move_by="ss")),
    ("the reporters' change by county alone", dict(move_by="county")),
]
# the shortcuts, each a complete estimate that stops short somewhere
SHORTCUTS = [
    ("the reports received alone", dict(classify="none", batch="zero_all", ibnr="none", sites="latest")),
    ("September carried for every report outstanding, accounts on the register, the latest worksite reports",
     dict(classify="none", batch="locf", ibnr="none", sites="latest")),
    ("the reporting employers' change for every report outstanding, accounts on the register, the latest worksite reports",
     dict(classify="none", batch="reporters", ibnr="none", sites="latest")),
    ("outstanding reports read by cause; late transmissions at the reporters' change; accounts on the register; the latest worksite reports",
     dict(batch="reporters", ibnr="none", sites="latest")),
    ("the same with last year's unregistered jobs carried as they were",
     dict(batch="reporters", ibnr="level", sites="latest")),
    ("the full estimate without the employers that have no account yet", dict(ibnr="none")),
    ("the full estimate with the latest worksite reports' split", dict(sites="latest")),
    ("the full estimate with last December's worksite split", dict(sites="yearago")),
    ("the full estimate with late transmissions at the reporters' change", dict(batch="reporters")),
    ("the full estimate with the missing-alone share from every earlier quarter", dict(alone="allclosed")),
    ("the reporting employers' change for every report outstanding, the rest as in the estimate",
     dict(classify="none", batch="reporters")),
    ("unregistered employers at the same share of jobs as at earlier cut-offs", dict(ibnr="ratio")),
    ("unregistered employers at the size of the new employers already registered", dict(ibnr="regsize")),
]
QUICK = dict(classify="none", batch="locf", ibnr="none", sites="latest")
CAREFUL = dict(batch="reporters", ibnr="level", sites="latest")
