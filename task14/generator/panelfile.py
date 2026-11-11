"""The Statistics Office's rent survey as its collection system exports it, and the survey-based private rents index the
Office has published from it each quarter.

Each panel dwelling reports the weekly rent payable on the fifteenth of the quarter's middle month, the current
tenancy's start date, the kind of landlord and whether an agent manages it. A dwelling that leaves the rental market is
out of scope from that quarter and is replaced by another from the same stratum of the frame the panel was drawn from.
The published index chains each quarter's rents to the last over the dwellings reporting in both, with the design
weights; dwellings vacant or not responding on either reference day are left out of that link."""
import numpy as np
import pandas as pd

import params as P
import world as WD


def owner_on(W, tid, n):
    o = int(W.T["owner0"][tid])
    for t, kind, d, ow in W._ev_by_t.get(tid, []):
        if kind == "transfer" and d <= n:
            o = ow
    return o


def _ev_index(W):
    if hasattr(W, "_ev_by_t"):
        return
    W._ev_by_t = {}
    for t, kind, d, o in zip(W.EV["tenancy"], W.EV["kind"], W.EV["date"], W.EV["owner"]):
        W._ev_by_t.setdefault(int(t), []).append((int(t), str(kind), int(d), int(o)))
    for v in W._ev_by_t.values():
        v.sort(key=lambda x: x[2])


def pso_address(W, d):
    si = int(W.dw["suburb"][d])
    name, stype = W.streets[si][int(W.dw["street"][d])]
    num = int(W.dw["number"][d])
    unit = W.dw["unit"][d]
    if unit:
        return "Flat %s, %d %s %s" % (unit, num, name, stype)
    return "%d %s %s" % (num, name, stype)


def build(W, seed=P.SEED + 23):
    rng = np.random.default_rng(seed)
    _ev_index(W)
    dws = sorted(set(r[1] for r in W.panel_rows))
    refs = rng.choice(np.arange(10000, 99999), size=len(dws), replace=False)
    ref_of = {d: "RS%05d" % r for d, r in zip(dws, refs)}
    weights = {k: v["N"] / v["n"] for k, v in W.panel_strata.items()}
    rows = []
    stratum_of = {}
    for slot, d, yq, rd, status, tid, repl in W.panel_rows:
        code = P.REGION_CODES[int(W.dw["region"][d])]
        dt_ = W.dw["dtype"][d]
        key = (code, dt_)
        stratum_of[d] = key
        si = int(W.dw["suburb"][d])
        sub = W.suburbs[si]
        q = "%dQ%d" % yq
        resp = {"R": "R", "N": "N", "V": "V", "X": "O"}[status]
        rent = start = ltype = agent = ""
        if status in ("R",) and tid >= 0:
            rent = WD.rent_on(W, tid, rd)
            start = WD.date_of(int(W.T["start"][tid])).isoformat()
        if tid >= 0:
            o = owner_on(W, tid, rd)
            ltype = "C" if W.owners[o]["kind"] == "company" else "I"
            agent = "Y" if W.owners[o]["agent"] is not None else "N"
        rows.append([ref_of[d], "%s-%s" % key, round(weights[key], 2), q, WD.date_of(rd).isoformat(), resp,
                     rent, start, ltype, agent, pso_address(W, d), sub["name"], sub["postcode"], code,
                     ref_of[repl] if (repl is not None and repl in ref_of) else ""])
    cols = ["dwelling_ref", "stratum", "design_weight", "quarter", "reference_date", "response", "weekly_rent",
            "tenancy_start", "landlord_type", "agent_managed", "address", "suburb", "postcode", "region", "replaces"]
    F = pd.DataFrame(rows, columns=cols)
    F = F.sort_values(["quarter", "dwelling_ref"], kind="stable").reset_index(drop=True)
    W.panel_ref_of = ref_of
    return F


def published_series(F):
    """The Office's survey-based index: each quarter chained to the last over dwellings reporting a rent in both,
    weighted by the design weight; June quarter 2018 = 1000; annual change in per cent. National and by region."""
    R = F[F["response"] == "R"].copy()
    R["rent"] = R["weekly_rent"].astype(float)
    quarters = sorted(R["quarter"].unique(), key=lambda s: (int(s[:4]), int(s[-1])))
    out = {}
    for g in ["NAT"] + P.REGION_CODES:
        sub = R if g == "NAT" else R[R["region"] == g]
        idx = {}
        lvl = 1000.0
        base_q = "2018Q2"
        level = {quarters[0]: 1.0}
        for i in range(1, len(quarters)):
            a = sub[sub["quarter"] == quarters[i - 1]].set_index("dwelling_ref")
            b = sub[sub["quarter"] == quarters[i]].set_index("dwelling_ref")
            c = a.index.intersection(b.index)
            ratio = float((b.loc[c, "design_weight"] * b.loc[c, "rent"]).sum() /
                          (a.loc[c, "design_weight"] * a.loc[c, "rent"]).sum())
            level[quarters[i]] = level[quarters[i - 1]] * ratio
        base = level[base_q]
        for qq in quarters:
            idx[qq] = 1000.0 * level[qq] / base
        out[g] = idx
    return quarters, out
