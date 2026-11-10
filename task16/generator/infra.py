"""The systems around the training jobs: the departmental cluster's scheduler, the tracking server, the checkpoint
store and the programme's benchmark server.

The arithmetic of a job is real (trainer.py). What this module adds is where and when it ran: the node, the queue
wait, how long a step took on that node, when the scheduler took the node back, and the ids each system gave things.
Those are simulated from a small process (six GPU nodes of two generations, batches submitted by a script, a
preemptible partition, a 24 hour walltime), because the lab's real cluster is not ours to ship.
"""
import datetime as dt
import hashlib

import numpy as np

import params as P
import world as W

UTC = dt.timezone.utc
NODES = [("hugin-g01", 1.00), ("hugin-g02", 1.00), ("hugin-g03", 1.02), ("hugin-g04", 0.99),
         ("munin-g01", 1.36), ("munin-g02", 1.41)]
STEP_SECONDS = {64: 1.86, 128: 2.07, 256: 2.61, 512: 4.42, 1024: 9.35}
EVAL_SECONDS = 37.0
WALLTIME = 24 * 3600
USER = {"ladder": "maas", "lrcheck": "maas", "wide": "maas", "vend": "maas"}

# when each batch of the pilot went onto the queue (UTC); a batch is submitted by a script, a few seconds apart
BATCH_START = {
    ("ladder", 64): dt.datetime(2026, 9, 28, 8, 41, 12, tzinfo=UTC),
    ("ladder", 128): dt.datetime(2026, 9, 30, 13, 5, 47, tzinfo=UTC),
    ("ladder", 256): dt.datetime(2026, 10, 5, 7, 58, 30, tzinfo=UTC),
    ("lrcheck", 0): dt.datetime(2026, 10, 12, 9, 14, 3, tzinfo=UTC),
    ("lrcheck", 1): dt.datetime(2026, 10, 14, 11, 37, 55, tzinfo=UTC),   # the two 128k learning-rate pairs
    ("wide", 0): dt.datetime(2026, 10, 19, 8, 22, 41, tzinfo=UTC),
    ("vend", 0): dt.datetime(2026, 10, 26, 7, 49, 18, tzinfo=UTC),
    ("vend", 1): dt.datetime(2026, 10, 28, 14, 26, 9, tzinfo=UTC),       # the two 256-wide trials
}


def _rng(*parts):
    return np.random.default_rng(W.seed_of("infra", *parts))


def run_id(name, submit):
    """The tracking server's id for a run: eight base-36 characters."""
    h = int(hashlib.sha256(("%s|%s" % (name, submit.isoformat())).encode()).hexdigest()[:16], 16)
    out = ""
    for _ in range(8):
        h, r = divmod(h, 36)
        out += "0123456789abcdefghijklmnopqrstuvwxyz"[r]
    return out


def _batch_key(job):
    st, w, t = job["stage"], job["train"]["width"], job["train"]
    if st == "ladder":
        return ("ladder", w)
    if st == "lrcheck":
        return ("lrcheck", 1 if t.get("nA") == 128000 else 0)
    if st == "wide":
        return ("wide", 0)
    return ("vend", 1 if w == 256 else 0)


def schedule(jobs):
    """Put every job's attempts on the cluster. Returns the jobs with: submit time, run id, and a list of attempts,
    each with its node, start, end, state, the step range it covered and its seconds per step."""
    order = {}
    for j in jobs:
        order.setdefault(_batch_key(j), []).append(j)
    pending = []
    for key, batch in order.items():
        t = BATCH_START[key]
        r = _rng("batch", key)
        firsts = [j for j in batch if j["fate"] in ("cancelled", "node_fail")]
        rest = [j for j in batch if j not in firsts]
        seq = []
        # a failed first launch goes on with the batch; its relaunch (the job of the same name) goes on later
        names_failed = {j["name"] for j in firsts}
        for j in rest:
            if j["name"] in names_failed:
                continue
            seq.append(j)
        idx = r.permutation(len(seq)) if key[0] == "vend" else np.arange(len(seq))
        seq = [seq[i] for i in idx]
        for f in firsts:
            seq.insert(int(r.integers(1, max(2, len(seq) // 2))), f)
        for j in seq:
            t = t + dt.timedelta(seconds=float(r.uniform(2.2, 9.5)))
            j["submit"] = t
        for j in rest:
            if j["name"] in names_failed:
                first = next(f for f in firsts if f["name"] == j["name"])
                # relaunched after the failure was seen: the same day or the next morning
                j["relaunch_of"] = first
    # node timeline
    free = {n: BATCH_START[("ladder", 64)] - dt.timedelta(hours=1) for n, _ in NODES}
    speed = dict(NODES)
    events = []
    for j in jobs:
        if "relaunch_of" not in j:
            events.append(j)
    events.sort(key=lambda j: j["submit"])
    relaunches = [j for j in jobs if "relaunch_of" in j]
    done_end = {}

    def place(j):
        t = j["train"]
        r = _rng("job", j["name"], j["submit"].isoformat())
        steps = t["steps"]
        stop = t.get("stop_at", steps)
        pre = sorted(t.get("preempt_at", []))
        ready = j["submit"]
        start_step = 0
        attempts = []
        cuts = [p for p in pre if p < stop] + [stop]
        for k, cut in enumerate(cuts):
            node = min(free, key=lambda n: (max(free[n], ready), speed[n] if j["fate"] != "timeout" or k == 0 else -speed[n]))
            begin = max(free[node], ready) + dt.timedelta(seconds=float(r.uniform(4, 70)))
            sps = STEP_SECONDS[t["width"]] * speed[node] * float(np.exp(r.normal(0, 0.025)))
            startup = float(r.uniform(140, 265))
            n_steps = cut - start_step
            n_eval = len([s for s in range(start_step + 1, cut + 1) if s % t["eval_every"] == 0])
            last = (k == len(cuts) - 1)
            state = "PREEMPTED"
            if last:
                state = {"finished": "COMPLETED", "cancelled": "CANCELLED", "node_fail": "NODE_FAIL",
                         "timeout": "TIMEOUT"}[j["fate"]]
            if state == "TIMEOUT":
                # the job runs out of walltime: the last attempt lasts exactly the limit
                sps = (WALLTIME - startup - n_eval * EVAL_SECONDS) / float(n_steps)
                elapsed = float(WALLTIME)
            else:
                elapsed = startup + n_steps * sps + n_eval * EVAL_SECONDS
                if state == "COMPLETED":
                    elapsed += float(r.uniform(35, 120))      # final scoring and the item dump
            end = begin + dt.timedelta(seconds=elapsed)
            attempts.append(dict(restart=k, node=node, start=begin, end=end, state=state, from_step=start_step,
                                 to_step=cut, sps=sps, startup=startup))
            free[node] = end + dt.timedelta(seconds=float(r.uniform(20, 400)))
            if not last:
                # someone else's job holds the node; ours goes back on the queue and resumes from its last checkpoint
                free[node] = end + dt.timedelta(minutes=float(r.uniform(35, 240)))
                ready = end + dt.timedelta(seconds=float(r.uniform(30, 180)))
                start_step = (cut // t["ckpt_every"]) * t["ckpt_every"]
        j["attempts"] = attempts
        j["run_id"] = run_id(j["name"], j["submit"])
        done_end[id(j)] = attempts[-1]["end"]

    for j in events:
        place(j)
    for j in sorted(relaunches, key=lambda j: done_end[id(j["relaunch_of"])]):
        r = _rng("relaunch", j["name"])
        seen = done_end[id(j["relaunch_of"])] + dt.timedelta(hours=float(r.uniform(1.5, 19)))
        # nobody relaunches at night
        if seen.hour < 7:
            seen = seen.replace(hour=7, minute=int(r.integers(5, 55)))
        elif seen.hour >= 21:
            seen = (seen + dt.timedelta(days=1)).replace(hour=7, minute=int(r.integers(5, 55)))
        j["submit"] = seen
        place(j)
    # scheduler job ids rise with the cluster's traffic (other users' jobs fall between ours)
    t0 = BATCH_START[("ladder", 64)]
    base = 4118203
    allj = sorted(jobs, key=lambda j: j["submit"])
    last_id = base
    for j in allj:
        hours = (j["submit"] - t0).total_seconds() / 3600.0
        r = _rng("jobid", j["name"], j["submit"].isoformat())
        jid = base + int(hours * 41.7) + int(r.integers(0, 23))
        last_id = max(last_id + int(r.integers(1, 4)), jid)
        j["job_id"] = last_id
    return jobs


def step_time(job, attempt, step, eval_every):
    """When the trainer logged a given step in a given attempt."""
    a = job["attempts"][attempt]
    n_eval = (step // eval_every) - (a["from_step"] // eval_every)
    return a["start"] + dt.timedelta(seconds=a["startup"] + (step - a["from_step"]) * a["sps"] + n_eval * EVAL_SECONDS)


def n_params(width):
    return (P.D_IN * width + width) + (width * width + width) * (P.DEPTH - 1) + (width * P.K + P.K)


def ckpt_bytes(width):
    """Weights and both Adam moments in float32, plus the trainer's small header."""
    return 3 * 4 * n_params(width) + 1387
