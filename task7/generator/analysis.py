"""The estimators, on what the pack shows (an Obs object: customer-meter sums, head meters where installed, the far-end
meters' hourly minimum voltage, the LTC tap log, the trial's regulator log and assignment, weather, the survey, the
register), each with a switch for its hurried reading. J1 the trial read on the volts achieved (else on assignment);
J2 each feeder's own response from its bus's tap changes (else the trial feeders' average); J3 the energy response by
season and hour with the thermostatic give-back (else the trial's shoulder figure carried flat); J4 the volts each
feeder can give hour by hour from its far-end meters (else the trial's 4 percent); J5 the losses from a fitted I^2 R
model (else the annual report's 6.1 percent added in proportion)."""
import math

import numpy as np

import params as P

GOLD = {1: True, 2: True, 3: True, 4: True, 5: True}
# the analyst's settings a rival may choose differently (the golden family varies them)
OPT = dict(cop=12100 / 4350, whkw=3200 / 8.76e6, quad=True, win=2, ctrl="class", tctl="class", comp=None, lam=1.0, lossk=1.0, room=0.0)


def reset():
    """clear every cached estimate (between golden-family members)"""
    for fn in (tap_events, pooled_exponents, makeup, eta_structural, saving2, saving):
        d = fn.__defaults__
        if d:
            for x in d:
                if isinstance(x, dict):
                    x.clear()
SEASON = np.array([0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 0])          # DJF, MAM, JJA, SON by month
MONTH_OF_DAY = None


def months():
    import datetime as dt
    return np.array([(P.T0 + dt.timedelta(days=d)).month for d in range(P.ND)])


def cells():
    """season x time-of-day block for every quarter-hour"""
    m = months()
    s = np.repeat(SEASON[m - 1], P.Q)
    b = np.tile(np.arange(P.Q) // 24, P.ND)                        # 00-06, 06-12, 12-18, 18-24
    return s * 4 + b


CELL = None


def trial_effect(O, f, use_dose):
    """per unit change in daily energy per per unit volt on a trial feeder: its daily customer energy over the untested
    feeders' on the same day, on the trial days, regressed on the day's achieved reduction (or its assignment) with
    heating, cooling and weekend terms"""
    days = O.trial_days
    E = O.ami[f].reshape(P.ND, P.Q).sum(axis=1)[days]
    peers = [g for g in range(P.NF) if g not in O.trial and (O.kind[g] == O.kind[f] or OPT["tctl"] == "all")] or [g for g in range(P.NF) if g not in O.trial]
    ctl = sum(O.ami[g] for g in peers).reshape(P.ND, P.Q).sum(axis=1)[days]
    y = E / ctl
    tm = O.T.reshape(P.ND, 24).mean(axis=1)[days]
    hdd, cdd = np.clip(58 - tm, 0, None), np.clip(tm - 68, 0, None)
    wk = (((days + 3) % 7) >= 5).astype(float)
    x = (O.dose_daily[f][days] / P.VNOM) if use_dose else O.assign[f][days] * (P.TRIAL_DV / P.VNOM)
    X = np.column_stack([np.ones(len(days)), x, hdd, cdd, hdd ** 2, cdd ** 2, wk]) if OPT["quad"] else np.column_stack([np.ones(len(days)), x, hdd, cdd, wk])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return -b[1] / np.mean(y)


def tap_response(O, f):
    """the per unit change in a feeder's load per per unit volt in the half hour after each tap of its bus, net of the
    same feeder's change over the same quarters on that month's other days of the same kind (weekday or weekend) with
    no tap near that time, by season and time-of-day block"""
    global CELL
    if CELL is None:
        CELL = cells()
    S = O.ami[f]
    sub = O.sub[f]
    Sd = S.reshape(P.ND, P.Q)
    tq = O.tap_q[sub]
    near = np.zeros((P.ND, P.Q), dtype=bool)
    for (q, step) in tq:
        for qq in range(q - 3, q + 4):
            if 0 <= qq < P.NQ:
                near[qq // P.Q, qq % P.Q] = True
    m = months()
    wkd = ((np.arange(P.ND) + 3) % 7) >= 5
    acc = [[] for _ in range(16)]
    qs = np.array([q for q, _ in tq])
    V = O.vbus[sub]
    for (q, step) in tq:
        d, k = q // P.Q, q % P.Q
        if k < 2 or k > P.Q - 3:
            continue
        if ((qs >= q - 3) & (qs <= q + 3)).sum() > 1:              # another tap too close to read this one cleanly
            continue
        if f in O.trial and O.dose_q[f][q - 2:q + 3].max() > 0:
            continue
        rel = Sd[d, k + 1:k + 3].mean() / Sd[d, k - 2:k].mean() - 1
        same = (m == m[d]) & (wkd == wkd[d]) & ~near[:, k]
        same[d] = False
        base = (Sd[same, k + 1:k + 3].mean(axis=1) / Sd[same, k - 2:k].mean(axis=1) - 1).mean()
        dv = (V[q + 1:q + 3].mean() - V[q - 2:q].mean()) / P.VNOM   # the step the bus SCADA recorded
        if abs(dv) * P.VNOM < 0.2:
            continue
        acc[CELL[q]].append((rel - base, dv))
    est = []
    for a in acc:
        if len(a) < 5:
            est.append(np.nan)
            continue
        y, x = np.array(a).T
        est.append(float((x * y).sum() / (x * x).sum()))
    return np.array(est), np.array([len(a) for a in acc])


def thermostatic_share(O, f):
    """the share of each season-block's load that is thermostatic resistive: electric water heating (about 0.45 kW a
    heater on average) and resistive space heat (the feeder's heating load split by the survey's holdings, a resistive
    home drawing about 2.8 times a heat pump home for the same heat)"""
    global CELL
    if CELL is None:
        CELL = cells()
    sv = O.survey[f]
    S = O.ami[f] * 4
    lvl = np.array([S[CELL == c].mean() for c in range(16)])
    spring = lvl[4:8]
    heat = np.clip(lvl - np.tile(spring, 4), 0, None)
    heat[4:12] = 0.0                                                # spring is the reference; summer's excess is cooling
    rs = sv["sat_res_heat"] * 2.8 / max(sv["sat_res_heat"] * 2.8 + sv["sat_hp"], 1e-9)
    wh = sv["sat_ewh"] * O.cust[f] * 0.00045
    return np.clip((heat * rs + wh) / lvl, 0, 1)


def headroom(O, f, J4):
    """volts the program can take off, hour by hour: the far-end meters' lowest reading less 115 V, at most 4.8 V"""
    if not J4:
        return np.full(P.ND * 24, P.TRIAL_DV)
    v = O.vmin_h[f].copy()
    if f in O.trial:                                                # the trial's ON days, back to normal running
        v = v + O.dose_q[f].reshape(-1, 4).mean(axis=1)
    return np.clip(v + OPT["room"] - (P.VMIN + P.MARGIN), 0, P.DVMAX)


def loss_k(O):
    """the lumped loss coefficient from the head-metered feeders: head less customers against S^2 r L"""
    xs, ys = [], []
    for f in O.headmetered:
        S = O.ami[f] * 4                        # MW
        L = O.head[f] * 4 - S
        x = S ** 2 * O.r[f] * O.L[f] / (P.KV ** 2) * (P.VNOM / O.vmin_h_head[f]) ** 2
        xs.append(x)
        ys.append(L)
    x, y = np.concatenate(xs), np.concatenate(ys)
    return float((x * y).sum() / (x * x).sum())


def saving(O, f, J, cache={}):
    """annual MWh at the substation if the feeder gets voltage optimization, under judgment set J"""
    key = (id(O), "trial", J[1])
    if key not in cache:
        cache[key] = {g: trial_effect(O, g, J[1]) for g in O.trial}
    tr = cache[key]
    trial_avg = np.mean(list(tr.values()))
    key2 = (id(O), "tap")
    if key2 not in cache:
        cache[key2] = {g: tap_response(O, g)[0] for g in range(P.NF)}
    taps = cache[key2]
    key3 = (id(O), "th")
    if key3 not in cache:
        cache[key3] = {g: thermostatic_share(O, g) for g in range(P.NF)}
    th = cache[key3]
    # the give-back: on the trial feeders the spring and autumn taps against the trial's energy figure, per unit of
    # thermostatic share
    key4 = (id(O), "g", J[1])
    if key4 not in cache:
        xs, ys = [], []
        for g in O.trial:
            sh = np.nanmean(taps[g][4:8]) * 0.5 + np.nanmean(taps[g][12:16]) * 0.5
            ths = np.nanmean(np.r_[th[g][4:8], th[g][12:16]])
            xs.append(ths)
            ys.append(sh - tr[g])
        xs, ys = np.array(xs), np.array(ys)
        cache[key4] = float((xs * ys).sum() / (xs * xs).sum())
    gb = cache[key4]
    global CELL
    if CELL is None:
        CELL = cells()
    S = O.ami[f] * 4                                               # MW by quarter
    dvh = headroom(O, f, J[4])
    dvq = np.repeat(dvh, 4) / P.VNOM
    if J[2] or f in O.trial:
        if J[3]:
            resp = taps[f] - gb * th[f]
            resp = np.where(np.isnan(resp), np.nanmean(resp), resp)
            if f in O.trial:                                       # its own trial fixes the level in spring and autumn
                sho = np.r_[4:8, 12:16]
                resp = resp + (tr[f] - resp[sho].mean())
            eta = resp[CELL]
        else:
            eta = np.full(P.NQ, tr[f] if f in O.trial else np.nanmean(taps[f][[4, 5, 6, 7, 12, 13, 14, 15]]) - gb * np.nanmean(
                th[f][[4, 5, 6, 7, 12, 13, 14, 15]]))
    else:
        eta = np.full(P.NQ, trial_avg)
    dcust = eta * dvq * S
    if J[5]:
        k = loss_k(O)
        V0 = O.vmin_h_head[f]
        S1 = S - dcust
        V1 = V0 - np.repeat(dvh, 4)
        l0 = k * S ** 2 * O.r[f] * O.L[f] / (P.KV ** 2) * (P.VNOM / V0) ** 2
        l1 = k * S1 ** 2 * O.r[f] * O.L[f] / (P.KV ** 2) * (P.VNOM / V1) ** 2
        dl = l0 - l1
    else:
        dl = P.LOSS_RATE_REPORT * dcust
    return float((dcust + dl).sum() * 0.25)


def call(O, J):
    return tuple(f for f in range(P.NF) if saving(O, f, J) * P.PRICE * P.ANNUITY >= O.cost[f])


# ---- the structural route: each feeder's makeup, the response of each load type pooled over every tap event ------------
CLASS = ("res", "com", "rural")


def weather_split(O, f, keep={}):
    """the feeder's heating and cooling load: its quarter-hour load regressed on a quarter-of-day by day-type profile
    plus heating degrees (below 58 F) and cooling degrees (above 68 F, by daytime and night)"""
    if (id(O), f) in keep:
        return keep[(id(O), f)]
    S = O.ami[f] * 4
    Tq = np.interp(np.arange(P.NQ) / 4.0, np.arange(len(O.T)) + 0.5, O.T)
    hdd, cdd = np.clip(58 - Tq, 0, None), np.clip(Tq - 68, 0, None)
    qod = np.tile(np.arange(P.Q), P.ND)
    wkd = np.repeat(((np.arange(P.ND) + 3) % 7) >= 5, P.Q)
    day = (qod >= 36) & (qod < 88)
    grp = qod + P.Q * wkd
    # the profile dummies are absorbed by demeaning within each quarter-of-day and day type, then the three slopes fitted
    Xw = np.column_stack([hdd, cdd * day, cdd * ~day])
    Sm, Xm = S.copy(), Xw.copy()
    for g in range(2 * P.Q):
        k = grp == g
        Sm[k] -= S[k].mean()
        Xm[k] -= Xw[k].mean(axis=0)
    b = np.linalg.lstsq(Xm, Sm, rcond=None)[0]
    heat = np.clip(b[0], 0, None) * hdd
    cool = np.clip(b[1], 0, None) * cdd * day + np.clip(b[2], 0, None) * cdd * ~day
    keep[(id(O), f)] = (heat, cool)
    return heat, cool


def makeup(O, f, cache={}):
    """shares of each quarter-hour's load: base, thermostatic resistive, heat pumps, cooling. The feeder's load is
    regressed on its quarter-of-day by day-type profile plus heating degrees (below 58 F) and cooling degrees (above
    68 F, by daytime and night): the weather terms are its heating and cooling load; heating is split between resistive
    heat and heat pumps by the survey's holdings (a resistive home drawing about 2.8 times a heat pump home for the same
    heat); water heating, about 0.36 kW a heater of the survey's holding, sits inside the base"""
    if (id(O), f) in cache:
        return cache[(id(O), f)]
    S = O.ami[f] * 4
    heat, cool = weather_split(O, f)
    sv = O.survey[f]
    rs = sv["sat_res_heat"] * OPT["cop"] / max(sv["sat_res_heat"] * OPT["cop"] + sv["sat_hp"], 1e-9)
    base_all = np.clip(S - heat - cool, 1e-6, None)
    wh = np.minimum(sv["sat_ewh"] * O.cust[f] * OPT["whkw"], 0.6 * base_all)
    sh = dict(base=(base_all - wh) / S, TH=(wh + heat * rs) / S, HP=heat * (1 - rs) / S, AC=cool / S)
    cache[(id(O), f)] = sh
    return sh


def tap_events(O, cache={}):
    """every clean tap event on every feeder: its quarter, its response net of the same quarters' change on the
    same-class feeders of the other substations that had no tap near that time, and the step the bus SCADA recorded"""
    if id(O) in cache:
        return cache[id(O)]
    near = {}
    for sub in P.SUBSTATIONS:
        nz = np.zeros(P.NQ, dtype=bool)
        for q, _ in O.tap_q[sub]:
            nz[max(0, q - 3):q + 4] = True
        near[sub] = nz
    out = []
    for f in range(P.NF):
        S = O.ami[f]
        sub = O.sub[f]
        tq = O.tap_q[sub]
        qs = np.array([q for q, _ in tq])
        V = O.vbus[sub]
        peers = [g for g in range(P.NF) if O.kind[g] == O.kind[f] and O.sub[g] != sub]
        for q in qs:
            if q < 3 or q > P.NQ - 4 or ((qs >= q - 3) & (qs <= q + 3)).sum() > 1:
                continue
            if f in O.trial and O.dose_q[f][q - 2:q + 3].max() > 0:
                continue
            e = 1 + OPT["win"]
            dv = (V[q + 1:q + e].mean() - V[q - 2:q].mean()) / P.VNOM
            if abs(dv) * P.VNOM < 0.2:
                continue
            pool = peers if OPT["ctrl"] == "class" else [g for g in range(P.NF) if O.sub[g] != sub]
            ctl = [O.ami[g][q + 1:q + e].mean() / O.ami[g][q - 2:q].mean() - 1 for g in pool
                   if not near[O.sub[g]][q] and not (g in O.trial and O.dose_q[g][q - 2:q + 3].max() > 0)]
            if len(ctl) < 2:
                continue
            rel = S[q + 1:q + e].mean() / S[q - 2:q].mean() - 1
            out.append((f, q, rel - float(np.mean(ctl)), dv))
    cache[id(O)] = out
    return out


def pooled_exponents(O, cache={}):
    """the response of each load type in the half hour after a step: every event's response regressed (through the
    origin, weighted by the step) on its quarter's makeup, the base split by class"""
    if id(O) in cache:
        return cache[id(O)]
    ev = tap_events(O)
    mk = {f: makeup(O, f) for f in range(P.NF)}
    rows, ys = [], []
    for (f, q, y, dv) in ev:
        sh = mk[f]
        x = [sh["base"][q], sh["TH"][q], sh["HP"][q] + sh["AC"][q]]
        rows.append(np.array(x) * dv)
        ys.append(y)
    X, Y = np.array(rows), np.array(ys)
    from scipy.optimize import lsq_linear
    b = lsq_linear(X, Y, bounds=(0.0, 2.5)).x                      # a load's voltage exponent lies between 0 and 2.5
    k = dict(zip(["base", "TH_win", "COMP"], b))
    if OPT["comp"] is not None:                                     # a compressor response taken from engineering tables
        k["COMP"] = OPT["comp"] * k["base"]
    k["base_res"] = k["base_com"] = k["base_rural"] = k["base"]
    k["HP"] = k["AC"] = k["COMP"]                                   # compressors: heat pumps and air conditioners alike
    cache[id(O)] = k, mk
    return cache[id(O)]


def eta_structural(O, f, J, cache={}):
    """the feeder's energy response by quarter-hour: thermostatic load (water heating, resistive heat) gives its energy
    back over the day, every other load answers in proportion to its share; the proportion is the trial's: on the trial
    feeders' trial days the structure reproduces what the trial measured"""
    sh = makeup(O, f)
    def nonth(g):
        m = makeup(O, g)
        return m["base"] + m["HP"] + m["AC"]
    key = (id(O), J[1])
    if key not in cache:
        sel = np.zeros(P.NQ, bool)
        for d in O.trial_days:
            sel[d * P.Q:(d + 1) * P.Q] = True
        ratios = []
        for g in O.trial:
            wS = O.ami[g][sel]
            ratios.append(trial_effect(O, g, J[1]) / float((nonth(g)[sel] * wS).sum() / wS.sum()))
        cache[key] = float(np.median(ratios))                       # one noisy trial feeder does not set the scale
    return nonth(f) * cache[key] * OPT["lam"]


def saving2(O, f, J, cache={}):
    """annual MWh at the substation, the structural route"""
    key = (id(O), "tr", J[1])
    if key not in cache:
        cache[key] = {g: trial_effect(O, g, J[1]) for g in O.trial}
    tr = cache[key]
    S = O.ami[f] * 4
    sel = np.zeros(P.NQ, bool)
    for d in O.trial_days:
        sel[d * P.Q:(d + 1) * P.Q] = True
    if J[2] or f in O.trial:
        eta = eta_structural(O, f, J)
        if not J[3]:
            eta = np.full(P.NQ, float((eta[sel] * S[sel]).sum() / S[sel].sum()) if f not in O.trial else tr[f])
    else:
        eta = np.full(P.NQ, float(np.mean(list(tr.values()))))
        if J[3]:
            pass                                                       # without its own makeup there is no shape to carry
    dvh = headroom(O, f, J[4])
    dvq = np.repeat(dvh, 4) / P.VNOM
    dcust = eta * dvq * S
    if J[5]:
        kl = loss_k(O) * OPT["lossk"]
        V0 = O.vmin_h_head[f]
        S1 = S - dcust
        V1 = V0 - np.repeat(dvh, 4)
        l0 = kl * S ** 2 * O.r[f] * O.L[f] / (P.KV ** 2) * (P.VNOM / V0) ** 2
        l1 = kl * S1 ** 2 * O.r[f] * O.L[f] / (P.KV ** 2) * (P.VNOM / V1) ** 2
        dl = l0 - l1
    else:
        dl = P.LOSS_RATE_REPORT * dcust
    return float((dcust + dl).sum() * 0.25)


def call2(O, J):
    return tuple(f for f in range(P.NF) if saving2(O, f, J) * P.PRICE * P.ANNUITY >= O.cost[f])
