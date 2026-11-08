"""task5 architecture 3: every route to each county's December 2026 covered jobs, read from the shipped tables.

A Pack holds the extract as parsed from its files (or as cut in memory). conform() gives, for any quarter and any
as-at moment, the latest version of each report received by then, the accounts liable then, and the worksite split;
classify() reads each missing report as late with its transmission, late as usual, missing alone, missing a second
quarter, or a new employer's first; outcomes() measures what earlier missing employers turned out to have; and
estimate() carries a route's choices into county totals. The golden route and every rung are settings of one
function, so they differ only where they say they do."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

SIZE_EDGES = (9, 49)          # the outcome strata: 1-9, 10-49, 50 and more September jobs
TRANSMISSION_MIN = 3          # a transmission is three or more electronic reports received in the same second
SEASONAL_RATIO = 0.6          # an employer whose own December runs under 0.6 of its September in both earlier years
GOLDEN = dict(missing="impute", classify="golden", two_q="hist", alone="closed_pooled", seasonal=True, new="mean")
CLOSED_QUARTERS = list(range(4, 11))      # 2024Q1 .. 2025Q3: four quarters of history before, every missing employer resolved by the extract
LATEST_QUARTERS = [13, 14]                # 2026Q2, 2026Q3: the six months before the flash


def qindex(year, quarter):
    return (int(year) - 2023) * 4 + int(quarter) - 1


def acct_key(s):
    """the account number without its hyphen: the register writes 1234567-8, the worksite file 12345678"""
    return str(s).replace("-", "").strip()


class Pack:
    def __init__(self, reports, accounts, status, worksites, counties, naics):
        r = reports.copy()
        r["acct"] = r["account_no"].map(acct_key)
        r["q"] = [qindex(y, k) for y, k in zip(r["year"], r["quarter"])]
        r["t"] = pd.to_datetime(r["received_at"])
        for c in ("month1_employment", "month2_employment", "month3_employment"):
            r[c] = r[c].astype(int)
        # a resubmission repeats an original's values within two minutes: keep the first
        r = r.sort_values(["acct", "q", "t"], kind="stable")
        key = ["acct", "q", "report_type", "month1_employment", "month2_employment", "month3_employment", "total_wages"]
        prev_t = r.groupby(key, sort=False)["t"].shift(1)
        r = r[~((prev_t.notna()) & ((r["t"] - prev_t) <= pd.Timedelta(seconds=120)))]
        self.r = r.reset_index(drop=True)
        a = accounts.copy()
        a["acct"] = a["account_no"].map(acct_key)
        a["liab"] = pd.to_datetime(a["liability_date"], format="%m/%d/%Y")
        nx = naics.copy()
        ss = dict(zip(nx["naics_code"].astype(str), nx["supersector_code"].astype(str)))
        a["ss"] = a["naics_code"].astype(str).map(ss)
        ss22 = dict(zip(nx.loc[nx["naics_vintage"].astype(str) == "2022", "naics_code"].astype(str),
                        nx.loc[nx["naics_vintage"].astype(str) == "2022", "supersector_code"].astype(str)))
        a["ss22"] = a["naics_code"].astype(str).map(ss22)
        self.a = a.set_index("acct")
        s = status.copy()
        s["acct"] = s["account_no"].map(acct_key)
        s["eff"] = pd.to_datetime(s["effective_date"])
        s["proc"] = pd.to_datetime(s["processed_date"])
        self.s = s
        wk = worksites.copy()
        wk["acct"] = wk["uiacct"].map(acct_key)
        wk["q"] = [qindex(y, k) for y, k in zip(wk["year"], wk["quarter"])]
        cmap = {n.upper(): c for c, n in zip(counties["county_code"], counties["county_name"])}
        wk["county"] = wk["worksite_county"].str.upper().str.strip().map(cmap)
        assert wk["county"].notna().all()
        self.wk = wk
        self.codes = list(counties["county_code"])
        self._cache = {}
        # the golden's conventions; the rival families vary them (checks.py, SF12)
        self.trans_window = 0          # seconds: a transmission's reports share a receipt second
        self.mates_quarters = 1        # the transmission an employer came in last quarter
        self.mates_threshold = 0.5     # at least half its transmission-mates have reported
        self.cell = "county_ss"        # the field's cell: county by supersector
        self.seasonal_ratio = SEASONAL_RATIO
        self.closed = list(CLOSED_QUARTERS)
        self.version = "latest"        # mess knobs (checks.py R2): which version of a report counts
        self.use_worksites = True      # split multiple worksite employers by their worksite reports
        self.paper_transmissions = False
        self.trans_min = TRANSMISSION_MIN
        self.transfers_end = True      # a transfer ends the predecessor's liability
        self.naics_2017 = True         # map NAICS 2017 codes through the concordance

    def variant(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
        self._cache = {k: v for k, v in self._cache.items() if k[0] == "latest" or k[0] == "liable"}
        return self

    # ------------------------------------------------------------------------------------------- conformance
    def latest(self, q, asof):
        """per account, the latest version of quarter q's report received by asof, with the original's receipt time"""
        k = ("latest", q, asof)
        if k not in self._cache:
            x = self.r[(self.r["q"] == q) & (self.r["t"] <= asof)]
            srt = x.sort_values("t", kind="stable").groupby("acct")
            last = (srt.tail(1) if self.version == "latest" else srt.head(1)).set_index("acct")
            orig = x[x["report_type"] == "ORIGINAL"].sort_values("t", kind="stable").groupby("acct").head(1).set_index("acct")
            last = last[["month1_employment", "month2_employment", "month3_employment"]].copy()
            last["orig_t"] = orig["t"]
            self._cache[k] = last
        return self._cache[k]

    def liable(self, q, asof):
        """accounts liable for quarter q as the register and its history stood at asof"""
        k = ("liable", q, asof)
        if k not in self._cache:
            qstart = pd.Timestamp(dt.date(2023 + q // 4, 3 * (q % 4) + 1, 1))
            qend = pd.Timestamp(W.quarter_end(q))
            ok = set(self.a.index[self.a["liab"] <= qend])
            kinds = ["INACTIVATED", "CLOSED", "TRANSFERRED"] if self.transfers_end else ["INACTIVATED", "CLOSED"]
            ends = self.s[(self.s["change_type"].isin(kinds)) & (self.s["proc"] <= asof)]
            gone = set(ends.loc[ends["eff"] <= qstart, "acct"])
            self._cache[k] = ok - gone
        return self._cache[k]

    def ended(self, asof):
        """accounts the Division has closed or inactivated by asof, with the effective date"""
        e = self.s[(self.s["change_type"].isin(["INACTIVATED", "CLOSED"])) & (self.s["proc"] <= asof)]
        return e.groupby("acct")["eff"].min()

    def transmissions(self, q, asof):
        """quarter q's transmissions: three or more electronic originals received in the same second"""
        x = self.r[(self.r["q"] == q) & (self.r["t"] <= asof) & (self.r["report_type"] == "ORIGINAL")]
        x = x.sort_values("t", kind="stable").groupby("acct").head(1)
        if not self.paper_transmissions:
            x = x[(x["t"].dt.hour + x["t"].dt.minute + x["t"].dt.second) > 0]      # paper is keyed by date alone
        if self.trans_window == "minute":
            key = x["t"].dt.floor("min")
            size = x.groupby(key)["acct"].transform("count")
            keep = size >= self.trans_min
            return dict(zip(x.loc[keep, "acct"], key[keep]))
        if self.trans_window:
            x = x.sort_values("t", kind="stable")
            gap = x["t"].diff().dt.total_seconds().fillna(1e9)
            key = (gap > self.trans_window).cumsum()
        else:
            key = x["t"]
        size = x.groupby(key)["acct"].transform("count")
        keep = size >= self.trans_min
        return dict(zip(x.loc[keep, "acct"], (key[keep] if self.trans_window else x.loc[keep, "t"])))

    # ---------------------------------------------------------------------------------------- the missing
    def view(self, q, asof=None):
        """the flash view of quarter q: what was received by its cut-off, who was liable, who had not reported"""
        asof = pd.Timestamp(asof or W.cutoff(q))
        k = ("view", q, asof)
        if k in self._cache:
            return self._cache[k]
        liab = self.liable(q, asof)
        rec = self.latest(q, asof)
        rec = rec[rec.index.isin(liab)]          # a final report from an account closed before the quarter is no reporter
        missing = sorted(liab - set(rec.index))
        prev = self.latest(q - 1, asof)
        info = []
        trans_prev = self.transmissions(q - 1, asof)
        members = {}
        for a_, t_ in trans_prev.items():
            members.setdefault(t_, []).append(a_)
        mates_of = {}
        for h in range(max(0, q - self.mates_quarters), q):
            th = self.transmissions(h, asof)
            grp = {}
            for a_, t_ in th.items():
                grp.setdefault(t_, []).append(a_)
            for t_, ms in grp.items():
                for a_ in ms:
                    mates_of.setdefault(a_, set()).update(ms)
        # habitual: every report on file for the four quarters before came after its quarter's cut-off (two at least)
        late4, on4 = {}, {}
        for h in range(max(0, q - 4), q):
            lt = self.latest(h, asof)
            for a_, t_ in lt["orig_t"].items():
                late4[a_] = late4.get(a_, 0) + int(t_ > pd.Timestamp(W.cutoff(h)))
                on4[a_] = on4.get(a_, 0) + 1
        habit = {a_ for a_ in on4 if on4[a_] >= 2 and late4[a_] == on4[a_]}
        agent_hist = set()
        for h in range(max(0, q - 4), q):
            agent_hist |= set(self.transmissions(h, asof))
        prior_any = {}
        for h in range(q - 1, -1, -1):
            lt = self.latest(h, asof)
            for a_, v in lt["month3_employment"].items():
                if a_ not in prior_any:
                    prior_any[a_] = (h, int(v))
        for a_ in missing:
            row = {"acct": a_}
            if a_ in prev.index:
                row["prior"] = int(prev.loc[a_, "month3_employment"])
                row["prior_q"] = q - 1
                tp = trans_prev.get(a_)
                if tp is not None or (self.mates_quarters > 1 and a_ in mates_of):
                    pool = mates_of.get(a_, set()) if self.mates_quarters > 1 else set(members[tp])
                    mates = [m for m in pool if m != a_ and m in liab]
                    arrived = np.mean([m in rec.index for m in mates]) if mates else 0.0
                    row["mates"] = len(mates)
                    row["arrived"] = float(arrived)
                    if self.mates_threshold == 0:
                        row["golden"] = "alone" if arrived > 0 else "batch"
                    else:
                        row["golden"] = "alone" if arrived >= self.mates_threshold else "batch"
                else:
                    row["golden"] = "habitual" if a_ in habit else "alone"
                row["agent_client"] = a_ in agent_hist
                row["habitual"] = a_ in habit
            elif a_ in prior_any:
                row["prior_q"], row["prior"] = prior_any[a_]
                row["golden"] = "two_q"
                row["agent_client"] = a_ in agent_hist
                row["habitual"] = False
            else:
                row["prior"], row["prior_q"] = np.nan, -1
                row["golden"] = "new"
                row["agent_client"] = False
                row["habitual"] = False
            info.append(row)
        mi = pd.DataFrame(info).set_index("acct") if info else pd.DataFrame(columns=["prior", "golden"])
        out = dict(q=q, asof=asof, rec=rec, liable=liab, missing=mi, prev=prev)
        self._cache[k] = out
        return out

    def classes(self, v, how):
        mi = v["missing"]
        if how == "golden":
            return mi["golden"].copy()
        if how == "none":
            return mi["golden"].where(mi["golden"].isin(["two_q", "new"]), "batch")
        if how == "filer":      # every agent client's lateness taken as its agent's
            g = mi["golden"].copy()
            g[(g == "alone") & mi["agent_client"]] = "batch"
            return g
        if how == "newly":      # every employer late without the habit taken as in trouble
            g = mi["golden"].copy()
            g[(g == "batch")] = "alone"
            return g
        raise ValueError(how)

    # --------------------------------------------------------------------------------------------- outcomes
    def eventual(self, q):
        """what each quarter-q report turned out to be by the extract: its latest version, or nought for an account
        the Division has closed or inactivated with effect by the quarter's third month; NaN while unresolved"""
        fin = self.latest(q, pd.Timestamp(W.EXTRACT))["month3_employment"]
        end = self.ended(pd.Timestamp(W.EXTRACT))
        m3 = pd.Timestamp(dt.date(2023 + q // 4, 3 * (q % 4) + 3, 1))
        def get(a_):
            if a_ in fin.index:
                return float(fin[a_])
            if a_ in end.index and end[a_] <= m3:
                return 0.0
            return np.nan
        return get

    def outcomes(self, quarters, how="golden", drop_never_filed=False):
        """kept share of prior jobs by class (and, for missing alone, by size), over the quarters' flash views"""
        acc = {}
        for h in quarters:
            v = self.view(h)
            cls = self.classes(v, how)
            ev = self.eventual(h)
            mi = v["missing"]
            for a_, c in cls.items():
                p = mi.loc[a_, "prior"]
                if not np.isfinite(p) or p <= 0:
                    continue
                e = ev(a_)
                if not np.isfinite(e):
                    continue
                if drop_never_filed and a_ not in self.latest(h, pd.Timestamp(W.EXTRACT)).index:
                    continue
                s = 0 if p <= SIZE_EDGES[0] else (1 if p <= SIZE_EDGES[1] else 2)
                ch = "agent" if mi.loc[a_, "agent_client"] else "direct"
                for key in ((c, "all"), (c, s), (c, ch)):
                    n_, d_ = acc.get(key, (0.0, 0.0))
                    acc[key] = (n_ + e, d_ + p)
        return {k: (n_ / d_ if d_ else np.nan) for k, (n_, d_) in acc.items()}, acc

    def cell_ratio(self, v):
        """the reporting employers' change from the quarter before, by county and supersector (county alone where
        a cell has fewer than ten)"""
        rec, prev = v["rec"], v["prev"]
        both = rec.index.intersection(prev.index)
        df = pd.DataFrame({"now": rec.loc[both, "month3_employment"], "before": prev.loc[both, "month3_employment"]})
        df["county"] = self.a.loc[both, "county_code"].values
        df["ss"] = self.a.loc[both, "ss"].values if self.naics_2017 else self.a.loc[both, "ss22"].values
        cell = df.groupby(["county", "ss"]).agg(now=("now", "sum"), before=("before", "sum"), n=("now", "size"))
        cty = df.groupby("county").agg(now=("now", "sum"), before=("before", "sum"))
        def ratio(county, ss):
            if self.cell == "county":
                c = cty.loc[county]
                return c["now"] / c["before"]
            if (county, ss) in cell.index and cell.loc[(county, ss), "n"] >= 10 and cell.loc[(county, ss), "before"] > 0:
                c = cell.loc[(county, ss)]
                return c["now"] / c["before"]
            c = cty.loc[county]
            return c["now"] / c["before"]
        return ratio

    def own_seasonal(self, v, accts):
        """an employer's own December against its September in the two years before, where both are on file"""
        q = v["q"]
        out = {}
        pairs = [(q - 4, q - 5), (q - 8, q - 9)]
        tabs = {h: self.latest(h, v["asof"])["month3_employment"] for p in pairs for h in p if h >= 0}
        for a_ in accts:
            rs = []
            for d_, s_ in pairs:
                if d_ in tabs and s_ in tabs and a_ in tabs[d_].index and a_ in tabs[s_].index and tabs[s_][a_] > 0:
                    rs.append(tabs[d_][a_] / tabs[s_][a_])
            if len(rs) == 2 and max(rs) < self.seasonal_ratio:
                out[a_] = float(np.mean(rs))
        return out

    # ------------------------------------------------------------------------------------------- estimation
    def estimate(self, q=W.FLASH_Q, route=None, ratios=None):
        """each account's estimated month-three jobs for quarter q under a route, and the county totals"""
        rt = dict(GOLDEN)
        rt.update(route or {})
        v = self.view(q)
        rec, mi = v["rec"], v["missing"]
        cls = self.classes(v, rt["classify"]) if len(mi) else pd.Series(dtype=str)
        cr = self.cell_ratio(v)
        if ratios is None:
            ratios = self.route_ratios(rt)
        seas = self.own_seasonal(v, mi.index) if rt["seasonal"] else {}
        new_mean = self.new_mean(v)
        est = {}
        kind = {}
        for a_ in rec.index:
            est[a_] = float(rec.loc[a_, "month3_employment"])
            kind[a_] = "reported"
        for a_, c in cls.items():
            p = mi.loc[a_, "prior"]
            county, ss = self.a.loc[a_, "county_code"], (self.a.loc[a_, "ss"] if self.naics_2017 else self.a.loc[a_, "ss22"])
            if rt["missing"] == "zero":
                e = 0.0
            elif c in ("batch", "habitual"):
                e = p * seas[a_] if a_ in seas else p * cr(county, ss)
            elif c == "alone":
                s = 0 if p <= SIZE_EDGES[0] else (1 if p <= SIZE_EDGES[1] else 2)
                rr = ratios.get(("alone", s)) if rt["alone"].endswith("strat") else ratios.get(("alone", "all"))
                if rt["alone"] == "closed_channel":
                    rr = ratios.get(("alone", "agent" if mi.loc[a_, "agent_client"] else "direct"))
                if rr is None or not np.isfinite(rr):
                    rr = ratios.get(("alone", "all"))
                e = p * rr
            elif c == "two_q":
                e = {"hist": p * ratios.get(("two_q", "all"), 0.0), "zero": 0.0, "alive": p * cr(county, ss)}[rt["two_q"]]
            else:
                e = new_mean if rt.get("new", "mean") == "mean" else 0.0
            est[a_] = float(e)
            kind[a_] = c
        return est, kind, v

    def route_ratios(self, rt):
        if rt["alone"] in ("closed_strat", "closed_pooled", "closed_channel"):
            r, _ = self.outcomes(self.closed)
        elif rt["alone"] == "latest":
            r, _ = self.outcomes(LATEST_QUARTERS)
        elif rt["alone"] == "closed_dropped":
            r, _ = self.outcomes(self.closed, drop_never_filed=True)
        else:
            raise ValueError(rt["alone"])
        if rt["alone"] != "closed_strat":
            r = {k: v for k, v in r.items()}
            for s in (0, 1, 2):
                r[("alone", s)] = r.get(("alone", "all"))
        two, _ = self.outcomes(self.closed)
        r[("two_q", "all")] = two.get(("two_q", "all"), 0.0)
        return r

    def new_mean(self, v):
        """a new employer whose first report has not arrived: the quarter's new employers who did report, on average"""
        q = v["q"]
        qstart = pd.Timestamp(dt.date(2023 + q // 4, 3 * (q % 4) + 1, 1))
        new = self.a.index[(self.a["liab"] >= qstart) & (self.a["liab"] <= pd.Timestamp(W.quarter_end(q)))]
        got = v["rec"].index.intersection(new)
        return float(v["rec"].loc[got, "month3_employment"].mean()) if len(got) else 0.0

    # ---------------------------------------------------------------------------------------------- counties
    def split(self, q, est, asof):
        """account estimates to counties: a multiple worksite employer by its worksite report for the quarter, or its
        latest one on file; everyone else by the register's county"""
        wk = self.wk[self.wk["t"] <= asof] if "t" in self.wk else self.wk
        tot = {c: 0.0 for c in self.codes}
        rows = []
        mw = self.a["multi_worksite"] == "Y"
        for a_, e in est.items():
            if self.use_worksites and mw.get(a_, False):
                sh = self.worksite_shares(a_, q)
                if sh:
                    for c, s in sh.items():
                        tot[c] += e * s
                        rows.append((a_, c, e * s))
                    continue
            c = self.a.loc[a_, "county_code"]
            tot[c] += e
            rows.append((a_, c, e))
        return tot, rows

    def worksite_shares(self, a_, q):
        x = self.wk[(self.wk["acct"] == a_) & (self.wk["q"] <= q)]
        if not len(x):
            return None
        last = x[x["q"] == x["q"].max()]
        s = last.groupby("county")["m3_emp"].sum()
        if s.sum() <= 0:
            s = last.groupby("county")["m1_emp"].sum()
        if s.sum() <= 0:
            return None
        return (s / s.sum()).to_dict()

    def base(self, q=W.BASE_Q):
        """December 2025 by county from the closed fourth-quarter reports"""
        lt = self.latest(q, pd.Timestamp(W.EXTRACT))
        est = {a_: float(v) for a_, v in lt["month3_employment"].items()}
        tot, _ = self.split(q, est, pd.Timestamp(W.EXTRACT))
        return tot


def county_change(pack, route=None, ratios=None):
    est, kind, v = pack.estimate(W.FLASH_Q, route, ratios)
    tot, rows = pack.split(W.FLASH_Q, est, v["asof"])
    base = pack.base()
    imp = {c: 0.0 for c in pack.codes}
    for a_, c, e in rows:
        if kind[a_] != "reported":
            imp[c] += e
    ch = {c: 100.0 * (tot[c] / base[c] - 1) for c in pack.codes}
    return dict(total=tot, imputed=imp, base=base, change=ch, kind=kind, est=est, rows=rows)


def designated(ch):
    return sorted(c for c, x in ch.items() if round(x + 1e-9, 1) <= W.THRESHOLD)
