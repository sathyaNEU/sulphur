"""Every owed figure computed from the cut pack (methods.py on target/), the rivals that set each band, the named
shortcuts and the three passes, written as figures.json and effort.json (architecture 5 as repaired on 2026-11-13: the
January 2027 rises, with the subscriptions that stop and take their plan up again and the stayers' listening)."""
import math

import numpy as np

import methods as M
import params as P

NAMES = {"FLEX": "Flex", "STD": "Standaard", "ONB": "Onbeperkt", "GEZ": "Gezin"}
CTY = {"NL": "Netherlands", "BE": "Flanders"}
GOLD = M.GOLD
# the judgments the call can turn on: (switch, golden choice, hurried choice, sentence, precedents), each a stump a run
# has been seen to name and wave through or to lose
STUMPS = {
    "J1": ("ret", "band", "none", "a subscription that stops paying can take its plan up again on the same account, "
           "the light listeners soonest, so those a rise loses are not all lost for 2027", ["N33", "N24"]),
    "J2": ("sal", "within", "none", "the account holders who stay listen more for months after the bill at the higher "
           "price, the heavier listeners most, and each extra hour costs EUR 0.40", ["N23", "L45"]),
}
REFLEXES = [
    ("the first bill's response read by whether each past rise passed the rival's price, with the profile limit of "
     "the plan below", ["R61"]),
    ("the light listeners' extra leaving at the December bill after the price e-mail", ["R62"]),
    ("downgraders kept paying on the lower plan, valued on their own months", ["R43"]),
    ("each subscription valued on its own listening", ["R44"]),
    ("EUR 0.40 per counted hour, filed in schedule B 2.1", []),
    ("a past response carried to a rise of another size", ["R45"]),
]


def stump_opts(fixed):
    return M.opts(**{k: (g if j in fixed else h) for j, (k, g, h, _, _) in STUMPS.items()})


# the careful but hurried pass is the reflex route: every move the runs make unprompted right, every stump hurried
CAREFUL = stump_opts(set())
QUICK = M.opts(resp="pooled", cost="share26", channels=("live",), member="today", down_as_exit=True, who="flat",
               ret="none", sal="none", announce=False, r1="open")
# defensible methods that set each figure's band
RIVALS = {
    "the same country a year earlier as the control where the records reach it": M.opts(control="prior"),
    "the January and February bills as the first bill's window": M.opts(window="two"),
    "each past response carried on the log of the price ratio": M.opts(dose="log"),
    "each plan's own rises of the same kind, as they were read": M.opts(resp="kind"),
    "each plan's own level and one step where a rise passes the rival, fitted on the eight": M.opts(resp="plan_step"),
    "the plan's continuation by paying months alone": M.opts(surv="plan_tenure"),
    "downgraders modelled on their own hours at the lower plan's cap": M.opts(dval="model"),
    "the stayers' fade fitted plan by plan": M.opts(sal_fit="per_plan"),
    "the stayers' extra listening as observed month by month, no fitted fade": M.opts(sal_fit="observed"),
    "re-sent warehouse rows summed": M.opts(dedup=False),
}
ROUTES = {
    "the golden": GOLD,
    "the careful route: no return after a stop, the stayers listening as before": CAREFUL,
    "returns after a stop, the stayers listening as before": stump_opts({"J1"}),
    "the stayers' extra listening, no return after a stop": stump_opts({"J2"}),
    "the careful route with each plan's own rises read together": M.opts(resp="plan", ret="none", sal="none"),
    "the careful route with each plan's own rise in its country": M.opts(resp="region", ret="none", sal="none"),
    "the careful route with the response at the first bill alone": M.opts(announce=False, ret="none", sal="none"),
    "the careful route with one response for every rise": M.opts(resp="pooled", ret="none", sal="none"),
    "the careful route on the 2026 basis (52 per cent of net revenue)": M.opts(cost="share26", ret="none", sal="none"),
    "the careful route with the stayers' listening read off the plan's averages": M.opts(sal="average", ret="none"),
    "returns at one rate for every listener, the stayers listening as before": M.opts(ret="pooled", sal="none"),
    "the golden with returns at one rate for every listener": M.opts(ret="pooled"),
    "the golden with the stayers' listening read off the plan's averages": M.opts(sal="average"),
    "the golden with the stayers' extra listening held at its first months": M.opts(sal="persist"),
    "the golden with every subscription answering at its plan's rate": M.opts(who="flat"),
    "the golden on the 2026 basis": M.opts(cost="share26"),
    "the quick route": QUICK,
}
SINGLE = ["the careful route: no return after a stop, the stayers listening as before",
          "returns after a stop, the stayers listening as before",
          "the stayers' extra listening, no return after a stop",
          "the careful route with each plan's own rises read together",
          "the careful route with each plan's own rise in its country",
          "the careful route with the response at the first bill alone",
          "the careful route with one response for every rise",
          "the careful route on the 2026 basis (52 per cent of net revenue)",
          "the careful route with the stayers' listening read off the plan's averages"]
CLOSED_ROUTES = ["the golden with returns at one rate for every listener",
                 "the golden with the stayers' listening read off the plan's averages"]
_TARGET = [None]


def results(pk, o):
    F = M.forecast(pk, o)
    R = {"R1": M.r1(pk) if o.get("r1") != "open" else _open_periods(pk),
         "CH": {NAMES[k]: v for k, v in M.r2(pk, o).items()}}
    R["R3"] = {"%s %s" % (NAMES[p], CTY[c]): 100 * F[p]["cells"][c]["extra_cancel"] for p in P.PLANS for c in ("NL", "BE")}
    R["R4"] = {"%s %s" % (NAMES[p], CTY[c]): 100 * F[p]["cells"][c]["extra_down"] for p in ("STD", "ONB", "GEZ")
               for c in ("NL", "BE")}
    R["R5"] = {NAMES[p]: 100 * F[p]["back_share"] for p in P.PLANS}
    R["R6"] = {NAMES[p]: F[p]["sal_hours"] for p in P.PLANS}
    R["R7"] = {NAMES[p]: F[p]["change"] for p in P.PLANS}
    R["R8"] = sorted(NAMES[p] for p in P.PLANS if F[p]["change"] > 0)
    R["R9"] = {NAMES[p]: F[p]["end27"] for p in P.PLANS}
    R["R2"] = {NAMES[p]: F[p]["remun"] for p in P.PLANS}
    R["F"] = F
    return R


def _open_periods(pk):
    """Every plan period open on 31 October 2026, trials, staff and test accounts included."""
    pl = pk["plan"]
    op = pl[(pl["period_start"] <= "2026-10-31") & (pl["period_end"].isna() | (pl["period_end"] >= "2026-10-31"))]
    return {p: int((op["plan_code"] == p).sum()) for p in P.PLANS}


def _band(vals, w):
    return [round(min(vals) - w, 2), round(max(vals) + w, 2)]


def _r(d, nd=1):
    return {k: round(float(v), nd) for k, v in d.items()}


def _as_read(pk):
    """The 2027 cells read straight off each plan's own past rise of the same kind, not floored (a rise can read below
    none on sampling noise): a reading of the first bill a run may file, kept inside the bands."""
    rows = M.response(pk, GOLD)
    c3, c4 = {}, {}
    for p in P.PLANS:
        for c in ("NL", "BE"):
            cross = P.PRICE[p] <= pk["rival"][(2027, c, p)] < P.PRICE27[p]
            xc, xd, _ = M._resp_rate(rows, p, cross, c, "kind", GOLD)
            c3["%s %s" % (NAMES[p], CTY[c])] = 100 * xc
            if p != "FLEX":
                c4["%s %s" % (NAMES[p], CTY[c])] = 100 * xd
    return c3, c4


def run_all(target):
    _TARGET[0] = target
    pk = M.load(target)
    G = results(pk, GOLD)
    riv = {nm: results(pk, o) for nm, o in RIVALS.items()}
    out = {nm: results(pk, o) for nm, o in ROUTES.items()}
    C, Q = out[list(ROUTES)[1]], out["the quick route"]
    a3, a4 = _as_read(pk)
    spec = {"R3": (0.05, 0.3), "R4": (0.05, 0.3), "R5": (0.05, 2.0), "R6": (0.10, 1.0), "R7": (0.03, 0.3),
            "R9": (0.02, 5.0), "R2": (0.02, 0.3), "CH": (0.01, 0.005)}
    bands = {}
    for key, (w, fl) in spec.items():
        bands[key] = {}
        for k, v in G[key].items():
            vals = [v] + [r[key][k] for r in riv.values()]
            if key == "R3":
                vals.append(a3[k])
            if key == "R4":
                vals.append(a4[k])
            bands[key][k] = _band(vals, max(w * abs(v), fl))
    bands["R9"] = {k: [math.floor(v[0]), math.ceil(v[1])] for k, v in bands["R9"].items()}
    rows = M.response(pk, GOLD)
    ann = M.announce(pk, GOLD)
    haz, hfail = M.return_hazard(pk, GOLD)
    path, obs, tau = M.salience(pk, GOLD)
    back12 = {}
    for b in range(M.NB):
        s = 1.0
        for k in range(1, 13):
            s *= 1.0 - haz[b, k, (P.CUT + 2 + k) % 12]
        back12[b] = round(100 * (1 - s), 1)
    gf = G["F"]
    fig = {
        "raise": G["R8"], "hold": sorted(NAMES[p] for p in P.PLANS if NAMES[p] not in G["R8"]),
        "careful_raise": C["R8"], "quick_raise": Q["R8"],
        "paying_oct": {NAMES[k]: v for k, v in G["R1"].items()}, "paying_oct_total": sum(G["R1"].values()),
        "counted_per_month": _r(G["CH"], 2),
        "extra_cancel": _r(G["R3"]), "extra_down": _r(G["R4"]),
        "back_share": _r(G["R5"]), "sal_hours": _r(G["R6"]), "change_2027": _r(G["R7"]),
        "paying_end27": {k: int(round(v)) for k, v in G["R9"].items()},
        "paying_end27_total": int(sum(round(v) for v in G["R9"].values())),
        "remun_2027": _r(G["R2"]),
        "careful": {"change_2027": _r(C["R7"]), "paying_end27": {k: int(round(v)) for k, v in C["R9"].items()},
                    "remun_2027": _r(C["R2"])},
        "bands": bands,
        "events": [{"year": r["year"], "country": CTY[r["country"]], "plan": NAMES[r["plan"]], "subscriptions": r["n"],
                    "crossed": bool(r["cross"]), "extra_cancel": round(100 * r["x_cancel"], 1),
                    "extra_down": round(100 * r["x_down"], 1)} for r in rows],
        "announce_events": [{"year": r["year"], "country": CTY[r["country"]], "plan": NAMES[r["plan"]],
                             "announce": round(100 * r["x_announce"], 1)} for r in ann],
        "announce_pct": {NAMES[p]: round(100 * gf[p]["xa"], 1) for p in P.PLANS},
        "back12_by_band": {["under 3", "3 to 8", "8 to 20", "20 and more"][b]: v for b, v in back12.items()},
        "uplift_first_month": {NAMES[p]: round(100 * path[p][0], 1) for p in P.PLANS},
        "uplift_obs": {NAMES[p]: [[k, round(100 * u, 1)] for k, u, n in obs[p]] for p in P.PLANS},
        "fade_months": round(tau, 1),
        "routes": {nm: {"raise": r["R8"], "change_2027": _r(r["R7"])} for nm, r in out.items()},
        "rival_family": {nm: r["R8"] for nm, r in riv.items()},
        "price0": {NAMES[k]: v for k, v in P.PRICE0.items()},
        "price26": {NAMES[k]: v for k, v in P.PRICE.items()}, "price27": {NAMES[k]: v for k, v in P.PRICE27.items()},
        "rival_2027": {"%s %s" % (NAMES[p], CTY[c]): pk["rival"][(2027, c, p)] for p in P.PLANS for c in ("NL", "BE")},
        "cross_2027": {NAMES[p]: bool(gf[p]["cells"]["NL"]["cross"]) for p in P.PLANS},
        "rise_eur": {NAMES[k]: round(P.PRICE27[k] - P.PRICE[k], 2) for k in P.PLANS},
        "per": 100, "rate": P.RATE27, "clauses": [2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.5, 3.8, 3.9, 3.10],
    }
    return fig, effort(G, C, Q, riv, out, fig), {"pk": pk}


def effort(G, C, Q, riv, out, fig):
    b = fig["bands"]
    pk = M.load(_TARGET[0])

    def tab(R, key, nd=1):
        return _r(R[key], nd)
    res = [
        {"id": "R1", "name": "paying subscriptions by plan at 31 October 2026", "graded_as": "Ask 1",
         "figure": "paying_oct", "depends": [], "independent": "the October base", "golden": fig["paying_oct"],
         "bands": {k: [v - 0.5, v + 0.5] for k, v in fig["paying_oct"].items()},
         "passes": {"quick": {NAMES[k]: v for k, v in Q["R1"].items()}, "careful": fig["paying_oct"],
                    "thorough": fig["paying_oct"]}},
        {"id": "R3", "name": "extra cancellations per 100 at the first 2027 bill, by plan and country",
         "graded_as": "Ask 2", "figure": "extra_cancel", "depends": [], "independent": "the 2025 and 2026 rises",
         "golden": fig["extra_cancel"], "bands": b["R3"], "partly_share": 0.75,
         "passes": {"quick": tab(Q, "R3"), "careful": tab(C, "R3"), "thorough": fig["extra_cancel"]}},
        {"id": "R4", "name": "extra downgrades per 100 at the first 2027 bill, by plan and country",
         "graded_as": "Ask 3", "figure": "extra_down", "depends": [], "independent": "the 2025 and 2026 rises",
         "golden": fig["extra_down"], "bands": b["R4"], "partly_share": 0.75,
         "passes": {"quick": tab(Q, "R4"), "careful": tab(C, "R4"), "thorough": fig["extra_down"]}},
        {"id": "R9", "name": "of each plan's October 2026 subscriptions, paying on any plan at 31 December 2027 with "
         "the rise", "graded_as": "Ask 4", "figure": "paying_end27", "depends": ["R3", "R4"], "independent": "",
         "golden": fig["paying_end27"], "bands": b["R9"], "precedent": ["N33"], "partly_share": 0.75,
         "passes": {"quick": tab(Q, "R9", 0), "careful": tab(C, "R9", 0), "thorough": fig["paying_end27"]}},
        {"id": "R2", "name": "the 2027 publisher remuneration on each plan's October 2026 subscriptions with the "
         "rise, per subscription", "graded_as": "Ask 5", "figure": "remun_2027", "depends": [], "independent":
         "the counted hours and the October base", "golden": fig["remun_2027"], "bands": b["R2"],
         "precedent": ["N23", "L45", "N33"], "partly_share": 0.75,
         "passes": {"quick": tab(Q, "R2"), "careful": tab(C, "R2"), "thorough": fig["remun_2027"]}},
        {"id": "R7", "name": "each plan's change in its October 2026 subscriptions' 2027 contribution with the rise",
         "graded_as": "Component 1", "figure": "change_2027", "depends": ["R3", "R4", "R5", "R6"], "independent": "",
         "golden": fig["change_2027"], "bands": b["R7"], "precedent": ["N33", "N23", "L45"],
         "passes": {"quick": tab(Q, "R7"), "careful": tab(C, "R7"), "thorough": fig["change_2027"]}},
        {"id": "R5", "name": "of the subscriptions that stop paying by December 2027, how many per 100 pay again "
         "then", "graded_as": "Component 2", "figure": "back_share", "depends": [], "independent":
         "the lapses to October 2026", "golden": fig["back_share"], "bands": b["R5"], "precedent": ["N33", "N24"],
         "passes": {"quick": tab(Q, "R5"), "careful": tab(C, "R5"), "thorough": fig["back_share"]}},
        {"id": "R6", "name": "the stayers' extra counted hours over 2027 after the rise, per subscription staying all "
         "year", "graded_as": "Component 3", "figure": "sal_hours", "depends": [], "independent":
         "the 2025 and 2026 rises' stayers", "golden": fig["sal_hours"], "bands": b["R6"],
         "precedent": ["N23", "L45"],
         "passes": {"quick": tab(Q, "R6"), "careful": tab(C, "R6"), "thorough": fig["sal_hours"]}},
        {"id": "R8", "name": "the rises that go ahead", "graded_as": "Recommendation", "figure": "raise",
         "depends": ["R7"], "independent": "", "golden": fig["raise"], "precedent": ["N33", "N23"],
         "passes": {"quick": Q["R8"], "careful": C["R8"], "thorough": fig["raise"]}},
    ]
    keys = ("R2", "R3", "R4", "R5", "R6", "R7", "R9")

    def inb(R, key):
        return all(b[key][k][0] <= v <= b[key][k][1] for k, v in R[key].items())

    def rescues(o):
        R = results(pk, o)
        return [k for k in keys if inb(R, k)] + (["R8"] if R["R8"] == G["R8"] else [])
    careful_right = set(rescues(CAREFUL))
    hints = [{"sentence": STUMPS[j][3], "rescues": [k for k in rescues(stump_opts({j})) if k not in careful_right]}
             for j in STUMPS]

    def moved(R):
        return [k for k in keys if not inb(R, k)] + (["R8"] if R["R8"] != G["R8"] else [])
    judg = []
    for j, (k, g, h, name, prec) in STUMPS.items():
        dr = results(pk, stump_opts(set(STUMPS) - {j}))
        al = stump_opts({j})
        judg.append({"id": j, "name": name, "kind": "stump", "precedent": prec,
                     "dropped": {"answer": dr["R8"], "results_moved": moved(dr)},
                     "alone": {"answer": results(pk, al)["R8"],
                               "results_rescued": [x for x in rescues(al) if x not in careful_right]}})
    for i, (name, prec) in enumerate(REFLEXES, 3):
        judg.append({"id": "J%d" % i, "name": name, "kind": "reflex", "precedent": prec})
    factorial = {"golden_answer": G["R8"], "reflex_route": {"answer": C["R8"]}, "judgments": judg}
    fam = [{"name": "the golden", "answer": G["R8"]}] + [{"name": nm, "answer": r["R8"]} for nm, r in riv.items()]
    pert = []
    for nm, k in (("extra cancellations", "scale_cancel"), ("extra downgrades", "scale_down"),
                  ("the December leaving", "scale_announce"), ("the stayers' extra listening", "scale_sal"),
                  ("the return after a stop", "scale_ret")):
        for s in (1.2, 0.8):
            pert.append({"input": "%s %+d%%" % (nm, round(100 * (s - 1))),
                         "answer": results(pk, dict(GOLD, **{k: s}))["R8"]})
    shortcuts = [{"name": nm, "answer": out[nm]["R8"]} for nm in SINGLE]
    return {"results": res, "hints": hints, "factorial": factorial,
            "forcing": {"kind": "set", "golden_answer": G["R8"], "golden_family": fam, "perturbations": pert,
                        "shortcuts": shortcuts,
                        "closed_supporting": [{"name": nm, "answer": out[nm]["R8"]} for nm in CLOSED_ROUTES]},
            "routes": [{"name": nm, "answer": r["R8"], "golden": nm == "the golden"} for nm, r in out.items()],
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
