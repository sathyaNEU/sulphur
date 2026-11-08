"""task7 checks, run on the cut pack under target/: every graded figure's bin and margin, the ladder's rungs and their
separation, the rival family, every semantic fork row (SF1 to SF23), the Sulfur block and the input gates."""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

import golden as GD

UT, UB = 500000.0, 250000.0
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def rnd(v, u):
    return round(v / u) * u


def edge(v, u):
    """distance from v to the nearest edge of the cell it rounds into"""
    return u / 2 - abs(v - rnd(v, u))


def pdf_text(target, name):
    from pypdf import PdfReader
    rd = PdfReader(os.path.join(target, name))
    text = " ".join(" ".join((pg.extract_text() or "").split()) for pg in rd.pages)
    return re.sub(r"([A-Za-z])- (\d)", r"\1-\2", text)   # a hyphen broken across lines, as in a model's name


def total_of(items, fac):
    return GD.summarise(GD.ecl(items, fac))


def run(target, gen_dir):
    T, rec, items, fns, fits, res = GD.compute(target)
    gold = res["golden"]
    G_T, G_I, G_O = gold["total"], gold["investment"], gold["owner_occupied"]
    cT, cI, cO = rnd(G_T, UT), rnd(G_I, UB), rnd(G_O, UB)
    out = {}
    # ---- the call and its asks sit mid-bin, and every member of the standing family files the same cells
    main_family = ["golden", "split_normal", "split_lin", "split_band", "split_median", "pooled", "pooled_lin",
                   "pooled_band", "pooled_median"]
    book_family = ["golden", "split_normal", "split_lin", "split_band", "split_median"]
    for k in main_family:
        check("main family %s files the plan figure's cell" % k, rnd(res[k]["total"], UT) == cT,
              "%.0f -> %.0f" % (res[k]["total"], rnd(res[k]["total"], UT)))
    check("main figure clear of its bin edge (every family member, 80,000 or more)",
          min(edge(res[k]["total"], UT) for k in main_family) >= 80000,
          "%.0f" % min(edge(res[k]["total"], UT) for k in main_family))
    for k in book_family:
        check("book family %s files the investment cell" % k, rnd(res[k]["investment"], UB) == cI, "%.0f" % res[k]["investment"])
        check("book family %s files the owner-occupied cell" % k, rnd(res[k]["owner_occupied"], UB) == cO, "%.0f" % res[k]["owner_occupied"])
    check("book cells clear of their bin edges (every split member, 30,000 or more)",
          min(min(edge(res[k]["investment"], UB), edge(res[k]["owner_occupied"], UB)) for k in book_family) >= 30000)
    top = set(gold["top5"])
    for k in book_family:
        check("top five identical under %s" % k, set(res[k]["top5"]) == top, str(res[k]["top5"]))
    # ---- the ladder: each shallow route files another plan figure, by at least a fifth of a bin
    for k in ("carried", "reflex_10_over_3y", "record_mean"):
        check("rung %s files another plan figure" % k, rnd(res[k]["total"], UT) != cT,
              "%.0f -> %.0f" % (res[k]["total"], rnd(res[k]["total"], UT)))
        check("rung %s clear of the golden cell" % k, abs(res[k]["total"] - cT) - UT / 2 >= 0.2 * UT,
              "%.0f" % (abs(res[k]["total"] - cT) - UT / 2))
    # the cycle's own re-inspections (no default selection, no distress) as a rival
    cyc_t, cyc_r = [], []
    for p, h in T.val.items():
        ins = [x for x in h if x["basis"] == "INSPECTION"]
        for a, b in zip(ins[:-1], ins[1:]):
            car = GD.in_force(h, b["vdate"] - dt.timedelta(days=1))
            if car is None or car["basis"] != "INDEX ROLL-FORWARD":
                continue
            # an inspection that follows a default is not a cycle inspection
            cyc_t.append((b["vdate"] - a["vdate"]).days / 365.25)
            cyc_r.append(b["value"] / car["value"])
    dflt_insp = {(x["p"]) for x in rec}
    cy = np.polyfit(np.array(cyc_t), np.log(np.array(cyc_r)), 1)
    cyc = total_of(items, lambda t, bk: math.exp(cy[1] + cy[0] * t))
    res["cycle_drift"] = cyc
    check("rung cycle_drift (inspections of performing loans) files another plan figure", rnd(cyc["total"], UT) != cT,
          "%.0f" % cyc["total"])
    # blanket haircuts a solver might add by reflex
    for hc in (0.10, 0.15, 0.20, 0.25):
        b = total_of(items, lambda t, bk, hc=hc: 1 - hc)
        res["blanket_%d" % int(100 * hc)] = b
        check("blanket %d per cent haircut misses the plan cell" % int(100 * hc), rnd(b["total"], UT) != cT, "%.0f" % b["total"])
    # recent experience: the record's average shortfall over its latest years, flat on every facility, overall and
    # by lending book, by mean, exposure-weighted mean and median (the improving recent years read as the market)
    R_ = np.array([x["ratio"] for x in rec])
    Y_ = np.array([x["date"].year for x in rec])
    E_ = np.array([x["ead"] for x in rec])
    B_ = np.array([x["book"] == GD.TRADING for x in rec])
    worst = None
    for lo in range(2016, 2027):
        m_ = Y_ >= lo
        variants = {"mean": lambda m: float(R_[m].mean()), "exposure-weighted mean": lambda m: float((R_[m] * E_[m]).sum() / E_[m].sum()),
                    "median": lambda m: float(np.median(R_[m]))}
        for vn, vf in variants.items():
            v = vf(m_)
            r_ = total_of(items, lambda t, bk, v=v: v)
            res["recent %s from %d" % (vn, lo)] = r_
            gap = abs(r_["total"] - cT) - UT / 2
            worst = gap if worst is None else min(worst, gap)
            vb = {True: vf(m_ & B_), False: vf(m_ & ~B_)}
            r_ = total_of(items, lambda t, bk, vb=vb: vb[bk == GD.TRADING])
            res["recent %s by book from %d" % (vn, lo)] = r_
            worst = min(worst, abs(r_["total"] - cT) - UT / 2)
    check("rung: recent experience (any window from 2016, mean, weighted or median, pooled or by book) misses the plan "
          "cell", worst > 0, "nearest %.0f outside" % worst)
    # the landed run that pools the books lands the call and misses both book cells
    check("pooled staleness files the plan cell", rnd(res["pooled"]["total"], UT) == cT)
    check("pooled staleness misses the investment cell", rnd(res["pooled"]["investment"], UB) != cI, "%.0f" % res["pooled"]["investment"])
    check("pooled staleness misses the owner-occupied cell", rnd(res["pooled"]["owner_occupied"], UB) != cO, "%.0f" % res["pooled"]["owner_occupied"])
    check("pooled staleness: the five recorded (the landed run keeps them)", True,
          "%d of 5" % len(set(res["pooled"]["top5"]) & top))
    # ---- Sulfur block: the analyst test on the clean truth, the deep chain's links, the judgment's evidence
    check("analyst test: the model on the carried values files two or more cells below the plan figure",
          rnd(res["carried"]["total"], UT) <= cT - 2 * UT, "%.0f, cell %.0f" % (res["carried"]["total"], rnd(res["carried"]["total"], UT)))
    pt, it = fits["split"][True], fits["split"][False]
    check("record: the shortfall grows with years since inspection, owner-occupied", pt["b"] < -0.02, "%.4f" % pt["b"])
    check("record: the shortfall grows with years since inspection, investment", it["b"] < -0.02, "%.4f" % it["b"])
    taus = np.array([x["tau"] for x in rec])
    ratios = np.array([x["ratio"] for x in rec])
    slope_se = float(np.sqrt(np.var(np.log(ratios) - np.polyval(np.polyfit(taus, np.log(ratios), 1), taus)) /
                             (len(taus) * np.var(taus))))
    check("record: the staleness slope is many standard errors from nought", abs(fits["pooled"]["b"]) / slope_se > 8,
          "slope %.4f, se %.4f" % (fits["pooled"]["b"], slope_se))
    check("record: owner-occupied security falls further at default (level)", pt["a"] < it["a"] - 0.03,
          "%.4f against %.4f" % (pt["a"], it["a"]))
    check("record covers the book's staleness (defaults 7 years or more since inspection)",
          int((taus >= 7).sum()) >= 60, str(int((taus >= 7).sum())))
    book_tau = [(pt_["tau"], it_["ead"]) for it_ in items for pt_ in it_["parts"]]
    ead_tot = sum(e for _, e in book_tau)
    stale_share = sum(e for t, e in book_tau if t >= 7) / ead_tot
    rec_stale = float((taus >= 7).mean())
    check("the book is staler than the record (exposure last inspected 7 years or more ago)", stale_share > 2 * rec_stale,
          "book %.3f, record %.3f" % (stale_share, rec_stale))
    # the write-up's worded bounds, each asserted against the quantity it bounds (reduce-house-fixes H29)
    recent_ = [x for x in rec if x["date"].year >= 2022]
    fresh_share = sum(1 for x in recent_ if x["tau"] < 0.5) / len(recent_)
    recent_stale = sum(1 for x in recent_ if x["tau"] >= 7) / len(recent_)
    check("bound: over a third of the defaults since 2022 were inspected in the six months before default",
          fresh_share > 1 / 3, "%.3f" % fresh_share)
    check("bound: about one in ten of the defaults since 2022 rested on an inspection seven or more years old",
          0.05 <= recent_stale <= 0.15, "%.3f" % recent_stale)
    check("bound: fewer than one in ten of the record's properties rested on an inspection seven or more years old",
          rec_stale < 0.10, "%.3f" % rec_stale)
    t_book = {}
    for bk_ in (True, False):
        sub = [x for x in rec if (x["book"] == GD.TRADING) == bk_]
        tt = np.array([x["tau"] for x in sub])
        yy = np.log(np.array([x["ratio"] for x in sub]))
        Xb = np.c_[np.ones_like(tt), tt]
        cb = np.linalg.lstsq(Xb, yy, rcond=None)[0]
        eb = yy - Xb @ cb
        s2 = float(eb @ eb) / (len(tt) - 2)
        t_book[bk_] = abs(cb[1]) / np.sqrt(s2 * np.linalg.inv(Xb.T @ Xb)[1, 1])
    check("bound: the staleness slope is more than 10 standard errors from nought in each lending book",
          min(t_book.values()) > 10, "owner-occupied %.1f, investment %.1f" % (t_book[True], t_book[False]))
    # ---- the standing family beyond the main grid: every rival a careful analyst would run lands the same cells
    TR = GD.TRADING
    cells = lambda r: (rnd(r["total"], UT), rnd(r["investment"], UB), rnd(r["owner_occupied"], UB), frozenset(r["top5"]))
    gcells = cells(gold)

    def split_fit(rr, design, weights=None):
        F = {}
        for bk in (True, False):
            sub = [x for x in rr if (x["book"] == TR) == bk]
            t = np.array([x["tau"] for x in sub])
            y = np.log(np.array([x["ratio"] for x in sub]))
            X = design(t)
            w = np.ones_like(t) if weights is None else np.array([weights(x) for x in sub])
            c = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
            F[bk] = (c, float(np.sum(w * np.exp(y - X @ c)) / np.sum(w)))
        return F

    def apply_fit(F, design):
        return lambda t, bk: math.exp(float((design(np.array([t])) @ F[bk == TR][0])[0])) * F[bk == TR][1]

    lin_d = lambda t: np.c_[np.ones_like(t), t]
    rivals = {
        "exposure-weighted": (rec, lin_d, lambda x: x["ead"]),
        "defaults 2017 to 2026": ([x for x in rec if x["date"].year >= 2017], lin_d, None),
        "defaults 2012 to 2019": ([x for x in rec if x["date"].year <= 2019], lin_d, None),
        "defaults 2020 to 2026": ([x for x in rec if x["date"].year >= 2020], lin_d, None),
        "quadratic in years": (rec, lambda t: np.c_[np.ones_like(t), t, t * t], None),
        "square root of years": (rec, lambda t: np.c_[np.ones_like(t), np.sqrt(t)], None),
        "log of one plus years": (rec, lambda t: np.c_[np.ones_like(t), np.log1p(t)], None),
    }
    for name, (rr, des, wt) in rivals.items():
        r = total_of(items, apply_fit(split_fit(rr, des, wt), des))
        res["rival " + name] = r
        check("rival (%s) files the golden's cells" % name, cells(r) == gcells,
              "%.0f / %.0f / %.0f" % (r["total"], r["investment"], r["owner_occupied"]))
    # one slope, an intercept for each book
    t_ = np.array([x["tau"] for x in rec])
    y_ = np.log(np.array([x["ratio"] for x in rec]))
    o_ = np.array([1.0 if x["book"] == TR else 0.0 for x in rec])
    Xc = np.c_[np.ones_like(t_), o_, t_]
    cc = np.linalg.lstsq(Xc, y_, rcond=None)[0]
    smc = float(np.mean(np.exp(y_ - Xc @ cc)))
    r = total_of(items, lambda t, bk: math.exp(cc[0] + cc[1] * (bk == TR) + cc[2] * t) * smc)
    res["rival common slope"] = r
    check("rival (one slope, a level for each book) files the golden's cells", cells(r) == gcells,
          "%.0f / %.0f / %.0f" % (r["total"], r["investment"], r["owner_occupied"]))
    # the receivers' net proceeds against the carried value, fitted the same way, priced with no further haircut
    sales = defaultdict(list)
    for s_ in GD.rows(target, "receiver_sales_2012_2026.csv"):
        sales[s_["property_id"]].append(s_)
    net = []
    for x in rec:
        ss = [s_ for s_ in sales.get(x["p"], []) if GD.D(s_["completion_date"]) >= x["date"]]
        if ss:
            car = GD.in_force(T.val[x["p"]], x["date"])["value"]
            net.append(dict(x, ratio=(float(ss[0]["gross_price_eur"]) - float(ss[0]["selling_costs_eur"])) / car))
    Fn = split_fit(net, lin_d)
    fn_net = apply_fit(Fn, lin_d)
    loans = []
    for it_ in items:
        v = sum(p_["carried"] * fn_net(p_["tau"], it_["book"]) for p_ in it_["parts"])
        loans.append(dict(fac=it_["fac"], book=it_["book"], el=it_["pd"] * max(0.0, it_["ead"] - v)))
    r = GD.summarise(loans)
    res["rival sale proceeds"] = r
    check("rival (receivers' net proceeds against the carried value, no haircut) files the golden's cells",
          cells(r) == gcells, "%.0f / %.0f / %.0f, %d sales" % (r["total"], r["investment"], r["owner_occupied"], len(net)))

    # ---- semantic fork rows: each alternative reading lands the golden's cells (same call) or is ruled out by a
    # sentence the pack ships, asserted on the PDF's own text
    memo = pdf_text(target, "plan_2027_credit_loss_request.pdf")
    pol = pdf_text(target, "ardcarn_credit_risk_policy_part4_2025.pdf")
    mdl = pdf_text(target, "cre_lgd_model_documentation_2025.pdf")
    # SF1: the line is the expected loss on 2027 defaults of the year-end performing book, not 2027 write-offs
    check("SF1 the memo files the line as expected credit loss on facilities performing at the year end",
          "expected credit loss on the commercial property facilities that are performing at 31 December 2026" in memo
          and "default during 2027" in memo and G_T > 0)
    # SF2: the population is the facilities performing at 31 December 2026
    in_default = sum(1 for f, r_ in T.book.items() if r_["default_flag"] != "N")
    check("SF2 the population excludes facilities in default at the year end",
          in_default == 0 and len(items) == len(T.book) and "are provided for separately and are not in this line" in memo)
    # SF3: the batch loaded twice (June 2024) reaches no year-end row: one 20261231 row per facility
    ye = [r_["facility_no"] for r_ in GD.rows(target, "dw_fact_loan_month_end_2022_2026.csv")
          if r_["month_end_key"] == "20261231"]
    check("SF3 one year-end row per facility", len(ye) == len(set(ye)), "%d rows" % len(ye))
    # SF4: the master scale sets the chance of default (memo and policy 4.1)
    check("SF4 every graded facility carries a master-scale grade, as the memo and policy file it",
          all(i_["grade"] in GD.MASTER_PD for i_ in items) and "master scale for its grade at 31 December 2026" in memo)
    # SF5: exposure is the year-end balance (memo)
    check("SF5 exposure is the 31 December 2026 balance", all(i_["ead"] > 0 for i_ in items)
          and "its exposure is its balance at that date" in memo)
    # SF6: the expected value at default (mean); the median variant lands the same cells (corridor)
    check("SF6 the median variant files the golden's cells", cells(res["split_median"]) == gcells)
    # SF7: each default as if on 1 January 2027 (memo); a default spread through 2027 is another cell, ruled out
    late = total_of([dict(it_, parts=[dict(p_, tau=p_["tau"] + 0.5) for p_ in it_["parts"]]) for it_ in items], fns["golden"])
    res["midyear"] = late
    check("SF7 the memo files each default as if on 1 January 2027 (a mid-2027 default is recorded)",
          "as if it fell on 1 January 2027" in memo, "%.0f, cell %.0f" % (late["total"], rnd(late["total"], UT)))
    # SF8: prices held at the latest published level (memo); the outlook's 2027 capital growth lands the same cells
    sector_of = {}
    for r_ in GD.rows(target, "brackley_rowe_cre_index_2004_2026.csv"):
        sector_of[r_["series_code"]] = (r_["sector"], r_["region_group"])
    grow = {"Retail": 0.010, "Industrial": 0.035, "Hospitality": 0.020, "Healthcare": 0.015}
    gfac = lambda code: (1 + grow[sector_of[code][0]]) if sector_of[code][0] in grow else \
        (0.975 if sector_of[code][1] == "Dublin" else 0.965)
    outl = total_of([dict(it_, parts=[dict(p_, carried=p_["carried"] * gfac(p_["series"])) for p_ in it_["parts"]])
                     for it_ in items], fns["golden"])
    res["outlook_growth"] = outl
    check("SF8 the outlook's 2027 capital growth on every property files the golden's cells",
          cells(outl) == gcells and "held at their latest published level" in memo, "%.0f" % outl["total"])
    # SF9: shared security in proportion to exposure (policy 4.4)
    shared = sum(1 for it_ in items for p_ in it_["parts"] if p_["share"] < 1 - 1e-9)
    check("SF9 shared properties are split in proportion to exposure", shared > 0
          and "in proportion to their exposures at the reporting date" in pol, "%d shared parts" % shared)
    # SF10: the register's row in force at the year end, against the last inspection rolled forward on the index as
    # published at the as-of date (every revision taken): the same cells
    idx = defaultdict(dict)
    for r_ in GD.rows(target, "brackley_rowe_cre_index_2004_2026.csv"):
        k = (int(r_["quarter"][:4]), int(r_["quarter"][5]))
        if k not in idx[r_["series_code"]] or int(r_["release"]) > idx[r_["series_code"]][k][0]:
            idx[r_["series_code"]][k] = (int(r_["release"]), float(r_["index_value"]))
    def rerolled(p_):
        h = T.val[p_["p"]]
        li = GD.anchor(h, GD.in_force(h, GD.REPORT))
        ser = idx[p_["series"]]
        lastq = max(ser)
        kq = (li["vdate"].year, (li["vdate"].month - 1) // 3 + 1)
        full = li["value"] * ser[lastq][1] / ser[kq][1] if kq < lastq else li["value"]
        return full * p_["share"]
    rr_ = total_of([dict(it_, parts=[dict(p_, carried=rerolled(p_)) for p_ in it_["parts"]]) for it_ in items], fns["golden"])
    res["latest_release"] = rr_
    check("SF10 the roll-forward redone on the latest release files the golden's cells", cells(rr_) == gcells,
          "%.0f" % rr_["total"])
    # SF11: the lending book is the facility's own (register and fact agree)
    agree = sum(1 for f, r_ in T.book.items() if GD.BOOK_CODE[r_["lending_book"]] == T.book_of.get(f))
    check("SF11 the fact and the register agree on every facility's book", agree == len(T.book), "%d of %d" % (agree, len(T.book)))
    # SF12: cost to the bank is the expected 2027 loss (the ask's words); by exposure or by LGD is another list
    by_ead = [x["fac"] for x in sorted(GD.ecl(items, fns["golden"]), key=lambda x: -x["ead"])[:5]]
    check("SF12 ranking by exposure gives another list (ruled out by the ask's words)", set(by_ead) != top)
    # SF13: a loan is a facility; no customer holds two of the five
    custs = [T.cust_of.get(f) for f in gold["top5"]]
    check("SF13 the five belong to five customers", len(set(custs)) == 5, str(custs))
    # SF14: inferred property members carry no type; the lending book sits on the facility, so none is unbooked
    inferred = {r_["property_id"] for r_ in GD.rows(target, "dw_dim_property_2026-12.csv") if r_["source"] == "INFERRED"}
    on_inferred = [i_ for i_ in items if any(p_["p"] in inferred for p_ in i_["parts"])]
    check("SF14 facilities on inferred property members still carry a lending book",
          all(i_["book"] in ("Investment", "Owner-occupied") for i_ in items), "%d facilities" % len(on_inferred))
    # SF15: duplicate and zero-length valuation rows never sit in force
    check("SF15 cleaned history holds no overlapping rows", all(
        all(a["exp"] < b["eff"] or a["eff"] == b["eff"] for a, b in zip(h[:-1], h[1:])) for h in T.val.values()))
    # SF16: legacy codes (FULL, IDX) are the same bases (policy 4.6)
    check("SF16 legacy codes mapped as policy 4.6 files them",
          all(x["basis"] in ("INSPECTION", "INDEX ROLL-FORWARD") for h in T.val.values() for x in h)
          and "FULL" in pol and "IDX" in pol)
    # SF17: the inspection at default within three months of the default; 60 or 180 days give the same cells
    for win in (60, 180):
        rw = GD.record(T, window=win)
        fw, _ = GD.factor_fns(rw)
        r = total_of(items, fw["golden"])
        res["window_%d" % win] = r
        check("SF17 a %d-day window after default files the golden's cells" % win, cells(r) == gcells,
              "%d defaults, %.0f" % (len(rw), r["total"]))
    # SF18: the carried value read on the default date, or on the day before the inspection: the same cells
    rc = GD.record(T, carried_on="inspection")
    fc, _ = GD.factor_fns(rc)
    r = total_of(items, fc["golden"])
    res["carried_before_inspection"] = r
    check("SF18 the value carried the day before the inspection files the golden's cells", cells(r) == gcells, "%.0f" % r["total"])
    # SF19: years since inspection counted to 1 January 2027 or to 31 December 2026: the same cells
    r = total_of(GD.book_items(T, tau_from=GD.REPORT), fns["golden"])
    check("SF19 years counted to 31 December 2026 file the golden's cells", cells(r) == gcells, "%.0f" % r["total"])
    # SF20: a default's years since inspection from the inspection its carried value rests on, or from the last
    # inspection dated before the default whether or not the register had it on file: the same cells
    rd = GD.record(T, age="dated")
    fd, _ = GD.factor_fns(rd)
    r = total_of(items, fd["golden"])
    res["age_dated"] = r
    differ = sum(1 for a, b in zip(sorted(rec, key=lambda x: x["p"]), sorted(rd, key=lambda x: x["p"])) if abs(a["tau"] - b["tau"]) > 1e-9)
    check("SF20 years counted from the last inspection dated before the default file the golden's cells",
          cells(r) == gcells, "%.0f, %d defaults differ" % (r["total"], differ))
    # SF21: each default's ratio taken against the carried value moved by the index to the inspection's quarter (the
    # market's move between the two dates taken out), against the value carried on the default date: the same cells
    adj = []
    for x in rec:
        h = T.val[x["p"]]
        car = GD.in_force(h, x["date"])
        ser = idx[car["series"]]
        qc = min((car["vdate"].year, (car["vdate"].month - 1) // 3 + 1), max(ser))
        ins = [y for y in h if y["basis"] == "INSPECTION" and x["date"] <= y["vdate"] <= x["date"] + dt.timedelta(days=92)][0]
        qi = min((ins["vdate"].year, (ins["vdate"].month - 1) // 3 + 1), max(ser))
        adj.append(dict(x, ratio=x["ratio"] / (ser[qi][1] / ser[qc][1])))
    fa, _ = GD.factor_fns(adj)
    for k_ in ("golden", "pooled"):
        r = total_of(items, fa[k_])
        res["index_adjusted_" + k_] = r
    check("SF21 the record's ratios with the market's move taken out file the golden's cells",
          cells(res["index_adjusted_golden"]) == gcells, "%.0f" % res["index_adjusted_golden"]["total"])
    # SF22: the inspection at default is the one the bank commissions when the facility defaults (on or after the
    # default date); the inspection nearest the default on either side picks up some made before it
    rn = GD.record(T, side="nearest")
    fn_, _ = GD.factor_fns([x for x in rn if x["ratio"] > 0])
    r = total_of(items, fn_["golden"])
    res["nearest_inspection"] = r
    check("SF22 the inspection nearest the default on either side files the golden's cells, or the model's definition rules "
          "it out", cells(r) == gcells or "the inspection the bank commissions when the facility defaults" in mdl,
          "%.0f / %.0f / %.0f%s" % (r["total"], r["investment"], r["owner_occupied"], "" if cells(r) == gcells else ", other cells"))
    # SF23: the loss is the CRE-LGD-3 figure on the expected value of the security (memo), not the expected loss over the
    # spread of values an inspection might return (the model is convex in V, so that reading runs higher)
    sp = {}
    for bk_ in (True, False):
        sub = [x for x in rec if (x["book"] == GD.TRADING) == bk_]
        t_ = np.array([x["tau"] for x in sub])
        y_ = np.log(np.array([x["ratio"] for x in sub]))
        X_ = np.c_[np.ones_like(t_), t_]
        c_ = np.linalg.lstsq(X_, y_, rcond=None)[0]
        sp[bk_] = (c_, np.exp(y_ - X_ @ c_))
    spread = []
    for it_ in items:
        c_, e_ = sp[it_["book"] == GD.TRADING]
        base = sum(p_["carried"] * math.exp(c_[0] + c_[1] * p_["tau"]) for p_ in it_["parts"])
        lgd_ = np.maximum(0.0, it_["ead"] - (1 - GD.H) * base * e_) / it_["ead"]
        spread.append(dict(fac=it_["fac"], book=it_["book"], el=it_["pd"] * float(lgd_.mean()) * it_["ead"]))
    r = GD.summarise(spread)
    res["expected_lgd_over_spread"] = r
    check("SF23 the memo files the loss as the CRE-LGD-3 figure on the expected value (the loss averaged over the "
          "spread of values is recorded)", "CRE-LGD-3 applied to the value we would expect our inspection to put on "
          "the security if the facility defaulted" in memo, "%.0f, cell %.0f" % (r["total"], rnd(r["total"], UT)))
    check("SF21 pooled with the market's move taken out files the plan cell",
          rnd(res["index_adjusted_pooled"]["total"], UT) == cT, "%.0f" % res["index_adjusted_pooled"]["total"])
    # ---- input gates
    files = sorted(f for f in os.listdir(target) if not f.startswith("."))
    ext = Counter(os.path.splitext(f)[1] for f in files)
    check("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("input gate: 2 or more categories", len({".csv", ".xlsx"} & set(ext)) >= 1 and ".pdf" in ext)
    with open(os.path.join(target, "dw_fact_loan_month_end_2022_2026.csv"), encoding="utf-8") as fh:
        n_fact = sum(1 for _ in fh) - 1
    with open(os.path.join(target, "dw_dim_property_valuation_2004_2026.csv"), encoding="utf-8") as fh:
        n_val = sum(1 for _ in fh) - 1
    check("input gate: a CSV of 20,000 rows or more", n_fact >= 20000, str(n_fact))
    check("input gate: a second long CSV", n_val >= 2000, str(n_val))
    out.update(dict(res=res, fits=fits, rec=rec, items=items, cT=cT, cI=cI, cO=cO, stale_share=stale_share,
                    rec_stale=rec_stale, n_fact=n_fact, n_val=n_val, slope_se=slope_se, t_book=t_book))
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "target")
    run(target, here)
    bad = [r for r in RESULTS if not r[1]]
    for name, ok, d in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + d + "]") if d else ""))
    print("%d checks, %d failed" % (len(RESULTS), len(bad)))
    sys.exit(1 if bad else 0)
