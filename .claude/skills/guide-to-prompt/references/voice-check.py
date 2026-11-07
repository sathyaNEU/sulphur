#!/usr/bin/env python3
"""The prompt gate. Checks a build's prompt.txt against the prompt rules and measures the batch.

Two modes. The default is the draft standard, Project Mark's prompt rules (short, one paragraph, question first, no
persona, no roll call, no count the data hold), which the author asked the harness to keep because Mark's prompts
came out short and crisp, plus Sulfur's two leak rules: no method, comparison or adjustment named, and no warning to
the solver. `--rewrite` (or `"prompt_rewritten": true` in the task's pipeline.json) checks the author's
humanised rewrite: every leak rule still FAILs, and the voice and shape rules (length, paragraphs, question
placement, persona, sequencing, LLM tells, roll call, rounding placement, shell quota) become WARNs, because the
voice is the author's.

    python3 .claude/skills/guide-to-prompt/references/voice-check.py task134        # the gate: exit 1 on any FAIL
    python3 .claude/skills/guide-to-prompt/references/voice-check.py                # the batch report, last 12 builds
    python3 .claude/skills/guide-to-prompt/references/voice-check.py --all
    python3 .claude/skills/guide-to-prompt/references/voice-check.py --file <path>  # a draft anywhere on disk

Per build it prints one PASS or FAIL line per rule and exits 1 when any rule fails, so the gate can sit in a
script. The rules are in the guide-to-prompt `SKILL.md`. The prompt is `prompt.txt`, plain text; a folder carrying only
`prompt.md` is a build shipped before the rule and is read with a warning (and fails the file rule when it
is the build under check, unless `--legacy` is passed). The batch report measures what no single prompt can
see: the spread of question forms, repeated word runs, file counts and formats.
"""

import argparse
import collections
import glob
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CARDS = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")
WINDOW = 12
CHARS = 1000

FAMILIES = {
    "Data": ("csv", "tsv", "json", "xlsx", "parquet"),
    "Visual": ("pptx", "png", "svg", "html", "jpg"),
    "Text": ("pdf", "docx"),
    "Code": ("py", "ipynb", "sql", "r"),
}
EXTS = tuple(e for group in FAMILIES.values() for e in group)
FILE_TOKEN = re.compile(r"\b[A-Za-z0-9][A-Za-z0-9_\-]*\.(?:%s)\b" % "|".join(EXTS), re.I)

# The question forms a prompt can lead with. The batch report shows their spread; a run of one form is the
# monoculture the client's note was about, now at the question instead of the role.
QUESTION_FORMS = [
    ("how-many", r"\bhow many\b"), ("how-much", r"\bhow much\b"), ("which", r"\bwhich\b"),
    ("whether", r"\bwhether\b|\b(do|does|should|will|can|is|are) (we|it|the|our|this|that)\b"),
    ("what", r"\bwhat\b"), ("when", r"\bwhen\b"), ("who", r"\bwho\b"), ("where", r"\bwhere\b"),
]

# Markdown and layout characters. Underscores and asterisks are read outside file names only.
MARKDOWN = [
    ("backtick", r"`"), ("hash", r"(?m)^\s*#"), ("pipe", r"\|"), ("bracket", r"[\[\]]"),
    ("bullet", r"(?m)^\s*(?:[-*+]|\d+[.)])\s"), ("emphasis", r"\*|(?<![\w.\-])_|_(?![\w.\-])"),
    ("bold-colon label", r"(?m)^\s*\w[\w ]{0,30}:\s"),
]

# Job-title introductions, sign-off chains and the people who read the file: point 2 of the prompt rules.
TITLE_INTRO = [
    r"\b(I am|I'm|I was|we are|we're) (the |a |an |our )?(?:[a-z\-]+ ){0,3}(director|manager|head|lead|officer|analyst|planner|chair|chairman|chairwoman|coordinator|engineer|controller|actuary|economist|statistician|superintendent|commissioner|administrator|supervisor|scientist|strategist|epidemiologist|underwriter|treasurer|secretary|partner|principal|consultant|specialist)\b",
    r"\bI (run|lead|head|manage|direct|chair|oversee|look after|am responsible for|sit on|own)\b",
    r"\bmy (team|desk|unit|department|office|staff|analysts?|colleagues?)\b",
    r"\b(head|director|manager|chair|lead|officer|vice president|controller|superintendent|commissioner|secretary)s? of (the )?[A-Z][\w&]*",
    r"\b(she|he|they|who) (chairs?|runs?|leads?|heads?|manages?|directs?|reviews?|oversees?) (the|our|its)\b",
    r"\b(signs? (it )?off|sign-off|takes? (it|them|this|these) to the (board|committee|council|cabinet|minister)|goes to the (board|committee|council)|the (board|committee|council|cabinet) (votes?|meets|signs|sees|reviews) )",
    r"\b(reads? (it|this|them|the \w+) first|who reads|will read it|reads first)\b",
]

ROLL_CALL = r"\b(thinks|believes|argues|wants|reckons|insists|is convinced|has been working on the basis|would rather|prefers|blames|says the answer|expects it to be|is sure)\b"
SEQUENCING = r"(?:(?<=[.;?!]\s)|^)(Then|Next|Last|Lastly|Finally|First|Firstly|Second|Secondly|Third|Thirdly|After that|Following that),?\s"
TELLS = [
    r"\bleverag\w*\b", r"\brobust\b", r"\bcomprehensive\b", r"\bseamless\w*\b", r"\bdelve\b", r"\bactionable\b",
    r"\bholistic\b", r"\bstreamlin\w*\b", r"\butili[sz]\w*\b", r"\bnuanced\b", r"\blandscape\b", r"\bnavigat(?:e|es|ed|ing)\b",
    r"\bcrucial\b", r"\bpivotal\b", r"\bin order to\b", r"\bfurthermore\b", r"\bmoreover\b", r"\badditionally\b",
    r"\bit is (important|worth) (to note|noting)\b", r"\bnote that\b", r"\bmake sure\b", r"\bensur\w*\b",
    r"\bplease\b", r"\bkey (insight|driver|finding|takeaway)s?\b", r"\bdeep[- ]dive\b", r"\bbest practice\b",
    r"\bstakeholders?\b", r"\brobustly\b", r"\bempower\w*\b", r"\bunlock\b", r"\bjourney\b", "\u2013", "\u2014",
]
NOT_NAMES = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
             "Attachment", "Schedule", "Section", "Appendix", "Table", "Figure", "Part", "Chapter", "Order", "Act",
             "Reservoir", "Creek", "River", "County", "District", "Services", "Committee", "Board", "Council", "Street"}
# A count the data hold, stated in the prompt. The portal's models are handed the size of the candidate set, the
# population or a derivable count ("which four of the eight", "each of our twelve zones", "we run 264 schools"), and
# what the model should find on its own is read off the prompt instead. A filed decision parameter stays legal
# where it is not tied to a count the data hold ("designate seven" passes; "seven of the sixteen" fails). Years,
# money, physical and time units and the deliverable's own parts are not counts of the data.
NUM = r"(?:\d{1,3}(?:,\d{3})*|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|dozen)"
UNIT_NOUNS = {"decimals", "places", "days", "weeks", "months", "quarters", "years", "hours", "minutes", "seconds", "characters",
              "files", "sheets", "tabs", "pages", "charts", "figures", "dollars", "euros", "pounds", "cents", "pence", "kronor",
              "francs", "yen", "rupees", "tonnes", "tons", "kilograms", "kilos", "grams", "litres", "liters", "gallons", "barrels",
              "megawatts", "kilowatts", "gigawatts", "miles", "kilometres", "kilometers", "metres", "meters", "feet", "inches",
              "hectares", "acres", "degrees", "points", "percent", "bins", "decimal", "seasons", "terms", "fortnights", "nights",
              "shifts", "rounds", "cycles", "halves", "thirds"}
COUNT_DISCLOSURE = [
    ("N of the M", r"\b%s\s+of\s+(?:the|our|its|their|these|those)\b" % NUM),
    ("each of the N", r"\b(?:each|every one|all|any|which|how many|most)\s+of\s+(?:the|our|its|their|these|those)\s+(?:about\s+|some\s+)?%s\b" % NUM),
    ("the N things", r"\b(?:the|our|its|their|all|these|those)\s+(?:about\s+|some\s+|roughly\s+)?%s\s+([a-z][a-z\-]+(?:s|es))\b" % NUM),
    ("we have N", r"\bwe\s+(?:have|run|operate|serve|cover|track|hold|manage|own|list|field)\s+(?:about\s+|some\s+|roughly\s+|around\s+|just\s+over\s+|just\s+under\s+)?%s\s+[a-z]" % NUM),
]
# The shell a reviewer reads across the corpus, and the share of shipped prompts any one class may hold. The portal
# holds every accepted task with no window, so the quotas run over every prompt on file, not the last twelve.
QUOTAS = {"question form": 0.30, "second-sentence opener": 0.20, "rounding opener": 0.20, "deliverable set": 0.20}

# Sulfur: the prompt "never names the method, the trap, the comparison group, the confounder, the adjustment or the
# file that matters, and never warns". FAIL in both modes.
METHOD_NAMED = [
    r"\bdifference[- ]in[- ]differences?\b", r"\bdiff[- ]in[- ]diff\b", r"\bsynthetic control\b", r"\bpropensity\b",
    r"\binstrumental variables?\b", r"\bregression discontinuity\b", r"\bparallel trends?\b", r"\bpre[- ]?trends?\b",
    r"\bevent[- ]study\b", r"\bplacebo test\b", r"\bclustered (standard )?errors?\b", r"\bcluster[- ]robust\b",
    r"\bdesign effect\b", r"\bintra[- ]?class\b", r"\bshrink(age)?\b", r"\bempirical bayes\b", r"\bpartial pooling\b",
    r"\bhierarchical model\b", r"\bmixed[- ]effects?\b", r"\brandom effects?\b", r"\bfixed effects?\b",
    r"\bregression to the mean\b", r"\bsimpson'?s\b", r"\bmix (shift|effect)\b", r"\bcomposition(al)? effect\b",
    r"\bseasonal(ly)? adjust\w*\b", r"\bdeseasonali[sz]\w*\b", r"\bchain[- ]ladder\b", r"\bdevelopment (triangle|factors?|curves?)\b",
    r"\bkaplan\b", r"\bcox (model|regression)\b", r"\bsurvival (curve|analysis|model)\b", r"\bcensor\w*\b",
    r"\bback[- ]?test\w*\b", r"\bcross[- ]validat\w*\b", r"\bout[- ]of[- ]sample\b", r"\bstratif\w*\b", r"\bre-?weight\w*\b",
    r"\bstandardi[sz]\w*\b", r"\bde-?dup\w*\b", r"\b(adjust|adjusting|control|controlling|correct|correcting) for\b",
    r"\bcounterfactual\b", r"\bconfound\w*\b",
]
# The organisation's own word for a thing, or a pointer at the step: WARN, the author judges.
METHOD_HINT = [r"\bhold[- ]?out\b", r"\bcohorts?\b", r"\bmatur\w*\b", r"\bspillover\b", r"\bcontaminat\w*\b",
               r"\bnovelty\b", r"\bpooled\b", r"\bweighted\b", r"\bseasonal\w*\b", r"\bcannibali[sz]\w*\b",
               r"\bcomparison group\b", r"\bcontrol group\b"]   # a trial's own arm is a fact; choosing one is the step
SOLVER_WARNING = [r"\bbe careful\b", r"\bwatch out\b", r"\bbeware\b", r"\bmake sure\b", r"\bdon'?t forget\b",
                  r"\bdo not forget\b", r"\bkeep in mind\b", r"\bbear in mind\b", r"\bnote that\b", r"\bbe aware\b",
                  r"\bpay (close )?attention\b", r"\btricky\b", r"\btraps?\b", r"\bpitfalls?\b", r"\bgotchas?\b",
                  r"\bmisleading\b", r"\bdon'?t be fooled\b", r"\bat face value\b"]
# The client's templating checker (portal, 2026-11-07): seven signals, templated at three, borderline at two. The
# gate counts them and FAILs at two in both modes, because the portal reads the rewrite the same way.
UP_FRONT_FILES = r"\b(?:using|with|from|in|see) (?:the )?(?:attached|enclosed|supplied|provided) (?:files?|data|pack|documents?)\b"
DICTATED = [r"\baccording to (?:the|our) (?:standard|manual|policy|procedure|guidelines?|method\w*)\b",
            r"\b(?:by|following|per|under) (?:the|our) (?:manual|procedure|methodology|playbook)\b",
            r"\bthe way (?:the|our) (?:standard|manual|policy|procedure|guidelines?) (?:sets? out|says|lays? out)\b"]
INLINE_LIST = r"(?:^|[\s;:,])(?:\(?[0-9]{1,2}\)|\(?[a-hA-H]\)|\(?(?:i|ii|iii|iv|v)\))\s+\w|\u2022|(?:^|\s)[-*]\s+\w"
UK_SPELLING = [r"\blabell(?:ed|ing)\b", r"\bcolour\w*\b", r"\borganis\w*\b",
               r"\b(?:recognis|realis|prioritis|summaris|minimis|maximis|optimis|categoris|standardis|normalis|"
               r"finalis|utilis|characteris|emphasis|apologis|authoris|capitalis)(?:e|es|ed|ing|ation)\b",
               r"\banalys(?:e|es|ed|ing)\b(?<!analyses)", r"\bbehaviour\w*\b", r"\bfavour\w*\b", r"\bcentre\w*\b",
               r"\bprogramme\w*\b", r"\bmodell(?:ed|ing)\b", r"\bcatalogue\w*\b", r"\blicence\b"]
DOC_NOUNS = r"\b(?:memo|note|report|deck|slides?|workbook|spreadsheet|csv|chart|table|summary|brief|notebook|script|file|files|document|documents)\b"


def templating_signals(text):
    """The client's seven templating signals found in a prompt, each with its evidence."""
    sents = sentences(text)
    found = []
    head = " ".join(sents[:2])
    if len(FILE_TOKEN.findall(head)) >= 2 or re.search(UP_FRONT_FILES, head, re.I):
        found.append("files listed up front (%s)" % (", ".join(FILE_TOKEN.findall(head)) or "attached files"))
    seq = [m.group(1) for m in re.finditer(SEQUENCING, re.sub(r"\s+", " ", text))]
    if seq:
        found.append("requests laid out as steps (%s)" % ", ".join(seq))
    qs = [s for s in sents if "?" in s]
    opening_qs = [s for s in sents[:2] if "?" in s]
    if len(qs) >= 3 or len(opening_qs) >= 2:
        found.append("stacked questions (%d question sentences, %d in the opening)" % (len(qs), len(opening_qs)))
    if sents:
        last = sents[-1]
        nfiles = len(FILE_TOKEN.findall(last)); ndocs = len(re.findall(DOC_NOUNS, FILE_TOKEN.sub(" ", last), re.I))
        words = len(re.findall(r"[A-Za-z]+", FILE_TOKEN.sub(" ", last)))
        if nfiles >= 2 or (nfiles + ndocs >= 3 and words <= 18):
            found.append("a closing list of documents (%r)" % last[:80])
    for pat in DICTATED:
        m = re.search(pat, text, re.I)
        if m:
            found.append("a dictated method (%r)" % m.group(0)); break
    if re.search(INLINE_LIST, FILE_TOKEN.sub(" FILE ", text)):
        found.append("a list inside the prompt")
    uk = []
    for pat in UK_SPELLING:
        m = re.search(pat, text, re.I)
        if m:
            uk.append(m.group(0))
    if uk:
        found.append("UK spelling (%s)" % ", ".join(dict.fromkeys(uk)))
    return found


# The rules a rewrite turns into WARNs: voice and shape, which the author owns.
VOICE_RULES = {"one paragraph", "question first", "under 1,000 characters", "no persona or title", "no sequencing",
               "no LLM tells", "no roll call", "rounding at the close", "shell quota"}


def rewritten(task):
    """True when the task's pipeline.json records that prompt.txt is the author's rewrite."""
    if not task:
        return False
    p = os.path.join(REPO, task if str(task).startswith("task") else "task%s" % task, "pipeline.json")
    try:
        return bool(json.load(open(p, encoding="utf-8")).get("prompt_rewritten"))
    except (OSError, ValueError):
        return False


ROUNDING = (r"to the nearest \w+|to (?:one|two|three|\d) decimal(?: place)?s?|a decimal place|whole (?:number|unit|count|dollar|pound|euro|case|household|record|release|day|cubic yard|ton)s?|"
            r"significant figures?|rounded? (?:up|down|to)|no decimals?|as (?:a )?whole numbers?|in whole \w+")


def task_no(path):
    m = re.search(r"task(\d+)", path)
    return int(m.group(1)) if m else -1


def find_prompt(task_dir):
    """prompt.txt first; prompt.md only for a build shipped before the rule, flagged legacy."""
    txt = os.path.join(task_dir, "prompt.txt")
    md = os.path.join(task_dir, "prompt.md")
    if os.path.exists(txt):
        return txt, False
    if os.path.exists(md):
        return md, True
    return None, False


def body(path, legacy):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if legacy:
        raw = re.sub(r"^```.*?^```", "", raw, flags=re.M | re.S)
        raw = re.sub(r"^\s*#.*$", "", raw, flags=re.M)
        raw = re.sub(r"^\s*>.*$", "", raw, flags=re.M)
    return raw.strip("\n")


def sentences(text):
    flat = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in re.split(r"(?<![0-9])(?<=[.!?])\s+", flat) if s.strip()]


def first_sentence(text):
    s = sentences(text)
    return s[0] if s else text[:200]


def question_form(text):
    """The form of the first question in the prompt, or 'none'."""
    for s in sentences(text)[:2]:
        if "?" in s:
            for name, pat in QUESTION_FORMS:
                if re.search(pat, s, re.I):
                    return name
            return "other"
    return "none"


def deliverables(text):
    return sorted({m.group(0).lower() for m in FILE_TOKEN.finditer(text)})


def people_of(task):
    """Personas from the fingerprint card, as full names, so a prompt that names one fails."""
    p = os.path.join(CARDS, "%s.json" % task)
    if not os.path.exists(p):
        return []
    try:
        card = json.load(open(p))
    except Exception:
        return []
    people = ((card.get("world") or {}).get("people")) or []
    out = []
    for x in people:
        if isinstance(x, dict):
            x = x.get("name") or x.get("full_name") or ""
        if isinstance(x, str) and x.strip():
            out.append(x.strip())
    return out


def task_status(task):
    """The build's pipeline.json status, or '' when it cannot be read."""
    if not task:
        return ""
    try:
        import json
        d = os.path.join(REPO, task if str(task).startswith("task") else "task%s" % re.sub(r"[^0-9]", "", str(task)))
        return json.load(open(os.path.join(d, "pipeline.json"))).get("status") or ""
    except Exception:
        return ""


def count_disclosures(text):
    """Every count of the data the prompt states (see COUNT_DISCLOSURE)."""
    masked = FILE_TOKEN.sub(" FILE ", text)
    hits = []
    for name, pat in COUNT_DISCLOSURE:
        for m in re.finditer(pat, masked, re.I):
            if name == "the N things" and m.group(1).lower() in UNIT_NOUNS:
                continue
            hits.append("%s: \"%s\"" % (name, re.sub(r"\s+", " ", m.group(0)).strip()))
    return hits


def opener(sentence, words=1):
    ws = re.findall(r"[A-Za-z']+", sentence)
    return " ".join(w.lower() for w in ws[:words]) if ws else ""


def shell_of(text):
    """The prompt's shell classes: question form, the second sentence's opening word, the rounding sentence's opening
    word and the deliverable set (sorted extensions)."""
    sents = sentences(text)
    r_sents = [s for s in sents if re.search(ROUNDING, s, re.I)]
    return {
        "question form": question_form(text),
        "second-sentence opener": opener(sents[1]) if len(sents) > 1 else "",
        "rounding opener": opener(r_sents[-1]) if r_sents else "",
        "deliverable set": "+".join(sorted(f.rsplit(".", 1)[-1].lower() for f in deliverables(text))),
    }


_SHARES = {}


def corpus_shares():
    """Share of every shell class over every prompt on file, computed once per run."""
    if _SHARES:
        return _SHARES
    folders = [d for d in glob.glob(os.path.join(REPO, "task*")) if os.path.isdir(d)]
    counts = {k: collections.Counter() for k in QUOTAS}
    n = 0
    for d in folders:
        path, legacy = find_prompt(d)
        if not path:
            continue
        try:
            sh = shell_of(body(path, legacy))
        except Exception:
            continue
        n += 1
        for k, v in sh.items():
            counts[k][v] += 1
    _SHARES["n"] = n
    for k in QUOTAS:
        _SHARES[k] = {v: c / max(n, 1) for v, c in counts[k].items()}
    return _SHARES


def gate(text, task=None, legacy=False, rewrite=None):
    """One (rule, PASS|FAIL|WARN, detail) per rule. The gate fails on any FAIL. On a rewrite the voice rules WARN."""
    if rewrite is None:
        rewrite = rewritten(task)
    rows = _gate(text, task, legacy)
    if rewrite:
        rows = [(r, "WARN" if (lv == "FAIL" and r in VOICE_RULES) else lv, d) for r, lv, d in rows]
    return rows


def _gate(text, task=None, legacy=False):
    rows = []
    masked = FILE_TOKEN.sub(" FILE ", text)
    sents = sentences(text)

    rows.append(("file", "FAIL" if legacy else "PASS",
                 "prompt.md is a build shipped before the rule; write prompt.txt" if legacy else "prompt.txt"))

    hits = []
    for name, pat in MARKDOWN:
        src = masked if name in ("emphasis",) else text
        ms = list(re.finditer(pat, src))
        if ms:
            hits.append("%s x%d" % (name, len(ms)))
    rows.append(("plain text", "FAIL" if hits else "PASS", ", ".join(hits) or "no markdown character"))

    inner = text.strip()
    breaks = inner.count("\n")
    rows.append(("one paragraph", "FAIL" if breaks else "PASS",
                 "%d line break(s) inside the prompt" % breaks if breaks else "one continuous paragraph"))

    early = any("?" in s for s in sents[:2])
    rows.append(("question first", "PASS" if early else "FAIL",
                 "a question in the first two sentences" if early else "no question mark in the first two sentences; lead with the question"))

    n = len(inner)
    rows.append(("under 1,000 characters", "PASS" if n < CHARS else "FAIL", "%d characters" % n))

    named, hints, warns = [], [], []
    for pat in METHOD_NAMED:
        m = re.search(pat, masked, re.I)
        if m:
            named.append(m.group(0))
    rows.append(("no method named", "FAIL" if named else "PASS",
                 ("names %s: the prompt pins the question, the decision, the deciding outcome or threshold and the "
                  "deliverables, never the method, comparison or adjustment" % ", ".join(dict.fromkeys(named))) if named else "none"))
    for pat in METHOD_HINT:
        m = re.search(pat, masked, re.I)
        if m:
            hints.append(m.group(0))
    rows.append(("no method hint", "WARN" if hints else "PASS",
                 ("carries %s: keep only if it is the organisation's own word for a thing, not a pointer to the step"
                  % ", ".join(dict.fromkeys(hints))) if hints else "none"))
    for pat in SOLVER_WARNING:
        m = re.search(pat, masked, re.I)
        if m:
            warns.append(m.group(0))
    rows.append(("no warning to the solver", "FAIL" if warns else "PASS",
                 "warns the solver: " + ", ".join(dict.fromkeys(warns)) if warns else "none"))

    dash = len(re.findall("\u2014", text))
    rows.append(("no em dash", "FAIL" if dash else "PASS", "%d em dash(es)" % dash if dash else "none"))

    found = []
    for name in people_of(task) if task else []:
        parts = name.split()
        if re.search(r"\b%s\b" % re.escape(name), text):
            found.append(name)
        elif len(parts) >= 2 and re.search(r"\b%s\b" % re.escape(parts[-1]), text) and re.search(r"\b%s\b" % re.escape(parts[0]), text):
            found.append(name)
    generic = re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z]+)(?:'s)? (?:chairs|reviews|runs|leads|heads|manages|signs|wants|reads|takes|presents|asked|sits|is our|is the)\b", text)
    found += [g for g in generic if g not in found and g.split()[0] not in NOT_NAMES and g.split()[1] not in NOT_NAMES]
    titles = []
    for pat in TITLE_INTRO:
        for m in re.finditer(pat, text):
            titles.append(re.sub(r"\s+", " ", m.group(0)).strip())
    detail = []
    if found:
        detail.append("persona named: " + ", ".join(found))
    if titles:
        detail.append("title or sign-off: " + "; ".join(titles[:4]))
    rows.append(("no persona or title", "FAIL" if detail else "PASS", "; ".join(detail) or "no name, title, sign-off chain or reader"))

    seq = [m.group(1) for m in re.finditer(SEQUENCING, re.sub(r"\s+", " ", text))]
    rows.append(("no sequencing", "FAIL" if seq else "PASS", "sentence openers: " + ", ".join(seq) if seq else "none"))

    tells = []
    for pat in TELLS:
        ms = re.findall(pat, text, re.I)
        if ms:
            tells.append(ms[0] if isinstance(ms[0], str) else pat)
    tells = [t if t not in ("\u2013", "\u2014") else ("en dash" if t == "\u2013" else "em dash") for t in tells]
    rows.append(("no LLM tells", "FAIL" if tells else "PASS", ", ".join(dict.fromkeys(tells)) or "none"))

    beliefs = re.findall(ROLL_CALL, text, re.I)
    level = "FAIL" if len(beliefs) >= 2 else ("WARN" if beliefs else "PASS")
    rows.append(("no roll call", level, "%d attributed opinion(s)" % len(beliefs) if beliefs else "none"))

    r_sents = [i for i, s in enumerate(sents) if re.search(ROUNDING, s, re.I)]
    non_final = [i for i in r_sents if i < len(sents) - 1]
    if not r_sents:
        rows.append(("rounding at the close", "WARN", "no rounding words anywhere; every derived figure needs one, stated once at the end"))
    elif len(non_final) >= 2 or (non_final and (len(sents) - 1) not in r_sents):
        rows.append(("rounding at the close", "FAIL", "rounding stated in %d sentence(s) before the last; state each rule once at the end" % len(non_final)))
    else:
        rows.append(("rounding at the close", "PASS", "rounding stated once, at the close"))

    counts = count_disclosures(text)
    shipped = task_status(task) in ("SHIPPED", "SHIPPED_APPROVED", "RETIRED", "SUBMITTED", "APPROVED")
    rows.append(("no data count disclosed", ("WARN" if shipped else "FAIL") if counts else "PASS",
                 ("; ".join(counts) + " (a count the data hold is the model's to find; drop it or keep only the "
                  "decision parameter)") if counts else "no candidate-set size, population or derivable count stated"))

    sh = shell_of(text)
    shares = corpus_shares()
    over = []
    for k, cap in QUOTAS.items():
        v = sh.get(k) or ""
        share = shares.get(k, {}).get(v, 0.0)
        if v and v != "none" and share > cap:
            over.append("%s %r at %d%% of %d prompts (cap %d%%)" % (k, v, round(share * 100), shares.get("n", 0), round(cap * 100)))
    rows.append(("shell quota", "WARN" if over else "PASS",
                 "; ".join(over) + "; reword at the role level, not the verb" if over else
                 "question form, second-sentence opener, rounding opener and deliverable set all under their corpus caps"))

    sig = templating_signals(text)
    rows.append(("templating signals", "FAIL" if len(sig) >= 2 else ("WARN" if sig else "PASS"),
                 ("%d of seven: " % len(sig) + "; ".join(sig) + " (the portal marks two as borderline and three as "
                  "templated: one question, each file named in the sentence that gives its reason, no closing list)")
                 if sig else "none of the client's seven templating signals"))

    files = deliverables(text)
    if not files:
        rows.append(("deliverables named", "FAIL", "no output file name with an extension"))
    elif len(files) > 3:
        rows.append(("deliverables named", "FAIL", "%d files named, three is the ceiling" % len(files)))
    else:
        rows.append(("deliverables named", "PASS", ", ".join(files)))
    return rows


def print_gate(label, rows):
    worst = "PASS"
    print("PROMPT GATE  %s" % label)
    for rule, level, detail in rows:
        print("  %-5s %-24s %s" % (level, rule, detail))
        if level == "FAIL":
            worst = "FAIL"
    print("  -> %s" % worst)
    return worst


def econ(text):
    sents = sentences(text)
    wc = len(re.findall(r"[A-Za-z']+", text))
    return {"chars": len(text.strip()), "words": wc, "sents": len(sents),
            "wps": round(wc / max(len(sents), 1), 1), "files": len(deliverables(text)),
            "form": question_form(text)}


def ngrams(text, n):
    words = re.findall(r"[a-z']+", FILE_TOKEN.sub(" FILE ", text).lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def batch(paths):
    texts = {}
    for p in paths:
        path, legacy = find_prompt(p)
        if not path:
            continue
        texts[p] = (body(path, legacy), legacy)
    if not texts:
        sys.exit("no task*/prompt.txt or prompt.md found under %s" % REPO)
    names = ", ".join(os.path.basename(p) for p in texts)
    print("voice-check over %d builds: %s\n" % (len(texts), names))
    legacy_n = sum(1 for _, (t, lg) in texts.items() if lg)
    if legacy_n:
        print("WARNING  %d build(s) carry prompt.md only (shipped before the prompt.txt rule); read for the batch view\n" % legacy_n)

    print("QUESTION FORM".ljust(22) + "builds")
    forms = collections.Counter(question_form(t) for t, _ in texts.values())
    for f, c in forms.most_common():
        flag = "  <-- concentrated" if f != "none" and c > max(2, len(texts) // 3) else ""
        print("  %-20s%2d  %s%s" % (f, c, "#" * c, flag))
    print("  %d distinct forms; %d prompt(s) with no question in the first two sentences\n" % (len(forms) - (1 if "none" in forms else 0), forms.get("none", 0)))

    print("FIRST SENTENCE")
    for p, (t, lg) in texts.items():
        print("  %-9s [%-9s] %s" % (os.path.basename(p), question_form(t), first_sentence(t)[:90]))
    print()

    print("UNLISTED REPEATS (6+ word runs shared by a third of the batch)")
    shared = collections.Counter()
    for t, _ in texts.values():
        for g in ngrams(t, 6):
            shared[g] += 1
    floor = max(3, len(texts) // 3)
    rows = sorted([(c, g) for g, c in shared.items() if c >= floor], key=lambda r: (-r[0], r[1]))
    if rows:
        for c, g in rows[:12]:
            print("  %2d  \"%s\"" % (c, g))
    else:
        print("  none")
    print()

    print("SHELL QUOTAS (share of every prompt on file; the portal has no window)")
    shares = corpus_shares()
    for k, cap in QUOTAS.items():
        top = sorted(shares.get(k, {}).items(), key=lambda kv: -kv[1])[:4]
        line = ", ".join("%s %d%%" % (v or "(none)", round(sh * 100)) for v, sh in top)
        worst = top[0][1] if top else 0.0
        flag = "  <-- over the %d%% cap" % round(cap * 100) if worst > cap else ""
        print("  %-24s %s%s" % (k, line, flag))
    disclosed = sum(1 for t, _ in texts.values() if count_disclosures(t))
    print("  %d of %d prompts in this batch disclose a count the data hold\n" % (disclosed, len(texts)))

    print("SHAPE AND SIZE".ljust(12) + "   chars  words  sents  w/sent  files")
    ext_counter = collections.Counter()
    fails = 0
    for p, (t, lg) in texts.items():
        e = econ(t)
        for f in deliverables(t):
            ext_counter[f.rsplit(".", 1)[-1]] += 1
        rows_g = gate(t, os.path.basename(p), legacy=lg)
        nf = sum(1 for _, lv, _ in rows_g if lv == "FAIL")
        fails += 1 if nf else 0
        flag = "   <-- %d rule(s) fail" % nf if nf else ""
        print("  %-9s %6d %6d %6d %7s %6d%s" % (os.path.basename(p), e["chars"], e["words"], e["sents"], e["wps"], e["files"], flag))
    chars = [econ(t)["chars"] for t, _ in texts.values()]
    print("  median chars %.0f, over the ceiling %d of %d; formats %s" % (
        statistics.median(chars), sum(1 for c in chars if c >= CHARS), len(chars),
        ", ".join(".%s %d" % (e, c) for e, c in ext_counter.most_common())))
    print("  %d of %d prompts fail at least one gate rule (run with the task number for the list)" % (fails, len(texts)))
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tasks", nargs="*", help="task numbers or folders to gate; none for the batch report")
    ap.add_argument("--all", action="store_true", help="batch report over every build")
    ap.add_argument("--file", help="gate a draft prompt file anywhere on disk")
    ap.add_argument("--task", help="with --file: the task number whose card names the personas")
    ap.add_argument("--legacy", action="store_true", help="accept prompt.md for a build shipped before the rule")
    ap.add_argument("--rewrite", action="store_true", help="the author's rewrite: leak rules FAIL, voice rules WARN")
    a = ap.parse_args(argv)

    if a.file:
        legacy = a.file.endswith(".md") and not a.legacy
        text = body(a.file, legacy=a.file.endswith(".md"))
        worst = print_gate(a.file, gate(text, a.task, legacy=legacy, rewrite=True if a.rewrite else None))
        return 1 if worst == "FAIL" else 0

    folders = sorted((d for d in glob.glob(os.path.join(REPO, "task*")) if os.path.isdir(d)), key=task_no)
    folders = [d for d in folders if find_prompt(d)[0]]
    if a.tasks:
        wanted = {re.sub(r"[^0-9]", "", t) for t in a.tasks}
        rc = 0
        for d in folders:
            if str(task_no(d)) not in wanted:
                continue
            wanted.discard(str(task_no(d)))
            path, legacy = find_prompt(d)
            text = body(path, legacy)
            rows = gate(text, os.path.basename(d), legacy=legacy and not a.legacy, rewrite=True if a.rewrite else None)
            if print_gate("%s (%s)" % (os.path.basename(d), os.path.basename(path)), rows) == "FAIL":
                rc = 1
            print()
        for miss in sorted(wanted, key=lambda x: int(x or 0)):
            sys.stderr.write("voice-check: no prompt found for task%s (looked for task%s/prompt.txt)\n" % (miss, miss))
            rc = 2
        return rc
    selected = folders if a.all else folders[-WINDOW:]
    return batch(selected)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
