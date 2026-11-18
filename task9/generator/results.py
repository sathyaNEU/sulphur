"""Every owed figure, computed from the shipped pack: the golden route (the core's estimators on the loaded files),
the battery of conventions (the core's 125 and the readings the records add beside it), the lattice of shortcuts, the
direct and the rigorous standard routes, April's check, the forcing rows, the rivals a reviewer would try, the rubric
the core prices and the effort record."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))
import core as C  # noqa: E402
import corelib  # noqa: E402
import effort as EF  # noqa: E402
import load as L  # noqa: E402
import world as WL  # noqa: E402

G, LINE = C.GROUPS, C.LINE
MONTHS = [n for n, _, _ in C.Q3_MONTHS]
KEYS = C.lat_keys()
REFLEX = "S1+S2+S3"
ALONE = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
ALL, LISTED = "all groups", "listed groups"
LOCAL_DAYS = "the quarter cut on Utrecht's calendar days"
STUMP_NAME = {
    "S1": "an ablation test's effect is the group's worth on the share of the held slice's result page views built at "
          "origin, taken by market, device and day from the edge cache record",
    "S2": "the sessions served a group's default are replayed source by source from the gap, batch, lag and scoring "
          "logs with each value's validity, weighted by the traffic each source carries, net of what normal service "
          "leaves at the default",
    "S3": "the cost through each component that also reads the group is built from the component's own holdout test and "
          "its own render record, and added",
}
ROUTE_NAME = {
    "S1": "the ablation effects as measured",
    "S2": "the status record's unhealthy share as the share of sessions served the default",
    "S3": "each group priced through the ranking model alone",
    "S1+S2": "the ablation effects as measured, on the status record's unhealthy share",
    "S1+S3": "the ablation effects as measured, each group priced through the ranking model alone",
    "S2+S3": "the status record's unhealthy share, each group priced through the ranking model alone",
    "S1+S2+S3": "the pooled ablation effects on the traffic-weighted status record",
}
PREC = {"S1": ["L18", "L28"], "S2": ["N21", "L26"], "S3": ["L16", "N27"]}
WORD = {1: "listed", 0: "not listed"}


# ---------------------------------------------------------------- helpers
def cells(v):
    out = {j: float(v["loss"][j]) for j in G}
    out.update({n: float(v["month"][n]) for n in MONTHS})
    out[ALL], out[LISTED] = float(v["total"]), float(v["tier"])
    return out


def call_of(loss):
    return ["%s %s" % (j, WORD[int(loss[j] >= LINE)]) for j in G]


def listed(loss):
    return [j for j in G if loss[j] >= LINE]


def band_of(golden, family, step):
    """The family's range and a quarter of its width each side, rounded outward to the stated precision."""
    lo, hi = min(family + [golden]), max(family + [golden])
    lo, hi = lo - corelib.BAND_ROOM * (hi - lo), hi + corelib.BAND_ROOM * (hi - lo)
    return [round(float(np.floor(lo / step + 1e-9) * step), 6), round(float(np.ceil(hi / step - 1e-9) * step), 6)]


def hourly_cost(W, o=None):
    """Each group's cost by market, device and hour, in points (the golden's arithmetic, kept apart)."""
    o = o or {}
    exp = C.exposure(W, o)
    eff, rd = C.effects(W, o, exp), C.readers(W, o, exp)
    out = {}
    for j in G:
        out[j] = eff[j][:, None] * exp[j]["exc"]
        if j in rd:
            out[j] = out[j] + rd[j]["per"][:, None] * rd[j]["share"]
    return out


def group_month(W, o=None):
    """Each group's cost in each month of the quarter and over the quarter."""
    hc = hourly_cost(W, o)
    out = {}
    for j in G:
        tot = hc[j]
        out[j] = {n: float(np.sum(C.q3w(W, lo, hi) * tot[:, lo * 24:hi * 24])) for n, lo, hi in C.Q3_MONTHS}
        out[j]["quarter"] = float(np.sum(C.q3w(W) * tot[:, C.Q3[0] * 24:C.Q3[1] * 24]))
    return out


def direct_cells(W):
    """The direct route's cells: each job's own unhealthy figure (each shard counted once) times the group's latest
    ablation test as its record reports it."""
    Lg = W["logs"]
    raw = {"stock": Lg["stock"]["unavail"].mean(axis=0), "price": Lg["price"]["st_src"].mean(axis=0),
           "trend": Lg["trend"]["lag_s"].mean(axis=0)}
    out = {j: 0.0 for j in G}
    mon = {n: 0.0 for n in MONTHS}
    for j in G:
        t = [t for t in W["tests"] if t["group"] == j][-1]
        itt = 100.0 * (t["oc"].sum() / t["nc"].sum() - t["oh"].sum() / t["nh"].sum())
        s = np.tile(raw[j], (12, 1)) if j in raw else W["S"][j]
        out[j] = float(itt * np.sum(C.q3w(W) * s[:, C.Q3[0] * 24:C.Q3[1] * 24]))
        for n, lo, hi in C.Q3_MONTHS:
            mon[n] += float(itt * np.sum(C.q3w(W, lo, hi) * s[:, lo * 24:hi * 24]))
    c = dict(out)
    c.update(mon)
    c[ALL] = float(sum(out.values()))
    c[LISTED] = float(sum(x for x in out.values() if x >= LINE))
    return c


def local_days(W):
    """The same records with the quarter cut on Utrecht's calendar days (two hours ahead of UTC all quarter)."""
    roll = lambda a: np.roll(a, 2, axis=-1)   # noqa: E731
    Lg = W["logs"]
    logs = dict(Lg, stock=dict(Lg["stock"], default_c=roll(Lg["stock"]["default_c"]), unavail=roll(Lg["stock"]["unavail"])),
                price=dict(Lg["price"], df_src=roll(Lg["price"]["df_src"]), st_src=roll(Lg["price"]["st_src"])),
                trend=dict(Lg["trend"], lag_d=roll(Lg["trend"]["lag_d"]), lag_s=roll(Lg["trend"]["lag_s"])))
    return dict(W, sess=roll(W["sess"]), S={j: roll(v) for j, v in W["S"].items()}, logs=logs,
                render={j: {k: roll(v) for k, v in r.items()} for j, r in W["render"].items()})


def reader_rate_scale(W):
    """The component's cost read the other consistent way: its loss per session of its own test (eligible or not), so
    the quarter's eligible share is taken to be the test's, as a scale on the golden's per-eligible-session figure."""
    out = {}
    for j in C.READERS:
        t, r = W["rtest"][j], W["render"][j]
        es_test = t["elig_c"] / t["nc"]
        hq = slice(C.Q3[0] * 24, C.Q3[1] * 24)
        es_rec = r["eligible"][:, hq].sum(axis=1) / W["sess"][:, hq].sum(axis=1)
        out[j] = es_test / es_rec
    return out


def effect_by_test_scale(W):
    """Each group's full effect as the mean of its tests' own ratios (each test's measured effect over its own share
    built at origin, by device), in place of one ratio over all its tests, as a scale on the golden's effect."""
    exp = C.exposure(W, {})
    base = C.effects(W, {}, exp)
    out = {}
    for j in G:
        ratios, wts = [], []
        for t in W["tests"]:
            if t["group"] != j:
                continue
            itt = 100.0 * (t["oc"] / np.maximum(t["nc"], 1) - t["oh"] / np.maximum(t["nh"], 1))
            n = t["nh"].astype(float)
            fresh = W["u"][:, t["d0"]:t["d1"]] if C.G[j]["pre"] else np.ones_like(itt)
            hs = slice(t["d0"] * 24, t["d1"] * 24)
            sw = W["sess"][:, hs].reshape(12, -1, 24)
            dflt = (exp[j]["tot"][:, hs].reshape(12, -1, 24) * sw).sum(axis=2) / np.maximum(sw.sum(axis=2), 1)
            fresh = fresh * (1 - np.clip(dflt, 0, 0.9))
            num, den = (itt * n).sum(axis=1), (fresh * n).sum(axis=1)
            ratios.append(np.array([num[d::2].sum() / den[d::2].sum() for m, d in C.CELLS]))
            wts.append(np.array([n.sum(axis=1)[d::2].sum() for m, d in C.CELLS]))
        ratios, wts = np.array(ratios), np.array(wts)
        out[j] = (ratios * wts).sum(axis=0) / wts.sum(axis=0) / base[j]
    return out


def reader_by_cell_scale(W):
    """Each component's loss per eligible session market by market and device by device, as a scale on the golden's
    (which pools the markets within a device)."""
    base = C.readers(W, {}, C.exposure(W, {}))
    out = {}
    for j in C.READERS:
        t = W["rtest"][j]
        d = 100.0 * (t["oc"] / t["nc"] - t["oh"] / t["nh"])
        out[j] = d / (t["elig_c"] / t["nc"]) / base[j]["per"]
    return out


def daily_grain(W):
    """The same records with every default share taken day by day before it meets the sessions: the request-time
    groups by the day's requests, the replayed groups by the share of the day's hours."""
    sd = W["sess"].reshape(12, C.DAYS, 24)
    by_req = lambda a: np.repeat((a.reshape(12, C.DAYS, 24) * sd).sum(axis=2) / sd.sum(axis=2), 24, axis=1)   # noqa: E731
    by_time = lambda a: np.repeat(a.reshape(a.shape[0], C.DAYS, 24).mean(axis=2), 24, axis=1)   # noqa: E731
    Lg = W["logs"]
    S = dict(W["S"], promise=by_req(W["S"]["promise"]), history=by_req(W["S"]["history"]), match=by_time(W["S"]["match"]))
    logs = dict(Lg, stock=dict(Lg["stock"], default_c=by_time(Lg["stock"]["default_c"])),
                price=dict(Lg["price"], df_src=by_time(Lg["price"]["df_src"])),
                trend=dict(Lg["trend"], lag_d=by_time(Lg["trend"]["lag_d"])))
    return dict(W, S=S, logs=logs)


def april(W, o, window=None):
    """April's missed batches as a route calls them and as the record shows them, on the fourteen business days the
    expired hours touch or on the given days."""
    if window is not None:
        win = np.zeros(C.H, bool)
        for dd in window:
            win[dd * 24:(dd + 1) * 24] = True
        W = dict(W, split=dict(W["split"], window=win))
    return C.view(W, o)["split"], C.split_measured(W)


# ---------------------------------------------------------------- the run
def test_rows(W, j, exp):
    """Each completed test of a group, in date order: its full effect at the quarter's device mix (the reported effect
    times the held sessions over the share built at origin times one less the default share times the held sessions,
    by device) and the binomial standard error of its two arms' conversion carried through the same ratio."""
    sw = C.q3w(W).sum(axis=1)
    mix = [float(sw[d::2].sum()) for d in (0, 1)]
    rows = []
    for t in sorted((t for t in W["tests"] if t["group"] == j), key=lambda t: t["d0"]):
        hs = slice(t["d0"] * 24, t["d1"] * 24)
        s_ = W["sess"][:, hs].reshape(12, -1, 24)
        dflt = (exp[j]["tot"][:, hs].reshape(12, -1, 24) * s_).sum(axis=2) / np.maximum(s_.sum(axis=2), 1)
        fresh = W["u"][:, t["d0"]:t["d1"]] if C.G[j]["pre"] else np.ones_like(dflt)
        den = fresh * (1 - np.clip(dflt, 0, 0.9))
        itt = 100.0 * (t["oc"] / np.maximum(t["nc"], 1) - t["oh"] / np.maximum(t["nh"], 1))
        est = var = 0.0
        for d in (0, 1):
            nh, nc, oh, oc = (float(t[k][d::2].sum()) for k in ("nh", "nc", "oh", "oc"))
            dn = float((den[d::2] * t["nh"][d::2]).sum())
            pc, ph = oc / nc, oh / nh
            est += mix[d] * float((itt[d::2] * t["nh"][d::2]).sum()) / dn
            var += (mix[d] * 100.0 * np.sqrt(pc * (1 - pc) / nc + ph * (1 - ph) / nh) * nh / dn) ** 2
        rows.append((t["d0"], est, float(np.sqrt(var))))
    return rows


def pooled(rows):
    """The precision-weighted mean of the tests' effects, its standard error and Cochran's Q about it."""
    wt = np.array([1.0 / r[2] ** 2 for r in rows])
    est = np.array([r[1] for r in rows])
    m = float((est * wt).sum() / wt.sum())
    return m, float(1.0 / np.sqrt(wt.sum())), float(((est - m) ** 2 * wt).sum())


def tests_kept(W, keep):
    """The route with each group's effect taken from a subset of its tests."""
    W2 = dict(W)
    W2["tests"] = [t for t in W["tests"] if keep(t)]
    return W2


def wls_cluster(X, y, wv, grp):
    """Weighted least squares with standard errors clustered on grp (the usual small-sample correction)."""
    Xw, yw = X * np.sqrt(wv)[:, None], y * np.sqrt(wv)
    beta = np.linalg.lstsq(Xw, yw, rcond=None)[0]
    e = y - X @ beta
    bread = np.linalg.pinv(Xw.T @ Xw)
    n, k = X.shape
    ug = np.unique(grp)
    meat = np.zeros((k, k))
    for gg in ug:
        m = grp == gg
        sc = X[m].T @ (wv[m] * e[m])
        meat += np.outer(sc, sc)
    corr = len(ug) / (len(ug) - 1.0) * (n - 1.0) / (n - k)
    return beta, np.sqrt(np.diag(bread @ meat @ bread * corr))


def day_effects(cl, dy):
    """Market and device, weekday and month columns for rows keyed by cell and day."""
    cols = [(cl == c).astype(float) for c in range(12)]
    cols += [(((dy + 3) % 7) == k).astype(float) for k in range(1, 7)]
    mon = np.searchsorted(C.MONTH_START, dy, side="right") - 1
    cols += [(mon == k).astype(float) for k in range(1, 9)]
    return cols


def daily_regression(W, shares):
    """Daily conversion by market and device on the seven groups' shares, with market and device, weekday, month and
    promotion effects, weighted by sessions, standard errors clustered by day. Returns each group's implied cost over
    the quarter, its standard error and the coefficient (points a session at the default)."""
    sd = W["sess"].reshape(12, C.DAYS, 24).sum(axis=2)
    od = W["orders"].reshape(12, C.DAYS, 24).sum(axis=2)
    cl, dy = np.repeat(np.arange(12), C.DAYS), np.tile(np.arange(C.DAYS), 12)
    cols = day_effects(cl, dy)
    cols.append(np.array([W["promo"][m].astype(float) for m, d in C.CELLS]).ravel())
    nb = len(cols)
    for j in G:
        cols.append(((shares[j] * W["sess"]).reshape(12, C.DAYS, 24).sum(axis=2) / sd).ravel())
    beta, se = wls_cluster(np.array(cols).T, (100.0 * od / sd).ravel(), sd.ravel().astype(float), dy)
    w = C.q3w(W)
    hq = slice(C.Q3[0] * 24, C.Q3[1] * 24)
    out = {}
    for i, j in enumerate(G):
        ms = float(np.sum(w * shares[j][:, hq]))
        out[j] = (-beta[nb + i] * ms, se[nb + i] * ms, -beta[nb + i])
    return out


def arm_on_share(W, j, arm, hc):
    """In group j's tests, one arm's daily conversion by market and device, with the other groups' cost that day
    added back, on the group's default share that day (market and device, weekday and month effects, weighted by the
    arm's sessions, clustered by day). Returns the points lost per unit of the share and the standard error."""
    sd = W["sess"].reshape(12, C.DAYS, 24).sum(axis=2)
    share = (C.exposure(W, {})[j]["tot"] * W["sess"]).reshape(12, C.DAYS, 24).sum(axis=2) / sd
    ys, xs, ws, ds, cs = [], [], [], [], []
    for t in W["tests"]:
        if t["group"] != j:
            continue
        n, o = (t["nh"], t["oh"]) if arm == "held" else (t["nc"], t["oc"])
        dd = np.arange(t["d0"], t["d1"])
        ys.append((100.0 * o / np.maximum(n, 1) + sum(hc[k][:, dd] for k in G if k != j)).ravel())
        xs.append(share[:, dd].ravel())
        ws.append(n.ravel().astype(float))
        ds.append(np.tile(dd, 12))
        cs.append(np.repeat(np.arange(12), len(dd)))
    y, x, wv, dy, cl = map(np.concatenate, (ys, xs, ws, ds, cs))
    beta, se = wls_cluster(np.array([x] + day_effects(cl, dy)).T, y, wv, dy)
    return float(-beta[0]), float(se[0])


def run(target):
    W, info = L.load(target)
    WC = C.make_world()
    spec0, x0 = C.build(WC)
    tr = C.truth(WC)
    g = C.view(W)
    bat = [(n, C.view(W, o)) for n, o in C.VARIANTS]
    fam = [v for _, v in bat]
    lat = {k: C.view(W, C.lat_opts(k.split("+"))) for k in KEYS}
    rg = C.view(W, C.RIGOROUS)
    dr = direct_cells(W)
    gm = group_month(W)
    for n in MONTHS:
        assert abs(sum(gm[j][n] for j in G) - g["month"][n]) < 1e-9
    r2, r3, r4 = (lambda v: round(float(v), 2)), (lambda v: round(float(v), 3)), (lambda v: round(float(v), 4))

    # ---- the readings the records add beside the battery (each stays on the golden's list)
    W_first, _ = L.load(target, keep_first_status=True)
    W_abort, _ = L.load(target, keep_aborted=True)
    for t in W_abort["tests"]:                      # the aborted run's two days, laid on a test's fourteen
        short = C.TEST_DAYS - (t["d1"] - t["d0"])
        if short > 0:
            for k in ("nh", "oh", "nc", "oc"):
                t[k] = np.hstack([t[k], np.zeros((12, short))])
            t["d1"] = t["d0"] + C.TEST_DAYS
    side = [(LOCAL_DAYS, C.view(local_days(W))),
            ("the monitor's first load of each hour kept", C.view(W_first)),
            ("the aborted test read with the completed ones", C.view(W_abort)),
            ("a component's loss per session of its own test, eligible or not, at its group's default share",
             C.view(W, {"rd_scale": reader_rate_scale(W)})),
            ("each group's full effect as the mean of its tests' own ratios", C.view(W, {"eff_scale": effect_by_test_scale(W)})),
            ("a component's loss per eligible session market by market", C.view(W, {"rd_scale": reader_by_cell_scale(W)})),
            ("every default share taken day by day before it meets the sessions", C.view(daily_grain(W)))]
    sv = [v for _, v in side]

    # ---- bands as the blocks state them: the battery's range and a quarter of its width, at the stated precision
    gc = cells(g)
    step = {j: 0.001 for j in G}
    step.update({n: 0.01 for n in MONTHS})
    step[ALL] = step[LISTED] = 0.01
    bands = {k: band_of(gc[k], [cells(f)[k] for f in fam] + [cells(v)[k] for v in sv], step[k]) for k in gc}
    c1b = band_of(g["c1"], [f["c1"] for f in fam] + [v["c1"] for v in sv], 0.01)
    c2b = band_of(g["c2"], [f["c2"] for f in fam] + [v["c2"] for v in sv], 0.01)
    c3b = band_of(g["c3"], [f["c3"] for f in fam] + [v["c3"] for v in sv], 0.001)
    # April's record is the mart's, by its business days: the calendar-day reading has no April figure of its own
    c4b = band_of(g["split"], [f["split"] for f in fam] + [v["split"] for n, v in side if n != LOCAL_DAYS], 0.001)

    def figure(fid, block, get, band):
        return dict(id=fid, block=block, golden=get(g), family=[get(f) for f in fam], band=band,
                    lattice={k: get(v) for k, v in lat.items()}, routes={"rigorous": get(rg)})
    figs = [figure("C1 full effect, %s" % C.FRESH_GROUP, "component", lambda v: v["c1"], c1b),
            figure("C2 sessions served the default, %s" % C.STATE_GROUP, "component", lambda v: v["c2"], c2b),
            figure("C3 the reader's loss, %s" % C.READER_GROUP, "component", lambda v: v["c3"], c3b),
            figure("C4 April's missed batches as called", "component", lambda v: v["split"], c4b)]
    for j in G:
        figs.append(dict(id="A1 %s" % j, block="ask", member=j, band=bands[j]))
    for n in MONTHS:
        figs.append(figure("A2 %s" % n, "ask", lambda v, n=n: v["month"][n], bands[n]))
    figs.append(figure("A3 all seven", "ask", lambda v: v["total"], bands[ALL]))
    figs.append(figure("A4 the tier one list", "ask", lambda v: v["tier"], bands[LISTED]))
    members = {j: dict(lines=[LINE], truth=tr[j], golden=g["loss"][j], family=[f["loss"][j] for f in fam],
                       routes={"direct": dr[j], "rigorous": rg["loss"][j]}) for j in G}
    meas = C.split_measured(W)
    ref = dict(slice=spec0["referee"]["slice"], covers_target=False, truth=meas, golden=g["split"],
               rivals=dict([("%s lost" % k, lat[k]["split"]) for k in C.SIDS] +
                           [("every stump lost", lat[REFLEX]["split"]), ("rigorous", rg["split"])]))
    spec = dict(task="task9 architecture 4 (the cut pack)", call="lines", members=members,
                lattice={k: dict(v["loss"]) for k, v in lat.items()}, referee=ref, stumps=spec0["stumps"], figures=figs)
    x = dict(g=g, fam=fam, lat=lat, rg=rg, dr=dr, tr=tr, meas=meas)

    fig = {}
    # ---- the graded figures as the blocks state them
    fig["cost"] = {j: r3(g["loss"][j]) for j in G}
    fig["cost_band"] = {j: bands[j] for j in G}
    fig["month"] = {n: r2(g["month"][n]) for n in MONTHS}
    fig["month_band"] = {n: bands[n] for n in MONTHS}
    fig["all"], fig["all_band"] = r2(g["total"]), bands[ALL]
    fig["listed_cost"], fig["listed_band"] = r2(g["tier"]), bands[LISTED]
    fig["list"] = listed(g["loss"])
    fig["off_list"] = [j for j in G if j not in fig["list"]]
    fig["call"] = call_of(g["loss"])
    fig["margin"] = {j: r3(abs(g["loss"][j] - LINE)) for j in G}
    fig["line"] = LINE
    fig["c1"], fig["c1_band"] = r2(g["c1"]), c1b
    fig["c2"], fig["c2_band"] = r2(g["c2"]), c2b
    fig["c3"], fig["c3_band"] = r3(g["c3"]), c3b
    fig["c4"], fig["c4_band"] = r3(g["split"]), c4b
    fig["asks"] = dict(fig["cost"])
    fig["asks"].update(fig["month"])
    fig["asks"][ALL], fig["asks"][LISTED] = fig["all"], fig["listed_cost"]
    fig["asks_together"] = {k: fig["asks"][k] for k in [ALL] + MONTHS}
    fig["group_month"] = {j: {n: r4(gm[j][n]) for n in MONTHS + ["quarter"]} for j in G}
    fig["csv_rows"] = len(G) * len(MONTHS)

    # ---- the inputs behind them
    P = g["parts"]
    exp = C.exposure(W, {})
    eff = C.effects(W, {}, exp)
    eff_raw = C.effects(W, {"s1": True}, exp)
    rd = C.readers(W, {}, exp)
    sw = C.q3w(W).sum(axis=1)
    dev = lambda a, d: float(np.sum(sw[d::2] * a[d::2]) / sw[d::2].sum())   # noqa: E731
    fig["full_effect"] = {j: r2(P[j]["eff"]) for j in G}
    fig["full_effect_device"] = {j: {"app": r2(dev(eff[j], 0)), "web": r2(dev(eff[j], 1))} for j in G}
    fig["measured_effect"] = {j: r2(float(np.sum(sw * eff_raw[j]))) for j in G}

    def reported(j, ks):
        ts = [t for t in W["tests"] if t["group"] == j and t["k"] in ks]
        return r2(100.0 * (sum(t["oc"].sum() for t in ts) / sum(t["nc"].sum() for t in ts) -
                           sum(t["oh"].sum() for t in ts) / sum(t["nh"].sum() for t in ts)))
    fig["reported_effect_halves"] = {j: dict(jan_may=reported(j, range(0, 5)), jul_sep=reported(j, range(6, 9))) for j in G}
    held = sum(t["nh"].sum() for t in W["tests"]) / sum((t["nh"] + t["nc"]).sum() for t in W["tests"])
    fig["held_share_pct"] = r2(100.0 * float(held))
    fig["served_default_pct"] = {j: r2(P[j]["exposed"]) for j in G}
    w = C.q3w(W)
    hq = slice(C.Q3[0] * 24, C.Q3[1] * 24)
    fig["status_unhealthy_pct"] = {j: r2(100 * float(np.sum(w * W["S"][j][:, hq]))) for j in G}
    fig["rank_cost"] = {j: r3(P[j]["rank"]) for j in G}
    fig["reader_cost"] = {j: r3(P[j]["reader"]) for j in C.READERS}
    fig["reader_per_eligible"] = {j: r2(float(np.sum(sw * rd[j]["per"]))) for j in C.READERS}
    fig["reader_eligible_pct"] = {j: int(round(100 * float(np.sum(sw * rd[j]["elig"])))) for j in C.READERS}
    q2 = slice(C.Q2[0] * 24, C.Q2[1] * 24)
    fig["render_failed_pct"] = {j: dict(q2=r2(100 * float(W["render"][j]["suppressed"][:, q2].sum() / W["render"][j]["eligible"][:, q2].sum())),
                                        q3=r2(100 * float(W["render"][j]["suppressed"][:, hq].sum() / W["render"][j]["eligible"][:, hq].sum())))
                                for j in C.READERS}
    u = W["u"]
    sd = W["sess"].reshape(12, C.DAYS, 24).sum(axis=2)
    ush = lambda d, lo, hi: float(np.sum(u[d::2, lo:hi] * sd[d::2, lo:hi]) / sd[d::2, lo:hi].sum())   # noqa: E731
    fig["fresh_share_pct"] = {dv: dict(before=int(round(100 * ush(d, 0, C.CACHE_CHANGE))),
                                       after=int(round(100 * ush(d, C.CACHE_CHANGE, C.DAYS))),
                                       q3=int(round(100 * ush(d, C.Q3[0], C.Q3[1]))))
                              for d, dv in enumerate(C.DEVICES)}
    sl = W["logs"]["seller"]
    fig["seller"] = dict(sellers=int(info["sellers"]), runs=int(info["scoring_runs"]),
                         failed_share_q3_pct=r2(100 * float(sl["failed"][C.Q3[0]:C.Q3[1]].sum() / sl["due"][C.Q3[0]:C.Q3[1]].sum())),
                         total_default_pct=r2(100 * float(np.sum(w * exp["seller"]["tot"][:, hq]))),
                         usual_default_pct=r2(100 * float(np.sum(w * (exp["seller"]["tot"] - exp["seller"]["exc"])[:, hq]))))
    # a seller's run after a failed run against after a scored one: each of the quarter's runs set against the same
    # seller's run before it, wherever that falls
    ff = fs_ = nf = ns_ = 0
    for i in range(sl["dirty"].shape[0]):
        idx = np.nonzero(sl["dirty"][i])[0]
        for d0_, d1_ in zip(idx[:-1], idx[1:]):
            if C.Q3[0] <= d1_ < C.Q3[1]:
                if sl["fail"][i, d0_]:
                    nf += 1
                    ff += int(sl["fail"][i, d1_])
                else:
                    ns_ += 1
                    fs_ += int(sl["fail"][i, d1_])
    fig["seller"]["fail_after_fail_pct"] = round(100.0 * ff / nf, 1)
    fig["seller"]["fail_after_scored_pct"] = round(100.0 * fs_ / ns_, 1)
    fam_sizes = dict(effects=len(C.DIMS["effect"]), fresh=len(C.DIMS["fresh"]), state=len(C.DIMS["state"]),
                     reader=len(C.DIMS["reader"]))
    # joint exposure: sessions with two groups at the default in the same market, device and hour
    joint = np.zeros_like(exp["stock"]["exc"])
    for a in range(len(G)):
        for b in range(a + 1, len(G)):
            joint += np.clip(exp[G[a]]["exc"], 0, 1) * np.clip(exp[G[b]]["exc"], 0, 1)
    fig["joint_default_pct"] = r2(100 * float(np.sum(w * joint[:, hq])))

    # ---- counts and bases every route reaches (the Step-by-Step only)
    fig["counts"] = dict(files=len(WL.FILES), unused=len(WL.UNUSED), session_rows=int(info["session_rows"]),
                         mart_rows=int(info["mart_rows"]), status_rows=int(info["status_rows"]),
                         status_rows_kept=int(info["status_rows_kept"]),
                         status_rows_reloaded=int(info["status_rows"] - info["status_rows_kept"]),
                         gaps=int(info["gaps"]), lag_episodes=int(info["lag_episodes"]),
                         scoring_rows=int(info["scoring_rows"]), scoring_runs=int(info["scoring_runs"]),
                         scoring_repeats=int(info["scoring_rows"] - info["scoring_runs"]), sellers=int(info["sellers"]),
                         experiments=int(info["experiments"]), ablation_tests=int(info["ablation_tests"]),
                         aborted=int(info["aborted"]), holdouts=len(C.READERS), render_rows=int(info["render_rows"]),
                         chains=14, sources=5, partitions=24, replicas=6, markets=6, cells=12, hours=C.H, days=C.DAYS,
                         tests_per_group=9, test_days=C.TEST_DAYS, holdout_days=42, split_batches=int(info["split_batches"]),
                         split_days=len(info["split_days"]))
    q3s = float(W["sess"][:, hq].sum())
    q2s = float(W["sess"][:, q2].sum())
    od = W["orders"]
    fig["conversion"] = dict(q2=r2(100 * float(od[:, q2].sum() / q2s)), q3=r2(100 * float(od[:, hq].sum() / q3s)))
    fig["conversion"]["fall"] = r2(fig["conversion"]["q2"] - fig["conversion"]["q3"])
    fig["q3_sessions_m"] = round(q3s / 1e6, 1)

    # ---- every route
    def route(v, name):
        c = cells(v) if "loss" in v else v
        ls = {j: c[j] for j in G}
        return dict(name=name, cost={j: r3(c[j]) for j in G}, month={n: r2(c[n]) for n in MONTHS}, all=r2(c[ALL]),
                    listed_cost=r2(c[LISTED]), list=listed(ls), call=call_of(ls))
    fig["routes"] = {k: route(lat[k], ROUTE_NAME[k]) for k in KEYS}
    for k in KEYS:                                  # each route nets a group's tests for the share that route serves
        fig["routes"][k]["effect"] = {j: r2(lat[k]["parts"][j]["eff"]) for j in G}
    fig["routes"]["direct"] = route(dr, "each job's unhealthy share over the quarter (every chain, price source and "
                                        "click-stream partition counted once) times the group's latest ablation test "
                                        "as reported, markets and devices pooled")
    fig["routes"]["rigorous"] = route(rg, "every ablation test pooled by market and device with precision weights, on "
                                          "the traffic-weighted status record")
    fig["hurried"] = dict(c1=r2(lat[REFLEX]["c1"]), c2=r2(lat[REFLEX]["c2"]), c3=r3(lat[REFLEX]["c3"]),
                          c4=r3(lat[REFLEX]["split"]), cost=fig["routes"][REFLEX]["cost"], list=fig["routes"][REFLEX]["list"],
                          all=fig["routes"][REFLEX]["all"], listed_cost=fig["routes"][REFLEX]["listed_cost"],
                          month=fig["routes"][REFLEX]["month"], effect=fig["routes"][REFLEX]["effect"])
    fig["lost_alone"] = {s: dict(c1=r2(lat[s]["c1"]), c2=r2(lat[s]["c2"]), c3=r3(lat[s]["c3"]), c4=r3(lat[s]["split"]))
                         for s in C.SIDS}

    # ---- April
    off = lambda v: r3(abs(r3(v) - r3(meas)))   # noqa: E731  (the difference of the figures as stated)
    fig["april"] = dict(record=r3(meas), golden=r3(g["split"]), off=off(g["split"]), band=c4b,
                        rivals={k: dict(value=r3(v), off=off(v)) for k, v in ref["rivals"].items()},
                        days=len(info["split_days"]), batches=int(info["split_batches"]))
    seven = [d for d in info["split_days"] if d in C.SPLIT["days"]]
    g7, m7 = april(W, {}, seven)
    fig["april_batch_days"] = dict(record=r3(m7), golden=r3(g7), off=r3(abs(r3(g7) - r3(m7))),
                                   rivals={k: dict(value=r3(april(W, C.lat_opts(k.split("+")), seven)[0]),
                                                   off=r3(abs(r3(april(W, C.lat_opts(k.split("+")), seven)[0]) - r3(m7))))
                                           for k in list(C.SIDS) + [REFLEX]})
    fig["referee_golden"] = fig["april"]["golden"]
    # the standard error of the record's difference between the two regions over the days touched
    sp = W["split"]
    wn = sp["window"]
    na, oa, nb, ob = (float(sp[k][:, wn].sum()) for k in ("na", "oa", "nb", "ob"))
    pa, pb = oa / na, ob / nb
    se_april = 100 * float(np.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb))
    fig["april"]["record_se"] = r3(se_april)
    fig["april"]["golden_off_se"] = round(abs(g["split"] - meas) / se_april, 1)

    # ---- the battery, the readings beside it and the forcing
    fig["variants"] = len(bat)
    fig["variant_names"] = [n for n, _ in bat]
    fig["family_calls_all_golden"] = all(call_of(f["loss"]) == fig["call"] for f in fam)
    fig["variant_range"] = {j: [r4(min(members[j]["family"])), r4(max(members[j]["family"]))] for j in G}
    near = min((abs(f["loss"][j] - LINE), j, n, f["loss"][j]) for n, f in bat for j in G)
    fig["nearest_variant"] = dict(distance=r4(near[0]), group=near[1], variant=near[2], value=r4(near[3]))
    fig["family_sizes"] = fam_sizes
    def outside(v):
        c = cells(v)
        return sorted(k for k in c if not bands[k][0] <= round(c[k], 3 if k in G else 2) <= bands[k][1])
    fig["beside"] = [dict(name=n, cost={j: r4(v["loss"][j]) for j in G}, call_holds=call_of(v["loss"]) == fig["call"],
                          c=[r4(v["c1"]), r4(v["c2"]), r4(v["c3"]), None if n == LOCAL_DAYS else r4(v["split"])],
                          outside=outside(v)) for n, v in side]
    near_s = min((abs(v["loss"][j] - LINE), j, n) for n, v in side for j in G)
    fig["nearest_beside"] = dict(distance=r4(near_s[0]), group=near_s[1], reading=near_s[2])
    rows, spd = C.forcing_rows(W, x)
    fig["perturbations"] = [dict(input=nm, call_holds=bool(same), nearest=r4(d), group=j_, cost={j: r4(v[j]) for j in G})
                            for nm, same, d, j_, v in rows]
    fig["spreads_pct"] = {j: dict(effect=round(100 * spd[j]["eff"], 1), served=round(100 * spd[j]["exp"], 1),
                                  reader=round(100 * spd[j]["rd"], 1)) for j in G}

    # ---- the rivals a reviewer would try, each with its figures
    un = C.view(W, {"seller_base": "none"})
    ind = C.view(W, {"seller_indep": True})
    fig["rival_seller_not_netted"] = dict(cost=r3(un["loss"]["seller"]), served_pct=r2(un["parts"]["seller"]["exposed"]),
                                          call_holds=call_of(un["loss"]) == fig["call"])
    fig["rival_seller_independent_nights"] = dict(cost=r4(ind["loss"]["seller"]), served_pct=r2(ind["parts"]["seller"]["exposed"]))
    # normal service read as the second quarter's level of service (the charter's 3.2 refuses it): each default share
    # over its second-quarter mean, the components' failed renders over their second-quarter rate
    q2w = C.q3w(W, *C.Q2)
    keep = {j: 1.0 - float(np.sum(q2w * exp[j]["exc"][:, q2])) / float(np.sum(w * exp[j]["exc"][:, hq])) for j in G}
    us = C.view(W, {"exp_scale": keep, "rd_base": "q2"})
    fig["rival_usual_level"] = dict(cost={j: r3(us["loss"][j]) for j in G}, list=listed(us["loss"]),
                                    q2_default_pct={j: r2(100 * float(np.sum(q2w * exp[j]["exc"][:, q2]))) for j in G},
                                    wrong=[j for j in G if (us["loss"][j] >= LINE) != (g["loss"][j] >= LINE)])
    # the groups' losses compounding in place of adding (each group's loss scaled by what the others left of conversion)
    hc = hourly_cost(W)
    p0 = 100.0 * float(od[:, hq].sum() / q3s) + g["total"]
    cp = {j: float(np.sum(w * (hc[j] * np.prod([1.0 - hc[k2] / p0 for k2 in G if k2 != j], axis=0))[:, hq])) for j in G}
    fig["rival_compounding"] = dict(cost={j: r4(cp[j]) for j in G}, call_holds=call_of(cp) == fig["call"],
                                    outside=[j for j in G if not bands[j][0] <= round(cp[j], 3) <= bands[j][1]],
                                    most_moved=r4(max(abs(cp[j] - g["loss"][j]) for j in G)))
    ratio = meas / lat[REFLEX]["split"]
    carried = {j: ratio * lat[REFLEX]["loss"][j] for j in G}
    fig["rival_april_ratio"] = dict(ratio=r2(ratio), cost={j: r3(carried[j]) for j in G}, list=listed(carried),
                                    wrong=[j for j in G if (carried[j] >= LINE) != (g["loss"][j] >= LINE)])
    r1 = lambda v: round(float(v), 1)   # noqa: E731
    pn = daily_regression(W, {j: W["S"][j] for j in G})
    fig["rival_daily_regression"] = {j: dict(cost=r3(pn[j][0]), se=r3(pn[j][1])) for j in G}
    fig["rival_daily_regression_list"] = [j for j in G if pn[j][0] >= LINE]
    # the groups it cannot place against the line: its own interval of two standard errors holds the line
    fig["rival_daily_regression_unplaced"] = {j: r1(abs(pn[j][0] - LINE) / pn[j][1]) for j in G
                                              if abs(pn[j][0] - LINE) < 2 * pn[j][1]}
    # the same regression on the replayed shares over normal service (the estimate's own exposure)
    pr = daily_regression(W, {j: exp[j]["exc"] for j in G})
    fig["rival_replayed_regression"] = dict(cost={j: r3(pr[j][0]) for j in G}, se={j: r3(pr[j][1]) for j in G},
                                            all=r2(sum(pr[j][0] for j in G)), list=[j for j in G if pr[j][0] >= LINE],
                                            per_session={j: r2(pr[j][2]) for j in G},
                                            unplaced={j: r1(abs(pr[j][0] - LINE) / pr[j][1]) for j in G
                                                      if abs(pr[j][0] - LINE) < 2 * pr[j][1]})
    # trend's default share is one figure a day: the same in every market and device
    sd_ = W["sess"].reshape(12, C.DAYS, 24).sum(axis=2)
    tday = (exp["trend"]["tot"] * W["sess"]).reshape(12, C.DAYS, 24).sum(axis=2) / sd_
    fig["trend_share_spread"] = dict(within_day=r4(float(tday[:, C.Q3[0]:C.Q3[1]].std(axis=0).mean())),
                                     across_days=r4(float(tday[:, C.Q3[0]:C.Q3[1]].mean(axis=0).std())))
    # the arms of trend's own tests on trend's default share that day
    hcd = {j: (hc[j] * W["sess"]).reshape(12, C.DAYS, 24).sum(axis=2) / sd_ for j in G}
    held_s, held_se = arm_on_share(W, "trend", "held", hcd)
    ctl_s, ctl_se = arm_on_share(W, "trend", "control", hcd)
    tt = [t for t in W["tests"] if t["group"] == "trend"]
    u_held = float(sum((W["u"][:, t["d0"]:t["d1"]] * t["nh"]).sum() for t in tt) / sum(t["nh"].sum() for t in tt))
    fig["trend_arms"] = dict(held=r2(held_s), held_se=r2(held_se), control=r2(ctl_s), control_se=r2(ctl_se),
                             held_expected=r2(g["c1"] * (1 - u_held)), held_origin_pct=int(round(100 * u_held)))
    # ---- a group's tests against each other, and the route on a subset of them
    agree = {}
    for j in G:
        rows_ = test_rows(W, j, exp)
        m9, se9, q9 = pooled(rows_)
        _, se3, _ = pooled([r for r in rows_ if r[0] >= C.Q3[0]])
        served = P[j]["exposed"] / 100.0
        agree[j] = dict(tests=len(rows_), q=r1(q9), df=len(rows_) - 1, pooled=r2(m9), se_all=r3(se9), se_quarter=r3(se3),
                        se_latest=r3(rows_[-1][2]), cost_se_all=r4(se9 * served), cost_se_quarter=r3(se3 * served),
                        cost_se_latest=r3(rows_[-1][2] * served),
                        from_line_all=r1((g["loss"][j] - LINE) / (se9 * served)))
        agree[j]["se_ratio_quarter"] = r1(se3 / se9)
    fig["test_agreement"] = agree
    last_k = {j: max(t["k"] for t in W["tests"] if t["group"] == j) for j in G}
    assert all(C.MONTH_START[5] <= t["d0"] < C.MONTH_START[6] for t in W["tests"] if t["k"] == last_k[t["group"]] - 3)
    subsets = [("the quarter's own tests", lambda t: t["d0"] >= C.Q3[0]),
               ("the four tests from June", lambda t: t["k"] >= last_k[t["group"]] - 3),
               ("the latest test alone", lambda t: t["k"] == last_k[t["group"]])]
    fig["rival_test_subsets"] = {}
    for nm, keep in subsets:
        v = C.view(tests_kept(W, keep))
        fig["rival_test_subsets"][nm] = dict(
            cost={j: r3(v["loss"][j]) for j in G}, list=listed(v["loss"]), call_holds=call_of(v["loss"]) == fig["call"],
            all=r2(v["total"]), listed_cost=r2(v["tier"]), c1=r2(v["c1"]), c4=r3(v["split"]), outside=outside(v),
            c_outside=[n for n, x_, b_, nd in (("1", v["c1"], c1b, 2), ("2", v["c2"], c2b, 2), ("3", v["c3"], c3b, 3),
                                               ("4", v["split"], c4b, 3)) if not b_[0] <= round(x_, nd) <= b_[1]],
            trend_from_line=r3(abs(v["loss"]["trend"] - LINE)))
    se_q3 = pooled([r for r in test_rows(W, "trend", exp) if r[0] >= C.Q3[0]])[1] * P["trend"]["exposed"] / 100.0
    v_q3 = C.view(tests_kept(W, subsets[0][1]))["loss"]["trend"]
    fig["rival_test_subsets"][subsets[0][0]]["trend_from_line_se"] = r1((v_q3 - LINE) / se_q3)
    fig["rival_test_subsets"][subsets[0][0]]["april_off_se"] = r1(
        abs(C.view(tests_kept(W, subsets[0][1]))["split"] - meas) / se_april)
    # a feed gap that ends before the snapshot's validity runs out: the estimate never puts it at the default; counted
    # from the validity's end to the next sync it is a few minutes more
    sk = W["logs"]["stock"]
    ttl = C.G["stock"]["ttl"]
    W_short = dict(W)
    W_short["logs"] = dict(W["logs"])
    W_short["logs"]["stock"] = dict(sk, default_c=np.array(
        [C.cover([(a_ + ttl - 0.125, b_ + 0.125) for kk, a_, b_ in sk["gaps"] if kk == ki and b_ + 0.125 > a_ + ttl - 0.125])
         for ki in range(sk["Wc"].shape[1])]))
    vs = C.view(W_short)
    fig["rival_stock_short_gaps"] = dict(served_pct=r2(vs["parts"]["stock"]["exposed"]), cost=r4(vs["loss"]["stock"]),
                                         inside=bands["stock"][0] <= round(vs["loss"]["stock"], 3) <= bands["stock"][1],
                                         call_holds=call_of(vs["loss"]) == fig["call"])
    wq = tests_kept(W, subsets[0][1])
    stacked = [C.view(wq, {"trend_refill": 0.0}), C.view(wq, {"trend_refill": 0.0, "eff_raw": True})]
    fig["rival_test_subsets_stacked"] = dict(trend=[r4(v["loss"]["trend"]) for v in stacked],
                                             call_holds=all(call_of(v["loss"]) == fig["call"] for v in stacked),
                                             nearest=r3(min(abs(v["loss"]["trend"] - LINE) for v in stacked)))
    pdid = C.panel_did(W, {j: exp[j]["exc"] for j in G})
    fig["rival_daily_within_day"] = {j: (dict(cost=r3(pdid[j][0]), se=r3(pdid[j][1])) if j in pdid else None) for j in G}
    one = C.view(W, {"u_grain": "test", "eff_pool": "all"})
    fig["rival_one_pooled_effect"] = dict(cost={j: r3(one["loss"][j]) for j in G}, call_holds=call_of(one["loss"]) == fig["call"])

    # ---- the world's own values, for the checks (never shipped)
    fig["truth"] = {j: r4(tr[j]) for j in G}
    fig["truth_call"] = call_of(tr)
    fig["core_world_golden"] = {j: r4(x0["g"]["loss"][j]) for j in G}

    # ---- the core on the cut pack
    rws, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))  # noqa: E731
    fig["rubric"] = dict(level=level, fails=[r[0] + ": " + r[2] for r in rws if r[1] == "FAIL"],
                         one_lost={s: round(earn["earn"][key(s)], 1) for s in C.SIDS},
                         fixed_alone={s: round(earn["earn"][key(ALONE[s])], 1) for s in C.SIDS},
                         reflex=round(earn["earn"][key(REFLEX)], 1), rigorous=round(earn["rigorous"], 1))
    fig["stated"] = dict(sections=[2.1, 3.1, 3.2, 3.3, 3.4, 4.1], line=0.05, year=[2026, 2027], validity_hours=[2, 36, 6, 120],
                         sync_minutes=15, half_sync_minutes=7.5, window_hours=1, batch_hour="04:00", held_pct=4, holdout_pct=10,
                         five_nights=5, ttl_change="9 June", seven=7, twelve=12, three=3, four=4, two=2, one=1, zero=0,
                         hundred=100, expired_from="16:00", expired_to="04:00", stock_default_after_minutes=112.5,
                         ttl_seconds=[300, 720])
    E, g_lost = effort(W, fig, spec, x, bands, dr)
    fig["result_grades"] = g_lost
    return dict(W=W, info=info, x=x, bat=bat, gm=gm, core=WC), fig, E, spec


def result_values(W, o, fig):
    v = C.view(W, o)
    return {"R1": dict(fig["counts"]), "R2": float(v["c1"]), "R3": float(v["c2"]), "R4": float(v["c3"]),
            "R5": float(v["split"]), "R6": {j: cells(v)[j] for j in G},
            "R7": {k: cells(v)[k] for k in [ALL] + MONTHS}, "R8": call_of(v["loss"])}


def effort(W, fig, spec, x, bands, dr):
    gold = result_values(W, {}, fig)
    gold.update(R2=fig["c1"], R3=fig["c2"], R4=fig["c3"], R5=fig["referee_golden"], R6=dict(fig["cost"]),
                R7=dict(fig["asks_together"]))  # as the blocks state them
    careful = result_values(W, C.lat_opts(REFLEX.split("+")), fig)
    quick = {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None, "R6": {j: dr[j] for j in G},
             "R7": {k: dr[k] for k in [ALL] + MONTHS}, "R8": call_of({j: dr[j] for j in G})}
    whole = ["L18", "N21", "L16"]
    meta = [
        ("R1", "the registry, the status record, the gap, batch, lag and scoring logs, the experiment export, the edge "
               "cache record and the render record on one calendar and one market and device scheme: the rows, runs, "
               "tests and sources each holds", "Step-by-Step", "counts", [], "", {}, []),
        ("R2", "each group's full effect per session at its default, from its ablation tests over the share of the held "
               "slice's result page views built at origin: trend's (points)", "Component 1", "c1", ["R1"],
         "the ablation results by test, market, device and day against the edge cache's daily record",
         dict(band=fig["c1_band"]), PREC["S1"]),
        ("R3", "the share of the quarter's sessions served each group's default over what normal service leaves there, "
               "rebuilt source by source: seller's (per cent)", "Component 2", "c2", ["R1"],
         "the scoring log by seller and night, each score's validity and the month's traffic by seller",
         dict(band=fig["c2_band"]), PREC["S2"]),
        ("R4", "the cost through each component that also reads a group, from its own holdout test and its own render "
               "record: the delivery promise badge's (points)", "Component 3", "c3", ["R1"],
         "the component holdout results and the render record by hour", dict(band=fig["c3_band"]), PREC["S3"]),
        ("R5", "April's missed price batches in one serving region, called from R2 to R4 and the hours the prices had "
               "expired (points over the business days touched)", "Component 4", "referee_golden", ["R2", "R3", "R4"],
         "the conversion mart by serving region and day", dict(band=fig["c4_band"]), ["L28", "N21", "L16"]),
        ("R6", "each feature group's third-quarter cost (points)", "Asks 1 to 7", "cost", ["R2", "R3", "R4"], "",
         dict(bands={k: bands[k] for k in G}, partly_share=0.5), whole),
        ("R7", "the cost of all the groups together over the quarter and over each of its months' search sessions "
               "(points)", "Asks 8 to 11", "asks_together", ["R2", "R3", "R4"], "",
         dict(bands={k: bands[k] for k in [ALL] + MONTHS}, partly_share=0.5), whole),
        ("R8", "the groups on the 2027 tier one list", "Recommendation", "call", ["R6"], "", {}, whole),
    ]
    res = []
    for rid, name, graded, key_, dep, indep, extra, prec in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": key_, "depends": dep, "independent": indep,
             "golden": gold[rid], "passes": {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]},
             "precedent": prec}
        r.update(extra)
        res.append(r)
    by = {r["id"]: r for r in res}

    def grades(k):
        v = result_values(W, C.lat_opts(k.split("+")), fig)
        return {rid: EF.grade(v[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(k) for k in KEYS}
    lat = spec["lattice"]
    said = {s: spec["stumps"][s]["said_out_loud"] for s in C.SIDS}
    judgments = []
    for s in C.SIDS:
        ak = ALONE[s]
        judgments.append({"id": s, "name": STUMP_NAME[s], "kind": "stump", "precedent": PREC[s],
                          "dropped": {"answer": call_of(lat[s]), "results_moved": [r for r, v in g_lost[s].items() if v != "right"]},
                          "alone": {"answer": call_of(lat[ak]),
                                    "results_rescued": [r for r, v in g_lost[ak].items() if v == "right" and r != "R1"]}})
    judgments += [
        {"id": "J4", "name": "the monitor's reloaded week, renamed shards, rows the scoring writer wrote twice, two status "
                             "vocabularies, the aborted test, the mart's market keys and wall-clock times brought to one "
                             "calendar and scheme", "kind": "reflex", "precedent": ["R01"]},
        {"id": "J5", "name": "every file read, the three unused ones set aside", "kind": "reflex", "precedent": ["R02"]},
        {"id": "J6", "name": "the randomised tests pooled by market and device with intervals", "kind": "reflex",
         "precedent": ["R55", "R04", "R67"]},
        {"id": "J7", "name": "the two serving regions compared over April's nights with other weeks as a placebo and an "
                             "interval", "kind": "reflex", "precedent": ["R92"]},
        {"id": "J8", "name": "each source weighted by the traffic the shipped tables give it", "kind": "reflex",
         "precedent": ["R01"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": call_of(lat[REFLEX])}, "judgments": judgments}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": ROUTE_NAME[k], "answer": call_of(lat[k])} for k in KEYS]
    for k in ("direct", "rigorous"):
        routes.append({"name": fig["routes"][k]["name"], "answer": fig["routes"][k]["call"]})
    mem = spec["members"]
    n = len(fig["variant_names"])
    fam_rows = [{"name": fig["variant_names"][i], "answer": call_of({j: mem[j]["family"][i] for j in G})} for i in range(n)]
    forcing = {"kind": "set", "golden_answer": fig["call"], "golden_family": fam_rows,
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": p["input"], "answer": call_of(p["cost"])} for p in fig["perturbations"]]}
    hints = [{"sentence": said[s], "rescues": [r for r, v in g_lost[ALONE[s]].items() if v == "right" and r != "R1"]}
             for s in C.SIDS]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


if __name__ == "__main__":
    import json
    X, fig, E, spec = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    code = corelib.run(spec)
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "nearest_variant", "april", "truth", "variants")}, default=float))
    for j in G:
        print("%-8s %.3f %-16s truth %.4f  effect %.2f (as measured %.2f)  served %.2f%% (status %.2f%%)  margin %.3f" % (
            j, fig["cost"][j], fig["cost_band"][j], fig["truth"][j], fig["full_effect"][j], fig["measured_effect"][j],
            fig["served_default_pct"][j], fig["status_unhealthy_pct"][j], fig["margin"][j]))
    print("months", fig["month"], fig["month_band"], "all", fig["all"], fig["all_band"], "listed", fig["listed_cost"], fig["listed_band"])
    print("C1", fig["c1"], fig["c1_band"], "C2", fig["c2"], fig["c2_band"], "C3", fig["c3"], fig["c3_band"], "C4", fig["c4"], fig["c4_band"])
    for b in fig["beside"]:
        print("beside: %-66s %s %s c %s" % (b["name"][:66], "same call" if b["call_holds"] else "CALL MOVES",
                                            " ".join("%.4f" % b["cost"][j] for j in G), b["c"]))
    print("golden:  %s" % " ".join("%.4f" % X["x"]["g"]["loss"][j] for j in G), "april se", fig["april"]["record_se"])
    for p in fig["perturbations"]:
        print("%-46s %s nearest %.4f %s" % (p["input"], "same call" if p["call_holds"] else "CALL MOVES", p["nearest"], p["group"]))
    for k in ("rival_compounding", "rival_usual_level", "rival_seller_not_netted", "rival_seller_independent_nights", "rival_april_ratio", "rival_daily_regression",
              "rival_daily_within_day", "rival_one_pooled_effect", "april_batch_days", "joint_default_pct", "conversion",
              "fresh_share_pct", "seller", "render_failed_pct", "reader_per_eligible", "reader_eligible_pct"):
        print(k, json.dumps(fig[k], default=float))
    sys.exit(code)
