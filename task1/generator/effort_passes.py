"""Every owed figure computed from the cut pack (methods.py on target/), the rivals that set each band, the named
shortcuts and the three passes, written as figures.json and effort.json (architecture 5: the January 2027 rises)."""
import methods as M
import params as P

NAMES = {"FLEX": "Flex", "STD": "Standaard", "ONB": "Onbeperkt", "GEZ": "Gezin"}
CTY = {"NL": "Netherlands", "BE": "Flanders"}
GOLD = M.GOLD
CAREFUL = M.opts(resp="plan", down_as_exit=True, who="avg")
QUICK = M.opts(resp="pooled", cost="share26", channels=("live",), member="today", down_as_exit=True, who="avg",
               r1="open")
RIVALS = {
    "the same country a year earlier as the control where the record holds it": M.opts(control="prior"),
    "the first bill alone as the response window": M.opts(window="first"),
    "downgraders valued on their own hours capped at the lower plan's, with the cap response": M.opts(dval="model"),
    "re-sent warehouse rows summed": M.opts(dedup=False),
}
ROUTES = {
    "the golden": GOLD,
    "the careful route: each plan's own past response, a downgrade counted as an exit, leavers at the plan's average": CAREFUL,
    "one response for every rise, scaled by the rise": M.opts(resp="pooled"),
    "each plan's own past response": M.opts(resp="plan"),
    "the response read off the new price's gap to the rival, in a straight line": M.opts(resp="gap"),
    "a downgrade counted as an exit from the plan": M.opts(down_as_exit=True),
    "the 2026 remuneration basis carried (52 per cent of net revenue)": M.opts(cost="share26"),
    "the quick route": QUICK,
}
SINGLE = ["one response for every rise, scaled by the rise", "each plan's own past response",
          "the response read off the new price's gap to the rival, in a straight line",
          "the 2026 remuneration basis carried (52 per cent of net revenue)"]
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
    for key, w in (("R2", 0.01), ("R3", 0.05), ("R4", 0.05), ("R5", 0.01), ("R6", 0.01), ("R7", 0.03)):
        bands[key] = {k: _band([v] + [r[key][k] for r in riv.values()], max(w * abs(v), floor[key]))
                      for k, v in G[key].items()}
    fig = {
        "raise": G["R8"], "hold": sorted(NAMES[p] for p in P.PLANS if NAMES[p] not in G["R8"]),
        "careful_raise": C["R8"], "quick_raise": Q["R8"],
        "paying_oct": {NAMES[k]: v for k, v in G["R1"].items()}, "paying_oct_total": sum(G["R1"].values()),
        "counted_per_month": _r(G["R2"], 2),
        "extra_cancel": _r(G["R3"]), "extra_down": _r(G["R4"]), "downgrader_value": _r(G["R5"]),
        "leaver_hours_ratio": _r(G["R6"], 2), "change_2027": _r(G["R7"]),
        "careful": {"extra_cancel": _r(C["R3"]), "change_2027": _r(C["R7"]), "leaver_hours_ratio": _r(C["R6"], 2)},
        "bands": bands,
        "events": [{"year": r["year"], "country": CTY[r["country"]], "plan": NAMES[r["plan"]], "subscriptions": r["n"],
                    "crossed": bool(r["cross"]), "extra_cancel": round(100 * r["x_cancel"], 1),
                    "extra_down": round(100 * r["x_down"], 1)} for r in G["rows"]],
        "routes": {nm: {"raise": r["R8"], "change_2027": _r(r["R7"])} for nm, r in out.items()},
        "rival_family": {nm: r["R8"] for nm, r in riv.items()},
        "price26": {NAMES[k]: v for k, v in P.PRICE.items()}, "price27": {NAMES[k]: v for k, v in P.PRICE27.items()},
        "rival_nl": {NAMES[k]: v for k, v in P.RIVAL["NL"].items()},
        "rival_be": {NAMES[k]: v for k, v in P.RIVAL["BE"].items()},
        "rate": P.RATE27, "clauses": [2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.5, 3.8, 3.9, 3.10],
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
         "golden": fig["extra_cancel"], "bands": b["R3"], "precedent": ["L15", "N02"], "partly_share": 0.75,
         "passes": {"quick": _r(Q["R3"]), "careful": _r(C["R3"]), "thorough": fig["extra_cancel"]}},
        {"id": "R4", "name": "extra downgrades per 100 subscriptions at the first 2027 bill, by plan and region",
         "graded_as": "Ask 3", "figure": "extra_down", "depends": [], "independent": "the 2025 and 2026 rises",
         "golden": fig["extra_down"], "bands": b["R4"], "precedent": ["L15", "L06"], "partly_share": 0.75,
         "passes": {"quick": _r(Q["R4"]), "careful": _r(C["R4"]), "thorough": fig["extra_down"]}},
        {"id": "R7", "name": "each plan's change in its October 2026 base's 2027 contribution if its rise goes ahead",
         "graded_as": "Component 1", "figure": "change_2027", "depends": ["R3", "R4"], "independent": "",
         "golden": fig["change_2027"], "bands": b["R7"], "precedent": ["L15", "L17"],
         "passes": {"quick": _r(Q["R7"]), "careful": _r(C["R7"]), "thorough": fig["change_2027"]}},
        {"id": "R8", "name": "the rises that go ahead", "graded_as": "Recommendation", "figure": "raise", "depends": ["R7"],
         "independent": "", "golden": fig["raise"], "precedent": ["L15", "L06"],
         "passes": {"quick": Q["R8"], "careful": C["R8"], "thorough": fig["raise"]}},
    ]

    def inb(R, key):
        return all(b[key][k][0] <= v <= b[key][k][1] for k, v in R[key].items())

    def rescues(o):
        R = results(pk, o)
        got = [k for k in ("R3", "R4", "R7") if inb(R, k)]
        return got + (["R8"] if R["R8"] == G["R8"] else [])
    hints = [
        {"sentence": "a rise's cancellations and downgrades jump only where the new price passes the rival's comparable plan",
         "rescues": rescues(dict(CAREFUL, resp="plan_cross"))},
        {"sentence": "a subscription that moves down a plan is kept, not lost", "rescues": rescues(dict(CAREFUL, down_as_exit=False))},
        {"sentence": "the subscriptions that leave at a rise listen less than their plan's average",
         "rescues": rescues(dict(CAREFUL, who="own"))},
    ]
    fam = [{"name": "the golden", "answer": G["R8"]}] + [{"name": nm, "answer": r["R8"]} for nm, r in riv.items()]
    pert = []
    for k, s in (("extra cancellations", 0.2), ("extra cancellations", -0.2), ("extra downgrades", 0.2),
                 ("extra downgrades", -0.2)):
        o = dict(GOLD, scale_cancel=1 + s if k == "extra cancellations" else 1.0,
                 scale_down=1 + s if k == "extra downgrades" else 1.0)
        pert.append({"input": "%s %+d%%" % (k, round(100 * s)), "answer": results(pk, o)["R8"]})
    shortcuts = [{"name": nm, "answer": out[nm]["R8"]} for nm in SINGLE]
    return {"results": res, "hints": hints, "forcing": {"kind": "set", "golden_answer": G["R8"], "golden_family": fam,
                                                          "perturbations": pert, "shortcuts": shortcuts},
            "routes": [{"name": nm, "answer": r["R8"], "golden": nm == "the golden"} for nm, r in out.items()],
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
