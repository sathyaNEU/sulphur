"""task9: the clean truth an analyst would reconstruct from the pack, read straight off the world.

checks.py runs the easy routes and the rivals on these arrays (dataset-generation 7.1: the easy route executed on the
clean truth), and analysis.py must land on the same arrays from the shipped files.
"""
import collections
import datetime as dt

import numpy as np

import world as WD


def panel(W, clock="buy", covered_only=True):
    """Company-years at risk from 2008: a loan outstanding on 1 January (and reported to Lenderbase), its default in
    the year. Columns: company, year, fund, sector, rating, age, defaulted, house."""
    byc = collections.defaultdict(list)
    for L in W.loans:
        byc[L["comp"]].append(L)
    rows = []
    for (c, y, f, k, r, age, d) in W.cy:
        if y < WD.DB0:
            continue
        jan = dt.date(int(y), 1, 1)
        cur = [L for L in byc[c] if L["orig"] < jan and (L["end"] is None or L["end"] >= jan)]
        if not cur:
            continue
        L = cur[-1]
        if covered_only and not L["covered"]:
            continue
        a = age if clock == "buy" else int(y) - L["orig"].year
        rows.append((c, int(y), f, k, L["rating"], max(a, 1), d, W.funds[f]["house"]))
    return np.array(rows, dtype=np.int64)


def port(W, comps, clock="buy", year=2027):
    loans = [W.loans[W.comps[c]["loan"]] for c in comps]
    w = np.array([L["size"] for L in loans], dtype=float)
    w = w / w.sum()
    if clock == "buy":
        a = np.array([year - W.comps[c]["buy_year"] for c in comps])
    else:
        a = np.array([year - L["orig"].year for L in loans])
    return dict(w=w, r=np.array([L["rating"] for L in loans]), a=np.maximum(a, 1),
                k=np.array([W.comps[c]["ind"] for c in comps]),
                h=np.array([W.funds[W.owner[c]]["house"] for c in comps]),
                f=np.array([W.owner[c] for c in comps]))


def lgd(W, mature_to=2021, cut=WD.AS_OF):
    """Loss given default three ways over the reported defaults: every workout's true outcome (unknowable), the
    defaults old enough to have closed, and the workouts closed by the cut (complete cases)."""
    D = [L for L in W.loans if L["status"] == "default" and L["covered"] and L["end"].year >= WD.DB0]
    every = 1 - np.mean([L["recovery"] for L in D])
    mature = 1 - np.mean([L["recovery"] for L in D if L["end"].year <= mature_to])
    closed = 1 - np.mean([L["recovery"] for L in D if L["resolved"] <= cut])
    open_n = sum(1 for L in D if L["resolved"] > cut)
    return dict(every=float(every), mature=float(mature), closed=float(closed), n=len(D), open=open_n)
