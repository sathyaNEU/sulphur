"""task8 architecture 18: the clean truth. Items (pool, strand, context, stem length, difficulty on the Level 2
reference), papers 2022 to 2027, centres, candidates, sittings and every scored response, drawn from one seed
with a separate stream per component so that a change in one leaves the others where they were."""
import datetime as dt

import numpy as np

import params as P

STRANDS_L1 = ("N", "MM", "D", "SS")
STRAND_NAME = {"N": "Number", "MM": "Money and measures", "D": "Data", "SS": "Shape and space",
               "PR": "Patterns and relationships"}


def sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def streams(seed):
    ss = np.random.SeedSequence(seed)
    names = ("items", "papers", "centres", "people", "theta", "resp", "dates", "mess", "ids", "survey", "audit")
    return {n: np.random.default_rng(s) for n, s in zip(names, ss.spawn(len(names)))}


def _codes(rng, n, prefix, start):
    """Bank codes advance by uneven steps, the way a bank numbers items as writers submit them."""
    steps = rng.integers(1, 9, size=n)
    nums = start + np.cumsum(steps)
    return ["%s-%04d" % (prefix, k) for k in nums]


def draw_items(rng):
    """Two pools on one reference scale (what a Level 2 candidate finds). Returns a dict of arrays."""
    n1, n2 = 236, 204
    strand1 = rng.choice(STRANDS_L1, size=n1, p=[0.30, 0.30, 0.20, 0.20])
    strand2 = rng.choice(STRANDS_L1 + ("PR",), size=n2, p=[0.25, 0.24, 0.17, 0.16, 0.18])
    strand = np.concatenate([strand1, strand2])
    p_every = {"N": 0.18, "MM": 0.90, "D": 0.58, "SS": 0.38, "PR": 0.08}
    everyday = np.array([rng.random() < p_every[s] for s in strand])
    p_long = {"N": 0.10, "MM": 0.34, "D": 0.40, "SS": 0.20, "PR": 0.62}
    long_ = np.array([rng.random() < p_long[s] for s in strand])
    words = np.where(long_, rng.integers(82, 151, size=n1 + n2), rng.integers(14, 49, size=n1 + n2))
    b = np.concatenate([np.clip(rng.normal(-1.20, 0.82, n1), -3.3, 0.9), np.clip(rng.normal(0.55, 0.74, n2), -1.2, 2.3)])
    pool = np.array(["L1"] * n1 + ["L2"] * n2)
    resid = rng.normal(0.0, P.RESID_DIF, n1 + n2)
    codes = _codes(rng, n1, "N1", 1000) + _codes(rng, n2, "N2", 2000)
    it = dict(code=np.array(codes), pool=pool, strand=strand, everyday=everyday, words=words.astype(int), b=b,
              resid=resid)
    I2 = np.arange(n1, n1 + n2)

    def take(cond, k, used):
        cand = [i for i in I2 if cond(i) and i not in used]
        rng.shuffle(cand)
        out = cand[:k]
        used.update(out)
        return np.array(out)
    used = set()
    acc = lambda i: -0.75 <= b[i] <= 0.85
    sp = take(lambda i: acc(i) and strand[i] == "MM", 8, used)
    sa = take(lambda i: acc(i) and strand[i] == "N", 12, used)
    lp = take(lambda i: acc(i) and strand[i] in ("MM", "D"), 16, used)
    # patterns and relationships items the Item Review Group may draw on for the 2027 Level 1 paper
    pr = take(lambda i: -0.95 <= b[i] <= 0.75 and strand[i] == "PR", 24, used)
    if len(pr) < 18:
        more = sorted((i for i in I2 if strand[i] == "PR" and i not in used), key=lambda i: abs(b[i] + 0.1))
        pr = np.concatenate([pr, np.array(more[:18 - len(pr)], dtype=int)]).astype(int)
        used.update(pr.tolist())
    everyday[sp] = True
    words[sp] = rng.integers(17, 42, size=len(sp))
    everyday[sa] = False
    words[sa] = rng.integers(15, 44, size=len(sa))
    everyday[lp] = True
    # long everyday items: their reading cost sits about where their everyday advantage does
    words[lp] = np.clip(np.round(100.0 * P.BETA / P.LAMBDA + rng.normal(0, 15, size=len(lp))), 90, 142).astype(int)
    everyday[pr] = False
    words[pr] = rng.integers(98, 141, size=len(pr))
    it["everyday"], it["words"] = everyday, words.astype(int)
    it["sets"] = dict(sp=sp, sa=sa, lp=lp, pr_pool=pr)
    return it


def mix_chance(it, idx, th):
    """Chance that a Level 1 candidate at ability th (reference scale) answers each item, over the regions."""
    shares = np.array([r[3] for r in P.REGIONS])
    shares = shares / shares.sum()
    out = np.zeros(len(idx))
    for reg, sh in zip(P.REGIONS, shares):
        out += sh * sig(th - it["b"][idx] - l1_shift(it, idx, reg[5]))
    return out


def true_standard(it, ref):
    lo, hi = -8.0, 8.0
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if mix_chance(it, ref, m).sum() < P.STANDARD_RAW:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def l1_shift(it, idx, delta_r=0.0):
    """How much harder item idx is for a Level 1 candidate than for a Level 2 candidate (logits)."""
    return (P.LAMBDA * it["words"][idx] / 100.0 - (P.BETA + delta_r) * it["everyday"][idx].astype(float)
            + it["resid"][idx])


def draw_papers(rng, it):
    n1 = int((it["pool"] == "L1").sum())
    I1 = np.arange(n1)
    I2 = np.arange(n1, len(it["b"]))
    s = it["sets"]
    bridging = set(np.concatenate([s["sp"], s["sa"], s["lp"], s["pr_pool"]]).tolist())
    b, ev = it["b"], it["everyday"]
    papers = {}
    # the 2022 reference paper: forty Level 1 items, sixteen in everyday contexts
    order = rng.permutation(I1)
    evs = [i for i in order if ev[i] and -2.7 <= b[i] <= 0.2]
    mts = [i for i in order if not ev[i] and -2.7 <= b[i] <= 0.2]
    ref = np.array(evs[:16] + mts[:24])
    used = set(ref.tolist())
    papers["L1-2022"] = ref
    prev = list(ref)
    for k, y in enumerate(P.YEARS[1:]):
        reuse = list(rng.choice(prev, size=10, replace=False))
        fresh_ev = [i for i in order if ev[i] and i not in used][:11]
        fresh_mt = [i for i in order if not ev[i] and i not in used][:10]
        used.update(fresh_ev + fresh_mt)
        br = list(s["sp"][2 * k:2 * k + 2]) + list(s["sa"][3 * k:3 * k + 3]) + list(s["lp"][4 * k:4 * k + 4])
        papers["L1-%d" % y] = np.array(reuse + fresh_ev + fresh_mt + br)
        prev = list(set(prev) | set(fresh_ev) | set(fresh_mt))
    # the 2027 paper: twenty-eight Level 1 items already sat (eight everyday, twenty mathematical) and the twelve
    # patterns and relationships items from the Level 2 pool
    th_std = true_standard(it, ref)
    clear = lambda i: not (0.14 <= mix_chance(it, np.array([i]), th_std)[0] <= 0.27 or
                           0.84 <= mix_chance(it, np.array([i]), th_std)[0] <= 0.95)
    sat0 = [i for i in rng.permutation(sorted(set(np.concatenate([papers["L1-%d" % y] for y in P.YEARS])) - bridging))]
    sat = [i for i in sat0 if clear(i)]
    e27 = [i for i in sat if ev[i] and -2.4 <= b[i] <= 0.1][:8]
    e27 += [i for i in sat + sat0 if ev[i] and i not in e27][:8 - len(e27)]
    m27 = [i for i in sat if not ev[i] and -2.4 <= b[i] <= 0.3][:20]
    m27 += [i for i in sat + sat0 if not ev[i] and i not in m27][:20 - len(m27)]
    pool = [i for i in rng.permutation(s["pr_pool"]) if clear(i)]
    low = [i for i in pool if mix_chance(it, np.array([i]), th_std)[0] < 0.14]
    high = [i for i in pool if mix_chance(it, np.array([i]), th_std)[0] > 0.27]
    k_low = min(len(low), 6)
    pr = np.array(low[:k_low] + high[:12 - k_low], dtype=int)
    if len(pr) < 12:
        rest = [i for i in list(pool) + list(s["pr_pool"]) if i not in set(pr.tolist())]
        rest = list(dict.fromkeys(rest))
        pr = np.concatenate([pr, np.array(rest[:12 - len(pr)], dtype=int)])
    s["pr"] = pr
    bridging |= set(pr.tolist())
    papers["L1-2027"] = np.array(e27 + m27 + list(s["pr"]))
    # Level 2 papers: forty Level 2 items each, ten carried from earlier papers; every bridging item and every
    # patterns item the 2027 paper borrows sits on at least one of them
    o2 = [i for i in rng.permutation(I2) if i not in bridging]
    prev2, pos = [], 0
    br_all = list(s["sp"]) + list(s["sa"]) + list(s["lp"])
    rng.shuffle(br_all)
    for k, y in enumerate(P.YEARS):
        reuse = list(rng.choice(prev2, size=10, replace=False)) if prev2 else []
        br = br_all[k * 7:(k + 1) * 7] + ([br_all[35]] if k == 0 else [])
        prs = list(s["pr"][4 * (k - 2):4 * (k - 2) + 4]) if k >= 2 else []
        n_new = 40 - len(reuse) - len(br) - len(prs)
        fresh = o2[pos:pos + n_new]
        pos += n_new
        papers["L2-%d" % y] = np.array(reuse + fresh + br + prs)
        prev2 = list(set(prev2) | set(fresh))
    for name, arr in papers.items():
        assert len(arr) == 40 and len(set(arr.tolist())) == 40, name
    return papers


REGION_CENTRES = {
    "WPG": ["North End Adult Learning Centre", "Point Douglas Community Learning", "St. Vital Adult Education",
            "Westwood Literacy Program", "Elmwood Learning Hub", "Sargent Avenue Adult Centre (Suite 210)",
            "Downtown Skills Centre", "Transcona Adult Ed."],
    "WST": ["Brandon Adult Learning Centre", "Virden Community Learning", "Souris Valley Adult Ed.",
            "Neepawa Literacy Council", "Killarney Learning Place"],
    "INT": ["Selkirk Adult Learning Centre", "Gimli Community Learning", "Steinbach Adult Education",
            "Beausejour Learning Centre", "Arborg Literacy Program", "Stonewall Adult Ed. (Library annex)"],
    "PKN": ["Dauphin Adult Education", "Swan River Learning Centre", "The Pas Community Learning",
            "Flin Flon Adult Ed.", "Thompson Learning Hub"],
    "SKC": ["Saskatoon Westside Learning Centre", "Riverside Adult Education", "Humboldt Community Learning",
            "North Battleford Adult Learning", "Warman Literacy Program", "Prince Albert Learning Centre"],
    "RGS": ["Regina North Central Learning", "Heritage Adult Education (Regina)", "Moose Jaw Adult Learning",
            "Weyburn Community Learning", "Swift Current Literacy Council", "Estevan Learning Place"],
}


def draw_centres(rng):
    rows = []
    codes = _codes(rng, sum(len(v) for v in REGION_CENTRES.values()), "LC", 100)
    order = rng.permutation(len(codes))
    k = 0
    for reg in P.REGIONS:
        rc = reg[0]
        names = REGION_CENTRES[rc]
        w = rng.dirichlet(np.ones(len(names)) * 2.5)
        for nm, wt in zip(names, w):
            rows.append(dict(code=codes[order[k]], name=nm, region=rc, prov=reg[2], weight=float(wt)))
            k += 1
    return rows


def _date(rng, year):
    a = dt.date(year, *P.SITTING_START)
    z = dt.date(year, *P.SITTING_END)
    span = (z - a).days
    # sittings bunch at the ends of the centres' course blocks (late April to June, October)
    u = rng.random()
    if u < 0.42:
        d = a + dt.timedelta(days=int(rng.integers(75, 140)))
    elif u < 0.70:
        d = a + dt.timedelta(days=int(rng.integers(220, span + 1)))
    else:
        d = a + dt.timedelta(days=int(rng.integers(0, span + 1)))
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return max(a, min(z, d))


def draw_people(R, centres):
    """Every sitting 2022 to 2026: level, year, person, centre sat at, region, true ability. Some Level 1
    candidates sit again the next year, and some go on to Level 2."""
    rng, rt, rd = R["people"], R["theta"], R["dates"]
    by_region = {}
    for c in centres:
        by_region.setdefault(c["region"], []).append(c)
    shares = np.array([r[3] for r in P.REGIONS])
    shares = shares / shares.sum()
    sittings = []
    pid = [int(rng.integers(300000, 310000))]

    def new_pid():
        pid[0] += int(rng.integers(1, 6))
        return pid[0]
    carry_l1, carry_l2 = [], []
    for y in P.YEARS:
        # Level 1
        n = P.L1_SITTINGS[y]
        resit = carry_l1
        carry_l1 = []
        for k in range(n):
            if k < len(resit):
                person, reg, theta0 = resit[k]
                theta = theta0 + rt.normal(0.18, 0.12)
            else:
                person = new_pid()
                reg = P.REGIONS[int(rng.choice(len(P.REGIONS), p=shares))][0]
                off = [r[4] for r in P.REGIONS if r[0] == reg][0]
                theta = rt.normal(P.L1_MU + off, P.L1_SD)
            cs = by_region[reg]
            cw = np.array([c["weight"] for c in cs])
            cen = cs[int(rng.choice(len(cs), p=cw / cw.sum()))]
            sittings.append(dict(level="L1", year=y, person=person, region=reg, centre=cen["code"], theta=float(theta),
                                 date=_date(rd, y)))
        # Level 2
        n = P.L2_SITTINGS[y]
        prog = carry_l2
        carry_l2 = []
        for k in range(n):
            if k < len(prog):
                person, reg, theta0 = prog[k]
                theta = theta0 + rt.normal(0.55, 0.15)
            else:
                person = new_pid()
                reg = P.REGIONS[int(rng.choice(len(P.REGIONS), p=shares))][0]
                theta = rt.normal(P.L2_MU, P.L2_SD)
            cs = by_region[reg]
            cw = np.array([c["weight"] for c in cs])
            cen = cs[int(rng.choice(len(cs), p=cw / cw.sum()))]
            sittings.append(dict(level="L2", year=y, person=person, region=reg, centre=cen["code"], theta=float(theta),
                                 date=_date(rd, y)))
        # who comes back: a tenth of this year's Level 1 sitters below the middle sit Level 1 again, and a seventh of
        # those above go on to Level 2 the next year
        this = [s for s in sittings if s["year"] == y and s["level"] == "L1"]
        for s in this:
            if s["theta"] < P.L1_MU - 0.1 and rng.random() < 0.20:
                carry_l1.append((s["person"], s["region"], s["theta"]))
            elif s["theta"] > P.L1_MU + 0.6 and rng.random() < 0.30:
                carry_l2.append((s["person"], s["region"], s["theta"]))
    return sittings


def respond(R, it, papers, sittings):
    """Scored responses of every sitting: an (n_sittings x n_items) matrix with NaN where not presented."""
    rng = R["resp"]
    n = len(sittings)
    I = len(it["b"])
    X = np.full((n, I), np.nan)
    delta = {r[0]: r[5] for r in P.REGIONS}
    for j, s in enumerate(sittings):
        idx = papers["%s-%d" % (s["level"], s["year"])]
        d = it["b"][idx].copy()
        if s["level"] == "L1":
            d = d + l1_shift(it, idx, delta[s["region"]])
        p = sig(s["theta"] - d)
        X[j, idx] = (rng.random(len(idx)) < p).astype(float)
    return X


def build():
    R = streams(P.SEED)
    it = draw_items(R["items"])
    papers = draw_papers(R["papers"], it)
    centres = draw_centres(R["centres"])
    sittings = draw_people(R, centres)
    X = respond(R, it, papers, sittings)
    return dict(R=R, it=it, papers=papers, centres=centres, sittings=sittings, X=X)
