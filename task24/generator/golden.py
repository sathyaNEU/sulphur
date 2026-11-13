"""task24: the golden on the cut pack and everything graded against it: each request's cost and drivers with an
80 per cent range, the 2026 delivery cost and each project's actual cost beside the costing, the call, the stump
factorial, the rivals, the perturbations and the shortcuts (effort.json), and figures.json."""
import json
import math

import numpy as np
import pandas as pd

import analysis as A
import readpack as RP
import world as Wd

KIND = {"A": "box", "B": "box", "C": "video", "D": "polygon", "E": "box"}
SCENE = {"A": "street", "B": "retail", "D": "pallet", "E": "warehouse"}
UNIT = {"A": "image", "B": "image", "C": "frame", "D": "image", "E": "image"}
# the stump factorial: two stumps (c1 the QA chain, c3 the video driver); the floor (c2) is a reflex the careful pass
# sets right, so dropping one stump from the golden is the same route as fixing the other alone on the reflex route
ROUTES = {"golden": (1, 1, 1), "reflex": (0, 1, 0), "drop_c1": (0, 1, 1), "drop_c3": (1, 1, 0)}


def history(T):
    """2026's shares by scene type and pooled by kind: the hurried route's inputs."""
    P, R, WK, proj = T["P"], T["R"], T["WK"], T["proj"]
    j = P.merge(R[["pass_key", "found_missed", "found_misplaced"]], on="pass_key").merge(proj[["project", "scene"]], on="project")
    j["ret"] = (j.found_missed + j.found_misplaced) > 0
    first = j[j.pass_no == 1]
    corr = P[P.pass_no > 1].merge(proj[["project", "scene"]], on="project")
    scene_ret = first.groupby("scene").ret.mean().to_dict()
    scene_fix = corr.groupby("scene").active_seconds.mean().to_dict()
    kind_ret = first.groupby("kind").ret.mean().to_dict()
    kind_fix = corr.groupby("kind").active_seconds.mean().to_dict()
    ret = {k: scene_ret.get(SCENE.get(k), kind_ret.get(KIND[k])) for k in KIND}
    fix = {k: scene_fix.get(SCENE.get(k), kind_fix.get(KIND[k])) for k in KIND}
    return dict(return_share=ret, fix_seconds=fix, topup_share=float(WK.topup.sum() / WK.piece.sum()),
                scene_ret=scene_ret, scene_fix=scene_fix, kind_ret=kind_ret, kind_fix=kind_fix)


def cost(T, F, H, key, c=(1, 1, 1), cfg=None, scale=None, sample=None, staff=None):
    return A.request_cost(T, F, KIND[key], T["samples"][key] if sample is None else sample, bool(c[0]), bool(c[1]), bool(c[2]),
                          H=H, key=key, cfg=cfg, scale=scale, staff=staff)


def accept_set(costs, prices):
    return sorted(k for k in costs if prices[k] >= Wd.MARGIN * costs[k] - 1e-12)


# ------------------------------------------------------------------ R1: 2026 as payroll settled it
def delivery_2026(T):
    WK, pr, P, R = T["WK"], T["pay_r"], T["P"], T["R"]
    out = dict(piece=float(WK.piece.sum()), topup=float(WK.topup.sum()), reviewer=float(pr.pay_usd.sum()),
               ann_hours=float(WK.paid_hours.sum()), rev_hours=float(pr.paid_hours.sum()))
    out["overhead"] = Wd.OVERHEAD_PER_PAID_HOUR * (out["ann_hours"] + out["rev_hours"])
    out["total"] = out["piece"] + out["topup"] + out["reviewer"] + out["overhead"]
    # each project's share, as the pricing policy files it
    act = P.groupby(["annotator_id", "week", "project"]).active_seconds.sum().rename("act").reset_index()
    act["w"] = act.act / act.groupby(["annotator_id", "week"]).act.transform("sum")
    wk = act.merge(WK[["annotator_id", "week", "piece", "topup", "paid_hours"]], on=["annotator_id", "week"])
    wk["cost"] = wk.w * (wk.piece + wk.topup + Wd.OVERHEAD_PER_PAID_HOUR * wk.paid_hours)
    proj_cost = wk.groupby("project").cost.sum()
    rv = R.merge(P[["pass_key", "project"]], on="pass_key")
    local = pd.to_datetime(rv.reviewed_at_utc, utc=True) + pd.to_timedelta(rv.centre.map({"KSM": 3, "ILO": 8}), unit="h")
    rv["week"] = [(d - RP.WEEK0).days // 7 for d in local.dt.date]          # the reviewer's local pay week
    rs = rv.groupby(["reviewer_id", "week", "project"]).seconds.sum().rename("s").reset_index()
    rs["w"] = rs.s / rs.groupby(["reviewer_id", "week"]).s.transform("sum")
    rw = rs.merge(pr.rename(columns={"staff_id": "reviewer_id"})[["reviewer_id", "week", "pay_usd", "paid_hours"]],
                  on=["reviewer_id", "week"])
    rw["cost"] = rw.w * (rw.pay_usd + Wd.OVERHEAD_PER_PAID_HOUR * rw.paid_hours)
    proj_cost = proj_cost.add(rw.groupby("project").cost.sum(), fill_value=0.0)
    reg = T["proj"].set_index("project")
    per = (proj_cost / reg.delivered_units.reindex(proj_cost.index)).rename("actual")
    out["projects"] = per
    out["project_cost_total"] = float(proj_cost.sum())
    return out


def project_samples(T):
    P = T["P"]
    out = {}
    for p, g in P[P.pass_no == 1].groupby("project"):
        kind = g.kind.iloc[0]
        if kind == "box":
            s = g[A.COUNT_COLS].astype(float).reset_index(drop=True)
        elif kind == "polygon":
            s = g[["n_poly", "n_poly_occ", "vertices"]].astype(float).reset_index(drop=True)
        else:
            s = T["chunks"][T["chunks"].item_ref.isin(set(g.item_ref))].reset_index(drop=True)
        st = g.groupby(["annotator_id"]).size().rename("n").reset_index()
        st = st.merge(T["ann"][["annotator_id", "centre", "scheduled_hours"]], on="annotator_id", how="left")
        st["centre"] = st.centre.fillna(st.annotator_id.str[:3])
        st["scheduled_hours"] = st.scheduled_hours.fillna(40)
        st["share"] = st.n / st.n.sum()
        out[p] = (kind, s, st)
    return out


def costing_2026(T, F, H, c=(1, 1, 1)):
    ps = project_samples(T)
    proj = T["proj"].set_index("project")
    res = {}
    for p, (kind, s, st) in ps.items():
        scene = proj.loc[p, "scene"]
        H2 = dict(H)
        H2["return_share"] = {p: H["scene_ret"].get(scene, H["kind_ret"][kind])}
        H2["fix_seconds"] = {p: H["scene_fix"].get(scene, H["kind_fix"][kind])}
        r = A.request_cost(T, F, kind, s, bool(c[0]), bool(c[1]), bool(c[2]), H=H2, key=p, staff=st)
        res[p] = r["cost"]
    return pd.Series(res)


# ------------------------------------------------------------------ ranges, rivals, perturbations
def resample(s, key, rng):
    """One bootstrap draw of a request's sample: images with replacement; for the video, whole sequences (a sequence's
    tasks share its traffic)."""
    if key == "C":
        seqs = s.seq.unique()
        pick = rng.choice(seqs, len(seqs), replace=True)
        return pd.concat([s[s.seq == q] for q in pick], ignore_index=True)
    return s.iloc[rng.integers(0, len(s), len(s))].reset_index(drop=True)


def ranges(T, F, H, reps=160, seed=11, c=(1, 1, 1)):
    """The expected cost's 80 per cent range: the request's sample resampled (the staff is the roster the pricing
    policy names, so it is not drawn)."""
    rng = np.random.default_rng(seed)
    out = {}
    for k in "ABCDE":
        s = T["samples"][k]
        vals = [cost(T, F, H, k, c, sample=resample(s, k, rng))["cost"] for _ in range(reps)]
        out[k] = [float(np.percentile(vals, 10)), float(np.percentile(vals, 90))]
    return out


# further hurried routes: the reflex route with one judgment taken the cruder way
SHORTCUTS = [("the careful pass with QA at 2026's return share by scene type and one correction", (0, 1, 0), dict(qa="scene")),
             ("the careful pass with QA stopped at one correction", (0, 1, 0), dict(qa="logit_one")),
             ("the careful pass with the floor on the request's average paid time", (0, 0, 0), dict(floor="average")),
             ("the careful pass with floor top-ups at 2026's share of piece pay", (0, 0, 0), dict(floor="share"))]
# careful alternatives for the QA chain alone, with the floor and the video as the golden takes them
ALTERNATIVES = [("QA re-returns extrapolated by a logistic on the counts", dict(qa="logit_logit")),
                ("QA returns and re-returns read from 2026's density bins", dict(qa="binned_binned"))]
RIVALS = [("issue intensities with every annotator's care set to one", dict(care_spread=False)),
          ("each annotator's care estimated with a lighter prior", dict(care_prior=0.5)),
          ("the floor settled without week-to-week variation", dict(week_noise=False)),
          ("paid weeks at contracted hours rather than the clock's", dict(paid_week="contract")),
          ("video time on tracks starting and objects on screen, without track ends", dict(video_terms="no_ends")),
          ("reviewer paid time per review second pooled across centres", dict(rev_ratio="pooled"))]
# a reading the pricing policy rules out (it allots images, not hours, in proportion to contracted hours): run as a check
STAFF_HOURS = ("each annotator's share of the request as contracted hours of work, faster annotators delivering more images",
               dict(staff_basis="hours"))


def compute(target, quick=False):
    T = RP.load(target)
    F = A.fit_all(T)
    H = history(T)
    prices = dict(Wd.OFFERED)
    G = dict(prices=prices)
    route_costs = {r: {k: cost(T, F, H, k, c) for k in "ABCDE"} for r, c in ROUTES.items()}
    G["routes"] = {r: dict(costs={k: v["cost"] for k, v in d.items()}, answer=accept_set({k: v["cost"] for k, v in d.items()}, prices))
                   for r, d in route_costs.items()}
    gold = route_costs["golden"]
    G["requests"] = {k: dict(gold[k], unit=UNIT[k], price=prices[k], line=prices[k] / Wd.MARGIN,
                             accept=prices[k] >= Wd.MARGIN * gold[k]["cost"], lowest_price=Wd.MARGIN * gold[k]["cost"])
                     for k in "ABCDE"}
    G["reflex"] = route_costs["reflex"]
    G["call"] = G["routes"]["golden"]["answer"]
    # further shortcuts
    extra = {}
    for name, c, cfg in SHORTCUTS:
        extra[name] = {k: cost(T, F, H, k, c, cfg=cfg)["cost"] for k in "ABCDE"}
    extra["2026's delivery cost per object carried to each request"] = quick_costs(T, H)
    G["extra"] = {n: dict(costs=v, answer=accept_set(v, prices)) for n, v in extra.items()}
    G["alternatives"] = {}
    for name, cfg in ALTERNATIVES:
        v = {k: cost(T, F, H, k, (0, 1, 1), cfg=cfg) for k in "ABCDE"}
        G["alternatives"][name] = dict(costs={k: x["cost"] for k, x in v.items()}, reviews={k: x["reviews"] for k, x in v.items()},
                                       answer=accept_set({k: x["cost"] for k, x in v.items()}, prices))
    G["rivals"] = {}
    for name, cfg in RIVALS:
        v = {k: cost(T, F, H, k, cfg=cfg)["cost"] for k in "ABCDE"}
        G["rivals"][name] = dict(costs=v, answer=accept_set(v, prices))
    v = {k: cost(T, F, H, k, cfg=STAFF_HOURS[1])["cost"] for k in "ABCDE"}
    G["staff_hours"] = dict(costs=v, answer=accept_set(v, prices))
    G["perturb"] = {}
    for name, sc in [("per-object time 5 per cent higher", dict(time=1.05)), ("per-object time 5 per cent lower", dict(time=0.95)),
                     ("issue intensities 10 per cent higher", dict(issues=1.10)), ("issue intensities 10 per cent lower", dict(issues=0.90)),
                     ("every annotator's pace 4 per cent faster", dict(pace=0.96)), ("every annotator's pace 4 per cent slower", dict(pace=1.04))]:
        v = {k: cost(T, F, H, k, scale=sc)["cost"] for k in "ABCDE"}
        G["perturb"][name] = dict(costs=v, answer=accept_set(v, prices))
    G["ranges"] = ranges(T, F, H, reps=40 if quick else 160)
    G["ranges_reflex"] = ranges(T, F, H, reps=40 if quick else 160, c=ROUTES["reflex"])
    G["r1"] = delivery_2026(T)
    G["costing_golden"] = costing_2026(T, F, H, (1, 1, 1))
    G["costing_reflex"] = costing_2026(T, F, H, ROUTES["reflex"])
    G["H"] = H
    G["F"] = F
    G["T_proj"] = T["proj"]
    return G


def quick_costs(T, H):
    """The ten-minute pass: 2026's delivery cost per object carried to each request's objects per image."""
    r1 = delivery_2026(T)
    P = T["P"]
    first = P[P.pass_no == 1]
    objs = float(first[first.kind != "video"].nobj.sum())
    frames = float(T["chunks"].frames.sum())
    per_obj = r1["total"] / (objs + frames * 1.0)
    out = {}
    for k in "ABCDE":
        s = T["samples"][k]
        if KIND[k] == "box":
            n = float(s[A.COUNT_COLS].sum(axis=1).mean())
        elif KIND[k] == "polygon":
            n = float(s.n_poly.mean())
        else:
            n = 1.0
        out[k] = per_obj * n
    return out
