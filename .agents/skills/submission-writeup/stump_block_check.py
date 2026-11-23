#!/usr/bin/env python3
"""stump_block_check.py, the form's stump question is answered in the paste as soon as the runs are back.

    python3 .agents/skills/submission-writeup/stump_block_check.py taskNN
    python3 .agents/skills/submission-writeup/stump_block_check.py --all

Checks that once both responses are saved (runs/run1.md + run2.md or response1.md + response2.md),
submission.md carries `## How is each model stumped?` directly after `## Final Recommendation`,
mentions Response 1 and Response 2, runs >= 250 words, and every quoted phrase appears in the saved
responses, prompt, or generator. Wired into gates.py as the `stump` gate.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
HEAD = "How is each model stumped?"
QUOTE = re.compile(r"\"([^\"\n]{12,}?)\"|“([^”\n]{12,}?)”")
PAIRS = [("run1.md", "run2.md"), ("response1.md", "response2.md"), ("response_1.md", "response_2.md")]
BOUND = ("RUNS", "SUBMITTED")
AFTER = ("APPROVED", "RETURNED")


def task_dir(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    return os.path.join(REPO, "task%s" % m.group(1)) if m else os.path.abspath(arg)


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'")).strip()


def find_runs(d):
    rdir = os.path.join(d, "runs")
    for a, b in PAIRS:
        pa, pb = os.path.join(rdir, a), os.path.join(rdir, b)
        if os.path.exists(pa) or os.path.exists(pb):
            return [pa, pb], [os.path.exists(pa), os.path.exists(pb)]
    return [os.path.join(rdir, "run1.md"), os.path.join(rdir, "run2.md")], [False, False]


def check(d):
    runs, have = find_runs(d)
    if not any(have):
        return "PASS", "no response on file yet; the block is written once both are saved"
    status, void = "", None
    try:
        pj = json.load(open(os.path.join(d, "pipeline.json"), encoding="utf-8"))
        status, void = str(pj.get("status", "")).upper(), (pj.get("runs") or {}).get("void")
    except Exception:
        pass
    if void:
        return "PASS", "the pair on file is recorded void in pipeline.json (%s)" % str(void)[:90]
    if status not in BOUND + AFTER:
        return "WARN", ("responses are on file at status %s: if they are the current pack's pair, set status RUNS "
                        "and write the block now; if an earlier cut's, archive them or record runs.void"
                        % (status or "unknown"))
    level, msg = content(d, runs, have)
    if level == "FAIL" and status in AFTER:
        return "WARN", "%s (status %s, filed before the block was required)" % (msg, status)
    return level, msg


def content(d, runs, have):
    if not all(have):
        return "FAIL", "only %s is on file; save both responses verbatim before the block" % (
            os.path.basename(runs[0]) if have[0] else os.path.basename(runs[1]))
    sub = os.path.join(d, "submission.md")
    if not os.path.exists(sub):
        return "FAIL", "both responses are on file and there is no submission.md"
    text = open(sub, encoding="utf-8").read()
    heads = re.findall(r"^## (.+?)\s*$", text, re.M)
    if heads.count(HEAD) != 1:
        return "FAIL", "both responses are on file and submission.md has %d '## %s' blocks (one is mandatory)" % (
            heads.count(HEAD), HEAD)
    if "Final Recommendation" not in heads:
        return "FAIL", "submission.md has no '## Final Recommendation'"
    i = heads.index("Final Recommendation")
    if i + 1 >= len(heads) or heads[i + 1] != HEAD:
        return "FAIL", "'## %s' must come directly after '## Final Recommendation' (it follows '## %s')" % (
            HEAD, heads[heads.index(HEAD) - 1] if heads.index(HEAD) else "nothing")
    block = re.search(r"^## " + re.escape(HEAD) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S).group(1)
    words = len(block.split())
    missing_names = [n for n in ("Response 1", "Response 2") if n not in block]
    if missing_names:
        return "FAIL", "the block does not take %s by name" % " and ".join(missing_names)
    if words < 250:
        return "FAIL", "the block runs %d words; each response, the fairness and the rigour take a paragraph" % words
    hay = [norm(open(p, encoding="utf-8").read()) for p in runs]
    extra = [os.path.join(d, "prompt.txt")] + sorted(glob.glob(os.path.join(d, "generator", "*.py")))
    hay += [norm(open(p, encoding="utf-8", errors="ignore").read()) for p in extra if os.path.exists(p)]
    stale = []
    for m in QUOTE.finditer(block):
        q = m.group(1) or m.group(2)
        for seg in re.split(r"\s*(?:\.\.\.|…)\s*", q):
            seg = norm(seg).strip(" .,;:")
            if len(seg) >= 12 and not any(seg in h for h in hay):
                stale.append(seg[:70])
    if stale:
        return "FAIL", "%d quoted phrase(s) in the block are in neither response, the prompt nor the generator: %s" % (
            len(stale), "; ".join(repr(s) for s in stale[:3]))
    return "PASS", "the block follows the Final Recommendation, %d words, both responses by name, every quote found" % (
        words)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--all":
        bad = 0
        for d in sorted(glob.glob(os.path.join(REPO, "task*")), key=lambda p: int(re.sub(r"\D", "", p) or 0)):
            if os.path.isdir(d):
                level, msg = check(d)
                bad += level == "FAIL"
                print("%-4s  %-7s %s" % (level, os.path.basename(d), msg))
        return 1 if bad else 0
    d = task_dir(argv[0])
    level, msg = check(d)
    print("%s  stump block: %s" % (level, msg))
    return 1 if level == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
