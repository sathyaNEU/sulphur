"""task8: every graded result, computed from the loaded pack (load.py) under a set of options. The golden's options
are GOLD; the rivals and the hurried routes change one or more of them (routes.py).

R1  students on roll with a valid entry sitting by the census, by academy, and those without one
R2  the second-sitting gain on the Brightway academies' Lexis trial (standardised score points)
R3  the Lexis score of a Brightway result at 70, 75, 80, 85, 90 and 95
R4  the Lexis score of a Quill result at 70, 75, 80, 85, 90 and 95
R5  how far the July transition-day Lexis sittings stand above the start of Year 7 (points)
R6  Reading Forward students by academy, and the trust's total
R7  the change from each academy's own-test list, by academy and by test
R8  the trust's tutor hours a week and the year's cost, with a range (results.boot)
R9  tutor hours a week by academy"""
import datetime as dt
import math

import numpy as np

import link
import params as P

GOLD = dict(degree=6, quill="chained", brightway="trial", gain="did", july="ks2", ks2_link="equi", ref="sept",
            fe_weight=0.5, dip_stat="mean", gain_stat="mean", trial_academies="all", resit="as_recorded")
POINTS = [70, 75, 80, 85, 90, 95]
KR, LR, QR, BR = (80, 120), (69, 141), (69, 141), (69, 131)


def opts(**kw):
    o = dict(GOLD)
    o.update(kw)
    return o


def whole(x):
    return int(math.floor(x + 0.5))


def first_valid(s):
    for x in s["sittings"]:
        if x["valid"] and x["date"] <= P.CENSUS and x["sas"] is not None:
            return x
    return None


def own_first(s):
    for x in s["sittings"]:
        if x["valid"] and x["test"] == s["test"].upper() and x["sas"] is not None:
            return x
    return None


def samples(D):
    """The linking samples the records give: the September Lexis academies' first sittings with KS2 (the reference),
    the Quill academies' first sittings with KS2, the Brightway academies' pairs, the July sittings with KS2."""
    ref, quill, july, pairs = [], [], [], []
    for s in D["students"]:
        f = first_valid(s)
        test = s["test"].upper()
        if f is not None and s["ks2"] is not None and f["academy"] == s["academy"]:
            if test == "LEXIS" and f["test"] == "LEXIS" and f["date"].month >= 9:
                ref.append((s["ks2"], f["sas"], s))
            if test == "LEXIS" and f["test"] == "LEXIS" and f["date"].month == 7:
                july.append((s["ks2"], f["sas"], s))
            if test == "QUILL" and f["test"] == "QUILL":
                quill.append((s["ks2"], f["sas"], s))
        if test == "BRIGHTWAY":
            b = [x for x in s["sittings"] if x["test"] == "BRIGHTWAY" and x["valid"] and x["academy"] == s["academy"]]
            l = [x for x in s["sittings"] if x["test"] == "LEXIS" and x["valid"] and x["academy"] == s["academy"]]
            if b and l:
                pairs.append((b[0], l[0], s))
    return dict(ref=ref, quill=quill, july=july, pairs=pairs)


def ks2_lexis(sm, o):
    K = [k for k, _, _ in sm["ref"]]
    L = [l for _, l, _ in sm["ref"]]
    if o["ks2_link"] == "regression":
        b = np.polyfit(K, L, 1)
        return lambda x: np.polyval(b, np.asarray(x, float))
    return link.equi(K, L, KR, LR, degree=o["degree"])


def quill_lexis(sm, o, eKL):
    Q = [q for _, q, _ in sm["quill"]]
    KQ = [k for k, _, _ in sm["quill"]]
    if o["quill"] == "chained":
        return link.Chain(link.equi(Q, KQ, QR, KR, degree=o["degree"]), eKL)
    if o["quill"] == "linear":
        return link.Chain(link.linear(Q, KQ), link.linear([k for k, _, _ in sm["ref"]], [l for _, l, _ in sm["ref"]]))
    if o["quill"] == "fe":
        return link.freq_estimation(Q, KQ, [k for k, _, _ in sm["ref"]], [l for _, l, _ in sm["ref"]], QR, KR, LR,
                                    w1=o["fe_weight"], degree=o["degree"])
    if o["quill"] == "regression":
        b1 = np.polyfit(Q, KQ, 1)
        b2 = np.polyfit([k for k, _, _ in sm["ref"]], [l for _, l, _ in sm["ref"]], 1)
        return lambda x: np.polyval(b2, np.polyval(b1, np.asarray(x, float)))
    if o["quill"] == "zscore":
        L = np.array([l for _, l, _ in sm["ref"]], float)
        qq = np.array(Q, float)
        return link.Linear(qq.mean(), qq.std(), L.mean(), L.std())
    return lambda x: np.asarray(x, float)        # nominal: the Quill score read as a Lexis score


def gain(sm, o):
    """The second-sitting gain from the academy where both orders occur: half the difference between its
    Lexis-minus-Brightway gaps when Lexis came second and when it came first."""
    if o["gain"] == "none":
        return 0.0
    by = {}
    for b, l, s in sm["pairs"]:
        by.setdefault(s["academy"], []).append((b, l))
    stat = np.mean if o["gain_stat"] == "mean" else np.median
    if o["gain"] == "did":
        # the academies where both orders occur, each academy's own two gaps compared
        num, den = 0.0, 0
        for ac in sorted(by):
            prs = by[ac]
            first = [l["sas"] - b["sas"] for b, l in prs if l["date"] < b["date"]]
            second = [l["sas"] - b["sas"] for b, l in prs if l["date"] > b["date"]]
            if len(first) >= 20 and len(second) >= 20:
                w = len(first) + len(second)
                num += w * (stat(second) - stat(first)) / 2
                den += w
        return float(num / den) if den else 0.0
    raise ValueError(o["gain"])


def brightway_lexis(sm, o, g, eKL):
    if o["brightway"] == "nominal":
        return lambda x: np.asarray(x, float)
    if o["brightway"] == "ks2":
        BK = [(b["sas"], s["ks2"]) for b, l, s in sm["pairs"] if s["ks2"] is not None and b["date"] < l["date"]]
        return link.Chain(link.equi([x for x, _ in BK], [k for _, k in BK], BR, KR, degree=o["degree"]), eKL)
    if o["brightway"] == "zscore":
        L = np.array([l for _, l, _ in sm["ref"]], float)
        bb = np.array([b["sas"] for b, l, s in sm["pairs"]], float)
        return link.Linear(bb.mean(), bb.std(), L.mean(), L.std())
    bs, ls = [], []
    for b, l, s in sm["pairs"]:
        if o["trial_academies"] == "fixed" and s["academy"] in P.SWITCH_ACADEMIES:
            continue
        if l["date"] > b["date"]:
            bs.append(b["sas"])
            ls.append(l["sas"] - g)
        else:
            bs.append(b["sas"] - g)
            ls.append(l["sas"])
    if o["brightway"] == "trial_linear":
        return link.linear(bs, ls)
    return link.equi(bs, ls, BR, LR, degree=o["degree"])


def july_dip(sm, o, eKL):
    if o["july"] == "none":
        return 0.0
    stat = np.mean if o["dip_stat"] == "mean" else np.median
    if o["july"] == "regression":
        K = np.array([k for k, _, _ in sm["ref"] + sm["july"]], float)
        L = np.array([l for _, l, _ in sm["ref"] + sm["july"]], float)
        J = np.array([0.0] * len(sm["ref"]) + [1.0] * len(sm["july"]))
        X = np.column_stack([np.ones(len(K)), K, J])
        return float(np.linalg.lstsq(X, L, rcond=None)[0][2])
    r_ref = stat([l - float(eKL(k)[0]) for k, l, _ in sm["ref"]])
    r_jul = stat([l - float(eKL(k)[0]) for k, l, _ in sm["july"]])
    return float(r_jul - r_ref)


def links(D, o, sm=None):
    sm = sm or samples(D)
    if o["ref"] == "all":
        # every Lexis academy's first Lexis sitting with KS2 as the reference, the July transition day's included
        sm = dict(sm, ref=sm["ref"] + sm["july"])
    eKL = ks2_lexis(sm, o)
    eQL = quill_lexis(sm, o, eKL)
    g = gain(sm, o)
    eBL = brightway_lexis(sm, o, g, eKL)
    dip = july_dip(sm, o, eKL)
    return dict(eKL=eKL, eQL=eQL, eBL=eBL, gain=g, dip=dip, sm=sm, resit=o["resit"])


def resat(s, f):
    """The first valid sitting follows a failed or short session of the same test."""
    return any(x["test"] == f["test"] and not x["valid"] and x["date"] <= f["date"] for x in s["sittings"])


def entry(s, Lk):
    f = first_valid(s)
    if f is None:
        if s["ks2"] is None:
            return None, "none"
        return float(np.asarray(Lk["eKL"](s["ks2"])).ravel()[0]), "ks2"
    off = Lk["gain"] if Lk.get("resit") == "gain" and resat(s, f) else 0.0
    if f["test"] == "LEXIS":
        if f["date"].month == 7:
            return f["sas"] - Lk["dip"] - off, "july"
        return float(f["sas"]) - off, "lexis"
    if f["test"] == "QUILL":
        return float(np.asarray(Lk["eQL"](f["sas"])).ravel()[0]) - off, "quill"
    return float(np.asarray(Lk["eBL"](f["sas"])).ravel()[0]) - off, "brightway"


def place(D, Lk):
    out = []
    for s in D["students"]:
        v, basis = entry(s, Lk)
        w = None if v is None else whole(v)
        out.append(dict(s=s, value=v, whole=w, basis=basis, placed=(w is not None and w < P.THRESHOLD)))
    return out


def own_list(D, Lk):
    """Each academy's own-test list: the first valid sitting of its own test as its own standardised score; no
    own-test sitting, the KS2 rule."""
    out = {}
    for s in D["students"]:
        f = own_first(s)
        if f is not None:
            placed = f["sas"] < P.THRESHOLD
        elif first_valid(s) is not None:
            placed = whole(entry(s, Lk)[0]) < P.THRESHOLD
        elif s["ks2"] is not None:
            placed = whole(float(np.asarray(Lk["eKL"](s["ks2"])).ravel()[0])) < P.THRESHOLD
        else:
            placed = False
        out[s["academy"]] = out.get(s["academy"], 0) + int(placed)
    return out


def all_results(D, o=GOLD):
    sm = samples(D)
    Lk = links(D, o, sm)
    pl = place(D, Lk)
    acad = sorted(D["academies"])
    r1 = {a: sum(1 for p in pl if p["s"]["academy"] == a and p["basis"] not in ("ks2", "none")) for a in acad}
    r1_none = {a: sum(1 for p in pl if p["s"]["academy"] == a and p["basis"] in ("ks2", "none")) for a in acad}
    r6 = {a: sum(1 for p in pl if p["s"]["academy"] == a and p["placed"]) for a in acad}
    own = own_list(D, Lk)
    test_of = {a: D["academies"][a]["entry_reading_test"] for a in acad}
    r7 = {a: r6[a] - own.get(a, 0) for a in acad}
    r7_test = {}
    for a in acad:
        r7_test[test_of[a]] = r7_test.get(test_of[a], 0) + r7[a]
    total = sum(r6.values())
    hours = {a: round(P.HOURS_PER_STUDENT * r6[a], 1) for a in acad}
    return dict(
        R1=r1, R1_none=r1_none, R2=Lk["gain"],
        R3={x: float(np.asarray(Lk["eBL"](x)).ravel()[0]) for x in POINTS},
        R4={x: float(np.asarray(Lk["eQL"](x)).ravel()[0]) for x in POINTS},
        R5=Lk["dip"], R6=r6, R6_total=total, R7=r7, R7_test=r7_test, own=own, own_total=sum(own.values()),
        R8_hours=round(P.HOURS_PER_STUDENT * total, 1),
        R8_cost=round(P.HOURS_PER_STUDENT * total * P.WEEKS * P.RATE, 2),
        R9=hours, placements=pl, links=Lk)


def boot(D, o=GOLD, reps=P.BOOT_REPS, seed=P.SEED + 31):
    """The range: the linking samples drawn again (students with replacement, within each sample; the trial's pairs
    within each academy and order), every conversion and the gain and dip refitted, every student placed again."""
    rng = np.random.default_rng(seed)
    sm0 = samples(D)
    totals = []
    for _ in range(reps):
        sm = {}
        for k in ("ref", "quill", "july"):
            v = sm0[k]
            sm[k] = [v[i] for i in rng.integers(0, len(v), size=len(v))]
        groups = {}
        for p in sm0["pairs"]:
            groups.setdefault((p[2]["academy"], p[1]["date"] > p[0]["date"]), []).append(p)
        prs = []
        for key in sorted(groups, key=str):
            v = groups[key]
            prs += [v[i] for i in rng.integers(0, len(v), size=len(v))]
        sm["pairs"] = prs
        Lk = links(D, o, sm)
        pl = place(D, Lk)
        totals.append(sum(1 for p in pl if p["placed"]))
    return np.array(totals)
