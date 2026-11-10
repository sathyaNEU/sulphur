"""The pilot's analysis under a named set of choices: every quantity the forecast rests on, by plain name.

GOLDEN is the thorough analysis. rivals() are the other choices a thorough analyst could defend (they set each
result's band); also_ran() are choices such an analyst tries and the pack rules out. QUICK and CAREFUL are the
hurried passes, and the other configurations are shortcuts, each a complete analysis that commits to an answer.
None of this reads the prompt: it is the same arithmetic under different stated methods.

    trial     the benchmark loss the largest map-transfer trial corresponds to
    costs     what each route's labels add, per tenth of the training set
    level     the loss 512,000 expert labels would give at 128 wide
    expected  each shortlisted configuration's expected benchmark loss
    range     the four-in-five range round the named configuration
    call      the configuration to name
    counts, heldback, rate    working the six rest on (the usable record, the forecast on the runs held back, the
                              learning rate for the widest), computed and shown and not graded on their own
"""
import math

import numpy as np

import analysis as A
import sweep as S

Z80 = 1.2816
BIG_CELLS = {"exp128k_map384k": (128000, 0, 384000)}

# the thorough analysis: the expert-item yardstick calibrated to the benchmark, a level of its own at every total the
# trials ran with each route's cost read from the contrasts between mixes at one total, the gain per doubling
# shrinking past the largest runs as it did over the last two, the width steps the pilot shows, three sources of spread
GOLDEN = dict(score="yardstick", cal="linear", prefer_bench=True, lr_fix="matched", beyond="every", form="top",
              width_rule="top", lr1024="fit", counts="assembled", spread="three")
# the other sound reading of the routes: at or under the expert pool the level is the expert-label runs' own, the
# ladder put on the trials' learning rate, and only the totals past the pool are unknowns
POOL_READING = dict(GOLDEN, beyond="free")
# the ten-minute pass: the logged development loss, the ladder's straight line, every record counted
QUICK = dict(score="logged", cal="linear", prefer_bench=True, lr_fix="none", beyond="line", form="line",
             width_rule="flat", lr1024="last", counts="raw", spread=None)
# the careful analyst in a hurry: the right yardstick, then one scaling-law regression over every run, its form
# chosen among the three it tried by its own held-out miss (compute_pooled)
CAREFUL = dict(GOLDEN, pooled="best", spread="residual")
# other shortcuts, each a complete analysis that commits to an answer
LINE = dict(GOLDEN, lr_fix="none", beyond="line", form="line", width_rule="flat", spread="residual")
# the careful pass's own habit once it has levels to carry on: the best of its three forms on the runs held back
HABIT_FORMS = ("line", "quadratic", "wide")


QUADRATIC = "a quadratic in log examples through the levels"


def rivals():
    """The defensible family: every choice the pack leaves open to a thorough analyst and does not rule out. Each
    member is run end to end and has to land inside every band (checks.py)."""
    out = {}
    for cal in ("linear", "offset"):
        for wr in ("top", "flat"):
            for by in ("free", "every"):
                for pb in (True, False):
                    for form in ("top", "last", "none"):
                        name = "calibration %s, width gap %s, a level of its own %s, %s, %s" % (
                            cal, "at the largest totals" if wr == "top" else "averaged",
                            "past the pool" if by == "free" else "at every total",
                            "a scored run on its own benchmark score" if pb else "every run on the carried loss",
                            {"top": "the gain shrinking as it did", "last": "the last gain carried on undiminished",
                             "none": "no gain past the largest runs"}[form])
                        out[name] = dict(GOLDEN, cal=cal, width_rule=wr, beyond=by, prefer_bench=pb, form=form)
    out[QUADRATIC] = dict(GOLDEN, form="quadratic")       # lands between the two bounding continuations
    return out


def central(name):
    """A family member whose continuation past the largest runs is the golden's (the two others are its bounds)."""
    return name.endswith("the gain shrinking as it did")


def also_ran():
    """Choices a thorough analyst tries and the pack rules out, with what rules each out."""
    return {
        "the straight line through the levels": dict(GOLDEN, form="line"),
        "routes read against the ladder as it ran": dict(POOL_READING, lr_fix="none"),
        "expert items read without the benchmark calibration": dict(GOLDEN, cal="none"),
    }


def hinted(rows, facts, beyond):
    """The careful pass given the levels in one sentence: it takes them (past the pool only, or at every total, as
    the sentence says), carries them on with the best of its three forms on the runs held back, and keeps its
    residual range."""
    tried = {f: run_pass(rows, facts, dict(GOLDEN, beyond=beyond, form=f, spread="residual")) for f in HABIT_FORMS}
    best = min(HABIT_FORMS, key=lambda f: tried[f]["heldback"])
    out = dict(tried[best]); out["_habit_form"] = best
    return out


def scored_rows(rows, cfg):
    """The benchmark-equivalent loss of every run under the pass's reading of the scores."""
    if cfg["score"] == "yardstick":
        return A.with_yardstick(rows, cfg["cal"], cfg["prefer_bench"])
    # the logged development loss carried to the benchmark by a line through the runs the benchmark scored
    cal = [r for r in rows if r.get("bench") is not None]
    b, a = np.polyfit([r["dev"] for r in cal], [r["bench"] for r in cal], 1)
    out = []
    for r in rows:
        q = dict(r); q["yhat"] = a + b * r["dev"]
        q["y"] = r["bench"] if r.get("bench") is not None else q["yhat"]
        out.append(q)
    res = np.array([r["bench"] - (a + b * r["dev"]) for r in cal])
    return out, dict(a=float(a), b=float(b), sd=float(res.std(ddof=2)), n=len(cal))


def within_cell_sd(yr):
    cells_ = {}
    for r in yr:
        cells_.setdefault((r["stage"], r["width"], r["lr"], r["nA"], r["nB"], r["nC"]), []).append(r["y"])
    ss, dof = 0.0, 0
    for v in cells_.values():
        if len(v) > 1:
            ss += float(((np.array(v) - np.mean(v)) ** 2).sum()); dof += len(v) - 1
    return math.sqrt(ss / dof)


def _miss_key(k):
    return "%d/%d/%d/%dk" % (k[0], k[1] // 1000, k[2] // 1000, k[3] // 1000)


def compute(rows, facts, cfg, shortlist=None):
    shortlist = shortlist or S.SHORTLIST
    yr, cal = scored_rows(rows, cfg)
    out = {}
    # the usable record
    if cfg["counts"] == "assembled":
        out["counts"] = dict(complete=facts["complete"], final_scores=facts["sub_final"])
    else:
        out["counts"] = dict(complete=facts["run_ids"], final_scores=facts["sub_rows"])
    # the benchmark loss the largest map-transfer trial corresponds to (128 wide)
    out["trial"] = {k: A.cell(yr, "y", stage="vend", width=128, nA=v[0], nB=v[1], nC=v[2])[0] for k, v in BIG_CELLS.items()}
    # what each route's labels add, per tenth of the training set
    rm = A.route_model(yr, 128, "y", cfg["lr_fix"], cfg["beyond"])
    out["costs"] = dict(map_per10=rm["kC"] / 10.0, ctr_per10=rm["kB"] / 10.0)
    # the loss 512,000 expert-labelled examples would give at 128 wide
    out["level"] = rm["levels"][512000] if 512000 in rm["levels"] else rm["line"](512000)
    # the forecast checked on the pilot's largest runs held out
    miss = A.backtest(yr, 256000, "y", cfg["lr_fix"], cfg["form"], cfg["beyond"])
    out["heldback"] = float(np.mean(np.abs(list(miss.values()))))
    out["heldback_signed"] = float(np.mean(list(miss.values())))
    line_miss = A.backtest(yr, 256000, "y", cfg["lr_fix"], "line")
    out["heldback_line"] = float(np.mean(np.abs(list(line_miss.values()))))
    # the learning rate for the 1,024-wide configuration
    expo, lr1024, opt = A.lr_rule(yr)
    if cfg["lr1024"] == "fit":
        out["rate"] = lr1024
    elif cfg["lr1024"] == "last":
        out["rate"] = A.TUNED_LR[512]
    else:
        out["rate"] = A.TABLE_LR[256] / 4.0
    out["rate_exponent"] = expo
    # each shortlisted configuration's expected benchmark loss
    fc = A.forecast(yr, shortlist, "y", cfg["lr_fix"], cfg["beyond"], cfg["form"], cfg["width_rule"], rm=rm)
    out["expected"] = {k: v["expected"] for k, v in fc["forecast"].items()}
    # the configuration to name and its margin over the next best
    order = sorted(out["expected"], key=lambda k: out["expected"][k])
    out["call"] = dict(pick=order[0], margin=out["expected"][order[1]] - out["expected"][order[0]], order=order)
    # the range round the named configuration
    pick = order[0]
    s_run = within_cell_sd(yr)
    s_fore = math.sqrt(float(np.mean(np.array(list(miss.values())) ** 2)))
    s_cal = cal["sd"]
    if cfg["spread"] == "three":
        sd = math.sqrt(s_run ** 2 + s_fore ** 2 + s_cal ** 2)
        parts = dict(run=s_run, forecast=s_fore, yardstick=s_cal)
    elif cfg["spread"] == "residual":
        sd, parts = rm["resid_sd"], {}
    elif cfg["spread"] == "seed":
        sd, parts = s_run, dict(run=s_run)
    else:
        sd = None
    out["range"] = None if sd is None else dict(config=pick, low=out["expected"][pick] - Z80 * sd,
                                             high=out["expected"][pick] + Z80 * sd, sd=sd, parts=parts)
    out["_cal"] = cal
    out["_levels"] = rm["levels"]
    out["_form"] = fc["form"]
    out["_width"] = fc["width"]
    out["_lr_opt"] = opt
    out["_miss"] = {_miss_key(k): v for k, v in miss.items()}
    return out


POOLED_FORMS = ("line", "quadratic", "floor")


def _lr_opt_fn(yr):
    expo, lr1024, opt = A.lr_rule(yr)
    x1 = np.log2(np.array(sorted(opt), float)); y1 = np.log10(np.array([opt[w] for w in sorted(opt)]))
    sl, ic = np.polyfit(x1, y1, 1)
    return lambda w: ic + sl * math.log2(w)


def pooled_fit(yr, form="floor", one_vendor=False):
    """One regression over every finished run, the scaling-law fit a careful analyst runs first: a curve in total
    examples (a straight line in log examples, a quadratic in log examples, or a power law with a floor), a term in
    log width, each route's share of the training set, and a learning-rate term (squared distance in log10 from the
    width's own best rate). `one_vendor` reads the two vendor routes as one share."""
    lropt = _lr_opt_fn(yr)
    y = np.array([r["y"] for r in yr])

    def cols(width, n, sB, sC, lr, b=None):
        d = 0.0 if lr is None else (math.log10(lr) - lropt(width)) ** 2
        shares = [sB + sC] if one_vendor else [sB, sC]
        base = [1.0, math.log2(width / 128.0)] + shares + [d]
        if form == "line":
            return base + [math.log2(n / 1e5)]
        if form == "quadratic":
            return base + [math.log2(n / 1e5), math.log2(n / 1e5) ** 2]
        return base + [(n / 1e5) ** (-b)]

    def design(b=None):
        return np.array([cols(r["width"], A.total(r), r["nB"] / A.total(r), r["nC"] / A.total(r), r["lr"], b) for r in yr])

    if form == "floor":
        best = None
        for b in np.linspace(0.02, 1.2, 119):
            X = design(b)
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            sse = float(((y - X @ beta) ** 2).sum())
            if beta[-1] > 0 and (best is None or sse < best[0]):
                best = (sse, float(b), beta)
        sse, b, beta = best
    else:
        b = None
        X = design()
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        sse = float(((y - X @ beta) ** 2).sum())
    k = len(beta) + (1 if form == "floor" else 0)

    def predict(width, n, sB, sC, lr=None):
        return float(np.dot(cols(width, n, sB, sC, lr, b), beta))
    kB = float(beta[2]); kC = float(beta[2] if one_vendor else beta[3])
    return dict(predict=predict, kB=kB, kC=kC, resid_sd=math.sqrt(sse / (len(y) - k)), width=float(beta[1]), b=b)


def pooled_holdout(yr, form="floor", one_vendor=False, hold_above=256000):
    """The pooled fit made without the runs above `hold_above` examples, and its misses on those cells."""
    kept = [r for r in yr if not (r["stage"] == "vend" and A.total(r) > hold_above)]
    fit = pooled_fit(kept, form, one_vendor)
    held = {}
    for r in yr:
        if r["stage"] == "vend" and A.total(r) > hold_above:
            held.setdefault((r["width"], r["nA"], r["nB"], r["nC"], r["lr"]), []).append(r["y"])
    miss = {}
    for (w, a, b, c, lr), v in sorted(held.items()):
        n = a + b + c
        miss[(w, a, b, c)] = fit["predict"](w, n, b / float(n), c / float(n), lr) - float(np.mean(v))
    return miss


def compute_pooled(rows, facts, cfg, shortlist=None):
    """The nine results from the pooled scaling-law fit. cfg["pooled"] names the form, or "best" to take the form
    with the smallest held-out miss (the careful pass: it back-tests, and keeps the best of what it tried)."""
    shortlist = shortlist or S.SHORTLIST
    yr, cal = scored_rows(rows, cfg)
    one = cfg.get("one_vendor", False)
    form = cfg.get("pooled", "best")
    misses = {f: pooled_holdout(yr, f, one) for f in (POOLED_FORMS if form == "best" else (form,))}
    mae = {f: float(np.mean(np.abs(list(m.values())))) for f, m in misses.items()}
    form = min(mae, key=lambda f: mae[f])
    fit = pooled_fit(yr, form, one)
    out = {}
    out["counts"] = dict(complete=facts["complete"], final_scores=facts["sub_final"])
    out["trial"] = {k: A.cell(yr, "y", stage="vend", width=128, nA=v[0], nB=v[1], nC=v[2])[0] for k, v in BIG_CELLS.items()}
    out["costs"] = dict(map_per10=fit["kC"] / 10.0, ctr_per10=fit["kB"] / 10.0)
    out["level"] = fit["predict"](128, 512000, 0.0, 0.0, A.TUNED_LR[128])
    miss = misses[form]
    out["heldback"] = mae[form]
    out["heldback_signed"] = float(np.mean(list(miss.values())))
    out["heldback_line"] = mae.get("line", mae[form])
    expo, lr1024, opt = A.lr_rule(yr)
    out["rate"] = lr1024
    out["rate_exponent"] = expo
    out["expected"] = {}
    for c in shortlist:
        n = c["nA"] + c["nB"] + c["nC"]
        out["expected"][c["key"]] = fit["predict"](c["width"], n, c["nB"] / float(n), c["nC"] / float(n), None)
    order = sorted(out["expected"], key=lambda k: out["expected"][k])
    out["call"] = dict(pick=order[0], margin=out["expected"][order[1]] - out["expected"][order[0]], order=order)
    sd = fit["resid_sd"]
    out["range"] = dict(config=order[0], low=out["expected"][order[0]] - Z80 * sd, high=out["expected"][order[0]] + Z80 * sd, sd=sd,
                     parts={})
    out["_form"] = form
    out["_mae"] = mae
    out["_cal"] = cal
    out["_lr_opt"] = opt
    out["_width_term"] = fit["width"]
    out["_miss"] = {_miss_key(k): v for k, v in miss.items()}
    return out


def scored_only(rows, facts):
    """Only the runs the benchmark scored: the vendor-label configurations cannot be forecast at all, and the widest
    expert-label configuration is the one the scored runs reach."""
    kept = [r for r in rows if r.get("bench") is not None]
    yr = [dict(r, y=r["bench"], yhat=r["bench"]) for r in kept]
    lv = lambda w, lr: A.expert_level(yr, w, 128000, lr)
    a = lv(512, A.TUNED_LR[512]) - (lv(256, A.TUNED_LR[256]) - lv(512, A.TUNED_LR[512]))
    return dict(expected=dict(A=a), call=dict(pick="A", margin=None, order=["A"]))


def run_pass(rows, facts, cfg):
    return compute_pooled(rows, facts, cfg) if "pooled" in cfg else compute(rows, facts, cfg)


# The six results the prompt asks for, and each one's band: what every member of the defensible family lands inside
# (rivals(), which holds the determinism judge's own readings: a level of its own at every total, every run on the
# carried loss, the continuation past the largest runs anywhere between the last gain undiminished and none). The
# hurried figures sit outside by the margins checks.py asserts. counts, heldback and rate are working the six rest
# on: computed, shown in the workbook, and not graded on their own.
GRADED = ["trial", "costs", "level", "expected", "range", "call"]
WORKING = ["counts", "heldback", "rate"]
BANDS = {
    "trial": {"exp128k_map384k": (0.680, 0.690)},
    "costs": {"map_per10": (0.0095, 0.0125), "ctr_per10": (0.0005, 0.0032)},
    "level": (0.595, 0.613),
    "rate": (1.7e-4, 3.6e-4),
    "expected": {"A": (0.650, 0.720), "B": (0.615, 0.650), "C": (0.648, 0.689), "D": (0.660, 0.697)},
    "range": {"low": (0.580, 0.640), "high": (0.625, 0.690), "half": (0.010, 0.040)},
}


def half_width(r):
    return (r["high"] - r["low"]) / 2.0


def cells(res, key):
    """One True or False per graded cell of a result."""
    def inside(v, b):
        return v is not None and b[0] <= v <= b[1]
    r = res.get(key)
    if key == "counts":
        return [r["complete"] == 129, r["final_scores"] == 28]
    if key == "call":
        return [r["pick"] == "B"]
    if key == "range":
        if r is None:
            return [False, False, False]
        half = inside(half_width(r), BANDS["range"]["half"])
        if r["config"] != "B":                      # a range drawn round another configuration is not this result
            return [False, False, half]
        return [inside(r["low"], BANDS["range"]["low"]), inside(r["high"], BANDS["range"]["high"]), half]
    if key in ("level", "rate"):
        return [inside(r, BANDS[key])]
    if key == "heldback":
        return [r is not None]
    return [inside(r.get(k), b) for k, b in BANDS[key].items()]


def grade(res, key):
    """Right, Partly or Missed for one result of a pass against the golden's bands (the effort.py rule)."""
    ok = cells(res, key)
    share = sum(ok) / float(len(ok))
    return "right" if share >= 0.999 else ("partly" if share >= 0.5 else "missed")
