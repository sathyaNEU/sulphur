"""task24: everything graded, computed from the cut pack alone: the golden, its bootstrap band, the golden family of
defensible rivals, the hurried routes the factorial and the effort passes run, and the perturbations the forcing
block records."""
import os

import numpy as np

import analysis as A
import readpack as RP

FAMILY = [  # defensible rivals: each a different but sound method on the same estimand
    ("the learning curve as a logistic in log label information", dict(form="hill")),
    ("each run's pull a share of the square root of its labels' crowd share", dict(tilt="sqrt")),
    ("each source's error as its plain disagreement with unanimous technicians", dict(errors="plain")),
    ("the contrast in three bins, not nine", dict(bins="coarse")),
    ("the order's comparisons used in full, no-preference judgments included", dict(ties="kept")),
    ("the technicians' error and split share from the audit alone", dict(review_votes=False)),
    ("the crowd's pull read from the audit, not the deliveries", dict(pull="audit")),
    ("the learning curve fitted on the seven reviewed runs alone", dict(internal=False)),
]
RULED_OUT = [  # rivals the records reject, with the test that rejects them
    ("a separate bend of the learning curve for each ticket type", dict(alpha="by_type"), "alpha"),
    ("IS-25's labels read at the 2026 audit's crowd error", dict(is_error="audit"), "is_error"),
]
DROPS = {
    "J2": ("labels weighted by their accuracy, not their information", dict(value="acc")),
    "J2raw": ("labels counted", dict(value="raw")),
    "J3": ("no pull to the longer reply in the bridge or the curve", dict(tilt="none")),
    "J4": ("accuracy rising with log label information, no bound", dict(form="loglin")),
    "J1alone": ("the bridge right; labels weighted by accuracy, no pull, no bound", dict(value="acc", tilt="none", form="loglin")),
}


def purchase(R):
    if R["best"] is None:
        return dict(option=None, desk=None, cost=None, reach=False)
    return dict(option=int(R["best"][1]), desk=int(R["best"][2]), cost=float(R["best"][0]), reach=True)


def cells(R, V):
    """a route's graded tables: current, signed order, whole option, each Ardentdesk volume, by type and the mix"""
    m27 = V["mix27"]
    out = dict(current=list(R["current"]) + [R["current_mix"]],
               order=list(R["grid"][0]) + [R["grid_mix"][0]],
               option=list(R["option_acc"]) + [R["option_mix"]])
    for x in A.VOLS[1:]:
        out["desk_%d" % x] = list(R["grid"][x]) + [R["grid_mix"][x]]
    return {k: [float(v) for v in vv] for k, vv in out.items()}


def perturb(G, V, which, factor):
    """the golden's fit with one fitted input moved, everything else held, the purchase recomputed"""
    C = dict(G["C"]); S = dict(C["S"]); theta = np.array(G["theta"], float)
    opt = G["opt"]
    if which == "K_troubleshooting":
        theta[4] += np.log(factor)
    elif which == "alpha":
        theta[5] *= factor
    elif which == "kappa":
        theta[6] *= factor
    elif which == "crowd_info":
        C["IA"] = C["IA"].copy(); C["IA"][4] *= factor
    elif which == "desk_info":
        C["IB"] = C["IB"].copy(); C["IB"][4] *= factor
    elif which == "split_share":
        S["a"] = S["a"].copy(); S["a"][4] *= factor
    C["S"] = S
    nA0, nB0, usable = A.plan(V, C, opt)
    m27 = V["mix27"]; dm = V["desk_mix"]; ou = m27 * (1 - C["tie"])
    f = lambda o, x: float((A.acc_standard(theta, C, nA0 + usable + o * ou, nB0 + x * dm, opt) * m27).sum())
    best = A.least_cost(f, V)
    return dict(option=(int(best[1]) if best else None), desk=(int(best[2]) if best else None),
                cost=(float(best[0]) if best else None))


def _review_overall(V):
    R = V["REV"]
    maj = np.where(np.stack([(R["vote%d" % k].values == "B") for k in (1, 2, 3)], 1).sum(1) >= 2, "B", "A")
    return {rid: float((R.pick.values[R.run_id.values == rid] == maj[R.run_id.values == rid]).mean())
            for rid in sorted(set(R.run_id.values))}


def vendor_error(V):
    """each vendor's error against the standard by ticket type: the share of its audit judgments (no-preference set
    aside) whose reply is not the one at least two of the three technicians chose, every audit pair counted"""
    ST = V["ST"]
    maj = np.where(np.stack([(ST["tech%d" % k].values == "B") for k in (1, 2, 3)], 1).sum(1) >= 2, "B", "A")
    out = {}
    for src, name in (("crowd", "tallyfield"), ("desk", "ardentdesk")):
        for d, t in enumerate(RP.TYPES):
            s = ST.type.values == d
            w = n = 0
            for k in (1, 2, 3):
                v = ST["%s%d" % (src, k)].values[s]
                okv = v != "none"
                w += (v[okv] != maj[s][okv]).sum(); n += okv.sum()
            out["%s.%s" % (name, t)] = float(w / n)
    return out


def quick_vendor_error(target):
    """the quick pass's reading: Tallyfield's own gold-question accuracy, as an error rate for every ticket type"""
    import re
    txt = RP.pdf_text(os.path.join(target, "tallyfield_quality_summary_2026.pdf"))
    vals = [float(x) for x in re.findall(r"(\d{2}\.\d)%", txt)]
    return float(round(100 - np.mean(vals), 1)) if vals else None


def compute(target, n_boot=40):
    V = RP.view(target)
    G = A.golden(V)
    B = A.band(V, G, n_boot=n_boot)
    out = dict(V=V, G=G, B=B, cells=cells(G, V), purchase=purchase(G), vendor_error=vendor_error(V),
               quick_vendor_error=quick_vendor_error(target))
    fam = []
    for name, o in FAMILY:
        R = A.golden(V, o)
        fam.append(dict(name=name, opt=o, purchase=purchase(R), cells=cells(R, V)))
    out["family"] = fam
    ruled = []
    for name, o, key in RULED_OUT:
        R = A.golden(V, o)
        k_extra = (A.ND - 1) if key == "alpha" else 0
        lr = 2.0 * (G["nll"] - R["nll"])
        ruled.append(dict(name=name, opt=o, purchase=purchase(R), cells=cells(R, V), lr=float(lr), df=k_extra))
    out["ruled_out"] = ruled
    drops = {}
    for key, (name, o) in DROPS.items():
        R = A.golden(V, o)
        drops[key] = dict(name=name, purchase=purchase(R), cells=cells(R, V))
    C = G["C"]
    routes = {
        "J1": ("the internal set read through the reviews by a constant per ticket type", ("const", "info", "struct_tilt")),
        "reflex": ("the careful but hurried pass: IS-25 plus a constant per type, labels weighted by accuracy, no pull, "
                   "accuracy rising with log labels", ("const", "acc", "loglin")),
        "J2alone": ("the reflex route with labels weighted by information", ("const", "info", "loglin")),
        "J3alone": ("the reflex route with the pull", ("const", "acc", "struct_tilt")),
        "J4alone": ("the reflex route with the bound", ("const", "acc", "struct")),
        "quick": ("the dashboard figures, labels counted, a straight line in log labels", ("dashboard", "raw", "loglin")),
        "textbook": ("IS-25 corrected for the crowd's error with no shared pull", ("textbook", "info", "struct")),
    }
    for key, (name, args) in routes.items():
        R = A.hurried(V, *args, C=C)
        drops[key] = dict(name=name, purchase=purchase(R), cells=cells(R, V))
    out["drops"] = drops
    pert = []
    lk, al, kap, _ = A._split(G["theta"], G["opt"])
    value = dict(K_troubleshooting=float(np.exp(lk[4])), alpha=float(al), kappa=float(kap),
                 crowd_info=float(G["C"]["IA"][4]), desk_info=float(G["C"]["IB"][4]), split_share=float(G["C"]["S"]["a"][4]))
    for which in ("K_troubleshooting", "alpha", "kappa", "crowd_info", "desk_info", "split_share"):
        rel = B["spread"][which] / value[which]          # each fitted input moved by its own bootstrap spread
        for f in (1 + rel, 1 - rel):
            pert.append(dict(input=which, factor=float(f), spread=float(B["spread"][which]), value=value[which],
                             **perturb(G, V, which, f)))
    out["perturbations"] = pert
    # the cheapest purchase at each tranche of the option, in the golden's own model
    f = G["forecast"]
    tranches = {}
    for o in range(0, 80001, int(V["option_step"])):
        g = lambda x: f(o, x) - V["bar"]
        if g(0) >= 0:
            x = 0
        elif g(V["cap"]) < 0:
            tranches[o] = None; continue
        else:
            from scipy.optimize import brentq
            x = int(np.ceil(brentq(g, 0, V["cap"], xtol=1.0) / V["step"]) * V["step"])
            x = max(x, int(V["min_order"]))
            while g(x) < 0:
                x += int(V["step"])
        tranches[o] = dict(desk=int(x), cost=float(o * V["price_tf"] + x * V["price_ad"]))
    out["tranches"] = tranches
    agr, rev = A.per_run_measures(V)
    X = V["register"]
    out["D"] = dict(dashboard=float(X.loc[X.run_id == V["production"], "is25_agreement_pct"].iloc[0]) / 100.0,
                    is25={r: float(v) / 100.0 for r, v in zip(X.run_id, X.is25_agreement_pct)},
                    review=_review_overall(V),
                    status=dict(zip(X.run_id, X.status)))
    return out
