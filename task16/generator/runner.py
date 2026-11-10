"""Runs training jobs once and keeps what each logged, keyed by everything that sets the arithmetic."""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import hashlib
import json
import time
from multiprocessing import Pool

import numpy as np

import params as P
import world as W

KEYS = ("width", "nA", "nB", "nC", "nX", "lr", "seed", "steps", "stop_at", "log_every", "eval_every", "ckpt_every",
        "preempt_at", "bench_at")


def key_of(spec):
    core = {k: spec.get(k) for k in KEYS if spec.get(k) not in (None, 0, [], ())}
    core["world"] = (P.WORLD_TAG, P.WORLD_SEED, P.ROUTE_ERROR, P.BATCH, P.WARMUP, P.DEPTH)
    return hashlib.sha1(json.dumps(core, sort_keys=True).encode()).hexdigest()[:20]


def _path(spec):
    return os.path.join(W.CACHE, "run_%s.npz" % key_of(spec))


def planned_steps(spec):
    n = spec.get("nA", 0) + spec.get("nB", 0) + spec.get("nC", 0) + spec.get("nX", 0)
    return int(round(P.EPOCHS * n / P.BATCH))


def _job(spec):
    path = _path(spec)
    if os.path.exists(path):
        return path, 0.0
    import trainer as T
    t0 = time.time()
    o = T.train(spec)
    f = o["final"]
    bench_steps = sorted(o["bench"])
    np.savez_compressed(
        path,
        train=np.array(o["train_rows"], dtype=np.float64), evals=np.array(o["eval_rows"], dtype=np.float64),
        ckpt_att=np.array([c[0] for c in o["ckpts"]]), ckpt_step=np.array([c[1] for c in o["ckpts"]]),
        ckpt_hash=np.array([c[2] for c in o["ckpts"]]),
        bench_step=np.array(bench_steps), bench_loss=np.array([o["bench"][s][0] for s in bench_steps]),
        bench_acc=np.array([o["bench"][s][1] for s in bench_steps]), bench_hash=np.array([o["bench"][s][2] for s in bench_steps]),
        nll=o["nll"], pred=o["pred"],
        final=np.array([f["step"], f["attempt"], f["dev_loss"], f["dev_acc"], f["bench_loss"], f["bench_acc"]], dtype=np.float64),
        final_hash=np.array(f["hash"]), n_examples=np.array(o["n_examples"]))
    return path, time.time() - t0


def run_all(specs, procs=4, verbose=True):
    """Train every job not yet on disk, largest first, and return the path of each job's record."""
    W.build_arrays()
    todo = [s for s in specs if not os.path.exists(_path(s))]
    todo.sort(key=lambda s: -(s["width"] ** 2) * s.get("stop_at", s["steps"]))
    if todo:
        t0 = time.time()
        with Pool(procs) as pool:
            for i, (path, secs) in enumerate(pool.imap_unordered(_job, todo, chunksize=1)):
                if verbose and (secs > 60 or (i + 1) % 20 == 0 or i + 1 == len(todo)):
                    print("  trained %d of %d (%.0fs elapsed)" % (i + 1, len(todo), time.time() - t0), flush=True)
    return [_path(s) for s in specs]


def load(spec):
    z = np.load(_path(spec), allow_pickle=False)
    return {k: z[k] for k in z.files}
