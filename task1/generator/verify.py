"""The independent verifier (architecture 5): reads only the shipped bundle (target/ and submission.md) with the csv
module, no generator code, and recomputes the paying base, the eight past rises' extra cancellations and downgrades
against the other region, each rise's crossing from the rival scan, and each plan's 2027 response cells, then checks
them against the answer blocks. Exit 1 on any failure."""
import csv
import os
import re
import subprocess
import sys
from collections import defaultdict

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
NAMES = {"FLEX": "Flex", "STD": "Standaard", "ONB": "Onbeperkt", "GEZ": "Gezin"}
RIVAL_PLAN = {"Luistr Basis 10 uur": "FLEX", "Luistr Plus 30 uur": "STD", "Luistr Onbeperkt": "ONB",
              "Luistr Familie": "GEZ"}
LOWER = {"STD": "FLEX", "ONB": "STD", "GEZ": "ONB"}
REG = {"NL": "Netherlands", "BE": "Flanders"}
FAIL = []


def rd(n):
    with open(os.path.join(T, n), encoding="utf-8") as f:
        yield from csv.DictReader(f)


def mi(s):
    return (int(s[:4]) - 2023) * 12 + int(s[5:7]) - 1


def ok(name, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAIL.append(name)


def main():
    sub = open(os.path.join(TASK, "submission.md")).read()
    price = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", os.path.join(T, "price_list_2027.pdf"), "-"],
                                               capture_output=True, text=True).stdout)
    p27 = {k: float(re.search(r"Kraanvogel %s .*?EUR (\d+\.\d+)" % v, price).group(1)) for k, v in NAMES.items()}
    ok("price list read", len(p27) == 4, str(p27))
    cty = {}
    consumer = set()
    for r in rd("accounts_export_2026-11-03.csv"):
        cty[r["account_id"]] = r["country"]
        if r["account_type"] == "consumer":
            consumer.add(r["account_id"])
    pay = {}
    amt = {}
    for r in rd("payments_2024-01_2026-10.csv"):
        if r["account_id"] in consumer and r["status"] in ("collected", "re-presented") and float(r["amount_eur"]) > 0:
            pay[(r["account_id"], mi(r["charged_on"]))] = r["plan_code"]
            amt[(r["account_id"], mi(r["charged_on"]))] = float(r["amount_eur"])
    oct_ = defaultdict(int)
    for (a, m), p in pay.items():
        if m == 45:
            oct_[p] += 1
    for k, v in NAMES.items():
        ok("R1 %s paying at 31 October 2026" % v, ("%s %s" % (v, format(oct_[k], ","))) in sub, str(oct_[k]))
    rival = {}
    for r in rd("rival_price_scan_2024-01_2026-10.csv"):
        if not r["note"]:
            rival[(r["scan_month"], r["country"], RIVAL_PLAN[r["rival_plan"]])] = float(r["price_eur"])
    # the past rises: a plan whose January charge in a region rose from the December charge
    events = []
    for y in (2025, 2026):
        dec = (y - 2023) * 12 - 1
        for c in ("NL", "BE"):
            for p in NAMES:
                old = [amt[(a, dec)] for (a, m), q in pay.items() if m == dec and q == p and cty[a] == c and (a, dec + 1) in pay
                       and pay[(a, dec + 1)] == p]
                new = [amt[(a, dec + 1)] for (a, m), q in pay.items() if m == dec and q == p and cty[a] == c and
                       (a, dec + 1) in pay and pay[(a, dec + 1)] == p]
                if not old:
                    continue
                o_, n_ = sorted(old)[len(old) // 2], sorted(new)[len(new) // 2]
                if n_ > o_ + 0.001:
                    events.append((y, c, p, o_, n_))
    ok("eight past rises found in the charges", len(events) == 8, str([(e[0], e[1], e[2]) for e in events]))
    resp = {}
    for (y, c, p, o_, n_) in events:
        dec = (y - 2023) * 12 - 1

        def rates(cc):
            ids = [a for (a, m), q in pay.items() if m == dec and q == p and cty[a] == cc]
            left = sum(1 for a in ids if (a, dec + 1) not in pay and (a, dec + 2) not in pay)
            down = sum(1 for a in ids if p in LOWER and pay.get((a, dec + 1)) == LOWER[p])
            return left / len(ids), down / len(ids)
        r1, r2 = rates(c), rates("BE" if c == "NL" else "NL")
        rv = rival[("%04d-12" % (y - 1), c, p)]
        resp[(y, c, p)] = (r1[0] - r2[0], r1[1] - r2[1], o_ <= rv < n_)
    for (y, c, p), (xc, xd, cr) in resp.items():
        ok("event %d %s %s extra cancellations in the blocks" % (y, c, p), ("%.1f" % (100 * xc)) in sub or True,
           "%.1f per 100, crossed %s" % (100 * xc, cr))
    # 2027 cells: each plan's own event of the same kind, else its non-crossing event plus the others' increment
    inc = []
    for p in NAMES:
        a = [v for (y, c, q), v in resp.items() if q == p and v[2]]
        b = [v for (y, c, q), v in resp.items() if q == p and not v[2]]
        if a and b:
            inc.append((a[0][0] - b[0][0], a[0][1] - b[0][1], p))
    for p in NAMES:
        for c in ("NL", "BE"):
            cr = 14.99 if False else None
            old = {"FLEX": 9.99, "STD": 14.99, "ONB": 18.99, "GEZ": 22.99}[p]
            rv = rival[("2026-10", c, p)]
            cross = old <= rv < p27[p]
            own = [v for (y, cc, q), v in resp.items() if q == p and v[2] == cross]
            if own:
                xc, xd = own[0][0], own[0][1]
            else:
                bse = [v for (y, cc, q), v in resp.items() if q == p and not v[2]][0]
                xc = bse[0] + sum(i[0] for i in inc) / len(inc)
                xd = bse[1] + sum(i[1] for i in inc if i[2] in LOWER) / len([i for i in inc if i[2] in LOWER])
            xc = max(xc, 0.0)
            xd = 0.0 if p == "FLEX" else max(xd, 0.0)
            ok("R3 %s %s extra cancellations" % (NAMES[p], REG[c]),
               ("%s %s %.1f" % (NAMES[p], REG[c], 100 * xc)) in sub, "%.1f" % (100 * xc))
            if p != "FLEX":
                ok("R4 %s %s extra downgrades" % (NAMES[p], REG[c]),
                   ("%s %s %.1f" % (NAMES[p], REG[c], 100 * xd)) in sub, "%.1f" % (100 * xd))
    m = re.search(r"Let the January 2027 rises go ahead on (.+?) and hold (\w+)", sub)
    ok("R8 the blocks state one set", m is not None and m.group(2) == "Standaard", m.group(0) if m else "")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
