"""The golden route, from target/ alone. One fault per two-ended trip sequence in the SCADA sequence of events; each
relay's records matched to it on the relay's own clock, set against SCADA; each fault located by the split of its
residual current between the line's two terminals solved against the protection study in force on its date (on the
solar tap line, Shell Ridge's distance with the farm's ground infeed taken out); each fault's cause from the lightning
record on the true time, the weather at the line (the cooperative's own substation stations once they exist), the
roost survey's structures, the conductor's temperature from the hourly loading and the weather, the gusts and the
patrols; the repeat locations and what has already been fixed; the 2026 member impact from SCADA; and each washing
section's salt deposit on 31 October carried from its last wash or soaking rain at its own rate, against the deposit
at which the porcelain has flashed over in fog.

Every judgment is a switch (OPTS) so the effort passes can run the hurried choice in place of the golden one."""
import cmath
import csv
import datetime as dt
import json
import math
import os
import re
import sqlite3
from collections import defaultdict

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy.optimize import brentq
from scipy.spatial import cKDTree

import common as C

MI = 1.609344
GOLD = dict(loc='ratio', study_by_date=True, tap_infeed=True, fog='stations', survey=True, growin='thermal',
            deposit='stock',
            # the golden family's knobs: each at the golden's setting
            fog_dep=0.5, storm_n=3, storm_km=8.0, tc_min=40.0, gust_min=9.5, level='min', keep=None, rate='loglin',
            src_scale=1.0, win_km=0.4)


def _wb(path, sheet, header_row=None):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    if header_row is None:
        header_row = next(i for i, r in enumerate(rows) if r and sum(1 for v in r if v not in (None, '')) >= 3)
    head = [str(h) for h in rows[header_row]]
    data = [r[:len(head)] for r in rows[header_row + 1:] if any(v not in (None, '') for v in r)]
    return pd.DataFrame(data, columns=head)


def _local_to_utc(s):
    """a Central prevailing wall-clock string to aware UTC (the repeated autumn hour read as the first)"""
    t = dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f' if '.' in s else ('%Y-%m-%d %H:%M' if len(s) == 16 else '%Y-%m-%d %H:%M:%S'))
    return t.replace(tzinfo=C.TZ).astimezone(C.UTC)


# ------------------------------------------------------------------------------------------------ loading

def load(target):
    p = lambda k: os.path.join(target, C.FILES[k])
    d = {}
    lines = _wb(p('lines'), 'Lines')
    d['lines'] = {}
    for _, r in lines.iterrows():
        lid = 'L%02d' % int(str(r['Line']).split()[1])
        d['lines'][lid] = dict(id=lid, a_name=r['Terminal A'], b_name=r['Terminal B'], length=float(r['Length (km)']),
                               conductor=r['Conductor'], z1=complex(float(r['R1 (ohm/km)']), float(r['X1 (ohm/km)'])),
                               z0=complex(float(r['R0 (ohm/km)']), float(r['X0 (ohm/km)'])), insulators=r['Insulators'])
    st = _wb(p('subs'), 'Stations')
    name_to_code = {r['Station']: r['Code'] for _, r in st.iterrows()}
    d['stations'] = {r['Code']: dict(name=r['Station'], relay=r['Relays on the 69 kV line terminals']) for _, r in st.iterrows()}
    for L in d['lines'].values():
        L['a'], L['b'] = name_to_code[L['a_name']], name_to_code[L['b_name']]
    taps = _wb(p('lines'), 'Taps')
    d['taps'] = []
    for _, r in taps.iterrows():
        d['taps'].append(dict(name=r['Tap substation'], line='L%02d' % int(str(r['Line']).split()[1]),
                              km=float(r['Distance from terminal A (km)']), members=int(r['Members (Oct 2026)']),
                              backup={'automatic throw-over': 'auto', 'by control room (SCADA)': 'manual'}.get(r['Transfer to second source'] or '', 'none'),
                              alt=r['Second 69 kV source']))
    solar = _wb(p('lines'), 'Solar tap', header_row=0)
    sv = dict(zip(solar['Item'], solar['Value']))
    d['tap_km'] = float(sv['Tap point, distance from Shell Ridge (km)'])
    d['tap_len'] = float(sv['Tap line to the solar farm substation (km)'])
    xf = _wb(p('subs'), 'Transformers')
    d['transformers'] = xf
    s = pd.read_csv(p('structures'))
    s['lid'] = s['structure_id'].str.slice(0, 3)
    d['structures'] = s
    d['settings'] = _wb(p('settings'), 'Line relays')
    d['studies'] = {}
    for key, yr in (('study22', 2022), ('study25', 2025)):
        d['studies'][yr] = study_table(p(key))
    d['study_dates'] = {2022: dt.datetime(2022, 1, 1, tzinfo=C.UTC), 2025: auto_in_service(xf)}
    d['er'] = pd.read_csv(p('er'), dtype={'Location': str})
    d['gv'] = pd.DataFrame(json.load(open(p('gv')))['records'])
    d['soe'] = pd.read_csv(p('soe'))
    d['ipp'] = pd.read_csv(p('ipp'))
    d['members'] = pd.read_csv(p('members'))
    con = sqlite3.connect(p('oms'))
    d['feeders'] = pd.read_sql('select * from feeder', con)
    con.close()
    d['strokes'] = pd.read_csv(p('strokes'))
    d['apt'] = pd.read_csv(p('apt'), na_values=['M'])
    d['ina'] = pd.read_csv(p('inl_apt'), na_values=['M'])
    d['stations_wx'] = pd.read_csv(p('stations'))
    d['loading'] = pd.read_csv(p('loading'))
    d['avian'] = _wb(p('avian'), 'Counts')
    d['esdd'] = _wb(p('esdd'), 'Readings')
    d['esdd_sites'] = _wb(p('esdd'), 'Sites')
    d['washing'] = _wb(p('washing'), 'Log')
    d['wash_sections'] = _wb(p('washing'), 'Sections')
    d['patrols'] = _wb(p('patrols'), 'Patrols')
    d['rebuilt'] = {}
    for _, r in lines.iterrows():
        v = r['Rebuilt, structures renumbered']
        if v is not None and not (isinstance(v, float) and math.isnan(v)) and str(v).strip():
            d['rebuilt']['L%02d' % int(str(r['Line']).split()[1])] = pd.Timestamp(v).date()
    d['maint'] = pd.read_csv(p('maint'))
    d['veg'] = pd.read_csv(p('veg'))
    return d


def auto_in_service(xf):
    r = xf[(xf['Location'] == 'Inland') & (xf['Unit'].str.startswith('T2'))].iloc[0]
    return dt.datetime.strptime(str(r['In service'])[:10], '%Y-%m-%d').replace(tzinfo=C.UTC)


def study_table(path):
    """the line-out source table from a protection study's text"""
    import subprocess
    txt = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout
    out = {}
    for m in re.finditer(r'Line\s+(\d+)\s+([A-Za-z ]+?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', txt):
        lid = 'L%02d' % int(m.group(1))
        out[(lid, m.group(2).strip())] = (cmath.rect(float(m.group(3)), math.radians(float(m.group(4)))),
                                           cmath.rect(float(m.group(5)), math.radians(float(m.group(6)))))
    gsu = re.search(r'zero-sequence impedance seen from the 69 kV tap point ([\d.]+) ohm at ([\d.]+)', txt.replace('\n', ' '))
    if gsu:
        out['GSU0'] = cmath.rect(float(gsu.group(1)), math.radians(float(gsu.group(2))))
    return out


# ------------------------------------------------------------------------------------------------ relay records and faults

def relay_records(d):
    lines = d['lines']
    ends = {}
    for lid, L in lines.items():
        ends[(L['a'], lid)] = 'a'
        ends[(L['b'], lid)] = 'b'
    recs = []
    for _, r in d['er'].iterrows():
        lid = 'L%02d' % int(r['Relay'].split('-L')[1])
        t = dt.datetime.strptime('%s %s' % (r['Date'], r['Time']), '%m/%d/%Y %H:%M:%S.%f').replace(tzinfo=C.UTC)
        loc = str(r['Location'])
        dist = float(loc) * MI if re.match(r'^-?[\d.]+$', loc or '') else None
        trip = 'TRIP' in str(r['Targets'])
        recs.append(dict(station=r['Station'], line=lid, end=ends[(r['Station'], lid)], t=t, type=r['Type'], trip=trip,
                         shot=int(r['Shot']), dist=dist, I={'A': float(r['IA']), 'B': float(r['IB']), 'C': float(r['IC'])},
                         IG=float(r['IG']), fam='ER'))
    for _, r in d['gv'].iterrows():
        st, ln = r['device'].split('_')[0], r['device'].split('_')[1]
        lid = 'L%02d' % int(ln[1:])
        t = _local_to_utc(r['time_local'])
        recs.append(dict(station=st, line=lid, end=ends[(st, lid)], t=t, type=r['fault_type'], trip=bool(r['trip']),
                         shot=int(r['reclose_shot']), dist=(None if pd.isna(r['distance_km']) else float(r['distance_km'])),
                         I={'A': r['ia_ka'] * 1000, 'B': r['ib_ka'] * 1000, 'C': r['ic_ka'] * 1000}, IG=r['in_ka'] * 1000,
                         fam='GV'))
    return recs


def soe_trips(d):
    s = d['soe']
    s = s[s['point'].str.contains('69KV BKR')]
    out = []
    for _, r in s.iterrows():
        st = r['rtu']
        b = r['point'].split()[-1]
        lid = 'L%02d' % int(b[-2:])
        end = 'a' if b[1:3] == '52' else 'b'
        t = dt.datetime.strptime(r['time_utc'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=C.UTC)
        out.append(dict(t=t, station=st, line=lid, end=end, state=r['state'], cause=r['cause']))
    return out


def build_faults(d):
    """one fault per sequence of protection trips that takes out both terminals of a line within a second; a single-ended
    protection trip with no fault record is a relay test"""
    trips = [x for x in soe_trips(d) if x['state'] == 'OPEN' and x['cause'] == 'PROT']
    trips.sort(key=lambda x: (x['line'], x['t']))
    faults = []
    by_line = defaultdict(list)
    for x in trips:
        by_line[x['line']].append(x)
    for lid, xs in by_line.items():
        i = 0
        while i < len(xs):
            t0 = xs[i]['t']
            grp = [x for x in xs if 0 <= (x['t'] - t0).total_seconds() <= 60.0]
            ends0 = set(x['end'] for x in grp if (x['t'] - t0).total_seconds() < 1.0)
            if len(ends0) == 2:
                faults.append(dict(line=lid, t=t0, soe=grp))
            i += len(grp)
    faults.sort(key=lambda f: f['t'])
    # relay records matched on each relay's own clock: offsets estimated from the trips both saw
    recs = [r for r in relay_records(d) if r['trip']]
    by_relay = defaultdict(list)
    for r in recs:
        by_relay[(r['station'], r['line'])].append(r)
    for key in by_relay:
        by_relay[key].sort(key=lambda r: r['t'])
    for f in faults:
        f['rec'] = {}
    for (st, lid), rs in by_relay.items():
        fl = [f for f in faults if f['line'] == lid]
        if not fl:
            continue
        ft = np.array([f['t'].timestamp() for f in fl])
        firsts = [r for r in rs if r['shot'] == 0]
        # first pass: nearest fault within 10 minutes; the offsets' running median sets the clock
        pairs = []
        for r in firsts:
            j = int(np.argmin(np.abs(ft - r['t'].timestamp())))
            dtt = r['t'].timestamp() - ft[j]
            if abs(dtt) < 600:
                pairs.append((r['t'].timestamp(), dtt))
        if not pairs:
            continue
        pairs.sort()
        tt = np.array([p[0] for p in pairs])
        off = np.array([p[1] for p in pairs])
        for r in firsts:
            k = np.argsort(np.abs(tt - r['t'].timestamp()))[:5]
            o = float(np.median(off[k]))
            j = int(np.argmin(np.abs(ft - (r['t'].timestamp() - o))))
            if abs(r['t'].timestamp() - o - ft[j]) < 1.0:
                fl[j]['rec'][r['end']] = dict(r, offset=o)
    return faults


def ipp_records(d):
    s = d['ipp']
    s = s[s['description'].str.contains('GND FAULT')]
    out = []
    for _, r in s.iterrows():
        t = dt.datetime.strptime(r['timestamp'], '%m/%d/%Y %H:%M:%S.%f').replace(tzinfo=C.CST).astimezone(C.UTC)
        out.append(dict(t=t, I={'A': r['ia_ka'] * 1000, 'B': r['ib_ka'] * 1000, 'C': r['ic_ka'] * 1000}, IG=r['in_ka'] * 1000))
    return out


# ------------------------------------------------------------------------------------------------ location

def _sources(d, lid, t, by_date):
    L = d['lines'][lid]
    yr = 2025
    if by_date and t < d['study_dates'][2025]:
        yr = 2022
    tab = d['studies'][yr]
    return tab[(lid, d['stations'][L['a']]['name'])], tab[(lid, d['stations'][L['b']]['name'])], tab


def ratio_location(d, lid, iga, igb, t, by_date=True):
    L = d['lines'][lid]
    (z1a, z0a), (z1b, z0b), _ = _sources(d, lid, t, by_date)
    z0a, z0b = z0a * d.get('src_scale', 1.0), z0b * d.get('src_scale', 1.0)
    z0 = L['z0']
    Lk = L['length']
    f = lambda x: abs(z0b + (Lk - x) * z0) / abs(z0a + x * z0) - iga / igb
    xs = np.linspace(0.005, Lk - 0.005, 400)
    fs = np.array([f(x) for x in xs])
    for i in range(len(xs) - 1):
        if fs[i] == 0 or fs[i] * fs[i + 1] < 0:
            return float(brentq(f, xs[i], xs[i + 1]))
    return None


def locate(d, faults, opts):
    ipp = ipp_records(d)
    ipp_t = np.array([r['t'].timestamp() for r in ipp]) if ipp else np.array([])
    for f in faults:
        L = d['lines'][f['line']]
        ra, rb = f['rec'].get('a'), f['rec'].get('b')
        f['type'] = (ra or rb or {}).get('type')
        km = None
        slg = f['type'] in ('AG', 'BG', 'CG')
        if opts['loc'] == 'ratio' and ra and rb and slg:
            km = ratio_location(d, f['line'], ra['IG'], rb['IG'], f['t'], opts['study_by_date'])
        if km is None:
            ests = []
            if ra and ra['dist'] is not None:
                ests.append(ra['dist'])
            if rb and rb['dist'] is not None:
                ests.append(L['length'] - rb['dist'])
            if f['line'] == 'L09' and ra and ra['dist'] is not None and ra['dist'] > d['tap_km'] and opts['tap_infeed'] and slg:
                j = int(np.argmin(np.abs(ipp_t - f['t'].timestamp()))) if len(ipp_t) else None
                if j is not None and abs(ipp_t[j] - f['t'].timestamp()) < 2.0:
                    r = ipp[j]
                    p = f['type'][0]
                    k0 = abs((L['z0'] - L['z1']) / (3 * L['z1']))
                    k = (r['I'][p] + k0 * r['IG']) / (ra['I'][p] + k0 * ra['IG'])
                    ests = [d['tap_km'] + (ra['dist'] - d['tap_km']) / (1.0 + k)]
            if ests:
                km = float(np.mean(ests))
        f['km'] = km
        if km is not None:
            s = d['structures'][d['structures']['lid'] == f['line']]
            kms = s['km_from_terminal_a'].to_numpy()
            j = int(np.argmin(np.abs(kms - km)))
            f['structure'] = int(s.iloc[j]['structure_no'])
            k2 = j + 1 if (j + 1 < len(kms) and km > kms[j]) else j - 1
            f['span'] = tuple(sorted((int(s.iloc[j]['structure_no']), int(s.iloc[max(k2, 0)]['structure_no']))))
        else:
            f['structure'] = None
            f['span'] = None
    return faults


# ------------------------------------------------------------------------------------------------ cause

def _xy(lat, lon):
    return (lon - (-97.02)) * 111.32 * math.cos(math.radians(28.18)), (lat - 28.18) * 110.95


def _asos(df):
    df = df.copy()
    df['t'] = pd.to_datetime(df['valid']).dt.tz_localize('UTC')
    df['hour'] = df['t'].dt.floor('h')
    df['tc'] = (df['tmpf'] - 32) * 5 / 9
    df['gust_ms'] = pd.to_numeric(df['gust'], errors='coerce') / 1.94384
    return {r.hour: r for r in df.itertuples()}


def weather_index(d):
    apt = d['apt'].copy()
    apt['t'] = pd.to_datetime(apt['valid']).dt.tz_localize('UTC')
    apt['hour'] = apt['t'].dt.floor('h')
    apt['tc'] = (apt['tmpf'] - 32) * 5 / 9
    apt['dc'] = (apt['dwpf'] - 32) * 5 / 9
    apt['gust_ms'] = pd.to_numeric(apt['gust'], errors='coerce') / 1.94384
    apt['rain_mm'] = pd.to_numeric(apt['p01i'].replace('T', '0.001'), errors='coerce') * 25.4
    aptd = {r.hour: r for r in apt.itertuples()}
    sw = d['stations_wx'].copy()
    sw['t'] = [_local_to_utc(s) for s in sw['hour_local']]
    swd = {(r.station, r.t): r for r in sw.itertuples()}
    return aptd, swd


STATION_XY = {'PORT ALCORN SUB': (76.0, 27.0), 'SHELL RIDGE SUB': (88.0, 43.0), 'SEDGE POINT SUB': (97.0, 60.0),
              'TULE MARSH SUB': (68.0, 31.0), 'CANEY BEND SUB': (60.0, 41.0), 'MESQUITE FLAT SUB': (36.0, 44.0)}


def fault_xy(d, f):
    s = d['structures']
    r = s[(s['lid'] == f['line']) & (s['structure_no'] == f['structure'])]
    if len(r) == 0:
        return None
    return _xy(float(r.iloc[0]['latitude']), float(r.iloc[0]['longitude']))


def roost_structures(d):
    """structures the roost survey's sites stand on: survey points within 60 m of a 69 kV structure"""
    av = d['avian']
    s = d['structures']
    pts = np.array([_xy(la, lo) for la, lo in zip(s['latitude'], s['longitude'])])
    tree = cKDTree(pts)
    out = {}
    for site, g in av.groupby('Site'):
        la, lo = float(g.iloc[0]['Latitude']), float(g.iloc[0]['Longitude'])
        dd, j = tree.query(_xy(la, lo))
        if dd <= 0.06:
            out[site] = (s.iloc[j]['lid'], int(s.iloc[j]['structure_no']), int(pd.to_numeric(g['Count']).mean()))
    return out


def conductor_temp(i, cond, ta, wind, solar):
    import loads as Lmod
    return Lmod.conductor_temp(i, cond, ta, wind, solar)


def line_xy(d):
    s = d['structures']
    out = {}
    for lid, grp in s.groupby('lid'):
        out[lid] = np.array([_xy(la, lo) for la, lo in zip(grp['latitude'], grp['longitude'])])
    return out


def classify(d, faults, opts):
    """each fault's cause, first from its own signature, then for repeat clusters from what their faults share"""
    aptd, swd = weather_index(d)
    inad = _asos(d['ina'])
    st = d['strokes']
    st = st[st['type'] == 'CG']
    st_t = (pd.to_datetime(st['time_utc']).astype('int64') / 1e9).to_numpy()
    sxy = np.array([_xy(a, b) for a, b in zip(st['latitude'], st['longitude'])])
    lxy = line_xy(d)
    roosts = roost_structures(d) if opts['survey'] else {}
    roost_set = {(l, n) for (l, n, c) in roosts.values()}
    load = d['loading'].copy()
    load['t'] = pd.to_datetime(load['hour_utc']).dt.tz_localize('UTC')
    loadd = {r['t']: r for r in load.to_dict('records')}
    gulf = {'L01', 'L02', 'L03', 'L04'}
    s = d['structures']
    ina = d.get('ina')
    for f in faults:
        f['cause'] = 'unknown'
        xy = fault_xy(d, f) if f['structure'] is not None else None
        tt = f['t'].timestamp()
        lt = C.to_local(f['t'])
        hr = f['t'].replace(minute=0, second=0, microsecond=0)
        # a stroke within a second of the trip and within 1 km of the line's route
        k = np.nonzero(np.abs(st_t - tt) <= 1.0)[0]
        route = lxy[f['line']]
        if len(k) and any(np.min(np.hypot(route[:, 0] - sxy[j][0], route[:, 1] - sxy[j][1])) <= 1.0 for j in k):
            f['cause'] = 'lightning'
            f['sig'] = 'stroke'
            continue
        ref = xy if xy is not None else tuple(route[len(route) // 2])
        k2 = np.nonzero(np.abs(st_t - tt) <= 3600.0)[0]
        storm = sum(1 for j in k2 if math.hypot(sxy[j][0] - ref[0], sxy[j][1] - ref[1]) <= opts['storm_km']) >= opts['storm_n']
        a = aptd.get(hr)
        b = inad.get(hr)
        gust = 0.0
        if lt.month in (10, 11, 12, 1, 2, 3, 4):        # fronts: the inland airport's gusts; summer storms show in the strokes
            if b is not None and not pd.isna(b.gust_ms):
                gust = float(b.gust_ms)
        src = None
        if opts['fog'] == 'stations':
            near = sorted(STATION_XY, key=lambda n: math.hypot(STATION_XY[n][0] - ref[0], STATION_XY[n][1] - ref[1]))
            for n in near[:2]:
                r = swd.get((n, hr))
                if r is not None and math.hypot(STATION_XY[n][0] - ref[0], STATION_XY[n][1] - ref[1]) <= 18.0:
                    src = r
                    break
        if src is not None:
            fog = False
            seen = False
            for n in near[:2]:
                if math.hypot(STATION_XY[n][0] - ref[0], STATION_XY[n][1] - ref[1]) > 18.0:
                    continue
                for dh in (-1, 0, 1):
                    r2 = swd.get((n, hr + dt.timedelta(hours=dh)))
                    if r2 is not None:
                        seen = True
                        if (r2.air_temp_c - r2.dewpoint_c) <= opts['fog_dep']:
                            fog = True
            if not seen:
                fog = a is not None and isinstance(a.wxcodes, str) and 'FG' in a.wxcodes
            rain = src.rain_mm >= 0.25
            tair, wind = src.air_temp_c, src.wind_ms
        else:
            fog = a is not None and isinstance(a.wxcodes, str) and ('FG' in a.wxcodes or (opts['fog'] == 'airport' and 'BR' in a.wxcodes))
            rain = a is not None and (a.rain_mm or 0) >= 0.25
            tair = a.tc if a is not None else 25.0
            wind = (a.sknt / 1.94384) if a is not None and not pd.isna(a.sknt) else 2.0
        night = lt.hour >= 21 or lt.hour <= 10
        porcelain = False
        if xy is not None:
            row = s[(s['lid'] == f['line']) & (s['structure_no'] == f['structure'])].iloc[0]
            porcelain = row['insulator'] == 'porcelain'
        near_roost = any(l == f['line'] and abs(n - (f['structure'] or -99)) <= 2 for (l, n) in roost_set)
        summer_pm = lt.month in (5, 6, 7, 8, 9, 10) and 12 <= lt.hour <= 20
        tc = None
        if summer_pm:
            lr = loadd.get(hr)
            L = d['lines'][f['line']]
            col = [c for c in (lr or {}) if c.endswith('_L%d_AMPS' % int(f['line'][1:]))]
            if lr is not None and col:
                tc = conductor_temp(float(lr[col[0]]), L['conductor'], tair, wind, 850.0)
        f['sig'] = dict(storm=storm, gust=gust, fog=fog, rain=rain, night=night, roost=near_roost and lt.month in (11, 12, 1, 2, 3) and lt.hour <= 7,
                        summer_pm=summer_pm, tc=tc, gulf_porcelain=(f['line'] in gulf and porcelain))
        sg = f['sig']
        if opts['growin'] == 'season' and summer_pm:
            f['cause'] = 'growin'
            continue
        if storm or gust >= opts['gust_min']:
            f['cause'] = 'fallin'
            continue
        if sg['roost']:
            f['cause'] = 'bird'
            continue
        if night and fog and sg['gulf_porcelain']:
            f['cause'] = 'fog'
            continue
        if summer_pm and not rain and tc is not None and tc >= opts['tc_min']:
            f['cause'] = 'growin'
            continue
    # patrol findings name what a crew saw
    pat = d['patrols']
    for _, r in pat.iterrows():
        txt = str(r['Findings']).lower()
        lid = 'L%02d' % int(str(r['Line']).split()[1])
        day = pd.Timestamp(r['Date']).date()
        cand = [f for f in faults if f['line'] == lid and 0 <= (day - C.to_local(f['t']).date()).days <= 6]
        if not cand:
            continue
        f = min(cand, key=lambda f: abs((day - C.to_local(f['t']).date()).days))
        for keys, cause in ((('vehicle', 'truck'), 'vehicle'), (('connector', 'clamp'), 'hardware'),
                            (('outside the right of way', 'dead pine'), 'fallin'), (('grown up into', 'reaching the bottom phase'), 'growin'),
                            (('cracked porcelain', 'broken bell'), 'insulator')):
            if any(k_ in txt for k_ in keys):
                f['cause'] = cause
                f['patrol'] = True
    return faults


def settle_clusters(faults, opts):
    """repeat clusters: faults of one line within 400 m that the event signatures did not explain take the cause their
    cluster shares (storms and fronts: trees from outside the right of way; roost-season pre-dawn at a surveyed roost:
    birds; hot afternoons: grow-in; anything else that keeps coming back at one structure: a failing string)"""
    by = defaultdict(list)
    for f in faults:
        if f['structure'] is not None and f['cause'] not in ('lightning', 'fog', 'vehicle', 'hardware'):
            by[f['line']].append(f)
    for lid, fs in by.items():
        fs.sort(key=lambda f: f['km'])
        wins = []
        for i, f in enumerate(fs):
            grp = [g for g in fs[i:] if g['km'] - f['km'] <= opts['win_km']]
            if len(grp) >= 3:
                wins.append(grp)
        merged = []
        for grp in wins:
            if merged and grp[0]['km'] <= merged[-1][-1]['km']:
                ids = {id(x) for x in merged[-1]}
                merged[-1] = merged[-1] + [g for g in grp if id(g) not in ids]
            else:
                merged.append(list(grp))
        for grp in merged:
            sg = [g['sig'] for g in grp if isinstance(g.get('sig'), dict)]
            share = lambda key: sum(1 for x in sg if x.get(key)) / max(1, len(sg))
            if opts['growin'] == 'season':
                causes = [g['cause'] for g in grp]
                top = max(set(causes), key=causes.count)
                cause = top if top != 'unknown' else 'insulator'
            elif sum(1 for x in sg if x.get('storm') or x.get('gust', 0) >= opts['gust_min'] - 0.5) / max(1, len(sg)) >= 0.5:
                cause = 'fallin'
            elif share('roost') >= 0.5:
                cause = 'bird'
            elif sum(1 for x in sg if x.get('summer_pm') and not x.get('storm')) / max(1, len(sg)) >= 0.75:
                cause = 'growin'
            else:
                cause = 'insulator'
            for g in grp:
                if not g.get('patrol'):
                    g['cause'] = cause
    return faults


def settle_insulators(faults):
    """a structure where faults keep coming in light rain at any hour is a failing string; isolated rain faults stay
    unknown"""
    by = defaultdict(list)
    for f in faults:
        if f['cause'] in ('insulator?', 'insulator') and f['structure'] is not None:
            by[f['line']].append(f)
    for lid, fs in by.items():
        for f in fs:
            near = [g for g in fs if abs((g['km'] or 0) - (f['km'] or 0)) <= 0.4]
            f['cause'] = 'insulator' if len(near) >= 3 else 'unknown'
    for f in faults:
        if f['cause'] == 'insulator?':
            f['cause'] = 'unknown'
    return faults


# ------------------------------------------------------------------------------------------------ repeat locations

def repeat_locations(d, faults, win_km=0.4):
    """three or more faults of one cause within 400 m on one line since January 2022 (salt contamination excepted):
    every 400 m window holding three, windows that overlap read as one place"""
    out = []
    for cause in ('bird', 'insulator', 'growin', 'fallin'):
        by = defaultdict(list)
        for f in faults:
            if f['cause'] == cause and f['km'] is not None:
                by[f['line']].append(f)
        for lid, fs in by.items():
            fs.sort(key=lambda f: f['km'])
            wins = []
            for i, f in enumerate(fs):
                grp = [g for g in fs[i:] if g['km'] - f['km'] <= win_km]
                if len(grp) >= 3:
                    wins.append(grp)
            merged = []
            for grp in wins:
                if merged and grp[0]['km'] <= merged[-1][-1]['km']:
                    ids = {id(x) for x in merged[-1]}
                    merged[-1] = merged[-1] + [g for g in grp if id(g) not in ids]
                else:
                    merged.append(list(grp))
            for grp in merged:
                nos = sorted(g['structure'] for g in grp)
                spans = [g['span'] for g in grp if g['span']]
                span = max(set(spans), key=spans.count) if spans else None
                out.append(dict(line=lid, cause=cause, n=len(grp), first=min(g['t'] for g in grp), last=max(g['t'] for g in grp),
                                structure=int(np.median(nos)), s_min=nos[0], s_max=nos[-1], span=span,
                                km=float(np.median([g['km'] for g in grp])), faults=grp))
    return out


def plate_to_current(d, lid, no, day):
    """a work order's structure number in today's numbering (rebuilt lines' orders before the rebuild carry the former
    plate numbers, which the inventory maps)"""
    s = d['structures']
    s = s[(s['lid'] == lid) & s['former_no'].notna()]
    if len(s) == 0:
        return no
    rebuilt = d.get('rebuilt', {}).get(lid)
    if rebuilt is not None and day >= rebuilt:
        return no
    r = s[s['former_no'].astype(float).astype(int) == int(no)]
    return int(r.iloc[0]['structure_no']) if len(r) else no


def fixed_since(d, rl):
    """the fix for a repeat location's cause completed on or after the day of its last fault"""
    last = C.to_local(rl['last']).date()
    lname = 'Line %d' % int(rl['line'][1:])
    lo, hi = rl['s_min'] - 1, rl['s_max'] + 1
    if rl['cause'] in ('bird', 'insulator'):
        typ = 'AVIAN' if rl['cause'] == 'bird' else 'INSULATOR'
        m = d['maint']
        m = m[(m['line'] == lname) & (m['work_type'] == typ)]
        for _, r in m.iterrows():
            day = pd.Timestamp(r['completed']).date()
            no = plate_to_current(d, rl['line'], int(r['structure']), pd.Timestamp(r['opened']).date())
            if lo <= no <= hi and day >= last:
                return True
        return False
    v = d['veg']
    v = v[v['line'] == lname]
    kinds = ['HOT SPOT', 'CYCLE TRIM'] if rl['cause'] == 'growin' else ['HAZARD TREE']
    for _, r in v[v['work_type'].isin(kinds)].iterrows():
        day = pd.Timestamp(r['completed']).date()
        a = plate_to_current(d, rl['line'], int(r['from_structure']), day)
        b = plate_to_current(d, rl['line'], int(r['to_structure']), day)
        if a <= hi and lo <= b and day >= last:
            return True
    return False


# ------------------------------------------------------------------------------------------------ the 2026 member impact

def member_impact(d, faults, year=2026, per_fault=False):
    soe = d['soe']
    soe = soe.assign(t=pd.to_datetime(soe['time_utc']).dt.tz_localize('UTC'))
    mem = d['members']
    taps = defaultdict(list)
    for tp in d['taps']:
        taps[tp['line']].append(tp)
    code_of = {}
    for _, r in d['feeders'].iterrows():
        code_of[r['substation']] = r['sub_code']
    res = defaultdict(lambda: dict(sustained=0, minutes=0.0, momentary=0))
    for f in faults:
        if year is not None and C.to_local(f['t']).year != year:
            continue
        f['impact'] = dict(sustained=0, minutes=0.0, momentary=0)
        L = d['lines'][f['line']]
        t0 = f['t']
        win = soe[(soe['t'] >= t0 - pd.Timedelta(seconds=1)) & (soe['t'] <= t0 + pd.Timedelta(days=3))]
        bpts = ['%s 69KV BKR B%d%02d' % (L['a'], 52, int(f['line'][1:])), '%s 69KV BKR B%d%02d' % (L['b'], 62, int(f['line'][1:]))]
        lb = win[win['point'].isin(bpts)]
        lock = lb[(lb['state'] == 'LOCKOUT') & (lb['t'] <= t0 + pd.Timedelta(seconds=60))]
        month = '%d-%02d' % (C.to_local(t0).year, C.to_local(t0).month)
        for tp in taps.get(f['line'], []):
            m = int(mem[(mem['month'] == month) & (mem['substation'] == tp['name'])]['members'].sum())
            if len(lock) == 0:
                closes = lb[(lb['state'] == 'CLOSE') & (lb['cause'] == '79 RECL')]
                last_close = closes[closes['t'] <= t0 + pd.Timedelta(seconds=60)]['t'].max()
                secs = (last_close - t0).total_seconds() if pd.notna(last_close) else 1.0
            else:
                code = code_of.get(tp['name'])
                alt = win[(win['point'].str.startswith('%s 69KV ALT SRC' % code)) & (win['state'] == 'CLOSE')]
                line_close = lb[(lb['state'] == 'CLOSE') & (lb['t'] > t0 + pd.Timedelta(seconds=60))]['t'].min()
                cand = [x for x in [alt['t'].min() if len(alt) else pd.NaT, line_close] if pd.notna(x)]
                secs = (min(cand) - t0).total_seconds() if cand else 0.0
            if secs > 300:
                res[f['line']]['sustained'] += m
                res[f['line']]['minutes'] += m * secs / 60.0
                f['impact']['sustained'] += m
                f['impact']['minutes'] += m * secs / 60.0
            else:
                res[f['line']]['momentary'] += m
                f['impact']['momentary'] += m
    return dict(res)


# ------------------------------------------------------------------------------------------------ salt deposits

def daily_rain_series(d):
    """mm per local day at each substation station, the Port Alcorn airport standing in before the stations"""
    sw = d['stations_wx'].copy()
    sw['day'] = pd.to_datetime(sw['hour_local']).dt.date
    st = sw.groupby(['station', 'day'])['rain_mm'].sum()
    apt = d['apt'].copy()
    apt['t'] = pd.to_datetime(apt['valid']).dt.tz_localize('UTC').dt.tz_convert(C.ZONE)
    apt['day'] = apt['t'].dt.date
    apt['mm'] = pd.to_numeric(apt['p01i'].replace('T', '0'), errors='coerce').fillna(0) * 25.4
    ap = apt.groupby('day')['mm'].sum()
    return st, ap


def deposit_model(d, faults, opts):
    """each washing section's deposit on 31 October 2026 against the flashover level"""
    s = d['structures']
    secs = d['wash_sections']
    ws = d['washing']
    st_rain, ap_rain = daily_rain_series(d)
    sites = d['esdd_sites']
    rd = d['esdd'].copy()
    rd['date'] = pd.to_datetime(rd['Date sampled']).dt.date
    near_station = {'L01': ['PORT ALCORN SUB'], 'L02': ['PORT ALCORN SUB', 'SHELL RIDGE SUB'],
                    'L03': ['SHELL RIDGE SUB', 'SEDGE POINT SUB'], 'L04': ['PORT ALCORN SUB']}
    site_station = {}
    for _, r in sites.iterrows():
        x, y = _xy(float(r['Latitude']), float(r['Longitude']))
        site_station[r['Site']] = min(STATION_XY, key=lambda n: math.hypot(STATION_XY[n][0] - x, STATION_XY[n][1] - y))

    def rain(stations, day):
        vals = [st_rain.get((n, day)) for n in stations]
        vals = [v for v in vals if v is not None and not pd.isna(v)]
        return float(np.mean(vals)) if vals else float(ap_rain.get(day, 0.0))

    # accumulation between readings with no rain of 5 mm or more in between, by site
    rates = {}
    for site, g in rd.groupby('Site'):
        g = g.sort_values('date')
        sl = []
        for (_, a), (_, b) in zip(g.iterrows(), g.iloc[1:].iterrows()):
            days = (b['date'] - a['date']).days
            wet = any(rain([site_station[site]], a['date'] + dt.timedelta(days=k)) >= 5.0 for k in range(1, days + 1))
            if not wet and days >= 10 and b['ESDD (mg/cm2)'] > a['ESDD (mg/cm2)']:
                sl.append((b['ESDD (mg/cm2)'] - a['ESDD (mg/cm2)']) / days)
        if sl:
            rates[site] = float(np.median(sl))
    shore = dict(zip(sites['Site'], sites['Gulf shore (km)']))
    xs = np.array([float(shore[k]) for k in rates])
    ys = np.array([rates[k] for k in rates])
    # rate falls off exponentially with distance from the Gulf: log-linear fit
    A = np.vstack([np.ones_like(xs), xs]).T
    coef, *_ = np.linalg.lstsq(A, np.log(np.maximum(ys, 1e-6)), rcond=None)
    if opts.get('rate') == 'nearest':
        sd = sorted((float(shore[k]), rates[k]) for k in rates)
        rate_at = lambda dist: min(sd, key=lambda p: abs(p[0] - dist))[1]
    elif opts.get('rate') == 'linear':
        cl = np.polyfit(xs, ys, 1)
        rate_at = lambda dist: max(1e-5, float(np.polyval(cl, dist)))
    else:
        rate_at = lambda dist: float(math.exp(coef[0] + coef[1] * dist))
    if opts.get('rate_scale'):
        _ra = rate_at
        rate_at = lambda dist: _ra(dist) * opts['rate_scale']
    # what a soaking rain leaves: readings either side of one soaking day and no other wet day
    keeps = []
    for site, g in rd.groupby('Site'):
        g = g.sort_values('date')
        for (_, a), (_, b) in zip(g.iterrows(), g.iloc[1:].iterrows()):
            days = (b['date'] - a['date']).days
            r = [rain([site_station[site]], a['date'] + dt.timedelta(days=k)) for k in range(1, days + 1)]
            if sum(1 for x in r if x >= 12.0) == 1 and sum(1 for x in r if 5.0 <= x < 12.0) == 0:
                acc = rates.get(site, 0.0) * days
                keeps.append(max(0.0, (b['ESDD (mg/cm2)'] - acc)) / a['ESDD (mg/cm2)'])
    keep = float(np.median(keeps)) if keeps else 0.5
    if opts.get('keep') is not None:
        keep = opts['keep']
    keep_mod = 0.85
    out = {}
    day0, day_end = dt.date(2022, 1, 1), dt.date(2026, 10, 31)
    sec_dep = {}
    for _, r in secs.iterrows():
        lid = 'L%02d' % int(str(r['Line']).split()[1])
        sid = '%s-W%s' % (lid, str(r['Section']).split()[-1])
        sub = s[(s['lid'] == lid) & (s['structure_no'] >= int(r['From structure'])) & (s['structure_no'] <= int(r['To structure']))]
        dist = float(sub['gulf_shore_km'].mean())
        rate = rate_at(dist)
        washes = set(pd.to_datetime(ws[(ws['Line'] == r['Line']) & (ws['Section'] == r['Section'])]['Date']).dt.date)
        dep = rate * 60.0
        series = {}
        day = day0
        while day <= day_end:
            dep += rate
            rr = rain(near_station[lid], day)
            if rr >= 12.0:
                dep *= keep
            elif rr >= 5.0:
                dep *= keep_mod
            if day in washes:
                dep = 0.003
            series[day] = dep
            day += dt.timedelta(days=1)
        sec_dep[sid] = dict(line=lid, s0=int(r['From structure']), s1=int(r['To structure']), dist=dist, series=series)
    # the deposit at each fog flashover, and the level
    at_flash = []
    for f in faults:
        if f['cause'] != 'fog' or f['structure'] is None:
            continue
        for sid, sd in sec_dep.items():
            if sd['line'] == f['line'] and sd['s0'] <= f['structure'] <= sd['s1']:
                at_flash.append(sd['series'][C.to_local(f['t']).date()])
    if not at_flash:
        level = None
    elif opts.get('level') == 'p5':
        level = float(np.percentile(at_flash, 5))
    elif opts.get('level') == 'p10':
        level = float(np.percentile(at_flash, 10))
    else:
        level = float(np.min(at_flash))
    if level is not None and opts.get('level_scale'):
        level *= opts['level_scale']
    flashed = defaultdict(int)
    for f in faults:
        if f['cause'] != 'fog' or f['structure'] is None:
            continue
        for sid, sd in sec_dep.items():
            if sd['line'] == f['line'] and sd['s0'] <= f['structure'] <= sd['s1']:
                flashed[sid] += 1
    # the latest test reading at the site nearest each section (the hurried state of the deposit)
    latest = {}
    for site, g_ in rd.groupby('Site'):
        g_ = g_.sort_values('date')
        latest[site] = float(g_.iloc[-1]['ESDD (mg/cm2)'])
    site_xy = {r['Site']: _xy(float(r['Latitude']), float(r['Longitude'])) for _, r in sites.iterrows()}
    for sid, sd in sec_dep.items():
        sub = s[(s['lid'] == sd['line']) & (s['structure_no'] >= sd['s0']) & (s['structure_no'] <= sd['s1'])]
        cx, cy = _xy(float(sub['latitude'].mean()), float(sub['longitude'].mean()))
        near_site = min(site_xy, key=lambda k: math.hypot(site_xy[k][0] - cx, site_xy[k][1] - cy))
        if opts['deposit'] == 'stock':
            due = level is not None and sd['series'][day_end] >= level
        elif opts['deposit'] == 'history':
            due = flashed[sid] > 0
        else:
            due = level is not None and latest[near_site] >= level
        out[sid] = dict(deposit=sd['series'][day_end], dist=sd['dist'], due=due, flashed=flashed[sid], test_site=near_site,
                        test_latest=latest[near_site])
    return dict(sections=out, level=level, rates=rates, coef=coef.tolist(), keep=keep, at_flash=at_flash)


def run(target, opts=None):
    opts = dict(GOLD, **(opts or {}))
    d = load(target)
    d['src_scale'] = opts.get('src_scale', 1.0)
    faults = build_faults(d)
    locate(d, faults, opts)
    classify(d, faults, opts)
    settle_clusters(faults, opts)
    rls = repeat_locations(d, faults, opts['win_km'])
    for rl in rls:
        rl['fixed'] = fixed_since(d, rl)
    impact = member_impact(d, faults)
    dep = deposit_model(d, faults, opts)
    return dict(d=d, faults=faults, repeat=rls, impact=impact, deposits=dep)
