#!/usr/bin/env python3
"""corelib.py: the checker every task's generator/core.py ends on (stumping SKILL.md Part 1d,
references/core-method.md). The architect writes the world and the estimators; this file decides whether what they
print is a core, and at which level. It is arithmetic on the spec: nothing here reads a prompt or solves a task.

    # taskNN/generator/core.py
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".agents", "skills", "stumping"))
    import corelib
    spec = {...}                      # built from the world's arrays, never typed
    sys.exit(corelib.run(spec))       # prints the core table and CORE PASS level N, or CORE FAIL

    python3 .agents/skills/stumping/corelib.py selftest

The spec:

  call      "lines" (each member is read against its own line or lines; the default) or "top_k" (the call is the k
            members with the largest figures; give "k")
  members   {name: {"lines": [x, ...],          one line, or several for a banded call ("top_k": omit)
                    "truth": x,                  the world's own value
                    "golden": x,                 the golden estimator's figure from what the files hold
                    "family": [x, ...],          twelve or more defensible rebuilds of the golden's conventions
                    "routes": {"direct": x, "rigorous": x, ...}}}   the pack's most direct evidence read raw, and
                                                 the most rigorous standard design the pack affords; both required
  stumps    {id: {"axis": who | what | when | against | unit,
                  "opens": member,               the member this judgment brings back
                  "said_out_loud": sentence,     the stump's problem as if the prompt carried it
                  "steps_left": n,               dependent steps still to do once that sentence is known
                  "precedents": [ids],           loss or named_assumption ids in references/precedents.json
                  "sides": {"over": {member: x, ...}}}}   every member's figure with this stump alone pushed past
                                                 its fitted value to the far end a run might set (the default's
                                                 mirror: a receiver worth nothing, hours raised in proportion) and
                                                 everything else golden; it files a wrong call too, so a run that
                                                 over-corrects the stump does not land the call (task3 arch 9)
  lattice   {"S1": {member: x, ...}, "S1+S2": {...}, ...}   every member's figure with exactly those stumps made
            the hurried way and everything else golden. Required keys: each stump alone, all together (the reflex
            route), and all but one (each stump fixed alone on the reflex route).
  referee   {"slice": text, "covers_target": false, "truth": x, "golden": x, "rivals": {route: x, ...}}, or
  falsification {"check": text, "observes_target": false, "truth": x, "golden": x, "rivals": {route: x, ...}}
            what forces the call between estimators. A referee is a slice where the hidden quantity is known; a
            falsification check is a statistic of the members' own records that the golden's model reproduces and
            each rival's misses (example 17's within-group share across the deadline bands), with no file observing
            the target or a stump's quantity. One of the two is required. A referee is a calibration set first: a
            pack that ships one prices the calibrated run route on it (task3 arch 8's two runs calibrated the whole
            chain on the research valley's gauges and landed every class).
  run_routes {"generous": {member: x, ...}, "calibrated": {member: x, ...} | {"none": why},
              "hedge": {member: x, ...}, "cutoff": {member: x, ...} | {"none": why}}
            the routes frontier runs were seen to take, each implemented on the world's arrays and each filing a
            wrong call (task3 arch 8, both runs on every class against a paper pair of 26.7; the approved sheets of
            2026-11-14; examples 16 and 17). generous: every correction the pack suggests applied in full, at the
            strength the data allows, with the estimate's uncertainty integrated into the figure (expected counts
            over a fitted spread, not a point plug). calibrated: the whole chain calibrated end to end on any slice
            that observes the target or a stump's quantity, conditioned on every other instrument shipped, and
            carried to the members ("none" only when no file observes either). hedge: every signal noticed and
            reported as a sensitivity, the face value kept as the central figure. cutoff: each signal handled by a
            filter, a threshold or a subset instead of a fitted model ("none" when no signal admits one). Across
            the lattice and these routes the misses fall on both sides of a line, so no blanket adjustment lands the
            call; each route is priced on the rubric like the rigorous standard one, its member figures read from
            its map and every other figure from the figure's "routes". A route that takes a free setting (the cut
            of a filter, the slice a calibration is run on, the share a hedge keeps) is implemented against each
            stump's own mechanism and priced over its whole family: every setting a run could choose is a further
            key "<route>:<label>" ({member: x}), and every one of them files a wrong call (task3 arch 9: the
            filter a run puts in place of the replay, the well-covered days cut to the thin stations' storm size,
            filed the golden's call at every cut from 5 to 12 strokes while the route the core priced was another
            filter).
  figures   every figure the answer blocks will state (the recommendation is the call itself and is not listed).
            Each figure sentence of the blocks is one rubric criterion, all or nothing: figures stated in one
            sentence share a "sentence" id and are earned together, and a figure with none is its own sentence:
            {"id": "F3", "block": "component" | "ask", "weight": 1.0 (relative inside its block),
             "sentence": id (optional),
             "member": name}                     the member's own figure: golden, family, lattice and routes are
                                                 read from the member, or
            {"id": ..., "block": ..., "golden": x, "family": [x, ...] (twelve or more), "band": [lo, hi] (optional:
             the family's range with a quarter of its width as room on each side; "exact": true for a count or a
             set, which carries neither),
             "lattice": {"S1": x, "S1+S2": x, ...},   the figure on the same keys as the members' lattice
             "routes": {"rigorous": x}}               the figure on the most rigorous standard route

The rubric (supplemental-stumping Part 0). The generated rubrics on file split 18 to the recommendation, about 20 to
the critical components, about 53 to the asks and 9 to instruction-following, which every run earns. A route earns
a figure when its value sits inside the figure's band stretched by NEAR_MISS about the golden (a narrower miss is a
near miss, which the review gives back), and a criterion when it earns every figure of its sentence (the generated
rubrics made one criterion of a sentence naming several figures, and it needs them all). corelib prices every route
of the lattice on that rubric and refuses a core
where a run that loses any one stump still clears ONE_LOST_MAX, where the reflex route clears REFLEX_MAX, or where
fixing one stump alone on the reflex route earns nothing or more than a third.

The critical components are the decisive steps (the client's guidelines of 11/20, guidelines/client/
guidelines-2026-11-20.md: "list the two or more decisive, challenging steps and the correct answer to each", "a model
that gets one step wrong should still be able to earn the others"). So every component figure is one stump's own:
it is lost when that stump is lost alone and earned when any other stump is lost alone, and every stump has one. A
figure that falls with two stumps is an ask. A core whose card was registered before INDEPENDENT_FROM meets this as
WARN.
"""
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AXES = ("who", "what", "when", "against", "unit")
WORTH = 3.0          # a stump's worth on its member, over the honest family's spread there
REFEREE = 3.0        # each rival's error on the referee slice, over the golden's
FAMILY_MIN = 12
STEPS_MIN = 3
BLOCKS = {"recommendation": 18.0, "components": 20.0, "asks": 53.0, "instruction": 9.0}
# Holistic Audit v4 realistic rubric model: 1 check per figure (no multi-figure sentence bundling),
# 48% combined recommend+components (matching v4's 45-55% recommend share), 7% IF, and worst-case
# Error Carried Forward (ECF) on arithmetic rollups/totals tagged "ecf": true.
V4_BLOCKS = {"recommendation": 14.0, "components": 34.0, "asks": 45.0, "instruction": 7.0}
ONE_LOST_MAX = 50.0  # what a run that loses any one stump, and nothing else, may still earn (the bar is 60)
V4_TWO_LOST_MAX = 35.0  # with 2+ stumps lost under v4-ECF, scores land in the 20s-35s (never borderline 55-65)
V4_REFLEX_MAX = 25.0    # zero-stump / naive run under v4-ECF (0 free texture/base asks)
REFLEX_MAX = 30.0    # what the reflex route (every stump lost) may earn; the design aims at the twenties
HINT_MAX = 100.0 / 3  # what fixing one stump alone on the reflex route may add
BAND_ROOM = 0.25     # a default band: the family's range and a quarter of its width on each side
NEAR_MISS = 1.5      # a figure counts as lost only outside its band stretched by this about the golden
INDEPENDENT_FROM = "2026-11-21T08:00:00Z"   # the client's guidelines of 11/20: the critical components independent
RUN_ROUTES = ("generous", "calibrated", "hedge", "cutoff")
RUNS_FROM = "2026-11-21T21:45:00Z"   # task3 arch 8's runs: the gates' opponent is the runs' recorded routes
V4_HARDENED_FROM = "2026-11-23T21:00:00Z"   # task27/task9/task1 returns: v4-ECF split rubric, coupled matrix, coded one-fact catch check


def _key(ids):
    return "+".join(sorted(ids))


def _band(x, lines):
    return sum(1 for l in sorted(lines) if x >= l)


def _calls(spec, figures):
    """The call a set of figures files: a band per member, or the top-k set."""
    members = spec["members"]
    if spec.get("call", "lines") == "top_k":
        k = int(spec.get("k", 1))
        order = sorted(members, key=lambda m: (-figures[m], m))
        return tuple(sorted(order[:k]))
    return tuple(_band(figures[m], members[m]["lines"]) for m in sorted(members))


def _member_call(spec, m, x, figures=None):
    if spec.get("call", "lines") == "top_k":
        f = dict(figures)
        f[m] = x
        return m in _calls(spec, f)
    return _band(x, spec["members"][m]["lines"])


def _precedent_kinds():
    try:
        rows = json.load(open(os.path.join(HERE, "references", "precedents.json")))["precedents"]
        return {r["id"]: r["kind"] for r in rows}
    except Exception:
        return {}


def _registered(spec):
    """When the card of the task this core belongs to was registered ("" for an unfiled draw or a selftest). The
    task is read from the spec's label, or from the folder of the core.py that is running (taskNN/generator)."""
    m = re.match(r"\s*(task\d+)\b", str(spec.get("task") or ""))
    if not m and not spec.get("task"):
        main = getattr(sys.modules.get("__main__"), "__file__", "") or ""
        m = re.search(r"(task\d+)[\\/]generator[\\/][^\\/]+$", os.path.abspath(main)) if main else None
    if not m:
        return ""
    try:
        card = os.path.join(HERE, "..", "fingerprint", "cards", m.group(1) + ".json")
        return json.load(open(card)).get("registered") or ""
    except Exception:
        return ""


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _same(a, b):
    if _num(a) and _num(b):
        return abs(a - b) <= 1e-9 * max(1.0, abs(b))
    if isinstance(a, (list, tuple, set)) and isinstance(b, (list, tuple, set)):
        return sorted(map(str, a)) == sorted(map(str, b))
    return str(a).strip().lower() == str(b).strip().lower()


def _figures(spec, lat):
    """Every graded figure resolved to its block, weight, golden, band, family and its value on each lattice key."""
    out, problems = [], []
    members = spec.get("members") or {}
    blocks = {"component": "components", "components": "components", "ask": "asks", "asks": "asks"}
    for f in spec.get("figures") or []:
        fid = str(f.get("id") or f.get("member") or "?")
        m = f.get("member")
        if m is not None:
            if m not in members:
                problems.append("%s names no member" % fid)
                continue
            golden, family = members[m]["golden"], list(members[m].get("family") or [])
            values = {k: v.get(m) for k, v in lat.items()}
            routes = dict(members[m].get("routes") or {})
        else:
            golden, family = f.get("golden"), list(f.get("family") or [])
            values = {_key(k.split("+")): v for k, v in (f.get("lattice") or {}).items()}
            routes = {}
        routes.update(f.get("routes") or {})
        band = f.get("band")
        if band is None and _num(golden) and family:
            lo, hi = min(family + [golden]), max(family + [golden])
            band = [lo - BAND_ROOM * (hi - lo), hi + BAND_ROOM * (hi - lo)]
        block = blocks.get(str(f.get("block") or "").lower())
        if block is None:
            problems.append("%s has no block (component or ask)" % fid)
        exact = bool(f.get("exact")) or not _num(golden)
        if "ecf" in f or "rollup" in f:
            is_ecf = bool(f.get("ecf") or f.get("rollup"))
        else:
            # Auto-detect arithmetic rollups (totals, EUR/USD sums, shares, corridor/quarter sums) on non-member asks
            # because Holistic Audit v3/v4 routinely applies Error Carried Forward to them (task27: 18 pts, task9: 30 pts).
            is_ecf = (
                block == "asks"
                and m is None
                and bool(re.search(
                    r"(?:^|_)(?:total|sum|eur|usd|cost|avoidable|share|pct|remed_days|corridor|quarter|q[1-4]|bhv|ham|whv)(?:$|_|\d)",
                    fid.lower(),
                ))
            )
        out.append({"id": fid, "block": block, "weight": float(f.get("weight", 1.0)), "golden": golden,
                    "band": None if exact else band, "family": family, "values": values, "routes": routes,
                    "member": m, "exact": exact, "sentence": str(f.get("sentence") or fid),
                    "ecf": is_ecf})
    return out, problems


def _v4_enforced(spec):
    if spec.get("v4_hardened"):
        return True
    reg = _registered(spec)
    return bool(reg) and reg >= V4_HARDENED_FROM


def _criteria(fs):
    """The figures of one block as rubric criteria: the figures of one sentence are one criterion."""
    crit = {}
    for f in fs:
        crit.setdefault(f["sentence"], []).append(f)
    return list(crit.values())


def _earned(f, x):
    """True when a route's value earns the figure: inside the band stretched by NEAR_MISS about the golden."""
    g, band = f["golden"], f["band"]
    if x is None:
        return False
    if not _num(g) or not _num(x) or band is None:
        return _same(x, g)
    return g - NEAR_MISS * (g - band[0]) <= x <= g + NEAR_MISS * (band[1] - g)


def _score(figs, call_right, value_of):
    """What a route earns on the rubric: instruction-following, the recommendation, and each figure it lands."""
    e = BLOCKS["instruction"] + (BLOCKS["recommendation"] if call_right else 0.0)
    for b in ("components", "asks"):
        crit = _criteria([f for f in figs if f["block"] == b])
        tot = sum(max(f["weight"] for f in c) for c in crit)
        if tot > 0:
            e += BLOCKS[b] * sum(max(f["weight"] for f in c) for c in crit
                                 if all(_earned(f, value_of(f)) for f in c)) / tot
    return e


def _score_v4(figs, call_right, value_of, apply_ecf=True):
    """Holistic Audit v4 realistic rubric score: one independent check per figure (C1.7),
    48% recommend+components (C1.2), 7% IF, and worst-case ECF credit on arithmetic rollups."""
    e = V4_BLOCKS["instruction"] + (V4_BLOCKS["recommendation"] if call_right else 0.0)
    for b in ("components", "asks"):
        fs = [f for f in figs if f["block"] == b]
        tot = sum(f["weight"] for f in fs)
        if tot > 0:
            e += V4_BLOCKS[b] * sum(
                f["weight"] for f in fs
                if (apply_ecf and f.get("ecf")) or _earned(f, value_of(f))
            ) / tot
    return e


def _route_score(spec, figs, route, gcall):
    """(score, the figure with no value on the route) for a named route such as the rigorous standard one. A member
    with no value on the route is taken as right there (a forced member)."""
    members = spec["members"]
    vals = {}
    for f in figs:
        x = f["routes"].get(route)
        if x is None and f["member"] is not None:
            x = f["golden"]
        if x is None:
            return None, f["id"]
        vals[f["id"]] = x
    mfig = {m: (members[m].get("routes") or {}).get(route, members[m]["golden"]) for m in members}
    return _score(figs, _calls(spec, mfig) == gcall, lambda f: vals[f["id"]]), None


def _run_maps(spec):
    """({route: {member: x}} for the run routes given as a figure per member, [the routes missing or malformed])."""
    names = sorted(spec.get("members") or {})
    rr = spec.get("run_routes") or {}
    maps, absent = {}, []
    for name in RUN_ROUTES:
        v = rr.get(name)
        if isinstance(v, dict) and names and all(m in v and _num(v[m]) for m in names):
            maps[name] = {m: float(v[m]) for m in names}
        elif name in ("calibrated", "cutoff") and isinstance(v, dict) and len(str(v.get("none") or "").strip()) >= 20:
            continue
        else:
            absent.append(name)
    return maps, absent


def _run_family(spec):
    """{"<route>:<label>": {member: x}} for the further settings of the run routes (every cut, slice or share a run
    could choose), and [the keys that are malformed]."""
    names = sorted(spec.get("members") or {})
    fam, bad = {}, []
    for k, v in (spec.get("run_routes") or {}).items():
        if ":" not in str(k):
            continue
        if str(k).split(":", 1)[0] in RUN_ROUTES and isinstance(v, dict) and names and all(
                m in v and _num(v[m]) for m in names):
            fam[k] = {m: float(v[m]) for m in names}
        else:
            bad.append(str(k))
    return fam, bad


def _run_route_score(spec, figs, name, mp, gcall):
    """(score, the figure with no value on the route) for one of the runs' recorded routes: a member's figure from the
    route's map, every other figure from its "routes"."""
    vals = {}
    for f in figs:
        x = mp[f["member"]] if f["member"] is not None else f["routes"].get(name)
        if x is None:
            return None, f["id"]
        vals[f["id"]] = x
    return _score(figs, _calls(spec, mp) == gcall, lambda f: vals[f["id"]]), None


def earnings(spec):
    """{"figs", "earn": {lattice key: score}, "rigorous": score or None} for a spec whose lattice is complete."""
    lat = {_key(k.split("+")): v for k, v in (spec.get("lattice") or {}).items()}
    names = sorted(spec["members"])
    gcall = _calls(spec, {m: spec["members"][m]["golden"] for m in names})
    figs, _ = _figures(spec, lat)
    earn = {}
    for k, v in lat.items():
        if all(k in f["values"] for f in figs):
            earn[k] = _score(figs, _calls(spec, v) == gcall, lambda f, k=k: f["values"][k])
    return {"figs": figs, "earn": earn, "rigorous": _route_score(spec, figs, "rigorous", gcall)[0] if figs else None}


def check(spec):
    """Returns (rows, level). rows are (name, PASS | FAIL | WARN, detail)."""
    rows = []

    def row(name, ok, detail, warn=False):
        rows.append((name, "PASS" if ok else ("WARN" if warn else "FAIL"), detail))
        return ok

    members, stumps, lattice = spec.get("members") or {}, spec.get("stumps") or {}, spec.get("lattice") or {}
    names = sorted(members)
    sids = sorted(stumps)
    if not row("shape", len(names) >= 2 and len(sids) >= 2,
               "%d members, %d stumps (two or more of each)" % (len(names), len(sids))):
        return rows, 0
    golden = {m: members[m]["golden"] for m in names}
    truth = {m: members[m]["truth"] for m in names}
    gcall = _calls(spec, golden)

    # 1. the golden files the world's own call
    row("golden files the truth's call", gcall == _calls(spec, truth),
        "golden %s, truth %s" % (gcall, _calls(spec, truth)))

    # 2. the honest family: twelve or more rebuilds, one call
    spread = {}
    fam_ok, short = True, []
    n_var = min(len(members[m].get("family") or []) for m in names)
    for m in names:
        fam = members[m].get("family") or []
        spread[m] = max([abs(v - golden[m]) for v in fam] or [0.0])
        if len(fam) < FAMILY_MIN:
            short.append(m)
    for i in range(n_var):
        if _calls(spec, {m: members[m]["family"][i] for m in names}) != gcall:
            fam_ok = False
    row("variant battery", not short and fam_ok,
        "%d variants, the call holds under every one" % n_var if (not short and fam_ok) else
        ("fewer than %d variants on %s" % (FAMILY_MIN, ", ".join(short)) if short else "a variant moves the call"))

    # 3. the lattice is complete
    need = {_key([s]) for s in sids} | {_key(sids)} | {_key([t for t in sids if t != s]) for s in sids}
    lat = {_key(k.split("+")): v for k, v in lattice.items()}
    missing = sorted(need - set(lat))
    if not row("lattice complete", not missing, "every stump alone, all together, all but one" if not missing
               else "missing: " + ", ".join(missing)):
        return rows, 0
    lcall = {k: _calls(spec, v) for k, v in lat.items()}
    reflex = lat[_key(sids)]
    rcall = lcall[_key(sids)]

    # 4. the reflex route misses, and the members it misses are the open ones
    if spec.get("call", "lines") == "top_k":
        open_members = sorted(set(gcall) ^ set(rcall))
    else:
        open_members = [m for i, m in enumerate(names) if rcall[i] != gcall[i]]
    row("reflex route misses the call", rcall != gcall, "open members: %s" % (", ".join(open_members) or "none"))

    # 5. each stump: necessary alone, worth a multiple, not sufficient alone
    necessary, opened = [], {}
    for s in sids:
        st = stumps[s]
        m = st.get("opens")
        alone = lat[_key([s])]
        flips = lcall[_key([s])] != gcall
        own = m in members and _member_call(spec, m, alone[m], golden) != _member_call(spec, m, golden[m], golden)
        worth = abs(alone[m] - golden[m]) if m in members else 0.0
        mult = worth / spread[m] if (m in members and spread[m] > 0) else float("inf")
        fixed = lcall[_key([t for t in sids if t != s])]
        suff = fixed == gcall
        ok = flips and own and mult >= WORTH and not suff
        row("stump %s" % s, ok,
            "dropped alone %s its member %s (worth %.3g, %.1f times the family's spread %.3g); fixed alone on the "
            "reflex route %s" % ("moves" if own else "does NOT move", m, worth, mult, spread.get(m, 0.0),
                                 "REACHES the call (one trick)" if suff else "still misses"))
        if ok:
            necessary.append(s)
            opened.setdefault(m, []).append(s)
        if st.get("axis") not in AXES:
            row("stump %s axis" % s, False, "axis %r is not one of %s" % (st.get("axis"), ", ".join(AXES)))
        if int(st.get("steps_left") or 0) < STEPS_MIN or not (st.get("said_out_loud") or "").strip():
            row("stump %s said out loud" % s, False,
                "the sentence that names it must leave %d or more dependent steps (stump-screen test 14)" % STEPS_MIN)
        kinds = _precedent_kinds()
        cited = st.get("precedents") or []
        bad = [p for p in cited if kinds and kinds.get(p) not in ("loss", "named_assumption")]
        if not cited or bad:
            row("stump %s precedents" % s, False, "cite loss or named_assumption ids; %s" %
                ("none cited" if not cited else "not a loss on file: " + ", ".join(bad)))

    # 6. no open member is settled by the direct or the rigorous standard route
    forced = []
    for m in open_members:
        routes = members[m].get("routes") or {}
        for want in ("direct", "rigorous"):
            if want not in routes:
                forced.append("%s has no %s route" % (m, want))
        for r, x in routes.items():
            f = dict(reflex)
            f[m] = x
            if _member_call(spec, m, x, reflex) == _member_call(spec, m, golden[m], golden):
                forced.append("%s is filed right by the %s route (%.4g)" % (m, r, x))
    row("no easier route on an open member", not forced, "; ".join(forced) or
        "the direct and the rigorous standard routes land wrong on every open member")

    # 7. distinct wrong answers
    wrong = {c for c in lcall.values() if c != gcall}
    singles = {lcall[_key([s])] for s in necessary} - {gcall}
    row("distinct wrong answers", len(wrong) >= 2, "%d distinct wrong calls across the lattice, %d among the single "
        "drops" % (len(wrong), len(singles)))

    # 8. what forces the call between estimators: a referee slice, or a falsification check on the members' records
    ref = spec.get("referee") or {}
    fal = spec.get("falsification") or {}
    for kind, obj, flag in (("referee", ref, "covers_target"), ("falsification check", fal, "observes_target")):
        if not obj:
            continue
        gerr = abs(obj["golden"] - obj["truth"])
        rerr = {r: abs(x - obj["truth"]) for r, x in (obj.get("rivals") or {}).items()}
        sep = bool(rerr) and all(e >= REFEREE * max(gerr, 1e-12) for e in rerr.values())
        row(kind, sep and obj.get(flag) is False,
            "golden off by %.3g; rivals off by %s%s" % (gerr, ", ".join("%s %.3g" % kv for kv in sorted(rerr.items())),
            "" if obj.get(flag) is False else (
                "; the slice covers the target, so it is a key, not a referee" if kind == "referee" else
                "; the check observes the target or a stump's quantity, so it is a referee: file it as one")))
    if not ref and not fal:
        row("referee", False, "no referee slice and no falsification check: the call is forced by nothing but the "
            "golden's own method")

    # 8b. the routes frontier runs were seen to take, each implemented on the world's arrays, each filing a wrong call
    rreg = _registered(spec)
    soft = bool(rreg) and rreg < RUNS_FROM
    maps, absent = _run_maps(spec)
    if ref and isinstance((spec.get("run_routes") or {}).get("calibrated"), dict) and "calibrated" not in maps:
        absent.append("calibrated (the pack ships a referee slice, and a referee is a calibration set first: price "
                      "the route that calibrates the whole chain on it and carries it to the members)")
    row("run routes listed", not absent,
        "the four routes the runs take are implemented: %s" % ", ".join(sorted(maps)) if not absent else
        "missing or not a figure for every member: %s (stumping Part 1d; task3 arch 8's runs took routes no lattice "
        "key held)%s" % ("; ".join(absent), "; registered before the rule of %s" % RUNS_FROM[:10] if soft else ""),
        warn=soft)
    fam, badfam = _run_family(spec)
    allmaps = dict(maps, **fam)
    right = sorted(n for n, mp in allmaps.items() if _calls(spec, mp) == gcall)
    row("run routes land wrong", bool(maps) and not right and not badfam,
        ("each files a wrong call: " + "; ".join("%s %s" % (n, _calls(spec, maps[n])) for n in sorted(maps)) +
         ("; with %d further settings, every one wrong" % len(fam) if fam else ""))
        if maps and not right and not badfam else
        ("files the golden's call: " + ", ".join(right)) if right else
        ("malformed family keys: " + ", ".join(badfam)) if badfam else "no run route",
        warn=soft)
    if spec.get("call", "lines") != "top_k":
        dirs = set()
        for mp in list(lat.values()) + list(allmaps.values()):
            for m in names:
                d = _band(mp[m], members[m]["lines"]) - _band(golden[m], members[m]["lines"])
                if d:
                    dirs.add(1 if d > 0 else -1)
        row("both sides of the line", dirs == {1, -1},
            "the shortcuts and the run routes miss above and below the golden's classes" if dirs == {1, -1} else
            "every miss falls %s the golden's class, so a route that errs the other way lands the call (task3 arch "
            "8: every open member 1.1 to 1.5 above its line, every priced shortcut under it, and the runs' generous "
            "corrections filed every class)" % ("above" if dirs == {1} else "below" if dirs == {-1} else "on neither side of"),
            warn=soft)
    for st_id in sids:
        over = (stumps[st_id].get("sides") or {}).get("over")
        if not (isinstance(over, dict) and all(m in over and _num(over[m]) for m in names)):
            row("stump %s two-sided" % st_id, False,
                "no over-corrected side: give sides.over, the golden with this stump alone pushed past its fitted "
                "value to the far end a run might set, a figure per member (stumping Part 1d rule 7)%s" % (
                    "; registered before the rule of %s" % RUNS_FROM[:10] if soft else ""), warn=soft)
            continue
        oc = _calls(spec, {m: float(over[m]) for m in names})
        row("stump %s two-sided" % st_id, oc != gcall,
            ("lost alone and over-corrected alone both file a wrong call (over: %s)" % (oc,)) if oc != gcall else
            "over-corrected alone it files the golden's call, so a run that errs past the fitted value lands the "
            "call (task3 arch 9: a legacy receiver worth nothing filed the golden's call)", warn=soft)

    # 9. independence and weight
    axes = {stumps[s].get("axis") for s in necessary}
    row("stumps on different axes", len(axes) >= min(len(necessary), 2),
        "axes: %s" % ", ".join(sorted(a for a in axes if a)), warn=True)

    # 10. the rubric: what each route earns on the figures the answer blocks will state
    figs, fprob = _figures(spec, lat)
    comps = [f for f in figs if f["block"] == "components"]
    asks = [f for f in figs if f["block"] == "asks"]
    nsent = len(_criteria(asks))
    if row("graded figures listed", not fprob and 2 <= len(comps) <= 5 and len(asks) >= 2,
           "%d critical components (two to five) and %d ask figures (two or more)%s%s" % (
               len(comps), len(asks), (" in %d sentences, each one criterion" % nsent) if nsent != len(asks) else "",
               ("; " + "; ".join(fprob)) if fprob else "")):
        gaps = [f["id"] for f in figs if any(f["values"].get(k) is None for k in need)]
        loose = []
        for f in figs:
            if f["exact"]:
                continue
            if len(f["family"]) < FAMILY_MIN:
                loose.append("%s has %d variants" % (f["id"], len(f["family"])))
            elif any(not (f["band"][0] <= v <= f["band"][1]) for v in f["family"] + [f["golden"]]):
                loose.append("%s's band leaves a variant outside (a fork)" % f["id"])
        row("every graded figure banded by the battery", not gaps and not loose,
            "each figure's band holds its twelve or more variants" if not gaps and not loose else
            "; ".join((["no lattice value on " + ", ".join(gaps)] if gaps else []) + loose))
        if not gaps:
            earn = {k: _score(figs, lcall[k] == gcall, lambda f, k=k: f["values"][k]) for k in need}
            base = earn[_key(sids)]
            one = {s: earn[_key([s])] for s in sids}
            fixed = {s: earn[_key([t for t in sids if t != s])] for s in sids}
            silent = [f["id"] for f in figs if _earned(f, f["values"][_key(sids)])]
            whole = [c[0]["sentence"] for c in _criteria(asks)
                     if len(c) > 1 and all(_earned(f, f["values"][_key(sids)]) for f in c)]
            row("one stump lost, the run stays under the bar", max(one.values()) <= ONE_LOST_MAX + 1e-9,
                "a run that loses only %s (%.0f or under each; the review reads its strongest run)" % (
                    ", ".join("%s earns %.0f" % (s, one[s]) for s in sids), ONE_LOST_MAX))
            row("the reflex route on the rubric", base <= REFLEX_MAX + 1e-9,
                "every stump lost earns %.0f (%.0f or under; %.0f of it is instruction-following); figures it "
                "still lands: %s%s" % (base, REFLEX_MAX, BLOCKS["instruction"], ", ".join(silent) or "none",
                                       ("; sentences it lands whole: " + (", ".join(whole) or "none"))
                                       if nsent != len(asks) else ""))
            flat = [s for s in sids if fixed[s] <= base + 1e-9]
            rich = [s for s in sids if fixed[s] - base > HINT_MAX + 1e-9]
            row("one stump fixed alone earns more, a third at most", not flat and not rich,
                "; ".join("%s fixed alone earns %.0f" % (s, fixed[s]) for s in sids) +
                (("; no figure of its own: " + ", ".join(flat)) if flat else "") +
                (("; one sentence rescues over a third: " + ", ".join(rich)) if rich else ""))
            # The critical components are the decisive steps, kept independent: each falls with one stump alone.
            falls = {f["id"]: [s for s in sids if not _earned(f, f["values"][_key([s])])] for f in comps}
            joint = sorted(fid for fid, ss in falls.items() if len(ss) != 1)
            bare = [s for s in sids if not any(ss == [s] for ss in falls.values())]
            reg = _registered(spec)
            row("critical components independent", not joint and not bare,
                ("each falls with one stump alone: " + ", ".join("%s with %s" % (fid, falls[fid][0]) for fid in sorted(falls)))
                if not joint and not bare else "; ".join(
                    (["%s falls with %s" % (fid, "+".join(falls[fid]) or "no stump (a reflex figure)") for fid in joint]) +
                    (["no component of its own: " + ", ".join(bare)] if bare else []) +
                    ["a component is one decisive step's answer, earned whatever happens to the other steps; a figure "
                     "that falls with two stumps is an ask"] +
                    (["registered before the rule of %s" % INDEPENDENT_FROM[:10]] if reg and reg < INDEPENDENT_FROM else [])),
                warn=bool(reg) and reg < INDEPENDENT_FROM)
            rs, lacking = _route_score(spec, figs, "rigorous", gcall)
            row("the rigorous standard route on the rubric", rs is not None and rs <= ONE_LOST_MAX + 1e-9,
                ("it earns %.0f (%.0f or under)" % (rs, ONE_LOST_MAX)) if rs is not None else
                "%s has no value on the rigorous route, so the strongest run is unpriced" % lacking)
            for name in sorted(maps):
                sc, lacking = _run_route_score(spec, figs, name, maps[name], gcall)
                row("the %s route on the rubric" % name, sc is not None and sc <= ONE_LOST_MAX + 1e-9,
                    ("it earns %.0f (%.0f or under; the review reads the strongest run)" % (sc, ONE_LOST_MAX))
                    if sc is not None else "%s has no value on the %s route, so the run's route is unpriced" % (
                        lacking, name), warn=soft)

            # Holistic Audit v4 hardened checks (split 1-check criteria + worst-case ECF + coupled matrix + coded one-fact catch check)
            v4_strict = _v4_enforced(spec)
            v4_earn = {k: _score_v4(figs, lcall[k] == gcall, lambda f, k=k: f["values"][k], apply_ecf=True) for k in need}
            v4_one = {s: v4_earn[_key([s])] for s in sids}
            v4_base = v4_earn[_key(sids)]
            v4_two = {s: v4_earn[_key([t for t in sids if t != s])] for s in sids} if len(sids) >= 3 else {}
            row("v4-ECF one stump lost <= 50", max(v4_one.values()) <= ONE_LOST_MAX + 1e-9,
                "split 1-check + worst-case ECF: %s (%.0f or under each)" % (
                    ", ".join("%s=%.0f" % (s, v4_one[s]) for s in sids), ONE_LOST_MAX),
                warn=not v4_strict)
            if v4_two:
                row("v4-ECF two stumps lost <= 35", max(v4_two.values()) <= V4_TWO_LOST_MAX + 1e-9,
                    "split 1-check + worst-case ECF (1 stump fixed alone): %s (%.0f or under each; targets 30s-40s)" % (
                        ", ".join("%s_only=%.0f" % (s, v4_two[s]) for s in sids), V4_TWO_LOST_MAX),
                    warn=not v4_strict)
            row("v4-ECF reflex route <= 25", v4_base <= V4_REFLEX_MAX + 1e-9 and not silent,
                "every stump lost earns %.0f (<= %.0f); un-stumped/silent figures: %s" % (
                    v4_base, V4_REFLEX_MAX, ", ".join(silent) or "none"),
                warn=not v4_strict)
            non_ecf_asks = [f for f in asks if not f.get("ecf")]
            if non_ecf_asks:
                coupled = [f["id"] for f in non_ecf_asks
                           if sum(1 for s in sids if not _earned(f, f["values"][_key([s])])) >= 2]
                c_share = len(coupled) / float(len(non_ecf_asks))
                row("coupled figure matrix (>=50% multi-stump asks)", c_share >= 0.50 - 1e-9,
                    "%d of %d non-ECF ask figures (%.0f%%) move under 2+ independent stumps: %s" % (
                        len(coupled), len(non_ecf_asks), 100.0 * c_share, ", ".join(coupled) or "none"),
                    warn=not v4_strict)
            # Coded one-fact catch check: once told a stump's one-sentence mechanism, an obvious 1-step shortcut
            # must NOT recover both the golden call and the stump's own component band.
            comp_by_stump = {falls[fid][0]: next(f for f in comps if f["id"] == fid)
                             for fid in falls if len(falls[fid]) == 1}
            for s in sids:
                ofs = stumps[s].get("one_fact_shortcut")
                if ofs is None:
                    if v4_strict:
                        row("stump %s coded one-fact catch check" % s, False,
                            "missing one_fact_shortcut in core.py (provide the 1-step post-hint shortcut figures to prove %s is not a catch)" % s)
                    continue
                if isinstance(ofs, dict) and "members" in ofs:
                    ofs_m = {m: float(ofs["members"][m]) for m in names}
                    ofs_c = ofs.get("component")
                elif isinstance(ofs, dict) and all(m in ofs and _num(ofs[m]) for m in names):
                    ofs_m = {m: float(ofs[m]) for m in names}
                    cf = comp_by_stump.get(s)
                    ofs_c = ofs_m[cf["member"]] if (cf and cf["member"] in ofs_m) else None
                else:
                    row("stump %s coded one-fact catch check" % s, False, "malformed one_fact_shortcut on %s" % s)
                    continue
                call_landed = _calls(spec, ofs_m) == gcall
                cf = comp_by_stump.get(s)
                comp_landed = bool(cf and ofs_c is not None and _earned(cf, ofs_c))
                not_catch = not (call_landed and (comp_landed or ofs_c is None))
                row("stump %s coded one-fact catch check" % s, not_catch,
                    "1-step post-hint shortcut %s the call%s (%s)" % (
                        "LANDS" if call_landed else "misses",
                        "" if ofs_c is None else (" and %s component %s" % ("LANDS" if comp_landed else "misses", cf["id"])),
                        "genuine modeling required" if not_catch else "FAIL: this stump is a catch (Holistic Audit v4 Part D.4)"))

    members_opened = [m for m in opened if m in open_members]
    level = 0
    if not any(r[1] == "FAIL" for r in rows) and len(members_opened) >= 2:
        level = 5 if (len(members_opened) >= 3 and len(necessary) >= 3 and len(singles) >= 2) else 4
    row("open members opened by different stumps", len(members_opened) >= 2,
        "%d: %s" % (len(members_opened), "; ".join("%s by %s" % (m, "+".join(opened[m])) for m in members_opened)))
    return rows, (level if not any(r[1] == "FAIL" for r in rows) else 0)


def table(spec):
    members, stumps = spec["members"], spec["stumps"]
    lat = {_key(k.split("+")): v for k, v in spec["lattice"].items()}
    reflex = lat.get(_key(sorted(stumps)), {})
    out = ["| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |", "|---|---|---|---|---|---|---|---|"]
    for m in sorted(members):
        mm = members[m]
        sp = max([abs(v - mm["golden"]) for v in mm.get("family") or []] or [0.0])
        by = [s for s in sorted(stumps) if stumps[s].get("opens") == m]
        r = mm.get("routes") or {}
        out.append("| %s | %s | %.4g | %.3g | %s | %s | %s | %s |" % (
            m, "/".join("%g" % l for l in mm.get("lines") or []) or "top-k", mm["golden"], sp,
            ("%.4g" % reflex[m]) if m in reflex else "-", ("%.4g" % r["direct"]) if "direct" in r else "-",
            ("%.4g" % r["rigorous"]) if "rigorous" in r else "-", ", ".join(by) or "forced"))
    maps, _ = _run_maps(spec)
    if maps:
        gcall = _calls(spec, {m: members[m]["golden"] for m in members})
        out += ["", "| Run route | Call | %s |" % " | ".join(sorted(members)), "|---|---|%s" % ("---|" * len(members))]
        for name in sorted(maps):
            out.append("| %s | %s | %s |" % (name, "right" if _calls(spec, maps[name]) == gcall else "wrong",
                                             " | ".join("%.4g" % maps[name][m] for m in sorted(members))))
    return "\n".join(out)


def rubric_table(spec):
    """The figure exposure (which stump moves which graded figure) and what each route earns on the rubric."""
    stumps, members = spec["stumps"], spec["members"]
    sids = sorted(stumps)
    lat = {_key(k.split("+")): v for k, v in spec["lattice"].items()}
    names = sorted(members)
    golden = {m: members[m]["golden"] for m in names}
    gcall = _calls(spec, golden)
    figs, _ = _figures(spec, lat)
    if not figs:
        return ""
    out = ["| Figure | Block | ECF | Golden | Band | %s | Reflex route |" % " | ".join("%s lost" % s for s in sids),
           "|---|---|---|---|---|%s---|" % ("---|" * len(sids))]

    def cell(f, k):
        x = f["values"].get(k)
        if x is None:
            return "?"
        if f["member"] is not None and _member_call(spec, f["member"], x, lat[k]) != _member_call(
                spec, f["member"], f["golden"], golden):
            return "flips"
        return "-" if _earned(f, x) else "moves"

    for f in figs:
        band = ("%.4g to %.4g" % tuple(f["band"])) if f["band"] else "exact"
        gold = ("%.4g" % f["golden"]) if _num(f["golden"]) else str(f["golden"])
        out.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            f["id"], f["block"] or "?", "yes" if f.get("ecf") else "no", gold, band,
            " | ".join(cell(f, _key([s])) for s in sids),
            {"-": "earned"}.get(cell(f, _key(sids)), "lost")))
    keys = [(_key([s]), "%s lost alone" % s) for s in sids]
    keys += [(_key([t for t in sids if t != s]), "%s fixed alone" % s) for s in sids if len(sids) > 2]
    keys += [(_key(sids), "reflex route (every stump lost)")]
    out += ["", "| Route | Call | House rubric | v4-ECF rubric |", "|---|---|---|---|", "| golden | right | 100 | 100 |"]
    for k, label in keys:
        if k in lat and all(f["values"].get(k) is not None for f in figs):
            right = _calls(spec, lat[k]) == gcall
            out.append("| %s | %s | %.0f | %.0f |" % (
                label, "right" if right else "wrong",
                _score(figs, right, lambda f, k=k: f["values"][k]),
                _score_v4(figs, right, lambda f, k=k: f["values"][k], apply_ecf=True)))
    rs, _ = _route_score(spec, figs, "rigorous", gcall)
    if rs is not None:
        mfig = {m: (members[m].get("routes") or {}).get("rigorous", golden[m]) for m in names}
        rvals = {f["id"]: (f["routes"].get("rigorous") if f["routes"].get("rigorous") is not None else f["golden"]) for f in figs}
        v4_rs = _score_v4(figs, _calls(spec, mfig) == gcall, lambda f: rvals[f["id"]], apply_ecf=True)
        out.append("| rigorous standard route | %s | %.0f | %.0f |" % (
            "right" if _calls(spec, mfig) == gcall else "wrong", rs, v4_rs))
    maps, _ = _run_maps(spec)
    for name in sorted(maps):
        sc, _ = _run_route_score(spec, figs, name, maps[name], gcall)
        if sc is not None:
            rvals = {f["id"]: (maps[name][f["member"]] if f["member"] is not None else f["routes"].get(name)) for f in figs}
            v4_sc = _score_v4(figs, _calls(spec, maps[name]) == gcall, lambda f: rvals[f["id"]], apply_ecf=True)
            out.append("| %s run route | %s | %.0f | %.0f |" % (
                name, "right" if _calls(spec, maps[name]) == gcall else "wrong", sc, v4_sc))
    return "\n".join(out)


def run(spec):
    rows, level = check(spec)
    print(table(spec))
    print()
    rt = rubric_table(spec)
    if rt:
        print(rt)
        print()
    for name, lv, detail in rows:
        print("%-4s  %-40s %s" % (lv, name, detail))
    fails = sum(1 for r in rows if r[1] == "FAIL")
    print(("CORE PASS level %d  %s" % (level, spec.get("task", ""))) if level else
          ("CORE FAIL  %s: %d failing checks" % (spec.get("task", ""), fails)))
    if "--json" in sys.argv:
        print(json.dumps({"level": level, "rows": rows}))
    return 0 if level else 1


OFFSETS = (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.15, -0.15, 0.25)
DENSE = {"S1": {"a": -4.0, "b": 1.2, "d": -1.5}, "S2": {"b": 4.0, "c": -1.2, "d": -1.3},
         "S3": {"c": -4.5, "a": -0.5, "d": -1.4}}
SPARSE = {"S1": {"a": -4.0}, "S2": {"b": 4.0}, "S3": {"c": -4.5, "a": -0.5}}


def _demo(eff=None):
    """A three-stump core on four members, each read against a line of 10: three open, one forced. Each stump flips
    one member's call and moves most of the other graded figures outside their bands without flipping them."""
    eff = eff or DENSE
    fam = lambda g, k=1.0: [g + k * d for d in OFFSETS]
    g = {"a": 12.0, "b": 8.0, "c": 12.5, "d": 15.0}
    members = {m: {"lines": [10.0], "truth": g[m] + 0.1, "golden": g[m], "family": fam(g[m]),
                   "routes": {"direct": {"a": 7.0, "b": 13.0, "c": 6.5, "d": 15.5}[m],
                              "rigorous": {"a": 8.5, "b": 11.5, "c": 8.0, "d": 15.2}[m]}} for m in g}
    over = {"S1": {"a": 15.5, "b": 10.4, "c": 12.5, "d": 15.8}, "S2": {"a": 9.6, "b": 6.0, "c": 13.0, "d": 15.5},
            "S3": {"a": 12.0, "b": 10.6, "c": 16.0, "d": 16.0}}
    stumps = {s: {"axis": ax, "opens": m, "said_out_loud": "the labelled rows are selected on the outcome",
                  "steps_left": 4, "precedents": ["L53"], "sides": {"over": over[s]}}
              for s, ax, m in (("S1", "who", "a"), ("S2", "what", "b"), ("S3", "against", "c"))}
    combos = [c for n in (1, 2, 3) for c in itertools.combinations(sorted(eff), n)]
    lattice = {"+".join(c): {m: g[m] + sum(eff[s].get(m, 0.0) for s in c) for m in g} for c in combos}
    own = {"S1": ("C1", 0.60, 0.03, 0.25, 0.52), "S2": ("C2", 0.30, 0.03, 0.55, 0.41), "S3": ("C3", 40.0, 2.0, 55.0, 47.0)}
    figures = [{"id": fid, "block": "component", "golden": gold, "family": fam(gold, k),
                "lattice": {"+".join(c): (hurried if s in c else gold) for c in combos}, "routes": {"rigorous": rig}}
               for s, (fid, gold, k, hurried, rig) in sorted(own.items())]
    figures += [{"id": m, "block": "ask", "member": m} for m in sorted(g)]
    factor = {"S1": 0.8, "S2": 1.3, "S3": 0.7}
    total = lambda c: 100.0 * (factor["S1"] if "S1" in c else 1) * (factor["S2"] if "S2" in c else 1) * (
        factor["S3"] if "S3" in c else 1)
    figures.append({"id": "X", "block": "ask", "golden": 100.0, "family": fam(100.0, 2.5),
                    "lattice": {"+".join(c): total(c) for c in combos}, "routes": {"rigorous": 84.0}})
    run_routes = {"generous": {"a": 13.4, "b": 10.5, "c": 13.6, "d": 16.2},
                  "calibrated": {"a": 9.5, "b": 8.6, "c": 12.0, "d": 15.4},
                  "hedge": {"a": 8.6, "b": 9.2, "c": 8.9, "d": 15.6},
                  "cutoff": {"a": 9.2, "b": 9.6, "c": 9.4, "d": 15.8}}
    off = {"generous": (0.70, 0.36, 47.0, 112.0), "calibrated": (0.66, 0.24, 45.0, 93.0),
           "hedge": (0.40, 0.45, 52.0, 80.0), "cutoff": (0.45, 0.40, 50.0, 88.0)}
    for i, fid in enumerate(("C1", "C2", "C3", "X")):
        f = next(f for f in figures if f["id"] == fid)
        f["routes"].update({name: off[name][i] for name in off})
    return {"task": "selftest", "members": members, "stumps": stumps, "lattice": lattice, "figures": figures,
            "referee": {"slice": "a labelled sample the target does not reach", "covers_target": False,
                        "truth": 0.60, "golden": 0.61, "rivals": {"direct": 0.25, "rigorous": 0.52}},
            "run_routes": run_routes}


def selftest():
    import copy
    ok = True

    def expect(label, spec, want_level, must_fail=None):
        nonlocal ok
        rows, level = check(spec)
        failed = [r[0] for r in rows if r[1] == "FAIL"]
        good = level == want_level and (must_fail is None or any(must_fail in f for f in failed))
        ok &= good
        print("  %s  %-62s level %d%s" % ("PASS" if good else "FAIL", label, level,
                                         (" (fails: " + ", ".join(failed) + ")") if failed else ""))

    def fig(spec, fid):
        return next(f for f in spec["figures"] if f["id"] == fid)

    base = _demo()
    expect("three stumps opening three members", base, 5)
    s = copy.deepcopy(base)                     # two stumps on two members is level 4
    del s["stumps"]["S3"]
    s["lattice"] = {k: v for k, v in s["lattice"].items() if "S3" not in k}
    s["figures"] = [f for f in s["figures"] if f["id"] != "C3"]
    for f in s["figures"]:
        if "lattice" in f:
            f["lattice"] = {k: v for k, v in f["lattice"].items() if "S3" not in k}
    expect("two stumps opening two members", s, 4)
    s = copy.deepcopy(base)                     # the rigorous standard route files an open member right
    s["members"]["a"]["routes"]["rigorous"] = 11.8
    expect("an open member the rigorous route files right", s, 0, "no easier route")
    s = copy.deepcopy(base)                     # a stump worth less than three times the family's spread
    for k in s["lattice"]:
        if "S2" in k.split("+"):
            s["lattice"][k]["b"] = s["lattice"][k]["b"] - 4.0 + 2.05
    for m in s["members"]:
        s["members"][m]["family"] = [v + (0.5 if v > s["members"][m]["golden"] else -0.5 if v < s["members"][m]["golden"] else 0)
                                     for v in s["members"][m]["family"]]
    expect("a stump worth under three times the family's spread", s, 0, "stump S2")
    s = copy.deepcopy(base)                     # one trick: every member rides on one stump
    for st in ("S2", "S3"):
        for k in s["lattice"]:
            if st in k.split("+"):
                for m in s["lattice"][k]:
                    s["lattice"][k][m] = s["members"][m]["golden"] + (-4.0 if ("S1" in k.split("+") and m == "a") else 0.0)
    expect("one stump carrying the call (the others move nothing)", s, 0, "stump S")
    s = copy.deepcopy(base)                     # a referee that does not separate the golden from a rival
    s["referee"]["rivals"]["rigorous"] = 0.615
    expect("a referee the rigorous rival also passes", s, 0, "referee")
    s = copy.deepcopy(base)                     # a referee slice that covers the target is a key
    s["referee"]["covers_target"] = True
    expect("a referee slice that covers the target", s, 0, "referee")
    s = copy.deepcopy(base)                     # a stump that dies when said out loud
    s["stumps"]["S1"]["steps_left"] = 1
    expect("a stump one step from its figure once named", s, 0, "said out loud")
    s = copy.deepcopy(base)                     # a stump priced on a reflex
    s["stumps"]["S1"]["precedents"] = ["R91"]
    expect("a stump citing a reflex", s, 0, "precedents")
    # the rubric
    s = copy.deepcopy(base)                     # no graded figures: the rubric is unpriced
    s["figures"] = []
    expect("a core with no graded figures", s, 0, "graded figures")
    s = _demo(SPARSE)                           # each stump moves its own member's figure and nothing else
    expect("a run that loses one stump still clears 50 (sparse figures)", s, 0, "one stump lost")
    s = _demo(SPARSE)                           # the same figures stated in one sentence are one criterion
    for f in s["figures"]:
        if f.get("member"):
            f["sentence"] = "every member's figure"
    lost = [r for r in check(s)[0] if r[0].startswith("one stump lost")]
    good = bool(lost) and lost[0][1] == "PASS"
    ok &= good
    print("  %s  %-62s %s" % ("PASS" if good else "FAIL", "figures of one sentence earned together or not at all",
                              lost[0][2][:60] if lost else "no rubric row"))
    s = copy.deepcopy(base)                     # figures no stump touches: counts and totals every run rebuilds
    keys = list(fig(s, "X")["lattice"])
    s["figures"] += [{"id": "N%d" % i, "block": "ask", "golden": 1000 + i, "exact": True,
                      "lattice": {k: 1000 + i for k in keys}, "routes": {"rigorous": 1000 + i}} for i in range(4)]
    expect("four ask figures no stump touches", s, 0, "the reflex route on the rubric")
    s = copy.deepcopy(base)                     # a band narrower than the honest family is a fork
    fig(s, "X")["band"] = [99.5, 100.5]
    expect("a band that leaves a variant outside", s, 0, "banded by the battery")
    s = copy.deepcopy(base)                     # a stump with no figure of its own
    s["figures"] = [f for f in s["figures"] if f["id"] != "C2"]
    expect("a stump whose fix alone earns nothing", s, 0, "fixed alone")
    s = copy.deepcopy(base)                     # a component that falls with two stumps is not one step's answer
    c1 = fig(s, "C1")
    c1["lattice"] = {k: (0.25 if ("S1" in k.split("+") or "S2" in k.split("+")) else 0.60) for k in c1["lattice"]}
    expect("a critical component that falls with two stumps", s, 0, "critical components independent")
    s = copy.deepcopy(base)                     # a stump whose only figures are joint has no component of its own
    c3 = fig(s, "C3")
    c3["lattice"] = {k: (55.0 if "S1" in k.split("+") else 40.0) for k in c3["lattice"]}
    expect("a stump with no component of its own", s, 0, "critical components independent")
    s = copy.deepcopy(base)                     # the strongest run unpriced
    del fig(s, "X")["routes"]
    expect("a figure with no value on the rigorous route", s, 0, "rigorous standard route on the rubric")
    s = copy.deepcopy(base)                     # the rigorous route lands the estimated figures
    for f in s["figures"]:
        if "routes" in f:
            f["routes"]["rigorous"] = f["golden"]
    expect("a rigorous route that earns over 50", s, 0, "rigorous standard route on the rubric")
    # the runs' recorded routes (task3 arch 8)
    s = copy.deepcopy(base)                     # no run routes at all
    del s["run_routes"]
    expect("a core with none of the runs' routes", s, 0, "run routes listed")
    s = copy.deepcopy(base)                     # the generous route files the golden's call
    s["run_routes"]["generous"] = {"a": 12.4, "b": 8.4, "c": 12.9, "d": 15.4}
    expect("a generous route that lands the call", s, 0, "run routes land wrong")
    s = copy.deepcopy(base)                     # a referee shipped and the calibrated route declared absent
    s["run_routes"]["calibrated"] = {"none": "no file observes the target or any stump's own quantity"}
    expect("a referee with no calibrated route priced", s, 0, "run routes listed")
    s = copy.deepcopy(base)                     # no referee, a falsification check on the members' own records
    del s["referee"]
    s["run_routes"]["calibrated"] = {"none": "no file observes the target or any stump's own quantity"}
    s["falsification"] = {"check": "the within-group share across the recording bands", "observes_target": False,
                          "truth": 0.30, "golden": 0.31, "rivals": {"hedge": 0.15, "generous": 0.40}}
    expect("a falsification check in place of a referee", s, 5)
    s2 = copy.deepcopy(s)                       # a falsification check that observes the target is a referee
    s2["falsification"]["observes_target"] = True
    expect("a falsification check that observes the target", s2, 0, "falsification check")
    s = copy.deepcopy(base)                     # every miss below the golden's classes: one-sided
    for k in s["lattice"]:
        s["lattice"][k]["b"] = min(s["lattice"][k]["b"], 9.9)
    s["run_routes"]["generous"]["b"] = 9.6
    s["run_routes"]["generous"]["a"] = 9.8
    expect("misses on one side of the line only", s, 0, "both sides of the line")
    s = copy.deepcopy(base)                     # a run route with no value on a figure
    del fig(s, "X")["routes"]["hedge"]
    expect("a run route unpriced on the rubric", s, 0, "the hedge route on the rubric")
    s = copy.deepcopy(base)                     # the calibrated route earns the estimated figures
    for f in s["figures"]:
        if "routes" in f:
            f["routes"]["calibrated"] = f["golden"]
    s["run_routes"]["calibrated"] = {"a": 9.5, "b": 8.1, "c": 12.4, "d": 15.0}
    expect("a calibrated route that earns over 50", s, 0, "the calibrated route on the rubric")
    s = copy.deepcopy(base)                     # a stump that over-corrected alone lands the call
    s["stumps"]["S3"]["sides"]["over"] = {"a": 12.0, "b": 8.0, "c": 16.0, "d": 16.0}
    expect("a stump whose over-corrected side lands the call", s, 0, "stump S3 two-sided")
    s = copy.deepcopy(base)                     # a stump with no over-corrected side
    del s["stumps"]["S2"]["sides"]
    expect("a stump with no over-corrected side", s, 0, "stump S2 two-sided")
    s = copy.deepcopy(base)                     # one setting of a run route's family lands the call
    s["run_routes"]["cutoff:k5"] = {"a": 11.0, "b": 9.0, "c": 11.5, "d": 15.0}
    s["run_routes"]["cutoff:k20"] = {"a": 9.0, "b": 9.0, "c": 9.5, "d": 15.0}
    expect("a cut-off family with one setting that lands the call", s, 0, "run routes land wrong")
    s = copy.deepcopy(base)                     # a family whose every setting files a wrong call
    s["run_routes"]["cutoff:k5"] = {"a": 11.0, "b": 10.5, "c": 11.5, "d": 15.0}
    s["run_routes"]["cutoff:k20"] = {"a": 9.0, "b": 9.0, "c": 9.5, "d": 15.0}
    expect("a cut-off family wrong at every setting", s, 5)
    # v4 hardened checks: coded one-fact catch check, v4-ECF split rubric, coupled matrix
    s = copy.deepcopy(base)
    s["v4_hardened"] = True
    for sid, comp_v in (("S1", 0.35), ("S2", 0.45), ("S3", 50.0)):
        s["stumps"][sid]["one_fact_shortcut"] = {"members": s["lattice"][sid], "component": comp_v}
    expect("v4 hardened build with coupled asks and coded one-fact checks", s, 5)
    s2 = copy.deepcopy(s)                       # one-fact shortcut lands both call and component -> catch FAIL
    s2["stumps"]["S2"]["one_fact_shortcut"] = {"members": {"a": 12.0, "b": 8.0, "c": 12.5, "d": 15.0}, "component": 0.30}
    expect("a stump whose 1-step post-hint fix lands golden (catch)", s2, 0, "coded one-fact catch check")
    s3 = copy.deepcopy(s)                       # arithmetic rollups credited via ECF push one-lost > 50
    for f in s3["figures"]:
        if f["block"] == "ask" and f["id"] in ("X", "d"):
            f["ecf"] = True
    expect("v4-ECF rollup credit pushes one-stump-lost over 50", s3, 0, "v4-ECF one stump lost")
    print("SELFTEST %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    print(__doc__)
    sys.exit(2)
