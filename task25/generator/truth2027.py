"""The H1 2027 roadmap replayed under the world's true process, many times: what each run will really take. This is
the truth the golden (built from the shipped files alone) is checked against; nothing here ships."""
import datetime as dt
import math

import numpy as np

import params as P
import records as RC
import world as W

T0 = dt.datetime(2027, 1, 1)
DAYS = 200
NI = DAYS * 288


def gi(ts):
    return int((ts - T0).total_seconds() // 300)


def run_specs(budgets=None, cm=None, rng=None, sources=None, beta=P.BETA, steps=2500):
    """Per 2027 run: the slowest-rank and mean-rank step under the true length distributions, the fill, the dense
    time and the tokens per step."""
    rng = rng or np.random.default_rng(P.SEED + 101)
    out = []
    for (rid, model, hall, nodes, C, mix, rule, g, ws, we, budget, purpose) in P.ROADMAP_2027:
        ntok = 8.0e8 if C >= 32768 else 4.0e8
        docs = W.draw_docs(P.MIXES[mix], ntok, rng, sources=sources)
        S, F, _ = W.pack(docs, C, rule)
        cost = W.seq_cost(S, model, C, beta=beta)
        emax, emean, sd = W.step_stats(cost, nodes, g, rng, steps=steps)
        dense = W.dense_seconds(model, C, hall)
        b = budgets[rid] if budgets else budget
        out.append(dict(run_id=rid, model=model, hall=hall, nodes=nodes, C=C, mix=mix, rule=rule, g=g,
                        ws=dt.date.fromisoformat(ws), we=dt.date.fromisoformat(we), budget=b, emax=emax,
                        emean=emean, fill=float(F.mean()), dense_s=dense,
                        step_s=emax * dense * (1 + P.STEP_OVERHEAD), tok_step=nodes * g * C * float(F.mean())))
    return out


def works_windows(rng, ratio=True):
    """The 2027 calendar's works as they will run: actual length = planned times a draw of the overrun ratio."""
    out = []
    for wid, hall, typ, start_local, hours, title in P.WORKS_2027:
        med, sig = P.WORKS_RATIO[typ]
        rr = float(np.exp(math.log(med) + sig * rng.standard_normal())) if ratio else 1.0
        a = RC.to_utc(start_local)
        out.append(dict(hall=hall, a=a, b=a + dt.timedelta(hours=hours * rr), wid=wid))
    return out


def replay_once(specs, rng, pool_share=P.POOL_BUSY, throttle_on=True, works_ratio=True, overrun_extends=True):
    """One draw of H1 2027: interruptions, works and the hall B load, with each run kept on its block until it
    finishes. Returns days from each window's 00:00 UTC to its token budget."""
    works = works_windows(rng, ratio=works_ratio)
    hall_ev = []
    for h in P.HALLS:
        t = 0.0
        while True:
            t += rng.exponential(1.0 / P.HALL_EVENT_PER_DAY[h])
            if t >= DAYS:
                break
            hall_ev.append(dict(hall=h, ts=T0 + dt.timedelta(days=t), minutes=float(rng.choice([25, 40, 60, 95, 140]))))
    runs = []
    for s in specs:
        r = dict(s)
        r["launch"] = dt.datetime.combine(r["ws"], dt.time(0)) + dt.timedelta(minutes=float(rng.uniform(*P.LAUNCH_DELAY_MIN)))
        r["plan_end"] = r["we"]
        r["start"] = r["ws"]
        r["events"] = _events(r, rng, hall_ev, works)
        runs.append(r)
    ends = {r["run_id"]: dt.datetime.combine(r["we"], dt.time(0)) for r in runs}
    for _ in range(4):
        x = hall_x(runs, ends, rng_seed=int(rng.integers(1 << 30)), pool_share=pool_share) if throttle_on else \
            {h: np.zeros(NI) for h in P.HALLS}
        for r in runs:
            d = _progress(r, x)
            ends[r["run_id"]] = r["launch"] + dt.timedelta(days=d) if overrun_extends else \
                max(r["launch"] + dt.timedelta(days=d), dt.datetime.combine(r["we"], dt.time(0)))
    return {r["run_id"]: (ends[r["run_id"]] - dt.datetime.combine(r["ws"], dt.time(0))).total_seconds() / 86400
            for r in runs}


def _events(r, rng, hall_ev, works):
    t0 = r["launch"]
    days = 160.0
    ev = []
    lam_hw = P.NODE_FAIL_PER_DAY[r["hall"]] * r["nodes"]
    lam_sw = P.SOFT_FAIL_PER_DAY * min(1.0, (r["nodes"] / 256.0) ** 0.5)
    for kind, lam in (("hw_node", lam_hw), ("sw_crash", lam_sw)):
        t = 0.0
        while True:
            t += rng.exponential(1.0 / lam)
            if t >= days:
                break
            ev.append(dict(ts=t0 + dt.timedelta(days=t), kind=kind))
    for e in hall_ev:
        if e["hall"] == r["hall"] and e["ts"] > t0:
            ev.append(dict(ts=e["ts"], kind="hall_event", hall_minutes=e["minutes"]))
    for w in works:
        if w["hall"] == r["hall"] and w["b"] > t0:
            ev.append(dict(ts=max(w["a"], t0), kind="works", until=w["b"]))
    ev.sort(key=lambda e: e["ts"])
    gb = W.ckpt_gb(r["model"])
    for e in ev:
        base = float(np.exp(math.log(P.RESTART_MIN["median"]) + P.RESTART_MIN["sigma"] * rng.standard_normal()))
        load = gb / P.CKPT_LOAD_GBPS / 60.0
        if e["kind"] == "hall_event":
            e["down_min"] = e["hall_minutes"] + base + load
        elif e["kind"] == "works":
            e["down_min"] = (e["until"] - e["ts"]).total_seconds() / 60 + base + load
        else:
            e["down_min"] = base + load + (float(rng.uniform(5, 14)) if e["kind"] == "hw_node" else 0.0)
    return ev


def hall_x(runs, ends, rng_seed, pool_share=P.POOL_BUSY):
    rng = np.random.default_rng(rng_seed)
    x = {}
    for h, hp in P.HALLS.items():
        N = hp["rows"] * hp["slots"]
        held = np.zeros(NI)
        kw = np.zeros(NI)
        for r in runs:
            if r["hall"] != h:
                continue
            a = max(0, gi(dt.datetime.combine(r["ws"], dt.time(0))))
            b = min(NI, max(gi(dt.datetime.combine(r["we"], dt.time(0))), gi(ends[r["run_id"]]) + 1))
            held[a:b] += r["nodes"]
            kw[a:b] += r["nodes"] * hp["node_kw"] * P.DRAW_BY_MODEL[r["model"]]
        free = N - held
        idx = np.arange(NI)
        dates = [T0 + dt.timedelta(days=d) for d in range(DAYS)]
        wk = np.repeat([P.POOL_WEEKLY[d.weekday()] for d in dates], 288)
        mo = np.repeat([P.POOL_MONTHLY[d.month] for d in dates], 288)
        hour = (idx * 300 / 3600.0) % 24
        diurnal = 1 + 0.05 * np.sin((hour - 9) / 24 * 2 * math.pi)
        share = np.clip(pool_share[h] * wk * mo * diurnal, 0.05, 0.98)
        pool = free * share
        d = kw + pool * hp["node_kw"] * 0.95 + (N - held - pool) * hp["idle_kw"] + hp["infra_kw"]
        x[h] = np.maximum(0.0, d / hp["contract_kw"] - 1.0)
    return x


def _progress(r, x):
    """Days from launch to the budget (continuous, on the grid), stops rolled back to the last checkpoint."""
    a = gi(r["launch"])
    thr = W.throttle(x[r["hall"]]) if r["hall"] == "B" else np.ones(NI)
    rate = 300.0 / (r["step_s"] * thr)
    target = r["budget"] / r["tok_step"]
    cum = 0.0
    cur = a
    ck_every = int(P.CKPT_INTERVAL_MIN * 60 / 300)
    evs = [e for e in r["events"] if gi(e["ts"]) >= a]
    for k in range(len(evs) + 1):
        stop = gi(evs[k]["ts"]) if k < len(evs) else NI
        if stop <= cur:
            if k < len(evs):
                cur = max(cur, stop + int(math.ceil(evs[k]["down_min"] / 5.0)))
            continue
        seg = rate[cur:stop]
        cs = cum + np.cumsum(seg)
        if cs[-1] >= target:
            j = int(np.searchsorted(cs, target))
            frac = (target - (cs[j - 1] if j > 0 else cum)) / seg[j]
            return (cur + j + frac - a) * 300 / 86400 + (r["launch"] - dt.datetime.combine(r["ws"], dt.time(0))).total_seconds() * 0 / 86400
        n_ck = (stop - cur) // ck_every
        cum = cs[n_ck * ck_every - 1] if n_ck > 0 else cum
        if k < len(evs):
            cur = stop + int(math.ceil(evs[k]["down_min"] / 5.0))
    return 999.0


def replay(specs, n=60, seed=P.SEED + 303, **kw):
    rng = np.random.default_rng(seed)
    acc = {s["run_id"]: [] for s in specs}
    for _ in range(n):
        d = replay_once(specs, rng, **kw)
        for k, v in d.items():
            acc[k].append(v)
    return {k: np.array(v) for k, v in acc.items()}
