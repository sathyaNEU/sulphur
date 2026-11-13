"""The weather, lightning, loading and field files: the two airports' hourly observations as the ASOS feed gives them
(degrees Fahrenheit, knots, statute miles, inches), the cooperative's own substation weather stations (from March
2023, metric, local prevailing time, with their gaps), the lightning network's strokes within 3 km of the 69 kV
lines, the SCADA historian's hourly line loading, the environmental team's roost survey, the test insulator deposits,
the insulator washing log, the solar farm's own protection event export, and the work management system's
maintenance and vegetation orders."""
import csv
import datetime as dt
import math

import numpy as np
from scipy.spatial import cKDTree

import common as C
import faults as F
import network as N
import weather as W

LAT0, LON0 = 28.18, -97.02


def latlon(x, y):
    return LAT0 + y / 110.95, LON0 + x / (111.32 * math.cos(math.radians(LAT0)))


def _f(c):
    return c * 9.0 / 5.0 + 32.0


def asos_rows(wx, code, rng):
    s = wx['series'][code]
    rows = []
    for h in range(C.hour_index(C.REC0), C.NH):
        if rng.random() < 0.004:
            continue
        t = C.ts_of(h, 53 * 60)
        temp, dew = s['temp'][h], s['dew'][h]
        rh = 100.0 * math.exp(17.625 * dew / (243.04 + dew)) / math.exp(17.625 * temp / (243.04 + temp))
        rain = s['precip'][h]
        fog = temp - dew < 0.35
        if fog:
            vis = float(rng.choice([0.12, 0.25, 0.25, 0.5, 0.75]))
        elif rh > 92 or rain > 2.0:
            vis = float(rng.choice([2.0, 3.0, 4.0, 5.0, 7.0]))
        else:
            vis = 10.0
        codes = []
        if rain >= 0.25:
            codes.append(('-' if rain < 2.5 else ('' if rain < 7.6 else '+')) + ('TSRA' if s['gust'][h] > 14 and rain > 3 else 'RA'))
        elif rain > 0.05:
            codes.append('-DZ')
        if fog:
            codes.append('FG')
        elif vis < 7:
            codes.append('BR')
        rows.append([t.strftime('%Y-%m-%d %H:%M'), round(_f(temp), 1), round(_f(dew), 1), round(min(rh, 100.0), 2),
                     int(round(s['wdir'][h] / 10.0) * 10) % 360, int(round(s['wind'][h] * 1.94384)),
                     (int(round(s['gust'][h] * 1.94384)) if s['gust'][h] > 8.0 else 'M'), vis,
                     ('T' if 0 < rain < 0.25 else round(rain / 25.4, 2)), ' '.join(codes) or 'M'])
    return rows


def write_asos(rows, path, station):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['station', 'valid', 'tmpf', 'dwpf', 'relh', 'drct', 'sknt', 'gust', 'vsby', 'p01i', 'wxcodes'])
        for r in rows:
            wr.writerow([station] + r)
    return len(rows)


def station_rows(wx, rng):
    rows = []
    start = {'PAL': C.STATIONS_FROM, 'SHR': C.STATIONS_FROM, 'TUL': C.STATIONS_FROM,
             'SED': C.STATIONS_FROM + dt.timedelta(days=41), 'CAN': C.STATIONS_FROM + dt.timedelta(days=9),
             'MSQ': C.STATIONS_FROM + dt.timedelta(days=96)}
    names = {'PAL': 'PORT ALCORN SUB', 'SHR': 'SHELL RIDGE SUB', 'SED': 'SEDGE POINT SUB', 'TUL': 'TULE MARSH SUB',
             'CAN': 'CANEY BEND SUB', 'MSQ': 'MESQUITE FLAT SUB'}
    for code in W.STATION_CODES:
        s = wx['series'][code]
        gap_until = -1
        for h in range(C.hour_index(start[code]), C.NH):
            if h < gap_until:
                continue
            if rng.random() < 0.0008:
                gap_until = h + int(rng.integers(3, 36))      # a logger or radio outage
                continue
            t = C.to_local(C.ts_of(h))
            temp = s['temp'][h] + rng.normal(0, 0.15)
            dew = min(s['dew'][h] + rng.normal(0, 0.15), temp + 0.05)
            rh = 100.0 * math.exp(17.625 * dew / (243.04 + dew)) / math.exp(17.625 * temp / (243.04 + temp))
            rows.append([names[code], t.strftime('%Y-%m-%d %H:00'), round(temp, 2), round(min(rh, 100.0), 1),
                         round(dew, 2), round(max(0.0, s['wind'][h] + rng.normal(0, 0.2)), 2), int(s['wdir'][h]) % 360,
                         round(s['precip'][h], 1)])
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def write_stations(rows, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['station', 'hour_local', 'air_temp_c', 'rh_pct', 'dewpoint_c', 'wind_ms', 'wind_dir_deg', 'rain_mm'])
        for r in rows:
            wr.writerow(r)
    return len(rows)


def stroke_rows(w, rng):
    net, wx = w['net'], w['wx']
    w['fault_strokes'] = set(f['stroke'] for f in w['faults'] if f.get('stroke'))
    pts = np.array([(s['x'], s['y']) for s in net['structures']])
    tree = cKDTree(pts)
    days = wx['days']
    rows = []
    by_hour = {}
    for (i, lh, x, y, ka) in wx['strokes']:
        t = F._utc_from_local(days[i], lh)
        h = C.hour_index(t)
        by_hour.setdefault(h, []).append((x, y))
        if not (C.REC0 <= t < C.T_END):
            continue
        d, _ = tree.query((x, y))
        if d > 3.0:
            continue
        if rng.random() < 0.08 and abs(ka) < 15.0 and (i, lh, x, y) not in w['fault_strokes']:
            continue                      # a weak stroke the network did not detect
        semi = float(rng.lognormal(math.log(180.0), 0.45))
        ex, ey = x + rng.normal(0, semi / 1000.0 / 1.4), y + rng.normal(0, semi / 1000.0 / 1.4)
        la, lo = latlon(ex, ey)
        rows.append([t.strftime('%Y-%m-%d %H:%M:%S.') + '%03d' % (t.microsecond // 1000), round(la, 5), round(lo, 5),
                     round(ka, 1), 'CG', int(semi), int(semi * rng.uniform(0.35, 0.8))])
        if rng.random() < 0.35:
            t2 = t + dt.timedelta(milliseconds=float(rng.uniform(5, 400)))
            la2, lo2 = latlon(ex + rng.normal(0, 2.0), ey + rng.normal(0, 2.0))
            rows.append([t2.strftime('%Y-%m-%d %H:%M:%S.') + '%03d' % (t2.microsecond // 1000), round(la2, 5), round(lo2, 5),
                         round(float(rng.normal(0, 6)), 1), 'IC', int(semi * 1.6), int(semi * 0.9)])
    rows.sort(key=lambda r: r[0])
    w['strokes_by_hour'] = by_hour
    return rows


def write_strokes(rows, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['time_utc', 'latitude', 'longitude', 'peak_current_ka', 'type', 'semi_major_m', 'semi_minor_m'])
        for r in rows:
            wr.writerow(r)
    return len(rows)


def loading_rows(w, rng):
    net, ld = w['net'], w['ld']
    lids = sorted(net['lines'])
    head = ['hour_utc']
    for lid in lids:
        st = net['lines'][lid]['a']
        sb = net['lines'][lid]['b']
        head += ['%s_L%d_AMPS' % (st, int(lid[1:])), '%s_L%d_MW' % (st, int(lid[1:])),
                 '%s_L%d_AMPS' % (sb, int(lid[1:])), '%s_L%d_MW' % (sb, int(lid[1:]))]
    rows = [head]
    stuck = {}
    for h in range(C.hour_index(C.REC0), C.NH):
        if rng.random() < 0.0007:
            continue                                  # historian gap
        t = C.ts_of(h)
        row = [t.strftime('%Y-%m-%d %H:00')]
        for lid in lids:
            a = ld['amps'][lid][h]
            mw = ld['mw'][lid][h]
            if lid in stuck and stuck[lid][0] > h:
                a, mw = stuck[lid][1], stuck[lid][2]
            elif rng.random() < 0.0004:
                stuck[lid] = (h + int(rng.integers(4, 60)), a, mw)
            # the far end sees the same current less the taps' share taken along the line, and the power less the losses
            row += [round(float(a), 1), round(float(mw), 2), round(float(a) * (0.93 + 0.04 * rng.random()), 1),
                    round(float(mw) * (-0.985), 2)]
        rows.append(row)
    return rows


def write_rows(rows, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        for r in rows:
            wr.writerow(r)
    return len(rows) - 1


# ------------------------------------------------------------------------------------------------ the roost survey

OTHER_SITES = [
    ('RS-01', 'Mud Island rookery', (64.5, 38.8), 'marsh island', 'Great Blue Heron; Great Egret'),
    ('RS-02', 'Caney oak motte', (58.4, 43.1), 'live oak motte', 'Black Vulture; Turkey Vulture'),
    ('RS-05', 'Tule Point flats', (66.9, 33.0), 'tidal flat', 'Double-crested Cormorant'),
    ('RS-07', 'Port Alcorn water tower', (77.1, 28.4), 'water tower', 'Black Vulture'),
    ('RS-08', 'Gull Harbor jetty', (86.8, 40.1), 'rock jetty', 'Brown Pelican; Double-crested Cormorant'),
    ('RS-10', 'Bayside cell tower', (61.0, 16.2), 'communications tower', 'Turkey Vulture'),
    ('RS-12', 'County landfill west cell', (41.7, 41.0), 'landfill edge', 'Black Vulture'),
    ('RS-13', 'Sandhill pecan orchard', (44.0, 40.2), 'orchard', 'Black Vulture; Turkey Vulture'),
    ('RS-14', 'Mesquite Flat grain elevator', (36.6, 44.6), 'grain elevator', 'Turkey Vulture'),
    ('RS-17', 'Live Oak Crossing church', (39.4, 22.6), 'steeple', 'Black Vulture'),
    ('RS-18', 'Coloma creek bottom', (47.9, 24.8), 'riparian woods', 'Wood Stork; Great Egret'),
    ('RS-20', 'Redfish Pass dunes', (55.6, 4.9), 'dune scrub', 'Brown Pelican'),
    ('RS-21', 'Inland reservoir dam', (19.4, 49.8), 'dam spillway', 'Double-crested Cormorant'),
    ('RS-22', 'Granger Gap stock tank', (22.6, 30.1), 'stock tank', 'Great Blue Heron'),
]
ROOST_SPECIES = {'RS-03': 'Double-crested Cormorant; Great Blue Heron', 'RS-04': 'Double-crested Cormorant',
                 'RS-06': 'Great Blue Heron; Great Egret', 'RS-09': 'Brown Pelican; Double-crested Cormorant',
                 'RS-11': 'Great Blue Heron', 'RS-15': 'Black Vulture; Turkey Vulture', 'RS-16': 'Black Vulture',
                 'RS-19': 'Turkey Vulture'}


def avian_rows(w, rng):
    net = w['net']
    sites = []
    for lid, no, site, birds, guarded in F.ROOSTS:
        st = net['lines'][lid]['structures'][no - 1]
        x, y = st['x'] + rng.normal(0, 0.012), st['y'] + rng.normal(0, 0.012)
        hab = 'transmission structure (69 kV)' if st['kind'] != 'wood single pole' else 'utility pole (69 kV)'
        note = str(rng.choice(['roosting on crossarms', 'roosting on the 69 kV structure', 'night roost, birds on the H-frame',
                               'roost on co-op line, structure no. not read']))
        sites.append((site, 'roost %s' % site[-2:], (x, y), hab, ROOST_SPECIES[site], birds, note))
    for site, name, xy, hab, sp in OTHER_SITES:
        sites.append((site, name, xy, hab, sp, int(rng.integers(30, 260)), ''))
    rows = []
    observers = ['J. Choi', 'J. Choi', 'T. Nash (consultant)', 'J. Choi']
    for winter in range(2021, 2026):
        for mo, dy in ((12, 8), (1, 12), (2, 9)):
            yr = winter if mo == 12 else winter + 1
            d = dt.date(yr, mo, int(dy + rng.integers(-3, 4)))
            for site, name, (x, y), hab, sp, birds, note in sorted(sites):
                season = 0.75 + 0.5 * ((winter * 7 + sum(ord(ch) for ch in site) % 11) % 5) / 4.0
                count = int(max(0, rng.poisson(birds * season * rng.uniform(0.6, 1.2))))
                la, lo = latlon(x, y)
                rows.append([site, name, round(la, 5), round(lo, 5), hab, sp, d, count,
                             str(rng.choice(observers)), note if count else 'no birds present'])
        d = dt.date(winter, 10, int(rng.integers(14, 26)))
        for site, name, (x, y), hab, sp, birds, note in sorted(sites):
            la, lo = latlon(x, y)
            rows.append([site, name, round(la, 5), round(lo, 5), hab, sp, d, int(rng.poisson(birds * 0.2)),
                         str(rng.choice(observers)), 'fall count'])
    rows.sort(key=lambda r: (r[6], r[0]))
    return rows


# ------------------------------------------------------------------------------------------------ solar farm export

def ipp_rows(w, rng):
    rows = []
    eid = 70412
    for f in w['faults']:
        rec = f['records'].get('ipp')
        if not rec or len(f['phases']) > 1 and rec['IG'] < 50:
            continue
        if rec['IG'] < 120:
            continue
        t = C.to_cst(rec['t'])
        eid += int(rng.integers(1, 40))
        rows.append([eid, t.strftime('%m/%d/%Y %H:%M:%S.') + '%03d' % (t.microsecond // 1000), '69kV BKR 52-1 RELAY',
                     '51N PICKUP - GND FAULT ON 69KV SYSTEM, NO TRIP', round(rec['I']['A'] / 1000.0, 3),
                     round(rec['I']['B'] / 1000.0, 3), round(rec['I']['C'] / 1000.0, 3), round(rec['IG'] / 1000.0, 3)])
    # the plant's own events: inverter trips, controller curtailments, communications
    t0 = C.SOLAR_ENERGIZED
    span_h = int((C.T_END - t0).total_seconds() // 3600)
    for _ in range(int(rng.poisson(780))):
        t = C.to_cst(t0 + dt.timedelta(hours=float(rng.uniform(0, span_h))))
        kind = rng.random()
        eid += int(rng.integers(1, 40))
        if kind < 0.55:
            inv = int(rng.integers(1, 25))
            rows.append([eid, t.strftime('%m/%d/%Y %H:%M:%S.000'), 'INV-%02d' % inv,
                         'INV-%02d FAULT %d' % (inv, int(rng.choice([3412, 2207, 1150, 4102, 3390]))), '', '', '', ''])
        elif kind < 0.85:
            rows.append([eid, t.strftime('%m/%d/%Y %H:%M:%S.000'), 'PPC', 'PPC CURTAILMENT TO %d MW' % int(rng.integers(10, 55)),
                         '', '', '', ''])
        else:
            rows.append([eid, t.strftime('%m/%d/%Y %H:%M:%S.000'), 'RTU', 'COMMS LOSS TO ISO', '', '', '', ''])
    rows.sort(key=lambda r: dt.datetime.strptime(r[1][:19], '%m/%d/%Y %H:%M:%S'))
    return rows


def write_ipp(rows, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['event_id', 'timestamp', 'source', 'description', 'ia_ka', 'ib_ka', 'ic_ka', 'in_ka'])
        for r in rows:
            wr.writerow(r)
    return len(rows)


# ------------------------------------------------------------------------------------------------ work orders

def _plate(lid, no, day):
    """the structure number on the plate that day: rebuilt lines carried their former numbers before the rebuild"""
    if lid in N.REBUILT and day < N.REBUILT[lid][0]:
        return no + N.REBUILT[lid][1]
    return no


def maint_rows(w, rng):
    net = w['net']
    rows = []
    wo = 260000
    for (lid, no), t in sorted(w['replaced'].items(), key=lambda kv: kv[1]):
        lt = C.to_local(t)
        wo += int(rng.integers(3, 60))
        rows.append([wo, lt.date(), lt.date(), 'Line %d' % int(lid[1:]), _plate(lid, no, lt.date()), 'INSULATOR', 'replace 69 kV post insulator string, cracked bell', 'Crew 4'])
    for lid, no, site, birds, guarded in F.ROOSTS:
        if guarded is None:
            continue
        lt = C.to_local(guarded)
        wo += int(rng.integers(3, 60))
        rows.append([wo, (lt - dt.timedelta(days=int(rng.integers(10, 40)))).date(), lt.date(), 'Line %d' % int(lid[1:]), no,
                     'AVIAN', 'install perch guards and streamer shields on the crossarm', 'Crew 2'])
    for f in w['faults']:
        if not f['permanent']:
            continue
        lt = C.to_local(f['t'])
        if f['cause'] == 'vehicle':
            typ, desc = 'POLE', 'replace pole damaged by vehicle'
        elif f['cause'] == 'hardware':
            typ, desc = 'HARDWARE', str(rng.choice(['repair jumper connector', 'replace burnt clamp', 'replace failed splice']))
        elif f['cause'] == 'lightning':
            typ, desc = 'ARRESTER', 'replace failed line arrester / flashed insulator'
        else:
            continue
        wo += int(rng.integers(3, 60))
        rows.append([wo, lt.date(), (lt + dt.timedelta(days=float(rng.uniform(0, 3)))).date(), 'Line %d' % int(f['line'][1:]),
                     _plate(f['line'], f['structure'], lt.date()), typ, desc, str(rng.choice(['Crew 2', 'Crew 4', 'Crew 5']))])
    # routine work
    for _ in range(320):
        lid = sorted(net['lines'])[int(rng.integers(0, 16))]
        line = net['lines'][lid]
        d = dt.date(int(rng.integers(2022, 2027)), int(rng.integers(1, 11)), int(rng.integers(1, 28)))
        typ = str(rng.choice(['CROSSARM', 'GUY', 'INSPECTION', 'SWITCH', 'GROUND', 'SIGNAGE'], p=[0.2, 0.15, 0.3, 0.1, 0.15, 0.1]))
        desc = {'CROSSARM': 'replace split crossarm', 'GUY': 'retension guy', 'INSPECTION': 'climbing inspection',
                'SWITCH': 'line switch maintenance', 'GROUND': 'repair ground wire', 'SIGNAGE': 'replace structure number plate'}[typ]
        wo += int(rng.integers(3, 60))
        rows.append([wo, d, d + dt.timedelta(days=int(rng.integers(0, 20))), 'Line %d' % int(lid[1:]),
                     int(rng.integers(1, len(line['structures']) + 1)), typ, desc, str(rng.choice(['Crew 2', 'Crew 4', 'Crew 5', 'Crew 7']))])
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows


def veg_rows(w, rng):
    net = w['net']
    rows = []
    wo = 410000
    # spans the grow-ins still reach: no cycle trim may cover them after their last contact
    last_contact = {}
    for f in w['faults']:
        if f['cause'] == 'growin':
            key = (f['line'], f['span'][0])
            last_contact[key] = max(last_contact.get(key, f['t']), f['t'])
    protect = [(lid, no) for (lid, no) in last_contact
               if (lid, no) not in w['trims'] or last_contact[(lid, no)] > w['trims'][(lid, no)]]
    for (lid, no), t in sorted(w['trims'].items(), key=lambda kv: kv[1]):
        lt = C.to_local(t)
        cyc = [g for g in F.GROWIN if g[0] == lid and g[1] == no and any(abs((td - t).total_seconds()) < 86400 for td, r in g[3])]
        wo += int(rng.integers(2, 30))
        if cyc:
            rows.append([wo, lt.date(), 'Line %d' % int(lid[1:]), _plate(lid, max(1, no - 9), lt.date()), _plate(lid, no + 12, lt.date()),
                         'CYCLE TRIM', 'four-year cycle trim, side and under trimming', int(rng.integers(60, 180))])
        else:
            rows.append([wo, lt.date(), 'Line %d' % int(lid[1:]), _plate(lid, no, lt.date()), _plate(lid, no + 1, lt.date()), 'HOT SPOT',
                         'trim tree after contact', int(rng.integers(1, 4))])
    for lid in sorted(net['lines']):
        line = net['lines'][lid]
        n = len(line['structures'])
        segs = [(1, n // 3), (n // 3 + 1, 2 * n // 3), (2 * n // 3 + 1, n)]
        for k, (a, b) in enumerate(segs):
            yr = 2022 + (int(lid[1:]) + k) % 4
            d = dt.date(yr, int(rng.integers(1, 4)), int(rng.integers(1, 28)))
            covered = [p for p in protect if p[0] == lid and a <= p[1] <= b]
            if covered:
                # the cycle trim on this segment was in the winter before the trees reached the line
                d = dt.date(2022, 1, int(rng.integers(5, 28)))
            wo += int(rng.integers(2, 30))
            rows.append([wo, d, 'Line %d' % int(lid[1:]), _plate(lid, a, d), _plate(lid, b, d), 'CYCLE TRIM', 'four-year cycle trim',
                         int(rng.integers(40, 220))])
    for _ in range(140):
        lid = sorted(net['lines'])[int(rng.integers(0, 16))]
        line = net['lines'][lid]
        a = int(rng.integers(1, len(line['structures'])))
        d = dt.date(int(rng.integers(2022, 2027)), int(rng.integers(1, 11)), int(rng.integers(1, 28)))
        typ = str(rng.choice(['MOWING', 'HERBICIDE', 'HAZARD TREE'], p=[0.45, 0.35, 0.2]))
        if typ != 'MOWING' and F._near_source(lid, line['structures'][a - 1]['km'], 3.5):
            typ = 'MOWING'
        wo += int(rng.integers(2, 30))
        rows.append([wo, d, 'Line %d' % int(lid[1:]), a, min(a + int(rng.integers(1, 15)), len(line['structures'])), typ,
                     {'MOWING': 'mow right of way', 'HERBICIDE': 'basal herbicide', 'HAZARD TREE': 'remove leaning dead tree'}[typ],
                     int(rng.integers(1, 40))])
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows
