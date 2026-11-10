"""The group's trainer: a two-hidden-layer classifier trained with Adam on a cosine schedule.

A run here is a real optimisation run. Nothing in the logs it returns is drawn or edited: the losses, the gradient
norms, the development scores, the per-item scores of the final checkpoint and the checkpoint hashes are what the
arithmetic produced. A job that is preempted loses the steps since its last checkpoint and picks up again from that
checkpoint with a fresh data order, which is what the lab's trainer does (it saves weights and optimiser state, not
the loader's position).
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import hashlib
import math

import numpy as np

import params as P
import world as W


def _forward(Ws, bs, x):
    h = x
    for i in range(P.DEPTH):
        h = np.maximum(h @ Ws[i] + bs[i], 0)
    z = h @ Ws[P.DEPTH] + bs[P.DEPTH]
    z = z - z.max(1, keepdims=True)
    return z - np.log(np.exp(z).sum(1, keepdims=True))


def score(Ws, bs, x, y):
    """Mean log loss, accuracy, each item's own loss and the predicted class."""
    nll = np.empty(len(y), np.float32)
    pred = np.empty(len(y), np.int8)
    for i in range(0, len(y), 8192):
        lp = _forward(Ws, bs, x[i:i + 8192])
        nll[i:i + 8192] = -lp[np.arange(lp.shape[0]), y[i:i + 8192]]
        pred[i:i + 8192] = lp.argmax(1)
    return float(nll.mean()), float((pred == y).mean()), nll, pred


def _hash(Ws, bs):
    h = hashlib.sha1()
    for a in Ws + bs:
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def train(spec):
    """Run one job to its end (or to spec['stop_at']) and return everything it logged."""
    width = spec["width"]; lr = spec["lr"]; seed = spec["seed"]
    xtr, ytr = W.training_arrays(spec.get("nA", 0), spec.get("nB", 0), spec.get("nC", 0), spec.get("nX", 0))
    n = len(ytr)
    steps = spec["steps"]
    stop_at = spec.get("stop_at", steps)
    log_every = spec.get("log_every", 20)
    eval_every = spec.get("eval_every", 250)
    ckpt_every = spec.get("ckpt_every", 2000)
    preempt_at = sorted(spec.get("preempt_at", []))
    bench_at = set(spec.get("bench_at", []))
    xd, yd, _ = W.dev()
    xb, yb = W.bench()

    r = np.random.default_rng(W.seed_of("init", seed, width))
    sizes = [P.D_IN] + [width] * P.DEPTH + [P.K]
    Ws = [r.normal(0, np.sqrt(2.0 / sizes[i]), (sizes[i], sizes[i + 1])).astype(np.float32) for i in range(P.DEPTH + 1)]
    bs = [np.zeros(sizes[i + 1], np.float32) for i in range(P.DEPTH + 1)]
    m = [np.zeros_like(p) for p in Ws + bs]
    v = [np.zeros_like(p) for p in Ws + bs]
    b1, b2, eps = P.ADAM
    wsteps = max(1, int(P.WARMUP * steps))
    B = P.BATCH

    train_rows, eval_rows, ckpts, bench = [], [], [], {}
    attempt = 0
    saved = (0, [a.copy() for a in Ws], [a.copy() for a in bs], [a.copy() for a in m], [a.copy() for a in v])
    order = np.random.default_rng(W.seed_of("order", seed, attempt))
    perm = order.permutation(n); pos = 0
    acc_loss = 0.0; acc_n = 0
    t = 0
    pending = list(preempt_at)
    while t < stop_at:
        t += 1
        if pos + B > n:
            perm = order.permutation(n); pos = 0
        idx = np.sort(perm[pos:pos + B]); pos += B
        xb_ = xtr[idx]; yb_ = ytr[idx]
        acts = [xb_]; h = xb_
        for i in range(P.DEPTH):
            h = h @ Ws[i] + bs[i]
            np.maximum(h, 0, out=h)
            acts.append(h)
        z = h @ Ws[P.DEPTH] + bs[P.DEPTH]
        z -= z.max(1, keepdims=True)
        p = np.exp(z); p /= p.sum(1, keepdims=True)
        acc_loss += float(-np.log(p[np.arange(B), yb_] + 1e-12).mean()); acc_n += 1
        g = p; g[np.arange(B), yb_] -= 1; g /= B
        gW = [None] * (P.DEPTH + 1); gb = [None] * (P.DEPTH + 1)
        for i in range(P.DEPTH, -1, -1):
            gW[i] = acts[i].T @ g
            gb[i] = g.sum(0)
            if i > 0:
                g = (g @ Ws[i].T) * (acts[i] > 0)
        cur = lr * t / wsteps if t <= wsteps else lr * 0.5 * (1 + math.cos(math.pi * (t - wsteps) / max(1, steps - wsteps)))
        params = Ws + bs
        grads = gW + gb
        for j in range(len(params)):
            m[j] = b1 * m[j] + (1 - b1) * grads[j]
            v[j] = b2 * v[j] + (1 - b2) * grads[j] * grads[j]
            params[j] -= cur * (m[j] / (1 - b1 ** t)) / (np.sqrt(v[j] / (1 - b2 ** t)) + eps)
        if t % log_every == 0 or t == stop_at:
            gn = math.sqrt(sum(float((a * a).sum()) for a in grads))
            train_rows.append((attempt, t, t * B, acc_loss / acc_n, cur, gn))
            acc_loss = 0.0; acc_n = 0
        if t % eval_every == 0 or t == stop_at:
            dl, da, _, _ = score(Ws, bs, xd, yd)
            eval_rows.append((attempt, t, t * B, dl, da))
        if t in bench_at and t != stop_at:
            bl, ba, _, _ = score(Ws, bs, xb, yb)
            bench[t] = (bl, ba, _hash(Ws, bs))
        if t % ckpt_every == 0 and t != stop_at:
            saved = (t, [a.copy() for a in Ws], [a.copy() for a in bs], [a.copy() for a in m], [a.copy() for a in v])
            ckpts.append((attempt, t, _hash(Ws, bs)))
        if pending and t == pending[0] and t < stop_at:
            pending.pop(0)
            # the node is taken back: everything since the last checkpoint is lost
            t, Ws_, bs_, m_, v_ = saved
            Ws = [a.copy() for a in Ws_]; bs = [a.copy() for a in bs_]
            m = [a.copy() for a in m_]; v = [a.copy() for a in v_]
            attempt += 1
            order = np.random.default_rng(W.seed_of("order", seed, attempt))
            perm = order.permutation(n); pos = 0
            acc_loss = 0.0; acc_n = 0
    dl, da, nll, pred = score(Ws, bs, xd, yd)
    bl, ba, _, _ = score(Ws, bs, xb, yb)
    hfin = _hash(Ws, bs)
    ckpts.append((attempt, t, hfin))
    bench[t] = (bl, ba, hfin)
    return dict(train_rows=train_rows, eval_rows=eval_rows, ckpts=ckpts, bench=bench, n_examples=n,
                final=dict(step=t, attempt=attempt, dev_loss=dl, dev_acc=da, bench_loss=bl, bench_acc=ba, hash=hfin),
                nll=nll, pred=pred)
