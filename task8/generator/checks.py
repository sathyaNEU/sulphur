"""Every assertion of the build on the cut pack: the input gates, the never-filed list, the pack against the core's
arrays, the bar block (R1 to R7), every row of the fork table (SF1 to SF31), the pinning list read back from the
documents, the second implementation, the goldens against figures.json and the realism sweep.

    python3 task8/generator/checks.py [target]
"""
import csv
import glob
import json
import os
import re
import sys
import tempfile

import numpy as np
from openpyxl import load_workbook
from scipy.optimize import linear_sum_assignment

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import deliver  # noqa: E402
import docs  # noqa: E402
import load as L  # noqa: E402
import metadata  # noqa: E402
import pack  # noqa: E402
import results as RS  # noqa: E402
import verify as V  # noqa: E402
import world as WL  # noqa: E402

ROWS = []
M, BANKED = C.MEMBERS, C.BANKED
TASK = os.path.dirname(HERE)
NEVER = (r"\bblind|\bseen\b|anchor|\bcycle|\bphase|years[_ ]since|\bdual|\blink|offset|influenc|drawn to|understat|"
         r"compress|conservativ|lenien|sever(e|ity)|drift|tighten|comparab|\bcold\b|\bshare\b|\bslope|\bratio\b|"
         r"unsampled|not sampled|standards differ|different standards|\bbias|independen|second mark")
CONTROL = {docs.FILES["protocol"]: "A banked mark is a workshop portfolio mark awarded by a joining board",
           docs.FILES["code"]: "The mean difference of a sample is the mean, over the sampled portfolios",
           docs.FILES["scope"]: "The review covers every centre that entered candidates for the workshop portfolio"}


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond), str(detail)))
    return bool(cond)


def texts(target):
    """every word a reader can find in the pack: file names, headers, small files whole, workbook cells, the PDFs' text
    (through the verifier's own extractor)"""
    out = {}
    for path in sorted(glob.glob(os.path.join(target, "*"))):
        name = os.path.basename(path)
        if name.endswith(".csv"):
            with open(path, newline="") as fh:
                out[name] = fh.readline()
                if os.path.getsize(path) < 600000:
                    out[name] += " " + fh.read()
        elif name.endswith(".xlsx"):
            wb = load_workbook(path, read_only=True, data_only=True)
            out[name] = " ".join(wb.sheetnames) + " " + " ".join(
                str(c) for ws in wb for r in ws.iter_rows(values_only=True) for c in r if c is not None)
        elif name.endswith(".pdf"):
            out[name] = V.pdf_text(path)
    return out


def inside(v, band):
    return band[0] - 1e-9 <= round(float(v), 1) <= band[1] + 1e-9


def bands_of(fig):
    b = dict(fig["distance_band"])
    b.update({"%s %d" % (m, y): fig["by_series_band"][str(y)][m] for y in BANKED for m in M})
    b["whole"] = fig["whole_band"]
    return b


def cells_of(v):
    c = {m: v["pool"][m] for m in M}
    c.update({"%s %d" % (m, y): v["by"][y][m] for y in BANKED for m in M})
    c["whole"] = v["whole"] if "whole" in v else v["nat"]
    return c


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    X, fig_now, E_now, spec = RS.run(target)
    world, info, raw, WC = X["world"], X["info"], X["raw"], X["core"]
    ok("figures.json is the pack's: recomputed from target/ it is identical",
       json.loads(json.dumps(fig_now, sort_keys=True, default=float)) == fig)
    files = sorted(os.listdir(target))
    T = texts(target)
    bands = bands_of(fig)

    # ---------------------------------------------------------------- the input gates
    ok("gate: ten or more usable files", len(files) >= 10 and all(os.path.getsize(os.path.join(target, f)) > 200 for f in files),
       "%d files" % len(files))
    ext = {os.path.splitext(f)[1] for f in files}
    ok("gate: two file categories or more (spreadsheets as csv and xlsx, text as pdf)", {".csv", ".xlsx", ".pdf"} <= ext, ext)
    big = max(fig["mark_rows"].values())
    ok("gate: a CSV of 20,000 rows or more", big >= 20000, big)
    outc = [f for f in files if "outcomes" in f and f.endswith(".csv")]
    long_ = {f: sum(1 for _ in open(os.path.join(target, f))) for f in outc}
    ok("gate: a second CSV that runs 20 printed pages or more (an outcomes file at 50 lines a page)",
       max(long_.values()) >= 1000, long_)
    ok("gate: both large files carry mess to clean (a batch loaded twice; reissued records; entries with no mark)",
       sum(fig["repeat_rows"].values()) > 100 and all(info[b]["versions"] > len(raw[b]["outcomes"]) for b in C.BOARDS)
       and all((~raw[b]["marks"]["marked"]).sum() > 500 for b in C.BOARDS),
       {b: (info[b]["versions"] - len(raw[b]["outcomes"]), int((~raw[b]["marks"]["marked"]).sum())) for b in C.BOARDS})
    size = sum(os.path.getsize(os.path.join(target, f)) for f in files)
    ok("gate: the pack is 30 MB or more", size >= 30e6, "%.1f MB" % (size / 1e6))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dist = meta["distractor_files"]
    ok("gate: two or more files the analysis never reads, named only in metadata.json",
       len(dist) >= 2 and all(d in files for d in dist) and not any(re.search(r"distract|unused|decoy", f, re.I) for f in files), dist)
    ok("gate: metadata.json records every shipped file's source, date and licence", sorted(meta["files"]) == files,
       sorted(set(files) ^ set(meta["files"])))
    ok("gate: no file name names a judgment",
       not any(re.search(r"share|correct|adjust|estimate|convert|link|standardis(ed|ing)|cycle|rota|blind|truth", f, re.I)
               and not re.search(r"standardisation", f, re.I) for f in files))
    ok("gate: no file describes the data (no readme, dictionary, notes, manifest or schema, by name or by sheet)",
       not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook|definitions|guide", f, re.I) for f in files)
       and not any(re.search(r"notes|dictionary|definitions|readme", s, re.I)
                   for f in files if f.endswith(".xlsx") for s in load_workbook(os.path.join(target, f), read_only=True).sheetnames))
    heads = {f: T[f].split("\n")[0] for f in files if f.endswith(".csv")}
    desc = [f for f in files if f.endswith(".pdf") and len({h_ for hd in heads.values() for h_ in re.split(r"[,;]", hd.strip())
                                                            if len(h_) > 6 and h_ in T[f]}) >= 4]
    ok("gate: no document names four or more of the data files' columns", not desc, desc)
    # deleting the unused files leaves every figure where it was
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in dist:
            os.symlink(os.path.join(os.path.abspath(target), f), os.path.join(tmp, f))
    v_del = V.run(tmp)
    w_del = L.load(tmp)[0]
    g_del = C.view(w_del)
    ok("gate: with the three unused files deleted both implementations file the same figures",
       all(abs(g_del["pool"][b] - X["x"]["g"]["pool"][b]) < 1e-12 for b in M)
       and all(abs(v_del["pool"][b] - fig["distance_2dp"][b]) < 0.006 for b in M))

    # ---------------------------------------------------------------- the never-filed list
    for name, sentence in CONTROL.items():
        ok("control: %s is read back and holds its own sentence" % name, sentence in T[name] and len(T[name]) > 1500, len(T[name]))
    hits = {f: sorted(set(m.group(0).lower() for m in re.finditer(NEVER, t, re.I))) for f, t in T.items()}
    hits = {f: h for f, h in hits.items() if h}
    ok("never filed: no file, header, cell or document sentence carries the vocabulary of the three judgments", not hits, hits)
    ok("never filed: the control vocabulary is found by the same search (the word 'moderator' in every document)",
       all(re.search(r"moderator", T[f], re.I) for f in CONTROL))
    cols = " ".join(heads.values()).lower() + " " + " ".join(T[f][:300].lower() for f in files if f.endswith(".xlsx"))
    ok("never filed: no column named for a judgment or holding a result",
       not re.search(r"consensus|share|distance|estimate|expected|true|sampled_year|since|standard_|carrow_mark|merit", cols))
    ok("never filed: the scope letter gives the review's scope and no finding",
       not re.search(r"found|finding|conclu|result|higher|lower|above|below", T[docs.FILES["scope"]], re.I))
    ok("never filed: no document says how an estimate is made",
       not any(re.search(r"estimat|regress|model|adjusted for|corrected for|scaled|divid", T[f], re.I) for f in CONTROL))

    # ---------------------------------------------------------------- the documents' constants, read back by the verifier
    D = V.documents(target)
    ok("pinned: the protocol files 2.0 marks either way and the 2025 and 2026 series",
       D["line"] == C.LINE == fig["line"] and D["series"] == BANKED, (D["line"], D["series"]))
    ok("pinned: the code's schedule gives each board's rota and tolerance, and the rota is the one the sample records show",
       all(D["schedule"].get(b) == (C.BOARDS[b]["k"], int(C.BOARDS[b]["tol"])) for b in C.BOARDS)
       and all(D["schedule"][b][0] == fig["rota_years"][b] for b in C.BOARDS), D["schedule"])
    ok("pinned: the scope letter gives eight portfolios a centre and the review file holds eight or fewer for each",
       D["review_per_centre"] == "eight" and fig["review_portfolios"] <= 8 * fig["centres"][C.REFEREE[0]]
       and fig["review_portfolios"] > 7.5 * fig["centres"][C.REFEREE[0]], fig["review_portfolios"])
    for b in C.BOARDS:
        o, w = raw[b]["outcomes"], world["B"][b]
        ix = {r: i for i, r in enumerate(info[b]["rolls"])}
        ci, ti = o["roll"].map(ix).to_numpy(), (o["series"] - C.YEARS[0]).to_numpy()
        g = w["G"][ci, ti]
        tol = D["schedule"][b][1]
        good = (o["sampled"].to_numpy() == w["ns"][ci, ti]).all() and (-o["applied"].to_numpy() == w["adj"][ci, ti]).all()
        good = good and ((np.abs(g) > tol) == (w["adj"][ci, ti] != 0)).all()
        good = good and (np.where(np.abs(g) > tol, np.floor(np.abs(g) + 0.5) * np.sign(g), 0) == w["adj"][ci, ti]).all()
        if not o["mean_diff"].isna().all():
            good = good and (np.abs(o["mean_diff"].to_numpy() - g) < 0.0051).all()
        ok("code 4.1 to 4.3: every outcome record of %s reproduces from its sample marks (count, mean difference, tolerance, "
           "whole-mark adjustment)" % b, good and len(o) == int(w["samp"].sum()), len(o))
        m = raw[b]["marks"]
        mm = m[m["marked"]]
        d = (mm["centre_mark"] - mm["awarded_mark"]).groupby([mm["roll"], mm["series"]]).agg(["min", "max"])
        ok("SF9 an adjustment is applied to every candidate of the centre in the series: %s" % b,
           (d["min"] == d["max"]).all() and re.search(r"the mark of every candidate of the centre in that series", D["code"]))

    # ---------------------------------------------------------------- the pack against the core's arrays
    for b in C.BOARDS:
        a, w = WC["B"][b], world["B"][b]
        ok("pack against core: %s candidates, sample years, sample sizes, adjustments and rota are the core's" % b,
           (a["ncand"] == w["ncand"]).all() and (a["samp"] == w["samp"]).all() and (a["adj"] == w["adj"]).all()
           and (a["ns"][a["samp"]] == w["ns"][w["samp"]]).all() and a["P"]["k"] == w["P"]["k"])
        dg = float(np.nanmax(np.abs(a["G"] - w["G"])))
        dm = float(np.abs(a["mbar"] - w["mbar"]).max())
        ok("pack against core: %s recorded differences and mean marks are the core's to whole-mark rounding" % b,
           dg < 0.3 and dm < 0.1, (round(dg, 3), round(dm, 3)))
        # the files list a meeting's scripts in their own order: pair each of the core's with its nearest in the meeting
        dx = dy = dgp = 0.0
        one = True
        for yy in np.unique(a["ex_year"]):
            ia, iw = np.flatnonzero(a["ex_year"] == yy), np.flatnonzero(w["ex_year"] == yy)
            cost = (1000 * (a["ex_x"][ia][:, None] - w["ex_x"][iw][None, :]) ** 2 + (a["ex_y"][ia][:, None] - w["ex_y"][iw][None, :]) ** 2
                    + (a["ex_gap"][ia][:, None] - w["ex_gap"][iw][None, :]) ** 2)
            one = one and len(ia) == len(iw)
            j = linear_sum_assignment(cost)[1]
            dx = max(dx, float(np.abs(a["ex_x"][ia] - w["ex_x"][iw][j]).max()))
            dy = max(dy, float(np.abs(a["ex_y"][ia] - w["ex_y"][iw][j]).max()))
            dgp = max(dgp, float(np.abs(a["ex_gap"][ia] - w["ex_gap"][iw][j]).max()))
        ok("pack against core: %s meeting scripts carry the core's consensus, live difference and agreed marks" % b,
           # a team's size now varies by meeting (posts filled late, extra appointments), so the pack's consensus sits
           # within 0.03 of the core's and the gap to the whole-mark agreed mark within the rounding plus that
           one and dx < 0.03 and dy <= 0.5 and dgp <= 0.5 + 0.03, (one, round(dx, 3), round(dy, 3), round(dgp, 3)))
    dl, one = 0.0, True
    for a, l in zip(WC["D"], world["D"]):
        cost = (a["ra"][:, None] - l["ra"][None, :]) ** 2 + (a["rb"][:, None] - l["rb"][None, :]) ** 2
        one = one and len(a["ra"]) == len(l["ra"])
        j = linear_sum_assignment(cost)[1]
        dl = max(dl, float(np.abs(a["ra"] - l["ra"][j]).max()), float(np.abs(a["rb"] - l["rb"][j]).max()))
    ok("pack against core: the two-board moderators' marks carry the core's deviations at both meetings", one and dl < 0.03,
       (one, round(dl, 4)))
    ok("pack against core: the review marks carry the core's review", float(np.abs(WC["review"] - world["review"]).max()) < 0.1)
    gc = C.view(dict(WC, cache={}))
    ok("pack against core: the estimate on the pack is the core's to 0.15 marks and files the core's outcomes",
       all(abs(gc["pool"][b] - X["x"]["g"]["pool"][b]) < 0.15 for b in M) and RS.call_of(gc["pool"]) == fig["call"],
       {b: round(gc["pool"][b] - X["x"]["g"]["pool"][b], 3) for b in M})
    ok("the world's own values sit on the estimate's side of every tolerance, within half a mark",
       fig["truth_call"] == fig["call"] and all(abs(fig["truth"][b] - fig["distance_2dp"][b]) < 0.5 for b in M),
       {b: round(fig["truth"][b] - fig["distance_2dp"][b], 2) for b in M})
    ok("the core on the cut pack: level 5, one judgment lost earns 50 or under, the reflex route 30 or under, the rigorous "
       "standard route 50 or under", fig["rubric"]["level"] == 5 and not fig["rubric"]["fails"]
       and max(fig["rubric"]["one_lost"].values()) <= 50 and fig["rubric"]["reflex"] <= 30 and fig["rubric"]["rigorous"] <= 50,
       fig["rubric"])

    # ---------------------------------------------------------------- the bar block
    ok("R1 the raw material ships: every portfolio mark, every sampled portfolio's two marks, every moderator's mark on every "
       "meeting script and every appointment, and both implementations read them",
       fig["mark_rows_total"] > 1e6 and sum(len(raw[b]["samples"]) for b in C.BOARDS) > 100000
       and min(fig["trial_scripts"].values()) == 480 and sum(len(raw[b]["trial"]) for b in C.BOARDS) > 100000
       and fig["appointments"] > 300, (sum(len(raw[b]["samples"]) for b in C.BOARDS), sum(len(raw[b]["trial"]) for b in C.BOARDS)))
    base = V.run(target)
    for label, how in (("R2 a reissued moderation record read at its first issue", dict(first_version=True)),
                       ("R2 the batch loaded twice counted twice", dict(keep_repeats=True)),
                       ("R2 withdrawn and absent entries counted as candidates", dict(count_unmarked=True)),
                       ("R2 a meeting mark not given filled with that marker's mean in place of left out", dict(fill_blank=True))):
        v = V.run(target, **how)
        out = [k for k, val in cells_of(v).items() if not inside(val, bands[k])]
        ok("%s: every graded figure stays in its band and the outcomes stay" % label,
           not out and v["call"] == base["call"] and inside(100 * v["share"][C.PULL_BOARD], fig["c1_band"])
           and inside(v["cycle"][C.CYCLE_BOARD][1], fig["c2_band"]) and inside(v["standard"][C.LINK_BOARD], fig["c3_band"]),
           (out, {b: round(v["pool"][b] - base["pool"][b], 3) for b in M}))
    h = fig["hurried"]
    ok("R3 the careful but hurried pass files 100 per cent, no level after a sample and no standard: each outside its band",
       not inside(h["c1"], fig["c1_band"]) and not inside(h["c2"], fig["c2_band"]) and not inside(h["c3"], fig["c3_band"]))
    lat = X["x"]["lat"]
    out_n = {k: sum(not inside(val, bands[c]) for c, val in cells_of(lat[k]).items()) for k in lat}
    ok("R3 the careful but hurried pass lands none of the nineteen ask figures", out_n[RS.REFLEX] == 19, out_n[RS.REFLEX])
    ok("R3 each judgment lost alone moves seventeen or more of the nineteen ask figures outside their bands",
       all(out_n[s] >= 17 for s in C.SIDS), {s: out_n[s] for s in C.SIDS})
    ok("R3 each judgment lost alone moves its own component and leaves the other two",
       not inside(lat["S1"]["pull"], fig["c1_band"]) and inside(lat["S1"]["cycle"], fig["c2_band"]) and inside(lat["S1"]["link"], fig["c3_band"])
       and not inside(lat["S2"]["cycle"], fig["c2_band"]) and inside(lat["S2"]["pull"], fig["c1_band"])
       and not inside(lat["S3"]["link"], fig["c3_band"]) and inside(lat["S3"]["cycle"], fig["c2_band"]))
    wrong = {k: tuple(RS.call_of(lat[k]["pool"])) for k in lat}
    ok("R3 no shortcut files the estimate's outcomes, the three single losses land on three different wrong sets and the "
       "seven on five or more", all(list(v) != fig["call"] for v in wrong.values()) and len({wrong[s] for s in C.SIDS}) == 3
       and len(set(wrong.values())) >= 5, len(set(wrong.values())))
    ok("R3 the direct and the rigorous standard routes file wrong outcomes",
       fig["routes"]["direct"]["call"] != fig["call"] and fig["routes"]["rigorous"]["call"] != fig["call"])
    rows_ = sum((raw[b]["marks"].duplicated(["series", "roll", "cand"]).sum() for b in C.BOARDS))
    ok("R4 no plant: no memo, draft or note ships, no document carries a figure for any board's marks against any standard, and "
       "once the repeated batch is dropped no candidate repeats",
       rows_ == 0 and not any(re.search(r"memo|draft|note|minute|briefing", f, re.I) for f in files)
       and not any(re.search(r"\d\.\d+ marks (above|below|higher|lower)", T[f]) for f in CONTROL))
    yr = {b: [C.slope(world["B"][b]["ex_x"][world["B"][b]["ex_year"] <= 2020], world["B"][b]["ex_y"][world["B"][b]["ex_year"] <= 2020]),
              C.slope(world["B"][b]["ex_x"][world["B"][b]["ex_year"] > 2020], world["B"][b]["ex_y"][world["B"][b]["ex_year"] > 2020])]
          for b in C.BOARDS}
    ok("R5 the share recorded is under 80 per cent in all seven boards, Carrow among them, on the earlier and the later meetings alike",
       all(v < 0.8 for vs in yr.values() for v in vs) and all(fig["share_pct"][b] < 80 for b in C.BOARDS),
       {b: [round(v, 2) for v in vs] for b, vs in yr.items()})
    ok("R5 centres mark lower after a sample in all six boards on a rota of two or three years, by 1.0 mark or more in the first year",
       all(fig["cycle"][b][0] <= -1.0 for b in M), {b: fig["cycle"][b] for b in M})
    ok("R5 all six joining boards' standards stand 0.4 marks or more from Carrow's, on both sides",
       all(abs(fig["standard"][b]) >= 0.4 for b in M) and min(fig["standard"].values()) < 0 < max(fig["standard"].values()), fig["standard"])
    ok("R5 where they decide nothing: Dunmoyle carries all three (a share of 48 per cent, 1.5 marks after a sample, a standard "
       "1.7 above) and every single loss still converts it down",
       all("Dunmoyle down" in wrong[s] for s in C.SIDS) and fig["share_pct"]["Dunmoyle"] < 60 and fig["cycle"]["Dunmoyle"][0] < -1
       and fig["standard"]["Dunmoyle"] > 1)
    ok("R5 and R6 no one thing: each judgment fixed alone on the hurried pass rescues two results or fewer of the six it lost, and "
       "files wrong outcomes", all(len(hn["rescues"]) <= 2 for hn in E["hints"])
       and all(j["alone"]["answer"] != fig["call"] for j in E["factorial"]["judgments"] if j["kind"] == "stump"),
       [hn["rescues"] for hn in E["hints"]])
    ok("R7 the battery: every variant files the estimate's outcomes, twelve or more of them, the nearest 0.3 marks or more from a tolerance",
       fig["family_calls_all_golden"] and fig["variants"] >= 12 and fig["nearest_variant"]["distance"] >= 0.3,
       (fig["variants"], fig["nearest_variant"]))
    ok("R7 each fitted input moved one spread either way, alone and all three together, files the same outcomes",
       all(p["call_holds"] for p in fig["perturbations"]) and len(fig["perturbations"]) == 14,
       min(p["nearest"] for p in fig["perturbations"]))
    rf = fig["referee"]
    ok("R7 the review rules between routes: the estimate within 0.25 marks, every shortcut 1.0 or more away",
       rf["off"] <= 0.25 and min(v["off"] for v in rf["rivals"].values()) >= 1.0, rf)

    # ---------------------------------------------------------------- the fork table
    P = D["protocol"]
    names = " | ".join(fig["variant_names"])
    ok("SF1 a banked mark is the mark as awarded after moderation (protocol 2.1)", "as awarded by the board after moderation" in P)
    ok("SF2 every mark of the two series (protocol 2.1), entries with no mark out (2.3)",
       "in the 2025 series or the 2026 series" in P and "carries no mark and is outside this protocol" in P)
    ok("SF3 Carrow's standard is its principal moderator's agreed marks as applied in 2026 (protocol 3.1)",
       re.search(r"standard of the agreed marks of the principal moderator of Carrow Awards .* as applied in Carrow's moderation of the 2026 series", P))
    ok("SF4 a distance is a mean over candidates (protocol 4.1); the mean over centres is another figure",
       "the mean, over its candidates with a banked mark" in P)
    ok("SF5 the test is on the two series together (protocol 4.1), and each series alone files the same side for every board",
       "the 2025 and 2026 series taken together" in P
       and all(C.band(X["x"]["g"]["by"][y][b]) == C.band(X["x"]["g"]["pool"][b]) for y in BANKED for b in M))
    ok("SF6 the tolerance is 2.0 marks or more (protocol 4.2): unrounded, to 0.1 and to a whole mark the estimate files the same outcomes",
       "2.0 marks or more above" in P and "2.0 marks or more below" in P
       and all(C.band(round(X["x"]["g"]["pool"][b], n)) == C.band(X["x"]["g"]["pool"][b]) for b in M for n in (0, 1)))
    ok("SF7 the conversion is the distance, held to one decimal place (protocol 4.2, 4.3)",
       "converted down by the distance" in P and "held to one decimal place" in P
       and all(abs(fig["converted"][b] - abs(fig["distance"][b])) < 1e-9 for b in fig["converted"]))
    ok("SF8 a sample's difference is the centre's mark less the moderator's (code 4.1), the sign the outcome records carry",
       "of the centre's mark less the moderator's mark" in D["code"])
    v1 = V.run(target, first_version=True)
    ok("SF10 a reissued record replaces the earlier one (code 4.5); read at the first issue no figure moves",
       "The reissued record replaces the earlier one" in D["code"] and all(abs(v1["pool"][b] - base["pool"][b]) < 1e-9 for b in M))
    ok("SF11 the meetings the share is fitted on: the last five years and year by year are in the battery",
       "last five years of trial scripts" in names and "year by year and averaged" in names)
    ok("SF12 the form of the share: through the origin and with the consensus' own error allowed for are in the battery",
       "through the origin" in names and "consensus' own error" in names)
    ok("SF13 the level after a sample: each centre's own change, and the two averaged, are in the battery",
       "each centre's own change in mean mark" in names and "own change averaged" in names)
    ok("SF14 the series the levels are fitted on: six, twelve and weighted by candidates are in the battery",
       "last six years" in names and "last twelve years" in names and "weighted by candidates" in names)
    ok("SF15 the last sample: the last two averaged is in the battery", "last two samples averaged" in names)
    ok("SF16 how the links are pooled: trimmed, at the median, unweighted, and both sets of six shortest paths are in the battery",
       all(s in names for s in ("links trimmed", "links at the median", "links unweighted", "six shortest paths", "one link a board")))
    ok("SF17 agreed marks against the consensus at the median is in the battery", "agreed marks at the median" in names)
    rc = fig["rival_review_calibration"]
    ok("SF18 the review is a check: as Dunmoyle's own answer it lies inside Dunmoyle's three bands, and carried to the other "
       "boards as a calibration it files wrong outcomes for three boards or more",
       all(inside(rf["raw_all_centres"], bands[k]) for k in ("Dunmoyle", "Dunmoyle 2025", "Dunmoyle 2026"))
       and len(rc["boards_wrong"]) >= 3 and "in the 2023 series" in D["scope"], rc["boards_wrong"])
    blocks = open(os.path.join(TASK, "submission.md")).read()
    ok("SF19 stated precision: every distance to 0.1 mark with its band in the answer blocks, and the prompt dictates no rounding",
       all("%s %.1f (%.1f to %.1f)" % (b, fig["distance"][b], *fig["distance_band"][b]) in blocks for b in M)
       and not re.search(r"round|decimal|nearest", open(os.path.join(TASK, "prompt.txt")).read(), re.I))
    simple = float(np.mean([X["x"]["g"]["pool"][b] for b in M]))
    ok("SF20 the joining boards as a whole are a mean over every candidate (protocol 5.1); the mean of the six distances is another figure",
       "every candidate with a banked mark at any joining board" in P and abs(simple - X["x"]["g"]["nat"]) > 0.05, round(simple, 3))
    ok("SF21 the reference for the share: fitted on the agreed marks in place of the consensus is in the battery",
       "fitted on the agreed marks in place of the consensus" in names)
    pr = fig["rival_plain_ratio"]
    ok("SF22 a slope or a ratio of means: the ratio with the consensus centred is in the battery, and the plain ratio lands "
       "inside every band with the same outcomes", "mean live difference over the mean cold difference" in names
       and not pr["outside"] and pr["call"] == fig["call"], pr["outside"])
    ok("SF23 a marker's own mark in the consensus: left out is in the battery", "own mark left out of the consensus" in names)
    ok("SF24 the meetings the links are read on: 2023 to 2026 is in the battery", "links on the 2023 to 2026 meetings" in names)
    ok("SF25 the meetings the agreed marks are read on: 2020 to 2026 is in the battery", "consensus on the 2020 to 2026 meetings" in names)
    ab, ca = fig["rival_awarded_base"], fig["rival_cycle_on_awarded"]
    ok("SF26 which mark the levels after a sample are fitted on: the awarded mark as the base throughout lands inside every band "
       "with the same outcomes; awarded-mark levels added to a sample measured on the centre's mark stand 0.5 or more from the "
       "review and further than the estimate by 0.4",
       not ab["outside"] and ab["call"] == fig["call"] and ca["referee_off"] >= 0.5 and ca["referee_off"] - rf["off"] >= 0.4,
       (ab["outside"], ca["referee_off"]))
    sm = fig["rival_share_by_moderator"]
    ok("SF27 the grain of the share: one a moderator, shrunk to the board's, lands inside every band with the same outcomes",
       not sm["outside"] and sm["call"] == fig["call"], sm["between"])
    rs_ = fig["rival_recent_share"]
    bs_ = fig["beside"]
    ok("SF28 the meetings the share is read on, and the series the levels are read on: the share from recent meetings "
       "alone (with every form of the links and the levels) and the levels on all fifteen series file the same outcomes "
       "0.3 marks or more from a tolerance, every stated range holds every one, and the share's own range holds them",
       all(not v["outside"] and v["call"] == fig["call"] for v in rs_.values()) and bs_["calls_all_golden"]
       and not bs_["outside"] and bs_["rebuilds"] >= 150 and bs_["nearest"]["distance"] >= 0.3
       and fig["c1_band"][0] <= bs_["share_pct"][0] and bs_["share_pct"][1] <= fig["c1_band"][1] - 0.1,
       (bs_["rebuilds"], bs_["nearest"], bs_["share_pct"]))
    om_ = fig["rival_own_mark"]
    ok("SF31 what the share is fitted against: one marker's own unseen mark in place of the consensus moves two boards or "
       "more, is 1 mark or more from the review and ten times further than the estimate, and divided by that mark's "
       "own slope on the consensus difference returns the estimate's outcomes inside every range",
       len(om_["boards_wrong"]) >= 2 and om_["referee_off"] >= 1.0 and om_["referee_off"] >= 10 * rf["off"]
       and om_["corrected_call"] == fig["call"] and not om_["corrected_outside"]
       and max(om_["reliability"].values()) <= 0.9,
       (om_["boards_wrong"], om_["referee_off"], om_["reliability"], om_["corrected_outside"]))
    ok("a team is not the same size at every meeting: each board's marks a script run over four or more values",
       all(info[b]["count_max"] - info[b]["count_min"] >= 4 for b in C.BOARDS),
       {b: (info[b]["count_min"], info[b]["count_max"]) for b in C.BOARDS})
    cs_ = fig["rival_consensus_standard"]
    code_, prot_ = T[docs.FILES["code"]], T[docs.FILES["protocol"]]
    ok("SF29 whose marks are a board's standard: the team's consensus read as the standard brings Ardkeel to within 0.25 of the "
       "tolerance, and the Code's 5.4 and the protocol's 3.1 file the principal's agreed marks",
       abs(cs_["carrow_only"]["Ardkeel"] - C.LINE) < 0.25 and abs(cs_["every_board"]["Ardkeel"] - C.LINE) < 0.25
       and re.search(r"5\.4[^.]*agreed", code_) and re.search(r"3\.1[^.]*agreed", prot_),
       (cs_["carrow_only"]["Ardkeel"], cs_["every_board"]["Ardkeel"]))
    nn_ = fig["rival_no_netting"]
    ok("SF30 which mark is banked: the centre's mark with no adjustment netted moves Fennor and Gortavale, and the protocol's "
       "2.1 files the mark awarded after moderation",
       nn_["boards_wrong"] == ["Fennor", "Gortavale"] and re.search(r"2\.1[^.]*award", prot_, re.I), nn_["boards_wrong"])
    ok("the Code's 5.2 is true of every meeting on file: 40 scripts a meeting at every board",
       "40 portfolios" in code_ and all((raw[b]["scripts"].groupby("meeting").size() == 40).all() for b in C.BOARDS))
    ok("the standard route as stated: the record with each board's own meeting severity added files wrong outcomes and "
       "stands 3 marks or more from the review", fig["routes"]["rigorous"]["call"] != fig["call"]
       and rf["rivals"]["rigorous"]["off"] >= 3.0, rf["rivals"]["rigorous"])
    reg = {}
    with open(os.path.join(target, pack.FILES["register"]), newline="") as fh:
        for r in csv.DictReader(fh):
            reg.setdefault(r["registration_no"], set()).add(r["board"])
    seen_ = {}
    for b in C.BOARDS:
        for m_ in raw[b]["trial"]["moderator"].unique():
            if str(m_).startswith("MR"):
                seen_.setdefault(m_, set()).add(b)
    ok("the register's two-board moderators are the registration numbers that mark at two boards' meetings, and no number "
       "marks at three", {k for k, v in reg.items() if len(v) > 1} == {k for k, v in seen_.items() if len(v) > 1}
       and max(len(v) for v in seen_.values()) == 2, fig["two_board_people"])

    # ---------------------------------------------------------------- the second implementation
    cmp_ = V.compare(base, fig)
    bad_ = [(lab, a, c) for lab, a, c, good in cmp_ if not good]
    ok("verify: the second implementation, from the shipped files alone, agrees on every figure it shares with figures.json",
       not bad_ and len(cmp_) >= 55, bad_[:5])
    for k in RS.KEYS:
        v = V.run(target, lost=tuple(k.split("+")))
        ok("verify: the route '%s' files the same figures in both implementations" % RS.ROUTE_NAME[k],
           all(abs(v["pool"][b] - fig["routes"][k]["distance"][b]) < 0.006 for b in M),
           {b: round(v["pool"][b] - fig["routes"][k]["distance"][b], 3) for b in M})

    # ---------------------------------------------------------------- the goldens
    gold = os.path.join(TASK, "golden")
    ok("golden: exactly the two files the prompt asks for", sorted(os.listdir(gold)) == sorted(deliver.FILES.values()), os.listdir(gold))
    wb = load_workbook(os.path.join(gold, deliver.FILES["wb"]), data_only=True)
    ws = wb.worksheets[0]
    got = {ws.cell(row=r, column=1).value: [ws.cell(row=r, column=c).value for c in range(2, 10)] for r in range(5, 12)}
    ok("golden: the first sheet states the conversion and holds each board's distance, band, series figures and outcome from figures.json",
       ws.title == "Conversion" and str(ws["A1"].value).startswith("Convert ")
       and all(got[b][1] == fig["distance"][b] and got[b][3] == fig["by_series"]["2025"][b] and got[b][4] == fig["by_series"]["2026"][b]
               and got[b][2] == "%.1f to %.1f" % tuple(fig["distance_band"][b]) for b in M)
       and got["Joining boards as a whole"][1] == fig["whole"] and len(ws._charts) == 1, ws["A1"].value)
    ok("golden: the workbook's sheets are named for what they hold and none is a default",
       wb.sheetnames == ["Conversion", "Share recorded", "Years after a sample", "Standards", "2023 review", "Sensitivity",
                         "Routes", "Notes"], wb.sheetnames)
    with open(os.path.join(gold, deliver.FILES["csv"]), newline="") as fh:
        crow = list(csv.DictReader(fh))
    agg = {}
    for r in crow:
        k = (r["board"], int(r["series"]))
        n, d = int(r["candidates_with_banked_mark"]), float(r["distance_from_carrow_standard_marks"])
        agg[k] = (agg.get(k, (0, 0.0))[0] + n, agg.get(k, (0, 0.0))[1] + n * d)
    ok("golden: the CSV holds one row per centre and series, and its candidate-weighted means are the workbook's figures",
       len(crow) == fig["csv_rows"] == sum(2 * fig["centres"][b] for b in M)
       and all(abs(agg[b, y][1] / agg[b, y][0] - X["x"]["g"]["by"][y][b]) < 0.005 for b in M for y in BANKED)
       and all(agg[b, y][0] == fig["banked_candidates"][b][str(y)] for b in M for y in BANKED), len(crow))
    vc = base["centre"]
    worst = max(abs(float(r["distance_from_carrow_standard_marks"]) - vc[r["board"], int(r["series"])][int(r["roll_no"])][1]) for r in crow)
    ok("golden: every centre's figure in the CSV is the second implementation's to 0.01", worst < 0.0101, round(worst, 4))
    ok("the answer blocks carry no em dash and no design word",
       "—" not in blocks and not re.search(r"\bstump|\breflex\b|\bcore\b|golden|\bbattery\b|\bvariant", blocks))
    ok("the answer blocks state each refused route with its figure",
       all(s in blocks for s in ("plain ratio", "awarded mark", "calibration", "for each moderator", "own mark")))

    # ---------------------------------------------------------------- the realism sweep
    cen = {}
    with open(os.path.join(target, pack.FILES["centres"]), newline="") as fh:
        for r in csv.DictReader(fh):
            cen.setdefault(r["board"], []).append(r)
    steps = {b: len(set(np.diff([int(r["roll_no"]) for r in v]).tolist())) for b, v in cen.items()}
    ok("realism: no board's roll numbers run at one constant step", min(steps.values()) >= 3, steps)
    nm = [r["centre_name"] for v in cen.values() for r in v]
    shapes = {re.sub(r"^\S+\s+", "", n) for n in nm}
    ok("realism: centre names take more than two shapes and are not in alphabetical order",
       len(shapes) > 4 and nm != sorted(nm) and len(set(nm)) > 0.85 * len(nm), (len(shapes), len(set(nm)), len(nm)))
    ok("realism: every board's share, first-year level and standard is its own (no two boards within 0.5 per cent, 0.03 and "
       "0.03 marks on all three)", all(abs(fig["share_pct"][a] - fig["share_pct"][b]) > 0.5 or abs(fig["cycle"][a][0] - fig["cycle"][b][0]) > 0.03
                                        or abs(fig["standard"][a] - fig["standard"][b]) > 0.03 for a in M for b in M if a < b))
    adjp = fig["adjusted_pct"]
    ok("realism: boards adjust unevenly (the share of sampled centres adjusted runs from under 6 to over 25 per cent)",
       min(adjp.values()) < 6 and max(adjp.values()) > 25, adjp)
    sizes = np.concatenate([world["B"][b]["ncand"][:, -1] for b in C.BOARDS])
    ok("realism: centres vary tenfold in size and no size is shared by more than a twentieth of them",
       np.percentile(sizes, 95) / np.percentile(sizes, 5) >= 8 and np.bincount(sizes.astype(int)).max() < len(sizes) / 20,
       (np.percentile(sizes, 5), np.percentile(sizes, 95)))
    lastd = np.concatenate([np.array([v % 10 for v in raw[b]["marks"]["centre_mark"].dropna().astype(int).tolist()[:40000]]) for b in C.BOARDS])
    freq = np.bincount(lastd, minlength=10) / len(lastd)
    ok("realism: portfolio marks do not heap on round numbers (no last digit holds more than 12 per cent)", freq.max() < 0.12, freq.round(3))
    issued = {b: raw[b]["outcomes"] for b in C.BOARDS if "when" in raw[b]["outcomes"]}
    ok("realism: outcome records are issued on uneven days through June and July, reissues weeks later, none after its board's export",
       all(o["when"].dt.day.nunique() > 20 and o["when"].max().year <= 2026 for o in issued.values()))
    stamps = {f: os.path.getmtime(os.path.join(target, f)) for f in files}
    ok("realism: no two files share a save time and none is saved after the as-of date",
       len(set(stamps.values())) == len(stamps) and max(stamps.values()) < 1801958400, len(set(stamps.values())))
    ok("realism: each document's own date falls on or after the last event it describes (the protocol after its approval, the "
       "code's revision in January 2024, the scope letter before the review's return)",
       "approved by the Office of the Examinations Regulator on 14 December 2026" in P and "revised January 2024" in D["code"]
       and "12 September 2023" in D["scope"] and "6 October 2023" in D["scope"])
    ok("metadata.json names the decision, the deliverables and the provenance and no method, figure or mechanism",
       not re.search(r"share|cycle|link|stump|anchor|blind|reflex|\d\.\d", json.dumps({k: v for k, v in meta.items() if k != "files"}), re.I)
       and not re.search(NEVER, json.dumps(meta["files"]), re.I))

    bad = [r for r in ROWS if not r[1]]
    for label, good, detail in ROWS:
        if not good:
            print("FAIL  %s  %s" % (label, detail[:400]))
    print("checks: %d assertions, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
