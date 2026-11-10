"""The depot's night: can a set of buses be recharged between each one's return and its next departure, with each
bus drawing at most the charger's power and all of them together at most the supply at the connection point?
Exact feasibility by a maximum flow over the night's time intervals (bus -> interval -> sink), plus the greedy
schedule a planner would draw (earliest departure first), which the build asserts agrees with the exact answer."""
from collections import deque


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
    """jobs: list of (name, kwh needed at the connection point, start minute, end minute) with minutes counted from
    the evening's midnight (a return at 23:40 is 1420, a departure at 05:10 next day is 1750). Returns (the total
    energy the night can deliver to these jobs under the two limits, {name: kWh delivered})."""
    pts = sorted({m for _, _, a, b in jobs for m in (a, b)})
    ivs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    cap = {"s": {}, "t": {}}
    for j, (name, kwh, a, b) in enumerate(jobs):
        cap["s"]["j%d" % j] = kwh
        cap["j%d" % j] = {}
        for k, (x, y) in enumerate(ivs):
            if a <= x and y <= b:
                cap["j%d" % j]["i%d" % k] = charger_kw * (y - x) / 60.0
    for k, (x, y) in enumerate(ivs):
        cap.setdefault("i%d" % k, {})["t"] = supply_kw * (y - x) / 60.0
    orig = {j: kwh for j, (_, kwh, _, _) in enumerate(jobs)}
    f = _maxflow(cap, "s", "t")
    got = {jobs[j][0]: orig[j] - cap["s"]["j%d" % j] for j in orig}
    return f, got


def feasible(jobs, charger_kw, supply_kw, tol=1e-6):
    need = sum(j[1] for j in jobs)
    f, _ = deliverable(jobs, charger_kw, supply_kw)
    return f >= need - tol, need - f


def greedy(jobs, charger_kw, supply_kw, step=5, rule="slack"):
    """the schedule a planner draws: in 5-minute steps the supply goes first to the bus with the least slack (the
    time to its departure less the time its remaining energy needs at full charger power), or by earliest departure
    (rule="edf"); returns the energy each job still lacks at its departure"""
    rem = {name: kwh for name, kwh, _, _ in jobs}
    start = min(a for _, _, a, _ in jobs)
    end = max(b for _, _, _, b in jobs)
    m = start
    while m < end:
        avail = supply_kw * step / 60.0
        live = [j for j in jobs if j[2] <= m and m + step <= j[3] and rem[j[0]] > 1e-9]
        if rule == "edf":
            live = sorted(live, key=lambda j: j[3])
        else:
            live = sorted(live, key=lambda j: (j[3] - m) - rem[j[0]] / charger_kw * 60.0)
        for name, kwh, a, b in live:
            take = min(rem[name], charger_kw * step / 60.0, avail)
            rem[name] -= take
            avail -= take
            if avail <= 1e-9:
                break
        m += step
    return rem


def cut_by_priority(cands, charger_kw, supply_kw):
    """cands: list of (name, kwh, start, end) in priority order; the list is cut at the first candidate the night
    cannot recharge together with those above it (the standard's rule). Returns (taken names, the first refused
    name or None, the shortfall at the refusal in kWh)."""
    taken = []
    for c in cands:
        ok, short = feasible(taken + [c], charger_kw, supply_kw)
        if not ok:
            return [t[0] for t in taken], c[0], short
        taken.append(c)
    return [t[0] for t in taken], None, 0.0
