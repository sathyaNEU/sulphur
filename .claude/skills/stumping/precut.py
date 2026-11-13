#!/usr/bin/env python3
"""precut.py, the paper gate between design (stage 2) and build (stage 3), re-run on every final cut.

    python3 .claude/skills/stumping/precut.py taskNN [--quiet]

Reads <task>/DESIGN_NOTE.md and refuses to open stage 3 until the design is argued on paper the way `stumping`
sets out for the client's bar of 2026-11-09 (`guidelines/client/deep-reasoning.md`): difficulty throughout the
analysis, never one hidden or planted thing that flips the answer.

The contract a build in design or repair meets (DRAWING, DESIGN, BUILD, PAUSED, RETURNED, or any note carrying
`## Results chain`):

  ## Draw                  `Analysis type:` (one of the nine), `Answer shape:` (one of the fourteen), `Weight:`
                           (where the hardness sits, one of the eleven), each different from the recent builds
  ## Deep reasoning        one labelled line per point (DEEP_LABELS)
  ## Results chain         four or more checkable results across three or more of the fourteen areas, each with
                           how it is pinned, its band, the hurried analyst's failure (one of the six deep classes),
                           what it depends on and the answer block it is graded in; a `Carry-forward:` line
  ## Hidden factor record  every hidden factor: real or constructed, only in the deciding units, how it is found,
                           how deep the fix is; refused when constructed and only in the deciding units, or
                           constructed, found in one look and fixed by a routine step (the client's three
                           conditions); or a `No hidden factor:` line
  ## Effort test           a three-pass table pricing every result (quick, careful but hurried, thorough), the
                           quick pass earning a third of the results or fewer, the careful pass strictly between,
                           the thorough pass all; `Measured by:` (effort.py on generator/effort.json),
                           `Largest single hint:` (rescues N of M results), `Pair estimate:` (50 or under)
  ## Data provenance       `Source:` (generated or public); generated data `Behaves like the real thing:`,
                           `Genuine patterns:` (three or more), `Problems by process:`; public data `License:`,
                           `Used as is:`; both `Breadth:`
  ## Template check        `Chain signature:`, `Question form:`, `Nearest build:`; refused when another build on
                           file has the same chain of areas in the same order and the same answer shape
  ## Semantic fork table, ## Closure table (22 axes), ## Literal reader, ## Prompt contract, ## Tried and rejected
  ## Frontier check        the next-level contract (stumping Part 1b and 1c), required in full for a build whose card was
                           registered from skeleton.RULE_FROM on: `Precedents:` (each result the careful pass loses,
                           with the precedents.json ids behind it), `Shallow path checks:` (the checks the hurried
                           route passes and the check of another kind that refutes it), `Assumption made false:`
                           (the assumption a run lists and waves through, false here, and the file that tests it),
                           `Forcing:` (the golden family, the shortcuts and the perturbations against the line),
                           `Noun swap:` (the nearest task on file or in the client's library, nouns swapped, and the
                           elements that carry across); from skeleton.CLOSED_FROM on, `Closed strategies:` (the
                           deciding lesson and why the client's closed page does not hold it, each closed lesson kept
                           as a supporting step and the route showing it alone leaves the call standing); and the
                           card's skeleton screen (fingerprint Part 1b, the closed rule included) clear

  ## Pinning list          every constant the golden's estimator uses that the world also holds (a base temperature, a
                           threshold, an exponent, a share, a draw per unit, a time constant), one row each: Constant |
                           Golden value | Home (the shipped file a real organisation holds that carries it, or the
                           estimator family and its measured spread); and `Variant battery:` (how many variants of
                           every modelled transport were run and that they file one answer). Refused on an in-flight
                           build when missing (determinism-check §1, task7 architecture 12's 58 F that no file held)

  ## Stump factorial       the one-trick guard (stumping Part 3.3), on paper before the generator: `Reflex route:` (every
                           move a run makes unprompted or the files spell out set right, every stump hurried, and the
                           answer it files), and a table, one row per judgment the call can turn on, with columns
                           Judgment | Kind (stump or reflex) | Hurried choice | Evidence (precedents.json ids) |
                           Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told;
                           refused below two stumps whose "Dropped alone" moves the call ("same call" or "no change"
                           when it does not; an empty answer is a move), when any stump's "Fixed alone"
                           reaches the golden, or when a stump's evidence is a reflex or not a loss or named assumption;
                           FAIL on a build still being built or repaired, WARN on one already shipped

A build already READY, in runs or shipped under the retired single-deep-step design meets its old contract and a
WARN naming the retirement: it is not re-shipped until it is re-rooted to the results chain.

It also runs the prompt gate (voice-check.py) on prompt.txt and, where generator/effort.json exists, effort.py.
Exit status: 0 every check passed (WARNs allowed), 1 at least one FAIL, 2 the note or the task is missing. It reads
files and runs two scripts; it spawns no agent and costs nothing.
"""
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
VOICE = os.path.join(REPO, ".claude", "skills", "guide-to-prompt", "references", "voice-check.py")
EFFORT = os.path.join(HERE, "effort.py")
CARDS = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")
VOCAB = os.path.join(REPO, ".claude", "skills", "fingerprint", "vocab.json")

# Statuses whose builds were cut under the retired single-deep-step design and are not being reworked here.
SHIPPED_STATES = ("READY", "RUNS", "SUBMITTED", "APPROVED", "RETIRED", "SHIPPED", "SHIPPED_APPROVED")

# ---- the results-chain contract (the client's bar of 2026-11-09) ----
NEW_REQUIRED = ["Draw", "Deep reasoning", "Results chain", "Hidden factor record", "Effort test", "Data provenance",
                "Template check", "Semantic fork table", "Closure table", "Literal reader", "Prompt contract",
                "Tried and rejected"]
RETIRED_SECTIONS = ["Default path", "Stump sentence", "Survivor anatomy", "Readability screen", "Ladder",
                    "Ask sheet"]
DRAW_LABELS = ("Analysis type", "Answer shape", "Weight")
DEEP_LABELS = ("Task type", "Domain test", "Swap", "Where the weight sits", "Layer 1", "Not one thing",
               "One-fact test", "Not semantics", "Not rule application", "Estimand", "No decoy", "No replay",
               "Pinned", "Run forecast", "Strategy label", "Lesson")
TEMPLATE_LABELS = ("Chain signature", "Question form", "Nearest build")
FRONTIER_LABELS = ("Precedents", "Shallow path checks", "Assumption made false", "Forcing", "Noun swap")
# From skeleton.CLOSED_FROM (the client's closed strategies page, 2026-11-12): the deciding lesson and why it is not on
# the page, and every closed lesson the chain keeps as a supporting step with the route showing it alone does not flip
# the call.
CLOSED_LABEL = "Closed strategies"
# From SCREEN_FROM (the author's direction, 2026-11-13): the design note carries `## Stump screen`, three or more
# candidate traps put through the eleven tests of references/stump-screen.md on paper before any code, three kept.
SCREEN_FROM = "2026-11-13T00:45:00Z"
# From OPEN_FROM (the review round of 2026-11-13: task1 v5, task16 v3 and task13 v5 sent back as not difficult enough at
# rewards 83, 78 and 75, each with one member of its call a run could get wrong): the design note carries
# `## Open members`, two or more members opened by different stumps, and a `Direct route:` line (SKILL.md Part 3.4)
OPEN_FROM = "2026-11-14T00:00:00Z"
FINGERPRINT = os.path.join(REPO, ".claude", "skills", "fingerprint")
MIN_RESULTS, MIN_AREAS = 4, 3
PAIR_TARGET = 50.0

# The fourteen areas, the nine analysis types, the fourteen answer shapes and the eleven weights are keyed in
# vocab.json; these are the words a note may use for each key.
AREA_WORDS = {
    "framing": ("framing",),
    "data-discovery": ("data discovery", "discovery"),
    "assembly-reconciliation": ("assembly", "reconciliation", "record linkage", "linkage"),
    "missingness-measurement": ("missingness", "measurement", "censoring", "truncation"),
    "exploration-triage": ("exploration", "triage"),
    "investigation-loops": ("investigation",),
    "modeling": ("modeling", "modelling"),
    "validation": ("validation", "backtest", "back-test"),
    "causal-reasoning": ("causal",),
    "forecasting": ("forecasting", "forecast"),
    "decomposition-attribution": ("decomposition", "attribution", "bridge"),
    "uncertainty": ("uncertainty",),
    "synthesis": ("synthesis",),
    "self-verification": ("self-verification", "self verification", "verification"),
}
TYPE_WORDS = {
    "descriptive-distribution": ("descriptive", "distribution analysis"),
    "comparative-explanation": ("comparative",),
    "anomaly-detection": ("anomaly",),
    "root-cause": ("root-cause", "root cause"),
    "experiment-causal": ("experiment", "causal analysis"),
    "forecasting": ("forecasting", "predictive"),
    "opportunity-sizing-decision": ("opportunity", "decision support"),
    "etl": ("etl", "extraction", "conformation", "pipeline build"),
    "data-quality-monitoring": ("data quality", "monitoring", "alerting"),
}
SHAPE_WORDS = {
    "ranked-causes": ("ranked causes",),
    "timeline": ("timeline",),
    "forecast-bands-drivers": ("forecast path", "forecast with", "bands, plus its drivers"),
    "bridge": ("bridge",),
    "flagged-set": ("flagged set",),
    "reconciled-table": ("reconciled table",),
    "allocation-sensitivity": ("allocation",),
    "ranked-list-cap": ("ranked list",),
    "schedule-capacity": ("schedule",),
    "monitoring-rule": ("monitoring rule",),
    "scenarios-flip": ("scenarios", "flip point", "call flips"),
    "distribution-cut": ("distribution and", "where it is cut"),
    "composite-score": ("composite score",),
    "defined-metric": ("defined metric", "metric with its properties"),
}
WEIGHT_WORDS = {
    "assembly": ("assembly",),
    "measurement": ("measurement",),
    "triage": ("triage",),
    "investigation": ("investigation",),
    "modeling": ("modeling", "modelling"),
    "validation": ("validation",),
    "attribution": ("attribution",),
    "synthesis": ("synthesis",),
    "allocation": ("allocation",),
    "hard-to-measure": ("hard to measure", "hard-to-measure"),
    "metric-or-rule-design": ("metric design", "rule design", "metric or rule", "rule to design", "metric to design"),
}
DEEP_CLASSES = {
    "method-shortcut": r"method shortcut",
    "unfinished-chain": r"unfinished chain",
    "first-story": r"first story",
    "narrow-look": r"narrow look",
    "dismissed-evidence": r"dismissed (?:its |the run's )?own evidence|dismissed evidence",
    "self-confirming": r"self-confirming",
}
SURFACE_CLASSES = r"planted defect|missed a planted|hidden factor|misread|misapplied|written procedure|formatting"
PASS_SCORE = {"right": 1.0, "partly": 0.5, "missed": 0.0}

# ---- the retired contract (one deep step), kept to read builds cut under it ----
REQUIRED = ["Draw", "Default path", "Stump sentence", "Deep reasoning", "Survivor anatomy", "Readability screen",
            "Semantic fork table", "Ladder", "Closure table", "Literal reader", "Oracles", "Ask sheet",
            "Prompt contract", "Tried and rejected"]
LATER = {"Survivor anatomy"}
THREE_RULES = ("Task type", "Domain test", "Swap", "Layer 1", "Layer 2", "Decisive step", "Not semantics",
               "Not rule application", "Analyst test", "Estimand", "No decoy", "No certified replay", "Chain",
               "Judgment", "Hidden by", "After the notice", "One-fact test", "No replay", "Pinned", "Run forecast",
               "Strategy label", "Lesson")
SULFUR_LABELS = {"Chain", "Judgment", "Hidden by", "After the notice", "One-fact test", "No replay", "Pinned",
                 "Run forecast", "Strategy label"}
ANATOMY = ("Actor", "Link", "Reflex", "Back-test", "Second use", "Shock", "Pins")
PAIR_CEILING = 50.0
MIRROR_CEILING = 25.0
AXES = set(range(1, 23))
STOP = {"the", "and", "with", "from", "that", "this", "than", "into", "over", "under", "about", "ends",
        "golden", "answer", "figure", "candidate", "navigators", "per", "cent"}


def resolve(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    if m:
        return os.path.join(REPO, "task%s" % m.group(1))
    return os.path.abspath(arg)


def sections(text, dupes=None):
    """H2 heading -> body, headings matched case-insensitively on their stripped text.

    A repeated heading used to overwrite the earlier one silently, so a note carrying a duplicated or
    half-spliced section passed every check on whichever copy came last. task199's note reached a
    committed state with two "the judge's FIX_NOW, answered" headings and a "tried and rejected`) |"
    heading sitting inside a table cell, and this gate read it as clean. Repeats are collected into
    `dupes` for the caller to fail on.
    """
    out, cur, buf, seen = {}, None, [], []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = re.sub(r"[`*]", "", m.group(1)).strip().lower(), []
            if cur in seen and dupes is not None:
                dupes.append(cur)
            seen.append(cur)
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def section(secs, name):
    key = name.lower()
    if key in secs:
        return secs[key]
    for k, v in secs.items():   # a heading that starts with the name ("## Ladder (targets)")
        if k.startswith(key):
            return v
    return None


def tables(body):
    """Every markdown table in a body as a list of rows (lists of cells), header first, separators dropped."""
    out, cur = [], []
    for line in body.splitlines():
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            cur.append(cells)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


# The field's named methods, grouped into families so that two lines naming the same method with different
# wording ("the hazard of a violation", "the hazard by time on supervision") still collide.
METHOD_FAMILIES = {
    "test linking": ("concordance", "equipercentile", "equating", "linking", "percentile match",
                     "vertical scale", "score conversion"),
    "regression prediction": ("regression", "ordinary least squares", " ols ", "logistic", "predicted value"),
    "survival and hazard": ("hazard", "survival curve", "survival function", "kaplan", "proportional hazards",
                            "life table", "left truncation", "time to event"),
    "likelihood fitting": ("maximum likelihood", " mle ", "likelihood ratio"),
    "resampling": ("bootstrap", "cross-validation", "jackknife", "permutation test"),
    "shrinkage": ("credibility weighting", "shrinkage", "empirical bayes", "partial pooling"),
    "standardisation": ("standardisation", "standardization", "reweighting", "direct adjustment", "z-score"),
    "causal design": ("propensity", "difference in differences", "instrumental variable", "regression discontinuity",
                      "synthetic control"),
    "triangle development": ("chain ladder", "development triangle", "loss development", "run-off"),
    "extreme value": ("log-pearson", "extreme value", "generalised pareto", "return period"),
    "time series": ("arima", "exponential smoothing", "state space", "seasonal decomposition"),
    "flow balance": ("stock and flow", "max flow", "balance identity"),
    "backtest selection": ("backtest", "back-test", "out-of-sample selection"),
    # A field's own named PROCEDURE collides as surely as its named statistic. Two independent reconnaissance
    # passes found the statistical list alone clears the colliding lines it was built to catch, so the domain
    # procedures go in beside them.
    "audit sampling": ("attribute sample", "attribute sampling", "deviation rate", "sampling unit",
                       "tolerable rate", "monetary unit sampling", "sampling risk"),
    "record linkage": ("record linkage", "entity resolution", "probabilistic linkage", "fellegi",
                       "match weight", "blocking key", "clerical review"),
    "coverage estimation": ("capture-recapture", "dual system", "dual-system", "coverage estimation",
                            "post-enumeration"),
    "mass balance": ("mass balance", "material balance", "conservation identity", "closure error"),
    "emission inventory": ("emission factor", "tier 2 method", "tier-2 method", "activity data"),
    "occupancy and capacity": ("concurrency", "occupancy ceiling", "queueing", "erlang",
                               "utilisation standard", "capacity factor"),
    "seasonal adjustment": ("seasonal adjustment", "x-13", "x-12", "trading day adjustment"),
    "risk adjustment": ("risk adjustment", "case mix", "case-mix", "hierarchical condition"),
    "limit compliance testing": ("delegated authority", "authority schedule", "limit compliance",
                                 "segregation of duties", "three-way match"),
    "reserve measurement": ("loss reserve", "provision measurement", "ibnr", "incurred but not reported"),
}


def method_terms(line):
    """The families of field-named methods a Three-rules line mentions.

    Families, not raw strings: the same method named two ways in two lines must still collide.
    """
    low = " " + (line or "").lower() + " "
    return {fam for fam, pats in METHOD_FAMILIES.items() if any(pat in low for pat in pats)}


def labelled(body, label):
    """The text after `Label:`, with its wrapped continuation lines, up to a blank line, a new bullet, a table row,
    a heading or the next `Label:` line."""
    m = re.search(r"^\s*(?:[-*]\s*)?\**%s\**\s*:?\**\s*(.+?)\s*$" % re.escape(label), body, re.M | re.I)
    if not m:
        return None
    parts = [m.group(1).strip()]
    for line in body[m.end():].splitlines()[1:]:
        s = line.strip()
        if (not s or re.match(r"^([-*]\s|\d+[.)]\s|\||#)", s)
                or re.match(r"^\**[A-Z][A-Za-z0-9 ]{0,30}\**\s*:", s)):
            break
        parts.append(s)
    return " ".join(parts)


def norm_number(s):
    return re.sub(r"[,\s]", "", s)


def tokens(value):
    nums = [norm_number(n) for n in re.findall(r"\d[\d,]*(?:\.\d+)?", value)]
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", value) if w.lower() not in STOP]
    return nums, words


def names_value(sentence, value):
    nums, words = tokens(value)
    flat = norm_number(sentence)
    if any(n and n in flat for n in nums):
        return True
    low = sentence.lower()
    return any(w in low for w in words) if (words and not nums) else False


def build_status(task_dir):
    try:
        import json
        return json.load(open(os.path.join(task_dir, "pipeline.json"))).get("status") or ""
    except Exception:
        return ""


def task_type_serves(task, line):
    """Rule 1: the task type the note names is one of the card's domain's task types and serves its objective.
    Returns (True | False | None, detail); None when the card or vocabulary cannot be read."""
    import json
    try:
        card = json.load(open(os.path.join(CARDS, task + ".json")))
        vocab = json.load(open(VOCAB))
    except Exception:
        return None, "card or vocab.json unreadable; Task type line not checked"
    client = vocab.get("client_domains", {})
    obj, dom = card.get("objective"), card.get("domain")
    doms = [dom] if dom in client else ([card.get("client_domain")] if card.get("client_domain") else
                                        (vocab.get("house_domains", {}).get(dom, {}).get("maps_to") or []))
    low = re.sub(r"[^a-z0-9]+", " ", line.lower())
    named = []
    for d in doms:
        for key, objs in client.get(d, {}).get("task_types", {}).items():
            if key.replace("-", " ") in low:
                named.append((d, key, objs))
    if not named:
        return False, "names none of %s's task types (guide-to-prompt/references/domains/README.md)" % (", ".join(d for d in doms if d) or dom)
    hit = [(d, k) for d, k, objs in named if obj in objs]
    if hit:
        return True, "%s/%s serves %s" % (hit[0][0], hit[0][1], obj)
    return False, "%s serves %s, not %s" % (named[0][1], ", ".join(named[0][2]), obj)


def check_retired(task_dir, note_text, secs, dupes):
    rows = []
    task = os.path.basename(task_dir)

    def row(check, ok, detail, warn=False):
        rows.append((check, "PASS" if ok else ("WARN" if warn else "FAIL"), detail))

    row("no repeated H2 heading", not dupes,
        "each H2 appears once" if not dupes
        else "repeated, so the earlier copy is unread and unchecked: %s"
             % ", ".join(sorted(set(dupes))))

    shipped = build_status(task_dir) in ("SHIPPED", "SHIPPED_APPROVED", "RETIRED", "SUBMITTED", "APPROVED")
    for name in REQUIRED:
        row("section %s" % name, section(secs, name) is not None,
            "## %s present" % name if section(secs, name) is not None else "## %s missing" % name,
            warn=shipped and name in LATER)

    # Draw: the card exists, and the data-native sentence is written somewhere in the note.
    card = os.path.join(CARDS, task + ".json")
    row("card registered", os.path.exists(card), card if os.path.exists(card) else "no card under fingerprint/cards/")
    # A re-rooted slot whose registered card still belongs to the dead architecture passes every
    # note-reading check below vacuously, because the sections being read are the dead
    # architecture's. The card's domain appearing in pipeline.json's domain is the cheap signal:
    # it holds on 189 of 191 builds, and both exceptions were slots in exactly this state.
    dom_c = dom_p = ""
    if os.path.exists(card):
        try:
            dom_c = (json.load(open(card)).get("domain") or "").strip()
        except ValueError:
            dom_c = ""
    pj = os.path.join(task_dir, "pipeline.json")
    if os.path.exists(pj):
        try:
            dom_p = (json.load(open(pj)).get("domain") or "").strip()
        except ValueError:
            dom_p = ""
    if dom_c and dom_p:
        row("the registered card is this architecture's", dom_c in dom_p,
            "card domain %r is in pipeline domain %r" % (dom_c, dom_p) if dom_c in dom_p else
            "card domain %r is not in pipeline domain %r, so the card belongs to a dead "
            "architecture and every check below is reading its note, not this one's" % (dom_c, dom_p))
    row("data-native sentence", bool(re.search(r"data[- ]native", note_text, re.I)),
        "named in the note" if re.search(r"data[- ]native", note_text, re.I) else "no data-native sentence found", warn=True)

    # Default path: ends on a wrong answer.
    dp = section(secs, "Default path") or ""
    ends, gold = labelled(dp, "Ends on"), labelled(dp, "Golden")
    row("default path ends on", bool(ends), ends or "no `Ends on:` line")
    row("default path golden", bool(gold), gold or "no `Golden:` line")
    if ends and gold:
        same = norm_number(ends).lower() == norm_number(gold).lower()
        row("default path differs from golden", not same,
            "the default path is not the golden" if not same else "the default path ends on the golden: there is no stump")
    steps = len(re.findall(r"^\s*\d+[.)]\s+\S", dp, re.M))
    row("default path steps", steps >= 2, "%d numbered steps" % steps if steps >= 2 else "fewer than two numbered steps", warn=steps >= 1)

    # Stump sentence names the default path's answer.
    ss = (section(secs, "Stump sentence") or "").strip()
    ss_text = re.sub(r"\s+", " ", ss)
    row("stump sentence", bool(ss_text), ss_text[:140] + ("..." if len(ss_text) > 140 else "") if ss_text else "empty")
    if ss_text and ends:
        row("stump sentence names the default answer", names_value(ss_text, ends),
            "names %r" % ends if names_value(ss_text, ends) else "does not name the default path's answer %r" % ends)

    # Three rules: one labelled line per point of the client's own pre-ship check (stumping 1.1). A build that
    # has shipped meets a missing line as a WARN; a build being designed or repaired is refused.
    tr = section(secs, "Deep reasoning") or section(secs, "Three rules") or ""
    for label in THREE_RULES:
        v = labelled(tr, label)
        ok = bool(v) and len(v) >= 20
        row("deep reasoning: %s" % label, ok, (v or "missing")[:120] if ok else (v or "missing") + " (one line, 20 characters or more)",
            warn=shipped and label not in ("Domain test", "Analyst test", "Layer 1", "Layer 2"))
    # Sulfur's depth bar: three or more dependent inferences, one a statistical or modeling judgment; the runs
    # expected to fail on a deep class; the strategy not one Mark measured dead.
    ch = labelled(tr, "Chain")
    if ch:
        n_inf = len(re.findall(r"\(\d{1,2}\)|(?:^|[\s;,])\d{1,2}[.)]\s", ch))
        row("deep chain has three or more inferences", n_inf >= 3,
            "%d numbered inferences" % n_inf if n_inf >= 3 else
            "%d numbered inference(s) on the Chain line; Sulfur needs three or more dependent ones, numbered (1) (2) (3)"
            % n_inf, warn=shipped)
    an = labelled(tr, "After the notice")
    if an:
        n_after = len(re.findall(r"\(\d{1,2}\)|(?:^|[\s;,])\d{1,2}[.)]\s", an))
        row("two or more inferences owed after the notice", n_after >= 2,
            "%d numbered inferences after the notice" % n_after if n_after >= 2 else
            "%d numbered inference(s) on the After the notice line; a step whose remedy is standard once seen was the "
            "whole stump (stumping 1.1): number (1) (2) the inferences still owed, each with its wrong turn" % n_after,
            warn=shipped)
    rf = labelled(tr, "Run forecast")
    if rf:
        deep = re.search(r"method shortcut|unfinished chain|dismissed (its )?own evidence|self-confirming check", rf, re.I)
        row("run forecast is a deep class", bool(deep),
            "names %s" % deep.group(0) if deep else
            "names no deep class (method shortcut, unfinished chain, dismissed own evidence, self-confirming check)",
            warn=shipped)
    sl = labelled(tr, "Strategy label")
    if sl:
        dead = re.search(r"does not work", sl, re.I)
        row("strategy is not one Mark measured dead", not dead,
            "label: %s" % sl[:80] if not dead else
            "the family is DOES NOT WORK in references/sulfur-strategies.md: redraw, or build it only at rung 0 or 1",
            warn=shipped)

    at = labelled(tr, "Analyst test")
    if at and ends:
        row("analyst test names the default answer", names_value(at, ends),
            "names %r" % ends if names_value(at, ends) else "the analyst test does not name the default path's answer %r" % ends,
            warn=shipped)
    tt = labelled(tr, "Task type")
    if tt:
        ok, detail = task_type_serves(task, tt)
        row("task type serves the objective", ok, detail, warn=shipped or ok is None)

    # The reflex collision: if the field's own named method for the deciding quantity IS the decisive step,
    # the readability screen's test 3 is failed by construction and a competent analyst reaches the golden.
    # Three builds died this way (a domain's reflex estimator, a textbook weight, a test concordance).
    dt, ds = labelled(tr, "Domain test"), labelled(tr, "Decisive step")
    if dt and ds:
        shared = method_terms(dt) & method_terms(ds)
        row("the field's method is not the decisive step", not shared,
            "the Domain test and Decisive step lines share no method term"
            if not shared else
            "both lines name %s: if the field's own method for the deciding quantity is the golden, a competent "
            "analyst applies it by reflex and the screen's test 3 cannot be silent (stumping 1.1b: the field's "
            "method sits at rung 0 or 1 and the decisive step is the precondition this dataset violates)"
            % ", ".join(sorted(shared)), warn=shipped)

    # Survivor anatomy (stumping 1.4): one labelled line per property every approved main call shares. A build
    # that shipped before the section existed meets a missing line as a WARN; a build in design is refused.
    sa = section(secs, "Survivor anatomy") or ""
    for label in ANATOMY:
        v = labelled(sa, label)
        ok = bool(v) and len(v) >= 20
        row("survivor anatomy: %s" % label, ok,
            (v or "missing")[:120] if ok else (v or "missing") + " (one line, 20 characters or more)", warn=shipped)

    # Readability screen.
    rs = section(secs, "Readability screen") or ""
    tbs = [t for t in tables(rs) if len(t) >= 2]
    if not tbs:
        row("readability screen table", False, "no table with a header and at least one rung")
    else:
        t = tbs[0]
        verdicts = [(r[0], r[-1].strip().lower().strip("`*")) for r in t[1:] if r]
        bad = [r for r, v in verdicts if v not in ("silent", "readable")]
        row("readability verdicts", not bad, "every row silent or readable" if not bad else "verdict not silent/readable on: " + ", ".join(bad))
        dec = [(r, v) for r, v in verdicts if "decisive" in r.lower()]
        row("decisive rung marked", bool(dec), "%d rung(s) marked (decisive)" % len(dec) if dec else "no rung marked (decisive)")
        if dec:
            row("decisive rung silent", all(v == "silent" for _, v in dec),
                "the decisive rung is silent" if all(v == "silent" for _, v in dec) else "the decisive rung is readable: it is dead")

    # Semantic fork table.
    sf = section(secs, "Semantic fork table") or ""
    sf_rows = [r for t in tables(sf) for r in t[1:] if r and re.fullmatch(r"SF\d+", r[0].strip("`* "))]
    row("semantic fork rows", bool(sf_rows), "%d rows" % len(sf_rows) if sf_rows else "no SFn rows")
    empty = [r[0] for r in sf_rows if not r[-1].strip() or r[-1].strip() in ("...", "-", "?")]
    row("semantic forks ruled out", not empty, "every alternative ruled out or convergent" if not empty else "empty `Ruled out by` on: " + ", ".join(empty))
    checks = os.path.join(task_dir, "generator", "checks.py")
    if sf_rows and os.path.exists(checks):
        src = open(checks, encoding="utf-8", errors="replace").read()
        want = [r[0].strip("`* ") for r in sf_rows]
        # Whole-token matching: a bare substring test passes SF1 on a file that only carries SF15.
        missing = [i for i in want if not re.search(r"\b%s\b" % re.escape(i), src)]
        # A re-rooted build whose checks.py still belongs to the dead architecture passes every id by
        # coincidence, because the old file carries a longer SF run for entirely different forks. The
        # signature is an SF id asserted in checks.py that the note does not carry.
        asserted = set(re.findall(r"\bSF\d{1,3}\b", src))
        orphans = sorted(asserted - set(want), key=lambda x: int(x[2:]))
        if missing:
            row("semantic forks asserted", False, "not in checks.py: " + ", ".join(missing))
        elif orphans:
            row("semantic forks asserted", False,
                "checks.py asserts %d SF id(s) the fork table does not carry (%s), so it was written for another "
                "architecture and every id above matched by coincidence; this build's forks owe real assertions"
                % (len(orphans), ", ".join(orphans)))
        else:
            row("semantic forks asserted", True, "every SF id appears in generator/checks.py as its own token")
    elif sf_rows:
        ids = ", ".join(r[0].strip("`* ") for r in sf_rows)
        row("semantic forks asserted", False,
            "generator/checks.py not written yet, so this check is not run: %d rows still owe an assertion (%s)"
            % (len(sf_rows), ids), warn=True)

    # Closure table: 22 axes.
    ct = section(secs, "Closure table") or ""
    axes, blank = set(), []
    for t in tables(ct):
        for r in t[1:]:
            m = re.match(r"^\s*(\d{1,2})\b", r[0])
            if m:
                n = int(m.group(1))
                axes.add(n)
                if len(r) < 2 or not r[-1].strip():
                    blank.append(n)
    missing_axes = sorted(AXES - axes)
    row("closure table 22 axes", not missing_axes, "22 of 22 axes" if not missing_axes else "missing axes: " + ", ".join(map(str, missing_axes)))
    row("closure moves filled", not blank, "every axis closed" if not blank else "empty closure on axes: " + ", ".join(map(str, blank)))

    # Literal reader and oracles: present and non-empty.
    for name in ("Literal reader", "Oracles"):
        body = (section(secs, name) or "").strip()
        row("%s written" % name.lower(), bool(body), body.splitlines()[0][:120] if body else "empty")

    # Ask sheet: pair ceiling, mirror leakage and the cracker sheet.
    ask = section(secs, "Ask sheet") or ""
    pc = labelled(ask, "Pair ceiling")
    num = re.search(r"\d+(?:\.\d+)?", pc or "")
    if not num:
        row("pair ceiling", False, "no `Pair ceiling:` figure")
    else:
        v = float(num.group(0))
        row("pair ceiling", v <= PAIR_CEILING, "%.1f (ceiling %.0f)" % (v, PAIR_CEILING))
    ml = labelled(ask, "Shallow keep") or labelled(ask, "Mirror leakage")
    mnum = re.search(r"\d+(?:\.\d+)?", ml or "")
    if not mnum:
        row("shallow keep", False, "no `Shallow keep:` figure (supplemental-stumping Part 7)", warn=True)
    else:
        v = float(mnum.group(0))
        row("shallow keep", v < MIRROR_CEILING, "%.1f per cent of ask weight kept by the default path (under %.0f; the asks must ride the deep step)" % (v, MIRROR_CEILING))
    # The ceiling and the leakage have to come from code run on the cut pack, not from prose.
    # Two builds in one wave shipped a sheet whose figure was the complement or the mirror of the
    # truth (supplemental-stumping Part 7), and this gate reads the sheet, so the sheet has to name
    # the script that produced the numbers.
    mb = labelled(ask, "Measured by")
    script = (mb or "").strip()
    found = ""
    if script:
        for cand in re.findall(r"[\w./-]+\.py", script):
            for base in (os.path.join(task_dir, cand), os.path.join(task_dir, "generator", os.path.basename(cand)), cand):
                if os.path.exists(base):
                    found = base
                    break
            if found:
                break
    row("ceiling measured by a script", bool(found),
        ("%s" % found) if found else
        ("names no existing script: %r" % script if script else
         "no `Measured by:` line naming the script that ran the cracker on the cut pack"))

    cr = [t for t in tables(ask) if any("cracker" in c.lower() for c in t[0])]
    if not cr:
        row("cracker sheet", False, "no table whose header names the cracker")
    else:
        verdict = [(r[0], r[-1].strip().lower().strip("`*")) for t in cr for r in t[1:] if r]
        hits = [a for a, v in verdict if v not in ("miss", "misses", "yes", "outside")]
        # Sulfur: the landed run may keep the coupled asks, but some must carry their own judgment or the pair
        # cannot reach the target (supplemental-stumping Part 0: Lc near 0.65).
        row("the landed run loses some asks", bool(verdict) and len(hits) < len(verdict),
            "%d of %d ask rows missed by the landed run" % (len(verdict) - len(hits), len(verdict)) if verdict and len(hits) < len(verdict)
            else ("the landed run keeps every ask: give asks their own second judgment" if verdict else "(no rows)"))

    return rows

def words_hit(text, table):
    """The keys of `table` whose words appear in `text` (lower-cased, whole-phrase substring)."""
    low = " " + re.sub(r"\s+", " ", (text or "").lower()) + " "
    return [k for k, ws in table.items() if any(w in low for w in ws)]


IN_FLIGHT = ("DRAWING", "DESIGN", "BUILD", "PAUSED", "RETURNED")


def factorial_rows(task_dir, secs):
    """The stump factorial on paper: two or more stumps each necessary, none sufficient alone."""
    try:
        st = json.load(open(os.path.join(task_dir, "pipeline.json"))).get("status") or "DESIGN"
    except Exception:
        st = "DESIGN"
    strict = st in IN_FLIGHT
    rows = []

    def row(check, ok, detail):
        rows.append((check, "PASS" if ok else ("FAIL" if strict else "WARN"), detail))

    sf = section(secs, "Stump factorial")
    row("section Stump factorial", sf is not None, "present" if sf is not None else
        "## Stump factorial missing (stumping Part 3.3: each stump necessary alone, none sufficient alone, on paper "
        "before the generator)")
    if sf is None:
        return rows
    rr = labelled(sf, "Reflex route") or ""
    row("stump factorial: Reflex route", len(rr) >= 20, rr[:110] or "missing")
    t = find_table(sf, "judgment", "kind") or []
    if not t:
        row("stump factorial table", False, "no table with Judgment and Kind columns")
        return rows
    h = t[0]
    ck, cd, ca, ce, cr = (col(h, "kind"), col(h, "dropped"), col(h, "fixed alone", "alone"), col(h, "evidence"),
                          col(h, "routine"))
    if None in (ck, cd, ca, ce):
        row("stump factorial columns", False, "need Kind, Evidence, Dropped alone from the golden, Fixed alone on the reflex route")
        return rows
    try:
        known = {p["id"]: p for p in json.load(open(os.path.join(HERE, "references", "precedents.json")))["precedents"]}
    except Exception:
        known = {}
    data = [r for r in t[1:] if r and len(r) > max(ck, cd, ca, ce)]
    stumps = [r for r in data if re.search(r"\bstump\b", r[ck], re.I)]
    # "same call" (or "no change") means the drop leaves the call; an empty answer ("none go ahead") is a move
    nec = [r for r in stumps if not re.match(r"\s*(same call|no change|the golden)\b", r[cd], re.I)]
    suff = [r for r in stumps if re.search(r"\b(the golden|golden call|rescues the call|same as the golden)\b", r[ca], re.I)]
    badev = []
    for r in stumps:
        ids = re.findall(r"\b([LNR]\d{2})\b", r[ce])
        kinds = {known[i]["kind"] for i in ids if i in known}
        if "reflex" in kinds or not (kinds & {"loss", "named_assumption"}):
            badev.append(r[0][:40])
    row("stump factorial: two or more stumps each move the call when dropped alone", len(nec) >= 2,
        "%d of %d stumps necessary%s" % (len(nec), len(stumps), "" if len(nec) >= 2 else
                                         ": a one-trick design; add an independent judgment that moves the call alone"))
    row("stump factorial: no stump reaches the golden when fixed alone", not suff,
        "none sufficient" if not suff else "sufficient alone: " + "; ".join(r[0][:40] for r in suff))
    row("stump factorial: each stump cites a loss or named assumption, never a reflex", not badev,
        "cited" if not badev else "fix: " + "; ".join(badev))
    if cr is not None:
        routine = [r for r in stumps if len(r) > cr and re.match(r"\s*yes\b", r[cr], re.I)]
        rows.append(("stump factorial: not every stump a routine step once told",
                     "PASS" if len(routine) < len(stumps) or not stumps else "WARN",
                     "%d of %d stumps a routine step once told" % (len(routine), len(stumps))))
    lvl = 5 if len(nec) >= 3 and not suff else 4 if len(nec) >= 2 and not suff else 3
    rows.append(("stump factorial: depth level on paper", "PASS" if lvl == 5 else "WARN" if lvl == 4 else
                 ("FAIL" if strict else "WARN"), "level %d (%d necessary stumps)" % (lvl, len(nec))))
    return rows


def pinning_rows(task_dir, secs):
    """The golden may not know what the generator knows: every constant it shares with the world has a home in a shipped
    file or a measured spread, and the transport was rebuilt across a variant battery that files one answer."""
    try:
        st = json.load(open(os.path.join(task_dir, "pipeline.json"))).get("status") or "DESIGN"
    except Exception:
        st = "DESIGN"
    strict = st in IN_FLIGHT
    rows = []

    def row(check, ok, detail):
        rows.append((check, "PASS" if ok else ("FAIL" if strict else "WARN"), detail))
    pl = section(secs, "Pinning list")
    row("section Pinning list", pl is not None, "present" if pl is not None else
        "## Pinning list missing (determinism-check §1: each constant the golden shares with the world, filed or measured)")
    if pl is None:
        return rows
    t = find_table(pl, "constant", "home") or []
    data = [r for r in t[1:] if r and any(c.strip() for c in r)] if t else []
    row("pinning list table", bool(data), "%d constants" % len(data) if data else "no table with Constant and Home columns")
    if data:
        ch = col(t[0], "home")
        bad = [r[0][:40] for r in data if ch is None or len(r) <= ch or not (
            re.search(r"\.(pdf|xlsx|csv|docx|txt|json)\b", r[ch], re.I) or re.search(r"\bspread\b", r[ch], re.I))]
        row("pinning list: every constant filed in a shipped file or measured", not bad,
            "each has a home" if not bad else "no file or measured spread: " + "; ".join(bad))
    vb = labelled(pl, "Variant battery") or ""
    m = re.search(r"(\d[\d,]*)\s+variants", vb)
    n = int(m.group(1).replace(",", "")) if m else 0
    one = bool(re.search(r"\b(one|1|a single) (answer|set|call)\b|\bsame (call|answer|set)\b|\bevery variant\b", vb, re.I))
    row("pinning list: Variant battery run and files one answer", n >= 12 and one,
        vb[:110] if vb else "no `Variant battery:` line (twelve or more variants of every modelled transport, one answer)")
    return rows


def open_members_rows(task_dir, secs):
    """A call is only as hard as the members a run can get wrong: two or more open members (the reflex route or the
    direct route files them wrong and a stump brings them back), each opened by a different stump, and the direct route
    written (SKILL.md Part 3.4). FAIL on a build in flight registered from OPEN_FROM, WARN otherwise."""
    try:
        st = json.load(open(os.path.join(task_dir, "pipeline.json"))).get("status") or "DESIGN"
    except Exception:
        st = "DESIGN"
    try:
        reg = json.load(open(os.path.join(CARDS, os.path.basename(task_dir) + ".json"))).get("registered") or ""
    except Exception:
        reg = ""
    strict = st in IN_FLIGHT and (not reg or reg >= OPEN_FROM)
    rows = []

    def row(check, ok, detail):
        rows.append((check, "PASS" if ok else ("FAIL" if strict else "WARN"), detail))
    om = section(secs, "Open members")
    row("section Open members", om is not None, "present" if om is not None else
        "## Open members missing (SKILL.md Part 3.4: count the members a run can get wrong, not the stumps)")
    if om is None:
        return rows
    t = find_table(om, "member", "opened") or []
    data = [r for r in t[1:] if r and any(c.strip() for c in r)] if t else []
    co = col(t[0], "opened") if t else None
    cr, cd = (col(t[0], "reflex"), col(t[0], "direct")) if t else (None, None)
    opened = []
    for r in data:
        by = r[co].strip().lower() if co is not None and len(r) > co else ""
        right = [r[c].strip().lower() for c in (cr, cd) if c is not None and len(r) > c]
        if by and not by.startswith("forced") and not all(re.match(r"(right|same|golden)\b", x) for x in right if x):
            opened.append(re.split(r"[ ,;(]", by)[0])
    row("open members: two or more, each opened by a different stump", len(set(opened)) >= 2,
        "%d open of %d members, opened by %s" % (len(opened), len(data), ", ".join(sorted(set(opened))) or "none"))
    # each opener is a stump of the factorial (whose evidence effort.py holds to a loss or a named assumption), never a
    # judgment the factorial or the run record calls a reflex
    fs = section(secs, "Stump factorial")
    ft = find_table(fs, "judgment", "kind") if fs else None
    stumps = set()
    if ft:
        ck = col(ft[0], "kind")
        for r in ft[1:]:
            if r and ck is not None and len(r) > ck and r[ck].strip().lower().startswith("stump"):
                stumps.add(re.split(r"[ ,;(]", r[0].strip().lower())[0])
    bad = sorted(set(o for o in opened if o not in stumps))
    if opened:
        row("open members: each opened by a stump of the factorial", not bad and bool(ft),
            "openers %s are stumps of the factorial" % ", ".join(sorted(set(opened))) if not bad and ft else
            "not a stump in ## Stump factorial: %s" % (", ".join(bad) if bad else "no factorial table"))
    dr = labelled(om, "Direct route") or ""
    row("open members: the direct route written", len(dr) > 40, dr[:110] if dr else
        "no `Direct route:` line (the pack's most direct evidence read raw, per member, and what it files)")
    return rows


def col(header, *names):
    """Index of the first header cell containing any of `names` (case-insensitive), else None."""
    for i, h in enumerate(header):
        low = h.lower()
        if any(n in low for n in names):
            return i
    return None


def find_table(body, *must):
    """The first table in `body` whose header row carries every word in `must`."""
    for t in tables(body):
        head = " ".join(t[0]).lower()
        if all(m in head for m in must):
            return t
    return None


def results_chain(body):
    """Parse the Results chain table into dicts. Returns (rows, problem) with problem a string or None."""
    t = find_table(body, "result", "area")
    if not t or len(t) < 2:
        return [], "no table whose header names Result and Area"
    h = t[0]
    idx = {k: col(h, *names) for k, names in (
        ("result", ("result",)), ("area", ("area",)), ("pinned", ("pinned", "pin")), ("band", ("band",)),
        ("hurried", ("hurried",)), ("depends", ("depends", "depend")), ("graded", ("graded", "block")))}
    missing = [k for k, v in idx.items() if v is None]
    if missing:
        return [], "the table's header lacks a column for: " + ", ".join(missing)
    out = []
    for r in t[1:]:
        if not r or not r[0].strip():
            continue
        get = lambda k: r[idx[k]].strip() if idx[k] < len(r) else ""
        rid = re.sub(r"[`*]", "", r[0]).strip()
        out.append({"id": rid, "result": get("result"), "area": get("area"), "pinned": get("pinned"),
                    "band": get("band"), "hurried": get("hurried"), "depends": get("depends"),
                    "graded": get("graded")})
    return out, None


def hidden_factors(body):
    t = find_table(body, "factor")
    if not t or len(t) < 2:
        return None
    h = t[0]
    i_real = col(h, "real", "constructed")
    i_only = col(h, "only", "deciding")
    i_found = col(h, "found")
    i_fix = col(h, "fix")
    out = []
    for r in t[1:]:
        if not r or not r[0].strip():
            continue
        cell = lambda i: (r[i].lower() if i is not None and i < len(r) else "")
        real = cell(i_real)
        constructed = bool(re.search(r"construct|generat|simulat|author|planted|added", real)) and not \
            re.match(r"\s*(real|public)\b", real)
        only = cell(i_only)
        only_deciding = bool(re.match(r"\s*(yes|only)\b", only))
        found = cell(i_found)
        one_look = bool(re.search(r"one look|one cross-tab|one crosstab|one plot|one group-by|single cross-tab|"
                                  r"single plot|glance", found))
        fix = cell(i_fix)
        routine = bool(re.search(r"routine|one filter|one stratification|one reweight|one extra term|drop", fix)) \
            and not re.search(r"model+ing|judg", fix)
        out.append({"factor": r[0].strip(), "constructed": constructed, "only_deciding": only_deciding,
                    "one_look": one_look, "routine": routine, "cols_ok": None not in (i_real, i_only, i_found, i_fix)})
    return out


def effort_table(body):
    t = find_table(body, "quick", "thorough")
    if not t or len(t) < 2:
        return None, "no table whose header names Quick and Thorough"
    h = t[0]
    iq, ic, it = col(h, "quick"), col(h, "careful", "hurried"), col(h, "thorough")
    if ic is None:
        return None, "the effort table has no Careful but hurried column"
    rows = []
    for r in t[1:]:
        if not r or re.match(r"\s*(roughly|total|score)", r[0], re.I):
            continue
        def grade(i):
            c = (r[i] if i < len(r) else "").strip().lower().strip("`*")
            m = re.match(r"(right|partly|missed)", c)
            return m.group(1) if m else None
        rows.append({"result": re.sub(r"[`*]", "", r[0]).strip(), "quick": grade(iq), "careful": grade(ic),
                     "thorough": grade(it)})
    return rows, None


def other_chains(task_dir):
    """(task, chain signature, answer shape keys, weight keys, question form) for every other build whose note
    carries a Results chain."""
    out = []
    for note in sorted(glob.glob(os.path.join(REPO, "task*", "DESIGN_NOTE.md"))):
        tdir = os.path.dirname(note)
        if os.path.abspath(tdir) == os.path.abspath(task_dir):
            continue
        try:
            secs = sections(open(note, encoding="utf-8", errors="replace").read())
        except OSError:
            continue
        rc = section(secs, "Results chain")
        if rc is None:
            continue
        rows, _ = results_chain(rc)
        sig = tuple((words_hit(r["area"], AREA_WORDS) or ["?"])[0] for r in rows)
        draw = section(secs, "Draw") or ""
        tc = section(secs, "Template check") or ""
        out.append((os.path.basename(tdir), sig, set(words_hit(labelled(draw, "Answer shape") or "", SHAPE_WORDS)),
                    set(words_hit(labelled(draw, "Weight") or "", WEIGHT_WORDS)),
                    (labelled(tc, "Question form") or "").lower()))
    return out


def card_objective(task):
    try:
        return json.load(open(os.path.join(CARDS, task + ".json"))).get("objective") or ""
    except Exception:
        return ""


def check_throughout(task_dir, note_text, secs, dupes):
    rows = []
    task = os.path.basename(task_dir)

    def row(check, ok, detail, warn=False):
        rows.append((check, "PASS" if ok else ("WARN" if warn else "FAIL"), detail))

    row("no repeated H2 heading", not dupes,
        "each H2 appears once" if not dupes else
        "repeated, so the earlier copy is unread and unchecked: %s" % ", ".join(sorted(set(dupes))))
    for name in NEW_REQUIRED:
        present = section(secs, name) is not None
        row("section %s" % name, present, "## %s present" % name if present else "## %s missing" % name)
    stale = [n for n in RETIRED_SECTIONS if section(secs, n) is not None]
    row("no retired section left in the note", not stale,
        "none" if not stale else "retired under the results chain, delete so no reader takes it for the design: "
        + ", ".join(stale), warn=True)

    card = os.path.join(CARDS, task + ".json")
    row("card registered", os.path.exists(card), card if os.path.exists(card) else "no card under fingerprint/cards/")
    row("data-native sentence", bool(re.search(r"data[- ]native", note_text, re.I)),
        "named in the note" if re.search(r"data[- ]native", note_text, re.I) else "no data-native sentence found",
        warn=True)

    # Draw: the analysis type, the answer shape and where the weight sits, each one of the client's own lists.
    draw = section(secs, "Draw") or ""
    at, shp, wt = (labelled(draw, x) for x in DRAW_LABELS)
    at_k, shp_k, wt_k = words_hit(at, TYPE_WORDS), words_hit(shp, SHAPE_WORDS), words_hit(wt, WEIGHT_WORDS)
    row("draw: analysis type", bool(at_k), ("%s" % ", ".join(at_k)) if at_k else
        "%r names none of the nine analysis types (vocab.json objectives)" % (at or "missing"))
    obj = card_objective(task)
    if at_k and obj:
        row("analysis type agrees with the card", obj in at_k,
            "card objective %s" % obj if obj in at_k else "card objective %s, note %s" % (obj, ", ".join(at_k)),
            warn=True)
    row("draw: answer shape", bool(shp_k), ", ".join(shp_k) if shp_k else
        "%r names none of the fourteen answer shapes (vocab.json answer_shapes)" % (shp or "missing"))
    row("draw: where the weight sits", bool(wt_k), ", ".join(wt_k) if wt_k else
        "%r names none of the eleven weights (vocab.json weights)" % (wt or "missing"))

    # Deep reasoning: one labelled line per point.
    dr = section(secs, "Deep reasoning") or ""
    for label in DEEP_LABELS:
        v = labelled(dr, label)
        ok = bool(v) and len(v) >= 20
        row("deep reasoning: %s" % label, ok, (v or "missing")[:110] if ok else
            (v or "missing") + " (one line, 20 characters or more)")
    tt = labelled(dr, "Task type")
    if tt:
        ok, detail = task_type_serves(task, tt)
        row("task type serves the objective", ok, detail, warn=ok is None)
    dl = labelled(dr, "Depth level")
    lvl = re.match(r"\s*([1-5])\b", dl or "")
    n_ = int(lvl.group(1)) if lvl else 0
    row("depth level 4 or 5", n_ >= 4, ("level %d (guidelines/client/depth-scale-2026-11-09.md)" % n_) if n_ else
        "no Depth level line opening with a level from 1 to 5 (the client's depth scale; aim at 4 or 5)",
        warn=not dl or n_ == 3)
    sl = labelled(dr, "Strategy label")
    if sl:
        dead = re.search(r"does not work", sl, re.I)
        row("strategy is not one measured dead", not dead, "label: %s" % sl[:80] if not dead else
            "the strategy is DOES NOT WORK in references/sulfur-strategies.md: redraw")

    # Results chain.
    rc = section(secs, "Results chain") or ""
    res, problem = results_chain(rc)
    row("results chain table", not problem and bool(res), "%d results" % len(res) if not problem else problem)
    ids = [r["id"] for r in res]
    if res:
        row("four or more checkable results", len(res) >= MIN_RESULTS,
            "%d results" % len(res) if len(res) >= MIN_RESULTS else
            "%d results; the client asks for several pieces of genuine analysis, each ending in a checkable result"
            % len(res))
        areas = []
        bad_area = []
        for r in res:
            k = words_hit(r["area"], AREA_WORDS)
            if not k:
                bad_area.append(r["id"])
            areas.append(k[0] if k else "?")
        row("every result names one of the fourteen areas", not bad_area,
            "every row" if not bad_area else "no area recognised on: " + ", ".join(bad_area))
        distinct = sorted(set(a for a in areas if a != "?"))
        row("results span three or more areas", len(distinct) >= MIN_AREAS,
            "%d areas: %s" % (len(distinct), ", ".join(distinct)))
        unbanded = [r["id"] for r in res if len(r["band"]) < 2 or r["band"] in ("-", "?", "...")]
        row("every result has a band", not unbanded,
            "every row" if not unbanded else "no band (exact, or the range reasonable methods span) on: "
            + ", ".join(unbanded))
        unpinned = [r["id"] for r in res if len(r["pinned"]) < 6]
        row("every result is pinned", not unpinned,
            "every row" if not unpinned else "no pin (the data or a stated convention) on: " + ", ".join(unpinned))
        classes, no_class, surface = [], [], []
        for r in res:
            hit = [k for k, pat in DEEP_CLASSES.items() if re.search(pat, r["hurried"], re.I)]
            if not hit:
                no_class.append(r["id"])
            classes += hit
            if re.search(SURFACE_CLASSES, r["hurried"], re.I):
                surface.append(r["id"])
        row("every hurried failure is a deep class", not no_class,
            "every row" if not no_class else
            "names none of method shortcut, unfinished chain, first story, narrow look, dismissed own evidence, "
            "self-confirming check on: " + ", ".join(no_class))
        row("no hurried failure is a surface class", not surface,
            "none" if not surface else "a result lost to a plant, a reading or a procedure is a surface stump: "
            + ", ".join(surface))
        row("losses spread across two or more kinds", len(set(classes)) >= 2,
            "%d kinds: %s" % (len(set(classes)), ", ".join(sorted(set(classes)))), warn=True)
        # Dependencies: earlier results only.
        bad_dep, deps = [], {}
        for i, r in enumerate(res):
            d = re.findall(r"\b([A-Z]{1,2}\d{1,2}[a-z]?)\b", r["depends"])
            deps[r["id"]] = d
            if any(x not in ids[:i] for x in d):
                bad_dep.append(r["id"])
        row("dependencies point at earlier results", not bad_dep,
            "every row" if not bad_dep else "a dependency that is not an earlier result on: " + ", ".join(bad_dep))
        # A result most others hang on is the one-thing flip carried inside the chain: the platform grades every
        # figure against the golden, so a later result built on a wrong earlier figure is wrong unless it can be
        # graded on an input of its own (a Depends on cell saying "independent: <input>"). What makes a result one
        # thing is being the ONLY analytical result standing between a run and the later ones: where a later result
        # needs two analytical results (an AND), catching either alone carries nothing. So the count, for each
        # analytical result X, is of the results whose analytical ancestors are X alone. Foundation rows (assembly,
        # discovery, framing) feed everything by nature and are left out of the ancestor sets.
        foundation = {"assembly-reconciliation", "data-discovery", "framing"}
        area_of = dict(zip(ids, areas))
        indep = {r["id"] for r in res if re.search(r"independent\s*:?\s*\S.{8,}", r["depends"], re.I)}
        def ancestors(x, seen=None):
            seen = set() if seen is None else seen
            if x in indep:
                return seen
            for p_ in deps.get(x, []):
                if p_ not in seen:
                    seen.add(p_)
                    ancestors(p_, seen)
            return seen
        hubs = [x for x in ids if area_of.get(x) not in foundation]
        if hubs:
            sole = {x: [y for y in ids if y != x and
                        {a for a in ancestors(y) if area_of.get(a) not in foundation} == {x}] for x in hubs}
            hub = max(hubs, key=lambda x: len(sole[x]))
            nd = len(sole[hub])
            ok = nd <= (len(res) - 1) / 2.0
            row("no result carries most of the others", ok,
                "the widest analytical result, %s, is the only analytical input of %d of the other %d" % (hub, nd, len(res) - 1)
                if ok else
                "%s is the only analytical result behind %d of the other %d (%s): a run that misses it loses them all, "
                "which is one thing under another name; give later results a second analytical input or an input of "
                "their own (Depends on: \"independent: <input>\")" % (hub, nd, len(res) - 1, ", ".join(sole[hub])))
            # A linear chain passes the count above when every link is called analytical; it is kept visible here, and
            # the binding test is effort.py's largest single hint on the generator's own hurried passes.
            reach = {x: [y for y in ids if y != x and x in ancestors(y)] for x in hubs}
            wide = max(hubs, key=lambda x: len(reach[x]))
            if len(reach[wide]) > (len(res) - 1) / 2.0:
                row("results downstream of one analytical result", False,
                    "%s sits upstream of %d of the other %d (%s): make sure each of them needs work of its own, or the "
                    "largest single hint will show it" % (wide, len(reach[wide]), len(res) - 1, ", ".join(reach[wide])),
                    warn=True)
        # The careful column is calibrated to the run record: frontier runs hold out, bootstrap, run the field's
        # textbook method and model any pattern one plot shows without being asked (task7 arch 5 held out 122
        # pairs and bootstrapped). A hurried failure that is only one of those moves is not a loss the runs make.
        unmade = [r["id"] for r in res if re.search(r"in-sample|no hold-?out|without a hold-?out|no back-?test|"
                                                     r"without a back-?test|no bootstrap|never plots|misses the plot|"
                                                     r"does not plot|no cross-validation", r["hurried"], re.I)]
        row("hurried failures are ones the runs make", not unmade,
            "every row names a move beyond a holdout, a bootstrap, a plot or the textbook method" if not unmade else
            "runs hold out, back-test, bootstrap and plot unprompted, so these score Right in the careful column; "
            "name the move beyond that the result needs: " + ", ".join(unmade))
        cf = labelled(rc, "Carry-forward")
        row("carry-forward stated", bool(cf) and len(cf) >= 20, (cf or "missing")[:110] if cf else
            "no `Carry-forward:` line: which later results are graded on an input of their own, and which "
            "fall with an earlier one (the grader compares every figure to the golden)")
        graded = [r["graded"].lower() for r in res]
        nogr = [r["id"] for r in res if not r["graded"]]
        row("every result graded in an answer block", not nogr,
            "every row" if not nogr else "no answer block on: " + ", ".join(nogr))
        comp = sum(1 for g in graded if "component" in g)
        row("critical components among the results", comp >= 2,
            "%d results graded as critical components" % comp if comp >= 2 else
            "%d result(s) graded as a critical component; the components carry the most rubric weight" % comp)

    # Hidden factor record: the client's three conditions, plus the factor built only where it decides.
    hf = section(secs, "Hidden factor record") or ""
    nohf = labelled(hf, "No hidden factor")
    fac = hidden_factors(hf)
    if fac is None and not (nohf and len(nohf) >= 20):
        row("hidden factor record", False, "no table whose header names Factor, and no `No hidden factor:` line")
    elif fac is not None:
        cols_bad = [f["factor"] for f in fac if not f["cols_ok"]]
        row("hidden factor columns", not cols_bad, "real or constructed, only in deciding units, found by, fix depth"
            if not cols_bad else "the header lacks one of: real or constructed, only in deciding units, found by, fix")
        planted = [f["factor"] for f in fac if f["constructed"] and f["only_deciding"]]
        row("no constructed factor only in the deciding units", not planted,
            "none" if not planted else "built only where it decides, so it is planted whatever the fix (a real "
            "process would put it across the data): " + "; ".join(planted))
        shallow = [f["factor"] for f in fac if f["constructed"] and f["one_look"] and f["routine"]]
        row("no shallow hidden factor", not shallow,
            "none" if not shallow else "constructed, found in one look, fixed by one routine step (send-back): "
            + "; ".join(shallow))
        thin = [f["factor"] for f in fac if f["constructed"] and f["routine"] and f["factor"] not in shallow]
        row("constructed factors need modelling to fix", not thin,
            "none" if not thin else "constructed and fixed by a routine step, so it must be one of several pieces "
            "and never the one the call turns on: " + "; ".join(thin), warn=True)

    # Effort test.
    ef = section(secs, "Effort test") or ""
    er, problem = effort_table(ef)
    if problem:
        row("effort test table", False, problem)
    else:
        n = len(er)
        ungraded = [r["result"] for r in er if None in (r["quick"], r["careful"], r["thorough"])]
        row("every pass graded Right, Partly or Missed", not ungraded,
            "every row" if not ungraded else "ungraded cells on: " + ", ".join(ungraded))
        if res:
            row("the effort test prices every result", n == len(res),
                "%d of %d results" % (n, len(res)))
        sc = {p: sum(PASS_SCORE.get(r[p] or "missed", 0) for r in er) for p in ("quick", "careful", "thorough")}
        row("the thorough pass earns every result", sc["thorough"] == n,
            "%g of %d" % (sc["thorough"], n) if sc["thorough"] == n else
            "%g of %d: a result the thorough pass cannot earn is not pinned" % (sc["thorough"], n))
        row("the quick pass earns a third or less", sc["quick"] <= n / 3.0,
            "%g of %d" % (sc["quick"], n), warn=sc["quick"] <= n / 2.0)
        between = sc["quick"] < sc["careful"] < sc["thorough"]
        row("more care earns more", between,
            "quick %g < careful but hurried %g < thorough %g" % (sc["quick"], sc["careful"], sc["thorough"])
            if between else "quick %g, careful but hurried %g, thorough %g: each pass must earn strictly more "
            "than the last (the effort test)" % (sc["quick"], sc["careful"], sc["thorough"]))
    lh = labelled(ef, "Largest single hint") or ""
    m = re.search(r"(\d+)\s+of\s+(\d+)", lh)
    if not m:
        row("largest single hint", False, "no `Largest single hint:` line stating it rescues N of M results")
    else:
        k, mm = int(m.group(1)), int(m.group(2))
        row("largest single hint rescues a third or less", k <= mm / 3.0,
            "rescues %d of %d" % (k, mm) if k <= mm / 3.0 else
            "rescues %d of %d: one sentence moves too much of the score (the one-fact test)" % (k, mm),
            warn=k <= mm / 2.0)
    pe = labelled(ef, "Pair estimate") or ""
    pn = re.search(r"\d+(?:\.\d+)?", pe)
    row("pair estimate", bool(pn) and float(pn.group(0)) <= PAIR_TARGET,
        ("%s (target %.0f, bar 60)" % (pn.group(0), PAIR_TARGET)) if pn else "no `Pair estimate:` figure")
    mb = labelled(ef, "Measured by") or ""
    named = [c for c in re.findall(r"[\w./-]+\.(?:py|json)", mb)]
    row("effort measured by a script", bool(named), ", ".join(named) if named else
        "no `Measured by:` line naming effort.py and generator/effort.json")

    # Data provenance.
    dp = section(secs, "Data provenance") or ""
    src = labelled(dp, "Source") or ""
    generated = bool(re.search(r"generat|simulat|synthetic", src, re.I))
    public = bool(re.search(r"public|open data|portal|https?://|licen[cs]e", src, re.I))
    row("data source stated", generated or public,
        src[:110] if (generated or public) else "`Source:` says neither generated nor public")
    if generated:
        for label in ("Behaves like the real thing", "Genuine patterns", "Problems by process"):
            v = labelled(dp, label)
            row("generated data: %s" % label, bool(v) and len(v) >= 30, (v or "missing")[:110])
        gp = labelled(dp, "Genuine patterns") or ""
        n_pat = len(re.findall(r"\(\d{1,2}\)", gp)) or len([x for x in re.split(r";", gp) if x.strip()])
        row("three or more genuine patterns", n_pat >= 3,
            "%d patterns" % n_pat if n_pat >= 3 else
            "%d pattern(s): generated data has to behave like the real thing throughout, with many genuine "
            "patterns and noise, not one effect added for the solver to find" % n_pat)
    if public:
        for label in ("License", "Used as is"):
            v = labelled(dp, label)
            row("public data: %s" % label, bool(v) and len(v) >= 10, (v or "missing")[:110])
    br = labelled(dp, "Breadth")
    row("breadth stated", bool(br) and len(br) >= 20, (br or "missing")[:110], warn=True)

    # Template check: the same chain of areas in the same order with the same answer shape is a template.
    tc = section(secs, "Template check") or ""
    for label in TEMPLATE_LABELS:
        v = labelled(tc, label)
        row("template check: %s" % label, bool(v) and len(v) >= 10, (v or "missing")[:110])
    if res:
        sig = tuple(areas)
        twins, near = [], []
        qf = (labelled(tc, "Question form") or "").lower()
        for t_name, t_sig, t_shape, t_weight, t_qf in other_chains(task_dir):
            if t_sig == sig and (t_shape & set(shp_k)):
                twins.append(t_name)
            elif t_sig == sig or ((t_shape & set(shp_k)) and (t_weight & set(wt_k))):
                near.append(t_name)
        row("not a template of a build on file", not twins,
            "no build shares the chain and the shape" if not twins else
            "same chain of areas in the same order and the same answer shape as %s: a template, even on new data"
            % ", ".join(twins))
        if near:
            row("nearest chains", False, "shares the chain, or the shape and the weight, with %s: vary where the "
                "weight sits" % ", ".join(near), warn=True)

    # The next-level contract: frontier precedents, the shallow path's own checks, forcing, the skeleton screen.
    rows += frontier_rows(task_dir, secs)
    # Kept from the earlier contract: forks asserted, the closure table, the literal reader.
    rows += forks_closure_literal(task_dir, secs)
    return rows


def forks_closure_literal(task_dir, secs):
    rows = []

    def row(check, ok, detail, warn=False):
        rows.append((check, "PASS" if ok else ("WARN" if warn else "FAIL"), detail))

    sf = section(secs, "Semantic fork table") or ""
    sf_rows = [r for t in tables(sf) for r in t[1:] if r and re.fullmatch(r"SF\d+", r[0].strip("`* "))]
    row("semantic fork rows", bool(sf_rows), "%d rows" % len(sf_rows) if sf_rows else "no SFn rows")
    empty = [r[0] for r in sf_rows if not r[-1].strip() or r[-1].strip() in ("...", "-", "?")]
    row("semantic forks ruled out", not empty,
        "every alternative ruled out or convergent" if not empty else "empty `Ruled out by` on: " + ", ".join(empty))
    checks = os.path.join(task_dir, "generator", "checks.py")
    if sf_rows and os.path.exists(checks):
        src = open(checks, encoding="utf-8", errors="replace").read()
        want = [r[0].strip("`* ") for r in sf_rows]
        missing = [i for i in want if not re.search(r"\b%s\b" % re.escape(i), src)]
        asserted = set(re.findall(r"\bSF\d{1,3}\b", src))
        orphans = sorted(asserted - set(want), key=lambda x: int(x[2:]))
        if missing:
            row("semantic forks asserted", False, "not in checks.py: " + ", ".join(missing))
        elif orphans:
            row("semantic forks asserted", False,
                "checks.py asserts %d SF id(s) the fork table does not carry (%s): written for another architecture"
                % (len(orphans), ", ".join(orphans)))
        else:
            row("semantic forks asserted", True, "every SF id appears in generator/checks.py as its own token")
    elif sf_rows:
        row("semantic forks asserted", False, "generator/checks.py not written yet: %d rows still owe an assertion"
            % len(sf_rows), warn=True)
    ct = section(secs, "Closure table") or ""
    axes, blank = set(), []
    for t in tables(ct):
        for r in t[1:]:
            m = re.match(r"^\s*(\d{1,2})\b", r[0])
            if m:
                axes.add(int(m.group(1)))
                if len(r) < 2 or not r[-1].strip():
                    blank.append(int(m.group(1)))
    missing_axes = sorted(AXES - axes)
    row("closure table 22 axes", not missing_axes,
        "22 of 22 axes" if not missing_axes else "missing axes: " + ", ".join(map(str, missing_axes)))
    row("closure moves filled", not blank, "every axis closed" if not blank else
        "empty closure on axes: " + ", ".join(map(str, blank)))
    body = (section(secs, "Literal reader") or "").strip()
    row("literal reader written", bool(body), body.splitlines()[0][:120] if body else "empty")
    return rows


def effort_gate(task_dir):
    """effort.py on generator/effort.json, once the generator writes it (stage 3 on)."""
    ej = os.path.join(task_dir, "generator", "effort.json")
    if not os.path.exists(ej):
        return ("effort measured on the cut pack", "WARN",
                "generator/effort.json not written yet: the Effort test is paper until stage 3 measures it")
    if not os.path.exists(EFFORT):
        return ("effort measured on the cut pack", "FAIL", "effort.py not found at %s" % EFFORT)
    r = subprocess.run([sys.executable, EFFORT, task_dir, "--check-note"], capture_output=True, text=True)
    tail = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith(("FAIL", "WARN"))]
    if r.returncode == 0:
        return ("effort measured on the cut pack", "PASS", "effort.py exit 0" + ("; " + "; ".join(tail) if tail else ""))
    return ("effort measured on the cut pack", "FAIL", "effort.py exit %d: " % r.returncode + "; ".join(tail)[:400])


def next_level(task_dir):
    """True when the card was registered from skeleton.RULE_FROM on, or no card is registered yet."""
    sys.path.insert(0, FINGERPRINT)
    import skeleton as SK
    try:
        reg = json.load(open(os.path.join(CARDS, os.path.basename(task_dir) + ".json"))).get("registered") or ""
    except Exception:
        return True
    return not reg or reg >= SK.RULE_FROM


def closed_level(task_dir):
    """True when the card was registered from skeleton.CLOSED_FROM on, or no card is registered yet."""
    sys.path.insert(0, FINGERPRINT)
    import skeleton as SK
    try:
        reg = json.load(open(os.path.join(CARDS, os.path.basename(task_dir) + ".json"))).get("registered") or ""
    except Exception:
        return True
    return not reg or reg >= SK.CLOSED_FROM


def screen_level(task_dir):
    """True when the card was registered from SCREEN_FROM on, or no card is registered yet."""
    try:
        reg = json.load(open(os.path.join(CARDS, os.path.basename(task_dir) + ".json"))).get("registered") or ""
    except Exception:
        return True
    return not reg or reg >= SCREEN_FROM


def screen_rows(task_dir, secs):
    """The stump screen (references/stump-screen.md): three or more candidates on paper, three kept."""
    sl = screen_level(task_dir)
    sc = section(secs, "Stump screen")
    rows = []
    t = find_table(sc or "", "kept") or find_table(sc or "", "candidate") or []
    data = [r for r in t[1:] if r and any(c.strip() for c in r)] if t else []
    kept = [r for r in data if re.search(r"\bkept\b", " ".join(r), re.I) and not re.search(r"\bnot kept\b", " ".join(r), re.I)]
    ok = sc is not None and len(data) >= 3 and len(kept) >= 3
    detail = ("%d candidates, %d kept" % (len(data), len(kept))) if sc is not None else \
        "## Stump screen missing (stumping references/stump-screen.md: three to five candidates through the eleven tests)"
    rows.append(("stump screen on paper", "PASS" if ok else ("FAIL" if sl else "WARN"),
                 detail + ("" if sl else ", registered before the stump screen")))
    return rows


def frontier_rows(task_dir, secs):
    """The next-level contract: the Frontier check section and the card's skeleton screen."""
    rows = screen_rows(task_dir, secs)
    nl = next_level(task_dir)
    cl = closed_level(task_dir)

    def row(check, ok, detail):
        rows.append((check, "PASS" if ok else ("FAIL" if nl else "WARN"), detail))

    fc = section(secs, "Frontier check")
    row("section Frontier check", fc is not None, "## Frontier check present" if fc is not None else
        "## Frontier check missing (stumping Part 1b)%s" % ("" if nl else ", registered before the next-level rule"))
    for label in FRONTIER_LABELS:
        v = labelled(fc or "", label)
        row("frontier check: %s" % label, bool(v) and len(v) >= 20, (v or "missing")[:110])
    v = labelled(fc or "", CLOSED_LABEL)
    ok = bool(v) and len(v) >= 20
    rows.append(("frontier check: %s" % CLOSED_LABEL, "PASS" if ok else ("FAIL" if cl else "WARN"),
                 (v or "missing (stumping Part 1c: the deciding lesson off the client's closed list, closed lessons "
                  "only as supporting steps)%s" % ("" if cl else ", registered before the closed strategies"))[:110]))
    pv = labelled(fc or "", "Precedents") or ""
    if pv:
        ids = set(re.findall(r"\b([LNR]\d{2})\b", pv))
        try:
            known = {p["id"]: p for p in json.load(open(os.path.join(HERE, "references", "precedents.json")))["precedents"]}
        except Exception:
            known = {}
        bad = sorted(i for i in ids if i not in known)
        refl = sorted(i for i in ids if i in known and known[i]["kind"] == "reflex")
        row("precedent ids resolve", ids and not bad and not refl,
            "%d ids, every one a loss or named assumption" % len(ids) if ids and not bad and not refl else
            "unknown %s, reflexes cited as losses %s" % (bad or "none", refl or "none") if ids else
            "no precedents.json id named")
    sys.path.insert(0, FINGERPRINT)
    try:
        import skeleton as SK
        cards = SK.load_cards()
        task = os.path.basename(task_dir)
        card = next((c for c in cards if c.get("task") == task), None)
        if card is None:
            row("skeleton screen", False, "no card under fingerprint/cards/")
        else:
            fs = SK.findings(card, cards)
            blocks = [f for f in fs if f["level"] == "BLOCK"]
            warns = [f for f in fs if f["level"] == "WARN"]
            row("skeleton screen (the client's duplicate test)", not blocks,
                ("clear, %d WARN" % len(warns)) if not blocks else "; ".join("%s: %s" % (f["rule"], f["msg"][:120])
                                                                            for f in blocks[:3]))
    except Exception as e:
        row("skeleton screen", False, "did not run: %s" % e)
    return rows


def doctrine(task_dir, secs):
    """'throughout' for the results-chain contract, 'retired' for a build cut under the single deep step."""
    try:
        pj = json.load(open(os.path.join(task_dir, "pipeline.json")))
    except Exception:
        pj = {}
    if pj.get("doctrine") == "throughout" or section(secs, "Results chain") is not None:
        return "throughout"
    return "retired" if (pj.get("status") or "") in SHIPPED_STATES else "throughout"


def check_note(task_dir, note_text):
    dupes = []
    secs = sections(note_text, dupes)
    if doctrine(task_dir, secs) == "throughout":
        return check_throughout(task_dir, note_text, secs, dupes)
    rows = [("doctrine", "WARN", "designed around one deep step on a constructed world, which the client returns "
             "since 2026-11-09 (guidelines/client/deep-reasoning.md); checked on its old contract, and re-rooted to "
             "the results chain before any re-ship")]
    return rows + check_retired(task_dir, note_text, secs, dupes)


def prompt_gate(task_dir):
    """The prompt gate on <task>/prompt.txt, run through voice-check.py with the task's card for the personas."""
    if not os.path.exists(VOICE):
        return ("prompt gate", "WARN", "voice-check.py not found at %s" % VOICE)
    prompt = os.path.join(task_dir, "prompt.txt")
    if not os.path.exists(prompt):
        legacy = os.path.exists(os.path.join(task_dir, "prompt.md"))
        return ("prompt gate", "FAIL", "no prompt.txt" + (" (a prompt.md is a build from before the rule)" if legacy else ""))
    r = subprocess.run([sys.executable, VOICE, "--file", prompt, "--task", os.path.basename(task_dir)],
                       capture_output=True, text=True)
    tail = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith(("FAIL", "WARN"))]
    if r.returncode == 0:
        return ("prompt gate", "PASS", "voice-check.py exit 0" + ("; " + "; ".join(tail) if tail else ""))
    return ("prompt gate", "FAIL", "voice-check.py exit %d: " % r.returncode + "; ".join(tail)[:400])


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    quiet = "--quiet" in argv
    if not args:
        print(__doc__)
        return 2
    task_dir = resolve(args[0])
    note = os.path.join(task_dir, "DESIGN_NOTE.md")
    if not os.path.isdir(task_dir):
        print("no task folder at %s" % task_dir)
        return 2
    if not os.path.exists(note):
        print("no DESIGN_NOTE.md in %s" % task_dir)
        return 2
    rows = check_note(task_dir, open(note, encoding="utf-8", errors="replace").read())
    rows.append(prompt_gate(task_dir))
    if not any(r[0] == "doctrine" for r in rows):
        rows.extend(factorial_rows(task_dir, sections(open(note, encoding="utf-8", errors="replace").read())))
        rows.extend(pinning_rows(task_dir, sections(open(note, encoding="utf-8", errors="replace").read())))
        rows.extend(open_members_rows(task_dir, sections(open(note, encoding="utf-8", errors="replace").read())))
        rows.append(effort_gate(task_dir))
    fails = [r for r in rows if r[1] == "FAIL"]
    for check, level, detail in rows:
        if quiet and level == "PASS":
            continue
        print("%-4s  %-40s %s" % (level, check, detail))
    print("%s  %s: %d checks, %d FAIL, %d WARN" % ("PASS" if not fails else "FAIL", os.path.basename(task_dir), len(rows),
                                                 len(fails), sum(1 for r in rows if r[1] == "WARN")))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
