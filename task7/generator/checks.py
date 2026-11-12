"""task7 architecture 10: every result of the design note's results chain computed on the cut pack with its rivals (the
band) and the hurried routes (the shortcuts), the assertions the build must pass, figures.json and effort.json."""
import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as GD  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

RESULTS = []
MARGIN = 0.12            # every provider's golden figure 12 per cent or more from its line
RIVAL_MARGIN = 0.08      # and every rival's 8 per cent or more, on the golden's side
ROUTE_MARGIN = 0.06      # each shortcut 6 per cent or more across the line from the golden, where it flips
KW_BAND = 0.06           # a provider's kW per 2027 device: within 6 per cent, or 0.02 kW where it is small
N_BAND = 0.03            # devices enrolled on 1 July 2027 and what the quote costs: within 3 per cent
TOTAL_BAND = 0.08        # the renewed providers' MW and net saving: within 8 per cent


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def r3(x):
    return round(float(x), 3)


def kw_band(v, spread=0.0):
    """a provider's band: 6 per cent (0.02 kW where that is wider), or the rivals' spread with a fifth to spare"""
    return max(abs(v) * KW_BAND, 0.02, 1.2 * spread)


def results(P):
    C = {"P": P}
    slopes = GD.cooling_slopes(P)
    pred = GD.home_model(P, slopes, "log")
    C["slopes_n"] = len(slopes)
    split = {p: GD.shed_model(P, p, "split") for p in P.providers}
    itt = {p: GD.shed_model(P, p, "itt") for p in P.providers}
    C["kw"] = {p: GD.value(P, p, True, True, True, slope_pred=pred, shed=split[p]) for p in P.providers}
    C["renewed"] = GD.renewed(P, C["kw"])
    C["bar"] = {p: P.quote[p]["price"] / P.rate for p in P.providers}
    # rivals: other defensible constructions of each step
    pred_lin = GD.home_model(P, slopes, "linear")
    split_raw = {p: GD.shed_model(P, p, "split", adjust=False) for p in P.providers}
    def at(offset, fn):
        keep = GD.AT
        GD.AT = offset
        try:
            return fn()
        finally:
            GD.AT = keep
    C["rivals"] = {
        "still in the event read at the interval's start": at(0.0, lambda: {p: GD.value(
            P, p, slope_pred=pred, shed=GD.shed_model(P, p, "split")) for p in P.providers}),
        "still in the event read at the interval's end": at(14.99, lambda: {p: GD.value(
            P, p, slope_pred=pred, shed=GD.shed_model(P, p, "split")) for p in P.providers}),
        "a linear home model with a size-by-age term": {p: GD.value(P, p, slope_pred=pred_lin, shed=split[p]) for p in P.providers},
        "one attrition rate for every channel": {p: GD.value(P, p, slope_pred=pred, shed=split[p], fleet_how="pooled")
                                                 for p in P.providers},
        "the test halves compared without the pre-event load": {p: GD.value(P, p, slope_pred=pred, shed=split_raw[p])
                                                                for p in P.providers},
    }
    # the routes the shortcuts take
    C["routes_kw"] = {
        "the test events' reduction read at the 4CP intervals (careful but hurried)":
            {p: GD.value(P, p, False, False, False, itt=itt[p]) for p in P.providers},
        "... and the 4CP days' own share in the event":
            {p: GD.value(P, p, True, False, False, shed=split[p]) for p in P.providers},
        "... and the 2027 fleet's cohorts":
            {p: GD.value(P, p, False, True, False, itt=itt[p]) for p in P.providers},
        "... and the fleet's homes":
            {p: GD.value(P, p, False, False, True, slope_pred=pred, itt=itt[p]) for p in P.providers},
        "the test events' average over the window (quick)":
            {p: GD.hurried_itt(P, p, quick=True) for p in P.providers},
    }
    C["routes"] = {"the golden": C["renewed"]}
    for name, kw in C["routes_kw"].items():
        C["routes"][name] = GD.renewed(P, kw)
    # the 2027 fleets and what the quotes cost
    C["n27"] = {p: GD.n_2027(P, p) for p in P.providers}
    C["cost"] = {p: C["n27"][p] * P.quote[p]["price"] for p in P.providers}
    C["n_now"] = {p: sum(1 for v in GD.provider_devices(P, p) if V.active(v, GD.ASOF)) for p in P.providers}
    C["retail_share27"] = {p: sum(w for v, w in GD.fleet_2027(P, p) if v["ch"] == "retail") / C["n27"][p]
                           for p in P.providers}
    # the renewed providers' MW and net saving, and the hurried route's
    def totals(kw, keep):
        mw = sum(kw[p] * C["n27"][p] for p in keep) / 1000.0
        net = sum((kw[p] * P.rate - P.quote[p]["price"]) * C["n27"][p] for p in keep)
        return mw, net
    C["mw"], C["net"] = totals(C["kw"], C["renewed"])
    care = C["routes_kw"]["the test events' reduction read at the 4CP intervals (careful but hurried)"]
    C["care_mw"], C["care_net"] = totals(care, GD.renewed(P, care))
    # components: the share in the event at the 4CP intervals on the 4CP days against the test events (each
    # provider's whole enrolled fleet, the reports read per enrolled device), the transport factor, the fleet's cohorts
    cps = [cp for cp in P.cps if cp["called"]]
    C["share_cp_ends"] = {}
    for p in ("Lumivale",):
        s = P.settings[p]
        C["share_cp_ends"][p] = [float(np.mean([GD.observed_share(P, p, cp["date"], GD.at_minute(s, cp["start"] + off))
                                                for cp in cps])) for off in (0.0, 14.99)]
    C["share_cp"], C["share_test"] = {}, {}
    for p in P.providers:
        s = P.settings[p]
        vals = [GD.observed_share(P, p, cp["date"], GD.at_minute(s, cp["start"] + GD.STEP / 2)) for cp in cps]
        C["share_cp"][p] = float(np.mean(vals))
        tests = [t["date"] for t in itt[p]["tabs"]]
        at = GD.at_minute(s, 1050 + GD.STEP / 2)
        C["share_test"][p] = float(np.mean([GD.observed_share(P, p, d, at) for d in tests]))
    C["transport"] = {p: GD.transport(P, p, GD.fleet_2027(P, p), pred) for p in P.providers}
    # the share Pinecrest Home's 2027 fleet keeps in the event at the 4CP intervals against today's
    sm = {}
    for p in ("Pinecrest Home", "Lumivale"):
        s = P.settings[p]
        days = [cp["date"] for cp in cps]
        m = GD.share_model(P, p, days, lambda d: GD.at_minute(s, next(c["start"] for c in cps if c["date"] == d) + GD.STEP / 2))
        f27 = GD.fleet_2027(P, p)
        sm[p] = (float(np.mean([GD.predict_share(m, d, GD.fleet_mix(f27, d)) for d in days])),
                 float(np.mean([GD.observed_share(P, p, d, GD.at_minute(s, next(c["start"] for c in cps if c["date"] == d)
                                                                       + GD.STEP / 2)) for d in days])))
    C["share27"] = sm
    # Ondera's window against the 4CP intervals
    C["after_window"] = {p: sum(1 for cp in P.cps if cp["start"] + GD.STEP / 2 >= P.settings[p]["e"]) for p in P.providers}
    return C


def run(target, quick=False):
    P = V.load(target)
    C = results(P)
    kw, bar = C["kw"], C["bar"]
    # ---- the call is forced: every provider's golden 12 per cent or more from its line, each rival 8 per cent on the
    # golden's side
    for p in P.providers:
        g = kw[p]
        check("bar R5 %s 12 per cent or more from its line" % p, abs(g / bar[p] - 1) >= MARGIN,
              "%.3f against %.3f" % (g, bar[p]))
        for name, R in C["rivals"].items():
            side = (R[p] > bar[p]) == (g > bar[p])
            check("SF R5 %s: %s on the golden's side, 8 per cent or more from its line" % (name, p),
                  side and abs(R[p] / bar[p] - 1) >= RIVAL_MARGIN, "%.3f against %.3f" % (R[p], g))
        spread = max(abs(R[p] - g) for R in C["rivals"].values())
        C.setdefault("band", {})[p] = kw_band(g, spread)
        check("SF R5 every rival inside %s's band" % p, spread <= C["band"][p], "%.3f against %.3f" % (spread, C["band"][p]))
    check("bar R6 the golden renews Corvane, Ardena and Kitebrook", C["renewed"] == ["Corvane", "Ardena", "Kitebrook"],
          "%s" % C["renewed"])
    # ---- each judgment alone flips its own provider, and the shortcuts land on different wrong sets
    R = C["routes"]
    care = "the test events' reduction read at the 4CP intervals (careful but hurried)"
    check("bar R6 the careful but hurried route renews a different set", R[care] != C["renewed"], "%s" % R[care])
    sets = {tuple(v) for v in R.values()}
    check("bar R6 the five routes and the golden land on six different sets", len(sets) == 6, "%s" % R)
    flips = {"... and the 4CP days' own share in the event": "Lumivale", "... and the 2027 fleet's cohorts": "Pinecrest Home",
             "... and the fleet's homes": "Kitebrook"}
    ck = C["routes_kw"][care]
    for route, p in flips.items():
        v = C["routes_kw"][route][p]
        check("bar R6 %s alone moves %s across its line by 6 per cent or more" % (route.replace("... and ", ""), p),
              (v > bar[p]) != (ck[p] > bar[p]) and abs(v / bar[p] - 1) >= ROUTE_MARGIN and abs(ck[p] / bar[p] - 1) >= MARGIN,
              "%.3f against the careful %.3f and the line %.3f" % (v, ck[p], bar[p]))
    for p in ("Lumivale", "Kitebrook", "Pinecrest Home"):
        v = C["routes_kw"][care][p]
        check("bar R5 the careful but hurried figure for %s outside its band" % p, abs(v - kw[p]) > C["band"][p] * 1.2,
              "%.3f against %.3f, band %.3f" % (v, kw[p], C["band"][p]))
    # ---- R2: the share in the event on the 4CP days against the test events
    check("bar R2 Lumivale's share in the event at the 4CP intervals is under two thirds of its test events'",
          C["share_cp"]["Lumivale"] < 0.67 * C["share_test"]["Lumivale"],
          "%.2f against %.2f" % (C["share_cp"]["Lumivale"], C["share_test"]["Lumivale"]))
    # ---- R3: Pinecrest Home's 2027 fleet
    check("bar R3 Pinecrest Home's 2027 fleet is mostly the retail channel", C["retail_share27"]["Pinecrest Home"] > 0.5,
          "%.2f" % C["retail_share27"]["Pinecrest Home"])
    # ---- R4: Kitebrook's homes shed more than the research sample's
    check("bar R4 Kitebrook's fleet homes shed a fifth or more above its research-sample devices'",
          C["transport"]["Kitebrook"] >= 1.20, "%.3f" % C["transport"]["Kitebrook"])
    # ---- R1: Ondera's window ends before most 4CP intervals
    check("bar R1 Ondera's window ends before most of the twelve 4CP intervals", C["after_window"]["Ondera"] >= 7,
          "%d" % C["after_window"]["Ondera"])
    check("bar R1 Ondera's devices add load at the 4CP intervals", kw["Ondera"] < 0, "%.3f" % kw["Ondera"])
    # ---- the fork table's rows, SF1 to SF9 (DESIGN_NOTE.md, Semantic fork table)
    tabs = GD.test_tables(P, "Corvane", adjust=False)
    pre_gap = float(np.mean([abs(t["red"][:4].mean()) for t in tabs]))
    check("SF1 the held-back half is the no-event load: the halves' 13:00 to 14:00 loads agree before any event "
          "(Board Policy 412, 4.2)", pre_gap <= 0.08, "mean gap %.3f kW" % pre_gap)
    for p in ("Ondera", "Kitebrook", "Pinecrest Home"):
        cps = [cp for cp in P.cps if cp["called"]]
        d = cps[-1]["date"]
        enrolled = len(GD.called_devices(P, p, d))
        reported = sum(1 for v in GD.called_devices(P, p, d) if (d, v["pid"]) in P.rep)
        check("SF2 per device enrolled, reached or not: %s's report leaves out devices it did not reach (4.2)" % p,
              reported < enrolled, "%d reported of %d enrolled on %s" % (reported, enrolled, d))
    only_called = {p: kw[p] * len(P.cps) / sum(cp["called"] for cp in P.cps) for p in P.providers}
    check("SF3 a summer like the last three counts the uncalled 4CP day at nothing (4.3); averaging only the called "
          "days keeps the same set", GD.renewed(P, only_called) == C["renewed"], "%s" % GD.renewed(P, only_called))
    same = all(P.settings[p] == P.quote[p]["set"] for p in P.providers)
    check("SF4 each provider's quoted 2027 settings are its 2024 to 2026 settings in the event log (same call)", same,
          "%s" % {p: P.quote[p]["set"] for p in P.providers})
    check("SF5 the devices on 1 July 2027 are today's survivors and the quotes' enrolments (4.2, 5); today's count "
          "differs", any(abs(C["n27"][p] - C["n_now"][p]) / C["n_now"][p] > 0.05 for p in P.providers),
          "%s" % {p: (round(C["n27"][p]), C["n_now"][p]) for p in P.providers})
    check("SF6 the rate is the 2027 notice's USD 54.80 per kW of 4CP load", abs(P.rate - 54.80) < 1e-9)
    # SF10: the home model's covariates; living area alone is ruled out by the research sample's own homes
    slopes = GD.cooling_slopes(P)
    rows = [(np.log(P.home[a][0]), np.clip((2005 - P.home[a][1]) / 40.0, 0, 1.2), np.log(s))
            for a, s in slopes.items() if a in P.home and s > 0]
    la, ag, ls = map(np.array, zip(*rows))
    def r2(X):
        X = np.column_stack([np.ones(len(ls))] + X)
        b, *_ = np.linalg.lstsq(X, ls, rcond=None)
        return 1 - (ls - X @ b).var() / ls.var(), b
    r_area, _ = r2([la])
    r_both, b_both = r2([la, ag])
    C["home_fit"] = (r_area, r_both, b_both[2])
    check("SF10 the homes carried by living area and year built: the research sample's cooling slopes need the year "
          "(living area alone ruled out by the sample)", r_both - r_area >= 0.05 and b_both[2] >= 0.3,
          "R2 %.3f against %.3f, age term %.3f" % (r_both, r_area, b_both[2]))
    lo, hi = C["share_cp_ends"]["Lumivale"]
    check("SF11 still in the event read anywhere in the 4CP interval: Lumivale's share between its start and end "
          "readings stays under two thirds of its test events' and the set holds at either end",
          max(lo, hi) < 0.67 * C["share_test"]["Lumivale"]
          and GD.renewed(P, C["rivals"]["still in the event read at the interval's start"]) == C["renewed"]
          and GD.renewed(P, C["rivals"]["still in the event read at the interval's end"]) == C["renewed"],
          "%.3f to %.3f against %.3f" % (lo, hi, C["share_test"]["Lumivale"]))
    for sf, name in (("SF7", "the test halves compared without the pre-event load"),
                     ("SF8", "one attrition rate for every channel"),
                     ("SF9", "a linear home model with a size-by-age term")):
        R = C["rivals"][name]
        check("%s %s: the same set" % (sf, name), GD.renewed(P, R) == C["renewed"], "%s" % GD.renewed(P, R))
    return C


def figures(C):
    P = C["P"]
    F = {}
    F["providers"] = P.providers
    F["rate"] = P.rate
    F["price"] = {p: P.quote[p]["price"] for p in P.providers}
    F["bar_kw"] = {p: r3(C["bar"][p]) for p in P.providers}
    F["kw"] = {p: r3(C["kw"][p]) for p in P.providers}
    F["kw_band"] = {p: r3(C["band"][p]) for p in P.providers}
    F["breakeven_price"] = {p: round(C["kw"][p] * P.rate, 2) for p in P.providers}
    F["renewed"] = C["renewed"]
    F["n27"] = {p: int(round(C["n27"][p])) for p in P.providers}
    F["n_now"] = C["n_now"]
    F["cost"] = {p: int(round(F["n27"][p] * P.quote[p]["price"])) for p in P.providers}
    F["mw"] = round(C["mw"], 2)
    F["saving_usd"] = int(round(sum(C["kw"][p] * F["n27"][p] for p in C["renewed"]) * P.rate, -2))
    F["paid_usd"] = int(sum(F["cost"][p] for p in C["renewed"]))
    F["renewed_devices"] = int(sum(F["n27"][p] for p in C["renewed"]))
    F["net_usd"] = int(round(F["saving_usd"] - F["paid_usd"], -2))
    F["share_cp"] = {p: round(C["share_cp"][p], 2) for p in P.providers}
    F["share_test"] = {p: round(C["share_test"][p], 2) for p in P.providers}
    F["transport"] = {p: round(C["transport"][p], 2) for p in P.providers}
    F["retail_share27"] = {p: round(C["retail_share27"][p], 2) for p in P.providers}
    F["share27"] = {p: [round(a, 2), round(b, 2)] for p, (a, b) in C["share27"].items()}
    F["routes"] = {k: list(v) for k, v in C["routes"].items()}
    F["routes_kw"] = {k: {p: r3(v) for p, v in kw.items()} for k, kw in C["routes_kw"].items()}
    F["care_kw"] = F["routes_kw"]["the test events' reduction read at the 4CP intervals (careful but hurried)"]
    F["care_set"] = F["routes"]["the test events' reduction read at the 4CP intervals (careful but hurried)"]
    F["care_mw"] = round(C["care_mw"], 2)
    F["care_net_usd"] = int(round(C["care_net"], -2))
    F["after_window"] = C["after_window"]
    F["cps"] = [[cp["date"].strftime("%Y-%m-%d"), "%02d:%02d" % divmod(cp["start"] + 15, 60), cp["called"]] for cp in P.cps]
    missed = [cp["date"] for cp in P.cps if not cp["called"]]
    F["missed_cp"] = [d.strftime("%d %B %Y").lstrip("0") for d in missed]
    F["cp_run_min"] = min(P.ev_by_date[cp["date"]]["run"] for cp in P.cps if cp["called"]) + 1
    F["window_end"] = {p: "%d:%02d" % divmod(P.settings[p]["e"], 60) for p in P.providers}
    F["ondera_kw"] = F["kw"]["Ondera"]
    F["pct"] = {"lumivale_cp": int(round(100 * F["share_cp"]["Lumivale"])),
                "lumivale_test": int(round(100 * F["share_test"]["Lumivale"])),
                "pinecrest_retail27": int(round(100 * F["retail_share27"]["Pinecrest Home"])),
                "pinecrest_2027": int(round(100 * F["share27"]["Pinecrest Home"][0])),
                "pinecrest_now": int(round(100 * F["share27"]["Pinecrest Home"][1])),
                "lumivale_cp_start": int(round(100 * C["share_cp_ends"]["Lumivale"][0])),
                "lumivale_cp_end": int(round(100 * C["share_cp_ends"]["Lumivale"][1]))}
    F["lumivale_share_cp"] = F["share_cp"]["Lumivale"]
    F["lumivale_share_cp_ends"] = [round(x, 2) for x in C["share_cp_ends"]["Lumivale"]]
    F["pct"] = dict(F.get("pct", {}))
    F["kitebrook_transport"] = F["transport"]["Kitebrook"]
    F["pinecrest_share27_2027"] = F["share27"]["Pinecrest Home"][0]
    F["pinecrest_share27"] = F["share27"]["Pinecrest Home"]
    F["totals"] = {"MW": F["mw"], "net USD": F["net_usd"]}
    F["conventions"] = {"kw_band_pct": int(KW_BAND * 100), "kw_band_floor": 0.02, "n_band_pct": int(N_BAND * 100),
                        "total_band_pct": int(TOTAL_BAND * 100), "intervals": 12}
    return F


def effort(C, F):
    P = C["P"]
    res = []
    care = F["care_kw"]
    gk = F["kw"]
    bands = {p: [round(gk[p] - F["kw_band"][p], 3), round(gk[p] + F["kw_band"][p], 3)] for p in P.providers}
    res.append({"id": "R5", "name": "each provider's kW per 2027 device at the 4CP intervals", "graded_as": "Ask 1",
                "figure": "kw", "depends": ["R2", "R3", "R4"], "independent": "", "golden": gk, "bands": bands,
                "partly_share": 0.5, "precedent": ["N12", "L12", "L38"],
                "passes": {"quick": F["routes_kw"]["the test events' average over the window (quick)"], "careful": care,
                           "thorough": gk}})
    res.append({"id": "R6", "name": "the providers renewed", "graded_as": "Recommendation", "figure": "renewed",
                "depends": ["R5"], "independent": "", "golden": F["renewed"], "precedent": ["N12", "L12"],
                "passes": {"quick": F["routes"]["the test events' average over the window (quick)"],
                           "careful": F["care_set"], "thorough": F["renewed"]}})
    res.append({"id": "R3", "name": "each provider's devices on 1 July 2027 and the quote's cost", "graded_as": "Ask 2",
                "figure": "n27", "depends": [], "independent": "the roster and the quotes", "golden": F["n27"],
                "bands": {p: [round(v * (1 - N_BAND)), round(v * (1 + N_BAND))] for p, v in F["n27"].items()},
                "passes": {"quick": F["n_now"], "careful": F["n27"], "thorough": F["n27"]}})
    tot = F["totals"]
    res.append({"id": "R7", "name": "the renewed providers' MW at the 4CP intervals and the net saving", "graded_as": "Ask 3",
                "figure": "totals", "depends": ["R6"], "independent": "", "golden": F["totals"],
                "bands": {k: sorted([v * (1 - TOTAL_BAND), v * (1 + TOTAL_BAND)]) for k, v in tot.items()},
                "precedent": ["N12", "L12"],
                "passes": {"quick": {k: None for k in tot}, "careful": {"MW": F["care_mw"], "net USD": F["care_net_usd"]},
                           "thorough": tot}})
    res.append({"id": "R2", "name": "Lumivale's share in the event at the 4CP intervals on the 4CP days",
                "graded_as": "Component 1", "figure": "lumivale_share_cp", "depends": [],
                "independent": "the providers' reports and the 4CP list", "golden": F["lumivale_share_cp"],
                "band": [min(F["lumivale_share_cp_ends"]) - 0.02, max(F["lumivale_share_cp_ends"]) + 0.02],
                "precedent": ["N12", "L13"],
                "passes": {"quick": None, "careful": F["share_test"]["Lumivale"], "thorough": F["lumivale_share_cp"]}})
    res.append({"id": "R4", "name": "Kitebrook's fleet's homes against its research-sample devices'", "graded_as": "Component 3",
                "figure": "kitebrook_transport", "depends": [], "independent": "the appraisal roll and the research sample",
                "golden": F["kitebrook_transport"], "band": [F["kitebrook_transport"] - 0.06, F["kitebrook_transport"] + 0.06],
                "precedent": ["L38"], "passes": {"quick": None, "careful": 1.0, "thorough": F["kitebrook_transport"]}})
    res.append({"id": "R3b", "name": "Pinecrest Home's 2027 fleet's share in the event", "graded_as": "Component 2",
                "figure": "pinecrest_share27_2027", "depends": [], "independent": "the roster, the quotes and the reports",
                "golden": F["pinecrest_share27_2027"],
                "band": [F["pinecrest_share27_2027"] - 0.03, F["pinecrest_share27_2027"] + 0.03], "precedent": ["L11", "L12"],
                "passes": {"quick": None, "careful": F["share27"]["Pinecrest Home"][1],
                           "thorough": F["pinecrest_share27_2027"]}})
    res.append({"id": "R1", "name": "Ondera's devices at the 4CP intervals after its window", "graded_as": "Component 4",
                "figure": "ondera_kw", "depends": [], "independent": "the test events and the 4CP list",
                "golden": F["kw"]["Ondera"], "band": [F["kw"]["Ondera"] - 0.03, F["kw"]["Ondera"] + 0.03],
                "passes": {"quick": F["routes_kw"]["the test events' average over the window (quick)"]["Ondera"],
                           "careful": care["Ondera"], "thorough": F["kw"]["Ondera"]}})
    routes = [{"name": k, "answer": v, "golden": k == "the golden"} for k, v in F["routes"].items()]
    hints = [{"sentence": "the 4CP days come late in heat waves, when members leave events, so read the share still in the "
                          "event on those days, not on the test events", "rescues": ["R2"]},
             {"sentence": "Pinecrest Home's 2027 growth is a retail cohort that is often offline and leaves events",
              "rescues": ["R3b"]},
             {"sentence": "the research sample's homes are newer and smaller than the fleets', so carry the shed to the "
                          "fleet's homes off the appraisal roll", "rescues": ["R4"]}]
    forcing = {"kind": "set", "golden_family": [{"name": "the golden", "answer": F["renewed"]}] +
               [{"name": k, "answer": GD.renewed(P, v)} for k, v in C["rivals"].items()],
               "shortcuts": [{"name": k, "answer": v} for k, v in F["routes"].items() if k != "the golden"],
               "perturbations": []}
    for name, f in (("the shed per device in the event", "shed"), ("the share in the event", "share"),
                    ("the homes' transport", "tf")):
        for sgn in (-1, 1):
            moved = {p: C["kw"][p] * (1 + sgn * 0.10) for p in P.providers}
            forcing["perturbations"].append({"input": "%s %+d per cent" % (name, sgn * 10), "answer": GD.renewed(P, moved)})
    return {"results": res, "routes": routes, "hints": hints, "forcing": forcing,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
