"""The analysis: from the pilot's runs to each shortlisted configuration's loss on the verified benchmark.

Every function works on plain rows, one per finished run:
    name, stage, width, lr, seed, nA, nB, nC, dev (the logged development loss of the final checkpoint),
    devE (its mean loss on the expert-labelled development items), bench (its benchmark score if the final
    checkpoint was submitted, else None)
so the same code serves the golden (rows read back from the shipped pack), its rivals and the hurried passes.
"""
import math

import numpy as np

TABLE_LR = {64: 2e-3, 128: 1e-3, 256: 5e-4}
TUNED_LR = {64: 8e-3, 128: 2e-3, 256: 1e-3, 512: 5e-4}
LADDER = (8000, 16000, 32000, 64000, 128000)
Z80 = 1.2816


def _eq(a, b):
    return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))


def total(r):
    return r["nA"] + r["nB"] + r["nC"]


# ------------------------------------------------------------------------------------------------ the yardstick
def calibrate(rows, kind="linear"):
    """Benchmark score against the loss on the expert-labelled development items, over the final checkpoints the
    benchmark scored. Returns (intercept, slope, residual sd, n)."""
    cal = [r for r in rows if r.get("bench") is not None]
    x = np.array([r["devE"] for r in cal]); y = np.array([r["bench"] for r in cal])
    if kind == "linear":
        b, a = np.polyfit(x, y, 1)
        dof = 2
    elif kind == "offset":
        b, a, dof = 1.0, float((y - x).mean()), 1
    else:                                        # the expert items read as they are
        b, a, dof = 1.0, 0.0, 0
    res = y - (a + b * x)
    sd = float(np.sqrt((res ** 2).sum() / max(1, len(cal) - dof)))
    return float(a), float(b), sd, len(cal)


def with_yardstick(rows, kind="linear", prefer_bench=True):
    """Each run's benchmark-equivalent loss: its own benchmark score where it has one, else the calibrated loss on
    the expert-labelled development items."""
    a, b, sd, n = calibrate(rows, kind)
    out = []
    for r in rows:
        q = dict(r)
        q["yhat"] = a + b * r["devE"]
        q["y"] = r["bench"] if (prefer_bench and r.get("bench") is not None) else q["yhat"]
        out.append(q)
    return out, dict(a=a, b=b, sd=sd, n=n)


def cell(rows, key="y", **want):
    """Mean of `key` over the runs matching every given field (lr and totals compared with a tolerance)."""
    vals = []
    for r in rows:
        ok = True
        for k, v in want.items():
            rv = total(r) if k == "total" else r[k]
            if isinstance(v, float):
                ok = ok and _eq(rv, v)
            else:
                ok = ok and rv == v
        if ok:
            vals.append(r[key])
    return (float(np.mean(vals)), len(vals)) if vals else (None, 0)


# -------------------------------------------------------------------------------------------- learning rate, width
def lr_optimum(rows, width, nA=32000, key="y"):
    """A parabola in log10 learning rate through the cell means of one width on expert labels: the learning rate
    at its minimum, the loss there, and the cells used."""
    pts = {}
    for r in rows:
        if r["width"] == width and r["nA"] == nA and r["nB"] == 0 and r["nC"] == 0:
            pts.setdefault(r["lr"], []).append(r[key])
    lrs = sorted(pts)
    x = np.log10(np.array(lrs)); y = np.array([np.mean(pts[l]) for l in lrs])
    if len(lrs) >= 4:
        # the three or four cells around the lowest: the wings are not a parabola
        i = int(np.argmin(y))
        lo, hi = max(0, i - 1), min(len(lrs), i + 2)
        if hi - lo < 3:
            lo, hi = (0, 3) if i == 0 else (len(lrs) - 3, len(lrs))
        x, y = x[lo:hi], y[lo:hi]
    c2, c1, c0 = np.polyfit(x, y, 2)
    if c2 <= 0:
        i = int(np.argmin(y))
        return float(10 ** x[i]), float(y[i]), lrs
    xs = -c1 / (2 * c2)
    xs = min(max(xs, x.min()), x.max())
    return float(10 ** xs), float(c0 + c1 * xs + c2 * xs * xs), lrs


def lr_rule(rows, widths=(64, 128, 256, 512), key="y"):
    """The optimum learning rate against width as a power law; returns (exponent, the rate at 1,024, the optima)."""
    opt = {w: lr_optimum(rows, w, key=key)[0] for w in widths}
    x = np.log2(np.array(sorted(opt), float)); y = np.log10(np.array([opt[w] for w in sorted(opt)]))
    slope, icpt = np.polyfit(x, y, 1)
    return float(slope / math.log10(2)), float(10 ** (icpt + slope * 10.0)), opt


def expert_level(rows, width, nA, lr, key="y"):
    return cell(rows, key, width=width, nA=nA, nB=0, nC=0, lr=float(lr))[0]


def table_lr_cost(rows, width, key="y"):
    """What the ladder's tabled learning rate cost a width, where the same data was also run at the tuned rate."""
    out = {}
    for nA in (32000, 128000):
        a = expert_level(rows, width, nA, TABLE_LR[width], key)
        b = expert_level(rows, width, nA, TUNED_LR[width], key)
        if a is not None and b is not None:
            out[nA] = a - b
    return out


def expert_curve(rows, width, key="y", lr_fix="matched"):
    """The expert-label ladder of one width put on its tuned learning rate: {examples: loss}. The ladder ran at the
    tabled rate; its gap to the tuned rate is measured at 32,000 and 128,000 examples and carried along log
    examples between them."""
    if width not in TABLE_LR:
        return {nA: expert_level(rows, width, nA, TUNED_LR[width], key) for nA in (32000, 128000)
                if expert_level(rows, width, nA, TUNED_LR[width], key) is not None}
    cost = table_lr_cost(rows, width, key) if lr_fix == "matched" else {32000: 0.0, 128000: 0.0}
    out = {}
    for nA in LADDER:
        lad = expert_level(rows, width, nA, TABLE_LR[width], key)
        if lad is None:
            continue
        if len(cost) == 2:
            t = (math.log2(nA) - 15.0) / 2.0                      # 0 at 32,768, 1 at 131,072, near enough
            t = min(1.0, max(0.0, (math.log2(nA) - math.log2(32000)) / 2.0))
            c = cost[32000] + t * (cost[128000] - cost[32000])
        else:
            c = list(cost.values())[0] if cost else 0.0
        out[nA] = lad - c
    for nA in (32000, 128000):
        tuned = expert_level(rows, width, nA, TUNED_LR[width], key)
        if tuned is not None:
            out[nA] = tuned
    return out


# ------------------------------------------------------------------------------- the label routes and more examples
def vendor_cells(rows, width, key="y"):
    cells = {}
    for r in rows:
        if r["stage"] == "vend" and r["width"] == width:
            cells.setdefault((r["nA"], r["nB"], r["nC"]), []).append(r[key])
    return {k: (float(np.mean(v)), len(v)) for k, v in cells.items()}


def route_model(rows, width=128, key="y", lr_fix="matched", hold_out_above=None, form="levels"):
    """The vendor trials of one width read against expert labels at the same examples and learning rate.

    Each cell's loss = the expert-equivalent level at its total examples + a cost per unit share for each route.
    The level is known up to 128,000 examples (the expert ladder at the tuned rate) and free at each total beyond.
    Returns the two costs and the expert-equivalent levels at every total."""
    f = expert_curve(rows, width, key, lr_fix)
    cells = vendor_cells(rows, width, key)
    if hold_out_above:
        cells = {k: v for k, v in cells.items() if sum(k) <= hold_out_above}
    totals_free = sorted({sum(k) for k in cells if sum(k) not in f})
    cols = ["kB", "kC"] + ["g%d" % t for t in totals_free]
    A, y, w = [], [], []
    for (a, b, c), (m, n) in sorted(cells.items()):
        t = a + b + c
        row = [b / float(t), c / float(t)] + [1.0 if t == tf else 0.0 for tf in totals_free]
        A.append(row); y.append(m - (f[t] if t in f else 0.0)); w.append(math.sqrt(n))
    A = np.array(A); y = np.array(y); w = np.array(w)
    sol, *_ = np.linalg.lstsq(A * w[:, None], y * w, rcond=None)
    res = y - A @ sol
    out = dict(zip(cols, [float(s) for s in sol]))
    levels = dict(f)
    for tf in totals_free:
        levels[tf] = out["g%d" % tf]
    return dict(kB=out["kB"], kC=out["kC"], levels=levels, resid_sd=float(np.sqrt((res ** 2).mean())), cells=cells)


def fit_floor(levels, lo=32000):
    """Loss = floor + a * examples^-b through the expert-equivalent levels from `lo` examples up (three parameters,
    a grid over the floor and least squares for the rest)."""
    xs = np.array(sorted(t for t in levels if t >= lo), float)
    ys = np.array([levels[int(t)] for t in xs])
    best = None
    for E in np.linspace(0.30, ys.min() - 0.004, 400):
        z = np.log(ys - E)
        slope, icpt = np.polyfit(np.log(xs), z, 1)
        pred = E + np.exp(icpt) * xs ** slope
        sse = float(((pred - ys) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, float(E), float(np.exp(icpt)), float(-slope))
    _, E, a, b = best
    return lambda n: E + a * n ** (-b), dict(floor=E, a=a, b=b)


def fit_quadratic(levels, lo=32000):
    xs = np.array(sorted(t for t in levels if t >= lo), float)
    ys = np.array([levels[int(t)] for t in xs])
    c = np.polyfit(np.log2(xs), ys, 2)
    return (lambda n: float(np.polyval(c, math.log2(n)))), dict(c=[float(v) for v in c])


def fit_fading_slope(levels):
    """Carry the last doubling's gain on, shrinking by the ratio the last two doublings showed."""
    xs = sorted(levels)
    ys = [levels[t] for t in xs]
    d1 = ys[-1] - ys[-2]; d0 = ys[-2] - ys[-3]
    ratio = min(0.95, max(0.3, d1 / d0)) if d0 < 0 else 0.6
    n0, y0 = xs[-1], ys[-1]

    def f(n):
        k = math.log2(n / float(n0))
        if k <= 0:
            return float(np.interp(math.log2(n), [math.log2(t) for t in xs], ys))
        whole, frac = int(k), k - int(k)
        y, step = y0, d1
        for _ in range(whole):
            step *= ratio; y += step
        return y + frac * step * ratio
    return f, dict(ratio=ratio)


def fit_line(levels, hi=128000):
    """One straight line in log examples through the expert ladder (what the pilot's expert runs alone show)."""
    xs = np.array(sorted(t for t in levels if t <= hi), float)
    ys = np.array([levels[int(t)] for t in xs])
    slope, icpt = np.polyfit(np.log2(xs), ys, 1)
    return (lambda n: float(icpt + slope * math.log2(n))), dict(per_doubling=float(slope))


FORMS = {"floor": fit_floor, "quadratic": fit_quadratic, "fading": fit_fading_slope}


def width_gaps(rows, key="y", lr_fix="matched", rm128=None, rm256=None):
    """How much lower a 256-wide model sits than a 128-wide one at each total (tuned rates, expert-equivalent),
    and a 512-wide one than a 256-wide one where both were run."""
    rm128 = rm128 or route_model(rows, 128, key, lr_fix)
    rm256 = rm256 or route_model_fixed_costs(rows, 256, rm128, key)
    g = {t: rm128["levels"][t] - rm256[t] for t in sorted(rm256) if t in rm128["levels"]}
    g512 = {}
    for nA in (32000, 128000):
        a = expert_level(rows, 256, nA, TUNED_LR[256], key); b = expert_level(rows, 512, nA, TUNED_LR[512], key)
        if a is not None and b is not None:
            g512[nA] = a - b
    return g, g512


def route_model_fixed_costs(rows, width, rm, key="y"):
    """Expert-equivalent levels of another width: its expert runs at the tuned rate, and its vendor trials with the
    routes' costs taken off."""
    out = {}
    for nA in (32000, 128000):
        v = expert_level(rows, width, nA, TUNED_LR[width], key)
        if v is not None:
            out[nA] = v
    per = {}
    for (a, b, c), (m, n) in vendor_cells(rows, width, key).items():
        t = a + b + c
        per.setdefault(t, []).append((m - rm["kB"] * b / t - rm["kC"] * c / t, n))
    for t, vs in per.items():
        out[t] = float(sum(v * n for v, n in vs) / sum(n for _, n in vs))
    return out


# ------------------------------------------------------------------------------------------------- the forecast
def forecast(rows, shortlist, key="y", lr_fix="matched", form="floor", width_rule="grow", hold_out_above=None,
             kind_done=None):
    """Each shortlisted configuration's expected benchmark loss, and everything it rests on."""
    rm = route_model(rows, 128, key, lr_fix, hold_out_above)
    f128, fpar = FORMS[form](rm["levels"])
    lv256 = route_model_fixed_costs(rows if not hold_out_above else [r for r in rows if total(r) <= hold_out_above],
                                    256, rm, key)
    gaps = {t: rm["levels"][t] - lv256[t] for t in lv256 if t in rm["levels"]}
    ts = sorted(gaps)
    gap512 = {}
    for nA in (32000, 128000):
        a = expert_level(rows, 256, nA, TUNED_LR[256], key); b = expert_level(rows, 512, nA, TUNED_LR[512], key)
        if a is not None and b is not None:
            gap512[nA] = a - b

    def gap256(n):
        if width_rule == "flat":
            return float(np.mean([gaps[t] for t in ts]))
        # the gap as the pilot shows it at the largest totals it reached, held there beyond them
        big = [gaps[t] for t in ts if t >= 128000]
        if n >= 128000:
            return float(np.mean(big))
        return float(np.interp(math.log2(n), [math.log2(t) for t in ts], [gaps[t] for t in ts]))

    def level(width, n):
        if width == 128:
            return f128(n)
        if width == 256:
            return f128(n) - gap256(n)
        if width == 512:
            return f128(n) - gap256(n) - float(np.mean(list(gap512.values())))
        if width == 1024:
            # one more doubling of width at the gain the last doubling showed on the same examples
            step = gap512.get(128000, float(np.mean(list(gap512.values()))))
            return f128(n) - gap256(n) - float(np.mean(list(gap512.values()))) - step
        raise ValueError(width)

    out = {}
    for c in shortlist:
        n = c["nA"] + c["nB"] + c["nC"]
        base = level(c["width"], n)
        out[c["key"]] = dict(expected=base + rm["kB"] * c["nB"] / n + rm["kC"] * c["nC"] / n, level=base, total=n,
                             cost=rm["kB"] * c["nB"] / n + rm["kC"] * c["nC"] / n)
    return dict(forecast=out, routes=rm, form=fpar, gaps256=gaps, gap512=gap512, f128=f128, level=level)


def backtest(rows, shortlist, hold_above=256000, key="y", lr_fix="matched", form="floor"):
    """Hold out every pilot run above `hold_above` examples, forecast them from the rest, and return the misses
    (forecast minus what the held-out cells showed) cell by cell."""
    held = {}
    for r in rows:
        if r["stage"] == "vend" and total(r) > hold_above:
            held.setdefault((r["width"], r["nA"], r["nB"], r["nC"]), []).append(r[key])
    kept = [r for r in rows if not (r["stage"] == "vend" and total(r) > hold_above)]
    rm = route_model(kept, 128, key, lr_fix)
    f128, _ = FORMS[form](rm["levels"]) if form != "line" else fit_line(rm["levels"])
    lv256 = route_model_fixed_costs(kept, 256, rm, key)
    gaps = [rm["levels"][t] - lv256[t] for t in lv256 if t in rm["levels"] and t >= 128000]
    gap = float(np.mean(gaps)) if gaps else 0.0
    miss = {}
    for (w, a, b, c), v in sorted(held.items()):
        n = a + b + c
        pred = f128(n) - (gap if w == 256 else 0.0) + rm["kB"] * b / n + rm["kC"] * c / n
        miss[(w, a, b, c)] = pred - float(np.mean(v))
    return miss
