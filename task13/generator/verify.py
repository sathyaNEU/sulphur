"""An independent read of task13's bundle: unzips target.zip into a fresh folder and recomputes the graded figures by
its own code path (no generator module, no world), then compares them with generator/figures.json.

    python3 task13/generator/verify.py      # exit 1 on any disagreement
"""
import json
import math
import os
import re
import sys
import tempfile
import zipfile
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CT = ZoneInfo('America/Chicago')
CSTZ = 'Etc/GMT+6'


def read(folder, name, **kw):
    return pd.read_csv(os.path.join(folder, name), **kw)


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    tmp = tempfile.mkdtemp(prefix='t13verify')
    zipfile.ZipFile(os.path.join(TASK, 'target.zip')).extractall(tmp)
    out = []
    ev = read(tmp, 'scada_device_events_2022-2026.csv')
    ev['t'] = pd.to_datetime(ev['Time (CST)']).dt.tz_localize(CSTZ).dt.tz_convert('UTC')
    reg = pd.read_excel(os.path.join(tmp, 'da_device_register_2026.xlsx'), sheet_name='Devices', header=3)
    loops = pd.read_excel(os.path.join(tmp, 'flisr_loop_configuration_2026.xlsx'), sheet_name='Loops', header=3)
    oms = read(tmp, 'oms_outage_events_2022-2026.csv')
    oms['start'] = pd.to_datetime(oms['Outage Start'], format='%m/%d/%Y %H:%M').dt.tz_localize(CT, ambiguous=True, nonexistent='shift_forward').dt.tz_convert('UTC')
    feeder_of = dict(zip(reg['Asset No'], reg['Feeder']))
    tie_loop = dict(zip(loops['Tie switch'], loops['Loop']))
    loop_feeders = {}
    for _, r in loops.iterrows():
        loop_feeders[r['Loop']] = (r['Feeder A'], r['Feeder B'])
    in_service = dict(zip(loops['Loop'], pd.to_datetime(loops['FLISR in service'])))
    # ---- R1: each ADMS tie close, timed from the first trip of the lockout before it, customers from the
    # outage record's automatic steps (the configuration's sections where the outage record has none)
    secs = pd.read_excel(os.path.join(tmp, 'flisr_loop_configuration_2026.xlsx'), sheet_name='Sections', header=0)
    secs = secs[pd.to_numeric(secs['Section'], errors='coerce').notna()]
    cust = {(r['Feeder'], int(r['Section'])): int(r['Customers (Sep 2026)']) for _, r in secs.iterrows()}
    lock = ev[ev['Event'] == 'LOCKOUT'].copy()
    lock['feeder'] = lock['Device'].map(lambda d: d[:-3] if d.endswith(' CB') else feeder_of.get(d))
    trips = ev[ev['Event'] == 'TRIP']
    closes = ev[(ev['Event'] == 'CLOSE') & (ev['Source'] == 'ADMS') & ev['Device'].str.startswith('TSW')]
    opens = ev[(ev['Event'] == 'OPEN') & (ev['Source'] == 'ADMS')]
    auto = oms[oms['Step Type'] == 'Automatic']
    by_year = {}
    for _, c in closes.iterrows():
        lid = tie_loop[c['Device']]
        fa, fb = loop_feeders[lid]
        cand = lock[lock['feeder'].isin([fa, fb]) & (lock['t'] <= c['t']) & (lock['t'] >= c['t'] - pd.Timedelta(minutes=60))]
        if not len(cand):
            continue
        lo = cand.iloc[-1]
        if lo['t'].tz_convert(CT).tz_localize(None) < in_service[lid]:
            continue
        tr = trips[(trips['Device'] == lo['Device']) & (trips['t'] <= lo['t']) & (trips['t'] >= lo['t'] - pd.Timedelta(minutes=3))]
        first = tr['t'].min()
        f = lo['feeder']
        b = fb if f == fa else fa
        back = trips[(trips['Device'].map(feeder_of) == b) & (trips['t'] >= c['t']) & (trips['t'] <= c['t'] + pd.Timedelta(seconds=3))]
        if len(back):
            continue
        if (c['t'] - first).total_seconds() >= 300:
            continue
        o = auto[(auto['Interrupting Device'] == lo['Device']) & ((auto['start'] - first).abs() < pd.Timedelta(minutes=40))]
        if len(o):
            n = int(o['Customers Restored'].sum())
        else:
            op = opens[(opens['t'] >= lo['t']) & (opens['t'] <= c['t']) & (opens['Device'].map(feeder_of) == f)]
            k = max(int(str(reg.loc[reg['Asset No'] == d, 'Position'].iloc[0])[-1]) for d in op['Device'])
            n = sum(cust[(f, s)] for s in ([2, 3] if k == 1 else [3]))
        y = first.tz_convert(CT).year
        by_year[y] = by_year.get(y, 0) + n
    for y in range(2022, 2027):
        g = F['r1_by_year'][str(y)]
        v = by_year.get(y, 0)
        out.append(('R1 %d restorations within five minutes' % y, abs(v - g) <= 0.015 * g, '%d against %d' % (v, g)))
    # ---- the dashboard's 2026 figure
    db = pd.read_excel(os.path.join(tmp, 'adms_flisr_kpi_dashboard_2022-2026.xlsx'), header=None)
    hdr = db.index[db[0] == 'Month'][0]
    db.columns = list(db.iloc[hdr])
    db = db.iloc[hdr + 1:]
    d26 = int(db[db['Month'].astype(str).str.startswith('2026')]['CI saved'].sum())
    out.append(('R2 the dashboard\'s 2026 figure', d26 == F['dashboard_2026'], '%d' % d26))
    # ---- R2: receiving trips with no cause found during a transfer, and their first steps
    o26 = oms[(oms['Cause'] == 'Unknown - no cause found') & oms['Interrupting Device'].str.startswith('RCL', na=False)]
    o26 = o26[o26['start'].dt.tz_convert(CT).dt.year == 2026]
    own = 0
    undone = 0
    for oid, g in o26.groupby('Outage ID'):
        dev = g['Interrupting Device'].iloc[0]
        t = g['start'].iloc[0]
        f = feeder_of[dev]
        lid = [l for l, ff in loop_feeders.items() if f in ff][0]
        tie = [k for k, v in tie_loop.items() if v == lid][0]
        tc = closes[(closes['Device'] == tie) & (closes['t'] <= t + pd.Timedelta(minutes=1)) & (closes['t'] >= t - pd.Timedelta(hours=14))]
        if not len(tc):
            continue
        g = g.sort_values('Step')
        own += int(g['Customers Restored'].iloc[0])
        undone += int(g['Customers Interrupted'].iloc[0]) - int(g['Customers Restored'].iloc[0])
    out.append(('R2 receiving feeders\' own customers 2026', abs(own - F['bridge_2026']['recv_trips_own']) <= 0.02 * F['bridge_2026']['recv_trips_own'] + 1,
                '%d against %d' % (own, F['bridge_2026']['recv_trips_own'])))
    out.append(('R2 restorations undone 2026', abs(undone - F['bridge_2026']['reinterrupted']) <= 0.03 * F['bridge_2026']['reinterrupted'] + 1,
                '%d against %d' % (undone, F['bridge_2026']['reinterrupted'])))
    net = d26 - F['bridge_2026']['after_five'] + F['bridge_2026']['lost'] - own - undone - F['bridge_2026']['closes_own']
    out.append(('R2 the net', abs(net - F['net_2026']) <= 0.025 * F['net_2026'], '%d against %d' % (net, F['net_2026'])))
    # ---- R3: each current battery's ln R regressed on (25 - T) and age, its own coefficients, at -27 C on 28 Feb 2027
    wx = read(tmp, 'kmkt_hourly_weather_2022-2026.csv', na_values=['M'])
    wx['h'] = (pd.to_datetime(wx['valid']).dt.tz_localize('UTC') + pd.Timedelta(minutes=7)).dt.floor('h')
    temp = wx.set_index('h')['tmpf'].sub(32).mul(5 / 9)
    temp = temp[~temp.index.duplicated()].sort_index()
    temp = temp.reindex(pd.date_range(temp.index.min(), temp.index.max(), freq='h')).interpolate(limit=3)
    bt = ev[ev['Event'] == 'BATTERY TEST'].copy()
    vv = bt['Value'].str.extract(r'V_REST=([\d.]+) V_LOAD=([\d.]+)').astype(float)
    bt['R'] = (vv[0] - vv[1]) / 5.0
    bt['vr'] = vv[0]
    bt['T'] = temp.reindex(bt['t'].dt.floor('h')).values
    named = []
    vr_fit = np.polyfit(bt['T'].dropna(), bt.loc[bt['T'].notna(), 'vr'], 1)
    v_d = np.polyval(vr_fit, -27.0)
    for _, r in reg[reg['Asset No'].str.startswith('RCL')].iterrows():
        inst = pd.Timestamp(r['Battery installed']).tz_localize('UTC')
        g = bt[(bt['Device'] == r['Asset No']) & (bt['t'] >= inst) & bt['T'].notna() & (bt['R'] > 0)]
        if len(g) < 10:
            continue
        age = (g['t'] - inst).dt.days / 365.25
        Z = np.column_stack([np.ones(len(g)), 25 - g['T'], age])
        coef = np.linalg.lstsq(Z, np.log(g['R']), rcond=None)[0]
        a_end = (pd.Timestamp('2027-02-28', tz='UTC') - inst).days / 365.25
        R = math.exp(coef[0] + coef[1] * 52 + max(coef[2], 0) * a_end)
        if v_d - 30 * R < 21.2:
            named.append(r['Asset No'])
    core = set(F['rebattery_core'])
    margin = set(F['rebattery_margin'])
    ok = core <= set(named) and set(named) <= core | margin
    out.append(('R3 the battery set (own regression)', ok, '%d named; outside core and margin: %s; core missed: %s' %
                (len(named), sorted(set(named) - core - margin), sorted(core - set(named)))))
    for label, ok, d in out:
        print('%s  %-50s %s' % ('PASS' if ok else 'FAIL', label, d))
    bad = [x for x in out if not x[1]]
    print('%d checks, %d FAIL' % (len(out), len(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
