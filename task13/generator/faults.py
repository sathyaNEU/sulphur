"""Every 69 kV fault from January 2022 to October 2026, each from the process that makes it:
lightning where a stroke lands near the line; bird streamers at the structures waterbirds and vultures roost on, on
roost-season nights, until perch guards go on; fog flashovers on porcelain near the Gulf when local fog meets a salt
deposit built up since the last wash or soaking rain; cracked porcelain bells that flash over in light rain at any
hour, faster as the crack grows, until a permanent failure gets the string replaced; grow-in contacts where a tree
under the line meets the conductor once it sags hot on a still afternoon, until the span is trimmed; limbs and trees
blown into the line from outside the right of way in gusts (two stands of dead pines along the inland lines do it
again and again); and vehicles, hardware and causes nobody finds. Each fault carries its true time, place, phases,
fault resistance and whether it cleared on reclose."""
import datetime as dt
import math

import numpy as np
from scipy.spatial import cKDTree

import common as C
import network as N
import weather as W
import loads as L

# fault resistance by cause (ohm): arcs across insulators and streamers are low, tree contacts high
RF = {'lightning': (6.0, 28.0), 'bird': (0.8, 3.2), 'fog': (1.5, 4.5), 'insulator': (0.3, 0.9),
      'growin': (14.0, 38.0), 'fallin': (3.0, 22.0), 'vehicle': (0.5, 4.0), 'hardware': (0.5, 3.0),
      'unknown': (0.8, 9.0)}

# roost structures: line, structure no., the survey site, birds in a typical winter, guards fitted (UTC) or None
ROOSTS = [
    ('L07', 31, 'RS-03', 180, None),
    ('L07', 38, 'RS-04', 130, dt.datetime(2024, 11, 14, 17, 0, tzinfo=C.UTC)),
    ('L07', 52, 'RS-06', 150, None),
    ('L16', 23, 'RS-09', 170, None),
    ('L06', 79, 'RS-11', 90, None),
    ('L12', 96, 'RS-15', 190, dt.datetime(2024, 11, 20, 16, 0, tzinfo=C.UTC)),
    ('L12', 104, 'RS-16', 140, None),
    ('L14', 118, 'RS-19', 120, None),
]
# cracked strings: line, structure no., onset (UTC), hazard at onset per light-rain hour, e-folding days
CRACKED = [
    # line, structure no., onset (UTC), hazard at onset per light-rain hour, e-folding days, fails for good
    ('L02', 63, dt.datetime(2024, 9, 10, tzinfo=C.UTC), 0.020, 520.0, False),
    ('L05', 88, dt.datetime(2024, 5, 20, tzinfo=C.UTC), 0.017, 560.0, False),
    ('L15', 57, dt.datetime(2025, 1, 15, tzinfo=C.UTC), 0.018, 480.0, False),
    ('L09', None, dt.datetime(2024, 2, 5, tzinfo=C.UTC), 0.013, 520.0, False),   # beyond the solar tap
    ('L03', 41, dt.datetime(2023, 6, 1, tzinfo=C.UTC), 0.024, 400.0, True),       # fails for good, replaced
    ('L13', 72, dt.datetime(2022, 2, 1, tzinfo=C.UTC), 0.030, 300.0, True),       # fails for good, replaced
    ('L01', 49, dt.datetime(2022, 3, 1, tzinfo=C.UTC), 0.030, 300.0, True),       # fails for good, replaced
]
TAP_STRING_KM = 26.65            # the cracked string on Shell Ridge-Ponder Creek, 3.25 km beyond the solar tap
# grow-in spans: line, back structure no., contact temperature in May 2022 (deg C), trimmed for the cycle (UTC)
GROWIN = [
    # line, back structure no., contact temperature in May 2022 (deg C), cycle trims (UTC, deg C the trim buys)
    ('L10', 47, 51.0, [(dt.datetime(2024, 2, 13, 15, 0, tzinfo=C.UTC), 5.0)]),    # contacts 2022-23, again 2025-26
    ('L10', 88, 55.0, []),
    ('L14', 62, 57.0, []),
    ('L14', 131, 57.5, []),
    ('L12', 44, 54.5, []),
    ('L06', 57, 48.5, []),
    ('L05', 101, 53.5, []),
    ('L15', 33, 55.0, [(dt.datetime(2025, 2, 11, 15, 0, tzinfo=C.UTC), 25.0)]),   # cleared in the 2025 cycle
    ('L11', 64, 55.5, []),
]
GROWTH_C = 2.0          # deg C a year the trees take off the contact temperature
# dead pine stands outside the right of way (line, structure no. range) that drop limbs in gusts
DANGER = [('L13', 104, 106, 0.30, 0.0006), ('L11', 118, 120, 0.04, 0.0016)]   # summer storm and winter front odds
GULF_LINES = ('L01', 'L02', 'L03', 'L04')


_SOURCES = []


def _near_source(lid, km, tol):
    return any(l == lid and abs(k - km) <= tol for l, k in _SOURCES)


def _utc_from_local(d, lh):
    t = dt.datetime(d.year, d.month, d.day) + dt.timedelta(hours=lh)
    try:
        return C.local(t).astimezone(C.UTC)
    except Exception:
        return (C.local(t) + dt.timedelta(hours=1)).astimezone(C.UTC)


def _structure_xy(net):
    pts, keys = [], []
    for lid, line in net['lines'].items():
        for st in line['structures']:
            pts.append((st['x'], st['y']))
            keys.append((lid, st['no']))
    return np.array(pts), keys


def onshore_factor(month):
    """the Gulf wind's share of the year: strongest in spring and summer, weakest in early autumn"""
    return {3: 1.25, 4: 1.25, 5: 1.25, 6: 1.25, 7: 1.25, 8: 1.25, 9: 0.9, 10: 0.9}.get(month, 1.0)


def rain_keep(mm):
    for lim, keep in RAIN_KEEP:
        if mm >= lim:
            return keep
    return 1.0


def wash_sections(net):
    """the washing crews' sections on the Gulf lines: about 3.5 km of porcelain each"""
    secs = []
    for lid in GULF_LINES:
        sts = [s for s in net['lines'][lid]['structures'] if s['insulator'] == 'porcelain' and s['shore_km'] <= 6.0]
        if not sts:
            continue
        k0 = sts[0]['km']
        cur = []
        for s in sts:
            if cur and s['km'] - k0 > 3.4:
                secs.append(cur)
                cur, k0 = [], s['km']
            cur.append(s)
        if cur:
            secs.append(cur)
    out = []
    for i, ss in enumerate(secs):
        out.append(dict(id='%s-W%d' % (ss[0]['line'], sum(1 for o in out if o['line'] == ss[0]['line']) + 1),
                        line=ss[0]['line'], s0=ss[0]['no'], s1=ss[-1]['no'], km0=ss[0]['km'], km1=ss[-1]['km'],
                        shore=float(np.mean([s['shore_km'] for s in ss]))))
    return out


def deposit_rate(shore_km, onshore=1.0):
    """salt deposit accumulation, mg per cm2 per day, falling off with distance from the Gulf"""
    return 0.0042 * math.exp(-shore_km / 1.8) * onshore + 0.00005


RAIN_KEEP = ((12.0, 0.50), (5.0, 0.85))      # a soaking rain leaves half the deposit, a moderate one 85 per cent


def _storm_near(wx, x, y, h, radius, n=3):
    """a thunderstorm at a place in simulation hour h: n or more cloud-to-ground strokes within radius km that hour"""
    idx = wx.get('stroke_hour_index')
    if idx is None:
        idx = {}
        for (i, lh, sx, sy, ka) in wx['strokes']:
            t = _utc_from_local(wx['days'][i], lh)
            idx.setdefault(C.hour_index(t), []).append((sx, sy))
        wx['stroke_hour_index'] = idx
    cnt = 0
    for sx, sy in idx.get(h, ()):
        if (sx - x) ** 2 + (sy - y) ** 2 <= radius * radius:
            cnt += 1
            if cnt >= n:
                return True
    return False


def _benign(wx, x, y, h):
    """an hour with nothing in the weather to explain a fault: not a summer afternoon, no fog, rain, front or storm"""
    lh, mo = wx['hour'][h], wx['month'][h]
    if mo in (5, 6, 7, 8, 9, 10) and 12 <= lh <= 20:
        return False
    if wx['front'][wx['hday'][h]] > 1.0 or wx.get('fog_index', {}).get(h):
        return False
    code = min(W.PLACES, key=lambda c: math.hypot(W.PLACES[c][0] - x, W.PLACES[c][1] - y))
    if wx['series'][code]['precip'][h] > 0.05:
        return False
    if _storm_near(wx, x, y, h, 25.0):
        return False
    return True


def _random_km(net, rng, faults, cause, lid):
    """a random place on a line clear of the designed sources and of another fault of the same cause"""
    line = net['lines'][lid]
    for _ in range(60):
        km = float(rng.uniform(0.3, line['length'] - 0.3))
        if _near_source(lid, km, 0.8):
            continue
        if any(f['line'] == lid and f['cause'] == cause and abs(f['km'] - km) <= 1.0 for f in faults):
            continue
        return km
    return None


def _random_place(net, rng, faults, cause):
    while True:
        lid = list(net['lines'])[int(rng.integers(0, 16))]
        km = _random_km(net, rng, faults, cause, lid)
        if km is not None:
            return lid, km


def simulate(net, wx, ld, washes):
    streams = {k: np.random.default_rng(C.EV_SEED * 101 + i) for i, k in
               enumerate(['add', 'lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin', 'random'])}
    rng = streams['add']
    nh = C.NH
    h_rec0 = C.hour_index(C.REC0)
    faults = []
    del _SOURCES[:]
    for lid, no, *_ in ROOSTS:
        _SOURCES.append((lid, net['lines'][lid]['structures'][no - 1]['km']))
    for lid, no, *_ in CRACKED:
        _SOURCES.append((lid, TAP_STRING_KM if no is None else net['lines'][lid]['structures'][no - 1]['km']))
    for lid, no, *_ in GROWIN:
        _SOURCES.append((lid, net['lines'][lid]['structures'][no - 1]['km']))
    for lid, a, b, *_ in DANGER:
        _SOURCES.append((lid, (net['lines'][lid]['structures'][a - 1]['km'] + net['lines'][lid]['structures'][b - 1]['km']) / 2))

    def add(h, sec, lid, km, cause, perm, phases=None, rf=None, extra=None):
        rng = streams[{'lightning': 'lightning', 'bird': 'bird', 'fog': 'fog', 'insulator': 'insulator', 'growin': 'growin',
                       'fallin': 'fallin'}.get(cause, 'random')]
        km = min(max(float(km), 0.03), net['lines'][lid]['length'] - 0.03)
        st = N.structure_at(net, lid, km)
        if phases is None:
            phases = [['A', 'B', 'C'][int(rng.integers(0, 3))]]
        lo, hi = RF[cause]
        f = dict(t=C.ts_of(h, sec), h=int(h), line=lid, km=float(km), structure=st['no'], cause=cause,
                 permanent=bool(perm), phases=phases, rf=float(rf if rf is not None else rng.uniform(lo, hi)))
        if extra:
            f.update(extra)
        faults.append(f)
        return f

    rng = streams['lightning']
    # ---- lightning: strokes within 120 m of a line flash over with a chance that rises with the current
    pts, keys = _structure_xy(net)
    tree = cKDTree(pts)
    days = wx['days']
    for (i, lh, x, y, ka) in wx['strokes']:
        d, j = tree.query((x, y))
        if d > 0.25:
            continue
        lid, no = keys[j]
        line = net['lines'][lid]
        # perpendicular distance to the span: approximate by the distance to the nearest structure
        if d > 0.12:
            continue
        p = (1.0 - math.exp(-(abs(ka) / 38.0) ** 2)) * (0.45 if d < 0.05 else 0.18)
        if rng.random() < p:
            t = _utc_from_local(days[i], lh)
            h = C.hour_index(t)
            if h < 0 or h >= nh:
                continue
            km = line['structures'][no - 1]['km'] + rng.normal(0, 0.04)
            km = min(max(km, 0.05), line['length'] - 0.05)
            sec = (t - C.ts_of(h)).total_seconds()
            ph = [['A', 'B', 'C'][int(rng.integers(0, 3))]]
            if rng.random() < 0.18:
                ph = sorted(rng.choice(['A', 'B', 'C'], 2, replace=False).tolist())
            near = [f for f in faults if f['cause'] == 'lightning' and f['line'] == lid and abs(f['km'] - km) <= 1.0]
            if len(near) >= 1 or _near_source(lid, km, 0.6):
                continue
            add(h, sec, lid, km, 'lightning', rng.random() < 0.10, ph, rf=(float(rng.uniform(0.8, 3.0)) if len(ph) == 2 else None),
                extra=dict(stroke_ka=ka, stroke=(i, lh, x, y)))

    rng = streams['bird']
    # ---- bird streamers at roost structures, roost season nights (November to March), 01:00 to 06:30 local
    hour = wx['hour']
    month = wx['month']
    for lid, no, site, birds, guarded in ROOSTS:
        st = net['lines'][lid]['structures'][no - 1]
        lam = 0.0105 * birds / 100.0
        for di, d in enumerate(days):
            if d.month not in (11, 12, 1, 2, 3):
                continue
            season_birds = 0.75 + 0.5 * ((d.year * 7 + sum(ord(ch) for ch in site) % 11) % 5) / 4.0
            if wx['front'][di] > 2.5:
                continue
            if rng.random() < lam * season_birds:
                lh = rng.uniform(1.0, 6.5)
                t = _utc_from_local(d + dt.timedelta(days=1) if lh < 0 else d, lh)
                if guarded is not None and t >= guarded:
                    continue
                h = C.hour_index(t)
                if 0 <= h < nh:
                    outer = ['A', 'C'][int(rng.integers(0, 2))]
                    add(h, (t - C.ts_of(h)).total_seconds(), lid, st['km'] + rng.normal(0, 0.01), 'bird',
                        rng.random() < 0.03, [outer], extra=dict(roost=site))
    rng = streams['bird']
    # a few birds elsewhere (a hawk on a crossarm, a heron in flight)
    for _ in range(6):
        lid, km = _random_place(net, rng, faults, 'bird')
        h = int(rng.integers(h_rec0, nh))
        add(h, rng.uniform(0, 3600), lid, km, 'bird', rng.random() < 0.2)

    rng = streams['fog']
    # ---- salt deposits and fog flashovers on the Gulf lines' porcelain
    wash_by_line = {}
    for w in washes:
        wash_by_line.setdefault(w['line'], []).append(w)
    rain_codes = {'L01': ('PAL', 'APT'), 'L02': ('PAL', 'SHR'), 'L03': ('SHR', 'SED'), 'L04': ('APT', 'PAL')}
    drains = {c: W.daily_rain(wx, c) for c in ('APT', 'PAL', 'SHR', 'SED')}
    deposit_hist = {}
    fog_index = wx['fog_index']
    for lid in GULF_LINES:
        line = net['lines'][lid]
        sts = [s for s in line['structures'] if s['insulator'] == 'porcelain' and s['shore_km'] <= 6.0]
        rain = (drains[rain_codes[lid][0]] + drains[rain_codes[lid][1]]) / 2.0
        dep = np.zeros(len(sts))
        rates = np.array([deposit_rate(s['shore_km']) for s in sts])
        dep[:] = rates * 60.0
        series = np.zeros((len(days), len(sts)))
        wash_days = {}
        for w in washes:
            if w['line'] != lid:
                continue
            di = days.index(w['date']) if w['date'] in days else None
            if di is not None:
                wash_days.setdefault(di, []).append(w)
        for di, d in enumerate(days):
            onshore = onshore_factor(d.month)
            dep += rates * onshore
            dep *= rain_keep(rain[di])
            for w in wash_days.get(di, ()):
                for k, s in enumerate(sts):
                    if w['s0'] <= s['no'] <= w['s1']:
                        dep[k] = 0.003
            series[di] = dep
        deposit_hist[lid] = (sts, series, rates)
        # fog hours: each structure in a fog patch with a deposit past the porcelain's flashover level may flash over
        crit = 0.052
        last_fault_h = -999
        for h in range(nh):
            evs = fog_index.get(h)
            if not evs:
                continue
            lh = hour[h]
            if not (lh >= 22 or lh <= 9):
                continue
            di = wx['hday'][h]
            haz = []
            for k, s in enumerate(sts):
                if not W.fog_at(wx, s['x'], s['y'], h):
                    continue
                excess = series[di, k] / crit - 1.0
                if excess > 0:
                    haz.append((0.020 * min(excess, 2.5), s))
            if not haz or h - last_fault_h < 2:
                continue
            p_tot = 1.0 - math.exp(-sum(p for p, _ in haz))
            if rng.random() < p_tot:
                ps = np.array([p for p, _ in haz])
                s = haz[int(rng.choice(len(haz), p=ps / ps.sum()))][1]
                f = add(h, rng.uniform(0, 3600), lid, s['km'] + rng.normal(0, 0.01), 'fog', rng.random() < 0.04,
                        extra=dict(deposit=float(series[di, sts.index(s)])))
                last_fault_h = h

    rng = streams['insulator']
    # ---- cracked strings: flash over in light rain at any hour, faster as the crack grows
    st_places = {}
    replaced = {}
    for lid, no, onset, haz0, efold, fails in CRACKED:
        line = net['lines'][lid]
        st = N.structure_at(net, lid, TAP_STRING_KM) if no is None else line['structures'][no - 1]
        code = min(W.PLACES, key=lambda c: math.hypot(W.PLACES[c][0] - st['x'], W.PLACES[c][1] - st['y']))
        pr = wx['series'][code]['precip']
        h0 = max(C.hour_index(onset), 0)
        n_here = 0
        quiet_until = -1
        for h in range(h0, nh):
            if pr[h] < 0.25 or pr[h] >= 2.5 or h < quiet_until:
                continue
            if wx['front'][wx['hday'][h]] > 1.5 or _storm_near(wx, st['x'], st['y'], h, 15.0):
                continue
            age = (h - h0) / 24.0
            if rng.random() < haz0 * math.exp(age / efold):
                n_here += 1
                perm = fails and n_here >= 4
                add(h, rng.uniform(0, 3600), lid, st['km'] + rng.normal(0, 0.01), 'insulator', perm,
                    extra=dict(string=st['no']))
                quiet_until = h + 48
                if perm:
                    replaced[(lid, st['no'])] = C.ts_of(h) + dt.timedelta(hours=float(rng.uniform(5, 30)))
                    break
        st_places[(lid, st['no'])] = st

    rng = streams['growin']
    # ---- grow-in contacts: the conductor hot and sagged on a still afternoon reaches the tree
    trims = {}
    for lid, back_no, t0c, cycle in GROWIN:
        line = net['lines'][lid]
        s0 = line['structures'][back_no - 1]
        s1 = line['structures'][back_no]
        km = (s0['km'] + s1['km']) / 2.0
        code = min(W.PLACES, key=lambda c: math.hypot(W.PLACES[c][0] - s0['x'], W.PLACES[c][1] - s0['y']))
        temp = wx['series'][code]['temp']
        wind = wx['series'][code]['wind']
        amps = ld['amps'][lid]
        prc = wx['series'][code]['precip']
        cand = [h for h in range(h_rec0, nh) if 12 <= hour[h] <= 19 and month[h] in (5, 6, 7, 8, 9, 10)
                and prc[h] < 0.1 and not _storm_near(wx, s0['x'], s0['y'], h, 15.0)]
        raise_c = 0.0
        refractory = -1
        done = False
        for h in cand:
            t = C.ts_of(h)
            raise_c = sum(r for (td, r) in cycle if t >= td)
            if done:
                break
            tcontact = t0c - GROWTH_C * (wx['year'][h] - 2022) + raise_c
            if h < refractory:
                continue
            tc = L.conductor_temp(float(amps[h]), line['conductor'], float(temp[h]), float(wind[h]),
                                  L.solar_irradiance(h, wx, code))
            if tc >= tcontact and rng.random() < 0.20:
                perm = rng.random() < 0.06
                add(h, rng.uniform(0, 3600), lid, km + rng.normal(0, 0.02), 'growin', perm,
                    extra=dict(span=(s0['no'], s1['no']), tc=tc))
                refractory = h + 24 * 21
                if perm:
                    trims[(lid, s0['no'])] = t + dt.timedelta(days=float(rng.uniform(1, 4)))
                    done = True
        for (td, r) in cycle:
            trims.setdefault((lid, s0['no']), td)

    rng = streams['fallin']
    # ---- limbs and trees blown in: the two dead pine stands, in winter fronts and under summer storm cells
    front = wx['front']
    for lid, a, b, p_storm, p_front in DANGER:
        line = net['lines'][lid]
        st = line['structures'][a - 1]
        last = -999
        for h in range(h_rec0, nh):
            if h - last < 72:
                continue
            di = wx['hday'][h]
            p = 0.0
            if front[di] > 4.0 and 8 <= hour[h] <= 20:
                p = p_front * (front[di] - 3.5)
            elif month[h] in (5, 6, 7, 8, 9) and _storm_near(wx, st['x'], st['y'], h, 4.0, 4):
                p = p_storm
            if p and rng.random() < p:
                k = rng.uniform(line['structures'][a - 1]['km'], line['structures'][b - 1]['km'])
                add(h, rng.uniform(0, 3600), lid, k, 'fallin', rng.random() < 0.20, extra=dict(stand='%s %d-%d' % (lid, a, b)))
                last = h
    for lid, line in net['lines'].items():
        mid = line['structures'][len(line['structures']) // 2]
        for h in range(h_rec0, nh):
            di = wx['hday'][h]
            p = 0.0
            if front[di] > 7.0 and 8 <= hour[h] <= 20:
                p = 0.0011 * line['length'] / 25.0 * (front[di] - 6.5)
            elif month[h] in (5, 6, 7, 8, 9) and 12 <= hour[h] <= 20 and rng.random() < 0.05 and _storm_near(wx, mid['x'], mid['y'], h, 10.0, 6):
                p = 0.10
            if p and rng.random() < p:
                km = _random_km(net, rng, faults, 'fallin', lid)
                if km is not None:
                    add(h, rng.uniform(0, 3600), lid, km, 'fallin', rng.random() < 0.5)

    rng = streams['random']
    # ---- vehicles, hardware and causes nobody finds
    for cause, n, perm_p in (('vehicle', 11, 1.0), ('hardware', 14, 0.85), ('unknown', 30, 0.08)):
        for _ in range(n):
            lid, km = _random_place(net, rng, faults, cause)
            st = N.structure_at(net, lid, km)
            while True:
                h = int(rng.integers(h_rec0, nh))
                if _benign(wx, st['x'], st['y'], h):
                    break
            add(h, rng.uniform(0, 3600), lid, km, cause, rng.random() < perm_p)

    rng = streams['add']
    faults = [f for f in faults if C.REC0 <= f['t'] < C.T_END]
    faults.sort(key=lambda f: f['t'])
    # one fault per line at a time: a second initiation on the same line within two minutes is dropped
    keep, last = [], {}
    for f in faults:
        if f['line'] in last and (f['t'] - last[f['line']]).total_seconds() < 120:
            continue
        keep.append(f)
        last[f['line']] = f['t']
    for k, f in enumerate(keep):
        f['id'] = k + 1
    return dict(faults=keep, deposits=deposit_hist, replaced=replaced, trims=trims, strings=st_places)
