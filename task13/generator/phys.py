"""Lightning flashover physics on a zone's lines: a direct strike when the stroke lands inside the line's attractive
radius and no tree or building intercepts it; otherwise an induced flashover when the induced voltage beats the
line's insulation, raised where a working arrester with its ground lead clamps the surge."""
import numpy as np
import pandas as pd

import geo as G
import net as NET

K_IND = 38.8 * 1.35      # Rusck's peak induced voltage per kA x m / m, with a lossy-ground factor
CLAMP = 9.0              # a working, grounded arrester raises the flashover threshold this much near it
COVER_KM = 0.32          # each arrester protects about this much line


def contacts(St):
    """ground contacts: first strokes and subsequent strokes that made a new channel"""
    c = St[(St.k == 0) | St.new_contact].copy()
    return c


def pairs(N, St, rmax=0.6):
    """every (contact, zone) within rmax km, at the zone's nearest segment"""
    c = contacts(St)
    idx = G.SegIndex(N['S'], 1.0)
    p, s, d = idx.near(c.x.values, c.y.values, rmax)
    S = N['S']
    P = pd.DataFrame({'ci': p, 'seg': s, 'd': d})
    P['zone_ix'] = S.zone_ix.values[s]
    P = P.sort_values('d').drop_duplicates(['ci', 'zone_ix'])
    P['stroke'] = c.stroke.values[P.ci.values]
    P['flash'] = c.flash.values[P.ci.values]
    P['t'] = c.t.values[P.ci.values]
    P['I'] = np.abs(c.I.values[P.ci.values])
    return P.reset_index(drop=True)


def fault_prob(P, S, state_cov, state_cfo, rng=None):
    """probability that each contact faults its zone, given each segment's arrester cover and insulation factor
    (arrays over segments: share of the segment's line inside a working arrester's reach; CFO multiplier)"""
    seg = P.seg.values
    h = S.height.values[seg]
    sf = S.setting.map(NET.SHIELD).values[seg]
    I = P.I.values
    dm = np.maximum(P.d.values * 1000.0, 1.0)
    r_att = 0.67 * h ** 0.6 * I ** 0.74
    direct = dm < r_att
    p_direct = np.where(direct, 1 - sf, 0.0)
    # strikes intercepted by trees or buildings, or landing outside the attractive radius, induce a surge
    deff = np.where(direct, np.maximum(dm, 12.0), dm)
    V = K_IND * I * h / deff
    cfo = S.cfo.values[seg] * state_cfo[seg]
    cov = state_cov[seg]
    thr_open = 1.5 * cfo
    thr_clamp = 1.5 * cfo * CLAMP
    # a statistical insulation strength: lognormal scatter of 12 per cent
    from scipy.stats import norm
    p_ind_open = norm.cdf(np.log(V / thr_open) / 0.12)
    p_ind_clamp = norm.cdf(np.log(V / thr_clamp) / 0.12)
    p_ind = (1 - cov) * p_ind_open + cov * p_ind_clamp
    p_fault_point = p_direct + (1 - p_direct) * p_ind
    return 0.92 * p_fault_point


def sound_cover(S):
    return np.clip(S.tx_per_km.values * COVER_KM, 0, 0.97)
