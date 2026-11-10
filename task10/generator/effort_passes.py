"""task10 architecture 7: the three passes of the effort test, each computed end to end on the cut pack by the
generator's own implementations of named methods (estim.analyse under the pass's choices). Nothing here reads the
prompt; it is the paper argument computed.

  quick     ten minutes: each evening half-hour on a straight line through the latest winter's days without a
            service, the customers due after it in full, the megawatts contracted at the share the events delivered
            of their contract, taken off the 17:00 to 18:00 peak, the expected day set against firm capacity
  careful   an afternoon, calibrated to what the two platform runs on architecture 6 did unprompted: every file
            cleaned, the switching days left out, an event's megawatts measured against the day's own morning, the
            share capped at the instruction and taken on the megawatts in service (the guideline's words), the load
            that comes back replayed over the day, a predictive nine-in-ten level; and, where a result needs a move
            beyond those, the reading both runs gave: a straight line through the days without a service carried to
            the design temperature, the customers due after the latest winter at their type's established share of
            agreed capacity, and the sites still to come on their planned dates
  thorough  the golden
"""
import estim as E

CAREFUL = dict(baseline="pooled", conn="mature", comm="planned")
# the same pass if a run also groups the register by asset class and reads each class's lateness from the sites that
# have commissioned (one group-by of one file): recorded beside the careful pass as a sensitivity, never as the gate
CAREFUL_BY_CLASS = dict(baseline="pooled", conn="mature", comm="class_done")
BY_CLASS_NAME = "each class's record read from the sites commissioned alone"
QUICK = dict(baseline="latest", conn="full", comm="contract", avail_base="contract", censor=False, replay=False, tail=False)

# every shortcut a design-note row names, by the judgment it misses; the set each commits is a route in effort.json
SHORTCUTS = [
    # the days without a service read as design days
    ("each evening half-hour on a straight line through the days no service ran, three winters", dict(baseline="pooled")),
    ("the same line through the latest winter's days alone", dict(baseline="latest")),
    ("every working weekday with the megawatts scheduled as a regressor", dict(baseline="sched")),
    # what the register's customers add
    ("customers due after the latest winter, agreed capacity in full", dict(conn="full")),
    ("the same customers at the average share today's customers draw", dict(conn="ratio")),
    ("the same customers at their type's established share", dict(conn="mature")),
    ("the same customers on their type's build-up", dict(conn="new_buildup")),
    ("every customer at what the latest months show, no further build-up", dict(conn="observed")),
    # what will be in service
    ("the megawatts contracted, at the share the events delivered of their contract", dict(comm="contract", avail_base="contract")),
    ("the megawatts contracted, at the share of megawatts in service", dict(comm="contract")),
    ("the sites still to come on their planned dates", dict(comm="planned")),
    ("the zone's own past share of its contract in service in mid January", dict(comm="zone_ratio")),
    ("the sites still to come on the provider's record across its classes", dict(comm="provider")),
    ("the sites still to come on the register's record across every class", dict(comm="all")),
    (BY_CLASS_NAME, dict(comm="class_done")),
    # the day
    ("the delivery taken off the 17:00 to 18:00 peak", dict(replay=False)),
    # the careful but hurried pass and the quick one
    ("careful but hurried: the line, the type's established share, the planned dates", CAREFUL),
    ("quick: the latest winter's line, agreed capacity in full, the contract at face value, the expected day", QUICK),
]
# one sentence of help each, and what the careful pass becomes when it is told that sentence and nothing else
HINTS = [
    ("the days without a service stop near 2 C and are the low-running ones, and the heating load steepens below "
     "freezing: read the cold end from the hours before the window, which every day carries",
     dict(conn="mature", comm="planned")),
    ("a customer draws a share of its agreed capacity that depends on its type and takes two to three years to reach "
     "it: count every register customer's rise between the two assessment dates", dict(baseline="pooled", comm="planned")),
    ("a provider's availability follows the megawatts in service, and the sites still to come commission as late as "
     "their class has across the register, not on the planned dates", dict(baseline="pooled", conn="mature")),
    ("both of the first two sentences (the cold end and the customers' build-up)", dict(comm="planned")),
    ("both the cold end and the commissioning sentences", dict(conn="mature")),
    ("both the build-up and the commissioning sentences", dict(baseline="pooled")),
]


def r1(v):
    v = round(float(v) + 1e-9, 1)
    return 0.0 if v == 0 else v


def results_of(run, names, pmap, quick=False):
    """A pass's value for every result of the chain, at the answer blocks' rounding (pmap: the provider as the files
    key it, to the name the answer blocks use)."""
    Z = {q["name"]: q for q in run["zones"].values()}
    f = run["fits"]
    out = dict(
        R1={n: r1(Z[n]["before26"]) for n in names},
        R2={n: r1(Z[n]["conn_add"]) for n in names},
        R3={n: r1(Z[n]["before28"]) for n in names},
        R4={n: r1(Z[n]["commissioned"]) for n in names},
        R5={pmap[p]: round(f[p]["share"], 2) for p in pmap},
        R6={n: r1(Z[n]["delivered"]) for n in names},
        R7=None if quick else {pmap[p]: round(float(sum(f[p]["reb"])), 2) for p in pmap},
        R8={n: r1(Z[n]["mean_peak"]) for n in names},
        R9={n: r1(Z[n]["p90"]) for n in names},
        R10={n: int(round(100 * Z[n]["exceed"])) for n in names},
        R11=[n for n in names if Z[n]["commit"]])
    return out


def in_band(v, band):
    return band[0] - 1e-9 <= v <= band[1] + 1e-9


def grade(rid, value, gold, bands):
    """right, partly or missed, by effort.py's own rule: a table is right when every cell is inside its band and
    partly when half or more are; a set is right when it is the golden's."""
    if value is None:
        return "missed"
    if isinstance(gold, list):
        a, b = set(value), set(gold)
        return "right" if a == b else ("partly" if len(a & b) / float(len(a | b) or 1) >= 0.5 else "missed")
    ok = sum(1 for k in gold if value.get(k) is not None and in_band(value[k], bands[rid][k]))
    share = ok / float(len(gold))
    return "right" if share >= 0.999 else ("partly" if share >= 0.5 else "missed")


META = [
    ("R1", "design-day demand in winter 2025/26, MW", "Component 1", "r1_demand_2526", []),
    ("R2", "megawatts the register's customers add by 15 January 2028", "Component 2", "r2_connections", []),
    ("R3", "design-day demand before flexibility in winter 2027/28, MW", "Ask 1", "r3_before", ["R1", "R2"]),
    ("R4", "megawatts each provider will have in service on the assessment date", "Component 3", "r4_in_service", []),
    ("R5", "the share of its megawatts in service each provider has available on the design day", "Component 4",
     "r5_share", []),
    ("R6", "megawatts each contract delivers between 17:00 and 18:00", "Ask 2", "r6_delivered", ["R4", "R5"]),
    ("R7", "megawatts that come back after the window per megawatt delivered", "Component 5", "r7_comeback", []),
    ("R8", "the day's expected peak with the service instructed in full, MW", "Ask 3", "r8_peak", ["R3", "R6", "R7"]),
    ("R9", "the level the peak stays under on nine design days in ten, MW", "Ask 4", "r9_one_in_ten", ["R3", "R6", "R7"]),
    ("R10", "the share of design days over firm capacity, per cent", "Ask 5", "r10_share_over", ["R3", "R6", "R7"]),
    ("R11", "the primaries to reinforce", "Recommendation", "call", ["R9"]),
]
INDEPENDENT = {"R5": "the events, the asset register and the SCADA record",
               "R7": "the half-hours after the window on the event days themselves"}


def effort_json(X, F, G):
    """effort.json's object, the careful and the quick runs, and every shortcut's run."""
    names = F["order"]
    pmap = {v["key"]: d for d, v in F["providers"].items()}
    C = E.analyse(X, **CAREFUL)
    Q = E.analyse(X, **QUICK)
    gold = {m[0]: F[m[3]] for m in META}
    B = F["bands_by_result"]
    rc, rq = results_of(C, names, pmap), results_of(Q, names, pmap, quick=True)
    results = []
    for rid, name, graded, fig, dep in META:
        d = dict(id=rid, name=name, graded_as=graded, figure=fig, depends=dep, independent=INDEPENDENT.get(rid, ""),
                 golden=gold[rid], passes=dict(quick=rq[rid], careful=rc[rid], thorough=gold[rid]))
        if rid != "R11":
            d["bands"] = B[rid]
        results.append(d)
    base = {rid: grade(rid, rc[rid], gold[rid], B) for rid in gold}
    hints, hint_runs = [], {}
    for sentence, opts in HINTS:
        run = E.analyse(X, **opts)
        rv = results_of(run, names, pmap)
        rescued = [rid for rid in gold if base[rid] != "right" and grade(rid, rv[rid], gold[rid], B) == "right"]
        hints.append(dict(sentence=sentence, rescues=rescued, commits=rv["R11"]))
        hint_runs[sentence] = run
    routes = [dict(name="every result of the chain", answer=list(F["call"]), golden=True)]
    runs = {}
    for name, opts in SHORTCUTS:
        run = C if opts is CAREFUL else (Q if opts is QUICK else E.analyse(X, **opts))
        runs[name] = run
        routes.append(dict(name=name, answer=[n for n in names if {q["name"]: q for q in run["zones"].values()}[n]["commit"]]))
    # the sensitivity: the careful pass with each class's lateness read from the commissioned sites
    S = E.analyse(X, **CAREFUL_BY_CLASS)
    rs = results_of(S, names, pmap)
    gs = {rid: grade(rid, rs[rid], gold[rid], B) for rid in gold}
    block = {m[0]: m[2].split()[0] for m in META}
    weight = {"Recommendation": 14.0, "Component": 24.0 / 5, "Ask": 55.0 / 5}
    score = 7.0 + sum(weight[block[rid]] * {"right": 1.0, "partly": 0.5, "missed": 0.0}[gs[rid]] for rid in gold)
    told = []
    for sentence, opts in (
            ("the cold end read from the hours before the window", dict(conn="mature", comm="class_done")),
            ("every register customer's rise on its type's build-up", dict(baseline="pooled", comm="class_done")),
            ("the sites still to come and the sites withdrawn counted in each class's record", dict(baseline="pooled", conn="mature")),
            ("the cold end and the build-up together", dict(comm="class_done")),
            ("the cold end and the sites still to come together", dict(conn="mature")),
            ("the build-up and the sites still to come together", dict(baseline="pooled"))):
        rv = results_of(E.analyse(X, **opts), names, pmap)
        told.append(dict(sentence=sentence, commits=rv["R11"],
                         rescues=[rid for rid in gold if gs[rid] != "right" and grade(rid, rv[rid], gold[rid], B) == "right"]))
    sens = dict(name="the careful but hurried pass with each class's lateness read from the sites commissioned alone",
                commits=rs["R11"], grades=gs, results=rs, earned=sum({"right": 1.0, "partly": 0.5, "missed": 0.0}[g] for g in gs.values()),
                score=round(score, 1), hints=told,
                margins={q["name"]: q["p90"] - q["firm"] for q in S["zones"].values()})
    return dict(results=results, hints=hints, routes=routes, sensitivity=sens), C, Q, runs
