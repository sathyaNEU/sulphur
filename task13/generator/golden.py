"""The golden route for task13 (architecture 7, Level 5), from target/ alone.

Every physical and operational judgment is a switch in GOLD/opts so core.py and passes.py can evaluate the golden
family, every stump dropped alone, every stump fixed alone on the reflex route, over-corrected sides, one-fact
shortcuts, and all four frontier run routes directly on the shipped files:

  S1 (contacts):   IEEE 738 thermal sag trajectory post-trim separating 12.47 kV underbuild clearance spans
                   (L06 57-58, L15 48-49; hardware, 3 crew-days) from growing trees (including underbuilt decoys
                   L14 62-63 and L12 44-45; growin, 2 crew-days).
  S2 (tap_infeed): Dual YNd1 IPP lateral tap ground-infeed inversion on Line 9 (Coyote Draw Solar) and Line 8
                   (Brushy Creek BESS) using each facility's CST protection export.
  S3 (dc_mutual):  Coupled 2-line zero-sequence network inversion with Z0m on the 14.5 km double-circuit corridor
                   shared by Lines 10 and 11 out of Inland (parameters parsed directly from the protection studies).
  S4 (deposit):    Joint (ESDD, NSDD) two-state daily contamination model (sea salt on onshore winds with fast rain
                   washout + caliche/agricultural dust on dry inland winds with slow rain washout) and empirical 2D
                   fog-flashover frontier fitted by logistic regression over fog nights.
  S5 (topology):   Chronological SCADA as-operated switching topology state machine replaying planned supervisory
                   alternate-source tap transfers (ALT SRC / NORM SW) for exact 2022-2026 and 2026 member-minutes
                   and RP-04 Rev 5 Priority 1 36-crew-day programme allocation.
"""
import cmath
import datetime as dt
import json
import math
import os
import re
import sqlite3
import subprocess
from collections import defaultdict

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy.optimize import brentq, curve_fit, minimize
from scipy.spatial import cKDTree

import common as C

MI = 1.609344

GOLD = dict(
    loc='ratio',
    study_by_date=True,
    # The five Level-5 decisive judgments (all ON in golden)
    contacts='trajectory',     # S1: 'trajectory' | 'signature' | 'underbuild_all'
    tap_infeed='dual',         # S2: 'dual' | 'none' | 'solar_only' | 'over'
    dc_mutual='coupled',       # S3: 'coupled' | 'uncoupled' | 'over' | 'one_fact'
    deposit='joint',           # S4: 'joint' | 'esdd_wind' | 'over_nsdd' | 'one_fact' | 'const' | 'latest' | 'history'
    topology='as_operated',    # S5: 'as_operated' | 'static' | 'over_both' | 'oms_direct'
    # Reflex moves (all ON in golden & reflex route)
    fog='stations',
    survey=True,
    growin='thermal',
    # Variant-battery knobs (each at the golden's default)
    fog_dep=0.5,
    storm_n=3,
    storm_km=8.0,
    tc_min=40.0,
    gust_min=9.5,
    win_km=0.4,
    src_scale=1.0,
    traj_n=4,
    traj_slope=-0.8,
    wind_k=2.0,
    gulf_from=140.0,
    inland_from=325.0,
    wind_src='stations',
    rate='expfloor',
    level='pct',
    level_q=10,
    beta_override=None,
    beta_model='logistic',     # 'logistic' | 'probit' | 'poisson'
    esdd_k_scale=1.0,
    nsdd_k_scale=1.0,
    rate_scale=1.0,
    level_scale=1.0,
    salt_bg=None,
    dust_bg=None,
    budget_days=None,
    infeed_scale=1.0,
    dc_z0m_scale=1.0,
    dc_len_override=None,
)


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
    """a Central prevailing wall-clock string to aware UTC (repeated autumn hour read as first)"""
    fmt = '%Y-%m-%d %H:%M:%S.%f' if '.' in s else ('%Y-%m-%d %H:%M' if len(s) == 16 else '%Y-%m-%d %H:%M:%S')
    t = dt.datetime.strptime(s, fmt)
    return t.replace(tzinfo=C.TZ).astimezone(C.UTC)


def _xy(lat, lon):
    return (lon - (-97.02)) * 111.32 * math.cos(math.radians(28.18)), (lat - 28.18) * 110.95


# ------------------------------------------------------------------------------------------------ loading from target/

def parse_procedure_budget(path):
    """Extract the filed Priority 1 crew-day allowance from RP-04 Rev 5 Word document."""
    xml = subprocess.run(['unzip', '-p', path, 'word/document.xml'], capture_output=True, text=True).stdout
    txt = re.sub(r'<[^>]+>', ' ', xml)
    m = re.search(r'line-crew allowance\s*\((\d+)\s*crew-days\)', txt)
    return int(m.group(1)) if m else C.CREW_BUDGET_DAYS


def study_table(path):
    """Parse line-out source table, double-circuit Z0m/DC_KM/Inland bus Z0, and IPP tap Z0s from protection study PDF."""
    txt = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout
    flat = re.sub(r'\s+', ' ', txt)
    out = {}
    for m in re.finditer(r'Line\s+(\d+)\s+([A-Za-z ]+?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', txt):
        lid = 'L%02d' % int(m.group(1))
        out[(lid, m.group(2).strip())] = (
            cmath.rect(float(m.group(3)), math.radians(float(m.group(4)))),
            cmath.rect(float(m.group(5)), math.radians(float(m.group(6)))),
        )
    # Double-circuit mutual coupling block
    m_dc = re.search(
        r'to the ([\d.]+) km corridor junction.*?Z0m = ([\d.]+) \+ j([\d.]+) ohm/km.*?'
        r'bus zero-sequence source impedance is ([\d.]+) ohm at ([\d.]+) degrees',
        flat,
    )
    if m_dc:
        out['DC_KM'] = float(m_dc.group(1))
        out['DC_Z0M'] = complex(float(m_dc.group(2)), float(m_dc.group(3)))
        out['INL_BUS_Z0'] = cmath.rect(float(m_dc.group(4)), math.radians(float(m_dc.group(5))))
    # IPP tap GSUs (Coyote Draw Solar on Line 9, Brushy Creek BESS on Line 8)
    for m_g in re.finditer(
        r'tap on Line (\d+) at ([\d.]+) km from [A-Za-z ]+\):.*?'
        r'zero-sequence impedance seen from the 69 kV tap point ([\d.]+) ohm at ([\d.]+) degrees',
        flat,
    ):
        lid = 'L%02d' % int(m_g.group(1))
        out[('GSU0', lid)] = cmath.rect(float(m_g.group(3)), math.radians(float(m_g.group(4))))
    return out


def auto_in_service(xf):
    r = xf[(xf['Location'] == 'Inland') & (xf['Unit'].str.startswith('T2'))].iloc[0]
    return dt.datetime.strptime(str(r['In service'])[:10], '%Y-%m-%d').replace(tzinfo=C.UTC)


def load(target):
    p = lambda k: os.path.join(target, C.FILES[k])
    d = {}
    lines = _wb(p('lines'), 'Lines')
    d['lines'] = {}
    for _, r in lines.iterrows():
        lid = 'L%02d' % int(str(r['Line']).split()[1])
        d['lines'][lid] = dict(
            id=lid, a_name=r['Terminal A'], b_name=r['Terminal B'], length=float(r['Length (km)']),
            conductor=r['Conductor'],
            z1=complex(float(r['R1 (ohm/km)']), float(r['X1 (ohm/km)'])),
            z0=complex(float(r['R0 (ohm/km)']), float(r['X0 (ohm/km)'])),
            insulators=r['Insulators'],
        )
    st = _wb(p('subs'), 'Stations')
    name_to_code = {r['Station']: r['Code'] for _, r in st.iterrows()}
    d['stations'] = {r['Code']: dict(name=r['Station'], relay=r['Relays on the 69 kV line terminals']) for _, r in st.iterrows()}
    for L in d['lines'].values():
        L['a'], L['b'] = name_to_code[L['a_name']], name_to_code[L['b_name']]
    taps = _wb(p('lines'), 'Taps')
    d['taps'] = []
    for _, r in taps.iterrows():
        alt_str = str(r['Second 69 kV source'] or '').strip()
        alt_lid = 'L%02d' % int(alt_str.split()[1]) if alt_str.startswith('Line') else None
        d['taps'].append(dict(
            name=r['Tap substation'], line='L%02d' % int(str(r['Line']).split()[1]),
            km=float(r['Distance from terminal A (km)']), members=int(r['Members (Oct 2026)']),
            backup={'automatic throw-over': 'auto', 'by control room (SCADA)': 'manual'}.get(r['Transfer to second source'] or '', 'none'),
            alt=alt_lid,
        ))
    ipp_tab = _wb(p('lines'), 'IPP taps', header_row=0)
    d['ipp_taps'] = {}
    for _, r in ipp_tab.iterrows():
        lid = 'L%02d' % int(str(r['Line']).split()[1])
        d['ipp_taps'][lid] = dict(
            facility=str(r['Facility']),
            tap_km=float(r['Tap distance from terminal A (km)']),
            tap_len=float(r['Tap line length (km)']),
            in_service=dt.datetime.strptime(str(r['In service'])[:10], '%Y-%m-%d').replace(tzinfo=C.UTC),
        )
    xf = _wb(p('subs'), 'Transformers')
    d['transformers'] = xf
    s = pd.read_csv(p('structures'))
    s['lid'] = s['structure_id'].str.slice(0, 3)
    d['structures'] = s
    d['settings'] = _wb(p('settings'), 'Line relays')
    d['studies'] = {2022: study_table(p('study22')), 2025: study_table(p('study25'))}
    d['study_dates'] = {2022: dt.datetime(2022, 1, 1, tzinfo=C.UTC), 2025: auto_in_service(xf)}
    d['budget_days'] = parse_procedure_budget(p('procedure'))
    d['er'] = pd.read_csv(p('er'), dtype={'Location': str})
    d['gv'] = pd.DataFrame(json.load(open(p('gv')))['records'])
    d['soe'] = pd.read_csv(p('soe'))
    d['ipp'] = pd.read_csv(p('ipp'))
    d['ipp2'] = pd.read_csv(p('ipp2'))
    d['members'] = pd.read_csv(p('members'))
    con = sqlite3.connect(p('oms'))
    d['feeders'] = pd.read_sql('select * from feeder', con)
    d['oms_los'] = pd.read_sql("select * from outage where cause_code='LOS'", con)
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
                         zone=str(r['Targets']), shot=int(r['Shot']), dist=dist,
                         I={'A': float(r['IA']), 'B': float(r['IB']), 'C': float(r['IC'])},
                         IG=float(r['IG']), fam='ER'))
    for _, r in d['gv'].iterrows():
        st, ln = r['device'].split('_')[0], r['device'].split('_')[1]
        lid = 'L%02d' % int(ln[1:])
        t = _local_to_utc(r['time_local'])
        recs.append(dict(station=st, line=lid, end=ends[(st, lid)], t=t, type=r['fault_type'], trip=bool(r['trip']),
                         zone=str(r['element']), shot=int(r['reclose_shot']),
                         dist=(None if pd.isna(r['distance_km']) else float(r['distance_km'])),
                         I={'A': r['ia_ka'] * 1000, 'B': r['ib_ka'] * 1000, 'C': r['ic_ka'] * 1000},
                         IG=r['in_ka'] * 1000, fam='GV'))
    return recs


def soe_breakers(d):
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
    """One fault per two-ended protection sequence within 60 s; records exact raw LOCKOUT boolean on each fault
    (fixing Arch 6 deliver.py cleared_on_reclose bug) and matches relay records on each relay's own clock."""
    if '_base_faults' in d:
        return [dict(f) for f in d['_base_faults']]
    all_bkr = soe_breakers(d)
    trips = [x for x in all_bkr if x['state'] == 'OPEN' and x['cause'] == 'PROT']
    locks = defaultdict(list)
    for x in all_bkr:
        if x['state'] == 'LOCKOUT':
            locks[x['line']].append(x['t'])
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
                locked = any(0 <= (lt - t0).total_seconds() <= 60.0 for lt in locks[lid])
                faults.append(dict(line=lid, t=t0, soe=grp, locked=locked))
            i += len(grp)
    faults.sort(key=lambda f: f['t'])

    all_recs = relay_records(d)
    recs = [r for r in all_recs if r['trip']]
    by_relay = defaultdict(list)
    for r in recs:
        by_relay[(r['station'], r['line'])].append(r)
    for key in by_relay:
        by_relay[key].sort(key=lambda r: r['t'])
    for f in faults:
        f['rec'] = {}
        f['par_rec'] = {}

    # Synchronize relay clocks against SCADA UTC across all lines at each station (no per-line median smearing)
    st_pairs = defaultdict(list)
    for (st, lid), rs in by_relay.items():
        fl = [f for f in faults if f['line'] == lid]
        if not fl:
            continue
        ft = np.array([f['t'].timestamp() for f in fl])
        for r in [x for x in rs if x['shot'] == 0]:
            j = int(np.argmin(np.abs(ft - r['t'].timestamp())))
            dtt = r['t'].timestamp() - ft[j]
            if abs(dtt) <= 200.0:
                fl[j]['rec'][r['end']] = dict(r, offset=dtt)
                st_pairs[st].append((r['t'].timestamp(), dtt))

    relay_clock = {}
    for st, ps in st_pairs.items():
        ps.sort()
        relay_clock[st] = (np.array([p[0] for p in ps]), np.array([p[1] for p in ps]))

    # Match non-tripping 51N PU parallel-line pickups on double-circuit Lines 10 & 11
    par_recs = [r for r in all_recs if (not r['trip']) and r['line'] in ('L10', 'L11') and '51N' in r['zone']]
    for lid in ('L10', 'L11'):
        other = 'L11' if lid == 'L10' else 'L10'
        fl = [f for f in faults if f['line'] == lid]
        if not fl:
            continue
        ft = np.array([f['t'].timestamp() for f in fl])
        for r in [x for x in par_recs if x['line'] == other]:
            clk = relay_clock.get(r['station'])
            o = float(np.interp(r['t'].timestamp(), clk[0], clk[1])) if clk is not None else 0.0
            j = int(np.argmin(np.abs(ft - (r['t'].timestamp() - o))))
            if abs(r['t'].timestamp() - o - ft[j]) < 5.0:
                fl[j]['par_rec'][r['end']] = r
    d['_base_faults'] = [dict(f) for f in faults]
    return [dict(f) for f in d['_base_faults']]


def _ipp_records(df):
    s = df[df['description'].str.contains('GND FAULT', na=False)]
    out = []
    for _, r in s.iterrows():
        t = dt.datetime.strptime(r['timestamp'], '%m/%d/%Y %H:%M:%S.%f').replace(tzinfo=C.CST).astimezone(C.UTC)
        out.append(dict(t=t, I={'A': r['ia_ka'] * 1000, 'B': r['ib_ka'] * 1000, 'C': r['ic_ka'] * 1000}, IG=r['in_ka'] * 1000))
    return out


# ------------------------------------------------------------------------------------------------ S2 & S3: location

def _sources(d, lid, t, by_date):
    L = d['lines'][lid]
    yr = 2025
    if by_date and t < d['study_dates'][2025]:
        yr = 2022
    tab = d['studies'][yr]
    return tab[(lid, d['stations'][L['a']]['name'])], tab[(lid, d['stations'][L['b']]['name'])], tab


def ratio_location(d, lid, iga, igb, t, by_date=True):
    """Standard uncoupled two-ended residual-current split location."""
    L = d['lines'][lid]
    (_, z0a), (_, z0b), _ = _sources(d, lid, t, by_date)
    z0a, z0b = z0a * d.get('src_scale', 1.0), z0b * d.get('src_scale', 1.0)
    z0, Lk = L['z0'], L['length']
    fn = lambda x: abs(z0b + (Lk - x) * z0) / abs(z0a + x * z0) - iga / igb
    xs = np.linspace(0.01, Lk - 0.01, 400)
    fs = np.array([fn(x) for x in xs])
    for i in range(len(xs) - 1):
        if fs[i] == 0 or fs[i] * fs[i + 1] < 0:
            return float(brentq(fn, xs[i], xs[i + 1]))
    return None


def _dc_zero_ratio(d, lid, x, t, by_date=True, z0m_scale=1.0, dc_len_override=None):
    """Exact coupled 2-line zero-sequence ratio |I0_A(x)| / |I0_B(x)| for double-circuit Lines 10 & 11
    using ONLY parameters parsed from target/ (line register + protection studies)."""
    l10, l11 = d['lines']['L10'], d['lines']['L11']
    (_, _), (_, z0_msq), tab = _sources(d, 'L10', t, by_date)
    (_, _), (_, z0_grg), _ = _sources(d, 'L11', t, by_date)
    z0_inl = tab['INL_BUS_Z0'] * d.get('src_scale', 1.0)
    z0_msq = z0_msq * d.get('src_scale', 1.0)
    z0_grg = z0_grg * d.get('src_scale', 1.0)
    z0_10, z0_11 = l10['z0'], l11['z0']
    z0m = tab['DC_Z0M'] * z0m_scale
    L10, L11 = l10['length'], l11['length']
    Lm = dc_len_override if dc_len_override is not None else tab['DC_KM']
    Lm = min(Lm, min(L10, L11) - 0.05)

    def solve_nodal(nodes, branches, coupled):
        idx = {n: i for i, n in enumerate(nodes)}
        Y = np.zeros((len(nodes), len(nodes)), complex)
        I = np.zeros(len(nodes), complex)
        for n1, n2, z in branches:
            y = 1.0 / z
            i = idx[n1]
            Y[i, i] += y
            if n2 is not None:
                j = idx[n2]
                Y[j, j] += y
                Y[i, j] -= y
                Y[j, i] -= y
        for (a1, b1, a2, b2), Zmat in coupled:
            Ym = np.linalg.inv(Zmat)
            pairs = [(a1, b1), (a2, b2)]
            for r in range(2):
                for c in range(2):
                    y = Ym[r, c]
                    for nr, sr in ((pairs[r][0], 1), (pairs[r][1], -1)):
                        for nc, sc in ((pairs[c][0], 1), (pairs[c][1], -1)):
                            Y[idx[nr], idx[nc]] += sr * sc * y
        I[idx['F']] = -1.0
        return dict(zip(nodes, np.linalg.solve(Y, I)))

    if x < Lm - 0.01:
        nodes = ['INL', 'F', 'P_d', 'M10', 'M11', 'MSQ', 'GRG']
        if lid == 'L11':
            coupled = [
                (('INL', 'P_d', 'INL', 'F'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * x),
                (('P_d', 'M10', 'F', 'M11'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * (Lm - x)),
            ]
        else:
            coupled = [
                (('INL', 'F', 'INL', 'P_d'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * x),
                (('F', 'M10', 'P_d', 'M11'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * (Lm - x)),
            ]
        branches = [('M10', 'MSQ', z0_10 * (L10 - Lm)), ('M11', 'GRG', z0_11 * (L11 - Lm)),
                    ('INL', None, z0_inl), ('MSQ', None, z0_msq), ('GRG', None, z0_grg)]
        v = solve_nodal(nodes, branches, coupled)
        Z1 = np.array([[z0_10, z0m], [z0m, z0_11]], complex) * x
        dv = np.array([v['INL'] - v['P_d'], v['INL'] - v['F']]) if lid == 'L11' else np.array([v['INL'] - v['F'], v['INL'] - v['P_d']])
        i10_a, i11_a = np.linalg.solve(Z1, dv)
        i10_b = (v['MSQ'] - v['M10']) / (z0_10 * (L10 - Lm))
        i11_b = (v['GRG'] - v['M11']) / (z0_11 * (L11 - Lm))
    else:
        nodes = ['INL', 'M10', 'M11', 'F', 'MSQ', 'GRG']
        coupled = [(('INL', 'M10', 'INL', 'M11'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * Lm)]
        if lid == 'L11':
            branches = [('M10', 'MSQ', z0_10 * (L10 - Lm)), ('M11', 'F', z0_11 * (x - Lm)),
                        ('F', 'GRG', z0_11 * (L11 - x)), ('INL', None, z0_inl), ('MSQ', None, z0_msq), ('GRG', None, z0_grg)]
        else:
            branches = [('M11', 'GRG', z0_11 * (L11 - Lm)), ('M10', 'F', z0_10 * (x - Lm)),
                        ('F', 'MSQ', z0_10 * (L10 - x)), ('INL', None, z0_inl), ('MSQ', None, z0_msq), ('GRG', None, z0_grg)]
        v = solve_nodal(nodes, branches, coupled)
        Z1 = np.array([[z0_10, z0m], [z0m, z0_11]], complex) * Lm
        i10_a, i11_a = np.linalg.solve(Z1, np.array([v['INL'] - v['M10'], v['INL'] - v['M11']]))
        i10_b = (v['MSQ'] - (v['F'] if lid == 'L10' else v['M10'])) / (z0_10 * (L10 - (x if lid == 'L10' else Lm)))
        i11_b = (v['GRG'] - (v['F'] if lid == 'L11' else v['M11'])) / (z0_11 * (L11 - (x if lid == 'L11' else Lm)))
    ia, ib = (i11_a, i11_b) if lid == 'L11' else (i10_a, i10_b)
    return abs(ia) / max(abs(ib), 1e-12)


def dc_coupled_location(d, lid, iga, igb, t, opts):
    """Solve coupled double-circuit zero-sequence equations for distance x from Inland (km)."""
    Lk = d['lines'][lid]['length']
    z0m_sc = opts.get('dc_z0m_scale', 1.0)
    dc_len = opts.get('dc_len_override')
    if opts.get('dc_mutual') == 'over':
        z0m_sc = 1.95
        dc_len = Lk - 0.1
    yr = 2022 if (opts['study_by_date'] and t < d['study_dates'][2025]) else 2025
    key = (lid, yr, round(z0m_sc, 4), dc_len, round(d.get('src_scale', 1.0), 4))
    cache = d.setdefault('_dc_curve', {})
    if key not in cache:
        xs = np.linspace(0.15, Lk - 0.15, 140)
        rs = np.array([_dc_zero_ratio(d, lid, x, t, opts['study_by_date'], z0m_sc, dc_len) for x in xs])
        cache[key] = (xs, rs)
    xs, rs = cache[key]
    target = iga / igb
    vals = rs - target
    for i in range(len(xs) - 1):
        if vals[i] == 0 or vals[i] * vals[i + 1] < 0:
            # Linear interpolation across dense 140-pt grid (~0.18 km spacing) refined by brentq
            return float(brentq(lambda x: _dc_zero_ratio(d, lid, x, t, opts['study_by_date'], z0m_sc, dc_len) - target,
                                xs[i], xs[i + 1], xtol=1e-3))
    return float(xs[int(np.argmin(np.abs(vals)))])


def locate(d, faults, opts):
    ipp_map = {'L09': _ipp_records(d['ipp']), 'L08': _ipp_records(d['ipp2'])}
    ipp_ts = {k: np.array([r['t'].timestamp() for r in v]) if v else np.array([]) for k, v in ipp_map.items()}
    dc_mode = opts.get('dc_mutual', 'coupled')
    ti_mode = opts.get('tap_infeed', 'dual')
    for f in faults:
        lid = f['line']
        L = d['lines'][lid]
        ra, rb = f['rec'].get('a'), f['rec'].get('b')
        f['type'] = (ra or rb or {}).get('type')
        km = None
        slg = f['type'] in ('AG', 'BG', 'CG')
        if opts['loc'] == 'ratio' and ra and rb and slg:
            if lid in ('L10', 'L11') and dc_mode in ('coupled', 'over'):
                km = dc_coupled_location(d, lid, ra['IG'], rb['IG'], f['t'], opts)
            elif lid in ('L10', 'L11') and dc_mode == 'one_fact':
                # One-fact shortcut: apply a constant +0.65 km empirical shift on top of uncoupled ratio
                u = ratio_location(d, lid, ra['IG'], rb['IG'], f['t'], opts['study_by_date'])
                km = min(L['length'] - 0.05, u + 0.65) if u is not None else None
            else:
                km = ratio_location(d, lid, ra['IG'], rb['IG'], f['t'], opts['study_by_date'])
        if km is None:
            ests = []
            if ra and ra['dist'] is not None:
                ests.append(ra['dist'])
            if rb and rb['dist'] is not None:
                ests.append(L['length'] - rb['dist'])
            # Dual IPP lateral tap ground-infeed inversion (Line 9 Coyote Draw Solar & Line 8 Brushy Creek BESS)
            apply_ipp = (
                (ti_mode in ('dual', 'over') and lid in d['ipp_taps']) or
                (ti_mode == 'solar_only' and lid == 'L09')
            )
            if apply_ipp and ra and ra['dist'] is not None and slg:
                tap_km = d['ipp_taps'][lid]['tap_km']
                if ra['dist'] > tap_km and len(ipp_ts.get(lid, [])):
                    ts_arr = ipp_ts[lid]
                    j = int(np.argmin(np.abs(ts_arr - f['t'].timestamp())))
                    if abs(ts_arr[j] - f['t'].timestamp()) < 2.0:
                        r = ipp_map[lid][j]
                        p = f['type'][0]
                        k0 = abs((L['z0'] - L['z1']) / (3 * L['z1']))
                        k = (r['I'][p] + k0 * r['IG']) / max(ra['I'][p] + k0 * ra['IG'], 1e-6)
                        k *= (1.85 if ti_mode == 'over' else opts.get('infeed_scale', 1.0))
                        ests = [tap_km + (ra['dist'] - tap_km) / (1.0 + k)]
            if ests:
                km = float(np.mean(ests))
        f['km'] = km
        if km is not None:
            if '_st_by_lid' not in d:
                d['_st_by_lid'] = {
                    k_: (g_['km_from_terminal_a'].to_numpy(), g_['structure_no'].to_numpy(dtype=int))
                    for k_, g_ in d['structures'].groupby('lid')
                }
            kms, nos_arr = d['_st_by_lid'][lid]
            j = int(np.argmin(np.abs(kms - km)))
            f['structure'] = int(nos_arr[j])
            k2 = j + 1 if (j + 1 < len(kms) and km > kms[j]) else j - 1
            f['span'] = tuple(sorted((int(nos_arr[j]), int(nos_arr[max(k2, 0)]))))
        else:
            f['structure'] = None
            f['span'] = None
    return faults


# ------------------------------------------------------------------------------------------------ cause classification

def _asos(df):
    df = df.copy()
    df['t'] = pd.to_datetime(df['valid']).dt.tz_localize('UTC')
    df['hour'] = df['t'].dt.floor('h')
    df['tc'] = (df['tmpf'] - 32) * 5 / 9
    df['dc'] = (df['dwpf'] - 32) * 5 / 9
    df['gust_ms'] = pd.to_numeric(df['gust'], errors='coerce') / 1.94384
    df['rain_mm'] = pd.to_numeric(df['p01i'].replace('T', '0.05'), errors='coerce').fillna(0.0) * 25.4
    return {r.hour: r for r in df.itertuples()}


def weather_index(d):
    if '_wx_idx' in d:
        return d['_wx_idx']
    aptd = _asos(d['apt'])
    inad = _asos(d['ina'])
    sw = d['stations_wx'].copy()
    ts = pd.to_datetime(sw['hour_local']).dt.tz_localize(C.ZONE, ambiguous=True, nonexistent='shift_forward').dt.tz_convert('UTC')
    sw['t'] = ts
    swd = {(r.station, r.t): r for r in sw.itertuples()}
    d['_wx_idx'] = (aptd, inad, swd)
    return d['_wx_idx']


APT_XY, INA_XY = (76.0, 27.0), (16.0, 54.0)
STATION_XY = {
    'PORT ALCORN SUB': (76.0, 27.0), 'SHELL RIDGE SUB': (88.0, 43.0), 'SEDGE POINT SUB': (97.0, 60.0),
    'TULE MARSH SUB': (68.0, 31.0), 'CANEY BEND SUB': (60.0, 41.0), 'MESQUITE FLAT SUB': (36.0, 44.0),
}


def fault_xy(d, f):
    if '_st_xy' not in d:
        s = d['structures']
        d['_st_xy'] = {(r.lid, int(r.structure_no)): _xy(float(r.latitude), float(r.longitude)) for r in s.itertuples()}
    return d['_st_xy'].get((f['line'], f['structure']))


def roost_structures(d):
    if '_roosts' in d:
        return d['_roosts']
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
    d['_roosts'] = out
    return out


def conductor_temp(i, cond, ta, wind, solar):
    import loads as Lmod
    return Lmod.conductor_temp(i, cond, ta, wind, solar)


def line_xy(d):
    if '_lxy' in d:
        return d['_lxy']
    s = d['structures']
    out = {}
    for lid, grp in s.groupby('lid'):
        out[lid] = np.array([_xy(la, lo) for la, lo in zip(grp['latitude'], grp['longitude'])])
    d['_lxy'] = out
    return out


def classify(d, faults, opts):
    aptd, inad, swd = weather_index(d)
    if '_cg_st' not in d:
        st = d['strokes']
        st = st[st['type'] == 'CG']
        st_t = pd.DatetimeIndex(pd.to_datetime(st['time_utc'])).as_unit('ns').asi8 / 1e9
        sxy = np.array([_xy(a, b) for a, b in zip(st['latitude'], st['longitude'])])
        d['_cg_st'] = (st_t, sxy)
    st_t, sxy = d['_cg_st']
    lxy = line_xy(d)
    roosts = roost_structures(d) if opts['survey'] else {}
    roost_set = {(l, n) for (l, n, c) in roosts.values()}
    if '_loadd' not in d:
        load = d['loading'].copy()
        load['t'] = pd.to_datetime(load['hour_utc']).dt.tz_localize('UTC')
        d['_loadd'] = {r['t']: r for r in load.to_dict('records')}
    loadd = d['_loadd']
    if '_st_attr' not in d:
        s = d['structures']
        d['_st_attr'] = {
            (r.lid, int(r.structure_no)): (r.insulator == 'porcelain', False if pd.isna(r.underbuild) else bool(str(r.underbuild).strip()))
            for r in s.itertuples()
        }
    st_attr = d['_st_attr']
    gulf = {'L01', 'L02', 'L03', 'L04'}
    for f in faults:
        f['cause'] = 'unknown'
        xy = fault_xy(d, f) if f['structure'] is not None else None
        tt = f['t'].timestamp()
        lt = C.to_local(f['t'])
        hr = f['t'].replace(minute=0, second=0, microsecond=0)
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
        if lt.month in (10, 11, 12, 1, 2, 3, 4):
            if b is not None and not pd.isna(b.gust_ms):
                gust = float(b.gust_ms)
        src = None
        if opts['fog'] == 'stations':
            near = sorted(STATION_XY, key=lambda n: math.hypot(STATION_XY[n][0] - ref[0], STATION_XY[n][1] - ref[1]))
            for n in near[:2]:
                r = swd.get((n, hr))
                if r is not None and math.hypot(STATION_XY[n][0] - ref[0], STATION_XY[n][1] - ref[1]) <= 24.0:
                    src = r
                    break
        wet_inland = False
        if src is not None:
            fog = False
            seen = False
            for n in near[:2]:
                if math.hypot(STATION_XY[n][0] - ref[0], STATION_XY[n][1] - ref[1]) > 24.0:
                    continue
                for dh in (-1, 0, 1):
                    r2 = swd.get((n, hr + dt.timedelta(hours=dh)))
                    if r2 is not None:
                        seen = True
                        if (r2.air_temp_c - r2.dewpoint_c) <= opts['fog_dep']:
                            fog = True
                        if (r2.air_temp_c - r2.dewpoint_c) <= 1.2 or r2.rain_mm >= 0.2:
                            wet_inland = True
            if not seen:
                fog = a is not None and isinstance(a.wxcodes, str) and 'FG' in a.wxcodes
            rain = src.rain_mm >= 0.25
            tair, wind = src.air_temp_c, src.wind_ms
        else:
            if math.hypot(ref[0] - INA_XY[0], ref[1] - INA_XY[1]) < math.hypot(ref[0] - APT_XY[0], ref[1] - APT_XY[1]) and b is not None:
                a2 = b
            else:
                a2 = a
            wxc = str(a2.wxcodes) if (a2 is not None and isinstance(a2.wxcodes, str)) else ''
            fog = ('FG' in wxc) or (opts['fog'] == 'airport' and 'BR' in wxc)
            rain = a2 is not None and (a2.rain_mm >= 0.25 or 'RA' in wxc or 'DZ' in wxc)
            wet_inland = fog or rain or ('BR' in wxc) or (a2 is not None and (a2.tc - a2.dc) <= 1.5)
            tair = a2.tc if a2 is not None else 25.0
            wind = (a2.sknt / 1.94384) if a2 is not None and not pd.isna(a2.sknt) else 2.0
        # Also check nearby airport moisture for inland strings >18 km from substation stations
        for ap_r in (a, b):
            if ap_r is not None:
                wxc_ap = str(ap_r.wxcodes) if isinstance(ap_r.wxcodes, str) else ''
                if ap_r.rain_mm >= 0.2 or 'FG' in wxc_ap or 'BR' in wxc_ap or 'RA' in wxc_ap or 'DZ' in wxc_ap:
                    if math.hypot(ref[0] - (APT_XY[0] if ap_r is a else INA_XY[0]),
                                  ref[1] - (APT_XY[1] if ap_r is a else INA_XY[1])) <= 38.0:
                        wet_inland = True
        night = lt.hour >= 21 or lt.hour <= 10
        porcelain, underbuild = st_attr.get((f['line'], f['structure']), (False, False)) if xy is not None else (False, False)
        near_roost = any(l == f['line'] and abs(n - (f['structure'] or -99)) <= 2 for (l, n) in roost_set)
        summer_pm = lt.month in (5, 6, 7, 8, 9, 10) and 12 <= lt.hour <= 19
        tc, amps = None, None
        if summer_pm:
            lr = loadd.get(hr)
            L = d['lines'][f['line']]
            col = [c for c in (lr or {}) if c.endswith('_L%d_AMPS' % int(f['line'][1:]))]
            if lr is not None and col:
                amps = float(lr[col[0]])
                tc = conductor_temp(amps, L['conductor'], tair, wind, 850.0)
        f['sig'] = dict(
            storm=storm, gust=gust, fog=fog, rain=rain, wet=wet_inland or rain or fog, night=night,
            roost=near_roost and lt.month in (11, 12, 1, 2, 3) and lt.hour <= 7,
            summer_pm=summer_pm, tc=tc, gulf_porcelain=(f['line'] in gulf and porcelain),
            underbuild=underbuild, amps=(round(amps) if amps is not None else None),
            tair=round(float(tair), 1), wind=round(float(wind), 1),
        )
        sg = f['sig']
        if opts['growin'] == 'season' and summer_pm:
            f['cause'] = 'growin'
            continue
        if sg['roost']:
            f['cause'] = 'bird'
            continue
        if night and fog and sg['gulf_porcelain'] and not storm:
            f['cause'] = 'fog'
            continue
        if storm or (gust >= opts['gust_min'] and (f['line'] not in gulf or not fog)):
            f['cause'] = 'fallin'
            continue
        if summer_pm and not rain and tc is not None and tc >= opts['tc_min']:
            f['cause'] = 'growin'
            continue
    # Patrol findings (includes 'dead bird'/'droppings' keyword fix from Arch 6)
    pat = d['patrols']
    for _, r in pat.iterrows():
        txt = str(r['Findings']).lower()
        lid = 'L%02d' % int(str(r['Line']).split()[1])
        day = pd.Timestamp(r['Date']).date()
        cand = [f for f in faults if f['line'] == lid and 0 <= (day - C.to_local(f['t']).date()).days <= 6]
        if not cand:
            continue
        f = min(cand, key=lambda f: abs((day - C.to_local(f['t']).date()).days))
        for keys, cause in (
            (('vehicle', 'truck'), 'vehicle'),
            (('connector', 'clamp'), 'hardware'),
            (('outside the right of way', 'dead pine'), 'fallin'),
            (('grown up into', 'reaching the bottom phase'), 'growin'),
            (('cracked porcelain', 'broken bell'), 'insulator'),
            (('dead bird', 'droppings'), 'bird'),
        ):
            if any(k_ in txt for k_ in keys):
                f['cause'] = cause
                f['patrol'] = True
    return faults


def settle_clusters(faults, opts):
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
            elif sum(1 for x in sg if x.get('summer_pm') and not x.get('storm') and not x.get('rain')) / max(1, len(sg)) >= 0.70:
                cause = 'growin'
            elif share('wet') >= 0.40 or share('rain') + share('fog') >= 0.35:
                cause = 'insulator'
            else:
                cause = 'unknown'
            for g in grp:
                if not g.get('patrol') and not (cause == 'insulator' and g['cause'] == 'fallin'):
                    g['cause'] = cause
    return faults


def plate_to_current(d, lid, no, day):
    s = d['structures']
    s = s[(s['lid'] == lid) & s['former_no'].notna()]
    if len(s) == 0:
        return no
    rebuilt = d.get('rebuilt', {}).get(lid)
    if rebuilt is not None and day >= rebuilt:
        return no
    r = s[s['former_no'].astype(float).astype(int) == int(no)]
    return int(r.iloc[0]['structure_no']) if len(r) else no


def settle_replaced_strings(d, faults, opts):
    m = d['maint']
    m = m[m['work_type'] == 'INSULATOR']
    for _, r in m.iterrows():
        lid = 'L%02d' % int(str(r['line']).split()[1])
        day = pd.Timestamp(r['completed']).date()
        no = plate_to_current(d, lid, int(r['structure']), pd.Timestamp(r['opened']).date())
        for f in faults:
            if f['line'] != lid or f['structure'] is None or abs(f['structure'] - no) > 1:
                continue
            fd = C.to_local(f['t']).date()
            if f['cause'] in ('fog', 'unknown') and day - dt.timedelta(days=365) <= fd <= day:
                f['cause'] = 'insulator'
    return faults


# ------------------------------------------------------------------------------------------------ S1: thermal sag trajectories

def settle_contacts(d, faults, opts):
    """S1: Separate 12.47 kV underbuild clearance spans from growing trees using post-trim IEEE 738 contact
    temperature trajectories. Underbuilt grow-ins (L14 62-63, L12 44-45) defeat any raw underbuild filter."""
    mode = opts.get('contacts', 'trajectory')
    if mode == 'signature':
        return []
    by = defaultdict(list)
    for f in faults:
        if f['cause'] == 'growin' and f['km'] is not None and isinstance(f.get('sig'), dict) and f['sig'].get('tc') is not None:
            by[f['line']].append(f)
    v = d['veg']
    out = []
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
        lname = 'Line %d' % int(lid[1:])
        vv = v[(v['line'] == lname) & v['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])]
        for grp in merged:
            lo = min(g['structure'] for g in grp) - 1
            hi = max(g['structure'] for g in grp) + 1
            has_ub = any(g['sig'].get('underbuild') for g in grp)
            if not has_ub:
                continue
            last_contact = max(C.to_local(g['t']).date() for g in grp)
            trims = []
            for _, r in vv.iterrows():
                day = pd.Timestamp(r['completed']).date()
                a = plate_to_current(d, lid, int(r['from_structure']), day)
                b = plate_to_current(d, lid, int(r['to_structure']), day)
                if a <= hi and lo <= b and day <= last_contact:
                    trims.append(day)
            t_trim = max(trims) if trims else None
            after = [g for g in grp if t_trim is None or C.to_local(g['t']).date() > t_trim]
            summers = {C.to_local(g['t']).year for g in after}
            x = np.array([C.to_local(g['t']).year + C.to_local(g['t']).timetuple().tm_yday / 365.25 for g in after]) if after else np.array([])
            y = np.array([g['sig']['tc'] for g in after]) if after else np.array([])
            slope = float(np.polyfit(x, y, 1)[0]) if (len(after) >= 2 and len(summers) >= 2) else float('nan')
            if mode == 'underbuild_all':
                # Over-correction / one-fact shortcut: reclassify EVERY underbuilt summer contact cluster as clearance!
                if len(after) >= 3:
                    for g in grp:
                        g['cause'] = 'hardware'
                        g['fixed_contact'] = True
                    out.append(dict(line=lid, s_min=lo + 1, s_max=hi - 1, slope=slope, n=len(after), trim=t_trim,
                                    tc=[round(float(t_), 1) for t_ in y]))
                continue
            if len(after) < opts['traj_n'] or len(summers) < 3:
                continue
            if slope >= opts['traj_slope']:
                for g in grp:
                    g['cause'] = 'hardware'
                    g['fixed_contact'] = True
                out.append(dict(line=lid, s_min=lo + 1, s_max=hi - 1, slope=slope, n=len(after), trim=t_trim,
                                tc=[round(float(t_), 1) for t_ in y]))
    return out


# ------------------------------------------------------------------------------------------------ repeat locations

def repeat_locations(d, faults, win_km=0.4):
    out = []
    for cause in ('bird', 'insulator', 'growin', 'fallin', 'hardware'):
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
                out.append(dict(
                    line=lid, cause=cause, n=len(grp),
                    first=min(g['t'] for g in grp), last=max(g['t'] for g in grp),
                    structure=int(np.median(nos)), s_min=nos[0], s_max=nos[-1], span=span,
                    km=float(np.median([g['km'] for g in grp])), faults=grp,
                ))
    return out


def fixed_since(d, rl):
    last = C.to_local(rl['last']).date()
    lname = 'Line %d' % int(rl['line'][1:])
    lo, hi = rl['s_min'] - 1, rl['s_max'] + 1
    if rl['cause'] in ('bird', 'insulator', 'hardware'):
        typ = {'bird': 'AVIAN', 'insulator': 'INSULATOR', 'hardware': 'HARDWARE'}[rl['cause']]
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


# ------------------------------------------------------------------------------------------------ S5: chronological SCADA switching topology

def parse_switching_windows(d):
    """Replay SCADA SOE supervisory ALT SRC / NORM SW events chronologically to recover every multi-week
    abnormal feeding interval: (tap_name, normal_line, alt_line, t_start, t_end)."""
    if '_switch_windows' in d:
        return d['_switch_windows']
    soe = d['soe']
    sw = soe[soe['point'].str.contains('69KV ALT SRC|69KV NORM SW') & (soe['cause'] == 'SUPV')].copy()
    sw['t'] = pd.to_datetime(sw['time_utc']).dt.tz_localize('UTC')
    sw = sw.sort_values('t')
    code_to_tap = {}
    for _, r in d['feeders'].iterrows():
        code_to_tap[r['sub_code']] = r['substation']
    tap_info = {tp['name']: tp for tp in d['taps']}
    # Track planned windows where NORM SW opens (distinguishing multi-week planned switches from fault-time transfers!)
    active = {}
    windows = []
    for r in sw.itertuples():
        parts = r.point.split()
        code = parts[0]
        tap = code_to_tap.get(code)
        if tap is None or tap not in tap_info:
            continue
        lid = 'L%02d' % int(parts[-1][1:])
        if 'NORM SW' in r.point and r.state == 'OPEN':
            # Planned switch onto alt source started ~45s earlier when ALT SRC closed
            active[tap] = (tap_info[tap]['line'], tap_info[tap]['alt'], r.t - dt.timedelta(seconds=60))
        elif 'NORM SW' in r.point and r.state == 'CLOSE' and tap in active:
            norm, alt, t0 = active.pop(tap)
            windows.append(dict(tap=tap, normal=norm, alt=alt, start=t0, end=r.t))
    for tap, (norm, alt, t0) in active.items():
        windows.append(dict(tap=tap, normal=norm, alt=alt, start=t0, end=C.T_END))
    d['_switch_windows'] = windows
    return windows


def member_impact(d, faults, opts, year=None):
    """Recompute sustained member interruptions, member-minutes and momentary member events across 2022-2026
    (or a single year) under opts['topology'] ('as_operated' | 'static' | 'over_both' | 'oms_direct')."""
    topo = opts.get('topology', 'as_operated')
    soe = d['soe']
    if '_soe_t' not in d:
        d['_soe_t'] = soe.assign(t=pd.to_datetime(soe['time_utc']).dt.tz_localize('UTC'))
    soe_t = d['_soe_t']
    mem = d['members'].groupby(['month', 'substation'])['members'].sum().to_dict()
    code_of = dict(zip(d['feeders']['substation'], d['feeders']['sub_code']))
    if topo == 'as_operated':
        windows = parse_switching_windows(d)
    elif topo == 'over_both':
        windows = parse_switching_windows(d)
    elif topo == 'one_fact_2026':
        windows = [w for w in parse_switching_windows(d) if w['end'].year >= 2026]
    else:
        windows = []

    res_all = defaultdict(lambda: dict(sustained=0, minutes=0.0, momentary=0))
    res_26 = defaultdict(lambda: dict(sustained=0, minutes=0.0, momentary=0))

    if topo == 'oms_direct':
        # Direct route: read OMS LOS durations directly by substation's normal line
        tap_line = {tp['name']: tp['line'] for tp in d['taps']}
        fdr_tap = dict(zip(d['feeders']['feeder_id'], d['feeders']['substation']))
        los = d['oms_los'].copy()
        los['s'] = pd.to_datetime(los['start_time'])
        los['e'] = pd.to_datetime(los['restore_time'])
        los['mins'] = (los['e'] - los['s']).dt.total_seconds() / 60.0
        los['norm_line'] = los['feeder_id'].map(lambda fid: tap_line.get(fdr_tap.get(fid)))
        for f in faults:
            f['impact'] = dict(sustained=0, minutes=0.0, momentary=0)
        for r in los.itertuples():
            lid = r.norm_line
            if lid is None:
                continue
            m = int(r.members_out)
            mm = float(r.mins) * m
            res_all[lid]['sustained'] += m
            res_all[lid]['minutes'] += mm
            if r.s.year == 2026:
                res_26[lid]['sustained'] += m
                res_26[lid]['minutes'] += mm
        # Attach OMS LOS minutes to nearest lockout on the substation's normal line
        for f in faults:
            if not f['locked']:
                continue
            lt = C.to_local(f['t'])
            sub = los[(los['norm_line'] == f['line']) &
                      ((los['s'] - lt).abs() <= pd.Timedelta(minutes=15))]
            if len(sub):
                f['impact']['sustained'] = int(sub['members_out'].sum())
                f['impact']['minutes'] = float((sub['members_out'] * sub['mins']).sum())
        return dict(res_26) if year == 2026 else dict(res_all)

    # Pre-index 69 kV breaker CLOSE/reclose and ALT SRC CLOSE timestamps as sorted float arrays for fast binary search
    if '_soe_idx' not in d:
        bkr_df = soe_t[soe_t['point'].str.contains('69KV BKR')]
        alt_df = soe_t[soe_t['point'].str.contains('69KV ALT SRC') & (soe_t['state'] == 'CLOSE')]
        _to_s = lambda s: (pd.DatetimeIndex(s).as_unit('ns').asi8 / 1e9) if len(s) else np.empty(0)
        bkr_close, bkr_recl = {}, {}
        for lid_, L_ in d['lines'].items():
            bpts_ = {'%s 69KV BKR B52%02d' % (L_['a'], int(lid_[1:])), '%s 69KV BKR B62%02d' % (L_['b'], int(lid_[1:]))}
            sub_ = bkr_df[bkr_df['point'].isin(bpts_) & (bkr_df['state'] == 'CLOSE')]
            bkr_close[lid_] = np.sort(_to_s(sub_['t']))
            bkr_recl[lid_] = np.sort(_to_s(sub_[sub_['cause'] == '79 RECL']['t']))
        alt_close = {}
        for code_ in set(code_of.values()):
            sub_ = alt_df[alt_df['point'].str.startswith('%s 69KV ALT SRC' % code_)]
            alt_close[code_] = np.sort(_to_s(sub_['t']))
        d['_soe_idx'] = (bkr_close, bkr_recl, alt_close)
    bkr_close, bkr_recl, alt_close = d['_soe_idx']

    for f in faults:
        yr_f = C.to_local(f['t']).year
        if year is not None and yr_f != year:
            continue
        f['impact'] = dict(sustained=0, minutes=0.0, momentary=0)
        lid = f['line']
        t0 = f['t']
        t0_s = t0.timestamp()
        # Determine energized taps on lid at t0
        live_taps = []
        for tp in d['taps']:
            abn_win = next((w for w in windows if w['tap'] == tp['name'] and w['start'] <= t0 < w['end']), None)
            if topo in ('as_operated', 'one_fact_2026'):
                if abn_win is not None:
                    if abn_win['alt'] == lid:
                        live_taps.append((tp, True))
                elif tp['line'] == lid:
                    live_taps.append((tp, False))
            elif topo == 'over_both':
                # Over-correction: adds switched taps onto alt line WITHOUT removing them from normal line
                if abn_win is not None and abn_win['alt'] == lid:
                    live_taps.append((tp, True))
                if tp['line'] == lid:
                    live_taps.append((tp, False))
            else:
                # Static Taps sheet
                if tp['line'] == lid:
                    live_taps.append((tp, False))

        month = '%d-%02d' % (yr_f, C.to_local(t0).month)
        bc = bkr_close[lid]
        br = bkr_recl[lid]
        line_close_s = None
        if f['locked']:
            idx = int(np.searchsorted(bc, t0_s + 60.0, side='right'))
            if idx < len(bc) and bc[idx] <= t0_s + 259200.0:
                line_close_s = float(bc[idx])
        recl_close_s = None
        if not f['locked']:
            idx = int(np.searchsorted(br, t0_s + 60.0, side='right')) - 1
            if idx >= 0 and br[idx] >= t0_s - 1.0:
                recl_close_s = float(br[idx])

        for tp, is_abn in live_taps:
            m = int(mem.get((month, tp['name']), 0))
            if not f['locked']:
                secs = (recl_close_s - t0_s) if recl_close_s is not None else 1.0
            else:
                code = code_of.get(tp['name'])
                if is_abn:
                    # Tap is abnormally fed from alt_line (normal line in clearance -> no ALT SRC transfer back!)
                    secs = (line_close_s - t0_s) if line_close_s is not None else 0.0
                else:
                    ac = alt_close.get(code, np.empty(0))
                    idx = int(np.searchsorted(ac, t0_s, side='right'))
                    alt_s = float(ac[idx]) if (idx < len(ac) and ac[idx] <= t0_s + 259200.0) else None
                    cand = [x for x in (alt_s, line_close_s) if x is not None]
                    secs = (min(cand) - t0_s) if cand else 0.0
            if secs > 300:
                f['impact']['sustained'] += m
                f['impact']['minutes'] += m * secs / 60.0
                res_all[lid]['sustained'] += m
                res_all[lid]['minutes'] += m * secs / 60.0
                if yr_f == 2026:
                    res_26[lid]['sustained'] += m
                    res_26[lid]['minutes'] += m * secs / 60.0
            else:
                f['impact']['momentary'] += m
                res_all[lid]['momentary'] += m
                if yr_f == 2026:
                    res_26[lid]['momentary'] += m
    return dict(res_26) if year == 2026 else dict(res_all)


# ------------------------------------------------------------------------------------------------ S4: joint (ESDD, NSDD) contamination

def daily_rain_series(d):
    if '_daily_rain' in d:
        return d['_daily_rain']
    sw = d['stations_wx'].copy()
    sw['day'] = pd.to_datetime(sw['hour_local']).dt.date
    st = sw.groupby(['station', 'day'])['rain_mm'].sum().to_dict()
    apt = d['apt'].copy()
    apt['t'] = pd.to_datetime(apt['valid']).dt.tz_localize('UTC').dt.tz_convert(C.ZONE)
    apt['day'] = apt['t'].dt.date
    apt['mm'] = pd.to_numeric(apt['p01i'].replace('T', '0'), errors='coerce').fillna(0) * 25.4
    ap = apt.groupby('day')['mm'].sum().to_dict()
    d['_daily_rain'] = (st, ap)
    return d['_daily_rain']


def directional_series(d, bearing, opts):
    k = opts['wind_k']
    key = (round(float(bearing), 2), round(float(k), 3), opts['wind_src'])
    cache = d.setdefault('_dir_ser', {})
    if key in cache:
        return cache[key]
    apt = d['apt'].copy()
    apt['t'] = pd.to_datetime(apt['valid']).dt.tz_localize('UTC').dt.tz_convert(C.ZONE)
    apt['day'] = apt['t'].dt.date
    u = pd.to_numeric(apt['sknt'], errors='coerce') / 1.94384 * np.maximum(
        0.0, np.cos(np.radians(pd.to_numeric(apt['drct'], errors='coerce') - bearing)))
    apt['e'] = np.power(u.fillna(0.0), k)
    ap = apt.groupby('day')['e'].mean()
    out = {}
    sw = d['stations_wx'].copy()
    sw['day'] = pd.to_datetime(sw['hour_local']).dt.date
    us = sw['wind_ms'] * np.maximum(0.0, np.cos(np.radians(sw['wind_dir_deg'] - bearing)))
    sw['e'] = np.power(us, k)
    for n in ('PORT ALCORN SUB', 'SHELL RIDGE SUB', 'SEDGE POINT SUB', 'TULE MARSH SUB', 'CANEY BEND SUB', 'MESQUITE FLAT SUB'):
        se = sw[sw['station'] == n].groupby('day')['e'].mean()
        if opts['wind_src'] == 'stations' and len(se):
            both = sorted(set(se.index) & set(ap.index))
            sc = float(se.loc[both].mean() / max(float(ap.loc[both].mean()), 1e-9)) if both else 1.0
            ser = (ap * sc).to_dict()
            ser.update(se.to_dict())
        else:
            ser = ap.to_dict()
        m = float(np.mean(list(ser.values())))
        out[n] = {k_: v / max(m, 1e-9) for k_, v in ser.items()}
    cache[key] = out
    return out


def deposit_series(d, opts):
    """Fit both ESDD (shore-decay + onshore wind + fast exponential rain washout) and NSDD (corridor surface +
    dry inland wind + slow exponential rain washout) directly from esdd_monitoring_2022-2026.xlsx and carry every
    washing section day by day from 2022-01-01 through 2026-10-31."""
    use_wind = opts['deposit'] not in ('const', 'latest', 'history')
    dep_key = (
        use_wind, round(float(opts['wind_k']), 3), round(float(opts['gulf_from']), 2),
        round(float(opts['inland_from']), 2), opts['wind_src'], opts.get('rate'),
        round(float(opts.get('rate_scale', 1.0)), 4), round(float(opts.get('esdd_k_scale', 1.0)), 4),
        round(float(opts.get('nsdd_k_scale', 1.0)), 4), opts.get('salt_bg'), opts.get('dust_bg'),
    )
    dcache = d.setdefault('_dep_cache', {})
    if dep_key in dcache:
        return dcache[dep_key]
    s = d['structures']
    secs = d['wash_sections']
    ws = d['washing']
    st_rain, ap_rain = daily_rain_series(d)
    sites = d['esdd_sites']
    rd = d['esdd'].copy()
    rd['date'] = pd.to_datetime(rd['Date sampled']).dt.date
    near_station = {
        'L01': ['PORT ALCORN SUB'], 'L02': ['PORT ALCORN SUB', 'SHELL RIDGE SUB'],
        'L03': ['SHELL RIDGE SUB', 'SEDGE POINT SUB'], 'L04': ['PORT ALCORN SUB'],
    }
    site_station = {}
    for _, r in sites.iterrows():
        x, y = _xy(float(r['Latitude']), float(r['Longitude']))
        site_station[r['Site']] = min(STATION_XY, key=lambda n: math.hypot(STATION_XY[n][0] - x, STATION_XY[n][1] - y))

    expo_e = directional_series(d, opts['gulf_from'], opts) if use_wind else None
    expo_n = directional_series(d, opts['inland_from'], opts) if use_wind else None

    def rain(stations, day):
        vals = [st_rain.get((n, day)) for n in stations]
        vals = [v for v in vals if v is not None and not pd.isna(v)]
        return float(np.mean(vals)) if vals else float(ap_rain.get(day, 0.0))

    def fac(expo, stations, day):
        if expo is None:
            return 1.0
        return float(np.mean([expo[n].get(day, 1.0) for n in stations]))

    # Build day arrays for fast simulation & nonlinear least-squares fit of (rate, k_rain, bg) on test sites
    day0, day_end = dt.date(2022, 1, 1), dt.date(2026, 10, 31)
    all_days = [day0 + dt.timedelta(days=i) for i in range((day_end - day0).days + 1)]
    day_idx = {dd: i for i, dd in enumerate(all_days)}

    # Precompute rain & wind vectors per test site
    site_meta = {}
    for _, r in sites.iterrows():
        code = r['Site']
        st_n = [site_station[code]]
        r_vec = np.array([rain(st_n, dd) for dd in all_days])
        ef_vec = np.array([fac(expo_e, st_n, dd) for dd in all_days])
        nf_vec = np.array([fac(expo_n, st_n, dd) for dd in all_days])
        g = rd[rd['Site'] == code].sort_values('date')
        obs = [(day_idx[row['date']], float(row['ESDD (mg/cm2)']), float(row['NSDD (mg/cm2)']))
               for _, row in g.iterrows() if row['date'] in day_idx]
        site_meta[code] = dict(shore=float(r['Gulf shore (km)']), surface=str(r['Corridor surface']),
                               r=r_vec, ef=ef_vec, nf=nf_vec, obs=obs)

    # Fit ESDD dynamics: k_esdd, bg_e, and per-site rate r_e from all test-site intervals
    def sim_state(r_vec, f_vec, rate, k_rain, bg, dry_gate=False):
        out = np.empty(len(r_vec))
        v = rate * 50.0
        keep = np.exp(-k_rain * r_vec)
        add = rate * (bg + (1.0 - bg) * f_vec)
        if dry_gate:
            add = np.where(r_vec < 2.0, add, 0.0)
        for i in range(len(r_vec)):
            v = (v + add[i]) * keep[i]
            out[i] = v
        return out

    def fit_esdd():
        def loss(params):
            k_r, bg = params
            err = 0.0
            for code, m in site_meta.items():
                unit = sim_state(m['r'], m['ef'], 1.0, k_r, bg, dry_gate=False)
                idx = np.array([o[0] for o in m['obs']])
                y = np.array([o[1] for o in m['obs']])
                pred_u = np.maximum(unit[idx], 1e-9)
                r_hat = float(np.exp(np.mean(np.log(y / pred_u))))
                err += float(np.sum((np.log(y) - np.log(r_hat * pred_u)) ** 2))
            return err
        res = minimize(loss, [0.05, 0.25 if use_wind else 1.0],
                       bounds=[(0.01, 0.15), (0.0, 1.0) if use_wind else (1.0, 1.0)], method='L-BFGS-B')
        k_r = float(res.x[0]) * opts.get('esdd_k_scale', 1.0)
        bg = float(opts['salt_bg']) if opts.get('salt_bg') is not None else float(res.x[1])
        rates = {}
        for code, m in site_meta.items():
            unit = sim_state(m['r'], m['ef'], 1.0, k_r, bg, dry_gate=False)
            idx = np.array([o[0] for o in m['obs']])
            y = np.array([o[1] for o in m['obs']])
            rates[code] = float(np.exp(np.mean(np.log(y / np.maximum(unit[idx], 1e-9)))))
        return rates, k_r, bg, float(res.fun)

    def fit_nsdd():
        def loss(params):
            k_r, bg = params
            err = 0.0
            for code, m in site_meta.items():
                unit = sim_state(m['r'], m['nf'], 1.0, k_r, bg, dry_gate=True)
                idx = np.array([o[0] for o in m['obs']])
                y = np.array([o[2] for o in m['obs']])
                pred_u = np.maximum(unit[idx], 1e-9)
                r_hat = float(np.exp(np.mean(np.log(y / pred_u))))
                err += float(np.sum((np.log(y) - np.log(r_hat * pred_u)) ** 2))
            return err
        res = minimize(loss, [0.01, 0.30 if use_wind else 1.0],
                       bounds=[(0.001, 0.08), (0.0, 1.0) if use_wind else (1.0, 1.0)], method='L-BFGS-B')
        k_r = float(res.x[0]) * opts.get('nsdd_k_scale', 1.0)
        bg = float(opts['dust_bg']) if opts.get('dust_bg') is not None else float(res.x[1])
        rates = {}
        for code, m in site_meta.items():
            unit = sim_state(m['r'], m['nf'], 1.0, k_r, bg, dry_gate=True)
            idx = np.array([o[0] for o in m['obs']])
            y = np.array([o[2] for o in m['obs']])
            rates[code] = float(np.exp(np.mean(np.log(y / np.maximum(unit[idx], 1e-9)))))
        return rates, k_r, bg, float(res.fun)

    e_rates, k_esdd, bg_e, e_err = fit_esdd()
    n_rates, k_nsdd, bg_n, n_err = fit_nsdd()

    # Map ESDD rate by shore distance
    xs = np.array([site_meta[c]['shore'] for c in e_rates])
    ys = np.array([e_rates[c] for c in e_rates])
    if opts.get('rate') == 'nearest':
        sd_pairs = sorted((site_meta[c]['shore'], e_rates[c]) for c in e_rates)
        e_rate_at = lambda dist: min(sd_pairs, key=lambda p: abs(p[0] - dist))[1]
    elif opts.get('rate') == 'loglin':
        A = np.vstack([np.ones_like(xs), xs]).T
        coef, *_ = np.linalg.lstsq(A, np.log(np.maximum(ys, 1e-6)), rcond=None)
        e_rate_at = lambda dist: float(math.exp(coef[0] + coef[1] * dist))
    elif opts.get('rate') == 'loglin_coast':
        mk = xs <= 5.0
        A = np.vstack([np.ones(int(mk.sum())), xs[mk]]).T
        coef, *_ = np.linalg.lstsq(A, np.log(np.maximum(ys[mk], 1e-6)), rcond=None)
        e_rate_at = lambda dist: float(math.exp(coef[0] + coef[1] * dist))
    else:
        fn = lambda x, a, lam, c: a * np.exp(-x / lam) + c
        try:
            (pa, pl, pc), _ = curve_fit(fn, xs, ys, p0=(float(ys.max()) * 1.5, 1.5, float(ys.min())),
                                        bounds=([0, 0.4, 0], [0.1, 8.0, 0.01]), maxfev=20000)
        except Exception:
            pa, pl, pc = float(ys.max()) * 1.5, 1.5, float(ys.min())
        e_rate_at = lambda dist: max(1e-6, float(fn(dist, pa, pl, pc)))
    if opts.get('rate_scale', 1.0) != 1.0:
        _er = e_rate_at
        e_rate_at = lambda dist: _er(dist) * opts['rate_scale']

    # Map NSDD rate by corridor surface (geometric mean across sites sharing that surface)
    surf_vals = defaultdict(list)
    for code, r_n in n_rates.items():
        surf_vals[site_meta[code]['surface']].append(r_n)
    n_rate_by_surf = {sf: float(np.exp(np.mean(np.log(vs)))) for sf, vs in surf_vals.items()}
    n_rate_default = float(np.exp(np.mean(np.log(list(n_rates.values())))))

    # Carry every washing section day by day (both ESDD and NSDD)
    sec_dep = {}
    for _, r in secs.iterrows():
        lid = 'L%02d' % int(str(r['Line']).split()[1])
        sid = '%s-W%s' % (lid, str(r['Section']).split()[-1])
        sub = s[(s['lid'] == lid) & (s['structure_no'] >= int(r['From structure'])) & (s['structure_no'] <= int(r['To structure']))]
        dist = float(sub['gulf_shore_km'].mean())
        surf = str(r['Corridor surface']) if 'Corridor surface' in r and pd.notna(r['Corridor surface']) else str(sub['corridor_surface'].mode().iloc[0])
        er = e_rate_at(dist)
        nr = n_rate_by_surf.get(surf, n_rate_default)
        washes = set(pd.to_datetime(ws[(ws['Line'] == r['Line']) & (ws['Section'] == r['Section'])]['Date']).dt.date)
        st_l = near_station[lid]
        r_vec = np.array([rain(st_l, dd) for dd in all_days])
        ef_vec = np.array([fac(expo_e, st_l, dd) for dd in all_days])
        nf_vec = np.array([fac(expo_n, st_l, dd) for dd in all_days])
        ke = np.exp(-k_esdd * r_vec)
        kn = np.exp(-k_nsdd * r_vec)
        ae = er * (bg_e + (1.0 - bg_e) * ef_vec)
        an = np.where(r_vec < 2.0, nr * (bg_n + (1.0 - bg_n) * nf_vec), 0.0)
        esdd_v, nsdd_v = er * 45.0, nr * 60.0
        es_ser, ns_ser = {}, {}
        for i, dd in enumerate(all_days):
            esdd_v = (esdd_v + ae[i]) * ke[i]
            nsdd_v = (nsdd_v + an[i]) * kn[i]
            if dd in washes:
                esdd_v, nsdd_v = 0.003, 0.015
            es_ser[dd] = esdd_v
            ns_ser[dd] = nsdd_v
        sec_dep[sid] = dict(line=lid, s0=int(r['From structure']), s1=int(r['To structure']),
                            dist=dist, surface=surf, esdd=es_ser, nsdd=ns_ser, washes=sorted(washes))
    res_dep = dict(sections=sec_dep, e_rates=e_rates, n_rates=n_rates, n_rate_by_surf=n_rate_by_surf,
                   k_esdd=k_esdd, k_nsdd=k_nsdd, bg_e=bg_e, bg_n=bg_n, day_end=day_end,
                   e_err=e_err, n_err=n_err, all_days=all_days)
    dcache[dep_key] = res_dep
    return res_dep


def section_of(dep, f):
    for sid, sd in dep['sections'].items():
        if sd['line'] == f['line'] and sd['s0'] <= f['structure'] <= sd['s1']:
            return sid
    return None


def _fog_days_by_line(d):
    """Identify local days on which coastal fog occurred (for empirical 2D logistic/Poisson frontier fit)."""
    if '_fog_days' in d:
        return d['_fog_days']
    sw = d['stations_wx'].copy()
    sw['dt'] = pd.to_datetime(sw['hour_local'])
    sw['day'] = sw['dt'].dt.date
    sw['hr'] = sw['dt'].dt.hour
    fog_st = sw[(sw['station'].isin(['PORT ALCORN SUB', 'SHELL RIDGE SUB', 'SEDGE POINT SUB'])) &
                ((sw['hr'] >= 22) | (sw['hr'] <= 9)) & ((sw['air_temp_c'] - sw['dewpoint_c']) <= 0.5)]
    fog_days = set(fog_st['day'])
    apt = d['apt'].copy()
    apt['t'] = pd.to_datetime(apt['valid']).dt.tz_localize('UTC').dt.tz_convert(C.ZONE)
    apt_fg = apt[apt['wxcodes'].astype(str).str.contains('FG', na=False)]
    fog_days |= set(apt_fg['t'].dt.date)
    d['_fog_days'] = sorted(fog_days)
    return d['_fog_days']


def fit_joint_beta(d, faults, dep, opts):
    """Empirically estimate the IEC 60815 NSDD exponent beta in C_eff = ESDD * (NSDD/0.20)^beta from all
    section-fog-nights (2022-2026) via 2D logistic (or probit/Poisson) regression on (log ESDD, log NSDD)."""
    if opts.get('beta_override') is not None:
        return float(opts['beta_override'])
    mode = opts.get('deposit', 'joint')
    if mode in ('esdd_wind', 'const', 'latest', 'history'):
        return 0.0
    if mode == 'over_nsdd':
        return 1.50
    secs = dep['sections']
    flashes = set()
    for f in faults:
        if f['cause'] == 'fog' and f['structure'] is not None:
            sid = section_of(dep, f)
            if sid is not None:
                flashes.add((sid, C.to_local(f['t']).date()))
    bmodel = opts.get('beta_model', 'logistic')
    bkey = (id(dep), bmodel, frozenset(flashes))
    bcache = d.setdefault('_beta_cache', {})
    if bkey in bcache:
        return bcache[bkey]
    fog_days = sorted(set(_fog_days_by_line(d)) | {day for _, day in flashes})
    X_e, X_n, Y = [], [], []
    for sid, sd in secs.items():
        for dd in fog_days:
            if dd not in sd['esdd']:
                continue
            X_e.append(math.log(max(sd['esdd'][dd], 1e-4)))
            X_n.append(math.log(max(sd['nsdd'][dd], 5e-3)))
            Y.append(1.0 if (sid, dd) in flashes else 0.0)
    xe, xn, y = np.array(X_e), np.array(X_n), np.array(Y)
    if y.sum() < 5:
        return 0.45

    def nll(p):
        a0, a1, a2 = p
        eta = np.clip(a0 + a1 * xe + a2 * xn, -30.0, 30.0)
        if bmodel == 'poisson':
            return float(np.sum(np.exp(eta) - y * eta))
        return float(np.sum(np.logaddexp(0.0, eta) - y * eta))

    res = minimize(nll, [5.0, 3.0, 1.5], bounds=[(-50, 50), (0.2, 40.0), (0.0, 40.0)], method='L-BFGS-B')
    a1, a2 = float(res.x[1]), float(res.x[2])
    val = max(0.0, min(1.5, a2 / max(a1, 1e-6)))
    bcache[bkey] = val
    return val


def deposit_model(d, faults, dep, opts):
    secs = dep['sections']
    rd = d['esdd'].copy()
    rd['date'] = pd.to_datetime(rd['Date sampled']).dt.date
    sites = d['esdd_sites']
    s = d['structures']
    day_end = dep['day_end']
    beta = fit_joint_beta(d, faults, dep, opts)
    NREF = 0.20

    # Latest test-site readings (for direct / latest / one_fact shortcuts)
    latest_e, latest_n = {}, {}
    for site, g_ in rd.groupby('Site'):
        g_ = g_.sort_values('date')
        latest_e[site] = float(g_.iloc[-1]['ESDD (mg/cm2)'])
        latest_n[site] = float(g_.iloc[-1]['NSDD (mg/cm2)'])
    site_xy = {r['Site']: _xy(float(r['Latitude']), float(r['Longitude'])) for _, r in sites.iterrows()}

    def ceff_of(e, n):
        return float(e * ((max(n, 0.005) / NREF) ** beta))

    at_flash = []
    flashed = defaultdict(int)
    for f in faults:
        if f['cause'] != 'fog' or f['structure'] is None:
            continue
        sid = section_of(dep, f)
        if sid is not None:
            dd = C.to_local(f['t']).date()
            e_v = secs[sid]['esdd'][dd]
            n_v = secs[sid]['nsdd'][dd]
            at_flash.append(ceff_of(e_v, n_v))
            flashed[sid] += 1
    if not at_flash:
        level = None
    elif opts.get('level') == 'min':
        level = float(np.min(at_flash))
    else:
        level = float(np.percentile(at_flash, opts['level_q']))
    if level is not None and opts.get('level_scale', 1.0) != 1.0:
        level *= opts['level_scale']

    out = {}
    for sid, sd in secs.items():
        sub = s[(s['lid'] == sd['line']) & (s['structure_no'] >= sd['s0']) & (s['structure_no'] <= sd['s1'])]
        cx, cy = _xy(float(sub['latitude'].mean()), float(sub['longitude'].mean()))
        near_site = min(site_xy, key=lambda k: math.hypot(site_xy[k][0] - cx, site_xy[k][1] - cy))
        last_wash = max([w for w in sd['washes'] if w <= day_end], default=None)
        e31, n31 = sd['esdd'][day_end], sd['nsdd'][day_end]
        if opts['deposit'] == 'one_fact':
            # One-fact shortcut: multiply modeled ESDD by the nearest never-washed test site's raw latest NSDD
            c31 = e31 * ((max(latest_n[near_site], 0.005) / NREF) ** beta)
            due = level is not None and c31 >= level
        elif opts['deposit'] == 'history':
            c31 = ceff_of(e31, n31)
            due = flashed[sid] > 0
        elif opts['deposit'] == 'latest':
            rd_s = rd[rd['Site'] == near_site].sort_values('date')
            washed_after = last_wash is not None and last_wash >= rd_s.iloc[-1]['date']
            c31 = 0.003 if washed_after else latest_e[near_site]
            due = level is not None and (not washed_after) and latest_e[near_site] >= level
        else:
            c31 = ceff_of(e31, n31)
            due = level is not None and c31 >= level
        out[sid] = dict(
            esdd=e31, nsdd=n31, ceff=c31, deposit=c31, ratio=(c31 / level if level else 0.0),
            dist=sd['dist'], surface=sd['surface'], due=due, flashed=flashed[sid],
            test_site=near_site, test_latest_esdd=latest_e[near_site], test_latest_nsdd=latest_n[near_site],
            last_wash=last_wash,
        )
    return dict(sections=out, level=level, beta=beta, k_esdd=dep['k_esdd'], k_nsdd=dep['k_nsdd'],
                bg_e=dep['bg_e'], bg_n=dep['bg_n'], at_flash=at_flash, series=secs)


# ------------------------------------------------------------------------------------------------ RP-04 Rev 5 Priority 1 programme

def priority_programme(d, rls, deps, opts):
    """Allocate RP-04 Rev 5's fixed 36-crew-day winter/spring programme:
      1. Schedule all due coastal washing sections first (1 crew-day each).
      2. Rank qualifying unfixed repeat locations by historical (2022-2026) conformed member-minutes per crew-day
         descending (tie-break: fault count desc, line asc, structure asc).
      3. Greedily allocate remaining crew-days; skip items whose allowance exceeds remaining days -> Priority 2 backlog."""
    budget = opts.get('budget_days') or d['budget_days']
    due_washes = sorted(sid for sid, v in deps['sections'].items() if v['due'])
    wash_days = len(due_washes) * C.CREW_DAYS['wash']
    rem = max(0, budget - wash_days)

    open_rls = [rl for rl in rls if not rl['fixed']]
    for rl in open_rls:
        cd = C.CREW_DAYS[rl['cause']]
        mm = sum(float((f.get('impact') or {}).get('minutes', 0.0)) for f in rl['faults'])
        sust = sum(int((f.get('impact') or {}).get('sustained', 0)) for f in rl['faults'])
        rl['crew_days'] = cd
        rl['hist_mm'] = mm
        rl['hist_sust'] = sust
        rl['mm_per_day'] = mm / cd

    ranked = sorted(open_rls, key=lambda r: (-round(r['mm_per_day'], 2), -r['n'], int(r['line'][1:]), r['structure']))
    funded, deferred = [], []
    used_rep = 0
    for rl in ranked:
        if rl['crew_days'] <= rem:
            rl['priority'] = 'P1'
            funded.append(rl)
            rem -= rl['crew_days']
            used_rep += rl['crew_days']
        else:
            rl['priority'] = 'P2'
            deferred.append(rl)
    cutoff = funded[-1]['mm_per_day'] if funded else 0.0
    first_def = deferred[0]['mm_per_day'] if deferred else 0.0
    return dict(
        budget=budget, due_washes=due_washes, wash_days=wash_days,
        repeat_budget=budget - wash_days, repeat_days_used=used_rep, unused_days=rem,
        funded=funded, deferred=deferred, ranked=ranked,
        cutoff_mm_per_day=cutoff, first_deferred_mm_per_day=first_def,
    )


def run(target, opts=None, d=None):
    opts = dict(GOLD, **(opts or {}))
    if d is None:
        d = load(target)
    d['src_scale'] = opts.get('src_scale', 1.0)
    faults = build_faults(d)
    locate(d, faults, opts)
    classify(d, faults, opts)
    settle_clusters(faults, opts)
    contacts = settle_contacts(d, faults, opts)
    settle_replaced_strings(d, faults, opts)
    dep = deposit_series(d, opts)
    deps = deposit_model(d, faults, dep, opts)
    # Compute full 2022-2026 member impact first (attaching f['impact'] to every fault for Priority 1 ranking)
    impact_all = member_impact(d, faults, opts, year=None)
    impact_26 = defaultdict(lambda: dict(sustained=0, minutes=0.0, momentary=0))
    for f in faults:
        if C.to_local(f['t']).year == 2026:
            imp = f.get('impact') or {}
            impact_26[f['line']]['sustained'] += imp.get('sustained', 0)
            impact_26[f['line']]['minutes'] += imp.get('minutes', 0.0)
            impact_26[f['line']]['momentary'] += imp.get('momentary', 0)
    rls = repeat_locations(d, faults, opts['win_km'])
    for rl in rls:
        rl['fixed'] = fixed_since(d, rl)
    prog = priority_programme(d, rls, deps, opts)
    return dict(
        d=d, faults=faults, repeat=rls,
        impact=dict(impact_26), impact_all=impact_all,
        deposits=deps, contacts=contacts, programme=prog,
    )
