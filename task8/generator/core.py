#!/usr/bin/env python3
"""task8 architecture 20, the core: six boards' banked portfolio marks against the standard of the board taking them over.

Carrow Awards takes over six regional examining boards from the June 2027 awards. Candidates on the three-year
Senior Trades Certificate hold workshop portfolio marks banked with those boards in the 2025 and 2026 series, marked
out of 100 by their own instructors and carried into awards Carrow will make. The merger protocol converts a board's
banked marks to the standard in force at Carrow where they stand 2 marks or more from it. No record holds how far a
board's banked marks stand from that standard. What the boards hold is their moderation: in a centre's rota year a
moderator re-marks a sample of its portfolios and the board confirms the centre's marks or moves them by the
sample's mean difference.

The three stumps (each opens a different board, each leaves several dependent steps once said):
  S1 (what)     a moderator's mark is not a second reading: the moderator works from the centre's marked record and
                the difference a sample records is a fraction of the difference a marker working cold finds. The
                fraction is in no moderation record. It is in the standardisation trial, whose scripts are the year
                before's sampled portfolios marked cold by the board's whole team, joined back to the mark the
                moderator gave the same portfolio live.
  S2 (when)     a centre is sampled once in its rota cycle and banks marks every year. The marks it banks between
                samples are given at another point of the cycle, at a level the moderation record never sees and the
                centre's own mark sheets do, within centre and net of the board's year.
  S3 (against)  each board's moderators are standardised to their own principal. The boards' standards differ and no
                portfolio was marked by two boards. The people who moderate for two boards carry one standard into
                both trials: their cold trial marks against each team's consensus, then each board's agreed marks
                against its consensus, then the network of boards to Carrow.

Run:  python3 task8/generator/core.py            the corelib verdict
      python3 task8/generator/core.py --detail   the world, every route and the fitted inputs
      python3 task8/generator/core.py --forcing  the call under each fitted input moved by its measured spread
"""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 8134))
Y0, Y1 = 2012, 2026
YEARS = list(range(Y0, Y1 + 1))
NY = len(YEARS)
BANKED = (2025, 2026)                # the series whose banked marks carry into Carrow's awards
LINE = 2.0                           # marks from Carrow's standard at which a board's banked marks are converted
REF = "Carrow"
MEMBERS = ("Ardkeel", "Brannock", "Dunmoyle", "Eskerry", "Fennor", "Gortavale")

# w: how far a moderator's mark is drawn to the centre's; k: years in the rota; o: the board's live standard against
# Carrow's (marks); p: the team's cold consensus minus its principal's agreed mark; d: a centre's yearly drift;
# phi: the share of a recorded difference a centre takes back after its report; psi: what wears off each year;
# tol: the board's tolerance on a sample's mean difference; nc centres; nm moderators.
BOARDS = {
    "Ardkeel": dict(w=0.64, k=3, o=-0.5, p=-0.3, d=1.15, phi=0.85, psi=0.20, tol=3.0, nc=210, nm=34),
    "Brannock": dict(w=0.36, k=3, o=-3.6, p=-0.5, d=1.55, phi=0.90, psi=0.12, tol=5.0, nc=260, nm=44),
    "Dunmoyle": dict(w=0.50, k=3, o=1.5, p=-0.3, d=1.45, phi=0.85, psi=0.16, tol=4.0, nc=240, nm=40),
    "Eskerry": dict(w=0.42, k=2, o=-3.6, p=0.6, d=1.90, phi=0.85, psi=0.14, tol=4.0, nc=200, nm=36),
    "Fennor": dict(w=0.30, k=3, o=-4.0, p=0.2, d=2.20, phi=0.90, psi=0.10, tol=6.0, nc=230, nm=38),
    "Gortavale": dict(w=0.38, k=2, o=-6.7, p=-0.3, d=2.10, phi=0.90, psi=0.14, tol=4.0, nc=170, nm=30),
    "Carrow": dict(w=0.30, k=1, o=0.0, p=0.9, d=0.90, phi=0.85, psi=0.15, tol=3.0, nc=180, nm=32),
}
# people who moderate for two boards: (board, board, persons a year)
DUAL = [("Ardkeel", "Carrow", 9), ("Brannock", "Carrow", 7), ("Gortavale", "Carrow", 5), ("Dunmoyle", "Ardkeel", 11),
        ("Eskerry", "Brannock", 8), ("Fennor", "Dunmoyle", 6), ("Eskerry", "Ardkeel", 6),
        ("Fennor", "Gortavale", 7), ("Brannock", "Dunmoyle", 5), ("Gortavale", "Eskerry", 4)]
DUAL_YEARS = 7
SIG_T, SIG_M, SIG_H, SIG_P = 3.5, 2.0, 0.8, 1.2   # marks: instructor's error, moderator's, moderator's own lean, principal's
SIG_W, SIG_PHI = 0.05, 0.08                        # spread of the draw between moderators, of the take-back between centres
NEX, EX_YEARS = 40, 12                             # trial scripts a year, years of trials on file
REFEREE = ("Dunmoyle", 2023)                       # the regulator's review: every centre, marked cold at Carrow's standard
REVIEW_N = 8


def simulate(seed=SEED, boards=BOARDS):
    rng = np.random.default_rng(seed)
    W = {}
    for b, P in boards.items():
        nc, k = P["nc"], P["k"]
        grp = rng.integers(0, k, nc)
        dc = P["d"] * np.exp(rng.normal(-0.06, 0.35, nc))
        phic = np.clip(rng.normal(P["phi"], SIG_PHI, nc), 0.4, 1.0)
        abil = rng.normal(58, 5.5, nc)
        yr_eff = np.cumsum(rng.normal(0.1, 0.35, NY))
        size = np.exp(rng.normal(3.6, 0.7, nc))
        lam = np.zeros((nc, NY))
        G = np.full((nc, NY), np.nan)
        adj = np.zeros((nc, NY))
        samp = np.zeros((nc, NY), bool)
        ncand = np.zeros((nc, NY))
        mbar = np.zeros((nc, NY))
        ns = np.zeros((nc, NY))
        cur = dc / P["psi"] * 0.5
        for burn in range(40):
            s = ((burn - grp) % k) == 0
            cur = (1 - P["psi"]) * cur + dc - np.where(s, phic * (1 - P["w"]) * cur, 0.0)
        for ti, y in enumerate(YEARS):
            lam[:, ti] = cur
            s = ((y - grp) % k) == 0
            samp[:, ti] = s
            n = np.maximum(6, rng.poisson(size)).astype(float)
            ncand[:, ti] = n
            nsm = np.where(n <= 15, np.minimum(n, 10), np.where(n <= 100, 15, 20))
            ns[:, ti] = nsm
            h = rng.normal(0, SIG_H, nc)
            wm = np.clip(rng.normal(P["w"], SIG_W, nc), 0.05, 0.9)   # the moderator who drew the centre that year
            g = (1 - wm) * (cur - h + rng.normal(0, 1, nc) * np.sqrt(SIG_T ** 2 + SIG_M ** 2) / np.sqrt(nsm))
            G[s, ti] = g[s]
            adj[:, ti] = np.where(s & (np.abs(g) > P["tol"]), np.round(g), 0.0)
            mbar[:, ti] = abil + yr_eff[ti] + P["o"] + cur + rng.normal(0, 11.0, nc) / np.sqrt(n)
            cur = (1 - P["psi"]) * cur + dc - np.where(s, phic * g, 0.0) + rng.normal(0, 0.45, nc)
        nex = NEX * EX_YEARS
        ti = rng.integers(NY - 1 - EX_YEARS, NY - 1, nex)
        ci = np.array([rng.choice(np.flatnonzero(samp[:, t])) for t in ti])
        x_true = lam[ci, ti] + rng.normal(0, SIG_T, nex)             # centre mark minus the board's live standard
        wx = np.clip(rng.normal(P["w"], SIG_W, nex), 0.05, 0.9)
        y = (1 - wx) * (x_true - rng.normal(0, SIG_H, nex) - rng.normal(0, SIG_M, nex))
        cons_err = rng.normal(0, SIG_M / np.sqrt(P["nm"]), nex)
        x = x_true - P["p"] - cons_err                                 # centre mark minus the team's cold consensus
        gap = P["p"] + cons_err - rng.normal(0, SIG_P, nex)            # consensus minus the principal's agreed mark
        W[b] = dict(P=P, grp=grp, lam=lam, G=G, adj=adj, samp=samp, ncand=ncand, mbar=mbar, ns=ns,
                    ex_x=x, ex_y=y, ex_gap=gap, ex_year=np.array(YEARS)[ti + 1])
    D = []
    for a, b, m in DUAL:
        ca, cb = boards[a]["o"] + boards[a]["p"], boards[b]["o"] + boards[b]["p"]
        n = m * DUAL_YEARS
        J = rng.normal(0.5 * (ca + cb), 0.9, n)                       # each person's own standard that season
        D.append(dict(a=a, b=b, ra=J - ca + rng.normal(0, SIG_M / np.sqrt(NEX), n),
                      rb=J - cb + rng.normal(0, SIG_M / np.sqrt(NEX), n)))
    rb, ry = REFEREE
    ti = YEARS.index(ry)
    w = W[rb]
    rev = w["P"]["o"] + w["lam"][:, ti] + rng.normal(0, np.sqrt(SIG_T ** 2 + SIG_M ** 2) / np.sqrt(REVIEW_N),
                                                   w["lam"].shape[0])
    return dict(B=W, D=D, review=rev, boards=boards, cache={})


# ---------------------------------------------------------------- the world's own values
def truth_year(world, year):
    ti = YEARS.index(year)
    return {b: w["P"]["o"] + float(np.sum(w["ncand"][:, ti] * (w["lam"][:, ti] - w["adj"][:, ti])) /
                                   w["ncand"][:, ti].sum()) for b, w in world["B"].items()}


def weights(world, b):
    return np.array([world["B"][b]["ncand"][:, YEARS.index(y)].sum() for y in BANKED])


def pooled(world, by_year):
    """{board: the banked marks of both series together} from {year: {board: figure}}."""
    out = {}
    for b in world["B"]:
        wt = weights(world, b)
        out[b] = float(np.sum(wt * np.array([by_year[y][b] for y in BANKED])) / wt.sum())
    return out


def national(world, fig):
    wt = np.array([weights(world, b).sum() for b in MEMBERS])
    return float(np.sum(wt * np.array([fig[b] for b in MEMBERS])) / wt.sum())


# ---------------------------------------------------------------- the estimators
def slope(x, y, how="ols", nm=36):
    if how == "origin":
        return float(np.sum(x * y) / np.sum(x * x))
    xm, ym = x - x.mean(), y - y.mean()
    sxx = np.mean(xm * xm)
    if how == "deming":
        sxx -= SIG_M ** 2 / nm       # the consensus' own error; the pack's trial marks give it as their spread over nm
    return float(np.mean(xm * ym) / sxx)


def pulls(world, o):
    """The share of a cold difference the moderators record, board by board, from the trial scripts."""
    key = ("pull", o.get("pull", True), o.get("pull_how", "ols"), bool(o.get("pull_recent")))
    if key not in world["cache"]:
        out = {}
        for b, w in world["B"].items():
            if not o.get("pull", True):
                out[b] = 1.0
                continue
            x, y, yr = w["ex_x"], w["ex_y"], w["ex_year"]
            if o.get("pull_recent"):
                keep = yr >= Y1 - 5
                x, y, yr = x[keep], y[keep], yr[keep]
            if o.get("pull_how") == "years":
                out[b] = float(np.mean([slope(x[yr == v], y[yr == v]) for v in np.unique(yr)]))
            else:
                out[b] = slope(x, y, o.get("pull_how", "ols"), w["P"]["nm"])
        world["cache"][key] = out
    sc = o.get("pull_scale", {})
    return {b: v * float(sc.get(b, 1.0)) for b, v in world["cache"][key].items()}


def phase_effects(world, b, o):
    """The level of a centre's own marks by years since its last sample, within centre, net of the board's year."""
    w = world["B"][b]
    k = w["P"]["k"]
    if k == 1 or not o.get("phase", True):
        return np.zeros(max(k, 1))
    key = ("phase", b, int(o.get("phase_years", 9)), bool(o.get("phase_weight")))
    if key not in world["cache"]:
        t1 = NY
        t0 = max(0, t1 - key[2])
        yrs = np.array(YEARS[t0:t1])
        nc, nt = w["mbar"].shape[0], len(yrs)
        ph = (yrs[None, :] - w["grp"][:, None]) % k
        m = w["mbar"][:, t0:t1]
        wt = w["ncand"][:, t0:t1] if o.get("phase_weight") else np.ones_like(m)
        X = np.zeros((nc * nt, nc + nt - 1 + k - 1))
        r = np.arange(nc * nt)
        cc, jj = np.repeat(np.arange(nc), nt), np.tile(np.arange(nt), nc)
        X[r, cc] = 1
        nz = jj > 0
        X[r[nz], nc + jj[nz] - 1] = 1
        pf = ph.reshape(-1)
        nz = pf > 0
        X[r[nz], nc + nt - 1 + pf[nz] - 1] = 1
        sw = np.sqrt(wt.reshape(-1))
        beta = np.linalg.lstsq(X * sw[:, None], m.reshape(-1) * sw, rcond=None)[0]
        world["cache"][key] = (np.concatenate([[0.0], beta[nc + nt - 1:]]),
                               dict(zip(yrs.tolist(), np.concatenate([[0.0], beta[nc:nc + nt - 1]]).tolist())))
    th = world["cache"][key][0]
    return th + np.concatenate([[0.0], np.full(k - 1, float(o.get("phase_shift", {}).get(b, 0.0)))])


def year_effects(world, b, o):
    """The board's year effects from the same fit (the first year of the window is zero)."""
    phase_effects(world, b, o)
    return world["cache"][("phase", b, int(o.get("phase_years", 9)), bool(o.get("phase_weight")))][1]


def offsets(world, o):
    """Each board's live standard against Carrow's: the two-board moderators' cold trial marks link the teams'
    consensus, and each board's agreed marks place its live standard against its consensus."""
    names = list(world["B"])
    if not o.get("link", True):
        return {b: 0.0 for b in names}
    key = ("off", bool(o.get("link_tree")), bool(o.get("link_trim")), bool(o.get("link_median")),
           bool(o.get("link_unweighted")), bool(o.get("agreed_median")))
    if key not in world["cache"]:
        idx = {b: i for i, b in enumerate(names)}
        rows, rhs, wts = [], [], []
        for i, l in enumerate(world["D"]):
            if o.get("link_tree") and i >= 6:
                continue
            d = l["ra"] - l["rb"]                                  # consensus of b minus consensus of a
            if o.get("link_trim"):
                lo, hi = np.percentile(d, [10, 90])
                d = d[(d >= lo) & (d <= hi)]
            est = float(np.median(d)) if o.get("link_median") else float(np.mean(d))
            row = np.zeros(len(names))
            row[idx[l["b"]]], row[idx[l["a"]]] = 1, -1
            rows.append(row)
            rhs.append(est)
            wts.append(1.0 if o.get("link_unweighted") else np.sqrt(len(d)))
        A, y, wv = np.array(rows), np.array(rhs), np.array(wts)
        fix = np.zeros(len(names))
        fix[idx[REF]] = 1
        sol = np.linalg.lstsq(np.vstack([A * wv[:, None], fix * 1e3]), np.concatenate([y * wv, [0.0]]), rcond=None)[0]
        stat = np.median if o.get("agreed_median") else np.mean
        p = {b: float(stat(world["B"][b]["ex_gap"])) for b in names}
        world["cache"][key] = {b: float(sol[idx[b]]) - (p[b] - p[REF]) for b in names}
    sh = o.get("off_shift", {})
    return {b: v + float(sh.get(b, 0.0)) for b, v in world["cache"][key].items()}


def estimate(world, o=None, years=BANKED, subset=None):
    """{year: {board: marks above Carrow's standard}} and the fitted inputs. subset 'unsampled' keeps the centres
    not sampled in the year (the referee's cut)."""
    o = dict(o or {})
    pl = pulls(world, o)
    off = offsets(world, o)
    out = {y: {} for y in years}
    parts = {}
    for b, w in world["B"].items():
        k = w["P"]["k"]
        th = phase_effects(world, b, o)
        lam_hat = w["G"] / pl[b]
        parts[b] = dict(pull=pl[b], theta=th, off=off[b])
        for y in years:
            ti = YEARS.index(y)
            n = w["ncand"][:, ti].copy()
            s = w["samp"][:, ti]
            res = np.where(s, np.nan_to_num(lam_hat[:, ti]) - w["adj"][:, ti], 0.0)
            for back in range(1, k):
                m = w["samp"][:, ti - back] & ~s
                base = lam_hat[:, ti - back]
                if o.get("carry_two"):
                    base = 0.5 * (base + lam_hat[:, ti - back - k])
                step = th[back]
                if o.get("phase", True) and (o.get("cycle_own") or o.get("cycle_half")):
                    ye = year_effects(world, b, o)       # the centre's own change in mean mark, net of the year
                    own = (w["mbar"][:, ti] - ye[y]) - (w["mbar"][:, ti - back] - ye[YEARS[ti - back]])
                    own = own + float(o.get("phase_shift", {}).get(b, 0.0))
                    step = own if o.get("cycle_own") else 0.5 * (own + th[back])
                res = np.where(m, np.nan_to_num(base) + step, res)
            if subset == "unsampled":
                n = np.where(s, 0.0, n)
            out[y][b] = off[b] + float(np.sum(n * res) / n.sum()) if n.sum() > 0 else float("nan")
    return out, parts


def direct(world, years=BANKED):
    """The moderation record read raw: the mean recorded difference of the year's sampled portfolios."""
    out = {y: {} for y in years}
    for b, w in world["B"].items():
        for y in years:
            ti = YEARS.index(y)
            s = w["samp"][:, ti]
            out[y][b] = float(np.sum(w["ns"][s, ti] * w["G"][s, ti]) / np.sum(w["ns"][s, ti]))
    return out


def rigorous(world, years=BANKED, subset=None):
    """The most rigorous standard design the pack affords: moderator severity from each board's own trial (the
    team's cold consensus against the agreed marks, added to the recorded differences), candidate weights, the
    applied adjustments netted, centres not sampled in the year taken from their own last sample shrunk to the
    board's mean. No draw to the centre's mark, no cycle, no link between boards."""
    out = {y: {} for y in years}
    for b, w in world["B"].items():
        k = w["P"]["k"]
        sev = float(np.mean(w["ex_gap"]))
        for y in years:
            ti = YEARS.index(y)
            n = w["ncand"][:, ti].copy()
            s = w["samp"][:, ti]
            allg = w["G"][:, max(0, ti - 5):ti + 1]
            mu = np.nanmean(allg)
            vb = max(np.nanvar(allg) - 1.0, 0.2)
            sh = vb / (vb + 1.0)
            res = np.where(s, np.nan_to_num(w["G"][:, ti]) + sev - w["adj"][:, ti], 0.0)
            for back in range(1, k):
                m = w["samp"][:, ti - back] & ~s
                res = np.where(m, mu + sh * (np.nan_to_num(w["G"][:, ti - back]) - mu) + sev, res)
            if subset == "unsampled":
                n = np.where(s, 0.0, n)
            out[y][b] = float(np.sum(n * res) / n.sum()) if n.sum() > 0 else float("nan")
    return out


# ---------------------------------------------------------------- the honest family and the lattice of shortcuts
DIMS = {
    "pull": [("the draw fitted through the origin", {"pull_how": "origin"}),
             ("the draw on the last five years of trial scripts", {"pull_recent": True}),
             ("the draw with the consensus' own error allowed for", {"pull_how": "deming"}),
             ("the draw fitted year by year and averaged", {"pull_how": "years"})],
    "cycle": [("cycle levels weighted by candidates", {"phase_weight": True}),
              ("cycle levels on the last six years", {"phase_years": 6}),
              ("cycle levels on the last twelve years", {"phase_years": 12}),
              ("each centre's own change in mean mark since its sample, net of the board's year", {"cycle_own": True}),
              ("the cycle level and the centre's own change averaged", {"cycle_half": True})],
    "carry": [("the last two samples averaged before the carry", {"carry_two": True})],
    "link": [("links trimmed at the tenth and ninetieth percentiles", {"link_trim": True}),
             ("links at the median", {"link_median": True}),
             ("links unweighted", {"link_unweighted": True}),
             ("links along the six shortest paths only", {"link_tree": True})],
    "agreed": [("agreed marks at the median", {"agreed_median": True})],
}


def family():
    """Every single convention, and every two that change different choices."""
    out = [(n, dict(o)) for dim in DIMS.values() for n, o in dim]
    for da, db in itertools.combinations(DIMS, 2):
        for (na, oa), (nb, ob) in itertools.product(DIMS[da], DIMS[db]):
            out.append((na + "; " + nb, {**oa, **ob}))
    return out


VARIANTS = family()
LOST = {"S1": {"pull": False}, "S2": {"phase": False}, "S3": {"link": False}}
SIDS = ("S1", "S2", "S3")
PULL_BOARD, CYCLE_BOARD, LINK_BOARD = "Ardkeel", "Fennor", "Gortavale"


def lat_opts(keys):
    o = {}
    for k in keys:
        o.update(LOST[k])
    return o


def lat_keys():
    return ["+".join(ks) for r in (1, 2, 3) for ks in itertools.combinations(SIDS, r)]


def view(world, o=None):
    """Every graded figure on one route: the boards' pooled figures, each series, the six boards together and the
    three inputs the stumps own."""
    by, parts = estimate(world, o)
    pool = pooled(world, by)
    return dict(pool=pool, by=by, nat=national(world, pool), pull=100.0 * parts[PULL_BOARD]["pull"],
                cycle=float(parts[CYCLE_BOARD]["theta"][1]), link=parts[LINK_BOARD]["off"], parts=parts)


def band(x):
    return 1 if x >= LINE else (-1 if x <= -LINE else 0)


def calls(fig):
    return tuple(band(fig[b]) for b in MEMBERS)


def review_raw(world):
    """The regulator's review read raw: the referee board's 2023 marks above Carrow's standard, every centre."""
    rb, ry = REFEREE
    ti = YEARS.index(ry)
    w = world["B"][rb]
    n = w["ncand"][:, ti]
    return float(np.sum(n * (world["review"] - w["adj"][:, ti])) / n.sum())


def referee(world):
    rb, ry = REFEREE
    ti = YEARS.index(ry)
    w = world["B"][rb]
    n = np.where(w["samp"][:, ti], 0.0, w["ncand"][:, ti])
    obs = float(np.sum(n * (world["review"] - w["adj"][:, ti])) / n.sum())
    f = lambda o: estimate(world, o, (ry,), "unsampled")[0][ry][rb]  # noqa: E731
    riv = {"S1 lost": f(LOST["S1"]), "S2 lost": f(LOST["S2"]), "S3 lost": f(LOST["S3"]),
           "rigorous": rigorous(world, (ry,), "unsampled")[ry][rb]}
    return dict(slice="the regulator's 2023 review of %s: portfolios from every centre marked cold at Carrow's "
                      "standard, read on the centres not sampled that year" % rb,
                covers_target=False, truth=obs, golden=f(None), rivals=riv)


def build(world):
    g = view(world)
    fam = [view(world, o) for _, o in VARIANTS]
    lat = {k: view(world, lat_opts(k.split("+"))) for k in lat_keys()}
    dr = pooled(world, direct(world))
    rg_by = rigorous(world)
    rg = pooled(world, rg_by)
    tr_by = {y: truth_year(world, y) for y in BANKED}
    tr = pooled(world, tr_by)
    members = {}
    for b in MEMBERS:
        members[b] = dict(lines=[-LINE, LINE], truth=tr[b], golden=g["pool"][b], family=[f["pool"][b] for f in fam],
                          routes={"direct": dr[b], "rigorous": rg[b]})
    lattice = {k: {b: v["pool"][b] for b in MEMBERS} for k, v in lat.items()}
    figs = [dict(id="C1 share recorded, %s" % PULL_BOARD, block="component", golden=g["pull"],
                 family=[f["pull"] for f in fam], lattice={k: v["pull"] for k, v in lat.items()},
                 routes={"rigorous": 100.0}),
            dict(id="C2 year after a sample, %s" % CYCLE_BOARD, block="component", golden=g["cycle"],
                 family=[f["cycle"] for f in fam], lattice={k: v["cycle"] for k, v in lat.items()},
                 routes={"rigorous": 0.0}),
            dict(id="C3 standard against Carrow, %s" % LINK_BOARD, block="component", golden=g["link"],
                 family=[f["link"] for f in fam], lattice={k: v["link"] for k, v in lat.items()},
                 routes={"rigorous": 0.0})]
    for b in MEMBERS:
        figs.append(dict(id="A1 %s" % b, block="ask", member=b))
    for y in BANKED:
        for b in MEMBERS:
            figs.append(dict(id="A2 %s %d" % (b, y), block="ask", golden=g["by"][y][b],
                             family=[f["by"][y][b] for f in fam], lattice={k: v["by"][y][b] for k, v in lat.items()},
                             routes={"rigorous": rg_by[y][b]}))
    figs.append(dict(id="A3 six boards", block="ask", golden=g["nat"], family=[f["nat"] for f in fam],
                     lattice={k: v["nat"] for k, v in lat.items()}, routes={"rigorous": national(world, rg)}))
    stumps = {
        "S1": dict(axis="what", opens=PULL_BOARD, steps_left=4, precedents=["L22", "L28"],
                   said_out_loud="A moderator works from the centre's marked record, so the difference a sample "
                                 "records is only part of the difference a marker working cold would find."),
        "S2": dict(axis="when", opens=CYCLE_BOARD, steps_left=4, precedents=["N13", "L37"],
                   said_out_loud="A centre is sampled once in its rota cycle, and the marks it banks in the other "
                                 "years are not given at the level its sampled year shows."),
        "S3": dict(axis="against", opens=LINK_BOARD, steps_left=4, precedents=["N27", "L06"],
                   said_out_loud="Each board's moderators are standardised to their own principal, so a board's "
                                 "moderation measures its centres against its own standard and not Carrow's."),
    }
    spec = dict(task="task8 architecture 20", call="lines", members=members, lattice=lattice, referee=referee(world),
                stumps=stumps, figures=figs)
    return spec, dict(g=g, fam=fam, lat=lat, dr=dr, rg=rg, rg_by=rg_by, tr=tr, tr_by=tr_by)


def spreads(x):
    """The furthest any rebuild of the family moves each fitted input, board by board."""
    g, fam = x["g"]["parts"], [f["parts"] for f in x["fam"]]
    sp = {}
    for b in MEMBERS:
        sp[b] = dict(pull=max(abs(f[b]["pull"] / g[b]["pull"] - 1) for f in fam),
                     cycle=max(float(np.max(np.abs(f[b]["theta"] - g[b]["theta"]))) for f in fam),
                     off=max(abs(f[b]["off"] - g[b]["off"]) for f in fam))
    return sp


def forcing_rows(world, x):
    sp = spreads(x)
    gc = calls(x["g"]["pool"])

    def opt(sp_, sc_, so_):
        return {"pull_scale": {b: 1 + sp_ * sp[b]["pull"] for b in MEMBERS},
                "phase_shift": {b: sc_ * sp[b]["cycle"] for b in MEMBERS},
                "off_shift": {b: so_ * sp[b]["off"] for b in MEMBERS}}
    rows = []
    names = [("the share recorded", (1, 0, 0)), ("the cycle levels", (0, 1, 0)), ("the standards", (0, 0, 1))]
    for nm, (a, b_, c) in names:
        for sgn, word in ((1, "up"), (-1, "down")):
            rows.append(("%s one spread %s" % (nm, word), opt(sgn * a, sgn * b_, sgn * c)))
    for sa, sb, sc in itertools.product((1, -1), repeat=3):
        rows.append(("all three one spread (%+d, %+d, %+d)" % (sa, sb, sc), opt(sa, sb, sc)))
    out = []
    for nm, o in rows:
        v = view(world, o)["pool"]
        near = min((min(abs(v[b] - LINE), abs(v[b] + LINE)), b) for b in MEMBERS)
        out.append((nm, calls(v) == gc, near[0], near[1], v))
    return out, sp


def forcing(world, x):
    rows, sp = forcing_rows(world, x)
    print("measured spreads (share recorded, per cent of itself; cycle level, marks; standard, marks):")
    for b in MEMBERS:
        print("  %-10s %5.1f%%  %5.2f  %5.2f" % (b, 100 * sp[b]["pull"], sp[b]["cycle"], sp[b]["off"]))
    ok = True
    for nm, same, d, b, v in rows:
        ok = ok and same
        print("%-44s call %s  nearest line %.2f (%s)" % (nm, "holds" if same else "MOVES", d, b))
    fam_near = min((min(abs(f["pool"][b] - LINE), abs(f["pool"][b] + LINE)), b) for f in x["fam"] for b in MEMBERS)
    print("family of %d: nearest approach to a line %.2f (%s)" % (len(x["fam"]), fam_near[0], fam_near[1]))
    print("FORCING %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def detail(world, spec, x):
    g, lat = x["g"], x["lat"]
    print("board       truth golden spread |   S1    S2    S3 | S1S2  S1S3  S2S3 | reflex direct rigor | share  off  cycle")
    for b in MEMBERS:
        m = spec["members"][b]
        sp = max(abs(v - m["golden"]) for v in m["family"])
        P = g["parts"][b]
        print("%-10s %6.2f %6.2f %5.2f | %5.2f %5.2f %5.2f | %5.2f %5.2f %5.2f | %5.2f %5.2f %5.2f | %.3f %5.2f %s" % (
            b, m["truth"], m["golden"], sp, lat["S1"]["pool"][b], lat["S2"]["pool"][b], lat["S3"]["pool"][b],
            lat["S1+S2"]["pool"][b], lat["S1+S3"]["pool"][b], lat["S2+S3"]["pool"][b], lat["S1+S2+S3"]["pool"][b],
            m["routes"]["direct"], m["routes"]["rigorous"], P["pull"], P["off"], np.round(P["theta"], 2)))
    for y in BANKED:
        print(y, "truth", {b[:3]: round(x["tr_by"][y][b], 2) for b in MEMBERS}, "golden",
              {b[:3]: round(g["by"][y][b], 2) for b in MEMBERS})
    print("six boards: truth %.2f golden %.2f reflex %.2f rigorous %.2f" % (
        national(world, x["tr"]), g["nat"], lat["S1+S2+S3"]["nat"], national(world, x["rg"])))
    r = spec["referee"]
    print("referee: slice %.2f golden %.2f | %s | every centre read raw %.2f" % (
        r["truth"], r["golden"], ", ".join("%s %.2f" % kv for kv in r["rivals"].items()), review_raw(world)))
    print("calls (%s): truth %s golden %s" % (", ".join(b[:3] for b in MEMBERS), calls(x["tr"]), calls(g["pool"])))
    for k, v in lat.items():
        print("  %-9s %s" % (k, calls(v["pool"])))
    print("  direct    %s\n  rigorous  %s" % (calls(x["dr"]), calls(x["rg"])))
    for b, w in world["B"].items():
        s = w["samp"][:, -6:]
        a = w["adj"][:, -6:][s]
        print("  %-10s rota %d  mean recorded difference %.2f  centres adjusted %.0f%%" % (
            b, w["P"]["k"], float(np.mean(w["G"][:, -6:][s])), 100 * float(np.mean(a != 0))))
    wide = {b: VARIANTS[max(range(len(x["fam"])), key=lambda i: abs(x["fam"][i]["pool"][b] - g["pool"][b]))][0]
            for b in MEMBERS}
    print("widest variant:", wide)


def main():
    world = simulate()
    spec, x = build(world)
    if "--detail" in sys.argv:
        detail(world, spec, x)
    if "--forcing" in sys.argv:
        return forcing(world, x)
    return corelib.run(spec)


if __name__ == "__main__":
    sys.exit(main())
