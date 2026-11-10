"""The pilot sweep the group ran over five weeks, and the shortlist it now has to choose from.

Each entry is a job the lab launched: what was trained, on which shards, at which learning rate, and what happened
to the job (finished, taken back by the scheduler and resumed, cancelled, out of walltime). The arithmetic of every
job is run for real by trainer.py; this file only says which jobs exist.
"""
import params as P
import world as W
from runner import planned_steps

TABLE_LR = {64: 2e-3, 128: 1e-3, 256: 5e-4}            # the group's tabled learning rate per width (weeks 1 and 2)
LR_GRID = {64: (1e-3, 2e-3, 4e-3, 8e-3, 1.6e-2), 128: (5e-4, 1e-3, 2e-3, 4e-3, 8e-3),
           256: (2.5e-4, 5e-4, 1e-3, 2e-3, 4e-3), 512: (1.25e-4, 2.5e-4, 5e-4, 1e-3, 2e-3)}
TUNED_LR = {128: 2e-3, 256: 1e-3, 512: 5e-4}            # what the group took from its learning-rate check
LADDER_SIZES = (8000, 16000, 32000, 64000, 128000)
# the map-transfer labels were on hand from week 3; the contractor's lot arrived in the last week, in time for four
# trials and none that mixed it with the map labels
VENDOR_CELLS = [(32, 0, 32), (32, 0, 96), (32, 0, 224), (64, 0, 64), (64, 0, 192), (64, 0, 448), (128, 0, 128),
                (128, 0, 384),
                (32, 32, 0), (32, 96, 0), (64, 64, 0), (128, 128, 0)]


def _lr_tag(lr):
    s = ("%.2e" % lr).replace("e-0", "e-")
    m, e = s.split("e")
    m = m.rstrip("0").rstrip(".")
    return "%se%s" % (m, e)


def _data_tag(a, b, c):
    parts = []
    for tag, n in (("exp", a), ("ctr", b), ("map", c)):
        if n:
            parts.append("%s%dk" % (tag, n // 1000))
    return "-".join(parts)


def _spec(stage, width, lr, seed, a=0, b=0, c=0, logger=2, **kw):
    s = dict(width=width, lr=lr, seed=seed, nA=a, nB=b, nC=c)
    s["steps"] = planned_steps(s)
    s["log_every"] = 50 if logger == 1 else 20
    s["eval_every"] = 250 if s["steps"] <= 6000 else (500 if s["steps"] <= 24000 else 1000)
    s["ckpt_every"] = 2000
    s.update(kw)
    name = "%s-w%d-%s" % (stage, width, _data_tag(a, b, c))
    if stage in ("lrcheck", "wide"):
        name += "-lr%s" % _lr_tag(lr)
    name += "-s%d" % seed
    return dict(stage=stage, name=name, logger=logger, train=s)


def _preempt(job, share_list):
    """Give a long job the preemptions the scheduler dealt it: it loses the steps since its last checkpoint."""
    st = job["train"]["steps"]
    job["train"]["preempt_at"] = [(int(st * x / 10.0) // 10) * 10 + 7 for x in share_list]
    return job


def pilot_specs():
    jobs = []
    # weeks 1 and 2: the size ladder on expert labels, at the tabled learning rates (logger 1)
    for w in (64, 128, 256):
        for n in LADDER_SIZES:
            for sd in (1, 2, 3):
                jobs.append(_spec("ladder", w, TABLE_LR[w], sd, a=n, logger=1))
    # two ladder jobs were launched once before and did not survive
    bad1 = _spec("ladder", 128, TABLE_LR[128], 2, a=32000, logger=1, stop_at=700)
    bad1["name"] = "ladder-w128-exp64k-s2"; bad1["fate"] = "cancelled"
    bad1["note"] = "wrong shard range"
    bad2 = _spec("ladder", 256, TABLE_LR[256], 3, a=16000, logger=1, stop_at=400)
    bad2["fate"] = "node_fail"
    jobs += [bad1, bad2]
    # week 3: the learning-rate check (logger 2); the tabled rates were already run in the ladder
    for w in (64, 128, 256, 512):
        for lr in LR_GRID[w]:
            if w in TABLE_LR and abs(lr - TABLE_LR[w]) < 1e-12:
                continue
            for sd in (1, 2):
                jobs.append(_spec("lrcheck", w, lr, sd, a=32000))
    for w, lrs in ((128, (2e-3, 4e-3)), (256, (1e-3, 2e-3))):
        for lr in lrs:
            jobs.append(_spec("lrcheck", w, lr, 1, a=128000))
    bad3 = _spec("lrcheck", 512, 2.5e-4, 2, a=32000, stop_at=1160)
    bad3["fate"] = "node_fail"
    jobs.append(bad3)
    # week 4: wider
    for lr in (1e-3, 5e-4):
        for sd in (1, 2):
            jobs.append(_spec("wide", 512, lr, sd, a=128000))
    big = _spec("wide", 1024, 5e-4, 1, a=128000, stop_at=8460)
    big["fate"] = "timeout"
    jobs.append(big)
    # week 5: the contractor's lot and the map-transfer labels
    for a, b, c in VENDOR_CELLS:
        for sd in (1, 2, 3):
            jobs.append(_spec("vend", 128, TUNED_LR[128], sd, a=a * 1000, b=b * 1000, c=c * 1000))
    for a, b, c in ((128, 128, 0), (128, 0, 128), (128, 0, 384)):
        for sd in (1, 2):
            jobs.append(_spec("vend", 256, TUNED_LR[256], sd, a=a * 1000, b=b * 1000, c=c * 1000))
    bad4 = _spec("vend", 128, 2e-2, 1, a=64000, c=64000, stop_at=900)
    bad4["name"] = "vend-w128-exp64k-map64k-s1"; bad4["fate"] = "cancelled"; bad4["note"] = "learning rate typed 2e-2"
    jobs.append(bad4)

    # the scheduler takes back some long jobs: which ones, and when, is the cluster's business
    by_name = {}
    for j in jobs:
        by_name.setdefault(j["name"], []).append(j)
    plan = {"ladder-w256-exp128k-s1": [4.4], "ladder-w64-exp128k-s3": [7.1], "ladder-w128-exp128k-s2": [2.9],
            "lrcheck-w256-exp128k-lr2e-3-s1": [5.6], "wide-w512-exp128k-lr1e-3-s1": [3.3, 7.8],
            "wide-w512-exp128k-lr5e-4-s2": [6.2], "wide-w1024-exp128k-lr5e-4-s1": [2.4],
            "vend-w128-exp128k-map384k-s1": [1.9, 6.7], "vend-w128-exp128k-map384k-s3": [5.2],
            "vend-w128-exp64k-map448k-s2": [4.1], "vend-w128-exp64k-map192k-s2": [8.3],
            "vend-w128-exp32k-map224k-s1": [3.7], "vend-w128-exp128k-ctr128k-s3": [6.4],
            "vend-w256-exp128k-map384k-s1": [2.2, 5.9], "vend-w256-exp128k-map128k-s2": [4.8], "vend-w128-exp128k-map128k-s2": [7.4]}
    for name, shares in plan.items():
        for j in by_name[name]:
            if "fate" not in j or j["fate"] == "timeout":
                _preempt(j, shares)
    # the benchmark submissions that were of a checkpoint part-way through a job
    for name, step in (("ladder-w256-exp128k-s2", 10000), ("wide-w512-exp128k-lr1e-3-s2", 8000)):
        for j in by_name[name]:
            if "fate" not in j:
                j["train"]["bench_at"] = [step]
    for j in jobs:
        j.setdefault("fate", "finished")
    return jobs


# the shortlist the group agreed on 5 November: width, examples by route, learning rate (None where still to be set)
SHORTLIST = [
    dict(key="A", width=1024, nA=128000, nB=0, nC=0, lr=None),
    dict(key="B", width=512, nA=128000, nB=128000, nC=0, lr=5e-4),
    dict(key="C", width=256, nA=128000, nB=128000, nC=1024000, lr=1e-3),
    dict(key="D", width=256, nA=128000, nB=0, nC=1024000, lr=1e-3),
]


def truth_specs(seeds=(1, 2, 3)):
    """What each shortlisted configuration really scores, and what more expert labels would have given: run for the
    author only, to check the forecast against what happens. Nothing here ships."""
    out = []
    for c in SHORTLIST:
        lrs = (3.5e-4, 2.5e-4, 5e-4, 2.74e-4, 1.8e-4) if c["lr"] is None else (c["lr"],)
        for lr in lrs:
            for sd in (seeds if lr in (3.5e-4, c["lr"]) else (seeds[:2] if lr in (2.74e-4, 1.8e-4) else seeds[:1])):
                s = dict(width=c["width"], lr=lr, seed=sd, nA=c["nA"], nB=c["nB"], nC=c["nC"])
                s["steps"] = planned_steps(s)
                s["log_every"] = 20; s["eval_every"] = 1000; s["ckpt_every"] = 2000
                out.append(dict(stage="truth", name="truth-%s-lr%s-s%d" % (c["key"], _lr_tag(lr), sd), train=s))
    return out


def clean_truth_specs():
    """The expert-equivalent curve past the expert pool, from expert-quality labels the lab does not have."""
    out = []
    for w, lr, totals in ((128, 2e-3, (256000, 512000)), (256, 1e-3, (256000, 512000, 1152000, 1280000)),
                          (512, 5e-4, (256000,))):
        for tot in totals:
            s = dict(width=w, lr=lr, seed=1, nA=128000, nB=0, nC=0, nX=tot - 128000)
            s["steps"] = planned_steps(s)
            s["log_every"] = 20; s["eval_every"] = 1000; s["ckpt_every"] = 2000
            out.append(dict(stage="cleantruth", name="clean-w%d-%dk" % (w, tot // 1000), train=s))
    return out
