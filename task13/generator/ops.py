"""What operations recorded. Each 69 kV fault trips both terminals' breakers, recloses once after a second and again
after fifteen; a fault that is still there locks the line out, the taps with an automatic throw-over transfer to
their alternate line, the control room closes the manual alternates by SCADA, isolates the faulted section with the
line switches (on SCADA where the tap has motor-operated switches, by a crew otherwise) and recloses the line, and a
patrol finds what it can. The SCADA master time-stamps every breaker, switch and transfer to the millisecond; the
control room types its own log; the outage system opens a loss-of-source outage on each feeder that lost power for
more than its alarm delay and a dispatcher closes it, often well after the lights came back. Members are counted by
feeder each month. Patrols, insulator replacements, perch guards and the vegetation crews' work are booked in the
work management system."""
import datetime as dt
import math

import numpy as np

import common as C
import network as N
import weather as W

FIRST_SHOT = 1.0          # seconds of dead time before the first reclose
SECOND_SHOT = 15.0
AUTO_XFER = 20.0          # seconds after loss of voltage an automatic throw-over closes its alternate
CREW_SPEED = (45.0, 115.0)    # minutes for a crew to open a manual line switch
SCADA_SPEED = (6.0, 24.0)     # minutes for the control room to isolate with motor-operated switches


def _breakers(net):
    """breaker numbers at each line terminal"""
    out = {}
    for lid, line in net['lines'].items():
        n = int(lid[1:])
        out[(lid, 'a')] = '%s %d%02d' % (line['a'], 5, n) if False else '%s-%s' % (line['a'], 'B%d%02d' % (52, n))
        out[(lid, 'b')] = '%s-%s' % (line['b'], 'B%d%02d' % (62, n))
    return out


def members_at(net, tap, t):
    """members on a tap in the month of t: the 2026 count less growth back to that month"""
    months = (2026 - t.year) * 12 + (10 - t.month)
    return int(round(tap['members'] / (1.0 + 0.0013) ** max(months, 0)))


def operate(w):
    net, wx = w['net'], w['wx']
    rng = np.random.default_rng(C.EV_SEED + 505)
    brk = _breakers(net)
    soe, crlog, oms_ev, oms_steps, patrols, impacts = [], [], [], [], [], []
    taps_by_line = {}
    for tp in net['taps']:
        taps_by_line.setdefault(tp['line'], []).append(tp)
    for f in w['faults']:
        line = net['lines'][f['line']]
        t0 = f['t']
        t_trip = t0 + dt.timedelta(seconds=0.055 + 0.01 * rng.random())
        perm = f['permanent']
        second_ok = (not perm) and rng.random() < 0.09
        ev = dict(fault=f['id'], line=f['line'], t0=t0, trip=t_trip, perm=perm, ops=[],
                  n_trips=3 if perm else (2 if second_ok else 1))
        for end in ('a', 'b'):
            b = brk[(f['line'], end)]
            st = line[end]
            jit = dt.timedelta(milliseconds=float(rng.uniform(0, 12)))
            ev['ops'].append((t_trip + jit, st, b, 'TRIP'))
            ev['ops'].append((t_trip + jit + dt.timedelta(seconds=FIRST_SHOT), st, b, 'CLOSE'))
            if perm or second_ok:
                ev['ops'].append((t_trip + jit + dt.timedelta(seconds=FIRST_SHOT + 0.06), st, b, 'TRIP'))
                ev['ops'].append((t_trip + jit + dt.timedelta(seconds=SECOND_SHOT), st, b, 'CLOSE'))
                if perm:
                    ev['ops'].append((t_trip + jit + dt.timedelta(seconds=SECOND_SHOT + 0.06), st, b, 'TRIP'))
                    ev['ops'].append((t_trip + jit + dt.timedelta(seconds=SECOND_SHOT + 0.10), st, b, 'LOCKOUT'))
        line_back = t_trip + dt.timedelta(seconds=FIRST_SHOT if not (perm or second_ok) else SECOND_SHOT)
        tap_out = {}
        if perm:
            # the control room isolates the faulted section and recloses the line
            taps = taps_by_line.get(f['line'], [])
            fast = any(tp['moab'] for tp in taps) or not taps
            mins = rng.uniform(*SCADA_SPEED) if fast else rng.uniform(*CREW_SPEED)
            t_sect = t_trip + dt.timedelta(minutes=float(mins))
            # switch points: each tap's switch pair, plus the terminals
            pts = sorted([0.0] + [tp['km'] for tp in taps] + [line['length']])
            lo = max(p for p in pts if p <= f['km'])
            hi = min(p for p in pts if p >= f['km'])
            sw_ops = []
            for k in (lo, hi):
                if 0.0 < k < line['length']:
                    tp = [x for x in taps if x['km'] == k][0]
                    sw_ops.append((t_sect - dt.timedelta(seconds=float(rng.uniform(20, 90))), tp['name'], k))
            for (ts, name, k) in sw_ops:
                side = 'S1' if k == lo else 'S2'
                ev['ops'].append((ts, 'SW', '%s %s' % (name.upper()[:10].replace(' ', ''), side), 'OPEN' if k else 'OPEN'))
            # only a terminal on a healthy section is reclosed: a fault between a terminal and the first tap switch keeps
            # that terminal open until the repair
            ev['closed_ends'] = []
            for end in ('a', 'b'):
                if (end == 'a' and lo == 0.0) or (end == 'b' and hi == line['length']):
                    continue
                b = brk[(f['line'], end)]
                ev['ops'].append((t_sect + dt.timedelta(seconds=float(rng.uniform(5, 50))), line[end], b, 'CLOSE'))
                ev['closed_ends'].append(end)
            ev['t_sect'] = t_sect
            line_back = t_sect
            # repair and the switches closed again, hours to two days later
            t_rep = t_sect + dt.timedelta(hours=float(rng.uniform(3, 46)))
            for end in ('a', 'b'):
                if end not in ev['closed_ends']:
                    b = brk[(f['line'], end)]
                    ev['ops'].append((t_rep + dt.timedelta(seconds=float(rng.uniform(310, 900))), line[end], b, 'CLOSE'))
            for (ts, name, k) in sw_ops:
                side = 'S1' if k == lo else 'S2'
                ev['ops'].append((t_rep + dt.timedelta(seconds=float(rng.uniform(0, 300))), 'SW',
                                  '%s %s' % (name.upper()[:10].replace(' ', ''), side), 'CLOSE'))
            ev['t_rep'] = t_rep
        # member impact by tap
        imp = []
        for tp in taps_by_line.get(f['line'], []):
            m = members_at(net, tp, t0)
            if not perm:
                out_s = (line_back - t0).total_seconds()
                imp.append(dict(tap=tp['name'], members=m, seconds=out_s, how='reclose'))
                continue
            if tp['backup'] == 'auto':
                imp.append(dict(tap=tp['name'], members=m, seconds=AUTO_XFER + float(rng.uniform(0, 4)), how='auto transfer'))
                ev['ops'].append((t0 + dt.timedelta(seconds=AUTO_XFER), N.ST[f['line'][:0] or line['a']]['code'] if False else 'XFER',
                                  '%s ALT %s' % (tp['name'].upper()[:10].replace(' ', ''), tp['alt']), 'CLOSE'))
                continue
            closes = [o[0] for o in ev['ops'] if o[3] == 'CLOSE' and o[1] in (line['a'], line['b'])
                      and o[0] > t0 + dt.timedelta(seconds=60)]
            t_rest = min(closes) if closes else ev['t_sect']
            how = 'line reclosed after isolation'
            if tp['backup'] == 'manual':
                t_man = t_trip + dt.timedelta(minutes=float(rng.uniform(7, 19)))
                if t_man < t_rest:
                    t_rest = t_man
                    how = 'manual transfer'
                    ev['ops'].append((t_man, 'XFER', '%s ALT %s' % (tp['name'].upper()[:10].replace(' ', ''), tp['alt']), 'CLOSE'))
            imp.append(dict(tap=tp['name'], members=m, seconds=(t_rest - t0).total_seconds(), how=how))
        ev['impact'] = imp
        f['ops'] = ev
        soe.extend(ev['ops'])
        impacts.append(dict(fault=f['id'], line=f['line'], t0=t0, impact=imp, perm=perm))
    w['soe_fault_ops'] = soe
    w['impacts'] = impacts
    return w
