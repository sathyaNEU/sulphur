"""task2 architecture 6 golden, computed from the cut pack.

1. Each audited dictation's log word error read as its clinician's own level, plus the release in force, plus the
   hospital it was dictated at: the release steps measured within each clinician's stay at one hospital, the hospital
   effects within the clinicians who dictated at two (the moves the register records under a new staff number).
2. The population a university hospital will dictate from once it is compulsory: every clinician in post there on
   31 December 2026 (the register), each at the level the six smaller hospitals' whole staff show for their grade and
   specialty, where everyone has dictated since the go-live, with the university hospital's own effect added.
3. The clinicians who start in 2027 are that population less the ones already dictating, whose own dictations are on
   record: their heavy-correction share is what the whole staff would carry less what the volunteers already carry.
4. Each go-live's ramp read off the six past go-lives (the clinicians compelled at each, month by month from the
   compulsory date, against their own later months, the calendar's dictation pattern taken out).
5. Each 2027 month's dictations and heavy-correction share, hospital by hospital, the release held at 6.0; each
   quarter's share, its lowest ceiling, the call; the fourth quarter's 90th percentile from the mixture of the groups'
   dictation-level error distributions; and the 2023 to 2026 bridge split into the releases and the mix."""
import math
from collections import defaultdict
from statistics import NormalDist

import numpy as np

import world as W

FROZEN = "6.0"
DEC = W.DEC
Q27 = [(2027, q) for q in (1, 2, 3, 4)]
CEILINGS = (10, 12, 14, 16)
SMALL = [c for c in W.CODES if c not in W.TEACHING]
LN = math.log(W.LINE)
PHI = NormalDist().cdf


def months(y, q):
    return [W.mi(y, 3 * (q - 1) + k + 1) for k in range(3)]


def months_label(t):
    y, m = divmod(t, 12)
    return "1 %s %d" % (["January", "February", "March", "April", "May", "June", "July", "August", "September",
                         "October", "November", "December"][m], W.START[0] + y)


# ---------------------------------------------------------------- postings
def postings(P):
    """each staff number on the register: site, grade, specialty, person, appointment and leaving month, dictation"""
    out = {}
    for s in sorted(P.reg):
        d = P.reg[s]
        vol = dict(P.vol.get(s, {}))
        out[s] = dict(site=d["site"], grade=d["grade"], spec=d["specialty"], person=P.person.get(s, s),
                      start=d["start"], end=d["end"], first=min(vol) if vol else None, vol=vol, in_post=s in P.in_post)
    return out


def season_index(post):
    """dictation volume by calendar month against each steady clinician's own mean, 2022 to 2026"""
    acc = defaultdict(list)
    for s, d in post.items():
        if d["first"] is None:
            continue
        ts = [t for t in d["vol"] if t >= d["first"] + 3]
        full = [y for y in range(2022, 2027) if all(W.mi(y, m) in d["vol"] for m in range(1, 13))]
        for y in full:
            vals = [d["vol"][W.mi(y, m)] for m in range(1, 13)]
            mean = float(np.mean(vals))
            if mean > 0:
                for m in range(12):
                    acc[m].append(vals[m] / mean)
        _ = ts
    idx = np.array([float(np.mean(acc[m])) for m in range(12)])
    return idx / idx.mean()


# ---------------------------------------------------------------- 1. the error model
def fit(P, use=None, iters=60):
    """log word error = clinician at hospital (one effect per staff number) + release; then the hospital effects from
    the clinicians who dictated at two hospitals; releases relative to 6.0, hospitals relative to the six smaller ones"""
    rows = [(a["staff"], a["release"], math.log(a["wer"]), a["person"], a["site"]) for a in P.audits
            if a["e"] > 0 and (use is None or use(a))]
    staffs = sorted({r[0] for r in rows})
    rels = sorted({r[1] for r in rows})
    si = {s: k for k, s in enumerate(staffs)}
    ri = {r: k for k, r in enumerate(rels)}
    ist = np.array([si[r[0]] for r in rows])
    irl = np.array([ri[r[1]] for r in rows])
    y = np.array([r[2] for r in rows])
    ns = np.bincount(ist, minlength=len(staffs)).astype(float)
    nr = np.bincount(irl, minlength=len(rels)).astype(float)
    c = np.zeros(len(staffs))
    b = np.zeros(len(rels))
    for _ in range(iters):
        c = np.bincount(ist, y - b[irl], minlength=len(staffs)) / ns
        b = np.bincount(irl, y - c[ist], minlength=len(rels)) / nr
        ref = b[ri[FROZEN]]
        b -= ref
        c += ref
    resid = y - c[ist] - b[irl]
    sig_e = float(np.sqrt(np.sum(resid ** 2) / (len(y) - len(staffs) - len(rels) + 1)))
    steps = {r: float(b[ri[r]]) for r in rels}
    spell = {s: (float(c[si[s]]), float(ns[si[s]])) for s in staffs}
    # hospital effects: a clinician's effect at one hospital less their effect at another, over every pair of their stays
    site_of = {}
    for r in rows:
        site_of[r[0]] = r[4]
    person_of = {r[0]: r[3] for r in rows}
    byp = defaultdict(list)
    for s in staffs:
        byp[person_of[s]].append(s)
    codes = list(W.CODES)
    ci = {h: k for k, h in enumerate(codes)}
    A, rhs, wts = [], [], []
    for p, ss in sorted(byp.items()):
        ss = [s for s in ss if spell[s][1] >= 3]
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                hi, hj = site_of[ss[i]], site_of[ss[j]]
                if hi == hj:
                    continue
                row = np.zeros(len(codes))
                row[ci[hj]] += 1.0
                row[ci[hi]] -= 1.0
                A.append(row)
                rhs.append(spell[ss[j]][0] - spell[ss[i]][0])
                wts.append(1.0 / (1.0 / spell[ss[i]][1] + 1.0 / spell[ss[j]][1]))
    if not A:
        # no clinician on record at two hospitals: the hospitals' own effects cannot be told from who dictates there
        site = {h: 0.0 for h in codes}
        lev = defaultdict(lambda: [0.0, 0.0])
        for s in staffs:
            e, n = spell[s]
            lev[person_of[s]][0] += e * n
            lev[person_of[s]][1] += n
        level = {p: (v_[0] / v_[1], v_[1]) for p, v_ in lev.items()}
        return dict(steps=steps, site=site, sig_e=sig_e, level=level, spell=spell, movers=0, pairs=0,
                    into={h: 0 for h in codes})
    A, rhs, wts = np.array(A), np.array(rhs), np.array(wts)
    # the six smaller hospitals' effects average zero
    con = np.array([1.0 if h in SMALL else 0.0 for h in codes]) / len(SMALL)
    Aw = A * np.sqrt(wts)[:, None]
    rw = rhs * np.sqrt(wts)
    M = np.vstack([Aw, con * 1e3])
    v = np.concatenate([rw, [0.0]])
    g, *_ = np.linalg.lstsq(M, v, rcond=None)
    site = {h: float(g[ci[h]]) for h in codes}
    movers = sum(1 for p, ss in byp.items() if len({site_of[s] for s in ss if spell[s][1] >= 3}) >= 2)
    into = {h: sum(1 for k in range(len(rhs)) if A[k][ci[h]] != 0) for h in codes}
    # each clinician's own level, every stay's effect less its hospital's
    lev = defaultdict(lambda: [0.0, 0.0])
    for s in staffs:
        e, n = spell[s]
        lev[person_of[s]][0] += (e - site[site_of[s]]) * n
        lev[person_of[s]][1] += n
    level = {p: (v_[0] / v_[1], v_[1]) for p, v_ in lev.items()}
    return dict(steps=steps, site=site, sig_e=sig_e, level=level, spell=spell, movers=movers, pairs=len(rhs), into=into)


# ---------------------------------------------------------------- 2. the population model
def population(P, post, F, cells="grade+specialty", pop_set="december"):
    """the level of an unselected clinician of each grade and specialty: the six smaller hospitals' whole staff in
    December 2026, all dictating since their go-lives; returns the cell means and the spread between clinicians"""
    rows = []
    seen = set()
    for s, d in post.items():
        if d["site"] not in SMALL or d["first"] is None or d["person"] not in F["level"] or d["person"] in seen:
            continue
        if pop_set == "december" and not d["in_post"]:
            continue
        if pop_set == "post go-live" and not (d["end"] is None or d["end"] > P.comp[d["site"]] + 1):
            continue
        seen.add(d["person"])
        lv, n = F["level"][d["person"]]
        rows.append((d["grade"], d["spec"], lv, n))
    grades = sorted({r[0] for r in rows})
    specs = sorted({r[1] for r in rows})
    X = []
    for g, sp, _, _ in rows:
        x = [1.0] + [1.0 if g == gg else 0.0 for gg in grades[1:]]
        if cells == "grade+specialty":
            x += [1.0 if sp == ss else 0.0 for ss in specs[1:]]
        X.append(x)
    X = np.array(X)
    yv = np.array([r[2] for r in rows])
    beta, *_ = np.linalg.lstsq(X, yv, rcond=None)
    res = yv - X @ beta
    noise = float(np.mean([F["sig_e"] ** 2 / r[3] for r in rows]))
    sig_u = math.sqrt(max(1e-6, float(np.var(res, ddof=X.shape[1])) - noise))

    def mean_of(g, sp):
        x = [1.0] + [1.0 if g == gg else 0.0 for gg in grades[1:]]
        if cells == "grade+specialty":
            x += [1.0 if sp == ss else 0.0 for ss in specs[1:]]
        return float(np.array(x) @ beta)
    return dict(mean_of=mean_of, sig_u=sig_u, n=len(rows))


def grade_volume(post, season, kind="small"):
    """a clinician's dictations a month once settled, by grade: the smaller hospitals' 2026 dictators, the calendar out"""
    acc = defaultdict(list)
    for s, d in post.items():
        if d["site"] in SMALL and d["first"] is not None and d["first"] <= W.mi(2025, 9):
            v = [d["vol"].get(t, 0) / season[t % 12] for t in range(W.mi(2026, 1), DEC + 1)]
            if d["end"] is None and d["in_post"]:
                acc[d["grade"]].append(float(np.mean(v)))
    return {g: float(np.mean(v)) for g, v in acc.items()}


# ---------------------------------------------------------------- 3. the university hospitals' staff in 2027
def empirical_grade_rates(P, post, F, h):
    """a non-parametric route: the smaller hospitals' release 6.0 audits, each moved from its own hospital's effect to
    the university hospital's, the heavy share by grade"""
    acc = defaultdict(list)
    for a in P.audits:
        d = post.get(a["staff"])
        if d is None or a["site"] not in SMALL or a["release"] != FROZEN:
            continue
        acc[d["grade"]].append(math.log(max(a["wer"], 1e-4)) - F["site"][a["site"]] + F["site"][h] > LN)
    return {g_: float(np.mean(v_)) for g_, v_ in acc.items()}


def univ(P, post, F, POP, gvol, season, h, recent=3, rates_how="6.0 audits", pop_how="model"):
    """the whole staff in post at a university hospital on 31 December 2026, the clinicians already dictating there and
    the ones who start once it is compulsory"""
    S = math.sqrt(POP["sig_u"] ** 2 + F["sig_e"] ** 2)
    g = F["site"][h]
    staff = [s for s, d in post.items() if d["site"] == h and d["in_post"]]
    dictating = [s for s in staff if any(post[s]["vol"].get(t, 0) > 0 for t in range(DEC - 2, DEC + 1))]
    dset = set(dictating)
    entrants = [s for s in staff if s not in dset]
    mean = {s: POP["mean_of"](post[s]["grade"], post[s]["spec"]) for s in staff}
    v = {s: gvol[post[s]["grade"]] for s in staff}
    if pop_how == "empirical":
        er = empirical_grade_rates(P, post, F, h)
        pop_heavy = sum(v[s] * er[post[s]["grade"]] for s in staff)
    else:
        pop_heavy = sum(v[s] * (1 - PHI((LN - mean[s] - g) / S)) for s in staff)
    pop_vol = sum(v[s] for s in staff)
    # the dictators' own heavy-correction share under 6.0, from their audits at the hospital
    if rates_how == "6.0 audits":
        au = [a for a in P.audits if a["site"] == h and a["staff"] in dset and a["release"] == FROZEN]
        h_dict = float(np.mean([a["wer"] > W.LINE for a in au]))
    else:
        au = [a for a in P.audits if a["site"] == h and a["staff"] in dset]
        h_dict = float(np.mean([a["wer"] * math.exp(-F["steps"][a["release"]]) > W.LINE for a in au]))
    d_vol_grade = sum(v[s] for s in dictating)
    e_vol = sum(v[s] for s in entrants)
    h_ent = (pop_heavy - d_vol_grade * h_dict) / e_vol
    # the dictators' own volume, settled, the calendar out
    d_vol = sum(np.mean([post[s]["vol"].get(t, 0) / season[t % 12] for t in range(DEC - recent + 1, DEC + 1)])
                for s in dictating)
    wer_dict = np.array([a["wer"] for a in au])
    return dict(staff=staff, dictating=dictating, entrants=entrants, mean=mean, v=v, g=g, S=S, h_pop=pop_heavy / pop_vol,
                h_dict=h_dict, h_ent=h_ent, d_vol=float(d_vol), e_vol=float(e_vol), pop_vol=pop_vol,
                d_vol_grade=d_vol_grade, wer_dict=wer_dict)


# ---------------------------------------------------------------- 4. the go-live ramp
def ramp_curve(P, post, season, k_max=6, sites=None):
    """volume of the clinicians compelled at each past go-live, month by month from the compulsory date, per clinician
    still in post, against their own months 6 to 11, the calendar taken out; the mean over the go-lives"""
    curves = []
    for h in sites or SMALL:
        c = P.comp[h]
        if c < W.mi(2022, 2) or c + 11 > DEC:
            continue
        cohort = [s for s, d in post.items() if d["site"] == h and d["start"] < c and (d["end"] is None or d["end"] > c)
                  and (d["first"] is None or d["first"] >= c)]
        per = []
        for k in range(12):
            t = c + k
            live = [s for s in cohort if post[s]["end"] is None or post[s]["end"] > t + 1]
            per.append(sum(post[s]["vol"].get(t, 0) for s in live) / max(1, len(live)) / season[t % 12])
        steady = float(np.mean(per[6:12]))
        curves.append([x / steady for x in per[:k_max]])
    return [float(x) for x in np.mean(np.array(curves), axis=0)]


def leave_rate(post):
    """leavers a month among clinicians in post, 2022 to 2026, from the register"""
    at_risk = leave = 0.0
    for s, d in post.items():
        a = max(0.0, d["start"])
        b = d["end"] if d["end"] is not None else DEC + 1
        if b > a:
            at_risk += b - a
            if d["end"] is not None:
                leave += 1
    return leave / at_risk


# ---------------------------------------------------------------- 5. 2027 month by month
def project(P, post, F, POP, gvol, season, ramp, lam, U, small_rate, use_ramp=True, start_kind="golden",
            small_vol_months=3):
    out = {}
    small_vol = {}
    for h in SMALL:
        ss = [s for s, d in post.items() if d["site"] == h and any(d["vol"].get(t, 0) > 0 for t in range(DEC - 2, DEC + 1))]
        small_vol[h] = sum(np.mean([post[s]["vol"].get(t, 0) / season[t % 12]
                                    for t in range(DEC - small_vol_months + 1, DEC + 1)]) for s in ss)
    for t in range(W.mi(2027, 1), W.mi(2027, 12) + 1):
        sf = season[t % 12]
        cells = []
        for h in SMALL:
            cells.append((h, "staff", small_vol[h] * sf, small_rate[h]))
        for h in W.TEACHING:
            u = U[h]
            c = P.comp[h]
            cells.append((h, "dictating", u["d_vol"] * sf, u["h_dict"]))
            if t >= c:
                k = t - c
                if start_kind == "full":
                    r = 1.0
                elif start_kind == "own first months":
                    r = 0.5 if k == 0 else (0.8 if k == 1 else 1.0)
                else:
                    r = (ramp[k] if k < len(ramp) else 1.0) if use_ramp else 1.0
                # the staff in post held as on 31 December 2026, a leaver replaced like for like
                cells.append((h, "starters", u["e_vol"] * r * sf, u["h_ent"]))
        out[t] = cells
    return out, small_vol


def quarter_figures(out, sel=None):
    q = {}
    for (y, qq) in Q27:
        num = den = 0.0
        for t in months(y, qq):
            for h, kind, v, r in out[t]:
                if sel is None or h in sel:
                    num += v * r
                    den += v
        q[(y, qq)] = dict(vol=den, share=num / den)
    return q


def mix_cdf(x, groups):
    """the share of a quarter's dictations at or under word error rate x"""
    tot = sum(wt for wt, _ in groups)
    return sum(wt * f(x) for wt, f in groups) / tot


def p90_q4(out, P, U, POP, F, small_au):
    """the 90th percentile of the fourth quarter's dictations' word error rates"""
    wts = defaultdict(float)
    for t in months(2027, 4):
        for h, kind, v, r in out[t]:
            wts[(h, kind)] += v
    groups = []
    for (h, kind), wt in sorted(wts.items()):
        if h in SMALL:
            arr = np.sort(small_au[h])
            groups.append((wt, lambda x, arr=arr: np.searchsorted(arr, x, side="right") / len(arr)))
        else:
            u = U[h]
            arr = np.sort(u["wer_dict"])
            fd = (lambda x, arr=arr: np.searchsorted(arr, x, side="right") / len(arr))

            def fpop(x, u=u):
                lx = math.log(x)
                return sum(u["v"][s] * PHI((lx - u["mean"][s] - u["g"]) / u["S"]) for s in u["staff"]) / u["pop_vol"]
            if kind == "dictating":
                groups.append((wt, fd))
            elif kind == "starters" and "ent_arr" in u:
                groups.append((wt, lambda x, arr=u["ent_arr"]: np.searchsorted(arr, x, side="right") / len(arr)))
            elif kind == "starters":
                groups.append((wt, lambda x, u=u, fd=fd, fpop=fpop:
                               (u["pop_vol"] * fpop(x) - u["d_vol_grade"] * fd(x)) / u["e_vol"]))
            else:
                groups.append((wt, fpop))
    lo, hi = 0.01, 0.6
    for _ in range(50):
        mid = (lo + hi) / 2
        if mix_cdf(mid, groups) < 0.9:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- the bridge
def bridge(P, F, step=None):
    """the audited share from the second quarter of 2023 (release 4.0) to the fourth of 2026 (6.0), split into the
    releases (the 4.0 to 6.0 step measured within clinicians) and the mix of dictations, the two orders averaged"""
    d = (F["steps"]["6.0"] - F["steps"]["4.0"]) if step is None else step
    a = [x["wer"] for x in P.audits if W.mi(2023, 4) <= x["t"] <= W.mi(2023, 6)]
    b = [x["wer"] for x in P.audits if W.mi(2026, 10) <= x["t"] <= DEC]
    s = lambda arr, f: float(np.mean([w_ * f > W.LINE for w_ in arr]))
    s00, s11 = s(a, 1.0), s(b, 1.0)
    s01, s10 = s(a, math.exp(d)), s(b, math.exp(-d))
    rel = 0.5 * ((s01 - s00) + (s11 - s10))
    return dict(start=s00, end=s11, change=s11 - s00, releases=rel, mix=(s11 - s00) - rel,
                releases_orders=(s01 - s00, s11 - s10), step=d)


# ---------------------------------------------------------------- the whole golden
def band(x):
    return next((c for c in CEILINGS if 100 * x <= c), None)


def ceiling(q):
    m = 100 * max(f["share"] for f in q.values())
    return next((c for c in CEILINGS if m <= c), None)


def first_past(q):
    out = {}
    for c in CEILINGS:
        k = next((i + 1 for i, kk in enumerate(Q27) if 100 * q[kk]["share"] > c), None)
        if k is None:
            break
        out[c] = k
    return out


def golden(P, **kw):
    post = postings(P)
    season = season_index(post) if kw.get("season", True) else np.ones(12)
    F = fit(P, use=kw.get("fit_use"))
    if kw.get("site_off"):
        F = dict(F, site={h: (0.0 if h in W.TEACHING else v) for h, v in F["site"].items()})
    POP = population(P, post, F, cells=kw.get("cells", "grade+specialty"), pop_set=kw.get("pop_set", "december"))
    gvol = grade_volume(post, season)
    U = {h: univ(P, post, F, POP, gvol, season, h, recent=kw.get("recent", 3), rates_how=kw.get("rates_how", "6.0 audits"),
                 pop_how=kw.get("pop_how", "model")) for h in W.TEACHING}
    if kw.get("starter_from"):
        # a hurried route: the 2027 starters given the rate of one kind of the smaller hospitals' compulsory starters
        tk = typed(P, post)
        arr = defaultdict(list)
        for a in P.audits:
            if a["release"] == FROZEN and a["staff"] in tk:
                arr[tk[a["staff"]]].append(a["wer"])
        pick = {"compelled": arr["compelled"], "hired": arr["hired"], "pooled": arr["compelled"] + arr["hired"]}
        ent = np.array(pick[kw["starter_from"]])
        for h in W.TEACHING:
            U[h] = dict(U[h], h_ent=float(np.mean(ent > W.LINE)), ent_arr=np.sort(ent))
    ramp = ramp_curve(P, post, season, sites=kw.get("ramp_sites"))
    lam = leave_rate(post)
    small_au, small_rate = {}, {}
    for h in SMALL:
        au = [a["wer"] for a in P.audits if a["site"] == h and a["release"] == FROZEN]
        small_au[h] = np.array(au)
        small_rate[h] = float(np.mean(np.array(au) > W.LINE))
    out, small_vol = project(P, post, F, POP, gvol, season, ramp, lam, U, small_rate,
                             use_ramp=kw.get("use_ramp", True), start_kind=kw.get("start_kind", "golden"),
                             small_vol_months=kw.get("recent", 3))
    q = quarter_figures(out)
    hq = {h: quarter_figures(out, sel={h})[(2027, 4)] for h in W.TEACHING}
    p90 = p90_q4(out, P, U, POP, F, small_au)
    B = bridge(P, F) if "4.0" in F["steps"] else None
    return dict(post=post, season=season, F=F, POP=POP, gvol=gvol, U=U, ramp=ramp, lam=lam, small_rate=small_rate,
                small_vol=small_vol, out=out, q=q, hq=hq, p90=p90, bridge=B, ceiling=ceiling(q),
                bands=[band(q[k]["share"]) for k in Q27], first_past=first_past(q))


# ---------------------------------------------------------------- the hurried routes, each run end to end on the pack
def typed(P, post):
    """the smaller hospitals' compulsory starters typed the way the record allows: in post before the compulsory date
    and first dictating on or after it (compelled), or appointed on or after it (hired)"""
    kinds = {}
    for s, d in post.items():
        if d["site"] not in SMALL or d["first"] is None:
            continue
        c = P.comp[d["site"]]
        if d["first"] < c:
            kinds[s] = "chose"
        elif d["start"] < c:
            kinds[s] = "compelled"
        else:
            kinds[s] = "hired"
    return kinds


def small_kind_rates(P, post):
    k = typed(P, post)
    acc = defaultdict(list)
    for a in P.audits:
        if a["release"] == FROZEN and a["staff"] in k:
            acc[k[a["staff"]]].append(a["wer"] > W.LINE)
    return {kk: float(np.mean(v)) for kk, v in acc.items()}


def route(P, G, name):
    """each 2027 quarter's share under a hurried route"""
    if name == "steady":
        s = defaultdict(list)
        for a in P.audits:
            if W.mi(2026, 1) <= a["t"] <= DEC:
                s[0].append(a["wer"] > W.LINE)
        return [float(np.mean(s[0]))] * 4
    if name == "history":
        qs = defaultdict(list)
        for a in P.audits:
            qs[(a["t"] // 12, a["t"] % 12 // 3)].append(a["wer"] > W.LINE)
        return [max(float(np.mean(v)) for v in qs.values())] * 4
    if name == "hospitals":
        own = defaultdict(list)
        for a in P.audits:
            if W.mi(2026, 10) <= a["t"] <= DEC:
                own[a["site"]].append(a["wer"] > W.LINE)
        r = {h: float(np.mean(v)) for h, v in own.items()}
        out = {t: [(h, k, v, r[h]) for h, k, v, _ in cells] for t, cells in G["out"].items()}
        return [quarter_figures(out)[k]["share"] for k in Q27]
    kr = small_kind_rates(P, G["post"])
    if name in ("compelled", "pooled"):
        if name == "compelled":
            he = kr["compelled"]
        else:
            n = defaultdict(int)
            tk = typed(P, G["post"])
            for a in P.audits:
                if a["release"] == FROZEN and a["staff"] in tk:
                    n[tk[a["staff"]]] += 1
            he = (kr["compelled"] * n["compelled"] + kr["hired"] * n["hired"]) / (n["compelled"] + n["hired"])
        out = {t: [(h, k, v, he if k == "starters" else (kr["hired"] if k == "new hires" else r)) for h, k, v, r in cells]
               for t, cells in G["out"].items()}
        return [quarter_figures(out)[k]["share"] for k in Q27]
    raise KeyError(name)


# ---------------------------------------------------------------- the bridge's hurried routes
BENCHMARK = {"5.0": 0.078, "5.2": 0.039, "6.0": 0.032}      # the release notes' LCB-2 reductions, 4.0 to 6.0


def bridge_routes(P, G):
    B = G["bridge"]
    out = {"every point of the change to the releases": dict(releases=B["change"], mix=0.0)}
    bb = bridge(P, G["F"], step=sum(math.log(1 - x) for x in BENCHMARK.values()))
    out["the release notes' benchmark cuts"] = dict(releases=bb["releases"], mix=bb["mix"])
    # a shift-share by hospital: the hospitals' shares of the audits against each hospital's own audited share
    def by_h(lo, hi):
        acc = defaultdict(list)
        for a in P.audits:
            if lo <= a["t"] <= hi:
                acc[a["site"]].append(a["wer"] > W.LINE)
        n = sum(len(v) for v in acc.values())
        return {h: (len(v) / n, float(np.mean(v))) for h, v in acc.items()}
    a0, a1 = by_h(W.mi(2023, 4), W.mi(2023, 6)), by_h(W.mi(2026, 10), DEC)
    hs = sorted(set(a0) | set(a1))
    w0 = {h: a0.get(h, (0.0, 0.0))[0] for h in hs}
    w1 = {h: a1.get(h, (0.0, 0.0))[0] for h in hs}
    s0 = {h: a0.get(h, (0.0, a1[h][1]))[1] for h in hs}
    s1 = {h: a1.get(h, (0.0, a0[h][1]))[1] for h in hs}
    mix = 0.5 * (sum((w1[h] - w0[h]) * s0[h] for h in hs) + sum((w1[h] - w0[h]) * s1[h] for h in hs))
    out["a shift-share by hospital"] = dict(releases=B["change"] - mix, mix=mix)
    # the jumps in the monthly audited share at each release from 4.0 to 6.0
    mon = defaultdict(list)
    for a in P.audits:
        mon[a["t"]].append(a["wer"] > W.LINE)
    ms = {t: float(np.mean(v)) for t, v in mon.items()}
    jumps = 0.0
    for r, s, _ in W.RELEASES[1:]:
        jumps += np.mean([ms[t] for t in range(s, s + 3)]) - np.mean([ms[t] for t in range(s - 3, s)])
    out["the jumps at each release month"] = dict(releases=float(jumps), mix=B["change"] - float(jumps))
    return out


def p90_levels(P, G):
    """the 90th percentile read off clinicians' typical levels, as if each clinician's dictations sat at their level"""
    U, F, POP = G["U"], G["F"], G["POP"]
    wts = defaultdict(float)
    for t in months(2027, 4):
        for h, kind, v, r in G["out"][t]:
            wts[(h, kind)] += v
    lv = defaultdict(list)
    for a in P.audits:
        if a["release"] == FROZEN and a["person"] in F["level"]:
            lv[a["site"]].append(math.exp(F["level"][a["person"]][0] + F["site"][a["site"]]))
    groups = []
    for (h, kind), wt in sorted(wts.items()):
        if h in SMALL or kind == "dictating":
            arr = np.sort(lv[h]) if h in SMALL else np.sort([math.exp(F["level"][P.person.get(s, s)][0] + U[h]["g"])
                                                               for s in U[h]["dictating"] if P.person.get(s, s) in F["level"]])
            groups.append((wt, lambda x, arr=arr: np.searchsorted(arr, x, side="right") / len(arr)))
        else:
            u = U[h]
            groups.append((wt, lambda x, u=u: sum(u["v"][s] * PHI((math.log(x) - u["mean"][s] - u["g"]) / POP["sig_u"])
                                                  for s in u["entrants"]) / u["e_vol"]))
    lo, hi = 0.01, 0.6
    for _ in range(50):
        mid = (lo + hi) / 2
        if mix_cdf(mid, groups) < 0.9:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
