"""The SCADA historian's one-minute feeder-breaker kW for the 88 summer weekdays, 15:00 to 20:00 Central daylight time,
exported in UTC; its point list; and the switching log. The load is weather-driven with its own afternoon shape and slow
wander; every paging group's shed command takes that group's delivered kW off each feeder from the transmit minute (the
RTU samples each breaker at the half minute, after the page) and the restore from 19:00 puts it back with the air
conditioners' snap-back; the study homes' contractor sheds its homes at 15:45. The minute noise is white. Over each
event day's command span (15:50 to ten minutes after the last command) it is core.py's own minute noise, so every step
read over any window, a minutes before and b after, is core's step_win[(a, b)] to rounding; the historian's held
readings fall outside those spans."""
import datetime as dt

import numpy as np

import common as CM
import params as P

NM = 300                                  # minutes 15:00 to 19:59 local
SPAN0 = 50                                # 15:50, the first minute core's minute noise covers


def shape(m):
    """The feeder's afternoon shape on a hot weekday: rising to 15:50, flat to about 18:10, falling into the evening."""
    m = np.asarray(m, float)
    return 1.0 - 0.045 * np.clip((SPAN0 - m) / SPAN0, 0, None) ** 1.5 - 0.075 * np.clip((m - 190) / 110.0, 0, None) ** 1.3


def day_index(r):
    """The supplier's cooling index for every day 1 May to 30 September: core's index on the event days, lower on the
    weekdays the trial did not call and on weekends, with a summer swell."""
    days = [dt.date(2026, 5, 1) + dt.timedelta(k) for k in range(153)]
    ev = {d: i for i, d in enumerate(P.EVENT_DAYS)}
    out = {}
    for d in days:
        doy = (d - dt.date(2026, 5, 1)).days
        swell = 0.52 + 0.30 * np.sin(np.pi * (doy - 10) / 150.0)
        if d in ev:
            continue
        v = swell + r.normal(0, 0.11)
        if d.weekday() < 5 and d >= P.SUMMER0:
            v = min(v, 0.80 + 0.06 * r.random())
        out[d] = float(np.clip(v, 0.08, 1.02))
    return days, out


def build(world, r):
    """Every minute of every feeder on every summer weekday; returns the rounded minutes, the held-reading masks, each
    event's command order (core's slots) and what the other files need."""
    W = world
    n_f = W["n_feed"]
    codes, subs = CM.feeder_codes(W["dist"])
    load = W["load"]
    sig = 0.004 * load / np.sqrt(0.4)            # white minute noise: a five-minute difference has core's step noise
    days, idx_other = day_index(r)
    ev_of = {d: i for i, d in enumerate(P.EVENT_DAYS)}
    idx = {d: (float(W["w"][ev_of[d]]) if d in ev_of else idx_other[d]) for d in days}
    key = {(int(e), int(g)): i for i, (e, g) in enumerate(W["obs_eg"])}
    # each event's command order is core's: slot k goes out at 16:00 plus 10 k minutes
    order = {}
    for e in range(W["n_events"]):
        gl = [int(g) for g in np.flatnonzero(W["disp"][e])]
        sl = {g: int(W["slot"][key[(e, g)] * n_f]) for g in gl}
        order[e] = sorted(gl, key=lambda g: sl[g])
        assert [sl[g] for g in order[e]] == list(range(len(gl)))
    tx_sec = {(e, g): int(r.integers(1, 5)) for e in order for g in order[e]}
    rs_sec = {(e, g): int(r.integers(2, 9)) for e in order for g in order[e]}
    transfers = switching_plan(W, codes, r)
    series, frozen_all, spans = {}, {}, {}
    for d in P.WEEKDAYS:
        e = ev_of.get(d)
        F = 0.55 + 0.45 * idx[d]
        span = (SPAN0, P.FLEET_MIN0 + 10 * len(order[e])) if e is not None else None
        if span:
            spans[d] = span
        m = np.arange(NM)
        if span:
            # no wander inside the span: core's minute noise is the whole of the variation there
            dist_out = np.where(m < span[0], span[0] - m, np.where(m >= span[1], m - span[1] + 1, 0))
            taper = np.clip(dist_out / 15.0, 0, 1)
        else:
            taper = np.ones(NM)
        for f in range(n_f):
            kn = r.normal(0, 0.0028, NM // 30 + 2)
            wander = np.interp(m, np.arange(len(kn)) * 30.0, kn) * taper
            base = load[f] * F * shape(m) * (1 + wander)
            for (fa, fb, d0, d1, share) in transfers:
                if d0 <= d <= d1:
                    if f == fa:
                        base = base * (1 - share)
                    elif f == fb:
                        base = base + load[fa] * F * shape(m) * share
            det = base.copy()
            frozen = np.zeros(NM, bool)
            # the historian's dropouts: the last good value held for three to eleven minutes, never inside a span
            for _ in range(int(r.poisson(0.2))):
                s0 = int(r.integers(3, NM - 12))
                ln_ = int(r.integers(3, 12))
                if span and not (s0 + ln_ <= span[0] - 1 or s0 > span[1]):
                    continue
                frozen[s0:s0 + ln_] = True
            noise = r.normal(0, sig[f], NM)
            if e is not None:
                if W["dist"][f] == 0:
                    sh = st_drop(W, e, f)
                    det[P.STUDY_SHED[0]:P.STUDY_SHED[1]] -= sh
                    det[P.STUDY_SHED[1]:] += snap(sh, np.arange(NM - P.STUDY_SHED[1]))
                for k, g in enumerate(order[e]):
                    Mk = P.FLEET_MIN0 + 10 * k
                    D = float(W["delivered"][key[(e, g)]][f])
                    det[Mk:] -= D
                    Rk = P.RESTORE_MIN + k
                    det[Rk:] += D
                    det[Rk:] += snap(D, np.arange(NM - Rk))
                Z = W["minute_noise"][e][f]
                assert len(Z) == span[1] - span[0]
                noise[span[0]:span[1]] = -Z                   # core's minute noise, read as load
            series[(d, f)] = det + noise
            frozen_all[(d, f)] = frozen
    # the feeder load the steps are weighed by: each feeder's mean over 15:00 to 15:44 on the event days equals
    # core's load (one constant per feeder, which moves no step)
    for f in range(n_f):
        vals = np.concatenate([series[(d, f)][:45][~frozen_all[(d, f)][:45]] for d in P.EVENT_DAYS])
        off = load[f] - vals.mean()
        for d in P.WEEKDAYS:
            series[(d, f)] = series[(d, f)] + off
    # round to the historian's 0.1 kW, hold the dropouts, and keep good readings from ever reading as held
    out = {}
    for (d, f), v in series.items():
        q = np.round(v, 1)
        fr = frozen_all[(d, f)]
        for i in range(2, NM):
            if not (fr[i] or fr[i - 1] or fr[i - 2]) and q[i] == q[i - 1] == q[i - 2]:
                q[i] = round(q[i] + 0.1, 1)
        for i in range(1, NM):
            if fr[i]:
                q[i] = q[i - 1]
        for i in range(2, NM):
            if fr[i] and not fr[i - 1] and q[i - 1] == q[i - 2]:
                q[i - 2] = round(q[i - 2] - 0.1, 1)
        for i in range(1, NM):
            if fr[i]:
                q[i] = q[i - 1]
        for i in range(1, NM):
            if not fr[i] and fr[i - 1] and q[i] == q[i - 1]:
                q[i] = round(q[i] + 0.1, 1)
        out[(d, f)] = q
    return dict(series=out, frozen=frozen_all, order=order, tx_sec=tx_sec, rs_sec=rs_sec, codes=codes, subs=subs,
                index_days=days, index=idx, transfers=transfers, spans=spans)


def st_drop(W, e, f):
    """What the treated study homes on feeder f take off on event e (kW): their switches' own reduction, at the day's
    index; the household noise of a meter-level estimate is not a feeder load."""
    st = W["study"]
    on = W["study_feeder"] == f
    tr = st["tr"][e]
    return float(np.sum((st["kap"] * st["hw"] * st["rc"][e] * W["w"][e])[on & tr]))


def snap(D, t):
    """The air conditioners' snap-back after a restore: a third of what was shed, fading over about half an hour."""
    return (0.34 * max(D, 0.0)) * np.exp(-np.asarray(t, float) / 27.0)


def switching_plan(W, codes, r):
    """Three line-section transfers between neighbouring feeders, each on weekdays the trial did not call (the operators
    switch on mild days); a fifth to a tenth of the source feeder's load moves."""
    ne = sorted(P.NON_EVENT)
    spans = []
    i = 0
    while i < len(ne) - 1:
        a, b = ne[i], ne[i + 1]
        if (b - a).days == 3 and a.weekday() == 4:            # a Friday and the Monday after, both uncalled
            spans.append((a, b))
            i += 2
        else:
            i += 1
    singles = [d for d in ne if d.weekday() in (1, 2) and d not in P.HOLIDAYS]
    picks = (spans[:2] + [(singles[len(singles) // 2], singles[len(singles) // 2])])[:3]
    pairs = [("CTW-2", "CTW-3"), ("ANT-3", "SDH-1"), ("OST-2", "OST-4")]
    out = []
    for (d0, d1), (ca, cb) in zip(picks, pairs):
        out.append((codes.index(ca), codes.index(cb), d0, d1, float(0.06 + 0.05 * r.random())))
    return out


def rows(S, world):
    """The export: UTC time, point, kW; pulled month by month, each pull running a day into the next month, so the
    first afternoon of July, August and September appears twice (identical readings)."""
    codes = S["codes"]
    out = []
    months = [6, 7, 8, 9]
    for mo in months:
        days = [d for d in P.WEEKDAYS if d.month == mo]
        nxt = [d for d in P.WEEKDAYS if d.month == mo + 1][:1]
        for f, code in enumerate(codes):
            for d in days + nxt:
                tag_old = CM.point_tag(code)
                for m in range(NM):
                    t_loc = CM.local(d, m)
                    tag = tag_old
                    if code in P.RENAMED and t_loc >= P.RENAME_AT:
                        tag = P.RENAMED[code]
                    t_utc = t_loc.astimezone(P.UTC)
                    out.append((t_utc.strftime("%Y-%m-%d %H:%M:%S"), tag, "%.1f" % S["series"][(d, f)][m]))
    return out


def point_rows(S, world):
    out = []
    for f, code in enumerate(S["codes"]):
        sub, name = S["subs"][f]
        b = int(code.split("-")[1])
        desc = "%s feeder %d breaker, three-phase kW" % (name, b)
        if code in P.RENAMED:
            out.append((CM.point_tag(code), desc, name, code, P.DISTRICTS[int(world["dist"][f])], "2009-04-21",
                        P.RENAME_AT.strftime("%Y-%m-%d %H:%M")))
            out.append((P.RENAMED[code], desc + " (rebuilt substation, transformer 2)", name, code,
                        P.DISTRICTS[int(world["dist"][f])], P.RENAME_AT.strftime("%Y-%m-%d %H:%M"), ""))
        else:
            out.append((CM.point_tag(code), desc, name, code, P.DISTRICTS[int(world["dist"][f])],
                        ["2007-10-02", "2009-04-21", "2011-06-14", "2014-03-11"][f % 4], ""))
    out.sort(key=lambda t: t[0])
    return out


def switching_rows(S, world, r):
    codes = S["codes"]
    out = []
    no = 26104
    for (fa, fb, d0, d1, share) in S["transfers"]:
        sec = "%s section %d" % (codes[fa], int(r.integers(3, 19)))
        t0 = dt.datetime(d0.year, d0.month, d0.day, 6, int(r.integers(5, 55)), tzinfo=P.CDT)
        t1 = dt.datetime(d1.year, d1.month, d1.day, 20, int(r.integers(5, 55)), tzinfo=P.CDT) + dt.timedelta(minutes=15)
        why = ["recloser replacement", "pole change-out on the tie", "regulator bank maintenance"][len(out) % 3]
        out.append(("SO-%d" % no, sec, codes[fa], codes[fb], t0.strftime("%m/%d/%Y %H:%M"), t1.strftime("%m/%d/%Y %H:%M"),
                    why, P.PEOPLE["ops"]))
        no += int(r.integers(3, 40))
    # overnight and weekend switching that never touches an afternoon the export covers
    wk = [d for d in (dt.date(2026, 6, 1) + dt.timedelta(k) for k in range(122)) if d.weekday() == 5]
    for j in range(5):
        d = wk[int(r.integers(len(wk)))]
        fa = int(r.integers(len(codes)))
        fb = (fa + 1) if (fa + 1) < len(codes) and codes[fa + 1][:3] == codes[fa][:3] else fa - 1
        t0 = dt.datetime(d.year, d.month, d.day, 7, int(r.integers(0, 59)), tzinfo=P.CDT)
        t1 = t0 + dt.timedelta(hours=int(r.integers(3, 7)))
        out.append(("SO-%d" % no, "%s section %d" % (codes[fa], int(r.integers(2, 15))), codes[fa], codes[fb],
                    t0.strftime("%m/%d/%Y %H:%M"), t1.strftime("%m/%d/%Y %H:%M"), "planned outage avoidance", P.PEOPLE["ops"]))
        no += int(r.integers(3, 40))
    out.sort(key=lambda t: dt.datetime.strptime(t[4], "%m/%d/%Y %H:%M"))
    return out
