"""task14: every graded result computed from the shipped files alone (the golden), the rivals that set each band, and
the projection's back-test. Reads target/ only."""
import numpy as np
import openpyxl
import pandas as pd

import conform as CF
import measure as MS
import project as PJ

SEP26, SEP25 = MS.quarter_end(2026, 3), MS.quarter_end(2025, 3)
DEC26, DEC25 = MS.day(2026, 12, 31), MS.day(2025, 12, 31)
CUT = MS.day(2026, 11, 27)
B_BOOT = 400
SEED = 7713


def published_sep26(files):
    path = [v for k, v in files.items() if "private_rents_index_survey" in k][0]
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Annual change"]
    head = [c.value for c in ws[3]]
    out = {}
    for row in ws.iter_rows(min_row=4, values_only=True):
        if row[0] == "2026Q3":
            for h, v in zip(head[1:], row[1:]):
                out[h] = v
    return out


def cut_engine(E_full, T_full, tops_full, cut):
    """The register as it stood at the close of a cut day (Engine.as_of)."""
    return E_full.as_of(cut)


class Golden:
    def __init__(self, target, strict="golden"):
        self.D = CF.load(target)
        self.T, self.tops, self.ops = CF.conform(self.D, strict)
        self.E = MS.Engine(self.T, self.tops)
        self.pairs = MS.panel_pairs(self.D["PN"])
        self.m, self.p = MS.review_model(self.pairs)
        self.CL = MS.cumlog(self.m)
        self.ix = PJ.letting_index(self.E)
        self.cpi = self.D["CPI"]

    def series(self, CL=None, **kw):
        CL = self.CL if CL is None else CL
        out = {}
        for (y, q) in MS.quarters():
            r = self.E.measure(MS.quarter_end(y, q), MS.quarter_end(y - 1, q), CL, **kw)
            out["%dQ%d" % (y, q)] = {g: r[g]["measure"] for g in r}
        return out

    def sep26(self, CL=None, P=None, **kw):
        return self.E.measure(SEP26, SEP25, self.CL if CL is None else CL, P=self.p if P is None else P, **kw)

    def dec26(self, CL=None, **kw):
        kw.setdefault("cpi", self.cpi)
        return PJ.project(self.E, self.CL if CL is None else CL, ix=self.ix, **kw)

    def boot(self, B=B_BOOT, seed=SEED):
        """The panel's dwellings resampled within their strata; the review rates re-estimated; the national September
        2026 figure and the December projection recomputed."""
        rng = np.random.default_rng(seed)
        PN = self.D["PN"]
        dw = PN[["dwelling_ref", "stratum"]].drop_duplicates("dwelling_ref")
        by = {s: g["dwelling_ref"].values for s, g in dw.groupby("stratum")}
        pr = self.pairs_by_dwelling()
        sep, dec, decr = [], [], []
        self.boot_CL = []
        for b in range(B):
            pick = []
            for s, refs in by.items():
                pick.append(rng.choice(refs, size=len(refs), replace=True))
            pick = np.concatenate(pick)
            cnt = pd.Series(pick).value_counts()
            sub = pr[pr["dwelling_ref"].isin(cnt.index)].copy()
            sub["w"] = sub["w"] * sub["dwelling_ref"].map(cnt)
            m, p = MS.review_model(sub)
            CL = MS.cumlog(m)
            self.boot_CL.append(CL)
            r = self.E.measure(SEP26, SEP25, CL)
            sep.append(r["NAT"]["measure"])
            d = PJ.project(self.E, CL, ix=self.ix, cpi=self.cpi)
            dec.append(d["NAT"])
            decr.append([d[g] for g in MS.REGIONS])
        return np.array(sep), np.array(dec), np.array(decr)

    def pairs_by_dwelling(self):
        """The panel's anniversary pairs with the dwelling they came from (for the bootstrap)."""
        return self.pairs

    def backtest(self, years=(2023, 2024, 2025)):
        """The projection run at 27 November of earlier years on the register as it stood then, against the measure
        the full register gives for that December."""
        out = []
        for y in years:
            cut = MS.day(y, 11, 27)
            Ec = cut_engine(self.E, self.T, self.tops, cut)
            ixc = PJ.letting_index(Ec)
            ixc = {r: s.loc[:pd.Period("%d-11" % y, "M")] for r, s in ixc.items()}
            pj = PJ.project(Ec, self.CL, t1=MS.day(y - 1, 12, 31), t2=MS.day(y, 12, 31), cut=cut, ix=ixc,
                            rate_years=tuple(range(y - 3, y)), sched=PJ.review_schedule(self.E, cpi=self.cpi),
                            cpi=self.cpi)
            act = self.E.measure(MS.day(y, 12, 31), MS.day(y - 1, 12, 31), self.CL)
            out.append({"year": y, "projected": pj["NAT"], "actual": act["NAT"]["measure"],
                        "regions": {g: (pj[g], act[g]["measure"]) for g in MS.REGIONS}})
        return out
