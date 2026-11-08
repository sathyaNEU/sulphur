"""task2 golden, computed from the cut pack: each clinician typed by the first month dictated against the
hospital's compulsory date, every audit carried to release 6.0 by the release steps measured within clinicians, each
type's word error rates under 6.0, the 2027 dictations by type and hospital (incumbents leaving at the record's rate,
leavers replaced by compulsory starters, the teaching hospitals' clinicians in post not yet dictating starting at the
compulsory date with the ramp the record's go-lives show), and the mixture each quarter makes."""
import math
from collections import defaultdict

import numpy as np

import world as W

FROZEN = "6.0"
DEC = W.mi(2026, 12)
Q27 = [(2027, q) for q in (1, 2, 3, 4)]
CEILINGS = (10, 12, 14, 16)


def months_label(t):
    y, m = divmod(t, 12)
    return "1 %s %d" % (["January", "February", "March", "April", "May", "June", "July", "August", "September",
                         "October", "November", "December"][m], W.START[0] + y)


def months(y, q):
    return [W.mi(y, 3 * (q - 1) + k + 1) for k in range(3)]


def persons(P):
    """first month, first hospital, monthly volume, last month, per person (staff numbers linked by the register)"""
    per = defaultdict(lambda: dict(vol=defaultdict(int), sites={}))
    for s, series in P.vol.items():
        p = P.person.get(s, s)
        for t, n in series.items():
            per[p]["vol"][t] += n
            per[p]["sites"][t] = P.site_of[(s, t)]
    out = {}
    for p, d in per.items():
        ts = sorted(d["vol"])
        out[p] = dict(first=ts[0], last=ts[-1], site0=d["sites"][ts[0]], site_last=d["sites"][ts[-1]],
                      vol=dict(d["vol"]))
    return out


def types(P, per, boundary=0):
    return {p: ("V" if d["first"] < P.comp[d["site0"]] + boundary else "M") for p, d in per.items()}


def release_steps(P, iters=30):
    """log release effects from within-clinician comparisons (two-way fixed effects, 6.0 the reference)"""
    rows = [(a["person"], a["release"], math.log(a["wer"])) for a in P.audits if a["e"] > 0]
    rel = sorted({r for _, r, _ in rows})
    b = {r: 0.0 for r in rel}
    a = defaultdict(float)
    for _ in range(iters):
        acc = defaultdict(list)
        for p, r, y in rows:
            acc[p].append(y - b[r])
        a = {p: float(np.mean(v)) for p, v in acc.items()}
        accr = defaultdict(list)
        for p, r, y in rows:
            accr[r].append(y - a[p])
        b = {r: float(np.mean(v)) for r, v in accr.items()}
        ref = b[FROZEN]
        b = {r: v - ref for r, v in b.items()}
    return b


def frozen_rates(P, typ, steps, how="all releases"):
    """each type's word error rates at 6.0: every audit carried by its release step, or the 6.0 audits alone"""
    out = {"V": [], "M": []}
    for a in P.audits:
        k = typ.get(a["person"])
        if k is None:
            continue
        if how == "frozen only" and a["release"] != FROZEN:
            continue
        out[k].append(a["wer"] * math.exp(-steps[a["release"]]))
    return {k: np.array(v) for k, v in out.items()}


def exit_rate(per, comp, boundary=None):
    """leavers a month among clinicians dictating, from the record (a person's last month before December 2026)"""
    at_risk = leave = 0
    for p, d in per.items():
        for t in range(max(d["first"], W.mi(2023, 1)), min(d["last"], DEC - 1) + 1):
            at_risk += 1
        if W.mi(2023, 1) <= d["last"] < DEC:
            leave += 1
    return leave / at_risk


def ramp_curve(P, per, typ, k_max=6):
    """the go-live ramp: compulsory starters' dictations in the months after a go-live against their own later months"""
    curves = []
    for h, c in P.comp.items():
        if c > DEC - 12 or c < W.mi(2022, 2):
            continue
        st = [p for p, d in per.items() if typ[p] == "M" and d["site0"] == h and c <= d["first"] <= c + 3]
        steady = np.mean([sum(per[p]["vol"].get(t, 0) for p in st) for t in range(c + 6, c + 12)])
        curves.append([sum(per[p]["vol"].get(c + k, 0) for p in st) / steady for k in range(k_max)])
    return [float(x) for x in np.mean(np.array(curves), axis=0)]


def steady_volume(per, typ, kind, months_from=W.mi(2026, 1)):
    v = [np.mean([n for t, n in d["vol"].items() if t >= months_from and t >= d["first"] + 3])
         for p, d in per.items() if typ[p] == kind and d["last"] >= months_from + 3 and
         any(t >= months_from and t >= d["first"] + 3 for t in d["vol"])]
    return float(np.mean(v))


def project(P, per, typ, rates, lam, ramp, vM, starters="M", use_ramp=True, incumbents_flat=False, inc_months=3):
    """2027 dictations by month, hospital and kind (the incumbents' own kind, starters the given kind)"""
    share = {k: float(np.mean(v > W.LINE)) for k, v in rates.items()}
    inc = {p: d for p, d in per.items() if d["last"] == DEC}
    vol_inc = {p: float(np.mean([d["vol"].get(t, 0) for t in range(DEC - inc_months + 1, DEC + 1)])) for p, d in inc.items()}
    sites = sorted(P.comp)
    by_site = defaultdict(list)
    for p, d in inc.items():
        by_site[d["site_last"]].append(p)
    out = {}
    for t in range(W.mi(2027, 1), W.mi(2027, 12) + 1):
        s = 1.0 if incumbents_flat else math.exp(-lam * (t - DEC))
        for h in sites:
            mine = by_site[h]
            v = defaultdict(float)
            for p in mine:
                v[typ[p]] += vol_inc[p] * s
            gone = sum(vol_inc[p] for p in mine) * (1 - s)
            c = P.comp[h]
            if c <= DEC:
                v[starters] += gone                               # leavers replaced by starters
            elif t < c:
                v["V"] += gone                                    # before the date the dictating count holds
            else:
                a = t - c
                r = (ramp[a] if a < len(ramp) else 1.0) if use_ramp else 1.0
                new = P.staff_in_post[h] - len(mine)
                sc = 1.0 if incumbents_flat else math.exp(-lam * (t - c))
                v[starters] += new * vM * (r * sc + (1 - sc))     # the go-live's starters, their leavers replaced
                v[starters] += gone                               # incumbents' leavers since December replaced
            out[(t, h)] = dict(v)
    return out, share


def figures(out, rates, share, sel=None):
    q = {}
    sites = {k[1] for k in out}
    for (y, qq) in Q27:
        ms = months(y, qq)
        wts = defaultdict(float)
        for t in ms:
            for h in sites:
                if sel is None or h in sel:
                    for k, x in out[(t, h)].items():
                        wts[k] += x
        tot = sum(wts.values())
        q[(y, qq)] = dict(vol=tot, share=sum(x * share[k] for k, x in wts.items()) / tot,
                          wV=wts.get("V", 0.0) / tot, p90=mix_quantile(rates, {k: x / tot for k, x in wts.items()}, 0.9))
    return q


def mix_quantile(rates, w, p):
    srt = {k: np.sort(rates[k]) for k in w if w[k] > 0}
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        cdf = sum(w[k] * np.searchsorted(v, mid, side="right") / len(v) for k, v in srt.items())
        if cdf < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def ceiling(qfigs):
    m = 100 * max(f["share"] for f in qfigs.values())
    return next((c for c in CEILINGS if m <= c), None)


def golden(P, **kw):
    per = persons(P)
    typ = types(P, per, kw.get("boundary", 0))
    steps = release_steps(P)
    rates = frozen_rates(P, typ, steps, kw.get("rates_how", "all releases"))
    lam = exit_rate(per, P.comp)
    ramp = ramp_curve(P, per, typ)
    vM = steady_volume(per, typ, "M", months_from=kw.get("vm_from", W.mi(2026, 1)))
    if kw.get("starter_rates") is not None:
        rates = dict(rates, S=kw["starter_rates"](P, per, typ, rates, steps))
    out, share = project(P, per, typ, rates, lam, ramp, vM, starters="S" if "S" in rates else "M",
                         use_ramp=kw.get("use_ramp", True), incumbents_flat=kw.get("incumbents_flat", False),
                         inc_months=kw.get("inc_months", 3))
    q = figures(out, rates, share)
    hq = {h: figures(out, rates, share, sel={h})[(2027, 4)] for h in sorted(P.comp)}
    hq4 = {h: f["share"] for h, f in hq.items()}
    hp90 = {h: f["p90"] for h, f in hq.items()}
    return dict(per=per, typ=typ, steps=steps, rates=rates, lam=lam, ramp=ramp, vM=vM, out=out, share=share, q=q,
                hq4=hq4, hp90=hp90, ceiling=ceiling(q), bands=bands(q), first_past=first_past(q))


def band(x):
    return next((c for c in CEILINGS if 100 * x <= c), None)


def bands(q):
    return [band(q[k]["share"]) for k in Q27]


def first_past(q):
    """for each ceiling below the call, the first 2027 quarter whose share passes it"""
    out = {}
    for c in CEILINGS:
        k = next((i + 1 for i, kk in enumerate(Q27) if 100 * q[kk]["share"] > c), None)
        if k is None:
            break
        out[c] = k
    return out
