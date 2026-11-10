"""The clean tables: what the pack's files carry, in one form, before any file-level mess. Built from the world
(from_world) by the generator and rebuilt from target/ by golden.py; analysis.py reads only these. Nothing the
generator knows beyond the files (true durations, templates, checkpoint intervals, failure classes) is in them."""
import datetime as dt
import hashlib
import math

import numpy as np
import pandas as pd

import params as P
import sim

STATE_NAMES = {0: "COMPLETED", 1: "TIMEOUT", 2: "FAILED", 3: "CANCELLED", 4: "NODE_FAIL"}
OPERATORS = ["mrenner", "tkoehl", "svogt", "jbaum", "akraus", "ops"]
REASONS = {
    "software": ["GPU Xid 79 fallen off the bus, reboot", "xid79 reset", "nvidia driver hang - rebooted",
                 "Not responding", "kernel panic, rebooted", "nvlink error, reboot", "reboot after GPU hang",
                 "xid 79 / reboot", "GPU lost, node rebooted", "Neustart nach GPU-Fehler", "Not responding",
                 "NHC: gpu check failed, reboot", "XID 31 MMU fault, rebooted", "Not responding",
                 "node hung, power cycled", "Knoten haengt, reboot", "slurmd not responding, rebooted"],
    "hardware": ["GPU3 ECC errors, RMA", "RMA GPU - awaiting part", "GPU getauscht", "DIMM replaced (CE storm)",
                 "HCA replaced", "PSU failure, replaced", "NVMe replaced", "GPU1 replaced (RMA)",
                 "Netzteil getauscht", "fan tray replaced", "GPU2 XID 79 repeat -> RMA", "mainboard swap",
                 "awaiting replacement GPU", "DIMM swap", "RMA pending, GPU0"],
    "switch": ["Not responding", "leaf switch {sw} down", "ib switch {sw} failure", "Not responding",
               "Not responding", "{sw} replaced", "switch {sw}", "Not responding", "IB leaf {sw} dead, replaced"],
    "pdu": ["Not responding", "PDU trip {pdu}", "{pdu} tripped, electrician", "power {pdu}", "Not responding",
            "Not responding", "PDU {pdu} replaced", "Stromausfall {pdu}"],
    "admin": ["drain: benchmark reservation", "drained for driver test", "reserved for firmware test",
              "drain: Netzwerktest", "drain: cable check", "drained: NHC test"],
    "maint": ["scheduled maintenance", "Wartungsfenster {m}", "PM window {m}", "maintenance", "Wartung {m}",
              "planned maintenance {m}"],
}


def rng_for(seed, *keys):
    h = hashlib.blake2b(("%d|%s" % (seed, "|".join(str(k) for k in keys))).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def node_name(i):
    return "gpu%03d" % (i + 1)


def rack_of(i):
    return i // P.NODES_PER_RACK + 1


def switch_of(i):
    return "sw-r%02d" % rack_of(i)


def pdu_of(i):
    return "pdu-r%02d-%s" % (rack_of(i), "a" if (i % P.NODES_PER_RACK) < 4 else "b")


def reason_text(seed, iv_index, iv):
    r = rng_for(seed, "reason", iv_index)
    cls = iv["cls"]
    if cls == "rack":
        kind = iv["event"]["kind"]
        pool = REASONS[kind]
        txt = pool[r.integers(len(pool))]
        return txt.format(sw=switch_of(iv["node"]), pdu=pdu_of(iv["node"]))
    pool = REASONS[cls]
    return pool[r.integers(len(pool))]


def maint_text(seed, k, mw):
    r = rng_for(seed, "maintreason", k)
    pool = REASONS["maint"]
    return pool[r.integers(len(pool))].format(m=mw["month"].strftime("%Y-%m"))


class Pack:
    """jobs, seg, events, rack, grants, requests, maint, limits, report, cut_h"""
    pass


def from_world(w):
    pk = Pack()
    cut_h = sim.hrs(P.CUT)
    pk.cut_h = cut_h
    q = lambda x: np.round(np.asarray(x, dtype=float) * 3600.0) / 3600.0
    J = w.ran.copy()
    for c in ("submit", "first_start", "final_end"):
        J[c] = np.where(J[c].values >= 0, q(J[c].values), J[c].values)
    S = w.seg.copy()
    S["start"] = q(S["start"].values)
    S["end"] = q(S["end"].values)
    # per-segment node lists
    masks = S["mask"].values.astype(np.uint64)
    nodes_per_seg = np.array([bin(int(m)).count("1") for m in masks])
    node_lists = [[k for k in range(P.N_NODES) if (int(m) >> k) & 1] for m in masks]
    seg = pd.DataFrame({"job": S["job"].values, "seg": S["no"].values, "start_h": S["start"].values,
                        "end_h": S["end"].values, "state_code": S["state"].values, "nodes": nodes_per_seg})
    seg["node_ids"] = node_lists
    seg["jobid"] = J["jobid"].values[seg["job"].values]
    seg["epoch"] = J["epoch"].values[seg["job"].values]
    seg = seg[seg["start_h"] < cut_h].copy()
    keep_jobs = set(np.where((J["final_end"].values < 0) | (J["final_end"].values >= sim.hrs(P.LOG_FROM)))[0])
    seg = seg[[j in keep_jobs for j in seg["job"].values]].copy()
    seg["running"] = seg["end_h"] > cut_h
    seg["state"] = np.where(seg["running"], "RUNNING", seg["state_code"].map(STATE_NAMES))
    seg["end_h_cut"] = np.where(seg["running"], np.nan, seg["end_h"])
    seg["elapsed_h"] = np.round(np.where(seg["running"], cut_h - seg["start_h"], seg["end_h"] - seg["start_h"]) * 3600.0) / 3600.0
    seg["nh"] = seg["elapsed_h"] * seg["nodes"]
    seg["end_h"] = seg["end_h_cut"]
    pk.seg = seg.sort_values(["start_h", "jobid"]).reset_index(drop=True)
    # jobs: those submitted before the cut; the final state at the cut
    log_from = sim.hrs(P.LOG_FROM)
    jobs = J.drop(columns=["nh"]).copy()
    jobs = jobs[(jobs["submit"] < cut_h) & ((jobs["final_end"] < 0) | (jobs["final_end"] >= log_from))].copy()
    jobs["account"] = jobs["project"]
    jobs["submit_h"] = jobs["submit"]
    # eligible: dependents become eligible when their predecessor ends (the kernel's elig is not returned; rebuilt here)
    dep = J["dep"].values
    elig = J["submit"].values.copy()
    has_dep = dep >= 0
    pred_end = np.where(has_dep, J["final_end"].values[np.maximum(dep, 0)], -1.0)
    elig = np.where(has_dep & (pred_end > elig), pred_end, elig)
    jobs["elig_h"] = q(elig[jobs.index.values])
    jobs["start_h"] = np.where(jobs["first_start"] >= 0, jobs["first_start"], np.nan)
    jobs.loc[jobs["start_h"] >= cut_h, "start_h"] = np.nan
    jobs["end_h"] = np.where((jobs["final_end"] >= 0) & (jobs["final_end"] <= cut_h), jobs["final_end"], np.nan)
    agg = pk.seg.groupby("job").agg(elapsed_h=("elapsed_h", "sum"), nh=("nh", "sum"), nseg=("seg", "size"),
                                    last_state=("state", "last"))
    jobs = jobs.join(agg, how="left")
    jobs["elapsed_h"] = jobs["elapsed_h"].fillna(0.0)
    jobs["nh"] = jobs["nh"].fillna(0.0)
    jobs["nseg"] = jobs["nseg"].fillna(0).astype(int)
    st = np.where(jobs["start_h"].isna(), "PENDING", jobs["last_state"].fillna("PENDING"))
    jobs["state"] = st
    jobs["wall_h"] = jobs["wall"]
    jobs["restarts"] = np.where(jobs["nseg"] > 0, jobs["nseg"] - 1, 0)
    first_nodes = pk.seg[pk.seg["seg"] == 0].set_index("job")["node_ids"]
    jobs["node_ids"] = jobs.index.map(lambda i: first_nodes.get(i, []))
    canc = w.cancelled.copy()
    canc["submit"] = q(canc["submit"].values)
    canc["final_end"] = q(canc["final_end"].values)
    canc = canc[(canc["submit"] < cut_h) & (canc["final_end"] >= log_from)].copy()
    canc["account"] = canc["project"]
    canc["submit_h"] = canc["submit"]
    canc["elig_h"] = canc["submit"]
    canc["start_h"] = np.nan
    canc["end_h"] = np.where(canc["final_end"] <= cut_h, canc["final_end"], np.nan)
    canc["state"] = np.where(canc["end_h"].isna(), "PENDING", "CANCELLED")
    canc["elapsed_h"] = 0.0
    canc["nh"] = 0.0
    canc["nseg"] = 0
    canc["wall_h"] = canc["wall"]
    canc["restarts"] = 0
    canc["node_ids"] = [[] for _ in range(len(canc))]
    cols = ["jobid", "epoch", "name", "user", "account", "qos", "state", "nodes", "wall_h", "submit_h", "elig_h",
            "start_h", "end_h", "elapsed_h", "nh", "restarts", "nseg", "node_ids"]
    jobs = pd.concat([jobs[cols], canc[cols]], ignore_index=True)
    jobs["kill_uid"] = 0
    pk.jobs = jobs.sort_values(["submit_h", "jobid"]).reset_index(drop=True)
    # node events (unplanned intervals and maintenance rows), reasons as the operators typed them
    rows = []
    for i, iv in enumerate(w.node_intervals):
        if iv["start"] >= cut_h or iv["end"] < log_from:
            continue
        rows.append({"node": iv["node"], "start_h": iv["start"], "end_h": min(iv["end"], cut_h) if iv["end"] <= cut_h else np.nan,
                     "state": iv["state"], "reason": reason_text(w.seed, i, iv), "user": OPERATORS[rng_for(w.seed, "op", i).integers(len(OPERATORS))],
                     "kind": "unplanned"})
    for k, mw in enumerate(w.maint):
        if mw["start"] >= cut_h or mw["end"] < log_from:
            continue
        txt = maint_text(w.seed, k, mw)
        who = OPERATORS[rng_for(w.seed, "mop", k).integers(len(OPERATORS) - 1)]
        for node in range(P.N_NODES):
            if sim.hrs(P.RACK_IN_SERVICE[rack_of(node)]) > mw["start"]:
                continue
            rows.append({"node": node, "start_h": mw["start"], "end_h": mw["end"], "state": "DRAIN", "reason": txt,
                         "user": who, "kind": "maintenance"})
    ev = pd.DataFrame(rows)
    # scheduler restarts cut the rows that span them in two
    cuts = [t for t in w.restarts if t < cut_h]
    out = []
    for r in ev.to_dict("records"):
        s, e = r["start_h"], r["end_h"]
        pieces = [s] + [t for t in cuts if s < t < (e if not (isinstance(e, float) and math.isnan(e)) else cut_h)]
        for a, b in zip(pieces, pieces[1:] + [e]):
            q = dict(r)
            q["start_h"], q["end_h"] = a, b
            out.append(q)
    ev = pd.DataFrame(out)
    pk.events = ev.sort_values(["start_h", "node"]).reset_index(drop=True)
    pk.restarts_h = cuts
    pk.rack = pd.DataFrame({"node": range(P.N_NODES)})
    pk.rack["name"] = [node_name(i) for i in range(P.N_NODES)]
    pk.rack["rack"] = [rack_of(i) for i in range(P.N_NODES)]
    pk.rack["switch"] = [switch_of(i) for i in range(P.N_NODES)]
    pk.rack["pdu"] = [pdu_of(i) for i in range(P.N_NODES)]
    pk.rack["in_service_h"] = [sim.hrs(P.RACK_IN_SERVICE[rack_of(i)]) for i in range(P.N_NODES)]
    g = []
    for gr in w.grants:
        pr = w.projects[gr["project"]]
        g.append({"project": gr["project"], "category": pr["category"], "first_year": pr["first_year"],
                  "year": gr["year"], "granted": gr["granted"], "requested": gr["requested"]})
    pk.grants = pd.DataFrame(g)
    rq = []
    for r in w.requests:
        pr = w.projects[r["project"]]
        rq.append({"project": r["project"], "category": pr["category"], "first_year": pr["first_year"],
                   "requested": r["requested"], "new": r["new"]})
    pk.requests = pd.DataFrame(rq)
    pk.maint = pd.DataFrame([{"start_h": m["start"], "end_h": m["end"], "kind": m["kind"]} for m in w.maint
                             if m["month"] >= dt.date(2024, 1, 1)])
    pk.limits = {"normal": [(sim.hrs(d), l) for d, l in P.QOS_NORMAL_LIMITS] + [(sim.hrs(P.QOS_NORMAL_2027[0]), P.QOS_NORMAL_2027[1])],
                 "short": P.QOS_SHORT}
    pk.projects = {pid: {"category": pr["category"], "first_year": pr["first_year"], "pi": pr["pi"],
                         "members": list(pr["members"]), "title": pr["title"], "university": pr["university"],
                         "institute": pr["institute"]} for pid, pr in w.projects.items()}
    pk.users = w.users
    pk.report = capacity_report(pk)
    return pk


# ---------------------------------------------------------------- the capacity report (the context artifact)
def week_starts(first, last):
    """Monday 00:00 local of every week from the week holding `first` to the one holding `last`"""
    d = first - dt.timedelta(days=first.weekday())
    out = []
    while d <= last:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def nodes_in_service(pk, a, b):
    """mean nodes in service over [a, b) in hours"""
    tot = 0.0
    for h in pk.rack["in_service_h"].values:
        tot += max(0.0, b - max(a, h))
    return tot / (b - a)


def delivered(pk, a, b):
    s, e = pk.seg["start_h"].values, pk.seg["end_h"].fillna(pk.cut_h).values
    ov = np.clip(np.minimum(e, b) - np.maximum(s, a), 0.0, None)
    return float((ov * pk.seg["nodes"].values).sum())


def lost_node_hours(pk, a, b, unplanned_only=True):
    ev = pk.events
    if unplanned_only:
        ev = ev[ev["kind"] == "unplanned"]
    s = ev["start_h"].values
    e = ev["end_h"].fillna(pk.cut_h).values
    ov = np.clip(np.minimum(e, b) - np.maximum(s, a), 0.0, None)
    if unplanned_only:
        # outside maintenance windows: subtract the overlap with windows
        m = pk.maint
        for ms, me in zip(m["start_h"].values, m["end_h"].values):
            lo, hi = max(a, ms), min(b, me)
            if hi <= lo:
                continue
            ov -= np.clip(np.minimum(e, hi) - np.maximum(s, lo), 0.0, None)
    return float(ov.sum())


def waits_in(pk, a, b):
    j = pk.jobs
    m = (j["elig_h"].values >= a) & (j["elig_h"].values < b) & ~np.isnan(j["start_h"].values)
    return (j["start_h"].values - j["elig_h"].values)[m]


def capacity_report(pk):
    first = dt.date(2024, 1, 1)
    last = P.CUT_DATE
    rows = []
    for ws in week_starts(first, last):
        a = sim.hrs(dt.datetime(ws.year, ws.month, ws.day, tzinfo=P.TZ))
        b = sim.hrs(dt.datetime.combine(ws + dt.timedelta(days=7), dt.time(), tzinfo=P.TZ))
        if ws + dt.timedelta(days=6) > last:
            continue
        nis = nodes_in_service(pk, a, b)
        d = delivered(pk, a, b)
        w = waits_in(pk, a, b)
        started = int(((pk.jobs["start_h"].values >= a) & (pk.jobs["start_h"].values < b)).sum())
        rows.append({"week": ws, "nodes": round(nis, 1), "delivered_nh": round(d, 1), "utilisation": round(d / (nis * (b - a)), 4),
                     "jobs_started": started, "p50_wait_h": round(float(np.percentile(w, 50)), 2) if len(w) else np.nan,
                     "p90_wait_h": round(float(np.percentile(w, 90)), 2) if len(w) else np.nan,
                     "lost_node_days": round(lost_node_hours(pk, a, b) / 24.0, 2)})
    weekly = pd.DataFrame(rows)
    q = []
    for y in (2024, 2025, 2026):
        for qq in (1, 2, 3, 4):
            a = sim.hrs(dt.datetime(y, 3 * (qq - 1) + 1, 1, tzinfo=P.TZ))
            b = sim.hrs(dt.datetime(y + (qq == 4), (3 * qq) % 12 + 1, 1, tzinfo=P.TZ))
            if b > pk.cut_h:
                continue
            w = waits_in(pk, a, b)
            q.append({"quarter": "%d Q%d" % (y, qq), "nodes": round(nodes_in_service(pk, a, b), 1),
                      "delivered_nh": round(delivered(pk, a, b), 1),
                      "utilisation": round(delivered(pk, a, b) / (nodes_in_service(pk, a, b) * (b - a)), 4),
                      "p50_wait_h": round(float(np.percentile(w, 50)), 2), "p90_wait_h": round(float(np.percentile(w, 90)), 2),
                      "lost_node_days": round(lost_node_hours(pk, a, b) / 24.0, 2)})
    return {"weekly": weekly, "quarterly": pd.DataFrame(q)}
