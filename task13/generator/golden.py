"""The golden analysis, from the pack alone (analysis.Pack), result by result:

R1  customers FLISR restored within five minutes of the first loss of supply, each year 2022 to 2026 (2026 to the
    end of October): every automatic restoration the devices' own event record shows, the ones the archive lost
    on storm days included, timed from the lockout device's first trip to the ADMS close;
R2  2026's walk from the dashboard's "CI saved" to the order's customer interruptions avoided: the restorations
    the archive lost, those that took five minutes or more, the restored customers a receiving recloser's trip
    then put out again, and the receiving feeders' own customers those trips and the closes onto faults put out;
R3  the recloser controls whose batteries will not carry a trip or close at the design minimum by the end of
    February 2027, from each battery's weekly load tests against the airport temperature at the test hour;
R4  the receiving feeders' customers the summer 2027 transfers would interrupt (June to September) if the transfer
    settings stand, with the four reinforcements carried at the completion the capital works record supports and
    the approved large load;
R5  2027's customer interruptions avoided if the schemes are operated as they stand, with its 80 per cent range.
"""
import datetime as dt
import json
import math
import os

import numpy as np
import pandas as pd

import analysis as A

UTC = dt.timezone.utc
FIVE_MIN = 300.0
V_MIN, TEST_A, OP_A = 21.2, 5.0, 30.0
DESIGN_C = -27.0
WINTER_END = pd.Timestamp('2027-02-28', tz='UTC')


# ------------------------------------------------------------------------------------------- operations (R1)

def lockouts(P):
    """every lockout of a loop feeder's breaker or midline recloser, with its first trip, from the device record"""
    d = P.devents
    lf = set(P.loop_of_feeder)
    rows = []
    trips = d[d['Event'] == 'TRIP']
    for _, r in d[d['Event'] == 'LOCKOUT'].iterrows():
        f = r['feeder']
        if f not in lf:
            continue
        dev = r['Device']
        kind = 'CB' if dev.endswith(' CB') else P.dev[dev]['Position'][-1]
        kind = kind if kind == 'CB' else 'R' + kind
        tt = trips[(trips['Device'] == dev) & (trips['t'] <= r['t']) & (trips['t'] >= r['t'] - pd.Timedelta(minutes=3))]
        first = tt['t'].min() if len(tt) else r['t'] - pd.Timedelta(seconds=40)
        rows.append({'feeder': f, 'loop': P.loop_of_feeder[f], 'device': dev, 'kind': kind, 't_lo': r['t'],
                     't_first': first})
    return pd.DataFrame(rows).sort_values('t_lo').reset_index(drop=True)


def operations(P):
    """each lockout on a loop in service, and what the scheme did, read from the device record (and the archive and
    the outage record where they hold it)"""
    d = P.devents
    lo = lockouts(P)
    lo = lo[lo.apply(lambda r: r['t_lo'].date() >= P.in_service[r['loop']], axis=1)].reset_index(drop=True)
    adms_close = d[(d['Event'] == 'CLOSE') & (d['Source'] == 'ADMS')]
    adms_open = d[(d['Event'] == 'OPEN') & (d['Source'] == 'ADMS')]
    trips = d[d['Event'] == 'TRIP']
    oms = P.oms
    auto = oms[oms['Step Type'] == 'Automatic']
    starts = P.adms[P.adms['kind'] == 'START']
    out = []
    for _, r in lo.iterrows():
        f, lid = r['feeder'], r['loop']
        b = P.partner[f]
        tie = P.tie[lid]
        nxt = lo[(lo['loop'] == lid) & (lo['t_lo'] > r['t_lo'])]['t_lo']
        w0 = r['t_lo']
        w1 = min(r['t_lo'] + pd.Timedelta(minutes=60), nxt.min() if len(nxt) else r['t_lo'] + pd.Timedelta(minutes=60))
        opened = adms_open[(adms_open['t'] >= w0) & (adms_open['t'] <= w1) & (adms_open['feeder'] == f)]
        iso = None
        if len(opened):
            kinds = sorted(P.dev[x]['Position'][-1] for x in opened['Device'])
            iso = 'R' + kinds[-1]
        cl = adms_close[(adms_close['t'] >= w0) & (adms_close['t'] <= w1)]
        tie_cl = cl[cl['Device'] == tie]
        cb_cl = cl[cl['Device'] == f + ' CB']
        rec = {'feeder': f, 'loop': lid, 'recv': b, 'device': r['device'], 'kind': r['kind'], 't_lo': r['t_lo'],
               't_first': r['t_first'], 'iso': iso, 'restored': 0, 'restored_5': 0, 'secs': 0.0, 'upstream': 0,
               'tie_close': None, 'recv_trip_on_close': False, 'in_archive': False}
        # the archive's own sequence for this lockout, if it kept it
        st = starts[(starts['loop'] == lid) & (starts['t'] >= w0 - pd.Timedelta(seconds=5)) & (starts['t'] <= w1)]
        rec['in_archive'] = bool(len(st))
        # the outage record's automatic steps for the outage this lockout opened
        o = oms[(oms['Interrupting Device'] == r['device']) & ((oms['start'] - r['t_first']).abs() < pd.Timedelta(minutes=40))]
        oid = o['Outage ID'].iloc[0] if len(o) else None
        rec['oms_id'] = oid
        a_steps = auto[auto['Outage ID'] == oid] if oid is not None else auto.iloc[0:0]
        if len(tie_cl):
            tc = tie_cl['t'].iloc[0]
            rec['tie_close'] = tc
            # a receiving recloser that trips the instant the tie closes: the transferred part held the fault
            rt = trips[(trips['feeder'] == b) & (trips['t'] >= tc) & (trips['t'] <= tc + pd.Timedelta(seconds=3))]
            if len(rt):
                rec['recv_trip_on_close'] = True
            else:
                secs = [2, 3] if iso == 'R1' else [3]
                when = tc.date()
                n = sum(P.customers(f, k, when) for k in secs)
                # where the outage record has the automatic step, its count stands
                n_oms = int(a_steps['Customers Restored'].sum()) if len(a_steps) else None
                up = 0
                if len(cb_cl):
                    up = P.customers(f, 1, when)
                if n_oms is not None:
                    n = n_oms - (up if len(cb_cl) and n_oms > up else 0)
                rec['restored'] = n
                rec['secs'] = (tc - r['t_first']).total_seconds()
                rec['restored_5'] = n if rec['secs'] < FIVE_MIN else 0
        # the breaker re-closed onto the sections above an isolated fault: restored whatever became of the transfer
        if len(cb_cl) and (cb_cl['t'].iloc[0] - r['t_first']).total_seconds() < FIVE_MIN:
            if rec['restored'] or (len(tie_cl) and not rec['recv_trip_on_close']):
                rec['upstream'] = P.customers(f, 1, tie_cl['t'].iloc[0].date())
            else:
                # no transfer restored anyone: the outage record's automatic steps are the breaker's alone
                rec['upstream'] = int(a_steps['Customers Restored'].sum()) if len(a_steps) else \
                    P.customers(f, 1, cb_cl['t'].iloc[0].date())
        out.append(rec)
    return pd.DataFrame(out)


def r1_by_year(ops):
    o = ops.copy()
    o['year'] = o['t_lo'].map(lambda t: t.tz_convert(A.CENTRAL).year)
    g = o.groupby('year').apply(lambda x: int(x['restored_5'].sum() + x['upstream'].sum()), include_groups=False)
    return {int(y): int(v) for y, v in g.items()}


# ------------------------------------------------------------------------------------------------ the bridge (R2)

def receiving_trips(P, ops):
    """a receiving recloser that trips while a transfer is in place, read from the device record: the trip falls
    between the ADMS close of the tie and the operators' opening of it, on the receiving feeder"""
    d = P.devents
    tie_open = d[(d['Event'] == 'OPEN') & (d['Source'] == 'SCADA OPERATOR')]
    trips = d[(d['Event'] == 'LOCKOUT')]
    oms = P.oms
    out = []
    for _, r in ops[ops['tie_close'].notna() & ~ops['recv_trip_on_close']].iterrows():
        tie = P.tie[r['loop']]
        tc = r['tie_close']
        op = tie_open[(tie_open['Device'] == tie) & (tie_open['t'] > tc)]
        t_end = op['t'].iloc[0] if len(op) else tc + pd.Timedelta(hours=24)
        rt = trips[(trips['feeder'] == r['recv']) & (trips['t'] > tc + pd.Timedelta(seconds=5)) & (trips['t'] <= t_end)]
        rt = rt[~rt['Device'].str.endswith(' CB')]
        if not len(rt):
            continue
        dev = rt['Device'].iloc[0]
        t = rt['t'].iloc[0]
        # an overload trip draws little more than the pickup; a fault on the receiving feeder draws far more
        tr = d[(d['Event'] == 'TRIP') & (d['Device'] == dev) & (d['t'] <= t) & (d['t'] >= t - pd.Timedelta(minutes=2))]
        amps = float(tr['amps'].iloc[0]) if len(tr) else float('nan')
        if not amps < 2.0 * float(P.dev[dev]['Phase pickup group 1 (A)']):
            continue
        o = oms[(oms['Interrupting Device'] == dev) & ((oms['start'] - t).abs() < pd.Timedelta(minutes=30))]
        own = None
        if len(o):
            first = o.sort_values('Step').iloc[0]
            own = int(first['Customers Restored'])
            tot = int(first['Customers Interrupted'])
        out.append({'loop': r['loop'], 'from': r['feeder'], 'to': r['recv'], 'device': dev, 't': t, 'own': own,
                    'restored_before': int(r['restored_5']), 'year': t.tz_convert(A.CENTRAL).year,
                    'hours_after': (t - tc).total_seconds() / 3600})
    return pd.DataFrame(out)


def closes_onto_fault(P, ops):
    oms = P.oms
    out = []
    for _, r in ops[ops['recv_trip_on_close']].iterrows():
        o = oms[(oms['Feeder'] == r['recv']) & ((oms['start'] - r['tie_close']).abs() < pd.Timedelta(minutes=30)) &
                (oms['Cause'] == 'Fault on transferred section')]
        own = int(o['Customers Interrupted'].iloc[0]) if len(o) else None
        out.append({'loop': r['loop'], 'to': r['recv'], 't': r['tie_close'], 'own': own,
                    'year': r['tie_close'].tz_convert(A.CENTRAL).year})
    return pd.DataFrame(out)


def dashboard(P):
    raw = pd.read_excel(P.p('dashboard'), header=None)
    hdr = raw.index[raw[0] == 'Month'][0]
    df = raw.iloc[hdr + 1:].copy()
    df.columns = list(raw.iloc[hdr])
    df = df.dropna(subset=['Month'])
    df['year'] = df['Month'].str[:4].astype(int)
    return df


def bridge_2026(P, ops, rt, cf):
    o = ops[ops['t_lo'].map(lambda t: t.tz_convert(A.CENTRAL).year) == 2026]
    dash = dashboard(P)
    D = int(dash.loc[dash['year'] == 2026, 'CI saved'].sum())
    lost = o[~o['in_archive']]
    A_ = int(lost['restored_5'].sum() + lost['upstream'].sum())
    kept = o[o['in_archive']]
    B = int(kept.loc[kept['secs'] >= FIVE_MIN, 'restored'].sum())
    # sequences the archive logs as failed after the breaker had re-closed: the dashboard counts none of them
    failed = kept[kept['tie_close'].isna() | kept['recv_trip_on_close']]
    U = int(failed['upstream'].sum())
    r26 = rt[rt['year'] == 2026] if len(rt) else rt
    Cc = int(r26['restored_before'].sum()) if len(r26) else 0
    E1 = int(r26['own'].sum()) if len(r26) else 0
    c26 = cf[cf['year'] == 2026] if len(cf) else cf
    E2 = int(c26['own'].sum()) if len(c26) else 0
    net = D + A_ + U - B - Cc - E1 - E2
    return {'dashboard': D, 'lost': A_, 'failed_upstream': U, 'after_five': B, 'reinterrupted': Cc,
            'recv_trips_own': E1, 'closes_own': E2, 'net': net}


# --------------------------------------------------------------------------------------------- batteries (R3)

def battery_tests(P):
    """every weekly load test with the airport temperature at its hour and the battery it was run on"""
    d = P.devents
    bt = d[d['Event'] == 'BATTERY TEST'].copy()
    bt['R'] = (bt['v_rest'] - bt['v_load']) / TEST_A
    wx = P.wx
    bt['T'] = wx.reindex(bt['t'].dt.floor('h')).values
    # which battery: the latest replacement before the test (maintenance book), else the one in service
    br = pd.read_excel(P.p('maint'), sheet_name='Battery replacements', header=None)
    hdr = br.index[br[0] == 'Date'][0]
    br.columns = list(br.iloc[hdr])
    br = br.iloc[hdr + 1:].dropna(subset=['Date'])
    br['Date'] = pd.to_datetime(br['Date']).dt.tz_localize('UTC')
    inst = {}
    for a, g in br.groupby('Asset No'):
        inst[a] = sorted(g['Date'].tolist())
    reg_batt = {a: pd.Timestamp(r['Battery installed']).tz_localize('UTC') for a, r in P.dev.items()
                if pd.notna(r['Battery installed'])}

    def batt_start(row):
        a, t = row['Device'], row['t']
        starts = [x for x in inst.get(a, []) if x <= t]
        if starts:
            return starts[-1]
        rb = reg_batt.get(a)
        if rb is not None and rb <= t:
            return rb
        # before the first replacement in the book: the battery the device was installed with or last given
        return pd.NaT
    bt['batt'] = bt.apply(batt_start, axis=1)
    bt['age'] = (bt['t'] - bt['batt']).dt.days / 365.25
    return bt.dropna(subset=['R', 'T']), reg_batt


def battery_risk(P, design=DESIGN_C, at=WINTER_END, pooled_k=True, age_term=True):
    """each control's battery as it stands: its internal resistance read from its load tests, fitted against the test
    hour's temperature and the battery's age, carried to the design minimum at the end of the winter"""
    bt, reg_batt = battery_tests(P)
    cur = bt[bt.apply(lambda r: pd.notna(r['batt']) and r['batt'] == reg_batt.get(r['Device']), axis=1)].copy()
    cur = cur[cur['R'] > 0]
    cur['lnR'] = np.log(cur['R'])
    cur['x'] = 25.0 - cur['T']
    # the cold coefficient, within batteries, pooled across the fleet
    def demean(g):
        g = g.copy()
        g['x0'] = g['x'] - g['x'].mean()
        g['y0'] = g['lnR'] - g['lnR'].mean()
        g['a0'] = g['age'] - g['age'].mean()
        return g
    dm = cur.groupby('Device', group_keys=False).apply(demean)
    X = np.column_stack([dm['x0'], dm['a0']]) if age_term else dm[['x0']].values
    beta = np.linalg.lstsq(X, dm['y0'].values, rcond=None)[0]
    k = beta[0]
    vr = np.polyfit(cur['T'], cur['v_rest'], 1)
    v_rest_d = float(np.polyval(vr, design))
    rows = []
    for a, g in cur.groupby('Device'):
        if pooled_k:
            y = g['lnR'] - k * g['x']
            if age_term and g['age'].max() - g['age'].min() > 0.4:
                sl, ic = np.polyfit(g['age'], y, 1)
                sl = max(sl, 0.0)
            else:
                sl, ic = (beta[1] if age_term else 0.0), float((y - (beta[1] if age_term else 0) * g['age']).mean())
        else:
            Z = np.column_stack([np.ones(len(g)), g['x'], g['age']])
            ic, kk, sl = np.linalg.lstsq(Z, g['lnR'], rcond=None)[0]
            y = None
        age_end = (at - reg_batt[a]).days / 365.25
        kk_ = k if pooled_k else kk
        lnR = ic + kk_ * (25.0 - design) + (sl if age_term else 0.0) * age_end
        R = math.exp(lnR)
        v_op = v_rest_d - OP_A * R
        rows.append({'asset': a, 'battery': reg_batt[a].date(), 'age_end': round(age_end, 2), 'R_design': R,
                     'v_op': v_op, 'fails': v_op < V_MIN, 'n_tests': len(g), 'coldest_test_C': float(g['T'].min())})
    return pd.DataFrame(rows).sort_values('v_op').reset_index(drop=True), k, v_rest_d


def battery_rivals(P, design=DESIGN_C, at=WINTER_END):
    """R3's model structure tested on the load tests themselves: nested F tests of each control's intercept, ageing
    and cold slope; every rival fitted to October 2025 and scored on last winter's cold tests at 30 A; each rival's
    count at the design minimum; each control's chance of failing under its own fit's uncertainty; RCL-21299, the
    oldest battery in service"""
    import statsmodels.formula.api as smf
    from scipy import stats
    bt, reg = battery_tests(P)
    cur = bt[bt.apply(lambda r: pd.notna(r['batt']) and r['batt'] == reg.get(r['Device']), axis=1)].copy()
    cur = cur[cur['R'] > 0].copy()
    cur['lnR'] = np.log(cur['R'])
    cur['x'] = 25.0 - cur['T']
    ctl = {a: P.dev[a]['Control'] for a in cur['Device'].unique()}
    devs = sorted(cur['Device'].unique())
    vr = np.polyfit(cur['T'], cur['v_rest'], 1)
    v_rest_d = float(np.polyval(vr, design))
    xd = 25.0 - design
    age_end = {a: (at - reg[a]).days / 365.25 for a in devs}
    # nested F tests on the full record
    D = pd.get_dummies(cur['Device']).reindex(columns=devs, fill_value=0).values.astype(float)
    ag, xx, y = cur['age'].values[:, None], cur['x'].values[:, None], cur['lnR'].values
    designs = [np.column_stack([np.ones(len(cur)), cur['x'], cur['age']]), np.column_stack([D, cur['x'], cur['age']]),
               np.column_stack([D, D * ag, cur['x']]), np.column_stack([D, D * ag, D * xx])]
    fits = []
    for X in designs:
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        fits.append((float(((y - X @ b) ** 2).sum()), int(np.linalg.matrix_rank(X))))
    n = len(cur)
    ftests = {}
    for name, (i, j) in (('control_intercepts', (0, 1)), ('control_age_slopes', (1, 2)), ('control_cold_slopes', (2, 3))):
        (r0, p0), (r1, p1) = fits[i], fits[j]
        F = ((r0 - r1) / (p1 - p0)) / (r1 / (n - p1))
        ftests[name] = {'F': round(F, 1), 'df': [p1 - p0, n - p1], 'p': float(stats.f.sf(F, p1 - p0, n - p1))}

    def models(tr):
        out = {}
        X = np.column_stack([np.ones(len(tr)), tr['x'], tr['age']])
        b = np.linalg.lstsq(X, tr['lnR'], rcond=None)[0]
        out['one fleet fit of log resistance'] = lambda a, x, age, b=b: math.exp(b[0] + b[1] * x + b[2] * age)
        bl = np.linalg.lstsq(X, tr['R'], rcond=None)[0]
        out['one fleet fit of resistance'] = lambda a, x, age, b=bl: max(1e-4, b[0] + b[1] * x + b[2] * age)
        bt_, btl = {}, {}
        for t, s in tr.groupby(tr['Device'].map(ctl)):
            Xs = np.column_stack([np.ones(len(s)), s['x'], s['age']])
            bt_[t] = np.linalg.lstsq(Xs, s['lnR'], rcond=None)[0]
            btl[t] = np.linalg.lstsq(Xs, s['R'], rcond=None)[0]
        out['a fit per control type, log resistance'] = lambda a, x, age, b=bt_: math.exp(b[ctl[a]] @ [1.0, x, age])
        out['a fit per control type, resistance'] = lambda a, x, age, b=btl: max(1e-4, b[ctl[a]] @ [1.0, x, age])
        dm = tr.copy()
        for c in ('lnR', 'x', 'age'):
            dm[c + '0'] = dm[c] - dm.groupby('Device')[c].transform('mean')
        beta = np.linalg.lstsq(np.column_stack([dm['x0'], dm['age0']]), dm['lnR0'], rcond=None)[0]
        ic = {a: float((s['lnR'] - beta[0] * s['x'] - beta[1] * s['age']).mean()) for a, s in tr.groupby('Device')}
        out['each control\'s level, fleet ageing'] = lambda a, x, age, ic=ic, b=beta: (
            math.exp(ic[a] + b[0] * x + b[1] * age) if a in ic else float('nan'))
        own, lin = {}, {}
        for a, s in tr.groupby('Device'):
            if len(s) < 20 or s['age'].max() - s['age'].min() <= 0.4:
                continue
            sl, i0 = np.polyfit(s['age'], s['lnR'] - beta[0] * s['x'], 1)
            own[a] = (i0, max(sl, 0.0))
            lin[a] = np.linalg.lstsq(np.column_stack([np.ones(len(s)), s['x'], s['age']]), s['R'], rcond=None)[0]
        out['each control\'s own resistance, linear'] = lambda a, x, age, b=lin: (
            max(1e-4, b[a] @ [1.0, x, age]) if a in b else float('nan'))
        out['each battery\'s own ageing (the golden)'] = lambda a, x, age, b=own, k=beta[0]: (
            math.exp(b[a][0] + k * x + b[a][1] * age) if a in b else float('nan'))
        m = smf.mixedlm('lnR ~ x + age', tr, groups=tr['Device'], re_formula='~age').fit(method='lbfgs')
        fe, re = m.fe_params, m.random_effects
        out['a mixed model, each control drawn around the fleet'] = lambda a, x, age, fe=fe, re=re: (
            math.exp(fe['Intercept'] + re[a].iloc[0] + fe['x'] * x + (fe['age'] + re[a].iloc[1]) * age)
            if a in re else float('nan'))
        return out

    full = models(cur)
    counts = {}
    for name, f in full.items():
        named = []
        for a in devs:
            r = f(a, xd, age_end[a])
            if not math.isnan(r) and v_rest_d - OP_A * r < V_MIN:
                named.append(a)
        counts[name] = named
    # out of sample: fitted to the end of October 2025, scored on the 2025-26 winter's tests below -15 C, on the tests
    # every rival can predict
    cut = pd.Timestamp('2025-11-01', tz='UTC')
    tr = cur[cur['t'] < cut]
    te = cur[(cur['t'] >= cut) & (cur['t'] < pd.Timestamp('2026-04-01', tz='UTC')) & (cur['T'] < -15.0)]
    oos = models(tr)
    pred = {name: np.array([f(r.Device, r.x, r.age) for r in te.itertuples()]) for name, f in oos.items()}
    ok = np.all([~np.isnan(v) for v in pred.values()], axis=0)
    rmse = {name: round(float(np.sqrt(((OP_A * (v[ok] - te['R'].values[ok])) ** 2).mean())), 3) for name, v in pred.items()}
    # each control's chance of failing under its own fit's uncertainty (the golden's structure)
    k = float(np.linalg.lstsq(np.column_stack([cur['x'] - cur.groupby('Device')['x'].transform('mean'),
                                               cur['age'] - cur.groupby('Device')['age'].transform('mean')]),
                              cur['lnR'] - cur.groupby('Device')['lnR'].transform('mean'), rcond=None)[0][0])
    rng = np.random.default_rng(7)
    p_fail, slopes = {}, {}
    for a, s in cur.groupby('Device'):
        if s['age'].max() - s['age'].min() <= 0.4:
            continue
        Xs = np.column_stack([np.ones(len(s)), s['age']])
        ys = (s['lnR'] - k * s['x']).values
        b = np.linalg.lstsq(Xs, ys, rcond=None)[0]
        cov = ((ys - Xs @ b) ** 2).sum() / (len(s) - 2) * np.linalg.inv(Xs.T @ Xs)
        slopes[a] = (float(b[1]), float(math.sqrt(cov[1, 1])))
        dr = rng.multivariate_normal(b, cov, 4000)
        v = v_rest_d - OP_A * np.exp(dr[:, 0] + k * xd + np.maximum(dr[:, 1], 0.0) * age_end[a])
        p_fail[a] = float((v < V_MIN).mean())
    sv = np.array([v[0] for v in slopes.values()])
    d = P.devents
    s99 = d[(d['Device'] == 'RCL-21299') & (d['Event'] == 'BATTERY TEST')]['t'].sort_values()
    up = pd.Timestamp('2025-03-18', tz='UTC')
    br = pd.read_excel(P.p('maint'), sheet_name='Battery replacements', header=None)
    risk = battery_risk(P, design=design, at=at)[0].set_index('asset')
    return {'f_tests': ftests,
            'counts': {name: len(v) for name, v in counts.items()}, 'named': counts,
            'oos_rmse_v': rmse, 'oos_tests': int(ok.sum()), 'oos_controls': int(te.loc[ok, 'Device'].nunique()),
            'slope_p5': round(float(np.percentile(sv, 5)), 2), 'slope_p95': round(float(np.percentile(sv, 95)), 2),
            'slope_se_median': round(float(np.median([v[1] for v in slopes.values()])), 3),
            'p_fail': {a: round(p, 4) for a, p in p_fail.items()},
            'rcl21299': {'slope': round(slopes['RCL-21299'][0], 3),
                         'slope_rank': int((sv < slopes['RCL-21299'][0]).sum()), 'controls': int(len(sv)),
                         'v_op': round(float(risk.loc['RCL-21299', 'v_op']), 2),
                         'battery_installed': str(reg['RCL-21299'].date()),
                         'tests': int(len(s99)), 'max_gap_days': int(s99.diff().dt.days.max()),
                         'tests_before_upgrade': int((s99 < up).sum()), 'tests_after_upgrade': int((s99 >= up).sum()),
                         'book_rows': int((br == 'RCL-21299').any(axis=1).sum())}}


# ------------------------------------------------------------------------------- transfers forward (R4 and R5)

KV, PF = 13.8, 0.96
SUMMER = (6, 7, 8, 9)


def mw_to_amps(mw):
    return mw * 1000.0 / (math.sqrt(3) * KV * PF)


def directions(P):
    """each transfer direction and whether the ADMS switches the receiving reclosers to their transfer group: read
    from the archive's transfers, and from the receiving controls where the archive holds none"""
    a = P.adms
    out = []
    for _, L in P.loops.iterrows():
        for fa, fb in ((L['Feeder A'], L['Feeder B']), (L['Feeder B'], L['Feeder A'])):
            r1, r2 = P.dev_at[(fb, 'R1')], P.dev_at[(fb, 'R2')]
            g2 = a[(a['loop'] == L['Loop']) & (a['kind'] == 'GROUP2') & a['asset'].isin([r1, r2])]
            ctl_old = P.dev[r1]['Control'] == 'CTL-4C' or P.dev[r2]['Control'] == 'CTL-4C'
            out.append({'loop': L['Loop'], 'from': fa, 'to': fb, 'r1': r1, 'r2': r2,
                        'switched': (len(g2) > 0) if len(g2) else (not ctl_old), 'group2_seen': len(g2),
                        'pick_r1': float(P.dev[r1]['Phase pickup group 1 (A)']),
                        'pick_r2': float(P.dev[r2]['Phase pickup group 1 (A)'])})
    return pd.DataFrame(out)


CB_TYPING = {'repair': True}


def cb_section(P, r):
    """the section a breaker lockout's fault lay in: where the scheme located it, else the section the outage
    record's repair restored, else section 1"""
    cache = P.__dict__.setdefault('_cb_section_%s' % CB_TYPING['repair'], {})
    key = (r['device'], r['t_lo'])
    if key in cache:
        return cache[key]
    loc = P.adms[P.adms['kind'] == 'LOCATED']
    m = loc[(loc['loop'] == r['loop']) & (loc['t'] >= r['t_lo']) & (loc['t'] <= r['t_lo'] + pd.Timedelta(minutes=10))]
    if len(m):
        sec = int(m['n'].iloc[0])
    elif not CB_TYPING['repair']:
        sec = 1
    else:
        rep = P.oms[(P.oms['Step Type'] == 'Repair') & (P.oms['Interrupting Device'] == r['device'])]
        rep = rep[(rep['start'] - r['t_first']).abs() < pd.Timedelta(minutes=40)]
        sec = 1
        if len(rep):
            n = int(rep['Customers Restored'].iloc[0])
            c = {k: P.customers(r['feeder'], k, r['t_lo'].date()) for k in (1, 2, 3)}
            sec = min(c, key=lambda kk: abs(c[kk] - n))
    cache[key] = sec
    return sec


def lockout_rates(P, ops_all):
    """main-line lockouts a year per loop feeder by what the scheme would transfer (sections 2 and 3 for a fault in
    section 1, section 3 for a fault in section 2), at the record's average annual rate since 1 January 2022"""
    lo = lockouts(P)
    years = (pd.Timestamp('2026-11-01', tz='UTC') - pd.Timestamp('2022-01-01', tz='UTC')).days / 365.25
    a = P.adms
    loc = a[a['kind'] == 'LOCATED']
    rate = {}
    month = {}
    for _, r in lo.iterrows():
        f = r['feeder']
        typ = None
        if r['kind'] == 'R1':
            typ = 'S2'
        elif r['kind'] == 'CB':
            # a breaker lockout transfers what lies beyond its fault: sections 2 and 3, or section 3
            typ = {1: 'S1', 2: 'S2'}.get(cb_section(P, r))
        if typ:
            rate[(f, typ)] = rate.get((f, typ), 0) + 1.0 / years
            mm = r['t_lo'].tz_convert(A.CENTRAL).month
            month[mm] = month.get(mm, 0) + 1
    tot = sum(month.values())
    mshare = {m: month.get(m, 0) / tot for m in range(1, 13)}
    return rate, mshare, lo


def upstream_rates(P, ops):
    """breaker lockouts for a section 2 fault a year per loop feeder, at the record's average annual rate since
    1 January 2022, and the share the scheme re-closed within five minutes: the breaker's own section, restored
    before any transfer is tried"""
    lo = lockouts(P)
    years = (pd.Timestamp('2026-11-01', tz='UTC') - pd.Timestamp('2022-01-01', tz='UTC')).days / 365.25

    def sec2(r):
        return cb_section(P, r) == 2
    rate = {}
    for _, r in lo[lo['kind'] == 'CB'].iterrows():
        if sec2(r):
            rate[r['feeder']] = rate.get(r['feeder'], 0) + 1.0 / years
    o = ops[ops['kind'] == 'CB']
    o = o[o.apply(sec2, axis=1)]
    q_up = float((o['upstream'] > 0).mean()) if len(o) else 0.0
    return rate, q_up, len(o)


def fault_hours(P, lo):
    """the hours of the day and months main-line lockouts on the loops struck, and the repairs' durations"""
    l = lo.copy()
    l['lt'] = l['t_lo'].dt.tz_convert(A.CENTRAL)
    oms = P.oms
    rep = oms[(oms['Step Type'] == 'Repair') & oms['Interrupting Device'].isin(set(lo['device']))]
    dur = ((rep['step_t'] - rep['start']).dt.total_seconds() / 3600.0).clip(0.5, 24).values
    return l, dur


def trip_prob(P, d, typ, l, dur, extra_amps=0.0, extra_from=None, pk=1.0, months=SUMMER, weighting='faults'):
    """the chance a transfer of this type on this direction trips a receiving recloser before the faulted section is
    repaired, replayed on the 2025 and 2026 hourly loads at the hours and months the loops' lockouts struck"""
    S = P.scada
    fa, fb = d['from'], d['to']
    xa = S['%s.R1.IA_AVG' % fa] if typ == 'S1' else S['%s.R2.IA_AVG' % fa]
    b2 = S['%s.R2.IA_AVG' % fb]
    b1 = S['%s.R1.IA_AVG' % fb]
    c2 = (b2 + xa + extra_amps).values
    c1 = (b1 + xa + extra_amps).values
    idx = S.index.tz_convert(A.CENTRAL)
    ok = ~(np.isnan(c2) | np.isnan(c1))
    trip_h = ok & ((c2 * pk > d['pick_r2']) | (c1 * pk > d['pick_r1']))
    mon = np.array(idx.month)
    hod = np.array(idx.hour)
    pos = {(m, h): np.nonzero((mon == m) & (hod == h) & ok)[0] for m in months for h in range(24)}
    ev = l[l['lt'].dt.month.isin(months)]
    if weighting == 'faults':
        keys = list(zip(ev['lt'].dt.month, ev['lt'].dt.hour))
    else:
        keys = [(m, h) for m in months for h in range(24)]
    rng = np.random.default_rng(7)
    n = 0
    hit = 0.0
    for (m, h) in keys:
        starts = pos.get((m, h))
        if starts is None or not len(starts):
            continue
        for s in starts:
            ds = dur[rng.integers(0, len(dur), size=8)]
            for D_ in ds:
                e = min(len(trip_h), s + int(math.ceil(D_)))
                n += 1
                hit += bool(trip_h[s:e].any())
    return hit / max(1, n)


def slip_months(P, cats=('Reconductor', 'Recloser control replacement')):
    cw = pd.read_excel(P.p('capital'), header=None)
    hdr = cw.index[cw[0] == 'Project'][0]
    cw.columns = list(cw.iloc[hdr])
    cw = cw.iloc[hdr + 1:].dropna(subset=['Project'])
    done = cw[(cw['Status'] == 'Complete') & cw['Category'].isin(cats)]
    sl = ((pd.to_datetime(done['Actual in service']) - pd.to_datetime(done['Planned in service'])).dt.days / 30.44).values
    plan = cw[(cw['Status'] == 'Approved 2027') & cw['Title'].str.contains('replace recloser controls', case=False)]
    return sl, plan


def p_in_service(sl, planned, when):
    """the share of comparable completed projects that would have been in service by this date"""
    gap = (pd.Timestamp(when) - pd.Timestamp(planned)).days / 30.44
    return float(np.mean(sl <= gap))


def large_loads(P):
    ll = pd.read_excel(P.p('loads'), header=None)
    hdr = ll.index[ll[0] == 'Request'][0]
    ll.columns = list(ll.iloc[hdr])
    ll = ll.iloc[hdr + 1:].dropna(subset=['Request'])
    ll = ll[ll['Status'].str.startswith('Approved') & (pd.to_datetime(ll['Requested in service']) < pd.Timestamp('2027-10-01'))]
    out = []
    for _, r in ll.iterrows():
        if r['Feeder'] in P.loop_of_feeder and str(r['Location']).startswith('Section'):
            k = int(str(r['Location']).split()[1])
            out.append({'feeder': r['Feeder'], 'section': k, 'mw': float(r['Load (MW)']),
                        'from': pd.Timestamp(r['Requested in service'])})
    return out


def success_rate(P, ops, months=None):
    """the share of lockouts with something to transfer that the scheme restored within five minutes"""
    o = ops[ops['iso'].notna() | ops['tie_close'].notna() | ops['kind'].isin(['CB', 'R1'])]
    if months:
        o = o[o['t_lo'].dt.tz_convert(A.CENTRAL).dt.month.isin(months)]
    ok = (o['restored_5'] > 0)
    return float(ok.mean()), len(o)


def forward(P, ops, months=SUMMER, plan_trusted=False, newload=True, pk=1.0, weighting='faults', reinf_cats=None):
    """R4: the receiving feeders' customers summer 2027 transfers would interrupt, settings as they stand"""
    D = directions(P)
    rate, mshare, lo = lockout_rates(P, ops)
    l, dur = fault_hours(P, lo)
    succ, _ = success_rate(P, ops)
    sl, plan = slip_months(P, reinf_cats or ('Reconductor', 'Recloser control replacement'))
    reinf = {}
    for _, r in plan.iterrows():
        reinf[r['Feeder']] = pd.Timestamp(r['Planned in service'])
    loads = large_loads(P) if newload else []
    rows = []
    for _, d in D[~D['switched']].iterrows():
        fa, fb = d['from'], d['to']
        extra = sum(mw_to_amps(x['mw']) for x in loads if x['feeder'] == fb and x['section'] == 3)
        tot = 0.0
        for typ in ('S1', 'S2'):
            r_ = rate.get((fa, typ), 0.0)
            T = P.customers(fa, 2, dt.date(2027, 1, 1)) + P.customers(fa, 3, dt.date(2027, 1, 1)) if typ == 'S1' else \
                P.customers(fa, 3, dt.date(2027, 1, 1))
            for m in months:
                w_m = mshare[m]
                p = trip_prob(P, d, typ, l, dur, extra_amps=extra, pk=pk, months=(m,), weighting=weighting)
                # which recloser goes first decides whose customers: section 3, or sections 2 and 3
                Bd = P.customers(fb, 3, dt.date(2027, 1, 1))
                still = 1.0
                if fb in reinf and not plan_trusted:
                    still = 1.0 - p_in_service(sl, reinf[fb], pd.Timestamp(2027, m, 15))
                elif fb in reinf and plan_trusted:
                    still = 0.0 if reinf[fb] <= pd.Timestamp(2027, m, 1) else 1.0
                tot += r_ * w_m * succ * p * Bd * still
        rows.append({'loop': d['loop'], 'from': fa, 'to': fb, 'harm': tot, 'reinforced_feeder': fb in reinf})
    return pd.DataFrame(rows)


def supervised_now(P):
    """loops whose scheme stands in supervised mode at the end of the record"""
    ch = P.changes
    state = {}
    for _, r in ch.sort_values('Date').iterrows():
        c = str(r['Change'])
        if c.startswith('Scheme set to supervised'):
            state[r['Loop']] = True
        elif c.startswith('Scheme returned to automatic'):
            state[r['Loop']] = False
    return {k for k, v in state.items() if v}


def battery_fail_temp(br, v_rest_fn, k):
    """the air temperature below which each control's battery cannot carry an operation, at its 2027 age"""
    out = {}
    for _, r in br.iterrows():
        # R(T) = R_design * exp(k * (T_design - T)); solve v_rest(T) - 30 R(T) = 21.2 on a grid
        Ts = np.arange(-40.0, 15.0, 0.25)
        R = r['R_design'] * np.exp(k * (DESIGN_C - Ts))
        v = v_rest_fn(Ts) - OP_A * R
        bad = Ts[v < V_MIN]
        out[r['asset']] = float(bad.max()) if len(bad) else -99.0
    return out


def forecast(P, ops, plan_trusted=False, net=True, skyline_fixed=True, battery=True, supervised=True, sims=4000,
             months_all=tuple(range(1, 13)), success_from='record', pk=1.0, weighting='faults', reinf_cats=None,
             upstream=True):
    """R5: 2027 customer interruptions avoided if the schemes are operated as they stand"""
    D = directions(P)
    rate, mshare, lo = lockout_rates(P, ops)
    l, dur = fault_hours(P, lo)
    sl, plan = slip_months(P, reinf_cats or ('Reconductor', 'Recloser control replacement'))
    reinf = {r['Feeder']: pd.Timestamp(r['Planned in service']) for _, r in plan.iterrows()}
    loads = large_loads(P)
    sup = supervised_now(P) if supervised else set()
    # the scheme's own record: lockouts with something to transfer, restored within five minutes, and why not
    o = ops[ops['kind'].isin(['CB', 'R1'])].copy()
    o['month'] = o['t_lo'].dt.tz_convert(A.CENTRAL).dt.month
    a = P.adms
    inc = pd.read_csv(P.p('incidents'))
    sky = inc[inc['Location'] == 'Skyline Tower'].copy()
    sky['o'] = pd.to_datetime(sky['Opened']).dt.tz_localize(A.CENTRAL, ambiguous=True).dt.tz_convert('UTC')
    sky['c'] = pd.to_datetime(sky['Closed']).dt.tz_localize(A.CENTRAL, ambiguous=True).dt.tz_convert('UTC')
    long_sky = sky[(sky['c'] - sky['o']) > pd.Timedelta(days=20)]
    sky_assets = {x for x, r in P.dev.items() if r['Radio site'] == 'Skyline Tower'}
    excl = np.zeros(len(o), bool)
    br, k, vrd = battery_risk(P)
    vr = np.polyfit(battery_tests(P)[0]['T'], battery_tests(P)[0]['v_rest'], 1)
    tfail = battery_fail_temp(br, lambda T: np.polyval(vr, T), k)
    for i, (_, r) in enumerate(o.iterrows()):
        seq = a[(a['loop'] == r['loop']) & (a['t'] >= r['t_lo']) & (a['t'] <= r['t_lo'] + pd.Timedelta(minutes=12))]
        to = seq[seq['kind'] == 'TIMEOUT']
        if skyline_fixed and len(to) and len(long_sky):
            s0, s1 = long_sky['o'].iloc[0], long_sky['c'].iloc[0]
            if s0 <= r['t_lo'] <= s1 and to['asset'].isin(sky_assets).any():
                excl[i] = True
        if battery and len(to) and r['restored_5'] == 0:
            # a control that browned out in the cold is the battery, not the radio: its own record shows it
            pass
        if r['loop'] in sup or r['loop'] in supervised_periods_loops(P, r['t_lo']):
            excl[i] = True if supervised else excl[i]
    base = o[~excl]
    q = float((base['restored_5'] > 0).mean())
    # the cold failures the record holds are the batteries as they were; the batteries as they stand replace them
    T_ev = np.array([P.temp_at(t) for t in o['t_lo']])
    T_ev = T_ev[~np.isnan(T_ev)]
    if battery:
        cold_fail_seen = 0.0
        q_nb = q
    rate_up, q_up, _ = upstream_rates(P, ops)
    rng = np.random.default_rng(11)
    units = []
    mean = 0.0
    for _, L in P.loops.iterrows():
        for fa in (L['Feeder A'], L['Feeder B']):
            fb = P.partner[fa]
            d = D[(D['from'] == fa) & (D['to'] == fb)].iloc[0]
            extra = sum(mw_to_amps(x['mw']) for x in loads if x['feeder'] == fb and x['section'] == 3)
            for typ, iso in (('S1', 'R1'), ('S2', 'R2')):
                r_ = rate.get((fa, typ), 0.0)
                if r_ == 0:
                    continue
                T = P.customers(fa, 2, dt.date(2027, 1, 1)) + P.customers(fa, 3, dt.date(2027, 1, 1)) if typ == 'S1' \
                    else P.customers(fa, 3, dt.date(2027, 1, 1))
                Bd = P.customers(fb, 3, dt.date(2027, 1, 1))
                dev = P.dev_at[(fa, iso)]
                pb = float(np.mean(T_ev < tfail.get(dev, -99))) if battery else 0.0
                qq = 0.0 if (supervised and L['Loop'] in sup) else q * (1 - pb)
                ev = 0.0
                for m in months_all:
                    p = 0.0
                    if net and not d['switched']:
                        p = trip_prob(P, d, typ, l, dur, extra_amps=extra, months=(m,), pk=pk, weighting=weighting)
                        if fb in reinf:
                            still = (0.0 if reinf[fb] <= pd.Timestamp(2027, m, 1) else 1.0) if plan_trusted else \
                                1.0 - p_in_service(sl, reinf[fb], pd.Timestamp(2027, m, 15))
                            p *= still
                    ev += mshare[m] * (T * (1 - p) - p * Bd)
                mean += r_ * qq * ev
                units.append((r_, qq, ev / max(1e-9, sum(mshare[m] for m in months_all)), T, Bd))
            # a breaker lockout for a section 2 fault: the breaker re-closes onto section 1 once R2 and then R1 have
            # opened on their batteries, before the capacity check, the settings and any operator confirmation
            ru = rate_up.get(fa, 0.0) if upstream else 0.0
            if ru:
                U1 = P.customers(fa, 1, dt.date(2027, 1, 1))
                t_w = max(tfail.get(P.dev_at[(fa, 'R1')], -99), tfail.get(P.dev_at[(fa, 'R2')], -99))
                qu = q_up * (1 - (float(np.mean(T_ev < t_w)) if battery else 0.0))
                mean += ru * qu * U1
                units.append((ru, qu, float(U1), U1, 0))
    # the 80 per cent range: the year's lockouts and outcomes drawn as they fall
    tot = np.zeros(sims)
    for r_, qq, evu, T, Bd in units:
        n = rng.poisson(r_, size=sims)
        s = rng.binomial(n, qq)
        tot += s * evu
    lo10, hi90 = np.percentile(tot, [10, 90])
    return {'mean': mean, 'p10': float(lo10), 'p90': float(hi90), 'q': q, 'tfail': tfail}


def supervised_periods_loops(P, t):
    ch = P.changes.sort_values('Date')
    out = set()
    state = {}
    for _, r in ch.iterrows():
        d = pd.Timestamp(r['Date']).tz_localize('UTC')
        if d > t:
            break
        c = str(r['Change'])
        if c.startswith('Scheme set to supervised'):
            state[r['Loop']] = True
        elif c.startswith('Scheme returned to automatic'):
            state[r['Loop']] = False
    return {k for k, v in state.items() if v}


def compute(target):
    P = A.Pack(target)
    ops = operations(P)
    rt = receiving_trips(P, ops)
    cf = closes_onto_fault(P, ops)
    br, k, vrd = battery_risk(P)
    res = {'R1': r1_by_year(ops), 'R2': bridge_2026(P, ops, rt, cf),
           'R3': sorted(br.loc[br['fails'], 'asset'].tolist()), 'R3_k': k, 'R3_vrest': vrd}
    res['_battery'] = br
    fw = forward(P, ops)
    res['R4'] = float(fw['harm'].sum())
    res['_forward'] = fw
    fc = forecast(P, ops)
    res['R5'] = fc['mean']
    res['R5_range'] = (fc['p10'], fc['p90'])
    res['_forecast'] = fc
    return P, ops, rt, cf, res


if __name__ == '__main__':
    import sys
    P, ops, rt, cf, res = compute(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'target'))
    print(json.dumps(res, indent=1, default=str))
    print(rt.to_string() if len(rt) else 'no receiving trips')
    print(cf.to_string() if len(cf) else 'no closes onto fault')


def results_for_deliverables(target):
    P = A.Pack(target)
    ops = operations(P)
    rt = receiving_trips(P, ops)
    cf = closes_onto_fault(P, ops)
    br_ = bridge_2026(P, ops, rt, cf)
    dash = dashboard(P)
    o = ops.copy()
    o['year'] = o['t_lo'].dt.tz_convert(A.CENTRAL).dt.year
    years = {}
    for y in range(2022, 2027):
        g = o[o['year'] == y]
        years[y] = {'lockouts': int(len(g)), 'restored_5': int(g['restored_5'].sum() + g['upstream'].sum()),
                    'restored_after': int(g.loc[g['secs'] >= FIVE_MIN, 'restored'].sum()),
                    'not_in_archive': int((~g['in_archive']).sum()),
                    'dashboard': int(dash.loc[dash['year'] == y, 'CI saved'].sum())}
    g26 = o[o['year'] == 2026].copy()
    rtk = {(r['loop'], r['from']): r for _, r in rt.iterrows()} if len(rt) else {}
    ops26 = pd.DataFrame([{
        'Lockout (CT)': r['t_lo'].tz_convert(A.CENTRAL).strftime('%Y-%m-%d %H:%M'), 'Loop': r['loop'],
        'Feeder': r['feeder'], 'Device': r['device'], 'In archive': 'Y' if r['in_archive'] else 'N',
        'Isolated at': r['iso'] or '', 'Tie closed (s)': round(r['secs']) if r['tie_close'] is not None and r['secs'] else '',
        'Restored <5 min': int(r['restored_5'] + r['upstream']),
        'Restored >=5 min': int(r['restored']) if r['secs'] >= FIVE_MIN else 0,
        'Receiving trip': 'Y' if any((x['from'] == r['feeder'] and abs((x['t'] - r['t_lo']).total_seconds()) < 86400)
                                     for _, x in (rt.iterrows() if len(rt) else [])) else '',
        'Close onto fault': 'Y' if r['recv_trip_on_close'] else ''} for _, r in g26.iterrows()])
    bat, k, vrd = battery_risk(P)
    bt = pd.DataFrame({'Asset No': bat['asset'], 'Battery installed': bat['battery'].astype(str),
                       'Age 28 Feb 2027 (y)': bat['age_end'], 'Load tests': bat['n_tests'],
                       'Coldest test (C)': bat['coldest_test_C'].round(1),
                       'Volts at 30 A, -27 C': bat['v_op'].round(2), 'Replace': bat['fails'].map({True: 'YES', False: ''})})
    fw = forward(P, ops)
    sl, plan = slip_months(P)
    reinf = {r['Feeder']: pd.Timestamp(r['Planned in service']).date() for _, r in plan.iterrows()}
    D = directions(P)
    sm = pd.DataFrame([{'Loop': r['loop'], 'From': r['from'], 'To': r['to'],
                        'Receiving R1 pickup (A)': int(D[(D['from'] == r['from'])]['pick_r1'].iloc[0]),
                        'Receiving R2 pickup (A)': int(D[(D['from'] == r['from'])]['pick_r2'].iloc[0]),
                        'Reinforcement planned': str(reinf.get(r['to'], '')),
                        'Receiving customers interrupted, Jun-Sep 2027': round(r['harm'], 1),
                        'Change settings': 'YES'} for _, r in fw.iterrows()])
    fc = forecast(P, ops)
    rate, mshare, lo = lockout_rates(P, ops)
    frows = []
    for _, L in P.loops.iterrows():
        for fa in (L['Feeder A'], L['Feeder B']):
            frows.append({'Loop': L['Loop'], 'Feeder': fa, 'S1 lockouts/yr': round(rate.get((fa, 'S1'), 0), 2),
                          'S2 lockouts/yr': round(rate.get((fa, 'S2'), 0), 2),
                          'Sections 2+3 customers': P.customers(fa, 2, dt.date(2027, 1, 1)) + P.customers(fa, 3, dt.date(2027, 1, 1)),
                          'Section 3 customers': P.customers(fa, 3, dt.date(2027, 1, 1)),
                          'Supervised now': 'Y' if L['Loop'] in supervised_now(P) else ''})
    frows = pd.DataFrame(frows)
    summer_set = ', '.join('%s to %s' % (r['from'], r['to']) for _, r in fw.iterrows())
    return {'bridge': br_, 'years': years, 'ops2026': ops26, 'batteries': bt, 'summer': sm, 'forecast': fc,
            'forecast_rows': frows, 'rebattery': sorted(bat.loc[bat['fails'], 'asset']), 'summer_set': summer_set,
            'summer_total': float(fw['harm'].sum()), 'slip_median': float(np.median(sl)),
            'r1': r1_by_year(ops), 'battery_table': bat, 'forward_table': fw}


def build(target, gold_dir, figures=None):
    import shutil
    import deliver as DL
    import postprocess as PP
    import common as C
    R = results_for_deliverables(target)
    if os.path.exists(gold_dir):
        shutil.rmtree(gold_dir)
    os.makedirs(gold_dir)
    DL.workbook(os.path.join(gold_dir, C.DELIVERABLES[0]), R)
    DL.memo(os.path.join(gold_dir, C.DELIVERABLES[1]), R)
    PP.own_mtimes(gold_dir, {})
    if figures:
        bat = R['battery_table']
        fw = R['forward_table']
        F = {'r1_by_year': {str(k): v for k, v in R['r1'].items()}, 'bridge_2026': R['bridge'], 'net_2026': R['bridge']['net'],
             'dashboard_2026': R['bridge']['dashboard'], 'rebattery_set': R['rebattery'], 'rebattery_n': len(R['rebattery']),
             'summer_2027_receiving': round(R['summer_total']), 'summer_directions': R['summer_set'],
             'forecast_2027': round(R['forecast']['mean']), 'forecast_2027_p10': round(R['forecast']['p10']),
             'forecast_2027_p90': round(R['forecast']['p90']), 'slip_median_months': round(R['slip_median'], 1),
             'years': {str(k): v for k, v in R['years'].items()}}
        import passes as PS
        P = A.Pack(target)
        ops = operations(P)
        c_r1, _, _ = PS.careful_r1(P, ops)
        F['careful_r1'] = {str(k): v for k, v in c_r1.items()}
        F['careful_net_2026'] = c_r1[2026]
        F['careful_rebattery_n'] = len(PS.careful_r3(P))
        F['book_rebattery_n'] = len(PS.careful_r3_book(P))
        F['quick_rebattery_n'] = len(PS.quick_r3(P))
        F['careful_summer_2027'] = round(PS.careful_r4(P, ops))
        F['summer_2027_plan_trusted'] = round(float(forward(P, ops, plan_trusted=True)['harm'].sum()))
        F['summer_2027_no_new_load'] = round(float(forward(P, ops, newload=False)['harm'].sum()))
        F['careful_forecast_2027'] = round(forecast(P, ops, net=False, plan_trusted=True, battery=False, supervised=False,
                                                    sims=400)['mean'])
        F['forecast_2027_gross'] = round(forecast(P, ops, net=False, sims=400)['mean'])
        sl, plan = slip_months(P)
        F['reinforcements'] = [{'feeder': r['Feeder'], 'planned': str(pd.Timestamp(r['Planned in service']).date()),
                                'p_by_jun1': round(p_in_service(sl, r['Planned in service'], pd.Timestamp('2027-06-01')), 2),
                                'p_by_sep1': round(p_in_service(sl, r['Planned in service'], pd.Timestamp('2027-09-01')), 2)}
                               for _, r in plan.iterrows()]
        F['slip_n'] = int(len(sl))
        sl_rc, _ = slip_months(P, ('Reconductor',))
        F['slip_median_months_reconductor'] = round(float(np.median(sl_rc)), 1)
        F['p_jun1_max_reconductor'] = round(max(p_in_service(sl_rc, r['Planned in service'], pd.Timestamp('2027-06-01'))
                                                for _, r in plan.iterrows()), 2)
        F['r3_ruling'] = battery_rivals(P)
        F['summer_windows'] = {'June to August': round(float(forward(P, ops, months=(6, 7, 8))['harm'].sum())),
                               'May to September': round(float(forward(P, ops, months=(5, 6, 7, 8, 9))['harm'].sum())),
                               'July to August': round(float(forward(P, ops, months=(7, 8))['harm'].sum()))}
        rivals, lowest = {}, {}
        for name, kw in (('per-battery', dict(pooled_k=False)), ('jan31', dict(at=pd.Timestamp('2027-01-31', tz='UTC'))),
                         ('m26', dict(design=-26.0)), ('m28', dict(design=-28.0))):
            b_ = battery_risk(P, **kw)[0]
            rivals[name] = set(b_.loc[b_['fails'], 'asset'])
            lowest[name] = list(b_['asset'].head(3))
        gold = set(R['rebattery'])
        core = set.intersection(gold, *rivals.values())
        F['rebattery_core'] = sorted(core)
        F['rebattery_margin'] = sorted((gold | set.union(*rivals.values())) - core)
        F['rebattery_band'] = [len(core), len(core) + len(F['rebattery_margin'])]
        F['rebattery_lowest'] = [r['asset'] for _, r in R['battery_table'].head(3).iterrows()]
        F['rebattery_lowest_rivals'] = lowest
        F['unswitched_directions'] = len(fw)
        F['supervised_now'] = sorted(supervised_now(P))
        F['lockout_rate_total'] = round(sum(lockout_rates(P, ops)[0].values()), 1)
        F['success_rate'] = round(forecast(P, ops, sims=10)['q'], 3)
        bt = R['battery_table']
        F['battery_v'] = {r['asset']: round(r['v_op'], 2) for _, r in bt.iterrows() if r['asset'] in gold | set(F['rebattery_margin'])}
        r5 = R['forecast']['mean']
        CB_TYPING['repair'] = False
        r5_loc, r4_loc = forecast(P, ops, sims=300)['mean'], round(float(forward(P, ops)['harm'].sum()))
        CB_TYPING['repair'] = True
        fam5 = [forecast(P, ops, pk=1.05, sims=300)['mean'], forecast(P, ops, weighting='hours', sims=300)['mean'],
                forecast(P, ops, reinf_cats=('Reconductor',), sims=300)['mean'],
                forecast(P, ops, skyline_fixed=False, sims=300)['mean'], r5_loc]
        F['forecast_2027_location_typing'] = round(r5_loc)
        F['forecast_2027_no_breaker_section'] = round(forecast(P, ops, sims=300, upstream=False)['mean'])
        ru_, qu_, nu_ = upstream_rates(P, ops)
        F['breaker_section'] = {'events_a_year': round(sum(ru_.values()), 2), 'reclosed_share': round(qu_, 3),
                                'lockouts': nu_, 'reclosed': int(round(qu_ * nu_))}
        F['forecast_2027_band'] = [math.floor(min(r5, *fam5) * 0.98), math.ceil(max(r5, *fam5) * 1.02)]
        F['lockouts_total'] = sum(v['lockouts'] for v in R['years'].values())
        F['not_in_archive_total'] = sum(v['not_in_archive'] for v in R['years'].values())
        ps = [x['p_by_jun1'] for x in F['reinforcements']]
        F['p_jun1_range'] = [min(ps), max(ps)]
        fam = [F['summer_2027_receiving'], round(float(forward(P, ops, pk=1.05)['harm'].sum())),
               round(float(forward(P, ops, weighting='hours')['harm'].sum())),
               round(float(forward(P, ops, reinf_cats=('Reconductor',))['harm'].sum())), r4_loc]
        F['summer_2027_band'] = [math.floor(min(fam) * 0.97), math.ceil(max(fam) * 1.03)]
        F['constants'] = {'test_a': 5, 'op_a': 30, 'v_min': 21.2, 'design_c': -27, 'new_load_mw': 2.2,
                          'margin_v': 0.1, 'band_r1_pct': 2, 'band_r2_pct': 2.5, 'band_r5_pct': 4, 'range_pct': 80,
                          'others_core': len(F['rebattery_core'])}
        json.dump(F, open(figures, 'w'), indent=1, default=str)
    return R
