"""Independent verifier: recomputes the assembly figures, the reserve, the spending, the policy's distributions and the
bases section 8 files (the pace of new investments, the benchmark's call rate for funds past their investment periods)
from target/ with plain parsing (no analysis.py), reads the filed sentences back from the shipped policy, and reads the
golden workbook and memo back against figures.json."""
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
# every live manager's company-level rows run to the fourth quarter of 2026
last = {}
for r in rows("manager_portfolio_activity_2013_2026.csv"):
    d = dt.date.fromisoformat(r["date"])
    if r["manager"] not in last or d > last[r["manager"]]:
        last[r["manager"]] = d
live_mgr = {r["Manager"] for r in reg.values() if r["Status"] in ("investing", "harvesting")}
ok("every live manager's company-level rows reach the fourth quarter of 2026", all(m in last and last[m] >= dt.date(2026, 10, 1) for m in live_mgr),
   "; ".join(sorted(m for m in live_mgr if m not in last or last[m] < dt.date(2026, 10, 1))) or "%d managers" % len(live_mgr))
# section 8's benchmark call rate: funds with a vintage six or more years before the quarter's year, contributions over the value a quarter earlier
ST = {"Buyout": "BO", "Growth equity": "GE", "Venture capital": "VC"}
cn = defaultdict(float); cd = defaultdict(float); prev = {}
for r in sorted(rows("industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv"), key=lambda r: (r["benchmark_fund"], r["period_end"])):
    d = dt.date.fromisoformat(r["period_end"]); q = d.year * 4 + (d.month - 1) // 3
    p = prev.get(r["benchmark_fund"])
    if p and p[0] == q - 1 and 2008 * 4 + 2 <= q <= 2010 * 4 + 1 and d.year - int(r["vintage"]) >= F["benchmark_vintage_years"] and r["strategy"] in ST:
        cn[(ST[r["strategy"]], q - (2008 * 4 + 2))] += float(r["contributions_pct_of_commitment"]); cd[(ST[r["strategy"]], q - (2008 * 4 + 2))] += p[1]
    prev[r["benchmark_fund"]] = (q, float(r["nav_pct_of_commitment"]))
for s_ in ("BO", "GE", "VC"):
    tot = 100 * sum(cn[(s_, k)] / cd[(s_, k)] for k in range(8))
    ok("benchmark call rate, eight quarters, %s" % s_, abs(tot - F["old_fund_rate_8q_pct"][s_]) < 0.006, "%.3f against %.2f" % (tot, F["old_fund_rate_8q_pct"][s_]))
# the funds that rate applies to at 31 December: buyout, growth and venture funds whose investment period has ended
old = [fid for fid, r in reg.items() if r["Status"] not in ("liquidated", "pending first close") and r["Strategy"] in ST
       and (r["Investment period ends"].date() if hasattr(r["Investment period ends"], "date") else r["Investment period ends"]) <= dt.date(2026, 12, 31)]
ok("funds past their investment periods at 31 December (buyout, growth, venture)", len(old) == F["old_funds_31dec"]
   and all(reg[f]["Status"] == "harvesting" for f in old), "%d funds" % len(old))
ok("their value at 31 December", abs(sum(max(nav.get(f, 0.0), 0.0) for f in old) - F["old_funds_value_usd_m"]) < 0.06,
   "%.2f against %.1f" % (sum(max(nav.get(f, 0.0), 0.0) for f in old), F["old_funds_value_usd_m"]))
# section 8's pace: investments, first and follow-on, over the commitment not yet invested, by strategy and year since first close
ST6 = {"Buyout": "BO", "Growth equity": "GE", "Venture capital": "VC", "Real estate": "RE", "Infrastructure": "IN", "Private credit": "PC"}
qn = lambda d: d.year * 4 + (d.month - 1) // 3
dd = lambda x: x.date() if hasattr(x, "date") else x
invq = defaultdict(float)
for r in rows("manager_portfolio_activity_2013_2026.csv"):
    if r["record_type"] in ("initial investment", "follow-on investment"):
        invq[(r["fund_id"], qn(dt.date.fromisoformat(r["date"])))] += float(r["amount_usd_m"])
pn = defaultdict(float); pd_ = defaultdict(float)
for fid, r in reg.items():
    if not r["First close"] or not r["Fund size (USD m)"]:
        continue
    C = float(r["Commitment (USD m)"]); sh = C / float(r["Fund size (USD m)"])
    fc = qn(dd(r["First close"])); ipl = min(qn(dd(r["Investment period ends"])), 2026 * 4 + 3)
    cum = 0.0
    for q in range(fc, ipl + 1):
        key = (ST6[r["Strategy"]], (q - fc) // 4)
        pn[key] += invq.get((fid, q), 0.0) * sh; pd_[key] += max(C - cum, 0.0)
        cum += invq.get((fid, q), 0.0) * sh
bad = [k for k in pd_ if pd_[k] > 0 and abs(100 * pn[k] / pd_[k] - F["pace_pct"].get("%s year %d" % (k[0], k[1] + 1), -9)) > 0.006]
ok("the pace of new investments by strategy and year since first close", not bad and len(pd_) == len(F["pace_pct"]), "%d cells" % len(pd_))
# section 8's facility balances: the latest audited borrowings, plus the investments since, less the capital called for investments since
audb = {}
for r in sheet("fund_audited_financials_FY2013_FY2026.xlsx", "Audited accounts"):
    d = dd(r["Fiscal year end"])
    if r["Fund ID"] not in audb or d > audb[r["Fund ID"]][0]:
        audb[r["Fund ID"]] = (d, float(r["Credit facility borrowings (USD thousands)"]) / 1000.0)
callq = defaultdict(float); stq4 = set()
for r in rows("capital_account_statements_2013Q1_2026Q4.csv"):
    if r["note"] == "superseded":
        continue
    d = dt.date.fromisoformat(r["period_end"])
    callq[(r["fund_id"], qn(d))] += float(r["contributions_investments_usd"]) / 1e6
    if d == dt.date(2026, 12, 31): stq4.add(r["fund_id"])
for r in rows("custodian_cash_activity_2026Q4.csv"):
    if r["fund_id"] not in stq4 and r["movement"] == "capital call":
        callq[(r["fund_id"], 2026 * 4 + 3)] += float(r["amount_usd"]) / 1e6
firstact = {}
for (fid, q) in invq:
    firstact[fid] = min(firstact.get(fid, q), q)
fb = 0.0
for fid, r in reg.items():
    if r["Status"] in ("pending first close", "liquidated") or fid not in firstact or not r["Fund size (USD m)"]:
        continue
    sh = float(r["Commitment (USD m)"]) / float(r["Fund size (USD m)"])
    qa, bor = (qn(audb[fid][0]), audb[fid][1] * sh) if fid in audb and qn(audb[fid][0]) >= min(firstact[fid], min(q for (f2, q) in callq if f2 == fid)) else (-1, 0.0)
    since_i = sum(v for (f2, q), v in invq.items() if f2 == fid and q > qa) * sh
    since_c = sum(v for (f2, q), v in callq.items() if f2 == fid and q > qa)
    fb += max(bor + since_i - since_c, 0.0)
ok("the facility balances as section 8 forms them", abs(fb - F["line_stock_usd_m"]) < 0.06, "%.2f against %.1f" % (fb, F["line_stock_usd_m"]))
# the sentences the policy files, read back from the shipped PDF
from pdfminer.high_level import extract_text
import re
pol = re.sub(r"\s+", " ", extract_text(T("wexmoor_endowment_liquidity_policy_2025.pdf"))).replace("\u2019", "'")
ok("policy reads back (control: section 7's benchmark sentence)", "times the distribution rate of its strategy in the matching quarter from the third quarter of 2008" in pol, "%d characters" % len(pol))
for name, sent in (("the minimum reserve", "the minimum reserve is USD %s million" % format(int(F["minimum_reserve_usd_m"]), ",")),
                   ("the cap at the commitment", "no fund is taken to call more than the part of its commitment it has not yet called"),
                   ("the pace", "first and follow-on, in the quarter over their commitments not yet invested at the start of it"),
                   ("the commitment not yet invested", "A commitment not yet invested is the commitment less the endowment's share of the investments the fund has made"),
                   ("first closes", "is taken to hold it in the quarter its manager has given"),
                   ("the benchmark funds", "with a vintage year six or more years before the year of that quarter"),
                   ("the rate taken whole", "The rate is taken whole"),
                   ("the facility balances", "counts as called in the first quarter of the stress, at its balance at 31 December"),
                   ("how the facility balance is formed", "the borrowings on the fund's latest audited balance sheet, plus the investments the fund has made since"),
                   ("no proceeds reinvested since", "No allowance is made for proceeds reinvested since the balance sheet"),
                   ("fees and expenses", "the management fee and the fund expenses of its latest quarterly statement"),
                   ("every call counts, judged on the evidence", "Capital calls are all those the endowment's managers can be expected to make in the stress, judged on the evidence")):
    ok("policy files %s" % name, sent in pol)
# the plan's programs
wb = load_workbook(T("corrigan_hart_pacing_plan_2027.xlsx"), data_only=True)
prog = {r[0]: r for r in wb["Programs"].iter_rows(min_row=2, values_only=True) if r[0]}
ok("the plan's program totals", all(abs(prog[c][3] - v["total_usd_m"]) < 1e-9 for c, v in F["programs"].items()))
# the property and infrastructure loans alive at 31 December 2026 that fall due in the eight quarters
loan = {}; gone = set()
for r in rows("manager_portfolio_activity_2013_2026.csv"):
    key = (r["fund_id"], r["portfolio_company"])
    if r["record_type"] in ("asset loan drawn", "asset loan refinanced"):
        d = dt.date.fromisoformat(r["date"])
        if key not in loan or d >= loan[key][0]: loan[key] = (d, float(r["amount_usd_m"]), dt.date.fromisoformat(r["loan_maturity"]))
    elif r["record_type"] == "realization":
        gone.add(key)
due = [k for k, x in loan.items() if k not in gone and reg.get(k[0], {}).get("Status") in ("investing", "harvesting")
       and dt.date(2027, 1, 1) <= x[2] <= dt.date(2028, 12, 31)]
ok("the loans falling due in 2027 and 2028", len(due) == F["loans_due_count"], "%d against %d" % (len(due), F["loans_due_count"]))
bal = sum(loan[k][1] * float(reg[k[0]]["Commitment (USD m)"]) / float(reg[k[0]]["Fund size (USD m)"]) for k in due)
ok("their balance at Wexmoor's share (commitment over fund size)", abs(bal - F["loans_due_balance_usd_m"]) < 0.11, "%.2f against %.1f" % (bal, F["loans_due_balance_usd_m"]))
# the managers' past successions: did the earlier fund's period end at the successor's first close?
by_m = defaultdict(list)
for r in reg.values(): by_m[r["Manager"]].append(r)
votes = {}
for m_, rs in by_m.items():
    rs = sorted(rs, key=lambda r: (r["Vintage"], r["Fund ID"]))
    for a, b in zip(rs[:-1], rs[1:]):
        if not (a["First close"] and b["First close"] and a["Investment period ends"]): continue
        fa = a["First close"].date() if hasattr(a["First close"], "date") else a["First close"]
        fb = b["First close"].date() if hasattr(b["First close"], "date") else b["First close"]
        ie = a["Investment period ends"].date() if hasattr(a["Investment period ends"], "date") else a["Investment period ends"]
        agreed = dt.date(fa.year + int(a["Investment period (years, per agreement)"]), fa.month, 1)
        qn = lambda d: d.year * 4 + (d.month - 1) // 3
        if qn(fb) < max(qn(agreed), qn(ie) + 1):
            votes.setdefault(m_, []).append(qn(ie) + 1 == qn(fb))
cl = sorted(m_ for m_, v in votes.items() if all(v)); nc = sorted(m_ for m_, v in votes.items() if not any(v))
ok("the managers whose past periods ended at the successor's first close", cl == F["clause_managers"], "%d managers" % len(cl))
ok("the managers whose past periods ran on", nc == F["no_clause_managers"], "; ".join(nc))
# the golden workbook against figures.json
wb = load_workbook(os.path.join(TASK, "golden", "wexmoor_2027_program_test.xlsx"), data_only=True)
summ = {r[0]: r[1:] for r in wb["Summary"].iter_rows(values_only=True) if r[0]}
ok("workbook: the program", summ["Program the policy lets the Committee adopt"][0] == F["program"])
ok("workbook: the headroom before any 2027 commitment", summ["Headroom above the minimum before any 2027 commitment"][0] == F["headroom_before_2027_usd_m"])
ok("workbook: net cash needs", summ["Net cash needs"][0] == F["net_needs_before_2027_usd_m"])
ok("workbook: each program's calls and headroom left", all(summ[c][2] == v["calls_usd_m"] and summ[c][3] == v["headroom_usd_m"] for c, v in F["programs"].items()))
hy = {r[0]: r[1:5] for r in wb["By half-year"].iter_rows(values_only=True) if r[0]}
H = ["H1 2027", "H2 2027", "H1 2028", "H2 2028"]
allc = {**F["calls_2027_by_half_usd_m"], **F["calls_2028_by_half_usd_m"]}
ok("workbook: calls by half", list(hy["Calls on the commitments made by the end of 2026"]) == [allc[h] for h in H])
ok("workbook: distributions by half", list(hy["Distributions, the policy's 2008-10 rates"]) == [F["distributions_by_half_usd_m"][h] for h in H])
ok("workbook: the refinancing calls by half", list(hy["   of which property and infrastructure loans refinanced short of their balance"]) == [F["refinancing_calls_by_half_usd_m"][h] for h in H])
scs = [r[0] for r in wb["Successor closes"].iter_rows(min_row=2, values_only=True) if r[0] and r[5]]
ok("workbook: the facility balances total", abs([r for r in wb["Facility balances"].iter_rows(values_only=True) if r[0] == "Total"][0][7] - F["line_stock_usd_m"]) < 1e-9)
ok("workbook: new investments and the funds past their periods by half", list(hy["   of which new investments at the pace of section 8"]) == [F["new_investments_by_half_usd_m"][h] for h in H]
   and list(hy["   of which buyout, growth and venture funds past their periods, at the benchmark's rate"]) == [F["old_fund_calls_by_half_usd_m"][h] for h in H])
ok("workbook: the successor closes", scs == F["successor_funds"], "; ".join(scs))
al = {r[0]: r for r in wb["Asset loans"].iter_rows(min_row=2, values_only=True) if r[0]}
ok("workbook: the loans' shortfall", abs(al["Total"][7] - F["loans_due_gap_usd_m"]) < 1e-9 and len([k for k in al if k != "Total" and al[k][2]]) >= 1)
un = {r[0]: r[1] for r in wb["Unfunded"].iter_rows(min_row=2, values_only=True) if r[0]}
ok("workbook: unfunded by strategy", all(un[s_] == v for s_, v in F["unfunded_by_strategy_usd_m"].items()))
from docx import Document
txt = "\n".join(p.text for p in Document(os.path.join(TASK, "golden", "commitment_program_2027_memo.docx")).paragraphs)
ok("memo: the program and the headroom", ("Adopt program %s" % F["program"]) in txt and ("USD %.1f million" % F["headroom_before_2027_usd_m"]) in txt)
print("\n%d failure%s" % (len(fails), "" if len(fails) == 1 else "s"))
sys.exit(1 if fails else 0)
