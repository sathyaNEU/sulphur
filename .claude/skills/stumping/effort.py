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
    return table, score, done, rescued, len(res), problems, hand


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
        m = re.match(r"([A-Z]{1,2}\d{1,2})\b", r["result"])
        if m:
            out[m.group(1)] = (r["quick"], r["careful"], r["thorough"])
    pe = P.labelled(P.section(secs, "Effort test") or "", "Pair estimate") or ""
    pn = re.search(r"\d+(?:\.\d+)?", pe)
    return out, (float(pn.group(0)) if pn else None)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    task_dir = resolve(args[0])
    if not os.path.exists(os.path.join(task_dir, "generator", "effort.json")):
        print("no generator/effort.json in %s" % task_dir)
        return 2
    table, score, done, rescued, n, problems, hand = measure(task_dir)
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
