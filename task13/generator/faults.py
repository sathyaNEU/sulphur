"""Every fault on every zone, December 2021 to October 2026, with the truth of what caused it."""
import numpy as np
import pandas as pd
from scipy.stats import norm

import net as NET
import phys as PH
import world as W

TYPHOONS = [  # (name, landfall-ish time over the network, hours of strong wind, intensity)
    ('Florita', '2022-08-23 03:00', 16, 1.0), ('Karding', '2022-09-25 17:00', 9, 1.6),
    ('Egay', '2023-07-26 06:00', 14, 0.8), ('Jenny', '2023-10-04 20:00', 10, 0.6),
    ('Carina', '2024-07-24 01:00', 18, 0.9), ('Kristine', '2024-10-23 22:00', 20, 1.4), ('Pepito', '2024-11-17 05:00', 12, 1.1),
    ('Emong', '2025-07-24 15:00', 12, 0.9), ('Opong', '2025-09-26 09:00', 15, 1.2),
    ('Basyang', '2026-08-14 11:00', 13, 0.8), ('Caloy', '2026-10-05 02:00', 17, 1.3),
]


def seg_cover(S, Z):
    zi = S.zone_ix.values
    prog = Z.set_index('zone_ix').la_prog.reindex(zi).values & S.setting.isin(['open', 'hill', 'treed']).values
    cov_tx = np.clip(S.tx_per_km.values * PH.COVER_KM, 0, 0.97)
    cov_la = np.where(prog, 0.95, 0.0)
    return cov_tx, cov_la


def state_at(St, zone_ix, t):
    """each pair's zone state (g, a, c) at its time, from the piecewise-constant timelines"""
    out = np.zeros((len(t), 3))
    St = St.sort_values(['zone_ix', 't'])
    for z, idx in pd.Series(np.arange(len(t))).groupby(zone_ix).groups.items():
        s = St[St.zone_ix == z]
        k = np.searchsorted(s.t.values, t[idx], side='right') - 1
        out[idx] = s[['g', 'a', 'c']].values[np.clip(k, 0, None)]
    return out


def lightning_faults(N, Z, P, Stt, rng):
    S = N['S']
    cov_tx, cov_la = seg_cover(S, Z)
    st = state_at(Stt, P.zone_ix.values, P.t.values)
    g, a, c = st[:, 0], st[:, 1], st[:, 2]
    seg = P.seg.values
    cov = 1 - (1 - cov_tx[seg] * g) * (1 - cov_la[seg] * g * a)
    cov_sound = 1 - (1 - cov_tx[seg]) * (1 - cov_la[seg])
    cracked_seg = np.isin(S.construction.values[seg], ['steel_xarm', 'bracket'])
    cfac = np.where(cracked_seg, c, 0.0)
    ones = np.ones(len(S))

    def prob(cov_arr, cfo_mult):
        tmp = P.copy()
        # fault_prob reads the cover per segment; pass it per pair through a segment-indexed array trick
        h = S.height.values[seg]
        sf = S.setting.map(NET.SHIELD).values[seg]
        I = P.I.values
        dm = np.maximum(P.d.values * 1000.0, 1.0)
        r_att = 0.67 * h ** 0.6 * I ** 0.74
        direct = dm < r_att
        # where a working arrester is close, a direct strike's current partly drains through it: half the
        # direct-strike flashovers there do not happen
        p_direct = np.where(direct, 1 - sf, 0.0) * (1 - 0.85 * cov_arr)
        deff = np.where(direct, np.maximum(dm, 12.0), dm)
        V = PH.K_IND * I * h / deff
        cfo = S.cfo.values[seg] * cfo_mult
        p_open = norm.cdf(np.log(V / (1.5 * cfo)) / 0.12)
        p_clamp = norm.cdf(np.log(V / (1.5 * cfo * PH.CLAMP)) / 0.12)
        p_ind = (1 - cov_arr) * p_open + cov_arr * p_clamp
        return 0.92 * (p_direct + (1 - p_direct) * p_ind), p_direct

    p_ok, p_dir = prob(cov, 1.0)
    p_cr, _ = prob(cov, 0.30)
    # what the register does not record: each zone's own susceptibility (soil, pole hardware, the line's exact
    # route against the trees) and a season-to-season part (soil moisture, regrowth)
    zm = Z.set_index('zone_ix').susc.reindex(P.zone_ix.values).values
    yr = pd.to_datetime(P.t.values).year.values
    ss = np.array(Z.sort_values('zone_ix').susc_season.tolist())
    pos = np.searchsorted(Z.zone_ix.sort_values().values, P.zone_ix.values)
    sm = ss[pos, np.clip(yr - 2021, 0, 5)]
    mult = zm * sm
    p = np.clip(((1 - cfac) * p_ok + cfac * p_cr) * mult, 0, 0.97)
    p_snd, _ = prob(cov_sound, 1.0)
    p_snd = np.clip(p_snd * mult, 0, 0.97)
    P = P.copy()
    P['p'] = p
    P['p_sound'] = p_snd
    P['p_cracked_share'] = np.where(p > 0, cfac * p_cr / np.maximum(p, 1e-12), 0)
    P['p_direct'] = 0.92 * p_dir
    # a flash faults a zone at most once (later strokes land while the recloser is open)
    P = P.sort_values(['flash', 'zone_ix', 't'])
    u = rng.random(len(P))
    P['hit'] = u < P.p.values
    first = P[P.hit].drop_duplicates(['flash', 'zone_ix'])
    F = first[['zone_ix', 'flash', 'stroke', 't', 'I', 'd', 'seg', 'p_cracked_share', 'p_direct']].copy()
    F['cause'] = 'lightning'
    # does the fault crack or puncture an insulator, holding it on (permanent)?
    F['on_cracked'] = rng.random(len(F)) < F.p_cracked_share.values
    exp_sound = P.groupby(['zone_ix']).p_sound.sum()
    return F.reset_index(drop=True), P
