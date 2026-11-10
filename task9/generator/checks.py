"""task9 checks (architecture 7, the results chain): the pack against the clean truth, every semantic fork (SF1 to
SF29), the bar block (R1 to R7: the field's raw material, neutral mess, each result's hurried figure, no plant, no one
thing, the hints computed, the rivals), the routes each shortcut files, the evidence for both strands (V1 to V7), the
back-test the easy route passes (B1), the world's own process (T1), Kestrel Lane's houses' ordinary records (S1) and
the literal reading (L1). Exit 1 on any failure.

    python3 task9/generator/checks.py
"""
import collections
import csv
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
NAME = {"KL": "Kestrel Lane", "OS": "Ostvale", "neither": "neither"}


def check(name, ok, detail=""):
    print("%-4s %-66s %s" % ("PASS" if ok else "FAIL", name[:66], detail))
    if not ok:
        FAIL.append(name)


def sim(port, E, lgd, nsim=NS, seed=31, **kw):
    cum = MD.simulate(port, E["pdt"], lgd=lgd, nsim=nsim, seed=seed, **kw)
    return MD.summary(cum, port["sub"], A.TARGETS)


def call_of(pk, po, bar=A.BAR):
    ok_k, ok_o = pk < bar, po < bar
    if ok_k and ok_o:
        return "KL" if pk < po else "OS"
    if ok_k:
        return "KL"
    if ok_o:
        return "OS"
    return "neither"


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    EF = json.load(open(os.path.join(HERE, "effort.json")))
    tgt = os.path.join(TASK, "target")
    W = WD.simulate()
    P = T.panel(W)
    E = MD.estimate(P)

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
    check("K12 every buyout from 2015 carries the target's LEI", recent_blank == 0, "%d without one" % recent_blank)

    # ------------------------------------------------------------ the golden on the truth
    SL = MD.sector_loadings(P, E["pdt"])
    pKY = MD.cond_pd(P, P[:, 1] * 100 + P[:, 3])
    ah = MD.house_share_latent(P, pKY, SL["l"], SL["k"])
    S = F["sectors"]
    lf = np.array([S["loadings"][n] for n in [s[1] for s in WD.SECTORS]])
    check("K20 each sector's loading and the house's share recompute on the truth",
          np.max(np.abs(np.round(SL["l"], 3) - lf)) < 1e-9 and abs(round(ah, 3) - F["house_share"]) < 1e-9,
          "max gap %.4f; house %.3f against %.3f" % (float(np.max(np.abs(np.round(SL["l"], 3) - lf))), ah, F["house_share"]))
    X, Y = dict(T.port(W, W.X), sub=A.SUBORD["KL"]), dict(T.port(W, W.Y), sub=A.SUBORD["OS"])
    gold = dict(am=SL["l"], ak=SL["k"], ah=ah)
    pooled = dict(am=E["am"], ak=E["ak"], ah=E["ah"])
    LK = F["link"]
    link = (LK["a"], LK["bm"], LK["bh"])
    Eg = dict(E, l=SL["l"], k=SL["k"], ah_lat=ah)
    lk_pack = A.lgd_link(pack, L, buys, PP, ids, Eg)
    check("K14 the recovery link recomputes from the pack", abs(lk_pack["a"] - LK["a"]) < 1e-3 and
          abs(lk_pack["bh"] - LK["bh"]) < 1e-3 and abs(lk_pack["bm"] - LK["bm"]) < 1e-3, str({k: round(v, 4) for k, v in
                                                                                           lk_pack.items() if isinstance(v, float)}))
    gk, go = sim(X, E, G["lgd"], link=link, **gold), sim(Y, E, G["lgd"], link=link, **gold)
    check("K9 the truth's golden matches figures.json within simulation noise",
          abs(100 * gk["p5"] - F["golden"]["KL"]["p5_pct"]) < 0.3 and abs(100 * go["p5"] - F["golden"]["OS"]["p5_pct"]) < 0.3,
          "KL %.2f/%.1f OS %.2f/%.1f" % (100 * gk["p5"], F["golden"]["KL"]["p5_pct"], 100 * go["p5"], F["golden"]["OS"]["p5_pct"]))
    check("K10 the golden call is neither", call_of(gk["p5"], go["p5"]) == "neither" and F["call"] == "neither")
    check("K17 the truth's expected credit losses match figures.json within simulation noise",
          abs(gk["el_port"] - F["golden"]["KL"]["el_raw"]) < 4e-4 and abs(go["el_port"] - F["golden"]["OS"]["el_raw"]) < 4e-4,
          "KL %.3f/%.3f OS %.3f/%.3f" % (100 * gk["el_port"], 100 * F["golden"]["KL"]["el_raw"], 100 * go["el_port"],
                                         100 * F["golden"]["OS"]["el_raw"]))
    pk, po = F["golden"]["KL"]["p5_raw"], F["golden"]["OS"]["p5_raw"]
    bk, bo = F["band_pct"]["KL"], F["band_pct"]["OS"]
    check("K13 the estimators' band holds the golden and keeps both notes over the bar at its lower edge",
          bk[0] <= F["golden"]["KL"]["p5_pct"] <= bk[1] + 0.1 and bo[0] <= F["golden"]["OS"]["p5_pct"] <= bo[1] + 0.1
          and bk[0] > 100 * A.BAR and bo[0] > 100 * A.BAR, "KL %s, OS %s" % (bk, bo))
    check("K11 margins: both notes over the bar by 1.5 times or more", pk > 1.5 * A.BAR and po > 1.5 * A.BAR,
          "%.2f, %.2f" % (100 * pk, 100 * po))
    for k_ in ("KL", "OS"):
        g = F["golden"][k_]
        edge = [round(min(abs(100 * v - (math.floor(1000 * v) + 0.5) / 10), abs(100 * v - (math.floor(1000 * v) - 0.5) / 10)), 3)
                for v in g["by_year_raw"]]
        print("INFO K15 %s: distance of each year-end chance from its rounding edge (points): %s" % (k_, edge))
        print("INFO K16 %s: subordination needed, unrounded: %s" % (k_, g["need_raw"][:2]))
        e = 100 * g["el_raw"]
        print("INFO K18 %s: expected loss %.3f per cent, %.3f points from its rounding edge"
              % (k_, e, min(abs(e - (math.floor(10 * e) + 0.5) / 10), abs(e - (math.floor(10 * e) - 0.5) / 10))))

    # ------------------------------------------------------------ semantic forks
    std = " ".join(re.sub(r"\s+", " ", pg.extract_text() or "") for fn in
                   ("phl_rated_note_standard_2026.pdf", "kestrel_lane_senior_note_term_sheet.pdf",
                    "ostvale_senior_note_term_sheet.pdf") for pg in PdfReader(os.path.join(tgt, fn)).pages)
    check("SF1 any loss in the five years is the loss at the end of 2031",
          abs(F["golden"]["KL"]["by_year_pct"][-1] - F["golden"]["KL"]["p5_pct"]) < 1e-9 and
          all(a <= b + 1e-12 for a, b in zip(gk["by_year"], gk["by_year"][1:])))
    check("SF2 MP-RN-2 3.2 files the portfolio held for the five years, repaid loans replaced",
          "replaced by an identical loan to the same borrower" in std)
    check("SF3 MP-RN-2 3.4 files each default's own loss over its workout, booked at default",
          "the share of it that is not recovered by the end of its workout" in std and "booked in the year of the default" in std)
    check("SF4 MP-RN-2 4.2 files Gaussian standings correlated as the record shows, and recoveries with them",
          "normally distributed and are correlated as far as the record" in std and
          "and so is what lenders recover on the loans that default" in std)
    check("SF5 MP-RN-2 4.1 files the record's conditions for the five years", "same conditions as that record" in std)
    rows30 = [r for r in csv.DictReader(open(os.path.join(tgt, "ecb_euro_reference_rates_2026-12.csv"))) if r["Date"] == "2026-12-30"][0]
    fx30 = {k: float(v) for k, v in rows30.items() if k != "Date"}
    fx30["EUR"] = 1.0
    t30 = A.tape(pack, "KL", by_name, fx30, A.sector_map(pack))
    p30 = dict(A.port_spec(t30, buys, dict(houses={}, funds={})), sub=A.SUBORD["KL"])
    s30 = sim(p30, E, G["lgd"], link=link, **gold)
    check("SF6 a 30 December rate moves no figure", abs(s30["p5"] - gk["p5"]) < 0.0015, "%.3f against %.3f" % (100 * s30["p5"], 100 * gk["p5"]))
    check("SF7 MP-RN-2 3.3 files Lenderbase's defaults", "a payment default, an insolvency or a distressed restructuring" in std)
    Lc = A.lgd_link(pack, L, buys, PP, ids, Eg, sample="closed")
    ck, co = sim(X, E, G["lgd"], link=(Lc["a"], Lc["bm"], Lc["bh"]), **gold), sim(Y, E, G["lgd"], link=(Lc["a"], Lc["bm"], Lc["bh"]), **gold)
    yrs = collections.defaultdict(lambda: [0, 0])
    for r_ in csv.DictReader(open(os.path.join(tgt, "lenderbase_workout_recoveries_2008-2026.csv"))):
        yrs[r_["default_date"][:4]][0] += 1
        yrs[r_["default_date"][:4]][1] += r_["workout_status"].strip().lower().startswith("open")
    full = sorted(y for y, (n_, o_) in yrs.items() if o_ == 0)
    check("SF8 MP-RN-2 4.1 reads what lenders recover from the default years whose workouts have all closed: 2008 to "
          "2019 on this record, the golden link's defaults; a link fitted on every closed workout reads the later years' "
          "quick workouts the standard keeps out",
          "what lenders recover is read from the default years whose workouts have all closed" in std
          and full == [str(y) for y in range(2008, 2020)] and LK["n"] == sum(yrs[y][0] for y in full),
          "years %s to %s, %d defaults (link n %d); every closed workout: slope %.3f against %.3f, KL %.2f OS %.2f"
          % (full[0], full[-1], sum(yrs[y][0] for y in full), LK["n"], Lc["bh"], LK["bh"], 100 * ck["p5"], 100 * co["p5"]))
    Pl = T.panel(W, clock="loan")
    El = MD.estimate(Pl)
    lkk = sim(dict(T.port(W, W.X, "loan"), sub=A.SUBORD["KL"]), El, G["lgd"], am=SL["l"], ak=SL["k"], ah=ah, link=link)
    lko = sim(dict(T.port(W, W.Y, "loan"), sub=A.SUBORD["OS"]), El, G["lgd"], am=SL["l"], ak=SL["k"], ah=ah, link=link)
    check("SF9 the loan-age clock keeps the call", call_of(lkk["p5"], lko["p5"]) == "neither",
          "KL %.2f OS %.2f; buyout clock fits better by %.1f" % (100 * lkk["p5"], 100 * lko["p5"], E["ll_pd"] - El["ll_pd"]))
    check("SF10 the fund-year and lasting forms fit the record worse than the house-year",
          E["ll_h"] > E["ll_f"] + 10 and E["ll_h"] > E["ll_q"] + 50,
          "loglik h %.1f f %.1f q %.1f" % (E["ll_h"], E["ll_f"], E["ll_q"]))
    check("SF11 MP-RN-2 2.2 chooses on the chance of loss", "buys the one with the lower chance" in std)
    cum = MD.simulate(X, E["pdt"], lgd=G["lgd"], nsim=NS, seed=33, link=link, **gold)
    need = MD.summary(cum, A.SUBORD["KL"])["need"]
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
    fzk = MD.summary(MD.simulate(X, E["pdt"], lgd=G["lgd"], nsim=NS, seed=31, frozen=True, link=link, **gold), A.SUBORD["KL"])
    fzo = MD.summary(MD.simulate(Y, E["pdt"], lgd=G["lgd"], nsim=NS, seed=31, frozen=True, link=link, **gold), A.SUBORD["OS"])
    check("SF16b ages held at the portfolio date (the reading 3.2 rules out) would keep the call",
          call_of(fzk["p5"], fzo["p5"]) == "neither", "KL %.2f OS %.2f" % (100 * fzk["p5"], 100 * fzo["p5"]))
    check("SF17 MP-RN-2 4.1 takes the workout file with its open workouts", "its open workouts included" in std)
    check("SF18 MP-RN-2 3.4 files that a defaulted loan leaves the portfolio and is not replaced",
          "A loan that has defaulted leaves the portfolio and is not replaced" in std)
    rg = F["rungs"]
    rcall = lambda name: {"Kestrel Lane": "KL", "Ostvale": "OS", "neither": "neither"}[rg[name]["call"]]
    check("SF19 house-year shocks read against the year's rates or the year's shock keep the call",
          rcall("house_link_given_year") == "neither" and all(m["KL"] > 100 * A.BAR and m["OS"] > 100 * A.BAR
                                                               for m in F["band_members"] if "year" in m["key"].split(" ")[-1]
                                                               or m["key"].endswith("year-shock")),
          "given the year KL %.2f OS %.2f" % (rg["house_link_given_year"]["KL"]["p5_pct"], rg["house_link_given_year"]["OS"]["p5_pct"]))
    check("SF20 the house shock alone, without the year's, keeps the call", rcall("house_link_only") == "neither",
          "KL %.2f OS %.2f" % (rg["house_link_only"]["KL"]["p5_pct"], rg["house_link_only"]["OS"]["p5_pct"]))
    check("SF21 recovery shares in per cent and in fractions are read as one unit (a 0 to 1 share in every row)",
          all(0 <= x <= 1 for x in [float(r["recovery"]) / (100.0 if float(r["recovery"]) > 1 else 1.0)
                                    for r in csv.DictReader(open(os.path.join(tgt, "lenderbase_workout_recoveries_2008-2026.csv")))
                                    if r["recovery"].strip()]))
    gr, cki = F["grain"], F["count_link"]
    check("SF22 the co-defaults a recovery moves with are the house-year's across its whole book: counted among a note's "
          "own loans they buy Ostvale (R7c), the grain rules them out (V4)",
          rcall("count_in_portfolio") == "OS" and rcall("count_whole_book") == "neither" and
          cki["book_seen_median"] >= 4 * gr["OS"]["loans_per_house_median"])
    check("SF23 each portfolio's expected credit loss is the mean of its five-year loss as a share of its par",
          "share of the portfolio's par" in std and abs(float(np.mean(cum[-1])) - gk["el_port"]) < 4e-4)
    keys = [m["key"] for m in F["band_members"]]
    check("SF24 each sector's loading by the likelihood, by pair moments or in two groups keeps the call",
          all(m["KL"] > 100 * A.BAR and m["OS"] > 100 * A.BAR for m in F["band_members"]) and
          any(" pairs " in k_ for k_ in keys) and any("two groups" in k_ for k_ in keys),
          "%d members, KL %s OS %s" % (len(keys), bk, bo))
    check("SF25 the house's share on the latent scale, the pooled scale or by pair moments keeps the call",
          rcall("pooled_scale_house") == "neither" and any("pair-moment house" in k_ for k_ in keys),
          "pooled scale KL %.2f OS %.2f" % (rg["pooled_scale_house"]["KL"]["p5_pct"], rg["pooled_scale_house"]["OS"]["p5_pct"]))
    se = F["sector_evidence"]
    check("SF26 the sectors' swing is a loading on the shared year, not larger factors of their own: given their own "
          "factors, one sector at a time, Ostvale is bought (R7e), and the five sectors' yearly rates move together (V5)",
          rcall("sector_independent") in ("OS", "KL") and se["swing_corr_within"] >= se["rest_corr_within"] + 0.3,
          "independent sectors KL %.2f OS %.2f; within %.2f against %.2f" % (
              rg["sector_independent"]["KL"]["p5_pct"], rg["sector_independent"]["OS"]["p5_pct"],
              se["swing_corr_within"], se["rest_corr_within"]))
    check("SF27 the two-group fit needs a threshold; the per-sector fit does not, and both keep the call",
          rcall("sector_two_group") == "neither", "KL %.2f OS %.2f" % (rg["sector_two_group"]["KL"]["p5_pct"],
                                                                     rg["sector_two_group"]["OS"]["p5_pct"]))
    k19 = []
    for fn, key_, pat_note, pat_sub in (
            ("kestrel_lane_senior_note_term_sheet.pdf", "KL", r"EUR ([\d,]+\.\d) million senior secured", r"Subordination (\d+\.\d) per cent"),
            ("ostvale_senior_note_term_sheet.pdf", "OS", r"Class A senior secured notes, EUR ([\d,]+\.\d) million",
             r"together equal (\d+\.\d) per cent")):
        txt = " ".join(re.sub(r"\s+", " ", pg.extract_text() or "") for pg in PdfReader(os.path.join(tgt, fn)).pages)
        note_m, sub_pct = float(re.search(pat_note, txt).group(1).replace(",", "")), float(re.search(pat_sub, txt).group(1))
        par = F["golden"][key_]["par_eur_m"]
        k19.append((key_, note_m, par, sub_pct, abs(note_m - par * (1 - sub_pct / 100)) < 1.5 and abs(sub_pct / 100 - A.SUBORD[key_]) < 1e-9))
    check("SF28 each term sheet's Class A notes are its collateral's par less the subordination it states, the one the "
          "golden reads", all(x[-1] for x in k19), "; ".join("%s EUR %.1f m on %.1f m par at %.1f per cent" % x[:4] for x in k19))

    import pandas as pd
    m2s = {"Ba1": "BB+", "Ba2": "BB", "Ba3": "BB-", "B1": "B+", "B2": "B", "B3": "B-", "Caa1": "CCC+", "Caa2": "CCC",
           "Caa3": "CCC-"}
    one = lambda r_: m2s.get(str(r_).strip(), str(r_).strip())
    iso = lambda d_: ("%s-%s-%s" % tuple(reversed(str(d_).split("/")))) if "/" in str(d_) else str(d_)[:10]
    lbr = pd.read_csv(os.path.join(tgt, "lenderbase_loan_performance_2008-2026.csv"), dtype=str).dropna(subset=["obligor_lei"])
    lbr = lbr.assign(orig=lbr["origination_date"].map(iso)).drop_duplicates(["obligor_lei", "orig"])
    seen, same, hdrs = 0, 0, []
    for fn, lei_c, r_c, o_c in (("klcp_static_portfolio_2026-12-31.xlsx", "LEI", "Rating at origination (Moody's equivalent)", "Origination"),
                                ("ostvale_collateral_tape_20261231.xlsx", "Borrower LEI", "S&P equivalent at close", "Close date")):
        tp = pd.read_excel(os.path.join(tgt, fn), header=3)
        hdrs.append(r_c in tp.columns)
        tp = tp.dropna(subset=[lei_c]).assign(orig=lambda d_: pd.to_datetime(d_[o_c]).dt.strftime("%Y-%m-%d"))
        mm = tp.merge(lbr, left_on=[lei_c, "orig"], right_on=["obligor_lei", "orig"])
        seen += len(mm)
        same += int((mm[r_c].map(one) == mm["rating_at_origination"].map(one)).sum())
    check("SF29 the tapes give each loan's rating at origination, as Lenderbase does: every tape loan the record holds "
          "carries the same rating in both", all(hdrs) and seen > 100 and same == seen,
          "%d of %d shared loans agree" % (same, seen))

    # ------------------------------------------------------------ the bar block
    hdr = next(csv.reader(open(os.path.join(tgt, "lenderbase_loan_performance_2008-2026.csv"))))
    check("R1 the field's raw material ships: loan-quarters, workouts and buyouts; no column holds a house, a sector's "
          "loading, a correlation or a recovery link",
          not any(re.search(r"sponsor|house|loading|correlation|cycl", h, re.I) for h in hdr))
    # R2: each mess item mishandled moves only the record's assembly, never the call
    first = {}
    for r in csv.DictReader(open(os.path.join(tgt, "lenderbase_loan_performance_2008-2026.csv"))):
        k_ = (r["lb_loan_id"], A._period_end(r["report_period"]))
        if k_ not in first or r["submission_ts"] < first[k_]["submission_ts"]:
            first[k_] = r
    late_d = sum(1 for k_, r in first.items() if A._STATUS[r["status"]] == "W") - sum(
        1 for r in first.values() if A._STATUS[r["status"]] == "W")
    n_res = sum(1 for _ in open(os.path.join(tgt, "lenderbase_loan_performance_2008-2026.csv"))) - 1 - len(first)
    check("R2a resubmitted loan-quarters (keep the latest) are the only repeated rows; kept as first filed they hide late "
          "defaults, a count the assembly fixes", n_res > 0 and len(PP) == len(P), "%d resubmissions" % n_res)
    check("R2b every mess item is neutral once conformed: the pack's panel is the truth's (K1) and its golden the "
          "truth's (K9)", "K1 the conformed pack gives the truth's company-years" not in FAIL and
          "K9 the truth's golden matches figures.json within simulation noise" not in FAIL)
    res = {r["id"]: r for r in EF["results"]}

    def graded(r, p_):
        v = r["passes"][p_]
        if isinstance(v, dict) and set(v) <= {"value", "grade", "why"} and v.get("grade"):
            return v["grade"]
        if v is None:
            return "missed"
        if isinstance(r["golden"], dict):
            b = r.get("bands", {})
            ok = sum(1 for c, gv in r["golden"].items() if c in b and b[c][0] <= v.get(c, -1e9) <= b[c][1])
            return "right" if ok == len(r["golden"]) else ("partly" if ok >= 0.5 * len(r["golden"]) else "missed")
        if isinstance(r["golden"], str):
            return "right" if str(v).lower() == r["golden"].lower() else "missed"
        if r["band"][0] <= v <= r["band"][1]:
            return "right"
        return "partly" if r.get("partly") and r["partly"][0] <= v <= r["partly"][1] else "missed"
    careful = {i: graded(r, "careful") for i, r in res.items()}
    check("R3 each result's hurried figure: the careful but hurried pass earns the house's share and loses every result "
          "past it outside its band", careful["R1"] == "right" and all(careful[i] != "right" for i in res if i != "R1"),
          str(careful))
    blocks = collections.Counter()
    for r in csv.DictReader(open(os.path.join(tgt, "lenderbase_workout_recoveries_2008-2026.csv"))):
        blocks[tuple(v for k_, v in r.items() if k_ not in ("lb_loan_id", "obligor_name"))] += 1
    check("R4 no plant: no workout row repeats another's outcome, dates and amounts", max(blocks.values()) == 1)
    houses_clustered = len({h for (h, y), n in collections.Counter((int(h), int(y)) for h, y, d in zip(P[:, 7], P[:, 1], P[:, 6])
                                                                    if d).items() if n >= 2})
    swing = [i for i, s_ in enumerate(WD.SECTORS) if s_[1] in S["swing"]]
    sw_companies = len(set(P[np.isin(P[:, 3], swing), 0].tolist()))
    kl_sw = int(np.isin(X["k"], swing).sum())
    early = [Lx["recovery"] for Lx in W.loans if Lx["status"] == "default" and Lx["covered"] and 2008 <= Lx["end"].year <= 2013]
    check("R5 no one thing: every factor runs across the record (house-years with two or more defaults in %d houses; %d "
          "companies in the five sectors, Kestrel Lane holding %d of them; the recovery gap in both halves of the closed "
          "cohorts), and each hint rescues a third of the results or fewer" % (houses_clustered, sw_companies, kl_sw),
          houses_clustered >= 40 and sw_companies >= 800 and kl_sw >= 10 and len(early) >= 100 and
          all(len(h["rescues"]) <= len(res) / 3.0 for h in EF["hints"]))
    hk, ho = rg["sector_independent"], rg["sector_one_lgd"]
    kb, ob = res["R4"]["band"], res["R5"]["band"]
    calc = {"R3": True, "R4": kb[0] <= hk["KL"]["p5_pct"] <= kb[1], "R5": ob[0] <= hk["OS"]["p5_pct"] <= ob[1]}
    calc2 = {"R2": True, "R5": ob[0] <= ho["OS"]["p5_pct"] <= ob[1]}
    check("R6 the one-fact test computed: the recovery hint rescues %s, the sectors' hint %s, and each list is what "
          "effort.json carries" % (EF["hints"][0]["rescues"], EF["hints"][1]["rescues"]),
          sorted(k_ for k_, ok in calc.items() if ok) == sorted(EF["hints"][0]["rescues"]) and
          sorted(k_ for k_, ok in calc2.items() if ok) == sorted(EF["hints"][1]["rescues"]))
    check("R7 the rivals: every band member (two default tables, three loading estimators, three shock bases, three house "
          "scales) keeps both notes over the test", all(m["KL"] > 100 * A.BAR and m["OS"] > 100 * A.BAR for m in F["band_members"]),
          "KL %s OS %s over %d members" % (bk, bo, len(F["band_members"])))

    # ------------------------------------------------------------ the routes: different shortcuts, different wrong answers
    in_k, in_o = sim(X, E, G["lgd"], am=E["am"], ak=E["ak"]), sim(Y, E, G["lgd"], am=E["am"], ak=E["ak"])
    pl_k, pl_o = sim(X, E, G["lgd"], **pooled), sim(Y, E, G["lgd"], **pooled)
    sl_k, sl_o = sim(X, E, G["lgd"], **gold), sim(Y, E, G["lgd"], **gold)
    LKp = F["link_pooled"]
    lp = (LKp["a"], LKp["bm"], LKp["bh"])
    hl_k, hl_o = sim(X, E, G["lgd"], link=lp, **pooled), sim(Y, E, G["lgd"], link=lp, **pooled)
    print("     routes on the truth: textbook %.2f/%.2f, house one loss %.2f/%.2f, loadings one loss %.2f/%.2f, "
          "house link pooled %.2f/%.2f, golden %.2f/%.2f" % tuple(100 * v for v in (
              in_k["p5"], in_o["p5"], pl_k["p5"], pl_o["p5"], sl_k["p5"], sl_o["p5"], hl_k["p5"], hl_o["p5"], gk["p5"], go["p5"])))
    check("R7a the quick answer (the agencies' copula, one average loss from the fully closed default years) files "
          "Kestrel Lane",
          call_of(in_k["p5"], in_o["p5"]) == "KL", "%.2f against %.2f" % (100 * in_k["p5"], 100 * in_o["p5"]))
    check("R7b the house's year with one average loss (the arch 6 runs' route) files a note, not neither",
          call_of(pl_k["p5"], pl_o["p5"]) in ("KL", "OS") and pl_k["p5"] < 0.75 * A.BAR,
          "%.2f against %.2f: %s" % (100 * pl_k["p5"], 100 * pl_o["p5"], NAME[call_of(pl_k["p5"], pl_o["p5"])]))
    check("R7c the co-defaults counted among each note's own loans file Ostvale (it holds about two companies a house)",
          rcall("count_in_portfolio") == "OS" and rcall("count_in_portfolio_sector") == "OS",
          "pooled KL %.2f OS %.2f; with the loadings KL %.2f OS %.2f" % (
              rg["count_in_portfolio"]["KL"]["p5_pct"], rg["count_in_portfolio"]["OS"]["p5_pct"],
              rg["count_in_portfolio_sector"]["KL"]["p5_pct"], rg["count_in_portfolio_sector"]["OS"]["p5_pct"]))
    check("R7d the sector loadings with one average loss file Kestrel Lane: Kestrel Lane passes on one recovery",
          call_of(sl_k["p5"], sl_o["p5"]) == "KL" and sl_k["p5"] < 0.75 * A.BAR,
          "%.2f against %.2f" % (100 * sl_k["p5"], 100 * sl_o["p5"]))
    check("R7e recovery on the house-year's shock with one pooled loading files Ostvale: only the sectors' joint swing "
          "takes Ostvale past the test", call_of(hl_k["p5"], hl_o["p5"]) == "OS" and hl_o["p5"] < 0.8 * A.BAR,
          "%.2f against %.2f" % (100 * hl_k["p5"], 100 * hl_o["p5"]))
    calls = {r["answer"] for r in EF["routes"] if not r.get("golden")}
    check("R7f depth: the shortcuts land on two or more different wrong answers and none of the eight files the golden",
          len(calls - {"neither"}) >= 2 and "neither" not in calls, str(sorted(calls)))

    # ------------------------------------------------------------ V: the evidence
    rb = F["recovery_by_other_defaults"]
    check("V1 on the closed cohorts the clustered defaults recover at least 15 points less than the lone ones",
          rb["0"]["recovery_pct"] - rb["3"]["recovery_pct"] >= 15, str(rb))
    oe = F["open_evidence"]
    oe_pack = A.open_evidence(pack, L, buys, PP, ids, Eg)
    check("V2 the open workouts are the clustered defaults' long ones: on the closed cohorts a workout in the worst third "
          "of house-years took longer than one in the best third, and since 2020 the open workouts sit in worse "
          "house-years than the closed ones", oe["worst_third_years"] > oe["best_third_years"] + 0.5 and
          oe["open_shock"] < oe["closed_shock"] - 0.1 and abs(oe_pack["open_shock"] - oe["open_shock"]) < 0.01,
          "%.2f against %.2f years; shocks %.2f against %.2f" % (oe["worst_third_years"], oe["best_third_years"],
                                                                  oe["open_shock"], oe["closed_shock"]))
    Ly = F["link_year_only"]
    check("V3 recovery does not fall in the economy's bad years (its slope on the year's shock alone is not positive) "
          "while its slope on the house-year's shock is", Ly["bm"] <= 0.01 and LK["bh"] >= 0.2,
          "%.3f against %.3f" % (Ly["bm"], LK["bh"]))
    check("V4 the grain: a default in the record counts its house's whole book while Ostvale's tape holds about two of a "
          "house's companies and Kestrel Lane's most of them",
          gr["OS"]["loans_per_house_median"] <= 2 and cki["book_seen_median"] >= 4 * gr["OS"]["loans_per_house_median"]
          and gr["KL"]["loans_per_house_median"] >= 0.6 * gr["KL"]["book_per_house_median"],
          "record %s; KL %s of %s, OS %s of %s" % (cki["book_seen_median"], gr["KL"]["loans_per_house_median"],
                                                   gr["KL"]["book_per_house_median"], gr["OS"]["loans_per_house_median"],
                                                   gr["OS"]["book_per_house_median"]))
    check("V5 the five sectors' yearly default rates move together, the rest's barely",
          se["swing_corr_within"] >= 0.45 and se["rest_corr_within"] <= 0.25,
          "%.2f against %.2f (cross %.2f)" % (se["swing_corr_within"], se["rest_corr_within"], se["swing_rest_corr"]))
    check("V6 one loading per sector fits the record far better than one for all (15 more parameters)",
          S["lr"] >= 30, "2 dlogL %.1f on %d" % (S["lr"], S["df"]))
    check("V7 the swing runs across the record's years and houses: in the economy's three worst years the five sectors "
          "default at least twice the rest's rate", all(se["swing_rate_pct"][str(y)] >= 2 * se["rest_rate_pct"][str(y)]
                                                        for y in se["worst_years"]), str(se["worst_years"]))

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
    check("B1 the agencies' copula back-tests on the record's yearly default counts",
          inside >= len(years) - 3, "%d of %d years inside the 95 per cent band" % (inside, len(years)))

    # ------------------------------------------------------------ T1: the world's own process, run forward
    def true_chance(comps, sub, ns=200_000, seed=91, chunk=25_000):
        p = T.port(W, comps)
        n = len(p["w"])
        uh, hi = np.unique(p["h"], return_inverse=True)
        macro = np.array([WD.MACRO[y] for y in range(WD.DB0, 2027)])
        am_i = np.array(WD.AM_S)[p["k"]]
        rng = np.random.default_rng(seed)
        out = np.zeros(ns)
        for s0 in range(0, ns, chunk):
            m = min(chunk, ns - s0)
            loss, alive = np.zeros(m), np.ones((m, n), dtype=bool)
            for t in range(5):
                thr_ = norm.ppf(WD.BASE[p["r"]] * WD.SEAS[np.minimum(p["a"] + t, len(WD.SEAS) - 1)])
                zm = macro[rng.integers(0, len(macro), (m, 1))]
                zh = rng.standard_normal((m, len(uh)))[:, hi]
                x = (np.sqrt(am_i)[None, :] * zm + np.sqrt(WD.AK) * rng.standard_normal((m, WD.NI))[:, p["k"]]
                     + np.sqrt(WD.AH) * zh + np.sqrt(1 - am_i - WD.AK - WD.AH)[None, :] * rng.standard_normal((m, n)))
                dd = (x < thr_[None, :]) & alive
                d = np.minimum(rng.gamma(WD.WO_SHAPE, WD.WO_SCALE, (m, n)) * np.exp(-WD.DUR_M * zm - WD.DUR_H * zh), WD.WO_MAX)
                r = np.clip(WD.REC_A - WD.REC_B * d + WD.REC_M * zm + WD.REC_H * zh + rng.normal(0, WD.REC_SD, (m, n)),
                            WD.REC_FLOOR, 1.0)
                loss += (dd * p["w"] * (1 - r)).sum(axis=1)
                alive &= ~dd
            out[s0:s0 + m] = loss
        return float((out > sub).mean())
    tk, to = true_chance(W.X, A.SUBORD["KL"]), true_chance(W.Y, A.SUBORD["OS"])
    check("T1 the world's own process, run forward over the record's years, files neither",
          call_of(tk, to) == "neither", "KL %.2f OS %.2f against the band KL %s OS %s" % (100 * tk, 100 * to, bk, bo))

    # ------------------------------------------------------------ S1: Kestrel Lane's houses have ordinary records
    rates = {}
    for h in set(P[:, 7].tolist()):
        m = P[:, 7] == h
        if m.sum() >= 60:
            rates[h] = P[m, 6].mean()
    allr = np.array(list(rates.values()))
    klr = [rates[h] for h in set(X["h"].tolist()) if h in rates]
    check("S1 no Kestrel Lane house stands out on its record (none above the houses' 90th percentile of default rates)",
          all(r <= np.percentile(allr, 90) for r in klr), "%s" % [round(float(r), 3) for r in klr])

    # ------------------------------------------------------------ L1 and the documents
    check("L1 the literal reading of MP-RN-2 is the golden's model (standings and recoveries as the record shows them)",
          "correlated as far as the record of comparable loans shows them to be" in std and "so is what lenders recover" in std)
    texts = std.lower()
    check("D1 no document names a sponsor house, a cycle or a sector's loading",
          not re.search(r"sponsor house|\bhouse\b|sponsor's|cyclical|\bcycle\b|loading", texts))
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("D2 no em or en dash in the write-up", "—" not in sub and "–" not in sub)
    print("\n%s: %d failures" % ("PASS" if not FAIL else "FAIL", len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
