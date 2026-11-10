"""task3: every graded figure from the cut pack alone (no world state): the harbor's expected tidal flood days in
the 2027-28 tide year, its range and its bridge from 2025-26, each low point's flooding level and transfer from its
own record, each low point's 2025-26 and expected 2027-28 tidal flood days, the funded pair, and the shortcuts."""
import csv
import os
import re

import numpy as np
import pandas as pd

F_HOURLY = "8673718_hourly_heights_2000-2026.csv"
F_HL = "8673718_high_low_1955-2026.csv"
F_HLP = "8673718_high_low_predictions_1955-2028.csv"
F_MONTHLY = "8673718_monthly_means_1955-2026.csv"
F_DATUMS = "8673718_datums.txt"
F_RIVER = "usgs_02203560_brayle_r_hensley_daily.txt"
F_LOG = {"marsh": "PEL-MR-24.csv", "oyster": "OYS-CR-25.csv", "river": "HEN-RR-25.csv"}
F_SENSOR = "pt-front-01_2024-05-14_2026-10-31.csv"
F_RAIN = "ghcnd_USW00003817_2023-2026.csv"
F_311 = "311_service_requests_2023-2026.csv"
F_SLR = "slr_scenarios_8673718.csv"
F_INV = "tidal_low_points_inventory_2026-10.xlsx"
F_GUIDE = "fy2028_tide_valve_round_guidelines.pdf"

PLAN = 0.70
HARBOR_MINOR = 8.6
WX_YEARS = list(range(1990, 2026))  # tide years 1990-91 to 2025-26
SITE_IDS = {"front": "LP-01", "marsh": "LP-02", "river": "LP-03", "wharf": "LP-04", "oyster": "LP-05"}
NAMES = {"front": "Front Street at Ferry Lane", "marsh": "Marsh Road at Pellam Creek", "river": "River Road at Hensley Landing",
         "wharf": "Wharf Street at Market Lane", "oyster": "Oyster Creek Road"}
ORDER = ["front", "marsh", "river", "wharf", "oyster"]


# ---------------------------------------------------------------- reading the pack
def _p(tgt, f):
    return os.path.join(tgt, f)


def read_hilo(tgt, f):
    d = pd.read_csv(_p(tgt, f), skipinitialspace=True)
    d.columns = [c.strip() for c in d.columns]
    d["t"] = pd.to_datetime(d["Date Time"])
    col = "Water Level" if "Water Level" in d.columns else "Prediction"
    d["h"] = d[col].astype(float)
    d["hi"] = d["Type"].str.strip().str.startswith("H")
    return d[["t", "h", "hi", "Type"]]


def read_monthly(tgt):
    d = pd.read_csv(_p(tgt, F_MONTHLY), skipinitialspace=True)
    d.columns = [c.strip() for c in d.columns]
    d["m"] = pd.to_datetime(dict(year=d.Year, month=d.Month, day=1))
    return d.set_index("m")["MSL"].astype(float)


def read_hourly(tgt):
    d = pd.read_csv(_p(tgt, F_HOURLY))
    d["t"] = pd.to_datetime(d["Date"] + " " + d["Time (LST)"], format="%Y/%m/%d %H:%M")
    return d.set_index("t")


def read_datums(tgt):
    out = {}
    for line in open(_p(tgt, F_DATUMS)):
        m = re.match(r"^(MHHW|MHW|MTL|MSL|DTL|MLW|MLLW|NAVD88)\s+(-?\d+\.\d+)", line)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


def read_river(tgt):
    rows = [r for r in csv.reader(open(_p(tgt, F_RIVER)), delimiter="\t") if r and not r[0].startswith("#")]
    hdr, body = rows[0], rows[2:]
    d = pd.DataFrame(body, columns=hdr)
    q = pd.Series(d.iloc[:, 3].astype(float).values, index=pd.to_datetime(d.datetime))
    return q


def read_logger(tgt, site):
    path = _p(tgt, F_LOG[site])
    with open(path, encoding="utf-8") as f:
        f.readline()
        hdr = next(csv.reader([f.readline()]))
        off = int(re.search(r"GMT([+-]\d+):00", hdr[1]).group(1))
        rows = list(csv.reader(f))
    t = pd.to_datetime([r[1] for r in rows], format="%m/%d/%y %I:%M:%S %p")
    lev = np.array([float(r[2]) for r in rows])
    t_lst = t - pd.Timedelta(hours=off) - pd.Timedelta(hours=5)  # to UT, then to local standard time
    return pd.Series(lev, index=t_lst)


def read_sensor(tgt):
    d = pd.read_csv(_p(tgt, F_SENSOR))
    d["t"] = pd.to_datetime(d.timestamp_utc.str.replace("Z", "")) - pd.Timedelta(hours=5)
    return d.set_index("t")


def read_inventory(tgt):
    from openpyxl import load_workbook
    wb = load_workbook(_p(tgt, F_INV), data_only=True)
    ws = wb["Low points"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    out = {}
    for r in rows[1:]:
        rec = dict(zip(hdr, r))
        key = [k for k, v in SITE_IDS.items() if v == rec["LP ID"]][0]
        out[key] = dict(rim=rec["Lowest inlet rim (ft NAVD88)"], lane=rec["Travel lane low point (ft NAVD88)"])
    return out


# ---------------------------------------------------------------- the harbor
def tide_year(t):
    t = pd.DatetimeIndex(t)
    return np.where(t.month >= 5, t.year, t.year - 1)


class Harbor:
    def __init__(self, tgt):
        self.dat = read_datums(tgt)
        self.nav = self.dat["NAVD88"]  # NAVD88 above MLLW
        hl = read_hilo(tgt, F_HL)
        hp = read_hilo(tgt, F_HLP)
        self.hw = hl[hl.hi].set_index("t").h
        self.hwp = hp[hp.hi].set_index("t").h
        self.monthly = read_monthly(tgt)
        hr = read_hourly(tgt)
        pm = hr["Predicted (ft)"].groupby(hr.index.month).mean()
        self.seas = pm - hr["Predicted (ft)"].mean()
        self.z0 = self.dat["MSL"]
        months = self.monthly.index
        a = self.monthly - (self.z0 + self.seas.reindex(months.month).values)
        self.anom = a
        ty = tide_year(months)
        A = a.groupby(ty).agg(["mean", "count"])
        self.A = A["mean"]
        self.A_count = A["count"]
        self._pair()

    def _pair(self):
        o, p = self.hw, self.hwp
        tp = p.index.values.astype("datetime64[s]").astype(np.int64)
        to = o.index.values.astype("datetime64[s]").astype(np.int64)
        j = np.clip(np.searchsorted(tp, to), 1, len(tp) - 1)
        jl = np.where(np.abs(tp[j - 1] - to) < np.abs(tp[j] - to), j - 1, j)
        ok = np.abs(tp[jl] - to) <= 3 * 3600
        d = pd.DataFrame({"obs": o.values[ok], "pred": p.values[jl[ok]], "tp": p.index[jl[ok]]}, index=o.index[ok])
        d["sk"] = d.obs - d.pred
        d["ty"] = tide_year(d.index)
        d["A"] = self.A.reindex(d.ty).values
        d["r"] = d["sk"] - d["A"]
        d["mon"] = d.index.to_period("M").to_timestamp()
        d["a_m"] = self.anom.reindex(d.mon).values
        d["r_month"] = d["sk"] - d["a_m"]
        self.pairs = d

    def residual_series(self, y, col="r"):
        d = self.pairs[self.pairs.ty == y]
        tau = (d.tp - pd.Timestamp("%d-05-01" % y)).dt.total_seconds().values / 3600.0
        return tau, d[col].values, d.index

    def year_hw(self, y, which="pred"):
        s = self.hwp if which == "pred" else self.hw
        a, b = pd.Timestamp("%d-05-01" % y), pd.Timestamp("%d-05-01" % (y + 1))
        return s[(s.index >= a) & (s.index < b)]

    def month_anom_series(self, y):
        """Each month of weather year y: its anomaly less the year's mean (the month-to-month weather and ocean
        departures the tide year's mean does not carry)."""
        months = pd.date_range("%d-05-01" % y, periods=12, freq="MS")
        a = self.anom.reindex(months)
        return (a - self.A.get(y, np.nan)).fillna(0.0).values


def count_days(times, levels, thr):
    t = pd.DatetimeIndex(times)
    hit = pd.Series(levels >= thr, index=t.floor("D")).groupby(level=0).any()
    return int(hit.sum())


# ---------------------------------------------------------------- site transfers
def hilo_series(s, smooth=3):
    v = s.values
    vs = np.convolve(v, np.ones(smooth) / smooth, mode="same")
    d = np.diff(vs)
    hi = np.where((d[:-1] > 0) & (d[1:] <= 0))[0] + 1
    keep = []
    for i in hi:
        a, b = max(0, i - 2), min(len(v), i + 3)
        keep.append(a + int(np.argmax(v[a:b])))
    keep = sorted(set(keep))
    out = s.iloc[keep]
    # one high per 8 hours at most (a semidiurnal creek)
    sel = []
    for t, h in out.items():
        if sel and (t - sel[-1][0]) < pd.Timedelta(hours=8):
            if h > sel[-1][1]:
                sel[-1] = (t, h)
            continue
        sel.append((t, h))
    return pd.Series([h for _, h in sel], index=[t for t, _ in sel])


def pair_site(H, site_hw, nav, monthly, Q=None):
    hw = H.hw
    th = hw.index.values.astype("datetime64[s]").astype(np.int64)
    ts = site_hw.index.values.astype("datetime64[s]").astype(np.int64)
    j = np.clip(np.searchsorted(th, ts), 1, len(th) - 1)
    jl = np.where(np.abs(th[j - 1] - ts) < np.abs(th[j] - ts), j - 1, j)
    ok = np.abs(th[jl] - ts) <= 3 * 3600
    d = pd.DataFrame({"site": site_hw.values[ok] + nav, "harbor": hw.values[jl[ok]]}, index=site_hw.index[ok])
    d["M"] = monthly.reindex(d.index.to_period("M").to_timestamp()).values
    if Q is not None:
        d["Q"] = Q.reindex(d.index.floor("D")).values
    return d


def fit_hinge(d, grid=np.arange(6.6, 8.6, 0.01)):
    best = None
    for P in grid:
        X = np.column_stack([np.ones(len(d)), d.harbor.values, np.maximum(d.harbor.values - P, 0.0)])
        co, *_ = np.linalg.lstsq(X, d.site.values, rcond=None)
        sse = float(((X @ co - d.site.values) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, P, co)
    sse, P, co = best
    return dict(P=float(P), a=float(co[0]), b1=float(co[1]), b2=float(co[2]), sse=sse, n=len(d))


def hinge_level(f, H):
    return f["a"] + f["b1"] * H + f["b2"] * np.maximum(H - f["P"], 0.0)


def hinge_inverse(f, L):
    Hs = np.arange(5.0, 12.0, 0.0005)
    v = hinge_level(f, Hs)
    i = np.argmax(v >= L)
    return float(Hs[i])


def fit_linear(d):
    c = np.polyfit(d.harbor.values, d.site.values, 1)
    return dict(b=float(c[0]), a=float(c[1]))


def linear_inverse(f, L):
    return (L - f["a"]) / f["b"]


def fit_river(d, form="lin"):
    g = {"lin": d.Q.values / 1e4, "log": np.log(d.Q.values / 1e4), "pow": (d.Q.values / 1e4) ** 0.85}[form]
    X = np.column_stack([np.ones(len(d)), g, d.harbor.values - d.M.values])
    co, *_ = np.linalg.lstsq(X, d.site.values - d.M.values, rcond=None)
    res = d.site.values - d.M.values - X @ co
    return dict(form=form, c0=float(co[0]), c1=float(co[1]), r=float(co[2]), sse=float((res ** 2).sum()), n=len(d))


def river_level(f, H, M, Q):
    g = {"lin": Q / 1e4, "log": np.log(Q / 1e4), "pow": (Q / 1e4) ** 0.85}[f["form"]]
    return M + f["c0"] + f["c1"] * g + f["r"] * (H - M)


def fit_pooled(d):
    X = np.column_stack([np.ones(len(d)), d.harbor.values - d.M.values])
    co, *_ = np.linalg.lstsq(X, d.site.values - d.M.values, rcond=None)
    return dict(c0=float(co[0]), r=float(co[1]))


def front_level(H, sen):
    """Front Street's flooding elevation (as a harbor high water): the harbor high water less the water depth the
    sensor recorded on the lane at that high tide, over the high tides that put water on the lane."""
    # a vehicle under the beam reads as one deep sample; water on the lane persists for many readings
    dep = sen.depth_in.rolling(5, center=True, min_periods=3).median()
    hw = H.hw[(H.hw.index >= sen.index[0]) & (H.hw.index <= sen.index[-1])]
    rows = []
    for t, h in hw.items():
        w = dep[(dep.index >= t - pd.Timedelta(hours=2)) & (dep.index <= t + pd.Timedelta(hours=2))]
        if len(w) < 30:
            continue
        rows.append((t, h, float(w.max())))
    d = pd.DataFrame(rows, columns=["t", "h", "dmax"]).set_index("t")
    wet = d[d.dmax >= 0.5]
    est = wet.h - wet.dmax / 12.0
    return float(np.median(est)), d, int(len(wet))


def front_sensor_days(H, sen, LA, y):
    """Front Street's tidal flood days in tide year y that the sensor itself recorded: water on the lane within two
    hours of a harbor high water at or above the lane (rain ponding at a lower tide is not tidal)."""
    dep = sen.depth_in.rolling(5, center=True, min_periods=3).median()
    hw = H.year_hw(y, "obs")
    days = set()
    for t, h in hw.items():
        if h < LA:
            continue
        w = dep[(dep.index >= t - pd.Timedelta(hours=2)) & (dep.index <= t + pd.Timedelta(hours=2))]
        if len(w) >= 30 and w.max() >= 0.5:
            days.add(t.floor("D"))
    return len(days)


# ---------------------------------------------------------------- the forecast machinery
class Ensemble:
    """The tide year's high waters at the harbor in each weather year: the year's predicted high waters, the planning
    mean sea level and that weather year's residuals at high water (its high waters less its predictions less its
    tide year's mean anomaly), with its month-to-month departures and its river flows alongside."""

    def __init__(self, H, Q, ty=2027, plan=PLAN, years=WX_YEARS, tides=None, sea=None, resid_col="r", align="interp"):
        self.H = H
        pred = H.year_hw(ty if tides is None else tides)
        self.t = pred.index
        self.p = pred.values
        self.tau = (self.t - pd.Timestamp("%d-05-01" % (ty if tides is None else tides))).total_seconds().values / 3600.0
        self.plan = plan if sea is None else sea
        self.years = list(years)
        self.levels, self.M, self.Q = {}, {}, {}
        mo = ((self.t.year - (ty if tides is None else tides)) * 12 + self.t.month - 5).values
        self.month_idx = mo
        for y in self.years:
            tau_y, r, _ = H.residual_series(y, resid_col)
            if align == "interp":
                rr = np.interp(self.tau, tau_y, r)
            elif align == "nearest":
                j = np.clip(np.searchsorted(tau_y, self.tau), 1, len(tau_y) - 1)
                rr = np.where(np.abs(tau_y[j - 1] - self.tau) < np.abs(tau_y[j] - self.tau), r[j - 1], r[j])
            else:  # the day's largest residual on every high water that day
                dy = np.floor(tau_y / 24.0)
                dmax = pd.Series(r).groupby(dy).max()
                rr = dmax.reindex(np.floor(self.tau / 24.0)).ffill().bfill().values
            self.levels[y] = self.p + self.plan + rr
            mdep = H.month_anom_series(y)
            self.M[y] = H.z0 + H.seas.reindex(self.t.month).values + self.plan + mdep[np.clip(mo, 0, 11)]
            qd = pd.Timestamp("%d-05-01" % y) + pd.to_timedelta(np.floor(self.tau / 24.0), unit="D")
            self.Q[y] = Q.reindex(qd).values

    def counts(self, site_fn):
        return np.array([count_days(self.t, site_fn(self.levels[y], self.M[y], self.Q[y]), 0.0) for y in self.years])


def summary(c):
    return dict(mean=float(np.mean(c)), lo=float(np.percentile(c, 5)), hi=float(np.percentile(c, 95)), counts=[int(x) for x in c])


# ---------------------------------------------------------------- the run
def run(tgt):
    H = Harbor(tgt)
    Q = read_river(tgt)
    inv = read_inventory(tgt)
    nav = H.nav
    lane = {k: (v["lane"] + nav if v["lane"] is not None else None) for k, v in inv.items()}
    rim = {k: v["rim"] + nav for k, v in inv.items()}
    sen = read_sensor(tgt)
    out = dict(datums=H.dat, nav=nav)

    # Front Street: its flooding elevation from the sensor
    LA, fr, n_wet = front_level(H, sen)
    out["front_level"] = LA
    out["front_level_navd88"] = LA - nav
    out["front_wet_tides"] = n_wet
    lane["front"] = LA

    # marsh creeks: the overmarsh transfer from each campaign
    fits = {}
    for site in ("marsh", "oyster"):
        s = read_logger(tgt, site)
        d = pair_site(H, hilo_series(s), nav, H.monthly)
        fh, fl = fit_hinge(d), fit_linear(d)
        res_l = d.site - (fl["a"] + fl["b"] * d.harbor)
        res_h = d.site - hinge_level(fh, d.harbor)
        top = d.harbor >= 8.3
        fits[site] = dict(pairs=d, hinge=fh, linear=fl, Hstar=hinge_inverse(fh, lane[site]),
                          Hlin=linear_inverse(fl, lane[site]), above=int((d.harbor > fh["P"]).sum()),
                          top_n=int(top.sum()), top_below_line=int((res_l[top] < 0).sum()),
                          top_resid=float(res_l[top].mean()), sd_line=float(res_l.std()), sd_hinge=float(res_h.std()))
    # River Road: the flow-dependent transfer from its campaign
    s = read_logger(tgt, "river")
    dR = pair_site(H, hilo_series(s), nav, H.monthly, Q)
    rf = {form: fit_river(dR, form) for form in ("lin", "log", "pow")}
    best_form = min(rf, key=lambda k: rf[k]["sse"])
    pooled = fit_pooled(dR)
    out["river_fit"] = rf
    out["river_form"] = best_form
    out["river_pooled"] = pooled
    out["river_campaign_q"] = (float(dR.Q.min()), float(dR.Q.max()), float(dR.Q.mean()))
    out["fits"] = {k: dict(hinge=v["hinge"], linear=v["linear"], Hstar=v["Hstar"], Hlin=v["Hlin"], above=v["above"],
                           n=len(v["pairs"]), top_n=v["top_n"], top_below_line=v["top_below_line"], top_resid=v["top_resid"],
                           sd_line=v["sd_line"], sd_hinge=v["sd_hinge"]) for k, v in fits.items()}

    def site_fn(site, variant="golden"):
        if site in ("front", "wharf"):
            L = lane[site] if not (site == "front" and variant == "rim") else rim["front"]
            return lambda Hh, M, Qq: Hh - L
        if site in ("marsh", "oyster"):
            L = fits[site]["Hstar"] if variant == "golden" else (fits[site]["Hlin"] if variant == "linear" else lane[site])
            return lambda Hh, M, Qq: Hh - L
        if site == "river":
            if variant == "golden":
                f = rf[best_form]
                return lambda Hh, M, Qq: river_level(f, Hh, M, Qq) - lane["river"]
            if variant in ("lin", "log", "pow"):
                f = rf[variant]
                return lambda Hh, M, Qq: river_level(f, Hh, M, Qq) - lane["river"]
            if variant == "pooled":
                return lambda Hh, M, Qq: M + pooled["c0"] + pooled["r"] * (Hh - M) - lane["river"]
            return lambda Hh, M, Qq: Hh - lane["river"]  # no transfer
        raise ValueError(site)

    # 2025-26: each low point's tidal flood days on the observed record
    y0 = 2025
    hw25 = H.year_hw(y0, "obs")
    M25 = H.monthly.reindex(hw25.index.to_period("M").to_timestamp()).values
    Q25 = Q.reindex(hw25.index.floor("D")).values
    hind = {}
    for site in ORDER:
        hind[site] = count_days(hw25.index, site_fn(site)(hw25.values, M25, Q25), 0.0)
    hind["front_sensor_only"] = front_sensor_days(H, sen, LA, 2025)
    hind["front_outage_days"] = hind["front"] - hind["front_sensor_only"]
    out["hind"] = hind
    out["harbor_obs"] = {int(y): count_days(H.year_hw(y, "obs").index, H.year_hw(y, "obs").values, HARBOR_MINOR)
                         for y in range(1990, 2026)}

    # 2027-28 expected days
    E = Ensemble(H, Q)
    exp = {}
    for site in ORDER:
        exp[site] = summary(E.counts(site_fn(site)))
    exp["harbor"] = summary(E.counts(lambda Hh, M, Qq: Hh - HARBOR_MINOR))
    out["exp"] = exp
    rank = sorted(ORDER, key=lambda k: -exp[k]["mean"])
    out["rank"] = rank
    out["funded"] = rank[:2]

    # the harbor bridge, 2025-26 observed to 2027-28 expected: sea level, tides, weather (Shapley over the six orders)
    A25 = float(H.A.loc[2025])
    out["A25"] = A25

    def f_br(sea, tides, wx):
        e = Ensemble(H, Q, ty=2027 if tides == "27" else 2025, plan=(PLAN if sea == "plan" else A25),
                     years=(WX_YEARS if wx == "clim" else [2025]))
        return float(np.mean(e.counts(lambda Hh, M, Qq: Hh - HARBOR_MINOR)))

    import itertools
    vals = {}
    for s_ in ("25", "plan"):
        for t_ in ("25", "27"):
            for w_ in ("25", "clim"):
                vals[(s_, t_, w_)] = f_br(s_, t_, w_)
    base, full = ("25", "25", "25"), ("plan", "27", "clim")
    contrib = {"sea": [], "tides": [], "weather": []}
    pos = {"sea": 0, "tides": 1, "weather": 2}
    for order in itertools.permutations(["sea", "tides", "weather"]):
        cur = list(base)
        for fct in order:
            nxt = list(cur)
            nxt[pos[fct]] = full[pos[fct]]
            contrib[fct].append(vals[tuple(nxt)] - vals[tuple(cur)])
            cur = nxt
    out["bridge"] = {k: dict(shapley=float(np.mean(v)), lo=float(min(v)), hi=float(max(v))) for k, v in contrib.items()}
    out["bridge_base"] = vals[base]
    out["bridge_full"] = vals[full]
    out["bridge_vals"] = {"%s|%s|%s" % k: v for k, v in vals.items()}

    # shortcuts and variants
    var = {}
    var["front_rim"] = dict(hind=count_days(hw25.index, site_fn("front", "rim")(hw25.values, M25, Q25), 0.0),
                            exp=summary(E.counts(site_fn("front", "rim")))["mean"])
    for site in ("marsh", "oyster"):
        var[site + "_linear"] = dict(hind=count_days(hw25.index, site_fn(site, "linear")(hw25.values, M25, Q25), 0.0),
                                     exp=summary(E.counts(site_fn(site, "linear")))["mean"])
        var[site + "_none"] = dict(hind=count_days(hw25.index, site_fn(site, "none")(hw25.values, M25, Q25), 0.0),
                                   exp=summary(E.counts(site_fn(site, "none")))["mean"])
    for v in ("pooled", "none", "lin", "log", "pow"):
        var["river_" + v] = dict(hind=count_days(hw25.index, site_fn("river", v)(hw25.values, M25, Q25), 0.0),
                                 exp=summary(E.counts(site_fn("river", v)))["mean"])
    # the harbor by the count trend (log-linear on 1990-91 to 2025-26) and a Poisson range
    ys = np.arange(1990, 2026)
    cc = np.array([out["harbor_obs"][int(y)] for y in ys])
    b = np.polyfit(ys, np.log(cc + 0.5), 1)
    var["harbor_count_trend"] = float(np.exp(np.polyval(b, 2027)) - 0.5)
    from scipy.stats import poisson
    m = exp["harbor"]["mean"]
    var["harbor_poisson_range"] = (float(poisson.ppf(0.05, m)), float(poisson.ppf(0.95, m)))
    # residuals detrended by month instead of by tide year
    Em = Ensemble(H, Q, resid_col="r_month")
    var["harbor_month_detrend"] = float(np.mean(Em.counts(lambda Hh, M, Qq: Hh - HARBOR_MINOR)))
    # raw skew surges on the planning sea level (the sea level counted twice)
    Er = Ensemble(H, Q, resid_col="sk")
    var["harbor_raw_skew"] = float(np.mean(Er.counts(lambda Hh, M, Qq: Hh - HARBOR_MINOR)))
    # the defensible family each band is set on
    fam = {}
    for nm, kw in (("interp", {}), ("nearest", dict(align="nearest")), ("month_detrend", dict(resid_col="r_month"))):
        e = Ensemble(H, Q, **kw)
        fam[nm] = {site: float(np.mean(e.counts(site_fn(site)))) for site in ORDER}
        c = e.counts(lambda Hh, M, Qq: Hh - HARBOR_MINOR)
        fam[nm]["harbor"] = float(np.mean(c))
        fam[nm]["harbor_lo"] = float(np.percentile(c, 5))
        fam[nm]["harbor_hi"] = float(np.percentile(c, 95))
        for meth in ("nearest", "weibull", "hazen"):
            fam[nm]["harbor_lo_" + meth] = float(np.percentile(c, 5, method=meth))
            fam[nm]["harbor_hi_" + meth] = float(np.percentile(c, 95, method=meth))
    # marsh transfers by other smooth forms, river by the other flow form the fit admits
    alt = {}
    Hs = np.arange(5.0, 12.0, 0.0005)
    for site in ("marsh", "oyster"):
        d = fits[site]["pairs"]
        L = lane[site]
        hs = []
        for deg in (2, 3):
            c = np.polyfit(d.harbor.values, d.site.values, deg)
            hs.append(float(Hs[np.argmax(np.polyval(c, Hs) >= L)]))
        top = d[d.harbor >= 7.0]
        c = np.polyfit(top.harbor.values, top.site.values, 1)
        hs.append(float((L - c[1]) / c[0]))
        alt[site + "_Hstar"] = hs
        alt[site + "_hind"] = [count_days(hw25.index, hw25.values - h, 0.0) for h in hs]
        alt[site + "_exp"] = [float(np.mean(E.counts(lambda Hh, M, Qq, h=h: Hh - h))) for h in hs]
    alt["river_forms"] = {f: rf[f]["sse"] for f in rf}
    # each alignment replayed on 2025-26 with that year's own residuals and sea level, against the observed count
    replay = {}
    for nm in ("interp", "nearest", "daymax"):
        e = Ensemble(H, Q, ty=2025, plan=A25, years=[2025], align=nm)
        replay[nm] = int(e.counts(lambda Hh, M, Qq: Hh - HARBOR_MINOR)[0])
    out["replay_2025"] = replay
    # how sure: in how many weather years the funded pair is the top two that year
    per_year = {site: E.counts(site_fn(site)) for site in ORDER}
    hold = 0
    displaced = {}
    for i, y in enumerate(E.years):
        yr = {site: per_year[site][i] for site in ORDER}
        top = sorted(ORDER, key=lambda k: (-yr[k], ORDER.index(k)))[:2]
        if set(top) == set(out["funded"]):
            hold += 1
        else:
            for k in top:
                if k not in out["funded"]:
                    displaced[k] = displaced.get(k, 0) + 1
    out["pair_hold"] = hold
    out["per_year"] = {site: [int(x) for x in per_year[site]] for site in ORDER}
    out["per_year"]["harbor"] = [int(x) for x in E.counts(lambda Hh, M, Qq: Hh - HARBOR_MINOR)]
    # the careful but hurried pass's pair (straight-line marsh transfers, one river offset) and how often it holds there
    hur = dict(per_year)
    hur["marsh"] = E.counts(site_fn("marsh", "linear"))
    hur["oyster"] = E.counts(site_fn("oyster", "linear"))
    hur["river"] = E.counts(site_fn("river", "pooled"))
    hp = sorted(ORDER, key=lambda k: -np.mean(hur[k]))[:2]
    hh = 0
    for i, y in enumerate(E.years):
        top = sorted(ORDER, key=lambda k: (-hur[k][i], ORDER.index(k)))[:2]
        hh += set(top) == set(hp)
    out.setdefault("var", {})
    out["careful_pair"] = hp
    out["careful_pair_hold"] = int(hh)
    out["pair_displaced"] = displaced
    out["family"] = fam
    out["alt"] = alt
    var["careful_pair_hold"] = out["careful_pair_hold"]
    out["var"] = var
    return out


if __name__ == "__main__":
    import json
    import sys
    r = run(sys.argv[1])
    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items() if k not in ("pairs",)}
        if isinstance(o, (list, tuple)):
            return [clean(x) for x in o]
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        return o
    print(json.dumps(clean({k: v for k, v in r.items() if k not in ("datums",)}), indent=1)[:6000])
