"""task9: the solver-side record, built from the pack alone (never from the simulator). One row per sorted wafer: its final
sort record (a retest supersedes the first pass), its product, interior and outer-band fail rates, its ILD-CMP unit and
polish record, the deposition chamber and scanner it went through, and the usage of each consumable on its unit when
it was polished, rebuilt from the maintenance log's own entries (what each entry's parts text says was replaced, placed
by the platen's wafer counter).
"""
import os
import re
import numpy as np
import openpyxl
import pandas as pd

import pack as PK
import params as P

CANON = {}
for _prod, _p in P.PRODUCTS.items():
    CANON[_prod] = _prod
    for _a in _p["alias"]:
        CANON[_a] = _prod
GROUP = {u: g for g, us in P.CMP_GROUPS.items() for u in us}


def parts_replaced(cls, text):
    """Which of pad, disk and ring an entry replaced, read from its parts text."""
    t = " " + str(text).lower() + " "
    if cls not in ("FULL_PM", "PAD_CHANGE", "UNSCHED"):
        return set()
    out = set()
    if "pad" in t:
        out.add("pad")
    if "ring" in t or "rr-300" in t or "rr300" in t:
        out.add("ring")
    disk = re.search(r"disk|\bcd\b", t)
    if disk and not re.search(r"retained|kept", t):
        out.add("disk")
    return out


class Record:
    def __init__(self, tgt):
        self.tgt = tgt
        self._sort()
        self._fdc()
        self._mes()
        self._pm()
        self._counters()
        self.d = self.sort.merge(self.fdc, on="wafer_id", how="left").merge(self.mes, on="wafer_id", how="left")
        self.d["group"] = self.d.unit.map(GROUP)

    def _sort(self):
        s = pd.read_csv(os.path.join(self.tgt, PK.F["sort"]))
        s["sort_ts"] = pd.to_datetime(s.sort_end_ts)
        s = s.sort_values(["wafer_id", "sort_ts"]).groupby("wafer_id", as_index=False).last()
        s["product"] = s["product"].str.strip().map(CANON)
        self._finish_sort(s)

    def _finish_sort(self, s):
        fz = s[["fail_z%d" % k for k in range(1, 9)]].values.astype(float)
        tz = s[["tested_z%d" % k for k in range(1, 9)]].values.astype(float)
        s["f_in"] = fz[:, :7].sum(axis=1) / tz[:, :7].sum(axis=1)
        s["f_band"] = fz[:, 7] / tz[:, 7]
        s["tested_band"] = tz[:, 7]
        s["gross"] = tz.sum(axis=1)
        s["sort_yield"] = s.good_die / s.gross_die
        self.sort = s[["wafer_id", "lot_id", "product", "sort_ts", "gross_die", "good_die", "f_in", "f_band", "tested_band", "gross",
                       "sort_yield", "adc_label"]]
        self.retests = int((pd.read_csv(os.path.join(self.tgt, PK.F["sort"]), usecols=["retest"]).retest == "Y").sum())

    def _fdc(self):
        f = pd.read_csv(os.path.join(self.tgt, PK.F["fdc"]))
        f["polish_ts"] = pd.to_datetime(f.polish_start_ts)
        f["rr_ratio"] = f.rr_edge_nm_min / f.rr_center_nm_min
        self.fdc = f[["wafer_id", "unit_id", "polish_ts", "platen_wafer_count", "pad_life_ctr", "downforce_psi", "rr_ratio"]].rename(
            columns={"unit_id": "unit", "platen_wafer_count": "platen"})

    def _mes(self):
        m = pd.read_csv(os.path.join(self.tgt, PK.F["mes"]), usecols=["lot_id", "wafer_id", "step_name", "tool_id", "chamber_id", "track_in_ts",
                                                                       "rework"], dtype=str, keep_default_na=False)
        dep = m[m.step_name == "ILD-DEP"][["wafer_id", "chamber_id", "track_in_ts"]].rename(columns={"chamber_id": "dep",
                                                                                                    "track_in_ts": "dep_ts"})
        dep["dep_day"] = dep.dep_ts.str[:10]
        dep = dep.drop(columns=["dep_ts"])
        lit = m[(m.step_name == "M1-LITHO") & (m.rework == "N")][["lot_id", "tool_id"]].drop_duplicates("lot_id").rename(
            columns={"tool_id": "m1_scanner"})
        lots = m[m.wafer_id != ""][["lot_id", "wafer_id"]].drop_duplicates("wafer_id")
        self.mes = dep.merge(lots, on="wafer_id", how="left").merge(lit, on="lot_id", how="left").drop(columns=["lot_id"])

    def _pm(self):
        self._pm_rows()

    def _pm_rows(self, drop_blank=False, back_by_time=False):
        wb = openpyxl.load_workbook(os.path.join(self.tgt, PK.F["pm"]), read_only=True)
        rows = list(wb.active.iter_rows(min_row=2, values_only=True))
        ev = pd.DataFrame(rows, columns=["unit", "event_ts", "event_class", "parts_text", "counter", "tech", "waiver", "entry_note"])
        ev["event_ts"] = pd.to_datetime(ev.event_ts)
        ev["parts"] = [parts_replaced(c, t) for c, t in zip(ev.event_class, ev.parts_text)]
        ev = ev[ev.parts.map(len) > 0].copy()
        miss = ev.counter.isna() | (ev.counter.astype(str) == "")
        if drop_blank:
            ev = ev[~miss].copy()
            miss = miss[~miss]
        if back_by_time:
            miss = miss | (ev.entry_note == "back-entered")
        # entries with no counter are placed by their time on the unit's polish record: the unit polishes nothing while
        # a part is being changed, so the first wafer after the entry is the first on the new part
        for i in ev.index[miss]:
            u = ev.at[i, "unit"]
            f = self.fdc[(self.fdc.unit == u) & (self.fdc.polish_ts >= ev.at[i, "event_ts"])]
            ev.at[i, "counter"] = int(f.platen.min()) if len(f) else np.nan
        ev["counter"] = pd.to_numeric(ev.counter)
        ev = ev[ev.counter.notna()]
        self.events = ev.sort_values(["unit", "counter"]).reset_index(drop=True)

    def _counters(self):
        f = self.fdc.sort_values(["unit", "platen"]).copy()
        for part in ("disk", "pad", "ring", "full"):
            f[part] = np.nan
        for u, g in f.groupby("unit"):
            ev = self.events[self.events.unit == u]
            for part in ("disk", "pad", "ring", "full"):
                if part == "full":
                    c = np.sort(ev[ev.event_class == "FULL_PM"].counter.values)
                else:
                    c = np.sort(ev[ev.parts.map(lambda s: part in s)].counter.values)
                k = np.searchsorted(c, g.platen.values, side="right") - 1
                val = np.where(k >= 0, g.platen.values - c[np.clip(k, 0, None)], np.nan)
                f.loc[g.index, part] = val
                if part == "disk":   # each disk's own life on the unit, named by the counter it was fitted at
                    f.loc[g.index, "disk_life"] = ["%s#%d" % (u, int(c[i])) if i >= 0 else "%s#pre" % u for i in k]
        self.fdc = f
