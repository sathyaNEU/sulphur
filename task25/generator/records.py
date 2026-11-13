"""The 2026 record, simulated as the systems wrote it: the run registry, node allocations, the trainer's step logs
(replayed steps after every rollback, the logger's re-sent buffer, a counter reset, three renames), the profiler's
per-rank samples with the loader's packing manifests, interruptions, the scheduler's node states, the provider's hall
meters, work orders and incident log, and the infrastructure team's throughput benchmark."""
import datetime as dt
import math
import zlib

import numpy as np
import pandas as pd

import params as P
import world as W

STEP_S = 300                      # the simulation grid: five minutes
T0 = dt.datetime(2026, 1, 1)
T_END = dt.datetime(2026, 11, 1)  # the record ends at the start of 1 November (UTC)
NI = int((T_END - T0).total_seconds() // STEP_S)


def gi(ts):
    return int((ts - T0).total_seconds() // STEP_S)


def gts(i, frac=0.0):
    return T0 + dt.timedelta(seconds=STEP_S * (i + frac))


# ------------------------------------------------------------------ cost statistics per configuration
class CostModel:
    """Per (model, context, mix, packing rule): a packed stream and its sequence-cost pool."""

    def __init__(self, rng):
        self.rng = rng
        self.cache = {}

    def stream(self, mix, C, rule, ntok=None):
        key = (mix, C, rule)
        if key not in self.cache:
            mixd = P.MIXES[mix] if mix != "synthetic" else None
            ntok = ntok or (6.0e8 if C >= 32768 else 3.0e8)
            if mixd is None:
                med, sig, cap = P.BENCH_CORPUS
                docs = W.draw_docs({"synthetic": 1.0}, ntok, self.rng, sources={"synthetic": (med, sig, cap)})
            else:
                docs = W.draw_docs(mixd, ntok, self.rng)
            S, F, pieces = W.pack(docs, C, rule, keep=True)
            self.cache[key] = (S, F, pieces)
        return self.cache[key]

    def stats(self, model, mix, C, rule, D, g, steps=1500):
        S, F, _ = self.stream(mix, C, rule)
        cost = W.seq_cost(S, model, C)
        emax, emean, sd = W.step_stats(cost, D, g, self.rng, steps=steps)
        return dict(emax=emax, emean=emean, sd=sd, fill=float(F.mean()), S_mean=float(S.mean()))


# ------------------------------------------------------------------ the registry
def ablation_runs(rng):
    out = []
    days0 = (P.RECORD_END - P.RECORD_START).days
    for k in range(P.N_ABLATIONS):
        model = rng.choice(["1B", "3B", "8B"], p=[0.40, 0.35, 0.25])
        nodes = int(rng.choice([8, 16, 32], p=[0.4, 0.4, 0.2]))
        C = int(rng.choice([4096, 8192], p=[0.35, 0.65]))
        hall = "A" if rng.random() < 0.6 else "B"
        start = P.RECORD_START + dt.timedelta(days=int(rng.integers(3, days0 - 12)))
        dur = int(rng.integers(1, 7))
        g = int(rng.choice([8, 16]))
        tag = rng.choice(["mix", "tok", "lr", "dedup", "filt", "sched"])
        rid = "abl-%s-%s-%02d" % (model.lower(), tag, k + 1)
        out.append((rid, model, hall, nodes, C, "abl-26", "sequential", g, start.isoformat(),
                    (start + dt.timedelta(days=dur)).isoformat(), False))
    return out


def assign_nodes(runs, rng):
    """Each run gets a node set for its window; registered runs take contiguous blocks first, ablations then take
    scattered nodes free over their own windows (moved later a day at a time when the hall is full). kide-8b-v3 sits
    on hall A rows 4 to 7 (row 6 among them)."""
    names = {h: W.node_names(h) for h in P.HALLS}
    occ = {h: {n: [] for n in names[h]} for h in P.HALLS}

    def free_for(h, s, e):
        return [n for n in names[h] if all(e <= a or s >= b for a, b in occ[h][n])]

    out = {}
    order = sorted([r for r in runs if not r["run_id"].startswith("abl-")], key=lambda r: r["start"]) + \
        sorted([r for r in runs if r["run_id"].startswith("abl-")], key=lambda r: r["start"])
    for r in order:
        h = r["hall"]
        while True:
            s, e = r["start"], r["plan_end"] + dt.timedelta(days=2)
            free = free_for(h, s, e)
            if len(free) >= r["nodes"]:
                break
            assert r["run_id"].startswith("abl-"), r["run_id"]
            r["start"] += dt.timedelta(days=1)
            r["plan_end"] += dt.timedelta(days=1)
        if r["run_id"] == "kide-8b-v3":
            pick = [n for n in free if n.split("-")[1] in ("r04", "r05", "r06", "r07")][: r["nodes"]]
        elif r["run_id"].startswith("abl-"):
            idx = sorted(rng.choice(len(free), size=r["nodes"], replace=False))
            pick = [free[i] for i in idx]
        else:
            pick = free[: r["nodes"]]
        assert len(pick) == r["nodes"], r["run_id"]
        for n in pick:
            occ[h][n].append((s, e))
        out[r["run_id"]] = pick
    return out


# ------------------------------------------------------------------ hall events, works, incidents
def works_2026(rng):
    """The provider's 2025 and 2026 work orders (Helsinki local times), planned against actual."""
    rows = []
    plan = [
        ("PV-25-031", "A", "major", dt.datetime(2025, 4, 14, 6, 0), 24.0, "Hall A UPS module replacement"),
        ("PV-25-047", "B", "major", dt.datetime(2025, 6, 2, 6, 0), 36.0, "Hall B busway extension, pod 2"),
        ("PV-25-058", "A", "major", dt.datetime(2025, 9, 8, 6, 0), 48.0, "Hall A cooling loop flush and valve works"),
        ("PV-25-066", "B", "major", dt.datetime(2025, 11, 17, 6, 0), 72.0, "Hall B pod 2 commissioning tie-in"),
        ("PV-26-008", "B", "major", dt.datetime(2026, 2, 23, 6, 0), 30.0, "Hall B spine switch firmware, both pods"),
        ("PV-26-019", "A", "major", dt.datetime(2026, 5, 4, 6, 0), 36.0, "Hall A PDU replacement, rows 9 to 12"),
        ("PV-26-027", "B", "major", dt.datetime(2026, 8, 3, 6, 0), 48.0, "Hall B chilled-water pump replacement"),
        ("PV-26-031", "A", "major", dt.datetime(2026, 10, 5, 6, 0), 24.0, "Hall A fire-suppression panel upgrade"),
    ]
    for y in (2025, 2026):
        for q, m in enumerate((2, 5, 8, 11)):
            for h, day0 in (("A", 10), ("B", 11)):
                d = dt.datetime(y, m, day0, 7, 0)
                if dt.datetime(y, m, 1) > dt.datetime(2026, 10, 31):
                    continue
                plan.append(("PV-%02d-%03d" % (y % 100, 100 + q * 2 + (h == "B")), h, "routine", d, 6.0,
                             "Hall %s quarterly UPS inspection" % h))
    for wid, h, typ, start, hours, title in sorted(plan, key=lambda x: x[3]):
        med, sig = P.WORKS_RATIO[typ]
        ratio = float(np.exp(math.log(med) + sig * rng.standard_normal()))
        delay = float(rng.choice([0, 0, 0, 15, 30, 45]))
        a_start = start + dt.timedelta(minutes=delay)
        a_end = a_start + dt.timedelta(hours=hours * ratio)
        rows.append(dict(work_order=wid, hall=h, work_type=typ, title=title,
                         planned_start=start, planned_hours=hours, actual_start=a_start,
                         actual_end=a_end.replace(second=0, microsecond=0)))
    return pd.DataFrame(rows)


HELSINKI_OFFSET = {"winter": 2, "summer": 3}


def helsinki_offset(ts_utc):
    """Hours Helsinki local time is ahead of UTC (EET/EEST, changes on the last Sundays of March and October)."""
    y = ts_utc.year

    def last_sunday(month):
        d = dt.datetime(y, month, 31 if month in (3, 10) else 30)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d.replace(hour=1)

    return 3 if last_sunday(3) <= ts_utc < last_sunday(10) else 2


def to_local(ts_utc):
    return ts_utc + dt.timedelta(hours=helsinki_offset(ts_utc))


def to_utc(ts_local):
    # local to UTC: try the summer offset first, check it round-trips
    for off in (3, 2):
        u = ts_local - dt.timedelta(hours=off)
        if helsinki_offset(u) == off:
            return u
    return ts_local - dt.timedelta(hours=2)


def hall_events(rng):
    """Facility or fabric events that stop every job in a hall (UTC), with how long the hall stays down."""
    ev = []
    for h in P.HALLS:
        t = 0.0
        days = (T_END - T0).days
        while True:
            t += rng.exponential(1.0 / P.HALL_EVENT_PER_DAY[h])
            if t >= days:
                break
            ts = T0 + dt.timedelta(days=t)
            dur = float(rng.choice([25, 40, 60, 95, 140]))
            kind = rng.choice(["fabric", "power", "cooling", "storage"], p=[0.35, 0.25, 0.2, 0.2])
            ev.append(dict(hall=h, ts=ts.replace(second=0, microsecond=0), minutes=dur, kind=kind))
    return ev


# ------------------------------------------------------------------ the simulation
def simulate(seed=P.SEED):
    rng = np.random.default_rng(seed)
    cm = CostModel(np.random.default_rng(seed + 1))
    spec = list(P.RUNS_2026) + ablation_runs(rng)
    runs = []
    for (rid, model, hall, nodes, C, mix, rule, g, start, end, prof) in spec:
        s = dt.date.fromisoformat(start)
        e = dt.date.fromisoformat(end) if end else dt.date(2026, 12, 20)
        runs.append(dict(run_id=rid, model=model, hall=hall, nodes=nodes, C=C, mix=mix, rule=rule, g=g,
                         start=s, plan_end=e, profiled=prof, live=end is None))
    nodes = assign_nodes(runs, rng)
    works = works_2026(rng)
    hevents = hall_events(rng)
    works_utc = []
    for _, w in works.iterrows():
        a, b = to_utc(w.actual_start), to_utc(w.actual_end)
        if b > T0 and a < T_END:
            works_utc.append(dict(hall=w.hall, a=a, b=b, wid=w.work_order))
    # cost statistics and budgets
    for r in runs:
        st = cm.stats(r["model"], r["mix"], r["C"], r["rule"], r["nodes"], r["g"])
        r.update(st)
        r["dense_s"] = W.dense_seconds(r["model"], r["C"], r["hall"])
        r["step_s"] = r["emax"] * r["dense_s"] * (1 + P.STEP_OVERHEAD) * 1.0
        r["tok_step"] = r["nodes"] * r["g"] * r["C"] * r["fill"]
        plan_days = (r["plan_end"] - r["start"]).days
        r["budget"] = float(round(plan_days * 86400 / r["step_s"] * r["tok_step"] * 0.925, -9)) if not r["live"] \
            else 9.9e14
        r["log_every"] = min(P.LOG_STEPS, key=lambda n: abs(n * r["step_s"] - P.LOG_TARGET_S))
        r["launch"] = dt.datetime.combine(r["start"], dt.time(0, 0)) + dt.timedelta(
            minutes=float(rng.uniform(*P.LAUNCH_DELAY_MIN)))
    # interruptions per run (independent of throttle), hall events shared
    for r in runs:
        r["events"] = interruptions(r, rng, hevents, works_utc)
    # two passes: busy nodes -> throttle -> progress -> ends -> busy nodes again
    ends = {r["run_id"]: dt.datetime.combine(r["plan_end"], dt.time(12, 0)) for r in runs}
    for _ in range(3):
        busy, draw, x = hall_load(runs, ends, nodes, rng_seed=seed + 7)
        for r in runs:
            progress(r, x, nodes[r["run_id"]], keep_rows=False)
            ends[r["run_id"]] = r["end_ts"] if r["end_ts"] else T_END
    busy, draw, x = hall_load(runs, ends, nodes, rng_seed=seed + 7)
    rng_log = np.random.default_rng(seed + 11)
    for r in runs:
        progress(r, x, nodes[r["run_id"]], keep_rows=True, rng=rng_log)
    rec = dict(runs=runs, nodes=nodes, works=works, hall_events=hevents, busy=busy, draw=draw, x=x, cm=cm,
               works_utc=works_utc)
    return rec


def interruptions(r, rng, hevents, works_utc):
    """Every stop a run meets between its launch and the end of the record: node faults (Poisson per node-day),
    software crashes (per run-day, more often on wide runs), the hall's facility events, and provider works."""
    t0 = r["launch"]
    t1 = min(T_END, dt.datetime.combine(r["plan_end"], dt.time(0)) + dt.timedelta(days=30))
    days = (t1 - t0).total_seconds() / 86400
    ev = []
    lam_hw = P.NODE_FAIL_PER_DAY[r["hall"]] * r["nodes"]
    lam_sw = P.SOFT_FAIL_PER_DAY * min(1.0, (r["nodes"] / 256.0) ** 0.5)
    for kind, lam in (("hw_node", lam_hw), ("sw_crash", lam_sw)):
        t = 0.0
        while True:
            t += rng.exponential(1.0 / lam) if lam > 0 else 1e9
            if t >= days:
                break
            ev.append(dict(ts=t0 + dt.timedelta(days=t), kind=kind))
    for e in hevents:
        if e["hall"] == r["hall"] and t0 < e["ts"] < t1:
            ev.append(dict(ts=e["ts"], kind="hall_event", hall_minutes=e["minutes"], cause=e["kind"]))
    for w in works_utc:
        if w["hall"] == r["hall"] and w["b"] > t0 and w["a"] < t1:
            ev.append(dict(ts=max(w["a"], t0), kind="works", until=w["b"], wid=w["wid"]))
    ev.sort(key=lambda e: e["ts"])
    gb = W.ckpt_gb(r["model"])
    for e in ev:
        base = float(np.exp(math.log(P.RESTART_MIN["median"]) + P.RESTART_MIN["sigma"] * rng.standard_normal()))
        load = gb / P.CKPT_LOAD_GBPS / 60.0
        extra = {"hw_node": float(rng.uniform(5, 14)), "sw_crash": 0.0}.get(e["kind"], 0.0)
        if e["kind"] == "hall_event":
            down = e["hall_minutes"] + base + load
        elif e["kind"] == "works":
            down = (e["until"] - e["ts"]).total_seconds() / 60 + base + load
        else:
            down = base + load + extra
        e["down_min"] = down
        e["code"] = {"hw_node": rng.choice(["Xid 79", "Xid 48", "ECC DBE", "NVLink CRC", "PSU fault", "node unreachable"]),
                     "sw_crash": rng.choice(["NCCL timeout", "CUDA OOM", "loader stall", "NaN in loss", "segfault"]),
                     "hall_event": "hall stop", "works": "provider works"}[e["kind"]]
    return ev


def hall_load(runs, ends, nodes, rng_seed):
    """Busy nodes, would-be draw and excess over contract per hall on the five-minute grid. Registered and ablation
    runs hold their nodes from launch to end (drawing far less while restarting); the research pool takes a weekly
    and monthly patterned share of the nodes no run holds."""
    rng = np.random.default_rng(rng_seed)
    busy, draw, x = {}, {}, {}
    for h, hp in P.HALLS.items():
        N = hp["rows"] * hp["slots"]
        held = np.zeros(NI)
        run_kw = np.zeros(NI)
        for r in runs:
            if r["hall"] != h:
                continue
            a = max(0, gi(r["launch"]))
            b = min(NI, gi(ends[r["run_id"]]) + 1)
            if b <= a:
                continue
            up = np.ones(b - a)
            for e in r["events"]:
                i = gi(e["ts"]) - a
                j = i + int(math.ceil(e["down_min"] * 60 / STEP_S))
                if 0 <= i < len(up):
                    up[i:max(i + 1, j)] = 0.0
            held[a:b] += r["nodes"]
            kw = hp["node_kw"] * P.DRAW_BY_MODEL[r["model"]]
            run_kw[a:b] += r["nodes"] * (up * kw + (1 - up) * hp["idle_kw"] * 1.6)
        free = N - held
        days = np.arange(NI) * STEP_S / 86400.0
        dates = [T0 + dt.timedelta(days=float(d)) for d in days[::288]]
        wk = np.repeat([P.POOL_WEEKLY[d.weekday()] for d in dates], 288)[:NI]
        mo = np.repeat([P.POOL_MONTHLY[d.month] for d in dates], 288)[:NI]
        hour = (np.arange(NI) * STEP_S / 3600.0) % 24
        diurnal = 1 + 0.05 * np.sin((hour - 9) / 24 * 2 * math.pi)
        ar = np.zeros(NI)
        e = rng.standard_normal(NI) * 0.012
        for i in range(1, NI):
            ar[i] = 0.995 * ar[i - 1] + e[i]
        share = np.clip(P.POOL_BUSY[h] * wk * mo * diurnal * (1 + ar), 0.05, 0.98)
        pool = np.floor(free * share + rng.random(NI))
        pool_kw = pool * hp["node_kw"] * 0.95
        idle = N - held - pool
        d = run_kw + pool_kw + idle * hp["idle_kw"] + hp["infra_kw"]
        busy[h] = held + pool
        draw[h] = d
        x[h] = np.maximum(0.0, d / hp["contract_kw"] - 1.0)
    return busy, draw, x


def progress(r, x, run_nodes, keep_rows=False, rng=None):
    """A run's progress on the grid: the slowest-rank step stretched by the hall's throttle and, for hall A row 6
    nodes in the cooling fault, their slowdown; rolled back to the last checkpoint at every stop; it ends when its
    token budget is reached or the record ends. With keep_rows, the logger's rows and the stops are kept."""
    a = gi(r["launch"])
    thr = W.throttle(x[r["hall"]]) if r["hall"] == "B" else np.ones(NI)
    slow = np.ones(NI)
    if r["hall"] == "A" and any(n.split("-")[1] == "r06" for n in run_nodes):
        f0, f1 = gi(dt.datetime.combine(P.ROW6_FAULT[0], dt.time(13, 20))), gi(dt.datetime.combine(P.ROW6_FAULT[1], dt.time(9, 0)))
        slow[f0:f1] = P.ROW6_SLOW
    drift_rng = np.random.default_rng(zlib.crc32(r["run_id"].encode()) % (1 << 31))
    e = drift_rng.standard_normal(NI) * 0.0011
    drift = np.empty(NI)
    acc = 0.0
    for i in range(NI):
        acc = 0.9993 * acc + e[i]
        drift[i] = acc
    step_s = r["step_s"] * thr * slow * (1.0 + drift)     # seconds per step on the grid
    rate = STEP_S / step_s                                # steps per grid interval
    tok_step = r["tok_step"]
    target_steps = r["budget"] / tok_step
    cum_counter = 0.0            # the trainer's step counter (rolls back)
    stops = []
    rows = []
    cur = a
    done = False
    end_i = None
    evs = [e for e in r["events"] if gi(e["ts"]) >= a]
    ckpt_every = int(P.CKPT_INTERVAL_MIN * 60 / STEP_S)
    srng = np.random.default_rng((zlib.crc32(r["run_id"].encode()) + 17) % (1 << 31))
    cur += int(math.ceil(float(srng.uniform(3, 9)) / 5.0))          # start-up after the launch
    for k in range(len(evs) + 1):
        stop_i = gi(evs[k]["ts"]) if k < len(evs) else NI
        stop_i = min(stop_i, NI)
        if stop_i <= cur:
            if k < len(evs):
                cur = max(cur, stop_i + int(math.ceil(evs[k]["down_min"] * 60 / STEP_S)))
            continue
        seg = rate[cur:stop_i]
        cs = cum_counter + np.cumsum(seg)
        if cs[-1] >= target_steps:
            j = int(np.searchsorted(cs, target_steps))
            frac = (target_steps - (cs[j - 1] if j > 0 else cum_counter)) / seg[j]
            end_i = cur + j + frac
            if keep_rows:
                emit_rows(r, rows, cur, cum_counter, cs[: j + 1], seg[: j + 1], step_s, target_steps, rng)
            cum_counter = target_steps
            done = True
            break
        if k == len(evs):
            # the record ends with the run still live
            if keep_rows:
                emit_rows(r, rows, cur, cum_counter, cs, seg, step_s, cs[-1], rng)
            cum_counter = float(cs[-1])
            break
        # a stop: roll back to the last checkpoint (taken every ckpt_every intervals since the segment began)
        n_ck = (stop_i - cur) // ckpt_every
        ck_counter = cs[n_ck * ckpt_every - 1] if n_ck > 0 else cum_counter
        ck_counter = math.floor(ck_counter / 100.0) * 100.0 if n_ck > 0 else cum_counter
        if keep_rows:
            emit_rows(r, rows, cur, cum_counter, cs, seg, step_s, cs[-1], rng)
            e = evs[k]
            stops.append(dict(ts_fail=gts(stop_i, rng.random()), kind=e["kind"], code=e["code"],
                              fail_step=int(cs[-1]), ckpt_step=int(ck_counter), down_min=e["down_min"],
                              wid=e.get("wid")))
        cum_counter = ck_counter
        if k < len(evs):
            cur = stop_i + int(math.ceil(evs[k]["down_min"] * 60 / STEP_S))
    if done:
        end_i = end_i + float(srng.uniform(12, 25)) * 60 / STEP_S      # the final checkpoint and shutdown
    r["end_ts"] = gts(end_i) if done else None
    r["steps_done"] = cum_counter
    if keep_rows:
        r["rows"] = rows
        r["stops"] = stops


def emit_rows(r, rows, cur, start_counter, cs, seg, step_s, last_counter, rng):
    """The logger writes one row every 100 steps of the counter, with the mean step time of those 100 steps."""
    n = float(r["log_every"])
    first = math.floor(start_counter / n) * n + n
    if first > last_counter:
        return
    marks = np.arange(first, math.floor(last_counter / n) * n + 1, n)
    if len(marks) == 0:
        return
    cs_full = np.concatenate([[start_counter], cs])
    idx = np.searchsorted(cs_full, marks)      # grid position of each mark
    idx = np.clip(idx, 1, len(cs_full) - 1)
    lo = cs_full[idx - 1]
    frac = (marks - lo) / np.maximum(seg[idx - 1], 1e-9)
    times = cur + (idx - 1) + frac
    st = step_s[(cur + idx - 1).astype(int)]
    for m, t, s in zip(marks, times, st):
        rows.append((float(t), int(m), float(s)))
