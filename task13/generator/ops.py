"""What operations recorded (architecture 7, Level 5): SCADA breaker/reclose/lockout sequences, chronological planned
supervisory switching configurations (multi-week alternate-source tap transfers where taps run on their alternate
69 kV line during maintenance or load-balancing windows), restoration times, and true member impact on the live
as-operated 69 kV topology."""
import datetime as dt

import numpy as np

import common as C
import network as N

FIRST_SHOT = 1.0
SECOND_SHOT = 15.0
AUTO_XFER = 20.0
CREW_SPEED = (45.0, 115.0)
SCADA_SPEED = (6.0, 24.0)

# Planned supervisory 69 kV alternate-source switching windows across 2022-2026:
# (tap_name, normal_line, alt_line, start_iso_utc, end_iso_utc, reason)
# During [start, end), the tap is energized from `alt_line` (its normal switch on `normal_line` is OPEN in SCADA SOE),
# and because its normal line is in maintenance/clearance, a lockout on `alt_line` has NO automatic/manual backup transfer
# back to `normal_line`, causing a sustained interruption until `alt_line` is isolated/restored.
SWITCH_WINDOWS = [
    # 2022-2025 planned 69 kV maintenance / rebuild / seasonal load-relief abnormal feeding windows
    ('Palmetto Shores', 'L02', 'L16', '2022-07-08 13:15:00', '2022-09-12 19:40:00', 'Line 2 coastal pole work'),
    ('Mesquite North', 'L10', 'L15', '2022-06-10 14:05:00', '2022-11-22 18:10:00', 'Line 10 double-circuit structure work'),
    ('Live Oak East', 'L14', 'L05', '2022-10-01 13:10:00', '2022-12-20 18:30:00', 'Line 14 tie check'),
    ('Coloma', 'L05', 'L14', '2023-03-10 13:30:00', '2023-06-25 20:00:00', 'Line 5 crossarm replacement'),
    ('Caney Mill', 'L08', 'L14', '2023-07-15 12:45:00', '2023-10-20 18:30:00', 'Line 8 rebuild staging'),
    ('Heron Bend', 'L06', 'L16', '2023-08-01 14:20:00', '2023-10-15 19:15:00', 'Line 6 steel pole work'),
    ('Heron Bend', 'L06', 'L16', '2024-01-15 14:20:00', '2024-03-22 19:15:00', 'Line 6 clearance work'),
    ('Mesquite South', 'L15', 'L12', '2024-05-06 13:10:00', '2024-08-28 17:50:00', 'Line 15 conductor splice'),
    ('Live Oak East', 'L14', 'L05', '2024-07-15 13:15:00', '2024-09-20 18:30:00', 'Line 14 summer conductor clearance'),
    ('Beachwood', 'L01', 'L04', '2024-09-09 13:40:00', '2024-11-18 19:05:00', 'Line 1 coastal hardware'),
    ('Sedge Village', 'L03', 'L09', '2024-10-15 13:30:00', '2025-03-10 18:45:00', 'Line 3 winter reinforcement'),
    ('Live Oak East', 'L14', 'L05', '2025-01-20 14:15:00', '2025-05-14 18:45:00', 'Line 14 pole changeout'),
    ('Bluestem', 'L11', 'L13', '2025-05-12 13:05:00', '2025-08-28 19:30:00', 'Line 11 switch upgrade'),
    ('Caney West', 'L12', 'L14', '2025-06-20 13:15:00', '2025-09-10 18:40:00', 'Line 12 summer tie relief'),
    ('Oyster Ridge', 'L09', 'L03', '2025-09-02 13:50:00', '2025-11-28 18:20:00', 'Line 9 tap inspection'),
    ('Caney West', 'L12', 'L14', '2025-11-18 14:30:00', '2026-02-05 18:15:00', 'Line 12 winter load balance'),
    # 2026 abnormal feeding windows (shift 2026 member-minutes by 20-35% and alter Priority 1 repeat rankings)
    ('Palmetto Shores', 'L02', 'L16', '2026-01-10 14:10:00', '2026-04-28 19:20:00', 'Line 2 winter insulator work'),
    ('Sedge Village', 'L03', 'L09', '2026-01-04 13:25:00', '2026-04-20 18:30:00', 'Line 3 coastal section work'),
    ('Mesquite North', 'L10', 'L15', '2026-02-12 13:45:00', '2026-06-18 18:35:00', 'Inland corridor double-circuit work'),
    ('Coloma', 'L05', 'L14', '2026-03-16 13:20:00', '2026-06-22 19:10:00', 'Line 5 structure work'),
    ('Caney Mill', 'L08', 'L14', '2026-04-06 13:30:00', '2026-08-25 18:50:00', 'Line 8 BESS tie check'),
    ('Heron Bend', 'L06', 'L16', '2026-05-20 13:15:00', '2026-08-28 19:05:00', 'Line 6 summer clearance relief'),
    ('Live Oak East', 'L14', 'L05', '2026-06-26 12:55:00', '2026-10-15 18:40:00', 'Line 14 summer load relief'),
    ('Mesquite South', 'L15', 'L12', '2026-07-02 13:05:00', '2026-10-22 18:25:00', 'Line 15 thermal relief'),
    ('Bluestem', 'L11', 'L13', '2026-08-15 14:00:00', '2026-10-25 19:00:00', 'Line 11 corridor clearance'),
    ('Beachwood', 'L01', 'L04', '2026-06-01 13:40:00', '2026-09-20 19:05:00', 'Line 1 coastal tie maintenance'),
]


def parsed_switch_windows():
    out = []
    for tap, norm, alt, s0, s1, why in SWITCH_WINDOWS:
        t0 = dt.datetime.strptime(s0, '%Y-%m-%d %H:%M:%S').replace(tzinfo=C.UTC)
        t1 = dt.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S').replace(tzinfo=C.UTC)
        out.append(dict(tap=tap, normal=norm, alt=alt, start=t0, end=t1, reason=why))
    return out


def active_feed_for_tap(tp, t, windows):
    """Returns (active_line, is_switched_abnormal) for tap substation `tp` at aware UTC timestamp `t`."""
    for w in windows:
        if w['tap'] == tp['name'] and w['start'] <= t < w['end']:
            return w['alt'], True
    return tp['line'], False


def _breakers(net):
    out = {}
    for lid, line in net['lines'].items():
        n = int(lid[1:])
        out[(lid, 'a')] = '%s-%s' % (line['a'], 'B%d%02d' % (52, n))
        out[(lid, 'b')] = '%s-%s' % (line['b'], 'B%d%02d' % (62, n))
    return out


def members_at(net, tap, t):
    months = (2026 - t.year) * 12 + (10 - t.month)
    return int(round(tap['members'] / (1.0 + 0.0013) ** max(months, 0)))


def operate(w):
    net = w['net']
    rng = np.random.default_rng(C.EV_SEED + 505)
    brk = _breakers(net)
    windows = parsed_switch_windows()
    w['switch_windows'] = windows
    soe, impacts = [], []
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
        # Determine taps actually energized by f['line'] at t0 (live as-operated topology!)
        live_taps = []
        for tp in net['taps']:
            feed_line, is_abn = active_feed_for_tap(tp, t0, windows)
            if feed_line == f['line']:
                live_taps.append((tp, is_abn))
        normal_taps = [tp for tp in net['taps'] if tp['line'] == f['line']]
        if perm:
            fast = any(tp['moab'] for tp in normal_taps) or not normal_taps
            mins = rng.uniform(*SCADA_SPEED) if fast else rng.uniform(*CREW_SPEED)
            t_sect = t_trip + dt.timedelta(minutes=float(mins))
            pts = sorted([0.0] + [tp['km'] for tp in normal_taps] + [line['length']])
            lo = max(p for p in pts if p <= f['km'])
            hi = min(p for p in pts if p >= f['km'])
            sw_ops = []
            for k in (lo, hi):
                if 0.0 < k < line['length']:
                    tp = [x for x in normal_taps if x['km'] == k][0]
                    sw_ops.append((t_sect - dt.timedelta(seconds=float(rng.uniform(20, 90))), tp['name'], k))
            for (ts, name, k) in sw_ops:
                side = 'S1' if k == lo else 'S2'
                ev['ops'].append((ts, 'SW', '%s %s' % (name.upper()[:10].replace(' ', ''), side), 'OPEN'))
            ev['closed_ends'] = []
            for end in ('a', 'b'):
                if (end == 'a' and lo == 0.0) or (end == 'b' and hi == line['length']):
                    continue
                b = brk[(f['line'], end)]
                ev['ops'].append((t_sect + dt.timedelta(seconds=float(rng.uniform(5, 50))), line[end], b, 'CLOSE'))
                ev['closed_ends'].append(end)
            ev['t_sect'] = t_sect
            line_back = t_sect
            t_rep = t_sect + dt.timedelta(hours=float(rng.uniform(2.5, 11.0)))
            for end in ('a', 'b'):
                if end not in ev['closed_ends']:
                    b = brk[(f['line'], end)]
                    ev['ops'].append((t_rep + dt.timedelta(seconds=float(rng.uniform(310, 900))), line[end], b, 'CLOSE'))
            for (ts, name, k) in sw_ops:
                side = 'S1' if k == lo else 'S2'
                ev['ops'].append((t_rep + dt.timedelta(seconds=float(rng.uniform(0, 300))), 'SW',
                                  '%s %s' % (name.upper()[:10].replace(' ', ''), side), 'CLOSE'))
            ev['t_rep'] = t_rep
        imp = []
        for tp, is_abn in live_taps:
            m = members_at(net, tp, t0)
            if not perm:
                out_s = (line_back - t0).total_seconds()
                imp.append(dict(tap=tp['name'], members=m, seconds=out_s, how='reclose', abnormal=is_abn))
                continue
            # If the tap is already running abnormally on its alternate line (normal line out for maintenance),
            # NO transfer back is available -> it waits for the faulted line's sectionalizing/reclose restoration!
            if (not is_abn) and tp['backup'] == 'auto':
                imp.append(dict(tap=tp['name'], members=m, seconds=AUTO_XFER + float(rng.uniform(0, 4)),
                                how='auto transfer', abnormal=False))
                ev['ops'].append((t0 + dt.timedelta(seconds=AUTO_XFER), 'XFER',
                                  '%s ALT %s' % (tp['name'].upper()[:10].replace(' ', ''), tp['alt']), 'CLOSE'))
                continue
            closes = [o[0] for o in ev['ops'] if o[3] == 'CLOSE' and o[1] in (line['a'], line['b'])
                      and o[0] > t0 + dt.timedelta(seconds=60)]
            t_rest = min(closes) if closes else ev['t_sect']
            how = 'line reclosed after isolation'
            if (not is_abn) and tp['backup'] == 'manual':
                t_man = t_trip + dt.timedelta(minutes=float(rng.uniform(7, 19)))
                if t_man < t_rest:
                    t_rest = t_man
                    how = 'manual transfer'
                    ev['ops'].append((t_man, 'XFER', '%s ALT %s' % (tp['name'].upper()[:10].replace(' ', ''), tp['alt']), 'CLOSE'))
            imp.append(dict(tap=tp['name'], members=m, seconds=(t_rest - t0).total_seconds(), how=how, abnormal=is_abn))
        ev['impact'] = imp
        f['ops'] = ev
        soe.extend(ev['ops'])
        impacts.append(dict(fault=f['id'], line=f['line'], t0=t0, impact=imp, perm=perm))
    w['soe_fault_ops'] = soe
    w['impacts'] = impacts
    return w
