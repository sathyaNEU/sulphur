"""A second implementation of the estimate, from the shipped files alone and sharing no code with core.py, load.py or
results.py: plain rows and dictionaries, the steps as the answer blocks state them, each file found by its name and
read in its own layout.

    python3 task8/generator/verify.py [target]
"""
import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = "Carrow"
BANKED = (2025, 2026)
LAST = 2026
NINE = 9
TOKEN = [("carrow", "Carrow"), ("ardkeel", "Ardkeel"), ("dunmoyle", "Dunmoyle"), ("brn", "Brannock"), ("fen", "Fennor"),
         ("eskerryeb", "Eskerry"), ("gortavaleeb", "Gortavale")]
KIND = [("portfoliomark", "marks"), ("moderationsample", "samples"), ("moderationoutcome", "outcomes"),
        ("scripts", "scripts"), ("standardisationmarks", "trial"), ("stdmeetingmarks", "trial")]


def files(target):
    """{board: {kind: path}} and the other files by a word of their name."""
    out, other = defaultdict(dict), {}
    for name in sorted(os.listdir(target)):
        flat = re.sub(r"[ _\-]", "", name.lower())
        board = [b for t, b in TOKEN if flat.startswith(t)]
        kind = [k for t, k in KIND if t in flat]
        if board and kind:
            out[board[0]][kind[0]] = os.path.join(target, name)
        else:
            other[name] = os.path.join(target, name)
    return out, other


def rows(path):
    if path.endswith(".xlsx"):
        ws = load_workbook(path, read_only=True, data_only=True).worksheets[0]
        it = ws.iter_rows(values_only=True)
        next(it)
        for r in it:
            yield ["" if v is None else str(v) for v in r]
    else:
        with open(path, newline="") as fh:
            head = fh.readline()
            for r in csv.reader(fh, delimiter=";" if head.count(";") > head.count(",") else ","):
                yield r


def year(s):
    return int(str(s).strip()[-4:])


def pdf_text(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout)


def documents(target):
    """What the three documents file, read back from the PDFs."""
    _, other = files(target)
    pick = lambda w: pdf_text([p for n, p in other.items() if w in n and n.endswith(".pdf")][0])  # noqa: E731
    prot, code, scope = pick("protocol"), pick("code_of_practice"), pick("scope")
    line = re.search(r"distance is (\d+\.\d) marks or more above", prot)
    series = re.search(r"in the (\d{4}) series or the (\d{4}) series", prot)
    sched = {m.group(1): (int(m.group(2)), int(m.group(3)))
             for m in re.finditer(r"(\w+) (?:Examining Board|Awards) (\d) (\d)\b", code)}
    per = re.search(r"draw (\w+) portfolios from each centre", scope)
    return dict(protocol=prot, code=code, scope=scope, line=float(line.group(1)) if line else None,
                series=tuple(int(v) for v in series.groups()) if series else None, schedule=sched,
                review_per_centre=per.group(1) if per else None)


def read(target, first_version=False, keep_repeats=False, count_unmarked=False, fill_blank=False):
    by_board, other = files(target)
    centres = defaultdict(dict)
    with open(other["centre_register.csv"], newline="") as fh:
        for r in csv.DictReader(fh):
            centres[r["board"]][r["board_centre_no"]] = int(r["roll_no"])
            centres[r["board"]][r["roll_no"]] = int(r["roll_no"])
    B = {}
    for b, F in by_board.items():
        roll = centres[b]
        # ---- the mark sheets
        n, sc, sa, seen, raw = Counter(), Counter(), Counter(), set(), 0
        for r in rows(F["marks"]):
            raw += 1
            key = (year(r[0]), roll[r[1].strip()], int(r[2]))
            if key in seen and not keep_repeats:
                continue
            seen.add(key)
            if r[4].strip() == "":
                if count_unmarked:
                    n[key[1], key[0]] += 1
                continue
            n[key[1], key[0]] += 1
            sc[key[1], key[0]] += int(r[4])
            sa[key[1], key[0]] += int(r[5])
        # ---- the samples
        sample = defaultdict(dict)
        who = {}
        if "outcomes" in F:
            for r in rows(F["samples"]):
                k = (roll[r[1].strip()], year(r[0]))
                sample[k][int(r[2])] = (int(r[3]), int(r[4]))
                who[k] = r[5]
        else:
            best = {}
            for r in rows(F["samples"]):
                k = (roll[r[1].strip()], year(r[0]))
                v = int(r[10])
                if k not in best or (v < best[k][0] if first_version else v > best[k][0]):
                    best[k] = (v, r)
            for k, (_v, r) in best.items():
                for cd, cm, mm in zip(r[4].split("|"), r[5].split("|"), r[6].split("|")):
                    sample[k][int(cd)] = (int(cm), int(mm))
                who[k] = r[2]
        # ---- the standardisation meetings
        marks = defaultdict(list)
        blank, own = [], defaultdict(list)
        for r in rows(F["trial"]):
            k = (year(r[0]), r[1].strip())
            if r[3].strip() == "":
                blank.append((k, r[2].strip()))
                continue
            marks[k].append((r[2].strip(), float(r[3])))
            own[r[2].strip(), k[0]].append(float(r[3]))
        if fill_blank:                       # a mark not given, filled with that marker's mean at the meeting
            for k, who_ in blank:
                marks[k].append((who_, sum(own[who_, k[0]]) / len(own[who_, k[0]])))
        scripts = []
        for r in rows(F["scripts"]):
            k = (year(r[0]), r[1].strip())
            cons = sum(m for _, m in marks[k]) / len(marks[k])
            cm, mm = sample[roll[r[3].strip()], year(r[2])][int(r[4])]
            scripts.append(dict(meeting=k[0], x=cm - cons, y=cm - mm, gap=cons - int(r[5]), cons=cons, key=k))
        cons = {s["key"]: s["cons"] for s in scripts}
        dev = defaultdict(list)
        for k, lst in marks.items():
            if k in cons:
                for who_, m in lst:
                    dev[who_, k[0]].append(m - cons[k])
        B[b] = dict(n=n, sc=sc, sa=sa, sample=sample, who=who, scripts=scripts, rolls=sorted(set(roll.values())),
                    dev={k: sum(v) / len(v) for k, v in dev.items()}, raw=raw, rows=len(seen))
    reg = defaultdict(list)
    with open(other["moderator_register_2020_2026.csv"], newline="") as fh:
        for r in csv.DictReader(fh):
            reg[r["registration_no"]].append((r["board"], int(r["first_series"]), int(r["last_series"] or LAST)))
    review = defaultdict(list)
    with open(other["oer_review_2023_dunmoyle_portfolio_marks.csv"], newline="") as fh:
        for r in csv.DictReader(fh):
            review[int(r["roll_no"])].append(int(r["centre_mark"]) - int(r["review_mark"]))
    return B, reg, {k: sum(v) / len(v) for k, v in review.items()}, sum(len(v) for v in review.values())


def fit(B, reg):
    """The three fitted inputs: each board's share, its levels by years since a sample and its standard."""
    share, rota, cycle, gap, last = {}, {}, {}, {}, {}
    for b, w in B.items():
        x = np.array([s["x"] for s in w["scripts"]])
        y = np.array([s["y"] for s in w["scripts"]])
        share[b] = float(np.cov(x, y, bias=True)[0, 1] / np.var(x))
        gap[b] = float(np.mean([s["gap"] for s in w["scripts"]]))
        yrs = defaultdict(list)
        for (r, t) in w["sample"]:
            yrs[r].append(t)
        gaps = Counter(d for v in yrs.values() for d in np.diff(sorted(v)))
        k = rota[b] = int(gaps.most_common(1)[0][0]) if gaps else 1
        last[b] = {r: sorted(v) for r, v in yrs.items()}
        if k == 1:
            cycle[b] = [0.0]
            continue
        # each centre's mean mark by years since its last sample, within centre and net of the year, the last nine series
        window = list(range(LAST - NINE + 1, LAST + 1))
        cen = w["rolls"]
        m = np.array([[w["sc"][r, t] / w["n"][r, t] for t in window] for r in cen])
        since = np.array([[t - max(v for v in last[b][r] if v <= t) for t in window] for r in cen])
        within = lambda a: a - a.mean(1, keepdims=True) - a.mean(0, keepdims=True) + a.mean()  # noqa: E731
        D = np.stack([within((since == j).astype(float)).ravel() for j in range(1, k)], 1)
        th = np.linalg.solve(D.T @ D, D.T @ within(m).ravel())
        cycle[b] = [0.0] + [float(v) for v in th]
    # ---- the standards: people appointed by two boards in a series, read on both boards' meetings
    pair = defaultdict(list)
    for who, apps in reg.items():
        for i in range(len(apps)):
            for j in range(i + 1, len(apps)):
                (a, a0, a1), (c, c0, c1) = sorted([apps[i], apps[j]])
                if a == c:
                    continue
                for t in range(max(a0, c0), min(a1, c1) + 1):
                    if (who, t) in B[a]["dev"] and (who, t) in B[c]["dev"]:
                        pair[a, c].append(B[a]["dev"][who, t] - B[c]["dev"][who, t])   # consensus of c less consensus of a
    names = [b for b in B if b != HOME]
    ix = {b: i for i, b in enumerate(names)}
    A, rhs = np.zeros((len(names), len(names))), np.zeros(len(names))
    for (a, c), d in pair.items():
        row = np.zeros(len(names))
        if c != HOME:
            row[ix[c]] = 1
        if a != HOME:
            row[ix[a]] = -1
        A += len(d) * np.outer(row, row)
        rhs += len(d) * row * float(np.mean(d))
    sol = np.linalg.solve(A, rhs)
    standard = {b: float(sol[ix[b]]) - (gap[b] - gap[HOME]) for b in names}
    standard[HOME] = 0.0
    return dict(share=share, rota=rota, cycle=cycle, gap=gap, last=last, standard=standard,
                links={k: (len(v), float(np.mean(v))) for k, v in pair.items()})


def centre(B, F, b, t, use_share=True, use_cycle=True, use_link=True):
    """{roll: (candidates, marks above Carrow's standard, sampled)} for one board and series."""
    w = B[b]
    sh = F["share"][b] if use_share else 1.0
    off = F["standard"][b] if use_link else 0.0
    out = {}
    for r in w["rolls"]:
        n = w["n"][r, t]
        if not n:
            continue
        diff = lambda u: sum(c - m for c, m in w["sample"][r, u].values()) / len(w["sample"][r, u])  # noqa: E731
        if (r, t) in w["sample"]:
            lev = diff(t) / sh - (w["sc"][r, t] - w["sa"][r, t]) / n
            out[r] = (n, off + lev, True)
        else:
            u = max(v for v in F["last"][b][r] if v < t)
            out[r] = (n, off + diff(u) / sh + (F["cycle"][b][t - u] if use_cycle else 0.0), False)
    return out


def run(target, lost=(), **how):
    B, reg, review, review_rows = read(target, **how)
    F = fit(B, reg)
    flags = dict(use_share="S1" not in lost, use_cycle="S2" not in lost, use_link="S3" not in lost)
    members = [b for b in B if b != HOME]
    mean = lambda c: sum(n * v for n, v, _ in c.values()) / sum(n for n, _, _ in c.values())  # noqa: E731
    cen = {(b, t): centre(B, F, b, t, **flags) for b in members for t in BANKED}
    by = {t: {b: mean(cen[b, t]) for b in members} for t in BANKED}
    cand = {b: {t: sum(n for n, _, _ in cen[b, t].values()) for t in BANKED} for b in members}
    pool = {b: sum(cand[b][t] * by[t][b] for t in BANKED) / sum(cand[b].values()) for b in members}
    tot = {b: sum(cand[b].values()) for b in members}
    whole = sum(tot[b] * pool[b] for b in members) / sum(tot.values())
    docs = documents(target)
    line = docs["line"]
    word = lambda v: "down" if v >= line else ("up" if v <= -line else "as banked")  # noqa: E731
    # ---- the review, on the centres its board did not sample in its series
    rb, ry = "Dunmoyle", 2023
    c23 = centre(B, F, rb, ry, **flags)
    un = [r for r, (_n, _v, s) in c23.items() if not s]
    wn = sum(c23[r][0] for r in un)
    w = B[rb]
    adj = lambda r: (w["sc"][r, ry] - w["sa"][r, ry]) / w["n"][r, ry]  # noqa: E731
    return dict(
        share={b: F["share"][b] for b in B}, cycle=F["cycle"], rota=F["rota"], standard=F["standard"], gap=F["gap"],
        links=F["links"], by=by, pool=pool, whole=whole, call=["%s %s" % (b, word(pool[b])) for b in sorted(members)],
        candidates=cand, centre=cen, docs=docs,
        referee=dict(review=sum(c23[r][0] * (review[r] - adj(r)) for r in un) / wn,
                     estimate=sum(c23[r][0] * c23[r][1] for r in un) / wn, centres=len(un),
                     all_centres=sum(c23[r][0] * (review[r] - adj(r)) for r in c23) / sum(v[0] for v in c23.values())),
        rows={b: B[b]["rows"] for b in B}, raw_rows={b: B[b]["raw"] for b in B}, review_rows=review_rows,
        scripts={b: len(B[b]["scripts"]) for b in B})


def compare(v, fig):
    """Every figure the verifier shares with figures.json: (label, verifier, figures.json, agrees)."""
    out = []
    add = lambda lab, a, c, tol=0.006: out.append((lab, round(float(a), 4), c, abs(float(a) - float(c)) <= tol))  # noqa: E731
    for b in fig["distance_2dp"]:
        add("distance %s" % b, v["pool"][b], fig["distance_2dp"][b])
        add("standard %s" % b, v["standard"][b], fig["standard"][b])
        for t in BANKED:
            add("%d %s" % (t, b), v["by"][t][b], fig["by_series"][str(t)][b], 0.051)
    for b in fig["share_pct"]:
        add("share %s" % b, 100 * v["share"][b], fig["share_pct"][b], 0.051)
        add("consensus less agreed %s" % b, v["gap"][b], fig["agreed_gap"][b])
        for j, c in enumerate(fig["cycle"][b]):
            add("level %d after a sample %s" % (j + 1, b), v["cycle"][b][j + 1], c)
        add("mark sheet rows %s" % b, v["rows"][b], fig["mark_rows"][b], 0)
    add("whole", v["whole"], fig["whole_2dp"])
    add("review", v["referee"]["review"], fig["referee"]["review"])
    add("review, the estimate", v["referee"]["estimate"], fig["referee"]["golden"])
    add("review, every centre", v["referee"]["all_centres"], fig["referee"]["raw_all_centres"])
    out.append(("the call", v["call"], fig["call"], v["call"] == sorted(fig["call"])))
    return out


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    v = run(tgt)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    res = compare(v, fig)
    for lab, a, c, good in res:
        if not good:
            print("DIFF  %s  verifier %s  figures.json %s" % (lab, a, c))
    print("verify: %d figures compared, %d differ; call %s" % (len(res), sum(not r[3] for r in res), "; ".join(v["call"])))
    sys.exit(1 if any(not r[3] for r in res) else 0)
