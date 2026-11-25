"""The world the pack is cut from: generator/core.py's build(), replayed draw for draw so that what each switch did on
each event day (whether its page arrived, what it took off) and what each study home did can be written into the
files. The replay is asserted equal to core.build() on every array core returns, so the pack carries core's world and
nothing else."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core  # noqa: E402


def replay(seed=core.SEED, n_events=core.N_EVENTS, noise=0.004):
    """core.build() line for line, keeping the draws build() uses and drops: each event's received pages and each
    switch's delivered kW, the step noise, and the study homes' working, reached and treated states."""
    r = np.random.default_rng(seed)
    n_f = [13, 12, 11, 10]
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
    hv = r.uniform(0.55, 1.6, n_feed)
    fm = np.array([2009, 2011, 2016, 2018])[dist] + r.uniform(-3.5, 3.5, n_feed)
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
    vhf = yr <= core.OLD_YEAR
    age = 2026 - yr
    vt = np.array([[0, 1], [-14, 1], [5, 20]])
    ct = np.array([[1, -2], [-31, 9], [17, 11], [27, 2], [-12, 33]])
    von = np.ones((n_events, 3), bool)
    con = np.ones((n_events, 5), bool)
    von[12:20, 2] = False
    von[40:46, 1] = False
    con[:30, 3] = False
    con[33:38, 2] = False
    dm = lambda t: np.sqrt((x[:, None] - t[None, :, 0]) ** 2 + (y[:, None] - t[None, :, 1]) ** 2)
    dv, dc = dm(vt), dm(ct)
    reach = np.empty((n_events, n_s))
    for e in range(n_events):
        reach[e] = np.where(vhf, np.where(von[e][None, :], dv, 1e9).min(1), np.where(con[e][None, :], dc, 1e9).min(1))
    qf = lambda d: 0.80 / (1 + np.exp((d - 18.5) / 3.6))
    hf = lambda a: 0.985 * np.exp(-(a / 30.0) ** 1.7)
    hw = r.random(n_s) < hf(age)
    u_repl = r.random(n_s)
    repl = u_repl < (1 - np.exp(-age * hv[sf] / 22.0))
    disc = repl & (r.random(n_s) < 0.72)
    flag = repl & (r.random(n_s) < 0.93)
    kap = r.lognormal(-0.5 * 0.35 ** 2, 0.35, n_s)
    w = r.uniform(0.65, 1.25, n_events)
    u_order = r.random(n_s)
    order = np.argsort(yr + u_order * 0.999)
    grp = np.empty(n_s, int)
    grp[order] = (np.arange(n_s) * 16) // n_s
    disp = np.zeros((n_events, 16), bool)
    for e in range(n_events):
        disp[e, r.choice(16, r.integers(4, 13), replace=False)] = True
    load = r.uniform(1500, 3500, n_feed)
    recv_all, dl_all, step, noise_all, obs = [], [], [], [], []
    for e in range(n_events):
        recv = r.random(n_s) < qf(reach[e])
        dl = kap * w[e] * recv * hw * (~disc)
        recv_all.append(recv)
        dl_all.append(dl)
        for gi in np.flatnonzero(disp[e]):
            m = grp == gi
            nz = r.normal(0, noise * load)
            st = np.bincount(sf[m], dl[m], n_feed) + nz
            noise_all.append(nz)
            step.append(st)
            obs.append((e, gi))
    n_st = 380
    s_age = r.choice([6, 7], n_st)
    s_hw = r.random(n_st) < hf(s_age)
    s_d = r.uniform(1, 8, n_st)
    s_q = qf(s_d)
    s_kap = r.lognormal(-0.5 * 0.35 ** 2, 0.35, n_st)
    s_tr = r.random((n_events, n_st)) < 0.5
    s_rc = r.random((n_events, n_st)) < s_q[None, :]
    s_nz = r.normal(0, 1.0, (n_events, n_st))
    s_resp = (s_kap[None, :] * s_hw[None, :] * s_rc + s_nz) * s_tr
    return dict(cent=cent, dist=dist, hv=hv, dv=dv, dc=dc, sf=sf, x=x, y=y, yr=yr, vhf=vhf, age=age, vt=vt, ct=ct, von=von, con=con,
                reach=reach, hw=hw, repl=repl, disc=disc, flag=flag, kap=kap, w=w, order_u=u_order, grp=grp, disp=disp,
                load=load, recv=np.array(recv_all), dl=np.array(dl_all), steps=np.array(step), noise=np.array(noise_all),
                obs_eg=np.array(obs), study=dict(age=s_age, hw=s_hw, d=s_d, q=s_q, kap=s_kap, tr=s_tr, rc=s_rc, nz=s_nz,
                                                  resp=s_resp), n_feed=n_feed, n_s=n_s, n_events=n_events)


def build(seed=core.SEED):
    """The replayed world, asserted equal to core.build() array for array."""
    c = core.build(seed)
    w = replay(seed)
    for k in ("dist", "sf", "x", "y", "yr", "vhf", "reach", "hw", "repl", "disc", "flag", "kap", "w", "grp", "disp", "load"):
        assert np.array_equal(np.asarray(c[k]), np.asarray(w[k])), "the replay differs from core.build() on %s" % k
    obs_e, obs_g, obs_f = c["obs"]
    assert np.array_equal(c["step"], w["steps"].reshape(-1)), "the replay's steps differ from core's"
    assert np.array_equal(obs_e, np.repeat(w["obs_eg"][:, 0], w["n_feed"])) and np.array_equal(obs_g, np.repeat(w["obs_eg"][:, 1], w["n_feed"]))
    s_resp, s_tr = c["study"]
    assert np.array_equal(s_resp, w["study"]["resp"]) and np.array_equal(s_tr, w["study"]["tr"])
    # the delivered part of every step, and its noise, add to core's step exactly
    dlv = np.array([np.bincount(w["sf"][w["grp"] == g], w["dl"][e][w["grp"] == g], w["n_feed"]) for e, g in w["obs_eg"]])
    assert np.allclose(dlv + w["noise"], w["steps"], atol=1e-9)
    w["delivered"] = dlv
    # the SCADA minutes behind each event's steps and the commands' slots, which core draws on its own stream
    w["minute_noise"] = c["minute_noise"]
    w["slot"] = c["slot"]
    w["step_win"] = c["step_win"]
    w["core"] = c
    return w


if __name__ == "__main__":
    w = build()
    print("replay equal to core.build():", w["n_s"], "switches,", len(w["obs_eg"]), "commands,", w["steps"].size, "steps")
