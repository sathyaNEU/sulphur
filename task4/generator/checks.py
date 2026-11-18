"""Every assertion of the build on the cut pack: the input gates, the bar block (R1 to R7), every row of the fork
table (SF1 to SF45), the pinning list read from the shipped documents' own text, the pack against the world's records,
the second implementation, and the realism sweep.

    python3 task4/generator/checks.py [target]
"""
import csv
import glob
import json
import os
import re
import sqlite3
import subprocess
import sys

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import analysis as A  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import results as RS  # noqa: E402
import verify as V  # noqa: E402

POOLS = A.POOLS
ROWS = []


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond), str(detail)))
    return bool(cond)


def texts(target):
    """every word a reader can find in the pack: file names, headers, small files, workbook cells, PDF text, schema"""
    out = {}
    for path in sorted(glob.glob(os.path.join(target, "*"))):
        name = os.path.basename(path)
        if name.endswith(".csv"):
            with open(path, newline="") as fh:
                out[name] = " ".join(next(csv.reader(fh)))
            if os.path.getsize(path) < 400000:
                out[name] += " " + open(path).read()
        elif name.endswith(".xlsx"):
            wb = load_workbook(path, read_only=True, data_only=True)
            out[name] = " ".join(wb.sheetnames) + " " + " ".join(str(c) for ws in wb for r in ws.iter_rows(values_only=True) for c in r if c is not None)
        elif name.endswith(".pdf"):
            out[name] = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        elif name.endswith(".sqlite"):
            con = sqlite3.connect(path)
            out[name] = " ".join(r[0] or "" for r in con.execute("SELECT sql FROM sqlite_master"))
            con.close()
    return out


def main(target):
    X, fig, E, spec = RS.run(target)
    R, WD = X["R"], X["WD"]
    T = texts(target)
    files = sorted(T)
    std = re.sub(r"\s+", " ", T[docs.FILES["standard"]])
    quo = T[docs.FILES["quotation"]]
    hire = re.sub(r"\s+", " ", T[docs.FILES["hire"]])
    gold = {p: X["gold"][p]["short"] for p in POOLS}
    hot = {p: X["hot"][p][0] for p in POOLS}
    names = [n for n, _ in A.FAMILY]
    n1 = len(A.SINGLES)
    fam = {p: np.array([x["short"] for x in X["fam"][p]]) for p in POOLS}
    hfam = {p: np.array(X["hot_fam"][p]) for p in POOLS}
    cover = {p: A.cover_of(gold[p], p) for p in POOLS}
    lat, hlat = X["lat"], X["hot_lat"]

    def single(*keys):
        """indices of the battery's single conventions that change exactly these option keys"""
        return [1 + i for i, (_, o) in enumerate(A.SINGLES) if set(o) == set(keys) or (len(keys) == 1 and keys[0] in o)]

    def held(idx):
        """the variants at these indices file the golden's covers and land every ask figure in its stated band"""
        good = True
        for i in idx:
            for p in POOLS:
                good &= A.cover_of(fam[p][i], p) == cover[p]
                good &= fig["plan_band"][p][0] <= round(fam[p][i]) <= fig["plan_band"][p][1]
                good &= fig["hot_band"][p][0] <= round(hfam[p][i]) <= fig["hot_band"][p][1]
        return good and len(idx) > 0

    def refused(name):
        return all(A.cover_of(X["refused"][name][p], p) == cover[p] for p in POOLS)

    # ------------------------------------------------------------------------------------------- the input gates
    kinds = {"spreadsheet": [f for f in files if f.endswith((".csv", ".xlsx"))], "database": [f for f in files if f.endswith(".sqlite")],
             "text": [f for f in files if f.endswith(".pdf")]}
    ok("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    ok("gate: two or more file categories", sum(1 for v in kinds.values() if v) >= 2, {k: len(v) for k, v in kinds.items()})
    rows = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv")}
    ok("gate: a CSV of 20,000 rows or more", max(rows.values()) >= 20000, "largest %d rows" % max(rows.values()))
    ok("gate: a second large CSV of ten printed pages or more", sum(1 for v in rows.values() if v >= 600) >= 2,
       "%d CSVs of 600 rows or more" % sum(1 for v in rows.values() if v >= 600))
    unused = [pack.FILES["packaging"], docs.FILES["prices"]]
    ok("gate: two distractors ship, unused and unlabelled", all(f in files for f in unused) and
       not any(f in A.FILES.values() for f in unused) and not any(re.search("distract|unused|decoy", f, re.I) for f in files))
    ok("gate: no file or sheet describes the data",
       not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook|guide", f, re.I) for f in files) and
       not any(re.search(r"\b(readme|notes|dictionary|about)\b", " ".join(load_workbook(os.path.join(target, f), read_only=True).sheetnames), re.I)
               for f in files if f.endswith(".xlsx")))
    ok("gate: no file name names a judgment", not any(re.search(r"loss|lost|shrink|cycle|fixed|par_|forecast|shortfall", f, re.I) for f in files))
    never = [r"cycle stock", r"safety stock", r"half (a|the|of each) (racking )?run", r"weeks of cover", r"in step with", r"proportion",
             r"whatever it sells", r"par level", r"par stock", r"loss rate", r"shrinkage", r"stock account", r"off site", r"regress",
             r"\bbend\b", r"hinge", r"degree.day", r"reconcil", r"calibrat", r"which record", r"not on the register"]
    hits = [(f, w) for f, t in T.items() for w in never if re.search(w, t, re.I)]
    ok("never filed: no shipped word names a judgment's step", not hits, hits[:4])
    heads = " ".join(T[f].split("\n")[0] for f in files if f.endswith(".csv"))
    ok("R1 no shipped column holds a result", not re.search(r"shortfall|requirement|at_customers|in_trade|lost|loss|forecast|cover", heads, re.I), heads[:0])
    ok("R1 the field's raw material ships", all(pack.FILES[k] in files for k in ("dockets", "register", "stocktake", "store", "racking", "audits", "tags", "weather")),
       "%s docket rows, %s serials, four counts, %s line counts, %s tag reads" % (
           format(fig["counts"]["docket_rows"], ","), format(fig["counts"]["register_rows"], ","),
           format(fig["counts"]["audit_rows"], ","), format(fig["tags"]["reads"], ",")))

    # --------------------------------------------------------------- the pinning list, in the documents' own text
    for label, pat in (
            ("SF4 the requirement's parts (2.1)", r"at customers, full in the cold store, at the depots, and in wash and repair \(empties awaiting wash are counted under wash\)"),
            ("SF6 the float is two sevenths of the week's deliveries (2.1)", r"a float of two sevenths of the containers delivered in the week"),
            ("SF5 the fleet is on Wrenfold's sites or at its customers (2.2)", r"on Wrenfold's sites or at its customers in that week"),
            ("SF3 the shortfall is signed, with no purchase and no hire after the count (2.3)", r"requirement less the fleet, taken with no purchase and no hire after the annual count\. A negative shortfall is a surplus and is reported as a negative figure"),
            ("SF1 the season is the 21 weeks from the first Monday of May (3.1)", r"21 weeks from the week beginning on the first Monday of May.*Monday 3 May 2027 to Monday 20 September 2027"),
            ("SF2 a week runs Monday to Sunday (3.1)", r"A week runs Monday to Sunday"),
            ("SF7 the planning case is every week at the station's normal (3.2)", r"largest weekly shortfall in the season, with every week taken at the Calder Vale weather station's normal temperature for that week"),
            ("SF8 the hot case is the second highest of the ten summers 2017 to 2026 (3.3)", r"2017 to 2026\).*the hot case is the second highest of the ten"),
            ("SF31 each summer's 21 season weeks are taken in order, every other week at its normal (3.3)", r"each summer's 21 season weeks taken in order and every other week at its normal"),
            ("the season as contracted and planned (3.4)", r"accounts supplied and those under a signed supply agreement, and the range and the brew plan as issued"),
            ("SF9 the cover is read on the planning case (4.1)", r"The cover for a container type is read on the planning case.*does not change the cover"),
            ("SF10 the lines: nil, and the maker's minimum order run (4.1)", r"nil or negative, no cover is put in place\. Where it is above nil and below the maker's minimum order run for the type, it is covered by a seasonal hire\. Where it is the minimum order run or more, it is covered by a purchase"),
            ("the minimum order run comes from the quotation in force (4.2)", r"taken from the maker's quotation in force at the review")):
        ok("pinned in the standard: " + label, re.search(pat, std), pat[:60])
    runs = {}
    for line in quo.splitlines():
        m = re.match(r"\s*(\d)\s+\S.*?\d+\.\d\d\s+([\d,]+)\s+\d+\s*$", line)
        if m:
            runs[POOLS[int(m.group(1)) - 1]] = int(m.group(2).replace(",", ""))
    ok("SF10 the quotation's text gives the five minimum order runs the golden uses", runs == A.MIN_RUN, runs)
    ok("SF10 no variant of the battery comes within 150 containers of a line",
       min(min(abs(v), abs(v - A.MIN_RUN[p])) for p in POOLS for v in fam[p]) >= 150,
       "nearest %.0f" % min(min(abs(v), abs(v - A.MIN_RUN[p])) for p in POOLS for v in fam[p]))
    ok("pinned: the hire has no upper limit on a booking", "no upper limit on a booking" in hire)
    ok("the golden uses no constant of the core or the world",
       not re.search(r"^\s*(import|from) (core|world)\b", open(os.path.join(HERE, "analysis.py")).read(), re.M) and
       not re.search(r"^\s*(import|from) (core|world|analysis)\b", open(os.path.join(HERE, "verify.py")).read(), re.M))
    ok("pinned in the files: the schedule's lines and volumes and the plan's runs are the core's",
       all(sum(n for _, n in R.estate[p]) == C.W[p]["estate"][0] and abs(R.estate_volume[p] - C.W[p]["estate"][1]) < 1e-9 for p in ("K50", "K30", "K20", "FIR")) and
       all(sorted(set(r for _s, _a, _b, r in R.plan[p])) == sorted(set([q26 for _c, _sh, q26, _q in C.W[p]["beers"]] + [q for _c, _sh, _q26, q in C.W[p]["beers"]] + [q for _c, q in C.W[p]["new27"]])) for p in POOLS))

    # --------------------------------------------------------------- the pack against the world's own records
    for p in POOLS:
        P = WD.pools[p]
        ok("pack against world: %s's weekly deliveries from the dockets are the world's, week for week" % p,
           np.array_equal(np.rint(R.flow[p]).astype(int), np.rint(P.D).astype(int)), "largest gap %.0f" % np.abs(R.flow[p] - P.D).max())
        ok("pack against world: %s's Monday store position is the world's" % p, np.array_equal(R.store[p][1:], P.store[1:len(R.store[p])]))
        g = X["gold"][p]
        ok("truth anchor: %s's containers alive at customers at the count within 5 per cent of the world's" % p,
           abs(g["alive_out"] / float(P.trade[R.WH]) - 1.0) < 0.05, "%.0f against %.0f" % (g["alive_out"], P.trade[R.WH]))
        ok("truth anchor: %s's loss per container delivered within a fifth of the world's" % p,
           abs(g["lam"] / C.W[p]["loss"] - 1.0) < 0.20, "%.4f against %.4f" % (g["lam"], C.W[p]["loss"]))
        ok("truth anchor: %s's fixed stock a line within a fifth of the world's" % p, abs(g["a"] / C.W[p]["a"] - 1.0) < 0.20,
           "%.2f against %.2f" % (g["a"], C.W[p]["a"]))
        ok("truth anchor: %s's store cover within a tenth of the world's" % p, abs(g["cov"] / C.W[p]["cover"] - 1.0) < 0.10,
           "%.3f against %.3f" % (g["cov"], C.W[p]["cover"]))
        ok("golden against truth: %s's planning and hot figures of the world sit inside the stated bands" % p,
           fig["plan_band"][p][0] <= fig["truth"][p] <= fig["plan_band"][p][1] and fig["hot_band"][p][0] <= fig["truth_hot"][p] <= fig["hot_band"][p][1],
           "truth %d and %d" % (fig["truth"][p], fig["truth_hot"][p]))
    ok("golden files the truth's covers", all(A.cover_of(fig["truth"][p], p) == cover[p] for p in POOLS), cover)
    ok("the cut pack re-proves the core at level 5", fig["rubric"]["level"] == 5 and not fig["rubric"]["fails"], fig["rubric"]["fails"])
    ok("rubric: a run that loses one stump earns 50 or under", max(fig["rubric"]["one_lost"].values()) <= 50, fig["rubric"]["one_lost"])
    ok("rubric: the reflex route earns 30 or under", fig["rubric"]["reflex"] <= 30, fig["rubric"]["reflex"])
    v, bad = V.main(target)
    ok("verify: the independent rebuild files the same covers and lands every stated figure in its band", bad == 0, "%d outside" % bad)

    # ------------------------------------------------------------------------------------ the bar block, R3 to R7
    rc = fig["route_components"]
    ok("R3 R2's hurried figure (stock at customers in step with deliveries) is outside the band by half or more",
       rc["S1"]["C1"] > 1.5 * fig["trade_rise_band"][1], "%s against %s" % (rc["S1"]["C1"], fig["trade_rise_band"]))
    ok("R3 R4's hurried figure (the store at last summer's weeks of cover) is outside the band", rc["S2"]["C2"] < 0.8 * fig["store_2027_band"][0],
       "%s against %s" % (rc["S2"]["C2"], fig["store_2027_band"]))
    ok("R3 R3's hurried figure (the tagged kegs' loss rate) is outside the band", rc["S3"]["C3"] < 0.5 * fig["year_loss_band"][0],
       "%s against %s" % (rc["S3"]["C3"], fig["year_loss_band"]))
    for s, m in (("S1", "K50"), ("S2", "K20"), ("S3", "FIR")):
        ok("R3 %s dropped alone moves %s across its line" % (s, m), A.cover_of(lat[m][s]["short"], m) != cover[m],
           "%.0f files %s against %s" % (lat[m][s]["short"], A.cover_of(lat[m][s]["short"], m), cover[m]))
        alone = RS.ALONE[s]
        ok("R3 %s fixed alone on the reflex route still misses the covers" % s,
           any(A.cover_of(lat[p][alone]["short"], p) != cover[p] for p in POOLS))
        others = [p for p in POOLS if A.cover_of(lat[p][s]["short"], p) == cover[p] and
                  not fig["plan_band"][p][0] <= round(lat[p][s]["short"]) <= fig["plan_band"][p][1]]
        ok("R5 %s lost misleads where it decides nothing too: a type whose cover stays has its figure outside the band" % s,
           len(others) >= 1, others)
    calls = {k: tuple(A.cover_of(lat[p][k]["short"], p) for p in POOLS) for k in lat["K50"]}
    ok("R3 the shortcuts land on different wrong covers", len({calls[s] for s in ("S1", "S2", "S3")}) == 3 and
       all(calls[s] != tuple(cover[p] for p in POOLS) for s in ("S1", "S2", "S3", RS.REFLEX)), {s: calls[s] for s in ("S1", "S2", "S3")})
    ok("R3 the direct and the rigorous standard routes miss the covers",
       any(A.cover_of(X["direct"][p], p) != cover[p] for p in POOLS) and any(A.cover_of(X["rigorous"][p]["short"], p) != cover[p] for p in POOLS))
    ok("R4 no week of deliveries repeats across the five types", len({tuple(int(R.flow[p][i]) for p in POOLS) for i in range(R.WH)}) == R.WH)
    ok("R4 no shipped file sizes or ranks the fleets (Gate G)",
       not any(re.search(r"shortfall|requirement", t, re.I) for f, t in T.items() if f != docs.FILES["standard"]))
    ok("R4 no memo, draft or stakeholder figure ships", not any(re.search(r"memo|draft|review_20|proposal", f, re.I) for f in files))
    Pp = fig["pool"]
    ok("R5 every type's lines hold a fixed stock: the fitted constant is 1.5 containers or more in all five",
       all(Pp[p]["fixed_per_line"] >= 1.5 for p in POOLS), {p: Pp[p]["fixed_per_line"] for p in POOLS})
    ok("R5 every type's store stands on its racking runs: raw weeks of cover differ across the types while the cover beside half the runs agrees",
       max(fig["store_weeks"].values()) - min(fig["store_weeks"].values()) > 0.3 and
       max(Pp[p]["store_cover_weeks"] for p in POOLS) - min(Pp[p]["store_cover_weeks"] for p in POOLS) < 0.03, fig["store_weeks"])
    ok("R5 every type without tags loses at 2.5 times the tagged kegs' rate or more", all(Pp[p]["loss_pct"] >= 2.5 * fig["tags"]["loss_pct"] for p in RS.UNTAGGED),
       {p: Pp[p]["loss_pct"] for p in RS.UNTAGGED})
    ok("R6 the hint rescues a third or fewer", all(len(h["rescues"]) <= len(E["results"]) / 3.0 for h in E["hints"]),
       [len(h["rescues"]) for h in E["hints"]])
    ok("R7 the battery: every variant files the golden's covers", all(A.cover_of(fam[p][i], p) == cover[p] for p in POOLS for i in range(len(names))),
       "%d variants" % len(names))
    ok("R7 the battery: every variant's every figure sits inside the stated band", held(range(len(names))))
    ok("R7 forcing: each fitted input moved, and all four together by two measured spreads, leaves the covers",
       all(A.cover_of(v[p], p) == cover[p] for v in list(X["forcing"].values()) + list(X["corners"].values()) for p in POOLS))
    ok("R7 the refused readings file the golden's covers all the same", all(refused(n) for n in X["refused"]), list(X["refused"]))

    # ------------------------------------------------------------------------------------ the fork table, row by row
    season = X["season"]
    rf0 = fig["referee"]
    ok("SF1 the season's weeks are those the standard names", R.week_dates[season[0]].isoformat() == "2027-05-03" and
       R.week_dates[season[-1]].isoformat() == "2027-09-20" and len(season) == 21)
    ok("SF2 every docket week and store position falls on the standard's Monday week", all(d.weekday() == 0 for d in R.week_dates[:R.WH]))
    ok("SF3 the kilderkins' figure is filed as a negative shortfall", gold["KIL"] < 0 and fig["plan"]["KIL"] < 0)
    ok("SF5 the register read as the fleet is the direct route and lands off the covers",
       any(A.cover_of(X["direct"][p], p) != cover[p] for p in POOLS), {p: round(X["direct"][p]) for p in POOLS})
    ok("SF7 the station's normal covers every week of the 2027 season", all(R.week_dates[i] in R.normal for i in season))
    ten = {p: X["hot"][p][1] for p in POOLS}
    ok("SF8 the second highest of ten is one summer's figure, not an interpolation", all(len(ten[p]) == 10 and abs(hot[p] - sorted(ten[p])[-2]) < 1e-9 for p in POOLS))
    ok("SF9 the hot case puts the 50 litre kegs above their minimum order run and the cover stays a hire (4.1)",
       hot["K50"] > A.MIN_RUN["K50"] and cover["K50"] == "hire", "%.0f against %d" % (hot["K50"], A.MIN_RUN["K50"]))
    ok("SF11 every estate outlet is listed before the season opens, and the scheduled volume level through the year is in the battery",
       all(d <= R.week_dates[season[0]] for p in POOLS for d, _n in R.estate[p]) and held(single("estate")))
    wb = load_workbook(os.path.join(target, pack.FILES["stocktake"]), read_only=True)
    ok("SF12 the count has one sheet a year and counts every site, full and empty", len(wb.sheetnames) == 4 and
       all(re.search(r"Brighouse", T[pack.FILES["stocktake"]]) for _ in [0]) and re.search(r"empty", T[pack.FILES["stocktake"]], re.I))
    lv = fig["levels"]["K50"]
    ok("SF13 deliveries at a count: the one, two and four weeks before it are in the battery", held(single("level")) and len(single("level")) == 3)
    ok("SF13 the eight and thirteen weeks before the count stand 10 per cent or more above its own week for 50 litre kegs and are refused; the covers stay",
       lv["eight_over_fit_pct"] >= 10 and lv["thirteen_over_fit_pct"] >= 20 and refused("deliveries at each count as the eight weeks before it") and
       refused("deliveries at each count as the thirteen weeks before it"), "%s and %s per cent" % (lv["eight_over_fit_pct"], lv["thirteen_over_fit_pct"]))
    ok("SF14 the loss over two and three years of the account, and without the customers' own change, are in the battery",
       held(single("loss_years") + single("trade_change")) and len(single("loss_years")) == 2)
    ok("SF15 the tagged kegs' loss from the stock account and on the year to the count are in the battery",
       held(single("account_tagged") + single("tag_window")))
    head = T[pack.FILES["audits"]].split("\n")[0]
    ok("SF16 the cellar audit counts full, on dispense and empty in separate columns", all(c in head for c in ("full", "on_dispense", "empty")))
    ok("SF17 the code table maps the dockets', the register's and the store's codes to the five types",
       all(c in T[pack.FILES["codes"]] for c in ("docket_code", "register_code")) and len(R.flow) == 5)
    ok("SF18 a beer's run as the mean of its rackings is in the battery and moves no figure by more than 5 containers",
       held(single("run_stat")) and max(abs(fam[p][single("run_stat")[0]] - gold[p]) for p in POOLS) <= 5)
    ok("SF19 the brew plan gives each beer's on-sale dates by container type", all(len(R.plan[p]) >= 2 for p in POOLS))
    ts = X["tests"]
    ok("SF20 the bend: a degree either way, kept by its F statistic, and a quadratic in its place are in the battery",
       held(single("hinge") + single("bend")) and len(single("hinge")) == 2 and len(single("bend")) == 2)
    ok("SF20 a single slope for every type is refused by the 50 litre kegs' F statistic of 20 or more; the covers stay",
       ts["K50"]["bend_F"] >= 20 and refused("a single slope in the weather response"), "F %.1f" % ts["K50"]["bend_F"])
    ok("SF21 the trend kept by its t statistic and the trend not carried past the count are in the battery", held(single("trend") + single("ahead")))
    ok("SF21 no trend for any type is refused by t statistics of 3 or more on three types; the covers stay",
       sum(1 for p in POOLS if abs(ts[p]["trend_t"]) >= 3) >= 3 and refused("no trend in the deliveries fit for any type"),
       {p: round(ts[p]["trend_t"], 1) for p in POOLS})
    sp = fig["split"]
    ok("SF22 the store's split fitted on the 104 Mondays agrees with half the runs within one standard error for every type and is in the battery",
       all(sp[p]["within_se"] <= 1.0 for p in POOLS) and held(single("split")), {p: sp[p]["within_se"] for p in POOLS})
    ok("SF22 the split fitted on 52 Mondays alone has the wider standard error on every type and is refused; the covers stay",
       all(sp[p]["se_52"] > sp[p]["se_104"] for p in POOLS) and refused("the store's stock split fitted on the last year's Mondays alone"))
    ok("SF22 the store's cover as the median week's, on the last year's Mondays and on all three years' are in the battery",
       held(single("cover") + single("cover_weeks")) and len([i for i in single("cover_weeks") if "split" not in A.FAMILY[i][1]]) == 2)
    ok("SF42 the fitted split stands within one standard error of the racking log's half runs for every type on 104 Mondays only: on 52 "
       "kilderkins and on 156 firkins and 50 litre kegs stand further off; both windows are refused in either form, the covers stay",
       all(sp[p]["errors_104"] <= 1.0 for p in POOLS) and sp["KIL"]["errors_52"] > 1.0 and sp["FIR"]["errors_156"] > 1.0 and
       sp["K50"]["errors_156"] > 1.0 and
       max(sp["FIR"]["cover_by_year"]) - min(sp["FIR"]["cover_by_year"]) <= 0.05 and
       abs(sp["FIR"]["fixed_156"] - sp["FIR"]["fixed_52"]) >= 100 and
       refused("the store's stock split fitted on all three years' Mondays") and
       refused("the fitted slope beside half the plan's runs, on all three years' Mondays") and
       refused("the fitted slope beside half the plan's runs, on the last year's Mondays alone"),
       {p: (sp[p]["errors_52"], sp[p]["errors_104"], sp[p]["errors_156"]) for p in POOLS})
    ok("SF23 condemned containers leave the fleet: over one year or three in the battery; left out is refused by the register's own count; the covers stay",
       held(single("scrap_years")) and all(fig["pool"][p]["condemned_last_year"] > 0 for p in POOLS) and
       refused("containers condemned at the wash after the count left out"))
    ok("SF24 depots, wash and repair at the last count, the depots from their weekly stock, and the backlog and the bay from the wash log, are in the battery",
       held(single("other")) and len(single("other")) == 3)
    ok("SF25 one and three seasonal harmonics are in the battery", held(single("harmonics")) and len(single("harmonics")) == 2)
    ok("SF26 a line's weekly sales from the fit, from four weeks, or on the last year's share are in the battery",
       held(single("rate") + single("share")) and len(single("rate")) == 4)
    ok("SF27 the cellar counts fitted apart by delivery interval, and on the summer's counts, are in the battery",
       held(single("fit") + single("count_months")))
    ok("SF28 the tagged kegs' stock at customers from their tags, scaled or not, and their response from the tags' rise, are in the battery",
       held(single("census")) and len(single("census")) == 3)
    ok("SF29 every two conventions together: the crossed battery holds the covers and the bands",
       len(names) >= 1 + n1 + 400 and held(range(1 + n1, len(names))), "%d crosses" % (len(names) - 1 - n1))
    c = fig["counts"]
    ok("SF30 a docket line sent twice is counted once: the re-sent rows are under half a per cent of the file", 0 < c["resent_rows"] < 0.005 * c["docket_rows"],
       "%d of %d" % (c["resent_rows"], c["docket_rows"]))
    ok("SF31 each summer gives 21 recorded weeks from its own first Monday of May",
       all(len(A.summer_temps(R, y)) == 21 for y in A.SUMMERS))
    ok("SF32 the harmonics on a 52 week year are in the battery and move no planning figure by more than 25 containers",
       held(single("period")) and max(abs(fam[p][single("period")[0]] - gold[p]) for p in POOLS) <= 25)
    ok("SF33 the first count's deliveries from the fit carried back a week are in the battery and move no planning figure by more than 25 containers",
       held(single("first")) and max(abs(fam[p][single("first")[0]] - gold[p]) for p in POOLS) <= 25)
    pg = fig["pairing"]["K50"]
    ok("SF34 a Monday position goes with the week ended: set against the week beginning the 50 litre kegs' fit loses a quarter of its R squared "
       "and its fixed part stands two standard errors above the racking log's half runs; refused, the covers stay",
       pg["r2_ended"] - pg["r2_beginning"] >= 0.25 and pg["fixed_beginning"] - sp["K50"]["half_runs"] >= 2 * pg["se_beginning"] and
       refused("the store's stock split fitted with each Monday set against the week beginning"), pg)
    ok("SF35 the fitted slope kept as the cover beside half the plan's runs is in the battery", held(single("split")) and len(single("split")) == 2)
    ok("SF36 the estate's season at the normal in the hot case is in the battery and leaves the planning case where it is",
       held(single("estate_temp")) and max(abs(fam[p][single("estate_temp")[0]] - gold[p]) for p in POOLS) < 1e-6)
    ok("SF37 the loss and the condemnations counted to the end of the week before are in the battery", held(single("accrue")))
    tg = fig["tags"]
    ok("SF38 the tags' count: with the not traced kegs left in, or unscaled, the rise stays within a fifth of the stated one and far from stock in step with deliveries",
       all(abs(x - rf0["seen"]) <= 0.2 * rf0["seen"] for x in (tg["rise_lost_in"], tg["rise_unscaled"])) and rf0["proportional"] > 5 * tg["rise_lost_in"],
       "%s, %s and %s" % (rf0["seen"], tg["rise_lost_in"], tg["rise_unscaled"]))
    od = fig["own_dockets"]
    ok("SF39 a line's own dockets: the fitted response rises with the window for every type, four weeks leaves the tagged kegs' rise under half "
       "the tags' count and is refused, thirteen weeks is in the battery; the covers stay",
       all(od["per_sale"]["1"][p] < od["per_sale"]["4"][p] < od["per_sale"]["13"][p] for p in POOLS) and od["rise"]["4"] < 0.5 * rf0["seen"] and
       refused("a line's sales from its own dockets over the four weeks to the count") and
       any(A.FAMILY[i][1].get("rate") == "own13" for i in single("rate")), od["rise"])
    ap = fig["apart"]["K50"]
    ok("SF40 a line's level and its movement apart, on four weeks of deliveries, is in the battery and on the count's week is refused; for 50 litre kegs its movement slope rises by 0.1 or more from the count's "
       "week to four weeks of deliveries while the level slope moves by under 0.05",
       held(single("fit")) and len(single("fit")) == 2 and ap["four"]["move"] - ap["week"]["move"] >= 0.1 and
       abs(ap["four"]["level"] - ap["week"]["level"]) < 0.05 and
       refused("the cellar counts fitted with a line's level and its movement apart, on the count's week"), ap)
    wl = fig["wash_log"]
    def moved(p, key):
        """a stock's rise from the count to the busiest weeks of summer 2026, over the rise in the type's deliveries"""
        return (wl[p][key + "_peak"] / float(wl[p][key + "_count"]) - 1.0) / (wl[p]["deliveries_peak"] / float(wl[p]["deliveries_count"]) - 1.0)

    ok("SF41 the wash line and the repair bay move with the season: by the wash log the 50 litre kegs' backlog and repair bay stand half as high "
       "again or more in the busiest weeks as at the count, and each keg type's rise by half its deliveries' rise or more; held at the count's "
       "level is refused, the covers stay",
       all(wl["K50"][k + "_peak"] >= 1.5 * wl["K50"][k + "_count"] for k in ("awaiting", "repair")) and
       all(moved(p, k) >= 0.5 for p in ("K50", "K30", "K20") for k in ("awaiting", "repair")) and
       refused("the wash line and the repair bay held at the last count's level"),
       {p: (round(moved(p, "awaiting"), 2), round(moved(p, "repair"), 2)) for p in ("K50", "K30", "K20")})
    ok("SF41 the wash log's repair balance is the counts' containers in repair, and its last backlog before a count is the count's",
       all(wl[p]["repair_at_counts"] == wl[p]["repair_counted"] and wl[p]["awaiting_count"] == wl[p]["awaiting_counted"] for p in POOLS),
       {p: (wl[p]["repair_at_counts"], wl[p]["repair_counted"]) for p in POOLS})

    fc = fig["first_count"]
    ok("SF43 the account starts clear at the first count: off site then stands within 2 per cent of the stock the cellar relation gives, every type",
       all(abs(fc[p]["gap_pct"]) <= 2.0 for p in POOLS), {p: fc[p]["gap_pct"] for p in POOLS})
    tg = fig["tags"]
    ok("SF44 the tags' count is still filling in its first months: a week after the first read it stands under a fifth of its level at the count of "
       "December 2024, and the count is used from that count on",
       tg["fill"][0][1] < 0.2 * rf0["start"] and tg["fill"][-1][1] > 0.9 * rf0["start"], tg["fill"])
    ok("SF45 the tagged kegs' measured response is stated both ways and both stand under a fifth: over the rise to summer 2026 and by a line "
       "through the last 104 weekly counts", 0 < tg["share_pct"] < 20 and 0 < tg["line_pct"] < 20, (tg["share_pct"], tg["line_pct"]))

    # ------------------------------------------------------------------------------- the referee and the realism sweep
    rf = rf0
    ok("referee: the line relation reproduces the tags' count of the rise and stock in step with deliveries misses by five times as much or more",
       abs(rf["proportional"] - rf["seen"]) >= 5 * abs(rf["golden"] - rf["seen"]), "%s seen, %s golden, %s in step" % (rf["seen"], rf["golden"], rf["proportional"]))
    ok("referee: no ask figure is the tags' own count", rf["seen"] not in list(fig["plan"].values()) + list(fig["hot"].values()))
    wash = {}
    with open(os.path.join(target, pack.FILES["wash"]), newline="") as fh:
        rd = csv.DictReader(fh)
        ok("control: the wash log carries no count of containers washed (no record of returning empties by type ships)",
           not any(re.search(r"washed|returned|received|throughput", c) for c in rd.fieldnames), rd.fieldnames)
        for r in rd:
            wash[r["container"]] = wash.get(r["container"], 0) + int(r["condemned"])
    wash = {p: wash[pack.CODE["register"][p]] for p in POOLS}
    ok("control: the wash log's condemnations agree with the register's within a tenth for every type, and never exceed them",
       all(0.9 * R.condemned_all[p] <= wash[p] <= R.condemned_all[p] for p in POOLS), "%s against %s" % (wash, R.condemned_all))
    ok("realism: the weather response differs by type (bends from %.1f to %.1f degrees)" % (min(Pp[p]["bend_c"] for p in POOLS), max(Pp[p]["bend_c"] for p in POOLS)),
       len({Pp[p]["bend_c"] for p in POOLS}) >= 3)
    ok("realism: the loss rate differs across the types without tags", len({Pp[p]["loss_pct"] for p in RS.UNTAGGED}) == 4)
    ok("realism: the tags miss some deliveries (read share under 100 per cent)", 90 < fig["tags"]["read_share_pct"] < 100, fig["tags"]["read_share_pct"])
    ok("realism: weekly deliveries scatter about the fitted season", fig["levels"]["K50"]["weekly_scatter_pct"] >= 2, fig["levels"]["K50"]["weekly_scatter_pct"])
    ok("stated: every band in the blocks holds its golden figure", all(fig["plan_band"][p][0] <= fig["plan"][p] <= fig["plan_band"][p][1] and
                                                                         fig["hot_band"][p][0] <= fig["hot"][p] <= fig["hot_band"][p][1] for p in POOLS))
    sub = os.path.join(os.path.dirname(HERE), "submission.md")
    if os.path.exists(sub):
        ok("no em dash in the answer blocks", "—" not in open(sub).read())
    bad = [r for r in ROWS if not r[1]]
    for label, good, detail in ROWS:
        if not good or "--all" in sys.argv:
            print("%s  %s  %s" % ("PASS" if good else "FAIL", label, detail[:160]))
    print("checks: %d of %d pass" % (len(ROWS) - len(bad), len(ROWS)))
    return len(bad)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(1 if main(args[0] if args else os.path.join(os.path.dirname(HERE), "target")) else 0)
