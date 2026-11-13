"""Hourly load on the 69 kV lines: each tap's member demand from its own temperature and the hour (air conditioning
on summer afternoons, electric heat on winter mornings), the flows that carry it from the two bulk stations, the solar
farm's output on the Shell Ridge-Ponder Creek tap, each line's current at its A terminal (signed by direction) and the
power angle across it, and the conductor's temperature from a steady-state heat balance (current squared on the
conductor's resistance at its temperature, the sun, convection on the wind across it, radiation)."""
import math

import numpy as np

import common as C
import network as N
import weather as W

V_LL = 69.0e3
PF = 0.96
# meshed through-flow the taps alone do not show: each line's current scaled by the flow the 69 kV mesh routes over it
MESH = {'L01': 1.05, 'L02': 1.0, 'L03': 1.35, 'L04': 1.6, 'L05': 2.3, 'L06': 2.6, 'L07': 1.6, 'L08': 1.3, 'L09': 1.0,
        'L10': 1.25, 'L11': 2.6, 'L12': 2.5, 'L13': 2.2, 'L14': 2.6, 'L15': 1.9, 'L16': 6.0}
# which lines carry each line's flow: the downstream lines each line also feeds (a share of their load), and the
# direction the flow runs (+1 A to B)
THROUGH = {
    'L01': (['L02', 'L16'], 0.55, +1), 'L02': (['L03', 'L09'], 0.40, +1), 'L03': ([], 0.0, +1),
    'L04': (['L05'], 0.45, +1), 'L05': (['L13'], 0.25, +1), 'L06': (['L07', 'L16'], 0.45, +1),
    'L07': (['L08', 'L12'], 0.35, +1), 'L08': ([], 0.0, +1), 'L09': ([], 0.0, +1),
    'L10': (['L15', 'L12'], 0.55, +1), 'L11': (['L13'], 0.45, +1), 'L12': ([], 0.0, -1),
    'L13': ([], 0.0, +1), 'L14': (['L08'], 0.45, +1), 'L15': (['L05'], 0.30, +1), 'L16': (['L07'], 0.30, -1),
}


def member_kw(temp, hour, month):
    """average kW per member at a temperature and hour"""
    diurnal = 0.55 + 0.45 * np.clip(np.sin(math.pi * (hour - 6) / 16.0), 0, None)
    cool = 0.115 * np.clip(temp - 21.0, 0, None) * (0.55 + 0.45 * np.clip(np.sin(math.pi * (hour - 9) / 12.0), 0, None))
    heat = 0.06 * np.clip(10.0 - temp, 0, None) * (1.0 + 0.5 * ((hour >= 5) & (hour <= 9)))
    return 0.85 + 1.15 * diurnal + cool + heat


def simulate(net, wx):
    rng = np.random.default_rng(C.SEED + 7)
    nh = C.NH
    hour, month, year = wx['hour'], wx['month'], wx['year']
    growth = 1.0 + 0.016 * (year - 2022) + 0.016 * (wx['doy'] / 365.0)
    tap_mw = {}
    for tp in net['taps']:
        line = net['lines'][tp['line']]
        st = N.structure_at(net, tp['line'], tp['km'])
        # the tap's temperature: the nearest simulated place
        best = min(W.PLACES, key=lambda c: math.hypot(W.PLACES[c][0] - st['x'], W.PLACES[c][1] - st['y']))
        temp = wx['series'][best]['temp']
        kw = member_kw(temp, hour, month) * (1.0 + rng.normal(0, 0.03, nh))
        tap_mw[tp['name']] = tp['members'] * kw * growth / 1000.0
    line_load = {lid: np.zeros(nh) for lid in net['lines']}
    for tp in net['taps']:
        line_load[tp['line']] += tap_mw[tp['name']]
    # the solar farm: clear-sky shape times a cloud factor, 60 MW AC, from its energization
    solar = np.zeros(nh)
    e0 = C.hour_index(C.SOLAR_ENERGIZED)
    doy = wx['doy']
    for h in range(e0, nh):
        lh = hour[h]
        day_len = 12.2 + 1.8 * math.sin(2 * math.pi * (doy[h] - 80) / 365.25)
        rise = 12.6 - day_len / 2
        x = (lh + 0.5 - rise) / day_len
        if 0 < x < 1:
            cloud = 1.0 - 0.6 * min(1.0, wx['series']['SHR']['precip'][h] / 2.0) - 0.15 * rng.random()
            solar[h] = 60.0 * math.sin(math.pi * x) ** 1.3 * max(0.1, cloud)
    flow = {}
    order = ['L03', 'L08', 'L09', 'L12', 'L13', 'L16', 'L02', 'L05', 'L07', 'L14', 'L15', 'L11', 'L01', 'L04', 'L06', 'L10']
    for lid in order:
        down, share, sign = THROUGH[lid]
        mw = line_load[lid].copy()
        for d in down:
            mw += share * flow.get(d, line_load[d])
        if lid == 'L09':
            mw = mw - 0.65 * solar          # the farm's output runs toward Shell Ridge
        if lid == 'L02':
            mw = mw - 0.25 * solar
        flow[lid] = mw
    out = dict(tap_mw=tap_mw, solar=solar, mw={}, amps={}, delta={})
    for lid in net['lines']:
        down, share, sign = THROUGH[lid]
        mw = flow[lid] * sign * MESH[lid]
        amps = np.abs(mw) * 1e6 / (math.sqrt(3) * V_LL * PF)
        line = net['lines'][lid]
        za1, _ = N.source(lid, line['a'])
        zb1, _ = N.source(lid, line['b'])
        x_tot = (za1 + line['z1'] * line['length'] + zb1).imag
        delta = np.degrees(mw * 1e6 * x_tot / V_LL ** 2)     # power angle across the two-source equivalent, A ahead
        out['mw'][lid] = mw
        out['amps'][lid] = amps * (1.0 + rng.normal(0, 0.012, nh))
        out['delta'][lid] = delta
    return out


def conductor_temp(i_amps, cond, t_air, wind, solar_wm2):
    """steady-state conductor temperature (deg C) from the heat balance, solved by bisection"""
    cd = N.CONDUCTORS[cond]
    d = cd['d_mm'] / 1000.0
    alpha = (cd['r75'] / cd['r25'] - 1.0) / 50.0
    v = max(0.3, wind)

    def resid(tc):
        tf = (tc + t_air) / 2.0
        kf = 2.424e-2 + 7.477e-5 * tf
        mu = (1.458e-6 * (tf + 273.0) ** 1.5) / (tf + 383.4)
        rho = 1.165
        re = d * rho * v / mu
        qc = max(1.01 + 1.35 * re ** 0.52, 0.754 * re ** 0.6) * kf * (tc - t_air)
        qr = 17.8 * d * 0.5 * (((tc + 273.0) / 100.0) ** 4 - ((t_air + 273.0) / 100.0) ** 4)
        qs = 0.5 * solar_wm2 * d
        qj = i_amps ** 2 * cd['r25'] / 1000.0 * (1.0 + alpha * (tc - 25.0))
        return qj + qs - qc - qr

    lo, hi = t_air, t_air + 150.0
    for _ in range(40):
        mid = (lo + hi) / 2.0
        if resid(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def solar_irradiance(h, wx, code='MSQ'):
    """W per square metre on the conductor: a clear-sky shape cut by rain"""
    lh = wx['hour'][h]
    doy = wx['doy'][h]
    day_len = 12.2 + 1.8 * math.sin(2 * math.pi * (doy - 80) / 365.25)
    rise = 12.6 - day_len / 2
    x = (lh + 0.5 - rise) / day_len
    if not 0 < x < 1:
        return 0.0
    peak = 780.0 + 220.0 * math.sin(2 * math.pi * (doy - 80) / 365.25)
    cut = 1.0 - 0.7 * min(1.0, wx['series'][code]['precip'][h] / 1.5)
    return peak * math.sin(math.pi * x) * cut
