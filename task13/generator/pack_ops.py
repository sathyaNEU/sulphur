"""The operations records: the SCADA sequence of events, the control room's 69 kV log, the outage system's database,
members by feeder and month, the line patrols, and the work management system's maintenance and vegetation orders."""
import csv
import datetime as dt
import math
import sqlite3

import numpy as np

import common as C
import network as N
import weather as W

TAP_CODE = {}


def tap_code(name):
    if name not in TAP_CODE:
        parts = name.replace('-', ' ').split()
        code = (parts[0][:2] + (parts[1][0] if len(parts) > 1 else parts[0][2])).upper()
        while code in TAP_CODE.values():
            code = code[:2] + chr(ord(code[2]) + 1)
        TAP_CODE[name] = code
    return TAP_CODE[name]


def feeders(net, rng=None):
    rng = rng or np.random.default_rng(C.SEED + 33)
    out = []
    for tp in net['taps']:
        code = tap_code(tp['name'])
        shares = rng.dirichlet(np.ones(tp['feeders']) * 4.0)
        for i, s in enumerate(shares):
            out.append(dict(feeder='%s%d' % (code, i + 1), tap=tp['name'], code=code, share=float(s)))
    return out


def feeder_members(net, fd, tp, t):
    from ops import members_at
    return int(round(members_at(net, tp, t) * fd['share']))


# ------------------------------------------------------------------------------------------------ SCADA SOE

def soe_rows(w, fds):
    net, wx = w['net'], w['wx']
    rng = np.random.default_rng(C.EV_SEED + 808)
    rows = []
    taps = {tp['name']: tp for tp in net['taps']}
    for f in w['faults']:
        for (t, st, dev, state) in f['ops']['ops']:
            if st == 'SW':
                name_key = [n for n in taps if dev.startswith(n.upper()[:10].replace(' ', ''))]
                tp = taps[name_key[0]] if name_key else None
                if tp is None or not tp['moab']:
                    continue
                rows.append((t, tap_code(tp['name']), '%s 69KV MOAB %s' % (tap_code(tp['name']), dev.split()[-1]), state, 'SUPV'))
            elif st == 'XFER':
                name_key = [n for n in taps if dev.startswith(n.upper()[:10].replace(' ', ''))]
                tp = taps[name_key[0]]
                how = 'AUTO XFER' if tp['backup'] == 'auto' else 'SUPV'
                rows.append((t, tap_code(tp['name']), '%s 69KV ALT SRC %s' % (tap_code(tp['name']), 'L%d' % int(tp['alt'][1:])), 'CLOSE', how))
            else:
                cause = {'TRIP': 'PROT', 'LOCKOUT': '79 LO', 'CLOSE': '79 RECL'}[state]
                if state == 'CLOSE' and (t - f['t']).total_seconds() > 60:
                    cause = 'SUPV'
                rows.append((t, st, '%s 69KV BKR %s' % (st, dev.split('-')[1]), 'OPEN' if state == 'TRIP' else state, cause))
    # planned outages and relay trip tests on the 69 kV lines
    for lid, line in net['lines'].items():
        for yr in range(2022, 2027):
            for _ in range(int(rng.integers(0, 3))):
                d = dt.datetime(yr, int(rng.integers(1, 11)), int(rng.integers(1, 28)), int(rng.integers(13, 17)),
                                int(rng.integers(0, 60)), int(rng.integers(0, 60)), tzinfo=C.UTC)
                dur = dt.timedelta(hours=float(rng.uniform(2, 9)))
                for end, pre in (('a', 52), ('b', 62)):
                    rows.append((d + dt.timedelta(seconds=float(rng.uniform(0, 40))), line[end],
                                 '%s 69KV BKR B%d%02d' % (line[end], pre, int(lid[1:])), 'OPEN', 'SUPV'))
                    rows.append((d + dur + dt.timedelta(seconds=float(rng.uniform(0, 40))), line[end],
                                 '%s 69KV BKR B%d%02d' % (line[end], pre, int(lid[1:])), 'CLOSE', 'SUPV'))
            if rng.random() < 0.8:
                d = dt.datetime(yr, int(rng.integers(1, 11)), int(rng.integers(1, 28)), int(rng.integers(14, 20)),
                                int(rng.integers(0, 60)), int(rng.integers(0, 60)), tzinfo=C.UTC)
                end = 'a' if rng.random() < 0.5 else 'b'
                pre = 52 if end == 'a' else 62
                rows.append((d, line[end], '%s 69KV BKR B%d%02d' % (line[end], pre, int(lid[1:])), 'OPEN', 'PROT'))
                rows.append((d + dt.timedelta(seconds=float(rng.uniform(40, 300))), line[end],
                             '%s 69KV BKR B%d%02d' % (line[end], pre, int(lid[1:])), 'CLOSE', 'SUPV'))
    # distribution feeder breakers and capacitor banks at the substations
    t_start, t_end = C.REC0, C.T_END
    span_h = int((t_end - t_start).total_seconds() // 3600)
    for fd in fds:
        n = int(rng.poisson(9 * 4.8))
        for _ in range(n):
            t = t_start + dt.timedelta(hours=float(rng.uniform(0, span_h)))
            rows.append((t, fd['code'], '%s 12KV FDR %s BKR' % (fd['code'], fd['feeder']), 'OPEN', 'PROT'))
            if rng.random() < 0.8:
                rows.append((t + dt.timedelta(seconds=float(rng.choice([2.0, 15.0, 30.0]))), fd['code'],
                             '%s 12KV FDR %s BKR' % (fd['code'], fd['feeder']), 'CLOSE', '79 RECL'))
            else:
                rows.append((t + dt.timedelta(seconds=32.1), fd['code'], '%s 12KV FDR %s BKR' % (fd['code'], fd['feeder']), 'LOCKOUT', '79 LO'))
                rows.append((t + dt.timedelta(minutes=float(rng.uniform(25, 180))), fd['code'],
                             '%s 12KV FDR %s BKR' % (fd['code'], fd['feeder']), 'CLOSE', 'SUPV'))
    hour, month = wx['hour'], wx['month']
    for tp in net['taps']:
        code = tap_code(tp['name'])
        for h in range(C.hour_index(C.REC0), C.NH, 24):
            if month[h] in (5, 6, 7, 8, 9) and rng.random() < 0.85:
                t_on = C.ts_of(h + 11 - (hour[h] - 0), float(rng.uniform(0, 3600)))
                rows.append((t_on, code, '%s 12KV CAP BANK 1' % code, 'CLOSE', 'AUTO VAR'))
                rows.append((t_on + dt.timedelta(hours=float(rng.uniform(6, 10))), code, '%s 12KV CAP BANK 1' % code, 'OPEN', 'AUTO VAR'))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    return rows


def write_soe(rows, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['time_utc', 'rtu', 'point', 'state', 'cause'])
        for t, rtu, point, state, cause in rows:
            wr.writerow([t.strftime('%Y-%m-%d %H:%M:%S.') + '%03d' % (t.microsecond // 1000), rtu, point, state, cause])
    return len(rows)


# ------------------------------------------------------------------------------------------------ control room log

def operator_cause(w, f, rng):
    """the code the operator typed: from what the weather and the radar looked like, and the patrol if one went"""
    wx = w['wx']
    h = f['h']
    # thunderstorms within 25 km of the line in the hour
    net = w['net']
    line = net['lines'][f['line']]
    mid = line['structures'][len(line['structures']) // 2]
    lt = C.to_local(f['t'])
    near_ltg = w['strokes_by_hour'].get(h, [])
    if any(math.hypot(x - mid['x'], y - mid['y']) < 25.0 for x, y in near_ltg):
        return 'LTG'
    apt = wx['series']['APT']
    if f['permanent'] and f['cause'] in ('vehicle', 'growin', 'fallin', 'insulator', 'hardware'):
        return {'vehicle': 'VEH', 'growin': 'TREE', 'fallin': 'TREE', 'insulator': 'EQUIP', 'hardware': 'EQUIP'}[f['cause']]
    if (lt.hour >= 21 or lt.hour <= 7) and apt['temp'][h] - apt['dew'][h] < 0.6:
        return 'CONTAM'
    gust = max(wx['series']['APT']['gust'][h], wx['series']['INA']['gust'][h])
    if gust >= 13.0:
        return 'WIND'
    if lt.month in (5, 6, 7, 8, 9, 10) and 12 <= lt.hour <= 19 and rng.random() < 0.35:
        return 'TREE'
    return 'UNK'


def crlog_rows(w):
    net = w['net']
    rng = np.random.default_rng(C.EV_SEED + 909)
    rows = []
    ops_names = ['D. Hart', 'R. Vance', 'K. Ochoa', 'M. Pruitt', 'L. Sorensen']
    taps = {tp['name']: tp for tp in net['taps']}
    for f in w['faults']:
        if rng.random() < 0.025:
            continue                                   # not written up
        lt = C.to_local(f['t'])
        night = lt.hour >= 22 or lt.hour <= 5
        delay = dt.timedelta(minutes=float(rng.uniform(0, 14 if night else 4)))
        tl = lt + delay
        line = net['lines'][f['line']]
        cause = operator_cause(w, f, rng)
        members = sum(i['members'] for i in f['ops']['impact']) if f['permanent'] else 0
        ev = 'Line trip, reclosed' if not f['permanent'] else 'Line lockout'
        rem = ''
        if cause == 'LTG':
            rem = 'storms in the area'
        elif cause == 'CONTAM':
            rem = 'fog at the airport'
        elif cause == 'WIND':
            rem = 'gusty'
        if f['permanent']:
            rem = (rem + '; ' if rem else '') + 'patrol dispatched'
        op = ops_names[int(rng.integers(0, len(ops_names)))]
        rows.append(dict(date=tl.date(), time=tl.strftime('%H:%M'), line='Line %d' % int(f['line'][1:]),
                         event=ev, cause=cause, remarks=rem, members=members if members else '', operator=op, ref=f['id']))
        if rng.random() < 0.03:
            rows.append(dict(rows[-1], time=(tl + dt.timedelta(minutes=float(rng.uniform(1, 9)))).strftime('%H:%M'),
                             operator=ops_names[int(rng.integers(0, len(ops_names)))], remarks=rem + ' (shift change)'))
        if f['permanent']:
            ts = C.to_local(f['ops']['t_sect']) + dt.timedelta(minutes=float(rng.uniform(0, 6)))
            moab = any(taps[i['tap']]['moab'] for i in f['ops']['impact']) or not f['ops']['impact']
            rows.append(dict(date=ts.date(), time=ts.strftime('%H:%M'), line='Line %d' % int(f['line'][1:]),
                             event='Faulted section isolated, line restored' + ('' if moab else ' (crew opened switches)'),
                             cause='', remarks='', members='', operator=op, ref=f['id']))
            tr = C.to_local(f['ops']['t_rep']) + dt.timedelta(minutes=float(rng.uniform(0, 20)))
            rows.append(dict(date=tr.date(), time=tr.strftime('%H:%M'), line='Line %d' % int(f['line'][1:]),
                             event='Repairs complete, line returned to normal', cause='', remarks='', members='', operator=op, ref=f['id']))
    rows.sort(key=lambda r: (r['date'], r['time']))
    return rows


# ------------------------------------------------------------------------------------------------ outage system

CAUSES = [('ANIMAL', 'Animal contact'), ('VEG', 'Vegetation'), ('EQUIP', 'Equipment failure'), ('WEATHER', 'Weather'),
          ('PUBLIC', 'Public (vehicle, dig-in)'), ('UNK', 'Unknown'), ('LOS', 'Loss of supply (69 kV or above)'),
          ('PLANNED', 'Planned (notified)')]


def oms_build(w, fds, path):
    net = w['net']
    rng = np.random.default_rng(C.EV_SEED + 1010)
    taps = {tp['name']: tp for tp in net['taps']}
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('CREATE TABLE feeder (feeder_id TEXT PRIMARY KEY, substation TEXT, sub_code TEXT)')
    cur.execute('CREATE TABLE cause_code (code TEXT PRIMARY KEY, description TEXT)')
    cur.execute('CREATE TABLE outage (outage_id INTEGER PRIMARY KEY, feeder_id TEXT, start_time TEXT, restore_time TEXT, '
                'cause_code TEXT, device TEXT, members_out INTEGER, remarks TEXT)')
    cur.execute('CREATE TABLE outage_step (outage_id INTEGER, step_no INTEGER, step_time TEXT, members_restored INTEGER)')
    for fd in fds:
        cur.execute('INSERT INTO feeder VALUES (?,?,?)', (fd['feeder'], fd['tap'], fd['code']))
    for c, d in CAUSES:
        cur.execute('INSERT INTO cause_code VALUES (?,?)', (c, d))
    events = []
    # loss-of-supply outages on the feeders a 69 kV lockout put out for longer than the alarm delay
    for f in w['faults']:
        if not f['permanent']:
            continue
        for imp in f['ops']['impact']:
            if imp['seconds'] < 60:
                continue
            tp = taps[imp['tap']]
            for fd in [x for x in fds if x['tap'] == imp['tap']]:
                m = feeder_members(net, fd, tp, f['t'])
                start = C.to_local(f['t']) + dt.timedelta(seconds=float(rng.uniform(25, 110)))
                restore = C.to_local(f['t']) + dt.timedelta(seconds=imp['seconds']) + dt.timedelta(minutes=float(rng.uniform(3, 38)))
                events.append(dict(feeder=fd['feeder'], start=start, restore=restore, cause='LOS', device='SUB SOURCE',
                                   members=m, remarks='Line %d lockout' % int(f['line'][1:]), steps=[]))
    # the distribution system's own outages
    t0 = C.to_local(C.REC0)
    span_h = int((C.T_END - C.REC0).total_seconds() // 3600)
    for fd in fds:
        tp = taps[fd['tap']]
        n = int(rng.poisson(34.0 * 4.83))
        for _ in range(n):
            start = t0 + dt.timedelta(hours=float(rng.uniform(0, span_h)))
            cause = str(rng.choice(['ANIMAL', 'VEG', 'EQUIP', 'WEATHER', 'PUBLIC', 'UNK', 'PLANNED'],
                                   p=[0.17, 0.21, 0.24, 0.12, 0.06, 0.14, 0.06]))
            dev = str(rng.choice(['FUSE', 'RECLOSER', 'FDR BKR', 'XFMR', 'SERVICE'], p=[0.18, 0.04, 0.015, 0.385, 0.38]))
            tot = feeder_members(net, fd, tp, start.replace(tzinfo=C.UTC))
            share = {'FUSE': rng.uniform(0.01, 0.12), 'RECLOSER': rng.uniform(0.15, 0.5), 'FDR BKR': 1.0,
                     'XFMR': rng.uniform(0.0005, 0.004), 'SERVICE': rng.uniform(0.0002, 0.0006)}[dev]
            m = max(1, int(round(tot * share)))
            dur = dt.timedelta(minutes=float(rng.lognormal(math.log(80), 0.7)))
            steps = []
            if dev in ('RECLOSER', 'FDR BKR') and rng.random() < 0.6:
                k = int(rng.integers(2, 4))
                left = m
                for s in range(k - 1):
                    part = int(left * rng.uniform(0.3, 0.6))
                    steps.append((start + dur * (s + 1) / k, part))
                    left -= part
                steps.append((start + dur, left))
            events.append(dict(feeder=fd['feeder'], start=start, restore=start + dur, cause=cause, device=dev, members=m,
                               remarks='', steps=steps))
    events.sort(key=lambda e: (e['start'], e['feeder']))
    for i, e in enumerate(events):
        oid = 100001 + i
        cur.execute('INSERT INTO outage VALUES (?,?,?,?,?,?,?,?)', (oid, e['feeder'], e['start'].strftime('%Y-%m-%d %H:%M'),
                    e['restore'].strftime('%Y-%m-%d %H:%M'), e['cause'], e['device'], e['members'], e['remarks']))
        for k, (ts, mres) in enumerate(e['steps']):
            cur.execute('INSERT INTO outage_step VALUES (?,?,?,?)', (oid, k + 1, ts.strftime('%Y-%m-%d %H:%M'), mres))
    con.commit()
    con.execute('VACUUM')
    con.close()
    return len(events)


def members_rows(w, fds):
    net = w['net']
    taps = {tp['name']: tp for tp in net['taps']}
    rows = []
    for yr in range(2022, 2027):
        for mo in range(1, 13):
            if yr == 2026 and mo > 10:
                continue
            t = dt.datetime(yr, mo, 15, tzinfo=C.UTC)
            for fd in fds:
                rows.append(('%d-%02d' % (yr, mo), fd['feeder'], fd['tap'], feeder_members(net, fd, taps[fd['tap']], t)))
    return rows


# ------------------------------------------------------------------------------------------------ patrols and work orders

FINDINGS = {
    'growin': ['tree grown up into the line mid-span {s}, burn marks on the limb, trimmed',
               'live oak reaching the bottom phase in span {s}, scorched, cut back'],
    'fallin': ['dead pine limb across the conductors between {s}, removed', 'tree from outside the right of way on the line near {s}'],
    'insulator': ['flashed and cracked porcelain on {s}, string replaced', 'broken bell, flash marks, {s}, replaced'],
    'vehicle': ['pole {s} broken by a vehicle, replaced', 'truck hit {s}, pole changed out'],
    'hardware': ['failed jumper connector at {s}, repaired', 'burnt clamp at {s}, repaired'],
    'bird': ['flash marks on the crossarm at {s}, droppings on the insulators', 'dead bird at the base of {s}, flash marks'],
    'fog': ['flash marks on the insulators at {s}, heavy salt film', 'tracking on the porcelain at {s}'],
    'lightning': ['shattered insulator at {s}', 'arrester blown at {s}, replaced'],
    'unknown': ['patrolled the line, nothing found'],
}


def _str_txt(no, rng):
    fmt = rng.choice(['str {n}', 'Str. {n}', 'structure {n}', '#{n}', 'pole {n}', 'str {n}'])
    return fmt.format(n=no)


def _as_numbered(lid, no, day):
    """the structure number a crew read off the plate on that day (rebuilt lines carried their old numbers before)"""
    if lid in N.REBUILT and day < N.REBUILT[lid][0]:
        return no + N.REBUILT[lid][1]
    return no


def patrol_rows(w):
    net = w['net']
    rng = np.random.default_rng(C.EV_SEED + 1111)
    rows = []
    for f in w['faults']:
        line = net['lines'][f['line']]
        rel = f['records'].get('a') if f['records'].get('a', {}).get('family') not in (None, 'EM') else f['records'].get('b')
        rep_km = None
        if rel and rel.get('family') not in (None, 'EM') and not rel.get('lost') and -1.0 <= rel['dist_km'] <= 1.6 * line['length']:
            # the dispatcher sends a crew only on a distance the locator printed
            rep_km = rel['dist_km'] if rel is f['records'].get('a') else line['length'] - rel['dist_km']
            rep_km = min(max(rep_km, 0.0), line['length'])
        lt = C.to_local(f['t'])
        if f['permanent']:
            d = lt + dt.timedelta(hours=float(rng.uniform(0.5, 5)))
            no = _as_numbered(f['line'], f['structure'], d.date())
            if f['cause'] in ('growin', 'fallin'):
                no2 = no + 1 if no < len(line['structures']) else no - 1
                stxt = '%s-%s' % (_str_txt(min(no, no2), rng), max(no, no2))
            else:
                stxt = _str_txt(no, rng)
            find = str(rng.choice(FINDINGS[f['cause']])).format(s=stxt)
            rows.append(dict(date=d.date(), line='Line %d' % int(f['line'][1:]), frm=1, to=len(line['structures']),
                             crew=str(rng.choice(['Crew 2', 'Crew 4', 'Crew 5', 'Crew 7'])), find=find, ref=f['id']))
        elif rep_km is not None and rng.random() < 0.28:
            d = lt + dt.timedelta(days=float(rng.uniform(0.3, 6)))
            k0 = max(0.0, rep_km - 1.5)
            k1 = min(line['length'], rep_km + 1.5)
            s0 = N.structure_at(net, f['line'], k0)['no']
            s1 = N.structure_at(net, f['line'], k1)['no']
            # a crew that walks past a passing fault sees its marks only sometimes
            found = s0 <= f['structure'] <= s1 and rng.random() < {'bird': 0.35, 'insulator': 0.3, 'growin': 0.15,
                                                                   'fog': 0.2, 'lightning': 0.2}.get(f['cause'], 0.0)
            s0, s1 = _as_numbered(f['line'], s0, d.date()), _as_numbered(f['line'], s1, d.date())
            if found:
                sn = _as_numbered(f['line'], f['structure'], d.date())
                find = str(rng.choice(FINDINGS[f['cause']])).format(s=_str_txt(sn, rng))
                if f['cause'] == 'insulator':
                    find = 'flash marks on the porcelain at %s, string looks sound, left in service' % _str_txt(sn, rng)
                if f['cause'] == 'growin':
                    find = 'scorched branch near %s, no clearance problem seen from the ground' % _str_txt(sn, rng)
            else:
                find = 'patrolled %s to %s, nothing found' % (_str_txt(s0, rng), s1)
            rows.append(dict(date=d.date(), line='Line %d' % int(f['line'][1:]), frm=s0, to=s1,
                             crew=str(rng.choice(['Crew 2', 'Crew 4', 'Crew 5', 'Crew 7'])), find=find, ref=f['id']))
    rows.sort(key=lambda r: r['date'])
    return rows
