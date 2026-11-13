"""The independent verifier (architecture 5 as repaired): reads only the shipped bundle (target/ and submission.md)
with the csv module, no generator code, and recomputes the paying base, the eight past rises found in the charges
with each one's first-bill extra cancellations against the other region and whether it passed the rival in the
December scan, the December leaving after each 1 December e-mail, which 2027 prices pass the rival's latest scan,
and how often a stop is followed by paying again; then checks them against the answer blocks. Exit 1 on any failure."""
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
    ok("price list dates the e-mails", all(d in price for d in ("1 December 2024", "1 December 2025", "1 December 2026")))
    cty, consumer = {}, set()
    for r in rd("accounts_export_2026-11-03.csv"):
        cty[r["account_id"]] = r["country"]
        if r["account_type"] == "consumer":
            consumer.add(r["account_id"])
    pay, amt = {}, {}
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
    on = defaultdict(list)
    for (a, m), p in pay.items():
        on[(m, p)].append(a)
    # the past rises: a plan whose January charge in a region rose from the December charge
    events = []
    for y in (2025, 2026):
        dec = (y - 2023) * 12 - 1
        for c in ("NL", "BE"):
            for p in NAMES:
                same = [a for a in on[(dec, p)] if cty[a] == c and pay.get((a, dec + 1)) == p]
                if not same:
                    continue
                o_ = sorted(amt[(a, dec)] for a in same)[len(same) // 2]
                n_ = sorted(amt[(a, dec + 1)] for a in same)[len(same) // 2]
                if n_ > o_ + 0.001:
                    events.append((y, c, p, o_, n_))
    ok("eight past rises found in the charges", len(events) == 8, str([(e[0], e[1], e[2]) for e in events]))
    xc, xa, cross = {}, {}, {}
    for (y, c, p, o_, n_) in events:
        dec = (y - 2023) * 12 - 1

        def left(cc):
            ids = [a for a in on[(dec, p)] if cty[a] == cc]
            return sum(1 for a in ids if (a, dec + 1) not in pay) / len(ids)

        def dec_left(cc):
            ids = [a for a in on[(dec - 1, p)] if cty[a] == cc]
            return sum(1 for a in ids if (a, dec) not in pay) / len(ids)
        other = "BE" if c == "NL" else "NL"
        xc[(y, c, p)] = 100 * (left(c) - left(other))
        xa[(y, c, p)] = 100 * (dec_left(c) - dec_left(other))
        rv = rival[("%04d-12" % (y - 1), c, p)]
        cross[(y, c, p)] = o_ <= rv < n_
    ok("four past rises passed the rival", sum(cross.values()) == 4, str([k for k, v in cross.items() if v]))
    ok("passing the rival reads one way: no plan was above the rival before any past rise",
       all(o_ <= rival[("%04d-12" % (y - 1), c, p)] for (y, c, p, o_, n_) in events))
    for k, v in xc.items():
        ok("event %d %s %s first-bill extra cancellations in the blocks" % k, ("%.1f" % v) in sub, "%.1f" % v)
    for p, v in NAMES.items():
        m = sum(x for (y, c, q), x in xa.items() if q == p) / 2
        ok("%s December leaving after the e-mail (mean of its two rises) in the blocks" % v,
           re.search(r"%s %.1f" % (v, m), sub) is not None or ("%s lost %.1f" % (v, m)) in sub, "%.1f" % m)
    # the 2027 prices against the rival's latest scan
    for p, v in NAMES.items():
        old = {"FLEX": 9.99, "STD": 14.99, "ONB": 18.99, "GEZ": 22.99}[p]
        past = [c for c in ("NL", "BE") if old <= rival[("2026-10", c, p)] < p27[p]]
        above = [c for c in ("NL", "BE") if p27[p] > rival[("2026-10", c, p)]]
        ok("%s's 2027 price %s the rival in both regions, read as crossing or as ending above" % (
            v, "passes" if p == "FLEX" else "does not pass"), (len(past) == 2) == (p == "FLEX") and past == above,
           "%s %s" % (past, above))
    # stops that pay again: of the consumer subscriptions that stopped in a December, the share paying within a year
    months = defaultdict(list)
    for (a, m) in pay:
        months[a].append(m)
    stops = back = 0
    for a, ms in months.items():
        s = set(ms)
        for m in (23, 35):
            if (m - 1) in s and m not in s:
                stops += 1
                back += any(k in s for k in range(m + 1, min(m + 13, 46)))
    ok("stops come back: a fifth or more of December stops pay again within the year", back / stops > 0.2,
       "%d of %d" % (back, stops))
    m = re.search(r"Let (\w+)'s and (\w+)'s January 2027 rises go ahead", sub)
    ok("R8 the blocks state one set", m is not None and {m.group(1), m.group(2)} == {"Standaard", "Gezin"},
       m.group(0) if m else "")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
