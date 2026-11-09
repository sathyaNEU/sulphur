"""task10 architecture 5: the generator's assertions, on the cut pack (target/) and on the clean truth.
python3 task10/generator/checks.py

Every semantic fork row of the design note (SF1 to SF22) is asserted by its id; the ladder's rungs, the margins, the
Sulfur block (the analyst test on the clean truth, the deep chain, the one-fact test, the rivals), Layer 1 neutrality,
the data-native facts, the input gates, the realism sweep, distractor deletion and the container gate follow."""
import contextlib
import copy
import datetime as dt
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import estim as E          # noqa: E402
import golden as GO        # noqa: E402
import pack as PK          # noqa: E402
import parse as PA         # noqa: E402
import world as W          # noqa: E402

CALL = ["Ashcombe Road", "Hartwell Common"]
RESULTS = []


def check(cid, ok, detail):
    RESULTS.append((cid, bool(ok), detail))
    print("%-4s %-34s %s" % ("PASS" if ok else "FAIL", cid, detail))


@contextlib.contextmanager
def patched(name, fn):
    old = getattr(E, name)
    setattr(E, name, fn)
    try:
        yield
    finally:
        setattr(E, name, old)


def graded(G):
    """The figures the prompt grades, at its rounding: delivery to one decimal, credited and after in whole MW, over."""
    return {z["primary"]: (round(z["delivery"], 1), int(round(z["credited"])), int(round(z["after"])), bool(z["over"]))
            for z in G["zones"]}


def recompute(G, delivery):
    """A route's call: each zone credited at the route's delivery per MW scheduled."""
    G = copy.deepcopy(G)
    for z in G["zones"]:
        z["delivery"] = delivery(z)
        z["credited"] = z["delivery"] * z["mw28"]
        z["after"] = z["before"] - z["credited"]
        z["over"] = z["after"] > z["firm"]
    G["commit"] = [z["primary"] for z in G["zones"] if z["over"]]
    return G


def fresh():
    return PA.load(TARGET)


def clean_truth():
    """The world before any mess or document: the metered demand, the events and the weather as the analyst's tables,
    with the registers' facts taken from the world itself."""
    T = W.build()
    ct = W.tables(T)
    links = {}
    for _, a, b in PK.NOPS:
        links.setdefault(W.BY[a]["code"], set()).add(W.BY[b]["code"])
        links.setdefault(W.BY[b]["code"], set()).add(W.BY[a]["code"])
    return dict(demand=ct["demand"], events=ct["events"], weather=ct["weather"],
                names={p["code"]: p["name"] for p in W.PRIMARIES},
                rates={p["code"]: PK.dfes_rates(p["key"]) for p in W.PRIMARIES}, links=links,
                growth={p["code"]: W.REGISTER_MW[p["key"]] for p in W.PRIMARIES},
                firm={p["code"]: p["firm"] for p in W.PRIMARIES},
                contracts={W.BY[z["key"]]["name"]: z["mw28"] for z in W.ZONES})


def routes(X, G):
    """Every rung of the ladder on one set of tables: name -> the route's golden-shaped result."""
    prep, tm, ev = X["_prep"], E.daily_mean(X["weather"]), X["events"]
    rec = {}
    for z in G["zones"]:
        code, lk = z["code"], z["linked_code"]
        base = E.delivery_records(prep, tm, ev, code)
        rec[code] = dict(base=base,
                         net=E.delivery_records(prep, tm, ev, code, partner=lk) if lk else base,
                         did=E.delivery_records(prep, tm, ev, code, partner=lk, partner_clean=False) if lk else base,
                         cbl=E.delivery_records(prep, tm, ev, code, method="cbl"),
                         pair=E.pair_records(prep, tm, ev, code, lk) if lk else base)
    R = {
        "rung 0a no flexibility": recompute(G, lambda z: 0.0),
        "rung 0b face value": recompute(G, lambda z: 1.0),
        "rung 0c unadjusted CBL": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["cbl"], net=False,
                                                                        temperature=False)),
        "rung 1 default": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["base"], net=False, temperature=False)),
        "rung 1b zone fall at -3 C": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["base"], net=False)),
        "rung 2 neighbour as control": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["did"], net=False,
                                                                             did=True, temperature=False)),
        "rung 2b neighbour as control at -3 C": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["did"], net=False,
                                                                                      did=True)),
        "rung 3 net at the average event day": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["net"],
                                                                                     temperature=False)),
        "rung 3a pair at the average event day": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["pair"], net=False,
                                                                                       temperature=False)),
        "rung 4 golden": G,
        "rung 4a pair at -3 C": recompute(G, lambda z: E.delivery_at(rec[z["code"]]["pair"], net=False)),
    }
    return R, rec


def main():
    X = fresh()
    G = E.golden_from(X)
    g = graded(G)
    tm = E.daily_mean(X["weather"])

    # ------------------------------------------------------------------------------------------------ the call
    check("call", G["commit"] == CALL, "commit %s" % G["commit"])
    edge = lambda v: abs(v % 1 - 0.5)               # distance to the nearest whole-MW rounding edge
    edge1 = lambda v: abs((v * 10) % 1 - 0.5) / 10  # distance to the nearest one-decimal rounding edge
    for z in G["zones"]:
        check("margin %s" % z["primary"][:12],
              edge1(z["delivery"]) >= 0.025 and edge(z["credited"]) >= 0.15 and edge(z["after"]) >= 0.15
              and abs(z["after"] - z["firm"]) >= 1.0,
              "delivery %.3f (%.3f from its rounding edge), credited %.2f (%.2f), after %.2f (%.2f) against firm %.1f (%+.2f)"
              % (z["delivery"], edge1(z["delivery"]), z["credited"], edge(z["credited"]), z["after"], edge(z["after"]),
                 z["firm"], z["after"] - z["firm"]))
        check("before mid-bin %s" % z["primary"][:12], edge(z["before"]) >= 0.3, "before %.2f" % z["before"])
    truth = {"Corvane Flex Ltd": W.PROVIDERS["Corvane"], "Quillon Energy Services Ltd": W.PROVIDERS["Quillon"]}
    off = max(abs(z["delivery"] - (truth[z["provider"]]["at0"] - truth[z["provider"]]["slope"] * 3.0)) for z in G["zones"])
    check("golden recovers the providers", off < 0.03, "largest gap to the world's own delivery at -3 C: %.3f" % off)

    # ------------------------------------------------------------------------------------------------ the ladder
    R, rec = routes(X, G)
    want = {"rung 0a no flexibility": ["Ashcombe Road", "Charlecote Way", "Fenwick Street", "Hartwell Common"],
            "rung 0b face value": [], "rung 0c unadjusted CBL": ["Ashcombe Road", "Charlecote Way", "Fenwick Street",
                                                                 "Hartwell Common"],
            "rung 1 default": [], "rung 1b zone fall at -3 C": ["Ashcombe Road"], "rung 2 neighbour as control": [],
            "rung 2b neighbour as control at -3 C": [], "rung 3 net at the average event day": CALL,
            "rung 3a pair at the average event day": CALL, "rung 4 golden": CALL, "rung 4a pair at -3 C": CALL}
    for k, v in want.items():
        check("ladder " + k, R[k]["commit"] == v, "files %s" % ("+".join(R[k]["commit"]) or "none"))
    avg = graded(R["rung 3 net at the average event day"])
    check("one-fact test: netting alone", all(avg[p][0] != g[p][0] for p in g) and all(avg[p][1] != g[p][1] for p in g),
          "netting without the design condition lands the call and misses every delivery and credit: %s"
          % {p[:4]: avg[p][:2] for p in avg})
    check("pair converges", graded(R["rung 4a pair at -3 C"]) == g, "the zone and its linked primary taken together")
    shallow = graded(R["rung 1 default"])
    keep = sum(shallow[p][k] == g[p][k] for p in g for k in range(4))
    check("shallow keep", keep <= 3, "the default path keeps %d of 16 ask figures" % keep)

    # ------------------------------------------------------------------------------------------------ the default's back-test
    prep = X["_prep"]
    for z in G["zones"]:
        code = z["code"]
        sched = set(X["events"][X["events"]["zone"] == code]["date"])
        tab = E.hh_table(prep, code)
        free = sorted(d for d in tab.index if E._workday(d) and d in tm.index and d not in sched)
        hold = set(free[::5])
        fall = E.baseline_excess(prep, tm, code, sorted(hold), sched | hold)
        placebo = float(np.mean([v for v in fall.values() if v is not None]))
        recs = rec[code]["base"]
        byw = {w: E.delivery_at([r for r in recs if E.WINTER_OF(r[0]) == w], net=False, temperature=False)
               for w in ("2024/25", "2025/26")}
        check("back-test %s" % z["primary"][:12], abs(placebo) < 0.15 and abs(byw["2024/25"] - byw["2025/26"]) < 0.1,
              "held-out non-event weekdays: mean fall %+.2f MW; the default's delivery by winter %.2f and %.2f per MW"
              % (placebo, byw["2024/25"], byw["2025/26"]))
    pins = ""
    for f in sorted(os.listdir(TARGET)):
        if f.endswith(".pdf"):
            pins += subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, f), "-"], capture_output=True,
                                   text=True).stdout
    pins += open(os.path.join(TASK, "prompt.txt")).read()
    hits = re.findall(r"(?i)\b(transfers?|transferred|switch\w*|neighbou?r\w*|open points?|normally.open|moved|mirror\w*|"
                      r"spill\w*|back.?feed\w*|interconnect\w*)\b", pins)
    check("pins", not hits, "the governing documents and the prompt name no transfer, neighbour, open point or switching"
          + (": %s" % sorted(set(hits)) if hits else ""))

    # ------------------------------------------------------------------------------------------------ the delivery family
    def fam_values(rr, pooled):
        T = np.array([r[1] for r in rr]); y = np.array([(r[3] - r[4]) / r[2] for r in rr]); w = np.array([r[2] for r in rr])
        Tp = np.array([r[1] for r in pooled]); yp = np.array([(r[3] - r[4]) / r[2] for r in pooled])
        pairs = [(y[j] - y[i]) / (T[j] - T[i]) for i in range(len(T)) for j in range(i + 1, len(T)) if abs(T[j] - T[i]) > 0.2]
        b = float(np.median(pairs))
        out = {"linear": np.polyval(np.polyfit(T, y, 1), -3.0), "pooled per provider": np.polyval(np.polyfit(Tp, yp, 1), -3.0),
               "quadratic": np.polyval(np.polyfit(T, y, 2), -3.0), "Theil-Sen": float(np.median(y - b * T)) - 3.0 * b,
               "weighted by MW": np.polyval(np.polyfit(T, y, 1, w=np.sqrt(w)), -3.0),
               "linear below 2 C": np.polyval(np.polyfit(T[T < 2], y[T < 2], 1), -3.0)}
        for h in (1.0, 1.5, 2.0, 2.5, 3.0):
            m = np.abs(T + 3.0) <= h
            out["mean within %.1f C" % h] = float(y[m].mean())
            out["ratio within %.1f C" % h] = float((y[m] * w[m]).sum() / w[m].sum())
        return out
    pooled = {}
    for z in G["zones"]:
        pooled.setdefault(z["provider"], []).extend(rec[z["code"]]["net"])
    def befores(z):
        """the literal guideline 3 read three ways: every scheduled day out, completed days out, the peak read at the
        credited half-hours"""
        code = z["code"]
        r1, r2 = X["rates"][code]
        grow = lambda d26: d26 * (1 + r1 / 100.0) * (1 + r2 / 100.0) + X["growth"].get(code, 0.0)
        allz = set(X["events"][X["events"]["zone"] == code]["date"])
        done = set(X["events"][(X["events"]["zone"] == code) & (X["events"]["status"] == "Completed")]["date"])
        out = [grow(E.design_peak(prep, tm, code, exclude=allz, winters=["2025/26"])[0]),
               grow(E.design_peak(prep, tm, code, exclude=done, winters=["2025/26"])[0])]
        with patched("daily_peaks", lambda p, c: p[(p["code"] == c) & (p["hh"].isin(E.CREDIT_HH))].groupby("ldate")["mw"].max()):
            out.append(grow(E.design_peak(prep, tm, code, exclude=allz, winters=["2025/26"])[0]))
        return out
    for z in G["zones"]:
        vals = fam_values(rec[z["code"]]["net"], pooled[z["provider"]])
        bs = befores(z)
        cells = {(round(v, 1), int(round(v * z["mw28"])), int(round(b - v * z["mw28"]))) for v in vals.values() for b in bs}
        lo, hi = min(vals.values()), max(vals.values())
        afters = [b - v * z["mw28"] for v in vals.values() for b in bs]
        credits = [v * z["mw28"] for v in vals.values()]
        mar = min(min(edge(a) for a in afters), min(edge(c) for c in credits))
        check("family %s" % z["primary"][:12], cells == {g[z["primary"]][:3]},
              "%d estimators of the design-day delivery (%.3f to %.3f) by %d readings of the before-demand give %s, "
              "every credit and after at least %.2f MW from its edge" % (len(vals), lo, hi, len(bs), sorted(cells), mar))

    # ------------------------------------------------------------------------------------------------ clean truth
    C = clean_truth()
    GC = E.golden_from(C)
    check("clean truth: golden", graded(GC) == g, "the golden on the world before mess: %s" % GC["commit"])
    RC, _ = routes(C, GC)
    check("analyst test (clean truth)", RC["rung 1 default"]["commit"] == [] and RC["rung 1b zone fall at -3 C"]["commit"]
          == ["Ashcombe Road"] and RC["rung 2 neighbour as control"]["commit"] == [],
          "default %s, with the design condition %s, neighbour as control %s"
          % (RC["rung 1 default"]["commit"], RC["rung 1b zone fall at -3 C"]["commit"],
             RC["rung 2 neighbour as control"]["commit"]))

    # ------------------------------------------------------------------------------------------------ data-native facts
    for z in G["zones"]:
        rises = z["rises"]
        mover = {k: v for k, v in rises.items() if v > E.MATERIAL_RISE}
        exp = {"Ashcombe Road": "PS40233", "Fenwick Street": "PS40975", "Hartwell Common": "PS40508"}.get(z["primary"])
        check("mirror %s" % z["primary"][:12], (list(mover) == [exp]) if exp else not mover,
              "neighbour rises in the credited half-hours: %s" % {X["names"][k]: round(v, 2) for k, v in rises.items()})
    check("providers fall with cold", all(p["slope"] > 0 for p in W.PROVIDERS.values()),
          "delivery per MW at 0 C less the slope per degree below")

    # ------------------------------------------------------------------------------------------------ semantic forks
    def variant(label, sid, Gv, expect_same=True, why=""):
        same = graded(Gv) == g
        check(sid, same == expect_same, "%s: %s%s" % (label, "same call and figures" if same else
                                                      "moves %s" % {p: v for p, v in graded(Gv).items() if v != g[p]},
                                                      ("; " + why) if why else ""))

    # SF1 the design day's daily mean over the GMT day, against the UK local day
    def local_mean(weather):
        w = weather.copy()
        w["date"] = [E.local_end(t.to_pydatetime() + dt.timedelta(minutes=30)).date() for t in w["t_utc"]]
        return w.groupby("date")["temp_c"].mean()
    with patched("daily_mean", local_mean):
        variant("daily mean over the UK local day", "SF1", E.golden_from(fresh()))
    # SF2 the design-day demand: the day's highest half-hour, against the credited half-hours only
    with patched("daily_peaks", lambda p, code: p[(p["code"] == code) & (p["hh"].isin(E.CREDIT_HH))]
                 .groupby("ldate")["mw"].max()):
        variant("peak read at 17:30 and 18:00 only", "SF2", E.golden_from(fresh()))
    # SF3 the correction's days: outside the scheduled days (guideline 3), against every working weekday
    dp = E.design_peak
    with patched("design_peak", lambda prep, tm_, code, exclude=(), base=E.BASE_T, winters=None, restore=None:
                 dp(prep, tm_, code, (), base, winters, restore)):
        variant("event days kept in the 2025/26 correction", "SF3", E.golden_from(fresh()), expect_same=False,
                why="ruled out by guideline 3, 'outside the days on which flexibility was scheduled in the primary's zone'")
    # SF4 the 2025/26 winter's own demand (guideline 3), against three winters pooled with winter levels
    with patched("design_peak", lambda prep, tm_, code, exclude=(), base=E.BASE_T, winters=None, restore=None:
                 dp(prep, tm_, code, exclude, base, None, restore)):
        Gv = E.golden_from(fresh())
    same4 = graded(Gv) == g
    check("SF4", Gv["commit"] == CALL, "three winters pooled: %s; guideline 3 corrects 'the primary's 2025/26 winter "
          "demand'" % ("same call and figures" if same4 else "same call, moves %s" % {p: v for p, v in graded(Gv).items()
                                                                                    if v != g[p]}))
    # SF5 to SF7 the growth register
    fmap, _ = PA.feeders(TARGET)
    rows = PA._book(os.path.join(TARGET, PK.F_GROW), "Register")

    def growth(statuses=("Accepted", "Energised"), first=False, planned=False):
        keep = {}
        for r in rows:
            if r["Status"] not in statuses or not r["Planned energisation"]:
                continue
            en = dt.datetime.strptime(r["Energised on"], "%d/%m/%Y").date() if r["Energised on"] and not planned else None
            day = en or dt.datetime.strptime(r["Planned energisation"], "%d/%m/%Y").date()
            if not (dt.date(2026, 4, 1) <= day <= dt.date(2027, 10, 31)) or (first and r["Reference"] in keep):
                continue
            keep[r["Reference"]] = (fmap[r["11 kV feeder"]], float(r["Design demand (kW)"]))
        out = {}
        for code, kw in keep.values():
            out[code] = out.get(code, 0.0) + kw / 1000.0
        return out
    check("growth parse", {k: round(v, 3) for k, v in growth().items()} == {k: round(v, 3) for k, v in X["growth"].items()},
          "the register read twice gives one growth table")
    for sid, label, kw, same, why in (
            ("SF5", "accepted offers only, the energised left out", dict(statuses=("Accepted",)), None,
             "ruled out by guideline 4, 'those already energised included'"),
            ("SF6", "a re-entered reference at its first row", dict(first=True), True, ""),
            ("SF7", "the planned date for a connection already energised", dict(planned=True), True, "")):
        Y = fresh()
        Y["growth"] = growth(**kw)
        Gv = E.golden_from(Y)
        if same is None:   # converges or not, the filed sentence decides; the call must hold either way
            check(sid, Gv["commit"] == CALL, "%s: %s; %s" % (label, "same call and figures" if graded(Gv) == g else
                                                            "same call, moves %s" % {p: v for p, v in graded(Gv).items()
                                                                                    if v != g[p]}, why))
        else:
            variant(label, sid, Gv, expect_same=same, why=why)
    # SF8 firm capacity: Appendix A against the world's own ratings
    check("SF8", all(abs(X["firm"][p["code"]] - p["firm"]) < 1e-9 and abs(PK.firm_from_nameplate(p["key"]) - p["firm"]) < 0.05
                     for p in W.PRIMARIES), "Appendix A, the nameplate rule and the world agree for all nine primaries")
    # SF9 the credited half-hours (guideline 6), against the whole event window
    be = E.baseline_excess
    with patched("baseline_excess", lambda prep, tm_, code, dates, exclude, hhs=None, base=E.BASE_T:
                 be(prep, tm_, code, dates, exclude, hhs=E.WINDOW, base=base)):
        variant("the whole event window", "SF9", E.golden_from(fresh()), expect_same=False,
                why="ruled out by guideline 6, 'in the half-hours ending 17:30 and 18:00'")
    # SF10 the MW scheduled: the instruction's latest revision, against its first
    ev = pd.read_csv(os.path.join(TARGET, PK.F_EVENTS), dtype=str)
    ev["revision"] = ev["revision"].astype(int)
    firstmw = ev[ev["revision"] == 1].set_index("instruction_ref")["scheduled_mw"].astype(float)
    last = ev.sort_values(["instruction_ref", "revision"]).groupby("instruction_ref").last()
    mp = {(r.primary_asset, dt.datetime.strptime(r.service_date, "%d/%m/%Y").date()): firstmw[ref]
          for ref, r in last.iterrows() if r.status == "Completed"}
    Y = fresh()
    Y["events"]["scheduled_mw"] = [mp.get((zz, d), m) for zz, d, m in zip(Y["events"]["zone"], Y["events"]["date"],
                                                                           Y["events"]["scheduled_mw"])]
    variant("each instruction at its first revision's MW", "SF10", E.golden_from(Y))
    # SF11 a cancelled instruction schedules nothing
    canc = last[last["status"] == "Cancelled"]
    check("SF11", len(canc) > 0 and (canc["scheduled_mw"].astype(float) == 0.0).all(),
          "%d cancelled instructions, every one at 0.0 MW in its latest revision" % len(canc))
    # SF12 the provider's reduction: net of the linked primary's rise (the decisive step), against the zone's fall
    variant("the zone's fall as the provider's reduction", "SF12", R["rung 1b zone fall at -3 C"], expect_same=False,
            why="ruled out by the linked primaries' rise in the same half-hours (the mirror rows above)")
    # SF13 the neighbour's baseline: fitted without the zone's scheduled days, against every workday
    dr = E.delivery_records
    with patched("delivery_records", lambda prep, tm_, ev_, zone, partner=None, method="regression", partner_clean=True:
                 dr(prep, tm_, ev_, zone, partner, method, False)):
        Gv = E.golden_from(fresh())
    variant("the neighbour's baseline fitted on its event days too", "SF13", Gv, expect_same=False,
            why="ruled out by the rise itself: on the zone's event days the neighbour carries the moved section")
    # SF14 the temperature: the daily mean, against the evening's, read at the design day's evening
    w = X["weather"].copy()
    w["date"] = [t.date() for t in w["t_utc"]]
    w["h"] = [t.hour for t in w["t_utc"]]
    eve = w[w["h"].isin([17, 18, 19])].groupby("date")["temp_c"].mean()
    cold = [d for d in tm.index if tm[d] < 0 and E._workday(d) and d in eve.index]
    off = float(np.mean([eve[d] - tm[d] for d in cold]))

    def evening(z, at):
        rr = [(d, float(eve[d]), mw, red, rise) for d, T, mw, red, rise in rec[z["code"]]["net"] if d in eve.index]
        return E.delivery_at(rr, at=at)
    variant("the evening's temperature, read at the design day's evening", "SF14",
            recompute(G, lambda z: evening(z, E.T_DESIGN + off)))
    check("SF14 read at -3.0", graded(recompute(G, lambda z: evening(z, E.T_DESIGN))) != g,
          "an evening regression read at -3.0 C moves the figures; ruled out by guideline 2 (the design day's evening "
          "runs %.1f C below its daily mean)" % -off)
    # SF15 the delivery's temperature form: linear, against quadratic
    da = E.delivery_at

    def quad(recs, net=True, at=E.T_DESIGN, temperature=True, did=False):
        if not temperature:
            return da(recs, net, at, temperature, did)
        y = np.array([((r[3] - r[4]) if net else r[3]) / r[2] for r in recs])
        t = np.array([r[1] for r in recs])
        c, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(t)), t, t * t]), y, rcond=None)
        return float(c[0] + c[1] * at + c[2] * at * at)
    with patched("delivery_at", quad):
        variant("delivery quadratic in temperature", "SF15", E.golden_from(fresh()))
    # SF16 the weather correction's base temperature
    for base in (14.0, 17.0, 40.0):
        variant("base %.1f C%s" % (base, " (linear)" if base == 40.0 else ""), "SF16", E.golden_from(fresh(), base=base))
    # SF17 the netting rule: the neighbour that rose, against every neighbour
    variant("every neighbour's rise netted", "SF17", E.golden_from(fresh(), linked_rule="sum"))
    # SF18 a delivery per zone, against one per provider
    byp = {}
    for z in G["zones"]:
        byp.setdefault(z["provider"], []).extend(rec[z["code"]]["net"])
    variant("one delivery per provider", "SF18", recompute(G, lambda z: E.delivery_at(byp[z["provider"]])))
    # SF19 rounding: unrounded to the end, against delivery rounded before crediting
    variant("delivery rounded before crediting", "SF19", recompute(G, lambda z: round(z["delivery"], 1)))
    # SF20 'exceeds' strictly, against at or over
    check("SF20", all(abs(z["after"] - z["firm"]) >= 1.0 for z in G["zones"]), "no primary within 1 MW of its firm capacity")
    # SF21 the MW contracted for 2027/28, against the previous winters' table
    prev = {W.BY[z["key"]]["name"]: z["mw"]["2025/26"] for z in W.ZONES}
    Gv = copy.deepcopy(G)
    for z in Gv["zones"]:
        z["mw28"] = prev[z["primary"]]
    Gv = recompute(Gv, lambda z: z["delivery"])
    check("SF21", Gv["commit"] != CALL and X["contracts"] == {k: v for k, v in
                                                             {W.BY[z["key"]]["name"]: z["mw28"] for z in W.ZONES}.items()},
          "the 2025/26 megawatts file %s; ruled out by guideline 6, 'the megawatts contracted for that winter in the "
          "contract award notice' (parsed: %s)" % (Gv["commit"], X["contracts"]))
    # SF22 the export's stamps on the UK clock as written, against the same stamps read as UTC and moved to the UK clock
    Y = fresh()
    Y["demand"] = Y["demand"].assign(t_utc=lambda d: d["t_utc"].dt.tz_convert("Europe/London").dt.tz_localize(None)
                                      .dt.tz_localize("UTC"))
    Gv = E.golden_from(Y)
    check("SF22", Gv["commit"] == CALL, "the UK-clock stamps read as UTC: %s; ruled out by the export's own column, "
          "interval_end_uk_local" % ("same call and figures" if graded(Gv) == g else "same call, moves %s"
                                     % {p: v for p, v in graded(Gv).items() if v != g[p]}))

    # ------------------------------------------------------------------------------------------------ the asks (rubric repair)
    # Each ask rides the deep step: the design-day exceedance at the primaries to reinforce, and the primaries over firm
    # capacity on the two colder working weekdays, where the providers' reduction is read at the colder day's own mean.
    TS = E.SENS_TS
    want_sens = {-6.0: ["Ashcombe Road", "Charlecote Way", "Fenwick Street", "Hartwell Common"]}
    check("ask: colder days", G["commit_sens"] == want_sens, "over firm capacity after flexibility: %s"
          % {"%.1f C" % t: "+".join(v) for t, v in G["commit_sens"].items()})
    ob = {z["primary"]: z["over_by"] for z in G["zones"] if z["over"]}
    check("ask: exceedance", {p: int(round(v)) for p, v in ob.items()} == {"Ashcombe Road": 3, "Hartwell Common": 2}
          and all(edge(v) >= 0.15 for v in ob.values()),
          "how far each primary to reinforce exceeds firm: %s" % {p: "%.2f (%.2f from its edge)" % (v, edge(v))
                                                                  for p, v in ob.items()})
    gap = {(z["primary"], t): z["sens"][t]["after"] - z["firm"] for z in G["zones"] for t in TS}
    check("ask: colder-day margins", all(abs(v) >= 0.25 for v in gap.values()),
          "after less firm at the colder days, nearest %s at %+.2f MW" % min(((k, v) for k, v in gap.items()),
                                                                              key=lambda kv: abs(kv[1])))

    def before_at(z, T, d26=None, slope=None, ungrown=False):
        d26 = z["d26"] if d26 is None else d26
        slope = z["slope"] if slope is None else slope
        r1, r2 = X["rates"][z["code"]]
        g_ = (1 + r1 / 100.0) * (1 + r2 / 100.0)
        if ungrown:   # the design-day demand moved by the 2025/26 slope alone
            return z["before"] + slope * (max(0.0, E.BASE_T - T) - max(0.0, E.BASE_T - E.T_DESIGN))
        return (d26 + slope * (max(0.0, E.BASE_T - T) - max(0.0, E.BASE_T - E.T_DESIGN))) * g_ + X["growth"].get(z["code"], 0.0)

    def colder(deliv, before=before_at):
        return {T: [z["primary"] for z in G["zones"] if before(z, T) - deliv(z, T) * z["mw28"] > z["firm"]] for T in TS}

    # the routes the ladder names, carried to the colder days
    def fit_at(recs, net, did=False):
        y = np.array([((r[3] - r[4]) if net else (r[3] + r[4] if did else r[3])) / r[2] for r in recs])
        t_ = np.array([r[1] for r in recs])
        c = np.polyfit(t_, y, 1)
        return lambda T: float(np.polyval(c, T))
    mean_of = lambda recs, net, did=False: float(np.mean([((r[3] - r[4]) if net else (r[3] + r[4] if did else r[3])) / r[2]
                                                          for r in recs]))
    sh = {
        "rung 1 default": colder(lambda z, T: mean_of(rec[z["code"]]["base"], False)),
        "rung 1b zone fall at the day": colder(lambda z, T: fit_at(rec[z["code"]]["base"], False)(T)),
        "rung 2 neighbour as control": colder(lambda z, T: mean_of(rec[z["code"]]["did"], False, True)),
        "rung 2b neighbour as control at the day": colder(lambda z, T: fit_at(rec[z["code"]]["did"], False, True)(T)),
        "rung 3 net at the average event day": colder(lambda z, T: mean_of(rec[z["code"]]["net"], True)),
        "the design day's credit held": colder(lambda z, T: z["delivery"]),
    }
    with patched("delivery_records", lambda prep, tm_, ev_, zone, partner=None, method="regression", partner_clean=True:
                 dr(prep, tm_, ev_, zone, partner, method, False)):
        Gd = E.golden_from(fresh())
    sh["the neighbour's baseline on every workday"] = Gd["commit_sens"]
    for k, v in sh.items():
        check("ask miss: " + k[:28], all(v[t] != want_sens[t] for t in TS),
              "files %s" % {"%.1f C" % t: "+".join(v[t]) or "none" for t in TS})
    keep_ = colder(lambda z, T: fit_at(rec[z["code"]]["pair"], False)(T))
    check("ask keep: the pair taken together", keep_ == want_sens, "the zone and its linked primary taken together at the "
          "colder days: %s" % {"%.1f C" % t: "+".join(v) for t, v in keep_.items()})
    byp_fit = {pv: fit_at(rr, True) for pv, rr in byp.items()}
    keep_ = colder(lambda z, T: byp_fit[z["provider"]](T))
    check("ask keep: one delivery per provider", keep_ == want_sens, "%s" % {"%.1f C" % t: "+".join(v)
                                                                             for t, v in keep_.items()})
    # the delivery family (16 estimators) by the three readings of guideline 3, at each colder day
    def fam_fns(rr, pooled_):
        T_ = np.array([r[1] for r in rr]); y = np.array([(r[3] - r[4]) / r[2] for r in rr]); w = np.array([r[2] for r in rr])
        Tp = np.array([r[1] for r in pooled_]); yp = np.array([(r[3] - r[4]) / r[2] for r in pooled_])
        pairs = [(y[j] - y[i]) / (T_[j] - T_[i]) for i in range(len(T_)) for j in range(i + 1, len(T_))
                 if abs(T_[j] - T_[i]) > 0.2]
        b = float(np.median(pairs)); a = float(np.median(y - b * T_))
        late = np.array([E.WINTER_OF(r[0]) == "2025/26" for r in rr])
        latep = np.array([E.WINTER_OF(r[0]) == "2025/26" for r in pooled_])
        return {"linear": np.poly1d(np.polyfit(T_, y, 1)), "pooled per provider": np.poly1d(np.polyfit(Tp, yp, 1)),
                "2025/26 events only": np.poly1d(np.polyfit(T_[late], y[late], 1)),
                "2025/26 events only, pooled": np.poly1d(np.polyfit(Tp[latep], yp[latep], 1)),
                "quadratic": np.poly1d(np.polyfit(T_, y, 2)), "pooled quadratic": np.poly1d(np.polyfit(Tp, yp, 2)),
                "Theil-Sen": np.poly1d([b, a]), "weighted by MW": np.poly1d(np.polyfit(T_, y, 1, w=np.sqrt(w))),
                "linear below 2 C": np.poly1d(np.polyfit(T_[T_ < 2], y[T_ < 2], 1)),
                "linear below 0 C": np.poly1d(np.polyfit(T_[T_ < 0], y[T_ < 0], 1))}

    def readings(z):
        code = z["code"]
        allz = set(X["events"][X["events"]["zone"] == code]["date"])
        done = set(X["events"][(X["events"]["zone"] == code) & (X["events"]["status"] == "Completed")]["date"])
        out = [E.design_peak(prep, tm, code, exclude=allz, winters=["2025/26"]),
               E.design_peak(prep, tm, code, exclude=done, winters=["2025/26"])]
        with patched("daily_peaks", lambda p, c: p[(p["code"] == c) & (p["hh"].isin(E.CREDIT_HH))].groupby("ldate")["mw"].max()):
            out.append(E.design_peak(prep, tm, code, exclude=allz, winters=["2025/26"]))
        return out
    worst = {}
    for z in G["zones"]:
        fns = fam_fns(rec[z["code"]]["net"], pooled[z["provider"]])
        for d26_, sl_ in readings(z):
            for nm, f in fns.items():
                for t in TS:
                    m = before_at(z, t, d26_, sl_) - float(f(t)) * z["mw28"] - z["firm"]
                    k = (z["primary"], t)
                    if k not in worst or abs(m) < abs(worst[k][0]):
                        worst[k] = (m, nm)
    # the quadratic correction (ruled out by winter 2023/24, SF24) read at the colder day all the same
    for z in G["zones"]:
        code = z["code"]
        allz = set(X["events"][X["events"]["zone"] == code]["date"])
        pk = E.daily_peaks(prep, code)
        dd = [d for d in pk.index if E._workday(d) and d in tm.index and d not in allz and E.WINTER_OF(d) == "2025/26"]
        cq = np.polyfit([tm[d] for d in dd], [pk[d] for d in dd], 2)
        r1, r2 = X["rates"][code]
        fns = fam_fns(rec[code]["net"], pooled[z["provider"]])
        for nm, f in fns.items():
            for t in TS:
                m = (np.polyval(cq, t) * (1 + r1 / 100.0) * (1 + r2 / 100.0) + X["growth"].get(code, 0.0)
                     - float(f(t)) * z["mw28"] - z["firm"])
                k = (z["primary"], t)
                if abs(m) < abs(worst[k][0]):
                    worst[k] = (m, nm + ", quadratic correction")
    flip = [k for k, (m, _) in worst.items() if (m > 0) != (gap[k] > 0)]
    check("ask: colder-day family", not flip and all(abs(m) >= 0.2 for m, _ in worst.values()),
          "%d estimators by 3 readings of guideline 3 and the quadratic correction keep every zone on its side of firm at "
          "the colder day; nearest %s"
          % (len(fns), min(((k, round(m, 2), nm) for k, (m, nm) in worst.items()), key=lambda r: abs(r[1]))))
    # SF23 the colder days' credit: the reduction the provider delivers on that day, against the design day's held
    check("SF23", sh["the design day's credit held"] == {-6.0: ["Ashcombe Road", "Fenwick Street", "Hartwell Common"]},
          "the design day's credit carried to the colder days files %s; ruled out by guideline 6 (the reduction the provider "
          "will deliver on the day) and the providers' net reduction falling with cold (slopes %s per degree)"
          % ({"%.1f C" % t: "+".join(v) for t, v in sh["the design day's credit held"].items()},
             {pv: round(float(np.polyfit([r[1] for r in rr], [(r[3] - r[4]) / r[2] for r in rr], 1)[0]), 4)
              for pv, rr in byp.items()}))
    # SF24 the correction's form: straight below the base, against quadratic in the daily mean
    fc = E.form_check(X, G["zones"])
    check("SF24", all(abs(v["linear"]) < abs(v["quadratic"]) for v in fc.values())
          and max(abs(v["linear"]) for v in fc.values()) < 0.25,
          "winter 2023/24 (no flexibility), fitted on its working weekdays above each zone's 2025/26 coldest and read on "
          "its sub-zero ones: linear %s, quadratic %s MW; the quadratic is ruled out by that winter"
          % ({p[:9]: round(v["linear"], 2) for p, v in fc.items()}, {p[:9]: round(v["quadratic"], 2) for p, v in fc.items()}))
    # SF25 the colder days' before-demand: the correction read at the day and grown, against the 2025/26 slope ungrown
    v25 = colder(lambda z, T: z["sens"][T]["delivery"], before=lambda z, T: before_at(z, T, ungrown=True))
    check("SF25", v25 == want_sens, "the design-day demand moved by the 2025/26 slope alone: %s"
          % {"%.1f C" % t: "+".join(v) for t, v in v25.items()})
    # SF26 "exceed" on the colder days: strictly, against at or over (no zone near firm under any estimator)
    check("SF26", all(abs(v) >= 0.4 for v in gap.values()) and all(abs(m) >= 0.25 for m, _ in worst.values()),
          "nearest zone to firm at the colder days %.2f MW on the golden, %.2f across the family: the same sets either way"
          % (min(abs(v) for v in gap.values()), min(abs(m) for m, _ in worst.values())))
    # SF27 the exceedance from the rounded figures, against the unrounded
    check("SF27", all(int(round(round(z["after"]) - z["firm"])) == int(round(z["over_by"])) for z in G["zones"] if z["over"]),
          "the rounded after less firm gives the same whole MW")
    # SF28 the colder days' daily mean over the UK local day
    with patched("daily_mean", local_mean):
        Gl = E.golden_from(fresh())
    check("SF28", Gl["commit_sens"] == want_sens, "daily mean over the UK local day: %s"
          % {"%.1f C" % t: "+".join(v) for t, v in Gl["commit_sens"].items()})
    # the gross route read at the design day, which the write-up's closing names: Ashcombe Road alone
    g1b = sh["rung 1b zone fall at the day"]
    fall_call = [z["primary"] for z in G["zones"]
                 if z["before"] - fit_at(rec[z["code"]]["base"], False)(E.T_DESIGN) * z["mw28"] > z["firm"]]
    check("closing: the zone's fall at the design day", fall_call == ["Ashcombe Road"] and
          "Fenwick Street" not in g1b[-6.0], "files %s at minus 3.0 C and leaves Fenwick Street within firm at minus 6.0 C (%s)"
          % (fall_call, "+".join(g1b[-6.0])))
    # the growth register records no acceptance after its own last save
    acc = [dt.datetime.strptime(r["Offer accepted"], "%d/%m/%Y").date() for r in rows if r["Offer accepted"]]
    check("realism: register dates", max(acc) <= dt.date(2026, 10, 30), "latest offer accepted %s; the register saved "
          "30 October 2026" % max(acc))
    check("ask: clean truth", GC["commit_sens"] == want_sens, "the colder days on the world before mess: %s"
          % {"%.1f C" % t: "+".join(v) for t, v in GC["commit_sens"].items()})

    # ------------------------------------------------------------------------------------------------ Layer 1 neutrality
    raw = pd.read_csv(os.path.join(TARGET, PK.F_SCADA), dtype={"quality": str})
    pmap, names, rates = PA.register(TARGET)

    def demand_from(df):
        d = df.copy()
        d["code"] = d["point"].map(pmap)
        d["t_utc"] = pd.to_datetime(d["interval_end_uk_local"]).dt.tz_localize("Europe/London").dt.tz_convert("UTC")
        d = d.rename(columns={"value_mw": "mw"})[["code", "t_utc", "mw"]].dropna(subset=["code"])
        return d.drop_duplicates(subset=["code", "t_utc"], keep="last").sort_values(["code", "t_utc"]).reset_index(drop=True)
    Y = fresh()
    Y["demand"] = demand_from(raw[raw["quality"].isin(["G", "S"])])
    variant("held (S) values kept", "L1 held values", E.golden_from(Y))
    Y = fresh()
    legacy = set(p["legacy"] for p in W.PRIMARIES)
    Y["demand"] = demand_from(raw[(raw["quality"] == "G") & ~raw["point"].isin(legacy)])
    variant("pre-migration rows lost (legacy names unmapped)", "L1 legacy names", E.golden_from(Y))
    Y = fresh()
    wv = pd.read_csv(os.path.join(TARGET, PK.F_WX))
    wv["t_utc"] = pd.to_datetime(wv["ob_end_time"], utc=True)
    Y["weather"] = wv.rename(columns={"air_temperature": "temp_c"})[["t_utc", "temp_c"]]
    variant("every weather row kept, raw and checked versions averaged in", "L1 weather versions", E.golden_from(Y))
    dup = raw.duplicated(subset=["point", "interval_end_uk_local"]).sum()
    check("L1 re-sent overlap", dup > 0 and len(X["demand"]) == len(X["demand"].drop_duplicates(subset=["code", "t_utc"])),
          "%d rows of the December 2024 extract re-sent; each half-hour kept once" % dup)

    # ------------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    check("inputs: files", len(files) >= 10 and {".csv", ".xlsx", ".pdf"} <= exts, "%d files: %s" % (len(files), sorted(exts)))
    n_scada = sum(1 for _ in open(os.path.join(TARGET, PK.F_SCADA))) - 1
    n_wx = sum(1 for _ in open(os.path.join(TARGET, PK.F_WX))) - 1
    wxv = pd.read_csv(os.path.join(TARGET, PK.F_WX))
    check("inputs: large CSVs", n_scada >= 20000 and n_wx >= 500 and (wxv["version_num"] == 0).sum() > 0,
          "SCADA %d rows (point renames, held and bad values, gaps, a re-sent extract); weather %d rows, about %d printed "
          "pages at 50 lines (logger gaps, %d raw readings beside their checked versions)"
          % (n_scada, n_wx, n_wx // 50, (wxv["version_num"] == 0).sum()))
    src = "".join(open(os.path.join(HERE, f)).read() for f in ("parse.py", "estim.py"))
    check("distractors unread", all(f not in src for f in PK.DISTRACTORS) and len(PK.DISTRACTORS) >= 2,
          "%s never opened by the golden's code" % ", ".join(PK.DISTRACTORS))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("metadata.json", sorted(f["path"] for f in meta["files"]) == sorted("target/" + f for f in files)
          and set(meta["distractor_files"]) == {"target/" + f for f in PK.DISTRACTORS}, "provenance for every file")
    check("no describing file", not any(re.search(r"readme|dictionary|notes|manifest|codebook|schema", f, re.I)
                                        for f in files), "no file whose job is to describe the data")

    # ------------------------------------------------------------------------------------------------ realism
    counts = X["events"][X["events"]["status"] == "Completed"].assign(w=lambda d: [E.WINTER_OF(x) for x in d["date"]]) \
        .groupby(["zone", "w"]).size()
    check("realism: event counts", counts.nunique() == len(counts), "per zone and winter: %s" % counts.to_dict())
    text = ""
    for f in files:
        if f.endswith(".pdf"):
            text += subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, f), "-"], capture_output=True,
                                   text=True).stdout
    people = set(re.findall(r"(?<!Appendix )\b(Marion Todd|Clifford Evans|Irene Carpenter|[A-Z]\. [A-Z][a-z]+)\b", text))
    check("realism: personas", people <= {"Marion Todd", "Clifford Evans", "Irene Carpenter", "C. Evans"},
          "people named in the documents: %s" % sorted(people))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("no em dashes", "—" not in text and "—" not in sub, "documents and submission")

    # ------------------------------------------------------------------------------------------------ deliverables
    gz = zipfile.ZipFile(os.path.join(TASK, "golden.zip"))
    check("golden zip", sorted(gz.namelist()) == sorted([GO.F_XLSX, GO.F_PPTX]), "%s" % gz.namelist())
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    check("figures.json", fig["call"] == CALL and fig["default_call"] == [], "call %s, default %s" % (fig["call"],
                                                                                                     fig["default_call"]))
    r = subprocess.run([sys.executable, os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/audit_containers.py"),
                        TASK], capture_output=True, text=True)
    check("container gate", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])

    bad = [c for c, ok, _ in RESULTS if not ok]
    print("\n%d checks, %d failed%s" % (len(RESULTS), len(bad), (": " + ", ".join(bad)) if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
