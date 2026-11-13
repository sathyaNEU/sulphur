"""Independent verifier: recomputes the assembly figures, the reserve, the spending and the policy's distributions from
target/ with plain parsing (no analysis.py), and reads the golden workbook back against figures.json."""
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = lambda f: os.path.join(TASK, "target", f)
F = json.load(open(os.path.join(HERE, "figures.json")))
fails = []


def ok(name, cond, detail=""):
    print("%-4s %-66s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        fails.append(name)


def rows(f):
    return list(csv.DictReader(open(T(f), newline="")))


def sheet(f, name=None):
    wb = load_workbook(T(f), data_only=True)
    ws = wb[name] if name else wb.worksheets[0]
    it = ws.iter_rows(values_only=True); hdr = next(it)
    return [dict(zip(hdr, r)) for r in it if any(v is not None for v in r)]


qkey = lambda d: (d.year, (d.month - 1) // 3)
reg = {r["Fund ID"]: r for r in sheet("private_commitment_register_2026-12-31.xlsx")}
paid = defaultdict(float); nav = {}; navq = {}
for r in rows("capital_account_statements_2013Q1_2026Q4.csv"):
    if r["note"] == "superseded":
        continue
    paid[r["fund_id"]] += sum(float(r[k]) for k in ("contributions_investments_usd", "contributions_management_fees_usd", "contributions_fund_expenses_usd")) / 1e6
    d = dt.date.fromisoformat(r["period_end"])
    if r["fund_id"] not in navq or d > navq[r["fund_id"]]:
        navq[r["fund_id"]] = d; nav[r["fund_id"]] = float(r["ending_nav_usd"]) / 1e6
for r in rows("custodian_cash_activity_2026Q4.csv"):
    if navq.get(r["fund_id"]) == dt.date(2026, 12, 31):
        continue
    a = float(r["amount_usd"]) / 1e6
    if r["movement"] == "capital call":
        paid[r["fund_id"]] += a; nav[r["fund_id"]] = nav.get(r["fund_id"], 0.0) + a
    else:
        nav[r["fund_id"]] = nav.get(r["fund_id"], 0.0) - a
unf = defaultdict(float)
for fid, r in reg.items():
    if r["Status"] == "liquidated":
        continue
    unf[r["Strategy"]] += float(r["Commitment (USD m)"]) - (paid[fid] if r["Status"] != "pending first close" else 0.0)
for s, v in F["unfunded_by_strategy_usd_m"].items():
    ok("unfunded %s" % s, abs(unf[s] - v) < 0.06, "%.2f against %.1f" % (unf[s], v))
fac = {"Cash, money market funds and US Treasuries": 1.0, "Investment-grade bonds": 0.9, "Public equities": 0.7,
       "Hedge funds: redeemable within 24 months": 0.9}
res = sum(float(h["Market value 31 Dec 2026 (USD m)"]) * fac.get(h["Policy liquidity class"], 0.0) for h in sheet("liquid_holdings_2026-12-31.xlsx") if h["Policy liquidity class"])
ok("the liquid reserve at the policy's factors", abs(res - F["reserve_usd_m"]) < 0.01, "%.2f" % res)
sp = {int(r["fiscal_year"]): float(r["approved_distribution_usd_m"]) for r in rows("spending_distributions_FY2014_FY2027.csv")}
ok("eight quarters of FY2027's distribution", abs(2 * sp[2027] - F["spending_24m_usd_m"]) < 0.01)
# the policy's distribution rates, from the benchmark
num = defaultdict(float); den = defaultdict(float); prev = {}
for r in sorted(rows("industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv"), key=lambda r: (r["benchmark_fund"], r["period_end"])):
    d = dt.date.fromisoformat(r["period_end"]); q = d.year * 4 + (d.month - 1) // 3
    p = prev.get(r["benchmark_fund"])
    if p and p[0] == q - 1 and 2008 * 4 + 2 <= q <= 2010 * 4 + 1:
        num[(r["strategy"], q - (2008 * 4 + 2))] += float(r["distributions_pct_of_commitment"]); den[(r["strategy"], q - (2008 * 4 + 2))] += p[1]
    prev[r["benchmark_fund"]] = (q, float(r["nav_pct_of_commitment"]))
dist = [0.0] * 8
for fid, r in reg.items():
    if r["Status"] in ("liquidated", "pending first close"):
        continue
    for k in range(8):
        dist[k] += max(nav.get(fid, 0.0), 0.0) * num[(r["Strategy"], k)] / den[(r["Strategy"], k)]
for i, h in enumerate(["H1 2027", "H2 2027", "H1 2028", "H2 2028"]):
    v = dist[2 * i] + dist[2 * i + 1]
    ok("distributions %s" % h, abs(v - F["distributions_by_half_usd_m"][h]) < 0.06, "%.2f against %.1f" % (v, F["distributions_by_half_usd_m"][h]))
# the golden workbook against figures.json
wb = load_workbook(os.path.join(TASK, "golden", "wexmoor_2027_commitment_capacity.xlsx"), data_only=True)
summ = {r[0]: r[1:] for r in wb["Summary"].iter_rows(values_only=True) if r[0]}
ok("workbook: the largest budget that passes", summ["Largest budget that passes (USD m, policy steps of 25)"][0] == F["capacity_usd_m"])
ok("workbook: net cash needs at USD 500m", summ["Net cash needs"][0] == F["net_cash_needs_500_usd_m"])
ok("workbook: headroom at USD 500m", summ["Headroom above the minimum"][0] == F["headroom_500_usd_m"])
hy = {r[0]: r[1:5] for r in wb["By half-year"].iter_rows(values_only=True) if r[0]}
ok("workbook: calls of the closed funds by half", list(hy["Calls, funds that have held a first close"]) == [F["calls_closed_funds_by_half_usd_m"][h] for h in ["H1 2027", "H2 2027", "H1 2028", "H2 2028"]])
ok("workbook: calls of the pending funds by half", list(hy["Calls, funds yet to hold a first close"]) == [F["calls_pending_funds_by_half_usd_m"][h] for h in ["H1 2027", "H2 2027", "H1 2028", "H2 2028"]])
print("\n%d failure%s" % (len(fails), "" if len(fails) == 1 else "s"))
sys.exit(1 if fails else 0)
