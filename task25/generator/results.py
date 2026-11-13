"""figures.json and effort.json from the golden and the routes, all computed on the cut pack."""
import copy
import json
import math

import numpy as np

import analysis as A

LC_RUNS = ("kide-13b-code-lc32", "kide-34b-lc64", "kide-8b-lc64", "kide-13b-lc32", "kide-34b-sci")
BRIDGE_KEYS = ["benchmark days", "the run's own mix at the mean rank", "waiting for the slowest rank",
               "padding in packed sequences", "hall B held to its contracted load", "interruptions and restarts",
               "provider works and the window's opening", "expected days"]
B26_KEYS = ["benchmark GPU-days", "the runs' own mixes at the mean rank", "waiting for the slowest rank",
            "padding in packed sequences", "hall B held to its contracted load", "hall A row 6 cooling fault",
            "interruptions and restarts", "provider works", "other", "GPU-days held"]


def rnd(x, d=1):
    return float(round(float(x), d))


def stretch_runs(G, days):
    """Each hall B run's mean step stretch over its running time in 2027, from the replay's hall load."""
    RP = G["RP"]
    ends = {r["run_id"]: A.dt.datetime.combine(r["ws"], A.dt.time(0)) + A.dt.timedelta(days=days[r["run_id"]]) for r in G["runs"]}
    xb = RP.hall_b(ends, G["pool"])
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
                  kw.pop("WM", G["WM"]), kw.pop("pool", G["pool"]), G["launch_min"], contract=8100.0,
                  kw=tuple(G["kwB"]))
    return RP.run(**kw)


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
        fig["throttle_pct_x%02d" % int(x * 100)] = rnd(100 * (A.stretch(th, x) - 1), 1)
    fig["beta"] = rnd(G["CM"]["beta"], 3)
    fig["joined_rank_steps"] = int(G["CM"]["rows"])
    fig["range_level_pct"] = 80
    fig["band"] = {"days_pct": 3, "range_pct": 5, "finish_days": 1, "bridge27_days": 0.35, "bridge27_pct": 12,
                   "b26_pct": 12, "b26_floor": 1500, "held_pct": 0.5, "beta": 0.03, "overhead_pts": 3,
                   "fill": 0.015, "stretch_pts": 2.5}
    fig["ovh_pct"] = rnd(100 * G["CM"]["ovh"], 1)
    fig["capped_days_2026"] = th["capped_days"]
    fig["xmax_2026"] = rnd(th["xmax"], 3)
    fig["pool_share"] = rnd(G["pool"], 3)
    fig["works_ratio_major"] = rnd(G["WM"]["ratio"]["major"], 2)
    fig["works_ratio_routine"] = rnd(G["WM"]["ratio"]["routine"], 2)
    led = G["ledger"]
    fig["held_2026_total"] = rnd(led["gpu_days_held"].sum(), 0)
    for h in ("A", "B"):
        fig["held_2026_%s" % h] = rnd(led[led["hall"] == h]["gpu_days_held"].sum(), 0)
    for i, bk in enumerate(B26_KEYS):
        fig["b26_%d" % i] = rnd(b26[bk], 0)
    fig["f26_ratio"] = rnd(F26, 3)
    for name, d in R.items():
        fig["route_late__%s" % name] = A.late_set(G, d)

    # ---------------- the effort test
    def table(fn, keys):
        return {k: fn(k) for k in keys}

    late_c = A.late_set(G, R["careful but hurried"])
    careful_days = R["careful but hurried"]
    quick_days = R["quick: benchmark days"]
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
    # the careful pass: the measured steady step's gap to the benchmark filed as one item, the cap left in the residual
    steady_gap = 0.0
    for rid, p in per26.items():
        steady_gap += p["mix"] + p["slow"] + p["pad"]
    care26 = dict(gold26)
    care26["the runs' own mixes at the mean rank"] = rnd(steady_gap, 0)
    care26["waiting for the slowest rank"] = 0.0
    care26["padding in packed sequences"] = 0.0
    care26["hall B held to its contracted load"] = 0.0
    care26["other"] = rnd(gold26["other"] + gold26["hall B held to its contracted load"], 0)
    fig["b26"] = gold26
    E["results"].append(dict(id="R2", name="the 2026 bridge from benchmark GPU-days to GPU-days held, by cause",
                             graded_as="Component 4", figure="b26", depends=["R1"], independent="2026's own records",
                             golden=gold26, bands=bands26, partly_share=0.6,
                             passes={"quick": None, "careful": care26, "thorough": gold26},
                             precedent=["L26", "L32"]))
    ov = {k: fig["overhead_pct_%s" % k] for k in LC_RUNS}
    fig["overhead_pct"] = ov
    E["results"].append(dict(id="R3", name="each long-context 2027 run's slowest-rank overhead over its mean rank, per cent",
                             graded_as="Component 1", figure="overhead_pct", depends=[], independent="traces, manifests, the length sample",
                             golden=ov, bands={k: [v - 3.0, v + 3.0] for k, v in ov.items()},
                             passes={"quick": None, "careful": {k: 0.0 for k in ov}, "thorough": ov},
                             precedent=["N04", "L22", "L26", "L36"]))
    E["results"].append(dict(id="R4", name="kide-34b-sci's packing fill", graded_as="Component 2", figure="fill_kide-34b-sci",
                             depends=[], independent="the length sample and the configs' packing rule",
                             golden=fig["fill_kide-34b-sci"], band=[fig["fill_kide-34b-sci"] - 0.015, fig["fill_kide-34b-sci"] + 0.015],
                             partly=[fig["fill_kide-34b-sci"] - 0.04, fig["fill_kide-34b-sci"] + 0.04],
                             passes={"quick": 1.0, "careful": 1.0, "thorough": fig["fill_kide-34b-sci"]},
                             precedent=["N04", "L36"]))
    s5 = {k: fig["stretch_pct_%s" % k] for k in st}
    fig["stretch"] = s5
    E["results"].append(dict(id="R5", name="each hall B run's mean step stretch in 2027 from the hall held to its contract, per cent",
                             graded_as="Component 3", figure="stretch", depends=[], independent="meter, node states, step logs, reservations",
                             golden=s5, bands={k: [v - 2.5, v + 2.5] for k, v in s5.items()},
                             passes={"quick": None, "careful": {k: 0.0 for k in s5}, "thorough": s5},
                             precedent=["L38", "L15", "L01"]))
    i6 = {k: fig["interrupt_days_%s" % k] for k in runs}
    fig["interrupt_days"] = i6
    E["results"].append(dict(id="R6", name="days each 2027 run loses to interruptions and restarts", graded_as="Ask 2",
                             figure="interrupt_days", depends=[], independent="the interruption log",
                             golden=i6, bands={k: [v * 0.75 - 0.05, v * 1.25 + 0.05] for k, v in i6.items()},
                             passes={"quick": {k: 0.0 for k in i6}, "careful": i6, "thorough": i6}))
    w7 = {k: fig["works_days_%s" % k] for k in runs if fig["works_days_%s" % k] > 0.2}
    fig["works_days"] = w7
    care_w = {}
    for k in w7:
        cw = replay_with(G, s1=True, s18=True, s3=True, works_ratio=False)[k] - replay_with(G, s1=True, s18=True, s3=True, works_on=False, launch=False)[k]
        care_w[k] = rnd(cw, 2)
    E["results"].append(dict(id="R7", name="days each 2027 window that holds provider works loses to them", graded_as="Ask 2",
                             figure="works_days", depends=[], independent="work orders and the 2027 notice",
                             golden=w7, bands={k: [v - 0.35, v + 0.35] for k, v in w7.items()},
                             passes={"quick": {k: 0.0 for k in w7}, "careful": care_w, "thorough": w7},
                             precedent=["N22", "N03", "L46"]))
    d8 = {k: fig["days_%s" % k] for k in runs}
    fig["days"] = d8
    E["results"].append(dict(id="R8", name="each 2027 run's expected days from its window's start", graded_as="Ask 1",
                             figure="days", depends=["R3", "R4", "R5", "R6", "R7"], independent="",
                             golden=d8, bands={k: [v * 0.97, v * 1.03] for k, v in d8.items()}, partly_share=0.6,
                             passes={"quick": {k: rnd(quick_days[k], 1) for k in runs},
                                     "careful": {k: rnd(careful_days[k], 1) for k in runs}, "thorough": d8},
                             precedent=["N04", "L38", "L36"]))
    E["results"].append(dict(id="R9", name="the runs that will not finish inside their windows", graded_as="Recommendation",
                             figure="call_late_runs", depends=["R8"], independent="", golden=gold_late,
                             passes={"quick": A.late_set(G, quick_days), "careful": late_c, "thorough": gold_late},
                             precedent=["N04", "L38", "L36"]))
    E["hints"] = [
        {"sentence": "each step waits for the data-parallel rank whose sequences hold the long documents", "rescues": ["R3"]},
        {"sentence": "the scientific run's best-fit packing leaves part of every sequence as padding", "rescues": ["R4"]},
        {"sentence": "hall B's meter sits at its contract on the days the hall wanted more, and every job there ran slower", "rescues": ["R5"]},
        {"sentence": "major works ran about twice their planned hours in 2025 and 2026", "rescues": ["R7"]},
    ]
    E["routes"] = [{"name": "the golden", "answer": gold_late, "golden": True}] + \
        [{"name": name, "answer": A.late_set(G, d)} for name, d in R.items()]
    # ---------------- forcing: rivals on the golden's side, shortcuts across, perturbations holding
    fam = []
    pr = G["CM"]["per_run"]
    bmin, bmax = min(v["beta"] for v in pr.values()), max(v["beta"] for v in pr.values())
    for name, kw in (("the attention coefficient at the lowest run's fit", dict(beta=bmin)),
                     ("the attention coefficient at the highest run's fit", dict(beta=bmax)),
                     ("lengths from a fitted lognormal per source", dict(lognormal=True)),
                     ("another packing and dealing seed", dict(seed=777)),
                     ("the slowest rank by a normal approximation", dict(normal_max=True))):
        rr, cm = rival_runs(G, **kw)
        fam.append({"name": name, "answer": A.late_set(dict(runs=rr), replay_with(G, runs=rr, CM=cm))})
    lin = dict(G["TH"])
    b = G["S"]
    reg = G["F"]["reg"].set_index("run_id")
    cb = b[(b["run_id"].map(reg["hall"]) == "B") & (b["x"] > 0)].copy()
    cb["stretch"] = cb["step_time_ms"] / cb["run_id"].map(G["steady"]) - 1.0
    cb = cb[np.isfinite(cb["stretch"])]
    lin = {"a1": float((cb["x"] * cb["stretch"]).sum() / (cb["x"] ** 2).sum()), "a2": 0.0}
    fam.append({"name": "the throttle as a straight line in the excess", "answer": A.late_set(G, replay_with(G, TH=lin))})
    med = dict(G["WM"])
    med["ratio"] = G["WM"]["rows"].groupby("work_type")["ratio"].median().to_dict()
    fam.append({"name": "works at the median overrun ratio", "answer": A.late_set(G, replay_with(G, WM=med))})
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
        t2 = {"a1": G["TH"]["a1"] * f, "a2": G["TH"]["a2"] * f}
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
    for nm, dlt in (("pool busy share -0.1", -0.1), ("pool busy share +0.1", 0.1)):
        pert.append({"input": nm, "answer": A.late_set(G, replay_with(G, pool=min(1.0, max(0.0, G["pool"] + dlt))))})
    E["forcing"] = {"kind": "set", "line": "each run's reserved window (expected finish against the window's end)",
                    "golden_answer": gold_late, "golden_family": fam,
                    "shortcuts": [{"name": n, "answer": A.late_set(G, d)} for n, d in R.items()
                                  if n in ("quick: benchmark days", "careful but hurried", "the full-context FLOPs formula",
                                           "the 2026 benchmark-to-held ratio")],
                    "perturbations": pert}
    E["factorial"] = {
        "golden_answer": gold_late,
        "reflex_route": {"answer": late_c},
        "judgments": [
            {"id": "S1", "name": "each step waits for the slowest data-parallel rank, its load quadratic in its documents' lengths",
             "kind": "stump", "precedent": ["N04", "L22", "L26", "L36"], "hurried": "each rank at its mean cost",
             "dropped": {"answer": fig["route_late__drop S1 (the mean rank)"], "results_moved": ["R3", "R8", "R9"]},
             "alone": {"answer": fig["route_late__fix S1 alone"], "results_rescued": ["R3"]}},
            {"id": "S18", "name": "best-fit packing pads the scientific mix's sequences", "kind": "stump",
             "precedent": ["N04", "L36"], "hurried": "every sequence full",
             "dropped": {"answer": fig["route_late__drop S18 (full sequences)"], "results_moved": ["R4", "R8", "R9"]},
             "alone": {"answer": fig["route_late__fix S18 alone"], "results_rescued": ["R4"]}},
            {"id": "S3", "name": "hall B held to its contracted load through February to April, every job's step stretched",
             "kind": "stump", "precedent": ["L38", "L15", "L01"], "hurried": "each run's throughput its own",
             "dropped": {"answer": fig["route_late__drop S3 (no throttle)"], "results_moved": ["R5", "R8", "R9"]},
             "alone": {"answer": fig["route_late__fix S3 alone"], "results_rescued": ["R5"]}},
            {"id": "S4", "name": "provider works at the 2025-26 overrun record", "kind": "stump", "precedent": ["N22", "N03", "L46"],
             "hurried": "the notice's planned hours",
             "dropped": {"answer": fig["route_late__drop S4 (planned works hours)"], "results_moved": ["R7"]},
             "alone": {"answer": fig["route_late__fix S4 alone"], "results_rescued": ["R7"]}},
            {"id": "J5", "name": "interruptions and restarts priced from the 2026 log", "kind": "reflex", "precedent": ["R07", "R30"]},
            {"id": "J6", "name": "each run's benchmark days and its own mix's mean attention", "kind": "reflex", "precedent": ["R18", "R40"]},
        ]}
    return fig, E, dict(b27=b27, b26=b26, per26=per26, R=R, F26=F26, rng=rng10_90, stretch=st)
