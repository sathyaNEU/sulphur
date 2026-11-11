"""task10 architecture 7, levelled up: the three passes of the effort test, each computed end to end on the cut pack by
the generator's own implementations of named methods (estim.analyse under the pass's choices). Nothing here reads
the prompt; it is the paper argument computed.

  quick     ten minutes: each evening half-hour on a straight line through the latest winter's days without a
            service, the customers due after it in full, the megawatts contracted at the share the events delivered
            of their contract, taken off the 17:00 to 18:00 peak, the expected day set against firm capacity; a further
            contract read straight off the margin, the schedule in full, the data hall at its agreed capacity
  careful   an afternoon, calibrated to the two platform runs on architecture 7 (runs/arch7_run1.md, arch7_run2.md):
            every file cleaned, the cold evening rebuilt from the hours before the window, every customer carried up its
            type's build-up, commissioning by class with the sites still to come and the sites withdrawn counted, the
            share capped at the instruction, the day replayed and design days drawn as guideline 7 sets them; and, where
            a result needs a move beyond those, the readings Response 2 gave cell for cell: the mornings on a straight
            line in temperature, and the load that comes back after the window replayed as the megawatts the record's
            events showed (about 2 MW delivered at Ashcombe Road) rather than in proportion to the design day's delivery
  thorough  the golden
"""
import estim as E

CAREFUL = dict(comeback="fixed", mform="linear")
# the same pass with the cold end read as the golden reads it (Response 1's demand figures sit nearer the golden than
# Response 2's): recorded beside the careful pass as a sensitivity, never as the gate
CAREFUL_CURVED = dict(comeback="fixed")
BY_CLASS_NAME = "each class's record read from the sites commissioned alone"
FIXED_NAME = "the come-back as the megawatts the record's events showed, whatever they delivered"
QUICK = dict(baseline="latest", conn="full", comm="contract", avail_base="contract", censor=False, replay=False, tail=False,
             further="contract", customer="full")

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
    (FIXED_NAME, dict(comeback="fixed")),
    ("the mornings on a straight line in temperature", dict(mform="linear")),
    # a further contract on the 2027/28 award's terms
    ("a further megawatt at the share of its contract the zone will have in service", dict(further="zone_ratio")),
    ("every further megawatt in service", dict(further="every")),
    ("a further contract read straight off the nine-days-in-ten level's margin", dict(further="linear")),
    # the data hall
    ("the data hall at its type's established share", dict(customer="mature")),
    ("the data hall at its agreed capacity", dict(customer="full")),
    ("the data hall on one build-up for every type", dict(customer="pooled")),
    # the careful but hurried pass and the quick one
    ("careful but hurried: the mornings on a straight line, the come-back as the record's megawatts", CAREFUL),
    ("quick: the latest winter's line, agreed capacity in full, the contract at face value, the expected day", QUICK),
]
# one sentence of help each, and what the careful pass becomes when it is told that sentence and nothing else
HINTS = [
    ("the load that comes back after the window is in proportion to what the window delivered, and the design day "
     "delivers several times what the record's events did", dict(mform="linear")),
    ("the heating load steepens below freezing, so a straight line through the mornings reads the cold mornings low",
     dict(comeback="fixed")),
    ("a further megawatt on the award's terms is mostly process load still to be commissioned",
     dict(comeback="fixed", mform="linear")),
    ("a data hall takes two years and more to build up to its established draw",
     dict(comeback="fixed", mform="linear")),
]
# two sentences at once: recorded beside the hints (the client's test is one sentence), never as the gate
COMPOUND = [("the come-back and the cold-end sentences together", dict())]


def r1(v):
    v = round(float(v) + 1e-9, 1)
    return 0.0 if v == 0 else v


def verdicts(Z, names):
    """The recommendation, primary by primary: hold, reinforce, or reinforce unless more flexibility is contracted."""
    out = []
    for n in names:
        q = Z[n]
        if not q["commit"]:
            out.append("%s: hold" % n)
        elif q.get("further") is None:
            out.append("%s: reinforce, no further flexibility would do" % n)
        else:
            out.append("%s: reinforce, or contract more flexibility" % n)
    return out


def further_tab(Z, names):
    return {n: ("none" if Z[n].get("further") is None else r1(Z[n]["further"])) for n in names}


def results_of(run, names, pmap, call, quick=False):
    """A pass's value for every result of the chain, at the answer blocks' rounding (pmap: the provider as the files
    key it, to the name the answer blocks use; call: the golden's primaries to reinforce, the rows R12 asks about)."""
    Z = {q["name"]: q for q in run["zones"].values()}
    f = run["fits"]
    sa, ca = Z[E.SCHEDULE_AT[0]], Z[E.CUSTOMER_AT]
    fixed = run["options"].get("comeback") == "fixed"
    out = dict(
        R1={n: r1(Z[n]["before26"]) for n in names},
        R2={n: r1(Z[n]["conn_add"]) for n in names},
        R3={n: r1(Z[n]["before28"]) for n in names},
        R4={n: r1(Z[n]["commissioned"]) for n in names},
        R5={pmap[p]: round(f[p]["share"], 2) for p in pmap},
        R6={n: r1(Z[n]["delivered"]) for n in names},
        R7=None if (quick or fixed) else {pmap[p]: round(float(sum(f[p]["reb"])), 2) for p in pmap},
        R8={n: r1(Z[n]["mean_peak"]) for n in names},
        R9={n: r1(Z[n]["p90"]) for n in names},
        R10={n: int(round(100 * Z[n]["exceed"])) for n in names},
        R11=further_tab(Z, call),
        R12=dict(schedule=r1(sa["schedule"]["schedule"]), one_in_ten=r1(sa["schedule"]["p90"])),
        R13=dict(adds=r1(ca["customer"]["adds"]), one_in_ten=r1(ca["customer"]["p90"])),
        R14=verdicts(Z, names))
    return out


def in_band(v, band):
    return band[0] - 1e-9 <= v <= band[1] + 1e-9


def grade(rid, value, gold, bands):
    """right, partly or missed, by effort.py's own rule: a table is right when every cell is inside its band (or equal,
    where a cell has no band) and partly when half or more are; a set is right when it is the golden's."""
    if value is None:
        return "missed"
    if isinstance(gold, list):
        a, b = set(value), set(gold)
        return "right" if a == b else ("partly" if len(a & b) / float(len(a | b) or 1) >= 0.5 else "missed")
    ok = 0
    for k in gold:
        v, b = value.get(k), (bands.get(rid) or {}).get(k)
        if b is not None and isinstance(v, (int, float)) and not isinstance(v, bool):
            ok += in_band(v, b)
        else:
            ok += v == gold[k]
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
    ("R11", "the further megawatts each primary to reinforce would need on its award's terms, or none", "Ask 6",
     "r12_further", ["R4", "R5", "R7", "R9"]),
    ("R12", "Ashcombe Road's schedule for the lowest share over firm, and its nine-days-in-ten level there", "Ask 7",
     "r13_schedule", ["R3", "R6", "R7"]),
    ("R13", "the data hall's megawatts by the assessment date, and Hartwell Common's nine-days-in-ten level with it",
     "Ask 8", "r14_customer", ["R2", "R9"]),
    ("R14", "each primary's call: hold, reinforce, or reinforce unless more flexibility is contracted", "Recommendation",
     "r11_verdicts", ["R9", "R11"]),
]
INDEPENDENT = {"R5": "the events, the asset register and the SCADA record",
               "R7": "the half-hours after the window on the event days themselves"}


def effort_json(X, F, G):
    """effort.json's object, the careful and the quick runs, and every shortcut's run."""
    names = F["order"]
    call = F["call"]
    pmap = {v["key"]: d for d, v in F["providers"].items()}
    C = E.analyse(X, **CAREFUL)
    Q = E.analyse(X, **QUICK)
    gold = {m[0]: F[m[3]] for m in META}
    B = F["bands_by_result"]
    rc, rq = results_of(C, names, pmap, call), results_of(Q, names, pmap, call, quick=True)
    results = []
    for rid, name, graded, fig, dep in META:
        d = dict(id=rid, name=name, graded_as=graded, figure=fig, depends=dep, independent=INDEPENDENT.get(rid, ""),
                 golden=gold[rid], passes=dict(quick=rq[rid], careful=rc[rid], thorough=gold[rid]))
        if rid != "R14":
            d["bands"] = {k: v for k, v in (B[rid] or {}).items() if v is not None}
        results.append(d)
    base = {rid: grade(rid, rc[rid], gold[rid], B) for rid in gold}
    hints, hint_runs = [], {}
    for sentence, opts in HINTS:
        run = E.analyse(X, **opts)
        rv = results_of(run, names, pmap, call)
        rescued = [rid for rid in gold if base[rid] != "right" and grade(rid, rv[rid], gold[rid], B) == "right"]
        hints.append(dict(sentence=sentence, rescues=rescued, commits=rv["R14"]))
        hint_runs[sentence] = run
    compound = []
    for sentence, opts in COMPOUND:
        rv = results_of(E.analyse(X, **opts), names, pmap, call)
        compound.append(dict(sentence=sentence, commits=rv["R14"],
                             rescues=[rid for rid in gold if base[rid] != "right" and grade(rid, rv[rid], gold[rid], B) == "right"]))
    routes = [dict(name="every result of the chain", answer=list(F["r11_verdicts"]), golden=True)]
    runs = {}
    for name, opts in SHORTCUTS:
        run = C if opts is CAREFUL else (Q if opts is QUICK else E.analyse(X, **opts))
        runs[name] = run
        routes.append(dict(name=name, answer=verdicts({q["name"]: q for q in run["zones"].values()}, names)))
    # the sensitivity: the careful pass with the cold end read as the golden reads it
    S = E.analyse(X, **CAREFUL_CURVED)
    rs = results_of(S, names, pmap, call)
    gs = {rid: grade(rid, rs[rid], gold[rid], B) for rid in gold}
    block = {m[0]: m[2].split()[0] for m in META}
    n_comp = sum(1 for m in META if block[m[0]] == "Component")
    n_ask = sum(1 for m in META if block[m[0]] == "Ask")
    weight = {"Recommendation": 14.0, "Component": 24.0 / n_comp, "Ask": 55.0 / n_ask}
    score = 7.0 + sum(weight[block[rid]] * {"right": 1.0, "partly": 0.5, "missed": 0.0}[gs[rid]] for rid in gold)
    told = []
    for sentence, opts in (
            ("the load that comes back is in proportion to what the window delivered", dict()),):
        rv = results_of(E.analyse(X, **opts), names, pmap, call)
        told.append(dict(sentence=sentence, commits=rv["R14"],
                         rescues=[rid for rid in gold if gs[rid] != "right" and grade(rid, rv[rid], gold[rid], B) == "right"]))
    sens = dict(name="the careful but hurried pass with the cold end read as a curve (the come-back still the record's megawatts)",
                commits=rs["R14"], grades=gs, results=rs, earned=sum({"right": 1.0, "partly": 0.5, "missed": 0.0}[g] for g in gs.values()),
                score=round(score, 1), hints=told,
                margins={q["name"]: q["p90"] - q["firm"] for q in S["zones"].values()})
    return dict(results=results, hints=hints, compound=compound, routes=routes, sensitivity=sens), C, Q, runs
