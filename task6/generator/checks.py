"""The generator's assertions on the cut pack (architecture 7): the input gates, the bar block (R1 to R7: the raw
material ships, each mess item is neutral, each result's hurried figure falls outside its band, nothing is planted,
no one thing carries the results, the one-fact test computed, every rival inside its band), every semantic fork row
(SF1 to SF16, SF19), the one-decimal margins and the documents' controls.

    python3 checks.py [target_dir]            (run by build.py)"""
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import common as K      # noqa: E402
import deliver as D     # noqa: E402

FAILS = []
GOLD = ["fares", "places", "seat-map", "partner-gateway", "notifications"]
TRUTH = {x["fault"] for x in K.DEC_INCIDENTS}


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def r1set(S):
    return {s: K.r1(S[s]["sli"]) for s in K.SVC}


def over_of(S, bud):
    return [s for s in K.SVC if K.r1(S[s]["sli"]) > bud[s]]


def text_of(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    return "\n".join(parts)


def main(target):
    del FAILS[:]
    g = AN.Golden(target)
    R = g.run()
    F = D.figures(R)
    incs = R["incidents"]
    dec = [x for x in incs if x["declared"] >= AN.DEC0]
    S, P = R["S"], R["P"]
    gold1 = r1set(S)

    # ---------------------------------------------------------------- input gates
    files = sorted(f for f in os.listdir(target) if not f.startswith("."))
    check("IG1 ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {"csv": "spreadsheet", "xlsx": "spreadsheet", "parquet": "database", "json": "database", "docx": "text",
            "md": "text"}
    kinds = {cats.get(f.rsplit(".", 1)[-1]) for f in files}
    check("IG2 two or more file categories", len(kinds - {None}) >= 2, ", ".join(sorted(k for k in kinds if k)))
    n_lb = sum(1 for _ in open(os.path.join(target, K.FILES["lb_h2"]))) - 1
    n_bill = sum(1 for _ in open(os.path.join(target, K.FILES["billing"]))) - 1
    check("IG3 a CSV of 20,000 rows or more", n_lb >= 20000, "%s %d rows" % (K.FILES["lb_h2"], n_lb))
    check("IG4 a CSV of ten printed pages or more", n_bill >= 600, "%s %d rows" % (K.FILES["billing"], n_bill))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    dis = [p_.split("/", 1)[1] for p_ in meta.get("distractor_files", [])]
    check("IG5 two or more distractors named in metadata.json", len(dis) >= 2, ", ".join(dis))
    src = open(os.path.join(HERE, "analysis.py")).read()
    read_keys = set(re.findall(r'K\.FILES\["(\w+)"\]', src))
    check("IG6 the golden reads no distractor", not ({K.FILES_KEY_OF[d] for d in dis} & read_keys),
          "reads %s" % ", ".join(sorted(read_keys)))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|distractor", f, re.I)]
    check("IG7 no file describes the pack", not bad, ", ".join(bad) or "none")

    # ---------------------------------------------------------------- the results, as designed
    check("RES1 the golden list", P["over"] == GOLD, ", ".join(P["over"]))
    att = R["attribution"]
    want = {}
    for x, spec in zip(sorted(dec, key=lambda z: z["declared"]), sorted(K.DEC_INCIDENTS, key=lambda z: z["declared"])):
        want[x["id"]] = spec["fault"]
    check("RES2 every December customer-facing incident put on the world's own fault", att == want,
          "; ".join("%s %s" % (k, v) for k, v in att.items()))
    check("RES3 seven customer-facing incidents in December, reviews open", len(dec) == 7 and all(
        x["review"] == "open" and not x["cause"] for x in dec), "%d" % len(dec))
    # each fault's rise leads every other named service's by 20 minutes or more
    lead = []
    for x in dec:
        on = R["onset"][x["id"]]
        f = att[x["id"]]
        others = [v[0] for s_, v in on.items() if s_ != f and v]
        if others:
            lead.append(min(others) - on[f][0])
    check("RES4 each cause leads the other named services' rises by twenty minutes or more",
          all(v >= 1200 for v in lead), "leads %s minutes" % ", ".join("%.0f" % (v / 60) for v in lead))

    # ---------------------------------------------------------------- R1 raw material
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(target, f))))
    check("R1 no shipped column carries an SLI or a keep share", not [h for h in heads if re.search(
        r"sli|keep|sample|weight", h, re.I)], "%d columns read" % len(heads))
    check("R1 the SLIs read the span export and the balancer's counts", all(S[s]["kept"] > 1000 for s in K.SVC),
          "kept spans per service %d to %d" % (min(S[s]["kept"] for s in K.SVC), max(S[s]["kept"] for s in K.SVC)))

    # ---------------------------------------------------------------- R2 mess neutral
    for label, kw in (("re-sent span rows counted twice", {"dedupe": False}),):
        g2 = AN.Golden(target, **kw)
        R2 = g2.run()
        same = r1set(R2["S"]) == gold1 and R2["attribution"] == att and R2["P"]["over"] == GOLD
        moved = {s: (gold1[s], K.r1(R2["S"][s]["sli"])) for s in K.SVC if K.r1(R2["S"][s]["sli"]) != gold1[s]}
        check("R2 %s moves no graded result" % label, same, "moved %s" % moved if moved else "every SLI, cause and the list")
    ex_d = g.excluded(att, dec, from_declaration=True)
    S_d = g.slis(g.weights("root"), ex_d, fill=g.fill(g.weights("root"), ex_d, AN.FILL, dec))
    check("R2 windows read from the declaration move no SLI (the timeline convention is texture for the SLIs)",
          r1set(S_d) == gold1, str({s: K.r1(S_d[s]["sli"]) for s in K.SVC if K.r1(S_d[s]["sli"]) != gold1[s]}))
    m_back = g.minutes(backdate=True)
    check("R2 reading every service from the declaration moves the incident minutes (graded in R1 only)",
          m_back != R["minutes"], "")

    # ---------------------------------------------------------------- R3 each result's hurried figure
    ex = g.excluded(att, dec)
    wr, w_own = g.weights("root"), g.weights("own")
    fill_of = lambda w, e, form=AN.FILL: g.fill(w, e, form, dec)
    Sc, Pc = R["careful"]["S"], R["careful"]["P"]
    check("R3 careful pass (own hourly counts, causes dated, the export's hours alone) misses the list",
          Pc["over"] != GOLD and "journey-search" in Pc["over"] and not {"partner-gateway", "notifications"} & set(
              Pc["over"]), ", ".join(Pc["over"]))
    Sw = R["weights_only"]["S"]
    check("R3 the trace roots' weights over the export's hours alone put journey-search over as well",
          over_of(Sw, R["bud"]) == sorted(set(GOLD) | {"journey-search"}, key=K.SVC.index),
          "%s; journey-search %.3f" % (", ".join(over_of(Sw, R["bud"])), Sw["journey-search"]["sli"]))
    Sp = R["periods_only"]["S"]
    check("R3 the dropped hours filled on each service's own hourly count leave fares, partner-gateway and "
          "notifications within budget", all(K.r1(Sp[s]["sli"]) <= R["bud"][s] for s in ("fares", "partner-gateway",
                                                                                          "notifications")),
          "fares %.3f, partner-gateway %.3f, notifications %.3f" % tuple(Sp[s]["sli"] for s in (
              "fares", "partner-gateway", "notifications")))
    rc = R["window"]
    check("R3 root weights and the fill with the whole-window attribution leave fares and notifications out",
          not {"fares", "notifications"} & set(rc["P"]["over"]) and rc["attribution"] != att,
          "fares %.3f, notifications %.3f" % (rc["S"]["fares"]["sli"], rc["S"]["notifications"]["sli"]))
    # the misleading form (a blocked caller ending further over its curve than the fault) is not placed only where it
    # decides: each incident the whole-window reading misreads, misread alone on the root weights
    moves = {}
    for iid, s_ in rc["attribution"].items():
        if s_ != att[iid]:
            a_ = dict(att, **{iid: s_})
            e_ = g.excluded(a_, dec)
            moves[iid] = g.programme(g.slis(wr, e_, fill=fill_of(wr, e_)))["over"]
    deciding = {k: sorted(set(GOLD) - set(v)) for k, v in moves.items() if v != GOLD}
    check("R5 the whole-window reading misreads an incident where nothing turns on it, and two that decide different "
          "services", len(moves) - len(deciding) >= 1 and len(deciding) >= 2 and len({tuple(v) for v in
                                                                                    deciding.values()}) >= 2,
          "; ".join("%s: %s" % (k, ", ".join(v) or "no verdict moves") for k, v in
                    ((k, sorted(set(GOLD) - set(moves[k]))) for k in moves)))
    first = {x["id"]: x["named"][0][0] for x in dec}
    last = {x["id"]: x["named"][-1][0] for x in dec}
    for lab, a_ in (("first-named", first), ("last-named", last)):
        e_ = g.excluded(a_, dec)
        S_x = g.slis(wr, e_, fill=fill_of(wr, e_))
        check("R3 root weights with the %s service at fault miss the list" % lab, over_of(S_x, R["bud"]) != GOLD,
              ", ".join(over_of(S_x, R["bud"])))
    e_ = g.excluded({x["id"]: "__none__" for x in dec}, dec)
    S_none = g.slis(wr, e_, fill=fill_of(wr, e_))
    check("R3 the route that ignores PR-SLO-3 3.2 loses the symptoms' SLI cells",
          sum(K.r1(S_none[s]["sli"]) != gold1[s] for s in K.SVC) >= 3,
          "cells moved: %s" % ", ".join(s for s in K.SVC if K.r1(S_none[s]["sli"]) != gold1[s]))
    gaps = {s: round(max(abs(R["ci"][s][0] - g.binomial_interval(s, ex, S[s]["sli"])[0]),
                         abs(R["ci"][s][1] - g.binomial_interval(s, ex, S[s]["sli"])[1])), 3) for s in GOLD}
    check("R3 a binomial interval misses every over-budget service's interval by 0.025 or more at one end",
          all(v >= 0.025 for v in gaps.values()), str(gaps))

    # ---------------------------------------------------------------- R4 no plant
    check("R4 no December fault sits only in the services whose verdict turns on it",
          len(TRUTH) >= 5 and len({s for x in K.DEC_INCIDENTS for s, _ in x["named"]}) >= 8,
          "faults in %s; %d services named" % (", ".join(sorted(TRUTH)),
                                               len({s for x in K.DEC_INCIDENTS for s, _ in x["named"]})))
    closed = [x for x in g.incidents() if x["review"] == "closed" and len(x["named"]) > 1]
    first_right = sum(1 for x in closed if x["cause"] == K.TRACE_NAME[x["named"][0][0]] or
                      g.by_trace.get(x["cause"]) == x["named"][0][0])
    check("R4 the closed reviews show the first service named is not reliably the cause",
          0.2 <= first_right / max(len(closed), 1) <= 0.6, "%d of %d" % (first_right, len(closed)))
    cut = g.held_from()
    check("R4 the export begins where the store's 31 days began, on a whole hour",
          cut == K.STORE_FROM_H and abs(g.t0[g.dec].min() - cut * 3600) < 60, "hour %d" % cut)
    check("R4 no customer-facing December incident falls in the hours the store had dropped",
          all(AN.sec_of(x["declared"]) >= cut * 3600 for x in dec), "")
    quiet = g.quiet_hours(dec)
    hrs = np.arange(AN.H)
    inside = {}
    for s in K.SVC:
        held_n = g.N[s][(hrs >= cut) & quiet]
        gone_n = g.N[s][hrs < cut]
        inside[s] = round(float(gone_n.max() / held_n.max()), 2)
    check("R4 every dropped hour's load lies inside the held, incident-free hours' range", all(v <= 1.0 for v in
                                                                                             inside.values()),
          str(inside))

    # ---------------------------------------------------------------- R5 no one thing: footprints
    S_own_gold = g.slis(w_own, ex, fill=fill_of(w_own, ex))
    shifts = {s: round(S[s]["sli"] - S_own_gold[s]["sli"], 3) for s in K.INTERNAL}
    check("R5 the root weights move every internal service's SLI by 0.1 or more, in both directions",
          all(abs(v) >= 0.1 for v in shifts.values()) and min(shifts.values()) < 0 < max(shifts.values()),
          str(shifts))
    held_shift = {s: round(Sw[s]["sli"] - S[s]["sli"], 3) for s in K.SVC}
    check("R5 the dropped hours move six or more services' one-decimal SLIs, the deciding one among them",
          sum(K.r1(Sw[s]["sli"]) != gold1[s] for s in K.SVC) >= 6, str(held_shift))
    eff = json.load(open(os.path.join(HERE, "effort.json")))
    worst = max(len(h["rescues"]) for h in eff["hints"])
    check("R5 no single correction rescues more than a third of the results", worst <= len(eff["results"]) / 3.0,
          "; ".join("%s: %s" % (h["sentence"][:48], ",".join(h["rescues"]) or "none") for h in eff["hints"]))

    # ---------------------------------------------------------------- R7 rivals inside each band
    w_sh = g.weights("root_span_hour")
    w_drop = wr.copy()
    for i in np.nonzero(g.dec)[0]:
        if g.tr[i] not in g.root_of:
            w_drop[i] = 0.0
    F_g = R["fill"]
    for lab, S_r in (("Horvitz-Thompson on the balancer's count", g.slis(wr, ex, ht=True, fill=F_g)),
                     ("the root's share at the span's own hour", g.slis(w_sh, ex, fill=fill_of(w_sh, ex))),
                     ("spans of traces begun before the export dropped", g.slis(w_drop, ex, fill=fill_of(w_drop, ex)))):
        check("R7 %s gives every one-decimal SLI" % lab, r1set(S_r) == gold1,
              str({s: K.r1(S_r[s]["sli"]) for s in K.SVC if K.r1(S_r[s]["sli"]) != gold1[s]}))
    for form in ("bands20", "isotonic", "logit2", "called"):
        S_r = g.slis(wr, ex, fill=fill_of(wr, ex, form))
        check("R7 the dropped hours filled by %s give every one-decimal SLI" % form, r1set(S_r) == gold1,
              str({s: round(S_r[s]["sli"], 3) for s in K.SVC if K.r1(S_r[s]["sli"]) != gold1[s]}))
    # a share linear in log load is rejected by the held hours themselves: the bend at the busiest hours
    from scipy.special import expit
    rej = {}
    for s in K.SVC:
        O, C = g.hourly(s, wr, ex)
        fit = (hrs >= cut) & quiet & (C > 0)
        x = np.log(g.N[s] + 1)[fit]
        dev = []
        for X in (np.column_stack([np.ones(len(x)), x]), np.column_stack([np.ones(len(x)), x, x ** 2])):
            b = g._logit_fit(X, O[fit], C[fit])
            p_ = np.clip(expit(X @ b), 1e-12, 1 - 1e-12)
            dev.append(-2 * float((O[fit] * np.log(p_) + (C[fit] - O[fit]) * np.log(1 - p_)).sum()))
        rej[s] = round(dev[0] - dev[1], 1)
    S_lin = g.slis(wr, ex, fill=fill_of(wr, ex, "logit"))
    lin_off = [s for s in K.SVC if K.r1(S_lin[s]["sli"]) != gold1[s]]
    check("R7 a share linear in log load is rejected wherever it would move a cell (curvature, chi-square 1 df, 1 per "
          "cent)", all(rej[s] > 6.63 for s in lin_off), "moves %s; deviance drop %s" % (
              ", ".join(lin_off) or "none", {s: rej[s] for s in lin_off}))
    for lab, lead in (("two", 2), ("four", 4)):
        q2 = np.ones(AN.H, dtype=bool)
        for x in dec:
            a_ = int(AN.sec_of(x["declared"]) // 3600) - lead
            b_ = int(AN.sec_of(x["end"]) // 3600) + 1
            q2[max(0, a_):min(AN.H, b_ + 1)] = False
        g.quiet_hours = lambda incs=None, _q=q2: _q
        S_r = g.slis(wr, ex, fill=fill_of(wr, ex))
        del g.quiet_hours
        check("R7 the fill fitted on hours clear of incidents from %s hours before gives every one-decimal SLI" % lab,
              r1set(S_r) == gold1, str({s: round(S_r[s]["sli"], 3) for s in K.SVC if K.r1(S_r[s]["sli"]) != gold1[s]}))
    # the fill earns its place out of sample: fitted from 18 December, predicting the export's own 12 to 17 December
    def bt_err(method):
        bt = g.backtest(method, wr, ex, dec)
        return float(np.mean([abs(np.log(max(p_, 1e-6 * o_ + 1e-9) / o_)) for p_, o_ in bt.values() if o_ > 0]))
    e_gold = bt_err(AN.FILL)
    rivals = {m: bt_err(m) for m in ("weekday-hour", "hour", "daytype-hour", "flat", "load+hour")}
    check("R7 the load bands beat every load-free match and the hour-adjusted model out of sample by a quarter or more",
          all(v >= 1.33 * e_gold for v in rivals.values()), "mean |log error| bands %.3f; %s" % (
              e_gold, ", ".join("%s %.3f" % (k, v) for k, v in rivals.items())))
    agg = {m: (lambda bt: sum(v[0] for v in bt.values()) / sum(v[1] for v in bt.values()))(g.backtest(m, wr, ex, dec))
           for m in (AN.FILL, "weekday-hour", "hour", "daytype-hour", "flat")}
    check("R7 summed over the services, the load bands predict the held-out days closest to what was seen",
          all(abs(np.log(agg[AN.FILL])) < abs(np.log(v)) for k, v in agg.items() if k != AN.FILL),
          ", ".join("%s %.2f" % (k, v) for k, v in agg.items()))
    S_wh = R["weekday_hour"]["S"]
    check("R7 the same-weekday-and-hour fill, the natural load-free one, puts journey-search over (a hurried route)",
          "journey-search" in over_of(S_wh, R["bud"]), "journey-search %.3f" % S_wh["journey-search"]["sli"])
    # the onsets: every rival detector, calibrated on placebo windows (each incident's window moved by whole days onto
    # the export's incident-free stretches), names the same seven owners
    curves = g.load_curves(dec)

    def series(x, s_):
        a0, b0 = AN.sec_of(x["declared"]) - 3 * 3600, AN.sec_of(x["end"])
        out = []
        for (ss, n_), cf in curves.items():
            if ss != s_:
                continue
            m_ = g.dec & (g.svc == s_) & (g.name == n_) & (g.t0 >= a0) & (g.t0 < b0)
            if m_.sum() < 20:
                continue
            o_ = np.argsort(g.t0[m_])
            out.append((g.t0[m_][o_], (np.log(g.own[m_]) - np.polyval(cf, np.log(g.N[s_][g.h[m_]] + 1)))[o_]))
        return out

    def shifted(x, days):
        y = dict(x)
        y["declared"] = x["declared"] + dt.timedelta(days=days)
        y["end"] = x["end"] + dt.timedelta(days=days)
        a0, b0 = int(AN.sec_of(y["declared"]) // 3600) - 3, int(AN.sec_of(y["end"]) // 3600) + 1
        return y if (a0 >= cut and b0 < AN.H and quiet[a0:b0 + 1].all()) else None

    placebos = [y for x in dec for d_ in range(-6, 7) if d_ for y in [shifted(x, d_)] if y]

    def cp(thr):
        def f(t, r):
            k_ = AN.sustained_split(t, r)
            ok = k_ and k_[2] - k_[1] >= np.log(thr) and k_[2] >= np.log(thr * AN.LEVEL / AN.RISE)
            return t[k_[0]] if ok else None
        return f

    def cp10(thr):
        def f(t, r):
            b_ = np.floor((t - t[0]) / 600).astype(int)
            u_ = np.unique(b_)
            med = np.array([np.median(r[b_ == k]) for k in u_])
            tt = np.array([t[b_ == k][0] for k in u_])
            k_ = AN.sustained_split(tt, med, min_n=3)
            ok = k_ and k_[2] - k_[1] >= np.log(thr) and k_[2] >= np.log(thr * AN.LEVEL / AN.RISE)
            return tt[k_[0]] if ok else None
        return f

    def roll(thr, minutes):
        def f(t, r):
            win = max(6, int(round(len(r) / ((t[-1] - t[0]) / 3600 + 1e-9) * minutes / 60)))
            if len(r) < 2 * win:
                return None
            med = np.array([np.median(r[j - win + 1:j + 1]) for j in range(win - 1, len(r))])
            for j in range(len(med) - win):
                if med[j] > np.log(thr) and med[j:j + win].min() > np.log(thr) * 0.65:
                    return t[j]
            return None
        return f

    def owners_of(fn, xs):
        out = {}
        for x in xs:
            firsts = {}
            for s_, _ in x["named"]:
                ts = [v for v in (fn(t, r) for t, r in series(x, s_)) if v is not None]
                if ts:
                    firsts[s_] = min(ts)
            out[x["id"]] = min(firsts, key=firsts.get) if firsts else None
        return out

    def rate(fn):
        return float(np.mean([any(v is not None for v in owners_of(fn, [y]).values()) for y in placebos]))

    fam = {"the golden's sustained changepoint": cp, "a changepoint on ten-minute medians": cp10,
           "a half-hour rolling median": lambda thr: roll(thr, 30), "an hour's rolling median": lambda thr: roll(thr, 60)}
    calib = {}
    for lab, mk in fam.items():
        for thr in (1.4, 1.6, 1.8, 2.0, 2.2):
            if rate(mk(thr)) <= 1 / 14.0:
                calib[lab] = (thr, mk(thr))
                break
    gold_rate = rate(cp(AN.RISE))
    check("R7 the golden's onset rule fires on one placebo window in fourteen or fewer",
          gold_rate <= 1 / 14.0 + 1e-9, "%d placebo windows, %.0f%% fire" % (len(placebos), 100 * gold_rate))
    disagree = {}
    for lab, (thr, fn) in calib.items():
        o_ = owners_of(fn, dec)                       # a detector that sees no rise at all abstains
        wrong = {k: v for k, v in o_.items() if v is not None and v != att[k]}
        if wrong:
            disagree[lab] = wrong
    check("R7 every rival onset detector, calibrated on the placebo windows, names the same seven owners",
          len(calib) == len(fam) and not disagree, "; ".join("%s at x%.1f" % (k, v[0]) for k, v in calib.items()) +
          ("" if not disagree else " | disagree: %s" % disagree))
    for lab, kw in (("a two-hour lead", {"lead_min": 120}), ("a four-hour lead", {"lead_min": 240})):
        alt = {x["id"]: (lambda on: min((s_ for s_, v in on.items() if v), key=lambda s_: on[s_][0]))(
            g.onsets(x, curves, **kw)) for x in dec}
        check("R7 the onset read over %s puts every incident on the same service" % lab, alt == att, str(alt))
    lin = {s: (R["ci"][s][0], R["ci"][s][1]) for s in GOLD}
    boot = R["ci_boot"]
    check("R7 the trace bootstrap with the fill refitted agrees with the linearised interval to 0.04 at both ends",
          all(abs(lin[s][0] - boot[s][0]) <= 0.04 and abs(lin[s][1] - boot[s][1]) <= 0.04 for s in GOLD),
          str({s: (round(lin[s][0], 2), round(boot[s][0], 2), round(lin[s][1], 2), round(boot[s][1], 2)) for s in GOLD}))

    # ---------------------------------------------------------------- margins
    dist = {s: round(min(abs(S[s]["sli"] - (np.floor(S[s]["sli"] * 10) / 10 + 0.05)),
                         abs(S[s]["sli"] - (np.floor(S[s]["sli"] * 10) / 10 - 0.05))), 3) for s in K.SVC}
    check("M1 every SLI 0.01 or more from a rounding line", min(dist.values()) >= 0.01, str(dist))
    vmarg = {s: round(S[s]["sli"] - (R["bud"][s] + 0.05), 3) for s in K.SVC}
    check("M2 every verdict 0.1 or more from its budget line", all(abs(v) >= 0.1 for v in vmarg.values()), str(vmarg))
    check("M3 the five's order holds by a tenth of the next service's count",
          all(S[a]["over_requests"] >= 1.1 * S[b]["over_requests"] for a, b in zip(P["order"], P["order"][1:])),
          ", ".join("%s %.0f" % (s, S[s]["over_requests"]) for s in P["order"]))

    # ---------------------------------------------------------------- the semantic fork rows
    check("SF1 December in Lisbon time is UTC: no span moves between days", True, "PR-SLO-3 3.1; WET all month")
    check("SF2 over threshold is strictly greater", sum(1 for i in np.nonzero(g.dec)[0]
                                                       if g.ms[i] == g.thr[g.svc[i]]) == 0, "no span on a threshold")
    check("SF3 a re-sent span id counts once", True, "R2 above")
    check("SF4 the balancer's probes are not requests", not any(g.name == "GET /healthz"),
          "PR-SLO-3 2.2; the edge sampler never sees a probe, so the export carries none")
    check("SF5 a retried call is a request", True, "PR-SLO-3 2.2: any call a caller sent")
    check("SF6 errors count like any request", True, "PR-SLO-3 2.4")
    check("SF7 a request belongs to the time its service started it", True, "PR-SLO-3 2.4")
    check("SF8 the weighting base (balancer count or weighted kept count)", True, "R7 above: same one decimal")
    check("SF9 the root's hour or the span's own hour", True, "R7 above")
    check("SF10 spans of traces begun before the export", True, "R7 above")
    check("SF11 a symptom's window starts when the timeline adds it", True, "PR-SLO-3 3.2; R2 above for the SLIs")
    check("SF12 an incident ends when the status page shows its last component operational",
          all(x["end"] <= x["resolved"] for x in dec), "PR-SLO-3 3.2 and 5.2")
    check("SF13 a December incident with no status post leaves nothing out", len([x for x in incs if x["declared"] >=
                                                                                 AN.DEC0]) == 7, "PR-SLO-3 5.2")
    check("SF14 the onset's lead window", True, "R7 above")
    check("SF15 shares are of the over-threshold requests all the SLIs count", abs(sum(P["share"].values()) - 100)
          < 1e-6, "the base is the ten SLIs' numerators")
    check("SF16 the interval's method (linearised against bootstrapped)", True, "R7 above")
    # an onset is stated to the nearest five minutes: the rounding keeps every pair of rises in its order, ten minutes
    # or more apart, so a time read a few minutes either way grades the same
    gaps = []
    for x in dec:
        on = R["onset"][x["id"]]
        f = att[x["id"]]
        for s_, v in on.items():
            if s_ != f and v:
                a5 = D.about((AN.DEC0 + __import__("datetime").timedelta(seconds=on[f][0])).strftime("%H:%M"))
                b5 = D.about((AN.DEC0 + __import__("datetime").timedelta(seconds=v[0])).strftime("%H:%M"))
                gaps.append((x["id"], a5, b5))
    check("SF19 an onset stated to five minutes keeps each cause's rise ten minutes or more before the others'",
          all((int(b[:2]) * 60 + int(b[3:])) - (int(a[:2]) * 60 + int(a[3:])) >= 10 for _, a, b in gaps),
          "; ".join("%s %s before %s" % g for g in gaps))

    check("SF20 December's hours the store had dropped count, at the share each service's load gives them", True,
          "PR-SLO-3 2.2 (kept or not) and 3.1 (December); R3 and R7 above")
    check("SF21 the fill's form (load bands, isotonic, a curved logit, the called services' loads)", True, "R7 above")
    check("SF22 the export begins on a whole hour", True, "R4 above")
    check("SF23 how an onset is dated: every placebo-calibrated detector names the same owners or abstains", True,
          "R7 above")

    # ---------------------------------------------------------------- the documents
    slo = text_of(os.path.join(target, K.FILES["slo"]))
    check("DOC1 the standard files the incident clause (positive control)", "owned the incident's root cause" in slo
          and "does not." in slo, "")
    check("DOC2 the standard names no method for finding the cause", not re.search(
        r"self.time|own handling time|changepoint|onset|first to slow|load curve|trace", slo.split("3.2")[1].split("3.4")[0],
        re.I), "")
    check("DOC3 no December review records a cause", all(not x["cause"] for x in dec), "")
    check("DOC4 the standard says nothing of the tracing store's retention", not re.search(
        r"31 days|retain|retention|the tracing store holds|expire", slo, re.I), "")
    print("%d checks failed" % len(FAILS) if FAILS else "all checks passed")
    return len(FAILS)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    sys.exit(main(tgt))
