"""The physics and processes behind Saukko Labs' records: how documents are drawn and packed into sequences, what a
sequence costs a data-parallel rank, how a synchronous step waits for its slowest rank, how the provider's power
manager holds a hall to its contract, how jobs are interrupted and restart. Shared by the 2026 simulation, the 2027
truth replay and (for the packing rule only, as the configs file it) the golden analysis."""
import math

import numpy as np

import params as P


# ------------------------------------------------------------------ documents
def draw_docs(mix, ntokens, rng, sources=None, with_source=False):
    """Documents in stream order until each source's token share of `ntokens` is met; lognormal lengths, capped."""
    sources = sources or P.SOURCES
    lens, srcs = [], []
    for s, sh in sorted(mix.items()):
        med, sig, cap = sources[s]
        need, got = sh * ntokens, 0
        mu = math.log(med)
        while got < need:
            l = np.minimum(rng.lognormal(mu, sig, 8192), cap).astype(np.int64) + 1
            c = np.cumsum(l) + got
            k = int(np.searchsorted(c, need)) + 1
            l = l[:k]
            lens.append(l)
            srcs.append(np.full(len(l), s, dtype=object))
            got += int(l.sum())
    d = np.concatenate(lens)
    o = rng.permutation(len(d))
    if with_source:
        return d[o], np.concatenate(srcs)[o]
    return d[o]


def docs_from_sample(sample_by_source, mix, ntokens, rng):
    """The golden's draw: documents resampled from the 2027 length sample at the mix's token shares."""
    lens = []
    for s, sh in sorted(mix.items()):
        pool = sample_by_source[s]
        need, got = sh * ntokens, 0
        while got < need:
            l = pool[rng.integers(0, len(pool), 8192)]
            c = np.cumsum(l) + got
            k = int(np.searchsorted(c, need)) + 1
            lens.append(l[:k])
            got += int(l[:k].sum())
    d = np.concatenate(lens)
    return d[rng.permutation(len(d))]


# ------------------------------------------------------------------ packing (the loader's two rules)
def pack_sequential(docs, C, keep=False):
    """Documents laid end to end and cut at every C tokens; every sequence full. Returns S (sum of piece lengths
    squared over C squared), fill (real tokens over C) and, with keep, each sequence's piece lengths."""
    S, F, pieces = [], [], []
    cur, acc, cur_p = 0, 0.0, []
    for l in docs:
        l = int(l)
        while l > 0:
            t = min(l, C - cur)
            acc += float(t) * t
            cur += t
            l -= t
            if keep:
                cur_p.append(t)
            if cur == C:
                S.append(acc / C / C)
                F.append(1.0)
                if keep:
                    pieces.append(cur_p)
                    cur_p = []
                cur, acc = 0, 0.0
    return np.array(S), np.array(F), pieces


def pack_best_fit(docs, C, open_max=64, keep=False):
    """The 2026 Q4 and 2027 long-context rule: a document up to C tokens is kept whole (longer ones are cut into
    C-token pieces and a remainder); each piece goes, in arrival order, to the open sequence with the least room that
    still fits it, else opens a new one; when more than open_max sequences are open the fullest is closed; leftover
    room is padding."""
    rem, sq, fl, cont = [], [], [], []
    S, F, pieces = [], [], []

    def close(j):
        S.append(sq[j] / C / C)
        F.append(fl[j] / C)
        if keep:
            pieces.append(cont[j])
        del rem[j], sq[j], fl[j], cont[j]

    for l in docs:
        l = int(l)
        parts = []
        while l > C:
            parts.append(C)
            l -= C
        if l > 0:
            parts.append(l)
        for x in parts:
            best, br = -1, C + 1
            for j in range(len(rem)):
                r = rem[j]
                if x <= r < br:
                    best, br = j, r
            if best < 0:
                rem.append(C - x)
                sq.append(float(x) * x)
                fl.append(x)
                cont.append([x] if keep else None)
                if rem[-1] == 0:
                    close(len(rem) - 1)
                elif len(rem) > open_max:
                    close(int(np.argmin(rem)))
            else:
                rem[best] -= x
                sq[best] += float(x) * x
                fl[best] += x
                if keep:
                    cont[best].append(x)
                if rem[best] == 0:
                    close(best)
    return np.array(S), np.array(F), pieces


def pack(docs, C, rule, keep=False):
    return pack_best_fit(docs, C, keep=keep) if rule == "best_fit" else pack_sequential(docs, C, keep=keep)


# ------------------------------------------------------------------ cost of a sequence and a step
def kappa_flops(model, C):
    """Attention FLOPs of one full-length document over the sequence's dense FLOPs: L d C / N."""
    N, L, d = P.MODELS[model]
    return L * d * C / N


def dense_seconds(model, C, hall):
    """Dense compute seconds for one sequence on one data-parallel rank (a node, tensor-parallel over its GPUs)."""
    N, L, d = P.MODELS[model]
    u = P.U_DENSE[model] * P.HALLS[hall]["ueff"]
    return 6.0 * N * C / (P.GPUS_PER_NODE * P.PEAK * u)


def seq_cost(S, model, C, beta=P.BETA):
    """A sequence's compute in units of its dense time: 1 + beta * kappa * S."""
    return 1.0 + beta * kappa_flops(model, C) * S


def step_stats(cost_pool, D, g, rng, steps=2000, jitter=P.RANK_JITTER):
    """Expected step compute (the slowest rank) and the mean rank, in dense-time units, from a pool of sequence
    costs dealt g to each of D ranks; also the step-to-step sd."""
    n = len(cost_pool)
    mx = np.empty(steps)
    mn = np.empty(steps)
    for i in range(steps):
        idx = rng.integers(0, n, size=(D, g))
        per = cost_pool[idx].sum(1) * (1.0 + jitter * rng.standard_normal(D))
        mx[i] = per.max()
        mn[i] = per.mean()
    return float(mx.mean()), float(mn.mean()), float(mx.std())


# ------------------------------------------------------------------ the provider's power manager
def throttle(x):
    """A step's compute stretch when the hall's would-be draw exceeds its contract by x (share)."""
    x = np.maximum(np.asarray(x, dtype=float), 0.0)
    return 1.0 + P.THR1 * x + P.THR2 * x * x


def pool_phi(base_ratio):
    """The research pool's admission: it starts no job once the load without it is POOL_KNEE of the contract and has
    none running by POOL_ZERO (a linear back-off between)."""
    return np.clip((P.POOL_ZERO - np.asarray(base_ratio, dtype=float)) / (P.POOL_ZERO - P.POOL_KNEE), 0.0, 1.0)


def hall_draw(hp, held, share, stop, rng, backoff=True):
    """Busy nodes and IT draw (kW) per interval of one hall. `held` is the nodes the registered runs (and the blocks of
    runs finished early, on backfill) occupy; the research pool takes `share` of the free nodes, scaled by its
    back-off against the contract; a hall-level stop (works, a facility event) leaves every node idle. The same
    process writes the 2026 meter and the 2027 truth."""
    N = hp["rows"] * hp["slots"]
    free = N - held
    base = (held * hp["node_kw"] + free * hp["idle_kw"] + hp["infra_kw"]) / hp["contract_kw"]
    phi = pool_phi(base) if backoff else np.ones(len(held))
    pool = np.minimum(np.floor(free * share * phi + rng.random(len(held))), free)
    busy = np.where(stop, 0.0, held + pool)
    draw = busy * hp["node_kw"] + (N - busy) * hp["idle_kw"] + hp["infra_kw"]
    return busy, draw


# ------------------------------------------------------------------ nodes
def node_names(hall):
    h = P.HALLS[hall]
    out = []
    if hall == "A":
        for r in range(1, h["rows"] + 1):
            for s in range(1, h["slots"] + 1):
                out.append("ka-r%02d-%02d" % (r, s))
    else:
        for p in range(1, h["pods"] + 1):
            for r in range(1, h["rows"] // h["pods"] + 1):
                for s in range(1, h["slots"] + 1):
                    out.append("kb-p%d-r%02d-%02d" % (p, r, s))
    return out


def block_nodes(hall, r0, r1):
    """The nodes of a reservation's rows r0 to r1 (hall-wide row numbers; hall B's rows 1 to 16 are pod 1)."""
    h = P.HALLS[hall]
    per = h["rows"] // h["pods"]
    out = []
    for r in range(r0, r1 + 1):
        for s in range(1, h["slots"] + 1):
            out.append("ka-r%02d-%02d" % (r, s) if hall == "A" else "kb-p%d-r%02d-%02d" % (1 + (r - 1) // per, 1 + (r - 1) % per, s))
    return out


def compress(nodes):
    """Slurm-style compressed node list: ka-r03-[01-32],ka-r04-[01-08]."""
    groups = {}
    for n in nodes:
        pre, num = n.rsplit("-", 1)
        groups.setdefault(pre, []).append(int(num))
    out = []
    for pre in sorted(groups):
        nums = sorted(groups[pre])
        spans, a = [], nums[0]
        b = a
        for x in nums[1:]:
            if x == b + 1:
                b = x
            else:
                spans.append((a, b))
                a = b = x
        spans.append((a, b))
        inner = ",".join("%02d" % a if a == b else "%02d-%02d" % (a, b) for a, b in spans)
        out.append("%s-[%s]" % (pre, inner))
    return ",".join(out)


def expand(s):
    out = []
    for part in split_top(s):
        pre, inner = part.split("-[")
        for span in inner.rstrip("]").split(","):
            if "-" in span:
                a, b = span.split("-")
                out += ["%s-%02d" % (pre, k) for k in range(int(a), int(b) + 1)]
            else:
                out.append("%s-%02d" % (pre, int(span)))
    return out


def split_top(s):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        parts.append(cur)
    return parts


def ckpt_gb(model):
    """A checkpoint's size: bf16 weights plus fp32 master weights and two Adam moments, GB."""
    N = P.MODELS[model][0]
    return N * (2 + 4 + 4 + 4) / 1e9
