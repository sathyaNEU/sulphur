"""generator/effort.json: each result's golden and band, and the value each pass files, computed end to end.

The passes are this generator's own implementations of named methods (results.py), run on the built pack. None reads
the prompt. effort.py grades them and prices the rubric.
"""
import analysis as AN
import golden as GD
import results as RS

CHAIN = [   # id, key, graded as, depends on, figures.json key
    ("R1", "linked", "Ask 4", [], "linked"),
    ("R2", "phone", "Component 1", [], "phone_unkeyed_share"),
    ("R3", "written", "Component 2", [], "written_open"),
    ("R4", "achieved", "Component 3", ["R2", "R3"], "achieved_all"),
    ("R5", "alerts", "Component 4", [], "alert_effect"),
    ("R6", "season", "Component 5", ["R5"], "season"),
    ("R7", "expected", "Ask 2", ["R2", "R3", "R6"], "expected_table"),
    ("R8", "range", "Ask 3", [], "half_table"),
    ("R9", "call", "Recommendation", ["R7"], "keep"),
]
INDEPENDENT = {"R8": "graded on the range's width, which the resampling sets whatever the rate it surrounds"}
HINTS = [
    ("the season's conversations come from its parcels, at each delivery outcome's own contact rate", dict(transport="propensity", alerts="none"), "iid"),
    ("the plan turns the delay alerts on at every depot: measure what they did to contacts at the pilot depots", "alerts_only", "iid"),
    ("resample whole days, because a good or bad day moves every family together", dict(), "day"),
    ("a call with no tracking number can follow a conversation too", dict(capture_how="state"), "iid"),
    ("the case export holds resolved cases only; the backlog report counts the open ones", dict(written="backlog"), "iid"),
]


def value(f, key):
    if key == "linked":
        return {"conversations": f["conversations"], "linked_rate": f["linked_rate"]}
    if key == "phone":
        return f["phone_unkeyed_share"]
    if key == "written":
        return f["written_open"]
    if key == "achieved":
        return f["achieved_all"]
    if key == "alerts":
        return f["alert_effect"] if f["alert_effect"] is not None else {"value": None, "grade": "missed", "why": "this pass carries the observed weeks forward and never measures the alerts"}
    if key == "season":
        if f["late_share"] is None:
            return {"value": None, "grade": "missed", "why": "this pass never builds the season's conversations from the plan's parcels"}
        return {"late_share": f["late_share"], "per_week": f["per_week"]}
    if key == "expected":
        return dict(f["expected"], ALL=f["expected_all"])
    if key == "range":
        return dict(f["half"], ALL=f["half_all"])
    return f["call"]["keep"]


def build(O, F):
    B = GD.bands(F)
    g = RS.figures(O["golden"])
    q = RS.figures(O["linked"]); c = RS.figures(O["careful"])
    results = []
    for rid, key, graded_as, depends, fig in CHAIN:
        e = {"id": rid, "name": RS.NAMES[key], "graded_as": graded_as, "figure": fig, "depends": depends,
             "independent": INDEPENDENT.get(rid, ""), "golden": F[fig]}
        b = B.get(fig)
        if isinstance(b, dict):
            e["bands"] = b
        elif b is not None:
            e["band"] = b
        e["passes"] = {"quick": value(q, key), "careful": value(c, key), "thorough": value(g, key)}
        results.append(e)
    S, D = O["S"], O["D"]
    base = dict(RS.GOLD); base.update(RS.ROUTES["careful"][1])
    hints = []
    for sentence, change, unit in HINTS:
        kw = dict(base)
        if change == "alerts_only":
            R = AN.run(S, D, **kw)
            R["boot"] = AN.bootstrap(S, D, R, B=300, unit="iid", transport=kw["transport"], alerts=kw["alerts"])
            f = RS.figures(R)
            e, _ = AN.alert_effect(S)
            f["alert_effect"] = round(100 * float(e), 0)
        else:
            kw.update(change)
            R = AN.run(S, D, **kw)
            R["boot"] = AN.bootstrap(S, D, R, B=300, unit=unit, transport=kw["transport"], alerts=kw["alerts"])
            f = RS.figures(R)
        resc = [rid for rid, key, _, _, _ in CHAIN if RS.grade(c, g, key) != "right" and RS.grade(f, g, key) == "right"]
        hints.append({"sentence": sentence, "rescues": resc})
    routes = [{"name": "the golden", "answer": g["call"]["keep"], "golden": True}]
    for name, (label, _, _) in RS.ROUTES.items():
        routes.append({"name": label, "answer": RS.figures(O[name])["call"]["keep"]})
    return {"results": results, "hints": hints, "routes": routes}
