"""task24 analysis: the golden estimate and every rival and hurried route, computed from the pack as readpack.py
reads it (never from the generator's constants).

The golden, in the order the work runs:
  1. the label audit: each source's error by ticket type against the technicians, the share of pairs the replies are
     as good as each other, and the crowd's pull to the longer reply, by one latent-class likelihood over every audit
     judgment; the pull's shape by contrast from every usable 2026 Tallyfield judgment;
  2. each label's information to the reward model, (1 - 2 x its error)^2 on the pairs that have a better reply;
  3. one likelihood over every run's picks on the internal set (whose labels are the crowd's, so a run's agreement
     with them depends on its accuracy, the crowd's error and the pull the two share) and the six shadow reviews
     (against the technicians), with each run's clear-pair accuracy on a learning curve in label information and its
     pull a share of its labels' pull;
  4. accuracy against the majority of three technicians by type for the production run and for the Q1 2027 model at
     each Ardentdesk volume, the volume the bar needs, the band and the cost."""
import numpy as np
from scipy.optimize import brentq, least_squares, minimize
from scipy.special import expit, logit

ND = 5
BINS = np.array([0.0, 0.04, 0.08, 0.13, 0.19, 0.26, 0.35, 0.50, 0.75, 9.0])
COARSE = np.array([0.0, 0.13, 0.35, 9.0])
VOLS = (0, 20000, 40000, 60000, 80000, 120000)
GOLDEN = dict(errors="latent", pull="deliveries", form="power", alpha="pooled", tilt="share", bins="fine",
              internal=True, reviews=True, ties="deducted", q="pooled", is_error="fitted", value="info")


def cbin(wa, wb, bins=BINS):
    c = np.abs(np.log(wb / wa))
    return np.clip(np.searchsorted(bins, c, side="right") - 1, 0, len(bins) - 2)


def side(wa, wb, choice):
    """True where the judgment (or pick) is for the longer reply; for equal lengths, for reply B"""
    lb = wb > wa
    eq = wa == wb
    return np.where(eq, choice == "B", (choice == "B") == lb)


# ------------------------------------------------------------------ 1. the label audit
def audit_arrays(ST, bins, REV=None):
    """the audit's judgments, and (when given) the shadow reviews' technician votes as pairs judged by the
    technicians alone"""
    wa, wb = ST.words_a.values, ST.words_b.values
    t = ST.type.values
    out = dict(t=t, b=cbin(wa, wb, bins), eq=wa == wb)
    for src in ("tech", "crowd", "desk"):
        cols = [ST["%s%d" % (src, k)].values for k in (1, 2, 3)]
        out[src + "_L"] = np.stack([side(wa, wb, c) for c in cols], 1)      # for the longer reply
        out[src + "_M"] = np.stack([c != "none" for c in cols], 1)
    if REV is not None:
        ra, rb = REV.words_a.values, REV.words_b.values
        n = len(REV)
        out["t"] = np.r_[t, REV.type.values]
        out["b"] = np.r_[out["b"], cbin(ra, rb, bins)]
        out["eq"] = np.r_[out["eq"], ra == rb]
        out["tech_L"] = np.r_[out["tech_L"], np.stack([side(ra, rb, REV["vote%d" % k].values) for k in (1, 2, 3)], 1)]
        out["tech_M"] = np.r_[out["tech_M"], np.ones((n, 3), bool)]
        for src in ("crowd", "desk"):
            out[src + "_L"] = np.r_[out[src + "_L"], np.zeros((n, 3), bool)]
            out[src + "_M"] = np.r_[out[src + "_M"], np.zeros((n, 3), bool)]
    return out


def _audit_unpack(x, nb):
    a = expit(x[0:5]); t = expit(x[5:10]); ea = expit(x[10:15]); eb = expit(x[15:20]); q = expit(x[20])
    pull = expit(x[21:21 + nb])
    return a, t, ea, eb, q, pull


def audit_nll(x, A, nb, pull_fixed=None):
    a, t, ea, eb, q, pull = _audit_unpack(x, nb)
    if pull_fixed is not None:
        pull = pull_fixed
    d, b, eq = A["t"], A["b"], A["eq"]
    qq = np.where(eq, 0.5, q)
    cp = np.where(eq, 0.0, pull[b])
    # classes: 0 as good as each other, 1 the longer (or B) better, 2 the other better
    logp = np.stack([np.log(a[d]), np.log(1 - a[d]) + np.log(qq), np.log(1 - a[d]) + np.log(1 - qq)], 1)
    for src, e in (("tech", t), ("desk", eb), ("crowd", ea)):
        L, M = A[src + "_L"], A[src + "_M"]
        for cls in range(3):
            pL = np.full(len(d), 0.5) if cls == 0 else (1 - e[d] if cls == 1 else e[d])
            if src == "crowd":
                pL = cp + (1 - cp) * pL
            pL = np.clip(pL, 1e-9, 1 - 1e-9)[:, None]
            logp[:, cls] += np.where(M, np.where(L, np.log(pL), np.log(1 - pL)), 0.0).sum(1)
    m = logp.max(1)
    return -(m + np.log(np.exp(logp - m[:, None]).sum(1))).sum()


def audit_latent(ST, bins=BINS, pull_fixed=None, REV=None, iters=400, tol=1e-9):
    """one latent-class model over every audit judgment (and the reviews' technician votes): each pair has no better
    reply, or the longer (for equal lengths, reply B) better, or the other; each source errs at its own rate by
    ticket type; a crowd judgment is pulled to the longer reply at a rate by length bin, else judged. Fitted by EM."""
    A = audit_arrays(ST, bins, REV)
    nb = len(bins) - 1
    d, b, eq = A["t"], A["b"], A["eq"]
    n = len(d)
    a = np.full(ND, 0.1); t = np.full(ND, 0.04); ea = np.full(ND, 0.2); eb = np.full(ND, 0.08); q = 0.5
    pull = np.full(nb, 0.1) if pull_fixed is None else np.asarray(pull_fixed, float)
    L = {s_: A[s_ + "_L"] for s_ in ("tech", "desk", "crowd")}
    M = {s_: A[s_ + "_M"] for s_ in ("tech", "desk", "crowd")}
    prev = None
    for it in range(iters):
        qq = np.where(eq, 0.5, q)
        logp = np.stack([np.log(a[d]), np.log(1 - a[d]) + np.log(qq), np.log(1 - a[d]) + np.log(1 - qq)], 1)
        for src, e in (("tech", t), ("desk", eb)):
            for cls in range(3):
                pL = (np.full(n, 0.5) if cls == 0 else (1 - e[d] if cls == 1 else e[d]))[:, None]
                logp[:, cls] += np.where(M[src], np.where(L[src], np.log(pL), np.log(1 - pL)), 0.0).sum(1)
        cp = np.where(eq, 0.0, pull[b])[:, None]
        crowd_pl = []
        for cls in range(3):
            base = (np.full(n, 0.5) if cls == 0 else (1 - ea[d] if cls == 1 else ea[d]))[:, None]
            pL = cp + (1 - cp) * base
            crowd_pl.append((pL, base))
            logp[:, cls] += np.where(M["crowd"], np.where(L["crowd"], np.log(pL), np.log(1 - pL)), 0.0).sum(1)
        mx = logp.max(1, keepdims=True)
        ll = float((mx[:, 0] + np.log(np.exp(logp - mx).sum(1))).sum())
        R = np.exp(logp - mx); R /= R.sum(1, keepdims=True)
        # M-step
        for k in range(ND):
            s_ = d == k
            a[k] = R[s_, 0].mean()
        ne = ~eq
        q = float((R[ne, 1].sum()) / (R[ne, 1] + R[ne, 2]).sum())
        for src, e in (("tech", t), ("desk", eb)):
            wrong = (R[:, 1][:, None] * (~L[src]) + R[:, 2][:, None] * L[src]) * M[src]
            tot = (R[:, 1] + R[:, 2])[:, None] * M[src]
            for k in range(ND):
                s_ = d == k
                e[k] = wrong[s_].sum() / max(tot[s_].sum(), 1e-12)
        # crowd: the pulled share of each judgment, by class
        Lc, Mc = L["crowd"], M["crowd"]
        ez = np.zeros(Lc.shape); w_wrong = np.zeros(Lc.shape); w_judged = np.zeros(Lc.shape)
        for cls in range(3):
            pL, base = crowd_pl[cls]
            z = np.where(Lc, cp / np.maximum(pL, 1e-12), 0.0)          # pulled, given the judgment and the class
            ez += R[:, cls][:, None] * z
            if cls > 0:
                wrong = np.where(cls == 1, ~Lc, Lc)
                w = R[:, cls][:, None] * (1 - z)
                w_wrong += w * wrong
                w_judged += w
        ez *= Mc; w_wrong *= Mc; w_judged *= Mc
        if pull_fixed is None:
            for k in range(nb):
                s_ = (b == k) & ~eq
                cnt = Mc[s_].sum()
                pull[k] = ez[s_].sum() / cnt if cnt else 0.0
        for k in range(ND):
            s_ = d == k
            ea[k] = w_wrong[s_].sum() / max(w_judged[s_].sum(), 1e-12)
        if prev is not None and abs(ll - prev) < tol * abs(ll):
            break
        prev = ll
    return dict(a=a, t=t, ea=ea, eb=eb, q=float(q), pull_audit=pull, loglik=ll)


def audit_plain(ST):
    """the plain reading: each source's disagreement with the technicians on pairs all three agreed on, the split
    share as the pairs the technicians did not all agree on"""
    tv = np.stack([(ST["tech%d" % k].values == "B") for k in (1, 2, 3)], 1).sum(1)
    unan = (tv == 0) | (tv == 3)
    truth_b = tv >= 2
    t = ST.type.values
    out = {}
    for src in ("crowd", "desk"):
        e = np.zeros(ND)
        for d in range(ND):
            s = (t == d) & unan
            w = n = 0
            for k in (1, 2, 3):
                v = ST["%s%d" % (src, k)].values[s]
                ok = v != "none"
                w += ((v[ok] == "B") != truth_b[s][ok]).sum(); n += ok.sum()
            e[d] = w / n
        out[src] = e
    split = np.array([(~unan[t == d]).mean() for d in range(ND)])
    return out["crowd"], out["desk"], split


def pull_from_deliveries(TF, S, bins=BINS):
    U = TF[TF.choice != "none"]
    wa, wb = U.words_a.values, U.words_b.values
    ne = wa != wb
    t = U.type.values[ne]; b = cbin(wa[ne], wb[ne], bins)
    took_longer = side(wa[ne], wb[ne], U.choice.values[ne])
    a, ea, q = S["a"], S["ea"], S["q"]
    base = (1 - a[t]) * (q * (1 - ea[t]) + (1 - q) * ea[t]) + a[t] * 0.5
    pull = np.zeros(len(bins) - 1)
    for k in range(len(bins) - 1):
        s = b == k
        obs = took_longer[s].mean(); bb = base[s].mean()
        pull[k] = max(0.0, (obs - bb) / (1 - bb))
    return pull


def contrast_profile(TF, bins=BINS):
    wa, wb = TF.words_a.values, TF.words_b.values
    t = TF.type.values; b = cbin(wa, wb, bins); eq = wa == wb
    prof = np.zeros((ND, len(bins) - 1)); eqs = np.zeros(ND)
    for d in range(ND):
        s = t == d
        eqs[d] = eq[s].mean()
        prof[d] = np.bincount(b[s & ~eq], minlength=len(bins) - 1) / s.sum()
    return prof, eqs


def info_weights(S, pull, prof, eqs):
    """each label's information about which reply is better: the square of its signal, the gap between its chance of
    naming a reply when that reply is the better one and when it is not; a judgment pulled to the longer reply carries
    none, and a pair with no better reply teaches nothing"""
    a, ea, eb = S["a"], S["ea"], S["eb"]
    IA = np.zeros(ND); IB = np.zeros(ND)
    for d in range(ND):
        ia = (prof[d] * ((1 - pull) * (1 - 2 * ea[d])) ** 2).sum() + eqs[d] * (1 - 2 * ea[d]) ** 2
        IA[d] = (1 - a[d]) * ia
        IB[d] = (1 - a[d]) * (1 - 2 * eb[d]) ** 2
    return IA, IB


def stage1(V, opt):
    bins = BINS if opt["bins"] == "fine" else COARSE
    rev = V["REV"] if opt.get("review_votes", True) else None
    if opt["errors"] == "latent":
        S = audit_latent(V["ST"], bins, REV=rev)
    else:
        ea, eb, split = audit_plain(V["ST"])
        S0 = audit_latent(V["ST"], bins, REV=rev)
        S = dict(S0, ea=ea, eb=eb)
    pull = pull_from_deliveries(V["TF"], S, bins) if opt["pull"] == "deliveries" else S["pull_audit"]
    prof, eqs = contrast_profile(V["TF"], bins)
    IA, IB = info_weights(S, pull, prof, eqs)
    if opt.get("value") == "acc":
        IA, IB = 1 - S["ea"], 1 - S["eb"]
    elif opt.get("value") == "raw":
        IA, IB = np.ones(ND), np.ones(ND)
    tie = np.array([(V["TF"].choice.values[V["TF"].type.values == d] == "none").mean() for d in range(ND)])
    return dict(S=S, pull=pull, prof=prof, eqs=eqs, IA=IA, IB=IB, tie=tie, bins=bins)


# ------------------------------------------------------------------ 2-3. the runs' evidence and the joint fit
def evidence(V, bins):
    IS = V["IS"]
    wa, wb = IS.words_a.values, IS.words_b.values
    t = IS.type.values; b = cbin(wa, wb, bins); eq = (wa == wb).astype(int)
    ll = side(wa, wb, IS.label.values).astype(int)
    nb = len(bins) - 1
    rows = []
    for ri, rid in enumerate(V["runs"]):
        pk = side(wa, wb, V["picks"][rid]).astype(int)
        key = ((t * nb + b) * 2 + eq) * 2 + ll
        n = np.bincount(key, minlength=ND * nb * 4)
        k = np.bincount(key, weights=pk, minlength=ND * nb * 4)
        nz = np.nonzero(n)[0]
        for c in nz:
            l_ = c % 2; e_ = (c // 2) % 2; bb = (c // 4) % nb; dd = c // (4 * nb)
            rows.append((ri, dd, bb, e_, l_, n[c], k[c]))
    E = np.array(rows, float)
    R = V["REV"]
    wa, wb = R.words_a.values, R.words_b.values
    rv = dict(r=np.array([V["runs"].index(x) for x in R.run_id.values]), t=R.type.values, b=cbin(wa, wb, bins),
              eq=(wa == wb), votes=sum(side(wa, wb, R["vote%d" % k].values).astype(int) for k in (1, 2, 3)),
              pick=side(wa, wb, R.pick.values))
    return dict(r=E[:, 0].astype(int), d=E[:, 1].astype(int), b=E[:, 2].astype(int), eq=E[:, 3].astype(bool),
                ll=E[:, 4].astype(bool), n=E[:, 5], k=E[:, 6]), rv


def curve(neff, K, al, form):
    if form == "power":
        return 1 - 0.5 * (1 + neff / K) ** (-al)
    if form == "loglin":
        return np.minimum(0.9999, 0.5 + 0.1 * al * np.log1p(neff / K))
    x = (np.maximum(neff, 0) / K) ** al
    return 0.5 + 0.5 * x / (1 + x)


def tilt_of(s, kap, form):
    if form == "share":
        return kap * s
    if form == "sqrt":
        return kap * np.sqrt(s)
    return 0.0 * s


def _split(theta, opt):
    nd = ND
    na = 1 if opt["alpha"] == "pooled" else nd
    lk = theta[:nd]
    al = theta[nd] if opt["alpha"] == "pooled" else theta[nd:nd + na]
    kap = theta[nd + na]
    eis = expit(theta[nd + na + 1:nd + na + 1 + nd]) if opt.get("is_error") == "fitted" else None
    return lk, al, kap, eis


def run_state(theta, C, nA, nB, opt):
    lk, al, kap, _ = _split(theta, opt)
    neff = nA * C["IA"] + nB * C["IB"]
    p = curve(neff, np.exp(lk), al, opt["form"])
    s = np.where(nA + nB > 0, nA / np.maximum(nA + nB, 1), 0.0)
    return p, tilt_of(s, kap, opt["tilt"])


def joint_nll(theta, C, E, RV, opt):
    S, pull = C["S"], C["pull"]
    a, ea, q, tt = S["a"], S["ea"], S["q"], S["t"]
    eis = _split(theta, opt)[3]
    if eis is not None:
        ea = eis
    NA, NB = C["NA"], C["NB"]
    P = np.zeros((len(NA), ND)); TS = np.zeros((len(NA), ND))
    for i in range(len(NA)):
        P[i], TS[i] = run_state(theta, C, NA[i], NB[i], opt)
    tot = 0.0
    if opt["internal"]:
        r, d, b, eq, ll, n, k = E["r"], E["d"], E["b"], E["eq"], E["ll"], E["n"], E["k"]
        p = P[r, d]; ts = TS[r, d]
        mp = np.where(eq, 0.0, ts * pull[b])
        pl = np.stack([mp + (1 - mp) * 0.5, mp + (1 - mp) * p, mp + (1 - mp) * (1 - p)], 1)
        cp = np.where(eq, 0.0, pull[b])
        cl = np.stack([cp + (1 - cp) * 0.5, cp + (1 - cp) * (1 - ea[d]), cp + (1 - cp) * ea[d]], 1)
        cl = np.where(ll[:, None], cl, 1 - cl)
        qq = np.where(eq, 0.5, q)
        w = np.stack([a[d], (1 - a[d]) * qq, (1 - a[d]) * (1 - qq)], 1) * cl
        pm = np.clip((w * pl).sum(1) / w.sum(1), 1e-9, 1 - 1e-9)
        tot += (k * np.log(pm) + (n - k) * np.log(1 - pm)).sum()
    if opt["reviews"]:
        r, d, b, eq, vl, pk = RV["r"], RV["t"], RV["b"], RV["eq"], RV["votes"], RV["pick"]
        p = P[r, d]; ts = TS[r, d]
        mp = np.where(eq, 0.0, ts * pull[b])
        pl = np.stack([mp + (1 - mp) * 0.5, mp + (1 - mp) * p, mp + (1 - mp) * (1 - p)], 1)
        pl = np.where(pk[:, None], pl, 1 - pl)
        t_ = tt[d]
        v = np.stack([np.full(len(d), 0.125), (1 - t_) ** vl * t_ ** (3 - vl), t_ ** vl * (1 - t_) ** (3 - vl)], 1)
        qq = np.where(eq, 0.5, q)
        w = np.stack([a[d], (1 - a[d]) * qq, (1 - a[d]) * (1 - qq)], 1) * v
        tot += np.log((w * pl).sum(1) / w.sum(1)).sum()
    return -tot


def fit_runs(V, C, opt):
    E, RV = evidence(V, C["bins"])
    C = dict(C, NA=np.array([V["counts"][r][0] for r in V["runs"]]), NB=np.array([V["counts"][r][1] for r in V["runs"]]))
    na = 1 if opt["alpha"] == "pooled" else ND
    x0 = np.r_[np.log(np.full(ND, 2000.0)), np.full(na, 0.8), 0.5]
    bounds = [(2, 14)] * ND + [(0.1, 3.0)] * na + [(0.0, 2.0)]
    if opt["tilt"] == "none":
        bounds[-1] = (0.0, 0.0); x0[-1] = 0.0
    if opt.get("is_error") == "fitted":
        x0 = np.r_[x0, logit(np.clip(C["S"]["ea"], 0.02, 0.48))]
        bounds += [(logit(0.01), logit(0.49))] * ND
    r = minimize(joint_nll, x0, args=(C, E, RV, opt), method="L-BFGS-B", bounds=bounds)
    return r.x, r.fun


def maj_err(t):
    return 3 * t ** 2 * (1 - t) + t ** 3


def acc_standard(theta, C, nA, nB, opt):
    S, pull, prof, eqs = C["S"], C["pull"], C["prof"], C["eqs"]
    p, ts = run_state(theta, C, nA, nB, opt)
    a, q, tt = S["a"], S["q"], S["t"]
    out = np.zeros(ND)
    for d in range(ND):
        m = maj_err(tt[d])
        g = lambda r: r * (1 - m) + (1 - r) * m
        mp = ts[d] * pull
        r_lb = mp + (1 - mp) * p[d]
        r_sb = (1 - mp) * p[d]
        clear = (prof[d] * (q * g(r_lb) + (1 - q) * g(r_sb))).sum() + eqs[d] * g(p[d])
        out[d] = (1 - a[d]) * clear + a[d] * 0.5
    return out


# ------------------------------------------------------------------ 4. the forecast, the dial, the band, the cost
def plan(V, C, opt):
    usable = V["order"] * (1 - C["tie"]) if opt["ties"] == "deducted" else V["order"].astype(float)
    nA0, nB0 = V["counts"][V["production"]]
    return nA0, nB0, usable


def dial_volume(f, bar, cap_search=2_000_000):
    g = lambda x: f(x) - bar
    if g(0) >= 0:
        return 0.0
    if g(cap_search) < 0:
        return float("inf")
    return brentq(g, 0, cap_search, xtol=1.0)


def least_cost(f, V):
    """the cheapest purchase that reaches the bar: Tallyfield's option in its steps, Ardentdesk comparisons in theirs
    (at least the minimum order), within each vendor's limit; None when nothing within the limits reaches it"""
    best = None
    for o in range(0, int(V["option"]) + 1, int(V["option_step"])):
        g = lambda x: f(o, x) - V["bar"]
        if g(0) >= 0:
            x = 0
        elif g(V["cap"]) < 0:
            continue
        else:
            xs = brentq(g, 0, V["cap"], xtol=1.0)
            x = int(np.ceil(xs / V["step"]) * V["step"])
            x = max(x, int(V["min_order"]))
            while x < V["cap"] and g(x) < 0:
                x += int(V["step"])
        cost = o * V["price_tf"] + x * V["price_ad"]
        if best is None or cost < best[0] - 1e-6:
            best = (cost, o, x)
    return best


def desk_needed(f, V, option=0):
    """the Ardentdesk volume (exact, before steps) at which the expected accuracy reaches the bar, with the option at
    the given volume"""
    return dial_volume(lambda x: f(option, x), V["bar"])


def golden(V, opt=None):
    opt = dict(GOLDEN, **(opt or {}))
    C = stage1(V, opt)
    theta, nll = fit_runs(V, C, opt)
    nA0, nB0, usable = plan(V, C, opt)
    m27 = V["mix27"]; dm = V["desk_mix"]
    opt_usable = m27 * (1 - C["tie"]) if opt["ties"] == "deducted" else m27

    def acc(o, x):
        return acc_standard(theta, C, nA0 + usable + o * opt_usable, nB0 + x * dm, opt)
    f = lambda o, x: float((acc(o, x) * m27).sum())
    cur = acc_standard(theta, C, nA0, nB0, opt)
    grid = {x: acc(0, x) for x in VOLS}
    full_option = acc(V["option"], 0)
    best = least_cost(f, V)
    xs = desk_needed(f, V)
    return dict(opt=opt, C=C, theta=theta, nll=nll, current=cur, current_mix=float((cur * m27).sum()), grid=grid,
                grid_mix={x: float((g * m27).sum()) for x, g in grid.items()}, option_acc=full_option,
                option_mix=float((full_option * m27).sum()), best=best,
                volume=(best[2] if best else float("inf")), option_bought=(best[1] if best else None),
                volume_exact=xs, at_volume=(f(best[1], best[2]) if best else None),
                cost=(best[0] if best else None), forecast=f, acc=acc)


def resample(V, rng):
    """one bootstrap replicate: the audit's pairs, the internal set's pairs (every run's pick on a pair moves with
    it), each review round's drafts, and the deliveries"""
    W = dict(V)
    ST = V["ST"]
    W["ST"] = ST.iloc[np.sort(rng.integers(0, len(ST), len(ST)))].reset_index(drop=True)
    idx = np.sort(rng.integers(0, len(V["IS"]), len(V["IS"])))
    W["IS"] = V["IS"].iloc[idx].reset_index(drop=True)
    W["picks"] = {r: np.asarray(p)[idx] for r, p in V["picks"].items()}
    parts = []
    for rid, g in V["REV"].groupby("run_id", sort=True):
        parts.append(g.iloc[np.sort(rng.integers(0, len(g), len(g)))])
    W["REV"] = __import__("pandas").concat(parts, ignore_index=True)
    TF = V["TF"]
    W["TF"] = TF.iloc[np.sort(rng.integers(0, len(TF), len(TF)))].reset_index(drop=True)
    return W


def band(V, G, n_boot=60, seed=2024, level=0.80):
    """the 2027-mix accuracy's range at the recommended volume, the volume's own range, from a bootstrap of every
    record the estimate rests on"""
    rng = np.random.default_rng(seed)
    acc = []; vols = []; pars = []
    for i in range(n_boot):
        W = resample(V, rng)
        opt = G["opt"]
        C = stage1(W, opt)
        theta, _ = fit_runs(W, C, opt)
        pars.append(dict(K_troubleshooting=float(np.exp(theta[4])), alpha=float(theta[5]), kappa=float(theta[6]),
                         crowd_info=float(C["IA"][4]), desk_info=float(C["IB"][4]), split_share=float(C["S"]["a"][4])))
        nA0, nB0, usable = plan(W, C, opt)
        m27 = W["mix27"]
        dm = W["desk_mix"]
        ou = m27 * (1 - C["tie"])
        f = lambda o, x: float((acc_standard(theta, C, nA0 + usable + o * ou, nB0 + x * dm, opt) * m27).sum())
        acc.append(f(G["option_bought"], G["volume"]))
        vols.append(desk_needed(f, W))
    lo, hi = (1 - level) / 2, 1 - (1 - level) / 2
    acc = np.array(acc); vols = np.array(vols)
    spread = {k: float(np.std([p_[k] for p_ in pars], ddof=1)) for k in pars[0]}
    centre = {k: float(np.mean([p_[k] for p_ in pars])) for k in pars[0]}
    return dict(acc_lo=float(np.quantile(acc, lo)), acc_hi=float(np.quantile(acc, hi)), acc=acc, vols=vols,
                vol_lo=float(np.quantile(vols, lo)), vol_hi=float(np.quantile(vols, hi)), spread=spread, centre=centre)


# ------------------------------------------------------------------ the hurried routes
def per_run_measures(V):
    IS = V["IS"]; t = IS.type.values
    agr = np.array([[(np.asarray(V["picks"][r])[t == d] == IS.label.values[t == d]).mean() for d in range(ND)]
                    for r in V["runs"]])
    R = V["REV"]
    maj = np.where(np.stack([(R["vote%d" % k].values == "B") for k in (1, 2, 3)], 1).sum(1) >= 2, "B", "A")
    rev = {}
    for rid in sorted(set(R.run_id.values)):
        s = R.run_id.values == rid
        rev[rid] = np.array([(R.pick.values[s & (R.type.values == d)] == maj[s & (R.type.values == d)]).mean()
                             for d in range(ND)])
    return agr, rev


def hurried(V, measure="const", value="acc", form="loglin", C=None):
    """the internal set read through the six reviews (a constant per type, a line, or the textbook noise correction
    with no shared pull), or the six reviews alone; labels counted, weighted by accuracy or by information; a curve
    in log labels, a saturating curve with its own ceiling, or the split pairs' bound"""
    C = C or stage1(V, GOLDEN)
    agr, rev = per_run_measures(V)
    runs = V["runs"]
    isrev = np.array([r in rev for r in runs])
    acc_rev = np.array([rev[r] for r in runs if r in rev])
    eA, eB, split = audit_plain(V["ST"])
    S = C["S"]
    if measure == "const":
        y = agr + (acc_rev - agr[isrev]).mean(0); sel = np.ones(len(runs), bool)
    elif measure == "lin":
        y = np.zeros_like(agr)
        for d in range(ND):
            b1, b0 = np.polyfit(agr[isrev, d], acc_rev[:, d], 1); y[:, d] = b0 + b1 * agr[:, d]
        sel = np.ones(len(runs), bool)
    elif measure == "textbook":
        a = split * 0 + S["a"]; e = eA
        y = ((agr - a * 0.5) / (1 - a) - e) / (1 - 2 * e) * (1 - a) + a * 0.5; sel = np.ones(len(runs), bool)
    elif measure == "dashboard":
        y = agr; sel = np.ones(len(runs), bool)
    else:
        y = np.zeros_like(agr); y[isrev] = acc_rev; sel = isrev
    if value == "info":
        wA, wB = C["IA"], C["IB"]
    elif value == "info_plain":
        wA, wB = (1 - 2 * eA) ** 2, (1 - 2 * eB) ** 2
    elif value == "acc":
        wA, wB = 1 - eA, 1 - eB
    else:
        wA, wB = np.ones(ND), np.ones(ND)
    NA = np.array([V["counts"][r][0] for r in runs]); NB = np.array([V["counts"][r][1] for r in runs])
    X = NA * wA + NB * wB
    pars = []
    share = lambda a, b: np.where(a + b > 0, a / np.maximum(a + b, 1), 0.0)
    if form == "struct_tilt":       # the bound and the inherited pull, fitted by least squares on the measured accuracies
        sh = share(NA, NB)

        def tilt_acc(d, p, ts):
            pull = C["pull"]; prof = C["prof"]; eqs = C["eqs"]; q = S["q"]; a = S["a"][d]
            mp = ts[:, None] * pull[None, :]
            r_lb = mp + (1 - mp) * p[:, None]; r_sb = (1 - mp) * p[:, None]
            clear = (prof[d][None, :] * (q * r_lb + (1 - q) * r_sb)).sum(1) + eqs[d] * p
            return (1 - a) * clear + a * 0.5

        def res(t):
            out = []
            for d in range(ND):
                p = 1 - 0.5 * (1 + X[sel, d] / np.exp(t[d])) ** (-t[ND])
                out.append(tilt_acc(d, p, t[ND + 1] * sh[sel, d]) - y[sel, d])
            return np.concatenate(out)
        r = least_squares(res, np.r_[np.log(np.full(ND, 2000.0)), 0.8, 0.5],
                          bounds=(np.r_[np.zeros(ND), 0.05, 0.0], np.r_[np.full(ND, 16.0), 4.0, 2.0]))
        tt = r.x

        def at_tilt(xx, nA, nB):
            out = np.zeros(ND)
            for d in range(ND):
                p = 1 - 0.5 * (1 + xx[d] / np.exp(tt[d])) ** (-tt[ND])
                ts = tt[ND + 1] * (nA[d] / max(nA[d] + nB[d], 1.0))
                out[d] = tilt_acc(d, np.array([p]), np.array([ts]))[0]
            return out
    for d in range(ND if form != "struct_tilt" else 0):
        x = X[sel, d]; yy = y[sel, d]
        if form == "loglin":
            b1, b0 = np.polyfit(np.log(np.maximum(x, 1)), yy, 1); pars.append(("l", b0, b1))
        elif form == "free":
            r = least_squares(lambda t: t[0] - (t[0] - 0.5) * (1 + x / np.exp(t[1])) ** (-t[2]) - yy,
                              [0.95, np.log(2000), 0.8], bounds=([0.55, 0, 0.05], [1.0, 16, 4]))
            pars.append(("f",) + tuple(r.x))
        else:
            a = S["a"][d]
            r = least_squares(lambda t: (1 - a) * (1 - 0.5 * (1 + x / np.exp(t[0])) ** (-t[1])) + a * 0.5 - yy,
                              [np.log(2000), 0.8], bounds=([0, 0.05], [16, 4]))
            pars.append(("s",) + tuple(r.x) + (a,))

    def at(xx):
        out = np.zeros(ND)
        for d, pr in enumerate(pars):
            if pr[0] == "l":
                out[d] = pr[1] + pr[2] * np.log(max(xx[d], 1.0))
            elif pr[0] == "f":
                c, lk, al = pr[1:]; out[d] = c - (c - 0.5) * (1 + xx[d] / np.exp(lk)) ** (-al)
            else:
                lk, al, a = pr[1:]; out[d] = (1 - a) * (1 - 0.5 * (1 + xx[d] / np.exp(lk)) ** (-al)) + a * 0.5
        return np.minimum(out, 1.0)
    nA0, nB0 = V["counts"][V["production"]]
    usable = V["order"] * (1 - C["tie"])
    m27 = V["mix27"]
    dm = V["desk_mix"]
    ou = m27 * (1 - C["tie"])
    if form == "struct_tilt":
        cur = at_tilt(nA0 * wA + nB0 * wB, nA0, nB0)
        accf = lambda o, x: at_tilt((nA0 + usable + o * ou) * wA + (nB0 + x * dm) * wB, nA0 + usable + o * ou, nB0 + x * dm)
    else:
        cur = at(nA0 * wA + nB0 * wB)
        accf = lambda o, x: at((nA0 + usable + o * ou) * wA + (nB0 + x * dm) * wB)
    f = lambda o, x: float((accf(o, x) * m27).sum())
    grid = {x: accf(0, x) for x in VOLS}
    best = least_cost(f, V)
    full = accf(V["option"], 0)
    return dict(current=cur, current_mix=float((cur * m27).sum()), grid=grid,
                grid_mix={x: float((g * m27).sum()) for x, g in grid.items()}, option_acc=full,
                option_mix=float((full * m27).sum()), best=best, volume=(best[2] if best else float("inf")),
                option_bought=(best[1] if best else None), volume_exact=desk_needed(f, V),
                cost=(best[0] if best else None))
