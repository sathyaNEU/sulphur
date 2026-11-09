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
            d = re.findall(r"\b([A-Z]{1,2}\d{1,2})\b", r["depends"])
            deps[r["id"]] = d
            if any(x not in ids[:i] for x in d):
                bad_dep.append(r["id"])
        row("dependencies point at earlier results", not bad_dep,
            "every row" if not bad_dep else "a dependency that is not an earlier result on: " + ", ".join(bad_dep))
        # A result most others hang on, directly or through others, is the one-thing flip carried inside the chain:
        # the platform grades every figure against the golden, so a later result built on a wrong earlier figure is
        # wrong unless it can be graded on an input of its own (a Depends on cell saying "independent: <input>").
        # Foundation rows (assembly, discovery, framing) feed everything by nature and are not counted as hubs.
        foundation = {"assembly-reconciliation", "data-discovery", "framing"}
        area_of = dict(zip(ids, areas))
        indep = {r["id"] for r in res if re.search(r"independent\s*:?\s*\S.{8,}", r["depends"], re.I)}
        def downstream(x, seen=None):
            seen = set() if seen is None else seen
            for k, v in deps.items():
                if x in v and k not in seen and k not in indep:
                    seen.add(k)
                    downstream(k, seen)
            return seen
        hubs = [x for x in ids if area_of.get(x) not in foundation]
        if hubs:
            hub = max(hubs, key=lambda x: len(downstream(x)))
            nd = len(downstream(hub))
            ok = nd <= (len(res) - 1) / 2.0
            row("no result carries most of the others", ok,
                "the widest analytical result, %s, carries %d of the other %d" % (hub, nd, len(res) - 1) if ok else
                "%s carries %d of the other %d results through the chain: a run that misses it loses them all, which "
                "is one thing under another name; give later results inputs of their own (Depends on: "
                "\"independent: <input>\") or move the weight" % (hub, nd, len(res) - 1))
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
