"""The golden route, read from the shipped pack alone (target/), never from the world.

1. The outage export cleaned by the reliability reporting standard: one interruption per device operation (the call
   centre's records of an operation SCADA or the field crew also logged are dropped), sustained means 1 minute or
   longer, unplanned only, vegetation is VEG to 30 September 2023 and TREE from 1 October 2023, and Rangiora Street's
   former feeder codes mapped through the feeder register.
2. Major event days: the day's unplanned SAIDI or SAIFI over the regulatory year's average month-end ICPs (the latest
   month-end for the year in progress) above the path's boundary value.
3. Each feeder's weather station is the station nearest its zone substation. Each station's exposure in a month is
   its gust load: the sum over the month's hours of the square of each hour's gust above 40 km/h (knots converted,
   missing and suspect hours left out). Of the measures tried (hours of gusts at or above 40 to 70 km/h, the gust
   excess over 30 to 50 km/h, straight or squared), it fits the record best, and the hour counts from 50 km/h up
   leave months with vegetation interruptions and no exposure at all.
4. Each feeder's vegetation interruptions outside major event days, month by month from April 2022, are fitted as
   Poisson counts on the station's exposure: a rate for the feeder's corridor straight after a cycle trim, times a
   growth common to the network per year since the feeder's last cycle trim (crew-finished dates in the cycle log).
5. 2027-28 is projected month by month at each station's long-run exposure (the mean of each calendar month over
   2006 to 2025), with the corridor left as it stands and with the catch-up finished on 31 March 2027, and turned into
   customer interruptions at the feeder's own customers per vegetation interruption since April 2022.
6. The six feeders with the most customer interruptions avoided.
"""
import json
import math
import os
import re
import warnings

import numpy as np
import pandas as pd

import common as C

warnings.filterwarnings('ignore')
THRESHOLD = 60.0       # the strong-wind hours the station figures report
BASE = 40.0            # the gust load counts each hour's gust above this, squared
NORMAL_YEARS = (2006, 2025)
OMS0 = pd.Timestamp('2022-04-01')
RY27 = pd.period_range('2027-04', '2028-03', freq='M')
CATCHUP_DONE = pd.Timestamp('2027-03-31')
LATEST = pd.Period('2026-10', 'M')
ANOM_YEARS = (2024, 2026)      # November-to-October years 2023-24 to 2025-26, for the station figures
VEG = {'VEG', 'TREE'}


def path_of(name, target):
    return os.path.join(target, C.FILES[name])


def regulatory_year(t):
    return t.year if t.month >= 4 else t.year - 1


# ------------------------------------------------------------------ reading the pack
def read_registers(target):
    fr = pd.read_excel(path_of('feeders', target), sheet_name='Feeders', header=3)
    zs = pd.read_excel(path_of('feeders', target), sheet_name='Zone substations', header=2)
    st = pd.read_csv(path_of('stations', target))
    cyc = pd.read_excel(path_of('vegcycle', target), sheet_name='Cycle jobs', header=3)
    icp = pd.read_csv(path_of('icps', target))
    return fr, zs, st, cyc, icp


def boundary_values(target):
    from docx import Document
    doc = Document(path_of('standard', target))
    out = {}
    for t in doc.tables:
        head = [c.text.strip() for c in t.rows[0].cells]
        if head and head[0] == 'Path':
            for r in t.rows[1:]:
                cells = [c.text.strip() for c in r.cells]
                out[cells[0]] = (float(cells[2]), float(cells[3]))
    return out


def read_oms(target, fr):
    o = pd.read_csv(path_of('oms', target), dtype=str, keep_default_na=False)
    former = {str(a): b for a, b in zip(fr['Former code'], fr['Feeder']) if isinstance(a, str) and a}
    o['feeder_now'] = o['feeder'].map(lambda x: former.get(x, x))
    o['device_now'] = [d.replace(f, g, 1) if f != g else d for d, f, g in zip(o['protection_ref'], o['feeder'], o['feeder_now'])]
    o['start'] = pd.to_datetime(o['start_time'], format='%Y-%m-%d %H:%M')
    o['minutes'] = o['duration_min'].astype(float)
    o['customers'] = o['customers_interrupted'].astype(int)
    return o


def dedupe(o):
    """the call centre's record of an operation that SCADA or the field crew also logged is not a second interruption"""
    cc = o[o['source'] == 'Call centre']
    rest = o[o['source'] != 'Call centre']
    by_dev = {d: g['start'].values for d, g in rest.groupby('device_now')}
    drop = []
    for i, r in cc.iterrows():
        s = by_dev.get(r['device_now'])
        if s is not None and np.any(np.abs((s - np.datetime64(r['start'])).astype('timedelta64[m]').astype(int)) <= 30):
            drop.append(i)
    return o.drop(index=drop), len(drop)


def ry_icps(icp):
    tot = icp.groupby('month_end')['icps_connected'].sum()
    tot.index = pd.PeriodIndex(tot.index, freq='M')
    out = {}
    for ry in range(2022, 2027):
        months = pd.period_range('%d-04' % ry, '%d-03' % (ry + 1), freq='M')
        have = [m for m in months if m in tot.index]
        out[ry] = float(tot[have].mean()) if len(have) == 12 else float(tot[LATEST])
    return out, float(tot[LATEST])


def major_event_days(u, icp_ry, bounds):
    """u: unplanned sustained interruptions (all causes)"""
    u = u.copy()
    u['day'] = u['start'].dt.normalize()
    u['ry'] = [regulatory_year(t) for t in u['start']]
    den = u['ry'].map(icp_ry)
    saidi = (u['customers'] * u['minutes'] / den).groupby(u['day']).sum()
    saifi = (u['customers'] / den).groupby(u['day']).sum()
    meds = set()
    for d in saidi.index:
        b = bounds['DPP3'] if regulatory_year(d) <= 2024 else bounds['DPP4']
        if saidi[d] > b[0] or saifi[d] > b[1]:
            meds.add(d)
    return meds, saidi, saifi


def read_weather(target):
    """hourly gusts in km/h at each station, indexed by New Zealand local time; missing and suspect hours dropped"""
    out = {}
    for sid in C.STATION_IDS:
        w = pd.read_csv(path_of('wx_' + sid, target), dtype={'gust_max': float})
        g = w['gust_max'].where(~w['qc'].isin(['M', 'S']))
        g = np.where(w['wind_unit'] == 'kt', g * 1.852, g)
        t = pd.to_datetime(w['obs_time_utc'], format='%Y-%m-%dT%H:%MZ', utc=True).dt.tz_convert(C.ZONE).dt.tz_localize(None)
        out[sid] = pd.Series(g, index=pd.DatetimeIndex(t))
    return out


def exposure(wx, threshold=THRESHOLD):
    """hours at or above the threshold, by station and local month"""
    cols = {}
    for sid, g in wx.items():
        cols[sid] = (g >= threshold).astype(float).groupby(g.index.to_period('M')).sum()
    return pd.DataFrame(cols)


def gust_load(wx, base=BASE, power=2.0):
    """the sum over each local month's hours of the gust above the base, raised to the power"""
    cols = {}
    for sid, g in wx.items():
        cols[sid] = (np.clip(g - base, 0, None) ** power).groupby(g.index.to_period('M')).sum()
    return pd.DataFrame(cols)


def normal(EX, years=NORMAL_YEARS):
    d = EX[(EX.index.year >= years[0]) & (EX.index.year <= years[1])]
    return d.groupby(d.index.month).mean()


def haversine(a, b, c, d):
    r = math.pi / 180
    x = math.sin((c - a) * r / 2) ** 2 + math.cos(a * r) * math.cos(c * r) * math.sin((d - b) * r / 2) ** 2
    return 12742 * math.asin(math.sqrt(x))


def station_of(fr, zs, st):
    zone = zs.set_index('Code')
    out = {}
    for _, r in fr.iterrows():
        la, lo = zone.loc[r['Zone substation'], 'Latitude'], zone.loc[r['Zone substation'], 'Longitude']
        dist = [(haversine(la, lo, s['latitude'], s['longitude']), s['station_id']) for _, s in st.iterrows()]
        out[r['Feeder']] = min(dist)[1]
    return out


def last_trims(cyc):
    t = {}
    for f, g in cyc.groupby('Feeder'):
        t[f] = sorted(pd.to_datetime(g['Crew finished']).tolist())
    return t


def years_since(trims, when):
    prior = [d for d in trims if d <= when]
    if not prior:
        return np.nan
    return (when - prior[-1]).days / 365.25


def mid(p):
    return p.start_time + pd.Timedelta(days=14)


# ------------------------------------------------------------------ the golden computation
def clean(target):
    fr, zs, st, cyc, icp = read_registers(target)
    o = read_oms(target, fr)
    o, n_dup = dedupe(o)
    u = o[(o['interruption_class'] == 'Unplanned') & (o['minutes'] >= 1.0)].copy()
    icp_ry, icp_latest = ry_icps(icp)
    bounds = boundary_values(target)
    meds, saidi, saifi = major_event_days(u, icp_ry, bounds)
    u['med'] = u['start'].dt.normalize().isin(meds)
    veg = u[u['cause_code'].isin(VEG)].copy()
    veg['ym'] = veg['start'].dt.to_period('M')
    return dict(fr=fr, zs=zs, st=st, cyc=cyc, icp=icp, o=o, u=u, veg=veg, n_dup=n_dup, meds=meds, saidi=saidi,
                saifi=saifi, icp_ry=icp_ry, icp_latest=icp_latest, bounds=bounds)


def panel(K, EX, station, trims, nonmed_only=True):
    veg = K['veg'][~K['veg']['med']] if nonmed_only else K['veg']
    cnt = veg.groupby(['feeder_now', 'ym']).size()
    months = pd.period_range(OMS0, LATEST, freq='M')
    rows = []
    for f in sorted(station):
        for p in months:
            rows.append((f, p, station[f], years_since(trims[f], mid(p)), int(cnt.get((f, p), 0)),
                         float(EX.loc[p, station[f]])))
    return pd.DataFrame(rows, columns=['feeder', 'ym', 'station', 'ys', 'n', 'ex'])


def fit(Pn, growth='loglinear', lag=0.0, offset=True):
    import statsmodels.api as sm
    d = Pn[Pn['ex'] > 0] if offset else Pn
    X = pd.get_dummies(d['feeder']).astype(float)
    if growth == 'loglinear':
        X['g'] = np.clip(d['ys'].values - lag, 0, None)
    elif growth == 'bins':
        b = np.clip(np.floor(d['ys'].values), 0, 6).astype(int)
        for k in range(1, 7):
            X['b%d' % k] = (b == k).astype(float)
    m = sm.GLM(d['n'].values, X.values, family=sm.families.Poisson(),
               offset=np.log(d['ex'].values) if offset else None).fit()
    return pd.Series(m.params, index=X.columns), m


def growth_fn(c, growth='loglinear', lag=0.0):
    if growth == 'loglinear':
        return lambda ys: np.exp(c['g'] * np.clip(np.asarray(ys) - lag, 0, None))

    def f(ys):
        b = np.clip(np.floor(np.asarray(ys)), 0, 6).astype(int)
        out = np.ones(len(b))
        for k in range(1, 7):
            out = np.where(b == k, np.exp(c['b%d' % k]), out)
        return out
    return f


def project(c, station, trims, NE, cpe, growth='loglinear', lag=0.0, done=CATCHUP_DONE, offset=True, monthly=False):
    g = growth_fn(c, growth, lag)
    out, by_month = {}, {}
    for f in sorted(station):
        ex = np.array([NE.loc[p.month, station[f]] if offset else 1.0 for p in RY27])
        ys_keep = np.array([years_since(trims[f], mid(p)) for p in RY27])
        ys_cu = np.array([(mid(p) - done).days / 365.25 for p in RY27])
        a = math.exp(c[f])
        keep_m = a * g(ys_keep) * ex
        cu_m = a * g(ys_cu) * ex
        keep, cu = keep_m.sum(), cu_m.sum()
        by_month[f] = (keep_m - cu_m) * cpe[f]
        out[f] = dict(keep_n=keep, cu_n=cu, cpe=cpe[f], keep_ci=keep * cpe[f], cu_ci=cu * cpe[f],
                      avoided=(keep - cu) * cpe[f])
    T = pd.DataFrame(out).T
    return (T, pd.DataFrame(by_month, index=[str(p) for p in RY27])) if monthly else T


def compute(target):
    K = clean(target)
    wx = read_weather(target)
    EX = gust_load(wx)
    NE = normal(EX)
    H60 = exposure(wx)
    station = station_of(K['fr'], K['zs'], K['st'])
    trims = last_trims(K['cyc'])
    Pn = panel(K, EX, station, trims)
    c, m = fit(Pn)
    nv = K['veg'][~K['veg']['med']]
    cpe = nv.groupby('feeder_now')['customers'].mean().reindex(sorted(station)).to_dict()
    T = project(c, station, trims, NE, cpe)
    T['avoided_r'] = T['avoided'].round().astype(int)
    T = T.sort_values('avoided', ascending=False)
    T['rank'] = range(1, len(T) + 1)
    six = list(T.index[:6])
    return dict(K=K, wx=wx, EX=EX, NE=NE, H60=H60, station=station, trims=trims, P=Pn, coef=c, model=m, cpe=cpe, T=T,
                six=six)


def quarters(R):
    """the six's customer interruptions avoided in each quarter of 2027-28 (April to June first), rounded so they
    add to the year's figure"""
    T, M = project(R['coef'], {f: R['station'][f] for f in R['six']}, R['trims'], R['NE'], R['cpe'], monthly=True)
    tot = M.sum(axis=1).values
    q = [float(tot[3 * k:3 * k + 3].sum()) for k in range(4)]
    r = [int(round(x)) for x in q]
    year = int(round(sum(q)))
    while sum(r) != year:
        k = int(np.argmax([x - round(x) for x in q]) if sum(r) < year else np.argmin([x - round(x) for x in q]))
        r[k] += 1 if sum(r) < year else -1
    return r


def weather_years(R, years=(2006, 2024)):
    """the six's customer interruptions avoided in 2027-28 had it the weather of each regulatory year of the station
    record (each month's exposure as recorded), the fitted corridors and growth held"""
    EX, six = R['EX'], R['six']
    out = {}
    for y in range(years[0], years[1] + 1):
        months = pd.period_range('%d-04' % y, '%d-03' % (y + 1), freq='M')
        NEy = pd.DataFrame({sid: [EX.loc[m, sid] for m in months] for sid in EX.columns},
                           index=[m.month for m in months])
        T = project(R['coef'], {f: R['station'][f] for f in six}, R['trims'], NEy, R['cpe'])
        out[y] = float(T['avoided'].sum())
    return pd.Series(out)


def weather_range(R):
    v = weather_years(R)
    return float(np.percentile(v, 5)), float(np.percentile(v, 95)), v


# ------------------------------------------------------------------ figures
def station_figures(EX):
    out = {}
    yr = np.array([p.year + (1 if p.month >= 11 else 0) for p in EX.index])
    for sid in C.STATION_IDS:
        s = EX[sid]
        norm = np.mean([s[yr == y].sum() for y in range(2007, 2024)])
        recent = np.mean([s[yr == y].sum() for y in range(ANOM_YEARS[0], ANOM_YEARS[1] + 1)])
        out[sid] = dict(normal=round(float(norm)), recent=round(float(recent)), ratio=round(float(recent / norm), 2))
    return out


def mean_gust_figures(wx):
    out = {}
    for sid, g in wx.items():
        yr = np.array([t.year + (1 if t.month >= 11 else 0) for t in g.index])
        norm = float(np.nanmean([np.nanmean(g.values[yr == y]) for y in range(2007, 2024)]))
        recent = float(np.nanmean(g.values[(yr >= ANOM_YEARS[0]) & (yr <= ANOM_YEARS[1])]))
        out[sid] = dict(normal=round(norm, 1), recent=round(recent, 1), change_pct=round((recent / norm - 1) * 100, 1))
    return out


def default_path(K, months=('2023-11', '2026-10')):
    nv = K['veg'][~K['veg']['med']]
    a, b = pd.Period(months[0], 'M'), pd.Period(months[1], 'M')
    x = nv[(nv['ym'] >= a) & (nv['ym'] <= b)]
    ci = x.groupby('feeder_now')['customers'].sum().sort_values(ascending=False)
    return ci


def family_totals(R):
    """the six's total under the exposure measures that fit the record nearly as well, and the hour counts"""
    out = []
    for EX in [exposure(R['wx'], t) for t in (45, 50, 55, 60)] + [gust_load(R['wx'], b) for b in (35, 45)] + \
              [gust_load(R['wx'], b, 1.0) for b in (40, 45)]:
        Pn = panel(R['K'], EX, R['station'], R['trims'])
        c, _ = fit(Pn)
        T = project(c, R['station'], R['trims'], normal(EX), R['cpe'])
        out.append(float(T.sort_values('avoided', ascending=False)['avoided'].iloc[:6].sum()))
    return [int(round(min(out))), int(round(max(out)))]


def fit_range(R, n=400):
    """what the fit's own uncertainty alone gives the six's total (5th and 95th percentiles)"""
    cov = np.asarray(R['model'].cov_params())
    rng = np.random.default_rng(5)
    sims = []
    for d in rng.multivariate_normal(R['coef'].values, cov, n):
        cc = pd.Series(d, index=R['coef'].index)
        sims.append(float(project(cc, {f: R['station'][f] for f in R['six']}, R['trims'], R['NE'], R['cpe'])['avoided'].sum()))
    lo, hi = np.percentile(sims, [5, 95])
    return [int(round(lo, -3)), int(round(hi, -3))]


def figures(R):
    T, K = R['T'], R['K']
    six = R['six']
    tot = float(T.loc[six, 'avoided'].sum())
    dp = default_path(K)
    lo, hi, wy = weather_range(R)
    F = {
        'range90': [int(round(lo, -3)), int(round(hi, -3))],
        'range90_raw': [round(lo, 1), round(hi, 1)],
        'weather_years': {int(k): int(round(v)) for k, v in wy.items()},
        'quarters': quarters(R),
        'six': six,
        'avoided_six': {f: int(round(T.loc[f, 'avoided'])) for f in six},
        'avoided_total': int(round(tot)),
        'saifi_avoided': round(tot / R['K']['icp_latest'], 2),
        'icps_latest': int(R['K']['icp_latest']),
        'growth_per_year_pct': round((math.exp(R['coef']['g']) - 1) * 100, 1),
        'gamma': round(float(R['coef']['g']), 4),
        'stations': station_figures(R['H60']),
        'mean_gust': mean_gust_figures(R['wx']),
        'station_of': R['station'],
        'seventh': T.index[6], 'seventh_avoided': int(round(T['avoided'].iloc[6])),
        'gap_6_7': round(float(T['avoided'].iloc[5] / T['avoided'].iloc[6]), 3),
        'default_six': list(dp.index[:6]),
        'default_six_avoided': int(round(float(T.loc[list(dp.index[:6]), 'avoided'].sum()))),
        'keep_six_total': int(round(float(T.loc[six, 'keep_ci'].sum()))),
        'cu_six_total': int(round(float(T.loc[six, 'cu_ci'].sum()))),
        'default_ci_3yr': {f: int(dp[f]) for f in dp.index[:6]},
        'med_days': len(R['K']['meds']),
        'duplicates_dropped': int(R['K']['n_dup']),
        'feeders': len(T),
        'strong_wind_kmh': int(THRESHOLD),
        'load_base_kmh': int(BASE),
        'record_years': 19,
        'vegetation_interruptions': int(len(K['veg'])),
        'oms_rows': int(len(K['o']) + K['n_dup']),
        'family_total_range': family_totals(R),
        'fit_range90': fit_range(R),
        'plantation': {f: dict(keep_ci=int(round(T.loc[f, 'keep_ci'])), cu_ci=int(round(T.loc[f, 'cu_ci'])),
                               avoided=int(round(T.loc[f, 'avoided'])), rank=int(T.loc[f, 'rank'])) for f in dp.index[:6]},
        'rows': [dict(feeder=f, station=R['station'][f], keep_n=round(float(T.loc[f, 'keep_n']), 1),
                      cpe=int(round(T.loc[f, 'cpe'])), keep_ci=int(round(T.loc[f, 'keep_ci'])),
                      cu_ci=int(round(T.loc[f, 'cu_ci'])), avoided=int(round(T.loc[f, 'avoided'])), rank=int(T.loc[f, 'rank']))
                 for f in T.index],
    }
    return F


def build(target, golden_dir, figures=None):
    import deliver
    R = compute(target)
    F_ = globals()['figures'](R)
    if figures:
        json.dump(F_, open(figures, 'w'), indent=1, default=str)
    deliver.build(F_, R, golden_dir)
    return R, F_
