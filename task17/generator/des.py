"""The scheduler kernel (des.c) compiled on first use into generator/cache/ and called through ctypes. One call
simulates one stretch of the partition: jobs in, segments and per-job outcomes out. Every random input is drawn in
Python; the kernel is deterministic."""
import ctypes
import hashlib
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
_LIB = None

STATES = {0: "COMPLETED", 1: "TIMEOUT", 2: "FAILED", 3: "CANCELLED", 4: "NODE_FAIL"}


def lib():
    global _LIB
    if _LIB is not None:
        return _LIB
    src = os.path.join(HERE, "des.c")
    code = open(src, "rb").read()
    h = hashlib.sha256(code).hexdigest()[:16]
    os.makedirs(CACHE, exist_ok=True)
    so = os.path.join(CACHE, "des_%s.so" % h)
    if not os.path.exists(so):
        tmp = so + ".%d.tmp" % os.getpid()
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", tmp, src], check=True)
        os.replace(tmp, so)
    L = ctypes.CDLL(so)
    D = ctypes.POINTER(ctypes.c_double)
    I = ctypes.POINTER(ctypes.c_int)
    U = ctypes.POINTER(ctypes.c_uint64)
    L.simulate.restype = ctypes.c_int
    L.simulate.argtypes = [ctypes.c_int, ctypes.c_int, D, I, D, D, D, I, I, D, I,
                           ctypes.c_int, I, D, D, ctypes.c_int, D, D,
                           ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,
                           D, D, I, I, D, D, D,
                           ctypes.c_int, I, I, I, D, D, U]
    _LIB = L
    return L


def _d(a):
    a = np.ascontiguousarray(a, dtype=np.float64)
    return a, a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


def _i(a):
    a = np.ascontiguousarray(a, dtype=np.int32)
    return a, a.ctypes.data_as(ctypes.POINTER(ctypes.c_int))


def simulate(n_nodes, jobs, outages, maint, t_end, mode=1, bf_max=200, hold=0.05):
    """jobs: dict of arrays submit, nodes, wall, dur, ckpt, dep, after, after_delay, endstate (all length n).
    outages: (node, start, end) arrays; maint: (start, end) arrays. Returns per-job arrays and the segments."""
    L = lib()
    n = len(jobs["submit"])
    keep = []
    def d(x):
        a, p = _d(x); keep.append(a); return p
    def i(x):
        a, p = _i(x); keep.append(a); return p
    first = np.full(n, -1.0); fend = np.full(n, -1.0); fstate = np.full(n, -1, dtype=np.int32)
    rest = np.zeros(n, dtype=np.int32); nh = np.zeros(n); rw = np.zeros(n); sub = np.zeros(n)
    seg_max = 3 * n + 8 * len(outages[0]) + 70 * len(maint[0]) + 1000
    sj = np.zeros(seg_max, dtype=np.int32); sn = np.zeros(seg_max, dtype=np.int32); ss = np.zeros(seg_max, dtype=np.int32)
    s_s = np.zeros(seg_max); s_e = np.zeros(seg_max); sm = np.zeros(seg_max, dtype=np.uint64)
    total = L.simulate(
        int(n_nodes), int(n), d(jobs["submit"]), i(jobs["nodes"]), d(jobs["wall"]), d(jobs["dur"]), d(jobs["ckpt"]),
        i(jobs["dep"]), i(jobs["after"]), d(jobs["after_delay"]), i(jobs["endstate"]),
        int(len(outages[0])), i(outages[0]), d(outages[1]), d(outages[2]),
        int(len(maint[0])), d(maint[0]), d(maint[1]),
        int(mode), int(bf_max), float(hold), float(t_end),
        first.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), fend.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        fstate.ctypes.data_as(ctypes.POINTER(ctypes.c_int)), rest.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
        nh.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), rw.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        sub.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        int(seg_max), sj.ctypes.data_as(ctypes.POINTER(ctypes.c_int)), sn.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
        ss.ctypes.data_as(ctypes.POINTER(ctypes.c_int)), s_s.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        s_e.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), sm.ctypes.data_as(ctypes.POINTER(ctypes.c_uint64)))
    assert 0 <= total <= seg_max, "kernel returned %d segments (cap %d)" % (total, seg_max)
    k = total
    return {"first_start": first, "final_end": fend, "final_state": fstate, "restarts": rest, "nh": nh,
            "rework": rw, "submit": sub,
            "seg": {"job": sj[:k].copy(), "no": sn[:k].copy(), "state": ss[:k].copy(), "start": s_s[:k].copy(),
                    "end": s_e[:k].copy(), "mask": sm[:k].copy()}}


def empty_jobs(n):
    return {"submit": np.zeros(n), "nodes": np.ones(n, dtype=np.int32), "wall": np.full(n, 24.0),
            "dur": np.ones(n), "ckpt": np.zeros(n), "dep": np.full(n, -1, dtype=np.int32),
            "after": np.full(n, -1, dtype=np.int32), "after_delay": np.zeros(n), "endstate": np.zeros(n, dtype=np.int32)}
