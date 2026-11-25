"""The golden, its variant battery, the lattice, the run routes and the falsification check, computed on the arrays
read back from the cut pack with core.py's own estimators (core.main() run on what the files hold instead of on
core's world). Every figure the answer blocks state comes from here."""
import itertools

import numpy as np

import core as C

BAND_ROOM = 0.25


def variants(wd, gm):
    obs_e = wd["obs"][0]
    th_cell = np.array([[gm["a"][d] * gm["h"][gi] for gi in range(16)] for d in range(4)])
    pred = np.einsum("nrk,r,k->n", C.tensor(wd, wd["reach"]), gm["q"], gm["c"]) * th_cell[wd["dist"][wd["obs"][2]], wd["obs"][1]]
    res = wd["step"] - pred
    sd_f = np.array([res[wd["obs"][2] == f].std() for f in range(wd["n_feed"])])
    V = {
        "bands 7/13/19 km": lambda: C.model(wd, rb=(7.0, 13.0, 19.0)),
        "bands 9/15/21 km": lambda: C.model(wd, rb=(9.0, 15.0, 21.0)),
        "bands 8/12/18 km": lambda: C.model(wd, rb=(8.0, 12.0, 18.0)),
        "bands 10/15/20 km": lambda: C.model(wd, rb=(10.0, 15.0, 20.0)),
        "unweighted least squares": lambda: C.model(wd, wls=False),
        "no district term": lambda: C.model(wd, district=False),
        "batch term a line in age": lambda: C.model(wd, batch="line"),
        "first six event days dropped": lambda: C.model(wd, keep=obs_e >= 6),
        "last six event days dropped": lambda: C.model(wd, keep=obs_e < wd["n_events"] - 6),
        "even event days only": lambda: C.model(wd, keep=obs_e % 2 == 0),
        "odd event days only": lambda: C.model(wd, keep=obs_e % 2 == 1),
        "study responders cut at 0.15 kW": lambda: C.model(wd, cut=0.15),
        "study responders cut at 0.35 kW": lambda: C.model(wd, cut=0.35),
        "steps beyond 2.5 sd of the feeder's residual trimmed": lambda: C.model(wd, keep=np.abs(res) < 2.5 * sd_f[wd["obs"][2]]),
    }
    return V


def run(wd):
    ln, cnt = C.lines(wd)
    gm = C.model(wd)
    gold = C.all_figures(wd, gm, ln)
    st = C.study(wd)
    V = variants(wd, gm)
    fam = {name: C.all_figures(wd, fn(), ln) for name, fn in V.items()}
    wd_sh = dict(wd, wx=wd["wx"] - 0.1)
    m_sh = C.model(wd_sh)
    m_sh2 = dict(m_sh, th=m_sh["th"] * (C.W_CP - 0.1) / C.W_CP)
    fam["cooling index measured from 0.1"] = C.all_figures(wd, m_sh2, ln)
    names = list(fam)
    combos = [c_ for k in (1, 2, 3) for c_ in itertools.combinations(C.STUMPS, k)]
    lat = {"+".join(c_): C.all_figures(wd, C.hurried(gm, c_), ln) for c_ in combos}
    reflex = lat["S1+S2+S3"]
    rig = {"rep_w": 0.0, "rep_n": 0.0, "recon_in": 0.0, "recon_out": 0.0, "c1_fringe_loss": 0.0,
           "c3_unwired": 1 - C.FACE["wo_connected"], "c2_failed_old": 1 - st["itt"] / st["working"], "lost_reach": 0.0,
           "lost_unwired": 0.0}
    for nm in ("fix_t", "fix_w"):
        rig[nm] = C.W_CP * cnt[nm] * (st["working"] - st["itt"])
    rig["lost_hw"] = C.W_CP * wd["n_s"] * (st["working"] - st["itt"])
    rig["delivered"] = C.W_CP * wd["n_s"] * st["itt"]
    go = [k for k in C.MEMBERS if rig[k] >= ln[k]]
    rig["plan_kw"] = float(sum(rig[k] for k in go))
    rig["plan_cost_per_kw"] = float(sum(ln[k] for k in go) * C.VALUE / rig["plan_kw"]) if go else 0.0
    wd_gen = dict(wd, now=wd["static_any"],
                  d_new_v=np.minimum(wd["static_any"], np.hypot(wd["x"] - C.NEW_VHF[0], wd["y"] - C.NEW_VHF[1])),
                  d_new_c=np.minimum(wd["static_any"], np.hypot(wd["x"] - C.NEW_CAR[0], wd["y"] - C.NEW_CAR[1])))
    gen_m = C.model(wd, reach=wd["static_any"])
    gen = C.all_figures(wd_gen, gen_m, ln)

    def cut_route(km, year):
        rbc = (km - 1e-9, km, km + 1e-9)
        qc = np.array([1.0, 1.0, 0.0, 0.0])
        th = np.where(wd["yr"] <= year, 0.0, gm["k"])
        m = dict(q=qc, th=th, c=np.array([1.0, 0.0]), k=gm["k"], rb=rbc)
        return C.all_figures(wd_gen, m, ln)

    cut = {"%d km, %d" % (km, yr_): cut_route(km, yr_) for km in (10, 14, 20) for yr_ in (2009, 2011, 2015)}
    over = {"S1": C.all_figures(wd, dict(gm, q=gm["q"] ** 2.5), ln),
            "S2": C.all_figures(wd, dict(gm, th=gm["th"] * 0.6), ln),
            "S3": C.all_figures(wd, C.model(wd, cfix=0.0), ln)}
    sl = C.slices(wd)
    fals = {"golden": C.closure(wd, gm, sl)}
    for c_ in combos:
        fals["+".join(c_)] = C.closure(wd, C.hurried(gm, c_), sl)
    fals["generous"] = C.closure(wd, gen_m, sl, reach=wd["static_any"])
    cal_m = dict(gm, q=np.ones(4), th=np.full(wd["n_s"], st["itt"]), c=np.array([1.0, 1.0]))
    fals["calibrated"] = C.closure(wd, cal_m, sl)
    return dict(ln=ln, cnt=cnt, gm=gm, gold=gold, study=st, fam=fam, names=names, lat=lat, reflex=reflex, rig=rig, gen=gen,
                gen_m=gen_m, cut=cut, over=over, fals=fals, wd_gen=wd_gen)


def band(golden, family):
    lo, hi = min(family + [golden]), max(family + [golden])
    return [lo - BAND_ROOM * (hi - lo), hi + BAND_ROOM * (hi - lo)]


def funded(f, ln):
    return [k for k in C.MEMBERS if f[k] >= ln[k]]


def perturb(wd, A):
    """Each fitted input moved by its defensible spread (20 per cent; the working level 10), the call recomputed."""
    gm, ln = A["gm"], A["ln"]
    out = {}
    q = gm["q"]
    for lab, qq in (("far band reception 20 per cent lower", np.r_[q[:3], q[3] * 0.8]),
                    ("far band reception 20 per cent higher", np.r_[q[:3], min(q[3] * 1.2, 1.0)]),
                    ("middle bands' reception 20 per cent lower", np.r_[q[0], q[1:3] * 0.8, q[3]]),
                    ("middle bands' reception 20 per cent higher", np.r_[q[0], np.minimum(q[1:3] * 1.2, 1.0), q[3]])):
        out[lab] = C.all_figures(wd, dict(gm, q=qq), ln)
    # the batch term moved 20 per cent towards and away from the working level
    for lab, s in (("batch term 20 per cent up", 1.2), ("batch term 20 per cent down", 0.8)):
        th = gm["th"] * s
        out[lab] = C.all_figures(wd, dict(gm, th=th), ln)
    for lab, s in (("replaced-unit term 20 per cent up", 1.2), ("replaced-unit term 20 per cent down", 0.8)):
        c = np.array([1.0, min(gm["c"][1] * s, 1.0)])
        out[lab] = C.all_figures(wd, dict(gm, c=c), ln)
    for lab, s in (("working level 10 per cent up", 1.1), ("working level 10 per cent down", 0.9)):
        out[lab] = C.all_figures(wd, dict(gm, k=gm["k"] * s), ln)
    return out
