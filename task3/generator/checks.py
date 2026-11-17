"""Every assertion of the build on the cut pack: the input gates, the bar block (R1 to R7), every row of the fork
table (SF1 to SF22), the pinning list, the pack against the core's arrays storm by storm, the second implementation,
and the realism sweep.

    python3 task3/generator/checks.py [target]
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
import world as WL  # noqa: E402

ROWS = []


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond), detail))
    return bool(cond)


def inside(v, band, nd):
    return band[0] - 1e-9 <= round(float(v), nd) <= band[1] + 1e-9


def texts(target):
    """every word a reader can find in the pack: file names, headers, workbook cells, the PDF's text, the schema"""
    out = {}
    for path in sorted(glob.glob(os.path.join(target, "*"))):
        name = os.path.basename(path)
        if name.endswith(".csv"):
            with open(path, newline="") as fh:
                head = next(csv.reader(fh))
            out[name] = " ".join(head)
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
            out[name] += " " + " ".join(sorted({r[0] for r in con.execute("SELECT DISTINCT wx FROM pw_block")}))
            con.close()
    return out


def figure_values(P, g, k, names):
    out = {"storms " + s: g[s] for s in names}
    out.update({"depth " + s: g.even[s] for s in names})
    return out


def main(target):
    X, fig, E, spec = RS.run(target)
    P, names = X["P"], X["names"]
    fb = fig["figure_band"]
    cls = fig["classes"]
    st, so, ref = fig["stations"], fig["sources"], fig["referee"]
    code = X["code"]
    T = texts(target)
    files = sorted(T)
    reg = re.sub(r"\s+", " ", T[docs.FILES["regulation"]])

    # ------------------------------------------------------------------------------------------- the input gates
    kinds = {"spreadsheet": [f for f in files if f.endswith((".csv", ".xlsx"))], "database": [f for f in files if f.endswith(".sqlite")],
             "text": [f for f in files if f.endswith(".pdf")]}
    ok("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    ok("gate: two or more file categories", sum(1 for v in kinds.values() if v) >= 2, str({k: len(v) for k, v in kinds.items()}))
    rows = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv")}
    ok("gate: a CSV of 20,000 rows or more", max(rows.values()) >= 20000, "largest %d rows" % max(rows.values()))
    ok("gate: a second large CSV of ten printed pages or more", sum(1 for v in rows.values() if v >= 600) >= 2,
       "%d CSVs of 600 rows or more" % sum(1 for v in rows.values() if v >= 600))
    unused = [pack.FILES["daily"], pack.FILES["traffic"]]
    ok("gate: two distractors ship, unused and unlabelled", all(f in files for f in unused) and
       not any(f in A.FILES.values() for f in unused) and not any(re.search("distract|unused|decoy", f, re.I) for f in files))
    ok("gate: no file or sheet describes the data",
       not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook|guide", f, re.I) for f in files) and
       not any(re.search(r"\b(readme|notes|dictionary|about)\b", " ".join(load_workbook(os.path.join(target, f), read_only=True).sheetnames), re.I)
               for f in files if f.endswith(".xlsx")))
    ok("gate: no file name names a judgment", not any(re.search(r"loss|melt|burst|lag|correct|calibrat|hail|bias", f, re.I) for f in files))
    never = [r"tip duration", r"tipping time", r"intensity correction", r"dynamic calibration", r"calibration curve", r"under-?read",
             r"under-?catch", r"\bmelt", r"\bdelay", r"\blag\b", r"retention", r"burst factor", r"areal reduction", r"representativ",
             r"validation", r"calibration set", r"which record"]
    hits = [(f, w) for f, t in T.items() for w in never if re.search(w, t, re.I)]
    ok("never filed: no shipped word names a judgment's step", not hits, str(hits[:4]))
    heads = " ".join(T[f].split("\n")[0] if f.endswith(".csv") else T[f] for f in files if not f.endswith(".pdf"))
    ok("R1 no shipped column holds a result", not re.search(r"\bclass\b|storms_per_season|triggering_storms|protection_class", heads, re.I))
    ok("R1 the field's raw material ships", all(f in files for f in [pack.FILES["tips"] % c for c in P.codes] +
                                                   [pack.FILES["visits"], pack.FILES["pw"], pack.FILES["radar"], pack.FILES["rs_events"]]),
       "tips to the second at six stations (%s rows), the storage gauge reads, the detector's blocks, the radar's cells" % format(fig["counts"]["tip_rows"], ","))

    # ----------------------------------------------------------------------------- the pinning list, in the files
    for label, pat in (("the storm separation (2.2)", r"six hours or more without rain"), ("the 60 consecutive minutes (2.3)", r"any 60 consecutive minutes"),
                       ("a storm counts once (2.3)", r"A storm counts once"), ("an equal depth reaches it (2.3)", r"equal to the triggering depth reaches it"),
                       ("the season (2.1)", r"from 1 May to 31 October"), ("the basis (3.1)", r"every complete warm season of its governing station's tip record"),
                       ("the depth of 3.2", r"\s+".join(r"the greatest depth that the rain at the crossing's source area reaches, counted as in 2\.3, in a mean of five or more storms a warm season over the same seasons as 3\.1".split())), ("class 3 (4.1)", r"class 3 at 3\.0 or more"),
                       ("class 2 (4.1)", r"class 2 at 1\.0 or more and under 3\.0"), ("class 1 (4.1)", r"class 1 under 1\.0"),
                       ("one class a program (1.2)", r"holds one class for a whole protection program"),
                       ("the point depth (2.4)", r"point rain depth at the source area")):
        ok("pinned in the regulation: " + label, re.search(pat, reg), pat)
    ok("pinned in the registers: triggering depths and governing stations are the core's",
       all(abs(P.M[s]["T"] - C.CROSSINGS[s]["T"]) < 1e-9 and P.S[P.M[s]["station"]].name == C.CROSSINGS[s]["depot"] for s in names))
    ok("pinned in the registers: bucket sizes are the tips' own increments", all(P.S[c].bucket == WL.BUCKET[C.DEPOTS[P.S[c].name]["model"]] for c in P.codes))
    ok("pinned: the loggers' clock and the unheated funnels", "UTC+1 all year" in T[docs.FILES["stations"]] and "none" in T[docs.FILES["stations"]])
    ok("the golden uses no constant of the core", "import core" not in open(os.path.join(HERE, "analysis.py")).read() and
       "import core" not in open(os.path.join(HERE, "verify.py")).read())

    # -------------------------------------------------------------------- the pack against the core, storm by storm
    WD = WL.build()
    worst, flags, unmatched = 0.0, 0, 0
    for d, w in WD["W"].items():
        s = P.S[code[d]]
        e = s.nearest(WD["onset"][d] + 60 * C.M // 2)
        unmatched += int((e < 0).sum()) + int(len(set(e.tolist())) != len(e))
        tot = s.total(s.r["lump"])[e]
        worst = max(worst, float(np.abs(tot - w["rec"].sum(axis=1)).max()) / s.bucket)
        flags += int((s.hail[e] != w["hail10"].any(axis=1)).sum())
        chk = np.array([w["check"][i] for i in range(w["nint"])])
        ok("pack against core: %s's storage reads are the core's account" % d, len(s.check) == len(chk) and float(np.abs(np.sort(s.check) - np.sort(np.round(chk, 1))).max()) < 0.051)
    ok("pack against core: every core storm is one storm of the tip logs", unmatched == 0, "%d unmatched" % unmatched)
    ok("pack against core: storm totals within two buckets", worst <= 2.0, "worst %.2f buckets" % worst)
    ok("pack against core: the detector's hail storms are the core's", flags == 0, "%d differ" % flags)
    ok("golden files the truth's classes", all(cls[s] == 1 + int(fig["truth"][s] >= 1.0) + int(fig["truth"][s] >= 3.0) for s in names), str(fig["truth"]))
    ok("the cut pack re-proves the core at level 5", fig["rubric"]["level"] == 5 and not fig["rubric"]["fails"], str(fig["rubric"]))
    ok("rubric: a run that loses one stump earns 50 or under", max(fig["rubric"]["one_lost"].values()) <= 50, str(fig["rubric"]["one_lost"]))
    ok("rubric: the reflex route earns 30 or under", fig["rubric"]["reflex"] <= 30 and fig["rubric"]["rigorous"] <= 50, str(fig["rubric"]["reflex"]))

    # ------------------------------------------------------------------------------- the second implementation
    v = V.run(target)
    bad = [r[0] for r in V.compare(v, fig) if not r[4]]
    ok("verify: the tip-by-tip rebuild files the same classes and lands every stated figure in its band", not bad, str(bad))

    # ---------------------------------------------------------------------------------------- R2 the mess, neutral
    def mishandled(label, Q=None, tag="R2 ", **kw):
        Q = Q or A.Pack(target, **kw)
        g, k = Q.estimate(), Q.kappas()
        out = figure_values(Q, g, k, names)
        out[RS.C1], out[RS.C2] = A.under_read(k[code["Valfosca"]]), Q.site_factor("Rio Marden")
        off = [f for f, x in out.items() if not inside(x, fb[f], RS.dec(f))]
        ok(tag + label + ": every graded figure stays in its band and the classes stay", not off and A.classes(g, names) == cls, str(off))
    mishandled("re-sent logger rows left in", dedupe=False)
    mishandled("the technicians' tip tests left in", drop_tests=False)
    mishandled("the visit book read on the loggers' clock", visit_clock="logger")
    mishandled("the radar read by the current pixel identifiers only", radar_ids="new")
    mishandled("the radar's clock read as local", radar_clock="local")
    for label, Q in X["conv"].items():       # a second implementation's readings of the stamp and of the sliding hour
        mishandled(label, Q=Q, tag="SF26 ")
    win = fig["window"]
    held = X["fam"] + X["crude_all"][A.CARRIED] + X["more"]["hail"]
    ok("SF26 a tip's stamp read as the start of its second, or the 60 minutes slid by the second, moves a count by a storm or "
       "two and no class, and every band's top stands a storm and a tenth of a millimetre above its widest way",
       win["classes_hold"] and 1 <= win["storms_moved"] <= 2 and
       all(fb["storms " + s][1] >= max(v[s] for v in held) + (A.TOP_STORMS / 18.0) - 0.006 and
           fb["depth " + s][1] >= max(v.even[s] for v in held) + A.TOP_MM - 0.05 for s in names),
       "storms moved %d at %d crossings, depth %.2f mm" % (win["storms_moved"], win["crossings_moved"], win["depth_moved_mm"]))
    ok("SF27 the cut on the storage account: every way of the loss used or held in the bands leaves less on the %s mm "
       "buckets' intervals than every way refused, and the power law's fitted exponent stands inside its limits" % fig["account_residual"]["small_bucket"],
       X["steps"]["held_max"] < X["steps"]["refused_min"] and 1.0 < min(X["steps"]["power"]) and max(X["steps"]["power"]) < 1.4,
       "held %.3f, refused %.3f, exponent %.3f to %.3f" % (X["steps"]["held_max"], X["steps"]["refused_min"],
                                                          min(X["steps"]["power"]), max(X["steps"]["power"])))

    # --------------------------------------------------------------------------------- R3 each result's hurried figure
    refl = X["lat"]["S1+S2+S3"]
    ok("R3 R2's hurried figure (one factor) is outside the band by half or more", X["c1"]["lost"] < 0.5 * fb[RS.C1][0],
       "%.2f against %s" % (X["c1"]["lost"], fb[RS.C1]))
    ok("R3 R3's hurried figure (the yearly rainfall's ratio) is outside the band", X["c2"]["lost"] < fb[RS.C2][0] - 0.2,
       "%.3f against %s" % (X["c2"]["lost"], fb[RS.C2]))
    ok("R3 R4's hurried figure (tips as rain) is outside the band", X["c3"]["lost"] < 0.5 * fb[RS.C3][0])
    for s in ("Rio Gelt", "Rio Marden", "Rio Bianc", "Rio Sass"):
        ok("R3 R5's hurried count at %s is across its line" % s, A.classes(refl, names)[s] != cls[s] and not inside(refl[s], fb["storms " + s], 2),
           "%.2f against %s" % (refl[s], fb["storms " + s]))
    ok("R3 R6's hurried depths are outside their bands at six crossings or more",
       sum(1 for s in names if not inside(refl.even[s], fb["depth " + s], 1)) >= 6)
    ok("R3 R7's hurried classing differs from the golden's at three crossings or more", sum(1 for s in names if A.classes(refl, names)[s] != cls[s]) >= 3)
    ok("R3 R1 is earned by every pass (a rebuilt total, never a graded figure)", all(abs(P.factor(c) - fig["account_factor"][P.S[c].name]) < 6e-4 for c in P.codes))
    for k_, own in (("S1", "Rio Gelt"), ("S2", "Rio Marden"), ("S3", "Rio Bianc")):
        lost = X["lat"][k_]
        ok("R3 %s dropped alone moves %s across its line and no other stump's member" % (k_, own),
           A.classes(lost, names)[own] != cls[own] and all(A.classes(lost, names)[o] == cls[o] for o in ("Rio Gelt", "Rio Marden", "Rio Bianc") if o != own),
           "%s at %.2f" % (own, lost[own]))
        alone = X["lat"][RS.ALONE[k_]]
        ok("R3 %s fixed alone on the reflex route still misses the classing" % k_, RS.call_of(alone, names) != fig["call"])
    ok("R3 the shortcuts land on different wrong classings", fig["distinct_wrong_calls"] >= 6 and
       len({tuple(RS.call_of(X["lat"][k_], names)) for k_ in ("S1", "S2", "S3")}) == 3, "%d distinct" % fig["distinct_wrong_calls"])

    # ---------------------------------------------------------------------------------------------- R4 no plant
    rep = 0
    for c in P.codes:
        tot = np.round(P.S[c].total(P.S[c].r["lump"]), 1)
        five = {}
        for i in range(len(tot) - 4):
            five[tuple(tot[i:i + 5])] = five.get(tuple(tot[i:i + 5]), 0) + 1
        rep += sum(1 for n in five.values() if n > 1)
    ok("R4 no block of storms repeats inside a tip log", rep == 0, "%d repeated runs of five storm totals" % rep)
    seqs = [tuple(np.round(P.S[c].total(P.S[c].r["lump"])[:200], 1)) for c in P.codes]
    ok("R4 no two stations carry the same storms", len(set(seqs)) == len(seqs))
    ok("R4 no shipped file ranks or classes the crossings (Gate G)", not any(re.search(r"class [123]\b.{0,40}Rio |Rio \w+.{0,40}class [123]\b", t) for t in T.values()))
    ok("R4 no memo, draft or stakeholder figure ships", not any(re.search(r"memo|draft|review|proposal", f, re.I) for f in files))

    # ------------------------------------------------------------------------------------------- R5 no one thing
    ok("R5 the loss by rate is at every station: one factor leaves every account open and the left-over runs with the rate",
       all(d["resid_factor"] > 1.5 * d["resid_rate"] and d["resid_r"] > 0.7 for d in st.values()),
       str({n: (d["resid_factor"], d["resid_rate"], d["resid_r"]) for n, d in st.items()}))
    ok("R5 the bursts part from the yearly rainfall at every source area, the forced crossings among them",
       sum(1 for s in names if abs(so[s]["burst_factor"] - so[s]["normal_ratio"]) > 0.04) >= 6 and
       abs(so["Rio Ciadin"]["burst_factor"] - so["Rio Ciadin"]["normal_ratio"]) > 0.2 and
       all(abs(so[g]["burst_factor"] - so[g]["normal_ratio"]) > 0.15 for g in P.research))
    ok("R5 hail storms tip late at every station", all(d["hail_storms"] >= 50 and d["late_hail_pct"] > 15 and d["late_rain_pct"] < 1 for d in st.values()),
       str({n: (d["hail_storms"], d["late_hail_pct"]) for n, d in st.items()}))
    for k_ in ("S1", "S2", "S3"):
        moved = [s for s in names if not inside(X["lat"][k_][s], fb["storms " + s], 2) and A.classes(X["lat"][k_], names)[s] == cls[s]]
        ok("R5 %s misleads where it decides nothing too" % k_, len(moved) >= 1, "moves without a flip: %s" % ", ".join(moved))
    by = {r["id"]: r for r in E["results"]}
    for j in E["factorial"]["judgments"][:3]:
        ok("R5 %s fixed alone rescues a third of the results or fewer" % j["id"], len(j["alone"]["results_rescued"]) <= len(by) / 3.0,
           str(j["alone"]["results_rescued"]))
    # ----------------------------------------------------------------------------------------- R6 the one-fact test
    for h in E["hints"]:
        ok("R6 the hint rescues a third or fewer: " + h["sentence"][:48], len(h["rescues"]) <= len(by) / 3.0, str(h["rescues"]))
    # ------------------------------------------------------------------------------------------------ R7 the rivals
    ok("R7 the battery: every variant files the golden's classes", fig["family_calls_all_golden"] and fig["variants"] >= 12, "%d variants" % fig["variants"])
    R = RS.figures(X)[1]
    ok("R7 the battery: every variant's every figure sits inside the stated band",
       all(inside(x, fb[fid], RS.dec(fid)) for fid in fb for x in R["famv"][fid]))
    ok("R7 forcing: each fitted input moved by a fifth leaves the classes", all(p["call_holds"] for p in fig["perturbations"]),
       "nearest %.2f" % min(p["nearest"] for p in fig["perturbations"]))

    # -------------------------------------------------------------------------------------------- the fork table
    ok("SF1 six hours is filed (2.2) and no dry gap lies between three and eight hours, so three, six and eight give one catalogue",
       all(d["gaps_3_to_6h"] == 0 and d["gaps_6_to_8h"] == 0 for d in st.values()))
    ok("SF2 any 60 consecutive minutes: windows anchored on the tips (the second implementation) land in every band", not bad)
    ok("SF3 a storm counts once: filed in 2.3", re.search(r"A storm counts once, however many times", reg))
    edge, moved = 0, {}
    for c in P.codes:
        s = P.S[c]
        big = s.slide(s.r["spread"]) >= 9.0
        last = (A.EPOCH + s.t1.astype("timedelta64[s]")).astype("datetime64[D]").astype(str)
        edge += int(sum(1 for d_, e_, b in zip(s.day, last, big) if b and d_ != e_ and d_[5:] in ("04-30", "10-31")))
    # 2.1 read by the day the largest 60 minutes open, by the day of the first tip, and by the day on civil summer time or UTC
    for how in ("open", "first", "civil", "utc"):
        Q = A.Pack(target, season_by=how)
        gq, kq = Q.estimate(), Q.kappas()
        out = figure_values(Q, gq, kq, names)
        out[RS.C1], out[RS.C2] = A.under_read(kq[code["Valfosca"]]), Q.site_factor("Rio Marden")
        base = figure_values(P, X["gold"], None, names)
        base[RS.C1], base[RS.C2] = A.under_read(P.kappas()[code["Valfosca"]]), P.site_factor("Rio Marden")
        csr_ = code["Costarossa"]            # the hail storms' share is taken over these storms and no others
        same_hail = bool(np.array_equal(Q.S[csr_].hail & Q.S[csr_].inseason, P.S[csr_].hail & P.S[csr_].inseason))
        moved[how] = (sorted(f for f in out if abs(out[f] - base[f]) > 1e-9) + ([] if same_hail else [RS.C3]),
                      A.classes(gq, names) == cls, sum(int((Q.S[c].inseason != P.S[c].inseason).sum()) for c in P.codes))
    ok("SF4 the season is filed (2.1: a storm belongs to the day in which its largest 60-minute depth falls) and no storm of 9 mm in 60 "
       "minutes at a station (the least any triggering depth or stated depth asks of one) runs across midnight at either end of it",
       edge == 0, "%d" % edge)
    ok("SF4 a storm's day read as the day its largest 60 minutes open, as the day of its first tip, or on civil summer time or UTC "
       "in place of the loggers' clock, moves no graded figure at all",
       all(not m[0] and m[1] for m in moved.values()), "storms whose season differs: %s; figures moved: %s" % (
           {h: m[2] for h, m in moved.items()}, {h: m[0] for h, m in moved.items()}))
    ok("SF5 the eighteen-season mean is filed (3.1) and every station holds the same eighteen complete seasons",
       all(P.S[c].seasons == 18 and min(P.S[c].year) == 2009 and max(P.S[c].year) == 2026 for c in P.codes))
    rounds = {}
    for r_ in csv.DictReader(open(os.path.join(target, pack.FILES["visits"]))):
        for word, key in (("season opening", "open"), ("season closing", "close")):
            if word in r_["remarks"]:
                rounds.setdefault((r_["station"], r_["visit_date"][:4]), {})[key] = r_["visit_date"][5:]
    ok("SF5 every station is in service over the whole of every warm season: its opening round falls before 1 May and its closing "
       "round after 31 October in each of the eighteen years, so every season of the tip record is complete",
       len(rounds) == 18 * len(P.codes) and all(v.get("open", "99") < "05-01" and v.get("close", "00") > "10-31" for v in rounds.values()),
       "openings %s to %s, closings %s to %s" % (min(v["open"] for v in rounds.values()), max(v["open"] for v in rounds.values()),
                                               min(v["close"] for v in rounds.values()), max(v["close"] for v in rounds.values())))
    ok("SF6 the triggering depth is a point depth at the source area: the register's column and 2.4",
       "triggering_depth_point_mm_60min" in T[docs.FILES["crossings"]] and re.search(r"point rain depth at the source area", reg))
    ok("SF7 the lines are inclusive (4.1) and no variant comes within 0.3 of one", fig["nearest_variant"]["distance"] >= 0.3,
       "%.2f at %s" % (fig["nearest_variant"]["distance"], fig["nearest_variant"]["crossing"]))
    ok("SF8 one class for the whole program: filed in 1.2", re.search(r"holds one class for a whole protection program", reg))
    near_km = {s: min(P.codes, key=lambda c: abs(WL.STATIONS[P.S[c].name][1] - P.M[s]["km"])) for s in names}
    near_xy = {s: min(P.codes, key=lambda c: (P.S[c].xy[0] - P.M[s]["xy"][0]) ** 2 + (P.S[c].xy[1] - P.M[s]["xy"][1]) ** 2) for s in names}
    ok("SF9 the register's governing station is the nearest by road and on the map at every crossing",
       all(near_km[s] == P.M[s]["station"] == near_xy[s] for s in names))
    acc = fig["account_residual"]
    sm = acc["small_bucket"]
    rt = acc["ratio"]
    ok("SF10 the rate read tip by tip and on totals of one, two, three and five minutes is in the battery; on ten- and fifteen-minute "
       "totals the account is left open by 1.5 times the fitted reading or more",
       min(rt["10-minute totals"][0], rt["15-minute totals"][0]) >= 1.5 and len(A.READS) == 9 and acc["kept"][sm][1] < 1.6 * acc["golden"][sm],
       "kept %.2f to %.2f, fitted %.2f; 10 and 15 minutes %s and %s times" % (acc["kept"][sm][0], acc["kept"][sm][1], acc["golden"][sm],
                                                                             rt["10-minute totals"], rt["15-minute totals"]))
    ok("SF10 the refused readings of the rate file the golden's classes all the same",
       acc["refused_calls_hold"]["10-minute totals"] and acc["refused_calls_hold"]["15-minute totals"], str(acc["refused_calls_hold"]))
    ok("SF11 the tipping-time form alone and with a fixed factor beside it, one a bucket model and one a station, is the battery (tip by "
       "tip its first-order form too); a power law leaves the account open by 1.4 times the tipping-time form's or more on the same reading",
       rt["power law"][0] >= 1.4 and A.LOSS_WAYS == ("recip", "scaled") and A.POOL_WAYS == ("model", "gauge") and
       ("lin", "tip", 1) in A.LOSS_READS, "power law %s" % rt["power law"])
    ok("SF11 the first-order form on minute totals is not refused by the account (%.2f to %.2f times) and every stated band holds it under "
       "every cross" % tuple(rt["first-order form"]),
       all(inside(x, fb[fid], RS.dec(fid)) for fid in fb for x in R["wide"][fid]) and fig["carried_variants"] >= 12, "%d crosses" % fig["carried_variants"])
    ok("SF11 the first-order form and the power law file the golden's classes under every cross", acc["refused_calls_hold"]["first-order form"] and
       acc["refused_calls_hold"]["power law"])
    ok("SF12 the under-read at 100 mm an hour: the band holds every loss reading of the battery and the tip-by-tip rebuild",
       all(inside(x, fb[RS.C1], 1) for x in X["c1"]["fam"]) and inside(v["under_read_valfosca_pct"], fb[RS.C1], 1),
       "%.1f to %.1f, verifier %.1f, band %s" % (min(X["c1"]["fam"]), max(X["c1"]["fam"]), v["under_read_valfosca_pct"], fb[RS.C1]))
    ok("SF13 eight ways of the burst factor are in the battery and agree at Rio Marden within 0.02",
       len(A.SITE_WAYS) == 8 and max(X["c2"]["fam"]) - min(X["c2"]["fam"]) < 0.02, "%.3f to %.3f" % (min(X["c2"]["fam"]), max(X["c2"]["fam"])))
    m = so["Rio Marden"]
    ok("SF14 the cruder burst factors: the regression and its reverse, the largest quarter chosen either way, straddle the paired mean, "
       "and each files the golden's classes", m["slope"] < m["burst_factor"] < m["slope_rev"] and m["top"] < m["burst_factor"] < m["top_rev"] and
       all(fig["crude"]["site " + a]["call_holds"] for a in A.CRUDE_SITE), "%.3f < %.3f < %.3f; %.3f < %.3f" % (m["slope"], m["burst_factor"], m["slope_rev"], m["top"], m["top_rev"]))
    ok("SF14 the unpaired upper deciles move between odd and even seasons more than the paired mean",
       max(so[s]["q90_halves_pct"] for s in names) > 2.0 * max(so[s]["geo_halves_pct"] for s in names),
       "%.1f against %.1f per cent" % (max(so[s]["q90_halves_pct"] for s in names), max(so[s]["geo_halves_pct"] for s in names)))
    ok("SF15 the burst factor of 2013 to 2026 serves all eighteen seasons: 3.1 files every season and no station moved",
       all(str(v_)[:4] == "2008" for v_ in [r["in_service_from"] for r in V.sheet(os.path.join(target, docs.FILES["stations"]), "Stations")]))
    Q = A.Pack(target, hail_by="day")
    gq = Q.estimate()
    offq = [f for f, x in figure_values(Q, gq, None, names).items() if not inside(x, fb[f], RS.dec(f))]
    ok("SF16 a hail storm by its own blocks or by its day: the day reading adds storms and moves no figure out of its band",
       not offq and A.classes(gq, names) == cls, "%d storms added; outside: %s" % (
           sum(int(Q.S[c].hail.sum() - P.S[c].hail.sum()) for c in P.codes), offq))
    ok("SF17 four ways of placing a hail storm's water are in the battery", len(A.HAIL_WAYS) == 4 and
       all(inside(x, fb[RS.C3], 1) for x in X["c3"]["fam"]))
    o = ref["others"]
    ok("SF18 the cruder hail handlings fall short of the weighing gauges or overshoot them",
       o["hail water moved only from the dry intervals"]["storms"] < ref["seen"]["storms"] - 10 and
       o["hail water spread evenly"]["storms"] < ref["seen"]["storms"] - 25 and
       o["the detector's own amounts on hail storms"]["storms"] > ref["seen"]["storms"] + 20 and
       min(d["optical_log_sd"] for d in st.values()) > 0.25,
       "seen %d; dry %d, even %d, the detector's amounts %d" % (ref["seen"]["storms"], o["hail water moved only from the dry intervals"]["storms"],
                                                                o["hail water spread evenly"]["storms"], o["the detector's own amounts on hail storms"]["storms"]))
    ok("SF19 the share of the hail storms' maximum the tips miss: the band holds the battery and the tip-by-tip rebuild",
       inside(v["hail_gap_costarossa_pct"], fb[RS.C3], 1), "verifier %.1f, band %s" % (v["hail_gap_costarossa_pct"], fb[RS.C3]))
    xs = P.station_maxima()[0]
    off20 = []
    for s in names:
        est = np.sort(P.transfer(s, xs[P.M[s]["station"]], "geo")[P.keep(s)])[::-1]
        r = fig["counts"]["even_rank"]
        if not inside(0.5 * (est[r - 1] + est[r]), fb["depth " + s], 1):
            off20.append(s)
    ok("SF20 the depth reached five times a season is the 90th largest of eighteen seasons; the interpolated reading lands in every band",
       fig["counts"]["even_rank"] == 90 and not off20, str(off20))
    tail, short = {}, {}
    for s in names:                          # 3.2 from a fitted tail in place of the count
        n_ = P.S[P.M[s]["station"]].seasons
        est = np.sort(P.transfer(s, xs[P.M[s]["station"]], "geo")[P.keep(s)])[::-1]
        gp, ex = [], []
        for per in (8, 10, 15, 20):          # thresholds, storms a season
            k = per * n_
            exc = est[:k][::-1] - est[k]
            a0 = float(exc.mean())
            a1 = float((((k - 1.0 - np.arange(k)) / (k - 1.0)) * exc).sum() / k)
            xi, sg = 2.0 - a0 / (a0 - 2.0 * a1), 2.0 * a0 * a1 / (a0 - 2.0 * a1)
            gp.append(float(est[k] + sg / xi * ((per / A.EVEN) ** xi - 1.0)))
            ex.append(float(est[k] + a0 * np.log(per / A.EVEN)))
        tail[s] = (min(gp), max(gp), min(ex), max(ex))
        short[s] = int((est >= max(ex)).sum())
    ok("SF20 3.2 files a count, not a fitted level: a generalised Pareto tail over thresholds of 8 to 20 storms a season lands in "
       "every band, and where an exponential tail's level leaves a band the record holds fewer than five storms a season at it",
       all(inside(v, fb["depth " + s], 1) for s in names for v in tail[s][:2]) and
       all(short[s] < fig["counts"]["even_rank"] for s in names if not inside(tail[s][3], fb["depth " + s], 1)),
       "; ".join("%s %.1f to %.1f, exponential %.1f to %.1f (%d storms reach it)" % ((s,) + tuple(tail[s]) + (short[s],)) for s in names))
    longest = max(float(np.max(h[3])) for d in WD["spells"] for h in WD["spells"][d])
    ok("SF21 the long rain's hourly depth stays under 7 mm against a lowest triggering depth of 12.5 mm",
       longest < 7.0 and min(fig["trigger"].values()) == 12.5, "%.2f mm" % longest)
    opened = [s for s in names if fig["routes"]["S1+S2+S3"][s]["class"] != cls[s]]
    for key, label in (("mapped_route", "matched rank for rank to the Rio Scuro weighing gauges"), ("radar_route", "adjusted to the stations by one factor")):
        rt = fig[key]
        away = [d["pct"] for k, d in rt["station"].items() if k != "Rio Scuro"]
        ok("SF22 the radar's depths %s land across the line on every open crossing and do not hold at the other stations' pixels" % label,
           all(rt["classes"][s] != cls[s] for s in opened) and len(away) == 5 and max(away) <= 75 and
           rt["station"]["Rio Scuro"]["scatter"] >= 1.2 * max(d["scatter"] for k, d in rt["station"].items() if k != "Rio Scuro"),
           "classes %s; %d to %d per cent of the stations' %d mm storms outside the valley, %d at Rio Scuro; scatter %.2f to %.2f" % (
               "".join(str(rt["classes"][s]) for s in names), min(away), max(away), rt["at_mm"], rt["station"]["Rio Scuro"]["pct"],
               min(d["scatter"] for d in rt["station"].values()), max(d["scatter"] for d in rt["station"].values())))
    ok("SF22 the radar holds fewer seasons than regulation 3.1 counts", fig["counts"]["radar_years"][1] - fig["counts"]["radar_years"][0] + 1 < fig["counts"]["seasons"],
       "%s against %d seasons" % (fig["counts"]["radar_years"], fig["counts"]["seasons"]))
    hq = [max(so[s]["halves"][how][i] for s in names) for how in ("qq", "pairs") for i in (0, 1)]
    ok("SF23 the two pixels matched rank for rank, unpaired: its odd and even seasons disagree on the depth three times as far as the paired mean's, "
       "and crossed with the battery it files the golden's classes", hq[1] >= 3.0 * hq[3] and hq[1] >= 1.0 and hq[0] > hq[2] and fig["more"]["site"]["classes_hold"],
       "depth %.2f against %.2f mm, storms a season %.2f against %.2f; %d crossed variants" % (hq[1], hq[3], hq[0], hq[2], fig["more"]["site"]["variants"]))
    offm = [(f_, round(x, 2)) for v_ in X["more"]["hail"] for f_, x in figure_values(P, v_, None, names).items() if not inside(x, fb[f_], RS.dec(f_))]
    ok("SF24 a hail storm's water laid on its hail-coded blocks alone, crossed with the battery: the golden's classes, every figure inside its band",
       fig["more"]["hail"]["classes_hold"] and not offm and all(inside(x, fb[RS.C3], 1) for x in X["c3"]["more"]) and
       o["hail water laid on the hail-coded blocks alone"]["storms"] > ref["golden"]["storms"],
       "%d crossed variants; Rio Scuro %d against %d seen; outside: %s" % (fig["more"]["hail"]["variants"], o["hail water laid on the hail-coded blocks alone"]["storms"],
                                                                       ref["seen"]["storms"], offm[:4]))
    per = {}
    for s in names:                          # 3.2 misread as the mean of each season's fifth largest storm
        st_ = P.S[P.M[s]["station"]]
        est, yr = P.transfer(s, xs[P.M[s]["station"]], "geo")[P.keep(s)], st_.year[P.keep(s)]
        per[s] = float(np.mean([np.sort(est[yr == y])[::-1][fig["regulation"]["times_a_season"] - 1] for y in sorted(set(yr))]))
    ok("SF25 the depth of 3.2 is filed as the depth reached in a mean of five or more storms a season; the mean of each season's fifth largest "
       "is another figure and the regulation's sentence does not read that way",
       max(abs(per[s] - fig["depth"][s]) for s in names) >= 0.3 and re.search(r"in\s+a\s+mean\s+of\s+five\s+or\s+more\s+storms\s+a\s+warm\s+season", reg) is not None,
       "; ".join("%s %.1f against %.1f" % (s, per[s], fig["depth"][s]) for s in names))

    # ------------------------------------------------------------------------------------- the referee and controls
    ok("referee: the estimate reproduces the weighing gauges and every shortcut misses by three times its error or more",
       all(abs(x["top"] - ref["seen"]["top"]) >= 3.0 * abs(ref["golden"]["top"] - ref["seen"]["top"]) for x in ref["rivals"].values()),
       "golden %.2f, seen %.2f" % (ref["golden"]["top"], ref["seen"]["top"]))
    ok("referee: no crossing stands in the research valley", all(P.M[s]["station"] != P.valley for s in names))
    ok("control: read as a calibration, the weighing gauges put the source areas at the bucket's own depth (nothing to carry)",
       abs(ref["source_over_bucket_raw"] - 1.0) < 0.05, "%.3f" % ref["source_over_bucket_raw"])
    ok("control: on rain storms the tips and the detector agree on timing", all(d["late_rain_pct"] < 0.5 for d in st.values()))
    # ------------------------------------------------------------------------------------------------ realism sweep
    ok("realism: tips to the whole second, never two in one second", all(np.all(np.diff(P.S[c].t) >= 1) for c in P.codes))
    ok("realism: every station's visit rounds slip (no fixed day of the month)",
       len({d_[8:] for d_ in open(os.path.join(target, pack.FILES["visits"])).read().split("\n")[1:400] if d_ and len(d_.split(",")) > 1
            for d_ in [d_.split(",")[1]]}) >= 8)
    ok("realism: the fitted loss differs by bucket model", len({round(d["loss_h_per_mm"], 5) for d in st.values()}) == 2)
    ok("realism: the account's left-over is noise once the loss is fitted (under 1.5 mm rms a station)", all(d["resid_rate"] < 1.5 for d in st.values()))
    blocks = open(os.path.join(os.path.dirname(HERE), "submission.md")).read() if os.path.exists(os.path.join(os.path.dirname(HERE), "submission.md")) else ""
    ok("the answer blocks carry no em dash and no design word", "\u2014" not in blocks and not re.search(r"\bstump|\breflex\b|\bcore\b", blocks))

    bad_rows = [r for r in ROWS if not r[1]]
    for label, good, detail in ROWS:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("%d checks, %d failed" % (len(ROWS), len(bad_rows)))
    return 1 if bad_rows else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
