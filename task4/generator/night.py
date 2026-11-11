"""The depot's night: can a set of buses be recharged between each one's return and its next departure, with each
bus drawing at most the charger's power and all of them together at most the supply at the connection point?
A job is (name, kWh of recharge at the connection point, start minute, end minute[, load kW]): the load is what the
bus takes through its charger beside the recharge for as long as it is plugged in and released (it is drawn at a
steady rate over the whole window, so it takes its share of the supply and of the charger in every interval).
Exact feasibility by a maximum flow over the night's time intervals (bus -> interval -> sink), the schedules a
planner would draw (least slack first, or earliest departure first), and the least supply at which a set fits."""
from collections import deque


def _load(job):
    return job[4] if len(job) > 4 else 0.0


def _maxflow(cap, s, t):
    """Edmonds-Karp on an adjacency dict of dicts; returns the flow value."""
    flow = 0
    while True:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 1e-9 and v not in parent:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            return flow
        f = float("inf")
        v = t
        while parent[v] is not None:
            u = parent[v]
            f = min(f, cap[u][v])
            v = u
        v = t
        while parent[v] is not None:
            u = parent[v]
            cap[u][v] -= f
            cap[v].setdefault(u, 0.0)
            cap[v][u] += f
            v = u
        flow += f


def deliverable(jobs, charger_kw, supply_kw):
    """jobs: list of (name, kwh, start minute, end minute[, load kW]) with minutes counted from the evening's midnight
    (a return at 23:40 is 1420, a departure at 05:10 next day is 1750). Returns (the recharge energy the night can
    deliver to these jobs under the two limits, {name: kWh delivered}, the steady loads' energy the supply could not
    carry)."""
    pts = sorted({m for j in jobs for m in (j[2], j[3])})
    ivs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    cap = {"s": {}, "t": {}}
    over = 0.0
    for j, job in enumerate(jobs):
        name, kwh, a, b = job[:4]
        cap["s"]["j%d" % j] = kwh
        cap["j%d" % j] = {}
        for k, (x, y) in enumerate(ivs):
            if a <= x and y <= b:
                cap["j%d" % j]["i%d" % k] = max(0.0, charger_kw - _load(job)) * (y - x) / 60.0
    for k, (x, y) in enumerate(ivs):
        held = sum(_load(job) for job in jobs if job[2] <= x and y <= job[3])
        over += max(0.0, held - supply_kw) * (y - x) / 60.0
        cap.setdefault("i%d" % k, {})["t"] = max(0.0, supply_kw - held) * (y - x) / 60.0
    orig = {j: job[1] for j, job in enumerate(jobs)}
    f = _maxflow(cap, "s", "t")
    got = {jobs[j][0]: orig[j] - cap["s"]["j%d" % j] for j in orig}
    return f, got, over


def feasible(jobs, charger_kw, supply_kw, tol=1e-6):
    need = sum(j[1] for j in jobs)
    f, _, over = deliverable(jobs, charger_kw, supply_kw)
    short = need - f + over
    return short <= tol, short


def greedy(jobs, charger_kw, supply_kw, step=5, rule="slack"):
    """the schedule a planner draws: in 5-minute steps the supply left after the plugged-in buses' steady loads goes
    first to the bus with the least slack (the time to its departure less the time its remaining energy needs at the
    charger's power left after its own load), or by earliest departure (rule="edf"); returns the energy each job still
    lacks at its departure"""
    rem = {job[0]: job[1] for job in jobs}
    start = min(job[2] for job in jobs)
    end = max(job[3] for job in jobs)
    m = start
    while m < end:
        present = [job for job in jobs if job[2] <= m and m + step <= job[3]]
        avail = max(0.0, supply_kw - sum(_load(job) for job in present)) * step / 60.0
        live = [job for job in present if rem[job[0]] > 1e-9]
        if rule == "edf":
            live = sorted(live, key=lambda j: j[3])
        else:
            live = sorted(live, key=lambda j: (j[3] - m) - rem[j[0]] / max(1e-6, charger_kw - _load(j)) * 60.0)
        for job in live:
            take = min(rem[job[0]], max(0.0, charger_kw - _load(job)) * step / 60.0, avail)
            rem[job[0]] -= take
            avail -= take
            if avail <= 1e-9:
                break
        m += step
    return rem


def cut_by_priority(cands, charger_kw, supply_kw):
    """cands: list of jobs in priority order; the list is cut at the first candidate the night cannot recharge
    together with those above it (the standard's rule). Returns (taken names, the first refused name or None, the
    shortfall at the refusal in kWh)."""
    taken = []
    for c in cands:
        ok, short = feasible(taken + [c], charger_kw, supply_kw)
        if not ok:
            return [t[0] for t in taken], c[0], short
        taken.append(c)
    return [t[0] for t in taken], None, 0.0


def least_supply(jobs, charger_kw, lo=0.0, hi=5000.0, tol=0.25):
    """the least supply at the connection point at which every job fits (a bisection on the exact feasibility)"""
    if not feasible(jobs, charger_kw, hi)[0]:
        return float("inf")
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if feasible(jobs, charger_kw, mid)[0]:
            hi = mid
        else:
            lo = mid
    return hi
