"""task8 architecture 18: the independent verifier. Reads only target/ (no generator state), conforms the files on
its own code path and recomputes every graded figure, then compares them with figures.json at the precision the
prompt asks for. Exit 0 when everything reproduces."""
import csv
import datetime as dt
import json
import os
import sys
import zipfile
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
FIG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "figures.json")

S = lambda x: 1.0 / (1.0 + np.exp(-x))


def read_csv(name):
    with open(os.path.join(TARGET, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_layouts(name):
    """Paper layouts from the workbook's own XML (no generator helper): sheet name -> list of item codes."""
    z = zipfile.ZipFile(os.path.join(TARGET, name))
    wb = z.read("xl/workbook.xml").decode()
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    sst = re.findall(r"<si>(?:<t[^>]*>)(.*?)</t></si>", z.read("xl/sharedStrings.xml").decode())
    rid = dict(re.findall(r'<Relationship[^>]*?Id="(rId\d+)"[^>]*?Target="([^"]+)"', rels))
    rid.update({a: b for b, a in re.findall(r'<Relationship[^>]*?Target="([^"]+)"[^>]*?Id="(rId\d+)"', rels)})
    out = {}
    for nm, r in re.findall(r'<sheet[^>]*?name="([^"]+)"[^>]*?r:id="(rId\d+)"', wb):
        xml = z.read("xl/" + rid[r].lstrip("/").replace("xl/", "")).decode()
        cells = re.findall(r'<c r="([A-Z]+)(\d+)"[^>]*?(?: t="(\w+)")?[^>]*?>(?:<v>([^<]*)</v>)?', xml)
        rows = {}
        for col, rn, t, v in cells:
            val = sst[int(v)] if t == "s" else v
            rows.setdefault(int(rn), {})[col] = val
        out[nm] = [rows[k]["B"] for k in sorted(rows) if k > 1]
    return out


def conform():
    lay = read_layouts("pacb_paper_layouts_2022_2027.xlsx")
    papers = {}
    for nm, codes in lay.items():
        lv, y = nm.split()
        papers["%s-%s" % (lv, y)] = codes
    bank = {}
    for r in read_csv("pacb_item_bank_2026.csv"):
        if r["run"] == "2026-10 final":
            bank[r["item"]] = dict(pool=r["pool"], context=r["context"], words=int(r["stem_words"]),
                                   b=float(r["difficulty_logits"]))
    latest = {}
    meta = {}
    for r in read_csv("pacb_numeracy_responses_2022_2026.csv"):
        paper = r["paper"]
        item = r["item"]
        if item.startswith("Q"):
            item = papers[paper][int(item[1:]) - 1]
        key = (r["sitting_id"], item)
        t = r["answered_utc"]
        if key not in latest or t > latest[key][0]:
            latest[key] = (t, int(r["score"]))
        meta[r["sitting_id"]] = (r["candidate_id"], paper)
    return papers, bank, latest, meta


def matrix(sids, items, latest):
    si = {s: k for k, s in enumerate(sids)}
    ii = {c: k for k, c in enumerate(items)}
    X = np.full((len(sids), len(items)), np.nan)
    for (s, c), (_, v) in latest.items():
        if s in si and c in ii:
            X[si[s], ii[c]] = v
    return X


def jml(X, anchor_cols, anchor_mean, off=None, iters=400, b0=None):
    M = (~np.isnan(X)).astype(float)
    Z = np.nan_to_num(X)
    off = np.zeros(X.shape) if off is None else off
    raw, cnt = (Z * M).sum(1), M.sum(1)
    keep = (raw > 0) & (raw < cnt)
    Zk, Mk, Ok = Z[keep], M[keep], off[keep]
    b = np.zeros(X.shape[1]) if b0 is None else b0.copy()
    th = np.zeros(Zk.shape[0])
    for _ in range(iters):
        p = S(th[:, None] - b[None, :] - Ok)
        th2 = np.clip(th + ((Zk - p) * Mk).sum(1) / np.maximum((p * (1 - p) * Mk).sum(1), 1e-9), -6, 6)
        p = S(th2[:, None] - b[None, :] - Ok)
        b2 = np.clip(b - ((Zk - p) * Mk).sum(0) / np.maximum((p * (1 - p) * Mk).sum(0), 1e-9), -6, 6)
        sh = b2[anchor_cols].mean() - anchor_mean
        b2, th2 = b2 - sh, th2 - sh
        d = max(abs(b2 - b).max(), abs(th2 - th).max())
        b, th = b2, th2
        if d < 1e-7:
            break
    p = S(th[:, None] - b[None, :] - Ok)
    se = 1 / np.sqrt(np.maximum((p * (1 - p) * Mk).sum(0), 1e-9))
    full = np.full(X.shape[0], np.nan)
    full[keep] = th
    return b, se, full


def wle(X, b, off):
    M = (~np.isnan(X)).astype(float)
    Z = np.nan_to_num(X)
    th = np.zeros(X.shape[0])
    for _ in range(60):
        p = S(th[:, None] - b[None, :] - off)
        q = p * (1 - p) * M
        inf = q.sum(1)
        g = ((Z - p) * M).sum(1) + (q * (1 - 2 * p)).sum(1) / np.maximum(2 * inf, 1e-9)
        th = np.clip(th + g / np.maximum(inf, 1e-9), -6, 6)
    return th


def solve(bs, target):
    lo, hi = -8.0, 8.0
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if S(m - bs).sum() < target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def main():
    fig = json.load(open(FIG))
    papers, bank, latest, meta = conform()
    s1 = sorted(s for s, (c, p) in meta.items() if p.startswith("LN1"))
    s2 = sorted(s for s, (c, p) in meta.items() if p.startswith("LN2"))
    i1 = sorted({c for nm, cs in papers.items() if nm.startswith("LN1") and not nm.endswith("2027") for c in cs})
    i2 = sorted({c for nm, cs in papers.items() if nm.startswith("LN2") for c in cs})
    X1, X2 = matrix(s1, i1, latest), matrix(s2, i2, latest)
    ref = [i1.index(c) for c in papers["LN1-2022"]]
    b1, se1, _ = jml(X1, ref, -0.96)
    b2, se2, _ = jml(X2, [i2.index(c) for c in papers["LN2-2022"]], 0.50)
    shared = [c for c in i1 if bank[c]["pool"] == "Level 2"]
    d = np.array([b1[i1.index(c)] - b2[i2.index(c)] for c in shared])
    se = np.array([np.hypot(se1[i1.index(c)], se2[i2.index(c)]) for c in shared])
    words = np.array([bank[c]["words"] for c in shared], float)
    ev = np.array([bank[c]["context"] == "everyday" for c in shared], float)
    A = np.column_stack([np.ones_like(d), words / 100.0, -ev])
    wgt = np.sqrt(1 / se ** 2)
    coef = np.linalg.lstsq(A * wgt[:, None], d * wgt, rcond=None)[0]
    p27 = papers["LN1-2027"]
    b27 = []
    for c in p27:
        if c in i1:
            b27.append(b1[i1.index(c)])
        else:
            b27.append(b2[i2.index(c)] + coef[0] + coef[1] * bank[c]["words"] / 100.0 - coef[2] * (bank[c]["context"] == "everyday"))
    b27 = np.array(b27)
    th = solve(np.array([b1[k] for k in ref]), 26)
    e = float(S(th - b27).sum())
    # the bank's own route
    bb = np.array([bank[c]["b"] for c in papers["LN1-2022"]])
    thb = solve(bb, 26)
    eb = float(S(thb - np.array([bank[c]["b"] for c in p27])).sum())
    ok = []

    def chk(name, got, want, tol):
        good = abs(got - want) <= tol
        ok.append(good)
        print("%-34s %-10s figures %-10s %s" % (name, ("%.3f" % got), str(want), "ok" if good else "MISMATCH"))
    chk("pass mark", int(round(e)), fig["pass_mark"], 0)
    chk("expected mark (golden)", e, fig["expected_golden"], 0.005)
    chk("expected mark (bank)", eb, fig["expected_bank"], 0.005)
    chk("pass mark (bank)", int(round(eb)), fig["pass_mark_bank"], 0)
    chk("reading cost per 100 words", coef[1], fig["reading_cost_per_100_words"], 0.005)
    chk("everyday advantage", coef[2], fig["everyday_advantage"], 0.005)
    ch = {("Q%02d" % (k + 1)): float(S(th - b27[k])) for k in range(len(p27))}
    for q, v in fig["chances"].items():
        chk("chance " + q, round(ch[q], 2), v, 0.0)
    below = [q for q, v in ch.items() if v < 0.20]
    above = [q for q, v in ch.items() if v > 0.90]
    ok.append(below == fig["items_below_band"] and above == fig["items_above_band"])
    print("band: below %s above %s %s" % (below, above, "ok" if ok[-1] else "MISMATCH"))
    # regions: the register's sitting centre for each 2026 Level 1 sitting, the centre's region
    reg_of = {r["centre"]: r["region_name"] for r in read_csv("pacb_learning_centres.csv")}
    sat = {}
    for r in read_csv("pacb_candidate_register_2022_2026.csv"):
        if r["status"] == "Sat" and r["candidate_id"]:
            lv = "LN1" if r["level"] in ("Level 1", "L1") else "LN2"
            sat[(r["candidate_id"], "%s-%s" % (lv, r["paper_year"]))] = r["sat_at"]
    region = {s: reg_of[sat[(c, p)]] for s, (c, p) in meta.items()}
    regs = sorted(set(reg_of.values()))
    rj = np.array([regs.index(region[s]) for s in s1])
    evi = np.array([bank[c]["context"] == "everyday" for c in i1], float)
    share = np.bincount(rj, minlength=len(regs)) / len(rj)
    delta = np.zeros(len(regs))
    br = b1.copy()
    for _ in range(12):
        off = -delta[rj][:, None] * evi[None, :]
        br, _, thr = jml(X1, ref, -0.96, off=off, iters=200, b0=br)
        M = (~np.isnan(X1)).astype(float)
        Z = np.nan_to_num(X1)
        okp = ~np.isnan(thr)
        p = S(np.nan_to_num(thr)[:, None] - br[None, :] - off)
        g = (Z - p) * M * evi[None, :]
        h = p * (1 - p) * M * evi[None, :]
        for k in range(len(regs)):
            sel = okp & (rj == k)
            delta[k] += g[sel].sum() / max(h[sel].sum(), 1e-9)
        delta -= (share * delta).sum()
    dr = np.array([br[i1.index(c)] - b2[i2.index(c)] for c in shared])
    cr = np.linalg.lstsq(A * wgt[:, None], dr * wgt, rcond=None)[0]
    b27r = np.array([br[i1.index(c)] if c in i1 else b2[i2.index(c)] + cr[0] + cr[1] * bank[c]["words"] / 100.0
                     for c in p27])
    ev27 = np.array([bank[c]["context"] == "everyday" for c in p27], float)
    s26 = [s for s in s1 if meta[s][1] == "LN1-2026"]
    p26 = papers["LN1-2026"]
    X26 = np.full((len(s26), len(i1)), np.nan)
    for k, s in enumerate(s26):
        for c in p26:
            X26[k, i1.index(c)] = latest[(s, c)][1]
    r26 = np.array([regs.index(region[s]) for s in s26])
    th26 = wle(X26, br, -delta[r26][:, None] * evi[None, :])
    e26 = np.array([S(th26[k] - b27r + delta[r26[k]] * ev27).sum() for k in range(len(s26))])
    for k, nm in enumerate(regs):
        if nm in fig["regions"]:
            chk("region " + nm, int(round(float(e26[r26 == k].mean()))), fig["regions"][nm], 0.0)
    print("verify: %d of %d reproduce" % (sum(ok), len(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
