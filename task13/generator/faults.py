"""Every 69 kV fault from January 2022 to October 2026 (architecture 7, Level 5):
lightning strokes near lines; bird streamers at winter roosts; coastal porcelain fog flashovers governed jointly by
ESDD (soluble sea salt on onshore winds, fast rain washout) and NSDD (non-soluble caliche/agricultural dust on dry
inland winds, slow rain washout) via a smooth IEC 60815 logistic hazard; cracked porcelain strings (including past
two YNd1 IPP lateral taps on Lines 8 and 9 and inside the Lines 10/11 double-circuit corridor); grow-in contacts with
heterogeneous per-span growth rates (including on underbuilt spans); two active 12.47 kV underbuild clearance spans;
outside-ROW dead pine stands; and random vehicle/hardware/unknown faults."""
import datetime as dt
import math

import numpy as np
from scipy.spatial import cKDTree

import common as C
import loads as L
import network as N
import weather as W

# fault resistance by cause (ohm)
RF = {'lightning': (6.0, 28.0), 'bird': (0.8, 3.2), 'fog': (1.5, 4.5), 'insulator': (0.3, 0.9),
      'growin': (9.0, 38.0), 'fallin': (3.0, 22.0), 'vehicle': (0.5, 4.0), 'hardware': (0.5, 3.0),
      'clearance': (4.0, 13.0), 'unknown': (0.8, 9.0)}

# roost structures: line, structure no., the survey site, birds in a typical winter, guards fitted (UTC) or None
ROOSTS = [
    ('L07', 31, 'RS-03', 180, None),
    ('L07', 38, 'RS-04', 130, dt.datetime(2024, 11, 14, 17, 0, tzinfo=C.UTC)),
    ('L07', 52, 'RS-06', 150, None),
    ('L16', 23, 'RS-09', 175, None),
    ('L06', 79, 'RS-11', 95, None),
    ('L12', 96, 'RS-15', 190, dt.datetime(2024, 11, 20, 16, 0, tzinfo=C.UTC)),
    ('L12', 104, 'RS-16', 260, None),
    ('L14', 118, 'RS-19', 125, None),
]

# cracked strings: line, structure no. (or None to use km_override), onset (UTC), haz0, efold days, fails_fixed, km_override
# Active strings (fails_fixed=False) experience occasional unfound lockouts (~22%) so they carry real member-minutes
# while staying in service until pinpointed; fixed strings (fails_fixed=True) break visibly on their 4th fault & get replaced.
CRACKED = [
    ('L09', None, dt.datetime(2024, 2, 5, tzinfo=C.UTC), 0.011, 460.0, False, 26.55),   # S2: past Coyote Draw Solar tap (23.4 km)
    ('L08', None, dt.datetime(2024, 3, 10, tzinfo=C.UTC), 0.011, 460.0, False, 18.65),  # S2: past Brushy Creek BESS tap (13.8 km)
    ('L11', None, dt.datetime(2024, 1, 15, tzinfo=C.UTC), 0.012, 440.0, False, 13.85),  # S3: inside L10/L11 double-circuit corridor
    ('L05', 88, dt.datetime(2024, 5, 20, tzinfo=C.UTC), 0.012, 500.0, False, None),     # inland unfixed baseline
    ('L13', 72, dt.datetime(2022, 2, 1, tzinfo=C.UTC), 0.030, 300.0, True, None),       # fails visibly, replaced
    ('L15', 92, dt.datetime(2023, 3, 1, tzinfo=C.UTC), 0.025, 360.0, True, None),       # fails visibly, replaced
    ('L07', 41, dt.datetime(2022, 6, 1, tzinfo=C.UTC), 0.028, 320.0, True, None),       # fails visibly, replaced
]
TAP_STRING_KM = 26.55
BESS_STRING_KM = 18.65
DC_STRING_KM = 13.85
DC_GROWIN_KM = 13.35

# grow-in spans with HETEROGENEOUS per-span tree growth rates (no constant 2.0 C/yr tell!):
# line, back_no (or None -> km_override), km_override, t0c in May 2022, growth_c_per_yr, cycle_trims, burn_year
GROWIN = [
    ('L10', None, DC_GROWIN_KM, 53.2, 2.35, [], None),                                   # S3: inside L10/L11 double-circuit corridor
    ('L14', 62, None, 56.0, 2.10, [], None),                                             # S1 decoy: carries 12.47 kV underbuild!
    ('L12', 44, None, 54.5, 2.75, [], None),                                             # S1 decoy: carries 12.47 kV underbuild!
    ('L11', 112, None, 51.8, 1.85, [], None),                                            # non-underbuilt active grow-in
    ('L10', 102, None, 51.0, 2.50, [(dt.datetime(2024, 2, 13, 15, 0, tzinfo=C.UTC), 5.5)], None),  # post-trim regrowth
    ('L14', 131, None, 54.5, 2.25, [], 2026),                                            # burned/cleared 2026 (fixed)
    ('L05', 101, None, 47.5, 2.60, [], 2026),                                            # burned/cleared 2026 (fixed)
    ('L15', 33, None, 55.0, 1.95, [(dt.datetime(2025, 2, 11, 15, 0, tzinfo=C.UTC), 25.0)], None),  # cleared in 2025 cycle (fixed)
]

# TWO active 12.47 kV underbuild clearance spans (S1): fixed clearance temperature (modulated by lower circuit's sag)
# line, back_no, t_ub (deg C at 32 C ambient), k_air
UNDERBUILD = [
    ('L06', 57, 42.2, 0.28),
    ('L15', 48, 49.0, 0.24),
]

# Joint coastal contamination physics (IEC 60815-1):
# - ESDD (sea salt): onshore Gulf wind (140 deg), exponential shore decay, fast rain washout
# - NSDD (caliche/agricultural dust): dry inland wind (325 deg), corridor surface dustiness, slow rain washout
GULF_FROM = 140.0
SALT_BG = 0.25
INLAND_FROM = 325.0
DUST_BG = 0.30
ESDD_K_RAIN = 0.052     # smooth exponential rain washout (/mm) for soluble sea salt
NSDD_K_RAIN = 0.008     # smooth exponential rain washout (/mm) for sticky clay/caliche dust
NSDD_REF = 0.20         # reference NSDD (mg/cm2)
NSDD_BETA = 0.45        # IEC 60815 NSDD exponent on effective contamination index
CEFF_CRIT = 0.052       # smooth logistic 50% flashover scale (mg/cm2 effective)

# dead pine stands outside the right of way (line, structure no. range, summer storm prob, winter front prob)
DANGER = [('L13', 104, 106, 0.30, 0.0006), ('L11', 124, 126, 0.04, 0.0016)]
GULF_LINES = ('L01', 'L02', 'L03', 'L04')

_SOURCES = []


def fill_sources(net):
    del _SOURCES[:]
    for lid, no, *_ in ROOSTS:
        _SOURCES.append((lid, net['lines'][lid]['structures'][no - 1]['km']))
    for lid, no, _on, _h, _e, _f, km_ov in CRACKED:
        _SOURCES.append((lid, km_ov if km_ov is not None else net['lines'][lid]['structures'][no - 1]['km']))
    for lid, no, km_ov, *_ in GROWIN:
        _SOURCES.append((lid, km_ov if km_ov is not None else net['lines'][lid]['structures'][no - 1]['km']))
    for lid, no, *_ in UNDERBUILD:
        _SOURCES.append((lid, net['lines'][lid]['structures'][no - 1]['km']))
    for lid, a, b, *_ in DANGER:
        _SOURCES.append((lid, (net['lines'][lid]['structures'][a - 1]['km'] + net['lines'][lid]['structures'][b - 1]['km']) / 2))


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


def directional_exposure(wx, code, bearing):
    """each local day's mean squared wind component blowing from `bearing` (degrees)"""
    s = wx['series'][code]
    u = s['wind'] * np.maximum(0.0, np.cos(np.radians(s['wdir'] - bearing)))
    e = np.zeros(len(wx['days']))
    n = np.zeros(len(wx['days']))
    np.add.at(e, wx['hday'], u ** 2)
    np.add.at(n, wx['hday'], 1.0)
    return e / np.maximum(n, 1.0)


def onshore_exposure(wx, code):
    return directional_exposure(wx, code, GULF_FROM)


def inland_exposure(wx, code):
    return directional_exposure(wx, code, INLAND_FROM)


def salt_factor(wx, codes):
    cache = wx.setdefault('_salt', {})
    key = tuple(codes)
    if key not in cache:
        e = np.mean([onshore_exposure(wx, c) for c in codes], axis=0)
        cache[key] = SALT_BG + (1.0 - SALT_BG) * e / max(float(e.mean()), 1e-9)
    return cache[key]


def dust_factor(wx, codes):
    cache = wx.setdefault('_dust', {})
    key = tuple(codes)
    if key not in cache:
        e = np.mean([inland_exposure(wx, c) for c in codes], axis=0)
        cache[key] = DUST_BG + (1.0 - DUST_BG) * e / max(float(e.mean()), 1e-9)
    return cache[key]


def esdd_rain_keep(mm):
    return math.exp(-ESDD_K_RAIN * max(0.0, float(mm)))


def nsdd_rain_keep(mm):
    return math.exp(-NSDD_K_RAIN * max(0.0, float(mm)))


def deposit_rate(shore_km, onshore=1.0):
    """soluble sea-salt accumulation (mg/cm2/day), decaying exponentially from the Gulf shore"""
    return 0.0068 * math.exp(-shore_km / 1.50) * onshore + 0.00006


def nsdd_rate(surface):
    """non-soluble dust/caliche accumulation (mg/cm2/dry-day) by corridor surface"""
    return 0.0042 * N.DUST_MULT.get(surface, 1.0)


def effective_ceff(esdd, nsdd):
    """IEC 60815 effective contamination index combining soluble salt (ESDD) and insoluble deposit (NSDD)"""
    return esdd * ((np.maximum(nsdd, 0.01) / NSDD_REF) ** NSDD_BETA)


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
    for ss in secs:
        surfs = [s['surface'] for s in ss]
        dom_surf = max(set(surfs), key=surfs.count)
        out.append(dict(id='%s-W%d' % (ss[0]['line'], sum(1 for o in out if o['line'] == ss[0]['line']) + 1),
                        line=ss[0]['line'], s0=ss[0]['no'], s1=ss[-1]['no'], km0=ss[0]['km'], km1=ss[-1]['km'],
                        shore=float(np.mean([s['shore_km'] for s in ss])), surface=dom_surf))
    return out


def _storm_near(wx, x, y, h, radius, n=3):
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
               enumerate(['add', 'lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin', 'random', 'clearance'])}
    nh = C.NH
    h_rec0 = C.hour_index(C.REC0)
    faults = []
    fill_sources(net)

    def add(h, sec, lid, km, cause, perm, phases=None, rf=None, extra=None):
        rng = streams[{'lightning': 'lightning', 'bird': 'bird', 'fog': 'fog', 'insulator': 'insulator', 'growin': 'growin',
                       'fallin': 'fallin', 'clearance': 'clearance'}.get(cause, 'random')]
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
    pts, keys = _structure_xy(net)
    tree = cKDTree(pts)
    days = wx['days']
    for (i, lh, x, y, ka) in wx['strokes']:
        d, j = tree.query((x, y))
        if d > 0.12:
            continue
        lid, no = keys[j]
        line = net['lines'][lid]
        p = (1.0 - math.exp(-(abs(ka) / 38.0) ** 2)) * (0.45 if d < 0.05 else 0.18)
        if rng.random() < p:
            t = _utc_from_local(days[i], lh)
            h = C.hour_index(t)
            if h < 0 or h >= nh:
                continue
            km = min(max(line['structures'][no - 1]['km'] + rng.normal(0, 0.04), 0.05), line['length'] - 0.05)
            sec = (t - C.ts_of(h)).total_seconds()
            ph = [['A', 'B', 'C'][int(rng.integers(0, 3))]]
            if rng.random() < 0.18:
                ph = sorted(rng.choice(['A', 'B', 'C'], 2, replace=False).tolist())
            near = [f for f in faults if f['cause'] == 'lightning' and f['line'] == lid and abs(f['km'] - km) <= 1.0]
            if len(near) >= 1 or _near_source(lid, km, 0.6):
                continue
            add(h, sec, lid, km, 'lightning', rng.random() < 0.12, ph, rf=(float(rng.uniform(0.8, 3.0)) if len(ph) == 2 else None),
                extra=dict(stroke_ka=ka, stroke=(i, lh, x, y)))

    rng = streams['bird']
    hour, month = wx['hour'], wx['month']
    for lid, no, site, birds, guarded in ROOSTS:
        st = net['lines'][lid]['structures'][no - 1]
        lam = 0.0110 * birds / 100.0
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
                        rng.random() < 0.08, [outer], extra=dict(roost=site))
    for _ in range(6):
        lid, km = _random_place(net, rng, faults, 'bird')
        h = int(rng.integers(h_rec0, nh))
        add(h, rng.uniform(0, 3600), lid, km, 'bird', rng.random() < 0.2)

    rng = streams['fog']
    # ---- joint (ESDD, NSDD) deposits and smooth logistic fog flashovers on the Gulf lines' porcelain
    rain_codes = {'L01': ('PAL', 'APT'), 'L02': ('PAL', 'SHR'), 'L03': ('SHR', 'SED'), 'L04': ('APT', 'PAL')}
    drains = {c: W.daily_rain(wx, c) for c in ('APT', 'PAL', 'SHR', 'SED')}
    deposit_hist = {}
    fog_index = wx['fog_index']
    for lid in GULF_LINES:
        line = net['lines'][lid]
        sts = [s for s in line['structures'] if s['insulator'] == 'porcelain' and s['shore_km'] <= 6.0]
        rain = (drains[rain_codes[lid][0]] + drains[rain_codes[lid][1]]) / 2.0
        erates = np.array([deposit_rate(s['shore_km']) for s in sts])
        nrates = np.array([nsdd_rate(s['surface']) for s in sts])
        esdd = erates * 45.0
        nsdd = nrates * 60.0
        es_ser = np.zeros((len(days), len(sts)))
        ns_ser = np.zeros((len(days), len(sts)))
        ce_ser = np.zeros((len(days), len(sts)))
        wash_days = {}
        for w in washes:
            if w['line'] != lid:
                continue
            di = days.index(w['date']) if w['date'] in days else None
            if di is not None:
                wash_days.setdefault(di, []).append(w)
        efac = salt_factor(wx, rain_codes[lid])
        nfac = dust_factor(wx, rain_codes[lid])
        for di, d in enumerate(days):
            esdd = (esdd + erates * efac[di]) * esdd_rain_keep(rain[di])
            nsdd = (nsdd + nrates * nfac[di] * (1.0 if rain[di] < 2.0 else 0.0)) * nsdd_rain_keep(rain[di])
            for w in wash_days.get(di, ()):
                for k, s in enumerate(sts):
                    if w['s0'] <= s['no'] <= w['s1']:
                        esdd[k] = 0.003
                        nsdd[k] = 0.015
            es_ser[di] = esdd
            ns_ser[di] = nsdd
            ce_ser[di] = effective_ceff(esdd, nsdd)
        deposit_hist[lid] = (sts, es_ser, ns_ser, ce_ser, erates, nrates)
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
                ce = float(ce_ser[di, k])
                # Smooth logistic flashover hazard in log(C_eff / CEFF_CRIT): zero hard 0% cutoff tell
                z = math.log(max(ce, 1e-6) / CEFF_CRIT) / 0.14
                if z < -4.5:
                    continue
                pk = 0.036 / (1.0 + math.exp(-z))
                haz.append((pk, s, k))
            if not haz or h - last_fault_h < 2:
                continue
            p_tot = 1.0 - math.exp(-sum(p for p, _, _ in haz))
            if rng.random() < p_tot:
                ps = np.array([p for p, _, _ in haz])
                _, s, k = haz[int(rng.choice(len(haz), p=ps / ps.sum()))]
                add(h, rng.uniform(0, 3600), lid, s['km'] + rng.normal(0, 0.01), 'fog', rng.random() < 0.06,
                    extra=dict(esdd=float(es_ser[di, k]), nsdd=float(ns_ser[di, k]), ceff=float(ce_ser[di, k])))
                last_fault_h = h

    rng = streams['insulator']
    # ---- cracked strings: flash over in light rain at any hour or in fog; unfixed strings occasionally lock out
    # without visible ground-level damage so they carry genuine member-minutes until diagnosed
    st_places = {}
    replaced = {}
    for lid, no, onset, haz0, efold, fails, km_ov in CRACKED:
        line = net['lines'][lid]
        st = N.structure_at(net, lid, km_ov) if km_ov is not None else line['structures'][no - 1]
        code = min(W.PLACES, key=lambda c: math.hypot(W.PLACES[c][0] - st['x'], W.PLACES[c][1] - st['y']))
        pr = wx['series'][code]['precip']
        h0 = max(C.hour_index(onset), 0)
        n_here = 0
        quiet_until = -1
        for h in range(h0, nh):
            if h < quiet_until:
                continue
            wet_rain = 0.25 <= pr[h] < 2.5
            wet_fog = ((not wet_rain) and (hour[h] >= 22 or hour[h] <= 9) and (h in fog_index or wx['bay_fog_day'][wx['hday'][h]])
                       and W.fog_at(wx, st['x'], st['y'], h))
            if not (wet_rain or wet_fog):
                continue
            if wx['front'][wx['hday'][h]] > 1.5 or _storm_near(wx, st['x'], st['y'], h, 15.0):
                continue
            age = (h - h0) / 24.0
            if rng.random() < haz0 * (3.5 if wet_fog else 1.0) * math.exp(age / efold):
                n_here += 1
                perm = (fails and n_here >= 4) or ((not fails) and (n_here in (3, 6) or rng.random() < 0.20))
                add(h, rng.uniform(0, 3600), lid, st['km'] + rng.normal(0, 0.01), 'insulator', perm,
                    extra=dict(string=st['no'], wet='fog' if wet_fog else 'rain', visible_break=(fails and n_here >= 4)))
                quiet_until = h + 48
                if fails and n_here >= 4:
                    replaced[(lid, st['no'])] = C.ts_of(h) + dt.timedelta(hours=float(rng.uniform(5, 30)))
                    break
        st_places[(lid, st['no'])] = st

    rng = streams['growin']
    # ---- grow-in contacts with heterogeneous per-span growth rates + stochastic weather/season noise
    trims = {}
    for lid, back_no, km_ov, t0c, growth_yr, cycle, burn_year in GROWIN:
        line = net['lines'][lid]
        if km_ov is not None:
            s0, s1 = N.span_at(net, lid, km_ov)
        else:
            s0 = line['structures'][back_no - 1]
            s1 = line['structures'][back_no]
        km = (s0['km'] + s1['km']) / 2.0
        code = min(W.PLACES, key=lambda c: math.hypot(W.PLACES[c][0] - s0['x'], W.PLACES[c][1] - s0['y']))
        temp, wind, _ = W.instrumented_series(wx, s0['x'], s0['y'])
        amps = ld['amps'][lid]
        prc = wx['series'][code]['precip']
        cand = [h for h in range(h_rec0, nh) if 12 <= hour[h] <= 19 and month[h] in (5, 6, 7, 8, 9, 10)
                and prc[h] < 0.1 and not _storm_near(wx, s0['x'], s0['y'], h, 15.0)]
        year_jitter = {y: float(rng.normal(0, 0.30)) for y in range(2022, 2027)}
        refractory = -1
        done = False
        n_g = 0
        for h in cand:
            t = C.ts_of(h)
            raise_c = sum(r for (td, r) in cycle if t >= td)
            if done:
                break
            yr_h = int(wx['year'][h])
            tcontact = t0c - growth_yr * (yr_h - 2022) + year_jitter[yr_h] + raise_c
            if h < refractory:
                continue
            tc = L.conductor_temp(float(amps[h]), line['conductor'], float(temp[h]), float(wind[h]), 850.0)
            if tc >= tcontact - 2.5 and rng.random() < 0.24 / (1.0 + math.exp(-(tc - tcontact) / 0.9)):
                n_g += 1
                burn_perm = burn_year is not None and yr_h == burn_year
                unfound_perm = (burn_year is None) and (n_g in (2, 5) or rng.random() < 0.16)
                add(h, rng.uniform(0, 3600), lid, km + rng.normal(0, 0.02), 'growin', burn_perm or unfound_perm,
                    extra=dict(span=(s0['no'], s1['no']), tc=tc, burned_clear=burn_perm))
                refractory = h + 24 * 20
                if burn_perm:
                    trims[(lid, s0['no'])] = t + dt.timedelta(days=float(rng.uniform(1, 4)))
                    done = True
        for (td, r) in cycle:
            trims.setdefault((lid, s0['no']), td)

    rng = streams['clearance']
    # ---- two active 12.47 kV underbuild clearance spans: flat conductor temperature across summers and trims
    # Aligned hour window 12 <= hour <= 19 with golden.py (fixes Arch 6 F0174 hour bug)
    for lid, back_no, t_ub, k_air in UNDERBUILD:
        line = net['lines'][lid]
        s0 = line['structures'][back_no - 1]
        s1 = line['structures'][back_no]
        km = (s0['km'] + s1['km']) / 2.0
        code = min(W.PLACES, key=lambda c: math.hypot(W.PLACES[c][0] - s0['x'], W.PLACES[c][1] - s0['y']))
        temp, wind, _ = W.instrumented_series(wx, s0['x'], s0['y'])
        amps = ld['amps'][lid]
        prc = wx['series'][code]['precip']
        cand = [h for h in range(h_rec0, nh) if 12 <= hour[h] <= 19 and month[h] in (5, 6, 7, 8, 9, 10)
                and prc[h] < 0.1 and not _storm_near(wx, s0['x'], s0['y'], h, 15.0)]
        refractory = -1
        first = None
        n_c = 0
        for h in cand:
            if h < refractory:
                continue
            tc = L.conductor_temp(float(amps[h]), line['conductor'], float(temp[h]), float(wind[h]), 850.0)
            reach = t_ub + k_air * (float(temp[h]) - 32.0) + float(rng.normal(0, 0.35))
            if tc >= reach - 2.0 and rng.random() < 0.17 / (1.0 + math.exp(-(tc - reach) / 0.8)):
                n_c += 1
                perm = (n_c in (3, 6) or rng.random() < 0.18)
                add(h, rng.uniform(0, 3600), lid, km + rng.normal(0, 0.02), 'clearance', perm,
                    extra=dict(span=(s0['no'], s1['no']), tc=tc))
                refractory = h + 24 * 20
                if first is None:
                    first = C.ts_of(h)
        if first is not None:
            trims[(lid, s0['no'])] = first + dt.timedelta(days=float(rng.uniform(28, 45)))

    rng = streams['fallin']
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
                add(h, rng.uniform(0, 3600), lid, k, 'fallin', rng.random() < 0.25, extra=dict(stand='%s %d-%d' % (lid, a, b)))
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
    for cause, n, perm_p in (('vehicle', 11, 1.0), ('hardware', 14, 0.85), ('unknown', 30, 0.08)):
        for _ in range(n):
            lid, km = _random_place(net, rng, faults, cause)
            st = N.structure_at(net, lid, km)
            while True:
                h = int(rng.integers(h_rec0, nh))
                if _benign(wx, st['x'], st['y'], h):
                    break
            add(h, rng.uniform(0, 3600), lid, km, cause, rng.random() < perm_p)

    faults = [f for f in faults if C.REC0 <= f['t'] < C.T_END]
    faults.sort(key=lambda f: f['t'])
    keep, last = [], {}
    for f in faults:
        if f['line'] in last and (f['t'] - last[f['line']]).total_seconds() < 120:
            continue
        keep.append(f)
        last[f['line']] = f['t']
    for k, f in enumerate(keep):
        f['id'] = k + 1
    return dict(faults=keep, deposits=deposit_hist, replaced=replaced, trims=trims, strings=st_places)
