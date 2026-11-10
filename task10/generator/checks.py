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
    check("bands are narrow", all(w <= 0.9 for w in widths.values()), "widest band by result: %s MW" % {k: round(v, 1) for k, v in widths.items()})
    fen, cha = [v for v in FAM.values()], None
    fmin = min(z["p90"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] == "Fenwick Street")
    fexp = max(z["peak"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] == "Fenwick Street")
    cmax = max(z["p90"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] == "Charlecote Way")
    amin = min(z["p90"] - z["firm"] for v in FAM.values() for z in v["zones"] if z["primary"] in ("Ashcombe Road", "Hartwell Common"))
    check("margins", fmin >= 0.3 and fexp <= -0.2 and cmax <= -0.4 and amin >= 2.0,
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
    check("SF4 the megawatts delivered", "half-hours ending 17:30 and 18:00" in gflat and not inside(v, F) and v["commit"] == CALL,
          "guideline 6: the half-hours ending 17:30 and 18:00; the lower of the two for the mean moves no figure out of its band")
    check("SF5 the call in full", "scheduled in full for the service window" in gflat, "guideline 6: the megawatts contracted scheduled in full")
    check("SF6 demand with flexibility", "its highest half-hourly demand on that day" in gflat,
          "guideline 6: the day's highest half-hour, whichever it is")
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
                            ("SF12 the scatter", "the scatter as measured", ("the scatter as measured",)),
                            ("SF13 the heating base", "14 or 17 C", ("heating base 14 C", "heating base 17 C"))):
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
    check("SF15 the backtest", F["backtest"]["n"] == int(sum((G["events"][c]["winter"] == E.TEST_WINTER).sum() for c in E.ZONES)),
          "winter 2025/26's %d completed events, fitted on 2023/24 and 2024/25, an 80 per cent range (the prompt)" % F["backtest"]["n"])
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
    check("routes", len(wrong) >= 3 and len(lucky) <= 1 and C["_call"] == ["Hartwell Common"],
          "%d shortcuts, %d distinct wrong sets %s; reaching the set with every megawatt figure wrong: %s"
          % (len(eff["routes"]) - 1, len(wrong), sorted(wrong), lucky or "none"))
    # the one-fact test, computed: the careful pass handed the available share
    hint = []
    for p in Z:
        d = Z[p]["delivered"]
        pk = Z[p]["before"] - d
        hint.append((p, abs(pk - Z[p]["peak"]) <= 0.3))
    check("one-fact test", sum(1 for _, ok in hint if not ok) >= 1 and F["careful_call"] != CALL,
          "told the available share, a pass that still takes the credit off the 17:30 to 18:00 peak with the fit's own range "
          "misreads Ashcombe Road's peak, every one-in-ten level and Fenwick Street's call: it rescues the megawatts delivered alone")

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
    check("L1 switching log", len(sw) == len(tsw) and all(abs(a - b["mw_at_start"]) < 0.006 for a, b in zip(sw["mw"], tsw)),
          "%d logged transfers pair up (closed, then opened to normal), megawatts as logged" % len(sw))
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
