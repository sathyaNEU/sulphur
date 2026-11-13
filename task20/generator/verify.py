"""Independent verifier: recomputes figures from target/ and the golden workbook with plain parsing, no analysis.py."""
import csv
import datetime as dt
import json
import os
import re
import sys
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = lambda f: os.path.join(TASK, "target", f)
F = json.load(open(os.path.join(HERE, "figures.json")))
fails = []


def ok(name, cond, detail=""):
    print("%-4s %-62s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        fails.append(name)


def rows(f):
    return list(csv.DictReader(open(T(f), newline="")))


# 2022 records: NEX net cash, day-ahead net, customer payments, by cash date
flow = {}
for r in rows("nex_clearing_statements_2018_2026.csv"):
    if r["status"] != "superseded" and r["statement_date"].startswith("2022"):
        flow[r["statement_date"]] = flow.get(r["statement_date"], 0.0) + float(r["net_cash_to_nex"])
days = sorted(flow)
for r in rows("nex_dayahead_settlements_2018_2026.csv"):
    if r["settlement_date"] in flow:
        flow[r["settlement_date"]] -= float(r["net_amount_eur"])
for r in rows("hk_sales_ledger_2018_2026.csv"):
    if r["paid_date"] in flow and r["paid_eur"]:
        flow[r["paid_date"]] -= float(r["paid_eur"])
cum, best = 0.0, (-1e18, None)
for d in days:
    cum += flow[d]
    if cum > best[0]:
        best = (cum, d)
ok("2022 records' peak", abs(best[0] / 1e6 - F["c22_actual_m"]) < 0.06, "%.2f on %s" % (best[0] / 1e6, best[1]))

# the opening book from the month-end statement
twh = {}
for r in rows("nex_positions_month_end_2017_2026.csv"):
    if r["month_end"] != "2026-12-30":
        continue
    s, e = dt.date.fromisoformat(r["delivery_start"]), dt.date.fromisoformat(r["delivery_end"])
    if s.year < 2027:
        continue
    twh[s.year] = twh.get(s.year, 0.0) - float(r["position_mw"]) * ((e - s).days + 1) * 24 / 1e6
ok("open book 2027", abs(twh.get(2027, 0) - F["book_open_2027_twh"]) < 0.001, "%.3f" % twh.get(2027, 0))
ok("open book 2028", abs(twh.get(2028, 0) - F["book_open_2028_twh"]) < 0.001, "%.3f" % twh.get(2028, 0))

# hedge ratios on the policy's basis
wb = load_workbook(T("hk_budget_vintages_2016_2026.xlsx"), data_only=True)
gen = {}
for r in list(wb.active.iter_rows(values_only=True))[1:]:
    s = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
    if s <= dt.date(2026, 12, 30):
        if r[1] not in gen or s >= gen[r[1]][0]:
            gen[r[1]] = (s, float(r[3]) * 1e3)
for y in (2027, 2028, 2029):
    hrs = ((dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days) * 24
    pol = (twh.get(y, 0.0) * 1e6 + 100 * hrs) / gen[y][1] * 100
    ok("hedge ratio %d" % y, abs(pol - F["ratio_%d_pct" % y]) < 0.06, "%.2f" % pol)

# the golden workbook's daily path: its cumulative maximum is the requirement and its date
wb = load_workbook(os.path.join(TASK, "golden", "hallingvass_margin_facility_2027.xlsx"), data_only=True)
p = list(wb["Daily path"].iter_rows(values_only=True))[1:]
cum, best = 0.0, (-1e18, None)
for r in p:
    cum += r[7]
    if cum > best[0]:
        best = (cum, r[0])
d = best[1].date() if isinstance(best[1], dt.datetime) else best[1]
ok("workbook's cumulative peak", abs(best[0] - F["peak_m"]) < 0.06, "%.2f on %s" % (best[0], d))
ok("workbook's peak date", "%d %s %d" % (d.day, d.strftime("%B"), d.year) == F["peak_date"])
ok("facility is the peak rounded up to EUR 50 million", F["facility_m"] == 50 * -(-F["peak_m"] // 50))

# every number in the answer blocks traces to figures.json
sub = open(os.path.join(TASK, "submission.md")).read()
vals = set()
for v in F.values():
    if isinstance(v, (int, float)):
        vals |= {"%g" % v, "%.1f" % v, "%.2f" % v, "%.3f" % v, "{:,}".format(v) if isinstance(v, int) else "%.1f" % v}
    else:
        vals.add(str(v))
nums = [n.rstrip(".,") for n in re.findall(r"(?<![\w.])\d[\d,]*\.?\d*(?![\w])", sub)]
stray = sorted({n for n in nums if n not in vals and not re.fullmatch(r"(19|20)\d\d|[0-9]|1[0-9]|2[0-9]|3[01]", n.rstrip("."))})
ok("numbers in the answer blocks trace to figures.json", not stray, ", ".join(stray))
print("%d FAIL" % len(fails))
sys.exit(1 if fails else 0)
