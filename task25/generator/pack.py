"""The pack under target/, written the way each system exports: the trainer's logs and the registry (UTC), the
profiler's samples and the loader's manifests, the scheduler's node states, the provider's meter, work orders and
incident log (Helsinki local time), the benchmark and its harness config, the 2027 plan inputs, and two files the
analysis never needs. Layer 1 mess is applied here, by the process step that produces it."""
import datetime as dt
import json
import math
import zlib
import os

import numpy as np
import pandas as pd

import params as P
import records as RC
import world as W

RENAMES = {"kide-34b-v1": "kide-34b-v1-r2", "kide-70b-v1": "kide-70b-v1-r3", "kide-13b-v3": "kide-13b-v3b"}
COUNTER_RESET = ("kide-13b-v2", "kide-70b-v1-lc32")    # trainer v2.3 restarted the logged step at a resume
TRAINER = {"2026-01": "kd-train 2.2.4", "2026-04": "kd-train 2.3.1", "2026-08": "kd-train 2.4.0"}


def rename_time(r):
    """A renamed run takes its new ID at the resume halfway through its stops."""
    stops = sorted(r.get("stops", []), key=lambda s: s["ts_fail"])
    if r["run_id"] in RENAMES and len(stops) > 4:
        s = stops[len(stops) // 2]
        return s["ts_fail"] + dt.timedelta(minutes=s["down_min"])
    return None


def id_at(r, when):
    t = rename_time(r)
    return RENAMES[r["run_id"]] if (t is not None and when >= t) else r["run_id"]


def trainer_version(d):
    v = "kd-train 2.2.4"
    for k, name in sorted(TRAINER.items()):
        if d.strftime("%Y-%m") >= k:
            v = name
    return v


def fmt_ts(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def fmt_local(t):
    return t.strftime("%d.%m.%Y %H:%M")


# ------------------------------------------------------------------ the trainer's step log and the registry
def step_log(rec, rng):
    rows = []
    for r in rec["runs"]:
        if not r["rows"]:
            continue
        rid0 = r["run_id"]
        tok = r["tok_step"]
        n = r["log_every"]
        stops = sorted(r["stops"], key=lambda s: s["ts_fail"])
        rename_at = rename_time(r)
        reset_at = stops[len(stops) // 3]["ts_fail"] if rid0 in COUNTER_RESET and len(stops) >= 3 else None
        reset_base = None
        prev_t = None
        prev_step = None
        loss0 = {"1B": 2.62, "3B": 2.38, "8B": 2.18, "13B": 2.09, "34B": 1.97, "70B": 1.88, "120B": 1.82}[r["model"]]
        last_buf = []
        stop_iter = iter(stops)
        next_stop = next(stop_iter, None)
        for (tg, step, st) in r["rows"]:
            ts = RC.gts(0, tg)
            while next_stop is not None and ts > next_stop["ts_fail"]:
                # the logger re-sends its last buffer at the resume, about half the time
                if last_buf and rng.random() < 0.55:
                    rows.extend(dict(x) for x in last_buf[-int(rng.integers(2, 5)):])
                next_stop = next(stop_iter, None)
                prev_t = None
            rid = RENAMES[rid0] if (rename_at is not None and ts >= rename_at) else rid0
            logged = step
            if reset_at is not None and ts > reset_at:
                if reset_base is None:
                    reset_base = step - n
                logged = step - reset_base
            tokens = step * tok * (1 + 0.0004 * rng.standard_normal()) if r["rule"] == "best_fit" else step * tok
            tokens = int(round(tokens))
            dtm = st * 1000.0 * (1 + 0.006 * rng.standard_normal())
            frac = min(1.0, tokens / max(r["budget"], 1.0)) if not r["live"] else tokens / 2.0e13
            lr = 3e-4 * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, frac)))) if frac > 0.01 else 3e-4 * frac / 0.01
            loss = loss0 + 3.1 * (max(tokens, 1e9) / 1e9) ** -0.30 + 0.012 * rng.standard_normal()
            gn = 0.9 + 0.35 * math.exp(-frac * 6) + abs(0.08 * rng.standard_normal())
            row = dict(ts_utc=fmt_ts(ts), run_id=rid, step=int(logged), tokens_seen=tokens,
                       step_time_ms=round(dtm, 1), tokens_per_s=int(round(tok / st)), loss=round(loss, 4),
                       lr=float("%.3e" % lr), grad_norm=round(gn, 3))
            rows.append(row)
            last_buf.append(row)
            if len(last_buf) > 6:
                last_buf.pop(0)
    df = pd.DataFrame(rows)
    return df.sort_values(["ts_utc", "run_id"], kind="mergesort").reset_index(drop=True)


def registry(rec):
    rows = []
    for r in rec["runs"]:
        N, L, d = P.MODELS[r["model"]]
        rid = RENAMES.get(r["run_id"], r["run_id"]) if r["run_id"] in RENAMES else r["run_id"]
        rows.append(dict(
            run_id=rid, previous_ids=r["run_id"] if r["run_id"] in RENAMES else "",
            purpose=("ablation" if r["run_id"].startswith("abl-") else
                     "scale test" if "scale" in r["run_id"] else
                     "long-context extension" if "-lc" in r["run_id"] else "pretraining"),
            model=r["model"], params_b=round(N / 1e9, 2), layers=L, d_model=d, context_tokens=r["C"],
            hall=r["hall"], nodes=r["nodes"], gpus=r["nodes"] * P.GPUS_PER_NODE, seqs_per_rank=r["g"],
            global_batch_seqs=r["nodes"] * r["g"], data_mix=r["mix"], packing=r["rule"],
            token_budget=int(r["budget"]) if not r["live"] else "",
            launched_utc=fmt_ts(r["launch"].replace(microsecond=0)),
            finished_utc=fmt_ts(r["end_ts"].replace(microsecond=0)) if r["end_ts"] else "",
            status="completed" if r["end_ts"] else "running",
            trainer=trainer_version(r["start"]), log_every_steps=r["log_every"],
        ))
    return pd.DataFrame(rows).sort_values("launched_utc").reset_index(drop=True)


def allocations(rec):
    rows = []
    for r in rec["runs"]:
        rid = r["run_id"]
        nodes = list(rec["nodes"][rid])
        names_all = W.node_names(r["hall"])
        seg_start = r["launch"]
        seg = 1
        rng = np.random.default_rng(zlib.crc32(rid.encode()) % (1 << 31))
        for s in sorted(r["stops"], key=lambda s: s["ts_fail"]):
            end = s["ts_fail"]
            rows.append(dict(run_id=id_at(r, seg_start), segment=seg, start_utc=fmt_ts(seg_start.replace(microsecond=0)),
                             end_utc=fmt_ts(end.replace(microsecond=0)), nodes=W.compress(nodes)))
            if s["kind"] == "hw_node":
                bad = nodes[int(rng.integers(0, len(nodes)))]
                spare = [n for n in names_all if n not in nodes and (r["hall"] == "A" or n[:5] == bad[:5])]
                if spare:
                    nodes[nodes.index(bad)] = spare[int(rng.integers(0, len(spare)))]
                s["node"] = bad
            seg += 1
            seg_start = end + dt.timedelta(minutes=s["down_min"])
        end = r["end_ts"] or RC.T_END
        if seg_start < end:
            rows.append(dict(run_id=id_at(r, seg_start), segment=seg, start_utc=fmt_ts(seg_start.replace(microsecond=0)),
                             end_utc=fmt_ts(end.replace(microsecond=0)), nodes=W.compress(nodes)))
    return pd.DataFrame(rows)


DETAIL = {
    "Xid 79": "GPU has fallen off the bus", "Xid 48": "double-bit ECC error, GPU reset required",
    "ECC DBE": "uncorrectable memory error on HBM stack", "NVLink CRC": "NVLink CRC errors over threshold",
    "PSU fault": "node power supply fault, node fenced", "node unreachable": "node missed 3 heartbeats",
    "NCCL timeout": "collective watchdog timeout after 600 s", "CUDA OOM": "CUDA out of memory in backward",
    "loader stall": "data loader stalled over 900 s", "NaN in loss": "non-finite loss, run halted by guard",
    "segfault": "worker exited with SIGSEGV", "hall stop": "all ranks lost, hall-level event",
}


def interruptions(rec, rng=None):
    """The alerting system's stop records: one row per stop, a few alerts sent twice, codes as each source wrote
    them (the GPU driver's 'Xid 79', the node agent's 'XID79'), the failed node blank when the agent could not name
    it."""
    rng = rng or np.random.default_rng(P.SEED + 61)
    rows = []
    for r in rec["runs"]:
        for s in sorted(r["stops"], key=lambda s: s["ts_fail"]):
            resumed = s["ts_fail"] + dt.timedelta(minutes=s["down_min"])
            if resumed >= RC.T_END:
                continue
            code = s["code"] if s["kind"] != "works" else (s.get("wid") or "works")
            if code.startswith("Xid") and rng.random() < 0.3:
                code = code.replace("Xid ", "XID")
            node = s.get("node", "")
            if node and rng.random() < 0.07:
                node = ""
            detail = DETAIL.get(s["code"], "hall handed to provider for works") if s["kind"] != "works" else \
                "hall stopped for provider works %s" % code
            if node:
                detail += " (%s, gpu %d)" % (node, int(rng.integers(0, 8))) if s["kind"] == "hw_node" else ""
            row = dict(run_id=id_at(r, s["ts_fail"]), failed_at_utc=fmt_ts(s["ts_fail"].replace(microsecond=0)),
                       kind={"hw_node": "hardware", "sw_crash": "software", "hall_event": "facility",
                             "works": "provider works"}[s["kind"]],
                       code=code, node=node, step_at_failure=s["fail_step"], resumed_from_step=s["ckpt_step"],
                       resumed_at_utc=fmt_ts(resumed.replace(second=0, microsecond=0)), detail=detail,
                       alert_id="ALR-%06d" % int(rng.integers(100000, 999999)))
            rows.append(row)
            if rng.random() < 0.04:
                dup = dict(row)
                dup["alert_id"] = "ALR-%06d" % int(rng.integers(100000, 999999))
                rows.append(dup)
    df = pd.DataFrame(rows).sort_values(["failed_at_utc", "run_id", "alert_id"]).reset_index(drop=True)
    return df


# ------------------------------------------------------------------ the scheduler and the provider
def node_states(rec, rng):
    rows = []
    for h, hp in P.HALLS.items():
        N = hp["rows"] * hp["slots"]
        busy = rec["busy"][h]
        # nodes out for repair: a few at a time
        down = np.clip(np.round(2.0 + 1.6 * np.sin(np.arange(RC.NI) / 2017.0) + rng.normal(0, 0.8, RC.NI)), 0, 9)
        alloc = np.minimum(busy, N - down)
        idle = N - alloc - down
        for i in range(0, RC.NI):
            rows.append((fmt_ts(RC.gts(i)), h, int(alloc[i]), int(idle[i]), int(down[i])))
    return pd.DataFrame(rows, columns=["ts_utc", "hall", "allocated", "idle", "down"])


def hall_meter(rec, rng):
    rows = []
    for h, hp in P.HALLS.items():
        d = rec["draw"][h]
        c = hp["contract_kw"]
        meter = np.where(d > c - 4.0, c - 11.0 + rng.normal(0, 5.5, RC.NI), d + rng.normal(0, P.METER_NOISE_KW, RC.NI))
        # collector outages drop runs of intervals
        keep = np.ones(RC.NI, bool)
        i = 0
        while i < RC.NI:
            if rng.random() < 0.0009:
                keep[i:i + int(rng.integers(1, 14))] = False
            i += 1
        for k in range(RC.NI):
            if not keep[k]:
                continue
            loc = RC.to_local(RC.gts(k))
            rows.append((loc.strftime("%Y-%m-%d %H:%M"), "HALL-%s" % h, round(float(meter[k]), 1)))
    return pd.DataFrame(rows, columns=["timestamp_local", "hall", "it_load_kw"])


def work_orders(rec):
    df = rec["works"].copy()
    for c in ("planned_start", "actual_start", "actual_end"):
        df[c] = df[c].map(fmt_local)
    df["hall"] = "HALL-" + df["hall"]
    df = df[["work_order", "hall", "work_type", "title", "planned_start", "planned_hours", "actual_start", "actual_end"]]
    df.columns = ["Work order", "Hall", "Type", "Title", "Planned start", "Planned duration (h)", "Actual start",
                  "Actual finish"]
    return df


def incident_log(rec, rng):
    rows = []
    for e in rec["hall_events"]:
        if e["ts"] >= RC.T_END:
            continue
        loc = RC.to_local(e["ts"])
        txt = {"fabric": "Spine link flaps on hall fabric; jobs lost connectivity",
               "power": "Upstream supply dip; UPS transfer, hall IT load dropped",
               "cooling": "Chiller trip; hall placed in protective IT load shed",
               "storage": "Parallel filesystem metadata server failover"}[e["kind"]]
        rows.append(dict(opened_local=fmt_local(loc), hall="HALL-%s" % e["hall"], category=e["kind"], summary=txt,
                         closed_local=fmt_local(loc + dt.timedelta(minutes=e["minutes"]))))
    f0 = dt.datetime.combine(P.ROW6_FAULT[0], dt.time(15, 20))
    f1 = dt.datetime.combine(P.ROW6_FAULT[1], dt.time(11, 0))
    rows.append(dict(opened_local=fmt_local(f0), hall="HALL-A", category="cooling",
                     summary="CRAC-6 compressor fault; row 6 cold-aisle inlet above setpoint, CRAC-5 and CRAC-7 covering",
                     closed_local=fmt_local(f1)))
    rows.append(dict(opened_local=fmt_local(dt.datetime(2026, 10, 19, 11, 0)), hall="HALL-A", category="cooling",
                     summary="CRAC-6 compressor replaced; row 6 inlet back at setpoint", closed_local=fmt_local(dt.datetime(2026, 10, 19, 11, 0))))
    for m in range(1, 11):
        rows.append(dict(opened_local=fmt_local(dt.datetime(2026, m, 3, 9, 0)), hall="HALL-B", category="routine",
                         summary="Monthly generator load test (no IT impact)", closed_local=fmt_local(dt.datetime(2026, m, 3, 10, 0))))
    df = pd.DataFrame(rows)
    df["_k"] = pd.to_datetime(df["opened_local"], format="%d.%m.%Y %H:%M")
    return df.sort_values("_k").drop(columns="_k").reset_index(drop=True)


# ------------------------------------------------------------------ the profiler and the loader
PROFILE_EVERY = {"kide-34b-v1": 12500, "kide-13b-v2": 70000, "kide-13b-v2-lc32": 950, "kide-34b-v1-lc32": 1560,
                 "kide-8b-v3": 39000, "kide-13b-v3-lc16": 1900, "kide-8b-v3-lc32": 720}
MANIFEST_EVERY = 4


def profiles(rec, x, rng):
    """The profiler samples one step in every k (first pass of that step only): each data-parallel rank's forward
    and backward time, its wait at the gradient reduction and the optimizer step; the loader's manifest for every
    third sampled step lists each rank's sequences and the documents packed in them."""
    samp, man = [], []
    for r in rec["runs"]:
        if not r["profiled"]:
            continue
        k = PROFILE_EVERY[r["run_id"]]
        S_pool, F_pool, pieces = rec["cm"].stream(r["mix"], r["C"], r["rule"])
        N, L, d = P.MODELS[r["model"]]
        kf = W.kappa_flops(r["model"], r["C"])
        nodes = rec["nodes"][r["run_id"]]
        seen = set()
        count = 0
        for (tg, step, st) in r["rows"]:
            if step % k != 0 or step in seen:
                continue
            seen.add(step)
            ts = RC.gts(0, tg)
            i = min(RC.NI - 1, int(tg))
            thr = float(W.throttle(x[r["hall"]][i])) if r["hall"] == "B" else 1.0
            idx = rng.integers(0, len(S_pool), size=(r["nodes"], r["g"]))
            cost = (1.0 + P.BETA * kf * S_pool[idx]).sum(1)
            slow = np.ones(r["nodes"])
            if r["hall"] == "A" and P.ROW6_FAULT[0] <= ts.date() < P.ROW6_FAULT[1]:
                slow = np.array([P.ROW6_SLOW if n.split("-")[1] == "r06" else 1.0 for n in nodes])
            comp = cost * r["dense_s"] * 1000.0 * thr * slow * (1 + P.RANK_JITTER * rng.standard_normal(r["nodes"]))
            mx = comp.max()
            opt = r["emean"] * r["dense_s"] * 1000.0 * P.STEP_OVERHEAD * (1 + 0.03 * rng.standard_normal())
            for rank in range(r["nodes"]):
                samp.append((id_at(r, ts), int(step), fmt_ts(ts.replace(microsecond=0)), rank, nodes[rank],
                             round(float(comp[rank]), 1), round(float(mx - comp[rank] + abs(rng.normal(3.0, 1.0))), 1),
                             round(float(opt), 1)))
            if count % MANIFEST_EVERY == 0:
                for rank in range(r["nodes"]):
                    seqs = [pieces[j] for j in idx[rank]]
                    pad = [int(r["C"] - sum(p)) for p in seqs]
                    man.append(json.dumps({"run_id": id_at(r, ts), "step": int(step), "dp_rank": rank,
                                           "seq_len": r["C"], "docs": [[int(v) for v in p] for p in seqs],
                                           "pad": pad}, separators=(",", ":")))
            count += 1
    samples = pd.DataFrame(samp, columns=["run_id", "step", "ts_utc", "dp_rank", "node", "fwd_bwd_ms",
                                          "reduce_wait_ms", "optimizer_ms"])
    return samples, man


# ------------------------------------------------------------------ the benchmark
def benchmark(rec, rng):
    """The harness runs every planned configuration on a 64-node slice of its hall for 300 steps on its synthetic
    corpus (sequential packing), the hall otherwise idle, and records tokens per GPU-second."""
    cm = rec["cm"]
    seen = {}
    configs = []
    for r in rec["runs"]:
        configs.append((r["model"], r["C"], r["g"], r["hall"], r["start"] - dt.timedelta(days=int(rng.integers(8, 30)))))
    for (rid, model, hall, nodes, C, mix, rule, g, ws, we, budget, purpose) in P.ROADMAP_2027:
        configs.append((model, C, g, hall, dt.date(2026, 10, int(rng.integers(6, 29)))))
    rows = []
    for model, C, g, hall, when in configs:
        key = (model, C, g, hall)
        if key in seen:
            continue
        S, F, _ = cm.stream("synthetic", C, "sequential")
        cost = W.seq_cost(S, model, C)
        emax, emean, sd = W.step_stats(cost, 64, g, rng, steps=300)
        step = emax * W.dense_seconds(model, C, hall) * (1 + P.STEP_OVERHEAD) * (1 + 0.004 * rng.standard_normal())
        tps = 64 * g * C / step / (64 * P.GPUS_PER_NODE)
        N = P.MODELS[model][0]
        seen[key] = len(rows)
        rows.append(dict(config_id="BM-%s-%dk-g%d-%s" % (model, C // 1024, g, hall), model=model, context_tokens=C,
                         seqs_per_rank=g, hall=hall, gpu=P.HALLS[hall]["gpu"], nodes=64, steps_timed=300,
                         tokens_per_gpu_s=round(tps, 1), mfu=round(6 * N * tps / P.PEAK, 4),
                         measured_on=max(when, dt.date(2025, 11, 20)).isoformat(), harness="tpbench 1.6"))
    return pd.DataFrame(rows).sort_values(["measured_on", "config_id"]).reset_index(drop=True)


def harness_yaml():
    med, sig, cap = P.BENCH_CORPUS
    return ("# tpbench 1.6: the infrastructure team's throughput harness\n"
            "slice_nodes: 64\n"
            "warmup_steps: 50\n"
            "timed_steps: 300\n"
            "metric: tokens_per_gpu_s   # real tokens over wall-clock, timed steps only\n"
            "corpus:\n"
            "  kind: random_tokens\n"
            "  doc_length: {distribution: lognormal, median_tokens: %d, sigma: %.1f, max_tokens: %d}\n"
            "  seed: 1729\n"
            "packing: sequential   # documents end to end, cut at the sequence length, document-masked attention\n"
            "checkpointing: off\n"
            "hall_load: other jobs drained from the slice's rows during timing\n" % (med, sig, cap))


# ------------------------------------------------------------------ the 2027 inputs
def length_sample(rng, per_source=20000):
    """The data team's October 2026 sample of document lengths, per source, from the cleaned corpora both years'
    mixes draw on."""
    rows = []
    srcs = sorted({s for m in P.MIXES for s in P.MIXES[m]})
    for s in srcs:
        med, sig, cap = P.SOURCES[s]
        l = np.minimum(rng.lognormal(math.log(med), sig, per_source), cap).astype(int) + 1
        for i, v in enumerate(l):
            rows.append((s, "%s-%06d" % (s[:4], i + 1), int(v)))
    return pd.DataFrame(rows, columns=["source", "doc_id", "length_tokens"])


def mixes():
    rows = []
    for m, d in P.MIXES.items():
        for s, sh in sorted(d.items()):
            rows.append((m, 2026 if m.endswith("-26") else 2027, s, sh))
    return pd.DataFrame(rows, columns=["mix_id", "year", "source", "token_share"])


def config_yaml(run):
    (rid, model, hall, nodes, C, mix, rule, g, ws, we, budget, purpose) = run
    N, L, d = P.MODELS[model]
    lines = ["# %s: %s" % (rid, purpose), "model:", "  family: kide", "  size: %s" % model,
             "  params: %d" % int(N), "  layers: %d" % L, "  d_model: %d" % d, "  vocab: %d" % P.VOCAB,
             "parallelism:", "  tensor: 8", "  data: %d" % nodes, "  nodes: %d" % nodes,
             "batch:", "  seq_len: %d" % C, "  seqs_per_rank: %d" % g,
             "  global_batch_seqs: %d" % (nodes * g),
             "data:", "  mix: %s" % mix, "  order: shuffled documents, fixed seed",
             "  packing: %s" % rule]
    if rule == "best_fit":
        lines += ["  best_fit:", "    keep_whole_up_to: %d   # longer documents cut into seq_len pieces" % C,
                  "    open_sequences: 64", "    placement: least room that fits, in arrival order",
                  "    close: fullest open sequence when more than 64 are open", "    remainder: padding"]
    else:
        lines += ["  sequential: documents end to end, cut at seq_len"]
    lines += ["  dealing: packed sequences to data-parallel ranks in turn",
              "attention: document-masked (flash varlen)", "checkpoint:", "  every_minutes: %d" % P.CKPT_INTERVAL_MIN,
              "  async: false", "optimizer: adamw", "precision: bf16",
              "reservation:", "  hall: %s" % hall, "  window_start: %s" % ws, "  window_end: %s" % we,
              "  token_budget: %d" % int(budget)]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ distractors
def checkpoint_evals(rec, rng):
    rows = []
    for r in rec["runs"]:
        if r["run_id"].startswith("abl-") or not r["rows"]:
            continue
        for frac in (0.25, 0.5, 0.75, 1.0):
            if r["end_ts"] is None and frac > 0.75:
                continue
            base = {"8B": 0.52, "13B": 0.57, "34B": 0.64, "70B": 0.70}[r["model"]]
            rows.append(dict(run_id=r["run_id"], checkpoint_tokens=int(r["budget"] * frac) if r["budget"] < 9e14 else int(1.2e13 * frac),
                             suite="kd-eval 0.9", mmlu_5shot=round(base + 0.06 * frac + rng.normal(0, 0.006), 3),
                             gsm8k=round(base - 0.12 + 0.11 * frac + rng.normal(0, 0.01), 3),
                             humaneval=round(base - 0.2 + 0.1 * frac + rng.normal(0, 0.012), 3),
                             longbench=round(base - 0.15 + (0.08 if "-lc" in r["run_id"] else 0.0) + rng.normal(0, 0.01), 3)))
    return pd.DataFrame(rows)


def energy_invoices(rec):
    rows = []
    for h, hp in P.HALLS.items():
        d = np.minimum(rec["draw"][h], hp["contract_kw"])
        for m in range(1, 11):
            a = RC.gi(dt.datetime(2026, m, 1))
            b = RC.gi(dt.datetime(2026, m + 1, 1)) if m < 10 else RC.NI
            kwh = float(d[a:b].sum() * 300 / 3600)
            rows.append(dict(invoice="PV-INV-26%02d-%s" % (m, h), hall="HALL-%s" % h, month="2026-%02d" % m,
                             it_energy_mwh=round(kwh / 1000, 1), pue=round(1.17 + 0.03 * math.cos(m / 12 * 2 * math.pi), 3),
                             price_eur_mwh=round(71 + 9 * math.cos((m - 1) / 12 * 2 * math.pi), 2)))
    df = pd.DataFrame(rows)
    df["energy_charge_eur"] = (df["it_energy_mwh"] * df["pue"] * df["price_eur_mwh"]).round(2)
    return df
