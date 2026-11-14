"""task13 architecture 6, the independent verifier: the graded figures recomputed from target/ by code that shares
nothing with golden.py or passes.py (its own sequence builder, member walk, study parser, residual-split solver, tap
infeed correction, wind-driven deposit model and conductor heat balance), each checked against figures.json inside its band. The one input taken from the
golden deliverables is the fault table's grouping of faults into repeat locations and its causes, which checks.py
holds against the simulated world; every place and the washing list are re-derived here from the pack.

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

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
FIG = json.load(open(os.path.join(HERE, 'figures.json')))
sys.path.insert(0, HERE)
import common as C  # noqa: E402  (file names only)

CENTRAL = ZoneInfo('America/Chicago')
CST = dt.timezone(dt.timedelta(hours=-6))
MI = 1.609344
N = {'pass': 0, 'fail': 0}


def ok(label, cond, detail=''):
    N['pass' if cond else 'fail'] += 1
    print(('PASS  ' if cond else 'FAIL  ') + label + ('' if cond else '  %s' % (detail,)))


def path(key):
    return os.path.join(T, C.FILES[key])


def sheet(key, name, first):
    """a sheet's rows as dicts, from the header row whose first cell reads `first`"""
    ws = openpyxl.load_workbook(path(key), read_only=True, data_only=True)[name]
    rows = [r for r in ws.iter_rows(values_only=True)]
    i = next(k for k, r in enumerate(rows) if r and r[0] == first)
    hdr = [str(c) if c is not None else '' for c in rows[i]]
    return [dict(zip(hdr, x)) for x in rows[i + 1:] if any(c is not None for c in x)]


# ---------------------------------------------------------------------------------------------- the network


def network():
    lines = {}
    for r in sheet('lines', 'Lines', 'Line'):
        n = int(str(r['Line']).split()[1])
        lines[n] = dict(a=r['Terminal A'], b=r['Terminal B'], length=float(r['Length (km)']), conductor=r['Conductor'],
                        z1=complex(float(r['R1 (ohm/km)']), float(r['X1 (ohm/km)'])),
                        z0=complex(float(r['R0 (ohm/km)']), float(r['X0 (ohm/km)'])))
    code = {r['Station']: r['Code'] for r in sheet('subs', 'Stations', 'Code')}
    for L in lines.values():
        L['ca'], L['cb'] = code[L['a']], code[L['b']]
    st = pd.read_csv(path('structures'))
    st['n'] = st['line'].str.split().str[1].astype(int)
    taps = defaultdict(list)
    for r in sheet('lines', 'Taps', 'Tap substation'):
        taps[int(str(r['Line']).split()[1])].append(r['Tap substation'])
    solar = {str(r['Item']): r['Value'] for r in sheet('lines', 'Solar tap', 'Item')}
    tap_km = float([v for k, v in solar.items() if k.startswith('Tap point')][0])
    retired = [r for r in sheet('subs', 'Transformers', 'Location') if r['Location'] == 'Inland' and r.get('Retired')]
    change = dt.date.fromisoformat(str(retired[0]['Retired'])[:10])
    return lines, st, taps, tap_km, change


def study(key):
    txt = subprocess.run(['pdftotext', '-layout', path(key), '-'], capture_output=True, text=True).stdout
    out = {}
    for m in re.finditer(r'^\s*Line (\d+)\s+(.+?)\s{2,}([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$', txt, re.M):
        n, term = int(m.group(1)), m.group(2).strip()
        z = lambda mag, ang: mag * complex(math.cos(math.radians(ang)), math.sin(math.radians(ang)))
        out[(n, term)] = (z(float(m.group(3)), float(m.group(4))), z(float(m.group(5)), float(m.group(6))))
    return out


# ---------------------------------------------------------------------------------------------- R1 and R5


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
    two = [f for f in faults if {'52', '62'} <= set(f['first']) and
           abs((f['first']['52'] - f['first']['62']).total_seconds()) <= 1.0]
    for f in two:
        f['t'] = pd.Timestamp(min(f['first'].values()))
    return soe, lb, two


def member_walk(soe, lb, faults, taps):
    mem = pd.read_csv(path('members'))
    by = mem.groupby(['month', 'substation'])['members'].sum().to_dict()
    code = {s: re.sub(r'\d+$', '', fdr) for fdr, s in zip(mem['feeder'], mem['substation'])}
    alt = soe[soe['point'].str.contains(' 69KV ALT SRC ') & (soe['state'] == 'CLOSE')]
    out = defaultdict(lambda: [0, 0.0])
    for f in faults:
        lt = f['t'].tz_convert(CENTRAL)
        if lt.year != 2026:
            continue
        own = lb[(lb['ln'] == f['ln']) & (lb['t'] >= f['t'] - pd.Timedelta(seconds=1)) & (lb['t'] <= f['t'] + pd.Timedelta(days=3))]
        locked = ((own['state'] == 'LOCKOUT') & (own['t'] <= f['t'] + pd.Timedelta(seconds=60))).any()
        later = own[(own['state'] == 'CLOSE') & (own['t'] > f['t'] + pd.Timedelta(seconds=60))]['t']
        for tap in taps.get(f['ln'], []):
            m = by.get(('%d-%02d' % (lt.year, lt.month), tap), 0)
            if not locked:
                continue
            a = alt[alt['point'].str.startswith(code.get(tap, '?') + ' 69KV') & (alt['t'] > f['t']) &
                    (alt['t'] <= f['t'] + pd.Timedelta(days=3))]['t']
            ends = [x for x in (a.min() if len(a) else None, later.min() if len(later) else None) if x is not None]
            secs = (min(ends) - f['t']).total_seconds() if ends else 0.0
            if secs > 300:
                out[f['ln']][0] += m
                out[f['ln']][1] += m * secs / 60.0
    return out


# ---------------------------------------------------------------------------------------------- the relay records


def relay_records():
    recs = []
    er = pd.read_csv(path('er'), dtype=str)
    for _, r in er.iterrows():
        if 'TRIP' not in str(r['Targets']) or str(r['Shot']) != '0':
            continue
        t = dt.datetime.strptime(r['Date'] + ' ' + r['Time'], '%m/%d/%Y %H:%M:%S.%f').replace(tzinfo=dt.timezone.utc)
        loc = r['Location'] if isinstance(r['Location'], str) and re.fullmatch(r'-?[\d.]+', r['Location']) else None
        recs.append(dict(st=r['Station'], ln=int(r['Relay'].split('-L')[1]), t=t, type=r['Type'],
                         dist=float(loc) * MI if loc else None,
                         I={'A': float(r['IA']), 'B': float(r['IB']), 'C': float(r['IC'])}, IG=float(r['IG'])))
    gv = json.load(open(path('gv')))['records']
    for r in gv:
        if not r['trip'] or r['reclose_shot'] != 0:
            continue
        st, ln = re.match(r'^(\w+?)_L(\d+)_', r['device']).groups()
        t = dt.datetime.strptime(r['time_local'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=CENTRAL).astimezone(dt.timezone.utc)
        recs.append(dict(st=st, ln=int(ln), t=t, type=r['fault_type'], dist=r['distance_km'],
                         I={'A': r['ia_ka'] * 1000, 'B': r['ib_ka'] * 1000, 'C': r['ic_ka'] * 1000}, IG=r['in_ka'] * 1000))
    return recs


def nearest(recs, st, ln, t, window=900):
    c = [r for r in recs if r['st'] == st and r['ln'] == ln and abs((r['t'] - t).total_seconds()) <= window]
    return min(c, key=lambda r: abs((r['t'] - t).total_seconds())) if c else None


def split_location(L, za0, zb0, iga, igb):
    """the distance from terminal A at which the residual current divides between the ends as recorded"""
    f = lambda x: abs(zb0 + (L['length'] - x) * L['z0']) / abs(za0 + x * L['z0']) - iga / igb
    xs = np.linspace(0.01, L['length'] - 0.01, 600)
    v = [f(x) for x in xs]
    for i in range(len(xs) - 1):
        if v[i] * v[i + 1] <= 0:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(60):
                mid = (lo + hi) / 2
                if f(lo) * f(mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            return (lo + hi) / 2
    return None


def solar_records():
    ipp = pd.read_csv(path('ipp'))
    ipp = ipp[ipp['in_ka'].notna()].copy()
    ipp['t'] = [dt.datetime.strptime(x, '%m/%d/%Y %H:%M:%S.%f').replace(tzinfo=CST).astimezone(dt.timezone.utc) for x in ipp['timestamp']]
    return ipp


# ---------------------------------------------------------------------------------------------- the deposits


def onshore_days(pos):
    """each Central day's onshore exposure at each coastal substation station: the mean squared wind component from the
    south-east (the Gulf's side of this shore, 140 degrees), the Port Alcorn airport scaled in before the station reads"""
    sw = pd.read_csv(path('stations'), usecols=['station', 'hour_local', 'wind_ms', 'wind_dir_deg'])
    sw['day'] = sw['hour_local'].str[:10]
    sw['e'] = (sw['wind_ms'] * np.maximum(0.0, np.cos(np.radians(sw['wind_dir_deg'] - 140.0)))) ** 2
    st_e = sw.groupby(['station', 'day'])['e'].mean()
    ap = pd.read_csv(path('apt'), usecols=['valid', 'drct', 'sknt'], na_values=['M'])
    ap['t'] = pd.to_datetime(ap['valid']).dt.tz_localize('UTC').dt.tz_convert(CENTRAL)
    ap['day'] = ap['t'].dt.strftime('%Y-%m-%d')
    ap['e'] = (pd.to_numeric(ap['sknt'], errors='coerce').fillna(0) * 0.514444 *
               np.maximum(0.0, np.cos(np.radians(pd.to_numeric(ap['drct'], errors='coerce').fillna(0) - 140.0)))) ** 2
    ap_e = ap.groupby('day')['e'].mean().to_dict()
    out = {}
    for n in pos:
        if n not in st_e.index.get_level_values(0):
            continue
        se = st_e.loc[n].to_dict()
        both = [k for k in se if k in ap_e]
        sc = float(np.mean([se[k] for k in both]) / np.mean([ap_e[k] for k in both]))
        ser = {k: v * sc for k, v in ap_e.items()}
        ser.update(se)
        m = float(np.mean(list(ser.values())))
        out[n] = {k: v / m for k, v in ser.items()}
    return out


def deposit_list(lines, st, gold_rows):
    sw = pd.read_csv(path('stations'), usecols=['station', 'hour_local', 'rain_mm'])
    sw['day'] = sw['hour_local'].str[:10]
    st_rain = sw.groupby(['station', 'day'])['rain_mm'].sum().to_dict()
    ap = pd.read_csv(path('apt'), usecols=['valid', 'p01i'])
    ap['t'] = pd.to_datetime(ap['valid']).dt.tz_localize('UTC').dt.tz_convert(CENTRAL)
    ap['day'] = ap['t'].dt.strftime('%Y-%m-%d')
    ap['mm'] = pd.to_numeric(ap['p01i'].replace('T', '0'), errors='coerce').fillna(0) * 25.4
    ap_rain = ap.groupby('day')['mm'].sum().to_dict()
    # each weather station sits at its substation: the substation's end structure in the inventory
    pos = {}
    for n, L in lines.items():
        s = st[st['n'] == n].sort_values('km_from_terminal_a')
        pos.setdefault(L['a'].upper() + ' SUB', (s.iloc[0]['latitude'], s.iloc[0]['longitude']))
        pos.setdefault(L['b'].upper() + ' SUB', (s.iloc[-1]['latitude'], s.iloc[-1]['longitude']))
    stations = sorted(set(sw['station']))
    pos = {k: v for k, v in pos.items() if k in stations}
    coastal = {k: v for k, v in pos.items() if k in ('PORT ALCORN SUB', 'SHELL RIDGE SUB', 'SEDGE POINT SUB', 'TULE MARSH SUB')}
    km = lambda a, b: math.hypot((a[1] - b[1]) * 111.32 * math.cos(math.radians(28.2)), (a[0] - b[0]) * 110.95)
    expo = onshore_days(coastal)

    def rain(names, day):
        v = [st_rain.get((n, day)) for n in names]
        v = [x for x in v if x is not None]
        return float(np.mean(v)) if v else float(ap_rain.get(day, 0.0))

    def fac(names, day):
        v = [expo[n].get(day) for n in names if n in expo]
        v = [x for x in v if x is not None]
        return float(np.mean(v)) if v else 1.0

    BG = 0.25
    sites = sheet('esdd', 'Sites', 'Site')
    reads = pd.DataFrame(sheet('esdd', 'Readings', 'Site'))
    reads['day'] = pd.to_datetime(reads['Date sampled']).dt.date
    near_site = {r['Site']: [min(coastal, key=lambda k: km(coastal[k], (r['Latitude'], r['Longitude'])))] for r in sites}
    shore = {r['Site']: float(r['Gulf shore (km)']) for r in sites}
    rates, keeps = {}, []
    for site, g in reads.groupby('Site'):
        g = g.sort_values('day')
        vals = list(zip(g['day'], g['ESDD (mg/cm2)'].astype(float)))
        num = den = 0.0
        for (d0, e0), (d1, e1) in zip(vals, vals[1:]):
            days = (d1 - d0).days
            span = [(d0 + dt.timedelta(days=k)).isoformat() for k in range(1, days + 1)]
            rr = [rain(near_site[site], x) for x in span]
            if days >= 10 and max(rr) < 5.0 and e1 > e0:
                x = sum(BG + (1 - BG) * fac(near_site[site], y) for y in span)
                num += (e1 - e0) * x
                den += x * x
        if den:
            rates[site] = num / den
    for site, g in reads.groupby('Site'):
        g = g.sort_values('day')
        vals = list(zip(g['day'], g['ESDD (mg/cm2)'].astype(float)))
        for (d0, e0), (d1, e1) in zip(vals, vals[1:]):
            days = (d1 - d0).days
            span = [(d0 + dt.timedelta(days=k)).isoformat() for k in range(1, days + 1)]
            rr = [rain(near_site[site], x) for x in span]
            if sum(x >= 12.0 for x in rr) == 1 and not any(5.0 <= x < 12.0 for x in rr):
                acc = rates.get(site, 0.0) * sum(BG + (1 - BG) * fac(near_site[site], y) for y in span)
                keeps.append(max(0.0, e1 - acc) / e0)
    keep = float(np.median(keeps))
    # the rate between the coastal sites, log-linear in distance on those within 5 km of the Gulf
    cs = [k for k in rates if shore[k] <= 5.0]
    b1, b0 = np.polyfit([shore[k] for k in cs], np.log([rates[k] for k in cs]), 1)
    secs = sheet('washing', 'Sections', 'Line')
    log = sheet('washing', 'Log', 'Date')
    washed = defaultdict(set)
    for r in log:
        if isinstance(r.get('Date'), dt.datetime):
            washed[(r['Line'], r['Section'])].add(r['Date'].date())
    fog_days = defaultdict(list)
    ins_days = defaultdict(list)
    for r in gold_rows:
        if r['structure'] and r['cause'] in ('salt contamination', 'insulator failure'):
            (fog_days if r['cause'] == 'salt contamination' else ins_days)[int(r['line'].split()[1])].append(
                (int(r['structure']), dt.date.fromisoformat(r['date'])))
    series, at_flash, at_ins = {}, [], []
    for r in secs:
        n = int(str(r['Line']).split()[1])
        s0, s1 = int(r['From structure']), int(r['To structure'])
        sub = st[(st['n'] == n) & (st['structure_no'] >= s0) & (st['structure_no'] <= s1)]
        rate = math.exp(b0 + b1 * float(sub['gulf_shore_km'].mean()))
        names = [k for k in (L.upper() + ' SUB' for L in (lines[n]['a'], lines[n]['b'])) if k in coastal]
        if not names:
            centre = (float(sub['latitude'].mean()), float(sub['longitude'].mean()))
            names = sorted(coastal, key=lambda k: km(coastal[k], centre))[:1]
        dep, day, ser = rate * 60.0, dt.date(2022, 1, 1), {}
        while day <= dt.date(2026, 10, 31):
            dep += rate * (BG + (1 - BG) * fac(names, day.isoformat()))
            x = rain(names, day.isoformat())
            dep *= keep if x >= 12.0 else (0.85 if x >= 5.0 else 1.0)
            if day in washed[(r['Line'], r['Section'])]:
                dep = 0.003
            ser[day] = dep
            day += dt.timedelta(days=1)
        name = '%s, %s' % (r['Line'], r['Section'])
        series[name] = ser
        at_flash += [ser[d] for s, d in fog_days[n] if s0 <= s <= s1]
        at_ins += [(n, s, ser[d]) for s, d in ins_days[n] if s0 <= s <= s1]
    level = float(np.percentile(at_flash, 10))
    med = float(np.median(at_flash))
    due = sorted(k for k, ser in series.items() if ser[dt.date(2026, 10, 31)] >= level)
    ratio = {k: ser[dt.date(2026, 10, 31)] / level for k, ser in series.items()}
    low_ins = Counter((n, s) for n, s, v in at_ins if v < 0.6 * med)
    return due, level, keep, ratio, low_ins


IEEE = dict(r25={'477 ACSR Hawk': 0.1196, '795 ACSR Drake': 0.0727, '336.4 ACSR Linnet': 0.1702},
            r75={'477 ACSR Hawk': 0.1430, '795 ACSR Drake': 0.0869, '336.4 ACSR Linnet': 0.2035},
            d={'477 ACSR Hawk': 21.8, '795 ACSR Drake': 28.1, '336.4 ACSR Linnet': 18.3})


def conductor(i, cond, ta, v, q=850.0):
    """an IEEE 738-style steady state: joule heat on the conductor's own resistance and the sun against forced
    convection and radiation, by bisection"""
    d = IEEE['d'][cond] / 1000.0
    a = (IEEE['r75'][cond] / IEEE['r25'][cond] - 1.0) / 50.0
    v = max(0.3, v)
    lo, hi = ta, ta + 150.0
    for _ in range(40):
        tc = (lo + hi) / 2.0
        tf = (tc + ta) / 2.0
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
    return (lo + hi) / 2.0


def main():
    lines, st, taps, tap_km, change = network()
    s22, s25 = study('study22'), study('study25')
    ok('both studies parsed: two terminals on each of the 16 lines', len(s22) == 32 and len(s25) == 32, (len(s22), len(s25)))

    soe, lb, faults = sequences()
    yr = Counter(str(f['t'].tz_convert(CENTRAL).year) for f in faults)
    ok('R1 the faults by year from the two-ended trip sequences', dict(yr) == FIG['faults_by_year'], (dict(yr), FIG['faults_by_year']))

    walk = member_walk(soe, lb, faults, taps)
    tot = [sum(v[0] for v in walk.values()), sum(v[1] for v in walk.values())]
    g = FIG['member_impact_2026']
    ok('R5 the 2026 member interruptions within 2 per cent', abs(tot[0] - g['sustained']) <= 0.02 * g['sustained'], (tot[0], g['sustained']))
    ok('R5 the 2026 member-minutes within 2 per cent', abs(tot[1] - g['member_minutes']) <= 0.02 * g['member_minutes'], (round(tot[1]), g['member_minutes']))
    bad = []
    for name, v in FIG['member_impact_2026_by_line'].items():
        n = int(name.split()[1])
        w = walk.get(n, [0, 0.0])
        if abs(w[0] - v['sustained']) > 0.02 * v['sustained'] + 1 or abs(w[1] - v['member_minutes']) > 0.02 * v['member_minutes'] + 1:
            bad.append((name, w, v))
    ok('R5 every line\'s 2026 figures within 2 per cent', not bad, bad)

    gold_csv = [x for x in os.listdir(os.path.join(TASK, 'golden')) if x.endswith('.csv')][0]
    rows = list(csv.DictReader(open(os.path.join(TASK, 'golden', gold_csv))))
    ok('the golden fault table carries the faults by year', dict(Counter(r['date'][:4] for r in rows)) == FIG['faults_by_year'])
    c26 = Counter(r['cause'] for r in rows if r['date'].startswith('2026'))
    names = {'lightning': 'lightning', 'bird': 'bird or other animal', 'fog': 'salt contamination', 'insulator': 'insulator failure',
             'growin': 'vegetation grown into the line', 'fallin': 'vegetation from outside the right of way',
             'vehicle': 'vehicle or other third party', 'hardware': 'equipment or hardware other than insulators',
             'unknown': 'other or unknown'}
    ok('R2 the golden fault table carries the 2026 causes', {k: c26.get(v, 0) for k, v in names.items()} == FIG['faults_2026_by_cause'])

    # the places: every repeat location's faults re-located from the two ends' residual currents, or on Line 9 past the
    # tap from Shell Ridge's distance corrected with the solar farm's own record
    recs = relay_records()
    ipp = solar_records()
    groups = defaultdict(list)
    for r in rows:
        if r['repeat_location']:
            groups[r['repeat_location']].append(r)
    far = []
    for rl, fs in sorted(groups.items()):
        n = int(fs[0]['line'].split()[1])
        L = lines[n]
        src = s22 if dt.date.fromisoformat(fs[0]['date']) < change else s25
        placed = []
        for r in fs:
            if r['fault_type'] not in ('AG', 'BG', 'CG'):
                continue
            t = dt.datetime.fromisoformat(r['date'] + 'T' + r['time']).replace(tzinfo=CENTRAL).astimezone(dt.timezone.utc)
            src = s22 if t.date() < change else s25
            ra, rb = nearest(recs, L['ca'], n, t), nearest(recs, L['cb'], n, t)
            x = None
            if ra and rb:
                x = split_location(L, src[(n, L['a'])][1], src[(n, L['b'])][1], ra['IG'], rb['IG'])
            elif ra and ra['dist'] is not None and n == 9 and ra['dist'] > tap_km:
                j = ipp.iloc[int(np.argmin([abs((u - t).total_seconds()) for u in ipp['t']]))]
                if abs((j['t'] - t).total_seconds()) <= 2.0:
                    k0 = abs((L['z0'] - L['z1']) / (3 * L['z1']))
                    p = r['fault_type'][0]
                    it = {'A': j['ia_ka'], 'B': j['ib_ka'], 'C': j['ic_ka']}[p] * 1000
                    k = (it + k0 * j['in_ka'] * 1000) / (ra['I'][p] + k0 * ra['IG'])
                    x = tap_km + (ra['dist'] - tap_km) / (1.0 + k)
            elif n != 9 and (ra is None) != (rb is None):
                # one end keeps no record (Ponder Creek's electromechanical relays): the recording end's own distance, fair for
                # the low-resistance arc of a string
                rr_ = ra or rb
                if rr_['dist'] is not None:
                    x = rr_['dist'] if rr_ is ra else L['length'] - rr_['dist']
            if x is not None:
                s = st[st['n'] == n]
                placed.append(int(s.iloc[int(np.argmin(np.abs(s['km_from_terminal_a'].to_numpy() - x)))]['structure_no']))
        mine = int(np.median(placed)) if placed else None
        gold = Counter(int(r['structure']) for r in fs if r['structure']).most_common(1)[0][0]
        if mine is None or abs(mine - gold) > 2:
            far.append((rl, fs[0]['line'], gold, mine, placed))
    ok('R8 every repeat location re-located within 2 structures from the pack', not far, far)
    tapl = [g_ for g_ in groups.values() if g_[0]['line'] == 'Line 9' and g_[0]['cause'] == 'insulator failure']
    tap_no = int([x for x in FIG['work_list'] if x.startswith('replace the string: Line 9')][0].split()[-1])
    ok('X5 the tap line\'s string re-located within 2 of structure %d' % tap_no, len(tapl) == 1 and
       abs(Counter(int(r['structure']) for r in tapl[0]).most_common(1)[0][0] - tap_no) <= 2)

    due, level, keep, ratio, low_ins = deposit_list(lines, st, rows)
    gw = sorted(x.replace('wash: ', '') for x in FIG['wash_due'])
    ok('R6 the washing list from an independent wind-driven deposit model', due == gw, (sorted(set(due) ^ set(gw))))
    ok('R6 Line 2 sections 1 and 6 due again, 1.12 times the level or more', min(ratio['Line 2, Section 1'], ratio['Line 2, Section 6']) >= 1.12,
       (round(ratio['Line 2, Section 1'], 2), round(ratio['Line 2, Section 6'], 2)))
    ok('R7 the flashover level within 15 per cent of the golden\'s', abs(level - FIG['flashover_level']) <= 0.15 * FIG['flashover_level'],
       (round(level, 4), FIG['flashover_level']))
    ok('R7 a soaking rain\'s keep within 0.08 of the golden\'s', abs(keep - FIG['soaking_rain_keep']) <= 0.08, (round(keep, 2), FIG['soaking_rain_keep']))
    gs = FIG['gulf_string']
    gn = int(gs['line'].split()[1])
    here = sum(v for (n, s_), v in low_ins.items() if n == gn and abs(s_ - gs['structure']) <= 1)
    elsewhere = [(n, s_, v) for (n, s_), v in low_ins.items() if not (n == gn and abs(s_ - gs['structure']) <= 1) and v >= 2
                 and n in (1, 2, 3, 4)]
    ok('R4 the Gulf string flashed over below 0.6 of the median salt deposit three times or more, and no other place twice',
       here >= 3 and not elsewhere, (here, elsewhere))

    # the summer contacts: each place's conductor temperature at its contacts since its last trim, from the loading and
    # the nearest station's weather (the nearer airport away from the stations)
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
    town = {'APT': spos['PORT ALCORN SUB'], 'INA': (float(st[st['n'] == 10].sort_values('km_from_terminal_a').iloc[0]['latitude']),
                                                   float(st[st['n'] == 10].sort_values('km_from_terminal_a').iloc[0]['longitude']))}
    veg = pd.read_csv(path('veg'))
    slopes = {}
    for rl, fs in sorted(groups.items()):
        if fs[0]['cause'] not in ('vegetation grown into the line', 'equipment or hardware other than insulators'):
            continue
        n = int(fs[0]['line'].split()[1])
        L = lines[n]
        nos = [int(r['structure']) for r in fs if r['structure']]
        lo, hi = min(nos) - 1, max(nos) + 1
        last = max(dt.date.fromisoformat(r['date']) for r in fs)
        vv = veg[(veg['line'] == 'Line %d' % n) & veg['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])]
        trims = [dt.date.fromisoformat(str(x.completed)[:10]) for x in vv.itertuples()
                 if int(x.from_structure) <= hi and lo <= int(x.to_structure) and dt.date.fromisoformat(str(x.completed)[:10]) <= last]
        tt = max(trims) if trims else None
        xs, ys = [], []
        for r in fs:
            dd = dt.date.fromisoformat(r['date'])
            if tt is not None and dd <= tt:
                continue
            t = dt.datetime.fromisoformat(r['date'] + 'T' + r['time']).replace(tzinfo=CENTRAL)
            h = t.astimezone(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
            col = [c for c in load.columns if c.endswith('_L%d_AMPS' % n)]
            if not col or h not in load.index:
                continue
            amps = float(load.loc[h, col[0]])
            sub = st[(st['n'] == n) & (st['structure_no'] == int(r['structure']))]
            p = (float(sub.iloc[0]['latitude']), float(sub.iloc[0]['longitude']))
            near_s = sorted(spos, key=lambda k: kmf(spos[k], p))[:2]
            wx = None
            for k in near_s:
                if kmf(spos[k], p) <= 18.0 and (k, t.strftime('%Y-%m-%d %H:00')) in swi:
                    wx = swi[(k, t.strftime('%Y-%m-%d %H:00'))]
                    break
            if wx is None:
                ap_ = inad if kmf(town['INA'], p) < kmf(town['APT'], p) else apd
                wx = ap_.get(h)
            if wx is None:
                continue
            xs.append(dd.year + dd.timetuple().tm_yday / 365.25)
            ys.append(conductor(amps, L['conductor'], float(wx[0]), float(wx[1])))
        if len(xs) >= 4 and len(set(int(x) for x in xs)) >= 3:
            slopes[(fs[0]['line'], lo + 1, fs[0]['cause'])] = float(np.polyfit(xs, ys, 1)[0])
    hw = {k: v for k, v in slopes.items() if k[2].startswith('equipment')}
    vg = {k: v for k, v in slopes.items() if k[2].startswith('vegetation')}
    ok('R5 the clearance contact\'s temperature flat since its trim, every grow-in falling (each by its own heat balance)',
       len(hw) == 1 and all(v >= -0.8 for v in hw.values()) and vg and all(v <= -1.2 for v in vg.values()),
       ({k: round(v, 2) for k, v in hw.items()}, {k: round(v, 2) for k, v in vg.items()}))

    print('%d passed, %d failed' % (N['pass'], N['fail']))
    return 1 if N['fail'] else 0


if __name__ == '__main__':
    sys.exit(main())
