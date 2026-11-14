"""Generator assertions for task20 architecture 6: the processes the golden reads off the evidence are the world's own,
the bases policy section 8 files are in the shipped policy and executed as written, every rival fit and every reading
one step from a filed basis gives the golden program with room on both sides, every shortcut gives another, the stump
factorial holds, and the figures add up across the deliverables."""
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import figures as FG  # noqa: E402
import pack as PK  # noqa: E402
import truth as T  # noqa: E402
import world as Wd  # noqa: E402

TGT = os.path.join(TASK, "target")
fails = []


def check(name, ok, detail=""):
    print("%-4s %-78s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)


def pdf_text(path):
    """the shipped PDF's text, whitespace collapsed (the reader every check of the policy goes through)."""
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join((p.extract_text() or "") for p in PdfReader(path).pages)).replace("’", "'")


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    R = A.full(TGT)
    g = R["golden"]; L = R["L"]; P = Wd.P; fit = R["fit"]; mkt = R["mkt"]; stock = R["stock"]
    ev = lambda sw, f=None, stk=None: A.evaluate(L, sw, f or fit, mkt, stk or stock)
    gold = g["R7"]; reg = L["reg"]
    lo, hi = FG.window(g)
    # ------------------------------------------------------------ the world's processes the golden reads off the evidence
    Wo = PK.build_world(); H = PK.history(Wo)
    Wf = {f["id"]: f for f in Wo["funds"]}
    tw = sum(H[f]["o"]["line"][Wd.H_END] for f in H if f in reg and reg[f]["Status"] != "liquidated")
    check("the facility balances within 3 per cent of the world's", abs(F["line_stock_usd_m"] / tw - 1) < 0.03, "%.1f against %.1f" % (F["line_stock_usd_m"], tw))
    check("the latest audited borrowings fall well short of the balances at 31 December (under half; the facilities were drawn again in 2026)",
          F["line_stock_audited_usd_m"] < 0.5 * F["line_stock_usd_m"], "%.1f against %.1f" % (F["line_stock_audited_usd_m"], F["line_stock_usd_m"]))
    mgr_gp = {reg[fid]["Manager"]: Wf[fid]["gp"] for fid in reg if fid in Wf}
    wrong = [m for m, v in R["clause"].items() if v[0] is not None and v[0] != mgr_gp[m]["succ_clause"]]
    check("S1 the clause read off each manager's past successions is its own", not wrong and sum(v[0] is not None for v in R["clause"].values()) >= 15,
          "%d managers read, %s" % (sum(v[0] is not None for v in R["clause"].values()), "; ".join(wrong) or "none wrong"))
    check("S1 every manager's past successions agree with each other (the clause is all or none)", all(v[1][0] in (0, v[1][1]) for v in R["clause"].values() if v[1]),
          "; ".join("%s %d/%d" % (m, v[1][0], v[1][1]) for m, v in sorted(R["clause"].items()) if v[1] and v[1][0] not in (0, v[1][1])) or "%d successions" % F["past_successions"])
    wev = set()
    for fid, r in reg.items():
        f = Wf.get(fid)
        if f is None or r["Status"] != "investing" or not f["gp"]["succ_clause"] or f.get("succ") is None: continue
        s = f["succ"]
        if s["fc"] <= Wd.H_END and s["vint"] <= 2026: continue
        sq = s["exp_fc"]; ie = A._qd(r["Investment period ends"])          # section 8: the manager's date
        if sq <= ie and A.W[0] <= sq <= A.W[-1]: wev.add(r["Fund"])
    gev = set(F["successor_funds"])
    check("S1 the funds whose successors close inside the stress are the world's", gev == wev and len(gev) >= 5, "golden %s; world %s" % (sorted(gev), sorted(wev)))
    unread = [r["Fund"] for fid, r in reg.items() if r["Fund"] in wev and R["clause"].get(r["Manager"], (None,))[0] is None]
    check("S1 no manager without a past succession has a successor closing inside the stress", not unread, "; ".join(unread) or "none")
    kinds = {fit["succ"][e["fid"]][0] for e in R["successor_events"]}
    check("S1 the successors are found in two places: funds awaiting a first close in the register, and the plan's re-ups", kinds == {"reg", "plan"}, str(sorted(kinds)))
    n_early = sum(1 for fid, r in reg.items() if r["First close"] and r["Investment period (years, per agreement)"]
                  and A._qd(r["Investment period ends"]) + 1 < A._qd(r["First close"]) + 4 * int(r["Investment period (years, per agreement)"]))
    n_late = sum(1 for fid, r in reg.items() if r["First close"] and r["Investment period (years, per agreement)"]
                 and A._qd(r["Investment period ends"]) + 1 > A._qd(r["First close"]) + 4 * int(r["Investment period (years, per agreement)"]))
    check("the register's periods end both sooner and later than agreed across the record (not only in the deciding funds)", n_early >= 20 and n_late >= 4,
          "%d ended sooner, %d later" % (n_early, n_late))
    lr, vr = fit["lender"], fit["value"]
    check("S2 the lenders' cap since mid-2022 within 0.02 of the world's", abs(lr["cap_post"] - P["ltv_post"]) <= 0.02, "%.3f against %.2f" % (lr["cap_post"], P["ltv_post"]))
    r26 = float(L["R"][A.H_END]); rates = [r26, r26 + Wd.P["stress_rate_up"]]
    fl = lambda r: min(lr["cap_post"], lr["kappa"] / (r + lr["spread"])); wl = lambda r: min(P["ltv_post"], P["refi_kappa"] / (r + P["refi_spread"]))
    check("S2 the fitted lenders' limit within 0.02 of the world's at 31 December's rate and at the stressed rate",
          all(abs(fl(r) - wl(r)) <= 0.02 for r in rates), "; ".join("%.2f%%: %.3f against %.3f" % (r, fl(r), wl(r)) for r in rates))
    seen = [p for p in lr["pts"] if p[0] >= A.qi(2022, 3) and abs(p[1] - rates[1]) < 0.35]
    check("S2 the stressed rate lies inside the record: refinancings granted within 0.35 points of it", len(seen) >= 4,
          "%d refinancings at %.2f to %.2f percent, granted %.3f to %.3f of value" % (len(seen), min(p[1] for p in seen), max(p[1] for p in seen),
                                                                                    min(p[2] for p in seen), max(p[2] for p in seen)) if seen else "none")
    check("S2 the assets' equity sensitivity within 0.1 of the world's", abs(vr["beta"] - P["beta_p"]) <= 0.1, "%.3f against %.2f" % (vr["beta"], P["beta_p"]))
    check("S2 the assets' rate sensitivity within 0.006 of the world's", abs(vr["c"] - P["cap1"] / P["cap0"]) <= 0.006, "%.3f against %.4f" % (vr["c"], P["cap1"] / P["cap0"]))
    asl = A.asset_loans(L); short = [(k, rf) for k, x in asl.items() for rf in x["refis"] if rf["new"] < rf["old"] - 1e-6]
    paired = 0
    for (fid, co), rf in short:
        fo = sum(a for q, t, c2, a, cb in L["act"][fid] if c2 == co and t == "follow-on investment" and q == rf["q"])
        paired += abs(fo - (rf["old"] - rf["new"])) < 0.01
    check("S2 the record holds refinancings at a lower balance, the fund investing the difference the same quarter", len(short) >= 2 and paired == len(short),
          "%d of %d refinancings, %d matched by a follow-on of the shortfall" % (len(short), F["refinancings_in_record"], paired))
    tr, tplan = T.truth()
    wref = float(tr["refi"][A.W].sum())
    check("S2 the refinancing calls within 20 per cent of the world's under the stress", abs(F["refinancing_calls_total_usd_m"] / wref - 1) < 0.20,
          "golden %.1f world %.1f" % (F["refinancing_calls_total_usd_m"], wref))
    terms = sorted({x["maturity"] - min(q for q, t, a, m in L["loans"][k] if t == "asset loan drawn") for k, x in asl.items() if x["maturity"] is not None and not x["refis"]})
    check("the loans' terms vary loan by loan (no one constant term)", len(terms) >= 6, "%d distinct terms, %d to %d quarters" % (len(terms), terms[0], terms[-1]))
    due_funds = {x["fund"] for x in F["loans_due"]}; due_mgrs = {reg[x["fid"]]["Manager"] for x in F["loans_due"]}
    alive = sum(1 for k, x in asl.items() if x["maturity"] is not None and x["maturity"] > A.H_END and k not in A._equity_vals(L)[1])
    check("S2 the loans falling due sit across funds and managers, a minority of the loans alive", len(due_funds) >= 6 and len(due_mgrs) >= 4 and F["loans_due_count"] < 0.5 * alive,
          "%d loans of %d alive, %d funds, %d managers" % (F["loans_due_count"], alive, len(due_funds), len(due_mgrs)))
    ex = fit["ext"]
    check("investment-period extensions: the length is the world's and the rule classes 85 per cent of the agreed ends or more",
          ex["length"] == P["ext_q"] and ex["accuracy"] >= 0.85, str({k: (round(v, 3) if isinstance(v, float) else v) for k, v in ex.items()}))
    check("each re-up's calls within 20 per cent of the world's", all(abs(F["re_up_calls_usd_m"][k] / v - 1) < 0.20 for k, v in tplan.items()),
          "; ".join("%s %.1f/%.1f" % (k.split()[0], F["re_up_calls_usd_m"][k], v) for k, v in tplan.items()))
    # ------------------------------------------------------------ the bases section 8 files, read from the shipped policy
    pol = pdf_text(os.path.join(TGT, DC.F_POLICY))
    check("the policy reads back (positive control: its title and the test of section 5)", "Liquidity policy for private-fund commitments" in pol
          and "is at least the minimum reserve the Investment Committee sets each year" in pol and len(pol) > 4000, "%d characters" % len(pol))
    filed = {
        "the minimum reserve": "For the 2027 budget the minimum reserve is USD %s million" % format(int(DC.CUSHION), ","),
        "the cap at the commitment (section 3)": "no fund is taken to call more than the part of its commitment it has not yet called",
        "the pace's numerator and denominator": "their investments in companies and assets, first and follow-on, in the quarter over their commitments not yet invested at the start of it, each summed and each at the endowment's share of the fund",
        "what a commitment not yet invested is": "A commitment not yet invested is the commitment less the endowment's share of the investments the fund has made",
        "the pace's grouping and sample": "in the same year since first close: over the quarters those funds spent in their investment periods in that year",
        "no allowance for the exit market or reinvested proceeds": "No allowance is made, up or down, for the state of the exit market, and none for proceeds a manager keeps back to reinvest",
        "first closes on the managers' dates": "A fund that has not held its first close is taken to hold it in the quarter its manager has given",
        "the benchmark funds past their periods": "with a vintage year six or more years before the year of that quarter",
        "the benchmark rate's basis": "over those funds' value at the end of the previous quarter, each summed over those funds",
        "the rate taken whole": "The rate is taken whole, with nothing taken off for the calls such funds make in ordinary markets",
        "what the rate stands for": "stands for the fund's fees and expenses and for the follow-on and rescue financings of the companies it holds",
        "the facility balances in the first quarter": "counts as called in the first quarter of the stress, at its balance at 31 December",
        "how the facility balance is formed": "The balance is taken as the borrowings on the fund's latest audited balance sheet, plus the investments the fund has made since the date of that balance sheet and less the capital it has called for investments since, at the endowment's share of the fund and never less than nil",
        "the facility balance of a fund with no audit": "a fund with no audited balance sheet is counted in the same way from its first investment",
        "the custodian's calls in the facility balance": "the calls the custodian recorded in the quarter are taken as called for investments",
        "no proceeds reinvested since the audit": "No allowance is made for proceeds reinvested since the balance sheet",
        "fees and expenses at the latest statement": "A fund calls in each quarter the management fee and the fund expenses of its latest quarterly statement, except a buyout, growth equity or venture fund past its investment period, whose fees and expenses are within the rate above",
        "fees and expenses of a fund yet to close": "the fee and the expenses of the median quarter, each as a share of commitment, among the quarters the endowment's funds of its strategy have spent in their investment periods after the quarter of first close",
        "every call counts, judged on the evidence": "Capital calls are all those the endowment's managers can be expected to make in the stress, judged on the evidence the Office of Investments holds",
        "values move with the stress (section 6)": "values move with these paths through the stress",
    }
    for k, sent in filed.items():
        check("policy files %s" % k, sent in pol, sent[:80])
    silent = ["successor", "refinanc", "loan", "matur", "extend", "lender"]
    check("the policy says nothing of what ends an investment period or of the assets' loans", not any(w in pol.lower() for w in silent),
          ", ".join(w for w in silent if w in pol.lower()) or "none of: " + ", ".join(silent))
    check("the analysis reads the policy's minimum, factors and vintage rule", DC.CUSHION == A.CUSHION and all(DC.FACTORS[k] == v for k, v in A.FACTORS.items())
          and A.OLD_YEARS == 6)
    # ------------------------------------------------------------ forcing: the family, the one-step readings, the shortcuts
    fam = E["forcing"]["golden_family"]; pert = E["forcing"]["perturbations"]
    check("R7 every golden-family method gives the golden program", all(x["answer"] == gold for x in fam) and len(fam) >= 10, ", ".join(x["answer"] for x in fam))
    check("every bootstrap percentile gives the golden program", all(x["answer"] == gold for x in pert if "bootstrap" in x["input"]))
    check("each estimated input moved by a fifth, and the filed pace by a twentieth, gives the golden program", all(o["R7"] == gold for n, o in R["perturb"]) and len(R["perturb"]) >= 8,
          "; ".join("%.1f" % o["R5"] for n, o in R["perturb"]))
    check("every reading one step from a basis section 8 files gives the golden program", all(o["R7"] == gold for n, o in R["readings"]) and len(R["readings"]) >= 6,
          "; ".join("%.1f" % o["R5"] for n, o in R["readings"]))
    aud = []
    for y in (4, 5, 6):
        for kind in ("gross", "excess"):
            cr = A.bench_rates(L, "calls", years=y) if kind == "gross" else A.old_rate_excess(L, years=y)
            o = ev(A.GOLDEN, A.with_(fit, crate=cr)); aud.append((y, kind, o["R5"], o["R7"]))
    check("the benchmark's funds 5 or 6 years past their vintage, the rate whole or net of the eight quarters before the window, all give the golden program "
          "(a rule two years younger than the filed one, taken whole, does not, and is recorded)",
          all(a[3] == gold for a in aud if a[0] >= 5), "; ".join("%d %s %.1f %s" % a for a in aud))
    check("the policy does not confine investments to the investment period (a loan's shortfall is invested after it)", "only during its investment period" not in pol)
    check("the policy closes on no stand-alone sentence pointing at calls it does not list (the stage 4 reader took one as a signpost to the loans)",
          "Any other call" not in pol and "any other call" not in pol)
    check("the readings a filed sentence rules out land on another program", all(o["R7"] != gold for n, o in R["ruled_out"]),
          "; ".join("%.1f %s" % (o["R5"], o["R7"]) for n, o in R["ruled_out"]))
    check("every shortcut gives another program", all(x["answer"] != gold for x in E["forcing"]["shortcuts"]),
          ", ".join(x["answer"] for x in E["forcing"]["shortcuts"]))
    B = FG.bands(R)
    for rid, k in FG.GRADED:
        offs = [n for n, o in R["family"] if not FG.inband(B[k], o[k])]
        check("R7 every golden-family method inside %s's bands" % rid, not offs, "; ".join(offs))
    car = R["passes"]["careful"]
    check("R3 the careful route lands outside the bands of the successor closes, the refinancing calls, the calls by half and the headroom",
          not any(FG.inband(B[k], car[k]) for rid, k in FG.GRADED), "headroom %.1f against %s" % (car["R5"], B["R5"]))
    cells = [h for h in A.HALVES if B["calls"][h][0] <= car["calls"][h] <= B["calls"][h][1]]
    far = [h for h in A.HALVES if min(abs(car["calls"][h] - B["calls"][h][0]), abs(car["calls"][h] - B["calls"][h][1])) >= 25 and h not in cells]
    check("the careful route files at least one half-year cell 25 or more outside its band (where the two judgments cancel it lands inside)",
          len(far) >= 1 and len(cells) <= 2, "inside %s; far outside %s" % (cells or "none", far))
    check("the careful route files none of the successor closes and none of the loans", car["succ"]["funds"] == 0 and car["refi_res"]["loans_due"] == 0)
    check("the headroom band sits inside the golden program's window with 40 or more on each side", lo + 40 <= B["R5"][0] and B["R5"][1] + 40 <= hi,
          "%s inside [%.1f, %.1f): %.1f below, %.1f above" % (B["R5"], lo, hi, B["R5"][0] - lo, hi - B["R5"][1]))
    check("the bootstrap's 5th to 95th percentiles sit inside the headroom band", all(B["R5"][0] <= v[0] and v[1] <= B["R5"][1] for v in F["bootstrap_p5_p95"].values()),
          str(F["bootstrap_p5_p95"]))
    ml, mh = F["margin_below_usd_m"], F["margin_above_usd_m"]
    famv = [o["R5"] for n, o in R["family"]]
    check("the program's margins: 60 or more below and above the headroom", ml >= 60 and mh >= 60, "%.1f below, %.1f above" % (ml, mh))
    check("the family's spread sits well inside each margin (half of it or less)", g["R5"] - min(famv) <= 0.5 * ml and max(famv) - g["R5"] <= 0.5 * mh,
          "family %.1f to %.1f around %.1f" % (min(famv), max(famv), g["R5"]))
    # ------------------------------------------------------------ the stump factorial and the open members
    fac = R["factorial"]
    w1, w2 = g["R5"] - fac["S1 dropped"]["R5"], fac["S2 dropped"]["R5"] - g["R5"]
    check("each stump dropped alone moves the program", all(fac[k]["R7"] != gold for k in ("S1 dropped", "S2 dropped")),
          ", ".join("%s %s" % (k, fac[k]["R7"]) for k in fac))
    check("the two single drops land on different programs", fac["S1 dropped"]["R7"] != fac["S2 dropped"]["R7"])
    check("no stump fixed alone on the careful route reaches the golden program", all(fac[k]["R7"] != gold for k in ("S1 alone", "S2 alone")))
    check("the careful route misses the call", car["R7"] != gold, car["R7"])
    check("each margin sits between the family's spread and its stump's worth, 20 or more clear of the stump", w1 - ml >= 20 and w2 - mh >= 20,
          "S1 worth %.1f against %.1f below; S2 worth %.1f against %.1f above" % (w1, ml, w2, mh))
    check("the careful route clears the upper line by 20 or more (the two stumps do not cancel)", car["R5"] - hi >= 20, "%.1f against %.1f" % (car["R5"], hi))
    progs = {p["code"]: set(next(x for x in L["programs"] if x["code"] == p["code"])["funds"]) for p in g["programs"]}
    open_s2 = progs[car["R7"]] - progs[gold]; open_s1 = progs[gold] - progs.get(fac["S1 dropped"]["R7"], set())
    check("open members: the careful route wrongly commits re-ups S2 takes out, and without S1 re-ups of the golden program drop out",
          len(open_s2) >= 1 and len(open_s1) >= 1 and not (open_s1 & open_s2), "S2 opens %s; S1 opens %s" % (sorted(open_s2), sorted(open_s1)))
    for h in E["hints"]:
        check("R6 the hint rescues a third of the results or fewer", len(h["rescues"]) <= 2, "%s: %s" % (h["sentence"][:60], h["rescues"]))
    check("the successor closes' effect is one figure: the calls taken off are the headroom the registered ends would cost",
          abs(F["successor_effect_usd_m"] - (g["R5"] - fac["S1 dropped"]["R5"])) < 0.051 and len(R["successor_events"]) == g["succ"]["funds"],
          "%.1f against %.1f" % (F["successor_effect_usd_m"], g["R5"] - fac["S1 dropped"]["R5"]))
    check("the refinancing calls are one figure: the halves add to the total, the loans' balance is the sheet's", abs(sum(g["refi"].values()) - F["refinancing_calls_total_usd_m"]) < 0.051
          and abs(sum(x["D"] for x in F["loans_due"]) - F["loans_due_balance_usd_m"]) < 0.051 and len(F["loans_due"]) == g["refi_res"]["loans_due"])
    # ------------------------------------------------------------ arithmetic across the deliverables
    calls = sum(g["R2"].values()) + sum(g["R3"].values())
    check("calls by half split into closed and pending funds", all(abs(({**g["R2"], **g["R3"]})[h] - g["closed"][h] - g["pending"][h]) < 0.11 for h in A.HALVES))
    comp = {h: g["new"][h] + g["fees"][h] + g["old"][h] + g["refi"][h] + (g["stock"] if h == A.HALVES[0] else 0.0) for h in A.HALVES}
    check("calls by half are the facility balances, new investments, fees, the funds past their periods and the refinancing calls",
          all(abs(comp[h] - ({**g["R2"], **g["R3"]})[h]) < 0.26 for h in A.HALVES), str({h: round(v, 1) for h, v in comp.items()}))
    check("net cash needs are spending plus calls less distributions",
          abs(F["spending_24m_usd_m"] + calls - sum(g["R4"].values()) - F["net_needs_before_2027_usd_m"]) < 0.21)
    check("headroom is the reserve less the needs less the minimum",
          abs(F["reserve_usd_m"] - F["net_needs_before_2027_usd_m"] - F["minimum_reserve_usd_m"] - F["headroom_before_2027_usd_m"]) < 0.11)
    check("each program's calls are its re-ups' calls", all(abs(F["programs"][pr["code"]]["calls_usd_m"] - sum(F["re_up_calls_usd_m"][f] for f in pr["funds"])) < 0.11
                                                              for pr in L["programs"]))
    check("each program's headroom left is the headroom less its calls", all(
        abs(F["programs"][c]["headroom_usd_m"] - (F["headroom_before_2027_usd_m"] - v["calls_usd_m"])) < 0.11 for c, v in F["programs"].items()))
    check("the adopted program is the largest that passes", F["program"] == max((c for c, v in F["programs"].items() if v["passes"]),
                                                                                     key=lambda c: F["programs"][c]["total_usd_m"]))
    check("the unfunded total is the strategies' sum", abs(sum(F["unfunded_by_strategy_usd_m"].values()) - F["unfunded_total_usd_m"]) < 0.11)
    plan_by = {p["st"]: p["fund"] for p in L["plan"]}
    check("the plan's programs as read are the plan's as written", [(pr["code"], pr["funds"]) for pr in L["programs"]] ==
          [(c, [plan_by[s] for s in sts if s in plan_by]) for c, _, sts in DC.PROGRAMS])
    # ------------------------------------------------------------ the semantic forks (DESIGN_NOTE.md, Semantic fork table)
    live = [f for f, r in reg.items() if r["Status"] not in ("liquidated", "pending first close")]
    col = sum(L["st"][f][max(q for q in L["st"][f] if "unfunded_commitment_usd" in L["st"][f][q])]["unfunded_commitment_usd"] for f in live
              if any("unfunded_commitment_usd" in v for v in L["st"][f].values()))
    cash_late = sum(v.get("contributions_investments_usd", 0.0) for f in live for q, v in L["st"][f].items() if v.get("cash_only"))
    paid = sum(float(reg[f]["Commitment (USD m)"]) - sum(v["contributions_investments_usd"] + v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"]
               for v in L["st"][f].values()) for f in live)
    check("SF1 commitment less contributions equals the statements' unfunded once the custodian's cash is in", abs(paid - (col - cash_late)) < 0.05,
          "%.2f against %.2f" % (paid, col - cash_late))
    released = [f for f, r in reg.items() if r["Status"] == "liquidated"]
    check("SF1 every released commitment's final statement shows nothing unfunded", all(
        L["st"][f][max(q for q in L["st"][f] if "unfunded_commitment_usd" in L["st"][f][q])]["unfunded_commitment_usd"] == 0.0 for f in released))
    check("SF2 funds with a first close are every status but pending", {reg[f]["Status"] for f in live} == {"investing", "harvesting"})
    fees = sum(v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"] for f in live for v in L["st"][f].values())
    check("SF3 fees and expenses are called as contributions (the unfunded falls by them)", fees > 0, "%.1f called as fees and expenses" % fees)
    check("SF4 the spending is eight quarters of one quarter of FY2027's distribution", R["spending24"] == 2.0 * L["spend"][2027])
    mv = sum(float(h["Market value 31 Dec 2026 (USD m)"]) for h in L["hold"] if h["Policy liquidity class"])
    check("SF5 the reserve at the policy's factors, not market value", abs(R["reserve"] - A.reserve(L)) < 0.01 and R["reserve"] < mv)
    states = [A.fund_state(L, fid, stock) for fid in reg]
    late = [x for x in states if not x["pending"] and not x["liquidated"] and L["st"].get(x["fid"], {}).get(A.H_END, {}).get("cash_only")]
    check("SF6 the late statements' value is 30 September plus the fourth quarter's cash", len(late) > 0 and all(
        abs(x["nav"] - (L["st"][x["fid"]][A.H_END - 1]["ending_nav_usd"] + L["st"][x["fid"]][A.H_END]["contributions_investments_usd"]
                        - L["st"][x["fid"]][A.H_END]["distributions_return_of_capital_usd"])) < 1e-9 for x in late), "%d funds" % len(late))
    check("SF7 the distribution rate is the sum of distributions over the sum of values", all(0.0 <= v < 0.2 for v in fit["drate"].values()))
    e = mkt[0]
    check("SF8 the stress index is 2026Q4's level times 2008's path relative to 2008Q2",
          all(abs(e[A.W[k]] - L["E"][A.H_END] * L["E"][A.qi(2008, 3) + k] / L["E"][A.qi(2008, 2)]) < 1e-9 for k in range(8)))
    check("SF9 each program is its re-ups at their proposed sizes", all(abs(pr["total"] - sum(p["C"] for p in L["plan"] if p["fund"] in pr["funds"])) < 1e-9
                                                                          for pr in L["programs"]))
    order = sorted(F["programs"], key=lambda c: -F["programs"][c]["total_usd_m"]); i = order.index(F["program"])
    check("SF10 the program adopted is the largest total that passes, and the next larger fails", i > 0 and not F["programs"][order[i - 1]]["passes"])
    check("SF11 the headroom is net of the minimum reserve", abs(F["reserve_usd_m"] - F["net_needs_before_2027_usd_m"] - F["headroom_before_2027_usd_m"] - F["minimum_reserve_usd_m"]) < 0.11)
    check("SF12 the halves are calendar halves of 2027 and 2028", A.W[0] == A.qi(2027, 1) and A.W[-1] == A.qi(2028, 4))
    pend = [f for f, r in reg.items() if r["Status"] == "pending first close"]
    q1 = float(A.project(L, states, [], A.GOLDEN, fit, mkt)["stock"][A.W[0]])
    check("SF13 the facility balances count in the first quarter of the stress (policy section 8)", abs(q1 - g["stock"]) < 0.06 and
          "counts as called in the first quarter of the stress" in pol, "%.1f of %.1f in the first quarter" % (q1, g["stock"]))
    check("SF14 the benchmark rate stands for the fund's fees and expenses (policy section 8); added on top, the call stands",
          {n: o for n, o in R["readings"]}["the funds' own fees and expenses added on top of section 8's benchmark rate"]["R7"] == gold,
          "%.1f" % {n: o for n, o in R["readings"]}["the funds' own fees and expenses added on top of section 8's benchmark rate"]["R5"])
    check("SF21 no allowance, up or down, for the state of the exit market (policy section 8)", "No allowance is made, up or down, for the state of the exit market" in pol)
    check("SF15 the pending funds count in full among the commitments not yet called", abs(sum(float(reg[f]["Commitment (USD m)"]) for f in pend)
                                                                                            - sum(p["C"] for p in R["pending"])) < 1e-9 and len(pend) == len(R["pending"]))
    check("SF16 the headroom before any 2027 commitment carries no re-up", abs(F["headroom_before_2027_usd_m"] - g["R5"]) < 1e-9)
    check("SF17 the calls of the commitments made by the end of 2026 include the pending funds'", sum(g["pending"].values()) > 0)
    ended = [x for x in states if not x["pending"] and not x["liquidated"] and x["term"] is not None and x["term"] in A.W[:-1]]
    late_calls = 0.0
    for x in ended:
        o_ = A.project(L, [x], [], A.GOLDEN, fit, mkt)
        late_calls += sum(float(o_["call_inv"][q]) for q in A.W if q > x["term"])
    check("SF18 a fund whose term ends inside the stress calls nothing after it", len(ended) > 0 and late_calls == 0.0, "%d funds" % len(ended))
    plan_funds = {p["fund"] for p in L["plan"]}
    check("SF19 the successors' first closes are their managers' whether or not Wexmoor commits (re-ups among them)",
          any(e_["successor"] in plan_funds for e_ in R["successor_events"]), "; ".join("%s to %s" % (e_["fund"], e_["successor"]) for e_ in R["successor_events"]))
    rt = {n: o for n, o in R["routes"]}
    vf = rt["the loans refinanced at the stressed rate on the values of 31 December 2026"]
    check("SF20 values move with the stress outside sections 4 and 7 (policy section 6); held at 31 December the loans land on another program",
          vf["R7"] != gold, "%.1f %s" % (vf["R5"], vf["R7"]))
    lf = [o for n, o in R["family"] if n.startswith("the lenders' limit")]
    check("SF22 the lenders' limit fitted since mid-2022 or since 2020, or read straight off the refinancings near the stressed rate (same call)",
          len(lf) == 2 and all(o["R7"] == gold for o in lf), "; ".join("%.1f" % o["R5"] for o in lf))
    fm_ = {n: o for n, o in R["family"]}
    so = fm_["a maturing loan's shortfall met before the fund's other calls within the commitment it has left"]
    check("SF42 the order a fund's calls meet the commitment it has left, the shortfall last or first (same call, the headroom within 2)",
          so["R7"] == gold and abs(so["R5"] - g["R5"]) <= 2.0,
          "%.1f against %.1f; refinancing called %.1f against %.1f" % (so["R5"], g["R5"], so["refi_res"]["calls_usd_m"], g["refi_res"]["calls_usd_m"]))
    va = fm_["the assets' value response fitted on every quarter of every asset, the first four years included"]
    check("SF43 the assets' value response on the assets past their plans or on every valuation (same call, the headroom within 5)",
          va["R7"] == gold and abs(va["R5"] - g["R5"]) <= 5.0, "%.1f against %.1f" % (va["R5"], g["R5"]))
    nocap = dict(R["readings"])["no cap at the commitment a fund has left"]
    check("SF45 the fee line before the commitment cap is each fund's filed fee and expenses summed (the cap, quarter by quarter, takes the rest off)",
          abs(sum(nocap["fees"].values()) - F["fees_before_cap_usd_m"]) < 0.06 and F["fees_before_cap_usd_m"] > F["fees_total_usd_m"],
          "%.1f before the cap, %.1f after" % (F["fees_before_cap_usd_m"], F["fees_total_usd_m"]))
    vl = R["value_lags"]
    check("SF44 the assets' values answer equities and the short rate a quarter late: the same fit with no lag or two quarters late leaves 100 times the residual or more",
          vl[1]["sse"] * 100 <= min(vl[0]["sse"], vl[2]["sse"]), "residual %.4f a quarter late, %.3f with no lag, %.3f two quarters late" % (vl[1]["sse"], vl[0]["sse"], vl[2]["sse"]))
    act_last = {}
    for fid, evs in L["act"].items(): act_last[reg[fid]["Manager"]] = max(act_last.get(reg[fid]["Manager"], -1), max(x[0] for x in evs))
    live_mgr = {r["Manager"] for r in reg.values() if r["Status"] in ("investing", "harvesting")}
    check("SF23 every live manager's company-level reports run to the fourth quarter of 2026", all(act_last.get(m, -1) == A.H_END for m in live_mgr),
          "; ".join(m for m in sorted(live_mgr) if act_last.get(m, -1) != A.H_END) or "%d managers" % len(live_mgr))
    unk = [r["Fund"] for fid, r in reg.items() if r["Status"] == "investing" and R["clause"].get(r["Manager"], (None,))[0] is None
           and (A.successor_close(L, fit, e, fid, A.GOLDEN) or [(None, 0)])[0][0] is not None
           and A.W[0] <= A.successor_close(L, fit, e, fid, A.GOLDEN)[0][0] <= A.W[-1]]
    check("SF24 no manager without a past succession has a successor closing inside the stress (same call)", not unk, "; ".join(unk) or "none")
    rd = {n: o for n, o in R["readings"]}; ro = {n: o for n, o in R["ruled_out"]}
    y = A.OLD_YEARS
    check("SF27 the benchmark's funds a year either side of the filed vintage rule keep the call", all(
        rd["section 8's benchmark funds at a vintage %d or more years before the quarter's year" % k]["R7"] == gold for k in (y - 1, y + 1)))
    check("SF28 the benchmark rate net of the same funds' ordinary calls keeps the call",
          rd["section 8's benchmark rate less the same funds' rate over the eight quarters before the stress window"]["R7"] == gold)
    old31 = [x for x in states if not x["pending"] and not x["liquidated"] and x["st"] in A.EQUITY and x["ipl"] <= A.H_END]
    check("SF29 the funds past their investment periods at 31 December are the register's harvesting funds (the status follows the recorded end)",
          all((reg[x["fid"]]["Status"] == "harvesting") == (x["ipl"] <= A.H_END) for x in states if not x["pending"] and not x["liquidated"]), "%d buyout, growth and venture funds" % len(old31))
    check("SF30 the pace on first investments alone is ruled out by the filed sentence and lands elsewhere", ro["the pace on first investments alone"]["R7"] != gold)
    check("SF31 the pace over the commitment not yet called keeps the call", rd["the pace over the commitment not yet called"]["R7"] == gold,
          "%.1f" % rd["the pace over the commitment not yet called"]["R5"])
    check("SF32 first closes slipped on the exit market are ruled out by the filed sentence and land elsewhere",
          ro["first closes slipped on the exit market as past closes were"]["R7"] != gold)
    check("SF33 reinvested proceeds netted from the calls keep the call", rd["proceeds reinvested at each manager's audited rate netted from the calls"]["R7"] == gold)
    check("SF34 no cap at the commitment keeps the call", rd["no cap at the commitment a fund has left"]["R7"] == gold,
          "%.1f" % rd["no cap at the commitment a fund has left"]["R5"])
    fm = {n: o for n, o in R["family"]}
    kfc = "the fee after a fund's investment period on the cost it still holds"
    check("SF35 fees and expenses at each fund's latest statement (policy section 8); on the cost still held after a period, the call stands",
          A.GOLDEN["fees_post"] == "flat" and rd[kfc]["R7"] == gold, "%.1f" % rd[kfc]["R5"])
    kex = "investment periods extended in the stress as the register shows past weak exit markets extended them"
    exo = fm[kex]
    check("SF36 no investment period is extended in the stress; extended as past weak markets extended them, the call stands and every graded figure stays in its band",
          A.GOLDEN["extensions"] == "none" and g["extended"] == 0 and exo["R7"] == gold and exo["extended"] > 0 and all(FG.inband(FG.bands(R)[k], exo[k]) for rid, k in FG.GRADED),
          "%.1f with USD %.0f million of commitments extended" % (exo["R5"], exo["extended"]))
    kmr = "the facility balances less proceeds reinvested since the last audit at each manager's audited rate"
    kgp = "the facility balances as the investments less the capital called for them, the audited borrowings set aside"
    check("SF37 the facility balances as policy section 8 forms them; proceeds reinvested since at the manager's rate, or the audits set aside, keep the call",
          rd[kmr]["R7"] == gold and rd[kgp]["R7"] == gold, "%.1f and %.1f" % (rd[kmr]["R5"], rd[kgp]["R5"]))
    ft = A.facility_table(L, R["per"])
    lit = sum(x["balance"] for fid, x in ft.items() if reg[fid]["Status"] != "liquidated")
    check("SF37 the facility balance is the filed sum fund by fund (audited borrowings, plus investments since, less capital called for them since, never below nil)",
          abs(lit - F["line_stock_usd_m"]) < 0.06 and all(abs(ft[fid]["balance"] - v) < 1e-6 for fid, v in R["stock"].items()), "%.1f against %.1f" % (lit, F["line_stock_usd_m"]))
    inip = [x for x in states if not x["pending"] and not x["liquidated"] and x["ipl"] > A.H_END]
    check("SF40 a fund's last investing quarter is the quarter its period ends, and the benchmark's rate starts the quarter after (the register's past successions end the quarter before the successor's first close)",
          all(v[1][0] == v[1][1] for m_, v in R["clause"].items() if v[0] is True and v[1] is not None) and len(inip) > 10
          and all(e_["close"] - 1 < e_["registered_end"] for e_ in R["successor_events"]),
          "%d past successions of the clause managers, all ending the quarter before; %d funds investing at 31 December"
          % (sum(v[1][1] for v in R["clause"].values() if v[0] is True and v[1] is not None), len(inip)))
    check("SF39 the custodian's fourth-quarter calls are taken as called for investments in the facility balance (policy section 8)",
          "the calls the custodian recorded in the quarter are taken as called for investments" in pol and F["late_statements"] > 0, "%d late statements" % F["late_statements"])
    check("SF41 investments and the commitment not yet invested are the managers' activity at the endowment's share (policy section 8)",
          "their investments in companies and assets, first and follow-on" in pol and "A commitment not yet invested is the commitment less the endowment's share of the investments the fund has made" in pol
          and fm["the pace summed over the funds' whole commitments, not Wexmoor's share of them"]["R7"] == gold)
    stack = ev(dict(A.GOLDEN, old_fees=True), None, A.line_stock(L, recycling="gap")[0])
    check("the two readings a judge stacked (the gap as the facility balance, the funds' fees on top of the benchmark's rate) are each ruled out by a filed sentence (SF37, SF14)",
          "The balance is taken as the borrowings on the fund's latest audited balance sheet" in pol and "whose fees and expenses are within the rate above" in pol,
          "stacked they would file %.1f and program %s" % (stack["R5"], stack["R7"]))
    an = rt["the same benchmark rate for every strategy on the careful route"]
    check("SF38 section 8's benchmark rate carried to the property, infrastructure and credit funds lands on another program", an["R7"] != gold
          and rt["the benchmark's rate of section 8 carried to the property, infrastructure and credit funds past their periods, the loans rolled over as they stand"]["R7"] != gold,
          "%.1f %s" % (an["R5"], an["R7"]))
    # ------------------------------------------------------------ hygiene of the pack
    prompt = open(os.path.join(TASK, "prompt.txt")).read() if os.path.exists(os.path.join(TASK, "prompt.txt")) else ""
    nums = re.findall(r"\d[\d,]*\.?\d*", prompt)
    check("the prompt states no figure the world produces (only the years)", all(n.strip(",.") in ("2026", "2027", "2028", "31") for n in nums), ", ".join(nums))
    over = [fid for fid in live if sum(v["contributions_investments_usd"] + v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"]
                                       for v in L["st"][fid].values()) > float(reg[fid]["Commitment (USD m)"]) + 1e-6]
    check("no fund has called more than its commitment", not over, "; ".join(over) or "%d funds" % len(live))
    stl = [r["Status"] for r in reg.values()]
    check("the register carries every status, none dominating", all(stl.count(s) >= 4 for s in ("investing", "harvesting", "liquidated", "pending first close")),
          ", ".join("%s %d" % (s, stl.count(s)) for s in sorted(set(stl))))
    # ------------------------------------------------------------ the deliverables
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("no em dash in the answer blocks", "—" not in sub)
    src = open(os.path.join(HERE, "analysis.py")).read()
    check("the distractors are never read", all(n not in src for n in (DC.F_PEER, DC.F_CAPPLAN, DC.F_IPS)))
    check("the stated figures appear in the answer blocks", all(format(x, ",.1f") in sub for x in (F["headroom_before_2027_usd_m"], F["refinancing_calls_total_usd_m"],
                                                                                                    F["successor_effect_usd_m"], F["line_stock_usd_m"])))
    check("the answer blocks name the golden program first", sub.split("## Final Recommendation")[1].strip().startswith("Adopt program %s" % F["program"]))
    print("\n%d failure%s" % (len(fails), "" if len(fails) == 1 else "s"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
