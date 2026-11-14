"""figures.json and effort.json from the golden and the routes, all computed on the cut pack."""
import copy
import json
import math

import numpy as np

import analysis as A

LC_RUNS = ("kide-13b-code-lc32", "kide-34b-lc64", "kide-8b-lc64", "kide-13b-lc32", "kide-34b-sci")
BRIDGE_KEYS = ["benchmark days", "the run's own mix at the mean rank", "waiting for the slowest rank",
               "padding in packed sequences", "a block across both pods", "hall B held to its contracted load",
               "interruptions and restarts", "provider works and the window's opening", "expected days"]
B26_KEYS = ["benchmark GPU-days", "the runs' own mixes at the mean rank", "waiting for the slowest rank",
            "padding in packed sequences", "blocks across both pods", "hall B held to its contracted load",
            "hall A row 6 cooling fault", "interruptions and restarts", "provider works", "other", "GPU-days held"]
VARIANTS = [
    ("clear intervals 60 kW under the contract", dict(clear_kw=60.0)),
    ("clear intervals 120 kW under the contract", dict(clear_kw=120.0)),
    ("the draw line fitted on 600 or more allocated nodes", dict(min_alloc=600)),
    ("the contract read as the meter's ceiling, 8,089 kW", dict(contract=8089.0)),
    ("the throttle as a straight line in the excess", dict(th_form="lin")),
    ("the throttle as the mean stretch by band of excess", dict(th_form="bins")),
    ("the stretch against each run's own clear steps within three days", dict(th_baseline="local")),
    ("the pod penalty from the registered runs alone", dict(pen_method="registered")),
    ("the pod penalty from each straddling run over its model's best-recorded run in one pod", dict(pen_method="twin")),
    ("the pool cut off at one load, full below it and none above", dict(pool_method="step")),
    ("the pool's back-off as a logistic curve in the registered load", dict(pool_method="logistic")),
    ("the pool's light-load share from runs below 88 per cent of the contract", dict(plateau_below=0.88)),
    ("works at the median overrun ratio", dict(works_stat="median")),
    ("another packing and dealing seed", dict(seed=777)),
    ("no launch delay", dict(launch="none")),
]


def rnd(x, d=1):
    return float(round(float(x), d))


def stretch_runs(G, days, phi=True):
    """Each hall B run's mean step stretch over its running time in 2027, from the replay's hall load."""
    RP = G["RP"]
    ends = {r["run_id"]: A.dt.datetime.combine(r["ws"], A.dt.time(0)) + A.dt.timedelta(days=days[r["run_id"]]) for r in G["runs"]}
    xb = RP.hall_b(ends, "extend", phi)
    out = {}
    for r in G["runs"]:
        if r["hall"] != "B":
            continue
        a = int((A.dt.datetime.combine(r["ws"], A.dt.time(0)) - A.T27).total_seconds() // 300)
        b = int((ends[r["run_id"]] - A.T27).total_seconds() // 300)
        out[r["run_id"]] = float(np.mean(A.stretch(G["TH"], xb[a:b])) - 1.0)
    return out


def rival_runs(G, beta=None, lognormal=False, seed=None, normal_max=False):
    """The 2027 runs rebuilt under a rival construction of the step and the fill."""
    F, CM = G["F"], dict(G["CM"])
    if beta is not None:
        CM["beta"] = beta
    PK = A.Packer(F, seed=seed or 20271)
    if lognormal:
        by = {}
        rng = np.random.default_rng(99)
        for s, v in PK.by_src.items():
            lv = np.log(v)
            mu, sg = lv.mean(), lv.std()
            cap = v.max()
            by[s] = np.minimum(np.exp(rng.normal(mu, sg, 60000)), cap).astype(np.int64) + 1
        PK.by_src = by
    runs = A.runs_2027(F, PK, CM)
    if normal_max:
        for r in runs:
            S, Fl = PK.stream(r["mix"], r["C"], r["rule"])
            kf = r["L"] * r["d"] * r["C"] / r["N"]
            c = 1 + CM["beta"] * kf * S
            mu, sd = c.mean(), c.std()
            z = expected_max_normal(r["D"])
            r["emax"] = r["g"] * mu + math.sqrt(r["g"]) * sd * z
    return runs, CM


def expected_max_normal(n, sims=20000):
    rng = np.random.default_rng(5)
    return float(rng.standard_normal((sims // max(1, n // 64 + 1), n)).max(1).mean())


def replay_with(G, runs=None, CM=None, **kw):
    RP = A.Replay(G["F"], runs or G["runs"], CM or G["CM"], kw.pop("TH", G["TH"]), kw.pop("SM", G["SM"]),
                  kw.pop("WM", G["WM"]), kw.pop("PR", G["PR"]), G["launch_min"], contract=8100.0,
                  kw=kw.pop("kw", tuple(G["kwB"])), pen=kw.pop("pen", G["PEN"]["pen"]))
    return RP.run(**kw)


def pool_nodes(G, reserved, phi=True):
    """Hall B's nodes the research pool keeps busy while the reservations hold `reserved` of its 1,024."""
    PR, (c0, c1) = G["PR"], tuple(G["kwB"])
    ratio = (c0 + c1 * reserved) / 8100.0
    share = PR["plateau"] * float(np.interp(ratio, PR["cen"], PR["phi"])) if phi else PR["mean_share"]
    return (1024 - reserved) * share


def battery(G):
    """The defensible alternatives to every modelled choice in the hall B chain, each one pass of the whole golden
    with that choice changed: the late set and the largest change in any run's expected days."""
    out = []
    for name, opts in VARIANTS:
        G2 = A.golden(None, F=G["F"], **opts)
        dev = {k: G2["days"][k] / G["days"][k] - 1.0 for k in G["days"]}
        worst = max(dev, key=lambda k: abs(dev[k]))
        out.append(dict(name=name, late=A.late_set(G2, G2["days"]), days=G2["days"],
                        dev_pct=100 * dev[worst], worst=worst, dev={k: 100 * v for k, v in dev.items()},
                        pen=G2["PEN"]["pen"], th=(G2["TH"]["a1"], G2["TH"]["a2"])))
    return out


def build(G, mc_n=160):
    runs = {r["run_id"]: r for r in G["runs"]}
    W = {k: r["window_days"] for k, r in runs.items()}
    days = G["days"]
    gold_late = A.late_set(G, days)
    rng10_90 = A.mc_range(G, n=mc_n)
    b27 = A.bridge_2027(G)
    b26, per26 = A.bridge_2026(G)
    R, F26 = A.routes(G)
    st = stretch_runs(G, days)
    th = G["TH"]
    PEN, PR = G["PEN"], G["PR"]
    fig = {}
    fig["call_late_runs"] = gold_late
    fig["call_fitting_runs"] = sorted(k for k in runs if k not in gold_late)
    for k, r in runs.items():
        fig["days_%s" % k] = rnd(days[k], 1)
        fig["p10_%s" % k] = rnd(rng10_90[k][0], 1)
        fig["p90_%s" % k] = rnd(rng10_90[k][1], 1)
        fig["window_%s" % k] = W[k]
        fin = A.dt.datetime.combine(r["ws"], A.dt.time(0)) + A.dt.timedelta(days=days[k])
        fig["finish_%s" % k] = fin.strftime("%Y-%m-%d")
        fig["short_%s" % k] = rnd(days[k] - W[k], 1)
        for i, bk in enumerate(BRIDGE_KEYS):
            fig["bridge_%s_%d" % (k, i)] = rnd(b27[k][bk], 2)
        fig["bench_days_%s" % k] = rnd(b27[k]["benchmark days"], 1)
        fig["interrupt_days_%s" % k] = rnd(b27[k]["interruptions and restarts"], 2)
        fig["works_days_%s" % k] = rnd(b27[k]["provider works and the window's opening"], 2)
        fig["overhead_pct_%s" % k] = rnd(100 * (r["emax"] / r["emean"] - 1), 1)
        fig["fill_%s" % k] = rnd(r["fill"], 3)
    for k, v in st.items():
        fig["stretch_pct_%s" % k] = rnd(100 * v, 1)
    for x in (0.05, 0.10, 0.15, 0.20):
        fig["throttle_pct_x%02d" % int(x * 100)] = rnd(100 * (float(A.stretch(th, x)) - 1), 1)
    fig["beta"] = rnd(G["CM"]["beta"], 3)
    fig["joined_rank_steps"] = int(G["CM"]["rows"])
    fig["range_level_pct"] = 80
    fig["band"] = {"days_pct": 3, "range_pct": 5, "finish_days": 1, "bridge27_days": 0.35, "bridge27_pct": 12,
                   "b26_pct": 12, "b26_floor": 1500, "held_pct": 0.5, "beta": 0.03, "overhead_pts": 3,
                   "fill": 0.015, "stretch_pts": 2.5, "pod_pts": 2.5, "pool_nodes": 12, "pool_light": 0.03}
    fig["ovh_pct"] = rnd(100 * G["CM"]["ovh"], 1)
    fig["capped_days_2026"] = th["capped_days"]
    fig["xmax_2026"] = rnd(th["xmax"], 3)
    fig["works_ratio_major"] = rnd(G["WM"]["ratio"]["major"], 2)
    fig["works_ratio_routine"] = rnd(G["WM"]["ratio"]["routine"], 2)
    # the pod boundary and the pool's back-off, each read from 2026
    fig["pod_penalty_pct"] = rnd(100 * PEN["pen"], 1)
    fig["pod_runs_2026"] = sorted(k for k, v in G["flags"].items() if v)
    fig["pod_runs_2027"] = sorted(k for k, r in runs.items() if r["both"])
    fig["pod_block_names"] = sorted(runs[fig["pod_runs_2027"][0]]["rows"])   # the rows the roadmap's block column names for the one straddling block
    fig["pod_ratio_one"] = rnd(PEN["ratio_one"], 3)
    fig["pod_ratio_both"] = rnd(PEN["ratio_both"], 3)
    fig["pool_share"] = rnd(PR["plateau"], 3)
    fig["pool_share_mean"] = rnd(PR["mean_share"], 3)
    fig["pool_nodes_512"] = rnd(pool_nodes(G, 512), 0)
    fig["pool_nodes_800"] = rnd(pool_nodes(G, 800), 0)
    fig["pool_nodes_800_const"] = rnd(pool_nodes(G, 800, phi=False), 0)
    fig["draw_line"] = [rnd(G["kwB"][0], 0), rnd(G["kwB"][1], 2)]
    # the stated parameters of the pool figures: hall B's nodes, the two reserved loads asked about, the load from which
    # the measured pool is none (the first bin at zero, in nodes, to a row of 32) and the light-load definition's share
    zero_bins = PR["cen"][PR["phi"] <= 0.02]
    fig["hall_b_nodes"] = 1024
    fig["pool_levels"] = [512, 800]
    fig["pool_off_nodes"] = int(round(((zero_bins.min() * 8100.0 - G["kwB"][0]) / G["kwB"][1]) / 32.0) * 32)
    fig["light_load_pct"] = 88
    led = G["ledger"]
    fig["held_2026_total"] = rnd(led["gpu_days_held"].sum(), 0)
    for h in ("A", "B"):
        fig["held_2026_%s" % h] = rnd(led[led["hall"] == h]["gpu_days_held"].sum(), 0)
    for i, bk in enumerate(B26_KEYS):
        fig["b26_%d" % i] = rnd(b26[bk], 0)
    fig["f26_ratio"] = rnd(F26, 3)
    for name, d in R.items():
        fig["route_late__%s" % name] = A.late_set(G, d)
    bat = battery(G)
    fig["battery_worst_pct"] = rnd(max(abs(b["dev_pct"]) for b in bat), 2)
    fig["battery_n"] = len(bat)

    # ---------------- the effort test
    reflex_days = R["careful but hurried"]
    quick_days = R["quick: benchmark days"]
    late_c = A.late_set(G, reflex_days)
    E = {"results": [], "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    quick_held = float(led[led["finished_utc"].fillna("").astype(str) != ""]["gpu_days_held"].sum())
    E["results"].append(dict(id="R1", name="the GPU-days the 2026 runs held, all of 2026", graded_as="Ask 3",
                             figure="held_2026_total", depends=[], independent="the registry's launch and finish times",
                             golden=fig["held_2026_total"], band=[fig["held_2026_total"] * 0.995, fig["held_2026_total"] * 1.005],
                             partly=[fig["held_2026_total"] * 0.98, fig["held_2026_total"] * 1.02],
                             passes={"quick": rnd(quick_held, 0), "careful": fig["held_2026_total"], "thorough": fig["held_2026_total"]}))
    gold26 = {bk: fig["b26_%d" % i] for i, bk in enumerate(B26_KEYS)}
    bands26 = {bk: [v - max(0.12 * abs(v), 1500), v + max(0.12 * abs(v), 1500)] for bk, v in gold26.items()}
    bands26["GPU-days held"] = [gold26["GPU-days held"] * 0.995, gold26["GPU-days held"] * 1.005]
    bands26["benchmark GPU-days"] = [gold26["benchmark GPU-days"] * 0.99, gold26["benchmark GPU-days"] * 1.01]
    # the careful pass: every cause the runs read unprompted filed, the blocks across both pods left in the residual
    care26 = dict(gold26)
    care26["blocks across both pods"] = 0.0
    care26["other"] = rnd(gold26["other"] + gold26["blocks across both pods"], 0)
    fig["b26"] = gold26
    E["results"].append(dict(id="R2", name="the 2026 bridge from benchmark GPU-days to GPU-days held, by cause",
                             graded_as="Component 4", figure="b26", depends=["R1"], independent="2026's own records",
                             golden=gold26, bands=bands26, partly_share=0.6,
                             passes={"quick": None, "careful": care26, "thorough": gold26},
                             precedent=["N09", "L26"]))
    ov = {k: fig["overhead_pct_%s" % k] for k in LC_RUNS}
    fig["overhead_pct"] = ov
    E["results"].append(dict(id="R3", name="each long-context 2027 run's slowest-rank overhead over its mean rank, per cent",
                             graded_as="Ask 4", figure="overhead_pct", depends=[], independent="traces, manifests, the length sample",
                             golden=ov, bands={k: [v - 3.0, v + 3.0] for k, v in ov.items()},
                             passes={"quick": None, "careful": ov, "thorough": ov}))
    E["results"].append(dict(id="R4", name="kide-34b-sci's packing fill", graded_as="Ask 4", figure="fill_kide-34b-sci",
                             depends=[], independent="the length sample and the configs' packing rule",
                             golden=fig["fill_kide-34b-sci"], band=[fig["fill_kide-34b-sci"] - 0.015, fig["fill_kide-34b-sci"] + 0.015],
                             partly=[fig["fill_kide-34b-sci"] - 0.04, fig["fill_kide-34b-sci"] + 0.04],
                             passes={"quick": 1.0, "careful": fig["fill_kide-34b-sci"], "thorough": fig["fill_kide-34b-sci"]}))
    s5 = {k: fig["stretch_pct_%s" % k] for k in st}
    fig["stretch"] = s5
    st_c = stretch_runs(G, reflex_days, phi=False)
    E["results"].append(dict(id="R7", name="each hall B run's mean step stretch in 2027 from the hall held to its contract, per cent",
                             graded_as="Component 2", figure="stretch", depends=["R5", "R6"], independent="meter, node states, step logs, reservations",
                             golden=s5, bands={k: [v - 2.5, v + 2.5] for k, v in s5.items()}, partly_share=0.6,
                             passes={"quick": None, "careful": {k: rnd(100 * v, 1) for k, v in st_c.items()}, "thorough": s5},
                             precedent=["L15", "N28"]))
    fig["interrupt_days"] = {k: fig["interrupt_days_%s" % k] for k in runs}
    fig["works_days"] = {k: fig["works_days_%s" % k] for k in runs if fig["works_days_%s" % k] > 0.2}
    d8 = {k: fig["days_%s" % k] for k in runs}
    fig["days"] = d8
    E["results"].append(dict(id="R8", name="each 2027 run's expected days from its window's start", graded_as="Ask 1",
                             figure="days", depends=["R3", "R4", "R7", "R5", "R6"], independent="",
                             golden=d8, bands={k: [v * 0.97, v * 1.03] for k, v in d8.items()}, partly_share=0.6,
                             passes={"quick": {k: rnd(quick_days[k], 1) for k in runs},
                                     "careful": {k: rnd(reflex_days[k], 1) for k in runs}, "thorough": d8},
                             precedent=["N09", "L15", "L36"]))
    E["results"].append(dict(id="R9", name="the runs that will not finish inside their windows", graded_as="Recommendation",
                             figure="call_late_runs", depends=["R8"], independent="", golden=gold_late,
                             passes={"quick": A.late_set(G, quick_days), "careful": late_c, "thorough": gold_late},
                             precedent=["N09", "L15", "L36"]))
    E["results"].append(dict(id="R5", name="the extra time a step takes when a job's nodes lie in both of hall B's pods, per cent",
                             graded_as="Component 1", figure="pod_penalty_pct", depends=[], independent="the allocations, the step logs and the benchmark",
                             golden=fig["pod_penalty_pct"], band=[fig["pod_penalty_pct"] - 2.5, fig["pod_penalty_pct"] + 2.5],
                             partly=[fig["pod_penalty_pct"] - 6.0, fig["pod_penalty_pct"] + 6.0],
                             passes={"quick": 0.0, "careful": 0.0, "thorough": fig["pod_penalty_pct"]},
                             precedent=["N09", "N04"]))
    E["results"].append(dict(id="R6", name="hall B's nodes the research pool keeps busy while the reservations hold 800 of its 1,024",
                             graded_as="Component 3", figure="pool_nodes_800", depends=[], independent="node states, the registry and the meter",
                             golden=fig["pool_nodes_800"], band=[0.0, fig["band"]["pool_nodes"]],
                             partly=[0.0, 2 * fig["band"]["pool_nodes"] + 12],
                             passes={"quick": rnd(pool_nodes(G, 800, phi=False), 0), "careful": rnd(pool_nodes(G, 800, phi=False), 0),
                                     "thorough": fig["pool_nodes_800"]},
                             precedent=["L15", "N28"]))
    ws0 = {r["run_id"]: A.dt.datetime.combine(r["ws"], A.dt.time(0)) for r in G["runs"]}
    day_no = lambda k, d: rnd((ws0[k] + A.dt.timedelta(days=d) - A.T27).total_seconds() / 86400.0, 1)
    fin_g = {k: day_no(k, days[k]) for k in runs}
    fig["finish_day"] = fin_g
    E["results"].append(dict(id="R10", name="each 2027 run's finish, in days from 1 January 2027", graded_as="Ask 1",
                             figure="finish_day", depends=["R8"], independent="", golden=fin_g,
                             bands={k: [v - 1.0, v + 1.0] for k, v in fin_g.items()}, partly_share=0.6,
                             passes={"quick": {k: day_no(k, quick_days[k]) for k in runs},
                                     "careful": {k: day_no(k, reflex_days[k]) for k in runs}, "thorough": fin_g},
                             precedent=["N09", "L15"]))
    rg = {}
    for k in runs:
        rg["p10_%s" % k], rg["p90_%s" % k] = fig["p10_%s" % k], fig["p90_%s" % k]
    fig["range_ends"] = rg
    scale = {k: reflex_days[k] / days[k] for k in runs}
    E["results"].append(dict(id="R11", name="the 80 per cent range of each 2027 run's days", graded_as="Ask 1",
                             figure="range_ends", depends=["R8"], independent="", golden=rg,
                             bands={c: [v * 0.95, v * 1.05] for c, v in rg.items()}, partly_share=0.6,
                             passes={"quick": None,
                                     "careful": {c: rnd(v * scale[c.split("_", 1)[1]], 1) for c, v in rg.items()},
                                     "thorough": rg},
                             precedent=["N09", "L15"]))
    b27c = A.bridge_2027(G, over=dict(pod=False, phi=False))
    cells_g, cells_c, bands27 = {}, {}, {}
    for k in runs:
        for i, bk in enumerate(BRIDGE_KEYS):
            c = "%s|%s" % (k, bk)
            v = fig["bridge_%s_%d" % (k, i)]
            cells_g[c] = v
            cells_c[c] = rnd(b27c[k][bk], 2)
            bands27[c] = [v - max(0.35, 0.12 * abs(v)), v + max(0.35, 0.12 * abs(v))]
    fig["bridge27"] = cells_g
    E["results"].append(dict(id="R12", name="each 2027 run's bridge from its benchmark days to its expected days, cause by cause",
                             graded_as="Ask 2", figure="bridge27", depends=["R3", "R4", "R7", "R5", "R6"], independent="",
                             golden=cells_g, bands=bands27, partly_share=0.6,
                             passes={"quick": None, "careful": cells_c, "thorough": cells_g},
                             precedent=["N09", "L15"]))
    E["results"].sort(key=lambda x: int(x["id"][1:]))
    E["battery"] = [dict(name=b["name"], same=bool(b["late"] == gold_late), worst=b["worst"], dev_pct=rnd(b["dev_pct"], 2),
                         pod_penalty_pct=rnd(100 * b["pen"], 1), throttle=[rnd(b["th"][0], 3), rnd(b["th"][1], 3)])
                    for b in bat]
    E["hints"] = [
        {"sentence": "a job whose nodes sit in both of hall B's pods runs about a fifth slower than the benchmark's idle slice",
         "rescues": ["R5"]},
        {"sentence": "the research pool takes no hall B nodes once the reservations alone nearly fill the contract",
         "rescues": ["R6", "R7"]},
    ]
    E["routes"] = [{"name": "the golden", "answer": gold_late, "golden": True}] + \
        [{"name": name, "answer": A.late_set(G, d)} for name, d in R.items()]
    # ---------------- forcing: rivals on the golden's side, shortcuts across, perturbations holding
    fam = [{"name": b["name"], "answer": b["late"]} for b in bat]
    pr = G["CM"]["per_run"]
    bmin, bmax = min(v["beta"] for v in pr.values()), max(v["beta"] for v in pr.values())
    for name, kw in (("the attention coefficient at the lowest run's fit", dict(beta=bmin)),
                     ("the attention coefficient at the highest run's fit", dict(beta=bmax)),
                     ("lengths from a fitted lognormal per source", dict(lognormal=True)),
                     ("the slowest rank by a normal approximation", dict(normal_max=True))):
        rr, cm = rival_runs(G, **kw)
        fam.append({"name": name, "answer": A.late_set(dict(runs=rr), replay_with(G, runs=rr, CM=cm))})
    SMp = copy.deepcopy(G["SM"])
    tot = (SMp["hw_per_node_day"]["A"] + SMp["hw_per_node_day"]["B"]) / 2
    SMp["hw_per_node_day"] = {"A": tot, "B": tot}
    fam.append({"name": "hardware stops pooled over both halls", "answer": A.late_set(G, replay_with(G, SM=SMp))})
    pert = []
    for nm, kw in (("attention coefficient -20%", dict(beta=G["CM"]["beta"] * 0.8)),
                   ("attention coefficient +20%", dict(beta=G["CM"]["beta"] * 1.2))):
        rr, cm = rival_runs(G, **kw)
        pert.append({"input": nm, "answer": A.late_set(dict(runs=rr), replay_with(G, runs=rr, CM=cm))})
    for nm, f in (("throttle response -20%", 0.8), ("throttle response +20%", 1.2)):
        t2 = dict(G["TH"])
        t2["a1"], t2["a2"] = G["TH"]["a1"] * f, G["TH"]["a2"] * f
        if "xs" in t2:
            t2["ys"] = t2["ys"] * f
        pert.append({"input": nm, "answer": A.late_set(G, replay_with(G, TH=t2))})
    for nm, f in (("interruption rates -20%", 0.8), ("interruption rates +20%", 1.2)):
        s2 = copy.deepcopy(G["SM"])
        s2["hw_per_node_day"] = {h: v * f for h, v in s2["hw_per_node_day"].items()}
        s2["sw_per_wday"] *= f
        s2["fac_per_hall_day"] = {h: v * f for h, v in s2["fac_per_hall_day"].items()}
        pert.append({"input": nm, "answer": A.late_set(G, replay_with(G, SM=s2))})
    for nm, f in (("works overrun ratio -20%", 0.8), ("works overrun ratio +20%", 1.2)):
        w2 = dict(G["WM"])
        w2["ratio"] = {t: v * f for t, v in G["WM"]["ratio"].items()}
        pert.append({"input": nm, "answer": A.late_set(G, replay_with(G, WM=w2))})
    for nm, dlt in (("pod penalty -4 points", -0.04), ("pod penalty +4 points", 0.04)):
        pert.append({"input": nm, "answer": A.late_set(G, replay_with(G, pen=G["PEN"]["pen"] + dlt))})
    for nm, dlt in (("pool light-load share -0.10", -0.10), ("pool light-load share +0.10", 0.10)):
        pr2 = dict(G["PR"])
        pr2["plateau"] = G["PR"]["plateau"] + dlt
        pert.append({"input": nm, "answer": A.late_set(G, replay_with(G, PR=pr2))})
    for nm, f in (("draw line slope -1%", 0.99), ("draw line slope +1%", 1.01)):
        k2 = (G["kwB"][0], G["kwB"][1] * f)
        pert.append({"input": nm, "answer": A.late_set(G, replay_with(G, kw=k2))})
    E["forcing"] = {"kind": "set", "line": "each run's reserved window (expected finish against the window's end)",
                    "golden_answer": gold_late, "golden_family": fam,
                    "shortcuts": [{"name": n, "answer": A.late_set(G, d)} for n, d in R.items()
                                  if n in ("quick: benchmark days", "careful but hurried", "the full-context FLOPs formula",
                                           "the 2026 benchmark-to-held ratio", "drop P (no pod penalty)",
                                           "drop Q (the pool at its mean share)",
                                           "direct: the nearest 2026 run's realised rate")],
                    "perturbations": pert}
    E["factorial"] = {
        "golden_answer": gold_late,
        "reflex_route": {"answer": late_c},
        "judgments": [
            {"id": "P", "name": "a job with nodes in both of hall B's pods pays for the boundary at every step, which the benchmark's "
                              "slice in one pod cannot show", "kind": "stump", "precedent": ["N09", "N04"],
             "hurried": "every job's step as the benchmark and the cost model give it",
             "dropped": {"answer": fig["route_late__drop P (no pod penalty)"], "results_moved": ["R2", "R7", "R8", "R9", "R5", "R10", "R11", "R12"]},
             "alone": {"answer": fig["route_late__fix P alone"], "results_rescued": ["R5"]}},
            {"id": "Q", "name": "the research pool backs off as the reservations near the contract, so hall B's free nodes add no load "
                              "from the load at which it stops", "kind": "stump", "precedent": ["L15", "N28"],
             "hurried": "the pool at its 2026 mean share of the free nodes",
             "dropped": {"answer": fig["route_late__drop Q (the pool at its mean share)"], "results_moved": ["R7", "R8", "R9", "R6", "R10", "R11", "R12"]},
             "alone": {"answer": fig["route_late__fix Q alone"], "results_rescued": ["R6"]}},
            {"id": "S1", "name": "each step waits for the slowest data-parallel rank, its load quadratic in its documents' lengths",
             "kind": "reflex", "precedent": ["R84"]},
            {"id": "S18", "name": "best-fit packing pads the scientific mix's sequences", "kind": "reflex", "precedent": ["R85"]},
            {"id": "S3", "name": "hall B held to its contracted load, the excess rebuilt from the node states", "kind": "reflex",
             "precedent": ["R86"]},
            {"id": "S4", "name": "provider works at the 2025-26 overrun record", "kind": "reflex", "precedent": ["R88"]},
            {"id": "J5", "name": "interruptions and restarts priced from the 2026 log", "kind": "reflex", "precedent": ["R87"]},
            {"id": "J6", "name": "each run's benchmark days and the 2026 GPU-days held reproduced", "kind": "reflex", "precedent": ["R90"]},
            {"id": "J7", "name": "a block extended to its run's finish, its next reservation waiting for the nodes", "kind": "reflex",
             "precedent": ["R89"]},
        ]}
    return fig, E, dict(b27=b27, b26=b26, per26=per26, R=R, F26=F26, rng=rng10_90, stretch=st, bat=bat, b27c=b27c,
                        stretch_c=st_c)
