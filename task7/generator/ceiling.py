"""task7: the ask layer's ceiling measured on the cut pack (supplemental-stumping Part 0 and Part 5).

Every route a run can take is scored on the same rubric model (38 main side, 7 instruction-following, 55 asks), each
ask cell counted once: the two fall-back intakes (set and write-off each) and the five envelope rows (set and write-off
each), fourteen cells. The landed run takes the deep step with the clean comparison and cleans every mess item; the
shallow run is the default path (each borrower's own expected write-off). The landed variants a careful run can also
take (the dependants' own PDs as the baseline, the raw rise with no baseline, the less dependent payees of the same
failing payers as the comparison, Matai's dependants priced but not Ridgeway's) are scored too, and the pair is the
worst honest one: the clean landed run beside the shallow run. Every route reads target/ only."""
import hashlib
import json
import math
import os
import re
import subprocess
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD  # noqa: E402

T = os.path.join(os.path.dirname(HERE), "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
MAIN, IF, ASKS = 38.0, 7.0, 55.0
PARTIAL = 5.0          # Part 0: the partial credit a run off the call collects on the main side


def rnd(x, u):
    return int(math.floor(x / u + 0.5)) * u


def digest():
    h = hashlib.md5()
    for f in sorted(os.listdir(T)):
        h.update(f.encode())
        h.update(open(os.path.join(T, f), "rb").read())
    return h.hexdigest()


wl = subprocess.run(["pdftotext", "-layout", os.path.join(T, "watch_list_2027-01.pdf"), "-"],
                    capture_output=True, text=True).stdout
LINES = {}
for ln in wl.splitlines():
    m = re.match(r"\s*(C\d{6})\s", ln)
    amts = re.findall(r"\d{1,3}(?:,\d{3})+", ln)
    if m and len(amts) >= 2:
        LINES[m.group(1)] = float(amts[-1].replace(",", ""))
wb = openpyxl.load_workbook(os.path.join(T, "customer_master_2026-12.xlsx"), read_only=True)
NAME = {r[0]: r[1].replace(" Limited", "") for r in list(wb["Customers"].iter_rows(values_only=True))[1:]}
P = GD.Pack(T, LINES)
ENV = FIG["envelope"]
p1 = P.p1(0.30)[0]
p0 = P.p0(0.30)[0]


def label(s):
    ns = sorted(NAME[c] for c in s)
    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]


GOLD_CALL = set(FIG["call_ids"])
GOLD_CELLS = {}
for b, x in FIG["fallback"].items():
    GOLD_CELLS["fall-back set, %s out" % b] = x["intake"]
    GOLD_CELLS["fall-back write-off, %s out" % b] = x["kept_off"]
for x in FIG["envelope_curve"]:
    GOLD_CELLS["envelope %s set" % format(x["envelope"], ",")] = x["intake"]
    GOLD_CELLS["envelope %s write-off" % format(x["envelope"], ",")] = x["kept_off"]


def route_cells(v):
    """The cells a run files under package values v: it answers the fall-back for the borrowers it takes on itself."""
    call = set(P.best_set(v)[0])
    out = {}
    for b in FIG["fallback"]:
        cid = next(c for c in LINES if NAME[c] == b)
        if cid in call:
            s, t, _, _ = P.best_at(v, ENV, without=(cid,))
            out["fall-back set, %s out" % b] = label(s)
            out["fall-back write-off, %s out" % b] = rnd(t, 50_000)
        else:
            out["fall-back set, %s out" % b] = None
            out["fall-back write-off, %s out" % b] = None
    for x in FIG["envelope_curve"]:
        s, t, _, _ = P.best_at(v, x["envelope"])
        out["envelope %s set" % format(x["envelope"], ",")] = label(s)
        out["envelope %s write-off" % format(x["envelope"], ",")] = rnd(t, 50_000)
    return call, out


def main_side(v, call):
    """The main side on its components: the call 14, the total 10, the three critical components 14 (the dependants
    protected 5, the rise measured on a clean comparison 5, Matai's figure 4). A run off the call keeps the Part 0
    partial credit."""
    if call != GOLD_CALL:
        return PARTIAL
    s = 14.0
    s += 10.0 if rnd(sum(v[c] for c in call), 50_000) == FIG["total_kept_off"] else 0.0
    s += 5.0 + 5.0
    mat = next(c for c in LINES if NAME[c] == "Matai Valley Foods")
    s += 4.0 if rnd(v[mat], 50_000) == FIG["kept_off"]["Matai Valley Foods"] else 0.0
    return s


own = {c: P.own(c) for c in LINES}
below_k = below_n = 0
U = P.borrower_universe()
for a in sorted(P.episodes):
    for s_, _ in P.episodes[a]:
        if not (GD.D(2022, 1, 1) <= s_ <= GD.D(2025, 12, 31)):
            continue
        for p in sorted(U):
            if p == a or a not in P.payers_of[p] or P.in_default(p, s_):
                continue
            sh = P.share(p, a, GD.add_months(GD.D(s_.year, s_.month, 1), -12), GD.D(s_.year, s_.month, 1))
            if 0 < sh < 0.30:
                below_n += 1
                below_k += any(s_ < t <= GD.add_months(s_, 12) for t in P.starts(p))
golden = P.values(p1 - p0)
rid = next(c for c in LINES if NAME[c] == "Ridgeway Precast")
matai_only = dict(golden)
matai_only[rid] = own[rid]
ROUTES = [
    ("landed: the rise against borrowers whose main payer kept trading (golden)", golden, 5.0),
    ("landed: the dependants' own PDs as the baseline", P.values(None, baseline=p1), 5.0),
    ("landed: Matai's dependants priced, Ridgeway's missed", matai_only, 5.0),
    ("landed: the raw rate, no baseline netted", P.values(p1), 0.0),
    ("landed: the less dependent payees of failing payers as the comparison (%d of %d)" % (below_k, below_n),
     P.values(p1 - below_k / below_n), 0.0),
    ("shallow: own twelve-month expected write-off (default path)", own, None),
    ("shallow: own lifetime expected write-off", {c: P.own(c, "pd_lifetime") for c in LINES}, None),
    ("shallow: an assumed rise of 0.25", P.values(0.25), None),
]
if len(LINES) != 8 or not GOLD_CELLS:
    print("ceiling: REFUSED, nothing to measure (watch-list lines %d, ask cells %d)" % (len(LINES), len(GOLD_CELLS)))
    sys.exit(2)

print("pack md5 %s  (%d files)" % (digest(), len(os.listdir(T))))
print("ask cells graded: %d (two fall-backs and %d envelope rows, a set and a write-off each)"
      % (len(GOLD_CELLS), len(FIG["envelope_curve"])))
scores = {}
for lab, v, cc2 in ROUTES:
    call, cells = route_cells(v)
    kept = [k for k in GOLD_CELLS if cells[k] == GOLD_CELLS[k]]
    m = main_side(v, call)
    if call == GOLD_CALL and cc2 == 0.0:
        m -= 5.0        # the rise not measured against a clean comparison: the second component is lost
    sc = m + IF + ASKS * len(kept) / len(GOLD_CELLS)
    scores[lab] = (sc, len(kept), call == GOLD_CALL)
    print("%-92s %s  asks %2d of %d  score %5.1f" % (lab, "on the call " if call == GOLD_CALL else "off the call",
                                                  len(kept), len(GOLD_CELLS), sc))
    missed = [k for k in GOLD_CELLS if k not in kept]
    if missed and lab.startswith("landed"):
        print("    misses: %s" % "; ".join(missed))
    print("    files: %s" % "; ".join("%s: %s" % (k, format(v, ",") if isinstance(v, int) else v)
                                        for k, v in cells.items() if v is not None))
C = scores[ROUTES[0][0]][0]
S = scores[ROUTES[5][0]][0]
Ls = scores[ROUTES[5][0]][1] / len(GOLD_CELLS)
print("Shallow keep: %.1f per cent of ask weight" % (100 * Ls))
print("Landed run (clean comparison) %.1f; shallow run %.1f" % (C, S))
print("Pair ceiling: %.1f" % ((C + S) / 2))
others = [scores[r[0]][0] for r in ROUTES[1:5]]
print("Pairs with a landed run that takes another comparison: %s" % ", ".join("%.1f" % ((x + S) / 2) for x in others))
bad = []
if Ls >= 0.25:
    bad.append("shallow keep at or over a quarter")
if (C + S) / 2 >= 60:
    bad.append("pair at or over the bar")
print("ceiling: %s" % ("PASS (under the bar of 60)" if not bad else "FAIL " + "; ".join(bad)))
sys.exit(1 if bad else 0)
