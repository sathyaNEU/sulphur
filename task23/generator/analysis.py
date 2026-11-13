"""task23 architecture 1: the analysis read back from the cut pack alone (never from the simulation), every method
choice a switch, so the golden, each hurried route, the rivals and the perturbations run on one code path.

    switches (GOLDEN in capitals):
      tickets  CLEAN (voids dropped, old codes mapped, blank areas from the daily log) | raw (every row as filed)
      baro     EMA (chamber flux on the barometer's lagged gap, the lag chosen by fit) | dp12 | dp24 (pressure change
               over 12 or 24 hours) | ema_ac1 (cell 4's chamber alone) | none (the campaigns' rates as measured)
      level    TCM (the state's campaigns) | tcm_drone (with the drone flights, inverse-variance) | drone
      kwet     True (the reached waste's decay fitted on the pumped wells) | False (one decay for all waste)
      r3       ZONES (dry wells and pumped wells, weighted by count) | collected (cell 4's collected gas) |
               dry (the dry wells alone) | pumped (the pumped wells alone)
      ox       SAT (a saturating capacity with a shared temperature factor) | exp | loglin | mean (the study's
               cover-type means) | default (the reporting rule's 10 per cent)
      c5       ANCHOR (cell 5 calibrated on its spring 2026 campaigns) | waste (cell 5 on cell 4's methane potential)
      pumps    YIELD (a yield model fitted on the pilot) | ratio (the pilot's mean flow ratio)
      ramp     the months over which the reached waste's decay moves to the faster rate (0)
      ce4      ZONES (cell 4's 2027 collection by zone, each zone's August to October 2026 efficiency carried with its
               own generation) | flat (cell 4's efficiency held at its August to October 2026 level)
      calib    (campaigns) | closed (the level from the closed cells' collected gas) | rule (the rule's potential)
"""
import datetime as dt
import math
import os

import numpy as np
import pandas as pd
from scipy.optimize import brentq, least_squares

import params as P

TONNE = 0.90718474
NM = (P.YEND - P.Y0) * 12
GOLDEN = dict(tickets="clean", baro="ema", level="tcm", kwet=True, r3="zones", ox="sat", c5="anchor",
              pumps="yield", ramp=0, kd_scale=1.0, kw_scale=1.0, v_scale=1.0, corr_shift=0.0, gain_scale=1.0,
              s5_scale=1.0, ce4="zones")
OLD_TO_NEW = {"MSW-COM": "MSW", "MSW-RES": "MSW", "MSW-TS": "MSW", "CD-MIX": "C&D", "SLDG": "BIOSOLIDS",
              "CVR-SOIL": "ADC-SOIL", "SPW-ASB": "SPECIAL", "SPW-OTH": "SPECIAL"}
MAT_OF = {"MSW": "MSW", "C&D": "CD", "BIOSOLIDS": "BIO", "ADC-SOIL": "SOIL", "SPECIAL": "SPEC"}


def mi(y, m):
    return (y - P.Y0) * 12 + (m - 1)


def mo(i):
    return P.Y0 + i // 12, i % 12 + 1


def dim(i):
    y, m = mo(i)
    return ((dt.date(y + (m == 12), m % 12 + 1, 1)) - dt.date(y, m, 1)).days


DIM = np.array([dim(i) for i in range(NM)], dtype=float)


# ------------------------------------------------------------------ loading the pack
def load(target):
    f = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    F = {}
    t = pd.read_csv(f["tickets"], dtype={"disposal_area": str, "status": str, "vehicle_id": str})
    t["ticket_date"] = pd.to_datetime(t["ticket_date"]).dt.date
    F["tickets"] = t
    F["history"] = pd.read_excel(f["history"], sheet_name="Tonnage by cell")
    F["cells"] = pd.read_excel(f["history"], sheet_name="Cells")
    lg = pd.read_csv(f["dailylog"])
    lg["log_date"] = pd.to_datetime(lg["log_date"]).dt.date
    F["dailylog"] = lg
    F["scada"] = pd.read_csv(f["scada"])
    w = pd.read_csv(f["wells"], dtype={"depth_to_liquid_ft": str})
    w["visit_date"] = pd.to_datetime(w["visit_date"]).dt.date
    F["wells"] = w
    F["register"] = pd.read_excel(f["register"], sheet_name="Wells")
    F["workorders"] = pd.read_csv(f["workorders"])
    F["recirc"] = pd.read_csv(f["recirc"])
    F["weather"] = pd.read_csv(f["weather"])
    F["chambers"] = pd.read_csv(f["chambers"])
    c = pd.read_csv(f["campaigns"])
    c["date"] = pd.to_datetime(c["date"]).dt.date
    F["campaigns"] = c
    d = pd.read_excel(f["drone"], sheet_name="Flights")
    d["date"] = pd.to_datetime(d["date"]).dt.date
    F["drone"] = d
    F["oxplots"] = pd.read_csv(f["oxplots"])
    F["fillplan"] = pd.read_excel(f["fillplan"], sheet_name="Cell 5 receipts")
    return F


# ------------------------------------------------------------------ R1 and the waste in place
def tickets_monthly(F, how="clean"):
    t = F["tickets"].copy()
    if how == "clean":
        t = t[t["status"].fillna("") != "VOID"]
        t["code"] = t["material_code"].map(lambda x: OLD_TO_NEW.get(x, x))
        log = dict(zip(F["dailylog"]["log_date"], F["dailylog"]["active_cell"]))
        area = t["disposal_area"].fillna("")
        fill = [log.get(d, "C4" if d < dt.date(2025, 2, 1) else "C5") if a == "" else a
                for a, d in zip(area, t["ticket_date"])]
        t["area"] = fill
    else:
        t["code"] = t["material_code"]
        t["area"] = t["disposal_area"].fillna("")
    t["mat"] = t["code"].map(lambda x: MAT_OF.get(x, MAT_OF.get(OLD_TO_NEW.get(x, ""), "MSW")))
    t["m"] = [mi(d.year, d.month) for d in t["ticket_date"]]
    return t


def r1_cell5_msw(F, how="clean"):
    t = tickets_monthly(F, how)
    if how == "clean":
        sel = (t["area"] == "C5") & (t["mat"] == "MSW") & (t["ticket_date"] <= dt.date(2026, 10, 31))
    else:
        sel = (t["area"] == "C5") & (t["ticket_date"] <= dt.date(2026, 10, 31))
    return float(t.loc[sel, "net_tons"].sum())


def waste_potential(F, how="clean", L0=None):
    """{cell: m3 of methane potential placed each month, 1986 to 2027}: the history by cell and material spread over
    each year's months in place, the tickets from 2021, the fill plan from November 2026."""
    L0 = L0 or P.L0_RULE
    pot = {c: np.zeros(NM) for c in P.CELLS}
    H = F["history"]
    cells = F["cells"]
    first = {int(r["cell"]): pd.Timestamp(r["first_waste"]).date() for _, r in cells.iterrows()}
    last = {int(r["cell"]): (pd.Timestamp(r["last_waste"]).date() if str(r["last_waste"]) != "filling"
                             else dt.date(2028, 12, 31)) for _, r in cells.iterrows()}
    cols = {"msw_tons": "MSW", "cd_tons": "CD", "biosolids_tons": "BIO", "soil_tons": "SOIL", "special_tons": "SPEC"}
    for _, r in H.iterrows():
        y, c = int(r["year"]), int(r["cell"])
        months = [m for m in range(1, 13) if dt.date(y, m, 1) >= dt.date(first[c].year, first[c].month, 1)
                  and dt.date(y, m, 1) <= dt.date(last[c].year, last[c].month, 1)]
        if not months:
            continue
        v = sum(float(r[k]) * TONNE * L0[mat] for k, mat in cols.items())
        for m in months:
            pot[c][mi(y, m)] += v / len(months)
    t = tickets_monthly(F, how)
    t = t[t["area"].isin(["C4", "C5"])]
    g = t.groupby(["area", "m", "mat"])["net_tons"].sum()
    for (a, m, mat), v in g.items():
        pot[int(a[1])][m] += v * TONNE * L0[mat]
    fp = F["fillplan"]
    for _, r in fp.iterrows():
        y, m = [int(x) for x in str(r["month"]).split("-")]
        if (y, m) < (2026, 11):
            continue
        v = sum(float(r[k]) * TONNE * L0[mat] for k, mat in cols.items() if k in fp.columns)
        pot[5][mi(y, m)] += v
    return pot


def fod(placed, kd, kw, reach, rec_month, lag=P.LAG_MONTHS, ramp=0):
    n = len(placed)
    g = np.zeros(n)
    gw_out = np.zeros(n)
    pend = np.zeros(n + lag + 1)
    pd_, pw = 0.0, 0.0
    for i in range(n):
        pend[i + lag] += placed[i]
        r = reach if rec_month is not None else 0.0
        pw += pend[i] * r
        pd_ += pend[i] * (1 - r)
        if rec_month is not None and i >= rec_month:
            w = 1.0 if ramp <= 0 else min(1.0, (i - rec_month + 1) / ramp)
        else:
            w = 0.0
        kr = kd + (kw - kd) * w
        gw = pw * (1 - math.exp(-kr / 12.0))
        gd = pd_ * (1 - math.exp(-kd / 12.0))
        pw -= gw
        pd_ -= gd
        g[i] = gw + gd
        gw_out[i] = gw
    return g, gw_out


# ------------------------------------------------------------------ the wells
def well_table(F):
    w = F["wells"].copy()
    reg = F["register"].copy()
    reg = reg[reg["type"] == "VW"]
    cell = {}
    for _, r in reg.iterrows():
        c = r["cell"]
        if pd.isna(c) or str(c).strip() == "":
            c = int(str(r["well_id"]).split("-")[1][0])
        cell[r["well_id"]] = int(c)
    w["cell"] = w["well_id"].map(cell)
    w["ch4_scfm"] = w["adj_flow_scfm"] * w["ch4_pct"] / 100.0
    w["m"] = [mi(d.year, d.month) for d in w["visit_date"]]
    sb = dict(zip(reg["well_id"], reg["screen_bottom_ft"]))
    st = dict(zip(reg["well_id"], reg["screen_top_ft"]))
    td = dict(zip(reg["well_id"], reg["total_depth_ft"]))

    def subm(row):
        v = row["depth_to_liquid_ft"]
        if pd.isna(v) or v == "":
            return np.nan
        if str(v).upper() == "DRY":
            return 0.0
        x = float(v)
        b, tp = sb[row["well_id"]], st[row["well_id"]]
        if x >= b:
            return 0.0
        return min(1.0, (b - x) / (b - tp))
    w["sub"] = w.apply(subm, axis=1)
    pump = {r["well_id"]: (pd.Timestamp(r["pump_installed"]).date() if not pd.isna(r["pump_installed"]) else None)
            for _, r in reg.iterrows()}
    return w, pump


def well_ratio(w, ids, a0, a1, b0, b1):
    """Ratio of summed methane flow over months [b0, b1) to [a0, a1) for the wells read in both."""
    A = w[(w["well_id"].isin(ids)) & (w["m"] >= a0) & (w["m"] < a1)].groupby("well_id")["ch4_scfm"].mean()
    B = w[(w["well_id"].isin(ids)) & (w["m"] >= b0) & (w["m"] < b1)].groupby("well_id")["ch4_scfm"].mean()
    common = sorted(set(A.index) & set(B.index))
    return float(B[common].sum() / A[common].sum()), len(common)


def cell4_zones(F, sw):
    w, pump = well_table(F)
    c4 = w[w["cell"] == 4]
    ids = sorted(c4["well_id"].unique())
    wet = sorted(c4[(c4["m"] >= mi(2023, 1)) & (c4["sub"] > 0.02)]["well_id"].unique())
    dry = [x for x in ids if x not in wet]
    pumped = [x for x in wet if pump.get(x)]
    share_wet = len(wet) / len(ids)
    p22, p26 = (mi(2022, 1), mi(2023, 1)), (mi(2025, 11), mi(2026, 11))
    r_dry, n_dry = well_ratio(w, dry, *p22, *p26)
    r_pump, n_pump = well_ratio(w, pumped, *p22, *p26)
    r_all, _ = well_ratio(w, ids, *p22, *p26)
    return dict(w=w, pump=pump, ids=ids, wet=wet, dry=dry, pumped=pumped, share_wet=share_wet, r_dry=r_dry,
                r_pump=r_pump, r_collected=r_all, n_dry=n_dry, n_pump=n_pump)


def kd_closed(F):
    """The dry decay from the closed cells' collected gas, 2019 to the twelve months to October 2026."""
    w, _ = well_table(F)
    cl = w[w["cell"].isin([1, 2, 3])]
    ids = sorted(cl["well_id"].unique())
    r, _ = well_ratio(w, ids, mi(2019, 1), mi(2020, 1), mi(2025, 11), mi(2026, 11))
    years = (mi(2025, 11) + 6 - (mi(2019, 1) + 6)) / 12.0
    return -math.log(r) / years


def recirc_months(F):
    """{cell: the month the faster decay begins}: the month after the log's first injection into the cell."""
    r = F["recirc"]
    r = r[r["days_injecting"] > 0]
    out = {}
    for c, g in r.groupby("cell"):
        y, m = [int(x) for x in str(g["month"].min()).split("-")]
        out[int(c)] = mi(y, m) + 1
    return out


def fit_kw(pot4, kd, share_wet, r_target, ramp=0, rec=None):
    rec = rec if rec is not None else mi(P.RECIRC[4].year, P.RECIRC[4].month) + 1
    p22, p26 = slice(mi(2022, 1), mi(2023, 1)), slice(mi(2025, 11), mi(2026, 11))

    def ratio(kw):
        g, gw = fod(pot4, kd, kw, share_wet, rec, ramp=ramp)
        return gw[p26].sum() / gw[p22].sum()
    return brentq(lambda k: ratio(k) - r_target, kd * 0.5, 0.6)


# ------------------------------------------------------------------ the barometer and the campaigns
def weather_lst(F):
    wx = F["weather"].copy()
    ts = pd.to_datetime(wx["timestamp_lst"].str[:16])
    wx["t"] = ts
    wx = wx.set_index("t").sort_index()
    full = pd.date_range(wx.index.min(), wx.index.max(), freq="h")
    wx = wx[~wx.index.duplicated()].reindex(full)
    wx[["baro_hpa", "soil_temp_10cm_c", "air_temp_c"]] = wx[["baro_hpa", "soil_temp_10cm_c", "air_temp_c"]].interpolate(limit=48)
    wx["rain_mm"] = wx["rain_mm"].fillna(0.0)
    return wx


def ema(x, tau):
    out = np.empty_like(x)
    out[0] = x[0]
    a = 1.0 / tau
    for k in range(1, len(x)):
        out[k] = out[k - 1] + a * (x[k] - out[k - 1])
    return out


def baro_fit(F, how="ema", wx=None):
    wx = wx if wx is not None else weather_lst(F)
    p = wx["baro_hpa"].values.astype(float)
    ch = F["chambers"].copy()
    use = {"ema_ac1": ["AC-1"], "ema_all": ["AC-1", "AC-2", "AC-3"],
           "ema_hl16_all": ["AC-1", "AC-2", "AC-3"]}.get(how, ["AC-1", "AC-3"])
    ch = ch[(ch["qc"] == "OK") & (ch["chamber"].isin(use))]
    ch["t"] = pd.to_datetime(ch["utc"].str[:19]) - pd.Timedelta(hours=8)
    ch = ch[ch["flux_g_m2_d"] > 0]
    idx = wx.index.get_indexer(ch["t"])
    ok = idx >= 0
    ch, idx = ch[ok], idx[ok]
    rain6 = np.convolve(wx["rain_mm"].values, np.ones(6), mode="full")[:len(wx)]
    y = np.log(ch["flux_g_m2_d"].values)
    grp = (ch["chamber"] + "_" + ch["t"].dt.strftime("%Y-%m")).values
    gcodes, ginv = np.unique(grp, return_inverse=True)
    dT = ch["soil_temp_c"].values - pd.Series(ch["soil_temp_c"].values).groupby(ginv).transform("mean").values

    def design(x):
        X = np.zeros((len(y), len(gcodes) + 3))
        X[np.arange(len(y)), ginv] = 1.0
        X[:, -3] = x[idx]
        X[:, -2] = dT
        X[:, -1] = rain6[idx]
        return X
    best = None
    if how in ("ema", "ema_ac1", "ema_all", "ema_hl16_all") or how.startswith("ema_tau"):
        taus = (4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 30, 36, 48)
        if how.startswith("ema_tau"):
            taus = (int(how[7:]),)
        if how == "ema_hl16_all":
            # an exponential mean with a 16-hour half-life, not chosen by fit, on all three chambers
            taus = (1.0 / (1.0 - 0.5 ** (1.0 / 16.0)),)
        for tau in taus:
            x = ema(p, tau) - p
            X = design(x)
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            sse = float(((y - X @ beta) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, tau, float(beta[-3]))
        sse, tau, c = best
        gap = ema(p, tau) - p
    else:
        L = 12 if how == "dp12" else 24
        x = np.r_[np.zeros(L), -(p[L:] - p[:-L])]
        X = design(x)
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        c, tau, gap = float(beta[-3]), L, x
        sse = float(((y - X @ beta) ** 2).sum())
    m = np.exp(c * gap)
    years = wx.index.year.values
    for yv in np.unique(years):
        s = years == yv
        m[s] /= np.nanmean(m[s])
    return dict(tau=tau, c=c, m=pd.Series(m, index=wx.index), sse=sse, n=len(y))


def local_to_lst(d, hhmm):
    """A local wall-clock time on date d to local standard time."""
    hh, mm = [int(x) for x in str(hhmm).split(":")]
    loc = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=P.TZ)
    return (loc.astimezone(P.UTC) - dt.timedelta(hours=8)).replace(tzinfo=None)


def window_factor(mser, d, start, end):
    a = local_to_lst(d, start)
    b = local_to_lst(d, end)
    s = mser[(mser.index >= pd.Timestamp(a).floor("h")) & (mser.index < pd.Timestamp(b))]
    return float(s.mean())


def corrected_rates(F, sw, B):
    c = F["campaigns"].copy()
    d = F["drone"].copy()
    if sw["baro"] == "none":
        c["m"] = 1.0
        d["m"] = 1.0
    else:
        c["m"] = [window_factor(B["m"], r["date"], r["start_local"], r["end_local"]) for _, r in c.iterrows()]
        d["m"] = [window_factor(B["m"], r["date"], r["takeoff"], r["landing"]) for _, r in d.iterrows()]
        c["m"] = c["m"] + sw.get("corr_shift", 0.0)
        d["m"] = d["m"] + sw.get("corr_shift", 0.0)
    c["site_corr"] = c["site_kg_h"] / c["m"]
    c["cell4_corr"] = c["cell4_kg_h"] / c["m"]
    c["cell5_corr"] = c["cell5_kg_h"] / c["m"]
    d["flux_corr"] = d["flux_kg_h"] / d["m"]
    return c, d


def actual_2025(c, d, how="tcm"):
    c5 = c[pd.to_datetime(c["date"]).dt.year == 2025]
    d5 = d[pd.to_datetime(d["date"]).dt.year == 2025]
    if how == "tcm":
        rate = c5["site_corr"].mean()
    elif how == "drone":
        rate = d5["flux_corr"].mean()
    else:
        wt_c = 1.0 / (c5["site_sd_kg_h"] / c5["site_kg_h"]) ** 2
        wt_d = 1.0 / (d5["unc_pct"] / 100.0) ** 2
        rate = (np.sum(c5["site_corr"] * wt_c) + np.sum(d5["flux_corr"] * wt_d)) / (wt_c.sum() + wt_d.sum())
    return float(rate) * 8.76


# ------------------------------------------------------------------ oxidation in the cover
COVER_OF_CELL = {1: "final", 2: "final", 3: "final", 4: "intermediate", 5: "active"}


def ox_fit(F, how="sat"):
    s = F["oxplots"].dropna(subset=["fraction_oxidized"]).copy()
    s = s[s["fraction_oxidized"] < 0.995]
    s["J"] = s["surface_flux_g_m2_d"] / (1 - s["fraction_oxidized"])
    covers = ["final", "intermediate", "active"]
    if how == "mean":
        means = s.groupby("cover")["fraction_oxidized"].mean().to_dict()
        return dict(kind="mean", means=means)
    if how == "default":
        return dict(kind="default")
    if how == "sat":
        def resid(p):
            q10 = p[0]
            out = []
            for k, cv in enumerate(covers):
                ss = s[s["cover"] == cv]
                V = p[1 + k] * q10 ** ((ss["soil_temp_c"].values - 15) / 10.0)
                out.append(V / (V + ss["J"].values) - ss["fraction_oxidized"].values)
            return np.concatenate(out)
        res = least_squares(resid, x0=[2.0, 20, 15, 10], bounds=([1.0, 0.1, 0.1, 0.1], [4.0, 200, 200, 200]))
        return dict(kind="sat", q10=float(res.x[0]), v15={cv: float(res.x[1 + k]) for k, cv in enumerate(covers)})
    if how == "exp":
        def resid(p):
            q10 = p[0]
            out = []
            for k, cv in enumerate(covers):
                ss = s[s["cover"] == cv]
                lam = p[1 + k] * q10 ** ((ss["soil_temp_c"].values - 15) / 10.0)
                out.append(np.exp(-ss["J"].values / lam) - ss["fraction_oxidized"].values)
            return np.concatenate(out)
        res = least_squares(resid, x0=[2.0, 30, 20, 15], bounds=([1.0, 0.1, 0.1, 0.1], [4.0, 500, 500, 500]))
        return dict(kind="exp", q10=float(res.x[0]), lam={cv: float(res.x[1 + k]) for k, cv in enumerate(covers)})
    if how == "mm":
        def resid(p):
            q10 = p[0]
            out = []
            for k, cv in enumerate(covers):
                ss = s[s["cover"] == cv]
                V = p[1 + 2 * k] * q10 ** ((ss["soil_temp_c"].values - 15) / 10.0)
                Km = p[2 + 2 * k]
                out.append(V / (Km + ss["J"].values) - ss["fraction_oxidized"].values)
            return np.concatenate(out)
        res = least_squares(resid, x0=[2.0, 20, 20, 15, 15, 10, 10],
                            bounds=([1.0] + [0.1] * 6, [4.0] + [500] * 6))
        return dict(kind="mm", q10=float(res.x[0]), v15={cv: float(res.x[1 + 2 * k]) for k, cv in enumerate(covers)},
                    km={cv: float(res.x[2 + 2 * k]) for k, cv in enumerate(covers)})
    if how == "loglin":
        out = {}
        for cv in covers:
            ss = s[s["cover"] == cv]
            f = ss["fraction_oxidized"].clip(0.005, 0.995)
            X = np.c_[np.ones(len(ss)), np.log(ss["J"].values), ss["soil_temp_c"].values]
            beta, *_ = np.linalg.lstsq(X, np.log(f / (1 - f)), rcond=None)
            out[cv] = beta
        return dict(kind="loglin", beta=out)
    raise ValueError(how)


def ox_share(OX, cover, J, T, v_scale=1.0):
    if OX["kind"] == "mean":
        return OX["means"][cover]
    if OX["kind"] == "default":
        return 0.10
    if J <= 0:
        return 0.0
    if OX["kind"] == "sat":
        V = OX["v15"][cover] * v_scale * OX["q10"] ** ((T - 15) / 10.0)
        return V / (V + J)
    if OX["kind"] == "exp":
        lam = OX["lam"][cover] * v_scale * OX["q10"] ** ((T - 15) / 10.0)
        return math.exp(-J / lam)
    if OX["kind"] == "mm":
        V = OX["v15"][cover] * v_scale * OX["q10"] ** ((T - 15) / 10.0)
        return min(0.999, V / (OX["km"][cover] + J))
    b = OX["beta"][cover]
    z = b[0] + b[1] * math.log(J) + b[2] * T
    return 1 / (1 + math.exp(-z))


def back_uncollected(OX, cover, e_month, area, days, T, v_scale=1.0):
    """The uncollected methane (t in the month) that leaves e_month at the surface after the cover's oxidation."""
    if OX["kind"] in ("mean", "default"):
        return e_month / (1 - ox_share(OX, cover, 1.0, T))
    u = e_month
    for _ in range(80):
        J = u * 1e6 / area / days
        u = e_month / (1 - ox_share(OX, cover, J, T, v_scale))
    return u


# ------------------------------------------------------------------ the gas system: collected methane by cell
def scada_monthly(F):
    s = F["scada"].copy()
    ts = pd.to_datetime(s["timestamp_local"])
    s["m"] = [mi(t.year, t.month) for t in ts]
    ch4 = s["flare_ch4_pct"].where(s["flare_ch4_pct"] > 5)
    eng = pd.concat([s["eng1_ch4_pct"], s["eng2_ch4_pct"]], axis=1).mean(axis=1)
    ch4 = ch4.fillna(eng)
    scfm = s["flare_flow_scfm"] * ch4 / 100.0 + s["eng1_fuel_scfm"] * s["eng1_ch4_pct"].fillna(0) / 100.0 \
        + s["eng2_fuel_scfm"] * s["eng2_ch4_pct"].fillna(0) / 100.0
    s["t_ch4"] = scfm * 60.0 * P.KG_PER_SCF / 1000.0
    return s.groupby("m")["t_ch4"].sum()


def collected_by_cell(F):
    """{cell: t per month}: the gas system's methane apportioned by each cell's share of the wells' methane flow."""
    w, _ = well_table(F)
    tot = scada_monthly(F)
    sh = w.groupby(["m", "cell"])["ch4_scfm"].sum().unstack(fill_value=0.0)
    out = {c: pd.Series(0.0, index=tot.index) for c in P.CELLS}
    for m in tot.index:
        if m in sh.index:
            row = sh.loc[m]
            ssum = row.sum()
            for c in (1, 2, 3, 4):
                out[c][m] = tot[m] * row.get(c, 0.0) / ssum if ssum > 0 else 0.0
    return out


# ------------------------------------------------------------------ the run
def normals(wx):
    s = wx["soil_temp_10cm_c"]
    s = s[(s.index.year >= 2016) & (s.index.year <= 2025)]
    return {m: float(s[s.index.month == m].mean()) for m in range(1, 13)}


def month_soil(wx):
    s = wx["soil_temp_10cm_c"].resample("MS").mean()
    return {mi(t.year, t.month): float(v) for t, v in s.items() if not np.isnan(v)}


def run(F, sw=None, cache=None):
    sw = dict(GOLDEN, **(sw or {}))
    cache = cache if cache is not None else {}
    R = {"sw": sw}
    if "wx" not in cache:
        cache["wx"] = weather_lst(F)
    wx = cache["wx"]
    norm = cache.setdefault("norm", normals(wx))
    msoil = cache.setdefault("msoil", month_soil(wx))
    area = {int(r_["cell"]): float(r_["footprint_acres"]) * 4046.86 for _, r_ in F["cells"].iterrows()}

    # R1
    R["R1"] = r1_cell5_msw(F, sw["tickets"])

    # the barometric correction and the campaigns
    key = "B_" + sw["baro"]
    if sw["baro"] != "none" and key not in cache:
        cache[key] = baro_fit(F, sw["baro"], wx)
    B = cache.get(key)
    c, d = corrected_rates(F, sw, B)
    R["campaigns"], R["drone"] = c, d
    R["baro"] = None if B is None else dict(tau=B["tau"], c=B["c"])
    R["R2"] = actual_2025(c, d, sw["level"])
    R["survey_2025"] = float(c[pd.to_datetime(c["date"]).dt.year == 2025]["site_kg_h"].mean() * 8.76)

    # the decay: the dry rate from the closed cells, the faster rate from cell 4's pumped wells
    if "kd" not in cache:
        cache["kd"] = kd_closed(F)
    kd = P.RULE["k_default"] if sw["kd_scale"] == "rule" else cache["kd"] * sw["kd_scale"]
    if "z4" not in cache:
        cache["z4"] = cell4_zones(F, sw)
    Z = cache["z4"]
    pk = "pot_" + sw["tickets"]
    if pk not in cache:
        cache[pk] = waste_potential(F, sw["tickets"])
    pot = cache[pk]
    share = Z["share_wet"]
    # the pumped wells still hold a little liquid over their screens: their ratio is read at full yield
    if "pilot" not in cache:
        cache["pilot"] = pilot_yield(Z)
    L, s_after = cache["pilot"]
    r_wet = Z["r_pump"] / (1 - L * s_after)
    R["r_wet"], R["r_dry"] = r_wet, Z["r_dry"]
    R["z"] = dict(n_wells=len(Z["ids"]), n_dry=len(Z["dry"]), n_wet=len(Z["wet"]), n_pumped=len(Z["pumped"]),
                  n_dry_read=Z["n_dry"], n_pumped_read=Z["n_pump"], r_dry=Z["r_dry"], r_pump=Z["r_pump"],
                  r_wet=r_wet, r_collected=Z["r_collected"], L=L, s_after=s_after)
    if "rec" not in cache:
        cache["rec"] = recirc_months(F)
    rec4, rec5 = cache["rec"][4], cache["rec"][5]
    if sw["kwet"]:
        kw = fit_kw(pot[4], kd, share, r_wet, ramp=sw["ramp"], rec=rec4) * sw["kw_scale"]
    else:
        kw = kd
    R["kd"], R["kw"], R["share_wet"] = kd, kw, share
    if sw["r3"] == "zones":
        R["R3"] = 100.0 * ((1 - share) * Z["r_dry"] + share * r_wet - 1)
    elif sw["r3"] == "collected":
        R["R3"] = 100.0 * (Z["r_collected"] - 1)
    elif sw["r3"] == "dry":
        R["R3"] = 100.0 * (Z["r_dry"] - 1)
    else:
        R["R3"] = 100.0 * (r_wet - 1)

    g4, g4w = fod(pot[4], kd, kw, share, rec4 if sw["kwet"] else None, ramp=sw["ramp"])
    g5, _ = fod(pot[5], kd, kw, 1.0, rec5 if sw["kwet"] else None, ramp=sw["ramp"])
    gc = {cc: fod(pot[cc], kd, kd, 0.0, None)[0] for cc in (1, 2, 3)}
    model = {1: gc[1], 2: gc[2], 3: gc[3], 4: g4, 5: g5}   # m3 per month at the rule's potential

    # oxidation
    ok = "OX_" + sw["ox"]
    if ok not in cache:
        cache[ok] = ox_fit(F, sw["ox"])
    OX = cache[ok]
    vs = sw["v_scale"]

    # collected methane by cell
    if "coll" not in cache:
        cache["coll"] = collected_by_cell(F)
    coll = cache["coll"]

    # cell 4 and cell 5 in February to July 2026, from the two-tracer campaigns
    c26 = c[pd.to_datetime(c["date"]).dt.year == 2026]
    months26 = [mi(x.year, x.month) for x in c26["date"]]
    u4_obs, g4_obs, u5_obs = [], [], []
    for (_, r), m in zip(c26.iterrows(), months26):
        T = msoil.get(m, norm[mo(m)[1]])
        e4 = r["cell4_corr"] * 24 * dim(m) / 1000.0     # t in the month at the campaign's rate
        e5 = r["cell5_corr"] * 24 * dim(m) / 1000.0
        u4 = back_uncollected(OX, "intermediate", e4, area[4], dim(m), T, vs)
        u5 = back_uncollected(OX, "active", e5, area[5], dim(m), T, vs)
        u4_obs.append(u4)
        g4_obs.append(u4 + coll[4].get(m, 0.0))
        u5_obs.append(u5)
    s4 = float(np.sum(g4_obs) / np.sum([model[4][m] for m in months26]))
    if sw["c5"] == "anchor":
        # every two-tracer campaign came before cell 5's recirculation began, so it calibrates the dry decay
        g5dry, _ = fod(pot[5], kd, kd, 0.0, None)
        s5 = float(np.sum(u5_obs) / np.sum([g5dry[m] for m in months26])) * sw["s5_scale"]
    else:
        s5 = s4 * sw["s5_scale"]
    if sw.get("calib") == "rule":
        # no calibration: the rule's methane potential at the rule's density, every cell
        s4 = s5 = P.RHO_CH4
    elif sw.get("calib") == "closed":
        # the level from the closed cells: their collected gas at the closure plan's design collection over the
        # twelve months to October 2026, against the decay model of their own waste
        yr = range(mi(2025, 11), mi(2026, 11))
        num = sum(coll[cc].get(m, 0.0) for cc in (1, 2, 3) for m in yr) / P.CE_CLOSED_DESIGN
        den = sum(model[cc][m] for cc in (1, 2, 3) for m in yr)
        s4 = s5 = float(num / den)
    scale = {1: s4, 2: s4, 3: s4, 4: s4, 5: s5}
    G = {cc: model[cc] * scale[cc] for cc in P.CELLS}         # t per month
    R["s4"], R["s5"] = s4, s5
    R["G"], R["OX"], R["norm"] = G, OX, norm

    # R4: cell 5's 2027 methane generation
    y27 = slice(mi(2027, 1), mi(2028, 1))
    R["R4"] = float(G[5][y27].sum())

    # collection efficiencies for 2027
    last = [mi(2026, 8), mi(2026, 9), mi(2026, 10)]
    ce = {cc: float(np.sum([coll[cc].get(m, 0.0) for m in last]) / np.sum([G[cc][m] for m in last])) for cc in (1, 2, 3, 4)}
    R["ce4_now"] = ce[4]
    # cell 4 by zone: the wells the leachate never reached collect from the unreached waste, the others from the
    # reached waste; each zone's collection efficiency over August to October 2026, carried with its own generation
    G4w = g4w * scale[4]
    G4d = G[4] - G4w
    w4 = Z["w"][Z["w"]["cell"] == 4]
    wetset = set(Z["wet"])
    fl = w4.assign(z=w4["well_id"].isin(wetset)).groupby(["m", "z"])["ch4_scfm"].sum().unstack(fill_value=0.0)
    cw, cd = 0.0, 0.0
    for m in last:
        tw = float(fl.loc[m].get(True, 0.0)) if m in fl.index else 0.0
        td = float(fl.loc[m].get(False, 0.0)) if m in fl.index else 0.0
        fr = tw / (tw + td) if (tw + td) > 0 else share
        cw += coll[4].get(m, 0.0) * fr
        cd += coll[4].get(m, 0.0) * (1 - fr)
    ce4_wet = cw / float(np.sum([G4w[m] for m in last])) if np.sum([G4w[m] for m in last]) > 0 else ce[4]
    ce4_dry = cd / float(np.sum([G4d[m] for m in last]))
    R["ce4_zones"] = dict(dry=ce4_dry, wet=ce4_wet)
    closed_col = {cc: float(np.mean([coll[cc].get(m, 0.0) for m in range(mi(2025, 11), mi(2026, 11))]))
                  for cc in (1, 2, 3)}

    # package C's pumps: the pilot's yield model on the wells still flooded
    gain = pump_gain(F, Z, sw["pumps"]) * sw["gain_scale"]           # t per month at the October 2026 rate
    R["pump_gain_t_month"] = gain

    def cell5_ce(pkgc, m):
        works = P.PACKAGES[pkgc]["works"]
        v = 0.0
        if "hc5" in works and m >= mi(P.WORKS["hc5"].year, P.WORKS["hc5"].month):
            v = P.CE5_HC
        if "wells5" in works and m >= mi(P.WORKS["wells5"].year, P.WORKS["wells5"].month):
            v = P.CE5_WELLS
        return v

    R7, detail = {}, {}
    for pkgc in P.PACKAGES:
        works = P.PACKAGES[pkgc]["works"]
        tot, coll27 = 0.0, 0.0
        per = {cc: 0.0 for cc in P.CELLS}
        for m in range(mi(2027, 1), mi(2028, 1)):
            T = norm[mo(m)[1]]
            for cc in P.CELLS:
                g = G[cc][m]
                if cc in (1, 2, 3):
                    # the closed cells: their own collected gas carried on the dry decline, at the closure plan's
                    # design collection
                    col = closed_col[cc] * math.exp(-kd * (m - mi(2026, 4)) / 12.0)
                    g = col / P.CE_CLOSED_DESIGN
                elif cc == 4:
                    if sw["ce4"] == "zones" and sw["kwet"]:
                        col = ce4_dry * G4d[m] + ce4_wet * G4w[m]
                        scale_g = G4w[m] / G4w[mi(2026, 10)] if G4w[mi(2026, 10)] > 0 else g / G[4][mi(2026, 10)]
                    else:
                        col = ce[4] * g
                        scale_g = g / G[4][mi(2026, 10)]
                    if "pumps4" in works and m >= mi(P.WORKS["pumps4"].year, P.WORKS["pumps4"].month):
                        col += gain * scale_g
                    if "cap4" in works and m >= mi(P.WORKS["cap4"].year, P.WORKS["cap4"].month):
                        col = max(col, P.CE4_CAP * g)
                else:
                    col = cell5_ce(pkgc, m) * g
                u = max(0.0, g - col)
                J = u * 1e6 / area[cc] / dim(m)
                f = ox_share(OX, COVER_OF_CELL[cc], J, T, vs)
                per[cc] += u * (1 - f)
                coll27 += col
        tot = sum(per.values()) + coll27 * (1 - P.RULE["de"])
        R7[pkgc] = tot
        detail[pkgc] = per
    R["R7"], R["R7_cells"] = R7, detail
    R["R7_slip"] = {pk: R7[pk] - sum(detail[pk].values()) for pk in P.PACKAGES}
    # R5: the share of the methane reaching cell 5's cover in 2027 that it oxidizes, under package A
    ux, ox_ = 0.0, 0.0
    for m in range(mi(2027, 1), mi(2028, 1)):
        u = G[5][m]
        J = u * 1e6 / area[5] / dim(m)
        f = ox_share(OX, "active", J, norm[mo(m)[1]], vs)
        ux += u
        ox_ += u * f
    R["R5"] = 100.0 * ox_ / ux
    R["R8"] = next((pkgc for pkgc in P.PACKAGES if R7[pkgc] <= P.LIMIT_T), "none") if P.LIMIT_T else None

    # R6: the 2025 bridge, by cell, in the reporting rule's order: collection, then oxidation, then the rest
    y25 = range(mi(2025, 1), mi(2026, 1))
    Rcol = float(scada_monthly(F)[[m for m in y25]].sum())
    U, E2 = 0.0, 0.0
    for m in y25:
        T = msoil.get(m, norm[mo(m)[1]])
        for cc in P.CELLS:
            g = G[cc][m]
            col = coll[cc].get(m, 0.0) if cc != 5 else 0.0
            if cc in (1, 2, 3):
                g = col / P.CE_CLOSED_DESIGN
            u = max(0.0, g - col)
            J = u * 1e6 / area[cc] / dim(m)
            f = ox_share(OX, COVER_OF_CELL[cc], J, T, vs)
            U += u
            E2 += u * (1 - f)
    rep = report_2025(F, Rcol)
    E1 = U * (1 - P.RULE["ox"]) + Rcol * (1 - P.RULE["de"])
    E2 += Rcol * (1 - P.RULE["de"])
    R["R6"] = dict(report=rep, collection=E1 - rep, oxidation=E2 - E1, residual=R["R2"] - E2,
                   survey=R["survey_2025"], survey_gap=R["R2"] - R["survey_2025"], collected_2025=Rcol,
                   generated_2025=U + Rcol)
    return R


def report_2025(F, Rcol):
    """The reporting rule's collection-based emission for 2025, as the division's report files it."""
    A = P.RULE_AREAS_2025
    ce = sum(a * P.RULE["ce"][k] for k, a in A.items()) / sum(A.values())
    gen = Rcol / ce
    return (gen - Rcol) * (1 - P.RULE["ox"]) + Rcol * (1 - P.RULE["de"])


def pilot_yield(Z):
    """The yield lost per unit of submerged screen, L, and the submergence the pumps hold, from the pilot wells."""
    w = Z["w"]
    Ls, sq_all = [], []
    for wid in Z["pumped"]:
        ww = w[w["well_id"] == wid]
        a = ww[(ww["m"] >= mi(2025, 1)) & (ww["m"] < mi(2025, 6))]["ch4_scfm"].mean()
        b = ww[(ww["m"] >= mi(2025, 7)) & (ww["m"] < mi(2025, 11))]["ch4_scfm"].mean()
        s_pre = ww[(ww["m"] >= mi(2025, 1)) & (ww["m"] < mi(2025, 6))]["sub"].dropna()
        s_post = ww[(ww["m"] >= mi(2025, 7))]["sub"].dropna()
        if np.isnan(a) or np.isnan(b) or s_pre.empty:
            continue
        rr = b / a
        sp, sq = float(s_pre.iloc[-1]), (float(s_post.mean()) if not s_post.empty else 0.0)
        sq_all.append(sq)
        if rr * sp - sq > 0:
            Ls.append(min(0.98, max(0.3, (rr - 1) / (rr * sp - sq))))
    return (float(np.mean(Ls)) if Ls else 0.85), (float(np.mean(sq_all)) if sq_all else 0.0)


def pump_gain(F, Z, how="yield"):
    """Methane (t per month, at the October 2026 rate) that pumps in cell 4's flooded wells add, read off the
    June 2025 pilot."""
    w = Z["w"]
    pre = (mi(2025, 1), mi(2025, 6))
    post = (mi(2025, 7), mi(2025, 11))
    ratios, Ls = [], []
    for wid in Z["pumped"]:
        ww = w[w["well_id"] == wid]
        a = ww[(ww["m"] >= pre[0]) & (ww["m"] < pre[1])]["ch4_scfm"].mean()
        b = ww[(ww["m"] >= post[0]) & (ww["m"] < post[1])]["ch4_scfm"].mean()
        s_pre = ww[(ww["m"] >= mi(2025, 1)) & (ww["m"] < mi(2025, 6))]["sub"].dropna()
        s_post = ww[(ww["m"] >= mi(2025, 7))]["sub"].dropna()
        if np.isnan(a) or np.isnan(b) or s_pre.empty:
            continue
        rr = b / a
        ratios.append(rr)
        sp, sq = float(s_pre.iloc[-1]), float(s_post.mean()) if not s_post.empty else 0.0
        # rr = (1 - L sq) / (1 - L sp)  ->  L
        L = (rr - 1) / (rr * sp - sq) if (rr * sp - sq) > 0 else 0.85
        Ls.append(min(0.98, max(0.3, L)))
    L = float(np.mean(Ls)) if Ls else 0.85
    rho = float(np.mean(ratios)) if ratios else 1.0
    s_after = 0.04
    flooded = [x for x in Z["wet"] if x not in Z["pumped"]]
    last = w[(w["m"] >= mi(2026, 7)) & (w["m"] < mi(2026, 11))]
    flows = last.groupby("well_id")["ch4_scfm"].mean()
    subs = w[w["m"] == mi(2026, 10)].set_index("well_id")["sub"]
    g = 0.0
    for wid in flooded:
        if wid not in flows.index:
            continue
        s = float(subs.get(wid, np.nan)) if wid in subs.index else np.nan
        if np.isnan(s) or s < 0.02:
            continue
        if how == "yield":
            g += flows[wid] * ((1 - L * s_after) / (1 - L * s) - 1)
        else:
            g += flows[wid] * (rho - 1)
    # scfm of methane to t per month, scaled from the wells' instantaneous readings to the gas system's total
    return g * 60 * 24 * 30.44 * P.KG_PER_SCF / 1000.0
