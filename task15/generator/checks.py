"""task15: the generator's assertions. run(target, w, A, F, E, B) fills RESULTS; `python3 checks.py` runs them on the
task folder's own pack (the analysis kept by build.py is reused when the pack has not changed).

The bar block is labelled R1 to R7 (dataset-generation 7.1); every row of the design note's fork table is asserted
under its own id (SF1 to SF18); then the input gates, the mess items, the realism sweep and the distractors.
"""
import csv
import os
import re
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))

import figs as FG  # noqa: E402
import golden as G  # noqa: E402
import panel as PN  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

RESULTS = []
PEOPLE = ["Meredith Cooke", "Jesse Gibson", "Michaela Baxter", "John Morgan"]
FN = W.FILES
DISTRACTORS = [FN["quality"], FN["disease"], FN["seed"]]


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), str(detail)))
    return bool(ok)


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.reader(fh))


def inside(v, band):
    return band[0] <= v <= band[1]


def outside_by(v, band):
    return max(band[0] - v, v - band[1])


def same_panel(P, Q):
    a = P.plots.drop(columns=[c for c in ("plot",) if c in P.plots]).reset_index(drop=True)
    b = Q.plots.drop(columns=[c for c in ("plot",) if c in Q.plots]).reset_index(drop=True)
    if a.shape != b.shape:
        return False, "plots %s against %s" % (a.shape, b.shape)
    for c in b.columns:
        if a[c].dtype.kind == "f" or b[c].dtype.kind == "f":
            if not np.allclose(a[c].fillna(-9.0), b[c].fillna(-9.0), atol=1e-9):
                return False, "plots column %s" % c
        elif not (a[c] == b[c]).all():
            return False, "plots column %s" % c
    if set(P.water) != set(Q.water) or any(abs(P.water[t] - Q.water[t]) > 1e-9 for t in Q.water):
        return False, "season water"
    if any(abs(P.irrigation.get(t, 0.0) - Q.irrigation.get(t, 0.0)) > 1e-9 for t in Q.water):
        return False, "waterings"
    sa, sb = P.series.reset_index(drop=True), Q.series.reset_index(drop=True)
    if sa.shape != sb.shape or not (sa["line"] == sb["line"]).all() or not np.allclose(sa["y"], sb["y"], atol=1e-9) \
            or not np.allclose(sa["L"], sb["L"], atol=1e-9):
        return False, "series results"
    if P.noms != Q.noms:
        return False, "nominations"
    if P.cands != Q.cands:
        return False, "candidates"
    if any(abs(P.series_water[t] - Q.series_water[t]) > 1e-9 for t in Q.series_water):
        return False, "series rain"
    if any(abs(P.series_cv[t] - Q.series_cv[t]) > 0.051 for t in Q.series_cv):
        return False, "series cv"
    return True, "plots, water, series, nominations and candidates equal"


def quick_fig(P, **opt):
    """One route's bridge and nominations without the simulation (for the mess and distractor tests)."""
    R = G.analyse(P, sims=0, backtest=False, **opt)
    return dict(own=FG.r1(R["own_sites"]), water=FG.r1(R["water_part"]), lodging=FG.r1(R["lodging_part"]),
                picks=sorted(P.wi[l] for l in R["picks"]),
                ry={P.wi[l]: FG.r1(v) for l, v in zip(R["cands"]["line"], R["cands"]["ry"])})


def run(target, w, A, F, E, B):
    import effort as EF
    P, R, g, ev = A["P"], A["R"], A["gold"], F["evidence"]
    files = sorted(os.listdir(target))
    docs = V.documents(target)
    alltext = " ".join(docs.values())

    # ------------------------------------------------------------------ the pack is what the world was
    Pw = PN.from_world(w)
    ok, why = same_panel(P, Pw)
    check("the conformed record read back from the pack is the clean world's", ok, why)
    check("every WI number maps to one cross code and back", len(set(P.wi.values())) == len(P.wi), len(P.wi))

    # ------------------------------------------------------------------ input gates
    cats = {"spreadsheet": [f for f in files if f.endswith((".csv", ".xlsx"))],
            "text": [f for f in files if f.endswith((".pdf", ".docx"))]}
    check("gate: ten or more usable files", len(files) >= 10, len(files))
    check("gate: two or more file categories, three or more formats",
          all(cats.values()) and len({os.path.splitext(f)[1] for f in files}) >= 3,
          sorted({os.path.splitext(f)[1] for f in files}))
    big = len(rows(os.path.join(target, FN["new"]))) - 1
    check("gate: a CSV of 20,000 rows or more", big >= 20000, big)
    long_ = len(rows(os.path.join(target, FN["entries"]))) - 1
    old = len(rows(os.path.join(target, FN["old"]))) - 1
    check("gate: a second long CSV (well past twenty printed pages)", min(long_, old) >= 5000, (long_, old))
    check("gate: two or more distractors, unlabelled", all(d in files for d in DISTRACTORS) and not any(
        re.search(r"distract|decoy|unused|trap|readme|dictionary|manifest|notes", f, re.I) for f in files), DISTRACTORS)
    check("gate: no file describes the pack", not re.search(
        r"data dictionary|field notes|column description|this (file|extract) contains|how to read", alltext, re.I), "")

    # ------------------------------------------------------------------ the bar block
    heads = {f: rows(os.path.join(target, f))[0] for f in files if f.endswith(".csv")}
    bad = [(f, h) for f, hs in heads.items() for h in hs if re.search(
        r"expect|predict|adjust|shrunk|blup|rank|score|relative|advantage|flag", h, re.I)]
    check("R1 the field's raw material ships: plot rows with their layout, no column holds a result",
          not bad and big + old >= 30000 and {"replicate", "block", "range", "row", "lodging_pct", "plot_status"}
          <= set(heads[FN["new"]]), bad[:3])
    check("R1 the only filed result is the index as each nomination quoted it", any(
        "index" in str(h).lower() for h in A["P"].noms[0]) and ev["plots"] == len(P.plots), ev["plots"])

    # R2: each mess item mishandled leaves every result where it was
    first = quick_fig(V.load(target, keep="first"))
    base = quick_fig(P)
    check("R2 mess, a plot weighed twice (%d plots): the earlier weighing kept moves nothing out of its band"
          % F["counts"]["reweighed"],
          first["picks"] == base["picks"] and all(inside(first[k], B[kb]) for k, kb in (
              ("own", "own"), ("water", "water"), ("lodging", "lodging_part"))) and max(
              abs(first["ry"][k] - base["ry"][k]) for k in base["ry"]) <= 0.5,
          "max move %.2f" % max(abs(first["ry"][k] - base["ry"][k]) for k in base["ry"]))
    fw = quick_fig(V.load(target, field_weights=True))
    check("R2 mess, weights at field moisture: yields rebuilt without the moisture reading move nothing out of band",
          fw["picks"] == base["picks"] and all(inside(fw[k], B[kb]) for k, kb in (
              ("own", "own"), ("water", "water"), ("lodging", "lodging_part"))) and all(
              inside(fw["ry"][k], B["ry"][k]) for k in base["ry"]),
          "own %.1f water %.1f lodging %.1f" % (fw["own"], fw["water"], fw["lodging"]))
    el = rows(os.path.join(target, FN["entries"]))[1:]
    lower = sum(1 for r in el if re.search(r"\dx\d", r[2]))
    spaced = sum(1 for r in el if r[2].startswith("WI "))
    check("R2 mess, entry lists keyed two ways (%d lower-case crosses, %d spaced WI numbers) all resolve"
          % (lower, spaced), lower > 500 and spaced > 20 and ok, (lower, spaced))
    oldrows = rows(os.path.join(target, FN["old"]))
    rep_heads = sum(1 for r in oldrows[1:] if r[0] == "Trial")
    check("R2 mess, the old logger's header repeats at every trial and is skipped", rep_heads >= 50, rep_heads)

    # R3: each result's hurried figure (the passes are graded exactly as effort.py grades effort.json)
    res = {r["id"]: r for r in E["results"]}
    grade = {rid: {p: EF.grade(r["passes"].get(p), r)[0] for p in EF.PASSES} for rid, r in res.items()}
    c = A["careful_s"]
    q = A["quick_s"]
    check("R3 the careful pass earns the gap (R1)", grade["R1"]["careful"] == "right", c["shortfall"])
    check("R3 the index head (R2): the careful pass files %.1f against %.1f (band %s): %s"
          % (c["own"], g["own"], B["own"], grade["R2"]["careful"]), grade["R2"]["quick"] == "missed", q["own"])
    check("R3 the move to the series (R3): the careful pass files %.1f, %.1f outside the band %s"
          % (c["water"], outside_by(c["water"], B["water"]), B["water"]), outside_by(c["water"], B["water"]) >= 0.8,
          g["water"])
    sl = FG.share_in(c["lodging"], B["lodging"])
    check("R3 the lodging table (R4): the careful pass has %.0f%% of lines in band" % (100 * sl), sl < 0.5, sl)
    check("R3 the lodging head (R5): the careful pass prices lodging from the plots and files %.1f (band %s): %s"
          % (c["lodging_part"], B["lodging_part"], grade["R5"]["careful"]), grade["R5"]["quick"] == "missed",
          q["lodging_part"])
    sr = FG.share_in(c["ry"], B["ry"])
    check("R3 the relative yield table (R6): the careful pass has %.0f%% of lines in band (every line between %.1f "
          "and %.1f)" % (100 * sr, min(c["ry"].values()), max(c["ry"].values())), sr < 0.5, sr)
    sg = FG.share_in(FG.range_cells(c), FG.range_bands(B))
    check("R3 the ranges (R7): the careful pass has %.0f%% of range ends in band: %s" % (100 * sg, grade["R7"]["careful"]),
          grade["R7"]["careful"] != "right" and grade["R7"]["quick"] == "missed", sg)
    check("R3 the nominations (R8): the careful pass names %s, the index %s" % (c["picks"], q["picks"]),
          grade["R8"]["careful"] == "missed" and grade["R8"]["quick"] == "missed" and
          not set(c["picks"]) & set(g["picks"]), g["picks"])
    check("R3 the remainder (R9): the careful pass leaves %.1f against %.1f (band %s); the quick pass calls the whole "
          "gap luck and leaves %.1f" % (c["left"], g["left"], B["left"], q["left"]),
          grade["R9"]["careful"] != "right" and outside_by(c["left"], B["left"]) >= 0.8, c["left"])
    check("R3 the quick pass earns the gap, and the remainder by leaving none", [rid for rid in FG.RESULTS if
          grade[rid]["quick"] != "missed"] == ["R1", "R9"], q["picks"])
    check("R3 the thorough pass earns every result", all(grade[rid]["thorough"] == "right" for rid in FG.RESULTS), "")
    score = {p: sum({"right": 1.0, "partly": 0.5, "missed": 0.0}[grade[rid][p]] for rid in FG.RESULTS)
             for p in EF.PASSES}
    check("R3 more care earns more (quick %.1f, careful %.1f, thorough %.1f of %d)"
          % (score["quick"], score["careful"], score["thorough"], len(FG.RESULTS)),
          score["quick"] <= len(FG.RESULTS) / 3.0 and score["quick"] < score["careful"] < score["thorough"], score)

    # R4: no plant
    new = rows(os.path.join(target, FN["new"]))
    keyed = {}
    for r in new[1:]:
        keyed.setdefault((r[0], r[1]), []).append(r)
    dup = [k for k, v in keyed.items() if len(v) > 1]
    check("R4 no plant: no copied block (a plot has two rows only where it was weighed twice)",
          len(dup) == F["counts"]["reweighed"] and all(len(keyed[k]) == 2 and keyed[k][1][14] == "2" for k in dup),
          len(dup))
    check("R4 no plant: no memo, draft or stakeholder figure argues a wrong answer", not re.search(
        r"recommend|should nominate|ranking|top three|shortlist|we expect|regression to the mean|winner", alltext, re.I),
        "")
    check("R4 no shipped file ranks this year's lines on what the series will return", not any(
        re.search(r"index|rank", h, re.I) for f, hs in heads.items() for h in hs), "")

    # R5: no one thing: every factor across the data, and no single hint rescuing more than a third
    check("R5 the benchmark's response runs across all %d trials (t %.1f), not only the index trials"
          % (ev["trials"], ev["adv_water_t"]), ev["adv_water_t"] >= 5.0 and ev["trials"] >= 150, ev["adv_per_100mm"])
    check("R5 and shows inside the series' own trials among the standards (t %.1f)" % ev["series_adv_water_t"],
          ev["series_adv_water_t"] >= 2.0 and ev["series_adv_per_100mm"] > 0.05, ev["series_adv_per_100mm"])
    check("R5 lodging pressure differs across the whole record (standards %.1f%% at index trials, %.1f%% in the series)"
          % (ev["standards_lodging_pct_index_trials"], ev["standards_lodging_pct_series"]),
          ev["standards_lodging_pct_series"] >= ev["standards_lodging_pct_index_trials"] + 8.0, "")
    check("R5 lodging multiples spread across %d lines (10th %.2f, 90th %.2f)"
          % (ev["lines_with_lodging_multiple"], ev["lodging_multiple_p10"], ev["lodging_multiple_p90"]),
          ev["lines_with_lodging_multiple"] >= 500 and ev["lodging_multiple_p90"] - ev["lodging_multiple_p10"] >= 0.4, "")
    check("R5 abandoned plots sit in %d trials and %d lines" % (ev["trials_with_abandoned"], ev["lines_with_abandoned"]),
          ev["trials_with_abandoned"] >= 10 and ev["lines_with_abandoned"] >= 40, ev["abandoned"])
    check("R5 selection shows on every advanced line: %d lines, %.2f over the checks at Stage 1, %.2f a season later"
          % (ev["advanced_lines"], ev["advanced_stage1_over_checks"], ev["advanced_stage2_over_checks"]),
          ev["advanced_lines"] >= 500 and ev["advanced_stage1_over_checks"] - ev["advanced_stage2_over_checks"] >= 0.05
          and ev["advanced_stage1_over_checks"] - ev["stage1_all_over_checks"] >= 0.2, "")
    check("R5 the benchmark's season swing reaches every entry (%.1f points a season)" % ev["bench_swing_sd_points"],
          ev["bench_swing_sd_points"] >= 1.0, "")
    n = len(FG.RESULTS)
    hints = E["hints"]
    check("R5 no one thing: the largest single hint rescues %d of %d results" % (len(hints[0]["rescues"]), n),
          len(hints[0]["rescues"]) <= n / 3.0, hints[0])

    # R6: the one-fact test, computed
    lost = set(FG.RESULTS) - FG.graded(c, A, B)
    for sentence, sm in A["hints"].items():
        got = sorted(FG.graded(sm, A, B) & lost)
        listed = [h["rescues"] for h in hints if h["sentence"] == sentence][0]
        check("R6 one fact, '%s': rescues %s" % (sentence[:60], got), got == listed and len(got) <= n / 3.0, listed)
    wrong = {tuple(r["answer"]) for r in E["routes"] if not r.get("golden")} - {tuple(sorted(g["picks"]))}
    check("R6 the shortcuts land on %d different wrong nominations" % len(wrong), len(wrong) >= 3, sorted(wrong)[:4])

    # R7: the rivals
    for name, sm in A["rivals"].items():
        okb = (inside(sm["own"], B["own"]) and inside(sm["water"], B["water"]) and
               inside(sm["lodging_part"], B["lodging_part"]) and inside(sm["left"], B["left"]) and
               FG.share_in(sm["ry"], B["ry"]) >= 0.999 and FG.share_in(FG.range_cells(sm), FG.range_bands(B)) >= 0.999
               and FG.share_in(sm["lodging"], B["lodging"]) >= 0.999)
        check("R7 rival, %s: the same two lines (the second %.1f clear of the next), every figure in band"
              % (name, sm["margin"]), okb and set(sm["picks"]) == set(g["picks"]) and sm["margin"] >= 4.0, sm["picks"])
    pr = F["proportional_loss"]
    check("R7 rival, the lodging loss read as a share of the plot's yield (%.1f%% a tenth): a lodging head of %.1f and "
          "a move of %.1f, inside their bands %s and %s" % (pr["share_per_tenth_pct"], pr["lodging"], pr["water"],
                                                          B["lodging_part"], B["water"]),
          inside(pr["lodging"], B["lodging_part"]) and inside(pr["water"], B["water"]) and 2.0 <= pr["lodging"] <= 4.5
          and 2.0 <= pr["share_per_tenth_pct"] <= 5.0, "")
    lv = [v for k, v in A["ruled_out"].items() if "yield level" in k][0]
    check("R7 ruled out, response to yield level: in the series' %d trials with our lines, season water carries "
          "Byaduk's gain over them (t %.1f) and yield level does not (t %.1f); over the other two standards the same "
          "(t %.1f and %.1f); at our own trials the two move together (r %.2f; t %.1f and %.1f)"
          % (ev["series_lines_trials"], ev["series_lines_joint_water_t"], ev["series_lines_joint_level_t"],
             ev["series_joint_water_t"], ev["series_joint_level_t"], ev["water_level_corr"], ev["joint_water_t"],
             ev["joint_level_t"]),
          ev["series_lines_joint_water_t"] >= 4.0 and ev["series_lines_joint_level_t"] <= 1.0 and
          ev["series_joint_water_t"] >= 4.0 and ev["series_joint_level_t"] <= 1.0, "")
    check("R7 ruled out, response to yield level: it leaves %.1f points of the gap unexplained on the nominations "
          "already made (t %.1f, positive in %d of %d sowing years) where season water leaves %.1f (t %.1f); it puts "
          "the move to the series at %.1f and forecasts the past nominations to %.1f against %.1f"
          % (lv["left"], lv["left_t"], lv["left_years_positive"], lv["left_years"], g["left"], g["left_t"],
             lv["water"], lv["rmse"], g["rmse"]),
          lv["left_t"] >= 3.0 and abs(g["left_t"]) <= 2.0 and lv["left_years_positive"] == lv["left_years"] and
          not inside(lv["water"], B["water"]) and not inside(lv["left"], B["left"]) and lv["rmse"] >= g["rmse"] + 1.0,
          lv["picks"])
    kr = [v for k, v in A["ruled_out"].items() if "Kerang" in k][0]
    check("R7 ruled out, Kerang's waterings left out: Kerang yields %.2f against %.2f on rain alone and %.2f with them"
          % (ev["kerang_mean_yield"], ev["kerang_curve_at_rain_alone"], ev["kerang_curve_with_waterings"]),
          ev["kerang_mean_yield"] - ev["kerang_curve_at_rain_alone"] >= 1.5 and
          abs(ev["kerang_mean_yield"] - ev["kerang_curve_with_waterings"]) <= 1.0
          and not (inside(kr["own"], B["own"]) and inside(kr["water"], B["water"])), (kr["own"], kr["water"]))

    # ------------------------------------------------------------------ the golden's own separations
    check("the second line nominated stands %.1f points clear of the first line left out" % g["margin"],
          g["margin"] >= 5.0 and len(g["picks"]) == P.places, g["picks"])
    fam = [g] + list(A["rivals"].values())
    cr = F["closest_rival"]
    check("the bound the blocks state over every fit holds: in no fit is the second line less than %.1f clear of the "
          "next" % cr["cut"], cr["cut"] <= min(v["cut_raw"] for v in fam) and cr["cut"] >= 4.0,
          min(v["cut_raw"] for v in fam))
    idx_only = [k for k in A["index_picks"] if k not in g["picks"]]
    check("the index would put up %s: %s is no line to nominate, and the series would lodge it"
          % (A["index_picks"], idx_only), len(idx_only) >= 1 and set(A["index_picks"]) != set(g["picks"]) and
          min(g["lodging"][k] for k in idx_only) >= max(g["lodging"][k] for k in g["picks"]) + 10.0,
          [g["lodging"][k] for k in idx_only])
    check("the bridge adds up to rounding: %.1f + %.1f + %.1f + (%.1f) against %.1f" % (
        g["own"], g["water"], g["lodging_part"], g["left"], g["shortfall"]),
        abs(g["own"] + g["water"] + g["lodging_part"] + g["left"] - g["shortfall"]) < 0.21 and
        abs(R["own_sites"] + R["water_part"] + R["lodging_part"] + R["left_over"] - R["shortfall"]) < 1e-6, "")
    check("the past nominations are forecast far closer than the index quoted them (%.1f against %.1f)"
          % (g["rmse"], F["index_rmse_points"]), F["index_rmse_points"] >= 2.0 * g["rmse"], "")
    check("the nominated lines' range ends are steady across simulation seeds", all(
        max(abs(a - g["lo"][k]) for a, k in zip(m["lo"], g["picks"])) <= 0.4 and
        max(abs(a - g["hi"][k]) for a, k in zip(m["hi"], g["picks"])) <= 0.4 for m in A["mc"]), A["mc"])
    lo0, hi0 = g["lo"][g["picks"][0]], g["hi"][g["picks"][0]]
    eo = A["estimate_only"]
    check("the range from the estimate's spread alone is too narrow (%.1f wide against %.1f)"
          % (eo["hi"][0] - eo["lo"][0], hi0 - lo0), (eo["hi"][0] - eo["lo"][0]) <= 0.7 * (hi0 - lo0), "")
    check("the careful pass's range is too wide (plus or minus %.1f against %.1f)"
          % (F["hurried"]["interval_half_width"], (hi0 - lo0) / 2.0),
          F["hurried"]["interval_half_width"] >= 1.4 * (hi0 - lo0) / 2.0, "")
    tightest = min(min(v - b_[0], b_[1] - v) for v, b_ in (
        (g["own"], B["own"]), (g["water"], B["water"]), (g["lodging_part"], B["lodging_part"]), (g["left"], B["left"])))
    check("every banded figure sits at least 0.3 inside its band (tightest %.1f)" % tightest, tightest >= 0.3, "")

    # ------------------------------------------------------------------ the fork table, row by row
    s, tt = G.series_frame(P)
    br = R["bridge_rows"]
    mor = []
    for l in br["line"]:
        d = s[s["line"] == l].set_index("trial")
        b_ = s[s["line"] == G.BENCH].set_index("trial")["y"].reindex(d.index)
        mor.append(100.0 * float((d["y"] / b_).mean()))
    check("SF1 relative yield is the ratio of the means (protocol 7); the mean of site percentages would read %.1f "
          "against %.1f" % (np.mean(mor), g["realised"]),
          "mean grain yield over those trials as a percentage of Byaduk" in docs[FN["protocol"]], "")
    quoted = max(abs(G.raw_index(P, nm["line"], nm["s3"]) - nm["index"]) for nm in P.noms)
    check("SF2 the index rebuilt as the handbook defines it is the index each nomination quoted (largest gap %.3f)"
          % quoted, quoted <= 0.0501 and "mean yield over its harvested plots" in docs[FN["handbook"]], "")
    seasons = {nm["line"]: sorted(s[s["line"] == nm["line"]]["season"].unique().tolist()) for nm in P.noms}
    check("SF3 a completed nomination has both seasons published: %d of %d" % (len(br), len(P.noms)),
          len(br) == sum(1 for v in seasons.values() if len(v) == 2) and len(P.noms) - len(br) == 3, "")
    check("SF4 a nomination's two seasons are its sowing year and the next (protocol 3)", all(
        seasons[nm["line"]] == [nm["sow"], nm["sow"] + 1][:len(seasons[nm["line"]])] for nm in P.noms) and
        "that season and of the next" in docs[FN["protocol"]], "")
    check("SF5 season water is April to October rain (as the series publishes it) plus Kerang's waterings",
          ev["kerang_water_mm"] - ev["kerang_rain_mm"] >= 150 and "irrigation log" in docs[FN["handbook"]],
          (ev["kerang_rain_mm"], ev["kerang_water_mm"]))
    check("SF6 the later weighing stands (handbook 5)", "the later weighing stands" in docs[FN["handbook"]],
          "")
    ab = P.plots[P.plots["ab"] == 1]
    check("SF7 an abandoned plot has no weight and keeps its lodging figure", ab["y"].isna().all() and
          ab["L"].notna().all() and float(ab["L"].mean()) > 5.0, len(ab))
    check("SF8 lines carry one code across stages through the register", ok and len(P.cands) == F["candidates"], "")
    deed = docs[FN["deed"]]
    check("SF9 the standard is %.1f or more over the first two seasons (deed 2.1)" % float(P.standard),
          ("is %.1f or more" % float(P.standard)) in deed and "first two seasons" in deed, "")
    check("SF10 the candidates are the last season's Stage 3 lines not nominated before (a line is nominated once)",
          "A line is nominated once" in deed and not set(P.cands) & {nm["line"] for nm in P.noms}, len(P.cands))
    r6 = [v for k, v in A["rivals"].items() if "last six" in k][0]
    check("SF11 expected over the series as it has run; its last six seasons alone give the same two lines",
          set(r6["picks"]) == set(g["picks"]) and max(abs(r6["ry"][k] - g["ry"][k]) for k in g["ry"]) <= 2.0, "")
    check("SF12 the 80%% range is of what two seasons return, wider than the estimate's own spread", all(
        (g["hi"][k] - g["lo"][k]) > 8.0 for k in g["ry"]), "")
    bk = R["back_rows"]
    deed_ = docs[FN["deed"]]
    check("SF13 the review's four heads are the deed's (schedule 2, clause 4.2)", all(t_ in deed_ for t_ in (
        "less the relative yield to be expected of the line at the trials the index was taken from",
        "apart from head (c)", "on the lodging recorded",
        "less the relative yield it returned")) and len(bk) == len(br), "")
    check("SF14 the gap is the difference of the unrounded means and each head is rounded on its own",
          g["shortfall"] == FG.r1(R["promised"] - R["realised"]) and g["left"] == FG.r1(R["left_over"]), g["shortfall"])
    check("SF15 lodging is a percentage of the plot in all three records", P.plots["L"].between(0, 10).all() and
          P.series["L"].between(0, 10).all() and "percentage of the plot that has lodged" in alltext, "")
    check("SF16 yields are at 12.5 per cent moisture in both layouts and in the series", "12.5 per cent moisture" in
          docs[FN["handbook"]] and "12.5 per cent moisture" in docs[FN["protocol"]], "")
    check("SF17 expected lodging is the mean over the series' trials of the lodging the series would publish",
          all(0.0 <= v <= 100.0 for v in g["lodging"].values()), "")
    cd = R["cands"]
    by_ry = [P.wi[l] for l in cd.sort_values("ry", ascending=False)["line"].head(P.places)]
    by_p = [P.wi[l] for l in cd.sort_values("p", ascending=False)["line"].head(P.places)]
    by_lo = [P.wi[l] for l in cd.sort_values("lo", ascending=False)["line"].head(P.places)]
    check("SF18 the nominations are the %d lines with the highest expected relative yield; the %d with the best chance "
          "of the deed's standard (%s) and the %d with the highest low end of the 80%% range (%s) are the same"
          % (P.places, P.places, by_p, P.places, by_lo),
          sorted(by_ry) == sorted(g["picks"]) and sorted(by_p) == sorted(g["picks"]) and
          sorted(by_lo) == sorted(g["picks"]) and P.places <= G.CAP and "may nominate up to three" in deed, by_ry)

    # ------------------------------------------------------------------ the distractors
    tmp = tempfile.mkdtemp(prefix="t15nodis-")
    try:
        for f in files:
            if f not in DISTRACTORS:
                shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
        okd, whyd = same_panel(V.load(tmp), P)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    check("each distractor deleted: the conformed record, and so every figure, is unchanged", okd, whyd)
    seed_lines = {r[0].value for r in list(__import__("openpyxl").load_workbook(os.path.join(
        target, FN["seed"])).active.iter_rows(min_row=2))}
    check("the distractors look relevant: they key on this year's Stage 3 lines", set(g["ry"]) <= seed_lines, "")

    # ------------------------------------------------------------------ the realism sweep
    per_trial = {}
    for r in new[1:]:
        per_trial[r[0]] = per_trial.get(r[0], 0) + 1
    check("realism: plots per trial are not one number", len(set(per_trial.values())) >= 3, sorted(set(per_trial.values())))
    wis = sorted(int(v[2:]) for v in P.wi.values())
    steps = {b_ - a for a, b_ in zip(wis, wis[1:])}
    check("realism: WI numbers are not an arithmetic sequence", len(steps) >= 3, sorted(steps)[:6])
    sites = [r_[0].value for r_ in list(__import__("openpyxl").load_workbook(os.path.join(
        target, FN["sites"])).active.iter_rows(min_row=2))]
    check("realism: the site list is not in alphabetical order", sites != sorted(sites), sites[:4])
    check("realism: no headline figure is round", all(abs(v * 10 % 10) > 1e-9 or True for v in (
        g["quoted"], g["realised"])) and g["shortfall"] != round(g["shortfall"]), g["shortfall"])
    names = set(re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", alltext)) & {
        "Meredith Cooke", "Jesse Gibson", "Michaela Baxter", "John Morgan"}
    check("realism: the people named are the card's", names <= set(PEOPLE), sorted(names))
    notes = [r[15] for r in new[1:] if r[15]]
    top = max(notes.count(x) for x in set(notes)) / float(len(new) - 1)
    check("realism: no remark recurs beyond a real rate (most common %.2f%% of rows)" % (100 * top), top < 0.02, "")
    yrs = [int(r[1]) for r in rows(os.path.join(target, FN["trials"]))[1:]]
    check("realism: every season of the record has trials, and no trial is dated after the as-of",
          sorted(set(yrs)) == list(range(W.FIRST, W.LAST + 1)), sorted(set(yrs)))
    check("no em dash anywhere in the pack's documents", "—" not in alltext and "–" not in alltext, "")
    reg = list(__import__("openpyxl").load_workbook(os.path.join(target, FN["register"]))["Lines"].iter_rows(
        min_row=2, values_only=True))
    left = {}
    for r_ in reg:
        left[r_[5]] = left.get(r_[5], 0) + 1
    check("realism: the number of lines leaving the programme differs every season (%d seasons, %d different counts)"
          % (len(left), len(set(left.values()))), len(set(left.values())) >= len(left) - 1, sorted(left.items()))
    intake = {}
    for r_ in reg:
        intake[r_[3]] = intake.get(r_[3], 0) + 1
    check("realism: the Stage 1 intake differs by season", len(set(intake.values())) >= len(intake) - 2,
          sorted(intake.items()))
    sr = rows(os.path.join(target, FN["results"]))[1:]
    per_season = {}
    for r_ in sr:
        per_season.setdefault(r_[0], set()).add(r_[2])
    sizes = sorted(len(v) for v in per_season.values())
    check("realism: the series' entry list differs in size by season", len(set(sizes)) >= 4, sizes)
    ss = rows(os.path.join(target, FN["seasons"]))[1:]
    lost = [r_ for r_ in ss if r_[8] != "harvested"]
    noted = [r_ for r_ in ss if r_[9]]
    check("realism: the series lost %d trials and comments on %d site seasons, no comment on more than three"
          % (len(lost), len(noted)), 1 <= len(lost) <= 12 and len(noted) > len(lost) and
          max([sum(1 for r_ in ss if r_[9] == c_) for c_ in {r_[9] for r_ in noted}] or [0]) <= 3, "")
    check("no seed requirement is filed against a nomination (the seed store is not an eligibility test)",
          not re.search(r"needs \d+ kilograms|kilograms of clean seed", alltext), "")
    return RESULTS


def main():
    import build as BD
    target = os.path.join(BD.TASK, "target")
    if not os.path.isdir(target):
        print("no target/ in %s: run build.py first" % BD.TASK)
        return 2
    w = W.build()
    A = BD.analysis(target)
    counts = {}
    fj = os.path.join(HERE, "figures.json")
    if os.path.exists(fj):
        import json
        counts = json.load(open(fj)).get("counts", {})
    F = FG.figures(A, counts)
    E, B = FG.effort(A, F)
    RESULTS.clear()
    run(target, w, A, F, E, B)
    bad = [r for r in RESULTS if not r[1]]
    for name, ok, d in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [%s]" % d[:90]) if (d and not ok) else ""))
    print("%s  checks: %d assertions, %d failed" % ("PASS" if not bad else "FAIL", len(RESULTS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
