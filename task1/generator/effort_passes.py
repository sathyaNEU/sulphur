"""Every owed figure computed from the cut pack (methods.py on target/), the rivals that set each band, the named
shortcuts and the three passes, written as figures.json and effort.json (architecture 5: the January 2027 rises)."""
import methods as M
import params as P

NAMES = {"FLEX": "Flex", "STD": "Standaard", "ONB": "Onbeperkt", "GEZ": "Gezin"}
CTY = {"NL": "Netherlands", "BE": "Flanders"}
GOLD = M.GOLD
# the judgments the call can turn on: (switch, golden choice, hurried choice), each a stump a run has been seen to miss
STUMPS = {
    "J1": ("resp", "plan_cross", "region", "the response read by whether each past rise passed the rival's price",
           ["N25", "L15"]),
    "J2": ("use", True, False, "the subscriptions that stay after a rise listen more (Onbeperkt accounts add their "
           "second profile), at EUR 0.40 a counted hour", ["N23", "L15"]),
    "J3": ("announce", True, False, "the light listeners who leave at the December bill after the price e-mail, "
           "before the new price", ["N24", "L04"]),
}
REFLEXES = [
    ("downgraders kept paying on the lower plan, valued on their own months", ["R43"]),
    ("each subscription valued on its own listening", ["R44"]),
    ("EUR 0.40 per counted hour, filed in schedule B 2.1", []),
    ("a past response carried to a rise of another size (every 2027 rise is the plan's past rise in euros)", ["R45"]),
]


def stump_opts(fixed):
    return M.opts(**{k: (g if j in fixed else h) for j, (k, g, h, _, _) in STUMPS.items()})


# the careful but hurried pass is the reflex route: every move the runs make unprompted right, every stump hurried
CAREFUL = stump_opts(set())
QUICK = M.opts(resp="pooled", cost="share26", channels=("live",), member="today", down_as_exit=True, who="avg",
               r1="open")
RIVALS = {
    "the same country a year earlier as the control where the record holds it": M.opts(control="prior"),
    "the first bill alone as the response window": M.opts(window="first"),
    "downgraders valued on their own hours capped at the lower plan's, with the cap response": M.opts(dval="model"),
    "re-sent warehouse rows summed": M.opts(dedup=False),
    "each past response carried in proportion to the rise in per cent": M.opts(dose="pct"),
    "each past response carried on the log of the price ratio": M.opts(dose="log"),
    "each plan's own level and one step where a rise passes the rival, fitted on the eight events": M.opts(resp="plan_step"),
}
ROUTES = {
    "the golden": GOLD,
    "the careful route: each plan's own past rise in its region, read at the first bill alone": CAREFUL,
    "each plan's own past response, a downgrade counted as an exit, leavers at the plan's average":
        M.opts(resp="plan", down_as_exit=True, who="avg", use=False, announce=False),
    "the crossing read, the first bill alone": stump_opts({"J1"}),
    "one response for every rise, scaled by the rise": M.opts(resp="pooled"),
    "each plan's own past response": M.opts(resp="plan"),
    "the response read off the new price's gap to the rival, in a straight line": M.opts(resp="gap"),
    "a downgrade counted as an exit from the plan": M.opts(down_as_exit=True),
    "the 2026 remuneration basis carried (52 per cent of net revenue)": M.opts(cost="share26"),
    "the quick route": QUICK,
}
SINGLE = ["one response for every rise, scaled by the rise", "each plan's own past response",
          "the crossing read, the first bill alone",
          "the response read off the new price's gap to the rival, in a straight line"]
_TARGET = [None]


def results(pk, o):
    r, d, rows = M.r5_rises(pk, o)
    R = {"R1": M.r1(pk) if o.get("r1") != "open" else _open_periods(pk),
         "R2": {NAMES[k]: v for k, v in M.r2(pk, o).items()}}
    R["R3"] = {"%s %s" % (NAMES[p], CTY[c]): 100 * d[p][c]["extra_cancel"] for p in P.PLANS for c in ("NL", "BE")}
    R["R4"] = {"%s %s" % (NAMES[p], CTY[c]): 100 * d[p][c]["extra_down"] for p in ("STD", "ONB", "GEZ")
               for c in ("NL", "BE")}
    R["R5"] = {NAMES[p]: d[p]["downgrader_value"] for p in ("STD", "ONB", "GEZ")}
    R["R6"] = {NAMES[p]: d[p]["h_ratio"][0] for p in P.PLANS}
    R["R6c"] = {NAMES[p]: d[p]["h_cross"] for p in P.PLANS}
    R["R7"] = {NAMES[p]: r[p] for p in P.PLANS}
    R["R8"] = sorted(NAMES[p] for p in P.PLANS if r[p] > 0)
    R["R9"] = {NAMES[p]: d[p]["paying_end27"] for p in P.PLANS}
    R["rows"] = rows
    return R


def _open_periods(pk):
    """Every plan period open on 31 October 2026, trials, staff and test accounts included."""
    pl = pk["plan"]
    op = pl[(pl["period_start"] <= "2026-10-31") & (pl["period_end"].isna() | (pl["period_end"] >= "2026-10-31"))]
    return {p: int((op["plan_code"] == p).sum()) for p in P.PLANS}


def _band(vals, w):
    return [round(min(vals) - w, 2), round(max(vals) + w, 2)]


def _r(d, nd=1):
    return {k: round(v, nd) for k, v in d.items()}


def run_all(target):
    _TARGET[0] = target
    pk = M.load(target)
    G = results(pk, GOLD)
    riv = {nm: results(pk, o) for nm, o in RIVALS.items()}
    out = {nm: results(pk, o) for nm, o in ROUTES.items()}
    C, Q = out[list(ROUTES)[1]], out["the quick route"]
    floor = {"R3": 0.3, "R4": 0.3, "R2": 0.005, "R5": 0.5, "R6": 0.005, "R7": 0.3}
    bands = {}
    floor["R9"] = 5.0
    for key, w in (("R2", 0.01), ("R3", 0.05), ("R4", 0.05), ("R5", 0.01), ("R6", 0.01), ("R7", 0.03), ("R9", 0.02)):
        bands[key] = {k: _band([v] + [r[key][k] for r in riv.values()], max(w * abs(v), floor[key]))
                      for k, v in G[key].items()}
    import math
    bands["R9"] = {k: [math.floor(v[0]), math.ceil(v[1])] for k, v in bands["R9"].items()}
    fig = {
        "raise": G["R8"], "hold": sorted(NAMES[p] for p in P.PLANS if NAMES[p] not in G["R8"]),
        "careful_raise": C["R8"], "quick_raise": Q["R8"],
        "paying_oct": {NAMES[k]: v for k, v in G["R1"].items()}, "paying_oct_total": sum(G["R1"].values()),
        "counted_per_month": _r(G["R2"], 2),
        "extra_cancel": _r(G["R3"]), "extra_down": _r(G["R4"]), "downgrader_value": _r(G["R5"]),
        "leaver_hours_ratio": _r(G["R6"], 2), "change_2027": _r(G["R7"]),
        "paying_end27": {k: int(round(v)) for k, v in G["R9"].items()},
        "paying_end27_total": int(sum(round(v) for v in G["R9"].values())),
        "later_events": [{"year": r["year"], "country": CTY[r["country"]], "plan": NAMES[r["plan"]],
                          "announce": round(100 * r["x_announce"], 1), "use": round(100 * r["x_use"], 1)}
                         for r in M.later_responses(pk, GOLD)],
        "announce_pct": {NAMES[p]: round(100 * float(sum(r["x_announce"] for r in M.later_responses(pk, GOLD) if r["plan"] == p) / 2), 1) for p in P.PLANS},
        "use_pct": {NAMES[p]: round(100 * float(sum(r["x_use"] for r in M.later_responses(pk, GOLD) if r["plan"] == p) / 2), 1) for p in P.PLANS},
        "careful": {"extra_cancel": _r(C["R3"]), "change_2027": _r(C["R7"]), "leaver_hours_ratio": _r(C["R6"], 2)},
        "bands": bands,
        "events": [{"year": r["year"], "country": CTY[r["country"]], "plan": NAMES[r["plan"]], "subscriptions": r["n"],
                    "crossed": bool(r["cross"]), "extra_cancel": round(100 * r["x_cancel"], 1),
                    "extra_down": round(100 * r["x_down"], 1)} for r in G["rows"]],
        "routes": {nm: {"raise": r["R8"], "change_2027": _r(r["R7"])} for nm, r in out.items()},
        "rival_family": {nm: r["R8"] for nm, r in riv.items()},
        "price26": {NAMES[k]: v for k, v in P.PRICE.items()}, "price27": {NAMES[k]: v for k, v in P.PRICE27.items()},
        "rival_nl": {NAMES[k]: P.rival_of("NL", k, P.CUT) for k in P.PLANS},
        "rival_be": {NAMES[k]: P.rival_of("BE", k, P.CUT) for k in P.PLANS},
        "rise_eur": {NAMES[k]: round(P.PRICE27[k] - P.PRICE[k], 2) for k in P.PLANS},
        "hint_cross_onb": round(results(pk, dict(CAREFUL, resp="plan_cross"))["R7"]["Onbeperkt"], 1),
        "per": 100, "rate": P.RATE27, "clauses": [2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.5, 3.8, 3.9, 3.10],
    }
    return fig, effort(G, C, Q, riv, out, fig), {"pk": pk}


def effort(G, C, Q, riv, out, fig):
    b = fig["bands"]
    pk = M.load(_TARGET[0])
    zero5 = {k: 0.0 for k in fig["downgrader_value"]}
    one6 = {k: 1.0 for k in fig["leaver_hours_ratio"]}
    res = [
        {"id": "R1", "name": "paying subscriptions by plan at 31 October 2026", "graded_as": "Ask 1", "figure": "paying_oct",
         "depends": [], "independent": "the October base", "golden": fig["paying_oct"],
         "bands": {k: [v - 0.5, v + 0.5] for k, v in fig["paying_oct"].items()},
         "passes": {"quick": {NAMES[k]: v for k, v in Q["R1"].items()}, "careful": fig["paying_oct"],
                    "thorough": fig["paying_oct"]}},
        {"id": "R3", "name": "extra cancellations per 100 subscriptions at the first 2027 bill, by plan and region",
         "graded_as": "Component 2", "figure": "extra_cancel", "depends": [], "independent": "the 2025 and 2026 rises",
         "golden": fig["extra_cancel"], "bands": b["R3"], "precedent": ["N25", "L15"], "partly_share": 0.75,
         "passes": {"quick": _r(Q["R3"]), "careful": _r(C["R3"]), "thorough": fig["extra_cancel"]}},
        {"id": "R4", "name": "extra downgrades per 100 subscriptions at the first 2027 bill, by plan and region",
         "graded_as": "Ask 3", "figure": "extra_down", "depends": [], "independent": "the 2025 and 2026 rises",
         "golden": fig["extra_down"], "bands": b["R4"], "precedent": ["N25", "L15"], "partly_share": 0.75,
         "passes": {"quick": _r(Q["R4"]), "careful": _r(C["R4"]), "thorough": fig["extra_down"]}},
        {"id": "R7", "name": "each plan's change in its October 2026 base's 2027 contribution if its rise goes ahead",
         "graded_as": "Component 1", "figure": "change_2027", "depends": ["R3", "R4"], "independent": "",
         "golden": fig["change_2027"], "bands": b["R7"], "precedent": ["N24", "N23", "L15"],
         "passes": {"quick": _r(Q["R7"]), "careful": _r(C["R7"]), "thorough": fig["change_2027"]}},
        {"id": "R9", "name": "each plan's October 2026 subscriptions still paying at the end of 2027 if its rise goes ahead",
         "graded_as": "Ask 4", "figure": "paying_end27", "depends": ["R3", "R4"], "independent": "",
         "golden": fig["paying_end27"], "bands": b["R9"], "precedent": ["N24", "L04"], "partly_share": 0.75,
         "passes": {"quick": _r(Q["R9"], 0), "careful": _r(C["R9"], 0), "thorough": fig["paying_end27"]}},
        {"id": "R8", "name": "the rises that go ahead", "graded_as": "Recommendation", "figure": "raise", "depends": ["R7"],
         "independent": "", "golden": fig["raise"], "precedent": ["L15", "L06"],
         "passes": {"quick": Q["R8"], "careful": C["R8"], "thorough": fig["raise"]}},
    ]

    def inb(R, key):
        return all(b[key][k][0] <= v <= b[key][k][1] for k, v in R[key].items())

    def rescues(o):
        R = results(pk, o)
        got = [k for k in ("R3", "R4", "R7", "R9") if inb(R, k)]
        return got + (["R8"] if R["R8"] == G["R8"] else [])
    hints = [{"sentence": STUMPS[j][3], "rescues": rescues(stump_opts({j}))} for j in STUMPS]
    gold_ans = G["R8"]

    def moved(R):
        return [k for k in ("R3", "R4", "R7", "R9") if not inb(R, k)] + (["R8"] if R["R8"] != gold_ans else [])
    judg = []
    for j, (k, g, h, name, prec) in STUMPS.items():
        dr = results(pk, stump_opts(set(STUMPS) - {j}))
        judg.append({"id": j, "name": name, "kind": "stump", "precedent": prec,
                     "dropped": {"answer": dr["R8"], "results_moved": moved(dr)},
                     "alone": {"answer": results(pk, stump_opts({j}))["R8"], "results_rescued": rescues(stump_opts({j}))}})
    for i, (name, prec) in enumerate(REFLEXES, 4):
        judg.append({"id": "J%d" % i, "name": name, "kind": "reflex", "precedent": prec})
    factorial = {"golden_answer": gold_ans, "reflex_route": {"answer": C["R8"]}, "judgments": judg}
    fam = [{"name": "the golden", "answer": G["R8"]}] + [{"name": nm, "answer": r["R8"]} for nm, r in riv.items()]
    pert = []
    for k, s in (("extra cancellations", 0.2), ("extra cancellations", -0.2), ("extra downgrades", 0.2),
                 ("extra downgrades", -0.2)):
        o = dict(GOLD, scale_cancel=1 + s if k == "extra cancellations" else 1.0,
                 scale_down=1 + s if k == "extra downgrades" else 1.0)
        pert.append({"input": "%s %+d%%" % (k, round(100 * s)), "answer": results(pk, o)["R8"]})
    pert.append({"input": "the response where a rise passes the rival half as large again",
                 "answer": results(pk, dict(GOLD, dose="cross15"))["R8"]})
    for k, sc in (("scale_announce", 1.2), ("scale_announce", 0.8), ("scale_use", 1.2), ("scale_use", 0.8)):
        pert.append({"input": "%s %+d%%" % ("the December leaving" if k == "scale_announce" else "the stayers' extra "
                                            "listening", round(100 * (sc - 1))), "answer": results(pk, dict(GOLD, **{k: sc}))["R8"]})
    shortcuts = [{"name": nm, "answer": out[nm]["R8"]} for nm in SINGLE]
    return {"results": res, "hints": hints, "factorial": factorial, "forcing": {"kind": "set", "golden_answer": G["R8"], "golden_family": fam,
                                                          "perturbations": pert, "shortcuts": shortcuts},
            "routes": [{"name": nm, "answer": r["R8"], "golden": nm == "the golden"} for nm, r in out.items()],
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
