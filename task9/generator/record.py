"""task9: the solver-side record, built from the pack alone (never from the simulator). One row per data drive with
its family, place, build week, install date (rebuilt where the inventory shows the migration day), the window the
records see it in, and how it left: a replacement (FAIL or PULL, with the pull's trigger), decommissioning, or still
in service. RMA reseats are merged back into one drive; boot SSDs and the QA vault are dropped.
"""
import datetime as dt
import os
import re

import numpy as np
import openpyxl
import pandas as pd

import pack as PK
import params as P

MODEL_FAMILY = {"MD8000NM": "OM-6", "MD14TNM": "M-14", "MD16TNM": "M-16", "TS20000E": "T-20", "TS22000E": "W-22",
                "HX18T8A": "HX-8", "KS10T0A": "KS-10", "VB12000": "VB-12", "TS24000E": "X-24"}


def parse_date(s):
    if not isinstance(s, str) or not s.strip():
        return pd.NaT
    s = s.strip()
    if "/" in s:
        m, d, y = s.split("/")
        return pd.Timestamp(int(y), int(m), int(d))
    return pd.Timestamp(s[:10])


def family_of(model):
    key = re.sub(r"[^A-Z0-9]", "", str(model).upper())
    for m, fam in MODEL_FAMILY.items():
        if key.endswith(m):
            return fam
    return None


def kestrel_week(serial):
    s = serial.replace("-", "")
    if not s.startswith("KS") or len(s) < 13:
        return None
    yy, ww = int(s[4:6]), int(s[6:8])
    try:
        return pd.Timestamp(dt.date.fromisocalendar(2000 + yy, ww, 1))
    except ValueError:
        return None


class Record:
    def __init__(self, tgt, lag_days=None):
        self.tgt = tgt
        inv = pd.read_csv(os.path.join(tgt, PK.F["inventory"]), dtype=str, keep_default_na=False)
        inv["family"] = inv.model_string.map(family_of)
        inv = inv[inv.family.notna() & (inv.vault_id != "") & (inv.vault_id != "QA-01")].copy()
        for c in ("install_date", "first_seen", "last_seen", "removal_date"):
            inv[c] = inv[c].map(parse_date)
        inv["base"] = inv.serial.str.replace(r"-R$", "", regex=True)
        self.raw_inventory = inv
        tk = pd.read_csv(os.path.join(tgt, PK.F["tickets"]), dtype=str, keep_default_na=False)
        tk["opened"] = pd.to_datetime(tk.opened_ts)
        self.tickets = tk
        self._merge_rma(inv)
        self._reasons()
        self._ages(lag_days)
        self.events = pd.read_csv(os.path.join(tgt, PK.F["events"]), dtype=str, keep_default_na=False)
        self.events["date"] = pd.to_datetime(self.events.event_date)

    # ---- a removal followed by the same serial back within 30 days was not a failure
    def _merge_rma(self, inv):
        back = inv[inv.serial.str.endswith("-R")].set_index("base")
        rows = []
        for _, r in inv[~inv.serial.str.endswith("-R")].iterrows():
            r = r.copy()
            if r.serial in back.index:
                b = back.loc[r.serial]
                if pd.notna(r.removal_date) and (b.install_date - r.removal_date).days <= 30:
                    r["last_seen"], r["removal_date"], r["removal_reason"], r["status"] = b.last_seen, b.removal_date, b.removal_reason, b.status
                    r["rma"] = True
            rows.append(r)
        self.d = pd.DataFrame(rows).reset_index(drop=True)
        self.d["rma"] = self.d.get("rma", False)
        self.d["rma"] = self.d["rma"].fillna(False).astype(bool)

    # ---- blank removal reasons from the technicians' tickets (by serial, else by slot and date)
    def _reasons(self):
        d, tk = self.d, self.tickets
        cat = {"DRIVE_FAILURE": "FAIL", "HEALTH_PULL": "PULL"}
        by_serial = {}
        for _, t in tk.iterrows():
            if t.serial:
                by_serial.setdefault(t.serial, []).append(t)
        by_slot = {}
        for _, t in tk.iterrows():
            by_slot.setdefault((t.vault_id, t.chassis_id, t.slot), []).append(t)
        trig = []
        for i, r in d.iterrows():
            reason = r.removal_reason
            note = ""
            if pd.notna(r.removal_date) and r.removal_reason in ("", "FAIL", "PULL"):
                cands = [t for t in by_serial.get(r.serial, []) if abs((t.opened - r.removal_date).days) <= 3]
                if not cands:
                    cands = [t for t in by_slot.get((r.vault_id, r.chassis_id, str(r.slot)), [])
                             if abs((t.opened - r.removal_date).days) <= 3 and t.category in cat]
                if cands:
                    t = cands[0]
                    note = t.tech_note
                    if reason == "":
                        reason = cat.get(t.category, "FAIL")
                elif reason == "":
                    reason = "FAIL"
            d.at[i, "removal_reason"] = reason
            trig.append("187" if re.search(r"187|uncorrectable", note) else ("smart" if reason == "PULL" else ""))
        d["trigger"] = trig
        d["event"] = d.removal_reason.isin(["FAIL", "PULL"]) & d.removal_date.notna()

    # ---- ages: the inventory's install date, except DC-3's migration-day entries, rebuilt
    def _ages(self, lag_days):
        d = self.d
        d["entry"] = d.first_seen
        d["exit"] = d.removal_date.where(d.removal_date.notna(), pd.Timestamp(P.END))
        d["build"] = d.serial.map(kestrel_week)
        kest = d[(d.family == "HX-8") & d.build.notna() & (d.install_date > pd.Timestamp(P.REC_START))]
        self.deploy_lag = float(np.median((kest.install_date - kest.build).dt.days)) if lag_days is None else lag_days
        d["install"] = d.install_date
        mig = (d.dc == "DC-3") & (d.install_date == pd.Timestamp(P.MIGRATION))
        self.migrated = int(mig.sum())
        # the handover manifest's deploy dates, where Brightstore kept them
        wb = openpyxl.load_workbook(os.path.join(self.tgt, PK.F["handover"]), read_only=True)
        man = {}
        for row in wb["rack_manifest"].iter_rows(min_row=3, values_only=True):
            if row[0] and row[2]:
                man[str(row[0]).replace("-", "")] = pd.Timestamp(str(row[2]))
        self.legacy = pd.DataFrame(list(wb["legacy_failure_summary"].iter_rows(min_row=3, values_only=True)),
                                   columns=["rack", "model", "year", "drives_installed", "failures_replaced"])
        poh = self._first_poh()
        rebuilt = []
        for i in np.where(mig)[0]:
            r = d.iloc[i]
            if r.serial in man:
                rebuilt.append((i, man[r.serial], "manifest"))
            elif r.serial in poh:
                rebuilt.append((i, poh[r.serial], "power-on hours"))
            elif pd.notna(r.build):
                rebuilt.append((i, r.build + pd.Timedelta(days=int(round(self.deploy_lag))), "build week"))
        for i, when, how in rebuilt:
            d.at[i, "install"] = when
        d["age_source"] = ""
        for i, _, how in rebuilt:
            d.at[i, "age_source"] = how

    # ---- the batch carrying the elevated hazard, found from the last year's replacements at a cut
    def hot_flags(self, cut, how="scan", min_llr=25.0, widen=0):
        """A boolean per drive: the HX-8 drives whose replacement rate over the year to `cut` stands out. `scan` finds the
        contiguous run of build weeks (from the serial) with the largest likelihood ratio against the rest of the
        family; `firmware` takes the firmware release with the largest one; `vaults` the vaults whose rates stand
        out. Nothing is flagged when the evidence is under `min_llr`."""
        d = self.d
        cut = pd.Timestamp(cut)
        a = cut - pd.Timedelta(days=365)
        flags = pd.Series(False, index=d.index)
        hx = d[(d.family == "HX-8") & (d.entry <= cut)]
        if not len(hx):
            return flags
        lo = np.maximum(hx.entry.values.astype("datetime64[D]"), np.datetime64(a.date()))
        ex_c = hx.exit.where(hx.exit <= cut, cut)
        hi = np.minimum(ex_c.values.astype("datetime64[D]"), np.datetime64(cut.date()))
        X = np.clip((hi - lo).astype(float), 0, None) / 365.25
        O = (hx.event & (hx.removal_date > a) & (hx.removal_date <= cut)).values.astype(float)
        # each vault's own level over the record before that year, shrunk to the family (ten events' weight)
        lo0 = hx.entry.values.astype("datetime64[D]")
        hi0 = np.minimum(ex_c.values.astype("datetime64[D]"), np.datetime64(a.date()))
        X0 = np.clip((hi0 - lo0).astype(float), 0, None) / 365.25
        O0 = (hx.event & (hx.removal_date <= a)).values.astype(float)
        vs = hx.vault_id.values
        r0 = O0.sum() / max(X0.sum(), 1e-9)
        lvl = {}
        for v in np.unique(vs):
            m = vs == v
            lvl[v] = (O0[m].sum() + 10.0) / (X0[m].sum() * r0 + 10.0) if r0 > 0 else 1.0
        X = X * np.array([lvl[v] for v in vs])
        self.hot_levels = lvl
        tot_o, tot_x = O.sum(), X.sum()
        if tot_o <= 0 or tot_x <= 0:
            return flags

        def llr(o, x):
            oo, xx = tot_o - o, tot_x - x
            if o <= 0 or x <= 0 or xx <= 0 or o / x <= oo / max(xx, 1e-9):
                return 0.0
            r0 = tot_o / tot_x
            v = o * np.log(o / x / r0) + (oo * np.log(oo / xx / r0) if oo > 0 else 0.0)
            return float(v)
        if how == "scan":
            wk = hx.build
            ok = wk.notna().values
            idx = ((wk[ok] - pd.Timestamp(2020, 12, 28)).dt.days // 7).astype(int).values
            weeks = np.unique(idx)
            o_w = np.array([O[ok][idx == w].sum() for w in weeks])
            x_w = np.array([X[ok][idx == w].sum() for w in weeks])
            co, cx = np.concatenate([[0], np.cumsum(o_w)]), np.concatenate([[0], np.cumsum(x_w)])
            best = (0.0, None)
            for i in range(len(weeks)):
                for j in range(i, len(weeks)):
                    v = llr(co[j + 1] - co[i], cx[j + 1] - cx[i])
                    if v > best[0]:
                        best = (v, (weeks[i], weeks[j]))
            self.hot_scan = dict(llr=best[0], window=None)
            if best[1] is None or best[0] < min_llr:
                return flags
            w0, w1 = best[1][0] - widen, best[1][1] + widen
            start = pd.Timestamp(2020, 12, 28) + pd.Timedelta(weeks=int(w0))
            end = pd.Timestamp(2020, 12, 28) + pd.Timedelta(weeks=int(w1), days=6)
            self.hot_scan["window"] = (start, end)
            flags.loc[hx.index[ok]] = ((wk[ok] >= start) & (wk[ok] <= end)).values
            return flags
        if how == "firmware":
            best = (0.0, None)
            for fw in hx.firmware.unique():
                m = (hx.firmware == fw).values
                v = llr(O[m].sum(), X[m].sum())
                if v > best[0]:
                    best = (v, fw)
            if best[1] is None or best[0] < min_llr:
                return flags
            flags.loc[hx.index[(hx.firmware == best[1]).values]] = True
            return flags
        if how == "vaults":
            vs = hx.vault_id.values
            rates = sorted(((O[vs == v].sum() / max(X[vs == v].sum(), 1e-9), v) for v in np.unique(vs)), reverse=True)
            best = (0.0, [])
            for k in range(1, len(rates)):
                take = [v for _, v in rates[:k]]
                m = np.isin(vs, take)
                val = llr(O[m].sum(), X[m].sum())
                if val > best[0]:
                    best = (val, take)
            if best[0] < min_llr:
                return flags
            flags.loc[hx.index[np.isin(vs, best[1])]] = True
            return flags
        raise ValueError(how)

    def _first_poh(self):
        q = pd.read_csv(os.path.join(self.tgt, PK.F["quarters"]), usecols=["serial", "quarter", "days_observed", "smart_9_hours_end"],
                        dtype={"serial": str, "quarter": str})
        q = q[q.quarter == "2024Q1"].dropna(subset=["smart_9_hours_end"]).drop_duplicates("serial")
        end = pd.Timestamp(2024, 3, 31)
        return {s: end - pd.Timedelta(hours=float(h)) for s, h in zip(q.serial, q.smart_9_hours_end)}
