"""The golden chain, computed from the shipped files only (target/), and the switches the hurried passes and the rivals
turn. Every graded figure comes from `run(target)`; checks.py, effort_passes.py and golden.py read it.

  R1  each fault's first trip matched to a ground stroke near its zone on the device's own clock (the radio-less
      reclosers' drift fitted per device from the strokes, the clock set at each read)
  R2  the radio-less zones' faults their memories overwrote and their unread months, filled at the zone's own rate
  R3  the sound-protection expectation, fitted on the zone-seasons a later cyclic inspection found sound
  R4  the referral after 2026: faults since the last cyclic inspection against the expectation, a negative binomial
      tail with the confirmed-sound zones' spread, at no more than one sound zone a season
  R5  the same rule after each season since 2022
  R6  the sound zones it should refer in a season: each zone's tail at the smallest count the rule refers it at
  R7  its referrals against the following cyclic inspections
  R8  the lightning faults the refit avoids in a season of average lightning"""
import json
import math
import os

import numpy as np
import pandas as pd
from scipy import optimize, stats

import common as C
import geo as GEO

SEASONS = [2022, 2023, 2024, 2025, 2026]          # the seasons the rule is run after and reported
ALL = list(range(2017, 2027))                      # every season in the record: the fit and the windows
DL_MAP = {'Trip': 'TRIP', 'Reclose': 'RECLOSE', 'Lockout': 'LOCKOUT', 'Close': 'CLOSE', 'Open': 'OPEN',
          'HLT On': 'HLT ON', 'HLT Off': 'HLT OFF', 'AC Supply Off': 'AC OFF', 'AC Supply On': 'AC ON',
          'Battery Test': 'BATTERY TEST', 'Door Open': 'DOOR OPEN', 'Event Log Read': 'LOG READ', 'Clock Set': 'CLOCK SET'}

DEFAULT = dict(clock='aligned', wide_win=(-600, 600), fill=True, null='verified', disp='nb', window='since_inspection', excl_ic=False,
               rmax=0.4, win=(-0.6, 0.7), alpha='zones', avoided='last_season', null_model='zone', own='outside', k_scale=1.0,
               match_dedupe=True, budget_seasons=5, kfit='mle', spec='full')


def season_of(t):
    t = pd.DatetimeIndex(t)
    return np.where((t.month >= 4) & (t.month <= 10), t.year, -1)


# ------------------------------------------------------------------ reading the pack
def load(target):
    f = lambda k: os.path.join(target, C.FILES[k])
    zr = pd.read_excel(f('zones'), sheet_name='Zones', header=3)
    zr = zr.rename(columns={'Zone (protective device)': 'zone'})
    zones = list(zr.zone)
    zix = {z: i for i, z in enumerate(zones)}
    gj = json.load(open(f('routes')))
    seg = []
    for ft in gj['features']:
        pr = ft['properties']
        co = np.array(ft['geometry']['coordinates'])
        x, y = C.to_xy(co[:, 1], co[:, 0])
        for i in range(len(co) - 1):
            seg.append((zix[pr['zone']], x[i], y[i], x[i + 1], y[i + 1], pr['construction'], pr['area'], pr['phases']))
    S = pd.DataFrame(seg, columns=['zone_ix', 'x0', 'y0', 'x1', 'y1', 'construction', 'area', 'phases'])
    st = pd.read_csv(f('strokes'))
    t = pd.to_datetime(st.datetime_utc.str.rstrip('Z'), format='%Y-%m-%dT%H:%M:%S.%f') + pd.Timedelta(hours=8)
    sx, sy = C.to_xy(st.latitude.values, st.longitude.values)
    t = t.astype('datetime64[ns]')
    strokes = pd.DataFrame({'t': t, 'x': sx, 'y': sy, 'I': st.peak_current_ka.values, 'type': st.type.values,
                            'major': st.semi_major_km.values})
    sc = pd.read_csv(f('scada'), dtype=str, keep_default_na=False)
    sc['zone'] = sc.point.str.replace(r' (CB|ACR)$', '', regex=True)
    sc['ts'] = pd.to_datetime(sc.timestamp, format='%Y-%m-%d %H:%M:%S.%f').astype('datetime64[ns]')
    sc['amps'] = pd.to_numeric(sc.fault_current_a, errors='coerce')
    dl = pd.read_csv(f('downloads'), dtype=str, keep_default_na=False)
    dl['ts'] = pd.to_datetime(dl.controller_time, format='%d/%m/%Y %H:%M:%S.%f').astype('datetime64[ns]')
    dl['read_at'] = pd.to_datetime(dl.read_at, format='%Y-%m-%d %H:%M').astype('datetime64[ns]')
    dl['event_no'] = dl.event_no.astype(int)
    dl['ev'] = dl.event.map(DL_MAP)
    dl['amps'] = pd.to_numeric(dl.current_a, errors='coerce')
    ins = pd.read_excel(f('inspections'), header=3)
    ins['start'] = pd.to_datetime(ins['Inspection start']).astype('datetime64[ns]')
    ins['end'] = pd.to_datetime(ins['Inspection end']).astype('datetime64[ns]')
    ins['done'] = pd.to_datetime(ins['Repairs completed']).astype('datetime64[ns]')
    ins['failed'] = (ins['Ground leads missing or cut'] + ins['Arresters failed'] + ins['Pin insulators cracked']) > 0
    oms = pd.read_csv(f('oms'), dtype=str, keep_default_na=False)
    oms['t_out'] = pd.to_datetime(oms.time_out, format='%m/%d/%Y %H:%M').astype('datetime64[ns]')
    tx = pd.read_excel(f('transformers'), header=3)
    tx['date'] = pd.to_datetime(tx['Date replaced']).astype('datetime64[ns]')
    return dict(zr=zr, zones=zones, zix=zix, S=S, strokes=strokes, sc=sc, dl=dl, ins=ins, oms=oms, tx=tx)


# ------------------------------------------------------------------ R1: faults and their lightning
def device_events(L):
    """one stream of events per protective device: the historian's for SCADA devices, the controller memories read
    and de-duplicated by event number for the radio-less reclosers"""
    zix = L['zix']
    sc = L['sc']
    a = pd.DataFrame({'zone_ix': sc.zone.map(zix).values, 'ts': sc.ts.values, 'event': sc.event.values,
                      'amps': sc.amps.values, 'seq': -1})
    dl = L['dl'].drop_duplicates(['recloser', 'event_no'])
    b = pd.DataFrame({'zone_ix': dl.recloser.map(zix).values, 'ts': dl.ts.values, 'event': dl.ev.values,
                      'amps': dl.amps.values, 'seq': dl.event_no.values})
    return pd.concat([a, b], ignore_index=True).sort_values(['zone_ix', 'ts']).reset_index(drop=True)


def fault_starts(ev, gap=40.0):
    e = ev[ev.event.isin(['TRIP', 'RECLOSE', 'LOCKOUT'])].copy()
    e['prev'] = e.groupby('zone_ix').ts.shift()
    e['gap'] = (e.ts - e.prev).dt.total_seconds()
    stt = e[(e.event == 'TRIP') & (e.gap.isna() | (e.gap > gap))].copy()
    lk = e[e.event == 'LOCKOUT'][['zone_ix', 'ts']].rename(columns={'ts': 'lk_ts'}).sort_values('lk_ts')
    stt = pd.merge_asof(stt.sort_values('ts'), lk, left_on='ts', right_on='lk_ts', by='zone_ix', direction='forward',
                        tolerance=pd.Timedelta(seconds=40))
    stt['lockout'] = stt.lk_ts.notna()
    return stt[['zone_ix', 'ts', 'amps', 'lockout']].reset_index(drop=True)


def drop_sympathetic(stt, parent_ix):
    """a feeder breaker or upstream recloser tripping within 0.25 s of a recloser below it trips on the same fault"""
    stt = stt.sort_values('ts').reset_index(drop=True)
    t = stt.ts.values
    z = stt.zone_ix.values
    drop = set()
    j0 = 0
    w = np.timedelta64(250, 'ms')
    for i in range(len(stt)):
        while t[j0] < t[i] - w:
            j0 += 1
        j = j0
        while j < len(stt) and t[j] <= t[i] + w:
            if j != i and parent_ix.get(z[i], -1) == z[j]:
                drop.add(j)
            j += 1
    return stt.drop(index=sorted(drop)).reset_index(drop=True)


def near_strokes(L, rmax=0.4, excl_ic=False):
    s = L['strokes']
    g = s[s.type == 'G']
    if excl_ic:
        g = g[~((g.I > 0) & (g.I < 10))]
    idx = GEO.SegIndex(L['S'], 1.0)
    p, sg, d = idx.near(g.x.values, g.y.values, rmax)
    P = pd.DataFrame({'r': g.index.values[p], 'zone_ix': L['S'].zone_ix.values[sg], 'd': d})
    P = P.sort_values('d').drop_duplicates(['r', 'zone_ix'])
    P['t'] = s.t.values[P.r.values]
    P['I'] = s.I.values[P.r.values]
    return P.reset_index(drop=True)


def reads(L):
    """each radio-less recloser's reads (the technician's time) and the clock set that follows each"""
    zix = L['zix']
    r = L['dl'][['recloser', 'read_at']].drop_duplicates()
    return {zix[z]: np.sort(g.read_at.values) for z, g in r.groupby('recloser')}


def clock_fits(stt, NS, radioless, rd, search=900.0):
    """one drift rate per radio-less controller and an offset for each period between reads: the rate that lines up
    the most fault starts with a ground stroke near the zone, refined by least squares on the lined-up pairs"""
    fits = {}
    for z in radioless:
        sets = rd.get(z, np.array([], dtype='datetime64[ns]'))
        sz = stt[stt.zone_ix == z]
        ns = np.sort(NS[NS.zone_ix == z].t.values)
        if len(sz) == 0 or len(sets) == 0:
            continue
        k = np.searchsorted(sets, sz.ts.values, side='right') - 1
        tau = np.where(k >= 0, (sz.ts.values - sets[np.clip(k, 0, None)]).astype('timedelta64[ns]').astype(np.int64) / 86400e9, np.nan)
        Dd, T, K = [], [], []
        for tt, ta, kk in zip(sz.ts.values, tau, k):
            lo, hi = np.searchsorted(ns, [tt - np.timedelta64(int(search), 's'), tt + np.timedelta64(int(search), 's')])
            if hi > lo:
                d = (tt - ns[lo:hi]).astype('timedelta64[ns]').astype(np.int64) / 1e9
                Dd.append(d)
                T.append(np.full(len(d), ta))
                K.append(np.full(len(d), kk))
        if not Dd:
            continue
        Dd = np.concatenate(Dd)
        T = np.concatenate(T)
        K = np.concatenate(K)
        kn = K >= 0
        best = (-1, 0.0)
        for b in np.arange(-5.0, 5.0001, 0.005):
            n = np.sum(np.abs(Dd[kn] - b * T[kn]) <= 3.0)
            if n > best[0]:
                best = (n, b)
        b = best[1]
        a_k = {}
        for tol in (3.0, 1.0, 0.6):
            r = Dd - b * np.nan_to_num(T)
            inl = kn & (np.abs(r - np.array([a_k.get(x, 0.0) for x in K])) <= tol)
            if inl.sum() < 3:
                break
            ks = np.unique(K[inl])
            X = np.zeros((inl.sum(), len(ks) + 1))
            for j, x in enumerate(ks):
                X[K[inl] == x, j] = 1.0
            X[:, -1] = T[inl]
            coef = np.linalg.lstsq(X, Dd[inl], rcond=None)[0]
            a_k = {x: coef[j] for j, x in enumerate(ks)}
            b = coef[-1]
        fits[z] = (b, a_k, sets)
    return fits


def offsets(stt, fits):
    o = np.zeros(len(stt))
    for i, (z, t) in enumerate(zip(stt.zone_ix.values, stt.ts.values)):
        if z not in fits:
            continue
        b, a_k, sets = fits[z]
        k = np.searchsorted(sets, t, side='right') - 1
        if k < 0:
            o[i] = np.nan
            continue
        o[i] = a_k.get(k, 0.0) + b * ((t - sets[k]) / np.timedelta64(1, 'D'))
    return o


def match(stt, NS, off, win, rmax):
    s = stt.copy()
    s['tcorr'] = s.ts - pd.to_timedelta(np.nan_to_num(off, nan=1e7), unit='s')
    g = NS[NS.d <= rmax][['zone_ix', 't', 'I']].sort_values('t').rename(columns={'t': 'st_t', 'I': 'st_I'})
    lo, hi = win
    m = pd.merge_asof(s.sort_values('tcorr'), g, left_on='tcorr', right_on='st_t', by='zone_ix', direction='nearest',
                      tolerance=pd.Timedelta(seconds=max(abs(lo), hi) + 0.001))
    dt = (m.tcorr - m.st_t).dt.total_seconds()
    m['lightning'] = m.st_t.notna() & (dt >= lo) & (dt <= hi)
    m['season'] = season_of(m.ts.values)
    return m


# ------------------------------------------------------------------ R2: what the radio-less memories did not keep
def coverage(L):
    """observed windows of each radio-less recloser: each read covers from its oldest kept event (when events were
    overwritten since the last read, shown by a jump in the event numbers) or from the last read, to the read"""
    zix = L['zix']
    dl = L['dl']
    out = {}
    for z, g in dl.groupby('recloser'):
        wins = []
        prev_max, prev_read = None, None
        for (ra,), gg in g.groupby(['read_at']):
            mn = gg.event_no.min()
            first_t = gg.loc[gg.event_no.idxmin(), 'ts']
            if prev_max is None or mn > prev_max + 1:
                start = first_t
                lost = 0 if prev_max is None else int(mn - prev_max - 1)
            else:
                start = prev_read
                lost = 0
            wins.append((start, ra, lost))
            prev_max = max(prev_max or 0, gg.event_no.max())
            prev_read = ra
        out[zix[z]] = wins
    return out


# ------------------------------------------------------------------ the whole chain
def covariates(L):
    zr = L['zr']
    km = zr['Overhead line km, three-phase'] + zr['Overhead line km, single-phase']
    cv = pd.DataFrame(index=range(len(zr)))
    cv['sh_treed'] = zr['km tree-lined'] / km
    cv['sh_town'] = zr['km town'] / km
    cv['sh_hill'] = zr['km hill'] / km
    cv['sh_steel'] = zr['km steel crossarm'] / km
    cv['sh_bracket'] = zr['km pole-top bracket'] / km
    cv['sh_concrete'] = zr['km bracket on concrete pole'] / km
    cv['prot'] = zr['km fitted with line arresters (2015-16 programme)'] / km
    cv['tx_km'] = zr['Distribution transformers'] / km
    return cv


def stroke_expectation(NSs, mo, DF, fitset, cols, cv):
    """each zone-season's sound expectation summed stroke by stroke: a logistic chance per located ground stroke
    on log current and log distance with the zone's features, fitted on the strokes of the confirmed-sound
    zone-seasons; returns (observed-months expectation, full-season expectation) aligned to DF's rows"""
    hit = mo[mo.lightning & mo.st_t.notna()][['zone_ix', 'st_t']].drop_duplicates()
    key = set(zip(hit.zone_ix.values, hit.st_t.values.astype('datetime64[ns]').astype(np.int64)))
    S = NSs[NSs.season > 0].copy()
    tk = S.t.values.astype('datetime64[ns]').astype(np.int64)
    S['hit'] = [(z, t) in key for z, t in zip(S.zone_ix.values, tk)]
    S['lI'] = np.log(np.maximum(np.abs(S.I.values), 1.0))
    S['ld'] = np.log(np.maximum(S.d.values, 0.005))
    feat = ['lI', 'ld'] + list(cols)
    S = S.join(cv[list(cols)], on='zone_ix')
    fs = set(DF[fitset].index.tolist()) if isinstance(DF.index, pd.MultiIndex) else \
        set(zip(DF[fitset].zone_ix.values, DF[fitset].season.values))
    sel = np.array([(z, s) in fs for z, s in zip(S.zone_ix.values, S.season.values)]) & S.obs.values
    Xa = np.c_[np.ones(len(S)), S[feat].values.astype(float)]
    Xf, yf = Xa[sel], S.hit.values[sel].astype(float)

    def nll(b):
        eta = Xf @ b
        return -(yf * eta - np.logaddexp(0, eta)).sum()

    def gr(b):
        return -Xf.T @ (yf - 1 / (1 + np.exp(-(Xf @ b))))
    b0 = np.zeros(Xf.shape[1])
    b0[0] = math.log(max(yf.mean(), 1e-4) / (1 - max(yf.mean(), 1e-4)))
    bb = optimize.minimize(nll, b0, jac=gr, method='BFGS', options={'gtol': 1e-7, 'maxiter': 3000}).x
    S['p'] = 1 / (1 + np.exp(-(Xa @ bb)))
    e_obs = S[S.obs].groupby(['zone_ix', 'season']).p.sum()
    e_all = S.groupby(['zone_ix', 'season']).p.sum()
    if isinstance(DF.index, pd.MultiIndex):
        ix = DF.index
    else:
        ix = pd.MultiIndex.from_arrays([DF.zone_ix.values, DF.season.values])
    return e_obs.reindex(ix, fill_value=0.0).values, e_all.reindex(ix, fill_value=0.0).values


def fit_poisson(df, cols):
    df = df[df.xo > 0]
    X = np.c_[np.ones(len(df)), df[cols].values]
    off = np.log(df.xo.values)
    y = df.y.values

    def nll(b):
        eta = X @ b + off
        return -(y * eta - np.exp(eta)).sum()

    def gr(b):
        return -X.T @ (y - np.exp(X @ b + off))
    b0 = np.zeros(X.shape[1])
    b0[0] = np.log(max(y.sum(), 1) / df.xo.sum())
    return optimize.minimize(nll, b0, jac=gr, method='BFGS', options={'gtol': 1e-8, 'maxiter': 2000}).x


def nb_k(y, mu):
    def nll(lk):
        k = math.exp(lk)
        return -stats.nbinom.logpmf(y, k, k / (k + mu)).sum()
    return math.exp(optimize.minimize_scalar(nll, bounds=(math.log(0.5), math.log(1e5)), method='bounded',
                                             options={'xatol': 1e-6}).x)


def nb_tail(x, mu, k):
    if k >= 1e8:
        return stats.poisson.sf(x - 1, mu)
    return stats.nbinom.sf(x - 1, k, k / (k + mu))


# ------------------------------------------------------------------ the two-level sound model
UGRID = np.exp(np.linspace(np.log(0.03), np.log(12.0), 361))
LOG_DU = np.log(np.gradient(UGRID))


def _nb_logpmf(y, mu, k):
    from scipy.special import gammaln
    return gammaln(y + k) - gammaln(k) - gammaln(y + 1) + k * np.log(k / (k + mu)) + y * np.log(mu / (k + mu))


def _gamma_logpdf(u, a):
    from scipy.special import gammaln
    return a * np.log(a) - gammaln(a) + (a - 1) * np.log(u) - a * u


def fit_levels(groups, start=(4.0, 20.0)):
    """the zones' own sound levels (a gamma of shape a around the register-feature rate) and the season-to-season
    scatter (a negative binomial of size k), by marginal likelihood over each zone's confirmed-sound seasons"""
    def nll(th):
        a, k = np.exp(np.clip(th, -3, 9))
        lg = _gamma_logpdf(UGRID, a) + LOG_DU
        tot = 0.0
        for y, e in groups:
            lp = _nb_logpmf(y[:, None], e[:, None] * UGRID[None, :], k).sum(0) + lg
            m = lp.max()
            tot += m + np.log(np.exp(lp - m).sum())
        return -tot
    r = optimize.minimize(nll, np.log(start), method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-7,
                                                                              'maxiter': 4000})
    a, k = np.exp(np.clip(r.x, -3, 9))
    return float(a), float(k), float(-r.fun)


def level_ll(groups, a, k):
    lg = _gamma_logpdf(UGRID, a) + LOG_DU
    tot = 0.0
    for y, e in groups:
        lp = _nb_logpmf(y[:, None], e[:, None] * UGRID[None, :], k).sum(0) + lg
        m = lp.max()
        tot += m + np.log(np.exp(lp - m).sum())
    return float(tot)


def level_ci(groups, a, k, ll):
    """the shape's 95 per cent profile interval (the season scatter held at its fit)"""
    out = []
    for side in (-1, 1):
        lo, hi = 0.0, 3.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if ll - level_ll(groups, a * math.exp(side * mid), k) > 1.92:
                hi = mid
            else:
                lo = mid
        out.append(a * math.exp(side * lo))
    return out[0], out[1]


def level_weights(y, e, a, k):
    """a zone's own level on the grid, given the confirmed-sound seasons it may learn from"""
    lw = _gamma_logpdf(UGRID, a) + LOG_DU
    if len(y):
        lw = lw + _nb_logpmf(np.asarray(y, float)[:, None], np.asarray(e, float)[:, None] * UGRID[None, :], k).sum(0)
    w = np.exp(lw - lw.max())
    return w / w.sum()


def pred_sf(y, w, M, e2, k):
    """P(the record's faults >= y) under sound protection: a negative binomial sum over the record's seasons, mixed
    over the zone's own level"""
    kW = k * M * M / max(e2, 1e-12)
    mu = UGRID * M
    return float((w * stats.nbinom.sf(y - 1, kW, kW / (kW + mu))).sum())


def pred_threshold_tail(w, M, e2, k, alpha):
    """the smallest count the rule refers at, and the chance a sound zone reaches it"""
    kW = k * M * M / max(e2, 1e-12)
    mu = UGRID * M
    hi = int(max(30, 12 * M + 60))
    while True:
        ys = np.arange(hi + 1)
        pm = (w[:, None] * stats.nbinom.pmf(ys[None, :], kW, kW / (kW + mu[:, None]))).sum(0)
        sf = 1 - np.concatenate([[0.0], np.cumsum(pm)[:-1]])
        ok = np.nonzero(sf < alpha)[0]
        if len(ok):
            c = int(ok[0])
            return c, float(max(sf[c], 0.0))
        hi *= 2


def run(target, opt=None, L=None):
    o = dict(DEFAULT)
    o.update(opt or {})
    L = L or load(target)
    zr = L['zr']
    N = len(zr)
    zix = L['zix']
    parent_ix = {zix[z]: zix.get(p, -1) for z, p in zip(zr.zone, zr['Upstream device'].fillna(''))}
    radioless = [zix[z] for z, t in zip(zr.zone, zr.Telemetry) if str(t).startswith('None')]
    ev = device_events(L)
    if not o['match_dedupe']:
        dl = L['dl']
        b = pd.DataFrame({'zone_ix': dl.recloser.map(zix).values, 'ts': dl.ts.values, 'event': dl.ev.values,
                          'amps': dl.amps.values, 'seq': dl.event_no.values})
        ev = pd.concat([ev[ev.seq < 0], b], ignore_index=True).sort_values(['zone_ix', 'ts']).reset_index(drop=True)
    stt = drop_sympathetic(fault_starts(ev), parent_ix)
    NS = near_strokes(L, max(o['rmax'], o.get('rexp') or 0.4, 0.4), o['excl_ic'])
    rd = reads(L)
    if o['clock'] == 'aligned':
        fits = clock_fits(stt, NS, radioless, rd)
        off = offsets(stt, fits)
    elif o['clock'] == 'constant':
        # one fixed offset per controller: the most common lag between its trips and nearby strokes
        off = np.zeros(len(stt))
        for z in radioless:
            sel = (stt.zone_ix == z).values
            ns = np.sort(NS[NS.zone_ix == z].t.values)
            ds = []
            for tt in stt.ts.values[sel]:
                lo, hi = np.searchsorted(ns, [tt - np.timedelta64(900, 's'), tt + np.timedelta64(900, 's')])
                ds += list((tt - ns[lo:hi]).astype('timedelta64[ns]').astype(np.int64) / 1e9)
            if ds:
                h, e = np.histogram(ds, bins=np.arange(-900, 901, 2.0))
                off[sel] = e[h.argmax()] + 1.0
        fits = {}
    else:
        off = np.zeros(len(stt))
        fits = {}
    if o['clock'] == 'wide':
        # the controllers with no radio link matched on a wide window around their own stamps, no offset fitted
        rl_sel = stt.zone_ix.isin(radioless).values
        m = pd.concat([match(stt[~rl_sel], NS, off[~rl_sel], o['win'], o['rmax']),
                       match(stt[rl_sel], NS, off[rl_sel], o['wide_win'], o['rmax'])], ignore_index=True)
        m = m.sort_values(['zone_ix', 'ts']).reset_index(drop=True)
    else:
        m = match(stt, NS, off, o['win'], o['rmax'])
    cov = coverage(L)
    # exposure: ground strokes reported near each zone, per season, all and inside the observed windows
    NSs = NS[NS.d <= (o.get('rexp') or o['rmax'])].copy()
    NSs['season'] = season_of(NSs.t.values)
    NSs['obs'] = True
    for z, wins in cov.items():
        sel = (NSs.zone_ix == z).values
        tt = NSs.t.values[sel]
        ok = np.zeros(len(tt), bool)
        for a0, a1, lost in wins:
            ok |= (tt >= np.datetime64(a0)) & (tt <= np.datetime64(a1))
        NSs.loc[sel, 'obs'] = ok
    mo = m.copy()
    mo['obs'] = True
    for z, wins in cov.items():
        sel = (mo.zone_ix == z).values
        tt = mo.ts.values[sel]
        ok = np.zeros(len(tt), bool)
        for a0, a1, lost in wins:
            ok |= (tt >= np.datetime64(a0) - np.timedelta64(400, 's')) & (tt <= np.datetime64(a1) + np.timedelta64(400, 's'))
        mo.loc[sel, 'obs'] = ok
    idx = range(N)
    O = mo[mo.lightning & (mo.season > 0)].groupby(['zone_ix', 'season']).size().unstack(fill_value=0).reindex(index=idx, columns=ALL, fill_value=0)
    X = NSs[NSs.season > 0].groupby(['zone_ix', 'season']).size().unstack(fill_value=0).reindex(index=idx, columns=ALL, fill_value=0)
    Xo = NSs[(NSs.season > 0) & NSs.obs].groupby(['zone_ix', 'season']).size().unstack(fill_value=0).reindex(index=idx, columns=ALL, fill_value=0)
    if not o['fill']:
        Xo = X.copy()
    cv = covariates(L)
    cols = list(cv.columns)
    if o['spec'] == 'notx':
        cols = [c for c in cols if c != 'tx_km']
    elif o['spec'] == 'prot':
        cols = ['prot']
    elif o['spec'] == 'none':
        cols = []
    if o.get('cols') is not None:
        cols = list(o['cols'])
    ins = L['ins']
    ins['zone_ix'] = ins.Zone.map(zix)
    # verified sound: whole seasons after a zone's previous inspection and before an inspection that found nothing
    ver = set()
    verd = {}
    post = set()
    bad = set()
    for z, g in ins.sort_values('start').groupby('zone_ix'):
        g = g.reset_index(drop=True)
        for i, r in g.iterrows():
            prev_done = g.done[i - 1] if i > 0 else pd.Timestamp('2016-01-01')
            for s in ALL:
                s0, s1 = pd.Timestamp('%d-04-01' % s), pd.Timestamp('%d-10-31' % s)
                if not r.failed and s1 < r.start and s0 > prev_done:
                    ver.add((z, s))
                    verd[(z, s)] = r.done
                if r.failed and s1 < r.start and s0 > prev_done:
                    bad.add((z, s))
            nxt = [s for s in ALL if pd.Timestamp('%d-04-01' % s) > r.done]
            if nxt:
                post.add((z, nxt[0]))
    rows = [(z, s, O.loc[z, s], Xo.loc[z, s], X.loc[z, s], (z, s) in ver, (z, s) in post, (z, s) in bad)
            for z in idx for s in ALL]
    DF = pd.DataFrame(rows, columns=['zone_ix', 'season', 'y', 'xo', 'x', 'ver', 'post', 'bad']).join(cv, on='zone_ix')
    if o['null'] == 'verified':
        fitset = DF.ver
    elif o['null'] == 'verified_post':
        fitset = DF.ver | DF.post
    elif o['null'] == 'post':
        fitset = DF.post
    elif o['null'] == 'not_failed':
        # every zone-season no inspection has yet found failed: the seasons since each zone's last inspection count
        fitset = ~DF.bad
    else:
        fitset = pd.Series(True, index=DF.index)
    b = fit_poisson(DF[fitset], cols)
    rate = np.exp(np.c_[np.ones(len(DF)), DF[cols].values] @ b)
    DF['E'] = rate * DF.xo
    DF['Ef'] = rate * DF.x
    if o.get('rate_scale'):
        # a perturbation of the fitted sound rate (forcing: each fitted input moved by its defensible spread)
        DF['E'] = DF['E'] * float(o['rate_scale'])
        DF['Ef'] = DF['Ef'] * float(o['rate_scale'])
    if o.get('expo') == 'stroke':
        # a stroke-level sound model: each located stroke's chance of faulting the zone from its current and its
        # distance to the lines, with the register's features, fitted on the confirmed-sound zone-seasons
        DF['E'], DF['Ef'] = stroke_expectation(NSs, mo, DF, fitset, cols, cv)
    fs = DF[fitset & (DF.E > 0)]
    if o['kfit'] == 'moments':
        k = float((fs.E ** 2).sum() / max(((fs.y - fs.E) ** 2 - fs.y).sum(), 1e-9)) * o['k_scale']
    else:
        k = nb_k(fs.y.values, fs.E.values) * o['k_scale']
    if o['disp'] == 'poisson':
        k = 1e9
    DF = DF.set_index(['zone_ix', 'season'])
    # R2 fill: a zone-season's unread or overwritten part at the rate its read part ran
    DF['yf'] = np.where(DF.E > 0, DF.y * DF.Ef / DF.E.where(DF.E > 0, 1), DF.y)
    if not o['fill']:
        DF['yf'] = DF.y
    alpha = 1.0 / (N * o['budget_seasons'])
    last_done = {}
    for z, g in ins.groupby('zone_ix'):
        last_done[z] = np.sort(g.done.values)

    def window(z, s):
        if o['window'] == 'whole':
            return [x for x in ALL if x <= s]
        if o['window'] == 'season':
            return [s]
        ld = last_done.get(z, np.array([], dtype='datetime64[ns]'))
        ld = ld[ld < np.datetime64('%d-04-01' % s)]
        last = ld.max() if len(ld) else np.datetime64('2016-01-01')
        return [x for x in ALL if x <= s and np.datetime64('%d-04-01' % x) > last]

    if o.get('fill_rate') == 'window' and o['fill']:
        # a restoration rival: a zone-season's unread or overwritten part at the zone's rate over its record since
        # inspection (its observed months), not the same season's
        for z in idx:
            for x in ALL:
                e_, ef_ = DF.loc[(z, x), 'E'], DF.loc[(z, x), 'Ef']
                if ef_ > e_:
                    W = window(z, x)
                    yw = sum(DF.loc[(z, w_), 'y'] for w_ in W)
                    ew = sum(DF.loc[(z, w_), 'E'] for w_ in W)
                    if ew > 0:
                        DF.loc[(z, x), 'yf'] = DF.loc[(z, x), 'y'] + yw / ew * (ef_ - e_)

    # the two-level sound model: each zone's own level, learned from its confirmed-sound seasons
    zone_model = o['null_model'] == 'zone' and o['disp'] not in ('poisson', 'quasi', 'nb_seasons')
    fsq = DF[DF.ver & (DF.E > 0)]
    phi_q = float((((fsq.y - fsq.E) ** 2) / fsq.E).sum() / max(len(fsq) - len(cols) - 1, 1))
    if zone_model:
        groups = []
        for z in idx:
            vs = [x for x in ALL if DF.loc[(z, x), 'ver'] and DF.loc[(z, x), 'E'] > 0]
            if vs:
                groups.append((np.array([DF.loc[(z, x), 'y'] for x in vs], float),
                               np.array([DF.loc[(z, x), 'E'] for x in vs], float)))
        a_lv, k_lv, ll_lv = fit_levels(groups)
        lv_groups = groups
        if o.get('a_fix'):
            a_lv = float(o['a_fix'])
        if o.get('klv_scale'):
            k_lv = k_lv * float(o['klv_scale'])
    else:
        a_lv, k_lv, ll_lv, lv_groups = None, k, None, []

    def own_seasons(z, W, s_run=None):
        vs = [x for x in ALL if DF.loc[(z, x), 'ver'] and DF.loc[(z, x), 'E'] > 0]
        if o.get('asof') and s_run is not None:
            # the rule as run after season s_run knows only the inspections completed by then
            cut = pd.Timestamp('%d-11-01' % s_run)
            vs = [x for x in vs if verd[(z, x)] < cut]
        if o['own'] == 'outside':
            vs = [x for x in vs if x not in W]
        elif o['own'] == 'none':
            vs = []
        return vs

    def weights(z, W, s_run=None):
        vs = own_seasons(z, W, s_run)
        return level_weights([DF.loc[(z, x), 'y'] for x in vs], [DF.loc[(z, x), 'E'] for x in vs], a_lv, k_lv)

    pred = {}

    def refer(s):
        out = []
        for z in idx:
            W = window(z, s)
            if not W:
                continue
            if o.get('test') == 'restored':
                yv = int(round(sum(DF.loc[(z, x), 'yf'] for x in W)))
                es = [float(DF.loc[(z, x), 'Ef']) for x in W]
            else:
                yv = int(sum(DF.loc[(z, x), 'y'] for x in W))
                es = [float(DF.loc[(z, x), 'E']) for x in W]
            ev_ = float(sum(es))
            if ev_ <= 0:
                continue
            if zone_model:
                w = weights(z, W, s)
                e2 = float(sum(e * e for e in es))
                p = pred_sf(yv, w, ev_, e2, k_lv)
                if o.get('level') == 'plugin':
                    # the zone's level taken as known: its posterior mean, the seasons' scatter alone
                    u = float((w * UGRID).sum())
                    p = nb_tail(yv, u * ev_, k_lv * ev_ * ev_ / max(e2, 1e-12))
                pred[(s, z)] = (w, ev_, e2)
                eown = float((w * UGRID).sum()) * ev_
            elif o['disp'] == 'quasi':
                # a quasi-Poisson scatter: the variance a constant multiple of the mean, season by season
                phi = max(phi_q, 1.0 + 1e-6)
                kq = ev_ / (phi - 1.0)
                p = nb_tail(yv, ev_, kq)
                eown = ev_
            elif o['disp'] == 'nb_seasons':
                # each season's scatter a negative binomial of the pooled size, the record's seasons independent
                e2 = float(sum(e * e for e in es))
                p = nb_tail(yv, ev_, k * ev_ * ev_ / max(e2, 1e-12))
                eown = ev_
            else:
                p = nb_tail(yv, ev_, k)
                eown = ev_
            out.append((z, yv, ev_, eown, p, len(W)))
        T = pd.DataFrame(out, columns=['zone_ix', 'y', 'E', 'E_own', 'p', 'nwin'])
        T['referred'] = T.p < alpha
        return T
    hist = {s: refer(s) for s in SEASONS}
    T26 = hist[2026]
    ref = sorted(T26[T26.referred].zone_ix.tolist())
    alerts = {s: int(hist[s].referred.sum()) for s in SEASONS}

    # R6: expected sound zones referred in a season: the null tail at each zone's threshold, summed
    def exp_false(s, T, true_tail=False):
        tot = 0.0
        for r in T.itertuples():
            if zone_model:
                w, M, e2 = pred[(s, r.zone_ix)]
                if o.get('level') == 'plugin':
                    # the known-level rule's threshold; its own claim, or its chance under the level as uncertain
                    # as the zone's confirmed seasons leave it
                    u = float((w * UGRID).sum())
                    kW = k_lv * M * M / max(e2, 1e-12)
                    lo, hi = 0, int(max(20, u * M * 8 + 60))
                    while lo < hi:
                        mid = (lo + hi) // 2
                        if nb_tail(mid, u * M, kW) < alpha:
                            hi = mid
                        else:
                            lo = mid + 1
                    tot += pred_sf(lo, w, M, e2, k_lv) if true_tail else nb_tail(lo, u * M, kW)
                    continue
                tot += pred_threshold_tail(w, M, e2, k_lv, alpha)[1]
                continue
            lo, hi = 0, int(max(20, r.E * 6 + 40))
            while lo < hi:
                mid = (lo + hi) // 2
                if nb_tail(mid, r.E, k) < alpha:
                    hi = mid
                else:
                    lo = mid + 1
            tot += nb_tail(lo, r.E, k)
        return tot
    false_per = float(np.mean([exp_false(s, hist[s]) for s in SEASONS]))
    # the same rule's sound referrals with each zone's level as uncertain as its confirmed seasons leave it
    false_true = (float(np.mean([exp_false(s, hist[s], True) for s in SEASONS]))
                  if zone_model and o.get('level') == 'plugin' else false_per)

    # R7: each cyclic round in the record against the rule after the season before it
    val = []
    for r in ins[(ins.start >= '2022-11-01') & (ins.start < '2026-06-01')].itertuples():
        s = r.start.year if r.start.month >= 11 else r.start.year - 1
        T = hist.get(s)
        if T is None:
            continue
        row = T[T.zone_ix == r.zone_ix]
        refd = bool(row.referred.iat[0]) if len(row) else False
        val.append((r.zone_ix, s, refd, bool(r.failed)))
    V = pd.DataFrame(val, columns=['zone_ix', 'season', 'referred', 'failed'])
    v_ref = int(V.referred.sum())
    v_conf = int((V.referred & V.failed).sum())
    v_fail = int(V.failed.sum())
    v_miss = int((~V.referred & V.failed).sum())

    # R3: the 2026 season with every zone sound, each at its own level (its confirmed seasons all lie before its
    # last inspection)
    Eu = {}
    for z in idx:
        Eu[z] = float((weights(z, []) * UGRID).sum()) if zone_model else 1.0
    y26 = DF.xs(2026, level='season')
    sound26 = float(sum(Eu[z] * y26.loc[z, 'Ef'] for z in idx))
    obs26 = float(y26.yf.sum())
    # R8: what the refit avoids: the faults its zones ran above their own sound level in the last season, taken
    # at the lightning of an average 2022-2026 season
    avoided = {}
    for z in ref:
        xbar = float(np.mean([DF.loc[(z, x), 'x'] for x in SEASONS]))
        x26 = float(DF.loc[(z, 2026), 'x'])
        if o['avoided'] == 'last_season':
            avoided[z] = (DF.loc[(z, 2026), 'yf'] - Eu[z] * DF.loc[(z, 2026), 'Ef']) * (xbar / x26 if x26 > 0 else 0.0)
        elif o['avoided'] == 'post_onset':
            # the seasons since the zone's failure began: the split of its record since inspection that a two-ratio
            # Poisson likelihood prefers, the excess ratio after it, at the zone's own sound level in an average season
            W = window(z, 2026)
            yv = np.array([DF.loc[(z, x), 'yf'] for x in W], float)
            ev = np.array([Eu[z] * DF.loc[(z, x), 'Ef'] for x in W], float)
            best, bi = -np.inf, 0
            for i in range(len(W)):
                ll = 0.0
                for yy, ee in ((yv[:i], ev[:i]), (yv[i:], ev[i:])):
                    if len(yy) and ee.sum() > 0:
                        th = max(yy.sum(), 1e-9) / ee.sum()
                        ll += float((yy * np.log(th * ee) - th * ee).sum())
                if ll > best:
                    best, bi = ll, i
            rate26 = DF.loc[(z, 2026), 'Ef'] / x26 if x26 > 0 else 0.0
            avoided[z] = (yv[bi:].sum() / max(ev[bi:].sum(), 1e-12) - 1) * Eu[z] * rate26 * xbar
        else:
            W = window(z, 2026)
            yv = sum(DF.loc[(z, x), 'y'] for x in W)
            ev_ = sum(DF.loc[(z, x), 'E'] for x in W)
            ebar = float(np.mean([DF.loc[(z, x), 'Ef'] for x in SEASONS]))
            avoided[z] = (yv / ev_ - 1) * ebar
    season_tot = {s: float(DF.xs(s, level='season').yf.sum()) for s in SEASONS}
    rl = [z for z in idx if z in set(radioless)]
    radioless26 = float(DF.loc[[(z, 2026) for z in rl], 'yf'].sum())
    return dict(L=L, opt=o, N=N, zones=L['zones'], radioless=radioless, stt=stt, m=mo, NS=NS, fits=fits, cov=cov,
                DF=DF, b=b, cols=cols, k=k, a_lv=a_lv, k_lv=k_lv, ll_lv=ll_lv, Eu=Eu, zone_model=zone_model,
                lv_groups=lv_groups, phi_q=phi_q,
                alpha=alpha, hist=hist, ref=ref, ref_names=[L['zones'][z] for z in ref],
                alerts=alerts, false_per=false_per, false_true=false_true, V=V, v_ref=v_ref, v_conf=v_conf, v_fail=v_fail, v_miss=v_miss,
                sound26=sound26, obs26=obs26, excess26=obs26 - sound26, avoided=avoided,
                avoided_total=float(sum(avoided.values())), season_tot=season_tot, radioless26=radioless26,
                window=window)

