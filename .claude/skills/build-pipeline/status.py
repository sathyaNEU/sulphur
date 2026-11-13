#!/usr/bin/env python3
"""status.py: the Sulfur board, read from every build's pipeline.json. Nothing here writes a file.

    python3 .claude/skills/build-pipeline/status.py            every Sulfur build, one line each
    python3 .claude/skills/build-pipeline/status.py next       the build to work next (a paused or returned one first)
    python3 .claude/skills/build-pipeline/status.py new        the next free task number
    python3 .claude/skills/build-pipeline/status.py taskNN     one build: status, resume line, runs, portal

Sulfur builds are numbered from task1 up. The twenty Project Mark cards kept under fingerprint/cards/ as
the already-submitted baseline are filed as markNN (mark110 to mark258, Mark's taskNN), so the two never collide.

Status (pipeline.json `status`, exact strings), in order:
  DRAWING    the draw is being fixed (card not yet registered)
  DESIGN     the card is registered; the design note is being argued (gate: precut.py exit 0)
  BUILD      pack, goldens and the answer blocks are being built (gate: the free gates, then the stage 4 threads)
  READY      every gate green; prompt and target.zip handed to the author for the platform
  RUNS       on the platform: the two runs are generating or graded, triage pending (/triage-runs)
  SUBMITTED  both runs triaged as analytical losses, average under 60, submitted for review
  APPROVED   the reviewer approved it
  RETURNED   the reviewer sent it back (the note says why)
  PAUSED     the session ended mid-stage; `resume` names the next action
  RETIRED    the author's call only
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIRST = 1


def carded():
    """Numbers with a fingerprint card on file. A retired build's folder leaves the tree but its card stays as spent,
    so its number is never handed out again (a new card would overwrite the spent record the guard reads)."""
    d = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")
    out = set()
    for f in os.listdir(d) if os.path.isdir(d) else []:
        m = re.match(r"task(\d+)\.json$", f)
        if m:
            out.add(int(m.group(1)))
    return out

ORDER = ["DRAWING", "DESIGN", "BUILD", "READY", "RUNS", "SUBMITTED", "APPROVED", "RETURNED", "PAUSED", "RETIRED"]
# What `next` picks first: work the author is waiting on, then work in flight, oldest number first.
PRIORITY = ["RETURNED", "PAUSED", "RUNS", "BUILD", "DESIGN", "DRAWING"]


def builds():
    out = []
    for name in os.listdir(REPO):
        m = re.fullmatch(r"task(\d+)", name)
        if m and int(m.group(1)) >= FIRST and os.path.isdir(os.path.join(REPO, name)):
            out.append((int(m.group(1)), name))
    return [t for _, t in sorted(out)]


def pipeline(t):
    p = os.path.join(REPO, t, "pipeline.json")
    if not os.path.exists(p):
        return {}
    try:
        return json.load(open(p, encoding="utf-8"))
    except ValueError:
        return {"status": "UNREADABLE"}


def runs_line(p):
    r = p.get("runs") or {}
    a, b = r.get("run1"), r.get("run2")
    if a is None and b is None:
        return "runs -"
    avg = r.get("average")
    if avg is None and a is not None and b is not None:
        avg = (float(a) + float(b)) / 2
    verdict = ""
    if avg is not None:
        verdict = " PASS" if avg < 60 else " FAIL"
    return "runs %s / %s avg %s%s" % (a, b, "-" if avg is None else ("%.1f" % avg), verdict)


def line(t):
    p = pipeline(t)
    st = p.get("status", "NO pipeline.json")
    dom = p.get("domain", "")
    obj = p.get("objective", "")
    arch = p.get("architecture")
    call = (p.get("call") or "")[:70]
    return "%-8s %-10s arch %-3s %-34s %-28s %-26s %s" % (
        t, st, arch if arch is not None else "-", dom[:34], obj[:28], runs_line(p), call)


def main(argv):
    ts = builds()
    if not argv:
        if not ts:
            print("no Sulfur builds yet; `status.py new` gives the first number (task%d)" % FIRST)
            return 0
        for t in ts:
            print(line(t))
        return 0
    cmd = argv[0]
    if cmd == "new":
        used = {int(t[4:]) for t in ts} | carded()
        n = FIRST
        while n in used:
            n += 1
        print("task%d" % n)
        return 0
    if cmd == "next":
        for st in PRIORITY:
            for t in ts:
                p = pipeline(t)
                if p.get("status") == st:
                    print("%s  %s  resume: %s" % (t, st, p.get("resume", "(none recorded)")))
                    return 0
        used = {int(t[4:]) for t in ts} | carded()
        n = FIRST
        while n in used:
            n += 1
        print("nothing in flight; start task%d with /build task%d <domain> <objective>" % (n, n))
        return 0
    if re.fullmatch(r"task\d+", cmd):
        p = pipeline(cmd)
        if not p:
            print("%s has no pipeline.json" % cmd)
            return 1
        print(line(cmd))
        for k in ("call", "resume", "note"):
            if p.get(k):
                print("  %s: %s" % (k, p[k]))
        fw = (p.get("runs") or {}).get("first_wrong_step") or {}
        for k, v in fw.items():
            print("  first wrong step, %s: %s" % (k, v))
        if p.get("portal"):
            print("  portal: %s" % json.dumps(p["portal"]))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
