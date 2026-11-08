"""task7: the independent verifier. Reads only target/ (PDFs through pdftotext) and recomputes the call, every
graded figure and the rates behind them on its own code path, then compares with figures.json."""
import csv
import datetime as dt
import itertools
import json
import math
import os
import re
import subprocess
import sys
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
bad = []


def ok(label, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        bad.append(label)


def num(s):
    return re.sub(r"[^0-9]", "", s)


def r_half(x, u):
    return int(math.floor(x / u + 0.5)) * u


def text(f):
    return subprocess.run(["pdftotext", "-layout", os.path.join(T, f), "-"], capture_output=True, text=True).stdout


def ym(d):
    return d[:7]


def mshift(y, m, k):
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


# ---- documents ---------------------------------------------------------------------------------------------
terms = text("bsu_terms_of_reference_2027.pdf")
ok("terms readable (positive control)", "Business Support Unit" in terms and len(terms) > 1000)
env = re.search(r"NZ\$(\d+\.\d) million of new working-capital lines", terms)
ok("terms file the envelope", bool(env))
ENV = float(env.group(1)) * 1e6
wl = text("watch_list_2027-01.pdf")
LINES = {}
for ln in wl.splitlines():
    m = re.match(r"\s*(C\d{6})\s", ln)
    amts = re.findall(r"\d{1,3}(?:,\d{3})+", ln)
    if m and len(amts) >= 2:
        LINES[m.group(1)] = float(num(amts[-1]))
ok("watch list: eight borrowers with proposed lines", len(LINES) == 8, str(len(LINES)))

# ---- accounts -------------------------------------------------------------------------------------------------
wb = openpyxl.load_workbook(os.path.join(T, "customer_master_2026-12.xlsx"), read_only=True)
NAME = {r[0]: r[1] for r in list(wb["Customers"].iter_rows(values_only=True))[1:]}
OWNER = {num(r[1]): r[0] for r in list(wb["Accounts"].iter_rows(values_only=True))[1:]}
with open(os.path.join(T, "account_number_crosswalk_2023.csv")) as f:
    for r in csv.DictReader(f):
        if num(r["new_account"]) in OWNER:
            OWNER[num(r["legacy_account"])] = OWNER[num(r["new_account"])]
OWN = defaultdict(set)
for a, c in OWNER.items():
    OWN[c].add(a)

# ---- ledger: monthly receipts by payer, and the loan accounts' payers ----------------------------------------
TOT = defaultdict(float)
FROM = defaultdict(float)
LOANS = {}
with open(os.path.join(T, "business_account_transactions_2021-2026.csv")) as f:
    for r in csv.DictReader(f):
        me = OWNER.get(num(r["account_number"]))
        oa = num(r["other_party_account"])
        if r["txn_code"] == "LN" and me:
            LOANS[oa] = me
        if r["dr_cr"] != "CR" or not me or oa in OWN[me] or oa.startswith("471299"):
            continue
        a = float(r["amount_nzd"])
        TOT[(me, ym(r["posting_date"]))] += a
        src = OWNER.get(oa)
        if src and src != me:
            FROM[(me, src, ym(r["posting_date"]))] += a
PAYERS = defaultdict(set)
for (p, a, m) in FROM:
    PAYERS[p].add(a)


def share(p, a, y, m, months):
    keys = ["%04d-%02d" % mshift(y, m, -k) for k in range(1, months + 1)]
    t = sum(TOT.get((p, k), 0.0) for k in keys)
    return sum(FROM.get((p, a, k), 0.0) for k in keys) / t if t else 0.0


# ---- defaults: episodes from the register and cures ---------------------------------------------------------
TRIG = defaultdict(list)
with open(os.path.join(T, "default_register_2021-2026.csv")) as f:
    for r in csv.DictReader(f):
        ref = r["reference"]
        who = ref if ref.startswith("C") else (OWNER.get(num(ref)) or LOANS.get(num(ref)))
        if who:
            TRIG[who].append(dt.date.fromisoformat(r["trigger_date"]))
CURE = {}
with open(os.path.join(T, "default_cures_2021-2026.csv")) as f:
    for r in csv.DictReader(f):
        CURE[(r["customer_no"], r["default_date"])] = dt.date.fromisoformat(r["cure_date"])
EP = defaultdict(list)
for c, ds in TRIG.items():
    end = None
    for d in sorted(ds):
        if EP[c] and (end is None or d < end):
            continue
        end = CURE.get((c, d.isoformat()))
        EP[c].append((d, end))


def in_def(c, d):
    return any(s <= d and (e is None or e > d) for s, e in EP[c])


def started(c, a, b):
    return any(a <= s < b for s, _ in EP[c])


run26 = list(csv.DictReader(open(os.path.join(T, "ifrs9_facility_run_2026-12-31.csv"))))
run24 = list(csv.DictReader(open(os.path.join(T, "ifrs9_facility_run_2024-12-31.csv"))))
BORR = set(r["customer_no"] for r in run26) | set(r["customer_no"] for r in run24) | set(EP)

# p1: payees taking 30 per cent or more of their receipts from a defaulting payer in the year before its default
k1 = n1 = 0
for a in sorted(EP):
    for s, _ in EP[a]:
        if not (dt.date(2022, 1, 1) <= s <= dt.date(2025, 12, 31)):
            continue
        for p in sorted(BORR):
            if p == a or a not in PAYERS[p] or share(p, a, s.year, s.month, 12) < 0.3 or in_def(p, s):
                continue
            n1 += 1
            yy, mm = mshift(s.year, s.month, 12)
            k1 += any(s < t <= dt.date(yy, mm, min(s.day, 28)) for t, _ in EP[p])
# p0: payee-years whose payer kept trading
k0 = n0 = 0
for Y in (2022, 2023, 2024, 2025):
    y0, y1 = dt.date(Y, 1, 1), dt.date(Y + 1, 1, 1)
    for p in sorted(BORR):
        if in_def(p, y0) or not any(TOT.get((p, "%04d-%02d" % (Y, m)), 0) > 0 for m in (1, 2, 3)):
            continue
        for a in PAYERS[p]:
            if share(p, a, Y, 1, 12) < 0.3 or in_def(a, y0) or started(a, y0, y1):
                continue
            n0 += 1
            k0 += started(p, y0, y1)
ok("p1 recomputed", (k1, n1) == (FIG["p1_k"], FIG["p1_n"]), "%d/%d" % (k1, n1))
ok("p0 recomputed", (k0, n0) == (FIG["p0_k"], FIG["p0_n"]), "%d/%d" % (k0, n0))
U = k1 / n1 - k0 / n0

# ---- the call ------------------------------------------------------------------------------------------------
FAC = defaultdict(list)
for r in run26:
    FAC[r["customer_no"]].append(r)
LE = {c: sum(float(r["lgd"]) * float(r["ead_nzd"]) for r in fs) for c, fs in FAC.items()}
PD = {c: float(fs[0]["pd_12m"]) for c, fs in FAC.items()}
VAL = {}
for c in LINES:
    deps = [p for p in FAC if p != c and FAC[p][0]["stage"] != "3" and c in PAYERS[p] and share(p, c, 2027, 1, 12) >= 0.3]
    VAL[c] = PD[c] * LE[c] + sum(PD[c] * U * LE[p] for p in deps)
best = max((comb for k in range(1, 9) for comb in itertools.combinations(sorted(LINES), k)
            if sum(LINES[x] for x in comb) <= ENV), key=lambda comb: sum(VAL[x] for x in comb))
call = " and ".join(sorted(NAME[c].replace(" Limited", "") for c in best))
ok("call", call == FIG["call"], call)
ok("total kept off", r_half(sum(VAL[c] for c in best), 50_000) == FIG["total_kept_off"])
short = {c: NAME[c].replace(" Limited", "") for c in LINES}
ok("each borrower's write-off kept off", all(r_half(VAL[c], 50_000) == FIG["kept_off"][short[c]] for c in LINES))

# ---- the asks: ranked packages, fall-back intakes, the intake at each envelope ---------------------------------
order = [short[c] for c in sorted(LINES, key=lambda c: -VAL[c])]
ok("ranked largest first", order == FIG["order"], ", ".join(order))


def intake(env_, out=()):
    ids = [c for c in sorted(LINES) if c not in out]
    sets = [comb for k in range(1, len(ids) + 1) for comb in itertools.combinations(ids, k)
            if sum(LINES[x] for x in comb) <= env_]
    comb = max(sets, key=lambda cb: sum(VAL[x] for x in cb))
    names_ = sorted(short[c] for c in comb)
    label = names_[0] if len(names_) == 1 else ", ".join(names_[:-1]) + " and " + names_[-1]
    return label, r_half(sum(VAL[x] for x in comb), 50_000)


for c in best:
    lab, tot = intake(ENV, (c,))
    want = FIG["fallback"][short[c]]
    ok("fall-back if %s turns its package down" % short[c], (lab, tot) == (want["intake"], want["kept_off"]),
       "%s, %d" % (lab, tot))
for row in FIG["envelope_curve"]:
    lab, tot = intake(row["envelope"])
    ok("intake at NZ$%s" % format(row["envelope"], ","), (lab, tot) == (row["intake"], row["kept_off"]),
       "%s, %d" % (lab, tot))
print("verify: %d failed" % len(bad))
sys.exit(1 if bad else 0)
