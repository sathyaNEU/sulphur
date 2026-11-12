"""The pack's system exports, each on its own clock and in its own form: the ADMS FLISR event archive (UTC, two
message formats either side of the March 2025 upgrade, the redundant server's echoes, and nothing from the minutes
its event queue overflowed), the outage record (Central prevailing time, one row per restoration step), the SCADA
historian's hourly amps (Central Standard Time, wide), the devices' sequence of events with their weekly battery
self-tests (Central Standard Time), the airport's hourly weather (UTC, Fahrenheit and knots) and the AMI head-end's
daily notification counts."""
import csv
import datetime as dt
import math

import numpy as np

import common as C
import load as LD
import sim as S

UPGRADE = dt.datetime(2025, 3, 18, 19, 40, tzinfo=dt.timezone.utc)     # 14:40 CDT 18 March 2025


def _rng(k):
    return np.random.default_rng(C.EV_SEED * 31 + k)


def in_windows(w, t):
    hf = (t - C.T0).total_seconds() / 3600.0
    for s, e in w['windows']:
        if s <= hf < e:
            return True
    return False


def tag(w, asset, when):
    if asset.endswith(' CB'):
        return asset.replace(' ', '_') if when < UPGRADE else asset.replace(' ', '-')
    D = w['NET']['devices'][asset]
    return D['tag_old'] if when < UPGRADE else D['tag_new']


def adms_messages(w):
    """every FLISR archive message the ADMS raised, in its own words for the release it ran, before any loss"""
    NET = w['NET']
    devs = NET['devices']
    loops = {Lp['loop']: Lp for Lp in NET['loops']}
    rows = []
    for Sx in w['seqs']:
        lp = loops[Sx['loop']]
        scheme = lp['scheme']
        for t, kind, d in Sx['steps']:
            new = t >= UPGRADE
            if kind == 'START':
                tg = tag(w, d['lockout'], t)
                msg = ('FLISR sequence started; lockout device=%s' % tg) if new else ('FLISR START: LOCKOUT %s' % tg)
            elif kind == 'NOT STARTED':
                why = d['why']
                if why == 'abnormal':
                    msg = 'FLISR not started; scheme disarmed (loop not in normal configuration)' if new else \
                        'FLISR NOT STARTED: SCHEME DISARMED (LOOP ABNORMAL)'
                else:
                    tg = tag(w, why, t) if why in devs else why
                    msg = ('FLISR not started; scheme disarmed (communication lost: %s)' % tg) if new else \
                        ('FLISR NOT STARTED: SCHEME DISARMED (%s COMM)' % tg)
            elif kind == 'FPI':
                tg = tag(w, d['dev'], t)
                msg = ('Fault indication: %s = %s' % (tg, 'YES' if d['ind'] else 'NO')) if new else \
                    ('FPI %s: %s' % (tg, 'FAULT' if d['ind'] else 'NO FAULT'))
            elif kind == 'LOCATED':
                msg = ('Fault located in section %d of %s' % (d['sec'], Sx['feeder'])) if new else \
                    ('FAULT LOCATED: SECTION %d (%s)' % (d['sec'], Sx['feeder']))
            elif kind == 'OPENED':
                tg = tag(w, d['dev'], t)
                msg = ('Open %s confirmed' % tg) if new else ('OPEN %s: CONFIRMED' % tg)
            elif kind == 'TIMEOUT':
                tg = tag(w, d['dev'], t)
                msg = ('Command %s to %s timed out' % (d['op'], tg)) if new else \
                    ('COMMAND TIMEOUT: %s (%s)' % (tg, d['op'].upper()))
            elif kind == 'OP FAILED':
                tg = tag(w, d['dev'], t)
                msg = ('Command %s to %s failed: device reported operation failure' % (d['op'], tg)) if new else \
                    ('OPERATION FAILED: %s (%s)' % (tg, d['op'].upper()))
            elif kind == 'CAPACITY':
                ok = d['load'] + d['xfer'] <= d['limit']
                msg = ('Capacity check on %s: pre-load %d A, transfer %d A, limit %d A, result %s' %
                       (d['recv'], round(d['load']), round(d['xfer']), d['limit'], 'OK' if ok else 'EXCEEDED')) if new \
                    else ('CAPACITY CHECK %s: LOAD %dA + XFER %dA / LIMIT %dA: %s' %
                          (d['recv'], round(d['load']), round(d['xfer']), d['limit'], 'PASS' if ok else 'FAIL'))
            elif kind == 'GROUP2':
                tg = tag(w, d['dev'], t)
                msg = ('Alternate settings group activated: %s' % tg) if new else ('SET GROUP 2 %s: CONFIRMED' % tg)
            elif kind == 'RECV TRIPPED ON CLOSE':
                tg = tag(w, d['dev'], t)
                msg = ('Receiving device %s tripped on tie close; sequence aborted' % tg) if new else \
                    ('RECV DEVICE %s TRIPPED ON CLOSE: ABORT' % tg)
            elif kind == 'COMPLETE':
                tie = S.tie_of(NET, Sx['loop'])
                msg = None
                rows.append((t - dt.timedelta(seconds=1), scheme,
                             ('Tie %s closed' % tag(w, tie, t)) if new else ('CLOSE %s: CONFIRMED' % tag(w, tie, t)),
                             tie))
                n = int(d['n'])
                msg = ('Restoration complete; customers restored=%d' % n) if new else \
                    ('RESTORATION COMPLETE: %d CUSTOMERS' % n)
            elif kind == 'AWAIT CONFIRM':
                msg = 'Supervised mode: transfer proposed, awaiting operator confirmation' if new else \
                    'SUPERVISED: AWAITING OPERATOR CONFIRMATION'
            elif kind == 'CONFIRMED':
                msg = 'Supervised mode: transfer confirmed by operator' if new else 'SUPERVISED: OPERATOR CONFIRMED'
            elif kind == 'UPSTREAM RESTORED':
                msg = 'Upstream section restored by breaker close' if new else 'UPSTREAM RESTORED: BREAKER CLOSED'
            elif kind == 'CLOSE ONTO FAULT':
                tg = tag(w, d['dev'], t)
                msg = ('Reclose of %s onto fault; sequence aborted' % tg) if new else ('%s RECLOSED ONTO FAULT: ABORT' % tg)
            else:
                continue
            rows.append((t, scheme, msg, d.get('dev') if isinstance(d, dict) else None))
        # an end-of-sequence line where the scheme stopped without restoring
        if Sx['outcome'] == 'blocked':
            t = Sx['steps'][-1][0] + dt.timedelta(seconds=1)
            rows.append((t, scheme, 'Restoration blocked: capacity' if t >= UPGRADE else 'RESTORATION BLOCKED: CAPACITY',
                         None))
        elif Sx['outcome'] == 'failed' and Sx['steps'] and Sx['steps'][-1][1] in ('TIMEOUT', 'OP FAILED'):
            t = Sx['steps'][-1][0] + dt.timedelta(seconds=2)
            rows.append((t, scheme, 'Sequence aborted' if t >= UPGRADE else 'FLISR ABORTED', None))
        elif Sx['outcome'] == 'no restoration possible':
            t = Sx['steps'][-1][0] + dt.timedelta(seconds=3)
            rows.append((t, scheme, 'No restoration available (fault in end section)' if t >= UPGRADE else
                         'NO RESTORATION AVAILABLE: END SECTION', None))
    # scheme arming: disarmed while a device is unreachable, and while the loop is out of its normal configuration
    for hf, lid, a, kind in w['disarm_log']:
        t = C.T0 + dt.timedelta(hours=hf)
        scheme = loops[lid]['scheme']
        new = t >= UPGRADE
        if kind == 'disarm':
            tg = tag(w, a, t)
            msg = ('Scheme disarmed: communication lost with %s' % tg) if new else ('SCHEME DISARMED: %s COMM FAIL' % tg)
        else:
            tg = tag(w, a, t)
            msg = ('Scheme armed: communication restored with %s' % tg) if new else ('SCHEME ARMED: %s COMM OK' % tg)
        rows.append((t, scheme, msg, a))
    for Sx in w['seqs']:
        if Sx.get('t_rtn') is not None:
            scheme = loops[Sx['loop']]['scheme']
            t0 = Sx['t_rest'] + dt.timedelta(seconds=3)
            t1 = Sx['t_rtn']
            rows.append((t0, scheme, 'Scheme disarmed: loop not in normal configuration' if t0 >= UPGRADE
                         else 'SCHEME DISARMED: LOOP ABNORMAL', None))
            rows.append((t1, scheme, 'Scheme armed: loop returned to normal configuration' if t1 >= UPGRADE
                         else 'SCHEME ARMED: LOOP NORMAL', None))
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def write_adms(w, path):
    rng = _rng(1)
    rows = [r for r in adms_messages(w) if r[0] >= C.REC0 and r[0] < C.T_END]
    kept = [r for r in rows if not in_windows(w, r[0])]
    out = []
    for t, scheme, msg, dev in kept:
        server = 'ADMS-A' if rng.random() < 0.93 else 'ADMS-B'
        out.append([t, server, scheme, msg])
        if rng.random() < 0.035:      # the standby server echoes a message during a sync
            out.append([t + dt.timedelta(milliseconds=int(rng.integers(5, 900))), 'ADMS-B' if server == 'ADMS-A'
                        else 'ADMS-A', scheme, msg])
    out.sort(key=lambda r: r[0])
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['record_no', 'event_time_utc', 'server', 'category', 'scheme', 'message'])
        no = 4471208
        for t, server, scheme, msg in out:
            no += 1
            ts = t.strftime('%Y-%m-%dT%H:%M:%S.') + '%03dZ' % (t.microsecond // 1000)
            wr.writerow([no, ts, server, 'FLISR', scheme, msg])
    return len(out), len(rows) - len(kept)


def oms_rows(w):
    """the outage record, one row per restoration step, as the dispatchers' system holds it"""
    rng = _rng(2)
    NET = w['NET']
    devs = NET['devices']
    out = []
    causes_main = ['Tree contact', 'Lightning', 'Equipment failure', 'Animal contact', 'Wind', 'Ice/snow',
                   'Unknown - no cause found', 'Vehicle', 'Insulator failure', 'Conductor down']
    causes_lat = ['Tree contact', 'Animal contact', 'Lightning', 'Fuse operation - no cause found',
                  'Equipment failure', 'Wind', 'Cutout failure']
    causes_x = ['Transformer failure', 'Secondary/service', 'Animal contact', 'Overload', 'Tree contact',
                'Lightning', 'Meter/base']
    for r in sorted(w['oms'], key=lambda x: x['true_start']):
        if r['true_start'] < C.REC0 - dt.timedelta(hours=1) or r['true_start'] >= C.T_END:
            continue
        lost = r['kind'] in ('main', 'recv_trip') and in_windows(w, r['true_start'])
        start = r['start']
        if lost:
            start = r['true_start'] + dt.timedelta(minutes=float(rng.lognormal(np.log(11), 0.6)))
        storm = r.get('storm', 0)
        if r['kind'] == 'xfmr':
            cause = rng.choice(causes_x, p=[.3, .2, .12, .1, .1, .1, .08])
        elif r['kind'] == 'lateral':
            cause = rng.choice(causes_lat, p=[.28, .2, .14, .14, .1, .09, .05])
        elif r['kind'] == 'recv_trip':
            cause = 'Unknown - no cause found' if r['cause'] == 'overload' else 'Fault on transferred section'
        else:
            p = np.array([.24, .14, .15, .1, .1, .04, .12, .03, .05, .03])
            if storm > 0.6:
                p = np.array([.3, .25, .08, .03, .2, .01, .06, .02, .03, .02])
            cause = rng.choice(causes_main, p=p / p.sum())
        dev = r['device']
        if dev in devs:
            dev_s = dev
        elif dev == 'FUSE':
            dev_s = 'FU-%s-%d' % (r['feeder'][-3:], int(rng.integers(1000, 9999)))
        elif dev == 'XFMR':
            dev_s = 'T%d' % int(rng.integers(100000, 999999))
        else:
            dev_s = dev
        steps = list(r['steps'])
        if lost:
            # the automatic restoration never reached the outage system: those customers wait in the next step
            keep = []
            carry = 0
            for st in steps:
                if st[2] == 'flisr':
                    carry += st[1]
                else:
                    keep.append(st)
            if carry and keep:
                m, n, k, s = keep[-1]
                keep[-1] = (m, n + carry, k, s)
            steps = keep
        steps = sorted(steps, key=lambda s: s[0])
        tot = sum(s[1] for s in steps)
        for i, (mins, n, kind, sec) in enumerate(steps):
            if n <= 0:
                continue
            t = r['true_start'] + dt.timedelta(minutes=mins)
            stype = {'flisr': 'Automatic', 'remote': 'SCADA switching', 'field': 'Field switching',
                     'repair': 'Repair'}[kind]
            out.append({'outage_id': r['id'], 'feeder': r['feeder'], 'device': dev_s, 'start': start,
                        'step_time': t, 'step': i + 1, 'cust_restored': int(n), 'step_type': stype,
                        'cust_interrupted': int(tot), 'cause': cause, 'storm': storm, 'kind': r['kind']})
    return out


def _wx_tag(w, t, rng):
    W = w['W']
    h = max(0, min(W['H'] - 1, C.hour_index(t)))
    if W['thunder'][h]:
        return 'Thunderstorm'
    if W['ice'][h] > 0:
        return 'Ice'
    if W['gust'][h] > 55:
        return 'Wind'
    if W['precip'][h] > 0.3:
        return 'Snow' if W['temp'][h] < 0 else 'Rain'
    if W['temp'][h] < -18:
        return 'Cold'
    if W['temp'][h] > 31:
        return 'Hot'
    return 'Clear' if rng.random() < 0.8 else ''


def _fmt_local(t, rng):
    lt = C.to_local(t)
    return lt.strftime('%m/%d/%Y %H:%M')


def write_oms(w, path):
    rng = _rng(3)
    rows = oms_rows(w)
    wx = ['Clear', 'Rain', 'Thunderstorm', 'Wind', 'Snow', 'Ice', 'Cold', 'Hot']
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['Outage ID', 'Feeder', 'Interrupting Device', 'Outage Start', 'Step', 'Step Restored',
                     'Step Type', 'Customers Restored', 'Customers Interrupted', 'Cause', 'Weather', 'Remarks'])
        for r in rows:
            fdr = r['feeder'] if rng.random() < 0.8 else r['feeder'][:3] + '-' + r['feeder'][3:]
            weather = _wx_tag(w, r['start'], rng)
            rem = ''
            if r['step_type'] == 'Repair' and rng.random() < 0.25:
                rem = rng.choice(['Crew repaired and re-energized', 'Replaced fuse', 'Patrolled, repaired',
                                  'Repaired conductor', 'Replaced cutout', 'Replaced transformer', 'Tree removed'])
            if r['cause'] == 'Unknown - no cause found' and r['step'] == 1:
                rem = rng.choice(['Patrolled, nothing found', 'Patrol complete NFF', 'No cause found, re-energized'])
            wr.writerow([r['outage_id'], fdr, r['device'], _fmt_local(r['start'], rng), r['step'],
                         _fmt_local(r['step_time'], rng), r['step_type'], r['cust_restored'],
                         r['cust_interrupted'], r['cause'], weather, rem])
    return len(rows)


def hourly_flows(w, h0, h1):
    """hourly average amps through every loop feeder's breaker and two reclosers, with outages and transfers applied"""
    NET = w['NET']
    L = w['L']
    amps = L['amps']
    lf = NET['loop_feeders']
    H = h1 - h0
    # fraction of each hour each section is energized normally, dead, or fed through the tie
    norm = {(f, k): np.ones(H) for f in lf for k in (1, 2, 3)}
    via = {(f, k): np.zeros(H) for f in lf for k in (1, 2, 3)}

    def mark(arr, t0, t1, val):
        a = (t0 - C.T0).total_seconds() / 3600.0 - h0
        b = (t1 - C.T0).total_seconds() / 3600.0 - h0
        if b <= 0 or a >= H:
            return
        a, b = max(a, 0.0), min(b, float(H))
        i0, i1 = int(math.floor(a)), int(math.ceil(b))
        for i in range(i0, i1):
            lo, hi = max(a, i), min(b, i + 1)
            if hi > lo:
                arr[i] = min(1.0, max(0.0, arr[i] + val * (hi - lo)))

    for r in w['oms']:
        if r['kind'] not in ('main', 'recv_trip') or r['feeder'] not in lf:
            continue
        f = r['feeder']
        if r['kind'] == 'main':
            sx = r.get('seq') or {}
            td = r.get('trip_dev', 'CB')
            secs = {'CB': [1, 2, 3], 'R1': [2, 3], 'R2': [3]}[td]
            ends = {}
            for mins, n, kind, sec in r['steps']:
                if sec is not None:
                    ends[sec] = min(ends.get(sec, 1e9), mins)
            for s_ in secs:
                end = ends.get(s_, max(st[0] for st in r['steps']))
                mark(norm[(f, s_)], r['true_start'], r['true_start'] + dt.timedelta(minutes=end), -1.0)
    for Sx in w['seqs']:
        if Sx.get('t_rest') is None or Sx.get('t_rtn') is None:
            continue
        f = Sx['feeder']
        xs = [s_ for s_ in (2, 3) if s_ > Sx['located']]
        t1 = Sx['t_rtn'] if not Sx.get('harm_kind') else Sx['harm_t']
        for s_ in xs:
            mark(via[(f, s_)], Sx['t_rest'], t1, +1.0)
            mark(norm[(f, s_)], Sx['t_rest'], t1, -1.0)
    out = {}
    for f in lf:
        a1, a2, a3 = (amps[(f, k)][h0:h1] for k in (1, 2, 3))
        n1, n2, n3 = norm[(f, 1)], norm[(f, 2)], norm[(f, 3)]
        p = NET['feeders'][f]['partner']
        v2, v3 = via[(p, 2)], via[(p, 3)]
        b2, b3 = amps[(p, 2)][h0:h1], amps[(p, 3)][h0:h1]
        xin = v2 * b2 + v3 * b3                 # partner's sections carried through this feeder's end
        out[(f, 'CB')] = a1 * n1 + a2 * n2 + a3 * n3 + xin
        out[(f, 'R1')] = a2 * n2 + a3 * n3 + xin
        out[(f, 'R2')] = a3 * n3 + xin
    # a receiving recloser that tripped on the combined load is dead until the operators switch
    for Sx in w['seqs']:
        if Sx.get('harm_kind') != 'overload':
            continue
        d = Sx['harm_dev']
        recv = Sx['recv']
        kind = w['NET']['devices'][d]['kind']
        a = (Sx['harm_t'] - C.T0).total_seconds() / 3600.0 - h0
        if 0 <= a < H:
            i = int(a)
            frac = 1 - (a - i)
            for key in [(recv, 'R2')] + ([(recv, 'R1')] if kind == 'R1' else []):
                out[key][i] *= (1 - 0.6 * frac)
    return out


def write_scada(w, path):
    rng = _rng(4)
    NET = w['NET']
    h0 = C.hour_index(dt.datetime(2025, 1, 1, 6, 0, tzinfo=dt.timezone.utc))
    h1 = min(w['W']['H'], C.hour_index(dt.datetime(2026, 11, 1, 6, 0, tzinfo=dt.timezone.utc)))
    fl = hourly_flows(w, h0, h1)
    cols = []
    for f in NET['loop_feeders']:
        for k in ('CB', 'R1', 'R2'):
            cols.append((f, k))
    names = ['%s.%s.IA_AVG' % (f, k) for f, k in cols]
    down = w['down']
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['TIMESTAMP_CST'] + names)
        for i in range(h1 - h0):
            t = C.ts_of(h0 + i)
            row = [C.to_cst(t).strftime('%Y-%m-%d %H:%M')]
            for f, k in cols:
                v = fl[(f, k)][i] * (1 + 0.008 * rng.normal())
                if k != 'CB':
                    a = S.dev_of(NET, f, k) if (f, k) not in _DEVCACHE else _DEVCACHE[(f, k)]
                    _DEVCACHE[(f, k)] = a
                    if S.is_down(down[a], h0 + i + 0.5):
                        row.append('')
                        continue
                if rng.random() < 0.0012:
                    row.append('')
                    continue
                row.append('%.1f' % max(0.0, v))
            wr.writerow(row)
    return h1 - h0


_DEVCACHE = {}


def write_devents(w, path):
    """the sequence of events the SCADA front end logged from every breaker, recloser and tie, and the controls'
    weekly battery tests"""
    rng = _rng(5)
    rows = []
    for e in w['events']:
        if e['t'] < C.REC0 or e['t'] >= C.T_END:
            continue
        val = ''
        if e['amps'] is not None:
            val = '%d A' % e['amps']
        rows.append((e['t'], e['dev'], e['ev'], val, e['src']))
    for s in w['selftests']:
        if s['t'] < C.REC0 or s['t'] >= C.T_END:
            continue
        rows.append((s['t'], s['dev'], 'BATTERY TEST', 'V_REST=%.2f V_LOAD=%.2f' % (s['v_rest'], s['v_load']), 'CTL'))
    rows.sort(key=lambda r: (r[0], r[1]))
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['Time (CST)', 'Device', 'Event', 'Value', 'Source'])
        for t, d, ev, val, src in rows:
            ts = C.to_cst(t)
            wr.writerow([ts.strftime('%Y-%m-%d %H:%M:%S.') + '%03d' % (ts.microsecond // 1000), d, ev, val, src])
    return len(rows)


def write_weather(w, path):
    rng = _rng(6)
    W = w['W']
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['station', 'valid', 'tmpf', 'dwpf', 'sknt', 'gust', 'p01i', 'wxcodes'])
        for h in range(W['H']):
            t = W['ts'][h]
            if t < C.REC0 or t >= C.T_END:
                continue
            tt = t + dt.timedelta(minutes=53)
            if rng.random() < 0.004:
                continue
            tf = W['temp'][h] * 9 / 5 + 32
            dfp = W['dew'][h] * 9 / 5 + 32
            kn = W['wind'][h] / 1.852
            g = W['gust'][h] / 1.852
            p = W['precip'][h] / 25.4
            codes = []
            if W['thunder'][h]:
                codes.append('TSRA' if p > 0.05 else 'TS')
            elif W['ice'][h] > 0:
                codes.append('FZRA')
            elif p > 0.01 and W['temp'][h] < 0:
                codes.append('-SN')
            elif p > 0.01:
                codes.append('-RA')
            missing_t = rng.random() < 0.002
            wr.writerow(['MKT', tt.strftime('%Y-%m-%d %H:%M'), 'M' if missing_t else '%.2f' % tf, '%.2f' % dfp,
                         '%.0f' % kn, ('%.0f' % g) if g > 14 else 'M', '%.2f' % p if p >= 0.005 else '0.00',
                         ' '.join(codes) if codes else 'M'])


def write_ami(w, path):
    """daily last-gasp and restoral notification counts per feeder from the AMI head-end (2025-2026)"""
    rng = _rng(7)
    rows = oms_rows(w)
    per = {}
    for r in rows:
        if r['step'] != 1:
            continue
        d = C.to_local(r['start']).date()
        if d < dt.date(2025, 1, 1):
            continue
        k = (d, r['feeder'])
        per[k] = per.get(k, 0) + r['cust_interrupted']
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['date', 'feeder', 'last_gasp_msgs', 'restoral_msgs', 'meters_reporting'])
        for (d, f), n in sorted(per.items()):
            lg = int(n * rng.uniform(0.55, 0.92))
            rs = int(n * rng.uniform(0.7, 0.98))
            wr.writerow([d.isoformat(), f, lg, rs, int(w['NET']['feeders'][f]['customers0'] * rng.uniform(0.97, 1.0))])
