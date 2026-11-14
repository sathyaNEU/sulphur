"""The golden analysis, read from target/ alone (nothing from the simulation): the 2026 ledger and its bridge from
benchmark to held GPU-days, the per-rank cost model, the hall B throttle, interruptions and works, and each H1 2027
run's days replayed from its benchmark cause by cause. The routes (each hurried method) reuse these pieces with one
judgment switched."""
import datetime as dt
import json
import math
import os
import re

import numpy as np
import pandas as pd
import yaml
from openpyxl import load_workbook

import world as W   # the two packing rules exactly as the configs file them, and node-list expansion

REVIEW_END = dt.datetime(2026, 11, 1)
T27 = dt.datetime(2027, 1, 1)
GRID = 300


# ------------------------------------------------------------------ loading
def load(T):
    F = {}
    rd = lambda p: pd.read_csv(os.path.join(T, p))
    F["reg"] = rd("runs/run_registry_2026.csv")
    F["steps"] = rd("runs/step_log_2026.csv")
    F["stops"] = rd("runs/interruptions_2026.csv")
    F["alloc"] = rd("runs/node_allocations_2026.csv")
    F["samples"] = rd("profiling/rank_step_samples_2026.csv")
    with open(os.path.join(T, "profiling/packing_manifests_2026.jsonl")) as fh:
        F["man"] = [json.loads(l) for l in fh if l.strip()]
    F["states"] = rd("cluster/node_states_2026.csv")
    F["meter"] = rd("provider/hall_it_load_2026.csv")
    F["works"] = rd("provider/work_orders_2025_2026.csv")
    F["incidents"] = rd("provider/incident_log_2026.csv")
    F["bench"] = rd("benchmark/tpbench_results.csv")
    with open(os.path.join(T, "benchmark/tpbench_harness.yaml")) as fh:
        F["harness"] = yaml.safe_load(fh)
    F["lengths"] = rd("data/doc_length_sample.csv")
    F["mixes"] = rd("data/data_mixes.csv")
    wb = load_workbook(os.path.join(T, "plan_2027/roadmap_h1_2027.xlsx"), data_only=True)
    ws = wb["H1 2027 runs"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = list(rows[2])
    F["roadmap"] = pd.DataFrame([r for r in rows[3:] if r[0]], columns=hdr)
    F["configs"] = {}
    for f in sorted(os.listdir(os.path.join(T, "plan_2027/configs"))):
        with open(os.path.join(T, "plan_2027/configs", f)) as fh:
            F["configs"][f[:-5]] = yaml.safe_load(fh)
    F["notice"] = works_notice_rows(T)
    return unify_ids(F)


def works_notice_rows(T):
    """The provider's 2027 notice, read back from its PDF table."""
    from pypdf import PdfReader
    txt = "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(T, "provider/planned_works_h1_2027.pdf")).pages)
    out = []
    import re
    for m in re.finditer(r"(PV-27-\d{3})\s+HALL-([AB])\s+(major|routine)\s+(\d\d\.\d\d\.\d{4} \d\d:\d\d)\s+(\d+)\s+(.+)", txt):
        out.append(dict(work_order=m.group(1), hall=m.group(2), work_type=m.group(3),
                        start_local=dt.datetime.strptime(m.group(4), "%d.%m.%Y %H:%M"), planned_hours=float(m.group(5)),
                        title=m.group(6).strip()))
    return pd.DataFrame(out)


def id_map(F):
    prev = {}
    for r in F["reg"].itertuples():
        if isinstance(r.previous_ids, str) and r.previous_ids:
            for p in r.previous_ids.split(";"):
                prev[p.strip()] = r.run_id
    return prev


def unify_ids(F):
    """Renamed runs: every file is mapped to the registry's current ID through its previous IDs."""
    prev = id_map(F)
    for k in ("steps", "stops", "alloc", "samples"):
        F[k]["run_id"] = F[k]["run_id"].map(lambda x: prev.get(x, x))
    for m in F["man"]:
        m["run_id"] = prev.get(m["run_id"], m["run_id"])
    return F


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def helsinki_offset(u):
    y = u.year

    def last_sunday(month):
        d = dt.datetime(y, month, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d.replace(hour=1)

    return 3 if last_sunday(3) <= u < last_sunday(10) else 2


def meter_utc(col):
    """Helsinki local readings to UTC; the hour repeated when clocks go back is read in file order, the first pass
    in summer time and the second in winter time."""
    lt = [dt.datetime.strptime(v, "%Y-%m-%d %H:%M") for v in col]
    seen = set()
    out = []
    for t in lt:
        if t in seen:
            out.append(t - dt.timedelta(hours=2))
        else:
            seen.add(t)
            out.append(local_to_utc(t))
    return out


def local_to_utc(t):
    for off in (3, 2):
        u = t - dt.timedelta(hours=off)
        if helsinki_offset(u) == off:
            return u
    return t - dt.timedelta(hours=2)


# ------------------------------------------------------------------ the step log, cleaned
def clean_steps(F):
    s = F["steps"].drop_duplicates().copy()
    prev = {}
    for r in F["reg"].itertuples():
        if isinstance(r.previous_ids, str) and r.previous_ids:
            for p in r.previous_ids.split(";"):
                prev[p.strip()] = r.run_id
    s["run_id"] = s["run_id"].map(lambda x: prev.get(x, x))
    s["t"] = pd.to_datetime(s["ts_utc"], format="%Y-%m-%dT%H:%M:%SZ")
    s = s.sort_values(["run_id", "t"], kind="mergesort").reset_index(drop=True)
    s["prev_max_tokens"] = s.groupby("run_id")["tokens_seen"].cummax().shift(1)
    s.loc[s["run_id"] != s["run_id"].shift(1), "prev_max_tokens"] = -1
    s["replay"] = s["tokens_seen"] <= s["prev_max_tokens"]
    return s


# ------------------------------------------------------------------ R1: the 2026 ledger
def ledger(F):
    reg = F["reg"].copy()
    reg["launch"] = reg["launched_utc"].map(ts)
    reg["finish"] = reg["finished_utc"].map(lambda v: ts(v) if isinstance(v, str) and v else REVIEW_END)
    reg["finish"] = reg["finish"].map(lambda v: min(v, REVIEW_END))
    reg["gpu_days_held"] = reg["nodes"] * 8 * (reg["finish"] - reg["launch"]).dt.total_seconds() / 86400
    return reg


# ------------------------------------------------------------------ hall B: would-be draw and excess
def hall_excess(F, hall="B", contract=None, clear_kw=40.0, min_alloc=0):
    """The meter reads the contract when the hall is held to it, so the excess is rebuilt from the scheduler's node
    states: the hall's draw as a straight line in its allocated nodes (every node left idle or down draws the same,
    so the line is the whole of it), fitted on the intervals the meter was clear of the contract and applied to every
    interval."""
    m = F["meter"][F["meter"]["hall"] == "HALL-%s" % hall].copy().reset_index(drop=True)
    m["t"] = meter_utc(m["timestamp_local"])
    st = F["states"][F["states"]["hall"] == hall].copy()
    st["t"] = pd.to_datetime(st["ts_utc"], format="%Y-%m-%dT%H:%M:%SZ")
    j = st.merge(m[["t", "it_load_kw"]], on="t", how="left")
    contract = contract or float(j["it_load_kw"].quantile(0.999))
    clear = j["it_load_kw"].notna() & (j["it_load_kw"] < contract - clear_kw) & (j["allocated"] >= min_alloc)
    X = np.c_[np.ones(clear.sum()), j.loc[clear, "allocated"]]
    coef, *_ = np.linalg.lstsq(X, j.loc[clear, "it_load_kw"].values, rcond=None)
    j["would_be_kw"] = coef[0] + coef[1] * j["allocated"]
    j["x"] = np.maximum(0.0, j["would_be_kw"] / contract - 1.0)
    return j[["t", "allocated", "idle", "down", "it_load_kw", "would_be_kw", "x"]], coef, contract


def contract_kw(hall):
    """Contracted IT capacity from the provider's service schedule (Service Schedule S-3)."""
    return {"A": 6600.0, "B": 8100.0}[hall]


# ------------------------------------------------------------------ the length sample and the packing replay
HARNESS_TOKENS = 1.2e10     # tokens of the benchmark corpus the golden replays
HARNESS_STREAMS = {}        # shared by every golden call of a process: a stream depends on its seed, context and corpus only


class Packer:
    def __init__(self, F, seed=20271):
        self.by_src = {s: g["length_tokens"].values.astype(np.int64) for s, g in F["lengths"].groupby("source")}
        self.mix = {m: dict(zip(g["source"], g["token_share"])) for m, g in F["mixes"].groupby("mix_id")}
        self.seed = seed
        self.cache = {}

    def stream(self, mix, C, rule, ntok=None):
        key = (mix, C, rule)
        if key not in self.cache:
            rng = np.random.default_rng(self.seed + C + len(mix))
            ntok = ntok or (6.0e8 if C >= 32768 else 3.0e8)
            docs = W.docs_from_sample(self.by_src, self.mix[mix], ntok, rng)
            S, Fl, _ = W.pack(docs, C, rule)
            self.cache[key] = (S, Fl)
        return self.cache[key]

    def harness(self, F, C):
        """The benchmark corpus replayed at a length where its slowest-rank cost has converged: the harness file files
        the corpus by its length distribution only, so every analyst draws their own stream, and a stream of 3e8 tokens
        moves the 64k-context runs' days by 1.5 to 2 per cent (sd) from one seed to the next. The golden is the converged
        value (0.2 per cent at 1.2e10 tokens); the answer blocks' bands carry the spread of an ordinary stream."""
        h = F["harness"]["corpus"]["doc_length"]
        med, sig, cap = h["median_tokens"], h["sigma"], h["max_tokens"]
        key = (self.seed, C, med, sig, cap)
        if key not in HARNESS_STREAMS:
            rng = np.random.default_rng(self.seed + 7 + C)
            docs = W.draw_docs({"x": 1.0}, HARNESS_TOKENS, rng, sources={"x": (med, sig, cap)})
            S, Fl, _ = W.pack(docs, C, "sequential")
            HARNESS_STREAMS[key] = (S, Fl)
        return HARNESS_STREAMS[key]


def step_units(S, kf, beta, D, g, seed, steps=3000):
    """Expected slowest-rank and mean-rank compute of a step, in units of one sequence's dense time."""
    rng = np.random.default_rng(seed)
    cost = 1.0 + beta * kf * S
    n = len(cost)
    mx = np.empty(steps)
    for i in range(steps):
        idx = rng.integers(0, n, size=(D, g))
        mx[i] = cost[idx].sum(1).max()
    return float(mx.mean()), float(g * cost.mean())


# ------------------------------------------------------------------ R3 part 1: the per-rank cost model
def cost_model(F, excess_B):
    """Join the profiler's per-rank samples to the loader's manifests (run, step, rank): a rank's forward and
    backward time against its sequences' dense count and their attention, sum over sequences of (L d C / N) times
    the sum of squared document lengths over C squared. Capped hall B intervals and row 6's nodes during its cooling
    fault are left out."""
    reg = F["reg"].set_index("run_id")
    man = pd.DataFrame([dict(run_id=m["run_id"], step=m["step"], dp_rank=m["dp_rank"], C=m["seq_len"],
                             g=len(m["docs"]), Ssum=sum(sum(d * d for d in seq) for seq in m["docs"]) / m["seq_len"] ** 2)
                        for m in F["man"]])
    smp = F["samples"].merge(man, on=["run_id", "step", "dp_rank"], how="inner")
    smp["t"] = pd.to_datetime(smp["ts_utc"], format="%Y-%m-%dT%H:%M:%SZ")
    fault = [r for r in F["incidents"].itertuples() if "CRAC-6 compressor fault" in r.summary]
    f0 = local_to_utc(dt.datetime.strptime(fault[0].opened_local, "%d.%m.%Y %H:%M"))
    f1 = local_to_utc(dt.datetime.strptime(fault[0].closed_local, "%d.%m.%Y %H:%M"))
    row6 = smp["node"].str.contains("-r06-") & (smp["t"] >= f0) & (smp["t"] < f1)
    xb = excess_B.set_index("t")["x"]
    smp["tg"] = smp["t"].dt.floor("5min")
    smp["x"] = smp["tg"].map(xb).fillna(0.0)
    hallB = smp["run_id"].map(reg["hall"]) == "B"
    keep = ~row6 & ~(hallB & (smp["x"] > 0))
    smp = smp[keep].copy()
    out = {}
    for rid, g in smp.groupby("run_id"):
        L, d, N = reg.loc[rid, "layers"], reg.loc[rid, "d_model"], reg.loc[rid, "params_b"] * 1e9
        kf = L * d * g["C"].iloc[0] / N
        X = np.c_[g["g"].values, kf * g["Ssum"].values]
        coef, *_ = np.linalg.lstsq(X, g["fwd_bwd_ms"].values, rcond=None)
        pred = X @ coef
        r2 = 1 - ((g["fwd_bwd_ms"] - pred) ** 2).sum() / ((g["fwd_bwd_ms"] - g["fwd_bwd_ms"].mean()) ** 2).sum()
        out[rid] = dict(c0=coef[0], beta=coef[1] / coef[0], n=len(g), r2=float(r2))
    betas = np.array([v["beta"] for v in out.values()])
    w = np.array([v["n"] for v in out.values()], float)
    beta = float((betas * w).sum() / w.sum())
    # step overhead beyond the slowest rank: the optimizer step against the slowest rank's compute
    allsmp = F["samples"].groupby(["run_id", "step"]).agg(mx=("fwd_bwd_ms", "max"), opt=("optimizer_ms", "mean"))
    ovh = float((allsmp["opt"] / allsmp["mx"]).median())
    return dict(beta=beta, per_run=out, ovh=ovh, rows=int(len(smp)), row6_window=(f0, f1))


def bench_row(F, model, C, g, hall):
    b = F["bench"]
    r = b[(b["model"] == model) & (b["context_tokens"] == C) & (b["seqs_per_rank"] == g) & (b["hall"] == hall)]
    assert len(r) == 1, (model, C, g, hall)
    return r.iloc[0]


def dense_ms(F, PK, CM, model, L, d, N, C, g, hall):
    """One sequence's dense time on a rank, from the benchmark: its step over the harness corpus's slowest rank."""
    b = bench_row(F, model, C, g, hall)
    bench_step_ms = g * C / (8.0 * b["tokens_per_gpu_s"]) * 1000.0
    S, _ = PK.harness(F, C)
    kf = L * d * C / N
    emax_b, emean_b = step_units(S, kf, CM["beta"], 64, g, seed=int(C + g))
    return bench_step_ms / (emax_b * (1 + CM["ovh"])), emax_b, emean_b, float(b["tokens_per_gpu_s"])


def predicted_steps(F, PK, CM):
    """Each 2026 run's step from its benchmark and the cost model at its own mix, width and sequences per rank:
    the slowest rank and the mean rank (ms), its fill, and the dense time per sequence."""
    out = {}
    for r in F["reg"].itertuples():
        N, L, d = r.params_b * 1e9, int(r.layers), int(r.d_model)
        a_ms, emax_b, emean_b, tps = dense_ms(F, PK, CM, r.model, L, d, N, int(r.context_tokens), int(r.seqs_per_rank), r.hall)
        S, Fl = PK.stream(r.data_mix, int(r.context_tokens), r.packing)
        kf = L * d * r.context_tokens / N
        emax, emean = step_units(S, kf, CM["beta"], int(r.nodes), int(r.seqs_per_rank), seed=int(r.nodes * 7 + r.seqs_per_rank + r.context_tokens))
        out[r.run_id] = dict(a_ms=a_ms, emax_b=emax_b, emean_b=emean_b, tps=tps, emax=emax, emean=emean,
                             fill=float(Fl.mean()), step_max_ms=a_ms * emax * (1 + CM["ovh"]),
                             step_mean_ms=a_ms * emean * (1 + CM["ovh"]), bench_step_ms=a_ms * emax_b * (1 + CM["ovh"]))
    return out


# ------------------------------------------------------------------ R5: the throttle response
def steady_steps(F, S, excess_B, CM):
    """Each 2026 run's steady step time: the median logged step over intervals clear of a capped hall and of row
    6's cooling fault."""
    reg = F["reg"].set_index("run_id")
    xb = excess_B.set_index("t")["x"]
    S = S.copy()
    S["tg"] = S["t"].dt.floor("5min")
    S["x"] = np.where(S["run_id"].map(reg["hall"]) == "B", S["tg"].map(xb).fillna(0.0), 0.0)
    row6_runs = set()
    for r in F["alloc"].itertuples():
        if "ka-r06-" in r.nodes:
            row6_runs.add(r.run_id)
    f0, f1 = CM["row6_window"]
    S["row6"] = S["run_id"].isin(row6_runs) & (S["t"] >= f0) & (S["t"] < f1)
    clean = (S["x"] == 0) & ~S["row6"]
    steady = S[clean].groupby("run_id")["step_time_ms"].median()
    return S, steady


def pod_flags(F):
    """Hall B runs whose nodes, in any segment of the allocations file, lie in both pods (the node names carry the
    pod; a replaced node comes from the failed one's pod)."""
    out = {}
    for rid, g in F["alloc"].groupby("run_id"):
        pods = set()
        for n in g["nodes"]:
            pods |= set(re.findall(r"kb-p(\d)", n))
        out[rid] = len(pods) > 1
    return out


def pod_penalty(F, S, steady0, pred, flags, method="weighted"):
    """The step a job pays for having nodes in both pods: each hall B run's steady step over the step its benchmark,
    mix and width predict, the runs with nodes in both pods over the runs with nodes in one, weighted by the logged
    rows each steady step rests on."""
    reg = F["reg"].set_index("run_id")
    clean = S[(S["x"] == 0) & ~S["row6"]].groupby("run_id").size()
    rows = []
    for rid, st in steady0.items():
        if rid not in reg.index or reg.loc[rid, "hall"] != "B" or not np.isfinite(st) or rid not in pred:
            continue
        rows.append(dict(run_id=rid, both=bool(flags.get(rid, False)), ratio=float(st / pred[rid]["step_max_ms"]),
                         n=int(clean.get(rid, 0))))
    d = pd.DataFrame(rows)
    d = d[d["n"] >= 30]
    w = lambda g: float((g["ratio"] * g["n"]).sum() / g["n"].sum())
    if method == "registered":
        d = d[d["run_id"].str.startswith("kide-")]
    one, two = d[~d["both"]], d[d["both"]]
    pen = w(two) / w(one) - 1.0
    if method == "twin":
        # each straddling run over the non-straddling run of its own model that has the most rows
        ratios = []
        for r in two.itertuples():
            same = one[one["run_id"].map(lambda i: reg.loc[i, "model"]) == reg.loc[r.run_id, "model"]]
            if len(same):
                ref = same.sort_values("n").iloc[-1]
                ratios.append((r.ratio / ref["ratio"] - 1.0, r.n))
        pen = float(sum(v * n for v, n in ratios) / sum(n for _, n in ratios))
    return dict(pen=float(pen), ratio_one=w(one), ratio_both=w(two), n_one=int(len(one)), n_both=int(len(two)), runs=d)


def steady_with_model(steady, pred, flags=None, pen=0.0):
    """A run with no interval clear of the cap (the January scale test ran the whole hall) takes its step from the
    cost model, with the pod penalty where its nodes lie in both pods."""
    st = steady.copy()
    for rid, p in pred.items():
        if rid not in st.index or not np.isfinite(st.get(rid, np.nan)):
            st.loc[rid] = p["step_max_ms"] * (1.0 + pen if (flags or {}).get(rid, False) else 1.0)
    return st


def local_baseline(S, b, steady, days=3):
    """For each capped row, the median of the same run's clear steps within `days` days either side (the run's own
    steady where none), a baseline that follows the run's slow drift."""
    clean = S[(S["x"] == 0) & ~S["row6"]].copy()
    clean["d"] = clean["t"].dt.floor("D")
    dm = clean.groupby(["run_id", "d"])["step_time_ms"].median()
    out = np.empty(len(b))
    cache = {}
    for i, (rid, t) in enumerate(zip(b["run_id"].values, b["t"].dt.floor("D").values)):
        key = (rid, t)
        if key not in cache:
            vals = []
            for k in range(-days, days + 1):
                v = dm.get((rid, t + np.timedelta64(k, "D")), np.nan)
                if np.isfinite(v):
                    vals.append(v)
            cache[key] = float(np.median(vals)) if vals else float(steady.get(rid, np.nan))
        out[i] = cache[key]
    return out


def throttle_fit(F, S, steady, form="quad", baseline="median"):
    """Step-time stretch on hall B against the rebuilt excess, through the origin: linear and quadratic terms (or the
    line alone, or the mean stretch by band of excess), against each run's steady step (or its own clear steps
    around the capped day)."""
    reg = F["reg"].set_index("run_id")
    b = S[(S["run_id"].map(reg["hall"]) == "B") & (S["x"] > 0)].copy()
    base = local_baseline(S, b, steady) if baseline == "local" else b["run_id"].map(steady).values
    b["stretch"] = b["step_time_ms"].values / base - 1.0
    b = b[np.isfinite(b["stretch"])]
    x, y = b["x"].values, b["stretch"].values
    th = dict(n=int(len(b)), xmax=float(x.max()), capped_days=int(b["t"].dt.date.nunique()))
    if form == "lin":
        th.update(a1=float((x * y).sum() / (x * x).sum()), a2=0.0)
    elif form == "bins":
        edges = np.array([0, 0.02, 0.04, 0.07, 0.10, 0.14, 0.20, 0.30])
        idx = np.digitize(x, edges)
        xs, ys = [0.0], [0.0]
        for k in range(1, len(edges)):
            sel = idx == k
            if sel.sum() >= 50:
                xs.append(float(x[sel].mean()))
                ys.append(float(y[sel].mean()))
        th.update(xs=np.array(xs), ys=np.array(ys), a1=float((x * y).sum() / (x * x).sum()), a2=0.0)
    else:
        coef, *_ = np.linalg.lstsq(np.c_[x, x ** 2], y, rcond=None)
        th.update(a1=float(coef[0]), a2=float(coef[1]))
    return th


def stretch(th, x):
    x = np.maximum(np.asarray(x, float), 0.0)
    if "xs" in th:
        return 1.0 + np.interp(x, th["xs"], th["ys"])
    return 1.0 + th["a1"] * x + th["a2"] * x * x


# ------------------------------------------------------------------ R6, R7: interruptions and works
def stop_model(F, S, steady):
    st = F["stops"].drop_duplicates(subset=["run_id", "failed_at_utc", "kind", "step_at_failure"]).copy()
    st["fail"] = st["failed_at_utc"].map(ts)
    st["resume"] = st["resumed_at_utc"].map(ts)
    st["down_min"] = (st["resume"] - st["fail"]).dt.total_seconds() / 60
    reg = ledger(F).set_index("run_id")
    st["hall"] = st["run_id"].map(reg["hall"])
    st["nodes"] = st["run_id"].map(reg["nodes"])
    st["lost_steps"] = st["step_at_failure"] - st["resumed_from_step"]
    st["lost_s"] = st["lost_steps"] * st["run_id"].map(steady) / 1000.0
    node_days = {h: float((reg[reg["hall"] == h]["nodes"] * (reg[reg["hall"] == h]["finish"] - reg[reg["hall"] == h]["launch"]).dt.total_seconds() / 86400).sum()) for h in ("A", "B")}
    run_days = reg.assign(days=(reg["finish"] - reg["launch"]).dt.total_seconds() / 86400)
    hw = st[st["kind"] == "hardware"]
    sw = st[st["kind"] == "software"]
    fac = st[st["kind"] == "facility"]
    m = {}
    m["hw_per_node_day"] = {h: float((hw["hall"] == h).sum() / node_days[h]) for h in ("A", "B")}
    # software crashes per run-day, by run width (wide runs crash more often), fitted as a share of the square root
    # of width over 256 nodes, capped at one
    wd = run_days.assign(w=np.minimum(1.0, np.sqrt(run_days["nodes"] / 256.0)))
    m["sw_per_wday"] = float(len(sw) / (wd["days"] * wd["w"]).sum())
    # facility events: one per hall stop, whatever the number of runs it stopped
    inc = F["incidents"]
    inc = inc[inc["category"].isin(["fabric", "power", "cooling", "storage"]) & ~inc["summary"].str.contains("CRAC-6")]
    hall_days = {h: (REVIEW_END - dt.datetime(2026, 1, 1)).days for h in ("A", "B")}
    m["fac_per_hall_day"] = {h: float((inc["hall"] == "HALL-%s" % h).sum() / hall_days[h]) for h in ("A", "B")}
    m["restart_min"] = {k: float(st[st["kind"] == k]["down_min"].mean()) for k in ("hardware", "software", "facility")}
    m["lost_frac_interval"] = float((st[st["kind"].isin(["hardware", "software", "facility"])]["lost_s"] / 1800.0).mean())
    m["stops"] = st
    return m


def works_model(F):
    w = F["works"].copy()
    w = w.rename(columns={"Work order": "work_order", "Hall": "hall", "Type": "work_type", "Title": "title",
                          "Planned start": "planned_start", "Planned duration (h)": "planned_hours",
                          "Actual start": "actual_start", "Actual finish": "actual_finish"})
    for c in ("planned_start", "actual_start", "actual_finish"):
        w[c] = pd.to_datetime(w[c], format="%d.%m.%Y %H:%M")
    w["actual_hours"] = (w["actual_finish"] - w["actual_start"]).dt.total_seconds() / 3600
    w["ratio"] = w["actual_hours"] / w["planned_hours"]
    w["delay_h"] = (w["actual_start"] - w["planned_start"]).dt.total_seconds() / 3600
    ratio = w.groupby("work_type")["ratio"].mean().to_dict()
    delay = w.groupby("work_type")["delay_h"].mean().to_dict()
    return dict(ratio=ratio, delay=delay, rows=w)


# ------------------------------------------------------------------ the 2027 runs
def runs_2027(F, PK, CM):
    out = []
    rm = F["roadmap"].set_index("run_id")
    for rid, cfg in F["configs"].items():
        m = cfg["model"]
        N, L, d = float(m["params"]), int(m["layers"]), int(m["d_model"])
        D, g, C = int(cfg["parallelism"]["data"]), int(cfg["batch"]["seqs_per_rank"]), int(cfg["batch"]["seq_len"])
        mix, rule = cfg["data"]["mix"], cfg["data"]["packing"]
        hall = cfg["reservation"]["hall"]
        a_ms, emax_b, emean_b, tps = dense_ms(F, PK, CM, m["size"], L, d, N, C, g, hall)
        S, Fl = PK.stream(mix, C, rule)
        kf = L * d * C / N
        emax, emean = step_units(S, kf, CM["beta"], D, g, seed=int(D * 7 + g + C))
        ws = rm.loc[rid, "window_start"]
        we = rm.loc[rid, "window_end"]
        ws = ws if isinstance(ws, dt.date) else dt.date.fromisoformat(str(ws)[:10])
        we = we if isinstance(we, dt.date) else dt.date.fromisoformat(str(we)[:10])
        if isinstance(ws, dt.datetime):
            ws, we = ws.date(), we.date()
        block = str(rm.loc[rid, "block"])
        out.append(dict(run_id=rid, model=m["size"], N=N, L=L, d=d, D=D, g=g, C=C, mix=mix, rule=rule, hall=hall,
                        ws=ws, we=we, window_days=(we - ws).days, budget=float(rm.loc[rid, "token_budget"]),
                        a_ms=a_ms, emax_b=emax_b, emean_b=emean_b, emax=emax, emean=emean, fill=float(Fl.mean()),
                        S_mean=float(S.mean()), tps_bench=tps, ckpt_gb=N * 14 / 1e9, block=block,
                        both=len(set(re.findall(r"kb-p(\d)", block))) > 1,
                        rows=set(re.findall(r"(kb-p\d-r\d\d|ka-r\d\d)", block))))
    for r in out:
        r["preds"] = [p["run_id"] for p in out if p["hall"] == r["hall"] and p["ws"] < r["ws"] and p["rows"] & r["rows"]]
    return out


def pava_down(y, w):
    """The non-increasing fit closest to y (weights w): pool adjacent violators."""
    blocks = [[float(v), float(wt), 1] for v, wt in zip(y, w)]
    out = []
    for blk in blocks:
        out.append(blk)
        while len(out) > 1 and out[-2][0] < out[-1][0]:
            b2, b1 = out.pop(), out.pop()
            tw = b1[1] + b2[1]
            out.append([(b1[0] * b1[1] + b2[0] * b2[1]) / tw, tw, b1[2] + b2[2]])
    fit = []
    for v, wt, n in out:
        fit += [v] * n
    return np.array(fit)


def pool_response(F, ledger_df, kw, contract=8100.0, method="curve", plateau_below=0.80):
    """The research pool's busy share of hall B's nodes no registered run holds, in 2026, against the load the
    registered runs alone put on the hall (their held nodes through the fitted draw line, over the contract): the
    share at light registered load, and how much of it is left as that load nears the contract."""
    ex = F["states"][F["states"]["hall"] == "B"].copy()
    ex["t"] = pd.to_datetime(ex["ts_utc"], format="%Y-%m-%dT%H:%M:%SZ")
    held = np.zeros(len(ex))
    tt = ex["t"].values
    for r in ledger_df[ledger_df["hall"] == "B"].itertuples():
        held += ((tt >= np.datetime64(r.launch)) & (tt < np.datetime64(r.finish))) * r.nodes
    alloc = ex["allocated"].values.astype(float)
    free = 1024.0 - held
    ok = (free > 32) & (alloc > 0)
    share = np.clip(alloc - held, 0, None)[ok] / free[ok]
    ratio = ((kw[0] + kw[1] * held) / contract)[ok]
    edges = np.arange(0.40, 1.50, 0.02)
    idx = np.digitize(ratio, edges)
    cen, mean, cnt = [], [], []
    for k in range(1, len(edges)):
        sel = idx == k
        if sel.sum() >= 60:
            cen.append(float(ratio[sel].mean()))
            mean.append(float(share[sel].mean()))
            cnt.append(int(sel.sum()))
    plateau = float(share[ratio < plateau_below].mean())
    cen, cnt = np.array(cen), np.array(cnt)
    phi = pava_down(np.clip(np.array(mean) / plateau, 0.0, 1.0), cnt)
    if method in ("step", "logistic"):
        grid = np.arange(0.40, 1.60, 0.005)
        if method == "step":
            c0 = 0.5 * (cen[phi >= 0.5].max() + cen[phi < 0.5].min())
            fit = (grid < c0).astype(float)
        else:
            best = (1e9, None)
            for m in np.arange(0.80, 1.10, 0.005):
                for sc in (0.004, 0.008, 0.015, 0.025, 0.04, 0.06):
                    sse = float((cnt * (1.0 / (1.0 + np.exp((cen - m) / sc)) - phi) ** 2).sum())
                    if sse < best[0]:
                        best = (sse, (m, sc))
            m, sc = best[1]
            fit = 1.0 / (1.0 + np.exp((grid - m) / sc))
        cen, phi = grid, fit
    return dict(plateau=plateau, mean_share=float(share.mean()), cen=np.array(cen), phi=phi, counts=cnt.tolist(),
                days_in_band=float(((ratio > 0.88) & (ratio < 0.97)).sum() * 300 / 86400))


class Replay:
    """H1 2027 replayed on the five-minute grid with the golden's fitted inputs: each run's step (and the pod penalty
    where its block lies in both pods), hall B's excess from the blocks and the pool at its measured back-off,
    interruptions and restarts as expected losses, works at the overrun record, a launch delay at the window's
    opening; every run kept on its block until it finishes, a block's next run launching when the nodes are back."""

    def __init__(self, F, runs, CM, TH, SM, WM, PR, launch_min, contract=8100.0, kw=None, pen=0.0):
        self.F, self.runs, self.CM, self.TH, self.SM, self.WM = F, runs, CM, TH, SM, WM
        self.PR, self.launch_min, self.contract = PR, launch_min, contract
        self.kw = kw   # (intercept, per allocated node) of hall B's draw line
        self.pen = pen
        self.NI = 200 * 288

    def works_windows(self, ratio_on=True, ratios=None):
        out = []
        for w in self.F["notice"].itertuples():
            r = (ratios or self.WM["ratio"]).get(w.work_type, 1.0) if ratio_on else 1.0
            a = local_to_utc(w.start_local) + dt.timedelta(hours=self.WM["delay"].get(w.work_type, 0.0) if ratio_on else 0.0)
            out.append((w.hall, a, a + dt.timedelta(hours=w.planned_hours * r)))
        return out

    def run(self, s1=True, s18=True, s3=True, works_ratio=True, interrupts=True, works_on=True, launch=True,
            mix=True, beta=None, th=None, rates=None, wratio=None, pool_delta=0.0, pen_delta=0.0, fullctx=False,
            bench_only=False, avail=None, hold="extend", pod=True, phi=True, precedence=True):
        beta = beta if beta is not None else self.CM["beta"]
        th = th or self.TH
        res = {}
        works = self.works_windows(works_ratio, wratio) if works_on else []
        spec = []
        for r in self.runs:
            if bench_only:
                step = r["g"] * r["C"] / (8.0 * r["tps_bench"])
                tok = r["D"] * r["g"] * r["C"]
            else:
                kf = r["L"] * r["d"] * r["C"] / r["N"]
                if fullctx:
                    units = r["g"] * (1 + beta * kf)
                elif s1:
                    units = r["emax"] if beta == self.CM["beta"] else r["emax"] * (1 + beta * kf * r["S_mean"]) / (1 + self.CM["beta"] * kf * r["S_mean"])
                else:
                    units = r["emean"] if mix else r["emean_b"]
                step = r["a_ms"] * units * (1 + self.CM["ovh"]) / 1000.0
                if pod and r["both"]:
                    step *= 1.0 + self.pen + pen_delta
                tok = r["D"] * r["g"] * r["C"] * (r["fill"] if s18 else 1.0)
            spec.append((r, step, tok))
        ends = {r["run_id"]: dt.datetime.combine(r["we"], dt.time(0)) for r in self.runs}
        for it in range(4):
            xb = self.hall_b(ends, hold, phi, pool_delta) if s3 else np.zeros(self.NI)
            for r, step, tok in spec:
                ready = max([ends[p] for p in r["preds"]], default=None) if precedence else None
                d = self.progress(r, step, tok, xb, works, interrupts, launch, th, rates,
                                  avail.get(r["run_id"]) if avail else None, ready)
                ends[r["run_id"]] = dt.datetime.combine(r["ws"], dt.time(0)) + dt.timedelta(days=d)
        for r in self.runs:
            res[r["run_id"]] = (ends[r["run_id"]] - dt.datetime.combine(r["ws"], dt.time(0))).total_seconds() / 86400
        return res

    def hall_b(self, ends, hold="extend", phi=True, pool_delta=0.0):
        held = np.zeros(self.NI)
        for r in self.runs:
            if r["hall"] != "B":
                continue
            a = int((dt.datetime.combine(r["ws"], dt.time(0)) - T27).total_seconds() // GRID)
            we, en = dt.datetime.combine(r["we"], dt.time(0)), ends[r["run_id"]]
            last = {"extend": max(we, en), "idle_after_finish": en, "window_only": we}[hold]
            b = int((last - T27).total_seconds() // GRID) + 1
            held[max(0, a):min(self.NI, b)] += r["D"]
        free = 1024 - held
        base = (self.kw[0] + self.kw[1] * held) / self.contract
        if phi:
            share = (self.PR["plateau"] + pool_delta) * np.interp(base, self.PR["cen"], self.PR["phi"])
        else:
            share = self.PR["mean_share"] + pool_delta
        alloc = held + free * share
        draw = self.kw[0] + self.kw[1] * alloc
        return np.maximum(0.0, draw / self.contract - 1.0)

    def progress(self, r, step, tok, xb, works, interrupts, launch, th, rates, avail_k=None, ready=None):
        SM = self.SM if rates is None else rates
        a0 = dt.datetime.combine(r["ws"], dt.time(0))
        i0 = int((a0 - T27).total_seconds() // GRID)
        lm = self.launch_min if launch else 0.0
        target = r["budget"] / tok
        st = stretch(th, xb) if r["hall"] == "B" else np.ones(self.NI)
        rate = GRID / (step * st)                       # steps per grid interval while up
        # expected losses per unit of running time: stops times (restart downtime + lost work)
        if interrupts:
            lam_hw = SM["hw_per_node_day"][r["hall"]] * r["D"]
            lam_sw = SM["sw_per_wday"] * min(1.0, math.sqrt(r["D"] / 256.0))
            lam_fac = SM["fac_per_hall_day"][r["hall"]]
            loss_day = (lam_hw * (SM["restart_min"]["hardware"] + 0.0) + lam_sw * SM["restart_min"]["software"] +
                        lam_fac * SM["restart_min"]["facility"]) / 1440.0
            lost_day = (lam_hw + lam_sw + lam_fac) * SM["lost_frac_interval"] * 30.0 / 1440.0
            avail = max(0.0, 1.0 - loss_day - lost_day)
        else:
            avail = 1.0
        if avail_k is not None:
            avail = avail_k
        up = np.ones(self.NI)
        for h, a, b in works:
            if h == r["hall"]:
                ia = int((a - T27).total_seconds() // GRID)
                ib = int(math.ceil((b - T27).total_seconds() / GRID)) + (int(math.ceil(SM["restart_min"]["facility"] / 5.0)) if interrupts else 0)
                up[max(0, ia):max(0, ib)] = 0.0
        start = i0 + int(math.ceil(lm / 5.0))
        if ready is not None:
            start = max(start, int((ready - T27).total_seconds() // GRID) + int(math.ceil(lm / 5.0)))
        cs = np.cumsum(rate[start:] * up[start:] * avail)
        j = int(np.searchsorted(cs, target))
        if j >= len(cs):
            return 999.0
        prev = cs[j - 1] if j > 0 else 0.0
        frac = (target - prev) / max(cs[j] - prev, 1e-12)
        return (start - i0 + j + frac) * GRID / 86400.0


def launch_delay(F):
    reg = ledger(F)
    first = clean_steps(F).groupby("run_id")["t"].min()
    d = (reg.set_index("run_id")["launch"] - reg.set_index("run_id")["launch"].dt.floor("D")).dt.total_seconds() / 60
    return float(d.mean())


# ------------------------------------------------------------------ the whole golden
def golden(T, mc=0, F=None, seed=20271, contract=None, clear_kw=40.0, min_alloc=0, th_form="quad",
           th_baseline="median", pen_method="weighted", pool_method="curve", plateau_below=0.80,
           works_stat="mean", launch="mean"):
    """The golden chain read from the pack; the keyword options are the defensible alternatives the variant battery
    runs (`results.battery`): each changes one modelling choice and nothing else."""
    F = F or load(T)
    S = clean_steps(F)
    led = ledger(F)
    exB, kwB, cB = hall_excess(F, "B", contract=contract or contract_kw("B"), clear_kw=clear_kw, min_alloc=min_alloc)
    CM = cost_model(F, exB)
    PK = Packer(F, seed=seed)
    S2, steady0 = steady_steps(F, S, exB, CM)
    pred = predicted_steps(F, PK, CM)
    flags = pod_flags(F)
    PEN = pod_penalty(F, S2, steady0, pred, flags, method=pen_method)
    steady = steady_with_model(steady0, pred, flags, PEN["pen"])
    TH = throttle_fit(F, S2, steady, form=th_form, baseline=th_baseline)
    SM = stop_model(F, S2, steady)
    WM = works_model(F)
    if works_stat == "median":
        WM = dict(WM)
        WM["ratio"] = WM["rows"].groupby("work_type")["ratio"].median().to_dict()
    runs = runs_2027(F, PK, CM)
    PR = pool_response(F, led, kwB, cB, method=pool_method, plateau_below=plateau_below)
    lm = launch_delay(F) if launch == "mean" else 0.0
    RP = Replay(F, runs, CM, TH, SM, WM, PR, lm, contract=cB, kw=tuple(kwB), pen=PEN["pen"])
    days = RP.run()
    return dict(F=F, S=S2, ledger=led, exB=exB, kwB=kwB, CM=CM, steady=steady, steady0=steady0, pred=pred, TH=TH, SM=SM,
                WM=WM, PK=PK, runs=runs, PR=PR, PEN=PEN, flags=flags, launch_min=lm, RP=RP, days=days)


# ------------------------------------------------------------------ the bridges
BRIDGE_2027 = [
    ("benchmark days", dict(bench_only=True, s3=False, interrupts=False, works_on=False, launch=False, pod=False, phi=False)),
    ("the run's own mix at the mean rank", dict(s1=False, s18=False, s3=False, interrupts=False, works_on=False, launch=False, pod=False, phi=False)),
    ("waiting for the slowest rank", dict(s1=True, s18=False, s3=False, interrupts=False, works_on=False, launch=False, pod=False, phi=False)),
    ("padding in packed sequences", dict(s1=True, s18=True, s3=False, interrupts=False, works_on=False, launch=False, pod=False, phi=False)),
    ("a block across both pods", dict(s3=False, interrupts=False, works_on=False, launch=False)),
    ("hall B held to its contracted load", dict(s3=True, interrupts=False, works_on=False, launch=False)),
    ("interruptions and restarts", dict(s3=True, interrupts=True, works_on=False, launch=False)),
    ("provider works and the window's opening", dict()),
]


def bridge_2027(G, over=None):
    RP = G["RP"]
    cum = [RP.run(**{**kw, **(over or {})}) for _, kw in BRIDGE_2027]
    out = {}
    for r in G["runs"]:
        k = r["run_id"]
        vals = [c[k] for c in cum]
        items = {BRIDGE_2027[0][0]: vals[0]}
        for i in range(1, len(vals)):
            items[BRIDGE_2027[i][0]] = vals[i] - vals[i - 1]
        items["expected days"] = vals[-1]
        out[k] = items
    return out


def bridge_2026(G):
    """2026 as a whole, GPU-days: the benchmark's, then each cause in order, to the GPU-days held."""
    F, S, pred, steady = G["F"], G["S"], G["pred"], G["steady"]
    led = G["ledger"].set_index("run_id")
    toks = S.groupby("run_id")["tokens_seen"].max()
    reg = F["reg"].set_index("run_id")
    items = {k: 0.0 for k in ("benchmark GPU-days", "the runs' own mixes at the mean rank", "waiting for the slowest rank",
                              "padding in packed sequences", "blocks across both pods", "hall B held to its contracted load",
                              "hall A row 6 cooling fault", "interruptions and restarts", "provider works", "other")}
    per = {}
    st = G["SM"]["stops"]
    for rid in led.index:
        p = pred[rid]
        gpus = led.loc[rid, "nodes"] * 8
        b0 = toks[rid] / p["tps"] / 86400.0
        mix = b0 * (p["emean"] / p["emax_b"] - 1.0)
        slow = b0 * (p["emax"] - p["emean"]) / p["emax_b"]
        pad = b0 * p["emax"] / p["emax_b"] * (1.0 / p["fill"] - 1.0)
        pod = (b0 + mix + slow + pad) * G["PEN"]["pen"] if G["flags"].get(rid, False) else 0.0
        rows = S[S["run_id"] == rid]
        n = reg.loc[rid, "log_every_steps"]
        sd = steady[rid]
        cap = float(((rows["step_time_ms"] - sd).clip(lower=0) * (rows["x"] > 0)).sum() * n / 1000.0 * gpus / 86400.0)
        r6 = float(((rows["step_time_ms"] - sd).clip(lower=0) * rows["row6"]).sum() * n / 1000.0 * gpus / 86400.0)
        s = st[st["run_id"] == rid]
        nonw = s[s["kind"] != "provider works"]
        intr = float(((nonw["lost_steps"] * sd / 1000.0) + nonw["down_min"] * 60).sum() * gpus / 86400.0)
        wk = s[s["kind"] == "provider works"]
        wks = float(((wk["lost_steps"] * sd / 1000.0) + wk["down_min"] * 60).sum() * gpus / 86400.0)
        held = float(led.loc[rid, "gpu_days_held"])
        other = held - (b0 + mix + slow + pad + pod + cap + r6 + intr + wks)
        per[rid] = dict(bench=b0, mix=mix, slow=slow, pad=pad, pod=pod, cap=cap, row6=r6, intr=intr, works=wks,
                        other=other, held=held)
        for k, v in zip(items, (b0, mix, slow, pad, pod, cap, r6, intr, wks, other)):
            items[k] += v
    items["GPU-days held"] = float(led["gpu_days_held"].sum())
    return items, per


# ------------------------------------------------------------------ the 80 per cent range
def mc_range(G, n=160, seed=4242):
    """Draws of the year: the fitted rates, restart and lost-work costs, the throttle and the pool share resampled
    from their 2026 records, each 2027 work's overrun drawn from the 2025-26 ratios of its type, and each run's
    interruptions drawn as a count over its running days."""
    rng = np.random.default_rng(seed)
    RP, SM, WM, TH = G["RP"], G["SM"], G["WM"], G["TH"]
    st = SM["stops"]
    S = G["S"]
    reg = G["F"]["reg"].set_index("run_id")
    capped = S[(S["run_id"].map(reg["hall"]) == "B") & (S["x"] > 0)].copy()
    capped["stretch"] = capped["step_time_ms"] / capped["run_id"].map(G["steady"]) - 1.0
    capped = capped[np.isfinite(capped["stretch"])]
    days_by = {d: g for d, g in capped.groupby(capped["t"].dt.date)}
    dkeys = list(days_by)
    ratios = WM["rows"].groupby("work_type")["ratio"].apply(list).to_dict()
    base = G["days"]
    out = {r["run_id"]: [] for r in G["runs"]}
    for k in range(n):
        pick = [dkeys[i] for i in rng.integers(0, len(dkeys), len(dkeys))]
        b = pd.concat([days_by[d] for d in pick])
        X = np.c_[b["x"].values, b["x"].values ** 2]
        c, *_ = np.linalg.lstsq(X, b["stretch"].values, rcond=None)
        th = dict(a1=float(c[0]), a2=float(c[1]))
        wr = {t: float(rng.choice(v)) for t, v in ratios.items()}
        dpool = float(rng.normal(0, 0.03))
        dpen = float(rng.normal(0, 0.012))
        avail = {}
        for r in G["runs"]:
            dd = base[r["run_id"]]
            lam = (SM["hw_per_node_day"][r["hall"]] * r["D"] + SM["sw_per_wday"] * min(1.0, math.sqrt(r["D"] / 256.0)) +
                   SM["fac_per_hall_day"][r["hall"]])
            m = rng.poisson(lam * dd)
            kinds = rng.choice(["hardware", "software", "facility"], size=m,
                               p=np.array([SM["hw_per_node_day"][r["hall"]] * r["D"],
                                           SM["sw_per_wday"] * min(1.0, math.sqrt(r["D"] / 256.0)),
                                           SM["fac_per_hall_day"][r["hall"]]]) / lam)
            lost = 0.0
            for kd in kinds:
                pool_k = st[st["kind"] == kd]["down_min"].values
                lost += float(rng.choice(pool_k)) + float(rng.uniform(0, 30))
            avail[r["run_id"]] = max(0.0, 1.0 - lost / (dd * 1440.0))
        d = RP.run(th=th, wratio=wr, pool_delta=dpool, pen_delta=dpen, avail=avail)
        for kk, v in d.items():
            out[kk].append(v)
    return {kk: (float(np.percentile(v, 10)), float(np.percentile(v, 90))) for kk, v in out.items()}


# ------------------------------------------------------------------ the routes
def direct_route(G):
    """The pack's most direct evidence read at face value: each 2027 run's benchmark days over the realised rate of
    its nearest 2026 twin (the run in the same hall whose model size, context and sequences per rank are closest),
    realised being its steady tokens per GPU-second over its benchmark's."""
    F, pred, steady = G["F"], G["pred"], G["steady0"]
    reg = F["reg"].set_index("run_id")
    rows = []
    for rid, r in reg.iterrows():
        st = steady.get(rid, np.nan)
        if not np.isfinite(st):
            continue
        p = pred[rid]
        real = r["nodes"] * r["seqs_per_rank"] * r["context_tokens"] * p["fill"] / (st / 1000.0) / (r["nodes"] * 8)
        rows.append(dict(hall=r["hall"], N=r["params_b"], C=r["context_tokens"], g=r["seqs_per_rank"], rho=real / p["tps"]))
    d = pd.DataFrame(rows)
    out = {}
    for r in G["runs"]:
        c = d[d["hall"] == r["hall"]].copy()
        c["dist"] = (np.log(c["N"] / (r["N"] / 1e9)) ** 2 + 0.5 * np.log(c["C"] / r["C"]) ** 2 +
                     0.25 * np.log(c["g"] / r["g"]) ** 2)
        out[r["run_id"]] = r["budget"] / (r["tps_bench"] * 8 * r["D"]) / 86400.0 / float(c.sort_values("dist").iloc[0]["rho"])
    return out


def routes(G):
    """Each hurried method as one pass of the replay with its judgments switched. The reflex route is the careful but
    hurried pass: every move the runs make unprompted right (the slowest rank, the padding, the throttle on the
    rebuilt excess, the works overrun, interruptions, the block's extension), the two judgments they have been seen
    to lose hurried (no pod penalty, the pool at its mean share of free nodes)."""
    RP = G["RP"]
    R = {}
    R["quick: benchmark days"] = RP.run(bench_only=True, s3=False, interrupts=False, works_on=False, launch=False,
                                        pod=False, phi=False)
    R["careful but hurried"] = RP.run(pod=False, phi=False)
    R["shallow: mean rank, full sequences, no throttle, planned works hours"] = RP.run(
        s1=False, s18=False, s3=False, works_ratio=False, pod=False, phi=False)
    R["the full-context FLOPs formula"] = RP.run(fullctx=True, s18=False, s3=False, works_ratio=False, pod=False,
                                                 phi=False)
    b26, _ = bridge_2026(G)
    F26 = b26["GPU-days held"] / b26["benchmark GPU-days"]
    bench = R["quick: benchmark days"]
    R["the 2026 benchmark-to-held ratio"] = {k: v * F26 for k, v in bench.items()}
    R["direct: the nearest 2026 run's realised rate"] = direct_route(G)
    R["drop P (no pod penalty)"] = RP.run(pod=False)
    R["drop Q (the pool at its mean share)"] = RP.run(phi=False)
    R["fix P alone"] = RP.run(phi=False)
    R["fix Q alone"] = RP.run(pod=False)
    R["drop S1 (the mean rank)"] = RP.run(s1=False)
    R["drop S18 (full sequences)"] = RP.run(s18=False)
    R["drop S3 (no throttle)"] = RP.run(s3=False)
    R["drop S4 (planned works hours)"] = RP.run(works_ratio=False)
    return R, F26


def late_set(G, days):
    return sorted(r["run_id"] for r in G["runs"] if days[r["run_id"]] > r["window_days"])
