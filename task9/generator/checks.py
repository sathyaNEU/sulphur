"""task9 checks (architecture 7): the pack against the clean truth, every semantic fork (SF1 to SF23), the ladder and
the rivals (the Sulfur block, R1 to R7), the back-tests the easy routes pass (B1, B2), the world's own process (T1), the ordinary record of Kestrel
Lane's houses (S1), the recovery evidence and its grain (V1 to V4) and the literal reading (L1). Exit 1 on any failure.

    python3 task9/generator/checks.py
"""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np
from pypdf import PdfReader
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import model as MD  # noqa: E402
import truth as T  # noqa: E402
import world as WD  # noqa: E402

NS = 200_000
FAIL = []


def check(name, ok, detail=""):
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAIL.append(name)


def sim(port, E, lgd, nsim=NS, seed=31, **kw):
    cum = MD.simulate(port, E["pdt"], lgd=lgd, nsim=nsim, seed=seed, **kw)
    return MD.summary(cum, port.get("sub", A.SUBORD["KL"]), A.TARGETS)


def call_of(pk, po, bar=A.BAR):
    ok_k, ok_o = pk < bar, po < bar
    if ok_k and ok_o:
        return "KL" if pk < po else "OS"
    if ok_k:
        return "KL"
    if ok_o:
        return "OS"
    return "neither"


NAME = {"KL": "Kestrel Lane", "OS": "Ostvale", "neither": "neither"}


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    tgt = os.path.join(TASK, "target")
    W = WD.simulate()
    P = T.panel(W)
    E = MD.estimate(P)
    lg = T.lgd(W)

    # ------------------------------------------------------------ the pack against the clean truth
    pack = A.Pack(tgt)
    by_name = A.lei_index(pack)
    L = A.loans(pack, by_name)
    buys = A.deals(pack, by_name)
    PP, ids = A.panel(L, buys)
    key = lambda arr: sorted(map(tuple, arr[:, [1, 3, 4, 5, 6]].tolist()))
    check("K1 the conformed pack gives the truth's company-years", key(PP) == key(P), "%d rows" % len(PP))
    check("K2 every reported loan links to a buyout", ids["unlinked"] == 0, "%d unlinked" % ids["unlinked"])
    house_true = sorted(collections.Counter(P[:, 7].tolist()).values())
    house_pack = sorted(collections.Counter(PP[:, 7].tolist()).values())
    check("K3 the pack's houses partition the panel as the truth's do", house_true == house_pack, "%d houses" % len(house_pack))
    G = A.lgd(pack)
    check("K4 every workout on a 2008 to 2019 default has closed", G["open_before"] == 0, str(G["open_by_year"]))
    check("K5 the pack's loss given default is the truth's closed-cohort figure",
          abs(G["lgd"] - (1 - np.mean([Lx["recovery"] for Lx in W.loans if Lx["status"] == "default" and Lx["covered"]
                                       and WD.DB0 <= Lx["end"].year <= 2019]))) < 1e-3, "%.4f" % G["lgd"])
    leis = [r["lei"] for r in csv.DictReader(open(os.path.join(tgt, "lei_reference_extract_2026-12-31.csv")))]
    check("K6 every identifier carries valid ISO 7064 check digits", all(WD.lei_ok(x) for x in leis), "%d LEIs" % len(leis))
    check("K7 the Lenderbase extract holds 20,000 rows or more",
          sum(1 for _ in open(os.path.join(tgt, "lenderbase_loan_performance_2008-2026.csv"))) - 1 >= 20000)
    n_dt = sum(1 for _ in open(os.path.join(tgt, "dealtrail_buyout_transactions_1997-2026.csv"))) - 1
    check("K8 the Dealtrail extract runs to more than 20 printed pages", n_dt >= 1200, "%d rows" % n_dt)
    dtrows = list(csv.DictReader(open(os.path.join(tgt, "dealtrail_buyout_transactions_1997-2026.csv"))))
    recent_blank = sum(1 for r in dtrows if r["deal_status"] == "Completed" and r["deal_type"] in ("Primary buyout", "Secondary buyout")
                       and A._date(r["completed"]).year >= 2015 and not r["target_lei"])
    check("K12 every buyout from 2015 carries the target's LEI, so a join on LEI alone finds each company's current house",
          recent_blank == 0, "%d recent buyouts without one" % recent_blank)

    # ------------------------------------------------------------ portfolios and the golden on the truth
    X, Y = dict(T.port(W, W.X), sub=A.SUBORD["KL"]), dict(T.port(W, W.Y), sub=A.SUBORD["OS"])
    gold = dict(am=E["am"], ak=E["ak"], ah=E["ah"])
    LK = F["link"]
    link = (LK["a"], LK["bm"], LK["bh"])
    lk_pack = A.lgd_link(pack, L, buys, PP, ids, E)
    check("K14 the recovery link recomputes from the pack", abs(lk_pack["a"] - LK["a"]) < 1e-3 and
          abs(lk_pack["bh"] - LK["bh"]) < 1e-3 and abs(lk_pack["bm"] - LK["bm"]) < 1e-3, str(lk_pack))
    gk, go = sim(X, E, G["lgd"], link=link, **gold), sim(Y, E, G["lgd"], link=link, **gold)
    check("K9 the truth's golden matches figures.json within simulation noise",
          abs(100 * gk["p5"] - F["golden"]["KL"]["p5_pct"]) < 0.25 and abs(100 * go["p5"] - F["golden"]["OS"]["p5_pct"]) < 0.2,
          "KL %.2f/%.1f OS %.2f/%.1f" % (100 * gk["p5"], F["golden"]["KL"]["p5_pct"], 100 * go["p5"], F["golden"]["OS"]["p5_pct"]))
    check("K10 the golden call is neither", call_of(gk["p5"], go["p5"]) == "neither" and F["call"] == "neither")
    check("K17 the truth's expected credit losses match figures.json within simulation noise",
          abs(gk["el_port"] - F["golden"]["KL"]["el_raw"]) < 3e-4 and abs(go["el_port"] - F["golden"]["OS"]["el_raw"]) < 3e-4,
          "KL %.3f/%.3f OS %.3f/%.3f" % (100 * gk["el_port"], 100 * F["golden"]["KL"]["el_raw"], 100 * go["el_port"],
                                         100 * F["golden"]["OS"]["el_raw"]))
    pk, po = F["golden"]["KL"]["p5_raw"], F["golden"]["OS"]["p5_raw"]
    bk, bo = F["band_pct"]["KL"], F["band_pct"]["OS"]
    check("K13 the estimators' band holds the golden and keeps both notes over the bar at its lower edge",
          bk[0] <= F["golden"]["KL"]["p5_pct"] <= bk[1] + 0.1 and bo[0] <= F["golden"]["OS"]["p5_pct"] <= bo[1] + 0.1
          and bk[0] > 100 * A.BAR and bo[0] > 100 * A.BAR, "KL %s, OS %s" % (bk, bo))
    check("K11 margins: both notes over the bar by 1.5 times or more", pk > 1.5 * A.BAR and po > 1.5 * A.BAR,
          "%.2f, %.2f" % (100 * pk, 100 * po))
    for key in ("KL", "OS"):
        g = F["golden"][key]
        edge = [round(min(abs(100 * v - (math.floor(1000 * v) + 0.5) / 10), abs(100 * v - (math.floor(1000 * v) - 0.5) / 10)), 3)
                for v in g["by_year_raw"]]
        print("INFO K15 %s: distance of each year-end chance from its rounding edge (points): %s" % (key, edge))
        print("INFO K16 %s: subordination needed, unrounded: %s" % (key, g["need_raw"][:2]))
        e = 100 * g["el_raw"]
        print("INFO K18 %s: expected loss %.3f per cent, %.3f points from its rounding edge"
              % (key, e, min(abs(e - (math.floor(10 * e) + 0.5) / 10), abs(e - (math.floor(10 * e) - 0.5) / 10))))

    # ------------------------------------------------------------ semantic forks
    check("SF1 any loss in the five years is the loss at the end of 2031",
          abs(F["golden"]["KL"]["by_year_pct"][-1] - F["golden"]["KL"]["p5_pct"]) < 1e-9 and
          all(a <= b + 1e-12 for a, b in zip(gk["by_year"], gk["by_year"][1:])))
    std = " ".join(re.sub(r"\s+", " ", pg.extract_text() or "") for fn in
                   ("phl_rated_note_standard_2026.pdf", "kestrel_lane_senior_note_term_sheet.pdf",
                    "ostvale_senior_note_term_sheet.pdf") for pg in PdfReader(os.path.join(tgt, fn)).pages)
    check("SF23 each portfolio's expected credit loss is the mean of its five-year loss as a share of its par, each "
          "default's own shortfall booked at default (MP-RN-2 3.4, par as in 3.5)",
          "share of the portfolio's par" in std and abs(float(np.mean(MD.simulate(X, E["pdt"], lgd=G["lgd"], nsim=NS, seed=31,
                                                                                    link=link, **gold)[-1])) - gk["el_port"]) < 1e-12)
    check("SF2 MP-RN-2 3.2 files the portfolio held for the five years, repaid loans replaced",
          "replaced by an identical loan to the same borrower" in std)
    check("SF3 MP-RN-2 3.4 files each default's own loss over its workout, booked at default",
          "the share of it that is not recovered by the end of its workout" in std and "booked in the year of the default" in std)
    rec = np.array([Lx["recovery"] for Lx in W.loans if Lx["status"] == "default" and Lx["covered"]
                    and WD.DB0 <= Lx["end"].year <= 2019])
    check("SF4 MP-RN-2 4.2 files Gaussian standings correlated as the record shows, and recoveries with them",
          "normally distributed and are correlated as far as the record" in std and
          "and so is what lenders recover on the loans that default" in std)
    check("SF5 MP-RN-2 4.1 files the record's conditions for the five years", "same conditions as that record" in std)
    fx = A.fx_rates(pack)
    rows30 = [r for r in csv.DictReader(open(os.path.join(tgt, "ecb_euro_reference_rates_2026-12.csv"))) if r["Date"] == "2026-12-30"][0]
    fx30 = {k: float(v) for k, v in rows30.items() if k != "Date"}
    fx30["EUR"] = 1.0
    t30 = A.tape(pack, "KL", by_name, fx30, A.sector_map(pack))
    p30 = A.port_spec(t30, buys, dict(houses={}, funds={}))
    s30 = sim(p30, E, G["lgd"], link=link, **gold)
    check("SF6 a 30 December rate moves no figure", abs(s30["p5"] - gk["p5"]) < 0.0015, "%.3f against %.3f" % (100 * s30["p5"], 100 * gk["p5"]))
    check("SF7 MP-RN-2 3.3 files Lenderbase's defaults", "a payment default, an insolvency or a distressed restructuring" in std)
    k19 = []
    for fn, key, pat_note, pat_sub in (
            ("kestrel_lane_senior_note_term_sheet.pdf", "KL", r"EUR ([\d,]+\.\d) million senior secured", r"Subordination (\d+\.\d) per cent"),
            ("ostvale_senior_note_term_sheet.pdf", "OS", r"Class A senior secured notes, EUR ([\d,]+\.\d) million",
             r"together equal (\d+\.\d) per cent")):
        txt = " ".join(re.sub(r"\s+", " ", pg.extract_text() or "") for pg in PdfReader(os.path.join(tgt, fn)).pages)
        note_m, sub_pct = float(re.search(pat_note, txt).group(1).replace(",", "")), float(re.search(pat_sub, txt).group(1))
        par = F["golden"][key]["par_eur_m"]
        k19.append((key, note_m, par, sub_pct, abs(note_m - par * (1 - sub_pct / 100)) < 1.5 and abs(sub_pct / 100 - A.SUBORD[key]) < 1e-9))
    check("K19 each term sheet's Class A notes are its collateral's par less the subordination it states, the one the "
          "golden reads", all(x[-1] for x in k19), "; ".join("%s EUR %.1f m on %.1f m par at %.1f per cent" % x[:4] for x in k19))
    Lc = A.lgd_link(pack, L, buys, PP, ids, E, sample="closed")
    ck, co = sim(X, E, G["lgd"], link=(Lc["a"], Lc["bm"], Lc["bh"]), **gold), \
        sim(Y, E, G["lgd"], link=(Lc["a"], Lc["bm"], Lc["bh"]), **gold)
    check("SF8 a link fitted on every closed workout drops the open ones MP-RN-2 4.1 keeps: its recent cohorts hold only "
          "the quick workouts, so its intercept sits above the closed cohorts' and every chance falls",
          "its open workouts included" in std and Lc["a"] > LK["a"] + 0.015 and ck["p5"] < gk["p5"] and co["p5"] < go["p5"],
          "intercept %.3f against %.3f; KL %.2f OS %.2f" % (Lc["a"], LK["a"], 100 * ck["p5"], 100 * co["p5"]))
    Pl = T.panel(W, clock="loan")
    El = MD.estimate(Pl)
    lk = sim(T.port(W, W.X, "loan"), El, G["lgd"], am=El["am"], ak=El["ak"], ah=El["ah"], link=link)
    lo = sim(dict(T.port(W, W.Y, "loan"), sub=A.SUBORD["OS"]), El, G["lgd"], am=El["am"], ak=El["ak"], ah=El["ah"], link=link)
    check("SF9 the loan-age clock keeps the call",
          call_of(lk["p5"], lo["p5"]) == "neither",
          "KL %.2f OS %.2f; buyout clock fits better by %.1f" % (100 * lk["p5"], 100 * lo["p5"], E["ll_pd"] - El["ll_pd"]))
    fk, fo = sim(X, E, G["lgd"], am=E["am"], ak=E["ak"], af=E["af"]), sim(Y, E, G["lgd"], am=E["am"], ak=E["ak"], af=E["af"])
    qk, qo = sim(X, E, G["lgd"], am=E["am"], ak=E["ak"], aq=E["aq"]), sim(Y, E, G["lgd"], am=E["am"], ak=E["ak"], aq=E["aq"])
    check("SF10 the fund-year and lasting forms fit the record worse than the house-year",
          E["ll_h"] > E["ll_f"] + 10
          and E["ll_h"] > E["ll_q"] + 50, "fund-year %.2f/%.2f, lasting %.2f/%.2f; loglik h %.1f f %.1f q %.1f"
          % (100 * fk["p5"], 100 * fo["p5"], 100 * qk["p5"], 100 * qo["p5"], E["ll_h"], E["ll_f"], E["ll_q"]))
    check("SF11 MP-RN-2 2.2 chooses on the chance of loss", "buys the one with the lower chance" in std)
    cum = MD.simulate(X, E["pdt"], lgd=G["lgd"], nsim=NS, seed=33, link=link, **gold)
    need = MD.summary(cum, 0.15)["need"]
    hit = [float((cum[-1] > q).mean()) for q in need]
    check("SF12 the subordination needed is the five-year loss quantile",
          all(abs(h - t) < 0.0012 for h, t in zip(hit, A.TARGETS)), str([round(100 * h, 3) for h in hit]))
    check("SF13 euro par weights: a count-weighted portfolio keeps the call",
          call_of(sim(dict(X, w=np.full(len(X["w"]), 1 / len(X["w"]))), E, G["lgd"], link=link, **gold)["p5"],
                  sim(dict(Y, w=np.full(len(Y["w"]), 1 / len(Y["w"]))), E, G["lgd"], link=link, **gold)["p5"]) == "neither")
    check("SF14 MP-RN-2 4.2 files a one-year default chance", "one-year" in std)
    check("SF15 the term sheets relend principal to the same borrower", "lent again to the same borrower" in std)
    check("SF16 MP-RN-2 3.2 files that borrowers and loans grow older over the five years",
          "Borrowers and loans grow older as the years pass" in std)
    check("SF18 MP-RN-2 3.4 files that a defaulted loan leaves the portfolio and is not replaced",
          "A loan that has defaulted leaves the portfolio and is not replaced" in std)
    fzk = MD.summary(MD.simulate(X, E["pdt"], lgd=G["lgd"], nsim=NS, seed=31, frozen=True, link=link, **gold), 0.15)
    fzo = MD.summary(MD.simulate(Y, E["pdt"], lgd=G["lgd"], nsim=NS, seed=31, frozen=True, link=link, **gold), A.SUBORD["OS"])
    check("SF16b ages held at the portfolio date (the reading 3.2 now rules out) would keep the call",
          call_of(fzk["p5"], fzo["p5"]) == "neither", "KL %.2f OS %.2f" % (100 * fzk["p5"], 100 * fzo["p5"]))
    check("SF17 MP-RN-2 4.1 takes the workout file with its open workouts", "its open workouts included" in std)
    Lg = A.lgd_link(pack, L, buys, PP, ids, E, given="year")
    hk, ho = sim(X, E, G["lgd"], link=(Lg["a"], Lg["bm"], Lg["bh"]), **gold), \
        sim(Y, E, G["lgd"], link=(Lg["a"], Lg["bm"], Lg["bh"]), **gold)
    check("SF19 house-year shocks inferred against the year's rates alone (not the sector-year's) keep the call",
          call_of(hk["p5"], ho["p5"]) == "neither" and min(hk["p5"], ho["p5"]) > 1.15 * A.BAR,
          "KL %.2f OS %.2f" % (100 * hk["p5"], 100 * ho["p5"]))
    Ln = A.lgd_link(pack, L, buys, PP, ids, E, terms=("house",))
    nk_, no_ = sim(X, E, G["lgd"], link=(Ln["a"], 0.0, Ln["bh"]), **gold), sim(Y, E, G["lgd"], link=(Ln["a"], 0.0, Ln["bh"]), **gold)
    check("SF20 the house shock alone, without the year's, keeps the call", call_of(nk_["p5"], no_["p5"]) == "neither",
          "KL %.2f OS %.2f" % (100 * nk_["p5"], 100 * no_["p5"]))
    check("SF21 recovery shares in per cent and in fractions are read as one unit (a 0 to 1 share in every row)",
          all(0 <= x <= 1 for x in [float(r["recovery"]) / (100.0 if float(r["recovery"]) > 1 else 1.0)
                                    for r in csv.DictReader(open(os.path.join(tgt, "lenderbase_workout_recoveries_2008-2026.csv")))
                                    if r["recovery"].strip()]))

    # ------------------------------------------------------------ the ladder and the rivals (R1 to R6)
    pl_k, pl_o = sim(X, E, G["lgd"], **gold), sim(Y, E, G["lgd"], **gold)
    Ly = A.lgd_link(pack, L, buys, PP, ids, E, terms=("year",))
    yl_k, yl_o = sim(X, E, G["lgd"], link=(Ly["a"], Ly["bm"], 0.0), **gold), sim(Y, E, G["lgd"], link=(Ly["a"], Ly["bm"], 0.0), **gold)
    of_k, of_o = sim(X, E, G["lgd"], am=E["am"]), sim(Y, E, G["lgd"], am=E["am"])
    in_k, in_o = sim(X, E, G["lgd"], am=E["am"], ak=E["ak"]), sim(Y, E, G["lgd"], am=E["am"], ak=E["ak"])
    ba_k, ba_o = sim(X, E, G["lgd"], am=0.15), sim(Y, E, G["lgd"], am=0.15)
    ob_k, ob_o = sim(X, E, G["lgd"], am=E["am"], ak=E["ak"], ah=0.98 * (1 - E["am"] - E["ak"])), \
        sim(Y, E, G["lgd"], am=E["am"], ak=E["ak"], ah=0.98 * (1 - E["am"] - E["ak"]))
    print("     ladder: one-factor %.2f/%.2f industry %.2f/%.2f house pooled %.2f/%.2f year link %.2f/%.2f "
          "golden %.2f/%.2f; basel %.2f/%.2f lasting %.2f/%.2f fund-year %.2f/%.2f house-as-obligor %.2f/%.2f" % tuple(
              100 * v for v in (of_k["p5"], of_o["p5"], in_k["p5"], in_o["p5"], pl_k["p5"], pl_o["p5"], yl_k["p5"],
                                yl_o["p5"], gk["p5"], go["p5"], ba_k["p5"], ba_o["p5"], qk["p5"], qo["p5"], fk["p5"],
                                fo["p5"], ob_k["p5"], ob_o["p5"])))
    check("R1 the field's raw material ships: loan-years and buyouts, no column holds a house or a correlation",
          not any(re.search(r"sponsor|house", h, re.I) for h in
                  next(csv.reader(open(os.path.join(tgt, "lenderbase_loan_performance_2008-2026.csv"))))))
    check("R2 every mess item is neutral: the conformed pack gives the truth's panel (K1) and figures (K9)",
          "K1 the conformed pack gives the truth's company-years" not in FAIL and
          "K9 the truth's golden matches figures.json within simulation noise" not in FAIL)
    check("R3a the analyst test: the field's copula files Kestrel Lane",
          call_of(of_k["p5"], of_o["p5"]) == "KL" and call_of(in_k["p5"], in_o["p5"]) == "KL" and
          in_o["p5"] / in_k["p5"] > 1.5, "industry %.2f against %.2f" % (100 * in_k["p5"], 100 * in_o["p5"]))
    check("R3b the decisive step files the golden", call_of(gk["p5"], go["p5"]) == "neither")
    mom = MD.moment_dependence(P)
    pm_k, pm_o = sim(X, E, G["lgd"], **mom), sim(Y, E, G["lgd"], **mom)
    check("R3d the arch 6 runs' route (house-year dependence, one average loss) files Kestrel Lane, under 0.75 per cent "
          "with the golden's dependence and with the pair-moment one (the arch 6 runs' house shares, 0.39, sat at its "
          "estimate)",
          call_of(pl_k["p5"], pl_o["p5"]) == "KL" and call_of(pm_k["p5"], pm_o["p5"]) == "KL" and
          pl_k["p5"] < 0.0075 and pm_k["p5"] < 0.0075,
          "%.2f against %.2f; moment %.2f against %.2f, house share %.3f" % (
              100 * pl_k["p5"], 100 * pl_o["p5"], 100 * pm_k["p5"], 100 * pm_o["p5"], mom["ah"]))
    check("R3e the textbook downturn link (recovery on the economy's year) finds no downturn (recovery no lower in the "
          "economy's bad years) and still files Kestrel Lane",
          call_of(yl_k["p5"], yl_o["p5"]) == "KL" and yl_k["p5"] < A.BAR / 1.5 and Ly["bm"] < 0.02,
          "%.2f against %.2f, slope %.3f per unit of the year's shock" % (100 * yl_k["p5"], 100 * yl_o["p5"], Ly["bm"]))
    check("R3c no plant: Basel's assumed correlation also files Kestrel Lane", call_of(ba_k["p5"], ba_o["p5"]) == "KL",
          "%.2f against %.2f" % (100 * ba_k["p5"], 100 * ba_o["p5"]))
    rg = F["rungs"]
    rcall = lambda name: {"Kestrel Lane": "KL", "Ostvale": "OS", "neither": "neither"}[rg[name]["call"]]
    check("R4 the layers act together: no house files Kestrel Lane, the house with one loss still files it, the "
          "house's recovery read off the co-defaults inside each note files Ostvale, the house-year's state files neither",
          call_of(in_k["p5"], in_o["p5"]) == "KL" and call_of(pl_k["p5"], pl_o["p5"]) == "KL" and
          rcall("count_in_portfolio") == "OS" and call_of(gk["p5"], go["p5"]) == "neither")
    check("R5 the one-fact hint executed literally (recoveries lower in bad years: the economy's year) misses the call",
          call_of(yl_k["p5"], yl_o["p5"]) != "neither")
    check("R6 the rivals: every form without a house-linked recovery files Kestrel Lane, every sound house-linked "
          "recovery files neither",
          all(call_of(a["p5"], b["p5"]) == "KL" for a, b in ((of_k, of_o), (in_k, in_o), (ba_k, ba_o), (pl_k, pl_o),
                                                              (yl_k, yl_o))) and
          all(call_of(a["p5"], b["p5"]) == "neither" for a, b in ((hk, ho), (nk_, no_), (gk, go))) and
          all(rcall(n) == "neither" for n in ("house_link_closed", "house_link_only", "house_link_given_year",
                                              "count_whole_book", "count_whole_book_line")))
    ci, cl = rg["count_in_portfolio"], rg["count_in_portfolio_line"]
    check("R7 the co-defaults counted among each note's own loans (the table's cells or a line in the count) file "
          "Ostvale: Ostvale holds two companies of each house, so its defaults price as lone ones",
          rcall("count_in_portfolio") == "OS" and rcall("count_in_portfolio_line") == "OS" and
          max(ci["OS"]["p5_raw"], cl["OS"]["p5_raw"]) < 0.9 * A.BAR and min(ci["KL"]["p5_raw"], cl["KL"]["p5_raw"]) > 1.15 * A.BAR,
          "cells KL %.2f OS %.2f; line KL %.2f OS %.2f" % (100 * ci["KL"]["p5_raw"], 100 * ci["OS"]["p5_raw"],
                                                           100 * cl["KL"]["p5_raw"], 100 * cl["OS"]["p5_raw"]))
    check("SF22 the co-defaults a recovery moves with are the house-year's across its whole book (the record's grain): "
          "counted among a note's own loans they move the call to Ostvale (R7), the grain rules them out (V4)",
          rcall("count_in_portfolio") == "OS" and rcall("count_whole_book") == "neither" and
          F["count_link"]["book_seen_median"] >= 4 * F["grain"]["OS"]["loans_per_house_median"])
    cb, cbl = rg["count_whole_book"], rg["count_whole_book_line"]
    check("R8 the same counts over each house's whole book (the record's own grain) file neither, as the golden",
          rcall("count_whole_book") == "neither" and rcall("count_whole_book_line") == "neither" and
          min(cb["KL"]["p5_raw"], cb["OS"]["p5_raw"], cbl["KL"]["p5_raw"], cbl["OS"]["p5_raw"]) > 1.33 * A.BAR,
          "cells KL %.2f OS %.2f; line KL %.2f OS %.2f" % (100 * cb["KL"]["p5_raw"], 100 * cb["OS"]["p5_raw"],
                                                           100 * cbl["KL"]["p5_raw"], 100 * cbl["OS"]["p5_raw"]))
    # V: the recovery evidence
    rb = F["recovery_by_other_defaults"]
    check("V1 on the closed cohorts the clustered defaults recover at least 15 points less than the lone ones",
          rb["0"]["recovery_pct"] - rb["3"]["recovery_pct"] >= 15, str(rb))
    opens = [Lx for Lx in W.loans if Lx["status"] == "default" and Lx["covered"] and Lx["end"].year >= WD.DB0]
    cnt = collections.Counter((W.funds[Lx["fund"]]["house"], Lx["end"].year) for Lx in opens)
    late = [Lx for Lx in opens if Lx["end"].year >= 2020]
    sh_open = lambda grp: np.mean([Lx["resolved"] > WD.AS_OF for Lx in grp]) if grp else 0.0
    lone = [Lx for Lx in late if cnt[(W.funds[Lx["fund"]]["house"], Lx["end"].year)] == 1]
    clus = [Lx for Lx in late if cnt[(W.funds[Lx["fund"]]["house"], Lx["end"].year)] >= 3]
    check("V2 the open workouts are the clustered defaults': since 2020 a larger share of clustered defaults is still open",
          sh_open(clus) > sh_open(lone) + 0.05, "%.2f against %.2f" % (sh_open(clus), sh_open(lone)))
    gr, cki = F["grain"], F["count_link"]
    check("V4 the grain: a default in the record counts its house's whole book (median companies at risk in its "
          "house-year) while Ostvale's tape holds two of a house's companies and Kestrel Lane's most of them",
          gr["OS"]["loans_per_house_median"] <= 2 and cki["book_seen_median"] >= 4 * gr["OS"]["loans_per_house_median"]
          and gr["KL"]["loans_per_house_median"] >= 0.6 * gr["KL"]["book_per_house_median"],
          "record %s (mean %s); KL %s of %s, OS %s of %s" % (cki["book_seen_median"], cki["book_seen_mean"],
                                                             gr["KL"]["loans_per_house_median"], gr["KL"]["book_per_house_median"],
                                                             gr["OS"]["loans_per_house_median"], gr["OS"]["book_per_house_median"]))
    check("V3 recovery's slope on the house-year shock is at least four times its slope on the year's",
          abs(LK["bh"]) >= 4 * abs(LK["bm"]) or abs(LK["bm"]) < 0.01, "%.3f against %.3f" % (LK["bh"], LK["bm"]))

    # ------------------------------------------------------------ B1: the easy route's back-test passes
    rng = np.random.default_rng(5)
    years = sorted(set(P[:, 1].tolist()))
    tabpd = E["pdt"][P[:, 4], np.minimum(P[:, 5], 30)]
    thr = norm.ppf(tabpd)
    obs = np.array([P[P[:, 1] == y, 6].sum() for y in years])
    sims = []
    for _ in range(400):
        tot = []
        for y in years:
            m = P[:, 1] == y
            z = np.sqrt(E["am"]) * rng.standard_normal() + np.sqrt(E["ak"]) * rng.standard_normal(16)[P[m, 3]] \
                + np.sqrt(1 - E["am"] - E["ak"]) * rng.standard_normal(m.sum())
            tot.append(int((z < thr[m]).sum()))
        sims.append(tot)
    sims = np.array(sims)
    lo_b, hi_b = np.percentile(sims, 2.5, axis=0), np.percentile(sims, 97.5, axis=0)
    inside = int(((obs >= lo_b) & (obs <= hi_b)).sum())
    vs = np.var(sims, axis=1)
    check("B1 the industry copula back-tests on the record's yearly default counts",
          inside >= len(years) - 2 and np.percentile(vs, 5) <= np.var(obs) <= np.percentile(vs, 95),
          "%d of %d years inside the 95 per cent band; variance %.0f in [%.0f, %.0f]"
          % (inside, len(years), np.var(obs), np.percentile(vs, 5), np.percentile(vs, 95)))

    # ------------------------------------------------------------ T1: the world's own process, run forward
    def true_chance(comps, sub, ns=200_000, seed=91, chunk=25_000):
        """Each note's five-year chance under the world's own default and recovery process, the five years drawn from
        the record's years (MP-RN-2 4.1): the economy's shock resampled from 2008 to 2026, fresh industry and house
        shocks, each default's workout and recovery drawn as the world draws them."""
        p = T.port(W, comps)
        n = len(p["w"])
        uh, hi = np.unique(p["h"], return_inverse=True)
        macro = np.array([WD.MACRO[y] for y in range(WD.DB0, 2027)])
        rng = np.random.default_rng(seed)
        out = np.zeros(ns)
        for s0 in range(0, ns, chunk):
            m = min(chunk, ns - s0)
            loss, alive = np.zeros(m), np.ones((m, n), dtype=bool)
            for t in range(5):
                thr = norm.ppf(WD.BASE[p["r"]] * WD.SEAS[np.minimum(p["a"] + t, len(WD.SEAS) - 1)])
                zm = macro[rng.integers(0, len(macro), (m, 1))]
                zh = rng.standard_normal((m, len(uh)))[:, hi]
                x = (np.sqrt(WD.AM) * zm + np.sqrt(WD.AK) * rng.standard_normal((m, WD.NI))[:, p["k"]] + np.sqrt(WD.AH) * zh
                     + np.sqrt(1 - WD.AM - WD.AK - WD.AH) * rng.standard_normal((m, n)))
                dd = (x < thr[None, :]) & alive
                d = np.minimum(rng.gamma(WD.WO_SHAPE, WD.WO_SCALE, (m, n)) * np.exp(-WD.DUR_M * zm - WD.DUR_H * zh), WD.WO_MAX)
                r = np.clip(WD.REC_A - WD.REC_B * d + WD.REC_M * zm + WD.REC_H * zh + rng.normal(0, WD.REC_SD, (m, n)),
                            WD.REC_FLOOR, 1.0)
                loss += (dd * p["w"] * (1 - r)).sum(axis=1)
                alive &= ~dd
            out[s0:s0 + m] = loss
        return float((out > sub).mean())
    tk, to = true_chance(W.X, A.SUBORD["KL"]), true_chance(W.Y, A.SUBORD["OS"])
    check("T1 the world's own process, run forward over the record's years, files neither and sits inside the "
          "estimators' band",
          call_of(tk, to) == "neither" and bk[0] - 0.3 <= 100 * tk <= bk[1] + 0.3 and bo[0] - 0.3 <= 100 * to <= bo[1] + 0.3,
          "KL %.2f OS %.2f against the band KL %s OS %s" % (100 * tk, 100 * to, bk, bo))

    # ------------------------------------------------------------ S1: Kestrel Lane's houses have ordinary records
    rates = {}
    for h in set(P[:, 7].tolist()):
        m = P[:, 7] == h
        if m.sum() >= 60:
            rates[h] = P[m, 6].mean()
    allr = np.array(list(rates.values()))
    klr = [rates[h] for h in set(X["h"].tolist()) if h in rates]
    check("S1 no Kestrel Lane house stands out on its record (none above the houses' 90th percentile of default rates)",
          all(r <= np.percentile(allr, 90) for r in klr),
          "%s against a 10 to 90 per cent band of [%.3f, %.3f]" % ([round(float(r), 3) for r in klr],
                                                                  np.percentile(allr, 10), np.percentile(allr, 90)))

    # ------------------------------------------------------------ L1 and the documents
    check("L1 the literal reading of MP-RN-2 is the golden's model (standings and recoveries as the record shows them)",
          "correlated as far as the record of comparable loans shows them to be" in std and "so is what lenders recover" in std)
    texts = std.lower()
    check("D1 no document names a sponsor, a house or a fund", not re.search(r"sponsor house|\bhouse\b|sponsor's", texts))
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("D2 no em or en dash in the write-up", "—" not in sub and "–" not in sub)
    print("\n%s: %d failures" % ("PASS" if not FAIL else "FAIL", len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
