"""task13 architecture 7 (Level 5), independent verifier: recomputes all graded figures directly from target/ using
independent code that shares nothing with golden.py or passes.py (independent SCADA sequence builder, chronological
ALT SRC / NORM SW switching state machine, PDF Z0m and source-impedance parser, first-principles 2-line coupled
zero-sequence nodal solver, dual CST YNd1 IPP infeed inversion, 2D (ESDD, NSDD) daily recurrence and logistic
fog-flashover frontier, IEEE 738 bisection heat balance, RP-04 Rev 5 greedy 36-crew-day allocation, and golden
deliverable checks).

    python3 task13/generator/verify.py
"""
import csv
import datetime as dt
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
FIG = json.load(open(os.path.join(HERE, 'figures.json')))
sys.path.insert(0, HERE)
import common as C  # noqa: E402  (filenames only)

CENTRAL = ZoneInfo('America/Chicago')
CST = dt.timezone(dt.timedelta(hours=-6))
MI = 1.609344
N = {'pass': 0, 'fail': 0}

CREW_DAYS = {
    'wash': 1, 'bird or other animal': 1, 'insulator failure': 2,
    'vegetation grown into the line': 2, 'vegetation from outside the right of way': 3,
    'equipment or hardware other than insulators': 3,
}


def ok(label, cond, detail=''):
    N['pass' if cond else 'fail'] += 1
    print(('PASS  ' if cond else 'FAIL  ') + label + ('' if cond else '  %s' % (detail,)))


def path(key):
    return os.path.join(T, C.FILES[key])


def sheet(key, name, first):
    """Read an Excel sheet from the header row whose first cell equals `first`."""
    ws = openpyxl.load_workbook(path(key), read_only=True, data_only=True)[name]
    rows = [r for r in ws.iter_rows(values_only=True)]
    i = next(k for k, r in enumerate(rows) if r and r[0] == first)
    hdr = [str(c) if c is not None else '' for c in rows[i]]
    return [dict(zip(hdr, x)) for x in rows[i + 1:] if any(c is not None for c in x)]


def _polar(mag, deg):
    return float(mag) * complex(math.cos(math.radians(float(deg))), math.sin(math.radians(float(deg))))


# ---------------------------------------------------------------------------------------------- Network & Studies


def network():
    lines = {}
    for r in sheet('lines', 'Lines', 'Line'):
        n = int(str(r['Line']).split()[1])
        lines[n] = dict(
            a=r['Terminal A'], b=r['Terminal B'], length=float(r['Length (km)']), conductor=r['Conductor'],
            z1=complex(float(r['R1 (ohm/km)']), float(r['X1 (ohm/km)'])),
            z0=complex(float(r['R0 (ohm/km)']), float(r['X0 (ohm/km)'])),
        )
    code = {r['Station']: r['Code'] for r in sheet('subs', 'Stations', 'Code')}
    for L in lines.values():
        L['ca'], L['cb'] = code[L['a']], code[L['b']]
    st = pd.read_csv(path('structures'))
    st['n'] = st['line'].str.split().str[1].astype(int)
    taps = {}
    for r in sheet('lines', 'Taps', 'Tap substation'):
        taps[r['Tap substation']] = dict(
            normal=int(str(r['Line']).split()[1]),
            alt=int(str(r['Second 69 kV source']).split()[1]) if r.get('Second 69 kV source') else None,
        )
    ipp_taps = {}
    for r in sheet('lines', 'IPP taps', 'Facility'):
        ln = int(str(r['Line']).split()[1])
        ipp_taps[ln] = dict(facility=str(r['Facility']), tap_km=float(r['Tap distance from terminal A (km)']))
    retired = [r for r in sheet('subs', 'Transformers', 'Location') if r['Location'] == 'Inland' and r.get('Retired')]
    change = dt.date.fromisoformat(str(retired[0]['Retired'])[:10])
    return lines, st, taps, ipp_taps, change


def study(key):
    txt = subprocess.run(['pdftotext', '-layout', path(key), '-'], capture_output=True, text=True).stdout
    src = {}
    for m in re.finditer(r'^\s*Line (\d+)\s+(.+?)\s{2,}([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$', txt, re.M):
        n, term = int(m.group(1)), m.group(2).strip()
        src[(n, term)] = (_polar(m.group(3), m.group(4)), _polar(m.group(5), m.group(6)))
    zm = re.search(r'Z0m\s*=\s*([\d.]+)\s*\+\s*j([\d.]+)\s*ohm/km', txt)
    z0m = complex(float(zm.group(1)), float(zm.group(2))) if zm else None
    cm = re.search(r'to the\s+([\d.]+)\s*km corridor junction', txt)
    cor_km = float(cm.group(1)) if cm else 14.5
    bm = re.search(r'bus zero-sequence source impedance is\s+([\d.]+)\s*ohm at\s+([\d.]+)\s*degrees', txt)
    z_bus = _polar(bm.group(1), bm.group(2)) if bm else None
    return dict(src=src, z0m=z0m, cor_km=cor_km, z_bus=z_bus)


# ---------------------------------------------------------------------------------------------- SCADA Sequences & Switching


def sequences():
    soe = pd.read_csv(path('soe'))
    soe['t'] = pd.to_datetime(soe['time_utc']).dt.tz_localize('UTC')
    m = soe['point'].str.extract(r'^(\w+) 69KV BKR B(52|62)(\d\d)$')
    soe['end'], soe['ln'] = m[1], m[2]
    lb = soe[soe['ln'].notna()].copy()
    lb['ln'] = lb['ln'].astype(int)
    prot = lb[(lb['state'] == 'OPEN') & (lb['cause'] == 'PROT')].sort_values('t')
    faults = []
    for ln, g in prot.groupby('ln'):
        seq = None
        for _, r in g.iterrows():
            if seq is not None and (r['t'] - seq['t0']).total_seconds() <= 60:
                seq['first'].setdefault(r['end'], r['t'])
                continue
            if seq is not None:
                faults.append(seq)
            seq = dict(ln=ln, t0=r['t'], first={r['end']: r['t']})
        if seq is not None:
            faults.append(seq)
    two = [f for f in faults if {'52', '62'} <= set(f['first'])
           and abs((f['first']['52'] - f['first']['62']).total_seconds()) <= 1.0]
    for f in two:
        f['t'] = pd.Timestamp(min(f['first'].values()))
    return soe, lb, two


def parse_switching(soe, code_to_tap):
    """Independent state machine for planned supervisory switching windows: NORM SW OPEN -> NORM SW CLOSE."""
    sw = soe[soe['point'].str.contains(' 69KV (?:NORM SW|ALT SRC) ', regex=True)].sort_values('t')
    windows = []
    open_norm = {}
    last_alt = {}
    for r in sw.itertuples():
        m_alt = re.match(r'^(\w+) 69KV ALT SRC L(\d+)$', r.point)
        m_norm = re.match(r'^(\w+) 69KV NORM SW L(\d+)$', r.point)
        if m_alt and r.state == 'CLOSE':
            last_alt[m_alt.group(1)] = (int(m_alt.group(2)), r.t)
        elif m_norm:
            rtu, n_ln = m_norm.group(1), int(m_norm.group(2))
            if r.state == 'OPEN':
                alt_ln = last_alt.get(rtu, (None, None))[0]
                open_norm[rtu] = dict(tap=code_to_tap.get(rtu, rtu), rtu=rtu, normal=n_ln, alt=alt_ln, start=r.t)
            elif r.state == 'CLOSE' and rtu in open_norm:
                w = open_norm.pop(rtu)
                w['end'] = r.t
                windows.append(w)
    return windows


def member_walk(soe, lb, faults, taps):
    """Independent 2022-2026 & 2026 chronological as-operated member impact walk."""
    mem = pd.read_csv(path('members'))
    by_ym = mem.groupby(['month', 'substation'])['members'].sum().to_dict()
    tap_code = {s: re.sub(r'\d+$', '', fdr) for fdr, s in zip(mem['feeder'], mem['substation'])}
    code_tap = {v: k for k, v in tap_code.items()}
    windows = parse_switching(soe, code_tap)
    alt_close = soe[soe['point'].str.contains(' 69KV ALT SRC ') & (soe['state'] == 'CLOSE')]

    def active_line_for(tap, t):
        for w in windows:
            if w['tap'] == tap and w['start'] <= t <= w['end'] and w['alt'] is not None:
                return w['alt'], True
        return taps[tap]['normal'], False

    out26 = defaultdict(lambda: [0, 0.0])
    per_fault = {}
    for f in faults:
        lt = f['t'].tz_convert(CENTRAL)
        own = lb[(lb['ln'] == f['ln']) & (lb['t'] >= f['t'] - pd.Timedelta(seconds=1))
                 & (lb['t'] <= f['t'] + pd.Timedelta(days=3))]
        locked = ((own['state'] == 'LOCKOUT') & (own['t'] <= f['t'] + pd.Timedelta(seconds=60))).any()
        later = own[(own['state'] == 'CLOSE') & (own['t'] > f['t'] + pd.Timedelta(seconds=60))]['t']
        mm_f = 0.0
        for tap in taps:
            cur_ln, abnormal = active_line_for(tap, f['t'])
            if cur_ln != f['ln'] or not locked:
                continue
            m = by_ym.get(('%d-%02d' % (lt.year, lt.month), tap), 0)
            ends = []
            if len(later):
                ends.append(later.min())
            if not abnormal:
                a = alt_close[alt_close['point'].str.startswith(tap_code.get(tap, '?') + ' 69KV')
                              & (alt_close['t'] > f['t']) & (alt_close['t'] <= f['t'] + pd.Timedelta(days=3))]['t']
                if len(a):
                    ends.append(a.min())
            secs = (min(ends) - f['t']).total_seconds() if ends else 0.0
            if secs > 300:
                mm = m * secs / 60.0
                mm_f += mm
                if lt.year == 2026:
                    out26[f['ln']][0] += m
                    out26[f['ln']][1] += mm
        per_fault[(f['ln'], round(f['t'].timestamp()))] = mm_f
    return windows, out26, per_fault


# ---------------------------------------------------------------------------------------------- Relays, IPPs & Coupled Z0m


def relay_records():
    recs = []
    er = pd.read_csv(path('er'), dtype=str)
    for _, r in er.iterrows():
        if 'TRIP' not in str(r['Targets']) or str(r['Shot']) != '0':
            continue
        t = dt.datetime.strptime(r['Date'] + ' ' + r['Time'], '%m/%d/%Y %H:%M:%S.%f').replace(tzinfo=dt.timezone.utc)
        loc = r['Location'] if isinstance(r['Location'], str) and re.fullmatch(r'-?[\d.]+', r['Location']) else None
        recs.append(dict(
            st=r['Station'], ln=int(r['Relay'].split('-L')[1]), t=t, type=r['Type'],
            dist=float(loc) * MI if loc else None,
            I={'A': float(r['IA']), 'B': float(r['IB']), 'C': float(r['IC'])}, IG=float(r['IG']),
        ))
    gv = json.load(open(path('gv')))['records']
    for r in gv:
        if not r['trip'] or r['reclose_shot'] != 0:
            continue
        st, ln = re.match(r'^(\w+?)_L(\d+)_', r['device']).groups()
        t = dt.datetime.strptime(r['time_local'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=CENTRAL).astimezone(dt.timezone.utc)
        recs.append(dict(
            st=st, ln=int(ln), t=t, type=r['fault_type'], dist=r['distance_km'],
            I={'A': r['ia_ka'] * 1000, 'B': r['ib_ka'] * 1000, 'C': r['ic_ka'] * 1000}, IG=r['in_ka'] * 1000,
        ))
    return recs


def nearest_rec(recs, st, ln, t, window=900):
    c = [r for r in recs if r['st'] == st and r['ln'] == ln and abs((r['t'] - t).total_seconds()) <= window]
    return min(c, key=lambda r: abs((r['t'] - t).total_seconds())) if c else None


def ipp_records(key):
    df = pd.read_csv(path(key))
    df = df[df['in_ka'].notna()].copy()
    df['t'] = [dt.datetime.strptime(x, '%m/%d/%Y %H:%M:%S.%f').replace(tzinfo=CST).astimezone(dt.timezone.utc)
               for x in df['timestamp']]
    return df


def split_uncoupled(L, za0, zb0, iga, igb):
    f = lambda x: abs(zb0 + (L['length'] - x) * L['z0']) / abs(za0 + x * L['z0']) - iga / igb
    xs = np.linspace(0.01, L['length'] - 0.01, 600)
    vals = [f(x) for x in xs]
    for i in range(len(xs) - 1):
        if vals[i] * vals[i + 1] <= 0:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                if f(lo) * f(mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            return 0.5 * (lo + hi)
    return None


def coupled_ratio(Lf, Lp, z_bus, z_bf, z_bp, z0m, L_cor, x):
    """First-principles coupled 2-line zero-sequence current ratio |I_A|/|I_B| on faulted line Lf at distance x."""
    z0f, z0p = Lf['z0'], Lp['z0']
    Lf_len, Lp_len = Lf['length'], Lp['length']
    c = min(x, L_cor)
    d = max(0.0, L_cor - x)
    # Unknowns: [I_A, I_B, I_p] where I_A flows A->f on Lf, I_B flows B->f on Lf, I_p flows A->B on healthy Lp.
    # KVL equations (reference node: fault voltage Vf = 1.0):
    # 1) Loop A->f: -z_bus*(I_A + I_p) - x*z0f*I_A - c*z0m*I_p = 1
    # 2) Loop B->f: -z_bf*I_B - (Lf_len - x)*z0f*I_B + d*z0m*I_p = 1
    # 3) Loop on healthy Lp (A->B->ground): z_bus*(I_A + I_p) + (Lp_len*z0p + z_bp)*I_p + c*z0m*I_A - d*z0m*I_B = 0
    A = np.array([
        [-(z_bus + x * z0f), 0.0, -(z_bus + c * z0m)],
        [0.0, -(z_bf + (Lf_len - x) * z0f), d * z0m],
        [z_bus + c * z0m, -d * z0m, z_bus + Lp_len * z0p + z_bp],
    ], dtype=complex)
    b = np.array([1.0, 1.0, 0.0], dtype=complex)
    ia, ib, _ = np.linalg.solve(A, b)
    return abs(ia) / abs(ib)


def coupled_location(Lf, Lp, z_bus, z_bf, z_bp, z0m, L_cor, iga, igb):
    target = iga / igb
    xs = np.linspace(0.05, Lf['length'] - 0.05, 400)
    vals = [coupled_ratio(Lf, Lp, z_bus, z_bf, z_bp, z0m, L_cor, x) - target for x in xs]
    for i in range(len(xs) - 1):
        if vals[i] * vals[i + 1] <= 0:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                if (coupled_ratio(Lf, Lp, z_bus, z_bf, z_bp, z0m, L_cor, lo) - target) * \
                   (coupled_ratio(Lf, Lp, z_bus, z_bf, z_bp, z0m, L_cor, mid) - target) <= 0:
                    hi = mid
                else:
                    lo = mid
            return 0.5 * (lo + hi)
    return float(xs[int(np.argmin(np.abs(vals)))])


# ---------------------------------------------------------------------------------------------- 2D (ESDD, NSDD) Model


def deposit_2d(lines, st, gold_rows):
    sw = pd.read_csv(path('stations'), usecols=['station', 'hour_local', 'wind_ms', 'wind_dir_deg', 'rain_mm'])
    sw['day'] = sw['hour_local'].str[:10]
    sw['on'] = (sw['wind_ms'] * np.maximum(0.0, np.cos(np.radians(sw['wind_dir_deg'] - 140.0)))) ** 2
    sw['in'] = (sw['wind_ms'] * np.maximum(0.0, np.cos(np.radians(sw['wind_dir_deg'] - 315.0)))) ** 2
    st_agg = sw.groupby(['station', 'day']).agg(on=('on', 'mean'), dry=('in', 'mean'), rain=('rain_mm', 'sum'))

    ap = pd.read_csv(path('apt'), usecols=['valid', 'drct', 'sknt', 'p01i'], na_values=['M'])
    ap['t'] = pd.to_datetime(ap['valid']).dt.tz_localize('UTC').dt.tz_convert(CENTRAL)
    ap['day'] = ap['t'].dt.strftime('%Y-%m-%d')
    v_ms = pd.to_numeric(ap['sknt'], errors='coerce').fillna(0.0) * 0.514444
    dr = pd.to_numeric(ap['drct'], errors='coerce').fillna(0.0)
    ap['on'] = (v_ms * np.maximum(0.0, np.cos(np.radians(dr - 140.0)))) ** 2
    ap['dry'] = (v_ms * np.maximum(0.0, np.cos(np.radians(dr - 315.0)))) ** 2
    ap['rain'] = pd.to_numeric(ap['p01i'].replace('T', '0'), errors='coerce').fillna(0.0) * 25.4
    ap_agg = ap.groupby('day').agg(on=('on', 'mean'), dry=('dry', 'mean'), rain=('rain', 'sum'))

    pos = {}
    for n, L in lines.items():
        s = st[st['n'] == n].sort_values('km_from_terminal_a')
        pos.setdefault(L['a'].upper() + ' SUB', (s.iloc[0]['latitude'], s.iloc[0]['longitude']))
        pos.setdefault(L['b'].upper() + ' SUB', (s.iloc[-1]['latitude'], s.iloc[-1]['longitude']))
    coastal = {k: v for k, v in pos.items() if k in ('PORT ALCORN SUB', 'SHELL RIDGE SUB', 'SEDGE POINT SUB', 'TULE MARSH SUB')}
    km = lambda a, b: math.hypot((a[1] - b[1]) * 111.32 * math.cos(math.radians(28.2)), (a[0] - b[0]) * 110.95)

    days = [dt.date(2022, 1, 1) + dt.timedelta(days=k) for k in range((dt.date(2026, 10, 31) - dt.date(2022, 1, 1)).days + 1)]
    day_s = [d.isoformat() for d in days]
    day_i = {d: i for i, d in enumerate(days)}

    wx_st = {}
    for cname in coastal:
        sub = st_agg.loc[cname] if cname in st_agg.index.get_level_values(0) else pd.DataFrame()
        on_a, dry_a, rain_a = [], [], []
        both = [k for k in sub.index if k in ap_agg.index]
        sc_on = float(sub.loc[both, 'on'].mean() / max(1e-6, ap_agg.loc[both, 'on'].mean())) if both else 1.0
        sc_dr = float(sub.loc[both, 'dry'].mean() / max(1e-6, ap_agg.loc[both, 'dry'].mean())) if both else 1.0
        for ds in day_s:
            if ds in sub.index:
                r = sub.loc[ds]
                on_a.append(float(r['on']))
                dry_a.append(float(r['dry']))
                rain_a.append(float(r['rain']))
            elif ds in ap_agg.index:
                r = ap_agg.loc[ds]
                on_a.append(float(r['on']) * sc_on)
                dry_a.append(float(r['dry']) * sc_dr)
                rain_a.append(float(r['rain']))
            else:
                on_a.append(0.0); dry_a.append(0.0); rain_a.append(0.0)
        on_a = np.array(on_a) / max(1e-6, float(np.mean(on_a)))
        dry_a = np.array(dry_a) / max(1e-6, float(np.mean(dry_a)))
        wx_st[cname] = (on_a, dry_a, np.array(rain_a))

    sites = sheet('esdd', 'Sites', 'Site')
    reads = pd.DataFrame(sheet('esdd', 'Readings', 'Site'))
    reads['day'] = pd.to_datetime(reads['Date sampled']).dt.date
    near_site = {r['Site']: min(coastal, key=lambda k: km(coastal[k], (r['Latitude'], r['Longitude']))) for r in sites}
    site_info = {r['Site']: (float(r['Gulf shore (km)']), str(r['Corridor surface'])) for r in sites}

    # Independent MLE/nonlinear least-squares fit of (k_esdd, bg_esdd, site_rates) and (k_nsdd, bg_nsdd, site_rates)
    def fit_species(col_name, wind_idx):
        grouped = []
        for s_id, g in reads.groupby('Site'):
            g = g.sort_values('day')
            on_a, dry_a, rain_a = wx_st[near_site[s_id]]
            w_a = on_a if wind_idx == 0 else dry_a
            pts = [(day_i[d], float(v)) for d, v in zip(g['day'], g[col_name]) if d in day_i]
            grouped.append((s_id, w_a, rain_a, pts))

        def loss(params):
            k_r, bg = params[0], params[1]
            if k_r <= 0 or k_r > 0.25 or bg < 0.05 or bg > 0.85:
                return 1e9
            tot = 0.0
            for s_id, w_a, rain_a, pts in grouped:
                # Linear in site rate -> solve optimal site rate analytically per (k_r, bg)
                xs, ys = [], []
                for (i0, v0), (i1, v1) in zip(pts, pts[1:]):
                    decay = 1.0
                    gain = 0.0
                    for j in range(i0 + 1, i1 + 1):
                        dr = math.exp(-k_r * rain_a[j])
                        decay *= dr
                        gain = (gain + (bg + (1.0 - bg) * w_a[j])) * dr
                    xs.append(gain)
                    ys.append(v1 - v0 * decay)
                xs, ys = np.array(xs), np.array(ys)
                rate = max(1e-6, float(np.dot(xs, ys) / max(1e-12, np.dot(xs, xs))))
                pred = np.array([v0 * math.exp(-k_r * rain_a[i0 + 1:i1 + 1].sum()) for (i0, v0), (i1, _) in zip(pts, pts[1:])]) + rate * xs
                obs = np.array([v1 for _, (_, v1) in zip(pts, pts[1:])])
                tot += float(np.sum((np.log(np.maximum(pred, 1e-5)) - np.log(np.maximum(obs, 1e-5))) ** 2))
            return tot

        res = minimize(loss, [0.05 if wind_idx == 0 else 0.005, 0.25], method='Nelder-Mead')
        k_r, bg = float(res.x[0]), float(res.x[1])
        rates = {}
        for s_id, w_a, rain_a, pts in grouped:
            xs, ys = [], []
            for (i0, v0), (i1, v1) in zip(pts, pts[1:]):
                decay, gain = 1.0, 0.0
                for j in range(i0 + 1, i1 + 1):
                    dr = math.exp(-k_r * rain_a[j])
                    decay *= dr
                    gain = (gain + (bg + (1.0 - bg) * w_a[j])) * dr
                xs.append(gain); ys.append(v1 - v0 * decay)
            xs, ys = np.array(xs), np.array(ys)
            rates[s_id] = max(1e-6, float(np.dot(xs, ys) / max(1e-12, np.dot(xs, xs))))
        return k_r, bg, rates

    k_e, bg_e, r_e = fit_species('ESDD (mg/cm2)', 0)
    k_n, bg_n, r_n = fit_species('NSDD (mg/cm2)', 1)

    # Spatial ESDD rate (exponential in gulf_shore_km) and NSDD rate (by surface type)
    sh = np.array([site_info[k][0] for k in r_e])
    ev = np.array([r_e[k] for k in r_e])
    re_fit = minimize(lambda p: float(np.sum((np.log(np.maximum(p[0] * np.exp(-sh / p[1]) + p[2], 1e-7)) - np.log(ev)) ** 2))
                      if p[0] > 0 and 0.3 < p[1] < 10 and p[2] >= 0 else 1e9, [0.006, 1.5, 0.0002], method='Nelder-Mead').x
    surf_n = defaultdict(list)
    for k, v in r_n.items():
        surf_n[site_info[k][1]].append(v)
    surf_n = {k: float(np.mean(v)) for k, v in surf_n.items()}

    # Simulate all 21 sections daily from washes
    secs = sheet('washing', 'Sections', 'Line')
    log = sheet('washing', 'Log', 'Date')
    washed = defaultdict(set)
    for r in log:
        if isinstance(r.get('Date'), dt.datetime):
            washed[(r['Line'], r['Section'])].add(r['Date'].date())

    fog_events = defaultdict(set)
    for r in gold_rows:
        if r['structure'] and r['cause'] == 'salt contamination':
            fog_events[int(r['line'].split()[1])].add((int(r['structure']), dt.date.fromisoformat(r['date'])))

    # Fog nights from coastal weather stations (RH >= 93% or T-Td <= 0.6 C)
    sw_fog = pd.read_csv(path('stations'), usecols=['station', 'hour_local', 'air_temp_c', 'dewpoint_c'])
    sw_fog = sw_fog[sw_fog['station'].isin(coastal)]
    fog_days = set(dt.date.fromisoformat(x[:10]) for x in sw_fog.loc[(sw_fog['air_temp_c'] - sw_fog['dewpoint_c']) <= 0.6, 'hour_local'])

    sec_end = {}
    X_fog, y_fog = [], []
    for r in secs:
        n = int(str(r['Line']).split()[1])
        s0, s1 = int(r['From structure']), int(r['To structure'])
        sub = st[(st['n'] == n) & (st['structure_no'] >= s0) & (st['structure_no'] <= s1)]
        d_km = float(sub['gulf_shore_km'].mean())
        surf = str(sub['corridor_surface'].mode().iloc[0])
        re_s = max(1e-5, float(re_fit[0] * math.exp(-d_km / re_fit[1]) + re_fit[2]))
        rn_s = surf_n.get(surf, float(np.mean(list(surf_n.values()))))
        centre = (float(sub['latitude'].mean()), float(sub['longitude'].mean()))
        cn = min(coastal, key=lambda k: km(coastal[k], centre))
        on_a, dry_a, rain_a = wx_st[cn]
        e, ns = re_s * 20.0, rn_s * 60.0
        wset = washed[(r['Line'], r['Section'])]
        f_dates = {d for s_no, d in fog_events[n] if s0 <= s_no <= s1}
        for i, day in enumerate(days):
            e = (e + re_s * (bg_e + (1.0 - bg_e) * on_a[i])) * math.exp(-k_e * rain_a[i])
            ns = (ns + rn_s * (bg_n + (1.0 - bg_n) * dry_a[i])) * math.exp(-k_n * rain_a[i])
            if day in wset:
                e, ns = 0.002, 0.015
            if day in fog_days or day in f_dates:
                X_fog.append((math.log(max(e, 1e-5)), math.log(max(ns / 0.20, 1e-5))))
                y_fog.append(1.0 if day in f_dates else 0.0)
        sec_end['%s, %s' % (r['Line'], r['Section'])] = (e, ns)

    X_fog, y_fog = np.array(X_fog), np.array(y_fog)
    def nll(p):
        z = np.clip(p[0] + p[1] * X_fog[:, 0] + p[2] * X_fog[:, 1], -30, 30)
        return float(np.sum(np.logaddexp(0.0, z) - y_fog * z))
    opt = minimize(nll, [-5.0, 2.0, 1.2], method='BFGS').x
    beta = float(opt[2] / opt[1])
    fl_ceff = [math.exp(x[0] + beta * x[1]) for x, y in zip(X_fog, y_fog) if y > 0.5]
    level = float(np.percentile(fl_ceff, 10))
    ratios = {k: (e * ((ns / 0.20) ** beta)) / level for k, (e, ns) in sec_end.items()}
    due = sorted(k for k, rat in ratios.items() if rat >= 1.0)
    return due, beta, level, k_e, k_n, ratios


# ---------------------------------------------------------------------------------------------- IEEE 738 Conductor Heat


IEEE = dict(
    r25={'477 ACSR Hawk': 0.1196, '795 ACSR Drake': 0.0727, '336.4 ACSR Linnet': 0.1702},
    r75={'477 ACSR Hawk': 0.1430, '795 ACSR Drake': 0.0869, '336.4 ACSR Linnet': 0.2035},
    d={'477 ACSR Hawk': 21.8, '795 ACSR Drake': 28.1, '336.4 ACSR Linnet': 18.3},
)


def conductor(i, cond, ta, v, q=850.0):
    d = IEEE['d'][cond] / 1000.0
    a = (IEEE['r75'][cond] / IEEE['r25'][cond] - 1.0) / 50.0
    v = max(0.3, v)
    lo, hi = ta, ta + 150.0
    for _ in range(40):
        tc = 0.5 * (lo + hi)
        tf = 0.5 * (tc + ta)
        kf = 2.424e-2 + 7.477e-5 * tf
        mu = 1.458e-6 * (tf + 273.0) ** 1.5 / (tf + 383.4)
        re_ = d * 1.165 * v / mu
        qc = max(1.01 + 1.35 * re_ ** 0.52, 0.754 * re_ ** 0.6) * kf * (tc - ta)
        qr = 17.8 * d * 0.5 * (((tc + 273.0) / 100.0) ** 4 - ((ta + 273.0) / 100.0) ** 4)
        qj = i * i * IEEE['r25'][cond] / 1000.0 * (1.0 + a * (tc - 25.0))
        if qj + 0.5 * q * d - qc - qr > 0:
            lo = tc
        else:
            hi = tc
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------------------------- Main Verifier


def main():
    lines, st, taps, ipp_taps, change = network()
    s22, s25 = study('study22'), study('study25')
    ok('studies parsed: 32 terminals + Z0m + Inland bus Z0 in both PDFs',
       len(s22['src']) == 32 and len(s25['src']) == 32 and s22['z0m'] is not None and s25['z0m'] is not None
       and s22['z_bus'] is not None and s25['z_bus'] is not None,
       (len(s22['src']), len(s25['src']), s22['z0m'], s25['z_bus']))

    # R1: fault sequences
    soe, lb, faults = sequences()
    yr = Counter(str(f['t'].tz_convert(CENTRAL).year) for f in faults)
    ok('R1 conformed faults by year from SCADA two-ended sequences',
       dict(yr) == FIG['faults_by_year'], (dict(yr), FIG['faults_by_year']))

    # R6 (S5): chronological SCADA switching state machine & 2026 member impact
    windows, walk26, per_fault = member_walk(soe, lb, faults, taps)
    tot26 = [sum(v[0] for v in walk26.values()), sum(v[1] for v in walk26.values())]
    g6 = FIG['member_impact_2026']
    ok('R6 (S5) 26 planned SCADA ALT SRC / NORM SW windows recovered independently',
       len(windows) == FIG['switching_windows_count'], (len(windows), FIG['switching_windows_count']))
    ok('R6 (S5) 2026 sustained member interruptions within 2 percent',
       abs(tot26[0] - g6['sustained']) <= 0.02 * g6['sustained'], (tot26[0], g6['sustained']))
    ok('R6 (S5) 2026 conformed member-minutes within 2 percent',
       abs(tot26[1] - g6['member_minutes']) <= 0.02 * g6['member_minutes'], (round(tot26[1]), g6['member_minutes']))
    bad_l = []
    for name, v in FIG['member_impact_2026_by_line'].items():
        n = int(name.split()[1])
        w = walk26.get(n, [0, 0.0])
        if abs(w[0] - v['sustained']) > 0.02 * v['sustained'] + 1 or abs(w[1] - v['member_minutes']) > 0.02 * v['member_minutes'] + 1:
            bad_l.append((name, w, v))
    ok('R6 (S5) every line 2026 member impact within 2 percent', not bad_l, bad_l)

    # Read golden CSV deliverable
    gold_csv = os.path.join(TASK, 'golden', C.DELIVERABLES[0])
    rows = list(csv.DictReader(open(gold_csv)))
    ok('golden CSV row count and annual distribution match figures.json',
       len(rows) == FIG['faults_total'] and dict(Counter(r['date'][:4] for r in rows)) == FIG['faults_by_year'])
    names = {'lightning': 'lightning', 'bird': 'bird or other animal', 'fog': 'salt contamination',
             'insulator': 'insulator failure', 'growin': 'vegetation grown into the line',
             'fallin': 'vegetation from outside the right of way', 'vehicle': 'vehicle or other third party',
             'hardware': 'equipment or hardware other than insulators', 'unknown': 'other or unknown'}
    c26 = Counter(r['cause'] for r in rows if r['date'].startswith('2026'))
    ok('golden CSV 2026 causes match figures.json',
       {k: c26.get(v, 0) for k, v in names.items()} == FIG['faults_2026_by_cause'])

    # R3 (S2) & R4 (S3): independent re-location of all repeat locations (coupled Z0m + dual YNd1 IPP infeed)
    recs = relay_records()
    ipp_dfs = {9: ipp_records('ipp'), 8: ipp_records('ipp2')}
    groups = defaultdict(list)
    for r in rows:
        if r['repeat_location']:
            groups[r['repeat_location']].append(r)

    far, dc_ok, ipp_ok = [], {}, {}
    for rl, fs in sorted(groups.items()):
        n = int(fs[0]['line'].split()[1])
        L = lines[n]
        placed = []
        for r in fs:
            if r['fault_type'] not in ('AG', 'BG', 'CG'):
                continue
            t = dt.datetime.fromisoformat(r['date'] + 'T' + r['time']).replace(tzinfo=CENTRAL).astimezone(dt.timezone.utc)
            st_info = s22 if t.date() < change else s25
            ra, rb = nearest_rec(recs, L['ca'], n, t), nearest_rec(recs, L['cb'], n, t)
            x = None
            if ra and rb:
                if n in (10, 11):
                    Lp = lines[11 if n == 10 else 10]
                    x = coupled_location(
                        L, Lp, st_info['z_bus'],
                        st_info['src'][(n, L['b'])][1], st_info['src'][(11 if n == 10 else 10, Lp['b'])][1],
                        st_info['z0m'], st_info['cor_km'], ra['IG'], rb['IG'],
                    )
                else:
                    x = split_uncoupled(L, st_info['src'][(n, L['a'])][1], st_info['src'][(n, L['b'])][1], ra['IG'], rb['IG'])
            elif ra and ra['dist'] is not None and n in ipp_taps and ra['dist'] > ipp_taps[n]['tap_km']:
                idf = ipp_dfs[n]
                j = idf.iloc[int(np.argmin([abs((u - t).total_seconds()) for u in idf['t']]))]
                if abs((j['t'] - t).total_seconds()) <= 2.0:
                    k0 = abs((L['z0'] - L['z1']) / (3 * L['z1']))
                    p = r['fault_type'][0]
                    it = {'A': j['ia_ka'], 'B': j['ib_ka'], 'C': j['ic_ka']}[p] * 1000.0
                    k = (it + k0 * j['in_ka'] * 1000.0) / (ra['I'][p] + k0 * ra['IG'])
                    tk = ipp_taps[n]['tap_km']
                    x = tk + (ra['dist'] - tk) / (1.0 + k)
            elif (ra is None) != (rb is None):
                rr_ = ra or rb
                if rr_['dist'] is not None:
                    x = rr_['dist'] if rr_ is ra else L['length'] - rr_['dist']
            if x is not None:
                s_df = st[st['n'] == n]
                placed.append(int(s_df.iloc[int(np.argmin(np.abs(s_df['km_from_terminal_a'].to_numpy() - x)))]['structure_no']))
        mine = int(round(float(np.median(placed)))) if placed else None
        gold_s = Counter(int(r['structure']) for r in fs if r['structure']).most_common(1)[0][0]
        if mine is None or abs(mine - gold_s) > 2:
            far.append((rl, fs[0]['line'], fs[0]['cause'], gold_s, mine))
        if n in (8, 9) and fs[0]['cause'] == 'insulator failure':
            ipp_ok[n] = (mine, gold_s)
        if (n == 11 and fs[0]['cause'] == 'insulator failure') or (n == 10 and fs[0]['cause'] == 'vegetation grown into the line' and gold_s < 85):
            dc_ok[(n, fs[0]['cause'])] = (mine, gold_s)
    ok('R3 (S2) both YNd1 IPP strings independently inverted within 2 structures (Line 8 str 93, Line 9 str 137)',
       8 in ipp_ok and 9 in ipp_ok and abs(ipp_ok[8][0] - FIG['ipp_details']['Line 8']['golden_structure']) <= 2
       and abs(ipp_ok[9][0] - FIG['ipp_details']['Line 9']['golden_structure']) <= 2, ipp_ok)
    ok('R4 (S3) both double-circuit corridor targets independently inverted with Z0m within 2 structures',
       (11, 'insulator failure') in dc_ok and (10, 'vegetation grown into the line') in dc_ok
       and abs(dc_ok[(11, 'insulator failure')][0] - FIG['dc_corridor_details']['Line 11 insulator']['golden_structure']) <= 2
       and abs(dc_ok[(10, 'vegetation grown into the line')][0] - FIG['dc_corridor_details']['Line 10 growin']['golden_structure']) <= 2,
       dc_ok)
    ok('all 27 repeat locations independently re-located within 2 structures from target/', not far, far)

    # R5 (S4): independent 2D (ESDD, NSDD) coastal washing standing
    due, beta, level, k_e, k_n, ratios = deposit_2d(lines, st, rows)
    gw = sorted(x.replace('wash: ', '') for x in FIG['wash_due'])
    ok('R5 (S4) independent 2D (ESDD, NSDD) model reproduces exact 9 due coastal washing sections',
       due == gw, (sorted(set(due) ^ set(gw)), round(beta, 3), round(level, 4)))
    ok('R5 (S4) independent k_ESDD / k_NSDD differential washout confirmed (k_ESDD > 3 * k_NSDD)',
       k_e > 3.0 * k_n and 0.30 <= beta <= 1.0, (round(k_e, 4), round(k_n, 4), round(beta, 3)))

    # R2 (S1): independent IEEE 738 thermal sag trajectories on underbuilt spans
    load = pd.read_csv(path('loading'))
    load['h'] = pd.to_datetime(load['hour_utc']).dt.tz_localize('UTC')
    load = load.set_index('h')
    sw = pd.read_csv(path('stations'), usecols=['station', 'hour_local', 'air_temp_c', 'wind_ms'])
    swi = {(r.station, r.hour_local): (r.air_temp_c, r.wind_ms) for r in sw.itertuples()}
    apt = pd.read_csv(path('apt'), usecols=['valid', 'tmpf', 'sknt'], na_values=['M'])
    ina = pd.read_csv(path('inl_apt'), usecols=['valid', 'tmpf', 'sknt'], na_values=['M'])
    def asos(df):
        df = df.copy()
        df['h'] = pd.to_datetime(df['valid']).dt.tz_localize('UTC').dt.floor('h')
        return {r.h: ((r.tmpf - 32) * 5 / 9, (r.sknt or 0) * 0.514444) for r in df.itertuples()}
    apd, inad = asos(apt), asos(ina)
    spos = {}
    for n, L in lines.items():
        s_ = st[st['n'] == n].sort_values('km_from_terminal_a')
        spos.setdefault(L['a'].upper() + ' SUB', (s_.iloc[0]['latitude'], s_.iloc[0]['longitude']))
        spos.setdefault(L['b'].upper() + ' SUB', (s_.iloc[-1]['latitude'], s_.iloc[-1]['longitude']))
    spos = {k: v for k, v in spos.items() if k in set(sw['station'])}
    kmf = lambda a, b: math.hypot((a[1] - b[1]) * 111.32 * math.cos(math.radians(28.2)), (a[0] - b[0]) * 110.95)
    town = {
        'APT': spos['PORT ALCORN SUB'],
        'INA': (float(st[st['n'] == 10].sort_values('km_from_terminal_a').iloc[0]['latitude']),
                float(st[st['n'] == 10].sort_values('km_from_terminal_a').iloc[0]['longitude'])),
    }
    veg = pd.read_csv(path('veg'))
    ub_set = set(zip(st.loc[st['underbuild'].fillna('').astype(str).str.len() > 0, 'n'],
                     st.loc[st['underbuild'].fillna('').astype(str).str.len() > 0, 'structure_no']))
    hw_slopes, ub_grow_slopes = {}, {}
    for rl, fs in sorted(groups.items()):
        if fs[0]['cause'] not in ('vegetation grown into the line', 'equipment or hardware other than insulators'):
            continue
        n = int(fs[0]['line'].split()[1])
        L = lines[n]
        nos = [int(r['structure']) for r in fs if r['structure']]
        lo, hi = min(nos) - 1, max(nos) + 1
        if not any((n, s_no) in ub_set for s_no in range(lo, hi + 1)):
            continue
        last = max(dt.date.fromisoformat(r['date']) for r in fs)
        vv = veg[(veg['line'] == 'Line %d' % n) & veg['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])]
        trims = [dt.date.fromisoformat(str(x.completed)[:10]) for x in vv.itertuples()
                 if int(x.from_structure) <= hi and lo <= int(x.to_structure)
                 and dt.date.fromisoformat(str(x.completed)[:10]) <= last]
        tt = max(trims) if trims else None
        xs, ys = [], []
        for r in fs:
            dd = dt.date.fromisoformat(r['date'])
            if tt is not None and dd <= tt:
                continue
            t = dt.datetime.fromisoformat(r['date'] + 'T' + r['time']).replace(tzinfo=CENTRAL)
            if not (5 <= dd.month <= 9 and 11 <= t.hour <= 20):
                continue
            h = t.astimezone(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
            col = [c for c in load.columns if c.endswith('_L%d_AMPS' % n)]
            if not col or h not in load.index:
                continue
            amps = float(load.loc[h, col[0]])
            sub = st[(st['n'] == n) & (st['structure_no'] == int(r['structure']))]
            p = (float(sub.iloc[0]['latitude']), float(sub.iloc[0]['longitude']))
            wx = None
            for k in sorted(spos, key=lambda k: kmf(spos[k], p))[:2]:
                if kmf(spos[k], p) <= 18.0 and (k, t.strftime('%Y-%m-%d %H:00')) in swi:
                    wx = swi[(k, t.strftime('%Y-%m-%d %H:00'))]
                    break
            if wx is None:
                wx = (inad if kmf(town['INA'], p) < kmf(town['APT'], p) else apd).get(h)
            if wx is None:
                continue
            xs.append(dd.year + dd.timetuple().tm_yday / 365.25)
            ys.append(conductor(amps, L['conductor'], float(wx[0]), float(wx[1])))
        if len(xs) >= 3 and len(set(int(x) for x in xs)) >= 2:
            slp = float(np.polyfit(xs, ys, 1)[0])
            if fs[0]['cause'].startswith('equipment'):
                hw_slopes[fs[0]['line']] = round(slp, 2)
            else:
                ub_grow_slopes[fs[0]['line']] = round(slp, 2)
    ok('R2 (S1) independent IEEE 738 slopes separate Line 6 & Line 15 clearance (> -0.5) from Line 12 & Line 14 grow-ins (< -1.8)',
       set(hw_slopes) == {'Line 6', 'Line 15'} and all(v > -0.5 for v in hw_slopes.values())
       and {'Line 12', 'Line 14'} <= set(ub_grow_slopes) and all(ub_grow_slopes[k] < -1.8 for k in ('Line 12', 'Line 14')),
       (hw_slopes, ub_grow_slopes))

    # R10 & Golden XLSX / DOCX consistency: independent greedy 36-crew-day Priority 1 allocation
    wb = openpyxl.load_workbook(os.path.join(TASK, 'golden', C.DELIVERABLES[1]), data_only=True)
    ok('golden workbook carries all 10 required review sheets', len(wb.sheetnames) == 10, wb.sheetnames)
    rep_rows = [r for r in wb['Repeat locations'].iter_rows(values_only=True)]
    hdr_i = next(i for i, r in enumerate(rep_rows) if r and r[0] == 'Ref')
    open_items = []
    for r in rep_rows[hdr_i + 1:]:
        if not r or not r[0] or str(r[11]).startswith('Fixed'):
            continue
        open_items.append(dict(rid=r[0], line=r[1], str=str(r[2]), cause=r[3], days=int(r[7]), mmd=int(r[9]), status=str(r[11])))
    rem = 36 - len(due)
    p1_ind, p2_ind = [], []
    for item in sorted(open_items, key=lambda x: (-x['mmd'], x['line'], x['str'])):
        if item['days'] <= rem:
            p1_ind.append(item)
            rem -= item['days']
        else:
            p2_ind.append(item)
    ok('R10 independent greedy 36-crew-day allocation matches golden workbook Priority 1 (13 funded, 6 deferred, 0 unused)',
       rem == 0 and len(p1_ind) == 13 and len(p2_ind) == 6
       and all(x['status'].startswith('Priority 1') for x in p1_ind)
       and all(x['status'].startswith('Priority 2') for x in p2_ind),
       (rem, len(p1_ind), len(p2_ind)))

    memo_xml = subprocess.run(['unzip', '-p', os.path.join(TASK, 'golden', C.DELIVERABLES[2]), 'word/document.xml'],
                              capture_output=True, text=True).stdout
    memo_txt = re.sub(r'<[^>]+>', ' ', memo_xml)
    ok('golden one-page Word memo addresses C. Ortiz and cites 36 crew-days and 5,376,602 member-minutes',
       'C. Ortiz' in memo_txt and '36 crew-days' in memo_txt and f"{FIG['member_impact_2026']['member_minutes']:,}" in memo_txt)

    print('%d passed, %d failed' % (N['pass'], N['fail']))
    return 1 if N['fail'] else 0


if __name__ == '__main__':
    sys.exit(main())
