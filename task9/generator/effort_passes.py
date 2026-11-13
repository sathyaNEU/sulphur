"""task9: the passes, run end to end on the cut pack. The golden is analysis.py's; the rivals are the other methods a
careful analyst could defend at each result (they set the bands); the careful but hurried pass is what a frontier run
files in a hurry at each result, calibrated to the run record (references/precedents.json); the quick pass is ten
minutes on the obvious file. Writes generator/effort.json from the same objects that write figures.json."""
import numpy as np

import analysis as A

CAUSE = {"R2": "the oxide slurry loop's flow (EP-114), graded by each polisher's distance along it",
         "R3": "the pre-gate bench's chemical life (ECN-2026-0417)",
         "R4": "DP2B's SH-300-C showerhead and CM3's R8 edge-zone tune, cancelling on the wafers that run both",
         "R5": "the deep contact recipe's polymer load on ET1B and ET3A"}


def rivals(F, X):
    """the golden family at each VR90 figure"""
    pk, sc, bc, ec, eg, bl = X["pk"], X["sc"], X["bc"], X["ec"], X["eg"], X["vr"]["blocks"]
    out = {}
    for name, opt in (("block yields read directly at VR90's area", dict(nb="interp")),
                      ("the cluster fit on VX40's blocks alone", dict(nb="vx40")),
                      ("the cluster fit on VP12's blocks alone", dict(nb="vp12")),
                      ("VR90 split evenly between CM1 and CM3", dict(mix="even13")),
                      ("particle kill per mm2 read from VP12", dict(etch_kill="VP12")),
                      ("the gate oxide fit at a straight hinge", dict(goi=dict(bc["goi"], gamma=1.0, k_per_mm2=_k_gamma1(pk, bc))))):
        out[name] = A.vr90_build(pk, sc, bc, ec, eg, opt, blocks=bl)
    out["bin 5 pooled over VX40 and VP12 per mm2 of die"] = A.vr90_build(pk, A.pooled_scratch(pk, sc), bc, ec, eg, {}, blocks=bl)
    return out


def _k_gamma1(pk, bc):
    """the hinge refitted with its power held at one (the rival's own fit, not the golden's coefficient)"""
    xs, ys, gs = [], [], []
    lb = bc["lot_bath"]
    for w in pk.wafers.values():
        if w["lot"] not in lb:
            continue
        risk = w["tested"] - sum(w["bins"].get(b, 0) for b in (3, 4, 5))
        xs.append(lb[w["lot"]][0])
        ys.append(w["bins"].get(6, 0) / max(1, risk))
        gs.append(A.GATE[w["product"]])
    xs, ys, gs = np.array(xs), np.array(ys), np.array(gs)
    z = gs * np.maximum(0.0, xs - bc["goi"]["c_th"])
    M = np.column_stack([gs, z])
    coef, *_ = np.linalg.lstsq(M, ys, rcond=None)
    return float(coef[1])


def hurried(F, X):
    """the careful but hurried pass and the quick pass, each result's method run on the pack"""
    pk, sc, bc, ec, eg, bl = X["pk"], X["sc"], X["bc"], X["ec"], X["eg"], X["vr"]["blocks"]
    ec1 = A.etch_cause(pk, kappa_fixed=1.0)
    car = A.vr90_build(pk, sc, bc, ec1, eg, dict(uniform_loop=True, q1_bath="q3", kappa=1.0, edge_plan="none",
                                                 nb="alpha=2"), blocks=bl)
    single = {k: A.vr90_build(pk, sc, bc, ec, eg, o, blocks=bl) for k, o in (
        ("uniform_loop", dict(uniform_loop=True)), ("q3_bath", dict(q1_bath="q3")),
        ("harmonise", dict(edge_plan="none")), ("poisson", dict(nb="poisson")), ("alpha2", dict(nb="alpha=2")))}
    single["kappa1"] = A.vr90_build(pk, sc, bc, ec1, eg, dict(kappa=1.0), blocks=bl)
    # the quick pass: VX40's own yields carried to VR90 as they are
    vx_base = F["R1"]["VX40"]["base"] / F["R1"]["VX40"]["gross"]
    vx_win = F["R1"]["VX40"]["win"] / F["R1"]["VX40"]["gross"]
    return dict(careful=car, single=single, ec1=ec1, quick=dict(fixed=vx_base, plan=vx_win))


def bands(F, X, R):
    """each graded figure's band: the span of the rival methods and readings run on the pack, with a margin of half the
    figure's printed precision plus the noise the rivals leave"""
    g = X["vr"]
    B = {}
    r1 = F["R1"]
    B["R1"] = {p: (round(min(r1[p]["shortfall"], F["R1_first"][p]) - 1.2, 1), round(max(r1[p]["shortfall"], F["R1_first"][p]) + 1.2, 1))
               for p in ("VX40", "VP12")}
    vr = [g] + list(R.values())
    def span(vals, m, k=1):
        return (round(min(vals) - m, k), round(max(vals) + m, k))
    for rid, c, key in (("R2", "loop", None), ("R3", "bath", None), ("R4", "edge", None), ("R5", "etch", None)):
        adj = F[rid]["cost_vx40"]
        raw = F[rid].get("raw_vx40", F[rid].get("excess_vx40", adj))
        cell = {"VX40": span([adj, raw], 0.6), "VR90": span([v["cost"][c] for v in vr], 0.5 if c != "edge" else 0.25,
                                                            1 if c != "edge" else 2)}
        if rid == "R5":
            nf = [v["no_flake"] for v in vr]
            cell["interval"] = (int(round((min(nf) - 120) / 10.0) * 10), int(round((max(nf) + 130) / 10.0) * 10))
        B[rid] = cell
    B["R6"] = span([100 * v["y_fixed"] for v in vr], 0.8)
    lo, hi = B["R6"]
    st = lambda y: 412000 / (184 * y / 100.0 * 0.992 * 0.981)
    B["R7"] = {"plan": span([100 * v["y_plan"] for v in vr], 0.7),
               "starts": (int(round(st(hi) / 10.0) * 10), int(round(st(lo) / 10.0) * 10))}
    return B


BANDS = {}
LABEL = {"R2": "the slurry loop", "R3": "the bench chemical life", "R4": "DP2B and CM3 together", "R5": "the deep recipe's polymer"}
QUARTER_VALUE_PER_POINT = None   # set from the cost inputs in figures.py


def change_set(vr, wafers=None):
    """the changes the plan needs: each cause whose VR90 quarter value beats its own quarterly cost"""
    starts = vr["starts_fixed"] if wafers is None else wafers
    per_pt = 0.01 * starts * 184 * 41.0
    cost = {"loop": (78.0 - 32.0) * 8760 * 0.19 / 4, "bath": (486000 - 272000) / 4, "edge": 38400 + 16 * 2400,
            "etch": 2 * 13 * 640 * max(0.0, 1.0 / max(vr["no_flake"], 1) - 1.0 / 2400) * 2900}
    out = []
    for c in ("loop", "bath", "edge", "etch"):
        if vr["cost"][c] * per_pt > cost[c]:
            out.append(c)
    return out


def build(F, X, FG):
    pk, sc, bc, ec, eg, bl = X["pk"], X["sc"], X["bc"], X["ec"], X["eg"], X["vr"]["blocks"]
    R, H = rivals(F, X), hurried(F, X)
    BANDS.clear()
    BANDS.update(bands(F, X, R))
    g, car, q = X["vr"], H["careful"], H["quick"]
    f = FG
    def cells(rid, d, extra=None):
        out = {k: v for k, v in d.items()}
        if extra:
            out.update(extra)
        return out
    res = [
        dict(id="R1", name="the June to September shortfall in good die per wafer, VX40 and VP12", graded_as="Ask 1",
             figure="R1_shortfall", depends=[], independent="the sort database's final insertions",
             golden=f["R1_shortfall"], bands={k: list(v) for k, v in BANDS["R1"].items()}, partly_share=0.5,
             passes=dict(quick=f["R1_shortfall"], careful=f["R1_shortfall"], thorough=f["R1_shortfall"])),
        dict(id="R2", name="the scratch cause: what it is, its cost per VX40 wafer and what fixing it adds to VR90 under the plan",
             graded_as="Component 1, Ask 2", figure="R2_loop", depends=[], independent="the loop's trend, line list and the polishers' exports",
             golden=f["R2_loop"], bands={k: list(v) for k, v in BANDS["R2"].items()}, partly_share=0.5,
             passes=dict(quick=dict(cause="CM3", VX40=f["R2_loop"]["VX40"], VR90=0.0),
                         careful=dict(cause=LABEL["R2"], VX40=f["R2_loop"]["VX40"], VR90=round(car["cost"]["loop"], 1)),
                         thorough=f["R2_loop"]), precedent=["L26", "L38"]),
        dict(id="R3", name="the bath cause: what it is, its cost per VX40 wafer and what fixing it adds to VR90 under the plan",
             graded_as="Ask 3", figure="R3_bath", depends=[], independent="the bench controller log and the lab's samples",
             golden=f["R3_bath"], bands={k: list(v) for k, v in BANDS["R3"].items()}, partly_share=0.5,
             passes=dict(quick=dict(cause="CM3", VX40=0.0, VR90=0.0),
                         careful=dict(cause=LABEL["R3"], VX40=f["R3_bath"]["VX40"], VR90=round(car["cost"]["bath"], 1)),
                         thorough=f["R3_bath"]), precedent=["L36", "N12"]),
        dict(id="R4", name="the edge cause: what it is, its cost per VX40 wafer and what fixing it adds to VR90 under the plan",
             graded_as="Component 2, Ask 4", figure="R4_edge", depends=[], independent="the deposition log, the polishers' exports and the 49-site maps",
             golden=f["R4_edge"], bands={k: list(v) for k, v in BANDS["R4"].items()}, partly_share=0.5,
             passes=dict(quick=dict(cause="CM3", VX40=f["R4_edge"]["VX40"], VR90=0.0),
                         careful=dict(cause="CM3 R8", VX40=f["R4_edge"]["VX40"], VR90=0.0),
                         thorough=f["R4_edge"]), precedent=["L01", "L06"]),
        dict(id="R5", name="the etch cause: what it is, its cost per VX40 wafer, what fixing it adds to VR90 under the plan, and the clean interval",
             graded_as="Component 3, Ask 5", figure="R5_etch", depends=[], independent="the contact-etch summary, the monitors and the PM log",
             golden=f["R5_etch"], bands={k: list(v) for k, v in BANDS["R5"].items()}, partly_share=0.5,
             passes=dict(quick=dict(cause="CM3", VX40=0.0, VR90=0.0, interval=2400),
                         careful=dict(cause="RF hours", VX40=round(H["ec1"]["cost_vx40"], 1), VR90=round(car["cost"]["etch"], 1),
                                      interval=int(round(car["no_flake"] / 10) * 10)),
                         thorough=f["R5_etch"]), precedent=["L36", "N04", "L37"]),
        dict(id="R6", name="VR90's Q1 2027 sort yield with every cause fixed", graded_as="Component 4, Ask 6", figure="R6_fixed",
             depends=[], independent="the January to March die maps", golden=f["R6_fixed"], band=list(BANDS["R6"]),
             partly=[BANDS["R6"][0] - 0.6, BANDS["R6"][1] + 0.6],
             passes=dict(quick=round(100 * q["fixed"], 1), careful=round(100 * car["y_fixed"], 1), thorough=f["R6_fixed"]),
             precedent=["L22"]),
        dict(id="R7", name="VR90's Q1 2027 sort yield under the ramp plan as filed, and the wafer starts with every cause fixed",
             graded_as="Recommendation, Component 5, Ask 7", figure="R7_plan", depends=["R2", "R3", "R4", "R5", "R6"],
             independent="", golden=f["R7_plan"], bands={k: list(v) for k, v in BANDS["R7"].items()}, partly_share=0.5,
             passes=dict(quick=dict(plan=round(100 * q["plan"], 1), starts=int(round(412000 / (184 * q["fixed"] * 0.992 * 0.981), -1))),
                         careful=dict(plan=round(100 * car["y_plan"], 1), starts=int(round(car["starts_fixed"], -1))),
                         thorough=f["R7_plan"]), precedent=["L32", "L11"]),
    ]
    routes = [dict(name="the golden", golden=True, answer=[round(100 * g["y_plan"], 1), round(100 * g["y_fixed"], 1), change_set(g)])]
    names = {"uniform_loop": "the far polishers' excess booked to their own filters and pads",
             "q3_bath": "the bath carried at the summer's loading",
             "harmonise": "CM3's harmonisation taken as the edge fix",
             "poisson": "VR90 read on a Poisson die-area formula",
             "alpha2": "VR90 read on a cluster factor of 2",
             "kappa1": "the etch cleans scaled by RF time alone"}
    for k, v in H["single"].items():
        cs = change_set(v)
        if k == "uniform_loop":
            cs = ["CM1 and CM3 filters and pads"] + [c for c in cs if c != "loop"]
        if k == "harmonise":
            cs = [c for c in cs if c != "edge"] + ["CM3 harmonised alone"]
        routes.append(dict(name=names[k], answer=[round(100 * v["y_plan"], 1), round(100 * v["y_fixed"], 1), cs]))
    routes.append(dict(name="the careful but hurried pass", answer=[round(100 * car["y_plan"], 1), round(100 * car["y_fixed"], 1),
                                                                   ["loop", "CM1 and CM3 filters and pads", "bath", "CM3 harmonised alone",
                                                                    "etch on RF hours"]]))
    routes.append(dict(name="VX40's own yields carried to VR90", answer=[round(100 * q["plan"], 1), round(100 * q["fixed"], 1), []]))
    golden_set = change_set(g)
    fam = [dict(name=k, answer=change_set(v)) for k, v in R.items()]
    shortcuts = [dict(name=r["name"], answer=r["answer"][2]) for r in routes[1:]]
    pert = []
    import copy
    for name, mod in (("scratch rates 20 per cent lower", ("sc", 0.8)), ("scratch rates 20 per cent higher", ("sc", 1.2)),
                      ("bath drag 20 per cent lower", ("drag", 0.8)), ("bath drag 20 per cent higher", ("drag", 1.2)),
                      ("polymer factor 20 per cent lower", ("kappa", 0.8)), ("polymer factor 20 per cent higher", ("kappa", 1.2)),
                      ("thick-edge kill 20 per cent lower", ("thick", 0.8)), ("thick-edge kill 20 per cent higher", ("thick", 1.2))):
        sc2, bc2, ec2, eg2 = sc, bc, ec, eg
        k, m = mod
        if k == "sc":
            sc2 = dict(sc, by_regime={t: {r: x * m for r, x in v.items()} for t, v in sc["by_regime"].items()})
        elif k == "drag":
            bc2 = dict(bc, fit=dict(bc["fit"], drag=bc["fit"]["drag"] * m))
        elif k == "kappa":
            ec2 = dict(ec, fit=dict(ec["fit"], kappa=ec["fit"]["kappa"] * m))
        else:
            e_, r_ = eg["thick_rate"]
            eg2 = dict(eg, thick_rate=(e_, r_ * m))
        v = A.vr90_build(pk, sc2, bc2, ec2, eg2, None, blocks=bl)
        pert.append(dict(input=name, answer=change_set(v)))
    forcing = dict(kind="set", what="the changes the ramp plan needs, each paying for itself in VR90's Q1 die value",
                   golden_answer=golden_set, golden_family=fam, shortcuts=shortcuts, perturbations=pert)
    hints = [dict(sentence="Contact-etch polymer builds per RF second about 1.7 times faster on the deep recipe", rescues=["R5"]),
             dict(sentence="The slurry loop's scratching grows with each polisher's distance along it", rescues=["R2"]),
             dict(sentence="DP2B's thick edge and CM3's thin-edge tune cancel on the wafers that run both", rescues=["R4"]),
             dict(sentence="The bath's metals build with every lot between spikes and changes, so the bench's loading sets them", rescues=["R3"]),
             dict(sentence="Defects cluster, so a large die yields more than a die-area formula says", rescues=["R6"])]
    # every result is also a sub-ask in Supplementary Questions, so each carries its block's share plus its own share of
    # the asks: the asks' 55 over seven sub-asks (7.857 each), the components' 24 over four, the call's 14 on R7
    ask = 55.0 / 7
    weights = {"recommendation": round(14 + ask, 3), "components": round(24 + 4 * ask, 3), "asks": round(2 * ask, 3),
               "instruction": 7}
    single = H["single"]
    shortcut = dict(careful_plan=round(100 * car["y_plan"], 1), careful_fixed=round(100 * car["y_fixed"], 1),
                    poisson_fixed=round(100 * single["poisson"]["y_fixed"], 1), alpha2_fixed=round(100 * single["alpha2"]["y_fixed"], 1),
                    uniform_loop_vr90=round(single["uniform_loop"]["cost"]["loop"], 1),
                    q3_bath_vr90=round(single["q3_bath"]["cost"]["bath"], 1),
                    kappa1_vr90=round(single["kappa1"]["cost"]["etch"], 1),
                    kappa1_interval=int(round(single["kappa1"]["no_flake"] / 10.0) * 10))
    return dict(results=res, routes=routes, forcing=forcing, hints=hints, weights=weights, _shortcut=shortcut)
