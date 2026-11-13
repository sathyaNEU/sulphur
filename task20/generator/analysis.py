"""The golden for task20 architecture 4, computed from target/ alone, and every hurried route beside it."""
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
HALF = [W[0:2], W[2:4], W[4:6], W[6:8]]
STRATS = {"Buyout": "BO", "Growth equity": "GE", "Venture capital": "VC", "Real estate": "RE", "Infrastructure": "IN", "Private credit": "PC"}

def rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))

def sheet(path, name=None):
    wb = load_workbook(path, data_only=True)
    ws = wb[name] if name else wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    hdr = next(it)
    return [dict(zip(hdr, r)) for r in it if any(v is not None for v in r)]

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
        if H_END in st.get(fid, {}):
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
    act = defaultdict(list)
    for r in rows(P("manager_portfolio_activity_2013_2026.csv")):
        act[r["fund_id"]].append((q_of(D(r["date"])), r["record_type"], r["portfolio_company"], float(r["amount_usd_m"]),
                                  float(r["cost_basis_usd_m"]) if r["cost_basis_usd_m"] else 0.0))
    L["act"] = act
    aud = defaultdict(dict)
    for r in sheet(P("fund_audited_financials_FY2013_FY2026.xlsx"), "Audited accounts"):
        d = r["Fiscal year end"]; d = d.date() if hasattr(d, "date") else d
        aud[r["Fund ID"]][q_of(d)] = {k.replace(" (USD thousands)", ""): (float(v) / 1000.0 if isinstance(v, (int, float)) else v) for k, v in r.items()}
    L["aud"] = aud
    mk = rows(P("market_series_quarterly_2000Q1_2026Q4.csv"))
    L["E"] = np.array([float(r["exit_activity_index_2015_100"]) for r in mk]); L["S"] = np.array([float(r["public_equity_total_return_index"]) for r in mk])
    L["R"] = np.array([float(r["short_rate_pct"]) for r in mk])
    L["bench"] = rows(P("industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv"))
    L["hold"] = sheet(P("liquid_holdings_2026-12-31.xlsx"))
    L["spend"] = {int(r["fiscal_year"]): float(r["approved_distribution_usd_m"]) for r in rows(P("spending_distributions_FY2014_FY2027.csv"))}
    names = {r["Fund"]: fid for fid, r in L["reg"].items()}
    L["plan"] = []
    for r in sheet(P("corrigan_hart_pacing_plan_2027.xlsx"), "2027 proposed commitments"):
        if r["Fund"] == "Total" or not r["Strategy"]: continue
        qn, yr = r["First close expected"].split()
        L["plan"].append(dict(fund=r["Fund"], mgr=r["Manager"], st=STRATS[r["Strategy"]], C=float(r["Proposed commitment (USD m)"]),
                              exp_fc=qi(int(yr), int(qn[1]))))
    return L

# ------------------------------------------------------------------------------------------------ the policy
FACTORS = {"Cash, money market funds and US Treasuries": 1.00, "Investment-grade bonds": 0.90, "Public equities": 0.70,
           "Hedge funds: redeemable within 24 months": 0.90}
CUSHION = 1200.0
GRID = 25.0

def reserve(L):
    return sum(float(h["Market value 31 Dec 2026 (USD m)"]) * FACTORS.get(h["Policy liquidity class"], 0.0)
               for h in L["hold"] if h["Policy liquidity class"])

def spending24(L):
    return 2.0 * L["spend"][2027]

def share(L, fid):
    r = L["reg"][fid]
    return float(r["Commitment (USD m)"]) / float(r["Fund size (USD m)"])

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

# ------------------------------------------------------------------------------------------------ R2
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

def line_stock(L, recycling="manager"):
    """the capital each manager has invested on its fund's subscription line and not yet called, at the endowment's
    share, at 31 December 2026: the gap between investments and investment calls less the proceeds the fund recycled,
    the recycled amount read off the audited year-ends (gap less the audited borrowings) and carried to the end of 2026
    at the fund's own recycling rate while it is still investing."""
    res = {}
    rho_m = defaultdict(list)
    per = {}
    for fid, r in L["reg"].items():
        if r["Status"] == "pending first close": continue
        g = gap_series(L, fid)
        if not g: continue
        sh = share(L, fid)
        aud = L["aud"].get(fid, {})
        ip_end = q_of(r["Investment period ends"].date() if hasattr(r["Investment period ends"], "date") else r["Investment period ends"])
        pts = []
        for qa, a in sorted(aud.items()):
            if qa in g:
                gap, cp, _ = g[qa]
                rec = gap - a["Credit facility borrowings"] * sh
                pts.append((qa, rec, cp, a["Credit facility borrowings"] * sh))
        per[fid] = dict(g=g, pts=pts, sh=sh, ip_end=ip_end, mgr=r["Manager"], size=float(r["Fund size (USD m)"]))
        if len(pts) >= 1 and pts[-1][2] > 0:
            # recycling rate: recycled over proceeds realised while investing
            cp_ip = sum(g[q][2] for q in g if q <= min(pts[-1][0], ip_end))
            if cp_ip > 1e-6:
                rho_m[r["Manager"]].append(max(pts[-1][1], 0.0) / cp_ip)
    for fid, x in per.items():
        g, pts, sh = x["g"], x["pts"], x["sh"]
        if pts:
            qa, rec, cp, line_a = pts[-1]
        else:   # no audited year-end yet: nothing recycled before the first realisation
            qa, rec = min(g) - 1, 0.0
        rho = float(np.median(rho_m[x["mgr"]])) if (recycling == "manager" and rho_m.get(x["mgr"])) else 0.0
        cap = 0.15 * x["size"] * sh
        rec_end = rec
        for q in range(qa + 1, H_END + 1):
            if q <= x["ip_end"]:
                rec_end = min(rec_end + rho * g[q][2], cap)
        gap_end = g[H_END][0]
        res[fid] = max(gap_end - rec_end, 0.0)
    return res, per

# ------------------------------------------------------------------------------------------------ the stress path
def stress_market(L):
    """the policy's scenario: exits as 2008Q3-2010Q2 relative to 2008Q2 on the 2026Q4 level; equities 85, 70, then five
    points a quarter back to 100 per cent; short rates up 2.5 points."""
    E, S, R = L["E"], L["S"], L["R"]
    e = np.concatenate([E, np.zeros(8)]); s = np.concatenate([S, np.zeros(8)]); r = np.concatenate([R, np.zeros(8)])
    eq = [0.85, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    for k in range(8):
        e[H_END + 1 + k] = E[H_END] * E[qi(2008, 3) + k] / E[qi(2008, 2)]
        s[H_END + 1 + k] = S[H_END] * eq[k]
        r[H_END + 1 + k] = R[H_END] + 2.5
    return e, s, r

# ------------------------------------------------------------------------------------------------ fund states and rates
def fund_state(L, fid, stock):
    r = L["reg"][fid]; st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"])
    s = L["st"].get(fid, {})
    paid = sum(v["contributions_investments_usd"] + v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"] for v in s.values())
    navq = max((q for q in s if "ending_nav_usd" in s[q]), default=None)
    nav = s[navq]["ending_nav_usd"] if navq is not None else 0.0
    if navq is not None and navq < H_END:          # a fourth-quarter statement still to come: roll the cash
        x = s.get(H_END, {})
        nav += x.get("contributions_investments_usd", 0.0) - x.get("distributions_return_of_capital_usd", 0.0)
    fc = q_of(r["First close"].date() if hasattr(r["First close"], "date") else r["First close"]) if r["First close"] else None
    ipe = q_of(r["Investment period ends"].date() if hasattr(r["Investment period ends"], "date") else r["Investment period ends"]) if r["Investment period ends"] else None
    sh = C / float(r["Fund size (USD m)"]) if r["Fund size (USD m)"] else None
    inv = sum(a for q, t, co, a, cb in L["act"].get(fid, []) if t in ("initial investment", "follow-on investment")) * (sh or 0)
    fee_last = s[max(s)]["contributions_management_fees_usd"] if s else 0.0
    return dict(fid=fid, st=st, C=C, paid=paid, unf=C - paid, nav=nav, fc=fc, ipe=ipe, sh=sh, inv=inv, mgr=r["Manager"],
                stock=stock.get(fid, 0.0), fee_q=fee_last, pending=(r["Status"] == "pending first close"), liquidated=(r["Status"] == "liquidated"),
                exp_fc=q_of(r["First close expected at commitment"].date() if hasattr(r["First close expected at commitment"], "date") else r["First close expected at commitment"]))

def deploy_rates(L, defensive=False):
    """investments as a share of the commitment not yet invested, by strategy and year since first close, with the deal
    market's elasticity fitted on the exit index. The follow-ons into companies held two years or more are the
    defensive kind and are left out (defensive=True keeps them in, the hurried reading of the activity file)."""
    obs = []
    for fid, r in L["reg"].items():
        if not r["First close"] or not r["Fund size (USD m)"]: continue
        st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"]); sh = C / float(r["Fund size (USD m)"])
        fc = q_of(r["First close"].date() if hasattr(r["First close"], "date") else r["First close"])
        inv = defaultdict(float); allinv = defaultdict(float); first = {}
        for q, t, co, a, cb in sorted(L["act"].get(fid, [])):
            if t == "initial investment":
                first[co] = q; inv[q] += a * sh; allinv[q] += a * sh
            elif t == "follow-on investment":
                allinv[q] += a * sh
                if defensive or not (co in first and q - first[co] >= 8): inv[q] += a * sh
        cum = 0.0
        for q in range(fc, H_END + 1):
            a = (q - fc) // 4
            room = max(C - cum, 0.0)
            if room > 0.02 * C and a < 7:
                obs.append((st, a, inv.get(q, 0.0) / room, L["E"][q], room))
            cum += allinv.get(q, 0.0)
    # the deal market's elasticity by least squares on the amounts, each cell's rate the ratio of sums at that elasticity
    cells = defaultdict(list)
    for st, a, y, e, room in obs: cells[(st, a)].append((y * room, room, max(min(e / 100.0, 1.4), 0.4)))
    best = None
    for eta in np.round(np.arange(-0.6, 1.01, 0.02), 2):
        sse = 0.0; rate = {}
        for k, v in cells.items():
            I = np.array([x[0] for x in v]); R_ = np.array([x[1] for x in v]); M = np.array([x[2] for x in v]) ** eta
            rate[k] = float(I.sum() / (R_ * M).sum()) if (R_ * M).sum() > 0 else 0.0
            sse += float(((I - rate[k] * R_ * M) ** 2).sum())
        if best is None or sse < best[0]: best = (sse, float(eta), rate)
    return best[2], best[1]

def fee_rates(L):
    """management fees per quarter as a share of the commitment while the fund is investing, by strategy (the median
    over the endowment's fund-quarters, statements only)."""
    by = defaultdict(list)
    for fid, r in L["reg"].items():
        if not r["First close"]: continue
        st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"])
        fc = q_of(r["First close"].date() if hasattr(r["First close"], "date") else r["First close"])
        ipe = q_of(r["Investment period ends"].date() if hasattr(r["Investment period ends"], "date") else r["Investment period ends"])
        for q, v in L["st"].get(fid, {}).items():
            if v.get("cash_only") or q <= fc or q > ipe: continue
            by[st].append(v["contributions_management_fees_usd"] / C)
    return {k: float(np.median(v)) for k, v in by.items()}

def nav_beta(L):
    xs, ys = [], []
    for fid, r in L["reg"].items():
        if r["Strategy"] not in ("Buyout", "Growth equity", "Venture capital"): continue
        s = L["st"].get(fid, {})
        for q in sorted(s):
            if q - 1 in s and "ending_nav_usd" in s[q - 1] and "ending_nav_usd" in s[q] and s[q - 1]["ending_nav_usd"] > 5:
                flow = s[q]["contributions_investments_usd"] - s[q]["distributions_return_of_capital_usd"] - s[q]["distributions_realized_gain_usd"]
                ys.append((s[q]["ending_nav_usd"] - flow) / s[q - 1]["ending_nav_usd"] - 1)
                xs.append(L["S"][q - 1] / L["S"][q - 2] - 1)
    return float(np.polyfit(xs, ys, 1)[0])

def slip_window(E, e, win):
    return float(np.mean([E[max(e - k, 0)] for k in range(1, win + 1)]))

def slip_points(L, win, ref):
    pts = []
    for fid, r in L["reg"].items():
        if not r["First close"]: continue
        e = q_of(r["First close expected at commitment"].date() if hasattr(r["First close expected at commitment"], "date") else r["First close expected at commitment"])
        a = q_of(r["First close"].date() if hasattr(r["First close"], "date") else r["First close"])
        pts.append((max(0.0, 1.0 - slip_window(L["E"], e, win) / ref), a - e))
    return np.array([p[0] for p in pts]), np.array([p[1] for p in pts])

def slip_model(L, wins=(1, 2, 3, 4), refs=(90.0, 95.0, 100.0, 105.0, 110.0), table=None):
    """quarters of slip (first close against the date given at commitment) on how far the exit market sat below normal
    over the quarters before the expected close: least squares with an intercept, the window and the reference level
    chosen by fit."""
    best = None
    for win in wins:
        for ref in refs:
            x, y = slip_points(L, win, ref)
            X = np.column_stack([np.ones(len(x)), x])
            coef, *_ = np.linalg.lstsq(X, y, rcond=None)
            sse = float(np.sum((y - X @ coef) ** 2))
            if table is not None: table.append((win, ref, float(coef[0]), float(coef[1]), sse))
            if best is None or sse < best[0]: best = (sse, float(coef[0]), float(coef[1]), win, ref)
    return dict(a=best[1], b=best[2], win=best[3], ref=best[4], sse=best[0])

def expected_slip(fit, e, exp_q):
    s = fit["slip"]
    return max(s["a"] + s["b"] * max(0.0, 1.0 - slip_window(e, exp_q, s["win"]) / s["ref"]), 0.0)

def _cell(tab, st, a, default):
    for aa in range(min(a, 11), -1, -1):
        if (st, aa) in tab: return tab[(st, aa)]
    return default

# ------------------------------------------------------------------------------------------------ deals held, support, recycling
def held_deals(L, fid):
    """the fund's companies still held at 31 December 2026 (endowment share): cost, first investment quarter, last value."""
    sh = share(L, fid)
    first = {}; cost = defaultdict(float); last_val = {}; gone = set()
    for q, t, co, a, cb in L["act"].get(fid, []):
        if t == "initial investment": first[co] = q; cost[co] += a * sh
        elif t == "follow-on investment": cost[co] += a * sh
        elif t == "realization": gone.add(co)
        elif t == "valuation": last_val[co] = (q, a * sh, cb * sh)
    return [dict(co=c, q0=first[c], cost=cost[c], fv=last_val.get(c, (None, cost[c]))[1]) for c in first if c not in gone]

def support_points(L, basis="cost"):
    """per BO/GE/VC fund and quarter: follow-ons into companies held two years or more (the defensive kind) and the
    cost of those companies at the start of the quarter (basis "value": their latest valuation instead)."""
    out = []
    for fid, r in L["reg"].items():
        if r["Strategy"] not in ("Buyout", "Growth equity", "Venture capital") or not r["Fund size (USD m)"]: continue
        sh = share(L, fid)
        ev = sorted(L["act"].get(fid, []))
        first = {}; cost = defaultdict(float); val = {}; alive = set()
        byq = defaultdict(list)
        for e in ev: byq[e[0]].append(e)
        if not byq: continue
        for q in range(min(byq), H_END + 1):
            if basis == "value":
                pool = sum(val.get(c, 0.0) for c in alive if q - first[c] >= 8)
            else:
                pool = sum(cost[c] for c in alive if q - first[c] >= 8)
            s_q = 0.0
            for (qq, t, co, a, cb) in byq.get(q, []):
                if t == "initial investment": first[co] = q; cost[co] += a * sh; val[co] = a * sh; alive.add(co)
                elif t == "follow-on investment":
                    if co in first and q - first[co] >= 8: s_q += a * sh
                    cost[co] += a * sh; val[co] = val.get(co, 0.0) + a * sh
                elif t == "realization": alive.discard(co)
                elif t == "valuation": val[co] = a * sh
            if pool > 1.0: out.append((q, s_q, pool))
    return out

def support_model(L, prm=None, lags=(1, 2, 3), stars=(0.90, 1.00, 1.10), table=None, pts=None):
    """defensive follow-ons per quarter as a share of the cost of companies held two years or more, on how far the exit
    market sat below normal some quarters earlier: least squares through the origin, the lag and the level chosen by
    fit."""
    pts = support_points(L) if pts is None else pts
    q = np.array([p[0] for p in pts]); s = np.array([p[1] for p in pts]); pool = np.array([p[2] for p in pts])
    y = s / pool; w = pool
    best = None
    for lag in lags:
        for es in stars:
            x = np.maximum(0.0, es - L["E"][np.maximum(q - lag, 0)] / 100.0) / es
            sig = float(np.sum(w * x * y) / np.sum(w * x * x)) if np.sum(w * x * x) > 0 else 0.0
            sse = float(np.sum(w * (y - sig * x) ** 2))
            if table is not None: table.append((lag, es, sig, sse))
            if best is None or sse < best[0]: best = (sse, sig, lag, es)
    return dict(sigma=best[1], lag=best[2], e_star=best[3], sse=best[0])

def recycling_rates(L, per, hurried=False):
    """each manager's share of proceeds kept and reinvested while investing: the audited gap less the borrowings over
    the proceeds (hurried: the whole gap read as recycling)."""
    out = defaultdict(list)
    for fid, x in per.items():
        g, pts = x["g"], x["pts"]
        if not pts: continue
        qa, rec, cp, line_a = pts[-1]
        cp_ip = sum(g[q][2] for q in g if q <= min(qa, x["ip_end"]))
        if cp_ip > 1e-6:
            num = g[qa][0] if hurried else rec
            out[x["mgr"]].append(max(num, 0.0) / cp_ip)
    return {m: float(np.median(v)) for m, v in out.items()}

# ------------------------------------------------------------------------------------------------ the projection
def project2(L, states, plan, budget, sw, fit, mkt):
    """the policy's 24 months, quarter by quarter. Calls: the managers' investments (deployment of the room left, slowed
    by the deal market), the defensive follow-ons, the fees, less the proceeds recycled, plus the line stock called at
    the clean-down. Distributions: each fund's 31 December value times its strategy's 2008-10 benchmark rate.
    sw: line ('rebuilt' or 'recycled'), support ('measured' or 'none'), closes ('slip' or 'expected')."""
    e, s, r = mkt
    out = {k: np.zeros(len(e)) for k in ("call_inv", "call_pend", "call_plan", "dist", "support", "stock", "fees", "recycled", "fees_closed")}
    rho = fit["rho_h"] if sw["line"] == "recycled" else fit["rho"]
    dep = fit["dep_h"] if sw["support"] == "none" and "dep_h" in fit else fit["dep"]
    eta = fit["eta_h"] if sw["support"] == "none" and "eta_h" in fit else fit["eta"]
    def closes(exp_q):
        """the first-close quarters with their weights: the expected slip split between the two quarters around it."""
        if sw["closes"] == "expected": return [(exp_q, 1.0)]
        sl = expected_slip(fit, e, exp_q); k = int(math.floor(sl)); fr = sl - k
        return [(exp_q + k, 1.0 - fr), (exp_q + k + 1, fr)] if fr > 1e-9 else [(exp_q + k, 1.0)]
    def run(st, C, fc, inv0, paid0, nav0, stock, deals, mgr, key):
        inv, paid, nav = inv0, paid0, nav0
        ipe = fc + (20 if st not in ("RE", "PC") else (16 if st == "RE" else 12))
        deals = [dict(d) for d in deals]
        cap_rec = 0.15 * C; rec_c = 0.0
        for k, q in enumerate(W):
            dx = nav0 * fit["drate"].get((st, k), 0.0)
            out["dist"][q] += dx
            if q < fc: continue
            a = (q - fc) // 4
            # the fee: on the commitment while investing, on the cost of the companies still held afterwards
            fee = fit["fee"][st] * C if q < ipe else fit["fee"][st] * sum(d["cost"] for d in deals)
            room = max(C - inv, 0.0) if q < ipe else 0.0
            md = max(min(e[q] / 100.0, 1.4), 0.4) ** eta
            I = _cell(dep, st, a, 0.05) * room * md
            sup = 0.0
            if sw["support"] == "measured" and st in ("BO", "GE", "VC"):
                sp = fit["support"]
                pool = sum(d["cost"] for d in deals if q - d["q0"] >= 8)
                sup = min(sp["sigma"] * max(0.0, sp["e_star"] - e[max(q - sp["lag"], 0)] / 100.0) / sp["e_star"] * pool, max(C - paid - I - fee, 0.0))
            rc = min(rho.get(mgr, 0.0) * dx, max(cap_rec - rec_c, 0.0), I + sup) if q < ipe else 0.0
            rec_c += rc
            call = max(I + sup + fee - rc, 0.0) + (stock if q == W[0] else 0.0)
            call = min(call, max(C - paid, 0.0) + (stock if q == W[0] else 0.0))
            paid += call; inv += I + sup
            g = 1 + fit["beta"] * (s[q] / s[q - 1] - 1) if st in ("BO", "GE", "VC") else 1 + 0.4 * fit["beta"] * (s[q] / s[q - 1] - 1)
            nav = nav * g
            frac = min(dx / nav, 1.0) if nav > 0 else 0.0
            for d in deals: d["cost"] *= (1 - frac)
            if sup > 0:
                pool = sum(d["cost"] for d in deals if q - d["q0"] >= 8)
                for d in deals:
                    if q - d["q0"] >= 8 and pool > 0: d["cost"] += sup * d["cost"] / pool
            if I > 0: deals.append(dict(co="new", q0=q, cost=I, fv=I))
            nav = max(nav - dx + I + sup, 0.0)
            out[key][q] += call; out["support"][q] += sup; out["fees"][q] += fee; out["recycled"][q] += rc
            if key == "call_inv": out["fees_closed"][q] += fee
            if q == W[0]: out["stock"][q] += stock
    for x in states:
        if x.get("liquidated"): continue
        if x["pending"]:
            for fc, wgt in closes(x["exp_fc"]):
                run(x["st"], x["C"] * wgt, fc, 0.0, 0.0, 0.0, 0.0, [], x["mgr"], "call_pend")
        else:
            st_ = x["stock"] if sw["line"] == "rebuilt" else 0.0
            deals = held_deals(L, x["fid"])
            if fit["support"].get("basis") == "value":
                deals = [dict(d, cost=d["fv"]) for d in deals]
            run(x["st"], x["C"], x["fc"], x["inv"], x["paid"], max(x["nav"], 0.0), st_, deals, x["mgr"], "call_inv")
    tot = sum(p["C"] for p in plan)
    for p in plan:
        for fc, wgt in closes(p["exp_fc"]):
            run(p["st"], budget * p["C"] / tot * wgt, fc, 0.0, 0.0, 0.0, 0.0, [], p.get("mgr", ""), "call_plan")
    return out

project3 = project2

def fit_all2(L):
    mkt = stress_market(L)
    dep, eta = deploy_rates(L)
    dep_h, eta_h = deploy_rates(L, defensive=True)
    stock, per = line_stock(L)
    fit = dict(dep=dep, eta=eta, dep_h=dep_h, eta_h=eta_h, slip=slip_model(L), fee=fee_rates(L), beta=nav_beta(L),
               support=support_model(L), rho=recycling_rates(L, per), rho_h=recycling_rates(L, per, hurried=True),
               drate=bench_rates_2008(L))
    return fit, mkt, stock, per

# ------------------------------------------------------------------------------------------------ the policy's distributions
def bench_rates_2008(L):
    """the policy's distribution rates: for each strategy and each quarter from 2008Q3 to 2010Q2, the benchmark funds'
    distributions in the quarter over their value at the end of the previous quarter, summed over the strategy's funds."""
    num = defaultdict(float); den = defaultdict(float)
    prev = {}
    rows_ = sorted(L["bench"], key=lambda r: (r["benchmark_fund"], r["period_end"]))
    for r in rows_:
        q = q_of(D(r["period_end"])); key = r["benchmark_fund"]
        nav_prev = prev.get(key) if prev.get(key, (None, None))[0] == q - 1 else None
        prev[key] = (q, float(r["nav_pct_of_commitment"]))
        if qi(2008, 3) <= q <= qi(2010, 2) and nav_prev is not None:
            st = STRATS[r["strategy"]]
            num[(st, q)] += float(r["distributions_pct_of_commitment"]); den[(st, q)] += nav_prev[1]
    return {(st, q - qi(2008, 3)): num[(st, q)] / den[(st, q)] for (st, q) in den if den[(st, q)] > 0}

# ------------------------------------------------------------------------------------------------ the textbook routes
def ta_fit(L, q_lo=None, q_hi=None):
    """calls in a year over the commitment not yet called at its start, by strategy and year since first close, from the
    capital accounts (optionally only the years starting inside a window)."""
    num = defaultdict(float); den = defaultdict(float)
    for fid, r in L["reg"].items():
        if not r["First close"]: continue
        st = STRATS[r["Strategy"]]; C = float(r["Commitment (USD m)"])
        fc = q_of(r["First close"].date() if hasattr(r["First close"], "date") else r["First close"])
        s = L["st"].get(fid, {})
        paid = 0.0
        for q in range(fc, H_END + 1):
            a = (q - fc) // 4
            c = 0.0
            if q in s:
                c = s[q]["contributions_investments_usd"] + s[q]["contributions_management_fees_usd"] + s[q]["contributions_fund_expenses_usd"]
            if (q_lo is None or q >= q_lo) and (q_hi is None or q <= q_hi) and C - paid > 0.01 * C:
                num[(st, min(a, 9))] += c; den[(st, min(a, 9))] += C - paid
            paid += c
    return {k: num[k] / den[k] for k in den if den[k] > 0}

def bench_call_rates(L):
    """the benchmark's contributions in each quarter of 2008Q3-2010Q2 over the commitment its funds had not yet called,
    by strategy and year of age."""
    num = defaultdict(float); den = defaultdict(float); paid = defaultdict(float)
    for r in sorted(L["bench"], key=lambda r: (r["benchmark_fund"], r["period_end"])):
        q = q_of(D(r["period_end"])); key = r["benchmark_fund"]
        unf = 100.0 - paid[key]
        c = float(r["contributions_pct_of_commitment"])
        if qi(2008, 3) <= q <= qi(2010, 2) and unf > 1.0:
            a = min((q - qi(int(r["vintage"]), 1)) // 4, 9)
            num[(STRATS[r["strategy"]], a, q - qi(2008, 3))] += c; den[(STRATS[r["strategy"]], a, q - qi(2008, 3))] += unf
        paid[key] += c
    return {k: num[k] / den[k] for k in den if den[k] > 0}

def project_rates(L, states, plan, budget, fit, rate_of):
    """calls at a rate on the commitment not yet called (rate_of(st, age, k) per quarter), distributions as the policy
    sets them, pending and new funds from their expected first close."""
    e = fit["mkt"][0]
    out = {k: np.zeros(len(e)) for k in ("call_inv", "call_pend", "call_plan", "dist", "support", "stock", "fees", "recycled", "fees_closed")}
    def run(st, C, unf, fc, nav0, key):
        for k, q in enumerate(W):
            out["dist"][q] += nav0 * fit["drate"].get((st, k), 0.0)
            if q < fc: continue
            a = (q - fc) // 4
            c = rate_of(st, a, k) * unf
            unf -= c; out[key][q] += c
    for x in states:
        if x.get("liquidated"): continue
        if x["pending"]: run(x["st"], x["C"], x["C"], x["exp_fc"], 0.0, "call_pend")
        else: run(x["st"], x["C"], max(x["unf"], 0.0), x["fc"], max(x["nav"], 0.0), "call_inv")
    tot = sum(p["C"] for p in plan)
    for p in plan:
        C = budget * p["C"] / tot; run(p["st"], C, C, p["exp_fc"], 0.0, "call_plan")
    return out

def ta_rate_of(tab):
    return lambda st, a, k: _cell(tab, st, a, 0.05)

def bench_rate_of(tab, ta):
    def f(st, a, k):
        for aa in range(min(a, 9), -1, -1):
            if (st, aa, k) in tab: return tab[(st, aa, k)]
        return _cell(ta, st, a, 0.05)
    return f

# ------------------------------------------------------------------------------------------------ results
HALVES = ["H1 2027", "H2 2027", "H1 2028", "H2 2028"]
STRAT_ORDER = ["Buyout", "Growth equity", "Venture capital", "Real estate", "Infrastructure", "Private credit"]
GOLDEN = dict(line="rebuilt", support="measured", closes="slip")
REFLEX = dict(line="recycled", support="none", closes="expected")

def halves(v):
    return {h: round(float(v[W[2 * i:2 * i + 2]].sum()), 1) for i, h in enumerate(HALVES)}

def outcome(L, fn):
    """fn(budget) -> projection; the figures the prompt asks for, from one projection method."""
    o0, o1, o5 = fn(0.0), fn(100.0), fn(500.0)
    n = lambda o: float((o["call_inv"] + o["call_pend"] + o["call_plan"])[W].sum() - o["dist"][W].sum())
    RES, SPEND = reserve(L), spending24(L)
    c = (n(o1) - n(o0)) / 100.0
    B = (RES - CUSHION - SPEND - n(o0)) / c
    N5 = SPEND + n(o5)
    return dict(R2=halves(o0["call_inv"]), R3=halves(o0["call_pend"]), R4=halves(o0["dist"]), R5=round(N5, 1),
                R6=round(round(RES, 1) - round(N5, 1) - CUSHION, 1), B=round(B, 1), R7=int(math.floor(B / GRID + 1e-9) * GRID), c_plan=round(c, 4),
                plan_calls=halves(o5["call_plan"]), support=halves(o0["support"]), stock=round(float(o0["stock"][W].sum()), 1),
                fees=halves(o0["fees_closed"]), recycled=halves(o0["recycled"]))

def outcome_at(L, fn, b):
    """the policy's test at one budget, component by component (USD m over the eight quarters)."""
    o = fn(b)
    tot = lambda v: round(float(v[W].sum()), 1)
    raw = lambda v: float(v[W].sum())
    RES, SPEND = round(reserve(L), 1), spending24(L)
    N = round(SPEND + raw(o["call_inv"]) + raw(o["call_pend"]) + raw(o["call_plan"]) - raw(o["dist"]), 1)
    return dict(reserve=RES, spending=SPEND, calls_closed=tot(o["call_inv"]), calls_pending=tot(o["call_pend"]), calls_budget=tot(o["call_plan"]),
                distributions=tot(o["dist"]), net=N, left=round(RES - N, 1), minimum=CUSHION, headroom=round(RES - N - CUSHION, 1),
                support=tot(o["support"]), stock=tot(o["stock"]), fees=tot(o["fees"]), recycled=tot(o["recycled"]))

def by_strategy(d):
    inv = {v: k for k, v in STRATS.items()}
    return {s: round(d.get(STRATS[s], 0.0), 1) for s in STRAT_ORDER}

def audited_stock(L):
    """the hurried line stock: each fund's latest audited credit-facility borrowings at the endowment's share, carried to 31
    December 2026 as they stand."""
    out = {}
    for fid, r in L["reg"].items():
        aud = L["aud"].get(fid, {})
        if r["Status"] in ("pending first close", "liquidated") or not aud: continue
        out[fid] = aud[max(aud)]["Credit facility borrowings"] * share(L, fid)
    return out

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

def full(tgt, boot=40):
    L = load(tgt)
    fit, mkt, stock, per = fit_all2(L); fit["mkt"] = mkt
    states = [fund_state(L, fid, stock) for fid in L["reg"]]
    proj = lambda sw, f2=None, stt=None: (lambda b: project2(L, stt or states, L["plan"], b, sw, f2 or fit, mkt))
    unf, pend = unfunded(L)
    R = dict(L=L, fit=fit, stock=stock, per=per, states=states)
    R["golden"] = outcome(L, proj(GOLDEN)); R["golden"]["R1"] = by_strategy(unf)
    R["reserve"], R["spending24"], R["cushion"] = round(reserve(L), 2), spending24(L), CUSHION
    live = {fid: v for fid, v in stock.items() if L["reg"][fid]["Status"] != "liquidated"}
    R["line_stock_total"] = round(sum(live.values()), 1)
    R["line_stock_by"] = by_strategy({st: sum(v for fid, v in live.items() if STRATS[L["reg"][fid]["Strategy"]] == st) for st in STRATS.values()})
    R["pending"] = []
    for x in states:
        if x["pending"]:
            sl = expected_slip(fit, mkt[0], x["exp_fc"])
            R["pending"].append(dict(fid=x["fid"], fund=L["reg"][x["fid"]]["Fund"], st=x["st"], C=x["C"], exp=x["exp_fc"], slip=round(sl, 2)))
    R["plan_slips"] = [dict(fund=p["fund"], st=p["st"], C=p["C"], exp=p["exp_fc"], slip=round(expected_slip(fit, mkt[0], p["exp_fc"]), 2)) for p in L["plan"]]
    # the passes
    careful = outcome(L, proj(REFLEX)); careful["R1"] = R["golden"]["R1"]
    ta = ta_fit(L)
    quick = outcome(L, lambda b: project_rates(L, states, L["plan"], b, fit, ta_rate_of(ta)))
    quick["R1"] = by_strategy(unfunded_quick(L)); quick["R4"] = dist_quick(L, fit)
    R["passes"] = dict(quick=quick, careful=careful, thorough=R["golden"])
    # the routes beside them
    ta23 = ta_fit(L, qi(2022, 1), qi(2023, 4)); bc = bench_call_rates(L)
    R["routes"] = [("the golden", R["golden"]), ("the careful route: the gap between investments and calls read as recycled proceeds, one investment pace for every follow-on, pending and new funds closing on their managers' dates", careful),
                   ("the textbook pacing model on the capital accounts", quick),
                   ("the pacing model recalibrated on 2022 and 2023", outcome(L, lambda b: project_rates(L, states, L["plan"], b, fit, ta_rate_of(ta23)))),
                   ("the benchmark's 2008-10 call rates replayed on the commitments not yet called", outcome(L, lambda b: project_rates(L, states, L["plan"], b, fit, bench_rate_of(bc, ta)))),
                   ("the latest audited borrowings carried as the line stock at 31 December 2026", outcome(L, proj(GOLDEN, stt=[fund_state(L, fid, audited_stock(L)) for fid in L["reg"]])))]
    # the golden family: the next-best fits and the defensible rivals
    fam = []
    tab = []; slip_model(L, table=tab); tab.sort(key=lambda t: t[4])
    for t in tab[1:3]:
        f = dict(fit); f["slip"] = dict(a=t[2], b=t[3], win=t[0], ref=t[1])
        fam.append(("slips fitted on a %d-quarter window against %.0f (the next-best fit)" % (t[0], t[1]), outcome(L, proj(GOLDEN, f))))
    tb2 = []; support_model(L, table=tb2); tb2.sort(key=lambda t: t[3])
    for t in tb2[1:3]:
        f = dict(fit); f["support"] = dict(sigma=t[2], lag=t[0], e_star=t[1])
        fam.append(("defensive follow-ons from %.0f on the index, %d quarters late" % (100 * t[1], t[0]), outcome(L, proj(GOLDEN, f))))
    f = dict(fit); f["support"] = dict(support_model(L, pts=support_points(L, basis="value")), basis="value")
    fam.append(("defensive follow-ons measured and carried on the held companies' latest value, not their cost", outcome(L, proj(GOLDEN, f))))
    f = dict(fit); f["rho"] = {m: float(np.median(list(fit["rho"].values()))) for m in fit["rho"]}
    fam.append(("recycling at the median of every manager", outcome(L, proj(GOLDEN, f))))
    f = dict(fit); f["eta"] = 0.0
    fam.append(("new deals at their normal pace, no deal-market term", outcome(L, proj(GOLDEN, f))))
    f = dict(fit); f["fee"] = {k: v * 0.95 for k, v in fit["fee"].items()}
    fam.append(("fees 5 per cent below the investing-period median", outcome(L, proj(GOLDEN, f))))
    stp, _ = line_stock(L, recycling="none")
    fam.append(("the line stock with no recycling since the last audited year-end", outcome(L, proj(GOLDEN, stt=[fund_state(L, fid, stp) for fid in L["reg"]]))))
    R["family"] = fam
    R["slip_table"], R["support_table"] = tab, tb2
    # the factorial
    fac = {}
    for tag, sw in [("J1 dropped", dict(GOLDEN, line="recycled")), ("J2 dropped", dict(GOLDEN, support="none")), ("J3 dropped", dict(GOLDEN, closes="expected")),
                    ("J1 alone", dict(REFLEX, line="rebuilt")), ("J2 alone", dict(REFLEX, support="measured")), ("J3 alone", dict(REFLEX, closes="slip"))]:
        fac[tag] = outcome(L, proj(sw)); fac[tag]["R1"] = R["golden"]["R1"]
    R["factorial"] = fac
    # the budget sweep: the reserve left above the minimum at each budget (the needs are linear in the budget)
    g = R["golden"]; h0 = g["R6"] + 500.0 * g["c_plan"]
    R["sweep"] = [(b, round(h0 - g["c_plan"] * b, 1)) for b in range(0, 1001, 25)]
    R["test_at"] = {b: outcome_at(L, proj(GOLDEN), b) for b in (250.0, 500.0)}
    # the fitted inputs for the workbook
    R["dep"], R["fee"], R["rho"] = fit["dep"], fit["fee"], fit["rho"]
    # the bootstrap over funds: every fitted input refitted on resampled funds, the portfolio projected as it stands
    rng = np.random.default_rng(5)
    fids = list(L["reg"]); bs = defaultdict(list)
    for b in range(boot):
        pick = rng.choice(len(fids), len(fids), replace=True)
        Lb = dict(L); Lb["reg"], Lb["st"], Lb["act"], Lb["aud"] = {}, {}, {}, {}
        for j, i in enumerate(pick):
            fid = fids[i]; k = "%s#%d" % (fid, j)
            Lb["reg"][k] = L["reg"][fid]; Lb["st"][k] = L["st"].get(fid, {}); Lb["act"][k] = L["act"].get(fid, []); Lb["aud"][k] = L["aud"].get(fid, {})
        fb, _, _, _ = fit_all2(Lb)
        for name, keys in (("deployment and the deal-market term", ("dep", "eta")), ("defensive follow-ons", ("support",)),
                           ("first-close slips", ("slip",)), ("recycling", ("rho",)), ("every fitted input together", ("dep", "eta", "support", "slip", "fee", "rho"))):
            f = dict(fit)
            for k in keys: f[k] = fb[k]
            bs[name].append(outcome(L, proj(GOLDEN, f))["B"])
        bs["eta"].append(fb["eta"]); bs["sigma"].append(fb["support"]["sigma"]); bs["slip_b"].append(fb["slip"]["b"])
    R["boot"] = {k: [float(x) for x in v] for k, v in bs.items()}
    return R
