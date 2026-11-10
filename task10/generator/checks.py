"""task10 architecture 6: the generator's assertions, on the cut pack (target/) and on the clean truth.
python3 task10/generator/checks.py

Every semantic fork row of the design note (SF1 to SF17) is asserted by its id; then the results chain result by
result (the golden against the clean truth, every variant inside its band, the margins), the bar block (the hidden
factor record's footprint across the data, the hurried route's misreadings and where they decide, the rivals ruled
out by named data, the one-fact test computed), Layer 1 neutrality, the input gates, realism and the containers."""
import json
import math
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import build as B          # noqa: E402
import effort_passes as EP  # noqa: E402
import estim as E          # noqa: E402
import golden as GO        # noqa: E402
import pack as PK          # noqa: E402
import parse as PA         # noqa: E402
import world as W          # noqa: E402

CALL = ["Ashcombe Road", "Fenwick Street", "Hartwell Common"]
RESULTS = []
KEYS = (("before", "before"), ("delivered", "delivered"), ("off_peak", "off_peak"), ("peak", "peak"), ("p90", "one_in_ten"))


def check(cid, ok, detail):
    RESULTS.append((cid, bool(ok), detail))
    print("%-4s %-34s %s" % ("PASS" if ok else "FAIL", cid, detail))


def fresh():
    return E.conform(PA.load(TARGET))


def clean_truth():
    """The world before any mess or document, as the analyst's tables, the registers' facts taken from the world."""
    T = W.build()
    ct = W.tables(T)
    X = dict(demand=ct["demand"], events=ct["events"], weather=ct["weather"], switching=ct["switching"],
             names={p["code"]: p["name"] for p in W.PRIMARIES},
             rates={p["code"]: PK.dfes_rates(p["key"]) for p in W.PRIMARIES},
             growth={p["code"]: W.REGISTER_MW[p["key"]] for p in W.PRIMARIES},
             firm={p["code"]: p["firm"] for p in W.PRIMARIES},
             contracts={W.BY[z["key"]]["name"]: z["mw28"] for z in W.ZONES},
             previous={W.BY[z["key"]]["name"]: dict(z["mw"]) for z in W.ZONES})
    return T, E.conform(X)


def inside(G, F, pad=0.0):
    """Every banded figure of a run inside the golden's band."""
    out = []
    for z in G["zones"]:
        for k, bk in KEYS:
            lo, hi = F["bands"][bk][z["primary"]]
            if not (lo - pad <= round(z[k], 2) <= hi + pad):
                out.append("%s %s %.2f not in %.1f to %.1f" % (z["primary"], bk, z[k], lo, hi))
    return out


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    X = fresh()
    G = E.golden_from(X)
    Z = {z["primary"]: z for z in G["zones"]}
    T, XT = clean_truth()
    GT = E.golden_from(XT)
    guide = subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, PK.F_GUIDE), "-"], capture_output=True, text=True).stdout
    award = subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, PK.F_AWARD), "-"], capture_output=True, text=True).stdout
    gflat, aflat = " ".join(guide.split()).replace("- ", "-"), " ".join(award.split()).replace("- ", "-")

    # ------------------------------------------------------------------------------------------------ the call
    check("call", G["commit"] == CALL, "reinforce %s" % ", ".join(G["commit"]))
    check("call on the clean truth", GT["commit"] == CALL and not inside(GT, F, 0.15),
          "the same set and every figure within 0.15 MW of its band on the world before any mess: %s" % (inside(GT, F, 0.15) or "all"))

    # ------------------------------------------------------------------------------------------------ the family and the bands
    FAM = B.family(X, G)
    bad = {k: inside(v, F) for k, v in FAM.items() if inside(v, F)}
    check("bands hold every variant", not bad and all(v["commit"] == CALL for v in FAM.values()),
          "%d variants (%s): every figure inside its band, the same three primaries" % (len(FAM) - 1, ", ".join(k for k in FAM if k != "golden")))
    widths = {bk: max(F["bands"][bk][p][1] - F["bands"][bk][p][0] for p in Z) for _, bk in KEYS}
    C0 = EP.careful(X, G)
    gap = {"megawatts delivered, Ashcombe Road": C0["Ashcombe Road"]["delivered"] - F["bands"]["delivered"]["Ashcombe Road"][1],
           "megawatts delivered, Charlecote Way": C0["Charlecote Way"]["delivered"] - F["bands"]["delivered"]["Charlecote Way"][1],
           "expected peak, Ashcombe Road": F["bands"]["peak"]["Ashcombe Road"][0] - C0["Ashcombe Road"]["peak"],
           "expected peak, Charlecote Way": F["bands"]["peak"]["Charlecote Way"][0] - C0["Charlecote Way"]["peak"],
           "nine days in ten, Ashcombe Road": F["bands"]["one_in_ten"]["Ashcombe Road"][0] - C0["Ashcombe Road"]["one_in_ten"],
           "nine days in ten, Charlecote Way": F["bands"]["one_in_ten"]["Charlecote Way"][0] - C0["Charlecote Way"]["one_in_ten"],
           "nine days in ten, Fenwick Street": F["bands"]["one_in_ten"]["Fenwick Street"][0] - C0["Fenwick Street"]["one_in_ten"]}
    check("the hurried figures sit outside the bands", min(gap.values()) >= 0.25,
          "the hurried pass's figure lies outside the band by %s MW; the widest band by result is %s MW"
          % (", ".join("%.1f (%s)" % (v, k) for k, v in gap.items()), {k: round(v, 1) for k, v in widths.items()}))
    fen, cha = [v for v in FAM.values()], None
    fmin = min(z["p90"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] == "Fenwick Street")
    fexp = max(z["peak"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] == "Fenwick Street")
    cmax = max(z["p90"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] == "Charlecote Way")
    amin = min(z["p90"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] in ("Ashcombe Road", "Hartwell Common"))
    check("margins", fmin >= 0.3 and fexp <= -0.05 and cmax <= -0.4 and amin >= 2.0,
          "across the variants Fenwick Street's one-in-ten level is at least %.2f MW over firm and its expected peak at least "
          "%.2f under; Charlecote Way at least %.2f inside; Ashcombe Road and Hartwell Common at least %.2f over"
          % (fmin, -fexp, -cmax, amin))

    # ------------------------------------------------------------------------------------------------ semantic forks
    check("SF1 the design day", "working weekday" in gflat and "minus 3.0 degrees Celsius" in gflat and "GMT day" in gflat,
          "guideline 2: a working weekday at a daily mean of minus 3.0 C, the mean of the hourly readings for the GMT day")
    v = E.golden_from(X, use_switching=False)
    VZ = {z["primary"]: z for z in v["zones"]}
    shift = {p: VZ[p]["before"] - Z[p]["before"] for p in Z}
    check("SF2 the days behind the before-demand",
          "outside the days on which flexibility was scheduled" in gflat and "switching log shows load transferred" in gflat
          and v["commit"] == CALL and max(abs(s) for s in shift.values()) <= 0.6,
          "guideline 3 files the days; with the %d logged transfers' days left in, the same three primaries, and the demand before "
          "flexibility moves by %s MW" % (len(X["switching"]), ", ".join("%+.2f at %s" % (s, p) for p, s in shift.items())))
    check("SF3 growth", "compounded" in gflat and "added in full" in gflat and "in the proportion its highest half-hour grows" in gflat,
          "guideline 4: DFES rates compounded, qualifying connections in full, every half-hour in the peak's proportion")
    v = E.golden_from(X, credit="lower")
    check("SF4 the megawatts delivered", "quoted as its delivery in the half-hours ending 17:30 and 18:00" in gflat and not inside(v, F) and v["commit"] == CALL,
          "guideline 6: the half-hours ending 17:30 and 18:00; the lower of the two for the mean moves no figure out of its band")
    v = E.golden_from(X, credit="last")
    check("SF4 the half-hour ending 18:00 alone", not inside(v, F) and v["commit"] == CALL,
          "the megawatts of the half-hour ending 18:00 alone for the two half-hours' mean (the prompt's 17:30 to 18:00 read as "
          "one half-hour): the same set, every figure inside its band")
    v = E.golden_from(X, window="flat")
    check("SF23 the megawatts through the window", not inside(v, F) and v["commit"] == CALL,
          "the megawatts quoted taken flat through every half-hour of the window, for the reduction each half-hour of the "
          "events shows: the same set, every figure inside its band")
    check("SF5 the call in full", "scheduled in full for the service window" in gflat, "guideline 6: the megawatts contracted scheduled in full")
    check("SF6 demand with flexibility", "its highest half-hourly demand on that day with the service delivered through its window" in gflat
          and "No flexibility other than the contracted service is credited" in gflat,
          "guideline 6: the day's highest half-hour, whichever it is, with the service delivered through its window; the two "
          "half-hours are how a contract's megawatts are quoted, not the extent of the credit")
    qs = []
    for z in G["zones"]:
        f = G["providers"][z["provider"]]
        d = z["delivered"]
        slope = (f["back"].get(z["peak_hh"], 0.0) - f["shape"].get(z["peak_hh"], 0.0))
        sd = math.sqrt((slope * f["cv"] * d) ** 2 + (z["cv_base"] * z["profile"][z["peak_hh"]]) ** 2)
        qs.append((z["primary"], z["peak"] + E.Z90 * sd, z["p90"]))
    check("SF7 one design day in ten", "on more than one design day in ten" in gflat and all(abs(a - b) <= 0.25 for _, a, b in qs),
          "guideline 7; the normal reading at the peaking half-hour sits within 0.25 MW of the day recomputed half-hour by half-hour (%s)"
          % ", ".join("%s %.2f against %.2f" % q for q in qs))
    check("SF8 the megawatts contracted", "registered capacity of the assets" in aflat and all(
        X["contract"][(W.BY[z["key"]]["code"], w)] == z["mw"][w] for z in W.ZONES for w in z["mw"]),
        "the award notice's table of the three winters, read as written; contracted megawatts are registered capacity")
    for sid, name, keys in (("SF9 the cold days", "taken at or below 0, minus 1.5 or minus 2 C", ("days at or below 0 C", "days at or below minus 1.5 C", "days at or below minus 2 C")),
                            ("SF10 the line", "a curved line", ("a curved line",)),
                            ("SF11 provider or zone", "each zone on its own", ("zone by zone",)),
                            ("SF12 the scatter", "the scatter as measured, or the share's own scatter as measured times the "
                             "award (pooled or zone by zone)",
                             ("the scatter as measured", "the share's own scatter as measured, times the award",
                              "the share's own scatter as measured, times the award, zone by zone")),
                            ("SF13 the heating base", "14 or 17 C", ("heating base 14 C", "heating base 17 C")),
                            ("SF18 the baseline behind an event", "a heating slope each winter, weekday levels, or the baseline "
                             "scaled to the day's own level before the window",
                             ("a heating slope each winter", "weekday levels", "the baseline scaled to the day's own level before the window")),
                            ("SF19 a call that was met", "left out, or taken as a floor (over the cold days, the days at or below "
                             "2 C or every day, on a straight or a curved line)",
                             ("the calls that fell short alone", "the calls that fell short alone, every day",
                              "met calls as floors, days at or below 2 C", "met calls as floors, every day",
                              "met calls as floors, every day, a curved line", "megawatts fitted over every event",
                              "megawatts fitted over every event, zone by zone")),
                            ("SF20 a cancelled instruction's day", "kept among the days behind the baselines",
                             ("a cancelled instruction's day kept",)),
                            ("SF22 the record's own scaling", "megawatts delivered carried to the award at the rate the three "
                             "winters' record gives for each per cent contracted",
                             ("the three winters' own scaling with the megawatts contracted",))):
        b = [inside(FAM[k], F) for k in keys]
        check(sid, not any(b) and all(FAM[k]["commit"] == CALL for k in keys), "%s: same set, every figure inside its band" % name)
    Y = fresh()
    raw = pd.read_csv(os.path.join(TARGET, PK.F_EVENTS), dtype=str)
    first = raw[raw["revision"] == "1"]
    first_mw = {(r.primary_asset, r.service_date): float(r.scheduled_mw) for r in first.itertuples()}
    ev = Y["events"].copy()
    ev["scheduled_mw"] = [first_mw.get((r.zone, r.date.strftime("%d/%m/%Y")), r.scheduled_mw) if r.status == "Completed" else r.scheduled_mw
                          for r in ev.itertuples()]
    Y["events"] = ev
    v = E.golden_from(Y)
    nrev = int((raw["revision"] == "2").sum())
    check("SF14 the instruction's revision", not inside(v, F) and v["commit"] == CALL,
          "%d instructions carry a second row; the megawatts first issued for the latest move no figure out of its band" % nrev)
    maes = F["family"]["mae"]
    check("SF15 the backtest", F["backtest"]["n"] == int(sum((G["events"][c]["winter"] == E.TEST_WINTER).sum() for c in E.ZONES))
          and F["bands"]["backtest"]["mae"][0] <= min(maes.values()) and max(maes.values()) <= F["bands"]["backtest"]["mae"][1],
          "winter 2025/26's completed events from winters 2023/24 and 2024/25 (the prompt): the average miss runs from %.2f to "
          "%.2f MW across the %d variants (the baseline scaled to the day's own level lowest, a curved line highest), inside "
          "the stated %.2f to %.2f" % (min(maes.values()), max(maes.values()), len(maes) - 1, F["bands"]["backtest"]["mae"][0],
                                       F["bands"]["backtest"]["mae"][1]))
    cb = F["careful_backtest"]
    check("R3 the hurried reading's own backtest", F["bands"]["backtest"]["mae"][0] <= cb["mae"] <= F["bands"]["backtest"]["mae"][1],
          "megawatts per megawatt scheduled is out by %.2f MW on the same held-out winter, inside the band: the backtest does "
          "not tell the readings apart, so the careful column earns it; the freezing-day count inside an 80 per cent range "
          "runs from %d to %d of %d across the variants and six constructions of the range (the workbook's context, not graded)"
          % (cb["mae"], F["bands"]["backtest"]["inside"][0], F["bands"]["backtest"]["inside"][1], F["backtest"]["n_cold"]))
    le = F["r1_evidence"]["by_primary"]
    others = F["r1_evidence"]["unscheduled_primaries_curve_t"]
    check("SF21 the weather correction's line",
          all(abs(v["line_miss_pct"]) <= 1.2 and abs(v["curve_miss_mw"]) > abs(v["line_miss_mw"]) and abs(v["peak_curve_t"]) < 2.0
              for v in le.values()) and all(abs(t) < 2.0 for t in others.values()) and len(others) == 5,
          "the guideline's 2025/26 sample is %s days no colder than %s C; in the hours before the window the straight line "
          "fitted on such days lands the days at or below 0 C within %s MW and a curve misses them by %s MW; the curve's t on "
          "the daily peak is %s in those samples and %s at the five primaries with nothing scheduled, whose days reach minus 5 C"
          % ("/".join(str(v["sample_days"]) for v in le.values()), "/".join("%+.1f" % v["coldest_c"] for v in le.values()),
             "/".join("%+.2f" % v["line_miss_mw"] for v in le.values()), "/".join("%+.2f" % v["curve_miss_mw"] for v in le.values()),
             "/".join("%+.1f" % v["peak_curve_t"] for v in le.values()), "/".join("%+.1f" % t for t in others.values())))
    sc = F["scaling"]
    check("SF22 megawatts that do not grow", abs(sc["elasticity"] - 1.0) <= 2 * sc["standard_error"] and
          sc["elasticity"] >= 5 * sc["standard_error"] and "registered capacity of the assets" in aflat,
          "over the three winters' %d cold-day calls that fell short, megawatts delivered move %.2f per cent for each per cent "
          "of megawatts contracted (standard error %.2f): in proportion is inside two standard errors and megawatts that do "
          "not grow is %.0f away; the award notice files the megawatts contracted as registered capacity"
          % (sc["events"], sc["elasticity"], sc["standard_error"], sc["elasticity"] / sc["standard_error"]))
    check("SF16 an event's temperature", all(abs(r["T"] - float(X["_tm"][r["date"]])) < 1e-9 for r in G["cold_rows"][:50]),
          "the event day's daily mean at the station, guideline 2's measure")
    tot = F["totals"]
    check("SF17 the bridge adds up", abs(tot["contracted"] - tot["not_available"] - tot["delivered"]) <= 0.15 and
          abs(tot["delivered"] - tot["comeback_loss"] - tot["off_peak"]) <= 0.15,
          "contracted %.1f less not available %.1f is delivered %.1f; less %.1f lost as load comes back is %.1f off the peaks"
          % (tot["contracted"], tot["not_available"], tot["delivered"], tot["comeback_loss"], tot["off_peak"]))

    # ------------------------------------------------------------------------------------------------ the bar block
    # R: the field's raw material and the footprint of each effect across the data (the hidden factor record)
    shares = {}
    for c in E.ZONES:
        e = G["events"][c]
        cold = e[e["T"] <= E.COLD]
        f = G["providers"][E.ZONE_PROVIDER[c]]
        for w in ("2023/24", "2024/25", "2025/26"):
            cw = cold[cold["winter"] == w]
            shares[(X["names"][c], w)] = float(np.mean(cw["delivered"] / cw["contract"] - E.line_share(f, cw["T"].values)))
    check("availability in every zone and winter", max(abs(v) for v in shares.values()) <= 0.07 and len(shares) == 12,
          "delivered over contracted on the cold days sits within %.3f of its provider's line in each of the 12 zone-winters"
          % max(abs(v) for v in shares.values()))
    nshort = sum(int((~E.met(G["events"][c][G["events"][c]["T"] <= E.COLD])).sum()) for c in E.ZONES)
    ncold = sum(int((G["events"][c]["T"] <= E.COLD).sum()) for c in E.ZONES)
    nmild_met = sum(int(E.met(G["events"][c][G["events"][c]["T"] >= 3.0]).sum()) for c in E.ZONES)
    nmild = sum(int((G["events"][c]["T"] >= 3.0).sum()) for c in E.ZONES)
    check("calls met when mild, short when cold", nshort >= 0.95 * ncold and nmild_met >= 0.85 * nmild,
          "%d of %d cold-day events fell short of the megawatts scheduled; %d of %d events at 3 C or milder delivered them" % (nshort, ncold, nmild_met, nmild))
    C = EP.careful(X, G)
    mis = {p: abs(C[p]["delivered"] - Z[p]["delivered"]) for p in Z}
    out_band = [p for p in Z if not (F["bands"]["delivered"][p][0] <= C[p]["delivered"] <= F["bands"]["delivered"][p][1])]
    check("per megawatt scheduled: where it misreads", sorted(out_band) == ["Ashcombe Road", "Charlecote Way"],
          "it misreads the two zones whose cold-day calls stopped short of the contract (%s) and not the two called in full"
          % ", ".join("%s by %.1f MW" % (p, mis[p]) for p in out_band))
    check("per megawatt scheduled: where it decides", C["Ashcombe Road"]["peak"] < Z["Ashcombe Road"]["firm"] and
          C["Charlecote Way"]["peak"] < Z["Charlecote Way"]["firm"] and not Z["Charlecote Way"]["over"],
          "the misreading holds Ashcombe Road (%.1f MW) and changes nothing at Charlecote Way, which holds either way"
          % C["Ashcombe Road"]["peak"])
    eA = G["events"]["PS40617"]
    eA = eA[eA["T"] <= E.COLD]
    Bm = np.column_stack([np.ones(len(eA)), eA["T"].values, (eA["scheduled"] / eA["contract"]).values])
    y = (eA["delivered"] / eA["contract"]).values
    beta, *_ = np.linalg.lstsq(Bm, y, rcond=None)
    res = y - Bm @ beta
    se = math.sqrt(float(res @ res) / (len(y) - 3) * np.linalg.inv(Bm.T @ Bm)[2, 2])
    implied = float(np.mean(y / Bm[:, 2]))
    check("scheduling more did not deliver more", beta[2] + 2 * se < implied,
          "Ashcombe Road's cold days at equal temperature: delivered share moves %.2f (se %.2f) per unit of share called, "
          "against %.2f if megawatts scheduled were what delivered" % (beta[2], se, implied))
    backs = {X["names"][c]: E.comeback(G["events"][c])["20:00"] for c in E.ZONES}
    check("load comes back at every zone", min(backs.values()) >= 0.18,
          "the half-hour after the window rises by %s MW per megawatt delivered" % ", ".join("%.2f at %s" % (v, k) for k, v in backs.items()))
    nb = E.golden_from(X, comeback_on=False)
    NB = {z["primary"]: z for z in nb["zones"]}
    moved = [p for p in Z if abs(NB[p]["peak"] - Z[p]["peak"]) >= 0.3]
    check("the come-back: where it misreads and decides", moved == ["Ashcombe Road"] and nb["commit"] == CALL,
          "left out, it misreads Ashcombe Road's peak by %.1f MW and no primary's call" % abs(NB["Ashcombe Road"]["peak"] - Z["Ashcombe Road"]["peak"]))
    sc = {}
    for c in E.ZONES:
        e = G["events"][c]
        cold = e[e["T"] <= E.COLD]
        f = G["providers"][E.ZONE_PROVIDER[c]]
        r = cold["delivered"].values - E.line_share(f, cold["T"].values) * cold["contract"].values
        sc[X["names"][c]] = (float(np.std(r)), float(np.std(r) / np.mean(cold["contract"])))
    sw_ = F["scatter_by_winter"]
    check("the scatter grew as the contracts grew", all(v["2025/26"] >= v["2023/24"] + 0.08 for v in sw_.values()),
          "megawatts of scatter on the cold days, winter 2023/24 to winter 2025/26: %s"
          % ", ".join("%.2f to %.2f at %s" % (v["2023/24"], v["2025/26"], k) for k, v in sw_.items()))
    check("the scatter grows with the contract", sc["Ashcombe Road"][0] >= 1.6 * sc["Hartwell Common"][0],
          "megawatts of scatter on the cold days: %s" % ", ".join("%.2f at %s (%.3f of its contract)" % (v[0], k, v[1]) for k, v in sc.items()))
    cs = E.golden_from(X, spread="constant")
    CS = {z["primary"]: z for z in cs["zones"]}
    check("megawatts of scatter carried unchanged", CS["Fenwick Street"]["p90"] < Z["Fenwick Street"]["p90"] - 0.2,
          "Fenwick Street's one-in-ten level reads %.1f MW against %.1f when the record's megawatts of scatter are not scaled to the contract"
          % (CS["Fenwick Street"]["p90"], Z["Fenwick Street"]["p90"]))
    # the rivals, run
    plateau = {}
    for p in sorted(G["providers"]):
        ev_p = pd.concat([G["events"][c] for c in E.ZONES if E.ZONE_PROVIDER[c] == p], ignore_index=True)
        tr, te = ev_p[ev_p["winter"].isin(E.TRAIN_WINTERS)], ev_p[(ev_p["winter"] == E.TEST_WINTER) & (ev_p["T"] <= E.COLD)]
        f = E.provider_fit(tr, G["noise"])
        prev = np.array([X["contract"][(z, "2024/25")] for z in te["zone"]])
        flat = np.minimum(te["scheduled"].values, E.line_share(f, te["T"].values) * prev) - te["delivered"].values
        grow = np.minimum(te["scheduled"].values, E.line_share(f, te["T"].values) * te["contract"].values) - te["delivered"].values
        plateau[p] = (float(np.mean(flat)), float(np.mean(grow)))
    check("delivery grew with the contracts", all(v[0] <= -0.12 and abs(v[1]) <= 0.2 for v in plateau.values()),
          "winter 2025/26's cold days from the two before: %s" % "; ".join(
              "%s %.2f MW short if what was available had not grown, %.2f with the contract" % (p.split()[0], -v[0], v[1]) for p, v in plateau.items()))
    eff = json.load(open(os.path.join(HERE, "effort.json")))
    wrong = {tuple(sorted(r["answer"])) for r in eff["routes"] if not r["golden"]}
    wrong.discard(tuple(sorted(CALL)))
    lucky = [r["name"] for r in eff["routes"] if not r["golden"] and sorted(r["answer"]) == sorted(CALL)]
    check("routes", len(wrong) >= 4 and not lucky and C["_call"] == ["Hartwell Common"],
          "%d shortcuts, %d distinct wrong sets %s; reaching the golden's set: %s"
          % (len(eff["routes"]) - 1, len(wrong), sorted(wrong), lucky or "none"))
    # the one-fact test, computed: the careful pass handed the available share (it still takes the credit off the
    # 17:30 to 18:00 peak and carries the record's megawatts of scatter unchanged)
    told = F["routes"]["the available share right, the credit off the 17:30 to 18:00 peak, the record's megawatts of scatter unchanged"]
    pk_told = {p: Z[p]["before"] - Z[p]["delivered"] for p in Z}
    off_band = [p for p in Z if not (F["bands"]["peak"][p][0] <= pk_told[p] <= F["bands"]["peak"][p][1])]
    hints = {h["order"]: h["rescues"] for h in eff["hints"]}
    check("one-fact test", sorted(told) != sorted(CALL) and off_band == ["Ashcombe Road"] and hints[1] == ["R2a", "R2"]
          and max(len(v) for v in hints.values()) <= len(eff["results"]) / 3.0,
          "told the available share, a pass that still takes the credit off the 17:30 to 18:00 peak with the record's megawatts "
          "of scatter reads Ashcombe Road's peak at %.1f MW for %.1f and reinforces %s: the sentence rescues the share and the "
          "megawatts delivered, %d of %d results" % (pk_told["Ashcombe Road"], Z["Ashcombe Road"]["peak"], " and ".join(told),
                                                      len(hints[1]), len(eff["results"])))

    # ------------------------------------------------------------------------------------------------ Layer 1 neutrality
    rawd = pd.read_csv(os.path.join(TARGET, PK.F_SCADA), dtype={"quality": str})
    pmap, names, rates = PA.register(TARGET)

    def demand_from(df):
        d = df.copy()
        d["code"] = d["point"].map(pmap)
        d["t_utc"] = pd.to_datetime(d["interval_end_uk_local"]).dt.tz_localize("Europe/London").dt.tz_convert("UTC")
        d = d.rename(columns={"value_mw": "mw"})[["code", "t_utc", "mw"]].dropna(subset=["code"])
        return d.drop_duplicates(subset=["code", "t_utc"], keep="last").sort_values(["code", "t_utc"]).reset_index(drop=True)

    def variant(label, cid, Yv):
        for k in ("_prep", "_tm"):
            Yv.pop(k, None)
        g = E.golden_from(E.conform(Yv))
        b = inside(g, F, 0.1)
        check(cid, g["commit"] == CALL and not b, "%s: same set, every figure within 0.1 MW of its band%s" % (label, "" if not b else " EXCEPT " + "; ".join(b[:3])))

    Y = PA.load(TARGET)
    Y["demand"] = demand_from(rawd[rawd["quality"].isin(["G", "S"])])
    variant("held (S) values kept", "L1 held values", Y)
    Y = PA.load(TARGET)
    wv = pd.read_csv(os.path.join(TARGET, PK.F_WX))
    wv["t_utc"] = pd.to_datetime(wv["ob_end_time"], utc=True)
    Y["weather"] = wv.rename(columns={"air_temperature": "temp_c"})[["t_utc", "temp_c"]]
    variant("every weather row kept, raw and checked versions averaged in", "L1 weather versions", Y)
    dup = rawd.duplicated(subset=["point", "interval_end_uk_local"]).sum()
    check("L1 re-sent overlap", dup > 0 and len(X["demand"]) == len(X["demand"].drop_duplicates(subset=["code", "t_utc"])),
          "%d rows of the December 2024 extract re-sent; each half-hour kept once" % dup)
    sw = X["switching"]
    tsw = sorted([s for s in T["switching"] if s["mw_at_start"] > 0], key=lambda s: (s["start"], s["nop"]))
    made = {(s["nop"], s["start"].date()): s for s in tsw}
    logged = {(r.nop, r.start.date()): r for r in sw.itertuples()}
    late = max(abs((r.start.to_pydatetime() - made[k]["start"]).total_seconds()) for k, r in logged.items() if k in made) / 60.0
    check("L1 switching log", len(sw) == len(tsw) and set(made) == set(logged) and late <= 8.0 and
          all(abs(r.mw - made[k]["mw_at_start"]) < 0.006 for k, r in logged.items()),
          "%d logged transfers pair up (closed, then opened to normal), megawatts as logged, each operation logged within "
          "%d minutes of the switching" % (len(sw), int(round(late))))
    te_ = T["events"]
    done = [e for e in te_ if e["status"] == "Completed"]
    check("L1 dispatch log", int((X["events"]["status"] == "Completed").sum()) == len(done),
          "%d completed and %d cancelled instructions at their latest revision" % (len(done), len(te_) - len(done)))

    # ------------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    check("inputs: files", len(files) >= 10 and {".csv", ".xlsx", ".pdf"} <= exts, "%d files: %s" % (len(files), sorted(exts)))
    n_scada = sum(1 for _ in open(os.path.join(TARGET, PK.F_SCADA))) - 1
    n_ev = sum(1 for _ in open(os.path.join(TARGET, PK.F_EVENTS))) - 1
    check("inputs: large CSVs", n_scada >= 20000 and n_ev >= 500,
          "SCADA %d rows (point renames, held and bad values, gaps, a re-sent extract); dispatch log %d rows, about %d printed "
          "pages at 50 lines (revisions, cancellations, provider names typed five ways)" % (n_scada, n_ev, n_ev // 50))
    src = "".join(open(os.path.join(HERE, f)).read() for f in ("parse.py", "estim.py"))
    check("distractors unread", all(f not in src for f in PK.DISTRACTORS) and len(PK.DISTRACTORS) >= 2,
          "%s never opened by the golden's code" % ", ".join(PK.DISTRACTORS))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("metadata.json", sorted(f["path"] for f in meta["files"]) == sorted("target/" + f for f in files)
          and set(meta["distractor_files"]) == {"target/" + f for f in PK.DISTRACTORS}, "provenance for every file")
    check("no describing file", not any(re.search(r"readme|dictionary|notes|manifest|codebook|schema", f, re.I)
                                        for f in files), "no file whose job is to describe the data")

    # ------------------------------------------------------------------------------------------------ realism
    counts = X["events"][X["events"]["status"] == "Completed"].assign(w=lambda d: [E.WINTER_OF(x) for x in d["date"]]) \
        .groupby(["zone", "w"]).size()
    check("realism: event counts", counts.nunique() >= len(counts) - 2, "per zone and winter: %s" % counts.to_dict())
    sched = X["events"][X["events"]["status"] == "Completed"]["scheduled_mw"]
    check("realism: no setting shows", sched.nunique() >= 10 and all(abs(G["providers"][p]["share"] * 100 % 5) > 0.3 for p in G["providers"]),
          "%d distinct megawatts scheduled; the available shares (%s) are not round figures" % (sched.nunique(), ", ".join("%.3f" % G["providers"][p]["share"] for p in sorted(G["providers"]))))
    text = guide + award + subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, PK.F_DUOS), "-"], capture_output=True, text=True).stdout
    people = set(re.findall(r"(?<!Appendix )\b(Marion Todd|Clifford Evans|Irene Carpenter|[A-Z]\. [A-Z][a-z]+)\b", text))
    check("realism: personas", people <= {"Marion Todd", "Clifford Evans", "Irene Carpenter", "C. Evans"},
          "people named in the documents: %s" % sorted(people))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("no em dashes", "—" not in text and "—" not in sub, "documents and submission")
    leak_words = [w for w in ("available", "come back", "comes back", "rebound", "payback", "share of", "fell short", "falls short")
                  if w in (gflat + " " + aflat).lower()]
    check("documents name no step", not leak_words, "the guideline and the award notice carry none of: available, come back, "
          "rebound, payback, share of, fell short (%s); the award notice's availability fee is its payment term" % (leak_words or "none"))

    # ------------------------------------------------------------------------------------------------ deliverables
    gz = zipfile.ZipFile(os.path.join(TASK, "golden.zip"))
    check("golden zip", sorted(gz.namelist()) == sorted([GO.F_XLSX, GO.F_PPTX]), "%s" % gz.namelist())
    check("figures.json", F["call"] == CALL and F["careful_call"] == ["Hartwell Common"] and F["quick_call"] == [],
          "call %s; the careful pass %s; the quick pass %s" % (F["call"], F["careful_call"], F["quick_call"]))
    r = subprocess.run([sys.executable, os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/audit_containers.py"),
                        TASK], capture_output=True, text=True)
    check("container gate", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])

    bad = [c for c, ok, _ in RESULTS if not ok]
    print("\n%d checks, %d failed%s" % (len(RESULTS), len(bad), (": " + ", ".join(bad)) if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
