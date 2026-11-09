"""Every route a careful analyst might take on the cut pack, scored against the golden six.

    python3 task13/generator/rivals.py

Two lists. The family (`family()`) holds the golden's own construction under every convention the pack leaves open:
the gust threshold, an excess-gust measure, the long-run years, a lag or bins in the growth, the customers-per-
interruption window, the catch-up's finish date, the station link, the trim date, the clock, the count model and the
cleaning choices. Each must return the golden six. The rungs (`rungs()`) are the routes that skip a step of the
golden: the worst-feeder ranking on recent vegetation customer interruptions, the overdue-weighted ranking, the
wind-normalised expected interruptions with all of them removable, the decomposition without the wind, the
decomposition with district-by-year effects in place of the station record, and the golden fit projected at the
recent or the outage record's own exposure. Each must miss most of the six.
"""
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import golden as G      # noqa: E402


def top6(s):
    return list(pd.Series(s).sort_values(ascending=False).index[:6])


class Ctx:
    """the cleaned pack, read once"""
    def __init__(self, target=C.TARGET):
        self.R = G.compute(target)
        self.K, self.wx = self.R['K'], self.R['wx']
        self.station, self.trims = self.R['station'], self.R['trims']
        self.EX, self.NE = self.R['EX'], self.R['NE']
        self.six = self.R['six']
        nv = self.K['veg'][~self.K['veg']['med']]
        self.nv = nv
        self.cpe = nv.groupby('feeder_now')['customers'].mean().reindex(sorted(self.station)).to_dict()


def golden_like(X, EX=None, NE=None, station=None, trims=None, growth='loglinear', lag=0.0, cpe=None, done=G.CATCHUP_DONE,
                K=None, nb=False):
    K = K or X.K
    EX = X.EX if EX is None else EX
    NE = G.normal(EX) if NE is None else NE
    station = station or X.station
    trims = trims or X.trims
    Pn = G.panel(K, EX, station, trims)
    if nb:
        import statsmodels.api as sm
        d = Pn[Pn['ex'] > 0]
        Xm = pd.get_dummies(d['feeder']).astype(float)
        Xm['g'] = d['ys'].values
        m = sm.GLM(d['n'].values, Xm.values, family=sm.families.NegativeBinomial(alpha=0.15),
                   offset=np.log(d['ex'].values)).fit()
        c = pd.Series(m.params, index=Xm.columns)
    else:
        c, _ = G.fit(Pn, growth=growth, lag=lag)
    if cpe is None:
        nv = K['veg'][~K['veg']['med']]
        cpe = nv.groupby('feeder_now')['customers'].mean().reindex(sorted(station)).to_dict()
    T = G.project(c, station, trims, NE, cpe, growth=growth, lag=lag, done=done)
    return T['avoided'], T, c


# ------------------------------------------------------------------ the family
def exposure_utc(target, base=G.BASE):
    """the gust load with months taken on the station record's own UTC clock"""
    cols = {}
    for sid in C.STATION_IDS:
        w = pd.read_csv(G.path_of('wx_' + sid, target))
        g = w['gust_max'].where(~w['qc'].isin(['M', 'S']))
        g = np.where(w['wind_unit'] == 'kt', g * 1.852, g)
        t = pd.to_datetime(w['obs_time_utc'], format='%Y-%m-%dT%H:%MZ').dt.to_period('M')
        cols[sid] = pd.Series(np.clip(g - base, 0, None) ** 2).groupby(t.values).sum()
    return pd.DataFrame(cols)


def blended_station(X):
    """each feeder's exposure as the inverse-distance blend of its two nearest stations"""
    zone = X.K['zs'].set_index('Code')
    st = X.K['st']
    out = {}
    for _, r in X.K['fr'].iterrows():
        la, lo = zone.loc[r['Zone substation'], 'Latitude'], zone.loc[r['Zone substation'], 'Longitude']
        d = sorted((G.haversine(la, lo, s['latitude'], s['longitude']), s['station_id']) for _, s in st.iterrows())[:2]
        w1, w2 = 1 / max(d[0][0], 1.0), 1 / max(d[1][0], 1.0)
        out[r['Feeder']] = ((d[0][1], w1 / (w1 + w2)), (d[1][1], w2 / (w1 + w2)))
    return out


def family(X, target=C.TARGET):
    F = {}
    for thr in (45, 50, 55, 60, 65, 70):
        EXt = G.exposure(X.wx, thr)
        F['SF8 hours of gusts %d km/h or more' % thr] = top6(golden_like(X, EX=EXt)[0])
    for b in (35, 45):
        F['SF8 gust load over %d km/h' % b] = top6(golden_like(X, EX=G.gust_load(X.wx, b))[0])
    for b in (40, 45):
        F['SF8 straight gust excess over %d km/h' % b] = top6(golden_like(X, EX=G.gust_load(X.wx, b, 1.0))[0])
    for yrs in ((2006, 2024), (2006, 2026), (2011, 2025), (2016, 2025)):
        F['SF9 normal %d-%d' % yrs] = top6(golden_like(X, NE=G.normal(X.EX, yrs))[0])
    for lag in (0.5, 1.0):
        F['SF10 growth after a %.1f-year lag' % lag] = top6(golden_like(X, lag=lag)[0])
    F['SF10 growth by whole years since trim'] = top6(golden_like(X, growth='bins')[0])
    nv = X.nv
    cpe3 = nv[nv['start'] >= '2023-11-01'].groupby('feeder_now')['customers'].mean().reindex(sorted(X.station)).to_dict()
    F['SF7 customers per interruption since November 2023'] = top6(golden_like(X, cpe=cpe3)[0])
    icp = X.K['icp']
    last = icp[icp['month_end'] == '2026-10'].set_index('feeder')['icps_connected']
    mean_icp = icp.groupby('feeder')['icps_connected'].mean()
    cpe_s = {f: X.cpe[f] * last[f] / mean_icp[f] for f in X.cpe}
    F['SF7 customers per interruption at October 2026 ICPs'] = top6(golden_like(X, cpe=cpe_s)[0])
    for done in ('2026-12-15', '2027-02-01'):
        F['SF6 catch-up finished %s' % done] = top6(golden_like(X, done=pd.Timestamp(done))[0])
    # SF11: the inverse-distance blend of the two nearest stations
    bl = blended_station(X)
    EXb = pd.DataFrame({f: sum(X.EX[s] * w for s, w in bl[f]) for f in bl})
    NEb = G.normal(EXb)
    station_b = {f: f for f in bl}
    F['SF11 two nearest stations blended'] = top6(golden_like(X, EX=EXb, NE=NEb, station=station_b, trims=X.trims)[0])
    # SF12: the job closed date as the trim date
    cyc = X.K['cyc'].copy()
    cyc['Crew finished'] = pd.to_datetime(cyc['Job closed']).fillna(pd.to_datetime(cyc['Crew finished']))
    F['SF12 trim dated by the job closed'] = top6(golden_like(X, trims=G.last_trims(cyc))[0])
    # SF13: exposure months by UTC
    EXu = exposure_utc(target)
    F['SF13 exposure months in UTC'] = top6(golden_like(X, EX=EXu)[0])
    F['SF16 negative binomial counts'] = top6(golden_like(X, nb=True)[0])
    # cleaning choices
    for name, K2 in variants(X).items():
        F[name] = top6(golden_like(X, K=K2)[0])
    return F


def variants(X):
    """the golden's cleaned record under each cleaning convention a run might take (SF1 to SF4, SF14)"""
    K = X.K
    o = K['o']
    out = {}
    base_u = K['u']

    def with_u(u):
        K2 = dict(K)
        K2['veg'] = u[u['cause_code'].isin(G.VEG)].copy()
        K2['veg']['ym'] = K2['veg']['start'].dt.to_period('M')
        return K2
    u = base_u.copy()
    u2 = u.copy()
    K2 = dict(K)
    v = u2[u2['cause_code'].isin(G.VEG | {'WTH', 'WEATHER'})].copy()
    v['ym'] = v['start'].dt.to_period('M')
    K2['veg'] = v
    out['SF1 adverse weather counted as vegetation'] = K2
    raw = pd.read_csv(G.path_of('oms', C.TARGET), dtype=str, keep_default_na=False)
    o_all = G.read_oms(C.TARGET, K['fr'])
    um = o_all[(o_all['interruption_class'] == 'Unplanned') & (o_all['source'] != 'Call centre')].copy()
    um['med'] = um['start'].dt.normalize().isin(K['meds'])
    out['SF2 momentary interruptions counted'] = with_u(um)
    ud = o_all[(o_all['interruption_class'] == 'Unplanned') & (o_all['minutes'] >= 1.0)].copy()
    ud['med'] = ud['start'].dt.normalize().isin(K['meds'])
    ud['cause_code'] = ud['cause_code'].replace({'Trees': 'TREE'})
    out['SF3 call centre records kept'] = with_u(ud)
    un = u.copy()
    un['med'] = False
    out['SF4 major event days kept'] = with_u(un)
    us = u.copy()
    meds_s = {d for d in K['saidi'].index
              if K['saidi'][d] > (K['bounds']['DPP3'] if G.regulatory_year(d) <= 2024 else K['bounds']['DPP4'])[0]}
    us['med'] = us['start'].dt.normalize().isin(meds_s)
    out['SF4 major event days on SAIDI alone'] = with_u(us)
    ur = u[~u['feeder'].str.startswith('RGS')].copy()
    out['SF14 Rangiora Street history before the rename dropped'] = with_u(ur)
    return out


# ------------------------------------------------------------------ the rungs
def ci_window(X, a, b='2026-10'):
    nv = X.nv
    x = nv[(nv['ym'] >= pd.Period(a, 'M')) & (nv['ym'] <= pd.Period(b, 'M'))]
    return x.groupby('feeder_now')['customers'].sum().reindex(sorted(X.station)).fillna(0)


def ys27(X):
    return pd.Series({f: G.years_since(X.trims[f], G.CATCHUP_DONE) for f in X.station})


def no_exposure(X, fe=None, growth='loglinear'):
    """the decomposition fitted on counts alone: a feeder's corridor rate and the growth since trim, no station"""
    import statsmodels.api as sm
    Pn = G.panel(X.K, X.EX, X.station, X.trims)
    d = Pn.copy()
    M = pd.get_dummies(d['feeder']).astype(float)
    if growth == 'loglinear':
        M['g'] = d['ys'].values
    else:
        b = np.clip(np.floor(d['ys'].values), 0, 6).astype(int)
        for k in range(1, 7):
            M['b%d' % k] = (b == k).astype(float)
    yrs = np.array([p.year for p in d['ym']])
    moy = np.array([p.month for p in d['ym']])
    if fe == 'year':
        for y in range(2023, 2027):
            M['y%d' % y] = (yrs == y).astype(float)
    if fe == 'month':
        for k in range(2, 13):
            M['m%d' % k] = (moy == k).astype(float)
    if fe == 'district-year':
        for s in C.STATION_IDS:
            for y in range(2023, 2027):
                M['%s%d' % (s, y)] = ((yrs == y) & (d['station'].values == s)).astype(float)
    m = sm.GLM(d['n'].values, M.values, family=sm.families.Poisson()).fit()
    c = pd.Series(m.params, index=M.columns)
    g = G.growth_fn(c, growth)
    out = {}
    for f in sorted(X.station):
        a = math.exp(c[f])
        if fe == 'year':
            a *= np.mean([math.exp(c.get('y%d' % y, 0.0)) for y in range(2022, 2027)])
        if fe == 'district-year':
            a *= np.mean([math.exp(c.get('%s%d' % (X.station[f], y), 0.0)) for y in range(2022, 2027)])
        sea = np.array([math.exp(c.get('m%d' % p.month, 0.0)) for p in G.RY27]) if fe == 'month' else np.ones(12)
        ys_k = np.array([G.years_since(X.trims[f], G.mid(p)) for p in G.RY27])
        ys_c = np.array([(G.mid(p) - G.CATCHUP_DONE).days / 365.25 for p in G.RY27])
        out[f] = ((a * g(ys_k) * sea).sum() - (a * g(ys_c) * sea).sum()) * X.cpe[f]
    return pd.Series(out)


def mean_gust_offset(X):
    cols = {sid: g.groupby(g.index.to_period('M')).mean() for sid, g in X.wx.items()}
    EXm = pd.DataFrame(cols)
    return golden_like(X, EX=EXm)[0]


def rungs(X):
    out = {}
    out['R0 vegetation customer interruptions, last twelve months'] = top6(ci_window(X, '2025-11'))
    out['R1 vegetation customer interruptions, three years to October 2026 (default path)'] = top6(ci_window(X, '2023-11'))
    out['R1b vegetation customer interruptions, the whole record'] = top6(ci_window(X, '2022-04'))
    n3 = X.nv[X.nv['ym'] >= pd.Period('2023-11', 'M')].groupby('feeder_now').size().reindex(sorted(X.station)).fillna(0)
    out['R1c vegetation interruptions, three years'] = top6(n3)
    y = ys27(X)
    out['R2 most years since the last cycle trim'] = top6(y)
    cyc = X.K['fr'].set_index('Feeder')['Vegetation cycle (years)']
    out['R2b most overdue against the feeder cycle'] = top6(y / cyc.reindex(y.index))
    ci3 = ci_window(X, '2023-11')
    out['R5 three-year customer interruptions times years since trim'] = top6(ci3 * y)
    out['R5b three-year customer interruptions times cycles overdue'] = top6(ci3 * np.clip(y / cyc.reindex(y.index) - 1, 0, None))
    ex3 = X.EX.loc[pd.Period('2023-11', 'M'):pd.Period('2026-10', 'M')].sum()
    NEs = X.NE.sum()
    r3 = {f: n3[f] / ex3[X.station[f]] * NEs[X.station[f]] * X.cpe[f] for f in X.station}
    out['R3 wind-normalised three-year rate at the long-run exposure, all of it removable'] = top6(r3)
    out['R3b the golden fit, all of 2027-28 removable'] = top6(X.R['T']['keep_ci'])
    out['R6 decomposition on counts, no station record'] = top6(no_exposure(X))
    out['R6y decomposition on counts with year effects'] = top6(no_exposure(X, fe='year'))
    out['R6m decomposition on counts with calendar-month effects'] = top6(no_exposure(X, fe='month'))
    out['R6b decomposition on counts, growth by whole years'] = top6(no_exposure(X, growth='bins'))
    out['R6w decomposition on the mean gust'] = top6(mean_gust_offset(X))
    out['R7 decomposition with district-by-year effects, projected at their average'] = top6(no_exposure(X, fe='district-year'))
    rec = X.EX.loc[pd.Period('2023-11', 'M'):pd.Period('2026-10', 'M')]
    NEr = rec.groupby(rec.index.month).mean()
    out['R8 the golden fit projected at the three years to October 2026'] = top6(golden_like(X, NE=NEr)[0])
    win = X.EX.loc[pd.Period('2022-04', 'M'):pd.Period('2026-10', 'M')]
    NEw = win.groupby(win.index.month).mean()
    out['R9 the golden fit projected at the outage record\'s own exposure'] = top6(golden_like(X, NE=NEw)[0])
    return out


def run(target=C.TARGET, X=None):
    X = X or Ctx(target)
    return X, family(X, target), rungs(X)


if __name__ == '__main__':
    X, fam, rg = run()
    six = set(X.six)
    print('golden six', X.six)
    print('family')
    for k, v in fam.items():
        print('  %d  %s' % (len(set(v) & six), k))
    print('rungs')
    for k, v in rg.items():
        print('  %d  %-80s %s' % (len(set(v) & six), k, ' '.join(v)))
    print('levels of the six across measures')
    for name, EX in [('gust load over 40 (golden)', X.EX)] + [('hours %d+' % t, G.exposure(X.wx, t)) for t in (45, 50, 60)] + [('load over %d' % b, G.gust_load(X.wx, b)) for b in (35, 45)] + [('straight over 45', G.gust_load(X.wx, 45, 1.0))]:
        av, T, c = golden_like(X, EX=EX)
        print('  %-28s total %.0f  growth %.1f%%' % (name, T.loc[X.six, 'avoided'].sum(), (math.exp(c['g']) - 1) * 100))
