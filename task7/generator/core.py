#!/usr/bin/env python3
"""task7 architecture 13, the stump core (stumping Part 1d, references/core-method.md).

The world: a rural electric cooperative's one-way (paging) air-conditioner load-control fleet. In summer 2026 it ran
a randomised dispatch trial: on each of 60 hot weekdays a random set of the 16 paging groups (install batches) was
shed 16:00 to 19:00. No member meter records intervals (monthly drive-by reads), so what a shed delivers is seen only
as a pool: the 46 feeder breakers' SCADA load against its counterfactual. A switch delivers only if (1) the page
reaches it, which depends on the distance to an on-air transmitter of its own paging system on that day (two systems,
transmitters off the air or commissioned during the trial), (2) its hardware still works, which falls with its
install batch's age, and (3) it is still wired to the air conditioner, which most are not where the unit was replaced
after the switch went in. 380 interval-metered study homes (in town, near a transmitter, 2019-20 switches, no
replaced unit) show what a working switch takes off.

Three judgments, each read at face value from the cooperative's own record by the hurried route and each fitted
from the feeder pool by the golden: S1 reception by reach (the coverage map), S2 failed hardware by install era (the
annual test log), S3 disconnection at replaced air conditioners (the service work orders). Nothing here reads a
prompt or solves a task: it is arithmetic on this world's arrays, ending on corelib.run(spec).
"""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = 713
N_EVENTS = 60
RB = (8.0, 14.0, 20.0)            # reach bands, km to the nearest on-air transmitter of the switch's own system
W_CP = 1.15                       # the weather index of the four 2026 coincident-peak afternoons (filed with the invoices)
OUT_KM = 14.0                     # the reconnection proposals split the flagged premises at 14 km from their transmitter
OLD_YEAR = 2015                   # switches installed to 2015 are on the cooperative's VHF system, later ones on the carrier's
NEW_VHF = np.array([-31.0, 12.0])  # the proposed Ridge VHF repeater
NEW_CAR = np.array([3.0, 25.0])    # the proposed carrier fill-in site in the North district
# the 2027 capital plan's filed appraisal constants (the build files them in the plan workbook)
VALUE = 88.0                      # USD per kW-year of coincident-peak reduction (four summer months of wholesale demand charges)
COST = {"rep_w": 16300.0, "rep_n": 24600.0}          # annualised cost of each transmitter proposal, USD per year
VISIT = {"fix_t": 15.6, "fix_w": 28.4, "recon_in": 13.7, "recon_out": 24.5}  # annualised cost per premise visited, USD per year
FACE = {"reach": 1.0, "test_pass": 0.96, "wo_connected": 0.91}   # the three records read at face value


def build(seed=SEED, n_events=N_EVENTS, noise=0.004):
    r = np.random.default_rng(seed)
    n_f = [13, 12, 11, 10]            # feeders in Town, West, North, East
    cent, dist = [], []
    for k in range(4):
        for j in range(n_f[k]):
            if k == 0:
                c = r.normal(0, 3.0, 2)
            elif k == 1:
                t = (j + 0.5) / n_f[k]
                c = np.array([-10 - 26 * t, -1 + 16 * t]) + r.normal(0, 2.0, 2)
            elif k == 2:
                c = np.array([4, 23]) + r.normal(0, 5.0, 2)
            else:
                c = np.array([25, -2]) + r.normal(0, 5.5, 2)
            cent.append(c)
            dist.append(k)
    cent, dist = np.array(cent), np.array(dist)
    n_feed = len(cent)
    hv = r.uniform(0.55, 1.6, n_feed)                               # how fast a feeder's housing replaces its units
    fm = np.array([2009, 2011, 2016, 2018])[dist] + r.uniform(-3.5, 3.5, n_feed)   # the enrolment drive's peak year
    lam = (300, 270, 240, 220)
    sf, xy, yr = [], [], []
    for f in range(n_feed):
        n = r.poisson(lam[dist[f]])
        p = cent[f] + r.normal(0, 1.4 if dist[f] == 0 else 2.3, (n, 2))
        y_ = np.rint(r.triangular(2004, np.clip(fm[f], 2004.5, 2025.4), 2025.99, n) - 0.49).astype(int).clip(2004, 2025)
        sf += [f] * n
        xy.append(p)
        yr.append(y_)
    sf, xy, yr = np.array(sf), np.vstack(xy), np.concatenate(yr)
    n_s = len(sf)
    x, y = xy[:, 0], xy[:, 1]
    vhf = yr <= OLD_YEAR
    age = 2026 - yr
    vt = np.array([[0, 1], [-14, 1], [5, 20]])                       # VHF: headquarters, West substation, North substation
    ct = np.array([[1, -2], [-31, 9], [17, 11], [27, 2], [-12, 33]])    # the carrier's 900 MHz sites
    von = np.ones((n_events, 3), bool)
    con = np.ones((n_events, 5), bool)
    von[12:20, 2] = False      # North VHF transmitter off the air, eight event days (lightning)
    von[40:46, 1] = False      # West VHF transmitter off the air, six event days (antenna work)
    con[:30, 3] = False        # the carrier's East site commissioned before event 31
    con[33:38, 2] = False      # the carrier's north-east site off the air, five event days
    dm = lambda t: np.sqrt((x[:, None] - t[None, :, 0]) ** 2 + (y[:, None] - t[None, :, 1]) ** 2)
    dv, dc = dm(vt), dm(ct)
    reach = np.empty((n_events, n_s))
    for e in range(n_events):
        reach[e] = np.where(vhf, np.where(von[e][None, :], dv, 1e9).min(1), np.where(con[e][None, :], dc, 1e9).min(1))
    now = np.where(vhf, dv.min(1), dc.min(1))                        # every transmitter on the air (the 2027 footing)
    static_any = np.minimum(dv.min(1), dc.min(1))                    # nearest transmitter of either system, today's list
    qf = lambda d: 0.80 / (1 + np.exp((d - 18.5) / 3.6))             # a page arrives
    hf = lambda a: 0.985 * np.exp(-(a / 30.0) ** 1.7)                # the hardware still works
    hw = r.random(n_s) < hf(age)
    repl = r.random(n_s) < (1 - np.exp(-age * hv[sf] / 22.0))        # the air conditioner replaced since the switch went in
    disc = repl & (r.random(n_s) < 0.72)                             # and the switch left unwired
    flag = repl & (r.random(n_s) < 0.93)                             # the replacement shows in the rebate or permit record
    kap = r.lognormal(-0.5 * 0.35 ** 2, 0.35, n_s)                   # kW a working, reached switch takes off at index 1
    w = r.uniform(0.65, 1.25, n_events)
    order = np.argsort(yr + r.random(n_s) * 0.999)
    grp = np.empty(n_s, int)
    grp[order] = (np.arange(n_s) * 16) // n_s                        # paging groups are install batches
    disp = np.zeros((n_events, 16), bool)
    for e in range(n_events):
        disp[e, r.choice(16, r.integers(4, 13), replace=False)] = True
    load = r.uniform(1500, 3500, n_feed)
    # the record: one step in each feeder's SCADA load at each group's shed command (five minutes before against
    # five minutes after), one group every ten minutes from 16:00 in a random order
    obs_e, obs_g, obs_f, step = [], [], [], []
    for e in range(n_events):
        recv = r.random(n_s) < qf(reach[e])
        dl = kap * w[e] * recv * hw * (~disc)
        for gi in np.flatnonzero(disp[e]):
            m = grp == gi
            st = np.bincount(sf[m], dl[m], n_feed) + r.normal(0, noise * load)
            obs_e += [e] * n_feed
            obs_g += [gi] * n_feed
            obs_f += list(range(n_feed))
            step += list(st)
    obs_e, obs_g, obs_f, step = map(np.array, (obs_e, obs_g, obs_f, step))
    d_new_v = np.minimum(dv.min(1), np.sqrt((x - NEW_VHF[0]) ** 2 + (y - NEW_VHF[1]) ** 2))
    d_new_c = np.minimum(dc.min(1), np.sqrt((x - NEW_CAR[0]) ** 2 + (y - NEW_CAR[1]) ** 2))
    # the study homes: unit-level interval meters, Town, 1 to 6 km from a transmitter, 2019-20 switches, no unit replaced
    n_st = 380
    s_age = r.choice([6, 7], n_st)
    s_hw = r.random(n_st) < hf(s_age)
    s_q = qf(r.uniform(1, 8, n_st))
    s_kap = r.lognormal(-0.5 * 0.35 ** 2, 0.35, n_st)
    s_tr = r.random((n_events, n_st)) < 0.5
    s_rc = r.random((n_events, n_st)) < s_q[None, :]
    s_resp = (s_kap[None, :] * s_hw[None, :] * s_rc + r.normal(0, 1.0, (n_events, n_st))) * s_tr
    batch_age = np.array([age[grp == gi].mean() for gi in range(16)])
    return dict(batch_age=batch_age, dist=dist, n_feed=n_feed, n_s=n_s, sf=sf, x=x, y=y, yr=yr, vhf=vhf, age=age, n_events=n_events, reach=reach,
                now=now, static_any=static_any, dv=dv, dc=dc, von=von, con=con, hw=hw, repl=repl, disc=disc, flag=flag, kap=kap,
                w=w, grp=grp, disp=disp, load=load, obs=(obs_e, obs_g, obs_f), step=step, qf=qf, hf=hf, d_new_v=d_new_v, d_new_c=d_new_c,
                study=(s_resp, s_tr), vt=vt, ct=ct)


# ---- what the files hold, and the estimators that read them -------------------------------------------------------

def tensor(wd, reach, rb=RB):
    """For every step observation (event, group shed, feeder): that group's switches on the feeder by reach band and
    replaced-unit flag, weighted by the event's weather index."""
    obs_e, obs_g, obs_f = wd["obs"]
    n_f = wd["n_feed"]
    fl = wd["flag"].astype(int)
    key = np.full((wd["n_events"], 16), -1)
    key[obs_e[::n_f], obs_g[::n_f]] = np.arange(len(obs_e) // n_f)
    n = np.zeros((len(obs_e) // n_f, n_f, len(rb) + 1, 2))
    for e in range(wd["n_events"]):
        rbnd = np.digitize(reach[e] if reach.ndim == 2 else reach, rb)
        on = wd["disp"][e, wd["grp"]]
        np.add.at(n, (key[e, wd["grp"][on]], wd["sf"][on], rbnd[on], fl[on]), wd["wx"][e])
    return n.reshape(-1, len(rb) + 1, 2)


def fit(wd, n, wls=True, iters=60, cfix=None, qfix=None, keep=None, district=True, batch="free"):
    """step = sum over cells of n * q[reach band] * c[flag], times a[district] * h[install batch]. q is relative to
    the nearest band, a to the Town district and c to the premises with no replaced unit, so h is the kW an enrolled
    switch of that batch delivers near a transmitter at index 1."""
    obs_e, obs_g, obs_f = wd["obs"]
    load = wd["load"][obs_f]
    wt = (1.0 / load) if wls else np.ones(len(load)) / wd["load"].mean()
    y = wd["step"] * wt
    nw = n * wt[:, None, None]
    dd = wd["dist"][obs_f]
    if keep is not None:
        y, nw, dd, obs_g = y[keep], nw[keep], dd[keep], obs_g[keep]
    rr = n.shape[1]
    q = np.ones(rr) if qfix is None else np.array(qfix, float)
    a = np.ones(4)
    h = np.full(16, 0.5)
    c = np.array([1.0, 0.5 if cfix is None else cfix])
    gd = np.zeros((len(y), 16))
    gd[np.arange(len(y)), obs_g] = 1.0
    dm_ = np.zeros((len(y), 4))
    dm_[np.arange(len(y)), dd] = 1.0
    age_g = wd["batch_age"]
    for _ in range(iters):
        z = np.einsum("nrk,r,k->n", nw, q, c)
        if batch == "free":
            h = np.linalg.lstsq(gd * (z * a[dd])[:, None], y, rcond=None)[0]
        else:                                   # a straight line in the batch's mean age
            xx = (z * a[dd])[:, None] * np.column_stack([np.ones(len(y)), age_g[obs_g]])
            b0, b1 = np.linalg.lstsq(xx, y, rcond=None)[0]
            h = b0 + b1 * age_g
        if district:
            aa = np.linalg.lstsq(dm_ * (z * h[obs_g])[:, None], y, rcond=None)[0]
            h, a = h * aa[0], aa / aa[0]
        if cfix is None:
            cc = np.linalg.lstsq(np.einsum("nrk,r->nk", nw, q) * (a[dd] * h[obs_g])[:, None], y, rcond=None)[0]
            h, c = h * cc[0], cc / cc[0]
        if qfix is None:
            qq = np.linalg.lstsq(np.einsum("nrk,k->nr", nw, c) * (a[dd] * h[obs_g])[:, None], y, rcond=None)[0]
            h, q = h * qq[0], qq / qq[0]
    return q, a, h, c


def study(wd, cut=0.25):
    """The interval-metered study homes: the mean response of every enrolled study switch, and of the ones that
    respond at all (what a working switch near a transmitter takes off at index 1)."""
    s_resp, s_tr = wd["study"]
    m = s_resp.sum(0) / s_tr.sum(0)
    work = m > cut
    return dict(itt=float(m.mean()), working=float(m[work].mean()), share=float(work.mean()))


def figures(wd, q, th, c, k_work, rb=RB):
    """Every figure the answer states, from a delivery model: q (reach band), th (kW per enrolled switch near a
    transmitter, by switch), c (replaced unit)."""
    fl = wd["flag"].astype(int)
    b = lambda d: np.digitize(d, rb)
    dist = wd["dist"][wd["sf"]]
    old = wd["yr"] <= OLD_YEAR
    vhf = wd["vhf"]
    base = th * c[fl]
    qn = q[b(wd["now"])]
    o = {}
    o["rep_w"] = W_CP * np.sum((base * (q[b(wd["d_new_v"])] - qn))[vhf])
    o["rep_n"] = W_CP * np.sum((base * (q[b(wd["d_new_c"])] - qn))[~vhf])
    for nm, k in (("fix_t", 0), ("fix_w", 1)):
        m = (dist == k) & old & (fl == 0)
        o[nm] = W_CP * np.sum(((k_work - th) * qn)[m])
    rec = th * qn * (1 - c[1])
    o["recon_in"] = W_CP * np.sum(rec[(fl == 1) & (wd["now"] < OUT_KM)])
    o["recon_out"] = W_CP * np.sum(rec[(fl == 1) & (wd["now"] >= OUT_KM)])
    # the three decisive steps' own figures
    o["c1_fringe_loss"] = 1.0 - q[b(np.array([22.0]))[0]]
    m_old = old & (fl == 0)
    o["c2_failed_old"] = 1.0 - float(np.mean(th[m_old])) / k_work
    o["c3_unwired"] = 1.0 - c[1]
    # the bridge from what the fleet could take off to what it does (kW at the coincident-peak index)
    o["lost_reach"] = W_CP * np.sum(k_work * (1 - qn))
    o["lost_hw"] = W_CP * np.sum((k_work - th) * qn)
    o["lost_unwired"] = W_CP * np.sum((th * qn * (1 - c[1]))[fl == 1])
    o["delivered"] = W_CP * np.sum(base * qn)
    return o


def truth(wd):
    qf, conn, hw, fl = wd["qf"], ~wd["disc"], wd["hw"], wd["flag"]
    dist = wd["dist"][wd["sf"]]
    old = wd["yr"] <= OLD_YEAR
    vhf = wd["vhf"]
    qn = qf(wd["now"])
    q0 = float(np.mean(qf(wd["now"][wd["now"] < RB[0]])))
    st = hw * conn
    o = {}
    o["rep_w"] = W_CP * np.sum(((qf(wd["d_new_v"]) - qn) * st)[vhf])
    o["rep_n"] = W_CP * np.sum(((qf(wd["d_new_c"]) - qn) * st)[~vhf])
    for nm, k in (("fix_t", 0), ("fix_w", 1)):
        o[nm] = W_CP * np.sum((qn * (1.0 - st))[(dist == k) & old & (~fl)])
    o["recon_in"] = W_CP * np.sum((qn * hw * wd["disc"])[fl & (wd["now"] < OUT_KM)])
    o["recon_out"] = W_CP * np.sum((qn * hw * wd["disc"])[fl & (wd["now"] >= OUT_KM)])
    o["c1_fringe_loss"] = 1.0 - float(np.mean(qf(wd["now"][wd["now"] >= RB[2]]))) / q0
    o["c2_failed_old"] = 1.0 - float(np.mean(st[old & ~fl]))
    o["c3_unwired"] = 1.0 - float(np.mean(conn[fl])) / float(np.mean(conn[~fl]))
    return o


MEMBERS = ("rep_w", "rep_n", "fix_t", "fix_w", "recon_in", "recon_out")


def lines(wd):
    dist = wd["dist"][wd["sf"]]
    old = wd["yr"] <= OLD_YEAR
    fl = wd["flag"]
    n = {"fix_t": int(((dist == 0) & old & ~fl).sum()), "fix_w": int(((dist == 1) & old & ~fl).sum()),
         "recon_in": int((fl & (wd["now"] < OUT_KM)).sum()), "recon_out": int((fl & (wd["now"] >= OUT_KM)).sum())}
    out = {k: COST[k] / VALUE for k in COST}
    out.update({k: n[k] * VISIT[k] / VALUE for k in VISIT})
    return out, n


STUMPS = ("S1", "S2", "S3")


def model(wd, rb=RB, reach=None, wls=True, district=True, batch="free", keep=None, cut=0.25, cfix=None):
    """One fitted delivery model: (q by reach band, th per switch, c, the working level from the study homes)."""
    n = tensor(wd, wd["reach"] if reach is None else reach, rb)
    q, a, h, c = fit(wd, n, wls=wls, district=district, batch=batch, keep=keep, cfix=cfix)
    th = a[wd["dist"][wd["sf"]]] * h[wd["grp"]]
    return dict(q=q, th=th, c=c, k=study(wd, cut)["working"], rb=rb, a=a, h=h)


def hurried(m, lost):
    """The model with the named judgments read at face value from the cooperative's own record and the rest as fitted."""
    q, th, c = m["q"].copy(), m["th"].copy(), m["c"].copy()
    if "S1" in lost:
        q = np.full_like(q, FACE["reach"])                  # the coverage map: every enrolled premise is covered
    if "S2" in lost:
        th = np.full_like(th, FACE["test_pass"] * m["k"])   # the annual test log: 96 in 100 switches pass
    if "S3" in lost:
        c = np.array([1.0, FACE["wo_connected"]])           # the work orders: 9 in 100 found unwired after a new unit
    return dict(m, q=q, th=th, c=c)


def all_figures(wd, m, ln):
    f = figures(wd, m["q"], m["th"], m["c"], m["k"], m["rb"])
    go = [k for k in MEMBERS if f[k] >= ln[k]]
    f["plan_kw"] = float(sum(f[k] for k in go))
    f["plan_cost_per_kw"] = float(sum(ln[k] for k in go) * VALUE / f["plan_kw"]) if go else 0.0
    return f


def slices(wd):
    """Three slices of the step record that tell the three judgments apart (the falsification check)."""
    obs_e, obs_g, obs_f = wd["obs"]
    n_f = wd["n_feed"]
    b = np.digitize(wd["reach"], RB) != np.digitize(wd["now"], RB)[None, :]      # a transmitter change moved the switch's band
    moved = np.zeros(len(obs_e))
    tot = np.zeros(len(obs_e))
    key = obs_e * 16 * n_f + obs_g * n_f + obs_f
    for e in range(wd["n_events"]):
        on = wd["disp"][e, wd["grp"]]
        k_ = e * 16 * n_f + wd["grp"][on] * n_f + wd["sf"][on]
        idx = np.searchsorted(key, k_)
        np.add.at(moved, idx, b[e][on])
        np.add.at(tot, idx, 1.0)
    flag_share = np.bincount(wd["sf"], wd["flag"], n_f) / np.bincount(wd["sf"], minlength=n_f)
    return {"off the air": moved >= 0.5 * np.maximum(tot, 1), "oldest batches": obs_g <= 3,
            "most replaced units": flag_share[obs_f] >= np.quantile(flag_share, 0.75)}


def closure(wd, m, sl, reach=None):
    """The largest relative gap, over the three slices, between the model's predicted steps and the recorded ones."""
    n = tensor(wd, wd["reach"] if reach is None else reach, m["rb"])
    obs_e, obs_g, obs_f = wd["obs"]
    th_cell = np.zeros((4, 16))
    dd = wd["dist"][wd["sf"]]
    for d in range(4):
        for gi in range(16):
            sel = (dd == d) & (wd["grp"] == gi)
            th_cell[d, gi] = m["th"][sel].mean() if sel.any() else 0.0
    pred = np.einsum("nrk,r,k->n", n, m["q"], m["c"]) * th_cell[wd["dist"][obs_f], obs_g]
    return max(abs(pred[s_].sum() / wd["step"][s_].sum() - 1.0) for s_ in sl.values())


def main():
    wd = build()
    wd["wx"] = wd["w"]
    ln, cnt = lines(wd)
    tr = truth(wd)
    gm = model(wd)
    gold = all_figures(wd, gm, ln)
    st = study(wd)

    # ---- the variant battery: defensible rebuilds of the golden's conventions ----
    obs_e = wd["obs"][0]
    th_cell = np.array([[gm["a"][d] * gm["h"][gi] for gi in range(16)] for d in range(4)])
    pred = np.einsum("nrk,r,k->n", tensor(wd, wd["reach"]), gm["q"], gm["c"]) * th_cell[wd["dist"][wd["obs"][2]], wd["obs"][1]]
    res = wd["step"] - pred
    sd_f = np.array([res[wd["obs"][2] == f].std() for f in range(wd["n_feed"])])
    variants = {
        "bands 7/13/19 km": lambda: model(wd, rb=(7.0, 13.0, 19.0)),
        "bands 9/15/21 km": lambda: model(wd, rb=(9.0, 15.0, 21.0)),
        "bands 8/12/18 km": lambda: model(wd, rb=(8.0, 12.0, 18.0)),
        "bands 10/15/20 km": lambda: model(wd, rb=(10.0, 15.0, 20.0)),
        "unweighted least squares": lambda: model(wd, wls=False),
        "no district term": lambda: model(wd, district=False),
        "batch term a line in age": lambda: model(wd, batch="line"),
        "first six event days dropped": lambda: model(wd, keep=obs_e >= 6),
        "last six event days dropped": lambda: model(wd, keep=obs_e < wd["n_events"] - 6),
        "even event days only": lambda: model(wd, keep=obs_e % 2 == 0),
        "odd event days only": lambda: model(wd, keep=obs_e % 2 == 1),
        "study responders cut at 0.15 kW": lambda: model(wd, cut=0.15),
        "study responders cut at 0.35 kW": lambda: model(wd, cut=0.35),
        "steps beyond 2.5 sd of the feeder's residual trimmed": lambda: model(wd, keep=np.abs(res) < 2.5 * sd_f[wd["obs"][2]]),
    }
    fam = {name: all_figures(wd, fn(), ln) for name, fn in variants.items()}
    # the cooling index measured from 0.1 instead of 0 (cooling load starting later): refit on the shifted index and
    # restate at the shifted coincident-peak index
    wd_sh = dict(wd, wx=wd["w"] - 0.1)
    m_sh = model(wd_sh)
    f_sh = figures(wd, m_sh["q"], m_sh["th"] * (W_CP - 0.1) / W_CP, m_sh["c"], m_sh["k"], m_sh["rb"])
    for k_ in ("fix_t", "fix_w", "lost_reach", "lost_hw"):          # the working level is the study homes' and is not rescaled
        pass
    m_sh2 = dict(m_sh, th=m_sh["th"] * (W_CP - 0.1) / W_CP)
    fam["cooling index measured from 0.1"] = all_figures(wd, m_sh2, ln)
    names = list(fam)

    # ---- the lattice: every subset of the three judgments read at face value ----
    combos = [c_ for k in (1, 2, 3) for c_ in itertools.combinations(STUMPS, k)]
    lat = {"+".join(c_): all_figures(wd, hurried(gm, c_), ln) for c_ in combos}

    # ---- the routes ----
    reflex = lat["S1+S2+S3"]
    # the most rigorous standard design: the randomised comparison on the interval-metered study homes, carried to the fleet
    rig = {"rep_w": 0.0, "rep_n": 0.0, "recon_in": 0.0, "recon_out": 0.0, "c1_fringe_loss": 0.0, "c3_unwired": 1 - FACE["wo_connected"],
           "c2_failed_old": 1 - st["itt"] / st["working"], "lost_reach": 0.0, "lost_unwired": 0.0}
    for nm in ("fix_t", "fix_w"):
        rig[nm] = W_CP * cnt[nm] * (st["working"] - st["itt"])
    rig["lost_hw"] = W_CP * wd["n_s"] * (st["working"] - st["itt"])
    rig["delivered"] = W_CP * wd["n_s"] * st["itt"]
    go = [k for k in MEMBERS if rig[k] >= ln[k]]
    rig["plan_kw"] = float(sum(rig[k] for k in go))
    rig["plan_cost_per_kw"] = float(sum(ln[k] for k in go) * VALUE / rig["plan_kw"]) if go else 0.0
    # generous: every named field and the one-step distance to the nearest listed transmitter, fitted jointly on the steps
    wd_gen = dict(wd, now=wd["static_any"],
                  d_new_v=np.minimum(wd["static_any"], np.sqrt((wd["x"] - NEW_VHF[0]) ** 2 + (wd["y"] - NEW_VHF[1]) ** 2)),
                  d_new_c=np.minimum(wd["static_any"], np.sqrt((wd["x"] - NEW_CAR[0]) ** 2 + (wd["y"] - NEW_CAR[1]) ** 2)))
    gen_m = model(wd, reach=wd["static_any"])
    gen = all_figures(wd_gen, gen_m, ln)

    def cut_route(km, year):
        q = np.array([1.0 if (hi <= km) else 0.0 for hi in (RB[0], RB[1], RB[2], 1e9)])   # reached inside km, lost beyond
        rbc = (km - 1e-9, km, km + 1e-9)
        qc = np.array([1.0, 1.0, 0.0, 0.0])
        th = np.where(wd["yr"] <= year, 0.0, gm["k"])                                      # old batches dead, the rest working
        m = dict(q=qc, th=th, c=np.array([1.0, 0.0]), k=gm["k"], rb=rbc)
        return all_figures(wd_gen, m, ln)

    cut = {"%d km, %d" % (km, yr_): cut_route(km, yr_) for km in (10, 14, 20) for yr_ in (2009, 2011, 2015)}

    # ---- each judgment pushed past its fitted value, the rest as fitted ----
    over = {}
    m1 = dict(gm, q=gm["q"] ** 2.5)
    over["S1"] = all_figures(wd, m1, ln)
    m2 = dict(gm, th=gm["th"] * 0.6)
    over["S2"] = all_figures(wd, m2, ln)
    over["S3"] = all_figures(wd, model(wd, cfix=0.0), ln)

    # ---- the falsification check ----
    sl = slices(wd)
    fals = {"golden": closure(wd, gm, sl)}
    for c_ in combos:
        fals["+".join(c_)] = closure(wd, hurried(gm, c_), sl)
    fals["generous"] = closure(wd, gen_m, sl, reach=wd["static_any"])
    cal_m = dict(gm, q=np.ones(4), th=np.full(wd["n_s"], st["itt"]), c=np.array([1.0, 1.0]))
    fals["calibrated"] = closure(wd, cal_m, sl)

    # ---- the spec ----
    def member(k):
        return {"lines": [ln[k]], "truth": float(tr[k]), "golden": float(gold[k]), "family": [float(fam[v][k]) for v in names],
                "routes": {"direct": float(reflex[k]), "rigorous": float(rig[k])}}

    said = {
        "S1": ("what", "rep_w", "A shed command sent is not a shed command received: how often a one-way switch hears its page falls with "
               "its distance to a transmitter of its own paging system that was on the air that day.",
               ["N09", "N27", "L38", "L70"]),
        "S2": ("when", "fix_t", "A switch that passed its last test is not a switch that works now: the share still shedding falls "
               "with the age of the install batch, and only the feeder steps of each batch's own commands show by how much.",
               ["N11", "N46", "N35"]),
        "S3": ("who", "recon_in", "The premise on the register is not the equipment the switch was wired to: where the air conditioner "
               "was replaced after the switch went in, most switches were left unwired.",
               ["N14", "L56", "L58", "N36"]),
    }
    stumps = {s_: {"axis": ax, "opens": mem, "said_out_loud": txt, "steps_left": 4, "precedents": pre,
                   "sides": {"over": {k: float(over[s_][k]) for k in MEMBERS}}} for s_, (ax, mem, txt, pre) in said.items()}

    def fig(fid, key, block, sentence=None, memb=None):
        if memb:
            d = {"id": fid, "block": block, "member": memb}
        else:
            d = {"id": fid, "block": block, "golden": float(gold[key]), "family": [float(fam[v][key]) for v in names],
                 "lattice": {k: float(v[key]) for k, v in lat.items()},
                 "routes": {"rigorous": float(rig[key]), "generous": float(gen[key]), "calibrated": float(rig[key]),
                            "hedge": float(reflex[key]), "cutoff": float(cut["14 km, 2011"][key])}}
        if sentence:
            d["sentence"] = sentence
        return d

    figs_ = [fig("C1 fringe commands lost", "c1_fringe_loss", "component"),
             fig("C2 pre-2016 switches failed", "c2_failed_old", "component"),
             fig("C3 switches unwired at replaced units", "c3_unwired", "component")]
    figs_ += [fig("A1 %s" % k, k, "ask", memb=k) for k in MEMBERS]
    figs_ += [fig("A2 kW lost to missed commands", "lost_reach", "ask", sentence="A2 bridge"),
              fig("A2 kW lost to failed switches", "lost_hw", "ask", sentence="A2 bridge"),
              fig("A2 kW lost to unwired switches", "lost_unwired", "ask", sentence="A2 bridge"),
              fig("A3 kW the funded plan adds", "plan_kw", "ask"), fig("A3 funded plan cost per kW", "plan_cost_per_kw", "ask")]

    run_routes = {"generous": {k: float(gen[k]) for k in MEMBERS}, "calibrated": {k: float(rig[k]) for k in MEMBERS},
                  "hedge": {k: float(reflex[k]) for k in MEMBERS}, "cutoff": {k: float(cut["14 km, 2011"][k]) for k in MEMBERS}}
    for lab, v in cut.items():
        if lab != "14 km, 2011":
            run_routes["cutoff:%s" % lab] = {k: float(v[k]) for k in MEMBERS}

    spec = {"task": "task7 architecture 13", "call": "lines", "members": {k: member(k) for k in MEMBERS}, "stumps": stumps,
            "lattice": {k: {m_: float(v[m_]) for m_ in MEMBERS} for k, v in lat.items()},
            "falsification": {"check": "predicted against recorded feeder steps on three slices (transmitter off the air, oldest "
                              "batches, feeders with most replaced units): the largest relative gap", "observes_target": False,
                              "truth": 0.0, "golden": float(fals["golden"]),
                              "rivals": {k: float(v) for k, v in fals.items() if k != "golden"}},
            "run_routes": run_routes, "figures": figs_}

    print("world: %d switches on %d feeders, %d step observations over %d event days; study homes: %s" % (
        wd["n_s"], wd["n_feed"], len(wd["step"]), wd["n_events"], {k: round(v, 3) for k, v in st.items()}))
    print("premises: %s; lines (kW): %s" % (cnt, {k: round(v, 1) for k, v in ln.items()}))
    print("golden model: q by reach band %s, c %.3f, working level %.3f kW" % (gm["q"].round(3), gm["c"][1], gm["k"]))
    print("truth:  " + ", ".join("%s %.3g" % (k, tr[k]) for k in tr))
    print("golden: " + ", ".join("%s %.4g" % (k, v) for k, v in gold.items()))
    for lab, v in (("rigorous", rig), ("generous", gen), ("cutoff 14 km, 2011", cut["14 km, 2011"])):
        print("%s: " % lab + ", ".join("%s %.4g" % (k, v[k]) for k in gold))
    for k, v in lat.items():
        print("lattice %-9s " % k + ", ".join("%s %.4g" % (kk, v[kk]) for kk in gold))
    for s_ in STUMPS:
        print("over %s: " % s_ + ", ".join("%s %.4g" % (k, over[s_][k]) for k in MEMBERS))
    print("variants:")
    for v in names:
        print("  %-46s " % v + ", ".join("%s %.4g" % (k, fam[v][k]) for k in gold))
    print("falsification: " + ", ".join("%s %.3f" % kv for kv in fals.items()))
    print()
    return corelib.run(spec)


if __name__ == "__main__":
    sys.exit(main())
