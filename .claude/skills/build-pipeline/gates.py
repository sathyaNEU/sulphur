#!/usr/bin/env python3
"""gates.py, every free gate of a build in one pass, run side by side, with one summary.

    python3 .claude/skills/build-pipeline/gates.py taskNN            # the gates that read the cut pack
    python3 .claude/skills/build-pipeline/gates.py taskNN --full     # also checks.py, verify.py, two rebuilds
    python3 .claude/skills/build-pipeline/gates.py taskNN --only precut,effort

The stage 3 and stage 5 gates were run one by one, each waiting on the last, and a build spent most of an hour of
its stage 5 re-running them in sequence. The scripts read the pack and write only their own reports, so they run
concurrently here. Each gate's own exit status is the verdict: 0 PASS, a REVIEW from leak.py or a WARN-only run is
WARN, anything else FAIL. Exit 1 when any gate FAILs. It spawns no agent and costs nothing.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SK = os.path.join(REPO, ".claude", "skills")
PY = sys.executable


def task_dir(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    return os.path.join(REPO, "task%s" % m.group(1)) if m else os.path.abspath(arg)


def gates(d, full):
    t = os.path.basename(d)
    rewrite = False
    try:
        rewrite = bool(json.load(open(os.path.join(d, "pipeline.json"))).get("prompt_rewritten"))
    except Exception:
        pass
    # the dates sweep runs only with the fiction's as-of date: metadata.json's as_of (task7 architecture 12 shipped a
    # year of exports past their own stamps because the sweep was skipped)
    asof = []
    try:
        a = json.load(open(os.path.join(d, "metadata.json"))).get("as_of")
        if a:
            asof = ["--asof", str(a)[:10]]
    except Exception:
        pass
    g = [
        ("precut", [PY, os.path.join(SK, "stumping", "precut.py"), d, "--quiet"]),
        ("voice", [PY, os.path.join(SK, "guide-to-prompt", "references", "voice-check.py"), t]
         + (["--rewrite"] if rewrite else [])),
        ("leak", [PY, os.path.join(SK, "leak-check", "leak.py"), t, "--quiet"] + asof),
        ("figures", [PY, os.path.join(SK, "determinism-check", "figures_check.py"), t]),
        ("containers", [PY, os.path.join(SK, "reduce-house-fixes", "scripts", "audit_containers.py"), t]),
        ("heart", [PY, os.path.join(SK, "fingerprint", "guard.py"), "heart", t]),
        ("surface", [PY, os.path.join(SK, "fingerprint", "guard.py"), "surface", t]),
    ]
    if os.path.exists(os.path.join(d, "generator", "effort.json")):
        g.insert(1, ("effort", [PY, os.path.join(SK, "stumping", "effort.py"), d, "--check-note"]))
    if full:
        for name in ("checks", "verify"):
            path = os.path.join(d, "generator", name + ".py")
            if os.path.exists(path):
                g.append((name, [PY, path]))
    return g


def run(name, cmd, cwd):
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=1800)
        out, code = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        out, code = "timed out after 1800s", 124
    if name == "leak":
        level = {0: "PASS", 1: "WARN", 2: "FAIL"}.get(code, "FAIL")
    else:
        level = "PASS" if code == 0 else "FAIL"
        if level == "PASS" and re.search(r"^\s*WARN\b", out, re.M):
            level = "WARN"
    lines = [l.strip() for l in out.splitlines() if re.match(r"\s*(FAIL|BLOCK|LEAK|Traceback|AssertionError|Error)", l)]
    if level == "WARN" and not lines:
        lines = [l.strip() for l in out.splitlines() if re.match(r"\s*(WARN|REVIEW)", l)]
    return name, level, time.time() - t0, lines[:4], code


def rebuild_twice(d):
    """Two builds into scratch folders, compared byte for byte (dataset-generation §11)."""
    build = os.path.join(d, "generator", "build.py")
    if not os.path.exists(build):
        return "rebuild", "WARN", 0.0, ["no generator/build.py"], 0
    t0 = time.time()
    digests = []
    for _ in range(2):
        out = tempfile.mkdtemp(prefix="gates-%s-" % os.path.basename(d))
        r = subprocess.run([PY, build, "--out", out], capture_output=True, text=True, cwd=d, timeout=3600)
        if r.returncode:
            shutil.rmtree(out, ignore_errors=True)
            return "rebuild", "FAIL", time.time() - t0, (r.stdout + r.stderr).strip().splitlines()[-3:], r.returncode
        h = hashlib.sha256()
        for root, _, files in sorted(os.walk(out)):
            for f in sorted(files):
                p = os.path.join(root, f)
                h.update(os.path.relpath(p, out).encode())
                h.update(open(p, "rb").read())
        digests.append(h.hexdigest())
        shutil.rmtree(out, ignore_errors=True)
    same = digests[0] == digests[1]
    return "rebuild", "PASS" if same else "FAIL", time.time() - t0, \
        [] if same else ["two builds differ: %s against %s" % (digests[0][:12], digests[1][:12])], 0 if same else 1


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    d = task_dir(args[0])
    if not os.path.isdir(d):
        print("no task folder at %s" % d)
        return 2
    full = "--full" in argv
    only = None
    for a in argv:
        if a.startswith("--only"):
            only = set((a.split("=", 1)[1] if "=" in a else args[1] if len(args) > 1 else "").split(","))
    todo = [(n, c) for n, c in gates(d, full) if not only or n in only]
    t0 = time.time()
    results = []
    with cf.ThreadPoolExecutor(max_workers=max(1, min(8, len(todo) + 1))) as ex:
        futs = [ex.submit(run, n, c, REPO) for n, c in todo]
        if full and (not only or "rebuild" in only):
            futs.append(ex.submit(rebuild_twice, d))
        for f in cf.as_completed(futs):
            results.append(f.result())
    order = [n for n, _ in todo] + ["rebuild"]
    results.sort(key=lambda r: order.index(r[0]) if r[0] in order else 99)
    for name, level, secs, lines, code in results:
        print("%-4s  %-11s %5.0fs  exit %d%s" % (level, name, secs, code, ("  " + lines[0][:150]) if lines else ""))
        for l in lines[1:]:
            print("      %-11s        %s" % ("", l[:150]))
    fails = [r for r in results if r[1] == "FAIL"]
    print("%s  %s: %d gates in %.0fs wall, %d FAIL, %d WARN" % (
        "PASS" if not fails else "FAIL", os.path.basename(d), len(results), time.time() - t0, len(fails),
        sum(1 for r in results if r[1] == "WARN")))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
