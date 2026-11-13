#!/usr/bin/env python3
"""effort.py, the client's effort test measured on the cut pack: three passes scored result by result.

    python3 .claude/skills/stumping/effort.py taskNN               # the scored table and the gate
    python3 .claude/skills/stumping/effort.py taskNN --markdown    # the Effort test table for the design note
    python3 .claude/skills/stumping/effort.py taskNN --check-note  # also refuse a note whose table disagrees

The generator writes <task>/generator/effort.json from its own code, run on the cut pack: each result's golden
value and band, and the value each pass's method files. The passes are the author's implementations of named
methods (the golden's, and the hurried analyst's shortcut at each result); none of them reads the prompt, so this is
the paper argument computed, never a solver (CLAUDE.md, the STOP block).

  quick                 ten minutes: the obvious file, the raw comparison, the first account that fits
  careful               an afternoon, careful but hurried, calibrated to the run record rather than to the design:
                        what a frontier run does unprompted (every file cleaned and every document read, any
                        pattern one plot or one group-by shows modelled, the field's textbook method run, a holdout
                        or back-test, a bootstrap, a sensitivity grid on nearby choices), stopping where the result
                        needs a move beyond those; a result whose only difficulty is one of them is Right here
  thorough              two days, every number checked twice: the golden

effort.json:

  {"results": [{"id": "R4", "name": "the six's saving", "graded_as": "Component 1", "figure": "avoided_total",
                "depends": ["R2", "R3"], "independent": "",
                "golden": 12984, "band": [12000, 14000], "partly": [9000, 17000],
                "passes": {"quick": 5770, "careful": {"value": 11800, "grade": "partly", "why": "..."},
                           "thorough": 12984}}, ...],
   "hints": [{"sentence": "the station gust records are not stationary", "rescues": ["R2"]}],
   "routes": [{"name": "the golden", "answer": [...], "golden": true}, {"name": "<a shortcut>", "answer": [...]}],
   "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}

Every result names its `figure`, the generator/figures.json key the answer blocks state it from, and the golden
must equal it (the platform grades against the blocks, so a scorer band that drifts from them measures nothing).
Every result lists what it `depends` on; a pass that misses a dependency cannot be hand-graded Right on the result
unless `independent` names the input that lets the result be graded on its own. A value the generator computes
end to end through the pass's own upstream figures is a measurement and stands as computed.

A value is graded against the golden: a number inside `band` is Right, inside `partly` Partly; a list is Right when
it equals the golden (as a set, or in order with "ordered": true), Partly when the two share half or more; a table
(a dict of cells, each with an optional band in `bands`) is Right when every cell is inside its band, Partly when at
least `partly_share` of them are (default a half); a string must match. A pass may carry its own grade with a `why`. Weights default to the measured Mark split (the call and
the components 38, the asks 55, instruction-following 7 earned by every pass).

Precedents (references/precedents.json). A result the careful but hurried pass grades Missed or Partly carries
`"precedent": ["L09", ...]`: the ids of the places where a frontier run actually lost that kind of move (kind loss)
or named it and waved it through (kind named_assumption), from the Sulfur runs or the client's pages, at least one of
them in the deep class the result's Hurried analyst cell names in the design note's Results chain. An uncited
cell is graded Right for the cited pair estimate, because every Sulfur paper estimate without a run behind it came
back 40 to 60 points high; a reflex id on a lost cell is refused (the runs make that move unprompted).

Forcing (both sides). `"forcing"` records the call's line and its two sides: the golden family (three or more
defensible rival methods run on the cut pack) all on the golden's side, the shortcuts on the other side, and each
fitted input perturbed by its defensible spread still on the golden's side (the holistic audit's test on task1
architecture 3: plus or minus 20 per cent on exit rates moved the call from 7 lines to 15):

  "forcing": {"kind": "numeric", "line": 4.0, "golden_side": "above",
              "golden_family": [{"name": "...", "value": 4.42}, ...],
              "shortcuts": [{"name": "...", "value": 3.70}, ...],
              "perturbations": [{"input": "new-account ratios -20%", "value": 4.21}, ...]}
  or {"kind": "set", "golden_family": [{"name": "...", "answer": [...]}], "perturbations": [{"input": "...", "answer": [...]}]}

The stump factorial (binding; the guard against a one-trick build dressed as a chain). `"factorial"` records every
judgment the call can turn on, each run on the cut pack by the generator's own switches:

  "factorial": {"golden_answer": [...],
                "reflex_route": {"answer": [...]},
                "judgments": [{"id": "J1", "name": "...", "kind": "stump", "precedent": ["N25"],
                               "dropped": {"answer": [...], "results_moved": ["R3", "R7", "R8"]},
                               "alone": {"answer": [...], "results_rescued": ["R3"]}},
                              {"id": "J4", "name": "...", "kind": "reflex", "precedent": ["R44"]}, ...]}

The reflex route sets every reflex judgment (a move runs make unprompted, or one the files spell out) to the golden's
choice and every stump to its hurried choice; it is the careful but hurried pass, so the Recommendation's careful
value must be its answer. `dropped` is the golden with that one judgment hurried; `alone` is the reflex route with that
one stump fixed. A build passes when two or more stumps are each necessary (dropped alone, the call moves) and none is
sufficient (fixed alone, the call is still wrong and a third of the results or fewer are rescued): two such stumps is
level 4, three is level 5, with the single drops on two or more distinct wrong answers. A stump cites a loss or a
named assumption, never a reflex; a move a platform run made unprompted is a reflex from then on (the run's line goes
to precedents.json and the judgment's kind changes to reflex). Enforced as FAIL on every build still being built or
repaired (pipeline status DRAWING, DESIGN, BUILD, PAUSED, RETURNED), WARN on builds already shipped.

Builds whose card was registered before skeleton.RULE_FROM meet both as WARN; every later build meets them as FAIL.
`--precedents` prints the catalogue.

Exit status: 0 the effort test holds, 1 a FAIL, 2 no effort.json.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PASSES = ("quick", "careful", "thorough")
SCORE = {"right": 1.0, "partly": 0.5, "missed": 0.0}
DEFAULT_WEIGHTS = {"recommendation": 14.0, "components": 24.0, "asks": 55.0, "instruction": 7.0}
PAIR_TARGET, BAR = 50.0, 60.0
PRECEDENTS = os.path.join(HERE, "references", "precedents.json")
FINGERPRINT = os.path.join(REPO, ".claude", "skills", "fingerprint")
sys.path.insert(0, FINGERPRINT)
try:
    import skeleton as _skeleton  # noqa: E402  (RULE_FROM, the one cut-over date for the next-level contract)
    RULE_FROM = _skeleton.RULE_FROM
except Exception:
    RULE_FROM = "2026-11-11T15:58:00Z"


def load_precedents():
    try:
        return {p["id"]: p for p in json.load(open(PRECEDENTS))["precedents"]}
    except Exception:
        return {}


def note_classes(task_dir):
    """{result id: the deep classes its Hurried analyst cell names} from the note's Results chain."""
    sys.path.insert(0, HERE)
    import precut as P
    note = os.path.join(task_dir, "DESIGN_NOTE.md")
    if not os.path.exists(note):
        return {}
    secs = P.sections(open(note, encoding="utf-8", errors="replace").read())
    rows, _ = P.results_chain(P.section(secs, "Results chain") or "")
    out = {}
    for r in rows:
        m = re.match(r"([A-Z]{1,2}\d{1,2}[a-z]?)\b", r["id"])
        if m:
            out[m.group(1)] = {k for k, rx in P.DEEP_CLASSES.items() if re.search(rx, r["hurried"], re.I)}
    return out


def precedent_classes(p):
    sys.path.insert(0, HERE)
    import precut as P
    return {k for k, rx in P.DEEP_CLASSES.items() if re.search(rx, p.get("class", ""), re.I)}


def next_level(task_dir):
    """True when the build meets the next-level contract in full: its card was registered from RULE_FROM on, or it
    has no registered card yet."""
    card = os.path.join(FINGERPRINT, "cards", os.path.basename(task_dir) + ".json")
    try:
        reg = json.load(open(card)).get("registered") or ""
    except Exception:
        return True
    return not reg or reg >= RULE_FROM


def resolve(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    return os.path.join(REPO, "task%s" % m.group(1)) if m else os.path.abspath(arg)


def grade(entry, res):
    """(grade, value, why) for one pass entry against one result."""
    why = ""
    wrapper = isinstance(entry, dict) and entry and set(entry) <= {"value", "grade", "why"}
    if wrapper:
        if entry.get("grade"):
            g = entry["grade"].lower()
            if g not in SCORE:
                raise ValueError("%s: grade %r is not right, partly or missed" % (res["id"], g))
            if len((entry.get("why") or "").strip()) < 10:
                raise ValueError("%s: a hand grade needs a `why` of ten characters or more" % res["id"])
            return g, entry.get("value"), entry["why"]
        entry = entry.get("value")
    gold, v = res.get("golden"), entry
    if v is None:
        return "missed", v, "no value filed"
    if isinstance(gold, dict) and isinstance(v, dict):
        # a table of cells (ten SLIs, twenty incident-minute cells): each cell inside its band, or equal
        bands = res.get("bands") or {}
        ok = 0
        for cell, gv in gold.items():
            pv = v.get(cell)
            b = bands.get(cell)
            if b is not None and isinstance(pv, (int, float)):
                ok += b[0] <= pv <= b[1]
            else:
                ok += same_value(pv, gv) if pv is not None else 0
        share = ok / float(len(gold) or 1)
        why = "%d of %d cells" % (ok, len(gold))
        if share >= 0.999:
            return "right", v, why
        return ("partly" if share >= res.get("partly_share", 0.5) else "missed"), v, why
    if isinstance(gold, (int, float)) and isinstance(v, (int, float)):
        band, partly = res.get("band"), res.get("partly")
        if band and band[0] <= v <= band[1]:
            return "right", v, why
        if not band and abs(v - gold) <= 1e-9 * max(1.0, abs(gold)):
            return "right", v, why
        if partly and partly[0] <= v <= partly[1]:
            return "partly", v, why
        return "missed", v, why
    if isinstance(gold, list) and isinstance(v, list):
        if res.get("ordered") and v == gold:
            return "right", v, why
        a, b = set(map(str, v)), set(map(str, gold))
        if not res.get("ordered") and a == b:
            return "right", v, why
        share = len(a & b) / float(len(a | b) or 1)
        return ("partly" if share >= 0.5 else "missed"), v, why
    return ("right" if str(v).strip().lower() == str(gold).strip().lower() else "missed"), v, why


def same_value(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(same_value(a[k], b[k]) for k in a)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-9 * max(1.0, abs(a))
    if isinstance(a, list) and isinstance(b, list):
        return [str(x) for x in a] == [str(x) for x in b]
    return str(a).strip().lower() == str(b).strip().lower()


def block_of(graded_as):
    g = (graded_as or "").lower()
    if "recommend" in g or g.strip() == "call":
        return "recommendation"
    if "component" in g:
        return "components"
    return "asks"


def measure(task_dir):
    ej = os.path.join(task_dir, "generator", "effort.json")
    E = json.load(open(ej))
    W = dict(DEFAULT_WEIGHTS)
    W.update(E.get("weights") or {})
    res = E["results"]
    counts = {}
    for r in res:
        counts[block_of(r.get("graded_as"))] = counts.get(block_of(r.get("graded_as")), 0) + 1
    table, score, done = [], {p: W["instruction"] for p in PASSES}, {p: 0.0 for p in PASSES}
    for r in res:
        b = block_of(r.get("graded_as"))
        w = W[b] / counts[b]
        line = {"id": r["id"], "name": r.get("name", ""), "block": r.get("graded_as", ""), "weight": w}
        for p in PASSES:
            g, v, why = grade(r["passes"].get(p), r)
            line[p] = (g, v, why)
            score[p] += w * SCORE[g]
            done[p] += SCORE[g]
        table.append(line)
    # Blocks with no result carry no rubric weight here: the asks or components a build never asked for.
    missing = sum(W[b] for b in ("recommendation", "components", "asks") if b not in counts)
    scale = 1.0
    if missing:
        scale = 100.0 / (100.0 - missing)
        score = {p: s * scale for p, s in score.items()}
    # The golden is the answer blocks' figure, and a hand grade respects the chain.
    problems = []
    fj = os.path.join(task_dir, "generator", "figures.json")
    figs = json.load(open(fj)) if os.path.exists(fj) else None
    for r in res:
        key = r.get("figure")
        if figs is None:
            problems.append("no generator/figures.json to tie %s to" % r["id"])
        elif not key or key not in figs:
            problems.append("%s names no figures.json key (figure: %r)" % (r["id"], key))
        elif not same_value(figs[key], r.get("golden")):
            problems.append("%s golden %r is not figures.json %s %r" % (r["id"], r.get("golden"), key, figs[key]))
    order = {"missed": 0, "partly": 1, "right": 2}
    by_id = {t["id"]: t for t in table}
    hand = 0
    for r in res:
        line = by_id[r["id"]]
        for p in PASSES:
            entry = r["passes"].get(p)
            is_hand = isinstance(entry, dict) and set(entry) <= {"value", "grade", "why"} and entry.get("grade")
            hand += 1 if is_hand else 0
            if not is_hand or line[p][0] != "right" or (r.get("independent") or "").strip():
                continue
            missed = [d for d in r.get("depends") or [] if d in by_id and by_id[d][p][0] == "missed"]
            if missed:
                problems.append("%s is hand-graded Right in the %s pass while %s is Missed there: the grader compares "
                                "to the golden, so name the independent input or grade it lower"
                                % (r["id"], p, ", ".join(missed)))
    hints = E.get("hints") or []
    rescued = []
    for h in hints:
        n = 0
        for rid in h.get("rescues", []):
            line = next((t for t in table if t["id"] == rid), None)
            if line and line["careful"][0] != "right":
                n += 1
        rescued.append((n, h.get("sentence", "")))
    return table, score, done, rescued, len(res), problems, hand, scale


def note_table(task_dir):
    """The Effort test table the design note carries, as {result id: (quick, careful, thorough)}."""
    sys.path.insert(0, HERE)
    import precut as P
    note = os.path.join(task_dir, "DESIGN_NOTE.md")
    secs = P.sections(open(note, encoding="utf-8", errors="replace").read())
    rows, problem = P.effort_table(P.section(secs, "Effort test") or "")
    if problem:
        return None, None
    out = {}
    for r in rows:
        m = re.match(r"([A-Z]{1,2}\d{1,2}[a-z]?)\b", r["result"])
        if m:
            out[m.group(1)] = (r["quick"], r["careful"], r["thorough"])
    pe = P.labelled(P.section(secs, "Effort test") or "", "Pair estimate") or ""
    pn = re.search(r"\d+(?:\.\d+)?", pe)
    return out, (float(pn.group(0)) if pn else None)


IN_FLIGHT = ("DRAWING", "DESIGN", "BUILD", "PAUSED", "RETURNED")


def in_flight(task_dir):
    try:
        return (json.load(open(os.path.join(task_dir, "pipeline.json"))).get("status") or "DESIGN") in IN_FLIGHT
    except Exception:
        return True


def _key(a):
    return json.dumps(sorted(a) if isinstance(a, list) else a, sort_keys=True)


def factorial_rows(task_dir, E, table, n, P):
    """The stump factorial: two or more stumps each necessary, none sufficient, the careful pass the reflex route."""
    rows = []
    strict = in_flight(task_dir)

    def row(check, ok, detail, warn=False):
        rows.append((check, "PASS" if ok else ("WARN" if (warn or not strict) else "FAIL"), detail))

    F = E.get("factorial")
    if not F:
        row("stump factorial recorded", False, "no `factorial` block: list every judgment the call can turn on (stump or "
            "reflex), the reflex route's answer, and for each stump the answer with it dropped alone from the golden and "
            "with it fixed alone on the reflex route (stumping Part 3.3)")
        return rows, None
    gold = F.get("golden_answer")
    rr = (F.get("reflex_route") or {}).get("answer")
    js = F.get("judgments") or []
    stumps = [j for j in js if j.get("kind") == "stump"]
    rec = next((t for t in table if (t["block"] or "").lower().startswith("recommendation")), None)
    if rec is not None and rr is not None:
        cv = rec["careful"][1]
        row("the careful pass is the reflex route", _key(cv) == _key(rr),
            "the Recommendation's careful value is the reflex route's answer" if _key(cv) == _key(rr) else
            "careful %s, reflex route %s: the careful column sets every reflex judgment right" % (cv, rr))
    row("the reflex route misses the call", rr is not None and _key(rr) != _key(gold),
        "reflex route %s, golden %s" % (rr, gold))
    bad = []
    for j in js:
        ids = j.get("precedent") or []
        kinds = {P[i]["kind"] for i in ids if i in P}
        if j.get("kind") == "stump" and ("reflex" in kinds or not (kinds & {"loss", "named_assumption"})):
            bad.append("%s (%s)" % (j.get("id"), ", ".join(ids) or "no precedent"))
    row("every stump cites a loss or named assumption, none a reflex", not bad,
        "%d stumps cited" % len(stumps) if not bad else "move to reflex or cite a run's loss: " + "; ".join(bad))
    nec = [j for j in stumps if _key((j.get("dropped") or {}).get("answer")) != _key(gold)]
    suff = [j for j in stumps if _key((j.get("alone") or {}).get("answer")) == _key(gold)
            or len((j.get("alone") or {}).get("results_rescued") or []) > n / 3.0]
    names = lambda L: ", ".join("%s %s" % (j.get("id"), (j.get("name") or "")[:40]) for j in L)
    row("two or more stumps each necessary (dropped alone, the call moves)", len(nec) >= 2,
        "%d necessary of %d stumps: %s" % (len(nec), len(stumps), names(nec) or "none") if len(nec) >= 2 else
        "%d necessary (%s): a one-trick build; add an independent judgment that moves the call alone" % (
            len(nec), names(nec) or "none"))
    row("no stump sufficient alone (fixed alone on the reflex route)", not suff,
        "each stump alone leaves the call wrong and rescues a third of the results or fewer" if not suff else
        "fixing one stump rescues the call or more than a third: " + names(suff))
    wrong = {_key((j.get("dropped") or {}).get("answer")) for j in nec}
    level = 5 if (len(nec) >= 3 and len(wrong) >= 2 and not suff) else 4 if (len(nec) >= 2 and not suff) else 3
    row("depth level from the factorial", level >= 4,
        "level %d: %d necessary stumps, %d distinct wrong answers when one is dropped%s" % (
            level, len(nec), len(wrong), "" if level == 5 else " (level 5 needs three, on two or more wrong answers)"),
        warn=level == 4)
    return rows, level


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    task_dir = resolve(args[0])
    if not os.path.exists(os.path.join(task_dir, "generator", "effort.json")):
        print("no generator/effort.json in %s" % task_dir)
        return 2
    if "--precedents" in argv:
        P = load_precedents()
        for kind in ("loss", "named_assumption", "reflex"):
            print("== %s" % kind)
            for p in P.values():
                if p["kind"] == kind:
                    print("  %-4s %-26s %s\n       %s" % (p["id"], p["class"], p["move"], p["source"]))
        return 0
    table, score, done, rescued, n, problems, hand, scale = measure(task_dir)
    if "--markdown" in argv:
        print("| Result | Quick pass | Careful but hurried | Thorough |")
        print("|---|---|---|---|")
        for t in table:
            print("| %s %s | %s | %s | %s |" % (t["id"], t["name"], *(t[p][0].capitalize() for p in PASSES)))
        print("| Roughly | %g of %d | %g of %d | %g of %d |" % (done["quick"], n, done["careful"], n,
                                                              done["thorough"], n))
        return 0
    rows = []

    def row(check, ok, detail, warn=False):
        rows.append((check, "PASS" if ok else ("WARN" if warn else "FAIL"), detail))

    for t in table:
        print("%-4s %-38s %-14s w%5.1f  quick %-7s careful %-7s thorough %-7s" % (
            t["id"], t["name"][:38], t["block"][:14], t["weight"], *(t[p][0] for p in PASSES)))
    print("scores: quick %.1f, careful but hurried %.1f, thorough %.1f (instruction-following earned by each)"
          % (score["quick"], score["careful"], score["thorough"]))
    row("golden tied to the answer blocks, grades respect the chain", not problems,
        "every result" if not problems else "; ".join(problems[:4]))
    row("passes computed, not asserted", hand <= n, "%d of %d cells hand-graded" % (hand, 3 * n) if hand <= n else
        "%d of %d cells hand-graded: compute the hurried passes end to end in the generator" % (hand, 3 * n),
        warn=True)
    row("thorough pass earns every result", done["thorough"] == n, "%g of %d" % (done["thorough"], n))
    row("quick pass earns a third or less", done["quick"] <= n / 3.0, "%g of %d" % (done["quick"], n),
        warn=done["quick"] <= n / 2.0)
    row("more care earns more", done["quick"] < done["careful"] < done["thorough"],
        "%g < %g < %g results" % (done["quick"], done["careful"], done["thorough"]))
    row("pair estimate (the careful but hurried pass)", score["careful"] <= PAIR_TARGET,
        "%.1f (target %.0f, bar %.0f): build to 50 on paper, the platform is the measurement"
        % (score["careful"], PAIR_TARGET, BAR))
    if rescued:
        k, sentence = max(rescued)
        row("largest single hint rescues a third or less", k <= n / 3.0,
            "rescues %d of %d: %s" % (k, n, sentence[:80]), warn=k <= n / 2.0)
    else:
        row("largest single hint recorded", False, "no `hints` in effort.json: name the most useful single sentence "
            "and the results it rescues")
    E = json.load(open(os.path.join(task_dir, "generator", "effort.json")))
    routes = E.get("routes") or []
    if routes:
        gold = next((r for r in routes if r.get("golden")), None)
        wrong = {json.dumps(r["answer"], sort_keys=True) for r in routes if not r.get("golden") and
                 (gold is None or json.dumps(r["answer"], sort_keys=True) != json.dumps(gold["answer"], sort_keys=True))}
        row("different shortcuts land on different wrong answers", len(wrong) >= 2,
            "%d distinct wrong answers over %d shortcuts (the depth scale's level-5 mark)" % (len(wrong), len(routes) - 1),
            warn=True)
    nl = next_level(task_dir)
    P = load_precedents()
    classes = note_classes(task_dir)
    uncited, reflexed, unknown, mismatched = [], [], [], []
    for r in E["results"]:
        t = next(x for x in table if x["id"] == r["id"])
        g = t["careful"][0]
        if g not in ("missed", "partly"):
            continue
        ids = r.get("precedent") or []
        unknown += ["%s:%s" % (r["id"], i) for i in ids if i not in P]
        reflexed += ["%s:%s" % (r["id"], i) for i in ids if i in P and P[i]["kind"] == "reflex"]
        losses = [i for i in ids if i in P and P[i]["kind"] in ("loss", "named_assumption")]
        want = classes.get(r["id"], set())
        matched = [i for i in losses if precedent_classes(P[i]) & want]
        if losses and not matched:
            mismatched.append("%s (note: %s; cited: %s)" % (r["id"], ", ".join(sorted(want)) or "no deep class",
                                                           ", ".join(sorted({c for i in losses for c in precedent_classes(P[i])}))))
        if not matched:
            uncited.append((r["id"], t["weight"], g))
    cited = score["careful"] + scale * sum(w * (1.0 - SCORE[g]) for _, w, g in uncited)
    row("careful losses cite a frontier precedent", not uncited and not unknown,
        "every Missed or Partly cell cites a run or client page" if not uncited and not unknown else
        "uncited: %s%s%s (references/precedents.json; a precedent counts only when its class is the result's hurried "
        "class in the Results chain; add a run's own line, never a design's)" % (
            ", ".join(x[0] for x in uncited) or "none", ("; unknown ids " + ", ".join(unknown)) if unknown else "",
            ("; class unmatched " + "; ".join(mismatched)) if mismatched else ""),
        warn=not nl)
    if reflexed:
        row("no reflex priced as a loss", False, "a reflex id on a lost cell, the runs make that move unprompted: %s"
            % ", ".join(reflexed), warn=not nl)
    row("pair estimate with uncited losses graded Right", cited <= PAIR_TARGET,
        "%.1f (measured %.1f; %d uncited cell%s regraded Right)" % (cited, score["careful"], len(uncited),
                                                                   "" if len(uncited) == 1 else "s"), warn=not nl)
    frows, level = factorial_rows(task_dir, E, table, n, P)
    rows.extend(frows)
    F = E.get("forcing")
    if not F:
        row("forcing recorded on both sides", False, "no `forcing` block: the golden family, the shortcuts and each "
            "fitted input's perturbation, each placed against the call's line", warn=not nl)
    else:
        fam, sc, pert = F.get("golden_family") or [], F.get("shortcuts") or [], F.get("perturbations") or []
        row("golden family run (three or more rivals)", len(fam) >= 3, "%d rival methods recorded" % len(fam), warn=not nl)
        if (F.get("kind") or "numeric") == "numeric":
            line, side = F.get("line"), (F.get("golden_side") or "").lower()
            if not isinstance(line, (int, float)) or side not in ("above", "below"):
                row("forcing line and side", False, "a numeric forcing block needs `line` and `golden_side` above or below")
            else:
                on = (lambda v: v > line) if side == "above" else (lambda v: v < line)
                fam_off = [x.get("name") for x in fam if not on(x.get("value"))]
                m = min((abs(x["value"] - line) for x in fam), default=None)
                row("every golden-family variant on the golden's side", not fam_off,
                    ("nearest variant %.4g from the line at %.4g" % (m, line)) if not fam_off and m is not None else
                    "across the line: %s" % ", ".join(map(str, fam_off)), warn=not nl)
                sc_on = [x.get("name") for x in sc if on(x.get("value"))]
                row("the shortcuts land across the line", bool(sc) and not sc_on,
                    ("%d shortcuts, nearest %.4g from the line" % (len(sc), min(abs(x["value"] - line) for x in sc)))
                    if sc and not sc_on else ("no shortcuts recorded" if not sc else
                                              "on the golden's side, so they land the call: %s" % ", ".join(map(str, sc_on))),
                    warn=not nl)
                p_off = [x.get("input") for x in pert if not on(x.get("value"))]
                row("the call survives each fitted input's perturbation", bool(pert) and not p_off,
                    ("%d perturbations hold" % len(pert)) if pert and not p_off else
                    ("none recorded" if not pert else "the call moves under: %s" % ", ".join(map(str, p_off))),
                    warn=not nl)
        else:
            gold = F.get("golden_answer")
            if gold is None:
                g_route = next((r for r in (E.get("routes") or []) if r.get("golden")), None)
                gold = g_route["answer"] if g_route else None
            key = lambda a: json.dumps(sorted(a) if isinstance(a, list) else a, sort_keys=True)
            fam_off = [x.get("name") for x in fam if gold is None or key(x.get("answer")) != key(gold)]
            row("every golden-family variant files the golden answer", bool(fam) and not fam_off,
                "%d variants agree" % len(fam) if fam and not fam_off else "differ: %s" % ", ".join(map(str, fam_off)),
                warn=not nl)
            p_off = [x.get("input") for x in pert if gold is None or key(x.get("answer")) != key(gold)]
            row("the call survives each fitted input's perturbation", bool(pert) and not p_off,
                ("%d perturbations hold" % len(pert)) if pert and not p_off else
                ("none recorded" if not pert else "the call moves under: %s" % ", ".join(map(str, p_off))), warn=not nl)
    if "--check-note" in argv:
        paper, pe = note_table(task_dir)
        if paper is None:
            row("note agrees with the measurement", False, "the design note has no Effort test table")
        else:
            off = [t["id"] for t in table if paper.get(t["id"]) != tuple(t[p][0] for p in PASSES)]
            row("note agrees with the measurement", not off,
                "every result" if not off else "the note's grades differ from the measurement on: " + ", ".join(off))
            if pe is not None:
                row("note's pair estimate is the measured one", abs(pe - score["careful"]) <= 1.0,
                    "note %.1f, measured %.1f" % (pe, score["careful"]))
    fails = [r for r in rows if r[1] == "FAIL"]
    for c, lv, d in rows:
        print("%-4s  %-44s %s" % (lv, c, d))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
