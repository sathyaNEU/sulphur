"""The relays' own exports: EventRecall's CSV (the stations with that family of relays: UTC from the station clock,
distances in miles, primary amperes), GridVue's JSON (local prevailing time, kilometres, kA), and Ponder Creek's
electromechanical targets as the technicians wrote them up. Every trip in a reclose sequence is its own record;
relays also keep a record of faults on the neighbouring lines their backup zones saw without tripping; a record lost
from memory is simply not in the export."""
import csv
import datetime as dt
import json
import math

import numpy as np

import common as C
import network as N

MI = 1.609344


def relay_name(st, lid):
    return '%s-%s' % (st, 'L%d' % int(lid[1:]))


def neighbours(net, lid):
    """lines sharing a terminal with lid, and the terminal they share"""
    line = net['lines'][lid]
    out = []
    for other, ol in net['lines'].items():
        if other == lid:
            continue
        for end in ('a', 'b'):
            if ol[end] in (line['a'], line['b']):
                out.append((other, end))
    return out


def _clamp(dist, length):
    return dist if -1.0 <= dist <= 1.6 * length else None


def build_rows(w):
    net = w['net']
    rng = np.random.default_rng(C.EV_SEED + 606)
    er, gv, em = [], [], []
    ev_no = {}
    lost = []

    def next_no(relay):
        ev_no[relay] = ev_no.get(relay, 3000 + int(rng.integers(0, 4000))) + 1
        return ev_no[relay]

    for f in w['faults']:
        line = net['lines'][f['line']]
        ops = f['ops']
        n_trips = ops['n_trips']
        ftype = ''.join(sorted(f['phases'])) + ('G' if len(f['phases']) == 1 else '')
        if len(f['phases']) == 1:
            ftype = f['phases'][0] + 'G'
        for end in ('a', 'b'):
            rec = f['records'].get(end)
            st = line[end]
            relay = relay_name(st, f['line'])
            if rec is None:
                continue
            if rec['family'] == 'EM':
                em.append(dict(f=f, st=st, line=f['line'], n_trips=n_trips))
                continue
            if rec['lost']:
                lost.append((relay, rec['t'], n_trips))
                continue
            for shot in range(n_trips):
                t = rec['t'] + dt.timedelta(seconds=[0.0, 1.06, 15.06][shot])
                scale = 1.0 + rng.normal(0, 0.006)
                dist = _clamp(rec['dist_km'] * (1 + rng.normal(0, 0.004)), line['length'])
                I = {p: v * scale for p, v in rec['I'].items()}
                IG = rec['IG'] * scale
                zone = 'Z1' if (dist is not None and dist <= 0.85 * line['length']) else 'Z2'
                row = dict(station=st, relay=relay, line=f['line'], t=t, type=ftype, dist=dist, I=I, IG=IG, shot=shot,
                           trip=True, zone=zone, family=rec['family'], no=next_no(relay))
                (er if rec['family'] == 'ER' else gv).append(row)
        # backup zones on the neighbouring lines see the fault without tripping
        for other, end in neighbours(net, f['line']):
            ol = net['lines'][other]
            st = ol[end]
            fam = N.ST[st]['relay']
            if fam == 'EM' or rng.random() > 0.55:
                continue
            shared_is_a = (st == line['a'])
            beyond = (f['km'] if shared_is_a else line['length'] - f['km'])
            dist = ol['length'] + beyond * (1.0 + rng.uniform(0.1, 0.6))
            if dist > 2.2 * ol['length']:
                continue
            relay = relay_name(st, other)
            ref = f['records'].get('a' if shared_is_a else 'b') or {}
            frac = rng.uniform(0.15, 0.45)
            I = {p: v * frac for p, v in (ref.get('I') or {'A': 300.0, 'B': 300.0, 'C': 300.0}).items()}
            IG = (ref.get('IG') or 200.0) * frac
            off = 0.0
            import relays as R
            for (sc, sl), (t0, t1, rate) in R.CLOCK_FAULTS.items():
                if sc == st and t0 <= f['t'] <= t1:
                    off = rate * (f['t'] - t0).total_seconds() / 86400.0
            t = f['t'] + dt.timedelta(seconds=0.012 + off + 0.004 * rng.random())
            row = dict(station=st, relay=relay, line=other, t=t, type=ftype, dist=_clamp(dist, ol['length']), I=I, IG=IG,
                       shot=0, trip=False, zone='Z2 PU' if rng.random() < 0.7 else 'Z3 PU', family=fam, no=next_no(relay))
            (er if fam == 'ER' else gv).append(row)
    # relay self-tests and manual triggers
    for lid, line in net['lines'].items():
        for end in ('a', 'b'):
            st = line[end]
            fam = N.ST[st]['relay']
            if fam == 'EM':
                continue
            relay = relay_name(st, lid)
            for yr in range(2022, 2027):
                if rng.random() < 0.85:
                    d = dt.datetime(yr, int(rng.integers(1, 11)), int(rng.integers(1, 28)), int(rng.integers(14, 21)),
                                    int(rng.integers(0, 60)), tzinfo=C.UTC)
                    row = dict(station=st, relay=relay, line=lid, t=d, type='TRIG', dist=None,
                               I={'A': float(rng.uniform(150, 420)), 'B': float(rng.uniform(150, 420)), 'C': float(rng.uniform(150, 420))},
                               IG=float(rng.uniform(1, 9)), shot=0, trip=False, zone='MANUAL', family=fam, no=next_no(relay))
                    (er if fam == 'ER' else gv).append(row)
    # each relay's event counter runs in time order and also counts what never reached the export: the records its
    # buffer overwrote before retrieval and its own settings, self-test and power-up events
    gap = np.random.default_rng(C.EV_SEED + 6061)
    start = {}
    for r in er + gv:
        start[r['relay']] = min(start.get(r['relay'], r['no']), r['no'])
    seq = {}
    for r in er + gv:
        seq.setdefault(r['relay'], []).append((r['t'], 1, r))
    for relay, t, n in lost:
        for k in range(n):
            seq.setdefault(relay, []).append((t + dt.timedelta(seconds=[0.0, 1.06, 15.06][k]), 0, None))
    for relay in sorted(seq):
        no = start.get(relay, 3000) - 1
        for t, _, r in sorted(seq[relay], key=lambda x: (x[0], x[1])):
            no += 1 + int(gap.poisson(0.3))
            if r is not None:
                r['no'] = no
    er.sort(key=lambda r: (r['station'], r['t']))
    gv.sort(key=lambda r: (r['station'], r['t']))
    return er, gv, em


def write_er(rows, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['Station', 'Relay', 'Event', 'Date', 'Time', 'Type', 'Targets', 'Location', 'IA', 'IB', 'IC', 'IG', 'Shot'])
        for r in rows:
            t = r['t']
            tg = ('%s TRIP' % r['zone'] + (' 79' if r['shot'] else '')) if r['trip'] else r['zone']
            loc = '%.2f' % (r['dist'] / MI) if r['dist'] is not None else '$$$$$$'
            if r['type'] == 'TRIG':
                tg, loc = 'TRIG', ''
            wr.writerow([r['station'], r['relay'], r['no'], t.strftime('%m/%d/%Y'), t.strftime('%H:%M:%S.') + '%03d' % (t.microsecond // 1000),
                         'ER' if r['type'] == 'TRIG' else r['type'], tg, loc, int(round(r['I']['A'])), int(round(r['I']['B'])),
                         int(round(r['I']['C'])), int(round(r['IG'])), r['shot']])
    return len(rows)


def write_gv(rows, path):
    out = []
    for r in rows:
        t = C.to_local(r['t'])
        out.append({
            'device': r['relay'].replace('-', '_') + '_D60',
            'record_id': int(r['no']),
            'time_local': t.strftime('%Y-%m-%d %H:%M:%S.') + '%03d' % (t.microsecond // 1000),
            'fault_type': None if r['type'] == 'TRIG' else r['type'],
            'distance_km': (None if r['dist'] is None else round(r['dist'], 1)),
            'ia_ka': round(r['I']['A'] / 1000.0, 3), 'ib_ka': round(r['I']['B'] / 1000.0, 3),
            'ic_ka': round(r['I']['C'] / 1000.0, 3), 'in_ka': round(r['IG'] / 1000.0, 3),
            'trip': bool(r['trip']), 'element': ('manual trigger' if r['type'] == 'TRIG' else r['zone']),
            'reclose_shot': int(r['shot']),
        })
    with open(path, 'w') as fh:
        json.dump({'export': 'GridVue event records', 'generated': '2026-11-03T09:06:41', 'count': len(out),
                   'records': out}, fh, indent=1)
    return len(out)


def legacy_rows(w, em, rng=None):
    """Ponder Creek: the technicians' visits, each listing the targets found and the breaker counter"""
    rng = rng or np.random.default_rng(C.EV_SEED + 707)
    counters = {}
    rows = []
    for item in sorted(em, key=lambda x: x['f']['t']):
        f = item['f']
        lid = f['line']
        brk = 'PND-B62%02d' % int(lid[1:])
        counters[brk] = counters.get(brk, 310 + int(rng.integers(0, 200))) + item['n_trips']
        visit = C.to_local(f['t']) + dt.timedelta(hours=float(rng.uniform(2, 30)))
        tg = ('21G Z1' if len(f['phases']) == 1 else '21P Z1') + (', 79 LO' if f['permanent'] else '')
        rows.append(dict(date=visit.date(), time=visit.strftime('%H:%M') if rng.random() < 0.7 else '', breaker=brk,
                         line=lid, targets=tg, counter=counters[brk], tech=['JRM', 'DLT', 'AKW', 'RSP'][int(rng.integers(0, 4))],
                         remark=('lockout, line patrolled' if f['permanent'] else 'targets reset')))
    return rows
