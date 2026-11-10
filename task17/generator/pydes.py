"""An independent scheduler in plain Python for the verifier: first come first served by eligible time with
conservative backfill on requested walltime over whole nodes, node outages that kill and requeue the job on the
node (restarting from its last checkpoint after a short hold), maintenance windows that no job may run into, and
dependency and follow-up links. Written from the configuration's description, not from des.c; the two are compared
on identical inputs by checks.py."""
import heapq

import numpy as np


def simulate(n_nodes, jobs, outages, maint, t_end, bf_max=100, hold=0.05):
    submit = np.asarray(jobs["submit"], dtype=float)
    nodes = np.asarray(jobs["nodes"], dtype=int)
    wall = np.asarray(jobs["wall"], dtype=float)
    dur = np.asarray(jobs["dur"], dtype=float)
    ckpt = np.asarray(jobs["ckpt"], dtype=float)
    dep = np.asarray(jobs["dep"], dtype=int)
    after = np.asarray(jobs["after"], dtype=int)
    after_delay = np.asarray(jobs["after_delay"], dtype=float)
    endstate = np.asarray(jobs["endstate"], dtype=int)
    n = len(submit)
    o_node, o_start, o_end = [np.asarray(x) for x in outages]
    m_start, m_end = [np.asarray(x, dtype=float) for x in maint]
    # event tie order: 0 outage end, 1 maintenance end, 2 arrival, 3 requeue release, 4 job end, 5 outage start,
    # 6 maintenance start
    ev = []
    for j in range(n):
        if after[j] < 0:
            heapq.heappush(ev, (submit[j], 2, j, 0))
    for i in range(len(o_node)):
        heapq.heappush(ev, (o_start[i], 5, i, 0))
        heapq.heappush(ev, (o_end[i], 0, i, 0))
    for i in range(len(m_start)):
        heapq.heappush(ev, (m_start[i], 6, i, 0))
        heapq.heappush(ev, (m_end[i], 1, i, 0))
    status = np.zeros(n, dtype=int)        # 0 unsubmitted 1 queued 2 running 3 done 4 held 5 waiting on dependency
    elig = submit.copy()
    remaining = dur.copy()
    restarts = np.zeros(n, dtype=int)
    epoch = np.zeros(n, dtype=int)
    seg_start = np.zeros(n)
    first_start = np.full(n, -1.0)
    final_end = np.full(n, -1.0)
    final_state = np.full(n, -1, dtype=int)
    nh = np.zeros(n)
    rework = np.zeros(n)
    sub_out = submit.copy()
    node_job = [-1] * n_nodes
    node_down = [0] * n_nodes
    job_nodes = {}
    queue = []                               # sorted list of (elig, j)
    dependents = {}
    followers = {}
    for j in range(n):
        if dep[j] >= 0:
            dependents.setdefault(dep[j], []).append(j)
        if after[j] >= 0:
            followers.setdefault(after[j], []).append(j)
    segments = []
    next_maint = 0

    def q_insert(j):
        import bisect
        bisect.insort(queue, (elig[j], j))
        status[j] = 1

    def start(j, t):
        need = nodes[j]
        got = []
        for k in range(n_nodes):
            if need == 0:
                break
            if node_down[k] == 0 and node_job[k] < 0:
                node_job[k] = j
                got.append(k)
                need -= 1
        job_nodes[j] = got
        status[j] = 2
        seg_start[j] = t
        if first_start[j] < 0:
            first_start[j] = t
        run = min(remaining[j], wall[j])
        epoch[j] += 1
        heapq.heappush(ev, (t + run, 4, j, epoch[j]))

    def kill(k, t):
        j = node_job[k]
        if j < 0:
            return
        e = t - seg_start[j]
        done = 0.0
        if ckpt[j] > 0:
            done = np.floor(e / ckpt[j] + 1e-9) * ckpt[j]
        done = min(done, remaining[j])
        rework[j] += (e - done) * nodes[j]
        nh[j] += e * nodes[j]
        segments.append((j, restarts[j], seg_start[j], t, 4, tuple(job_nodes[j])))
        for kk in job_nodes[j]:
            node_job[kk] = -1
        remaining[j] -= done
        restarts[j] += 1
        epoch[j] += 1
        status[j] = 4
        heapq.heappush(ev, (t + hold, 3, j, 0))

    def earliest(profile, t, free_now, w, W):
        avail = free_now
        cand = t
        ok = avail >= w
        i = 0
        while i < len(profile):
            tau = profile[i][0]
            if ok and tau - cand >= W:
                return cand
            while i < len(profile) and profile[i][0] == tau:
                avail += profile[i][1]
                i += 1
            if avail >= w:
                if not ok:
                    cand, ok = tau, True
            else:
                ok = False
        return cand if ok else float("inf")

    def schedule(t):
        import bisect
        if not queue:
            return
        free = sum(1 for k in range(n_nodes) if node_down[k] == 0 and node_job[k] < 0)
        profile = []
        seen = set()
        for k in range(n_nodes):
            j = node_job[k]
            if j >= 0 and j not in seen:
                seen.add(j)
                profile.append((seg_start[j] + wall[j], nodes[j]))
        for i in range(next_maint, len(m_start)):
            if m_end[i] <= t:
                continue
            profile.append((max(m_start[i], t), -n_nodes))
            profile.append((m_end[i], n_nodes))
        profile.sort()
        tested = 0
        pos = 0
        while pos < len(queue) and tested < bf_max:
            _, j = queue[pos]
            tested += 1
            w, W = nodes[j], wall[j]
            ts = earliest(profile, t, free, w, W)
            if ts == t:
                queue.pop(pos)
                start(j, t)
                free -= w
                bisect.insort(profile, (t + W, w))
                continue
            if ts < float("inf"):
                bisect.insort(profile, (ts, -w))
                bisect.insort(profile, (ts + W, w))
            pos += 1

    while ev:
        t, typ, a, b = heapq.heappop(ev)
        if t > t_end:
            break
        need = False
        while True:
            if typ == 2:
                j = a
                if dep[j] >= 0 and status[dep[j]] != 3:
                    status[j] = 5
                else:
                    de = final_end[dep[j]] if dep[j] >= 0 else -1.0
                    elig[j] = max(de, t) if de > submit[j] else t
                    q_insert(j)
                need = True
            elif typ == 3:
                q_insert(a)
                need = True
            elif typ == 4:
                j = a
                if b == epoch[j] and status[j] == 2:
                    e = t - seg_start[j]
                    st = endstate[j] if remaining[j] <= wall[j] + 1e-9 else 1
                    nh[j] += e * nodes[j]
                    segments.append((j, restarts[j], seg_start[j], t, st, tuple(job_nodes[j])))
                    for kk in job_nodes[j]:
                        node_job[kk] = -1
                    status[j] = 3
                    final_end[j] = t
                    final_state[j] = st
                    for d in dependents.get(j, []):
                        if status[d] == 5:
                            elig[d] = max(t, submit[d])
                            q_insert(d)
                    for f in followers.get(j, []):
                        if status[f] == 0:
                            sub_out[f] = t + after_delay[f]
                            heapq.heappush(ev, (sub_out[f], 2, f, 0))
                    need = True
            elif typ == 5:
                k = int(o_node[a])
                kill(k, t)
                node_down[k] += 1
            elif typ == 0:
                k = int(o_node[a])
                if node_down[k] > 0:
                    node_down[k] -= 1
                need = True
            elif typ == 6:
                for k in range(n_nodes):
                    kill(k, t)
                    node_down[k] += 1
            elif typ == 1:
                for k in range(n_nodes):
                    if node_down[k] > 0:
                        node_down[k] -= 1
                next_maint = a + 1
                need = True
            if not ev or ev[0][0] > t:
                break
            t, typ, a, b = heapq.heappop(ev)
        if need:
            schedule(t)
    return {"first_start": first_start, "final_end": final_end, "final_state": final_state, "restarts": restarts,
            "nh": nh, "rework": rework, "submit": sub_out, "segments": segments}
