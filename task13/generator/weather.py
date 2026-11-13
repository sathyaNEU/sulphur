"""Hourly weather on the coastal bend, September 2021 to October 2026, simulated as a regional state with local
departures: temperature and dew point on the season and the hour, the summer sea breeze, winter fronts, convective
cells that rain and strike lightning where they track, tropical rain in late summer, and the summer and autumn of 2026
with no soaking rain at the coast after 4 June. Fog comes two ways: Gulf sea fog in patches that roll onto a stretch
of the shore on winter and spring nights and reach a few kilometres inland, and radiation fog over the bay's marshes
on calm, clear winter nights. Every location's weather is the state at its own place; each instrument records the
place it stands (the Port Alcorn airport on the Gulf side, the inland regional airport, and from March 2023 the
cooperative's own weather stations at six substations)."""
import datetime as dt
import math

import numpy as np

import common as C
import network as N

# the places weather is simulated at: code -> (x, y)
PLACES = {
    'APT': (77.5, 25.0),     # Port Alcorn airport, on the Gulf side of town
    'INA': (14.0, 50.5),     # inland regional airport
    'PAL': N.ST['PAL']['xy'], 'SHR': N.ST['SHR']['xy'], 'SED': N.ST['SED']['xy'],
    'TUL': N.ST['TUL']['xy'], 'CAN': N.ST['CAN']['xy'], 'MSQ': N.ST['MSQ']['xy'],
    'BAY': N.ST['BAY']['xy'], 'RFP': N.ST['RFP']['xy'], 'LOK': N.ST['LOK']['xy'], 'GRG': N.ST['GRG']['xy'],
    'INL': N.ST['INL']['xy'], 'PND': N.ST['PND']['xy'],
}
STATION_CODES = ['PAL', 'SHR', 'SED', 'TUL', 'CAN', 'MSQ']


def shore_coord(x, y):
    """position along the shoreline (km from its south-west end) of the nearest shore point"""
    best, s_best, s0 = 1e9, 0.0, 0.0
    for (x0, y0), (x1, y1) in zip(N.SHORE[:-1], N.SHORE[1:]):
        dx, dy = x1 - x0, y1 - y0
        seg = math.hypot(dx, dy)
        t = max(0.0, min(1.0, ((x - x0) * dx + (y - y0) * dy) / (seg * seg)))
        d = math.hypot(x - (x0 + t * dx), y - (y0 + t * dy))
        if d < best:
            best, s_best = d, s0 + t * seg
        s0 += seg
    return s_best


def _seasonal(doy, jan, jul):
    return (jan + jul) / 2 - (jul - jan) / 2 * math.cos(2 * math.pi * (doy - 15) / 365.25)


def simulate():
    rng = np.random.default_rng(C.WX_SEED)
    nh = C.NH
    t0 = C.T0
    loc = [C.to_local(t0 + dt.timedelta(hours=h)) for h in range(nh)]
    hour = np.array([t.hour for t in loc])
    doy = np.array([t.timetuple().tm_yday for t in loc])
    date = [t.date() for t in loc]
    month = np.array([t.month for t in loc])
    year = np.array([t.year for t in loc])
    days = sorted(set(date))
    dindex = {d: i for i, d in enumerate(days)}
    hday = np.array([dindex[d] for d in date])
    nd = len(days)

    # regional daily anomalies (AR(1)) and winter fronts
    anom_t = np.zeros(nd)
    anom_d = np.zeros(nd)
    for i in range(1, nd):
        anom_t[i] = 0.78 * anom_t[i - 1] + rng.normal(0, 1.5)
        anom_d[i] = 0.70 * anom_d[i - 1] + rng.normal(0, 1.6)
    front = np.zeros(nd)
    dmonth = np.array([d.month for d in days])
    for i in range(nd):
        if dmonth[i] in (11, 12, 1, 2, 3) and rng.random() < 0.075:
            k = int(rng.integers(2, 5))
            for j in range(k):
                if i + j < nd:
                    front[i + j] = max(front[i + j], (1.0 - j / k) * rng.uniform(6, 11))
    # convective days (rain and lightning) and tropical rain
    conv = np.zeros(nd)
    for i, d in enumerate(days):
        p = {5: 0.18, 6: 0.32, 7: 0.40, 8: 0.42, 9: 0.33, 10: 0.12, 4: 0.10, 3: 0.05}.get(d.month, 0.02)
        if d.year == 2026 and d >= dt.date(2026, 6, 4):
            p *= 0.45
        if rng.random() < p:
            conv[i] = rng.uniform(0.3, 1.0)
    frontal_rain = np.zeros(nd)
    for i, d in enumerate(days):
        if front[i] > 0 and (i == 0 or front[i - 1] == 0):
            frontal_rain[i] = rng.gamma(1.6, 9.0)          # mm over the front's first day, regional
        elif d.month in (10, 11, 12, 1, 2, 3, 4, 5) and rng.random() < 0.085:
            frontal_rain[i] = rng.gamma(1.3, 7.5)
        elif d.month in (6, 7, 8, 9) and rng.random() < 0.035:
            frontal_rain[i] = rng.gamma(1.4, 9.0)          # a summer tropical wave's rain
        if d.month in (8, 9, 10) and rng.random() < 0.03:
            frontal_rain[i] += rng.gamma(2.0, 20.0)       # a tropical system's rain
        if d.year == 2026 and dt.date(2026, 6, 4) <= d <= dt.date(2026, 10, 31):
            frontal_rain[i] = min(frontal_rain[i], rng.uniform(0.5, 6.0)) if frontal_rain[i] > 0 else 0.0

    # sea fog events: Dec to Apr nights and mornings, a patch along the shore with a penetration inland
    shore_len = sum(math.hypot(x1 - x0, y1 - y0) for (x0, y0), (x1, y1) in zip(N.SHORE[:-1], N.SHORE[1:]))
    fog_events = []
    for i, d in enumerate(days):
        if d.month in (12, 1, 2, 3, 4, 11):
            p = {12: 0.13, 1: 0.17, 2: 0.19, 3: 0.16, 4: 0.08, 11: 0.04}[d.month]
            if front[i] > 2.5:
                p *= 0.15
            if rng.random() < p:
                start = rng.uniform(19.0, 27.0)                     # hours after local midnight of day d
                dur = rng.uniform(4.0, 13.0)
                centre = rng.uniform(-5.0, shore_len + 5.0)
                half = rng.uniform(12.0, 26.0)
                pen = rng.uniform(2.5, 7.0)
                fog_events.append(dict(day=i, start=start, dur=dur, centre=centre, half=half, pen=pen))
    # bay radiation fog: calm clear nights Nov to Mar
    bay_fog_day = np.zeros(nd, bool)
    for i, d in enumerate(days):
        if d.month in (11, 12, 1, 2, 3) and front[i] < 1.0 and rng.random() < 0.10:
            bay_fog_day[i] = True

    # lightning cells: for each convective day, cells tracking across the region in the afternoon
    strokes = []
    cells = []
    for i, d in enumerate(days):
        if conv[i] <= 0:
            continue
        ncell = int(rng.poisson(2.0 + 6.0 * conv[i]))
        for _ in range(ncell):
            x0, y0 = rng.uniform(5, 110), rng.uniform(-5, 75)
            ang = rng.uniform(0, 2 * math.pi)
            spd = rng.uniform(15, 35)                        # km/h
            tstart = rng.normal(15.5, 2.2)                   # local hour
            life = rng.uniform(0.6, 2.2)
            rate = rng.uniform(60, 260) * conv[i]            # strokes per hour
            cells.append((i, x0, y0, ang, spd, tstart, life, rate))
            n = int(rng.poisson(rate * life))
            for _ in range(n):
                u = rng.uniform(0, life)
                x = x0 + math.cos(ang) * spd * u + rng.normal(0, 3.0)
                y = y0 + math.sin(ang) * spd * u + rng.normal(0, 3.0)
                lh = tstart + u
                strokes.append((i, lh, x, y, float(rng.lognormal(math.log(24.0), 0.55)) * (1 if rng.random() < 0.9 else -1)))

    out = dict(days=days, hday=hday, hour=hour, month=month, year=year, doy=doy, date=date, front=front, conv=conv,
               frontal_rain=frontal_rain, fog_events=fog_events, bay_fog_day=bay_fog_day, strokes=strokes, cells=cells,
               shore_len=shore_len)

    # per place hourly series
    series = {}
    for code, (x, y) in PLACES.items():
        sd = N._shore_dist(x, y)
        coastal = math.exp(-sd / 12.0)
        prng = np.random.default_rng(C.WX_SEED * 31 + sum(ord(c) for c in code))
        jan = 12.5 + 1.5 * coastal
        jul = 29.0 - 0.6 * coastal
        base = np.array([_seasonal(v, jan, jul) for v in doy])
        amp = 4.6 - 1.6 * coastal + 0.8 * (month >= 5) * (month <= 9)
        diurnal = amp * np.cos(2 * math.pi * (hour - 15) / 24.0)
        loc_anom = np.zeros(nh)
        for h in range(1, nh):
            loc_anom[h] = 0.97 * loc_anom[h - 1] + prng.normal(0, 0.18)
        temp = base + diurnal + anom_t[hday] - front[hday] * (0.9 - 0.3 * coastal) + loc_anom
        # dew point as a depression below the air temperature: wide on afternoons and after fronts, narrow on humid
        # coastal nights, never saturated outside fog
        night = np.clip(np.cos(2 * math.pi * (hour - 4) / 24.0), 0, None)
        dep_base = 5.6 - 1.6 * coastal - 2.6 * night * (0.6 + 0.4 * coastal) + 0.35 * front[hday]
        dep_ar = np.zeros(nh)
        for h in range(1, nh):
            dep_ar[h] = 0.93 * dep_ar[h - 1] + prng.normal(0, 0.32)
        dep = np.clip(dep_base + dep_ar + 0.4 * np.abs(anom_d[hday]), 0.9, None)
        dew = temp - dep
        # sea breeze and winds
        breeze = (month >= 4) * (month <= 10) * np.clip(np.cos(2 * math.pi * (hour - 15) / 24.0), 0, None) * (5.5 * coastal + 1.5)
        calm = 1.2 + 0.8 * coastal
        wind = calm + breeze + front[hday] * 0.8 + np.abs(prng.normal(0, 0.8, nh))
        wdir = np.where(breeze > 1.0, 135 + prng.normal(0, 20, nh), np.where(front[hday] > 1.0, 350 + prng.normal(0, 25, nh), prng.uniform(0, 360, nh))) % 360
        gust = wind * (1.35 + 0.25 * prng.random(nh))
        precip = np.zeros(nh)
        # frontal rain spread over the first 8 to 14 hours of the day, regionally with local scatter
        for i in np.nonzero(frontal_rain > 0)[0]:
            tot = frontal_rain[i] * prng.uniform(0.75, 1.25)
            hs = np.nonzero(hday == i)[0]
            if len(hs) == 0:
                continue
            k0 = int(prng.integers(0, max(1, len(hs) - 12)))
            w = prng.dirichlet(np.ones(10) * 1.2)
            for j, frac in enumerate(w):
                if k0 + j < len(hs):
                    precip[hs[k0 + j]] += tot * frac
        out.setdefault('places', {})[code] = dict(x=x, y=y, shore_km=sd, s=shore_coord(x, y))
        series[code] = dict(temp=temp, dew=dew, wind=wind, wdir=wdir, gust=gust, precip=precip)
    # convective rain and gusts where a cell passes within 12 km of a place
    for (i, x0, y0, ang, spd, tstart, life, rate) in cells:
        hs = np.nonzero(hday == i)[0]
        for code, (x, y) in PLACES.items():
            s = series[code]
            for u in np.linspace(0, life, 6):
                cx, cy = x0 + math.cos(ang) * spd * u, y0 + math.sin(ang) * spd * u
                dd = math.hypot(cx - x, cy - y)
                if dd < 12.0:
                    lh = int(tstart + u) % 24
                    hh = hs[hour[hs] == lh]
                    if len(hh):
                        s['precip'][hh[0]] += 6.0 * math.exp(-dd / 5.0) * rate / 150.0
                        s['gust'][hh[0]] = max(s['gust'][hh[0]], 12.0 + 10.0 * math.exp(-dd / 6.0) * (rate / 160.0))
                        s['temp'][hh[0]] -= 2.5 * math.exp(-dd / 6.0)
    out['series'] = series
    return out


def fog_at(wx, x, y, h):
    """truth: is there fog at a place at simulation hour h (sea fog patch or bay radiation fog)"""
    t = C.to_local(C.ts_of(h))
    s = shore_coord(x, y)
    sd = N._shore_dist(x, y)
    hit = False
    for ev in wx['fog_index'].get(h, ()):
        if abs(s - ev['centre']) <= ev['half'] and sd <= ev['pen']:
            hit = True
            break
    if not hit and N._bay_dist(x, y) <= 2.5:
        di = wx['hday'][h]
        lh = t.hour
        if wx['bay_fog_day'][di] and (lh >= 1 and lh <= 8):
            hit = True
    return hit


def index_fog(wx):
    """hour -> the sea fog events active that hour"""
    idx = {}
    days = wx['days']
    for ev in wx['fog_events']:
        d = days[ev['day']]
        start_local = dt.datetime(d.year, d.month, d.day) + dt.timedelta(hours=ev['start'])
        for k in range(int(math.ceil(ev['dur']))):
            tl = start_local + dt.timedelta(hours=k)
            try:
                tu = C.local(tl).astimezone(C.UTC)
            except Exception:
                continue
            h = C.hour_index(tu)
            if 0 <= h < C.NH:
                idx.setdefault(h, []).append(ev)
    wx['fog_index'] = idx
    return idx


def apply_fog_to_series(wx):
    """the instruments see fog where they stand: dew point up to the temperature, light wind"""
    for code, p in wx['places'].items():
        s = wx['series'][code]
        x, y = p['x'], p['y']
        for h in range(C.NH):
            if fog_at(wx, x, y, h):
                s['dew'][h] = s['temp'][h] - abs(np.random.default_rng(h * 7 + len(code)).normal(0.05, 0.12))
                s['wind'][h] = min(s['wind'][h], 2.6)


def daily_rain(wx, code):
    """mm per local day at a place"""
    s = wx['series'][code]['precip']
    out = np.zeros(len(wx['days']))
    np.add.at(out, wx['hday'], s)
    return out


def local_weather(wx, x, y, h):
    """inverse-distance weather at a structure from the nearest simulated places (truth for the fault process)"""
    ds = []
    for code, p in wx['places'].items():
        ds.append((math.hypot(p['x'] - x, p['y'] - y), code))
    ds.sort()
    w = [1.0 / max(0.5, d) ** 2 for d, _ in ds[:3]]
    tot = sum(w)
    res = {}
    for key in ('temp', 'dew', 'wind', 'gust', 'precip'):
        res[key] = sum(wi * wx['series'][c][key][h] for wi, (_, c) in zip(w, ds[:3])) / tot
    return res
