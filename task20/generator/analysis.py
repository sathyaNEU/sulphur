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
    L["bench"] = rows(P("industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv"))
    L["cov"] = coverage(L)
    L["hold"] = sheet(P("liquid_holdings_2026-12-31.xlsx"))
    L["spend"] = {int(r["fiscal_year"]): float(r["approved_distribution_usd_m"]) for r in rows(P("spending_distributions_FY2014_FY2027.csv"))}
    names = {r["Fund"]: fid for fid, r in L["reg"].items()}
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

# ------------------------------------------------------------------------------------------------ the policy
FACTORS = {"Cash, money market funds and US Treasuries": 1.00, "Investment-grade bonds": 0.90, "Public equities": 0.70,
           "Hedge funds: redeemable within 24 months": 0.90}
CUSHION = 1535.0
GRID = 25.0

def reserve(L):
    return sum(float(h["Market value 31 Dec 2026 (USD m)"]) * FACTORS.get(h["Policy liquidity class"], 0.0)
               for h in L["hold"] if h["Policy liquidity class"])

def spending24(L):
    return 2.0 * L["spend"][2027]

def coverage(L):
    """the quarter each manager's company-level activity ends, for the managers whose funds' statements run on past it
    (the look-through feed stopped): {manager: last activity quarter}."""
    act_end = defaultdict(lambda: -1); st_end = defaultdict(lambda: -1)
    for fid, r in L["reg"].items():
        m = r["Manager"]
        if L["act"].get(fid): act_end[m] = max(act_end[m], max(e[0] for e in L["act"][fid]))
        if L["st"].get(fid): st_end[m] = max(st_end[m], max(L["st"][fid]))
    return {m: q for m, q in act_end.items() if st_end.get(m, -1) == H_END and q <= H_END - 4}

def covered_to(L, fid):
    """the last quarter the activity file covers the fund (H_END where the feed runs on)."""
    return L.get("cov", {}).get(L["reg"][fid]["Manager"], H_END)

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

def line_stock(L, recycling="manager", bridge=True, at=None, uncovered="bridged"):
    """the capital each manager has invested on its fund's subscription line and not yet called, at the endowment's
    share, at 31 December 2026: the gap between investments and investment calls less the proceeds the fund recycled,
    the recycled amount read off the audited year-ends (gap less the audited borrowings) and carried to the end of 2026
    at the manager's own recycling rate while the fund is still investing. For a manager whose company-level file
    stopped, the gap cannot be formed after the file ends: its funds' stock is their latest audited borrowings grown as
    the covered managers' stock grew from the same audit date (bridge=False: the file read as it stands)."""
    res = {}
    rho_m = defaultdict(list)
    per = {}
    for fid, r in L["reg"].items():
        if r["Status"] == "pending first close": continue
        g = gap_series(L, fid)
        if not g: continue
        sh = share(L, fid)
        aud = L["aud"].get(fid, {})
        cov = covered_to(L, fid) if bridge else H_END
        ip_end = q_of(r["Investment period ends"].date() if hasattr(r["Investment period ends"], "date") else r["Investment period ends"])
        pts = []
        for qa, a_ in sorted(aud.items()):
            if qa in g and qa <= cov:
                gap, cp, _ = g[qa]
                rec = gap - a_["Credit facility borrowings"] * sh
                pts.append((qa, rec, cp, a_["Credit facility borrowings"] * sh))
        per[fid] = dict(g=g, pts=pts, sh=sh, ip_end=ip_end, mgr=r["Manager"], size=float(r["Fund size (USD m)"]), cov=cov, aud=aud)
        if len(pts) >= 1 and pts[-1][2] > 0:
            cp_ip = sum(g[q][2] for q in g if q <= min(pts[-1][0], ip_end))
            if cp_ip > 1e-6:
                rho_m[r["Manager"]].append(max(pts[-1][1], 0.0) / cp_ip)
    def path(x):
        """the rebuilt stock at each quarter from the last usable audit to the end of 2026."""
        g, pts, sh = x["g"], x["pts"], x["sh"]
        if pts: qa, rec = pts[-1][0], pts[-1][1]
        else: qa, rec = min(g) - 1, 0.0
        rho = float(np.median(rho_m[x["mgr"]])) if (recycling == "manager" and rho_m.get(x["mgr"])) else 0.0
        cap = 0.15 * x["size"] * sh
        out, rec_q = {}, rec
        for q in range(qa + 1, H_END + 1):
            if q <= x["ip_end"]: rec_q = min(rec_q + rho * g[q][2], cap)
            out[q] = max(g[q][0] - rec_q, 0.0)
        if pts: out[qa] = max(pts[-1][3], 0.0)
        return out
    paths = {fid: path(x) for fid, x in per.items() if x["cov"] == H_END}
    for fid, x in per.items():
        if x["cov"] == H_END:
            res[fid] = paths[fid].get(H_END, 0.0)
            continue
        # the bridge: the stock where the file stops, rolled on the fitted pace less the statements' investment calls,
        # re-anchored at each later audited year-end (hurried: "zero", the file's gap as it stands; "audited", the latest
        # audited borrowings carried to 31 December 2026)
        if uncovered == "zero": res[fid] = 0.0
        elif uncovered == "audited":
            aud = {q: v for q, v in x["aud"].items() if v.get("Credit facility borrowings") is not None}
            res[fid] = aud[max(aud)]["Credit facility borrowings"] * x["sh"] if aud else 0.0
        else: res[fid] = uncovered_path(L, fid, x)["stock"]
    return res, per

_DEP = {}

def _dep_fit(L):
    k = id(L)
    if k not in _DEP: _DEP[k] = deploy_rates(L)
    return _DEP[k]

BRIDGE = {"anchor": True}

def uncovered_path(L, fid, x=None, anchor=None):
    """for a fund whose manager's company-level file stopped: the investments after the file ends at the pace fitted
    on the covered quarters, the line stock rolled from the file's last quarter (investments less the statements'
    investment calls) and re-anchored at each later audit, and the companies held, their cost reduced by the
    statements' returned capital and the new investments added as they are made."""
    anchor = BRIDGE["anchor"] if anchor is None else anchor
    r = L["reg"][fid]; sh = share(L, fid); C = float(r["Commitment (USD m)"]); st = STRATS[r["Strategy"]]
    fc = q_of(r["First close"].date() if hasattr(r["First close"], "date") else r["First close"])
    ipe = q_of(r["Investment period ends"].date() if hasattr(r["Investment period ends"], "date") else r["Investment period ends"])
    cov = covered_to(L, fid)
    dep, eta = _dep_fit(L)
    g = gap_series(L, fid)
    inv = sum(a_ * sh for q, t, co, a_, cb in L["act"].get(fid, []) if t in ("initial investment", "follow-on investment") and q <= cov)
    stock = 0.0
    if g and cov in g:
        # the stock at the file's last quarter: the gap less the recycled amount read at the last audit before it
        x = x or {}
        pts = [p for p in (x.get("pts") or []) if p[0] <= cov]
        rec = pts[-1][1] if pts else 0.0
        stock = max(g[cov][0] - rec, 0.0)
    s = L["st"].get(fid, {}); aud = L["aud"].get(fid, {})
    new, q_start = {}, max(cov + 1, fc)
    for q in range(q_start, H_END + 1):
        a_ = (q - fc) // 4
        room = max(C - inv, 0.0) if q < ipe else 0.0
        I = _cell(dep, st, a_, 0.05) * room * max(min(_mkt_e(L["E"], q) / 100.0, 1.4), 0.4) ** (eta[st] if isinstance(eta, dict) else eta)
        inv += I; new[q] = I
        stock = max(stock + I - s.get(q, {}).get("contributions_investments_usd", 0.0), 0.0)
        if anchor and q in aud and aud[q].get("Credit facility borrowings") is not None:
            stock = aud[q]["Credit facility borrowings"] * sh
    roc = sum(s[q]["distributions_return_of_capital_usd"] for q in range(cov + 1, H_END + 1) if q in s)
    return dict(stock=stock, new=new, inv=inv, roc=roc, cov=cov)

# ------------------------------------------------------------------------------------------------ the stress path
def stress_market(L):
    """the policy's scenario: exits as 2008Q3-2010Q2 relative to 2008Q2 on the 2026Q4 level; equities 85, 70, then five
    points a quarter back to 100 percent; short rates up 2.5 points."""
    E, S, R = L["E"], L["S"], L["R"]
    e = np.concatenate([E, np.zeros(8)]); s = np.concatenate([S, np.zeros(8)]); r = np.concatenate([R, np.zeros(8)])
    eq = [0.85, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    for k in range(8):
        e[H_END + 1 + k] = E[H_END] * E[qi(2008, 3) + k] / E[qi(2008, 2)]
        s[H_END + 1 + k] = S[H_END] * eq[k]
        r[H_END + 1 + k] = R[H_END] + 2.5
    return e, s, r

# ------------------------------------------------------------------------------------------------ fund states and rates
def fund_state(L, fid, stock, bridge=True):
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
    if fc is not None and covered_to(L, fid) < H_END:
        if bridge:
            inv = uncovered_path(L, fid)["inv"]
        else:   # the file to its last quarter, then the capital called since as what was invested
            cov = covered_to(L, fid)
            inv = sum(a for q, t, co, a, cb in L["act"].get(fid, []) if t in ("initial investment", "follow-on investment") and q <= cov) * (sh or 0)
            inv += sum(v["contributions_investments_usd"] for q, v in s.items() if q > cov)
    fee_last = s[max(s)]["contributions_management_fees_usd"] if s else 0.0
    te = r["Term ends"]
    term = q_of(te.date() if hasattr(te, "date") else te) if te else None
    return dict(fid=fid, st=st, C=C, paid=paid, unf=C - paid, nav=nav, fc=fc, ipe=ipe, sh=sh, inv=inv, mgr=r["Manager"], term=term,
                stock=stock.get(fid, 0.0), fee_q=fee_last, pending=(r["Status"] == "pending first close"), liquidated=(r["Status"] == "liquidated"),
                exp_fc=q_of(r["First close expected at commitment"].date() if hasattr(r["First close expected at commitment"], "date") else r["First close expected at commitment"]))

DEAL_WIN = [1.0, 1.0, 1.0]

def _mkt_e(E, q):
    """the exit index the deal market answers to: the quarter's own and, where the window is longer, the quarters before."""
    w = DEAL_WIN
    return float(sum(wt * E[max(q - k, 0)] for k, wt in enumerate(w)) / sum(w))

def deploy_rates(L, defensive=False, covered_only=True, by_strategy=False, eta_fixed=None):
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
        end = covered_to(L, fid) if covered_only else H_END
        ipe = _qd(r["Investment period ends"])
        if ipe is not None: end = min(end, ipe)          # new deals stop when the investment period ends
        for q in range(fc, end + 1):
            a = (q - fc) // 4
            room = max(C - cum, 0.0)
            if room > 0.02 * C and a < 7:
                obs.append((st, a, inv.get(q, 0.0) / room, _mkt_e(L["E"], q), room))
            cum += allinv.get(q, 0.0)
    # the deal market's elasticity by least squares on the amounts, each cell's rate the ratio of sums at that elasticity
    cells = defaultdict(list)
    for st, a, y, e, room in obs: cells[(st, a)].append((y * room, room, max(min(e / 100.0, 1.4), 0.4)))
    if by_strategy:
        out_rate, out_eta = {}, {}
        for st in sorted({k[0] for k in cells}):
            r_, e_ = _fit_cells({k: v for k, v in cells.items() if k[0] == st}, eta_fixed)
            out_rate.update(r_); out_eta[st] = e_
        return out_rate, out_eta
    return _fit_cells(cells, eta_fixed)

def _fit_cells(cells, eta_fixed=None):
    best = None
    for eta in (np.round(np.arange(-1.0, 1.01, 0.02), 2) if eta_fixed is None else [eta_fixed]):
        sse = 0.0; rate = {}
        for k, v in cells.items():
            I = np.array([x[0] for x in v]); R_ = np.array([x[1] for x in v]); M = np.array([x[2] for x in v]) ** eta
            rate[k] = float(I.sum() / (R_ * M).sum()) if (R_ * M).sum() > 0 else 0.0
            sse += float(((I - rate[k] * R_ * M) ** 2).sum())
        if best is None or sse < best[0]: best = (sse, float(eta), rate)
    return best[2], best[1]

def routine_follow_ons(L):
    """the routine follow-on a company takes a year or more after its first investment (the first follow-on within two
    years of it), as a share of the first investment, and the quarter it comes, by strategy (medians over the companies
    the activity file follows that long)."""
    sh_, lag_ = defaultdict(list), defaultdict(list)
    for fid, ev in L["act"].items():
        r = L["reg"].get(fid)
        if not r: continue
        st = STRATS[r["Strategy"]]; cov = covered_to(L, fid)
        first, done = {}, set()
        for q, t, co, a, cb in sorted(ev):
            if t == "initial investment": first[co] = (q, a)
            elif t == "follow-on investment" and co in first and co not in done:
                q0, a0 = first[co]
                if 4 <= q - q0 < 8 and a0 > 0:
                    sh_[st].append(a / a0); lag_[st].append(q - q0); done.add(co)
    return {st: dict(share=float(np.median(v)), lag=int(round(float(np.median(lag_[st]))))) for st, v in sh_.items() if len(v) >= 5}

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
def held_deals(L, fid, bridge=True):
    """the fund's companies still held at 31 December 2026 (endowment share): cost, first investment quarter, last value.
    Where the manager's company-level file stopped, the companies held when it stopped, their cost reduced by the
    capital the statements return since, and the investments made since (bridge=False: the file as it stands)."""
    if bridge and covered_to(L, fid) < H_END and L["reg"][fid]["First close"]:
        held = _held_from_file(L, fid)
        up = uncovered_path(L, fid)
        tot = sum(d["cost"] for d in held)
        keep = max(1.0 - up["roc"] / tot, 0.0) if tot > 0 else 0.0
        out = [dict(d, cost=d["cost"] * keep, fv=d["fv"] * keep) for d in held]
        out += [dict(co="since %d" % q, q0=q, cost=I, fv=I) for q, I in up["new"].items() if I > 0]
        return out
    return _held_from_file(L, fid)

def _held_from_file(L, fid):
    sh = share(L, fid)
    first = {}; cost = defaultdict(float); last_val = {}; gone = set(); fo = set(); init = {}
    for q, t, co, a, cb in sorted(L["act"].get(fid, [])):
        if t == "initial investment": first[co] = q; cost[co] += a * sh; init[co] = a * sh
        elif t == "follow-on investment":
            cost[co] += a * sh
            if co in first and q - first[co] < 8: fo.add(co)
        elif t == "realization": gone.add(co)
        elif t == "valuation": last_val[co] = (q, a * sh, cb * sh)
    return [dict(co=c, q0=first[c], cost=cost[c], fv=last_val.get(c, (None, cost[c]))[1], init=init.get(c, cost[c]), fo_done=c in fo)
            for c in first if c not in gone]

def support_points(L, basis="cost", covered_only=True):
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
        for q in range(min(byq), (covered_to(L, fid) if covered_only else H_END) + 1):
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

def own_record_max_shortfall(L, lag=2):
    """the deepest exit-market shortfall (lagged as the support fit lags it) over the quarters the endowment's own funds
    show defensive follow-ons on a pool of companies held two years or more."""
    return max(max(0.0, 1.0 - L["E"][q - lag] / 100.0) for q, _, _ in support_points(L))

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

def support_two_channel(L, covered_only=True, caps=(0.20, 0.25, 0.30, 0.35, 0.40, 9.0), table=None):
    """the first channel on the endowment's own funds (defensive follow-ons on the aged cost, two quarters after the exit
    index, capped where the managers' reserves run out, the cap chosen by fit); the second channel from the benchmark's
    funds past their investment period, where new deals cannot move: their calls per unit of commitment by quarter
    against the same shortfall, the rise past a threshold over the plateau giving the second channel's size relative
    to the first (threshold by fit)."""
    pts = support_points(L, covered_only=covered_only)
    q = np.array([p[0] for p in pts]); s = np.array([p[1] for p in pts]); pool = np.array([p[2] for p in pts]); y = s / pool
    sf = np.maximum(0.0, 1.0 - L["E"][np.maximum(q - 2, 0)] / 100.0)
    best = None
    for cap in caps:
        x = np.minimum(sf, cap); sig = float(np.sum(pool * x * y) / np.sum(pool * x * x)); sse = float(np.sum(pool * (y - sig * x) ** 2))
        if table is not None: table.append(("cap", cap, sig, sse))
        if best is None or sse < best[0]: best = (sse, cap, sig)
    _, cap, sig1 = best
    bq = bench_old_calls(L)
    qs = np.array(sorted(bq)); c = np.array([bq[k] for k in qs]); sfb = np.array([max(0.0, 1.0 - L["E"][k - 2] / 100.0) for k in qs])
    b2 = None
    for th in np.round(np.arange(0.36, 0.56, 0.01), 2):
        X = np.column_stack([np.ones(len(qs)), np.minimum(sfb, cap), np.maximum(0.0, sfb - th)])
        coef, *_ = np.linalg.lstsq(X, c, rcond=None); sse = float(np.sum((c - X @ coef) ** 2))
        if table is not None: table.append(("threshold", float(th), float(coef[2] / coef[1]) if coef[1] > 0 else 0.0, sse))
        if b2 is None or sse < b2[0]: b2 = (sse, float(th), coef)
    _, th, coef = b2
    ratio = float(coef[2] / coef[1]) if coef[1] > 0 else 0.0
    return dict(sigma=sig1, cap=cap, lag=2, e_star=1.0, th=th, ratio=ratio, sigma2=sig1 * ratio, sse=best[0])

def bench_old_calls(L, lo=25, hi=44, q0=None, q1=None, min_unfunded=10.0):
    """the benchmark's buyout, growth and venture funds past their investment period and its follow-on window (more than
    six years from the vintage, so new deals and routine follow-ons cannot move their calls) and with commitment left to
    call: mean calls per unit of commitment by quarter, 2004 to 2014."""
    q0 = qi(2004, 1) if q0 is None else q0; q1 = qi(2014, 4) if q1 is None else q1
    byq = defaultdict(list); paid = defaultdict(float)
    for r in sorted(L["bench"], key=lambda r: (r["benchmark_fund"], r["period_end"])):
        key = r["benchmark_fund"]; c = float(r["contributions_pct_of_commitment"])
        if r["strategy"] in ("Buyout", "Growth equity", "Venture capital"):
            qq = q_of(D(r["period_end"])); age = qq - qi(int(r["vintage"]), 1)
            if lo <= age <= hi and q0 <= qq <= q1 and float(r["nav_pct_of_commitment"]) > 5 and 100.0 - paid[key] >= min_unfunded:
                byq[qq].append(c / 100.0)
        paid[key] += c
    return {k: float(np.mean(v)) for k, v in byq.items()}

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

# ------------------------------------------------------------------------------------------------ the successor clause
def _qd(v):
    return q_of(v.date() if hasattr(v, "date") else v) if v else None

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
    """the quarters the fund's successor holds its first close, with weights (its manager's date slipped on the stress as
    the pending funds' are); None where it already closed by the end of 2026 or there is none."""
    s = fit["succ"].get(fid)
    if s is None: return None
    kind, ref = s
    if kind == "reg":
        r = L["reg"][ref]
        if r["First close"]: return None
        exp = _qd(r["First close expected at commitment"])
    else:
        exp = next(p["exp_fc"] for p in L["plan"] if p["fund"] == ref)
    if sw.get("closes_succ", sw.get("closes", "slip")) == "expected": return [(exp, 1.0)]
    sl = expected_slip(fit, e, exp); k = int(math.floor(sl)); fr = sl - k
    return [(exp + k, 1.0 - fr), (exp + k + 1, fr)] if fr > 1e-9 else [(exp + k, 1.0)]

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
        if not r or STRATS[r["Strategy"]] not in ("RE", "IN"): continue
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

def value_response(L):
    """the quarterly change in the real assets' value (equity valuation plus loan) against the change in equities and in
    the short rate, on assets past their four-year plan: log value change = beta x log equity change (a quarter late) +
    log((1 + c r[q-2]) / (1 + c r[q-1])), beta and c by least squares over a grid of c."""
    vals, _ = _equity_vals(L); bal = {}
    for key, ev in L["loans"].items():
        b = []
        for q, t, a, m in sorted(ev, key=lambda x: x[0]):
            if t != "proceeds": b.append((q, a))
        bal[key] = b
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
            if q - 1 in vs and q - first >= 17:
                d1, d0 = loan_at(q), loan_at(q - 1)
                if d1 is None or d0 is None or abs(d1 - d0) > 1e-6: continue
                g1, g0 = vs[q] + d1, vs[q - 1] + d0
                if g1 > 0 and g0 > 0: obs.append((q, math.log(g1 / g0)))
    best = None
    S, R = L["S"], L["R"]
    for c in np.round(np.arange(0.0, 0.151, 0.005), 3):
        X = np.array([math.log(S[q - 1] / S[q - 2]) for q, _ in obs])
        Y = np.array([y - math.log((1 + c * R[q - 2]) / (1 + c * R[q - 1])) for q, y in obs])
        beta = float(np.sum(X * Y) / np.sum(X * X)); sse = float(np.sum((Y - beta * X) ** 2))
        if best is None or sse < best[0]: best = (sse, float(c), beta)
    return dict(c=best[1], beta=best[2], n=len(obs))

def loans_due(L, fit, mkt, fid, bridge=True):
    """the fund's real-asset loans alive at 31 December 2026 that come due in the eight quarters: balance and maturity at
    the endowment's share and the asset's value at 31 December 2026 (its last valuation plus the loan, rolled to the end
    of 2026 on the fitted value response where the manager's company-level file stopped, and the loans scaled by the
    share of cost the fund still holds on its statements since)."""
    vals, gone = _equity_vals(L); sh = share(L, fid)
    cov = covered_to(L, fid) if bridge else H_END
    out = []
    keep = 1.0
    if bridge and cov < H_END:
        held = _held_from_file(L, fid); tot = sum(d["cost"] for d in held)
        roc = sum(v["distributions_return_of_capital_usd"] for q, v in L["st"].get(fid, {}).items() if q > cov)
        keep = max(1.0 - roc / tot, 0.0) if tot > 0 else 0.0
    vr = fit["value"]
    for (f2, co), x in asset_loans(L).items():
        if f2 != fid or (f2, co) in gone or x["balance"] is None: continue
        if x["maturity"] is None or x["maturity"] <= H_END: continue
        vs = vals.get((f2, co), {})
        if not vs: continue
        qv = max(vs); gross = vs[qv] + x["balance"]
        if qv < H_END:      # rolled to the end of 2026 on equities and the short rate
            gross *= (L["S"][H_END - 1] / L["S"][qv - 1]) ** vr["beta"] * (1 + vr["c"] * L["R"][qv - 1]) / (1 + vr["c"] * L["R"][H_END - 1])
        out.append(dict(co=co, D=x["balance"] * sh * keep, due=x["maturity"], P26=gross * sh * keep))
    return out

def refi_terms(fit, mkt, ln, q, terms="stressed"):
    """the asset's value and the loan-to-value a lender grants on it when its loan matures at quarter q."""
    e, s, r = mkt; vr, lr = fit["value"], fit["lender"]
    P = ln["P26"] if terms in ("current", "values_flat") else \
        ln["P26"] * (s[q - 1] / s[H_END - 1]) ** vr["beta"] * (1 + vr["c"] * r[H_END - 1]) / (1 + vr["c"] * r[q - 1])
    rate = r[H_END] if terms in ("current", "terms_flat") else r[q]
    return P, min(lr["cap_post"], lr["kappa"] / (rate + lr["spread"]))

def refi_gap(fit, mkt, ln, q, terms="stressed"):
    """the shortfall a maturing loan leaves at quarter q: its balance less what a lender grants on the asset's value then
    (the value at the end of 2026 moved on the stress path's equities and short rate)."""
    e, s, r = mkt; vr, lr = fit["value"], fit["lender"]
    P = ln["P26"] if terms in ("current", "values_flat") else \
        ln["P26"] * (s[q - 1] / s[H_END - 1]) ** vr["beta"] * (1 + vr["c"] * r[H_END - 1]) / (1 + vr["c"] * r[q - 1])
    rate = r[H_END] if terms in ("current", "terms_flat") else r[q]       # "current": the terms and values of 31 December 2026
    lim = min(lr["cap_post"], lr["kappa"] / (rate + lr["spread"]))
    return max(ln["D"] - lim * P, 0.0)

# ------------------------------------------------------------------------------------------------ the projection
def project2(L, states, plan, budget, sw, fit, mkt):
    """the policy's 24 months, quarter by quarter. Calls: the managers' investments (deployment of the room left, slowed
    by the deal market), the defensive follow-ons, the fees, less the proceeds recycled, plus the line stock called at
    the clean-down. Distributions: each fund's 31 December value times its strategy's 2008-10 benchmark rate.
    sw: line ('rebuilt' or 'recycled'), support ('measured' or 'none'), closes ('slip' or 'expected')."""
    e, s, r = mkt
    out = {k: np.zeros(len(e)) for k in ("call_inv", "call_pend", "call_plan", "dist", "support", "stock", "fees", "recycled", "fees_closed", "extended", "refi")}
    rho = fit["rho_h"] if sw["line"] == "recycled" else fit["rho"]
    rho_default = float(np.median(list(rho.values()))) if rho else 0.0       # a manager without an audited read: the median manager's
    dep = fit["dep_h"] if sw["support"] == "none" and "dep_h" in fit else fit["dep"]
    eta = fit["eta_h"] if sw["support"] == "none" and "eta_h" in fit else fit["eta"]
    if sw.get("market") == "pooled": dep, eta = fit["dep_p"], fit["eta_p"]
    elif sw.get("market", "none") == "none":          # the policy's normal pace: no deal-market term
        dep, eta = (fit["dep_h0"], 0.0) if sw["support"] == "none" and "dep_h0" in fit else (fit["dep_0"], 0.0)
    def closes(exp_q):
        """the first-close quarters with their weights: the expected slip split between the two quarters around it."""
        if sw["closes"] == "expected": return [(exp_q, 1.0)]
        sl = expected_slip(fit, e, exp_q); k = int(math.floor(sl)); fr = sl - k
        return [(exp_q + k, 1.0 - fr), (exp_q + k + 1, fr)] if fr > 1e-9 else [(exp_q + k, 1.0)]
    def run(st, C, fc, inv0, paid0, nav0, stock, deals, mgr, key, ipe=None, term=None, succ_q=None, loans=None, wt=1.0):
        inv, paid, nav = inv0, paid0, nav0
        if ipe is None: ipe = fc + (20 if st not in ("RE", "PC") else (16 if st == "RE" else 12))
        if succ_q is not None and succ_q < ipe: ipe = succ_q          # the successor's first close ends the period
        ext_q = ipe if (sw.get("extensions", "rule") == "rule" and "ext" in fit and ipe in W and key == "call_inv" and succ_q is None) else None
        deals = [dict(d) for d in deals]
        lns = [dict(l) for l in (loans or [])]
        cap_rec = 0.15 * C; rec_c = 0.0
        for k, q in enumerate(W):
            dx = nav0 * fit["drate"].get((st, k), 0.0)
            out["dist"][q] += dx * wt
            if q < fc: continue
            if term is not None and q > term: continue       # the term has ended: the commitment not called is released
            if ext_q is not None and q == ext_q:
                weak = float(np.mean([e[q - j] for j in range(1, fit["ext"]["win"] + 1)])) < fit["ext"]["e_star"]
                if weak and inv / C < fit["ext"]["s_star"]:
                    ipe = ipe + fit["ext"]["length"]; out["extended"][q] += C * wt          # the period extended
            if succ_q is not None and q == succ_q and q < ipe: ipe = q
            a = (q - fc) // 4
            # the fee: on the commitment while investing, on the cost of the companies still held afterwards
            fee = fit["fee"][st] * C if q < ipe else fit["fee"][st] * sum(d["cost"] for d in deals)
            room = max(C - inv, 0.0) if q < ipe else 0.0
            md = max(min(_mkt_e(e, q) / 100.0, 1.4), 0.4) ** (eta[st] if isinstance(eta, dict) else eta)
            ip_years = {"RE": 4, "PC": 3}.get(st, 5)
            I = _cell(dep, st, min(a, ip_years - 1), 0.05) * room * md       # an extended period invests at its last year's pace
            if q >= ipe and st in fit.get("routine", {}):
                rf = fit["routine"][st]
                for d in deals:          # after the period ends, a recent company still takes its routine follow-on
                    if not d.get("fo_done") and q - d["q0"] >= rf["lag"] and q < ipe + 8:
                        x_ = rf["share"] * d.get("init", d["cost"]); I += x_; d["cost"] += x_; d["fo_done"] = True
            sup = 0.0
            if sw["support"] != "none" and st in ("BO", "GE", "VC"):
                sp = fit["support"]
                pool = sum(d["cost"] for d in deals if q - d["q0"] >= 8)
                sfq = max(0.0, sp["e_star"] - e[max(q - sp["lag"], 0)] / 100.0) / sp["e_star"]
                if sw["support"] == "two_channel":
                    rate = sp["sigma"] * min(sfq, sp["cap"]) + sp["sigma2"] * max(0.0, sfq - sp["th"])
                elif sw["support"] == "capped":           # the first channel's plateau held past the record
                    rate = sp["sigma"] * min(sfq, sp["cap"])
                else:                                     # one straight line through the record, carried on
                    rate = sp["sigma_lin"] * sfq
                sup = min(rate * pool, max(C - paid - I - fee, 0.0))
            # a real-asset loan that comes due is refinanced at the lender's limit on the asset's value; the shortfall is
            # called while the commitment allows (a shortfall the fund cannot meet waits a year on an extension)
            gap_paid = 0.0
            if lns and sw.get("refi", "loans") != "none":
                for ln in lns:
                    if ln["due"] != q: continue
                    gap = refi_gap(fit, mkt, ln, q, terms=sw["refi"] if sw.get("refi") in ("current", "values_flat", "terms_flat") else "stressed")
                    pay = min(gap, max(C - paid - I - sup - fee - gap_paid, 0.0))
                    gap_paid += pay; ln["D"] -= pay
                    ln["due"] = q + 4 if pay < gap - 1e-9 else None
            rc = min(rho.get(mgr, rho_default) * dx, max(cap_rec - rec_c, 0.0), I + sup) if q < ipe else 0.0
            rec_c += rc
            call = max(I + sup + fee - rc, 0.0) + gap_paid + (stock if q == W[0] else 0.0)
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
            if I > 0: deals.append(dict(co="new", q0=q, cost=I, fv=I, init=I, fo_done=q >= ipe))
            nav = max(nav - dx + I + sup, 0.0)
            out[key][q] += call * wt; out["support"][q] += sup * wt; out["fees"][q] += fee * wt; out["recycled"][q] += rc * wt
            out["refi"][q] += gap_paid * wt
            if key == "call_inv": out["fees_closed"][q] += fee * wt
            if q == W[0]: out["stock"][q] += stock * wt
    for x in states:
        if x.get("liquidated"): continue
        if x["pending"]:
            for fc, wgt in closes(x["exp_fc"]):
                run(x["st"], x["C"] * wgt, fc, 0.0, 0.0, 0.0, 0.0, [], x["mgr"], "call_pend")
        else:
            st_ = x["stock"] if sw["line"] == "rebuilt" else 0.0
            deals = held_deals(L, x["fid"], bridge=sw.get("uncovered", "bridged") == "bridged" and sw.get("held", "bridged") == "bridged")
            if fit["support"].get("basis") == "value":
                deals = [dict(d, cost=d["fv"]) for d in deals]
            loans = loans_due(L, fit, mkt, x["fid"], bridge=sw.get("uncovered", "bridged") == "bridged") if x["st"] in ("RE", "IN") else None
            sc = None
            if sw.get("succession", "clause") == "clause" and fit["clause"].get(x["mgr"]):
                sc = successor_close(L, fit, e, x["fid"], sw)
            for sq, wgt in (sc or [(None, 1.0)]):
                run(x["st"], x["C"], x["fc"], x["inv"], x["paid"], max(x["nav"], 0.0), st_, deals, x["mgr"], "call_inv",
                    ipe=(x["ipe"] + 1) if x.get("ipe") is not None else None, term=x.get("term"), succ_q=sq, loans=loans, wt=wgt)
    tot = sum(p["C"] for p in plan)
    for p in plan:
        for fc, wgt in closes(p["exp_fc"]):
            run(p["st"], budget * p["C"] / tot * wgt, fc, 0.0, 0.0, 0.0, 0.0, [], p.get("mgr", ""), "call_plan")
    return out

project3 = project2

def fit_all2(L, coverage="bridged"):
    """every fitted input. coverage "bridged": the fits on the quarters the company-level file covers and the uncovered
    funds bridged from the complete records; "as_is": the file read as it stands."""
    cov_only = coverage == "bridged"
    mkt = stress_market(L)
    dep, eta = deploy_rates(L, covered_only=cov_only, by_strategy=True)
    dep_h, eta_h = deploy_rates(L, defensive=True, covered_only=cov_only)
    dep_p, eta_p = deploy_rates(L, covered_only=cov_only, by_strategy=False)
    dep_0, _ = deploy_rates(L, covered_only=cov_only, eta_fixed=0.0)
    dep_h0, _ = deploy_rates(L, defensive=True, covered_only=cov_only, eta_fixed=0.0)
    stock, per = line_stock(L, bridge=cov_only)
    sp = support_two_channel(L, covered_only=cov_only)
    sp["sigma_lin"] = support_model(L, pts=support_points(L, covered_only=cov_only))["sigma"]
    succ, clause, votes = successions(L)
    fit = dict(dep=dep, eta=eta, dep_h=dep_h, eta_h=eta_h, dep_p=dep_p, eta_p=eta_p, dep_0=dep_0, dep_h0=dep_h0, slip=slip_model(L), fee=fee_rates(L), beta=nav_beta(L),
               support=sp, rho=recycling_rates(L, per), rho_h=recycling_rates(L, per, hurried=True),
               drate=bench_rates_2008(L), coverage=coverage, ext=extension_rule(L), succ=succ, clause=clause, clause_votes=votes,
               lender=lender_rule(L), value=value_response(L), routine=routine_follow_ons(L))
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
    def run(st, C, unf, fc, nav0, key, term=None):
        for k, q in enumerate(W):
            out["dist"][q] += nav0 * fit["drate"].get((st, k), 0.0)
            if q < fc or (term is not None and q > term): continue
            a = (q - fc) // 4
            c = rate_of(st, a, k) * unf
            unf -= c; out[key][q] += c
    for x in states:
        if x.get("liquidated"): continue
        if x["pending"]: run(x["st"], x["C"], x["C"], x["exp_fc"], 0.0, "call_pend")
        else: run(x["st"], x["C"], max(x["unf"], 0.0), x["fc"], max(x["nav"], 0.0), "call_inv", term=x.get("term"))
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
    fam.append(("fees 5 percent below the investing-period median", outcome(L, proj(GOLDEN, f))))
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

def extension_points(L):
    """every fund whose agreed investment period ended by the end of 2026: whether the register shows it extended, the
    share of its commitment invested by the agreed end and the exit index over the four quarters before it."""
    out = []
    for fid, r in L["reg"].items():
        if not r["First close"] or not r["Investment period ends"] or not r["Investment period (years, per agreement)"]: continue
        fc = q_of(r["First close"].date() if hasattr(r["First close"], "date") else r["First close"])
        ipe = q_of(r["Investment period ends"].date() if hasattr(r["Investment period ends"], "date") else r["Investment period ends"])
        agreed = fc + 4 * int(r["Investment period (years, per agreement)"])
        if agreed > H_END or ipe + 1 < agreed: continue      # a period its successor's first close ended never reached its agreed end
        C = float(r["Commitment (USD m)"]); sh = share(L, fid)
        inv = sum(a_ * sh for q, t, co, a_, cb in L["act"].get(fid, []) if t in ("initial investment", "follow-on investment") and q < agreed) / C
        out.append((ipe + 1 > agreed, inv, {w_: float(np.mean([L["E"][agreed - k] for k in range(1, w_ + 1)])) for w_ in (1, 2, 4)}, fid,
                    (ipe + 1 - agreed) if ipe + 1 > agreed else 0))
    return out

def extension_rule(L, table=None):
    """the rule that sorts the register's extended periods from the rest: an extension when the exit index over the
    quarters before the agreed end (the window by fit) sits below e_star and the fund has invested less than s_star of
    its commitment, each threshold set midway between the nearest cases either side; the length is the register's own."""
    pts = extension_points(L)
    best = None
    for win in (1, 2, 4):
        for e_star in (80.0, 85.0, 90.0, 95.0, 100.0, 105.0):
            for s_star in np.round(np.arange(0.50, 0.90, 0.01), 2):
                ok = sum((p[2][win] < e_star and p[1] < s_star) == p[0] for p in pts)
                if table is not None: table.append((win, e_star, float(s_star), ok))
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

# ------------------------------------------------------------------------------------------------ architecture 5: the programs
GOLDEN5 = dict(line="rebuilt", support="two_channel", closes="slip", coverage="bridged", uncovered="bridged", market="none",
               extensions="rule", succession="clause", refi="loans")
# the careful but hurried route: every reflex set right (the pinned support basis and facility balances included), every
# investment period held to its registered end and the real-asset loans rolled over as they stand
REFLEX5 = dict(GOLDEN5, succession="registered", refi="none")

def evaluate(L, sw, fit=None, mkt=None, stock=None):
    """the policy's test for every program on one route: the calls and distributions of the commitments made by the end
    of 2026 by half-year, the room above the minimum before any 2027 commitment, each program's calls and result, and
    the program the policy adopts."""
    if fit is None:
        fit, mkt, _, _ = fit_all2(L)
    bridged = sw.get("uncovered", "bridged") == "bridged"
    if stock is None:
        stock, _ = line_stock(L, bridge=True, uncovered=sw.get("uncovered", "bridged"))
    states = [fund_state(L, fid, stock, bridge=bridged) for fid in L["reg"]]
    o = project2(L, states, L["plan"], 0.0, sw, fit, mkt)
    RES, SPEND = reserve(L), spending24(L)
    calls = o["call_inv"] + o["call_pend"]
    need0 = float(calls[W].sum() - o["dist"][W].sum())
    H0 = round(round(RES, 1) - round(SPEND + need0, 1) - CUSHION, 1)
    by_fund = {}
    for p in L["plan"]:
        op = project2(L, states, [p], p["C"], sw, fit, mkt)
        by_fund[p["fund"]] = round(float(op["call_plan"][W].sum()), 1)
    progs = []
    for pr in L["programs"]:
        c = round(sum(by_fund[f] for f in pr["funds"]), 1)
        progs.append(dict(code=pr["code"], total=pr["total"], calls=c, headroom=round(H0 - c, 1), passes=H0 - c >= 0))
    passing = [p for p in progs if p["passes"]]
    adopt = max(passing, key=lambda p: p["total"])["code"] if passing else "none"
    stk = sum(v for f, v in stock.items() if L["reg"][f]["Status"] != "liquidated")
    return dict(R2={h: v for h, v in list(halves(calls).items())[:2]}, R3={h: v for h, v in list(halves(calls).items())[2:]},
                R4=halves(o["dist"]), R5=H0, R7=adopt, programs=progs, by_fund=by_fund, support=halves(o["support"]),
                stock=round(stk, 1), closed=halves(o["call_inv"]), pending=halves(o["call_pend"]), need0=round(need0, 1),
                refi=halves(o["refi"]))

def _support_variant(L, fit, th=None, lo=25, hi=44, mu=10.0, cap=None):
    """the two-channel support refitted with one choice changed (the second channel's threshold, the benchmark slice,
    the first channel's cap)."""
    sp = dict(fit["support"])
    if cap is not None:
        pts = support_points(L); q = np.array([p[0] for p in pts]); s = np.array([p[1] for p in pts]); pool = np.array([p[2] for p in pts]); y = s / pool
        sfv = np.maximum(0.0, 1.0 - L["E"][np.maximum(q - 2, 0)] / 100.0); x = np.minimum(sfv, cap)
        sp["cap"] = cap; sp["sigma"] = float(np.sum(pool * x * y) / np.sum(pool * x * x))
    th = sp["th"] if th is None else th
    bq = bench_old_calls(L, lo, hi, min_unfunded=mu); qs = np.array(sorted(bq)); c = np.array([bq[k] for k in qs])
    sfb = np.array([max(0.0, 1.0 - L["E"][k - 2] / 100.0) for k in qs])
    X = np.column_stack([np.ones(len(qs)), np.minimum(sfb, sp["cap"]), np.maximum(0.0, sfb - th)]); coef, *_ = np.linalg.lstsq(X, c, rcond=None)
    sp.update(th=th, ratio=float(coef[2] / coef[1]), sigma2=sp["sigma"] * float(coef[2] / coef[1]))
    f = dict(fit); f["support"] = sp
    return f

def lender_variant(L, fit, kind):
    """the lenders' rule refitted one defensible way otherwise: on every refinancing since 2020, or with the next-best
    cap and spread of the grid."""
    f = dict(fit)
    if kind == "since 2020":
        f["lender"] = lender_rule(L, since=qi(2020, 1))
    else:
        tab = []; lender_rule(L, table=tab); tab.sort(key=lambda t: t[3])
        best = fit["lender"]
        alt = next(t for t in tab if abs(t[0] - best["cap_post"]) > 0.004 or abs(t[1] - best["spread"]) > 0.01)
        f["lender"] = dict(best, cap_post=alt[0], spread=alt[1], kappa=alt[2])
    return f

def value_variant(L, fit, c=None, beta=None):
    f = dict(fit); v = dict(fit["value"])
    if c is not None: v["c"] = c
    if beta is not None: v["beta"] = beta
    f["value"] = v
    return f

def successor_events(L, fit, mkt):
    """the funds whose investment period the successor's first close ends inside the eight quarters, with the quarter
    (the expected one where a slip splits it)."""
    out = []
    for fid, r in L["reg"].items():
        if r["Status"] not in ("investing", "harvesting") or not fit["clause"].get(r["Manager"]): continue
        sc = successor_close(L, fit, mkt[0], fid, GOLDEN5)
        ipe = _qd(r["Investment period ends"])
        if not sc or ipe is None: continue
        q_exp = sum(q * w for q, w in sc)
        if q_exp < ipe + 1 and q_exp <= W[-1]:
            out.append(dict(fid=fid, fund=r["Fund"], successor=fit["succ"][fid][1] if fit["succ"][fid][0] == "plan" else L["reg"][fit["succ"][fid][1]]["Fund"],
                            close=round(q_exp, 2), registered_end=ipe))
    return out

def full5(tgt, boot=30):
    L = load(tgt)
    fit, mkt, stock, per = fit_all2(L); fit["mkt"] = mkt
    ev = lambda sw, f=None, stk=None: evaluate(L, sw, f or fit, mkt, stk)
    R = dict(L=L, fit=fit, stock=stock, per=per, mkt=mkt)
    g = ev(GOLDEN5); unf, pend = unfunded(L); g["R1"] = by_strategy(unf)
    R["golden"] = g
    R["reserve"], R["spending24"], R["cushion"] = round(reserve(L), 2), spending24(L), CUSHION
    R["uncovered"] = sorted(L["cov"])
    live = {fid: v for fid, v in stock.items() if L["reg"][fid]["Status"] != "liquidated"}
    R["line_stock_total"] = round(sum(live.values()), 1)
    R["line_stock_uncovered"] = round(sum(v for fid, v in live.items() if L["reg"][fid]["Manager"] in L["cov"]), 1)
    aud_stock, _ = line_stock(L, bridge=True, uncovered="audited")
    R["line_stock_uncovered_audited"] = round(sum(v for fid, v in aud_stock.items() if L["reg"][fid]["Status"] != "liquidated"
                                                  and L["reg"][fid]["Manager"] in L["cov"]), 1)
    R["pending"] = [dict(fid=fid, fund=L["reg"][fid]["Fund"], C=float(L["reg"][fid]["Commitment (USD m)"]),
                         slip=round(expected_slip(fit, mkt[0], _qd(L["reg"][fid]["First close expected at commitment"])), 2))
                    for fid in L["reg"] if L["reg"][fid]["Status"] == "pending first close"]
    R["successor_events"] = successor_events(L, fit, mkt)
    R["clause"] = {m: (v, fit["clause_votes"].get(m)) for m, v in fit["clause"].items()}
    # the real assets' loans that come due in the eight quarters
    due = []
    for fid, r in L["reg"].items():
        if STRATS[r["Strategy"]] in ("RE", "IN") and r["Status"] in ("investing", "harvesting"):
            for ln in loans_due(L, fit, mkt, fid):
                if ln["due"] in W:
                    Pq, lim = refi_terms(fit, mkt, ln, ln["due"])
                    due.append(dict(fid=fid, fund=r["Fund"], asset=ln["co"], due=ln["due"], D=round(ln["D"], 2), P26=round(ln["P26"], 2),
                                    P=round(Pq, 2), ltv=round(lim, 4), gap=round(refi_gap(fit, mkt, ln, ln["due"]), 2)))
    R["loans_due"] = due
    # the passes
    careful = ev(REFLEX5); careful["R1"] = g["R1"]
    ta = ta_fit(L)
    states_q = [fund_state(L, fid, stock) for fid in L["reg"]]
    def rates_route(rate_of):
        """the policy's test with every existing fund and re-up calling at a rate on its commitment not yet called."""
        o = project_rates(L, states_q, L["plan"], 0.0, fit, rate_of)
        RES, SPEND = reserve(L), spending24(L)
        calls = o["call_inv"] + o["call_pend"]; need0 = float(calls[W].sum() - o["dist"][W].sum())
        H0 = round(round(RES, 1) - round(SPEND + need0, 1) - CUSHION, 1)
        progs = []
        for pr in L["programs"]:
            c = 0.0
            for f_ in pr["funds"]:
                p = next(x for x in L["plan"] if x["fund"] == f_)
                op = project_rates(L, states_q, [p], p["C"], fit, rate_of); c += float(op["call_plan"][W].sum())
            progs.append(dict(code=pr["code"], total=pr["total"], calls=round(c, 1), headroom=round(H0 - c, 1), passes=H0 - c >= 0))
        passing = [p for p in progs if p["passes"]]
        hv = halves(calls)
        return dict(R2={h: hv[h] for h in HALVES[:2]}, R3={h: hv[h] for h in HALVES[2:]}, R4=halves(o["dist"]), R5=H0,
                    R7=max(passing, key=lambda p: p["total"])["code"] if passing else "none", programs=progs)
    def quick_eval():
        out = rates_route(ta_rate_of(ta))
        out.update(R4=dist_quick(L, fit), R1=by_strategy(unfunded_quick(L)))
        return out
    quick = quick_eval()
    R["passes"] = dict(quick=quick, careful=careful, thorough=g)
    # each reflex dropped alone from the golden (the design note's stump factorial)
    R["reflex_drops"] = {k: ev(sw) for k, sw in (
        ("J1 the support curve's plateau held past the record (the policy's benchmark basis set aside)", dict(GOLDEN5, support="capped")),
        ("J2 the six managers' last audited facility balances carried to 31 December 2026", dict(GOLDEN5, uncovered="audited")),
        ("J3 the covered managers' facility stock read as recycled proceeds", dict(GOLDEN5, line="recycled")),
        ("J4 no defensive follow-ons or rescue financings", dict(GOLDEN5, support="none")),
        ("J5 the pending funds on their managers' first-close dates", dict(GOLDEN5, closes="expected")),
        ("J6 no investment-period extensions", dict(GOLDEN5, extensions="none")),
        ("J7 new investments slowed by a deal-market term fitted on the endowment's own record", dict(GOLDEN5, market="pooled")))}
    R["own_record_max_shortfall"] = round(own_record_max_shortfall(L), 3)
    R["stress_max_shortfall"] = round(max(max(0.0, 1.0 - mkt[0][q - fit["support"]["lag"]] / 100.0) for q in W), 3)
    R["six_live_funds"] = sum(1 for r in L["reg"].values() if r["Manager"] in L["cov"] and r["Status"] in ("investing", "harvesting"))
    R["past_first_closes"] = sum(1 for r in L["reg"].values() if r.get("First close") and r.get("First close expected at commitment"))
    # the routes beside them
    R["routes"] = [("the golden", g),
                   ("the careful route: every investment period to its registered end, the real-asset loans rolled over as they stand", careful),
                   ("the real-asset loans rolled over as they stand, the successor's first close ending its predecessor's period", ev(dict(GOLDEN5, refi="none"))),
                   ("every investment period to its registered end, the loans refinanced at the stressed terms", ev(dict(GOLDEN5, succession="registered"))),
                   ("the loans refinanced at the lenders' terms and the values of 31 December 2026", ev(dict(GOLDEN5, refi="current"))),
                   ("the loans refinanced at 31 December's terms, every period to its registered end", ev(dict(GOLDEN5, refi="current", succession="registered"))),
                   ("the textbook pacing model on the capital accounts", quick),
                   ("the benchmark's 2008-10 call rates replayed on the commitments not yet called", rates_route(bench_rate_of(bench_call_rates(L), ta))),
                   ("the pacing model recalibrated on the 2022 to 2024 exit drought", rates_route(ta_rate_of(ta_fit(L, qi(2022, 1), qi(2024, 4)))))]
    # the golden family
    fam = []
    th0 = fit["support"]["th"]
    for th in (round(th0 - 0.03, 2), round(th0 + 0.03, 2)):
        fam.append(("the second channel from a shortfall of %.2f" % th, ev(GOLDEN5, _support_variant(L, fit, th=th))))
    for lo, hi, mu, tag in ((25, 40, 10.0, "funds six to ten years old"), (28, 44, 10.0, "funds seven to eleven years old"),
                            (25, 44, 5.0, "funds with 5 percent or more left to call"), (25, 44, 20.0, "funds with 20 percent or more left to call")):
        fam.append(("the benchmark slice of %s" % tag, ev(GOLDEN5, _support_variant(L, fit, lo=lo, hi=hi, mu=mu))))
    for cap in (0.25, 0.35):
        fam.append(("the first channel capped at a shortfall of %.2f" % cap, ev(GOLDEN5, _support_variant(L, fit, cap=cap))))
    f = dict(fit); f["rho"] = {m: float(np.median(list(fit["rho"].values()))) for m in fit["rho"]}
    fam.append(("recycling at the median of every manager", ev(GOLDEN5, f)))
    f = dict(fit); f["fee"] = {k: v * 0.95 for k, v in fit["fee"].items()}
    fam.append(("fees 5 percent below the investing-period median", ev(GOLDEN5, f)))
    tab = []; slip_model(L, table=tab); tab.sort(key=lambda t: t[4])
    for t in tab[1:3]:
        f = dict(fit); f["slip"] = dict(a=t[2], b=t[3], win=t[0], ref=t[1])
        fam.append(("slips fitted on a %d-quarter window against %.0f" % (t[0], t[1]), ev(GOLDEN5, f)))
    BRIDGE["anchor"] = False
    stk2, _ = line_stock(L)
    fam.append(("the six managers' facility balances rolled from the file's end, not re-anchored at the later audits", ev(GOLDEN5, None, stk2)))
    BRIDGE["anchor"] = True
    for kind in ("since 2020", "next-best"):
        fam.append(("the lenders' limit fitted %s" % ("on every refinancing since 2020" if kind == "since 2020" else "at the grid's next-best cap and spread"),
                    ev(GOLDEN5, lender_variant(L, fit, kind))))
    vc = fit["value"]["c"]
    for c in (max(vc - 0.01, 0.0), vc + 0.01):
        fam.append(("the assets' rate sensitivity at %.3f" % c, ev(GOLDEN5, value_variant(L, fit, c=c))))
    for bb in (fit["value"]["beta"] - 0.05, fit["value"]["beta"] + 0.05):
        fam.append(("the assets' equity sensitivity at %.2f" % bb, ev(GOLDEN5, value_variant(L, fit, beta=bb))))
    R["family"] = fam
    # readings that do part of a stump's work (the note's fork table): each keeps the golden's program
    R["partials"] = [("the assets' values held at 31 December while the lenders' terms move with the stress", ev(dict(GOLDEN5, refi="values_flat"))),
                     ("the successor's first close on its manager's date, unslipped, while the pending funds' own calls slip", ev(dict(GOLDEN5, closes_succ="expected"))),
                     ("the successor clause missed and the assets' values held at 31 December", ev(dict(GOLDEN5, refi="values_flat", succession="registered"))),
                     ("the lenders' terms of 31 December on the stressed values", ev(dict(GOLDEN5, refi="terms_flat"))),
                     ("the six managers' held companies as their files last show them", ev(dict(GOLDEN5, held="stale")))]
    # the factorial
    fac = {}
    for tag, sw in [("S1 dropped", dict(GOLDEN5, succession="registered")), ("S2 dropped", dict(GOLDEN5, refi="none")),
                    ("S1 alone", dict(REFLEX5, succession="clause")), ("S2 alone", dict(REFLEX5, refi="loans"))]:
        fac[tag] = ev(sw); fac[tag]["R1"] = g["R1"]
    R["factorial"] = fac
    # the bootstrap over funds
    rng = np.random.default_rng(5); fids = list(L["reg"]); bs = defaultdict(list)
    for b in range(boot):
        pick = rng.choice(len(fids), len(fids), replace=True)
        Lb = dict(L); Lb["reg"], Lb["st"], Lb["act"], Lb["aud"] = {}, {}, {}, {}
        Lb["loans"] = defaultdict(list)
        for j, i in enumerate(pick):
            fid = fids[i]; k = "%s#%d" % (fid, j)
            Lb["reg"][k] = dict(L["reg"][fid], **{"Fund ID": k}); Lb["st"][k] = L["st"].get(fid, {}); Lb["act"][k] = L["act"].get(fid, []); Lb["aud"][k] = L["aud"].get(fid, {})
            for (f0, co), v in L["loans"].items():
                if f0 == fid: Lb["loans"][(k, co)] = v
        Lb["cov"] = L["cov"]
        fb, _, _, _ = fit_all2(Lb)
        for name, keys in (("deployment", ("dep_0",)), ("the support's two channels", ("support",)),
                           ("first-close slips", ("slip",)), ("recycling", ("rho",)), ("the lenders' limit and the assets' values", ("lender", "value")),
                           ("every fitted input together", ("dep_0", "support", "slip", "fee", "rho", "lender", "value", "routine"))):
            f = dict(fit)
            for k in keys:
                if fb.get(k) is not None: f[k] = fb[k]
            o_ = ev(GOLDEN5, f); bs[name].append((float(o_["R5"]), o_["R7"]))
    R["boot"] = {k: [x[0] for x in v] for k, v in bs.items()}
    R["boot_programs"] = {k: [x[1] for x in v] for k, v in bs.items()}
    return R
