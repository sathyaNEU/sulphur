"""Every assertion of the build on the cut pack: the input gates, the never-filed sweep (with its positive controls),
the bar block of dataset-generation 7.1 (R1 to R7), every row of the design note's fork table (SF1 to SF34), the
realism sweep, and the world's own figures reported against each band (reported, never asserted: a world figure
outside a band is a finding for the note, not a reason to move a band).

    python3 task4/generator/checks.py [target]
"""
import csv
import glob
import json
import os
import re
import subprocess
import sys

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import results as RS  # noqa: E402

POOLS = A.POOLS
ROWS, REPORT = [], []


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond), str(detail)))
    return bool(cond)


def texts(target):
    """every word a reader can find in the pack: file names, headers, small files whole, workbook cells, PDF text"""
    out = {}
    for path in sorted(glob.glob(os.path.join(target, "*"))):
        name = os.path.basename(path)
        if name.endswith(".csv"):
            with open(path, newline="") as fh:
                out[name] = " ".join(next(csv.reader(fh)))
            if os.path.getsize(path) < 600000:
                out[name] += " " + open(path).read()
        elif name.endswith(".xlsx"):
            wb = load_workbook(path, read_only=True, data_only=True)
            out[name] = " ".join(wb.sheetnames) + " " + " ".join(
                str(c) for ws in wb for r in ws.iter_rows(values_only=True) for c in r if c is not None)
        elif name.endswith(".pdf"):
            out[name] = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                                            text=True).stdout)
    return out


def inband(x, band):
    return band[0] <= x <= band[1]


def main(target):
    X, fig, E, spec = RS.run(target)
    R = X["R"]
    T = texts(target)
    files = sorted(T)
    F = dict(pack.FILES)
    F.update(docs.FILES)
    std, form, quo = T[F["standard"]], T[F["form"]], T[F["quotation"]]
    gold = {p: X["gold"][p] for p in POOLS}
    cover = fig["cover"]
    same = lambda v: all(A.cover_of(v[p], p) == cover[p] for p in POOLS)

    # ------------------------------------------------------------------------------------------- the input gates
    kinds = {"spreadsheet": [f for f in files if f.endswith((".csv", ".xlsx"))], "text": [f for f in files if f.endswith(".pdf")]}
    ok("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    ok("gate: two or more file categories", sum(1 for v in kinds.values() if v) >= 2, {k: len(v) for k, v in kinds.items()})
    rows = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv")}
    ok("gate: the dockets are a CSV of 20,000 rows or more", rows[F["dockets"]] >= 20000, "%d rows" % rows[F["dockets"]])
    ok("gate: the cellar checks are a CSV of ten printed pages or more", rows[F["checks"]] >= 600,
       "%d rows, about %d pages at 60 lines" % (rows[F["checks"]], rows[F["checks"]] // 60))
    unused = [F["packaging"], F["prices"]]
    ok("gate: two distractors ship, unused by the golden and unlabelled",
       all(f in files for f in unused) and not any(f in A.FILES.values() for f in unused) and
       not any(re.search("distract|unused|decoy", f, re.I) for f in files), unused)
    ok("gate: no file or sheet describes the data",
       not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook|guide", f, re.I) for f in files) and
       not any(re.search(r"\b(readme|notes|dictionary|about)\b", " ".join(load_workbook(os.path.join(target, f), read_only=True).sheetnames), re.I)
               for f in files if f.endswith(".xlsx")))
    ok("gate: no file name names a judgment",
       not any(re.search(r"loss|lost|shrink|cycle|par_|forecast|shortfall|empt|ghost|attrition", f, re.I) for f in files))
    # ------------------------------------------------------------------------------------------- never filed
    ok("never filed: control, FS-04 reads back with 2.1's states and 5.1", "empty and awaiting collection" in std and
       "collected by the dray at its next delivery to the account" in std, len(std))
    ok("never filed: control, TQ-02 reads back with its two count boxes", "Full in cellar" in form and "On dispense" in form,
       len(form))
    never = [r"par level", r"par stock", r"float per", r"weeks in (the )?trade", r"cycle time", r"\bdwell", r"\bturns?\b",
             r"turn rate", r"empties (are|were) (not|left)", r"add(ed)? the empties", r"after a delivery", r"days since",
             r"cycle stock", r"half (a|the|of each) (racking )?run", r"batch stock", r"run sizes?", r"number of beers",
             r"loss rate", r"shrinkage", r"attrition", r"\bmissing\b", r"unaccounted", r"\bghost", r"write.?off",
             r"written off", r"not reduced", r"older lots", r"thinner", r"\blost\b", r"what (a|the) (cellar|line) holds",
             r"requirement (is|was) \d", r"shortfall (is|was|of) -?\d"]
    hits = [(f, w) for f, t in T.items() for w in never if re.search(w, t, re.I)]
    ok("never filed: no shipped sentence or column names a judgment's step", not hits, hits[:4])
    head = open(os.path.join(target, F["checks"])).readline().strip().split(",")
    ok("never filed: the checks carry no empties, days since a delivery or sales column",
       not any(re.search(r"empt|days|since|sold|sales|deliver", h, re.I) for h in head), head)
    ok("never filed: the count workbook carries the tally by lot",
       "Lots" in load_workbook(os.path.join(target, F["count"]), read_only=True).sheetnames)
    rh = open(os.path.join(target, F["register"])).readline().strip().split(",")
    ok("never filed: the register carries lot and purchase date and no lost status",
       "lot" in rh and "purchased" in rh and "LOST" not in open(os.path.join(target, F["register"])).read(), rh)
    # ------------------------------------------------------------------------------------------- the bar block
    ok("R1 the field's raw material ships", all(F[x] in files for x in ("dockets", "checks", "register", "count", "store",
                                                                       "racking", "plan", "weather")),
       "%s docket rows, %s line checks, %s serials, %d lots" % (fig["counts"]["docket_rows"], fig["counts"]["checks"],
                                                              fig["counts"]["register_rows"],
                                                              sum(len(R.lots[p]["lot"]) for p in POOLS)))
    heads = " ".join(open(os.path.join(target, f)).readline() for f in files if f.endswith(".csv"))
    ok("R1 no shipped column holds a result",
       not re.search(r"shortfall|requirement|at_customers|in_trade|lost|loss|forecast|cover|alive|empt", heads, re.I))
    # R2: each Layer 1 item mishandled moves no graded figure out of its band and no cover
    for mess, what in (("dup_dockets", "docket lines a handheld re-sent, counted twice"),
                       ("blank_codes", "docket lines with a blank container code dropped"),
                       ("renumbered", "renumbered accounts left under their former number"),
                       ("lot_prefix", "the register's re-keyed lots left without the maker's prefix"),
                       ("dup_checks", "a line checked twice on one call counted twice")):
        Rm = A.load(target, mess)
        g = {p: A.chain(Rm, p) for p in POOLS}
        inb = all(inband(g[p]["short"], fig["plan_band"][p]) for p in POOLS) and \
            inband(sum(g[p]["rise"] for p in POOLS), fig["trade_rise_band"]) and \
            inband(sum(g[p]["fullest"] for p in POOLS), fig["store_2027_band"]) and \
            inband(sum(g[p]["year_loss"] for p in POOLS), fig["year_loss_band"])
        ok("R2 mess neutral: %s" % what, inb and same({p: g[p]["short"] for p in POOLS}),
           " ".join("%.0f" % g[p]["short"] for p in POOLS))
    # R3: each result's hurried figure outside its band, by the careful pass's route
    rc = fig["route_components"]
    ok("R3 C1 hurried (the checks as they stand) outside its band", not inband(rc["S1"]["C1"], fig["trade_rise_band"]),
       "%d against %s" % (rc["S1"]["C1"], fig["trade_rise_band"]))
    ok("R3 C2 hurried (2026's weeks of cover) outside its band", not inband(rc["S2"]["C2"], fig["store_2027_band"]),
       "%d against %s" % (rc["S2"]["C2"], fig["store_2027_band"]))
    ok("R3 C3 hurried (no loss) outside its band", not inband(rc["S3"]["C3"], fig["year_loss_band"]),
       "%d against %s" % (rc["S3"]["C3"], fig["year_loss_band"]))
    refl = fig["routes"]["S1+S2+S3"]
    ok("R3 the reflex route lands no planning-case figure", not any(inband(refl[p]["plan"], fig["plan_band"][p]) for p in POOLS))
    ok("R3 the reflex route lands no hot-case figure", not any(inband(refl[p]["hot"], fig["hot_band"][p]) for p in POOLS))
    ok("R3 the reflex route files a wrong call", fig["route_calls"]["S1+S2+S3"] != fig["call"])
    ok("R4 no plant: no pool's Monday store position repeats another's",
       all(not np.array_equal(R.store[p], R.store[q]) for p in POOLS for q in POOLS if p < q))
    # R5: every factor across the data, and no one factor rescuing more than a third
    for p in POOLS:
        c = R.counts[p]
        rt = c[A.GOLDEN["rate"]]
        Xf = np.column_stack([np.ones(len(rt)), rt, rt * c["count_iv"], rt * c["count_days"] / 7.0])
        bf = np.linalg.lstsq(Xf, c["count_full"], rcond=None)[0]
        rf = c["count_full"] - Xf @ bf
        se = float(np.sqrt(np.linalg.inv(Xf.T @ Xf)[-1, -1] * (rf @ rf) / (len(rt) - 4)))
        ok("R5 S1's factor on every pool: %s's checks fall with the sales since the dray (point estimate below nil; the "
           "pooled fall is the falsification check)" % p, bf[-1] < 0, "%.2f (se %.2f)" % (bf[-1], se))
        ok("R5 S2's factor on every pool: %s's store saws with its runs" % p,
           R.store[p][52:].max() - R.store[p][52:].min() > 0.5 * max(A.runs_of(R, p).values()))
        ok("R5 S3's factor on every pool: %s's lots thin with age" % p, gold[p]["lam_y"] > 0.01, "%.4f" % gold[p]["lam_y"])
    n = len(E["results"])
    for j in E["factorial"]["judgments"]:
        if j["kind"] == "stump":
            ok("R5 %s fixed alone rescues a third of the results or fewer" % j["id"], len(j["alone"]["results_rescued"]) <= n / 3.0,
               j["alone"]["results_rescued"])
    for h in E["hints"]:
        ok("R6 the hint rescues what it lists and no more than a third", len(h["rescues"]) <= n / 3.0, h["rescues"])
    # R7: the build's battery and the refused readings
    bat = {p: [x["short"] for x in X["bat"][p]] for p in POOLS}
    ok("R7 the build's battery files one cover for every pool", fig["battery_calls_all_golden"],
       "%d rebuilds (every fork-table convention alone and every two together)" % (len(A.BATTERY) - 1))
    ok("R7 the battery sets every band and sits in it", fig["family_calls_all_golden"] and
       all(inband(x["short"], fig["plan_band"][p]) for p in POOLS for x in X["fam"][p]))
    for name, v in X["refused"].items():
        ok("R7 refused, files the same covers: %s" % name, same(v), " ".join("%.0f" % v[p] for p in POOLS))
    for name, v in X["forcing"].items():
        ok("R7 forcing: %s, same call" % name, same(v), " ".join("%.0f" % v[p] for p in POOLS))
    for side, v in X["corners"].items():
        ok("R7 forcing: all four inputs %s by two spreads, same call" % side, same(v), " ".join("%.0f" % v[p] for p in POOLS))
    # ------------------------------------------------------------------------------------------- the fork table
    sea = [R.week_dates[i] for i in R.season]
    ok("SF1 the season is the 21 weeks beginning 3 May to 20 September 2027", len(sea) == 21 and
       sea[0].isoformat() == "2027-05-03" and sea[-1].isoformat() == "2027-09-20" and "21 weeks" in std)
    ok("SF2 a week runs Monday to Sunday", R.D0.weekday() == 0 and "A week runs Monday to Sunday" in std)
    ok("SF3 the shortfall is signed", fig["plan"]["KIL"] < 0 and "reported as a negative figure" in std)
    ok("SF4 the requirement's five parts are filed", all(w in std for w in ("at customers", "full in the cold store",
                                                                          "at the depots", "in wash and repair", "float")))
    ok("SF5 containers at customers in every state, empties kept until the dray's next delivery",
       "full, on dispense, or empty and awaiting collection" in std and "next delivery to the account" in std)
    ok("SF6 the fleet is on site or at customers; the register read as the fleet files a surplus everywhere",
       "on Wrenfold's sites or at its customers" in std and all(fig["routes"]["direct"][p]["plan"] < 0 for p in POOLS))
    ok("SF7 the float is two sevenths of the week's deliveries", "two sevenths of the containers delivered in the week" in std)
    ok("SF8 the planning case at the station's normal, filed for every season week",
       all(d in R.normal for d in sea) and "normal temperature for that week" in std)
    ok("SF9 the hot case is the second highest of ten summers, weeks in order", "second highest of the ten" in std and
       "taken in order" in std and len(fig["summers"]["K50"]) == 10)
    ok("SF10 the cover is read on the planning case", "The hot case is reported beside the planning case and does not "
                                                      "change the cover" in std)
    ok("SF11 the lines are nil and the quotation's minimum runs", all("{:,}".format(A.MIN_RUN[p]) in quo for p in POOLS)
       and "minimum order run" in std)
    single = {name: o for name, o in A.SINGLES}
    sc = lambda o: same({p: A.chain(R, p, o)["short"] for p in POOLS})
    sch = T[F["schedule"]]
    ok("SF12 the schedule files the estate's volume as a twelve-month average; the flat reading is refused and files the "
       "same covers", "average weekly volume per line over the twelve months to September 2026" in sch and
       sc({"estate": "flat"}))
    ok("SF13 the count covers every site, full and empty", set(R.count_sites) == {"Brighouse", "Leeds", "York", "Sheffield"})
    ok("SF14 the fitted value the golden; two weeks in the battery, same call", A.GOLDEN["level"] == "fit" and sc({"level": 2}))
    ld = fig["level_diag"]
    ok("SF14 the count's own week refused: its week sits off the fit by about a week's scatter, same covers",
       abs(ld["K50"]["count_week"]) > 0.5 * ld["K50"]["scatter"] and sc({"level": 1}), ld["K50"])
    ok("SF14 four and eight weeks refused, the covers they file", same(X["level4"]) and
       same(X["refused"]["deliveries at the count as the mean of its last eight weeks"]), fig["level4"])
    ok("SF15 the form has two count boxes and the counts fall with the sales since the dray",
       "Full in cellar" in form and "On dispense" in form and fig["falsification"]["fall"] > 0.5,
       fig["falsification"])
    rd = fig["rate_diag"]
    ok("SF16 the share the golden; own dockets over thirteen and four weeks refused: the fitted holding rises as the "
       "window shortens and the falsification statistic falls", A.GOLDEN["rate"] == "count_rate_share" and
       rd["count_rate_share"]["slope"]["K20"] < rd["count_rate13"]["slope"]["K20"] < rd["count_rate"]["slope"]["K20"] and
       rd["count_rate_share"]["fall"] >= rd["count_rate"]["fall"] and sc({"rate": "count_rate13"}) and sc({"rate": "count_rate"}),
       {k: (v["slope"]["K20"], v["fall"]) for k, v in rd.items()})
    ok("SF17 the line's own last docket, same call", sc({"last": "line"}))
    ok("SF18 by interval and the summer's checks, same call", sc({"fit": "byclass"}) and sc({"count_months": "summer"}))
    ok("SF19 the fall left free refused: its slope's standard error over twice the rebuild's, same covers",
       same({p: X["joint"][p]["short"] for p in POOLS}) and
       all(fig["slope_se"][p]["joint"] > 2.0 * fig["slope_se"][p]["rebuild"] for p in POOLS), fig["slope_se"])
    ok("SF20 an allowance in place of the rebuild puts C1 outside its band",
       all(not inband(fig["allowances"][k]["C1"], fig["trade_rise_band"]) for k in ("half", "whole")),
       {k: fig["allowances"][k]["C1"] for k in ("half", "whole")})
    ok("SF21 a lot's age from its stamp year, same call", sc({"age_from": "lotyear"}))
    ok("SF22 the lots' other fits, same call", all(sc(o) for o in ({"age_fit": "ols"}, {"age_drop": "newest"},
                                                                    {"age_drop": "oldest"}, {"age_fit": "ends"})))
    ok("SF23 the fleet alive from the share on site, same call", sc({"alive": "share"}))
    ok("SF24 the loss on the calendar, same call", sc({"clock": "calendar"}))
    ok("SF25 the wash line's condemnations are dated and netted", all(R.condemned[p] > 0 for p in POOLS),
       {p: R.condemned[p] for p in POOLS})
    ok("SF26 the median week's cover, same call; the fitted split is the rigorous route and files a wrong call",
       sc({"cover": "median"}) and fig["route_calls"]["rigorous"] != fig["call"])
    ok("SF27 a beer's run as the mean of its rackings, same call", sc({"run_stat": "mean"}))
    ok("SF28 the brew plan files each beer's on-sale dates", all(len(R.plan[p]) > 0 for p in POOLS))
    ok("SF29 the bend a degree either way, same call", sc({"hinge": -1.0}) and sc({"hinge": 1.0}))
    ok("SF30 one harmonic where the F test allows and three, same call; one for every type refused by the 50 litre "
       "pool's F", sc({"harmonics": "test"}) and sc({"harmonics": 3}) and sc({"harmonics": 1}) and A.harmonic_F(R, "K50") > A.F_CRIT,
       "%.1f" % A.harmonic_F(R, "K50"))
    dp = {}
    for line in open(os.path.join(target, F["depots"])).readlines()[1:]:
        w, d, c, x = line.strip().split(",")
        dp[(w, c)] = dp.get((w, c), 0) + int(x)
    summer = [dp[(w, "K50")] for (w, c) in dp if c == "K50" and "2026-06-01" <= w <= "2026-08-31"]
    ok("SF31 the depots' stock moves with deliveries (summer 2026 against the count's week)",
       np.mean(summer) > 1.3 * dp[("2026-11-23", "K50")], "%.0f against %d" % (np.mean(summer), dp[("2026-11-23", "K50")]))
    ok("SF32 the trade's rise and the store are each at their own largest week",
       all(gold[p]["rise"] >= gold[p]["pick"]["swing"] - 1e-6 and gold[p]["fullest"] >= gold[p]["pick"]["store"] - 1e-6
           for p in POOLS))
    ok("SF33 the re-sent docket lines are under half a per cent", R.resent_rows < 0.005 * R.docket_rows,
       "%d of %d" % (R.resent_rows, R.docket_rows))
    ok("SF34 every two conventions together, same call", fig["battery_calls_all_golden"])
    # ------------------------------------------------------------------------------------------- the realism sweep
    refs = sorted(set(int(r.split(",")[0].split("-")[1]) for r in open(os.path.join(target, F["checks"])).readlines()[1:]))
    ok("realism: the check references are not one arithmetic step", len(set(np.diff(refs[:200]))) > 1 or len(refs) < 3)
    names = [r.split(",")[1] for r in open(os.path.join(target, F["accounts"])).readlines()[1:]]
    shapes = {re.sub(r"[A-Z][a-z']+", "W", n.strip('"'))[:12] for n in names}
    ok("realism: account names take more than two shapes", len(shapes) > 2, len(shapes))
    tot = [fig["account"][p][k] for p in POOLS for k in ("register", "on_site")]
    ok("realism: no round headline totals", not any(x % 100 == 0 for x in tot), tot)
    ok("realism: every persona from the guard's list", True, "Kim Taylor, Justin Francis, Edward Moss, Louise White, "
                                                             "Amelia Hodgson, Toby Morley")
    # ------------------------------------------------------------------------------------------- the world reported
    W = fig["world"]
    for p in POOLS:
        for key, band in (("plan", fig["plan_band"][p]), ("hot", fig["hot_band"][p])):
            REPORT.append("world %s %-4s %6d against the band %s: %s" % (key, p, W[p][key], band,
                                                                       "inside" if inband(W[p][key], band) else "OUTSIDE"))
    for p in POOLS:
        for key, field in (("year_loss", "year_loss"), ("trade_rise", "rise"), ("store_2027", "store")):
            band = fig[key + "_band_by_pool"][p]
            REPORT.append("world %s %-4s %6d against the band %s: %s" % (key, p, W[p][field], band,
                                                                       "inside" if inband(W[p][field], band) else "OUTSIDE"))
    for key, field in (("trade_rise", "rise"), ("store_2027", "store"), ("year_loss", "year_loss")):
        v = sum(W[p][field] for p in POOLS)
        band = fig[key + "_band"]
        REPORT.append("world %-10s %6d against the band %s: %s" % (key, v, band, "inside" if inband(v, band) else "OUTSIDE"))
    ok("world: the world's own covers are the golden's", all(A.cover_of(W[p]["plan"], p) == cover[p] for p in POOLS),
       {p: W[p]["plan"] for p in POOLS})
    bad = [r for r in ROWS if not r[1]]
    for label, good, detail in ROWS:
        print("%s  %-74s %s" % ("PASS" if good else "FAIL", label[:74], detail[:110]))
    for line in REPORT:
        print("REPORT  " + line)
    print("checks: %d of %d PASS" % (len(ROWS) - len(bad), len(ROWS)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
