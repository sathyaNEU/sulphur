"""Everything owed, computed from the shipped files alone (target/): the cleaned records, each part's removals on the
exposure that drives them, the 2027 exposures from the programme, the propeller control's conversion, the Bodø
shop's turnaround at the 2027 load, the pool's fill rate by spares held, the 80 per cent ranges, and the watch list
read serial by serial. The hurried and quick routes the effort test scores live beside the golden, each a complete
pipeline, so every pass is run end to end on the same pack."""
import datetime as dt
import math
import os
import re

import numpy as np
import pandas as pd

import params as P

PARTS = [p["k"] for p in P.PARTS]
BY_PN = {p["pn"]: p["k"] for p in P.PARTS}
ICAO_BASE = {"ENBO": "BOO", "ENTC": "TOS", "ENBR": "BGO", "ENVA": "TRD"}
Y26 = (pd.Timestamp("2025-11-01"), pd.Timestamp("2026-10-31"))     # the report's twelve months
HIST = (pd.Timestamp("2023-01-01"), pd.Timestamp("2026-11-30"))


# ----------------------------------------------------------------------------------------------- loading

def load(target):
    F = {}
    F["legs"] = pd.read_csv(os.path.join(target, "flight_legs_2023-01_2026-11.csv"), dtype=str)
    F["changes"] = pd.read_csv(os.path.join(target, "component_changes_2023-01_2026-11.csv"), dtype=str, keep_default_na=False)
    F["shop"] = pd.read_csv(os.path.join(target, "bodo_shop_work_orders_2023-2026.csv"), dtype=str, keep_default_na=False)
    F["roster"] = pd.read_csv(os.path.join(target, "bodo_shop_roster_2023-2026.csv"), dtype=str, keep_default_na=False)
    F["vendor"] = pd.read_excel(os.path.join(target, "vendor_repair_orders_2023-2026.xlsx"), dtype=object)
    nu = pd.read_excel(os.path.join(target, "vendor_repair_orders_2023-2026.xlsx"), sheet_name="New units")
    nu.columns = ["po", "pn", "desc", "serial", "ordered", "delivered"]
    F["newunits"] = nu
    F["fleet"] = pd.read_excel(os.path.join(target, "fleet_register.xlsx"), sheet_name="Fleet")
    F["bases"] = pd.read_excel(os.path.join(target, "fleet_register.xlsx"), sheet_name="Base history")
    F["checks"] = pd.read_excel(os.path.join(target, "fleet_register.xlsx"), sheet_name="Heavy checks")
    F["pool"] = pd.read_excel(os.path.join(target, "rotable_stores_snapshot_2026-11-30.xlsx"), dtype=str)
    F["prog"] = pd.read_excel(os.path.join(target, "flying_programme_2027.xlsx"), sheet_name="Programme 2027")
    F["acbase"] = pd.read_excel(os.path.join(target, "flying_programme_2027.xlsx"), sheet_name="Aircraft by base")
    F["wx"] = pd.read_csv(os.path.join(target, "station_weather_daily_2023-2026.csv"), dtype=str, keep_default_na=False)
    F["plan_roster"] = pd.read_excel(os.path.join(target, "bodo_shop_plan_2027.xlsx"), sheet_name="Roster plan")
    F["plan_bench"] = pd.read_excel(os.path.join(target, "bodo_shop_plan_2027.xlsx"), sheet_name="Bench hours")
    return clean(F)


def _base_of(F):
    rows = []
    for _, r in F["bases"].iterrows():
        a = pd.Timestamp(r["From"])
        b = pd.Timestamp(r["To"]) if pd.notna(r["To"]) else HIST[1]
        rows.append((r["Registration"], r["Base"], a, b))
    return rows


def clean(F):
    # legs: the re-sent days' second copies dropped; air time from off and on, or block less the field's usual taxi
    L = F["legs"].drop_duplicates().copy()
    for c in ("out_utc", "off_utc", "on_utc", "in_utc"):
        L[c] = pd.to_datetime(L[c], format="%Y-%m-%dT%H:%MZ", errors="coerce")
    L["date"] = pd.to_datetime(L["flight_date"])
    L["block"] = (L["in_utc"] - L["out_utc"]).dt.total_seconds() / 60.0
    L["air"] = (L["on_utc"] - L["off_utc"]).dt.total_seconds() / 60.0
    L["taxi_out"] = (L["off_utc"] - L["out_utc"]).dt.total_seconds() / 60.0
    L["taxi_in"] = (L["in_utc"] - L["on_utc"]).dt.total_seconds() / 60.0
    tout = L.groupby("dep")["taxi_out"].median()
    tin = L.groupby("arr")["taxi_in"].median()
    miss = L["air"].isna()
    L.loc[miss, "air"] = L.loc[miss, "block"] - L.loc[miss, "dep"].map(tout) - L.loc[miss, "arr"].map(tin)
    L["fh"] = L["air"] / 60.0
    F["legs"] = L
    F["taxi"] = {"out": tout.to_dict(), "in": tin.to_dict()}
    # base each aircraft-day from the register
    B = _base_of(F)
    day = L.groupby(["aircraft", "date"]).agg(cyc=("fh", "size"), fh=("fh", "sum")).reset_index()
    day["base"] = None
    for t, b, a, z in B:
        m = (day["aircraft"] == t) & (day["date"] >= a) & (day["date"] <= z)
        day.loc[m, "base"] = b
    F["day"] = day
    # weather: each base's daily minimum, gaps filled from the day before
    W = F["wx"].copy()
    W["base"] = W["station"].map(ICAO_BASE)
    W["date"] = pd.to_datetime(W["date"])
    W["tmin"] = pd.to_numeric(W["tmin_c"], errors="coerce")
    W = W.sort_values(["base", "date"])
    W["tmin"] = W.groupby("base")["tmin"].ffill()
    F["wx"] = W[["base", "date", "tmin"]]
    day = day.merge(F["wx"], on=["base", "date"], how="left")
    day["frost"] = (-day["tmin"]).clip(lower=0)
    F["day"] = day
    # component changes: a corrected entry replaces the one it corrects; serials as the stores know them; the two
    # reason vocabularies on one footing; part numbers on their current form
    C = F["changes"].copy()
    C["base_no"] = C["change_no"].str.replace(r"-R\d+$", "", regex=True)
    corrected = set(C.loc[C["change_no"].str.contains(r"-R\d+$"), "base_no"])
    C = C[~((C["change_no"] == C["base_no"]) & C["base_no"].isin(corrected))].copy()
    C["serial_off"] = C["serial_off"].str.replace(r"^S/N\s*", "", regex=True).str.upper()
    C["serial_on"] = C["serial_on"].str.upper()
    C["reason"] = C["reason"].replace({"U": "UNSCH", "S": "SCHED", "C": "CONV"})
    desc_k = {p["name"].upper(): p["k"] for p in P.PARTS}
    C["k"] = C["description"].map(desc_k)
    C["date"] = pd.to_datetime(C["change_date"])
    F["changes"] = C
    # findings: the shop's and the repairers' orders, each matched to the removal that sent the unit
    S = F["shop"]
    S = S[S["order_type"] == "ROTABLE"].copy()
    for c in ("received", "parts_received", "work_started", "completed"):
        S[c] = pd.to_datetime(S[c].replace("", np.nan))
    S["parts_wait"] = (S["parts_received"] - S["received"]).dt.days
    S["k"] = S["part_no"].map(BY_PN)
    S["finding_n"] = S.apply(_shop_finding, axis=1)
    S["hours"] = pd.to_numeric(S["hours_booked"].replace("", np.nan))
    V = F["vendor"].copy()
    V.columns = ["order", "vendor", "pn", "serial", "shipped", "at_vendor", "returned", "finding", "amount", "ccy", "fx"]
    V["k"] = V["pn"].map(BY_PN)
    for c in ("shipped", "at_vendor", "returned"):
        V[c] = pd.to_datetime(V[c])
    V["finding"] = V["finding"].fillna("")
    V["finding_n"] = V["finding"].map(_vendor_finding)
    V["sb"] = V["finding"].str.contains("SB 61-0042")
    F["shopr"], F["vendorr"] = S, V
    F["removals"] = _match_findings(C, S, V)
    return F


def _shop_finding(r):
    if r["finding_code"]:
        return {"CONF": "CF", "NFF": "NFF", "BER": "BER"}[r["finding_code"]]
    t = r["finding"].lower()
    if not t:
        return ""
    if "no fault found" in t or "serviceable" in t and "replaced" not in t:
        return "NFF"
    if "beyond economic repair" in t or "scrapped" in t:
        return "BER"
    return "CF"


def _vendor_finding(t):
    t = (t or "").lower()
    if not t:
        return ""
    if t.startswith("sb 27-0089"):
        return "SB"
    if "no fault found" in t:
        return "NFF"
    if "beyond economic repair" in t:
        return "BER"
    return "CF"


def _match_findings(C, S, V):
    """Each removal's shop or repairer order: the first order for that serial received within ten days of the
    removal; the finding, the date the unit was serviceable again, and the work hours."""
    R = C[C["reason"].isin(["UNSCH", "SCHED", "CONV"]) & (C["serial_off"] != "")].copy()
    R["finding"] = ""
    R["back"] = pd.NaT
    R["hours"] = np.nan
    R["shop"] = ""
    shop_by = {sn: g.sort_values("received") for sn, g in S.groupby("serial")}
    ven_by = {sn: g.sort_values("shipped") for sn, g in V.groupby("serial")}
    for i, r in R.iterrows():
        sn, d = r["serial_off"], r["date"]
        k = r["k"]
        if P.PART[k]["shop"] == "BOO":
            g = shop_by.get(sn)
            if g is not None:
                m = g[(g["received"] >= d) & (g["received"] <= d + pd.Timedelta(days=10))]
                if len(m):
                    o = m.iloc[0]
                    R.at[i, "finding"] = o["finding_n"]
                    R.at[i, "back"] = o["completed"] + pd.Timedelta(days=1) if pd.notna(o["completed"]) else pd.NaT
                    R.at[i, "hours"] = o["hours"]
                    R.at[i, "shop"] = "BOO"
        else:
            g = ven_by.get(sn)
            if g is not None:
                m = g[(g["shipped"] >= d) & (g["shipped"] <= d + pd.Timedelta(days=10))]
                if len(m):
                    o = m.iloc[0]
                    R.at[i, "finding"] = o["finding_n"]
                    R.at[i, "back"] = o["returned"]
                    R.at[i, "shop"] = "VND"
    return R


# ----------------------------------------------------------------------------------------------- exposure panels

def panel(F, k, cause="CF"):
    """Aircraft-month counts of a part's unscheduled removals of one kind, beside the aircraft's landings, flight
    hours, calendar days and frost (degree-days below zero on flying days), with the base it flew from."""
    D = F["day"].copy()
    D["ym"] = D["date"].dt.to_period("M")
    g = D.groupby(["aircraft", "ym"]).agg(cyc=("cyc", "sum"), fh=("fh", "sum"), fly=("cyc", "size"),
                                          frost=("frost", "sum"), base=("base", lambda s: s.mode().iat[0] if len(s.mode()) else None)).reset_index()
    pos = P.PART[k]["pos"]
    g["days"] = g["ym"].map(lambda p: p.days_in_month)
    R = F["removals"]
    R = R[(R["k"] == k) & (R["reason"] == "UNSCH")]
    if cause == "CF":
        R = R[R["finding"].isin(["CF", "BER"])]
    elif cause == "NFF":
        R = R[R["finding"] == "NFF"]
    cnt = R.assign(ym=R["date"].dt.to_period("M")).groupby(["aircraft", "ym"]).size().rename("n")
    g = g.merge(cnt, left_on=["aircraft", "ym"], right_index=True, how="left").fillna({"n": 0})
    g = g[(g["ym"] >= pd.Period("2023-01", "M")) & (g["ym"] <= pd.Period("2026-10", "M"))]
    for c in ("cyc", "fh", "days"):
        g[c] = g[c] * pos
    g["frost_rate"] = g["frost"] / g["fly"].clip(lower=1)
    return g


def poisson_fit(y, X, offset, iters=60):
    """Poisson regression with an offset by iteratively reweighted least squares; returns coefficients and the
    log-likelihood."""
    beta = np.zeros(X.shape[1])
    beta[0] = math.log(max(y.sum(), 0.5) / np.exp(offset).sum())
    for _ in range(iters):
        eta = X @ beta + offset
        mu = np.exp(eta)
        z = eta - offset + (y - mu) / mu
        W = mu
        XtW = X.T * W
        try:
            nb = np.linalg.solve(XtW @ X + 1e-9 * np.eye(X.shape[1]), XtW @ z)
        except np.linalg.LinAlgError:
            break
        if np.max(np.abs(nb - beta)) < 1e-9:
            beta = nb
            break
        beta = nb
    mu = np.exp(X @ beta + offset)
    ll = float(np.sum(y * np.log(np.where(mu > 0, mu, 1e-300)) - mu - np.array([math.lgamma(v + 1) for v in y])))
    return beta, ll


DRIVERS = ("cyc", "fh", "days")


def drivers(F, cold=True):
    """For each part, the exposure its confirmed failures follow: a Poisson fit of aircraft-month counts on each
    exposure in turn (with frost), the best by likelihood, and the rates."""
    out = {}
    for k in PARTS:
        g = panel(F, k, "CF")
        y = g["n"].values.astype(float)
        res = {}
        for drv in DRIVERS:
            e = g[drv].values.astype(float)
            ok = e > 0
            X = np.column_stack([np.ones(ok.sum())] + ([g["frost_rate"].values[ok]] if cold else []))
            b, ll = poisson_fit(y[ok], X, np.log(e[ok]))
            res[drv] = {"beta": b, "ll": ll}
        best = max(res, key=lambda d: res[d]["ll"])
        out[k] = {"driver": best, "fits": res, "beta": res[best]["beta"],
                  "ll_gap": res[best]["ll"] - max(v["ll"] for d, v in res.items() if d != best)}
    return out


def nff_rates(F, k, drv):
    """No-fault-found removals per unit of the driving exposure, by the station that made the removal."""
    D = F["day"]
    pos = P.PART[k]["pos"]
    R = F["removals"]
    R = R[(R["k"] == k) & (R["reason"] == "UNSCH") & (R["finding"] == "NFF") & (R["date"] <= Y26[1])]
    ex = D[D["date"] <= Y26[1]].groupby("base").agg(cyc=("cyc", "sum"), fh=("fh", "sum"), days=("date", "size"))
    ex = ex * pos
    n = R.groupby("station").size()
    return {b: float(n.get(b, 0)) / float(ex.loc[b, drv]) for b in ex.index}


# ----------------------------------------------------------------------------------------------- 2027 exposure

def expo_2027(F):
    """2027 landings, flight hours and aircraft-days by month and operating group (each base, and the Helgeland
    routes flown from Bodø), from the programme's departures and block minutes less each field's usual taxi."""
    G = F["prog"].copy()
    G.columns = ["season", "group", "dep", "arr", "from", "to", "per_week", "block"]
    tout, tin = F["taxi"]["out"], F["taxi"]["in"]
    gmap = {"Bodø": "BOO", "Tromsø": "TOS", "Bergen": "BGO", "Trondheim": "TRD", "Bodø (Helgeland routes)": "HEL"}
    G["grp"] = G["group"].map(gmap)
    # a field the record has never seen takes the taxi times of the record's quieter fields
    so, si = float(np.percentile(list(tout.values()), 25)), float(np.percentile(list(tin.values()), 25))
    rows = []
    for _, r in G.iterrows():
        a, b = pd.Timestamp(r["from"]), pd.Timestamp(r["to"])
        days = pd.date_range(a, b, freq="D")
        per_day = float(r["per_week"]) / 7.0
        air = (float(r["block"]) - tout.get(r["dep"], so) - tin.get(r["arr"], si)) / 60.0
        for m, n in pd.Series(1, index=days).groupby(days.month).sum().items():
            rows.append((r["grp"], int(m), per_day * n, per_day * n * air))
    X = pd.DataFrame(rows, columns=["grp", "month", "cyc", "fh"]).groupby(["grp", "month"]).sum().reset_index()
    A = F["acbase"].copy()
    A.columns = ["month", "BOO", "TOS", "BGO", "TRD", "HEL"]
    A["m"] = pd.to_datetime(A["month"]).dt.month
    ad = []
    for _, r in A.iterrows():
        nd = pd.Period("2027-%02d" % r["m"], "M").days_in_month
        for g in ("BOO", "TOS", "BGO", "TRD", "HEL"):
            n = r[g] - (r["HEL"] if g == "BOO" else 0)
            ad.append((g, int(r["m"]), n * nd))
    X = X.merge(pd.DataFrame(ad, columns=["grp", "month", "acdays"]), on=["grp", "month"], how="outer").fillna(0)
    return X


def frost_clim(F):
    """Each base's expected frost on a flying day, by calendar month, from the four winters on record."""
    W = F["wx"].copy()
    W["frost"] = (-W["tmin"]).clip(lower=0)
    W["m"] = W["date"].dt.month
    return W.groupby(["base", "m"])["frost"].mean().to_dict()


def station_of(grp):
    return "BOO" if grp == "HEL" else grp


# ----------------------------------------------------------------------------------------------- forecasts

def pec_split(F):
    """The propeller control's removals per flight hour installed, with and without SB 61-0042: each serial's
    installed spells rebuilt from the changes, its embodiment date from the repairer's returns."""
    k = "PEC"
    V = F["vendorr"]
    moddate = V[V["sb"]].groupby("serial")["returned"].min().to_dict()
    snap = F["pool"]
    snap = snap[snap["Part number"] == P.PART[k]["pn"]]
    D = F["day"].set_index(["aircraft", "date"])["fh"].sort_index()
    spl = [(sn, (tt, pos), a0, b0) for sn, tt, pos, a0, b0 in spells(F, k)]
    fh_by_ac = {t: g.droplevel(0) for t, g in D.groupby(level=0)}
    exp_mod, exp_un = 0.0, 0.0
    for sn, (t, pos), a, b in spl:
        s = fh_by_ac.get(t)
        if s is None:
            continue
        md = moddate.get(sn)
        seg = s[(s.index >= a) & (s.index < b)]
        if md is not None:
            exp_mod += float(seg[seg.index >= md].sum())
            exp_un += float(seg[seg.index < md].sum())
        else:
            exp_un += float(seg.sum())
    R = F["removals"]
    R = R[(R["k"] == k) & (R["reason"] == "UNSCH") & (R["date"] >= pd.Timestamp(P.SB_DATE)) & (R["date"] <= Y26[1])]
    exp_mod_s, exp_un_s = 0.0, 0.0
    for sn, (t, pos), a, b in spl:
        s = fh_by_ac.get(t)
        if s is None:
            continue
        md = moddate.get(sn)
        seg = s[(s.index >= max(a, pd.Timestamp(P.SB_DATE))) & (s.index < min(b, Y26[1] + pd.Timedelta(days=1)))]
        if md is not None:
            exp_mod_s += float(seg[seg.index >= md].sum())
            exp_un_s += float(seg[seg.index < md].sum())
        else:
            exp_un_s += float(seg.sum())
    n_mod = n_un = 0
    nff_mod = nff_un = 0
    for _, r in R.iterrows():
        md = moddate.get(r["serial_off"])
        cf = r["finding"] in ("CF", "BER")
        if md is not None and r["date"] >= md:
            n_mod += cf
            nff_mod += r["finding"] == "NFF"
        else:
            n_un += cf
            nff_un += r["finding"] == "NFF"
    installed = snap[snap["Condition"] == "Installed"]
    mod_now = int((installed["SB 61-0042"] == "Incorporated").sum())
    spare = snap[snap["Condition"] != "Installed"]
    return {"rate_mod": n_mod / max(exp_mod_s, 1.0), "rate_un": n_un / max(exp_un_s, 1.0),
            "nff_rate": (nff_mod + nff_un) / max(exp_mod_s + exp_un_s, 1.0),
            "installed": len(installed), "mod_installed": mod_now,
            "spare_mod": int((spare["SB 61-0042"] == "Incorporated").sum()), "spare_n": len(spare),
            "exp_mod": exp_mod_s, "exp_un": exp_un_s, "n_mod": n_mod, "n_un": n_un}


def pec_forecast(F, fh_month, nff_per_fh, split=None):
    """2027 removals of the propeller control as the fleet converts: a removed unit goes to the repairer and comes
    back modified; the spare fitted in its place is modified at the pool's own share, which rises as the removed
    units come back."""
    s = split or pec_split(F)
    n_inst = float(s["installed"])
    mod_inst = float(s["mod_installed"])
    pool_n = float(max(s["spare_n"], 1))
    pool_mod = float(s["spare_mod"])
    total, cf_tot = 0.0, 0.0
    by_m = {}
    for m in range(1, 13):
        fh = fh_month[m]
        f = mod_inst / n_inst
        rem_un = (1 - f) * fh * (s["rate_un"] + nff_per_fh)
        rem_md = f * fh * (s["rate_mod"] + nff_per_fh)
        cf_tot += (1 - f) * fh * s["rate_un"] + f * fh * s["rate_mod"]
        rem = rem_un + rem_md
        q = pool_mod / pool_n
        mod_inst = min(n_inst, mod_inst - rem_md + rem * q)
        pool_mod = min(pool_n, pool_mod - rem * q + rem)
        by_m[m] = rem
        total += rem
    return total, cf_tot, by_m


def forecast(F, D=None):
    """Each part's expected 2027 unscheduled removals: confirmed failures on the driving exposure with frost, by
    month and operating group, and no-fault-found removals at each station's own rate; the propeller control by
    its conversion."""
    D = D or drivers(F)
    X = expo_2027(F)
    fr = frost_clim(F)
    out = {}
    for k in PARTS:
        p = P.PART[k]
        d = D[k]
        b = d["beta"]
        drv = d["driver"]
        nr = nff_rates(F, k, drv)
        cf, nff = 0.0, 0.0
        by_m = {m: 0.0 for m in range(1, 13)}
        for _, r in X.iterrows():
            st = station_of(r["grp"])
            e = {"cyc": r["cyc"], "fh": r["fh"], "days": r["acdays"]}[drv] * p["pos"]
            frost = fr.get((st, int(r["month"])), 0.0)
            lam = e * math.exp(b[0] + (b[1] * frost if len(b) > 1 else 0.0))
            cf += lam
            nn = e * nr.get(st, np.mean(list(nr.values())))
            nff += nn
            by_m[int(r["month"])] += lam + nn
        out[k] = {"cf": cf, "nff": nff, "total": cf + nff, "by_month": by_m, "driver": drv}
    # the propeller control converts through its own removals
    fhm = X.groupby("month")["fh"].sum().to_dict()
    fhm = {m: fhm.get(m, 0.0) * P.PART["PEC"]["pos"] for m in range(1, 13)}
    sp = pec_split(F)
    nff_fh = out["PEC"]["nff"] / max(sum(fhm.values()), 1.0)
    tot, cf, bym = pec_forecast(F, fhm, nff_fh, sp)
    out["PEC"].update({"total": tot, "cf": cf, "nff": tot - cf, "by_month": bym, "split": sp})
    return out


# ----------------------------------------------------------------------------------------------- turnaround

def findings_mix(F, k, since="2024-01-01"):
    R = F["removals"]
    R = R[(R["k"] == k) & (R["reason"] == "UNSCH") & (R["date"] >= pd.Timestamp(since)) & (R["finding"] != "")]
    n = R["finding"].value_counts()
    tot = float(n.sum())
    return {f: float(n.get(f, 0)) / tot for f in ("CF", "NFF", "BER")} if tot else {"CF": 1.0, "NFF": 0.0, "BER": 0.0}


def vendor_tat(F, k, since="2025-01-01"):
    """Days from removal to the unit's return to serviceable stock, by the repairer's finding."""
    R = F["removals"]
    R = R[(R["k"] == k) & (R["reason"] == "UNSCH") & (R["date"] >= pd.Timestamp(since)) & R["back"].notna()]
    out = {}
    for f in ("CF", "NFF"):
        x = (R[R["finding"] == f]["back"] - R[R["finding"] == f]["date"]).dt.days.values
        out[f] = x if len(x) else (R["back"] - R["date"]).dt.days.values
    return out


def shop_inputs(F):
    """What the Bodø shop's history says about its own process: the transit from each station, the hours a job of
    each kind books, the hours technicians on duty give to rotables once the other work is done."""
    S = F["shopr"]
    R = F["removals"]
    R = R[(R["shop"] == "BOO") & (R["reason"] == "UNSCH")]
    hours = {}
    for k in P.IN_HOUSE:
        for f in ("CF", "NFF", "BER"):
            x = R[(R["k"] == k) & (R["finding"] == f)]["hours"].dropna().values
            hours[(k, f)] = x if len(x) >= 3 else R[(R["k"] == k)]["hours"].dropna().values
    sh = F["shop"]
    oth = sh[sh["order_type"] == "OTHER"].copy()
    oth["date"] = pd.to_datetime(oth["received"])
    oth["h"] = pd.to_numeric(oth["hours_booked"])
    ro = F["roster"].copy()
    ro["date"] = pd.to_datetime(ro["date"])
    ro["h"] = pd.to_numeric(ro["hours_on_duty"])
    duty = ro.groupby("date")["h"].sum()
    rot = S.copy()
    # productive share of duty hours: the hours booked (rotables and other work) against the hours on duty, on
    # weeks the shop had a queue
    booked = (rot.groupby(rot["work_started"].dt.to_period("W"))["hours"].sum().add(
        oth.groupby(oth["date"].dt.to_period("W"))["h"].sum(), fill_value=0))
    dutyw = duty.groupby(duty.index.to_period("W")).sum()
    ratio = (booked / dutyw).dropna()
    prod = float(ratio.quantile(0.9))
    other_share = float((oth.groupby("date")["h"].sum() / duty.reindex(oth["date"].unique()).values).median()) if len(oth) else 0.5
    other_share = float((oth.set_index("date")["h"] / (duty.reindex(oth["date"]).values * prod)).median())
    # roster pattern: technicians and the share absent by month, the July weeks and Christmas
    ro["m"] = ro["date"].dt.month
    absent = ro[ro["date"] >= pd.Timestamp("2025-01-01")].groupby("m")["h"].apply(lambda s: float((s == 0).mean())).to_dict()
    techs = ro["technician"].nunique()
    pw = S[S["finding_n"] == "CF"]["parts_wait"].dropna().values
    r25 = ro[(ro["date"] >= pd.Timestamp("2025-01-01")) & (ro["absence"] != "FERIE")]
    sick = float((r25["absence"] == "SYK").mean())
    trans = {}
    for st in ("BOO", "TOS", "BGO", "TRD"):
        rr = R[R["station"] == st]
        m = []
        for _, r in rr.iterrows():
            g = S[(S["serial"] == r["serial_off"]) & (S["received"] >= r["date"]) & (S["received"] <= r["date"] + pd.Timedelta(days=10))]
            if len(g):
                m.append((g["received"].iloc[0] - r["date"]).days)
        trans[st] = np.array(m) if m else np.array([0])
    # the other work's hours per technician on duty, day by day, over the last two years of the record
    od = oth.groupby("date")["h"].sum()
    on_day = ro[ro["h"] > 0].groupby("date").size()
    opt = (od / on_day.reindex(od.index)).dropna()
    opt = opt[opt.index >= pd.Timestamp("2025-01-01")].values
    rd = ro.assign(d=ro["date"].dt.date)
    duty = rd[rd["h"] > 0].groupby("d").size().reindex(sorted(rd["d"].unique()), fill_value=0).to_dict()
    ferie = rd[rd["absence"] == "FERIE"].groupby("d").size().to_dict()
    other_day = {k.date(): float(v) for k, v in oth.groupby("date")["h"].sum().items()}
    # the 2027 plan: each technician's planned absences, the rotable bench hours a technician on duty gives
    planned = {}
    for _, r in F["plan_roster"].iterrows():
        a0, a1 = pd.Timestamp(r["From"]).date(), pd.Timestamp(r["To"]).date()
        d = a0
        while d <= a1:
            planned[d] = planned.get(d, 0) + 1
            d += dt.timedelta(days=1)
    pb = F["plan_bench"]
    bench = float(pb.iloc[:, 2].mean())
    bench_rot = {(pd.Timestamp(r.iloc[0]).year, pd.Timestamp(r.iloc[0]).month): float(r.iloc[4]) for _, r in pb.iterrows()}
    other_plan = {(pd.Timestamp(r.iloc[0]).year, pd.Timestamp(r.iloc[0]).month): float(r.iloc[3]) / (5.0 * float(r.iloc[1]))
                  for _, r in pb.iterrows()}
    return {"hours": hours, "prod": prod, "other": other_share, "absent": absent, "techs": techs, "trans": trans,
            "parts": pw if len(pw) else np.array([0]), "sick": sick, "other_per_tech": opt, "duty": duty,
            "ferie": ferie, "planned": planned, "bench": bench, "bench_rot": bench_rot, "other_plan": other_plan,
            "other_day": other_day}


def validate_shop(F, inputs, since="2024-06-01", until="2026-09-30", reps=12):
    """The shop's filed bench hours checked on its own record: the replay of every job it took in (from five months
    before the window, so the queue it had comes with it) on the roster's own staffing and the other work it booked
    each day, against the turnarounds it actually ran."""
    R = F["removals"]
    U = R[(R["reason"] == "UNSCH") & (R["shop"] == "BOO") & (R["date"] <= pd.Timestamp(until)) & R["finding"].isin(["CF", "NFF"])
          & R["back"].notna()]
    a0 = pd.Timestamp(since)
    actual = float((U[U["date"] >= a0]["back"] - U[U["date"] >= a0]["date"]).dt.days.mean())
    W = R[(R["reason"] == "UNSCH") & (R["shop"] == "BOO") & (R["date"] >= a0 - pd.DateOffset(months=5)) &
          (R["date"] <= pd.Timestamp(until)) & R["finding"].isin(["CF", "NFF", "BER"])]
    arr = {k: [(r["date"].date(), r["finding"], r["station"]) for _, r in W[W["k"] == k].iterrows()] for k in P.IN_HOUSE}
    tats = []
    for r in range(reps):
        done = shop_replay(F, arr, inputs, np.random.default_rng(900 + r), year=None)
        tats += [x[2] for x in done if x[3] != "BER" and x[1] >= a0.date()]
    return float(np.mean(tats)), actual


def _same_day(d, dates):
    """The same ISO week and weekday one year earlier, or two where the roster does not reach one."""
    y, w, wd = d.isocalendar()
    for back in (1, 2):
        try:
            ref = dt.date.fromisocalendar(y - back, w, wd)
        except ValueError:
            ref = dt.date.fromisocalendar(y - back, w - 1, wd)
        if ref in dates:
            return ref
    return None


def shop_replay(F, arrivals_by_k, inputs, rng, year=2027):
    """The Bodø shop replayed day by day: the removals arriving after their transit, first come first served; on a
    day of the record the technicians the roster has on duty, on a later day the technicians less those the roster
    had on holiday on the same week and weekday a year before, less sickness at the roster's rate; each day's other
    work as the shop booked it."""
    from sim import HOL
    jobs = []
    for k, lst in arrivals_by_k.items():
        for (d, f, st) in lst:
            tr = inputs["trans"].get(st, np.array([0]))
            arrive = d + dt.timedelta(days=int(rng.choice(tr)))
            hrs = inputs["hours"][(k, f)]
            ready = arrive + dt.timedelta(days=int(rng.choice(inputs["parts"]))) if f == "CF" else arrive
            jobs.append({"k": k, "removed": d, "arrive": ready, "left": float(rng.choice(hrs)), "f": f})
    jobs.sort(key=lambda j: (j["arrive"], j["k"]))
    out = []
    i = 0
    queue = []
    if not jobs:
        return out
    d = dt.date(year - 1, 12, 1) if year else min(j["removed"] for j in jobs)
    end = dt.date(year + 1, 3, 31) if year else max(j["arrive"] for j in jobs) + dt.timedelta(days=200)
    T = inputs["techs"]
    while d <= end and (i < len(jobs) or queue):
        while i < len(jobs) and jobs[i]["arrive"] <= d:
            queue.append(jobs[i])
            i += 1
        if d.weekday() < 5 and d not in HOL:
            if year is None and d in inputs["duty"]:
                # a day of the record: the technicians the roster had on duty, less the other work the shop booked
                on = inputs["duty"][d]
                cap = max(0.0, on * inputs["bench"] - inputs["other_day"].get(d, 0.0))
            else:
                # a day of the plan: the technicians not on planned leave, less sickness at the roster's own rate
                on = T - inputs["planned"].get(d, 0)
                on = sum(1 for _ in range(on) if rng.random() > inputs["sick"])
                ym = (d.year, d.month)
                if inputs.get("other_resample"):
                    # the record's own day-to-day spread of third-party work, at the plan's level for the month
                    lvl = inputs["other_plan"].get(ym, 3.6) / max(float(np.mean(inputs["other_per_tech"])), 1e-9)
                    cap = on * max(0.0, inputs["bench"] - lvl * float(rng.choice(inputs["other_per_tech"])))
                else:
                    cap = on * inputs["bench_rot"].get(ym, 3.3)
                cap *= inputs.get("cap_mult", 1.0)
            if inputs.get("queue_order") == "removed":
                queue.sort(key=lambda j: (j["removed"], j["k"]))
            for j in list(queue):
                if cap <= 1e-9:
                    break
                take = min(cap, j["left"])
                j["left"] -= take
                cap -= take
                if j["left"] <= 1e-9:
                    queue.remove(j)
                    out.append((j["k"], j["removed"], (d - j["removed"]).days + 1, j["f"]))
        d += dt.timedelta(days=1)
    return out


# ----------------------------------------------------------------------------------------------- the 2027 year, many times

def lead_times(F):
    """Days from a unit's scrapping to its replacement's delivery, from the purchasing sheet of new units."""
    try:
        N = F["newunits"]
        x = (pd.to_datetime(N["delivered"]) - pd.to_datetime(N["ordered"])).dt.days.dropna().values
        return x if len(x) else np.array([75])
    except KeyError:
        return np.array([75])


def nff_dispersion(F, k):
    """How much more the monthly no-fault-found count varies than a Poisson count with the same mean."""
    R = F["removals"]
    R = R[(R["k"] == k) & (R["reason"] == "UNSCH") & (R["finding"] == "NFF") & (R["date"] <= Y26[1])]
    m = R.groupby(R["date"].dt.to_period("M")).size().reindex(pd.period_range("2023-01", "2026-10", freq="M"), fill_value=0)
    mu = float(m.mean())
    return max(1.0, float(m.var()) / mu) if mu > 0 else 1.0


def frost_years(F):
    """The record's own years of daily frost at each base, December 2026 taken from December 2025."""
    W = F["wx"].copy()
    W["frost"] = (-W["tmin"]).clip(lower=0)
    out = []
    for y in (2023, 2024, 2025, 2026):
        g = W[W["date"].dt.year == y]
        if y == 2026:
            dec = W[(W["date"] >= "2025-12-01") & (W["date"] <= "2025-12-31")].copy()
            dec["date"] = dec["date"] + pd.DateOffset(years=1)
            g = pd.concat([g, dec])
        g = g.assign(doy=g["date"].dt.dayofyear.clip(upper=365))
        out.append({b: g[g["base"] == b].groupby("doy")["frost"].mean().reindex(range(1, 366)).ffill().bfill().values for b in ("BOO", "TOS", "BGO", "TRD")})
    return out


_CALCACHE = {}


def simulate(F, fc, D, reps=300, seed=20271, no_disp=False, no_frost=False, other_resample=False, cap_mult=1.0,
             frost_mult=1.0, queue_order="ready"):
    """The 2027 year replayed: each part's daily removals (its rate on its own exposure, frost from one of the record's
    winters, the rate's own sampling spread, the no-fault-found bursts' month-to-month overdispersion), each
    removal's return through the Bodø shop's queue or the repairer's own turnaround, and the pool replayed to read the
    fill rate at every number of spares."""
    import bisect
    X = expo_2027(F)
    fr = frost_clim(F)
    years = frost_years(F)
    inputs = shop_inputs(F)
    inputs["cap_mult"] = cap_mult
    inputs["other_resample"] = other_resample
    inputs["queue_order"] = queue_order
    lead = lead_times(F)
    alld = pd.date_range("2026-12-01", "2027-12-31", freq="D")
    nd_all = len(alld)
    months = alld.month.values.copy()
    months[alld.year == 2026] = 0                      # December 2026 on the record's own December networks
    doy = np.clip(alld.dayofyear.values, 1, 365) - 1
    dim = np.array([pd.Period(d, "M").days_in_month for d in alld])
    sts = ("BOO", "TOS", "BGO", "TRD")
    mix = {k: findings_mix(F, k) for k in PARTS}
    vt = {k: vendor_tat(F, k) for k in PARTS if P.PART[k]["shop"] != "BOO"}
    disp = {k: (1.0 if no_disp else nff_dispersion(F, k)) for k in PARTS}
    n_events = {k: int(((F["removals"]["k"] == k) & (F["removals"]["reason"] == "UNSCH")).sum()) for k in PARTS}
    snap = F["pool"]
    unsv = {k: int(((snap["Part number"] == P.PART[k]["pn"]) & snap["Condition"].isin(["Unserviceable", "On order"])).sum()) for k in PARTS}
    # expected confirmed and no-fault-found removals by month and station; December 2026 (slot 0) on December 2025's
    # own flying by base, before the Helgeland routes and the moves
    dd = F["day"][(F["day"]["date"] >= pd.Timestamp("2025-12-01")) & (F["day"]["date"] <= pd.Timestamp("2025-12-31"))]
    dec = dd.groupby("base").agg(cyc=("cyc", "sum"), fh=("fh", "sum"), acdays=("date", "size")).to_dict("index")
    base = {}
    for k in PARTS:
        drv = D[k]["driver"]
        b = D[k]["beta"]
        nr = nff_rates(F, k, drv)
        cf = {st: np.zeros(13) for st in sts}
        nf = {st: np.zeros(13) for st in sts}
        for _, r in X.iterrows():
            st = station_of(r["grp"])
            e = {"cyc": r["cyc"], "fh": r["fh"], "days": r["acdays"]}[drv] * P.PART[k]["pos"]
            m = int(r["month"])
            frost = fr.get((st, m), 0.0)
            cf[st][m] += e * math.exp(b[0] + (b[1] * frost if len(b) > 1 else 0.0))
            nf[st][m] += e * nr.get(st, np.mean(list(nr.values())))
        for st, r in dec.items():
            e = {"cyc": r["cyc"], "fh": r["fh"], "days": r["acdays"]}[drv] * P.PART[k]["pos"]
            frost = fr.get((st, 12), 0.0)
            cf[st][0] += e * math.exp(b[0] + (b[1] * frost if len(b) > 1 else 0.0))
            nf[st][0] += e * nr.get(st, np.mean(list(nr.values())))
        # the replay carries the forecast it is given: its confirmed and no-fault-found 2027 totals (the propeller
        # control's conversion, a rival's removals or a perturbed rate), on the month and station profile above
        tot_cf = sum(cf[s][1:].sum() for s in sts)
        tot_nf = sum(nf[s][1:].sum() for s in sts)
        sc_cf = fc[k]["cf"] / tot_cf if tot_cf > 0 else 1.0
        sc_nf = fc[k]["nff"] / tot_nf if tot_nf > 0 else 1.0
        for s in sts:
            cf[s] *= sc_cf
            nf[s] *= sc_nf
        base[k] = (cf, nf)
    exp27 = {k: float(sum(base[k][0][s][1:].sum() + base[k][1][s][1:].sum() for s in sts)) for k in PARTS}
    counts = {k: [] for k in PARTS}
    counts_u = {k: [] for k in PARTS}
    fills = {k: np.zeros(26) for k in PARTS}
    ndem = {k: 0 for k in PARTS}
    tat_in = []
    for rep in range(reps):
        fy = years[rep % len(years)]
        events = {}
        rk = {k: np.random.default_rng([seed, rep, ip]) for ip, k in enumerate(PARTS)}
        for k in PARTS:
            rng = rk[k]
            p = P.PART[k]
            cf, nf = base[k]
            g = 1.0
            phi = disp[k]
            gm = np.ones(13)
            if phi > 1.0:
                mu_m = np.array([sum(nf[s][m] for s in sts) for m in range(13)])
                for m in range(0, 13):
                    if mu_m[m] > 0:
                        a_m = mu_m[m] / (phi - 1.0)
                        gm[m] = rng.gamma(a_m, 1.0 / a_m)
            ev_d, ev_f, ev_s = [], [], []
            for st in sts:
                lam_cf = cf[st][months] / dim * g
                if len(D[k]["beta"]) > 1 and not no_frost:
                    clim = np.array([fr.get((st, m if m else 12), 0.0) for m in range(13)])[months]
                    lam_cf = lam_cf * np.exp(D[k]["beta"][1] * frost_mult * (fy[st][doy] - clim))
                lam_nf = nf[st][months] / dim * gm[months]
                n_cf = rng.poisson(lam_cf)
                n_nf = rng.poisson(lam_nf)
                for idx in np.nonzero(n_cf)[0]:
                    for _ in range(n_cf[idx]):
                        pb = mix[k]["BER"] / max(mix[k]["CF"] + mix[k]["BER"], 1e-9)
                        ev_d.append(idx); ev_f.append("BER" if rng.random() < pb else "CF"); ev_s.append(st)
                for idx in np.nonzero(n_nf)[0]:
                    for _ in range(n_nf[idx]):
                        ev_d.append(idx); ev_f.append("NFF"); ev_s.append(st)
            events[k] = [(alld[i].date(), f, s) for i, f, s in sorted(zip(ev_d, ev_f, ev_s))]
        arrivals_in = {k: list(events[k]) for k in P.IN_HOUSE}
        done = shop_replay(F, arrivals_in, inputs, np.random.default_rng([seed, rep, 99]))
        done = [x for x in done if x[3] != "BER"]
        tat_map = {}
        for k, rem, tat, f in done:
            tat_map.setdefault((k, rem), []).append(tat)
            if rem.year == 2027:
                tat_in.append((k, rem.month, tat, rep))
        for k in PARTS:
            rng = rk[k]
            outs = []
            used = {}
            for (d, f, st) in events[k]:
                if f == "BER":
                    back = d + dt.timedelta(days=int(rng.choice(lead)))
                elif P.PART[k]["shop"] == "BOO":
                    lst = tat_map.get((k, d), [])
                    i = used.get(d, 0)
                    used[d] = i + 1
                    back = d + dt.timedelta(days=int(lst[i] if i < len(lst) else 30))
                else:
                    pool_t = vt[k][f] if len(vt[k][f]) else vt[k]["CF"]
                    back = d + dt.timedelta(days=int(rng.choice(pool_t)))
                outs.append((d, back))
            init = [(dt.date(2026, 11, 30), dt.date(2026, 12, 1) + dt.timedelta(days=int(rng.integers(0, 30)))) for _ in range(unsv[k])]
            allo = sorted(init + outs)
            starts = [a for a, b in allo]
            backs = sorted(b for a, b in allo)
            y27 = [(a, b) for a, b in outs if a.year == 2027]
            counts[k].append(len(y27))
            # the year's count with the expected rate's own uncertainty, for the range: the replay's count moved by
            # the year's expected removals times the rate's own error
            gg = rng.gamma(max(n_events[k], 1), 1.0 / max(n_events[k], 1))
            counts_u[k].append(max(0, int(round(len(y27) + exp27[k] * (gg - 1.0)))))
            for a, b in y27:
                pipe = bisect.bisect_left(starts, a) - bisect.bisect_right(backs, a)
                fills[k][max(pipe, 0) + 1:] += 1
                ndem[k] += 1
    out = {}
    for k in PARTS:
        fr_k = fills[k] / max(ndem[k], 1)
        need = int(np.argmax(fr_k >= P.FILL)) if (fr_k >= P.FILL).any() else 25
        c = np.array(counts[k])
        cu = np.array(counts_u[k])
        out[k] = {"fill": fr_k, "need": need, "p10": int(np.floor(np.percentile(cu, 10))),
                  "p90": int(np.ceil(np.percentile(cu, 90))), "mean": float(c.mean())}
    out["_tat_in"] = tat_in
    return out


# ----------------------------------------------------------------------------------------------- the watch list

def listed(F, end=None):
    """The October watch list: serials with three or more unscheduled removals in the twelve months to the report's
    month end."""
    end = end or Y26[1]
    a = end - pd.DateOffset(years=1) + pd.Timedelta(days=1)
    U = F["removals"]
    U = U[(U["reason"] == "UNSCH") & (U["date"] >= a) & (U["date"] <= end)]
    c = U.groupby("serial_off").agg(n=("date", "size"), k=("k", "first"))
    return c[c["n"] >= 3].sort_values(["k", "n"], ascending=[True, False])


def spells(F, k):
    """Each serial's installed spells, (serial, aircraft, position, from, to), rebuilt from the changes: a unit is on
    a position from the change that fitted it to the change that took it off; the first unit on each position was
    there before the record starts."""
    C = F["changes"]
    C = C[C["k"] == k]
    out = []
    for (t, pos), g in C.groupby(["aircraft", "position"]):
        g = g.sort_values(["date", "change_no"])
        cur, start, first = None, HIST[0], True
        for _, r in g.iterrows():
            if r["serial_off"]:
                if first or cur is None:
                    out.append((r["serial_off"], t, pos, HIST[0] if first else start, r["date"]))
                else:
                    out.append((cur, t, pos, start, r["date"]))
                cur = None
            first = False
            if r["serial_on"]:
                cur, start = r["serial_on"], r["date"]
        if cur:
            out.append((cur, t, pos, start, HIST[1]))
    return out


def aircraft_driven(F, k, window=120, size=3):
    """No-fault-found removals the aircraft drove: one of a run of three or more removals from the same aircraft
    position, by two or more serials, each found serviceable, inside the window."""
    U = F["removals"]
    U = U[(U["k"] == k) & (U["reason"] == "UNSCH")].copy()
    flag = pd.Series(False, index=U.index)
    nff = U[U["finding"] == "NFF"]
    for (t, pos), g in nff.groupby(["aircraft", "position"]):
        g = g.sort_values("date")
        idx, dates, sns = list(g.index), list(g["date"]), list(g["serial_off"])
        for i in range(len(idx)):
            j = i
            while j + 1 < len(idx) and (dates[j + 1] - dates[i]).days <= window:
                j += 1
            if j - i + 1 >= size and len(set(sns[i:j + 1])) >= 2:
                for q in range(i, j + 1):
                    flag[idx[q]] = True
    U["by_aircraft"] = flag
    return U


def fault_windows(U, pad=30, gap=120):
    """The spans an aircraft position was driving removals: from the first to the last removal of each run, padded."""
    win = {}
    for (t, pos), g in U[U["by_aircraft"]].groupby(["aircraft", "position"]):
        ds = sorted(g["date"])
        spans = []
        a = b = ds[0]
        for d in ds[1:]:
            if (d - b).days <= gap:
                b = d
            else:
                spans.append((a - pd.Timedelta(days=pad), b + pd.Timedelta(days=pad)))
                a = b = d
        spans.append((a - pd.Timedelta(days=pad), b + pd.Timedelta(days=pad)))
        win[(t, pos)] = spans
    return win


def serial_exposure(F, k, win=None, upto=None):
    """Each serial's installed exposure since January 2023 on the part's own driving exposure, the days its position
    was driving removals set aside."""
    drv = drivers_cache(F)[k]["driver"]
    D = F["day"]
    col = {"cyc": "cyc", "fh": "fh", "days": None}[drv]
    by_ac = {}
    for t, g in D.groupby("aircraft"):
        s = g.set_index("date")[col] if col else g.set_index("date")["cyc"] * 0 + 1
        by_ac[t] = s.sort_index()
    win = win or {}
    out = {}
    end = (upto or Y26[1]) + pd.Timedelta(days=1)
    for sn, t, pos, a, b in spells(F, k):
        s = by_ac.get(t)
        if s is None:
            continue
        b = min(b, end)
        if b <= a:
            continue
        seg = s[(s.index >= a) & (s.index < b)] if col else pd.Series(1.0, index=pd.date_range(a, b - pd.Timedelta(days=1)))
        for wa, wb in win.get((t, pos), []):
            seg = seg[(seg.index < wa) | (seg.index > wb)]
        out[sn] = out.get(sn, 0.0) + float(seg.sum())
    return out


_DCACHE = {}


def drivers_cache(F):
    key = id(F)
    if key not in _DCACHE:
        _DCACHE[key] = drivers(F)
    return _DCACHE[key]


def mixture_rates(n, e, iters=400):
    """Two groups of serials, each with its own removal rate per unit of exposure, fitted by EM on the serials' own
    counts and exposures; each serial's expected rate is its two group rates weighted by its chance of each."""
    mu = n.sum() / e.sum()
    lo, hi, pi = mu * 0.8, mu * 6.0, 0.05
    for _ in range(iters):
        l1 = n * np.log(max(lo, 1e-12)) - lo * e
        l2 = n * np.log(max(hi, 1e-12)) - hi * e
        a = np.log(1 - pi) + l1
        b = np.log(pi) + l2
        mx = np.maximum(a, b)
        w2 = np.exp(b - mx) / (np.exp(a - mx) + np.exp(b - mx))
        pi = float(np.clip(w2.mean(), 1e-4, 0.5))
        lo = float(((1 - w2) * n).sum() / max(((1 - w2) * e).sum(), 1e-9))
        hi = float((w2 * n).sum() / max((w2 * e).sum(), 1e-9))
        if hi < lo:
            lo, hi = hi, lo
    l1 = n * np.log(max(lo, 1e-12)) - lo * e
    l2 = n * np.log(max(hi, 1e-12)) - hi * e
    a = np.log(1 - pi) + l1
    b = np.log(pi) + l2
    mx = np.maximum(a, b)
    w2 = np.exp(b - mx) / (np.exp(a - mx) + np.exp(b - mx))
    return lo, hi, pi, w2


def watch_golden(F, fc=None, estimator="mixture", new_unit="pooled", window=120, upto=None):
    """Each listed serial's expected 2027 removals over a new unit in its place: its own removals (those its
    aircraft drove set aside) over its installed exposure, to the end of the latest report's months, read through the
    two groups the part's serials form; a new unit at the part's expected rate; the saving the whole list's scrapping
    buys, and the serials worth scrapping."""
    L = listed(F)
    X = expo_2027(F)
    res = []
    for k, g in L.groupby("k"):
        U = aircraft_driven(F, k, window=window)
        win = fault_windows(U, gap=window)
        inwin = U.apply(lambda r: any(a <= r["date"] <= b for a, b in win.get((r["aircraft"], r["position"]), [])), axis=1) if len(U) else U["by_aircraft"]
        end = upto or Y26[1]
        own = U[~U["by_aircraft"] & ~inwin & (U["date"] <= end)].groupby("serial_off").size()
        ex = serial_exposure(F, k, win, upto=end)
        sns = [s for s in ex if ex[s] > 0]
        n = np.array([float(own.get(s, 0)) for s in sns])
        e = np.array([ex[s] for s in sns])
        mu = n.sum() / e.sum()
        m = mu * e
        denom = float(np.sum((n - m) ** 2 - m))
        alpha = float(np.sum(m ** 2) / denom) if denom > 0 else 1e6
        lo, hi, pi, w2 = mixture_rates(n, e)
        post = dict(zip(sns, w2))
        # a new unit fitted in the serial's place (standard 5.1): the part's own removals pooled over its serials'
        # exposure, the removals the aircraft drove set aside on both sides (they come with the position whichever unit
        # is fitted); the healthy group's rate is the rival reading
        mu_new = lo if new_unit == "healthy" else mu
        drv = drivers_cache(F)[k]["driver"]
        e27 = float({"cyc": X["cyc"].sum(), "fh": X["fh"].sum(), "days": 365.0 * P.FLEET_N}[drv]) / P.FLEET_N
        Rk = F["removals"]
        Rk = Rk[(Rk["k"] == k) & (Rk["reason"] == "UNSCH") & Rk["back"].notna() & (Rk["date"] >= pd.Timestamp("2025-01-01"))]
        tat_k = float((Rk["back"] - Rk["date"]).dt.days.mean()) if len(Rk) else 20.0
        for sn in g.index:
            ns, es = float(own.get(sn, 0)), ex.get(sn, 0.0)
            if estimator == "mixture":
                q = post.get(sn, 0.0)
                lam = q * hi + (1 - q) * lo
            elif estimator == "raw":
                lam = ns / es if es > 0 else mu
            else:
                lam = (alpha + ns) / (alpha / mu + es) if es > 0 else mu
            # the position's removals over a year with the serial kept: the serial installed between its repairs, a
            # healthy unit in the position while it is away; against a new unit there all year
            per_year = lam * e27
            on_wing = 1.0 / (1.0 + per_year * tat_k / 365.0)
            saving = on_wing * (lam - mu_new) * e27
            res.append({"serial": sn, "k": k, "n12": int(g.loc[sn, "n"]), "own": int(ns), "exposure": es,
                        "rate": lam, "excess": saving, "per_installed_year": (lam - mu_new) * e27, "on_wing": on_wing,
                        "tat": tat_k, "by_aircraft": int(U[(U["serial_off"] == sn) & U["by_aircraft"]].shape[0])})
    W = pd.DataFrame(res).set_index("serial")
    W["scrap"] = W["excess"] >= P.SCRAP_EXCESS
    return W, float(W["excess"].sum())


def watch_hurried(F):
    """The hurried readings of the list: every listed removal at face value against the part's average; and the
    confirmed failures alone, the no-fault-found removals set aside, read off the same twelve months."""
    L = listed(F)
    a = Y26[1] - pd.DateOffset(years=1) + pd.Timedelta(days=1)
    U = F["removals"]
    U = U[(U["reason"] == "UNSCH") & (U["date"] >= a) & (U["date"] <= Y26[1])]
    out = {}
    face, cf_only, cf_set, face_set = 0.0, 0.0, [], []
    for k, g in L.groupby("k"):
        units = P.FLEET_N * P.PART[k]["pos"] + P.POOL[k]
        avg = (U["k"] == k).sum() / units
        avg_cf = ((U["k"] == k) & U["finding"].isin(["CF", "BER"])).sum() / units
        for sn in g.index:
            face += g.loc[sn, "n"] - avg
            face_set.append(sn)
            ncf = int(((U["serial_off"] == sn) & U["finding"].isin(["CF", "BER"])).sum())
            cf_only += ncf - avg_cf
            if ncf - avg_cf >= P.SCRAP_EXCESS:
                cf_set.append(sn)
    return {"face": face, "face_set": face_set, "cf_only": cf_only, "cf_set": cf_set}



# ----------------------------------------------------------------------------------------------- the hurried routes

def palm(lam_per_day, tat_days, target=P.FILL):
    """The spares Palm's theorem gives: the least stock whose Poisson pipeline is under it with the target chance."""
    m = lam_per_day * tat_days
    s, cdf, term = 0, math.exp(-m), math.exp(-m)
    while cdf < target:
        s += 1
        term *= m / s
        cdf += term
    return s + 1


def pec_current_mix(F, n27_fh_pos, nff_fh):
    """The propeller control as a careful run reads it from the repairers' orders: the modified and unmodified rates
    split by one group-by, applied at the fleet's mix at the snapshot, with no conversion through 2027."""
    s = pec_split(F)
    f = s["mod_installed"] / s["installed"]
    return n27_fh_pos * (f * s["rate_mod"] + (1 - f) * s["rate_un"] + nff_fh)


def hurried(F, exposure="fh", tat="avg", D=None, fc=None):
    """The careful but hurried route and its variants: each part on its twelve months' unscheduled removals per
    flight hour (or on the driving exposure, or the golden forecast), the 2026 average turnaround (or the golden's),
    Palm's spares on a Poisson pipeline."""
    R = F["removals"]
    U = R[(R["reason"] == "UNSCH")]
    Dd = F["day"]
    m12 = (Dd["date"] >= Y26[0]) & (Dd["date"] <= Y26[1])
    X = expo_2027(F)
    tot27 = {"fh": X["fh"].sum(), "cyc": X["cyc"].sum(), "days": X["acdays"].sum()}
    tot12 = {"fh": Dd[m12]["fh"].sum(), "cyc": Dd[m12]["cyc"].sum(), "days": float(P.FLEET_N * 365)}
    out = {}
    for k in PARTS:
        n12 = int(((U["k"] == k) & (U["date"] >= Y26[0]) & (U["date"] <= Y26[1])).sum())
        if exposure == "fh":
            proj = n12 / tot12["fh"] * tot27["fh"]
        elif exposure == "golden":
            proj = fc[k]["total"]
        else:
            drv = (D or drivers_cache(F))[k]["driver"]
            proj = n12 / tot12[drv] * tot27[drv]
        if k == "PEC" and exposure == "fh":
            nff12 = int(((U["k"] == k) & (U["date"] >= Y26[0]) & (U["date"] <= Y26[1]) & (U["finding"] == "NFF")).sum())
            proj = pec_current_mix(F, tot27["fh"] * P.PART[k]["pos"], nff12 / (tot12["fh"] * P.PART[k]["pos"]))
        r26 = U[(U["k"] == k) & (U["date"] >= pd.Timestamp("2026-01-01")) & U["back"].notna()]
        t_avg = float((r26["back"] - r26["date"]).dt.days.mean()) if len(r26) else 20.0
        # the range a careful run bootstraps unprompted: the twelve months' removals resampled month by month, scaled
        # to 2027's exposure as the projection is
        mm = U[(U["k"] == k) & (U["date"] >= Y26[0]) & (U["date"] <= Y26[1])]
        mc = mm.groupby(mm["date"].dt.to_period("M")).size().reindex(pd.period_range(Y26[0], Y26[1], freq="M"), fill_value=0).values
        rng = np.random.default_rng(1000 + PARTS.index(k))
        boot = np.array([rng.choice(mc, size=12, replace=True).sum() for _ in range(2000)]) * (proj / max(n12, 1))
        out[k] = {"n12": n12, "proj": proj, "tat": t_avg, "spares": palm(proj / 365.0, t_avg),
                  "p10": float(np.floor(np.percentile(boot, 10))), "p90": float(np.ceil(np.percentile(boot, 90)))}
    return out


def _pois_q(m, q):
    k, cdf, term = 0, math.exp(-m), math.exp(-m)
    while cdf < q:
        k += 1
        term *= m / k
        cdf += term
    return k
