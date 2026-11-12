"""task7 architecture 10: the estimators, from the pack alone (verify.Pack).

The golden: each provider's reduction per assigned device on the randomised test events, measured on the research sample
(held-back half against called half, 15 minutes at a time) and split into the shed of a device still in the event and the
share still in it (the reports); the shed carried to each 4CP day's heat by a straight line in temperature and to the
fleet's homes by each home's cooling slope as the appraisal roll predicts it; the share read on the 4CP days themselves,
cohort by cohort (channel, years enrolled), and weighted to the devices that will be enrolled on 1 July 2027; the
product read at each 4CP interval's place in the provider's window, an uncalled day counted as nothing; the twelve
intervals averaged.

The routes the shortcuts take are the same functions with one carry or another left out."""
import datetime as dt

import numpy as np

import verify as V

STEP = 15
AT = STEP / 2                   # where in a 15-minute interval "still in the event" is read: its middle
ASOF = dt.date(2026, 10, 30)
JULY27 = dt.date(2027, 7, 1)
CH = ("app", "mail", "retail")
TEN_EDGES = (1.0, 2.0, 3.0)


def ten_band(t):
    return int(np.searchsorted(TEN_EDGES, t, side="right"))


def tenure(v, d):
    return max(0.0, (d - v["joined"]).days / 365.25)


def provider_devices(P, p):
    return [v for v in P.dev.values() if v["p"] == p]


def ami_devices(P, p):
    acc = set(P.ami_accts)
    return [v for v in provider_devices(P, p) if v["acct"] in acc]


def status(P, v, d, minute, end=False):
    """(received, still in the event at `minute`) for a device called on day d; a device a provider left out of its
    report was not reached"""
    rep = P.rep.get((d, v["pid"]))
    if rep is None:
        return False, False
    received, ov = rep
    if not received:
        return False, False
    if ov is None:
        return True, True
    return True, ov > minute


# ---------------------------------------------------------------- test events: the reduction and the share in the event
def test_tables(P, p, adjust=True):
    """for each test event: the interval means of the held-back and called halves of the research sample's devices, the
    called half's share received and still in the event at each interval's midpoint, and the temperature"""
    s = P.settings[p]
    out = []
    devs = ami_devices(P, p)
    for e in P.events:
        if e["kind"] != "test":
            continue
        d = e["date"]
        call, hold, sh = [], [], []
        for v in devs:
            if not V.active(v, d):
                continue
            g = P.assign.get((e["code"], v["pid"]))
            x = P.ami.get((v["acct"], d))
            if g is None or x is None:
                continue
            if g:
                call.append(x)
                sh.append([status(P, v, d, m + AT)[1] if m + STEP / 2 < s["e"] else status(P, v, d, s["e"])[1]
                           for m in P.ami_mins])
                sh[-1] = [float(z) for z in sh[-1]]
                sh[-1].append(float(status(P, v, d, 0)[0]))
            else:
                hold.append(x)
        if len(call) < 5 or len(hold) < 5:
            continue
        call, hold, sh = np.array(call), np.array(hold), np.array(sh)
        if adjust:
            # each interval regressed on the half and the home's own 13:00 to 14:30 load that day, before any event
            X = np.vstack([call, hold])
            g_ = np.r_[np.ones(len(call)), np.zeros(len(hold))]
            pre = np.nanmean(X[:, :6], axis=1)
            red = np.zeros(X.shape[1])
            for k in range(X.shape[1]):
                ok = np.isfinite(X[:, k]) & np.isfinite(pre)
                A = np.vstack([np.ones(ok.sum()), g_[ok], pre[ok]]).T
                b, *_ = np.linalg.lstsq(A, X[ok, k], rcond=None)
                red[k] = -b[1]
        else:
            red = np.nanmean(hold, axis=0) - np.nanmean(call, axis=0)
        S = sh[:, :-1].mean(axis=0)
        R = sh[:, -1].mean()
        T = np.array([V.temp_at(P, d, m + STEP / 2) for m in P.ami_mins])
        out.append(dict(date=d, red=red, S=S, R=R, T=T, n=(len(call), len(hold))))
    return out


def fit_line(x, y, w=None):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    w = np.ones(ok.sum()) if w is None else np.asarray(w, float)[ok]
    A = np.vstack([np.ones(ok.sum()), x[ok]]).T * np.sqrt(w)[:, None]
    b, *_ = np.linalg.lstsq(A, y[ok] * np.sqrt(w), rcond=None)
    return b


def shed_model(P, p, how="split", adjust=True):
    """per interval of the export window, a straight line in temperature of the reduction per assigned device ("itt",
    the hurried read) or of the shed per device still in the event and, after the window, the snapback per device that
    ran to the end and, before it, the pre-cool per device reached ("split")"""
    s = P.settings[p]
    tabs = test_tables(P, p, adjust)
    lines = []
    for k, m in enumerate(P.ami_mins):
        mid = m + STEP / 2
        xs, ys = [], []
        for t in tabs:
            if how == "itt":
                y = t["red"][k]
            elif mid < s["s"]:
                y = t["red"][k] / max(t["R"], 1e-6)
            else:
                y = t["red"][k] / max(t["S"][k], 1e-6)
            xs.append(t["T"][k])
            ys.append(y)
        lines.append(fit_line(xs, ys))
    return dict(lines=lines, tabs=tabs)


def shed_at(P, model, minute, T):
    k = int((minute - P.ami_mins[0]) // STEP)
    k = min(max(k, 0), len(P.ami_mins) - 1)
    b = model["lines"][k]
    return float(b[0] + b[1] * T)


# ---------------------------------------------------------------- the homes: each home's cooling slope from the roll
def cooling_slopes(P):
    """each research-sample home's afternoon load against the day's heat on its quiet days (no event, or held back):
    kW per degree, the air conditioning its size and age set"""
    quiet = {}
    for e in P.events:
        quiet[e["date"]] = e
    by_acct = {}
    devs = {v["acct"]: v for v in P.dev.values()}
    for (a, d), x in P.ami.items():
        e = P.ev_by_date.get(d)
        if e is not None:
            v = devs.get(a)
            if e["kind"] == "alert" or v is None:
                continue
            g = P.assign.get((e["code"], v["pid"]))
            if g is None or g:
                continue
        y = np.nanmean(x[8:20])                      # 15:00 to 18:00
        T = float(np.mean([V.temp_at(P, d, m) for m in range(900, 1080, 30)]))
        by_acct.setdefault(a, []).append((T, y))
    slope = {}
    for a, pts in by_acct.items():
        if len(pts) < 8:
            continue
        b = fit_line([t for t, _ in pts], [y for _, y in pts])
        slope[a] = b[1]
    return slope


def home_model(P, slope, form="log"):
    """a home's cooling slope from its living area and year built in the appraisal roll, fitted on the research sample"""
    X, y = [], []
    for a, s in slope.items():
        h = P.home.get(a)
        if h is None or s <= 0:
            continue
        sq, yb = h
        age = np.clip((2005 - yb) / 40.0, 0, 1.2)
        if form == "log":
            X.append([1, np.log(sq), age])
            y.append(np.log(s))
        else:
            X.append([1, sq / 1000.0, age, sq / 1000.0 * age])
            y.append(s)
    X, y = np.array(X), np.array(y)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)

    def pred(a):
        h = P.home.get(a)
        if h is None:
            return np.nan
        sq, yb = h
        age = np.clip((2005 - yb) / 40.0, 0, 1.2)
        if form == "log":
            return float(np.exp(b[0] + b[1] * np.log(sq) + b[2] * age))
        return float(b[0] + b[1] * sq / 1000.0 + b[2] * age + b[3] * sq / 1000.0 * age)
    return pred


# ---------------------------------------------------------------- next summer's devices
def attrition(P, ch):
    """devices leaving a year, per device-year enrolled, 2021 to the roster date, by channel"""
    ex = left = 0.0
    for v in P.dev.values():
        if v["ch"] != ch:
            continue
        end = v["left"] or ASOF
        ex += max(0.0, (end - v["joined"]).days / 365.25)
        left += v["left"] is not None
    return left / ex if ex else 0.0


def fleet_2027(P, p, how="channel"):
    """(device, weight) of the devices expected enrolled on 1 July 2027: today's, each surviving at its channel's rate,
    and the quote's new enrolments, each like the provider's recent enrolments through that channel"""
    rate = {ch: attrition(P, ch) for ch in CH}
    yrs = (JULY27 - ASOF).days / 365.25
    out = []
    for v in provider_devices(P, p):
        if not V.active(v, ASOF):
            continue
        r = rate[v["ch"]] if how == "channel" else np.mean(list(rate.values()))
        out.append((dict(v, kind="now"), float(np.exp(-r * yrs))))
    recent = [v for v in provider_devices(P, p) if v["joined"] >= dt.date(2025, 1, 1)]
    for ch, n in P.quote[p]["new"].items():
        if n <= 0:
            continue
        like = [v for v in recent if v["ch"] == ch] or [v for v in provider_devices(P, p) if v["ch"] == ch] or recent
        for k in range(n):
            src = like[k % len(like)]
            out.append((dict(src, kind="new", ch=ch, joined=dt.date(2027, 3, 15)), float(np.exp(-rate[ch] * 0.3))))
    return out


def n_2027(P, p):
    return sum(w for _, w in fleet_2027(P, p))


# ---------------------------------------------------------------- the share in the event: a device-level model
def called_devices(P, p, d):
    e = P.ev_by_date.get(d)
    out = []
    for v in provider_devices(P, p):
        if not V.active(v, d):
            continue
        if e is not None and e["kind"] == "test" and not P.assign.get((e["code"], v["pid"])):
            continue
        out.append(v)
    return out


def logit_fit(X, y, iters=40):
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        z = X @ b
        mu = 1 / (1 + np.exp(-z))
        W_ = mu * (1 - mu) + 1e-9
        H = X.T @ (X * W_[:, None]) + 1e-6 * np.eye(X.shape[1])
        b = b + np.linalg.solve(H, X.T @ (y - mu))
    return b


def share_model(P, p, days, minute_of):
    """in the event (reached and not yet overridden) at the given minute, device by device on the given days: a day's
    own level, the channel and the years enrolled"""
    rows, y = [], []
    for j, d in enumerate(days):
        for v in called_devices(P, p, d):
            rows.append((j, v["ch"], tenure(v, d)))
            y.append(float(status(P, v, d, minute_of(d))[1]))
    nd = len(days)
    X = np.zeros((len(rows), nd + 3))
    for k, (j, ch, t) in enumerate(rows):
        X[k, j] = 1
        X[k, nd] = ch == "mail"
        X[k, nd + 1] = ch == "retail"
        X[k, nd + 2] = t
    has = [X[:, nd].any(), X[:, nd + 1].any()]
    keep = [i for i in range(nd)] + [nd + k for k in range(2) if has[k]] + [nd + 2]
    b = np.zeros(nd + 3)
    b[keep] = logit_fit(X[:, keep], np.array(y))
    return dict(b=b, days=list(days), nd=nd)


def predict_share(m, d, mix):
    """the model's share in the event on day d for a set of (device, weight) at the tenure they have on the 2027
    date of that day (or the day itself)"""
    j = m["days"].index(d)
    b, nd = m["b"], m["nd"]
    num = den = 0.0
    for v, w, t in mix:
        z = b[j] + b[nd] * (v["ch"] == "mail") + b[nd + 1] * (v["ch"] == "retail") + b[nd + 2] * t
        num += w / (1 + np.exp(-z))
        den += w
    return num / den


def observed_share(P, p, d, minute):
    vs = called_devices(P, p, d)
    return sum(status(P, v, d, minute)[1] for v in vs) / max(len(vs), 1)


def fleet_mix(fleet, d):
    d27 = dt.date(2027, d.month, d.day)
    return [(v, w, tenure(v, d27)) for v, w in fleet]


def sample_mix(P, p, d):
    return [(v, 1.0, tenure(v, d)) for v in ami_devices(P, p) if V.active(v, d)]


# ---------------------------------------------------------------- the value at the 4CP intervals
def transport(P, p, fleet, slope_pred):
    """the fleet's predicted cooling slope over the research sample's devices' own: how much more (or less) a device in
    the fleet sheds than one in the sample"""
    num = [(slope_pred(v["acct"]), w) for v, w in fleet]
    num = [(x, w) for x, w in num if np.isfinite(x)]
    den = [slope_pred(v["acct"]) for v in ami_devices(P, p)]
    den = [x for x in den if np.isfinite(x)]
    return (sum(x * w for x, w in num) / sum(w for _, w in num)) / float(np.mean(den))


def at_minute(s, mid):
    return min(mid, s["e"]) if mid >= s["e"] else mid


def value(P, p, j2=True, j3=True, j4=True, slope_pred=None, fleet_how="channel", shed=None, itt=None, detail=None):
    """kW per device enrolled on 1 July 2027 that the provider takes off the co-op's load in the 4CP intervals of a
    summer like 2024 to 2026. The golden carries the test events' shed per device in the event to each 4CP day's heat,
    to the fleet's homes (j4) and multiplies it by the share in the event that day for the 2027 fleet's cohorts (j2 and
    j3). Without j2 the test events' own reduction per assigned device is read at the 4CP interval and adjusted for
    the 2027 cohorts on the test events (j3) or the fleet's homes (j4)."""
    s = P.settings[p]
    fleet = fleet_2027(P, p, fleet_how)
    tf = transport(P, p, fleet, slope_pred) if j4 else 1.0
    cps = [cp for cp in P.cps if cp["called"]]
    if j2:
        model = shed or shed_model(P, p, "split")
        days = [cp["date"] for cp in cps]
        sm = share_model(P, p, days, lambda d: at_minute(s, next(c["start"] for c in cps if c["date"] == d) + AT))
        tot = 0.0
        for cp in cps:
            d, mid = cp["date"], cp["start"] + STEP / 2
            sh = shed_at(P, model, mid, V.temp_at(P, d, mid)) * tf
            if j3:
                S = predict_share(sm, d, fleet_mix(fleet, d))
            else:
                S = observed_share(P, p, d, at_minute(s, cp["start"] + AT))
            tot += sh * (1.0 if mid < s["s"] else S)
            if detail is not None:
                detail[d] = dict(shed=sh, share=S, kw=sh * (1.0 if mid < s["s"] else S), T=V.temp_at(P, d, mid))
        return tot / len(P.cps)
    model = itt or shed_model(P, p, "itt")
    tests = [t["date"] for t in model["tabs"]]
    tot = 0.0
    for cp in cps:
        d, mid = cp["date"], cp["start"] + STEP / 2
        v = shed_at(P, model, mid, V.temp_at(P, d, mid)) * tf
        if j3 and mid >= s["s"]:
            at = at_minute(s, mid)
            sm = share_model(P, p, tests, lambda _d: at)
            r27 = np.mean([predict_share(sm, td, fleet_mix(fleet, td)) for td in tests])
            rs = np.mean([predict_share(sm, td, sample_mix(P, p, td)) for td in tests])
            v *= r27 / rs
        tot += v
    return tot / len(P.cps)


def hurried_itt(P, p, quick=False):
    """the reduction per assigned device read straight off the test events: a straight line in temperature at each 4CP
    interval (the careful but hurried read), or the event window's average on the test events (the quick read)"""
    s = P.settings[p]
    model = shed_model(P, p, "itt")
    if quick:
        vals = []
        for t in model["tabs"]:
            k0 = int((s["s"] - P.ami_mins[0]) // STEP)
            k1 = int((s["e"] - P.ami_mins[0]) // STEP)
            vals.append(np.nanmean(t["red"][k0:k1]))
        return float(np.mean(vals))
    return value(P, p, False, False, False, itt=model)


def renewed(P, kw):
    return [p for p in P.providers if kw[p] * P.rate > P.quote[p]["price"]]
