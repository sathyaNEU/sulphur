"""The golden for task20 architecture 6, computed from target/ alone, and every hurried route beside it. The liquidity
policy sets the test (sections 3 to 7 and 9) and, in section 8, the basis of the calls it does not leave to judgment:
the pace of new investments, the dates of first closes still to come, the calls of buyout, growth and venture funds
past their investment periods, the credit facilities and the cap at the commitment. Two things are left to the
evidence, and they decide the program: when each fund's investment period ends, and what the property and
infrastructure loans that fall due in the stress cost."""
import csv
import datetime as dt
import math
import os
from collections import defaultdict
import numpy as np
from openpyxl import load_workbook

D = dt.date.fromisoformat
Q0 = 2000
def qi(y, q): return (y - Q0) * 4 + (q - 1)
def q_of(d): return qi(d.year, (d.month - 1) // 3 + 1)
H_END = qi(2026, 4)
W = list(range(H_END + 1, H_END + 9))
STRATS = {"Buyout": "BO", "Growth equity": "GE", "Venture capital": "VC", "Real estate": "RE", "Infrastructure": "IN", "Private credit": "PC"}
EQUITY = ("BO", "GE", "VC")
REAL = ("RE", "IN")
HALVES = ["H1 2027", "H2 2027", "H1 2028", "H2 2028"]
STRAT_ORDER = ["Buyout", "Growth equity", "Venture capital", "Real estate", "Infrastructure", "Private credit"]
OLD_YEARS = 6              # policy section 8: benchmark funds with a vintage year six or more years before the quarter's year

def rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))

def sheet(path, name=None):
    wb = load_workbook(path, data_only=True)
    ws = wb[name] if name else wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    hdr = next(it)
    return [dict(zip(hdr, r)) for r in it if any(v is not None for v in r)]

def _qd(v):
    return q_of(v.date() if hasattr(v, "date") else v) if v else None

def load(tgt):
    P = lambda f: os.path.join(tgt, f)
    L = {}
    reg = sheet(P("private_commitment_register_2026-12-31.xlsx"))
    L["reg"] = {r["Fund ID"]: r for r in reg}
    # statements: drop superseded lines, one row per fund-quarter (millions)
    st = defaultdict(dict)
    for r in rows(P("capital_account_statements_2013Q1_2026Q4.csv")):
        if r["note"] == "superseded":
            continue
        q = q_of(D(r["period_end"]))
        st[r["fund_id"]][q] = {k: float(r[k]) / 1e6 for k in r if k.endswith("_usd")}
    # the custodian's cash for the fourth quarter where a statement is still to come
    for r in rows(P("custodian_cash_activity_2026Q4.csv")):
        fid = r["fund_id"]
        if H_END in st.get(fid, {}) and not st[fid][H_END].get("cash_only"):
            continue
        x = st[fid].setdefault(H_END, {"contributions_investments_usd": 0.0, "contributions_management_fees_usd": 0.0,
                                       "contributions_fund_expenses_usd": 0.0, "distributions_return_of_capital_usd": 0.0,
                                       "distributions_realized_gain_usd": 0.0, "distributions_income_usd": 0.0, "cash_only": 1.0})
        amt = float(r["amount_usd"]) / 1e6
        if r["movement"] == "capital call":
            x["contributions_investments_usd"] += amt      # the cash does not split investments from fees
        else:
            x["distributions_return_of_capital_usd"] += amt
    L["st"] = st
    # managers' activity at fund level (USD m)
    act = defaultdict(list); loans = defaultdict(list)
    for r in rows(P("manager_portfolio_activity_2013_2026.csv")):
        q = q_of(D(r["date"]))
        if r["record_type"] in ("asset loan drawn", "asset loan refinanced"):
            loans[(r["fund_id"], r["portfolio_company"])].append((q, r["record_type"], float(r["amount_usd_m"]), q_of(D(r["loan_maturity"]))))
            continue
        if r["record_type"] == "refinancing proceeds":
            loans[(r["fund_id"], r["portfolio_company"])].append((q, "proceeds", float(r["amount_usd_m"]), None))
            continue
        act[r["fund_id"]].append((q, r["record_type"], r["portfolio_company"], float(r["amount_usd_m"]),
                                  float(r["cost_basis_usd_m"]) if r["cost_basis_usd_m"] else 0.0))
    L["act"] = act; L["loans"] = loans
    aud = defaultdict(dict)
    for r in sheet(P("fund_audited_financials_FY2013_FY2026.xlsx"), "Audited accounts"):
        d = r["Fiscal year end"]; d = d.date() if hasattr(d, "date") else d
        aud[r["Fund ID"]][q_of(d)] = {k.replace(" (USD thousands)", ""): (float(v) / 1000.0 if isinstance(v, (int, float)) else v) for k, v in r.items()}
    L["aud"] = aud
    mk = rows(P("market_series_quarterly_2000Q1_2026Q4.csv"))
    L["E"] = np.array([float(r["exit_activity_index_2015_100"]) for r in mk]); L["S"] = np.array([float(r["public_equity_total_return_index"]) for r in mk])
    L["R"] = np.array([float(r["short_rate_pct"]) for r in mk])
    # the benchmark, one tuple per fund-quarter in fund and date order: (fund, strategy, vintage, quarter, contributions, distributions, value)
    L["bench"] = sorted(((r["benchmark_fund"], STRATS[r["strategy"]], int(r["vintage"]), q_of(D(r["period_end"])),
                          float(r["contributions_pct_of_commitment"]), float(r["distributions_pct_of_commitment"]), float(r["nav_pct_of_commitment"]))
                         for r in rows(P("industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv"))), key=lambda t: (t[0], t[3]))
    L["hold"] = sheet(P("liquid_holdings_2026-12-31.xlsx"))
    L["spend"] = {int(r["fiscal_year"]): float(r["approved_distribution_usd_m"]) for r in rows(P("spending_distributions_FY2014_FY2027.csv"))}
    L["programs"] = []
    for r in sheet(P("corrigan_hart_pacing_plan_2027.xlsx"), "Programs"):
        if r["Program"]: L["programs"].append(dict(code=r["Program"], desc=r["Description"], funds=[x.strip() for x in str(r["Funds committed in 2027"]).split(";")],
                                                     total=float(r["Total (USD m)"])))
    L["plan"] = []
    for r in sheet(P("corrigan_hart_pacing_plan_2027.xlsx"), "2027 proposed commitments"):
        if r["Fund"] == "Total" or not r["Strategy"]: continue
        qn, yr = r["Fund's first close (manager's schedule)"].split()
        L["plan"].append(dict(fund=r["Fund"], mgr=r["Manager"], st=STRATS[r["Strategy"]], C=float(r["Proposed commitment (USD m)"]),
                              exp_fc=qi(int(yr), int(qn[1]))))
    return L

# ------------------------------------------------------------------------------------------------ the policy's fixed parts
FACTORS = {"Cash, money market funds and US Treasuries": 1.00, "Investment-grade bonds": 0.90, "Public equities": 0.70,
           "Hedge funds: redeemable within 24 months": 0.90}
CUSHION = 1170.0
IP_YEARS = {"BO": 5, "GE": 5, "VC": 5, "RE": 4, "IN": 5, "PC": 3}

def reserve(L):
    return sum(float(h["Market value 31 Dec 2026 (USD m)"]) * FACTORS.get(h["Policy liquidity class"], 0.0)
               for h in L["hold"] if h["Policy liquidity class"])

def spending24(L):
    return 2.0 * L["spend"][2027]

def share(L, fid):
    r = L["reg"][fid]
    return float(r["Commitment (USD m)"]) / float(r["Fund size (USD m)"])

def stress_market(L):
    """the policy's scenario (section 6): exits as 2008Q3-2010Q2 relative to 2008Q2 on the 2026Q4 level; equities 85, 70,
    then five points a quarter back to 100 percent; short rates up 2.5 points."""
    E, S, R = L["E"], L["S"], L["R"]
    e = np.concatenate([E, np.zeros(8)]); s = np.concatenate([S, np.zeros(8)]); r = np.concatenate([R, np.zeros(8)])
    eq = [0.85, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    for k in range(8):
        e[H_END + 1 + k] = E[H_END] * E[qi(2008, 3) + k] / E[qi(2008, 2)]
        s[H_END + 1 + k] = S[H_END] * eq[k]
        r[H_END + 1 + k] = R[H_END] + 2.5
    return e, s, r

def bench_rates(L, field="dist", years=None, basis="value", q0=None, n=8):
    """the benchmark's rate by strategy for each of n quarters from q0 (2008Q3): the funds' distributions (field "dist") or
    contributions ("calls") in the quarter over their value at the end of the previous quarter, each summed over the
    strategy's funds (sections 7 and 8). years: only funds whose vintage year is that many years or more before the
    quarter's year (section 8's funds past their investment periods). basis "unfunded": over the commitment not yet called."""
    q0 = qi(2008, 3) if q0 is None else q0
    num = defaultdict(float); den = defaultdict(float)
    prev = None; paid = 0.0
    for (key, st, vint, q, c, d, nav) in L["bench"]:
        if prev is None or prev[0] != key:
            prev = None; paid = 0.0
        if q0 <= q < q0 + n and prev is not None and prev[1] == q - 1 and (years is None or (Q0 + q // 4) - vint >= years):
            num[(st, q - q0)] += d if field == "dist" else c
            den[(st, q - q0)] += prev[2] if basis == "value" else (100.0 - paid)
        paid += c; prev = (key, q, nav)
    return {k: num[k] / den[k] for k in den if den[k] > 0}

def bench_rate_normal(L, years, q0, q1):
    """the same funds' contributions over their previous quarter's value, pooled over the quarters q0 to q1, by strategy."""
    num = defaultdict(float); den = defaultdict(float); prev = None
    for (key, st, vint, q, c, d, nav) in L["bench"]:
        if prev is None or prev[0] != key: prev = None
        if q0 <= q <= q1 and prev is not None and prev[1] == q - 1 and (Q0 + q // 4) - vint >= years:
            num[st] += c; den[st] += prev[2]
        prev = (key, q, nav)
    return {k: num[k] / den[k] for k in den if den[k] > 0}

# ------------------------------------------------------------------------------------------------ R1
def unfunded(L):
    by = defaultdict(float); pend = defaultdict(float)
    for fid, r in L["reg"].items():
        st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"])
        if r["Status"] == "liquidated":
            by[st] += 0.0; continue
        paid = sum(v["contributions_investments_usd"] + v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"]
                   for v in L["st"].get(fid, {}).values())
        by[st] += C - paid
        if r["Status"] == "pending first close":
            pend[st] += C
    return dict(by), dict(pend)

def unfunded_quick(L):
    """the latest statement's unfunded figure for each fund with statements, and the register's commitment for pending
    funds (the custodian's fourth-quarter cash left out)."""
    by = defaultdict(float)
    for fid, r in L["reg"].items():
        st = STRATS[r["Strategy"]]
        if r["Status"] == "pending first close":
            by[st] += float(r["Commitment (USD m)"]); continue
        s = L["st"].get(fid, {})
        qs = [q for q in s if "unfunded_commitment_usd" in s[q]]
        if qs: by[st] += s[max(qs)]["unfunded_commitment_usd"]
    return dict(by)

# ------------------------------------------------------------------------------------------------ the credit facilities
def gap_series(L, fid):
    """the endowment's share of the manager's investments less its investment contributions, cumulated by quarter,
    with the realisations, for the fund's life to date."""
    sh = share(L, fid)
    inv = defaultdict(float); proc = defaultdict(float)
    for q, t, co, a, cb in L["act"][fid]:
        if t in ("initial investment", "follow-on investment"): inv[q] += a * sh
        elif t == "realization": proc[q] += a * sh
    calls = {q: v["contributions_investments_usd"] for q, v in L["st"].get(fid, {}).items()}
    qs = sorted(set(inv) | set(calls) | set(proc))
    out, ci, cc, cp = {}, 0.0, 0.0, 0.0
    if not qs: return out
    for q in range(qs[0], H_END + 1):
        ci += inv.get(q, 0.0); cc += calls.get(q, 0.0); cp += proc.get(q, 0.0)
        out[q] = (ci - cc, cp, proc.get(q, 0.0))
    return out

def line_stock(L, recycling="none"):
    """the capital each manager has invested through its fund's credit facility and not yet called, at the endowment's
    share, at 31 December 2026, as policy section 8 files it: the borrowings on the fund's latest audited balance sheet,
    plus its investments since and less the capital called for investments since, never less than nil; a fund with no
    audited balance sheet counted the same way from its first investment; no allowance for proceeds reinvested since.
    Readings the sentence rules out: recycling "manager" (the proceeds since the last audit reinvested at the manager's
    own audited rate while the fund is still investing) and "gap" (the investments less the capital called for them
    over the fund's whole life, the audited borrowings set aside)."""
    res = {}; rho_m = defaultdict(list); per = {}
    for fid, r in L["reg"].items():
        if r["Status"] == "pending first close": continue
        g = gap_series(L, fid)
        if not g: continue
        sh = share(L, fid); aud = L["aud"].get(fid, {})
        ip_end = _qd(r["Investment period ends"])
        pts = []
        for qa, a_ in sorted(aud.items()):
            if qa in g:
                gap, cp, _ = g[qa]
                pts.append((qa, gap - a_["Credit facility borrowings"] * sh, cp, a_["Credit facility borrowings"] * sh))
        per[fid] = dict(g=g, pts=pts, sh=sh, ip_end=ip_end, mgr=r["Manager"], size=float(r["Fund size (USD m)"]))
        if pts and pts[-1][2] > 0:
            cp_ip = sum(g[q][2] for q in g if q <= min(pts[-1][0], ip_end))
            if cp_ip > 1e-6:
                rho_m[r["Manager"]].append(max(pts[-1][1], 0.0) / cp_ip)
    for fid, x in per.items():
        g, pts, sh = x["g"], x["pts"], x["sh"]
        if recycling == "gap":
            res[fid] = max(g[H_END][0], 0.0); continue
        if pts: qa, rec = pts[-1][0], pts[-1][1]
        else: qa, rec = min(g) - 1, 0.0
        if recycling == "manager":
            rho = float(np.median(rho_m[x["mgr"]])) if rho_m.get(x["mgr"]) else 0.0
            cap = 0.15 * x["size"] * sh
            for q in range(qa + 1, H_END + 1):
                if q <= x["ip_end"]: rec = min(rec + rho * g[q][2], cap)
        res[fid] = max(g[H_END][0] - rec, 0.0)
    return res, per

def audited_stock(L):
    """the hurried facility balance: each fund's latest audited borrowings at the endowment's share, carried to 31
    December 2026 as they stand."""
    out = {}
    for fid, r in L["reg"].items():
        aud = L["aud"].get(fid, {})
        if r["Status"] in ("pending first close", "liquidated") or not aud: continue
        out[fid] = aud[max(aud)]["Credit facility borrowings"] * share(L, fid)
    return out

# ------------------------------------------------------------------------------------------------ the pace of new investments
def pace_cells(L, numerator="all", min_room=0.0, room="invested", weight="share", shift=0, mean=False):
    """policy section 8: by strategy and year since first close, over the quarters the endowment's funds spent in their
    investment periods, their investments (first and follow-on) in the quarter over their commitments not yet invested at
    its start, each summed. Variants: numerator "first" (first investments only); room "called" (over the commitment not
    yet called); weight "fund" (summed at fund level, not at the endowment's share); shift 1 (years counted from the
    quarter after the first close); mean (the average of the fund-quarters' own rates, not the ratio of sums)."""
    num = defaultdict(float); den = defaultdict(float); n = defaultdict(int); own = defaultdict(list)
    for fid, r in L["reg"].items():
        if not r["First close"] or not r["Fund size (USD m)"]: continue
        st = STRATS[r["Strategy"]]; sh = share(L, fid)
        w = sh if weight == "share" else 1.0
        C = float(r["Fund size (USD m)"]) * w
        fc = _qd(r["First close"]); ipl = _qd(r["Investment period ends"])
        inv = defaultdict(float); allinv = defaultdict(float)
        for q, t, co, a, cb in L["act"].get(fid, []):
            if t == "initial investment": inv[q] += a * w; allinv[q] += a * w
            elif t == "follow-on investment":
                allinv[q] += a * w
                if numerator == "all": inv[q] += a * w
        s = L["st"].get(fid, {})
        cum = 0.0
        for q in range(fc, min(ipl, H_END) + 1):
            a = max((q - fc - shift) // 4, 0)
            left = max(C - cum, 0.0)
            if left > min_room * C:
                num[(st, a)] += inv.get(q, 0.0); den[(st, a)] += left; n[(st, a)] += 1
                if left > 0: own[(st, a)].append(inv.get(q, 0.0) / left)
            if room == "called":
                v = s.get(q, {})
                cum += (v.get("contributions_investments_usd", 0.0) + v.get("contributions_management_fees_usd", 0.0) + v.get("contributions_fund_expenses_usd", 0.0)) * (w / sh)
            else:
                cum += allinv.get(q, 0.0)
    if mean: return {k: float(np.mean(v)) for k, v in own.items()}, dict(n)
    return {k: num[k] / den[k] for k in den if den[k] > 0}, dict(n)

def _cell(tab, st, a):
    for aa in range(min(a, 11), -1, -1):
        if (st, aa) in tab: return tab[(st, aa)]
    return 0.0

def fee_rates(L):
    """management fees and fund expenses per quarter as a share of the commitment while a fund is investing, by strategy
    (the median over the endowment's fund-quarters, statements only)."""
    fee = defaultdict(list); exp = defaultdict(list)
    for fid, r in L["reg"].items():
        if not r["First close"]: continue
        st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"])
        fc = _qd(r["First close"]); ipl = _qd(r["Investment period ends"])
        for q, v in L["st"].get(fid, {}).items():
            if v.get("cash_only") or q <= fc or q > ipl: continue
            fee[st].append(v["contributions_management_fees_usd"] / C); exp[st].append(v["contributions_fund_expenses_usd"] / C)
    return {k: float(np.median(v)) for k, v in fee.items()}, {k: float(np.median(v)) for k, v in exp.items()}

# ------------------------------------------------------------------------------------------------ fund states
def held_cost(L, fid):
    """the cost of the companies and assets the fund still holds at 31 December 2026, at the endowment's share."""
    sh = share(L, fid); cost = defaultdict(float); gone = set()
    for q, t, co, a, cb in L["act"].get(fid, []):
        if t in ("initial investment", "follow-on investment"): cost[co] += a * sh
        elif t == "realization": gone.add(co)
    return sum(v for c, v in cost.items() if c not in gone)

def fund_state(L, fid, stock):
    r = L["reg"][fid]; st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"])
    s = L["st"].get(fid, {})
    paid = sum(v["contributions_investments_usd"] + v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"] for v in s.values())
    full = [q for q in s if "ending_nav_usd" in s[q]]
    navq = max(full, default=None)
    nav = s[navq]["ending_nav_usd"] if navq is not None else 0.0
    if navq is not None and navq < H_END:          # a fourth-quarter statement still to come: roll the cash (section 7)
        x = s.get(H_END, {})
        nav += x.get("contributions_investments_usd", 0.0) - x.get("distributions_return_of_capital_usd", 0.0)
    fc = _qd(r["First close"]); ipl = _qd(r["Investment period ends"])
    sh = C / float(r["Fund size (USD m)"]) if r["Fund size (USD m)"] else None
    inv = sum(a for q, t, co, a, cb in L["act"].get(fid, []) if t in ("initial investment", "follow-on investment")) * (sh or 0)
    fee_q = s[navq]["contributions_management_fees_usd"] if navq is not None else 0.0
    exp_q = s[navq]["contributions_fund_expenses_usd"] if navq is not None else 0.0
    yrs = r["Investment period (years, per agreement)"]
    return dict(fid=fid, st=st, C=C, paid=paid, unf=C - paid, nav=nav, fc=fc, ipl=ipl, sh=sh, inv=inv, mgr=r["Manager"], term=_qd(r["Term ends"]),
                agreed=(fc + 4 * int(yrs) - 1) if (fc is not None and yrs) else None,
                stock=stock.get(fid, 0.0), fee_q=fee_q, exp_q=exp_q, cost=held_cost(L, fid) if sh else 0.0,
                pending=(r["Status"] == "pending first close"), liquidated=(r["Status"] == "liquidated"),
                exp_fc=_qd(r["First close expected at commitment"]))

# ------------------------------------------------------------------------------------------------ first closes (a variant only)
def slip_window(E, e, win):
    return float(np.mean([E[max(e - k, 0)] for k in range(1, win + 1)]))

def slip_model(L, wins=(1, 2, 3, 4), refs=(90.0, 95.0, 100.0, 105.0, 110.0)):
    """quarters of slip (first close against the date given at commitment) on how far the exit market sat below normal
    over the quarters before the expected close: least squares with an intercept, the window and the reference by fit.
    The policy takes first closes on their managers' dates (section 8); this is the reading it rules out."""
    best = None
    for win in wins:
        for ref in refs:
            pts = []
            for fid, r in L["reg"].items():
                if not r["First close"]: continue
                ex = _qd(r["First close expected at commitment"])
                pts.append((max(0.0, 1.0 - slip_window(L["E"], ex, win) / ref), _qd(r["First close"]) - ex))
            x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
            X = np.column_stack([np.ones(len(x)), x]); coef, *_ = np.linalg.lstsq(X, y, rcond=None)
            sse = float(np.sum((y - X @ coef) ** 2))
            if best is None or sse < best[0]: best = (sse, float(coef[0]), float(coef[1]), win, ref)
    return dict(a=best[1], b=best[2], win=best[3], ref=best[4], sse=best[0])

def closes(fit, e, exp_q, sw):
    """the first-close quarters with their weights: the manager's date (section 8), or slipped on the stress."""
    if sw.get("closes", "manager") == "manager": return [(exp_q, 1.0)]
    sl = fit["slip"]; x = max(sl["a"] + sl["b"] * max(0.0, 1.0 - slip_window(e, exp_q, sl["win"]) / sl["ref"]), 0.0)
    k = int(math.floor(x)); fr = x - k
    return [(exp_q + k, 1.0 - fr), (exp_q + k + 1, fr)] if fr > 1e-9 else [(exp_q + k, 1.0)]

# ------------------------------------------------------------------------------------------------ the successor clause
def successions(L):
    """each registered fund's successor (its manager's next fund by vintage; after a manager's last registered fund, its
    re-up in the plan) and, manager by manager, whether the agreement ends a fund's investment period when its successor
    holds its first close: read off every past fund whose successor closed before the fund's period would otherwise have
    ended (the register then shows the period ending the quarter before the successor's close, or running on)."""
    by = defaultdict(list)
    for fid, r in L["reg"].items(): by[r["Manager"]].append(r)
    succ, votes = {}, defaultdict(list)
    for m, rs in by.items():
        rs = sorted(rs, key=lambda r: (r["Vintage"], r["Fund ID"]))
        for a, b in zip(rs[:-1], rs[1:]):
            succ[a["Fund ID"]] = ("reg", b["Fund ID"])
            fa, fb, ie = _qd(a["First close"]), _qd(b["First close"]), _qd(a["Investment period ends"])
            if fa is None or fb is None or ie is None: continue
            agreed = fa + 4 * int(a["Investment period (years, per agreement)"])
            if fb < max(agreed, ie + 1):
                votes[m].append(ie + 1 == fb)
        last = rs[-1]["Fund ID"]
        for p in L["plan"]:
            if p["mgr"] == m: succ[last] = ("plan", p["fund"])
    clause = {m: (bool(all(v)) if v else None) for m, v in votes.items()}
    return succ, clause, {m: (sum(v), len(v)) for m, v in votes.items()}

def successor_close(L, fit, e, fid, sw):
    """the quarters the fund's successor holds its first close, with weights; None where it already closed by the end of
    2026 or there is none."""
    s = fit["succ"].get(fid)
    if s is None: return None
    kind, ref = s
    if kind not in sw.get("successors", ("reg", "plan")): return None
    if kind == "reg":
        r = L["reg"][ref]
        if r["First close"]: return None
        exp = _qd(r["First close expected at commitment"])
    else:
        exp = next(p["exp_fc"] for p in L["plan"] if p["fund"] == ref)
    return closes(fit, e, exp, sw)

def successor_events(L, fit, mkt, sw=None):
    """the funds whose investment period the successor's first close ends inside the eight quarters."""
    sw = sw or GOLDEN; out = []
    for fid, r in L["reg"].items():
        if r["Status"] != "investing" or not fit["clause"].get(r["Manager"]): continue
        sc = successor_close(L, fit, mkt[0], fid, sw); ipl = _qd(r["Investment period ends"])
        if not sc or ipl is None: continue
        q_exp = sum(q * w for q, w in sc)
        if q_exp <= ipl and q_exp <= W[-1]:
            s = fit["succ"][fid]
            out.append(dict(fid=fid, fund=r["Fund"], manager=r["Manager"], successor=s[1] if s[0] == "plan" else L["reg"][s[1]]["Fund"],
                            close=round(q_exp, 2), registered_end=ipl))
    return out

# ------------------------------------------------------------------------------------------------ the real assets' loans
def asset_loans(L):
    """per real-estate and infrastructure asset: its loan's balance and maturity after the last draw or refinancing, and
    every refinancing with the balance it replaced (fund level, USD m)."""
    out = {}
    for (fid, co), ev in L["loans"].items():
        ev = sorted(ev, key=lambda x: (x[0], 0 if x[1] == "proceeds" else 1))
        bal, mat, refis = None, None, []
        for q, t, a, m in ev:
            if t == "proceeds": continue
            if t == "asset loan refinanced" and bal is not None:
                refis.append(dict(q=q, old=bal, new=a, due=mat))
            bal, mat = a, m
        out[(fid, co)] = dict(balance=bal, maturity=mat, refis=refis)
    return out

def _equity_vals(L):
    """{(fund, asset): {quarter: equity valuation, fund level}} for the real assets, and their exits."""
    vals, gone = defaultdict(dict), set()
    for fid, ev in L["act"].items():
        r = L["reg"].get(fid)
        if not r or STRATS[r["Strategy"]] not in REAL: continue
        for q, t, co, a, cb in ev:
            if t == "valuation": vals[(fid, co)][q] = a
            elif t == "realization": gone.add((fid, co))
    return vals, gone

def lender_rule(L, since=None, table=None):
    """the loan-to-value lenders have granted at each refinancing: the new balance over the asset's value then (its
    equity valuation at the end of the quarter before plus the loan it replaced), against the short rate. Fitted as
    min(cap, kappa / (r + spread)) on the refinancings since mid-2022, by least squares over a grid of cap and spread."""
    since = qi(2022, 3) if since is None else since
    vals, _ = _equity_vals(L); pts = []
    for (fid, co), x in asset_loans(L).items():
        for rf in x["refis"]:
            v = vals.get((fid, co), {}).get(rf["q"] - 1)
            if v is None: continue
            gross = v + rf["old"]
            if gross > 0: pts.append((rf["q"], float(L["R"][rf["q"]]), rf["new"] / gross, fid, co))
    post = [p for p in pts if p[0] >= since]
    if len(post) < 4: post = [p for p in pts if p[0] >= qi(2020, 1)] or pts     # too few recent refinancings to read
    best = None
    for cap in np.round(np.arange(0.55, 0.851, 0.005), 3):
        for s_ in np.round(np.arange(1.0, 3.01, 0.25), 2):
            lo = [p for p in post if p[2] < cap - 0.01]
            if not lo: continue
            k = float(np.median([p[2] * (p[1] + s_) for p in lo]))
            sse = float(sum((min(cap, k / (p[1] + s_)) - p[2]) ** 2 for p in post))
            if table is not None: table.append((float(cap), float(s_), k, sse))
            if best is None or sse < best[0]: best = (sse, float(cap), float(s_), k)
    if best is None: return None
    sse, cap, s_, k = best
    return dict(cap_post=cap, kappa=k, spread=s_, sse=sse, n=len(post), n_all=len(pts), pts=pts)

def refinancing_table(L, fit):
    """every past refinancing the lenders' limit is read from: the loan replaced, the new loan, the asset's value then (the
    fund's valuation of its holding at the end of the quarter before plus the loan replaced), the new loan over that
    value, the short rate and the fitted limit at it (fund level, USD m)."""
    vals, _ = _equity_vals(L); lr = fit["lender"]; out = []
    for (fid, co), x in sorted(asset_loans(L).items()):
        for rf in x["refis"]:
            v = vals.get((fid, co), {}).get(rf["q"] - 1)
            if v is None or v + rf["old"] <= 0: continue
            rate = float(L["R"][rf["q"]])
            out.append(dict(fid=fid, co=co, q=rf["q"], old=rf["old"], new=rf["new"], value=v + rf["old"], ltv=rf["new"] / (v + rf["old"]),
                            rate=rate, limit=min(lr["cap_post"], lr["kappa"] / (rate + lr["spread"])), fitted=rf["q"] >= qi(2022, 3)))
    return sorted(out, key=lambda r: (r["q"], r["fid"], r["co"]))

def facility_table(L, per):
    """the facility balance of policy section 8 fund by fund: the latest audited year-end, the borrowings on it, the
    investments since and the capital called for investments since, all at the endowment's share (USD m)."""
    out = {}
    for fid, x in per.items():
        g, pts = x["g"], x["pts"]
        if pts: qa, bor, g0 = pts[-1][0], pts[-1][3], g[pts[-1][0]][0]
        else: qa, bor, g0 = None, 0.0, 0.0
        inv = defaultdict(float)
        for q, t, co, a, cb in L["act"][fid]:
            if t in ("initial investment", "follow-on investment") and (qa is None or q > qa): inv[fid] += a * x["sh"]
        d_inv = inv[fid]; d_call = d_inv - (g[H_END][0] - g0)
        out[fid] = dict(audit=qa, borrowings=bor, invested_since=d_inv, called_since=d_call, balance=max(bor + d_inv - d_call, 0.0))
    return out

def value_response(L, lag=1, min_age=17):
    """the quarterly change in the real assets' value (equity valuation plus loan) against the change in equities and in
    the short rate, on assets past their four-year plan: log value change = beta x log equity change (a quarter late) +
    log((1 + c r[q-2]) / (1 + c r[q-1])), beta and c by least squares over a grid of c."""
    vals, _ = _equity_vals(L); bal = {}
    for key, ev in L["loans"].items():
        bal[key] = [(q, a) for q, t, a, m in sorted(ev, key=lambda x: x[0]) if t != "proceeds"]
    obs = []
    for key, vs in vals.items():
        b = bal.get(key)
        if not b: continue
        first = b[0][0]
        def loan_at(q):
            x = None
            for qq, a in b:
                if qq <= q: x = a
            return x
        for q in sorted(vs):
            if q - 1 in vs and q - first >= min_age:
                d1, d0 = loan_at(q), loan_at(q - 1)
                if d1 is None or d0 is None or abs(d1 - d0) > 1e-6: continue
                g1, g0 = vs[q] + d1, vs[q - 1] + d0
                if g1 > 0 and g0 > 0: obs.append((q, math.log(g1 / g0)))
    best = None
    S, R = L["S"], L["R"]
    for c in np.round(np.arange(0.0, 0.151, 0.005), 3):
        X = np.array([math.log(S[q - lag] / S[q - lag - 1]) for q, _ in obs])
        Y = np.array([y - math.log((1 + c * R[q - lag - 1]) / (1 + c * R[q - lag])) for q, y in obs])
        beta = float(np.sum(X * Y) / np.sum(X * X)); sse = float(np.sum((Y - beta * X) ** 2))
        if best is None or sse < best[0]: best = (sse, float(c), beta)
    return dict(c=best[1], beta=best[2], n=len(obs), lag=lag, sse=best[0])

def loans_due(L, fid):
    """the fund's real-asset loans alive at 31 December 2026 that mature after it: balance and maturity at the endowment's
    share and the asset's value at 31 December 2026 (its valuation plus the loan)."""
    vals, gone = _equity_vals(L); sh = share(L, fid); out = []
    for (f2, co), x in asset_loans(L).items():
        if f2 != fid or (f2, co) in gone or x["balance"] is None: continue
        if x["maturity"] is None or x["maturity"] <= H_END: continue
        vs = vals.get((f2, co), {})
        if not vs: continue
        out.append(dict(co=co, D=x["balance"] * sh, due=x["maturity"], P26=(vs[max(vs)] + x["balance"]) * sh))
    return out

def refi_terms(fit, mkt, ln, q, terms="stressed"):
    """the asset's value and the loan-to-value a lender grants on it when its loan matures at quarter q (the value at the
    end of 2026 moved on the stress path's equities and short rate; "current": the terms and values of 31 December)."""
    e, s, r = mkt; vr, lr = fit["value"], fit["lender"]
    lg = vr.get("lag", 1)
    P = ln["P26"] if terms in ("current", "values_flat") else \
        ln["P26"] * (s[q - lg] / s[H_END - lg]) ** vr["beta"] * (1 + vr["c"] * r[H_END - lg]) / (1 + vr["c"] * r[q - lg])
    rate = r[H_END] if terms in ("current", "terms_flat") else r[q]
    return P, min(lr["cap_post"], lr["kappa"] / (rate + lr["spread"]))

def refi_gap(fit, mkt, ln, q, terms="stressed"):
    P, lim = refi_terms(fit, mkt, ln, q, terms)
    return max(ln["D"] - lim * P, 0.0)

# ------------------------------------------------------------------------------------------------ extensions
def extension_points(L):
    """every fund whose agreed investment period ended by the end of 2026 and was not ended sooner by its successor's first
    close: whether the register shows it extended, the share of its commitment invested by the agreed end and the exit
    index over the quarters before it."""
    out = []
    for fid, r in L["reg"].items():
        if not r["First close"] or not r["Investment period ends"] or not r["Investment period (years, per agreement)"]: continue
        fc = _qd(r["First close"]); ipl = _qd(r["Investment period ends"])
        agreed = fc + 4 * int(r["Investment period (years, per agreement)"])
        if agreed > H_END or ipl + 1 < agreed: continue
        C = float(r["Commitment (USD m)"]); sh = share(L, fid)
        inv = sum(a_ * sh for q, t, co, a_, cb in L["act"].get(fid, []) if t in ("initial investment", "follow-on investment") and q < agreed) / C
        out.append((ipl + 1 > agreed, inv, {w_: float(np.mean([L["E"][agreed - k] for k in range(1, w_ + 1)])) for w_ in (1, 2, 4)}, fid,
                    (ipl + 1 - agreed) if ipl + 1 > agreed else 0))
    return out

def extension_rule(L):
    """the rule that sorts the register's extended periods from the rest: an extension when the exit index over the
    quarters before the agreed end (the window by fit) sits below e_star and the fund has invested less than s_star of
    its commitment, each threshold set midway between the nearest cases either side; the length is the register's own."""
    pts = extension_points(L)
    best = None
    for win in (1, 2, 4):
        for e_star in (80.0, 85.0, 90.0, 95.0, 100.0, 105.0):
            for s_star in np.round(np.arange(0.50, 0.95, 0.01), 2):
                ok = sum((p[2][win] < e_star and p[1] < s_star) == p[0] for p in pts)
                if best is None or ok > best[0]: best = (ok, win, e_star, float(s_star))
    ok, win, e0, s0 = best
    ext = [p for p in pts if p[0]]
    if ext:
        hi_s = max(p[1] for p in ext); lo_s = min([p[1] for p in pts if not p[0] and p[2][win] < e0 and p[1] > hi_s] or [s0])
        hi_e = max(p[2][win] for p in ext); lo_e = min([p[2][win] for p in pts if not p[0] and p[1] < s0 and p[2][win] > hi_e] or [e0])
        s_star, e_star = (hi_s + lo_s) / 2.0, (hi_e + lo_e) / 2.0
        length = int(np.median([p[4] for p in ext]))
    else:
        s_star, e_star, length = s0, e0, 4
    return dict(win=win, e_star=float(e_star), s_star=float(s_star), length=length, accuracy=ok / float(len(pts)), n=len(pts), extended=len(ext))

# ------------------------------------------------------------------------------------------------ the projection
GOLDEN = dict(succession="clause", refi="loans", closes="manager", old="benchmark", recycle="none", extensions="none", cap=True, fees_post="flat")
# the careful but hurried route: every convention of section 8 applied as filed and every reflex set right; every investment
# period held to the end the register records and the real-asset loans carried as they stand
REFLEX = dict(GOLDEN, succession="registered", refi="none")
COMPS = ("call_inv", "call_pend", "call_plan", "dist", "stock", "new", "fees", "old", "refi", "extended", "recycled")

def project(L, states, plan, sw, fit, mkt):
    """the policy's eight quarters, fund by fund. A fund in its investment period calls its new investments (the pace of its
    strategy and year since first close on its commitment not yet invested), its fee and its expenses; a buyout, growth or
    venture fund past its investment period calls its 31 December value times the benchmark rate of section 8; any other
    fund past its period calls the fee and expenses of its latest statement (section 8); a real-asset loan that falls due is
    refinanced at the lenders' limit on the asset's value then and the shortfall called; the facility balance is called in
    the first quarter; no fund calls more than its commitment has left. Distributions are section 7's."""
    e, s, r = mkt
    out = {k: np.zeros(len(e)) for k in COMPS}
    pace, crate, drate = fit["pace"], fit["crate"], fit["drate"]
    def run(key, st, C, fc, paid, inv, nav0, stock, fee_q, exp_q, cost, mgr, ipl, agreed, term, succ_q, loans, wt):
        if succ_q is not None and succ_q - 1 < ipl: ipl = succ_q - 1          # the successor's first close ends the period
        ended_early = ipl < agreed
        lns = [dict(l) for l in (loans or [])]
        rec_c = 0.0
        for k, q in enumerate(W):
            dx = nav0 * drate.get((st, k), 0.0)
            out["dist"][q] += dx * wt
            if q < fc: continue
            if term is not None and q > term: continue       # the term has ended: the commitment not called is released
            if sw.get("extensions") == "rule" and q == agreed + 1 and ipl == agreed and not ended_early:
                ex = fit["ext"]
                weak = float(np.mean([e[q - j] for j in range(1, ex["win"] + 1)])) < ex["e_star"]
                if weak and inv / C < ex["s_star"]:
                    ipl = agreed + ex["length"]; out["extended"][q] += C * wt
            left = max(C - paid, 0.0)
            stk = stock if k == 0 else 0.0
            I = fee = old = rc = 0.0
            if q <= ipl:
                I = _cell(pace, st, (q - fc) // 4) * max(C - inv, 0.0)
                fee = fee_q + exp_q
                if sw.get("recycle") == "manager":
                    rc = min(fit["rho"].get(mgr, fit["rho_default"]) * dx, max(0.15 * C - rec_c, 0.0), I); rec_c += rc
            elif (st in EQUITY and sw.get("old") != "none") or sw.get("old") == "all":
                old = nav0 * crate.get((st, k), 0.0)
                if sw.get("old_fees"): fee = fee_q + exp_q          # a reading section 8 rules out: the fund's fee on top of the rate
            else:
                fee = (fit["fee"][st] * cost if sw.get("fees_post") == "cost" else fee_q) + exp_q
            # what the commitment has left goes to the facility balance first, then the fee, then the benchmark's rate, then the
            # investments, and last to a maturing loan's shortfall (sw "order": "shortfall_first" pays the shortfall before the rest)
            parts = [stk, fee, old, max(I - rc, 0.0)]
            first = sw.get("order") == "shortfall_first"
            def pay_gaps(room_):
                paid_ = 0.0
                if lns and sw.get("refi") != "none":
                    for ln in lns:
                        if ln["due"] != q: continue
                        gap = refi_gap(fit, mkt, ln, q, terms=sw["refi"] if sw["refi"] in ("current", "values_flat", "terms_flat") else "stressed") * sw.get("gap_scale", 1.0)
                        pay = min(gap, max(room_ - paid_, 0.0)) if sw.get("cap", True) else gap
                        paid_ += pay; ln["D"] -= pay
                        ln["due"] = q + 4 if pay < gap - 1e-9 else None      # a shortfall the fund cannot meet waits a year
                return paid_
            gap_paid = pay_gaps(left) if first else 0.0
            if sw.get("cap", True):
                room = left - gap_paid
                for i, v in enumerate(parts):
                    parts[i] = min(v, room); room -= parts[i]
            if not first: gap_paid = pay_gaps(left - sum(parts))
            call = sum(parts) + gap_paid
            paid += call; inv += I; cost += I + gap_paid
            out[key][q] += call * wt; out["stock"][q] += parts[0] * wt; out["fees"][q] += parts[1] * wt; out["old"][q] += parts[2] * wt
            out["new"][q] += parts[3] * wt; out["refi"][q] += gap_paid * wt; out["recycled"][q] += rc * wt
    for x in states:
        if x.get("liquidated"): continue
        st = x["st"]
        if x["pending"]:
            for fc, wgt in closes(fit, e, x["exp_fc"], sw):
                last = fc + 4 * IP_YEARS[st] - 1
                run("call_pend", st, x["C"], fc, 0.0, 0.0, 0.0, 0.0, fit["fee"][st] * x["C"], fit["exp"][st] * x["C"], 0.0, x["mgr"], last, last, None, None, None, wgt)
        else:
            loans = [l for l in fit["loans"].get(x["fid"], [])] if st in REAL else None
            sc = None
            if sw.get("succession") == "clause" and fit["clause"].get(x["mgr"]):
                sc = successor_close(L, fit, e, x["fid"], sw)
            for sq, wgt in (sc or [(None, 1.0)]):
                run("call_inv", st, x["C"], x["fc"], x["paid"], x["inv"], max(x["nav"], 0.0), x["stock"], x["fee_q"], x["exp_q"], x["cost"], x["mgr"],
                    x["ipl"], x["agreed"], x["term"], sq, loans, wgt)
    for p in plan:
        st = p["st"]
        for fc, wgt in closes(fit, e, p["exp_fc"], sw):
            last = fc + 4 * IP_YEARS[st] - 1
            run("call_plan", st, p["C"], fc, 0.0, 0.0, 0.0, 0.0, fit["fee"][st] * p["C"], fit["exp"][st] * p["C"], 0.0, p.get("mgr", ""), last, last, None, None, None, wgt)
    return out

def fit_all(L):
    """every input the projection reads off the evidence or the policy's bases."""
    mkt = stress_market(L)
    stock, per = line_stock(L)
    succ, clause, votes = successions(L)
    pace, pace_n = pace_cells(L)
    fee, exp = fee_rates(L)
    rho = defaultdict(list)
    for fid, x in per.items():
        g, pts = x["g"], x["pts"]
        if not pts: continue
        qa, rec, cp, _ = pts[-1]
        cp_ip = sum(g[q][2] for q in g if q <= min(qa, x["ip_end"]))
        if cp_ip > 1e-6: rho[x["mgr"]].append(max(rec, 0.0) / cp_ip)
    rho = {m: float(np.median(v)) for m, v in rho.items()}
    fit = dict(pace=pace, pace_n=pace_n, fee=fee, exp=exp, drate=bench_rates(L, "dist"), crate=bench_rates(L, "calls", years=OLD_YEARS),
               succ=succ, clause=clause, clause_votes=votes, lender=lender_rule(L), value=value_response(L), ext=extension_rule(L),
               slip=slip_model(L), rho=rho, rho_default=float(np.median(list(rho.values()))) if rho else 0.0,
               loans={fid: loans_due(L, fid) for fid, r in L["reg"].items() if STRATS[r["Strategy"]] in REAL and r["Status"] in ("investing", "harvesting")})
    return fit, mkt, stock, per

def halves(v):
    return {h: round(float(v[W[2 * i:2 * i + 2]].sum()), 1) for i, h in enumerate(HALVES)}

def by_strategy(d):
    return {s: round(d.get(STRATS[s], 0.0), 1) for s in STRAT_ORDER}

def evaluate(L, sw, fit, mkt, stock):
    """the policy's test for every program on one route: the calls and distributions of the commitments made by the end
    of 2026 by half-year, the headroom above the minimum before any 2027 commitment, each program's calls and result, and
    the program the policy adopts."""
    states = [fund_state(L, fid, stock) for fid in L["reg"]]
    o = project(L, states, [], sw, fit, mkt)
    RES, SPEND = reserve(L), spending24(L)
    calls = o["call_inv"] + o["call_pend"]
    hv = halves(calls); dv = halves(o["dist"])
    need0 = round(sum(hv.values()) - sum(dv.values()), 1)          # from the half-year figures as stated, so the test adds line by line
    H0 = round(round(RES, 1) - round(SPEND + need0, 1) - CUSHION, 1)
    by_fund = {}
    for p in L["plan"]:
        by_fund[p["fund"]] = round(float(project(L, [], [p], sw, fit, mkt)["call_plan"][W].sum()), 1)
    progs = []
    for pr in L["programs"]:
        c = round(sum(by_fund[f] for f in pr["funds"]), 1)
        progs.append(dict(code=pr["code"], total=pr["total"], calls=c, headroom=round(H0 - c, 1), passes=H0 - c >= 0))
    passing = [p for p in progs if p["passes"]]
    adopt = max(passing, key=lambda p: p["total"])["code"] if passing else "none"
    # the two deciding judgments as results of their own: the funds whose periods a successor's first close ends and the
    # calls that takes off (the same route with every period held to its registered end, less this one), and the loans
    # falling due with the shortfalls called
    succ = dict(funds=0, calls_taken_off_usd_m=0.0)
    if sw.get("succession") == "clause":
        evs = successor_events(L, fit, mkt, sw)
        o2 = project(L, states, [], dict(sw, succession="registered"), fit, mkt)
        succ = dict(funds=len(evs), calls_taken_off_usd_m=round(sum(halves(o2["call_inv"] + o2["call_pend"]).values()) - sum(hv.values()), 1))
    refi = dict(loans_due=0, balance_due_usd_m=0.0, calls_usd_m=0.0)
    if sw.get("refi") != "none":
        due = [ln for lns in fit["loans"].values() for ln in lns if ln["due"] in W]
        refi = dict(loans_due=len(due), balance_due_usd_m=round(sum(ln["D"] for ln in due), 1), calls_usd_m=round(sum(halves(o["refi"]).values()), 1))
    return dict(R2={h: hv[h] for h in HALVES[:2]}, R3={h: hv[h] for h in HALVES[2:]}, R4=dv, R5=H0, R7=adopt, programs=progs,
                calls=hv, succ=succ, refi_res=refi,
                by_fund=by_fund, need0=round(need0, 1), closed=halves(o["call_inv"]), pending=halves(o["call_pend"]),
                stock=round(float(o["stock"][W].sum()), 1), new=halves(o["new"]), fees=halves(o["fees"]), old=halves(o["old"]), refi=halves(o["refi"]),
                extended=round(float(o["extended"][W].sum()), 1), calls_total=round(float(calls[W].sum()), 1))

# ------------------------------------------------------------------------------------------------ the textbook routes
def ta_fit(L, q_lo=None, q_hi=None):
    """calls in a quarter over the commitment not yet called at its start, by strategy and year since first close, from the
    capital accounts (optionally only the quarters inside a window)."""
    num = defaultdict(float); den = defaultdict(float)
    for fid, r in L["reg"].items():
        if not r["First close"]: continue
        st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"]); fc = _qd(r["First close"])
        s = L["st"].get(fid, {}); paid = 0.0
        for q in range(fc, H_END + 1):
            a = (q - fc) // 4; c = 0.0
            if q in s:
                c = s[q]["contributions_investments_usd"] + s[q]["contributions_management_fees_usd"] + s[q]["contributions_fund_expenses_usd"]
            if (q_lo is None or q >= q_lo) and (q_hi is None or q <= q_hi) and C - paid > 0.01 * C:
                num[(st, min(a, 9))] += c; den[(st, min(a, 9))] += C - paid
            paid += c
    return {k: num[k] / den[k] for k in den if den[k] > 0}

def bench_unfunded_rates(L):
    """the benchmark's contributions in each quarter of 2008Q3-2010Q2 over the commitment its funds had not yet called,
    by strategy and year of age."""
    num = defaultdict(float); den = defaultdict(float); prev = None; paid = 0.0
    for (key, st, vint, q, c, d, nav) in L["bench"]:
        if prev != key: paid = 0.0
        prev = key
        unf = 100.0 - paid
        if qi(2008, 3) <= q <= qi(2010, 2) and unf > 1.0:
            a = min((q - qi(vint, 1)) // 4, 9)
            num[(st, a, q - qi(2008, 3))] += c; den[(st, a, q - qi(2008, 3))] += unf
        paid += c
    return {k: num[k] / den[k] for k in den if den[k] > 0}

def rates_route(L, fit, stock, rate_of):
    """the policy's test with every fund and re-up calling at a rate on its commitment not yet called (rate_of(st, age, k)
    per quarter) from its first close on its manager's date; distributions as the policy sets them."""
    e = fit["mkt"][0]; states = [fund_state(L, fid, stock) for fid in L["reg"]]
    calls = np.zeros(len(e)); dist = np.zeros(len(e))
    def run(st, unf, fc, nav0, term=None):
        tot = np.zeros(len(e))
        for k, q in enumerate(W):
            dist[q] += nav0 * fit["drate"].get((st, k), 0.0)
            if q < fc or (term is not None and q > term): continue
            c = rate_of(st, (q - fc) // 4, k) * unf
            unf -= c; tot[q] += c
        return tot
    for x in states:
        if x.get("liquidated"): continue
        calls += run(x["st"], x["C"], x["exp_fc"], 0.0) if x["pending"] else run(x["st"], max(x["unf"], 0.0), x["fc"], max(x["nav"], 0.0), x["term"])
    d0 = dist.copy()
    by_fund = {p["fund"]: round(float(run(p["st"], p["C"], p["exp_fc"], 0.0)[W].sum()), 1) for p in L["plan"]}
    need0 = round(sum(halves(calls).values()) - sum(halves(d0).values()), 1)
    H0 = round(round(reserve(L), 1) - round(spending24(L) + need0, 1) - CUSHION, 1)
    progs = []
    for pr in L["programs"]:
        c = round(sum(by_fund[f] for f in pr["funds"]), 1)
        progs.append(dict(code=pr["code"], total=pr["total"], calls=c, headroom=round(H0 - c, 1), passes=H0 - c >= 0))
    passing = [p for p in progs if p["passes"]]
    hv = halves(calls)
    return dict(R2={h: hv[h] for h in HALVES[:2]}, R3={h: hv[h] for h in HALVES[2:]}, R4=halves(d0), R5=H0, calls=hv,
                succ=dict(funds=0, calls_taken_off_usd_m=0.0), refi_res=dict(loans_due=0, balance_due_usd_m=0.0, calls_usd_m=0.0),
                R7=max(passing, key=lambda p: p["total"])["code"] if passing else "none", programs=progs, by_fund=by_fund, need0=round(need0, 1))

def dist_quick(L, fit):
    """the policy's rates on each fund's latest statement value (the late statements' third-quarter value as it stands)."""
    out = np.zeros(len(fit["mkt"][0]))
    for fid, r in L["reg"].items():
        s = L["st"].get(fid, {})
        qs = [q for q in s if "ending_nav_usd" in s[q]]
        if not qs or r["Status"] in ("liquidated", "pending first close"): continue
        nav = max(s[max(qs)]["ending_nav_usd"], 0.0)
        for k, q in enumerate(W):
            out[q] += nav * fit["drate"].get((STRATS[r["Strategy"]], k), 0.0)
    return halves(out)

# ------------------------------------------------------------------------------------------------ variants
def lender_variant(L, fit, kind, rate=None):
    """the lenders' rule read one defensible way otherwise: fitted on every refinancing since 2020, or read straight off
    the refinancings granted within 0.35 points of the stressed rate (their mean loan-to-value, no curve fitted)."""
    f = dict(fit)
    if kind == "since 2020":
        f["lender"] = lender_rule(L, since=qi(2020, 1))
    else:
        near = [p[2] for p in fit["lender"]["pts"] if p[0] >= qi(2022, 3) and abs(p[1] - rate) < 0.35]
        f["lender"] = dict(fit["lender"], cap_post=float(np.mean(near)), kappa=1e9, n=len(near))
    return f

def with_(fit, **kw):
    f = dict(fit); f.update(kw); return f

def value_variant(fit, c=None, beta=None):
    v = dict(fit["value"])
    if c is not None: v["c"] = c
    if beta is not None: v["beta"] = beta
    return with_(fit, value=v)

def old_rate_excess(L, years=OLD_YEARS):
    """a reading the policy rules out: the benchmark rate less the same funds' rate over the eight quarters before the
    stress window (2006Q3 to 2008Q2)."""
    gross = bench_rates(L, "calls", years=years); normal = bench_rate_normal(L, years, qi(2006, 3), qi(2008, 2))
    return {k: max(v - normal.get(k[0], 0.0), 0.0) for k, v in gross.items()}

# ------------------------------------------------------------------------------------------------ everything
def _resample(L, pick, fids):
    Lb = dict(L); Lb["reg"], Lb["st"], Lb["act"], Lb["aud"] = {}, {}, {}, {}
    Lb["loans"] = defaultdict(list)
    for j, i in enumerate(pick):
        fid = fids[i]; k = "%s#%d" % (fid, j)
        Lb["reg"][k] = dict(L["reg"][fid], **{"Fund ID": k}); Lb["st"][k] = L["st"].get(fid, {}); Lb["act"][k] = L["act"].get(fid, []); Lb["aud"][k] = L["aud"].get(fid, {})
        for (f0, co), v in L["loans"].items():
            if f0 == fid: Lb["loans"][(k, co)] = v
    return Lb

def full(tgt, boot=30):
    L = load(tgt)
    fit, mkt, stock, per = fit_all(L); fit["mkt"] = mkt
    ev = lambda sw, f=None, stk=None: evaluate(L, sw, f or fit, mkt, stk or stock)
    R = dict(L=L, fit=fit, stock=stock, per=per, mkt=mkt)
    g = ev(GOLDEN); unf, pend = unfunded(L); g["R1"] = by_strategy(unf)
    R["golden"] = g
    R["reserve"], R["spending24"], R["cushion"] = round(reserve(L), 2), spending24(L), CUSHION
    live = {fid: v for fid, v in stock.items() if L["reg"][fid]["Status"] != "liquidated"}
    R["line_stock_total"] = round(sum(live.values()), 1)
    R["line_stock_audited"] = round(sum(v for fid, v in audited_stock(L).items()), 1)
    R["pending"] = [dict(fid=fid, fund=r["Fund"], C=float(r["Commitment (USD m)"]), close=_qd(r["First close expected at commitment"]))
                    for fid, r in L["reg"].items() if r["Status"] == "pending first close"]
    R["successor_events"] = successor_events(L, fit, mkt)
    R["late_statements"] = sum(1 for fid, s_ in L["st"].items() if s_.get(H_END, {}).get("cash_only") and L["reg"][fid]["Status"] != "liquidated")
    R["clause"] = {m: (v, fit["clause_votes"].get(m)) for m, v in fit["clause"].items()}
    # the real assets' loans that come due in the eight quarters
    due = []
    for fid, lns in fit["loans"].items():
        r = L["reg"][fid]
        for ln in lns:
            if ln["due"] in W:
                Pq, lim = refi_terms(fit, mkt, ln, ln["due"])
                due.append(dict(fid=fid, fund=r["Fund"], asset=ln["co"], due=ln["due"], D=round(ln["D"], 2), P26=round(ln["P26"], 2),
                                P=round(Pq, 2), ltv=round(lim, 4), gap=round(refi_gap(fit, mkt, ln, ln["due"]), 2)))
    R["loans_due"] = due
    asl = asset_loans(L)
    R["refinancings"] = sum(len(x["refis"]) for x in asl.values())
    R["refinancings_short"] = sum(1 for x in asl.values() for rf in x["refis"] if rf["new"] < rf["old"] - 1e-6)
    # the funds past their investment periods on the benchmark's rate (section 8), and the periods the stress extends
    states = [fund_state(L, fid, stock) for fid in L["reg"]]
    R["old_funds_31dec"] = sum(1 for x in states if not x["pending"] and not x["liquidated"] and x["st"] in EQUITY and x["ipl"] <= H_END)
    R["old_funds_value"] = round(sum(max(x["nav"], 0.0) for x in states if not x["pending"] and not x["liquidated"] and x["st"] in EQUITY and x["ipl"] <= H_END), 1)
    # the passes
    careful = ev(REFLEX); careful["R1"] = g["R1"]
    ta = ta_fit(L)
    quick = rates_route(L, fit, stock, lambda st, a, k: _cell(ta, st, a))
    quick.update(R4=dist_quick(L, fit), R1=by_strategy(unfunded_quick(L)))
    R["passes"] = dict(quick=quick, careful=careful, thorough=g)
    # the factorial: each stump dropped alone from the golden, and fixed alone on the reflex route
    fac = {}
    for tag, sw in [("S1 dropped", dict(GOLDEN, succession="registered")), ("S2 dropped", dict(GOLDEN, refi="none")),
                    ("S1 alone", dict(REFLEX, succession="clause")), ("S2 alone", dict(REFLEX, refi="loans"))]:
        fac[tag] = ev(sw); fac[tag]["R1"] = g["R1"]
    R["factorial"] = fac
    # each reflex dropped alone from the golden
    R["reflex_drops"] = {
        "J1 the facility balances at the latest audited borrowings, carried to 31 December as they stand": ev(GOLDEN, None, audited_stock(L)),
        "J2 the funds past their investment periods on their fees alone (section 8's benchmark rate set aside)": ev(dict(GOLDEN, old="none")),
        "J3 the pace on first investments alone (section 8 counts first and follow-on)": ev(GOLDEN, with_(fit, pace=pace_cells(L, numerator="first")[0])),
        "J4 first closes slipped on the exit market (section 8 takes the managers' dates)": ev(dict(GOLDEN, closes="slip"))}
    # the routes beside them
    bc = bench_unfunded_rates(L)
    def replay(st, a, k):
        for aa in range(min(a, 9), -1, -1):
            if (st, aa, k) in bc: return bc[(st, aa, k)]
        return _cell(ta, st, a)
    ta_d = ta_fit(L, qi(2022, 1), qi(2024, 4))
    R["routes"] = [("the golden", g),
                   ("the careful route: every investment period to its registered end, the real-asset loans rolled over as they stand", careful),
                   ("the real-asset loans rolled over as they stand, the successor's first close ending its predecessor's period", fac["S2 dropped"]),
                   ("every investment period to its registered end, the loans refinanced at the stressed terms", fac["S1 dropped"]),
                   ("the loans refinanced at the lenders' terms and the values of 31 December 2026", ev(dict(GOLDEN, refi="current"))),
                   ("the loans refinanced at 31 December's terms, every period to its registered end", ev(dict(REFLEX, refi="current"))),
                   ("the loans refinanced at the stressed rate on the values of 31 December 2026", ev(dict(GOLDEN, refi="values_flat"))),
                   ("the loans refinanced at 31 December's rate on the stressed values", ev(dict(GOLDEN, refi="terms_flat"))),
                   ("the benchmark's rate of section 8 carried to the property, infrastructure and credit funds past their periods, the loans rolled over as they stand", ev(dict(GOLDEN, old="all", refi="none"))),
                   ("the same benchmark rate for every strategy on the careful route", ev(dict(REFLEX, old="all"))),
                   ("the textbook pacing model on the capital accounts", quick),
                   ("the pacing model recalibrated on the 2022 to 2024 exit drought", rates_route(L, fit, stock, lambda st, a, k: _cell(ta_d, st, a))),
                   ("the benchmark's 2008-10 call rates replayed on the commitments not yet called", rates_route(L, fit, stock, replay)),
                   ("the latest audited borrowings carried as the facility balances", R["reflex_drops"]["J1 the facility balances at the latest audited borrowings, carried to 31 December as they stand"])]
    # the golden family: every defensible way of doing what the policy leaves to the evidence
    fam = []
    fam.append(("investment periods extended in the stress as the register shows past weak exit markets extended them", ev(dict(GOLDEN, extensions="rule"))))
    fam.append(("the pace leaving out quarters with under 2 percent of the commitment left", ev(GOLDEN, with_(fit, pace=pace_cells(L, min_room=0.02)[0]))))
    fam.append(("the pace summed over the funds' whole commitments, not Wexmoor's share of them", ev(GOLDEN, with_(fit, pace=pace_cells(L, weight="fund")[0]))))
    fam.append(("the lenders' limit fitted on every refinancing since 2020", ev(GOLDEN, lender_variant(L, fit, "since 2020"))))
    fam.append(("the lenders' limit read straight off the refinancings granted within 0.35 points of the stressed rate",
                ev(GOLDEN, lender_variant(L, fit, "direct", rate=float(mkt[2][W[0]])))))
    vc, vb = fit["value"]["c"], fit["value"]["beta"]
    for c in (max(vc - 0.01, 0.0), vc + 0.01):
        fam.append(("the assets' rate sensitivity at %.3f" % c, ev(GOLDEN, value_variant(fit, c=c))))
    for bb in (vb - 0.05, vb + 0.05):
        fam.append(("the assets' equity sensitivity at %.2f" % bb, ev(GOLDEN, value_variant(fit, beta=bb))))
    fam.append(("the assets' value response fitted on every quarter of every asset, the first four years included",
                ev(GOLDEN, with_(fit, value=value_response(L, min_age=1)))))
    fam.append(("a maturing loan's shortfall met before the fund's other calls within the commitment it has left", ev(dict(GOLDEN, order="shortfall_first"))))
    R["family"] = fam
    # the quarter the assets' values answer the market in: the fit a quarter late against the same fit with no lag and two quarters late
    R["value_lags"] = {lg: value_response(L, lag=lg) for lg in (0, 1, 2)}
    # readings one step from a sentence the policy files: the sentence rules each out, and each still files the golden program
    rd = []
    for y in (OLD_YEARS - 1, OLD_YEARS + 1):
        rd.append(("section 8's benchmark funds at a vintage %d or more years before the quarter's year" % y, ev(GOLDEN, with_(fit, crate=bench_rates(L, "calls", years=y)))))
    rd.append(("section 8's benchmark rate less the same funds' rate over the eight quarters before the stress window", ev(GOLDEN, with_(fit, crate=old_rate_excess(L)))))
    rd.append(("the pace over the commitment not yet called", ev(GOLDEN, with_(fit, pace=pace_cells(L, room="called")[0]))))
    rd.append(("the pace as the average of the fund-quarters' own rates, not the ratio of the sums", ev(GOLDEN, with_(fit, pace=pace_cells(L, mean=True)[0]))))
    rd.append(("the pace's years counted from the quarter after the first close", ev(GOLDEN, with_(fit, pace=pace_cells(L, shift=1)[0]))))
    rd.append(("proceeds reinvested at each manager's audited rate netted from the calls", ev(dict(GOLDEN, recycle="manager"))))
    rd.append(("no cap at the commitment a fund has left", ev(dict(GOLDEN, cap=False))))
    rd.append(("the funds' own fees and expenses added on top of section 8's benchmark rate", ev(dict(GOLDEN, old_fees=True))))
    rd.append(("the facility balances less proceeds reinvested since the last audit at each manager's audited rate", ev(GOLDEN, None, line_stock(L, recycling="manager")[0])))
    rd.append(("the facility balances as the investments less the capital called for them, the audited borrowings set aside", ev(GOLDEN, None, line_stock(L, recycling="gap")[0])))
    rd.append(("the fee after a fund's investment period on the cost it still holds", ev(dict(GOLDEN, fees_post="cost"))))
    R["readings"] = rd
    # readings a filed sentence rules out that land on another program
    R["ruled_out"] = [("the pace on first investments alone", R["reflex_drops"]["J3 the pace on first investments alone (section 8 counts first and follow-on)"]),
                      ("first closes slipped on the exit market as past closes were", R["reflex_drops"]["J4 first closes slipped on the exit market (section 8 takes the managers' dates)"]),
                      ("the funds past their investment periods on their fees alone", R["reflex_drops"]["J2 the funds past their investment periods on their fees alone (section 8's benchmark rate set aside)"])]
    # readings that do part of a stump's work
    all_clause = with_(fit, clause={m: True for m in set(r["Manager"] for r in L["reg"].values())})
    R["partials"] = [("the successor clause taken for every manager, whatever its past successions show", ev(GOLDEN, all_clause)),
                     ("the successor closes found for the plan's re-ups alone", ev(dict(GOLDEN, successors=("plan",)))),
                     ("the successor closes found for the funds awaiting a first close alone", ev(dict(GOLDEN, successors=("reg",)))),
                     ("the successor clause missed and the loans refinanced on the values of 31 December 2026", ev(dict(REFLEX, refi="values_flat")))]
    # each estimated input moved by a fifth, and the filed pace by a twentieth (it is a ratio of sums over the files, with no free
    # choice; the facility balances are section 8's own sum, so they are not moved)
    pt = []
    for k_ in (0.8, 1.2):
        pt.append(("the refinancing shortfalls at %d percent of the estimate" % round(100 * k_), ev(dict(GOLDEN, gap_scale=k_))))
    fq, xq = fit["fee"], fit["exp"]
    for k_ in (0.8, 1.2):
        pt.append(("the fee and expense rates of the funds yet to close at %d percent of the filed median" % round(100 * k_),
                   ev(GOLDEN, with_(fit, fee={a_: v * k_ for a_, v in fq.items()}, exp={a_: v * k_ for a_, v in xq.items()}))))
    for d_ in (-0.02, 0.02):
        lv = dict(fit["lender"]); lv["cap_post"] += d_; lv["kappa"] *= 1 + d_ / 0.5
        pt.append(("the lenders' limit %s by 0.02 of value" % ("lower" if d_ < 0 else "higher"), ev(GOLDEN, with_(fit, lender=lv))))
    for k_ in (0.95, 1.05):
        pt.append(("the pace of new investments at %d percent of the filed ratio" % round(100 * k_), ev(GOLDEN, with_(fit, pace={c_: v * k_ for c_, v in fit["pace"].items()}))))
    R["perturb"] = pt
    # the bootstrap over funds: what is estimated from the endowment's own funds refitted on resampled funds
    rng = np.random.default_rng(5); fids = list(L["reg"]); bs = defaultdict(list)
    for b in range(boot):
        Lb = _resample(L, rng.choice(len(fids), len(fids), replace=True), fids)
        fb = dict(lender=lender_rule(Lb), value=value_response(Lb), fee=fee_rates(Lb)[0], exp=fee_rates(Lb)[1])
        for name, keys in (("the lenders' limit and the assets' values", ("lender", "value")), ("the fee and expense rates", ("fee", "exp")),
                           ("every fitted input together", ("lender", "value", "fee", "exp"))):
            f = dict(fit)
            for k in keys:
                if fb.get(k) is not None: f[k] = fb[k]
            o_ = ev(GOLDEN, f); bs[name].append((float(o_["R5"]), o_["R7"]))
    R["boot"] = {k: [x[0] for x in v] for k, v in bs.items()}
    R["boot_programs"] = {k: [x[1] for x in v] for k, v in bs.items()}
    return R
