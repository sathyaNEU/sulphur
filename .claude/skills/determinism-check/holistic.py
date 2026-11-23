#!/usr/bin/env python3
"""holistic.py, the platform's Holistic Audit v4 filled from one task folder, in a workspace of its own.

    python3 .claude/skills/determinism-check/holistic.py taskNN                      # holistic mode (both runs saved)
    python3 .claude/skills/determinism-check/holistic.py taskNN --mode determinism   # stage 4, before the runs
    python3 .claude/skills/determinism-check/holistic.py taskNN --out /path/to/empty/dir
    python3 .claude/skills/determinism-check/holistic.py taskNN --check                 # the inputs only, no workspace

The v4 text is the client's (guidelines/client/quality-checks/holistic-audit-v4-2026-11-22.md) and is never retyped:
this script cuts the system prompt out of that file and fills its {{variables}} the way the platform does, from
prompt.txt, a fresh unzip of target.zip, the four answer fields of submission.md (Final Recommendation,
Supplementary Questions, Critical Components, Step-by-Step; never the Tags or the stump answer) and, in holistic
mode, both saved responses with the files each run produced. The golden deliverables are never copied: the audit
does not receive them.

Holistic mode fills the whole audit (Step 0 to the rubric example). Determinism mode, for the pre-platform pass,
keeps the audit's opening, Step 0, Part A and Part B and leaves the runs out, so Part B's reading of the runs and
its convention check wait for the holistic pass.

The workspace holds inputs/ (the pack as the solver gets it), run1_files/ and run2_files/ (holistic mode), work/
(empty, for the auditor's scripts), audit_prompt.md (the filled audit) and manifest.json (what was supplied, with
md5s, so a verdict is scoped to the cut it saw). It spawns nothing and costs nothing; the determinism-judge agent
runs the audit on it.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CLIENT = os.path.join(REPO, "guidelines", "client", "quality-checks", "holistic-audit-v4-2026-11-22.md")
START = "# Holistic Audit v4 (agentic, with rubric): Project Sulfur"
END = "Copy"
FIELDS = [  # placeholder, the submission.md heading it comes from
    ("final_recommendation", "final recommendation"),
    ("supplementary_answers", "supplementary questions"),
    ("critical_components", "critical components"),
    ("step_by_step_solution", "step-by-step"),
]
PAIRS = [("run1.md", "run2.md"), ("response1.md", "response2.md"), ("response_1.md", "response_2.md")]


def die(msg):
    print("holistic.py: %s" % msg)
    sys.exit(2)


def task_dir(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    return os.path.join(REPO, "task%s" % m.group(1)) if m else os.path.abspath(arg)


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def template():
    lines = open(CLIENT, encoding="utf-8").read().splitlines()
    try:
        a = lines.index(START)
        b = lines.index(END, a)
    except ValueError:
        die("the v4 markers (%r ... %r) are not in %s" % (START, END, CLIENT))
    text = "\n".join(lines[a:b]).rstrip() + "\n"
    for name in ["prompt", "input_files"] + [f for f, _ in FIELDS] + [
            "response_1", "response_1_files", "response_2", "response_2_files"]:
        if "{{%s}}" % name not in text:
            die("the v4 template has no {{%s}}" % name)
    return text


def determinism_cut(text):
    """The audit's opening, Step 0, Part A and Part B, with the runs left out (the pre-platform pass)."""
    runs = text.index("## Model runs")
    step0 = text.index("## Step 0")
    partc = text.index("## Part C")
    note = ("## Model runs\n"
            "None yet: this is the pre-platform pass, run before the platform generates the two responses. Part B "
            "step 3's reading of the runs and step 5's convention check wait for the holistic pass; every other step "
            "of Step 0, Part A and Part B applies in full.\n\n")
    return text[:runs] + note + text[step0:partc].rstrip() + "\n"


def blocks(path):
    """The submission.md sections by their '## ' heading, lower-cased."""
    out, cur, buf = {}, None, []
    for line in open(path, encoding="utf-8").read().splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1).strip().lower(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return out


def field(secs, want):
    for name, body in secs.items():
        if name.startswith(want):
            return name, body
    return None, ""


def strip_house_header(text):
    """A saved response may open on the house's own comment line (who pasted it, when); the platform's text follows."""
    return re.sub(r"\A(\s*<!--.*?-->\s*)+", "", text, flags=re.S).strip()


def find_pair(d):
    runs = os.path.join(d, "runs")
    try:
        files = json.load(open(os.path.join(d, "pipeline.json"))).get("runs", {}).get("files") or []
        if len(files) == 2 and all(os.path.isfile(os.path.join(d, f)) for f in files):
            return [os.path.join(d, f) for f in files], "pipeline.json runs.files"
    except Exception:
        pass
    for a, b in PAIRS:
        pa, pb = os.path.join(runs, a), os.path.join(runs, b)
        if os.path.isfile(pa) and os.path.isfile(pb):
            return [pa, pb], "runs/%s and runs/%s" % (a, b)
    return None, None


def safe_unzip(zpath, dest):
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            name = info.filename
            if name.startswith("/") or ".." in name.split("/"):
                die("target.zip holds an unsafe path: %s" % name)
        z.extractall(dest)


def listing(root, base):
    rows = []
    for r, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            rows.append((os.path.relpath(p, base), os.path.getsize(p)))
    rows.sort()
    return rows


def human(n):
    for unit in ("bytes", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%d %s" % (n, unit)) if unit == "bytes" else ("%.1f %s" % (n, unit))
        n /= 1024.0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task")
    ap.add_argument("--mode", choices=("holistic", "determinism"), default="holistic")
    ap.add_argument("--out", help="an empty directory for the workspace (default: a new temporary one)")
    ap.add_argument("--check", action="store_true",
                    help="check the inputs the audit needs (the four blocks, the pair, a readable target.zip) and exit")
    a = ap.parse_args(argv)

    d = task_dir(a.task)
    t = os.path.basename(d)
    for need in ("prompt.txt", "target.zip", "submission.md"):
        if not os.path.isfile(os.path.join(d, need)):
            die("%s has no %s" % (t, need))

    secs = blocks(os.path.join(d, "submission.md"))
    fill = {"prompt": open(os.path.join(d, "prompt.txt"), encoding="utf-8").read().strip()}
    used = []
    for key, want in FIELDS:
        name, body = field(secs, want)
        if not name or not body:
            die("submission.md has no '## %s' block with text (the audit's Step 0 would fail: NO GOLDEN)" % want)
        fill[key] = body
        used.append(name)
    left_out = [n for n in secs if n not in used]

    pair, where = (None, None)
    if a.mode == "holistic":
        pair, where = find_pair(d)
        if not pair:
            die("%s has no saved pair under runs/ (run1.md and run2.md, or response1.md and response2.md); the "
                "holistic pass needs both responses, and the pre-platform pass is --mode determinism" % t)

    if a.check:
        with zipfile.ZipFile(os.path.join(d, "target.zip")) as z:
            bad = z.testzip()
            n = sum(1 for i in z.infolist() if not i.is_dir())
        if bad:
            die("target.zip is damaged at %s" % bad)
        print("CHECK PASS  %s, %s mode: %d files in target.zip; answer fields %s; left out: %s%s" % (
            t, a.mode, n, ", ".join(used), ", ".join(left_out) or "nothing",
            ("; pair from %s" % where) if pair else ""))
        return 0

    if a.out:
        ws = os.path.abspath(a.out)
        if os.path.exists(ws) and os.listdir(ws):
            die("--out %s is not empty" % ws)
        os.makedirs(ws, exist_ok=True)
    else:
        ws = tempfile.mkdtemp(prefix="holistic-%s-%s-" % (t, a.mode))
    inputs = os.path.join(ws, "inputs")
    os.makedirs(inputs)
    os.makedirs(os.path.join(ws, "work"))
    safe_unzip(os.path.join(d, "target.zip"), inputs)
    rows = listing(inputs, ws)
    fill["input_files"] = "\n".join("- %s (%s)" % (p, human(n)) for p, n in rows) or "- (target.zip is empty)"

    manifest = {
        "task": t, "mode": a.mode, "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "client_text": os.path.relpath(CLIENT, REPO),
        "md5": {"prompt.txt": md5(os.path.join(d, "prompt.txt")), "target.zip": md5(os.path.join(d, "target.zip")),
                "submission.md": md5(os.path.join(d, "submission.md"))},
        "answer_fields": used, "left_out_of_the_audit": left_out, "input_files": len(rows),
    }

    if a.mode == "holistic":
        texts = []
        for i, p in enumerate(pair, 1):
            texts.append(strip_house_header(open(p, encoding="utf-8").read()))
            stem = os.path.splitext(os.path.basename(p))[0]
            src = os.path.join(os.path.dirname(p), stem + "_files")
            dst = os.path.join(ws, "run%d_files" % i)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
                got = listing(dst, ws)
                fill["response_%d_files" % i] = "\n".join("- %s (%s)" % (q, human(n)) for q, n in got) \
                    or "- (the folder is empty)"
            else:
                os.makedirs(dst)
                got = []
                fill["response_%d_files" % i] = ("None were provided for this run: only its final response was "
                                                 "saved, so grade it from the response alone and say so.")
            fill["response_%d" % i] = texts[-1] or "(empty)"
            manifest["run%d" % i] = {"file": os.path.relpath(p, d), "md5": md5(p), "files": len(got),
                                     "chars": len(texts[-1])}
        manifest["pair_from"] = where
        manifest["duplicate_text"] = texts[0] == texts[1]
        body = template()
    else:
        body = determinism_cut(template())
        for k in ("response_1", "response_1_files", "response_2", "response_2_files"):
            fill.setdefault(k, "")

    filled = re.sub(r"\{\{(\w+)\}\}", lambda m: fill.get(m.group(1), m.group(0)), body)
    left = sorted(set(re.findall(r"\{\{(\w+)\}\}", body)) - set(fill))
    if left:
        die("unfilled placeholders: %s" % ", ".join(left))
    open(os.path.join(ws, "audit_prompt.md"), "w", encoding="utf-8").write(filled)
    json.dump(manifest, open(os.path.join(ws, "manifest.json"), "w"), indent=1)

    print("workspace   %s" % ws)
    print("audit       %s (%s mode, %d characters)" % (os.path.join(ws, "audit_prompt.md"), a.mode, len(filled)))
    print("inputs      %d files under inputs/" % len(rows))
    print("answer      %s; left out: %s" % (", ".join(used), ", ".join(left_out) or "nothing"))
    if a.mode == "holistic":
        print("runs        %s; files: run 1 %d, run 2 %d%s" % (
            where, manifest["run1"]["files"], manifest["run2"]["files"],
            "; THE TWO RESPONSES ARE IDENTICAL" if manifest["duplicate_text"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
