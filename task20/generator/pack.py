"""The data files of target/ for task20 architecture 4, written from the world's history to 31 December 2026."""
import csv
import datetime as dt
import math
import zlib
import os
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font
import world as Wd
import docs as DC
from world import qi, qy, qq, H_END, NQ

F_STMT = "capital_account_statements_2013Q1_2026Q4.csv"
F_CASH = "custodian_cash_activity_2026Q4.csv"
F_ACT = "manager_portfolio_activity_2013_2026.csv"
F_AUD = "fund_audited_financials_FY2013_FY2026.xlsx"
F_REG = "private_commitment_register_2026-12-31.xlsx"
F_BENCH = "industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv"
F_MKT = "market_series_quarterly_2000Q1_2026Q4.csv"

MGR_NAMES = {
    "BO1": "Ardley Square Partners", "BO2": "Thornwick Capital", "BO3": "Kelstone Equity", "BO4": "Marrable Partners",
    "BO5": "Oakhanger Capital", "BO6": "Pellworth Partners", "BO7": "Rudgely Equity", "BO8": "Sallowfield Capital",
    "GE1": "Brackley Growth", "GE2": "Tilsworth Growth Partners", "GE3": "Wendlebury Growth",
    "VC1": "Corvane Ventures", "VC2": "Lindhurst Ventures", "VC3": "Quarrendon Ventures", "VC4": "Yelden Venture Partners",
    "RE1": "Hambleden Real Estate", "RE2": "Nettlebed Property Partners", "RE3": "Ewelme Real Estate",
    "IN1": "Garsington Infrastructure", "IN2": "Shabbington Infrastructure", "IN3": "Waterperry Infrastructure",
    "PC1": "Harpsden Credit", "PC2": "Lewknor Credit Partners", "PC3": "Bix Direct Lending", "PC4": "Swyncombe Credit",
}
# the managers whose company-level reporting stopped after 2024 (the look-through feed covers the others; the property and
# infrastructure managers report asset by asset, loans included, through it to the end)
SUMMARY_ONLY = sorted(str(x) for x in np.random.default_rng(10).choice([g for g in ["BO1", "BO2", "BO3", "BO4", "BO5", "BO6", "BO7", "BO8", "GE1", "GE2", "GE3", "VC1", "VC2", "VC3", "VC4", "PC1", "PC2", "PC3", "PC4"]], 6, replace=False))
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
STRAT_NAME = {"BO": "Buyout", "GE": "Growth equity", "VC": "Venture capital", "RE": "Real estate", "IN": "Infrastructure", "PC": "Private credit"}

def qend(i):
    y, q = qy(i), qq(i)
    return dt.date(y, 3 * q, {3: 31, 6: 30, 9: 30, 12: 31}[3 * q])

def qmid(i, frac=0.5):
    a = qend(i - 1) + dt.timedelta(days=1); b = qend(i)
    return a + dt.timedelta(days=int((b - a).days * frac))

_ON = ["Bra", "Cor", "Dal", "Fen", "Gal", "Hal", "Jor", "Kel", "Lum", "Mar", "Nor", "Ost", "Pel", "Quen", "Ros", "Sel", "Tal",
       "Ver", "Wyn", "Zel", "Ard", "Bel", "Cal", "Dor", "Eld", "Fal", "Gry", "Hev", "Kav", "Lor", "Mav", "Nel", "Orv", "Pra", "Rul",
       "Sav", "Tem", "Ul", "Vel", "Wex"]
_END = ["exa", "ira", "ion", "ova", "ent", "ara", "ix", "ona", "ia", "eon", "ana", "ora", "ell", "yn", "eta", "ium", "ari", "ovo",
        "anta", "ido"]
_SECTOR = {"BO": ["Industries", "Packaging", "Foods", "Services", "Manufacturing", "Distribution", "Brands", "Components", "Group"],
           "GE": ["Software", "Health", "Payments", "Logistics", "Learning", "Systems", "Analytics", "Insurance Services"],
           "VC": ["Labs", "Bio", "Robotics", "Security", "Health", "AI", "Energy", "Therapeutics", "Networks"],
           "PC": ["Holdings", "Industries", "Services", "Software", "Healthcare", "Logistics", "Brands"]}
_PLACE = ["Linden", "Cedar", "Harbor", "Maple", "Willow", "Granite", "Summit", "Brook", "Hawthorn", "Aspen", "Juniper", "Sycamore",
          "Laurel", "Birch", "Copper", "Falcon", "Heron", "Prairie", "Mesa", "Canyon", "Bluff", "Sterling", "Quarry", "Orchard"]
_RE = ["Court Apartments", "Point Logistics Center", "Ridge Medical Office", "Self Storage", "Crossing Industrial Park",
       "Commons Shopping Center", "Plaza Office", "Park Life Science Campus", "Station Apartments"]
_IN = ["Solar", "Wind", "Water Utility", "Fiber", "Energy Storage", "Gas Storage", "Data Center", "Transit Parking", "Renewable Gas"]
_BEND = ["Hollow", "Creek", "Flats", "Bend", "Valley", "Mill", "Springs", "Fork"]
_NAMES = {}


def company_name(fid, st, dno):
    """the name a manager's report gives the company, property, asset or borrower behind one deal; one name each."""
    key = (fid, dno)
    if key in _NAMES:
        return _NAMES[key]
    used = set(_NAMES.values())
    k = 0
    while True:
        rng = np.random.default_rng(zlib.crc32(("%s-%d-%d" % (fid, dno, k)).encode()))
        if st == "RE":
            nm = "%s %s" % (_PLACE[rng.integers(len(_PLACE))], _RE[rng.integers(len(_RE))])
        elif st == "IN":
            nm = "%s %s %s" % (_PLACE[rng.integers(len(_PLACE))], _BEND[rng.integers(len(_BEND))], _IN[rng.integers(len(_IN))])
        else:
            brand = _ON[rng.integers(len(_ON))] + _END[rng.integers(len(_END))]
            nm = "%s %s" % (brand, _SECTOR[st][rng.integers(len(_SECTOR[st]))])
        if nm not in used:
            _NAMES[key] = nm
            return nm
        k += 1


def build_world():
    E, S, R = Wd.market()
    gps = Wd.managers()
    fs = Wd.commitments(gps, E)
    first_no = {}
    for f in fs:
        g = f["gp"]["id"]
        first_no.setdefault(g, int(np.random.default_rng(zlib.crc32(g.encode())).integers(2, 5)))
        f["no"] = first_no[g] + f["k"]
        f["id"] = "WX-%s-%03d" % (f["gp"]["st"], 100 + fs.index(f))
        nm = MGR_NAMES[f["gp"]["id"]]
        f["name"] = "%s %s" % (nm, ROMAN[f["no"] - 1])
    # the consultant's 2027 plan: the credit re-up at its own size, the equity and real-asset re-ups scaled to the rest
    plan = [f for f in fs if f["vint"] == 2027]
    eq = [f for f in plan if f["gp"]["st"] != "PC"]
    rest = Wd.P["plan_total"] - Wd.P["plan_pc"]
    tot = sum(f["C"] for f in eq)
    for f in plan:
        f["C"] = Wd.P["plan_pc"] if f["gp"]["st"] == "PC" else round(rest * f["C"] / tot / 5.0) * 5.0
    d = sum(f["C"] for f in eq) - rest
    eq[0]["C"] -= d
    for f in plan:
        f["size"] = round(f["C"] / f["share"])
    # each fund's successor: the same manager's next fund
    by_gp = {}
    for f in fs: by_gp.setdefault(f["gp"]["id"], []).append(f)
    for L_ in by_gp.values():
        L_.sort(key=lambda x: x["vint"])
        for a, b in zip(L_[:-1], L_[1:]): a["succ"] = b
    return dict(E=E, S=S, R=R, gps=gps, funds=fs)

def succ_fc(f, E=None):
    """the quarter f's successor holds its first close: as it happened by the end of 2026, otherwise its manager's date
    slipped on the market E (the stress for the forecast)."""
    s = f.get("succ")
    if s is None: return None
    if (s["fc"] <= H_END and s["vint"] <= 2026) or E is None: return s["fc"]
    return s["exp_fc"] + Wd.slip_of(s, E)

def history(Wo):
    E, S, R = Wo["E"], Wo["S"], Wo["R"]
    p = Wd.propensity(E)
    out = {}
    for f in Wo["funds"]:
        if f["vint"] > 2026 or f["fc"] > H_END:
            continue
        log = []; rec = {}
        o = Wd.run_fund(f, E, S, R, p, f["fc"], upto=H_END, rec=rec, deal_log=log, succ_fc=succ_fc(f))
        # fund-level contributions for the audited accounts
        out[f["id"]] = dict(o=o, log=log, rec=rec)
    return out

def w_csv(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)

def money(x): return "%.2f" % x

def write_all(Wo, H, tgt):
    E, S, R = Wo["E"], Wo["S"], Wo["R"]
    fs = Wo["funds"]
    byid = {f["id"]: f for f in fs}
    rng = np.random.default_rng(404)
    rows = {}
    # ---------------------------------------------------------------- capital account statements (USD, endowment share)
    late = sorted([fid for fid in H if byid[fid]["gp"]["st"] in ("BO", "VC", "RE")])[2::9][:3]   # Q4 statements not yet in
    restated = sorted(H)[5::31][:2]
    st_rows, cash_rows = [], []
    for fid in sorted(H):
        f = byid[fid]; o = H[fid]["o"]; C = f["C"]
        cum = 0.0
        name = f["name"]
        last = min(H_END, f["fc"] + Wd.ST[f["gp"]["st"]]["life"])
        for q in range(f["fc"], last + 1):
            ci, cf, other = o["call_inv"][q], o["call_fee"][q], o["call_exp"][q]
            dist = o["dist"][q]; inc = min(o["inc"][q], dist)
            # return of capital is the realised cost net of recycling; the rest of the proceeds is gain
            realised = [e for e in H[fid]["log"] if e[0] == "exit" and e[3] == q]
            cost_out = sum(e[4] for e in realised) * f["C"] / f["size"]
            proc_net = max(dist - inc, 0.0)
            roc = min(cost_out, proc_net); gain = proc_net - roc
            cum += (ci + cf + other) * 1e6
            final = q == f["fc"] + Wd.ST[f["gp"]["st"]]["life"]
            unf = 0.0 if final else C * 1e6 - cum
            nav = o["nav"][q] * 1e6
            disp = name
            if f["gp"]["id"] == "GE2" and q >= qi(2021, 3):
                disp = name.replace("Tilsworth Growth Partners", "Tilsworth Partners")
            row = [fid, disp, MGR_NAMES[f["gp"]["id"]] if not (f["gp"]["id"] == "GE2" and q >= qi(2021, 3)) else "Tilsworth Partners",
                   qend(q).isoformat(), (qend(q) + dt.timedelta(days=int(rng.integers(38, 71)))).isoformat(),
                   money((ci) * 1e6), money(cf * 1e6), money(other * 1e6), money(roc * 1e6), money(gain * 1e6), money(inc * 1e6),
                   money(nav), money(unf), "N", "final statement; commitment not called released" if final else ""]
            if q == H_END and fid in late:
                cash_rows += [[qmid(q, 0.3).isoformat(), fid, "capital call", money((ci + cf + other) * 1e6)]] if (ci + cf + other) > 0 else []
                cash_rows += [[qmid(q, 0.8).isoformat(), fid, "distribution", money(dist * 1e6)]] if dist > 0 else []
                continue
            if fid in restated and q == qi(2024, 2):
                old = list(row); old[11] = money(nav * 1.012); old[6] = money(cf * 1e6 * 1.08); old[13] = "N"; old[14] = "superseded"
                st_rows.append(old)
                row[13] = "Y"; row[4] = (qend(q) + dt.timedelta(days=118)).isoformat()
            st_rows.append(row)
            if q == H_END:
                if ci + cf + other > 0: cash_rows.append([qmid(q, 0.3).isoformat(), fid, "capital call", money((ci + cf + other) * 1e6)])
                if dist > 0: cash_rows.append([qmid(q, 0.8).isoformat(), fid, "distribution", money(dist * 1e6)])
    rows[F_STMT] = w_csv(os.path.join(tgt, F_STMT), ["fund_id", "fund_name", "manager", "period_end", "statement_date",
        "contributions_investments_usd", "contributions_management_fees_usd", "contributions_fund_expenses_usd",
        "distributions_return_of_capital_usd", "distributions_realized_gain_usd", "distributions_income_usd",
        "ending_nav_usd", "unfunded_commitment_usd", "restated", "note"], st_rows)
    cash_rows.sort()
    rows[F_CASH] = w_csv(os.path.join(tgt, F_CASH), ["value_date", "fund_id", "movement", "amount_usd"], cash_rows)
    # ---------------------------------------------------------------- managers' portfolio activity (fund level, USD m)
    act = []; seen_loan = set()
    for fid in sorted(H):
        f = byid[fid]
        nm = MGR_NAMES[f["gp"]["id"]]
        for e in H[fid]["log"]:
            kind, _, dno, q, a, b = e
            if f["gp"]["id"] in SUMMARY_ONLY and q > qi(2024, 4):
                continue          # these managers moved to quarterly letters in 2025: no company-level file since
            co = company_name(fid, f["gp"]["st"], dno)
            if kind == "new":
                act.append([fid, nm, co, qmid(q, 0.45).isoformat(), "initial investment", "%.3f" % a, ""])
            elif kind == "follow_on":
                act.append([fid, nm, co, qmid(q, 0.55).isoformat(), "follow-on investment", "%.3f" % a, ""])
            elif kind == "exit":
                act.append([fid, nm, co, qmid(q, 0.65).isoformat(), "realization", "%.3f" % b, "%.3f" % a, ""])
            elif kind == "val":
                act.append([fid, nm, co, qend(q).isoformat(), "valuation", "%.3f" % b, "%.3f" % a, ""])
            elif kind == "loan":
                first_loan = (fid, dno) not in seen_loan; seen_loan.add((fid, dno))
                act.append([fid, nm, co, qmid(q, 0.45 if first_loan else 0.5).isoformat(), "asset loan drawn" if first_loan else "asset loan refinanced",
                            "%.3f" % a, "", qend(b).isoformat()])
            elif kind == "refi_out":
                act.append([fid, nm, co, qmid(q, 0.5).isoformat(), "refinancing proceeds", "%.3f" % a, "", ""])
    act = [r_ if len(r_) == 8 else r_ + [""] for r_ in act]
    act.sort(key=lambda r: (r[0], r[3], r[2], r[4]))
    rows[F_ACT] = w_csv(os.path.join(tgt, F_ACT), ["fund_id", "manager", "portfolio_company", "date", "record_type",
        "amount_usd_m", "cost_basis_usd_m", "loan_maturity"], act)
    # ---------------------------------------------------------------- audited financials (fund level, USD thousands)
    wb = Workbook(); ws = wb.active; ws.title = "Audited accounts"
    ws.append(["Fund ID", "Fund", "Fiscal year end", "Total commitments (USD thousands)", "Investments at cost (USD thousands)",
               "Investments at fair value (USD thousands)", "Cash (USD thousands)", "Credit facility borrowings (USD thousands)",
               "Accrued liabilities (USD thousands)", "Partners' capital (USD thousands)", "Unfunded commitments (USD thousands)"])
    for c in ws[1]: c.font = Font(bold=True)
    aud_n = 0
    for fid in sorted(H):
        f = byid[fid]; rec = H[fid]["rec"]; o = H[fid]["o"]; sh = f["C"] / f["size"]
        june = f["gp"]["fy_june"]
        for y in range(qy(f["fc"]), 2027):
            qe = qi(y, 2) if june else qi(y, 4)
            if qe < f["fc"] or qe > H_END or qe > f["fc"] + Wd.ST[f["gp"]["st"]]["life"]: continue
            if not june and y == 2026: continue            # the 2026 accounts arrive in the spring
            fv = rec["fv"].get(qe, 0.0); line = rec["line"].get(qe, 0.0); cost = rec["cost"].get(qe, 0.0)
            contrib_f = (o["call_inv"][:qe + 1].sum() + o["call_fee"][:qe + 1].sum() + o["call_exp"][:qe + 1].sum()) / sh
            cash = 0.004 * f["size"]
            accr = o["call_fee"][qe] / sh * 0.33
            pc = fv + cash - line - accr
            ws.append([fid, f["name"], qend(qe), round(f["size"] * 1000), round(cost * 1000), round(fv * 1000), round(cash * 1000),
                       round(line * 1000), round(accr * 1000), round(pc * 1000), round((f["size"] - contrib_f) * 1000)])
            aud_n += 1
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        for c in row: c.number_format = "yyyy-mm-dd"
    wb.save(os.path.join(tgt, F_AUD)); rows[F_AUD] = aud_n
    # ---------------------------------------------------------------- the commitment register
    wb = Workbook(); ws = wb.active; ws.title = "Register"
    ws.append(["Fund ID", "Fund", "Manager", "Strategy", "Vintage", "Commitment (USD m)", "Fund size (USD m)", "Commitment date",
               "First close expected at commitment", "First close", "Investment period (years, per agreement)", "Investment period ends",
               "Term ends", "Status"])
    for c in ws[1]: c.font = Font(bold=True)
    reg_n = 0
    for f in sorted(fs, key=lambda x: x["id"]):
        if f["vint"] > 2026: continue
        st = Wd.ST[f["gp"]["st"]]
        closed = f["fc"] <= H_END
        status = "pending first close" if not closed else ("investing" if H_END < f["fc"] + st["ip"] else
                                                           ("harvesting" if H_END < f["fc"] + st["life"] else "liquidated"))
        ip_end = H[f["id"]]["o"]["ip_end"] if (closed and f["id"] in H) else (f["fc"] + st["ip"])
        ws.append([f["id"], f["name"], MGR_NAMES[f["gp"]["id"]], STRAT_NAME[f["gp"]["st"]], f["vint"], f["C"],
                   f["size"] if closed else None, qmid(f["commit_q"], 0.5), qend(f["exp_fc"]), qend(f["fc"]) if closed else None,
                   st["ip"] // 4 if closed else None, qend(ip_end - 1) if closed else None, qend(f["fc"] + st["life"]) if closed else None, status])
        reg_n += 1
    for row in ws.iter_rows(min_row=2, min_col=8, max_col=13):
        for c in row:
            if c.column != 11: c.number_format = "yyyy-mm-dd"
    wb.save(os.path.join(tgt, F_REG)); rows[F_REG] = reg_n
    # ---------------------------------------------------------------- the industry benchmark (per cent of commitment)
    bench = Wd.benchmark_funds(Wo["gps"])
    p = Wd.propensity(E)
    br = []
    last = qi(2026, 2)
    for b in bench:
        o = Wd.run_fund(b, E, S, R, p, b["fc"], upto=last)
        for q in range(b["fc"], min(last, b["fc"] + Wd.ST[b["gp"]["st"]]["life"]) + 1):
            c = o["call_inv"][q] + o["call_fee"][q] + o["call_exp"][q]; d = o["dist"][q]; n = o["nav"][q]
            if c == 0 and d == 0 and n == 0: continue
            br.append([b["id"], STRAT_NAME[b["gp"]["st"]], b["vint"], qend(q).isoformat(), "%.4f" % c, "%.4f" % d, "%.4f" % n])
    rows[F_BENCH] = w_csv(os.path.join(tgt, F_BENCH), ["benchmark_fund", "strategy", "vintage", "period_end",
        "contributions_pct_of_commitment", "distributions_pct_of_commitment", "nav_pct_of_commitment"], br)
    # ---------------------------------------------------------------- market series
    mk = []
    for q in range(0, H_END + 1):
        mk.append([qend(q).isoformat(), "%.2f" % E[q], "%.2f" % S[q], "%.3f" % R[q], "%.3f" % (R[q] * 0.55 + 2.1 + 0.3 * math.sin(q / 5.0))])
    rows[F_MKT] = w_csv(os.path.join(tgt, F_MKT), ["quarter_end", "exit_activity_index_2015_100", "public_equity_total_return_index",
        "short_rate_pct", "treasury_10y_yield_pct"], mk)
    # ---------------------------------------------------------------- the holdings, spending, plan and survey
    DC.holdings(os.path.join(tgt, DC.F_LIQ)); rows[DC.F_LIQ] = len(DC.HOLDINGS)
    rows[DC.F_SPEND] = DC.spending(os.path.join(tgt, DC.F_SPEND))
    plan = [f for f in fs if f["vint"] == 2027]
    DC.pacing_plan(os.path.join(tgt, DC.F_PLAN), plan, MGR_NAMES); rows[DC.F_PLAN] = len(plan)
    DC.peers(os.path.join(tgt, DC.F_PEER), np.random.default_rng(909)); rows[DC.F_PEER] = 24
    return rows
