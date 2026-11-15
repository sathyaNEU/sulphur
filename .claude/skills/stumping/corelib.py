#!/usr/bin/env python3
"""corelib.py: the checker every task's generator/core.py ends on (stumping SKILL.md Part 1d,
references/core-method.md). The architect writes the world and the estimators; this file decides whether what they
print is a core, and at which level. It is arithmetic on the spec: nothing here reads a prompt or solves a task.

    # taskNN/generator/core.py
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
    import corelib
    spec = {...}                      # built from the world's arrays, never typed
    sys.exit(corelib.run(spec))       # prints the core table and CORE PASS level N, or CORE FAIL

    python3 .claude/skills/stumping/corelib.py selftest

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
                  "precedents": [ids]}}          loss or named_assumption ids in references/precedents.json
  lattice   {"S1": {member: x, ...}, "S1+S2": {...}, ...}   every member's figure with exactly those stumps made
            the hurried way and everything else golden. Required keys: each stump alone, all together (the reflex
            route), and all but one (each stump fixed alone on the reflex route).
  referee   {"slice": text, "covers_target": false, "truth": x, "golden": x, "rivals": {route: x, ...}}
  results   optional [{"id": "R1", "weight": w, "reflex_earns": bool}]   the rubric weight the reflex route earns
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AXES = ("who", "what", "when", "against", "unit")
WORTH = 3.0          # a stump's worth on its member, over the honest family's spread there
REFEREE = 3.0        # each rival's error on the referee slice, over the golden's
FAMILY_MIN = 12
STEPS_MIN = 3
REFLEX_SHARE = 1.0 / 3


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

    # 8. the referee
    ref = spec.get("referee") or {}
    if ref:
        gerr = abs(ref["golden"] - ref["truth"])
        rerr = {r: abs(x - ref["truth"]) for r, x in (ref.get("rivals") or {}).items()}
        sep = bool(rerr) and all(e >= REFEREE * max(gerr, 1e-12) for e in rerr.values())
        row("referee", sep and ref.get("covers_target") is False,
            "golden off by %.3g; rivals off by %s%s" % (gerr, ", ".join("%s %.3g" % kv for kv in sorted(rerr.items())),
            "" if ref.get("covers_target") is False else "; the slice covers the target, so it is a key, not a referee"))
    else:
        row("referee", False, "no referee slice: the call is forced by nothing but the golden's own method")

    # 9. independence and weight
    axes = {stumps[s].get("axis") for s in necessary}
    row("stumps on different axes", len(axes) >= min(len(necessary), 2),
        "axes: %s" % ", ".join(sorted(a for a in axes if a)), warn=True)
    res = spec.get("results") or []
    if res:
        tot = sum(r["weight"] for r in res) or 1.0
        share = sum(r["weight"] for r in res if r.get("reflex_earns")) / tot
        row("weight on the estimated quantities", share <= REFLEX_SHARE + 1e-9,
            "the reflex route earns %.0f%% of the rubric weight (a third at most)" % (100 * share))

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
    return "\n".join(out)


def run(spec):
    rows, level = check(spec)
    print(table(spec))
    print()
    for name, lv, detail in rows:
        print("%-4s  %-40s %s" % (lv, name, detail))
    fails = sum(1 for r in rows if r[1] == "FAIL")
    print(("CORE PASS level %d  %s" % (level, spec.get("task", ""))) if level else
          ("CORE FAIL  %s: %d failing checks" % (spec.get("task", ""), fails)))
    if "--json" in sys.argv:
        print(json.dumps({"level": level, "rows": rows}))
    return 0 if level else 1


def _demo():
    """A three-stump core on four members, each read against a line of 10: three open, one forced."""
    fam = lambda g: [g + d for d in (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.15, -0.15, 0.25)]
    g = {"a": 12.0, "b": 8.0, "c": 12.5, "d": 15.0}
    members = {m: {"lines": [10.0], "truth": g[m] + 0.1, "golden": g[m], "family": fam(g[m]),
                   "routes": {"direct": {"a": 7.0, "b": 13.0, "c": 6.5, "d": 15.5}[m],
                              "rigorous": {"a": 8.5, "b": 11.5, "c": 8.0, "d": 15.2}[m]}} for m in g}
    eff = {"S1": {"a": -4.0}, "S2": {"b": 4.0}, "S3": {"c": -4.5, "a": -0.5}}
    stumps = {s: {"axis": ax, "opens": m, "said_out_loud": "the labelled rows are selected on the outcome",
                  "steps_left": 4, "precedents": ["L53"]}
              for s, ax, m in (("S1", "who", "a"), ("S2", "what", "b"), ("S3", "against", "c"))}
    lattice = {}
    for n in (1, 2, 3):
        for combo in itertools.combinations(sorted(eff), n):
            lattice["+".join(combo)] = {m: g[m] + sum(eff[s].get(m, 0.0) for s in combo) for m in g}
    return {"task": "selftest", "members": members, "stumps": stumps, "lattice": lattice,
            "referee": {"slice": "a labelled sample the target does not reach", "covers_target": False,
                        "truth": 0.60, "golden": 0.61, "rivals": {"direct": 0.25, "rigorous": 0.52}},
            "results": [{"id": "R1", "weight": 20, "reflex_earns": True}, {"id": "R2", "weight": 80, "reflex_earns": False}]}


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

    base = _demo()
    expect("three stumps opening three members", base, 5)
    s = copy.deepcopy(base)                     # two stumps on two members is level 4
    del s["stumps"]["S3"]
    s["lattice"] = {k: v for k, v in s["lattice"].items() if "S3" not in k}
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
    s = copy.deepcopy(base)                     # the reflex route earns most of the rubric
    s["results"][0]["weight"], s["results"][1]["weight"] = 60, 40
    expect("the reflex route earning 60 per cent of the weight", s, 0, "weight")
    s = copy.deepcopy(base)                     # a stump that dies when said out loud
    s["stumps"]["S1"]["steps_left"] = 1
    expect("a stump one step from its figure once named", s, 0, "said out loud")
    s = copy.deepcopy(base)                     # a stump priced on a reflex
    s["stumps"]["S1"]["precedents"] = ["R91"]
    expect("a stump citing a reflex", s, 0, "precedents")
    print("SELFTEST %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    print(__doc__)
    sys.exit(2)
