"""The golden cost model for task24 and the hurried routes, from the tables (clean tables now; the pack's files once
cut). Each judgment is a switch so the stump factorial is computed from the same code:
  c1  QA returns: per-object issue rates aggregated over each image (any found issue returns it), corrections that
      re-check every object and are reviewed again at an intensity that rises with the image's own (golden) | a
      logistic model of the first-pass return on the image's object counts, with 2026's re-return share of corrected
      tasks carried along the chain (hurried, cfg qa="logit_const"; "logit_one" stops at one correction, "scene"
      carries 2026's return share by scene type with one correction)
  c2  floor top-up: each annotator-week's piece pay against the centre's hourly floor over the spread of speeds
      and weeks (golden) | the floor applied to the request's average paid time per image (hurried, cfg
      floor="average"; "share" carries 2026's top-up share of piece pay)
  c3  video: frame time on frames, objects on screen and tracks starting and ending in each chunk (golden) | on
      frames and objects on screen (hurried)
"""
import math

import numpy as np
import pandas as pd
from scipy.optimize import minimize

COUNT_COLS = ["n_S_clr", "n_S_occ", "n_M_clr", "n_M_occ", "n_L_clr", "n_L_occ"]


def _ls_nonneg(X, y):
    from scipy.optimize import nnls
    b, _ = nnls(X, y)
    return b


# ------------------------------------------------------------------ fits on the 2026 record
def fit_time_box(P):
    f = P[(P.kind == "box") & (P.pass_no == 1)].copy()
    X = np.column_stack([np.ones(len(f))] + [f[c].to_numpy(float) for c in COUNT_COLS])
    y = f.active_seconds.to_numpy(float)
    speed = pd.Series(1.0, index=f.annotator_id.unique())
    for _ in range(4):
        s = speed.reindex(f.annotator_id).to_numpy()
        beta = _ls_nonneg(X, y / s)
        pred = X @ beta
        speed = (pd.Series(y / pred).groupby(f.annotator_id.to_numpy()).median())
        speed = speed / np.exp(np.log(speed).mean())
    return dict(beta=beta, speed=speed)


def fit_time_poly(P, speed):
    f = P[(P.kind == "polygon") & (P.pass_no == 1)].copy()
    X = np.column_stack([np.ones(len(f)), f.n_poly - f.n_poly_occ, f.n_poly_occ, f.vertices]).astype(float)
    s = speed.reindex(f.annotator_id).fillna(1.0).to_numpy()
    return _ls_nonneg(X, f.active_seconds.to_numpy(float) / s)


def video_features(P, vtracks, vchunks):
    """Join the archive's tracks to each chunk: tracks that start in it, tracks that end in it before their
    sequence ends, and object-frames on screen."""
    seq_end = vtracks.groupby(["project", "seq"]).last_frame.max().rename("seq_last")
    tr = vtracks.join(seq_end, on=["project", "seq"])
    ch = vchunks.copy()
    ch["starts"] = 0; ch["ends"] = 0
    for (pj, sq), g in ch.groupby(["project", "seq"]):
        t = tr[(tr.project == pj) & (tr.seq == sq)]
        for i, row in g.iterrows():
            ch.at[i, "starts"] = int(((t.first_frame >= row.frame_from) & (t.first_frame <= row.frame_to)).sum())
            ch.at[i, "ends"] = int(((t.last_frame >= row.frame_from) & (t.last_frame <= row.frame_to) &
                                   (t.last_frame < t.seq_last)).sum())
    return ch


def fit_time_video(P, chf, speed, flow=True):
    f = P[(P.kind == "video") & (P.pass_no == 1)][["item_ref", "annotator_id", "active_seconds"]].merge(
        chf[["item_ref", "frames", "frame_objects", "starts", "ends"]], on="item_ref", how="left")
    s = speed.reindex(f.annotator_id).fillna(1.0).to_numpy()
    if flow:
        X = np.column_stack([np.ones(len(f)), f.frames, f.frame_objects, f.starts, f.ends]).astype(float)
    else:
        X = np.column_stack([np.ones(len(f)), f.frames, f.frame_objects]).astype(float)
    return _ls_nonneg(X, f.active_seconds.to_numpy(float) / s)


def fit_issues(P, R, prior=2.0):
    """Found issues per review as Poisson with an intensity linear in the object counts, a care multiplier per
    annotator, and a second-review multiplier for corrected images."""
    j = P.merge(R[["pass_key", "found_missed", "found_misplaced", "seconds"]], on="pass_key")
    b = j[j.kind == "box"].copy()
    b["y"] = b.found_missed + b.found_misplaced
    X = b[COUNT_COLS].to_numpy(float)
    first = (b.pass_no == 1).to_numpy()
    y = b.y.to_numpy(float)
    care = pd.Series(1.0, index=b.annotator_id.unique())
    lam = np.full(X.shape[1], 0.005)
    for _ in range(3):
        cw = care.reindex(b.annotator_id).to_numpy()
        def nll(theta):
            l = np.exp(theta)
            mu = cw[first] * (X[first] @ l)
            return -(y[first] * np.log(mu + 1e-12) - mu).sum()
        res = minimize(nll, np.log(lam), method="L-BFGS-B")
        lam = np.exp(res.x)
        pred = care.reindex(b.annotator_id).to_numpy() * (X @ lam)
        g = pd.DataFrame(dict(a=b.annotator_id[first], y=y[first], p=pred[first] / cw[first])).groupby("a").sum()
        care = (g.y + prior) / (g.p + prior)    # a light prior, a careful analyst's shrink toward one
        care = care / np.average(care, weights=g.p)
    cw = care.reindex(b.annotator_id).to_numpy()
    second = ~first
    m2 = y[second].sum() / (cw[second] * (X[second] @ lam)).sum()
    return dict(lam=lam, care=care, m2=m2)


def _logit_fit(X, y):
    Xc = np.column_stack([np.ones(len(X)), X])
    mu, sd = Xc.mean(axis=0), Xc.std(axis=0)
    mu[0], sd[0] = 0.0, 1.0
    Z = (Xc - mu) / sd

    def f(w):
        z = Z @ w
        return float((np.logaddexp(0.0, z) - y * z).sum()), Z.T @ (1.0 / (1.0 + np.exp(-z)) - y)
    w = minimize(f, np.zeros(Z.shape[1]), jac=True, method="L-BFGS-B").x
    return dict(w=w, mu=mu, sd=sd)


def logit_predict(m, X):
    Xc = np.column_stack([np.ones(len(X)), X])
    return 1.0 / (1.0 + np.exp(-(((Xc - m["mu"]) / m["sd"]) @ m["w"])))


def fit_returns(P, R):
    """The hurried QA inputs: a logistic model of a first pass's return on its object counts, and 2026's share of
    corrected tasks returned again."""
    j = P.merge(R[["pass_key", "found_missed", "found_misplaced"]], on="pass_key")
    b = j[j.kind == "box"]
    ret = ((b.found_missed + b.found_misplaced) > 0).to_numpy(float)
    first = (b.pass_no == 1).to_numpy()
    X = b[COUNT_COLS].to_numpy(float)
    n = X.sum(axis=1)
    cut = np.digitize(n, BINS)
    t1 = pd.Series(ret[first]).groupby(cut[first]).mean()
    t2 = pd.Series(ret[~first]).groupby(cut[~first]).mean()
    return dict(logit=_logit_fit(X[first], ret[first]), rereturn=float(ret[~first].mean()),
                logit2=_logit_fit(X[~first], ret[~first]), bin_first=t1.to_dict(), bin_corr=t2.to_dict())


BINS = [20, 40, 60, 80, 100, 120]


def fit_corrections(P, R, speed):
    j = P.merge(R[["pass_key", "found_missed", "found_misplaced"]], on="pass_key")
    prev = j[["item", "pass_no", "found_missed", "found_misplaced"]].copy()
    prev["pass_no"] = prev.pass_no + 1
    c = P[(P.kind == "box") & (P.pass_no > 1)].merge(prev, on=["item", "pass_no"], how="left")
    s = speed.reindex(c.annotator_id).fillna(1.0).to_numpy()
    X = np.column_stack([np.ones(len(c)), c.nobj, c.found_missed.fillna(0), c.found_misplaced.fillna(0)]).astype(float)
    return _ls_nonneg(X, c.active_seconds.to_numpy(float) / s)


def fit_reviews(P, R):
    j = P.merge(R[["pass_key", "seconds"]], on="pass_key")
    out = {}
    for kind, g in j.groupby("kind"):
        X = np.column_stack([np.ones(len(g)), g.nobj]).astype(float)
        out[kind] = _ls_nonneg(X, g.seconds.to_numpy(float))
    return out


def ratios(P, WK, pay_r, R):
    act = P.groupby(["annotator_id", "week"]).active_seconds.sum().rename("act")
    wk = WK.join(act, on=["annotator_id", "week"]).dropna(subset=["act"])
    ann_ratio = (wk.groupby("centre").paid_hours.sum() * 3600 / wk.groupby("centre").act.sum())
    revsec = R.groupby("centre").seconds.sum()
    rev_paid = pay_r.groupby("site").paid_hours.sum() * 3600
    return dict(ann=ann_ratio, rev=rev_paid / revsec, rev_pooled=float(rev_paid.sum() / revsec.sum()))


# ------------------------------------------------------------------ a request's cost per image
CFG = dict(care_spread=True, care_prior=2.0, max_reviews=4, week_noise=True, paid_week="clock", video_terms="full",
           rev_ratio="centre", hinge="per_annotator", qa="logit_const", floor="average", staff_basis="images")


def staff_for(T, kind):
    """The pricing policy's staffing: annotators on the roster at the pull with the skill, shares by contracted hours."""
    ann = T["ann"]
    e = ann[(ann.left_date.isna()) & ann.skills.apply(lambda s: kind in s)].copy()
    e["share"] = e.scheduled_hours / e.scheduled_hours.sum()
    return e[["annotator_id", "centre", "scheduled_hours", "share"]]


def request_cost(T, F, kind, sample, c1=True, c2=True, c3=True, H=None, key=None, staff=None, cfg=None, sims=300, seed=7,
                 scale=None):
    import world as Wd
    cfg = dict(CFG, **(cfg or {}))
    scale = scale or {}
    rates, centres = Wd.RATES, Wd.CENTRES
    beta = F["time"]["beta"] * scale.get("time", 1.0)
    speed = F["time"]["speed"]
    staff = staff if staff is not None else staff_for(T, kind)
    if cfg.get("staff_basis") == "hours":     # contracted hours of work, so the faster annotators deliver more images
        staff = staff.copy()
        w = staff.scheduled_hours / staff.annotator_id.map(F["time"]["speed"]).fillna(1.0)
        staff["share"] = w / w.sum()
    sh = staff.share.to_numpy()
    if kind == "box":
        X = np.column_stack([np.ones(len(sample))] + [sample[c].to_numpy(float) for c in COUNT_COLS])
        t1 = X @ beta
        nobj = sample[COUNT_COLS].sum(axis=1).to_numpy(float)
        piece = nobj * rates["box"]
        frames = np.ones(len(sample))
    elif kind == "polygon":
        bp = F["poly"] * scale.get("time", 1.0)
        t1 = (bp[0] + bp[1] * (sample.n_poly - sample.n_poly_occ) + bp[2] * sample.n_poly_occ + bp[3] * sample.vertices).to_numpy(float)
        nobj = sample.n_poly.to_numpy(float)
        piece = nobj * rates["polygon"]
        frames = np.ones(len(sample))
    else:
        ch = sample
        if c3:
            bv = F["video_flow"] if cfg["video_terms"] == "full" else F["video_flow_noends"]
            t1 = (bv[0] + bv[1] * ch.frames + bv[2] * ch.frame_objects + bv[3] * ch.starts + bv[4] * ch.ends).to_numpy(float)
        else:
            bv = F["video_stock"]
            t1 = (bv[0] + bv[1] * ch.frames + bv[2] * ch.frame_objects).to_numpy(float)
        t1 = t1 * scale.get("time", 1.0)
        nobj = ch.starts.to_numpy(float)
        frames = ch.frames.to_numpy(float)
        piece = nobj * rates["track"] + frames * rates["frame"]
    rv = F["review"][kind]
    if kind == "box" and c1:
        fi = F["issues"] if cfg["care_prior"] == 2.0 else F["issues_light"]
        lam = fi["lam"] * scale.get("issues", 1.0)
        m2 = fi["m2"]
        care = fi["care"]
        cw = staff.annotator_id.map(care).fillna(1.0).to_numpy() if cfg["care_spread"] else np.ones(len(staff))
        D = sample[COUNT_COLS].to_numpy(float) @ lam
        q1 = 1 - np.exp(-np.outer(D, cw))
        q2 = 1 - np.exp(-np.outer(D * m2, cw))
        chain = q1 * (1 + q2 + q2 * q2) if cfg["max_reviews"] >= 4 else q1 * (1 + q2)
        ecorr = chain @ sh
        bc = F["corr"]
        fix_t = bc[0] + bc[1] * nobj + bc[2] * np.minimum(D, 3.0)
        corr_t = ecorr * fix_t
        reviews = 1 + ecorr
    elif kind == "box" and cfg["qa"] in ("logit_const", "logit_one", "logit_logit", "binned_binned", "binned_const"):
        Xs = sample[COUNT_COLS].to_numpy(float)
        fr = F["returns"]
        if cfg["qa"].startswith("logit"):
            p1 = logit_predict(fr["logit"], Xs)
        else:
            cb = np.digitize(Xs.sum(axis=1), BINS)
            p1 = np.array([fr["bin_first"].get(c, fr["bin_first"][max(fr["bin_first"])]) for c in cb])
        if cfg["qa"] == "logit_logit":
            r2 = logit_predict(fr["logit2"], Xs)
        elif cfg["qa"] == "binned_binned":
            r2 = np.array([fr["bin_corr"].get(c, fr["bin_corr"][max(fr["bin_corr"])]) for c in cb])
        else:
            r2 = fr["rereturn"]
        ecorr = p1 if cfg["qa"] == "logit_one" else p1 * (1 + r2 + r2 * r2)
        D = sample[COUNT_COLS].to_numpy(float) @ F["issues"]["lam"]
        bc = F["corr"]
        corr_t = ecorr * (bc[0] + bc[1] * nobj + bc[2] * np.minimum(D, 3.0))
        reviews = 1 + ecorr
    else:              # 2026's return share by scene type with one correction; polygons and video in every route
        share_r = H["return_share"][key] if H else 0.05
        fix_t = H["fix_seconds"][key] if H else 60.0
        corr_t = np.full(len(t1), share_r * fix_t); reviews = np.full(len(t1), 1 + share_r)
    ann_act = float((t1 + corr_t).mean())                     # active seconds per task for a pace of one
    rev_act = float((reviews * (rv[0] + rv[1] * nobj)).mean())
    piece_task = float(piece.mean())
    # each annotator: pace, productive share of paid time, paid week, week-to-week spread
    prod = F["prod"]; pw = F["paid_week"]; wsd = F["week_sd"]
    pm = float(np.mean(list(prod.values())))
    rng = np.random.default_rng(seed)
    paid_task, tau = [], []
    for a in staff.itertuples():
        s_i = float(speed.get(a.annotator_id, 1.0)) * scale.get("pace", 1.0)
        p_i = float(prod.get(a.annotator_id, pm))
        P_i = float(pw.get(a.annotator_id, a.scheduled_hours * 0.95)) if cfg["paid_week"] == "clock" else float(a.scheduled_hours)
        sec_i = ann_act * s_i
        paid_task.append(sec_i / p_i / 3600.0)
        if c2:
            f = np.exp(rng.normal(0, wsd.get(a.annotator_id, 0.07), sims)) if cfg["week_noise"] else np.ones(1)
            imgs = P_i * 3600.0 * p_i / (sec_i * f)
            top = np.maximum(0.0, centres[a.centre]["floor"] * P_i - imgs * piece_task)
            tau.append(top.mean() / imgs.mean())
    ann_paid_h = float(np.dot(sh, paid_task))
    fl = float(np.dot(sh, [centres[c]["floor"] for c in staff.centre]))
    if c2 and cfg["hinge"] == "per_annotator":
        topup = float(np.dot(sh, tau))
    elif (c2 and cfg["hinge"] == "average") or (not c2 and cfg["floor"] == "average"):
        topup = max(0.0, fl * ann_paid_h - piece_task)        # the floor on the request's average paid time
    else:
        topup = H["topup_share"] * piece_task
    share_c = staff.groupby("centre").share.sum()
    if cfg["rev_ratio"] == "centre":
        rr = sum(share_c[c] * F["ratio"]["rev"][c] for c in share_c.index)
    else:
        rr = F["ratio"]["rev_pooled"]
    rev_paid_h = rev_act / 3600.0 * rr
    rev_rate = sum(share_c[c] * centres[c]["rev_rate"] for c in share_c.index)
    cost = piece_task + topup + rev_paid_h * rev_rate + Wd.OVERHEAD_PER_PAID_HOUR * (ann_paid_h + rev_paid_h)
    per = float(np.mean(frames)) if kind == "video" else 1.0
    return dict(cost=cost / per, piece=piece_task / per, topup=topup / per, reviews=float(np.mean(reviews)),
                corrections=float(np.mean(reviews) - 1), ann_min=ann_paid_h * 60 / per, rev_min=rev_paid_h * 60 / per,
                first_min=float(t1.mean()) / 60 / per, unit_per_task=per)


def fit_all(T):
    P, R, WK = T["P"], T["R"], T["WK"]
    F = {}
    F["time"] = fit_time_box(P)
    sp = F["time"]["speed"]
    F["poly"] = fit_time_poly(P, sp)
    chf = T["chunks"]
    F["video_flow"] = fit_time_video(P, chf, sp, True)
    F["video_stock"] = fit_time_video(P, chf, sp, False)
    F["returns"] = fit_returns(P, R)
    chn = chf.assign(ends=0)
    F["video_flow_noends"] = fit_time_video(P, chn, sp, True)
    F["issues"] = fit_issues(P, R)
    F["issues_light"] = fit_issues(P, R, prior=0.5)
    F["corr"] = fit_corrections(P, R, sp)
    F["review"] = fit_reviews(P, R)
    F["ratio"] = ratios(P, WK, T["pay_r"], R)
    act = P.groupby(["annotator_id", "week"]).active_seconds.sum().rename("act")
    wk = WK.join(act, on=["annotator_id", "week"]).dropna(subset=["act"])
    F["prod"] = (wk.groupby("annotator_id").act.sum() / (wk.groupby("annotator_id").paid_hours.sum() * 3600)).to_dict()
    F["paid_week"] = wk.groupby("annotator_id").paid_hours.median().to_dict()
    F["week_sd"] = {}
    # weekly speed noise: a worker's weekly seconds per expected second, its spread
    f = P[(P.kind == "box") & (P.pass_no == 1)]
    X = np.column_stack([np.ones(len(f))] + [f[c].to_numpy(float) for c in COUNT_COLS])
    ratio = f.active_seconds.to_numpy() / (X @ F["time"]["beta"])
    g = pd.DataFrame(dict(a=f.annotator_id, w=f.week, r=ratio)).groupby(["a", "w"]).r.median()
    F["week_sd"] = np.log(g).groupby(level=0).std().fillna(0.07).to_dict()
    F["chf"] = chf
    return F


def history(T, F):
    """2026's shares by scene type: the hurried route's inputs."""
    P, R, WK, proj = T["P"], T["R"], T["WK"], T["proj"]
    j = P.merge(R[["pass_key", "found_missed", "found_misplaced"]], on="pass_key").merge(proj[["project", "scene"]], on="project")
    j["ret"] = (j.found_missed + j.found_misplaced) > 0
    first = j[j.pass_no == 1]
    rs = first.groupby("scene").ret.mean()
    corr = P[P.pass_no > 1].merge(proj[["project", "scene"]], on="project").groupby("scene").active_seconds.mean()
    share = {"A": rs["street"], "B": rs["retail"], "D": rs["pallet"], "E": rs["warehouse"], "C": rs.get("urban", 0.05)}
    fix = {"A": corr["street"], "B": corr["retail"], "D": corr["pallet"], "E": corr["warehouse"], "C": corr.get("urban", 60)}
    topup_share = WK.topup.sum() / WK.piece.sum()
    return dict(return_share=share, fix_seconds=fix, topup_share=topup_share)
