"""Platte Ridge PPD's distribution system through 2026, simulated at the quarter-hour: weather, each feeder's load by
component, the substation buses' voltage under their load tap changers, the trial's pilot regulators, the line losses,
the far-end voltages, and the 2027 voltage optimization replayed on a year like 2026 (the clean truth)."""
import math

import numpy as np

import params as P


class World:
    pass


def weather(rng):
    """hourly dry-bulb (deg F) for the district's ASOS station"""
    h = np.arange(P.ND * 24)
    doy = h / 24.0
    seasonal = 52 - 27 * np.cos(2 * np.pi * (doy - 18) / 365)
    diurnal = (9 + 3 * np.cos(2 * np.pi * (doy - 172) / 365)) * np.sin(2 * np.pi * ((h % 24) - 9) / 24)
    syn = np.zeros(len(h))
    e = rng.normal(0, 1, len(h))
    for i in range(1, len(h)):
        syn[i] = 0.985 * syn[i - 1] + 1.1 * e[i]
    return seasonal + diurnal + syn


def feeders(rng):
    out = []
    subs = P.SUBSTATIONS
    kinds = (["res"] * 11) + (["com"] * 6) + (["rural"] * 7)
    rng.shuffle(kinds)
    for f, k in enumerate(kinds):
        d = dict(idx=f, kind=k, sub=subs[f % len(subs)])
        # household appliance holdings (shares of customers), the survey samples them
        d["sat_res_heat"] = rng.uniform(0.02, 0.55) if k != "com" else rng.uniform(0.0, 0.10)
        d["sat_hp"] = rng.uniform(0.02, 0.30) if k != "rural" else rng.uniform(0.15, 0.55)
        d["sat_ewh"] = rng.uniform(0.15, 0.85) if k != "com" else rng.uniform(0.02, 0.15)
        d["sat_ac"] = rng.uniform(0.55, 0.95) if k != "rural" else rng.uniform(0.35, 0.70)
        d["customers"] = int(rng.uniform(1400, 5200) if k == "res" else rng.uniform(280, 700) if k == "com" else rng.uniform(900, 2400))
        d["L"] = rng.uniform(3, 9) if k != "rural" else rng.uniform(10, 25)
        d["r"] = rng.uniform(0.15, 0.40) if k != "rural" else rng.uniform(0.30, 0.62)
        d["midreg"] = bool(d["L"] > 9 and rng.random() < 0.65)
        out.append(d)
    return out


KW = dict(base_res=0.95, base_com=11.0, base_rural=1.25, res_heat=4.2, hp=1.5, ewh=0.45, ac=1.6)


def components(f, T, rng):
    """MW by quarter-hour at the reference voltage, per load component, from the customers' holdings"""
    q = np.arange(P.NQ)
    hr = (q % P.Q) / 4.0
    day = q // P.Q
    dow = (day + 3) % 7                                    # 1 January 2026 is a Thursday
    wk = dow >= 5
    Tq = np.interp(np.arange(P.NQ) / 4.0, np.arange(len(T)) + 0.5, T)       # the hourly readings, smooth between
    hdd = np.clip(58 - Tq, 0, None)
    cdd = np.clip(Tq - 68, 0, None)
    n = f["customers"]
    if f["kind"] == "com":
        shape = 0.45 + 0.75 * ((hr >= 7.5) & (hr <= 18.5)) * (~wk) + 0.15 * ((hr >= 9) & (hr <= 17)) * wk
        kwb = KW["base_com"]
    else:
        shape = (0.70 + 0.42 * np.exp(-((hr - 19.2) / 2.8) ** 2) + 0.22 * np.exp(-((hr - 7.6) / 1.7) ** 2) * (~wk)
                 + 0.12 * np.exp(-((hr - 11) / 3) ** 2) * wk)
        kwb = KW["base_res"] if f["kind"] == "res" else KW["base_rural"]
    ar = np.zeros(P.NQ)
    e = rng.normal(0, 0.0016 / math.sqrt(max(n, 1) / 2000.0), P.NQ)       # a feeder of a few thousand customers is smooth
    for i in range(1, P.NQ):
        ar[i] = 0.9 * ar[i - 1] + e[i]
    base = n * kwb / 1000.0 * shape * (1 + ar)
    zip_ = (0.36, 0.44, 0.20)
    C = dict(Z=zip_[0] * base, P=zip_[1] * base, I=zip_[2] * base)
    ewh = n * f["sat_ewh"] * KW["ewh"] / 1000.0 * (0.55 + 0.7 * np.exp(-((hr - 7.0) / 1.6) ** 2) + 0.45 * np.exp(-((hr - 20.0) / 2.0) ** 2)) / 0.86
    rheat = n * f["sat_res_heat"] * KW["res_heat"] / 1000.0 * hdd / 40.0
    C["TH"] = ewh + rheat
    C["HP"] = n * f["sat_hp"] * KW["hp"] / 1000.0 * hdd / 40.0
    C["AC"] = n * f["sat_ac"] * KW["ac"] / 1000.0 * cdd / 18.0 * (0.6 + 0.4 * np.clip(np.sin(np.pi * (hr - 9) / 13), 0, None))
    return {c: v * (1 + rng.normal(0, 0.0012, P.NQ)) for c, v in C.items()}


def bus_voltage(rng):
    """each substation bus at the minute: the transmission voltage drifts and the LTC steps 5/8 percent once it has
    been outside its 2 V band for two minutes; returns volts by minute and the tap log"""
    M = P.ND * 24 * 60
    out, log = {}, []
    for s in P.SUBSTATIONS:
        tm = np.zeros(M)
        e = rng.normal(0, 0.045, M)
        daily = 0.6 * np.sin(2 * np.pi * (np.arange(M) / 1440.0 - 0.3))
        for i in range(1, M):
            tm[i] = 0.9995 * tm[i - 1] + e[i]
        raw = 123.0 + tm + daily
        tap, out_m, v = 0, 0, np.zeros(M)
        for i in range(M):
            vb = raw[i] + tap * P.TAP
            if abs(vb - 123.0) > 0.8:
                out_m += 1
                if out_m >= 2:
                    step = -1 if vb > 123.0 else 1
                    tap += step
                    log.append((s, i, step, tap))
                    vb += step * P.TAP
                    out_m = 0
            else:
                out_m = 0
            v[i] = vb
        out[s] = v
    return out, log


def highpass(dv, tau_h):
    a = 1 - math.exp(-0.25 / tau_h)
    lp = np.zeros_like(dv)
    for i in range(1, len(dv)):
        lp[i] = lp[i - 1] + a * (dv[i] - lp[i - 1])
    return dv - lp


def respond(C, V):
    """each component's power at the voltage path V (volts by quarter at the loads), from its reference at 122 V"""
    dv = (V - 122.0) / P.VNOM
    hp_dv = highpass(dv, P.TAU_TH)
    out = {}
    for c, v in C.items():
        k = P.KE[c]
        if c == "TH":
            out[c] = v * (1 + P.KI[c] * hp_dv)
        else:
            out[c] = v * (1 + k * dv)
    return out


def drop_end(f, S, seg_frac=1.0):
    seg = f["L"] * (0.45 if f["midreg"] else 1.0) * seg_frac
    return 3.0 * S / 8.0 * seg / 8.0 * f["r"] / 0.25


def losses(f, S, V):
    Rf = f["r"] * f["L"] * 0.55
    I = S / (math.sqrt(3) * P.KV * (V / P.VNOM))
    return 3 * I ** 2 * Rf


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    w = World()
    w.T = weather(rng)
    w.F = feeders(rng)
    w.C0 = [components(f, w.T, rng) for f in w.F]
    for f, C in zip(w.F, w.C0):
        f["peak"] = float(np.percentile(sum(C.values()), 99.9))
        f["cost"] = (60 + 30 * f["peak"] + 11 * f["L"] + (45 if f["midreg"] else 0)) * rng.uniform(0.9, 1.1) * 1000 * P.COST_SCALE
    w.vbus_min, w.taplog = bus_voltage(rng)
    w.vbus = {s: v.reshape(-1, 15).mean(axis=1) for s, v in w.vbus_min.items()}       # quarter-hour mean
    # the trial: eight feeders, pilot regulators, random on and off days in the trial months
    w.trial = sorted(int(x) for x in rng.choice(P.NF, size=8, replace=False))
    days = np.arange(P.ND)
    import datetime as dt
    dates = [P.T0.date() + dt.timedelta(days=int(d)) for d in days]
    tm = np.array([(dt.date(2026, 3, 16) <= d <= dt.date(2026, 6, 12)) or (dt.date(2026, 9, 14) <= d <= dt.date(2026, 11, 13))
                   for d in dates])
    w.trial_days = days[tm]
    w.assign, w.dose = {}, {}
    for f in w.trial:
        a = np.zeros(P.ND, dtype=int)
        a[w.trial_days] = rng.random(len(w.trial_days)) < 0.5
        comply = rng.uniform(0.62, 0.95)
        settle = rng.uniform(15, 60)
        ok = a.astype(bool) & (rng.random(P.ND) < comply)
        dose = np.zeros(P.NQ)
        for d in np.where(ok)[0]:
            s0 = d * P.Q
            st = settle * rng.uniform(0.6, 1.4) / 15.0
            ramp = np.clip((np.arange(P.Q) - 0) / max(st, 0.5), 0, 1)
            dose[s0:s0 + P.Q] = P.TRIAL_DV * ramp
        w.assign[f], w.dose[f] = a, dose
        w.F[f]["comply"], w.F[f]["settle"] = comply, settle
    # actual 2026 operation and the 2027 replay
    w.S, w.Vhead, w.loss, w.comp = [], [], [], []
    w.truth = []
    for f in w.F:
        C0 = w.C0[f["idx"]]
        Vh = w.vbus[f["sub"]] - (w.dose[f["idx"]] if f["idx"] in w.dose else 0.0)
        Cr = respond(C0, Vh - 0.5 * drop_end(f, sum(C0.values())))
        S = sum(Cr.values())
        w.Vhead.append(Vh)
        w.S.append(S)
        w.loss.append(losses(f, S, Vh))
        w.comp.append(Cr)
        # 2027 like 2026, against normal running (no trial): the program takes off, hour by hour, what keeps the
        # far end at 115 V, at most DVMAX
        Vn = w.vbus[f["sub"]]
        Cn = respond(C0, Vn - 0.5 * drop_end(f, sum(C0.values())))
        Sn = sum(Cn.values())
        ln = losses(f, Sn, Vn)
        veol = Vn - drop_end(f, Sn)
        room_q = np.clip(veol - (P.VMIN + P.MARGIN), 0, P.DVMAX)
        room = np.repeat(room_q.reshape(-1, 4).min(axis=1), 4)                         # set hour by hour
        Vvo = Vn - room
        Cv = respond(C0, Vvo - 0.5 * drop_end(f, sum(C0.values())))
        Sv = sum(Cv.values())
        lv = losses(f, Sv, Vvo)
        cust = float((Sn - Sv).sum() * 0.25)
        dl = float((ln - lv).sum() * 0.25)
        w.truth.append(dict(cust_mwh=cust, loss_mwh=dl, total_mwh=cust + dl, room=room,
                            value=(cust + dl) * P.PRICE * P.ANNUITY, cost=f["cost"]))
    return w


if __name__ == "__main__":
    import time
    t = time.time()
    w = build()
    print("built in %.0fs, %d taps" % (time.time() - t, len(w.taplog)))
    for f in w.F:
        tr = w.truth[f["idx"]]
        print(f["idx"], f["kind"], "trial" if f["idx"] in w.trial else "", "MWh %.0f (loss %+.0f) value/cost %.2f" % (
            tr["total_mwh"], tr["loss_mwh"], tr["value"] / tr["cost"]))
