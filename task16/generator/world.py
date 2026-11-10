"""The world the Tromso group's models are trained in.

Nothing here is shipped. It is the process that produces the lab's data: one population of survey points with 32
acoustic and terrain features, a fixed relation from features to ten sediment classes that no model of the sizes
run can learn exactly, and three labelling routes that record a point's class with their own error. The training
runs in trainer.py are real optimisation runs on these arrays, and every curve in the pack is what such a run logged.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import hashlib

import numpy as np

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")


def seed_of(*parts):
    """A stable 32-bit seed from strings and numbers (never Python's hash, which is salted per process)."""
    h = hashlib.sha256(("|".join(str(p) for p in parts)).encode()).digest()
    return int.from_bytes(h[:4], "little")


class Teacher:
    """The fixed relation from a point's features to the chance of each sediment class."""

    def __init__(self):
        r = np.random.default_rng(P.WORLD_SEED)
        spec = (np.arange(1, P.D_IN + 1) ** -0.5).astype(np.float32)
        self.scale = (spec / np.sqrt((spec ** 2).mean())).astype(np.float32)
        self.W = (r.normal(0, 1.0, (P.D_IN, P.TEACHER_J)) / np.sqrt(P.D_IN) * 2.0).astype(np.float32)
        self.b = r.uniform(-1.5, 1.5, P.TEACHER_J).astype(np.float32)
        coef = (np.arange(1, P.TEACHER_J + 1) ** -P.TEACHER_GAMMA).astype(np.float32)
        A = r.normal(0, 1, (P.TEACHER_J, P.K)).astype(np.float32) * coef[:, None]
        self.A = (A / np.sqrt((coef ** 2).sum())).astype(np.float32)
        # each labelling route confuses a class with a few neighbouring grain-size classes, in its own way
        self.conf = {}
        for route in ("B", "C"):
            rr = np.random.default_rng(seed_of("confusion", route, P.WORLD_SEED))
            m = np.zeros((P.K, P.K), np.float64)
            for k in range(P.K):
                near = [j for j in (k - 2, k - 1, k + 1, k + 2) if 0 <= j < P.K]
                w = rr.dirichlet(np.ones(len(near)) * (0.9 if route == "C" else 2.0))
                for j, wj in zip(near, w):
                    m[k, j] = wj
                # a small share of slips land anywhere
                m[k] = 0.93 * m[k] + 0.07 * np.where(np.arange(P.K) == k, 0, 1.0 / (P.K - 1))
                m[k] /= m[k].sum()
            self.conf[route] = m

    def features(self, r, n):
        return r.normal(0, 1, (n, P.D_IN)).astype(np.float32) * self.scale

    def probs(self, x):
        out = np.empty((x.shape[0], P.K), np.float32)
        for i in range(0, x.shape[0], 16384):
            h = np.tanh(x[i:i + 16384] @ self.W + self.b)
            z = P.TEACHER_BETA * (h @ self.A)
            z -= z.max(1, keepdims=True)
            p = np.exp(z)
            out[i:i + 16384] = p / p.sum(1, keepdims=True)
        return out

    def draw(self, r, n, route):
        """n points labelled by a route: the class the ground truth process gives, then the route's recording error."""
        x = self.features(r, n)
        p = self.probs(x)
        y = (r.random(n)[:, None] > p.cumsum(1)).sum(1).clip(0, P.K - 1)
        rho = P.ROUTE_ERROR[route]
        if rho > 0:
            slip = r.random(n) < rho
            cc = self.conf[route][y].cumsum(1)
            y2 = (r.random(n)[:, None] > cc).sum(1).clip(0, P.K - 1)
            y = np.where(slip, y2, y)
        return x, y.astype(np.int8), p


_T = None
_MEM = {}


def teacher():
    global _T
    if _T is None:
        _T = Teacher()
    return _T


def _path(name):
    os.makedirs(CACHE, exist_ok=True)
    return os.path.join(CACHE, "world_%s_%s" % (P.WORLD_TAG, name))


def build_arrays():
    """Write every array of the world once; later processes memory-map them."""
    t = teacher()
    pools = dict(P.POOL)
    pools["X"] = P.PRIVATE_EXPERT_POOL
    for route, n in pools.items():
        if os.path.exists(_path("x_%s.npy" % route)):
            continue
        r = np.random.default_rng(seed_of("pool", route, P.WORLD_SEED))
        x, y, _ = t.draw(r, n, "A" if route == "X" else route)
        np.save(_path("x_%s.npy" % route), x)
        np.save(_path("y_%s.npy" % route), y)
    if not os.path.exists(_path("x_dev.npy")):
        xs, ys, rs = [], [], []
        for route, n in P.DEV_MIX.items():
            r = np.random.default_rng(seed_of("dev", route, P.WORLD_SEED))
            x, y, _ = t.draw(r, n, route)
            xs.append(x); ys.append(y); rs.extend([route] * n)
        x = np.concatenate(xs); y = np.concatenate(ys); rt = np.array(rs)
        order = np.random.default_rng(seed_of("devorder", P.WORLD_SEED)).permutation(len(y))
        np.save(_path("x_dev.npy"), x[order]); np.save(_path("y_dev.npy"), y[order]); np.save(_path("r_dev.npy"), rt[order])
    if not os.path.exists(_path("x_bench.npy")):
        r = np.random.default_rng(seed_of("benchmark", P.WORLD_SEED))
        x, y, p = t.draw(r, P.BENCH_N, "A")
        np.save(_path("x_bench.npy"), x); np.save(_path("y_bench.npy"), y)
        np.save(_path("floor.npy"), np.array([float(-np.log(p[np.arange(len(y)), y] + 1e-12).mean())]))


def pool(route):
    k = "pool" + route
    if k not in _MEM:
        _MEM[k] = (np.load(_path("x_%s.npy" % route), mmap_mode="r"), np.load(_path("y_%s.npy" % route), mmap_mode="r"))
    return _MEM[k]


def dev():
    if "dev" not in _MEM:
        _MEM["dev"] = (np.load(_path("x_dev.npy")), np.load(_path("y_dev.npy")).astype(np.int64), np.load(_path("r_dev.npy")))
    return _MEM["dev"]


def bench():
    if "bench" not in _MEM:
        _MEM["bench"] = (np.load(_path("x_bench.npy")), np.load(_path("y_bench.npy")).astype(np.int64))
    return _MEM["bench"]


def floor():
    return float(np.load(_path("floor.npy"))[0])


def training_arrays(nA, nB, nC, nX=0):
    """The first n examples of each route's shard list, as the lab's loader takes them."""
    xs, ys = [], []
    for route, n in (("A", nA), ("B", nB), ("C", nC), ("X", nX)):
        if n:
            x, y = pool(route)
            xs.append(np.asarray(x[:n])); ys.append(np.asarray(y[:n]).astype(np.int64))
    return np.concatenate(xs), np.concatenate(ys)
