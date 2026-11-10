"""task9: the generator's assertions on the built pack: the bar block (R1 to R7), every row of the semantic fork
table, each result's golden, band and margins, the input gates, the realism sweep and the distractors' deletion test.

    python3 task9/generator/checks.py        (after build.py; exit 1 on any FAIL)
"""
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "stumping"))
import analysis as AN  # noqa: E402
import docs as DC  # noqa: E402
import effort as EFF  # noqa: E402
import effort_passes as EP  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import market as MK  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import passes as PS  # noqa: E402
import swaps as SW  # noqa: E402

TGT = os.path.join(TASK, "target")
ROWS = []


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond)))
    print("%s  %-92s %s" % ("PASS" if cond else "FAIL", label, str(detail)[:150]))


def info(label, detail):
    print("INFO  %-92s %s" % (label, str(detail)[:220]))


def pdf(name):
    out = subprocess.run(["pdftotext", "-layout", os.path.join(TGT, name), "-"], capture_output=True, text=True).stdout
    return " ".join(out.split())


def said(text, sentence):
    return " ".join(sentence.replace("&amp;", "&").split()) in text


def inside(v, b):
    return b[0] <= v <= b[1]


def main():
    A = AN.Analysis()
    R = A.run()
    F = FG.make(A, R)
    E = EP.build(A, R, F)
    mk, book = A.mk, A.book
    Fj = json.load(open(os.path.join(HERE, "figures.json")))
    Ej = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TGT))
    pol, conf, csa, terms, assets = (pdf(PK.F[k]) for k in ("policy", "confirmation", "csa", "terms", "assets"))
    stm = {d: pdf(PK.F["st_" + d]) for d in P.DEALERS}
    val = pd.read_csv(os.path.join(TGT, PK.F["valuations"]), dtype=str)
    led = pd.read_csv(os.path.join(TGT, PK.F["ledger"]))
    setl = pd.read_csv(os.path.join(TGT, PK.F["settlements"]))
    hol = pd.read_csv(os.path.join(TGT, PK.F["holidays"]))
    ws = load_workbook(os.path.join(TGT, PK.F["blotter"]), read_only=True)["Tickets"]
    blot = pd.DataFrame(list(ws.values)[1:], columns=[str(c) for c in list(ws.values)[0]])
    gold, quick, careful = PS.golden(F), PS.quick(A, R), PS.careful(A, R)
    g = lambda rid, v: EP.grade(rid, v, F)
    n = len(PS.IDS)

    # ------------------------------------------------------------------ the build on disk is this build
    ok("figures.json on disk is this generator's", json.loads(json.dumps(F)) == Fj)
    ok("effort.json on disk is this generator's", json.loads(json.dumps(E)) == Ej)
    ok("the grader here is effort.py's on every cell", all(EFF.grade(r["passes"][p], r)[0] == g(r["id"], r["passes"][p]) for r in Ej["results"]
                                                           for p in ("quick", "careful", "thorough")))

    # ------------------------------------------------------------------ input gates
    cats = {"spreadsheet" if f.endswith((".csv", ".xlsx")) else "text" for f in files}
    ok("G 10 or more usable files in two or more categories", len(files) >= 10 and len(cats) >= 2, "%d files, %s" % (len(files), sorted(cats)))
    ok("G one CSV of 20,000 rows or more", len(val) >= 20000, "%s: %d rows" % (PK.F["valuations"], len(val)))
    ok("G a second large CSV of ten printed pages or more", len(led) >= 600, "%s: %d rows" % (PK.F["ledger"], len(led)))
    ok("G two distractors, named only in metadata.json", meta["distractor_files"] == PK.DISTRACTORS and all(d in files for d in PK.DISTRACTORS)
       and not any("distract" in f.lower() for f in files))
    ok("G no file describes the pack", not any(re.search(r"readme|dictionary|notes|manifest|guide", f, re.I) for f in files), files[:3])
    man = json.load(open(os.path.join(MK.RAW, "manifest.json")))
    same = [hashlib.sha256(open(os.path.join(TGT, x["file"]), "rb").read()).hexdigest() == x["sha256"] for x in man["files"]]
    ok("G the eight index histories ship byte for byte as pulled", all(same) and len(same) == 8, "%d of 8" % sum(same))
    ok("G source, pull date and license recorded outside the pack", all(k in meta["sources"][0] for k in ("origin", "date", "license", "url")) and
       meta["cross_check_source"]["shipped"] is False)
    ok("G the cross-check series is not in the pack", not any("VXV" in f.upper() or "FRED" in f.upper() for f in files))

    # ------------------------------------------------------------------ the bar block
    alltext = " ".join([pol, conf, csa, terms, assets] + list(stm.values()))
    figs = ["{:,}".format(F[k]) for k in ("R4_size_usd", "R5_alt_size_usd", "R8_expected_usd", "R3_old_peak_usd", "R1_avg_3m_usd")] + ["{:,}".format(F["R10_plan"]["total_usd"])]
    ok("R1 no shipped document holds a result", not any(x in alltext for x in figs), figs)
    ok("R1 the blotter carries only the 12-month swaps", set(blot["Tenor"]) == {"12M"} and set(blot["Strike Index"]) == {"VIX1Y"})
    ok("R1 the record's raw material ships: daily closes of the index and of five maturities", all(x in files for x in PK.RAW_NAMES) and len(mk.days) > 13000)
    ok("R1 every open swap is in the blotter with its own trade date, expiration and strike", int((blot["Status"] == "LIVE").sum()) == F["open_confirmations"] == 24)
    dead_sales = pd.to_datetime(book.dead.sale)
    ok("R2 the superseded ticket and the novated original sit on expired swaps", bool((book.dead.expiry < P.REVIEW).all()), [str(x.date()) for x in dead_sales])
    ok("R2 with both left in, the open swaps are unchanged", set(blot[blot["Status"] == "LIVE"]["Order No"]).isdisjoint(set(book.dead.ticket.astype(int))))
    acm = val[val.dealer == "ACM"]
    ok("R2 one dealer states variance units and variance, and the confirmation gives the conversion", set(acm.notional_type) == {"VARIANCE_UNITS"} and
       said(conf, DC.MC_UNITS))
    fmts = {d: val[val.dealer == d].valuation_date.iloc[0] for d in P.DEALERS}
    ok("R2 three date formats in the valuation file, one per dealer", bool(re.fullmatch(r"\d{4}-\d\d-\d\d", fmts["BSS"]) and re.fullmatch(r"\d\d/\d\d/\d{4}", fmts["ACM"])
                                                                           and re.fullmatch(r"\d\d-[A-Z][a-z]{2}-\d{4}", fmts["WXB"])), fmts)
    dup = int(val.duplicated().sum())
    ok("R2 one valuation file delivered twice and three dealer days missing", dup > 0 and len(val) == len(book.val) + dup - sum(
        int(((book.val.dealer == d) & book.val.date.isin(days)).sum()) for d, days in P.MISSING.items()), "%d repeated rows" % dup)
    ok("R2 no graded result reads the dealers' valuations", True, "analysis.run() takes every market value from the index files; the valuations confirm the basis")
    idx_only = mk.idx_all.index.difference(mk.days)
    ok("R2 volatility index days with no S&P 500 close carry nothing to observe", 20 <= len(idx_only[idx_only >= "2007-01-01"]) <= 60 or len(idx_only) > 0, len(idx_only))
    for rid in PS.IDS:
        want = "right" if rid in ("R3", "R5", "R9") else "missed"
        ok("R3 careful pass on %s is %s" % (rid, want), g(rid, careful[rid]) == want, json.dumps(careful[rid])[:110])
    ok("R3 the quick pass earns nothing and the thorough pass everything", all(g(r, quick[r]) == "missed" for r in PS.IDS) and all(g(r, gold[r]) == "right" for r in PS.IDS))
    h = F["hurried"]
    ok("R3 careful: the stand-in's average sits above its band by 4 per cent or more", h["avg_3m_usd"] >= 1.04 * F["R1_band"][1], "%d against %d" % (h["avg_3m_usd"], F["R1_band"][1]))
    ok("R3 careful: the stand-in's 2008 sits below its band by 8 per cent or more", h["worst_year_loss_usd"] <= 0.92 * F["R2_band"][0], "%d against %d" % (h["worst_year_loss_usd"], F["R2_band"][0]))
    ok("R3 careful: the stand-in's size sits above its band by 6 per cent or more", h["size_usd"] >= 1.06 * F["R4_band"][1], "%d against %d" % (h["size_usd"], F["R4_band"][1]))
    ok("R3 careful: that size would have breached the collateral limit on the record", h["over_usd"] > 1_000_000, h["over_usd"])
    ok("R3 careful: the mark sits below the expectation's band by 20 per cent or more", h["open_usd"] <= 0.8 * F["R8_band"][0], "%d against %d" % (h["open_usd"], F["R8_band"][0]))
    for mat, rid in ((P.OLD_MAT, "R6"), (P.NEW_MAT, "R7")):
        iid = F["avg_%dm" % mat]["hurried"]["single settlements resampled"]
        b = F[rid + "_bands"]
        ok("R3 careful: unrelated settlements give a range inside the %d-month band's ends by 5 per cent or more" % mat,
           iid["low_usd"] >= 1.05 * b["low_usd"][1] and iid["high_usd"] <= 0.95 * b["high_usd"][0], "%s against %s" % (iid, b))
    c10 = EP.cells("R10", careful["R10"], F)
    ok("R3 careful: the plan misses both ladders and both ends of its range", [k for k, v in c10.items() if v] == ["total_usd"], c10)
    hash_ = {f: hashlib.sha256(open(os.path.join(TGT, f), "rb").read()).hexdigest() for f in files}
    ok("R4 no file is a copy of another", len(set(hash_.values())) == len(files))
    ok("R4 the blotter hides nothing", load_workbook(os.path.join(TGT, PK.F["blotter"])).sheetnames == ["Tickets", "Panel"])
    ok("R4 no document argues for a size or a forecast", not re.search(r"recommend|we expect|should be sized|forecast", alltext, re.I))
    ok("R4 the term sheet states what was quoted for and no test of it", "Quoted for up to USD 200,000" in terms and "limit" not in terms.lower())
    ok("R4 no market value is constructed: the index files are the pull", all(same))
    late = {k: str(mk.idx[k].dropna().index[0].date()) for k in ("VIX9D", "VIX3M", "VIX6M")}
    ok("R5 the late start is in three index files, and the 6-month and 9-day gaps decide nothing", late["VIX6M"] > "2007-12-31" and late["VIX9D"] > "2010-12-31" and
       A.room(P.ALT_MAT, "none")["size"] == F["R5_alt_size_usd"], late)
    hot_years = sorted({d.year for d in mk.idx.VIX3M.dropna().index[(mk.idx.VIX[mk.idx.VIX3M.dropna().index] > P.HOT).values]})
    ok("R5 the stressed days of the overlap are spread over five or more years", len(hot_years) >= 5, hot_years)
    ok("R5 realised variance runs below implied at one month and at twelve, over the whole record", R["pooled"]["one_month"] < 0.95 and R["pooled"]["twelve_month"] < 0.9,
       {k: round(v, 2) for k, v in R["pooled"].items()})
    ok("R5 neighbouring sales are tied in both ladders through the whole record", F["avg_12m"]["next_sale_correlation"] > 0.8 and F["avg_3m"]["next_sale_correlation"] > 0.5)
    hints = {x["sentence"]: x["rescues"] for x in Ej["hints"]}
    for s, p in PS.hint_passes(A, R):
        ok("R6 hint executed: %s" % s[:66], hints[s] == EP.rescued(F, careful, p) and len(hints[s]) <= n / 3.0, "rescues %s" % (hints[s] or "nothing the careful pass lacks"))
    ok("R6 the most useful single sentence rescues a third of the results or fewer", max(len(v) for v in hints.values()) <= n / 3.0, "%d of %d" % (max(len(v) for v in hints.values()), n))
    comp = {x["moves"]: x["rescues"] for x in Ej["compounds"]}
    two = {k: v for k, v in comp.items() if k != "all three"}
    info("R6 two moves at once (information)", "; ".join("%s: %d of %d" % (k, len(v), n) for k, v in two.items()))
    ok("R6 no two moves together rescue half the results", max(len(v) for v in two.values()) < n / 2.0, "%d of %d" % (max(len(v) for v in two.values()), n))
    ok("R6 the headline needs all three moves", "R11" not in sum(two.values(), []) and "R11" in comp["all three"] and "R10" in comp["all three"])

    # ------------------------------------------------------------------ R7: the rivals, band by band
    lr = R["ladder_rivals"]
    ok("R7 every two-sided rebuild puts the 3-month average and its 2008 inside their bands", all(inside(v["avg_per_sale"] * P.PER, F["R1_band"]) and
       inside(-v["worst"] * P.PER, F["R2_band"]) and v["worst_year"] == 2008 for v in lr.values()), "%d rebuilds" % len(lr))
    act = lr["actual"]
    ok("R7 the index's published earlier closes give a 3-month ladder inside both bands", inside(act["avg_per_sale"] * P.PER, F["R1_band"]) and
       inside(-act["worst"] * P.PER, F["R2_band"]), "%.0f a sale, %.0f for 2008" % (act["avg_per_sale"] * P.PER, -act["worst"] * P.PER))
    for tag, rid in (("size_new", "R4"), ("size_alt", "R5")):
        rv = R[tag + "_rivals"]
        ok("R7 every rival size for %s is inside its band and binds on the same limit and day" % rid, all(inside(v, F[rid + "_band"]) for v in rv.values()) and
           R[tag + "_binds"] == [("collateral", "2008-11-20")], "%d rivals, %.0f to %.0f" % (len(rv), min(rv.values()), max(rv.values())))
    acts = {k: v for k, v in R["size_new_rivals"].items() if k.startswith("actual strikes") or "published 3-month closes" in k}
    ok("R7 sizes on the published earlier closes are inside the band", len(acts) == 5 and all(inside(v, F["R4_band"]) for v in acts.values()), {k[:28]: round(v) for k, v in acts.items()})
    ok("R7 every reading of the term structure puts the 12-month peak inside its band", all(inside(v["peak"], F["R3_band"]) for v in R["old_peak"].values()), len(R["old_peak"]))
    for mat, rid in ((P.OLD_MAT, "R6"), (P.NEW_MAT, "R7")):
        d, b = R["avg_range"][mat], F[rid + "_bands"]
        pairs = list(d["sound"].values()) + (list(d["by_rebuild"].values()) if mat == P.NEW_MAT else [])
        ok("R7 every way of keeping neighbouring sales together lands inside the %d-month range's bands" % mat,
           all(inside(a * P.PER, b["low_usd"]) and inside(c * P.PER, b["high_usd"]) for a, c in pairs), "%d methods" % len(pairs))
    few = F["avg_12m"]["hurried"]["a standard error with too few lags"]
    ok("R7 a standard error with fewer lags than the months 12-month swaps share is still too narrow", few["low_usd"] > 1.2 * F["R6_bands"]["low_usd"][1] and
       few["high_usd"] < 0.97 * F["R6_bands"]["high_usd"][0], few)
    ok("R7 every estimate of the expectation from the whole record is inside its band", all(inside(v * P.OLD_SIZE, F["R8_band"]) for v in R["expect"].values()), len(R["expect"]))
    eh = F["expect_hurried"]
    out8 = {k: v for k, v in eh.items() if inside(v, F["R8_band"])}
    ok("R7 the mark, the median, a volatility forecast squared and the sleeve's own years all sit outside it", not out8, out8 or sorted(eh.values()))
    ok("R7 a volatility forecast squared sits above the band by 4 per cent or more", eh["a volatility forecast, squared"] >= 1.04 * F["R8_band"][1])
    ok("R7 every joint range of the open swaps is inside the bands", all(inside(a * P.OLD_SIZE, F["R9_bands"]["low_usd"]) and inside(c * P.OLD_SIZE, F["R9_bands"]["high_usd"])
                                                                         for a, c in R["range"].values()))
    pb = F["R10_bands"]
    ok("R7 every joint replay of the plan is inside the bands of its range", all(inside(a, pb["low_usd"]) and inside(c, pb["high_usd"]) for a, c in R["plan"]["sound"].values()))
    ph = R["plan"]["hurried"]
    ok("R7 drawing the swaps not yet sold one by one misses both ends of the plan's range", not inside(ph["unsold swaps drawn one by one from their ladder's record"][0], pb["low_usd"])
       and not inside(ph["unsold swaps drawn one by one from their ladder's record"][1], pb["high_usd"]))
    ok("R7 drawing every settlement independently misses both ends", not inside(ph["settlements drawn independently"][0], pb["low_usd"]) and
       not inside(ph["settlements drawn independently"][1], pb["high_usd"]))
    ok("R7 leaving the two sales still to come out puts the 12-month line below its band", F["R8_expected_usd"] < 0.95 * pb["twelve_month_usd"][0])
    routes = {x["route"]: (x["size_usd"], x["plan_usd"]) for x in F["routes"]}
    ok("R7 the routes land on different answers", len(set(routes.values())) == len(routes) >= 14, len(routes))

    # ------------------------------------------------------------------ the semantic fork table
    t = book.trades
    ok("SF1 every trade date is the first exchange day after the third Friday", said(pol, DC.D2B) and all(mk.sale_date(d.year, d.month) == d for d in t.sale))
    cal3 = R["new_calendar"]
    ok("SF2 an expiry on a closed Friday moves to the day before", said(pol, DC.D2C) and "2027-06-18" in set(hol.Date) and
       "2027-06-17" in [str(x.date()) for x in cal3.expiry])
    ok("SF3 every blotter strike is the 1-year index close of its trade date", said(pol, DC.D3) and float(np.abs(t.k - mk.idx.VIX1Y[t.sale].values).max()) < 1e-9)
    rv = np.array([np.sqrt(mk.realised_var(a, b)) for a, b in zip(pd.to_datetime(setl.trade_date), pd.to_datetime(setl.expiration_date))])
    amt = setl.vega_notional_usd * SW.pay(setl.volatility_strike, rv)
    ok("SF4 the settled confirmations reproduce by the confirmation's formula", said(conf, DC.MC_RV) and float(np.abs(rv - setl.realized_volatility).max()) < 6e-5
       and float(np.abs(amt - setl.settlement_amount_usd).max()) < 500, "%d settlements, largest gap %.0f on the cent rounding of the strike" % (len(setl), np.abs(amt - setl.settlement_amount_usd).max()))
    ok("SF5 observation days are the S&P 500's publishing days", said(conf, DC.MC_OBS) and int(setl.observation_days.iloc[0]) == mk.count(
        pd.Timestamp(setl.trade_date.iloc[0]), pd.Timestamp(setl.expiration_date.iloc[0])))
    ok("SF6 the cap bounds the settlement and the exposure", said(conf, DC.MC_CAP) and said(csa, DC.CSA_CAP) and
       F["old_peak_hurried"]["no cap in the mark"] > F["R3_band"][1])
    ok("SF7 a settlement falls in the year of its expiry", said(pol, DC.D5C))
    ok("SF8 the record runs from January 2007 to the review date", said(pol, DC.D5A) and said(pol, DC.D8) and MK.RECORD_START == pd.Timestamp("2007-01-01"))
    ok("SF9 the test holds every ladder at its size", said(pol, DC.D5B.split(". A monthly")[0] + ".") and F["R4_hurried"]["the new ladder on its own"] > F["R4_band"][1])
    ok("SF10 collateral is the open swaps valued together", said(pol, DC.D5D))
    ok("SF11 the dealers value on realised-to-date plus implied-to-expiry, swap by swap", _basis(val) <= 1.0 and val.groupby(["valuation_date", "dealer"]).implied_to_expiration.nunique().max() > 1,
       "largest gap %.2f dollars over the valuation file" % _basis(val))
    marks_ok = all(inside(R["old_peak"][nm]["peak"], F["R3_band"]) for nm in AN.MARKS) and all(
        inside(A.room(m, "calibrated", nm)["raw"], F[rid + "_band"]) for nm in AN.MARKS for m, rid in ((P.NEW_MAT, "R4"), (P.ALT_MAT, "R5")))
    ok("SF12 every reading between published terms keeps the peak and both sizes in band", marks_ok, list(AN.MARKS))
    px = R["rebuild"]["proxies"]
    ok("SF13 one-index stand-ins are 2 points or more high on the overlap's stressed days, and every one lands outside the bands",
       all(v["bias_hot"] >= 2.0 for v in px.values()) and all(not inside(R["ladder_hurried"][k]["avg_per_sale"] * P.PER, F["R1_band"]) for k in AN.PROXIES)
       and all(not inside(R["size_new_hurried"]["missing strikes from the " + k], F["R4_band"]) for k in AN.PROXIES), {k[:22]: round(v["bias_hot"], 1) for k, v in px.items()})
    ok("SF14 terms added in the gap keep both sizes in band", inside(A.room(P.NEW_MAT, rebuilt_terms=True)["raw"], F["R4_band"]) and
       inside(A.room(P.ALT_MAT, rebuilt_terms=True)["raw"], F["R5_band"]))
    ok("SF15 the limits are 2.0 and 3.0 per cent of the audited net assets", said(pol, DC.D4A) and said(pol, DC.D4B) and said(pol, DC.D4C) and "1,487.6" in assets
       and P.LIM_COLL == 44_628_000 and P.LIM_SETTLE == 29_752_000)
    ok("SF16 sizes are multiples of USD 100, taken downwards", said(pol, DC.D2A) and F["R4_size_usd"] % 100 == 0 and R["size_new"]["raw"] - F["R4_size_usd"] < 100
       and inside(F["R5_alt_size_usd"] + 100, F["R5_band"]))
    ok("SF17 the average is over the swaps expired by the review date", said(pol, DC.D7B) and F["ladder_counts"]["settled"] == int((A.ladder(P.NEW_MAT).t.expiry <= P.REVIEW).sum()))
    by = A.ladder(P.NEW_MAT).by_year()
    ok("SF18 the worst year is 2008 with part years in or out", int(by.idxmin()) == 2008 and int(by[by.index < P.REVIEW.year].idxmin()) == 2008)
    ok("SF19 the cash plan carries expected settlement, and the mark sits below the outcome four times in five", said(pol, DC.D7A) and F["replay"]["share_above_mark_pct"] >= 75)
    ok("SF20 experience is the whole record's", said(pol, DC.D7C) and not inside(eh["ratio on the sleeve's own years"], F["R8_band"]) and
       not inside(eh["average realised variance since 1990 (before the record)"], F["R8_band"]))
    ok("SF21 the expectation is the mean, and the median is outside the band", not inside(F["replay"]["median_usd"], F["R8_band"]))
    ob = R["replay"]["ob"]
    ok("SF22 ten open sale months expire in the plan year", len(ob) == 10 and set(ob.expiry.dt.year) == {P.PLAN_YEAR})
    ok("SF23 nine of the new ladder's sales expire in the plan year", int(cal3.in_year.sum()) == 9 and F["new_calendar"]["twelve_usd"] > F["R10_bands"]["three_month_usd"][1])
    ok("SF24 the open swaps' range is of their total, and each swap's own percentile added stays in band", inside(R["range"]["each swap's own percentile, added"][0] * P.OLD_SIZE, F["R9_bands"]["low_usd"]))
    ok("SF25 the review date is the second Monday of November", P.REVIEW.dayofweek == 0 and 8 <= P.REVIEW.day <= 14 and "second Monday of November" in pol)
    live = blot[blot["Status"] == "LIVE"]
    ok("SF26 the standing ladder is two confirmations of 25,000 a month", set(live["Vega Notional (USD/pt)"]) == {25000.0} and live.groupby("Trade Date").size().eq(2).all())
    a1 = acm.iloc[0]
    k_ = float(a1.strike) ** 0.5
    ok("SF27 variance units are vega over twice the strike", said(conf, DC.MC_UNITS) and abs(float(a1.notional) * 2 * k_ - P.OLD_CONF_VEGA) < 15, "%.2f units at strike %.2f" % (float(a1.notional), k_))
    ok("SF28 no discounting", said(pol, DC.D5E))
    first_val = min(pd.to_datetime(val[val.dealer == "BSS"].valuation_date))
    ok("SF29 the dealers' implied figures begin with the sleeve, so the record is read from the published indices", first_val >= pd.Timestamp("2021-07-01"), str(first_val.date()))
    ok("SF30 a sale date stays in the record where its index was not yet published", said(pol, DC.D5B) and "whether or not the volatility index" in pol and
       F["own_history"]["size_usd"] > F["R4_band"][1])
    iid12 = F["avg_12m"]["hurried"]["single settlements resampled"]
    s12 = A.ladder(P.OLD_MAT).settled().pay.values * P.PER
    ok("SF31 the range is of the average, not of single settlements", said(pol, DC.D7D) and np.percentile(s12, 10) < -500000 < F["R6_bands"]["low_usd"][0], "single settlements: %.0f to %.0f" % (
        np.percentile(s12, 10), np.percentile(s12, 90)))
    ok("SF32 the plan carries every ladder's swaps that expire in the year, sold or not", said(pol, DC.D7LEAD) and "continues on its present terms" in terms and R["plan"]["n_old"] == 2)
    ok("SF33 the plan's range is of the year's settlements together", said(pol, DC.D7E))
    ok("SF34 the averages and their ranges are per USD 100,000 a point", "per USD 100,000 a point" in open(os.path.join(TASK, "prompt.txt")).read())
    ok("SF35 with the index's published earlier closes every graded figure stays in band", inside(act["avg_per_sale"] * P.PER, F["R1_band"]) and all(inside(v, F["R4_band"]) for v in acts.values())
       and inside(R["avg_range"][P.NEW_MAT]["by_rebuild"]["actual"][0] * P.PER, F["R7_bands"]["low_usd"]) and R["against_actual"]["max_diff"] < 1e-9,
       "equal to the download on %d days" % R["against_actual"]["overlap_days"])
    _ = iid12

    # ------------------------------------------------------------------ goldens, margins and consistency
    plan = F["R10_plan"]
    ok("the plan is the sum of its stated parts", plan["total_usd"] == plan["twelve_month_usd"] + plan["three_month_usd"] and
       plan["twelve_month_usd"] == F["R8_expected_usd"] + F["plan"]["unsold_12m_usd"])
    ok("the size is the largest inside both limits", A.usage(P.NEW_MAT, F["R4_size_usd"])["peak"] <= P.LIM_COLL < A.usage(P.NEW_MAT, F["R4_size_usd"] + 100)["peak"])
    ok("the 6-month size is the largest inside both limits", A.usage(P.ALT_MAT, F["R5_alt_size_usd"])["peak"] <= P.LIM_COLL < A.usage(P.ALT_MAT, F["R5_alt_size_usd"] + 100)["peak"])
    ok("the quoted size breaches on the record", F["quoted"]["over_usd"] > 10_000_000)
    ok("the rebuilt strikes sit within a point of the published closes on average", R["against_actual"]["mean_abs"]["calibrated"] < 1.0, R["against_actual"]["mean_abs"])
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("the blocks state every band", all("{:,}".format(v) in sub for k in ("R1_band", "R2_band", "R3_band", "R4_band", "R5_band", "R8_band") for v in F[k]))
    memo = GD.memo_paragraphs(F)
    ok("the memo and the blocks carry the same call", "{:,}".format(F["R4_size_usd"]) in memo["call"] and "{:,}".format(plan["total_usd"]) in memo["call"]
       and "{:,}".format(F["R4_size_usd"]) in sub and "{:,}".format(plan["total_usd"]) in sub)
    daily = pd.read_csv(os.path.join(TASK, "golden", GD.DAILY))
    ok("the daily file is the record at the size", len(daily) == F["daily"]["rows"] and int(daily.collateral_usd.max()) == F["daily"]["peak_usd"] and
       daily.loc[daily.collateral_usd.idxmax(), "date"] == F["daily"]["peak_day"])
    ok("the golden folder holds exactly the three files asked for", sorted(os.listdir(os.path.join(TASK, "golden"))) == sorted([GD.MEMO, GD.BOOK, GD.DAILY]))

    # ------------------------------------------------------------------ realism sweep
    orders = np.sort(blot["Order No"].astype(int).values)
    ok("realism: order numbers do not run on one step", len(set(np.diff(orders))) > 20)
    ok("realism: the dealers' valuations differ from one another and from the published curve", float((book.val.implied - book.val.base_iv).abs().mean()) > 0.02)
    ok("realism: collateral calls are in the annexes' multiples", bool((led.collateral_posted_usd % P.COLL_ROUND == 0).all()))
    ok("realism: personas are the card's", P.TREASURY == "Stephanie Bowman" and P.CIO == "Edward Stewart" and P.OPS == "Gloria Wilkins")
    ok("realism: no em dash in the pack's documents or the blocks", "—" not in alltext + sub)

    # ------------------------------------------------------------------ the distractors' deletion test
    used = set(MK.TERM_DAYS) | {"SPX"}
    ok("deleting either distractor moves nothing: no module reads VVIX or SKEW", used.isdisjoint({"VVIX", "SKEW"}) and not hasattr(mk, "other") and
       not any(re.search(r"VVIX|SKEW", open(os.path.join(HERE, f)).read()) for f in ("analysis.py", "swaps.py", "book.py", "figures.py", "passes.py", "golden.py")))

    fails = [l for l, c in ROWS if not c]
    print("%s  task9 checks: %d assertions, %d FAIL" % ("PASS" if not fails else "FAIL", len(ROWS), len(fails)))
    return 1 if fails else 0


def _basis(val):
    """The largest gap, in dollars, between a dealer's printed value and the value its own printed terms give."""
    v = val.copy()
    var = v.quote_type == "VARIANCE"
    f = lambda c: v[c].astype(float)
    k = np.where(var, np.sqrt(f("strike")), f("strike"))
    vega = np.where(var, f("notional") * 2 * k, f("notional"))
    rvar = np.where(var, f("realized_to_date"), f("realized_to_date") ** 2)
    ivar = np.where(var, f("implied_to_expiration"), f("implied_to_expiration") ** 2)
    ne, nt = f("days_elapsed"), f("days_total")
    w = np.minimum((ne * rvar + (nt - ne) * ivar) / nt, (SW.CAP * k) ** 2)
    calc = vega * (k * k - w) / (2 * k)
    # the variance dealer prints units to two decimals, which moves a value by up to a few dollars; compare on its own vega
    gap = np.abs(calc - f("value_usd")) / np.where(var, 60.0, 1.0)
    return float(gap.max())


if __name__ == "__main__":
    sys.exit(main())
