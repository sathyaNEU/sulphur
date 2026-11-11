"""task9: the record as the golden reads it, rebuilt from the cut pack alone.

The two generations of the risk system's daily export are put on one footing (USD P&L and USD capital, the
2022 book-code map applied so each pod keeps one code, the re-sent day taken once); a day the legacy feed missed is
a day with no rows, and the next day's row carries both days, so the market's returns are summed over the same span.
The register gives each pod's strategy group and first trading day; the draft gives each pod's 2026 and 2027 capital.
"""
import os

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import market as MK
import pack as PK
import params as P

GROUP_KEY = {v["name"]: k for k, v in P.GROUPS.items()}


def nyse_days(a, b):
    """US exchange trading days from a to b inclusive (the late-2026 and 2027 closures listed)."""
    hol = {"2026-11-26", "2026-12-25", "2027-01-01", "2027-01-18", "2027-02-15", "2027-03-26", "2027-05-31", "2027-06-18",
           "2027-07-05", "2027-09-06", "2027-11-25", "2027-12-24"}
    return pd.DatetimeIndex([t for t in pd.bdate_range(a, b) if t.strftime("%Y-%m-%d") not in hol])


class Record:
    def __init__(self, tgt):
        old = pd.read_csv(os.path.join(tgt, PK.F["legacy"]), dtype={"pod_code": str})
        new = pd.read_csv(os.path.join(tgt, PK.F["current"]), dtype={"book_id": str})
        cmap = pd.read_csv(os.path.join(tgt, PK.F["codes"]), dtype=str)
        reg = pd.read_csv(os.path.join(tgt, PK.F["register"]), dtype=str)
        self.n_dupes = int(old.duplicated().sum())
        old = old.drop_duplicates()
        to_new = dict(zip(cmap.old_pod_code, cmap.new_book_id))
        a = pd.DataFrame(dict(date=pd.to_datetime(old.cob_date), code=old.pod_code.map(lambda c: to_new.get(c, c)),
                              pnl=old.gross_pnl_usd.astype(float), capital=old.capital_usd.astype(float)))
        b = pd.DataFrame(dict(date=pd.to_datetime(new.trade_date, format="%m/%d/%Y"), code=new.book_id,
                              pnl=new.pnl_usd_000.astype(float) * 1e3, capital=new.alloc_capital_usd_mm.astype(float) * 1e6))
        rec = pd.concat([a, b], ignore_index=True)
        reg["g"] = reg.strategy_group.map(GROUP_KEY)
        reg["first"] = pd.to_datetime(reg.first_trading_day)
        reg = reg.sort_values(["first", "pod"]).reset_index(drop=True)
        self.code = dict(enumerate(reg.pod))
        ids = {c: i for i, c in self.code.items()}
        rec["n"] = rec.code.map(ids)
        assert rec.n.notna().all(), "a code the register does not hold"
        rec["n"] = rec.n.astype(int)
        self.days = pd.DatetimeIndex(sorted(rec.date.unique()))
        self.panel = rec[["date", "n", "capital", "pnl"]].sort_values(["n", "date"]).reset_index(drop=True)
        self.groups = dict(zip(range(len(reg)), reg.g))
        self.status = dict(zip(range(len(reg)), reg.status))
        mk = MK.Market(src=tgt)
        self.mk = mk
        # each record day's market return is the sum of the trading days since the record's previous day
        allday = mk.hold.index[(mk.hold.index >= self.days[0]) & (mk.hold.index <= self.days[-1])]
        pos = np.searchsorted(self.days, allday)
        self.hold = mk.hold.loc[allday].groupby(self.days[pos]).sum()
        self.riskf = mk.risk.loc[allday].groupby(self.days[pos]).sum()
        self.hold_alt = {k: v.loc[allday].groupby(self.days[pos]).sum() for k, v in mk.hold_alt.items()}
        self.level = mk.level
        tday = mk.hold.index[(mk.hold.index >= P.LAUNCH) & (mk.hold.index <= P.LAST_DAY)]
        self.start_i = {i: int(np.searchsorted(tday, reg["first"].iloc[i])) for i in range(len(reg))}
        self.T = len(tday)
        self.lead = len(nyse_days(P.LAST_DAY + pd.Timedelta(days=1), "2026-12-31"))
        self.plan_days = nyse_days("2027-01-01", "2027-12-31")
        self.draft = self._draft(tgt, ids)

    def _draft(self, tgt, ids):
        ws = load_workbook(os.path.join(tgt, PK.F["draft"]), data_only=True)["Draft 2027"]
        out = {}
        for row in ws.iter_rows(min_row=4, values_only=True):
            if not row[0] or row[0] == "Total":
                continue
            n = ids[row[0]]
            chg = {"Increase": "increase", "Decrease": "decrease", "No change": "unchanged", "Onboarding": "onboarding"}[row[4]]
            age = self.T - self.start_i[n] + self.lead          # trading days on the platform at the plan year's first day
            out[n] = dict(k2026=float(row[2]) * 1e6, k2027=float(row[3]) * 1e6, change=chg, age=age, target=float(row[3]) * 1e6)
        return out
