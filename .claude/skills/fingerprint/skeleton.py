#!/usr/bin/env python3
"""skeleton.py, the client's own duplicate test run mechanically: skeleton against skeleton, element by element.

    python3 .claude/skills/fingerprint/skeleton.py check task19            # or a scratch card .json
    python3 .claude/skills/fingerprint/skeleton.py lessons [--min 2]       # how often each lesson is already taught
    python3 .claude/skills/fingerprint/skeleton.py matrix                  # every pair on file at severity 1 to 3
    python3 .claude/skills/fingerprint/skeleton.py selftest                # the calibration the rule is held to
    python3 .claude/skills/fingerprint/skeleton.py validate                # every skeleton against the vocabulary

The client compares two tasks on their skeleton, not their setting (Templated Task Examples, read 2026-11-11): the
decision form, the deciding lessons (the trap that makes the easy answer wrong), how the solver detects each, the
resolving moves, the file roles and the answer pattern. A reviewer swaps the nouns of one task into the other and
counts what carries across unchanged; a change of domain does not reset the count. Its three severities, all sent
back:

  1 near copy     the same trap, the same method and the same file roles; only the setting and the numbers change
  2 templated     the same deciding lesson inside the same scaffold, with one part re-pointed (new physics, a new
                  estimator)
  3 variant       real new work, but the step that decides the answer, or the decision skeleton around it, is
                  already in the dataset; and a lesson two accepted tasks already turn on is not taught a third time

A card carries `skeleton` (skeleton_vocab.json keys; `mechanisms` are the build's own physics as free slugs, so a near
copy that keeps the mechanism is told from a templated build that re-points it). Lineage entries carry theirs, so a
re-root is compared with its own dead architectures: re-pointing one part of a scaffold the runs already landed is
the severity 2 pattern (task4 architectures 6 to 10, task10 architectures 4 to 7). The library of everything the
client has shown us is corpus/client_skeletons.json.

guard.py check, register and heart call findings() here, so every draw meets it with no new wiring. Differentiation
never clears it. A card registered before RULE_FROM meets it as WARN (no build already past design flips to BLOCK);
every later card, and every unfiled draft, meets it in full. It reads files only and spawns nothing.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.join(HERE, "skeleton_vocab.json")
LIBRARY = os.path.join(HERE, "corpus", "client_skeletons.json")
APPROVED = os.path.join(HERE, "corpus", "approved.json")
CARDS = os.path.join(HERE, "cards")
RULE_FROM = "2026-11-11T15:58:00Z"
LIST_KEYS = ("lessons", "mechanisms", "detection", "moves", "file_roles")
VOCAB_OF = {"decision_form": "decision_forms", "answer_pattern": "answer_patterns", "lessons": "lessons",
            "detection": "detections", "moves": "moves", "file_roles": "file_roles"}
# Elements every task carries, which identify nothing: they never count as a match.
GENERIC_PATTERNS = {"shortcuts_land_on_distinct_wrong_answers", "robust_call_figures_graded", "figure_crosses_bar",
                    "naive_set_swaps_members"}
# Decision forms too common to identify a skeleton on their own (the client's pages name specific forms: "rank six,
# name one" with its board minute, "twelve units, at most three, a runner-up", "act only if the whole interval clears").
GENERIC_FORMS = {"go_hold_stop_on_figure", "forecast_figure_with_range", "set_over_threshold", "rank_n_name_one",
                 "pick_one_of_few_options", "dial_or_cap_setting"}
GENERIC_MOVES = {"variant_sweep_holds_call", "back_test_select_estimator", "bridge_by_contribution"}
GENERIC_ROLES = {"primary_record", "governing_standard", "unused_distractor", "field_legend_or_dictionary"}
TEACHING = {"accepted", "judgment_call", "approved"}   # our unsubmitted live builds ("on_file") teach nothing yet
SEV_NAME = {1: "near copy", 2: "templated", 3: "variant"}


def load_vocab():
    return json.load(open(VOCAB))


def _load_library_file():
    try:
        return json.load(open(LIBRARY)).get("entries", [])
    except Exception:
        return []


load_library = _load_library_file


def validate(sk, vocab):
    """Every element present and keyed in the vocabulary; mechanisms free slugs."""
    errs = []
    if not isinstance(sk, dict):
        return ["skeleton is not an object"]
    for k in ("decision_form", "answer_pattern"):
        v = sk.get(k)
        if not v:
            errs.append("skeleton.%s missing" % k)
        elif v not in vocab[VOCAB_OF[k]]:
            errs.append("skeleton.%s %r is not a key in skeleton_vocab.json %s" % (k, v, VOCAB_OF[k]))
    for k in LIST_KEYS:
        v = sk.get(k)
        if not isinstance(v, list) or not v:
            errs.append("skeleton.%s must be a non-empty list" % k)
            continue
        if k == "mechanisms":
            bad = [x for x in v if not isinstance(x, str) or not re.fullmatch(r"[a-z0-9_]{3,80}", x)]
            if bad:
                errs.append("skeleton.mechanisms must be lower-case slugs in the build's own physics: %s" % bad)
            continue
        bad = [x for x in v if x not in vocab[VOCAB_OF[k]]]
        if bad:
            errs.append("skeleton.%s keys not in skeleton_vocab.json %s: %s" % (k, VOCAB_OF[k], ", ".join(map(str, bad))))
    return errs


def _set(sk, k, drop=()):
    return {x for x in (sk.get(k) or []) if x not in drop}


def compare(a, b):
    """How much of skeleton a carries across into skeleton b, and the client's severity (0 when none applies)."""
    la, lb = list(a.get("lessons") or []), _set(b, "lessons")
    L = set(la) & lb
    all_l = bool(L) and set(la) <= lb
    main = bool(la) and la[0] in lb
    M = _set(a, "moves", GENERIC_MOVES) & _set(b, "moves", GENERIC_MOVES)
    K = _set(a, "mechanisms") & _set(b, "mechanisms")
    T = _set(a, "detection") & _set(b, "detection")
    D = (bool(a.get("decision_form")) and a.get("decision_form") == b.get("decision_form")
         and a.get("decision_form") not in GENERIC_FORMS)
    A = (bool(a.get("answer_pattern")) and a.get("answer_pattern") == b.get("answer_pattern")
         and a.get("answer_pattern") not in GENERIC_PATTERNS)
    ra, rb = _set(a, "file_roles", GENERIC_ROLES), _set(b, "file_roles", GENERIC_ROLES)
    J = len(ra & rb) / float(len(ra | rb)) if (ra | rb) and min(len(ra), len(rb)) >= 2 else 0.0
    sev, why = 0, ""
    if all_l and M and K and (D or A) and J >= 0.5:
        sev, why = 1, "the same trap, mechanism, method, decision form, answer pattern and file roles"
    elif all_l and M and (D or A):
        sev, why = 2, "every deciding lesson and its resolving move inside the same %s, with %s re-pointed" % (
            "decision form" if D else "answer pattern", "the mechanism" if not K else "the file roles")
    elif main and D:
        sev, why = 3, "the lesson the call turns on (%s) is already decided inside the same decision form" % la[0]
    elif L and D and A:
        sev, why = 3, "the decision skeleton (form and answer pattern) with a shared lesson (%s)" % ", ".join(sorted(L))
    elif D and A and M and J >= 0.5:
        sev, why = 3, "the decision skeleton, the resolving move and the file roles, with new lessons"
    score = 3 * len(L) + 2 * len(M) + 2 * len(K) + (2 if D else 0) + (1 if A else 0) + len(T) + 2 * J
    return {"severity": sev, "why": why, "score": score, "lessons": sorted(L), "moves": sorted(M),
            "mechanisms": sorted(K), "detection": sorted(T), "decision_form": D, "answer_pattern": A,
            "file_roles": round(J, 2), "main_shared": main, "all_lessons_shared": all_l}


def arch_num(x):
    """The architecture number of a card or lineage entry, whose field is free text ('v7', 'v6 (re-root ...)', 5)."""
    m = re.search(r"\d+", str(x if x is not None else ""))
    return m.group(0) if m else "?"


def approved_set():
    try:
        return {(a["task"], str(a["architecture"])) for a in json.load(open(APPROVED)).get("approved", [])}
    except Exception:
        return set()


def entries_from_cards(cards):
    """One entry per card skeleton and per lineage skeleton. Ours teach a lesson only once approved (corpus/
    approved.json); a live build is on_file (every pair rule applies to it) and a spent architecture is screened as
    a scaffold."""
    out = []
    appr = approved_set()
    for c in cards:
        t = c.get("task") or "?"
        sk = c.get("skeleton")
        if isinstance(sk, dict) and sk:
            spent = bool(c.get("architecture_spent"))
            status = "approved" if (t, arch_num(c.get("architecture"))) in appr else ("spent" if spent else "on_file")
            out.append({"id": "%s v%s" % (t, arch_num(c.get("architecture"))), "task": t, "lineage": False,
                        "status": status, "title": (c.get("niche") or "")[:120], "skeleton": sk})
        for l in c.get("lineage") or []:
            if isinstance(l, dict) and isinstance(l.get("skeleton"), dict) and l["skeleton"]:
                out.append({"id": "%s arch %s" % (t, arch_num(l.get("architecture"))), "task": t, "lineage": True,
                            "status": "approved" if (t, arch_num(l.get("architecture"))) in appr else "spent",
                            "title": str(l.get("fate") or "")[:120], "skeleton": l["skeleton"]})
    return out


def library_entries():
    out = []
    for e in load_library():
        out.append({"id": e["id"], "task": e["id"], "lineage": False, "status": e.get("status", "accepted"),
                    "title": e.get("title", ""), "skeleton": e.get("skeleton") or {}, "client": True})
    return out


def carriers(lesson, entries, exclude_task=None):
    return [e for e in entries if e["status"] in TEACHING and e["task"] != exclude_task
            and lesson in (e["skeleton"].get("lessons") or [])]


def grandfathered(cand):
    reg = cand.get("registered") or ""
    return bool(reg) and reg < RULE_FROM


def findings(cand, cards, vocab=None):
    """Guard findings for a candidate card: [{level, rule, msg, against, fix}]. Never cleared by differentiation."""
    vocab = vocab or load_vocab()
    out = []
    gf = grandfathered(cand)
    me = cand.get("task")

    def add(level, rule, msg, against=(), fix=""):
        if gf and level == "BLOCK":
            level, msg = "WARN", msg + " (registered before the skeleton rule of %s: WARN, not BLOCK)" % RULE_FROM[:10]
        out.append({"level": level, "rule": rule, "msg": msg, "against": list(against), "fix": fix})

    sk = cand.get("skeleton")
    if not isinstance(sk, dict) or not sk:
        add("BLOCK", "skeleton.missing", "the card carries no skeleton, so the client's own duplicate test cannot run",
            fix="fill `skeleton` from the design note (fingerprint Part 1b: decision_form, answer_pattern, lessons with "
                "the one the call turns on first, mechanisms, detection, moves, file_roles; keys in skeleton_vocab.json)")
        return out
    for e in validate(sk, vocab):
        add("BLOCK", "skeleton.vocab", e, fix="use skeleton_vocab.json keys; add a key only when none is honest")
    others = [c for c in cards if c.get("task") != me]
    own = [c for c in cards if c.get("task") == me]
    pool = entries_from_cards(others) + library_entries()
    own_entries = [e for e in entries_from_cards(own) if e["lineage"] or e["id"] != "%s v%s" % (me, arch_num(cand.get("architecture")))]
    own_entries += [e for e in entries_from_cards([{"task": me, "lineage": cand.get("lineage") or []}]) if e["lineage"]]
    seen = set()
    own_entries = [e for e in own_entries if not (e["id"] in seen or seen.add(e["id"]))]
    for e in pool:
        r = compare(sk, e["skeleton"])
        if not r["severity"]:
            continue
        thin = len(sk.get("lessons") or []) <= 2
        hard = r["severity"] <= 2 or (e["status"] in TEACHING and (thin or len(r["lessons"]) >= 2))
        add("BLOCK" if hard else "WARN", "skeleton.%s" % SEV_NAME[r["severity"]].replace(" ", "_"),
            "severity %d (%s) against %s [%s]: %s" % (r["severity"], SEV_NAME[r["severity"]], e["id"], e["status"], r["why"]),
            [e["id"]], "redraw the element the match names: a new deciding lesson, or a new decision form and answer "
                       "pattern; a new setting never clears it (the client swaps the nouns and counts)")
    for e in own_entries:
        r = compare(sk, e["skeleton"])
        if r["severity"] and r["severity"] <= 2:
            add("BLOCK", "skeleton.own_lineage",
                "severity %d against this slot's own %s: %s; re-pointing one part of a scaffold the runs already "
                "landed is the templated pattern (task4 architectures 6 to 10, task10 architectures 4 to 7)"
                % (r["severity"], e["id"], r["why"]), [e["id"]],
                "a re-root changes the deciding lessons and the decision form, not one correction (stumping Part 8)")
        elif r["severity"] == 3:
            add("WARN", "skeleton.own_lineage", "severity 3 against this slot's own %s: %s" % (e["id"], r["why"]), [e["id"]])
    lessons = list(sk.get("lessons") or [])
    everyone = pool + own_entries
    sat = {}
    for les in lessons:
        cs = carriers(les, everyone, exclude_task=me)
        sat[les] = [c["id"] for c in cs]
    taught = [les for les in lessons if len(sat[les]) >= 2]
    if lessons and len(lessons) <= 2 and lessons[0] in taught:
        add("BLOCK", "skeleton.lesson_taught",
            "the call turns on %s, already taught by %d tasks on file, and the chain has %d lesson%s: a third copy "
            "teaches little" % (lessons[0], len(sat[lessons[0]]), len(lessons), "" if len(lessons) == 1 else "s"),
            sat[lessons[0]][:6], "make another judgment the one the call turns on, and add independent judgments "
                                 "of other kinds (depth level 4 or 5); this lesson may stay as one step")
    elif lessons and 2 * len(taught) > len(lessons):
        add("BLOCK", "skeleton.lesson_taught",
            "%d of the chain's %d lessons are already taught twice or more on file (%s): the chain is assembled from "
            "lessons the dataset holds" % (len(taught), len(lessons), ", ".join(taught)),
            sorted({i for les in taught for i in sat[les]})[:8],
            "replace the taught lessons with judgments no build on file decides (skeleton.py lessons --min 2)")
    else:
        for les in taught:
            add("WARN", "skeleton.lesson_taught", "%s is already taught by %d tasks on file; it is one step among "
                "several here, never the one the call turns on" % (les, len(sat[les])), sat[les][:6])
        if lessons and len(sat[lessons[0]]) == 1:
            add("WARN", "skeleton.lesson_once", "the lesson the call turns on (%s) is already taught once (%s)"
                % (lessons[0], sat[lessons[0]][0]), sat[lessons[0]])
    ours_live = [e for e in entries_from_cards(others) if e["status"] == "on_file"]
    for les in lessons:
        mine = [e["id"] for e in ours_live if les in (e["skeleton"].get("lessons") or [])]
        if len(mine) >= 2:
            add("WARN", "skeleton.house_lesson", "%s is on %d of our live builds: once they are accepted the client "
                "reads a third as a re-set" % (les, len(mine)), mine[:6])
    form, pat = sk.get("decision_form"), sk.get("answer_pattern")
    live = [c for c in others if not c.get("architecture_spent") and (c.get("skeleton") or {}).get("decision_form") == form]
    shell = [c for c in live if form not in GENERIC_FORMS and pat and pat not in GENERIC_PATTERNS
             and (c.get("skeleton") or {}).get("answer_pattern") == pat]
    if form and len(shell) >= 2:
        add("BLOCK", "skeleton.house_shell", "decision form %s with answer pattern %s is on %d live builds: the "
            "client reads that shell on its third use as a house template" % (form, pat, len(shell)),
            [c.get("task") for c in shell][:8],
            "draw the decision form and the answer's shape from the decision's own unit (a ranked list of causes, a "
            "timeline, a forecast with bands, a bridge that adds up, per-unit diagnoses, a monitoring rule)")
    elif form and len(live) >= 4:
        add("WARN", "skeleton.house_shell", "decision form %s is on %d live builds; vary it where the decision allows"
            % (form, len(live)), [c.get("task") for c in live][:8])
    return out


def nearest(sk, entries, n=5):
    scored = []
    for e in entries:
        r = compare(sk, e["skeleton"])
        scored.append((r["severity"] or 9, -r["score"], e, r))
    scored.sort(key=lambda x: (x[0], x[1]))
    return scored[:n]


def print_table(sk, e, r):
    b = e["skeleton"]
    print("  vs %s [%s] %s" % (e["id"], e["status"], (e.get("title") or "")[:80]))
    print("     severity %s%s" % (r["severity"] or "none", (": " + r["why"]) if r["why"] else ""))
    for k in ("decision_form", "answer_pattern"):
        tag = "same" if r[k] else "new "
        print("     %-15s %s  %s | %s" % (k, tag, sk.get(k), b.get(k)))
    for k in ("lessons", "mechanisms", "detection", "moves"):
        shared = r[k]
        tag = "same" if shared and set(shared) >= set(sk.get(k) or []) else ("part" if shared else "new ")
        print("     %-15s %s  %s" % (k, tag, ", ".join(shared) if shared else "-"))
    print("     %-15s %.2f overlap (non-generic roles)" % ("file_roles", r["file_roles"]))


def load_cards():
    cards = []
    for f in sorted(os.listdir(CARDS)):
        if f.endswith(".json"):
            try:
                cards.append(json.load(open(os.path.join(CARDS, f))))
            except Exception:
                pass
    return cards


def load_candidate(arg, cards):
    if os.path.isfile(arg):
        return json.load(open(arg))
    t = arg if arg.startswith(("task", "mark")) else "task" + arg
    for c in cards:
        if c.get("task") == t:
            return c
    raise SystemExit("no card for %s" % arg)


def cmd_check(arg):
    cards = load_cards()
    cand = load_candidate(arg, cards)
    fs = findings(cand, cards)
    sk = cand.get("skeleton") or {}
    if sk:
        pool = entries_from_cards([c for c in cards if c.get("task") != cand.get("task")]) + library_entries()
        print("== skeleton of %s v%s: %s / %s; lessons %s" % (cand.get("task"), arch_num(cand.get("architecture")),
              sk.get("decision_form"), sk.get("answer_pattern"), ", ".join(sk.get("lessons") or [])))
        print("nearest on file (the client's element-by-element read):")
        for _, _, e, r in nearest(sk, pool):
            print_table(sk, e, r)
    lv = "BLOCK" if any(f["level"] == "BLOCK" for f in fs) else ("WARN" if fs else "PASS")
    print("\n%s  skeleton %s" % (lv, cand.get("task")))
    for f in fs:
        print("  %-5s %-24s %s%s" % (f["level"], f["rule"], f["msg"], (" against " + ", ".join(f["against"])) if f["against"] else ""))
        if f["fix"] and f["level"] == "BLOCK":
            print("        fix: %s" % f["fix"])
    return 1 if lv == "BLOCK" else 0


def cmd_lessons(min_n):
    cards = load_cards()
    entries = entries_from_cards(cards) + library_entries()
    vocab = load_vocab()
    rows = []
    for les in vocab["lessons"]:
        cs = carriers(les, entries)
        main = [c for c in cs if (c["skeleton"].get("lessons") or [None])[0] == les]
        if len(cs) >= min_n:
            rows.append((len(cs), len(main), les, [c["id"] for c in cs]))
    rows.sort(key=lambda r: (-r[0], r[2]))
    print("lessons taught on file (the client's accepted and level 3 tasks, our approved builds), most first:")
    for n, m, les, ids in rows:
        flag = "SATURATED" if n >= 2 else "once"
        print("  %-9s %2d (%d as the deciding lesson)  %-36s %s" % (flag, n, m, les, ", ".join(ids)[:150]))
    return 0


def cmd_matrix():
    cards = load_cards()
    ours = entries_from_cards(cards)
    lib = library_entries()
    hits = []
    for i, a in enumerate(ours):
        for b in ours[i + 1:] + lib:
            if a["task"] == b["task"] and not (a["lineage"] or b["lineage"]):
                continue
            r = compare(a["skeleton"], b["skeleton"])
            r2 = compare(b["skeleton"], a["skeleton"])
            s = min(x for x in (r["severity"] or 9, r2["severity"] or 9))
            if s <= 3:
                hits.append((s, a["id"], b["id"], (r if (r["severity"] or 9) == s else r2)["why"]))
    hits.sort()
    print("pairs on file at severity 1 to 3 (our builds against each other and against the client's library):")
    for s, a, b, why in hits:
        print("  %d %-11s %-26s %-28s %s" % (s, SEV_NAME[s], a, b, why[:110]))
    return 0


def cmd_validate():
    vocab = load_vocab()
    bad = 0
    for e in load_library():
        for err in validate(e.get("skeleton"), vocab):
            print("library %s: %s" % (e["id"], err)); bad += 1
    for c in load_cards():
        if c.get("skeleton"):
            for err in validate(c["skeleton"], vocab):
                print("card %s: %s" % (c.get("task"), err)); bad += 1
        for l in c.get("lineage") or []:
            if isinstance(l, dict) and l.get("skeleton"):
                for err in validate(l["skeleton"], vocab):
                    print("card %s lineage arch %s: %s" % (c.get("task"), l.get("architecture"), err)); bad += 1
    print("%s: %d problems" % ("PASS" if not bad else "FAIL", bad))
    return 1 if bad else 0


def cmd_selftest():
    """The calibration the rule is held to: the client's five send-backs at their own severities, task4's re-pointed
    lineage flagged, and the two approved Sulfur builds (task6 v7 and task457, task14 arch 1) left apart."""
    lib = {e["id"]: e for e in library_entries()}
    cards = {c.get("task"): c for c in load_cards()}
    ok = True

    def expect(label, a, b, want):
        nonlocal ok
        r = compare(a, b)
        good = (r["severity"] == want) if want is not None else (r["severity"] != 0)
        ok &= good
        print("  %s  %-58s severity %s (want %s)%s" % ("PASS" if good else "FAIL", label, r["severity"] or 0,
              "any" if want is None else want, (": " + r["why"]) if r["why"] else ""))

    print("client's Templated Task Examples, submitted against existing:")
    for sub, ext, want in (("html:wholesale-connectors", "html:grocer-bays", 1),
                           ("html:shrub-root-stiffness", "html:valve-failure-on-demand", 2),
                           ("html:snowpack-trend", "html:nursing-home-citations", 2),
                           ("html:fuel-pass-through", "html:recipe-app-home-card", 3),
                           ("html:switchback-sizing", "html:b2b-experiment-sizing", 3)):
        expect("%s vs %s" % (sub[5:], ext[5:]), lib[sub]["skeleton"], lib[ext]["skeleton"], want)
    t4 = {arch_num(l.get("architecture")): l for l in (cards.get("task4") or {}).get("lineage") or []
          if isinstance(l, dict) and l.get("skeleton")}
    if "7" in t4 and "6" in t4:
        expect("task4 arch 7 vs arch 6 (one part re-pointed)", t4["7"]["skeleton"], t4["6"]["skeleton"], None)
    else:
        ok = False
        print("  FAIL  task4 lineage skeletons for architectures 6 and 7 missing")
    t14 = {arch_num(l.get("architecture")): l for l in (cards.get("task14") or {}).get("lineage") or []
           if isinstance(l, dict) and l.get("skeleton")}
    t6 = (cards.get("task6") or {}).get("skeleton")
    if t6 and "1" in t14:
        expect("task6 v7 vs task457 (task14 arch 1), both approved", t6, t14["1"]["skeleton"], 0)
        expect("task457 (task14 arch 1) vs task6 v7", t14["1"]["skeleton"], t6, 0)
    else:
        ok = False
        print("  FAIL  task6 skeleton or task14 lineage arch 1 skeleton missing")
    allc = load_cards()
    for label, sk in (("task6 v7 as a new draw", t6), ("task457 as a new draw", (t14.get("1") or {}).get("skeleton"))):
        if not sk:
            continue
        probe = {"task": "probe_selftest", "architecture": 1, "skeleton": sk}
        blocks = [f for f in findings(probe, [c for c in allc if c.get("task") not in ("task6", "task14")])
                  if f["level"] == "BLOCK"]
        good = not blocks
        ok &= good
        print("  %s  %-58s %s" % ("PASS" if good else "FAIL", label + " meets no skeleton BLOCK",
              "; ".join(f["rule"] + ": " + f["msg"][:90] for f in blocks) if blocks else "no BLOCK"))
    # Every accepted client task at depth 4 or 5 and every example passes as a new draw against the corpus minus
    # itself, with every rule on: the guard must never refuse what the client accepts.
    global load_library
    base_lib = load_library()
    # The client's own corpus already holds a few genuine overlaps, so a new draw on them would be the third copy and
    # the guard is right to refuse it: example 14 is the recipe app's interval-unit lesson in its k-of-n shell
    # (severity 2), and three or four accepted tasks already turn on interference, the interval unit and the split
    # carried to the decision. Every other accepted task clears as a new draw.
    expected = {"example:14": {"skeleton.templated", "skeleton.lesson_taught"},
                "example:4": {"skeleton.lesson_taught"}, "example:7": {"skeleton.lesson_taught"}}
    print("the client's accepted level 4 and 5 tasks and examples, each as a new draw against the rest:")
    for e in base_lib:
        src = e.get("source", "")
        if not (e["id"].startswith("example:") or (e["id"].startswith("depth:") and ("level 4" in src or "level 5" in src))):
            continue
        rest = [x for x in base_lib if x["id"] != e["id"]]
        load_library = (lambda rest=rest: rest)
        try:
            probe = {"task": "probe_" + re.sub(r"\W", "_", e["id"]), "architecture": 1, "skeleton": e["skeleton"]}
            blocks = [f for f in findings(probe, allc) if f["level"] == "BLOCK"]
        finally:
            load_library = _load_library_file
        rules = {f["rule"] for f in blocks}
        good = rules == expected.get(e["id"], set())
        ok &= good
        if not good or rules:
            print("  %s  %-58s %s" % ("PASS" if good else "FAIL", e["id"] + (" (an overlap the client's corpus holds)" if rules else ""),
                  "; ".join(sorted(rules)) or "no BLOCK"))
    print("  %s  every other accepted client task clears as a new draw" % ("PASS" if ok else "FAIL"))
    # A plain forecast with lessons no task on file uses passes: the guard never refuses a form for being common.
    vocab = load_vocab()
    used = {les for x in (library_entries() + entries_from_cards(allc)) for les in (x["skeleton"].get("lessons") or [])}
    fresh = [les for les in vocab["lessons"] if les not in used][:3]
    probe = {"task": "probe_forecast", "architecture": 1, "skeleton": {
        "decision_form": "forecast_figure_with_range", "answer_pattern": "robust_call_figures_graded", "lessons": fresh,
        "mechanisms": ["probe_mechanism"], "detection": ["second_source_at_other_grain"],
        "moves": ["simulate_with_fitted_inputs"], "file_roles": ["primary_record", "second_grain_source", "schedule_or_plan"]}}
    blocks = [f for f in findings(probe, allc) if f["level"] == "BLOCK"]
    good = bool(fresh) and not blocks
    ok &= good
    print("  %s  %-58s %s" % ("PASS" if good else "FAIL", "a plain forecast with untaught lessons (%s)" % ", ".join(fresh),
          "no BLOCK" if not blocks else "; ".join(f["rule"] for f in blocks)))
    print("SELFTEST %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd = argv[0]
    if cmd == "check" and len(argv) > 1:
        return cmd_check(argv[1])
    if cmd == "lessons":
        n = 1
        if "--min" in argv:
            n = int(argv[argv.index("--min") + 1])
        return cmd_lessons(n)
    if cmd == "matrix":
        return cmd_matrix()
    if cmd == "validate":
        return cmd_validate()
    if cmd == "selftest":
        return cmd_selftest()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
