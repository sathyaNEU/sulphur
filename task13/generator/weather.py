"""The airport weather, hourly from December 2021: a seasonal and daily temperature cycle with day-to-day weather
systems on top, the winters' arctic outbreaks and the summers' heat, warm-season thunderstorms clustered in the
afternoon and evening with a few severe wind events a year, winter clippers and the odd freezing-rain storm."""
import datetime as dt

import numpy as np

import common as C


def simulate():
    rng = np.random.default_rng(C.WX_SEED)
    H = int((C.T_END - C.T0).total_seconds() // 3600)
    hours = np.arange(H)
    ts_utc = [C.T0 + dt.timedelta(hours=int(h)) for h in hours]
    loc = [C.to_local(t) for t in ts_utc]
    doy = np.array([t.timetuple().tm_yday for t in loc], float)
    hod = np.array([t.hour + t.minute / 60 for t in loc], float)
    days = np.array([(t.date() - C.to_local(C.T0).date()).days for t in loc])
    nd = days.max() + 1
    # seasonal mean and the daily cycle
    seas = 6.8 + 16.2 * np.sin(2 * np.pi * (doy - 106) / 365.25)
    amp = 5.0 + 1.4 * np.sin(2 * np.pi * (doy - 106) / 365.25)
    diur = amp * np.cos(2 * np.pi * (hod - 15.0) / 24.0)
    # weather systems: daily AR(1), larger in winter
    dates = [C.to_local(C.T0).date() + dt.timedelta(days=int(d)) for d in range(nd)]
    ddoy = np.array([d.timetuple().tm_yday for d in dates], float)
    sig = 3.2 + 2.6 * (0.5 + 0.5 * np.cos(2 * np.pi * (ddoy - 15) / 365.25))
    an = np.zeros(nd)
    for d in range(1, nd):
        an[d] = 0.78 * an[d - 1] + sig[d] * np.sqrt(1 - 0.78 ** 2) * rng.normal()
    # arctic outbreaks and heat waves (start, days, depth), uneven in shape
    episodes = [(dt.date(2022, 1, 19), 6, -12.5), (dt.date(2022, 12, 20), 5, -13.0), (dt.date(2023, 2, 1), 4, -10.5),
                (dt.date(2024, 1, 12), 9, -14.0), (dt.date(2024, 12, 9), 4, -10.0), (dt.date(2025, 2, 16), 7, -14.0),
                (dt.date(2026, 1, 21), 8, -15.0), (dt.date(2023, 12, 30), 3, -8.5), (dt.date(2025, 1, 6), 4, -9.5),
                (dt.date(2022, 6, 13), 5, 4.6), (dt.date(2022, 7, 19), 6, 4.2), (dt.date(2023, 6, 1), 4, 3.8),
                (dt.date(2023, 8, 20), 5, 4.4), (dt.date(2024, 6, 16), 4, 4.1), (dt.date(2024, 8, 25), 4, 4.5),
                (dt.date(2025, 6, 20), 5, 4.8), (dt.date(2025, 7, 24), 7, 4.4), (dt.date(2026, 6, 8), 4, 4.0),
                (dt.date(2026, 7, 13), 6, 4.7), (dt.date(2026, 8, 24), 3, 3.6)]
    d0 = C.to_local(C.T0).date()
    for st, n, depth in episodes:
        i0 = (st - d0).days
        shape = np.sin(np.linspace(0.15, np.pi - 0.1, n)) ** 0.8 * (1 + 0.15 * rng.normal(size=n))
        for k in range(n):
            if 0 <= i0 + k < nd:
                an[i0 + k] += depth * shape[k]
    # hourly anomaly by interpolating the daily values, plus hourly noise
    x = days + hod / 24.0
    a_h = np.interp(x, np.arange(nd) + 0.5, an)
    temp = seas + diur + a_h + 0.6 * rng.normal(size=H)
    # thunderstorms: storm days in the warm season, onset in the afternoon or evening, a few severe wind events
    storm = np.zeros(H)
    thunder = np.zeros(H, bool)
    gust_add = np.zeros(H)
    precip = np.zeros(H)
    severe_days = []
    for d in range(nd):
        dd = dates[d]
        doy_d = dd.timetuple().tm_yday
        p = 0.31 * np.exp(-((doy_d - 188) / 40.0) ** 2)
        if rng.random() < p:
            n_cells = 1 + rng.poisson(0.6)
            sev = rng.random() < 0.075
            if sev:
                severe_days.append(dd)
            for _ in range(n_cells):
                start = rng.normal(17.5, 3.0)
                start = min(23.5, max(11.0, start))
                dur = rng.uniform(0.8, 4.5) * (1.4 if sev else 1.0)
                inten = rng.gamma(2.2, 0.32) * (3.2 if sev else 1.0)
                mask = (x >= d + start / 24.0) & (x < d + (start + dur) / 24.0)
                storm[mask] = np.maximum(storm[mask], inten)
                thunder[mask] = True
                gust_add[mask] = np.maximum(gust_add[mask], 25 + 32 * inten + 8 * rng.normal())
                precip[mask] += rng.gamma(1.4, 2.6 * (0.5 + inten), size=mask.sum())
                temp[mask] -= rng.uniform(2.0, 6.0)
    # winter clippers (wind) and freezing rain
    ice = np.zeros(H)
    for d in range(nd):
        dd = dates[d]
        if dd.month in (11, 12, 1, 2, 3) and rng.random() < 0.035:
            start = rng.uniform(0, 20)
            dur = rng.uniform(5, 14)
            mask = (x >= d + start / 24.0) & (x < d + (start + dur) / 24.0)
            gust_add[mask] = np.maximum(gust_add[mask], rng.uniform(42, 70))
            storm[mask] = np.maximum(storm[mask], 0.25)
    for st, n, inten in [(dt.date(2023, 2, 21), 2, 1.1), (dt.date(2024, 12, 27), 1, 0.8), (dt.date(2026, 3, 12), 1, 0.9)]:
        i0 = (st - d0).days
        mask = (x >= i0 + 0.3) & (x < i0 + n + 0.1)
        ice[mask] = inten
        precip[mask] += 0.8
    wind = np.clip(rng.gamma(3.0, 4.2, size=H) + 4 * np.cos(2 * np.pi * (doy - 80) / 365.25), 0, None)
    gust = np.where(gust_add > 0, np.maximum(gust_add, wind * 1.4), np.where(rng.random(H) < 0.3, wind * 1.5, 0))
    dew = temp - np.clip(rng.gamma(2.0, 2.5, size=H), 0.5, None) - 2 * (temp > 20)
    return {'H': H, 'ts': ts_utc, 'temp': temp, 'storm': storm, 'thunder': thunder, 'gust': gust, 'wind': wind,
            'precip': precip, 'ice': ice, 'dew': dew, 'hod': hod, 'doy': doy, 'severe_days': severe_days,
            'local': loc}
