"""Hourly load on every main-line section: households and businesses, each with its own daily and weekly shape,
cooling that rises steeply with the afternoon heat (a three-hour lag on the air temperature), a little electric
heat, growth by section (new subdivisions with their evening car charging), and noise. Amps at 13.8 kV."""
import datetime as dt

import numpy as np

import common as C
import net as N

KV = 13.8
PF = 0.96


def _shapes(W):
    hod = W['hod']
    loc = W['local']
    wd = np.array([t.weekday() for t in loc])
    res_base = 0.92 + 0.22 * np.exp(-((hod - 7.5) / 1.6) ** 2) + 0.48 * np.exp(-((hod - 19.5) / 2.6) ** 2) \
        - 0.24 * np.exp(-((hod - 3.5) / 2.2) ** 2)
    res_base = res_base * np.where(wd >= 5, 1.05, 1.0)
    cool_shape = 0.45 + 0.55 * np.exp(-((hod - 17.5) / 3.8) ** 2)
    com = np.where((wd < 5) & (hod >= 7) & (hod < 19), 1.0, 0.42) * (0.9 + 0.1 * np.cos(2 * np.pi * (hod - 13) / 24))
    ev_shape = np.exp(-((hod - 21.0) / 2.2) ** 2) + 0.35 * np.exp(-((hod - 1.0) / 1.8) ** 2)
    return res_base, cool_shape, com, ev_shape


def simulate(NET, W):
    rng = np.random.default_rng(C.SEED + 7)
    H = W['H']
    T = W['temp']
    # thermal lag: an exponential smoothing of the air temperature
    Te = np.empty(H)
    Te[0] = T[0]
    for h in range(1, H):
        Te[h] = Te[h - 1] + (T[h] - Te[h - 1]) / 3.0
    res_base, cool_shape, com, ev_shape = _shapes(W)
    cool = np.clip(Te - 17.5, 0, None) ** 1.15 * cool_shape
    heat = np.clip(4.0 - Te, 0, None)
    yearfrac = np.array([t.year + (t.timetuple().tm_yday - 1) / 365.25 for t in W['local']])
    recon = {r['feeder']: r for r in NET['recon']}
    amps = {}
    cust = {}
    for f in NET['fids']:
        F = NET['feeders'][f]
        res_s = F['res_share']
        cool_k = rng.uniform(0.072, 0.098)
        heat_k = rng.uniform(0.012, 0.03)
        for S in F['sections']:
            k = S['s']
            c = np.array([N.section_customers(F, k, y, recon) for y in yearfrac[::24]])
            c = np.repeat(c, 24)[:H]
            ev = np.zeros(H)
            if S['boom_from'] is not None:
                ev = 0.22 * np.clip(yearfrac - S['boom_from'], 0, None) * ev_shape
            per = res_s * (res_base + cool_k * cool + heat_k * heat + ev) + (1 - res_s) * 3.1 * com * \
                (1 + 0.022 * np.clip(Te - 20, 0, None))
            noise = np.exp(0.035 * rng.normal(size=H))
            kw = c * per * noise
            amps[(f, k)] = kw / (np.sqrt(3) * KV * PF)
            cust[(f, k)] = c
    return {'amps': amps, 'cust': cust, 'yearfrac': yearfrac}


def device_flow(L, f, kind):
    """current through a device in the normal configuration: CB carries all three sections, R1 sections 2 and 3,
    R2 section 3"""
    a = L['amps']
    if kind == 'CB':
        return sum(a[(f, k)] for k in (1, 2, 3) if (f, k) in a)
    if kind == 'R1':
        return a[(f, 2)] + a[(f, 3)]
    if kind == 'R2':
        return a[(f, 3)]
    raise ValueError(kind)
