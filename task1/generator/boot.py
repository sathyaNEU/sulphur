"""The cluster bootstrap behind the forcing check: each line's starts of a month share that month's campaign, so
whole start months are drawn with replacement within each line (a household goes with the month of its first
subscription, the paywall's and the base book's households one by one), every model is refitted and every 2027 line
revalued. Copies keep their subscriptions together under their own household and customer numbers."""
import numpy as np

import lines as LN
import models

ROWS = ["start", "title", "channel", "offer", "route", "end", "reason", "L", "ip", "kind", "tenure0", "stepup",
        "running", "withdrawn", "last", "proxy", "gross", "reading"]


def clusters(pn):
    """Each household's cluster: its first subscription's line and start month; the paywall's and the base book's
    households are their own clusters. Returns {stratum: [cluster key, ...]} and {cluster key: [row, ...]}."""
    first = {}
    for i in np.argsort(pn["start"], kind="stable"):
        h = int(pn["household"][i])
        if h not in first:
            first[h] = i
    members, strata = {}, {}
    for i, h in enumerate(pn["household"]):
        f = first[int(h)]
        c, t, m, k = int(pn["channel"][f]), int(pn["title"][f]), int(pn["start"][f]), pn["kind"][f]
        own = k == "base" or models.CH[c] == "DIR"
        key = ("h", int(h)) if own else (c, t, m)
        stratum = ("own", k == "base") if own else (c, t)
        members.setdefault(key, []).append(i)
        strata.setdefault(stratum, set()).add(key)
    return {s: sorted(v) for s, v in strata.items()}, members


def resample(pn, rng, cl=None):
    strata, members = cl or clusters(pn)
    rows, cid = [], []
    copy = 0
    for s in sorted(strata, key=str):
        keys = strata[s]
        for q in rng.integers(0, len(keys), size=len(keys)):
            for i in members[keys[q]]:
                rows.append(i)
                cid.append(copy)
            copy += 1
    rows = np.array(rows)
    out = {k: pn[k][rows] for k in ROWS}
    # each copy keeps its own customer numbers, payment fingerprints and addresses, so the links rebuild inside it
    ids = {}

    def new(k):
        return ids.setdefault(k, len(ids))
    out["customer"] = np.array([new(("c", c, int(pn["customer"][i]))) for i, c in zip(rows, cid)])
    fp = np.empty(len(rows), dtype=object)
    ad = np.empty(len(rows), dtype=object)
    for n_, (i, c) in enumerate(zip(rows, cid)):
        f = pn["fingerprint"][i]
        fp[n_] = tuple(new(("f", c, x)) for x in (f if isinstance(f, tuple) else (f,)))
        a = pn["address"][i]
        ad[n_] = tuple(new(("a", c, x)) for x in (a if isinstance(a, tuple) else (a,)))
    out["fingerprint"] = fp
    out["address"] = ad
    import panel
    out["household"] = panel.households(out["customer"], fp, ad)
    out["n"] = len(rows)
    return out


def run(pn, plan, reps, seed=11, o=None):
    o = o or models.GOLD
    rng = np.random.default_rng(seed)
    cl = clusters(pn)
    vals = []
    for r in range(reps):
        b = resample(pn, rng, cl)
        M = models.fit_all(b, o)
        v = {}
        for l, spec in plan.items():
            px, rt = LN.line_inputs(b, l)
            v[l] = models.line_value(M, l, spec["starts"], spec["offer"], px, rt, o)
        vals.append(v)
    return vals
